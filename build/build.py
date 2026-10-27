#!/usr/bin/env python3
"""Builds the static services site into ../svc-site from shared header/footer + page bodies."""
import html as htmlmod, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import seo

OUT = pathlib.Path(sys.argv[1])
PAGES_DIR = pathlib.Path(__file__).parent / "pages"

BIZ = "QAISEN"
WORDMARK = '<span class="wordmark">QAISEN</span>'

NAV = [
    ("ai-opportunity-assessment.html", "AI Assessment"),
    ("discovery-sprint.html", "Sprints"),
    ("ux-audit.html", "UX Audit"),
    ("workshops.html", "Workshops"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

ICON_WA = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l1.65-3.8a9 9 0 1 1 3.4 2.9L3 21"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"/></svg>'
ICON_CAL = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
ICON_MAIL = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'


ICON_SEARCH = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICON_BULB = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.2 1 2V17h6v-.3c0-.8.4-1.5 1-2A7 7 0 0 0 12 2z"/></svg>'
ICON_TEAM = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18.5 20a6.5 6.5 0 0 0-3-5.5"/></svg>'

ICON_CODE = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/></svg>'

def head(title, desc, extra=""):
    title, desc = htmlmod.escape(title), htmlmod.escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{extra}<meta name="theme-color" content="#F5F4FA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B0815" media="(prefers-color-scheme: dark)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Dots&amp;text=QAISEN&amp;display=swap">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a class="nav-link" href="{href}"{cur}>{label}</a></li>')
    items = "\n          ".join(items)
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="QAISEN home">{WORDMARK}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="nav-toggle-bars" aria-hidden="true"><span></span></span><span class="nav-toggle-label">Menu</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main" hidden>
      <ul class="nav-list">
          {items}
          <li class="nav-cta"><a class="btn btn-primary btn-sm" href="contact.html" data-link="calendly">Book a call</a></li>
      </ul>
    </nav>
  </div>
</header>
"""


def footer():
    return f"""<footer class="site-footer night">
  <div class="wrap">
    <div class="footer-grid">
      <div class="stack">
        <a class="brand" href="index.html" aria-label="QAISEN home">{WORDMARK}</a>
        <p class="muted small" style="max-width:42ch">Problem first. Outcomes by design. Fixed-price UX and AI diagnosis for Singapore SMEs.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul class="footer-links">
          <li><a href="ai-opportunity-assessment.html#reality-check">AI Reality Check (coming soon)</a></li>
          <li><a href="ai-opportunity-assessment.html">AI Opportunity Assessment</a></li>
          <li><a href="discovery-sprint.html">Discovery &amp; Design Sprints</a></li>
          <li><a href="ux-audit.html">UX Audit</a></li>
          <li><a href="workshops.html">Applied AI Workshops</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul class="footer-links">
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="privacy.html">Privacy Policy</a></li>
          <li><a href="terms.html">Terms of Use</a></li>
          <li><a href="contact.html" data-link="linkedin">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <p>© <span data-year>2026</span> {BIZ} · UEN <span class="ph">[UEN]</span> · Singapore</p>
      <p>Prices in Singapore dollars, before GST where applicable.</p>
    </div>
  </div>
</footer>
<div class="mobile-cta" role="region" aria-label="Quick contact">
  <a class="btn btn-primary" href="contact.html" data-link="calendly">{ICON_CAL}Book a call</a>
  <a class="btn btn-tint" href="contact.html" data-link="whatsapp">{ICON_WA}WhatsApp</a>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="main.js" defer></script>
</body>
</html>
"""

def cta_band(title="Not sure where to start?", text="Book a free 20-minute call. Tell me the business problem, and I'll tell you honestly whether AI is the right fix, which offer suits you, or whether you need one at all."):
    return f"""<section class="section-tight" aria-labelledby="cta-title">
  <div class="wrap">
    <div class="cta-band" data-reveal>
      <h2 id="cta-title">{title}</h2>
      <p>{text}</p>
      <div class="btn-row">
        <a class="btn btn-light btn-lg" href="contact.html" data-link="calendly">{ICON_CAL}Book a 20-minute call</a>
        <a class="btn btn-ghost-light btn-lg" href="contact.html" data-link="whatsapp">{ICON_WA}Message on WhatsApp</a>
      </div>
    </div>
  </div>
</section>
"""

CTX = dict(ICON_CODE=ICON_CODE, ICON_SEARCH=ICON_SEARCH, ICON_BULB=ICON_BULB, ICON_TEAM=ICON_TEAM, BIZ=BIZ, ICON_WA=ICON_WA, ICON_CAL=ICON_CAL, ICON_MAIL=ICON_MAIL, CTA=cta_band())

PAGES = [(f, t, d) for f, (t, d, _kw) in seo.PAGES.items()]

OUT.mkdir(parents=True, exist_ok=True)
for fname, title, desc in PAGES:
    body = (PAGES_DIR / fname).read_text()
    for k, v in CTX.items():
        body = body.replace("{{" + k + "}}", v)
    html = head(title, desc, seo.head_extra(fname) + seo.jsonld(fname, body)) + header(fname) + '<main id="main" tabindex="-1">\n' + body + "\n</main>\n" + footer()
    (OUT / fname).write_text(html)
    print("built", fname, len(html))
(OUT / "sitemap.xml").write_text(seo.sitemap([f for f, _, _ in PAGES]))
(OUT / "robots.txt").write_text(seo.robots())
