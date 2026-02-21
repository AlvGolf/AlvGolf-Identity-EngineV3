# 📋 Plan de Implementación Detallado V2 - AlvGolf Dashboard Backend

**🎯 OBJETIVO: Completar Dashboard 100% Dinámico**

**Fecha creación:** 2026-02-07
**Última actualización:** 2026-02-07 21:15
**Versión:** 2.1
**Estado:** 🟢 Sprint 9 - TASK 9.1 Completado
**Estrategia:** Plan Optimizado por Prioridades
**Metodología:** Sprints iterativos con testing continuo
**Objetivo Final:** 56/61 charts dinámicos (91.8% completado)
**Progreso Actual:** 17/61 charts dinámicos (27.9%) - +1 desde última actualización

---

## 📊 RESUMEN DEL DESARROLLO ANTERIOR

### ✅ Sprints 1-8 Completados (2026-02-03 a 2026-02-06)

**Backend ETL (generate_dashboard_data.py):**
- ✅ 22 funciones implementadas
- ✅ 21 secciones JSON generadas
- ✅ 128 KB JSON size
- ✅ 3.1s execution time
- ✅ 98.3% tests passing (118/120)

**Frontend Dashboard (dashboard_dynamic.html):**
- ✅ 16 visualizaciones dinámicas integradas
- ✅ 16,457 líneas de código
- ✅ Chart.js v4.x implementado
- ✅ Event system (`dashboardDataReady`)
- ✅ 12 charts Sprint 8 integrados

**Deployment:**
- ✅ GitHub Pages online: https://alvgolf.github.io/AlvGolf-Identity-EngineV3/
- ✅ Responsive optimizado (iOS 18, Android 15, Windows 11)
- ✅ CSS Safe integrado sin conflictos

**Funciones Backend Implementadas:**
1. `calculate_player_stats()` - Player overview
2. `calculate_club_statistics()` - 11 clubs stats
3. `calculate_club_gaps()` - Gaps between clubs
4. `generate_dispersion_scatter_data()` - 11 scatter plots
5. `calculate_temporal_evolution()` - Temporal trends
6. `calculate_course_statistics()` - 12 courses analysis
7. `calculate_score_history()` - 85 rounds timeline
8. `calculate_percentiles()` - Distance percentiles
9. `calculate_directional_distribution()` - Left/center/right
10. `calculate_bubble_chart_data()` - Distance vs consistency
11. `calculate_player_profile_radar()` - 8 dimensions radar
12. `extract_trajectory_data()` - Flight trajectory
13. `calculate_best_worst_rounds()` - Top/bottom rounds
14. `calculate_quarterly_scoring()` - Quarterly analysis
15. `calculate_monthly_volatility()` - 22 months volatility
16. `calculate_momentum_indicators()` - SMA-5, SMA-10
17. `extract_milestone_achievements()` - 15 milestones
18. `calculate_learning_curve()` - Long/mid/short game
19. `calculate_launch_metrics()` - Launch analysis (Fase 5)
20. `calculate_dispersion_analysis()` - Dispersion metrics (Fase 5)
21. `calculate_consistency_benchmarks()` - Consistency analysis (Fase 5)
22. 🆕 `calculate_current_form_chart()` - Last 20 rounds with trend (Sprint 9) ✅
23. `generate_dashboard_data()` - Main orchestrator

**Total Backend Functions:** 22 implementadas (21 completas + 1 nuevo Sprint 9)

---

## 🎯 ESTADO ACTUAL DEL PROYECTO

### 📊 Audit Completo (2026-02-07 - Actualizado 21:15)

**Resultado del Audit:**
- **Total Charts en Dashboard:** 61
- **Charts Dinámicos (✅):** 17 (27.9%) ⬆️ +1 desde 2026-02-07
- **Charts Hardcodeados (⚠️):** 44 (72.1%)
- **Funciones Backend Implementadas:** 22 (42.3%)
- **Funciones Backend FALTANTES:** 29 (55.8%)

### Desglose por Tab

| Tab | Total Charts | Dinámicos | Hardcoded | % Completado |
|-----|--------------|-----------|-----------|--------------|
| **Tab 1: Mi Identidad** | 7 | 2 (+1) | 5 | 28.6% ⬆️ |
| **Tab 2: Evolución Temporal** | 11 | 4 | 7 | 36.4% |
| **Tab 3: Mis Campos** | 12 | 2 | 10 | 16.7% |
| **Tab 4: Bolsa de Palos** | 18 | 15 | 3 | 83.3% ✅ |
| **Tab 5: Análisis Profundo** | 19 | 4 | 15 | 21.1% |
| **Tab 6: Estrategia & Acción** | 4 | 0 | 4 | 0% |
| **TOTAL** | **61** | **17** | **44** | **27.9%** |

