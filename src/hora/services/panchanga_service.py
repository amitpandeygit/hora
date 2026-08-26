"""Panchanga service."""
from __future__ import annotations

from hora.api.serialize import envelope, panchanga_out
from hora.charts.chart import Place
from hora.core.settings import Settings
from hora.core.timeutil import Instant
from hora.panchanga.core import compute_panchanga


def panchanga_for(instant: Instant, place: Place, settings: Settings) -> dict:
    """Five limbs and the day structure. Raises ValueError at polar latitudes."""
    panchanga = compute_panchanga(
        instant, place.latitude, place.longitude, settings, place.altitude
    )
    return {**envelope(instant, place, settings), **panchanga_out(panchanga)}
