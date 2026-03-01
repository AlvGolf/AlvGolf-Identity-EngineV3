# CLAUDE.md - AlvGolf Multi-Agent System

## Project Overview

**AlvGolf Multi-Agent System** is a comprehensive golf performance analytics platform combining a 360-degree dashboard with a 5-agent AI system. Built for Alvaro Peralta, it provides multi-dimensional analysis of golf performance across 52 rounds spanning 18 months, featuring 36 dynamic data visualizations, 11 golf courses, AI-generated content in Spanish, and complete equipment analytics.

**Primary Language:** Spanish (es)
**Type:** Multi-component system (Static HTML Dashboard + FastAPI Backend + Multi-Agent AI)
**Version:** v3.0.5 - Identity Timeline + Temporal Archetype Evolution (2026-02-25)
**Status:** Production Ready
**Deployment:** Dashboard on GitHub Pages + Backend on localhost:8000

## Repository Structure

```
AlvGolf/
├── app/                              # FastAPI Backend (Agentic Analytics Engine)
│   ├── __init__.py
│   ├── main.py                       # FastAPI app (5 endpoints)
│   ├── config.py                     # Settings management (.env)
│   ├── models.py                     # Pydantic models (12 models)
│   ├── rag.py                        # RAG Core (Pinecone + Claude)
│   └── agents/                       # Multi-Agent System
│       ├── __init__.py
│       ├── orchestrator.py           # LangGraph workflow orchestrator
│       ├── analytics_pro.py          # Legacy Analytics Agent (TIER 1)
│       ├── analista.py               # Team 2: Performance analysis (650 lines)
│       ├── tecnico.py                # Team 2: Biomechanics analysis (550 lines)
│       ├── estratega.py              # Team 2: Practice design (600 lines)
│       ├── ux_writer.py              # Team 3: Dashboard content writer (752 lines)
│       └── coach.py                  # Team 3: Coaching reports (807 lines)
│
├── scripts/                          # Test scripts and utilities
│   ├── test_team3_complete.py        # Team 3 test suite (6 tests)
│   ├── test_optimized_architecture.py
│   ├── test_dashboard_integration.py # E2E tests (4/4)
│   └── ingest_full_data.py           # Data ingestion (120 vectors)
│
│   ├── scoring_engine.py              # Deterministic scoring (0-10, 8 dimensions)
│   ├── archetype_classifier.py       # 12 archetypes across 4 families
│   ├── scoring_integration.py        # Scoring + archetype + timeline integration
│   └── temporal_analysis.py          # Sliding window identity analysis (~375 lines)
│
├── output/
│   └── dashboard_data.json           # Generated data (266.4 KB, 54 keys)
│
├── data/                             # Raw data sources
│   ├── flightscope/                  # 493 shots, 11 clubs
│   └── tarjetas/                     # 52 rounds, 11 courses
│
├── dashboard_dynamic.html            # Main dashboard (v5.3.0, ~17,500 lines)
├── dashboard_agentic.html            # AI Insights dashboard
├── index.html                        # Landing page
├── generate_dashboard_data.py        # Backend generator (53 functions)
│
├── .env                              # API keys (NOT committed)
├── .env.example                      # Template for .env
├── requirements.txt                  # Python dependencies
├── ARCHITECTURE_DIAGRAMS.md          # Mermaid architecture diagrams (8 diagrams)
├── README.md                         # Project documentation
└── .claude/
    └── CLAUDE.md                     # This file
```

## Technology Stack

### Frontend
- **HTML5** - Semantic markup with accessibility support
- **CSS3** - Embedded styles with 11 media queries for responsive design
- **Vanilla JavaScript (ES6+)** - No frameworks, pure JS implementation
- **AI Content Integration** - Async fetch from AgentUXWriter (progressive enhancement)

