---
name: github-publish
description: Sube cambios a GitHub (cuenta erickson558, repo público onedriverresetter) con commit convencional y push a main.
---

Cuenta: `erickson558` (ya autenticada con `gh auth login`; verificar con `gh auth status`).
**Nunca** escribir tokens en archivos, skills, commits ni logs; `gh` usa el keyring.

Primera vez:
```
git init -b main
git add . && git commit -m "feat: initial release V1.0.0"
gh repo create erickson558/onedriverresetter --public --source . --remote origin --push \
  --description "Restart OneDrive automatically when it stops responding"
```

Cambios posteriores:
```
git add -A
git status            # revisar que no haya secretos ni .exe
git commit -m "<tipo>: <resumen> (VX.Y.Z)"
git push origin main  # dispara el workflow de Release
gh run watch          # opcional: seguir el build
```
Verificar: `gh release view V<versión>`.
