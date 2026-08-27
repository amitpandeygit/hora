"""Planetary yoga endpoints — book chapter 11 onward.

Distinct from `yoga_service`, which serves §1.3.9's nithya yoga and shares
only the word.

The contract is exhaustiveness: :func:`chart` evaluates **every** registered
yoga and returns a verdict for each, present or absent, with the reason either
way. Nothing is filtered on the way out, so "not in the response" never has to
be interpreted.
"""
from __future__ import annotations

from hora.charts.planetary_yogas import (
    YOGA_REGISTRY,
    YogaError,
    YogaInput,
    evaluate,
    evaluate_one,
    groups,
)
from hora.charts.planetary_yogas.registry import describe
from hora.core import validate
from hora.core.const import (
    AAKRITI_BASIS,
    AAKRITI_MEANS,
    AAKRITI_NAME_VARIANTS,
    AAKRITI_NODES_NOTE,
    AAKRITI_ORDER_DIFFERS,
    AAKRITI_READING_RULE,
    AASRAYA_BASIS,
    ADHI_EXAMPLE_CONTRADICTS_RULE,
    BUDHA_AADITYA_SPELLING_VARIANTS,
    BUDHA_AADITYA_TERMS,
    BUDHA_AADITYA_TIMING_CHART,
    BUDHA_AADITYA_TIMING_PERIODS,
    BUDHA_AADITYA_TIMING_SIGN,
    BUDHA_AADITYA_TIMING_TEXT,
    CHANDRA_ASPECT_BY_BIRTH_TIME,
    CHANDRA_BENEFICS_IN_UPACHAYA_GRADE,
    CHANDRA_GUIDELINE_1,
    CHANDRA_GUIDELINE_2,
    CHANDRA_GUIDELINE_2_RESPECTIVELY_NOTE,
    CHANDRA_GUIDELINE_3,
    CHANDRA_MOON_FROM_SUN_GRADE,
    CHANDRA_YOGA_INTRO,
    COMBUSTION_WEAKENS_YOGA,
    ELEMENT_RULER,
    GRAHA_NAMES,
    HAMSA_MEANS,
    HAMSA_MISNAMED_IN_ITS_DEFINITION,
    HOUSE_CATEGORIES,
    KARTARI_DEFINITION,
    KARTARI_EFFECT,
    KARTARI_HOUSES,
    KARTARI_IS_GENERAL,
    KARTARI_MEANS,
    KEMADRUMA_EFFORT_NOTE,
    KEMADRUMA_KILLS_OTHER_YOGAS,
    MAALAVYA_SPELLING_VARIANTS,
    MAHAPURUSHA_ELEMENT_ROLE,
    MAHAPURUSHA_ELEMENT_RULERS_SENTENCE,
    MAHAPURUSHA_FOOTNOTES_UNREAD,
    MAHAPURUSHA_INTRO,
    MAHAPURUSHA_REFERENCE_RULE,
    MAHAPURUSHA_TERMS,
    NAABHASA_CLASSIFICATION,
    NAABHASA_INTRO,
    NAABHASA_NOT_YET_DEFINED,
    NAABHASA_TIMING_RULE,
    PANAPHARA_SPELLING_VARIANTS,
    PANCHA_BHOOTA_NAMES,
    PLANET_ELEMENT_ADJECTIVES,
    PLANET_ELEMENT_TATTVAS,
    POPULAR_YOGA_COUNT,
    POPULAR_YOGA_FULLNESS_RULE,
    POPULAR_YOGA_INTRO,
    POPULAR_YOGAS,
    RASI_NAMES,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
    SANKHYA_BASIS,
    SANKHYA_EXCLUDES_NODES,
    SANKHYA_IS_A_FALLBACK,
    SANKHYA_MEANS,
    SARPA_IS_VERY_BAD,
    SASA_MEANS,
    STRENGTH_NOT_ASSESSED,
    TATTVA_GLOSS_IN_3_2_8,
    TATTVA_GLOSS_IN_11_4,
    UPACHAYA,
    WEAKENED_YOGA_IS_NOT_APPLICABLE,
    Graha,
)

InputError = validate.InputError

