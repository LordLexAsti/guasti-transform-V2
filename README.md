# Guasti — Ordre cyclique & score multi-échelle (P = 2310)

Ce dépôt documente une étape **reproductible** et **falsifiable** de l’approche “Grille / Transformée de Guasti” appliquée à la **priorisation** des candidats premiers via :
- un **ordre cyclique** (roue primorielle) : classes résiduelles copremières à `P`,
- un **motif de respiration** : gaps cycliques entre résidus survivants,
- une annotation “Guasti-compatible” : **seuls les impacts de divisibilité** (rayons) sont utilisés,
- un **score** multi-échelle + texture locale, mesuré par **precision@K**.

> Important : ce travail **ne prouve pas** la primalité et **ne prétend pas** résoudre l’Hypothèse de Riemann.  
> Il fournit une méthode de **tri / priorisation** dans un espace de candidats cycliquement structuré.

---

## 1) Définitions

### 1.1 Roue primorielle (ordre cyclique des candidats)

Soit `P` une primorielle (ici `P = 2310 = 2·3·5·7·11`).

Les **résidus survivants** (candidats possibles) sont :
\[
R(P)=\{r\in\{1,\dots,P\}:\gcd(r,P)=1\}.
\]

Tout entier `n` tel que `gcd(n,P)=1` appartient à une classe :
\[
n \equiv r \pmod P,\quad r\in R(P).
\]

C’est l’**ordre cyclique** de base : l’ensemble des candidats est périodique modulo `P`.

### 1.2 Motif de respiration

Écrire `R(P)` trié :
\[
R(P)=\{r_1<r_2<\dots<r_{\varphi(P)}\}.
\]

Définir les **gaps cycliques** :
\[
g_i =
\begin{cases}
r_{i+1}-r_i & \text{pour } i<\varphi(P),\\
(P+r_1)-r_{\varphi(P)} & \text{pour } i=\varphi(P).
\end{cases}
\]

Le **motif de respiration** est :
\[
\mathcal{G}(P)=(g_1,\dots,g_{\varphi(P)}),
\]
avec \(\sum g_i = P\).

---

## 2) Annotation Guasti-compatible : “rayons” (divisibilité) & texture

### 2.1 Impacts multi-échelle (rayons)

On fixe des échelles `D_list = [31, 101, 251]` (nombres premiers ≤ D).

Pour un entier `n`, on note :
- `cD(n)` : nombre de **premiers** `p ≤ D` tels que `p | n`,
- `sD(n) = 1/(1 + cD(n))` : “silence” (plus cD est petit, plus c’est silencieux).

On utilise donc :
- `s31(n)`, `s101(n)`, `s251(n)`.

### 2.2 Proxy angulaire minimal (optionnel mais utilisé)

On note `spf(n)` le plus petit diviseur premier `≤ 251` (ou 0 si aucun).

\[
\theta_{\min}(n) =
\begin{cases}
\arctan\big(n / \mathrm{spf}(n)^2\big) & \text{si spf(n)>0},\\
\pi/2 & \text{sinon (silence)}.
\end{cases}
\]

Normalisation :
\[
ang(n) = \theta_{\min}(n) / (\pi/2) \in [0,1].
\]

### 2.3 Texture locale (saturation de voisinage)

On définit une fenêtre locale de rayon `w` (ici `w=3`) et :
- `sat31(n)` : moyenne de `c31` sur `[n-w, …, n+w]`.

Intuition : une zone localement saturée en impacts (beaucoup de multiples) est moins “prime-ish”.

---

## 3) Score v1 (sans résidu) — Version recommandée pour relecture hostile

Paramètres :
- `P = 2310`
- `D_list = [31, 101, 251]`
- `w = 3`

Pour un candidat `n` (avec `gcd(n,P)=1`), définir :
- `r = n mod P` (remplacer `0` par `P`),
- `gap_norm = gap(r) / max(G(P))`.

