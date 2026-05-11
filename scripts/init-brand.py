#!/usr/bin/env python3
"""
init-brand.py — bootstrap a per-fork team-brand-spec.json from the default.

Copies `assets/team-brand-spec.default.json` to `team-brand-spec.json` (or
a user-specified target path), strips the `_meta` / `_note` guidance keys
that the default carries inline as documentation, and re-validates the
result is parseable JSON. Prints a reminder list of the fields the team
needs to fill in.

The `.default.json` file ships *operational* values (evidence-anchored to
the 11-service style sweep in `references/web3-game-style-stats.md`), so
the stamped carrier is immediately usable as a fallback while the adopter
replaces placeholder fields (logo path, brand name, custom typography).

Usage:
    python3 scripts/init-brand.py
    python3 scripts/init-brand.py --target /path/to/your-project/team-brand-spec.json
    python3 scripts/init-brand.py --keep-meta            # leave _meta / _note in place
    python3 scripts/init-brand.py --force                # overwrite an existing target

Exit codes:
    0  written
    1  source missing, target collision (without --force), invalid JSON,
       or write failure

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT / "assets" / "team-brand-spec.default.json"
DEFAULT_TARGET = REPO_ROOT / "team-brand-spec.json"

# Most-common fields a fork operator will need to replace before the
# spec is project-specific. The list is intentionally a hint, not an
# exhaustive schema — references/brand-spec-fields.md is canonical.
PLACEHOLDER_FIELDS = [
    ("team.company", "Real company name (replaces 'Example Studios')"),
    ("team.division", "Studio / division name"),
    ("brand.name", "Brand name as it appears on output"),
    ("brand.tagline_short", "One-line product tagline (<= 8 words)"),
    ("brand.tone_keywords", "Voice descriptors, 3-5 entries"),
    ("logo.primary", "Path to primary logo SVG inside the repo"),
    ("colors.accent.primary", "Brand accent color (hex) — overrides the neutral default #5B7CFA"),
    ("typography.display.family", "Heading / hero typeface (default ships Inter)"),
    ("typography.body.family", "Body copy typeface (default ships Inter)"),
    ("approved_asset_hosts.internal", "Team-internal asset host allowlist (per-fork)"),
]


def strip_meta_keys(data):
    """Recursively strip keys starting with `_meta` or `_note` from a dict tree."""
    if isinstance(data, dict):
        return {
            k: strip_meta_keys(v)
            for k, v in data.items()
            if not (k.startswith("_meta") or k.startswith("_note"))
        }
    if isinstance(data, list):
        return [strip_meta_keys(item) for item in data]
    return data


def _format_path(p: Path) -> str:
    """Print paths relative to cwd when possible, absolute otherwise."""
    try:
        cwd = Path.cwd().resolve()
        return str(p.resolve().relative_to(cwd))
    except (ValueError, OSError):
        return str(p)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Bootstrap a per-fork team-brand-spec.json from the example template.",
    )
    ap.add_argument(
        "--source",
        "--example",
        dest="source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="path to the default-spec source (default: assets/team-brand-spec.default.json). "
        "The `--example` alias is preserved for callers from the pre-Step-5.1 layout.",
    )
    ap.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help="path to write the bootstrapped spec (default: team-brand-spec.json at repo root)",
    )
    ap.add_argument(
        "--keep-meta",
        action="store_true",
        help="leave _meta / _note guidance blocks in place (default: strip them)",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="overwrite the target if it already exists",
    )
    args = ap.parse_args(argv)

    if not args.source.exists():
        sys.stderr.write(f"ERROR: source file not found at {args.source}\n")
        return 1

    if args.target.exists() and not args.force:
        sys.stderr.write(f"ERROR: target already exists at {args.target}\n")
        sys.stderr.write("       Re-run with --force to overwrite, or pick a different --target.\n")
        return 1

    try:
        raw = args.source.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"ERROR: source file is not valid JSON: {e}\n")
        return 1

    if not args.keep_meta:
        data = strip_meta_keys(data)

    try:
        args.target.parent.mkdir(parents=True, exist_ok=True)
        args.target.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as e:
        sys.stderr.write(f"ERROR: write failed: {e}\n")
        return 1

    # Re-validate the written file is round-trip parseable.
    try:
        json.loads(args.target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"ERROR: the file we just wrote is not valid JSON: {e}\n")
        return 1

    print(f"✓ wrote {_format_path(args.target)}")
    print()
    print("Next: fill in the placeholder values. The most-common fields:")
    for path, desc in PLACEHOLDER_FIELDS:
        print(f"  - {path:30s} {desc}")
    print()
    print("Then re-validate:")
    print(f'  python3 -c "import json; json.load(open(\'{_format_path(args.target)}\'))"')
    print()
    print("See references/brand-spec-fields.md for the full field reference.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
