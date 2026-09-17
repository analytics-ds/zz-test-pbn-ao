# -*- coding: utf-8 -*-
"""Génère les articles (<cat>/<slug>/index.html) depuis articles/*.py.

Structure GEO d'un article : encart « En bref » (réponse directe), sommaire, sections H2
(p, h3, ul, ol, img, quote, table, table2, podium), verdict, FAQ, méthode, articles liés,
JSON-LD Article + FAQPage + ItemList + BreadcrumbList. Usage : python3 build_articles.py"""
import os
import config as C
from common import head, header, footer, logo_src, strip, jsonld, write, cat
from contenus import ARTICLES, get, card
from linkify import linkify

def render_table(t, R):
    h = "".join(f"<th>{x}</th>" for x in t["head"])
    rows = ""
    for r in t["rows"]:
        best = len(r) > len(t["head"]) and r[-1] == 1
        tds = ""
        for i, c in enumerate(r[:len(t["head"])]):
            if i == 0:
                tds += f'<td class="brand">{c}{"<span class=\'badge\'>Notre choix</span>" if best else ""}</td>'
            elif i == 1 and "Note" in t["head"][1]:
                tds += f'<td class="note{" best" if best else ""}">{c}</td>'
            else:
                tds += f"<td>{c}</td>"
        rows += f"<tr>{tds}</tr>"
    note = f'<div class="table-note">{t["note"]}</div>' if t.get("note") else ""
    return f'<div class="table-wrap"><div class="table-scroll"><table><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table></div>{note}</div>'

def render_podium(a, R):
    out = ""
    for i, (logo, name, label, detail, score) in enumerate(a["podium"]):
        out += (f'<div class="pod{" first" if i == 0 else ""}"><span class="rank">0{i+1}</span>'
                f'<img src="{logo_src(R, logo)}" alt="{strip(name)}"><b>{label}</b>'
                f'<span>{detail}</span><span class="sc">{score}<span style="font-size:13px;opacity:.6">/10</span></span></div>')
    return f'<div class="podium">{out}</div>'

def render_body(a, R):
    html = ""
    for s in a["sections"]:
        html += f'<h2 id="{s["id"]}">{s["h2"]}</h2>'
        for kind, val in s["body"]:
            if kind == "p":
                html += f"<p>{val}</p>"
            elif kind == "h3":
                html += f"<h3>{val}</h3>"
            elif kind == "ul":
                html += "<ul>" + "".join(f"<li>{li}</li>" for li in val) + "</ul>"
            elif kind == "ol":
                html += "<ol>" + "".join(f"<li>{li}</li>" for li in val) + "</ol>"
            elif kind == "img":
                html += (f'<figure><img src="{R}assets/img/{val["src"]}" alt="{val["alt"]}" '
                         f'width="1200" height="700" loading="lazy"><figcaption>{val["cap"]}</figcaption></figure>')
            elif kind == "quote":
                html += f"<blockquote><p>{val}</p></blockquote>"
            elif kind == "table":
                html += render_table(a["table"], R)
            elif kind == "table2":
                html += render_table(val, R)
            elif kind == "podium":
                html += render_podium(a, R)
            else:
                raise SystemExit(f'bloc inconnu {kind!r} dans {a["slug"]}')
    return html

def ld(a):
    url = f'{C.SITE}/{a["cat"]}/{a["slug"]}/'
    catnom = strip(cat(a["cat"])["nom"])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": strip(a["title"]), "description": strip(a["desc"]),
           "datePublished": a["date"], "dateModified": a.get("date_mod", a["date"]), "inLanguage": "fr-FR",
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "image": f'{C.SITE}/assets/img/{a["img"]}',
           "author": {"@type": "Organization", "name": C.NOM, "url": C.SITE + "/"},
           "publisher": {"@type": "Organization", "name": C.NOM, "url": C.SITE + "/", "logo": {"@type": "ImageObject", "url": f"{C.SITE}/assets/logo/logo.svg"}},
           "articleSection": catnom, "about": [strip(r[0]) for r in a["table"]["rows"]]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(r)}} for q, r in a["faq"]]}
    items = {"@context": "https://schema.org", "@type": "ItemList", "name": strip(a["title"]),
             "itemListOrder": "https://schema.org/ItemListOrderDescending", "numberOfItems": len(a["table"]["rows"]),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": strip(r[0]),
                                  "description": f'Note {r[1]}/10. {strip(str(r[len(a["table"]["head"]) - 1]))}.'} for i, r in enumerate(a["table"]["rows"])]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": C.SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": catnom, "item": f'{C.SITE}/{a["cat"]}/'},
        {"@type": "ListItem", "position": 3, "name": strip(a["h1"])}]}
    return jsonld(art, faq, items, crumbs)

