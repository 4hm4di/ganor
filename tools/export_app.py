#!/usr/bin/env python3
"""Export the built site into the Ganor app as its public homepage ("launch mode").

    python3 tools/build.py && python3 tools/export_app.py [path/to/ganor-app]

Copies index.html, the legal pages and assets/ into the app's public/ folder, then
switches pre-launch pieces to the live app:
  * "Host your event" buttons go to /dashboard (sign-in first if needed); a Sign in link is added
  * the hero search, chips and category cards open /events with the right filters
  * the "Ganor opens in" countdown becomes "Ganor is open" with sign-up and browse buttons
    (the updates form stays for Ganor Places, which is still coming soon)
The source site (ganor.ng) is untouched; run this again after editing src/.
"""
import pathlib
import re
import shutil
import sys
from urllib.parse import quote_plus

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent / "ganor-app"
PUBLIC = APP / "public"
PAGES = ["index.html", "docs.html", "terms.html", "privacy.html", "refunds.html"]
ROOT_FILES = ["favicon.ico", "favicon.svg", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png",
              "android-chrome-192x192.png", "android-chrome-512x512.png", "maskable-512x512.png", "site.webmanifest"]


def sub(text: str, old: str, new: str, count: int = 1, page: str = "") -> str:
    """Replace exactly `count` occurrences (0 = all, at least one) or fail loudly."""
    n = text.count(old)
    if n == 0 or (count and n != count):
        sys.exit(f"export_app: expected {count or 'some'} of {old[:60]!r} in {page}, found {n}")
    return text.replace(old, new)


def launch(html: str, page: str) -> str:
    # Header and menu: host CTA goes into the app; add Sign in.
    html = re.sub(r'href="\./#join"(\s*(?:data-menu-link)?\s*)><span>Host your event', r'href="/dashboard"\1><span>Host your event', html)
    html = sub(html, '<a href="docs.html">Docs</a>\n', '<a href="docs.html">Docs</a>\n      <a href="/login">Sign in</a>\n', 0, page)
    html = re.sub(r'(<li style="--i:5"><a href="\./#faq" data-menu-link><span class="sheet__row"><b>FAQ</b></span></a></li>)',
                  r'\1\n      <li style="--i:6"><a href="/login" data-menu-link><span class="sheet__row"><b>Sign in</b></span></a></li>', html)
    if page != "index.html":
        return html

    # Hero search: a real GET form to /events (no data-search, so the pre-launch script leaves it alone).
    html = sub(html, '<form class="search" data-search role="search"', '<form class="search" action="/events" method="get" role="search"', 1, page)
    html = sub(html, '<select name="area">', '<select name="city">', 1, page)

    # Chips and category cards become links to filtered event lists.
    def chip(m: re.Match) -> str:
        return f'<a class="chip" href="/events?type={quote_plus(m.group(1))}">{m.group(2)}</a>'
    html, n = re.subn(r'<button class="chip" type="button" data-chip="([^"]+)">(.*?)</button>', chip, html, flags=re.S)
    if n < 3:
        sys.exit("export_app: chips not found")
    html = re.sub(r'<button class="chip chip--halal" type="button" aria-pressed="false" data-halal>(.*?)</button>',
                  r'<a class="chip chip--halal" href="/events?halal=1">\1</a>', html, flags=re.S)
    html, n = re.subn(r'<a class="cat" href="#join" data-interest="([^"]+)"',
                      lambda m: f'<a class="cat" href="/events?type={quote_plus(m.group(1))}"', html)
    if n < 6:
        sys.exit("export_app: category cards not found")

    # Pricing card CTA.
    html = sub(html, '<a class="btn btn--light btn--block" href="#join"><span>Host your event</span>',
               '<a class="btn btn--light btn--block" href="/dashboard"><span>Host your event</span>', 1, page)

    # Join: countdown and pre-launch copy become launch copy with two buttons; the form stays for Places updates.
    start = html.index('<p class="label label--on-indigo" data-reveal>Ganor opens in</p>')
    end = html.index('</p>', html.index('class="join__lede"')) + len('</p>')
    arrow = '<span class="btn__arrow"><svg class="i" aria-hidden="true" focusable="false"><use href="#i-arrow"/></svg></span>'
    html = html[:start] + f'''<p class="label label--on-indigo" data-reveal>Ganor is open</p>
      <h2 class="join__title" id="join-title" data-lines><span class="line"><span>Host here today.</span></span></h2>
      <p class="join__lede" data-reveal>Create your event in minutes, sell tickets on one link and scan guests in at the gate. Looking for something to go to? See what’s on.</p>
      <div class="join__ctas" data-reveal>
        <a class="btn btn--light" href="/login?mode=signup"><span>Create your host account</span>{arrow}</a>
        <a class="btn btn--ghost-light" href="/events"><span>Find events</span>{arrow}</a>
      </div>
      <p class="join__lede join__lede--small" data-reveal>Own a business or want updates? Leave your details and we’ll tell you when Ganor Places opens.</p>''' + html[end:]

    # The updates form now mainly serves businesses waiting for Ganor Places.
    html = sub(html, '<input type="radio" name="role" value="host" checked>', '<input type="radio" name="role" value="host">', 1, page)
    html = sub(html, '<input type="radio" name="role" value="business">', '<input type="radio" name="role" value="business" checked>', 1, page)

    # Small style additions for the launch buttons.
    html = sub(html, '</head>', '''<style>
a.chip{text-decoration:none}
.join__ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px}
.btn--ghost-light{background:transparent;color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.6)}
.join__lede--small{font-size:15px;line-height:22px;margin-top:20px;color:rgba(255,255,255,.75)}
</style>
</head>''', 1, page)
    return html


def main() -> None:
    if not (PUBLIC.is_dir()):
        sys.exit(f"export_app: {PUBLIC} not found")
    for page in PAGES:
        src = ROOT / page
        (PUBLIC / page).write_text(launch(src.read_text(), page))
    for name in ROOT_FILES:
        if (ROOT / name).exists():
            shutil.copy2(ROOT / name, PUBLIC / name)
    dest = PUBLIC / "assets"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ROOT / "assets", dest, ignore=shutil.ignore_patterns("*.ai", "*.psd", "*.zip", "brand-guidelines*", "BRAND.md"))
    print(f"exported {len(PAGES)} pages and assets to {PUBLIC}")


if __name__ == "__main__":
    main()
