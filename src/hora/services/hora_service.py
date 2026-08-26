"""Hora service — book §1.3.11."""
from __future__ import annotations

from hora.charts.hora import (
    HORA_LORD_CYCLE,
    HORAS_PER_DAY,
    NOMINAL_DAY_HOURS,
    HoraError,
    HoraResult,
)
from hora.charts.hora import (
    hora as _hora,
)
from hora.charts.hora import (
    horas_of_weekday as _horas_of_weekday,
)
from hora.core import validate
from hora.core.const import GRAHA_NAMES, HORA_LORD_ORDER, VAARA_LORD, VAARA_NAMES

InputError = validate.InputError

__all__ = ["HoraError", "InputError", "day", "hora", "rules"]


def _serialise(value: HoraResult) -> dict:
    return {
        "index": value.index,
        "lord": value.lord,
        "lord_name": value.lord_name,
        "position_in_cycle": value.position_in_cycle,
        "weekday": value.weekday,
        "weekday_name": value.weekday_name,
        "weekday_lord": value.weekday_lord,
        "weekday_lord_name": value.weekday_lord_name,
        "elapsed_hours": value.elapsed_hours,
        "day_length_hours": value.day_length_hours,
        "hora_length_hours": value.hora_length_hours,
        "steps": [
            {
                "number": s.number,
                "description": s.description,
                "detail": s.detail,
                "value": s.value,
            }
            for s in value.steps
        ],
    }


def hora(
    weekday: int,
    elapsed_hours: float,
    day_length_hours: float = NOMINAL_DAY_HOURS,
) -> dict:
    """The hora running so many hours after sunrise on a weekday."""
    return _serialise(_hora(weekday, elapsed_hours, day_length_hours))


def day(weekday: int) -> dict:
    """All 24 hora lords of a weekday, in order from sunrise."""
    validate.in_range("weekday", weekday, 0, 6)
    lords = _horas_of_weekday(weekday)
    return {
        "weekday": weekday,
        "weekday_name": str(VAARA_NAMES[weekday]),
        "weekday_lord_name": str(GRAHA_NAMES[VAARA_LORD[weekday]]),
        "horas": [
            {"index": i + 1, "lord": int(g), "lord_name": str(GRAHA_NAMES[g])}
            for i, g in enumerate(lords)
        ],
    }


def rules() -> dict:
    """§1.3.11's definitions, the speed order, and the weekday lords."""
    return {
        "section": "1.3.11",
        "title": "Hora",
        "definition": (
            "Each day starts at sunrise and ends at next day's sunrise. This "
            "period is divided into 24 equal parts and they are called horas."
        ),
        "approximation": "A hora is almost equal to an hour.",
        "horas_per_day": HORAS_PER_DAY,
        "cycle_length": HORA_LORD_CYCLE,
        "speed_order_rule": (
            "The lords of hora come in the order of decreasing speed with "
            "respect to earth: Saturn, Jupiter, Mars, Sun, Venus, Mercury and "
            "Moon. After Moon, we go back to Saturn and repeat the 7 planets."
        ),
        "speed_order": [
            {"position": i + 1, "graha": int(g), "name": str(GRAHA_NAMES[g])}
            for i, g in enumerate(HORA_LORD_ORDER)
        ],
        "first_hora_rule": (
            "The first hora of any day is ruled by the lord of the weekday. "
            "After that, we list planets in the order mentioned above."
        ),
        "weekday_lords": [
            {
                "weekday": i,
                "weekday_name": str(VAARA_NAMES[i]),
                "lord": int(g),
                "lord_name": str(GRAHA_NAMES[g]),
            }
            for i, g in enumerate(VAARA_LORD)
        ],
        "nominal_day_hours": NOMINAL_DAY_HOURS,
        "day_length_note": (
            "Section 1.3.11 divides the actual sunrise-to-sunrise interval "
            "into 24, so a hora is only approximately an hour. Its own worked "
            "example instead treats a hora as exactly one hour. "
            "day_length_hours defaults to 24, reproducing the example; pass "
            "the real interval for the other reading. See open item OI-40."
        ),
    }
