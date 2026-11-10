"""Make the 1200x630 share images (assets/img/og*.png) used by WhatsApp, X, Facebook, LinkedIn.

Needs Playwright with Chrome:  pip install playwright && python3 -m playwright install chromium
Run:  python3 tools/og.py
"""
import os
import pathlib
import re

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPRITE = (ROOT / "assets/icons/sprite.svg").read_text()
LOCKUP = (ROOT / "assets/brand/ganor-lockup-currentcolor.svg").read_text()
LOCKUP = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r"\1", LOCKUP, count=2).replace("<svg", '<svg class="lock"', 1)


def icon(name, cls=""):
    return f'<svg class="i {cls}"><use href="#i-{name}"/></svg>'


# file, kicker, title (use <br>), subtitle, big icon, chips [(icon, text)], url
CARDS = [
    ("og.png", "Events · Tickets · Places", "Your city,<br>found.",
     "Find what’s happening near you. Host an event, sell tickets, scan guests in.",
     None, [("search", "Find events"), ("ticket", "Sell tickets"), ("scan", "Gate check-in"), ("shop", "Places")], "ganor.ng"),
    ("og-docs.png", "Docs", "How Ganor<br>works.",
     "Create an event, sell tickets, share one link and check guests in.",
     "doc", [("calendar", "Create"), ("share", "Share"), ("ticket", "Sell"), ("scan", "Gate")], "ganor.ng/docs"),
    ("og-terms.png", "Legal", "Terms<br>of use.",
     "The rules for hosting, buying and listing on Ganor, written to be read.",
     "shield", [], "ganor.ng/terms"),
    ("og-privacy.png", "Legal", "Privacy<br>policy.",
     "What we collect, why, and your rights under the Nigeria Data Protection Act 2023.",
     "lock", [], "ganor.ng/privacy"),
    ("og-refunds.png", "Legal", "Refund<br>policy.",
     "Ask the host first. If an event is cancelled, you get your money back.",
     "wallet", [], "ganor.ng/refunds"),
    ("og-credits.png", "Credits", "Credits and<br>licences.",
     "The icons, typefaces and logos that help make Ganor.",
     "star", [], "ganor.ng/credits"),
]

CSS = """
html,body{margin:0}
body{width:1200px;height:630px;overflow:hidden;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.c{position:relative;width:1200px;height:630px;box-sizing:border-box;background:#3730B8 url(../assets/img/pattern-indigo.svg);background-size:96px 192px;color:#fff;overflow:hidden}
.fade{position:absolute;inset:0;background:linear-gradient(90deg,#3730B8 0%,#3730B8 46%,rgba(55,48,184,.6) 72%,rgba(55,48,184,.15) 100%)}
.in{position:relative;height:100%;box-sizing:border-box;padding:64px 72px;display:flex;flex-direction:column}
.lock{height:50px;width:auto;color:#fff;align-self:flex-start}
.k{margin:auto 0 14px;font:600 20px/1 Inter;letter-spacing:3px;text-transform:uppercase;color:#C9C3E8}
h1{margin:0;font:800 104px/.98 'Bricolage Grotesque';font-variation-settings:'opsz' 48;letter-spacing:-.012em}
p.s{margin:18px 0 0;max-width:640px;font:500 26px/1.35 Inter;color:rgba(255,255,255,.88)}
.foot{margin-top:30px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:10px;height:48px;padding:0 20px 0 14px;border-radius:999px;background:rgba(255,255,255,.12);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.28);font:600 20px/1 Inter}
.chip .i{width:26px;height:26px}
.url{display:inline-flex;align-items:center;height:48px;padding:0 20px;border-radius:999px;background:#fff;color:#3730B8;font:700 20px/1 Inter}
.tile{position:absolute;right:84px;top:50%;width:300px;height:300px;margin-top:-150px;border-radius:72px;background:#fff;color:#3730B8;display:grid;place-items:center;transform:rotate(-6deg);box-shadow:0 40px 80px -30px rgba(21,19,42,.55)}
.tile .i{width:168px;height:168px}
.tile:after{content:"";position:absolute;inset:-22px;border-radius:90px;box-shadow:inset 0 0 0 2px rgba(255,255,255,.35)}
.stack{position:absolute;right:76px;top:96px;display:grid;gap:18px}
.stack .t{width:116px;height:116px;border-radius:32px;background:#fff;color:#3730B8;display:grid;place-items:center;box-shadow:0 26px 50px -24px rgba(21,19,42,.6)}
.stack .t .i{width:64px;height:64px}
.stack .t:nth-child(1){transform:translateX(-60px) rotate(-8deg)}
.stack .t:nth-child(2){transform:translateX(30px) rotate(5deg)}
.stack .t:nth-child(3){transform:translateX(-30px) rotate(-3deg)}
"""


def card_html(kicker, title, sub, big, chips, url):
    chips_html = "".join(f'<span class="chip">{icon(i)}{t}</span>' for i, t in chips)
    if big:
        art = f'<div class="tile">{icon(big)}</div>'
    else:
        art = '<div class="stack">' + "".join(f'<div class="t">{icon(n)}</div>' for n in ("ticket", "location", "scan")) + "</div>"
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/css/fonts.css"><style>{CSS}</style></head><body>
{SPRITE}
<div class="c"><div class="fade"></div>{art}<div class="in">
{LOCKUP}
<p class="k">{kicker}</p>
<h1>{title}</h1>
<p class="s">{sub}</p>
<div class="foot">{chips_html}<span class="url">{url}</span></div>
</div></div></body></html>"""


def main():
    tmp = ROOT / "tools" / "_og.html"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for name, *rest in CARDS:
            tmp.write_text(card_html(*rest))
            pg.goto(tmp.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(ROOT / "assets/img" / name), type="png")
            print("made", name)
        b.close()
    tmp.unlink()


if __name__ == "__main__":
    main()
