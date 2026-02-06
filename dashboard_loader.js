/**
 * Dashboard Data Loader
 * Carga datos desde dashboard_data.json y los hace disponibles para el dashboard
 */

// Variable global para almacenar los datos
window.dashboardData = null;

/**
 * Carga los datos del JSON
 */
async function loadDashboardData() {
    try {
        const response = await fetch('output/dashboard_data.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        window.dashboardData = await response.json();
        console.log('✅ Datos del dashboard cargados exitosamente');
        console.log('📊 Datos disponibles:', window.dashboardData);
        return window.dashboardData;
    } catch (error) {
        console.error('❌ Error cargando datos del dashboard:', error);
        return null;
    }
}

/**
 * Obtiene los datos del jugador
 */
function getPlayerStats() {
    return window.dashboardData?.player_stats || {};
}

/**
 * Obtiene las estadísticas de palos
 */
function getClubStatistics() {
    return window.dashboardData?.club_statistics || [];
}

/**
 * Obtiene la evolución temporal
 */
function getTemporalEvolution() {
    return window.dashboardData?.temporal_evolution || {};
}

/**
 * Obtiene las estadísticas por campo
 */
function getCourseStatistics() {
    return window.dashboardData?.course_statistics || [];
}

/**
 * Formatea los datos de club para el formato esperado por el dashboard
 */
function getFormattedClubData() {
    const clubStats = getClubStatistics();
    return clubStats.map(club => ({
        name: club.name,
        distance: club.distance,
        deviation: club.deviation,
        speed: club.speed,
        rating: club.rating,
        category: club.category
    }));
}

/**
 * Genera los labels temporales formateados (ej: "Sep 2024", "Oct", etc.)
 */
function generateTemporalLabels(period_data) {
    // Convertir los períodos (ej: "2024-09") a formato "Sep 2024", "Oct", etc.
    if (!period_data || period_data.length === 0) return [];

    const months = {
        '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
    };

    return period_data.map((period, index) => {
        const [year, month] = period.split('-');
        const monthName = months[month];

        // Mostrar año en el primer mes o cuando cambia el año
        if (index === 0 || (index > 0 && year !== period_data[index - 1].split('-')[0])) {
            return `${monthName} ${year}`;
        }
        return monthName;
    });
}

/**
 * Obtiene datos temporales para un palo específico
 */
function getClubTemporalData(clubCode) {
    const temporal = getTemporalEvolution();
    const clubData = temporal[clubCode];

    if (!clubData) return { labels: [], values: [] };

    return {
        labels: generateTemporalLabels(clubData.labels),
        values: clubData.values
    };
}

/**
 * Actualiza un elemento HTML con un valor de los datos
 */
function updateElement(selector, value) {
    const element = document.querySelector(selector);
    if (element) {
        element.textContent = value;
    }
}

/**
 * Actualiza los elementos del dashboard con los datos cargados
 */
function updateDashboardElements() {
    const playerStats = getPlayerStats();

    // Actualizar estadísticas del jugador
    updateElement('[data-stat="handicap"]', playerStats.handicap_actual);
    updateElement('[data-stat="total-rondas"]', playerStats.total_rondas);
    updateElement('[data-stat="mejor-score"]', playerStats.mejor_score);
    updateElement('[data-stat="promedio-score"]', Math.round(playerStats.promedio_score));
    updateElement('[data-stat="mejora-handicap"]', playerStats.mejora_handicap);

    console.log('✅ Elementos del dashboard actualizados');
}

/**
 * FASE 5 - FUNCIONES DE ACCESO A DATOS AVANZADOS
 */

/**
 * Obtiene los datos de Launch Metrics (Fase 5)
 */
function getLaunchMetrics() {
    return window.dashboardData?.launch_metrics || {};
}

/**
 * Obtiene los datos de Dispersion Analysis (Fase 5)
 */
function getDispersionAnalysis() {
    return window.dashboardData?.dispersion_analysis || {};
}

/**
 * Obtiene los datos de Consistency Benchmarks (Fase 5)
 */
function getConsistencyBenchmarks() {
    return window.dashboardData?.consistency_benchmarks || {};
}

/**
 * Verifica si Fase 5 está habilitada
 */
function isPhase5Enabled() {
    return window.dashboardData?.metadata?.phase_5_enabled || false;
}

/**
 * Inicializa el sistema de carga de datos
 */
async function initDashboardData() {
    console.log('🚀 Inicializando carga de datos del dashboard...');

    const data = await loadDashboardData();

    if (data) {
        // Hacer los datos disponibles globalmente con nombres compatibles
        window.clubData = getFormattedClubData();
        window.playerStats = getPlayerStats();
        window.courseStats = getCourseStatistics();

        // Actualizar elementos HTML si ya están cargados
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', updateDashboardElements);
        } else {
            updateDashboardElements();
        }

        // Disparar evento personalizado para que otros scripts sepan que los datos están listos
        document.dispatchEvent(new CustomEvent('dashboardDataReady', { detail: data }));

        // Log Fase 5 status
        if (isPhase5Enabled()) {
            console.log('✅ Fase 5 habilitada - Datos avanzados disponibles');
        }

        return data;
    }

    console.warn('⚠️ No se pudieron cargar los datos del dashboard');
    return null;
}

// Auto-inicializar cuando se cargue el script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboardData);
} else {
    initDashboardData();
}
