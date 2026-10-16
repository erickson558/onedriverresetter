---
name: release-versioning
description: Sube la versión Vx.x.x (major/minor/patch), actualiza CHANGELOG y README, y compila el .exe. Úsala con cada cambio relevante.
---

Criterio SemVer:
- **major**: cambio incompatible (comportamiento o config rotos).
- **minor**: funcionalidad nueva compatible (p. ej. nuevo idioma, nueva opción).
- **patch**: corrección de errores, docs o refactor sin cambio funcional.

Pasos:
1. `python scripts/bump_version.py <major|minor|patch>` (actualiza `version.py` y README).
2. Añadir entrada en `CHANGELOG.md` con la versión y fecha.
3. Actualizar `specs/` si cambió el comportamiento.
4. `python -m unittest discover -s tests -v`
5. `powershell -ExecutionPolicy Bypass -File build.ps1` → `OneDriveResetter.exe` junto al `.py`.
6. Commit convencional y push (skill `github-publish`). El workflow crea tag y Release `Vx.x.x`.

Commits convencionales: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`; incluir `!` o `BREAKING CHANGE:` para major.
