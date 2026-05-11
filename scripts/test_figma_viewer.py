#!/usr/bin/env python3
"""Regression tests for scripts/figma-viewer.py.

Covers the offline `--fixture` path (no network):
  - well-formed Figma fixture renders to a self-contained HTML doc
  - every CANVAS becomes a <section class="figma-canvas">
  - solid-fill rectangles emit a background-coloured div with the correct
    rounded hex
  - text nodes preserve `characters` (escaped) and font-family / weight /
    size in inline style
  - missing fixture errors out (not a silent network attempt)
  - invalid JSON errors out
  - output collision blocks without --force; --force overwrites
  - missing FIGMA_TOKEN with no fixture errors out
  - empty document still emits a "no pages" placeholder
  - unsupported node type lands in figma-unknown placeholder, not silently
    dropped

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "figma-viewer.py"
FIXTURE = REPO_ROOT / "scripts" / "fixtures" / "figma_viewer_sample.json"


def _run(args: list[str], env_overrides: dict | None = None,
         expect_code: int = 0) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.pop("FIGMA_TOKEN", None)
    if env_overrides:
        env.update(env_overrides)
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, env=env,
    )
    if proc.returncode != expect_code:
        raise AssertionError(
            f"unexpected exit code {proc.returncode} (expected {expect_code})\n"
            f"  args: {args}\n  stdout: {proc.stdout}\n  stderr: {proc.stderr}"
        )
    return proc


class FigmaViewerCase(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.output = self.tmp / "viewer.html"

    # ── happy path ────────────────────────────────────────────────────

    def test_renders_html_with_doctype_and_title(self) -> None:
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("Default Studio · Sample Design", html,
                      "file name from fixture should appear as <title> and chrome label")

    def test_every_canvas_becomes_a_section(self) -> None:
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        # The fixture has 2 CANVAS pages: "Page · Cover" + "Page · Tokens".
        self.assertEqual(
            html.count('<section class="figma-canvas"'), 2,
            "fixture's 2 CANVAS pages should each produce a <section>"
        )
        self.assertIn("Page · Cover", html)
        self.assertIn("Page · Tokens", html)

    def test_solid_fill_rect_emits_correct_rgba(self) -> None:
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        # Accent / Primary swatch is 0.357 / 0.486 / 0.980 → 91 / 124 / 250
        self.assertIn("rgba(91,124,250,1.000)", html,
                      "accent.primary RGBA should appear on the swatch background")

    def test_corner_radius_applied(self) -> None:
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        # Swatch has cornerRadius 12; CTA has cornerRadius 8
        self.assertIn("border-radius:12px", html)
        self.assertIn("border-radius:8px", html)

    def test_text_node_preserves_characters_and_font(self) -> None:
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        self.assertIn("Design that ships.", html)
        # font-family is wrapped in CSS-single-quotes; the family name itself
        # is HTML-escaped (so a malicious " or > can't break out of the
        # inline style attribute), but plain ASCII like "Inter" comes
        # through unchanged inside the quotes.
        self.assertIn("font-family:'Inter'", html,
                      "font family should appear quoted in inline style")
        self.assertIn("font-weight:700", html)
        self.assertIn("font-size:72px", html)

    def test_text_family_with_quote_chars_is_escaped(self) -> None:
        """Defence-in-depth: if a malicious Figma payload puts a quote/
        bracket in fontFamily, it must be HTML-escaped before landing
        in the inline style attribute so it can't break the attribute."""
        evil = self.tmp / "evil.json"
        evil.write_text(json.dumps({
            "name": "Evil",
            "document": {
                "id": "0:0", "type": "DOCUMENT",
                "children": [{
                    "id": "1:0", "name": "Page", "type": "CANVAS",
                    "children": [{
                        "id": "2:1", "name": "Text", "type": "TEXT",
                        "absoluteBoundingBox": {"x": 0, "y": 0, "width": 100, "height": 30},
                        "style": {"fontFamily": "Inter\"><script>alert(1)</script>",
                                  "fontWeight": 400, "fontSize": 16},
                        "characters": "ok"
                    }]
                }]
            }
        }), encoding="utf-8")
        _run(["--fixture", str(evil), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        self.assertNotIn("<script>alert(1)</script>", html,
                         "literal <script> from fontFamily must not survive")
        self.assertIn("&lt;script&gt;", html,
                      "quote / angle-bracket chars in fontFamily must be HTML-escaped")

    def test_html_is_self_contained(self) -> None:
        """No external <link>, <script src>, or @import — keyboard JS and
        styles are inlined so the viewer works without network."""
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        self.assertNotIn("<link ", html, "no external stylesheet linkage")
        self.assertNotIn("<script src=", html, "no external script linkage")
        self.assertNotIn("@import", html, "no CSS @import")

    def test_canvas_dims_label_present(self) -> None:
        _run(["--fixture", str(FIXTURE), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        # Cover page contains a 1200×800 frame; canvas-dims label appears.
        self.assertIn("1200 × 800", html)

    # ── error paths ───────────────────────────────────────────────────

    def test_missing_fixture_errors_out(self) -> None:
        bogus = self.tmp / "no-such-fixture.json"
        proc = _run(
            ["--fixture", str(bogus), "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("not found", proc.stderr.lower())
        self.assertFalse(self.output.exists())

    def test_invalid_fixture_json_errors_out(self) -> None:
        bad = self.tmp / "bad.json"
        bad.write_text("{ not valid json }", encoding="utf-8")
        proc = _run(
            ["--fixture", str(bad), "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("not valid json", proc.stderr.lower())

    def test_missing_token_and_no_fixture_errors_out(self) -> None:
        proc = _run(
            ["some-file-key", "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("no figma token", proc.stderr.lower())
        self.assertFalse(self.output.exists())

    def test_output_collision_blocks_without_force(self) -> None:
        self.output.write_text("placeholder", encoding="utf-8")
        proc = _run(
            ["--fixture", str(FIXTURE), "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("already exists", proc.stderr.lower())
        self.assertEqual(self.output.read_text(encoding="utf-8"), "placeholder")

    def test_force_overwrites_existing_output(self) -> None:
        self.output.write_text("placeholder", encoding="utf-8")
        _run([
            "--fixture", str(FIXTURE), "--output", str(self.output), "--force",
        ])
        html = self.output.read_text(encoding="utf-8")
        self.assertTrue(html.startswith("<!DOCTYPE html>"))

    # ── edge cases ────────────────────────────────────────────────────

    def test_empty_document_renders_no_pages_placeholder(self) -> None:
        empty = self.tmp / "empty.json"
        empty.write_text(json.dumps({
            "name": "Empty file",
            "lastModified": "2026-05-11T00:00:00Z",
            "document": {"id": "0:0", "name": "Document", "type": "DOCUMENT", "children": []}
        }), encoding="utf-8")
        _run(["--fixture", str(empty), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        self.assertIn("No pages", html)
        self.assertIn("0 pages", html)

    def test_unsupported_node_type_renders_as_unknown_placeholder(self) -> None:
        weird = self.tmp / "weird.json"
        weird.write_text(json.dumps({
            "name": "Weird",
            "document": {
                "id": "0:0", "name": "Document", "type": "DOCUMENT",
                "children": [{
                    "id": "1:0", "name": "Page", "type": "CANVAS",
                    "children": [{
                        "id": "2:1", "name": "Boolean op", "type": "BOOLEAN_OPERATION",
                        "absoluteBoundingBox": {"x": 0, "y": 0, "width": 100, "height": 100}
                    }]
                }]
            }
        }), encoding="utf-8")
        _run(["--fixture", str(weird), "--output", str(self.output)])
        html = self.output.read_text(encoding="utf-8")
        self.assertIn("figma-unknown", html,
                      "unsupported node type must surface as a visible placeholder")
        self.assertIn('data-type="BOOLEAN_OPERATION"', html)


if __name__ == "__main__":
    unittest.main()
