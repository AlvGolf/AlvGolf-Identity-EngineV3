"""
AlvGolf — Temporal Identity Analysis
=====================================
Análisis temporal de la identidad golfística usando ventanas deslizantes.
Ejecuta ScoringEngine + ArchetypeClassifier por período para mostrar
la evolución del arquetipo del jugador a lo largo de 18 meses.

Ventana: 90 días de ancho, paso de 60 días.
Dimensiones computables: 6 de 8 (putting y mental quedan en 5.0 neutral).

Autor: AlvGolf / Álvaro Peralta
Versión: 1.0.0
"""

import math
import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

from app.scoring_engine import ScoringEngine, ScoringResult
from app.archetype_classifier import ArchetypeClassifier, ArchetypeResult


# ══════════════════════════════════════════════════════════════
# HCP INTERPOLATION
# ══════════════════════════════════════════════════════════════

# Monthly HCP data from hcp_trajectory.historical
_HCP_TIMELINE = [
    ("2024-04-15", 35.8),
    ("2024-05-15", 35.2),
    ("2024-06-15", 32.6),
    ("2024-07-15", 30.6),
    ("2024-08-15", 30.7),
    ("2024-09-15", 33.6),
    ("2024-10-15", 34.7),
    ("2024-11-15", 33.7),
    ("2024-12-15", 31.0),
    ("2025-03-15", 30.8),
    ("2025-04-15", 30.8),
    ("2025-05-15", 29.4),
    ("2025-07-15", 26.1),
    ("2025-08-15", 24.6),
    ("2025-09-15", 24.9),
    ("2025-10-15", 25.7),
    ("2025-11-15", 24.3),
    ("2025-12-15", 23.0),
]

_HCP_DATES = [datetime.strptime(d, "%Y-%m-%d") for d, _ in _HCP_TIMELINE]
_HCP_VALUES = [v for _, v in _HCP_TIMELINE]


def _interpolate_hcp(target_date: datetime) -> float:
    """Interpolación lineal del HCP para una fecha dada."""
    if target_date <= _HCP_DATES[0]:
        return _HCP_VALUES[0]
    if target_date >= _HCP_DATES[-1]:
        return _HCP_VALUES[-1]

    for i in range(len(_HCP_DATES) - 1):
        if _HCP_DATES[i] <= target_date <= _HCP_DATES[i + 1]:
            span = (_HCP_DATES[i + 1] - _HCP_DATES[i]).days
            pos = (target_date - _HCP_DATES[i]).days
            ratio = pos / span if span > 0 else 0
            return round(_HCP_VALUES[i] + ratio * (_HCP_VALUES[i + 1] - _HCP_VALUES[i]), 1)

    return _HCP_VALUES[-1]


def _interpolate_hcp_from_data(target_date: datetime, hcp_data: dict) -> float:
    """Interpolación HCP usando datos del JSON (hcp_trajectory.historical).
    Falls back to hardcoded timeline if data not available."""
    labels = hcp_data.get("labels", [])
    values = hcp_data.get("values", [])

    if not labels or not values:
        return _interpolate_hcp(target_date)

    dates = []
    for label in labels:
        try:
            dt = datetime.strptime(f"15 {label}", "%d %b %Y")
            dates.append(dt)
        except ValueError:
            continue

    if not dates:
        return _interpolate_hcp(target_date)

    hcp_vals = values[:len(dates)]

    if target_date <= dates[0]:
        return hcp_vals[0]
    if target_date >= dates[-1]:
        return hcp_vals[-1]

    for i in range(len(dates) - 1):
        if dates[i] <= target_date <= dates[i + 1]:
            span = (dates[i + 1] - dates[i]).days
            pos = (target_date - dates[i]).days
            ratio = pos / span if span > 0 else 0
            return round(hcp_vals[i] + ratio * (hcp_vals[i + 1] - hcp_vals[i]), 1)

    return hcp_vals[-1]


# ══════════════════════════════════════════════════════════════
# PERIOD METRICS EXTRACTION
# ══════════════════════════════════════════════════════════════

# Club code mapping for FlightScope (same as generate_dashboard_data.py)
_DRIVER_CODES = {"Dr", "Driver"}
_IRON7_CODES = {"7i", "7 Iron", "7Iron"}
_PW_CODES = {"PW", "Pitching W"}


