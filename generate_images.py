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
    "une-1.jpg":   (1131, 381, 500),    # HYPOTHÈSE : à calibrer
    "une-2.jpg":   (1131, 381, 500),    # HYPOTHÈSE : à calibrer
    "une-3.jpg":   (4709, 1585, 3000),  # HYPOTHÈSE : à calibrer
    "bref-1.jpg":  (192, 136, 25), "bref-2.jpg": (192, 136, 25), "bref-3.jpg": (192, 136, 25),
    "bref-4.jpg":  (192, 136, 25), "bref-5.jpg": (192, 136, 25),
    "video-1.jpg": (480, 360, 30), "video-2.jpg": (480, 360, 30), "video-3.jpg": (480, 360, 30),
    "video-4.jpg": (480, 360, 30), "video-5.jpg": (480, 360, 30), "video-6.jpg": (480, 360, 30),
    "mag.jpg":     (331, 441, 60),
}
ICONS = {  # nom: (largeur, hauteur)
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
