from skyfield.api import Topos, EarthSatellite, Time,utc, load
from datetime import datetime, timedelta, UTC

from skyfield.toposlib import GeographicPosition

ts = load.timescale()

def get_current_position(sat: EarthSatellite) -> GeographicPosition:

    now = ts.from_datetime(datetime.now(UTC).replace(tzinfo=utc))
    return sat.at(now).subpoint()


# Topos(latitude_degrees=0, longitude_degrees=0, elevation_m=0)
def get_passes(sat: EarthSatellite, obs: Topos,
               start: Time, end: Time, min_el=1.0) -> list[dict]:

    output = []
    t, _ = sat.find_events(obs, start, end, altitude_degrees=0.0)
    for r,c,s in zip(t[::3], t[1::3], t[2::3]):
        dp = sat-obs
        if int(dp.at(c).altaz()[0].degrees) < min_el: continue
        positions = []
        time = r
        while time < s:
            alt, az, _ = dp.at(time).altaz()
            geocentric = sat.at(time).subpoint()
            positions.append({
                "az": az.degrees,
                "el": alt.degrees,
                "lat": geocentric.latitude.degrees,
                "lon": geocentric.longitude.degrees
            })
            time = time + timedelta(seconds=10)

        output.append({
            "start": {
                "dt": int(datetime.timestamp(r.utc_datetime())),
                "az": int(dp.at(r).altaz()[1].degrees),
                "el": int(dp.at(r).altaz()[0].degrees)
            },
            "max": {
                "dt": int(datetime.timestamp(c.utc_datetime())),
                "az": int(dp.at(c).altaz()[1].degrees),
                "el": int(dp.at(c).altaz()[0].degrees)
            },
            "end": {
                "dt": int(datetime.timestamp(s.utc_datetime())),
                "az": int(dp.at(s).altaz()[1].degrees),
                "el": int(dp.at(s).altaz()[0].degrees)
            },
            "positions": positions  # Add the positions list to the output
        })
    return output


def get_trajectory(satellite: EarthSatellite,
                   rev_count: int = 1, step: int = None) -> list[dict]:

    rev_duration = 60/(satellite.model.no / (2 * 3.1415))

    if not step: step = rev_duration/100

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
            "lon": float(geocentric.longitude.degrees),
            "alt": float(geocentric.elevation.km)
        })
        time = time + timedelta(seconds=step)
    return positions