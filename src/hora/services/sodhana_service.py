"""Section 12.7 — Sodhya Pindas, service layer."""
from __future__ import annotations

from hora.charts.ashtakavarga import (
    AshtakavargaError,
    bhinnashtakavarga,
    ekaadhipatya_sodhana,
    sodhya_pinda,
    trikona_sodhana,
)
from hora.core.const import (
    EKAADHIPATYA_OCCUPANCY_UNDEFINED,
    EKAADHIPATYA_RULES_ALL_EXERCISED,
    EKAADHIPATYA_SODHANA_MEANS,
    EKAADHIPATYA_SODHANA_RULE,
    EKAADHIPATYA_SODHANA_RULES,
    EKAADHIPATYA_TIE_IS_UNCOVERED,
    EKAADHIPATYA_TIE_READING,
    EKAADHIPATYA_UNPAIRED,
    ELEMENT_NAMES,
    EXAMPLE_40,
    EXAMPLE_40_ANSWER,
    EXAMPLE_40_CHART,
    EXAMPLE_40_OWNER,
    EXAMPLE_40_WORKED,
    EXAMPLE_41,
    EXAMPLE_41_ANSWER,
    EXAMPLE_42,
    EXAMPLE_42_CASES,
    EXAMPLE_43,
    EXAMPLE_43_GRAHA_PINDA,
    EXAMPLE_43_GRAHA_PRODUCTS,
    EXAMPLE_43_RASI_PINDA,
    EXAMPLE_43_RASI_PRODUCTS,
    EXAMPLE_43_SOAV,
    EXAMPLE_43_SODHYA_PINDA,
    FOOTNOTE_45_NOT_IMPLEMENTED,
    FOOTNOTE_45_ROOMS,
    GRAHA_NAMES,
    GRAHA_PINDA_EXCLUDES_LAGNA,
    GRAHA_PINDA_RULE,
    RASI_NAMES,
    RASI_PINDA_RULE,
    SOAV_IS_A_REDUCED_BAV,
    SOAV_MEANS,
    SODHYA_PINDA_DEFINITION,
    SODHYA_PINDA_FOOTNOTE_45,
    SODHYA_PINDA_RULE,
    SODHYA_PINDAS_INTRO,
    TABLE_28_RASIMANA,
    TABLE_29_GRAHAMANA,
    TRIKONA_SODHANA_DISPUTED_CASE,
    TRIKONA_SODHANA_FOOTNOTE_44,
    TRIKONA_SODHANA_MEANS,
    TRIKONA_SODHANA_RULE,
    TRIKONA_SODHANA_RULES,
    TRINE_SET_NAMES,
)
from hora.core.validate import InputError

ONLY_RULE_THREE = (
    "Only rule (3) is implemented. Footnote 44 says why: '(1) and (2) are "
    "special cases cases of (3)'. Subtracting the lowest does nothing when "
    "the lowest is zero, which is rule (1), and zeroes all three when they "
    "are equal, which is rule (2). Each trine below still reports which rule "
    "describes what happened, because that is what Example 40 narrates."
)


def trikona(owner: str, rekhas: list[int] | None,
            reference_signs: dict[str, int] | None) -> dict:
    """Section 12.7.1's trinal reduction of one planet's BAV."""
    counts = (
        list(bhinnashtakavarga(owner, reference_signs).rekhas)
        if reference_signs is not None else list(rekhas or [])
    )
    result = trikona_sodhana(owner, counts)
    return {
        "owner": result.owner,
        "rule": TRIKONA_SODHANA_RULE,
        "rules": list(TRIKONA_SODHANA_RULES),
        "before": list(result.before),
        "after": list(result.after),
        "trines": [
            {
                "element": trine.element,
                "element_name": f"{TRINE_SET_NAMES[trine.element]} trines",
                "signs": list(trine.signs),
                "sign_names": [str(RASI_NAMES[s]) for s in trine.signs],
                "before": list(trine.before),
                "after": list(trine.after),
                "lowest": trine.lowest,
                "rule": trine.rule,
                "rule_text": TRIKONA_SODHANA_RULES[trine.rule - 1],
            }
            for trine in result.trines
        ],
        "footnote_44": TRIKONA_SODHANA_FOOTNOTE_44,
        "only_rule_three_is_implemented": ONLY_RULE_THREE,
        "means": TRIKONA_SODHANA_MEANS,
        "elements": list(ELEMENT_NAMES),
    }


