# Análisis de las 52 Funciones del Backend y el Filtrado UI_ONLY_KEYS

**Fecha:** 2026-02-24
**Contexto:** Evaluación del impacto del filtrado `UI_ONLY_KEYS` sobre las funciones de `generate_dashboard_data.py`

---

## Aclaración Importante

**NO SE PIERDE NINGUNA FUNCIÓN DEL BACKEND.**

Las 52 funciones siguen ejecutándose al 100%. Los datos que generan siguen existiendo en `dashboard_data.json` y el dashboard frontend los sigue consumiendo normalmente.

Lo que hace `UI_ONLY_KEYS` es filtrar **5 claves del JSON cuando se pasan como contexto a los agentes IA** (Analista, Tecnico, Estratega, Coach). Es un filtro de *lectura* para los LLMs, no de *generación*.

```
┌─────────────────────────────┐
│ generate_dashboard_data.py  │ ← 52 funciones ejecutan al 100%
│ (52 funciones)              │
└─────────────┬───────────────┘
              │ genera
              ▼
┌─────────────────────────────┐
│ dashboard_data.json         │ ← 52 claves, 106.8 KB (SIN CAMBIOS)
│ (52 claves completas)       │
└──────┬──────────────┬───────┘
       │              │
       ▼              ▼
┌──────────────┐ ┌──────────────────────┐
│ Dashboard    │ │ Agentes IA           │
│ Frontend     │ │ (orchestrator.py)    │
│ (HTML/JS)    │ │                      │
│              │ │ ┌──────────────────┐ │
│ USA LAS 52   │ │ │ _filter_for_     │ │
│ CLAVES       │ │ │ agents()         │ │
│ COMPLETAS    │ │ │                  │ │
│              │ │ │ Quita 5 claves   │ │
│              │ │ │ de pura UI       │ │
│              │ │ │ (-36.8 KB)       │ │
│              │ │ └──────────────────┘ │
│              │ │                      │
│              │ │ Pasa 47 claves       │
│              │ │ (69.8 KB) a LLMs    │
└──────────────┘ └──────────────────────┘
```

---

## Catálogo Completo de las 52 Funciones

### Funciones de Infraestructura (3) — No generan claves JSON

| # | Función | Línea | Propósito |
|---|---------|-------|-----------|
| — | `load_flightscope_data()` | 53 | Carga datos FlightScope desde Excel (493 shots) |
| — | `load_tarjetas_data()` | 70 | Carga tarjetas de rondas desde Excel (52 rondas) |
| — | `merge_club_data()` | 510 | Fusiona estadísticas de palos con launch + dispersión |

---

### Funciones que Generan las 52 Claves del JSON

#### Sprint Base — Métricas Fundamentales (7 funciones → 7 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 1 | `calculate_player_stats()` | 266 | `player_stats` | 0.2 KB | 1 | Estadísticas generales: HCP, rondas, media, mejor score |
| 2 | `calculate_club_statistics()` | 140 | `club_statistics` | 2.5 KB | 4 | Stats por palo: distancia media, dispersión, smash factor |
| 3 | `calculate_temporal_evolution()` | 217 | `temporal_evolution` | 1.2 KB | 2 | Evolución temporal de distancias (11 palos, mensual) |
| 4 | `calculate_course_statistics()` | 238 | `course_statistics` | 2.2 KB | 3 | Rendimiento por campo: media, mejor, peor, rondas |
| 5 | `calculate_launch_metrics()` | 296 | `launch_metrics` | 6.3 KB | 4-5 | Métricas de launch: ángulo, velocidad, spin por palo |
| 6 | `calculate_dispersion_analysis()` | 331 | `dispersion_analysis` | 8.9 KB | 4-5 | Análisis de dispersión: lateral, carry, total por palo |
| 7 | `calculate_consistency_benchmarks()` | 366 | `consistency_benchmarks` | 3.5 KB | 5 | Benchmarks de consistencia vs PGA/HCP15/HCP23 |

#### Sprint 1 — Scatter + Gaps (2 funciones → 2 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 8 | `generate_dispersion_scatter_data()` | 403 | `dispersion_by_club` | **11.8 KB** | 4 | Datos scatter plot: cada shot individual {x, y} por palo |
| 9 | `calculate_club_gaps()` | 635 | `club_gaps` | 0.2 KB | 4 | Gaps de distancia entre palos consecutivos |

