# GUASTI_WHITEPAPER.md
## Grille de Guasti, Transformée de Guasti et Tamis Angulaire
### Document maître (version consolidée)

> **Statut** : document de travail reproductible (pédagogie + protocole expérimental).  
> **Principe** : re-description géométrique de la divisibilité ; pas de redéfinition de la primalité au sens classique.  
> **Objectif** : rendre la structure multiplicative **visible**, **annotable**, et **testable** (y compris en “relecture hostile”).

---

## Table des matières
1. Résumé exécutif  
2. Définitions et notations  
3. Axiomes opératoires (cadre Guasti)  
4. Manifeste Guasti — version “marbre”  
5. Exemples guidés (mod 30 puis mod 2310)  
6. Falsifiabilité : tests quantifiés + contrôle “sans résidu”  
7. Limites, non-claims, et interprétations correctes  
8. Feuille de route expérimentale (scripts, métriques, fenêtres)  
9. Annexes (pseudocode minimal)

---

## 1) Résumé exécutif
La **Grille de Guasti** représente la divisibilité des entiers dans un espace discret (2D) où un entier est lu via sa **signature de diviseurs**.  
Un **composé** apparaît comme une zone de convergence (plusieurs diviseurs actifs), tandis qu’un **premier** se lit comme un **silence structurel** (aucune intersection non triviale).

Au niveau opératoire, **2** et **3** jouent un rôle structurant (“architectes”) : ils imposent la parité et le cycle minimal mod 6, ce qui canalise tous les candidats premiers > 3 dans les deux couloirs **6k±1**.  
La méthode se prolonge par “montée en résolution” via des cycles primoriels (ex. **30**, **210**, **2310**), interprétés comme une **respiration** (suite cyclique d’écarts entre résidus survivants).

Ce document pose :
- des **définitions reproductibles** (grille, piliers, polarité, respiration),
- un **manifeste** stabilisé,
- des **tests falsifiables** (invariants + promesses + robustesse),
- et une **roadmap** pour évaluer la valeur prédictive au-delà des baselines.

---

## 2) Définitions et notations

### 2.1 La Grille (divisibilité)
On indexe une grille par :
- **lignes** : \(k \ge 1\)
- **colonnes** : \(n \ge 1\)

**Règle de remplissage** : la case \((k,n)\) est active si et seulement si \(k \mid n\).

- **Ligne 1** : table des 1, sert de référence d’alignement.
- **Colonne \(n\)** : encode tous les diviseurs de \(n\).
- **Diagonale \((n,n)\)** : diagonale d’identité (chaque point porte \(n\)), pas une diagonale “des carrés” au sens pythagoricien.

> **Conséquence** : un nombre premier \(p\) a exactement deux lignes actives dans sa colonne : \(1\) et \(p\).

### 2.2 Piliers (mod 6)
Après filtrage par 2 et 3 :
- les multiples de 6, \(6k\), forment des **piliers** (axe),
- les candidats premiers \(>3\) ne peuvent être que dans \(6k-1\) ou \(6k+1\).

### 2.3 Polarité (mod 6)
Pour les entiers copremiers à 6 :
- **Droite (D)** : \(n \equiv 1 \pmod 6\)
- **Gauche (G)** : \(n \equiv 5 \pmod 6\) (i.e. \(-1\pmod 6\))

La polarité est multiplicative :
- \(G\times G \to D\)
- \(D\times D \to D\)
- \(G\times D \to G\)

Corollaire invariant :
\[
\gcd(n,6)=1 \Rightarrow n^2 \equiv 1 \pmod 6.
\]
Donc aucun carré (copremier à 6) ne tombe dans \(6k-1\).

### 2.4 Respiration (cycle primoriel)
Soit un primorial (ou “roue”) :
\[
P=\prod_{p\le q} p \in \{30,210,2310,\dots\}.
\]
On définit :
- **Résidus survivants** : \(R(P)=\{r \in [1,P] : \gcd(r,P)=1\}\)
- **Respiration** : \(\mathcal{G}(P)\) = suite cyclique des écarts (gaps) entre résidus consécutifs de \(R(P)\) triés.

Invariants :
- \(|R(P)|=\varphi(P)\)
- la somme des gaps sur un tour vaut \(P\).

---

## 3) Axiomes opératoires (cadre Guasti)

**Axiome A — Espace (Grille)**  
La structure multiplicative peut être observée dans un espace 2D discret où la divisibilité devient géométrie (alignements, symétries, densités).

**Axiome B — Apparition (Diviseurs)**  
Un composé est défini par sa **signature de diviseurs** (plusieurs marques non triviales). Il est visible par convergence.

**Axiome C — Premier (Définition négative)**  
Un premier est un silence structurel : aucune intersection non triviale ne l’atteint (hors 1 et lui-même).

**Axiome D — Respiration (Cyclique)**  
Les candidats se structurent par cycles (mod 6, 30, 210, 2310…) : la “périodicité” est une respiration multi-échelle.

---

## 4) Manifeste Guasti — version “marbre”
Guasti propose une re-description géométrique et discrète de la structure multiplicative des entiers. Elle ne prétend pas remplacer l’arithmétique classique ni résoudre RH, mais offrir un langage alternatif où certains phénomènes deviennent visibles et testables.

### 4.1 Trinité fondatrice (niveau Guasti)
Dans l’arithmétique standard, 2 et 3 sont premiers.  
Dans le **moteur opératoire** Guasti, ils sont **architectes** : ils définissent la première compression de l’espace.