**Última actualización:** 2026-02-07 21:15 - Sprint 9 TASK 9.1 completado ✅

---

## 🚀 PLAN DE IMPLEMENTACIÓN V2 (Sprints 9-12)

### Objetivo Final
**56/61 charts dinámicos (91.8% completado)**

**Timeline:** 7 semanas
**Sprints:** 4 sprints (9, 10, 11, 12)
**Funciones a implementar:** 30

---

## 📅 SPRINT 9: OVERVIEW + EVOLUTION (Tabs 1-2)

**Duración:** 2 semanas
**Objetivo:** Dinamizar Tabs 1 y 2 (los más visibles)
**Funciones:** 8
**Charts impactados:** 11
**Resultado esperado:** 27/61 charts (44.3%)
**Progreso:** 3/8 funciones (37.5%) ✅
**Estado:** 🟡 EN PROGRESO
**Completadas:** TASK 9.1 (current_form), 9.2 (percentile_gauges), 9.3 (hcp_trajectory)
**Próxima:** TASK 9.4 (temporal_long_game)

---

### ✅ TASK 9.1: `calculate_current_form_chart()` - COMPLETADO

**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Baja
**Tiempo real:** 2 horas
**Tab:** 1 (Mi Identidad)
**Chart ID:** `currentFormChart`
**Línea HTML:** 15535-15700
**Línea Backend:** 1886-1956
**Fecha completado:** 2026-02-07
**Commit:** af124f4

**Descripción:**
Genera datos para el gráfico de "Current Form" que muestra las últimas 20 rondas con scores y campos.

**Input:**
- `self.tarjetas_data`: Diccionario con todas las rondas

**Output esperado:**
```json
{
  "current_form": {
    "labels": ["16/11/2025", "07/12/2025", ...],  // Últimas 20 fechas
    "scores": [88, 92, 89, ...],                   // Scores
    "courses": ["Marina Golf", "LA DEHESA", ...],  // Nombres campos
    "average": 91.5,                                // Promedio últimas 20
    "trend": "improving"                            // improving/declining/stable
  }
}
```

**Algoritmo:**
```python
def calculate_current_form_chart(self):
    """
    Extrae últimas 20 rondas con fecha, score y campo.
    Calcula promedio y tendencia.
    """
    logger.info("Calculating current form chart (últimas 20 rondas)")

    all_rounds = []

    # Extraer todas las rondas
    for campo_nombre, campo_data in self.tarjetas_data.items():
        for ronda in campo_data['rondas']:
            all_rounds.append({
                'fecha': ronda['fecha'],
                'score': ronda['total_ronda'],
                'campo': campo_nombre
            })

    # Ordenar por fecha descendente (más recientes primero)
    all_rounds.sort(key=lambda x: x['fecha'], reverse=True)

    # Tomar últimas 20
    last_20 = all_rounds[:20]

    # Invertir para que cronológicamente vaya de izquierda a derecha
    last_20.reverse()

    # Extraer datos
    labels = [r['fecha'] for r in last_20]
    scores = [r['score'] for r in last_20]
    courses = [r['campo'] for r in last_20]

    # Calcular promedio
    average = sum(scores) / len(scores) if scores else 0

    # Determinar tendencia (últimas 5 vs primeras 5)
    if len(scores) >= 10:
        first_5_avg = sum(scores[:5]) / 5
        last_5_avg = sum(scores[-5:]) / 5

        if last_5_avg < first_5_avg - 2:
            trend = "improving"
        elif last_5_avg > first_5_avg + 2:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"

    logger.success(f"Current form chart: {len(last_20)} rounds, avg: {average:.1f}, trend: {trend}")

    return {
        'labels': labels,
        'scores': scores,
        'courses': courses,
        'average': round(average, 1),
        'trend': trend,
        'total_rounds': len(last_20)
    }
```

**Integración en generate_dashboard_data():**
```python
# En línea ~1900, añadir:
current_form = self.calculate_current_form_chart()

# En dashboard_data dict:
'current_form': current_form,
```

**Criterios de aceptación:**
- [x] Retorna últimas 20 rondas ordenadas cronológicamente ✅
- [x] Labels con fechas en formato YYYY-MM-DD (backend) → DD/MM (frontend) ✅
- [x] Scores son números válidos ✅
- [x] Courses tiene nombres de campos ✅
- [x] Average calculado correctamente ✅
- [x] Trend determina correctamente mejora/empeora/estable ✅
- [x] Dashboard HTML muestra line chart con 20 puntos ✅

