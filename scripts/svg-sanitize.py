#!/usr/bin/env python3
"""
svg-sanitize.py — whitelist-based SVG sanitizer for the internal-fork skill.

Reads an SVG file, strips disallowed tags / attributes / CSS tokens,
records SHA-256 hashes and findings to a provenance markdown file.

Policy lives in references/svg-sanitize.md (§1 tags, §2 attributes).
This script is the executable side of that policy.

Usage:
    python svg-sanitize.py --in <source.svg> --out <safe.svg> --report <PROVENANCE.md>
    python svg-sanitize.py --in <source.svg> --out <safe.svg> --strict   # exit non-zero on any strip

Exit codes:
    0  clean (or clean after harmless strips)
    2  parse error (malformed XML or external entity attempted)
    3  policy violation flagged (script / foreignObject / javascript: URL found)

Dependencies: only stdlib (xml.etree, hashlib, re, argparse). lxml not required.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

# §1 · Allowed tags (svg-sanitize.md)
ALLOWED_TAGS = frozenset({
    "svg", "defs", "g", "use", "symbol", "marker",
    "path", "circle", "rect", "line", "polyline", "polygon", "ellipse",
    "text", "tspan", "textPath",
    "title", "desc",
    "linearGradient", "radialGradient", "stop", "pattern",
    "clipPath", "mask",
    "filter",
    "feGaussianBlur", "feOffset", "feFlood", "feComposite", "feColorMatrix",
    "feMerge", "feMergeNode", "feTurbulence", "feDisplacementMap", "feMorphology",
    "feBlend", "feSpecularLighting", "feDiffuseLighting", "feDistantLight", "fePointLight",
    "animate", "animateTransform",
    "style",
})

# Always-strip tags (even if listed in custom configs — these are dangerous)
DANGEROUS_TAGS = frozenset({
    "script", "foreignObject", "iframe", "object", "embed",
    "image", "audio", "video", "handler", "set",
})

# §2 · Allowed attributes
ALLOWED_ATTRS = frozenset({
    # Geometry
    "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry",
    "width", "height", "points", "d", "transform",
    "viewBox", "preserveAspectRatio",
    # Visual
    "fill", "stroke", "stroke-width",
    "stroke-linecap", "stroke-linejoin",
    "stroke-dasharray", "stroke-dashoffset", "stroke-miterlimit",
    "stroke-opacity", "fill-opacity", "opacity",
    "fill-rule", "clip-rule",
    "stop-color", "stop-opacity", "offset",
    "gradientUnits", "gradientTransform", "spreadMethod",
    "mask", "clip-path", "filter",
    # Typography
    "font-family", "font-size", "font-weight", "font-style",
    "text-anchor", "letter-spacing", "word-spacing",
    "dominant-baseline", "alignment-baseline",
    # Identification + a11y
    "id", "class",
    "aria-label", "aria-labelledby", "aria-describedby", "role",
    # Namespace
    "xmlns", "xmlns:xlink", "xml:space",
    # Style (handled by CSS sub-sanitizer)
    "style",
    # Animation declarative
    "attributeName", "from", "to", "dur", "begin", "end",
    "repeatCount", "values", "keyTimes",
})

# href is conditionally allowed only on <use> with intra-document fragment
HREF_FRAGMENT_RE = re.compile(r"^#[A-Za-z][A-Za-z0-9_-]*$")

# CSS sanitize: forbidden tokens inside style="" or <style>
CSS_FORBIDDEN_TOKEN_RE = re.compile(
    r"""
    \burl\s*\(           # url()
    | @import            # external import
    | \bexpression\s*\(  # IE expression
    | javascript:        # javascript: URL
    | \bbehavior\s*:     # IE behavior
    | data:text/html     # data URL of html
    """,
    re.IGNORECASE | re.VERBOSE,
)


def localname(tag: str) -> str:
    """Strip XML namespace prefix from a tag like '{http://...}path' -> 'path'."""
    return tag.split("}", 1)[1] if "}" in tag else tag


def localname_attr(attr: str) -> str:
    """Strip namespace from an attribute, but keep xmlns:* for namespace decls."""
    if "}" not in attr:
        return attr
    ns, local = attr[1:].split("}", 1)
    if ns == XLINK_NS and local == "href":
        return "xlink:href"
    return local


def sanitize_css(css: str, findings: list[str], where: str) -> str:
    """Drop CSS declarations containing forbidden tokens. Returns the filtered CSS."""
    if not css:
        return css
    if CSS_FORBIDDEN_TOKEN_RE.search(css):
        findings.append(f"CSS sanitize: stripped forbidden tokens in {where}")
        return ""  # nuke the entire style — safer than partial
    return css


def is_dangerous_value(value: str) -> bool:
    """Catch javascript:, data:text/html, and on* event payloads sneaking via attrs."""
    if not value:
        return False
    v = value.strip().lower()
    if v.startswith("javascript:"):
        return True
    if v.startswith("data:text/html"):
        return True
    return False


def sanitize_element(el: ET.Element, findings: list[str], dangerous_flag: list[bool]) -> ET.Element | None:
    """Sanitize a single element in place. Returns None if the whole element should be dropped."""
    tag = localname(el.tag)

    # 1. Dangerous tags — drop the entire subtree, raise the policy flag
    if tag in DANGEROUS_TAGS:
        findings.append(f"Dropped <{tag}> (dangerous tag)")
        dangerous_flag[0] = True
        return None

    # 2. Tag not in whitelist — drop
    if tag not in ALLOWED_TAGS:
        findings.append(f"Dropped <{tag}> (not in allowlist)")
        return None

    # 3. Attribute pass — copy allowed, strip the rest
    new_attribs: dict[str, str] = {}
    for raw_attr, value in list(el.attrib.items()):
        attr = localname_attr(raw_attr)

        # Strip every event handler attribute
        if attr.startswith("on"):
            findings.append(f"Stripped event handler {attr} on <{tag}>")
            dangerous_flag[0] = True
            continue

        # Strip dangerous-value attributes
        if is_dangerous_value(value):
            findings.append(f"Stripped {attr}=javascript:/data:text-html on <{tag}>")
            dangerous_flag[0] = True
            continue

        # href / xlink:href — only allow intra-document fragment on <use>
        if attr in ("href", "xlink:href"):
            if tag == "use" and HREF_FRAGMENT_RE.match(value or ""):
                new_attribs[raw_attr] = value
            else:
                findings.append(f"Stripped {attr} on <{tag}> (only intra-doc fragment on <use> allowed)")
                if value and not value.startswith("#"):
                    dangerous_flag[0] = True
            continue

        # Standard whitelist
        if attr in ALLOWED_ATTRS:
            if attr == "style":
                value = sanitize_css(value, findings, f"style attr on <{tag}>")
                if not value:
                    continue
            new_attribs[raw_attr] = value
            continue

        # xmlns:* declarations (namespace) are fine
        if attr.startswith("xmlns"):
            new_attribs[raw_attr] = value
            continue

        # Anything else — strip
        findings.append(f"Stripped attr {attr} on <{tag}>")

    el.attrib.clear()
    el.attrib.update(new_attribs)

    # 4. Special handling for <style> element text
    if tag == "style" and el.text:
        cleaned = sanitize_css(el.text, findings, "<style> element body")
        el.text = cleaned

    # 5. Recurse children — replace each child with its sanitized version, drop None
    new_children: list[ET.Element] = []
    for child in list(el):
        sanitized_child = sanitize_element(child, findings, dangerous_flag)
        if sanitized_child is not None:
            new_children.append(sanitized_child)

    # rebuild children list
    for child in list(el):
        el.remove(child)
    for child in new_children:
        el.append(child)

    return el


def parse_xml_safe(data: bytes) -> ET.Element:
    """Parse XML rejecting DOCTYPE / external entities at the byte level (XXE guard)."""
    # xml.etree's underlying expat does NOT resolve external entities by default,
    # so the only XXE risk left is in-document DOCTYPE / ENTITY declarations.
    # Reject those at the byte level before parsing — fastest and cleanest.
    head = data[:4096].lower()
    if b"<!doctype" in head or b"<!entity" in head:
        raise ValueError("DOCTYPE / ENTITY declarations not allowed (XXE guard)")
    return ET.fromstring(data)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _xml_comment_safe(text: str) -> str:
    """Make a string safe to embed in an XML comment: no '--', no trailing dash."""
    s = text.replace("--", "- -").replace("\n", " ").replace("\r", " ")
    if s.endswith("-"):
        s += " "
    return s


def append_provenance(report_path: Path, in_path: Path, out_path: Path,
                      in_hash: str, out_hash: str,
                      findings: list[str], dangerous: bool, source_url: str | None) -> None:
    """Append a provenance record to the report markdown."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    if not report_path.exists():
        report_path.write_text(
            "# Asset PROVENANCE\n\n"
            "Audit trail for every external asset brought into this project. "
            "Maintained by `scripts/svg-sanitize.py`.\n\n",
            encoding="utf-8",
        )

    section = io.StringIO()
    section.write(f"\n## {in_path.name} → {out_path.name}\n")
    section.write(f"- Date: {date.today().isoformat()}\n")
    if source_url:
        section.write(f"- Source: {source_url}\n")
    section.write(f"- Input  SHA-256: `{in_hash}`\n")
    section.write(f"- Output SHA-256: `{out_hash}`\n")
    if findings:
        section.write("- Sanitizer findings:\n")
        for f in findings:
            section.write(f"  - {f}\n")
    else:
        section.write("- Sanitizer findings: clean (no strips)\n")
    section.write(f"- Policy violation flag: {'YES (review required)' if dangerous else 'no'}\n")

    with report_path.open("a", encoding="utf-8") as fh:
        fh.write(section.getvalue())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", required=True, help="path to source .svg")
    ap.add_argument("--out", dest="dst", required=True, help="path for sanitized output .svg")
    ap.add_argument("--report", help="PROVENANCE.md path (appended). Optional.")
    ap.add_argument("--source-url", default=None, help="original URL — recorded in PROVENANCE")
    ap.add_argument("--strict", action="store_true", help="exit non-zero if anything was stripped")
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)

    try:
        data = src.read_bytes()
    except OSError as exc:
        print(f"ERROR: cannot read {src}: {exc}", file=sys.stderr)
        return 2

    in_hash = sha256(data)

    try:
        root = parse_xml_safe(data)
    except (ET.ParseError, ValueError) as exc:
        print(f"ERROR: parse failed: {exc}", file=sys.stderr)
        return 2

    findings: list[str] = []
    dangerous_flag = [False]
    sanitized = sanitize_element(root, findings, dangerous_flag)

    if sanitized is None:
        print("ERROR: root element was rejected — nothing to write", file=sys.stderr)
        return 3

    # Serialize. Preserve XML declaration. Default namespace registration keeps things readable.
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XLINK_NS)
    out_bytes = ET.tostring(sanitized, encoding="utf-8", xml_declaration=True)

    # Visibility guard: when anything was stripped, prepend a comment to the SVG body so
    # the sanitization is discoverable from the file alone (not only via PROVENANCE.md).
    # Aligns with svg-sanitize.md §"sanitize-fail produces visible trace, never silent".
    if findings:
        head = findings[:3]
        suffix = f" (+{len(findings) - 3} more)" if len(findings) > 3 else ""
        summary = "; ".join(_xml_comment_safe(f) for f in head) + suffix
        flag = " POLICY-VIOLATION" if dangerous_flag[0] else ""
        comment = f"<!-- svg-sanitize: stripped {len(findings)} item(s){flag} - {summary} -->\n"
        out_str = out_bytes.decode("utf-8")
        if out_str.startswith("<?xml"):
            end_decl = out_str.index("?>") + 2
            out_str = out_str[:end_decl] + "\n" + comment + out_str[end_decl:].lstrip("\n")
        else:
            out_str = comment + out_str
        out_bytes = out_str.encode("utf-8")

    out_hash = sha256(out_bytes)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(out_bytes)

    if args.report:
        append_provenance(
            Path(args.report), src, dst, in_hash, out_hash,
            findings, dangerous_flag[0], args.source_url,
        )

    # Console summary
    if not findings:
        print(f"✓ clean: {src.name} → {dst.name}")
    else:
        flag = " [POLICY VIOLATION]" if dangerous_flag[0] else ""
        print(f"⚠ stripped {len(findings)} item(s): {src.name} → {dst.name}{flag}")
        for f in findings:
            print(f"   · {f}")

    if dangerous_flag[0]:
        return 3
    if args.strict and findings:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