- **1** : unité et repère (alignement, référence), ni premier ni composé.  
- **2** : découpeur binaire (pair/impair) ; interdit structurellement les candidats pairs.  
- **3** : stabilisateur cyclique ; avec 2, installe le cycle mod 6 et les piliers.

> **Lecture hostile** : “architecte” = rôle fonctionnel dans le filtrage, pas redéfinition de la primalité.

### 4.2 Piliers et couloirs
\[
p>3 \Rightarrow p=6k\pm1.
\]
Les multiples de 6 sont les piliers (ossature). Les candidats résident dans les couloirs \(6k\pm1\).

### 4.3 Tamis angulaire
Un nombre composé est une convergence de rayons (diviseurs).  
Un nombre premier est un point où le tissage ne converge pas (silence).

### 4.4 Polarité
La polarité mod 6 encode une algèbre des positions et implique l’exemption de carrés dans \(6k-1\).

### 4.5 Respiration
La montée en résolution via \(P \in \{30,210,2310,\dots\}\) définit des respirations \(\mathcal{G}(P)\) (gaps) servant d’ossature expérimentale pour l’annotation et le scoring.

---

## 5) Exemples guidés

### 5.1 Exemple (mod 30)
Ici \(P=30=2\cdot3\cdot5\).  
Résidus copremiers à 30 :
\[
R(30)=\{1,7,11,13,17,19,23,29\}.
\]
Respiration (gaps cycliques) :
\[
\mathcal{G}(30) = [6,4,2,4,2,4,6,2]
\quad\text{(somme = 30, longueur = }\varphi(30)=8\text{)}.
\]

Interprétation “tamis” :
- les candidats sont déjà filtrés contre 2, 3, 5 ;
- le “reste” se distribue selon cette respiration ;
- les nouveaux impacts qualitatifs du rayon 5 commencent à \(5^2=25\) (dans le couloir Droite).

### 5.2 Exemple (mod 2310) — méthode
Ici \(P=2310=2\cdot3\cdot5\cdot7\cdot11\).  
On ne liste pas \(R(2310)\) en entier (480 résidus), on fixe la procédure :

1) Générer \(R(2310)=\{r\in[1,2310] : \gcd(r,2310)=1\}\).  
2) Trier \(R(2310)\), calculer les gaps cycliques \(\mathcal{G}(2310)\).  
3) Pour une fenêtre \([A,B]\), les candidats wheel sont :
\[
C(2310;A,B)=\{n\in[A,B] : \gcd(n,2310)=1\}.
\]
4) Annoter chaque candidat par :
- polarité mod 6 (G/D),
- distance au pilier mod 6 (±1),
- résidu mod 2310 (position dans la respiration),
- impacts attendus par rayons (au moins \(p\ge 13\), puisque 2,3,5,7,11 sont déjà filtrés).

Exemples de résidus valides (illustratifs) : 1, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47… (tous copremiers à 2,3,5,7,11).

---

## 6) Falsifiabilité : tests quantifiés + contrôle “sans résidu”

### 6.1 Mesures
- densité : \(\pi(X)/|X|\)
- Precision@k
- lift vs baselines (baseline-6, baseline-wheel, random)

### 6.2 Cinq tests falsifiables
**Test 1 — Invariant respiration (wheel)**  
Somme des gaps = \(P\), longueur = \(\varphi(P)\), signature stable.

**Test 2 — Polarité + exemption des carrés à Gauche**  
Aucun carré copremier à 6 ne tombe en \(6k-1\).

**Test 3 — Événements nouveaux à partir de \(p^2\)**  
Les impacts qualitativement nouveaux d’un rayon \(p\) commencent à \(p^2\) (auto-intersection).

**Test 4 — Promesse prédictive : lift > 1**  
Le scoring Guasti doit enrichir la densité de primes dans les tops (top 1%, top 5%) au-delà de baseline-wheel.

**Test 5 — Robustesse : stabilité sur fenêtres disjointes**  
L’effet (lift, precision) doit persister hors de fenêtres “chanceuses”.

### 6.3 Contrôle négatif “sans résidu”
Désactiver l’info wheel (résidu mod \(P\)).  
Attendu : retour vers baseline-6 / baseline-wheel.  
Si l’effet ne chute pas, suspecter fuite d’information ou sur-ajustement.

---

## 7) Limites et non-claims (lecture hostile)
- Guasti ne redéfinit pas la primalité classique.  
- Guasti n’est pas une preuve de RH.  
- Guasti peut être (a) un excellent outil pédagogique/visualisation, et (b) un prédicteur **uniquement si** les tests de lift/robustesse passent.  
- Si le score ne bat pas baseline-wheel : la contribution est principalement **interface, nomenclature, visualisation, pédagogie** (ce qui est déjà une contribution).

---

## 8) Feuille de route expérimentale
1) Implémenter `wheel_residues(P)` + `gaps(P)`  
2) Implémenter `candidates(A,B,P)`  
3) Implémenter un `score(n)` (version minimale d’abord)  
4) Mesurer lift/precision sur 10 fenêtres disjointes  
5) Comparer à baselines (6n±1, wheel, random)  
6) Documenter résultats (tableaux + graphiques)  
7) Itérer sur la définition du score (sans tricher : protocole fixe)

---

## 9) Annexe — pseudocode minimal

### 9.1 Résidus + respiration
```pseudo
function residues(P):
  R = []
  for r in 1..P:
    if gcd(r, P) == 1:
      R.append(r)
  return R

function gaps(P):
  R = residues(P)
  sort(R)
  G = []
  for i in 0..len(R)-2:
    G.append(R[i+1] - R[i])
  G.append(P + R[0] - R[-1])   # gap cyclique
  return G
