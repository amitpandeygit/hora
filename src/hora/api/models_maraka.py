"""Request and response models for chapter 14."""
from __future__ import annotations

from pydantic import BaseModel, Field


class MarakaIn(BaseModel):
    """`graha_signs` is optional. Without it only the 2nd and 7th lords are
    returned, and the response says the list is incomplete."""

    lagna: int = Field(..., ge=0, le=11, examples=[4])
    graha_signs: dict[int, int] | None = Field(
        None, examples=[{"2": 2, "6": 8}])


class MarakaRulesOut(BaseModel):
    framing: str
    scope: str
    not_covered: list[dict]
    maraka_means: str
    maraka_sthana_means: str
    maraka_graha_means: str
    charts: str
    chart_order: list[dict]
    houses_of_life_rule: str
    houses_of_life: dict
    derivation: list[dict]
    maraka_houses: list[int]
    good_longevity: str
    sthana_rule: str
    additional_rule: str
    additional_targets: list[str]
    powerfully_undefined: str
    malefics: list[str]
    malefics_note: str
    stronger_remark: str
    not_ranked: str
    use: str
    examples: list[dict]