### Backend (FastAPI)
- **FastAPI** - REST API with 5 endpoints
- **LangGraph** - Multi-agent orchestrator
- **Anthropic Claude Sonnet 4** - LLM for all 5 agents
- **Pinecone** - Vector database (120 vectors, multilingual-e5-large)
- **Pydantic** - Data validation (12 models)
- **Loguru** - Structured logging

### External Dependencies (CDN - Frontend)
- **Chart.js** - `https://cdn.jsdelivr.net/npm/chart.js` - Data visualization (36 charts)
- **html2pdf.js** - `https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js` - PDF export

### External APIs
- **Anthropic API** - Claude Sonnet 4 (LLM calls, prompt caching)
- **Pinecone API** - Serverless vector database (US-East-1)

---

## Multi-Agent System v3.0

### Architecture Overview

The system runs 5 specialized AI agents organized in 2 parallel teams, orchestrated by LangGraph:

```
data_loader_node (106.9 KB JSON, 0 RAG queries)
  |
  v
TEAM 2 PARALLEL (~89s — asyncio.to_thread() v4.1)
  ├── AgentAnalista   (Performance analysis, 11,919 chars)
  ├── AgentTecnico    (Biomechanics analysis, 9,884 chars)
  └── AgentEstratega  (Practice program, 8,818 chars)
  |
  v
TEAM 3 PARALLEL (~112s — asyncio.to_thread() v4.1)
  ├── AgentUXWriter   (Dashboard content, 9,754 chars)
  └── AgentCoach      (Coaching reports, 14,443 chars)
  |
  v
writer_node (Motivational sections, ~1,200 chars)
  |
  v
END (Total: ~56,000 chars, ~3.6 min — was 5.3 min before v4.1)
```

### Agent Specifications

| Agent | Team | Purpose | Output | Lines |
|-------|------|---------|--------|-------|
| AgentAnalista | 2 | Performance analysis | Technical analysis text | 650 |
| AgentTecnico | 2 | Biomechanics patterns | Biomech analysis text | 550 |
| AgentEstratega | 2 | Practice program design | Weekly program | 600 |
| AgentUXWriter | 3 | Dashboard UI content | JSON (6 sections) | 752 |
| AgentCoach | 3 | Coaching reports | Markdown (PDF-ready) | 807 |

### UXWriter Dashboard Integration (v3.0.3)

AgentUXWriter generates **6 content sections** in Spanish inserted into the dashboard.
(Previously described as 10 sections — stat_cards, trend_narratives, course_cards, club_cards
were removed from the skill prompt in v3.0.3 to fix JSON truncation bug.)

1. **hero_statement** (50-80 words) --> Tab 1: Mi Identidad
2. **dna_profile** (30-50 words) --> Tab 1: Mi Identidad
3. **chart_titles** (object) --> All charts across all tabs
4. **insight_boxes** (array) --> Tab 5: Analisis Profundo
5. **quick_wins** (array) --> Tab 6: Estrategia
6. **roi_cards** (array) --> Tab 6: Estrategia

**Frontend Integration Pattern (v3.0.4 - Static Only):**
- `loadUXContent()` -- single source: `output/ai_content.json` (11 lines, zero fallbacks)
- Priority 1 (only): `output/ai_content.json` (pre-generated, loads in <100ms, **instantaneo**)
- `insertUXContent(content)` -- DOM manipulation for 6 content sections + sets `window.coachReportMd`
- Graceful degradation if file unavailable (dashboard works without AI content)
- **CERO llamadas live a localhost:8000** — dashboard 100% estático, GitHub Pages native

**Auto-save of ai_content.json:**
- `/generate-content` endpoint saves ai_content.json after each successful call
- `/analyze` orchestrator also saves ai_content.json at end of full workflow
- File committed to repo so GitHub Pages serves it statically with zero latency

### API Endpoints

| Method | Path | Purpose | Time |
|--------|------|---------|------|
| GET | `/` | Health check | <100ms |
| POST | `/ingest` | Data ingestion to Pinecone | ~2s |
| POST | `/query` | RAG query | 10-15s |
| POST | `/analyze` | Full multi-agent workflow (5 agents) | ~3.6 min |
| POST | `/generate-content` | UXWriter content only | ~60-70s |

