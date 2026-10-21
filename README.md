# GE Metric — site web

Refonte du site de GE Metric, géomètre-expert à Nice (Côte d'Azur & Monaco). Optimisé SEO / GEO, 14 pages statiques.

## Structure

- `dist/` — le site prêt à déployer (HTML statique, `sitemap.xml`, `robots.txt`, `llms.txt`).
- `build/` — le générateur : `content.py` (infos du cabinet, reprises du site d'origine), `services_short.py` (contenu des 9 landing pages), `mentions.html` (mentions légales et CGV), `build.py` (gabarits).
- `assets/` — styles, script, logo et photos (sources copiées dans `dist/assets/` à la génération).

## Regénérer le site

```bash
python3 build/build.py dist artifact
mkdir -p dist/assets && cp assets/* dist/assets/
```

## Avant la mise en ligne

- Redirections 301 : `/contactez-nous/` → `/contact.html`, `/mentions-legales/` → `/mentions-legales.html`.
- Vérifier que le format d'URL de l'hébergement correspond aux canoniques (`.html`) ; sinon adapter `url()` dans `build/build.py` et regénérer.
- Brancher le formulaire de contact sur un vrai envoi (actuellement : préparation d'un e-mail).
- À valider avec le cabinet : « 14 ans de métier », « mesurées au centimètre », intervention à Monaco.
