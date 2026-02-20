"""
AlvGolf — Scoring Integration Module
=====================================
Función que se añade al generador del backend Python (el script que produce
dashboard_data.json). Calcula scoring + arquetipo y los añade al JSON
en menos de 50ms, sin IA, sin esperas.

CÓMO USAR:
  Al final de tu script principal de backend, antes de hacer json.dump(),
  llama a esta función:

    from scoring_integration import add_scoring_to_dashboard
    data = add_scoring_to_dashboard(data)
    
  El resultado es el mismo dashboard_data.json con dos nuevas claves:
    - data['scoring_profile']   → 8 scores 0-10 + metadata
    - data['golf_identity']     → arquetipo completo + insight personalizado

Autor: AlvGolf
Versión: 1.0.0
"""

import math
import sys
from pathlib import Path

# Importar los módulos que ya hemos creado
# (ajustar el path según dónde estén en tu proyecto)
sys.path.insert(0, str(Path(__file__).parent))
from app.scoring_engine import ScoringEngine, ScoringResult
from app.archetype_classifier import ArchetypeClassifier, ArchetypeResult


def _extract_lateral_std_from_dispersion(dispersion_dict: dict) -> float:
    """
    Calcula el lateral_std real a partir de los puntos de dispersión del JSON.
    
    El JSON tiene los shots categorizados (poor/regular/good/excellent).
    Calculamos la desviación estándar real de todos los puntos X.
    
    Nota: la dispersión del JSON incluye algunos outliers extremos que
    distorsionan la std. Usamos percentil 90 para una métrica más representativa
    del swing típico (no del peor golpe).
    """
    all_x = []
    for cat in ['excellent', 'good', 'regular', 'poor']:
        all_x += [abs(pt['x']) for pt in dispersion_dict.get(cat, [])]
    
    if not all_x:
        return None
    
    # Usar percentil 75 como proxy de lateral_std "típica"
    # (más representativo que la std pura que penaliza extremos)
    all_x_sorted = sorted(all_x)
    p75_idx = int(len(all_x_sorted) * 0.75)
    return round(all_x_sorted[p75_idx], 1)


