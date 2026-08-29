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
    naming_warning: str = Field(
        description="Footnote 42's trap: PVR's bindu and rekha are the "
                    "reverse of common modern usage.",
    )
    worked_reading: str
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
        description="Partial until all eight tables are supplied, and it says "
                    "so rather than passing a partial sum off as a total.",
    )
    tables_pending: list[str]
