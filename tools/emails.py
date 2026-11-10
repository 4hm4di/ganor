"""Build Ganor's email templates into emails/ (and sample previews into emails/preview/).

Email apps ignore most modern CSS, so these are table layouts with inline styles,
600px wide, stacking on phones. Images are PNGs hosted at https://ganor.ng/assets/email/.

Merge tags look like {{first_name}}. Swap them for your sending tool's syntax
(see emails/README.md). Run:  python3 tools/emails.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "emails"
PREVIEW = OUT / "preview"
SITE = "https://ganor.ng"
IMG = f"{SITE}/assets/email"

INDIGO, INK, SAND, LAV, MUTED, LINE, MARI, OK = "#3730B8", "#15132A", "#F6F1E7", "#C9C3E8", "#55526B", "#E3DDD0", "#FFB21E", "#1C7A45"
SANS = "Inter,'Helvetica Neue',Helvetica,Arial,sans-serif"
HEAD = "'Bricolage Grotesque',Inter,'Helvetica Neue',Helvetica,Arial,sans-serif"

# ---------- building blocks ----------

def shell(title, preheader, header, body, footer):
    pad = "&#847;&zwnj;&nbsp;" * 40
    return f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>{title}</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<style>
@font-face {{ font-family: 'Bricolage Grotesque'; font-weight: 200 800; src: url({SITE}/assets/fonts/bricolage-grotesque-latin.woff2) format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 100 900; src: url({SITE}/assets/fonts/inter-latin.woff2) format('woff2'); }}
body {{ margin: 0; padding: 0; width: 100% !important; background: {SAND}; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
table {{ border-collapse: collapse; mso-table-lspace: 0; mso-table-rspace: 0; }}
img {{ border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; display: block; }}
a {{ color: {INDIGO}; }}
u + #body a, #MessageViewBody a {{ color: inherit; text-decoration: none; }}
@media (max-width: 620px) {{
  .w {{ width: 100% !important; }}
  .px {{ padding-left: 22px !important; padding-right: 22px !important; }}
  .stack {{ display: block !important; width: 100% !important; box-sizing: border-box; }}
  .stack-gap {{ padding-top: 16px !important; padding-left: 0 !important; }}
  .h1 {{ font-size: 30px !important; line-height: 34px !important; }}
  .hero-h {{ font-size: 40px !important; line-height: 42px !important; }}
  .full {{ width: 100% !important; }}
  .center-sm {{ text-align: center !important; }}
  .left-sm {{ text-align: left !important; }}
}}
</style>
</head>
<body id="body" style="margin:0;padding:0;background:{SAND};">
<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">{preheader}{pad}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{SAND}" style="background:{SAND};">
<tr><td align="center" style="padding:28px 12px 36px;">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
<table role="presentation" class="w" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">
{header}
<tr><td class="px" bgcolor="#FFFFFF" style="background:#FFFFFF;padding:40px 44px 44px;border-radius:0 0 22px 22px;font-family:{SANS};font-size:16px;line-height:26px;color:{INK};">
{body}
</td></tr>
{footer}
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr>
</table>
</body>
</html>
"""


def header_bar():
    return f"""<tr><td class="px" bgcolor="{INDIGO}" style="background:{INDIGO};padding:26px 44px;border-radius:22px 22px 0 0;">
  <a href="{SITE}" style="text-decoration:none;"><img src="{IMG}/logo-white.png" width="140" height="26" alt="Ganor" style="width:140px;height:26px;"></a>
</td></tr>"""