**Score v1 (sans résidu)** :
\[
\mathrm{score}(n)=
0.40\,s31(n) + 0.30\,s101(n) + 0.18\,s251(n)
+ 0.08\,ang(n)
+ 0.04\,gap\_norm(n)
- 0.06\,\mathrm{clip}\big(sat31(n)/4, 0, 1\big).
\]

> Cette version n’utilise **aucun prior appris** sur les résidus : elle est plus “structurelle”.

---

## 4) Pseudo-code (canonique)

```pseudo
P := 2310
D_list := [31, 101, 251]
w := 3

R := { r in 1..P : gcd(r,P)=1 }
G := gaps cycliques de R
gap_of_residue[r] := gap associé
max_gap := max(G)

Precompute primes ≤ 251
Precompute for all n:
  c31[n], c101[n], c251[n]  # nb de petits premiers divisant n
  sat31[n]                  # moyenne locale de c31 sur n±w
  spf[n]                    # plus petit diviseur premier ≤ 251 sinon 0

Candidates C := { n in [A..B] : gcd(n,P)=1 }

For each n in C:
  s31 := 1/(1+c31[n]); s101 := 1/(1+c101[n]); s251 := 1/(1+c251[n])
  if spf[n]==0: theta_min := π/2 else theta_min := atan(n/spf[n]^2)
  ang := theta_min/(π/2)
  r := n mod P; if r==0 then r:=P
  gap_norm := gap_of_residue[r] / max_gap
  neigh := sat31[n]

  score(n) :=
     0.40*s31 + 0.30*s101 + 0.18*s251
   + 0.08*ang + 0.04*gap_norm
   - 0.06*clip(neigh/4,0,1)

Sort C by score descending
Measure precision@K for K ∈ {100,500,1000,5000,20000}
```

---

## 5) Métrique : Precision@K (priorisation)

On mesure :
- `base_rate` : taux de premiers parmi les candidats `gcd(n,P)=1`,
- `P@K` : proportion de nombres premiers dans les `K` meilleurs scores.

> `P@K` évalue la **qualité de tri**, pas une preuve de primalité.

---

## 6) Reproduction rapide

### Installer
```bash
pip install -r requirements.txt
```

### Exemple : une fenêtre
```bash
python -m src.eval --P 2310 --A 500001 --B 1000000 --w 3 --K 100 500 1000 5000 20000
```

### Exemple : 4 fenêtres (falsifiabilité)
```bash
python -m src.eval --P 2310 --windows 2 250000 250001 500000 500001 750000 750001 1000000 --w 3 --K 5000
```

---

## 7) Conjecture falsifiable

**Conjecture-Score2310-v1**  
Avec `P=2310`, `D_list=[31,101,251]`, `w=3`, score v1 sans résidu :

> Sur toute fenêtre de taille 250 000 située dans `[250001, 1000000]`, on observe **P@5000 ≥ 0,70**.

**Réfutation** : si une fenêtre valide ces paramètres et donne **P@5000 < 0,70**, la conjecture est réfutée (pour cette version).

---



## Y) Loi de polarité (mod 6) — formulation canonique

Pour tout entier \(n\) **copremier à 6** (donc non divisible par 2 ni par 3), on définit :

- **Droite** `D` si \(n\equiv 1 \pmod 6\)
- **Gauche** `G` si \(n\equiv 5 \pmod 6\) (i.e. \(n\equiv -1 \pmod 6\))

On peut définir une “charge” :

\[
\chi(n)=\begin{cases}
+1 & \text{si } n\equiv 1\ (\mathrm{mod}\ 6),\\
-1 & \text{si } n\equiv 5\ (\mathrm{mod}\ 6).
\end{cases}
\]

**Lemme (polarité multiplicative mod 6).**  
Si \(\gcd(a,6)=\gcd(b,6)=1\), alors \(\chi(ab)=\chi(a)\chi(b)\).  
En particulier :

