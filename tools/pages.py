"""Writes the inner pages (docs, legal, credits) into src/ from the content below.
Run: python3 tools/pages.py && python3 tools/build.py
"""
from pathlib import Path
SRC = Path(__file__).resolve().parent.parent / "src"
UPDATED = "10 November 2026"

def page(slug, title, desc, label, h1, lede, sections, meta=None, nav_title="On this page"):
    nav = "\n".join(f'        <li><a href="#{sid}">{name}</a></li>' for sid, name, _icon, _body in sections)
    body = []
    for sid, name, icon, html in sections:
        ic = f"{{{{icon:{icon}}}}}" if icon else ""
        body.append(f'    <section id="{sid}" aria-labelledby="{sid}-t">\n      <h2 id="{sid}-t">{ic}{name}</h2>\n{html.strip()}\n    </section>')
    meta_html = f'    <p class="meta">{meta}</p>\n' if meta else ""
    out = f"""<!DOCTYPE html>
<html lang="en-NG">
<head>
{{{{include:head.html}}}}
{{{{seo:{slug}}}}}
<script>document.documentElement.classList.add('js','no-intro')</script>
</head>
<body class="inner">
{{{{sprite}}}}
{{{{include:header.html}}}}
<main id="main">
<section class="page-hero" aria-labelledby="page-title">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="page-hero__inner wrap">
    <p class="label">{label}</p>
    <h1 id="page-title">{h1}</h1>
    <p>{lede}</p>
  </div>
</section>
<div class="doc wrap">
  <nav class="doc__nav" aria-label="{nav_title}">
    <p>{nav_title}</p>
    <ul>
{nav}
    </ul>
  </nav>
  <article class="prose">
{meta_html}{chr(10).join(body)}
  </article>
</div>
</main>
{{{{include:footer.html}}}}
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""
    (SRC / f"{slug}.html").write_text(out)

CONTACT = """<p>WhatsApp or call <a href="https://wa.me/2348103301999" rel="noopener">0810 330 1999</a>, email <a href="mailto:support@ganor.ng">support@ganor.ng</a>, or visit us at No. 15 Guda Abdullahi Road, Farm Center, Kano.</p>"""

# ---------------- DOCS ----------------
page("docs", "Docs", "How Ganor works for hosts, guests and businesses: creating events, tickets, fees, sharing, gate check-in and getting help.",
 "Docs", "How Ganor works", "Everything you need to host an event, buy a ticket or get your business found. Short answers, in plain words.",
 [
 ("start", "Getting started", "compass", """
      <p>Ganor is where you find what’s happening near you. Hosts create an event, share one link, sell tickets or take free RSVPs, and scan guests in at the gate. Guests find events, pay the way they already pay, and get their ticket on WhatsApp.</p>
      <div class="callout"><b>Ganor opens soon.</b> These docs describe how it works when it opens. <a href="./#join">Join the list</a> and we’ll message you on WhatsApp the day you can start.</div>
      <h3>Who Ganor is for</h3>
      <ul>
        <li><b>Hosts:</b> anyone running a gathering, from conferences, trade fairs and cooperative launches to lectures, campus events and shows.</li>
        <li><b>Guests:</b> anyone looking for something to go to, or holding a ticket.</li>
        <li><b>Businesses:</b> shops, hospitals, restaurants, hotels and more, listed on Ganor Places.</li>
      </ul>"""),
 ("create", "Create an event", "calendar", """
      <ol>
        <li>Give your event a name, a date and a start time.</li>
        <li>Add the venue. A full address and a map pin help guests find you.</li>
        <li>Add a banner for the top of your event page, and your logo or a photo of you as the host. Guests see them on the event page, in search and on their ticket.</li>
        <li>Add a few lines about what to expect.</li>
        <li>Add how guests can reach you. Guests contact the host about the event, so this is required.</li>
        <li>Add your ticket types (see below), then publish.</li>
      </ol>
      <p>You can save a draft and come back to it. After you publish, you can still change the details; guests who already have tickets get a WhatsApp message when the date, time or venue changes.</p>"""),
 ("tickets", "Tickets and RSVPs", "ticket", """
      <p>An event can have as many ticket types as you need, for example Regular, VIP and Table for 10. For each one you set:</p>
      <ul>
        <li>The price, or free.</li>
        <li>How many are available.</li>
        <li>When sales open and close.</li>
      </ul>
      <p>Free RSVPs work the same way as tickets: each guest gets a QR code on WhatsApp, and you scan it at the gate. You can turn any ticket type on or off at any time.</p>"""),
 ("share", "Share your event", "share", """
      <p>Every event gets one link, like <b>ganor.ng/e/your-event</b>. Post it on WhatsApp, your status, Instagram or anywhere else. The link shows a clean preview with your banner, date and venue.</p>
      <h3>Your host profile</h3>
      <p>Your logo or avatar, name and past events live on your host profile, so guests can follow you and find your next event.</p>
      <p>Guests who open the link can buy or RSVP straight away. They don’t need to download anything.</p>"""),
 ("fees", "Fees and payouts", "percent", """
      <p>Free events and free RSVPs cost nothing. On paid tickets, the Ganor fee is <b>5% of the ticket price + ₦100 per ticket</b>. Card and bank transfer charges are included in that fee. There is no setup fee and no monthly fee.</p>
      <h3>Who pays the fee</h3>
      <p>You choose, per event:</p>
      <ul>
        <li><b>Buyer pays the fee:</b> the fee is added at checkout. You receive your full ticket price.</li>
        <li><b>You absorb the fee:</b> buyers pay your ticket price only, and the fee comes out of each sale.</li>
      </ul>
      <div class="table"><table>
        <thead><tr><th>Ticket price</th><th>Ganor fee</th><th>Buyer pays (buyer pays fee)</th><th>You get (you absorb fee)</th></tr></thead>
        <tbody>
          <tr><td>₦2,000</td><td>₦200</td><td>₦2,200</td><td>₦1,800</td></tr>
          <tr><td>₦5,000</td><td>₦350</td><td>₦5,350</td><td>₦4,650</td></tr>
          <tr><td>₦20,000</td><td>₦1,100</td><td>₦21,100</td><td>₦18,900</td></tr>
        </tbody>
      </table></div>
      <p>Try your own numbers with the <a href="./#pricing">calculator</a>.</p>
      <h3>Payouts</h3>
      <p>Ticket money is paid to the bank account you add in your host account. Your dashboard shows every sale, every fee and every payout, so you always know where your money is.</p>"""),
 ("gate", "Gate check-in", "scan", """
      <p>Any phone becomes the scanner. Open your event, tap <b>Scan</b>, and point the camera at a guest’s QR code. You’ll see one of three results:</p>
      <ul>
        <li><b>Admitted:</b> the ticket is valid. Let the guest in.</li>
        <li><b>Already checked in:</b> this ticket was scanned before. The screen shows when and at which gate.</li>
        <li><b>Not a valid ticket:</b> the code isn’t for this event. Send the guest to your help desk.</li>
      </ul>
      <p>Several people can scan at once, at different gates. Each ticket works once, so the same QR code can’t get two people in.</p>"""),
 ("guests", "For guests", "user", """
      <h3>Buying a ticket</h3>
      <p>Open the event link, choose your tickets and pay by card, bank transfer or USSD. Your ticket arrives on WhatsApp straight away, with a QR code to show at the gate.</p>
      <h3>Questions about an event</h3>
      <p><b>Contact the host.</b> The host runs the event, so questions about the venue, the programme, changes or refunds go to them. Every event page shows how to reach the host.</p>
      <h3>When to contact Ganor</h3>
      <p>Message us if you paid but your ticket didn’t arrive, if you were charged twice, or if you can’t reach the host about a cancelled event. See the <a href="refunds.html">refund policy</a>.</p>"""),
 ("places", "For businesses", "shop", """
      <p>Ganor Places helps people find the businesses they can trust nearby: phone and electronics shops, fabric sellers, markets, hospitals, pharmacies, restaurants, hotels, event halls, salons, mechanics, schools, coworking spaces, tech hubs, gyms, football pitches and mini stadiums, parks and more.</p>
      <p>Every listing is checked in person, with directions and a working phone number. Ganor Places comes after events. To be among the first listed, <a href="./#join">join the list</a> and choose <b>A local business</b>.</p>"""),
 ("help", "Get help", "support", f"""
      <p>We answer on WhatsApp first.</p>
      {CONTACT}"""),
 ])

# ---------------- TERMS ----------------
page("terms", "Terms of use", "The terms for using Ganor as a host, a guest or a business.",
 "Legal", "Terms of use", "The rules for using Ganor, written to be read. Please read them before you host, buy or list on Ganor.",
 [
 ("about", "About these terms", "doc", """
      <p>These terms apply when you use ganor.ng, the Ganor app or any Ganor service (together, “Ganor”). “We” and “us” mean Ganor. “You” means anyone using Ganor: a <b>host</b> who runs an event, a <b>guest</b> who buys a ticket or RSVPs, or a <b>business</b> listed on Ganor Places.</p>
      <p>By using Ganor you agree to these terms, our <a href="privacy.html">privacy policy</a> and our <a href="refund-policy">refund policy</a>.</p>""".replace('refund-policy','refunds.html')),
 ("who", "Who can use Ganor", "users", """
      <ul>
        <li>Hosts and businesses must be at least 18 and able to enter a contract in Nigeria.</li>
        <li>Guests under 18 should use Ganor with a parent or guardian’s permission.</li>
        <li>You must give true details and keep your account safe. You’re responsible for what happens in your account.</li>
      </ul>"""),
 ("role", "What Ganor does", "compass", """
      <p>Ganor provides the tools to list events, sell tickets and RSVPs, take payments, deliver tickets and check guests in. <b>Ganor does not organise or run the events listed on it.</b> Each event is run by its host, and the host is responsible for it.</p>
      <p>When you buy a ticket, your agreement for the event is with the host. We sell and deliver the ticket on the host’s behalf.</p>"""),
 ("hosts", "If you host an event", "calendar", """
      <ul>
        <li>Describe your event honestly: date, time, venue, prices and what’s included.</li>
        <li>Give a way for guests to reach you, and answer their questions.</li>
        <li>Run the event as described. If you change or cancel it, tell guests through Ganor straight away.</li>
        <li>Set a clear refund rule for your event and honour it, and refund guests if you cancel (see the <a href="refunds.html">refund policy</a>).</li>
        <li>Make sure your event, venue and ticket sales follow the law and any permits you need.</li>
        <li>Use guests’ details only to run your event.</li>
      </ul>"""),
 ("guests", "If you buy a ticket", "ticket", """
      <ul>
        <li>The price you pay is shown before you pay, including any Ganor fee.</li>
        <li>Your ticket is sent to the WhatsApp number you give. Keep your QR code to yourself: each ticket works once, and the first scan is the one that counts.</li>
        <li>Questions about the event, changes and refunds go to the host. If you can’t reach them, message us.</li>
        <li>Don’t resell tickets for more than you paid or copy tickets. The host may refuse entry for copied or resold tickets.</li>
        <li>The host and venue decide who is let in and the rules on the day.</li>
      </ul>"""),
 ("fees", "Fees and payments", "percent", """
      <p>Free events cost nothing. On paid tickets, the Ganor fee is 5% of the ticket price + ₦100 per ticket, with card and transfer charges included. The host chooses whether the buyer pays the fee at checkout or the host absorbs it. We may change our fees; changes never apply to tickets already sold, and we’ll tell hosts before they take effect.</p>
      <p>Payments are processed by our licensed payment partners. We don’t store card details. Ticket money, minus the Ganor fee where the host absorbs it, is paid out to the host’s bank account.</p>"""),
 ("not-allowed", "What’s not allowed", "shield", """
      <ul>
        <li>Fake, misleading or duplicate events or listings.</li>
        <li>Events or businesses that break the law, or that promote hate, violence or harm.</li>
        <li>Selling tickets you don’t have the right to sell.</li>
        <li>Collecting payments outside Ganor for tickets advertised on Ganor.</li>
        <li>Trying to break, copy or overload Ganor, or to get into other people’s accounts.</li>
      </ul>
      <p>We may remove events or listings, hold payouts while we check a problem, or close accounts that break these terms. Where we can, we’ll tell you why.</p>"""),
 ("places", "Ganor Places", "shop", """
      <p>Businesses on Ganor Places must give true details and keep them up to date. We check listings in person, but we can’t promise the quality of any business’s goods or services. Deal with businesses carefully, as you would anywhere.</p>"""),
 ("liability", "Our responsibility", "info", """
      <p>We work hard to keep Ganor running and safe, but we can’t promise it will always be available or free of errors. We are not responsible for how an event is run, for what happens at an event, or for a host’s or business’s actions.</p>
      <p>Nothing in these terms limits rights you have under Nigerian consumer law, including the Federal Competition and Consumer Protection Act 2018.</p>"""),
 ("changes", "Changes and law", "settings", """
      <p>We may update these terms. If a change is important, we’ll tell you before it applies. These terms are governed by the laws of the Federal Republic of Nigeria.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- PRIVACY ----------------
