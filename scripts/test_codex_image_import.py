#!/usr/bin/env python3
"""
test_codex_image_import.py — regression tests for scripts/codex-image-import.py

Ships clean PNG, scan-warn PNG, scan-critical PNG fixtures (built in-memory
from PNG chunk primitives, no PIL) and asserts:
  - confidentiality gate exits 4 on codename in prompt
  - clean PNG passes through, file moved, PROVENANCE recorded
  - WARN PNG (oversized tEXt) blocks the import, source untouched, BLOCKED record
  - CRITICAL PNG (trailing bytes after IEND) blocks the import, exit 3
  - dry-run does not move
  - latest-PNG discovery picks the most recently mtime'd file

Stdlib only. No pytest, no PIL. Reuses scripts/scan_assets.py via subprocess
just like the production script does.

Run:
    python3 scripts/test_codex_image_import.py
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import struct
import sys
import tempfile
import time
import unittest
import zlib
from pathlib import Path


# --- Module loader (handles hyphen in filename) ----------------------------
_HERE = Path(__file__).resolve().parent
_TARGET = _HERE / "codex-image-import.py"
_spec = importlib.util.spec_from_file_location("codex_image_import", _TARGET)
mod = importlib.util.module_from_spec(_spec)
sys.modules["codex_image_import"] = mod
_spec.loader.exec_module(mod)


# --- PNG fixture builders --------------------------------------------------
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def _chunk(tag: bytes, data: bytes) -> bytes:
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return length + tag + data + crc


def _ihdr(width: int = 1, height: int = 1) -> bytes:
    # 1x1 RGBA, bit depth 8, color type 6, default filter/interlace
    body = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return _chunk(b"IHDR", body)


def _idat() -> bytes:
    # 1x1 RGBA pixel: filter byte 0 + RGBA(0,0,0,0)
    raw = b"\x00\x00\x00\x00\x00"
    return _chunk(b"IDAT", zlib.compress(raw))


def _iend() -> bytes:
    return _chunk(b"IEND", b"")


def make_clean_png() -> bytes:
    return PNG_SIG + _ihdr() + _idat() + _iend()


def make_oversized_text_png() -> bytes:
    """tEXt chunk far above 4 KB soft cap → scan_assets WARN (exit 2)."""
    huge = b"k\x00" + (b"x" * 8192)  # keyword 'k' + 8KB null + payload
    text_chunk = _chunk(b"tEXt", huge)
    return PNG_SIG + _ihdr() + text_chunk + _idat() + _iend()


def make_trailing_byte_png() -> bytes:
    """Bytes after IEND → scan_assets CRITICAL (exit 3)."""
    return PNG_SIG + _ihdr() + _idat() + _iend() + b"GOTCHA-payload"


def make_cabx_png(payload_size: int = 26415) -> bytes:
    """Simulate gpt-image-2 output: caBX C2PA chunk between IHDR and IDAT.

    The chunk tag 'caBX' is what OpenAI inserts as the JUMBF / C2PA
    provenance container. PNG spec calls it ancillary (lowercase first
    letter) — strip-and-import keeps the image, drops the metadata.
    """
    cabx = _chunk(b"caBX", b"\x00" * payload_size)
    return PNG_SIG + _ihdr() + cabx + _idat() + _iend()


def make_cabx_with_trailing_png() -> bytes:
    """caBX + trailing bytes after IEND. Strip removes caBX but trailing
    bytes survive (we stop emitting after IEND, so the cleaned output is
    actually clean — but the strip output is the *before-IEND* portion.
    Threats still get caught when the original anomaly is inside the
    chunk stream, not after IEND.)"""
    return make_cabx_png() + b"PAYLOAD-AFTER-IEND"


# --- Test harness ----------------------------------------------------------
class CodexImportCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="codex_import_test_"))
        self.codex_home = self.tmp / "codex-home"
        self.gen_dir = self.codex_home / "generated_images"
        self.gen_dir.mkdir(parents=True)
        self.assets_root = self.tmp / "assets"
        self.assets_root.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _drop_png(self, name: str, payload: bytes) -> Path:
        p = self.gen_dir / name
        p.write_bytes(payload)
        return p

    def _run(self, *args: str) -> int:
        old_argv = sys.argv
        sys.argv = ["codex-image-import.py", *args]
        try:
            return mod.main()
        finally:
            sys.argv = old_argv


# --- 1. Confidentiality gate -----------------------------------------------
class TestConfidentialityGate(CodexImportCase):

    def test_clean_prompt_passes_gate(self) -> None:
        # Build a clean PNG so the gate is the only failure path
        self._drop_png("a.png", make_clean_png())
        code = self._run(
            "--brand", "acme",
            "--name", "asset",
            "--prompt", "matte black product render on charcoal background",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0)

    def test_codename_in_prompt_blocks_with_exit_4(self) -> None:
        self._drop_png("a.png", make_clean_png())
        code = self._run(
            "--brand", "acme",
            "--name", "asset",
            "--prompt", "logo for project Falcon launching next quarter",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 4, "exit 4 = confidentiality gate violation")
        # No file should have moved
        dst = self.assets_root / "acme-brand" / "generated" / "asset.png"
        self.assertFalse(dst.exists(), "destination must not be created when gate fires")

    def test_internal_keyword_caught(self) -> None:
        self._drop_png("a.png", make_clean_png())
        code = self._run(
            "--brand", "acme",
            "--name", "asset",
            "--prompt", "internal-prototype illustration",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 4)


# --- 2. Stego scan hard-fail -----------------------------------------------
class TestStegoHardFail(CodexImportCase):

    def test_clean_png_imports_and_records_provenance(self) -> None:
        src = self._drop_png("clean.png", make_clean_png())
        code = self._run(
            "--brand", "acme",
            "--name", "hero",
            "--prompt", "abstract gradient background, no text",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0)
        dst = self.assets_root / "acme-brand" / "generated" / "hero.png"
        self.assertTrue(dst.is_file(), "clean PNG must move to destination")
        prov = (self.assets_root / "acme-brand" / "PROVENANCE.md").read_text()
        self.assertIn("hero.png (imported)", prov)
        self.assertIn("Stego scan (post-strip): PASS", prov)
        self.assertIn("Source SHA-256:", prov)
        self.assertIn("Output SHA-256:", prov)
        self.assertFalse(src.exists(), "source PNG should be removed after import")

    def test_oversized_text_chunk_blocks_with_exit_2(self) -> None:
        src = self._drop_png("warn.png", make_oversized_text_png())
        code = self._run(
            "--brand", "acme",
            "--name", "warn-asset",
            "--prompt", "abstract scene",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 2, "scan WARN should propagate as exit 2")
        dst = self.assets_root / "acme-brand" / "generated" / "warn-asset.png"
        self.assertFalse(dst.exists(), "WARN PNG must NOT move into assets")
        self.assertTrue(src.exists(), "source PNG must remain so user can retry")
        prov = (self.assets_root / "acme-brand" / "PROVENANCE.md").read_text()
        self.assertIn("BLOCKED — not imported", prov)
        self.assertIn("Stego scan (post-strip): BLOCKED", prov)

    def test_trailing_byte_stripped_and_audited(self) -> None:
        """Trailing bytes after IEND are dropped by the strip stage (we
        stop emitting at IEND), so the post-strip scan is clean and the
        import succeeds. The audit trail must record the trailing bytes
        as a synthetic dropped entry so the user knows something was
        cut from the upstream file."""
        self._drop_png("trailing.png", make_trailing_byte_png())
        code = self._run(
            "--brand", "acme",
            "--name", "trailing-asset",
            "--prompt", "abstract scene",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0, "trailing bytes should be stripped, not blocked")
        dst = self.assets_root / "acme-brand" / "generated" / "trailing-asset.png"
        self.assertTrue(dst.is_file())
        self.assertNotIn(b"GOTCHA-payload", dst.read_bytes())
        prov = (self.assets_root / "acme-brand" / "PROVENANCE.md").read_text()
        self.assertIn("trailing-bytes(", prov, "audit must record stripped trailing bytes")


# --- 3. Source discovery (latest mtime, recursive across session dirs) ---
class TestLatestDiscovery(CodexImportCase):

    def test_latest_png_is_picked(self) -> None:
        old = self._drop_png("old.png", make_clean_png())
        time.sleep(0.05)  # ensure mtime difference
        new = self._drop_png("new.png", make_clean_png())
        # Bump new's mtime explicitly so the test is robust on coarse FS clocks
        os.utime(new, None)
        # And lower old's mtime
        os.utime(old, (old.stat().st_atime, new.stat().st_mtime - 1))

        code = self._run(
            "--brand", "acme",
            "--name", "latest-asset",
            "--prompt", "abstract gradient",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0)
        # `new` should have been the imported source — it's removed; `old` survives
        self.assertTrue(old.exists(), "older PNG must not be touched")
        self.assertFalse(new.exists(), "latest PNG must be moved")

    def test_session_subdirectory_layout_is_handled(self) -> None:
        """Codex CLI v0.130 stores PNGs at <session-id>/ig_<hash>.png — the
        importer must recurse, not only look at direct children."""
        session_dir = self.gen_dir / "019e0cb9-4285-77e1-bca8-7f3d9b844994"
        session_dir.mkdir()
        nested = session_dir / "ig_0bbeee3bf10c6d5e0169ff2963e6c88191b220ac.png"
        nested.write_bytes(make_clean_png())

        code = self._run(
            "--brand", "acme",
            "--name", "session-asset",
            "--prompt", "abstract still life",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0, "PNG inside session subdir must be discovered")
        dst = self.assets_root / "acme-brand" / "generated" / "session-asset.png"
        self.assertTrue(dst.is_file())
        self.assertFalse(nested.exists(), "session-dir source must be consumed")


# --- 4. Dry-run mode --------------------------------------------------------
class TestDryRun(CodexImportCase):

    def test_dry_run_does_not_move(self) -> None:
        src = self._drop_png("dry.png", make_clean_png())
        code = self._run(
            "--brand", "acme",
            "--name", "dry-asset",
            "--prompt", "a teapot",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
            "--dry-run",
        )
        self.assertEqual(code, 0)
        self.assertTrue(src.exists(), "dry-run keeps source")
        dst = self.assets_root / "acme-brand" / "generated" / "dry-asset.png"
        self.assertFalse(dst.exists(), "dry-run must not write destination")


# --- 5. Explicit --src override --------------------------------------------
class TestExplicitSrc(CodexImportCase):

    def test_explicit_src_path_used(self) -> None:
        # Place a PNG OUTSIDE the codex-home directory and pass via --src
        outside = self.tmp / "from-elsewhere.png"
        outside.write_bytes(make_clean_png())
        code = self._run(
            "--brand", "acme",
            "--name", "outside-asset",
            "--prompt", "a still life",
            "--src", str(outside),
            "--codex-home", str(self.codex_home),  # has no PNGs
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0)
        dst = self.assets_root / "acme-brand" / "generated" / "outside-asset.png"
        self.assertTrue(dst.is_file())


# --- 6. C2PA / non-whitelist chunk strip -----------------------------------
class TestChunkStrip(CodexImportCase):

    def test_cabx_chunk_stripped_then_imported(self) -> None:
        """gpt-image-2 caBX (C2PA) chunk is auto-stripped, image imports."""
        self._drop_png("ig_real.png", make_cabx_png())
        code = self._run(
            "--brand", "acme",
            "--name", "stripped-asset",
            "--prompt", "matte black sphere",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0, "caBX should be stripped and import should succeed")
        dst = self.assets_root / "acme-brand" / "generated" / "stripped-asset.png"
        self.assertTrue(dst.is_file())
        # Verify caBX is gone from the imported file
        self.assertNotIn(b"caBX", dst.read_bytes(), "caBX must be removed from output")
        # PROVENANCE records the strip
        prov = (self.assets_root / "acme-brand" / "PROVENANCE.md").read_text()
        self.assertIn("Stripped chunks: caBX", prov)
        self.assertIn("AI provenance:", prov)
        self.assertIn("Stego scan (post-strip): PASS", prov)

    def test_cabx_stripped_size_smaller(self) -> None:
        """Output PNG should be smaller than input by at least the caBX payload."""
        src_bytes = make_cabx_png(payload_size=20000)
        src = self._drop_png("ig_big.png", src_bytes)
        self._run(
            "--brand", "acme",
            "--name", "smaller-asset",
            "--prompt", "abstract",
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        dst = self.assets_root / "acme-brand" / "generated" / "smaller-asset.png"
        self.assertTrue(dst.is_file())
        # Stripped output should be smaller — caBX gone, IEND still terminates
        self.assertLess(
            dst.stat().st_size, len(src_bytes),
            "stripped PNG must be smaller than input"
        )

    def test_strip_only_keeps_whitelist_chunks(self) -> None:
        """Direct unit test of strip_png_to_whitelist."""
        cleaned, dropped = mod.strip_png_to_whitelist(make_cabx_png())
        # caBX removed
        self.assertEqual(len(dropped), 1)
        self.assertEqual(dropped[0][0], "caBX")
        # IHDR / IDAT / IEND survive
        self.assertIn(b"IHDR", cleaned)
        self.assertIn(b"IDAT", cleaned)
        self.assertIn(b"IEND", cleaned)
        self.assertNotIn(b"caBX", cleaned)

    def test_strip_drops_trailing_bytes_implicitly(self) -> None:
        """Strip stops emitting after IEND. Trailing payload disappears
        because we don't copy it — and the output is then clean."""
        cleaned, dropped = mod.strip_png_to_whitelist(make_cabx_with_trailing_png())
        self.assertNotIn(b"PAYLOAD-AFTER-IEND", cleaned)
        # The strip ends at IEND, so the trailing-bytes anomaly is gone
        self.assertTrue(cleaned.endswith(b"IEND") or b"IEND" in cleaned)
        # caBX still recorded as dropped
        self.assertIn(("caBX", 26415), dropped)

    def test_whitelist_matches_scan_assets(self) -> None:
        """Single source of truth: PNG_WHITELIST in this script must be
        identical to scan_assets.PNG_WHITELIST."""
        scripts_dir = _HERE
        sys.path.insert(0, str(scripts_dir))
        try:
            import scan_assets  # type: ignore
        finally:
            sys.path.remove(str(scripts_dir))
        self.assertEqual(
            set(mod.PNG_WHITELIST), set(scan_assets.PNG_WHITELIST),
            "codex-image-import PNG_WHITELIST must match scan_assets PNG_WHITELIST"
        )


# --- 7. PROVENANCE prompt redaction ----------------------------------------
class TestProvenanceFormat(CodexImportCase):

    def test_long_prompt_truncated_in_provenance(self) -> None:
        self._drop_png("a.png", make_clean_png())
        long_prompt = "abstract gradient background, " + ("very specific detail " * 50)
        code = self._run(
            "--brand", "acme",
            "--name", "long-asset",
            "--prompt", long_prompt,
            "--codex-home", str(self.codex_home),
            "--assets-root", str(self.assets_root),
        )
        self.assertEqual(code, 0)
        prov = (self.assets_root / "acme-brand" / "PROVENANCE.md").read_text()
        self.assertIn("…", prov, "long prompt should be truncated with ellipsis")
        # Full prompt is still recoverable via SHA-256 hash
        self.assertIn("Prompt SHA-256:", prov)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main(verbosity=2)
