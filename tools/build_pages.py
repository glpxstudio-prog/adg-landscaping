#!/usr/bin/env python3
"""Generate ADG Landscaping SEO landing pages (one folder per page) + sitemap.

Run from the repo root:  python3 tools/build_pages.py
Edit PAGES below to change copy; edit SITE when the custom domain is live.
"""
import json, os, re, html

SITE = "https://glpxstudio-prog.github.io/adg-landscaping"   # change to https://adglandscapingfl.com once the domain is connected
PHONE_DISPLAY, PHONE_TEL = "(407) 744-8136", "+14077448136"
EMAIL = "adglandscaping.si@gmail.com"
WEBHOOK = "https://services.leadconnectorhq.com/hooks/f2LEZaqBQn15xe3ODXJR/webhook-trigger/gTrHxpPqnd4wLMJkGQsb"
BOOK_HOME = "https://api.leadconnectorhq.com/widget/booking/GahmOIcBkYr3TCYFqPrr"
BOOK_COMM = "https://api.leadconnectorhq.com/widget/booking/mFxWUsD9LI5l9yRflmoO"
GHL_SCRIPTS = '''<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="6ac014d0b9d1919abaf4302b"></script>
<script src="https://link.msgsndr.com/js/external-tracking.js" data-tracking-id="tk_b532270c66e04cebae6fc6b048101c1f"></script>'''

CITY_PAGES = [
  ("landscaping-orlando", "Orlando"),
  ("landscaping-kissimmee", "Kissimmee"),
  ("landscaping-davenport", "Davenport"),
  ("landscaping-haines-city", "Haines City"),
]

