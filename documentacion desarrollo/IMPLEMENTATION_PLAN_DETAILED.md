# 📋 Plan de Implementación Detallado - AlvGolf Dashboard Backend

**🎉 ESTADO FINAL: ✅ PLAN COMPLETADO CON ÉXITO 🎉**

**Fecha creación:** 2026-02-03
**Fecha completado:** 2026-02-04
**Última actualización:** 2026-02-06
**Estrategia:** Opción C - Híbrida (Incremental con refactorización controlada)
**Metodología:** Sprints iterativos con testing continuo
**Resultado:** 100% completado - Sprints 1-8 finalizados + Documentación actualizada
**Estado:** 🟢 Producción Estable

---

## ✅ RESUMEN DE COMPLETITUD

| Sprint | Objetivo | Estado | Fecha Completado |
|--------|----------|--------|------------------|
| Sprint 1-2 | Base Calculations + Validation | ✅ | 2026-02-03 |
| Sprint 3 | Important Functions (4) | ✅ | 2026-02-03 |
| Sprint 4 | Testing Suite | ✅ | 2026-02-03 |
| Sprint 5 | Visual Improvements (4) | ✅ | 2026-02-03 |
| Sprint 6 | Trend Improvements (4) | ✅ | 2026-02-03 |
| Sprint 7 | Finalization | ✅ | 2026-02-03 |
| Sprint 8 | Dashboard Integration (12 viz) | ✅ | 2026-02-03 |
| **Bug Fixes** | Post-Integration (3 bugs) | ✅ | 2026-02-04 |
| **Documentation** | README + memory/ai updates | ✅ | 2026-02-06 |

**Total Secciones Implementadas:** 21 (Backend) + 12 (Frontend integradas)
**Proyecto Consolidado:** `C:\Users\alvar\Documents\AlvGolf\`
**Tests:** 98.3% passing (118/120)
**Performance:** 3.1s ejecución, 128 KB JSON

---

## 🚀 Workflow de Producción

### Uso Diario del Dashboard

```bash
# 1. Navegar al proyecto
cd C:\Users\alvar\Documents\AlvGolf

# 2. Regenerar datos (después de actualizar Excels)
python generate_dashboard_data.py  # 3.1 segundos

# 3. Iniciar servidor HTTP
python start_dashboard_server.py

# 4. Dashboard abre automáticamente
# URL: http://localhost:8000/dashboard_dynamic.html
```

### ⚠️ IMPORTANTE: Servidor HTTP Requerido

El dashboard requiere servidor HTTP debido a políticas CORS del navegador:

| Método | Protocolo | ¿Funciona? | Razón |
|--------|-----------|------------|-------|
| **Servidor HTTP** | `http://localhost:8000` | ✅ SÍ | Fetch de JSON permitido |
| **Doble clic** | `file:///C:/Users/...` | ❌ NO | Bloqueado por CORS |

**Conclusión:** El sistema mantiene la separación de datos (JSON) y presentación (HTML), lo que preserva la automatización completa del ETL. No hay forma de evitar el servidor HTTP sin perder esta arquitectura.

### Actualizar Datos Después de Nuevas Rondas

```bash
# 1. Actualizar Excel (TARJETAS_RECORRIDOS.xlsx)
# 2. Regenerar JSON
python generate_dashboard_data.py

# 3. Refrescar navegador (si servidor ya está corriendo)
Ctrl+F5  # Recarga sin caché
```

**Tiempo total:** < 1 minuto

---

## 📁 Estructura Final del Proyecto

```
C:\Users\alvar\Documents\AlvGolf/
├── 🎨 FRONTEND
│   ├── dashboard_dynamic.html         ✅ (16,373 líneas, v4.0.1)
│   ├── dashboard_loader.js            ✅ (6 KB)
│   └── start_dashboard_server.py      ✅ (Servidor HTTP)
│
├── 🐍 BACKEND
│   ├── generate_dashboard_data.py     ✅ (2,100+ líneas, v3.3.0)
│   └── data/raw/FlightScope-AP-Prov1.Next.xlsx
│
├── 📊 OUTPUT
│   └── output/dashboard_data.json     ✅ (128 KB)
│
├── 🧪 TESTS
│   ├── test_sprint3_validation.py     ✅ (36/37 PASS)
│   ├── test_sprint5_validation.py     ✅ (39/40 PASS)
│   └── test_sprint6_validation.py     ✅ (43/43 PASS)
│
├── 📚 DOCS
│   ├── README.md                      ✅ (Actualizado 2026-02-06)
│   ├── SPRINT_1-8_RESUMEN.md          ✅
│   └── DASHBOARD_INTEGRATION_GUIDE.md ✅
│
└── 🧠 MEMORY/AI
    ├── DASHBOARD_DATA_MAPPING.md      ✅ (Actualizado 2026-02-06)
    ├── GENERATE_DASHBOARD_ANALYSIS.md ✅ (Actualizado 2026-02-06)
    └── IMPLEMENTATION_PLAN_DETAILED.md ✅ (Este archivo)
```

