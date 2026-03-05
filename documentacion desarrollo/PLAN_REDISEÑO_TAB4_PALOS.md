# Plan de Rediseño — Tab 4: Bolsa de Palos

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
> Clases disponibles: `.text-label`, `.kpi-card`, `.kpi-value`, `.kpi-sub`, `.quick-nav-link`, `.ai-conclusion`, `.inner-box`

---

## 1. Auditoría de Quick Menu

### Estado actual (9 items en 3 grupos, 11 secciones) — ⚠️ Faltan 2

| # | Quick Menu Item | Target ID | En Dashboard |
|---|----------------|-----------|--------------|
| 1 | Rendimiento por Palo | `rendimiento-distancias` | ✅ (7592) |
| 2 | Análisis de Brechas | `brechas-palos` | ✅ (7645) |
| 3 | Performance Detallado | `performance-detallado` | ✅ (7834) |
| 4 | Distribución Direccional | `distribucion-direccional` | ✅ (7839) |
| — | ❌ Percentiles de Distancia | `percentiles-distancia` | ✅ (7862) — **FALTA** |
| — | ❌ Datos de Trayectoria | `trajectory-data` | ✅ (7880) — **FALTA** |
| 5 | Análisis de Dispersión | `analisis-dispersion` | ✅ (7897) |
| 6 | Análisis de Burbujas | `analisis-burbujas` | ✅ (8043) |
| 7 | Smash Factor por Palo | `smash-factor-palo` | ✅ (8073) |
| 8 | Métricas de Velocidad | `metricas-velocidad` | ✅ (8339) |
| 9 | Matriz de Rendimiento | `matriz-rendimiento` | ✅ (8448) |

### Acciones requeridas
- [ ] Añadir "Percentiles de Distancia" → `percentiles-distancia`
- [ ] Añadir "Datos de Trayectoria" → `trajectory-data`
- [ ] Quitar emojis del quick menu → solo `•` + texto
- [ ] Eliminar agrupación en 3 sub-grupos → lista plana en orden secuencial
- [ ] Migrar inline styles a `.quick-nav-link`

### Orden correcto (11 items)
1. Rendimiento por Palo - Distancias
2. Análisis de Brechas Entre Palos
3. Performance Detallado por Club
4. Distribución Direccional
5. Percentiles de Distancia por Palo
6. Datos de Trayectoria por Palo
7. Análisis de Dispersión por Palo
8. Análisis de Burbujas
9. Smash Factor por Palo
10. Métricas de Velocidad y Potencia
11. Matriz de Rendimiento Palos

---

## 2. Glassmorphism — Secciones a rediseñar (usando clases CSS)

- [ ] **Rendimiento por Palo** — Cards carry/roll/total → `.kpi-card` + `.text-label`
- [ ] **Análisis de Brechas** — Gráfico de gaps → `.card-detail`
- [ ] **Performance Detallado** — Tabla matrix (cl-matrix-body) → borders con tokens CSS
- [ ] **Distribución Direccional** — Gráficos dispersión → `.card-detail`
- [ ] **Percentiles de Distancia** — Cards percentiles → `.kpi-card`
- [ ] **Datos de Trayectoria** — Cards launch angle/spin → `.card-detail`
- [ ] **Análisis de Dispersión** — Charts + summary → `.inner-box`
- [ ] **Análisis de Burbujas** — Bubble cards → `.card-detail` + `.accent-*`
- [ ] **Smash Factor** — Gráfico comparativo → `.card-detail`
- [ ] **Métricas de Velocidad** — Cards ball/club speed → `.kpi-card`
- [ ] **Matriz de Rendimiento** — Tabla resumen → borders con tokens CSS

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas
- [ ] **Análisis de Dispersión** — Conclusión sobre patrones y prioridades de mejora
- [ ] **Matriz de Rendimiento** — Conclusión general sobre estado de la bolsa

### Implementación
1. Añadir keys al skill prompt: `dispersion_conclusion`, `equipment_conclusion`
2. Añadir anchors HTML al pie de cada sección
3. Inyección JS usa `class="ai-conclusion"` (no inline style)

---

## 4. Checklist final

- [ ] Quick menu: 11 secciones, orden correcto, sin emojis, lista plana, `.quick-nav-link`
- [ ] Glassmorphism con clases CSS (no inline)
- [ ] Conclusiones AI con `.ai-conclusion`
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Tablas/matrices legibles en mobile