def ekaadhipatya(owner: str, rekhas: list[int] | None,
                 reference_signs: dict[str, int] | None,
                 occupied_signs: list[int],
                 already_trikona_reduced: bool) -> dict:
    """Section 12.7.2's co-owned reduction.

    :param already_trikona_reduced: section 12.7.2 begins "After we carry out
        Trikona Sodhana", so a BAV that has not been through 12.7.1 is the
        wrong input. Say so explicitly rather than have us guess.
    """
    counts = (
        list(bhinnashtakavarga(owner, reference_signs).rekhas)
        if reference_signs is not None else list(rekhas or [])
    )
    if not already_trikona_reduced:
        counts = list(trikona_sodhana(owner, counts).after)
    result = ekaadhipatya_sodhana(owner, counts, occupied_signs)
    flagged = [p for p in result.pairs if p.tie_not_covered_by_the_book]
    return {
        "owner": result.owner,
        "rule": EKAADHIPATYA_SODHANA_RULE,
        "rules": [{"number": number, "text": text}
                  for number, text in EKAADHIPATYA_SODHANA_RULES],
        "trikona_applied_first": not already_trikona_reduced,
        "before": list(result.before),
        "after": list(result.after),
        "occupied_signs": sorted(set(occupied_signs)),
        "pairs": [
            {
                "signs": list(pair.signs),
                "sign_names": [str(RASI_NAMES[s]) for s in pair.signs],
                "lord": str(GRAHA_NAMES[pair.lord]),
                "before": list(pair.before),
                "after": list(pair.after),
                "occupied": list(pair.occupied),
                "rule": pair.rule,
                "tie_not_covered_by_the_book":
                    pair.tie_not_covered_by_the_book,
            }
            for pair in result.pairs
        ],
        "untouched": {
            "signs": list(result.untouched),
            "sign_names": [str(RASI_NAMES[s]) for s in result.untouched],
            "why": (
                "Cancer and Leo have one owner each, so they are in no "
                "co-owned pair and section 12.7.2 never reaches them."
            ),
        },
        "occupancy_undefined": EKAADHIPATYA_OCCUPANCY_UNDEFINED,
        "tie_is_uncovered": EKAADHIPATYA_TIE_IS_UNCOVERED,
        "tie_reading": EKAADHIPATYA_TIE_READING,
        "tie_hit_in_this_chart": [list(p.signs) for p in flagged],
    }


def pinda(owner: str, reference_signs: dict[str, int],
          graha_signs: dict[str, int], occupied_signs: list[int]) -> dict:
    """Section 12.7.3's sodhya pinda, run end to end from a chart.

    BAV, then 12.7.1, then 12.7.2, then the pinda — the order 12.7.3 states.
    Every intermediate is returned, because the pinda is one number and a
    caller who cannot see the SoAV cannot check it.
    """
    bav = bhinnashtakavarga(owner, reference_signs)
    trikona_step = trikona_sodhana(owner, bav.rekhas)
    ekaadhipatya_step = ekaadhipatya_sodhana(
        owner, trikona_step.after, occupied_signs)
    result = sodhya_pinda(owner, ekaadhipatya_step.after, graha_signs)
    ties = [list(p.signs) for p in ekaadhipatya_step.pairs
            if p.tie_not_covered_by_the_book]
    return {
        "owner": result.owner,
        "definition": SODHYA_PINDA_DEFINITION,
        "steps": {
            "bav": list(bav.rekhas),
            "after_trikona": list(trikona_step.after),
            "soav": list(result.soav),
        },
        "rasi_pinda": {
            "rule": RASI_PINDA_RULE,
            "total": result.rasi_pinda,
            "products": [
                {"rasi": str(RASI_NAMES[sign]), "rekhas": rekhas,
                 "multiplier": multiplier, "product": product}
                for sign, rekhas, multiplier, product in result.rasi_products
            ],
        },
        "graha_pinda": {
            "rule": GRAHA_PINDA_RULE,
            "total": result.graha_pinda,
            "excludes_lagna": GRAHA_PINDA_EXCLUDES_LAGNA,
            "products": [
                {"planet": planet, "rasi": str(RASI_NAMES[sign]),
                 "rekhas": rekhas, "multiplier": multiplier,
                 "product": product}
                for planet, sign, rekhas, multiplier, product
                in result.graha_products
            ],
        },
        "sodhya_pinda": result.sodhya_pinda,
        "rule": SODHYA_PINDA_RULE,
        "tie_hit_in_this_chart": ties,
        "tie_reading": EKAADHIPATYA_TIE_READING if ties else None,
        "occupancy_undefined": EKAADHIPATYA_OCCUPANCY_UNDEFINED,
    }


