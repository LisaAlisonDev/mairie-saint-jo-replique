#!/usr/bin/env python3
"""Génère les feuilles de style et scripts factices (même nombre de requêtes que le site observé).

CALIBRAGE : les poids (Ko) ci-dessous sont des HYPOTHÈSES. Mesure chaque fichier du site réel dans DevTools
(onglet Réseau, colonne Taille) puis remplace les valeurs et relance.
"""
import os, base64
RATIO = 0.75  # HYPOTHÈSE : taux de compression gzip du contenu aléatoire base64 (à vérifier au transfert)
BASE = os.path.dirname(os.path.abspath(__file__))
CSS_KB = {"slider":1.6,"theme":1.7,"960":2.0,"480":3.2,"ui":8.8,"toolbar":2.4,"toolbar-icons":1.8,"gallery":2.3,"agenda":1.1,
          "upload":0.9,"typo":1.3,"tools":1.3,"consent":5.9}  # HAR : poids TRANSFÉRÉS (Ko)
JS_KB = {"form":13.4,"autosave":1.3,"placeholder-label":1.2,"ajax-callback":11.5,"js-cookie":2.0,"markitup":9.0,"previsu":2.3,
         "toolbar-start":4.4,"colorbox":9.8,"gallery":1.9,"scrollto":3.0,"localscroll":2.2,"tools-header":4.8,"consent":59.8,
         "ui-copy":171,"slider":11.8,"slider-fx":2.1}  # HAR : poids TRANSFÉRÉS (Ko) ; ui-copy inclut l'écart jQuery SPIP/cdnjs
def stub(path, kb, kind):
    head = f"/* {kind} factice : poids cible {kb} Ko (hypothèse à calibrer) */\n"
    line = "/* remplissage pour reproduire le poids de transfert observé */\n"
    # contenu aléatoire (base64) : peu compressible, donc poids transféré ~ poids de fichier x 0,75 avec gzip
    size = int(kb*1024/RATIO)
    body = head
    while len(body) < size:
        body += "/*" + base64.b64encode(os.urandom(45)).decode() + "*/\n"
    open(path, "w", encoding="utf-8").write(body[:size])
for n, kb in CSS_KB.items():
    stub(os.path.join(BASE, "css", f"{n}.css"), kb, "CSS")
for n, kb in JS_KB.items():
    stub(os.path.join(BASE, "js", f"{n}.js"), kb, "JS")
print(len(CSS_KB), "CSS et", len(JS_KB), "JS générés")
