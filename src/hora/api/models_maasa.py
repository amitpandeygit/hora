"""Models for the lunar month endpoints — book §1.3.8.2."""
from __future__ import annotations

from pydantic import BaseModel, Field


class MaasaIn(BaseModel):
    """One longitude, and optionally which of a Nija/Adhika pair this is."""

    conjunction_longitude: float = Field(
        ...,
        description=(
            "Sidereal longitude of the Sun-Moon conjunction that starts the "
            "month; wrapped into 0-360. Footnote 2 defines conjunction as "
            "exactly the same longitude, so there is one value to give."
        ),
        examples=[345.0],
    )
    qualifier: str | None = Field(
        None,
        description=(
            'Either "Nija" (real) or "Adhika" (extra), when the caller has '
            "already established that this rasi carries two conjunctions. "
            "Never inferred: section 1.3.8.2 does not say which of a pair is "
            "which."
        ),
        examples=["Adhika"],
    )


class MaasaPairIn(BaseModel):
    """Two conjunctions that fall in the same rasi."""

    first_longitude: float = Field(..., examples=[30.383333333333333])
    second_longitude: float = Field(..., examples=[58.483333333333334])


class MaasaStepOut(BaseModel):
    number: int = Field(..., ge=1, le=3)
    description: str = Field(..., description="The step as section 1.3.8.2 states it")
    detail: str = Field(..., description="This conjunction's working, in words")
    value: str


class MaasaOut(BaseModel):
    conjunction_longitude: float
    conjunction_rasi: int = Field(..., ge=0, le=11)
    conjunction_rasi_name: str = Field(..., examples=["Pisces"])
    index: int = Field(..., ge=1, le=12, description="1 is Chaitra, 12 Phaalguna")
    name: str = Field(..., description="Common transliteration", examples=["Chaitra"])
    name_book: str = Field(
        ..., description="Table 4's own spelling", examples=["Chaitra"]
    )
    full_name: str = Field(
        ...,
        description='Qualifier first when there is one — "Adhika Jyeshtha"',
        examples=["Chaitra"],
    )
    qualifier: str | None = None
    full_moon_nakshatra: str = Field(
        ...,
        description=(
            "Table 4 column 3, the constellation Moon is most likely to occupy "
            "on the full Moon day. Transcribed, not derived: Aaswayuja's is "
            "Aswini, which is not a variant of the month name."
        ),
        examples=["Chitra"],
    )
    approximate_gregorian: str = Field(
        ...,
        description="Table 4 column 4. Indicative only; drifts with adhika maasas",
        examples=["Mar/Apr"],
    )
    steps: list[MaasaStepOut]


class MaasaPairOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str = Field(..., examples=["Taurus"])
    month_name: str = Field(..., examples=["Jyeshtha"])
    months: list[MaasaOut] = Field(..., min_length=2, max_length=2)
    qualifiers: list[str]
    qualifier_meanings: dict[str, str]
    qualifier_undecided: str = Field(
        ..., description="Why neither month in the pair is labelled"
    )


class Table4RowOut(BaseModel):
    conjunction_rasi: int = Field(..., ge=0, le=11)
    conjunction_rasi_name: str
    month_name: str
    month_name_simple: str
    full_moon_nakshatra: str
    approximate_gregorian: str


class MaasaRulesOut(BaseModel):
    section: str = Field(..., examples=["1.3.8.2"])
    title: str
    definition: str
    naming_rule: str
    naming_origin: str
    maasa_meaning: str
    month_length_days: list[int]
    conjunction_definition: str
    conjunction_approximate_note: str
    solar_year_days: float
    lunar_year_days: int
    adhika_interval_years: int
    adhika_rule: str
    qualifiers: dict[str, str]
    table_4: list[Table4RowOut] = Field(..., min_length=12, max_length=12)
