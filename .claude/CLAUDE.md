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

- Main working file: `index.html`
- Backup file: `dashboard_FINAL_M3_I2 (3).html` (keep in sync if needed)
- Commit messages should describe what changed and which tab/feature affected
