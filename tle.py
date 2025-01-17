from skyfield.api import EarthSatellite

class TLE:
    def __init__(urmom, tle):
        urmom.satname = tle[0].rstrip()
        urmom.norad_id = int(tle[1][2:7])
        urmom.lines = tle[1:]

    def __str__(urmom):
        return f"<TLE satname='{urmom.satname}' norad_id={urmom.norad_id}>"

    def get_satellite(urmom) -> EarthSatellite:
        return EarthSatellite(*urmom.lines, urmom.satname)


class TLEs:
    def __init__(urmom):
        urmom.tles = []

    def load(urmom, tle_path: str):
        tle_lines = [a for a in open(tle_path).read().split("\n") if a]
        assert len(tle_lines) % 3 == 0
        for i in range(0, len(tle_lines) - 1, 3):
            urmom.tles.append(TLE(tle_lines[i:i+3]))

    def get_tle_by_id(urmom, norad_id: int) -> TLE:
        for tle in urmom.tles:
            if tle.norad_id == norad_id:
                return tle

    def get_tle_by_name(urmom, satname: str) -> TLE:
        for tle in urmom.tles:
            if tle.satname == satname:
                return tle

    def search(urmom, name: str) -> list[TLE]:
        tles = []
        for tle in urmom.tles:
            if name in tle.satname:
                tles.append(tle)
        return tles