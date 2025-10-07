# Pretty Precise Approach Runway Database

High-precision GPS runway data, crowdsourced from RTK/PPP GPS surveys.

## Why This Repository?

Testing a "Pretty Precise Approach" app for DIY decimiter class GPS approach/landing guidance and that will only work if there is precise survey data for the airstrip.

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

The PPA (Pretty Precise Approach) app automatically downloads and updates this database. You can also access the data directly:

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

### Quality Standards

- GPS accuracy must be <30 cm or better
- All 4 runway corners must be surveyed
- Coordinates must have 8 decimal places precision

## Data License

This data is provided under the **Open Database License (ODbL)**. You are free to:
- Use the data for any purpose
- Modify and build upon the data
- Share and distribute the data


## Support

- Issues: https://github.com/perryc/ppa_airports/issues
- Discussions: https://github.com/perryc/ppa_airports/discussions
- Pretty Precise Approach App: https://github.com/perryc/ppa

## Statistics

- **Airports**: 1
- **Runways Surveyed**: 2
- **Countries**: 1
- **Last Update**: Never

---

**Note**: This repository is in initial setup. First surveys coming soon!
