# -*- coding: utf-8 -*-
import json, os, random, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
from content import *
from services_short import SERVICES, SERVICE_PHOTOS, FLOW

OUT_PROD = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/site/dist"
OUT_ART = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/site/artifact"

ORG_ID = SITE + "/#cabinet"
PERSON_ID = SITE + "/#adrien-arnal"
OPT = {p["key"]: p["option"] for p in PILLARS}
PILLAR = {p["key"]: p for p in PILLARS}

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
ICON_ARROW = '<span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 17 17 7M8 7h9v9"/></svg></span>'
CORNER = '<span class="corner" aria-hidden="true"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 17 17 7M8 7h9v9"/></svg></span></span>'

def url(slug):
    return SITE + "/" if slug == "index" else f"{SITE}/{slug}.html"

def esc(s):
    return H.escape(s, quote=True)

def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)

# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": ORG_ID,
        "name": "GE Metric",
        "legalName": "SASU GE METRIC",
        "alternateName": ["Gemetric", "GE Metric Géomètre-Expert"],
        "slogan": TAGLINE,
        "description": CABINET,
        "url": SITE + "/",
        "logo": SITE + "/assets/logo.svg",
        "image": [SITE + "/assets/adrien-arnal-geometre-expert.jpg", SITE + "/assets/nice-baie-des-anges-1600.jpg"],
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS[0], "postalCode": ADDRESS[1],
                    "addressLocality": ADDRESS[2], "addressRegion": "Provence-Alpes-Côte d’Azur", "addressCountry": "FR"},
        "areaServed": [{"@type": "City", "name": "Nice"}, {"@type": "AdministrativeArea", "name": "Côte d’Azur"},
                       {"@type": "AdministrativeArea", "name": "Alpes-Maritimes"}, {"@type": "Country", "name": "Monaco"}],
        "founder": {"@id": PERSON_ID},
        "employee": {"@id": PERSON_ID},
        "foundingDate": "2025",
        "vatID": "FR10992581470",
        "taxID": "992 581 470",
        "identifier": [
            {"@type": "PropertyValue", "propertyID": "SIRET", "value": "99258147000018"},
            {"@type": "PropertyValue", "propertyID": "RCS Nice", "value": "992 581 470"},
            {"@type": "PropertyValue", "propertyID": "Ordre des Géomètres-Experts", "value": "STR_00000186"}],
        "knowsAbout": ["Bornage", "Division parcellaire", "Servitudes", "Relevé topographique", "Implantation",
                       "État descriptif de division", "Règlement de copropriété", "Division en volumes",
                       "Relevé d’architecte", "Nuage de points 3D"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services de géomètre-expert",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": SERVICES[s]["nav"], "url": url(s)}}
                                for p in PILLARS for s in p["pages"]]},
        "sameAs": [LINKEDIN],
    }

def person_schema():
    return {
        "@context": "https://schema.org", "@type": "Person", "@id": PERSON_ID,
        "name": "Adrien Arnal", "jobTitle": "Géomètre-Expert",
        "image": SITE + "/assets/adrien-arnal-geometre-expert.jpg",
        "worksFor": {"@id": ORG_ID},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "École Supérieure des Géomètres et Topographes (ESGT)"},
        "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "Diplôme", "name": "Ingénieur ESGT (2012)"},
                          {"@type": "EducationalOccupationalCredential", "credentialCategory": "Inscription ordinale",
                           "name": "Géomètre-Expert, prestation de serment auprès de l’Ordre des Géomètres-Experts (mars 2020)"}],
        "sameAs": [LINKEDIN],
    }

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(s)} for i, (n, s) in enumerate(items)]}

def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def service_schema(slug, s):
    return {"@context": "https://schema.org", "@type": "Service", "@id": url(slug) + "#service",
            "name": s["nav"], "serviceType": s["nav"], "description": s["answer"],
            "provider": {"@id": ORG_ID}, "url": url(slug),
            "areaServed": [{"@type": "City", "name": "Nice"}, {"@type": "AdministrativeArea", "name": "Côte d’Azur"}, {"@type": "Country", "name": "Monaco"}],
            "category": PILLAR[s["pillar"]]["name"]}

def ld(*objs):
    return "\n".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>" for o in objs)

