# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/) · Versionado: [SemVer](https://semver.org/) (`Vx.x.x`).

## V1.1.1 - 2026-10-16
### Changed
- El cierre automático ahora viene desactivado por defecto (se activa con la casilla).

## V1.1.0 - 2026-10-16
### Added
- Casilla "Reiniciar OneDrive al abrir": activa/desactiva la automatización al iniciar la app.
- Cierre automático con cuenta regresiva configurable (3-300 s) tras reiniciar OneDrive con éxito; se cancela al desmarcar la casilla o al reiniciar manualmente.
- Ajustes persistentes en `config.json` (idioma, cierre automático, segundos).

## V1.0.0 - 2026-10-16
### Added
- Detección y terminación de todos los procesos de OneDrive y reinicio automático al abrir la app.
- GUI con botón de reinicio manual, registro de actividad, barra de progreso y estado.
- Soporte multi-idioma: español, inglés, portugués y francés (se recuerda la elección).
- Botón "Cómprame una cerveza" (PayPal).
- Versionado centralizado, build a `.exe` sin consola y workflow de Release automático.
- Documentación, SDD (`specs/`), agentes y skills del proyecto. Licencia Apache 2.0.
