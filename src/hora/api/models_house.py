"""Models for the house endpoints — book chapter 7."""
from __future__ import annotations

from pydantic import BaseModel, Field


class HousesFromIn(BaseModel):
    """A reference rasi, and which reference it is taken to be."""

    reference_rasi: int = Field(..., ge=0, le=11, description="0 = Aries")
    reference: str = Field(
        "lagna",
        examples=["lagna", "chandra_lagna", "paaka_lagna"],
        description="Which of section 7.3's references this rasi is",
    )


class HouseOut(BaseModel):
    house: int = Field(..., ge=1, le=12)
    rasi: int
    rasi_name: str
    lord: int
    lord_name: str
    categories: list[str] = Field(
        ..., description="trikona, kendra, upachaya, dusthana and the rest"
    )
    purushartha: str | None = Field(
        None, description="dharma, artha, kaama or moksha"
    )
    half: str = Field(..., description='"visible" or "invisible"')
    signifies: str


class HousesFromOut(BaseModel):
    reference: str
    reference_name: str
    reference_rasi: int
    reference_rasi_name: str
    shows: str
    houses: list[HouseOut]


class ReferencesIn(BaseModel):
    """Everything needed to resolve the references of section 7.3."""

    lagna_rasi: int = Field(..., ge=0, le=11)
    graha_rasis: dict[int, int] = Field(
        default_factory=dict,
        examples=[{0: 5, 1: 3}],
        description="Graha id to rasi. 0 = Sun .. 8 = Ketu.",
    )
    ghati_lagna_rasi: int | None = Field(None, ge=0, le=11)
    hora_lagna_rasi: int | None = Field(None, ge=0, le=11)


class ReferenceOut(BaseModel):
    reference: str
    name: str
    shows: str
    available: bool
    rasi: int | None = None
    rasi_name: str | None = None
    unavailable_because: str | None = Field(
        None, description="Why it could not be resolved — never silently dropped"
    )


class ReferencesOut(BaseModel):
    lagna_rasi: int
    references: list[ReferenceOut]


class CategoryOut(BaseModel):
    category: str
    synonyms: list[str]
    houses: list[int]
    shows: str | None = Field(
        None,
        description=(
            'What the category signifies. None for panaphara, apoklima '
            'and chaturasra, which section 7.4 gives no signification.'
        ),
    )
    derivation: str | None = Field(
        None,
        description=(
            'How the category is defined, where section 7.4 defines it by '
            'construction rather than by meaning.'
        ),
    )
    presiding_deity: str | None = None


class HalvesOut(BaseModel):
    """§7.4.5's split, counted from the same base house as the categories."""

    visible: list[int]
    invisible: list[int]


class CategoriesOut(BaseModel):
    base_house: int
    categories: list[CategoryOut]
    halves: HalvesOut


class SignificationOut(BaseModel):
    house: int
    signifies: str
    purushartha: str | None = None
    half: str


class PurusharthaOut(BaseModel):
    purushartha: str
    houses: list[int]
    meaning: str


class GrahaLagnaOut(BaseModel):
    graha: int
    graha_name: str
    houses: list[int] = Field(..., description="Table 12")


class HouseReferenceRuleOut(BaseModel):
    reference: str
    name: str
    shows: str
    available: bool
    note: str


class HouseDefinitionOut(BaseModel):
    """Section 1.3.3 — what a house is and what it is counted from."""

    sanskrit: str = Field(..., examples=["bhava"])
    text: str
    order_wraps: str = Field(
        ..., description="The step readers get wrong: Pisces is followed by Aries"
    )
    common_references: list[str]
    default_reference: str = Field(..., examples=["lagna"])
    default_reference_rule: str = Field(
        ...,
        description=(
            "Why every reference argument defaults to the lagna: section "
            "1.3.3 says an unspecified reference means the lagna"
        ),
    )


class HouseRulesOut(BaseModel):
    definition: HouseDefinitionOut
    significations: list[SignificationOut]
    categories: list[CategoryOut]
    purusharthas: list[PurusharthaOut]
    halves: dict[str, list[int]]
    graha_lagnas: list[GrahaLagnaOut]
    references: list[HouseReferenceRuleOut]
    note: str


class DerivedHouseOut(BaseModel):
    """Section 7.2: a house counted from another house."""

    house: int = Field(..., ge=1, le=12)
    from_house: int = Field(..., ge=1, le=12)
    result: int = Field(..., ge=1, le=12)
    counting_note: str = Field(
        ...,
        description="Counting is inclusive — the 2nd from the 3rd is the 4th",
    )
    from_house_signifies: str
    house_signifies: str
    result_signifies: str
    concatenation: str
    rule: str


class HouseMeaningsOut(BaseModel):
    """Section 7.3: which of a house's meanings apply in a divisional chart."""

    house: int = Field(..., ge=1, le=12)
    chart: str = Field(..., examples=["D16"])
    house_signifies: str
    chart_signifies: str
    shared_meanings: list[str] = Field(
        ..., description="Words present in both lists; never invented"
    )
    derivable: bool
    rule: str
    limitation: str = Field(
        ...,
        description=(
            "Where the link is semantic rather than literal the overlap is "
            "empty or partial. Section 7.3's own D-12 case is one such."
        ),
    )
