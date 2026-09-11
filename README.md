# ADG Landscaping — Website

Marketing site for **ADG Landscaping** (Orlando / Central Florida). Single-file static site, hosted on GitHub Pages.

## Edit content
Everything is in `index.html`. Config values live at the bottom of the file in the `ADG` object:

| Key | What to put there |
|---|---|
| `phoneDisplay` / `phoneTel` | Business phone (updates every phone link on the page) |
| `email` | Business email |
| `GHL_FORM_EMBED_URL` | GoHighLevel form embed URL → replaces the fallback quote form |
| `PAY_LINKS.invoice` | GHL / Stripe link for paying an invoice |
| `PAY_LINKS.deposit` | GHL / Stripe payment link for a project deposit |
| `PAY_LINKS.recurring` | GHL subscription link for monthly lawn plans |
| `FALLBACK_FORM_ENDPOINT` | Optional webhook (e.g., GHL inbound webhook) for the fallback form |

Search the file for **"placeholder"** to find copy, reviews, photos, license # and stats that need real content.

## Custom domain
Settings → Pages → Custom domain → enter `adglandscaping.com` (or her domain), then add the DNS records GitHub shows. Commit the generated `CNAME` file.

## CRM
Lead capture, scheduling, invoicing and payments run through GoHighLevel. See `docs/GHL-CRM-BLUEPRINT.md`.
