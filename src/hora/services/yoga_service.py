"""Sun-Moon yoga service — book §1.3.9.

Standalone: §1.3.9's procedure needs two longitudes and nothing else.
`/v1/panchanga` reports the yoga running at an instant; this answers "what
yoga is this pair of longitudes" without a nativity.
"""
from __future__ import annotations

from hora.charts.yoga import (
    MINUTES_PER_DEGREE,
    YOGA_SPAN,
    YOGA_SPAN_MINUTES,
    YOGAS_PER_CIRCLE,
    Yoga,
    YogaError,
)
from hora.charts.yoga import (
    yoga as _yoga,
)
from hora.core import validate
from hora.core.const import YOGA_MEANINGS, YOGA_NAMES, YOGA_NAMES_BOOK

InputError = validate.InputError

__all__ = ["InputError", "YogaError", "rules", "table_5", "yoga"]


def _serialise(value: Yoga) -> dict:
    return {
        "index": value.index,
        "name": value.name,
        "name_book": value.name_book,
        "meaning": value.meaning,
        "sun_longitude": value.sun_longitude,
        "moon_longitude": value.moon_longitude,
        "raw_sum": value.raw_sum,
        "total": value.total,
        "total_minutes": value.total_minutes,
        "quotient": value.quotient,
        "completed": value.completed,
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


def yoga(sun_longitude: float, moon_longitude: float) -> dict:
    """The yoga running for a Sun and Moon longitude, with all five steps."""
    return _serialise(_yoga(sun_longitude, moon_longitude))


def table_5() -> list[dict]:
    """Table 5: Sun-Moon Yogas — index, yoga, meaning."""
    return [
        {
            "index": i + 1,
            "name": str(YOGA_NAMES_BOOK[i]),
            "name_simple": str(YOGA_NAMES[i]),
            "meaning": str(YOGA_MEANINGS[i]),
        }
        for i in range(YOGAS_PER_CIRCLE)
    ]


def rules() -> dict:
    """§1.3.9's procedure and Table 5."""
    return {
        "section": "1.3.9",
        "title": "Yogas",
        "procedure": [
            "Add the longitudes of Sun and Moon.",
            "Remove 360° from the sum if it is greater than 360°.",
            "Divide the sum by the length of one nakshatra (13°20' or 800').",
            "Ignore fractions and take the integer part.",
            "Add 1 to it and the result is the index of the yoga running.",
            "Refer to Table 5 and find the yoga corresponding to the index.",
        ],
        "span_degrees": YOGA_SPAN,
        "span_minutes": YOGA_SPAN_MINUTES,
        "minutes_per_degree": MINUTES_PER_DEGREE,
        "count": YOGAS_PER_CIRCLE,
        "uses_sum_not_difference": (
            "A yoga uses the sum of the two longitudes. A tithi uses the "
            "difference. The two are otherwise alike and are easily confused."
        ),
        "table_5": table_5(),
    }