def header_hero(kicker, title, text, cta, href):
    return f"""<tr><td class="px" bgcolor="{INDIGO}" style="background:{INDIGO};padding:30px 44px 46px;border-radius:22px 22px 0 0;">
  <a href="{SITE}" style="text-decoration:none;"><img src="{IMG}/logo-white.png" width="140" height="26" alt="Ganor" style="width:140px;height:26px;"></a>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:40px;"><tr>
    <td bgcolor="{MARI}" style="background:{MARI};border-radius:999px;padding:6px 14px;font-family:{SANS};font-size:12px;line-height:16px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{INK};">{kicker}</td>
  </tr></table>
  <h1 class="hero-h" style="margin:18px 0 0;font-family:{HEAD};font-size:52px;line-height:52px;font-weight:800;color:#FFFFFF;">{title}</h1>
  <p style="margin:16px 0 0;font-family:{SANS};font-size:17px;line-height:27px;color:#E9E6F7;">{text}</p>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:26px;"><tr>
    <td bgcolor="#FFFFFF" style="background:#FFFFFF;border-radius:999px;"><a href="{href}" style="display:inline-block;padding:15px 28px;font-family:{SANS};font-size:15px;line-height:20px;font-weight:700;color:{INDIGO};text-decoration:none;border-radius:999px;">{cta} &rarr;</a></td>
  </tr></table>
</td></tr>"""


def footer(marketing=False):
    icons = "".join(
        f'<td style="padding:0 7px;"><a href="{url}" style="text-decoration:none;"><img src="{IMG}/social-{n}-ink.png" width="20" height="20" alt="{label}" style="width:20px;height:20px;"></a></td>'
        for n, label, url in [
            ("instagram", "Instagram", "https://www.instagram.com/ganor.ng"),
            ("tiktok", "TikTok", "https://www.tiktok.com/@ganor.ng"),
            ("x", "X", "https://x.com/ganorng"),
            ("facebook", "Facebook", "https://www.facebook.com/ganor.ng"),
            ("youtube", "YouTube", "https://www.youtube.com/@ganor.ng"),
            ("whatsapp", "WhatsApp", "https://wa.me/2348103301999"),
        ]
    )
    why = (
        f'You’re getting this because you joined the Ganor list at ganor.ng.<br>'
        f'<a href="{{{{unsubscribe_url}}}}" style="color:{MUTED};text-decoration:underline;">Unsubscribe</a> &nbsp;·&nbsp; '
        f'<a href="{{{{preferences_url}}}}" style="color:{MUTED};text-decoration:underline;">Email preferences</a><br><br>'
        if marketing else ""
    )
    return f"""<tr><td align="center" style="padding:30px 20px 0;font-family:{SANS};font-size:12px;line-height:19px;color:{MUTED};">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>{icons}</tr></table>
  <p style="margin:18px 0 0;">{why}Ganor · No. 15 Guda Abdullahi Road, Farm Center, Kano<br>
  <a href="mailto:support@ganor.ng" style="color:{MUTED};">support@ganor.ng</a> &nbsp;·&nbsp; <a href="tel:+2348103301999" style="color:{MUTED};text-decoration:none;">0810 330 1999</a><br>
  <a href="{SITE}/terms.html" style="color:{MUTED};">Terms</a> &nbsp;·&nbsp; <a href="{SITE}/privacy.html" style="color:{MUTED};">Privacy</a> &nbsp;·&nbsp; <a href="{SITE}/refunds.html" style="color:{MUTED};">Refunds</a></p>
</td></tr>"""


def button(label, href, fill=INDIGO, text="#FFFFFF", outline=False):
    if outline:
        return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;"><tr>
  <td style="border-radius:999px;border:1.5px solid {INK};"><a href="{href}" style="display:inline-block;padding:13px 24px;font-family:{SANS};font-size:15px;line-height:20px;font-weight:700;color:{INK};text-decoration:none;border-radius:999px;">{label}</a></td>
</tr></table>"""
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
  <td bgcolor="{fill}" style="background:{fill};border-radius:999px;"><a href="{href}" style="display:inline-block;padding:15px 26px;font-family:{SANS};font-size:15px;line-height:20px;font-weight:700;color:{text};text-decoration:none;border-radius:999px;">{label} &rarr;</a></td>
</tr></table>"""


def kicker(text, color=MUTED, icon=None):
    ic = f'<td valign="middle" style="padding-right:8px;"><img src="{IMG}/i-{icon}.png" width="18" height="18" alt="" style="width:18px;height:18px;"></td>' if icon else ""
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>{ic}
  <td valign="middle" style="font-family:{SANS};font-size:12px;line-height:16px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:{color};">{text}</td>
