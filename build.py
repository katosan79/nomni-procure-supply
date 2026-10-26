#!/usr/bin/env python3
"""Build the Procure & Supply staging site.

Each file in src/pages/ starts with a header comment:
  <!-- title: Page title | desc: Meta description | nav: procure -->
The rest of the file is the page body. {{i:name}} inserts an inline icon.
This script wraps each page in the shared layout and writes it to docs/
(GitHub Pages serves main /docs). Run: python3 build.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

_P = {
    "order": '<path d="M4 5h2l2 10h10l2-7H7.2"/><circle cx="10" cy="19" r="1.3"/><circle cx="17" cy="19" r="1.3"/>',
    "invoice": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "box": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
    "recipe": '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/><path d="M9 8h6"/>',
    "hq": '<path d="M4 21V5l8-2v18M12 9l8 2v10"/><path d="M7 8h2M7 12h2M7 16h2M15 14h2M15 18h2"/>',
    "truck": '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h4"/>',
    "spark": '<path d="M12 3v5M12 16v5M3 12h5M16 12h5M6 6l3 3M15 15l3 3M18 6l-3 3M9 15l-3 3"/>',
    "shield": '<path d="M12 3 5 6v6c0 4 3 7.5 7 9 4-1.5 7-5 7-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/>',
    "grant": '<circle cx="12" cy="9" r="5"/><path d="m9 13-2 8 5-3 5 3-2-8"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="m7 15 4-4 3 3 5-6"/>',
    "kitchen": '<path d="M4 10h16v10H4zM8 10V6a4 4 0 0 1 8 0v4"/><path d="M8 14h8"/>',
    "check": '<path d="m5 12 4.5 4.5L19 7"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "lock": '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "undo": '<path d="M9 7 4 12l5 5"/><path d="M4 12h10a6 6 0 0 1 0 12h-3"/>',
    "eye": '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.6"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
    "store": '<path d="M4 9 5.5 4h13L20 9M4 9h16v11H4zM4 9a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0A2.7 2.7 0 0 0 20 9"/><path d="M10 20v-5h4v5"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.3 5 2.7 5 5.8"/>',
    "home": '<path d="M4 11 12 4l8 7v9H4z"/><path d="M10 20v-6h4v6"/>',
}

def icon(name, size=18, sw=1.6):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>')

HEAD = """<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0E3727">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%230E3727'/%3E%3Ctext x='7' y='22' font-family='Arial' font-weight='700' font-size='17' fill='white'%3En%3C/text%3E%3Ccircle cx='24' cy='20' r='3' fill='%238FDB6A'/%3E%3C/svg%3E">
<link rel="preload" href="assets/fonts/hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div class="staging">STAGING PREVIEW · Not for public distribution · Feature status, numbers and quotes are still being verified</div>
<div class="rebrand"><b>Zeemart is now Nomni.</b> Same team, same logins, a smarter platform.<a href="nomni.html">What's changed →</a></div>
"""

def mi(href, ic, title, desc):
    return f'<a href="{href}"><span class="ic">{icon(ic)}</span><span><b>{title}</b><span class="d">{desc}</span></span></a>'

def header(current):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<div class="nav-item"><a href="{href}"{cur}>{label}</a></div>'
    return f"""<header class="site-header">
  <div class="nav">
    <a class="brand" href="index.html" aria-label="Nomni Procure and Supply home"><span class="brand-mark">nomni<i></i></span><span class="brand-sub">Procure &amp; Supply</span></a>
    <nav class="nav-links" aria-label="Main">
      <div class="nav-item"><button aria-expanded="false" aria-haspopup="true">Procure</button>
        <div class="menu">
          {mi("procure.html", "order", "Procure for restaurants", "Ordering, invoices, inventory and recipe costs")}
          {mi("groups.html", "hq", "Procure for groups", "HQ control across every outlet")}
          {mi("central-kitchens.html", "kitchen", "Central kitchens", "Pick, pack and invoice your outlets")}
          {mi("solutions.html", "users", "Who it's for", "Cafés, restaurants, kiosks and franchise groups")}
        </div>
      </div>
      <div class="nav-item"><button aria-expanded="false" aria-haspopup="true">Supply</button>
        <div class="menu">
          {mi("supply.html", "store", "Supply for suppliers", "Your B2B store and back office")}
          {mi("ai-inbox.html", "chat", "AI order inbox", "WhatsApp, voice notes and photos become orders")}
          {mi("payments.html", "card", "Payments", "Get paid on terms, automatically")}
        </div>
      </div>
      {link("ai.html", "AI agents", "ai")}
      <div class="nav-item"><button aria-expanded="false" aria-haspopup="true">Platform</button>
        <div class="menu">
          {mi("peppol.html", "shield", "PEPPOL InvoiceNow", "E-invoicing on both sides of the invoice")}
          {mi("integrations.html", "plug", "Integrations", "Accounting, POS and ERP")}
          {mi("edge-grant.html", "grant", "EDGE grant (SG)", "Check if your business qualifies")}
        </div>
      </div>
      {link("customers.html", "Customers", "customers")}
      {link("pricing.html", "Pricing", "pricing")}
    </nav>
    <div class="nav-actions">
      <select class="region" aria-label="Region"><option value="sg">SG</option><option value="au">AU</option><option value="my">MY</option></select>
      <a class="link-quiet" href="contact.html#demo">Book a demo</a>
      <a class="btn btn-sm" href="contact.html#trial">Start free</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span></button>
    </div>
  </div>
  <div class="region-note" hidden>AU and MY versions are coming. You're viewing the Singapore site.</div>
