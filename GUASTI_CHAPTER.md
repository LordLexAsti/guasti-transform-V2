# GUASTI_CHAPTER.md
## Chapitre — La Grille qui respire
### Version narrative (chapitre de livre)

> **Intention** : raconter l’idée sans la diluer.  
> **Promesse** : un lecteur curieux peut *comprendre*, un lecteur exigeant peut *tester*.

---

## 0. Ouverture : le bon outil rend le réel lisible
Il y a deux manières de parler des nombres premiers.

La première est la voie classique : on construit des fonctions, on écoute des fréquences, on suit des ombres analytiques. C’est puissant, mais ça ressemble parfois à regarder un paysage au travers d’un télescope inversé : beaucoup de détails… et une impression de brouillard.

La seconde voie, c’est celle que propose l’approche Guasti : déplacer la question. Non pas “où sont les nombres premiers ?”, mais “**qu’est-ce qui fait qu’un nombre composé devient visible, et qu’un premier reste silencieux ?**”. La thèse n’est pas que le chaos disparaît. La thèse est plus rude et plus vérifiable : **le chaos devient lisible** dès qu’on observe la divisibilité comme une géométrie.

---

## 1. Les fondations : 1, 2, 3 — la trinité fondatrice (statut opératoire)
Dans l’arithmétique standard, 2 et 3 sont des nombres premiers comme les autres.  
Dans le *moteur* Guasti (grille/tamis), ils ont un **statut fonctionnel** particulier : ce sont des architectes.

- **1** : le fondateur, l’unité, le repère. Il ne “gagne” pas, il **référence**.
- **2** : le découpeur binaire. Il introduit une séparation massive : pair/impair.
- **3** : le premier impair “fertile” (au sens structural). Il introduit le rythme : triangulation, cycle, charpente.

> **Lecture hostile (obligatoire)** : dire “architecte” ne change pas la définition de “premier”.  
> Cela décrit un rôle de *compression* et de *structure* dans un protocole de filtrage.

---

## 2. Le stade : piliers et couloirs (mod 6)
Quand 2 (parité) et 3 (rythme) ont fait leur travail, l’univers des candidats se rétrécit brutalement.  
Tout premier \(p>3\) doit être dans l’un des deux couloirs :

\[
p \equiv 1 \pmod 6 \quad \text{ou} \quad p \equiv 5 \pmod 6
\]
soit \(p=6k\pm1\).

Les multiples de 6 deviennent des **piliers** : une ossature.  
Entre les piliers, il reste deux balcons : le voisin de gauche \((6k-1)\) et le voisin de droite \((6k+1)\).

On n’a pas encore “trouvé” les premiers.  
On a fait mieux : on a **éliminé le bruit**.

---

## 3. La Grille : la divisibilité comme image
La Grille de Guasti encode une idée simple : un entier n’est pas d’abord une “quantité”, c’est une **signature**.

Dans la grille, une case “existe” (devient visible) parce que des diviseurs viennent y laisser une marque.  
Un composé brille comme un carrefour : il a plusieurs routes qui y arrivent.  
Un premier, lui, n’a (structurellement) rien à montrer : il reste silencieux, sauf le 1 et lui-même.

Le point clef : on ne parle pas d’un tableau de Pythagore où l’on “pointe” un produit.  
On parle d’un dispositif où **seuls les diviseurs apparaissent**.

---

## 4. Le Tamis angulaire : rayons, impacts, et survivants
Imagine maintenant un phare à l’origine : chaque diviseur est un **rayon**.  
Un nombre composé est une zone où les rayons convergent.  
Un premier est un endroit où **aucun rayon non trivial** ne converge.

Cette image est précieuse parce qu’elle donne une intuition opérationnelle :
- tu ne “cherches” pas un premier,
- tu observes un endroit qui **n’a pas été touché**.

La conséquence : le problème devient une dynamique d’**impacts**.

---

## 5. La polarité : gauche / droite (mod 6)
Les deux couloirs \(6k\pm1\) ne sont pas symétriques.  
On peut les doter d’une polarité :

- **Droite (D)** : \(n\equiv 1\pmod 6\)
- **Gauche (G)** : \(n\equiv 5\pmod 6\)

La multiplication conserve une logique de signes :

- \(G\times G \to D\)
- \(D\times D \to D\)
- \(G\times D \to G\)

Le fait brutal, testable, non-poétique :
\[
\gcd(n,6)=1 \Rightarrow n^2\equiv 1\pmod 6
\]
Donc **tous les carrés** survivants tombent à droite.  
La gauche n’est pas “pure” au sens “peu de composés” : elle est **exempte de carrés**. C’est plus solide.

---

## 6. La respiration : cycles qui montent en résolution (30, 210, 2310…)
Mod 6 est le premier étage.  
On peut durcir le filtre en montant en résolution : \(P = 30, 210, 2310,\dots\) (primorielles).

Pour chaque \(P\), on garde les résidus copremiers à \(P\).  
L’ordre de ces résidus possède une signature : la **respiration**, suite cyclique des gaps.

Ce n’est pas un slogan : c’est un invariant calculable.
- nombre de résidus = \(\varphi(P)\)
- somme des gaps = \(P\)

Et surtout : la respiration sert d’ossature annotable pour comparer, scorer, tester.

---

## 7. Ce que Guasti promet — et ce qu’il ne promet pas
Guasti promet un changement de perspective : rendre lisible un tissage multiplicatif par signatures, polarité et respiration.

Guasti ne promet pas une preuve de RH.  
Guasti ne promet pas un oracle à premiers.  
Guasti promet quelque chose de très sérieux : **un protocole qui peut échouer**, et donc qui peut réussir sans tricher.

---

## 8. Pont vers l’expérimentation
Le chapitre se ferme là où la science commence : sur des tests.

- Le dispositif “wheel” (mod 2310) est une baseline connue.
- La question est simple et cruelle : **le score Guasti fait-il mieux qu’une roue sans score ?**
- Si oui, on a un moteur prédictif.
- Si non, on a un outil pédagogique et une géométrie de signatures — ce qui est déjà une contribution.

---

**Fin du chapitre.**