</tr></table>"""


def h1(text):
    return f'<h1 class="h1" style="margin:12px 0 0;font-family:{HEAD};font-size:36px;line-height:40px;font-weight:800;color:{INK};">{text}</h1>'


def p(text, top=16, size=16, color=INK):
    return f'<p style="margin:{top}px 0 0;font-family:{SANS};font-size:{size}px;line-height:{int(size*1.62)}px;color:{color};">{text}</p>'


def icon_row(icon, html, top=14):
    return f"""<tr><td valign="top" width="30" style="padding-top:{top}px;"><img src="{IMG}/i-{icon}.png" width="20" height="20" alt="" style="width:20px;height:20px;"></td>
<td valign="top" style="padding-top:{top}px;font-family:{SANS};font-size:15px;line-height:22px;color:{INK};">{html}</td></tr>"""


def panel(inner, bg=SAND, pad="22px 24px", top=28):
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:{top}px;"><tr>
<td bgcolor="{bg}" style="background:{bg};border-radius:16px;padding:{pad};">{inner}</td></tr></table>"""


def text_version(s):
    return s.strip() + "\n"


# ---------- 1. Auto-reply ----------

def auto_reply():
    body = (
        kicker("Ganor support", icon="support")
        + h1("We’ve got your message.")
        + p("Hi there, thanks for writing to Ganor. A real person reads every message, and we’ll get back to you as soon as we can, usually within one working day.")
        + panel(
            f"""<p style="margin:0;font-family:{SANS};font-size:13px;line-height:18px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{MUTED};">While you wait</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{icon_row("ticket", "<b>Ticket didn’t arrive?</b> Reply with the event name and the WhatsApp number or email you used to pay.")}
{icon_row("support", "<b>Question about an event?</b> The host can help fastest. Their contact is on the event page.")}
{icon_row("doc", f'<b>Hosting?</b> Our <a href="{SITE}/docs.html" style="color:{INDIGO};font-weight:600;">docs</a> cover creating events, fees and gate check-in.')}
</table>"""
        )
        + f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:28px;"><tr><td>{button("Read the docs", SITE + "/docs.html")}</td></tr></table>'
        + p(f'Need us now? <a href="https://wa.me/2348103301999" style="color:{INDIGO};font-weight:600;">WhatsApp 0810 330 1999</a>.', top=18, size=15, color=MUTED)
        + p("The Ganor team", top=28, size=15)
    )
    html = shell("We’ve got your message", "Thanks for writing to Ganor. Here’s what happens next.", header_bar(), body, footer())
    txt = f"""We've got your message.

Hi there, thanks for writing to Ganor. A real person reads every message, and we'll get back to you as soon as we can, usually within one working day.

While you wait:
- Ticket didn't arrive? Reply with the event name and the WhatsApp number or email you used to pay.
- Question about an event? The host can help fastest. Their contact is on the event page.
- Hosting? Our docs cover creating events, fees and gate check-in: {SITE}/docs.html

Need us now? WhatsApp 0810 330 1999.

The Ganor team
support@ganor.ng · ganor.ng"""
    return html, txt


# ---------- 2. Everyday email (layout + signature) ----------

