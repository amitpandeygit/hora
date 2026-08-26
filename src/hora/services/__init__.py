"""Application services — everything the HTTP layer would otherwise do itself.

Routers are responsible for HTTP alone: parse the request, call one service,
return the result. Every decision worth testing lives here instead, because a
router is awkward to test and things hide in it. The one serious bug this
project has shipped — a thirteen-hour error in the pre-dawn upagraha period —
lived in a router for exactly that reason.
"""
from hora.services import house_service, lagna_service, varga_service
from hora.services.chart_service import (
    rasi_chart,
    shodasavarga_charts,
    special_lagnas,
    upagraha_chart,
    varga_charts,
)
from hora.services.dasha_service import dasha_tree
from hora.services.panchanga_service import panchanga_for

__all__ = [
    "dasha_tree",
    "house_service",
    "lagna_service",
    "panchanga_for",
    "rasi_chart",
    "shodasavarga_charts",
    "special_lagnas",
    "upagraha_chart",
    "varga_charts",
    "varga_service",
]