### Cost Analysis

- Monthly operational cost: **$0.52/month** (~EUR 0.46)
- Per-call (no cache): $0.185
- Per-call (with cache): $0.110
- Prompt caching saves 90% on skill tokens
- 0 RAG queries (eliminated bottleneck)

### Prompt Caching Implementation (v3.0.2)

All 6 agents use explicit `cache_control` markers via structured LangChain messages:

```python
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content=[{
        "type": "text",
        "text": self.skill_prompt,           # Static skill (2,100-2,800 tokens)
        "cache_control": {"type": "ephemeral"}  # Cached by Anthropic (~5 min TTL)
    }]),
    HumanMessage(content=f"{data_context}\n---\nExecute...")  # Dynamic data (not cached)
]
response = self.llm.invoke(messages)
```

- **Requires:** `default_headers: {"anthropic-beta": "prompt-caching-2024-07-31"}` in ChatAnthropic
- **What's cached:** Skill prompts only (static, same every call)
- **What's NOT cached:** dashboard_data.json (~30K tokens, changes daily)
- **Savings:** -90% input token cost on skill prompts per call

### Key Design Decisions

1. **0 RAG queries:** Replaced Analytics Pro bottleneck with direct JSON loading
2. **Separate /generate-content endpoint:** UXWriter runs standalone (~70s) vs full workflow (~3.6 min)
3. **Static ai_content.json cache:** Pre-generated JSON committed to repo → AI content loads in <100ms (v3.0.3)
4. **Progressive enhancement:** Dashboard loads charts first, AI content loads async (or instant from file)
5. **Graceful degradation:** Dashboard fully functional without backend
6. **Spanish-only:** All AI-generated content in Spanish, motivational tone
7. **Structured messages for caching:** `SystemMessage`+`HumanMessage` with `cache_control` (not plain string invoke)
8. **UXWriter skill prompt = 6 sections only:** Removed descriptions of unused sections to prevent JSON truncation (v3.0.3)
9. **Identity Timeline (v3.0.5):** Sliding window analysis (90d/60d) runs ScoringEngine + ArchetypeClassifier per period. Last period uses full `scoring_profile` + `golf_identity` (not partial window data). Cache fix: always set `window.dashboardData = fresh` from server.
10. **Template vs Data (2026-02-28 → 2026-03-01):** ~216 dynamic IDs (`<span id="xx-*">fallback</span>`) + 7 injection functions + 12 dynamic containers. Dashboard reusable with different player data. Hardcodes remain as visual fallback. `dispatchDashboardReady` waits for `DOMContentLoaded` to ensure all containers exist before injecting.

### Template vs Data System (Dynamic Dashboard Injection)

Pattern for separating template from player data across all 6 tabs + header:

```
<span id="hd-player-name">Álvaro Peralta</span>   ← HTML fallback
         ↓
injectHeaderStats() {                                ← JS injection
    set('hd-player-name', ps.player_name);           ← from JSON
}
         ↓
document.addEventListener('dashboardDataReady', injectHeaderStats, { once: true });
```

**ID Convention:** `{prefix}-{descriptive-name}` where prefix = tab zone:
| Prefix | Zone | Function | IDs |
|--------|------|----------|-----|
| `ps-` | Tab 1 Mi Identidad | `injectPlayerStats()` | 22 + 3 containers + ~21 DNA + ~23 form/last5 + ~25 zones |
| `hd-` | Header + Score Summary | `injectHeaderStats()` | 12 |
| `ev-` | Tab 2 Evolución | `injectEvolutionStats()` | 24 |
| `cs-` | Tab 3 Campos | `injectCourseStats()` | 17 + 22 narratives + 1 goals container + 3 containers |
| `cl-` | Tab 4 Palos | `injectClubStats()` | 14 + 4 containers |
| `an-` | Tab 5 Análisis | `injectAnalysisStats()` | 4 + 14 metrics |
| `st-` | Tab 6 Estrategia | `injectStrategyStats()` | 9 |

