"""Soporte multi-idioma (i18n) de OneDrive Resetter.

Cada idioma es un diccionario clave -> texto. Para añadir un idioma:
1. Agregar su código y nombre en LANGUAGES.
2. Agregar su diccionario en TRANSLATIONS con TODAS las claves de "en".
(tests/test_i18n.py verifica que ningún idioma tenga claves faltantes.)
"""

import locale

# Código de idioma -> nombre que se muestra en el selector de la GUI.
LANGUAGES = {
    "es": "Español",
    "en": "English",
    "pt": "Português",
    "fr": "Français",
}

DEFAULT_LANGUAGE = "en"

# Textos de la interfaz y del registro de actividad. Los {marcadores}
# se rellenan con str.format() en t().
TRANSLATIONS = {
    "en": {
        "window_title": "OneDrive Resetter",
        "btn_reset": "Restart OneDrive",
        "btn_beer": "🍺 Buy me a beer",
        "lang_label": "Language:",
        "version_label": "Version",
        "status_idle": "Ready",
        "status_running": "Restarting OneDrive...",
        "status_ok": "OneDrive restarted successfully",
        "status_error": "Could not restart OneDrive (see log)",
        "log_not_windows": "This tool only works on Windows.",
        "log_scanning": "Looking for OneDrive processes...",
        "log_found": "Found {name} (PID {pid})",
        "log_none": "No OneDrive processes were running.",
        "log_killing": "Terminating {name} (PID {pid})...",
        "log_kill_failed": "Could not terminate {name} (PID {pid}).",
        "log_still_running": "{count} process(es) still running after waiting.",
        "log_all_stopped": "All OneDrive processes are stopped.",
        "log_exe_missing": "OneDrive.exe was not found on this PC.",
        "log_starting": "Starting OneDrive: {path}",
        "log_started_ok": "OneDrive is running again.",
        "log_start_failed": "Failed to start OneDrive: {error}",
        "log_done": "Done.",
    },
    "es": {
        "window_title": "Reiniciador de OneDrive",
        "btn_reset": "Reiniciar OneDrive",
        "btn_beer": "🍺 Cómprame una cerveza",
        "lang_label": "Idioma:",
        "version_label": "Versión",
        "status_idle": "Listo",
        "status_running": "Reiniciando OneDrive...",
        "status_ok": "OneDrive se reinició correctamente",
        "status_error": "No se pudo reiniciar OneDrive (revisa el registro)",
        "log_not_windows": "Esta herramienta solo funciona en Windows.",
        "log_scanning": "Buscando procesos de OneDrive...",
        "log_found": "Encontrado {name} (PID {pid})",
        "log_none": "No había procesos de OneDrive en ejecución.",
        "log_killing": "Terminando {name} (PID {pid})...",
        "log_kill_failed": "No se pudo terminar {name} (PID {pid}).",
        "log_still_running": "Siguen {count} proceso(s) activos tras esperar.",
        "log_all_stopped": "Todos los procesos de OneDrive están detenidos.",
        "log_exe_missing": "No se encontró OneDrive.exe en este equipo.",
        "log_starting": "Iniciando OneDrive: {path}",
        "log_started_ok": "OneDrive está en ejecución nuevamente.",
        "log_start_failed": "Error al iniciar OneDrive: {error}",
        "log_done": "Listo.",
    },
    "pt": {
        "window_title": "Reiniciador do OneDrive",
        "btn_reset": "Reiniciar OneDrive",
        "btn_beer": "🍺 Pague-me uma cerveja",
        "lang_label": "Idioma:",
        "version_label": "Versão",
        "status_idle": "Pronto",
        "status_running": "Reiniciando o OneDrive...",
        "status_ok": "OneDrive reiniciado com sucesso",
        "status_error": "Não foi possível reiniciar o OneDrive (veja o registro)",
        "log_not_windows": "Esta ferramenta só funciona no Windows.",
        "log_scanning": "Procurando processos do OneDrive...",
        "log_found": "Encontrado {name} (PID {pid})",
        "log_none": "Nenhum processo do OneDrive estava em execução.",
        "log_killing": "Encerrando {name} (PID {pid})...",
        "log_kill_failed": "Não foi possível encerrar {name} (PID {pid}).",
        "log_still_running": "{count} processo(s) ainda ativos após a espera.",
        "log_all_stopped": "Todos os processos do OneDrive foram encerrados.",
        "log_exe_missing": "OneDrive.exe não foi encontrado neste computador.",
        "log_starting": "Iniciando o OneDrive: {path}",
        "log_started_ok": "O OneDrive está em execução novamente.",
        "log_start_failed": "Falha ao iniciar o OneDrive: {error}",
        "log_done": "Concluído.",
    },
    "fr": {
        "window_title": "Redémarrage de OneDrive",
        "btn_reset": "Redémarrer OneDrive",
        "btn_beer": "🍺 Offrez-moi une bière",
        "lang_label": "Langue :",
        "version_label": "Version",
        "status_idle": "Prêt",
        "status_running": "Redémarrage de OneDrive...",
        "status_ok": "OneDrive a redémarré avec succès",
        "status_error": "Impossible de redémarrer OneDrive (voir le journal)",
        "log_not_windows": "Cet outil fonctionne uniquement sous Windows.",
        "log_scanning": "Recherche des processus OneDrive...",
        "log_found": "Trouvé {name} (PID {pid})",
        "log_none": "Aucun processus OneDrive n'était en cours d'exécution.",
        "log_killing": "Arrêt de {name} (PID {pid})...",
        "log_kill_failed": "Impossible d'arrêter {name} (PID {pid}).",
        "log_still_running": "{count} processus toujours actif(s) après l'attente.",
        "log_all_stopped": "Tous les processus OneDrive sont arrêtés.",
        "log_exe_missing": "OneDrive.exe est introuvable sur cet ordinateur.",
        "log_starting": "Démarrage de OneDrive : {path}",
        "log_started_ok": "OneDrive est de nouveau en cours d'exécution.",
        "log_start_failed": "Échec du démarrage de OneDrive : {error}",
        "log_done": "Terminé.",
    },
}


def detect_language():
    """Devuelve el código de idioma del sistema si está soportado, si no el por defecto."""
    try:
        code = (locale.getlocale()[0] or "").split("_")[0].lower()
    except (ValueError, TypeError):
        code = ""
    # Windows a veces devuelve nombres largos ("Spanish_Mexico"); se mapean los comunes.
    long_names = {"spanish": "es", "english": "en", "portuguese": "pt", "french": "fr"}
    code = long_names.get(code, code)
    return code if code in TRANSLATIONS else DEFAULT_LANGUAGE


def t(lang, key, **kwargs):
    """Traduce `key` al idioma `lang` (con respaldo a inglés) y aplica format(**kwargs)."""
    text = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE]).get(
        key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
    )
    try:
        return text.format(**kwargs)
    except (KeyError, IndexError):
        return text
