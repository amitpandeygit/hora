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
    maheswara,
    maraka_grahas,
    maraka_houses,
    maraka_sthanas,
    marakas,
    rudra_candidates,
    three_pairs,
    trishoola_rasis,
)
from hora.core.const import (
    ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED,
    ADDITIONAL_MARAKA_RULE,
    ADDITIONAL_MARAKA_TARGETS,
    CHAPTER_14_INTRO,
    CHAPTER_14_NOT_COVERED,
    CHAPTER_14_SCOPE,
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
