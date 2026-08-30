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
    eighth_lord_method,
    houses_of_life,
    maheswara,
    maraka_grahas,
    maraka_houses,
    maraka_sthanas,
    marakas,
    rudra_candidates,
    three_pairs,
    trishoola_rasis,
)
from hora.charts.maraka import rudra as _rudra_cascade
from hora.core.const import (
    ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED,
    ADDITIONAL_MARAKA_RULE,
    ADDITIONAL_MARAKA_TARGETS,
    CHAPTER_14_ADMITS_ITS_GAPS,
    CHAPTER_14_CLOSING,
    CHAPTER_14_CLOSING_TYPO,
    CHAPTER_14_INTRO,
    CHAPTER_14_NOT_COVERED,
    CHAPTER_14_SCOPE,
    CHAPTER_14_USE_AND_CAUTION,
    EIGHTH_LORD_GROUPS,
    EIGHTH_LORD_METHOD_FAILED_HERE,
    EIGHTH_LORD_METHOD_RULE,
    EIGHTH_LORD_STRENGTH_IS_GIVEN,
    EIGHTH_LORD_USES_THE_ORDINARY_EIGHTH,
    EXAMPLE_47,
    EXAMPLE_47_CATEGORY,
    EXAMPLE_47_CHART,
    EXAMPLE_47_COVERS,
    EXAMPLE_47_PAIRS,
    EXAMPLE_47_PARAMAAYUSH,
    EXAMPLE_47_RESULT,
    EXAMPLE_48,
    EXAMPLE_48_BRANCHES,
    EXAMPLE_48_EIGHTH_LORD,
    EXAMPLE_48_REFERENCE,
    EXERCISE_23,
    EXERCISE_23_AGE_AT_DEATH,
    EXERCISE_23_CASCADE_STEP,
    EXERCISE_23_CATEGORY,
    EXERCISE_23_EIGHTH_LORD,
    EXERCISE_23_EIGHTH_LORD_CATEGORY,
    EXERCISE_23_MAHESWARA,
    EXERCISE_23_MAHESWARA_PLANET,
    EXERCISE_23_MAIN_MARAKAS,
    EXERCISE_23_MARAKAS,
    EXERCISE_23_MERCURY_IS_A_FURTHER_CONSIDERATION,
    EXERCISE_23_PAIR_CATEGORIES,
    EXERCISE_23_RUDRA,
    EXERCISE_23_RUDRA_PLANET,
    EXERCISE_23_RUDRA_RASI,
    EXERCISE_23_THREE_PAIRS,
    EXERCISE_23_TRISHOOLA,
    FOOTNOTE_50,
    GOOD_LONGEVITY_RULE,
    GRAHA_NAMES,
    HOUSES_OF_LIFE_RULE,
    LONGEVITY_RANGE_TEXT,
    LONGEVITY_RANGES,
    MAHESWARA_EXAMPLES,
    MAHESWARA_EXCEPTIONS,
    MAHESWARA_NODE_SUBSTITUTES,
    MAHESWARA_RULE,
    MAHESWARA_USES_THE_ORDINARY_EIGHTH,
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
    PARAMAAYUSH_CAN_EXCEED_THE_RANGE,
    PARAMAAYUSH_ONLY_FOR_THE_SPLIT_CASE,
    RASI_NAMES,
    RUDRA_AFFLICTION_MALEFICS,
    RUDRA_AFFLICTION_RULE,
    RUDRA_INTRO,
    RUDRA_MYTHOLOGY,
    RUDRA_RULE,
    RUDRA_STRENGTH_CASCADE,
    SIXTH_IS_THE_ANTIZODIACAL_EIGHTH,
    TABLE_32_CONSTRUCTION,
    TABLE_32_EIGHTH,
    TABLE_33_PRINTED,
    TABLE_34_FACTORS,
    TABLE_34_PARAMAAYUSH,
    TABLE_34_STRUCTURE,
    THREE_PAIRS,
    THREE_PAIRS_COMBINATION_RULE,
    THREE_PAIRS_INTRO,
    THREE_PAIRS_TIEBREAK_RULE,
    TRISHOOLA_RULE,
    WHICH_EIGHTH_HOUSE,
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
        "closing": CHAPTER_14_CLOSING,
        "closing_typo": CHAPTER_14_CLOSING_TYPO,
        "admits_its_gaps": CHAPTER_14_ADMITS_ITS_GAPS,
        "use_and_caution": list(CHAPTER_14_USE_AND_CAUTION),
        "examples": [
            {"lagna": lagna, "positions": dict(positions),
             "marakas": [{"graha": name, "why": why}
                         for name, why in expected]}
            for lagna, positions, expected in MARAKA_EXAMPLES
        ],
    }


