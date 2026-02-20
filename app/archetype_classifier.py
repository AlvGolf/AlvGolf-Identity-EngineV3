"""
AlvGolf — Archetype Classifier
================================
Clasificador determinista que asigna una Golf Identity (arquetipo)
a partir del vector de scores 0-10 generado por ScoringEngine.

FILOSOFÍA DE DISEÑO:
Un arquetipo no es solo una etiqueta — es un MAPA que le dice al jugador:
  1. Quién eres como golfista hoy
  2. Cuál es tu patrón de fortalezas y debilidades
  3. Qué estrategia de mejora tiene más ROI para tu perfil
  4. En qué arquetipo puedes convertirte si trabajas las áreas correctas

TAXONOMÍA: 12 arquetipos cubriendo todos los perfiles amateur reales.
Organizados en 4 familias según la dimensión dominante:

  FAMILIA A — Dominantes en juego largo / potencia:
    A1: El Bombardero Descontrolado
    A2: El Artillero Técnico
    A3: El Especialista en Distancia

  FAMILIA B — Dominantes en juego corto / green:
    B1: El Mago del Short Game
    B2: El Maestro del Green
    B3: El Artista Completo (short+putting)

  FAMILIA C — Dominantes en consistencia / mental:
    C1: El Estratega Calculador
    C2: El Jugador de Torneo
    C3: El Sólido Amateur

  FAMILIA D — Perfiles en desarrollo / mixtos:
    D1: El Jugador en Transición
    D2: El Potencial sin Pulir
    D3: El Amateur Completo

ÁRBOL DE DECISIÓN:
El clasificador aplica un árbol de decisión en 4 niveles:
  Nivel 1: Identifica el patrón de scores extremos (>7.5 o <4.0)
  Nivel 2: Determina la familia dominante (A/B/C/D)
  Nivel 3: Selecciona el arquetipo específico dentro de la familia
  Nivel 4: Ajusta por factores secundarios (HCP, consistencia)

Autor: AlvGolf / Álvaro Peralta
Versión: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from app.scoring_engine import ScoringResult, Zone


# ══════════════════════════════════════════════════════════════
# DATACLASSES
# ══════════════════════════════════════════════════════════════

@dataclass
class Archetype:
    """
    Definición estática de un arquetipo de Golf Identity.
    Estos son los "tipos" posibles — el resultado de clasificación
    apunta a uno de estos objetos.
    """
    id:               str          # e.g. "B1"
    name_es:          str          # Nombre del arquetipo en español
    tagline_es:       str          # Frase corta (para UI)
    description_es:   str          # Descripción completa (150-200 palabras)
    
    # Condiciones que definen este arquetipo (para documentación)
    defining_strengths: List[str]  # Dimensiones que deben ser altas (>6.5)
    defining_gaps:      List[str]  # Dimensiones que suelen ser bajas (<5.5)
    
    # Estrategia de mejora específica para este arquetipo
    strategy_es:      str          # Recomendación táctica (100-150 palabras)
    
    # Evolución posible
    can_evolve_to:    List[str]    # IDs de arquetipos alcanzables con mejora
    evolved_from:     List[str]    # IDs de arquetipos que evolucionan a este
    
    # Referentes del golf profesional (para motivación)
    pro_references:   List[str]    # Jugadores PGA/LIV con perfil similar


@dataclass
class ArchetypeResult:
    """
    Resultado de clasificar a un jugador en un arquetipo.
    
    Contiene el arquetipo asignado + contexto personalizado
    calculado a partir de los scores reales del jugador.
    """
    archetype:            Archetype
    
    # Puntuación de ajuste (0-1): qué tan bien encaja el jugador en este arquetipo
    # 1.0 = perfecto match, 0.6 = match razonable con matices
    fit_score:            float
    
    # Fortaleza y gap primarios (de los scores reales)
    primary_strength_dim:  str     # Nombre de la dimensión más fuerte
    primary_strength_val:  float   # Score de esa dimensión
    primary_gap_dim:       str     # Nombre de la dimensión más débil
    primary_gap_val:       float   # Score de esa dimensión
    
    # Arquetipos cercanos (para UI "También podrías ser...")
    similar_archetypes:   List[Tuple[str, str, float]]  # (id, name, similarity_score)
    
    # Arquetipo objetivo (evolución natural)
    evolution_target:     Optional[Tuple[str, str]]     # (id, name)
    
    # Insight personalizado generado por el clasificador
    personalized_insight_es: str   # 2-3 frases con datos reales del jugador


# ══════════════════════════════════════════════════════════════
# TAXONOMÍA DE ARQUETIPOS (12 arquetipos)
# ══════════════════════════════════════════════════════════════

ARCHETYPES: Dict[str, Archetype] = {

    # ── FAMILIA A: Dominantes en largo / potencia ──────────────

    "A1": Archetype(
        id="A1",
        name_es="El Bombardero Descontrolado",
        tagline_es="Mucha potencia, poca dirección",
        description_es=(
            "Tienes uno de los swings más potentes del campo, capaz de "
            "generar distancias que dejan boquiabiertos a tus compañeros. "
            "El problema es que esa energía no siempre va donde quieres: "
            "tus drives pueden terminar en cualquier parte del hoyo, y la "
            "dispersión alta te cuesta golpes que tu potencial no merece. "
            "Tu juego corto es funcional pero no compensa las penalizaciones "
            "del tee. El putting y la gestión del campo son áreas que apenas "
            "has desarrollado porque siempre estás intentando salir del rough "
            "o los árboles. Con disciplina técnica —especialmente en el control "
            "de la cara del palo— podrías transformar esa potencia en ventaja "
            "real. Eres el jugador que más disfruta el campo de prácticas "
            "golpeando drivers, y eso es exactamente donde debes invertir "
            "tu energía: canalizarla, no frenarla."
        ),
        defining_strengths=["power"],
        defining_gaps=["accuracy", "consistency", "mental"],
        strategy_es=(
            "Prioridad absoluta: face-to-path. Reduce la apertura de cara "
            "de +4-6° a ±2° en 6 semanas con drills de grip y release. "
            "No busques más distancia —ya tienes suficiente. Busca fairways. "
            "Cada fairway adicional por ronda vale ~0.8 golpes. Con 5 fairways "
            "extra/semana en práctica = 1.5 golpes/ronda en 8 semanas. "
            "Segundo paso: gestión de campo. Juega 'fairway iron' en hoyos "
            "de rough peligroso aunque pierdas 30m. El rough te cuesta más "
            "que esos metros."
        ),
        can_evolve_to=["A2", "D3"],
        evolved_from=["D2"],
        pro_references=["John Daly (joven)", "Bubba Watson (antes del control)"],
    ),

    "A2": Archetype(
        id="A2",
        name_es="El Artillero Técnico",
        tagline_es="Potencia con control emergente",
        description_es=(
            "Has logrado algo que muy pocos amateurs consiguen: combinar "
            "distancias de élite con un nivel técnico sólido. Tu driver "
            "es largo Y razonablemente preciso, lo que te da una ventaja "
            "real en pares 5 y hoyos largos. Tus hierros medios son tu "
            "segundo punto fuerte —llegas a greens donde otros ni lo "
            "intentan. La brecha en tu juego está en la zona de scoring: "
            "el juego corto y putting necesitan el mismo rigor técnico "
            "que has aplicado al swing largo. Tienes la mentalidad correcta "
            "(buscas mejorar técnicamente, no solo golpear fuerte) y eso "
            "te diferencia del Bombardero. Tu reto ahora es 'complete the "
            "package': un short game a nivel de tu long game te dejaría "
            "en HCP 10-12 en 18-24 meses."
        ),
        defining_strengths=["power", "long_game", "mid_game"],
        defining_gaps=["short_game", "putting"],
        strategy_es=(
            "Tu long game ya no necesita mucho trabajo —está bien. "
            "Invierte el 60% de tu tiempo de práctica en cuña y putting. "
            "Objetivo: llevar tu short game del percentil actual al percentil "
            "70 en 12 semanas. Eso equivale a ~2-3 golpes/ronda. "
            "Plan: 3 sesiones/semana de 30min exclusivamente cuñas a "
            "distancias fijas (50, 75, 100m). Mide la dispersión en cada "
            "sesión. Cuando lateral_std PW baje de 8m, empieza con putting "
            "desde 3-5m (make rate objetivo: 70%)."
        ),
        can_evolve_to=["D3"],
        evolved_from=["A1"],
        pro_references=["Jon Rahm", "Dustin Johnson (completo)"],
    ),

    "A3": Archetype(
        id="A3",
        name_es="El Especialista en Distancia",
        tagline_es="Velocidad de tour, juego de campo corto",
        description_es=(
            "Tu velocidad de swing es genuinamente excepcional para un "
            "amateur —estás en el top 10-15% de velocidad pura. El "
            "problema es que esa velocidad no se convierte en distancia "
            "real porque el contacto y el control técnico no están a la "
            "altura. Tu smash factor bajo indica que estás perdiendo "
            "mucha energía en el impacto: pegas muy fuerte pero no "
            "eficientemente. Parece paradójico, pero pegarías más lejos "
            "con menos esfuerzo si mejoraras el contacto. Tu mid y short "
            "game están claramente por debajo de lo que tu HCP sugiere. "
            "Eres el jugador que todos subestiman en el tee y luego "
            "ven luchar desde el hoyo 4 en adelante."
        ),
        defining_strengths=["power"],
        defining_gaps=["mid_game", "short_game", "accuracy"],
        strategy_es=(
            "Contra-intuitivo pero crucial: trabaja a 80% de velocidad. "
            "El objetivo no es más velocidad —es mejor smash factor. "
            "De 1.38 a 1.44 = +15 metros sin cambiar nada más. "
            "Drill: impact tape en el driver durante 4 semanas. "
            "Objetivo: 70% de strikes en zona central. "
            "Paralelo: invierte en tu mid-iron. Tu hierro 7 necesita "
            "carry consistente. 20 bolas diarias a distancia fija, "
            "midiendo dispersión. Cuando CV < 7%, el juego mejora solo."
        ),
        can_evolve_to=["A1", "A2"],
        evolved_from=[],
        pro_references=["Cameron Champ (joven)", "Bryson DeChambeau (pre-técnica)"],
    ),

    # ── FAMILIA B: Dominantes en juego corto / green ──────────

    "B1": Archetype(
        id="B1",
        name_es="El Mago del Short Game",
        tagline_es="Salva golpes donde otros no pueden",
        description_es=(
            "Tu habilidad alrededor del green es genuinamente élite. "
            "Con una cuña en la mano, eres capaz de hacer pares y birdies "
            "desde sitios donde tus compañeros dan el hoyo por perdido. "
            "Tu scrambling es excepcional, tu touch con las cuñas es "
            "natural, y has desarrollado una sensibilidad para la "
            "distancia que tarda años en construirse. El precio de "
            "esta especialización es que has llegado demasiado tarde "
            "al green con demasiada frecuencia: tu juego largo y mid "
            "necesitan trabajo. La buena noticia es que tienes el "
            "perfil correcto para bajar rápido de HCP: cuando mejores "
            "la llegada al green, ese short game élite multiplicará "
            "su impacto. Eres el jugador que nunca se rinde en un hoyo "
            "y eso, en competición, vale más de lo que muestra el HCP."
        ),
        defining_strengths=["short_game"],
        defining_gaps=["long_game", "power"],
        strategy_es=(
            "Tu short game ya está donde tiene que estar. No lo toques. "
            "Foco 100% en el largo: necesitas llegar más cerca del green "
            "para que ese short game explote de verdad. "
            "Prioridad 1: ataque angle con driver. Subir de negativo a "
            "+2° te dará 12-18 metros sin más esfuerzo. "
            "Prioridad 2: smash factor con hierros medios. "
            "De mejorar el largo +2 golpes/ronda, tu short game "
            "convertirá esos 2 en 3-4 golpes reales. El ROI es enorme."
        ),
        can_evolve_to=["B3", "D3"],
        evolved_from=["D1"],
        pro_references=["José María Olazábal", "Seve Ballesteros"],
    ),

    "B2": Archetype(
        id="B2",
        name_es="El Maestro del Green",
        tagline_es="Los putts son tu superpoder",
        description_es=(
            "En el green, eres otro jugador. Tu putting está claramente "
            "por encima de tu HCP —con frecuencia salvas rondas con el "
            "putter que deberían haber acabado en números mucho peores. "
            "Tienes una lectura de greens excepcional, un ritmo de "
            "putter estable, y bajo presión tu putting mejora en lugar "
            "de empeorar. El SG Putting positivo es el diferencial que "
            "te separa de jugadores con mejor juego largo. La limitación "
            "es que dependes demasiado del putter para sobrevivir rondas "
            "donde el juego desde tee y los hierros no funcionan. Cuando "
            "el putter calla —cosa que pasa a todos— no tienes red de "
            "seguridad en el short game. Un buen día de putting con mejor "
            "largo sería devastadoramente bueno para tu score."
        ),
        defining_strengths=["putting"],
        defining_gaps=["long_game", "mid_game"],
        strategy_es=(
            "Preserva tu putting. No cambies nada en el green. "
            "Construye el juego que alimenta ese putter: "
            "necesitas llegar al green con más frecuencia y más cerca. "
            "GIR es tu métrica clave. Por cada 5% de mejora en GIR "
            "= ~1 golpe/ronda (y tu putter convierte esos GIR mucho "
            "mejor que el promedio). "
            "Plan: hierros 5-7 con técnica de descenso y compresión. "
            "Objetivo: lateral_std < 10m con 7 hierro en 8 semanas."
        ),
        can_evolve_to=["B3", "C2"],
        evolved_from=[],
        pro_references=["Brad Faxon", "Luke Donald"],
    ),

    "B3": Archetype(
        id="B3",
        name_es="El Artista Completo",
        tagline_es="Short game + putting como ventaja real",
        description_es=(
            "Has construido algo valioso: una combinación de short game "
            "sólido Y putting por encima del promedio. Esto significa que "
            "cada vez que llegas razonablemente cerca del green, tienes "
            "una alta probabilidad de hacer el hoyo bien. Tu scrambling "
            "es un seguro de vida en rondas difíciles. Lo que te falta "
            "para dar el siguiente salto es llegar más y mejor: si el "
            "largo mejora, la zona donde más brillas (50m hacia el hole) "
            "se activará con más frecuencia. Eres el jugador ideal para "
            "competición en formato stableford o matchplay —tu gestión "
            "del daño es excelente y rara vez anotas grandes números. "
            "Con trabajo en el largo, HCP <15 es un objetivo real."
        ),
        defining_strengths=["short_game", "putting"],
        defining_gaps=["long_game", "power"],
        strategy_es=(
            "Zona de confort actual: bien. Siguiente nivel: el largo. "
            "No necesitas ser un bombardero. Necesitas ser consistente "
            "desde tee. Objetivo realista: 55% fairways (desde tu nivel "
            "actual) en 10 semanas. Drill principal: eje de rotación "
            "en driver —face-to-path de ±1° a ±2°, no más. "
            "Cada fairway que ganes activa tu zona fuerte antes en el hoyo. "
            "El ROI de este cambio en tu perfil es el más alto posible."
        ),
        can_evolve_to=["D3"],
        evolved_from=["B1", "B2"],
        pro_references=["Corey Pavin", "Zach Johnson"],
    ),

    # ── FAMILIA C: Dominantes en consistencia / mental ─────────

    "C1": Archetype(
        id="C1",
        name_es="El Estratega Calculador",
        tagline_es="Gestión del campo como ventaja competitiva",
        description_es=(
            "Tu juego técnico es moderado pero tu cabeza está claramente "
            "por encima de tu HCP. Tomas mejores decisiones que la mayoría "
            "de jugadores con tu nivel técnico: eliges bien el palo, "
            "juegas a zonas seguras del green, rara vez intentas golpes "
            "imposibles. Tu F9/B9 delta es mínimo y tu bounce-back rate "
            "es excelente —cuando haces un mal hoyo, no te afecta. "
            "El resultado es que tu score suele ser mejor de lo que "
            "merecería tu swing. La limitación: hay un techo físico. "
            "Sin cierta mejora técnica, la estrategia sola no baja "
            "del HCP 15-18. Pero si combinas tu mentalidad con técnica "
            "mejorada, el salto será espectacular."
        ),
        defining_strengths=["mental", "consistency"],
        defining_gaps=["power", "long_game"],
        strategy_es=(
            "Tu activo es el cerebro. Ahora añade herramientas técnicas. "
            "Prioridad 1: distancia con hierros. Un jugador estratégico "
            "con 10m más de carry en hierros medios gana 2 opciones "
            "de ataque por hoyo. Eso multiplica tu ventaja de gestión. "
            "Prioridad 2: ataque angle con driver +1° adicional = "
            "10 metros más sin cambiar mentalidad. "
            "Mantén tu rutina de pre-shot (probablemente ya la tienes). "
            "No cambies lo que funciona. Solo añade potencia."
        ),
        can_evolve_to=["C2", "D3"],
        evolved_from=["D1"],
        pro_references=["Nick Faldo", "Bernhard Langer"],
    ),

    "C2": Archetype(
        id="C2",
        name_es="El Jugador de Torneo",
        tagline_es="Mejor bajo presión que en práctica",
        description_es=(
            "Hay jugadores que juegan mejor cuanto más importa el "
            "resultado. Tú eres uno de ellos. Tu rendimiento en "
            "competición supera al de tus rondas casuales —el nervio "
            "te activa en lugar de paralizarte. Tu consistencia entre "
            "rondas es alta, tu gestión de errores es madura, y sabes "
            "cuándo jugar conservador y cuándo atacar. Tu SG Putting "
            "bajo presión es un indicador concreto de mentalidad ganadora. "
            "Técnicamente estás en un nivel sólido sin ser brillante en "
            "ninguna dimensión específica. Esto es bueno en competición "
            "(no tienes puntos débiles evidentes) pero limita tu techo "
            "a largo plazo. Para bajar más HCP necesitas al menos una "
            "dimensión de élite que te diferencie."
        ),
        defining_strengths=["mental", "consistency", "putting"],
        defining_gaps=["power"],
        strategy_es=(
            "Eres completo. El siguiente paso es añadir UN arma élite. "
            "Identifica cuál dimensión tiene más potencial en tu caso "
            "y especialízate 3 meses en ella. No lo hagas con todo. "
            "Opciones: (a) short game a percentil 85+ = arma de torneo "
            "letal, (b) driver a fairway 60%+ = ventaja estructural. "
            "Tu mentalidad ya está. Ahora necesitas la herramienta."
        ),
        can_evolve_to=["D3"],
        evolved_from=["C1", "B2"],
        pro_references=["Sergio García", "Rory McIlroy (2011-2012)"],
    ),

    "C3": Archetype(
        id="C3",
        name_es="El Sólido Amateur",
        tagline_es="Consistente, equilibrado, fiable",
        description_es=(
            "Eres el modelo de amateur equilibrado: sin brillar en ninguna "
            "dimensión específica, tampoco tienes agujeros graves en tu "
            "juego. Tu scorecard rara vez muestra números explosivos en "
            "ninguna dirección —ni birdies encadenados ni grandes "
            "desastres. Tu HCP refleja fielmente tu nivel real, sin "
            "oscilaciones grandes entre rondas. Esta solidez es valiosa "
            "en matchplay y equipo, donde la consistencia importa más "
            "que el brillantismo. El riesgo del Jugador Sólido es el "
            "estancamiento: si no hay área de trabajo prioritaria clara, "
            "el HCP puede quedarse estático. La clave es elegir UNA "
            "dimensión e invertir tiempo real en ella durante 3 meses."
        ),
        defining_strengths=["consistency"],
        defining_gaps=[],  # No hay gaps extremos — el perfil es equilibrado
        strategy_es=(
            "El peligro de tu perfil es no tener urgencia de mejora. "
            "Todo funciona 'bastante bien'. Para bajar HCP, necesitas "
            "romper esa homogeneidad. Elige la dimensión con más potencial "
            "de mejora rápida (normalmente short game o putting) y "
            "trabájala de forma intensiva. 60% del tiempo de práctica "
            "en esa única área durante 10 semanas. La especialización "
            "temporal es el camino para jugadores con tu perfil."
        ),
        can_evolve_to=["B3", "C2", "D3"],
        evolved_from=["D1"],
        pro_references=["Steve Stricker", "Jim Furyk"],
    ),

    # ── FAMILIA D: Perfiles en desarrollo / transición ─────────

    "D1": Archetype(
        id="D1",
        name_es="El Jugador en Transición",
        tagline_es="Construyendo las bases del juego",
        description_es=(
            "Estás en una fase de aprendizaje activo donde múltiples "
            "dimensiones de tu juego están mejorando simultáneamente. "
            "Esto es natural en etapas de reducción de HCP desde niveles "
            "altos (28-36) y refleja un jugador que lleva menos de 2-3 "
            "años practicando con regularidad o que ha tenido un cambio "
            "técnico importante reciente. La buena noticia: en esta fase "
            "los avances son rápidos porque cada hora de práctica bien "
            "orientada genera mejoras visibles. La clave es no intentar "
            "mejorar todo a la vez. El mayor error del jugador en "
            "transición es cambiar el foco de trabajo cada semana. "
            "Elige uno o dos fundamentos y dales tiempo. La paciencia "
            "ahora genera aceleración después."
        ),
        defining_strengths=[],
        defining_gaps=["consistency", "mental"],
        strategy_es=(
            "Regla de oro: un foco por mes. No más. "
            "Mes 1: el fundamento más básico (grip, postura, o ataque angle "
            "según diagnóstico). "
            "Mes 2: el segundo fundamento. No antes. "
            "Métricas de progreso: lleva registro de 3 métricas simples "
            "por ronda (fairways, GIR, putts). Ver el número mejorar "
            "semana a semana es el motor de motivación más potente. "
            "Busca un coach para 2-3 sesiones mensuales de orientación."
        ),
        can_evolve_to=["C3", "B1", "A1"],
        evolved_from=[],
        pro_references=["Cualquier tour pro en sus primeros años amateur"],
    ),

    "D2": Archetype(
        id="D2",
        name_es="El Potencial sin Pulir",
        tagline_es="Talento físico esperando técnica",
        description_es=(
            "Tienes algo que no se puede entrenar fácilmente: velocidad "
            "de swing y coordinación atletica natural. Tus datos de "
            "velocidad y potencia superan a jugadores con tu HCP, lo "
            "que significa que hay mucho rendimiento latente esperando "
            "ser liberado. El gap entre tu potencial físico y tu score "
            "actual es grande —y eso es una buena noticia, porque ese "
            "gap se cierra con técnica, no con más esfuerzo físico. "
            "Probablemente llegaste al golf desde otro deporte, o "
            "aprendiste solo sin mucha instrucción técnica. Tu swing "
            "tiene potencia pero no estructura. Con 6-9 meses de "
            "trabajo técnico orientado, podrías perder 5-8 puntos de "
            "HCP más rápido que la media."
        ),
        defining_strengths=["power"],
        defining_gaps=["consistency", "accuracy", "short_game"],
        strategy_es=(
            "Aprovecha el talento con estructura técnica. "
            "Prioridad absoluta: face-to-path y ataque angle. "
            "Son los dos parámetros que más impactan en convertir "
            "velocidad en distancia Y dirección. "
            "Secundario: short game. Un jugador con tu velocidad "
            "que desarrolle short game competente baja a HCP 15 "
            "en 18-24 meses. El camino está claro, solo necesita "
            "consistencia en el trabajo."
        ),
        can_evolve_to=["A1", "A2"],
        evolved_from=[],
        pro_references=["Cameron Champ", "Tony Finau (joven)"],
    ),

    "D3": Archetype(
        id="D3",
        name_es="El Amateur Completo",
        tagline_es="Equilibrio de alto nivel en todas las dimensiones",
        description_es=(
            "Has conseguido algo que muy pocos amateurs logran: un nivel "
            "sólido en todas las dimensiones sin agujeros graves. No "
            "tienes una dimensión en zone FOCUS_AREA —todas están en "
            "DEVELOPING o superior. Esto, combinado con un HCP bajo-medio "
            "(<18), te coloca en el tier más alto del amateur. Tu juego "
            "es completo, difícil de leer para rivales, y consistente "
            "bajo presión. Las áreas de mejora existen, pero son matices "
            "—optimizaciones de rendimiento ya sólido, no fundamentos "
            "que construir. Eres el jugador que todos los coaches quieren "
            "tener como alumno porque responde bien al trabajo técnico "
            "refinado. Llegar a HCP <10 es un objetivo plausible con "
            "dedicación sostenida."
        ),
        defining_strengths=["long_game", "mid_game", "short_game", "putting"],
        defining_gaps=[],
        strategy_es=(
            "En tu nivel, la mejora viene de los márgenes. "
            "Identifica las 2 dimensiones con mayor diferencia entre "
            "tu score actual y el score de HCP objetivo. "
            "Esas son tus palancas. "
            "Para bajar de HCP 15 a HCP 10: typically SG_Approach "
            "y SG_Putting marcan la diferencia. "
            "Trabaja con un coach de alto nivel 2x/mes para análisis "
            "de datos y ajustes técnicos. A este nivel el ojo experto "
            "vale más que el volumen de práctica."
        ),
        can_evolve_to=[],
        evolved_from=["A2", "B3", "C2", "C3"],
        pro_references=["Rory McIlroy", "Viktor Hovland", "Scottie Scheffler"],
    ),
}


# ══════════════════════════════════════════════════════════════
# CLASSIFIER
# ══════════════════════════════════════════════════════════════

class ArchetypeClassifier:
    """
    Clasificador determinista de Golf Identity para AlvGolf.
    
    Implementa un árbol de decisión en 4 niveles que asigna
    uno de los 12 arquetipos a partir del ScoringResult del jugador.
    
    GARANTÍA DE DETERMINISMO: Para el mismo ScoringResult, siempre
    asigna el mismo arquetipo. No hay aleatoriedad ni inferencia.
    """

    # Umbrales del árbol de decisión (documentados para patent)
    ELITE_THRESHOLD    = 7.5   # Score que define una dimensión como "élite"
    STRONG_THRESHOLD   = 6.5   # Score que define una dimensión como "fuerte"
    GAP_THRESHOLD      = 4.5   # Score por debajo del cual es un gap prioritario
    CRITICAL_THRESHOLD = 3.5   # Score que define un gap crítico

    def classify(self, result: ScoringResult) -> ArchetypeResult:
        """
        Clasifica al jugador en un arquetipo.
        
        Árbol de decisión en 4 niveles:
          L1: Detectar dimensiones extremas (élite o gap crítico)
          L2: Determinar familia dominante (A/B/C/D)
          L3: Seleccionar arquetipo específico
          L4: Ajustar por HCP y contexto
        
        Args:
            result: ScoringResult del ScoringEngine
            
        Returns:
            ArchetypeResult con arquetipo asignado y contexto personalizado
        """
        scores = result.scores_as_dict()
        hcp = result.player_hcp

        # ── Nivel 1: Detectar dimensiones extremas ─────────────
        elite_dims  = [d for d, s in scores.items() if d != "overall" and s >= self.ELITE_THRESHOLD]
        strong_dims = [d for d, s in scores.items() if d != "overall" and self.STRONG_THRESHOLD <= s < self.ELITE_THRESHOLD]
        gap_dims    = [d for d, s in scores.items() if d != "overall" and s <= self.GAP_THRESHOLD]
        critical_dims = [d for d, s in scores.items() if d != "overall" and s <= self.CRITICAL_THRESHOLD]

        # ── Nivel 2-3: Árbol de decisión por familia ───────────
        archetype_id = self._decision_tree(scores, elite_dims, strong_dims, gap_dims, critical_dims, hcp)
        archetype = ARCHETYPES[archetype_id]

        # ── Nivel 4: Calcular fit score ────────────────────────
        fit_score = self._calculate_fit(scores, archetype)

        # Fortaleza y gap primarios (de los datos reales)
        strength_name, strength_val = result.top_strength()
        gap_name, gap_val = result.top_gap()

        # Arquetipos similares
        similar = self._get_similar_archetypes(archetype_id, scores)

        # Arquetipo de evolución
        evolution = self._get_evolution_target(archetype, scores, hcp)

        # Insight personalizado
        insight = self._generate_insight(result, archetype, strength_name, strength_val, gap_name, gap_val)

        return ArchetypeResult(
            archetype=archetype,
            fit_score=round(fit_score, 2),
            primary_strength_dim=strength_name,
            primary_strength_val=round(strength_val, 2),
            primary_gap_dim=gap_name,
            primary_gap_val=round(gap_val, 2),
            similar_archetypes=similar,
            evolution_target=evolution,
            personalized_insight_es=insight,
        )

    def _decision_tree(
        self,
        scores: dict,
        elite_dims: list,
        strong_dims: list,
        gap_dims: list,
        critical_dims: list,
        hcp: float,
    ) -> str:
        """
        Árbol de decisión principal.
        
        LÓGICA (documentada para transparencia y patent):
        
        El árbol prioriza patrones de COMBINACIÓN, no dimensiones aisladas.
        Un score alto en power con gap en accuracy → A1, no "potente y preciso".
        
        Orden de evaluación:
        1. Patrones de élite dominante (una dimensión muy por encima de las demás)
        2. Patrones de gap dominante (una dimensión muy por debajo)
        3. Patrones de consistencia/mental
        4. Perfil equilibrado (ningún extremo)
        """

        # ── RAMA A: Power / Long Game dominante ────────────────

        if "power" in elite_dims:
            # Power élite — ¿va acompañado de accuracy?
            if "accuracy" in gap_dims or "consistency" in gap_dims:
                return "A1"  # Bombardero: potente pero descontrolado
            elif "long_game" in elite_dims or "mid_game" in strong_dims:
                return "A2"  # Artillero Técnico: potente Y con control emergente
            else:
                return "A3"  # Especialista en Distancia: velocidad sin conversión

        if "long_game" in elite_dims and "power" not in elite_dims:
            # Long game élite sin power élite → resultado de técnica, no fuerza
            if "short_game" in gap_dims or "putting" in gap_dims:
                return "A2"  # Artillero sin juego corto
            return "A2"

        # ── RAMA B: Short Game / Putting dominante ─────────────

        if "short_game" in elite_dims and "putting" in elite_dims:
            return "B3"  # Artista Completo: ambas zonas de scoring élite

        if "short_game" in elite_dims:
            if "long_game" in gap_dims or "power" in gap_dims:
                return "B1"  # Mago del Short Game: dependiente del short
            return "B3"  # Short élite sin gaps graves → casi completo

        if "putting" in elite_dims:
            if "long_game" in gap_dims or "mid_game" in gap_dims:
                return "B2"  # Maestro del Green: putter salva rondas
            return "B2"

        if "short_game" in strong_dims and "putting" in strong_dims:
            if "long_game" not in gap_dims and "mid_game" not in gap_dims:
                return "B3"  # B3 también con strong (no solo elite)

        # ── RAMA C: Consistencia / Mental dominante ────────────

        if "mental" in elite_dims and "consistency" in elite_dims:
            if "putting" in strong_dims or "putting" in elite_dims:
                return "C2"  # Jugador de Torneo: mental + putting
            return "C1"  # Estratega Calculador: gestión sin arma

        if "mental" in elite_dims:
            return "C1"  # Mental élite sin otra fortaleza

        if "consistency" in elite_dims:
            # Muy consistente — ¿con qué?
            if len(gap_dims) == 0 and len(critical_dims) == 0:
                return "C3"  # Sólido Amateur: equilibrado y consistente
            return "C1"

        # ── RAMA D: Perfiles en desarrollo ────────────────────

        # ¿Perfil de élite en múltiples dimensiones? → Amateur Completo
        if len(elite_dims) >= 3 or (len(elite_dims) >= 2 and len(strong_dims) >= 2):
            return "D3"

        # ¿Score global alto y sin gaps críticos? → Amateur Completo
        if scores.get("overall", 0) >= 7.0 and len(critical_dims) == 0:
            return "D3"

        # ¿Power alto pero juego muy por debajo del potencial? → Potencial sin Pulir
        if scores.get("power", 0) >= 6.0 and scores.get("overall", 0) < 5.0:
            return "D2"

        # ¿Score global equilibrado pero ninguna élite? → Sólido (si HCP bajo-medio)
        if hcp <= 20 and len(critical_dims) == 0 and scores.get("overall", 0) >= 5.0:
            return "C3"

        # ¿Múltiples gaps y HCP alto? → En Transición
        if len(gap_dims) >= 3 or hcp >= 28:
            return "D1"

        # ¿Power alto pero mucho por mejorar? → Potencial sin Pulir
        if scores.get("power", 5) >= 5.5 and len(gap_dims) >= 2:
            return "D2"

        # Default: Jugador en Transición (el más seguro cuando el perfil es mixto)
        return "D1"

    def _calculate_fit(self, scores: dict, archetype: Archetype) -> float:
        """
        Calcula qué tan bien encaja el jugador en el arquetipo asignado.
        
        Score 0-1:
        - 1.0: Las fortalezas del arquetipo coinciden exactamente con las del jugador
        - 0.7-0.9: Buen match con alguna excepción
        - 0.5-0.7: Match razonable, podría ser otro arquetipo también
        - <0.5: Borde de clasificación (caso ambiguo)
        
        MÉTODO: Compara los scores del jugador en las dimensiones
        definitorias del arquetipo vs los umbrales esperados.
        """
        fit_points = 0.0
        max_points = 0.0

        # Comprobar fortalezas definitorias del arquetipo
        for dim in archetype.defining_strengths:
            if dim in scores:
                max_points += 1.0
                if scores[dim] >= self.ELITE_THRESHOLD:
                    fit_points += 1.0
                elif scores[dim] >= self.STRONG_THRESHOLD:
                    fit_points += 0.7
                elif scores[dim] >= 5.0:
                    fit_points += 0.4

        # Comprobar gaps definitorios del arquetipo
        for dim in archetype.defining_gaps:
            if dim in scores:
                max_points += 0.5
                if scores[dim] <= self.GAP_THRESHOLD:
                    fit_points += 0.5
                elif scores[dim] <= self.STRONG_THRESHOLD:
                    fit_points += 0.3

        if max_points == 0:
            return 0.75  # Default para D3 y C3 (sin definición estricta)

        return fit_points / max_points

    def _get_similar_archetypes(
        self, current_id: str, scores: dict
    ) -> List[Tuple[str, str, float]]:
        """
        Encuentra los 2 arquetipos más similares al asignado.
        
        Usado en UI para mostrar "También podrías ser..." o
        "Eres un híbrido de X e Y".
        
        Método: distancia euclidiana en el espacio de scores
        comparando con los arquetipos can_evolve_to del actual.
        """
        current = ARCHETYPES[current_id]
        candidates = []

        for aid, arch in ARCHETYPES.items():
            if aid == current_id:
                continue

            # Solo incluir si es evolución posible o familia cercana
            is_related = (
                aid in current.can_evolve_to
                or aid in current.evolved_from
                or aid[0] == current_id[0]  # misma familia
            )
            if not is_related:
                continue

            # Similaridad basada en solapamiento de defining_strengths
            overlap = len(
                set(arch.defining_strengths) & set(current.defining_strengths)
            )
            total = len(
                set(arch.defining_strengths) | set(current.defining_strengths)
            ) or 1
            similarity = overlap / total

            candidates.append((aid, arch.name_es, round(similarity, 2)))

        # Ordenar por similaridad y devolver top 2
        candidates.sort(key=lambda x: x[2], reverse=True)
        return candidates[:2]

    def _get_evolution_target(
        self, archetype: Archetype, scores: dict, hcp: float
    ) -> Optional[Tuple[str, str]]:
        """
        Determina el arquetipo objetivo más probable para este jugador.
        
        Selecciona el primer can_evolve_to que tiene sentido según
        el HCP actual y el patrón de scores.
        """
        if not archetype.can_evolve_to:
            return None

        # Buscar el arquetipo de evolución más cercano en perfil
        for target_id in archetype.can_evolve_to:
            target = ARCHETYPES[target_id]
            # El target es válido si sus defining_strengths son áreas
            # que el jugador ya tiene en DEVELOPING o superior
            applicable = all(
                scores.get(dim, 0) >= 4.0  # Al menos en desarrollo
                for dim in target.defining_strengths
            )
            if applicable:
                return (target_id, target.name_es)

        # Si ninguno es perfectamente aplicable, devolver el primero
        first = archetype.can_evolve_to[0]
        return (first, ARCHETYPES[first].name_es)

    def _generate_insight(
        self,
        result: ScoringResult,
        archetype: Archetype,
        strength_name: str,
        strength_val: float,
        gap_name: str,
        gap_val: float,
    ) -> str:
        """
        Genera un insight personalizado de 2-3 frases con datos reales del jugador.
        
        IMPORTANTE: Este texto usa los datos reales del jugador, no ejemplos genéricos.
        Es el único punto "semi-dinámico" del clasificador — pero sigue siendo
        determinista (mismo input → mismo output).
        """
        dim_names_es = {
            "long_game":   "juego largo",
            "mid_game":    "hierros medios",
            "short_game":  "juego corto",
            "putting":     "putting",
            "consistency": "consistencia",
            "mental":      "juego mental",
            "power":       "potencia",
            "accuracy":    "precisión",
        }

        strength_name_es = dim_names_es.get(strength_name, strength_name)
        gap_name_es = dim_names_es.get(gap_name, gap_name)

        # Determinar zona de la fortaleza y el gap para fraseado
        strength_zone = result.scores_as_dict()
        if strength_val >= 8.5:
            strength_qualifier = "de élite absoluta"
        elif strength_val >= 7.0:
            strength_qualifier = "muy por encima de tu HCP"
        else:
            strength_qualifier = "sólido para tu nivel"

        if gap_val <= 3.5:
            gap_qualifier = "claramente por debajo de tu potencial"
        elif gap_val <= 4.5:
            gap_qualifier = "el área con más margen de mejora"
        else:
            gap_qualifier = "un área con recorrido de mejora"

        insight = (
            f"Eres '{archetype.name_es}' con un {strength_name_es} "
            f"{strength_qualifier} ({strength_val:.1f}/10) que define tu identidad "
            f"en el campo. "
            f"Tu {gap_name_es} es {gap_qualifier} ({gap_val:.1f}/10) y concentra "
            f"el mayor ROI de mejora en tu caso específico. "
            f"Con HCP {result.player_hcp:.1f}, el camino más directo hacia tu siguiente "
            f"nivel es trabajar el {gap_name_es} mientras consolidas tu ventaja "
            f"en {strength_name_es}."
        )

        return insight


# ══════════════════════════════════════════════════════════════
# HELPERS DE CONSULTA
# ══════════════════════════════════════════════════════════════

def get_archetype_by_id(archetype_id: str) -> Optional[Archetype]:
    """Devuelve un arquetipo por su ID. None si no existe."""
    return ARCHETYPES.get(archetype_id)


def list_all_archetypes() -> List[Archetype]:
    """Devuelve todos los arquetipos ordenados por familia."""
    return [ARCHETYPES[k] for k in sorted(ARCHETYPES.keys())]


# ══════════════════════════════════════════════════════════════
# TEST / DEMO
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from scoring_engine import ScoringEngine

    alvaro_metrics = {
        "rounds_count": 52,
        "shots_count": 493,
        "carry_driver_m": 212.8,
        "ball_speed_driver_kmh": 235.5,
        "club_speed_driver_kmh": 164.0,
        "lateral_std_driver_m": 10.2,
        "face_to_path_driver_deg": +4.2,
        "smash_factor_driver": 1.43,
        "driver_shots_count": 45,
        "carry_7iron_m": 145.0,
        "ball_speed_7iron_kmh": 148.0,
        "club_speed_7iron_kmh": 110.0,
        "lateral_std_7iron_m": 9.5,
        "smash_factor_7iron": 1.33,
        "7iron_shots_count": 38,
        "carry_pw_m": 96.1,
        "lateral_std_pw_m": 8.0,
        "pw_shots_count": 55,
        "score_mean": 95.3,
        "score_std_dev": 5.2,
        "fairway_hit_pct": 52,
        "gir_pct": 28,
        "putts_per_round": 33.2,
        "three_putt_pct": 12,
        "scrambling_pct": 45,
        "sg_ott": -1.8,
        "sg_approach": -2.1,
        "sg_arg": +1.8,
        "sg_putt": -0.4,
        "bounce_back_rate_pct": 22,
        "f9_vs_b9_delta": 3.5,
        "par3_vs_par_relative": 1.3,
        "explosion_hole_pct": 8,
        "carry_cv_driver_pct": 5.8,
    }

    engine = ScoringEngine()
    scoring_result = engine.score("alvaro", player_hcp=23.2, metrics=alvaro_metrics)

    classifier = ArchetypeClassifier()
    archetype_result = classifier.classify(scoring_result)

    ar = archetype_result
    arch = ar.archetype

    print("\n" + "=" * 65)
    print(f"  GOLF IDENTITY — {arch.id}: {arch.name_es.upper()}")
    print("=" * 65)
    print(f"  \"{arch.tagline_es}\"")
    print(f"\n  Fit Score: {ar.fit_score:.0%}")
    print(f"\n  Fortaleza principal: {ar.primary_strength_dim} → {ar.primary_strength_val}/10")
    print(f"  Gap principal:       {ar.primary_gap_dim} → {ar.primary_gap_val}/10")
    print(f"\n  DESCRIPCIÓN:")
    # Wrap a 60 chars
    words = arch.description_es.split()
    line = "  "
    for w in words:
        if len(line) + len(w) > 63:
            print(line)
            line = "  " + w + " "
        else:
            line += w + " "
    print(line)

    print(f"\n  ESTRATEGIA:")
    words = arch.strategy_es.split()
    line = "  "
    for w in words:
        if len(line) + len(w) > 63:
            print(line)
            line = "  " + w + " "
        else:
            line += w + " "
    print(line)

    print(f"\n  INSIGHT PERSONALIZADO:")
    words = ar.personalized_insight_es.split()
    line = "  "
    for w in words:
        if len(line) + len(w) > 63:
            print(line)
            line = "  " + w + " "
        else:
            line += w + " "
    print(line)

    if ar.similar_archetypes:
        print(f"\n  ARQUETIPOS SIMILARES:")
        for sid, sname, ssim in ar.similar_archetypes:
            print(f"    {sid}: {sname} (similitud: {ssim:.0%})")

    if ar.evolution_target:
        eid, ename = ar.evolution_target
        print(f"\n  EVOLUCIÓN NATURAL → {eid}: {ename}")

    print(f"\n  REFERENTES PRO: {', '.join(arch.pro_references)}")
    print("=" * 65)