**Dashboard Accesible:** `http://localhost:8000/dashboard_dynamic.html`

---

## 📝 PLAN ORIGINAL (Referencia Histórica)

---

## 🎯 OBJETIVO PRINCIPAL

Completar el backend `generate_dashboard_data.py` para que genere un JSON que alimente correctamente **TODOS los 54+ charts** del dashboard HTML sin modificar el frontend.

---

## 📊 ESTADO ACTUAL vs OBJETIVO

### Cobertura Actual
- **Player Stats:** 100% ✅
- **Overview Charts:** 29% ⚠️
- **Evolution Charts:** 38% ⚠️
- **Campos Charts:** 17% ⚠️
- **Performance Charts:** 5% ⚠️
- **Deep Analysis Charts:** 0% ❌

### Objetivo Final
- **Todas las categorías:** 100% ✅
- **54+ charts funcionales**
- **0 datos hardcodeados en HTML**
- **Dashboard completamente dinámico**

---

## 🏗️ ARQUITECTURA DE SPRINTS

```
Sprint 0: Preparación y Setup          (1 día)
├── Documentación
├── Configuración ambiente
└── Backup código actual

Sprint 1: Funciones Críticas            (3 días)  🔴 CRÍTICO
├── Dispersion scatter data
├── Merge club data
├── Club gaps
└── Temporal evolution fix

Sprint 2: Testing y Validación S1       (1 día)
├── Unit tests
├── Integration tests
└── Dashboard HTML validation

Sprint 3: Funciones Importantes         (3 días)  🟡 IMPORTANTE
├── Score history
├── Percentiles
├── Directional analysis
└── Bubble chart data

Sprint 4: Testing y Validación S3       (1 día)
├── Visual validation
└── Performance tests

Sprint 5: Mejoras Visuales              (2 días)  🟢 MEJORA
├── Player profile radar
├── Trajectory data
├── Best/worst rounds
└── Quarterly scoring

Sprint 6: Mejoras de Tendencias         (2 días)  🟢 MEJORA
├── Differential distribution
├── Monthly volatility
├── Recent momentum
├── Milestones detection
└── Learning curve

Sprint 7: Finalización y Pulido         (1 día)
├── Documentation update
├── Code cleanup
└── Final testing

TOTAL: 14 días (2 semanas laborales)
```

---

## 📦 BACKLOG COMPLETO DE FUNCIONES

### SPRINT 0: PREPARACIÓN

#### TASK 0.1: Crear Backup
**Complejidad:** Trivial
**Tiempo:** 10 min
**Descripción:** Backup del código actual antes de modificaciones

**Acciones:**
```bash
cp generate_dashboard_data.py generate_dashboard_data_backup_$(date +%Y%m%d).py
git add -A
git commit -m "Backup before dashboard backend refactoring"
```

---

#### TASK 0.2: Crear Módulo de Tests
**Complejidad:** Baja
**Tiempo:** 30 min
**Archivo:** `tests/test_dashboard_generator.py`

**Código base:**
```python
import pytest
from generate_dashboard_data import DashboardDataGenerator

@pytest.fixture
def generator():
    return DashboardDataGenerator(
        flightscope_path="data/raw/FlightScope-AP-Prov1.Next.xlsx",
        tarjetas_path="path/to/TARJETAS_RECORRIDOS.xlsx",
        output_path="tests/output/test_dashboard_data.json"
    )

def test_load_flightscope(generator):
    generator.load_flightscope_data()
    assert generator.flightscope_df is not None
    assert len(generator.flightscope_df) > 0

# ... más tests
```

---

#### TASK 0.3: Documentar Estructura JSON Objetivo
**Complejidad:** Baja
**Tiempo:** 20 min
**Archivo:** `docs/json_schema.md`

**Contenido:** Schema completo del JSON esperado por el dashboard

---

### SPRINT 1: FUNCIONES CRÍTICAS 🔴

#### TASK 1.1: `generate_dispersion_scatter_data()`
**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Alta
**Tiempo estimado:** 4 horas
**Dependencias:** Ninguna
**Archivo:** `generate_dashboard_data.py` línea ~500

**Especificación técnica:**

**Input:**
- `self.flightscope_df`: DataFrame con columnas ['palo', 'vuelo_act', 'lateral_vuelo']

**Output:**
```python
{
  "Dr": {
    "poor": [{"x": -30, "y": 205}, ...],      # 10-15 puntos
    "regular": [{"x": -15, "y": 210}, ...],   # 4-6 puntos
    "good": [{"x": -8, "y": 215}, ...],       # 4 puntos
    "excellent": [{"x": -3, "y": 220}, ...],  # 5 puntos
    "xMin": -35,
    "xMax": 30,
    "yMin": 200,
    "yMax": 225
  },
  # ... repetir para 11 palos
}
```

