import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('README.md', encoding='utf-16') as f:
    content = f.read()

# 1. Update header version and date
content = content.replace(
    '**Version:** v3.0.1 - Multi-Agent System + UXWriter Dashboard Integration\n**Estado:** Production Ready\n**Ultima actualizacion:** 2026-02-17',
    '**Version:** v3.0.3 - Static AI Cache + UXWriter 6-Section Fix\n**Estado:** Production Ready\n**Ultima actualizacion:** 2026-02-22'
)

# 2. Update agentic badge
content = content.replace(
    'badge/Agentic-v3.0.1%20UXWriter%20Integrated-purple',
    'badge/Agentic-v3.0.3%20AI%20Cache-purple'
)

# 3. Insert new What's New section before v3.0.1
NEW_SECTION = """## What's New in v3.0.3 (2026-02-22)

### Static AI Content Cache - Dashboard AI Content Instantaneo

**Problema resuelto:** El dashboard tardaba ~70s en mostrar contenido AI (llamada al backend en vivo).
**Solucion:** Pre-generar `output/ai_content.json` y servirlo como fichero estatico.
**Impacto:** AI content carga en <100ms desde fichero, en lugar de ~70s desde backend.

**Cambios tecnicos:**
- `app/agents/ux_writer.py`: Skill prompt reducido a solo las 4 secciones requeridas.
  Se eliminaron las descripciones detalladas de stat_cards, trend_narratives, course_cards
  y club_cards, que rellenaban el budget de tokens antes de generar insight_boxes/quick_wins/roi_cards
- `app/agents/ux_writer.py`: Fix UnicodeEncodeError en Windows (caracter U+2192 sustituido por ASCII ->)
- `app/main.py`: `/generate-content` ahora auto-guarda `output/ai_content.json` tras cada llamada
- `app/agents/orchestrator.py`: `/analyze` tambien guarda ai_content.json al finalizar el workflow
- `dashboard_dynamic.html`: `loadUXContent()` carga ai_content.json como primera fuente (prioridad 1)
- `output/ai_content.json`: Fichero pre-generado commiteado (6 secciones, 7116 chars, JSON valido)
- `.claude/settings.local.json`: Hook py_compile en Stop event (validacion sintaxis automatica)

**Orden de carga AI content en dashboard (cascada):**
1. `output/ai_content.json` (instantaneo, <100ms) **← NUEVO - primera prioridad**
2. localStorage cache (TTL 24h)
3. Backend `/generate-content` en vivo (~70s)
4. Degradacion graceful sin backend

---

"""

insert_pos = content.find("## What's New in v3.0.1")
if insert_pos >= 0:
    content = content[:insert_pos] + NEW_SECTION + content[insert_pos:]
    print("Inserted new section OK")
else:
    print("WARNING: Could not find insert position")

# 4. Update bottom version references
OLD_BOTTOM = '**Ultima actualizacion:** 17 de febrero de 2026\n**Estado:** Production Ready\n**Version:** v3.0.1 - Multi-Agent System + UXWriter Dashboard Integration\n**Proximo Milestone:** Optimizacion frontend (carga <10 segundos)'
NEW_BOTTOM = '**Ultima actualizacion:** 22 de febrero de 2026\n**Estado:** Production Ready\n**Version:** v3.0.3 - Static AI Cache + UXWriter 6-Section Fix\n**Proximo Milestone:** Ampliar datos (mas rondas 2026) + mejoras UX movil'
if OLD_BOTTOM in content:
    content = content.replace(OLD_BOTTOM, NEW_BOTTOM)
    print("Updated bottom footer OK")
else:
    print("WARNING: Bottom footer not found, skipping")

# Write back UTF-16
with open('README.md', 'w', encoding='utf-16') as f:
    f.write(content)

print('README.md updated and saved OK')
print('New length:', len(content), 'chars')
