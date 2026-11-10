# Ganor emails

Email templates in the Ganor brand. They are built by `tools/emails.py`. Edit that script, not the HTML, then run:

```
python3 tools/emails.py
```

| File | What it's for |
| --- | --- |
| `auto-reply.html` / `.txt` | Automatic reply from support@ganor.ng |
| `general.html` | Layout for everyday emails, with the signature |
| `signatures.html` | Two signatures: Ganor Support and Ahmad Abdallah. Open it in a browser, copy one, and paste it into your mail app's signature settings |
| `ticket-confirmation.html` / `.txt` | Sent after someone buys a ticket |
| `newsletter.html` | Marketing email, with unsubscribe links |
| `preview/` | The same emails filled with sample data, for viewing in a browser |

## How they're built

- Table layout with inline styles, 600px wide. On phones the columns stack.
- Images are PNGs from `https://ganor.ng/assets/email/` (made by `tools/email_assets.py`). They only show once the site is live on ganor.ng.
- Fonts are Bricolage Grotesque and Inter. Apple Mail and iOS load them; Gmail and Outlook fall back to Helvetica or Arial.

## Merge tags

Tags look like `{{first_name}}`. Change them to your sending tool's syntax. For Brevo, `{{first_name}}` becomes `{{ contact.FIRSTNAME }}`, and data from your app becomes `{{ params.event_name }}`.

**Everyone:** `first_name`

**Ticket confirmation:**
- Event: `event_name`, `event_date`, `event_time`, `gate_time`, `venue_name`, `venue_address`, `map_url`, `event_banner_url` (1020×420 works best)
- Host: `host_name`, `host_logo_url` (square), `host_phone`, `host_email`
- Ticket: `ticket_type`, `ticket_qty`, `holder_name`, `ticket_code`, `qr_image_url` (a PNG, at least 368px), `ticket_url`, `calendar_url`
- Payment: `order_id`, `paid_at`, `subtotal`, `fee`, `total`, `payment_method`

**Newsletter:** `unsubscribe_url`, `preferences_url`, `event_url`. The three events in it are examples; replace them each time you send.

**Everyday email:** `subject`, `preheader`, `button_label`, `button_url`, `sender_name`, `sender_role`

## Setting up the auto-reply

1. Sign in to webmail for support@ganor.ng.
2. Go to Settings, then Autoresponder (it may be called Vacation or Auto reply).
3. Subject: `We've got your message`.
4. If HTML is allowed, paste `auto-reply.html`. If not, paste `auto-reply.txt`.
5. Set it to reply once per sender per day, so it doesn't send a reply to every message.

## Before sending marketing email

Only send to people who signed up. Every newsletter must include the unsubscribe link. Send from a tool like Brevo, not from your inbox, so Gmail doesn't mark it as spam.
