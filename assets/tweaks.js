/**
 * <tweak-panel> + <tweak> — live design-tuning controls
 *
 * The author declares a panel and a few tweaks once; the component
 * renders a floating control panel (bottom-right by default), keeps
 * the chosen values in localStorage, and writes each value as a
 * `data-tweak-<name>` attribute on the document root. Caller CSS
 * reacts to those attributes — no caller JavaScript required.
 *
 * Markup (place at the end of <body>; one panel per page):
 *   <tweak-panel>
 *     <tweak name="palette"  options="warm|cool|neutral"
 *            default="warm"   label="Palette"></tweak>
 *     <tweak name="density"  options="compact|comfortable|spacious"
 *            default="comfortable" label="Density"></tweak>
 *     <tweak name="accent"   options="orange|blue|green"
 *            default="orange" label="Accent"></tweak>
 *   </tweak-panel>
 *
 * Caller CSS reads the attributes off <html>:
 *   :root[data-tweak-palette="warm"]    { --bg: #fef3c7; }
 *   :root[data-tweak-palette="cool"]    { --bg: #dbeafe; }
 *   :root[data-tweak-density="compact"] { --gap: 8px; }
 *
 * Hotkey: pressing `t` toggles the panel. Pressing `Esc` while the
 * panel is open hides it.
 *
 * <tweak-panel> attributes:
 *   position    "bottom-right" (default) | "bottom-left"
 *               | "top-right" | "top-left"
 *   open        present → panel starts visible (otherwise hidden until 't')
 *   hotkey      override the toggle key (default "t"; pass "" to disable)
 *
 * <tweak> attributes:
 *   name        required; becomes data-tweak-<name>. lowercase, kebab-case.
 *   options     required; pipe-separated value list (e.g. "a|b|c").
 *   default     required; one of the options.
 *   label       optional; display name in the panel (default = name).
 *
 * Events:
 *   document.addEventListener('tweakchange', e => {
 *     // e.detail = { name, value, source: 'user' | 'restore' }
 *   });
 *
 * Public API (instance methods on <tweak-panel>):
 *   .set(name, value)   — programmatically change a tweak
 *   .get(name)          — read the current value
 *   .values             — { name: value, ... } snapshot
 *   .reset()            — restore defaults and clear localStorage
 */
