"""Models for the hora endpoints — book §1.3.11."""
from __future__ import annotations

from pydantic import BaseModel, Field


class HoraIn(BaseModel):
    """A weekday and how long after sunrise."""

    weekday: int = Field(
        ..., ge=0, le=6, description="0 for Sunday through 6 for Saturday",
        examples=[3],
    )
    elapsed_hours: float = Field(
        ..., ge=0, description="Hours since sunrise", examples=[15.5]
    )
    day_length_hours: float = Field(
        24.0,
        gt=0,
        description=(
            "Sunrise to next sunrise. Defaults to 24, which is what §1.3.11's "
            "worked example assumes. Pass the real interval to divide the "
            "actual day into 24 equal parts, as the same section's first "
            "paragraph says. See open item OI-40."
        ),
    )


class HoraStepOut(BaseModel):
    number: int = Field(..., ge=1, le=5)
    description: str = Field(..., description="The step as section 1.3.11 states it")
    detail: str
    value: float | int | str


class HoraOut(BaseModel):
    index: int = Field(..., ge=1, le=24, description="Counted from sunrise")
    lord: int
    lord_name: str = Field(..., examples=["Moon"])
    position_in_cycle: int = Field(
        ..., ge=1, le=7, description="After subtracting multiples of 7"
    )
    weekday: int = Field(..., ge=0, le=6)
    weekday_name: str = Field(..., examples=["Wednesday"])
    weekday_lord: int
    weekday_lord_name: str = Field(..., examples=["Mercury"])
    elapsed_hours: float
    day_length_hours: float
    hora_length_hours: float
    steps: list[HoraStepOut]


class HoraOfDayOut(BaseModel):
    index: int = Field(..., ge=1, le=24)
    lord: int
    lord_name: str


class HoraDayOut(BaseModel):
    weekday: int = Field(..., ge=0, le=6)
    weekday_name: str
    weekday_lord_name: str
    horas: list[HoraOfDayOut] = Field(..., min_length=24, max_length=24)


class SpeedOrderOut(BaseModel):
    position: int = Field(..., ge=1, le=7)
    graha: int
    name: str


class WeekdayLordOut(BaseModel):
    weekday: int = Field(..., ge=0, le=6)
    weekday_name: str
    lord: int
    lord_name: str


class HoraRulesOut(BaseModel):
    section: str = Field(..., examples=["1.3.11"])
    title: str
    definition: str
    approximation: str
    horas_per_day: int
    cycle_length: int
    speed_order_rule: str
    speed_order: list[SpeedOrderOut] = Field(..., min_length=7, max_length=7)
    first_hora_rule: str
    weekday_lords: list[WeekdayLordOut] = Field(..., min_length=7, max_length=7)
    nominal_day_hours: float
    day_length_note: str
