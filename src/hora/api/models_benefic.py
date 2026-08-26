"""Models for the natural benefic endpoints — book §3.2.2."""
from __future__ import annotations

from pydantic import BaseModel, Field


class BeneficIn(BaseModel):
    """A graha, plus whatever its nature depends on."""

    graha: int = Field(..., ge=0, le=8, examples=[3])
    paksha: int | None = Field(
        None, ge=0, le=1,
        description="Required for the Moon: 0 Sukla (waxing), 1 Krishna (waning)",
    )
    companions: list[int] | None = Field(
        None,
        description=(
            "Grahas sharing Mercury's rasi. Omit or leave empty for "
            '"alone", which section 3.2.2 makes a benefic.'
        ),
        examples=[[0, 2]],
    )


class BeneficOut(BaseModel):
    graha: int = Field(..., ge=0, le=8)
    graha_name: str
    nature: str = Field(..., examples=["benefic", "malefic", "neutral"])
    conditional: bool = Field(
        ..., description="True for Moon and Mercury, whose nature is not fixed"
    )
    reason: str


class GrahaRefOut(BaseModel):
    graha: int
    name: str


class BeneficRulesOut(BaseModel):
    section: str = Field(..., examples=["3.2.2"])
    title: str
    benefic_names: list[str] = Field(..., min_length=2, max_length=2)
    malefic_names: list[str] = Field(..., min_length=2, max_length=2)
    fixed_benefics: list[GrahaRefOut]
    fixed_malefics: list[GrahaRefOut]
    conditional: list[GrahaRefOut] = Field(..., min_length=2, max_length=2)
    mercury_rule: str
    moon_rule: str
    equal_split_note: str
    saturn_note: str
    inherent_nature_note: str
    counts: dict[str, int]
