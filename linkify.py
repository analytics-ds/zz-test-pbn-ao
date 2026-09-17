# -*- coding: utf-8 -*-
"""Remplacement automatique des href="#" par l'URL de l'article dont le titre figure dans le lien.

Un lien reste en "#" tant que l'article correspondant n'existe pas : jamais de lien mort.
La table est construite depuis les articles publiés (contenus.ARTICLES) + config.EXTRA_LINKS.
"""
import re
from config import EXTRA_LINKS

_A = re.compile(r'<a([^>]*?)href="#"([^>]*?)>(.*?)</a>', re.S)

def _strip(t):
    return t.replace("&amp;", "&").replace("<b>", "").replace("</b>", "")

def links():
    from contenus import ARTICLES
    out = []
    for a in ARTICLES:
        path = f'{a["cat"]}/{a["slug"]}/'
        out.append((a["title"], path))
        if a.get("h1") and a["h1"] != a["title"]:
            out.append((a["h1"], path))
    out += list(EXTRA_LINKS)
    return out

def linkify(html, prefix=""):
    table = links()
    def sub(m):
        before, after, inner = m.group(1), m.group(2), m.group(3)
        plain = _strip(inner)
        for frag, url in table:
            if frag in inner or _strip(frag) in plain:
                return f'<a{before}href="{prefix}{url}"{after}>{inner}</a>'
        return m.group(0)
    return _A.sub(sub, html)