(() => {
  const STORAGE_PREFIX = 'tweak::';

  const POSITION_STYLES = {
    'bottom-right': { right: '20px',  bottom: '20px' },
    'bottom-left':  { left:  '20px',  bottom: '20px' },
    'top-right':    { right: '20px',  top:    '20px' },
    'top-left':     { left:  '20px',  top:    '20px' },
  };

  class TweakPanel extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      this.tweaks = [];          // [{ name, label, options[], default, current }]
      this.byName = new Map();
      this.isOpen = false;
      this._key = (name) => `${STORAGE_PREFIX}${location.pathname || '/'}::${name}`;
    }

    connectedCallback() {
      const init = () => {
        this._collect();
        this._renderShadow();
        this._restoreAll();
        this._applyAllToRoot('restore');
        this._attachHotkey();
        if (this.hasAttribute('open')) this._show();
      };
      if (this.ownerDocument.readyState === 'loading') {
        this.ownerDocument.addEventListener('DOMContentLoaded', init, { once: true });
      } else {
        requestAnimationFrame(init);
      }
    }

    _collect() {
      const els = Array.from(this.querySelectorAll(':scope > tweak'));
      // <tweak> is an unknown HTML element (no hyphen → not a registered
      // custom element by spec). Hide it explicitly so its default inline
      // box does not affect surrounding layout.
      els.forEach(el => { el.style.display = 'none'; });
      this.tweaks = els.map(el => {
        const name = (el.getAttribute('name') || '').trim();
        const optionsRaw = (el.getAttribute('options') || '').trim();
        const def = (el.getAttribute('default') || '').trim();
        const label = (el.getAttribute('label') || name).trim();
        const options = optionsRaw.split('|').map(s => s.trim()).filter(Boolean);
        if (!name || options.length === 0 || !def) {
          // Skip malformed declarations rather than crash; surface in console.
          console.warn('[tweak-panel] skipping malformed <tweak>:',
                       { name, options: optionsRaw, default: def });
          return null;
        }
        if (!options.includes(def)) {
          console.warn(`[tweak-panel] default "${def}" is not in options for "${name}"; using first option`);
        }
        return {
          name, label, options,
          default: options.includes(def) ? def : options[0],
          current: options.includes(def) ? def : options[0],
        };
      }).filter(Boolean);
      this.byName = new Map(this.tweaks.map(t => [t.name, t]));
    }

    _renderShadow() {
      const pos = POSITION_STYLES[this.getAttribute('position') || 'bottom-right']
                || POSITION_STYLES['bottom-right'];

      const style = document.createElement('style');
      style.textContent = `
        :host { all: initial; }

        .panel {
          position: fixed;
          ${Object.entries(pos).map(([k, v]) => `${k}: ${v};`).join(' ')}
          z-index: 9999;
          background: rgba(20, 21, 24, 0.94);
          color: rgba(255,255,255,0.92);
          font-family: -apple-system, "SF Pro Text", "Segoe UI", system-ui, sans-serif;
          font-size: 13px;
          line-height: 1.4;
          border-radius: 12px;
          box-shadow: 0 12px 40px rgba(0,0,0,0.45);
          padding: 14px 16px 16px;
          min-width: 240px;
          max-width: 320px;
          opacity: 0;
          transform: translateY(8px);
          pointer-events: none;
          transition: opacity 160ms ease, transform 160ms ease;
        }
        .panel.is-open {
          opacity: 1;
          transform: translateY(0);
          pointer-events: auto;
        }

        header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 11px;
          letter-spacing: 0.16em;
          text-transform: uppercase;
          color: rgba(255,255,255,0.55);
          margin-bottom: 12px;
        }
        header .reset {
          background: none;
          border: 1px solid rgba(255,255,255,0.18);
          color: rgba(255,255,255,0.65);
          font-size: 10px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          padding: 3px 8px;
          border-radius: 999px;
          cursor: pointer;
          font-family: inherit;
        }
        header .reset:hover { color: #fff; border-color: rgba(255,255,255,0.4); }

        .row { display: flex; flex-direction: column; gap: 5px; margin-top: 10px; }
        .row:first-of-type { margin-top: 0; }
        .row-label {
          font-size: 12px;
          color: rgba(255,255,255,0.7);
        }

        .seg {
          display: inline-flex;
          background: rgba(255,255,255,0.06);
          border-radius: 8px;
          padding: 3px;
        }
        .seg button {
          background: transparent;
          border: none;
          color: rgba(255,255,255,0.7);
          font-family: inherit;
          font-size: 12px;
          padding: 5px 10px;
          border-radius: 6px;
          cursor: pointer;
          transition: background 140ms ease, color 140ms ease;
        }
        .seg button:hover { color: #fff; }
        .seg button.is-on {
          background: rgba(255,255,255,0.16);
          color: #fff;
        }

        .hint {
          margin-top: 12px;
          font-size: 10.5px;
          letter-spacing: 0.04em;
          color: rgba(255,255,255,0.4);
        }
      `;

      const panel = document.createElement('div');
      panel.className = 'panel';
      panel.setAttribute('role', 'group');
      panel.setAttribute('aria-label', 'Live tweak panel');

      const header = document.createElement('header');
      const title = document.createElement('span');
      title.textContent = 'Tweaks';
      const reset = document.createElement('button');
      reset.className = 'reset';
      reset.type = 'button';
      reset.textContent = 'Reset';
      reset.addEventListener('click', () => this.reset());
      header.append(title, reset);
      panel.appendChild(header);

      this.tweaks.forEach(t => {
        const row = document.createElement('div');
        row.className = 'row';
        const lab = document.createElement('div');
        lab.className = 'row-label';
        lab.textContent = t.label;
        const seg = document.createElement('div');
        seg.className = 'seg';
        seg.setAttribute('role', 'radiogroup');
        seg.setAttribute('aria-label', t.label);
        t.options.forEach(opt => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.dataset.value = opt;
          btn.textContent = opt;
          btn.setAttribute('role', 'radio');
          btn.setAttribute('aria-checked', String(opt === t.current));
          if (opt === t.current) btn.classList.add('is-on');
          btn.addEventListener('click', () => this.set(t.name, opt, 'user'));
          seg.appendChild(btn);
        });
        row.append(lab, seg);
        panel.appendChild(row);
      });

      const hint = document.createElement('div');
      hint.className = 'hint';
      const key = this.getAttribute('hotkey');
      if (key !== '') {
        hint.textContent = `Press "${(key || 't').toUpperCase()}" to toggle · Esc to close`;
      } else {
        hint.textContent = 'Hotkey disabled';
      }
      panel.appendChild(hint);

      this.shadowRoot.append(style, panel);
      this._panelEl = panel;
    }

    _attachHotkey() {
      const key = this.getAttribute('hotkey');
      if (key === '') return; // explicitly disabled
      const wantedKey = (key || 't').toLowerCase();
      this._keyHandler = (e) => {
        const t = e.target;
        if (t && t.matches && t.matches('input, textarea, select, [contenteditable=""], [contenteditable="true"]')) return;
        if (e.key.toLowerCase() === wantedKey && !e.metaKey && !e.ctrlKey && !e.altKey) {
          e.preventDefault();
          this._toggle();
        } else if (e.key === 'Escape' && this.isOpen) {
          this._hide();
        }
      };
      document.addEventListener('keydown', this._keyHandler);
    }

    _toggle() { this.isOpen ? this._hide() : this._show(); }
    _show()   { this.isOpen = true;  this._panelEl.classList.add('is-open');    this.setAttribute('open', ''); }
    _hide()   { this.isOpen = false; this._panelEl.classList.remove('is-open'); this.removeAttribute('open'); }

    /* -------- value persistence + application -------- */

    _restoreAll() {
      this.tweaks.forEach(t => {
        try {
          const stored = localStorage.getItem(this._key(t.name));
          if (stored !== null && t.options.includes(stored)) t.current = stored;
        } catch (_) { /* localStorage may be blocked */ }
      });
    }

    _persist(name, value) {
      try { localStorage.setItem(this._key(name), value); } catch (_) {}
    }

    _applyAllToRoot(source) {
      this.tweaks.forEach(t => this._applyOneToRoot(t, source, /*emit=*/ source === 'user'));
    }

    _applyOneToRoot(t, source, emit) {
      // dataset auto-converts: dataset.tweakPalette → data-tweak-palette
      // We want the attribute name verbatim from `name`, so write directly:
      const attr = `data-tweak-${t.name}`;
      document.documentElement.setAttribute(attr, t.current);
      if (emit) {
        document.dispatchEvent(new CustomEvent('tweakchange', {
          detail: { name: t.name, value: t.current, source },
        }));
      }
    }

    _updateButtons(t) {
      const btns = this._panelEl.querySelectorAll(`.row .seg button`);
      btns.forEach(btn => {
        if (btn.parentElement.getAttribute('aria-label') !== t.label) return;
        const on = btn.dataset.value === t.current;
        btn.classList.toggle('is-on', on);
        btn.setAttribute('aria-checked', String(on));
      });
    }

    /* -------- public API -------- */

    set(name, value, source = 'user') {
      const t = this.byName.get(name);
      if (!t) return;
      if (!t.options.includes(value)) return;
      if (t.current === value) return;
      t.current = value;
      this._persist(name, value);
      this._applyOneToRoot(t, source, /*emit=*/ true);
      this._updateButtons(t);
    }

    get(name) {
      const t = this.byName.get(name);
      return t ? t.current : undefined;
    }

    get values() {
      const out = {};
      this.tweaks.forEach(t => { out[t.name] = t.current; });
      return out;
    }

    reset() {
      this.tweaks.forEach(t => {
        if (t.current !== t.default) {
          t.current = t.default;
          try { localStorage.removeItem(this._key(t.name)); } catch (_) {}
          this._applyOneToRoot(t, 'user', /*emit=*/ true);
          this._updateButtons(t);
        } else {
          // still clear storage so reload starts clean
          try { localStorage.removeItem(this._key(t.name)); } catch (_) {}
        }
      });
    }
  }

  // Note: <tweak> deliberately is NOT a custom element — the web-components
  // spec requires a hyphen in registered names ("tweak" alone is illegal),
  // and the panel only needs to read attributes off the children. Leaving
  // <tweak> as a plain unknown HTML element keeps the markup short.

  if (!customElements.get('tweak-panel')) customElements.define('tweak-panel', TweakPanel);

  if (typeof window !== 'undefined') {
    window.TweakPanel = TweakPanel;
  }
})();
