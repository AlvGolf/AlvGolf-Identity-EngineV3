# Plan de Rediseño — Tab 6: Estrategia & Acción

## Patrones establecidos en Tab 2 (aplicar consistentemente)

### Look & Feel
- **Glassmorphism**: containers `rgba(255,255,255,0.04)` + `1px solid rgba(255,255,255,0.08)` + `border-radius: 14px`
- **KPI cards**: flat + `border-top: 2px solid [accent-color]` + valor `2-2.6em font-weight 900` sin text-shadow
- **Labels**: `9px uppercase letter-spacing 1.5px color #9a9e94 font-weight 700`
- **Inner boxes**: `rgba(255,255,255,0.03)` + `border-left: 3px solid [accent]`
- **Conclusiones AI**: `"Conclusión:"` en azul `#4A9FD8`, sin emoji, sin "IA"

### Quick Menu
- Sin emojis, solo bullet point `•` + texto
- Todas las secciones representadas en orden exacto del dashboard
- Lista plana (sin sub-grupos), usando clase `.quick-nav-link`

### Prerequisito
> Las clases CSS utilitarias del Paso 0 (definidas en `PLAN_REDISEÑO_TAB3_CAMPOS.md`) deben estar ya implementadas.

---

## 1. Auditoría de Quick Menu

### Estado actual (9 items en 3 grupos, 9 secciones) — ✅ Cobertura 100%

**Quick menu actual (9 items en 3 grupos):**

Grupo 1 — Diagnóstico Estratégico:
1. Análisis DAFO Completo → `dafo-completo`
2. Matriz DAFO Visual → `matriz-dafo`
3. Posicionamiento vs Tour → `posicionamiento`
4. Estrategias Derivadas → `estrategias-derivadas`

Grupo 2 — Plan de Acción:
5. Matriz de Priorización → `matriz-priorizacion`
6. Optimización Técnica → `optimizacion-tecnica`
7. Heatmap ROI por Palo → `heatmap-roi`
8. ROI Plan Mejora → `roi-plan-mejora`

Grupo 3 — Conclusión:
9. Conclusión & Próximos Pasos → `conclusion-final`

**Secciones H2 reales (9):**

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

### Acciones requeridas
- [ ] Fix: mover `id="roi-plan-mejora"` del div container al h2 (línea 11440)
- [ ] Eliminar agrupación en 3 sub-grupos → lista plana
- [ ] Quitar emojis → solo `•` + texto
- [ ] Migrar inline styles a `.quick-nav-link`

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

## 2. Glassmorphism — Secciones a rediseñar (usando clases CSS)

- [ ] **Análisis DAFO** — Cards D/A/F/O → `.card-detail` + `.accent-*`
- [ ] **Matriz DAFO** — Visualización 2x2 → borders con tokens CSS
- [ ] **Posicionamiento** — Gráfico comparativo → `.card-detail`
- [ ] **Estrategias Derivadas** — Cards por cuadrante → `.card-detail` + `.inner-box`
- [ ] **Matriz de Priorización** — Scatter plot + cards → `.kpi-card` + `.card-detail`
- [ ] **Optimización Técnica** — Hoja de ruta timeline (la más compleja) → `.card-detail` + `.inner-box`
- [ ] **Heatmap ROI** — Heat map acciones → `.card-detail`
- [ ] **ROI Plan de Mejora** — Cards antes/después → `.kpi-card` + `.text-label`
- [ ] **Conclusión & Próximos Pasos** — Resumen final → `.card-detail` + `.inner-box`

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas
- [ ] **Análisis DAFO** — Conclusión síntesis del DAFO y prioridad estratégica
- [ ] **Conclusión Final** — Ya existe como sección completa; valorar si necesita AI adicional

### Implementación
1. Añadir key: `dafo_conclusion`
2. Añadir anchor HTML al pie de la sección DAFO
3. Inyección JS con `class="ai-conclusion"`

---

## 4. Checklist final

- [ ] Quick menu: 9 secciones, orden correcto, sin emojis, lista plana, `.quick-nav-link`
- [ ] Fix: id `roi-plan-mejora` movido al h2
- [ ] Glassmorphism con clases CSS (no inline)
- [ ] Conclusión AI con `.ai-conclusion`
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Sección Optimización Técnica legible en mobile (la más densa)
