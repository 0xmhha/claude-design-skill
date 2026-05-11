#!/usr/bin/env python3
"""
figma-viewer.py — render a Figma file to a single self-contained HTML viewer.

Reads a Figma file via the public REST API (or a fixture for offline runs),
walks the document tree, and emits a *single* HTML page that lays each
CANVAS (page) out side-by-side with its FRAME / RECTANGLE / ELLIPSE / TEXT
children positioned absolutely using each node's `absoluteBoundingBox`.

The viewer is intentionally minimal — frames, rect / ellipse shapes with
solid fills + corner radii, and text nodes with `fontFamily` / `fontWeight`
/ `fontSize`. Vectors (`d` paths), images, components / instances, masks,
auto-layout constraints, and effects are *not* re-rendered; their bounding
boxes still show so the layout is legible at a glance.

Why minimal: the goal is "review what landed in Figma without opening
Figma" (offline visual smoke), not a full Figma replacement.

Usage:
    # Online (requires FIGMA_TOKEN env var):
    FIGMA_TOKEN='<YOUR_FIGMA_PERSONAL_ACCESS_TOKEN>' \
        python3 scripts/figma-viewer.py <FILE_KEY> --output viewer.html

    # Offline (fixture):
    python3 scripts/figma-viewer.py --fixture path/to/fixture.json --output viewer.html

Open the output HTML in any browser — keyboard shortcuts:
    ← / →  previous / next page
    1..9   jump to page N
    d      toggle dark page chrome

Exit codes:
    0  written
    1  missing token, missing fixture, Figma API error, invalid JSON,
       write failure, or output collision without --force

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = Path("figma-viewer.html")

FIGMA_API = "https://api.figma.com/v1"


# ──────────────────────────────────────────────────────────────────────
# Figma API
# ──────────────────────────────────────────────────────────────────────

def fetch_figma_file(file_key: str, token: str) -> dict:
    """Fetch a Figma file's tree in one call. Raises on non-2xx."""
    url = f"{FIGMA_API}/files/{file_key}"
    req = urllib.request.Request(url, headers={"X-Figma-Token": token})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ──────────────────────────────────────────────────────────────────────
# Color helpers
# ──────────────────────────────────────────────────────────────────────

def _rgba_to_css(color: dict, opacity: float = 1.0) -> str:
    """Figma 0-1 RGB(A) → CSS rgba() string with opacity baked in."""
    try:
        r = int(round(float(color.get("r", 0)) * 255))
        g = int(round(float(color.get("g", 0)) * 255))
        b = int(round(float(color.get("b", 0)) * 255))
        a = float(color.get("a", 1.0)) * float(opacity)
    except (TypeError, ValueError):
        return "transparent"
    return f"rgba({r},{g},{b},{a:.3f})"


def _first_solid_fill_css(node: dict) -> str:
    """Return the CSS background colour for the first visible solid fill,
    or 'transparent' if none."""
    for fill in node.get("fills", []) or []:
        if not isinstance(fill, dict):
            continue
        if fill.get("type") != "SOLID":
            continue
        if fill.get("visible") is False:
            continue
        return _rgba_to_css(fill.get("color") or {}, fill.get("opacity", 1.0))
    return "transparent"


# ──────────────────────────────────────────────────────────────────────
# Node rendering
# ──────────────────────────────────────────────────────────────────────

