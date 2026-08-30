"""Request and response models for section 12.7."""
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class TrikonaSodhanaIn(BaseModel):
    """Section 12.7.1. Give either the twelve rekhas directly, or the eight
    reference signs to have the BAV computed first."""

    owner: str = Field(..., examples=["Mercury"])
    rekhas: list[int] | None = Field(
        None, examples=[[7, 4, 7, 4, 4, 3, 4, 4, 4, 3, 6, 4]])
    reference_signs: dict[str, int] | None = Field(None, examples=[None])

    @model_validator(mode="after")
    def one_of_them(self) -> TrikonaSodhanaIn:
        if (self.rekhas is None) == (self.reference_signs is None):
            raise ValueError(
                "give exactly one of rekhas or reference_signs: rekhas to "
                "reduce a BAV you already have, reference_signs to have it "
                "computed from a chart first")
        return self


class TrikonaSodhanaOut(BaseModel):
    owner: str
    rule: str
    rules: list[str]
    before: list[int]
    after: list[int]
    trines: list[dict]
    footnote_44: str
    only_rule_three_is_implemented: str


class SodhanaRulesOut(BaseModel):
    intro: str
    soav_means: str
    soav_is_a_reduced_bav: str
    pinda_not_yet_defined: str
    trikona_sodhana: dict
    ekaadhipatya_sodhana: dict
    example_40: dict
    example_41: dict
    example_42: dict


class EkaadhipatyaIn(BaseModel):
    """Section 12.7.2. `occupied_signs` is required and has no default: the
    section says "occupied by a planet (or planets)" without saying whether
    Rahu and Ketu count, so the caller states it rather than us guessing."""

    owner: str = Field(..., examples=["Mercury"])
    rekhas: list[int] | None = Field(
        None, examples=[[3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0]])
    reference_signs: dict[str, int] | None = Field(None, examples=[None])
    occupied_signs: list[int] = Field(..., examples=[[2, 4, 5, 11]])
    already_trikona_reduced: bool = Field(..., examples=[True])

    @model_validator(mode="after")
    def one_of_them(self) -> EkaadhipatyaIn:
        if (self.rekhas is None) == (self.reference_signs is None):
            raise ValueError(
                "give exactly one of rekhas or reference_signs")
        if self.reference_signs is not None and self.already_trikona_reduced:
            raise ValueError(
                "reference_signs yields a raw BAV, so it cannot already be "
                "trikona reduced; set already_trikona_reduced to false")
        return self


class EkaadhipatyaOut(BaseModel):
    owner: str
    rule: str
    rules: list[dict]
    trikona_applied_first: bool
    before: list[int]
    after: list[int]
    occupied_signs: list[int]
    pairs: list[dict]
    untouched: dict
    occupancy_undefined: str
    tie_is_uncovered: str
    tie_reading: str
    tie_hit_in_this_chart: list[list[int]]