# ---------------------------------------------------------------- plans (illustrations)
def plan_svg(kind, label):
    g = []
    W, Hh = 480, 360
    for x in range(40, W, 40): g.append(f'<line class="grid" x1="{x}" y1="0" x2="{x}" y2="{Hh-40}"/>')
    for y in range(40, Hh - 40, 40): g.append(f'<line class="grid" x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    contours = ['M-10 70 C 90 40 190 95 300 60 S 470 30 500 55', 'M-10 120 C 100 92 200 140 310 108 S 470 85 500 104',
                'M-10 175 C 110 150 215 190 320 160 S 470 140 500 156', 'M-10 232 C 120 210 230 245 330 214 S 470 196 500 210',
                'M-10 290 C 130 270 240 300 340 272 S 470 256 500 266']
    body = []
    if kind in ("parcel", "division", "topo", "implant", "home"):
        body += [f'<path class="contour" d="{d}"/>' for d in contours]
    if kind in ("parcel", "division", "home", "implant"):
        pts = [(120, 78), (360, 62), (392, 262), (98, 280)]
        body.append('<polygon class="parcel" pathLength="1" points="' + " ".join(f"{x},{y}" for x, y in pts) + '"/>')
        if kind != "implant":
            body.append('<rect class="bldg" x="168" y="128" width="96" height="70" transform="rotate(-4 216 163)"/>')
        if kind == "division":
            body.append('<line class="cut" x1="238" y1="70" x2="250" y2="271" stroke="var(--red)" stroke-width="2" stroke-dasharray="7 5"/>')
            body.append('<text class="lbl" x="150" y="240">LOT A</text><text class="lbl" x="296" y="200">LOT B</text>')
        if kind == "implant":
            b = [(186, 130), (306, 122), (312, 214), (192, 222)]
            body.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in b) + '" fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 4"/>')
            for i, (x, y) in enumerate(b):
                body.append(f'<path d="M{x-7} {y}h14M{x} {y-7}v14" stroke="var(--red)" stroke-width="2"/><text class="lbl" x="{x+8}" y="{y-6}">P{i+1}</text>')
            body.append('<path d="M98 280 L192 222" stroke="var(--ink-3)" stroke-dasharray="2 3"/><text class="lbl" x="118" y="244">recul</text>')
        else:
            for i, (x, y) in enumerate(pts):
                body.append(f'<g class="borne-g" style="--i:{i}"><circle class="borne" cx="{x}" cy="{y}" r="5.5"/><circle class="borne-ring" cx="{x}" cy="{y}" r="10" fill="none" stroke="var(--red)" stroke-width="1"/></g>')
                body.append(f'<text class="lbl" x="{x+12}" y="{y-10}">B{i+1}</text>')
            if kind == "division":
                for x, y in [(238, 70), (250, 271)]:
                    body.append(f'<circle class="borne" cx="{x}" cy="{y}" r="5.5"/>')
        body.append('<text class="lbl" x="22" y="330" opacity=".8">Parcelle voisine</text>')
    if kind == "topo":
        for x, y, z in [(90, 96, "z 148.2"), (210, 132, "z 141.7"), (330, 180, "z 134.9"), (150, 262, "z 127.3"), (390, 250, "z 125.8")]:
            body.append(f'<path d="M{x-5} {y-5}l10 10M{x+5} {y-5}l-10 10" stroke="var(--red)" stroke-width="2"/><text class="lbl" x="{x+9}" y="{y+4}">{z}</text>')
        body.append('<rect class="bldg" x="250" y="56" width="80" height="54"/><path d="M60 300 Q 160 250 220 200 T 420 120" fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="9 4"/>')
        for cx, cy in [(120, 170), (380, 300), (430, 70), (60, 230)]:
            body.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="none" stroke="var(--ink-2)"/><circle cx="{cx}" cy="{cy}" r="2" fill="var(--ink-2)"/>')
    if kind == "copro":
        body.append('<rect x="60" y="40" width="360" height="240" fill="var(--surface)" stroke="var(--ink)" stroke-width="3"/>')
        body.append('<path d="M200 40V280M60 160H200M300 40V160M200 160H420M300 160V280" stroke="var(--ink)" stroke-width="1.5"/>')
        body.append('<rect x="200" y="40" width="100" height="120" fill="var(--red-soft)"/>')
        for x, y, t in [(105, 104, "LOT 12"), (105, 224, "LOT 13"), (222, 104, "PARTIES"), (222, 120, "COMMUNES"), (335, 104, "LOT 14"), (226, 224, "LOT 15"), (335, 224, "LOT 16")]:
            body.append(f'<text class="lbl" x="{x}" y="{y}">{t}</text>')
        body.append('<text class="lbl" x="60" y="310">Niveau R+3 — plan annexé à l’EDD</text>')
    if kind == "volumes":
        layers = [(220, 270, "VOLUME 1 · Parking public", "var(--paper-2)"), (160, 220, "VOLUME 2 · Commerces", "var(--red-soft)"),
                  (60, 160, "VOLUME 3 · Logements", "var(--surface)")]
        for y1, y2, t, f in layers:
            body.append(f'<rect x="80" y="{y1}" width="320" height="{y2-y1}" fill="{f}" stroke="var(--ink)" stroke-width="1.5"/><text class="lbl" x="96" y="{(y1+y2)//2+4}">{t}</text>')
        body.append('<line x1="40" y1="220" x2="440" y2="220" stroke="var(--red)" stroke-width="1.5" stroke-dasharray="6 4"/><text class="lbl" x="404" y="214">sol</text>')
        for y, z in [(60, "NGF +24.30"), (160, "NGF +12.10"), (270, "NGF +5.60")]:
            body.append(f'<text class="lbl" x="404" y="{y+4}">{z}</text><path d="M396 {y}h-8" stroke="var(--ink)"/>')
    if kind == "releve":
        body.append('<rect x="90" y="60" width="300" height="230" fill="var(--surface)" stroke="var(--ink)" stroke-width="2"/><path d="M80 60 L240 20 L400 60" fill="none" stroke="var(--ink)" stroke-width="2"/>')
        for r, y in enumerate([84, 160, 230]):
            for c in range(4):
                x = 112 + c * 70
                hh = 52 if r < 2 else 60
                body.append(f'<rect x="{x}" y="{y}" width="36" height="{hh}" fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1.2"/>')
        body.append('<path d="M60 160h20M60 60v230" stroke="var(--red)" stroke-width="1.2"/><text class="lbl" x="20" y="64">+9.80</text><text class="lbl" x="20" y="164">+4.95</text><text class="lbl" x="20" y="294">±0.00</text>')
        body.append('<text class="lbl" x="90" y="318">Façade sud — relevé de l’existant</text>')
    if kind == "scan":
        rnd = random.Random(7)
        def edge(x1, y1, x2, y2, n):
            for _ in range(n):
                t = rnd.random(); jx = rnd.gauss(0, 1.4); jy = rnd.gauss(0, 1.4)
                body.append(f'<circle cx="{x1+(x2-x1)*t+jx:.1f}" cy="{y1+(y2-y1)*t+jy:.1f}" r="1.3" fill="var(--ink)"/>')
        for e in [(90, 290, 390, 290, 90), (90, 290, 90, 90, 60), (390, 290, 390, 90, 60), (70, 95, 240, 30, 60), (240, 30, 410, 95, 60),
                  (90, 90, 390, 90, 70), (150, 290, 150, 200, 26), (200, 290, 200, 200, 26), (150, 200, 200, 200, 16)]:
            edge(*e)
        for wx in (250, 320):
            for (a, b, c, d) in [(wx, 140, wx + 40, 140), (wx, 200, wx + 40, 200), (wx, 140, wx, 200), (wx + 40, 140, wx + 40, 200)]:
                edge(a, b, c, d, 14)
        for _ in range(160):
            body.append(f'<circle cx="{rnd.uniform(95,385):.1f}" cy="{rnd.uniform(95,285):.1f}" r="1" fill="var(--ink-3)" opacity=".5"/>')
        for _ in range(40):
            body.append(f'<circle cx="{rnd.uniform(100,380):.1f}" cy="{rnd.uniform(100,280):.1f}" r="1.4" fill="var(--red)"/>')
    # north + scale
    deco = ('<g transform="translate(446 34)"><path d="M0 -18 L7 8 L0 3 L-7 8 Z" fill="var(--ink)"/><text class="lbl" x="-4" y="24">N</text></g>'
            f'<g transform="translate(300 {Hh-22})"><rect width="40" height="5" fill="var(--ink)"/><rect x="40" width="40" height="5" fill="none" stroke="var(--ink)"/>'
            '<text class="lbl" x="0" y="18">0</text><text class="lbl" x="74" y="18">10 m</text></g>')
    return (f'<svg class="plan" viewBox="0 0 {W} {Hh}" role="img" aria-label="{esc(label)}">'
            f'<rect width="{W}" height="{Hh}" fill="var(--surface)"/>' + "".join(g) + "".join(body) + deco + "</svg>")


