"""Models for the Sun-Moon yoga endpoints — book §1.3.9."""
from __future__ import annotations

from pydantic import BaseModel, Field


class YogaIn(BaseModel):
    """Two longitudes. Section 1.3.9's procedure needs nothing else."""

    sun_longitude: float = Field(
        ..., description="Sidereal longitude in degrees; the sum is wrapped into 0-360",
        examples=[293.8333333333333],
    )
    moon_longitude: float = Field(..., examples=[197.33333333333334])


class YogaStepOut(BaseModel):
    number: int = Field(..., ge=1, le=5)
    description: str = Field(..., description="The step as section 1.3.9 states it")
    detail: str = Field(..., description="This pair's working, in words")
    value: float | int | str


class YogaOut(BaseModel):
    index: int = Field(..., ge=1, le=27, description="Table 5's index")
    name: str = Field(..., description="Common transliteration", examples=["Ganda"])
    name_book: str = Field(..., description="Table 5's own spelling", examples=["Ganda"])
    meaning: str = Field(
        ..., description="Table 5's third column", examples=["Danger"]
    )
    sun_longitude: float
    moon_longitude: float
    raw_sum: float = Field(..., description="Before 360 is removed", examples=[491.1667])
    total: float = Field(..., ge=0, lt=360, description="After 360 is removed")
    total_minutes: float = Field(
        ..., description="The book divides in arcminutes: 7870' / 800'"
    )
    quotient: float = Field(..., examples=[9.8375])
    completed: int = Field(..., ge=0, le=26, description="The integer part")
    steps: list[YogaStepOut]


class Table5RowOut(BaseModel):
    index: int = Field(..., ge=1, le=27)
    name: str
    name_simple: str
    meaning: str


class YogaRulesOut(BaseModel):
    section: str = Field(..., examples=["1.3.9"])
    title: str
    procedure: list[str]
    span_degrees: float
    span_minutes: int
    minutes_per_degree: int
    count: int
    uses_sum_not_difference: str
    table_5: list[Table5RowOut] = Field(..., min_length=27, max_length=27)
