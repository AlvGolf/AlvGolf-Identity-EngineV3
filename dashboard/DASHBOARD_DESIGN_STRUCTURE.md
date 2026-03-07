# Dashboard Design Structure v3.2.0

**Fecha:** 2026-03-07
**Estado:** Glassmorphism completo en 6 tabs
**Archivo:** `dashboard_dynamic.html` (~20,200 lineas)

---

## 1. Design System

### Glassmorphism Tokens (aplicados globalmente)

| Token | Valor | Uso |
|-------|-------|-----|
| Container bg | `rgba(255,255,255,0.04)` | Fondos de seccion |
| Container border | `1px solid rgba(255,255,255,0.08)` | Bordes de seccion |
| Container radius | `14px` | Esquinas de seccion |
| Card bg | `rgba(255,255,255,0.04)` | Fondos de tarjeta |
| Card border | `1px solid rgba(255,255,255,0.08)` | Bordes de tarjeta |
| Card accent | `border-top: 2px solid [color]` | Acento superior |
| Card radius | `8px` | Esquinas de tarjeta |
| Inner box bg | `rgba(255,255,255,0.03)` | Cajas interiores |
| Inner box accent | `border-left: 3px solid [color]` | Acento lateral |
| Label | `9px uppercase letter-spacing 1.5px #9a9e94 700` | Etiquetas |
| Value | `2-2.6em font-weight 900` (sin text-shadow) | Valores KPI |

### Colores de Acento

| Color | Hex | Uso |
|-------|-----|-----|
| Azul | `#4A9FD8` | Primary, diagnostico, conclusiones AI |
| Verde | `#5ABF8F` | Exito, fortalezas, short game |
| Oro | `#D4B55A` | Advertencia, mid game, planes |
| Rojo | `#E88B7A` | Critico, debilidades, long game |
| Background | `#0F2027` → `#203A43` | Gradiente de fondo |
| Texto | `#E8E8E8` | Texto principal |

### CSS Utility Classes (Paso 0)

| Clase | Proposito |
|-------|-----------|
| `.text-label` | Labels 9px uppercase |
| `.kpi-card` (+ `--blue/--green/--gold/--red`) | Tarjeta KPI con acento |
| `.kpi-value` | Valor grande |
| `.kpi-sub` | Subtexto KPI |
| `.quick-nav-link` | Link de navegacion rapida |
| `.ai-conclusion` | Conclusion generada por IA |
| `.inner-box` (+ `--blue/--green/--gold/--red`) | Caja interior con acento |

### Card System (4 niveles)

```
card-hero      → Tarjeta principal (mayor prominencia)
  card-section → Seccion dentro de hero
    card-detail → Detalle con accent color (green/blue/gold/red/neutral)
      card-nested → Elemento anidado
```

---

## 2. Quick Menu Pattern

Todos los tabs (2-6) usan el mismo patron de quick menu:

```html
<div class="quick-nav-header" style="background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 15px; padding: 30px;">

    <!-- Sub-grupo -->
    <div style="margin-bottom: 25px; padding: 20px;
                background: rgba(R,G,B,0.05); border-radius: 10px;
                border-left: 4px solid #COLOR;">
        <h4 style="color: #COLOR;">TITULO GRUPO</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px;">
            <a class="quick-nav-link" onclick="scrollToSection('id')">* Seccion</a>
        </div>
    </div>
</div>
```

---

## 3. Tab Structure

### Tab 1: Mi Identidad (8 secciones)
**Glassmorphism:** v3.1.1 (2026-03-04)

Secciones:
1. Header + Score Summary
2. Perfil del Jugador
3. Estado Actual de Forma
4. Percentiles vs Benchmarks
5. Trayectoria y Goals
6. Goal Banner
7. Highlight de Sesion
8. Recomendaciones Coaching

Radar: Chart.js (canvas `gi-scoring-radar`) con 3 datasets (Tu/PGA/HCP20)

---

### Tab 2: Evolucion Temporal (13 secciones)
**Glassmorphism:** v3.1.3 (2026-03-05)