**Resultados Reales (2026-02-07):**
```json
{
  "current_form": {
    "labels": ["2025-07-19", "2025-07-26", ..., "2025-12-07"],
    "scores": [103, 93, 101, 92, 94, 94, 96, 89, 89, 89, 95, 100, 101, 99, 107, 90, 88, 97, 96, 93],
    "courses": ["LA DEHESA", "MARINA GOLF", "LA DEHESA", ..., "LA DEHESA"],
    "average": 95.3,
    "trend": "improving",
    "total_rounds": 20
  }
}
```

**Análisis de datos:**
- ✅ 20 rondas extraídas correctamente
- ✅ Promedio: 95.3 (primeras 5: 96.6, últimas 5: 92.8)
- ✅ Tendencia: **IMPROVING** (mejorando 3.8 puntos)
- ✅ Mejor score L20: 88 (Marina Golf)
- ✅ Frontend renderiza correctamente con tooltips dinámicos

**Cambios implementados:**
- Backend: `generate_dashboard_data.py` líneas 1886-1956
- Frontend: `dashboard_dynamic.html` líneas 15535-15700
- Metadata actualizada: version 3.4.0, sprint 9
- IDs añadidos: formTrendIcon, formTrendText, formAverageValue, formBestScore, formStreakText

**GitHub:**
- Commit: af124f4
- URL: https://github.com/AlvGolf/AlvGolf-Identity-EngineV3
- Public dashboard: https://alvgolf.github.io/AlvGolf-Identity-EngineV3/

---

### 🔴 TASK 9.2: `calculate_percentile_gauges()`

**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Media
**Tiempo estimado:** 3 horas
**Tab:** 1 (Mi Identidad)
**Chart IDs:** `percentileShortGame`, `percentileBallSpeed`, `percentileConsistency`, `percentileAttackAngle`
**Líneas HTML:** 2642, 2660, 2679, 2697

**Descripción:**
Calcula 4 percentiles gauges comparando el jugador vs benchmarks:
1. Short Game (distancia wedges vs HCP 23)
2. Ball Speed (velocidad vs PGA Tour)
3. Consistency (CV de scores vs benchmark)
4. Attack Angle (ángulo vs óptimo)

**Output esperado:**
```json
{
  "percentile_gauges": {
    "short_game": {
      "value": 91,                     // Percentil 0-100
      "player_avg": 95.2,              // Promedio jugador (metros wedges)
      "benchmark_avg": 85.0,           // Benchmark HCP 23
      "rating": "excellent"            // excellent/good/average/poor
    },
    "ball_speed": {
      "value": 78,
      "player_avg": 235.5,             // km/h
      "benchmark_avg": 273.0,          // PGA Tour
      "rating": "good"
    },
    "consistency": {
      "value": 65,
      "player_cv": 0.15,               // Coef. variación scores
      "benchmark_cv": 0.18,            // HCP 23 típico
      "rating": "average"
    },
    "attack_angle": {
      "value": 25,
      "player_avg": -2.5,              // Grados (negativo = descending)
      "benchmark_avg": -1.5,           // Óptimo
      "rating": "poor"
    }
  }
}
```

