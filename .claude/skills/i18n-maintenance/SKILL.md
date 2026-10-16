---
name: i18n-maintenance
description: Añade o modifica textos/idiomas manteniendo todas las claves sincronizadas en i18n.py.
---

- Todo texto visible usa `t(lang, clave, **datos)`; nunca literales en la GUI.
- Nueva clave: agregarla a **todos** los idiomas de `TRANSLATIONS` (`en` es el respaldo).
- Nuevo idioma: añadir a `LANGUAGES` y `TRANSLATIONS`, y a `long_names` en `detect_language` si aplica.
- Verificar con `python -m unittest discover -s tests` (test_all_languages_have_all_keys).
- Nuevo idioma = cambio **minor** (ver `release-versioning`).
