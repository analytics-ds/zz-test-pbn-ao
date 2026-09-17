# -*- coding: utf-8 -*-
"""Régénère tout le site : accueil, catégories, articles, pages fixes, sitemap/robots/llms."""
import subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for s in ("build_home.py", "build_categories.py", "build_articles.py", "build_pages.py", "build_sitemap.py"):
    subprocess.run([sys.executable, s], check=True)
