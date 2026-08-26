"""Raw ephemeris service — positions without chart context."""
from __future__ import annotations

from hora.api.serialize import angle, envelope, sign_and_degree
from hora.charts.chart import Place
from hora.core.const import GRAHA_NAMES, NAVAGRAHA, Graha
from hora.core.ephemeris import get_ephemeris
from hora.core.settings import Settings
from hora.core.timeutil import Instant


def positions(instant: Instant, place: Place, settings: Settings) -> dict:
    eph = get_ephemeris(settings)
    if settings.topocentric:
        eph.set_observer(place.latitude, place.longitude, place.altitude)
    bodies = tuple(NAVAGRAHA)
    if settings.include_outer_planets:
        bodies += (Graha.URANUS, Graha.NEPTUNE, Graha.PLUTO)
    pos = eph.positions(instant.jd_ut, bodies)
    return {
        **envelope(instant, place, settings),
        "julian_day_ut": round(instant.jd_ut, 9),
        "utc": instant.utc.isoformat(),
        "ayanamsa": angle(eph.ayanamsa(instant.jd_ut)),
        "positions": [
            {
                "id": int(g),
                "name": GRAHA_NAMES[g],
                **sign_and_degree(p.longitude),
                "latitude": round(p.latitude, 8),
                "distance_au": round(p.distance, 10),
                "speed": round(p.speed_longitude, 8),
                "retrograde": p.is_retrograde,
            }
            for g, p in pos.items()
        ],
    }