def _extract_period_metrics(
    shots: List[dict],
    rounds: List[dict],
    player_hcp: float,
) -> dict:
    """Extrae métricas compatibles con ScoringEngine desde datos del período.

    Args:
        shots: Golpes FlightScope en la ventana [{f, p, c, v, l}, ...]
        rounds: Rondas de tarjetas en la ventana [{date, score, ...}, ...]
        player_hcp: HCP interpolado para el período

    Returns:
        Dict de métricas para ScoringEngine.score()
    """
    metrics = {}
    metrics["rounds_count"] = len(rounds)
    metrics["shots_count"] = len(shots)

    # ── Driver metrics ──────────────────────────────────────
    dr_shots = [s for s in shots if s.get("p") in _DRIVER_CODES]
    dr_carries = [s["c"] for s in dr_shots if s.get("c") is not None]
    dr_speeds = [s["v"] for s in dr_shots if s.get("v") is not None]
    dr_laterals = [s["l"] for s in dr_shots if s.get("l") is not None]

    if dr_carries:
        metrics["carry_driver_m"] = statistics.mean(dr_carries)
        metrics["driver_shots_count"] = len(dr_carries)
    if dr_speeds:
        metrics["ball_speed_driver_kmh"] = statistics.mean(dr_speeds)
    if len(dr_laterals) >= 3:
        metrics["lateral_std_driver_m"] = statistics.stdev(dr_laterals) if len(dr_laterals) > 1 else abs(dr_laterals[0])

    # ── 7 Iron metrics ──────────────────────────────────────
    ir7_shots = [s for s in shots if s.get("p") in _IRON7_CODES]
    ir7_carries = [s["c"] for s in ir7_shots if s.get("c") is not None]
    ir7_speeds = [s["v"] for s in ir7_shots if s.get("v") is not None]
    ir7_laterals = [s["l"] for s in ir7_shots if s.get("l") is not None]

    if ir7_carries:
        metrics["carry_7iron_m"] = statistics.mean(ir7_carries)
        metrics["7iron_shots_count"] = len(ir7_carries)
    if ir7_speeds:
        metrics["ball_speed_7iron_kmh"] = statistics.mean(ir7_speeds)
    if len(ir7_laterals) >= 3:
        metrics["lateral_std_7iron_m"] = statistics.stdev(ir7_laterals) if len(ir7_laterals) > 1 else abs(ir7_laterals[0])

    # ── Pitching Wedge metrics ──────────────────────────────
    pw_shots = [s for s in shots if s.get("p") in _PW_CODES]
    pw_carries = [s["c"] for s in pw_shots if s.get("c") is not None]
    pw_laterals = [s["l"] for s in pw_shots if s.get("l") is not None]

    if pw_carries:
        metrics["carry_pw_m"] = statistics.mean(pw_carries)
        metrics["pw_shots_count"] = len(pw_carries)
    if len(pw_laterals) >= 3:
        metrics["lateral_std_pw_m"] = statistics.stdev(pw_laterals) if len(pw_laterals) > 1 else abs(pw_laterals[0])

    # ── Scoring stats from rounds ───────────────────────────
    scores = [r["score"] for r in rounds if "score" in r]
    if len(scores) >= 2:
        metrics["score_mean"] = statistics.mean(scores)
        metrics["score_std_dev"] = statistics.stdev(scores)
    elif len(scores) == 1:
        metrics["score_mean"] = scores[0]

    # ── Power metrics (reuse driver speed) ──────────────────
    # ball_speed_driver_kmh already set above — used by _score_power()

    return {k: v for k, v in metrics.items() if v is not None}


# ══════════════════════════════════════════════════════════════
# CONFIDENCE CALCULATION
# ══════════════════════════════════════════════════════════════

def _period_confidence(shots_count: int, rounds_count: int) -> str:
    """Determine period confidence level."""
    if shots_count >= 20 and rounds_count >= 8:
        return "HIGH"
    elif shots_count >= 10 or rounds_count >= 4:
        return "MEDIUM"
    elif shots_count >= 1 or rounds_count >= 1:
        return "LOW"
    return "NONE"


# ══════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ══════════════════════════════════════════════════════════════