**Dynamic Containers** (JS generates full HTML from JSON):
- `ps-dna-compact-container` → `scoring_profile.dimensions` (4 zone groups)
- `ps-dna-expanded-container` → `scoring_profile.dimensions` (8 dims with rich descriptions)
- `ps-last5-container` → `score_history.rounds` (last 5 rounds)
- `ps-zones-container` → `launch_metrics` + `dispersion_analysis` + `comfort_zones` (4 distance zones)
- `cs-best-rounds-container` → `score_history.rounds` (top 6)
- `cs-quarterly-container` → `quarterly_scoring` (7 quarters)
- `cs-timeline-container` → `milestone_achievements` (9 milestones)
- `cs-goals-container` → `goals_progress` (4 goals with progress bars)
- `cl-carry-long/mid/short` → `launch_metrics.clubs` (carry/roll/total)
- `cl-matrix-body` → `launch_metrics.clubs` (11 rows)

**Backend fields** in `player_stats` (21 total):
`total_rondas`, `mejor_score`, `peor_score`, `promedio_score`, `handicap_actual`, `mejora_handicap`, `primera_ronda`, `ultima_ronda`, `campos_jugados`, `golpes_flightscope`, `player_name`, `best_round_course`, `best_round_date`, `best_round_differential`, `best_hcp`, `best_hcp_date`, `hcp_date`, `player_id`, `location`, `handicap_inicial`, `months_tracked`

## Application Architecture

### Navigation Structure (6 Main Tabs)
1. **📊 Mi Identidad** - Player identity, DNA profile, overview stats
2. **📈 Evolución Temporal** - 18-month historical performance tracking
3. **⛳ Mis Campos** - Performance across 12 golf courses
4. **🏌️ Bolsa de Palos** - Club/equipment performance analysis
5. **🎯 Análisis Profundo** - Deep analysis with SWOT, radar charts
6. **🚀 Estrategia & Acción** - Strategy, ROI analysis, improvement plans

### Chart Types Used
- Line Charts (14) - Temporal trends
- Bar Charts (13) - Category comparisons
- Radar/Spider Charts (10) - Multi-dimensional skills
- Scatter Plots (3) - Dispersion analysis
- Bubble Charts (2) - Multi-variable analysis
- Doughnut Charts (2) - Distribution
- Custom Dispersion Charts (12) - Per-club visualization

### Key JavaScript Functions
| Function | Purpose |
|----------|---------|
| `showTab(tabName)` | Tab navigation, triggers chart resize |
| `handleMenuAction('pdf')` | PDF export of current tab |
| `openYouTubeVideo()` | Opens tutorial videos |
| `scrollToSection(sectionId)` | Smooth scroll with highlight effect |
| `toggleDownloadsMenu()` | Download menu toggle |
| `createDispersionChart()` | Club-specific scatter plot generation |
| `formatPlayerDate(dateStr, style)` | Date formatting (short/month-year/full) |
| `injectPlayerStats()` | Tab 1: 22 values from player_stats |
| `injectHeaderStats()` | Header: 12 values from player_stats + scoring_profile |
| `injectEvolutionStats()` | Tab 2: 24 values from launch_metrics + learning_curve |
| `injectCourseStats()` | Tab 3: 17 values + 3 dynamic containers |
| `injectClubStats()` | Tab 4: 14 values + 4 dynamic containers |
| `injectAnalysisStats()` | Tab 5: 4 values from strokes_gained |
| `injectStrategyStats()` | Tab 6: 9 values from player_stats + launch_metrics |

## Code Conventions

### Naming Standards
- **Functions:** camelCase (`showTab`, `toggleDownloadsMenu`)
- **IDs/Classes:** kebab-case (`tab-content`, `quick-nav-header`)
- **Variables:** camelCase (`chartColors`, `isMobile`, `activeTab`)