def img_tag(key, pos=None, cls="", eager=False, sizes="(max-width: 860px) 100vw, 1180px"):
    ph = PHOTOS[key]
    ss = f' srcset="{ph["srcset"]}" sizes="{sizes}"' if ph["srcset"] else ""
    st = f' style="object-position:{pos}"' if pos else ""
    return (f'<img src="{ph["src"]}"{ss} alt="{esc(ph["alt"])}" width="{ph["w"]}" height="{ph["h"]}"'
            f' loading="{"eager" if eager else "lazy"}" decoding="async"{st}{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>')

def figure(key, pos=None, cls="photo", caption=True, eager=False, sizes="(max-width: 860px) 100vw, 1180px"):
    cap = f'<figcaption>{esc(PHOTOS[key]["caption"])}</figcaption>' if caption else ""
    return f'<figure class="{cls}">{img_tag(key, pos, eager=eager, sizes=sizes)}{cap}</figure>'

def terrain_section(slug):
    if slug not in SERVICE_PHOTOS: return ""
    key, pos, title, text = SERVICE_PHOTOS[slug]
    txt = f'<div class="sec-head" style="margin-bottom:0"><h2>{esc(title)}</h2><p>{esc(text)}</p></div>'
    if PHOTOS[key]["w"] > PHOTOS[key]["h"]:
        return f'<section class="section section-photo"><div class="wrap photo-stack">{txt}{figure(key, pos, "photo photo-wide")}</div></section>'
    return f'<section class="section section-photo"><div class="wrap photo-split">{txt}{figure(key, None, "photo photo-tall", sizes="(max-width: 860px) 100vw, 420px")}</div></section>'

# ---------------------------------------------------------------- layout pieces
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">'

def head_tags(slug, title, desc, schema, short_title):
    return f"""<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url(slug)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="GE Metric — Géomètre-Expert">
<meta property="og:title" content="{esc(short_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url(slug)}">
<meta property="og:image" content="{SITE}/assets/nice-baie-des-anges-1600.jpg"><meta property="og:image:alt" content="Vue sur la baie des Anges à Nice"><meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="FR-06"><meta name="geo.placename" content="Nice">
<link rel="icon" href="assets/logo.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
{schema}"""

def nav_html():
    cols = []
    for p in PILLARS:
        links = "".join(f'<a href="{s}.html">{esc(SERVICES[s]["nav"])}</a>' for s in p["pages"])
        cols.append(f'<div><p class="nav-h">{esc(p["name"])}</p>{links}</div>')
    mob = "".join(f'<p class="nav-h">{esc(p["name"])}</p>' + "".join(f'<a href="{s}.html">{esc(SERVICES[s]["nav"])}</a>' for s in p["pages"]) for p in PILLARS)
    return f"""<header class="site-header"><div class="wrap"><div class="header-pill">
<a class="logo" href="index.html" aria-label="GE Metric, accueil"><img src="assets/logo.svg" alt="GE Metric Géomètre-Expert" width="62" height="64"></a>
<nav class="nav" aria-label="Navigation principale">
<details class="dd"><summary>Services</summary><div class="dd-panel">{''.join(cols)}</div></details>
<a href="geometre-expert-nice.html">Zone d’intervention</a>
<a href="cabinet-adrien-arnal.html">Le cabinet</a>
<a href="contact.html">Contact</a>
<a class="phone" href="tel:{PHONE_INTL}" data-cta="header-phone">{PHONE}</a>
<a class="btn btn-red btn-sm" href="contact.html" data-cta="header-devis">Devis {ICON_ARROW}</a>
</nav>
<details class="menu-btn"><summary>Menu</summary><div class="menu-panel">
<a href="contact.html"><b>Demander un devis</b></a><a href="tel:{PHONE_INTL}">Appeler le {PHONE}</a>{mob}
<p class="nav-h">Le cabinet</p><a href="cabinet-adrien-arnal.html">Adrien Arnal, géomètre-expert</a><a href="geometre-expert-nice.html">Zone d’intervention</a><a href="contact.html">Contact</a>
</div></details>
</div></div></header>"""

def footer_html():
    svc = "".join(f'<li><a href="{s}.html">{esc(SERVICES[s]["nav"])}</a></li>' for p in PILLARS for s in p["pages"])
    return f"""<footer class="site-footer"><div class="wrap"><div class="footer-card">
<div><a class="logo" href="index.html" style="display:inline-block"><img src="assets/logo.svg" alt="GE Metric Géomètre-Expert" width="80" height="84"></a>
<address><b>GE Metric</b><span>{ADDRESS[0]}</span><span>{ADDRESS[1]} {ADDRESS[2].upper()}</span><a href="tel:{PHONE_INTL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></address></div>
<div><p class="nav-h">Services</p><ul>{svc}</ul></div>
<div><p class="nav-h">Cabinet</p><ul><li><a href="cabinet-adrien-arnal.html">Adrien Arnal</a></li><li><a href="geometre-expert-nice.html">Zone d’intervention</a></li><li><a href="contact.html">Contactez-nous</a></li><li><a href="mentions-legales.html">Mentions légales</a></li><li><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></li></ul></div>
</div></div>
<div class="foot-legal"><div class="wrap"><span>SASU GE METRIC · Société de Géomètres-Experts · Ordre des Géomètres-Experts n° STR_00000186 · RCS 992 581 470 NICE</span><span>Copyright © 2026 Gemetric</span></div></div>
</footer>
<div class="mbar"><a class="btn btn-light" href="tel:{PHONE_INTL}" data-cta="mbar-phone">{ICON_PHONE}Appeler</a><a class="btn btn-red" href="contact.html" data-cta="mbar-devis">Demander un devis</a></div>
<script src="assets/site.js" defer></script>"""

