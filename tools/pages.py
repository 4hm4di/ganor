"""Writes the inner pages (docs, legal) into src/ from the content below.
Run: python3 tools/pages.py && python3 tools/build.py
"""
from pathlib import Path
SRC = Path(__file__).resolve().parent.parent / "src"
UPDATED = "21 November 2026"

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

CONTACT = """<p>WhatsApp or call <a href="https://wa.me/2348106742222" rel="noopener">0810 674 2222</a>, email <a href="mailto:support@ganor.ng">support@ganor.ng</a>, or visit us at No. 15 Guda Abdullahi Road, Farm Center, Kano.</p>"""

# ---------------- DOCS ----------------
page("docs", "Docs", "How Ganor works for hosts, gate teams and guests: accounts, free RSVP events and plans, paid tickets, fees, gate check-in and getting help.",
 "Docs", "How Ganor works", "Everything you need to host an event, run the gate or get a ticket. Short answers, in plain words.",
 [
 ("start", "Getting started", "compass", """
      <p>Ganor is where you find what’s happening near you. Hosts create an event, share one link, take free RSVPs or sell tickets, and scan guests in at the gate. Guests open the link, get their ticket with a QR code, and show it at the door.</p>
      <div class="callout"><b>Ganor is open.</b> Create your host account at <a href="https://app.ganor.ng/login?mode=signup">app.ganor.ng</a>, or <a href="https://app.ganor.ng/events">find events near you</a>.</div>
      <h3>Who Ganor is for</h3>
      <ul>
        <li><b>Hosts:</b> anyone running a gathering, from conferences, summits, trade fairs and cooperative launches to lectures, campus events and shows.</li>
        <li><b>Gate teams:</b> the people a host trusts to scan guests in.</li>
        <li><b>Guests:</b> anyone looking for something to go to, or holding a ticket.</li>
      </ul>
      <p>Hosts and gate teams work in the Ganor app at <b>app.ganor.ng</b>. Guests don’t need an account.</p>"""),
 ("account", "Your host account", "user", """
      <h3>Signing up</h3>
      <p>Create your host account at <b>app.ganor.ng</b> with your email and a password, then open the link we email you to confirm your address. Either way, you tick the box to agree to the Terms and Privacy policy first. Or tap <b>Continue with Google</b> to sign up and sign in with your Google account.</p>
      <p>Your first visit opens your overview with a short <b>to-do list</b>: add a contact number and logo, create and publish your first event, share the link, and add a payout account and gate team if you need them. Hide it any time.</p>
      <h3>Your host profile</h3>
      <p>Your name, logo and a few lines about you appear on your event pages. Add how guests can reach you: a <b>WhatsApp or call number is required before you can publish</b>. Email, website and Instagram are optional.</p>
      <h3>Staying safe</h3>
      <ul>
        <li><b>One device at a time.</b> Signing in on a new phone or computer signs your account out everywhere else.</li>
        <li><b>Automatic sign-out.</b> After 30 minutes without activity, or when you close the browser, you’re signed out.</li>
        <li><b>Your bank account</b> for payouts is added once in your dashboard. Ganor confirms the account name, then your share of each paid ticket goes straight to it.</li>
      </ul>"""),
 ("create", "Create an event", "calendar", """
      <p>Tap <b>New event</b> and choose what kind it is:</p>
      <ul>
        <li><b>Free RSVP:</b> guests register for free. Choose a plan by how many guests you expect (see <a href="#rsvp">Free RSVP events</a>).</li>
        <li><b>Paid tickets:</b> guests buy tickets (see <a href="#tickets">Paid tickets</a>).</li>
      </ul>
      <ol>
        <li>Give your event a name, a category, a date and start and end times.</li>
        <li>Add the city, the venue and its address so guests can find you.</li>
        <li>Add a banner for the top of your event page and a few lines about what to expect.</li>
        <li>If it applies, tick <b>Halal-friendly</b> (see <a href="#halal">Halal-friendly events</a>).</li>
        <li>Save. Your event stays a draft, visible only to you, until you publish it.</li>
      </ol>
      <p>Before you can publish, Ganor checks that your profile has a WhatsApp or call number, that a paid event has at least one ticket type, and that a paid RSVP plan has been paid. You can change the details after you publish; tell your guests about any change to the date, time or venue.</p>
      <h3>Public or private</h3>
      <p>When you publish, you choose who can find your event. <b>Public</b> events are listed on Ganor&rsquo;s Find events page and can show up in search. <b>Private</b> events are left off Find events and out of search; only people you send the link to can open them. You can switch between the two any time from your event page.</p>"""),
 ("rsvp", "Free RSVP events", "users", """
      <p>A Free RSVP event costs your guests nothing. Each guest gives their name and phone number, answers any questions you add, and gets a ticket with a QR code to show at the gate. One phone number can RSVP once per event.</p>
      <h3>Plans</h3>
      <p>You pay once per event, by how many guests you expect. Small events are free.</p>
      <div class="table"><table>
        <thead><tr><th>Plan</th><th>Price per event</th><th>Guests</th><th>Your questions</th></tr></thead>
        <tbody>
          <tr><td>Free</td><td>₦0</td><td>Up to 30</td><td>2</td></tr>
          <tr><td>Basic</td><td>₦50,000</td><td>Up to 200</td><td>4</td></tr>
          <tr><td>Standard</td><td>₦100,000</td><td>Up to 500</td><td>6</td></tr>
          <tr><td>Pro</td><td>₦175,000</td><td>Up to 1,500</td><td>6</td></tr>
          <tr><td>Premium</td><td>₦250,000</td><td>Up to 5,000</td><td>6</td></tr>
        </tbody>
      </table></div>
      <ul>
        <li>A paid plan is paid before the event is published, and covers that one event. To pay, email support@ganor.ng with the reference in your event’s <b>Plan</b> card and we’ll send the bank details; once Ganor confirms your payment, you can publish.</li>
        <li>On the Free plan, RSVPs close when 30 guests have registered. You can upgrade from your event page at any time.</li>
        <li>The Free plan includes one gate account for the event. Paid plans can have as many as you need.</li>
        <li>You can run one Free plan event at a time, and start up to 2 a month. Past that, Ganor shows you the paid plans for your next event; or try again later.</li>
        <li>Your dashboard shows what each plan includes before you choose.</li>
      </ul>
      <h3>Your questions</h3>
      <p>Add questions to the RSVP form, such as organisation, job title or t-shirt size, and mark which ones are required. You can download your guest list with their answers.</p>
      <h3>Keeping RSVPs real</h3>
      <p>Ganor limits fake RSVPs for you: one RSVP per phone number, up to 4 guests registered from the same phone, and a cap on bursts of RSVPs from one network. Guests who hit a limit see a clear message telling them what to do.</p>"""),
 ("tickets", "Paid tickets", "ticket", """
      <p>A paid event can have as many ticket types as you need, for example Regular, VIP and Table for 10. For each one you set:</p>
      <ul>
        <li><b>The price.</b> Every paid ticket costs at least <b>₦1,000</b>. Paid events can’t have free tickets; for a free event, create a Free RSVP event.</li>
        <li><b>How many</b> are available, and the most one person can buy in an order.</li>
        <li><b>What’s included</b>, such as front rows, lunch or a certificate (optional).</li>
      </ul>
      <p>You can pause or reopen any ticket type at any time. Once a ticket type has sold, its price is locked; add a new ticket type for a different price.</p>
      <div class="callout"><b>Card, transfer and USSD checkout is switching on.</b> You can set up, publish and share paid events now. Until checkout is live, your event page tells guests that ticket sales open soon.</div>"""),
 ("share", "Share your event", "share", """
      <p>Every event gets one link, like <b>app.ganor.ng/e/your-event</b>. Post it on WhatsApp, your status, Instagram or anywhere else. The link shows a clean preview with your banner, date and venue, and your event page has buttons to share it on WhatsApp, X, Facebook and LinkedIn.</p>
      <p>Guests who open the link can RSVP or buy straight away. They don’t need an account or an app.</p>"""),
 ("fees", "Fees and payouts", "percent", """
      <p>Free events on the Free plan cost nothing. On paid tickets, the Ganor fee is <b>6% of the ticket price + ₦100 per ticket</b>. Card and bank transfer charges are included in that fee. There is no setup fee and no monthly fee. Larger free events use a <a href="#rsvp">plan</a> instead.</p>
      <h3>Who pays the fee</h3>
      <p>You choose, per event:</p>
      <ul>
        <li><b>Buyer pays the fee:</b> the fee is added at checkout. You receive your full ticket price.</li>
        <li><b>You absorb the fee:</b> buyers pay your ticket price only, and the fee comes out of each sale.</li>
      </ul>
      <div class="table"><table>
        <thead><tr><th>Ticket price</th><th>Ganor fee</th><th>Buyer pays (buyer pays fee)</th><th>You get (you absorb fee)</th></tr></thead>
        <tbody>
          <tr><td>₦2,000</td><td>₦220</td><td>₦2,220</td><td>₦1,780</td></tr>
          <tr><td>₦5,000</td><td>₦400</td><td>₦5,400</td><td>₦4,600</td></tr>
          <tr><td>₦20,000</td><td>₦1,300</td><td>₦21,300</td><td>₦18,700</td></tr>
        </tbody>
      </table></div>
      <p>Try your own numbers with the <a href="./#pricing">calculator</a>.</p>
      <h3>Your dashboard</h3>
      <p>Your dashboard shows tickets and RSVPs, take-home and check-ins over 7, 30 or 90 days, with a chart for each event and a projection to event day. Download your guest list as a spreadsheet (CSV) or a branded PDF, and look up any guest by phone to resend their ticket on WhatsApp.</p>
      <h3>Payouts</h3>
      <p>Add the bank account for your payouts in your dashboard. Ganor confirms the account name matches your bank&rsquo;s record, and your paid tickets go on sale once it&rsquo;s verified. After that, every ticket payment is split at checkout by Paystack, our licensed payment partner: your share settles directly to your bank account on Paystack&rsquo;s normal settlement schedule, and the Ganor fee goes to Ganor. Ganor doesn&rsquo;t hold ticket money, and there&rsquo;s nothing to request. Your <b>Earnings</b> page in the dashboard shows your take-home, the Ganor fees, any refunds, each event&rsquo;s sales and your payout account&rsquo;s status, so you always know where your money is.</p>"""),
 ("gate", "Gate check-in", "scan", """
      <p>Any phone becomes the scanner. Open your event and tap <b>Gate check-in</b>, or let your gate team scan for you. Point the camera at a guest’s QR code, or type the code under it. You’ll see one of these results:</p>
      <ul>
        <li><b>Admitted:</b> the ticket is valid. Let the guest in.</li>
        <li><b>Already checked in:</b> this ticket was scanned before. The screen shows when.</li>
        <li><b>Not a valid ticket:</b> the code isn’t for this event. Send the guest to your help desk.</li>
        <li><b>Not assigned:</b> this gate account isn’t set up for this event. Ask the host to tick it.</li>
      </ul>
      <p>Each ticket works once, so the same QR code can’t get two people in. The scanner shows how many guests are in so far.</p>
      <h3>Your gate team</h3>
      <ol>
        <li>In your dashboard, open <b>Gate team</b> and add each person with their own username and password.</li>
        <li>Tick the events each person can check in. They see only those events.</li>
        <li>Share their sign-in details with <b>Copy</b> or <b>Send on WhatsApp</b>. They sign in at <b>app.ganor.ng/gate</b>.</li>
      </ol>
      <ul>
        <li>A password is shown once, when you set it. If someone loses theirs, set a new one; it signs them out on their phone.</li>
        <li>Each gate account works on <b>one phone at a time</b>. Signing in on another phone signs out the first.</li>
        <li>You can switch an account off or delete it at any time.</li>
      </ul>"""),
 ("guests", "For guests", "user", """
      <h3>Getting your ticket</h3>
      <p>Open the event link. For a free event, enter your name, your phone number and any details the host asks for, then tap <b>RSVP</b>. For a paid event, choose your tickets and pay by card, bank transfer or USSD once sales are open.</p>
      <p>Your ticket appears straight away with its QR code. Each ticket also has a <b>private link</b>: tap <b>Save to my WhatsApp</b> to send it to your own chat, copy it, and if you gave an email we email it to you too. On the day, open the link (or a screenshot) and show the QR code at the gate. Each ticket gets one person in, once.</p>
      <p>Lost your link? Ask the host. They can look you up by your phone number and send your ticket link to you on WhatsApp.</p>
      <h3>Questions about an event</h3>
      <p><b>Contact the host.</b> The host runs the event, so questions about the venue, the programme, changes or refunds go to them. Every event page has the host’s WhatsApp or phone number.</p>
      <h3>When to contact Ganor</h3>
      <p>Message us if you paid but your ticket didn’t appear, if you were charged twice, or if you can’t reach the host about a cancelled event. See the <a href="refunds.html">refund policy</a>.</p>"""),
 ("halal", "Halal-friendly events", "halal", """
      <p>Hosts can mark an event <b>Halal-friendly</b> so guests who care about it can find it with the Halal-friendly filter. Say in your event details what applies. The label can mean:</p>
      <h3>How the event is run</h3>
      <ul>
        <li>Halal food and drinks only, and no alcohol.</li>
        <li>Prayer times kept in the programme, with a place to pray.</li>
        <li>A modest dress code, or separate seating for men and women.</li>
      </ul>
      <h3>What the event is about</h3>
      <ul>
        <li>Islamic finance and non-interest banking.</li>
        <li>Halal investment, savings, takaful and zakat.</li>
        <li>Halal products, trade and certification, such as halal expos and Muslim business fairs.</li>
        <li>Islamic lectures, Eid fests and community gatherings.</li>
      </ul>
      <div class="callout"><b>This is the host’s description.</b> Ganor doesn’t certify events as halal. If an event isn’t what the host said, tell us and we’ll look into it. Using the label falsely counts as a misleading event under our <a href="terms.html#not-allowed">terms</a>.</div>"""),
  ("help", "Get help", "support", f"""
      <p>We answer on WhatsApp first.</p>
      {CONTACT}"""),
 ])

