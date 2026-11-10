#!/usr/bin/env python3
"""Build the Ganor site.

Reads src/*.html, expands the placeholders below, and writes the result to the
repo root. Run from anywhere:  python3 tools/build.py

Placeholders
  {{sprite}}                     inline icon sprite (assets/icons/sprite.svg)
  {{icon:name}}                  <svg><use href="#i-name"></svg> from the sprite
  {{icon:name|class}}            same, with extra classes
  {{svg:path/to/file.svg|class}} inline an SVG file (currentColor logos etc.)
  {{qr:text}}                    QR code as inline SVG, black on white, quiet zone
  {{include:partial.html}}       insert src/partials/partial.html
  {{seo:slug}}                   title, description, canonical, social cards, JSON-LD (tools/seo.py)
"""
import pathlib
import re

import qrcode
import qrcode.image.svg

import seo

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def inline_svg(path: str, cls: str = "") -> str:
    text = (ROOT / path).read_text()
    text = re.sub(r"<\?xml[^>]*>", "", text).strip()
    text = re.sub(r"<title>.*?</title>", "", text, flags=re.S)
    attrs = ' aria-hidden="true" focusable="false"'
    if cls:
        attrs += f' class="{cls}"'
    # drop fixed width/height so CSS controls the size
    text = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r"\1", text, count=2)
    return text.replace("<svg", "<svg" + attrs, 1)


def icon(name: str, cls: str = "") -> str:
    c = ("i " + cls).strip()
    return f'<svg class="{c}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def qr_svg(data: str) -> str:
    qr = qrcode.QRCode(border=4, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    rects = []
    for y, row in enumerate(m):
        x = 0
        while x < n:
            if row[x]:
                start = x
                while x < n and row[x]:
                    x += 1
                rects.append(f"M{start} {y}h{x - start}v1h-{x - start}z")
            else:
                x += 1
    return (
        f'<svg class="qr" viewBox="0 0 {n} {n}" role="img" aria-label="QR code" shape-rendering="crispEdges">'
        f'<rect width="{n}" height="{n}" fill="#fff"/><path fill="#000" d="{"".join(rects)}"/></svg>'
    )


def pattern_tile() -> None:
    """Symbol pattern for Indigo grounds: a regular grid, every other row pointing south."""
    src = (ROOT / "assets/brand/ganor-symbol-small-currentcolor.svg").read_text()
    d = re.search(r'\sd="([^"]+)"', src).group(1)
    s = 0.4  # 120 -> 48 px
    tile = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="96" height="192" viewBox="0 0 96 192">'
        f'<g fill="#433CC9" fill-rule="evenodd">'
        f'<path transform="translate(24 24) scale({s})" d="{d}"/>'
        f'<path transform="translate(72 168) rotate(180) scale({s})" d="{d}"/>'
        "</g></svg>"
    )
    (ROOT / "assets/img/pattern-indigo.svg").write_text(tile)


def expand(text: str) -> str:
    def repl(m: re.Match) -> str:
        kind, arg = m.group(1), m.group(2)
        parts = arg.split("|", 1)
        main, extra = parts[0], (parts[1] if len(parts) > 1 else "")
        if kind == "icon":
            return icon(main, extra)
        if kind == "svg":
            return inline_svg(main, extra)
        if kind == "qr":
            return qr_svg(main)
        if kind == "include":
            return expand((SRC / "partials" / main).read_text())
        raise ValueError(kind)

    text = text.replace("{{sprite}}", (ROOT / "assets/icons/sprite.svg").read_text())
    return re.sub(r"\{\{(icon|svg|qr|include):([^}]+)\}\}", repl, text)


def main() -> None:
    pattern_tile()
    for page in sorted(SRC.glob("*.html")):
        out = ROOT / page.name
        built = expand(page.read_text())
        built = re.sub(r"\{\{seo:([a-z0-9-]+)\}\}", lambda m: seo.head(m.group(1), built), built)
        out.write_text(built)
        print("built", out.relative_to(ROOT))
    (ROOT / "sitemap.xml").write_text(seo.sitemap())
    print("built sitemap.xml")


if __name__ == "__main__":
    main()
