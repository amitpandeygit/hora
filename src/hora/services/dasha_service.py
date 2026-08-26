"""Dasha service."""
from __future__ import annotations

from datetime import datetime

from hora.api.serialize import dasha_out, envelope
from hora.charts.chart import Place, compute_chart
from hora.core.const import Graha
from hora.core.settings import Settings
from hora.core.timeutil import Instant, from_local
from hora.dasha.base import balance_at_birth, compute_nakshatra_dasha, find_running
from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS


class UnknownDashaSystem(ValueError):
    """Raised when the requested dasa system is not implemented."""


class BadAsOf(ValueError):
    """Raised when ``as_of`` is not an ISO 8601 datetime."""


def dasha_tree(
    instant: Instant,
    place: Place,
    settings: Settings,
    *,
    system: str,
    levels: int,
    cycles: int,
    as_of: str | None,
    tz_name: str | None,
    utc_offset_hours: float | None,
) -> dict:
    """A nakshatra dasa tree, plus the chain running at ``as_of`` if given."""
    spec = NAKSHATRA_DASHA_SYSTEMS.get(system)
    if spec is None:
        raise UnknownDashaSystem(f"unknown dasha system {system!r}")

    chart = compute_chart(instant, place, settings)
    moon = chart.positions[Graha.MOON].longitude
    off = chart.instant.utc_offset_hours

    periods = compute_nakshatra_dasha(
        spec, moon, chart.instant.jd_ut, settings.dasha_year_length,
        levels=levels, cycles=cycles,
    )
    lord, balance_years = balance_at_birth(spec, moon)

    as_of_jd = chart.instant.jd_ut
    if as_of:
        try:
            dt = datetime.fromisoformat(as_of)
        except ValueError as exc:
            raise BadAsOf("as_of must be ISO 8601") from exc
        as_of_jd = from_local(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
            tz_name=tz_name, utc_offset_hours=utc_offset_hours,
        ).jd_ut

    return {
        **envelope(instant, place, settings),
        "system": {"key": spec.key, "name": spec.display_name,
                   "total_years": spec.total_years},
        "moon_longitude": round(moon, 8),
        "balance_at_birth": {"lord": lord, "years": round(balance_years, 8)},
        "year_length": settings.dasha_year_length.value,
        "periods": [dasha_out(p, off) for p in periods],
        "running": [
            {"level": p.level, "lord": p.lord, "lord_name": p.lord_name}
            for p in find_running(periods, as_of_jd)
        ],
    }