#### Sprint 3 — Análisis Importantes (4 funciones → 4 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 10 | `calculate_score_history()` | 693 | `score_history` | 7.6 KB | 1-2 | Historial completo de scores con milestones |
| 11 | `calculate_percentiles()` | 813 | `percentiles` | 1.1 KB | 4-5 | Percentiles de distancia y scores por palo |
| 12 | `calculate_directional_distribution()` | 871 | `directional_distribution` | 1.4 KB | 4 | Distribución left/center/right por palo |
| 13 | `calculate_bubble_chart_data()` | 943 | `bubble_chart_data` | 1.2 KB | 4 | Consistencia vs distancia (bubble chart) |

#### Sprint 5 — Mejoras Visuales (4 funciones → 4 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 14 | `calculate_player_profile_radar()` | 1017 | `player_profile_radar` | 0.3 KB | 1 | Radar 8 dimensiones del perfil de jugador |
| 15 | `extract_trajectory_data()` | 1217 | `trajectory_data` | 1.3 KB | 4 | Trayectorias de vuelo por palo |
| 16 | `calculate_best_worst_rounds()` | 1271 | `best_worst_rounds` | 1.7 KB | 1-3 | Top 5 mejores y peores rondas con contexto |
| 17 | `calculate_quarterly_scoring()` | 1365 | `quarterly_scoring` | 0.8 KB | 2 | Scoring promedio por trimestre |

#### Sprint 6 — Tendencias (4 funciones → 4 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 18 | `calculate_monthly_volatility()` | 1444 | `monthly_volatility` | 1.7 KB | 2 | Volatilidad mensual de scores |
| 19 | `calculate_momentum_indicators()` | 1521 | `momentum_indicators` | 6.8 KB | 2 | Moving averages y momentum por ronda |
| 20 | `extract_milestone_achievements()` | 1605 | `milestone_achievements` | 1.2 KB | 1 | Hitos alcanzados: broke 90, best scores, rachas |
| 21 | `calculate_learning_curve()` | 1769 | `learning_curve` | 0.4 KB | 2 | Curva de aprendizaje por categoría de tiro |

#### Sprint 9 — Overview + Evolution (8 funciones → 8 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 22 | `calculate_current_form_chart()` | 1886 | `current_form` | 0.8 KB | 1 | Últimas 20 rondas con tendencia |
| 23 | `calculate_percentile_gauges()` | 1955 | `percentile_gauges` | 0.4 KB | 1 | 4 gauges: short game, ball speed, consistencia, ataque |
| 24 | `calculate_hcp_trajectory()` | 2085 | `hcp_trajectory` | 0.7 KB | 1-2 | HCP histórico + proyección 6 meses |
| 25 | `calculate_temporal_long_game()` | 2236 | `temporal_long_game` | 0.3 KB | 2 | Evolución mensual Driver, 3W, Hybrid |
| 26 | `calculate_irons_evolution()` | 2336 | `irons_evolution` | 0.4 KB | 2 | Evolución mensual hierros 5i-9i |
| 27 | `calculate_wedges_evolution()` | 2446 | `wedges_evolution` | 0.2 KB | 2 | Evolución mensual PW, GW, SW |
| 28 | `calculate_attack_angle_evolution()` | 2546 | `attack_angle_evolution` | 0.1 KB | 2 | Evolución ángulo de ataque Driver |
| 29 | `calculate_smash_factor_evolution()` | 2639 | `smash_factor_evolution` | 0.5 KB | 2 | Evolución smash factor 4 categorías |

