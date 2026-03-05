# Plan de Rediseño — Tab 5: Análisis Profundo

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

### Estado actual (16 items en 2 grupos, 14 secciones) — ⚠️ Discrepancias graves

**Quick menu actual (16 items):**

Grupo 1 — Análisis Avanzado (10 items):
1. Shot Zones → `shot-zones`
2. Probabilidad Par/Birdie → `probabilidad-par-birdie`
3. Tempo & Rhythm → `tempo-rhythm`
4. Strokes Gained → `strokes-gained`
5. Game Plan Simulator → `game-plan-simulator`
6. Swing DNA → `swing-dna`
7. Quick Wins Calculator → `quick-wins`
8. Launch Metrics → `launch-metrics` ⚠️ **FANTASMA — no existe como h2 en Tab 5**
9. Dispersion Analysis → `dispersion-analysis` ⚠️ **FANTASMA — es `analisis-dispersion` de Tab 4**
10. Consistency Benchmarks → `consistency-benchmarks` ⚠️ **VERIFICAR si existe**

Grupo 2 — vs PGA Tour (6 items):
11. Distancias Comparativa → `distancias-comparativa`
12. Dispersión/Precisión → `dispersion-comparativa`
13. Análisis de Pérdidas → `waterfall-analysis`
14. Métricas Vista Radar → `metricas-radar`
15. 8 Competencias vs Tour → `comparativa-8-competencias`
16. Zonas de Confort → `zonas-confort`

**Secciones H2 reales (14):**

| # | ID | Título (línea) |
|---|----|----|
| 1 | `learning-curve` | 📈 Curvas de Aprendizaje (8814) — **FALTA en menu** |
| 2 | `shot-zones` | 🎯 Shot Zones (8910) |
| 3 | `probabilidad-par-birdie` | 🎲 Probabilidad Par/Birdie (9002) |
| 4 | `tempo-rhythm` | ⏱️ Tempo & Rhythm (9040) |
| 5 | `strokes-gained` | 📊 Strokes Gained (9080) |
| 6 | `game-plan-simulator` | 🎮 Game Plan Simulator (9121) |
| 7 | `swing-dna` | 🎨 Swing DNA (9193) |
| 8 | `quick-wins` | ⚡ Quick Wins Calculator (9240) |
| 9 | `distancias-comparativa` | 📏 Distancias Comparativa Triple (9348) |
| 10 | `dispersion-comparativa` | 🎯 Dispersión Comparativa (9382) |
| 11 | `waterfall-analysis` | 📊 Análisis de Pérdidas (9424) |
| 12 | `metricas-radar` | 📊 Radar de Dimensiones (9517) |
| 13 | `comparativa-8-competencias` | ⚔️ 8 Competencias vs PGA (9568) |
| 14 | `zonas-confort` | 🗺️ Zonas de Confort (9648) |

### Acciones requeridas
- [ ] Verificar `launch-metrics`, `dispersion-analysis`, `consistency-benchmarks` — si no existen como secciones en Tab 5, eliminar del menu
- [ ] Añadir "Curvas de Aprendizaje" → `learning-curve` como primer item
- [ ] Eliminar items fantasma
- [ ] Eliminar agrupación en 2 sub-grupos → lista plana
- [ ] Quitar emojis → solo `•` + texto
- [ ] Migrar inline styles a `.quick-nav-link`

### Orden correcto propuesto (14 items, ajustar según verificación)
1. Curvas de Aprendizaje
2. Shot Zones - Mapa de Calor
3. Probabilidad de Par/Birdie
4. Tempo & Rhythm Analysis
5. Strokes Gained Simplified
6. Game Plan Simulator
7. Swing DNA Fingerprint
8. Quick Wins Calculator
9. Distancias Comparativa Triple
10. Dispersión/Precisión Comparativa
11. Análisis de Pérdidas
12. Análisis 360° - Radar
13. Comparativa vs PGA Tour
14. Zonas de Confort

---

## 2. Glassmorphism — Secciones a rediseñar (usando clases CSS)

- [ ] **Curvas de Aprendizaje** — Gráfico → `.card-detail`
- [ ] **Shot Zones** — Mapa de calor → `.card-detail`
- [ ] **Probabilidad Par/Birdie** — Gráfico por distancia → `.card-detail`
- [ ] **Tempo & Rhythm** — Cards de análisis → `.kpi-card` + `.text-label`
- [ ] **Strokes Gained** — Cards SG por categoría + gráfico → `.kpi-card` + `.inner-box`
- [ ] **Game Plan Simulator** — Interfaz simulador → `.card-detail`
- [ ] **Swing DNA** — Visualización fingerprint → `.card-detail`
- [ ] **Quick Wins Calculator** — Matriz esfuerzo vs impacto → `.card-detail` + `.accent-*`
- [ ] **Distancias Comparativa** — Triple (Tú/HCP15/PGA) → `.kpi-card`
- [ ] **Dispersión Comparativa** — Por categoría → `.card-detail`
- [ ] **Análisis de Pérdidas (Waterfall)** — Gráfico → `.card-detail`
- [ ] **Radar de Dimensiones** — Radar 360° con toggles → `.card-detail`
- [ ] **8 Competencias** — Cards comparativas → `.kpi-card` + `.inner-box`
- [ ] **Zonas de Confort** — Heat map → `.card-detail`

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas
- [ ] **Strokes Gained** — Conclusión sobre dónde se ganan/pierden golpes vs benchmark
- [ ] **Zonas de Confort** — Conclusión sobre zonas fuertes/débiles y estrategia

### Implementación
1. Añadir keys: `strokes_gained_conclusion`, `comfort_zones_conclusion`
2. Añadir anchors HTML al pie de cada sección
3. Inyección JS con `class="ai-conclusion"`

---

## 4. Checklist final

- [ ] Quick menu: secciones reales, orden correcto, sin emojis, lista plana, `.quick-nav-link`
- [ ] Items fantasma eliminados
- [ ] Glassmorphism con clases CSS (no inline)
- [ ] Conclusiones AI con `.ai-conclusion`
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
