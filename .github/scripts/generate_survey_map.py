#!/usr/bin/env python3
"""
Generate an interactive map visualization of runway survey data from PR files.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

def find_survey_files(base_path: str = ".") -> List[Path]:
    """Find all survey JSON files in the PR."""
    survey_files = []
    for json_file in Path(base_path).rglob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                # Check if it looks like survey data (has runway info)
                if 'runways' in data or 'runway' in data or 'corners' in data:
                    survey_files.append(json_file)
        except (json.JSONDecodeError, KeyError):
            continue
    return survey_files

def parse_survey_data(file_path: Path) -> Optional[Dict[str, Any]]:
    """Parse survey data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Extract runway survey data (adapt to your JSON structure)
        survey_info = {
            'file': str(file_path),
            'airport_icao': data.get('icao', data.get('airport_icao', 'UNKNOWN')),
            'airport_name': data.get('name', data.get('airport_name', '')),
            'runways': []
        }

        # Handle different JSON structures
        runways = data.get('runways', [data]) if 'runways' in data else [data]

        for runway in runways:
            runway_info = {
                'designator': runway.get('runwayNumber', runway.get('designator', 'N/A')),
                'heading': runway.get('trueHeading', runway.get('heading', 0)),
                'length': runway.get('length', 0),
                'width': runway.get('width', 0),
                'threshold1': {
                    'lat': runway.get('threshold1Latitude', 0),
                    'lon': runway.get('threshold1Longitude', 0),
                },
                'threshold2': {
                    'lat': runway.get('threshold2Latitude', 0),
                    'lon': runway.get('threshold2Longitude', 0),
                },
                'touchdown1': {
                    'lat': runway.get('touchdown1Latitude', 0),
                    'lon': runway.get('touchdown1Longitude', 0),
                },
                'touchdown2': {
                    'lat': runway.get('touchdown2Latitude', 0),
                    'lon': runway.get('touchdown2Longitude', 0),
                }
            }

            # Extract corner points if available
            corners = runway.get('corners', [])
            if corners and len(corners) >= 4:
                runway_info['corners'] = [
                    {'lat': c.get('latitude', 0), 'lon': c.get('longitude', 0)}
                    for c in corners[:4]
                ]
            else:
                # Calculate corners from threshold and width if not provided
                runway_info['corners'] = calculate_corners(runway_info)

            survey_info['runways'].append(runway_info)

        return survey_info
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return None

def calculate_corners(runway: Dict[str, Any]) -> List[Dict[str, float]]:
    """Calculate runway corners from thresholds and width (simplified)."""
    # This is a simplified version - just returns thresholds for now
    # In production, you'd calculate perpendicular offsets
    import math

    lat1 = runway['threshold1']['lat']
    lon1 = runway['threshold1']['lon']
    lat2 = runway['threshold2']['lat']
    lon2 = runway['threshold2']['lon']
    width_ft = runway.get('width', 100)

    # Calculate perpendicular bearing
    heading_rad = math.radians(runway.get('heading', 0))
    perp_bearing = heading_rad + math.pi / 2

    # Offset distance in degrees (approximate for small distances)
    width_deg = (width_ft / 2) / 364000  # rough conversion feet to degrees

    lat_offset = width_deg * math.cos(perp_bearing)
    lon_offset = width_deg * math.sin(perp_bearing)

    return [
        {'lat': lat1 - lat_offset, 'lon': lon1 - lon_offset},  # C1: threshold1 left
        {'lat': lat1 + lat_offset, 'lon': lon1 + lon_offset},  # C2: threshold1 right
        {'lat': lat2 + lat_offset, 'lon': lon2 + lon_offset},  # C3: threshold2 right
        {'lat': lat2 - lat_offset, 'lon': lon2 - lon_offset},  # C4: threshold2 left
    ]

def generate_html_map(surveys: List[Dict[str, Any]]) -> str:
    """Generate interactive HTML map with Leaflet and satellite imagery."""

    # Calculate center point from all runways
    all_lats = []
    all_lons = []
    for survey in surveys:
        for runway in survey['runways']:
            all_lats.extend([runway['threshold1']['lat'], runway['threshold2']['lat']])
            all_lons.extend([runway['threshold1']['lon'], runway['threshold2']['lon']])

    center_lat = sum(all_lats) / len(all_lats) if all_lats else 0
    center_lon = sum(all_lons) / len(all_lons) if all_lons else 0

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map {{ height: 600px; width: 100%; border: 2px solid #333; border-radius: 8px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Initialize map centered on survey data
        var map = L.map('map').setView([{center_lat}, {center_lon}], 15);

        // Add satellite imagery layer (Esri World Imagery)
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 19
        }}).addTo(map);

        // Add labels overlay (optional, for better context)
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_only_labels/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            pane: 'shadowPane',
            maxZoom: 19
        }}).addTo(map);