PAGES = [
 dict(slug="landscaping-orlando", city="Orlando", county="Orange County",
  title="Lawn Care & Landscaping in Orlando, FL | ADG Landscaping",
  desc="Lawn care, landscaping, cleanups and commercial grounds maintenance in Orlando, FL. Free quotes, online booking and easy card payments. Se habla español.",
  h1_top="Orlando", h1="Lawn Care & Landscaping", h1_tail="you can count on",
  lede="Mowing, edging, cleanups, mulch and landscaping for Orlando homes, rentals and businesses, with a crew that shows up when it says it will.",
  intro=[
   "Orlando yards work hard. Between the summer rainy season, sandy soil and grass that seems to double overnight from June through September, a lawn that looked sharp last week can look overgrown by the weekend. ADG Landscaping keeps Orlando properties on a regular schedule so you don't have to think about it.",
   "We take care of homes across Orlando and Orange County, plus rentals, HOAs and commercial properties. Every job starts with a free quote, and you can book a site visit online in under a minute.",
  ],
  services=["Lawn mowing, edging, trimming and blowing","Seasonal and one-time yard cleanups","Fresh mulch, rock and clean bed edges","Hedge trimming and palm trimming","Florida-friendly plants and sod","Grounds maintenance for apartments, HOAs and businesses"],
  local_h="Orlando lawns, Orlando problems",
  local=[
   ("Rainy-season growth","From late spring through early fall, St. Augustine and Bahia lawns grow fast. Regular visits keep them from getting away from you."),
   ("HOA standards","Many Orlando neighborhoods have HOA rules on lawn height, edges and beds. We keep your property inside the lines."),
   ("Storm prep","Before and during hurricane season we trim back palms and hedges and clear loose debris."),
  ],
  faq=[
   ("How much does lawn care cost in Orlando?","It depends on your lot size and what you need. Send your address through the quote form and we'll reply with a clear price, usually within 24 hours."),
   ("Do you work in my Orlando neighborhood?","We serve Orlando and the surrounding Orange County area. If you're not sure, send your address and we'll confirm."),
   ("Can I book a visit online?","Yes. Use the booking button on this page to pick a time for a free on-site visit."),
   ("¿Hablan español?","¡Sí! Puede llamarnos o escribirnos en español o inglés."),
  ]),
 dict(slug="landscaping-kissimmee", city="Kissimmee", county="Osceola County",
  title="Lawn Care & Landscaping in Kissimmee, FL | ADG Landscaping",
  desc="Lawn care, yard cleanups and landscaping for Kissimmee homes, vacation rentals and HOAs. Free quotes, online booking, se habla español.",
  h1_top="Kissimmee", h1="Lawn Care & Landscaping", h1_tail="for homes and rentals",
  lede="Reliable lawn service for Kissimmee homeowners, vacation-rental owners and HOAs across Osceola County.",
  intro=[
   "Kissimmee has a mix you don't see everywhere: family homes, HOA communities and a lot of short-term rentals that need to look guest-ready every week. ADG Landscaping handles all three.",
   "Whether you live here or manage a rental from out of town, we keep the lawn cut, the beds clean and the curb appeal where it needs to be, and we keep you updated so you don't have to drive over and check.",
  ],
  services=["Lawn mowing, edging and trimming","Vacation-rental and turnover yard cleanups","Mulch, rock and bed refreshes","Hedge, shrub and palm trimming","Overgrown-yard recovery","HOA common areas and commercial properties"],
  local_h="Built around Kissimmee properties",
  local=[
   ("Rental-ready curb appeal","Guests notice the yard first. We keep rental properties sharp between stays, and you can pay online from anywhere."),
   ("Out-of-town owners","Book, approve and pay without being here. We text or email so you know the work is done."),
   ("HOA communities","We keep homes and common areas within HOA lawn and landscaping standards."),
  ],
  faq=[
   ("Do you service vacation rentals in Kissimmee?","Yes. We maintain rental properties and can do cleanups between guests. Tell us about the property in the quote form."),
   ("I don't live in Florida. Can you still take care of my property?","Yes. You can request a quote, book and pay online, and we'll keep you updated by text or email."),
   ("How fast can you start?","Most regular service starts within about a week of approving your quote. Bigger cleanups depend on the size of the job."),
   ("¿Hablan español?","¡Sí! Atendemos en español e inglés."),
  ]),
 dict(slug="landscaping-davenport", city="Davenport", county="Polk County",
  title="Lawn Care & Landscaping in Davenport, FL | ADG Landscaping",
  desc="Lawn care and landscaping for Davenport, FL new builds, vacation homes and communities near US-27 and I-4. Free quotes and online booking.",
  h1_top="Davenport", h1="Lawn Care & Landscaping", h1_tail="for new homes and vacation homes",
  lede="From brand-new builds to vacation homes off US-27 and I-4, ADG Landscaping keeps Davenport properties looking finished.",
  intro=[
   "Davenport has grown fast, and a lot of homes here still have builder-grade landscaping: thin beds, young sod and plants that struggle once the Florida summer hits. Many are also vacation homes whose owners aren't nearby.",
   "ADG Landscaping helps Davenport homeowners and owners get a yard that looks complete and stays that way, with regular service, easy online booking and payments that don't require you to be here.",
  ],
  services=["Lawn mowing, edging and trimming","Upgrades for builder-grade landscaping","Florida-friendly shrubs, palms and sod","Mulch and decorative rock","Vacation-home yard maintenance","Community and commercial grounds"],
  local_h="What Davenport yards need",
  local=[
   ("New-build landscaping","We fill in and upgrade sparse builder landscaping with plants that hold up in Central Florida heat."),
   ("Vacation homes","Keep the property guest-ready while you're away, with updates by text or email."),
   ("Growing communities","We work with HOAs and community managers on common-area maintenance."),
  ],
  faq=[
   ("Can you upgrade the landscaping on my new Davenport home?","Yes. We can add beds, plants, rock and mulch to builder landscaping. Request a quote and tell us what you have in mind."),
   ("Do you maintain vacation homes in Davenport?","Yes. We keep vacation homes on a regular schedule, and you can approve and pay online."),
   ("What areas near Davenport do you cover?","Davenport and the surrounding area along US-27 and I-4. Send your address and we'll confirm."),
   ("¿Hablan español?","¡Sí! Puede escribirnos o llamarnos en español."),
  ]),
 dict(slug="landscaping-haines-city", city="Haines City", county="Polk County",
  title="Lawn Care & Landscaping in Haines City, FL | ADG Landscaping",
  desc="Lawn care, yard cleanups and landscaping in Haines City, FL. Homes, rentals and commercial properties in Polk County. Free quotes, se habla español.",
  h1_top="Haines City", h1="Lawn Care & Landscaping", h1_tail="in Polk County",
  lede="Dependable lawn care and landscaping for Haines City homes, rentals and businesses.",
  intro=[
   "Haines City homeowners and landlords need a lawn crew they can actually rely on, one that shows up on schedule, does the job right and makes it easy to pay.",
   "ADG Landscaping covers Haines City and nearby Polk County with regular lawn service, cleanups and landscaping, plus grounds maintenance for rental and commercial properties.",
  ],
  services=["Lawn mowing, edging and trimming","Overgrown-yard and rental turnover cleanups","Mulch, rock and bed edging","Hedge and palm trimming","Florida-friendly plants and sod","Commercial and rental property grounds"],
  local_h="Lawn care that fits Haines City",
  local=[
   ("Rental properties","We get neglected yards back in shape between tenants and keep them that way."),
   ("Regular service","Same crew on a set route, so your yard never goes weeks without attention."),
   ("Easy to pay","Pay by card online. No chasing invoices, no checks in the mail."),
  ],
  faq=[
   ("Do you offer lawn service in Haines City?","Yes. Haines City is one of our regular service areas. Send your address for a free quote."),
   ("Can you clean up a yard that's really overgrown?","Yes. We do one-time cleanups and haul-away, then can keep it on a regular schedule."),
   ("Do you work with landlords and property managers?","Yes. We maintain rental and commercial properties and can bill online."),
   ("¿Hablan español?","¡Sí! Hablamos español e inglés."),
  ]),
 dict(slug="commercial-landscaping", city=None, county=None, commercial=True,
  title="Commercial Landscaping & Grounds Maintenance in Central Florida | ADG Landscaping",
  desc="Commercial grounds maintenance for apartment complexes, HOAs, offices and retail in Orlando, Kissimmee, Davenport and Haines City. Written proposals, one point of contact.",
  h1_top="Central Florida", h1="Commercial Grounds Maintenance", h1_tail="for apartments, HOAs & businesses",
  lede="Apartment complexes, HOA communities, offices and retail properties across Orlando, Kissimmee, Davenport and Haines City.",
  intro=[
   "Property managers and boards need a landscaping vendor who shows up when scheduled, keeps the grounds tenant-ready and is easy to reach when something comes up. That's how ADG Landscaping works.",
   "We provide written proposals with a clear scope, keep a regular maintenance schedule and give you one point of contact, the owner, in English or Spanish.",
  ],
  services=["Apartment complex grounds and common areas","HOA entrances, medians, ponds and amenity areas","Office, retail and business properties","Mulch, rock and seasonal refreshes","Hedge, shrub and palm trimming","Storm-prep cutbacks and cleanups"],
  local_h="Why property managers choose ADG",
  local=[
   ("Written proposals","Clear scope and pricing your board or management company can review and approve."),
   ("One point of contact","Talk directly with the owner, not a call center, in English or Spanish."),
   ("Reliable schedule","Regular visits on a set schedule, with the grounds kept within your community's standards."),
  ],
  faq=[
   ("What types of commercial properties do you maintain?","Apartment complexes, HOA communities, offices, retail and other business properties in Orlando, Kissimmee, Davenport and Haines City."),
   ("Do you provide written proposals for bids?","Yes. Book a consultation or request a bid and we'll walk the property and send a written proposal."),
   ("Do you offer annual or multi-year contracts?","Yes. We can price ongoing maintenance on an annual or multi-year basis."),
   ("¿Atienden en español?","¡Sí! Atendemos a administradores y juntas en español o inglés."),
  ]),
]

