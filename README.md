# flight-tracker-local

A lightweight Python-based flight tracking app for visualizing live aircraft within a 1,000 km radius using real-time data from the OpenSky Network API.

## Features
- Tracks real-time flights within a defined bounding box (default: 1,000 km around Frankfurt)
- Displays aircraft positions on an interactive map (Folium + Leaflet.js)
- Optionally serves the map via Flask for web viewing
- Easy to extend: Add weather overlays, airport info, flight detail pages, and more

## Codebase Overview

This repository currently exposes a small Flask application for tracking aircraft near a fixed point.

```
flight_data/
├── README.md
└── tracking_app/
    ├── flight_map.py
    └── templates/
        └── map.html
```

### General structure and flow

- **`tracking_app/flight_map.py`** – entry-point Flask app. Defines constants for Düsseldorf as the center and a 100 km search radius. Routes:
  - `/` renders `templates/map.html`.
  - `/flights` queries the OpenSky Network API for aircraft within a bounding box and returns raw state data as JSON.
  - `/map` uses Folium to generate a server-side map with markers and predicted paths.
- **`tracking_app/templates/map.html`** – Leaflet and jQuery front end that initializes the map, polls `/flights` every 15 seconds, and displays markers with a sidebar of flight details.

### Important things to know

- Server dependencies: Flask, `requests`, and `folium`. Client dependencies: Leaflet, jQuery, and PolylineDecorator.
- The `/flights` endpoint constructs a latitude/longitude bounding box and sends it to `https://opensky-network.org/api/states/all`.
- Center coordinates and radius are hardcoded in `flight_map.py`.
- Two rendering paths exist: server-side Folium via `/map` or client-side Leaflet via `/` + `/flights`.

### Pointers for learning next

- Learn the basics of Flask routing and template rendering.
- Compare Folium and Leaflet to decide when to render maps server-side vs. client-side.
- Explore the OpenSky API `states` array to interpret flight information.
- Review geospatial concepts such as converting kilometers to degrees and predicting positions using headings.
- Investigate front-end techniques for polling APIs and updating Leaflet layers dynamically.

## Installation

### Prerequisites
- Python 3.8+
- `pip` (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/yourusername/flight-tracker-local.git
cd flight-tracker-local
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### 1. Generate a live map from OpenSky data
```bash
python tracker.py
```
This creates a `flight_map.html` file with real-time aircraft positions.

### 2. (Optional) Start the Flask web server to serve the map
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Project Structure
```
flight-tracker-local/
├── tracker.py        # Main script for fetching and plotting flights
├── app.py            # Flask server to host the map
├── flight_map.html   # Output map (generated)
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Dependencies
- requests
- folium
- flask

Install them via:
```bash
pip install requests folium flask
```

## Configuration
Edit `tracker.py` to change:
- Center point (latitude/longitude)
- Radius (in km)

## License
MIT License

## Credits
- [OpenSky Network](https://opensky-network.org/) for real-time flight data
- [Folium](https://python-visualization.github.io/folium/) for map rendering

---

Happy tracking! ✈️
