# Japon en hiver, 26 décembre 2026 au 11 janvier 2027

Guide de voyage personnel pour le programme sur-mesure Allibert Trekking (version 2 du 2 novembre 2026).

- `index.html` : le guide mobile, un seul fichier autonome (hors ligne) : journées heure par heure, adresses (restaurants, cafés, bains, photo, papeterie, course à pied), checklist, infos pratiques, cartes. S'ouvre dans Safari ; « Sur l'écran d'accueil » pour l'avoir comme une app.
- `pdf/Japon_hiver_carnet_v7.pdf` : le carnet complet en PDF (version 7.0, itinéraire organisé par nous-mêmes, pour mémoire).
- `sw.js` et `pwa/` : le service worker et les icônes (installation sur l'écran d'accueil, cache hors ligne sur GitHub Pages).
- `src/` : les sources Python qui génèrent le carnet et le guide (contenu dans `content_*.py`, adresses dans `content_guide.py`).
- `assets/` : photos (Wikimedia Commons, crédits dans le carnet), cartes, polices, tuiles de relief GSI.

## Regénérer

```
cd src
python3 maps.py      # cartes
python3 build.py && python3 render.py   # carnet PDF (Playwright + Chromium)
python3 mobile.py    # guide mobile (MODE = 'allibert' dans mobile.py)
cp ../Japon_hiver_guide_allibert.html ../index.html
```

Dépendances : Python 3, Pillow, Jinja2, matplotlib, numpy, Playwright.