- `G × G → D` (\(-\times- = +\))
- `D × D → D` (\(+\times+ = +\))
- `G × D → G` (\(-\times+ = -\))

Et comme corollaire : pour tout \(n\) copremier à 6, \(n^2\equiv 1\pmod 6\) — **les carrés survivants tombent toujours à Droite**.



## Z) Trinité fondatrice (niveau Guasti)

Ce bloc formalise **ton intuition** : 1–2–3 ne sont pas seulement “les premiers nombres”, ce sont les **fondations computationnelles** du stade.

> **Trinité fondatrice (niveau Guasti)**  
> **1** est le repère (unité / alignement).  
> **2** est l’opérateur de parité (duplication minimale : 1+1) ; il tranche l’espace pair/impair.  
> **3** est l’opérateur de rythme (premier impair structurant) ; avec 2, il installe le cycle mod 6 et les piliers.  
> Ensemble, ils définissent le stade sur lequel la respiration cyclique et les rayons des autres premiers deviennent lisibles.

**Note “relecture hostile” (importante)** : ceci décrit un **statut fonctionnel** dans le moteur de filtrage (grille/tamis), **pas** une redéfinition de la primalité au sens classique. Arithmétiquement, 2 et 3 restent des nombres premiers standard ; opératoirement, ils jouent un rôle d’architectes car ils définissent la première compression (mod 6).

## AA) Falsifiabilité (tests quantifiés + lecture hostile)

Cette section définit **ce qui peut échouer** (et donc ce qui rend l’approche testable).  
Elle distingue : (i) des **invariants** (doivent être vrais si l’implémentation est correcte), (ii) des **promesses** (doivent battre des baselines), (iii) des **limites** (où la méthode ne prétend pas faire mieux).

### AA.1 Définitions (pour mesurer sans poésie)

On se donne un primorial \(P\in\{30,210,2310,\dots\}\) et une fenêtre d’étude \([A,B]\).

- **Candidats wheel** : \(C(P;A,B)=\{n\in[A,B] : \gcd(n,P)=1\}\).
- **Vérité terrain** :
  - `isPrime(n)` via test déterministe 64-bit (Miller–Rabin bases fixes) ou via crible exact pour fenêtres petites.
  - Optionnel : `smallFactor(n)` = plus petit facteur premier \(\le \sqrt{n}\) s’il existe.

- **Score Guasti** (abstrait) : une fonction \(S(n)\) qui ordonne/annote les candidats (polarité, impacts attendus, signatures, etc.).  
  *Important :* la falsifiabilité ne dépend pas de la formule exacte, mais d’un protocole de comparaison.

Mesures standards :
- **Densité de premiers** sur un ensemble \(X\) : \(\pi(X)/|X|\).
- **Precision@k** : proportion de premiers parmi les \(k\) meilleurs candidats selon \(S\).
- **Lift** vs baseline : \(\text{lift} = \frac{\text{densité(primes dans top)} }{\text{densité(primes dans baseline)}}\).
- **Erreur** : faux positifs / faux négatifs (si on “prédit premier” ou “prédit composé”).

Baselines minimales (simples, donc cruelles) :
1) **Baseline-6** : candidats \(6n\pm1\) (sans roue).
2) **Baseline-wheel** : candidats \(\gcd(n,P)=1\) **sans scoring** (ordre naturel).
3) **Random** : permutation aléatoire des mêmes candidats (contrôle statistique).

---

### AA.2 Cinq tests falsifiables (ce qui te met vraiment en danger)

#### Test 1 — Invariant de respiration (wheel) : signature des gaps
**Énoncé.** Pour un primorial \(P\), la respiration \(\mathcal{G}(P)\) (suite cyclique des gaps entre résidus copremiers à \(P\)) doit :
- sommer à \(P\),
- contenir exactement \(\varphi(P)\) pas (où \(\varphi\) est l’indicatrice d’Euler),
- être identique à la respiration canonique calculée indépendamment.

