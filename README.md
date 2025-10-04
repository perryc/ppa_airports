# PPA Airports - Community Precision Airport Database

High-precision airport and runway data for precision approach applications, crowdsourced from RTK/PPP GPS surveys.

## Why This Repository?

Traditional airport databases (like OurAirports) provide location data with ~1-10 meter precision, which is insufficient for precision approach guidance. This repository contains community-contributed airport surveys with centimeter-level accuracy from RTK/PPP GPS receivers.

## Data Quality

- **Precision**: Sub-meter accuracy (typically <20cm with RTK/PPP GPS)
- **Coverage**: 4-corner runway surveys with calculated thresholds and touchdown points
- **Validation**: Community-reviewed for accuracy and completeness
- **Updates**: Continuous improvement as better surveys become available

## Repository Structure

```
ppa_airports/
├── airports/
│   ├── CA/              # Canada
│   │   ├── CDS2.json   # Disley Airport, SK
│   │   └── ...
│   ├── US/              # United States
│   └── ...
├── schema.json          # JSON schema for validation
├── CONTRIBUTING.md      # Contribution guidelines
└── README.md           # This file
```

## Using This Data

### Download the Database

The PPA (Precision Pilot Assistant) app automatically downloads and updates this database. You can also access the data directly:

```bash
git clone https://github.com/perryc/ppa_airports.git
```

### Data Format

Each airport is stored as a JSON file with the following structure:

```json
{
  "icao": "CDS2",
  "name": "Disley Airport",
  "location": {
    "latitude": 52.00000000,
    "longitude": -106.00000000,
    "elevation_ft": 1850.5
  },
  "runways": [
    {
      "designator": "17/35",
      "surveyed": true,
      "survey_date": "2025-10-03",
      "survey_accuracy_m": 0.02,
      "survey_method": "RTK_GPS",
      "surveyor": "username",
      "length_ft": 2250,
      "width_ft": 65,
      "surface": "grass",
      "threshold_17": {
        "latitude": 52.00000000,
        "longitude": -106.00000000,
        "elevation_ft": 1850.2,
        "heading_mag": 170.0,
        "heading_true": 182.0,
        "magnetic_variation": 12.0
      },
      "threshold_35": {
        "latitude": 52.00000000,
        "longitude": -106.00000000,
        "elevation_ft": 1850.0,
        "heading_mag": 350.0,
        "heading_true": 002.0,
        "magnetic_variation": 12.0
      },
      "touchdown_17": {
        "latitude": 52.00000000,
        "longitude": -106.00000000,
        "elevation_ft": 1850.1
      },
      "touchdown_35": {
        "latitude": 52.00000000,
        "longitude": -106.00000000,
        "elevation_ft": 1849.9
      },
      "corners": [
        {
          "id": "corner_1",
          "latitude": 52.00000000,
          "longitude": -106.00000000,
          "elevation_ft": 1850.0
        }
      ]
    }
  ],
  "metadata": {
    "last_updated": "2025-10-03T12:00:00Z",
    "contributors": ["username"],
    "data_source": "ppa_mobile_survey"
  }
}
```

## Contributing

We welcome high-precision airport surveys! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start

1. Survey a runway using the PPA app with RTK/PPP GPS
2. Export the survey data (JSON format)
3. Fork this repository
4. Add your airport file to the appropriate country folder
5. Submit a pull request

### Quality Standards

- GPS accuracy must be <2 meters (preferably <0.5m)
- All 4 runway corners must be surveyed
- Survey date must be within last 5 years
- Coordinates must have 8 decimal places precision

## Data License

This data is provided under the **Open Database License (ODbL)**. You are free to:
- Use the data for any purpose
- Modify and build upon the data
- Share and distribute the data

**Attribution Required**: Please credit "PPA Airports Community Database"

## Support

- Issues: https://github.com/perryc/ppa_airports/issues
- Discussions: https://github.com/perryc/ppa_airports/discussions
- App: https://github.com/perryc/ppa

## Statistics

- **Airports**: 0
- **Runways Surveyed**: 0
- **Countries**: 0
- **Last Update**: Never

---

**Note**: This repository is in initial setup. First surveys coming soon!