__all__ = ["InputError", "YogaError", "catalogue", "chart", "guidelines",
           "one", "rules"]

#: Charts a caller may name. §11.2 singles out D-9 and D-10; the rest are
#: accepted because the yoga arithmetic is chart-agnostic.
KNOWN_CHARTS = ("D1", "D9", "D10", "D2", "D3", "D4", "D7", "D12", "D16",
                "D20", "D24", "D27", "D30", "D40", "D45", "D60")


def _verdict(verdict, data: YogaInput) -> dict:
    spec = YOGA_REGISTRY[verdict.key]
    return {
        "key": verdict.key,
        "name": verdict.name,
        "aliases": list(spec.aliases),
        "section": spec.section,
        "group": spec.group,
        "definition": spec.definition,
        "present": verdict.present,
        "reason": verdict.reason,
        "participants": [
            {"graha": g, "graha_name": GRAHA_NAMES[g],
             "sign": data.rasis[g], "sign_name": RASI_NAMES[data.rasis[g]],
             "house_from_sun": verdict.houses.get(g)}
            for g in verdict.participants
        ],
        "qualifiers": list(verdict.qualifiers),
        "weakened": verdict.weakened,
        "implies": list(spec.implies),
    }


def _input(rasis: dict[int, int], chart_code: str, include_nodes: bool,
           positions=None, lagna_rasi: int | None = None,
           paksha: int | None = None) -> YogaInput:
    if chart_code not in KNOWN_CHARTS:
        raise InputError(
            f"unknown chart {chart_code!r}; expected one of "
            f"{', '.join(KNOWN_CHARTS)}"
        )
    if lagna_rasi is not None:
        validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    if paksha is not None:
        validate.in_range("paksha", int(paksha), 0, 1)
    return YogaInput(
        rasis={int(g): int(s) for g, s in rasis.items()},
        chart=chart_code, include_nodes=include_nodes, positions=positions,
        lagna_rasi=None if lagna_rasi is None else int(lagna_rasi),
        paksha=None if paksha is None else int(paksha),
    )


def chart(
    rasis: dict[int, int],
    *,
    chart_code: str = "D1",
    include_nodes: bool = False,
    group: str | None = None,
    lagna_rasi: int | None = None,
    paksha: int | None = None,
) -> dict:
    """Every registered yoga on one chart, present or absent.

    `lagna_rasi` and `paksha` are optional because most yogas do not need
    them. A yoga that does and lacks it says so in its own reason rather than
    the whole call failing — §11.3.4 needs a lagna, §11.3.6 a paksha.
    """
    data = _input(rasis, chart_code, include_nodes, lagna_rasi=lagna_rasi,
                  paksha=paksha)
    if group is not None and group not in groups():
        raise InputError(
            f"unknown group {group!r}; expected one of {', '.join(groups())}")
    verdicts = evaluate(data, group=group)
    # §11.3.4: Kemadruma "kills the results of other good yogas in the chart,
    # especially Chandra yogas". It kills the *results*, not the yoga, so it
    # is applied as a qualifier and never flips another verdict's `present`.
    kemadruma = next(
        (v for v in verdicts if v.key == "kemadruma" and v.present), None)
    killed = {v.key for v in verdicts
              if kemadruma and v.present and v.key != "kemadruma"}
    return {
        "chart": chart_code,
        "group": group,
        "include_nodes": include_nodes,
        "lagna_rasi": data.lagna_rasi,
        "paksha": data.paksha,
        "inputs_missing": [
            name for name, value in (("lagna_rasi", data.lagna_rasi),
                                     ("paksha", data.paksha))
            if value is None
        ],
        "grahas_considered": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
            for g in data.considered()
        ],
        "evaluated": len(verdicts),
        "present": [v.key for v in verdicts if v.present],
        "yogas": [
            {**_verdict(v, data),
             "qualifiers": (
                 [*v.qualifiers, KEMADRUMA_KILLS_OTHER_YOGAS]
                 if v.key in killed else list(v.qualifiers))}
            for v in verdicts
        ],
        "kemadruma_present": bool(kemadruma),
        "results_killed_by_kemadruma": sorted(killed),
        # A caller cannot tell from signs alone whether Mercury is combust, so
        # the response says which qualifiers could be judged at all.
        "qualifiers_available": [],
        "qualifiers_unavailable": ["combustion"],
        "chart_note": (
            RAVI_YOGA_FREQUENCY_NOTE if chart_code == "D1" else None
        ),
    }


