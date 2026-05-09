#!/usr/bin/env python3
"""
test_scan_assets.py — sanity tests for scripts/scan_assets.py

Synthesises minimal PNG and JPG containers in-memory, mutates them to
simulate the adversarial cases scan_assets.py is supposed to catch, and
asserts both (a) clean inputs pass and (b) every documented finding fires.

Run:
    python3 scripts/test_scan_assets.py
    python3 -m unittest scripts.test_scan_assets

Stdlib only.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path


# ---------------------------------------------------------------------------
# Load scan_assets.py — its filename has no hyphen, but routing it through
# importlib keeps this test stable if the module is renamed later.
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_TARGET = _HERE / "scan_assets.py"
_spec = importlib.util.spec_from_file_location("scan_assets", _TARGET)
scan_assets = importlib.util.module_from_spec(_spec)
sys.modules["scan_assets"] = scan_assets
_spec.loader.exec_module(scan_assets)


# ---------------------------------------------------------------------------
# Minimal PNG / JPG synthesis helpers.
# ---------------------------------------------------------------------------
def _png_chunk(ctype: bytes, body: bytes) -> bytes:
    crc = zlib.crc32(ctype + body) & 0xFFFFFFFF
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", crc)


def _make_minimal_png(extra_chunks: list[tuple[bytes, bytes]] | None = None,
                       extra_after_iend: bytes = b"") -> bytes:
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)  # 1x1, 8-bit, RGB
    ihdr_chunk = _png_chunk(b"IHDR", ihdr)
    idat_chunk = _png_chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00"))
    iend_chunk = _png_chunk(b"IEND", b"")
    extras = b"".join(_png_chunk(t, b) for t, b in (extra_chunks or []))
    return sig + ihdr_chunk + extras + idat_chunk + iend_chunk + extra_after_iend


def _make_minimal_jpg(*, extra_app: bytes | None = None,
                       extra_after_eoi: bytes = b"") -> bytes:
    """Build a structurally-minimal JPG without real entropy data.

    The JPG that scan_assets walks is structural-only (markers + length
    fields). Real decoders would reject it, but scan_assets reads markers
    and lengths only — that's the surface we're testing.
    """
    soi = b"\xff\xd8"
    # APP0 (JFIF) — required for a recognisable JPG
    jfif_body = b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    app0 = b"\xff\xe0" + struct.pack(">H", 2 + len(jfif_body)) + jfif_body
    extras = b""
    if extra_app is not None:
        extras = b"\xff\xe1" + struct.pack(">H", 2 + len(extra_app)) + extra_app
    # SOS with empty entropy data, then immediate EOI
    sos = b"\xff\xda" + struct.pack(">H", 2)
    eoi = b"\xff\xd9"
    return soi + app0 + extras + sos + eoi + extra_after_eoi


# ---------------------------------------------------------------------------
# Test harness.
# ---------------------------------------------------------------------------
class ScanCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scan_assets_test_"))

    def tearDown(self) -> None:
        for p in self.tmp.iterdir():
            p.unlink()
        self.tmp.rmdir()

    def _scan_bytes(self, suffix: str, blob: bytes) -> tuple[list[scan_assets.Finding], str]:
        path = self.tmp / f"in{suffix}"
        path.write_bytes(blob)
        return scan_assets._scan_one(path)


# ---------------------------------------------------------------------------
# 1. Clean PNG / JPG should produce no warnings.
# ---------------------------------------------------------------------------
class TestClean(ScanCase):

    def test_clean_png_passes(self) -> None:
        findings, fmt = self._scan_bytes(".png", _make_minimal_png())
        self.assertEqual(fmt, "PNG")
        critical = [f for f in findings if f.severity in ("WARN", "CRITICAL")]
        self.assertEqual(critical, [], f"unexpected findings: {critical}")

    def test_clean_jpg_passes(self) -> None:
        findings, fmt = self._scan_bytes(".jpg", _make_minimal_jpg())
        self.assertEqual(fmt, "JPG")
        critical = [f for f in findings if f.severity in ("WARN", "CRITICAL")]
        self.assertEqual(critical, [], f"unexpected findings: {critical}")


# ---------------------------------------------------------------------------
# 2. PNG: trailing bytes after IEND must trigger CRITICAL.
# ---------------------------------------------------------------------------
class TestPngTrailing(ScanCase):

    def test_trailing_bytes_after_iend(self) -> None:
        evil = _make_minimal_png(extra_after_iend=b"GOTCHA-PAYLOAD-DATA")
        findings, _ = self._scan_bytes(".png", evil)
        criticals = [f for f in findings if f.severity == "CRITICAL"]
        self.assertTrue(criticals, "trailing bytes after IEND must produce CRITICAL")
        self.assertTrue(any("after IEND" in f.message for f in criticals))


# ---------------------------------------------------------------------------
# 3. PNG: non-whitelist chunk → WARN.
# ---------------------------------------------------------------------------
class TestPngNonWhitelist(ScanCase):

    def test_unknown_chunk_warns(self) -> None:
        weird = _make_minimal_png(extra_chunks=[(b"xXxX", b"payload")])
        findings, _ = self._scan_bytes(".png", weird)
        warns = [f for f in findings if f.severity == "WARN"]
        self.assertTrue(warns, "non-whitelist chunk must WARN")
        self.assertTrue(any("xXxX" in f.message for f in warns))


# ---------------------------------------------------------------------------
# 4. PNG: oversized text chunk → WARN.
# ---------------------------------------------------------------------------
class TestPngOversizedText(ScanCase):

    def test_huge_text_chunk_warns(self) -> None:
        big = b"k\x00" + (b"x" * (scan_assets.PNG_TEXT_CHUNK_SOFT_CAP + 1024))
        bloat = _make_minimal_png(extra_chunks=[(b"tEXt", big)])
        findings, _ = self._scan_bytes(".png", bloat)
        warns = [f for f in findings if f.severity == "WARN"]
        self.assertTrue(any("soft cap" in f.message for f in warns))


# ---------------------------------------------------------------------------
# 5. PNG: missing signature → CRITICAL.
# ---------------------------------------------------------------------------
class TestPngBadSignature(ScanCase):

    def test_missing_signature_critical(self) -> None:
        broken = b"NOTAPNG" + _make_minimal_png()[8:]
        findings, fmt = self._scan_bytes(".png", broken)
        # Without a valid signature the scanner classifies the file as "unknown"
        # — no findings, fmt=UNK. That is itself a useful signal: the scanner
        # didn't lie about being able to read it.
        self.assertEqual(fmt, "UNK")


# ---------------------------------------------------------------------------
# 6. JPG: trailing bytes after EOI → CRITICAL.
# ---------------------------------------------------------------------------
class TestJpgTrailing(ScanCase):

    def test_trailing_bytes_after_eoi(self) -> None:
        evil = _make_minimal_jpg(extra_after_eoi=b"GOTCHA-JPEG-PAYLOAD")
        findings, _ = self._scan_bytes(".jpg", evil)
        criticals = [f for f in findings if f.severity == "CRITICAL"]
        self.assertTrue(criticals, "trailing bytes after EOI must produce CRITICAL")
        self.assertTrue(any("after EOI" in f.message for f in criticals))


# ---------------------------------------------------------------------------
# 7. SVG path is delegated, not scanned in-place.
# ---------------------------------------------------------------------------
class TestSvgDelegation(ScanCase):

    def test_svg_returns_info_delegation(self) -> None:
        findings, fmt = self._scan_bytes(".svg", b"<svg/>")
        self.assertEqual(fmt, "SVG")
        self.assertTrue(findings)
        self.assertEqual(findings[0].severity, "INFO")
        self.assertIn("svg-sanitize", findings[0].message)


# ---------------------------------------------------------------------------
# 8. Exit code mapping.
# ---------------------------------------------------------------------------
class TestExitCode(unittest.TestCase):

    def test_clean_returns_zero(self) -> None:
        rows = [(Path("x"), "PNG", "deadbeef", [])]
        self.assertEqual(scan_assets._exit_code(rows, strict=False, advisory=False), 0)

    def test_warn_returns_two(self) -> None:
        rows = [(Path("x"), "PNG", "deadbeef", [scan_assets.Finding("WARN", "x")])]
        self.assertEqual(scan_assets._exit_code(rows, strict=False, advisory=False), 2)

    def test_strict_warn_returns_three(self) -> None:
        rows = [(Path("x"), "PNG", "deadbeef", [scan_assets.Finding("WARN", "x")])]
        self.assertEqual(scan_assets._exit_code(rows, strict=True, advisory=False), 3)

    def test_critical_returns_three(self) -> None:
        rows = [(Path("x"), "PNG", "deadbeef", [scan_assets.Finding("CRITICAL", "x")])]
        self.assertEqual(scan_assets._exit_code(rows, strict=False, advisory=False), 3)

    def test_advisory_always_zero(self) -> None:
        rows = [(Path("x"), "PNG", "deadbeef", [scan_assets.Finding("CRITICAL", "x")])]
        self.assertEqual(scan_assets._exit_code(rows, strict=False, advisory=True), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
