# -*- coding: utf-8 -*-
"""Charge tous les articles du dossier articles/ (un fichier par article, variable ARTICLE,
ou une liste ARTICLES) et les expose triés par date décroissante."""
import glob, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load_articles():
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "articles", "*.py"))):
        if os.path.basename(f).startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location("art_" + os.path.basename(f)[:-3], f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "ARTICLE"):
            out.append(mod.ARTICLE)
        if hasattr(mod, "ARTICLES"):
            out.extend(mod.ARTICLES)
    keys = [f'{a["cat"]}/{a["slug"]}' for a in out]
    dup = {k for k in keys if keys.count(k) > 1}
    if dup:
        raise SystemExit(f"articles en double : {sorted(dup)}")
    out.sort(key=lambda a: a.get("date", ""), reverse=True)
    return out

ARTICLES = load_articles()
BY_KEY = {f'{a["cat"]}/{a["slug"]}': a for a in ARTICLES}

def by_cat(cat):
    return [a for a in ARTICLES if a["cat"] == cat]

def get(key):
    """Article par clé 'cat/slug'. Erreur explicite si absent."""
    if key not in BY_KEY:
        raise SystemExit(f"article inconnu : {key} (connus : {sorted(BY_KEY)})")
    return BY_KEY[key]

def card(a):
    """Champs d'une carte d'article : image, étiquette, titre, extrait, compteur, durée."""
    excerpt = a.get("excerpt") or a["lead"].split(". ")[0].rstrip(".") + "."
    return dict(img=a["img"], k=a.get("kicker", "Comparatif"), t=a["title"], ex=excerpt,
                n=f'{a["nb"]} {a.get("nb_unit", "")}'.strip(), d=f'{a["reading"]} min',
                href=f'{a["cat"]}/{a["slug"]}/')
