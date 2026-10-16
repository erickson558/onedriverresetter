"""Sube la versión (major | minor | patch) en version.py y en el README.

Uso:  python scripts/bump_version.py patch
Imprime la nueva versión como Vx.x.x. Después: actualizar CHANGELOG.md, commit,
y push a main (el workflow crea el tag y el release).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def bump(current, part):
    """Calcula la versión siguiente según SemVer."""
    major, minor, patch = (int(x) for x in current.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise SystemExit("Uso: bump_version.py [major|minor|patch]")


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else ""
    version_file = ROOT / "version.py"
    text = version_file.read_text(encoding="utf-8")
    current = re.search(r'__version__ = "(\d+\.\d+\.\d+)"', text).group(1)
    new = bump(current, part)

    # version.py: fuente de verdad.
    version_file.write_text(text.replace(f'"{current}"', f'"{new}"'), encoding="utf-8")

    # README: los marcadores <!-- version -->Vx.x.x<!-- /version --> se actualizan.
    readme = ROOT / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        content = re.sub(r"(<!-- version -->)V[\d.]+(<!-- /version -->)", rf"\g<1>V{new}\g<2>", content)
        readme.write_text(content, encoding="utf-8")

    print(f"V{new}")


if __name__ == "__main__":
    main()