Quick Menu: 4 sub-grupos
- Metricas Clave (5): Trayectoria RFEG, Mejores/Peores Rondas, Performance Trimestre, Volatilidad, Momentum
- Evolucion por Categoria (2): Irons 5-9, Wedges PW/GW/SW
- Proyeccion (3): Score & Consistencia, Progresion Consistencia, Comparativa Mejora
- AI Conclusions: quarterly_conclusion, volatility_conclusion

---

### Tab 3: Mis Campos (9 secciones)
**Glassmorphism:** v3.1.3 (2026-03-05)

Quick Menu: 3 sub-grupos
- Rendimiento (3): Trayectoria RFEG, Mejores Rondas, Performance Campo
- Analisis (3): Scoring, Consistencia, Estado de Forma
- Proyeccion (3): Proyeccion Rendimiento, Objetivos/Logros, Optimizacion Practica

---

### Tab 4: Bolsa de Palos (11 secciones)
**Glassmorphism:** v3.1.3 (2026-03-05)

Quick Menu: 3 sub-grupos
- Distancias (3): Rendimiento por Palo, Percentiles, Brechas
- Precision (4): Distribucion Direccional, Dispersion, Trayectoria, Smash Factor
- Rendimiento (4): Velocidad/Potencia, Burbujas, Performance Detallado, Matriz

---

### Tab 5: Analisis Profundo (14 secciones)
**Glassmorphism:** v3.2.0 (2026-03-07)
**Reorganizado:** Flujo logico Metricas→Analisis→Comparativas→Estrategia

Quick Menu: 4 sub-grupos
- Metricas (3): Curvas Aprendizaje, Strokes Gained, Tempo & Rhythm
- Analisis (4): Shot Zones, Swing DNA, Probabilidad Par/Birdie, Zonas Confort
- Comparativas vs PGA (5): Distancias, Dispersion, Radar 360, 8 Competencias, Waterfall
- Estrategia (2): Game Plan Simulator, Quick Wins

Orden de secciones (post-reorder):
1. `learning-curve` — Curvas de Aprendizaje
2. `strokes-gained` — Strokes Gained Simplified
3. `tempo-rhythm` — Tempo & Rhythm Analysis
4. `shot-zones` — Shot Zones Heatmap (KDE 200x250 + bilinear)
5. `swing-dna` — Swing DNA Fingerprint
6. `probabilidad-par-birdie` — Probabilidad de Par/Birdie
7. `zonas-confort` — Zonas de Confort
8. `distancias-comparativa` — Distancias Comparativa Triple
9. `dispersion-comparativa` — Dispersion Comparativa
10. `metricas-radar` — Radar 360 Dimensiones
11. `comparativa-8-competencias` — 8 Competencias vs PGA
12. `waterfall-analysis` — Analisis de Perdidas
13. `game-plan-simulator` — Game Plan Simulator
14. `quick-wins` — Quick Wins Calculator

Legacy sections (sin quick menu, al final):
- `launch-metrics` — Launch Metrics
- `dispersion-analysis` — Dispersion Analysis
- `consistency-benchmarks` — Consistency Benchmarks

---

### Tab 6: Estrategia & Accion (9 secciones)
**Glassmorphism:** v3.2.0 (2026-03-07)

Quick Menu: 4 sub-grupos
- Diagnostico (3): DAFO Completo, Matriz DAFO, Posicionamiento
- Estrategia (2): Estrategias Derivadas, Matriz Priorizacion
- Plan de Accion (3): Optimizacion Tecnica, Heatmap ROI, ROI Plan Mejora
- Conclusion (1): Conclusion & Proximos Pasos