**Algoritmo:**
```python
def calculate_percentile_gauges(self):
    """
    Calcula 4 percentiles gauges para Tab 1.
    Compara player vs benchmarks y asigna percentil 0-100.
    """
    logger.info("Calculating percentile gauges (4 metrics)")

    # 1. SHORT GAME (promedio wedges)
    wedges = ['PW', 'GW 52', 'SW 58']
    wedge_distances = []

    for palo in wedges:
        palo_df = self.flightscope_df[self.flightscope_df['palo'] == palo]
        if len(palo_df) > 0:
            avg_dist = palo_df['vuelo_act'].mean()
            wedge_distances.append(avg_dist)

    player_wedges_avg = sum(wedge_distances) / len(wedge_distances) if wedge_distances else 0
    benchmark_wedges_hcp23 = 85.0  # Benchmark típico HCP 23

    # Calcular percentil (más distancia = mejor)
    short_game_pct = min(100, max(0, int((player_wedges_avg / benchmark_wedges_hcp23) * 100)))
    short_game_rating = (
        "excellent" if short_game_pct >= 90 else
        "good" if short_game_pct >= 75 else
        "average" if short_game_pct >= 50 else
        "poor"
    )

    # 2. BALL SPEED (promedio driver)
    driver_df = self.flightscope_df[self.flightscope_df['palo'] == 'Dr']
    if len(driver_df) > 0:
        player_ball_speed = driver_df['vel_bola'].mean()
    else:
        player_ball_speed = 0

    benchmark_ball_speed_pga = 273.0  # km/h PGA Tour promedio

    ball_speed_pct = min(100, max(0, int((player_ball_speed / benchmark_ball_speed_pga) * 100)))
    ball_speed_rating = (
        "excellent" if ball_speed_pct >= 90 else
        "good" if ball_speed_pct >= 75 else
        "average" if ball_speed_pct >= 50 else
        "poor"
    )

    # 3. CONSISTENCY (CV de scores)
    all_scores = []
    for campo_data in self.tarjetas_data.values():
        for ronda in campo_data['rondas']:
            all_scores.append(ronda['total_ronda'])

    if len(all_scores) > 1:
        score_mean = sum(all_scores) / len(all_scores)
        score_std = (sum((s - score_mean)**2 for s in all_scores) / len(all_scores))**0.5
        player_cv = score_std / score_mean if score_mean > 0 else 0
    else:
        player_cv = 0

    benchmark_cv_hcp23 = 0.18  # CV típico HCP 23

    # Menor CV = mejor (invertir)
    consistency_pct = min(100, max(0, int((1 - player_cv / benchmark_cv_hcp23) * 100)))
    consistency_rating = (
        "excellent" if consistency_pct >= 90 else
        "good" if consistency_pct >= 75 else
        "average" if consistency_pct >= 50 else
        "poor"
    )

    # 4. ATTACK ANGLE (ángulo de ataque driver)
    if 'attack_angle_est' in self.dashboard_data.get('launch_metrics', {}).get('clubs', [{}])[0]:
        driver_launch = next(
            (c for c in self.dashboard_data.get('launch_metrics', {}).get('clubs', [])
             if c.get('palo') == 'Dr'),
            {}
        )
        player_attack_angle = driver_launch.get('attack_angle_est', -2.5)
    else:
        player_attack_angle = -2.5  # Estimado

    optimal_attack_angle = -1.5  # Óptimo driver

    # Más cercano a óptimo = mejor
    attack_diff = abs(player_attack_angle - optimal_attack_angle)
    attack_angle_pct = min(100, max(0, int((1 - attack_diff / 5.0) * 100)))
    attack_rating = (
        "excellent" if attack_angle_pct >= 90 else
        "good" if attack_angle_pct >= 75 else
        "average" if attack_angle_pct >= 50 else
        "poor"
    )

    logger.success(f"Percentile gauges: Short Game={short_game_pct}%, Ball Speed={ball_speed_pct}%, "
                   f"Consistency={consistency_pct}%, Attack Angle={attack_angle_pct}%")

    return {
        'short_game': {
            'value': short_game_pct,
            'player_avg': round(player_wedges_avg, 1),
            'benchmark_avg': benchmark_wedges_hcp23,
            'rating': short_game_rating
        },
        'ball_speed': {
            'value': ball_speed_pct,
            'player_avg': round(player_ball_speed, 1),
            'benchmark_avg': benchmark_ball_speed_pga,
            'rating': ball_speed_rating
        },
        'consistency': {
            'value': consistency_pct,
            'player_cv': round(player_cv, 3),
            'benchmark_cv': benchmark_cv_hcp23,
            'rating': consistency_rating
        },
        'attack_angle': {
            'value': attack_angle_pct,
            'player_avg': round(player_attack_angle, 1),
            'benchmark_avg': optimal_attack_angle,
            'rating': attack_rating
        }
    }
```

**Criterios de aceptación:**
- [ ] 4 percentiles calculados (short_game, ball_speed, consistency, attack_angle)
- [ ] Valores entre 0-100
- [ ] Ratings asignados (excellent/good/average/poor)
- [ ] Comparaciones vs benchmarks correctas
- [ ] Dashboard HTML muestra 4 doughnut gauges

---

### ✅ TASK 9.3: `calculate_hcp_trajectory()` - COMPLETADO

**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Media
**Tiempo real:** 4 horas (incluyendo suavizado y fixes)
**Tab:** 1 (Mi Identidad)
**Chart ID:** `hcpTrajectoryChart`
**Línea Backend:** 2085-2211
**Línea Frontend:** 15807-15926
**Fecha completado:** 2026-02-08

**Descripción:**
Genera datos de handicap real histórico + proyección futura con plan de mejora.

