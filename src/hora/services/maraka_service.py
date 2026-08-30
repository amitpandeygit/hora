"""Chapter 14 — longevity, service layer.

Every response carries §14.1's own framing on how the subject is used. That
is the book's paragraph, not a caveat we invented, and it is the first thing
the chapter says.
"""
from __future__ import annotations

from hora.charts.maraka import (
    MALEFICS,
    MarakaError,
    additional_marakas,
    houses_of_life,
    maraka_grahas,
    maraka_houses,
    maraka_sthanas,
    marakas,
)
from hora.core.const import (
    ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED,
    ADDITIONAL_MARAKA_RULE,
    ADDITIONAL_MARAKA_TARGETS,
    CHAPTER_14_INTRO,
    CHAPTER_14_NOT_COVERED,
    CHAPTER_14_SCOPE,
    GOOD_LONGEVITY_RULE,
    GRAHA_NAMES,
    HOUSES_OF_LIFE_RULE,
    MARAKA_CHART_ORDER,
    MARAKA_CHARTS,
    MARAKA_DERIVATION,
    MARAKA_EXAMPLES,
    MARAKA_GRAHA_MEANS,
    MARAKA_MEANS,
    MARAKA_STHANA_MEANS,
    MARAKA_STHANA_RULE,
    MARAKA_STRONGER_NOT_A_RULE,
    MARAKA_STRONGER_REMARK,
    MARAKA_USE,
)
from hora.core.validate import InputError

#: §14.1's framing, served with every answer.
FRAMING = CHAPTER_14_INTRO


def for_lagna(lagna: int, graha_signs: dict[int, int] | None = None) -> dict:
    """Every maraka for one lagna, with §14.1's framing attached."""
    body = marakas(lagna, graha_signs)
    body["framing"] = FRAMING
    body["use"] = MARAKA_USE
    body["powerfully_undefined"] = ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED
    body["not_ranked"] = MARAKA_STRONGER_NOT_A_RULE
    return body


def rules() -> dict:
    """Chapter 14's framing and section 14.2's rules."""
    return {
        "framing": CHAPTER_14_INTRO,
        "scope": CHAPTER_14_SCOPE,
        "not_covered": [{"what": what, "why": why}
                        for what, why in CHAPTER_14_NOT_COVERED],
        "maraka_means": MARAKA_MEANS,
        "maraka_sthana_means": MARAKA_STHANA_MEANS,
        "maraka_graha_means": MARAKA_GRAHA_MEANS,
        "charts": MARAKA_CHARTS,
        "chart_order": [{"chart": code, "why": why}
                        for code, why in MARAKA_CHART_ORDER],
        "houses_of_life_rule": HOUSES_OF_LIFE_RULE,
        "houses_of_life": {str(house): shows
                           for house, shows in houses_of_life().items()},
        "derivation": [
            {"house_of_life": life, "twelfth_from_it": death}
            for life, death in MARAKA_DERIVATION
        ],
        "maraka_houses": list(maraka_houses()),
        "good_longevity": GOOD_LONGEVITY_RULE,
        "sthana_rule": MARAKA_STHANA_RULE,
        "additional_rule": ADDITIONAL_MARAKA_RULE,
        "additional_targets": list(ADDITIONAL_MARAKA_TARGETS),
        "powerfully_undefined": ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED,
        "malefics": sorted(str(GRAHA_NAMES[g]) for g in MALEFICS),
        "malefics_note": (
            "Section 14.2 says 'a malefic planet' without listing them. The "
            "Moon's nature depends on his phase and Mercury's on his "
            "association, and neither worked example uses either, so neither "
            "is assumed malefic here. See OI-105."
        ),
        "stronger_remark": MARAKA_STRONGER_REMARK,
        "not_ranked": MARAKA_STRONGER_NOT_A_RULE,
        "use": MARAKA_USE,
        "examples": [
            {"lagna": lagna, "positions": dict(positions),
             "marakas": [{"graha": name, "why": why}
                         for name, why in expected]}
            for lagna, positions, expected in MARAKA_EXAMPLES
        ],
    }


__all__ = ["InputError", "MarakaError", "additional_marakas", "for_lagna",
           "maraka_grahas", "maraka_sthanas", "rules"]
