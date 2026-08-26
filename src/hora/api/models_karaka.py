"""Models for the karaka endpoints — book chapter 8."""
from __future__ import annotations

from pydantic import BaseModel, Field

# --------------------------------------------------------------------------
# Shared
# --------------------------------------------------------------------------


class DegreesOut(BaseModel):
    """An arc, in the units chapter 8's tie rule is stated in.

    §8.2: "If two planets have the same degrees, we should compare minutes.
    If minutes are same, we should compare the seconds."
    """

    decimal: float = Field(..., description="Degrees as a float, 0 to 30")
    degrees: int
    minutes: int
    seconds: int
    formatted: str = Field(..., examples=["28°17'00\""])


# --------------------------------------------------------------------------
# Chara karakas
# --------------------------------------------------------------------------


class CharaKarakaIn(BaseModel):
    """Sidereal longitudes for the eight grahas of section 8.2.

    Keys are Graha ids as strings (JSON object keys); values are degrees.
    Ketu is rejected rather than ignored — 8.1 excludes it from chara karakas
    on purpose, and silently dropping it would hide a caller's misreading.
    """

    longitudes: dict[int, float] = Field(
        ...,
        description=(
            "Graha id -> sidereal longitude in degrees. Exactly the eight "
            "grahas of section 8.2: the seven classical plus Rahu."
        ),
        examples=[{0: 72.783, 1: 20.467, 2: 73.85, 3: 85.3,
                   4: 35.667, 5: 77.35, 6: 32.467, 7: 91.717}],
    )


class CharaKarakaOut(BaseModel):
    order: int = Field(..., ge=1, le=8, description="1 = highest advancement")
    symbol: str = Field(..., examples=["AK", "AmK", "DK"])
    symbol_aliases: list[str] = Field(
        default_factory=list, description='GK is also written "JK"'
    )
    name: str
    name_aliases: list[str] = Field(default_factory=list)
    shows: str
    note: str | None = Field(
        None, description="Extra meanings from the Table 13 footnotes"
    )
    graha: int
    graha_name: str
    rasi: int
    rasi_name: str
    advancement: DegreesOut
    measured_from_end_of_rasi: bool = Field(
        ..., description="True for Rahu only — section 8.2 step 1"
    )
    shares_karakatwa: bool = Field(
        ...,
        description=(
            "True when another graha is at exactly the same longitude. Both "
            "hold the karakatwa together and the next has no ruler; section "
            "8.2 says to use the corresponding sthira karaka instead."
        ),
    )


class CharaKarakasOut(BaseModel):
    kind: str = "chara"
    presiding: str = Field(..., examples=["Vishnu"])
    used_for: str
    read_as: str = Field(
        ..., examples=["karaka_himself"],
        description=(
            'Section 8.3: "We do not take the 7th from DK for spouse, but DK '
            'himself shows spouse."'
        ),
    )
    read_as_note: str
    shared_karakatwa_note: str = Field(
        ...,
        description=(
            "What section 8.2 says to do when two grahas share a longitude, "
            "and how often that happens"
        ),
    )
    karakas: list[CharaKarakaOut]


# --------------------------------------------------------------------------
# Sthira karakas
# --------------------------------------------------------------------------


class SthiraKarakaOut(BaseModel):
    relative: str
    grahas: list[int] = Field(
        ..., description="Two grahas when the rule is 'stronger', otherwise one"
    )
    graha_names: list[str]
    rule: str = Field(..., examples=["fixed", "stronger"])
    note: str | None


class SpouseKarakaOut(BaseModel):
    graha: int
    graha_name: str


class SthiraSpouseOut(BaseModel):
    female: SpouseKarakaOut
    male: SpouseKarakaOut
    note: str


class SthiraKarakasOut(BaseModel):
    kind: str = "sthira"
    presiding: str = Field(..., examples=["Shiva"])
    used_for: str
    name_explained: str = Field(
        ...,
        description=(
            'Footnote 21 links the name to the function: "sthira" means fixed, '
            "and death is life becoming fixed."
        ),
    )
    read_as: str = Field(..., examples=["karaka_himself"])
    read_as_note: str
    strength_comparison_defined_in: str = Field(
        ...,
        description=(
            "Father and mother go to the stronger of two grahas. Footnote 26 "
            "defers that comparison to a later chapter, so those two rows "
            "cannot be resolved from chapter 8 alone."
        ),
    )
    karakas: list[SthiraKarakaOut]
    spouse: SthiraSpouseOut


# --------------------------------------------------------------------------
# Naisargika karakas
# --------------------------------------------------------------------------


class NaisargikaPrimaryOut(BaseModel):
    house: int = Field(..., ge=1, le=12)
    graha: int
    graha_name: str
    signifies: str


class SignificationOut(BaseModel):
    house: int = Field(..., ge=1, le=12)
    matters: str


class NaisargikaByGrahaOut(BaseModel):
    graha: int
    graha_name: str
    significations: list[SignificationOut]


class NaisargikaExampleOut(BaseModel):
    """One of section 8.4's worked readings: the Nth house from a graha."""

    house: int = Field(..., ge=1, le=12)
    graha: int
    graha_name: str
    shows: str
    table: int = Field(..., description="Which table the reading comes from, 15 or 16")


