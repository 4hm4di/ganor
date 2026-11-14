"""Writes the inner pages (docs, legal) into src/ from the content below.
Run: python3 tools/pages.py && python3 tools/build.py
"""
from pathlib import Path
SRC = Path(__file__).resolve().parent.parent / "src"
UPDATED = "14 November 2026"

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
page("docs", "Docs", "How Ganor works for hosts, gate teams, guests and businesses: accounts, free RSVP events and plans, paid tickets, fees, gate check-in and getting help.",
 "Docs", "How Ganor works", "Everything you need to host an event, run the gate, get a ticket or get your business found. Short answers, in plain words.",
 [
 ("start", "Getting started", "compass", """
      <p>Ganor is where you find what’s happening near you. Hosts create an event, share one link, take free RSVPs or sell tickets, and scan guests in at the gate. Guests open the link, get their ticket with a QR code, and show it at the door.</p>
      <div class="callout"><b>Ganor opens soon.</b> These docs describe how it works when it opens. <a href="./#join">Join the list</a> and we’ll message you on WhatsApp the day you can start.</div>
      <h3>Who Ganor is for</h3>
      <ul>
        <li><b>Hosts:</b> anyone running a gathering, from conferences, summits, trade fairs and cooperative launches to lectures, campus events and shows.</li>
        <li><b>Gate teams:</b> the people a host trusts to scan guests in.</li>
        <li><b>Guests:</b> anyone looking for something to go to, or holding a ticket.</li>
        <li><b>Businesses:</b> shops, hospitals, restaurants, hotels and more, listed on Ganor Places.</li>
      </ul>
      <p>Hosts and gate teams work in the Ganor app at <b>app.ganor.ng</b>. Guests don’t need an account.</p>"""),
 ("account", "Your host account", "user", """
      <h3>Signing up</h3>
      <p>Create your host account at <b>app.ganor.ng</b> with your email and a password, then open the link we email you to confirm your address. Or tap <b>Continue with Google</b> to sign up and sign in with your Google account.</p>
      <h3>Your host profile</h3>
      <p>Your name, logo and a few lines about you appear on your event pages. Add how guests can reach you: a <b>WhatsApp or call number is required before you can publish</b>. Email, website and Instagram are optional.</p>
      <h3>Staying safe</h3>
      <ul>
        <li><b>One device at a time.</b> Signing in on a new phone or computer signs your account out everywhere else.</li>
        <li><b>Automatic sign-out.</b> After 30 minutes without activity, or when you close the browser, you’re signed out.</li>
        <li><b>Your bank account</b> for payouts is added once in your dashboard and checked before money is paid out.</li>
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
      <p>Before you can publish, Ganor checks that your profile has a WhatsApp or call number, that a paid event has at least one ticket type, and that a paid RSVP plan has been paid. You can change the details after you publish; tell your guests about any change to the date, time or venue.</p>"""),
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
        <li>A paid plan is paid before the event is published, and covers that one event.</li>
        <li>On the Free plan, RSVPs close when 30 guests have registered. You can upgrade from your event page at any time.</li>
        <li>The Free plan includes one gate account for the event. Paid plans can have as many as you need.</li>
        <li>Your dashboard shows what each plan includes before you choose.</li>
      </ul>
      <h3>Your questions</h3>
      <p>Add questions to the RSVP form, such as organisation, job title or t-shirt size, and mark which ones are required. You can download your guest list with their answers.</p>"""),
 ("tickets", "Paid tickets", "ticket", """
      <p>A paid event can have as many ticket types as you need, for example Regular, VIP and Table for 10. For each one you set:</p>
      <ul>
        <li><b>The price.</b> Every paid ticket costs at least <b>₦1,000</b>. Paid events can’t have free tickets; for a free event, create a Free RSVP event.</li>
        <li><b>How many</b> are available, and the most one person can buy in an order.</li>
        <li><b>What’s included</b>, such as front rows, lunch or a certificate (optional).</li>
      </ul>
      <p>You can pause or reopen any ticket type at any time. Once a ticket type has sold, its price is locked; add a new ticket type for a different price.</p>
      <div class="callout"><b>Online payments are switching on soon.</b> You can set up and publish paid events now; the event page shows that ticket sales open soon until card, transfer and USSD payments go live.</div>"""),
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
      <h3>Payouts</h3>
      <p>Add the bank account for your payouts in your dashboard. Ganor checks it before any money is paid out. Your dashboard shows your sales, your take-home and your payout details, so you always know where your money is.</p>"""),
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
      <p>Your ticket appears straight away with its QR code. Keep it on your phone (a screenshot works) and show it at the gate. Each ticket gets one person in, once.</p>
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
 ("places", "For businesses", "shop", """
      <p>Ganor Places helps people find the businesses they can trust nearby: phone and electronics shops, fabric sellers, markets, hospitals, pharmacies, restaurants, hotels, event halls, salons, mechanics, schools, coworking spaces, tech hubs, gyms, football pitches and mini stadiums, parks and more.</p>
      <p>Every listing is checked in person, with directions and a working phone number. Ganor Places comes after events. To be among the first listed, <a href="./#join">join the list</a> and choose <b>A local business</b>.</p>"""),
 ("help", "Get help", "support", f"""
      <p>We answer on WhatsApp first.</p>
      {CONTACT}"""),
 ])

