# 🎯 Lista Priorizada de Integración Frontend

**Objetivo:** Integrar 35 funciones backend ya existentes en dashboard_dynamic.html para alcanzar 56/61 charts dinámicos (91.8%)

**Fecha:** 2026-02-08
**Estado actual:** 21/62 dinámicos (34%)
**Meta:** 56/62 dinámicos (91.8%)
**Funciones a integrar:** 35

---

## PRIORIDAD ALTA (15 funciones) - Sprint 13A

### Tab 1: Mi Identidad
1. **percentile_gauges** ✅ YA INTEGRADO
   - 4 gauges: short_game, ball_speed, consistency, attack_angle

### Tab 2: Evolución Temporal
2. **smash_factor_evolution** ⚡ ALTA
   - Chart: Line chart de Smash Factor por mes
   - Datos: driver_avg, 3wood_avg, irons_avg por 12 meses
   - HTML: Buscar "smashFactorEvolutionChart"

3. **club_distance_comparison** ⚡ ALTA
   - Chart: Bar chart distancias vs benchmarks
   - Datos: player_distance, vs_pga, vs_hcp15, vs_hcp23
   - HTML: Buscar "clubDistanceComparison"

### Tab 3: Mis Campos
4. **campo_performance** ⚡ ALTA
   - Chart: Bar chart por campo
   - Datos: avg_score, best_score, rounds, difficulty_rating
   - HTML: Buscar "campoPerfChart"

5. **hcp_evolution_rfeg** ⚡ ALTA
   - Chart: Line chart HCP oficial RFEG
   - Datos: monthly HCP histórico
   - HTML: Buscar "hcpEvolutionChart"

6. **differential_distribution** ⚡ ALTA
   - Chart: Histogram/Bar de differentials
   - Datos: bins con counts, mean, median
   - HTML: Buscar "diffDistChart"

7. **volatility_index** ⚡ ALTA
   - Chart: Line chart volatilidad trimestral
   - Datos: avg_score, std_dev, coefficient_variation
   - HTML: Buscar "volatilityChart"

8. **estado_forma** ⚡ ALTA
   - Chart: Line chart estado mes a mes
   - Datos: avg_score, form_status, vs_baseline
   - HTML: Buscar "estadoFormaChart"

9. **hcp_curve_position** ⚡ ALTA
   - Chart: Histogram distribución scores
   - Datos: bins, counts, curve normal
   - HTML: Buscar "hcpCurveChart"

10. **prediction_model** ⚡ ALTA
    - Chart: Line chart predicción
    - Datos: historical + predicted scores
    - HTML: Buscar "predictionChart"

11. **scoring_zones_by_course** ⚡ ALTA
    - Chart: Stacked bar por campo
    - Datos: birdies, pars, bogeys rates
    - HTML: Buscar "scoringZonesChart"

### Tab 5: Análisis Profundo
12. **shot_zones_heatmap** ⚡ ALTA
    - Chart: Scatter plot densidad
    - Datos: x, y coordinates por club
    - HTML: Buscar "shotZonesChart"

13. **comfort_zones** ⚡ ALTA
    - Chart: Bar chart zonas distancia
    - Datos: avg_score, gir_percentage por rango
    - HTML: Buscar "comfortZonesChart"

14. **scoring_probability** ⚡ ALTA
    - Chart: Line chart probabilidades
    - Datos: birdie/par/bogey rates por distancia
    - HTML: Buscar "scoringProbChart"

15. **swing_dna** ⚡ ALTA
    - Chart: Radar multi-dimensional
    - Datos: 12 dimensiones skill profile
    - HTML: Buscar "swingDNAChart"

---

## PRIORIDAD MEDIA (12 funciones) - Sprint 13B

### Tab 5: Análisis Profundo
16. **quick_wins_matrix** 🟡 MEDIA
    - Chart: Bubble chart oportunidades
    - Datos: difficulty vs impact matrix
    - HTML: Buscar "quickWinsChart"

17. **strokes_gained** 🟡 MEDIA
    - Chart: Bar chart por categoría
    - Datos: driving, approach, short_game, putting
    - HTML: Buscar "strokesGainedChart"

18. **tempo_analysis** 🟡 MEDIA
    - Chart: Bar chart tempo
    - Datos: backswing, downswing por club
    - HTML: Buscar "tempoChart"

### Tab 6: Estrategia & Acción
19. **six_month_projection** 🟡 MEDIA
    - Chart: Line chart proyección HCP + Score
    - Datos: 6 meses futuro con confidence intervals
    - HTML: Buscar "sixMonthProjection"

20. **swot_matrix** 🟡 MEDIA
    - Chart: Radar 4 cuadrantes
    - Datos: strengths, weaknesses, opportunities, threats
    - HTML: Buscar "swotMatrix"

21. **benchmark_radar** 🟡 MEDIA
    - Chart: Radar comparison
    - Datos: player vs PGA vs HCP15 vs HCP23
    - HTML: Buscar "benchmarkComparisonRadar"

22. **roi_plan** 🟡 MEDIA
    - Chart: Bar chart + table
    - Datos: action items con ROI scores
    - HTML: Buscar "roiPlanChart"