**Output esperado:**
```json
{
  "hcp_trajectory": {
    "historical": {
      "labels": ["Mar 2024", "Apr 2024", ..., "Dec 2025"],
      "values": [32.0, 30.5, 28.2, ..., 23.2]
    },
    "projection": {
      "labels": ["Jan 2026", "Feb 2026", ..., "Jun 2026"],
      "values": [22.5, 21.8, 21.0, 20.5, 19.8, 19.2],
      "confidence_low": [23.0, 22.5, 22.0, 21.5, 21.0, 20.5],
      "confidence_high": [22.0, 21.0, 20.0, 19.5, 18.5, 18.0]
    },
    "milestones": [
      {"month": "Apr 2026", "hcp": 20.0, "label": "Sub-20 Goal"}
    ],
    "current": 23.2,
    "target": 19.0,
    "improvement_rate": -0.5  // Puntos/mes
  }
}
```

**Algoritmo:**
```python
def calculate_hcp_trajectory(self):
    """
    Calcula trayectoria histórica de handicap + proyección.
    Usa regresión lineal para proyectar mejora futura.
    """
    logger.info("Calculating HCP trajectory (historical + projection)")

    import numpy as np
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta

    # Extraer todas las rondas con fecha y score
    all_rounds = []
    for campo_data in self.tarjetas_data.values():
        for ronda in campo_data['rondas']:
            all_rounds.append({
                'fecha': datetime.strptime(ronda['fecha'], '%Y-%m-%d'),
                'score': ronda['total_ronda']
            })

    # Ordenar por fecha
    all_rounds.sort(key=lambda x: x['fecha'])

    if len(all_rounds) < 5:
        logger.warning("Insufficient data for HCP trajectory")
        return {}

    # Calcular HCP estimado por ronda (simplificado)
    # HCP = (score - course_rating) * 113 / slope
    # Asumimos course rating = 72, slope = 113
    course_rating = 72
    slope = 113

    hcp_by_month = {}

    for ronda in all_rounds:
        month_key = ronda['fecha'].strftime('%Y-%m')
        differential = ((ronda['score'] - course_rating) * 113 / slope)

        if month_key not in hcp_by_month:
            hcp_by_month[month_key] = []

        hcp_by_month[month_key].append(differential)

    # Promediar por mes
    historical_labels = []
    historical_values = []

    for month_key in sorted(hcp_by_month.keys()):
        diffs = hcp_by_month[month_key]
        # Handicap = promedio de mejores 8 de últimas 20
        # Simplificado: promedio de ese mes
        hcp_est = sum(diffs) / len(diffs)

        historical_labels.append(datetime.strptime(month_key, '%Y-%m').strftime('%b %Y'))
        historical_values.append(round(hcp_est, 1))

    # Calcular tasa de mejora (regresión lineal)
    if len(historical_values) >= 3:
        x = np.arange(len(historical_values))
        y = np.array(historical_values)

        # Regresión lineal simple
        slope_fit = np.polyfit(x, y, 1)[0]
        improvement_rate = slope_fit
    else:
        improvement_rate = -0.5  # Default

    # Proyección futura (6 meses)
    last_month = datetime.strptime(sorted(hcp_by_month.keys())[-1], '%Y-%m')
    projection_labels = []
    projection_values = []
    projection_conf_low = []
    projection_conf_high = []

    current_hcp = historical_values[-1]

    for i in range(1, 7):  # 6 meses
        future_month = last_month + relativedelta(months=i)
        projection_labels.append(future_month.strftime('%b %Y'))

        # Proyección lineal
        projected_hcp = current_hcp + (improvement_rate * i)
        projection_values.append(round(projected_hcp, 1))

        # Bandas de confianza (±1 punto)
        projection_conf_low.append(round(projected_hcp + 0.5, 1))
        projection_conf_high.append(round(projected_hcp - 0.5, 1))

    # Milestone: Sub-20
    milestones = []
    for i, hcp in enumerate(projection_values):
        if hcp <= 20.0:
            milestones.append({
                'month': projection_labels[i],
                'hcp': 20.0,
                'label': 'Sub-20 Goal'
            })
            break

    logger.success(f"HCP trajectory: {len(historical_values)} historical months, "
                   f"current={current_hcp:.1f}, target=19.0, rate={improvement_rate:.2f}/mes")

    return {
        'historical': {
            'labels': historical_labels,
            'values': historical_values
        },
        'projection': {
            'labels': projection_labels,
            'values': projection_values,
            'confidence_low': projection_conf_low,
            'confidence_high': projection_conf_high
        },
        'milestones': milestones,
        'current': round(current_hcp, 1),
        'target': 19.0,
        'improvement_rate': round(improvement_rate, 2)
    }
```