**Lógica de clasificación:**
```python
# Para cada shot:
carry_mean = palo_df['vuelo_act'].mean()
carry_std = palo_df['vuelo_act'].std()

if carry > carry_mean + 0.5 * carry_std and abs(lateral) < 5:
    → excellent
elif carry > carry_mean and abs(lateral) < 10:
    → good
elif carry > carry_mean - 0.5 * carry_std or abs(lateral) < 15:
    → regular
else:
    → poor
```

**Palos a procesar:**
```python
palo_codes = ['Dr', '3W', 'Hyb', '5i', '6i', '7i', '8i', '9i', 'PW', 'GW 52', 'SW 58']
```

**Algoritmo completo:**
```python
def generate_dispersion_scatter_data(self):
    """
    Genera scatter plot data para los 11 palos.

    Clasifica cada shot en 4 categorías de calidad:
    - excellent: muy bueno (carry alto, lateral bajo)
    - good: bueno (carry decente, lateral aceptable)
    - regular: promedio
    - poor: malo (carry bajo o lateral alto)

    Returns:
        dict: {palo_code: {poor, regular, good, excellent, xMin, xMax, yMin, yMax}}
    """
    logger.info("Generando dispersion scatter data para 11 palos")

    palo_codes = ['Dr', '3W', 'Hyb', '5i', '6i', '7i', '8i', '9i', 'PW', 'GW 52', 'SW 58']
    palo_name_map = {
        'Dr': 'Driver', '3W': '3Wood', 'Hyb': 'Hybrid',
        '5i': '5Iron', '6i': '6Iron', '7i': '7Iron',
        '8i': '8Iron', '9i': '9Iron', 'PW': 'PW',
        'GW 52': 'GW', 'SW 58': 'SW'
    }

    dispersion_data = {}

    for palo_code in palo_codes:
        # Filtrar shots del palo
        palo_df = self.flightscope_df[self.flightscope_df['palo'] == palo_code].copy()

        if len(palo_df) == 0:
            logger.warning(f"No hay datos para {palo_code}, skipping...")
            continue

        # Parsear lateral (I = izquierda negativo, D = derecha positivo)
        def parse_lateral(valor):
            if pd.isna(valor):
                return 0
            valor_str = str(valor)
            try:
                num = float(valor_str.replace('I', '').replace('D', '').replace('C', '').strip())
                if 'D' in valor_str:
                    return num  # Derecha es positivo
                else:
                    return -num  # Izquierda es negativo
            except:
                return 0

        palo_df['lateral_m'] = palo_df['lateral_vuelo'].apply(parse_lateral)

        # Calcular estadísticas para clasificación
        carry_mean = palo_df['vuelo_act'].mean()
        carry_std = palo_df['vuelo_act'].std()

        # Inicializar categorías
        poor_shots = []
        regular_shots = []
        good_shots = []
        excellent_shots = []

        # Clasificar cada shot
        for _, shot in palo_df.iterrows():
            carry = shot['vuelo_act']
            lateral = shot['lateral_m']

            point = {'x': round(lateral, 1), 'y': round(carry, 1)}

            # Clasificación por calidad
            if carry > carry_mean + 0.5 * carry_std and abs(lateral) < 5:
                excellent_shots.append(point)
            elif carry > carry_mean and abs(lateral) < 10:
                good_shots.append(point)
            elif carry > carry_mean - 0.5 * carry_std or abs(lateral) < 15:
                regular_shots.append(point)
            else:
                poor_shots.append(point)

        # Calcular límites de los ejes (con margen)
        all_laterals = palo_df['lateral_m'].tolist()
        all_carries = palo_df['vuelo_act'].tolist()

        lateral_min = min(all_laterals)
        lateral_max = max(all_laterals)
        carry_min = min(all_carries)
        carry_max = max(all_carries)

        # Agregar margen de 10%
        lateral_range = lateral_max - lateral_min
        carry_range = carry_max - carry_min

        dispersion_data[palo_name_map.get(palo_code, palo_code)] = {
            'poor': poor_shots,
            'regular': regular_shots,
            'good': good_shots,
            'excellent': excellent_shots,
            'xMin': round(lateral_min - lateral_range * 0.1, 1),
            'xMax': round(lateral_max + lateral_range * 0.1, 1),
            'yMin': round(carry_min - carry_range * 0.1, 1),
            'yMax': round(carry_max + carry_range * 0.1, 1)
        }

        logger.debug(f"{palo_code}: {len(poor_shots)} poor, {len(regular_shots)} regular, "
                     f"{len(good_shots)} good, {len(excellent_shots)} excellent")

    logger.success(f"Dispersion scatter data generada para {len(dispersion_data)} palos")
    return dispersion_data
```

**Criterios de aceptación:**
- [ ] Genera datos para los 11 palos
- [ ] Cada palo tiene 4 categorías (poor, regular, good, excellent)
- [ ] Al menos 1 punto en cada categoría (si hay suficientes shots)
- [ ] Límites xMin, xMax, yMin, yMax son razonables
- [ ] Dashboard HTML renderiza 11 scatter plots correctamente

