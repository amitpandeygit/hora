"""Arudha pada service — §9.2.

Shapes the six-step derivation for the API. The steps themselves are in
:mod:`hora.charts.arudha`; nothing here computes anything.
"""
from __future__ import annotations

from hora.charts.arudha import (
    ARUDHA_GENERIC_NAMES,
    ARUDHA_SPECIAL_NAMES,
    ARUDHA_SPECIAL_SYMBOLS,
    ARUDHA_SPECIFIC_NAMES,
    ARUDHA_SYMBOLS,
    DUAL_LORDED,
    STRENGTH_COMPARISON_CHAPTER,
    ArudhaError,
    ArudhaPada,
    all_arudha_padas,
    arudha_pada,
)
from hora.charts.graha_arudha import (
    GRAHA_ARUDHA_SYMBOLS,
    GrahaArudhaError,
    all_graha_arudhas,
    graha_arudha,
)
from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_NAMES

InputError = validate.InputError

__all__ = [
    "ArudhaError", "GrahaArudhaError", "InputError", "graha", "graha_table",
    "one", "resolve_dual_lords", "rules", "table",
]


def resolve_dual_lords(
    graha_longitudes: dict[int, float],
    rasi_aspects: dict[int, tuple[int, ...]] | None = None,
    advancement_known: bool = True,
) -> dict[int, int]:
    """Build §9.2's ``stronger_lord`` map using §15.5.1's cascade.

    §9.2 says "take the stronger lord" and defers the comparison; §15.5.1 is
    that comparison. This runs it for Scorpio and Aquarius with
    ``purpose="arudha"``, so the step-5 tie-break is rule 5b — the planet more
    advanced in its rasi.

    A sign the cascade cannot decide is **omitted**, leaving the arudha
    endpoint to raise its usual error rather than answer from a guess.

    :param advancement_known: False when only signs are available. Rules basic
        to 4 still run; rule 5b cannot.
    """
    from hora.charts.colord import CO_LORDS, stronger

    resolved: dict[int, int] = {}
    for sign in CO_LORDS:
        try:
            verdict = stronger(
                sign, graha_longitudes, purpose="arudha",
                rasi_aspects=rasi_aspects, advancement_known=advancement_known,
            )
        except ValueError:
            continue
        if verdict.winner is not None:
            resolved[sign] = verdict.winner
    return resolved


def _resolve_from(
    graha_signs: dict[int, int],
    graha_longitudes: dict[int, float] | None,
    stronger_lord: dict[int, int] | None,
) -> dict[int, int]:
    """The ``stronger_lord`` map to use, filling gaps from §15.5.1.

    An explicit ``stronger_lord`` always wins — a caller who has decided is not
    overruled. Anything it leaves out is resolved by the cascade, from
    longitudes when they are given and from signs otherwise.
    """
    supplied = dict(stronger_lord or {})
    longitudes = graha_longitudes or {
        graha: sign * 30.0 for graha, sign in graha_signs.items()
    }
    derived = resolve_dual_lords(
        longitudes, advancement_known=graha_longitudes is not None
    )
    return derived | supplied


def _step(step) -> dict:
    return {
        "number": step.number,
        "name": step.name,
        "description": step.description,
        "sign": step.sign,
        "sign_name": step.sign_name,
        "count": step.count,
        "detail": step.detail,
    }


def _pada(pada: ArudhaPada) -> dict:
    return {
        "house": pada.house,
        "symbol": pada.symbol,
        "generic_names": list(pada.generic_names),
        "specific_names": list(pada.specific_names),
        "special_symbol": pada.special_symbol,
        "special_name": pada.special_name,
        "house_sign": pada.house_sign,
        "house_sign_name": pada.house_sign_name,
        "lord": pada.lord,
        "lord_name": pada.lord_name,
        "lord_sign": pada.lord_sign,
        "lord_sign_name": pada.lord_sign_name,
        "count": pada.count,
        "before_exception": pada.before_exception,
        "before_exception_name": pada.before_exception_name,
        "exception_applied": pada.exception_applied,
        "exception_position": pada.exception_position,
        "sign": pada.sign,
        "sign_name": pada.sign_name,
        "steps": [_step(s) for s in pada.steps],
    }