### Code Organization (in index.html)
```
Lines 1-38:      DOCTYPE and head meta tags
Lines 39-300:    Header/navigation HTML
Lines 300-1970:  Embedded <style> block
Lines 1971-9070: Main HTML content (6 tabs)
Lines 9071-13242: Embedded <script> block
```

### CSS Patterns
- Mobile-first responsive design
- Glassmorphism effects (backdrop-filter blur)
- Dark theme with color scheme:
  - Primary Blue: `#4A9FD8`
  - Success Green: `#5ABF8F`
  - Gold Accent: `#D4B55A`
  - Alert Red: `#E88B7A`
  - Background: `#0F2027` to `#203A43` gradient
  - Text: `#E8E8E8`

### Responsive Breakpoints
- 1024px - Tablets
- 768px - Small tablets/large phones
- 480px - Small phones
- 375px - Extra small phones
- 360px - iPhone SE level

## Development Guidelines for AI Assistants

### DO
- Preserve the single-file architecture - all code stays in index.html
- Maintain Spanish language for user-facing content
- Follow existing naming conventions (camelCase functions, kebab-case CSS)
- Test changes across all 6 tabs (charts must resize properly)
- Preserve Chart.js and html2pdf.js CDN dependencies
- Maintain mobile responsiveness (test breakpoints)
- Keep accessibility features (ARIA labels, semantic HTML)

### DON'T
- Don't introduce new external dependencies without justification
- Don't break the tab navigation system
- Don't remove the PDF export functionality
- Don't change the color scheme without explicit request
- Don't modify player data (Handicap 23.2, 85 rounds, etc.) without request
- Don't convert to a multi-file structure unless explicitly asked

### When Adding Charts
1. Use existing `chartColors` object for consistency
2. Add canvas element in appropriate tab section
3. Initialize in the script block following existing patterns
4. Ensure responsive sizing (`max-height: 400px`, `300px` mobile)
5. Test tab switching (charts must resize on tab change)

### When Modifying Styles
1. Add styles to the embedded `<style>` block (lines 300-1970)
2. Follow existing media query structure
3. Use CSS custom properties pattern where applicable
4. Test on mobile viewports (360px minimum)

## Key Player Metrics (Reference Data)

| Metric | Value |
|--------|-------|
| Official Handicap | 23.2 (RFEG, September 2025) |
| Improvement | -8.8 points in 18 months |
| Personal Best | 88 (Marina Golf, Nov 16, 2025) |
| Total Rounds | 85 (March 2024 - December 2025) |
| Goal 2026 | Sub-20 handicap |
| Courses Played | 12 different courses |

## Embedded Tutorial Videos

| Tab | YouTube Video ID |
|-----|-----------------|
| Overview | nqKzFGCZ5yI |
| Evolution | oauYCC7BU3U |
| Courses | NdNWLr7tM0I |
| Equipment | PxrzSFNuiT0 |
| Deep Analysis | IPqv5dTiEmk |
| Strategy | PENDIENTE_STRATEGY (pending) |

## Testing Checklist

Before committing changes:
- [ ] All 6 tabs load correctly
- [ ] Charts render and resize on tab switch
- [ ] PDF export works for each tab
- [ ] Mobile view (360px) displays properly
- [ ] Scroll behavior works (sticky header, scroll-to-top)
- [ ] No JavaScript console errors
- [ ] Download menu functions correctly

## Common Tasks

### Adding a New Section to a Tab
1. Find the tab's `<div id="tab-[name]">` container
2. Add HTML structure following existing section patterns
3. Add styles in the `<style>` block if needed
4. Add to quick-nav if applicable

### Adding a New Chart
```javascript
// In the script block, follow this pattern:
new Chart(document.getElementById('newChartId'), {
    type: 'bar', // or 'line', 'radar', etc.
    data: {
        labels: [...],
        datasets: [{
            label: 'Label',
            data: [...],
            backgroundColor: chartColors.primary,
            borderColor: chartColors.primaryBorder,
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
        // ... additional options
    }
});
```

