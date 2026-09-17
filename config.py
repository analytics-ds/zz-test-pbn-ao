# -*- coding: utf-8 -*-
"""Identité du média et textes transverses. UN SEUL endroit à remplir pour tout ce qui
n'est pas du contenu éditorial (nom, baseline, CTA, méthode, critères du comparateur).

Rempli par Claude à l'étape 4 de la skill pbn-ao-geo. Tout ce qui est marqué OBLIGATOIRE
doit être adapté au secteur : la QA (check_site.py) refuse les valeurs d'exemple.
"""

# ------------------------------------------------------------------ identité
NOM = "Comparabio"                       # OBLIGATOIRE nom du média, tel qu'affiché
SLUG = "zz-test-pbn-ao"                      # OBLIGATOIRE nom du dossier et du repo GitHub (ascii, minuscules, tirets)
OWNER = "analytics-ds"                    # compte GitHub qui héberge le repo (rempli par scripts/prereqs.sh)
SITE = f"https://{OWNER}.github.io/{SLUG}"  # racine publique, sans slash final (canonical, JSON-LD, sitemap)
LANG = "fr"
ACCENT = "#2E8B57"                        # couleur d'accent, réécrite par scripts/recolor.py (theme-color)
CSS_V = "7"                               # cache-buster des assets

# ------------------------------------------------------------------ vocabulaire
UNIT = "enseignes"                          # OBLIGATOIRE ce que l'on compare : marques, contrats, opérateurs, box, écoles...
UNIT_ONE = "enseigne"                       # singulier
CTA = "Comparer 2 enseignes"                # OBLIGATOIRE bouton du header et des encarts
CTA_LONG = "Comparer deux enseignes"        # lien texte du hero
BASELINE = "Le comparateur des enseignes bio. Prix relevés en rayon, gammes comptées, avis lus."  # OBLIGATOIRE pied de page
TAGLINE_FOOTER = "Le média des courses bio."  # OBLIGATOIRE après « © 2026 NOM. »
AUTHOR = "La rédaction Comparabio"       # signature des articles
AUTHOR_INITIAL = "C"

# Liste « Marques » du pied de page : (libellé, href). Mettre le client en premier.
FOOTER_BRANDS = [("Biocoop", "magasins/"), ("Naturalia", "magasins/"), ("La Vie Claire", "magasins/"), ("Greenweez", "en-ligne/")]

# ------------------------------------------------------------------ textes transverses
NEWSLETTER_P = "Un email par semaine avec le classement du mois, les nouveaux comparatifs et les baisses de prix relevées en rayon."
NEWSLETTER_NOTE = "Pas de publicité, désinscription en un clic."
ASIDE_NEWS_P = "Le classement du mois et les nouveaux comparatifs, un email par semaine."

# Encart « Notre méthode » en bas de chaque article. OBLIGATOIRE : 5 puces propres au secteur.
METHOD_INTRO = "Ce comparatif repose sur des données publiques, vérifiables une par une."
METHOD_ITEMS = [
 "Les prix sont relevés en rayon et sur les sites des enseignes, hors promotion, sur un panier identique",
 "La largeur de gamme est comptée sur les rayons frais, vrac et épicerie à partir des catalogues en ligne",
 "Les avis clients proviennent de Google Maps et de Trustpilot, sur les douze derniers mois",
 "Les engagements (vrac, local, commerce équitable) sont ceux publiés par chaque enseigne",
 "Les relevés sont datés et refaits chaque trimestre",
]

# Critères du comparateur 2 entités de l'accueil : 5 critères, le dernier est la note globale.
CRITERIA = [
 ("Prix", "panier de 20 produits bio courants"),
 ("Gamme", "références frais, vrac, épicerie"),
 ("Proximité", "nombre de magasins et livraison"),
 ("Avis", "note Google et Trustpilot"),
 ("Note globale", "moyenne pondérée"),
]

# Liens internes supplémentaires pour linkify : (fragment de titre présent dans le libellé du lien, chemin).
# Les titres complets des articles publiés sont branchés automatiquement.
EXTRA_LINKS = []

# Google Fonts : réécrit par scripts/recolor.py --display/--text
FONTS_HREF = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap"
