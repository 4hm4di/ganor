"""Render the PNG images used in emails (email apps don't show SVG) into assets/email/.
Run: CHROME=/path/to/chrome python3 tools/email_assets.py
"""
import os, pathlib, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/email"
SPRITE = (ROOT / "assets/icons/sprite.svg").read_text()
LOCK = (ROOT / "assets/brand/ganor-lockup-currentcolor.svg").read_text()
SYMBOL = (ROOT / "assets/brand/ganor-symbol-currentcolor.svg").read_text()
SOCIAL = {n: (ROOT / f"assets/social/{n}.svg").read_text() for n in ["instagram", "tiktok", "x", "facebook", "linkedin", "whatsapp"]}

INDIGO, INK, WHITE = "#3730B8", "#15132A", "#FFFFFF"

def page(body, w, h):
    return f"""<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}
    .b{{width:{w}px;height:{h}px;display:grid;place-items:center}} svg{{display:block}}</style></head>
    <body>{SPRITE}<div class="b">{body}</div></body></html>"""

def sized(svg, h, color):
    svg = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r"\1", svg, count=2)
    return svg.replace("<svg", f'<svg style="height:{h}px;width:auto;color:{color}"', 1)

JOBS = []
# lockups at 3x of 32px display height
for name, color in [("logo-white", WHITE), ("logo-indigo", INDIGO)]:
    JOBS.append((f"{name}.png", page(sized(LOCK, 96, color), 900, 120), 900, 120))
for name, color in [("symbol-indigo", INDIGO), ("symbol-white", WHITE)]:
    JOBS.append((f"{name}.png", page(sized(SYMBOL, 120, color), 128, 128), 128, 128))
# social icons, 3x of 20px, ink and white
for n, svg in SOCIAL.items():
    for tone, color in [("ink", INK), ("white", WHITE)]:
        s = svg.replace("<svg", f'<svg style="width:60px;height:60px;color:{color}" stroke-width="1.6"', 1)
        JOBS.append((f"social-{n}-{tone}.png", page(s, 60, 60), 60, 60))
# UI icons, 3x of 20px, indigo
for n in ["calendar", "clock", "location", "ticket", "user", "support", "whatsapp", "wallet",
          "search", "shop", "scan", "check-circle", "share", "doc", "chat", "percent"]:
    JOBS.append((f"i-{n}.png", page(f'<svg style="width:60px;height:60px;color:{INDIGO}"><use href="#i-{n}"/></svg>', 60, 60), 60, 60))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
    pg = b.new_page(device_scale_factor=1)
    for name, html, w, h in JOBS:
        pg.set_viewport_size({"width": w, "height": h})
        pg.set_content(html)
        pg.screenshot(path=str(OUT / name), omit_background=True, clip={"x": 0, "y": 0, "width": w, "height": h})
    b.close()
# trim the transparent edges off the logos so they size exactly
from PIL import Image
for f in ["logo-white.png", "logo-indigo.png", "symbol-indigo.png", "symbol-white.png"]:
    im = Image.open(OUT / f)
    im.crop(im.getbbox()).save(OUT / f)
print(len(JOBS), "images")
