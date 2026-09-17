# -*- coding: utf-8 -*-
"""Briques partagées par les générateurs : <head>, header, newsletter, footer, icônes.

Un seul endroit pour le menu et le pied de page : si une catégorie change de nom,
elle change partout. R est le préfixe relatif vers la racine ("" à l'accueil,
"../" sur une catégorie, "../../" sur un article)."""
import json, os
import config as C
from categories import CATS

HERE = os.path.dirname(os.path.abspath(__file__))

ICON_SEARCH = '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M16 16l5 5"/></svg>'
BURGER = '<svg width="22" height="14" viewBox="0 0 22 14" fill="none" stroke="#111" stroke-width="1.7"><path d="M0 1h22M0 7h22M0 13h22"/></svg>'
ARROW = '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def strip(t):
    return t.replace("&amp;", "&").replace("<b>", "").replace("</b>", "").replace("<em>", "").replace("</em>", "")

def cat(slug):
    for c in CATS:
        if c["slug"] == slug:
            return c
    raise SystemExit(f"catégorie inconnue : {slug} (connues : {[c['slug'] for c in CATS]})")

# ---------------------------------------------------------------- logos
def _logo_exts():
    d = os.path.join(HERE, "assets", "logos")
    out = {}
    if os.path.isdir(d):
        for f in os.listdir(d):
            slug, ext = os.path.splitext(f)
            if ext in (".svg", ".png", ".jpg", ".webp", ".ico"):
                out.setdefault(slug, ext.lstrip("."))
                if ext == ".svg":
                    out[slug] = "svg"
    return out

LOGO_EXT = _logo_exts()

def logo_src(R, slug):
    if slug not in LOGO_EXT:
        raise SystemExit(f"logo absent : assets/logos/{slug}.(svg|png) ; lance scripts/fetch_logos.py")
    return f'{R}assets/logos/{slug}.{LOGO_EXT[slug]}'

def _exists(rel):
    return os.path.exists(os.path.join(HERE, rel))

# ---------------------------------------------------------------- head
def head(R, title, desc, canonical, extra="", og_type="website", og_image=None):
    icons = f'<link rel="icon" href="{R}assets/logo/favicon.svg" type="image/svg+xml">'
    if _exists("assets/logo/favicon-32.png"):
        icons += f'\n<link rel="icon" type="image/png" sizes="32x32" href="{R}assets/logo/favicon-32.png">'
    if _exists("assets/logo/apple-touch-icon.png"):
        icons += f'\n<link rel="apple-touch-icon" href="{R}assets/logo/apple-touch-icon.png">'
    og_img = f'\n<meta property="og:image" content="{og_image}">' if og_image else ""
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{C.NOM}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">{og_img}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{C.FONTS_HREF}" rel="stylesheet">
{icons}
<meta name="theme-color" content="{C.ACCENT}">
<link rel="stylesheet" href="{R}assets/css/site.css?v={C.CSS_V}">
{extra}'''

# ---------------------------------------------------------------- header
def header(R, current=None, scrolled=False):
    menu = ""
    for c in CATS:
        style = ' style="text-decoration:underline;text-underline-offset:6px"' if c["slug"] == current else ""
        menu += f'      <li><a href="{R}{c["slug"]}/"{style}>{c["menu"]}</a></li>\n'
    home = R if R else "./"
    return f'''<header{' class="scrolled"' if scrolled else ''}>
  <div class="wrap nav">
    <a class="logo" href="{home}" aria-label="{C.NOM}, accueil"><img class="l-light" src="{R}assets/logo/logo-light.svg" alt="{C.NOM}" width="620" height="133"><img class="l-dark" src="{R}assets/logo/logo.svg" alt="" aria-hidden="true" width="620" height="133"></a>
    <ul class="menu">
{menu}    </ul>
    <div class="nav-actions">
      <a class="iconbtn" href="{R}#outil" aria-label="Rechercher">{ICON_SEARCH}</a>
      <a class="btn btn-dark" href="{R}#outil">{C.CTA}</a>
      <button class="burger" aria-label="Menu">{BURGER}</button>
    </div>
  </div>
</header>'''

# ---------------------------------------------------------------- newsletter
def newsletter(h2, p=None):
    return f'''<section class="news" id="newsletter">
  <div class="wrap">
    <div class="news-card">
      <div>
        <h2>{h2}</h2>
        <p>{p or C.NEWSLETTER_P}</p>
      </div>
      <div>
        <form class="form" onsubmit="return false">
          <input type="email" placeholder="Votre adresse email" aria-label="Adresse email" required>
          <button class="btn btn-yellow" type="submit">Je m'inscris</button>
        </form>
        <p class="form-note">{C.NEWSLETTER_NOTE}</p>
      </div>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- footer
def footer(R):
    home = R if R else "./"
    cats = "".join(f'<li><a href="{R}{c["slug"]}/">{c["nom"]}</a></li>' for c in CATS)
    brands = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in C.FOOTER_BRANDS)
    return f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand"><a class="logo" href="{home}" aria-label="{C.NOM}, accueil"><img src="{R}assets/logo/logo.svg" alt="{C.NOM}" width="620" height="133" loading="lazy"></a><p>{C.BASELINE}</p></div>
      <div><h4>Comparatifs</h4><ul>{cats}</ul></div>
      <div><h4>{C.UNIT.capitalize()}</h4><ul>{brands}<li><a href="{R}#marques">Toutes les {C.UNIT}</a></li></ul></div>
      <div><h4>À propos</h4><ul><li><a href="{R}#methode">Notre méthode</a></li><li><a href="{R}a-propos/">Qui sommes-nous</a></li><li><a href="{R}a-propos/#contact">Contact</a></li><li><a href="{R}mentions-legales/">Mentions légales</a></li></ul></div>
    </div>
    <div class="foot-bottom"><span>© 2026 {C.NOM}. {C.TAGLINE_FOOTER}</span><span>Les logos appartiennent à leurs propriétaires respectifs.</span></div>
  </div>
</footer>

<script src="{R}assets/js/site.js?v={C.CSS_V}"></script>'''

def jsonld(*dicts):
    return "".join('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n" for d in dicts)

def org():
    return {"@context": "https://schema.org", "@type": "Organization", "name": C.NOM, "url": C.SITE + "/",
            "logo": f"{C.SITE}/assets/logo/logo.svg", "description": strip(C.BASELINE)}

def write(path, html):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    print("ok", path)
