# EXCEL SPREADSHEET DATA GUIDE
## How to Track Your Golf Metrics

---

## 📊 SPREADSHEET STRUCTURE

Your golf tracking spreadsheet should have these columns:

### COLUMN HEADERS (Add these to Row 1)

| Col | Header | Format | Description |
|-----|--------|--------|-------------|
| A | **Date** | MM/DD/YYYY | When you played |
| B | **Club** | Text | Driver, 3W, 4W, Hyb, 5i, 6i, 7i, 8i, 9i, PW, SW52, SW58 |
| C | **Carry** | Meters | Ball in air distance |
| D | **Total** | Meters | Total distance (carry + roll) |
| E | **Ball Speed** | km/h | Speed off clubface |
| F | **Height** | Meters | Ball flight height |
| G | **Launch Angle** | Degrees | Angle of launch |
| H | **Direction** | Degrees | Left (-) / Center (0) / Right (+) |
| I | **Lateral** | Meters | Left/right deviation |
| J | **Spin Rate** | RPM | Revolutions per minute |
| K | **Roll** | Meters | Distance after landing |
| L | **Consistency** | StdDev | Standard deviation (calculate) |
| M | **Notes** | Text | Any observations |

---

## 📈 KEY METRICS TO TRACK

### DISTANCE METRICS (by Club)
- **Average:** Mean of all shots with that club
- **Maximum:** Best distance achieved
- **Minimum:** Shortest distance (exclude mishits)
- **Consistency:** Standard deviation (lower is better)

### ACCURACY METRICS
- **Direction:** Target is 0° (straight)
  - Negative = LEFT (your current issue with Driver)
  - Positive = RIGHT
  - Acceptable range: ±6°
  
- **Lateral Deviation:** How many meters left/right
  - Target: <3 meters
  
### PERFORMANCE METRICS
- **Ball Speed:** Energy transfer (higher = more power)
- **Launch Angle:** Too high or too low affects distance
  - Driver: 10-15° ideal
  - Irons: 15-25° ideal
  - Wedges: 25-40° ideal

- **Spin Rate:** Backspin on ball
  - Driver: 2000-2500 RPM ideal
  - Irons: 4000-6000 RPM ideal
  - Wedges: 7000-10000 RPM ideal

---

## 📋 SAMPLE DATA (Copy this format)

### Driver Tracking Example

| Date | Club | Carry | Total | Ball Speed | Height | Launch | Direction | Notes |
|------|------|-------|-------|------------|--------|--------|-----------|-------|
| 1/4/26 | Dr | 232 | 255 | 254 | 27 | 11.8 | -10.7° | Slice present |
| 1/4/26 | Dr | 223 | 251 | 249 | 19 | 8.3 | -9.3° | Better |
| 1/4/26 | Dr | 236 | 255 | 256 | 27 | 9.1 | -12.1° | Back to slice |
| **AVG** | **Dr** | **230** | **253** | **253** | **24** | **9.7** | **-10.7°** | |
| **StdDev** | **Dr** | **6.5** | **2.3** | **3.5** | **4.2** | **1.4** | **1.4°** | |

---

## 🧮 EXCEL FORMULAS

### AVERAGE DISTANCE (for Driver)
```
=AVERAGEIF(B:B,"Dr",D:D)
```
Finds all rows where Club = "Dr" and averages Total distance

### STANDARD DEVIATION (Consistency)
```
=STDEV(D2:D50)
```
Calculates spread of distances (lower = more consistent)

### MAXIMUM DISTANCE
```
=MAXIFS(D:D,B:B,"Dr")
```
Finds longest distance with Driver

### MINIMUM DISTANCE
```
=MINIFS(D:D,B:B,"Dr")
```
Finds shortest distance with Driver (exclude mishits)

### COUNT SHOTS
```
=COUNTIF(B:B,"Dr")
```
Counts total Driver shots

### AVERAGE DIRECTION
```
=AVERAGEIF(B:B,"Dr",H:H)
```
Calculates average direction (target: 0°)

---

## 📱 WHAT TO TRACK WHEN

### AT THE RANGE (with FlightScope)
- ✅ Distance (carry + total)
- ✅ Direction
- ✅ Ball speed
- ✅ Launch angle
- ✅ Spin rate
- ✅ Height
- ✅ Lateral deviation

### ON THE COURSE
- ✅ Clubs used
- ✅ Distances hit (estimate or GPS)
- ✅ Fairways (Y/N)
- ✅ Direction (left/center/right)
- ✅ Score for hole
- ✅ Confidence (1-10)
- ✅ Notes (feel, mechanics observations)

---

## 📊 DASHBOARD SETUP (Advanced)

### Create Summary Dashboard (Tab 2)

**This summarizes all your data:**

