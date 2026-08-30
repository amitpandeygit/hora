"""Section 12.7 — Sodhya Pindas, service layer."""
from __future__ import annotations

from hora.charts.ashtakavarga import (
    AshtakavargaError,
    bhinnashtakavarga,
    trikona_sodhana,
)
from hora.core.const import (
    ELEMENT_NAMES,
    EXAMPLE_40,
    EXAMPLE_40_ANSWER,
    EXAMPLE_40_CHART,
    EXAMPLE_40_OWNER,
    EXAMPLE_40_WORKED,
    RASI_NAMES,
    SOAV_IS_A_REDUCED_BAV,
    SOAV_MEANS,
    SODHYA_PINDA_NOT_YET_DEFINED,
    SODHYA_PINDAS_INTRO,
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


def rules() -> dict:
    """Section 12.7's framing, its three rules, and Example 40."""
    return {
        "intro": SODHYA_PINDAS_INTRO,
        "soav_means": SOAV_MEANS,
        "soav_is_a_reduced_bav": SOAV_IS_A_REDUCED_BAV,
        "pinda_not_yet_defined": SODHYA_PINDA_NOT_YET_DEFINED,
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


__all__ = ["AshtakavargaError", "InputError", "rules", "trikona"]
