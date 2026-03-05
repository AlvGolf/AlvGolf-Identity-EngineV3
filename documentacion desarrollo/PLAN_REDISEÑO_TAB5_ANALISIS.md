# Plan de Rediseño — Tab 5: Análisis Profundo

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

### Estado actual (16 items en 2 grupos, 14 secciones) — ⚠️ Discrepancias

**Quick menu actual (16 items en 2 grupos):**

Grupo 1 — Análisis Avanzado (10 items):
1. Shot Zones → `shot-zones`
2. Probabilidad Par/Birdie → `probabilidad-par-birdie`
3. Tempo & Rhythm → `tempo-rhythm`
4. Strokes Gained → `strokes-gained`
5. Game Plan Simulator → `game-plan-simulator`
6. Swing DNA → `swing-dna`
7. Quick Wins Calculator → `quick-wins`
8. Launch Metrics → `launch-metrics` ⚠️
9. Dispersion Analysis → `dispersion-analysis` ⚠️
10. Consistency Benchmarks → `consistency-benchmarks` ⚠️

Grupo 2 — vs PGA Tour (6 items):
11. Distancias Comparativa → `distancias-comparativa`
12. Dispersión/Precisión → `dispersion-comparativa`
13. Análisis de Pérdidas → `waterfall-analysis`
14. Métricas Vista Radar → `metricas-radar`
15. 8 Competencias vs Tour → `comparativa-8-competencias`
16. Zonas de Confort → `zonas-confort`

**Secciones H2 reales en el dashboard (14):**

| # | ID | Título (línea) |
|---|----|----|
| 1 | `learning-curve` | 📈 Curvas de Aprendizaje (8814) |
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

### Problemas detectados
1. **`learning-curve` (Curvas de Aprendizaje)** — Sección existe en dashboard pero **NO está en quick menu**
2. **`launch-metrics`** — Está en quick menu pero **NO existe como h2 en Tab 5** (puede ser sección de otro tab o ID fantasma)
3. **`dispersion-analysis`** — Está en quick menu pero **NO existe como h2 en Tab 5** (es `analisis-dispersion` en Tab 4)
4. **`consistency-benchmarks`** — Está en quick menu pero **verificar si existe como h2 en Tab 5**

### Acciones requeridas
- [ ] Verificar si `launch-metrics`, `dispersion-analysis`, `consistency-benchmarks` existen como secciones en Tab 5 (pueden tener id en div pero no en h2)
- [ ] Añadir "Curvas de Aprendizaje" → `learning-curve` como primer item
- [ ] Eliminar items fantasma que no corresponden a secciones de Tab 5
- [ ] Eliminar agrupación en 2 sub-grupos → lista plana en orden secuencial
- [ ] Quitar emojis del quick menu → solo `•` + texto

### Orden correcto propuesto (14 items o ajustar según verificación)
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

## 2. Glassmorphism — Secciones a rediseñar

- [ ] **Curvas de Aprendizaje** — Gráfico de learning curves
- [ ] **Shot Zones** — Mapa de calor del campo
- [ ] **Probabilidad Par/Birdie** — Gráfico por distancia
- [ ] **Tempo & Rhythm** — Cards de análisis de tempo
- [ ] **Strokes Gained** — Cards SG por categoría + gráfico
- [ ] **Game Plan Simulator** — Interfaz del simulador
- [ ] **Swing DNA** — Visualización de fingerprint
- [ ] **Quick Wins Calculator** — Matriz esfuerzo vs impacto
- [ ] **Distancias Comparativa** — Triple comparativa (Tú/HCP15/PGA)
- [ ] **Dispersión Comparativa** — Comparativa por categoría
- [ ] **Análisis de Pérdidas (Waterfall)** — Gráfico waterfall
- [ ] **Radar de Dimensiones** — Radar 360° con toggles
- [ ] **8 Competencias** — Cards comparativas vs PGA
- [ ] **Zonas de Confort** — Heat map de distancias

### Patrón de migración por sección
1. Gradient backgrounds → `rgba(255,255,255,0.04)`
2. Borders con color → `1px solid rgba(255,255,255,0.08)` + `border-top: 2px solid [accent]`
3. Text-shadow en valores → eliminar
4. Labels descriptivos → `9px uppercase #9a9e94`
5. Inner boxes → `rgba(255,255,255,0.03)` con `border-left: 3px solid`

---

## 3. Conclusiones AI (UXWriter)

### Secciones candidatas para conclusión AI
- [ ] **Strokes Gained** — Conclusión sobre dónde se ganan/pierden golpes vs benchmark
- [ ] **Zonas de Confort** — Conclusión sobre zonas fuertes/débiles y estrategia derivada

### Implementación
1. Añadir keys al skill prompt: `strokes_gained_conclusion`, `comfort_zones_conclusion`
2. Añadir anchors HTML al pie de cada sección
3. Añadir inyección JS en `insertUXContent()` con estilo azul `#4A9FD8`

---

## 4. Checklist final

- [ ] Quick menu: todas las secciones reales, orden correcto, sin emojis, lista plana
- [ ] Items fantasma eliminados del quick menu
- [ ] Glassmorphism aplicado a todas las secciones
- [ ] Conclusiones AI inyectadas y funcionales
- [ ] Consola sin errores
- [ ] Test en mobile (360px)
- [ ] Gráficos resize correctamente al cambiar de tab