### Updating Player Statistics
Player data is hardcoded throughout the HTML. Search for specific values:
- Handicap: Search for "23.2"
- Rounds: Search for "85"
- Best score: Search for "88"

## Git Workflow

- Main working file: `dashboard_dynamic.html`
- Backend generator: `generate_dashboard_data.py`
- Backup file: `dashboard_FINAL_M3_I2 (3).html` (keep in sync if needed)
- Commit messages should describe what changed and which tab/feature affected

---

## Sprint 13: Production Patterns and Best Practices

### Version 5.0.0 - PRODUCTION READY (2026-02-09)

**Achievement:** 96% chart dynamization with 0 console errors

**Key Stats:**
- 52 backend functions implemented
- 33 frontend integrations completed
- 50+ charts fully dynamic
- 6 critical bugs resolved
- GitHub Pages 100% functional

---

### Safety Pattern for Dynamic Charts

**Problem Solved:** Charts executing before data loaded causing "dashboardData is not defined" errors.

**Solution:** Defensive programming pattern applied to all charts:

```javascript
// Pattern applied to all 33 integrations
if (document.getElementById('chartId')) {
    // Safe data access with optional chaining + fallback
    const data = window.dashboardData?.backend_key?.property || hardcodedFallback;

    // Chart creation
    const ctx = document.getElementById('chartId').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels || ['Default'],
            datasets: [{
                label: 'Dataset',
                data: data.values || [0]
            }]
        }
    });
} // End if chartId
```

**Key Elements:**
1. **IF wrapper:** Prevents execution if canvas doesn't exist
2. **window.dashboardData?. :** Optional chaining prevents undefined errors
3. **|| fallback:** Hardcoded data for offline/error scenarios
4. **Closing comment:** `// End if chartId` for code clarity

---

### Chart Lifecycle Management Pattern

**Problem Solved:** "Canvas is already in use" errors when recreating charts.

**Solution:** Proper chart destruction before recreation:

```javascript
// Initialize global storage
window.chartInstances = window.chartInstances || {};

// Destroy existing chart if present
if (window.chartInstances.chartName) {
    window.chartInstances.chartName.destroy();
}

// Create and store new chart
window.chartInstances.chartName = new Chart(ctx, {...});
```

**Benefits:**
- Prevents memory leaks
- Allows chart updates without page reload
- Enables tab switching without conflicts
- Proper cleanup on re-initialization

---

### Event-Driven Data Loading Pattern

**Problem Solved:** Charts trying to access data before fetch() completes.

**Solution:** Custom event system with dashboardDataReady:

```javascript
// Fetch and dispatch event (lines 71-111)
fetch('dashboard_data.json')
    .catch(() => fetch('output/dashboard_data.json'))  // Fallback
    .then(response => response.json())
    .then(data => {
        window.dashboardData = data;

        // Dispatch custom event
        const event = new Event('dashboardDataReady');
        document.dispatchEvent(event);
    });

// All charts listen for event
document.addEventListener('dashboardDataReady', function() {
    // Initialize all charts here
    initializeHardcodedCharts();
    // ... other initializations
});
```

**Execution Order:**
1. Fetch JSON from server
2. Assign to window.dashboardData
3. Dispatch dashboardDataReady event
4. All listeners execute synchronously
5. Charts render with data available

---

### Fetch Fallback Pattern for Deployment

**Problem Solved:** Different directory structure between localhost and GitHub Pages.

**Solution:** Try root first, then output/ directory:

```javascript
fetch('dashboard_data.json')  // Try root first (GitHub Pages)
    .catch(() => {
        console.warn('⚠️ Intentando cargar desde output/dashboard_data.json');
        return fetch('output/dashboard_data.json');  // Fallback (localhost)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    });
```

**Works on:**
- ✅ GitHub Pages: dashboard_data.json in root
- ✅ Localhost: dashboard_data.json in output/
- ✅ Both environments without code changes

---

### Incremental Integration Methodology

