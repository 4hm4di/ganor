# ganor.ng

The pre-launch site for **Ganor** — find what's happening in Kano. Opens 30 November 2026.

Plain HTML, CSS and JavaScript. No framework and no runtime dependencies.

## Structure

```
src/                 Page sources (edit these)
  index.html
  credits.html
  404.html
  partials/          head, header, footer
assets/
  css/fonts.css      Self-hosted brand fonts (Bricolage Grotesque, Inter)
  css/tokens.css     Brand tokens (colour, type, radius, motion)
  fonts/             Font files and their OFL licences
  css/site.css       Site styles
  js/site.js         Intro, reveals, demos, waitlist form
  brand/             Logo lockups, symbol, loader, wordmark
  icons/sprite.svg   Icon sprite (Solar, CC BY 4.0, see /credits)
  gate/              Gate check-in status graphics
  social/            Social icons (Feather and Tabler, MIT)
  img/               Pattern tile, share image (og.png)
tools/build.py       Builds src/ into the root HTML files
index.html, credits.html, 404.html   Built output (committed, served as-is)
```

## Build

Requires Python 3 and the `qrcode` package (for the sample ticket QR).

```sh
pip install qrcode
python3 tools/build.py
```

The build expands these tags in `src/*.html`:

| Tag | Does |
| --- | --- |
| `{{include:name}}` | Inserts `src/partials/name.html` |
| `{{sprite}}` | Inlines the icon sprite |
| `{{icon:name\|class}}` | An icon from the sprite |
| `{{svg:path\|class}}` | Inlines an SVG file |
| `{{qr:text}}` | A QR code SVG for the text |

Always edit `src/`, then rebuild. Don't edit the root HTML files by hand.

## Preview

```sh
python3 -m http.server 8080
```

Open http://localhost:8080. To test on a phone, open `http://<your-computer-ip>:8080` on the same Wi-Fi.

The first-visit intro plays once per browser session. To see it again, open a new tab or clear `sessionStorage`.

## Waitlist

The form in `#join` posts JSON to the URL in its `data-endpoint` attribute:

```json
{ "role": "host", "name": "…", "phone": "…", "interest": "…", "source": "ganor.ng" }
```

With no endpoint set, it opens WhatsApp with the details filled in, so sign-ups still reach the team. To collect sign-ups in a sheet or form service, set `data-endpoint` on the `<form data-join>` in `src/index.html` and rebuild.

## Deploy (GitHub Pages)

1. Repo settings → Pages → Deploy from branch → `main`, folder `/ (root)`.
2. Preview address: https://4hm4di.github.io/ganor/ (all paths are relative, so the site works there and on the domain).
3. When DNS is ready: add a `CNAME` file containing `ganor.ng`, set the custom domain in Pages settings, then tick **Enforce HTTPS** once the certificate is issued.
4. DNS at the registrar:
   - `A @` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME www` → `<github-username>.github.io`

## Content rules

- Fees, payout times and similar claims stay off the site until payments are final.
- Screens in the demos use sample data and are labelled as samples.
- Hausa copy only where it has been approved.
