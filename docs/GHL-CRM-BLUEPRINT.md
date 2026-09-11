# ADG Landscaping — GoHighLevel CRM Blueprint

**Goal:** fix ADG's #1 problem — organization. Every lead, quote, job, invoice and payment lives in one place, with automatic reminders so nothing falls through the cracks.

**Stack:** GitHub Pages website → GHL forms/webhooks → GHL pipeline → GHL calendar → GHL invoices & payments (Stripe).

---

## 1. Sub-account setup (30 min)

1. Agency view → **Sub-Accounts → Create** → "ADG Landscaping", Orlando FL, timezone America/New_York.
2. **Settings → Business Profile:** name, address, phone, logo, hours (Mon–Sat 7am–6pm).
3. **Settings → Phone Numbers:** buy a local 407/321 number for SMS + call tracking (register A2P 10DLC — required for texting; takes 1–5 days, start immediately).
4. **Settings → Email Services:** connect her Gmail/Google Workspace or set up LC Email with her domain (add DKIM/SPF records when she has a domain).
5. **Settings → Integrations:** connect Google Business Profile (reviews + GBP messaging), Facebook/Instagram (DMs land in one inbox).

## 2. Payments — Stripe (20 min)

1. **Payments → Integrations → Connect Stripe.** She creates the Stripe account under *her* name/EIN (Gerson should not enter her banking details — she does this step herself).
2. **Payments → Settings:** turn on card + ACH bank payments, enable receipts, set invoice terms (Net 7 by default).
3. **Payments → Products:** create these products (edit prices with her):
   - Weekly Lawn Maintenance — recurring, monthly
   - Bi-Weekly Lawn Maintenance — recurring, monthly
   - Project Deposit — one-time (e.g., $250 or 25%)
   - Irrigation Service Call — one-time
   - Cleanup / Mulch — one-time (custom)
4. **Payments → Payment Links:** create 3 links and paste them into the website config (`PAY_LINKS` in `index.html`):
   - `deposit` → Project Deposit
   - `recurring` → lawn plan (use a link that lets them choose weekly/bi-weekly, or two links)
   - `invoice` → Customer portal / "pay invoice" URL (Payments → Settings → Customer Portal) so existing customers can look up and pay any invoice.
5. **Invoices → Templates:** set default template with logo, terms, late-fee note. Turn on **auto-reminders** (day 0, +3, +7).
6. **Text2Pay:** enable so a crew lead can text a pay link from the mobile app when a job is done.

## 3. Pipeline — "Jobs" (15 min)

Opportunities → Pipelines → create **Jobs** with stages:

| # | Stage | Enters when | Auto-action |
|---|---|---|---|
| 1 | New Lead | Website form / call / DM | Instant SMS + email reply; task for ADG: "Call within 1 hr" |
| 2 | Contacted | Someone replied or ADG called | Book site visit link sent |
| 3 | Site Visit Scheduled | Calendar booking | Reminder 24h + 1h before; reschedule link |
| 4 | Quote Sent | Estimate/proposal sent | Follow-ups day 2, 5, 10 if unsigned |
| 5 | Approved / Deposit Paid | Proposal signed or deposit invoice paid | Move here automatically on payment; task "Schedule job" |
| 6 | Job Scheduled | Job date set on calendar | Customer confirmation + day-before reminder |
| 7 | Job Complete | ADG marks complete | Send final invoice; 24h later → review request |
| 8 | Paid / Won | Invoice paid | Tag `customer`; if recurring, tag `recurring-plan` |
| 9 | Lost | Manual | Tag `lost`, reason note; 90-day re-engagement |

Second pipeline **Recurring Clients** (optional): Active → Paused → Cancelled, for the weekly/bi-weekly accounts.

## 4. Custom fields & tags

**Contact custom fields:** Property Address, Property Type (Residential / Commercial / HOA), Service Interested In (multi-select), Lot Size, Gate Code / Access Notes, Preferred Service Day, Lead Source, Quoted Amount, Job Date.