**Problem Solved:** Risk of breaking entire dashboard when integrating many changes.

**Solution:** Lote (batch) approach with testing between phases:

**Sprint 13B Example:**
- **Lote 1:** 3 charts → test → commit
- **Lote 2:** 4 charts → test → commit
- **Lote 3:** 4 charts → test → commit

**Benefits:**
- Isolated failures
- Easier rollback
- Confidence building
- Progressive validation
- Clear commit history

---

### Bug Resolution Patterns

#### Bug #1: dashboardData is not defined
**Symptom:** ReferenceError at multiple lines
**Root Cause:** Missing `window.` prefix on global variable
**Fix:** Change `dashboardData` to `window.dashboardData?.`
**Prevention:** Always use window. prefix for cross-script globals

#### Bug #2: Cannot set properties of undefined
**Symptom:** TypeError when assigning to chartInstances
**Root Cause:** Object not initialized before property access
**Fix:** Add `window.chartInstances = window.chartInstances || {};` at script start
**Prevention:** Initialize global objects before first use

#### Bug #3: Canvas already in use
**Symptom:** Chart.js error preventing chart creation
**Root Cause:** Duplicate chart using same canvas ID
**Fix:** Comment out old chart + add destruction logic
**Prevention:** Search for canvas ID before creating new chart

#### Bug #4: Fetch path 404
**Symptom:** Failed to load dashboard_data.json
**Root Cause:** Wrong directory assumption
**Fix:** Implement fallback fetch pattern
**Prevention:** Test on both localhost and production before commit

#### Bug #5: Charts not waiting for data
**Symptom:** Charts render empty or with errors
**Root Cause:** Execution before async fetch completes
**Fix:** Wrap all initializations in dashboardDataReady listener
**Prevention:** Never initialize charts outside event listener

#### Bug #6: Y-axis inverted
**Symptom:** Chart appears upside down (low values at top)
**Root Cause:** Chart.js default behavior for some chart types
**Fix:** Add `reverse: true` to Y-axis options
**Prevention:** Check axis orientation in Chart.js docs

---

### Code Organization Best Practices

#### Global Initialization (lines 60-68)
```javascript
// Error handler
window.addEventListener('error', function(e) {
    console.error('Error capturado:', e.message, e.filename, e.lineno);
    return false;
});

// Initialize global objects
window.chartInstances = window.chartInstances || {};
```

#### Fetch + Event Dispatch (lines 71-111)
- Fetch JSON with fallback
- Assign to window.dashboardData
- Dispatch dashboardDataReady event
- Log success/failure

#### Chart Initialization (inside event listener)
- Check element exists (IF wrapper)
- Destroy old chart if exists
- Access data with optional chaining
- Create chart with fallback data
- Store chart instance

#### Hardcoded Charts (fallback mode)
- Keep original hardcoded data as fallback
- Wrap in same IF pattern
- Load from JSON when available
- Degrade gracefully if JSON unavailable

---

### Testing Checklist for New Charts

Before committing new chart integration:

- [ ] Chart wrapped in `if (document.getElementById(...)) { }`
- [ ] Data accessed with `window.dashboardData?.`
- [ ] Fallback data provided with `|| [...]`
- [ ] Chart destruction implemented if applicable
- [ ] Chart instance stored in window.chartInstances
- [ ] Closing comment added `// End if chartId`
- [ ] Tested on localhost:8001
- [ ] Tested on GitHub Pages
- [ ] Console shows 0 errors (F12 → Console)
- [ ] Chart renders correctly in target tab
- [ ] Tab switching doesn't break chart
- [ ] Browser refresh works without errors

---

### Performance Optimizations

**JSON Size Management:**
- Current: 194 KB (97% of 200 KB limit)
- Technique: Minimize unnecessary data
- Strategy: Only include data actually used by charts
- Monitoring: Check file size after each function addition

**Execution Time:**
- Backend: 3.1 seconds (generate_dashboard_data.py)
- Frontend: <500ms (chart rendering)
- Total: ~3.6 seconds from generation to visualization