#### Sprint 10 — Campos + Análisis Avanzados (10 funciones → 10 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 30 | `calculate_campo_performance()` | 2781 | `campo_performance` | 0.8 KB | 3 | Mejor/promedio/peor score por campo |
| 31 | `calculate_hcp_evolution_rfeg()` | 2845 | `hcp_evolution_rfeg` | 0.1 KB | 1-2 | HCP oficial RFEG estimado mensual |
| 32 | `calculate_scoring_zones_by_course()` | 2999 | `scoring_zones_by_course` | **0.0 KB** | 3 | Distribución birdie/par/bogey por campo |
| 33 | `calculate_volatility_index()` | 3086 | `volatility_index` | 0.6 KB | 2 | Índice de variabilidad por trimestre |
| 34 | `calculate_estado_forma()` | 3152 | `estado_forma` | 0.8 KB | 1 | Estado de forma últimos 12 meses |
| 35 | `calculate_hcp_curve_position()` | 3244 | `hcp_curve_position` | 0.2 KB | 5 | Distribución scores vs curva normal |
| 36 | `calculate_differential_distribution()` | 3339 | `differential_distribution` | 0.5 KB | 5 | Distribución de differentials |
| 37 | `calculate_prediction_model()` | 3418 | `prediction_model` | 0.1 KB | 6 | Predicción próximo score (regresión) |
| 38 | `calculate_roi_practice()` | 3523 | `roi_practice` | 0.8 KB | 6 | ROI frecuencia de práctica vs mejora |
| — | *(generado inline)* | 5076 | `generated_at` | **0.0 KB** | — | Timestamp ISO de generación |

#### Sprint 11 — Deep Analysis (8 funciones → 8 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 39 | `calculate_shot_zones_heatmap()` | 3644 | `shot_zones_heatmap` | **21.4 KB** | 5 | Heatmap: cada shot {x, y, distance} por palo + density map |
| 40 | `calculate_scoring_probability()` | 3764 | `scoring_probability` | 0.7 KB | 5 | Probabilidad birdie/par/bogey por rango de distancia |
| 41 | `calculate_swing_dna()` | 3834 | `swing_dna` | 1.5 KB | 5 | Fingerprint 12 dimensiones vs benchmarks |
| 42 | `calculate_quick_wins_matrix()` | 3966 | `quick_wins_matrix` | 1.3 KB | 6 | Matriz dificultad vs impacto |
| 43 | `calculate_club_distance_comparison()` | 4083 | `club_distance_comparison` | 1.1 KB | 4 | Comparación distancias vs PGA/HCP |
| 44 | `calculate_comfort_zones()` | 4178 | `comfort_zones` | 0.8 KB | 5 | Zonas de confort por rango de distancia |
| 45 | `calculate_tempo_analysis()` | 4255 | `tempo_analysis` | 0.3 KB | 5 | Tempo backswing/downswing vs PGA |
| 46 | `calculate_strokes_gained()` | 4329 | `strokes_gained` | 1.0 KB | 5-6 | Strokes gained por categoría vs HCP 15 |

#### Sprint 12 — Estrategia (4 funciones → 4 claves)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 47 | `calculate_six_month_projection()` | 4435 | `six_month_projection` | 0.6 KB | 6 | Proyección HCP y scores 6 meses |
| 48 | `calculate_swot_matrix()` | 4538 | `swot_matrix` | 1.4 KB | 5 | Análisis SWOT automático |
| 49 | `calculate_benchmark_radar()` | 4610 | `benchmark_radar` | 0.5 KB | 5 | Radar multidimensional vs PGA/HCP15/HCP23 |
| 50 | `calculate_roi_plan()` | 4701 | `roi_plan` | 1.6 KB | 6 | Plan de mejora con ROI y milestones |

#### Metadata (1 bloque inline → 1 clave)

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 51 | *(inline en generate_dashboard_data)* | 5155 | `metadata` | **3.6 KB** | — | Versión, sprint, changelog, stats del generador |

#### Scoring Integration (añadido en save_json) → 2 claves adicionales

| # | Función | Línea | Clave JSON | Tamaño | Tab | Descripción |
|---|---------|-------|------------|--------|-----|-------------|
| 52 | `add_scoring_to_dashboard()` | save_json | `scoring_profile` | ~0.8 KB | 1 | 8 dimensiones 0-10, ranking, fortaleza/gap |
| 53 | *(dentro de scoring)* | save_json | `golf_identity` | ~1.0 KB | 1 | Arquetipo, fit score, evolución, insights |

> **Nota:** El JSON tiene 52 claves. Las funciones son ~50 funciones `calculate_*` + 2 claves generadas inline (`generated_at`, `metadata`) + 2 claves añadidas en `save_json()` por scoring integration (`scoring_profile`, `golf_identity`).

---


## Resumen Visual del Filtrado

