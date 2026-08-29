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
    summed: dict = Field(
        description="The supplied tables added sign by sign. Not called a "
                    "sarvashtakavarga: the book has not reached that term, "
                    "and the seven-planet and eight-reference sums differ "
                    "(337 against 386 when complete). Both are returned.",
    )
    tables_pending: list[str]


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
