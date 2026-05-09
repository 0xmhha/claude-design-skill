# Prototype ↔ Production Boundary

> The skill produces **prototype** HTML — fast iteration, demo-quality, designer-driven. Several patterns it uses are **not safe for production** without rework. This document is the explicit boundary list and the migration path for each pattern.
>
> Read this before any prototype is shared with users outside the design team (clients, public beta, app stores).

---

## 0 · Why a separate document

Designers in a game / web3 studio routinely send their prototypes to:
- Internal stakeholders (PM / engineering / leadership)
- External clients (publisher / partner / investor reviews)
- Public beta channels (Discord, Telegram, X)
- Internal staging or app-store soft launch

The skill's prototype patterns are tuned for **the first audience** (internal design review, double-click-and-open HTML). Sending the same artifact to the second / third / fourth audience without modification leaks development-mode signals and exposes attack surface that prototype designers don't have to think about.

This document marks every "OK in prototype, dangerous in production" pattern and gives the conversion path.

---

## 1 · Boundary table

| # | Prototype pattern | Production reality | Migration |
|---|---|---|---|
| 1 | `react.development.js` from unpkg.com | 5× slower, dev warnings exposed, dev-only code paths active. Available offline if unpkg is down: **no**. | Switch to `react.production.min.js` AND vendor a copy under `vendor/` so unpkg outages don't break the deploy. See §2. |
| 2 | `<script src="@babel/standalone">` (5MB compiler in the browser) | Compiles JSX every page load. The compile is dynamic code execution at runtime — any user-controlled JSX = RCE. | Pre-compile JSX with esbuild / vite / swc at build time. Babel-standalone is removed. See §3. |
| 3 | `<script type="text/babel">` JSX inline blocks | Same as #2 — runtime compile. | Same migration as #2 — convert each block to a pre-compiled JS bundle. |
| 4 | API keys read from a DOM `<input>` and used by `fetch` | Plaintext in DOM, browser autofill, DevTools network tab. Any extension or analytics SDK can read it. | Use a **proxy backend** the user authenticates against (SSO / session cookie). The browser never holds the upstream API key. See §4. |
| 5 | `localStorage` for tweaks / state | Persistent across reloads. **Not** persistent across users. **Not** secure. Anyone with shared-machine access reads it. | Move user-specific state behind authenticated session storage on the backend. Tweaks panels are designer tools, not user-facing features anyway. |
| 6 | Inline raw external SVG | XSS vector. Mitigated by `references/svg-sanitize.md`, but production should also have CSP without `'unsafe-inline'`. | Pre-sanitize all assets at build time, then ship a tightened CSP (no `'unsafe-inline'` script-src). |
| 7 | Allowlisted CDN font fetch (`fonts.googleapis.com`) | Privacy concern (Google sees IP+UA of every visitor) and adds a 3rd-party request to the critical path. | Self-host the WOFF2 files. The font loader becomes `font-src 'self'` only. |
| 8 | `<meta http-equiv="Content-Security-Policy" content="… 'unsafe-inline' …">` (the prototype CSP) | `'unsafe-inline'` defeats most of CSP's value. Acceptable only because Babel-standalone needs it. | After #2 is migrated, remove `'unsafe-inline'` and use nonces or hashes. |
| 9 | `personal-asset-index.json` (already removed in this fork) | n/a | Use `team-brand-spec.json` (`security-config.md` §4) — already the only path. |
| 10 | `curl -A "Mozilla/5.0"` style scraping (already forbidden in this fork) | n/a | Allowlist + user-approval (`security-config.md`). |

---

## 2 · Migrating React/Babel CDN → Vendored Production Build

**Prototype version (current default)**:
```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js"
        integrity="sha384-…" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
        integrity="sha384-…" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
        integrity="sha384-…" crossorigin="anonymous"></script>
```

**Production version (vendored, no Babel)**:

Step 1 — vendor React / React-DOM into the project:
```bash
mkdir -p vendor/react@18.3.1
curl -o vendor/react@18.3.1/react.production.min.js \
  https://unpkg.com/react@18.3.1/umd/react.production.min.js
curl -o vendor/react@18.3.1/react-dom.production.min.js \
  https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js
# verify SRI before committing
shasum -a 384 -b vendor/react@18.3.1/*.js | base64
```

Step 2 — pre-compile every `<script type="text/babel">` block via esbuild / vite / swc. The output is a single `dist/app.js`. No Babel runtime in the browser.

Step 3 — update HTML:
```html
<script src="./vendor/react@18.3.1/react.production.min.js"></script>
<script src="./vendor/react@18.3.1/react-dom.production.min.js"></script>
<script src="./dist/app.js"></script>
```

