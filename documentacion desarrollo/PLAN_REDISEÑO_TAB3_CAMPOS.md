# Plan de Rediseño — Tab 3: Mis Campos

## Patrones establecidos en Tab 2 (aplicar consistentemente)

### Look & Feel
- **Glassmorphism**: containers `rgba(255,255,255,0.04)` + `1px solid rgba(255,255,255,0.08)` + `border-radius: 14px`
- **KPI cards**: flat + `border-top: 2px solid [accent-color]` + valor `2-2.6em font-weight 900` sin text-shadow
- **Labels**: `9px uppercase letter-spacing 1.5px color #9a9e94 font-weight 700`
- **Inner boxes**: `rgba(255,255,255,0.03)` + `border-left: 3px solid [accent]`
- **Conclusiones AI**: `"Conclusión:"` en azul `#4A9FD8`, sin emoji robot, sin texto "IA", fondo `rgba(74,159,216,0.06)` + borde `rgba(74,159,216,0.18)`

### Quick Menu
- Sin emojis, solo bullet point `•` + texto
- Todas las secciones representadas en orden exacto del dashboard
- Grid `repeat(auto-fill, minmax(280px, 1fr))`, items con fondo `rgba(255,255,255,0.03)`

---

## 0. Refactoring CSS — Paso previo (ejecutar ANTES del rediseño)

> Este paso se ejecuta una sola vez y beneficia a los 4 tabs (3, 4, 5, 6).
> Ya existe Card System v3.1 con tokens y clases CSS (líneas ~4835-4959) pero apenas se usa.
> El objetivo es crear las clases utilitarias que faltan y luego migrar inline styles → clases.

### Auditoría de inline styles repetidos

