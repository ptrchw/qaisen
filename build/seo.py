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
        f"Problem-First AI Diagnosis for Singapore Businesses | {BRAND}",
        "Find out whether AI is the right fix before you spend on it. Fixed-price AI assessments, sprints, UX audits and AI workshops for Singapore SMEs.",
        ["AI consultant Singapore", "AI readiness assessment", "AI for SMEs Singapore", "AI opportunity assessment", "UX consultant Singapore", "design sprint"],
    ),
    "ai-opportunity-assessment.html": (
        f"AI Opportunity Assessment for Singapore SMEs | {BRAND}",
        "A fixed-price review of your key workflows, with a written answer on where AI could help, where it couldn't, and what to do next. Tool-neutral.",
        ["AI opportunity assessment", "AI readiness assessment Singapore", "AI use case discovery", "AI for SMEs", "AI consultant Singapore", "AI reality check"],
    ),
    "discovery-sprint.html": (
        f"Discovery & Design Sprints in Singapore | {BRAND}",
        "Test whether AI is the right tool before you build: a Discovery Sprint with real users and a prototype, or a 4-day Design Sprint. From S$5,900.",
        ["design sprint Singapore", "product discovery", "discovery sprint", "validate an AI idea", "prototype testing", "user research"],
    ),
    "ux-audit.html": (
        f"UX Audit for Websites & Apps in Singapore | {BRAND}",
        "Find out why users get stuck. An expert UX audit of three key journeys, backed by your customer feedback, plus a workshop to rank every fix. From S$5,000.",
        ["UX audit Singapore", "usability audit", "heuristic evaluation", "website UX review", "app UX review", "usability testing"],
    ),
    "workshops.html": (
        f"Applied AI Workshops for Teams in Singapore | {BRAND}",
        "Hands-on team training: your people learn to spot and test AI ideas with design thinking and rapid prototyping. 1–3 days, up to 10 people. From S$4,500.",
        ["AI workshop Singapore", "AI training for teams", "design thinking workshop", "GenAI training", "rapid prototyping workshop", "AI training for SMEs"],
    ),
    "about.html": (
        f"Peter Chow, Founder of QAISEN | {BRAND}",
        "Peter Chow is a Singapore UX architect and founder of QAISEN, with 20+ years turning complex problems into products and services people actually use.",
        ["Peter Chow UX", "UX architect Singapore", "AI consultant Singapore", "design thinking"],
    ),
    "contact.html": (
        f"Book a Free 20-Minute Call | {BRAND}",
        "Book a free 20-minute call to find out whether AI is the right fix for your business problem, and which offer suits you. Or message on WhatsApp or email.",
        ["AI consultation Singapore", "book an AI consultant", "UX consultation Singapore", "contact"],
    ),
}

ORG_ID = SITE_URL + "/#org"
PERSON_ID = SITE_URL + "/about.html#peter"

SERVICES = [
    # (page, name, serviceType, description, lowPrice, highPrice); prices None until set
    ("ai-opportunity-assessment.html", "AI Opportunity Assessment", "AI opportunity and readiness assessment",
     "A fixed-price review of up to three key workflows with a written answer on where AI fits, partly fits or doesn't.", None, None),
    ("ux-audit.html", "UX Audit", "UX audit and usability review",
     "Expert heuristic review and flow audit of three key journeys, backed by customer feedback, with a prioritisation workshop.", 5000, 7500),
    ("discovery-sprint.html", "Discovery & Design Sprints", "Design sprint and product discovery",
     "A 4-day Design Sprint or a Discovery Sprint of up to 5 weeks to test ideas with real users before you build.", 5900, 8700),
    ("workshops.html", "Applied AI Workshops", "AI and design thinking team training",
     "Hands-on, in-house workshops of one to three days for up to 10 people.", 4500, 10500),
]

CRUMB_NAMES = {
    "ai-opportunity-assessment.html": "AI Opportunity Assessment", "ux-audit.html": "UX Audit", "discovery-sprint.html": "Sprints", "workshops.html": "Workshops",
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
        "knowsAbout": ["AI opportunity assessment", "AI readiness", "User experience design", "UX audit", "Usability testing", "Design sprint",
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
            svc = {"@type": "Service", "name": name, "serviceType": stype, "description": desc, "url": url(p),
                   "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "Singapore"}}
            if lo is not None:
                svc["offers"] = {"@type": "AggregateOffer", "priceCurrency": "SGD", "lowPrice": lo, "highPrice": hi}
            graph.append(svc)
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