**Réfutation.** Une seule fenêtre où la somme \(\ne P\) ou où le multiset des gaps diffère → implémentation ou définition incohérente.

---

#### Test 2 — Loi de polarité (mod 6) + exclusion des carrés à Gauche
**Énoncé.** Pour tout \(n\) copremier à 6 : \(n^2\equiv 1\pmod 6\).  
Donc **aucun** carré \(m^2\) (avec \(\gcd(m,6)=1\)) ne peut tomber en \(6k-1\).

**Réfutation.** Trouver un seul carré \(m^2\equiv 5\pmod 6\) → impossible (erreur logique ou erreur de code de polarité).

---

#### Test 3 — Couverture “p²” (événements nouveaux) : apparition structurelle
**Énoncé (niveau moteur).** Si l’on ajoute un rayon \(p\ge 5\) dans le modèle, les **événements qualitativement nouveaux** (auto-intersection du rayon, nouveaux impacts systématiques) commencent à \(p^2\).

**Mesure.** Sur une fenêtre \([A,B]\), on compare la distribution des “impacts attribués à \(p\)” avant et après \(p^2\) (par annotation, pas par intuition).

**Réfutation.** Si l’annotation attribue régulièrement des “événements nouveaux” à \(p\) bien avant \(p^2\) sans explication cohérente (ex : déjà expliqués par facteurs plus petits), le principe est faux ou mal défini.

---

#### Test 4 — Promesse prédictive : le score doit battre la roue (lift > 1)
**Énoncé.** Pour une fenêtre large (ex : 1e6 à 1e7 selon capacités), et un \(P\) fixé (ex : 2310) :
- on prend les candidats \(C(P;A,B)\),
- on ordonne par \(S(n)\),
- on mesure la densité de premiers dans le **top 1%** et le **top 5%**.

**Critère minimal (falsifiable).**
- Lift(top 1%) > 1.05
- Lift(top 5%) > 1.02  
(à ajuster, mais il faut **>1** de façon stable sur plusieurs fenêtres)

**Réfutation.** Si le lift ≈ 1 (ou < 1) de manière stable, alors le score n’apporte pas de pouvoir prédictif au-delà de la roue : joli dessin, zéro moteur.

---

#### Test 5 — Robustesse en “relecture hostile” : stabilité sur fenêtres disjointes
**Énoncé.** Les résultats du Test 4 doivent être stables sur des fenêtres disjointes :
- \([A,B]\), \([A+\Delta,B+\Delta]\), \([A+2\Delta,B+2\Delta]\) avec \(\Delta\) grand.

**Mesure.** Variance du lift et des Precision@k.  
**Réfutation.** Si l’effet apparaît seulement “là où ça arrange” et s’effondre ailleurs → surapprentissage de motifs locaux (apophénie), pas une loi.

---

### AA.3 Variante “sans résidu” (contrôle négatif)
On désactive l’information “wheel/résidus” et on garde seulement :
- la polarité mod 6 (G/D),
- et/ou une annotation minimale.

**Attendu (hostile).** Les performances doivent chuter vers Baseline-6.  
Si elles ne chutent pas, c’est que tu réinjectes implicitement la roue (fuite d’info).

---

### AA.4 Ce que cette section te protège (et t’oblige à faire)
- Elle empêche le “c’est beau donc c’est vrai”.
- Elle force un protocole reproductible : mêmes fenêtres, mêmes baselines, même métrique.
- Elle donne une porte de sortie honnête : *si ça ne bat pas la roue, alors c’est une visualisation/pédagogie, pas un prédicteur.*
## X) Visualisation ASCII (mod 30 / mod 2310)

Un mini-script est fourni pour imprimer un “tamis angulaire” façon *tour + balcons*.