def one(
    house: int,
    lagna_sign: int,
    graha_signs: dict[int, int],
    stronger_lord: dict[int, int] | None = None,
    graha_longitudes: dict[int, float] | None = None,
) -> dict:
    """One house's arudha pada, with all six steps shown.

    A house in Scorpio or Aquarius has its lord resolved by §15.5.1 unless the
    caller names one. Supplying ``graha_longitudes`` lets that cascade reach
    rule 5b; with signs alone it can only reach rule 4.
    """
    lords = _resolve_from(graha_signs, graha_longitudes, stronger_lord)
    return _pada(arudha_pada(house, lagna_sign, graha_signs, lords))


def table(
    lagna_sign: int,
    graha_signs: dict[int, int],
    stronger_lord: dict[int, int] | None = None,
    include_steps: bool = True,
    graha_longitudes: dict[int, float] | None = None,
) -> dict:
    """All twelve arudha padas.

    :param include_steps: set False for just the answers. The steps are on by
        default because the derivation is the point of this endpoint.
    """
    lords = _resolve_from(graha_signs, graha_longitudes, stronger_lord)
    padas = [_pada(p) for p in all_arudha_padas(lagna_sign, graha_signs, lords)]
    if not include_steps:
        for entry in padas:
            entry.pop("steps")
    return {
        "lagna_sign": lagna_sign,
        "lagna_sign_name": RASI_NAMES[lagna_sign],
        "padas": padas,
    }


def rules() -> dict:
    """§9.2's procedure as data — the six steps and the dual-lordship note."""
    return {
        "section": "9.2 Computation of Bhava Arudhas",
        "steps": [
            {"number": 1, "name": "house_sign",
             "text": "Take sign containing the house of interest in the "
                     "divisional chart of interest."},
            {"number": 2, "name": "lord_sign",
             "text": "Find the sign occupied by the lord of that house."},
            {"number": 3, "name": "count_to_lord",
             "text": "Count signs from the house of interest to the sign "
                     "containing its lord. Counting is in the zodiacal "
                     "direction always."},
            {"number": 4, "name": "advance_from_lord",
             "text": "Count the same number of signs from the sign containing "
                     "the lord and find the ending sign."},
            {"number": 5, "name": "apply_exception",
             "text": "Exception: If the sign found thus in step (4) is in the "
                     "1st or 7th from the original sign in step (1), then we "
                     "take the 10th sign from the sign found in step (4). "
                     "Otherwise we don't make any change."},
            {"number": 6, "name": "arudha_pada",
             "text": "The resulting sign contains the arudha pada of the house "
                     "of interest."},
        ],
        "dual_lorded_signs": [
            {
                "sign": sign,
                "sign_name": RASI_NAMES[sign],
                "owners": [int(g) for g in owners],
                "owner_names": [GRAHA_NAMES[g] for g in owners],
                "rule": "take the stronger lord",
            }
            for sign, owners in DUAL_LORDED.items()
        ],
        "strength_comparison_defined_in": STRENGTH_COMPARISON_CHAPTER,
        "strength_comparison_available": True,
        "strength_comparison_note": (
            "Section 15.5.1 gives the rule: a cascade of five steps, stopping "
            "at the first that decides. /v1/colord/stronger runs it. Rule 2 "
            "needs rasi aspects, which the caller supplies; without them the "
            "cascade stops undecided rather than skipping to rule 3."
        ),
        "strength_comparison_section": "15.5.1 Stronger Co-Lord",
        "generic_names": list(ARUDHA_GENERIC_NAMES),
        "specific_names": [
            {"house": house, "symbol": ARUDHA_SYMBOLS[house],
             "names": list(names)}
            for house, names in sorted(ARUDHA_SPECIFIC_NAMES.items())
        ],
        "special_symbols": [
            {"house": house, "symbol": ARUDHA_SPECIAL_SYMBOLS[house],
             "name": ARUDHA_SPECIAL_NAMES[house]}
            for house in sorted(ARUDHA_SPECIAL_SYMBOLS)
        ],
    }


