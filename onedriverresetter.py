"""OneDrive Resetter: al iniciar, detecta los procesos de OneDrive, los termina y
vuelve a iniciar OneDrive. Útil cuando OneDrive deja de responder.

Secciones del archivo:
1. Constantes y configuración
2. Lógica de procesos (listar, terminar, esperar, reiniciar)  -> sin GUI, testeable
3. Persistencia del idioma elegido
4. Interfaz gráfica (tkinter)
5. Punto de entrada

Seguridad: no se usa shell=True, los ejecutables se invocan con rutas absolutas
de Windows y listas de argumentos fijas; nunca se interpola texto externo en
un comando.
"""

import csv
import io
import json
import os
import queue
import subprocess
import sys
import threading
import time
import webbrowser
import tkinter as tk
from tkinter import ttk

from i18n import LANGUAGES, detect_language, t
from version import __version__

# ---------------------------------------------------------------------------
# 1. Constantes y configuración
# ---------------------------------------------------------------------------

# Enlace del botón "Cómprame una cerveza".
DONATE_URL = "https://www.paypal.com/donate/?hosted_button_id=ZABFRXC2P3JQN"

# Nombres EXACTOS (minúsculas) de procesos de OneDrive a terminar. Se usan
# nombres exactos y no "contiene onedrive" para no matar esta misma app
# (OneDriveResetter.exe).
ONEDRIVE_PROCESS_NAMES = {
    "onedrive.exe",
    "onedrive.sync.service.exe",
    "onedrivestandaloneupdater.exe",
    "filecoauth.exe",
    "filesynchelper.exe",
}

# Flags de Windows: ocultar la ventana de consola de los subprocesos y lanzar
# OneDrive desacoplado de esta app (sobrevive si se cierra el reiniciador).
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
DETACHED_FLAGS = 0x00000008 | 0x00000200 if os.name == "nt" else 0  # DETACHED_PROCESS | NEW_PROCESS_GROUP

WAIT_STOP_SECONDS = 15   # tiempo máximo esperando a que mueran los procesos
WAIT_START_SECONDS = 10  # tiempo máximo esperando a que OneDrive reaparezca


def _system32(exe):
    """Ruta absoluta a un ejecutable de System32 (evita secuestro por PATH)."""
    return os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", exe)


# ---------------------------------------------------------------------------
# 2. Lógica de procesos
# ---------------------------------------------------------------------------

def list_onedrive_processes():
    """Devuelve [(nombre, pid), ...] de los procesos de OneDrive activos."""
    out = subprocess.run(
        [_system32("tasklist.exe"), "/FO", "CSV", "/NH"],
        capture_output=True, text=True, errors="replace",
        creationflags=CREATE_NO_WINDOW, timeout=30, check=False,
    ).stdout
    found = []
    for row in csv.reader(io.StringIO(out)):
        # Formato CSV de tasklist: "nombre","pid","sesión","#","memoria"
        if len(row) >= 2 and row[0].lower() in ONEDRIVE_PROCESS_NAMES and row[1].isdigit():
            pid = int(row[1])
            if pid != os.getpid():
                found.append((row[0], pid))
    return found


def kill_process(pid):
    """Termina un proceso (y sus hijos) por PID. True si taskkill tuvo éxito."""
    result = subprocess.run(
        [_system32("taskkill.exe"), "/F", "/T", "/PID", str(int(pid))],
        capture_output=True, creationflags=CREATE_NO_WINDOW, timeout=30, check=False,
    )
    return result.returncode == 0


def find_onedrive_exe():
    """Busca OneDrive.exe en las ubicaciones estándar. None si no existe."""
    candidates = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "OneDrive", "OneDrive.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Microsoft OneDrive", "OneDrive.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Microsoft OneDrive", "OneDrive.exe"),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "SysWOW64", "OneDriveSetup.exe"),
    ]
    for path in candidates:
        if path and os.path.isfile(path) and os.path.basename(path).lower() == "onedrive.exe":
            return path
    return None


