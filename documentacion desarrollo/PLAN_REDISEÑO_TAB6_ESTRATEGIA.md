# Plan de Rediseño — Tab 6: Estrategia & Acción

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
- Lista plana (sin sub-grupos), grid `repeat(auto-fill, minmax(280px, 1fr))`

---

## 1. Auditoría de Quick Menu

### Estado actual (9 items en 3 grupos, 8 secciones H2 + 1 sin id en h2)

**Quick menu actual (9 items en 3 grupos):**

Grupo 1 — Diagnóstico Estratégico (4 items):
1. Análisis DAFO Completo → `dafo-completo`
2. Matriz DAFO Visual → `matriz-dafo`
3. Posicionamiento vs Tour → `posicionamiento`
4. Estrategias Derivadas → `estrategias-derivadas`

Grupo 2 — Plan de Acción (4 items):
5. Matriz de Priorización → `matriz-priorizacion`
6. Optimización Técnica → `optimizacion-tecnica`
7. Heatmap ROI por Palo → `heatmap-roi`
8. ROI Plan Mejora → `roi-plan-mejora`

Grupo 3 — Conclusión (1 item):
9. Conclusión & Próximos Pasos → `conclusion-final`

**Secciones H2 reales en el dashboard (8 + 1):**

| # | ID | Título (línea) |
|---|----|----|
| 1 | `dafo-completo` | 🎯 Análisis DAFO Completo (10035) |
| 2 | `matriz-dafo` | 📊 Matriz DAFO (10280) |
| 3 | `posicionamiento` | ⚔️ Posicionamiento vs PGA Tour (10300) |
| 4 | `estrategias-derivadas` | 🎯 Estrategias Derivadas (10351) |
| 5 | `matriz-priorizacion` | 🎯 Matriz de Priorización (10398) |
| 6 | `optimizacion-tecnica` | 🔧 Optimización Técnica (10579) |
| 7 | `heatmap-roi` | 🔥 Heatmap ROI (11274) |
| 8 | `roi-plan-mejora` | 📈 ROI del Plan de Mejora (11439) — ⚠️ id en div, NO en h2 |
| 9 | `conclusion-final` | 🎯 Conclusión & Próximos Pasos (11491) |

### Problemas detectados
1. **`roi-plan-mejora`** — El `id` está en el `<div>` container (línea 11439), no en el `<h2>` (línea 11440). Inconsistencia estructural.

### Acciones requeridas
- [ ] Mover `id="roi-plan-mejora"` del div al h2 para consistencia estructural
- [ ] Eliminar agrupación en 3 sub-grupos → lista plana en orden secuencial
- [ ] Quitar emojis del quick menu → solo `•` + texto
- [ ] Verificar que el orden es correcto (parece serlo)

### Orden correcto (9 items)
1. Análisis DAFO Completo
2. Matriz DAFO Visual
3. Posicionamiento vs PGA Tour
4. Estrategias Derivadas del DAFO
5. Matriz de Priorización
6. Optimización Técnica
7. Heatmap ROI por Palo
8. ROI Plan de Mejora
9. Conclusión & Próximos Pasos

---

## 2. Glassmorphism — Secciones a rediseñar

- [ ] **Análisis DAFO** — Cards de Debilidades/Amenazas/Fortalezas/Oportunidades
- [ ] **Matriz DAFO** — Visualización 2x2 estratégica
- [ ] **Posicionamiento** — Gráfico comparativo Tú/PGA/HCP15
- [ ] **Estrategias Derivadas** — Cards de estrategias por cuadrante DAFO
- [ ] **Matriz de Priorización** — Scatter plot impacto vs esfuerzo + cards
- [ ] **Optimización Técnica** — Hoja de ruta con timeline (la más compleja)
- [ ] **Heatmap ROI** — Heat map de acciones por palo
- [ ] **ROI Plan de Mejora** — Cards antes/después con métricas (st-plan-metrics, st-plan-weeks, st-plan-success)
- [ ] **Conclusión & Próximos Pasos** — Resumen final con call-to-action

### Patrón de migración por sección
1. Gradient backgrounds → `rgba(255,255,255,0.04)`
2. Borders con color → `1px solid rgba(255,255,255,0.08)` + `border-top: 2px solid [accent]`
3. Text-shadow en valores → eliminar
4. Labels descriptivos → `9px uppercase #9a9e94`
5. Inner boxes → `rgba(255,255,255,0.03)` con `border-left: 3px solid`

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas para conclusión AI
- [ ] **Análisis DAFO** — Conclusión síntesis del DAFO y prioridad estratégica
- [ ] **Conclusión Final** — Ya existe como sección completa; valorar si necesita AI adicional o si el contenido actual es suficiente

### Implementación
1. Añadir key al skill prompt: `dafo_conclusion`
2. Añadir anchor HTML al pie de la sección DAFO
3. Añadir inyección JS en `insertUXContent()` con estilo azul `#4A9FD8`

---

## 4. Checklist final

- [ ] Quick menu: 9 secciones, orden correcto, sin emojis, lista plana
- [ ] Fix estructural: id de `roi-plan-mejora` en h2
- [ ] Glassmorphism aplicado a todas las secciones
- [ ] Conclusiones AI inyectadas y funcionales
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Gráficos resize correctamente al cambiar de tab
- [ ] Sección Optimización Técnica legible en mobile (es la más densa)
