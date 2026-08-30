"""Section 13.3 — baadhakas, service layer."""
from __future__ import annotations

from hora.charts.baadhaka import (
    BaadhakaError,
    baadhaka_of,
    is_baadhaka,
    table_31,
)
from hora.core.const import (
    BAADHAKA_EXAMPLE,
    BAADHAKA_EXAMPLE_STEPS,
    BAADHAKA_HOUSE_BY_MODALITY,
    BAADHAKA_INCLUDES_OCCUPANTS,
    BAADHAKA_MEANS,
    BAADHAKA_RULE,
    BAADHAKA_SCOPE,
    BAADHAKA_STHAANA_MEANS,
    BAADHAKA_TAKES_BOTH_CO_LORDS,
    GRAHA_NAMES,
    MODALITY_NAMES_EN,
    RASI_ABBR,
    RASI_NAMES,
    TABLE_31_BAADHAKAS,
)
from hora.core.validate import InputError


def _result(result) -> dict:
    return {
        "sign": result.sign,
        "sign_name": str(RASI_NAMES[result.sign]),
        "modality": result.modality,
        "house": result.house,
        "sthaana": result.sthaana,
        "sthaana_name": str(RASI_NAMES[result.sthaana]),
        "lords": [str(GRAHA_NAMES[g]) for g in result.lords],
        "occupants": [str(GRAHA_NAMES[g]) for g in result.occupants],
        "why": result.why,
    }


def of_sign(sign: int, graha_signs: dict[int, int] | None = None) -> dict:
    """The baadhaka sthaana of one sign — a house's or an arudha's."""
    return _result(baadhaka_of(sign, graha_signs))


def check(graha: int, sign: int,
          graha_signs: dict[int, int] | None = None) -> dict:
    """Whether one graha troubles whatever falls in `sign`."""
    return is_baadhaka(graha, sign, graha_signs)


def for_chart(lagna_sign: int,
              graha_signs: dict[int, int] | None = None) -> dict:
    """The baadhaka of every house from a lagna.

    §13.3 ends "we can consider baadhaka from every house and arudha pada in
    every divisional chart", so all twelve are given rather than lagna's only.
    """
    return {
        "lagna": lagna_sign,
        "lagna_name": str(RASI_NAMES[lagna_sign]),
        "scope": BAADHAKA_SCOPE,
        "houses": [
            {"house": house,
             **_result(baadhaka_of((lagna_sign + house - 1) % 12,
                                   graha_signs))}
            for house in range(1, 13)
        ],
    }


def rules() -> dict:
    """Section 13.3's rule, Table 31 and its worked example."""
    derived = table_31()
    return {
        "rule": BAADHAKA_RULE,
        "sthaana_means": BAADHAKA_STHAANA_MEANS,
        "baadhaka_means": BAADHAKA_MEANS,
        "house_by_modality": {
            name: house for name, house
            in zip(MODALITY_NAMES_EN, BAADHAKA_HOUSE_BY_MODALITY, strict=True)
        },
        "table_31": {
            abbr: {"sthaana": sthaana, "baadhakas": list(lords)}
            for abbr, (sthaana, lords) in TABLE_31_BAADHAKAS.items()
        },
        "table_31_is_derived": (
            "All twenty-four entries of Table 31 are derived from the rule "
            "above it and compared against the printed table, so each checks "
            "the other."
        ),
        "co_lords": BAADHAKA_TAKES_BOTH_CO_LORDS,
        "includes_occupants": BAADHAKA_INCLUDES_OCCUPANTS,
        "scope": BAADHAKA_SCOPE,
        "example": BAADHAKA_EXAMPLE,
        "example_steps": [
            {"reads": reads, "rasi": rasi, "sthaana": sthaana,
             "baadhakas": list(lords), "trouble": trouble}
            for reads, rasi, sthaana, lords, trouble in BAADHAKA_EXAMPLE_STEPS
        ],
        "derived_matches_printed": derived == TABLE_31_BAADHAKAS,
        "rasis": list(RASI_ABBR),
    }


__all__ = ["BaadhakaError", "InputError", "check", "for_chart", "of_sign",
           "rules"]
