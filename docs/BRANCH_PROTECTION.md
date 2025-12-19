# docs/BRANCH_PROTECTION.md
## Branch protection “dernier cran” (à configurer dans GitHub UI)

> GitHub → Settings → Branches → Add rule (branch: `main`)

Activer :
- ✅ Require a pull request before merging  
  - ✅ Require approvals: **1** (ou 2 si tu veux “double verrou”)  
  - ✅ Dismiss stale approvals when new commits are pushed  
  - ✅ Require review from Code Owners
- ✅ Require status checks to pass before merging  
  - Cocher :
    - `ci (3.10)`
    - `ci (3.11)`
    - `ci (3.12)`
    - `docs-lint`
    - `links-check`
    - `hardening`
- ✅ Require conversation resolution before merging
- ✅ Require signed commits (optionnel mais très “armure”)
- ✅ Do not allow force pushes
- ✅ Do not allow deletions

Option “ultra” :
- ✅ Require linear history (évite les merge commits si tu préfères rebase)
- ✅ Restrict who can push to matching branches (toi uniquement)

Résultat :
- rien ne rentre dans `main` si :
  - pas relu (CODEOWNERS),
  - pas testé,
  - docs cassées,
  - liens morts,
  - gros fichier / secret suspect.
