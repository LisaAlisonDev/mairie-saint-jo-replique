#!/usr/bin/env python3
"""Génère les images de substitution (bruit JPEG) aux dimensions observées sur le site réel.

CALIBRAGE : les poids cibles ci-dessous sont des HYPOTHÈSES. Remplace-les par les poids
mesurés dans DevTools (onglet Réseau, colonne Taille) sur le site réel, puis relance.
Le bruit aléatoire rend les images peu compressibles : on ajuste la qualité JPEG pour
approcher le poids cible (le script indique le poids obtenu).
"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

# nom: (largeur, hauteur, poids cible en Ko ou None pour une icône)
JPEGS = {
    "une-1.jpg":   (1131, 381, 311),    # HAR : artgrand3988.jpg
    "une-2.jpg":   (4709, 1585, 3047),  # HAR : artgrand3925.jpg (72 % du poids des images)
    
    "bref-1.jpg":  (700, 500, 293), "bref-2.jpg": (320, 226, 63), "bref-3.jpg": (230, 163, 36),  # dimensions naturelles HYPOTHÈSE (non relevées dans le HAR), affichées à 192x136
     # HAR : arton4020/4025/4030
    "bref-4.jpg":  (230, 163, 33), "bref-5.jpg": (230, 163, 32),  # HAR : arton4024/4021
    "video-1.jpg": (480, 360, 16), "video-2.jpg": (480, 360, 16), "video-3.jpg": (480, 360, 15),  # HAR : hqdefault YouTube
    "video-4.jpg": (480, 360, 15), "video-5.jpg": (480, 360, 14), "video-6.jpg": (480, 360, 10),
    "mag.jpg":     (331, 441, 156)  # HAR : arton4023.jpg,
}
ICONS = {  # + pictogrammes ajoutés pour reproduire les 38 requêtes images relevées
    "arrow-left.png": (20, 20), "arrow-right.png": (20, 20), "play.png": (24, 24), "pause.png": (24, 24), "play2.png": (24, 24), "pause3.png": (24, 24), "puce-menu-haut.png": (10, 10), "puce-jaune.png": (10, 10), "puce-blanche.png": (10, 10), "ouvrir-menu.png": (24, 24), "rss.png": (16, 16), "rss-rouge.png": (16, 16), "pdf.png": (42, 42), "logo-tv-filigrane.png": (120, 40), "logo-tv-50.png": (50, 50), "ui-icons-444.png": (256, 240), "ui-icons-fff.png": (256, 240),
     # nom: (largeur, hauteur)
    "logo.png": (104, 120), "fil-info.png": (47, 37), "loupe.png": (24, 24),
    "facebook.png": (32, 32), "twitter.png": (32, 32), "ville-internet.png": (120, 83),
}

def noisy(w, h):
    return Image.frombytes("RGB", (w, h), os.urandom(w * h * 3))

def save_to_target(img, path, target_kb):
    lo, hi, best = 1, 95, 1
    while lo <= hi:
        q = (lo + hi) // 2
        img.save(path, "JPEG", quality=q, optimize=False)
        if os.path.getsize(path) / 1024 <= target_kb:
            best, lo = q, q + 1
        else:
            hi = q - 1
    img.save(path, "JPEG", quality=best)
    return best

for name, (w, h, kb) in JPEGS.items():
    p = os.path.join(OUT, name)
    q = save_to_target(noisy(w, h), p, kb)
    print(f"{name:12s} {w}x{h}  cible {kb} Ko -> {os.path.getsize(p)/1024:.0f} Ko (qualité {q})")

for name, (w, h) in ICONS.items():
    im = Image.new("RGB", (w, h), (192, 57, 43))
    ImageDraw.Draw(im).rectangle([2, 2, w - 3, h - 3], outline=(255, 255, 255))
    im.save(os.path.join(OUT, name))
print("Icônes générées.")

# ville-internet noisy : HAR ville_internet_gauche.png = 39,7 Ko transférés (PNG de bruit pour atteindre ce poids)
im = Image.frombytes("RGB", (116, 120), os.urandom(116*120*3)); im.save(os.path.join(OUT, "ville-internet.png"), optimize=True)
