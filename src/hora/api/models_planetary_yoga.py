"""Schemas for the planetary yoga endpoints — book chapter 11 onward.

Not the nithya yoga of `/v1/yoga`; see `models_yoga.py` for that.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class YogaParticipantOut(BaseModel):
    graha: int
    graha_name: str
    sign: int = Field(..., ge=0, le=11)
    sign_name: str
    house_from_sun: int | None = Field(
        None, ge=1, le=12,
        description="Which house from the Sun this graha occupies, for a Ravi yoga",
    )


class YogaVerdictOut(BaseModel):
    key: str = Field(..., examples=["vesi"])
    name: str = Field(..., examples=["Vesi Yoga"])
    aliases: list[str]
    section: str = Field(..., examples=["11.2.1"])
    group: str = Field(..., examples=["ravi"])
    definition: str = Field(..., description="The book's own words")
    present: bool
    reason: str = Field(
        ...,
        description=(
            "Why the verdict is what it is — **always** populated. An absent "
            "yoga says what was missing, so 'not found' and 'not looked for' "
            "are distinguishable."
        ),
    )
    participants: list[YogaParticipantOut] = Field(
        ..., description="Empty when the yoga is absent"
    )
    qualifiers: list[str] = Field(
        ...,
        description=(
            "Things that weaken the yoga without cancelling it — section "
            "11.2.4's combustion is the first. Never flips `present`."
        ),
    )
    implies: list[str] = Field(
        ...,
        description=(
            "Yogas this one cannot hold without. Ubhayachara needs both the "
            "2nd and the 12th, so it implies Vesi and Vosi."
        ),
    )


class GrahaRefOut(BaseModel):
    graha: int
    graha_name: str


class YogaChartIn(BaseModel):
    rasis: dict[int, int] = Field(
        ..., description="Graha id to rasi index, 0 = Aries",
        examples=[{0: 3, 2: 4, 5: 2}],
    )
    chart: str = Field(
        "D1", description="Which chart these positions come from",
        examples=["D1", "D9", "D10"],
    )
    include_nodes: bool = Field(
        False,
        description=(
            "Whether Rahu and Ketu count as 'a planet' where a definition "
            "says so. Chapter 11 never settles it — see OI-73."
        ),
    )
    group: str | None = Field(
        None, examples=["ravi"],
        description="Restrict to one group of yogas; omit for all",
    )


class YogaChartOut(BaseModel):
    chart: str
    group: str | None = None
    include_nodes: bool
    grahas_considered: list[GrahaRefOut] = Field(
        ...,
        description=(
            "Which grahas a 'a planet other than Moon' definition drew on, so "
            "the node choice is visible in the output and not only the input."
        ),
    )
    evaluated: int = Field(
        ..., description="How many yogas were checked — every registered one"
    )
    present: list[str] = Field(..., description="Keys of the yogas that hold")
    yogas: list[YogaVerdictOut] = Field(
        ...,
        description=(
            "**Every** yoga evaluated, present or absent. Nothing is filtered "
            "out on the way here."
        ),
    )
    qualifiers_available: list[str]
    qualifiers_unavailable: list[str] = Field(
        ...,
        description=(
            "Qualifiers that could not be judged from the input. Combustion "
            "needs longitudes and a retrograde flag; signs alone cannot "
            "answer it, and its absence is not a finding of 'not combust'."
        ),
    )
    chart_note: str | None = None


class YogaOneIn(BaseModel):
    key: str = Field(..., examples=["budha_aaditya"])
    rasis: dict[int, int]
    chart: str = "D1"
    include_nodes: bool = False


class YogaSpecOut(BaseModel):
    key: str
    name: str
    aliases: list[str]
    section: str
    group: str
    definition: str
    implies: list[str]


class YogaCatalogueOut(BaseModel):
    groups: list[str]
    count: int
    yogas: list[YogaSpecOut]


class TimingPeriodsOut(BaseModel):
    graha: int
    graha_name: str


class TimingExampleOut(BaseModel):
    chart: str
    sign: int
    sign_name: str
    text: str
    periods: list[TimingPeriodsOut]


class PlanetaryYogaRulesOut(BaseModel):
    ravi_intro: str
    frequency_note: str
    preferred_charts: list[str]
    budha_aaditya_terms: dict[str, str]
    budha_aaditya_spelling_variants: list[str]
    combustion_note: str
    combustion_is_a_qualifier_not_a_veto: str
    timing_example: TimingExampleOut
    node_note: str
    results_note: str
    sun_excluded_note: str
