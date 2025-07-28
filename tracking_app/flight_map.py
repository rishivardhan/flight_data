from flask import Flask, render_template, jsonify, request
import folium
import requests

app = Flask(__name__)

DUSSELDORF_LAT, DUSSELDORF_LON = 51.2277, 6.7735
RADIUS_KM = 100

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/flights')
def flights():
    deg = RADIUS_KM / 111
    bounds = {
        "lamin": DUSSELDORF_LAT - deg,
        "lamax": DUSSELDORF_LAT + deg,
        "lomin": DUSSELDORF_LON - deg,
        "lomax": DUSSELDORF_LON + deg
    }
    response = requests.get("https://opensky-network.org/api/states/all", params=bounds)
    flights = response.json().get("states", [])
    return jsonify(flights)

@app.route('/map')
def map_view():
    m = folium.Map(location=[DUSSELDORF_LAT, DUSSELDORF_LON], zoom_start=9)
    folium.Circle([DUSSELDORF_LAT, DUSSELDORF_LON], radius=RADIUS_KM*1000, color='blue', fill=True, fill_opacity=0.1).add_to(m)
    deg = RADIUS_KM / 111
    bounds = {
        "lamin": DUSSELDORF_LAT - deg,
        "lamax": DUSSELDORF_LAT + deg,
        "lomin": DUSSELDORF_LON - deg,
        "lomax": DUSSELDORF_LON + deg
    }
    response = requests.get("https://opensky-network.org/api/states/all", params=bounds)
    flights = response.json().get("states", [])
    for f in flights:
        lat = f[6]
        lon = f[5]
        callsign = f[1] if f[1] else "N/A"
        velocity = f[9] if f[9] else 0
        heading = f[10] if f[10] else 0
        icao24 = f[0] if f[0] else ""
        airline = callsign[:3] if len(callsign) >= 3 else "Unknown"
        altitude = f[7] if f[7] else 0  # barometric altitude in meters
        altitude_ft = altitude * 3.28084 if altitude else 0
        marker_color = 'blue' if altitude_ft > 10000 else 'red'
        import math
        path = [[lat, lon]]
        # Project 10 points ahead, each ~2km
        for i in range(1, 11):
            step = 0.018 * i  # ~2km per step
            next_lat = lat + step * math.cos(math.radians(heading))
            next_lon = lon + step * math.sin(math.radians(heading))
            path.append([next_lat, next_lon])
        img_url = f"https://content.jetphotos.com/photos/medium/{icao24}.jpg"
        details = f"""
        <b>Callsign:</b> {callsign}<br>
        <b>ICAO24:</b> {icao24}<br>
        <b>Country of Origin:</b> {f[2]}<br>
        <b>Time Position:</b> {f[3]}<br>
        <b>Last Contact:</b> {f[4]}<br>
        <b>Longitude:</b> {lon}<br>
        <b>Latitude:</b> {lat}<br>
        <b>Barometric Altitude:</b> {altitude_ft:.0f} ft<br>
        <b>On Ground:</b> {f[8]}<br>
        <b>Velocity:</b> {velocity} m/s<br>
        <b>True Track:</b> {heading}°<br>
        <b>Vertical Rate:</b> {f[11]} m/s<br>
        <b>Sensors:</b> {f[12]}<br>
        <b>Geometric Altitude:</b> {f[13]}<br>
        <b>Squawk:</b> {f[14]}<br>
        <b>SPI:</b> {f[15]}<br>
        <b>Position Source:</b> {f[16]}<br>
        <b>Airline:</b> {airline}<br>
        <img src="{img_url}" alt="plane" style="width:200px;height:auto;" onerror="this.style.display='none';">
        """
        if lat is not None and lon is not None:
            folium.Marker([lat, lon], popup=details, icon=folium.Icon(color=marker_color, icon='plane', prefix='fa')).add_to(m)
            folium.PolyLine(path, color=marker_color, weight=2, opacity=0.7).add_to(m)
    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True, port=5002)