### Mod 30 (autour du pilier 30)
```bash
python -m src.ascii_tower --P 30 --m 1 --span 80 --rays "7,11,13,17" --show-respiration --resp-k 16 --show-polarity --show-signature
```

### Mod 2310 (autour du pilier 2310)
```bash
python -m src.ascii_tower --P 2310 --m 1 --span 400 --rays "13,17,19,23,29,31" --show-respiration --resp-k 24 --show-polarity --show-signature
```

Notes :
- `--span` contrôle la taille de la fenêtre autour du pilier `P*m`.
- `--rays` ne sert qu’à annoter des “impacts évidents” (divisibilité par ces rayons) avant la vérification MR.
- Les 💎 affichés sont testés par Miller–Rabin déterministe 64-bit (donc fiables pour nos tailles usuelles).


## 8) Organisation du code

- `src/wheel.py` : calcul de `R(P)` et `G(P)`
- `src/features.py` : pré-calculs (primes, impacts, spf, saturation)
- `src/score.py` : score v1 (sans résidu)
- `src/eval.py` : extraction candidats + calcul `P@K` + fenêtres
- `notebooks/` : espace de démonstration (optionnel)

---

---

## 9) Tamis Angulaire (schéma ASCII) — version “reviewer hostile”

### 9.1 Filtre mod 6 (piliers 6k : respiration grossière)

Pour tout premier \(p>3\), on a nécessairement \(p \equiv 1\) ou \(5 \pmod 6\), donc \(p=6k\pm1\).
Ce filtre est **vrai** mais **grossier** : il élimine uniquement les multiples de 2 et 3.

Schéma (exemple autour de 90) :

```
...  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98 ...
      X       X       X       X   P   X   C   X       X   C   X   P
          (6k-1)    (6k)     (6k+1)
```

- `X` : éliminé d’office (pair ou multiple de 3)
- `P` : premier (parmi les survivants)
- `C` : composé (parmi les survivants)

### 9.2 Filtre mod 2310 (roue primorielle : respiration haute définition)

Avec \(P=2310=2·3·5·7·11\), les candidats sont exactement :
\[
C=\{n:\gcd(n,P)=1\} = \bigcup_{r\in R(P)} \{n\equiv r \pmod P\}.
\]

Le tour complet contient \(\varphi(P)=480\) résidus survivants.
Le motif de respiration \(\mathcal{G}(P)\) décrit les **gaps cycliques** entre ces résidus.

ASCII (un tour de roue) :

```
2310m |---g1---| r1 |--g2--| r2 |--g3--| r3 | ... |--g480--| r480 | ↺
        ^              ^              ^
   cases impossibles   candidats       candidats
   (touchées par       (coprimes)     (coprimes)
   2,3,5,7,11)
```

### 9.3 Lemme “entrée en jeu à p²” (principe de crible, formulation Guasti)

> **Lemme (début d’action d’un rayon \(p\))**  
> Si un entier composé \(n\) a pour plus petit facteur premier \(p\), alors \(n \ge p^2\).  
> Donc avant \(p^2\), le “rayon \(p\)” n’élimine **aucun** candidat qui n’aurait déjà été éliminé par des facteurs plus petits.

Interprétation “Tamis Angulaire” : chaque nouveau premier \(p\) ne commence à créer des “pièges” (intersections inédites) qu’à partir de \(p^2\).
C’est une justification structurelle (et standard) du fait que la grille se “sature” par paliers.

### 9.4 Ce que l’on affirme (et ce que l’on n’affirme pas)

- ✅ **Certain** : la périodicité des candidats modulo \(P\) (roue) et l’invariant \(\mathcal{G}(P)\).
- ✅ **Mesurable / falsifiable** : la performance de tri (P@K) du score v1 sur des fenêtres disjointes.
- ❌ **Non-claim** : aucune “preuve” de primalité, aucune démonstration de RH, aucune formule fermée.

---

## 10) License

À définir (MIT recommandé pour diffusion/interop).