def calculate_identity_timeline(
    dashboard_data: dict,
    window_days: int = 90,
    step_days: int = 60,
) -> List[dict]:
    """Ventana deslizante de identity analysis.

    Args:
        dashboard_data: Complete dashboard_data.json dict
        window_days: Window width in days (default 90)
        step_days: Step between windows in days (default 60)

    Returns:
        List of period dicts with archetype classification per window.
    """
    engine = ScoringEngine()
    classifier = ArchetypeClassifier()

    # ── Extract data sources ────────────────────────────────
    shots_timeline = dashboard_data.get("flightscope_shots_timeline", [])
    rounds_raw = dashboard_data.get("score_history", {}).get("rounds", [])
    hcp_historical = dashboard_data.get("hcp_trajectory", {}).get("historical", {})

    # Parse dates
    shots_with_dates = []
    for s in shots_timeline:
        try:
            s["_dt"] = datetime.strptime(s["f"], "%Y-%m-%d")
            shots_with_dates.append(s)
        except (ValueError, KeyError):
            continue

    rounds_with_dates = []
    for r in rounds_raw:
        try:
            r["_dt"] = datetime.strptime(r["date"], "%Y-%m-%d")
            rounds_with_dates.append(r)
        except (ValueError, KeyError):
            continue

    if not shots_with_dates and not rounds_with_dates:
        return []

    # ── Detect date range ───────────────────────────────────
    all_dates = [s["_dt"] for s in shots_with_dates] + [r["_dt"] for r in rounds_with_dates]
    date_min = min(all_dates)
    date_max = max(all_dates)

    # ── Generate windows ────────────────────────────────────
    windows = []
    current_start = date_min - timedelta(days=window_days // 3)  # Start earlier to capture first data
    while current_start + timedelta(days=window_days) <= date_max + timedelta(days=window_days // 2):
        window_end = current_start + timedelta(days=window_days)
        windows.append((current_start, window_end))
        current_start += timedelta(days=step_days)

    # Ensure last window always covers the most recent data
    last_end = date_max + timedelta(days=1)
    last_start = last_end - timedelta(days=window_days)
    if not windows or windows[-1][1] < last_end - timedelta(days=step_days // 2):
        windows.append((last_start, last_end))

    # ── Process each window ─────────────────────────────────
    timeline = []
    for i, (w_start, w_end) in enumerate(windows):
        # Filter data for this window
        w_shots = [s for s in shots_with_dates if w_start <= s["_dt"] < w_end]
        w_rounds = [r for r in rounds_with_dates if w_start <= r["_dt"] < w_end]

        shots_count = len(w_shots)
        rounds_count = len(w_rounds)

        # Skip empty periods
        confidence = _period_confidence(shots_count, rounds_count)
        if confidence == "NONE":
            continue

        # Center date for labeling and HCP interpolation
        date_center = w_start + timedelta(days=window_days // 2)

        # Interpolate HCP
        hcp_estimated = _interpolate_hcp_from_data(date_center, hcp_historical)

        # Extract metrics for this period
        metrics = _extract_period_metrics(w_shots, w_rounds, hcp_estimated)

        # Run ScoringEngine
        scoring_result = engine.score(
            player_id="alvaro",
            player_hcp=float(hcp_estimated),
            metrics=metrics,
        )

        # Run ArchetypeClassifier
        archetype_result = classifier.classify(scoring_result)
        arch = archetype_result.archetype

        # Build period label (e.g., "Abr 2024")
        _MONTHS_ES = {
            1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic",
        }
        period_label = f"{_MONTHS_ES[date_center.month]} {date_center.year}"

        # Is this the last (current) period?
        is_current = (i == len(windows) - 1) or (w_end >= date_max)

        # Dimension scores dict
        dimensions = scoring_result.scores_as_dict()
        dimensions.pop("overall", None)

        # Top strength and gap
        ranking = scoring_result.dimensions_by_score()
        top_strength = ranking[0][0] if ranking else "unknown"
        top_gap = ranking[-1][0] if ranking else "unknown"

        timeline.append({
            "period_label": period_label,
            "date_center": date_center.strftime("%Y-%m-%d"),
            "date_start": w_start.strftime("%Y-%m-%d"),
            "date_end": w_end.strftime("%Y-%m-%d"),
            "shots_count": shots_count,
            "rounds_count": rounds_count,
            "hcp_estimated": hcp_estimated,
            "archetype_id": arch.id,
            "archetype_name": arch.name_es,
            "archetype_family": arch.id[0],
            "overall_score": scoring_result.overall_score,
            "dimensions": dimensions,
            "top_strength": top_strength,
            "top_gap": top_gap,
            "confidence": confidence,
            "is_current": False,  # Will set last one below
        })

    # Mark the last period as current
    if timeline:
        timeline[-1]["is_current"] = True

    # Clean up temporary _dt fields
    for s in shots_with_dates:
        s.pop("_dt", None)
    for r in rounds_with_dates:
        r.pop("_dt", None)

    return timeline