**Testing:**
```python
def test_dispersion_scatter_data(generator):
    generator.load_flightscope_data()
    dispersion_data = generator.generate_dispersion_scatter_data()

    assert len(dispersion_data) > 0

    # Verificar Driver
    assert 'Driver' in dispersion_data
    driver = dispersion_data['Driver']

    assert 'poor' in driver
    assert 'regular' in driver
    assert 'good' in driver
    assert 'excellent' in driver
    assert 'xMin' in driver
    assert 'xMax' in driver
    assert 'yMin' in driver
    assert 'yMax' in driver

    # Verificar que hay puntos
    total_points = (len(driver['poor']) + len(driver['regular']) +
                   len(driver['good']) + len(driver['excellent']))
    assert total_points > 0

    # Verificar formato de puntos
    if len(driver['excellent']) > 0:
        point = driver['excellent'][0]
        assert 'x' in point
        assert 'y' in point
        assert isinstance(point['x'], (int, float))
        assert isinstance(point['y'], (int, float))
```

---

#### TASK 1.2: `merge_club_data()`
**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Media
**Tiempo estimado:** 2 horas
**Dependencias:** Ninguna
**Archivo:** `generate_dashboard_data.py` línea ~600

**Especificación técnica:**

**Input:**
- `club_stats`: Lista de dicts con stats básicas
- `launch_data`: Dict con launch_metrics.clubs
- `dispersion_data`: Dict con dispersion_analysis.clubs

**Output:**
```python
[
  {
    # De club_stats
    "name": "Driver",
    "distance": "212.8m",
    "distance_raw": 212.8,
    "deviation": "10.2m I",
    "speed": "235.5 km/h",
    "speed_raw": 235.5,
    "rating": 5,
    "category": "long",

    # De launch_metrics
    "launch_angle_mean": 12.3,
    "launch_angle_std": 2.1,
    "launch_delta_pga": 1.9,
    "launch_rating": "needs_work",
    "ball_speed_pct_pga": 86.2,
    "speed_rating": "good",
    "attack_angle_est": -2.5,
    "attack_angle_std": 1.2,
    "height_mean": 32.1,
    "carry_pct_pga": 81.8,

    # De dispersion_analysis
    "lateral_mean": -2.3,
    "lateral_std": 10.2,
    "consistency_score": 72,
    "consistency_rating": "good",
    "pattern_shape": "tight",
    "dispersion_area": 272.1,

    # Adicionales calculados
    "smash_factor": 1.42,
    "club_speed_est": 165.8,
    "precision_pct": 82
  },
  # ... 10 palos más
]
```