**Criterios de aceptación:**
- [x] Historical data con meses y HCP estimado (18 meses, media móvil 3 meses)
- [x] Projection 6 meses con bandas de confianza (regresión lineal)
- [x] Milestones identificados (Sub-20 en Abril 2026)
- [x] Improvement rate calculado (-0.72 puntos/mes)
- [x] Dashboard HTML muestra line chart con proyección (dinámico desde JSON)

**Resultado real:**
- 18 meses históricos con suavizado (Apr 2024 - Dec 2025)
- Proyección 6 meses (Jan - Jun 2026)
- HCP actual: 22.5, Target: 19.0
- Milestone: Sub-20 alcanzable en Abril 2026
- Chart 100% dinámico, eje Y corregido (36 arriba, 18 abajo)

---

### 🟡 TASK 9.4-9.8: Evolution Charts (Tab 2)

**TASK 9.4:** `calculate_temporal_long_game()`
**TASK 9.5:** `calculate_irons_evolution()`
**TASK 9.6:** `calculate_wedges_evolution()`
**TASK 9.7:** `calculate_attack_angle_evolution()`
**TASK 9.8:** `calculate_smash_factor_evolution()`

**Tiempo total:** 8 horas (estas 5 funciones son similares)

**Descripción general:**
Extraer evolución temporal mensual de:
- Long Game (Driver, 3W, Hybrid)
- Irons (5i-9i)
- Wedges (PW, GW, SW)
- Attack Angle promedio por mes
- Smash Factor promedio por mes

**Output pattern (todos similares):**
```json
{
  "temporal_long_game": {
    "labels": ["Jan 2024", "Feb 2024", ...],
    "driver": [210, 212, 215, ...],
    "3wood": [190, 192, 195, ...],
    "hybrid": [175, 178, 180, ...]
  }
}
```

**Algoritmo compartido:**
```python
def calculate_temporal_evolution_by_category(self, palos, category_name):
    """
    Template genérico para evolution charts.

    Args:
        palos: Lista de códigos de palos ['Dr', '3W', 'Hyb']
        category_name: Nombre para logging

    Returns:
        dict: {labels: [...], palo1: [...], palo2: [...]}
    """
    logger.info(f"Calculating temporal evolution: {category_name}")

    from datetime import datetime
    from collections import defaultdict

    # Agrupar shots por mes y palo
    monthly_data = defaultdict(lambda: defaultdict(list))

    for _, shot in self.flightscope_df.iterrows():
        if 'fecha_shot' not in shot or pd.isna(shot['fecha_shot']):
            continue

        palo = shot['palo']
        if palo not in palos:
            continue

        fecha = datetime.strptime(str(shot['fecha_shot']), '%Y-%m-%d')
        month_key = fecha.strftime('%Y-%m')

        distance = shot['vuelo_act']
        monthly_data[month_key][palo].append(distance)

    # Promediar por mes
    sorted_months = sorted(monthly_data.keys())
    labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in sorted_months]

    result = {'labels': labels}

    for palo in palos:
        palo_values = []
        for month in sorted_months:
            distances = monthly_data[month].get(palo, [])
            avg_dist = sum(distances) / len(distances) if distances else None
            palo_values.append(round(avg_dist, 1) if avg_dist else None)

        result[palo] = palo_values

    logger.success(f"Temporal {category_name}: {len(labels)} months, {len(palos)} clubs")
    return result

# Implementaciones específicas:
def calculate_temporal_long_game(self):
    return self.calculate_temporal_evolution_by_category(
        ['Dr', '3W', 'Hyb'],
        'Long Game'
    )

def calculate_irons_evolution(self):
    return self.calculate_temporal_evolution_by_category(
        ['5i', '6i', '7i', '8i', '9i'],
        'Irons'
    )

def calculate_wedges_evolution(self):
    return self.calculate_temporal_evolution_by_category(
        ['PW', 'GW 52', 'SW 58'],
        'Wedges'
    )

def calculate_attack_angle_evolution(self):
    """Attack angle promedio por mes (driver solo)."""
    # Similar pero usando 'attack_angle_est' en lugar de 'vuelo_act'
    pass

def calculate_smash_factor_evolution(self):
    """Smash factor promedio por mes (todos los palos)."""
    # Similar pero calculando smash = ball_speed / club_speed
    pass
```

**Criterios de aceptación (por función):**
- [ ] Labels con meses cronológicos
- [ ] Datos por palo con valores mensuales
- [ ] None para meses sin datos
- [ ] Dashboard HTML muestra line charts

---

## 📊 RESULTADO SPRINT 9

**Al completar Sprint 9:**
- ✅ 8 funciones implementadas
- ✅ 11 charts dinámicos (4 gauges + 7 evolution)
- ✅ **Total: 27/61 charts (44.3%)**
- ✅ Tabs 1-2 mayormente dinámicos

