"""Models for the graha arudha endpoints — book §9.5."""
from __future__ import annotations

from pydantic import BaseModel, Field

from hora.api.models_arudha import StepOut


class GrahaArudhaIn(BaseModel):
    """A chart as signs. Section 9.5 needs nothing finer."""

    graha_signs: dict[int, int] = Field(
        ...,
        description=(
            "Graha id -> occupied sign, 0 = Aries. For a divisional graha "
            "arudha, pass that chart's signs."
        ),
    )
    graha_longitudes: dict[int, float] | None = Field(
        None,
        description=(
            "Optional. Lets section 15.5.2's last rule run if the comparison "
            "of a planet's two owned signs ever reaches it. Section 15.5.2's "
            "own note says rule 4 always settles this case first."
        ),
    )


class GrahaArudhaOneIn(GrahaArudhaIn):
    graha: int = Field(..., ge=0, le=8, description="0 = Sun")


class GrahaArudhaTableIn(GrahaArudhaIn):
    include_steps: bool = Field(True, description="Set false for just the answers")


class GrahaArudhaOut(BaseModel):
    graha: int
    graha_name: str
    symbol: str = Field(..., examples=["AL(Su)"])
    graha_sign: int = Field(..., description="Step 1")
    graha_sign_name: str
    owned: list[int] = Field(..., description="Every sign the planet owns")
    owned_names: list[str]
    owned_sign: int = Field(..., description="Step 2 — the one selected")
    owned_sign_name: str
    owned_decided_by: str | None = Field(
        None,
        description=(
            "Which section 15.5.2 rule chose between two owned signs, or null "
            "when the planet owns only one"
        ),
    )
    owned_reason: str
    count: int = Field(..., ge=1, le=12, description="Step 3")
    before_exception: int = Field(..., description="Step 4, before step 5")
    before_exception_name: str
    exception_applied: bool
    exception_position: int | None = Field(
        None, description="1 or 7 when the exception fired, else null"
    )
    sign: int = Field(..., description="Step 6 — the arudha pada's sign")
    sign_name: str
    steps: list[StepOut] | None = None


class GrahaArudhaTableOut(BaseModel):
    arudhas: list[GrahaArudhaOut]


class OwnershipOut(BaseModel):
    graha: int
    graha_name: str
    symbol: str
    owns: list[int]
    owns_names: list[str]
    needs_comparison: bool = Field(
        ..., description="True for the five planets that own two signs"
    )


class GrahaArudhaRuleStepOut(BaseModel):
    number: int = Field(..., ge=1, le=6)
    name: str
    text: str


class GrahaArudhaRulesOut(BaseModel):
    section: str
    steps: list[GrahaArudhaRuleStepOut]
    note: str = Field(..., description="Section 9.5's note on the two-sign owners")
    stronger_sign_section: str
    ownership: list[OwnershipOut]