**Memory Management:**
- Proper chart destruction prevents memory leaks
- Global chartInstances object maintains references
- Event listeners properly scoped
- No memory accumulation on page refresh

---

## Future Maintenance Guidelines

### Adding New Backend Function

1. Implement in `generate_dashboard_data.py`
2. Add to orchestrator in `generate_dashboard_data()`
3. Add to `dashboard_data` dict with clear key name
4. Update metadata version and changelog
5. Regenerate JSON: `python generate_dashboard_data.py`
6. Verify JSON contains new key

### Integrating New Frontend Chart

1. Locate canvas element in HTML or add new one
2. Wrap initialization in `if (document.getElementById(...)) {}`
3. Access data: `window.dashboardData?.new_key?.property || fallback`
4. Add chart destruction if updating existing
5. Store instance: `window.chartInstances.chartName = new Chart(...)`
6. Add closing comment: `// End if chartId`
7. Place inside dashboardDataReady event listener
8. Test on localhost first
9. Commit and push to GitHub
10. Verify on GitHub Pages

### Debugging Chart Issues

1. Open browser console (F12 → Console)
2. Look for errors (red text)
3. Check if dashboardDataReady event fired
4. Verify JSON loaded: `console.log(window.dashboardData)`
5. Check canvas exists: `document.getElementById('chartId')`
6. Verify data structure matches expected format
7. Test with hardcoded data to isolate issue
8. Check Chart.js documentation for specific error

---

## Git Workflow (Updated)

### Commit Message Patterns
```
feat(v3.0): complete UXWriter dashboard integration
feat(sprint13): integrate smash_factor_evolution chart
fix(sprint13): resolve dashboardData undefined errors
refactor(charts): apply safety pattern to all 14 Sprint 13A charts
docs(readme): update with Sprint 13 completion status
```

### Branch Strategy
- Main branch: `main`
- All development on `main` (single developer project)
- Tags for major versions: `v5.0.0`, `v3.0`

### Pre-Commit Checklist
- [ ] All console errors resolved
- [ ] Tested on localhost
- [ ] dashboard_data.json in root for GitHub Pages
- [ ] No hardcoded paths to local directories
- [ ] All changes functional on both environments
- [ ] Backend server starts without errors (`python -m app.main`)
- [ ] /generate-content endpoint responds correctly
- [ ] AI content integration tested in dashboard

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| v3.0.6 | 2026-03-01 | Template vs Data Phase 2 — ~216 IDs dinámicos + 12 containers + 3 backend functions (form_summary, scoring_streaks, goals_progress) + DOMContentLoaded fix |
| v3.0.5+ | 2026-02-28 | Template vs Data Phase 1 — 106 IDs dinámicos + 7 funciones inyección + 7 containers (dashboard reutilizable) |
| v3.0.5 | 2026-02-25 | Identity Timeline — evolución temporal del arquetipo (11 períodos, ventana 90d/60d, colores por zona) |
| v3.0.4 | 2026-02-24 | Orchestrator v4.1 asyncio.to_thread() (-33% tiempo) + arquitectura estática completa (cero live calls) |
| v3.0.3 | 2026-02-22 | Static ai_content.json cache + UXWriter 6-section fix + Windows encoding fix |
| v3.0.2 | 2026-02-21 | Prompt caching (cache_control) + model update to claude-sonnet-4-6 |
| v3.0.1 | 2026-02-17 | UXWriter dashboard integration + documentation consolidation |
| v3.0.0 | 2026-02-16 | Multi-Agent System complete (5 agents, architecture optimization) |
| v5.1.1 | 2026-02-13 | Heatmap + Mobile optimization |
| v5.1.0 | 2026-02-12 | 10D radar + data corrections |
| v5.0.0 | 2026-02-09 | 36 charts dynamized (100% completion) |
| TIER 1 | 2026-02-15 | Agentic analytics engine (FastAPI + RAG + Agent) |
