# -*- coding: utf-8 -*-
"""Génère index.html depuis home.py (HOME) + les articles publiés.
Usage : python3 build_home.py (depuis la racine du site)."""
import json
import config as C
from common import head, header, footer, newsletter, logo_src, strip, jsonld, org, write, ARROW, cat
from contenus import ARTICLES, get, card
from home import HOME
from linkify import linkify

def side_item(a):
    c = card(a)
    return (f'\n        <a class="side-item" href="{c["href"]}">\n          <img src="assets/img/{c["img"]}" alt="" width="96" height="80">\n'
            f'          <div><span class="eyebrow">{c["k"]}</span><h3>{c["t"]}</h3><small>{c["d"]} de lecture</small></div>\n        </a>')

def post(a):
    c = card(a)
    return (f'\n      <a class="post" href="{c["href"]}"><img src="assets/img/{c["img"]}" alt="" width="800" height="560">'
            f'<div class="post-body"><span class="eyebrow">{c["k"]}</span><h3>{c["t"]}</h3><span class="meta">{c["n"]} <i></i> {c["d"]}</span></div></a>')

def render(H):
    feat = get(H["feat"])
    others = [a for a in ARTICLES if a is not feat]
    side = [get(k) for k in H["side"]] if H.get("side") else others[:4]
    posts = [get(k) for k in H["posts"]] if H.get("posts") else ARTICLES[:4]
    marquee = "".join(f'<img src="{logo_src("", s)}" alt="{n}">' for s, n in H["marquee"])
    tiles = "".join(
        f'\n      <a class="tile" href="{s}/"><img src="assets/img/{img}" alt="{strip(cat(s)["nom"])}" width="760" height="720"><span class="tile-label"><span><strong>{cat(s)["nom"]}</strong><em>{count}</em></span><span class="arrow">{ARROW}</span></span></a>'
        for s, img, count in H["tiles"])
    rank = "".join(
        f'\n      <div class="rank-row"><span class="pos{" first" if i == 0 else ""}">0{i+1}</span><img src="{logo_src("", logo)}" alt="{name}"><div class="why"><b>{b}</b>{why}</div><div class="score"><b>{sc}</b><small>/10</small><span class="chip{"" if cls == "up" else " " + cls}">{chip}</span></div></div>'
        for i, (logo, name, b, why, sc, cls, chip) in enumerate(H["rank"]))
    steps = "".join(f'\n      <div class="step"><span class="n">0{i+1}</span><h3>{h3}</h3><p>{p}</p></div>' for i, (h3, p) in enumerate(H["steps"]))
    scores = json.dumps(H["scores"], ensure_ascii=False)
    crits = json.dumps([list(c) for c in C.CRITERIA], ensure_ascii=False)
    fc = card(feat)
    ld = jsonld(org(), {"@context": "https://schema.org", "@type": "WebSite", "name": C.NOM, "url": C.SITE + "/", "inLanguage": f"{C.LANG}-FR" if C.LANG == "fr" else C.LANG})
    return f'''<!doctype html>
<html lang="{C.LANG}">
<head>
{head("", H["title"], H["desc"], C.SITE + "/", ld, og_image=f'{C.SITE}/assets/img/{H["hero_img"]}')}</head>
<body>

{header("")}

<section class="hero">
  <img class="hero-bg" src="assets/img/{H["hero_img"]}" alt="{H["hero_alt"]}" width="2400" height="1790" fetchpriority="high">
  <div class="wrap hero-inner">
    <h1>{H["h1"]}</h1>
    <p>{H["p"]}</p>
    <div class="btns">
      <a class="btn-pill" href="#comparatifs">Voir les comparatifs <span class="circ">{ARROW}</span></a>
      <a class="btn-link" href="#outil">{C.CTA_LONG}</a>
    </div>
  </div>
</section>

<section class="brands" id="marques">
  <div class="brands-head">{H["marquee_head"]}</div>
  <div class="marquee"><div class="marquee-track" id="logoTrack">{marquee}</div></div>
</section>

<section class="featured" id="comparatifs">
  <div class="wrap">
    <div class="section-head">
      <div><h2>{H["feat_h2"]}</h2></div>
      <a class="btn btn-ghost" href="#derniers">Tous les comparatifs</a>
    </div>
    <div class="feat-grid">
      <a class="feat-main" href="{fc["href"]}">
        <img src="assets/img/{feat["img"]}" alt="{feat["img_alt"]}" width="1300" height="860">
        <div class="feat-body">
          <span class="tag">{fc["k"]}</span>
          <h2>{feat["title"]}</h2>
          <p>{fc["ex"]}</p>
          <span class="feat-meta">{fc["n"]} · {fc["d"]} de lecture · Mis à jour le {feat["date_fr"]}</span>
        </div>
      </a>
      <div class="feat-side">{"".join(side_item(a) for a in side)}
      </div>
    </div>
  </div>
</section>

<section class="tool" id="outil">
  <div class="wrap">
    <div class="tool-card">
      <div class="tool-intro">
        <h2>{H["tool_h2"]}</h2>
        <p>{H["tool_p"]}</p>
        <div class="selects">
          <div class="select"><select id="brandA" aria-label="Première {C.UNIT_ONE}"></select></div>
          <span class="vs">VS</span>
          <div class="select"><select id="brandB" aria-label="Seconde {C.UNIT_ONE}"></select></div>
        </div>
        <p class="tool-note">{H["tool_note"]}</p>
      </div>
      <div class="compare">
        <div class="cmp-head"><span>Critère</span><b id="nameA"></b><b id="nameB"></b></div>
        <div id="rows"></div>
        <div class="verdict"><b id="verdict"></b><span id="verdictSub"></span></div>
      </div>
    </div>
  </div>
</section>

<section class="cats" id="categories">
  <div class="wrap">
    <div class="section-head">
      <div><h2>{H["cats_h2"]}</h2><p>{H["cats_p"]}</p></div>
    </div>
    <div class="grid4">{tiles}
    </div>
  </div>
</section>

<section class="ranking" id="classement">
  <div class="wrap rank-grid">
    <div class="rank-intro">
      <h2>{H["rank_h2"]}</h2>
      <p>{H["rank_p"]}</p>
      <a class="btn btn-dark" href="#methode">Voir la méthode de notation</a>
    </div>
    <div class="rank-list">{rank}
    </div>
  </div>
</section>

<section class="posts" id="derniers">
  <div class="wrap">
    <div class="section-head">
      <div><h2>{H["posts_h2"]}</h2></div>
      <a class="btn btn-ghost" href="{posts[0]["cat"]}/">Voir tous les comparatifs</a>
    </div>
    <div class="grid4">{"".join(post(a) for a in posts)}
    </div>
  </div>
</section>

<section class="method" id="methode">
  <div class="wrap">
    <div class="method-head">
      <h2>{H["method_h2"]}</h2>
      <p>{H["method_p"]}</p>
    </div>
    <div class="steps">{steps}
    </div>
  </div>
</section>

{newsletter(H["news_h2"], H.get("news_p"))}

{footer("")}
<script>
(function(){{
  var brands={scores};
  var crits={crits};
  var A=document.getElementById('brandA'),B=document.getElementById('brandB');
  Object.keys(brands).forEach(function(n){{A.add(new Option(n,n));B.add(new Option(n,n));}});
  A.value={json.dumps(H["default_a"], ensure_ascii=False)};B.value={json.dumps(H["default_b"], ensure_ascii=False)};
  function fmt(v){{return v.toFixed(1).replace('.',',');}}
  function render(){{
    var a=A.value,b=B.value,ra=brands[a],rb=brands[b],wins=0,rows='';
    document.getElementById('nameA').textContent=a;document.getElementById('nameB').textContent=b;
    crits.forEach(function(c,i){{
      var va=ra[i],vb=rb[i],wa=va>vb,wb=vb>va; if(i<4&&wa)wins++;
      rows+='<div class="cmp-row"><div class="crit">'+c[0]+'<small>'+c[1]+'</small></div>'
        +'<div class="bar'+(wa?' win':'')+'" data-brand="'+a+'"><div class="track"><div class="fill" style="width:'+(va*10)+'%"></div></div><span class="val">'+fmt(va)+'</span></div>'
        +'<div class="bar'+(wb?' win':'')+'" data-brand="'+b+'"><div class="track"><div class="fill" style="width:'+(vb*10)+'%"></div></div><span class="val">'+fmt(vb)+'</span></div></div>';
    }});
    document.getElementById('rows').innerHTML=rows;
    var v=document.getElementById('verdict'),s=document.getElementById('verdictSub');
    if(a===b){{v.textContent='Choisissez deux {C.UNIT} différentes';s.textContent='';return;}}
    var lead=ra[4]>rb[4]?a:rb[4]>ra[4]?b:null;
    v.textContent=lead?lead+' l’emporte':'Égalité parfaite';
    s.textContent=lead?(lead===a?wins:4-wins)+' critères sur 4, note globale '+fmt(lead===a?ra[4]:rb[4])+' contre '+fmt(lead===a?rb[4]:ra[4]):'Même note globale sur nos relevés';
  }}
  A.addEventListener('change',render);B.addEventListener('change',render);render();
}})();
</script>
</body>
</html>
'''

if __name__ == "__main__":
    write("index.html", linkify(render(HOME), ""))
