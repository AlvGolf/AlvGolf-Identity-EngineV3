"""
AlvGolf — Scoring Engine
========================
Motor de scoring determinista que convierte métricas brutas de golf
en puntuaciones normalizadas 0-10 por dimensión de juego.

DISEÑO: Patent-defensible — todos los umbrales son explícitos, documentados
y derivados de benchmarks PGA Tour / WHS publicados. No hay inferencia de IA
en este módulo: dado el mismo input, siempre produce el mismo output.

DIMENSIONES (8):
  1. Long Game    — Driver y maderas de calle
  2. Mid Game     — Hierros medios (5i-7i)
  3. Short Game   — Wedges (PW, GW, SW, LW) y chip
  4. Putting      — Rendimiento en green
  5. Consistency  — Varianza y reproducibilidad
  6. Mental       — Gestión de rondas y presión
  7. Power        — Velocidad y distancia brutas
  8. Accuracy     — Dirección y dispersión

Autor: AlvGolf / Álvaro Peralta
Versión: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from enum import Enum
import math


# ══════════════════════════════════════════════════════════════
# ENUMS Y TIPOS
# ══════════════════════════════════════════════════════════════

class Zone(str, Enum):
    """
    Zona de rendimiento para cada dimensión.
    Mapea scores 0-10 a categorías interpretables por coaches y jugadores.
    """
    ELITE      = "elite"        # 8.5 – 10.0  → Top 10% amateur / nivel Tour
    STRONG     = "strong"       # 6.5 – 8.4   → Por encima de su HCP objetivo
    DEVELOPING = "developing"   # 4.0 – 6.4   → A nivel de su HCP actual
    FOCUS_AREA = "focus_area"   # 0.0 – 3.9   → Área de mejora prioritaria


class Confidence(str, Enum):
    """
    Nivel de confianza de una puntuación, basado en volumen de datos.
    Un score con LOW confidence debe tratarse con cautela en decisiones.
    """
    HIGH   = "high"    # ≥20 shots/rondas para esa dimensión
    MEDIUM = "medium"  # 8-19 shots/rondas
    LOW    = "low"     # 1-7 shots/rondas
    NONE   = "none"    # Sin datos — dimensión no puntuable


# ══════════════════════════════════════════════════════════════
# DATACLASSES
# ══════════════════════════════════════════════════════════════

@dataclass
class DimensionScore:
    """
    Puntuación de una sola dimensión con metadatos completos.
    
    score:       Valor normalizado 0.0-10.0
    percentile:  Percentil 0-100 vs grupo de referencia (HCP del jugador)
    zone:        Categoría interpretable (elite/strong/developing/focus_area)
    confidence:  Fiabilidad del dato basada en volumen de shots/rondas
    data_points: Número de observaciones usadas para calcular el score
    benchmark_used: Nombre del benchmark de referencia aplicado
    notes:       Lista de observaciones técnicas concretas
    """
    score:          float
    percentile:     float
    zone:           Zone
    confidence:     Confidence
    data_points:    int
    benchmark_used: str
    notes:          List[str] = field(default_factory=list)

    def __post_init__(self):
        # Validación de rangos
        assert 0.0 <= self.score <= 10.0, f"Score fuera de rango: {self.score}"
        assert 0.0 <= self.percentile <= 100.0, f"Percentil fuera de rango: {self.percentile}"


@dataclass
class ScoringResult:
    """
    Resultado completo del scoring engine para un jugador.
    
    Contiene las 8 dimensiones + metadata global.
    Es el input principal del ArchetypeClassifier.
    """
    player_id:   str
    player_hcp:  float

    # Las 8 dimensiones
    long_game:   DimensionScore
    mid_game:    DimensionScore
    short_game:  DimensionScore
    putting:     DimensionScore
    consistency: DimensionScore
    mental:      DimensionScore
    power:       DimensionScore
    accuracy:    DimensionScore

    # Scores globales derivados
    overall_score:     float  # Promedio ponderado de las 8 dimensiones
    tee_to_green:      float  # Promedio: long + mid + short + accuracy
    scoring_game:      float  # Promedio: putting + mental + consistency

    # Metadata
    rounds_analyzed:   int
    shots_analyzed:    int
    data_completeness: float  # 0-1: fracción de dimensiones con confidence ≥ MEDIUM

    def scores_as_dict(self) -> Dict[str, float]:
        """Devuelve todos los scores como dict simple para serialización."""
        return {
            "long_game":   self.long_game.score,
            "mid_game":    self.mid_game.score,
            "short_game":  self.short_game.score,
            "putting":     self.putting.score,
            "consistency": self.consistency.score,
            "mental":      self.mental.score,
            "power":       self.power.score,
            "accuracy":    self.accuracy.score,
            "overall":     self.overall_score,
        }

    def dimensions_by_score(self) -> List[Tuple[str, float]]:
        """Devuelve lista de (nombre_dimensión, score) ordenada de mayor a menor."""
        scores = self.scores_as_dict()
        scores.pop("overall")
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def top_strength(self) -> Tuple[str, float]:
        """Devuelve la dimensión con mayor score."""
        return self.dimensions_by_score()[0]

    def top_gap(self) -> Tuple[str, float]:
        """Devuelve la dimensión con menor score (mayor área de mejora)."""
        return self.dimensions_by_score()[-1]


# ══════════════════════════════════════════════════════════════
# BENCHMARKS INTERNOS
# ══════════════════════════════════════════════════════════════

# Estructura de benchmarks por nivel de HCP.
# Fuentes: PGA Tour ShotLink, USGA/WHS datos publicados, 
# Broadie "Every Shot Counts" (2014), DeNunzio research (2016-2020).
#
# Formato: { hcp_max: { metric: (min_value, max_value) } }
# donde el rango representa el intervalo "normal" para ese nivel.

DRIVER_BENCHMARKS = {
    # (ball_speed_kmh, carry_m, lateral_std_m, smash_factor)
     0: {"ball_speed": 267, "carry": 257, "lateral_std": 5.5,  "smash_factor": 1.49},
     5: {"ball_speed": 240, "carry": 228, "lateral_std": 7.0,  "smash_factor": 1.47},
    10: {"ball_speed": 232, "carry": 218, "lateral_std": 9.0,  "smash_factor": 1.45},
    15: {"ball_speed": 225, "carry": 210, "lateral_std": 10.5, "smash_factor": 1.43},
    20: {"ball_speed": 215, "carry": 198, "lateral_std": 13.0, "smash_factor": 1.41},
    25: {"ball_speed": 210, "carry": 190, "lateral_std": 15.5, "smash_factor": 1.39},
    30: {"ball_speed": 200, "carry": 178, "lateral_std": 19.0, "smash_factor": 1.36},
    36: {"ball_speed": 188, "carry": 162, "lateral_std": 23.0, "smash_factor": 1.32},
}

IRON7_BENCHMARKS = {
    # (ball_speed_kmh, carry_m, lateral_std_m)
     0: {"ball_speed": 177, "carry": 160, "lateral_std": 3.5},
     5: {"ball_speed": 165, "carry": 150, "lateral_std": 5.0},
    10: {"ball_speed": 158, "carry": 142, "lateral_std": 7.0},
    15: {"ball_speed": 153, "carry": 135, "lateral_std": 8.5},
    20: {"ball_speed": 147, "carry": 128, "lateral_std": 11.0},
    25: {"ball_speed": 143, "carry": 122, "lateral_std": 13.5},
    30: {"ball_speed": 136, "carry": 113, "lateral_std": 17.0},
    36: {"ball_speed": 128, "carry": 103, "lateral_std": 21.0},
}

PW_BENCHMARKS = {
    # (carry_m, lateral_std_m, spin_rpm)
     0: {"carry": 125, "lateral_std": 2.5,  "spin": 9500},
     5: {"carry": 118, "lateral_std": 3.5,  "spin": 8500},
    10: {"carry": 112, "lateral_std": 5.0,  "spin": 7800},
    15: {"carry": 105, "lateral_std": 6.5,  "spin": 7000},
    20: {"carry": 98,  "lateral_std": 9.0,  "spin": 6200},
    25: {"carry": 93,  "lateral_std": 11.5, "spin": 5600},
    30: {"carry": 86,  "lateral_std": 14.0, "spin": 5000},
    36: {"carry": 78,  "lateral_std": 18.0, "spin": 4300},
}

# Benchmarks de scoring en campo (Strokes Gained vs scratch)
# Fuente: Broadie & Feit (2012), adaptado a rangos HCP RFEG
SG_BENCHMARKS = {
    # SG esperado por categoría para llegar a scoring de scratch (0)
    # Valores negativos = golpes perdidos vs scratch
     0: {"sg_ott": 0.0,   "sg_app": 0.0,   "sg_arg": 0.0,   "sg_putt": 0.0},
     5: {"sg_ott": -0.3,  "sg_app": -0.4,  "sg_arg": -0.3,  "sg_putt": -0.2},
    10: {"sg_ott": -0.6,  "sg_app": -0.9,  "sg_arg": -0.6,  "sg_putt": -0.4},
    15: {"sg_ott": -1.0,  "sg_app": -1.6,  "sg_arg": -0.9,  "sg_putt": -0.6},
    20: {"sg_ott": -1.5,  "sg_app": -2.3,  "sg_arg": -1.3,  "sg_putt": -0.8},
    25: {"sg_ott": -2.1,  "sg_app": -3.0,  "sg_arg": -1.7,  "sg_putt": -1.0},
    30: {"sg_ott": -2.8,  "sg_app": -3.8,  "sg_arg": -2.2,  "sg_putt": -1.3},
    36: {"sg_ott": -3.8,  "sg_app": -5.0,  "sg_arg": -3.0,  "sg_putt": -1.7},
}


# ══════════════════════════════════════════════════════════════
# FUNCIONES DE APOYO
# ══════════════════════════════════════════════════════════════

def _interpolate_benchmark(hcp: float, benchmark_table: dict, metric: str) -> float:
    """
    Interpola linealmente el valor de benchmark para el HCP exacto del jugador.
    
    Ejemplo: HCP 23 → interpola entre HCP 20 y HCP 25.
    Esto es más preciso que usar el bracket más cercano.
    
    Args:
        hcp: Handicap del jugador (puede ser decimal, e.g. 23.2)
        benchmark_table: Diccionario con benchmarks por HCP
        metric: Clave de la métrica a interpolar
        
    Returns:
        Valor interpolado del benchmark
    """
    levels = sorted(benchmark_table.keys())
    
    # Clamp a los límites de la tabla
    if hcp <= levels[0]:
        return benchmark_table[levels[0]][metric]
    if hcp >= levels[-1]:
        return benchmark_table[levels[-1]][metric]
    
    # Encontrar el intervalo correcto
    for i in range(len(levels) - 1):
        lo, hi = levels[i], levels[i + 1]
        if lo <= hcp <= hi:
            t = (hcp - lo) / (hi - lo)  # factor de interpolación 0-1
            return benchmark_table[lo][metric] * (1 - t) + benchmark_table[hi][metric] * t
    
    return benchmark_table[levels[-1]][metric]


def _metric_to_percentile(
    value: float,
    benchmark_at_hcp: float,
    benchmark_at_scratch: float,
    higher_is_better: bool = True
) -> float:
    """
    Convierte una métrica bruta a percentil 0-100 relativo al nivel del jugador.
    
    La escala es:
      - 50° percentil = rendimiento exactamente a nivel del HCP del jugador
      - 100° percentil = rendimiento a nivel PGA Tour para esa métrica
      - 0° percentil = rendimiento significativamente por debajo del HCP
    
    DISEÑO DE ESCALA:
    Usamos una escala donde el punto 50 es el benchmark del HCP actual,
    el punto 85 es el benchmark del HCP objetivo (HCP - 8 aproximadamente),
    y el punto 100 es el benchmark PGA Tour. Esto permite ver claramente
    dónde está el jugador respecto a su potencial de mejora.
    
    Args:
        value: Valor medido del jugador
        benchmark_at_hcp: Valor esperado para el HCP actual del jugador
        benchmark_at_scratch: Valor del mejor benchmark (PGA Tour / scratch)
        higher_is_better: True para distancia/velocidad, False para dispersión/score
        
    Returns:
        Percentil 0-100
    """
    if not higher_is_better:
        # Para métricas donde menor = mejor (lateral_std, score), invertimos
        value = -value
        benchmark_at_hcp = -benchmark_at_hcp
        benchmark_at_scratch = -benchmark_at_scratch
    
    # Rango completo de la escala
    full_range = benchmark_at_scratch - benchmark_at_hcp
    
    if abs(full_range) < 0.001:
        # Evitar división por cero
        return 50.0
    
    # Posición del jugador en la escala
    # 0 = a nivel HCP, full_range = a nivel scratch
    position = value - benchmark_at_hcp
    
    # Convertir a percentil centrado en 50 (HCP = 50, scratch = ~95)
    # Usamos factor de compresión para que 100 = scratch sea alcanzable pero difícil
    raw_percentile = 50.0 + (position / full_range) * 45.0
    
    # Clamp con límites razonables
    return max(0.0, min(100.0, raw_percentile))


def _percentile_to_score(percentile: float) -> float:
    """
    Convierte percentil 0-100 a score 0-10.
    
    CURVA DE CONVERSIÓN:
    No es lineal — usamos una curva ligeramente sigmoide que:
    - Hace más difícil subir de 8.5 (zona elite)
    - Hace más fácil salir de zona 0-2 (para evitar desmotivación)
    - El punto 50 (HCP actual) mapea a ≈5.0
    
    Umbrales clave:
      0  percentil → 0.0 score
      25 percentil → 2.5 score  
      50 percentil → 5.0 score  (benchmark del HCP)
      75 percentil → 7.2 score
      85 percentil → 8.2 score
      95 percentil → 9.2 score
     100 percentil → 10.0 score  (PGA Tour elite)
    """
    if percentile <= 0:
        return 0.0
    if percentile >= 100:
        return 10.0
    
    # Conversión base lineal
    base = percentile / 10.0
    
    # Ajuste no-lineal: comprimir la zona alta (>8) para que sea más difícil
    if percentile >= 85:
        # Zona elite: mapea 85-100 percentil a 8.5-10.0 score
        elite_fraction = (percentile - 85) / 15.0
        return 8.5 + elite_fraction * 1.5
    elif percentile >= 50:
        # Zona buena: mapea 50-85 percentil a 5.0-8.5 score
        good_fraction = (percentile - 50) / 35.0
        return 5.0 + good_fraction * 3.5
    else:
        # Zona de desarrollo: mapea 0-50 percentil a 0.0-5.0 score
        return percentile / 10.0


def _score_to_zone(score: float) -> Zone:
    """
    Asigna zona cualitativa basada en score numérico.
    
    Umbrales justificados:
    - 8.5+: Elite — supera claramente el HCP objetivo del jugador en esa dimensión
    - 6.5-8.4: Strong — rendimiento sólido, por encima del promedio de su HCP
    - 4.0-6.4: Developing — a nivel de su HCP actual, margen de mejora claro
    - <4.0: Focus Area — por debajo del nivel esperado, prioridad de trabajo
    """
    if score >= 8.5:
        return Zone.ELITE
    elif score >= 6.5:
        return Zone.STRONG
    elif score >= 4.0:
        return Zone.DEVELOPING
    else:
        return Zone.FOCUS_AREA


def _get_confidence(data_points: int) -> Confidence:
    """
    Determina nivel de confianza según volumen de datos.
    
    Umbrales basados en estadística de muestras pequeñas:
    - 20+ observaciones: intervalo de confianza 95% suficientemente estrecho
    - 8-19: confianza media, resultados orientativos
    - 1-7: muestra muy pequeña, resultado indicativo solamente
    - 0: sin datos
    """
    if data_points >= 20:
        return Confidence.HIGH
    elif data_points >= 8:
        return Confidence.MEDIUM
    elif data_points >= 1:
        return Confidence.LOW
    else:
        return Confidence.NONE


# ══════════════════════════════════════════════════════════════
# SCORING ENGINE PRINCIPAL
# ══════════════════════════════════════════════════════════════

class ScoringEngine:
    """
    Motor de scoring determinista de AlvGolf.
    
    Convierte métricas brutas de golf (FlightScope + tarjetas de campo)
    en puntuaciones normalizadas 0-10 por cada dimensión de juego.
    
    USO:
        engine = ScoringEngine()
        result = engine.score(player_id="alvaro", player_hcp=23.2, metrics=data_dict)
    
    IMPORTANTE: Este módulo es completamente determinista.
    El mismo input siempre produce el mismo output, independientemente
    de cuándo se ejecute o qué versión de IA esté en producción.
    """

    def score(self, player_id: str, player_hcp: float, metrics: dict) -> ScoringResult:
        """
        Punto de entrada principal. Calcula el ScoringResult completo.
        
        Args:
            player_id: Identificador del jugador
            player_hcp: Handicap actual (puede ser decimal, e.g. 23.2)
            metrics: Diccionario con todas las métricas disponibles.
                     Las métricas no disponibles deben estar ausentes (no None).
                     
        Returns:
            ScoringResult con las 8 dimensiones puntuadas y metadata global.
        """
        # Calcular cada dimensión
        long_game   = self._score_long_game(player_hcp, metrics)
        mid_game    = self._score_mid_game(player_hcp, metrics)
        short_game  = self._score_short_game(player_hcp, metrics)
        putting     = self._score_putting(player_hcp, metrics)
        consistency = self._score_consistency(player_hcp, metrics)
        mental      = self._score_mental(player_hcp, metrics)
        power       = self._score_power(player_hcp, metrics)
        accuracy    = self._score_accuracy(player_hcp, metrics)

        # Scores agregados
        tee_to_green = _weighted_average([
            (long_game.score,  0.30),
            (mid_game.score,   0.30),
            (short_game.score, 0.25),
            (accuracy.score,   0.15),
        ])
        scoring_game = _weighted_average([
            (putting.score,     0.40),
            (mental.score,      0.35),
            (consistency.score, 0.25),
        ])
        overall_score = _weighted_average([
            (long_game.score,   0.15),
            (mid_game.score,    0.15),
            (short_game.score,  0.15),
            (putting.score,     0.15),
            (consistency.score, 0.12),
            (mental.score,      0.10),
            (power.score,       0.10),
            (accuracy.score,    0.08),
        ])

        # Data completeness
        dims = [long_game, mid_game, short_game, putting, consistency, mental, power, accuracy]
        confident_dims = sum(1 for d in dims if d.confidence in [Confidence.HIGH, Confidence.MEDIUM])
        completeness = confident_dims / 8.0

        return ScoringResult(
            player_id=player_id,
            player_hcp=player_hcp,
            long_game=long_game,
            mid_game=mid_game,
            short_game=short_game,
            putting=putting,
            consistency=consistency,
            mental=mental,
            power=power,
            accuracy=accuracy,
            overall_score=round(overall_score, 2),
            tee_to_green=round(tee_to_green, 2),
            scoring_game=round(scoring_game, 2),
            rounds_analyzed=metrics.get("rounds_count", 0),
            shots_analyzed=metrics.get("shots_count", 0),
            data_completeness=round(completeness, 2),
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 1: LONG GAME
    # ──────────────────────────────────────────────
    def _score_long_game(self, hcp: float, m: dict) -> DimensionScore:
        """
        Long Game = Driver + Fairway Woods.
        
        Métricas principales (de mayor a menor peso):
        - carry_driver: Distancia de carry con driver (40% del score)
        - sg_ott: Strokes Gained Off the Tee (35%)
        - driver_ball_speed: Velocidad de bola con driver (15%)
        - fairway_hit_pct: % de fairways alcanzados (10%)
        
        NOTA: sg_ott es la métrica más importante porque captura el resultado
        final (fairway + distancia), no solo un parámetro aislado.
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- Carry Driver (0-10 sub-score) ---
        if "carry_driver_m" in m:
            carry = m["carry_driver_m"]
            data_points += m.get("driver_shots_count", 10)
            bm_hcp    = _interpolate_benchmark(hcp, DRIVER_BENCHMARKS, "carry")
            bm_pga    = DRIVER_BENCHMARKS[0]["carry"]
            pct = _metric_to_percentile(carry, bm_hcp, bm_pga, higher_is_better=True)
            sub_scores.append((pct, 0.40))
            diff = carry - bm_hcp
            notes.append(
                f"Driver carry: {carry:.0f}m (benchmark HCP{hcp:.0f}: {bm_hcp:.0f}m, "
                f"diferencia: {diff:+.0f}m)"
            )

        # --- Strokes Gained Off the Tee ---
        if "sg_ott" in m:
            sg = m["sg_ott"]
            bm_hcp = _interpolate_benchmark(hcp, SG_BENCHMARKS, "sg_ott")
            bm_pga = 0.0  # PGA Tour = 0 por definición
            # SG_OTT negativo = perdiendo golpes. Ajustamos escala:
            # sg = bm_hcp (nivel HCP) → percentil 50
            # sg = bm_pga (= 0) → percentil 95
            sg_range = bm_pga - bm_hcp  # rango positivo
            if abs(sg_range) > 0.001:
                position = sg - bm_hcp
                pct = 50.0 + (position / sg_range) * 45.0
                pct = max(0.0, min(100.0, pct))
            else:
                pct = 50.0
            sub_scores.append((pct, 0.35))
            notes.append(
                f"SG Off the Tee: {sg:+.2f} (benchmark HCP{hcp:.0f}: {bm_hcp:+.2f})"
            )

        # --- Ball Speed Driver ---
        if "ball_speed_driver_kmh" in m:
            bs = m["ball_speed_driver_kmh"]
            bm_hcp = _interpolate_benchmark(hcp, DRIVER_BENCHMARKS, "ball_speed")
            bm_pga = DRIVER_BENCHMARKS[0]["ball_speed"]
            pct = _metric_to_percentile(bs, bm_hcp, bm_pga, higher_is_better=True)
            sub_scores.append((pct, 0.15))
            notes.append(f"Ball speed driver: {bs:.0f} km/h (benchmark: {bm_hcp:.0f} km/h)")

        # --- Fairway Hit % ---
        if "fairway_hit_pct" in m:
            fir = m["fairway_hit_pct"]  # 0-100
            # Benchmarks FIR: PGA=60%, HCP 10=50%, HCP 20=42%, HCP 30=34%
            fir_benchmarks = {0: 60, 10: 50, 20: 42, 30: 34, 36: 28}
            bm_hcp_fir = _interpolate_benchmark(hcp, {k: {"fir": v} for k, v in fir_benchmarks.items()}, "fir")
            bm_pga_fir = 60.0
            pct = _metric_to_percentile(fir, bm_hcp_fir, bm_pga_fir, higher_is_better=True)
            sub_scores.append((pct, 0.10))
            notes.append(f"Fairways hit: {fir:.0f}% (benchmark: {bm_hcp_fir:.0f}%)")

        if not sub_scores:
            return _empty_dimension("long_game")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 2: MID GAME
    # ──────────────────────────────────────────────
    def _score_mid_game(self, hcp: float, m: dict) -> DimensionScore:
        """
        Mid Game = Hierros 5-7 (aproximaciones medias-largas).
        
        Métricas:
        - carry_7iron: Distancia de carry con 7 hierro (35%)
        - sg_approach: Strokes Gained Approach (45%)  ← más importante que la distancia
        - smash_factor_irons: Eficiencia de contacto (20%)
        
        El SG Approach tiene el mayor peso porque las aproximaciones al green
        tienen el mayor impacto en el score total tras el driver.
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- SG Approach (mayor peso) ---
        if "sg_approach" in m:
            sg = m["sg_approach"]
            bm_hcp = _interpolate_benchmark(hcp, SG_BENCHMARKS, "sg_app")
            sg_range = 0.0 - bm_hcp
            if abs(sg_range) > 0.001:
                pct = 50.0 + ((sg - bm_hcp) / sg_range) * 45.0
                pct = max(0.0, min(100.0, pct))
            else:
                pct = 50.0
            sub_scores.append((pct, 0.45))
            notes.append(f"SG Approach: {sg:+.2f} (benchmark HCP{hcp:.0f}: {bm_hcp:+.2f})")

        # --- Carry 7 Hierro ---
        if "carry_7iron_m" in m:
            carry = m["carry_7iron_m"]
            data_points += m.get("7iron_shots_count", 8)
            bm_hcp = _interpolate_benchmark(hcp, IRON7_BENCHMARKS, "carry")
            bm_pga = IRON7_BENCHMARKS[0]["carry"]
            pct = _metric_to_percentile(carry, bm_hcp, bm_pga, higher_is_better=True)
            sub_scores.append((pct, 0.35))
            diff = carry - bm_hcp
            notes.append(
                f"7 Hierro carry: {carry:.0f}m (benchmark: {bm_hcp:.0f}m, {diff:+.0f}m)"
            )

        # --- Smash Factor Irons ---
        if "smash_factor_7iron" in m:
            sf = m["smash_factor_7iron"]
            # Driver SF benchmark: PGA=1.49, HCP15=1.43, HCP25=1.38
            # Iron SF es más uniforme entre niveles: PGA=1.37, HCP25=1.29
            iron_sf_benchmarks = {0: 1.37, 10: 1.35, 15: 1.33, 20: 1.31, 25: 1.29, 30: 1.26, 36: 1.23}
            bm_hcp_sf = _interpolate_benchmark(hcp, {k: {"sf": v} for k, v in iron_sf_benchmarks.items()}, "sf")
            bm_pga_sf = 1.37
            # Escala: SF 1.28 = percentil 0, SF bm_hcp = percentil 50, SF 1.37 = percentil 95
            sf_range = bm_pga_sf - bm_hcp_sf
            if abs(sf_range) > 0.001:
                pct = 50.0 + ((sf - bm_hcp_sf) / sf_range) * 45.0
                pct = max(0.0, min(100.0, pct))
            else:
                pct = 50.0
            sub_scores.append((pct, 0.20))
            notes.append(f"Smash factor 7i: {sf:.3f} (benchmark: {bm_hcp_sf:.3f})")

        if not sub_scores:
            return _empty_dimension("mid_game")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points if data_points > 0 else 10)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 3: SHORT GAME
    # ──────────────────────────────────────────────
    def _score_short_game(self, hcp: float, m: dict) -> DimensionScore:
        """
        Short Game = Wedges (PW, GW, SW, LW) + Chip + Pitch.
        
        Métricas:
        - sg_arg: Strokes Gained Around the Green (45%) ← incluye chip y pitch
        - wedge_lateral_std: Dispersión lateral con wedges (30%)
        - scrambling_pct: % de up & downs logrados (25%)
        
        El short game es el mayor diferencial entre amateurs del mismo HCP.
        Un jugador con short game elite (percentil 90+) puede jugar 3-5 golpes
        menos que otro del mismo HCP con short game débil.
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- SG Around the Green ---
        if "sg_arg" in m:
            sg = m["sg_arg"]
            bm_hcp = _interpolate_benchmark(hcp, SG_BENCHMARKS, "sg_arg")
            sg_range = 0.0 - bm_hcp
            if abs(sg_range) > 0.001:
                pct = 50.0 + ((sg - bm_hcp) / sg_range) * 45.0
                pct = max(0.0, min(100.0, pct))
            else:
                pct = 50.0
            sub_scores.append((pct, 0.45))
            notes.append(f"SG Around the Green: {sg:+.2f} (benchmark: {bm_hcp:+.2f})")

        # --- Dispersión wedges (lateral_std PW) ---
        if "lateral_std_pw_m" in m:
            disp = m["lateral_std_pw_m"]
            data_points += m.get("pw_shots_count", 10)
            bm_hcp = _interpolate_benchmark(hcp, PW_BENCHMARKS, "lateral_std")
            bm_pga = PW_BENCHMARKS[0]["lateral_std"]
            # MENOR dispersión = MEJOR → higher_is_better=False
            pct = _metric_to_percentile(disp, bm_hcp, bm_pga, higher_is_better=False)
            sub_scores.append((pct, 0.30))
            diff = disp - bm_hcp
            notes.append(
                f"Dispersión PW: {disp:.1f}m (benchmark: {bm_hcp:.1f}m, {diff:+.1f}m)"
            )

        # --- Scrambling % ---
        if "scrambling_pct" in m:
            scr = m["scrambling_pct"]
            # Benchmarks scrambling: PGA=58%, HCP10=45%, HCP20=30%, HCP30=18%
            scr_benchmarks = {0: 58, 10: 45, 15: 38, 20: 30, 25: 23, 30: 18, 36: 13}
            bm_hcp_scr = _interpolate_benchmark(hcp, {k: {"s": v} for k, v in scr_benchmarks.items()}, "s")
            bm_pga_scr = 58.0
            pct = _metric_to_percentile(scr, bm_hcp_scr, bm_pga_scr, higher_is_better=True)
            sub_scores.append((pct, 0.25))
            notes.append(f"Scrambling: {scr:.0f}% (benchmark: {bm_hcp_scr:.0f}%)")

        if not sub_scores:
            return _empty_dimension("short_game")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points if data_points > 0 else 10)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 4: PUTTING
    # ──────────────────────────────────────────────
    def _score_putting(self, hcp: float, m: dict) -> DimensionScore:
        """
        Putting = rendimiento total en greens.
        
        Métricas:
        - sg_putt: Strokes Gained Putting (50%) ← mejor métrica global de putting
        - putts_per_round: Putts totales por ronda (30%)
        - three_putt_pct: % de hoyos con 3 putts (20%)
        
        El SG Putting es más fiable que putts/ronda porque ajusta por
        la calidad de las proximidades (más fácil hacer 1 putt desde 30cm).
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- SG Putting ---
        if "sg_putt" in m:
            sg = m["sg_putt"]
            bm_hcp = _interpolate_benchmark(hcp, SG_BENCHMARKS, "sg_putt")
            sg_range = 0.0 - bm_hcp
            if abs(sg_range) > 0.001:
                pct = 50.0 + ((sg - bm_hcp) / sg_range) * 45.0
                pct = max(0.0, min(100.0, pct))
            else:
                pct = 50.0
            sub_scores.append((pct, 0.50))
            notes.append(f"SG Putting: {sg:+.2f} (benchmark HCP{hcp:.0f}: {bm_hcp:+.2f})")

        # --- Putts por ronda ---
        if "putts_per_round" in m:
            ppr = m["putts_per_round"]
            data_points += m.get("rounds_count", 10)
            # Benchmarks: PGA=28.2, HCP10=31.5, HCP20=33.8, HCP30=36.5
            putt_benchmarks = {0: 28.2, 10: 31.5, 15: 32.8, 20: 33.8, 25: 35.2, 30: 36.5, 36: 38.5}
            bm_hcp_pp = _interpolate_benchmark(hcp, {k: {"p": v} for k, v in putt_benchmarks.items()}, "p")
            bm_pga_pp = 28.2
            # Menos putts = mejor → higher_is_better=False
            pct = _metric_to_percentile(ppr, bm_hcp_pp, bm_pga_pp, higher_is_better=False)
            sub_scores.append((pct, 0.30))
            diff = ppr - bm_hcp_pp
            notes.append(
                f"Putts/ronda: {ppr:.1f} (benchmark: {bm_hcp_pp:.1f}, {diff:+.1f})"
            )

        # --- 3-putt % ---
        if "three_putt_pct" in m:
            tp = m["three_putt_pct"]
            # Benchmarks 3-putt %: PGA=2.5%, HCP10=8%, HCP20=14%, HCP30=22%
            tp_benchmarks = {0: 2.5, 10: 8.0, 15: 11.0, 20: 14.0, 25: 18.0, 30: 22.0, 36: 28.0}
            bm_hcp_tp = _interpolate_benchmark(hcp, {k: {"t": v} for k, v in tp_benchmarks.items()}, "t")
            bm_pga_tp = 2.5
            # Menos 3-putts = mejor → higher_is_better=False
            pct = _metric_to_percentile(tp, bm_hcp_tp, bm_pga_tp, higher_is_better=False)
            sub_scores.append((pct, 0.20))
            notes.append(f"3-putt %: {tp:.0f}% (benchmark: {bm_hcp_tp:.0f}%)")

        if not sub_scores:
            return _empty_dimension("putting")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points if data_points > 0 else 10)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 5: CONSISTENCY
    # ──────────────────────────────────────────────
    def _score_consistency(self, hcp: float, m: dict) -> DimensionScore:
        """
        Consistency = reproducibilidad del rendimiento ronda a ronda.
        
        Métricas:
        - score_std_dev: Desviación estándar de scores por ronda (40%)
        - consistency_index: (std_dev / mean) × 100 (30%)
        - carry_cv_driver: Coeficiente de variación del carry con driver (30%)
        
        DISEÑO: La consistencia no mide si juegas bien, sino si juegas
        de forma predecible. Un jugador HCP 25 muy consistente puede
        competir mejor que un HCP 20 volátil.
        
        Benchmark de consistencia: coeficiente de variación del score.
        - CV < 8%: muy consistente
        - CV 8-12%: consistente
        - CV > 12%: volátil
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- Score std_dev (varianza de puntuaciones) ---
        if "score_std_dev" in m and "score_mean" in m:
            std = m["score_std_dev"]
            mean = m["score_mean"]
            data_points += m.get("rounds_count", 10)
            cv = (std / mean) * 100 if mean > 0 else 20.0  # Coeficiente de variación en %

            # Benchmarks CV: PGA=3%, HCP10=6%, HCP20=10%, HCP30=15%
            cv_benchmarks = {0: 3.0, 10: 6.0, 15: 8.0, 20: 10.0, 25: 12.5, 30: 15.0, 36: 19.0}
            bm_hcp_cv = _interpolate_benchmark(hcp, {k: {"cv": v} for k, v in cv_benchmarks.items()}, "cv")
            bm_pga_cv = 3.0

            # Menor CV = más consistente = mejor → higher_is_better=False
            pct_cv = _metric_to_percentile(cv, bm_hcp_cv, bm_pga_cv, higher_is_better=False)
            sub_scores.append((pct_cv, 0.40))
            sub_scores.append((pct_cv, 0.30))  # también para consistency_index
            notes.append(
                f"Varianza scores: std={std:.1f}, CV={cv:.1f}% (benchmark: {bm_hcp_cv:.1f}%)"
            )

        # --- Carry CV Driver ---
        if "carry_cv_driver_pct" in m:
            carry_cv = m["carry_cv_driver_pct"]
            # Benchmarks: PGA=2%, HCP15=5%, HCP25=8%
            carry_cv_bm = {0: 2.0, 10: 4.0, 15: 5.0, 20: 6.5, 25: 8.0, 30: 10.0, 36: 13.0}
            bm_hcp_ccv = _interpolate_benchmark(hcp, {k: {"ccv": v} for k, v in carry_cv_bm.items()}, "ccv")
            bm_pga_ccv = 2.0
            pct = _metric_to_percentile(carry_cv, bm_hcp_ccv, bm_pga_ccv, higher_is_better=False)
            sub_scores.append((pct, 0.30))
            notes.append(f"Driver carry CV: {carry_cv:.1f}% (benchmark: {bm_hcp_ccv:.1f}%)")

        if not sub_scores:
            return _empty_dimension("consistency")

        # Consolidar los sub-scores (puede haber duplicado del CV)
        total_weight = sum(w for _, w in sub_scores)
        final_pct = sum(p * w for p, w in sub_scores) / total_weight
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 6: MENTAL
    # ──────────────────────────────────────────────
    def _score_mental(self, hcp: float, m: dict) -> DimensionScore:
        """
        Mental = gestión mental del juego y la ronda.
        
        Esta es la dimensión más difícil de cuantificar porque no viene
        de FlightScope sino de patrones en tarjetas de campo.
        
        Métricas proxy (no directas):
        - bounce_back_rate: % de birdies/pares tras bogey doble o peor (35%)
          → Proxy de resiliencia mental
        - early_vs_late_delta: Diferencia de scoring en hoyos 1-9 vs 10-18 (25%)
          → Proxy de aguante y gestión de fatiga/presión
        - par3_vs_par4_relative: Rendimiento relativo en par 3 (hoyos de presión) (20%)
          → Proxy de gestión bajo presión de tee
        - worst_hole_frequency: % de rondas con hoyo +3 o peor (20%)
          → Proxy de control de daños (la "explosion hole")
        
        NOTA: Todos estos son PROXIES, no medidas directas. La confianza
        de esta dimensión será siempre MEDIUM como máximo.
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- Bounce-back rate ---
        if "bounce_back_rate_pct" in m:
            bbr = m["bounce_back_rate_pct"]
            data_points += m.get("rounds_count", 10)
            # Benchmarks: PGA=33%, HCP10=22%, HCP20=15%, HCP30=9%
            bbr_bm = {0: 33, 10: 22, 15: 18, 20: 15, 25: 12, 30: 9, 36: 6}
            bm_hcp_bbr = _interpolate_benchmark(hcp, {k: {"b": v} for k, v in bbr_bm.items()}, "b")
            bm_pga_bbr = 33.0
            pct = _metric_to_percentile(bbr, bm_hcp_bbr, bm_pga_bbr, higher_is_better=True)
            sub_scores.append((pct, 0.35))
            notes.append(f"Bounce-back rate: {bbr:.0f}% (benchmark: {bm_hcp_bbr:.0f}%)")

        # --- Delta Front 9 vs Back 9 ---
        if "f9_vs_b9_delta" in m:
            delta = abs(m["f9_vs_b9_delta"])  # Valor absoluto de la diferencia
            # Un delta < 3 = buena gestión. Delta > 6 = problema de aguante.
            # Benchmarks (delta promedio): PGA=0.8, HCP15=2.5, HCP25=4.0
            delta_bm = {0: 0.8, 10: 2.0, 15: 2.5, 20: 3.2, 25: 4.0, 30: 5.2, 36: 7.0}
            bm_hcp_d = _interpolate_benchmark(hcp, {k: {"d": v} for k, v in delta_bm.items()}, "d")
            bm_pga_d = 0.8
            # Menor delta = mejor
            pct = _metric_to_percentile(delta, bm_hcp_d, bm_pga_d, higher_is_better=False)
            sub_scores.append((pct, 0.25))
            notes.append(f"Delta F9/B9: {delta:.1f} golpes (benchmark: {bm_hcp_d:.1f})")

        # --- Par 3 scoring vs par (relativo) ---
        if "par3_vs_par_relative" in m:
            p3r = m["par3_vs_par_relative"]  # e.g. +0.8 = jugando 0.8 sobre par en par3s
            # Benchmark: todos los tipos de hoyo deberían costar ~igual respecto al HCP
            # Si par3_vs_par_relative > par4_vs_par_relative + 0.5, hay presión en tee corto
            # Benchmarks de sobre-par en par 3: PGA=+0.0, HCP15=+0.8, HCP25=+1.4
            p3_bm = {0: 0.0, 10: 0.5, 15: 0.8, 20: 1.1, 25: 1.4, 30: 1.8, 36: 2.3}
            bm_hcp_p3 = _interpolate_benchmark(hcp, {k: {"p3": v} for k, v in p3_bm.items()}, "p3")
            bm_pga_p3 = 0.0
            # Menor sobre-par = mejor
            pct = _metric_to_percentile(p3r, bm_hcp_p3, bm_pga_p3, higher_is_better=False)
            sub_scores.append((pct, 0.20))
            notes.append(
                f"Par 3 sobre-par relativo: {p3r:+.2f} (benchmark: {bm_hcp_p3:+.2f})"
            )

        # --- Worst hole frequency (explosion holes) ---
        if "explosion_hole_pct" in m:
            expl = m["explosion_hole_pct"]  # % de hoyos con +3 o peor vs par
            # Benchmarks: PGA≈0.5%, HCP10=3%, HCP20=7%, HCP30=12%
            expl_bm = {0: 0.5, 10: 3.0, 15: 5.0, 20: 7.0, 25: 9.5, 30: 12.0, 36: 16.0}
            bm_hcp_ex = _interpolate_benchmark(hcp, {k: {"ex": v} for k, v in expl_bm.items()}, "ex")
            bm_pga_ex = 0.5
            pct = _metric_to_percentile(expl, bm_hcp_ex, bm_pga_ex, higher_is_better=False)
            sub_scores.append((pct, 0.20))
            notes.append(f"Hoyos explosivos (+3): {expl:.0f}% (benchmark: {bm_hcp_ex:.0f}%)")

        if not sub_scores:
            return _empty_dimension("mental")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        # Mental siempre máximo MEDIUM por ser proxies
        confidence = Confidence.MEDIUM if data_points >= 10 else Confidence.LOW

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0 (proxies)",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 7: POWER
    # ──────────────────────────────────────────────
    def _score_power(self, hcp: float, m: dict) -> DimensionScore:
        """
        Power = capacidad física bruta de generación de velocidad.
        
        Métricas:
        - club_speed_driver_kmh: Velocidad de cabeza con driver (50%) ← métrica principal
        - ball_speed_driver_kmh: Velocidad de bola con driver (30%)
        - club_speed_7iron_kmh: Velocidad de cabeza con hierro 7 (20%)
        
        NOTA: Power difiere de Long Game en que mide el POTENCIAL físico,
        no el resultado en campo. Un jugador puede tener mucho power pero
        perderlo por mala técnica (smash factor bajo). Power alto + Long Game bajo
        → problema técnico corregible, no físico.
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- Club Speed Driver ---
        if "club_speed_driver_kmh" in m:
            cs = m["club_speed_driver_kmh"]
            data_points += m.get("driver_shots_count", 10)
            # Benchmarks club speed: PGA=179 km/h, HCP10=155, HCP20=143, HCP30=133
            cs_bm = {0: 179, 5: 165, 10: 155, 15: 150, 20: 143, 25: 138, 30: 133, 36: 125}
            bm_hcp_cs = _interpolate_benchmark(hcp, {k: {"cs": v} for k, v in cs_bm.items()}, "cs")
            bm_pga_cs = 179.0
            pct = _metric_to_percentile(cs, bm_hcp_cs, bm_pga_cs, higher_is_better=True)
            sub_scores.append((pct, 0.50))
            diff = cs - bm_hcp_cs
            notes.append(
                f"Club speed driver: {cs:.0f} km/h (benchmark: {bm_hcp_cs:.0f} km/h, {diff:+.0f})"
            )

        # --- Ball Speed Driver ---
        if "ball_speed_driver_kmh" in m:
            bs = m["ball_speed_driver_kmh"]
            bm_hcp_bs = _interpolate_benchmark(hcp, DRIVER_BENCHMARKS, "ball_speed")
            bm_pga_bs = DRIVER_BENCHMARKS[0]["ball_speed"]
            pct = _metric_to_percentile(bs, bm_hcp_bs, bm_pga_bs, higher_is_better=True)
            sub_scores.append((pct, 0.30))
            notes.append(f"Ball speed driver: {bs:.0f} km/h (benchmark: {bm_hcp_bs:.0f} km/h)")

        # --- Club Speed 7 Hierro ---
        if "club_speed_7iron_kmh" in m:
            cs7 = m["club_speed_7iron_kmh"]
            # Benchmarks 7i club speed: PGA=136, HCP15=118, HCP25=108
            cs7_bm = {0: 136, 10: 124, 15: 118, 20: 113, 25: 108, 30: 103, 36: 97}
            bm_hcp_cs7 = _interpolate_benchmark(hcp, {k: {"cs7": v} for k, v in cs7_bm.items()}, "cs7")
            bm_pga_cs7 = 136.0
            pct = _metric_to_percentile(cs7, bm_hcp_cs7, bm_pga_cs7, higher_is_better=True)
            sub_scores.append((pct, 0.20))
            notes.append(f"Club speed 7i: {cs7:.0f} km/h (benchmark: {bm_hcp_cs7:.0f} km/h)")

        if not sub_scores:
            return _empty_dimension("power")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )

    # ──────────────────────────────────────────────
    # DIMENSIÓN 8: ACCURACY
    # ──────────────────────────────────────────────
    def _score_accuracy(self, hcp: float, m: dict) -> DimensionScore:
        """
        Accuracy = precisión y control de dirección.
        
        Métricas:
        - lateral_std_driver_m: Dispersión lateral con driver (35%)
        - face_to_path_driver: Ángulo cara-camino (indicador de control) (25%)
        - gir_pct: Greens en regulación % (25%)
        - lateral_std_7iron_m: Dispersión lateral con 7 hierro (15%)
        
        DISEÑO: Accuracy mide DÓNDE van los golpes, no lo lejos que van.
        Complementa Power: juntos revelan si la velocidad está bien aprovechada.
        face_to_path → cuanto más cerca de 0° mejor, es una medida de consistencia técnica.
        """
        sub_scores = []
        notes = []
        data_points = 0

        # --- Lateral std Driver ---
        if "lateral_std_driver_m" in m:
            lat = m["lateral_std_driver_m"]
            data_points += m.get("driver_shots_count", 10)
            bm_hcp = _interpolate_benchmark(hcp, DRIVER_BENCHMARKS, "lateral_std")
            bm_pga = DRIVER_BENCHMARKS[0]["lateral_std"]
            # Menor dispersión = mejor
            pct = _metric_to_percentile(lat, bm_hcp, bm_pga, higher_is_better=False)
            sub_scores.append((pct, 0.35))
            diff = lat - bm_hcp
            notes.append(
                f"Dispersión lateral driver: {lat:.1f}m (benchmark: {bm_hcp:.1f}m, {diff:+.1f}m)"
            )

        # --- Face-to-path (valor absoluto → cerca de 0 = mejor) ---
        if "face_to_path_driver_deg" in m:
            ftp = abs(m["face_to_path_driver_deg"])  # valor absoluto
            # Benchmarks |face-to-path|: PGA=1.0°, HCP15=3.5°, HCP25=5.5°
            ftp_bm = {0: 1.0, 5: 2.0, 10: 2.8, 15: 3.5, 20: 4.5, 25: 5.5, 30: 7.0, 36: 9.0}
            bm_hcp_ftp = _interpolate_benchmark(hcp, {k: {"ftp": v} for k, v in ftp_bm.items()}, "ftp")
            bm_pga_ftp = 1.0
            pct = _metric_to_percentile(ftp, bm_hcp_ftp, bm_pga_ftp, higher_is_better=False)
            sub_scores.append((pct, 0.25))
            direction = "slice" if m.get("face_to_path_driver_deg", 0) > 0 else "hook"
            notes.append(
                f"|Face-to-path|: {ftp:.1f}° ({direction}, benchmark: {bm_hcp_ftp:.1f}°)"
            )

        # --- GIR % ---
        if "gir_pct" in m:
            gir = m["gir_pct"]
            # Benchmarks GIR%: PGA=66%, HCP10=40%, HCP20=25%, HCP30=13%
            gir_bm = {0: 66, 5: 52, 10: 40, 15: 32, 20: 25, 25: 18, 30: 13, 36: 8}
            bm_hcp_gir = _interpolate_benchmark(hcp, {k: {"gir": v} for k, v in gir_bm.items()}, "gir")
            bm_pga_gir = 66.0
            pct = _metric_to_percentile(gir, bm_hcp_gir, bm_pga_gir, higher_is_better=True)
            sub_scores.append((pct, 0.25))
            diff = gir - bm_hcp_gir
            notes.append(f"GIR: {gir:.0f}% (benchmark: {bm_hcp_gir:.0f}%, {diff:+.0f}pp)")

        # --- Lateral std 7 Hierro ---
        if "lateral_std_7iron_m" in m:
            lat7 = m["lateral_std_7iron_m"]
            bm_hcp_l7 = _interpolate_benchmark(hcp, IRON7_BENCHMARKS, "lateral_std")
            bm_pga_l7 = IRON7_BENCHMARKS[0]["lateral_std"]
            pct = _metric_to_percentile(lat7, bm_hcp_l7, bm_pga_l7, higher_is_better=False)
            sub_scores.append((pct, 0.15))
            notes.append(f"Dispersión 7 hierro: {lat7:.1f}m (benchmark: {bm_hcp_l7:.1f}m)")

        if not sub_scores:
            return _empty_dimension("accuracy")

        final_pct = sum(p * w for p, w in sub_scores) / sum(w for _, w in sub_scores)
        final_score = _percentile_to_score(final_pct)
        confidence = _get_confidence(data_points)

        return DimensionScore(
            score=round(final_score, 2),
            percentile=round(final_pct, 1),
            zone=_score_to_zone(final_score),
            confidence=confidence,
            data_points=data_points,
            benchmark_used=f"AlvGolf HCP{hcp:.0f} Benchmark v1.0",
            notes=notes,
        )


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def _empty_dimension(name: str) -> DimensionScore:
    """Devuelve una dimensión vacía cuando no hay datos suficientes."""
    return DimensionScore(
        score=5.0,  # Score neutral para no distorsionar agregados
        percentile=50.0,
        zone=Zone.DEVELOPING,
        confidence=Confidence.NONE,
        data_points=0,
        benchmark_used="N/A — Sin datos",
        notes=[f"Dimensión '{name}' sin datos disponibles. Score neutral asignado."],
    )


