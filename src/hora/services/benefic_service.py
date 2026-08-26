"""Natural benefic service — book §3.2.2."""
from __future__ import annotations

from hora.charts.benefic import (
    BENEFIC_NAMES,
    CONDITIONAL,
    INHERENT_NATURE_NOTE,
    MALEFIC_NAMES,
    BeneficError,
    Nature,
    fixed_grahas,
)
from hora.charts.benefic import (
    nature as _nature,
)
from hora.core import validate
from hora.core.const import GRAHA_NAMES, NATURAL_BENEFIC, NATURAL_MALEFIC

InputError = validate.InputError

__all__ = ["BeneficError", "InputError", "nature", "rules"]


def _serialise(value: Nature) -> dict:
    return {
        "graha": value.graha,
        "graha_name": value.graha_name,
        "nature": value.nature,
        "conditional": value.conditional,
        "reason": value.reason,
    }


def nature(
    graha: int,
    paksha: int | None = None,
    companions: list[int] | None = None,
) -> dict:
    """The natural benefic status of a graha, with the reason."""
    return _serialise(
        _nature(graha, paksha=paksha, companions=set(companions or []))
    )


def rules() -> dict:
    """§3.2.2's two clauses and which grahas each fixes."""
    fixed = fixed_grahas()
    return {
        "section": "3.2.2",
        "title": "Benefics and Malefics",
        "benefic_names": list(BENEFIC_NAMES),
        "malefic_names": list(MALEFIC_NAMES),
        "fixed_benefics": [
            {"graha": g, "name": str(GRAHA_NAMES[g])} for g in fixed["benefic"]
        ],
        "fixed_malefics": [
            {"graha": g, "name": str(GRAHA_NAMES[g])} for g in fixed["malefic"]
        ],
        "conditional": [
            {"graha": g, "name": str(GRAHA_NAMES[g])} for g in sorted(CONDITIONAL)
        ],
        "mercury_rule": (
            "Mercury becomes a natural benefic when he is alone or with more "
            "natural benefics. Mercury becomes a natural malefic when he is "
            "joined by more natural malefics."
        ),
        "moon_rule": (
            "Waxing Moon of Sukla paksha is a natural benefic. Waning Moon of "
            "Krishna paksha is a natural malefic."
        ),
        "equal_split_note": (
            "Section 3.2.2 covers Mercury alone, with more benefics, and with "
            "more malefics. An equal split is covered by none of the three "
            "and is reported as neutral rather than forced. See OI-45."
        ),
        "saturn_note": (
            "Section 3.2.2's malefic list omits Saturn. Page 102 corroborates "
            "that it is one, so Saturn is kept as a fixed malefic. See PVR-2."
        ),
        "inherent_nature_note": INHERENT_NATURE_NOTE,
        "counts": {
            "fixed_benefic": len(NATURAL_BENEFIC),
            "fixed_malefic": len(NATURAL_MALEFIC),
            "conditional": len(CONDITIONAL),
        },
    }