### Tab 3: Mis Campos
23. **roi_practice** 🟡 MEDIA
    - Chart: Scatter ROI práctica
    - Datos: practice_hours vs improvement
    - HTML: Buscar "roiPracticeChart"

### Tab 2: Evolución Temporal
24. **learning_curve** 🟡 MEDIA (ya referido parcialmente)
    - Chart: Line chart aprendizaje
    - Datos: long_game, mid_game, short_game trend
    - HTML: Buscar "learningCurveChart"

25. **milestone_achievements** 🟡 MEDIA
    - Chart: Timeline milestones
    - Datos: achievements con fechas
    - HTML: Buscar "milestonesChart"

26. **consistency_benchmarks** 🟡 MEDIA
    - Chart: Bar comparison
    - Datos: player vs benchmarks consistency
    - HTML: Buscar referencias

27. **launch_metrics** 🟡 MEDIA
    - Chart: Bar launch angles
    - Datos: launch_angle, peak_height por club
    - HTML: Buscar "launchAngleChart"

---

## PRIORIDAD BAJA (8 funciones) - Sprint 13C

### Charts adicionales/redundantes
28. **dispersion_analysis** 🔵 BAJA
    - Datos: Ya usado en dispersion_by_club
    - Posible: Chart resumen dispersion

29. **best_worst_rounds** 🔵 BAJA
    - Chart: Table/List top/bottom rounds
    - HTML: Buscar referencias

30. **club_gaps** 🔵 BAJA
    - Chart: Line gaps entre clubs
    - Ya parcialmente en club_distance_comparison

31. **temporal_evolution** 🔵 BAJA
    - Similar a temporal_long_game
    - Verificar si es legacy

32. **momentum_indicators** ✅ YA INTEGRADO
    - SMA-5, SMA-10

33. **quarterly_scoring** ✅ YA INTEGRADO
    - Quarterly trends

34. **monthly_volatility** ✅ YA INTEGRADO
    - Monthly scores

35. **trajectory_data** ✅ YA INTEGRADO
    - Launch trajectory

---

## RESUMEN

### Por Prioridad
- ⚡ **ALTA (15):** Impacto visual inmediato, datos completos
- 🟡 **MEDIA (12):** Análisis avanzado, estrategia
- 🔵 **BAJA (8):** Redundantes o ya integrados

### Por Sprint
- **Sprint 13A (Semana 1):** 15 funciones ALTA prioridad → 36/62 (58%)
- **Sprint 13B (Semana 2):** 12 funciones MEDIA prioridad → 48/62 (77%)
- **Sprint 13C (Semana 3):** 8 funciones BAJA prioridad → 56/62 (91.8%) ✅

### Target Final
- **Meta:** 56/62 dinámicos (91.8%)
- **Charts hardcoded permanentes:** 6 (por falta datos o complejidad extrema)

---

## METODOLOGÍA DE INTEGRACIÓN

Para cada función:
1. Buscar el chart ID en dashboard_dynamic.html
2. Localizar el `new Chart()` con datos hardcoded
3. Reemplazar `labels: [...]` por `labels: dashboardData.{key}.labels`
4. Reemplazar `data: [...]` por `data: dashboardData.{key}.data`
5. Añadir fallback: `labels: dashboardData.{key}?.labels || [...]`
6. Verificar renderizado en navegador
7. Test responsive (mobile)
8. Commit cambios

### Pattern Example

**ANTES (Hardcoded):**
```javascript
new Chart(document.getElementById('hcpEvolutionChart'), {
    type: 'line',
    data: {
        labels: ['Mar 2024', 'Apr 2024', ...],
        datasets: [{
            label: 'HCP Oficial RFEG',
            data: [27.5, 27.2, 26.8, ...]
        }]
    }
});
```

**DESPUÉS (Dinámico):**
```javascript
new Chart(document.getElementById('hcpEvolutionChart'), {
    type: 'line',
    data: {
        labels: dashboardData.hcp_evolution_rfeg?.labels || ['Mar 2024', 'Apr 2024'],
        datasets: [{
            label: 'HCP Oficial RFEG',
            data: dashboardData.hcp_evolution_rfeg?.values || [27.5, 27.2]
        }]
    }
});
```

---

## CRONOGRAMA

**Semana 1 (Sprint 13A):**
- Día 1-2: Integrar funciones 2-5 (4 charts)
- Día 3-4: Integrar funciones 6-10 (5 charts)
- Día 5: Integrar funciones 11-15 (5 charts)
- Día 6-7: Testing y ajustes

**Semana 2 (Sprint 13B):**
- Día 1-2: Integrar funciones 16-20 (5 charts)
- Día 3-4: Integrar funciones 21-24 (4 charts)
- Día 5: Integrar funciones 25-27 (3 charts)
- Día 6-7: Testing y ajustes

**Semana 3 (Sprint 13C + Optimización):**
- Día 1-2: Integrar funciones 28-35 (8 charts)
- Día 3-4: Optimización final (TASK 12.5)
- Día 5-7: Testing completo, documentación, deploy

**Total:** 3 semanas para alcanzar 91.8% dinamización

---

## NOTAS

- Funciones ya integradas marcadas con ✅
- Algunas funciones pueden estar parcialmente integradas
- Verificar cada chart individualmente antes de declarar "completado"
- Priorizar tabs más visibles (Tab 1, Tab 2, Tab 3)
