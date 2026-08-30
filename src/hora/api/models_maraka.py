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


class MaheswaraIn(BaseModel):
    """`graha_signs` drives exceptions 1 and 2; without it the answer names
    which exceptions could not be tested."""

    ak_sign: int = Field(..., ge=0, le=11, examples=[2])
    graha_signs: dict[int, int] | None = Field(None, examples=[None])


class LongevityIn(BaseModel):
    """Section 14.4. The lagna lord, the 8th lord by Table 32, the Moon and
    Saturn must all appear in `graha_signs`."""

    lagna: int = Field(..., ge=0, le=11, examples=[4])
    graha_signs: dict[int, int] = Field(..., examples=[{
        "0": 4, "1": 0, "2": 3, "3": 5, "4": 8, "5": 1, "6": 9}])
    hl_sign: int = Field(..., ge=0, le=11, examples=[2])


class EighthLordIn(BaseModel):
    """Section 14.5. `reference` is whichever of lagna and the 7th house you
    judge stronger — the section gives no way to compare them."""

    reference: int = Field(..., ge=0, le=11, examples=[7])
    graha_signs: dict[int, int] = Field(..., examples=[{"3": 6}])


class RudraIn(BaseModel):
    lagna: int = Field(..., ge=0, le=11, examples=[7])
    graha_signs: dict[int, int] = Field(..., examples=[{"3": 6, "4": 6}])
    graha_longitudes: dict[int, float] | None = Field(None, examples=[None])