</header>
<main>
"""

FOOTER = """</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html"><span class="brand-mark">nomni<i></i></span></a>
        <p class="about">Procure and Supply connect restaurants and their suppliers. Part of Nomni, the all-in-one technology platform built for hospitality.</p>
      </div>
      <div><h4>Procure</h4><ul>
        <li><a href="procure.html">For restaurants</a></li>
        <li><a href="groups.html">For groups</a></li>
        <li><a href="central-kitchens.html">Central kitchens</a></li>
        <li><a href="solutions.html">Who it's for</a></li>
        <li><a href="pricing.html">Pricing</a></li></ul></div>
      <div><h4>Supply</h4><ul>
        <li><a href="supply.html">For suppliers</a></li>
        <li><a href="ai-inbox.html">AI order inbox</a></li>
        <li><a href="payments.html">Payments</a></li></ul></div>
      <div><h4>Platform</h4><ul>
        <li><a href="ai.html">AI agents</a></li>
        <li><a href="peppol.html">PEPPOL InvoiceNow</a></li>
        <li><a href="integrations.html">Integrations</a></li>
        <li><a href="edge-grant.html">EDGE grant</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="customers.html">Customers</a></li>
        <li><a href="news.html">News</a></li>
        <li><a href="nomni.html">Zeemart is now Nomni</a></li>
        <li><a href="https://www.nomni.ai/">Nomni.ai</a></li>
        <li><a href="https://support.zeemart.co/">Help centre</a></li>
        <li><a href="contact.html">Contact</a></li></ul></div>
    </div>
    <div class="wordmark" aria-hidden="true">nomni</div>
    <div class="footer-bottom"><span>© 2026 Nomni · Procure and Supply are Nomni products</span><span>Singapore · Australia · Malaysia</span></div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    (OUT / ".nojekyll").write_text("")
    for page in sorted((SRC / "pages").glob("*.html")):
        text = page.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(.*?)-->", text, re.S)
        meta = {}
        if m:
            for part in m.group(1).split("|"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    meta[k.strip()] = v.strip()
            text = text[m.end():]
        text = re.sub(r"\{\{i:(\w+)(?::(\d+))?\}\}", lambda mm: icon(mm.group(1), int(mm.group(2) or 18)), text)
        html = HEAD.format(title=meta.get("title", "Nomni"), desc=meta.get("desc", "")) \
            + header(meta.get("nav", "")) + text.strip() + "\n" + FOOTER
        (OUT / page.name).write_text(html, encoding="utf-8")
        print("built", page.name)

if __name__ == "__main__":
    build()
