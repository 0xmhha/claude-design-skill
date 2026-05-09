#!/usr/bin/env python3
"""
test_svg_sanitize.py — regression tests for scripts/svg-sanitize.py

Sanitizers are security modules; without tests, future edits silently
weaken the policy. This file exercises every removal rule + every
preservation rule so a single failed test means a real policy regression.

Run:
    python3 scripts/test_svg_sanitize.py            # one-shot
    python3 -m unittest scripts.test_svg_sanitize   # also fine

Exit 0 = all tests pass.
Exit non-zero = a regression in svg-sanitize.py.

Stdlib only — no pytest, no lxml, no fixtures directory.
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Sanitizer-visibility meta comment we prepend on any strip — strip it before
# inspecting the SVG element body so test assertions stay focused on the actual
# threat surface, not on the audit metadata.
_META_COMMENT_RE = re.compile(r"<!--\s*svg-sanitize:.*?-->\s*", flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Load svg-sanitize.py as a module despite the hyphen in the filename.
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_TARGET = _HERE / "svg-sanitize.py"
_spec = importlib.util.spec_from_file_location("svg_sanitize", _TARGET)
svg_sanitize = importlib.util.module_from_spec(_spec)
sys.modules["svg_sanitize"] = svg_sanitize
_spec.loader.exec_module(svg_sanitize)


# ---------------------------------------------------------------------------
# Test harness — every test writes an SVG, runs main() via argv, and
# inspects (a) the exit code, (b) the output content, (c) optional report.
# ---------------------------------------------------------------------------
class SanitizerCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="svg_sanitize_test_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, body: str, *, strict: bool = False, with_report: bool = False) -> tuple[int, str, str | None]:
        src = self.tmp / "in.svg"
        dst = self.tmp / "out.svg"
        report = self.tmp / "PROVENANCE.md" if with_report else None
        src.write_text(body, encoding="utf-8")

        argv = ["svg-sanitize.py", "--in", str(src), "--out", str(dst)]
        if with_report:
            argv += ["--report", str(report)]
        if strict:
            argv.append("--strict")

        old_argv = sys.argv
        sys.argv = argv
        try:
            code = svg_sanitize.main()
        finally:
            sys.argv = old_argv

        out_full = dst.read_text(encoding="utf-8") if dst.exists() else ""
        # Body-only view: the meta comment intentionally records what was stripped
        # (so the audit is visible in the file alone), but element-level assertions
        # should ignore it. _full is exposed as an instance attr for tests that
        # need to verify the meta comment itself.
        self._last_full = out_full
        out_body = _META_COMMENT_RE.sub("", out_full, count=1) if out_full else ""
        rep = report.read_text(encoding="utf-8") if (report and report.exists()) else None
        return code, out_body, rep


# ---------------------------------------------------------------------------
# 1. Clean SVG should pass through unchanged (no false positives).
# ---------------------------------------------------------------------------
class TestCleanPassthrough(SanitizerCase):

    def test_basic_logo_is_clean(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="80" viewBox="0 0 200 80">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#3B82F6"/>
      <stop offset="1" stop-color="#10B981"/>
    </linearGradient>
  </defs>
  <rect width="200" height="80" fill="url(#g)"/>
  <text x="100" y="48" text-anchor="middle" font-family="Inter" font-size="20" fill="white">CLEAN</text>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 0, "clean SVG must exit 0")
        self.assertIn("<linearGradient", out)
        self.assertIn("<rect", out)
        self.assertIn("<text", out)

    def test_intra_doc_use_href_is_preserved(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="50" height="50">
  <defs><circle id="dot" cx="25" cy="25" r="10"/></defs>
  <use xlink:href="#dot"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 0)
        self.assertIn("xlink:href=\"#dot\"", out)

    def test_strict_mode_passes_clean_input(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <rect width="10" height="10" fill="black"/>
</svg>'''
        code, _, _ = self._run(body, strict=True)
        self.assertEqual(code, 0, "--strict on clean SVG still exits 0")


# ---------------------------------------------------------------------------
# 2. Dangerous tags must be dropped + flagged as policy violation (exit 3).
# ---------------------------------------------------------------------------
class TestDangerousTags(SanitizerCase):

    def test_script_tag_dropped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <script>alert("boom")</script>
  <rect width="10" height="10" fill="black"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 3, "<script> must trigger exit 3")
        self.assertNotIn("<script", out)
        self.assertNotIn("alert", out)
        self.assertIn("<rect", out)  # legitimate content preserved

    def test_foreign_object_dropped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <foreignObject><p>x</p></foreignObject>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 3)
        self.assertNotIn("foreignObject", out)

    def test_image_tag_dropped_with_javascript_href(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <image href="javascript:alert(1)" width="10" height="10"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 3)
        self.assertNotIn("<image", out)


# ---------------------------------------------------------------------------
# 3. Event handlers and dangerous attribute values must be stripped.
# ---------------------------------------------------------------------------
class TestAttributeStripping(SanitizerCase):

    def test_onload_handler_stripped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" onload="alert(1)">
  <rect width="10" height="10"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 3, "event handlers should trip the policy flag")
        self.assertNotIn("onload", out)
        self.assertNotIn("alert", out)

    def test_onclick_on_inner_element_stripped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <rect width="10" height="10" onclick="track()"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 3)
        self.assertNotIn("onclick", out)

    def test_external_href_on_use_stripped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="10" height="10">
  <use xlink:href="https://attacker.example/evil.svg#x"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 3, "external href on <use> must trip policy")
        self.assertNotIn("attacker.example", out)


# ---------------------------------------------------------------------------
# 4. Tags outside the whitelist should be stripped without raising the
#    policy flag (these are merely "not-allowed", not "dangerous").
# ---------------------------------------------------------------------------
class TestNonWhitelistTagsDropped(SanitizerCase):

    def test_anchor_tag_dropped_without_policy_flag(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <a href="https://example.com"><circle cx="5" cy="5" r="3"/></a>
</svg>'''
        code, out, _ = self._run(body)
        # <a> is non-whitelist but not in the dangerous set; tracker URL doesn't
        # appear because the entire <a> subtree is dropped → exit 0.
        self.assertEqual(code, 0)
        self.assertNotIn("<a ", out)
        self.assertNotIn("example.com", out)


# ---------------------------------------------------------------------------
# 5. CSS sub-sanitize — tokens like url(), @import, expression() are stripped
#    when they appear inside style="" or <style> bodies.
# ---------------------------------------------------------------------------
class TestCssSubSanitize(SanitizerCase):

    def test_style_element_with_import_stripped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <style>@import url("https://attacker.example/x.css");</style>
  <rect width="10" height="10"/>
</svg>'''
        code, out, _ = self._run(body)
        # Stripped content but no dangerous-tag flag → exit 0 (clean strip)
        self.assertEqual(code, 0)
        self.assertNotIn("attacker.example", out)
        self.assertNotIn("@import", out)

    def test_inline_style_with_url_stripped(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <rect width="10" height="10" style="background: url('https://attacker.example/track.png')"/>
</svg>'''
        code, out, _ = self._run(body)
        self.assertEqual(code, 0)
        self.assertNotIn("attacker.example", out)


# ---------------------------------------------------------------------------
# 6. XXE / DOCTYPE / ENTITY are rejected at the parser layer (exit 2).
# ---------------------------------------------------------------------------
class TestXxeGuard(SanitizerCase):

    def test_doctype_rejected(self) -> None:
        body = '''<?xml version="1.0"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <text>&xxe;</text>
</svg>'''
        code, _, _ = self._run(body)
        self.assertEqual(code, 2, "DOCTYPE should be rejected at the parser (exit 2)")

    def test_entity_block_rejected(self) -> None:
        body = '<!ENTITY foo "bar"><svg xmlns="http://www.w3.org/2000/svg"/>'
        code, _, _ = self._run(body)
        self.assertEqual(code, 2)


# ---------------------------------------------------------------------------
# 7. Strict mode escalates clean-strip outcomes to non-zero.
# ---------------------------------------------------------------------------
class TestStrictMode(SanitizerCase):

    def test_strict_fails_on_any_strip(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <a href="https://example.com"><rect width="10" height="10"/></a>
</svg>'''
        code, _, _ = self._run(body, strict=True)
        self.assertNotEqual(code, 0, "--strict should turn clean-strip into non-zero")


# ---------------------------------------------------------------------------
# 8. Provenance report records hashes and findings.
# ---------------------------------------------------------------------------
class TestProvenanceReport(SanitizerCase):

    def test_report_records_hashes_and_findings(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <script>boom</script>
  <rect width="10" height="10"/>
</svg>'''
        code, _, report = self._run(body, with_report=True)
        self.assertEqual(code, 3)
        self.assertIsNotNone(report)
        self.assertIn("Input  SHA-256:", report)
        self.assertIn("Output SHA-256:", report)
        self.assertIn("YES (review required)", report)
        self.assertIn("Dropped <script>", report)


# ---------------------------------------------------------------------------
# 9. Visibility meta comment is prepended whenever something was stripped so
#    the audit trail is discoverable from the SVG file alone — not only via
#    the optional PROVENANCE.md report.
# ---------------------------------------------------------------------------
class TestVisibilityMetaComment(SanitizerCase):

    def test_meta_comment_prepended_on_strip(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <script>boom</script>
  <rect width="10" height="10"/>
</svg>'''
        self._run(body)
        self.assertIn("<!-- svg-sanitize:", self._last_full)
        self.assertIn("POLICY-VIOLATION", self._last_full)
        self.assertIn("<rect", self._last_full)

    def test_clean_input_has_no_meta_comment(self) -> None:
        body = '''<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
  <rect width="10" height="10" fill="black"/>
</svg>'''
        self._run(body)
        self.assertNotIn("<!-- svg-sanitize:", self._last_full)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main(verbosity=2)
