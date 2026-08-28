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
from hora.content.store import serving_unconfirmed_allowed
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
    ADHI_HOUSES_FROM_MOON,
    ADVANCED_RAAJA_INTRO,
    ADVANCED_RAAJA_YOGA_COUNT,
    ADVANCED_RAAJA_YOGAS,
    AMSA_SPELLINGS_IN_11_7_2,
    ARUDHA_EFFECTIVENESS_RULE,
    BRAHMA_VARIATION,
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
    CHART_10_BIRTH_FOOTNOTE,
    CHART_10_OLD_CALENDAR_DATE,
    CHART_10_TIME_IS_LMT,
    COMBUSTION_WEAKENS_YOGA,
    DHARMA_KARMADHIPATI_DEFINITION,
    DHARMA_KARMADHIPATI_REASON,
    DHARMA_KARMADHIPATI_RESULTS_TRUNCATED,
    DHARMA_STHANA,
    DUSTHANA,
    DUSTHANA_LORD_IN_OWN_HOUSE,
    ELEMENT_RULER,
    FUNCTIONAL_MALEFIC_DATA_POINTS,
    FUNCTIONAL_MALEFIC_NOT_DEFINED,
    GRAHA_NAMES,
    HAMSA_MEANS,
    HAMSA_MISNAMED_IN_ITS_DEFINITION,
    HOUSE_CATEGORIES,
    KALPADRUMA_EXAMPLE_CHAIN,
    KALPADRUMA_EXAMPLE_CONCLUSION,
    KALPADRUMA_EXAMPLE_NAVAMSA_LAGNA_CLAIM,
    KALPADRUMA_EXAMPLE_WALKTHROUGH,
    KALPADRUMA_RESULT_WORD_SANSKRIT,
    KALPADRUMA_RESULT_WORDS,
    KALPADRUMA_RESULTS_FOOTNOTE,
    KARMA_STHANA,
    KARTARI_DEFINITION,
    KARTARI_EFFECT,
    KARTARI_HOUSES,
    KARTARI_IS_GENERAL,
    KARTARI_MEANS,
    KEMADRUMA_EFFORT_NOTE,
    KEMADRUMA_KILLS_OTHER_YOGAS,
    LAGNA_IS_BOTH_QUADRANT_AND_TRINE,
    LAGNAADHI_GLOSS,
    LAGNAADHI_HOUSES,
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
    PARASARA_DASA_VARGA_RULE,
    PARIVARTANA_FOOTNOTE,
    PARIVARTANA_SANSKRIT,
    PLANET_ELEMENT_ADJECTIVES,
    PLANET_ELEMENT_TATTVAS,
    POPULAR_YOGA_CONTINUED_COUNT,
    POPULAR_YOGA_COUNT,
    POPULAR_YOGA_FULLNESS_RULE,
    POPULAR_YOGA_INTRO,
    POPULAR_YOGA_TOTAL,
    POPULAR_YOGAS_ALL,
    RAAJA_AMSA_COUNT_NOT_DISCUSSED,
    RAAJA_AMSA_DIVINE_COUNTS,
    RAAJA_AMSA_DIVINE_PERSONS,
    RAAJA_AMSA_DIVINE_RULE,
    RAAJA_AMSA_RESULTS,
    RAAJA_ASSOCIATION_RULE,
    RAAJA_ASSOCIATIONS,
    RAAJA_BASIC_PREMISE,
    RAAJA_BLEMISH_RULE,
    RAAJA_CLOSE_ORB_DEGREES,
    RAAJA_CLOSE_ORB_IS_APPROXIMATE,
    RAAJA_FINAL_JUDGMENT,
    RAAJA_MAGNITUDE_FACTORS,
    RAAJA_MAGNITUDE_INTRO,
    RAAJA_MEANS,
    RAAJA_ORB_EXAMPLE,
    RAAJA_ORB_FOOTNOTE,
    RAAJA_SAMBANDHA_ARE_COMMON,
    RAAJA_SAMBANDHA_COUNT,
    RAAJA_SAMBANDHA_INTRO,
    RAAJA_SAMBANDHA_MAGNITUDE_RULE,
    RAAJA_SAMBANDHA_YOGAS,
    RAAJA_YOGA_COUNT,
    RAAJA_YOGA_INTRO,
    RASI_NAMES,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
    SAMBANDHA_KARAKA_NAMES,
    SAMBANDHA_MEANS,
    SANKHYA_BASIS,
    SANKHYA_EXCLUDES_NODES,
    SANKHYA_IS_A_FALLBACK,
    SANKHYA_MEANS,
    SARPA_IS_VERY_BAD,
    SASA_MEANS,
    SHADVARGA_NAMED_IN_11_7_3,
    SIMHAASANAAMSA_EMPERORS,
    SIMHAASANAAMSA_FOOTNOTE_UNREAD,
    SIMHAASANAAMSA_RULE,
    STRENGTH_NOT_ASSESSED,
    TATTVA_GLOSS_IN_3_2_8,
    TATTVA_GLOSS_IN_11_4,
    TRIK_STHANA_NAMES,
    TRIMURTHI_COMBINED_NAME,
    TRIMURTHI_NOTE,
    TRIMURTHI_YOGAS,
    TRIVARGA_NAMED_IN_11_7_3,
    UPACHAYA,
    VARGOTTAMAAMSA_DEFINITION,
    VARGOTTAMAAMSA_SPELLINGS,
    VIPAREETA_DEFINITION,
    VIPAREETA_IDEAL_CASE,
    VIPAREETA_IDEAL_HOUSES,
    VIPAREETA_MEANS,
    VIPAREETA_REASON,
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
           paksha: int | None = None, lagna_longitude: float | None = None,
           special_lagnas: dict[str, float] | None = None) -> YogaInput:
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
        lagna_longitude=(None if lagna_longitude is None
                         else float(lagna_longitude) % 360.0),
        special_lagnas=(None if special_lagnas is None else
                        {str(k): float(v) % 360.0
                         for k, v in special_lagnas.items()}),
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
            for entry in POPULAR_YOGAS_ALL if entry.get("strength")
        },
        "popular_intro": POPULAR_YOGA_INTRO,
        # 11.6's only worked example: Chart 9, Chatrapati Shivaji.
        "kalpadruma_example": {
            "chart": "Chart 9",
            "native": "Chatrapati Shivaji",
            "walkthrough": KALPADRUMA_EXAMPLE_WALKTHROUGH,
            "conclusion": KALPADRUMA_EXAMPLE_CONCLUSION,
            "chain": list(KALPADRUMA_EXAMPLE_CHAIN),
            "navamsa_lagna_claim": KALPADRUMA_EXAMPLE_NAVAMSA_LAGNA_CLAIM,
            "navamsa_lagna_note": (
                "Chart 9's own navamsa diagram puts Venus in Gemini and the "
                "navamsa lagna in Sagittarius, so she is in the 7th from it, "
                "not in it. Our D-9 reproduces all ten of that diagram's "
                "placements. Nothing in the yoga turns on the claim. See "
                "docs/book-deviations.md D-34."
            ),
        },
        # Footnote 34 quotes three words out of Kalpadruma's results, which
        # is PVR's own prose and carries OI-12's gate like the rest of it.
        "kalpadruma_results_footnote": (
            KALPADRUMA_RESULTS_FOOTNOTE if serving_unconfirmed_allowed() else None
        ),
        "kalpadruma_result_words": (
            list(KALPADRUMA_RESULT_WORDS) if serving_unconfirmed_allowed() else []
        ),
        "kalpadruma_result_word_sanskrit": (
            KALPADRUMA_RESULT_WORD_SANSKRIT if serving_unconfirmed_allowed() else None
        ),
        "popular_count": POPULAR_YOGA_TOTAL,
        "popular_count_before_the_example": POPULAR_YOGA_COUNT,
        "popular_count_after_the_example": POPULAR_YOGA_CONTINUED_COUNT,
        "trimurthi_note": TRIMURTHI_NOTE,
        "trimurthi_yogas": list(TRIMURTHI_YOGAS),
        "trimurthi_combined_name": TRIMURTHI_COMBINED_NAME,
        "brahma_variation": BRAHMA_VARIATION,
        "brahma_variation_note": (
            "NOTE (2) gives a second, unrelated definition of Brahma yoga. "
            "The first one \u2014 benefics in the 4th, 10th and 11th from lagna "
            "lord \u2014 is the one detected; the variation is carried here so a "
            "caller can see it was not silently dropped."
        ),
        "parivartana_footnote": PARIVARTANA_FOOTNOTE,
        "parivartana_sanskrit": PARIVARTANA_SANSKRIT,
        "parivartana_yogas": ["devendra", "indra", "chapa"],
        "lagnaadhi_gloss": LAGNAADHI_GLOSS,
        "lagnaadhi_note": (
            "Section 11.6 says Lagnaadhi yoga \u201cmeans Adhi Yoga from lagna\u201d, "
            "but its definition takes only the 7th and 8th, where section "
            "11.3.6\u2019s Adhi takes the 6th, 7th and 8th from Moon. The "
            "definition is followed. See docs/book-deviations.md D-35."
        ),
        "lagnaadhi_houses": list(LAGNAADHI_HOUSES),
        "adhi_houses_from_moon": list(ADHI_HOUSES_FROM_MOON),
        "dusthana_lord_in_own_house": list(DUSTHANA_LORD_IN_OWN_HOUSE),
        "deep_exaltation_note": (
            "Jaya and Vidyut require a planet in \u201cdeep exaltation\u201d. The book "
            "gives the exact exaltation degree but no tolerance around it, so "
            "neither yoga is ever reported present: when the planet is not in "
            "his exaltation sign the verdict is a definite absence, and when "
            "he is, the verdict names his distance from the exact degree and "
            "says the depth is undecided. See docs/open-items.md OI-83."
        ),
        "vasumati_reference_note": (
            "Vasumati says only \u201cbenefics occupy upachayas\u201d, naming no "
            "reference and no count. Houses are counted from lagna, as "
            "everywhere else in section 11.6, and one benefic in an upachaya "
            "is enough; a verdict says how many benefics sit outside them so "
            "a stricter reading stays available. See docs/open-items.md OI-84."
        ),
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
        # 11.7 --------------------------------------------------------------
        "raaja_intro": RAAJA_YOGA_INTRO,
        "raaja_count": RAAJA_YOGA_COUNT,
        "raaja_definitions": {
            "raaja_basic": RAAJA_ASSOCIATION_RULE,
            "dharma_karmadhipati": DHARMA_KARMADHIPATI_DEFINITION,
            "vipareeta_raaja": VIPAREETA_DEFINITION,
        },
        # PVR's own prose, so it carries OI-12's gate. The sentence is cut
        # off in the book \u2014 see docs/open-items.md OI-87.
        "dharma_karmadhipati_results": (
            DHARMA_KARMADHIPATI_RESULTS_TRUNCATED
            if serving_unconfirmed_allowed() else None
        ),
        "raaja_means": RAAJA_MEANS,
        "raaja_basic_premise": RAAJA_BASIC_PREMISE,
        "raaja_association_rule": RAAJA_ASSOCIATION_RULE,
        "raaja_associations": [
            {"key": entry["key"], "text": entry["text"]}
            for entry in RAAJA_ASSOCIATIONS
        ],
        "lagna_is_both_quadrant_and_trine": LAGNA_IS_BOTH_QUADRANT_AND_TRINE,
        "raaja_lagna_note": (
            "\u201cLagna can be taken as a quadrant or a trine here. It is "
            "both.\u201d So the lagna lord is counted on both sides of every "
            "pairing."
        ),
        "mutual_drishti_is_both_ways_note": (
            "Association (2) reads \u201caspect **each other** with graha "
            "drishti\u201d. Graha drishti is not symmetric \u2014 Saturn\u2019s 3rd and "
            "10th, Mars\u2019s 4th and 8th and Jupiter\u2019s 5th and 9th are "
            "one-sided \u2014 so one planet aspecting the other is not an "
            "association here."
        ),
        "dharma_sthana": DHARMA_STHANA,
        "karma_sthana": KARMA_STHANA,
        "dharma_karmadhipati_reason": DHARMA_KARMADHIPATI_REASON,
        "trik_sthana_names": list(TRIK_STHANA_NAMES),
        "dusthanas": list(DUSTHANA),
        "vipareeta_means": VIPAREETA_MEANS,
        "vipareeta_reason": VIPAREETA_REASON,
        "vipareeta_ideal_case": VIPAREETA_IDEAL_CASE,
        "vipareeta_ideal_houses": list(VIPAREETA_IDEAL_HOUSES),
        "vipareeta_ideal_note": (
            "The ideal case names the 3rd and the 11th, which are not "
            "dusthanas. Three dusthana lords heaped there occupy no dusthana "
            "but do conjoin one another, which is why the second clause of "
            "the definition \u2014 \u201cor conjoin dusthanas\u201d \u2014 is tested "
            "alongside the first. See docs/open-items.md OI-86."
        ),
        "yogakaraka_note": (
            "For six lagnas \u2014 Taurus, Cancer, Leo, Libra, Capricorn and "
            "Aquarius \u2014 one planet lords a quadrant and a trine that are "
            "different houses. Section 11.7.1 asks for an association between "
            "two planets and says nothing about one planet holding both "
            "sides, so the engine reports the fact as a qualifier and draws "
            "no conclusion. See docs/open-items.md OI-85."
        ),
        # 11.7.3 ------------------------------------------------------------
        "advanced_raaja_intro": ADVANCED_RAAJA_INTRO,
        "advanced_raaja_count": ADVANCED_RAAJA_YOGA_COUNT,
        "advanced_raaja_numbering": {
            entry["key"]: entry["number"] for entry in ADVANCED_RAAJA_YOGAS
        },
        "shadvarga_named_in_11_7_3": list(SHADVARGA_NAMED_IN_11_7_3),
        "trivarga_named_in_11_7_3": list(TRIVARGA_NAMED_IN_11_7_3),
        "arudha_effectiveness_rule": ARUDHA_EFFECTIVENESS_RULE,
        "arudha_effectiveness_note": (
            "Section 11.7.3 (18) is not a combination \u2014 it says how "
            "effective the chart\u2019s Raaja yogas are. It is returned by "
            "/v1/planetary-yoga/raaja-magnitude beside the yogas and never "
            "among them."
        ),
        "advanced_raaja_input_note": (
            "These seventeen reach past signs \u2014 into chara karakas, the "
            "navamsa, the divisional lagnas, HL and GL. A chart that cannot "
            "decide one of them gets a verdict whose reason begins \u201cthis "
            "yoga cannot be decided\u201d, never a bare absence. Supply "
            "longitudes for the karaka and varga yogas, a lagna longitude for "
            "yogas 7 and 9, and HL and GL for yogas 6 and 8."
        ),
        "raaja_orb_footnote": RAAJA_ORB_FOOTNOTE,
        "worked_charts": [
            {"chart": "Chart 9", "native": "Chatrapati Shivaji",
             "section": "11.6", "shows": "Kalpadruma yoga",
             "birth_footnote": None, "recomputable": False,
             "note": ("Given as a Hindu calendar date and a time measured "
                      "from sunrise, so it is transcribed, not recomputed.")},
            {"chart": "Chart 10", "native": "Emperor Akbar",
             "section": "11.7.2", "shows": "the magnitude of a Raaja yoga",
             "birth_footnote": CHART_10_BIRTH_FOOTNOTE,
             "recomputable": True,
             "old_calendar_date": CHART_10_OLD_CALENDAR_DATE,
             "time_is_lmt": CHART_10_TIME_IS_LMT,
             "note": ("Footnote 39 settles the calendar: 24 November 1542 in "
                      "the old calendar is 4 December 1542 in the new, ten "
                      "days apart, and the printed date is the new one.")},
        ],
        # 11.8 ----------------------------------------------------------------
        "raaja_sambandha_intro": RAAJA_SAMBANDHA_INTRO,
        "raaja_sambandha_count": RAAJA_SAMBANDHA_COUNT,
        "sambandha_means": SAMBANDHA_MEANS,
        "sambandha_karaka_names": dict(SAMBANDHA_KARAKA_NAMES),
        "raaja_sambandha_numbering": {
            entry["key"]: entry["number"] for entry in RAAJA_SAMBANDHA_YOGAS
        },
        "raaja_sambandha_are_common": RAAJA_SAMBANDHA_ARE_COMMON,
        "raaja_sambandha_magnitude_rule": RAAJA_SAMBANDHA_MAGNITUDE_RULE,
        "raaja_sambandha_note": (
            "Section 11.8 warns about itself before listing one: \u201cthese "
            "yogas are very common\u201d. Every verdict in the group carries "
            "that sentence and the section\u2019s own pointer back to section "
            "11.7.2, so a present verdict here is never read as weighing the "
            "same as one from section 11.7."
        ),
        "vargottamaamsa_definition": VARGOTTAMAAMSA_DEFINITION,
        "vargottamaamsa_spellings": list(VARGOTTAMAAMSA_SPELLINGS),
        "sun_excluded_note": (
            "The Sun cannot form a yoga about what accompanies him, so he is "
            "excluded from his own houses alongside the Moon."
        ),
    }


