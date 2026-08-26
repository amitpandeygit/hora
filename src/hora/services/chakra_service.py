"""Chakra service — book §1.3.4.

Shapes a chart for the API, and gives other services one place to ask "what is
in this rasi / this house" without each rebuilding the buckets.

No drawing. The response carries what either family of styles needs — the rasi
for a rasi-based one, the house for a bhava-based one — so a renderer chooses
its own layout from the same object.
"""
from __future__ import annotations

from hora.charts.chakra import (
    CHART_STYLES,
    DEFAULT_REFERENCE,
    LAGNA_MARK,
    STYLES_USED_IN_THE_BOOK,
    Body,
    Chakra,
    ChakraError,
    build,
)
from hora.core import validate
from hora.services import reference_service

InputError = validate.InputError

# DEFAULT_REFERENCE is imported above and re-exported here, so a router can
# pass "the caller said nothing" through without importing a calculation
# module — see test_routers_do_not_import_calculation_modules.

__all__ = [
    "DEFAULT_REFERENCE", "ChakraError", "InputError", "chakra", "chart",
    "styles",
]


def _body(body: Body) -> dict:
    return {
        "kind": body.kind,
        "id": body.id,
        "name": body.name,
        "rasi": body.rasi,
        "longitude": body.longitude,
        "degrees_in_rasi": (
            None if body.degrees_in_rasi is None
            else round(body.degrees_in_rasi, 8)
        ),
    }


def _cell(cell) -> dict:
    return {
        "rasi": cell.rasi,
        "rasi_name": cell.rasi_name,
        "abbreviation": cell.abbreviation,
        "rasi_number": cell.rasi_number,
        "house": cell.house,
        "is_empty": cell.is_empty,
        "bodies": [_body(b) for b in cell.bodies],
    }


def chakra(built: Chakra) -> dict:
    """Serialise an already-built chart.

    Separate from :func:`chart` so a service that has produced a
    :class:`~hora.charts.chakra.Chakra` by another route can render the same
    shape without going back through the inputs.
    """
    return {
        "reference": built.reference,
        "reference_rasi": built.reference_rasi,
        "reference_rasi_name": (
            None if built.reference_rasi is None
            else built.cells[built.reference_rasi].rasi_name
        ),
        "has_houses": built.reference_rasi is not None,
        "cells": [_cell(c) for c in built.cells],
        "occupied_rasis": list(built.occupied_rasis),
        "empty_rasis": list(built.empty_rasis),
        "body_count": len(built.bodies),
    }


def chart(
    graha_positions: dict[int, float] | None = None,
    upagraha_positions: dict[int, float] | None = None,
    special_lagna_positions: dict[int, float] | None = None,
    lagna: float | None = None,
    positions_are_longitudes: bool = True,
    reference: str | None = DEFAULT_REFERENCE,
    reference_rasi: int | None = None,
) -> dict:
    """Build and serialise a chart from the bodies §1.3.4 names."""
    return chakra(build(
        graha_positions, upagraha_positions, special_lagna_positions, lagna,
        positions_are_longitudes=positions_are_longitudes,
        reference=reference, reference_rasi=reference_rasi,
    ))


def styles() -> dict:
    """§1.3.4's three drawing styles and the distinction that matters.

    The styles differ in looks, which is a renderer's problem. They differ in
    *substance* in one respect only: whether a fixed position holds a rasi or
    a house.
    """
    return {
        "sanskrit": "chakra",
        "prepared_from": (
            "the rasis occupied by all planets, upagrahas, lagna and special "
            "lagnas"
        ),
        "cells": 12,
        "lagna_mark": LAGNA_MARK,
        "bhava_name": reference_service.house_definition()["sanskrit"],
        "used_in_the_book": list(STYLES_USED_IN_THE_BOOK),
        "styles": [
            {"key": key} | {k: v for k, v in entry.items()}
            for key, entry in CHART_STYLES.items()
        ],
    }
