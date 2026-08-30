"""Section 13.4.1 — the basic guidelines, service layer."""
from __future__ import annotations

from hora.charts.analysis import (
    MATTERS,
    AnalysisError,
    influence_frame,
    influences_on,
    plan,
)
from hora.core.const import (
    A3_BOOK_WRITING,
    A3_PERIODS,
    ANALYSIS_CLOSING,
    ANALYSIS_CLOSING_POINTS_AT,
    ANALYZING_CHARTS_INTRO,
    ARUDHA_IS_MAYA,
    BASIC_GUIDELINES,
    D24_MATTERS,
    DIVISIONAL_CHART_FOR,
    HOUSE_VERSUS_ARUDHA_RULE,
    INFLUENCE_KINDS,
    INFLUENCES_RULE,
    REFERENCE_RULE,
    STANDARD_RESULTS_NOT_IMPLEMENTED,
    STANDARD_RESULTS_RULE,
    THIRD_HOUSE_VERSUS_A3,
)
from hora.core.validate import InputError


def _plan(result) -> dict:
    return {
        "matter": result.matter,
        "chart": result.chart,
        "house": result.house,
        "references": list(result.references),
        "arudha": result.arudha,
        "why": result.why,
    }


def for_matter(matter: str) -> dict:
    """Factors 1 to 4 for one matter §13.4.1 names."""
    return _plan(plan(matter))


def matters() -> dict:
    """Every matter §13.4.1 works through, and the caveat on the rest."""
    return {
        "matters": [_plan(MATTERS[name]) for name in sorted(MATTERS)],
        "not_a_lookup_table": (
            "Section 13.4.1 teaches a method and works these matters through "
            "it. It is not a list of every question a chart can be asked, so "
            "anything else is refused rather than guessed at — choose the "
            "chart, house, reference and arudha yourself and post to "
            "/v1/analysis/influences."
        ),
    }


def influences(sign: int, graha_signs: dict[int, int]) -> dict:
    """Factor 5, all five kinds, on one house or arudha."""
    return influences_on(sign, graha_signs)


def frame(sign: int) -> dict:
    """The four house classes counted from one house or arudha."""
    return {"sign": sign, "frame": influence_frame(sign)}


def rules() -> dict:
    """Section 13.4.1's six factors and its two worked examples."""
    return {
        "intro": ANALYZING_CHARTS_INTRO,
        "factors": [{"number": n, "name": name, "rule": rule}
                    for n, (name, rule) in enumerate(BASIC_GUIDELINES, 1)],
        "divisional_chart_for": [
            {"matter": matter, "chart": chart, "note": note}
            for matter, chart, note in DIVISIONAL_CHART_FOR
        ],
        "d24_worked_example": [
            {"matter": matter, "house": house,
             "references": list(references), "arudha": arudha, "note": note}
            for matter, house, references, arudha, note in D24_MATTERS
        ],
        "reference_rule": REFERENCE_RULE,
        "house_versus_arudha": HOUSE_VERSUS_ARUDHA_RULE,
        "arudha_is_maya": ARUDHA_IS_MAYA,
        "influences_rule": INFLUENCES_RULE,
        "influence_kinds": list(INFLUENCE_KINDS) + ["house classes",
                                                    "baadhaka"],
        "influence_kinds_note": (
            "Section 13.4.1 names rasi drishti, graha drishti and argala "
            "directly, then the four house classes counted from the house, "
            "then baadhaka. All five are composed by "
            "/v1/analysis/influences."
        ),
        "a3_example": A3_BOOK_WRITING,
        "third_house_versus_a3": THIRD_HOUSE_VERSUS_A3,
        "a3_periods": [{"where": where, "result": result}
                       for where, result in A3_PERIODS],
        "standard_results": STANDARD_RESULTS_RULE,
        "standard_results_not_implemented": STANDARD_RESULTS_NOT_IMPLEMENTED,
        "closing": ANALYSIS_CLOSING,
        "closing_points_at": [{"what": what, "where": where}
                              for what, where in ANALYSIS_CLOSING_POINTS_AT],
    }


__all__ = ["AnalysisError", "InputError", "for_matter", "frame", "influences",
           "matters", "rules"]
