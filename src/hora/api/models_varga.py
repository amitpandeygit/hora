"""Request and response models for the longitude-level varga endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class VargaComputeIn(BaseModel):
    """A longitude and the charts to place it in."""

    longitude: str | float = Field(
        ...,
        examples=["11 Ge 00", "5s 17 45", 71.0],
        description=(
            "Decimal degrees from 0 Aries, or either classical notation — "
            'rasi-relative ("11 Ge 00") or sign-degree-minute ("5s 17 45")'
        ),
    )
    charts: list[str] = Field(
        default_factory=lambda: ["D9"],
        min_length=1,
        max_length=64,
        examples=[["D9", "D10", "D60"]],
        description=(
            "Varga codes. Any D<N> up to D300 is accepted. At least one and at "
            "most 64 — an empty list is a mistake, not a request for nothing."
        ),
    )
    variants: dict[str, str] = Field(
        default_factory=dict,
        description='Per-chart variant override, e.g. {"D2": "parivritti"}',
    )


class VargaInputOut(BaseModel):
    degrees: float
    sign_dm: str
    rasi_dm: str
    rasi: int
    rasi_name: str
    degrees_in_rasi: float


class VargaPlacementOut(BaseModel):
    """Where the longitude landed, and the rule that put it there."""

    chart: str
    name: str
    divisions: int
    part_size_degrees: float
    part_index: int = Field(..., description="Which part of the natal rasi, 1-based")
    rasi: int
    rasi_name: str
    varga_longitude: float = Field(
        ..., description="Position projected into the divisional chart"
    )
    degrees_in_rasi: float
    dms: str
    counts_from: str | None = Field(
        None, description="The book's rule, so a placement can be explained"
    )
    variant: str | None = None


class VargaComputeOut(BaseModel):
    input: VargaInputOut
    charts: list[VargaPlacementOut]


class VargaRuleOut(BaseModel):
    chart: str
    name: str
    divisions: int
    part_size_degrees: float
    aliases: list[str]
    counts_from: str | None = None
    worked_example_in_book: bool = Field(
        ..., description="False marks a rule with no example to catch a slip"
    )
    signifies: str | None = Field(None, description="Table 11 — the area of life")


class AnalysisPatternOut(BaseModel):
    matter: str
    chart: str
    why: str
    houses: list[int]
    significator: str
    link: str


class VargaPlaneOut(BaseModel):
    plane: str = Field(..., examples=["physical", "mental"])
    divisions: str = Field(..., examples=["1 to 12", "above 36"])
    low: int
    high: int | None = None
    shows: str


class HigherChartsCautionOut(BaseModel):
    note: str
    charts: list[str] = Field(..., min_length=3, max_length=3)


class VargaRulesOut(BaseModel):
    charts: list[VargaRuleOut]
    choose_by_matter: str = Field(
        ..., description="Section 6.5: pick the chart from the matter of interest"
    )
    method: str = Field(..., description="Section 6.5's find-the-links procedure")
    key_to_analysis: str
    analysis_patterns: list[AnalysisPatternOut] = Field(
        ..., min_length=2, max_length=2, description="Section 6.5's two worked patterns"
    )
    planes: list[VargaPlaneOut] = Field(
        ..., min_length=4, max_length=4, description="Section 6.4's four planes"
    )
    higher_charts_caution: HigherChartsCautionOut
    groups: dict[str, list[str]] = Field(..., description="The four groups of section 6.6")
    amsa_names: dict[str, dict[str, str]] = Field(
        ..., description="Amsa by count of strong charts, keyed by group"
    )
    generic: str
    note: str


class AmsabalaIn(BaseModel):
    longitude: str | float = Field(..., examples=["10 Ar 00", 10.0])
    graha: int = Field(..., ge=0, le=8, description="0 = Sun .. 8 = Ketu")


class StrongChartOut(BaseModel):
    chart: str
    rasi_name: str
    dignity: str = Field(..., description="moolatrikona, own or exalted")


class AmsaGroupOut(BaseModel):
    charts_in_group: int
    strong_in: list[StrongChartOut]
    count: int
    amsa: str | None = Field(
        None, description="Null below a count of two, which the book does not name"
    )


class AmsabalaOut(BaseModel):
    graha: int
    graha_name: str
    input: VargaInputOut
    groups: dict[str, AmsaGroupOut]


class MatterChartOut(BaseModel):
    chart: str = Field(..., examples=["D10"])
    name: str
    divisions: int
    signifies: str
    cautioned: bool = Field(
        ...,
        description=(
            "True for D-40, D-45 and D-60. Footnote 12 advises leaving these "
            "higher charts until a competent guru is found — a caution about "
            "interpretation, not about the arithmetic, which is computed "
            "either way."
        ),
    )


class MatterOut(BaseModel):
    matter: str
    charts: list[MatterChartOut]
    method: str
    no_match_note: str
