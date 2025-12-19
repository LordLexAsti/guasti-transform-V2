# docs/EXPERIMENTS_ON_GITHUB.md
## Lancer une expérience depuis GitHub Actions (sans rien installer)

1) Onglet **Actions** → workflow **experiments**
2) Cliquer **Run workflow**
3) Entrer :
- `P` : 30 / 210 / 2310
- `A` et `B` : fenêtre [A,B)
- `seed` : seed fixée

4) À la fin, télécharger l’artefact :
- `guasti-results-...`
qui contient `report.md` + sorties.

### Notes
- C’est volontairement “workflow_dispatch” : tu déclenches à la main → zéro surprise.
- Les artefacts servent de preuves : mêmes inputs → mêmes outputs.

---
