"""Tithi service — book §1.3.8.1.

Standalone: it takes two longitudes, not a nativity, because §1.3.8.1's
procedure needs nothing else. `/v1/panchanga` computes the tithi running at an
instant; this answers "what tithi is this pair of longitudes" without one.
"""
from __future__ import annotations

from hora.charts.tithi import (
    PAKSHA_ELONGATION,
    TITHI_SPAN,
    TITHIS_PER_MONTH,
    TITHIS_PER_PAKSHA,
    Tithi,
    TithiError,
)
from hora.charts.tithi import (
    tithi as _tithi,
)
from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    PAKSHA_DESCRIPTIONS,
    PAKSHA_NAMES,
    PAKSHA_SYNONYMS,
    TITHI_ALTERNATE_NAMES,
    TITHI_LORD,
    TITHI_NAMES_BOOK,
)

InputError = validate.InputError

__all__ = ["InputError", "TithiError", "rules", "tithi"]


def _serialise(value: Tithi) -> dict:
    return {
        "index": value.index,
        "number_in_paksha": value.number_in_paksha,
        "name": value.name,
        "full_name": value.full_name,
        "alternate_names": list(value.alternate_names),
        "paksha": value.paksha,
        "paksha_name": value.paksha_name,
        "lord": value.lord,
        "lord_name": value.lord_name,
        "raw_difference": round(value.raw_difference, 8),
        "elongation": round(value.elongation, 8),
        "completed": value.completed,
        "elapsed_in_tithi": round(value.elapsed_in_tithi, 8),
        "fraction_elapsed": round(value.fraction_elapsed, 8),
        "starts_at": value.starts_at,
        "ends_at": value.ends_at,
        "steps": [
            {"number": s.number, "name": s.name, "description": s.description,
             "value": s.value, "detail": s.detail}
            for s in value.steps
        ],
    }


def tithi(sun_longitude: float, moon_longitude: float) -> dict:
    """The tithi for a pair of longitudes, with all four steps shown."""
    return _serialise(_tithi(sun_longitude, moon_longitude))


def rules() -> dict:
    """§1.3.8.1 as data: the definition, the procedure and Table 3."""
    return {
        "section": "1.3.8.1 Tithis",
        "definition": (
            "Tithi or lunar day is a period in which the difference between "
            "the longitudes of Moon and Sun changes by exactly 12 degrees"
        ),
        "span_degrees": TITHI_SPAN,
        "per_month": TITHIS_PER_MONTH,
        "per_paksha": TITHIS_PER_PAKSHA,
        "month_starts": (
            "When Sun and Moon are at the same longitude, a new lunar month "
            "of 30 tithis starts"
        ),
        "steps": [
            {"number": 1, "name": "elongation",
             "text": "Find the difference: (Moon's longitude - Sun's "
                     "longitude). Add 360 degrees if the result is negative. "
                     "The result will be between 0 and 360 degrees and will "
                     "show how advanced Moon is with respect to Sun."},
            {"number": 2, "name": "completed",
             "text": "Divide this result by 12 degrees. Ignore the remainder "
                     "and take the quotient."},
            {"number": 3, "name": "index",
             "text": "Add 1 to the quotient. You get a number from 1 to 30. "
                     "That will give the index of the tithi running."},
            {"number": 4, "name": "name",
             "text": "Refer to Table 3 and find the name of the tithi. There "
                     "are 15 tithis and the same tithis repeat in the brigher "
                     "and darker fortnights."},
        ],
        "naming_convention": (
            "We write the classification of fortnight (Sukla or Krishna) "
            "first and then write tithi name"
        ),
        "pakshas": [
            {
                "index": index,
                "name": PAKSHA_NAMES[index],
                "synonyms": PAKSHA_SYNONYMS[index],
                "describes": PAKSHA_DESCRIPTIONS[index],
                "elongation_from": PAKSHA_ELONGATION[index][0],
                "elongation_to": PAKSHA_ELONGATION[index][1],
                "moon_is": "waxing" if index == 0 else "waning",
            }
            for index in range(len(PAKSHA_NAMES))
        ],
        "table_3": [
            {
                "sukla": number,
                "krishna": number + TITHIS_PER_PAKSHA
                if number < TITHIS_PER_PAKSHA else None,
                "name": TITHI_NAMES_BOOK[number - 1],
                "krishna_name": (
                    TITHI_NAMES_BOOK[number + TITHIS_PER_PAKSHA - 1]
                    if number < TITHIS_PER_PAKSHA else None
                ),
                "alternate_names": list(TITHI_ALTERNATE_NAMES[number]),
                "lord": int(TITHI_LORD[number - 1]),
                "lord_name": GRAHA_NAMES[TITHI_LORD[number - 1]],
            }
            for number in range(1, TITHIS_PER_PAKSHA + 1)
        ],
        "new_moon": {
            "index": TITHIS_PER_MONTH,
            "name": TITHI_NAMES_BOOK[TITHIS_PER_MONTH - 1],
            "note": "the 30th tithi; it has no counterpart in the brighter fortnight",
        },
        "full_moon": {
            "index": TITHIS_PER_PAKSHA,
            "name": TITHI_NAMES_BOOK[TITHIS_PER_PAKSHA - 1],
            "note": "the 15th tithi; it has no counterpart in the darker fortnight",
        },
    }
