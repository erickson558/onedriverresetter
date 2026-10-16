# Política de seguridad

## Versiones soportadas
Solo la última versión publicada en Releases.

## Reportar una vulnerabilidad
Abre un [Security Advisory privado](https://github.com/erickson558/onedriverresetter/security/advisories/new). No publiques detalles en issues públicos.

## Medidas de diseño
- Sin dependencias en runtime (superficie de ataque mínima).
- Sin `shell=True`; argumentos fijos; binarios del sistema por ruta absoluta.
- Procesos objetivo por nombre exacto; la app nunca se termina a sí misma.
- Workflow con permisos mínimos y versión de PyInstaller fijada.
- La configuración local solo guarda el idioma.