def guidelines(
    rasis: dict[int, int], *, paksha: int | None = None,
) -> dict:
    """§11.3's three General Guidelines.

    **Not yogas.** Each is a graded reading: guideline 1 always yields one of
    three verdicts because its three categories partition the twelve houses,
    and guideline 3 grades by a count. They are computed and returned apart
    from the registry so nothing reads them as combinations.
    """
    data = YogaInput(rasis={int(g): int(s) for g, s in rasis.items()},
                     paksha=paksha)
    sun = data.sign_of(Graha.SUN)
    moon = data.sign_of(Graha.MOON)

    first: dict = {"text": CHANDRA_GUIDELINE_1, "verdict": None,
                   "category": None, "house": None}
    if sun is None or moon is None:
        first["reason"] = "guideline 1 needs both Sun and Moon"
    else:
        house = (moon - sun) % 12 + 1
        category = next(
            name for name in ("kendra", "panaphara", "apoklima")
            if house in HOUSE_CATEGORIES[name]["houses"]
        )
        first.update(
            house=house, category=category,
            verdict=CHANDRA_MOON_FROM_SUN_GRADE[category],
            reason=(f"Moon is in the {house}th from Sun, "
                    f"{'a' if category != 'apoklima' else 'an'} {category}"),
        )

    benefics, undecidable = data.benefics()
    third: dict = {"text": CHANDRA_GUIDELINE_3, "verdict": None}
    if moon is None:
        third["reason"] = "guideline 3 counts upachayas from Moon"
    else:
        upachaya = {(moon + h - 1) % 12 for h in UPACHAYA}
        inside = tuple(g for g in benefics
                       if int(g) != int(Graha.MOON) and data.rasis[g] in upachaya)
        placed = tuple(g for g in benefics if int(g) != int(Graha.MOON))
        count = len(inside)
        # "If **all** the natural benefics occupy upachayas" outranks the
        # counts: three benefics all in upachayas is "great wealth", not the
        # "medium" the count of two would give.
        verdict: str | None
        if count and count == len(placed):
            verdict = CHANDRA_BENEFICS_IN_UPACHAYA_GRADE["all"]
        else:
            verdict = CHANDRA_BENEFICS_IN_UPACHAYA_GRADE.get(count)
        third.update(
            verdict=verdict,
            benefics_in_upachaya=[
                {"graha": int(g), "graha_name": GRAHA_NAMES[g]} for g in inside],
            benefics_placed=[
                {"graha": int(g), "graha_name": GRAHA_NAMES[g]} for g in placed],
            undecidable=[
                {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
                for g in undecidable if int(g) != int(Graha.MOON)],
            reason=(f"{count} of {len(placed)} placed natural benefics occupy "
                    f"an upachaya from Moon"),
        )

    return {
        "guideline_1": first,
        "guideline_2": {
            "text": CHANDRA_GUIDELINE_2,
            "aspect_table": [
                {"graha": graha, "birth_time": when, "effect": effect}
                for (graha, when), effect in CHANDRA_ASPECT_BY_BIRTH_TIME.items()
            ],
            "respectively_note": CHANDRA_GUIDELINE_2_RESPECTIVELY_NOTE,
            "verdict": None,
            "reason": (
                "guideline 2 needs the Moon's navamsa, its lord's compound "
                "relationship to the Moon, whether the birth was by day, and "
                "Jupiter's and Venus's aspects on the Moon. It is not computed "
                "here — see docs/open-items.md OI-76."
            ),
        },
        "guideline_3": third,
    }


def one(key: str, rasis: dict[int, int], *, chart_code: str = "D1",
        include_nodes: bool = False) -> dict:
    data = _input(rasis, chart_code, include_nodes)
    return _verdict(evaluate_one(key, data), data)


def catalogue(group: str | None = None) -> dict:
    """Every yoga the engine knows, whether or not any chart is supplied."""
    if group is not None and group not in groups():
        raise InputError(
            f"unknown group {group!r}; expected one of {', '.join(groups())}")
    specs = [
        describe(spec) for spec in YOGA_REGISTRY.values()
        if group is None or spec.group == group
    ]
    return {"groups": groups(), "count": len(specs), "yogas": specs}


def rules() -> dict:
    """Chapter 11's framing, and what the engine does not decide."""
    return {
        "ravi_intro": RAVI_YOGA_INTRO,
        "chandra_intro": CHANDRA_YOGA_INTRO,
        "mahapurusha_terms": dict(MAHAPURUSHA_TERMS),
        "mahapurusha_intro": MAHAPURUSHA_INTRO,
        "pancha_bhoota_names": dict(PANCHA_BHOOTA_NAMES),
        "mahapurusha_element_rulers": MAHAPURUSHA_ELEMENT_RULERS_SENTENCE,
        "mahapurusha_element_role": MAHAPURUSHA_ELEMENT_ROLE,
        "mahapurusha_reference_rule": MAHAPURUSHA_REFERENCE_RULE,
        "mahapurusha_elements": [
            {"tattva": PLANET_ELEMENT_TATTVAS[index],
             "gloss_in_11_4": f"{PLANET_ELEMENT_ADJECTIVES[index]} {TATTVA_GLOSS_IN_11_4}",
             "gloss_in_3_2_8": f"{PLANET_ELEMENT_ADJECTIVES[index]} {TATTVA_GLOSS_IN_3_2_8}",
             "graha": int(ELEMENT_RULER[index]),
             "graha_name": GRAHA_NAMES[ELEMENT_RULER[index]]}
            for index in range(5)
        ],
        "maalavya_spelling_variants": list(MAALAVYA_SPELLING_VARIANTS),
        "hamsa_misnamed_in_its_definition": HAMSA_MISNAMED_IN_ITS_DEFINITION,
        "hamsa_name_note": (
            "Section 11.4.5's Definition calls the yoga "
            f"\u201c{HAMSA_MISNAMED_IN_ITS_DEFINITION}\u201d, which is Mars's "
            "yoga from section 11.4.1. The heading reads \u201cHamsa Yoga\u201d "
            "and is followed \u2014 see docs/book-deviations.md D-30."
        ),
        "footnotes_unread": list(MAHAPURUSHA_FOOTNOTES_UNREAD),
        "sasa_means": SASA_MEANS,
        "hamsa_means": HAMSA_MEANS,
        "naabhasa_intro": NAABHASA_INTRO,
        "naabhasa_timing_rule": NAABHASA_TIMING_RULE,
        "aasraya_basis": AASRAYA_BASIS,
        "sarpa_is_very_bad": SARPA_IS_VERY_BAD,
        "naabhasa_classification": [
            {"family": family, "count": entry["count"],
             "names": list(entry["names"]), "section": entry["section"],
             "means": entry["means"], "basis": entry["basis"]}
            for family, entry in NAABHASA_CLASSIFICATION.items()
        ],
        # Twenty-seven of the thirty-two are named by §11.5 and defined
        # nowhere we have read. Listed so the gap shows in the API rather than
        # looking like an absence.
        "naabhasa_not_yet_defined": list(NAABHASA_NOT_YET_DEFINED),
        "aakriti_means": AAKRITI_MEANS,
        "aakriti_basis": AAKRITI_BASIS,
        "aakriti_nodes_note": AAKRITI_NODES_NOTE,
        "aakriti_reading_rule": AAKRITI_READING_RULE,
        "aakriti_name_variants": {
            key: list(values) for key, values in AAKRITI_NAME_VARIANTS.items()
        },
        "aakriti_order_differs": AAKRITI_ORDER_DIFFERS,
        "sankhya_means": SANKHYA_MEANS,
        "sankhya_basis": SANKHYA_BASIS,
        "sankhya_excludes_nodes": SANKHYA_EXCLUDES_NODES,
        "sankhya_is_a_fallback": SANKHYA_IS_A_FALLBACK,
        "weakened_yoga_is_not_applicable": WEAKENED_YOGA_IS_NOT_APPLICABLE,
        "sankhya_unreachable": ["gola", "yuga"],
        "sankhya_unreachable_note": (
            "Taken as stated, section 11.5.4's fallback rule makes Gola and "
            "Yuga permanently absent: one or two distinct signs always fit "
            "inside a seven-sign window, and section 11.5.3's run yogas cover "
            "all twelve windows, so one of them always applies first. Both are "
            "still defined and evaluated, and their verdicts name what "
            "superseded them. See docs/open-items.md OI-79."
        ),
        "naabhasa_gap_note": (
            "Section 11.5 classifies 32 Naabhasa yogas and sections 11.5.1 "
            "to 11.5.4 define every one. Nothing is pending. They are listed here rather "
            "than registered, so that a yoga the engine cannot detect never "
            "appears among the verdicts where its absence would read as a "
            "finding."
        ),
        "kemadruma_kills_other_yogas": KEMADRUMA_KILLS_OTHER_YOGAS,
        "kemadruma_effort_note": KEMADRUMA_EFFORT_NOTE,
        "kemadruma_is_a_qualifier_not_a_veto": (
            "Section 11.3.4 says Kemadruma kills the *results* of other good "
            "yogas, not the yogas themselves. A yoga forming beside it is "
            "reported present with a qualifier, never suppressed."
        ),
        "adhi_example_note": ADHI_EXAMPLE_CONTRADICTS_RULE,
        "panaphara_spelling_variants": list(PANAPHARA_SPELLING_VARIANTS),
        "frequency_note": RAVI_YOGA_FREQUENCY_NOTE,
        "preferred_charts": list(RAVI_YOGA_PREFERRED_CHARTS),
        "budha_aaditya_terms": dict(BUDHA_AADITYA_TERMS),
        "budha_aaditya_spelling_variants": list(BUDHA_AADITYA_SPELLING_VARIANTS),
        "combustion_note": COMBUSTION_WEAKENS_YOGA,
        "combustion_is_a_qualifier_not_a_veto": (
            "Section 11.2.4 says a yoga formed by a combust planet loses "
            "“some of their power to do good”, not all of it. A combust "
            "yoga is therefore reported as present with a qualifier, never "
            "suppressed."
        ),
        "timing_example": {
            "chart": BUDHA_AADITYA_TIMING_CHART,
            "sign": BUDHA_AADITYA_TIMING_SIGN,
            "sign_name": RASI_NAMES[BUDHA_AADITYA_TIMING_SIGN],
            "text": BUDHA_AADITYA_TIMING_TEXT,
            "periods": [
                {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
                for g in BUDHA_AADITYA_TIMING_PERIODS
            ],
        },
        "node_note": (
            "Three of the four Ravi yogas turn on “a planet other than "
            "Moon”. Chapter 11 never says whether Rahu and Ketu count as "
            "“a planet”, so it is a per-call choice and the nodes are "
            "excluded by default. See docs/open-items.md OI-73."
        ),
        "results_note": (
            "The results each yoga gives are PVR's own prose and are withheld "
            "from this response under the licence gate of OI-12."
        ),
        # 11.6 --------------------------------------------------------------
        "popular_fullness_rule": POPULAR_YOGA_FULLNESS_RULE,
        "popular_strength_note": STRENGTH_NOT_ASSESSED,
        "popular_yogas_needing_a_named_lord": {
            entry["key"]: list(entry["strength"])
            for entry in POPULAR_YOGAS if entry.get("strength")
        },
        "popular_intro": POPULAR_YOGA_INTRO,
        "popular_count": POPULAR_YOGA_COUNT,
        "kartari_means": KARTARI_MEANS,
        "kartari_houses": list(KARTARI_HOUSES),
        "kartari_definition": KARTARI_DEFINITION,
        "kartari_effect": KARTARI_EFFECT,
        "kartari_is_general": KARTARI_IS_GENERAL,
        "kartari_note": (
            "Both flanks must carry the same nature — footnote 31 reads \u201cthe "
            "2nd and 12th\u201d — so a benefic on one side and a malefic on the "
            "other is neither subha nor paapa kartari."
        ),
        "sun_excluded_note": (
            "The Sun cannot form a yoga about what accompanies him, so he is "
            "excluded from his own houses alongside the Moon."
        ),
    }