PIN = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5z"/></svg>'
CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#78b52b" stroke-width="2.6"><path d="M20 6 9 17l-5-5"/></svg>'
LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="16" fill="{bg}"/><path d="M32 50c0-14 6-24 18-30-2 14-8 24-18 30zM32 50c0-14-6-24-18-30 2 14 8 24 18 30z" fill="{fg}"/></svg>'
PHONE_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'

e = html.escape

def area_links(current):
    items = []
    for slug, city in CITY_PAGES:
        if slug == current: continue
        items.append(f'<a class="area" href="../{slug}/"><i>{PIN}</i><h3>{city}</h3><p>Lawn care &amp; landscaping in {city} →</p></a>')
    if current != "commercial-landscaping":
        items.append(f'<a class="area" href="../commercial-landscaping/"><i>{PIN}</i><h3>Commercial</h3><p>Apartments, HOAs &amp; businesses →</p></a>')
    return "\n      ".join(items)

def schema(p):
    url = f"{SITE}/{p['slug']}/"
    biz = {"@context":"https://schema.org","@type":"LandscapingBusiness","name":"ADG Landscaping","url":SITE+"/",
           "telephone":"+1-407-744-8136","email":EMAIL,"knowsLanguage":["en","es"],
           "areaServed":[f"{p['city']}, FL"] if p.get("city") else ["Orlando, FL","Kissimmee, FL","Davenport, FL","Haines City, FL"]}
    svc = {"@context":"https://schema.org","@type":"Service","name":p["h1"] + (f" in {p['city']}, FL" if p.get("city") else ""),
           "provider":{"@type":"LandscapingBusiness","name":"ADG Landscaping"},"areaServed":biz["areaServed"],"url":url}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]}
    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":p["h1_top"] if p.get("city") else "Commercial","item":url}]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (biz, svc, faq, crumbs))

