# Contributing to PPA Airports

Thank you for contributing high-precision airport data! This guide will help you submit your runway surveys.

## Prerequisites

- PPA app with survey feature
- RTK or PPP-capable GPS receiver (or high-quality GPS with <2m accuracy)
- Access to the runway you want to survey
- GitHub account

## Surveying an Airport

### Equipment Requirements

**Minimum Requirements:**
- GPS accuracy: <2 meters
- Survey method: 4-corner runway survey

**Recommended Equipment:**
- RTK GPS (accuracy: 1-5 cm)
- PPP GPS with corrections (accuracy: 5-20 cm)
- NTRIP connection for real-time corrections

### Survey Procedure

1. **Safety First**
   - Never survey an active runway without permission
   - Contact airport management before surveying
   - Ensure proper authorization and safety protocols

2. **Using the PPA App**
   - Open PPA app and navigate to Survey Mode
   - Select or create the airport
   - Wait for GPS accuracy <2m (preferably <0.5m)
   - Walk to each corner of the runway in clockwise order
   - Capture each corner point when GPS accuracy is optimal
   - Finalize the survey

3. **Quality Checks**
   - All 4 corners captured with good accuracy
   - Opposite sides of runway are within 25% length match
   - Runway designator matches published information
   - Survey completed on same day (avoid GPS drift)

## Exporting Survey Data

### From PPA App

1. Open Survey Mode
2. Find your surveyed runway in "SAVED RUNWAYS"
3. Tap "Export" button
4. Choose "Export as JSON"
5. Save file to accessible location

### File Naming Convention

Name your file using the ICAO code:
```
CDS2.json      # ICAO code
CYQV.json      # Canadian airports
KORD.json      # US airports
```

For airports without ICAO codes, use FAA LID or local code:
```
3W5.json       # FAA LID
```

## Submitting Your Survey

### Step 1: Fork the Repository

1. Go to https://github.com/perryc/ppa_airports
2. Click "Fork" button (top right)
3. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/ppa_airports.git
cd ppa_airports
```

### Step 2: Add Your Airport File

1. Determine the country folder:
   - `CA/` for Canada
   - `US/` for United States
   - Create new folder if needed

2. Copy your exported JSON file:
```bash
cp ~/Downloads/CDS2.json airports/CA/CDS2.json
```

3. Validate the JSON (optional but recommended):
```bash
python scripts/validate.py airports/CA/CDS2.json
```

### Step 3: Commit and Push

```bash
git add airports/CA/CDS2.json
git commit -m "Add CDS2 (Disley Airport) survey

- Survey date: 2025-10-03
- GPS accuracy: 0.02m (RTK)
- Runway 17/35: 2250ft x 65ft
- Method: 4-corner survey with RTK GPS"

git push origin main
```

### Step 4: Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request" button
3. Fill in the details:
   - **Title**: "Add [ICAO] - [Airport Name]"
   - **Description**: Include survey details (date, accuracy, equipment)
4. Submit the pull request

## Pull Request Review

Your submission will be reviewed for:

### Automated Checks
- JSON schema validation
- Coordinate precision (8 decimal places)
- Required fields present
- Accuracy thresholds met

### Manual Review
- Runway geometry makes sense
- Coordinates are in correct location (rough check)
- Survey date is recent
- No duplicate/conflicting data

### Approval Process
- ✅ Automated checks pass
- ✅ Manual review complete
- ✅ Any feedback addressed
- 🎉 Merged into main branch
- 📡 Available to all users on next app update

## Data Format Requirements

### Coordinate Precision
- Use 8 decimal places for lat/lon (~1mm precision)
- Example: `52.12345678` not `52.123`

### Elevation
- Feet MSL
- 1 decimal place: `1850.2`

### Dates
- ISO 8601 format: `2025-10-03T12:00:00Z`
- Use UTC timezone

### Headings
- Magnetic heading: rounded to nearest degree
- True heading: calculated from geometry
- Magnetic variation: from WMM model

## Updating Existing Surveys

If you have a more accurate survey of an existing airport:

1. Include comparison in PR description
2. Explain why your survey is better (equipment, accuracy, date)
3. Old data will be archived, not deleted

## Code of Conduct

- Be respectful and professional
- Accurate data only - no guessing coordinates
- Credit original surveyor if improving their work
- Report any issues or concerns

## Questions?

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: (to be added)

## Recognition

Contributors will be:
- Listed in airport metadata
- Credited in CONTRIBUTORS.md
- Recognized in app "About" section

Thank you for helping build the world's most precise airport database! ✈️