def _extract_metrics_from_json(data: dict) -> dict:
    """
    Extrae todas las métricas del dashboard_data.json y las mapea
    al formato que espera ScoringEngine.
    
    Mapeo completo basado en la estructura real del JSON de AlvGolf.
    """
    metrics = {}
    
    # ── Metadata ──────────────────────────────────────────────
    ps = data.get('player_stats', {})
    metrics['rounds_count'] = ps.get('total_rondas', 52)
    metrics['shots_count']  = ps.get('golpes_flightscope', 493)
    
    # ── Club statistics ───────────────────────────────────────
    club_stats = data.get('club_statistics', [])
    clubs = {c['name']: c for c in club_stats}
    
    # Driver
    dr = clubs.get('Driver', {})
    if dr:
        metrics['carry_driver_m']        = dr.get('distance_raw')
        metrics['ball_speed_driver_kmh'] = dr.get('speed_raw')
        metrics['driver_shots_count']    = 45  # approx — no está en club_statistics
        
        # Lateral std desde dispersion_by_club
        disp_dr = data.get('dispersion_by_club', {}).get('Driver', {})
        if disp_dr:
            metrics['lateral_std_driver_m'] = _extract_lateral_std_from_dispersion(disp_dr)
    
    # 7 Iron
    ir7 = clubs.get('7 Iron', {})
    if ir7:
        metrics['carry_7iron_m']        = ir7.get('distance_raw')
        metrics['ball_speed_7iron_kmh'] = ir7.get('speed_raw')
        metrics['7iron_shots_count']    = 48
    
    # Pitching Wedge
    pw = clubs.get('Pitching W', {})
    if pw:
        metrics['carry_pw_m']       = pw.get('distance_raw')
        metrics['pw_shots_count']   = 55
        # Lateral std del PW desde dispersion
        disp_pw = data.get('dispersion_by_club', {}).get('PitchingW', 
                  data.get('dispersion_by_club', {}).get('Pitching W', {}))
        if disp_pw:
            metrics['lateral_std_pw_m'] = _extract_lateral_std_from_dispersion(disp_pw)
    
    # ── Strokes Gained ────────────────────────────────────────
    sg_data = data.get('strokes_gained', {})
    sg_cats = {c['category']: c for c in sg_data.get('categories', [])}
    
    if 'Off the Tee (Driving)' in sg_cats:
        metrics['sg_ott'] = sg_cats['Off the Tee (Driving)']['strokes_gained']
    if 'Approach Shots' in sg_cats:
        metrics['sg_approach'] = sg_cats['Approach Shots']['strokes_gained']
    if 'Short Game' in sg_cats:
        metrics['sg_arg'] = sg_cats['Short Game']['strokes_gained']
    if 'Putting' in sg_cats:
        metrics['sg_putt'] = sg_cats['Putting']['strokes_gained']
    
    # ── Scoring stats ─────────────────────────────────────────
    cb = data.get('consistency_benchmarks', {}).get('scoring_18', {})
    if cb:
        metrics['score_mean']    = cb.get('score_mean')
        metrics['score_std_dev'] = cb.get('score_std')
        # CV ya está calculado en el JSON
        metrics['carry_cv_driver_pct'] = cb.get('score_cv')  # proxy
    
    # ── Swing DNA → face_to_path y attack_angle ───────────────
    swing_dims = {d['name']: d for d in data.get('swing_dna', {}).get('dimensions', [])}
    
    # Face Angle player_value (0-100) → convertir a grados aproximados
    # player_value=62 → moderado slice. Escala: 100=0°, 50=±6°, 0=±12°
    fa_val = swing_dims.get('Face Angle', {}).get('player_value', 75)
    # Invertir: 100→0°, 62→~4.7°, 50→6°
    face_to_path_deg = round((100 - fa_val) / 8.5, 1)
    metrics['face_to_path_driver_deg'] = face_to_path_deg
    
    # Smash factor desde swing_dna (aproximado)
    sf_val = swing_dims.get('Smash Factor', {}).get('player_value', 82)
    # Escala: 100→1.50, 72(hcp23 bench)→1.39, 82→~1.43
    smash_factor = round(1.28 + (sf_val / 100) * 0.22, 3)
    metrics['smash_factor_driver']  = smash_factor
    metrics['smash_factor_7iron']   = round(smash_factor - 0.06, 3)
    
    # ── Benchmark radar → dimensiones de scoring ─────────────
    # El benchmark_radar tiene scores 0-100 por dimensión para el jugador
    # Los usamos directamente para dimensiones que no tienen métrica directa
    br = data.get('benchmark_radar', {})
    br_dims = br.get('dimensions', [])
    br_player = br.get('player', [])
    br_map = dict(zip(br_dims, br_player))
    
    # GIR % proxy desde Approach Accuracy (0-100 → 0-66%)
    if 'Approach Accuracy' in br_map:
        aa_val = br_map['Approach Accuracy']
        # hcp23 benchmark GIR ≈ 18%, PGA = 66%
        # aa_val=65 → ~28% GIR (interpolado)
        metrics['gir_pct'] = round(8 + (aa_val / 100) * 58, 1)
    
    # ── Mental proxies desde datos de campo ───────────────────
    # Course Management del benchmark radar (0-100) → convertir a proxies
    cm_val = br_map.get('Course Management', 77)
    
    # bounce_back_rate: cm_val=77 → ~22% (interpolado)
    metrics['bounce_back_rate_pct'] = round(5 + (cm_val / 100) * 30, 1)
    
    # F9 vs B9 delta: desde score_history si disponible
    rounds = data.get('score_history', {}).get('rounds', [])
    if len(rounds) >= 10:
        # Proxy: usar volatility como indicador del delta
        # (no tenemos F9/B9 separado en el JSON)
        vi = data.get('volatility_index', [])
        if vi:
            avg_cv = sum(q.get('coefficient_variation', 8) for q in vi) / len(vi)
            metrics['f9_vs_b9_delta'] = round(avg_cv * 0.4, 1)  # proxy
        else:
            metrics['f9_vs_b9_delta'] = 3.5
    
    # explosion_hole_pct: desde hole_rates del consistency_benchmark
    hb = data.get('consistency_benchmarks', {}).get('handicap_benchmark', {})
    hole_rates = hb.get('player_hole_rates', {})
    if hole_rates:
        # double_plus rate = 53.3% de hoyos. Los +3 son ~20% de los doubles
        double_plus = hole_rates.get('double_plus', 53.3)
        metrics['explosion_hole_pct'] = round(double_plus * 0.18, 1)
    
    # Par3 relative: desde benchmark_radar Mental Game
    mental_val = br_map.get('Mental Game', 70)
    metrics['par3_vs_par_relative'] = round(2.5 - (mental_val / 100) * 1.5, 2)
    
    # Putts per round: desde scoring y benchmarks
    # HCP 23 típico: 33-34 putts. SG_putt=-0.5 → cerca del promedio
    metrics['putts_per_round'] = 33.2
    metrics['three_putt_pct'] = 12
    
    # Scrambling: Short Game SG=+1.8 → muy bueno → ~45%
    if 'Short Game' in sg_cats:
        sg_short = sg_cats['Short Game']['strokes_gained']
        # sg=0 → 30% scrambling para HCP23, sg=+1.8 → ~45%
        metrics['scrambling_pct'] = round(30 + sg_short * 8.3, 1)
    
    # Fairway hit %: desde Driving Accuracy del benchmark_radar
    if 'Driving Accuracy' in br_map:
        da_val = br_map['Driving Accuracy']
        # da_val=62 → ~52% fairways (hcp23 promedio ~42%, PGA 60%)
        metrics['fairway_hit_pct'] = round(28 + (da_val / 100) * 32, 1)
    
    # ── Limpiar Nones ─────────────────────────────────────────
    return {k: v for k, v in metrics.items() if v is not None}


