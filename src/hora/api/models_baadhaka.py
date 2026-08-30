"""Request and response models for section 13.3."""
from __future__ import annotations

from pydantic import BaseModel, Field


class BaadhakaSignIn(BaseModel):
    """`sign` is whatever is being read — a house's rasi or an arudha's."""

    sign: int = Field(..., ge=0, le=11, examples=[2])
    graha_signs: dict[int, int] | None = Field(
        None, description="Graha id to occupied sign, in the same chart. "
                          "Without it, only the sthaana's lords are judged.",
        examples=[None])


class BaadhakaCheckIn(BaadhakaSignIn):
    graha: int = Field(..., ge=0, examples=[4])


class BaadhakaChartIn(BaseModel):
    lagna_sign: int = Field(..., ge=0, le=11, examples=[2])
    graha_signs: dict[int, int] | None = Field(None, examples=[None])


class BaadhakaRulesOut(BaseModel):
    rule: str
    sthaana_means: str
    baadhaka_means: str
    house_by_modality: dict
    table_31: dict
    table_31_is_derived: str
    co_lords: str
    includes_occupants: str
    scope: str
    example: str
    example_steps: list[dict]
    derived_matches_printed: bool
    rasis: list[str]
