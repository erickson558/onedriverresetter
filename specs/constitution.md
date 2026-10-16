# Constitución del proyecto (SDD)

Principios no negociables. Todo cambio debe respetarlos.

1. **Spec primero**: ningún comportamiento nuevo se implementa sin actualizar antes `specs/<feature>/spec.md`, `plan.md` y `tasks.md`.
2. **Cero dependencias en runtime**: la app solo usa la biblioteca estándar. PyInstaller es solo de build y va fijado en `requirements.txt`.
3. **Seguridad**: sin `shell=True`, sin interpolar texto externo en comandos, rutas absolutas a binarios de System32, nombres de proceso por lista exacta (nunca "contiene").
4. **Versión única**: `version.py` es la fuente de verdad; se sube con `scripts/bump_version.py` y se refleja en GUI, README, tag `Vx.x.x` y Release.
5. **Código comentado**: cada módulo, función y bloque no trivial explica qué hace.
6. **i18n completo**: todo texto visible va por `i18n.t()`; todos los idiomas tienen las mismas claves (lo valida `tests/test_core.py`).
7. **Cada cambio relevante = versión nueva + CHANGELOG + commit convencional + push a main.**
