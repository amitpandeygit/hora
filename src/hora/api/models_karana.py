"""Models for the karana endpoints — book §1.3.10."""
from __future__ import annotations

from pydantic import BaseModel, Field


class KaranaSlotIn(BaseModel):
    """A half-tithi slot, or a tithi and which half of it — one or the other."""

    slot: int | None = Field(
        None, ge=1, le=60, description="Half-tithi slot, 1 to 60", examples=[58]
    )
    tithi: int | None = Field(None, ge=1, le=30, examples=[29])
    half: int | None = Field(
        None, ge=1, le=2, description="1 for the first half, 2 for the second",
        examples=[2],
    )


class KaranaLongitudesIn(BaseModel):
    sun_longitude: float = Field(..., examples=[227.76666666666668])
    moon_longitude: float = Field(..., examples=[84.2])


class KaranaOut(BaseModel):
    slot: int = Field(..., ge=1, le=60, description="Half-tithi slot in the month")
    tithi: int = Field(..., ge=1, le=30)
    half: int = Field(..., ge=1, le=2)
    index: int = Field(..., ge=1, le=11, description="Which of the 11 karanas")
    name: str = Field(..., examples=["Shakuni"])
    name_book: str = Field(..., description="§1.3.10's spelling", examples=["Sakuna"])
    repeats: bool = Field(
        ..., description="True for the first 7, which repeat 8 times"
    )
    occurrences: int = Field(..., description="8 for the repeating 7, 1 for the last 4")


class KaranaTableRowOut(BaseModel):
    index: int = Field(..., ge=1, le=11)
    name: str
    name_simple: str
    repeats: bool
    occurrences: int
    slots: list[int] = Field(..., description="Every slot in a month it falls on")


class KaranaRulesOut(BaseModel):
    section: str = Field(..., examples=["1.3.10"])
    title: str
    definition: str
    count: int
    karanas_per_tithi: int
    slots_per_month: int
    span_degrees: float
    repeating_rule: str
    repeating_count: int
    repetitions: int
    first_repeating_slot: int
    once_only_rule: str
    once_only_count: int
    first_once_only_slot: int
    wraps_the_month: str
    karanas: list[KaranaTableRowOut] = Field(..., min_length=11, max_length=11)
