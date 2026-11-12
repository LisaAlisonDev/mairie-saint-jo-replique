# Réplique « AVANT » d'un site de mairie (banc d'essai ACV)

Site de test sans lien officiel avec une commune réelle. Contenus, logos et images sont des substituts.

## Utilisation
1. `python3 generate_images.py` (déjà exécuté une fois) : régénère les images ; modifie les poids cibles dans le script après avoir mesuré le site réel avec DevTools.
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
- Le site réel compte environ 18 feuilles de style et 22 scripts ; la réplique en compte moins (voir le décompte dans la conversation).
- Pas de CMS, pas de serveur applicatif : la réplique est statique.
- Pas de bandeau de consentement ni de scripts de mesure d'audience / réseaux sociaux.
- Poids des images = hypothèses à calibrer.