def page(p):
    commercial = p.get("commercial", False)
    url = f"{SITE}/{p['slug']}/"
    place = p["city"] or "Central Florida"
    book = BOOK_COMM if commercial else BOOK_HOME
    book_label = "Book a consultation" if commercial else "Book a free site visit"
    ptype_default = "Apartment complex" if commercial else "Home"
    ptype_opts = "".join(f'<option{" selected" if o==ptype_default else ""}>{o}</option>' for o in ["Home","Apartment complex","HOA / community","Office / retail / business","Other commercial"])
    intro = "".join(f"<p>{e(t)}</p>" for t in p["intro"])
    services = "".join(f"<li>{CHECK}<span>{e(s)}</span></li>" for s in p["services"])
    local = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h,t in p["local"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in p["faq"])
    source = f"Website - {p['slug']}"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
{schema(p)}
</head>
<body id="top">

<div class="topbar">
  <div class="wrap">
    <div class="ask">Lawn care &amp; landscaping in {e(place)}. <span>Free quotes, fast replies.</span></div>
    <div style="display:flex;gap:14px;align-items:center;margin-left:auto">
      <span class="es">Se habla español</span>
      <a href="mailto:{EMAIL}">{e(EMAIL)}</a>
    </div>
  </div>
</div>

<header>
  <div class="wrap" style="position:relative">
    <a href="../" class="logo" aria-label="ADG Landscaping home">{LOGO.format(bg="#24470f", fg="#8cc63f")}<span>ADG Landscaping<small>Central Florida</small></span></a>
    <nav id="menu">
      <a href="../">Home</a>
      <a href="../#services">Services</a>
      <a href="../#work">Our Work</a>
      <a href="../commercial-landscaping/">Commercial</a>
      <a href="../#areas">Areas</a>
      <a href="#book">Book</a>
      <a href="#quote">Contact</a>
    </nav>
    <a class="hcall" href="tel:{PHONE_TEL}"><i>{PHONE_ICON}</i><span>{PHONE_DISPLAY}</span></a>
    <a class="btn btn-lime head-cta" href="#quote">Free Quote</a>
    <button class="menu-btn" aria-label="Open menu" onclick="document.getElementById('menu').classList.toggle('open')"><span></span><span></span><span></span></button>
  </div>
</header>

<main>
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> <span>/</span> {e(p["h1_top"] if p.get("city") else "Commercial")}</div>
    <h1><span>{e(p["h1_top"])}</span> <b>{e(p["h1"])}</b> {e(p["h1_tail"])}</h1>
    <p class="tag">{e(p["lede"])}</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-white" href="#quote">{"Request a bid" if commercial else "Get my free quote"}</a><a class="btn btn-lime" href="{book}" target="_blank" rel="noopener">{book_label}</a></div>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div class="prose">
      <span class="eyebrow">{e(p["county"] or "Orlando · Kissimmee · Davenport · Haines City")}</span>
      <h2>{"Commercial landscaping" if commercial else "Lawn care in " + e(p["city"])} <b>done right</b></h2>
      {intro}
    </div>
    <div class="panel">
      <h3>{"What we maintain" if commercial else "Services in " + e(p["city"])}</h3>
      <ul class="checks">{services}</ul>
      <a class="btn btn-lime" style="width:100%;margin-top:18px" href="#quote">Request a {"bid" if commercial else "free quote"}</a>
    </div>
  </div>
</section>

<section class="svc-sec">
  <div class="wrap">
    <div class="center"><h2>{e(p["local_h"])}</h2></div>
    <div class="grid3">{local}</div>
  </div>
</section>

