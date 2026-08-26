"""Models for the stronger-rasi endpoints — book §15.5.2."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RasiStrengthIn(BaseModel):
    first: int = Field(..., ge=0, le=11, description="0 = Aries")
    second: int = Field(..., ge=0, le=11)
    graha_longitudes: dict[int, float] = Field(
        ..., description="Graha id -> sidereal longitude in degrees"
    )
    purpose: str = Field(
        "phalita",
        description=(
            "Which adaptation of the section's warning applies. 'phalita' "
            "covers Narayana and other phalita dasas; 'ak_based' covers "
            "Atmakaraka kendradi dasas; 'ayur' is refused, because the text "
            "does not say how to weigh its aspects."
        ),
        examples=["phalita", "ak_based"],
    )
    dasa_years: dict[int, float] | None = Field(
        None,
        description=(
            "Passed through to section 15.5.1 when a co-owned rasi's lord has "
            "to be resolved for dasa purposes"
        ),
    )
    atma_karaka_rasi: int | None = Field(
        None, ge=0, le=11, description="Required by purpose 'ak_based'"
    )


class RasiRuleVerdictOut(BaseModel):
    rule: str = Field(..., examples=["1", "4", "6", "ak", "ak-placement"])
    description: str = Field(..., description="The rule as section 15.5.2 states it")
    winner: int | None = None
    winner_name: str | None = None
    decided: bool | None = Field(
        None, description="Null when the rule could not be evaluated"
    )
    detail: str


class RasiStrengthOut(BaseModel):
    first: int
    first_name: str
    second: int
    second_name: str
    purpose: str
    winner: int | None = None
    winner_name: str | None = None
    decided_by: str | None = None
    determined: bool
    reason: str
    rules: list[RasiRuleVerdictOut]


class PurposeOut(BaseModel):
    key: str
    name: str
    applies_to: str
    rule_2_planets: str
    implemented: bool
    note: str | None = None


class PurposesOut(BaseModel):
    warning: str = Field(..., description="Section 15.5.2's warning, verbatim")
    purposes: list[PurposeOut]