# ---------------- TERMS ----------------
page("terms", "Terms of use", "The terms for using Ganor as a host, a gate team member or a guest.",
 "Legal", "Terms of use", "The rules for using Ganor, written to be read. Please read them before you host, buy or list on Ganor.",
 [
 ("about", "About these terms", "doc", """
      <p>These terms apply when you use ganor.ng, the Ganor app at app.ganor.ng or any Ganor service (together, “Ganor”). “We” and “us” mean Ganor. “You” means anyone using Ganor: a <b>host</b> who runs an event, a <b>gate team member</b> who scans tickets for a host, or a <b>guest</b> who RSVPs or buys a ticket.</p>
      <p>By using Ganor you agree to these terms, our <a href="acceptable-use.html">acceptable use policy</a>, <a href="privacy.html">privacy policy</a>, <a href="refunds.html">refund policy</a> and <a href="ticket-delivery.html">ticket delivery policy</a>.</p>"""),
 ("who", "Who can use Ganor", "users", """
      <ul>
        <li>Hosts must be at least 18 and able to enter a contract in Nigeria.</li>
        <li>Guests under 18 should use Ganor with a parent or guardian’s permission.</li>
        <li>You must give true details and keep your account safe. You’re responsible for what happens in your account.</li>
      </ul>"""),
 ("accounts", "Accounts and sign-in", "lock", """
      <ul>
        <li>You can sign in with your email and password, an email link, or your Google account. Keep your password to yourself.</li>
        <li>Each host account and each gate account can be used on <b>one device at a time</b>. Signing in on another device signs out the first.</li>
        <li>For safety, you’re signed out after 30 minutes without activity and when you close your browser.</li>
        <li>Gate accounts are created by a host. The host is responsible for who they give a gate account to, for the events they assign, and for switching an account off when it’s no longer needed.</li>
      </ul>"""),
 ("role", "What Ganor does", "compass", """
      <p>Ganor provides the tools to list events, take free RSVPs, sell tickets, take payments, deliver tickets and check guests in. <b>Ganor does not organise or run the events listed on it.</b> Each event is run by its host, and the host is responsible for it.</p>
      <p>When you RSVP or buy a ticket, your agreement for the event is with the host. We deliver the ticket, and sell it on the host’s behalf.</p>"""),
 ("hosts", "If you host an event", "calendar", """
      <ul>
        <li>Describe your event honestly: date, time, venue, prices and what’s included.</li>
        <li>Give a WhatsApp or call number guests can reach you on, and answer their questions. You can’t publish without one.</li>
        <li>Run the event as described. If you change or cancel it, tell your guests straight away.</li>
        <li>Refund guests if you cancel a paid event, and handle other refund requests fairly (see the <a href="refunds.html">refund policy</a>).</li>
        <li>Make sure your event, venue and ticket sales follow the law and any permits you need.</li>
        <li>Use guests’ details, including their answers to your RSVP questions, only to run your event.</li>
      </ul>"""),
 ("guests", "If you get a ticket", "ticket", """
      <ul>
        <li>The price you pay is shown before you pay, including any Ganor fee.</li>
        <li>Your ticket and its QR code appear as soon as you RSVP or pay, with a private link to your ticket. Keep the QR code and the link to yourself: anyone with them can use the ticket, each ticket works once, and the first scan is the one that counts.</li>
        <li>One phone number can RSVP once to each free event.</li>
        <li>Questions about the event, changes and refunds go to the host. If you can’t reach them, message us.</li>
        <li>Don’t resell tickets for more than you paid or copy tickets. The host may refuse entry for copied or resold tickets.</li>
        <li>The host and venue decide who is let in and the rules on the day.</li>
      </ul>"""),
 ("fees", "Fees and payments", "percent", """
      <p><b>Paid tickets:</b> the Ganor fee is 6% of the ticket price + ₦100 per ticket, with card and transfer charges included. Paid tickets cost at least ₦1,000. The host chooses whether the buyer pays the fee at checkout or the host absorbs it.</p>
      <p><b>Free RSVP events:</b> the Free plan costs nothing and allows up to 30 guests, for one event at a time and up to 2 events a calendar month. Hosts pay for plans by bank transfer, confirmed by Ganor before the event is published. Larger free events use a paid plan (Basic, Standard, Pro or Premium), priced per event and shown before you choose. A plan is paid before the event is published and covers that one event only. Plan fees aren’t refundable once the event is published, except where the law requires.</p>
      <p>We may change our fees. Changes never apply to tickets or plans already paid for, and we’ll tell hosts before they take effect.</p>
      <p>Payments are processed by our licensed payment partners. We don’t store card details. Each ticket payment is split at checkout by our payment partner: the host’s share (the ticket price, minus the Ganor fee where the host absorbs it) settles directly to the host’s verified bank account, and the Ganor fee goes to Ganor. Ganor doesn’t hold ticket money for hosts or guests.</p>"""),
 ("not-allowed", "What’s not allowed", "shield", """
      <ul>
        <li>Fake, misleading or duplicate events or listings, including misusing the Halal-friendly label.</li>
        <li>Events that break the law, or that promote hate, violence or harm.</li>
        <li>Selling tickets you don’t have the right to sell.</li>
        <li>Collecting payments outside Ganor for tickets advertised on Ganor.</li>
        <li>Fake RSVPs, filling an event’s places to keep real guests out, or using several phones or networks to get round RSVP limits.</li>
        <li>Sharing one account between people to get round the one-device rule.</li>
        <li>Trying to break, copy or overload Ganor, or to get into other people’s accounts.</li>
      </ul>
      <p>We may remove events or listings, pause ticket sales while we check a problem, or suspend or close accounts that break these terms. Where we can, we’ll tell you why.</p>"""),
  ("liability", "Our responsibility", "info", """
      <p>We work hard to keep Ganor running and safe, but we can’t promise it will always be available or free of errors. We are not responsible for how an event is run, for what happens at an event, or for a host’s or business’s actions.</p>
      <p>Nothing in these terms limits rights you have under Nigerian consumer law, including the Federal Competition and Consumer Protection Act 2018.</p>"""),
 ("changes", "Changes and law", "settings", """
      <p>We may update these terms. If a change is important, we’ll tell you before it applies. These terms are governed by the laws of the Federal Republic of Nigeria.</p>"""),
 ("credits", "Credits and licences", "star", """
      <p>Ganor uses work by others, under these licences:</p>
      <ul>
        <li><b>Icons:</b> the <a href="https://icon-sets.iconify.design/solar/" rel="noopener">Solar icon set</a> by 480 Design, licensed <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener">CC BY 4.0</a>, recoloured and reorganised for Ganor.</li>
        <li><b>Social icons:</b> Facebook, Instagram, LinkedIn and YouTube from <a href="https://feathericons.com" rel="noopener">Feather</a>; TikTok, X and WhatsApp from <a href="https://tabler.io/icons" rel="noopener">Tabler Icons</a>. Both MIT licensed. The platform logos are trademarks of their owners and are used only to link to Ganor’s accounts.</li>
        <li><b>Typefaces:</b> Bricolage Grotesque and Inter, licensed under the <a href="https://openfontlicense.org" rel="noopener">SIL Open Font License 1.1</a>.</li>
      </ul>
      <p>The Ganor name, logo and symbol are Ganor’s. Please don’t use them without asking.</p>"""),
  ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- PRIVACY ----------------
page("privacy", "Privacy policy", "What personal data Ganor collects, why, who it’s shared with, and your rights under the Nigeria Data Protection Act 2023.",
 "Legal", "Privacy policy", "What we collect, why we collect it, and the choices you have. We only collect what we need to run Ganor.",
 [
 ("who", "Who we are", "info", """
      <p>Ganor (“we”) runs ganor.ng and the Ganor app at app.ganor.ng, and is responsible for the personal data described here. We follow the Nigeria Data Protection Act 2023.</p>"""),
 ("collect", "What we collect", "doc", """
      <h3>When you sign up for updates</h3>
      <p>Your name, your WhatsApp number or email (you choose), whether you’re a host or a guest, and the kind of event you’re interested in, if you tell us.</p>
      <h3>When you use Ganor</h3>
      <ul>
        <li><b>Host account:</b> your name and email, and your password (stored scrambled, so no one can read it). If you sign in with Google, Google shares your name and email address with us.</li>
        <li><b>Host profile:</b> your logo, a few lines about you, and your contact details: WhatsApp or call number, and email, website and Instagram if you add them. These are shown on your event pages.</li>
        <li><b>Guests:</b> the name and phone number on each RSVP or ticket, your email if the host asks for it, your answers to the host’s questions, what you got and when it was scanned at the gate. Each RSVP or ticket also gets a private ticket link.</li>
        <li><b>Stopping fake RSVPs:</b> when you RSVP we keep a scrambled code for your browser and for your network, so we can limit how many RSVPs come from one phone or one place. We never store your IP address or a readable device ID.</li>
        <li><b>Gate team:</b> each gate account’s name and username, which events it can check in, when it signed in, and the tickets it scanned.</li>
        <li><b>Ratings:</b> if you agreed at checkout, the star rating and comment you leave after an event, the name you choose to show, and whether your ticket was scanned.</li>
        <li><b>Hosts:</b> event details, and the bank account for payouts.</li>
        <li><b>Payments:</b> handled by our licensed payment partners. We receive confirmation of payment, not your card details.</li>
      </ul>
      <h3>Cookies</h3>
      <p>We don’t use advertising or tracking cookies. The Ganor app uses only the cookies it needs to work: keeping you signed in (they end when you close your browser), signing you out after 30 minutes without activity, keeping a gate phone signed in, and showing a short message after you save something, and one cookie that lets us limit how many RSVPs one phone can make for an event. The ganor.ng website stores one small note in your browser so the opening animation only plays once per visit.</p>"""),
 ("use", "How we use it", "settings", """
      <ul>
        <li>To run your account, keep it to one device at a time, and keep it secure.</li>
        <li>To deliver tickets and check guests in at the gate, including emailing your ticket link if you gave an email address, and letting the host resend your ticket link on WhatsApp if you lose it.</li>
        <li>To process payments and pay hosts.</li>
        <li>To send you one WhatsApp message after an event asking you to rate it, only if you ticked that box at checkout. Reply STOP and we won’t send another.</li>
        <li>To show guests’ ratings of events and hosts, so people can choose events with confidence.</li>
        <li>To tell you about new events and other Ganor updates, if you signed up for them.</li>
        <li>To keep Ganor safe and stop fraud, such as fake RSVPs.</li>
        <li>To meet our legal duties.</li>
      </ul>
      <p>We never sell your personal data.</p>"""),
 ("share", "Who we share it with", "users", """
      <ul>
        <li><b>The host of an event you attend:</b> your name, phone number, email if asked, answers to their questions, your ticket type and your check-in, so they can run their event. Hosts may only use this for that event.</li>
        <li><b>The host’s gate team:</b> what they need to check you in, such as your name and ticket type when your code is scanned.</li>
        <li><b>Everyone who visits Ganor:</b> a host’s profile and contact details on their event pages. If you leave a rating, your stars, your comment and either your first name and last initial or “Verified attendee” (your choice). Never a guest’s phone number. The host can reply publicly.</li>
        <li><b>Payment partners:</b> to process payments and payouts.</li>
        <li><b>Service providers:</b> to run Ganor, send emails and WhatsApp messages, and deliver website form submissions to our inbox. Some are outside Nigeria, including Supabase (UK), Vercel, Brevo (email), Google (if you sign in with Google) and Meta (WhatsApp). We use their data protection terms to keep your data safe.</li>
        <li><b>Authorities:</b> when the law requires it.</li>
      </ul>"""),
 ("keep", "How long we keep it", "clock", """
      <p>We keep your data only as long as we need it: account data while your account is open, ticket and payment records for as long as the law requires, gate sign-in records for up to a week after they end, and update sign-ups until you unsubscribe or ask us to delete them. Rating links and the records of who agreed to rating messages are deleted 6 months after ratings for that event close. Published reviews stay up until you ask us to remove them; they are linked to a coded reference, not your phone number.</p>"""),
 ("rights", "Your rights", "shield", """
      <p>You can ask us to:</p>
      <ul>
        <li>Show you the personal data we hold about you.</li>
        <li>Correct it or delete it.</li>
        <li>Stop using it for messages about Ganor, including rating requests (or just reply STOP).</li>
        <li>Remove a review you left.</li>
        <li>Give you a copy to take elsewhere.</li>
      </ul>
      <p>Message us and we’ll reply within 30 days. If you’re unhappy with our answer, you can complain to the Nigeria Data Protection Commission.</p>"""),
 ("safety", "Security", "lock", """
      <p>We protect your data with access controls, encryption in transit and scrambled passwords. Accounts work on one device at a time and sign out when idle. If a breach puts your data at risk, we’ll tell you and the Nigeria Data Protection Commission as the law requires.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- REFUNDS ----------------
page("refunds", "Refund policy", "How refunds work on Ganor: who to contact, what happens when an event is cancelled, RSVP plan payments, and when Ganor steps in.",
 "Legal", "Refund policy", "Refunds start with the host, because the host runs the event. Here’s how it works, and when we step in.",
 [
 ("host", "Ask the host first", "chat", """
      <p>Each event is run by its host. For any question about refunds, changes or the event itself, <b>contact the host</b> on the WhatsApp or phone number shown on the event page.</p>"""),
 ("cancelled", "If an event is cancelled", "close-circle", """
      <p>If the host cancels a paid event, everyone who bought a ticket gets their money back, including the Ganor fee. The refund goes back the way you paid.</p>"""),
 ("changed", "If an event changes", "calendar", """
      <p>If the date, time or venue changes, the host should tell guests straight away, and the event page shows the new details. If you can’t make the new date or place, ask the host for a refund.</p>"""),
 ("plans", "RSVP plan payments (hosts)", "receipt", """
      <p>A paid RSVP plan covers one event. If you paid for a plan and haven’t published the event yet, message us and we’ll sort it out. Once the event is published, plan fees aren’t refundable, except where the law requires. If you paid twice for the same plan, we’ll refund the extra payment.</p>"""),
 ("ganor", "When to contact Ganor", "info", """
      <p>Message us directly if:</p>
      <ul>
        <li>You paid but your ticket didn’t appear.</li>
        <li>You were charged more than once for the same ticket.</li>
        <li>An event was cancelled and you can’t reach the host.</li>
      </ul>
      <p>We’ll look into it and, where a refund is owed, make sure it reaches you.</p>"""),
 ("how", "How refunds are paid", "wallet", """
      <p>Refunds go back to the card or account you paid with, through our payment partner. Banks can take a few working days to show the money in your account.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- ACCEPTABLE USE ----------------
page("acceptable-use", "Acceptable use policy", "What you can and can’t host, sell or do on Ganor, how we check, and what happens when the rules are broken.",
 "Legal", "Acceptable use policy", "Ganor is for real events, run honestly. This page sets out what’s allowed, what isn’t, and what we do about it.",
 [
 ("scope", "Who this applies to", "info", """
      <p>This policy applies to everyone who uses Ganor: <b>hosts</b> who run events, <b>gate team members</b> who scan tickets, and <b>guests</b> who RSVP or buy tickets. It is part of our <a href="terms.html">terms of use</a>.</p>"""),
 ("allowed", "What Ganor is for", "check-circle", """
      <p>Ganor is for listing real events, taking free RSVPs, selling tickets to them and checking guests in. For example:</p>
      <ul>
        <li>Conferences, summits, trade fairs, exhibitions and workshops.</li>
        <li>Concerts, comedy shows, film screenings and cultural events.</li>
        <li>Religious, community and charity gatherings.</li>
        <li>Weddings, naming ceremonies and other private events.</li>
        <li>Sports, fitness and outdoor events.</li>
      </ul>
      <p>A ticket on Ganor is entry to an event. It can include what the host says comes with it, such as a meal or an event pack, but it can’t be used to sell something else.</p>"""),
 ("not-allowed", "What isn’t allowed", "close-circle", """
      <p>You can’t use Ganor to list, promote or sell tickets for any of these:</p>
      <ul>
        <li>Anything illegal in Nigeria, or an event without the permits, licences or venue permission the law requires.</li>
        <li>Weapons, ammunition or explosives, or events that sell or hand them out.</li>
        <li>Illegal drugs or controlled substances, and alcohol or tobacco for anyone under 18.</li>
        <li>Adult, sexual or escort content or services.</li>
        <li>Gambling, betting, lotteries or raffles, unless the host holds the licence the law requires.</li>
        <li>Investment, trading or “money-making” schemes that promise returns, including forex or crypto signals, Ponzi, pyramid or multi-level recruitment schemes.</li>
        <li>Goods, services, memberships, loans or donations dressed up as tickets.</li>
        <li>Counterfeit or stolen goods, or events that copy another brand or event to mislead people.</li>
        <li>Hate, violence, harassment or discrimination, or groups that promote them.</li>
        <li>Fake events, events you don’t run or don’t have the right to sell tickets for, or details meant to mislead guests.</li>
      </ul>"""),
 ("conduct", "How everyone must use Ganor", "user", """
      <ul>
        <li>Give true details about yourself, your event and your payout account. Don’t pretend to be someone else.</li>
        <li>Take ticket payments for Ganor events only through Ganor’s checkout, and don’t use it to move money for anything other than tickets.</li>
        <li>Don’t make fake purchases, test stolen cards or try to get money back unfairly.</li>
        <li>Hosts use guests’ details only to run their event, and don’t send them spam.</li>
        <li>Guests don’t copy tickets or resell them for more than they paid.</li>
        <li>Gate accounts are only for checking guests in at the host’s events.</li>
        <li>Don’t try to break, overload, scrape or get around the security of Ganor.</li>
      </ul>"""),
 ("checks", "How we check", "shield", """
      <ul>
        <li>Hosts confirm their email address, and must add a WhatsApp or call number guests can reach before they can publish.</li>
        <li>A host’s paid tickets only go on sale once Ganor has confirmed that the name on their payout bank account matches their bank’s record.</li>
        <li>We may review any event, and we look into every report we receive from guests or anyone else.</li>
        <li>Our payment partner also runs its own checks on payments.</li>
      </ul>"""),
 ("breaking", "If the rules are broken", "warning", """
      <p>Depending on what happened, we may:</p>
      <ul>
        <li>Ask the host to change the event, or take the event down.</li>
        <li>Pause ticket sales while we look into a problem.</li>
        <li>Refund guests, for example when an event was fake or misleading.</li>
        <li>Switch off gate accounts, or suspend or close the account.</li>
        <li>Report it to our payment partner, and to the authorities where the law requires.</li>
      </ul>"""),
 ("report", "Report an event or account", "chat", """
      <p>If something on Ganor looks wrong, tell us. Send the event link and what you saw to <a href="mailto:support@ganor.ng">support@ganor.ng</a>, or WhatsApp us on <a href="https://wa.me/2348106742222">0810 674 2222</a>. We read every report.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

# ---------------- TICKET DELIVERY ----------------
page("ticket-delivery", "Ticket delivery policy", "Ganor tickets are digital: how and when you get your ticket, what it contains, and what to do if it doesn’t arrive. Nothing is shipped.",
 "Legal", "Ticket delivery policy", "Every Ganor ticket is digital. It arrives the moment you RSVP or pay, and nothing is ever shipped.",
 [
 ("digital", "Digital tickets only", "ticket", """
      <p>Ganor sells digital tickets and takes free RSVPs for events. We don’t sell or ship physical goods, and there’s no delivery fee.</p>"""),
 ("when", "When you get your ticket", "clock", """
      <ul>
        <li><b>Straight away:</b> as soon as you RSVP, or your payment goes through, your ticket opens on screen with its QR code.</li>
        <li><b>A private link:</b> your ticket also has its own private link, so you can open it again on any phone.</li>
        <li><b>By email:</b> if you give an email address, we send the ticket there too.</li>
        <li><b>On WhatsApp:</b> one tap sends the ticket link to your own WhatsApp, so it’s easy to find on the day.</li>
      </ul>"""),
 ("contents", "What your ticket shows", "qr-code", """
      <p>Your name, the event, its date, time and venue, your ticket type, a QR code and a ticket code. Each ticket works once: the first scan at the gate is the one that counts, so keep your QR code and link to yourself.</p>"""),
 ("gate", "At the event", "scan", """
      <p>Show your ticket on your phone at the gate. The host’s team scans the QR code, or types the ticket code, to check you in. The host and venue decide who is let in and the rules on the day.</p>"""),
 ("missing", "If your ticket doesn’t arrive", "warning", """
      <ul>
        <li>Check your email’s spam or promotions folder, and look for the ticket link in your WhatsApp.</li>
        <li>Ask the host: they can resend your ticket from their dashboard using your phone number.</li>
        <li>If you paid but no ticket appeared, or you can’t reach the host, message us with the phone number or email you used. We’ll find your ticket and send it again.</li>
      </ul>
      <p>If you were charged but no ticket was issued, see the <a href="refunds.html">refund policy</a>.</p>"""),
 ("changes", "If the event changes or is cancelled", "calendar", """
      <p>Your ticket stays valid for the new date or venue. If the host cancels a paid event, you get your money back as set out in the <a href="refunds.html">refund policy</a>.</p>"""),
 ("contact", "Contact", "support", CONTACT),
 ], meta=f"Last updated {UPDATED}")

print("pages written")
