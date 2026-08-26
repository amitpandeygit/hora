"""Stronger rasi service — §15.5.2.

Returns every rule reached with what it decided, so a caller checking a chart
against JHora can see which step diverged.
"""
from __future__ import annotations

from hora.charts.rasi_strength import (
    PURPOSE_ADAPTATIONS,
    RasiStrengthError,
)
from hora.charts.rasi_strength import (
    stronger as _stronger,
)
from hora.core import validate

InputError = validate.InputError

__all__ = ["InputError", "RasiStrengthError", "purposes", "stronger"]


def stronger(
    first: int,
    second: int,
    graha_longitudes: dict[int, float],
    purpose: str = "phalita",
    dasa_years: dict[int, float] | None = None,
    atma_karaka_rasi: int | None = None,
) -> dict:
    """Run §15.5.2's cascade for two rasis."""
    verdict = _stronger(
        first, second, graha_longitudes, purpose, dasa_years, atma_karaka_rasi
    )
    return {
        "first": verdict.first, "first_name": verdict.first_name,
        "second": verdict.second, "second_name": verdict.second_name,
        "purpose": verdict.purpose,
        "winner": verdict.winner, "winner_name": verdict.winner_name,
        "decided_by": verdict.decided_by, "determined": verdict.determined,
        "reason": verdict.reason,
        "rules": [
            {
                "rule": r.rule, "description": r.description,
                "winner": r.winner, "winner_name": r.winner_name,
                "decided": r.decided, "detail": r.detail,
            }
            for r in verdict.rules
        ],
    }


def purposes() -> dict:
    """§15.5.2's warning as data: which adaptation applies to which dasas."""
    return {
        "warning": (
            "The above rules are too general. One should understand the "
            "meaning of each rule and adapt based on the situation."
        ),
        "purposes": [
            {"key": key} | {k: v for k, v in entry.items()}
            for key, entry in PURPOSE_ADAPTATIONS.items()
        ],
    }