def crumbs_html(items):
    lis = "".join(f'<li><a href="{"index" if s=="index" else s}.html">{esc(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{esc(n)}</li>' for i, (n, s) in enumerate(items))
    return f'<nav class="crumbs wrap" aria-label="Fil d’Ariane"><ol>{lis}</ol></nav>'

VARIANTS = ["dark", "red", "light", "photo:port", "light", "dark", "photo:monaco", "light"]
def card(href, tag, title, sub="", variant="light", eager=False):
    bg = ""
    cls = variant
    if variant.startswith("photo:"):
        key = variant.split(":")[1]; cls = "photo"
        bg = img_tag(key, cls="card-bg", sizes="(max-width: 760px) 100vw, 300px")
    sub_html = f'<span class="card-sub">{esc(sub)}</span>' if sub else ""
    return f'<a class="card card-{cls} rv" href="{href}">{bg}<span class="card-tag">{esc(tag)}</span><span class="card-body"><b class="card-title">{esc(title)}</b>{sub_html}</span>{CORNER}</a>'

def marquee():
    items = []
    photos = ["nice", "port", "monaco", "nice"]
    i = 0
    for p in PILLARS:
        for s in p["pages"]:
            items.append(f'<a class="mq-pill" href="{s}.html">{esc(SERVICES[s]["nav"])}</a>')
            if len(items) % 3 == 2:
                items.append(f'<span class="mq-photo">{img_tag(photos[i % 4], sizes="140px")}</span>'); i += 1
    track = "".join(items)
    dup = track.replace('<a class="mq-pill"', '<a tabindex="-1" class="mq-pill"')
    return f'<section class="marquee" aria-label="Nos missions"><div class="mq-track"><div class="mq-group">{track}</div><div class="mq-group" aria-hidden="true">{dup}</div></div></section>'

def band(title, text, key=None):
    href = "contact.html" + (f"#{key}" if key else "")
    return f"""<section class="band-wrap"><div class="wrap"><div class="band rv">
<div><h2>{esc(title)}</h2><p>{esc(text)}</p></div>
<div><div class="cta-row"><a class="btn btn-red" href="{href}" data-cta="band-devis">Demander un devis {ICON_ARROW}</a><a class="btn btn-ghost" href="tel:{PHONE_INTL}" data-cta="band-phone">{ICON_PHONE}{PHONE}</a></div>
</div>
</div></div></section>"""

TRUST = ['Inscrit à l’Ordre des Géomètres-Experts', 'Assermenté depuis 2020', 'Assuré RC pro &amp; décennale']
def trust_html():
    return '<ul class="trust">' + "".join(f"<li>{t}</li>" for t in TRUST) + "</ul>"

def faq_html(faq):
    return '<div class="faq rv">' + "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>' for q, a in faq) + "</div>"

def doc(slug, title, desc, schema, body, artifact=False, short=None):
    head = head_tags(slug, title, desc, schema, short or title)
    main = f'<a class="skip" href="#contenu">Aller au contenu</a>\n{nav_html()}\n<main id="contenu">{body}</main>\n{footer_html()}'
    if artifact and slug == "index":
        return head + "\n" + main + "\n"
    return f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{main}\n</body>\n</html>\n'

# ---------------------------------------------------------------- pages
def service_page(slug, s):
    p = PILLAR[s["pillar"]]
    items = [("Accueil", "index"), (p["name"], p["pages"][0]), (s["nav"], slug)]
    if p["pages"][0] == slug: items = [("Accueil", "index"), (s["nav"], slug)]
    dl = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in s["answer_dl"])
    pains = "".join(f'<div class="pain"><span class="tag">{esc(t)}</span><h3>{esc(h)}</h3><p>{esc(x)}</p></div>' for t, h, x in s["pains"])
    deliv = "".join(f"<li><div><b>{esc(b)}</b><span>{esc(x)}</span></div></li>" for b, x in s["deliverables"])
    steps = "".join(f"<li><h3>{esc(h)}</h3><p>{esc(x)}</p></li>" for h, x in s["steps"])
    legal = s["legal"]
    rel = "".join(card(f"{r}.html", PILLAR[SERVICES[r]["pillar"]]["name"], SERVICES[r]["nav"], variant=["dark","red","light"][k % 3]) for k, r in enumerate(s["related"]))
    dlrow = "".join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in s["answer_dl"])
    pains = "".join(f'<details class="pain-card"><summary><span class="tag">{esc(t)}</span><span class="pain-q">{esc(h)}</span></summary><p>{esc(x)}</p></details>' for t, h, x in s["pains"])
    flow = ""
    for k, (h, x, recv) in enumerate(FLOW[slug]):
        chips = "".join(f'<li>{esc(r)}</li>' for r in recv)
        flow += f'<li class="{"has-recv" if recv else ""}"><span class="flow-n">{k+1}</span><h3>{esc(h)}</h3><p>{esc(x)}</p>' + (f'<ul class="recv" aria-label="Vous recevez">{chips}</ul>' if recv else "") + "</li>"
    body = f"""{crumbs_html(items)}
<section class="hero hero-lp"><div class="wrap hero-split">
<div class="panel hero-copy">
<span class="eyebrow">{esc(s["eyebrow"])} · Nice</span>
<h1>{s["h1"]}</h1>
<p class="lede">{esc(s["lede"])}</p>
<div class="cta-row"><a class="btn btn-red" href="contact.html#{s["pillar"]}" data-cta="hero-devis">Demander un devis {ICON_ARROW}</a></div>
</div>
<div class="hero-plan">{plan_svg(s["plan"], "Illustration : " + s["nav"])}</div>
</div></section>

<section class="brief-wrap" aria-labelledby="enbref"><div class="wrap"><div class="brief brief-grid rv">
<p class="brief-text"><b id="enbref">En bref.</b> {esc(s["answer"])}</p>
<dl class="brief-dl">{dlrow}</dl>
</div></div></section>

<section class="section tex-tri"><div class="wrap">
<div class="sec-head rv"><h2>{esc(s["pains_title"])}</h2></div>
<div class="pain-grid rv-group pains-{3 if len(s["pains"])==3 else 2}">{pains}</div>
</div></section>
{terrain_section(slug)}
<section class="section section-alt"><div class="wrap">
<div class="sec-head rv"><h2>Les étapes, et ce que vous recevez</h2></div>
<ol class="flow rv-group">{flow}</ol>
</div></section>

<section class="section tex-tri tex-left"><div class="wrap">
<div class="sec-head rv"><h2>{esc(s["nav"])} : vos questions</h2></div>
{faq_html(s["faq"])}
<div class="callout callout-inline"><h3>{esc(legal["title"])}</h3>{''.join(f"<p>{esc(x)}</p>" for x in legal["paras"])}</div>
</div></section>

<section class="section section-alt"><div class="wrap">
<div class="sec-head rv"><h2>Ces missions vont souvent ensemble</h2></div>
<div class="cards cards-3">{rel}</div>
</div></section>
{band(s["cta_title"], s["cta_text"], s["pillar"])}"""
    schema = ld(service_schema(slug, s), faq_schema(s["faq"]), crumbs_schema(items))
    return s["title"], s["desc"], schema, body

