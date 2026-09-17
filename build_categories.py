# -*- coding: utf-8 -*-
"""Génère les pages catégorie (<slug>/index.html) depuis categories.py (CATS, SUBIMG) + les articles.
Les blocs feat / side / grid sont facultatifs : sans eux, ils se remplissent avec les articles publiés
(jamais de lien mort). Usage : python3 build_categories.py"""
import os
import config as C
from common import head, header, footer, newsletter, logo_src, strip, jsonld, write, ARROW
from categories import CATS, SUBIMG
from contenus import ARTICLES, by_cat, get, card
from linkify import linkify

def subimg(c, label):
    m = SUBIMG.get(c["slug"], {})
    if label not in m:
        raise SystemExit(f'SUBIMG[{c["slug"]!r}] n\'a pas d\'image pour la sous-catégorie {label!r}')
    return m[label]

def render(c):
    R = "../"
    mine = by_cat(c["slug"])
    others = [a for a in ARTICLES if a["cat"] != c["slug"]]
    if not mine:
        raise SystemExit(f'aucun article dans la catégorie {c["slug"]} : il en faut au moins un')
    feat = get(c["feat"]) if isinstance(c.get("feat"), str) else mine[0]
    side_src = [get(k) for k in c["side"]] if c.get("side") else ([a for a in mine if a is not feat] + others)[:4]
    grid_src = [get(k) for k in c["grid"]] if c.get("grid") else (mine + others)[:6]
    fc = card(feat)
    subnav = "".join(f'''
    <a class="subcard" href="#articles"><img src="{R}assets/img/{subimg(c, s)}" alt="" width="56" height="56" loading="lazy"><span>{s}</span><i>{ARROW}</i></a>''' for s in c["subnav"])
    side = "".join((lambda k: f'''
        <a class="side-item" href="{R}{k["href"]}"><img src="{R}assets/img/{k["img"]}" alt="" width="96" height="80"><div><span class="eyebrow">{k["k"]}</span><h3>{k["t"]}</h3><small>{k["d"]} de lecture</small></div></a>''')(card(a)) for a in side_src)
    grid = "".join((lambda k: f'''
      <a class="post big" href="{R}{k["href"]}"><img src="{R}assets/img/{k["img"]}" alt="" width="800" height="560"><div class="post-body"><span class="eyebrow">{k["k"]}</span><h3>{k["t"]}</h3><p class="excerpt">{k["ex"]}</p><span class="meta">{k["n"]} <i></i> {k["d"]}</span></div></a>''')(card(a)) for a in grid_src)
    rank = "".join(f'''
      <div class="rank-row"><span class="pos{" first" if i == 0 else ""}">0{i+1}</span><img src="{logo_src(R, logo)}" alt="{alt}"><div class="why"><b>{b}</b>{why}</div><div class="score"><b>{sc}</b><small>/10</small><span class="chip{"" if cls == "up" else " " + cls}">{chip}</span></div></div>''' for i, (logo, alt, b, why, sc, cls, chip) in enumerate(c["rank"]))
    faq = "".join(f'''
      <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>''' for i, (q, a) in enumerate(c["faq"]))
    url = f'{C.SITE}/{c["slug"]}/'
    ld = jsonld(
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": strip(c["title"]), "description": strip(c["desc"]),
         "url": url, "inLanguage": "fr-FR", "isPartOf": {"@type": "WebSite", "name": C.NOM, "url": C.SITE + "/"},
         "hasPart": [{"@type": "Article", "headline": strip(a["title"]), "url": f'{C.SITE}/{a["cat"]}/{a["slug"]}/'} for a in mine]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in c["faq"]]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": strip(c["rank_h2"]), "itemListOrder": "https://schema.org/ItemListOrderDescending",
         "numberOfItems": len(c["rank"]),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": strip(r[1]), "description": f'Note {r[4]}/10. {strip(r[2])}. {strip(r[3])}'} for i, r in enumerate(c["rank"])]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": C.SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": strip(c["nom"]), "item": url}]})
    return f'''<!doctype html>
<html lang="{C.LANG}">
<head>
{head(R, c["title"], c["desc"], url, ld, og_image=f'{C.SITE}/assets/img/{c["hero"]}')}</head>
<body>

{header(R, c["slug"])}

<section class="hero cat-hero">
  <img class="hero-bg" src="{R}assets/img/{c["hero"]}" alt="{c["hero_alt"]}" width="2000" height="900" fetchpriority="high">
  <div class="wrap hero-inner">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="{R}">Accueil</a><i></i><span>{c["nom"]}</span></nav>
    <h1>{c["h1"]}</h1>
    <p>{c["intro"]}</p>
  </div>
</section>

<nav class="subnav" aria-label="Sous-catégories">
  <div class="wrap subcards">{subnav}
  </div>
</nav>

<section class="cat-featured" id="articles">
  <div class="wrap">
    <div class="section-head">
      <h2>{c["une_h2"]}</h2>
      <a class="btn btn-ghost" href="#classement">Voir le classement</a>
    </div>
    <div class="feat-grid">
      <a class="feat-main" href="{R}{fc["href"]}">
        <img src="{R}assets/img/{feat["img"]}" alt="{feat["img_alt"]}" width="800" height="560">
        <div class="feat-body">
          <span class="tag">{fc["k"]}</span>
          <h2>{feat["title"]}</h2>
          <p>{fc["ex"]}</p>
          <span class="feat-meta">{fc["n"]} · {fc["d"]} de lecture · Mis à jour le {feat["date_fr"]}</span>
        </div>
      </a>
      <div class="feat-side">{side}
      </div>
    </div>
  </div>
</section>

<section class="cat-grid">
  <div class="wrap">
    <div class="section-head">
      <h2>{c["grid_h2"]}</h2>
      <span style="font-size:13px;color:var(--muted)">Du plus récent au plus ancien</span>
    </div>
    <div class="grid3">{grid}
    </div>
  </div>
</section>

<section class="cat-rank" id="classement">
  <div class="wrap rank-grid">
    <div class="rank-intro">
      <h2>{c["rank_h2"]}</h2>
      <p>{c["rank_p"]}</p>
      <a class="btn btn-dark" href="{R}#methode">Voir la méthode de notation</a>
    </div>
    <div class="rank-list">{rank}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <div class="cta-card">
      <div><h2>{c["cta_h2"]}</h2><p>{c["cta_p"]}</p></div>
      <a class="btn btn-dark" href="{R}#outil">{C.CTA}</a>
    </div>
  </div>
</section>

<section class="faq">
  <div class="wrap faq-head">
    <h2>{c["faq_h2"]}</h2>
    <div>{faq}
    </div>
  </div>
</section>

{newsletter(c["news_h2"])}

{footer(R)}
</body>
</html>
'''

if __name__ == "__main__":
    for c in CATS:
        write(os.path.join(c["slug"], "index.html"), linkify(render(c), "../"))
