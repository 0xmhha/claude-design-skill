#!/usr/bin/env python3
"""Regression tests for scripts/figma-to-brand-spec.py.

Covers the offline extraction path through `--fixture` (no network):
  - solid-fill colors with `color/<group>/<name>` Figma names map to
    spec.colors.<group>.<name>
  - text-style nodes with `text/<role>/family` map to spec.typography.<role>
  - unmapped style names land in _meta.unmapped_styles, not silently
  - hex conversion is correct (rounded from Figma's 0-1 RGB to 0-255 HEX)
  - missing FIGMA_TOKEN with no fixture errors out, not silently fetches
  - invalid fixture JSON errors out
  - output collision blocks without --force
  - --force overwrites
  - merge mode pulls untouched values from the base spec
  - --no-merge omits the base spec
  - round-trip JSON validity

Stdlib only.
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
SCRIPT = REPO_ROOT / "scripts" / "figma-to-brand-spec.py"
FIXTURE = REPO_ROOT / "scripts" / "fixtures" / "figma_minimal.json"
BASE_SPEC = REPO_ROOT / "assets" / "team-brand-spec.default.json"


def _run(args: list[str], env_overrides: dict | None = None,
         expect_code: int = 0) -> subprocess.CompletedProcess:
    """Invoke the script with the given args; assert expected exit code."""
    env = os.environ.copy()
    # Always strip FIGMA_TOKEN unless explicitly set, so tests don't
    # accidentally pick up a real token from the shell.
    env.pop("FIGMA_TOKEN", None)
    if env_overrides:
        env.update(env_overrides)
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, env=env,
    )
    if proc.returncode != expect_code:
        msg = (
            f"unexpected exit code {proc.returncode} (expected {expect_code})\n"
            f"  args: {args}\n  stdout: {proc.stdout}\n  stderr: {proc.stderr}"
        )
        raise AssertionError(msg)
    return proc


class FigmaToBrandSpecCase(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.output = self.tmp / "team-brand-spec.json"

    # ── happy path · color extraction ─────────────────────────────────

    def test_color_styles_map_to_nested_spec_slots(self) -> None:
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(data["colors"]["accent"]["primary"], "#5B7CFA",
                         "RGB 0.357 / 0.486 / 0.980 should round to #5B7CFA")
        self.assertEqual(data["colors"]["surface"]["base_light"], "#FFFFFF")
        self.assertEqual(data["colors"]["surface"]["base_dark"], "#0F1115")
        self.assertEqual(data["colors"]["status"]["success_light"], "#0C8911",
                         "fixture's status_success_light should match Uniswap Spore green")

    # ── happy path · text extraction ──────────────────────────────────

    def test_text_styles_map_to_typography(self) -> None:
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        display = data["typography"]["display"]["family"]
        self.assertIsInstance(display, dict, "text/<role>/family should land as a dict, not a string")
        self.assertEqual(display["family"], "Inter")
        self.assertEqual(display["weight"], 700)
        self.assertEqual(display["size"], 48)
        self.assertEqual(display["line_height_px"], 56)

        body = data["typography"]["body"]["family"]
        self.assertEqual(body["family"], "Inter")
        self.assertEqual(body["weight"], 400)
        self.assertEqual(body["size"], 16)

    # ── unmapped-style preservation ───────────────────────────────────

    def test_unmapped_styles_are_recorded_not_dropped(self) -> None:
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        unmapped = data["_meta"]["unmapped_styles"]
        self.assertEqual(len(unmapped), 1, "fixture has exactly one loose-random style")
        self.assertEqual(unmapped[0]["figma_name"], "primitives/Loose Random")
        self.assertEqual(unmapped[0]["kind"], "color")
        self.assertEqual(unmapped[0]["value"], "#808080")

    def test_unstyled_nodes_do_not_pollute_output(self) -> None:
        """Nodes without a styles{} reference should never reach the spec."""
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        # The fixture has an unstyled black rectangle (2:8). It must not
        # appear anywhere in the output.
        flat = json.dumps(data)
        self.assertNotIn("#000000", flat,
                         "unstyled black rect should not leak as a color token")

    # ── metadata ──────────────────────────────────────────────────────

    def test_meta_records_source_file(self) -> None:
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        meta = data["_meta"]
        self.assertEqual(meta["extracted_from"], "Test Design System")
        self.assertEqual(meta["extracted_at"], "2026-05-11T00:00:00Z")
        self.assertEqual(meta["tool"], "scripts/figma-to-brand-spec.py")

    # ── merge mode ────────────────────────────────────────────────────

    def test_merge_mode_preserves_untouched_groups(self) -> None:
        """Without --no-merge, extracted slots overlay the default spec;
        groups the Figma file doesn't define (iconography, motion) keep
        the evidence-anchored defaults."""
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            # no --no-merge; default merge into team-brand-spec.default.json
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        # Extracted slots should be present
        self.assertEqual(data["colors"]["accent"]["primary"], "#5B7CFA")
        # Untouched groups should still ship from the base
        self.assertEqual(data["iconography"]["family"], "Lucide")
        self.assertEqual(data["motion"]["duration_ms"]["medium"], 300)

    def test_no_merge_omits_base_groups(self) -> None:
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        # Without merge, iconography / motion from the default shouldn't
        # appear in the output.
        self.assertNotIn("iconography", data)
        self.assertNotIn("motion", data)

    # ── error paths ───────────────────────────────────────────────────

    def test_missing_token_and_no_fixture_errors_out(self) -> None:
        """The script must refuse to call Figma when no token is set,
        not silently fall through to a public-API attempt."""
        proc = _run(
            ["some-file-key", "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("no figma token", proc.stderr.lower())
        self.assertFalse(self.output.exists(),
                         "output must not be created when token is missing")

    def test_missing_fixture_path_errors_out(self) -> None:
        bogus = self.tmp / "no-such-fixture.json"
        proc = _run(
            ["--fixture", str(bogus), "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("not found", proc.stderr.lower())

    def test_invalid_fixture_json_errors_out(self) -> None:
        bad = self.tmp / "bad.json"
        bad.write_text("{ this is not: valid json }", encoding="utf-8")
        proc = _run(
            ["--fixture", str(bad), "--output", str(self.output)],
            expect_code=1,
        )
        self.assertIn("not valid json", proc.stderr.lower())

    def test_output_collision_blocks_without_force(self) -> None:
        self.output.write_text("{}\n", encoding="utf-8")
        proc = _run(
            [
                "--fixture", str(FIXTURE),
                "--output", str(self.output),
                "--no-merge",
            ],
            expect_code=1,
        )
        self.assertIn("already exists", proc.stderr.lower())
        # Existing content untouched
        self.assertEqual(self.output.read_text(encoding="utf-8"), "{}\n")

    def test_force_overwrites_existing_output(self) -> None:
        self.output.write_text("{}\n", encoding="utf-8")
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
            "--force",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertIn("colors", data)

    # ── round-trip integrity ──────────────────────────────────────────

    def test_written_file_is_valid_json(self) -> None:
        _run([
            "--fixture", str(FIXTURE),
            "--output", str(self.output),
            "--no-merge",
        ])
        data = json.loads(self.output.read_text(encoding="utf-8"))
        # Re-serialise + re-parse should be lossless.
        rewritten = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        again = json.loads(rewritten)
        self.assertEqual(data, again)


if __name__ == "__main__":
    unittest.main()
