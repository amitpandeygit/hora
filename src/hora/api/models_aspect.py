"""Request and response schemas for the aspect endpoints — book chapter 10."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AspectedRasiOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    house_from_graha: int = Field(
        ..., ge=1, le=12,
        description="Which house the aspected rasi is, counted from the graha",
    )
    house: int | None = Field(
        None, ge=1, le=12,
        description=(
            "Which house of the chart the aspected rasi is. Null unless a "
            "lagna_rasi was given — section 10.2 needs no lagna to say which "
            "rasis are aspected, only to say which houses."
        ),
    )


class AspectedGrahaOut(BaseModel):
    graha: int
    graha_name: str
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str


class RasiRefOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str


class GrahaAspectOut(BaseModel):
    graha: int
    graha_name: str
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    aspects_houses_from_itself: list[int] = Field(
        ...,
        description='The 7th always; plus the graha\'s special aspects if it has any',
        examples=[[5, 7, 9]],
    )
    has_special_aspect: bool = Field(
        ...,
        description="True only for Mars, Jupiter and Saturn — section 10.2 names no others",
    )
    aspected_rasis: list[AspectedRasiOut]
    aspected_grahas: list[AspectedGrahaOut] = Field(
        ...,
        description=(
            "Grahas occupying the aspected rasis. Empty unless other "
            "placements were supplied, and it can include Rahu or Ketu: being "
            "aspected depends only on where a graha sits."
        ),
    )
    rasi_drishti_rasis: list[RasiRefOut] = Field(
        ...,
        description=(
            "Section 10.1's second kind — the rasis aspected by the rasi this "
            "graha occupies, which the graha inherits."
        ),
    )


class GrahaAspectIn(BaseModel):
    graha: int = Field(..., ge=0, le=8, examples=[4])
    rasi: int = Field(..., ge=0, le=11, examples=[2])
    lagna_rasi: int | None = Field(None, ge=0, le=11)
    others: dict[int, int] | None = Field(
        None,
        description="Other placements, graha id to rasi, to resolve aspected grahas",
    )
    rahu_ketu_aspects: bool = Field(
        False,
        description=(
            "Give Rahu and Ketu the 5th and 9th as well. Off by default: "
            "section 10.2 names special aspects for Mars, Jupiter and Saturn "
            "only."
        ),
    )


class ChartAspectIn(BaseModel):
    rasis: dict[int, int] = Field(
        ..., description="Graha id to rasi index, 0 = Aries",
        examples=[{0: 1, 1: 0, 2: 7, 3: 8, 4: 5, 5: 9, 6: 7}],
    )
    lagna_rasi: int | None = Field(None, ge=0, le=11, examples=[7])
    rahu_ketu_aspects: bool = False


class ChartAspectOut(BaseModel):
    lagna_rasi: int | None = None
    lagna_rasi_name: str | None = None
    aspecting_grahas: list[int]
    grahas: list[GrahaAspectOut]
    note: str


class BetweenIn(BaseModel):
    graha: int = Field(..., ge=0, le=8)
    graha_rasi: int = Field(..., ge=0, le=11)
    target_rasi: int = Field(..., ge=0, le=11)
    rahu_ketu_aspects: bool = False


class BetweenOut(BaseModel):
    graha: int
    graha_name: str
    graha_rasi: int
    graha_rasi_name: str
    target_rasi: int
    target_rasi_name: str
    house_from_graha: int = Field(..., ge=1, le=12)
    aspects: bool
    graha_aspects_houses: list[int]


class AspectKindOut(BaseModel):
    key: str
    name: str
    gloss: str
    rule: str
    counted_from: str
    varies_by: str


class SpecialAspectOut(BaseModel):
    graha: int
    graha_name: str
    houses: list[int] = Field(..., description="The special houses, without the 7th")
    all_houses: list[int] = Field(..., description="Including the 7th")
    text: str


class GrahaRefOut(BaseModel):
    graha: int
    graha_name: str


class AspectRulesOut(BaseModel):
    definition: str
    drishti_means: str = Field(..., examples=["aspect"])
    kinds: list[AspectKindOut]
    seventh_house_rule: str
    special_aspect_rule: str
    special_aspects: list[SpecialAspectOut]
    aspected_planet_rule: str
    aspected_planet_example: str
    aspecting_grahas: list[GrahaRefOut]
    nodes_note: str
    skill_note: str