```
CLUB          | AVG DIST | MAX | MIN | CONSISTENCY | AVG DIR | STATUS
─────────────────────────────────────────────────────────────────────
Driver        | 231.6m   | 262 | 178 | 10.3m      | -12.2°  | 🔴 FIX
3W            | 225.7m   | 256 | 210 | 15.2m      | -10.8°  | 🟠 WORK
4W            | 195m     | — | — | TBD        | TBD    | ⭐ NEW
Hybrid        | 179.4m   | 196 | 146 | 12.1m      | -6.1°   | ✅ SOLID
5i            | 150.4m   | 173 | 136 | 3.1m       | -1.8°   | ⭐ TOUR
6i            | 140.2m   | 154 | 126 | 8.9m       | -2.1°   | ✅ EXCEL
7i            | 143.1m   | 153 | 113 | 7.4m       | -1.2°   | ✅ EXCEL
8i            | 123.4m   | 139 | 106 | 6.8m       | -0.8°   | ⭐ TOUR
9i            | 119.3m   | 127 | 98  | 6.5m       | -0.5°   | ⭐ TOUR
PW            | 113.2m   | 159 | 78  | 13.2m      | -1.4°   | ⚠️ WORK
SW52          | 93.1m    | 106 | 75  | 8.9m       | -2.3°   | ✅ GOOD
SW58          | 96.4m    | 129 | 80  | 11.2m      | -3.8°   | ✅ GOOD
```

### Create Progress Tracker (Tab 3)

```
WEEK  | DATE  | DR SLICE | DR CONSISTENCY | 4W DIST | PW VAR | SCORE | GIR | FAI
─────────────────────────────────────────────────────────────────────────────
0     | 1/1   | -12.2°   | 10.3m         | N/A     | 13.2m  | 80    | 13  | 8
1     | 1/8   | -11.0°   | 10.5m         | N/A     | 12.8m  | 79    | 13  | 9
2     | 1/15  | -8.5°    | 9.8m          | 195m    | 11.2m  | 78    | 14  | 10
3     | 1/22  | -7.0°    | 9.2m          | 195m    | 10.5m  | 78    | 14  | 10
4     | 1/29  | -6.5°    | 8.9m          | 196m    | 9.8m   | 77    | 15  | 11
```

---

## 📥 DATA DOWNLOAD GUIDE

### From FlightScope (if you have access)
1. **Login** to FlightScope app/system
2. **Select Date Range** (your practice sessions)
3. **Download CSV** option
4. **Open in Excel**
5. **Paste into your tracking sheet**
6. **Format and clean data**

### Manual Entry (from range cards)
1. **Create column** for each data point
2. **Enter data** after each session
3. **Calculate averages** weekly
4. **Update dashboard** automatically via formulas

### From Golf GPS App (on course)
1. **Record distances** with GPS app (18birdies, Golfshot, etc.)
2. **Note direction** (left/center/right)
3. **Export data** weekly
4. **Compile into master sheet**

---

## 🎯 WEEKLY REVIEW CHECKLIST

**Every Sunday, update your spreadsheet:**

- [ ] Enter all range session data for the week
- [ ] Calculate averages for each club
- [ ] Check consistency (StdDev) trends
- [ ] Update progress dashboard
- [ ] Compare to previous week
- [ ] Identify improvements or regressions
- [ ] Note any mechanical changes or observations
- [ ] Print cheat sheet with updated numbers

---

## 💾 FILE MANAGEMENT

**Recommended Structure:**

```
Golf Analysis/
├── FlightScope_Master.xlsx (main data)
├── 2026_Dashboard.xlsx (summaries & charts)
├── Progress_Tracker.xlsx (week-by-week)
├── Course_Scorecard.xlsx (18-hole tracks)
└── Backups/
    ├── Backup_2026_Jan.xlsx
    ├── Backup_2026_Feb.xlsx
    └── ...
```

**Backup:** Save copies to cloud (Google Drive, OneDrive, Dropbox)

---

## 📊 CHARTS TO CREATE (Advanced)

### Chart 1: Distance Progression by Club
Shows average distance for each club (visual comparison)

### Chart 2: Direction Accuracy by Club
Shows deviation from target (0°) for each club

### Chart 3: Consistency Trend (over time)
Shows StdDev decreasing (improving consistency) over weeks

### Chart 4: Score Improvement Trend
Shows your score improving from 80 → 79 → 78 → 77

### Chart 5: GIR Improvement Trend
Shows more greens in regulation (goal: 15+ per round)

---

## 🎓 INTERPRETATION GUIDE

### What These Numbers Mean

**Average Distance:**
- Shows typical performance with each club
- Used for course management (distance selection)
- Target: Within 2-3m of your average

**Consistency (StdDev):**
- Lower = More consistent (better!)
- Tour-level: <5m StdDev
- Your best: 5i at 3.1m (excellent!)
- Your worst: 3W at 15.2m (needs work!)

**Direction:**
- 0° = Perfect straight
- Negative = Left (your slice issue)
- Positive = Right
- Target: Within ±6°

**Ball Speed:**
- Higher = More energy/power
- Varies by club
- Driver: 240-260 km/h typical
- Wedges: 120-160 km/h typical

**Launch Angle:**
- Too high = More backspin, less distance
- Too low = Less height, loss of distance
- Sweet spot varies by club
- Driver: 10-15° ideal

---

## ✅ NEXT STEPS

1. **Download your FlightScope data** (if available)
2. **Create Excel spreadsheet** with columns above
3. **Populate with your 284 shots** (from attached Excel)
4. **Create dashboard** with formulas
5. **Set up auto-update** for new range sessions
6. **Review weekly** every Sunday
7. **Track 4-week progress** toward 8.3/10

**This spreadsheet becomes your golf performance engine.**

---

*Use this data to make smarter decisions, track progress, and identify exactly what's improving and what needs work.*