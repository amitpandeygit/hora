"""Shared request-to-domain conversion."""
from __future__ import annotations

from hora.api.schemas import BirthDataIn
from hora.charts.chart import Chart, Place, compute_chart
from hora.core.settings import Settings
from hora.core.timeutil import Instant, from_local


def to_instant(req: BirthDataIn) -> Instant:
    return from_local(
        req.year, req.month, req.day, req.hour, req.minute, req.second,
        tz_name=req.tz_name, utc_offset_hours=req.utc_offset_hours,
    )


def to_place(req: BirthDataIn) -> Place:
    p = req.place
    return Place(latitude=p.latitude, longitude=p.longitude, altitude=p.altitude, name=p.name)


def build_chart(req: BirthDataIn, settings: Settings) -> Chart:
    return compute_chart(to_instant(req), to_place(req), settings)
