# {NOM}

Média comparateur {SECTEUR}, construit sur le modèle du média Comparamode (analytics-ds/comparamode).
Site statique, sans dépendance ni build côté serveur : les pages HTML sont générées par des scripts Python
et servies telles quelles par GitHub Pages.

## Structure

| Chemin | Rôle |
|---|---|
| `config.py` | Identité du média : nom, slug, CTA, baseline, méthode, critères du comparateur |
| `home.py` | Données de l'accueil (hero, bandeau, à la une, comparateur, classement, méthode) |
| `categories.py` | Les pages catégorie (`CATS`) et les icônes de sous-navigation (`SUBIMG`) |
| `articles/*.py` | Un fichier par article comparatif (`ARTICLE = dict(...)`) |
| `pages.py` | Pages fixes (à propos, mentions légales) |
| `photos.json`, `brands.json` | Ce qu'il faut télécharger : photos (avec requête source) et logos des entités comparées |
| `sources_photos.json`, `sources_logos.json` | Origine de chaque visuel (crédit, URL) |
| `assets/css/site.css`, `assets/js/site.js` | Feuille de style et scripts hérités de Comparamode, recolorés |
| `build_*.py`, `common.py`, `contenus.py`, `linkify.py` | Générateurs. `build_all.py` régénère tout |

## Régénérer

```bash
python3 build_all.py          # accueil, catégories, articles, pages fixes, sitemap, robots, llms.txt
python3 -m http.server 8778   # aperçu local
```

Les liens internes vers les articles se branchent automatiquement (`linkify.py`) : un lien vers un article
non publié reste en `#` et la QA le signale.

## Avant une mise en ligne sur un vrai domaine

- Les notes, prix et volumes sont des ordres de grandeur de marché à remplacer par des relevés datés.
- Vérifier les droits des visuels (`sources_photos.json`) et des logos (`sources_logos.json`).
- Renseigner un éditeur réel dans `pages.py` (mentions légales) et l'adresse de contact.
- Mettre `SITE` sur le domaine définitif dans `config.py`, régénérer, ajouter un `CNAME`.