def render(a):
    R = "../../"
    c = cat(a["cat"])
    toc = "".join(f'<li><a href="#{s["id"]}">{strip(s["h2"])}</a></li>' for s in a["sections"])
    brief = "".join(f"<li>{b}</li>" for b in a["brief"])
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{r}</p></details>' for i, (q, r) in enumerate(a["faq"]))
    verdict = "".join(f"<p>{p}</p>" for p in a["verdict"]["body"])
    rel_src = [get(k) for k in a["related"]] if a.get("related") else [x for x in ARTICLES if x is not a][:3]
    related = "".join((lambda k: f'<a class="post big" href="{R}{k["href"]}"><img src="{R}assets/img/{k["img"]}" alt="" width="800" height="560" loading="lazy">'
                       f'<div class="post-body"><span class="eyebrow">{k["k"]}</span><h3>{k["t"]}</h3></div></a>')(card(x)) for x in rel_src)
    win_logo, win_name, win_label, win_detail, win_score = a["podium"][0]
    method = "".join(f"<li>{m}</li>" for m in C.METHOD_ITEMS)
    url = f'{C.SITE}/{a["cat"]}/{a["slug"]}/'
    return f'''<!doctype html>
<html lang="{C.LANG}">
<head>
{head(R, a["title"], a["desc"], url, ld(a), og_type="article", og_image=f'{C.SITE}/assets/img/{a["img"]}')}</head>
<body>

{header(R, a["cat"], scrolled=True)}

<section class="art-hero">
  <img src="{R}assets/img/{a["img"]}" alt="{a["img_alt"]}" width="1300" height="731" fetchpriority="high">
</section>

<section class="art-head">
  <div class="wrap">
    <div class="art-card">
      <nav class="crumbs" aria-label="Fil d'Ariane"><a href="{R}">Accueil</a><i></i><a href="{R}{a["cat"]}/">{c["nom"]}</a><i></i><span>{strip(a["h1"])}</span></nav>
      <h1>{a["h1"]}</h1>
      <p class="art-lead">{a["lead"]}</p>
      <div class="art-meta">
        <span class="art-author"><span>{C.AUTHOR_INITIAL}</span><b>{C.AUTHOR}</b></span>
        <span>Mis à jour le <b>{a["date_fr"]}</b></span>
        <span><b>{a["reading"]} min</b> de lecture</span>
        <span><b>{a["nb"]} {a.get("nb_unit", C.UNIT)}</b> comparées</span>
      </div>
    </div>
  </div>
</section>

<section class="art-body">
  <div class="wrap art-cols">
    <article class="prose">

      <div class="brief">
        <h2>En bref</h2>
        <p class="answer">{a["brief_answer"]}</p>
        <ul>{brief}</ul>
      </div>

      <details class="toc">
        <summary>Sommaire de ce comparatif</summary>
        <ol>{toc}</ol>
      </details>

      {render_body(a, R)}

      <div class="verdict-box">
        <h2>{a["verdict"]["h2"]}</h2>
        {verdict}
      </div>

      <h2 id="faq">Questions fréquentes</h2>
      <div class="faq" style="padding:0">{faq}</div>

      <div class="method-box">
        <h2>Notre méthode</h2>
        <p>{C.METHOD_INTRO}</p>
        <ul>{method}</ul>
      </div>
    </article>

    <aside class="aside">
      <div class="aside-card">
        <h3>Notre choix</h3>
        <div class="aside-win"><img src="{logo_src(R, win_logo)}" alt="{strip(win_name)}"><b>{win_score}</b></div>
        <p>{win_label}. {win_detail}.</p>
        <a class="btn btn-dark" href="{R}#outil" style="width:100%;justify-content:center">{C.CTA}</a>
      </div>
      <div class="aside-card">
        <h3>Dans ce comparatif</h3>
        <div class="aside-links">{"".join(f'<a href="#{s["id"]}">{strip(s["h2"])}</a>' for s in a["sections"])}<a href="#faq">Questions fréquentes</a></div>
      </div>
      <div class="aside-card dark">
        <h3>Newsletter</h3>
        <p>{C.ASIDE_NEWS_P}</p>
        <a class="btn btn-yellow" href="{R}#newsletter" style="width:100%;justify-content:center">Je m'inscris</a>
      </div>
    </aside>
  </div>
</section>

<section class="related">
  <div class="wrap">
    <div class="section-head"><h2>À lire ensuite</h2><a class="btn btn-ghost" href="{R}{a["cat"]}/">Tous les comparatifs {strip(c["nom"]).lower()}</a></div>
    <div class="grid3">{related}</div>
  </div>
</section>

{footer(R)}
</body>
</html>
'''

if __name__ == "__main__":
    for a in ARTICLES:
        write(os.path.join(a["cat"], a["slug"], "index.html"), linkify(render(a), "../../"))