def signature(name, role):
    social = "".join(
        f'<td style="padding-right:10px;"><a href="{url}" style="text-decoration:none;"><img src="{IMG}/social-{n}-ink.png" width="16" height="16" alt="{label}" style="width:16px;height:16px;display:block;border:0;"></a></td>'
        for n, label, url in [("instagram", "Instagram", "https://www.instagram.com/ganor.ng"), ("tiktok", "TikTok", "https://www.tiktok.com/@ganor.ng"),
                              ("x", "X", "https://x.com/ganorng"), ("facebook", "Facebook", "https://www.facebook.com/ganor.ng"),
                              ("whatsapp", "WhatsApp", "https://wa.me/2348103301999")]
    )
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="font-family:{SANS};color:{INK};">
<tr>
  <td valign="top" style="padding:2px 14px 0 0;border-right:2px solid {INDIGO};"><a href="{SITE}" style="text-decoration:none;"><img src="{IMG}/symbol-indigo.png" width="40" height="40" alt="Ganor" style="width:40px;height:40px;display:block;border:0;"></a></td>
  <td valign="top" style="padding-left:14px;">
    <p style="margin:0;font-family:{HEAD};font-size:16px;line-height:20px;font-weight:800;color:{INK};">{name}</p>
    <p style="margin:2px 0 0;font-size:13px;line-height:18px;color:{MUTED};">{role}</p>
    <p style="margin:8px 0 0;font-size:13px;line-height:19px;color:{INK};">
      <a href="tel:+2348103301999" style="color:{INK};text-decoration:none;">0810 330 1999</a> &nbsp;·&nbsp;
      <a href="mailto:support@ganor.ng" style="color:{INDIGO};text-decoration:none;">support@ganor.ng</a> &nbsp;·&nbsp;
      <a href="{SITE}" style="color:{INDIGO};text-decoration:none;font-weight:600;">ganor.ng</a></p>
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:8px;"><tr>{social}</tr></table>
  </td>
</tr></table>"""


def general():
    body = (
        p("Hi {{first_name}},", top=0)
        + p("Write your message here. Keep it short and plain: one idea per paragraph, and say what you need from the reader in the first two lines.")
        + p("Use a second paragraph for the details. If there’s one thing to click, add a single button below; otherwise leave it out.")
        + f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:24px;"><tr><td>{button("{{button_label}}", "{{button_url}}")}</td></tr></table>'
        + p("Thanks,", top=28)
        + f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px;"><tr><td>{signature("{{sender_name}}", "{{sender_role}} · Ganor")}</td></tr></table>'
    )
    return shell("{{subject}}", "{{preheader}}", header_bar(), body, footer())


def signatures_page():
    sigs = [signature("Ganor Support", "We usually reply within one working day"), signature("Ahmad Abdallah", "Ganor")]
    blocks = "".join(f'<div style="margin:0 0 36px;padding:24px;background:#fff;border-radius:16px;">{s}</div>' for s in sigs)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Ganor email signatures</title></head>
<body style="margin:0;padding:32px;background:{SAND};font-family:{SANS};color:{INK};">
<p style="margin:0 0 20px;font-size:14px;color:{MUTED};">To use one: open this file in a browser, select everything inside the white box, copy, and paste into your mail app’s signature settings.</p>
{blocks}
</body></html>"""


# ---------- 3. Ticket purchase ----------

def ticket():
    rows = "".join([
        icon_row("calendar", "<b>{{event_date}}</b>", top=12),
        icon_row("clock", "{{event_time}} &nbsp;·&nbsp; Gate opens {{gate_time}}", top=10),
        icon_row("location", '{{venue_name}}<br><span style="color:' + MUTED + ';">{{venue_address}}</span> &nbsp;<a href="{{map_url}}" style="color:' + INDIGO + ';font-weight:600;white-space:nowrap;">Get directions</a>', top=10),
        icon_row("ticket", "{{ticket_type}} × {{ticket_qty}}", top=10),
        icon_row("user", "{{holder_name}}", top=10),
    ])
    event_card = f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:28px;border:1px solid {LINE};border-radius:18px;border-collapse:separate;">
<tr><td bgcolor="{INDIGO}" style="background:{INDIGO};border-radius:18px 18px 0 0;line-height:0;font-size:0;">
  <img src="{{{{event_banner_url}}}}" width="510" alt="{{{{event_name}}}}" class="full" style="width:100%;max-width:510px;height:auto;border-radius:18px 18px 0 0;">
</td></tr>
<tr><td style="padding:20px 22px 22px;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
    <td valign="middle" style="padding-right:10px;"><img src="{{{{host_logo_url}}}}" width="36" height="36" alt="" style="width:36px;height:36px;border-radius:10px;"></td>
    <td valign="middle" style="font-family:{SANS};font-size:13px;line-height:18px;color:{MUTED};">Hosted by <b style="color:{INK};">{{{{host_name}}}}</b></td>
  </tr></table>
  <h2 style="margin:14px 0 0;font-family:{HEAD};font-size:26px;line-height:30px;font-weight:800;color:{INK};">{{{{event_name}}}}</h2>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:4px;">{rows}</table>
