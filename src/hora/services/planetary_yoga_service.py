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
    BUDHA_AADITYA_SPELLING_VARIANTS,
    BUDHA_AADITYA_TERMS,
    BUDHA_AADITYA_TIMING_CHART,
    BUDHA_AADITYA_TIMING_PERIODS,
    BUDHA_AADITYA_TIMING_SIGN,
    BUDHA_AADITYA_TIMING_TEXT,
    COMBUSTION_WEAKENS_YOGA,
    GRAHA_NAMES,
    RASI_NAMES,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
)

InputError = validate.InputError

__all__ = ["InputError", "YogaError", "catalogue", "chart", "one", "rules"]

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
           positions=None) -> YogaInput:
    if chart_code not in KNOWN_CHARTS:
        raise InputError(
            f"unknown chart {chart_code!r}; expected one of "
            f"{', '.join(KNOWN_CHARTS)}"
        )
    return YogaInput(
        rasis={int(g): int(s) for g, s in rasis.items()},
        chart=chart_code, include_nodes=include_nodes, positions=positions,
    )


def chart(
    rasis: dict[int, int],
    *,
    chart_code: str = "D1",
    include_nodes: bool = False,
    group: str | None = None,
) -> dict:
    """Every registered yoga on one chart, present or absent."""
    data = _input(rasis, chart_code, include_nodes)
    if group is not None and group not in groups():
        raise InputError(
            f"unknown group {group!r}; expected one of {', '.join(groups())}")
    verdicts = evaluate(data, group=group)
    return {
        "chart": chart_code,
        "group": group,
        "include_nodes": include_nodes,
        "grahas_considered": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
            for g in data.considered()
        ],
        "evaluated": len(verdicts),
        "present": [v.key for v in verdicts if v.present],
        "yogas": [_verdict(v, data) for v in verdicts],
        # A caller cannot tell from signs alone whether Mercury is combust, so
        # the response says which qualifiers could be judged at all.
        "qualifiers_available": [],
        "qualifiers_unavailable": ["combustion"],
        "chart_note": (
            RAVI_YOGA_FREQUENCY_NOTE if chart_code == "D1" else None
        ),
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