def rules() -> dict:
    """Section 12.7's framing, its three rules, and Example 40."""
    return {
        "intro": SODHYA_PINDAS_INTRO,
        "soav_means": SOAV_MEANS,
        "soav_is_a_reduced_bav": SOAV_IS_A_REDUCED_BAV,
        "sodhya_pinda": {
            "definition": SODHYA_PINDA_DEFINITION,
            "rasi_pinda_rule": RASI_PINDA_RULE,
            "graha_pinda_rule": GRAHA_PINDA_RULE,
            "rule": SODHYA_PINDA_RULE,
            "table_28_rasimana": list(TABLE_28_RASIMANA),
            "table_29_grahamana": dict(TABLE_29_GRAHAMANA),
            "excludes_lagna": GRAHA_PINDA_EXCLUDES_LAGNA,
            "inherits": (
                "A pinda is computed from a SoAV, so it inherits both of "
                "section 12.7.2's open questions: D-41's uncovered tie and "
                "OI-104's undefined occupancy. Neither reaches Example 43, "
                "whose pairs all stop at rule (1)."
            ),
            "footnote_45": SODHYA_PINDA_FOOTNOTE_45,
            "footnote_45_rooms": dict(FOOTNOTE_45_ROOMS),
            "footnote_45_not_implemented": FOOTNOTE_45_NOT_IMPLEMENTED,
        },
        "example_43": {
            "question": EXAMPLE_43,
            "soav": list(EXAMPLE_43_SOAV),
            "rasi_pinda": EXAMPLE_43_RASI_PINDA,
            "graha_pinda": EXAMPLE_43_GRAHA_PINDA,
            "sodhya_pinda": EXAMPLE_43_SODHYA_PINDA,
            "rasi_products": [
                {"rasi": rasi, "rekhas": rekhas, "multiplier": multiplier,
                 "product": product}
                for rasi, rekhas, multiplier, product
                in EXAMPLE_43_RASI_PRODUCTS
            ],
            "graha_products": [
                {"planet": planet, "rasi": rasi, "rekhas": rekhas,
                 "multiplier": multiplier, "product": product}
                for planet, rasi, rekhas, multiplier, product
                in EXAMPLE_43_GRAHA_PRODUCTS
            ],
            "chart": "Chart 6",
        },
        "ekaadhipatya_sodhana": {
            "means": EKAADHIPATYA_SODHANA_MEANS,
            "rule": EKAADHIPATYA_SODHANA_RULE,
            "rules": [{"number": number, "text": text}
                      for number, text in EKAADHIPATYA_SODHANA_RULES],
            "unpaired": list(EKAADHIPATYA_UNPAIRED),
            "unpaired_why": (
                "Cancer and Leo have one owner each. The book's list of five "
                "pairs says so by omission."
            ),
            "occupancy_undefined": EKAADHIPATYA_OCCUPANCY_UNDEFINED,
            "tie_is_uncovered": EKAADHIPATYA_TIE_IS_UNCOVERED,
            "tie_reading": EKAADHIPATYA_TIE_READING,
            "rules_all_exercised": list(EKAADHIPATYA_RULES_ALL_EXERCISED),
            "rules_all_exercised_note": (
                "Example 41 works rule (1) and Example 42 the other five "
                "branches, so the book works every rule it states."
            ),
        },
        "example_41": {
            "question": EXAMPLE_41,
            "answer": list(EXAMPLE_41_ANSWER),
            "note": (
                "Example 41's answer is Example 40's answer: rule (1) fires "
                "on all five pairs and nothing moves."
            ),
        },
        "example_42": {
            "question": EXAMPLE_42,
            "cases": [
                {"label": label, "before": list(before),
                 "occupied": list(occupied), "after": list(after),
                 "rule": rule, "text": text}
                for label, before, occupied, after, rule, text
                in EXAMPLE_42_CASES
            ],
        },
        "trikona_sodhana": {
            "means": TRIKONA_SODHANA_MEANS,
            "rule": TRIKONA_SODHANA_RULE,
            "rules": list(TRIKONA_SODHANA_RULES),
            "footnote_44": TRIKONA_SODHANA_FOOTNOTE_44,
            "disputed_case": TRIKONA_SODHANA_DISPUTED_CASE,
            "disputed_case_note": (
                "The reading PVR rejects differs from Parasara's on exactly "
                "24 of the 729 possible trine triples, all of them with two "
                "zeros and a non-zero third. Everywhere else the two agree."
            ),
            "only_rule_three_is_implemented": ONLY_RULE_THREE,
            "trine_sets": [
                {"element": element, "name": f"{adjective} trines"}
                for element, adjective in TRINE_SET_NAMES.items()
            ],
        },
        "example_40": {
            "question": EXAMPLE_40,
            "owner": EXAMPLE_40_OWNER,
            "chart": EXAMPLE_40_CHART,
            "answer": list(EXAMPLE_40_ANSWER),
            "worked": [
                {"trines": f"{element} trines", "signs": list(names),
                 "before": list(before), "after": list(after), "rule": rule}
                for element, names, before, after, rule in EXAMPLE_40_WORKED
            ],
            "worked_note": (
                "The example works the fiery and watery sets longhand and "
                "leaves the earthy and airy ones to the reader. All four are "
                "computed and tested."
            ),
        },
    }


__all__ = ["AshtakavargaError", "InputError", "ekaadhipatya", "pinda",
           "rules", "trikona"]
