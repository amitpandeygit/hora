"""Lunar month service — book §1.3.8.2.

Standalone: §1.3.8.2 names a month from *where* the Sun-Moon conjunction
happened, so a longitude is the whole input. `/v1/panchanga` reports the month
running at an instant, which needs an ephemeris; this answers "which month
does a conjunction here start" without one.
"""
from __future__ import annotations

from hora.charts.maasa import (
    ADHIKA,
    FIRST_MONTH_RASI,
    NIJA,
    Maasa,
    MaasaError,
)
from hora.charts.maasa import (
    maasa as _maasa,
)
from hora.charts.maasa import (
    month_pair as _month_pair,
)
from hora.core import validate
from hora.core.const import (
    ADHIKA_MAASA_INTERVAL_YEARS,
    CONJUNCTION_APPROXIMATE_NOTE,
    CONJUNCTION_DEFINITION,
    LUNAR_MONTH_DAYS_BOOK,
    LUNAR_YEAR_DAYS_BOOK,
    MAASA_MEANING,
    MAASA_QUALIFIERS,
    MASA_APPROXIMATE_GREGORIAN_BOOK,
    MASA_FROM_CONJUNCTION_RASI,
    MASA_FULL_MOON_NAKSHATRA_BOOK,
    MASA_NAMES,
    MASA_NAMES_BOOK,
    RASI_NAMES,
    SOLAR_YEAR_DAYS_BOOK,
)

InputError = validate.InputError

__all__ = ["InputError", "MaasaError", "maasa", "month_pair", "rules"]


def _serialise(value: Maasa) -> dict:
    return {
        "conjunction_longitude": value.conjunction_longitude,
        "conjunction_rasi": value.conjunction_rasi,
        "conjunction_rasi_name": value.conjunction_rasi_name,
        "index": value.index,
        "name": value.name,
        "name_book": value.name_book,
        "full_name": value.full_name,
        "qualifier": value.qualifier,
        "full_moon_nakshatra": value.full_moon_nakshatra,
        "approximate_gregorian": value.approximate_gregorian,
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


def maasa(conjunction_longitude: float, qualifier: str | None = None) -> dict:
    """Name the lunar month a conjunction at this longitude starts."""
    return _serialise(_maasa(conjunction_longitude, qualifier))


def month_pair(first: float, second: float) -> dict:
    """The two months of an adhika year, both left unqualified.

    §1.3.8.2 names the pair Nija and Adhika but never says which is which, so
    neither is labelled here. See ``qualifier_undecided`` in the response.
    """
    a, b = _month_pair(first, second)
    return {
        "rasi": a.conjunction_rasi,
        "rasi_name": a.conjunction_rasi_name,
        "month_name": a.name_book,
        "months": [_serialise(a), _serialise(b)],
        "qualifiers": sorted(MAASA_QUALIFIERS),
        "qualifier_meanings": dict(MAASA_QUALIFIERS),
        "qualifier_undecided": (
            "Section 1.3.8.2 states that one is Nija and the other Adhika, but "
            "not which. Neither is labelled here. See open item OI-3."
        ),
    }


def table_4() -> list[dict]:
    """Table 4: Lunar Months, all four columns, in the book's own order."""
    rows = []
    for offset in range(12):
        rasi = (FIRST_MONTH_RASI + offset) % 12
        index = int(MASA_FROM_CONJUNCTION_RASI[rasi])
        rows.append(
            {
                "conjunction_rasi": rasi,
                "conjunction_rasi_name": str(RASI_NAMES[rasi]),
                "month_name": str(MASA_NAMES_BOOK[index]),
                "month_name_simple": str(MASA_NAMES[index]),
                "full_moon_nakshatra": str(MASA_FULL_MOON_NAKSHATRA_BOOK[index]),
                "approximate_gregorian": str(MASA_APPROXIMATE_GREGORIAN_BOOK[index]),
            }
        )
    return rows


def rules() -> dict:
    """§1.3.8.2's definitions, Table 4, and the adhika maasa arithmetic."""
    return {
        "section": "1.3.8.2",
        "title": "Lunar Months",
        "definition": (
            "A new lunar month starts whenever Sun and Moon are at the same "
            "longitude."
        ),
        "naming_rule": (
            "The name of a lunar month is decided by the rasi in which "
            "Sun-Moon conjunction takes place."
        ),
        "naming_origin": (
            "These names come from the constellation that Moon is most likely "
            "to occupy on the full Moon day."
        ),
        "maasa_meaning": MAASA_MEANING,
        "month_length_days": list(LUNAR_MONTH_DAYS_BOOK),
        "conjunction_definition": CONJUNCTION_DEFINITION,
        "conjunction_approximate_note": CONJUNCTION_APPROXIMATE_NOTE,
        "solar_year_days": SOLAR_YEAR_DAYS_BOOK,
        "lunar_year_days": LUNAR_YEAR_DAYS_BOOK,
        "adhika_interval_years": ADHIKA_MAASA_INTERVAL_YEARS,
        "adhika_rule": (
            "Once in every 3 years, this difference accumulates to one month "
            "and an extra lunar month comes. This results in Sun-Moon "
            "conjunction coming twice in the same rasi."
        ),
        "qualifiers": {NIJA: MAASA_QUALIFIERS[NIJA], ADHIKA: MAASA_QUALIFIERS[ADHIKA]},
        "table_4": table_4(),
    }