def rudra(lagna: int) -> dict:
    """Section 14.3's two Rudra candidates for one lagna."""
    result = rudra_candidates(lagna)
    return {
        "lagna": result.from_lagna[0],
        "from_lagna": {"rasi": str(RASI_NAMES[result.from_lagna[0]]),
                       "lord": str(GRAHA_NAMES[result.from_lagna[1]])},
        "from_seventh": {"rasi": str(RASI_NAMES[result.from_seventh[0]]),
                         "lord": str(GRAHA_NAMES[result.from_seventh[1]])},
        "candidates": [str(GRAHA_NAMES[g]) for g in result.candidates],
        "rudra": result.rudra,
        "decided_by": result.decided_by,
        "why": result.why,
        "strength_cascade": list(RUDRA_STRENGTH_CASCADE),
        "affliction_rule": RUDRA_AFFLICTION_RULE,
        "framing": FRAMING,
    }


def trishoola(rudra_sign: int) -> dict:
    """The three Trishoola rasis from the rasi Rudra occupies."""
    signs = trishoola_rasis(rudra_sign)
    return {
        "rudra_sign": rudra_sign,
        "rudra_rasi": str(RASI_NAMES[rudra_sign]),
        "trishoola": [{"sign": s, "rasi": str(RASI_NAMES[s])} for s in signs],
        "rule": TRISHOOLA_RULE,
        "framing": FRAMING,
    }


def maheswara_for(ak_sign: int,
                  graha_signs: dict[int, int] | None = None) -> dict:
    """Section 14.3's Maheswara, with its three exceptions."""
    body = maheswara(ak_sign, graha_signs)
    body["rule"] = MAHESWARA_RULE
    body["exceptions"] = list(MAHESWARA_EXCEPTIONS)
    body["uses_the_ordinary_eighth"] = MAHESWARA_USES_THE_ORDINARY_EIGHTH
    body["framing"] = FRAMING
    return body


def section_14_3() -> dict:
    """Section 14.3's framing, Table 32 and the three definitions."""
    return {
        "mythology": RUDRA_MYTHOLOGY,
        "intro": RUDRA_INTRO,
        "table_32": dict(TABLE_32_EIGHTH),
        "footnote_50": FOOTNOTE_50,
        "table_32_construction": TABLE_32_CONSTRUCTION,
        "rudra_rule": RUDRA_RULE,
        "strength_cascade": list(RUDRA_STRENGTH_CASCADE),
        "affliction_rule": RUDRA_AFFLICTION_RULE,
        "affliction_malefics": list(RUDRA_AFFLICTION_MALEFICS),
        "trishoola_rule": TRISHOOLA_RULE,
        "maheswara_rule": MAHESWARA_RULE,
        "maheswara_uses_the_ordinary_eighth":
            MAHESWARA_USES_THE_ORDINARY_EIGHTH,
        "maheswara_exceptions": list(MAHESWARA_EXCEPTIONS),
        "maheswara_node_substitutes": dict(MAHESWARA_NODE_SUBSTITUTES),
        "maheswara_examples": [
            {"exception": which, "setup": setup, "yields": result}
            for which, setup, result in MAHESWARA_EXAMPLES
        ],
        "sixth_is_the_antizodiacal_eighth": SIXTH_IS_THE_ANTIZODIACAL_EIGHTH,
        "framing": FRAMING,
    }


def longevity(lagna: int, graha_signs: dict[int, int],
              hl_sign: int) -> dict:
    """Section 14.4's method of three pairs."""
    body = three_pairs(lagna, graha_signs, hl_sign)
    body["framing"] = FRAMING
    body["range_text"] = LONGEVITY_RANGE_TEXT
    body["paramaayush_scope"] = PARAMAAYUSH_ONLY_FOR_THE_SPLIT_CASE
    return body


def eighth_lord(reference: int, graha_signs: dict[int, int]) -> dict:
    """Section 14.5's eighth lord method, from a reference the caller names."""
    body = eighth_lord_method(reference, graha_signs)
    body["framing"] = FRAMING
    body["reference_is_the_callers"] = EIGHTH_LORD_STRENGTH_IS_GIVEN
    body["uses_the_ordinary_eighth"] = EIGHTH_LORD_USES_THE_ORDINARY_EIGHTH
    return body


def rudra_for(lagna: int, graha_signs: dict[int, int],
              graha_longitudes: dict[int, float] | None = None) -> dict:
    """Section 14.3's Rudra, run through the strength cascade."""
    body = _rudra_cascade(lagna, graha_signs, graha_longitudes)
    body["strength_cascade"] = list(RUDRA_STRENGTH_CASCADE)
    body["framing"] = FRAMING
    return body


