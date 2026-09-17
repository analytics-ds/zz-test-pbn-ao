# -*- coding: utf-8 -*-
"""Génère sitemap.xml, robots.txt (robots IA explicitement autorisés) et llms.txt depuis les pages présentes."""
import os, datetime
import config as C
from common import strip
from categories import CATS
from contenus import ARTICLES

today = datetime.date.today().isoformat()
urls = [("", "1.0")]
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "assets", "__pycache__", ".playwright-cli", "articles", "node_modules", "_work")]
    if root == "." or "index.html" not in files:
        continue
    path = os.path.relpath(root, ".").replace(os.sep, "/") + "/"
    urls.append((path, "0.8" if path.count("/") == 1 else "0.7"))

body = "".join(f'  <url><loc>{C.SITE}/{p}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>\n' for p, prio in sorted(urls))
open("sitemap.xml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")

bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai",
        "PerplexityBot", "Perplexity-User", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended",
        "CCBot", "Amazonbot", "meta-externalagent", "Bytespider", "DuckAssistBot", "YouBot", "MistralAI-User"]
robots = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE}/sitemap.xml\n"
open("robots.txt", "w", encoding="utf-8").write(robots)

lines = [f"# {C.NOM}", "", f"> {strip(C.BASELINE)}", "", f"Site : {C.SITE}/", "", "## Rubriques", ""]
for c in CATS:
    lines.append(f"- [{strip(c['nom'])}]({C.SITE}/{c['slug']}/) : {strip(c['desc'])}")
lines += ["", "## Comparatifs", ""]
for a in ARTICLES:
    lines.append(f"- [{strip(a['title'])}]({C.SITE}/{a['cat']}/{a['slug']}/) : {strip(a['desc'])}")
lines += ["", "## Méthode", ""] + [f"- {strip(m)}" for m in C.METHOD_ITEMS] + [""]
open("llms.txt", "w", encoding="utf-8").write("\n".join(lines))
print(f"ok sitemap.xml ({len(urls)} URL), robots.txt, llms.txt")
