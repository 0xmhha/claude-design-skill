/**
 * <deck-stage> — fixed-canvas slide deck web component
 *
 * Runs at a designer-fixed canvas size (default 1920×1080) and scales
 * to the viewport with letterbox bars. Speaker notes are colocated
 * with each slide via a nested `<aside slot="notes">`. Keyboard nav,
 * hash deep-link, position memory, blackout key, and a print sheet
 * that emits one canvas-sized page per slide are all built in.
 *
 * Children:
 *   <deck-stage>
 *     <section>
 *       <h1>Slide 1</h1>
 *       <aside slot="notes">Pace yourself; emphasize KPI #2.</aside>
 *     </section>
 *     <section>...</section>
 *   </deck-stage>
 *
 * Attributes:
 *   width / height        — canvas size in CSS px (default 1920 × 1080)
 *   noscale               — disable fit-to-viewport scaling
 *   broadcast-origin      — opt-in slide-change postMessage; values:
 *                           "self"  (same-origin parent only) or an
 *                           explicit https origin. Wildcard "*" is
 *                           intentionally NOT supported.
 *
 * Methods (instance · also on window.DeckStage class):
 *   .next()   .prev()   .goTo(idx)   .toggleNotes()   .blackout()
 *   .currentSlide        .totalSlides        .notesVisible
 *
 * Keyboard:
 *   ← / →                  prev / next
 *   space / pgdown        next
 *   pgup                  prev
 *   home / end            jump to first / last
 *   1–9                   jump to slide N
 *   n                     toggle speaker-notes overlay
 *   b                     blackout (press again to restore)
 *   esc                   close blackout / notes
 *
 * Print:
 *   Cmd / Ctrl + P emits one canvas-sized page per slide. Notes
 *   overlay, counter, and click-zone navs are hidden in print.
 *
 * CSS hooks (set on the host element):
 *   --deck-bg              page-letterbox background (default #0c0c0e)
 *   --deck-slide-bg        slide canvas background  (default #fff)
 *   --deck-stage-shadow    drop shadow under the canvas
 *   --deck-font            UI font for counter / notes panel
 */