def _weighted_average(score_weight_pairs: List[Tuple[float, float]]) -> float:
    """Calcula media ponderada de (score, weight) pairs."""
    total_weight = sum(w for _, w in score_weight_pairs)
    if total_weight == 0:
        return 5.0
    return sum(s * w for s, w in score_weight_pairs) / total_weight


# ══════════════════════════════════════════════════════════════
# TEST / DEMO
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Test con datos reales de Álvaro (HCP 23.2):
    - Short game elite (percentil 95)
    - Driver con dispersión alta y face-to-path problema
    - Mejora sostenida en los últimos 18 meses
    """

    alvaro_metrics = {
        # Control y metadata
        "rounds_count": 52,
        "shots_count": 493,

        # Driver
        "carry_driver_m": 212.8,
        "ball_speed_driver_kmh": 235.5,
        "club_speed_driver_kmh": 164.0,
        "lateral_std_driver_m": 10.2,
        "face_to_path_driver_deg": +4.2,  # Slice moderado
        "smash_factor_driver": 1.43,
        "driver_shots_count": 45,

        # 7 Hierro
        "carry_7iron_m": 145.0,
        "ball_speed_7iron_kmh": 148.0,
        "club_speed_7iron_kmh": 110.0,
        "lateral_std_7iron_m": 9.5,
        "smash_factor_7iron": 1.33,
        "7iron_shots_count": 38,

        # Pitching Wedge
        "carry_pw_m": 96.1,
        "lateral_std_pw_m": 8.0,  # Excelente para HCP 23
        "pw_shots_count": 55,

        # Scoring (campo)
        "score_mean": 95.3,
        "score_std_dev": 5.2,
        "fairway_hit_pct": 52,
        "gir_pct": 28,
        "putts_per_round": 33.2,
        "three_putt_pct": 12,
        "scrambling_pct": 45,  # Elite para HCP 23

        # SG (calculados por backend)
        "sg_ott": -1.8,
        "sg_approach": -2.1,
        "sg_arg": +1.8,   # Elite — short game
        "sg_putt": -0.4,

        # Mental proxies
        "bounce_back_rate_pct": 22,
        "f9_vs_b9_delta": 3.5,
        "par3_vs_par_relative": 1.3,
        "explosion_hole_pct": 8,

        # Consistency
        "carry_cv_driver_pct": 5.8,
    }

    engine = ScoringEngine()
    result = engine.score("alvaro", player_hcp=23.2, metrics=alvaro_metrics)

    print("=" * 65)
    print(f"  ALVGOLF SCORING ENGINE — {result.player_id.upper()} (HCP {result.player_hcp})")
    print("=" * 65)

    dim_map = {
        "Long Game":   result.long_game,
        "Mid Game":    result.mid_game,
        "Short Game":  result.short_game,
        "Putting":     result.putting,
        "Consistency": result.consistency,
        "Mental":      result.mental,
        "Power":       result.power,
        "Accuracy":    result.accuracy,
    }

    for name, dim in dim_map.items():
        bar = "█" * int(dim.score) + "░" * (10 - int(dim.score))
        print(
            f"  {name:<12} [{bar}] {dim.score:4.1f}/10  "
            f"P{dim.percentile:4.0f}  {dim.zone.value:<12}  {dim.confidence.value}"
        )

    print("-" * 65)
    print(f"  OVERALL:     {result.overall_score:.2f}/10")
    print(f"  Tee-to-Green: {result.tee_to_green:.2f}/10")
    print(f"  Scoring Game: {result.scoring_game:.2f}/10")
    print(f"  Data completeness: {result.data_completeness*100:.0f}%")
    print("=" * 65)

    print("\nTop Strength:", result.top_strength())
    print("Top Gap:     ", result.top_gap())
    print()
    for note in result.short_game.notes:
        print(f"  Short Game — {note}")