**Tags:** `website-lead`, `phone-lead`, `gbp-lead`, `fb-lead`, `residential`, `commercial`, `recurring-plan`, `one-time`, `customer`, `lost`, `review-left`, `spanish` (for bilingual comms).

## 5. Forms & calendars

- **Form: "Free Quote Request"** — First, Last, Phone, Email, Property Address, Service Needed, Property Type, Message, TCPA consent checkbox. Copy the embed URL → paste into `GHL_FORM_EMBED_URL` in `index.html`. The site swaps the fallback form for it automatically.
- **Calendar: "Site Visit (30 min)"** — round-robin or single user (her), buffer 30 min, only Mon–Sat 8am–4pm, travel zones Orlando metro. Confirmation + reminder SMS/email on.
- **Calendar: "Job Day"** — service calendar used internally to schedule crews; appointments sync to Google Calendar.

## 6. Automations (workflows)

1. **New Lead Instant Response** — trigger: form submitted / inbound call missed / FB DM. Actions: add tag by source, create opportunity in *New Lead*, SMS ("Hi {{first_name}}, this is ADG Landscaping — got your request! Book your free site visit here: {{calendar_link}}"), email confirmation, internal notification to ADG, task due in 1 hr.
2. **Missed Call Text-Back** — trigger: missed call → SMS within 60 s. Biggest quick win for a solo owner in the field.
3. **Site Visit Reminders** — 24 h and 1 h before appointment; no-show → auto "let's reschedule" SMS + move back to *Contacted*.
4. **Quote Follow-Up** — when moved to *Quote Sent*: day 2 SMS, day 5 email, day 10 SMS "still interested?"; stops when stage changes.
5. **Deposit Paid → Approved** — trigger: invoice/payment received with product = Deposit → move to *Approved*, notify ADG, task "Schedule job".
6. **Job Complete → Invoice + Review** — trigger: stage = Job Complete → send invoice; wait 24 h after paid → Google review request SMS with GBP link; if 5★ add tag `review-left`.
7. **Recurring Plan Billing** — subscriptions auto-charge monthly; failed payment → SMS + email with update-card link; 2nd failure → task for ADG.
8. **Seasonal Campaigns** — Feb: spring cleanup / mulch; May: hurricane-prep palm trimming; Oct: fall refresh. Send to `customer` + `lost` tags.
9. **Bilingual Branch** — if tag `spanish`, send Spanish versions of every message (write both versions in each workflow).

## 7. Mobile app (for the field)

Install the **LeadConnector** app on her phone: inbox, pipeline, calendar, Text2Pay, and invoice creation from the truck. This is what actually fixes "organization" day-to-day — one app instead of texts, notes, and paper.

## 8. Weekly operating rhythm (give her this checklist)

- **Daily (5 min):** clear Conversations inbox; check tasks.
- **Mon:** review *New Lead* and *Quote Sent* columns — anything older than 3 days gets a personal call.
- **Fri:** confirm next week's *Job Scheduled* column; send invoices for *Job Complete*.
- **Monthly:** Reporting → Attribution: leads by source, close rate, revenue collected.

## 9. Rollout plan

| Week | Deliverable |
|---|---|
| 1 | Sub-account, phone number, A2P registration, Stripe connected, products + payment links → website config filled in |
| 2 | Pipeline, fields, tags, quote form embedded, site-visit calendar live |
| 3 | Workflows 1–6 built and tested with test contacts |
| 4 | Import existing customers (CSV), recurring plans set up, review request live, training session with ADG |

## 10. Website ↔ GHL connection checklist

- [ ] `GHL_FORM_EMBED_URL` set (quote form)
- [ ] `PAY_LINKS.invoice` / `.deposit` / `.recurring` set
- [ ] Real phone number + email in config
- [ ] Custom domain pointed at GitHub Pages
- [ ] GBP link in review workflow
- [ ] Test: submit form → lead appears in *New Lead* → SMS received → pay deposit link works
