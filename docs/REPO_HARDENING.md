# docs/REPO_HARDENING.md
## Repo Hardening — ce qui est “blindé”

### CI & Style
- `ci.yml` : ruff + format check + pytest sur 3 versions Python
- `pre-commit` : empêche les erreurs triviales avant commit

### Documentation
- `docs-lint.yml` : fichiers obligatoires + markdownlint
- `links-check.yml` : vérifie les liens dans les `.md`

### Expériences
- `experiments.yml` : run manuel, artifacts upload
- `artifacts-index.yml` : journal automatique des runs

### Sécurité / Hygiène
- `hardening.yml` :
  - blocage fichiers > 20MB
  - scan minimal “secret-like”

### Bonnes pratiques
- `.gitignore` : évite les résultats/données/venv
- `SECURITY.md` : vuln reporting
- `CODE_OF_CONDUCT.md` : cadre social
- `CITATION.cff` : citabilité

---
