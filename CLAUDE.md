# OneDrive Resetter

App tkinter para Windows que termina y reinicia OneDrive al abrirse.

- Metodología: Spec-Driven Development. Leer `specs/constitution.md` y `specs/001-onedrive-resetter/` antes de cambiar nada; actualizar specs, skills y agents con cada cambio para no perder contexto.
- Agentes: `.claude/agents/` (python-gui-dev, release-manager, security-reviewer).
- Skills: `.claude/skills/` (comment-code, release-versioning, github-publish, i18n-maintenance).
- Tests: `python -m unittest discover -s tests -v`
- Build: `powershell -ExecutionPolicy Bypass -File build.ps1`