---

## 📅 SPRINT 10: CAMPOS (Tab 3)

**Duración:** 2 semanas
**Objetivo:** Dinamizar Tab 3 (Mis Campos)
**Funciones:** 9
**Charts impactados:** 9
**Resultado esperado:** 36/61 charts (59.0%)

---

### TASK 10.1: `calculate_campo_performance()`

**Descripción:** Performance por campo (mejor/promedio/peor score por cada uno de los 12 campos)

**Output:**
```json
{
  "campo_performance": {
    "Marina Golf": {
      "best": 88,
      "average": 92.5,
      "worst": 98,
      "rounds": 15
    },
    // ... 11 campos más
  }
}
```

---

### TASK 10.2: `calculate_hcp_evolution_rfeg()`

**Descripción:** Handicap oficial RFEG histórico (extraer de archivo externo si existe)

---

### TASK 10.3: `calculate_scoring_zones_by_course()`

**Descripción:** Zonas de scoring por campo (birdie rate, par rate, bogey+ rate)

---

### TASK 10.4: `calculate_volatility_index()`

**Descripción:** Índice de volatilidad por quarter

---

### TASK 10.5: `calculate_estado_forma()`

**Descripción:** Estado de forma mes a mes (últimos 12 meses)

---

### TASK 10.6: `calculate_hcp_curve_position()`

**Descripción:** Distribución de rondas vs curva normal

---

### TASK 10.7: `calculate_prediction_model()`

**Descripción:** Predicción de próximo score usando regresión

---

### TASK 10.8: `calculate_roi_practice()`

**Descripción:** ROI de frecuencia de práctica vs mejora

---

### TASK 10.9: `calculate_differential_distribution()`

**Descripción:** Distribución de differentials (doughnut chart)

---

## 📊 RESULTADO SPRINT 10

**Al completar Sprint 10:**
- ✅ 9 funciones implementadas
- ✅ 9 charts dinámicos
- ✅ **Total: 36/61 charts (59.0%)**
- ✅ Tab 3 completamente dinámico

---

## 📅 SPRINT 11: DEEP ANALYSIS (Tab 5)

**Duración:** 2 semanas
**Objetivo:** Dinamizar análisis profundos
**Funciones:** 8
**Charts impactados:** 8
**Resultado esperado:** 44/61 charts (72.1%)

---

### TASK 11.1: `calculate_shot_zones_heatmap()`

**Descripción:** Heat map de donde caen los shots (scatter plot con densidad)

---

### TASK 11.2: `calculate_scoring_probability()`

**Descripción:** Probabilidad de birdie/par/bogey según distancia al hoyo

---

### TASK 11.3: `calculate_swing_dna()`

**Descripción:** Swing DNA fingerprint (radar 12 dimensiones)

---

### TASK 11.4: `calculate_quick_wins_matrix()`

**Descripción:** Matrix dificultad vs impacto (bubble chart)

---

### TASK 11.5: `calculate_club_distance_comparison()`

**Descripción:** Comparación distancias vs benchmarks (PGA/HCP15/HCP23)

---

### TASK 11.6: `calculate_comfort_zones()`

**Descripción:** Comfort zones analysis (distancias donde mejor juega)

---

### TASK 11.7: `calculate_tempo_analysis()`

**Descripción:** Tempo backswing/downswing vs PGA

---

### TASK 11.8: `calculate_strokes_gained()`

**Descripción:** Strokes gained vs HCP 15 por categoría

---

## 📊 RESULTADO SPRINT 11

**Al completar Sprint 11:**
- ✅ 8 funciones implementadas
- ✅ 8 charts dinámicos
- ✅ **Total: 44/61 charts (72.1%)**
- ✅ Tab 5 mayoría dinámico

---

## 📅 SPRINT 12: ESTRATEGIA + FINALES (Tab 6 + Restantes)

**Duración:** 1 semana
**Objetivo:** Completar charts finales y optimización
**Funciones:** 5
**Charts impactados:** 12
**Resultado esperado:** 56/61 charts (91.8%)

---

### TASK 12.1: `calculate_six_month_projection()`

**Descripción:** Proyección HCP y scores 6 meses

---

### TASK 12.2: `calculate_swot_matrix()`

**Descripción:** SWOT analysis automático (Strengths/Weaknesses/Opportunities/Threats)

---

### TASK 12.3: `calculate_benchmark_radar()`

**Descripción:** Benchmark comparison radar vs PGA/HCP15

---

### TASK 12.4: `calculate_roi_plan()`

**Descripción:** ROI de plan de mejora propuesto

---

### TASK 12.5: Optimización Final