**Algoritmo:**
```python
def merge_club_data(self, club_stats, launch_data, dispersion_data):
    """
    Combina datos de club_statistics, launch_metrics y dispersion_analysis
    en un solo array unificado.

    Args:
        club_stats: Lista de stats básicas por palo
        launch_data: Dict con launch_metrics
        dispersion_data: Dict con dispersion_analysis

    Returns:
        list: Array de objetos club con TODOS los datos combinados
    """
    logger.info("Merging club data from multiple sources")

    merged = []

    # Mapeo de nombres de palos (diferentes formatos en diferentes fuentes)
    name_variants = {
        'Driver': ['Dr', 'Driver'],
        '3 Wood': ['3W', '3 Wood', '3Wood'],
        'Hybrid': ['Hyb', 'Hybrid'],
        '5 Iron': ['5i', '5 Iron', '5Iron'],
        '6 Iron': ['6i', '6 Iron', '6Iron'],
        '7 Iron': ['7i', '7 Iron', '7Iron'],
        '8 Iron': ['8i', '8 Iron', '8Iron'],
        '9 Iron': ['9i', '9 Iron', '9Iron'],
        'Pitching W': ['PW', 'Pitching W', 'PW'],
        'Gap Wedge': ['GW 52', 'Gap Wedge', 'GW', 'GW52'],
        'Sand Wedge': ['SW 58', 'Sand Wedge', 'SW', 'SW58']
    }

    def find_club_in_data(club_name, data_clubs, key='palo'):
        """Encuentra un club en un array por nombre (flexibilidad en nombres)."""
        if not data_clubs:
            return None

        # Buscar variantes del nombre
        variants = name_variants.get(club_name, [club_name])

        for club in data_clubs:
            club_key = club.get(key, '')
            if club_key in variants or club_key == club_name:
                return club

        return None

    # Iterar sobre club_stats como base
    for club in club_stats:
        club_name = club['name']

        # Copiar datos base
        merged_club = {**club}

        # Buscar en launch_metrics
        launch_clubs = launch_data.get('clubs', []) if launch_data else []
        launch_club = find_club_in_data(club_name, launch_clubs)

        if launch_club:
            # Agregar métricas de lanzamiento
            merged_club.update({
                'launch_angle_mean': launch_club.get('launch_angle_mean'),
                'launch_angle_std': launch_club.get('launch_angle_std'),
                'launch_delta_pga': launch_club.get('launch_delta_pga'),
                'launch_rating': launch_club.get('launch_rating'),
                'ball_speed_pct_pga': launch_club.get('ball_speed_pct_pga'),
                'speed_rating': launch_club.get('speed_rating'),
                'attack_angle_est': launch_club.get('attack_angle_est'),
                'attack_angle_std': launch_club.get('attack_angle_std'),
                'attack_delta_pga': launch_club.get('attack_delta_pga'),
                'attack_rating': launch_club.get('attack_rating'),
                'height_mean': launch_club.get('height_mean'),
                'height_delta_pga': launch_club.get('height_delta_pga'),
                'carry_pct_pga': launch_club.get('carry_pct_pga'),
                'carry_pct_hcp15': launch_club.get('carry_pct_hcp15'),
            })

        # Buscar en dispersion_analysis
        dispersion_clubs = dispersion_data.get('clubs', []) if dispersion_data else []
        dispersion_club = find_club_in_data(club_name, dispersion_clubs)

        if dispersion_club:
            # Agregar métricas de dispersión
            merged_club.update({
                'lateral_mean': dispersion_club.get('lateral_mean'),
                'lateral_std': dispersion_club.get('lateral_std'),
                'lateral_range': dispersion_club.get('lateral_range'),
                'lateral_min': dispersion_club.get('lateral_min'),
                'lateral_max': dispersion_club.get('lateral_max'),
                'bias_direction': dispersion_club.get('bias_direction'),
                'carry_std': dispersion_club.get('carry_std'),
                'carry_cv': dispersion_club.get('carry_cv'),
                'dispersion_area': dispersion_club.get('dispersion_area'),
                'dispersion_ratio': dispersion_club.get('dispersion_ratio'),
                'corridor_80_lateral': dispersion_club.get('corridor_80_lateral'),
                'corridor_80_long': dispersion_club.get('corridor_80_long'),
                'lateral_vs_pga': dispersion_club.get('lateral_vs_pga'),
                'lateral_vs_hcp15': dispersion_club.get('lateral_vs_hcp15'),
                'consistency_score': dispersion_club.get('consistency_score'),
                'consistency_rating': dispersion_club.get('consistency_rating'),
                'pattern_shape': dispersion_club.get('pattern_shape'),
                'lateral_tendency': dispersion_club.get('lateral_tendency'),
                'longitudinal_tendency': dispersion_club.get('longitudinal_tendency'),
            })

        # Calcular métricas adicionales
        if merged_club.get('speed_raw') and merged_club.get('distance_raw'):
            # Estimar smash factor (aproximado)
            # ball_speed en km/h, necesitamos m/s
            ball_speed_ms = merged_club['speed_raw'] / 3.6
            # Estimar club speed (smash factor típico ~1.4 para driver, ~1.3 irons)
            typical_smash = 1.42 if club_name == 'Driver' else 1.35
            club_speed_ms = ball_speed_ms / typical_smash

            merged_club['smash_factor_est'] = round(typical_smash, 2)
            merged_club['club_speed_est'] = round(club_speed_ms * 3.6, 1)  # km/h

        # Calcular precisión (% shots dentro de fairway/target)
        # Simplificado: basado en consistency_score
        if merged_club.get('consistency_score'):
            merged_club['precision_pct'] = merged_club['consistency_score']

        merged.append(merged_club)

    logger.success(f"Club data merged: {len(merged)} clubs with complete data")
    return merged
```

**Criterios de aceptación:**
- [ ] Combina datos de 3 fuentes correctamente
- [ ] 11 palos con datos completos
- [ ] No hay datos `None` en campos críticos
- [ ] Nombres de palos coinciden en todas las fuentes
- [ ] Métricas adicionales calculadas (smash_factor, club_speed)

---

#### TASK 1.3: `calculate_club_gaps()`
**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Baja
**Tiempo estimado:** 1 hora
**Dependencias:** TASK 1.2 (usa merged clubs)
**Archivo:** `generate_dashboard_data.py` línea ~750

**Especificación técnica:**

**Input:**
- `club_stats`: Lista de clubs (merged o no merged)

**Output:**
```python
{
  "Dr-3W": 10.4,
  "3W-Hyb": 41.8,
  "Hyb-5i": 12.5,
  "5i-6i": 15.2,
  "6i-7i": -3.8,  # Overlap negativo!
  "7i-8i": 17.4,
  "8i-9i": 1.6,
  "9i-PW": 9.9,
  "PW-GW": 15.1,
  "GW-SW": 4.4
}
```

