#!/usr/bin/env python3
"""Regression tests for scripts/init-brand.py.

Covers the cp + meta-strip + JSON-validate contract:
  - default run writes target and strips _meta / _note keys
  - --keep-meta flag preserves them
  - target collision blocks without --force, even when the existing
    target is empty / invalid
  - --force overwrites
  - missing source file errors out
  - invalid JSON in source errors out
  - written file is round-trip valid JSON

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "init-brand.py"
EXAMPLE = REPO_ROOT / "assets" / "team-brand-spec.example.json"


class InitBrandCase(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.target = self.tmp / "team-brand-spec.json"

    def _run(self, *extra_args: str, expect_code: int = 0) -> subprocess.CompletedProcess:
        cmd = [sys.executable, str(SCRIPT), "--target", str(self.target), *extra_args]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(
            proc.returncode,
            expect_code,
            f"unexpected exit code {proc.returncode}\n  stdout: {proc.stdout}\n  stderr: {proc.stderr}",
        )
        return proc

    # 1 — happy path

    def test_default_run_writes_target(self) -> None:
        self._run()
        self.assertTrue(self.target.exists(), "target file should exist after run")
        json.loads(self.target.read_text(encoding="utf-8"))  # round-trip parse

    def test_meta_keys_are_stripped_by_default(self) -> None:
        self._run()
        data = json.loads(self.target.read_text(encoding="utf-8"))
        for key in data.keys():
            self.assertFalse(
                key.startswith("_meta") or key.startswith("_note"),
                f"top-level _meta/_note key not stripped: {key}",
            )
        # The watermark block in the example carries an inline _note.
        self.assertIn("watermark", data)
        for key in data["watermark"].keys():
            self.assertFalse(
                key.startswith("_note"),
                f"nested _note key not stripped under watermark: {key}",
            )

    def test_actual_fields_preserved(self) -> None:
        self._run()
        data = json.loads(self.target.read_text(encoding="utf-8"))
        for required_top in ("team", "brand", "watermark", "logo", "colors", "typography"):
            self.assertIn(required_top, data, f"top-level field missing: {required_top}")

    # 2 — flag behavior

    def test_keep_meta_preserves_meta_block(self) -> None:
        self._run("--keep-meta")
        data = json.loads(self.target.read_text(encoding="utf-8"))
        meta_keys = [k for k in data.keys() if k.startswith("_meta") or k.startswith("_note")]
        self.assertTrue(
            meta_keys,
            "with --keep-meta at least one _meta/_note top-level key should remain",
        )
        # The watermark block should also still carry its _note guidance.
        self.assertIn("_note", data.get("watermark", {}),
                      "with --keep-meta the watermark._note guidance should remain")

    def test_target_collision_blocks_without_force(self) -> None:
        self.target.write_text("{}\n", encoding="utf-8")
        proc = self._run(expect_code=1)
        self.assertIn("already exists", proc.stderr.lower())
        # Existing content untouched.
        self.assertEqual(self.target.read_text(encoding="utf-8"), "{}\n")

    def test_force_overwrites_existing_target(self) -> None:
        self.target.write_text("{}\n", encoding="utf-8")
        self._run("--force")
        data = json.loads(self.target.read_text(encoding="utf-8"))
        self.assertIn("team", data)

    # 3 — error paths

    def test_missing_example_errors_out(self) -> None:
        bogus = self.tmp / "no-such-source.json"
        cmd = [
            sys.executable, str(SCRIPT),
            "--example", str(bogus),
            "--target", str(self.target),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not found", proc.stderr.lower())
        self.assertFalse(self.target.exists(), "target must not be created when source is missing")

    def test_invalid_json_example_errors_out(self) -> None:
        bad = self.tmp / "bad-source.json"
        bad.write_text("{ this is not: valid json }", encoding="utf-8")
        cmd = [
            sys.executable, str(SCRIPT),
            "--example", str(bad),
            "--target", str(self.target),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not valid json", proc.stderr.lower())
        self.assertFalse(self.target.exists(), "target must not be created when source is invalid")

    # 4 — round-trip integrity

    def test_written_file_round_trips(self) -> None:
        self._run()
        # Re-parse, re-write, re-parse — should be byte-identical (modulo
        # ordering, which json preserves in Python 3.7+).
        first = json.loads(self.target.read_text(encoding="utf-8"))
        rewritten = json.dumps(first, indent=2, ensure_ascii=False) + "\n"
        again = json.loads(rewritten)
        self.assertEqual(first, again)


if __name__ == "__main__":
    unittest.main()
