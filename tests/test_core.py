"""Pruebas de la lógica sin GUI ni procesos reales (todo con mocks)."""

import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import i18n  # noqa: E402
import onedriverresetter as app  # noqa: E402
from version import __version__  # noqa: E402


class FakeRun:
    """Imita subprocess.run().stdout de tasklist."""

    def __init__(self, stdout="", returncode=0):
        self.stdout = stdout
        self.returncode = returncode


class ProcessListTests(unittest.TestCase):
    def test_lists_only_onedrive_and_never_self(self):
        csv_out = (
            '"OneDrive.exe","1234","Console","1","50,000 K"\n'
            '"FileCoAuth.exe","2222","Console","1","10,000 K"\n'
            '"OneDriveResetter.exe","3333","Console","1","20,000 K"\n'
            '"notepad.exe","4444","Console","1","5,000 K"\n'
        )
        with mock.patch.object(app.subprocess, "run", return_value=FakeRun(csv_out)):
            procs = app.list_onedrive_processes()
        self.assertEqual(procs, [("OneDrive.exe", 1234), ("FileCoAuth.exe", 2222)])

    def test_kill_process_uses_no_shell(self):
        with mock.patch.object(app.subprocess, "run", return_value=FakeRun(returncode=0)) as run:
            self.assertTrue(app.kill_process(99))
        args, kwargs = run.call_args
        self.assertIsInstance(args[0], list)
        self.assertNotIn("shell", kwargs)


class ResetFlowTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "flujo exclusivo de Windows")
    def test_reports_missing_exe(self):
        events = []
        with mock.patch.object(app, "list_onedrive_processes", return_value=[]), \
                mock.patch.object(app, "find_onedrive_exe", return_value=None):
            ok = app.reset_onedrive(lambda k, **d: events.append(k))
        self.assertFalse(ok)
        self.assertIn("log_exe_missing", events)


class SettingsTests(unittest.TestCase):
    def test_invalid_settings_fall_back_to_defaults(self):
        bad = '{"language": "zz", "auto_close": "yes", "close_seconds": 99999}'
        with mock.patch("builtins.open", mock.mock_open(read_data=bad)):
            self.assertEqual(app.load_settings(), app.DEFAULT_SETTINGS)

    def test_valid_settings_are_loaded(self):
        good = '{"language": "es", "auto_close": false, "close_seconds": 20}'
        with mock.patch("builtins.open", mock.mock_open(read_data=good)):
            cfg = app.load_settings()
        self.assertEqual((cfg["language"], cfg["auto_close"], cfg["close_seconds"]), ("es", False, 20))


class I18nTests(unittest.TestCase):
    def test_all_languages_have_all_keys(self):
        base = set(i18n.TRANSLATIONS["en"])
        for code in i18n.LANGUAGES:
            self.assertEqual(base, set(i18n.TRANSLATIONS[code]), code)

    def test_fallback_and_format(self):
        self.assertEqual(i18n.t("xx", "log_found", name="a", pid=1), "Found a (PID 1)")

    def test_version_format(self):
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(p.isdigit() for p in parts))


if __name__ == "__main__":
    unittest.main()
