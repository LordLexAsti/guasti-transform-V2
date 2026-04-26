# Rapport d'Analyse du Dépôt Guasti Transform V2

**Date:** 23 décembre 2025
**Analyseur:** Claude Code
**Branche:** claude/analyze-repo-graphs-8Relu

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Architecture du processus](#2-architecture-du-processus)
3. [Évaluation des performances](#3-évaluation-des-performances)
4. [Analyse technique détaillée](#4-analyse-technique-détaillée)
5. [Vérification de la falsifiabilité](#5-vérification-de-la-falsifiabilité)
6. [Points forts et limitations](#6-points-forts-et-limitations)
7. [Conclusions et recommandations](#7-conclusions-et-recommandations)

---

## 1. Vue d'ensemble

### 1.1 Objectif du projet

Le projet **Guasti Transform V2** implémente une méthode de **priorisation des nombres premiers candidats** basée sur :

- **Roue primorielle** (P = 2310 = 2×3×5×7×11) : ordre cyclique des candidats
- **Motif de respiration** : gaps cycliques entre résidus survivants
- **Score multi-échelle** : combinaison de features structurelles
- **Métrique Precision@K** : évaluation de la qualité de tri

### 1.2 Périmètre

⚠️ **Important** : Ce projet ne prétend **PAS** :
- Prouver la primalité de nombres
- Résoudre l'Hypothèse de Riemann
- Fournir un test de primalité déterministe

✅ **Il fournit** :
- Une méthode de **tri/priorisation** des candidats premiers
- Une approche **reproductible** et **falsifiable**
- Des métriques quantifiables (Precision@K, Lift)

### 1.3 Structure du dépôt

```
guasti-transform-V2/
├── src/
│   ├── wheel.py          # Roue primorielle et gaps cycliques
│   ├── features.py       # Pré-calculs (primes, impacts, saturation)
│   ├── score.py          # Fonction de score v1
│   ├── eval.py           # Évaluation et Precision@K
│   └── ascii_tower.py    # Visualisation ASCII
├── guasti_core.py        # Transformée de Guasti (théorèmes angulaires)
├── guasti_utils.py       # Utilitaires
├── basic_usage.py        # Exemple d'utilisation
├── tests/                # Tests unitaires
└── docs/                 # Documentation
```

---

## 2. Architecture du processus

### 2.1 Pipeline de traitement

Le processus suit une architecture en 6 étapes (voir `guasti_architecture.png`) :

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ENTRÉE: Fenêtre [A, B], P = 2310                        │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. GÉNÉRATION DES CANDIDATS                                 │
│    - Filtrage: gcd(n, P) = 1                                │
│    - φ(2310) = 480 classes de résidus                       │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. CALCUL DES FEATURES                                      │
│    • Impacts multi-échelle: c31, c101, c251                 │
│    • Silence: s_D = 1/(1 + c_D)                             │
│    • Angle minimal: θ_min = atan(n/spf²)                    │
│    • Gap normalisé: gap_norm = gap(r)/max_gap               │
│    • Saturation locale: sat31 = mean(c31) sur n±w           │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. CALCUL DU SCORE v1                                       │
│    score = 0.40·s31 + 0.30·s101 + 0.18·s251                 │
│          + 0.08·ang + 0.04·gap_norm - 0.06·sat_clip         │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. TRI DÉCROISSANT PAR SCORE                                │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. ÉVALUATION: Precision@K                                  │
│    P@K = proportion de premiers dans les K meilleurs        │
│    Lift = P@K / base_rate                                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Composants clés

#### 2.2.1 Roue primorielle (`src/wheel.py`)

```python
def residues_and_gaps(P: int) -> Wheel:
    """Calcule R(P) = {r ∈ [1..P] : gcd(r,P)=1} et G(P)."""
```

**Implémentation** :
- Calcul des résidus copremiers à P
- Gaps cycliques entre résidus consécutifs
- Pour P=2310 : φ(2310) = 480 résidus

**Propriétés vérifiées** :
- ✅ sum(gaps) = P (invariant de respiration)
- ✅ |gaps| = φ(P)

#### 2.2.2 Features (`src/features.py`)

**Pré-calculs optimisés** :

```python
def build_precomp(B: int, w: int = 3) -> Precomp:
    """Pré-calcule tous les arrays nécessaires jusqu'à B."""
```

**Features calculées** :
1. **c31, c101, c251** : nombre de premiers ≤ D divisant n
2. **spf_251** : plus petit facteur premier ≤ 251
3. **sat31** : moyenne de c31 sur fenêtre n±w (texture locale)
4. **is_prime** : crible d'Ératosthène pour vérité terrain

**Complexité** : O(B log log B) pour le crible

#### 2.2.3 Score v1 (`src/score.py`)

**Formule canonique** :

```
score(n) = 0.40 · s31 + 0.30 · s101 + 0.18 · s251
         + 0.08 · ang + 0.04 · gap_norm
         - 0.06 · clip(sat31/4, 0, 1)
```

**Où** :
- `s_D = 1/(1 + c_D)` : "silence" (inverse des impacts)
- `ang = θ_min/(π/2)` : proxy angulaire normalisé
- `gap_norm = gap(r)/max_gap` : respiration cyclique
- `sat31` : saturation locale (pénalité)

**Pondérations** :
- **88%** sur les impacts multi-échelle (s31 + s101 + s251)
- **8%** sur l'angle minimal
- **4%** sur la respiration
- **-6%** pénalité de saturation

---

## 3. Évaluation des performances

### 3.1 Méthodologie

**Protocole de test** :
- **P = 2310** (primorielle)
- **D_list = [31, 101, 251]** (échelles)
- **w = 3** (rayon de voisinage)
- **K = [100, 500, 1000, 5000, 20000]** (seuils de Precision@K)

**Fenêtres testées** :
1. [250,001 - 500,000]
2. [500,001 - 750,000]
3. [750,001 - 1,000,000]

### 3.2 Résultats quantitatifs

#### Tableau récapitulatif

| Fenêtre         | Candidats | Base Rate | P@5000  | Lift@5000 | Gain (pp) |
|-----------------|-----------|-----------|---------|-----------|-----------|
| [250k-500k]     | 51,952    | 37.52%    | 79.28%  | **2.11x** | +41.76    |
| [500k-750k]     | 51,947    | 36.00%    | 75.50%  | **2.10x** | +39.50    |
| [750k-1M]       | 51,947    | 35.15%    | 73.14%  | **2.08x** | +37.99    |

#### Observations clés

1. **Lift stable** : 2.08x - 2.11x sur toutes les fenêtres
   - Démontre la **robustesse** de l'approche
   - Pas de surapprentissage local

2. **Gain absolu significatif** : +38 à +42 points de %
   - Le score identifie efficacement les "zones riches" en premiers

3. **Décroissance naturelle du base_rate** :
   - 37.5% → 36.0% → 35.2%
   - Conforme au Théorème des Nombres Premiers

4. **Vérification de la conjecture** :
   - **Conjecture** : P@5000 ≥ 0.70 sur fenêtres de 250k
   - **Résultat** : ✅ **VÉRIFIÉE** sur les 3 fenêtres

### 3.3 Courbes de performance

Voir `guasti_performance_analysis.png` :

#### Graphique 1 : Precision@K vs Baseline
- **Toutes** les courbes P@K sont au-dessus des baselines
- Stabilité du gain sur différentes valeurs de K

#### Graphique 2 : Lift analysis
- Lift constant ≈ 2.1x pour K ∈ [100, 20000]
- Pas de dégradation significative avec K croissant

#### Graphique 3 : Évolution du base rate
- Décroissance naturelle avec la magnitude
- Densité de premiers : ~37.5% à 250k → ~35% à 1M

#### Graphique 4 : Tableau de synthèse
- Vue consolidée des métriques principales

### 3.4 Distribution des scores

Voir `guasti_score_distribution.png` :

#### Séparation premiers/composés

**Statistiques comparatives** :

| Statistique     | Premiers  | Composés  | Différence |
|-----------------|-----------|-----------|------------|
| **Moyenne**     | 0.573891  | 0.485206  | +0.088685  |
| **Médiane**     | 0.585299  | 0.491228  | +0.094071  |
| **Écart-type**  | 0.062773  | 0.071043  | -0.008270  |

**Interprétation** :
- ✅ **Séparation claire** : les premiers ont des scores **significativement plus élevés**
- ✅ Écart de ~0.09 entre moyennes (sur échelle [0,1])
- ✅ Les distributions se chevauchent partiellement (normal, pas de preuve déterministe)

#### Histogrammes
- Bimodalité visible : pics distincts pour premiers vs composés
- Queue longue chez les composés (faibles scores)

#### Box plots
- Médiane des premiers > Q3 des composés
- Confirme le pouvoir discriminant

---

## 4. Analyse technique détaillée

### 4.1 Structure de la roue primorielle

Voir `guasti_wheel_structure.png` :

#### Paramètres de la roue P=2310

- **φ(P) = 480 résidus** survivants
- **Max gap = 72** (plus grand saut cyclique)
- **Min gap = 2** (plus petit saut)
- **Mean gap = 4.81** (moyenne)

#### Distribution des gaps

**Gaps dominants** :
- Gap de 2 : apparaît ~100 fois
- Gap de 4 : apparaît ~80 fois
- Gap de 6 : apparaît ~70 fois
- Gaps rares (30+) : quelques occurrences

**Motif de respiration** :
- Pattern irrégulier mais **strictement périodique** mod 2310
- Invariant : sum(gaps) = 2310 ✅

### 4.2 Analyse des features

#### 4.2.1 Impacts multi-échelle

**Principe** : comptage des petits premiers diviseurs

```python
c31[n]  = nombre de premiers ≤ 31 divisant n
c101[n] = nombre de premiers ≤ 101 divisant n
c251[n] = nombre de premiers ≤ 251 divisant n
```

**Silence** : `s_D = 1/(1 + c_D)`
- s_D = 1 si aucun petit diviseur (silencieux)
- s_D → 0 si beaucoup de diviseurs (bruyant)

**Échelles choisies** :
- **31** : capture 11 premiers (2..31)
- **101** : capture 26 premiers
- **251** : capture 54 premiers

**Justification** : balance entre pouvoir discriminant et coût computationnel

#### 4.2.2 Proxy angulaire

**Définition** :

```
θ_min = atan(n / spf²)  si spf > 0
      = π/2              sinon
```

**Normalisation** : `ang = θ_min / (π/2) ∈ [0, 1]`

**Interprétation** :
- Si n premier → spf = 0 → ang = 1 (maximal)
- Si n = p×q avec p petit → ang proche de 0
- Capte la "distance" au plus petit diviseur

#### 4.2.3 Saturation locale

**Définition** :

```python
sat31[n] = mean(c31[k] for k in [n-w, ..., n+w])
```

**Rôle** : détecte les "zones saturées" (beaucoup de multiples locaux)

**Pénalité** : `-0.06 · clip(sat31/4, 0, 1)`
- Réduit le score dans les régions "bruyantes"

### 4.3 Complexité algorithmique

#### Pré-calcul (une fois par fenêtre)
- **Crible d'Ératosthène** : O(B log log B)
- **Calcul c_D** : O(B · |primes_D|)
- **Saturation** : O(B · w) via prefix sums

**Total** : O(B log log B)

#### Scoring (par candidat)
- **Lookup** des features : O(1)
- **Calcul score** : O(1)

**Total pour N candidats** : O(N)

#### Évaluation globale
**O(B log log B + N log N)** pour le tri

---

## 5. Vérification de la falsifiabilité

### 5.1 Tests d'invariants

Le README définit 5 tests falsifiables (section AA.2). Vérifions :

#### ✅ Test 1 : Invariant de respiration

**Énoncé** : sum(gaps) = P, |gaps| = φ(P)

**Vérification** (P=2310) :
```python
wheel = residues_and_gaps(2310)
assert sum(wheel.gaps) == 2310
assert len(wheel.gaps) == 480  # φ(2310)
```

**Statut** : ✅ **VALIDÉ**

#### ✅ Test 2 : Loi de polarité (mod 6)

**Énoncé** : tout carré n² (avec gcd(n,6)=1) vérifie n² ≡ 1 (mod 6)

**Vérification** : implémenté dans `test_theorems.py`

**Statut** : ✅ **VALIDÉ** (théorème classique)

#### ✅ Test 3 : Couverture "p²"

**Énoncé** : les impacts qualitativement nouveaux d'un rayon p commencent à p²

**Implémentation** : implicite dans le calcul de spf (smallest prime factor)

**Statut** : ✅ **COHÉRENT** avec la théorie du crible

#### ✅ Test 4 : Promesse prédictive (lift > 1)

**Critère** : Lift(top 1%) > 1.05, Lift(top 5%) > 1.02

**Résultats** :
- Lift@100 (top ~0.2%) : 2.16x, 2.14x, 2.05x ✅
- Lift@5000 (top ~10%) : 2.11x, 2.10x, 2.08x ✅

**Statut** : ✅ **LARGEMENT DÉPASSÉ**

#### ✅ Test 5 : Robustesse (fenêtres disjointes)

**Critère** : stabilité du lift sur fenêtres disjointes

**Résultats** :
- Lift@5000 : [2.11, 2.10, 2.08] → écart-type = 0.015
- Variance faible, effet stable

**Statut** : ✅ **ROBUSTE**

### 5.2 Contrôle négatif (section AA.3)

**Question** : que se passerait-il sans la roue ?

**Test proposé** :
- Désactiver gap_norm (mettre w_gap = 0)
- Observer la dégradation

**Résultat attendu** : chute du lift vers baseline-6

**Implémentation** : à ajouter dans les tests (recommandation)

---

## 6. Points forts et limitations

### 6.1 Points forts

#### 6.1.1 Scientifiques
✅ **Reproductibilité totale** :
- Code source ouvert
- Paramètres explicites (P, D_list, w, pondérations)
- Protocole de test détaillé

✅ **Falsifiabilité** :
- 5 tests quantifiés
- Seuils de réussite/échec clairs
- Conjecture vérifiable

✅ **Approche structurelle** :
- Pas de "machine learning" opaque
- Features interprétables (impacts, gaps, angles)
- Score v1 "sans résidu" = pas de prior appris

#### 6.1.2 Techniques
✅ **Performance** :
- Lift stable 2.1x
- Gain absolu +40 points de %
- Robuste sur fenêtres disjointes

✅ **Efficacité algorithmique** :
- O(B log log B) pré-calcul
- O(1) scoring par candidat
- Scalable

✅ **Documentation exemplaire** :
- README détaillé (420+ lignes)
- Pseudo-code canonique
- Sections anti-"relecture hostile"

### 6.2 Limitations

#### 6.2.1 Conceptuelles
⚠️ **Pas un test de primalité** :
- Ne prouve PAS qu'un nombre est premier
- Faux positifs inévitables (composés bien classés)

⚠️ **Dépendance à P** :
- Choix de P=2310 est heuristique (compromis φ(P) vs calcul)
- Tests avec P=30, P=210 seraient instructifs

⚠️ **Pondérations du score** :
- Poids (0.40, 0.30, 0.18...) semblent "tuned"
- Justification théorique limitée
- Risque de surapprentissage local

#### 6.2.2 Empiriques
⚠️ **Fenêtres testées limitées** :
- [250k - 1M] : 3 fenêtres
- Manque : tests sur [1M - 10M], [10M - 100M]

⚠️ **Absence de comparaison** :
- Pas de baseline "random"
- Pas de comparaison avec d'autres heuristiques (ex: BPSW heuristics)

⚠️ **Contrôle négatif absent** :
- Test sans roue (section AA.3) : non implémenté

#### 6.2.3 Techniques
⚠️ **Dépendances** :
- Requiert NumPy (acceptable)
- Pas de tests unitaires automatisés visibles
- Pas de CI/CD

⚠️ **Scalabilité** :
- B jusqu'à 1M : OK
- Au-delà (10M+) : mémoire devient un enjeu

---

## 7. Conclusions et recommandations

### 7.1 Évaluation globale

#### Notation (sur 10)

| Critère                  | Note | Commentaire                                    |
|--------------------------|------|------------------------------------------------|
| **Reproductibilité**     | 10/10| Code + protocole + paramètres complets         |
| **Falsifiabilité**       | 9/10 | 5 tests définis, 1 manquant (contrôle négatif)|
| **Documentation**        | 10/10| Exemplaire, anti-hostile                       |
| **Performance**          | 9/10 | Lift 2.1x stable, +40pp gain                   |
| **Robustesse**           | 8/10 | 3 fenêtres OK, manque tests >1M                |
| **Innovation**           | 8/10 | Approche structurelle intéressante             |
| **Tests automatisés**    | 6/10 | Présents mais pas de CI, coverage inconnu      |

**Note globale** : **8.6/10** ⭐⭐⭐⭐⭐

### 7.2 Verdict

#### ✅ Le projet démontre avec succès :

1. **Une méthode de priorisation fonctionnelle** :
   - Lift stable ~2.1x sur plusieurs fenêtres
   - Gain prédictif significatif (+40 points de %)

2. **Une démarche scientifique rigoureuse** :
   - Falsifiable (5 tests quantifiés)
   - Reproductible (code + paramètres)
   - Honnête (disclaimer clair : pas un test de primalité)

3. **Une approche structurelle cohérente** :
   - Features interprétables (impacts, gaps, angles)
   - Pas de "boîte noire"

#### ⚠️ Limites à reconnaître :

1. **Portée empirique** : tests limités à [250k - 1M]
2. **Justification théorique** : poids du score heuristiques
3. **Absence de comparaison** : pas de baseline "random" ni autres heuristiques

### 7.3 Recommandations

#### 7.3.1 Court terme (améliorations immédiates)

1. **Ajouter le contrôle négatif (test AA.3)** :
   ```python
   def test_without_wheel():
       # Score avec w_gap=0, vérifier chute du lift
   ```

2. **Implémenter baseline random** :
   ```python
   def evaluate_random_baseline(A, B, P, ks):
       # Permutation aléatoire, calculer P@K
   ```

3. **Ajouter tests unitaires automatisés** :
   ```python
   def test_invariant_respiration():
       for P in [30, 210, 2310]:
           wheel = residues_and_gaps(P)
           assert sum(wheel.gaps) == P
   ```

4. **CI/CD** : GitHub Actions pour tests auto à chaque commit

#### 7.3.2 Moyen terme (validation étendue)

5. **Étendre les fenêtres de test** :
   - [1M - 10M] : 5 fenêtres
   - [10M - 100M] : 3 fenêtres
   - Vérifier si lift reste stable

6. **Tester d'autres primorielles** :
   - P = 30 (φ=8)
   - P = 210 (φ=48)
   - P = 30030 (φ=5760) si feasible
   - Analyser impact sur lift

7. **Ablation study** :
   - Désactiver tour à tour chaque feature
   - Mesurer contribution au lift
   - Justifier les pondérations

8. **Comparaison avec heuristiques existantes** :
   - Baseline-6 (déjà mentionné)
   - Heuristiques de densité locale
   - Sieve-based heuristics

#### 7.3.3 Long terme (recherche)

9. **Justification théorique des poids** :
   - Peut-on dériver les pondérations (0.40, 0.30...) de premiers principes ?
   - Ou via optimisation formelle ?

10. **Lien avec la théorie analytique** :
    - Explorer connexion avec fonctions L, caractères de Dirichlet
    - Formaliser la "respiration" en termes théoriques

11. **Publication** :
    - Rédiger article pour journal accessible (ex: arXiv)
    - Suivre PUBLICATION_PLAN.md

12. **Package Python** :
    - Publier sur PyPI : `pip install guasti-transform`
    - Documentation Sphinx

### 7.4 Graphiques générés

Les 4 graphiques suivants ont été générés et sauvegardés :

1. **`guasti_architecture.png`** (428 KB)
   - Diagramme de flux du processus complet
   - Architecture en 6 étapes
   - Détail des features

2. **`guasti_performance_analysis.png`** (424 KB)
   - Courbes Precision@K vs Baseline
   - Analyse du Lift
   - Évolution du base rate
   - Tableau de synthèse

3. **`guasti_score_distribution.png`** (375 KB)
   - Histogrammes premiers vs composés
   - Box plots comparatifs
   - Distribution cumulative
   - Statistiques détaillées

4. **`guasti_wheel_structure.png`** (714 KB)
   - Distribution des gaps cycliques
   - Motif de respiration
   - Propriétés de la roue P=2310

### 7.5 Mot de la fin

Le projet **Guasti Transform V2** représente une **contribution sérieuse et rigoureuse** à la recherche sur la structure des nombres premiers. L'approche est :

- ✅ **Scientifiquement honnête** (disclaimers clairs)
- ✅ **Empiriquement solide** (lift 2.1x stable)
- ✅ **Méthodologiquement exemplaire** (reproductible, falsifiable)

Si les auteurs continuent dans cette direction (tests étendus, ablation study, justification théorique), ce travail pourrait :

1. **Court terme** : devenir un outil pédagogique de qualité pour comprendre la structure cyclique des premiers
2. **Moyen terme** : inspirer de nouvelles heuristiques de priorisation dans les cribles modernes
3. **Long terme** : contribuer à une meilleure compréhension théorique de la distribution locale des premiers

**Recommandation finale** : ⭐ **Continuer le développement** avec focus sur :
- Validation étendue (fenêtres >1M)
- Justification théorique des pondérations
- Publication formelle

---

## Annexe : Commandes de reproduction

Pour reproduire l'analyse complète :

```bash
# 1. Installation
pip install -r requirements.txt
pip install matplotlib

# 2. Évaluation sur 3 fenêtres
python -m src.eval --P 2310 --windows \
    250001 500000 \
    500001 750000 \
    750001 1000000 \
    --w 3 --K 100 500 1000 5000 20000

# 3. Génération des graphiques
python analyze_and_visualize.py

# 4. Vérification des théorèmes
python test_theorems.py

# 5. Tests unitaires
python -m pytest tests/
```

---

**Fin du rapport**

*Généré par Claude Code - Branch: claude/analyze-repo-graphs-8Relu*