# ---------------- TERMS ----------------
page("terms", "Terms of use", "The terms for using Ganor as a host, a gate team member, a guest or a business.",
 "Legal", "Terms of use", "The rules for using Ganor, written to be read. Please read them before you host, buy or list on Ganor.",
 [
 ("about", "About these terms", "doc", """
      <p>These terms apply when you use ganor.ng, the Ganor app at app.ganor.ng or any Ganor service (together, “Ganor”). “We” and “us” mean Ganor. “You” means anyone using Ganor: a <b>host</b> who runs an event, a <b>gate team member</b> who scans tickets for a host, a <b>guest</b> who RSVPs or buys a ticket, or a <b>business</b> listed on Ganor Places.</p>
      <p>By using Ganor you agree to these terms, our <a href="privacy.html">privacy policy</a> and our <a href="refunds.html">refund policy</a>.</p>"""),
 ("who", "Who can use Ganor", "users", """
      <ul>
        <li>Hosts and businesses must be at least 18 and able to enter a contract in Nigeria.</li>
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
        <li>Your ticket and its QR code appear as soon as you RSVP or pay. Keep your QR code to yourself: each ticket works once, and the first scan is the one that counts.</li>
        <li>One phone number can RSVP once to each free event.</li>
        <li>Questions about the event, changes and refunds go to the host. If you can’t reach them, message us.</li>
        <li>Don’t resell tickets for more than you paid or copy tickets. The host may refuse entry for copied or resold tickets.</li>
        <li>The host and venue decide who is let in and the rules on the day.</li>
      </ul>"""),
 ("fees", "Fees and payments", "percent", """
      <p><b>Paid tickets:</b> the Ganor fee is 6% of the ticket price + ₦100 per ticket, with card and transfer charges included. Paid tickets cost at least ₦1,000. The host chooses whether the buyer pays the fee at checkout or the host absorbs it.</p>
      <p><b>Free RSVP events:</b> the Free plan costs nothing and allows up to 30 guests. Larger free events use a paid plan (Basic, Standard, Pro or Premium), priced per event and shown before you choose. A plan is paid before the event is published and covers that one event only. Plan fees aren’t refundable once the event is published, except where the law requires.</p>
      <p>We may change our fees. Changes never apply to tickets or plans already paid for, and we’ll tell hosts before they take effect.</p>
      <p>Payments are processed by our licensed payment partners. We don’t store card details. Ticket money, minus the Ganor fee where the host absorbs it, is paid out to the host’s bank account after we’ve checked it.</p>"""),
 ("not-allowed", "What’s not allowed", "shield", """
      <ul>
        <li>Fake, misleading or duplicate events or listings, including misusing the Halal-friendly label.</li>
        <li>Events or businesses that break the law, or that promote hate, violence or harm.</li>
        <li>Selling tickets you don’t have the right to sell.</li>
        <li>Collecting payments outside Ganor for tickets advertised on Ganor.</li>
        <li>Fake RSVPs, or filling an event’s places to keep real guests out.</li>
        <li>Sharing one account between people to get round the one-device rule.</li>
        <li>Trying to break, copy or overload Ganor, or to get into other people’s accounts.</li>
      </ul>
      <p>We may remove events or listings, hold payouts while we check a problem, or suspend or close accounts that break these terms. Where we can, we’ll tell you why.</p>"""),
 ("places", "Ganor Places", "shop", """
      <p>Businesses on Ganor Places must give true details and keep them up to date. We check listings in person, but we can’t promise the quality of any business’s goods or services. Deal with businesses carefully, as you would anywhere.</p>"""),
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
      <h3>When you join the list</h3>
      <p>Your name, your WhatsApp number or email (you choose), whether you’re a host, a guest or a business, and the kind of event you’re interested in, if you tell us.</p>
      <h3>When you use Ganor</h3>
      <ul>
        <li><b>Host account:</b> your name and email, and your password (stored scrambled, so no one can read it). If you sign in with Google, Google shares your name and email address with us.</li>
        <li><b>Host profile:</b> your logo, a few lines about you, and your contact details: WhatsApp or call number, and email, website and Instagram if you add them. These are shown on your event pages.</li>
        <li><b>Guests:</b> the name and phone number on each RSVP or ticket, your email if the host asks for it, your answers to the host’s questions, what you got and when it was scanned at the gate.</li>
        <li><b>Gate team:</b> each gate account’s name and username, which events it can check in, when it signed in, and the tickets it scanned.</li>
        <li><b>Ratings:</b> if you agreed at checkout, the star rating and comment you leave after an event, the name you choose to show, and whether your ticket was scanned.</li>
        <li><b>Hosts and businesses:</b> event or business details, and the bank account for payouts.</li>
        <li><b>Payments:</b> handled by our licensed payment partners. We receive confirmation of payment, not your card details.</li>
      </ul>
      <h3>Cookies</h3>
      <p>We don’t use advertising or tracking cookies. The Ganor app uses only the cookies it needs to work: keeping you signed in (they end when you close your browser), signing you out after 30 minutes without activity, keeping a gate phone signed in, and showing a short message after you save something. The ganor.ng website stores one small note in your browser so the opening animation only plays once per visit.</p>"""),
 ("use", "How we use it", "settings", """
      <ul>
        <li>To run your account, keep it to one device at a time, and keep it secure.</li>
        <li>To deliver tickets and check guests in at the gate.</li>
        <li>To process payments and pay hosts.</li>
        <li>To send you one WhatsApp message after an event asking you to rate it, only if you ticked that box at checkout. Reply STOP and we won’t send another.</li>
        <li>To show guests’ ratings of events and hosts, so people can choose events with confidence.</li>
        <li>To tell you when Ganor opens, if you joined the list.</li>
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
      <p>We keep your data only as long as we need it: account data while your account is open, ticket and payment records for as long as the law requires, gate sign-in records for up to a week after they end, and waitlist details until Ganor opens or until you ask us to delete them. Rating links and the records of who agreed to rating messages are deleted 6 months after ratings for that event close. Published reviews stay up until you ask us to remove them; they are linked to a coded reference, not your phone number.</p>"""),
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

print("pages written")
