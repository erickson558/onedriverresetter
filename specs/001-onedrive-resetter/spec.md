# Spec 001 — OneDrive Resetter

## Problema
OneDrive deja de responder con frecuencia. Reiniciarlo a mano (matar procesos y relanzar) es tedioso.

## Historias de usuario
- **US1**: Al abrir la app, se buscan todos los procesos de OneDrive, se terminan y se reinicia OneDrive automáticamente.
- **US2**: Puedo repetir el reinicio con un botón.
- **US3**: Veo un registro de lo que ocurre y el estado final (éxito/error).
- **US4**: Puedo elegir idioma (es, en, pt, fr); se recuerda entre sesiones.
- **US5**: Hay un botón "Cómprame una cerveza" que abre el enlace de PayPal.
- **US6**: Veo la versión Vx.x.x en la ventana.

## Requisitos funcionales
- RF1: Procesos objetivo (nombre exacto): OneDrive.exe, OneDrive.Sync.Service.exe, OneDriveStandaloneUpdater.exe, FileCoAuth.exe, FileSyncHelper.exe.
- RF2: Terminar con `taskkill /F /T /PID`; esperar hasta 15 s a que desaparezcan.
- RF3: Relanzar `OneDrive.exe /background` desde LOCALAPPDATA o Program Files; verificar que reaparece (10 s).
- RF4: La GUI nunca se congela (trabajo en hilo + cola).
- RF5: `--no-auto` desactiva el reinicio al abrir.
- RF6: Idioma guardado en `%APPDATA%\OneDriveResetter\config.json`.

## Requisitos no funcionales
- Solo Windows. Sin dependencias en runtime. Ver `specs/constitution.md` (seguridad).
- Distribución: `OneDriveResetter.exe` único, sin consola, con `icon.ico`.

## Criterios de aceptación
- Con OneDrive colgado, abrir la app lo reinicia y la GUI muestra "reiniciado correctamente".
- Sin OneDrive en ejecución, la app igualmente lo inicia.
- Si OneDrive.exe no existe, se informa el error sin romper la app.
- La app nunca termina su propio proceso.