</td></tr></table>"""
    qr = panel(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="#FFFFFF" style="background:#FFFFFF;border-radius:16px;padding:16px;">
    <img src="{{{{qr_image_url}}}}" width="184" height="184" alt="Ticket QR code {{{{ticket_code}}}}" style="width:184px;height:184px;">
  </td></tr></table>
  <p style="margin:14px 0 0;font-family:'SFMono-Regular',Menlo,Consolas,monospace;font-size:15px;line-height:20px;font-weight:700;letter-spacing:1px;color:{INK};">{{{{ticket_code}}}}</p>
  <p style="margin:6px 0 0;font-family:{SANS};font-size:14px;line-height:21px;color:{MUTED};">Show this at the gate. Each code works once, so keep it to yourself.</p>
</td></tr></table>""", pad="26px 20px")
    buttons = f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:26px;"><tr>
<td class="stack" style="padding-right:10px;">{button("Add to calendar", "{{calendar_url}}")}</td>
<td class="stack stack-gap">{button("View ticket", "{{ticket_url}}", outline=True)}</td>
</tr></table>"""
    receipt_rows = "".join(
        f'<tr><td style="padding:9px 0;border-bottom:1px solid {LINE};font-family:{SANS};font-size:15px;line-height:20px;color:{MUTED};">{k}</td>'
        f'<td align="right" style="padding:9px 0;border-bottom:1px solid {LINE};font-family:{SANS};font-size:15px;line-height:20px;color:{INK};font-weight:600;">{v}</td></tr>'
        for k, v in [("Tickets", "{{subtotal}}"), ("Ganor fee", "{{fee}}")]
    )
    receipt = f"""<h3 style="margin:34px 0 0;font-family:{HEAD};font-size:20px;line-height:26px;font-weight:800;color:{INK};">Receipt</h3>
<p style="margin:4px 0 0;font-family:{SANS};font-size:13px;line-height:18px;color:{MUTED};">Order {{{{order_id}}}} · {{{{paid_at}}}}</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:10px;">
{receipt_rows}
<tr><td style="padding:12px 0 0;font-family:{SANS};font-size:16px;line-height:22px;color:{INK};font-weight:700;">Total paid</td>
<td align="right" style="padding:12px 0 0;font-family:{HEAD};font-size:20px;line-height:24px;color:{INK};font-weight:800;">{{{{total}}}}</td></tr>
<tr><td colspan="2" style="padding-top:4px;font-family:{SANS};font-size:13px;line-height:18px;color:{MUTED};">Paid by {{{{payment_method}}}}</td></tr>
</table>"""
    host = panel(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{icon_row("support", '<b>Questions about the event?</b> Contact the host, {{host_name}}:<br><a href="tel:{{host_phone}}" style="color:' + INDIGO + ';font-weight:600;">{{host_phone}}</a> &nbsp;·&nbsp; <a href="mailto:{{host_email}}" style="color:' + INDIGO + ';font-weight:600;">{{host_email}}</a><br><span style="color:' + MUTED + ';">Changes and refunds are up to the host. See our <a href="' + SITE + '/refunds.html" style="color:' + MUTED + ';">refund policy</a>.</span>', top=0)}
</table>""", top=30)
    body = (
        kicker("Ticket confirmed", color=OK, icon="check-circle")
        + h1("You’re going, {{first_name}}!")
        + p("Here’s your ticket for <b>{{event_name}}</b>. We’ve sent it to your WhatsApp too.")
        + event_card + qr + buttons + receipt + host
        + p(f'Didn’t buy this? Reply to this email or write to <a href="mailto:support@ganor.ng" style="color:{INDIGO};">support@ganor.ng</a> and we’ll look into it.', top=26, size=14, color=MUTED)
    )
    html = shell("Your ticket for {{event_name}}", "{{event_date}} · {{venue_name}}. Show the QR code at the gate.", header_bar(), body, footer())
    txt = """You're going, {{first_name}}!

Your ticket for {{event_name}} is confirmed. We've sent it to your WhatsApp too.

Date: {{event_date}}
Time: {{event_time}} (gate opens {{gate_time}})
Venue: {{venue_name}}, {{venue_address}}
Directions: {{map_url}}
Ticket: {{ticket_type}} x {{ticket_qty}}
Name: {{holder_name}}

Ticket code: {{ticket_code}}
View your ticket and QR code: {{ticket_url}}
Show it at the gate. Each code works once, so keep it to yourself.
Add to calendar: {{calendar_url}}

Receipt, order {{order_id}} ({{paid_at}})
Tickets: {{subtotal}}
Ganor fee: {{fee}}
Total paid: {{total}} by {{payment_method}}

Questions about the event? Contact the host, {{host_name}}: {{host_phone}} · {{host_email}}
Changes and refunds are up to the host: https://ganor.ng/refunds.html

Didn't buy this? Reply to this email or write to support@ganor.ng.

Ganor · ganor.ng"""
    return html, txt


