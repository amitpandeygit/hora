"""Karana service — book §1.3.10."""
from __future__ import annotations

from hora.charts.karana import (
    FIRST_ONCE_ONLY_SLOT,
    FIRST_REPEATING_SLOT,
    KARANA_COUNT,
    KARANA_SLOTS,
    KARANA_SPAN,
    KARANAS_PER_TITHI,
    ONCE_ONLY_COUNT,
    REPEATING_COUNT,
    REPETITIONS,
    Karana,
    KaranaError,
)
from hora.charts.karana import (
    karana as _karana,
)
from hora.charts.karana import (
    karana_at as _karana_at,
)
from hora.charts.karana import (
    slot_of as _slot_of,
)
from hora.charts.karana import (
    slots_of_index as _slots_of_index,
)
from hora.core import validate
from hora.core.const import KARANA_NAMES, KARANA_NAMES_BOOK

InputError = validate.InputError

__all__ = [
    "InputError", "KaranaError", "at_longitudes", "for_slot", "for_tithi_half",
    "rules", "table",
]


def _serialise(value: Karana) -> dict:
    return {
        "slot": value.slot,
        "tithi": value.tithi,
        "half": value.half,
        "index": value.index,
        "name": value.name,
        "name_book": value.name_book,
        "repeats": value.repeats,
        "occurrences": value.occurrences,
    }


def for_slot(slot: int) -> dict:
    """The karana occupying a half-tithi slot, 1 to 60."""
    return _serialise(_karana(slot))


def for_tithi_half(tithi: int, half: int) -> dict:
    """The karana in a given half of a given tithi."""
    return _serialise(_karana(_slot_of(tithi, half)))


def at_longitudes(sun_longitude: float, moon_longitude: float) -> dict:
    """The karana running for a Sun and Moon longitude."""
    return _serialise(_karana_at(sun_longitude, moon_longitude))


def table() -> list[dict]:
    """The 11 karanas, with where each falls in a month."""
    return [
        {
            "index": i + 1,
            "name": str(KARANA_NAMES_BOOK[i]),
            "name_simple": str(KARANA_NAMES[i]),
            "repeats": i < REPEATING_COUNT,
            "occurrences": REPETITIONS if i < REPEATING_COUNT else 1,
            "slots": list(_slots_of_index(i + 1)),
        }
        for i in range(KARANA_COUNT)
    ]


def rules() -> dict:
    """§1.3.10's four statements, and the 11 karanas."""
    return {
        "section": "1.3.10",
        "title": "Karanas",
        "definition": "Each tithi is divided into 2 karanas.",
        "count": KARANA_COUNT,
        "karanas_per_tithi": KARANAS_PER_TITHI,
        "slots_per_month": KARANA_SLOTS,
        "span_degrees": KARANA_SPAN,
        "repeating_rule": (
            "The first 7 karanas repeat 8 times starting from the 2nd half of "
            "the first lunar day of a month."
        ),
        "repeating_count": REPEATING_COUNT,
        "repetitions": REPETITIONS,
        "first_repeating_slot": FIRST_REPEATING_SLOT,
        "once_only_rule": (
            "The last 4 karanas come just once in a month, starting from the "
            "2nd half of the 29th lunar day and ending at the 1st half of the "
            "first lunar day."
        ),
        "once_only_count": ONCE_ONLY_COUNT,
        "first_once_only_slot": FIRST_ONCE_ONLY_SLOT,
        "wraps_the_month": (
            "The four that come once straddle the month boundary: three close "
            "it and Kimstughna opens the next, so slot 1 carries the 11th "
            "name, not the 1st."
        ),
        "karanas": table(),
    }