def home_page():
    router = "".join(f'<a href="{sl}.html"><small>{esc(PILLAR[SERVICES[sl]["pillar"]]["name"])}</small><b>{esc(q)}</b><span>{esc(sub)}</span></a>' for sl, q, sub in HOME_ROUTER)
    svcs = ""
    for i, p in enumerate(PILLARS):
        links = "".join(f'<li><a href="{s}.html">{esc(SERVICES[s]["nav"])}</a></li>' for s in p["pages"])
        svcs += f'<article class="svc"><div class="svc-top"><h3>{esc(p["name"])}</h3></div><p>{p["desc"].split(". ")[0].rstrip(".")}.</p><ul>{links}</ul></article>'
    bio = f"<p>{esc(BIO[0])}</p><p><a href=\"cabinet-adrien-arnal.html\">Découvrir le cabinet →</a></p>"
    router = "".join(card(f"{sl}.html", PILLAR[SERVICES[sl]["pillar"]]["name"], q, sub, VARIANTS[k % len(VARIANTS)]) for k, (sl, q, sub) in enumerate(HOME_ROUTER))
    B = [(842, 312), (950, 296), (968, 360), (854, 380)]
    edges = ""
    for k in range(4):
        (x1, y1), (x2, y2) = B[k], B[(k + 1) % 4]
        edges += f'<line class="hl-edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" pathLength="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin="{1.6 + k:.1f}s" dur=".25s" fill="freeze"/></line>'
    bornes = "".join(f'<g class="hl-b"><circle cx="{x}" cy="{y}" r="0" class="hl-dot"><animate attributeName="r" values="0;8;5" begin="{0.8 + k:.1f}s" dur=".45s" fill="freeze"/></circle><circle cx="{x}" cy="{y}" r="6" class="hl-ring"><animate attributeName="r" values="6;20" begin="{0.8 + k:.1f}s" dur="1.2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" begin="{0.8 + k:.1f}s" dur="1.2s" repeatCount="indefinite"/></circle><text x="{x + (12 if k in (1, 2) else -12)}" y="{y + (20 if k in (2, 3) else -10)}" text-anchor="{'start' if k in (1, 2) else 'end'}" class="hl-lbl" opacity="0">B{k+1}<set attributeName="opacity" to="1" begin="{0.9 + k:.1f}s"/></text></g>' for k, (x, y) in enumerate(B))
    xs = ";".join(str(B[k][0]) for k in [0, 0, 1, 1, 2, 2, 3, 3, 0]); ys = ";".join(str(B[k][1]) for k in [0, 0, 1, 1, 2, 2, 3, 3, 0])
    kt = "0;.2;.25;.45;.5;.7;.75;.95;1"
    poly = " ".join(f"{x},{y}" for x, y in B)
    scene = f"""<svg class="hl-svg" viewBox="0 0 1024 434" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter></defs>
<polygon class="hl-fill" points="{poly}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="4.9s" dur=".8s" fill="freeze"/></polygon>
{edges}
<g opacity="0"><set attributeName="opacity" to="1" begin="5.1s"/>
<text class="hl-cote" x="872" y="296" transform="rotate(-8 872 296)">11,84 m</text><text class="hl-cote" x="945" y="318" transform="rotate(74 945 318)">7,46 m</text></g>
<g class="hl-laser" opacity="0"><set attributeName="opacity" to="1" begin=".8s"/>
<line x1="735" y1="100" x2="{B[0][0]}" y2="{B[0][1]}" class="hl-beam-glow" filter="url(#glow)"><animate attributeName="x2" values="{xs}" keyTimes="{kt}" dur="4s" begin=".8s" repeatCount="indefinite"/><animate attributeName="y2" values="{ys}" keyTimes="{kt}" dur="4s" begin=".8s" repeatCount="indefinite"/></line>
<line x1="735" y1="100" x2="{B[0][0]}" y2="{B[0][1]}" class="hl-beam"><animate attributeName="x2" values="{xs}" keyTimes="{kt}" dur="4s" begin=".8s" repeatCount="indefinite"/><animate attributeName="y2" values="{ys}" keyTimes="{kt}" dur="4s" begin=".8s" repeatCount="indefinite"/></line>
<circle r="4" class="hl-hit" cx="{B[0][0]}" cy="{B[0][1]}"><animate attributeName="cx" values="{xs}" keyTimes="{kt}" dur="4s" begin=".8s" repeatCount="indefinite"/><animate attributeName="cy" values="{ys}" keyTimes="{kt}" dur="4s" begin=".8s" repeatCount="indefinite"/></circle>
<circle cx="735" cy="100" r="5" class="hl-src"/></g>
{bornes}
</svg>"""
    pills = [("bornage-terrain-nice", "J’ai un doute sur mes limites", "Bornage", "nice", "35% 40%"),
             ("division-parcellaire-nice", "Je divise mon terrain", "Division parcellaire", "nice", "85% 45%"),
             ("plan-topographique-nice", "Je construis ou j’agrandis", "Plan topographique", "station", "75% 40%"),
             ("etat-descriptif-division-copropriete", "Je vends ou réunis des lots", "Copropriété", "port", "50% 70%")]
    def med(key, pos):
        src = "assets/station-totale-geometre-expert.jpg" if key == "station" else PHOTOS[key]["src"].replace("-1600", "-900")
        return f'<span class="med"><img src="{src}" alt="" width="88" height="88" style="object-position:{pos}" decoding="async"></span>'
    pill_html = "".join(f'<a class="hp-pill" href="{sl}.html" data-cta="hero-pill-{sl}">{med(k, pos)}<span class="hp-txt"><b>{esc(t)}</b><small>{esc(sv)}</small></span><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 17 17 7M8 7h9v9"/></svg></span></a>' for sl, t, sv, k, pos in pills)
    body = f"""<section class="hero hero-live"><div class="wrap"><div class="hl-card">
<div class="hl-scene"><img src="assets/station-totale-geometre-expert.jpg" alt="Station totale de géomètre-expert en train de relever les bornes d’une parcelle" width="1024" height="434" fetchpriority="high" decoding="async">{scene}
<span class="hl-status"><i></i>Relevé en cours</span></div>
<div class="hl-copy">
<span class="eyebrow">Géomètre-Expert · Côte d'Azur &amp; Monaco</span>
<h1><span class="nw">Géomètre-expert</span> à <em>Nice</em> et Monaco</h1>
<p class="hl-sub">Vos limites, mesurées au centimètre. <span>Dites-nous votre projet :</span></p>
<div class="hp-grid">{pill_html}</div>
<div class="hl-foot"><a class="btn btn-red" href="contact.html" data-cta="hero-devis">Demander un devis {ICON_ARROW}</a><a class="link-phone" href="tel:{PHONE_INTL}" data-cta="hero-phone">{ICON_PHONE}{PHONE}</a><a class="hl-more" href="#projet">Autre projet ↓</a></div>
</div>
</div></div></section>

<section class="section tex-tri" id="projet"><div class="wrap">
<div class="sec-split"><span class="tag-pill">Toutes nos missions</span><h2>Votre situation n’est pas dans la liste ?</h2></div>
<div class="cards cards-4">{router}</div>
</div></section>
{marquee()}

<section class="section"><div class="wrap">
<div class="sec-split"><span class="tag-pill">Le cabinet</span><h2>Notre géomètre expert : Adrien Arnal</h2></div>
<div class="expert rv">
<figure><img src="assets/adrien-arnal-geometre-expert.jpg" alt="Adrien Arnal, géomètre-expert, fondateur de GE Metric à Nice" width="300" height="300" loading="lazy"><figcaption>Adrien Arnal · Géomètre-Expert · Fondateur</figcaption></figure>
<div class="prose"><p class="lede">Géomètre-expert diplômé de l’ESGT, assermenté depuis 2020, fondateur de GE Metric à Nice.</p><p><a href="cabinet-adrien-arnal.html">Découvrir le cabinet →</a></p></div>
</div>
</div></section>

<section class="stats">
<img class="stats-bg" src="assets/nice-baie-des-anges-1600.jpg" alt="" width="1600" height="1067" loading="lazy" decoding="async">
<div class="wrap stats-grid">
<div class="stat rv"><span class="stat-n"><b data-count="14">14</b><sup>ans</sup></span><span class="stat-l">dans la profession, depuis l’ESGT</span></div>
<div class="stat rv"><span class="stat-n"><b>2020</b></span><span class="stat-l">serment auprès de l’Ordre des Géomètres-Experts</span></div>
<div class="stat rv"><span class="stat-n"><b data-count="9">9</b></span><span class="stat-l">missions, du bornage au scan 3D</span></div>
<div class="stat rv"><span class="stat-n"><b data-count="4">4</b></span><span class="stat-l">domaines d’intervention</span></div>
</div></section>

<section class="section section-alt"><div class="wrap split">
<div class="callout rv"><h3>Pourquoi choisir un géomètre-expert ?</h3>
<p>Lui seul peut fixer les limites de propriété (loi du 7 mai 1946) et établir les plans de copropriété (Cass., 29 juin 2022).</p></div>
<div class="rv"><div class="sec-head" style="margin-bottom:1rem"><h3 style="font-size:1.5rem">Basé à Nice, sur toute la Côte d’Azur et à Monaco</h3></div>
{figure("nice", "60% 40%", "photo photo-card", sizes="(max-width: 860px) 100vw, 560px")}
<a class="btn btn-white" href="geometre-expert-nice.html">Voir la zone d’intervention {ICON_ARROW}</a></div>
</div></section>

<section class="section tex-tri tex-left"><div class="wrap">
<div class="sec-head rv"><h2>Faire appel à un géomètre-expert</h2></div>
{faq_html(HOME_FAQ)}
</div></section>
{band("Un projet à nous confier ?", "Décrivez-le avec l’adresse du bien : nous revenons vers vous avec un devis.")}"""
    schema = ld(org_schema(), person_schema(), faq_schema(HOME_FAQ),
                {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "GE Metric", "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}})
    return ("Géomètre-Expert à Nice, Côte d’Azur & Monaco | GE Metric",
            "GE Metric, géomètre-expert à Nice : bornage, division parcellaire, plan topographique, copropriété, relevé d’architecte et 3D sur la Côte d’Azur et à Monaco. Devis : 04 93 16 29 60.",
            schema, body)

def zone_page():
    items = [("Accueil", "index"), ("Géomètre-expert à Nice", "geometre-expert-nice")]
    zl = "".join(f"<li>{esc(n)}<span>{c}</span></li>" for n, c in ZONES)
    svc = "".join(card(f"{s}.html", p["name"], SERVICES[s]["nav"], variant=["dark","red","light","light"][k % 4]) for k, (p, s) in enumerate((p, s) for p in PILLARS for s in p["pages"]))
    faq = [("Quel PLU s’applique à Nice ?", "Le PLU métropolitain de la Métropole Nice Côte d’Azur. D’autres communes de la zone ont leur propre document : nous vérifions celui de votre parcelle."),
           ("Le déplacement est-il facturé ?", "Le devis tient compte de la localisation de la mission, notamment du temps de trajet depuis le bureau.")]
    body = f"""{crumbs_html(items)}
<section class="hero-city-wrap"><div class="wrap"><div class="hero-photo hero-city">
<img class="hero-photo-img" src="assets/nice-baie-des-anges-1600.jpg" srcset="assets/nice-baie-des-anges-900.jpg 900w, assets/nice-baie-des-anges-1600.jpg 1600w" sizes="100vw" alt="Vue sur la baie des Anges et les collines de Nice depuis la colline du Château" width="1600" height="1067" fetchpriority="high" decoding="async">
<div class="wrap hero-photo-inner">
<div class="hero-copy"><span class="eyebrow">Zone d’intervention</span>
<h1>Géomètre-expert à <em>Nice</em>, sur la Côte d’Azur et à Monaco</h1>
<p class="lede">Un cabinet local, qui connaît les pentes, les restanques et les règles d’urbanisme de la Riviera.</p>
<div class="cta-row"><a class="btn btn-red" href="contact.html" data-cta="hero-devis">Demander un devis {ICON_ARROW}</a><a class="btn btn-ghost" href="tel:{PHONE_INTL}" data-cta="hero-phone">{ICON_PHONE}{PHONE}</a></div>
<p class="hero-addr">GE Metric · {ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]}</p>
</div></div></div></div></section>
<section class="section tex-tri"><div class="wrap">
<div class="sec-head rv"><h2>Où intervenons-nous ?</h2></div>
<ul class="zones rv">{zl}</ul>
<p class="cta-note" style="margin-top:1rem">Liste non exhaustive.</p>
</div></section>
<section class="section section-alt"><div class="wrap">
<div class="sec-head rv"><h2>Du port de Nice à Monaco</h2></div>
<div class="gallery gallery-2">{figure("port", None, "photo", sizes="(max-width: 860px) 50vw, 580px")}{figure("monaco", None, "photo", sizes="(max-width: 860px) 50vw, 580px")}</div>
</div></section>
<section class="section section-alt"><div class="wrap">
<div class="sec-head rv"><h2>Nos missions à Nice et sur la Côte d’Azur</h2></div>
<div class="cards cards-3">{svc}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head rv"><h2>Questions fréquentes</h2></div>{faq_html(faq)}</div></section>
{band("Un projet sur la Côte d’Azur ?", "Indiquez l’adresse du bien : nous vous rappelons.")}"""
    return ("Géomètre-Expert Nice, Côte d’Azur et Monaco | Cabinet GE Metric",
            "Cabinet de géomètre-expert basé 142 avenue de la Clua à Nice. Interventions sur la Côte d’Azur et à Monaco : bornage, topographie, copropriété, relevés. 04 93 16 29 60.",
            ld(org_schema(), faq_schema(faq), crumbs_schema(items)), body)

def cabinet_page():
    items = [("Accueil", "index"), ("Le cabinet", "cabinet-adrien-arnal")]
    bio = "".join(f"<p>{esc(b)}</p>" for b in BIO)
    body = f"""{crumbs_html(items)}
<section class="hero"><div class="wrap"><div class="panel expert">
<figure><img src="assets/adrien-arnal-geometre-expert.jpg" alt="Portrait d’Adrien Arnal, géomètre-expert à Nice" width="300" height="300"><figcaption>Adrien Arnal · Géomètre-Expert</figcaption></figure>
<div class="hero-copy"><span class="eyebrow">Le cabinet</span><h1>Notre géomètre expert : <em>Adrien Arnal</em></h1>
<div class="prose">{bio}</div>
<div class="cta-row"><a class="btn btn-red" href="contact.html" data-cta="hero-devis">Demander un devis {ICON_ARROW}</a><a class="btn btn-white" href="{LINKEDIN}" target="_blank" rel="noopener">Profil LinkedIn</a></div>
</div></div></div></section>
<section class="section"><div class="wrap split">
<div><div class="sec-head rv"><h2>GE Metric</h2><p>{esc(CABINET)}</p></div>{figure("port", None, "photo photo-card photo-card-tall", sizes="(max-width: 860px) 100vw, 560px")}</div>
<dl class="nap">
<div><dt>Société</dt><dd>SASU GE METRIC, Société de Géomètres-Experts au capital de 5 000 euros</dd></div>
<div><dt>Ordre</dt><dd>Inscrite à l’Ordre des Géomètres-Experts sous le numéro STR_00000186 depuis le 16/10/2025</dd></div>
<div><dt>Siège</dt><dd>{ADDRESS[0]} – {ADDRESS[1]} {ADDRESS[2].upper()}</dd></div>
<div><dt>Assurance</dt><dd>Responsabilité civile professionnelle et décennale : MMA IARD Assurances Mutuelles / MMA IARD, par le courtier SOPHIASSUR</dd></div>
<div><dt>RCS</dt><dd>992 581 470 NICE – SIRET 992 581 470 00018</dd></div>
</dl></div></section>
<section class="section section-alt"><div class="wrap"><div class="sec-head rv"><h2>Quatre domaines d’intervention</h2></div>
<div class="cards cards-4">{''.join(card(f'{p["pages"][0]}.html', "Pôle", p["name"], variant=["dark","red","light","photo:monaco"][k]) for k, p in enumerate(PILLARS))}</div></div></section>
{band("Parlons de votre projet", "Nous prenons le temps d’expliquer les enjeux.")}"""
    return ("Adrien Arnal, Géomètre-Expert à Nice | Le cabinet GE Metric",
            "Adrien Arnal, géomètre-expert diplômé de l’ESGT, assermenté auprès de l’Ordre en 2020, fondateur de GE Metric à Nice en 2025. Rigueur, écoute et pédagogie.",
            ld(person_schema(), org_schema(), crumbs_schema(items)), body)

def contact_page():
    items = [("Accueil", "index"), ("Contactez-nous", "contact")]
    opts = "".join(f'<option data-key="{p["key"]}" value="{esc(p["option"])}">{esc(p["option"])}</option>' for p in PILLARS)
    body = f"""{crumbs_html(items)}
<section class="hero"><div class="wrap hero-grid">
<div class="panel hero-copy"><span class="eyebrow">Demander un devis</span><h1>Contactez-nous</h1>
<p class="lede">N'hésitez pas à nous contacter ! Nous sommes disponibles pour toutes questions et estimations.</p>
<form class="form" id="devis-form" novalidate>
<div class="row"><div class="field"><label for="f-nom">Nom *</label><input id="f-nom" name="nom" required autocomplete="name"></div>
<div class="field"><label for="f-tel">Numéro de téléphone *</label><input id="f-tel" name="tel" type="tel" required autocomplete="tel"></div></div>
<div class="row"><div class="field"><label for="f-email">E-mail *</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="f-service">Vous êtes intéressé pour</label><select id="f-service" name="service">{opts}<option data-key="autre" value="Autre / je ne sais pas">Autre / je ne sais pas</option></select></div></div>
<div class="row"><div class="field"><label for="f-adresse">Adresse du bien</label><input id="f-adresse" name="adresse" autocomplete="street-address"></div>
<div class="field"><label for="f-delai">Échéance souhaitée</label><select id="f-delai" name="delai"><option>Dès que possible</option><option>Dans le mois</option><option>Dans les 3 mois</option><option>Pas d’échéance précise</option></select></div></div>
<div class="field"><label for="f-message">Message</label><textarea id="f-message" name="message" placeholder="Ex. : je souhaite vendre une partie de mon terrain à Nice, environ 1 200 m², accès par un chemin privé."></textarea></div>
<p class="legal">Les informations recueillies par nos formulaires nous sont transmises par mail et sont destinées à un usage interne uniquement.</p>
<div class="cta-row"><button class="btn btn-red" type="submit" data-cta="form-submit">Envoyer ma demande {ICON_ARROW}</button><span class="cta-note">* champs obligatoires</span></div>
</form>
<div class="form-done" id="devis-done" hidden>
<h2 class="h3">Votre demande est prête</h2>
<p>Envoyez-la à <b style="user-select:all">{EMAIL}</b> : ouvrez votre messagerie avec le bouton ci-dessous, ou copiez le texte. Vous pouvez aussi appeler le <b style="user-select:all">{PHONE}</b>.</p>
<pre id="devis-text"></pre>
<div class="cta-row"><a class="btn btn-red" id="devis-mailto" href="mailto:{EMAIL}">Ouvrir ma messagerie</a><button class="btn btn-line" type="button" id="devis-copy">Copier la demande</button><button class="btn btn-line" type="button" id="devis-edit">Modifier</button></div>
</div>
</div>
<aside class="answer"><div class="answer-head"><span>Coordonnées</span><span>GE Metric</span></div>
<div class="answer-body"><dl><dt>Téléphone</dt><dd><a href="tel:{PHONE_INTL}" style="user-select:all">{PHONE}</a></dd><dt>E-mail</dt><dd><a href="mailto:{EMAIL}" style="user-select:all">{EMAIL}</a></dd><dt>Adresse</dt><dd>{ADDRESS[0]}<br>{ADDRESS[1]} {ADDRESS[2].upper()}</dd><dt>Zone</dt><dd>Côte d'Azur &amp; Monaco</dd></dl>
</div></aside>
</div></section>"""
    return ("Contact et devis | GE Metric, Géomètre-Expert à Nice",
            "Contactez GE Metric, géomètre-expert à Nice : 04 93 16 29 60, contact@gemetric.fr, 142 avenue de la Clua 06100 Nice. Demande de devis en ligne.",
            ld(org_schema(), crumbs_schema(items)), body)

def legal_page():
    items = [("Accueil", "index"), ("Mentions légales", "mentions-legales")]
    L = open(os.path.join(os.path.dirname(__file__), "mentions.html"), encoding="utf-8").read()
    body = f"""{crumbs_html(items)}<section class="section"><div class="wrap"><div class="sec-head"><h1>Mentions légales</h1></div><div class="legal-doc">{L}</div></div></section>"""
    return ("Mentions légales et CGV | GE Metric", "Mentions légales et conditions générales de vente de la SASU GE METRIC, société de géomètres-experts à Nice.",
            ld(crumbs_schema(items)), body)

# ---------------------------------------------------------------- write
def build(out, artifact):
    os.makedirs(out, exist_ok=True)
    pages = {"index": home_page(), "geometre-expert-nice": zone_page(), "cabinet-adrien-arnal": cabinet_page(),
             "contact": contact_page(), "mentions-legales": legal_page()}
    for sl, s in SERVICES.items(): pages[sl] = service_page(sl, s)
    for sl, (t, d, sc, b) in pages.items():
        with open(os.path.join(out, sl + ".html"), "w", encoding="utf-8") as f:
            f.write(doc(sl, t, d, sc, b, artifact=artifact))
    return pages

pages = build(OUT_PROD, False)
build(OUT_ART, True)

# SEO / GEO files (prod)
with open(os.path.join(OUT_PROD, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for sl in pages: f.write(f"  <url><loc>{url(sl)}</loc><lastmod>2026-10-17</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(OUT_PROD, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\n# Moteurs de réponse IA autorisés (GEO)\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(OUT_PROD, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(f"# GE Metric — Géomètre-Expert à Nice\n\n> {TAGLINE} {CABINET}\n\n")
    f.write(f"- Géomètre-expert : Adrien Arnal (ESGT 2012, serment auprès de l’Ordre des Géomètres-Experts en mars 2020), fondateur en 2025\n- Société : SASU GE METRIC, Ordre des Géomètres-Experts n° STR_00000186, RCS 992 581 470 Nice\n- Adresse : {ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]}\n- Téléphone : {PHONE} · E-mail : {EMAIL}\n- Zone d’activité principale : Côte d’Azur & Monaco\n\n## Services\n\n")
    for p in PILLARS:
        f.write(f"### {p['name']}\n\n")
        for s in p["pages"]:
            f.write(f"- [{SERVICES[s]['nav']}]({url(s)}) : {SERVICES[s]['answer']}\n")
        f.write("\n")
    f.write(f"## Pages\n\n- [Accueil]({url('index')})\n- [Zone d’intervention]({url('geometre-expert-nice')})\n- [Le cabinet]({url('cabinet-adrien-arnal')})\n- [Contact]({url('contact')})\n- [Mentions légales]({url('mentions-legales')})\n")
print("ok", len(pages), "pages")
