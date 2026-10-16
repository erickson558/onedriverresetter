# Plan técnico — Spec 001

| Módulo | Responsabilidad |
|---|---|
| `onedriverresetter.py` | Lógica de procesos (`list_onedrive_processes`, `kill_process`, `find_onedrive_exe`, `reset_onedrive`), persistencia de idioma y GUI tkinter. |
| `i18n.py` | Diccionarios de traducción, `t()`, `detect_language()`. |
| `version.py` | Versión única. |
| `scripts/bump_version.py` | Sube versión y actualiza README. |
| `build.ps1` | PyInstaller → `OneDriveResetter.exe` junto al `.py`. |
| `.github/workflows/release.yml` | Tests, build y Release automático por versión nueva. |

## Decisiones
- `tasklist`/`taskkill` en lugar de `psutil`: cero dependencias.
- `reset_onedrive(emit)` emite claves i18n: la lógica no conoce la GUI ni el idioma, y el registro se re-traduce al cambiar de idioma.
- Hilo + `queue.Queue` + `after()` para mantener la GUI fluida (tkinter no es thread-safe).
- Release solo si el tag `Vx.x.x` no existe: permite pushes sin release (docs) y evita duplicados.
