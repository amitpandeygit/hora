"""Request and response models for chapter 12's ashtakavarga endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AshtakavargaChartIn(BaseModel):
    """All eight reference points. None may be omitted — a missing one would
    silently cost the chart up to twelve rekhas."""

    reference_signs: dict[str, int] = Field(
        ...,
        description=("Each of Sun, Moon, Mars, Mercury, Jupiter, Venus, "
                     "Saturn and Lagna to its sign, 0 = Aries."),
        examples=[{"Sun": 7, "Moon": 2, "Mars": 9, "Mercury": 8,
                   "Jupiter": 6, "Venus": 6, "Saturn": 6, "Lagna": 6}],
    )
    owner: str | None = Field(
        None, examples=["Sun"],
        description="One table by name; omit for every table that exists.",
    )


class AshtakavargaEntryOut(BaseModel):
    value: int
    term: str = Field(description="PVR's word for this entry — see the "
                                  "naming warning.")
    sanskrit: str


class AshtakavargaRulesOut(BaseModel):
    intro: str
    means: str
    reference_point_note: str
    all_planets_are_references: str
    purpose: str
    references: list[str]
    table_numbers: dict[str, int]
    tables_available: list[str]
    tables_verified: dict[str, dict]
    classical_totals_provenance: str = Field(
        description="Where the totals used to check the "
                    "transcription come from — not this book.",
    )
    tables_verified_note: str
    tables_pending: list[str] = Field(
        description="Tables the book names that have not been supplied. A "
                    "missing table is never treated as an empty one.",
    )
    tables_pending_note: str
    notation: str
    benefic_entry: AshtakavargaEntryOut
    malefic_entry: AshtakavargaEntryOut
    bindu_rekha_footnote: str
    bav_definition: str
    bhinna_means: str
    abbreviations: dict[str, str]
    bav_grading: str
    bav_count_range: list[int]
    bav_count_is_called_rekhas: str
    bav_grades: dict[str, str] = Field(
        description="Section 12.3's grade for each possible count, 0 to 8.",
    )
    bav_grade_counts: dict[str, list[int]]
    bav_grade_names: list[str] = Field(
        description="The book's own spelling of the three "
                    "grades, kept rather than anglicised.",
    )
    bav_applies_to_transits: str
    bav_naming_agrees_with_footnote_42: str
    naming_warning: str = Field(
        description="Footnote 42's trap: PVR's bindu and rekha are the "
                    "reverse of common modern usage.",
    )
    worked_reading: str
    example_37: dict
    example_38: dict
    exercise_18: dict
    exercise_19: dict
    exercise_20: dict
    exercise_21: dict
    prastaara: dict
    example_39: dict
    chart_3: dict
    chart_12: dict
    sav_definition: str
    samudaaya_means: str
    sarva_means: str
    sav_is_seven_planets: str = Field(
        description="The sentence that settles what the SAV sums.",
    )
    sav_owners: list[str]
    sav_excludes: list[str]
    sav_total: int
    sav_worked_example: str
    sav_strength_rule: str
    sav_grade_bands: dict[str, str]
    sav_grade_names: list[str]
    sav_overlap_note: str = Field(
        description="Why 30 is read as strong. See docs/book-deviations.md "
                    "D-40.",
    )
    sav_muhurta_rule: str
    sav_muhurta_positions: list[str]
    muhurta_footnote: str
    muhurta_definition: str
    not_only_rasi: str
    in_divisional_charts: str
    tables_are_the_same: str = Field(
        description="Section 12.5: the eight tables do not change from chart "
                    "to chart.",
    )
    divisional_example: dict
    divisional_note: str
    sodhya_pinda_where_defined: str = Field(
        description="A second family of principles section 12.5 names and "
                    "nothing read so far defines. See OI-101.",
    )
    yuga_footnote: str
    yugas: list[dict]


class AshtakavargaTableOut(BaseModel):
    owner: str
    owner_graha: int | None
    owner_graha_name: str | None
    table: int
    references: list[str]
    rows: list[dict] = Field(
        description="Twelve rows, one per house, in the orientation the book "
                    "prints the table.",
    )
    benefic_houses: dict[str, list[int]] = Field(
        description="The column view, derived from the rows rather than "
                    "transcribed a second time.",
    )
    rekhas_per_reference: dict[str, int]
    total: int


class AshtakavargaChartOut(BaseModel):
    reference_signs: dict[str, dict]
    bhinnashtakavarga: list[dict]
    sarvashtakavarga: dict = Field(
        description="Section 12.4's SAV: the seven planets' BAVs summed sign "
                    "by sign, with lagna's table excluded.",
    )
    summed: dict = Field(
        description="The supplied tables added sign by sign. Not called a "
                    "sarvashtakavarga: the book has not reached that term, "
                    "and the seven-planet and eight-reference sums differ "
                    "(337 against 386 when complete). Both are returned.",
    )
    tables_pending: list[str]
    chart: str = Field(
        "D1", description="Which chart the signs came from.",
    )
    chart_note: str | None = Field(
        None, description="Set when the signs were resolved from longitudes "
                          "into a divisional chart — see section 12.5.",
    )
    reference_longitudes: dict[str, float] | None = Field(
        None, description="Echoed back when the request supplied them.",
    )


class BeneficRasisIn(BaseModel):
    """Section 12.2's Example 37 and Exercise 18: where is one planet benefic
    with respect to each reference point?"""

    owner: str = Field(..., examples=["Mercury"],
                       description="Whose ashtakavarga to read.")
    reference_signs: dict[str, int] = Field(
        ...,
        description="All eight reference points to their signs, 0 = Aries.",
        examples=[{"Sun": 2, "Moon": 11, "Mars": 2, "Mercury": 2,
                   "Jupiter": 4, "Venus": 0, "Saturn": 4, "Lagna": 5}],
    )


class BeneficRasisOut(BaseModel):
    owner: str
    table: int
    reference_signs: dict[str, dict]
    benefic_rasis: list[dict] = Field(
        description="Per reference: the benefic houses from the owner's "
                    "table, and the rasis they land in once counted from "
                    "where that reference sits.",
    )


class MuhurtaIn(BaseModel):
    """Section 12.4's muhurta rule. The SAV is the natal chart's; the signs
    looked up in it are the muhurta chart's."""

    natal_reference_signs: dict[str, int] = Field(
        ..., description="The natal chart's eight reference points.",
        examples=[{"Sun": 2, "Moon": 11, "Mars": 2, "Mercury": 2,
                   "Jupiter": 4, "Venus": 0, "Saturn": 4, "Lagna": 5}],
    )
    muhurta_signs: dict[str, int] = Field(
        ..., description="The muhurta chart's Lagna, Moon and Sun signs.",
        examples=[{"Lagna": 0, "Moon": 6, "Sun": 9}],
    )


