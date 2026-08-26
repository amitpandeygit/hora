"""Models for the strength and avastha endpoints — book chapter 15."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ChartIn(BaseModel):
    """Graha longitudes. Avasthas need nothing finer."""

    graha_longitudes: dict[int, float] = Field(
        ...,
        description="Graha id -> sidereal longitude in degrees",
        examples=[{0: 12.5, 1: 100.2, 2: 220.8, 3: 15.0, 4: 250.4, 5: 40.1,
                   6: 310.7, 7: 95.3, 8: 275.3}],
    )


class AvasthaIn(ChartIn):
    graha: int = Field(..., ge=0, le=8, description="0 = Sun")
    house: int | None = Field(
        None, ge=1, le=12,
        description="The house the graha occupies. Needed by Lajjita only.",
    )
    aspected_by: list[int] | None = Field(
        None,
        description=(
            "Grahas aspecting this one. This engine does not compute aspects "
            "(see docs/open-items.md OI-18), so four mood states stay "
            "undetermined unless this is supplied."
        ),
    )
    close_orb: float | None = Field(
        None, gt=0, le=30,
        description=(
            'Degrees for Kopita\'s "joined closely by Sun". The book does not '
            "quantify \"closely\"; without this, same-rasi is used."
        ),
    )


class AgeAvasthaOut(BaseModel):
    name: str = Field(..., examples=["Kumaara"])
    meaning: str = Field(..., examples=["Adolescent"])
    results: str = Field(..., examples=["Half"])
    fraction: float | None = Field(
        None,
        description=(
            'The results as a number, where the book gives one. Vriddha\'s is '
            '"Some", which is not a quantity, so it is null rather than an '
            "invented value."
        ),
    )
    rasi: int
    rasi_name: str
    rasi_is_odd: bool = Field(
        ..., description="Odd and even rasis run Table 35's bands in opposite directions"
    )
    degrees_in_rasi: float
    band: list[float] = Field(..., description="The band this state occupies")
    caution: str = Field(..., description="Section 15.4.1's closing caution")


class AlertnessAvasthaOut(BaseModel):
    name: str = Field(..., examples=["Jaagrita"])
    meaning: str = Field(..., examples=["awake"])
    results: str = Field(..., examples=["full", "medium", "negligible"])
    when: str
    basis: str = Field(..., description="What the relationship to the rasi was judged to be")


class MoodAvasthaOut(BaseModel):
    name: str
    meaning: str
    when: str
    applies: bool | None = Field(
        None,
        description=(
            "null means the condition could not be decided from the inputs "
            "given. It is never collapsed to false."
        ),
    )
    reason: str
    additional: bool = Field(
        ..., description="True for the six additional states of section 15.4.3"
    )


class AvasthaOut(BaseModel):
    graha: int
    graha_name: str
    age: AgeAvasthaOut
    alertness: AlertnessAvasthaOut
    mood: list[MoodAvasthaOut]
    in_mood: list[str] = Field(..., description="Names of the states that apply")
    undetermined: list[str] = Field(
        ..., description="Names of the states that could not be decided"
    )


class CompareIn(ChartIn):
    left: int = Field(..., ge=0, le=8)
    right: int = Field(..., ge=0, le=8)


class AxisVerdictOut(BaseModel):
    axis: str = Field(..., examples=["age", "alertness"])
    winner: int | None
    winner_name: str | None
    left: str
    right: str
    determined: bool
    reason: str


class ComparisonOut(BaseModel):
    left: int
    left_name: str
    right: int
    right_name: str
    axes: list[AxisVerdictOut]
    winner: int | None = Field(
        None, description="Set only when every deciding axis agrees"
    )
    winner_name: str | None
    determined: bool
    reason: str
    caveat: str = Field(
        ...,
        description=(
            "The measure the book nominates for this comparison is not "
            "available. Always present."
        ),
    )


class MeasureOut(BaseModel):
    key: str
    name: str
    shows: str
    used_for: str
    available: bool
    why_not: str | None
    note: str | None


class MeasuresOut(BaseModel):
    measures: list[MeasureOut]
    caveat: str


class AgeRowOut(BaseModel):
    name: str
    meaning: str
    results: str
    fraction: float | None
    odd_rasi: list[float]
    even_rasi: list[float]


class AgeTableOut(BaseModel):
    table: str
    rows: list[AgeRowOut]
    caution: str


class AlertnessRuleOut(BaseModel):
    name: str
    meaning: str
    results: str
    when: str


class MoodRuleOut(BaseModel):
    name: str
    meaning: str
    when: str
    needs: list[str]
    additional: bool


class EffectOut(BaseModel):
    avastha: str
    house: int | None = None
    effect: str


class AvasthaRulesOut(BaseModel):
    section: str
    age: AgeTableOut
    alertness: list[AlertnessRuleOut]
    mood: list[MoodRuleOut]
    effects: list[EffectOut]
    activity: ActivityRulesOut


# --------------------------------------------------------------------------
# 15.4.4 — states related to activity (sayanaadi avasthas)
#
# UNVERIFIED against the book. See docs/open-items.md OI-26.
# --------------------------------------------------------------------------


class ActivityIn(BaseModel):
    """The six terms of section 15.4.4's formula, as inputs."""

    graha: int = Field(..., ge=0, le=8, description="0 = Sun. The book's P is this + 1.")
    graha_longitude: float = Field(
        ..., description="Sidereal longitude; supplies C and A"
    )
    moon_longitude: float = Field(..., description="Supplies M")
    lagna_rasi: int = Field(
        ..., ge=0, le=11, description="0 = Aries. The book's L is this + 1."
    )
    ghati: int = Field(
        ..., ge=1, le=60, description="The ghati running at birth; supplies G"
    )
    name_sound: int | str | None = Field(
        None,
        description=(
            "Table 37's number (1-5), or a syllable to look up. Prefer the "
            "Devanagari letter: the book's Roman column is ambiguous. Without "
            "it the strength of the activity is null, not guessed."
        ),
        examples=[1, "\u0915"],
    )


