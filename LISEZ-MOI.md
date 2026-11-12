# Réplique « AVANT » d'un site de mairie (banc d'essai ACV)

Site de test sans lien officiel avec une commune réelle. Contenus, logos et images sont des substituts.

## Utilisation
1. `python3 generate_images.py` et `python3 generate_stubs.py` : régénèrent les images et les fichiers CSS/JS factices ; remplace les poids cibles par ceux mesurés dans DevTools sur le site réel.
2. Héberge le dossier tel quel (ex. Cloudflare Workers ou surge.sh) ou ouvre `index.html` en local.
3. Mesure : DevTools (Réseau, cache désactivé), EcoIndex, PageSpeed Insights.

## Défauts reproduits volontairement (version AVANT)
- Cache navigateur désactivé par balises meta
- Pas de meta viewport
- Police web tierce (Google Fonts) et jQuery / jQuery Migrate / jQuery UI / jQuery Cookie chargés en entier depuis cdnjs
- Feuilles de style multiples non regroupées
- Aucune image en chargement différé, images sans srcset, formats JPEG, image du slider très grande (4709 x 1585)
- Miniatures vidéo 480x360 affichées à 151 px de large

## Ce qui diffère du site réel (à citer dans les limites du rapport)
- Le site réel compte environ 18 feuilles de style et 22 scripts ; la réplique reproduit ces nombres avec des fichiers factices (poids = hypothèses, voir generate_stubs.py).
- Pas de CMS, pas de serveur applicatif : la réplique est statique.
- Pas de bandeau de consentement ni de scripts de mesure d'audience / réseaux sociaux.
- Les 17 pictogrammes (flèches, play/pause, puces, RSS, PDF, logos TV, sprites jQuery UI) sont regroupés dans un bandeau `.pictos` pour reproduire le nombre de requêtes images relevé (38) ; sur le vrai site ils sont répartis dans le slider, le menu et le pied de page.

## Calibrage sur le HAR du site réel (mesure du 12/11/2026, cache désactivé)
- Poids des images, CSS et JS calés sur les poids TRANSFÉRÉS du HAR (images 4 145 Ko / 36 requêtes ; CSS 45 Ko / 19 ; JS 414 Ko / 24 ; HTML 14 Ko ; police 15 Ko).
- Images : slider 3 047 Ko et 311 Ko, brefs 293/63/36/33/32 Ko, miniatures YouTube 10 à 16 Ko, mag 156 Ko.
- Hypothèses restantes : dimensions naturelles des images « en bref » (non relevées), taux de compression gzip du contenu factice (0,75), CSS/JS factices = contenu aléatoire, donc DOM/exécution JS non représentatifs.
- Le site réel charge jQuery SPIP (78 Ko) ; la réplique charge jQuery depuis cdnjs et compense l'écart dans `ui-copy.js`.
- Le logo « SaintJo TV filigrane » renvoie un 404 sur le site réel (non reproduit).
- Les temps de chargement dépendent de l'hébergeur : ne compare que des mesures faites avec les mêmes outils et conditions.

## Complexité du DOM
- Mesure EcoIndex du vrai site : 845 éléments ; première version de la réplique : 331.
- Écart comblé en développant les sous-menus du menu haut et du plan du site en pied de page (liens de substitution « Page n.m ») : le compteur DOM de la réplique est maintenant de 845 éléments (compté avec `document.getElementsByTagName('*')`, identique à la valeur 331 mesurée par EcoIndex avant l'ajout).
- Limite : la structure réelle des 845 éléments (répartition, profondeur) n'est pas connue ; seul le total est reproduit. Le HTML de la réplique est plus lourd qu'avant l'ajout.