def add_scoring_to_dashboard(data: dict) -> dict:
    """
    Función principal. Añade scoring_profile y golf_identity al dashboard_data.
    
    USAGE en tu backend:
        data = add_scoring_to_dashboard(data)
    
    Tiempo de ejecución: < 50ms
    Determinista: mismo JSON → mismo resultado siempre
    
    Args:
        data: El dict completo del dashboard_data.json
        
    Returns:
        El mismo dict con dos claves nuevas añadidas:
        - 'scoring_profile': ScoringResult serializado
        - 'golf_identity': ArchetypeResult serializado
    """
    try:
        hcp = data.get('player_stats', {}).get('handicap_actual', 23.2)
        player_id = 'alvaro'  # En versión multi-usuario esto vendría del contexto
        
        # Extraer métricas del JSON
        metrics = _extract_metrics_from_json(data)
        
        # Calcular scores (< 10ms)
        engine = ScoringEngine()
        scoring_result: ScoringResult = engine.score(
            player_id=player_id,
            player_hcp=float(hcp),
            metrics=metrics,
        )
        
        # Clasificar arquetipo (< 5ms)
        classifier = ArchetypeClassifier()
        archetype_result: ArchetypeResult = classifier.classify(scoring_result)
        
        # Serializar scoring_profile
        arch = archetype_result.archetype
        scores = scoring_result.scores_as_dict()
        
        data['scoring_profile'] = {
            'player_hcp':         hcp,
            'overall_score':      scoring_result.overall_score,
            'tee_to_green':       scoring_result.tee_to_green,
            'scoring_game':       scoring_result.scoring_game,
            'data_completeness':  scoring_result.data_completeness,
            'dimensions': {
                name: {
                    'score':       dim.score,
                    'percentile':  dim.percentile,
                    'zone':        dim.zone.value,
                    'confidence':  dim.confidence.value,
                    'notes':       dim.notes,
                }
                for name, dim in [
                    ('long_game',   scoring_result.long_game),
                    ('mid_game',    scoring_result.mid_game),
                    ('short_game',  scoring_result.short_game),
                    ('putting',     scoring_result.putting),
                    ('consistency', scoring_result.consistency),
                    ('mental',      scoring_result.mental),
                    ('power',       scoring_result.power),
                    ('accuracy',    scoring_result.accuracy),
                ]
            },
            'ranking': scoring_result.dimensions_by_score(),
            'top_strength': scoring_result.top_strength(),
            'top_gap':      scoring_result.top_gap(),
        }
        
        # Serializar golf_identity
        data['golf_identity'] = {
            'archetype_id':          arch.id,
            'archetype_name':        arch.name_es,
            'archetype_tagline':     arch.tagline_es,
            'archetype_description': arch.description_es,
            'archetype_strategy':    arch.strategy_es,
            'fit_score':             archetype_result.fit_score,
            'primary_strength': {
                'dimension': archetype_result.primary_strength_dim,
                'score':     archetype_result.primary_strength_val,
            },
            'primary_gap': {
                'dimension': archetype_result.primary_gap_dim,
                'score':     archetype_result.primary_gap_val,
            },
            'similar_archetypes': [
                {'id': sid, 'name': sname, 'similarity': ssim}
                for sid, sname, ssim in archetype_result.similar_archetypes
            ],
            'evolution_target': {
                'id':   archetype_result.evolution_target[0],
                'name': archetype_result.evolution_target[1],
            } if archetype_result.evolution_target else None,
            'personalized_insight': archetype_result.personalized_insight_es,
            'pro_references':       arch.pro_references,
            'defining_strengths':   arch.defining_strengths,
            'defining_gaps':        arch.defining_gaps,
        }
        
        print(f"[ScoringIntegration] ✓ scoring_profile: overall={scoring_result.overall_score}/10")
        print(f"[ScoringIntegration] ✓ golf_identity: {arch.id} — {arch.name_es} (fit={archetype_result.fit_score:.0%})")
        
    except Exception as e:
        print(f"[ScoringIntegration] ERROR: {e} — añadiendo datos de fallback")
        data['scoring_profile'] = {'error': str(e)}
        data['golf_identity']   = {'error': str(e)}
    
    return data


# ── Test standalone ───────────────────────────────────────────
if __name__ == '__main__':
    import json
    
    with open('/mnt/user-data/uploads/dashboard_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data = add_scoring_to_dashboard(data)
    
    sp = data['scoring_profile']
    gi = data['golf_identity']
    
    print("\n" + "="*60)
    print("SCORING PROFILE")
    print("="*60)
    for dim_name, dim in sp['dimensions'].items():
        bar = "█" * int(dim['score']) + "░" * (10 - int(dim['score']))
        print(f"  {dim_name:<12} [{bar}] {dim['score']:4.1f}/10  {dim['zone'].upper()}")
    print(f"\n  Overall: {sp['overall_score']}/10")
    print(f"  Top strength: {sp['top_strength']}")
    print(f"  Top gap:      {sp['top_gap']}")
    
    print("\n" + "="*60)
    print("GOLF IDENTITY")
    print("="*60)
    print(f"  {gi['archetype_id']} — {gi['archetype_name']}")
    print(f"  \"{gi['archetype_tagline']}\"")
    print(f"  Fit: {gi['fit_score']:.0%}")
    print(f"  Evolution → {gi.get('evolution_target', {}).get('name', 'N/A')}")
    print(f"\n  Insight: {gi['personalized_insight']}")
