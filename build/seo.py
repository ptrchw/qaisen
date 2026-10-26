"""SEO settings for the services site: page titles, descriptions, keywords,
canonical URLs, structured data (JSON-LD), sitemap.xml and robots.txt.

Change SITE_URL and BIZ_NAME once the domain and company name are final;
every page, the sitemap and the structured data update on the next build.
"""
import html, json, re

SITE_URL = "https://qaisen.com"         # final domain, no trailing slash
BIZ_NAME = "QAISEN"                    # TODO: registered name, e.g. "Qaisen Pte. Ltd.", once incorporated
BRAND = "QAISEN"                       # brand used in page titles
LIVE = False   # TODO: set True at launch. While False, search engines are told not to index the site
FOUNDER = "Peter Chow"
LINKEDIN = "https://www.linkedin.com/in/ptrchw/"

# fname: (title, description, keywords used to write the copy above; kept for reference)
PAGES = {
    "index.html": (
        f"UX & Product Innovation Consultant in Singapore | {BRAND}",
        "Singapore UX and product innovation consultancy: fixed-price UX audits, design and discovery sprints, and GenAI workshops for startups, SMEs and ICT teams.",
        ["UX consultant Singapore", "UX consultancy Singapore", "product innovation consultant", "GenAI workshops", "UX audit", "design sprint"],
    ),
    "ux-audit.html": (
        f"UX Audit for Websites & Apps in Singapore | {BRAND}",
        "Find out why users get stuck. An expert UX audit of three key journeys, backed by your customer feedback, plus a workshop to rank every fix. From S$5,000.",
        ["UX audit Singapore", "usability audit", "heuristic evaluation", "website UX review", "app UX review", "usability testing"],
    ),
    "discovery-sprint.html": (
        f"Design Sprint & Product Discovery in Singapore | {BRAND}",
        "Know what's worth building before you build it: a 4-day Design Sprint or a Discovery Sprint with user interviews and real-user testing. From S$5,900.",
        ["design sprint Singapore", "product discovery", "discovery sprint", "validate a product idea", "prototype testing", "user research"],
    ),
    "workshops.html": (
        f"GenAI & Design Thinking Workshops for Teams | {BRAND}",
        "Hands-on GenAI workshops that train your team to use AI for design thinking and rapid prototyping on real challenges. Up to 10 people. From S$4,500.",
        ["GenAI workshop Singapore", "AI training for teams", "design thinking workshop", "rapid prototyping workshop", "corporate AI training"],
    ),
    "about.html": (
        f"Peter Chow, UX Architect in Singapore | {BRAND}",
        "Peter Chow is a Singapore UX architect and product innovation consultant with 20+ years across government, enterprise, fintech and education.",
        ["Peter Chow UX", "UX architect Singapore", "product innovation consultant", "design thinking"],
    ),
    "contact.html": (
        f"Book a 20-Minute UX Consultation | {BRAND}",
        "Book a free 20-minute call to find the right UX audit, sprint or GenAI workshop for your team, or message on WhatsApp or email. Based in Singapore.",
        ["UX consultation Singapore", "book a UX consultant", "contact"],
    ),
}

ORG_ID = SITE_URL + "/#org"
PERSON_ID = SITE_URL + "/about.html#peter"

SERVICES = [
    # (page, name, serviceType, description, lowPrice, highPrice)
    ("ux-audit.html", "UX Audit", "UX audit and usability review",
     "Expert heuristic review and flow audit of three key journeys, backed by customer feedback, with a prioritisation workshop.", 5000, 7500),
    ("discovery-sprint.html", "Discovery & Design Sprints", "Design sprint and product discovery",
     "A 4-day Design Sprint or a Discovery Sprint of up to 5 weeks to test ideas with real users before you build.", 5900, 8700),
    ("workshops.html", "Applied AI for Design Thinking and Rapid Prototyping workshops", "GenAI and design thinking training",
     "Hands-on, in-house workshops of one to three days for up to 10 people.", 4500, 10500),
]

CRUMB_NAMES = {
    "ux-audit.html": "UX Audit", "discovery-sprint.html": "Sprints", "workshops.html": "Workshops",
    "about.html": "About", "contact.html": "Contact",
}


def url(fname):
    return SITE_URL + "/" if fname == "index.html" else f"{SITE_URL}/{fname}"


def _text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()


def _org():
    return {
        "@type": "ProfessionalService", "@id": ORG_ID, "name": BIZ_NAME, "url": url("index.html"),
        "description": PAGES["index.html"][1],
        "areaServed": {"@type": "Country", "name": "Singapore"},
        "address": {"@type": "PostalAddress", "addressCountry": "SG"},
        "founder": {"@id": PERSON_ID},
        "knowsAbout": ["User experience design", "UX audit", "Usability testing", "Design sprint",
                       "Product discovery", "Design thinking", "Generative AI", "Rapid prototyping"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Fixed-scope services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": url(p)}} for p, n, *_ in SERVICES]},
    }


def _person():
    return {
        "@type": "Person", "@id": PERSON_ID, "name": FOUNDER, "jobTitle": "UX Architect",
        "url": url("about.html"), "sameAs": [LINKEDIN], "worksFor": {"@id": ORG_ID},
        "knowsAbout": ["UX architecture", "Product innovation", "Design thinking", "Generative AI", "Experience design"],
    }


def jsonld(fname, body):
    graph = []
    if fname == "index.html":
        graph += [_org(), _person(), {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": url("index.html"),
                                      "name": BRAND, "publisher": {"@id": ORG_ID}, "inLanguage": "en-SG"}]
    else:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": url("index.html")},
            {"@type": "ListItem", "position": 2, "name": CRUMB_NAMES.get(fname, fname), "item": url(fname)}]})
    for p, name, stype, desc, lo, hi in SERVICES:
        if p == fname:
            graph.append({"@type": "Service", "name": name, "serviceType": stype, "description": desc, "url": url(p),
                          "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "Singapore"},
                          "offers": {"@type": "AggregateOffer", "priceCurrency": "SGD", "lowPrice": lo, "highPrice": hi}})
    if fname == "about.html":
        graph.append({"@type": "ProfilePage", "url": url(fname), "mainEntity": _person()})
    faqs = re.findall(r"<summary>(.*?)</summary>\s*<div class=\"answer\">(.*?)</div>", body, re.S)
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": _text(q), "acceptedAnswer": {"@type": "Answer", "text": _text(a)}} for q, a in faqs]})
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{data}\n</script>\n'


def head_extra(fname):
    u = html.escape(url(fname))
    noindex = '' if LIVE else '<meta name="robots" content="noindex, nofollow">\n'
    return (noindex + f'<link rel="canonical" href="{u}">\n<meta property="og:url" content="{u}">\n'
            f'<meta property="og:site_name" content="{html.escape(BRAND)}">\n<meta property="og:locale" content="en_SG">\n'
            '<meta name="twitter:card" content="summary">\n')


def sitemap(fnames):
    rows = "".join(f"  <url><loc>{url(f)}</loc></url>\n" for f in fnames)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}</urlset>\n'


def robots():
    if not LIVE:
        return "User-agent: *\nDisallow: /\n"
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
