#!/usr/bin/env python3
"""
figma-to-brand-spec.py — extract a team-brand-spec.json from a Figma file.

Reads a Figma file via the public REST API (or an offline fixture for
testing), walks the document tree, finds nodes that reference named
styles (color / text / effect), maps style names to spec slots using
a slash-separated naming convention, and emits a JSON spec compatible
with `assets/team-brand-spec.default.json`.

Naming convention (Figma style name → spec slot):

    color/accent/primary            → colors.accent.primary
    color/surface/base_dark         → colors.surface.base_dark
    color/status/success_light      → colors.status.success_light
    text/display/family             → typography.display.family
    text/body/family                → typography.body.family
    effect/shadow/subtle            → design_system.shadow_tokens.subtle

Styles whose names don't match a known prefix are recorded under
`_unmapped` so adopters can see what was skipped and either rename
the Figma styles or extend their carrier file manually.

Usage:
    # Online (requires FIGMA_TOKEN env var; token from
    # https://www.figma.com/developers/api#access-tokens):
    FIGMA_TOKEN=figd_... python3 scripts/figma-to-brand-spec.py <FILE_KEY>

    # Offline (fixture):
    python3 scripts/figma-to-brand-spec.py --fixture path/to/fixture.json

    # Pin output path (default: team-brand-spec.json at cwd):
    python3 scripts/figma-to-brand-spec.py <FILE_KEY> --output spec.json

    # Don't merge over a starter file (default: merge into the default
    # spec so untouched groups still have evidence-anchored values):
    python3 scripts/figma-to-brand-spec.py <FILE_KEY> --no-merge

    # Merge into a custom starter (use a per-team carrier as base):
    python3 scripts/figma-to-brand-spec.py <FILE_KEY> --base team-brand-spec.json

Exit codes:
    0  written
    1  missing token, missing fixture, Figma API error, invalid JSON,
       write failure, or refusal to overwrite without --force

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Generator

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE = REPO_ROOT / "assets" / "team-brand-spec.default.json"
DEFAULT_OUTPUT = Path("team-brand-spec.json")

FIGMA_API = "https://api.figma.com/v1"


# ──────────────────────────────────────────────────────────────────────
# Figma API
# ──────────────────────────────────────────────────────────────────────

def fetch_figma_file(file_key: str, token: str) -> dict:
    """Fetch a Figma file's tree + style index in one call.

    Returns the parsed JSON. Raises urllib.error.HTTPError on non-2xx.
    """
    url = f"{FIGMA_API}/files/{file_key}"
    req = urllib.request.Request(url, headers={"X-Figma-Token": token})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ──────────────────────────────────────────────────────────────────────
# Extraction
# ──────────────────────────────────────────────────────────────────────

def _walk(node: dict) -> Generator[dict, None, None]:
    """Recursively yield every node in a Figma document tree."""
    if not isinstance(node, dict):
        return
    yield node
    for child in node.get("children", []) or []:
        yield from _walk(child)


def _solid_fill_hex(node: dict) -> str | None:
    """If node has a visible solid fill, return its hex (uppercase).

    Returns None when no solid fill is found or its alpha is 0.
    """
    for fill in node.get("fills", []) or []:
        if not isinstance(fill, dict):
            continue
        if fill.get("type") != "SOLID":
            continue
        if fill.get("visible") is False:
            continue
        color = fill.get("color") or {}
        try:
            r = int(round(float(color.get("r", 0)) * 255))
            g = int(round(float(color.get("g", 0)) * 255))
            b = int(round(float(color.get("b", 0)) * 255))
        except (TypeError, ValueError):
            continue
        a = color.get("a", 1)
        # opacity field on fill overrides color.a for fills
        opacity = fill.get("opacity", 1)
        if (a is not None and a <= 0) or (opacity is not None and opacity <= 0):
            continue
        return f"#{r:02X}{g:02X}{b:02X}"
    return None


def _text_style_meta(node: dict) -> dict | None:
    """Extract font family / weight / size / line-height from a text node."""
    style = node.get("style")
    if not isinstance(style, dict):
        return None
    meta: dict[str, Any] = {}
    if "fontFamily" in style:
        meta["family"] = style["fontFamily"]
    if "fontWeight" in style:
        meta["weight"] = style["fontWeight"]
    if "fontSize" in style:
        meta["size"] = style["fontSize"]
    # lineHeightPx is the resolved px value Figma exposes
    if "lineHeightPx" in style:
        meta["line_height_px"] = style["lineHeightPx"]
    return meta or None


def extract_named_styles(file_data: dict) -> tuple[dict, dict]:
    """Walk the document and resolve each named style to its concrete value.

    Returns `(paint_styles, text_styles)` where each maps style name
    (e.g. "color/accent/primary") to the resolved value (hex string
    for paint, dict for text).
    """
    style_index = file_data.get("styles", {}) or {}
    paint: dict[str, str] = {}
    text: dict[str, dict] = {}

    doc = file_data.get("document") or {}
    for node in _walk(doc):
        styles_ref = node.get("styles") or {}
        if not isinstance(styles_ref, dict):
            continue

        # Color: Figma uses "fill" (singular) for the style reference
        fill_sid = styles_ref.get("fill")
        if fill_sid and fill_sid in style_index:
            name = style_index[fill_sid].get("name")
            if name and name not in paint:
                hex_value = _solid_fill_hex(node)
                if hex_value:
                    paint[name] = hex_value

        # Text style
        text_sid = styles_ref.get("text")
        if text_sid and text_sid in style_index:
            name = style_index[text_sid].get("name")
            if name and name not in text:
                meta = _text_style_meta(node)
                if meta:
                    text[name] = meta

    return paint, text


# ──────────────────────────────────────────────────────────────────────
# Spec mapping
# ──────────────────────────────────────────────────────────────────────

# Recognised top-level slash prefixes. A Figma style named
# "color/accent/primary" maps to spec path colors.accent.primary.
_PREFIX_MAP = {
    "color": "colors",
    "colors": "colors",
    "text": "typography",
    "type": "typography",
    "typography": "typography",
    "effect": "design_system.shadow_tokens",
    "shadow": "design_system.shadow_tokens",
}


def slot_for(style_name: str) -> str | None:
    """Translate a Figma style name to a dotted spec slot path.

    Returns None when the name doesn't start with a known prefix.
    """
    if not style_name or "/" not in style_name:
        return None
    head, _, rest = style_name.partition("/")
    head_clean = head.strip().lower()
    base = _PREFIX_MAP.get(head_clean)
    if not base:
        return None
    rest_clean = ".".join(seg.strip() for seg in rest.split("/") if seg.strip())
    if not rest_clean:
        return None
    return f"{base}.{rest_clean}"


def _set_nested(target: dict, dotted: str, value: Any) -> None:
    """Set `target[a][b][c] = value` for dotted path "a.b.c"."""
    parts = dotted.split(".")
    cursor = target
    for part in parts[:-1]:
        nxt = cursor.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cursor[part] = nxt
        cursor = nxt
    cursor[parts[-1]] = value


def build_spec(file_data: dict, base_spec: dict | None = None) -> dict:
    """Turn Figma file data into a team-brand-spec-shaped dict.

    When `base_spec` is provided, extracted values are merged on top
    of it (deep-overwriting only the slots that the Figma file
    actually defines), so untouched groups keep their evidence-anchored
    defaults from `team-brand-spec.default.json`.
    """
    paint, text = extract_named_styles(file_data)
    spec: dict[str, Any] = json.loads(json.dumps(base_spec)) if base_spec else {}

    unmapped: list[dict] = []

    for name, hex_value in paint.items():
        slot = slot_for(name)
        if slot:
            _set_nested(spec, slot, hex_value)
        else:
            unmapped.append({"figma_name": name, "value": hex_value, "kind": "color"})

    for name, meta in text.items():
        slot = slot_for(name)
        if slot:
            _set_nested(spec, slot, meta)
        else:
            unmapped.append({"figma_name": name, "value": meta, "kind": "text"})

    spec.setdefault("_meta", {})
    spec["_meta"]["extracted_from"] = file_data.get("name", "Unknown Figma file")
    last_modified = file_data.get("lastModified")
    if last_modified:
        spec["_meta"]["extracted_at"] = last_modified
    spec["_meta"]["tool"] = "scripts/figma-to-brand-spec.py"
    if unmapped:
        spec["_meta"]["unmapped_styles"] = unmapped

    return spec


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract a team-brand-spec.json from a Figma file.",
    )
    ap.add_argument(
        "file_key",
        nargs="?",
        help="Figma file key (the segment after /file/ in the URL). "
        "Omit when using --fixture.",
    )
    ap.add_argument(
        "--fixture",
        type=Path,
        help="Path to a JSON fixture mimicking a Figma file response. "
        "Used by tests and for offline runs; takes precedence over file_key.",
    )
    ap.add_argument(
        "--token",
        default=os.environ.get("FIGMA_TOKEN"),
        help="Figma personal access token (default: $FIGMA_TOKEN). "
        "Required when --fixture is not given.",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write the spec (default: team-brand-spec.json at cwd).",
    )
    ap.add_argument(
        "--base",
        type=Path,
        default=DEFAULT_BASE,
        help="Starter spec to merge extracted values into "
        "(default: assets/team-brand-spec.default.json). "
        "Use --no-merge to disable.",
    )
    ap.add_argument(
        "--no-merge",
        action="store_true",
        help="Don't merge into a starter; emit only the extracted slots.",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it exists.",
    )
    args = ap.parse_args(argv)

    if args.output.exists() and not args.force:
        sys.stderr.write(f"ERROR: output already exists at {args.output}\n")
        sys.stderr.write("       Re-run with --force to overwrite, or pick a different --output.\n")
        return 1

    # Load Figma file data
    if args.fixture:
        if not args.fixture.exists():
            sys.stderr.write(f"ERROR: fixture not found at {args.fixture}\n")
            return 1
        try:
            file_data = json.loads(args.fixture.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sys.stderr.write(f"ERROR: fixture is not valid JSON: {e}\n")
            return 1
    else:
        if not args.file_key:
            sys.stderr.write("ERROR: file_key is required (or use --fixture).\n")
            return 1
        if not args.token:
            sys.stderr.write(
                "ERROR: no Figma token. Set FIGMA_TOKEN env var or pass --token.\n"
                "       Get one at https://www.figma.com/developers/api#access-tokens\n"
            )
            return 1
        try:
            file_data = fetch_figma_file(args.file_key, args.token)
        except urllib.error.HTTPError as e:
            sys.stderr.write(f"ERROR: Figma API {e.code}: {e.reason}\n")
            return 1
        except urllib.error.URLError as e:
            sys.stderr.write(f"ERROR: Figma API unreachable: {e.reason}\n")
            return 1

    # Load optional base spec
    base_spec: dict | None = None
    if not args.no_merge:
        if not args.base.exists():
            sys.stderr.write(
                f"WARN: base spec {args.base} not found; emitting extracted slots only.\n"
            )
        else:
            try:
                base_spec = json.loads(args.base.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                sys.stderr.write(f"ERROR: base spec is not valid JSON: {e}\n")
                return 1

    spec = build_spec(file_data, base_spec=base_spec)

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as e:
        sys.stderr.write(f"ERROR: write failed: {e}\n")
        return 1

    # Re-parse to confirm round-trip JSON validity.
    try:
        json.loads(args.output.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"ERROR: the file we just wrote is not valid JSON: {e}\n")
        return 1

    extracted_count = len(spec.get("_meta", {}).get("unmapped_styles", [])) + sum(
        1 for slot in ("colors", "typography", "design_system")
        if slot in spec
    )
    print(f"✓ wrote {args.output}")
    unmapped = spec.get("_meta", {}).get("unmapped_styles") or []
    if unmapped:
        print(f"  {len(unmapped)} style(s) had unrecognised names — see _meta.unmapped_styles.")
        print("  Rename them in Figma using the slash convention or extend the spec manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