def reset_onedrive(emit):
    """Ejecuta el ciclo completo: detectar -> terminar -> esperar -> reiniciar.

    `emit(clave, **datos)` informa el progreso con claves de i18n; así la
    lógica no depende del idioma ni de la GUI. Devuelve True si OneDrive quedó
    corriendo.
    """
    if os.name != "nt":
        emit("log_not_windows")
        return False

    # Paso 1: detectar procesos.
    emit("log_scanning")
    procs = list_onedrive_processes()
    if not procs:
        emit("log_none")
    for name, pid in procs:
        emit("log_found", name=name, pid=pid)

    # Paso 2: terminar cada proceso.
    for name, pid in procs:
        emit("log_killing", name=name, pid=pid)
        if not kill_process(pid):
            emit("log_kill_failed", name=name, pid=pid)

    # Paso 3: esperar a que desaparezcan todos.
    deadline = time.time() + WAIT_STOP_SECONDS
    remaining = list_onedrive_processes()
    while remaining and time.time() < deadline:
        time.sleep(0.5)
        remaining = list_onedrive_processes()
    if remaining:
        emit("log_still_running", count=len(remaining))
    else:
        emit("log_all_stopped")

    # Paso 4: reiniciar OneDrive en segundo plano.
    exe = find_onedrive_exe()
    if not exe:
        emit("log_exe_missing")
        return False
    emit("log_starting", path=exe)
    try:
        subprocess.Popen(
            [exe, "/background"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=DETACHED_FLAGS, close_fds=True,
        )
    except OSError as exc:
        emit("log_start_failed", error=str(exc))
        return False

    # Paso 5: verificar que el proceso reapareció.
    deadline = time.time() + WAIT_START_SECONDS
    while time.time() < deadline:
        if any(n.lower() == "onedrive.exe" for n, _ in list_onedrive_processes()):
            emit("log_started_ok")
            return True
        time.sleep(0.5)
    emit("log_start_failed", error="timeout")
    return False


# ---------------------------------------------------------------------------
# 3. Persistencia del idioma
# ---------------------------------------------------------------------------

def _config_path():
    """%APPDATA%\\OneDriveResetter\\config.json (o carpeta home si no hay APPDATA)."""
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, "OneDriveResetter", "config.json")


def load_language():
    """Lee el idioma guardado; si no hay o es inválido, detecta el del sistema."""
    try:
        with open(_config_path(), encoding="utf-8") as fh:
            lang = json.load(fh).get("language")
        if lang in LANGUAGES:
            return lang
    except (OSError, ValueError, AttributeError):
        pass
    return detect_language()


def save_language(lang):
    """Guarda el idioma elegido. Los errores de disco se ignoran (no es crítico)."""
    try:
        path = _config_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"language": lang}, fh)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# 4. Interfaz gráfica
# ---------------------------------------------------------------------------

