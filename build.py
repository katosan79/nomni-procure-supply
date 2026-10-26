#!/usr/bin/env python3
"""Build the Procure & Supply staging site.

Each file in src/pages/ starts with a header comment:
  <!-- title: Page title | desc: Meta description | nav: procure -->
The rest of the file is the page body. This script wraps it in the shared
layout (head, banners, header, footer) and writes the result to the repo root
(GitHub Pages serves from there). Run: python3 build.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"  # GitHub Pages: serve from /docs on main

HEAD = """<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E3727'/%3E%3Ccircle cx='22' cy='11' r='4' fill='%238FDB6A'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div class="staging"><strong>Staging preview.</strong> Not for public distribution. Feature status, numbers and quotes are still being verified.</div>
<div class="rebrand">Zeemart is now Nomni. Same team, same logins, a smarter platform.<a href="nomni.html">What's changed →</a></div>
"""

def nav_link(href, label, key, current):
    cur = ' aria-current="page"' if key == current else ""
    return f'<div class="nav-item"><a href="{href}"{cur}>{label}</a></div>'

def header(current):
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Nomni Procure and Supply home">nomni<span class="dot"></span><small>Procure &amp; Supply</small></a>
    <nav class="nav-links" aria-label="Main">
      <div class="nav-item"><button aria-expanded="false" aria-haspopup="true">Procure ▾</button>
        <div class="menu">
          <a href="procure.html"><b>Procure for restaurants</b><span>Ordering, invoices, inventory and recipe costs</span></a>
          <a href="groups.html"><b>Procure for groups (HQ)</b><span>Master lists, recipes and POS mapping across outlets</span></a>
          <a href="procure.html#central-kitchen"><b>Central kitchens</b><span>Pick, pack and invoice your outlets</span></a>
        </div>
      </div>
      <div class="nav-item"><button aria-expanded="false" aria-haspopup="true">Supply ▾</button>
        <div class="menu">
          <a href="supply.html"><b>Supply for suppliers</b><span>Your B2B store and back office</span></a>
          <a href="supply.html#inbox"><b>AI order inbox</b><span>WhatsApp, voice notes and photos become orders</span></a>
          <a href="supply.html#payments"><b>Payments</b><span>Get paid on terms, automatically</span></a>
        </div>
      </div>
      {nav_link("ai.html", "AI agents", "ai", current)}
      <div class="nav-item"><button aria-expanded="false" aria-haspopup="true">Platform ▾</button>
        <div class="menu">
          <a href="peppol.html"><b>PEPPOL InvoiceNow</b><span>E-invoicing on both sides of the invoice</span></a>
          <a href="integrations.html"><b>Integrations</b><span>Accounting, POS and ERP</span></a>
          <a href="edge-grant.html"><b>EDGE grant (SG)</b><span>Check if your business qualifies</span></a>
        </div>
      </div>
      {nav_link("pricing.html", "Pricing", "pricing", current)}
    </nav>
    <div class="nav-actions">
      <select class="region" aria-label="Region"><option value="sg">SG</option><option value="au">AU</option><option value="my">MY</option></select>
      <a class="btn btn-ghost btn-sm" href="contact.html#demo">Book a demo</a>
      <a class="btn btn-primary btn-sm" href="contact.html#trial">Start free</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false">Menu</button>
    </div>
  </div>
  <div class="wrap region-note small muted" hidden style="padding-bottom:10px">AU and MY versions of this site are coming. You're viewing the Singapore site.</div>
</header>
<main>
"""

FOOTER = """</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html">nomni<span class="dot"></span></a>
        <p style="margin-top:14px;max-width:300px">Procure and Supply connect restaurants and their suppliers. Part of Nomni, the all-in-one technology platform built for hospitality.</p>
      </div>
      <div><h4>Procure</h4><ul>
        <li><a href="procure.html">For restaurants</a></li>
        <li><a href="groups.html">For groups (HQ)</a></li>
        <li><a href="procure.html#central-kitchen">Central kitchens</a></li>
        <li><a href="pricing.html">Pricing</a></li></ul></div>
      <div><h4>Supply</h4><ul>
        <li><a href="supply.html">For suppliers</a></li>
        <li><a href="supply.html#inbox">AI order inbox</a></li>
        <li><a href="supply.html#payments">Payments</a></li></ul></div>
      <div><h4>Platform</h4><ul>
        <li><a href="ai.html">AI agents</a></li>
        <li><a href="peppol.html">PEPPOL InvoiceNow</a></li>
        <li><a href="integrations.html">Integrations</a></li>
        <li><a href="edge-grant.html">EDGE grant</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="nomni.html">Zeemart is now Nomni</a></li>
        <li><a href="https://www.nomni.ai/">Nomni.ai</a></li>
        <li><a href="https://support.zeemart.co/">Help centre</a></li>
        <li><a href="contact.html">Contact</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 Nomni. Procure and Supply are Nomni products.</span><span>Singapore · Australia · Malaysia</span></div>
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
        html = HEAD.format(title=meta.get("title", "Nomni"), desc=meta.get("desc", "")) \
            + header(meta.get("nav", "")) + text.strip() + "\n" + FOOTER
        (OUT / page.name).write_text(html, encoding="utf-8")
        print("built", page.name)

if __name__ == "__main__":
    build()
