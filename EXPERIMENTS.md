# EXPERIMENTS.md
## Protocole expérimental — Grille/Transformée de Guasti (mod 6, mod 30, mod 2310)
### Objectif : mesurer, comparer, falsifier

> Ce fichier est conçu pour transformer le dépôt en “laboratoire reproductible”.  
> Tout ce qui suit est **quantifié**, **comparatif**, et compatible avec une **relecture hostile**.

---

## 0) Ce que ce protocole teste (et ne teste pas)

### Teste
- La **cohérence interne** (respiration, invariants mod 6 / mod P).
- Une éventuelle **valeur de scoring** au-delà d’une roue (lift > 1).
- La **robustesse** sur fenêtres disjointes (anti cherry-picking).
- La détection d’une **fuite d’information** (contrôle “sans résidu”).

### Ne teste pas
- Une “preuve” de conjectures globales (RH, etc.).
- Une redéfinition de la primalité.
- Une supériorité absolue sur les méthodes optimales de criblage.

---

## 1) Paramètres standard (à figer)

### 1.1 Primorial / roue
- `P = 30` (niveau didactique)
- `P = 210` (niveau intermédiaire)
- `P = 2310` (niveau test robuste)

### 1.2 Fenêtres disjointes
Choisir **au moins 10 fenêtres** de taille identique `W` :
- Exemple : `W = 2_000_000`
- Fenêtres : `[A_i, A_i + W)` avec `A_{i+1} = A_i + 10W` (espacement large)

> Important : l’espacement sert à éviter que des effets “locaux” soient pris pour des lois.

### 1.3 Baselines (cruelles)
- **Baseline-6** : candidats `6k±1` (ordre naturel).
- **Baseline-wheel** : candidats `gcd(n, P)=1` (ordre naturel).
- **Random** : permutation aléatoire des candidats wheel (seed fixée).

---

## 2) Données générées

### 2.1 Résidus wheel et respiration
- `R(P) = { r in [1..P] : gcd(r,P)=1 }`
- `G(P) = gaps cycliques de R(P)` (respiration)

**Invariants attendus** :
- `len(R(P)) == phi(P)`
- `sum(G(P)) == P`
- `len(G(P)) == phi(P)`

### 2.2 Extraction candidats sur fenêtre
- `C(P;A,B) = { n in [A,B) : gcd(n,P)=1 }`

---

## 3) Vérité terrain (prime labels)

### 3.1 Méthode recommandée
- Fenêtres “moyennes” : crible segmenté (exact).
- Fenêtres “grandes” : Miller–Rabin déterministe 64-bit (bases fixes) ou crible segmenté optimisé.

### 3.2 Sorties attendues
Pour chaque fenêtre :
- `candidates.csv` : liste des n candidats
- `labels.csv` : `is_prime` (bool) + optionnel `small_factor` (int)

---

## 4) Scoring Guasti (interfaces)

### 4.1 Design principe
Le scoring doit être défini comme une fonction :
- `score(n) -> float` (plus grand = plus “prime-like”)

et une annotation :
- `features(n) -> dict` (diagnostic)

### 4.2 Features minimales (version v0)
- `polarity6`: G/D
- `is_pillar6`: bool (devrait être faux pour les candidats)
- `residueP`: `n % P`
- `residue_index`: index de `residueP` dans `R(P)`
- `gap_prev`, `gap_next`: gaps voisins dans la respiration
- `distance_to_pillar`: ici 1 par construction (±1), mais utile si variante

### 4.3 Features optionnelles (versions v1+)
- “impacts attendus” : marquage si `n` tombe sur un produit `a*b` avec `a,b` dans un set restreint (à définir)
- seuils `p^2` : annotation “nouveaux événements” à partir du carré d’un nouveau rayon

> Note : toute feature qui simule une factorisation complète revient à “tricher” (elle fait le job par définition).  
> On veut tester un *score léger*, pas un oracle.

---

## 5) Mesures de performance

### 5.1 Mesures standard
Pour un ensemble X :
- **densité** : `prime_density(X) = primes(X) / len(X)`
- **Precision@k** : primes dans les `k` meilleurs `score`

### 5.2 Lift vs baselines
Pour une fenêtre fixée :
- `top1 = top 1%` des candidats (par score)
- `top5 = top 5%`

\[
lift(top) = \frac{density(top)}{density(baseline\_wheel\_same\_size)}
\]

### 5.3 Résultats requis
Pour chaque fenêtre :
- lift(top1), lift(top5)
- precision@k (k = 100, 1_000, 10_000 selon taille fenêtre)
- variance inter-fenêtres (écart-type)

---

## 6) Tests falsifiables (checklist)

### Test F1 — Respiration correcte
- `sum(gaps)==P`
- `len(gaps)==phi(P)`

**FAIL** : incohérence / bug.

### Test F2 — Carrés à Gauche impossibles (mod 6)
Vérifier sur un range :
- pour `m` copremier à 6, `m*m % 6 == 1`
- donc jamais `==5`

**FAIL** : bug.

### Test F3 — “Événements nouveaux” à partir de `p^2`
Si une feature “rayon p” est utilisée, elle ne doit pas attribuer de “nouveau régime” avant `p^2` sans justification factorielle stricte.

**FAIL** : définition incohérente / narratif.

### Test F4 — Lift > 1 stable
Seuils minimum (à discuter, mais **>1** obligatoire) :
- lift(top1) > 1.05
- lift(top5) > 1.02

**FAIL** : pas de pouvoir prédictif au-delà de la roue.

### Test F5 — Robustesse
Les lifts doivent rester >1 sur fenêtres disjointes.

**FAIL** : surapprentissage local / apophénie.

---

## 7) Contrôle négatif : variante “sans résidu”

### 7.1 But
Détecter une fuite d’info mod P.

### 7.2 Protocole
Recalculer score en supprimant :
- `residueP`, `residue_index`, `gap_prev`, `gap_next`

Garder seulement :
- polarité mod 6
- (éventuelles features non-wheel)

**Attendu** : retour vers baseline-6 / baseline-wheel.

**FAIL** : fuite d’info (ou reconstruction implicite du wheel).

---

## 8) Format des rapports (à produire)

### 8.1 Tableau par fenêtre
| window_id | A | B | P | #candidates | baseline_density | top1_density | top1_lift | top5_lift |
|---|---:|---:|---:|---:|---:|---:|---:|---:|

### 8.2 Résumé global
- moyenne et écart-type des lifts
- histogramme des lifts par fenêtre
- courbe `precision@k` (k croissant)

---

## 9) Commandes (placeholder)
> À adapter selon l’arborescence du repo.

Exemples :
```bash
# Générer respiration
python -m guasti.wheel --P 2310 --out data/wheel_2310.json

# Lancer expérimentation sur N fenêtres
python -m guasti.experiment \
  --P 2310 \
  --window 2000000 \
  --n_windows 10 \
  --stride 20000000 \
  --seed 42 \
  --out results/exp_P2310

# Rapport
python -m guasti.report --in results/exp_P2310 --out results/exp_P2310/report.md
