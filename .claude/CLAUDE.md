# CLAUDE.md - AlvGolf Human Identity Engine

## Project Overview

**AlvGolf Human Identity Engine** is a comprehensive golf performance analytics dashboard (IA Golf Performance Dashboard 360°) built for Alvaro Peralta. It provides multi-dimensional analysis of golf performance across 85 rounds spanning 18 months, featuring 47+ data visualizations, 12 golf courses, and complete equipment analytics.

**Primary Language:** Spanish (es)
**Type:** Single-file static HTML application
**Deployment:** Ready to deploy as-is (no build process required)

## Repository Structure

```
AlvGolf-Human-Identity-Engine/
├── index.html                              # Main dashboard application (843 KB, ~13,000 lines)
├── dashboard_FINAL_M3_I2 (3).html          # Backup/duplicate copy
├── AIvGolf_Identity_Performance_Enginev2.png  # Branding image
├── Augusta_National.png                    # Course background image
└── CLAUDE.md                               # This file
```

## Technology Stack

### Frontend
- **HTML5** - Semantic markup with accessibility support
- **CSS3** - Embedded styles with 11 media queries for responsive design
- **Vanilla JavaScript (ES6+)** - No frameworks, pure JS implementation

### External Dependencies (CDN)
- **Chart.js** - `https://cdn.jsdelivr.net/npm/chart.js` - Data visualization (47+ charts)
- **html2pdf.js** - `https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js` - PDF export

### No Build Tools
- No webpack, transpiler, or bundler
- No package.json or node_modules
- Single HTML file contains all styles and scripts

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
feat(sprint13): integrate smash_factor_evolution chart
fix(sprint13): resolve dashboardData undefined errors
refactor(charts): apply safety pattern to all 14 Sprint 13A charts
docs(readme): update with Sprint 13 completion status
```

### Branch Strategy
- Main branch: `main`
- All development on `main` (single developer project)
- Tags for major versions: `v5.0.0`

### Pre-Commit Checklist
- [ ] All console errors resolved
- [ ] Tested on localhost
- [ ] dashboard_data.json in root for GitHub Pages
- [ ] No hardcoded paths to local directories
- [ ] All changes functional on both environments
