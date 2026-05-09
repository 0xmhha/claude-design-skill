#!/usr/bin/env bash
# scripts/install-hooks.sh — opt-in installer for repo-managed git hooks.
#
# Run once after cloning:
#     ./scripts/install-hooks.sh
#
# What it does:
#   * Sets `core.hooksPath = .githooks` on this repo only.
#   * Marks .githooks/pre-commit executable.
#
# Why opt-in:
#   Auto-installing hooks on clone is a long-standing footgun — it surprises
#   contributors and gives the repo write-side power over their working tree.
#   This script makes activation deliberate.
#
# Uninstall:
#     git config --unset core.hooksPath

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "${REPO_ROOT:-}" ]; then
  echo "✘ Not inside a git repository." >&2
  exit 1
fi

HOOKS_DIR="$REPO_ROOT/.githooks"
if [ ! -d "$HOOKS_DIR" ]; then
  echo "✘ $HOOKS_DIR not found. Are you in the right repo?" >&2
  exit 1
fi

git -C "$REPO_ROOT" config core.hooksPath .githooks
find "$HOOKS_DIR" -type f -exec chmod +x {} \;

echo "✓ Hooks installed."
echo "  core.hooksPath -> .githooks"
echo "  Active hooks:"
ls -1 "$HOOKS_DIR" | sed 's/^/    /'
echo ""
echo "  Pre-commit will now run svg-sanitize.py on staged .svg and"
echo "  scan_assets.py on staged .png / .jpg / .jpeg / .gif."
echo ""
echo "  Bypass (use sparingly): git commit --no-verify"
echo "  Uninstall:              git config --unset core.hooksPath"