class MuhurtaOut(BaseModel):
    rule: str
    favorable_from: int
    positions: list[dict]
    all_favorable: bool
    natal_sav: list[int]
    footnote: str
    muhurta_definition: str


class DivisionalIn(BaseModel):
    """Section 12.5: the same eight tables applied to a divisional chart."""

    reference_longitudes: dict[str, float] = Field(
        ...,
        description="All eight reference points to sidereal longitudes.",
        examples=[{"Sun": 73.27, "Moon": 340.55, "Mars": 73.55,
                   "Mercury": 87.67, "Jupiter": 140.10, "Venus": 27.67,
                   "Saturn": 146.43, "Lagna": 174.32}],
    )
    chart: str = Field("D1", examples=["D12"],
                       description="A varga code; D1 is the rasi chart.")
    owner: str | None = Field(None, examples=["Mercury"])


class PrastaaraIn(BaseModel):
    """§12.6. `rasi` and `references` are the transit question; without them
    the response is Table 27's grid alone."""

    owner: str = Field(..., examples=["Mercury"])
    reference_signs: dict[str, int] = Field(..., examples=[{
        "Sun": 2, "Moon": 11, "Mars": 2, "Mercury": 2,
        "Jupiter": 4, "Venus": 0, "Saturn": 4, "Lagna": 5}])
    rasi: int | None = Field(None, ge=0, le=11, examples=[1])
    references: list[str] | None = Field(None, examples=[["Venus"]])


class PrastaaraOut(BaseModel):
    owner: str
    table: int
    means: str
    purpose: str
    rows: list[dict]
    rekhas: list[int]
    rekhas_note: str
    benefic_from: list[dict]
    representations: list[str]
    asked: dict | None = None