"""

    # Add each runway to the map
    for survey in surveys:
        icao = survey['airport_icao']
        name = survey['airport_name']

        for runway in survey['runways']:
            designator = runway['designator']
            heading = runway['heading']
            length_ft = runway['length']
            width_ft = runway['width']

            # Add corner markers
            corners = runway.get('corners', [])
            for i, corner in enumerate(corners, 1):
                html += f"""
        L.circleMarker([{corner['lat']}, {corner['lon']}], {{
            radius: 6,
            fillColor: '#ff0000',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }}).addTo(map)
        .bindPopup('<b>Corner {i}</b><br>Lat: {corner['lat']:.8f}<br>Lon: {corner['lon']:.8f}');
"""

            # Add runway centerline
            thr1 = runway['threshold1']
            thr2 = runway['threshold2']
            html += f"""
        L.polyline([
            [{thr1['lat']}, {thr1['lon']}],
            [{thr2['lat']}, {thr2['lon']}]
        ], {{
            color: '#00ff00',
            weight: 3,
            opacity: 0.8
        }}).addTo(map)
        .bindPopup('<b>{icao} Runway {designator}</b><br>Heading: {heading:.1f}°<br>Length: {length_ft:.0f} ft<br>Width: {width_ft:.0f} ft');
"""

            # Add threshold markers
            html += f"""
        L.circleMarker([{thr1['lat']}, {thr1['lon']}], {{
            radius: 8,
            fillColor: '#0066ff',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        }}).addTo(map)
        .bindPopup('<b>Threshold 1</b><br>RWY {designator}');

        L.circleMarker([{thr2['lat']}, {thr2['lon']}], {{
            radius: 8,
            fillColor: '#0066ff',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        }}).addTo(map)
        .bindPopup('<b>Threshold 2</b><br>RWY {designator}');
"""

            # Add touchdown point markers
            td1 = runway['touchdown1']
            td2 = runway['touchdown2']
            if td1['lat'] != 0 and td1['lon'] != 0:
                html += f"""
        L.circleMarker([{td1['lat']}, {td1['lon']}], {{
            radius: 6,
            fillColor: '#ffcc00',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }}).addTo(map)
        .bindPopup('<b>Touchdown 1</b><br>RWY {designator}');
"""

            if td2['lat'] != 0 and td2['lon'] != 0:
                html += f"""
        L.circleMarker([{td2['lat']}, {td2['lon']}], {{
            radius: 6,
            fillColor: '#ffcc00',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }}).addTo(map)
        .bindPopup('<b>Touchdown 2</b><br>RWY {designator}');
"""

    html += """
        // Fit map to show all markers
        var bounds = L.latLngBounds([]);
"""

    # Add all points to bounds
    for survey in surveys:
        for runway in survey['runways']:
            for corner in runway.get('corners', []):
                html += f"        bounds.extend([{corner['lat']}, {corner['lon']}]);\n"

    html += """
        if (bounds.isValid()) {
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    </script>
</body>
</html>
"""

    return html

def main():
    parser = argparse.ArgumentParser(description='Generate survey map visualization')
    parser.add_argument('--pr-number', type=int, help='Pull request number')
    parser.add_argument('--repo', type=str, help='Repository name')
    args = parser.parse_args()

    print(f"Searching for survey files in PR #{args.pr_number}...")

    # Find all survey files
    survey_files = find_survey_files()

    if not survey_files:
        print("No survey files found in this PR.")
        # Create empty map file to avoid errors
        with open('survey_map.html', 'w') as f:
            f.write("<p><em>No survey data found in this PR.</em></p>")
        sys.exit(0)

    print(f"Found {len(survey_files)} survey file(s): {[str(f) for f in survey_files]}")

    # Parse survey data
    surveys = []
    for file_path in survey_files:
        survey = parse_survey_data(file_path)
        if survey:
            surveys.append(survey)

    if not surveys:
        print("No valid survey data could be parsed.")
        with open('survey_map.html', 'w') as f:
            f.write("<p><em>Survey files found but could not be parsed.</em></p>")
        sys.exit(0)

    print(f"Parsed {len(surveys)} survey(s) successfully.")

    # Generate HTML map
    html_map = generate_html_map(surveys)

    # Write to file
    with open('survey_map.html', 'w') as f:
        f.write(html_map)

    print("✅ Map generated successfully: survey_map.html")

if __name__ == '__main__':
    main()
