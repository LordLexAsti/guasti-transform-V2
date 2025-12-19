# SECURITY.md
## Politique de sécurité

Même si ce projet n’est pas un produit “security-critical”, il peut contenir :
- du code d’expérimentation,
- des scripts qui manipulent de gros volumes,
- des dépendances qui évoluent.

L’objectif ici : traiter proprement les vulnérabilités et éviter les dégâts collatéraux.

---

## 1) Versions supportées
Ce dépôt est en évolution. Les correctifs de sécurité sont appliqués sur :
- la branche `main` (toujours),
- les tags de release récents (si existants).

---

## 2) Signaler une vulnérabilité
### 2.1 Ce qui compte comme vulnérabilité
- Exécution de code arbitraire via entrées non fiables
- Fuite de secrets (tokens, clés API, données perso)
- Dépendances compromises
- Scripts pouvant supprimer/écraser des fichiers hors dossier prévu
- Téléchargements non vérifiés (supply chain)

### 2.2 Comment signaler
Merci de **ne pas ouvrir d’issue publique** pour une vulnérabilité exploitable.

Procédure :
1) Envoyer un message privé au mainteneur du dépôt (via GitHub profile) **ou** utiliser la fonctionnalité “Report a vulnerability” (si activée).
2) Inclure :
   - description courte
   - preuve de concept minimale (si possible)
   - environnement (OS, Python, version)
   - impact estimé
   - suggestions de mitigation

---

## 3) Bonnes pratiques dans ce dépôt
- Pas de secrets dans le code / commits / exemples.
- Utiliser `.env` et l’ignorer dans git (si nécessaire).
- Préférer des chemins relatifs confinés (`results/`, `data/`).
- Vérifier les hash si téléchargement d’artefacts externes.

---

## 4) Délais de réponse (indicatifs)
- Accusé de réception dès que possible.
- Patch dès qu’un correctif minimal est disponible.

---

## 5) Crédit
Si vous le souhaitez, vous serez crédité dans la note de release du correctif.
