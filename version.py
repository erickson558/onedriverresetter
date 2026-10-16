"""Única fuente de verdad de la versión (formato SemVer, se muestra como Vx.x.x).

Lo leen: la GUI, el script de build, el workflow de GitHub Actions (tag/release)
y scripts/bump_version.py (que es quien lo modifica).
"""

__version__ = "1.2.0"