(() => {
  const KEY_PREFIX = 'deck-stage-current-slide';

  class DeckStage extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      this.idx = 0;
      this.slides = [];
      this.notes = [];
      this.notesOpen = false;
      this.blacked = false;
      this._stageEl = null;
      this._counterEl = null;
      this._notesEl = null;
      this._notesBodyEl = null;
      this._key = `${KEY_PREFIX}::${location.pathname || 'default'}`;
    }

    connectedCallback() {
      this.W = parseInt(this.getAttribute('width'),  10) || 1920;
      this.H = parseInt(this.getAttribute('height'), 10) || 1080;

      this._renderShadow();
      this._cacheRefs();
      this._attachPrintSheet();
      this._attachKeyboard();
      this._attachResize();
      this._attachHash();

      const init = () => {
        this._collect();
        this._restore();
        this._render();
      };
      if (this.ownerDocument.readyState === 'loading') {
        this.ownerDocument.addEventListener('DOMContentLoaded', init, { once: true });
      } else {
        requestAnimationFrame(init);
      }
    }

    /* -------- shadow DOM bootstrap (no runtime interpolation) -------- */
    _renderShadow() {
      const style = document.createElement('style');
      style.textContent = `
        :host {
          display: block;
          position: fixed;
          inset: 0;
          background: var(--deck-bg, #0c0c0e);
          font-family: var(--deck-font,
            -apple-system, "SF Pro Text", "Segoe UI", system-ui, sans-serif);
          overflow: hidden;
        }
        :host([noscale]) #stage { transform: none !important; }

        #stage {
          position: absolute;
          top: 0; left: 0;
          transform-origin: top left;
          background: var(--deck-slide-bg, #fff);
          box-shadow: var(--deck-stage-shadow, 0 12px 60px rgba(0,0,0,0.45));
        }
        #stage > .slot-host { width: 100%; height: 100%; position: relative; }

        ::slotted(section) {
          position: absolute; inset: 0;
          overflow: hidden;
        }
        /* !important is required: caller stylesheets may set per-slide
           display (e.g. .slide.outro { display: flex }), which would
           otherwise win the cascade over a plain ::slotted display rule
           and leak hidden slides on top of the active one. */
        ::slotted(section:not(.is-active)) { display: none !important; }

        #counter {
          position: fixed; bottom: 18px; right: 22px;
          padding: 7px 14px;
          background: rgba(8,8,10,0.65);
          color: rgba(255,255,255,0.86);
          border-radius: 999px;
          font-size: 12.5px;
          font-variant-numeric: tabular-nums;
          letter-spacing: 0.08em;
          z-index: 100;
          opacity: 0.55;
          transition: opacity 180ms ease;
          user-select: none;
        }
        #counter:hover { opacity: 1; }

        .nav { position: fixed; top: 0; bottom: 0; width: 14%; cursor: pointer; z-index: 60; }
        .nav.l { left: 0; }
        .nav.r { right: 0; }
        .nav .hint {
          position: absolute; top: 50%; transform: translateY(-50%);
          width: 42px; height: 42px;
          background: rgba(255,255,255,0.10);
          color: rgba(255,255,255,0.7);
          border-radius: 999px;
          display: flex; align-items: center; justify-content: center;
          font-size: 22px;
          opacity: 0;
          transition: opacity 200ms ease;
        }
        .nav.l .hint { left: 22px; }
        .nav.r .hint { right: 22px; }
        .nav:hover .hint { opacity: 1; }

        #notes {
          position: fixed;
          left: 50%; bottom: 26px;
          transform: translateX(-50%);
          width: min(720px, 86vw);
          max-height: 36vh;
          padding: 18px 22px 20px;
          background: rgba(15, 16, 18, 0.94);
          color: rgba(255,255,255,0.92);
          font-size: 15px;
          line-height: 1.5;
          border-radius: 14px;
          box-shadow: 0 12px 40px rgba(0,0,0,0.45);
          overflow: auto;
          z-index: 110;
          display: none;
        }
        #notes.is-open { display: block; }
        #notes header {
          font-size: 11px;
          letter-spacing: 0.16em;
          text-transform: uppercase;
          color: rgba(255,255,255,0.55);
          margin-bottom: 8px;
        }

        #blackout {
          position: fixed; inset: 0;
          background: #000;
          z-index: 200;
          display: none;
        }
        :host([blacked]) #blackout { display: block; }

        @media print {
          :host { position: static; background: #fff; }
          #stage { position: static; transform: none !important; box-shadow: none; }
          #counter, .nav, #notes, #blackout { display: none !important; }
          ::slotted(section) {
            display: block !important;
            position: relative !important;
            width: ${this.W}px;
            height: ${this.H}px;
            page-break-after: always;
          }
          ::slotted(section:last-of-type) { page-break-after: auto; }
        }
      `;

      const stage = document.createElement('div');
      stage.id = 'stage';
      stage.style.width  = `${this.W}px`;
      stage.style.height = `${this.H}px`;
      const host = document.createElement('div');
      host.className = 'slot-host';
      host.appendChild(document.createElement('slot'));
      stage.appendChild(host);

      const navL = document.createElement('div'); navL.className = 'nav l';
      const navR = document.createElement('div'); navR.className = 'nav r';
      const hintL = document.createElement('div'); hintL.className = 'hint'; hintL.textContent = '‹';
      const hintR = document.createElement('div'); hintR.className = 'hint'; hintR.textContent = '›';
      navL.appendChild(hintL); navR.appendChild(hintR);

      const counter = document.createElement('div');
      counter.id = 'counter';
      counter.textContent = '01 / 01';

      const notes = document.createElement('div'); notes.id = 'notes';
      const notesHeader = document.createElement('header');
      notesHeader.textContent = 'Speaker notes';
      const notesBody = document.createElement('div'); notesBody.id = 'notes-body';
      notes.appendChild(notesHeader); notes.appendChild(notesBody);

      const blackout = document.createElement('div'); blackout.id = 'blackout';

      this.shadowRoot.append(style, stage, navL, navR, counter, notes, blackout);

      navL.addEventListener('click', () => this.prev());
      navR.addEventListener('click', () => this.next());
    }

    _cacheRefs() {
      const r = this.shadowRoot;
      this._stageEl     = r.getElementById('stage');
      this._counterEl   = r.getElementById('counter');
      this._notesEl     = r.getElementById('notes');
      this._notesBodyEl = r.getElementById('notes-body');
    }

    _attachPrintSheet() {
      // Inject @page rule into the host document so the PDF page size matches the canvas.
      // The shadow-DOM stylesheet alone cannot set @page in some browsers.
      const id = 'deck-stage-print-page-rule';
      if (document.getElementById(id)) return;
      const style = document.createElement('style');
      style.id = id;
      style.textContent = `@media print { @page { size: ${this.W}px ${this.H}px; margin: 0; } }`;
      document.head.appendChild(style);
    }

    _attachKeyboard() {
      document.addEventListener('keydown', (e) => {
        const t = e.target;
        if (t && t.matches && t.matches('input, textarea, select, [contenteditable=""], [contenteditable="true"]')) return;
        switch (e.key) {
          case 'ArrowRight': case ' ': case 'PageDown':
            e.preventDefault(); this.next(); break;
          case 'ArrowLeft': case 'PageUp':
            e.preventDefault(); this.prev(); break;
          case 'Home': e.preventDefault(); this.goTo(0); break;
          case 'End':  e.preventDefault(); this.goTo(this.slides.length - 1); break;
          case 'n': case 'N': e.preventDefault(); this.toggleNotes(); break;
          case 'b': case 'B': e.preventDefault(); this.blackout(); break;
          case 'Escape':
            if (this.blacked) { this.blacked = false; this.removeAttribute('blacked'); }
            else if (this.notesOpen) { this.toggleNotes(); }
            break;
          default:
            if (e.key >= '1' && e.key <= '9') {
              const i = parseInt(e.key, 10) - 1;
              if (i < this.slides.length) { e.preventDefault(); this.goTo(i); }
            }
        }
      });
    }

    _attachResize() {
      window.addEventListener('resize', () => this._fit());
    }

    _attachHash() {
      window.addEventListener('hashchange', () => this._consumeHash());
    }

    _consumeHash() {
      const m = location.hash.match(/^#slide-(\d+)$/);
      if (!m) return;
      const idx = parseInt(m[1], 10) - 1;
      if (idx >= 0 && idx < this.slides.length) this.goTo(idx);
    }

    _collect() {
      this.slides = Array.from(this.querySelectorAll(':scope > section'));
      this.notes = this.slides.map(section => {
        const aside = section.querySelector(':scope > aside[slot="notes"]');
        // Detach the notes element from light DOM. It cannot be distributed
        // through a slot (shadow-host slot routing only sees direct children
        // of the host, not grandchildren), so leaving it in place would
        // render it on top of the active slide. We keep the live reference
        // and clone its contents into the overlay on every slide change.
        if (aside && aside.parentNode) aside.parentNode.removeChild(aside);
        return aside;
      });
      this.slides.forEach((slide, i) => {
        if (!slide.hasAttribute('data-screen-label')) {
          slide.setAttribute('data-screen-label', String(i + 1).padStart(2, '0'));
        }
      });
    }

    _restore() {
      const m = location.hash.match(/^#slide-(\d+)$/);
      if (m) {
        const idx = parseInt(m[1], 10) - 1;
        if (idx >= 0 && idx < this.slides.length) { this.idx = idx; return; }
      }
      try {
        const v = parseInt(localStorage.getItem(this._key), 10);
        if (!Number.isNaN(v) && v >= 0 && v < this.slides.length) this.idx = v;
      } catch (_) { /* localStorage may be blocked */ }
    }

    _persist() {
      try { localStorage.setItem(this._key, String(this.idx)); } catch (_) {}
    }

    _fit() {
      if (this.hasAttribute('noscale')) {
        this._stageEl.style.transform = 'none';
        this._stageEl.style.left = '0';
        this._stageEl.style.top  = '0';
        return;
      }
      const vw = window.innerWidth, vh = window.innerHeight;
      const s  = Math.min(vw / this.W, vh / this.H);
      const x  = (vw - this.W * s) / 2;
      const y  = (vh - this.H * s) / 2;
      this._stageEl.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
    }

    _render() {
      this.slides.forEach((slide, i) => slide.classList.toggle('is-active', i === this.idx));
      const total = this.slides.length || 1;
      const pad   = String(total).length;
      const fmt   = (n) => String(n).padStart(pad, '0');
      this._counterEl.textContent = `${fmt(this.idx + 1)} / ${fmt(total)}`;
      this._fit();
      this._renderNotes();
      this._broadcast();
    }

    _renderNotes() {
      const body = this._notesBodyEl;
      while (body.firstChild) body.removeChild(body.firstChild);
      const node = this.notes[this.idx];
      if (node) {
        // Clone live notes content so author markup (lists, <strong>) renders.
        // Origin is the page itself — no untrusted HTML flows in.
        for (const child of node.childNodes) body.appendChild(child.cloneNode(true));
        body.style.opacity = '1';
      } else {
        body.textContent = '— no notes —';
        body.style.opacity = '0.45';
      }
    }

    _broadcast() {
      const target = this.getAttribute('broadcast-origin');
      if (!target) return;
      if (target === '*') return; // wildcard intentionally not supported
      const origin = target === 'self' ? window.location.origin : target;
      const payload = { type: 'deck-stage:slide', index: this.idx, total: this.slides.length };
      try { window.postMessage(payload, origin); } catch (_) {}
      try {
        if (window.parent && window.parent !== window) {
          window.parent.postMessage(payload, origin);
        }
      } catch (_) {}
    }

    /* -------- public API -------- */
    next()  { if (this.idx < this.slides.length - 1) { this.idx++; this._persist(); this._render(); } }
    prev()  { if (this.idx > 0)                       { this.idx--; this._persist(); this._render(); } }
    goTo(i) { if (i >= 0 && i < this.slides.length)  { this.idx = i;  this._persist(); this._render(); } }

    toggleNotes() {
      this.notesOpen = !this.notesOpen;
      this._notesEl.classList.toggle('is-open', this.notesOpen);
    }

    blackout() {
      this.blacked = !this.blacked;
      if (this.blacked) this.setAttribute('blacked', '');
      else              this.removeAttribute('blacked');
    }

    get currentSlide() { return this.idx; }
    get totalSlides()  { return this.slides.length; }
    get notesVisible() { return this.notesOpen; }
  }

  customElements.define('deck-stage', DeckStage);
  if (typeof window !== 'undefined') window.DeckStage = DeckStage;
})();