Step 4 — tighten the CSP:
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src  'self';
  style-src   'self';
  font-src    'self';
  img-src     'self' data:;
  connect-src 'self';
  frame-src   'none';
  object-src  'none';
  base-uri    'self';
">
```

`'unsafe-inline'` is gone. Inline event handlers and inline `<script>` tags will no longer execute.

---

## 3 · Migrating Babel-Standalone JSX → Pre-compiled Bundle

The skill ships JSX files (`assets/*.jsx`) that are used inline at prototype time. For production:

**Build setup (esbuild)**:
```bash
npm install -D esbuild

cat > build.mjs <<'JS'
import { build } from 'esbuild';
await build({
  entryPoints: ['src/app.jsx'],
  bundle: true,
  outfile: 'dist/app.js',
  jsx: 'automatic',
  target: ['es2020'],
  minify: true,
  external: ['react', 'react-dom'],
});
JS

node build.mjs
```

For Tweaks / animations / device frames bundled together, change `entryPoints` to a single `src/app.jsx` that imports them.

**Result**: the production HTML has `<script src="./dist/app.js">` and **zero runtime compile**. RCE risk via JSX injection is eliminated structurally.

---

## 4 · Migrating Direct API Key Use → Proxy Backend

This is the most important migration. Direct API key use in the browser is **never** acceptable in production — even for "internal" tools.

**Prototype version** (was Option B in `react-setup.md`, **removed in this fork**):
```html
<input id="api-key" />
<script>
  fetch('https://api.anthropic.com/v1/messages', {
    headers: { 'x-api-key': document.getElementById('api-key').value }
  });
</script>
```

**Production pattern · proxy backend**:

Backend (any framework — Cloudflare Worker / Deno / Express / FastAPI):
```javascript
// pseudocode — reject anything not coming from an authenticated session
export default {
  async fetch(req, env) {
    const session = await authenticate(req);  // SSO cookie / session token / OAuth
    if (!session) return new Response('Unauthorized', { status: 401 });

    // Optional: rate-limit per session, sanitize prompts, log for audit
    const body = await req.json();

    const upstream = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': env.ANTHROPIC_API_KEY,   // server-side secret, never sent to browser
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    return new Response(upstream.body, { headers: upstream.headers });
  },
};
```

Browser:
```html
<script>
window.claude = {
  async complete(prompt) {
    // No API key in the browser. Session cookie carries the auth.
    const res = await fetch('/api/claude/complete', {
      method: 'POST',
      credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    return (await res.json()).content[0].text;
  }
};
</script>
```

**Properties**:
- API key lives on the server (env var). The browser never sees it.
- Session cookies are `HttpOnly; Secure; SameSite=Lax` → not readable from JS.
- Rate-limiting and audit logging happen at the proxy.
- If the prototype is exposed beyond the team, no key gets exposed with it.

For a quick internal proxy: deploy as a Cloudflare Worker pointing at `https://api.anthropic.com`. ~30 lines of code, $5/mo.

---

## 5 · Pre-Production Checklist

Before sending a prototype to anyone outside the design team, walk this list:

- [ ] React: switched from `*.development.js` → `*.production.min.js`, vendored under `vendor/`.
- [ ] No `<script src="@babel/standalone">` and no `<script type="text/babel">` blocks remain.
- [ ] No `<input>` element exists with `id`, `name`, or `placeholder` matching `key`, `secret`, `token`, `password`.
- [ ] All API calls go to a same-origin proxy or a documented internal endpoint — never directly to a third-party API host with credentials.
- [ ] CSP `'unsafe-inline'` removed (now possible because Babel is gone).
- [ ] Every external SVG used has a corresponding entry in `assets/*/PROVENANCE.md` with sanitize hashes.
- [ ] Fonts self-hosted (no `fonts.googleapis.com` request).
- [ ] No `localStorage` keys store user-identifying or secret data — only ephemeral UI state.
- [ ] `team-brand-spec.json` checked for placeholder values (`"REPLACE_ME"`, example.com URLs).
- [ ] `--no-watermark` applied for any external delivery (Group E).

---

## 6 · Skill-side enforcement

The skill itself cannot run a build pipeline, but it can:
1. **Mark patterns explicitly** in `references/react-setup.md` with `> ⚠ prototype only — see production-boundaries.md` callouts.
2. **Refuse to add Option B-style direct key code** (the previous `react-setup.md` Option B is removed in this fork).
3. **Default `team-brand-spec.json` lookup** is preferred over `personal-asset-index.json` (which is removed).

When a designer asks "make this production-ready", the skill should walk this checklist with them, rather than try to silently swap files.

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `security-config.md` · `svg-sanitize.md` · `react-setup.md` · `PROJECT-PLAN.md` Phase 1 Group C
