"""Models for the tithi endpoints — book §1.3.8.1."""
from __future__ import annotations

from pydantic import BaseModel, Field


class TithiIn(BaseModel):
    """Two longitudes. Section 1.3.8.1's procedure needs nothing else."""

    sun_longitude: float = Field(
        ..., description="Sidereal longitude in degrees; wrapped into 0-360",
        examples=[227.76666666666668],
    )
    moon_longitude: float = Field(..., examples=[84.2])


class TithiStepOut(BaseModel):
    number: int = Field(..., ge=1, le=4)
    name: str = Field(..., examples=["elongation", "completed", "index", "name"])
    description: str = Field(..., description="The step as section 1.3.8.1 states it")
    value: float | int | None = None
    detail: str | None = Field(None, description="This pair's working, in words")


class TithiOut(BaseModel):
    index: int = Field(..., ge=1, le=30, description="Counted from the new moon")
    number_in_paksha: int = Field(
        ..., ge=1, le=15, description="Table 3 lists fifteen names, used twice"
    )
    name: str = Field(..., examples=["Chaturthi"])
    full_name: str = Field(
        ...,
        description=(
            'Fortnight first, then the tithi name — "Krishna Chaturthi", not '
            '"Chaturthi"'
        ),
        examples=["Krishna Chaturthi"],
    )
    alternate_names: list[str] = Field(
        default_factory=list, description="Table 3's other spellings for this tithi"
    )
    paksha: int = Field(..., ge=0, le=1, description="0 = Sukla, 1 = Krishna")
    paksha_name: str
    lord: int
    lord_name: str

    raw_difference: float = Field(
        ..., description="Moon minus Sun, before normalising. Negative when Sun leads."
    )
    elongation: float = Field(
        ..., ge=0, lt=360, description="Step 1 — how advanced the Moon is"
    )
    completed: int = Field(..., ge=0, le=29, description="Step 2 — whole tithis over")
    elapsed_in_tithi: float = Field(..., description="Degrees into the current tithi")
    fraction_elapsed: float = Field(..., ge=0, lt=1)
    starts_at: float = Field(..., description="Elongation at which this tithi begins")
    ends_at: float
    steps: list[TithiStepOut]


class PakshaOut(BaseModel):
    index: int
    name: str
    synonyms: list[str]
    describes: str = Field(..., examples=["brighter fortnight"])
    elongation_from: float
    elongation_to: float
    moon_is: str = Field(..., examples=["waxing", "waning"])


class Table3RowOut(BaseModel):
    sukla: int = Field(..., ge=1, le=15, description="Its number in the brighter fortnight")
    krishna: int | None = Field(
        None,
        description=(
            "Its number in the darker fortnight. Null for the 15th, which is "
            "the full moon and has no counterpart."
        ),
    )
    name: str
    krishna_name: str | None = Field(
        None,
        description=(
            "The name of the corresponding tithi in the darker fortnight. "
            "Null for the 15th, whose counterpart is Amavasya rather than a "
            "repeat of Paurnami."
        ),
    )
    alternate_names: list[str]
    lord: int
    lord_name: str


class TithiRuleStepOut(BaseModel):
    number: int = Field(..., ge=1, le=4)
    name: str
    text: str


class SpecialTithiOut(BaseModel):
    index: int
    name: str
    note: str


class TithiRulesOut(BaseModel):
    section: str
    definition: str
    span_degrees: float = Field(..., description="Twelve")
    per_month: int = Field(..., description="Thirty")
    per_paksha: int = Field(..., description="Fifteen")
    month_starts: str
    steps: list[TithiRuleStepOut]
    naming_convention: str
    pakshas: list[PakshaOut]
    table_3: list[Table3RowOut]
    new_moon: SpecialTithiOut
    full_moon: SpecialTithiOut
