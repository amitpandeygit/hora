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
    GRAHA_NAMES,
    HOUSE_CATEGORIES,
    KEMADRUMA_EFFORT_NOTE,
    KEMADRUMA_KILLS_OTHER_YOGAS,
    PANAPHARA_SPELLING_VARIANTS,
    RASI_NAMES,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
    UPACHAYA,
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
        "sun_excluded_note": (
            "The Sun cannot form a yoga about what accompanies him, so he is "
            "excluded from his own houses alongside the Moon."
        ),
    }
