# 🚀 GUIDE DE MISE EN LIGNE GITHUB

## Pour débutants - Étape par étape

---

## 📋 Prérequis

Avant de commencer, assure-toi d'avoir :

1. **Un compte GitHub** → https://github.com/join
2. **Git installé** sur ton ordinateur
   - Windows : Télécharge depuis https://git-scm.com/download/win
   - Mac : `brew install git` ou télécharge depuis https://git-scm.com/download/mac
   - Linux : `sudo apt install git`

---

## 🔧 Configuration initiale (une seule fois)

Ouvre un terminal et configure ton identité Git :

```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton.email@example.com"
```

---

## 📦 Option A : Mettre à jour ton dépôt existant

Tu as déjà un dépôt `guasti-transform`. Voici comment le mettre à jour :

### Étape 1 : Clone ton dépôt existant

```bash
# Dans un dossier de ton choix
cd ~/Documents
git clone https://github.com/LordLexAsti/guasti-transform.git
cd guasti-transform
```

### Étape 2 : Remplace les fichiers

Copie tous les nouveaux fichiers (que je t'ai fournis) dans ce dossier.

### Étape 3 : Ajoute et envoie les modifications

```bash
# Voir ce qui a changé
git status

# Ajouter tous les nouveaux fichiers
git add .

# Créer un commit avec un message descriptif
git commit -m "Version 2.0 : 9 théorèmes validés, palimpseste, validation TriadIA"

# Envoyer sur GitHub
git push origin main
```

---

## 📦 Option B : Créer un nouveau dépôt

### Étape 1 : Crée le dépôt sur GitHub

1. Va sur https://github.com/new
2. Nom du dépôt : `guasti-transform` (ou un nouveau nom)
3. Description : "A Geometric Framework for Multiplicative Structure Analysis"
4. Choisis "Public"
5. **NE PAS** cocher "Add a README" (on en a déjà un)
6. Clique "Create repository"

### Étape 2 : Initialise le dépôt local

Dans ton terminal, va dans le dossier contenant les fichiers :

```bash
cd /chemin/vers/guasti-transform-v2

# Initialise Git
git init

# Ajoute tous les fichiers
git add .

# Crée le premier commit
git commit -m "Initial commit: Guasti Transform v2.0"

# Connecte au dépôt GitHub (remplace par ton URL)
git remote add origin https://github.com/LordLexAsti/guasti-transform.git

# Envoie sur GitHub
git branch -M main
git push -u origin main
```

---

## 📁 Structure des fichiers à envoyer

Voici ce que tu dois avoir dans ton dossier :

```
guasti-transform/
├── README.md                 ← Présentation du projet
├── LICENSE                   ← Licence MIT
├── requirements.txt          ← Dépendances Python
├── .gitignore               ← Fichiers à ignorer
│
├── src/                     ← Code source
│   ├── __init__.py
│   ├── guasti_core.py       ← Fonctions principales
│   └── guasti_utils.py      ← Utilitaires
│
├── docs/                    ← Documentation
│   ├── PUBLICATION_PLAN.md
│   └── TRIADIA_CREDITS.md
│
├── examples/                ← Exemples
│   └── basic_usage.py
│
├── figures/                 ← Visualisations (optionnel)
│   └── (tes images PNG)
│
└── tests/                   ← Tests (optionnel)
    └── test_theorems.py
```

---

## ✅ Vérification

Après avoir poussé, vérifie que tout est en ligne :

1. Va sur https://github.com/LordLexAsti/guasti-transform
2. Vérifie que le README s'affiche correctement
3. Vérifie que les dossiers `src/`, `docs/`, `examples/` sont présents

---

## 🔄 Pour les mises à jour futures

Chaque fois que tu modifies quelque chose :

```bash
# Voir les modifications
git status

# Ajouter les fichiers modifiés
git add .

# Créer un commit
git commit -m "Description de ta modification"

# Envoyer sur GitHub
git push
```

---

## 🆘 Problèmes courants

### "Permission denied"

Tu dois te connecter à GitHub. Deux options :

**Option 1 : HTTPS avec token**
1. Va sur GitHub → Settings → Developer settings → Personal access tokens
2. Génère un nouveau token avec les droits "repo"
3. Utilise ce token comme mot de passe

**Option 2 : SSH (recommandé)**
```bash
# Génère une clé SSH
ssh-keygen -t ed25519 -C "ton.email@example.com"

# Affiche la clé publique
cat ~/.ssh/id_ed25519.pub

# Copie cette clé et ajoute-la sur GitHub :
# Settings → SSH and GPG keys → New SSH key
```

### "Repository not found"

Vérifie l'URL du dépôt :
```bash
git remote -v
```

Si l'URL est incorrecte :
```bash
git remote set-url origin https://github.com/LordLexAsti/guasti-transform.git
```

### "Merge conflict"

Si quelqu'un d'autre a modifié le dépôt :
```bash
git pull origin main
# Résous les conflits si nécessaire
git push
```

---

## 📚 Ressources utiles

- [GitHub Docs (français)](https://docs.github.com/fr)
- [Git - Petit guide](https://rogerdudler.github.io/git-guide/index.fr.html)
- [Learn Git Branching (interactif)](https://learngitbranching.js.org/?locale=fr_FR)

---

## 🎯 Résumé des commandes essentielles

| Commande | Description |
|----------|-------------|
| `git clone URL` | Télécharge un dépôt |
| `git status` | Voir l'état des fichiers |
| `git add .` | Ajouter tous les fichiers |
| `git commit -m "message"` | Créer un point de sauvegarde |
| `git push` | Envoyer sur GitHub |
| `git pull` | Récupérer les modifications |

---

**Bonne chance !** Si tu as des questions, n'hésite pas à demander. 🚀
