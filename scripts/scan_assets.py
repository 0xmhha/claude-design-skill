#!/usr/bin/env python3
"""
scan_assets.py — defensive scanner for image assets ingested into the skill.

Sits next to scripts/svg-sanitize.py and covers the formats svg-sanitize cannot
parse: PNG and JPG. The two scanners look for footprints typical of careless
or hostile asset hand-offs:

    * Trailing bytes after the file's logical EOF (PNG IEND, JPG FFD9)
    * Non-whitelist PNG chunks
    * Oversized PNG text metadata (tEXt / iTXt / zTXt over a soft cap)
    * Non-whitelist JPG markers
    * Oversized JPG comment / APPn segments
    * Truncated containers (length runs past the file)

Out of scope (intentionally — these need dedicated tools):
    * LSB steganography statistical analysis
    * Polyglot detection beyond trailing bytes
    * GIF / WebP / AVIF — add when the team starts using them

Usage:
    python3 scripts/scan_assets.py --file <path>
    python3 scripts/scan_assets.py --dir <path> [--exts png,jpg,jpeg,gif]
    python3 scripts/scan_assets.py --file <path> --report PROVENANCE.md
    python3 scripts/scan_assets.py --dir assets/ --advisory
    python3 scripts/scan_assets.py --file <path> --strict

Exit codes:
    0  no findings, or only INFO findings
    2  one or more WARN findings
    3  one or more CRITICAL findings (e.g. trailing data after EOF)
    1  CLI / IO error

`--advisory` forces exit 0 unless an IO error occurred — used by CI as a
reporting-only gate. `--strict` escalates WARN to CRITICAL.

Stdlib only. No PIL / no Pillow / no exifread.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# --- Limits ----------------------------------------------------------------

PNG_TEXT_CHUNK_SOFT_CAP = 4 * 1024            # 4 KB inline text is plenty
JPG_COMMENT_SOFT_CAP = 4 * 1024
TRAILING_BYTES_INFO_THRESHOLD = 0             # any trailing byte = CRITICAL


# --- PNG -------------------------------------------------------------------

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

PNG_WHITELIST = {
    "IHDR", "PLTE", "IDAT", "IEND",
    "tRNS", "cHRM", "gAMA", "iCCP", "sBIT", "sRGB",
    "iTXt", "tEXt", "zTXt",
    "bKGD", "hIST", "pHYs", "sPLT", "tIME",
    "acTL", "fcTL", "fdAT",
    "eXIf",
}
PNG_TEXT_CHUNKS = {"tEXt", "iTXt", "zTXt"}


def _scan_png(data: bytes) -> list["Finding"]:
    out: list[Finding] = []
    if not data.startswith(PNG_SIGNATURE):
        out.append(Finding("CRITICAL", "PNG signature missing"))
        return out

    pos = len(PNG_SIGNATURE)
    saw_iend = False
    iend_at = -1
    while pos + 12 <= len(data):
        length = int.from_bytes(data[pos:pos + 4], "big")
        ctype = data[pos + 4:pos + 8].decode("ascii", errors="replace")
        chunk_end = pos + 8 + length + 4

        if chunk_end > len(data):
            out.append(Finding("CRITICAL", f"truncated chunk {ctype!r} at offset {pos} (length {length} runs past EOF)"))
            return out

        if ctype not in PNG_WHITELIST:
            out.append(Finding("WARN", f"non-whitelist chunk {ctype!r} at offset {pos} (length {length})"))

        if ctype in PNG_TEXT_CHUNKS and length > PNG_TEXT_CHUNK_SOFT_CAP:
            out.append(Finding("WARN", f"{ctype} chunk size {length} exceeds soft cap {PNG_TEXT_CHUNK_SOFT_CAP}"))

        if ctype == "IEND":
            saw_iend = True
            iend_at = chunk_end
            pos = chunk_end
            break

        pos = chunk_end

    if not saw_iend:
        out.append(Finding("CRITICAL", "no IEND chunk — file may be truncated"))
        return out

    trailing = len(data) - iend_at
    if trailing > TRAILING_BYTES_INFO_THRESHOLD:
        out.append(Finding("CRITICAL", f"{trailing} bytes after IEND — probable polyglot or stuffed payload"))

    return out


# --- JPG -------------------------------------------------------------------

JPG_SOI = b"\xff\xd8"
JPG_EOI = b"\xff\xd9"

# Standalone (no length) markers per JFIF / EXIF / JPEG.
JPG_STANDALONE = {0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0x01}

# Whitelist of length-bearing markers we expect in a normal JPEG.
JPG_LENGTHED_WHITELIST = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF,
    0xFE,
} | {0xE0 + n for n in range(16)}  # APP0..APP15


def _scan_jpg(data: bytes) -> list["Finding"]:
    out: list[Finding] = []
    if not data.startswith(JPG_SOI):
        out.append(Finding("CRITICAL", "JPG SOI (FFD8) missing"))
        return out

    pos = 2
    saw_eoi = False
    eoi_at = -1
    while pos < len(data):
        if data[pos] != 0xFF:
            out.append(Finding("CRITICAL", f"expected marker prefix 0xFF at offset {pos}, got {data[pos]:#04x}"))
            return out

        # Marker prefixes can be padded with 0xFF — skip them.
        while pos + 1 < len(data) and data[pos + 1] == 0xFF:
            pos += 1

        if pos + 1 >= len(data):
            out.append(Finding("CRITICAL", "EOF reached inside marker"))
            return out

        marker = data[pos + 1]

        if marker == 0xD9:  # EOI
            saw_eoi = True
            eoi_at = pos + 2
            pos = eoi_at
            break

        if marker == 0xDA:  # SOS — entropy-coded data follows; scan forward to next non-padded FF Mxx
            pos += 2
            length = int.from_bytes(data[pos:pos + 2], "big")
            pos += length
            # Walk through entropy-coded segment
            while pos + 1 < len(data):
                if data[pos] == 0xFF and data[pos + 1] != 0x00 and data[pos + 1] not in (0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7):
                    break
                pos += 1
            continue

        if marker in JPG_STANDALONE:
            pos += 2
            continue

        if pos + 4 > len(data):
            out.append(Finding("CRITICAL", f"truncated length field for marker {marker:#04x} at offset {pos}"))
            return out

        length = int.from_bytes(data[pos + 2:pos + 4], "big")
        seg_end = pos + 2 + length

        if length < 2 or seg_end > len(data):
            out.append(Finding("CRITICAL", f"invalid segment length {length} for marker {marker:#04x} at offset {pos}"))
            return out

        if marker not in JPG_LENGTHED_WHITELIST:
            out.append(Finding("WARN", f"non-whitelist JPG marker {marker:#04x} at offset {pos} (length {length})"))

        if marker == 0xFE and length > JPG_COMMENT_SOFT_CAP:  # COM
            out.append(Finding("WARN", f"COM segment size {length} exceeds soft cap {JPG_COMMENT_SOFT_CAP}"))
        if 0xE0 <= marker <= 0xEF and length > 64 * 1024:  # APPn — usually small unless EXIF/XMP
            out.append(Finding("WARN", f"APP{marker - 0xE0} segment size {length} unusually large"))

        pos = seg_end

    if not saw_eoi:
        out.append(Finding("CRITICAL", "no EOI marker — file may be truncated"))
        return out

    trailing = len(data) - eoi_at
    if trailing > TRAILING_BYTES_INFO_THRESHOLD:
        out.append(Finding("CRITICAL", f"{trailing} bytes after EOI — probable polyglot or stuffed payload"))

    return out


# --- Findings + report -----------------------------------------------------

@dataclass
class Finding:
    severity: str  # INFO / WARN / CRITICAL
    message: str


def _scan_one(path: Path) -> tuple[list[Finding], str]:
    """Return (findings, format-tag) for a single file."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [Finding("CRITICAL", f"unable to read file: {exc}")], "ERR"

    head = data[:8]
    if head.startswith(PNG_SIGNATURE):
        return _scan_png(data), "PNG"
    if head.startswith(JPG_SOI):
        return _scan_jpg(data), "JPG"
    if path.suffix.lower() == ".svg":
        return [Finding("INFO", "SVG — delegate to scripts/svg-sanitize.py")], "SVG"
    return [Finding("INFO", "unknown format — not scanned")], "UNK"