Orden de secciones:
1. `dafo-completo` — Analisis DAFO Completo (4 cards: Fortalezas/Oportunidades/Debilidades/Amenazas)
2. `matriz-dafo` — Matriz DAFO Visual 2x2
3. `posicionamiento` — Posicionamiento vs PGA Tour vs HCP15
4. `estrategias-derivadas` — Estrategias Derivadas (FO/DA/FA/DO)
5. `matriz-priorizacion` — Matriz de Priorizacion (Quick Wins/Proyectos/Incrementales/Evitar)
6. `optimizacion-tecnica` — Optimizacion Tecnica (6 sub-secciones, ~700 lineas, la mas compleja)
7. `heatmap-roi` — Heatmap ROI por Palo
8. `roi-plan-mejora` — ROI Plan de Mejora (antes/despues)
9. `conclusion-final` — Conclusion & Proximos Pasos + Roadmap 12 Meses

---

## 4. Shot Zones Heatmap (Tab 5)

### Implementacion tecnica
- **Grid:** 200x250 celdas (alta resolucion)
- **KDE:** Gaussian splat por shot (sigma 8x10, kernel radius 24)
- **Interpolacion:** Bilinear sampling de density matrix
- **DPI:** canvas.width = CSS width * devicePixelRatio, ImageData a resolucion completa
- **Rendering:** putImageData (pixel a pixel), luego ctx.scale(dpr) para ejes

### Paleta termica
```
Densidad 0.00-0.01 → Fondo oscuro (15,32,39)
Densidad 0.01-0.20 → Azul oscuro → Cyan
Densidad 0.20-0.40 → Cyan → Verde
Densidad 0.40-0.60 → Verde → Amarillo
Densidad 0.60-0.80 → Amarillo → Naranja
Densidad 0.80-1.00 → Naranja → Rojo
```

### Filtros por categoria
```javascript
CLUB_CATEGORIES = {
    'long': ['Driver', 'Dr', '3 Wood', '3W', 'Hybrid', 'Hyb'],
    'mid':  ['5 Iron', '5i', '6 Iron', '6i', '7 Iron', '7i', '8 Iron', '8i', '9 Iron', '9i'],
    'short': ['PW', 'GW', 'SW', 'Gap Wedge', 'Sand Wedge']
}
```

---

## 5. AI Content Integration

### UXWriter Sections (12)
1. `hero_statement` → Tab 1
2. `dna_profile` → Tab 1
3. `stat_cards` → Tab 2
4. `chart_titles` → All tabs
5. `trend_narratives` → Tab 2
6. `course_cards` → Tab 3
7. `insight_boxes` → Tab 5
8. `club_cards` → Tab 4
9. `quick_wins` → Tab 6
10. `roi_cards` → Tab 6
11. `quarterly_conclusion` → Tab 2
12. `volatility_conclusion` → Tab 2

### AI Conclusion Style
- Texto: "Conclusion:" en `#4A9FD8`
- Fondo: `rgba(74,159,216,0.06)`
- Borde: `rgba(74,159,216,0.18)`
- Sin emoji, sin "IA"
- Clase CSS: `.ai-conclusion`

---

## 6. Responsive Breakpoints

| Breakpoint | Target |
|------------|--------|
| 1024px | Tablets |
| 768px | Small tablets |
| 480px | Phones |
| 375px | Small phones |
| 360px | iPhone SE |

---

## 7. Chart Dependencies

- **Chart.js** — 35 charts (line, bar, radar, scatter, bubble, doughnut)
- **html2pdf.js** — PDF export por tab
- **Canvas API** — Shot Zones heatmap (custom rendering)

---

## 8. Version History

| Version | Fecha | Cambios |
|---------|-------|---------|
| v3.2.0 | 2026-03-07 | Full Glassmorphism Tabs 1-6 + Tab 5/6 redesign + Shot Zones KDE |
| v3.1.3 | 2026-03-05 | Tab 2 redesign + CSS Paso 0 + Tab 3-4 glassmorphism |
| v3.1.1 | 2026-03-04 | Tab 1 glassmorphism + SVG→Chart.js radar |
| v3.0.9 | 2026-03-03 | Radar dedup + Card System v3.1 |
| v3.0.7 | 2026-03-02 | 100% Dynamic Dashboard (176 hardcodes → JSON) |
| v3.0.5 | 2026-02-25 | Identity Timeline + Scoring Engine |
| v3.0.0 | 2026-02-16 | Multi-Agent System (5 agents) |
