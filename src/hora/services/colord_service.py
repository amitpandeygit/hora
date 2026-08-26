"""Stronger co-lord service — §15.5.1.

Shapes the cascade for the API. Every rule reached is returned in order with
what it decided, because a caller checking a chart against JHora needs to see
which step diverged, not just that the lord did.
"""
from __future__ import annotations

from hora.charts.colord import CoLordError
from hora.charts.colord import stronger as _stronger
from hora.core import validate

InputError = validate.InputError

__all__ = ["CoLordError", "InputError", "stronger"]


def stronger(
    rasi: int,
    graha_longitudes: dict[int, float],
    purpose: str = "arudha",
    rasi_aspects: dict[int, list[int]] | None = None,
    dasa_years: dict[int, float] | None = None,
) -> dict:
    """Run §15.5.1's cascade for one co-owned rasi."""
    aspects = (
        {sign: tuple(targets) for sign, targets in rasi_aspects.items()}
        if rasi_aspects is not None else None
    )
    verdict = _stronger(rasi, graha_longitudes, purpose, aspects, dasa_years)
    return {
        "rasi": verdict.rasi,
        "rasi_name": verdict.rasi_name,
        "co_lords": list(verdict.co_lords),
        "co_lord_names": list(verdict.co_lord_names),
        "winner": verdict.winner,
        "winner_name": verdict.winner_name,
        "decided_by": verdict.decided_by,
        "determined": verdict.determined,
        "reason": verdict.reason,
        "rules": [
            {
                "rule": r.rule, "description": r.description,
                "winner": r.winner, "winner_name": r.winner_name,
                "evaluated": r.evaluated, "decided": r.decided, "detail": r.detail,
            }
            for r in verdict.rules
        ],
    }