# ---------- 4. Marketing newsletter ----------

def newsletter():
    def event(day, mon, title, meta, price, href="{{event_url}}"):
        return f"""<tr><td style="padding-top:12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:16px;border-collapse:separate;"><tr>
  <td width="64" valign="middle" style="padding:14px 0 14px 14px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" bgcolor="{SAND}" style="background:{SAND};border-radius:12px;width:50px;padding:8px 0;font-family:{SANS};">
      <span style="display:block;font-family:{HEAD};font-size:20px;line-height:22px;font-weight:800;color:{INK};">{day}</span>
      <span style="display:block;font-size:11px;line-height:14px;font-weight:700;text-transform:uppercase;color:{MUTED};">{mon}</span>
    </td></tr></table>
  </td>
  <td valign="middle" style="padding:14px 12px;font-family:{SANS};">
    <span style="display:block;font-size:16px;line-height:21px;font-weight:700;color:{INK};">{title}</span>
    <span style="display:block;margin-top:3px;font-size:13px;line-height:18px;color:{MUTED};">{meta}</span>
  </td>
  <td align="right" valign="middle" style="padding:14px 16px 14px 0;font-family:{SANS};white-space:nowrap;">
    <span style="display:block;font-size:14px;line-height:18px;font-weight:700;color:{INDIGO};">{price}</span>
    <a href="{href}" style="display:inline-block;margin-top:4px;font-size:13px;line-height:18px;font-weight:600;color:{INK};">Get tickets</a>
  </td>
</tr></table></td></tr>"""

    events = "".join([
        event("13", "Dec", "Northern Tech Summit", "Abuja · Sat 9:00 am", "₦5,000"),
        event("12", "Dec", "Annual Public Lecture", "Kano · Fri 4:00 pm", "Free"),
        event("20", "Dec", "Kano International Trade Fair", "Kano · Sat 10:00 am", "₦1,000"),
    ])
    chips = "".join(
        f'<td style="padding:0 8px 8px 0;"><span style="display:inline-block;padding:8px 14px;border-radius:999px;border:1px solid {LINE};font-family:{SANS};font-size:13px;line-height:18px;font-weight:600;color:{INK};white-space:nowrap;">{t}</span></td>'
        for t in ["Phones &amp; electronics", "Hospitals", "Places to eat", "Hotels", "Gyms"]
    )
    host = f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:36px;"><tr>
<td bgcolor="{INK}" style="background:{INK};border-radius:20px;padding:30px 28px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td class="stack" valign="top" style="font-family:{SANS};">
      <p style="margin:0;font-size:12px;line-height:16px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:{LAV};">For hosts</p>
      <h2 style="margin:10px 0 0;font-family:{HEAD};font-size:28px;line-height:32px;font-weight:800;color:#FFFFFF;">Hosting something?</h2>
      <p style="margin:10px 0 0;font-size:15px;line-height:24px;color:#E9E6F7;">One link to share, tickets on WhatsApp, every gate opens with a scan. Free events cost nothing; paid tickets are 5% + ₦100 each.</p>
    </td>
    <td class="stack stack-gap left-sm" valign="bottom" align="right" width="190" style="padding-left:16px;">{button("Host your event", SITE + "/#join", fill="#FFFFFF", text=INDIGO)}</td>
  </tr></table>
