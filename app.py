from flask import Flask, request, render_template
from skyfield.api import utc, load, EarthSatellite
from datetime import datetime, timedelta, UTC
from tle import TLEs
import os

import urllib.request

if not os.path.exists("tles.txt"):
    print("Downloading TLEs...")
    try:
        urllib.request.urlretrieve(
            "http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle",
            "tles.txt"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


tles = TLEs()
tles.load("tles.txt")

ts = load.timescale()

def get_trajectory(satellite: EarthSatellite,
                   rev_count: int = 1, step: int = 60) -> list[dict]:

    rev_duration = 60/(satellite.model.no / (2 * 3.1415))
    start = ts.from_datetime(datetime.now(UTC).replace(tzinfo=utc))
    end = ts.from_datetime(
        (datetime.now(UTC) + timedelta(seconds=rev_duration * rev_count)).replace(tzinfo=utc)
    )

    positions = []
    time = start
    while time < end:
        geocentric = satellite.at(time).subpoint()
        positions.append({
            "lat": float(geocentric.latitude.degrees),
            "lon": float(geocentric.longitude.degrees)
        })
        time = time + timedelta(seconds=step)
    return positions

app = Flask(__name__)


@app.route('/api/search')
def hello_world():
    query = request.args.get("query")
    if not query: return "Pls gimme query", 418
    return [{"name": tle.satname, "id": tle.norad_id} for tle in tles.search(query)]

@app.route('/api/trajectory')
def trajectory():
    norad_id = request.args.get("norad_id")
    if not norad_id: return "Pls gimme satellite", 500
    if not norad_id.isdigit(): return "Invalid NORAD ID", 500

    satellite = tles.get_tle_by_id(int(norad_id))
    if not satellite: return "Unknown NORAD ID", 500

    return get_trajectory(satellite.get_satellite(), 3)

@app.route('/api/position')
def position():
    norad_id = request.args.get("norad_id")
    if not norad_id: return "Pls gimme satellite", 500
    if not norad_id.isdigit(): return "Invalid NORAD ID", 500

    satellite_tle = tles.get_tle_by_id(int(norad_id))
    if not satellite_tle: return "Unknown NORAD ID", 500

    satellite = satellite_tle.get_satellite()

    now = ts.from_datetime(datetime.now(UTC).replace(tzinfo=utc))
    geocentric = satellite.at(now).subpoint()

    return {
        "lat": float(geocentric.latitude.degrees),
        "lon": float(geocentric.longitude.degrees)
    }

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=8080, debug=True)
