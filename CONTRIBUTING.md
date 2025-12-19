# CONTRIBUTING.md
## Contribuer au projet Guasti

Merci de contribuer ! Ce dépôt vise un double objectif :
1) **pédagogie** (grille, signatures, visualisation),
2) **expérimentation** (protocoles falsifiables, baselines, scores reproductibles).

L’esprit général : *pas de magie, pas de cherry-picking, pas de “ça marche parce que je le sens”.*

---

## 1) Types de contributions acceptées
### Documentation
- Clarification des définitions (grille, polarité, respiration)
- Exemples didactiques (mod 30, mod 210, mod 2310)
- Améliorations du README / schémas ASCII

### Code
- Génération wheel / respiration
- Expériences multi-fenêtres + reporting
- Visualisations (plots simples) + export

### Expérimentation
- Nouvelles baselines
- Tests de robustesse (fenêtres disjointes)
- Contrôles négatifs (sans résidu, random, permutation)

---

## 2) Règles de rigueur (relecture hostile)
### 2.1 Reproductibilité
Toute PR qui prétend “améliorer” doit inclure :
- une commande de run (ou script)
- la seed
- une sortie résumée dans `results/` (ou un extrait dans la PR)
- comparaison à **baseline-wheel**

### 2.2 Anti-leakage (interdit)
Est considéré comme “triche” (même involontaire) :
- utiliser `is_prime` ou des labels dans le score
- utiliser une factorisation complète comme feature principale
- réinjecter le crible sous un autre nom

### 2.3 Contrôle négatif obligatoire
Toute nouvelle feature mod \(P\) (résidus/gaps) doit être accompagnée d’un run :
- **avec** résidu
- **sans** résidu  
et montrer la chute attendue.

---

## 3) Organisation des fichiers
### 3.1 Documentation
- `GUASTI_CHAPTER.md` : narratif
- `GUASTI_PAPER.md` : sec / soumission
- `EXPERIMENTS.md` : protocole

### 3.2 Résultats
- `results/<exp_id>/report.md`
- `results/<exp_id>/metrics.json` (recommandé)
- `results/<exp_id>/config.json` (recommandé)

---

## 4) Style et conventions
### 4.1 Code
- noms explicites (pas de variables “x1/x2” sans raison)
- fonctions pures quand possible (entrées → sorties)
- éviter les dépendances lourdes sauf nécessité

### 4.2 Docs
- phrases courtes, définitions en tête
- séparer : *définition* / *intuition* / *test*

---

## 5) Checklist PR (copier-coller)
- [ ] J’ai indiqué le but (docs / code / expérimentation)
- [ ] J’ai fourni une commande de run
- [ ] J’ai fixé la seed
- [ ] J’ai comparé à baseline-wheel
- [ ] J’ai ajouté un contrôle négatif “sans résidu” si nécessaire
- [ ] J’ai ajouté/actualisé `CHANGELOG.md`

---

## 6) Signalement de bugs / demandes
Ouvrir une issue avec :
- contexte (P, fenêtre, seed)
- commande exacte
- logs/traceback
- fichier de config si dispo

---
