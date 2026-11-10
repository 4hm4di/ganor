"""Search and social-preview data for every page, in one place.

build.py replaces {{seo:slug}} in a page's <head> with the full block:
title, description, canonical, Open Graph, Twitter/X card and JSON-LD.
Share images are made by tools/og.py (assets/img/og-*.png).
"""
import html
import json
import re

SITE = "https://ganor.ng"
NAME = "Ganor"
LOCALE = "en_NG"
X_HANDLE = "@ganorng"
UPDATED = "2026-11-10"

SOCIAL = [
    "https://www.instagram.com/ganor.ng",
    "https://www.tiktok.com/@ganor.ng",
    "https://x.com/ganorng",
    "https://www.facebook.com/ganor.ng",
    "https://www.youtube.com/@ganor.ng",
]

# slug: (path, share title, description, share image, image alt, breadcrumb name)
# Browser-tab titles are kept short so they show in full on a tab
TAB = {"index": "Ganor · Your city, found.", "docs": "Docs · Ganor", "terms": "Terms · Ganor",
       "privacy": "Privacy · Ganor", "refunds": "Refunds · Ganor", "credits": "Credits · Ganor"}
PAGES = {
    "index": (
        "/",
        "Ganor · Events, tickets and trusted places near you",
        "Find events and trusted places near you. Hosts create an event, share one link, "
        "sell tickets and scan guests in at the gate. Free events cost nothing.",
        "og.png",
        "Ganor: your city, found. Events, tickets and places near you.",
        "Home",
    ),
    "docs": (
        "/docs.html",
        "Docs · How Ganor works",
        "How to host an event on Ganor, sell tickets and free RSVPs, share one link, "
        "check guests in at the gate, and get your business on Ganor Places.",
        "og-docs.png",
        "Ganor docs: how Ganor works for hosts, guests and businesses.",
        "Docs",
    ),
    "terms": (
        "/terms.html",
        "Terms of use · Ganor",
        "The terms for using Ganor as a host, a guest or a business, written to be read.",
        "og-terms.png",
        "Ganor terms of use.",
        "Terms of use",
    ),
    "privacy": (
        "/privacy.html",
        "Privacy policy · Ganor",
        "What personal data Ganor collects, why, who it is shared with, and your rights "
        "under the Nigeria Data Protection Act 2023.",
        "og-privacy.png",
        "Ganor privacy policy.",
        "Privacy policy",
    ),
    "refunds": (
        "/refunds.html",
        "Refund policy · Ganor",
        "How refunds work on Ganor: ask the host first, what happens when an event is "
        "cancelled, and when Ganor steps in.",
        "og-refunds.png",
        "Ganor refund policy.",
        "Refund policy",
    ),
    "credits": (
        "/credits.html",
        "Credits and licences · Ganor",
        "Credits and licences for the icons, typefaces and logos used on ganor.ng.",
        "og-credits.png",
        "Ganor credits and licences.",
        "Credits",
    ),
}

ORG = {
    "@type": "Organization",
    "@id": f"{SITE}/#org",
    "name": NAME,
    "url": f"{SITE}/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/android-chrome-512x512.png", "width": 512, "height": 512},
    "slogan": "Your city, found.",
    "email": "support@ganor.ng",
    "telephone": "+2348103301999",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "No. 15 Guda Abdullahi Road, Farm Center",
        "addressLocality": "Kano",
        "addressRegion": "Kano",
        "addressCountry": "NG",
    },
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": "support@ganor.ng",
        "telephone": "+2348103301999",
        "areaServed": "NG",
        "availableLanguage": ["English", "Hausa"],
    }],
    "sameAs": SOCIAL,
}


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def faq_from(page_html: str) -> list:
    """Questions and answers straight from the FAQ accordion, so schema and page never drift."""
    qs = re.findall(r'<span class="acc__q">(.*?)</span>', page_html)
    answers = re.findall(r'<div class="acc__panel"[^>]*><div>(.*?)</div></div>', page_html, flags=re.S)
    return [
        {"@type": "Question", "name": _text(q), "acceptedAnswer": {"@type": "Answer", "text": _text(a)}}
        for q, a in zip(qs, answers)
    ]


def jsonld(slug: str, page_html: str) -> str:
    path, title, desc, img, alt, crumb = PAGES[slug]
    url = SITE + path
    website = {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": NAME,
        "inLanguage": "en-NG",
        "publisher": {"@id": f"{SITE}/#org"},
    }
    webpage = {
        "@type": "WebPage",
        "@id": f"{url}#page",
        "url": url,
        "name": title,
        "description": desc,
        "inLanguage": "en-NG",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/assets/img/{img}", "width": 1200, "height": 630},
        "dateModified": UPDATED,
    }
    graph = [ORG, website, webpage]
    if slug == "index":
        faq = faq_from(page_html)
        if faq:
            graph.append({"@type": "FAQPage", "@id": f"{SITE}/#faq", "mainEntity": faq})
    else:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Ganor", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": crumb, "item": url},
            ],
        })
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{data}</script>'


def head(slug: str, page_html: str) -> str:
    path, title, desc, img, alt, _ = PAGES[slug]
    url = SITE + path
    image = f"{SITE}/assets/img/{img}"
    e = lambda s: html.escape(s, quote=True)
    return "\n".join([
        f"<title>{e(TAB[slug])}</title>",
        f'<meta name="description" content="{e(desc)}">',
        f'<link rel="canonical" href="{url}">',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        f'<meta name="application-name" content="{NAME}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{NAME}">',
        f'<meta property="og:locale" content="{LOCALE}">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{image}">',
        f'<meta property="og:image:secure_url" content="{image}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{e(alt)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:site" content="{X_HANDLE}">',
        f'<meta name="twitter:title" content="{e(title)}">',
        f'<meta name="twitter:description" content="{e(desc)}">',
        f'<meta name="twitter:image" content="{image}">',
        f'<meta name="twitter:image:alt" content="{e(alt)}">',
        jsonld(slug, page_html),
    ])


def sitemap() -> str:
    pri = {"index": "1.0", "docs": "0.8"}
    rows = []
    for slug, (path, *_rest) in PAGES.items():
        img = PAGES[slug][3]
        rows.append(
            f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{UPDATED}</lastmod>\n"
            f"    <priority>{pri.get(slug, '0.3')}</priority>\n"
            f"    <image:image><image:loc>{SITE}/assets/img/{img}</image:loc></image:image>\n  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(rows) + "\n</urlset>\n"
    )