def section_14_5() -> dict:
    """Section 14.5's rule, Example 48 and where the two 8ths are used."""
    return {
        "rule": EIGHTH_LORD_METHOD_RULE,
        "groups": [
            {"group": name, "houses": list(houses), "category": category}
            for name, houses, category in EIGHTH_LORD_GROUPS
        ],
        "uses_the_ordinary_eighth": EIGHTH_LORD_USES_THE_ORDINARY_EIGHTH,
        "which_eighth_house": [
            {"where": where, "eighth": which, "settled_by": how}
            for where, which, how in WHICH_EIGHTH_HOUSE
        ],
        "reference_is_the_callers": EIGHTH_LORD_STRENGTH_IS_GIVEN,
        "example_48": {
            "question": EXAMPLE_48,
            "reference": EXAMPLE_48_REFERENCE,
            "eighth_lord": EXAMPLE_48_EIGHTH_LORD,
            "branches": [
                {"rasis": list(rasis), "group": group, "category": category}
                for rasis, group, category in EXAMPLE_48_BRANCHES
            ],
        },
        "exercise_23": {
            "question": EXERCISE_23,
            "chart": 8,
            "marakas": EXERCISE_23_MARAKAS,
            "main_marakas": [{"graha": name, "why": why}
                             for name, why in EXERCISE_23_MAIN_MARAKAS],
            "mercury": EXERCISE_23_MERCURY_IS_A_FURTHER_CONSIDERATION,
            "rudra": EXERCISE_23_RUDRA,
            "rudra_planet": EXERCISE_23_RUDRA_PLANET,
            "rudra_rasi": EXERCISE_23_RUDRA_RASI,
            "cascade_step": EXERCISE_23_CASCADE_STEP,
            "trishoola": list(EXERCISE_23_TRISHOOLA),
            "maheswara": EXERCISE_23_MAHESWARA,
            "maheswara_planet": EXERCISE_23_MAHESWARA_PLANET,
            "three_pairs": EXERCISE_23_THREE_PAIRS,
            "category": EXERCISE_23_CATEGORY,
            "pair_categories": list(EXERCISE_23_PAIR_CATEGORIES),
            "age_at_death": EXERCISE_23_AGE_AT_DEATH,
            "eighth_lord": EXERCISE_23_EIGHTH_LORD,
            "eighth_lord_category": EXERCISE_23_EIGHTH_LORD_CATEGORY,
            "method_failed_here": EIGHTH_LORD_METHOD_FAILED_HERE,
        },
        "framing": FRAMING,
    }


def section_14_4() -> dict:
    """Section 14.4's rules, Table 33 and Table 34."""
    return {
        "intro": THREE_PAIRS_INTRO,
        "pairs": [{"pair": name, "note": note} for name, note in THREE_PAIRS],
        "table_33": [
            {"combination_1": first, "combination_2": second,
             "result": result}
            for first, second, result in TABLE_33_PRINTED
        ],
        "table_33_is_exhaustive": (
            "Table 33's six rows cover every unordered pair of the three "
            "modalities, so no combination can fall through."
        ),
        "ranges": {name: list(span)
                   for name, span in LONGEVITY_RANGES.items()},
        "range_text": LONGEVITY_RANGE_TEXT,
        "combination_rule": THREE_PAIRS_COMBINATION_RULE,
        "tiebreak_rule": THREE_PAIRS_TIEBREAK_RULE,
        "table_34": {third: dict(row)
                     for third, row in TABLE_34_PARAMAAYUSH.items()},
        "table_34_structure": TABLE_34_STRUCTURE,
        "table_34_factors": {k: list(v)
                             for k, v in TABLE_34_FACTORS.items()},
        "paramaayush_scope": PARAMAAYUSH_ONLY_FOR_THE_SPLIT_CASE,
        "paramaayush_can_exceed_the_range": PARAMAAYUSH_CAN_EXCEED_THE_RANGE,
        "eighth_uses_table_32": (
            "The first pair's 8th house comes from Table 32, as section 14.4 "
            "says in its own parenthesis — the same table Rudra uses, and not "
            "the ordinary 8th."
        ),
        "example_47": {
            "question": EXAMPLE_47,
            "chart": dict(EXAMPLE_47_CHART),
            "pairs": [
                {"pair": number, "working": working,
                 "combination": combination, "result": result}
                for number, working, combination, result in EXAMPLE_47_PAIRS
            ],
            "result_text": EXAMPLE_47_RESULT,
            "category": EXAMPLE_47_CATEGORY,
            "paramaayush_years": EXAMPLE_47_PARAMAAYUSH,
            "covers": EXAMPLE_47_COVERS,
        },
        "framing": FRAMING,
    }


__all__ = [
    "InputError",
    "MarakaError",
    "additional_marakas",
    "for_lagna",
    "longevity",
    "maheswara_for",
    "maraka_grahas",
    "maraka_sthanas",
    "rudra",
    "rules",
    "section_14_3",
    "section_14_4",
    "trishoola",
]
