"""Request and response models for section 13.4.1."""
from __future__ import annotations

from pydantic import BaseModel, Field


class InfluencesIn(BaseModel):
    """`sign` is the rasi the house or arudha under analysis falls in — not
    necessarily the lagna's."""

    sign: int = Field(..., ge=0, le=11, examples=[3])
    graha_signs: dict[int, int] = Field(..., examples=[{
        "0": 3, "1": 6, "2": 1, "3": 7, "4": 9, "5": 10, "6": 2}])


class AnalysisRulesOut(BaseModel):
    intro: str
    factors: list[dict]
    divisional_chart_for: list[dict]
    d24_worked_example: list[dict]
    reference_rule: str
    house_versus_arudha: str
    arudha_is_maya: str
    influences_rule: str
    influence_kinds: list[str]
    influence_kinds_note: str
    a3_example: str
    third_house_versus_a3: str
    a3_periods: list[dict]
    standard_results: str
    standard_results_not_implemented: str
    closing: str
    closing_points_at: list[dict]
    tapaswi_yoga: dict
    example_44: dict