**Algoritmo:**
```python
def calculate_club_gaps(self, club_stats):
    """
    Calcula gaps (brechas) entre palos consecutivos.

    Un gap negativo indica overlap (el palo "corto" pega más lejos que el "largo").

    Args:
        club_stats: Lista de clubs con distance_raw

    Returns:
        dict: {club1-club2: gap_meters}
    """
    logger.info("Calculating club gaps")

    # Ordenar palos por distancia descendente (más largo primero)
    sorted_clubs = sorted(
        club_stats,
        key=lambda x: x.get('distance_raw', 0),
        reverse=True
    )

    gaps = {}

    # Calcular gap entre cada par consecutivo
    for i in range(len(sorted_clubs) - 1):
        club1 = sorted_clubs[i]
        club2 = sorted_clubs[i + 1]

        dist1 = club1.get('distance_raw', 0)
        dist2 = club2.get('distance_raw', 0)

        gap = dist1 - dist2

        # Nombre del gap (usar nombres cortos si están disponibles)
        name1 = club1.get('name', 'Unknown')
        name2 = club2.get('name', 'Unknown')

        # Simplificar nombres para el gap
        name1_short = name1.replace(' Iron', 'i').replace(' Wood', 'W').replace(' Wedge', '').replace('Pitching W', 'PW').replace('Gap ', 'G').replace('Sand ', 'S')
        name2_short = name2.replace(' Iron', 'i').replace(' Wood', 'W').replace(' Wedge', '').replace('Pitching W', 'PW').replace('Gap ', 'G').replace('Sand ', 'S')

        gap_name = f"{name1_short}-{name2_short}"

        gaps[gap_name] = round(gap, 1)

        # Log warnings para overlaps
        if gap < 0:
            logger.warning(f"⚠️ OVERLAP detected: {gap_name} = {gap:.1f}m (negative gap)")
        elif gap < 5:
            logger.warning(f"⚠️ Small gap: {gap_name} = {gap:.1f}m (consider gapping)")

    logger.success(f"Club gaps calculated: {len(gaps)} gaps")
    return gaps
```

**Criterios de aceptación:**
- [ ] Calcula 10 gaps (11 palos → 10 gaps)
- [ ] Gaps ordenados por distancia
- [ ] Detecta overlaps (gaps negativos)
- [ ] Nombres de gaps son legibles
- [ ] Dashboard HTML muestra bar chart correctamente

---

#### TASK 1.4: Fix `calculate_temporal_evolution()`
**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Trivial
**Tiempo estimado:** 30 min
**Dependencias:** Ninguna
**Archivo:** `generate_dashboard_data.py` línea 217

**Cambio requerido:**

**ANTES:**
```python
palos_principales = ['Dr', '3W', 'Hyb', '7i', '9i', 'PW']  # Línea 224
```

**DESPUÉS:**
```python
palos_principales = ['Dr', '3W', 'Hyb', '5i', '6i', '7i', '8i', '9i', 'PW', 'GW 52', 'SW 58']
```

**Criterios de aceptación:**
- [ ] Genera datos para 11 palos
- [ ] Cada palo tiene labels (meses) y values (distancias)
- [ ] Dashboard HTML muestra 11 líneas en charts temporales

---

#### TASK 1.5: Modificar `generate_dashboard_data()`
**Prioridad:** 🔴 CRÍTICA
**Complejidad:** Media
**Tiempo estimado:** 2 horas
**Dependencias:** TASKS 1.1, 1.2, 1.3, 1.4
**Archivo:** `generate_dashboard_data.py` línea 403

**Código NUEVO:**
```python
def generate_dashboard_data(self):
    """Genera el objeto completo de datos para el dashboard."""
    logger.info("Generando datos del dashboard (versión 3.0)")

    # ========== CÁLCULOS BASE ==========
    logger.info("Paso 1/3: Calculando métricas base...")
    player_stats = self.calculate_player_stats()
    club_stats_basic = self.calculate_club_statistics()
    course_stats = self.calculate_course_statistics()
    temporal_evolution = self.calculate_temporal_evolution()  # Ahora con 11 palos

    # ========== FASE 5 - ANÁLISIS AVANZADOS ==========
    logger.info("Paso 2/3: Ejecutando análisis Fase 5...")
    launch_data = self.calculate_launch_metrics()
    dispersion_data = self.calculate_dispersion_analysis()
    consistency_data = self.calculate_consistency_benchmarks()

    # ========== MERGE Y ENRIQUECIMIENTO ==========
    logger.info("Paso 3/3: Merging y generando datos adicionales...")

    # CRÍTICO: Merge club data
    club_stats = self.merge_club_data(club_stats_basic, launch_data, dispersion_data)

    # CRÍTICO: Dispersion scatter data
    dispersion_by_club = self.generate_dispersion_scatter_data()

    # CRÍTICO: Club gaps
    club_gaps = self.calculate_club_gaps(club_stats)

    # ========== ESTRUCTURA JSON FINAL ==========
    self.dashboard_data = {
        'generated_at': datetime.now().isoformat(),

        # Player Stats
        'player_stats': player_stats,

        # Club Data (MERGED con launch + dispersion)
        'club_statistics': club_stats,
        'club_gaps': club_gaps,

        # Dispersion Scatter (CRÍTICO para 11 charts)
        'dispersion_by_club': dispersion_by_club,

        # Temporal Evolution (ahora 11 palos)
        'temporal_evolution': temporal_evolution,

        # Course Statistics
        'course_statistics': course_stats,

        # Fase 5 Original (para referencia/debugging)
        'launch_metrics': launch_data,
        'dispersion_analysis': dispersion_data,
        'consistency_benchmarks': consistency_data,

        # Metadata
        'metadata': {
            'version': '3.0.0',
            'sprint': 1,
            'data_sources': {
                'flightscope': str(self.flightscope_path),
                'tarjetas': str(self.tarjetas_path)
            },
            'phase_5_enabled': LaunchMetricsAnalyzer is not None,
            'total_clubs': len(club_stats),
            'total_dispersion_charts': len(dispersion_by_club)
        }
    }

    logger.success("✅ Dashboard data generado (Sprint 1 completo)")
```