def _graha(arudha) -> dict:
    return {
        "graha": arudha.graha,
        "graha_name": arudha.graha_name,
        "symbol": arudha.symbol,
        "graha_sign": arudha.graha_sign,
        "graha_sign_name": arudha.graha_sign_name,
        "owned": list(arudha.owned),
        "owned_names": list(arudha.owned_names),
        "owned_sign": arudha.owned_sign,
        "owned_sign_name": arudha.owned_sign_name,
        "owned_decided_by": arudha.owned_decided_by,
        "owned_reason": arudha.owned_reason,
        "count": arudha.count,
        "before_exception": arudha.before_exception,
        "before_exception_name": arudha.before_exception_name,
        "exception_applied": arudha.exception_applied,
        "exception_position": arudha.exception_position,
        "sign": arudha.sign,
        "sign_name": arudha.sign_name,
        "steps": [_step(s) for s in arudha.steps],
    }


def graha(
    graha_id: int,
    graha_signs: dict[int, int],
    graha_longitudes: dict[int, float] | None = None,
) -> dict:
    """One planet's arudha pada — §9.5, with all six steps shown."""
    return _graha(graha_arudha(graha_id, graha_signs, graha_longitudes))


def graha_table(
    graha_signs: dict[int, int],
    graha_longitudes: dict[int, float] | None = None,
    include_steps: bool = True,
) -> dict:
    """All nine graha arudhas."""
    out = [_graha(a) for a in all_graha_arudhas(graha_signs, graha_longitudes)]
    if not include_steps:
        for entry in out:
            entry.pop("steps")
    return {"arudhas": out}


def graha_rules() -> dict:
    """§9.5's procedure as data — the six steps and the two-sign note."""
    from hora.charts.graha_arudha import TWO_SIGN_OWNERS
    from hora.core.const import GRAHA_NAMES, GRAHA_OWNS

    return {
        "section": "9.5 Computation of Graha Arudhas",
        "steps": [
            {"number": 1, "name": "graha_sign",
             "text": "Take the sign containing the planet of interest in the "
                     "divisional chart of interest."},
            {"number": 2, "name": "owned_sign",
             "text": "Find the sign owned by that planet."},
            {"number": 3, "name": "count_to_owned",
             "text": "Count signs from the sign containing the planet of "
                     "interest to the stronger sign owned by it. Counting is "
                     "in the zodiacal direction always."},
            {"number": 4, "name": "advance_from_owned",
             "text": "Count the same number of signs from the stronger sign "
                     "owned and find the ending sign."},
            {"number": 5, "name": "apply_exception",
             "text": "Exception: If the sign found thus in step (4) is in the "
                     "1st or 7th from the original sign containing the planet, "
                     "then we take the 10th sign from the sign found in step "
                     "(4). Otherwise we don't make any change."},
            {"number": 6, "name": "graha_arudha",
             "text": "The resulting sign contains the arudha pada of the "
                     "planet of interest."},
        ],
        "note": (
            "Mars, Mercury, Jupiter, Venus and Saturn own 2 signs each. In "
            "their case, take the stronger sign owned by the planet."
        ),
        "stronger_sign_section": "15.5.2 Stronger Rasi",
        "ownership": [
            {
                "graha": graha_id,
                "graha_name": GRAHA_NAMES[graha_id],
                "symbol": GRAHA_ARUDHA_SYMBOLS[graha_id],
                "owns": [int(s) for s in GRAHA_OWNS[graha_id]],
                "owns_names": [RASI_NAMES[s] for s in GRAHA_OWNS[graha_id]],
                "needs_comparison": graha_id in TWO_SIGN_OWNERS,
            }
            for graha_id in range(9)
        ],
    }
