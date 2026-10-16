# OneDrive Resetter

![License](https://img.shields.io/badge/license-Apache%202.0-blue) ![Platform](https://img.shields.io/badge/platform-Windows-0078d6) ![Python](https://img.shields.io/badge/python-3.10%2B-yellow)

Versión actual: <!-- version -->V1.2.0<!-- /version -->

Aplicación de Windows que **busca todos los procesos de OneDrive, los termina y vuelve a iniciar OneDrive** cada vez que se abre. Pensada para cuando OneDrive deja de responder.

## Funcionalidades
- Reinicio automático al iniciar la app (desactivable con `--no-auto`).
- Casilla **Reiniciar OneDrive al abrir** para activar o desactivar la automatización al iniciar.
- **Cierre automático** con cuenta regresiva configurable tras reiniciar OneDrive (se cancela desmarcando la casilla o pulsando Reiniciar).
- Botón para repetir el reinicio, registro de actividad y barra de progreso.
- Multi-idioma: Español, English, Português, Français (se recuerda la elección).
- Botón "🍺 Cómprame una cerveza" ([PayPal](https://www.paypal.com/donate/?hosted_button_id=ZABFRXC2P3JQN)).
- Sin dependencias en ejecución (solo biblioteca estándar de Python).

## Uso rápido
Descarga `OneDriveResetter.exe` desde [Releases](https://github.com/erickson558/onedriverresetter/releases) y ejecútalo. No requiere instalación ni permisos de administrador.

## Requisitos (desarrollo)
- Windows 10/11 y Python 3.10+ (con tkinter).
- `requirements.txt`: solo `pyinstaller` (para compilar).

## Ejecutar desde código
```powershell
python onedriverresetter.py            # reinicia OneDrive al abrir
python onedriverresetter.py --no-auto  # solo abre la ventana
python -m unittest discover -s tests -v
```

## Configuración
Se guarda en `config.json` junto al .exe (idioma, reinicio al abrir, cierre automático y segundos).

## Compilar el .exe
```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```
Genera `OneDriveResetter.exe` en la misma carpeta que el `.py`, con `icon.ico` y sin consola.

## Versionado (Vx.x.x)
`version.py` es la única fuente de verdad. Con cada cambio relevante:
```powershell
python scripts/bump_version.py patch   # o minor / major
```
- **major**: cambios incompatibles · **minor**: funcionalidad nueva · **patch**: correcciones/docs.
- Actualizar `CHANGELOG.md`, hacer commit y push a `main`: el workflow crea el tag `Vx.x.x` y el Release con el `.exe`.

## Estructura
```
onedriverresetter.py     App (lógica + GUI), comentada
i18n.py                  Traducciones
version.py               Versión única
build.ps1                Compilación a .exe
scripts/bump_version.py  Subida de versión
tests/                   Pruebas unitarias
specs/                   Spec-Driven Development (constitución, spec, plan, tasks)
.claude/                 Agentes y skills del proyecto
.github/workflows/       Release automático
```

## Seguridad
Ver [SECURITY.md](SECURITY.md).

## Licencia
[Apache License 2.0](LICENSE)
