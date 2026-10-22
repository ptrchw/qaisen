# Services website

Static marketing site for Peter Chow's fixed-scope UX and GenAI services (Singapore).

## Structure

- `svc-site/` — the published website. Cloudflare Pages serves this folder as-is.
  - `styles.css`, `main.js` and `img/` are edited directly here.
  - The `.html` files, `sitemap.xml` and `robots.txt` are **generated**. Don't edit them by hand.
- `build/` — the generator.
  - `build/pages/*.html` — the body of each page (edit content here).
  - `build/build.py` — wraps each page with the shared head, header, footer and call-to-action.
  - `build/seo.py` — page titles, descriptions, structured data, domain and launch settings.
  - `build/archive/` — retired pages and images, kept for reference. Not published.

## Updating the site

```bash
python3 build/build.py svc-site
git add -A && git commit -m "Describe the change" && git push
```

Cloudflare Pages redeploys automatically on every push to `main`.

## Cloudflare Pages settings

- Framework preset: **None**
- Build command: *(leave empty)*
- Build output directory: **svc-site**

## Before launch

In `build/seo.py` set `SITE_URL`, `BIZ_NAME` and `BRAND`, then set `LIVE = True` (this lifts the
`noindex` that keeps the preview out of search engines). In `svc-site/main.js` fill in the
`SITE` settings (Calendly, WhatsApp, email, portfolio). Rebuild and push.