def raaja_magnitude(
    longitudes: dict[int, float],
    *,
    lagna_rasi: int,
    lagna_longitude: float | None = None,
    special_lagnas: dict[str, float] | None = None,
) -> dict:
    """§11.7.2 — how far each Raaja yoga in a chart fructifies.

    Longitudes, not signs: two of the three factors and Parasara's dasavarga
    count are degree measurements. Nothing is collapsed into a verdict —
    "None of the above factors influences the end result completely."
    """
    from dataclasses import asdict

    from hora.charts.planetary_yogas.raaja_advanced import arudha_effectiveness
    from hora.charts.planetary_yogas.raaja_magnitude import (
        dharma_karmadhipati_pair,
        magnitude,
    )
    from hora.core.ephemeris.base import PlanetPosition

    validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    if not longitudes:
        raise InputError("at least one graha longitude is required")
    positions = {}
    for graha, longitude in longitudes.items():
        validate.in_range("graha", int(graha), 0, 8)
        positions[int(graha)] = PlanetPosition(
            graha=int(graha), longitude=float(longitude) % 360.0,
            latitude=0.0, distance=1.0, speed_longitude=0.0,
            speed_latitude=0.0, speed_distance=0.0)
    data = _input(
        {g: int(p.longitude // 30) for g, p in positions.items()},
        "D1", False, positions=positions, lagna_rasi=int(lagna_rasi),
        lagna_longitude=lagna_longitude, special_lagnas=special_lagnas)

    pairs = [asdict(entry) for entry in magnitude(data)]
    special = dharma_karmadhipati_pair(data)
    return {
        "lagna_rasi": int(lagna_rasi),
        "lagna_rasi_name": RASI_NAMES[int(lagna_rasi)],
        "intro": RAAJA_MAGNITUDE_INTRO,
        "factors": [dict(entry) for entry in RAAJA_MAGNITUDE_FACTORS],
        "close_orb_degrees": RAAJA_CLOSE_ORB_DEGREES,
        "close_orb_is_approximate": RAAJA_CLOSE_ORB_IS_APPROXIMATE,
        "blemish_rule": RAAJA_BLEMISH_RULE,
        "orb_example": RAAJA_ORB_EXAMPLE,
        "dasa_varga_rule": PARASARA_DASA_VARGA_RULE,
        "amsa_results": [dict(entry) for entry in RAAJA_AMSA_RESULTS],
        "amsa_count_not_discussed": RAAJA_AMSA_COUNT_NOT_DISCUSSED,
        "amsa_divine_counts": list(RAAJA_AMSA_DIVINE_COUNTS),
        "amsa_divine_rule": RAAJA_AMSA_DIVINE_RULE,
        "amsa_divine_persons": list(RAAJA_AMSA_DIVINE_PERSONS),
        "simhaasanaamsa_rule": SIMHAASANAAMSA_RULE,
        "simhaasanaamsa_emperors": list(SIMHAASANAAMSA_EMPERORS),
        "simhaasanaamsa_footnote_unread": SIMHAASANAAMSA_FOOTNOTE_UNREAD,
        "amsa_spellings_in_11_7_2": dict(AMSA_SPELLINGS_IN_11_7_2),
        "amsa_spelling_note": (
            "Section 11.7.2 spells three of section 6.6's amsa names "
            "differently. Section 6.6 is the definitional table and is "
            "followed; the variants are recorded so a caller matching the "
            "section 11.7.2 spelling still finds the amsa."
        ),
        "dharma_karmadhipati_pair": (
            None if special is None else
            [{"graha": g, "graha_name": GRAHA_NAMES[g]} for g in special]
        ),
        "pairs": pairs,
        # 11.7.3 (18) — a modifier on the chart's Raaja yogas, not a yoga.
        "arudha_effectiveness_rule": ARUDHA_EFFECTIVENESS_RULE,
        "arudha_effectiveness": arudha_effectiveness(data),
        "final_judgment": RAAJA_FINAL_JUDGMENT,
        "not_assessed": [
            {"factor": "unafflicted",
             "why": FUNCTIONAL_MALEFIC_NOT_DEFINED,
             "open_item": "OI-88",
             "evidence": {
                 lagna: {"named": list(entry["named"]),
                         "candidates": list(entry["candidates"]),
                         "example": entry["example"], "text": entry["text"]}
                 for lagna, entry in FUNCTIONAL_MALEFIC_DATA_POINTS.items()
             },
             "evidence_note": (
                 "Two data points section 11.7.2 gives in passing, recorded "
                 "as data. They are not generalised into a rule and no lagna "
                 "the book has not spoken about appears here."
             )},
            {"factor": "unblemished",
             "why": ("section 11.7.2 says “bad avasthas (states)” without "
                     "naming which are bad"),
             "open_item": "OI-89"},
        ],
    }
