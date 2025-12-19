# RESULTS_TEMPLATE.md
## Résultats — Expériences Guasti (mod 6 / mod P)
### Gabarit de rendu reproductible

> Remplir ce fichier après chaque run expérimental.  
> Objectif : rendre les résultats lisibles en 3 minutes, auditables en 30.

---

## 0) Contexte du run
- **Date** : YYYY-MM-DD  
- **Commit** : `<git sha>`  
- **Machine / OS** :  
- **Python** :  
- **Seed** :  
- **P (primorial)** :  
- **Taille fenêtre W** :  
- **Nombre de fenêtres** :  
- **Stride (espacement)** :  
- **Méthode labels (primalité)** : (crible segmenté / MR 64-bit / autre)  
- **Baselines** : baseline-6 / baseline-wheel / random

---

## 1) Sanity checks (invariants)
### 1.1 Wheel / respiration
- `phi(P)` attendu :  
- `len(R(P))` obtenu :  
- `sum(gaps)` attendu (=P) :  
- `sum(gaps)` obtenu :  
- **Statut** : ✅ PASS / ❌ FAIL

### 1.2 Polarité / carrés
- Test `m^2 mod 6 == 1` (échantillon) : ✅ PASS / ❌ FAIL  
- Observations :

---

## 2) Définition du score (version du modèle)
### 2.1 Features utilisées
- [ ] polarité mod 6  
- [ ] résidu mod P  
- [ ] index résidu (dans R(P))  
- [ ] gap_prev / gap_next  
- [ ] “impacts” (rayons p≥?)  
- [ ] autres :

### 2.2 Formule du score (copier-coller)
```text
S(n) =