class ActivityTermOut(BaseModel):
    symbol: str = Field(..., examples=["C", "P", "A", "M", "G", "L"])
    name: str
    text: str = Field(..., description="The term as section 15.4.4 defines it")
    value: int


class ActivityStepOut(BaseModel):
    number: int = Field(..., ge=1, le=9)
    name: str
    description: str
    value: int | None = None
    detail: str | None = None


class ActivityOut(BaseModel):
    graha: int
    graha_name: str
    formula: str = Field(..., examples=["((C x P x A) + M + G + L) mod 12"])
    terms: list[ActivityTermOut]
    index: int = Field(..., ge=1, le=12)
    name: str = Field(..., examples=["Sayana"])
    meaning: str = Field(..., examples=["Lying down, resting"])
    aliases: list[str]
    sound_number: int | None = Field(None, ge=1, le=5)
    strength: str | None = Field(
        None, description="Null when no name sound was given",
        examples=["cheshta", "drishti", "vicheshta"],
    )
    strength_results: str | None = Field(None, examples=["full", "medium"])
    strength_remainder: int | None = Field(None, ge=0, le=2)
    steps: list[ActivityStepOut]


class GhatiIn(BaseModel):
    hours_after_sunrise: float = Field(..., ge=0, le=24)


class GhatiOut(BaseModel):
    hours_after_sunrise: float
    ghatis_per_hour: float
    ghati: int = Field(..., ge=1, le=61)
    note: str


class SoundIn(BaseModel):
    syllable: str = Field(
        ..., min_length=1, max_length=8,
        description="A Devanagari letter, or a Roman syllable from Table 37",
    )


class SoundOut(BaseModel):
    syllable: str
    sound_number: int = Field(..., ge=1, le=5)


class SayanaadiStateOut(BaseModel):
    index: int
    name: str
    meaning: str
    aliases: list[str]


class SoundNumberRowOut(BaseModel):
    number: int
    devanagari: list[str]
    roman: str


class ActivityStrengthRowOut(BaseModel):
    remainder: int
    name: str
    results: str


class ActivityTermRuleOut(BaseModel):
    symbol: str
    name: str
    text: str
    range: list[int]


class ActivityRulesOut(BaseModel):
    most_important: str = Field(
        ..., description="Section 15.4.4 ranks this family above the other three"
    )
    formula: str
    terms: list[ActivityTermRuleOut]
    states: list[SayanaadiStateOut]
    sound_numbers: list[SoundNumberRowOut]
    strength: list[ActivityStrengthRowOut]
    vicheshta_remainder_note: str
    navamsa_index_note: str
    ghati_note: str
    ghatis_per_hour: float
    verified: bool = Field(
        ..., description="Tables 36 and 37 and the formula match the book"
    )
    verification_note: str
    footnotes_verified: bool = Field(
        ..., description="Footnotes 51 and 52 match the book"
    )


class ActivityResultsIn(BaseModel):
    """A sayanaadi avastha plus what is known about the graha's placement.

    Every placement field is optional. Omitting one makes any clause that
    needs it *undetermined*, never false.
    """

    avastha: int = Field(..., ge=1, le=12, description="Table 36 index")
    graha: int = Field(..., ge=0, le=8)
    house: int | None = Field(None, ge=1, le=12)
    rasi: int | None = Field(None, ge=0, le=11)
    joined_by: list[int] | None = Field(
        None, description="Grahas sharing the rasi"
    )
    moon_phase: str | None = Field(None, examples=["waxing", "waning"])
    dignity: str | None = Field(None, examples=["exalted", "own", "friend"])
    associated_with_malefics: bool | None = None
    associated_with_benefics: bool | None = None


class ResolvedResultOut(BaseModel):
    text: str | None = Field(
        None, description="Null when the source's licence is unconfirmed"
    )
    applies: bool | None = Field(
        None, description="Null when an input the condition needs was not given"
    )
    conditional: bool
    reason: str


class ActivityResultsOut(BaseModel):
    avastha: int
    avastha_name: str | None = None
    graha: int
    graha_name: str | None = None
    available: bool = Field(
        ..., description="False when this pair has not been transcribed yet"
    )
    note: str | None = None
    source: str | None = None
    licence_status: str | None = None
    text_withheld: bool = False
    verbatim: str | None = None
    transcription_notes: str | None = None
    results: list[ResolvedResultOut]
    applies_count: int = 0
    undetermined_count: int = 0