class NaisargikaKarakasOut(BaseModel):
    kind: str = "naisargika"
    presiding: str = Field(..., examples=["Brahma"])
    used_for: str
    counted_from_the_graha: bool = Field(
        ...,
        description=(
            "Table 15 gives the Nth house *from the karaka*, not the Nth house "
            'of the chart: "the 4th house from Moon shows mother".'
        ),
    )
    read_as: str = Field(..., examples=["house_from_karaka"])
    read_as_note: str
    primary: list[NaisargikaPrimaryOut] = Field(..., description="Table 15")
    by_graha: list[NaisargikaByGrahaOut] = Field(..., description="Table 16")
    definition: str | None = Field(
        None, description="Section 8.4's own definition of a naisargika karaka"
    )
    used_in: str | None = Field(
        None, description="Where section 8.4 says these significations are used"
    )
    table_16_source: str | None = Field(
        None,
        description=(
            "Table 16 is compiled from the classics, where Table 15 is the "
            "chapter's own primary list. The two do not carry the same weight "
            "when a source has to be ranked."
        ),
    )
    table_16_rule: str | None = Field(
        None,
        description=(
            "How Table 16 is read: a matter shared by a graha and a house is "
            'read at that house counted from that graha — "Mercury and 5th '
            'house show memory and so the 5th house from Mercury shows memory".'
        ),
    )
    worked_examples: list[NaisargikaExampleOut] = Field(
        default_factory=list,
        description="Section 8.4's own three readings, with the table each comes from",
    )


# --------------------------------------------------------------------------
# All three kinds
# --------------------------------------------------------------------------


class KarakaExclusionOut(BaseModel):
    graha: int
    graha_name: str
    reason: str


class KarakaKindOut(BaseModel):
    key: str = Field(..., examples=["chara", "sthira", "naisargika"])
    name: str
    gloss: str
    count: int
    presiding: str
    grahas: list[int]
    graha_names: list[str]
    shows: str
    shows_broadly: str | None = Field(
        None,
        description=(
            "Section 8.1's wider statement of the same scope, where it gives "
            "one. Chara karakas show 'people who play a role in one's life' "
            "before the section narrows them to sustenance and achievements."
        ),
    )
    shows_contrast: str | None = Field(
        None,
        description=(
            "What section 8.1 says the kind is *not* limited to. Naisargika "
            "karakas show 'not only human beings' — the contrast that "
            "separates them from chara karakas."
        ),
    )
    not_limited_to: str | None = None
    presiding_because: str = Field(
        ..., description="Why that deity presides, as section 8.1 gives it"
    )
    used_for: str
    read_as: str = Field(
        ...,
        examples=["karaka_himself", "house_from_karaka"],
        description=(
            "Whether the karaka itself shows the matter, or a house counted "
            "from it does. Section 8.3 turns on this distinction."
        ),
    )
    read_as_note: str
    examples: list[str] = Field(
        default_factory=list, description="Section 8.1's examples, where it gives any"
    )
    also_shows: str | None = None
    excludes: list[KarakaExclusionOut]


class GrahaRefOut(BaseModel):
    """A graha named by id and name, with nothing else attached."""

    graha: int
    graha_name: str


class CharaTableRowOut(BaseModel):
    order: int = Field(..., ge=1, le=8)
    symbol: str
    symbol_aliases: list[str]
    name: str
    shows: str
    note: str | None
    advancement: str | None = Field(
        None,
        description=(
            "Table 13's first column, which labels only the two extreme rows: "
            "'Highest' for AK and 'Lowest' for DK. The label is on the "
            "advancement, not on the karaka."
        ),
        examples=["Highest", "Lowest"],
    )


class UsageRuleOut(BaseModel):
    """One of section 8.3's explicit corrections."""

    rule: str
    wrong: str
    right: str
    because: str


class ChoosingOut(BaseModel):
    """Section 8.4's worked comparison: same matter, different question."""

    matter: str
    question: str
    kind: str = Field(..., examples=["naisargika", "chara", "sthira"])
    use: str


class KarakaKindsOut(BaseModel):
    definition: str = Field(
        ..., description="Section 8.1's definition of a karaka, in full"
    )
    word: str = Field("karaka", description="The Sanskrit term this chapter defines")
    meaning: str = Field(..., examples=["one who causes"])
    pronounced: str = Field(
        ..., description="Footnote 20 spells out the pronunciation",
        examples=["kaaraka"],
    )
    warning: str = Field(
        ..., description="Section 8.1's instruction not to mix the three kinds"
    )
    jnaati_pronunciation: str = Field(..., description="Footnote 24 in full")
    kinds: list[KarakaKindOut]
    usage_rules: list[UsageRuleOut] = Field(
        ..., description="Section 8.3's named mistakes and what to use instead"
    )
    choosing: list[ChoosingOut] = Field(
        ...,
        description=(
            "Section 8.4 worked through children: which kind answers which "
            "question about the same matter"
        ),
    )
    chara_table: list[CharaTableRowOut] = Field(..., description="Table 13")
    chara_procedure: list[str] = Field(
        default_factory=list,
        description=(
            "Section 8.2's three steps for finding the chara karakas, as "
            "printed. The rule the engine applies, published rather than left "
            "to be inferred from the output."
        ),
    )
    chara_tie_break: str | None = Field(
        None,
        description=(
            "Section 8.2 on close advancements: compare degrees, then "
            "minutes, then seconds."
        ),
    )
    shared_karakatwa: str | None = Field(
        None,
        description=(
            "What section 8.2 says to do when two grahas share an exact "
            "longitude, and how rare it says that is."
        ),
    )
    measured_from_end_of_rasi: list[GrahaRefOut] = Field(
        default_factory=list,
        description=(
            "Grahas whose advancement is measured from the end of the rasi "
            "rather than its beginning. Section 8.2 step 1 names only Rahu."
        ),
    )