**Criterios de aceptación:**
- [ ] JSON genera correctamente
- [ ] Todas las funciones nuevas se ejecutan sin errores
- [ ] JSON tiene estructura correcta
- [ ] Metadata incluye versión y stats

---

### SPRINT 2: TESTING Y VALIDACIÓN S1

#### TASK 2.1: Unit Tests Sprint 1
**Tiempo:** 2 horas

**Tests a crear:**
```python
def test_dispersion_scatter_data_structure()
def test_dispersion_scatter_data_classification()
def test_merge_club_data_completeness()
def test_merge_club_data_name_matching()
def test_club_gaps_calculation()
def test_club_gaps_overlap_detection()
def test_temporal_evolution_11_clubs()
def test_generate_dashboard_data_structure()
```

---

#### TASK 2.2: Integration Test con Dashboard HTML
**Tiempo:** 2 horas

**Acciones:**
1. Ejecutar `generate_dashboard_data.py`
2. Copiar JSON al directorio del dashboard
3. Abrir dashboard HTML en navegador
4. Validar que los 11 scatter plots se rendericen
5. Validar que club gaps chart funcione
6. Validar que temporal evolution tenga 11 palos
7. Captura de pantalla de cada chart

**Criterios:**
- [ ] 11 dispersion charts muestran puntos
- [ ] Club gaps chart muestra 10 barras
- [ ] Temporal evolution muestra 11 líneas
- [ ] No hay errores en consola JS

---

#### TASK 2.3: Performance Test
**Tiempo:** 1 hora

**Métricas a medir:**
- Tiempo de ejecución total
- Tamaño del JSON generado
- Tiempo de carga en navegador

**Objetivo:**
- Ejecución < 10 segundos
- JSON < 2 MB
- Carga HTML < 2 segundos

---

### SPRINT 3: FUNCIONES IMPORTANTES 🟡

#### TASK 3.1: `calculate_score_history()`
**Prioridad:** 🟡 IMPORTANTE
**Complejidad:** Baja
**Tiempo:** 1 hora

**Output:**
```python
[
  {"fecha": "2025-11-16", "score": 88, "campo": "Marina Golf"},
  {"fecha": "2025-12-07", "score": 92, "campo": "LA DEHESA"},
  # ...últimas 20
]
```

**Código:**
```python
def calculate_score_history(self, limit=20):
    """Extrae últimas N rondas ordenadas por fecha."""
    logger.info(f"Extracting last {limit} rounds")

    all_rounds = []

    for campo_nombre, campo_data in self.tarjetas_data.items():
        for ronda in campo_data['rondas']:
            all_rounds.append({
                'fecha': ronda['fecha'],
                'score': ronda['total_ronda'],
                'campo': campo_nombre
            })

    # Ordenar por fecha descendente
    all_rounds.sort(key=lambda x: x['fecha'], reverse=True)

    return all_rounds[:limit]
```

---

#### TASK 3.2: `calculate_percentiles()`
**Prioridad:** 🟡 IMPORTANTE
**Complejidad:** Media
**Tiempo:** 2 horas

**Output:**
```python
{
  "shortGame": 91,
  "ballSpeed": 78,
  "consistency": 65,
  "attackAngle": 25
}
```

**Código:** (ver TASK en sección anterior del documento)

---

#### TASK 3.3: `calculate_directional_distribution()`
**Prioridad:** 🟡 IMPORTANTE
**Complejidad:** Media
**Tiempo:** 2 horas

**Output:**
```python
[
  {"club": "Driver", "left": 12, "center": 65, "right": 23},
  # ...11 palos
]
```

**Código:** (ver TASK en sección anterior del documento)

---

#### TASK 3.4: `calculate_bubble_chart_data()`
**Prioridad:** 🟡 IMPORTANTE
**Complejidad:** Baja
**Tiempo:** 1 hora

**Output:**
```python
[
  {
    "club": "Driver",
    "consistency": 60,
    "distance": 212.8,
    "ballSpeed": 235.5,
    "category": "long"
  },
  # ...11 palos
]
```

**Código:**
```python
def calculate_bubble_chart_data(self, club_stats):
    """Genera datos para bubble chart (consistency vs distance vs ball speed)."""
    logger.info("Generating bubble chart data")

    bubble_data = []

    for club in club_stats:
        bubble_data.append({
            'club': club.get('name'),
            'consistency': club.get('consistency_score', 50),
            'distance': club.get('distance_raw', 0),
            'ballSpeed': club.get('speed_raw', 0),
            'category': club.get('category', 'mid')
        })

    return bubble_data
```

