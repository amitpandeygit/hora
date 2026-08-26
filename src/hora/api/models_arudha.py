"""Models for the arudha pada endpoints — book chapter 9."""
from __future__ import annotations

from pydantic import BaseModel, Field


class StepOut(BaseModel):
    """One of section 9.2's six numbered steps, and what it produced."""

    number: int = Field(..., ge=1, le=6)
    name: str = Field(..., examples=["count_to_lord"])
    description: str = Field(..., description="The step as section 9.2 states it")
    sign: int | None = Field(None, description="0 = Aries, where the step lands on one")
    sign_name: str | None = None
    count: int | None = Field(None, ge=1, le=12)
    detail: str | None = Field(
        None, description="This chart's working for the step, in words"
    )


class ArudhaPadaOut(BaseModel):
    house: int = Field(..., ge=1, le=12)
    symbol: str = Field(..., examples=["A1", "A7"])
    generic_names: list[str] = Field(
        ...,
        description=(
            'Section 9.2: "Arudha pada of a house is simply called arudha or '
            'pada also."'
        ),
    )
    specific_names: list[str] = Field(
        ..., description="Table 18's specific names for this house's arudha"
    )
    special_symbol: str | None = Field(None, examples=["AL", "UL"])
    special_name: str | None = Field(None, examples=["Arudha Lagna"])

    house_sign: int = Field(..., description="Step 1")
    house_sign_name: str
    lord: int = Field(..., description="Step 2 — the lord of that sign")
    lord_name: str
    lord_sign: int = Field(..., description="Step 2 — the sign it occupies")
    lord_sign_name: str
    count: int = Field(..., ge=1, le=12, description="Step 3")
    before_exception: int = Field(..., description="Step 4, before step 5 is applied")
    before_exception_name: str
    exception_applied: bool = Field(..., description="Whether step 5 changed the sign")
    exception_position: int | None = Field(
        None, description="1 or 7 when the exception fired, else null"
    )
    sign: int = Field(..., description="Step 6 — the arudha pada's sign")
    sign_name: str
    steps: list[StepOut] | None = Field(
        None, description="All six steps in order; omitted when not requested"
    )


class ArudhaIn(BaseModel):
    """A chart, as signs. Section 9.2 needs nothing finer than the sign."""

    lagna_sign: int = Field(
        ..., ge=0, le=11,
        description=(
            "The lagna's sign in the chart of interest, 0 = Aries. For a "
            "divisional arudha, pass the divisional lagna."
        ),
    )
    graha_signs: dict[int, int] = Field(
        ...,
        description="Graha id -> occupied sign, in that same chart",
        examples=[{0: 11, 1: 2, 2: 0, 3: 11, 4: 0, 5: 11, 6: 0, 7: 0, 8: 0}],
    )
    graha_longitudes: dict[int, float] | None = Field(
        None,
        description=(
            "Graha id -> sidereal longitude, in the same chart. Optional. "
            "Supplying it lets section 15.5.1's cascade reach its last rule "
            "(the co-lord more advanced in its rasi) when a house falls in "
            "Scorpio or Aquarius; with signs alone the cascade can only reach "
            "rule 4."
        ),
    )
    stronger_lord: dict[int, int] | None = Field(
        None,
        description=(
            "Sign -> graha, for Aquarius (10) and Scorpio (7) only. Optional: "
            "section 15.5.1's cascade resolves these on its own. Supply it "
            "only to override that — an explicit choice is never overruled."
        ),
        examples=[{7: 2, 10: 6}],
    )


class ArudhaOneIn(ArudhaIn):
    house: int = Field(..., ge=1, le=12)


class ArudhaTableIn(ArudhaIn):
    include_steps: bool = Field(
        True, description="Set false for just the twelve answers"
    )


class ArudhaTableOut(BaseModel):
    lagna_sign: int
    lagna_sign_name: str
    padas: list[ArudhaPadaOut]


class RuleStepOut(BaseModel):
    number: int = Field(..., ge=1, le=6)
    name: str
    text: str = Field(..., description="Section 9.2's wording")


class DualLordedOut(BaseModel):
    sign: int
    sign_name: str
    owners: list[int]
    owner_names: list[str]
    rule: str


class SpecificNamesOut(BaseModel):
    house: int = Field(..., ge=1, le=12)
    symbol: str
    names: list[str]


class SpecialSymbolOut(BaseModel):
    house: int
    symbol: str
    name: str


class ArudhaRulesOut(BaseModel):
    section: str
    steps: list[RuleStepOut]
    dual_lorded_signs: list[DualLordedOut]
    strength_comparison_defined_in: str
    strength_comparison_note: str
    strength_comparison_section: str
    generic_names: list[str]
    specific_names: list[SpecificNamesOut] = Field(..., description="Table 18")
    strength_comparison_available: bool = Field(
        ...,
        description=(
            "True: section 15.5.1's cascade is implemented. A house in "
            "Aquarius or Scorpio can be resolved, or an explicit "
            "stronger_lord may still be supplied."
        ),
    )
    special_symbols: list[SpecialSymbolOut]
