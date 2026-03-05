# Plan de Rediseño — Tab 4: Bolsa de Palos

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

### Estado actual (9 items en 3 grupos, 11 secciones) — ⚠️ Faltan 2

| # | Quick Menu Item | Target ID | En Dashboard |
|---|----------------|-----------|--------------|
| 1 | Rendimiento por Palo | `rendimiento-distancias` | ✅ (7592) |
| 2 | Análisis de Brechas | `brechas-palos` | ✅ (7645) |
| 3 | Performance Detallado | `performance-detallado` | ✅ (7834) |
| 4 | Distribución Direccional | `distribucion-direccional` | ✅ (7839) |
| — | ❌ Percentiles de Distancia | `percentiles-distancia` | ✅ (7862) — **FALTA en menu** |
| — | ❌ Datos de Trayectoria | `trajectory-data` | ✅ (7880) — **FALTA en menu** |
| 5 | Análisis de Dispersión | `analisis-dispersion` | ✅ (7897) |
| 6 | Análisis de Burbujas | `analisis-burbujas` | ✅ (8043) |
| 7 | Smash Factor por Palo | `smash-factor-palo` | ✅ (8073) |
| 8 | Métricas de Velocidad | `metricas-velocidad` | ✅ (8339) |
| 9 | Matriz de Rendimiento | `matriz-rendimiento` | ✅ (8448) |

### Acciones requeridas
- [ ] Añadir "Percentiles de Distancia" → `percentiles-distancia` (entre Distribución Direccional y Análisis de Dispersión)
- [ ] Añadir "Datos de Trayectoria" → `trajectory-data` (entre Percentiles y Análisis de Dispersión)
- [ ] Quitar emojis del quick menu → solo `•` + texto
- [ ] Eliminar agrupación en 3 sub-grupos → lista plana en orden secuencial (patrón Tab 2)
- [ ] Total final: 11 items en orden exacto del dashboard

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

## 2. Glassmorphism — Secciones a rediseñar

Revisar cada sección y migrar al patrón glassmorphism:

- [ ] **Rendimiento por Palo** — Cards carry/roll/total (cl-carry-long/mid/short)
- [ ] **Análisis de Brechas** — Gráfico de gaps entre palos
- [ ] **Performance Detallado** — Tabla matrix (cl-matrix-body)
- [ ] **Distribución Direccional** — Gráficos de dispersión lateral
- [ ] **Percentiles de Distancia** — Cards de percentiles
- [ ] **Datos de Trayectoria** — Cards de launch angle, spin, etc.
- [ ] **Análisis de Dispersión** — Charts por palo + summary (cl-disp-summary)
- [ ] **Análisis de Burbujas** — Bubble cards (cl-bubble-cards) + strategy (cl-bubble-strategy)
- [ ] **Smash Factor** — Gráfico comparativo por palo
- [ ] **Métricas de Velocidad** — Cards ball speed / club speed
- [ ] **Matriz de Rendimiento** — Tabla resumen general

### Patrón de migración por sección
1. Gradient backgrounds → `rgba(255,255,255,0.04)`
2. Borders con color → `1px solid rgba(255,255,255,0.08)` + `border-top: 2px solid [accent]`
3. Text-shadow en valores → eliminar
4. Labels descriptivos → `9px uppercase #9a9e94`
5. Inner boxes → `rgba(255,255,255,0.03)` con `border-left: 3px solid`

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas para conclusión AI
- [ ] **Análisis de Dispersión** — Conclusión sobre patrones de dispersión y prioridades de mejora
- [ ] **Matriz de Rendimiento** — Conclusión general sobre el estado de la bolsa de palos

### Implementación
1. Añadir keys al skill prompt: `dispersion_conclusion`, `equipment_conclusion`
2. Añadir anchors HTML al pie de cada sección
3. Añadir inyección JS en `insertUXContent()` con estilo azul `#4A9FD8`

---

## 4. Checklist final

- [ ] Quick menu: 11 secciones, orden correcto, sin emojis, lista plana
- [ ] Glassmorphism aplicado a todas las secciones
- [ ] Conclusiones AI inyectadas y funcionales
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Gráficos resize correctamente al cambiar de tab
- [ ] Tablas/matrices legibles en mobile