def _walk_dir(root: Path, exts: Iterable[str]) -> Iterable[Path]:
    suffix_set = {f".{e.lower().lstrip('.')}" for e in exts}
    for child in sorted(root.rglob("*")):
        if child.is_file() and child.suffix.lower() in suffix_set:
            yield child


def _render_report(rows: list[tuple[Path, str, str, list[Finding]]]) -> str:
    lines = [
        "# Asset scan report",
        "",
        "Format: PNG chunk + JPG segment scan. Stdlib-only.",
        "",
        "| File | Format | SHA-256 (first 16) | Verdict | Details |",
        "|---|---|---|---|---|",
    ]
    for path, fmt, sha, findings in rows:
        if not findings or all(f.severity == "INFO" for f in findings):
            verdict = "clean"
        elif any(f.severity == "CRITICAL" for f in findings):
            verdict = "**CRITICAL**"
        else:
            verdict = "warn"
        details = "<br>".join(f"`{f.severity}` {f.message}" for f in findings) or "—"
        lines.append(f"| `{path}` | {fmt} | `{sha[:16]}` | {verdict} | {details} |")
    lines.append("")
    return "\n".join(lines)


def _exit_code(rows: list[tuple[Path, str, str, list[Finding]]], strict: bool, advisory: bool) -> int:
    if advisory:
        return 0
    worst = 0  # 0 clean, 2 warn, 3 critical
    for _, _, _, findings in rows:
        for f in findings:
            if f.severity == "CRITICAL":
                worst = max(worst, 3)
            elif f.severity == "WARN":
                worst = max(worst, 3 if strict else 2)
    return worst


# --- CLI -------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Defensive scanner for PNG / JPG assets.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", help="single file to scan")
    g.add_argument("--dir", help="directory to scan recursively")
    p.add_argument("--exts", default="png,jpg,jpeg,gif,svg", help="comma-separated extensions when --dir")
    p.add_argument("--report", help="write a Markdown report to this path")
    p.add_argument("--strict", action="store_true", help="escalate WARN to non-zero exit")
    p.add_argument("--advisory", action="store_true", help="advisory-only mode (always exits 0 unless IO error)")
    return p


def main() -> int:
    args = _build_parser().parse_args()

    targets: list[Path] = []
    if args.file:
        targets = [Path(args.file)]
    else:
        root = Path(args.dir)
        if not root.is_dir():
            print(f"error: {root} is not a directory", file=sys.stderr)
            return 1
        targets = list(_walk_dir(root, args.exts.split(",")))

    if not targets:
        print("(no files matched)", file=sys.stderr)
        return 0

    rows: list[tuple[Path, str, str, list[Finding]]] = []
    for path in targets:
        try:
            sha = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            rows.append((path, "ERR", "-", [Finding("CRITICAL", f"unable to hash file: {exc}")]))
            continue
        findings, fmt = _scan_one(path)
        rows.append((path, fmt, sha, findings))

    report = _render_report(rows)
    print(report)

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"\nwrote report → {args.report}", file=sys.stderr)

    return _exit_code(rows, strict=args.strict, advisory=args.advisory)


if __name__ == "__main__":
    sys.exit(main())
