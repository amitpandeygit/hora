"""Request and response models for section 13.2."""
from __future__ import annotations

from pydantic import BaseModel, Field


class FunctionalRulesOut(BaseModel):
    chapter_intro: str
    further_reading: str
    intro: str
    rules: list[str]
    two_rasi_owners: str
    moon_not_listed_for_movable: str
    moon_movable_wording: str
    moon_omitted_from: list[str]
    table_30: dict
    table_is_the_authority: str
    divergences: list[dict]
    yogakarakas: dict
    yogakaraka_rule: str
    placement: str
    yogada: str
    yogada_kinds: dict
    yogada_links: list[str]
    natural_versus_functional: str
    planets: list[str]
    planets_note: str
    houses_owned_example: dict


class FunctionalLagnaOut(BaseModel):
    lagna: int
    lagna_name: str
    yogakaraka: str | None
    planets: list[dict]
    moon_needs_phase: bool
    placement: str
    table_is_the_authority: str


class FunctionalPlanetIn(BaseModel):
    planet: str = Field(..., examples=["Saturn"])
    lagna: int = Field(..., ge=0, le=11, examples=[1])
    waxing: bool | None = Field(
        None, description="Only the Moon needs this, and only for Ar, Li, Cp.",
        examples=[None])