| Patrón | Ocurrencias | Token/Clase existente | Acción |
|--------|-------------|----------------------|--------|
| `rgba(255,255,255,0.03)` (inner boxes) | **58** | `--card-bg-4` | Usar `.card-nested` o crear `.bg-inner` |
| `rgba(255,255,255,0.08)` (borders) | **42** | ❌ falta token | Añadir `--card-border-md: rgba(255,255,255,0.08)` |
| `rgba(255,255,255,0.04)` (containers) | **37** | `--card-bg-3` | Usar `.card-detail` existente |
| `border-top: 2px solid [color]` (KPI) | **23** | `.accent-*` parcial | Crear `.kpi-card` + `.kpi-card--blue/green/gold/red` |
| Label pattern (9px/uppercase/#9a9e94) | **20** | ❌ no existe | Crear `.text-label` |
| Quick-nav inline (style largo) | **13+** por tab | ❌ no existe | Crear `.quick-nav-link` |
| AI conclusion pattern | **2** (crecerá) | ❌ no existe | Crear `.ai-conclusion` |

### Nuevas clases CSS a crear (~6 clases)

```css
/* --- Utility Classes (añadir al bloque <style>) --- */

/* Labels uppercase minimalistas */
.text-label {
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #9a9e94;
    font-weight: 700;
    margin-bottom: 10px;
}

/* KPI card base (glassmorphism flat) */
.kpi-card {
    background: rgba(255,255,255,0.04);
    padding: 22px 18px;
    border-radius: 8px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}
.kpi-card--blue  { border-top: 2px solid #4A9FD8; }
.kpi-card--green { border-top: 2px solid #5ABF8F; }
.kpi-card--gold  { border-top: 2px solid #D4B55A; }
.kpi-card--red   { border-top: 2px solid #E88B7A; }

/* KPI value (número grande) */
.kpi-value {
    font-size: 2em;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 6px;
}

/* KPI subtitle */
.kpi-sub {
    font-size: 0.82em;
    color: #9a9e94;
}

/* Quick nav link */
.quick-nav-link {
    color: rgba(255,255,255,0.75);
    text-decoration: none;
    padding: 10px 14px;
    border-radius: 8px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    transition: all 0.2s ease;
    display: block;
    font-size: 0.88em;
}
.quick-nav-link:hover {
    background: rgba(255,255,255,0.06);
    color: rgba(255,255,255,0.95);
}

/* AI Conclusion box */
.ai-conclusion {
    margin-top: 14px;
    padding: 18px;
    background: rgba(74,159,216,0.06);
    border-radius: 10px;
    border: 1px solid rgba(74,159,216,0.18);
}

/* Inner box with accent left border */
.inner-box {
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 14px 16px;
}
.inner-box--blue  { border-left: 3px solid #4A9FD8; }
.inner-box--green { border-left: 3px solid #5ABF8F; }
.inner-box--gold  { border-left: 3px solid #D4B55A; }
.inner-box--red   { border-left: 3px solid #E88B7A; }
```

### Token CSS faltante

```css
:root {
    --card-border-md: rgba(255,255,255, 0.08);  /* añadir junto a los existentes */
}
```

### Plan de migración

1. **Añadir clases y token** al bloque `<style>` (~30 líneas nuevas)
2. **Migrar Tab 2** primero (ya rediseñada, es el test case)
   - Quick menu: 13 `<a style="...">` → `<a class="quick-nav-link">`
   - KPI cards: 4 cards en score-history → `class="kpi-card kpi-card--blue"`
   - Labels: `<div style="font-size: 9px...">` → `<div class="text-label">`
   - AI conclusions: 2 inline divs → `<div class="ai-conclusion">`
3. **Aplicar en Tab 3** como parte del rediseño (este plan)
4. **Tabs 4, 5, 6** usan las mismas clases en sus respectivos rediseños

### Impacto estimado
- ~280-300 inline styles eliminados en total (across all tabs)
- ~200-250 líneas HTML reducidas
- Rediseños Tab 3-6 se hacen cambiando clases, no copiando inline styles

---

## 1. Auditoría de Quick Menu

### Estado actual (9 items, 9 secciones) — ✅ Cobertura 100%

| # | Quick Menu Item | Target ID | Sección H2 (línea) |
|---|----------------|-----------|---------------------|
| 1 | Mi Trayectoria RFEG | `trayectoria-rfeg` | 📊 Mi Trayectoria RFEG (6730) |
| 2 | Performance por Campo | `performance-campo` | 🏌️ Performance por Campo (6780) |
| 3 | Mis Mejores Rondas | `mejores-rondas` | 🏆 Mis Mejores Rondas (6840) |
| 4 | Análisis de Scoring | `analisis-scoring` | 📊 Análisis de Scoring (6908) |
| 5 | Análisis de Consistencia | `analisis-consistencia` | 🎲 Análisis de Consistencia (6954) |
| 6 | Estado de Forma | `estado-forma` | 📈 Estado de Forma (7037) |
| 7 | Proyección de Rendimiento | `proyeccion-rendimiento` | ⚔️ Proyección de Rendimiento (7079) |
| 8 | Objetivos y Logros | `objetivos-logros` | 🏆 Objetivos y Logros (7160) |
| 9 | Optimización de Práctica | `optimizacion-practica` | 🎓 Optimización de Práctica (7331) |

### Acción requerida
- [ ] Verificar que el orden del quick menu coincide con el orden en el dashboard
- [ ] Quitar emojis del quick menu (si los tiene) → solo `•` + texto
- [ ] Migrar inline styles a `.quick-nav-link` (del Paso 0)

---

## 2. Glassmorphism — Secciones a rediseñar

Revisar cada sección y migrar de gradients/shadows al patrón glassmorphism usando las clases CSS del Paso 0:

- [ ] **Trayectoria RFEG** — KPI cards → `.kpi-card` + `.text-label`
- [ ] **Performance por Campo** — Cards por campo → `.card-detail` + `.accent-*`
- [ ] **Mejores Rondas** — Container (cs-best-rounds-container) → `.card-detail`
- [ ] **Análisis de Scoring** — KPI cards → `.kpi-card`
- [ ] **Análisis de Consistencia** — KPI cards → `.kpi-card`
- [ ] **Estado de Forma** — Indicadores → `.kpi-card` + `.inner-box`
- [ ] **Proyección de Rendimiento** — Cards → `.card-detail`
- [ ] **Objetivos y Logros** — Progress bars (cs-goals-container)
- [ ] **Optimización de Práctica** — Cards → `.card-detail`

### Patrón de migración por sección
1. Identificar inline styles que matchean las nuevas clases
2. Reemplazar `style="..."` por `class="kpi-card kpi-card--blue"` etc.
3. Mantener styles únicos (sizing, grid layouts) como inline
4. Verificar visual idéntico después de migración

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas para conclusión AI
- [ ] **Performance por Campo** — Conclusión sobre qué campos favorecen el juego y por qué
- [ ] **Análisis de Scoring** — Conclusión sobre patrones de scoring

### Implementación
1. Añadir keys al skill prompt de UXWriter: `campo_conclusion`, `scoring_analysis_conclusion`
2. Añadir anchors HTML: `<div id="ai-campo-conclusion"></div>`, `<div id="ai-scoring-conclusion"></div>`
3. Inyección JS usa `class="ai-conclusion"` (del Paso 0) en vez de inline style
4. Añadir `course_statistics` y `campo_performance` al `_compact()` (ya están)

---

## 4. Checklist final

- [ ] Paso 0: Clases CSS añadidas y Tab 2 migrada como test
- [ ] Quick menu: todas las secciones, orden correcto, sin emojis, usando `.quick-nav-link`
- [ ] Glassmorphism aplicado usando clases CSS (no inline)
- [ ] Conclusiones AI inyectadas con `.ai-conclusion`
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Gráficos resize correctamente al cambiar de tab