class App(tk.Tk):
    """Ventana principal: botón de reinicio, selector de idioma, registro y donación."""

    def __init__(self, auto_run=True):
        super().__init__()
        self.lang = load_language()
        self.events = queue.Queue()   # el hilo de trabajo deja aquí sus mensajes
        self.log_entries = []         # (clave, datos) para re-traducir al cambiar idioma
        self.status_key = "status_idle"
        self.running = False

        self.geometry("560x380")
        self.minsize(460, 320)
        icon = os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), "icon.ico")
        if os.path.isfile(icon):
            try:
                self.iconbitmap(icon)
            except tk.TclError:
                pass

        self._build_widgets()
        self._apply_texts()
        self.after(100, self._poll_events)
        if auto_run:
            # Reinicio automático al abrir la app (requisito principal).
            self.after(300, self.start_reset)

    def _build_widgets(self):
        """Crea los widgets una sola vez; los textos se asignan en _apply_texts."""
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        self.btn_reset = ttk.Button(top, command=self.start_reset)
        self.btn_reset.pack(side="left")
        self.btn_beer = ttk.Button(top, command=lambda: webbrowser.open(DONATE_URL))
        self.btn_beer.pack(side="left", padx=8)

        # Selector de idioma alineado a la derecha.
        self.lang_label = ttk.Label(top)
        self.lang_label.pack(side="right")
        self.lang_box = ttk.Combobox(top, state="readonly", width=11, values=list(LANGUAGES.values()))
        self.lang_box.set(LANGUAGES[self.lang])
        self.lang_box.pack(side="right", padx=(0, 6))
        self.lang_box.bind("<<ComboboxSelected>>", self._on_language_change)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=10)

        self.log = tk.Text(self, height=10, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=10, pady=8)

        bottom = ttk.Frame(self, padding=(10, 0, 10, 8))
        bottom.pack(fill="x")
        self.status_label = ttk.Label(bottom)
        self.status_label.pack(side="left")
        self.version_label = ttk.Label(bottom)
        self.version_label.pack(side="right")

    def _apply_texts(self):
        """Aplica el idioma actual a todos los textos y re-dibuja el registro."""
        self.title(t(self.lang, "window_title"))
        self.btn_reset.config(text=t(self.lang, "btn_reset"))
        self.btn_beer.config(text=t(self.lang, "btn_beer"))
        self.lang_label.config(text=t(self.lang, "lang_label"))
        self.status_label.config(text=t(self.lang, self.status_key))
        self.version_label.config(text=f"{t(self.lang, 'version_label')} V{__version__}")
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        for key, data in self.log_entries:
            self.log.insert("end", t(self.lang, key, **data) + "\n")
        self.log.config(state="disabled")
        self.log.see("end")

    def _on_language_change(self, _event):
        """Cambia el idioma al elegir otro en el combo y lo guarda."""
        names = {name: code for code, name in LANGUAGES.items()}
        self.lang = names.get(self.lang_box.get(), self.lang)
        save_language(self.lang)
        self._apply_texts()

    def start_reset(self):
        """Lanza el reinicio en un hilo aparte para no congelar la ventana."""
        if self.running:
            return
        self.running = True
        self.status_key = "status_running"
        self.btn_reset.config(state="disabled")
        self.progress.start(12)
        self._apply_texts()
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        """Hilo de trabajo: ejecuta la lógica y reporta por la cola."""
        ok = False
        try:
            ok = reset_onedrive(lambda key, **data: self.events.put(("log", key, data)))
        except Exception as exc:  # cualquier fallo inesperado se muestra, no se pierde
            self.events.put(("log", "log_start_failed", {"error": str(exc)}))
        self.events.put(("done", ok, None))

    def _poll_events(self):
        """Corre en el hilo de la GUI: vacía la cola y actualiza la pantalla."""
        try:
            while True:
                kind, a, b = self.events.get_nowait()
                if kind == "log":
                    self.log_entries.append((a, b))
                    self.log.config(state="normal")
                    self.log.insert("end", t(self.lang, a, **b) + "\n")
                    self.log.config(state="disabled")
                    self.log.see("end")
                else:  # "done"
                    self.running = False
                    self.progress.stop()
                    self.btn_reset.config(state="normal")
                    self.status_key = "status_ok" if a else "status_error"
                    self.log_entries.append(("log_done", {}))
                    self._apply_texts()
        except queue.Empty:
            pass
        self.after(100, self._poll_events)


# ---------------------------------------------------------------------------
# 5. Punto de entrada
# ---------------------------------------------------------------------------

def main():
    """Abre la GUI. Con --no-auto no reinicia OneDrive al abrir (solo con el botón)."""
    App(auto_run="--no-auto" not in sys.argv).mainloop()


if __name__ == "__main__":
    main()