page("privacy", "Privacy policy", "What personal data Ganor collects, why, who it’s shared with, and your rights under the Nigeria Data Protection Act 2023.",
 "Legal", "Privacy policy", "What we collect, why we collect it, and the choices you have. We only collect what we need to run Ganor.",
 [
 ("who", "Who we are", "info", """
      <p>Ganor (“we”) runs ganor.ng and the Ganor app, and is responsible for the personal data described here. We follow the Nigeria Data Protection Act 2023.</p>"""),
 ("collect", "What we collect", "doc", """
      <h3>When you join the list</h3>
      <p>Your name, your WhatsApp number or email (you choose), whether you’re a host, a guest or a business, and the kind of event you’re interested in, if you tell us.</p>
      <h3>When you use Ganor</h3>
      <ul>
        <li><b>Account:</b> name, phone number, email and password.</li>
        <li><b>Tickets:</b> the name and WhatsApp number on each ticket, what you bought and when it was scanned at the gate.</li>
        <li><b>Hosts and businesses:</b> event or business details, contact details and the bank account for payouts.</li>
        <li><b>Payments:</b> handled by our licensed payment partners. We receive confirmation of payment, not your card details.</li>
      </ul>
      <h3>On this website</h3>
      <p>We don’t use advertising or tracking cookies. The site stores one small note in your browser so the opening animation only plays once per visit.</p>"""),
 ("use", "How we use it", "settings", """
      <ul>
        <li>To deliver tickets and messages on WhatsApp.</li>
        <li>To process payments and pay hosts.</li>
        <li>To check guests in at the gate.</li>
        <li>To tell you when Ganor opens, if you joined the list.</li>
        <li>To keep Ganor safe and stop fraud.</li>
        <li>To meet our legal duties.</li>
      </ul>
      <p>We never sell your personal data.</p>"""),
 ("share", "Who we share it with", "users", """
      <ul>
        <li><b>The host of an event you attend:</b> the name on your ticket, your ticket type and your check-in, so they can run their event. Hosts may only use this for that event.</li>
        <li><b>Payment partners:</b> to process payments and payouts.</li>
        <li><b>Messaging, email and hosting providers:</b> to send WhatsApp messages and emails, deliver website form submissions to our inbox, and run our service.</li>
        <li><b>Authorities:</b> when the law requires it.</li>
      </ul>"""),
 ("keep", "How long we keep it", "clock", """
      <p>We keep your data only as long as we need it: account data while your account is open, ticket and payment records for as long as the law requires, and waitlist details until Ganor opens or until you ask us to delete them.</p>"""),
 ("rights", "Your rights", "shield", """
      <p>You can ask us to:</p>
      <ul>
        <li>Show you the personal data we hold about you.</li>
        <li>Correct it or delete it.</li>
        <li>Stop using it for messages about Ganor.</li>
        <li>Give you a copy to take elsewhere.</li>
      </ul>
      <p>Message us and we’ll reply within 30 days. If you’re unhappy with our answer, you can complain to the Nigeria Data Protection Commission.</p>"""),
 ("safety", "Security", "lock", """
      <p>We protect your data with access controls and encryption in transit. If a breach puts your data at risk, we’ll tell you and the Nigeria Data Protection Commission as the law requires.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- REFUNDS ----------------
page("refunds", "Refund policy", "How refunds work on Ganor: who to contact, what happens when an event is cancelled, and when Ganor steps in.",
 "Legal", "Refund policy", "Refunds start with the host, because the host runs the event. Here’s how it works, and when we step in.",
 [
 ("host", "Ask the host first", "chat", """
      <p>Each event has its own refund rule, set by the host and shown on the event page before you pay. For any question about refunds, changes or the event itself, <b>contact the host</b> using the details on the event page.</p>"""),
 ("cancelled", "If an event is cancelled", "close-circle", """
      <p>If the host cancels the event, everyone who bought a ticket gets their money back, including the Ganor fee. The refund goes back the way you paid.</p>"""),
 ("changed", "If an event changes", "calendar", """
      <p>If the date, time or venue changes, we’ll message you on WhatsApp. If you can’t make the new date or place, ask the host for a refund under their event’s refund rule.</p>"""),
 ("ganor", "When to contact Ganor", "info", """
      <p>Message us directly if:</p>
      <ul>
        <li>You paid but your ticket didn’t arrive.</li>
        <li>You were charged more than once for the same ticket.</li>
        <li>An event was cancelled and you can’t reach the host.</li>
      </ul>
      <p>We’ll look into it and, where a refund is owed, make sure it reaches you.</p>"""),
 ("how", "How refunds are paid", "wallet", """
      <p>Refunds go back to the card or account you paid with, through our payment partner. Banks can take a few working days to show the money in your account.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- CREDITS ----------------
page("credits", "Credits and licences", "Credits and licences for the icons, typefaces and logos used on ganor.ng.",
 "Legal", "Credits and licences", "The work of others that helps make Ganor.",
 [
 ("icons", "Icons", "star", """<p>Icons from the <a href="https://icon-sets.iconify.design/solar/" rel="noopener">Solar icon set</a> by 480 Design, licensed <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener">CC BY 4.0</a>, recoloured and reorganised for Ganor.</p>"""),
 ("type", "Typefaces", "pen", """<p>Bricolage Grotesque and Inter, both licensed under the <a href="https://openfontlicense.org" rel="noopener">SIL Open Font License 1.1</a>. Font files are hosted on this site; licence texts are in <a href="assets/fonts/OFL-Inter.txt">assets/fonts</a>.</p>"""),
 ("social", "Social media logos", "share", """<p>Instagram, TikTok, X, Facebook, YouTube and WhatsApp logos are trademarks of their owners and are used only to link to Ganor’s accounts. Facebook, Instagram and YouTube icons from <a href="https://feathericons.com" rel="noopener">Feather</a> (MIT). TikTok, X and WhatsApp icons from <a href="https://tabler.io/icons" rel="noopener">Tabler Icons</a> (MIT).</p>"""),
 ("ganor", "Ganor", "verified", """<p>The Ganor name, logo and symbol are Ganor’s. Please don’t use them without asking.</p>"""),
 ])
print("pages written")