<section id="quote">
  <div class="wrap two" style="margin-top:0">
    <div class="panel" id="book">
      <h3>{book_label}</h3>
      <p class="sub">{"45-minute consultation, weekdays 8am–5pm." if commercial else "30-minute visit. We walk the property and send a written quote."}</p>
      <a class="btn btn-lime" style="width:100%" href="{book}" target="_blank" rel="noopener">Pick a time →</a>
      <div class="contact-list">
        <a href="tel:{PHONE_TEL}"><i>📞</i>{PHONE_DISPLAY}</a>
        <a href="mailto:{EMAIL}"><i>✉️</i>{e(EMAIL)}</a>
        <div><i>🕗</i>Mon–Sat · Se habla español</div>
      </div>
    </div>
    <div class="panel">
      <h3>{"Request a commercial bid" if commercial else "Get a free quote in " + e(p["city"])}</h3>
      <p class="sub">We reply within one business day.</p>
      <form class="full" onsubmit="return sendLead(event)">
        <div class="row">
          <div><label for="fn">First name</label><input id="fn" name="first_name" required></div>
          <div><label for="ln">Last name</label><input id="ln" name="last_name" required></div>
        </div>
        <div class="row">
          <div><label for="ph">Phone</label><input id="ph" name="phone" type="tel" required></div>
          <div><label for="em">Email</label><input id="em" name="email" type="email" required></div>
        </div>
        <label for="addr">Property address</label><input id="addr" name="address" placeholder="Street, {e(p["city"] or "city")}">
        <div class="row">
          <div><label for="ptype">Property type</label><select id="ptype" name="property_type">{ptype_opts}</select></div>
          <div><label for="co">Company / property name <span style="font-weight:500;color:var(--mute)">(optional)</span></label><input id="co" name="company_name"></div>
        </div>
        <label for="msg">What do you need?</label><textarea id="msg" name="message" placeholder="Tell us about the property and what you'd like done."></textarea>
        <input type="hidden" name="service" value="{"Commercial / HOA" if commercial else "Lawn maintenance"}">
        <button class="btn btn-lime" type="submit">Send my request</button>
        <p class="fine">By submitting, you agree to be contacted by ADG Landscaping by phone, text, or email about your request. Standard message rates may apply. Reply STOP to opt out.</p>
      </form>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap" style="max-width:860px">
    <div class="center"><span class="eyebrow">FAQ</span><h2>{e(place)} <b>questions</b></h2></div>
    <div style="margin-top:28px">{faq}</div>
  </div>
</section>

<section class="areas">
  <div class="wrap">
    <span class="eyebrow">More areas</span><h2>We also serve</h2>
    <div class="area-grid">
      {area_links(p["slug"])}
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="cols">
      <div><a href="../" class="logo">{LOGO.format(bg="#8cc63f", fg="#24470f")}<span>ADG Landscaping<small>Central Florida</small></span></a>
        <p style="margin-top:16px;max-width:34ch;font-size:15px">Reliable lawn care and landscaping for homes and businesses across Central Florida.</p></div>
      <div><h4>Services</h4><ul><li><a href="../#services">Lawn maintenance</a></li><li><a href="../#services">Landscaping</a></li><li><a href="../#services">Cleanups</a></li><li><a href="../commercial-landscaping/">Commercial &amp; HOA</a></li></ul></div>
      <div><h4>Areas</h4><ul>{"".join(f'<li><a href="../{s}/">{c}</a></li>' for s,c in CITY_PAGES)}</ul></div>
      <div><h4>Contact</h4><ul><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li><a href="mailto:{EMAIL}">{e(EMAIL)}</a></li><li>Mon–Sat</li><li>Se habla español</li><li><a href="../#pay">Pay online</a></li></ul></div>
    </div>
    <div class="copy"><span>© <span id="yr"></span> ADG Landscaping. All rights reserved.</span><span>Website by GLPX Studio</span></div>
  </div>
</footer>

<div class="sticky-call"><a class="btn btn-white" style="box-shadow:var(--shadow)" href="tel:{PHONE_TEL}">Call</a><a class="btn btn-lime" href="#quote">Free quote</a></div>

<script>
document.getElementById('yr').textContent = new Date().getFullYear();
async function sendLead(ev){{
  ev.preventDefault();
  const f = ev.target, b = f.querySelector('button');
  const d = Object.fromEntries(new FormData(f).entries()); d.source = {json.dumps(source)};
  b.disabled = true; b.textContent = 'Sending…';
  try {{
    await fetch({json.dumps(WEBHOOK)}, {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(d)}});
    f.outerHTML = '<div class="qdone"><h3>Thanks' + (d.first_name ? ', ' + d.first_name : '') + '! 🌿</h3><p style="color:var(--body)">We got your request and will reach out within one business day.</p></div>';
  }} catch(err) {{ b.disabled = false; b.textContent = 'Send my request'; alert('Something went wrong. Please call {PHONE_DISPLAY}.'); }}
  return false;
}}
</script>
{GHL_SCRIPTS}
</body>
</html>
'''

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for p in PAGES:
        d = os.path.join(root, p["slug"]); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as fh: fh.write(page(p))
    urls = [SITE + "/"] + [f"{SITE}/{p['slug']}/" for p in PAGES]
    with open(os.path.join(root, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        fh.write("".join(f"  <url><loc>{u}</loc></url>\n" for u in urls))
        fh.write("</urlset>\n")
    with open(os.path.join(root, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(PAGES), "pages")

if __name__ == "__main__":
    main()