```
┌──────────────────────────────────────────────────────────────────┐
│                    dashboard_data.json (106.8 KB)                 │
│                                                                   │
│  ┌── PASAN A LOS AGENTES (47 claves, 69.8 KB) ───────────────┐  │
│  │                                                             │  │
│  │  player_stats (0.2)   club_statistics (2.5)                 │  │
│  │  temporal_evolution (1.2)   course_statistics (2.2)         │  │
│  │  launch_metrics (6.3)   dispersion_analysis (8.9)          │  │
│  │  consistency_benchmarks (3.5)   club_gaps (0.2)            │  │
│  │  score_history (7.6)   percentiles (1.1)                   │  │
│  │  directional_distribution (1.4)   bubble_chart_data (1.2)  │  │
│  │  player_profile_radar (0.3)   trajectory_data (1.3)        │  │
│  │  best_worst_rounds (1.7)   quarterly_scoring (0.8)         │  │
│  │  monthly_volatility (1.7)   momentum_indicators (6.8)      │  │
│  │  milestone_achievements (1.2)   learning_curve (0.4)       │  │
│  │  current_form (0.8)   percentile_gauges (0.4)              │  │
│  │  hcp_trajectory (0.7)   temporal_long_game (0.3)           │  │
│  │  irons_evolution (0.4)   wedges_evolution (0.2)            │  │
│  │  attack_angle_evolution (0.1)   smash_factor_evolution (0.5)│  │
│  │  campo_performance (0.8)   hcp_evolution_rfeg (0.1)        │  │
│  │  volatility_index (0.6)   estado_forma (0.8)               │  │
│  │  hcp_curve_position (0.2)   differential_distribution (0.5)│  │
│  │  prediction_model (0.1)   roi_practice (0.8)               │  │
│  │  scoring_probability (0.7)   swing_dna (1.5)               │  │
│  │  quick_wins_matrix (1.3)   club_distance_comparison (1.1)  │  │
│  │  comfort_zones (0.8)   tempo_analysis (0.3)                │  │
│  │  strokes_gained (1.0)   six_month_projection (0.6)         │  │
│  │  swot_matrix (1.4)   benchmark_radar (0.5)                 │  │
│  │  roi_plan (1.6)   scoring_profile (~0.8)                   │  │
│  │  golf_identity (~1.0)                                       │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌── FILTRADAS (5 claves, 36.9 KB) ── Solo para Chart.js ─────┐  │
│  │                                                             │  │
│  │  shot_zones_heatmap    (21.4 KB) — coords XY crudas        │  │
│  │  dispersion_by_club    (11.8 KB) — scatter plots crudos    │  │
│  │  metadata              ( 3.6 KB) — config del generador    │  │
│  │  generated_at          ( 0.0 KB) — timestamp               │  │
│  │  scoring_zones_by_course (0.0 KB) — datos vacíos           │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  NOTA: UXWriter tiene su propio _compact() que selecciona solo   │
│  14 claves específicas (~15 KB). No le afecta este filtro.       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```


---

## Flujo de datos: Función → Clave → Consumidores

```
calculate_shot_zones_heatmap()
    │
    ├──→ dashboard_data.json["shot_zones_heatmap"]  (21.4 KB)
    │         │
    │         ├──→ Dashboard Tab 5 (heatmap visual)     ✅ SIGUE FUNCIONANDO
    │         └──→ Agentes IA                           ❌ FILTRADA (datos crudos XY)
    │
    └──→ La info ANALÍTICA derivada ya existe en:
              ├──→ dispersion_analysis (8.9 KB)         ✅ PASA A AGENTES
              └──→ directional_distribution (1.4 KB)    ✅ PASA A AGENTES


generate_dispersion_scatter_data()
    │
    ├──→ dashboard_data.json["dispersion_by_club"]  (11.8 KB)
    │         │
    │         ├──→ Dashboard Tab 4 (11 scatter plots)   ✅ SIGUE FUNCIONANDO
    │         └──→ Agentes IA                           ❌ FILTRADA (datos crudos)
    │
    └──→ La info ANALÍTICA derivada ya existe en:
              ├──→ dispersion_analysis (8.9 KB)         ✅ PASA A AGENTES
              └──→ club_statistics (2.5 KB)             ✅ PASA A AGENTES

