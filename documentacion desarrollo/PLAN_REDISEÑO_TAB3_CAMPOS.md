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
- [ ] Verificar que el quick menu usa el mismo estilo glassmorphism que Tab 2

---

## 2. Glassmorphism — Secciones a rediseñar

Revisar cada sección y migrar de gradients/shadows al patrón glassmorphism:

- [ ] **Trayectoria RFEG** — KPI cards + gráfico HCP evolution
- [ ] **Performance por Campo** — Cards por campo con stats
- [ ] **Mejores Rondas** — Container de mejores rondas (cs-best-rounds-container)
- [ ] **Análisis de Scoring** — KPI cards de scoring
- [ ] **Análisis de Consistencia** — KPI cards de consistencia
- [ ] **Estado de Forma** — Indicadores de forma actual
- [ ] **Proyección de Rendimiento** — Cards de proyección
- [ ] **Objetivos y Logros** — Progress bars (cs-goals-container)
- [ ] **Optimización de Práctica** — Cards de práctica recomendada

### Patrón de migración por sección
1. Identificar gradient backgrounds → reemplazar por `rgba(255,255,255,0.04)`
2. Borders con color → `1px solid rgba(255,255,255,0.08)` + `border-top: 2px solid [accent]`
3. Text-shadow en valores → eliminar
4. Labels descriptivos → `9px uppercase #9a9e94`
5. Inner boxes → `rgba(255,255,255,0.03)` con `border-left: 3px solid`

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas para conclusión AI
- [ ] **Performance por Campo** — Conclusión sobre qué campos favorecen el juego y por qué
- [ ] **Análisis de Scoring** — Conclusión sobre patrones de scoring

### Implementación
1. Añadir keys al skill prompt de UXWriter: `campo_conclusion`, `scoring_analysis_conclusion`
2. Añadir anchors HTML: `<div id="ai-campo-conclusion"></div>`, `<div id="ai-scoring-conclusion"></div>`
3. Añadir inyección JS en `insertUXContent()` con estilo azul `#4A9FD8`
4. Añadir `course_statistics` y `campo_performance` al `_compact()` (ya están)

---

## 4. Checklist final

- [ ] Quick menu: todas las secciones, orden correcto, sin emojis
- [ ] Glassmorphism aplicado a todas las secciones
- [ ] Conclusiones AI inyectadas y funcionales
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Gráficos resize correctamente al cambiar de tab