</td></tr></table>"""
    body = (
        kicker("This week near you", icon="calendar")
        + h1("Something to go to.")
        + p("Hi {{first_name}}, here are a few events coming up. Tap one to get your ticket in seconds.", top=12)
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:10px;">{events}</table>'
        + f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:20px;"><tr><td>{button("See all events", SITE + "/#find", outline=True)}</td></tr></table>'
        + host
        + f'<div style="margin-top:36px;">{kicker("Coming next", icon="shop")}</div>'
        + f'<h2 style="margin:10px 0 0;font-family:{HEAD};font-size:24px;line-height:30px;font-weight:800;color:{INK};">Ganor Places: who to trust nearby.</h2>'
        + p("Shops, hospitals, places to eat and stay, workspaces and more, checked in person.", top=8, size=15, color=MUTED)
        + f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;"><tr>{chips}</tr></table>'
        + p(f'Own a business? <a href="{SITE}/#join" style="color:{INDIGO};font-weight:600;">Get found first</a>.', top=10, size=15)
    )
    hero = header_hero("Ganor weekly", "Your city,<br>found.", "Find what’s happening near you, buy tickets in seconds, and get them on WhatsApp.", "See what’s on", SITE + "/#find")
    return shell("Ganor: what’s on near you", "Events this week, plus what’s coming to Ganor.", hero, body, footer(marketing=True))


# ---------- sample data for previews ----------

SAMPLE = {
    "first_name": "Fatima", "event_name": "Northern Tech Summit", "event_date": "Saturday, 13 December 2026",
    "event_time": "9:00 am", "gate_time": "8:30 am", "venue_name": "Abuja International Conference Centre",
    "venue_address": "Herbert Macaulay Way, Central Business District, Abuja", "map_url": "#", "ticket_type": "Regular",
    "ticket_qty": "2", "holder_name": "Fatima Jamil", "ticket_code": "GANOR-TKT-000123", "ticket_url": "#", "calendar_url": "#",
    "order_id": "GNR-48213", "paid_at": "10 Nov 2026, 3:42 pm", "subtotal": "₦10,000", "fee": "₦700", "total": "₦10,700",
    "payment_method": "bank transfer", "host_name": "Northern Tech Community", "host_phone": "0801 234 5678",
    "host_email": "hello@example.com", "event_banner_url": "sample-banner.png", "host_logo_url": "sample-host.png",
    "qr_image_url": "sample-qr.png", "unsubscribe_url": "#", "preferences_url": "#", "event_url": "#",
    "subject": "A note from Ganor", "preheader": "", "button_label": "Open Ganor", "button_url": SITE,
    "sender_name": "Ahmad Abdallah", "sender_role": "Team",
}


def fill(s):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: SAMPLE.get(m.group(1), m.group(0)), s)


def main():
    OUT.mkdir(exist_ok=True)
    PREVIEW.mkdir(exist_ok=True)
    files = {}
    html, txt = auto_reply(); files["auto-reply.html"] = html; files["auto-reply.txt"] = txt
    files["general.html"] = general()
    html, txt = ticket(); files["ticket-confirmation.html"] = html; files["ticket-confirmation.txt"] = txt
    files["newsletter.html"] = newsletter()
    files["signatures.html"] = signatures_page()
    for name, content in files.items():
        (OUT / name).write_text(content if name.endswith(".html") else text_version(content))
        if name.endswith(".html"):
            prev = fill(content).replace(f"{IMG}/", "../../assets/email/").replace(f"{SITE}/assets/fonts/", "../../assets/fonts/")
            (PREVIEW / name).write_text(prev)
    print("wrote", ", ".join(files))


if __name__ == "__main__":
    main()
