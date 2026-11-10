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


# file, kicker, title (use <br>), subtitle, phone screen (find|pay|ticket), chips [(icon, text)], url
# The phone screens are taken from the live hero on index.html (see shoot_phones below).
CARDS = [
    ("og.png", "Events · Tickets · Places", "Your city,<br>found.",
     "Find what’s happening near you. Host an event, sell tickets, scan guests in.",
     "find", [("search", "Find events"), ("ticket", "Sell tickets"), ("scan", "Check-in")], "ganor.ng"),
    ("og-docs.png", "Docs", "How Ganor<br>works.",
     "Create an event, sell tickets, share one link and check guests in.",
     "pay", [("calendar", "Create"), ("share", "Share"), ("scan", "Gate")], "ganor.ng/docs"),
    ("og-terms.png", "Legal", "Terms<br>of use.",
     "The rules for hosting, buying and listing on Ganor, written to be read.",
     "ticket", [], "ganor.ng/terms"),
    ("og-privacy.png", "Legal", "Privacy<br>policy.",
     "What we collect, why, and your rights under the Nigeria Data Protection Act 2023.",
     "find", [], "ganor.ng/privacy"),
    ("og-refunds.png", "Legal", "Refund<br>policy.",
     "Ask the host first. If an event is cancelled, you get your money back.",
     "pay", [], "ganor.ng/refunds"),
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
.ph{position:absolute;right:96px;top:62px;width:330px;transform:rotate(-5deg);transform-origin:50% 0;filter:drop-shadow(0 40px 60px rgba(21,19,42,.45))}
.ph img{display:block;width:100%;height:auto}
.in{max-width:850px}
.foot{flex-wrap:nowrap!important}
p.s{max-width:600px}
"""


def card_html(kicker, title, sub, screen, chips, url):
    chips_html = "".join(f'<span class="chip">{icon(i)}{t}</span>' for i, t in chips)
    art = f'<div class="ph"><img src="_phones/{screen}.png" alt=""></div>'
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


SET_SCREEN = """(i) => {
  const live = document.querySelector('[data-live]');
  live.querySelectorAll('.scr').forEach((s, k) => { s.classList.toggle('is-on', k === i); s.classList.remove('is-out'); });
  const t = live.querySelector('[data-type]'); t.textContent = t.dataset.type;
  const caret = live.querySelector('.app__caret'); if (caret) caret.style.display = 'none';
  if (i === 1) {
    const set = (q, v) => { live.querySelector(q).textContent = v; };
    set('[data-qty]', '2'); set('[data-co-sub]', '₦10,000'); set('[data-co-fee]', '₦700');
    set('[data-co-total]', '₦10,700'); set('[data-co-label]', 'Pay ₦10,700');
  }
  if (i === 2) live.querySelector('.scr--tk').classList.add('is-admitted');
}"""
FREEZE = """*{animation:none!important;transition:none!important}
[data-rise]{opacity:1!important;transform:none!important} .phone{box-shadow:none!important} [data-tag]{display:none!important}
html,body,.hero,.hero *:not(.phone):not(.phone *){background:transparent!important}
.hero::before,.hero::after,.hero__visual::before,.hero__visual::after{display:none!important}"""


def shoot_phones(b, folder):
    """Screenshot the hero phone on index.html in each of its three screens (transparent PNGs)."""
    folder.mkdir(exist_ok=True)
    ctx = b.new_context(viewport={"width": 1280, "height": 1000}, device_scale_factor=2, reduced_motion="reduce")
    ctx.add_init_script("try{localStorage.setItem('ganor-intro','1')}catch(e){}")
    pg = ctx.new_page()
    pg.goto((ROOT / "index.html").as_uri())
    pg.wait_for_timeout(1500)
    pg.add_style_tag(content=FREEZE)
    pg.evaluate("() => document.querySelectorAll('[data-live-pause]').forEach(b => b.click())")
    for i, name in enumerate(("find", "pay", "ticket")):
        pg.evaluate(SET_SCREEN, i)
        pg.wait_for_timeout(300)
        pg.locator(".hero .phone").screenshot(path=str(folder / f"{name}.png"), omit_background=True)
    ctx.close()


def main():
    import shutil
    tmp = ROOT / "tools" / "_og.html"
    phones = ROOT / "tools" / "_phones"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        shoot_phones(b, phones)
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
    shutil.rmtree(phones)


if __name__ == "__main__":
    main()