**Tareas:**
- Code cleanup y refactoring
- Performance optimization
- Documentation update
- Full testing suite
- Final validation

---

## 📊 RESULTADO FINAL

**Al completar Sprint 12:**
- ✅ 30 funciones nuevas implementadas
- ✅ **52 funciones backend total**
- ✅ **56/61 charts dinámicos (91.8%)**
- ✅ 5 charts quedan hardcoded (por falta de datos o complejidad)

**Charts que quedarán hardcoded (5):**
- Algunos charts de Tab 5 que requieren datos externos
- Charts de tempo/swing que requieren sensores
- Charts predictivos muy complejos

---

## 📅 TIMELINE COMPLETO

| Sprint | Semanas | Funciones | Charts Nuevos | Total Charts | % Completado |
|--------|---------|-----------|---------------|--------------|--------------|
| **Sprints 1-8** | *(completado)* | 22 | 16 | 16/61 | 26.2% |
| **Sprint 9** | 2 | 8 | 11 | 27/61 | 44.3% |
| **Sprint 10** | 2 | 9 | 9 | 36/61 | 59.0% |
| **Sprint 11** | 2 | 8 | 8 | 44/61 | 72.1% |
| **Sprint 12** | 1 | 5 | 12 | **56/61** | **91.8%** |
| **TOTAL V2** | **7 semanas** | **30** | **40** | **56/61** | **91.8%** |

---

## ✅ DEFINITION OF DONE

### Por Función
- [ ] Código implementado y funcional
- [ ] Docstring completo
- [ ] Unit test pasando
- [ ] Integrado en `generate_dashboard_data()`
- [ ] JSON generado correctamente
- [ ] Dashboard HTML renderiza sin errores

### Por Sprint
- [ ] Todas las funciones del sprint completadas
- [ ] Integration tests pasando
- [ ] Dashboard HTML validado manualmente
- [ ] Sin regresiones en funciones anteriores
- [ ] Performance aceptable (< 5s ejecución total)
- [ ] JSON size < 200 KB

### Global (Sprint 12)
- [ ] 56/61 charts dinámicos (91.8%)
- [ ] JSON < 200 KB
- [ ] Ejecución < 5 segundos
- [ ] 0 errores JavaScript en consola
- [ ] Tests > 95% passing
- [ ] Documentation actualizada
- [ ] GitHub Pages deployado
- [ ] Cliente satisfecho

---

## 🔧 WORKFLOW DE DESARROLLO

```
1. Leer spec de TASK en este documento
2. Implementar función en generate_dashboard_data.py
3. Añadir a generate_dashboard_data() orchestrator
4. Regenerar JSON: python generate_dashboard_data.py
5. Verificar JSON contiene nueva sección
6. Abrir dashboard HTML: python start_dashboard_server.py
7. Verificar chart renderiza correctamente
8. Commit: git commit -m "feat: add [función]"
9. Repetir para siguiente TASK
10. Al completar sprint: git tag v4.{sprint}.0
```

---

## 📝 CONVENCIONES

### Naming
- Funciones: `calculate_[nombre]()` o `extract_[nombre]()`
- Secciones JSON: `snake_case`
- Chart IDs HTML: `camelCase`

### Commits
```
feat: add calculate_current_form_chart()
fix: correct percentile calculation in gauges
test: add unit tests for Sprint 9 functions
docs: update IMPLEMENTATION_PLAN_DETAILED_V2
```

### Testing
```python
# En tests/test_sprint9_validation.py
def test_current_form_chart():
    generator = DashboardDataGenerator(...)
    generator.load_data()
    result = generator.calculate_current_form_chart()

    assert 'labels' in result
    assert 'scores' in result
    assert len(result['scores']) == 20
    assert result['average'] > 0
```

---

## 📊 MÉTRICAS DE ÉXITO

### Objetivo Principal
**56/61 charts dinámicos (91.8%)**

### Métricas Secundarias
- Performance: Ejecución total < 5 segundos
- Size: JSON < 200 KB
- Quality: Tests > 95% passing
- UX: 0 errores en consola navegador

---

## 🚀 PRÓXIMO PASO

**Empezar Sprint 9 - TASK 9.1**

**Acción inmediata:**
```bash
cd C:\Users\alvar\Documents\AlvGolf
# Implementar calculate_current_form_chart() en generate_dashboard_data.py
# Línea: ~1850 (después de calculate_learning_curve)
```

---

**Última actualización:** 2026-02-07
**Próximo sprint:** Sprint 9
**Estado:** 🟡 Ready to start
**Autor:** Claude Sonnet 4.5 (Anthropic)