---

### SPRINT 4: TESTING S3

(Similar al Sprint 2, validar funciones de Sprint 3)

---

### SPRINT 5: MEJORAS VISUALES 🟢

#### TASK 5.1: `calculate_player_profile_radar()`
**Prioridad:** 🟢 MEJORA
**Complejidad:** Media
**Tiempo:** 2 horas

**Output:**
```python
{
  "shortGame": 65,
  "power": 78,
  "strategy": 55,
  "equipment": 82,
  "consistency": 72,
  "longGame": 84,
  "mental": 60,
  "accuracy": 68
}
```

---

#### TASK 5.2: `extract_trajectory_data()`
**Prioridad:** 🟢 MEJORA
**Complejidad:** Trivial
**Tiempo:** 30 min

---

#### TASK 5.3: `calculate_best_worst_rounds()`
**Prioridad:** 🟢 MEJORA
**Complejidad:** Baja
**Tiempo:** 1 hora

---

#### TASK 5.4: `calculate_quarterly_scoring()`
**Prioridad:** 🟢 MEJORA
**Complejidad:** Media
**Tiempo:** 1.5 horas

---

### SPRINT 6: MEJORAS DE TENDENCIAS 🟢

#### TASK 6.1: `extract_differential_distribution()`
**Tiempo:** 30 min

---

#### TASK 6.2: `calculate_monthly_volatility()`
**Tiempo:** 1 hora

---

#### TASK 6.3: `extract_recent_momentum()`
**Tiempo:** 30 min

---

#### TASK 6.4: `detect_milestones()`
**Tiempo:** 2 horas

---

#### TASK 6.5: `calculate_learning_curve()`
**Tiempo:** 1 hora

---

### SPRINT 7: FINALIZACIÓN

#### TASK 7.1: Code Review & Cleanup
**Tiempo:** 2 horas

- [ ] Remover código comentado
- [ ] Añadir docstrings a todas las funciones
- [ ] Verificar manejo de errores
- [ ] Optimizar performance

---

#### TASK 7.2: Documentation Update
**Tiempo:** 1 hora

- [ ] Actualizar README.md
- [ ] Actualizar CLAUDE.md
- [ ] Crear changelog

---

#### TASK 7.3: Final Testing
**Tiempo:** 1 hora

- [ ] Full regression test
- [ ] Dashboard validation completa
- [ ] Performance benchmarks

---

## 📊 ESTIMACIONES TOTALES

| Sprint | Tareas | Horas | Días (8h) |
|--------|--------|-------|-----------|
| Sprint 0 | 3 | 1h | 0.1 |
| Sprint 1 | 5 | 10h | 1.3 |
| Sprint 2 | 3 | 5h | 0.6 |
| Sprint 3 | 4 | 6h | 0.8 |
| Sprint 4 | 3 | 4h | 0.5 |
| Sprint 5 | 4 | 5h | 0.6 |
| Sprint 6 | 5 | 5h | 0.6 |
| Sprint 7 | 3 | 4h | 0.5 |
| **TOTAL** | **30** | **40h** | **5 días** |

**Nota:** Estimación conservadora con buffer. En práctica optimista: 3-4 días.

---

## ✅ DEFINITION OF DONE

### Por Tarea
- [ ] Código implementado y testeado
- [ ] Unit tests pasando
- [ ] Documentación actualizada
- [ ] Code review aprobado

### Por Sprint
- [ ] Todas las tareas completadas
- [ ] Integration tests pasando
- [ ] Dashboard HTML validado
- [ ] Sin regresiones

### Global
- [ ] 54+ charts funcionando
- [ ] JSON < 2 MB
- [ ] Performance < 10s generación
- [ ] 0 errores en consola
- [ ] Cliente satisfecho

---

## 🔄 WORKFLOW DE DESARROLLO

```
1. Crear branch: sprint-{N}-{descripción}
2. Implementar TASK
3. Run unit tests
4. Commit con mensaje descriptivo
5. Run integration test con dashboard
6. Merge a develop
7. Repetir hasta completar sprint
8. Testing completo de sprint
9. Merge a main
10. Tag versión (v3.{sprint}.0)
```

---

## 📝 NOTAS IMPORTANTES

### Restricciones
- ❌ **NUNCA modificar dashboard HTML**
- ✅ **SIEMPRE validar con dashboard después de cambios**
- ✅ **SIEMPRE crear backup antes de merge**

### Prioridades
1. **Funcionalidad** - Que el dashboard funcione
2. **Corrección** - Datos correctos
3. **Performance** - Optimización
4. **Estética** - Código limpio

### Comunicación
- Commits descriptivos en español
- Logs claros durante ejecución
- Documentar decisiones técnicas

---

**Última actualización:** 2026-02-03
**Próximo paso:** Ejecutar Sprint 0 (Setup)
**Estado:** 🟢 Ready to start