def _bbox(node: dict) -> tuple[float, float, float, float] | None:
    bb = node.get("absoluteBoundingBox")
    if not isinstance(bb, dict):
        return None
    try:
        return (
            float(bb["x"]), float(bb["y"]),
            float(bb["width"]), float(bb["height"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def _safe_text(value: Any) -> str:
    """Escape arbitrary text for HTML embedding."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def _render_node(node: dict, offset_x: float, offset_y: float) -> str:
    """Render a single node + its descendants to absolute-positioned HTML.

    `offset_x` / `offset_y` are the canvas-relative origin so a node's
    absoluteBoundingBox is converted to canvas-relative coordinates.
    """
    bbox = _bbox(node)
    node_type = node.get("type", "")

    # Skip nodes without a bounding box (DOCUMENT / CANVAS — handled at
    # higher level — or visibility:false nodes without coordinates).
    if not bbox and node_type not in ("FRAME", "GROUP"):
        # Still descend into children if any
        return "".join(
            _render_node(c, offset_x, offset_y)
            for c in node.get("children", []) or []
        )

    if node.get("visible") is False:
        return ""

    if bbox:
        x, y, w, h = bbox
        rel_x = x - offset_x
        rel_y = y - offset_y
        base_style = (
            f"position:absolute;left:{rel_x:.2f}px;top:{rel_y:.2f}px;"
            f"width:{w:.2f}px;height:{h:.2f}px;"
        )
    else:
        base_style = ""

    bg = _first_solid_fill_css(node)
    radius = node.get("cornerRadius") or 0
    name = _safe_text(node.get("name", ""))
    nid = _safe_text(node.get("id", ""))

    if node_type == "TEXT":
        style = node.get("style") or {}
        family = _safe_text(style.get("fontFamily", "Inter"))
        weight = style.get("fontWeight", 400)
        size = style.get("fontSize", 16)
        line_h = style.get("lineHeightPx") or float(size) * 1.4
        try:
            line_h_f = float(line_h)
        except (TypeError, ValueError):
            line_h_f = float(size) * 1.4
        characters = _safe_text(node.get("characters", ""))
        text_style = (
            f"color:{bg if bg != 'transparent' else 'inherit'};"
            f"font-family:'{family}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;"
            f"font-weight:{weight};"
            f"font-size:{size}px;"
            f"line-height:{line_h_f:.2f}px;"
            f"margin:0;padding:0;white-space:pre-wrap;"
        )
        return (
            f'<div class="figma-node figma-text" '
            f'data-id="{nid}" data-name="{name}" '
            f'style="{base_style}">'
            f'<p style="{text_style}">{characters}</p></div>'
        )

    if node_type in ("RECTANGLE", "ELLIPSE", "REGULAR_POLYGON", "STAR", "VECTOR"):
        shape_style = (
            f"background:{bg};border-radius:"
            f"{'50%' if node_type == 'ELLIPSE' else f'{radius}px'};"
        )
        return (
            f'<div class="figma-node figma-shape" '
            f'data-id="{nid}" data-name="{name}" '
            f'style="{base_style}{shape_style}"></div>'
        )

    if node_type in ("FRAME", "COMPONENT", "INSTANCE", "GROUP", "COMPONENT_SET"):
        frame_style = (
            f"background:{bg};"
            f"border-radius:{radius}px;"
            f"overflow:hidden;"
        )
        children = "".join(
            _render_node(c, offset_x, offset_y)
            for c in node.get("children", []) or []
        )
        return (
            f'<div class="figma-node figma-frame" '
            f'data-id="{nid}" data-name="{name}" '
            f'style="{base_style}{frame_style}">{children}</div>'
        )

    # Unknown / unsupported types — render an outline placeholder so the
    # layout slot is still visible without claiming the node was painted.
    children = "".join(
        _render_node(c, offset_x, offset_y)
        for c in node.get("children", []) or []
    )
    placeholder_style = (
        "background:transparent;border:1px dashed rgba(127,127,127,0.35);"
    )
    return (
        f'<div class="figma-node figma-unknown" '
        f'data-id="{nid}" data-name="{name}" data-type="{_safe_text(node_type)}" '
        f'style="{base_style}{placeholder_style}">{children}</div>'
    )


def _render_canvas(canvas: dict, index: int) -> dict:
    """Render one CANVAS (page) into a self-contained block."""
    bg_color = _rgba_to_css(canvas.get("backgroundColor") or {})
    name = _safe_text(canvas.get("name", f"Page {index + 1}"))
    nid = _safe_text(canvas.get("id", ""))

    # Compute the canvas bounds by union of child bboxes; fallback to
    # 1200×800 so an empty page still has a visible canvas.
    xs, ys, ws, hs = [], [], [], []
    for child in canvas.get("children", []) or []:
        bb = _bbox(child)
        if bb is None:
            continue
        x, y, w, h = bb
        xs.append(x)
        ys.append(y)
        ws.append(x + w)
        hs.append(y + h)
    if xs and ys:
        origin_x, origin_y = min(xs), min(ys)
        width = max(ws) - origin_x
        height = max(hs) - origin_y
    else:
        origin_x, origin_y, width, height = 0, 0, 1200, 800

    children_html = "".join(
        _render_node(c, origin_x, origin_y)
        for c in canvas.get("children", []) or []
    )

    canvas_html = (
        f'<section class="figma-canvas" data-id="{nid}" data-name="{name}" data-index="{index}">'
        f'<header class="figma-canvas-header">'
        f'<span class="figma-canvas-index">{index + 1}</span>'
        f'<span class="figma-canvas-name">{name}</span>'
        f'<span class="figma-canvas-dims">{int(width)} × {int(height)}</span>'
        f'</header>'
        f'<div class="figma-canvas-stage" '
        f'style="width:{width:.2f}px;height:{height:.2f}px;background:{bg_color};">'
        f'{children_html}'
        f'</div>'
        f'</section>'
    )
    return {"name": name, "html": canvas_html, "width": width, "height": height}


# ──────────────────────────────────────────────────────────────────────
# Page HTML
# ──────────────────────────────────────────────────────────────────────

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>__TITLE__</title>
  <style>
    :root {
      --bg: #F7F8FA;
      --fg: #0F1115;
      --muted: rgba(15,17,21,0.66);
      --chrome: #FFFFFF;
      --hairline: rgba(15,17,21,0.08);
      --accent: #5B7CFA;
    }
    :root[data-theme="dark"] {
      --bg: #0F1115;
      --fg: #F2F4F8;
      --muted: rgba(242,244,248,0.68);
      --chrome: #1A1D24;
      --hairline: rgba(255,255,255,0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--fg);
    }
    header.viewer-chrome {
      position: sticky;
      top: 0;
      z-index: 10;
      background: var(--chrome);
      border-bottom: 1px solid var(--hairline);
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    header.viewer-chrome .file-name {
      font-weight: 600;
      font-size: 14px;
    }
    header.viewer-chrome .file-meta {
      color: var(--muted);
      font-size: 12px;
    }
    header.viewer-chrome .help {
      margin-left: auto;
      color: var(--muted);
      font-size: 12px;
    }
    main.canvas-list {
      padding: 24px 20px 80px;
    }
    section.figma-canvas {
      max-width: 100%;
      margin: 0 auto 48px;
      background: var(--chrome);
      border: 1px solid var(--hairline);
      border-radius: 12px;
      overflow: hidden;
    }
    section.figma-canvas[hidden] { display: none; }
    .figma-canvas-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 16px;
      border-bottom: 1px solid var(--hairline);
      font-size: 13px;
    }
    .figma-canvas-index {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px; height: 22px;
      border-radius: 50%;
      background: var(--accent);
      color: white;
      font-weight: 600;
      font-size: 12px;
    }
    .figma-canvas-name { font-weight: 600; }
    .figma-canvas-dims { color: var(--muted); font-variant-numeric: tabular-nums; }
    .figma-canvas-stage {
      position: relative;
      margin: 24px auto;
      transform-origin: top left;
      box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
    }
    .figma-node { box-sizing: border-box; }
    .figma-unknown::after {
      content: attr(data-type);
      position: absolute;
      top: 4px; left: 4px;
      font-size: 10px;
      color: rgba(127,127,127,0.7);
    }
  </style>
</head>
<body>
  <header class="viewer-chrome">
    <span class="file-name">__TITLE__</span>
    <span class="file-meta">__META__</span>
    <span class="help">← → · 1..9 · d toggle dark</span>
  </header>
  <main class="canvas-list">__CANVASES__</main>
  <script>
    (function () {
      var canvases = Array.prototype.slice.call(document.querySelectorAll('section.figma-canvas'));
      if (canvases.length === 0) return;
      var current = 0;
      function show(i) {
        if (i < 0 || i >= canvases.length) return;
        current = i;
        canvases.forEach(function (c, idx) { c.hidden = idx !== current; });
        // Scale stage to viewport width if it overflows
        canvases.forEach(function (c) {
          var stage = c.querySelector('.figma-canvas-stage');
          if (!stage) return;
          var w = parseFloat(stage.style.width) || 0;
          var available = c.clientWidth - 32;
          var scale = w > available ? available / w : 1;
          stage.style.transform = 'scale(' + scale.toFixed(3) + ')';
          stage.style.marginBottom = ((parseFloat(stage.style.height) || 0) * (scale - 1)) + 'px';
        });
      }
      show(0);
      window.addEventListener('resize', function () { show(current); });
      window.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') show(Math.min(current + 1, canvases.length - 1));
        else if (e.key === 'ArrowLeft') show(Math.max(current - 1, 0));
        else if (e.key === 'd' || e.key === 'D') {
          var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
          document.documentElement.dataset.theme = next;
        } else if (e.key >= '1' && e.key <= '9') {
          show(parseInt(e.key, 10) - 1);
        }
      });
    })();
  </script>
</body>
</html>
"""


def render_html(file_data: dict) -> str:
    """Render a full Figma file dict to a single self-contained HTML page."""
    title = _safe_text(file_data.get("name", "Figma viewer"))
    last_modified = _safe_text(file_data.get("lastModified", ""))
    meta_parts = []
    if last_modified:
        meta_parts.append(f"Last modified {last_modified}")
    doc = file_data.get("document") or {}
    canvases = [c for c in doc.get("children", []) or [] if c.get("type") == "CANVAS"]
    meta_parts.append(f"{len(canvases)} page{'s' if len(canvases) != 1 else ''}")
    meta = " · ".join(meta_parts)

    if not canvases:
        canvases_html = (
            '<section class="figma-canvas"><header class="figma-canvas-header">'
            '<span class="figma-canvas-name">No pages</span></header>'
            '<div class="figma-canvas-stage" style="width:600px;height:200px;background:transparent;">'
            '<p style="position:absolute;top:80px;left:24px;color:rgba(127,127,127,0.7);">'
            'This Figma file has no CANVAS pages.</p></div></section>'
        )
    else:
        canvases_html = "".join(
            _render_canvas(c, idx)["html"] for idx, c in enumerate(canvases)
        )

    return (
        _HTML_TEMPLATE
        .replace("__TITLE__", title)
        .replace("__META__", _safe_text(meta))
        .replace("__CANVASES__", canvases_html)
    )


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Render a Figma file to a single self-contained HTML viewer.",
    )
    ap.add_argument(
        "file_key",
        nargs="?",
        help="Figma file key (segment after /file/ in the URL). "
        "Omit when using --fixture.",
    )
    ap.add_argument(
        "--fixture",
        type=Path,
        help="Offline mode: load a JSON fixture in Figma API response shape.",
    )
    ap.add_argument(
        "--token",
        default=os.environ.get("FIGMA_TOKEN"),
        help="Figma personal access token (default: $FIGMA_TOKEN).",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write the viewer HTML (default: figma-viewer.html).",
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

    html_doc = render_html(file_data)
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html_doc, encoding="utf-8")
    except OSError as e:
        sys.stderr.write(f"ERROR: write failed: {e}\n")
        return 1

    page_count = len(
        [c for c in (file_data.get("document") or {}).get("children", []) or []
         if c.get("type") == "CANVAS"]
    )
    print(f"✓ wrote {args.output} ({page_count} page(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
