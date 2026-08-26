"""Response models for the reference tables and editorial content.

Separate from :mod:`hora.api.models` because these publish book tables rather
than computed results: they change when a chapter is transcribed, not when an
algorithm changes.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class NotationOut(BaseModel):
    """One longitude in every notation the book uses."""

    input: str
    degrees: float
    sign_dm: str
    rasi_dm: str
    rasi: int
    rasi_name: str
    degrees_in_rasi: float
    dms: str


class NakshatraRowOut(BaseModel):
    index: int
    number: int
    name: str
    name_standard: str
    starts: float
    ends: float
    vimsottari_lord: int
    vimsottari_lord_name: str
    deity: str = Field(..., description="Table 2's ruling deity")


class NakshatraTableOut(BaseModel):
    span_degrees: float
    nakshatras: list[NakshatraRowOut]


class TithiRowOut(BaseModel):
    number: int
    name: str
    name_standard: str
    paksha: int
    paksha_name: str
    lord: int
    lord_name: str
    alternate_names: list[str] = Field(
        ..., description='Table 3 gives some tithis several names'
    )
    paksha_synonyms: list[str] = Field(
        ..., description='Sukla is also Suddha; Krishna is also Bahula'
    )


class TithiTableOut(BaseModel):
    tithis: list[TithiRowOut]


class RasiRowOut(BaseModel):
    """Every rasi attribute from book chapter 2."""

    rasi: int
    footed_names: list[str] = Field(
        default_factory=list,
        description='Section 2.2.3 gives three names per half, e.g. '
                    '"odd-footed", "vishamapada", "ojapada"',
    )
    ayana: str = Field(
        ...,
        description='Section 3.2.14: "uttara" or "dakshina", the half-year the rasi falls in',
        examples=["uttara", "dakshina"],
    )
    guna_adjectives: list[str] = Field(
        default_factory=list,
        description='Section 2.2.7\'s adjectival forms, e.g. "saattwik"',
    )
    name: str
    sanskrit: str
    symbol: str
    starts: float
    ends: float
    limb: str
    is_odd: bool
    odd_even_names: list[str] = Field(
        default_factory=list,
        description='Section 2.2.2 gives four names per half, e.g. "odd", '
                    '"vishama", "oja", "male"',
    )
    is_odd_footed: bool
    modality: str
    modality_english: str = Field(..., examples=["movable", "fixed", "dual"])
    modality_deity: str
    modality_deity_role: str = Field(
        ..., description="Section 2.2.4 names each deity by role",
        examples=["Creator", "Destroyer", "Sustainer"],
    )
    modality_nature: str = Field(
        ..., description="Section 2.2.4's stated nature for the modality"
    )
    element: str
    element_sanskrit: str
    element_definition: str = Field(
        ..., description="Section 2.2.5's definition of that element's state"
    )
    dosha: str
    dosha_english: str | None = Field(
        None, description='Section 2.2.6\'s English name; None for "mixed"',
        examples=["bilious", "windy", "phlegmatic"],
    )
    guna: str
    guna_meaning: str = Field(..., examples=["purity", "energy", "darkness"])
    direction: str
    color: str
    strong_at: str
    day_night_names: list[str] = Field(
        default_factory=list, description='Section 2.2.10, e.g. "night time", "nishaa"'
    )
    day_night_governor: int = Field(
        ..., description="Moon governs the nishaa rasis, Sun the divaa rasis"
    )
    rising: str
    rising_description: str
    rising_dasa_half: str | None = Field(
        None,
        description=(
            "Section 2.2.11: seershodaya planets give results in the first "
            "half of their dasa, prishthodaya in the second. Pisces is "
            "ubhayodaya and is given no half."
        ),
        examples=["first", "second"],
    )
    varna: str
    varna_english: str = Field(..., examples=["scholars", "warriors"])
    varna_description: str
    lord: int
    lord_name: str


class Section221Out(BaseModel):
    zodiac_as_vishnu: str
    applies_to_native: str


class Section222Out(BaseModel):
    names: list[list[str]] = Field(..., min_length=2, max_length=2)
    used_for: str


class Section223Out(BaseModel):
    names: list[list[str]] = Field(..., min_length=2, max_length=2)
    used_for: str
    note: str


class ModalityOut(BaseModel):
    modality: str
    english: str
    deity: str
    role: str
    nature: str


class Section224Out(BaseModel):
    modalities: list[ModalityOut] = Field(..., min_length=3, max_length=3)
    trinity_note: str


class Section225Out(BaseModel):
    five_elements: list[str] = Field(..., min_length=5, max_length=5)
    definitions: dict[str, str]
    ether_name: str
    ether_name_sanskrit: str
    ether_in_every_rasi: str
    elements_underlie_everything: str


class HumourOut(BaseModel):
    dosha: str
    english: str | None = None
    elements: list[str] | None = None
    shows: str | None = None
    body_example: str | None = None


class Section226Out(BaseModel):
    ayurveda_note: str
    humours: list[HumourOut] = Field(..., min_length=4, max_length=4)
    note: str


class GunaOut(BaseModel):
    guna: str
    alternate_name: str | None = None
    meaning: str
    effect: str
    adjectives: list[str]


class Section227Out(BaseModel):
    triguna_note: str
    gunas: list[GunaOut] = Field(..., min_length=3, max_length=3)


class DayNightGovernorOut(BaseModel):
    half: str
    graha: int
    graha_name: str


class Section2210Out(BaseModel):
    names: list[list[str]] = Field(..., min_length=2, max_length=2)
    pair_rule: str
    governors: list[DayNightGovernorOut] = Field(..., min_length=2, max_length=2)


class Section2211Out(BaseModel):
    descriptions: list[str] = Field(..., min_length=3, max_length=3)
    dasa_rule: str
    prishthodaya_note: str


class VarnaOut(BaseModel):
    varna: str
    english: str
    description: str
    element: str


class Section2212Out(BaseModel):
    varnas: list[VarnaOut] = Field(..., min_length=4, max_length=4)


class RasiTableOut(BaseModel):
    rasis: list[RasiRowOut]
    section_2_2_1: Section221Out
    section_2_2_2: Section222Out
    section_2_2_3: Section223Out
    section_2_2_4: Section224Out
    section_2_2_5: Section225Out
    section_2_2_6: Section226Out
    section_2_2_7: Section227Out
    section_2_2_10: Section2210Out
    section_2_2_11: Section2211Out
    section_2_2_12: Section2212Out
    deviations: list[str] = Field(
        ..., description="Where the book departs from convention"
    )


class MoolatrikonaOut(BaseModel):
    rasi: str
    from_degree: float
    to_degree: float


class GrahaRowOut(BaseModel):
    """Every graha attribute and dignity from book chapter 3.

    ``None`` means the book gives no value, never that it was not computed.
    """

    id: int
    sanskrit: str
    abbreviation: str
    is_chaayaa_graha: bool = Field(
        ...,
        description=(
            'Section 1.3.1: Rahu and Ketu are the two "chaayaa grahas" (shadow '
            "planets), mathematical points rather than real planets"
        ),
    )
    aliases: list[str] = Field(
        default_factory=list,
        description='"north node" / "head of dragon" and their counterparts',
    )
    avatara_description: str | None = Field(
        None, description="Section 3.2.1's parenthetical, where it gives one",
        examples=["fish", "tortoise", "boar"],
    )
    avatara_aliases: list[str] = Field(
        default_factory=list,
        description="Section 3.2.1's second name for the avatara, where it gives one",
    )
    strong_in_ayana: str | None = Field(
        None,
        description=(
            "The ayana that strengthens this graha — benefics in uttarayana, "
            "malefics in dakshinayana. Null where the book classifies the "
            "graha as neither."
        ),
    )
    element_adjective: str | None = Field(
        None, description='Section 3.2.8\'s "fiery", "ethery" and so on'
    )
    element_tattva: str | None = Field(
        None, description='Section 3.2.8\'s "agni tattva", "aakaasa tattva"'
    )
    name: str
    avatara: str | None = None
    governs: str | None = None
    color: str | None = None
    cabinet_role: str | None = None
    taste_examples: list[str] = Field(
        default_factory=list,
        description="Section 3.2.14's examples; empty for Mercury's mixed taste",
        examples=[["onion", "ginger", "pepper"]],
    )
    dhatu_moola_jeeva_meaning: str | None = Field(
        None, examples=["metals and materials", "roots and vegetables"]
    )
    dig_bala_house: int | None = Field(
        None, ge=1, le=12, description="Section 3.2.15's direction strength house"
    )
    ritu: str | None = Field(
        None, description="Section 3.2.16's season, where the graha rules one",
        examples=["vasanta", "greeshma"],
    )
    shares_element_without_ruling: bool = Field(
        False,
        description=(
            'Section 3.2.8: Sun and Moon "also have the same nature" as Mars '
            "and Venus without ruling those tattvas."
        ),
    )
    element_governance: str | None = Field(
        None, description="Section 3.2.8's clause for the element's ruler",
        examples=["leadership, enterprise"],
    )
    varna_english: str | None = Field(
        None, description="Section 3.2.9's gloss, which differs from 2.2.12's",
        examples=["learned", "worker"],
    )
    varna_forte: str | None = None
    guna_definition: str | None = None
    dhatu_description: str | None = Field(
        None, description="Section 3.2.12 glosses only Venus's dhatu"
    )
    deity: str | None = None
    deity_role: str | None = Field(
        None, description="Section 3.2.6's office for the deity",
        examples=["fire god", "rain god"],
    )
    sex: str | None = None
    natural_nature: str = Field(
        ...,
        description=(
            'Section 3.2.2. "conditional" for Moon and Mercury, whose nature '
            "depends on phase and company respectively — use /v1/graha/nature."
        ),
        examples=["benefic", "malefic", "conditional"],
    )
    element: str | None = None
    rules_element: bool
    varna: str | None = None
    guna: str | None = None
    abode: str | None = Field(None, description="The book gives Mars none")
    dhatu: str | None = None
    time_period: str | None = None
    taste: str | None = None
    dhatu_moola_jeeva: str | None = None
    strong_at: str | None = None
    natural_benefic: bool
    natural_malefic: bool
    digbala_house: int | None = None
    owns: list[str]
    co_lord_only: bool = Field(
        ..., description="True for the nodes: dignity only, never rasi lordship"
    )
    exaltation_rasi: str | None = None
    deep_exaltation_degree: float | None = Field(
        None, description="The book gives the nodes none"
    )
    debilitation_rasi: str | None = None
    moolatrikona: MoolatrikonaOut | None = None
    natural_relations: dict[str, str]


class RituRowOut(BaseModel):
    index: int
    name: str
    meaning: str
    ruler: str


class Section322Out(BaseModel):
    benefic_class_names: list[str] = Field(..., min_length=2, max_length=2)
    malefic_class_names: list[str] = Field(..., min_length=2, max_length=2)
    fixed_benefics: list[int]
    fixed_malefics: list[int]
    conditional: list[int] = Field(..., min_length=2, max_length=2)
    mercury_rule: str
    moon_rule: str
    inherent_nature_note: str


class Section324Out(BaseModel):
    color_use: str


class Section327Out(BaseModel):
    sex_prediction_note: str


class Section328Out(BaseModel):
    note: str
    shares_without_ruling_phrase: str
    shares_without_ruling: list[int] = Field(..., min_length=2, max_length=2)


class Section329Out(BaseModel):
    english_names: list[str] = Field(..., min_length=4, max_length=4)
    fortes: list[str] = Field(..., min_length=4, max_length=4)
    nature_not_caste: str
    cabinet_note: str
    gloss_differs_from_2_2_12: str


class Section3210Out(BaseModel):
    definitions: list[str] = Field(..., min_length=3, max_length=3)
    sattwa_meaning: str
    misconception_note: str


class SectionNoteOut(BaseModel):
    note: str


class Section3212Out(BaseModel):
    name: str
    note: str
    affliction_note: str


class Section3213Out(BaseModel):
    use: str


class Section3214Out(BaseModel):
    use: str
    mercury_has_no_examples: str


class Section3215Out(BaseModel):
    name: str
    note: str
    always_strong_note: str
    strong_at_night: list[int] = Field(..., min_length=3, max_length=3)
    strong_by_day: list[int] = Field(..., min_length=3, max_length=3)
    always_strong: list[int] = Field(..., min_length=1, max_length=1)
    benefic_strong_paksha: str
    malefic_strong_paksha: str
    benefic_strong_ayana: str
    malefic_strong_ayana: str


class RituRulerOut(BaseModel):
    ritu: str
    meaning: str
    lord: int
    lord_name: str


class Section3216Out(BaseModel):
    note: str
    ritus: list[RituRulerOut] = Field(..., min_length=6, max_length=6)


class DhatuMoolaJeevaOut(BaseModel):
    name: str
    meaning: str
    grahas: list[int]


class Section3217Out(BaseModel):
    classes: list[DhatuMoolaJeevaOut] = Field(..., min_length=3, max_length=3)


class Section33Out(BaseModel):
    strong_note: str
    strong_placements: list[str] = Field(..., min_length=3, max_length=3)
    sanskrit_names: dict[str, str]
    analogy: dict[str, str]
    subtle_difference: str


class GrahaTableOut(BaseModel):
    grahas: list[GrahaRowOut]
    ritus: list[RituRowOut]
    section_3_2_14: Section3214Out
    section_3_2_15: Section3215Out
    section_3_2_16: Section3216Out
    section_3_2_17: Section3217Out
    section_3_3: Section33Out
    section_3_2_8: Section328Out
    section_3_2_9: Section329Out
    section_3_2_10: Section3210Out
    section_3_2_11: SectionNoteOut
    section_3_2_12: Section3212Out
    section_3_2_13: Section3213Out
    section_3_2_2: Section322Out
    section_3_2_4: Section324Out
    section_3_2_7: Section327Out
    deviations: list[str]


class NameSchemesOut(BaseModel):
    default: str
    schemes: list[str]
    note: str


class VargaCatalogEntryOut(BaseModel):
    code: str
    name: str
    divisions: int


class VargaCatalogOut(BaseModel):
    named: list[VargaCatalogEntryOut]
    generic: str
    groups: dict[str, list[str]]


class SettingsSchemaOut(BaseModel):
    """Every calculation knob, its default, and its JSON Schema.

    The ``schema`` member is the Pydantic-generated schema of ``Settings``, so
    its internals move with Pydantic rather than with our contract; it is typed
    as a free-form object deliberately.
    """

    defaults: dict[str, object]
    json_schema: dict[str, object] = Field(..., alias="schema")

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


# -- editorial content ------------------------------------------------------


class TermOut(BaseModel):
    term: str
    category: str = Field(
        ..., description="Our editorial tag, not the source author's"
    )


class ContentEntryOut(BaseModel):
    """One source's entry, or a statement of why it is withheld.

    Every key is always present. A withheld entry carries ``reason`` and nulls
    for the text fields; a served entry carries the text and a null ``reason``.
    """

    source: str
    licence_status: str
    term_count: int
    withheld: bool
    reason: str | None = None
    verbatim: str | None = None
    transcription_notes: str | None = None
    terms: list[TermOut] | None = None
    by_category: dict[str, list[str]] | None = None


class RasiContentOut(BaseModel):
    rasi: int
    rasi_name: str
    entries: list[ContentEntryOut]


class AllRasiContentOut(BaseModel):
    subject: str
    rasis: list[RasiContentOut]


class ContentSourcesOut(BaseModel):
    serving_unconfirmed: bool
    sources: dict[str, dict]
    note: str


class YogaRowOut(BaseModel):
    number: int
    index: int
    name: str
    name_standard: str
    means: str = Field(..., description="Table 5's third column")
    starts: float
    ends: float


class YogaTableOut(BaseModel):
    span_degrees: float
    yogas: list[YogaRowOut]


class NaturalRelationTermOut(BaseModel):
    value: int
    label: str
    sanskrit: str


class CompoundRelationTermOut(BaseModel):
    label: str = Field(..., description="The engine's own label")
    sanskrit: str
    gloss: str


class RelationshipTermsOut(BaseModel):
    kinds: dict[str, str]
    natural: list[NaturalRelationTermOut]
    compound: list[CompoundRelationTermOut]
    dignities: dict[str, str]


# --------------------------------------------------------------------------
# Vocabulary that belongs to no single table row
# --------------------------------------------------------------------------


class ZodiacNameOut(BaseModel):
    name: str = Field(..., examples=["nirayana", "sayana"])
    means: str


class ZodiacTermsOut(BaseModel):
    used: str = Field(..., description="The zodiac Hora computes in")
    names: list[ZodiacNameOut]


class PanchangaTermsOut(BaseModel):
    book_spelling: str = Field(..., examples=["Panchaanga"])
    means: str = Field(..., examples=["one with 5 limbs"])
    almanacs_called: str


class ChaayaaGrahaOut(BaseModel):
    id: int
    name: str
    aliases: list[str]


class ChaayaaGrahasOut(BaseModel):
    term: str
    grahas: list[ChaayaaGrahaOut]


class EssenceOut(BaseModel):
    key: str
    name: str
    aliases: list[str]


class PakshaTermOut(BaseModel):
    index: int
    name: str
    synonyms: list[str]
    describes: str


class PurusharthaTermsOut(BaseModel):
    book_spelling: str
    means: str


class UpagrahaAliasOut(BaseModel):
    name: str
    aliases: list[str]


class GrahaTermsOut(BaseModel):
    definition: str = Field(
        ..., description="Section 1.3.1's definition of the word graha"
    )
    note: str = Field(
        ...,
        description=(
            "Why it is not the astronomical sense: the Sun is a star and the "
            "Moon a satellite, and both are grahas"
        ),
    )
    count: int = Field(..., description="Nine, including the two nodes")
    classical_count: int = Field(..., description="Seven, excluding them")


class NodeTermsOut(BaseModel):
    are_mathematical_points: str = Field(
        ...,
        description=(
            "Section 1.3.1 on Rahu and Ketu. The reason they have no disc, no "
            "combustion and no deep-exaltation degree."
        ),
    )


class UpagrahaTermsOut(BaseModel):
    definition: str = Field(..., examples=["moving mathematical points"])
    gloss: str = Field(..., examples=["sub-planets or satellites"])
    count: int = Field(..., description="Eleven")


class LagnaTermsOut(BaseModel):
    definition: str
    special_ascendants_term: str


class SolarCalendarTermsOut(BaseModel):
    year_degrees: float = Field(..., description="360 — a year is 360 deg of Sun")
    month_degrees: float = Field(..., description="30 — a month is 30 deg of Sun")
    day_degrees: float = Field(..., description="1 — a day is 1 deg of Sun")
    days_per_month: int = Field(..., description="Thirty, always")
    definition: str
    used_in: list[str] = Field(..., examples=[["dasas", "Tajaka analysis"]])
    note: str = Field(
        ...,
        description=(
            "Why a solar month is not a fixed number of days: it is defined "
            "by the Sun's motion, and the Sun does not move at a constant rate"
        ),
    )


class NakshatraTermsOut(BaseModel):
    count: int = Field(..., description="27, for every purpose but a few charts")
    span_degrees: float = Field(..., description="360/27 = 13 deg 20 min")
    padas_each: int = Field(..., description="Four quarters per nakshatra")
    pada_span_degrees: float = Field(..., description="3 deg 20 min")
    pada_gloss: str = Field(..., examples=["legs/feet"])
    count_for_special_charts: int = Field(..., description="28, with Abhijit")
    special_charts: list[str] = Field(
        ..., description="The charts section 1.3.6 names as using 28"
    )
    abhijit_rule: str = Field(
        ..., description="Section 1.3.6's exception, verbatim"
    )


class VargaTermsOut(BaseModel):
    sanskrit: str = Field(..., examples=["varga chakra"])
    aliases: list[str] = Field(
        ..., description='Section 1.3.5 also calls them "harmonic charts"'
    )
    definition: str = Field(
        ...,
        description=(
            "The general definition chapter 6 assumes without restating: "
            "divide each rasi into n parts and map each part to a rasi again"
        ),
    )
    signifies: str
    independent_chart_rule: str = Field(
        ...,
        description=(
            "Why houses, arudhas and the rest are taken inside a divisional "
            "chart from that chart's own lagna rather than the rasi lagna"
        ),
    )


class PillarOut(BaseModel):
    number: int = Field(..., ge=1, le=4)
    sanskrit: str
    english: str


class FourPillarsOut(BaseModel):
    statement: str
    pillars: list[PillarOut] = Field(..., description="Section 1.3.5's order")
    conclusion_order: list[str] = Field(
        ..., description="Section 6.7's order, which differs"
    )
    ordering_note: str = Field(
        ...,
        description=(
            "The two orderings cannot both be indexed by number. Recorded "
            "rather than resolved by silently preferring one."
        ),
    )


class TermsOut(BaseModel):
    """Terms the book defines once and uses throughout."""

    solar_calendar: SolarCalendarTermsOut
    nakshatra: NakshatraTermsOut
    varga: VargaTermsOut
    four_pillars: FourPillarsOut
    graha: GrahaTermsOut
    nodes: NodeTermsOut
    upagraha: UpagrahaTermsOut
    lagna: LagnaTermsOut
    zodiac: ZodiacTermsOut
    panchanga: PanchangaTermsOut
    chaayaa_grahas: ChaayaaGrahasOut
    essences: list[EssenceOut]
    paksha: list[PakshaTermOut]
    purushartha: PurusharthaTermsOut
    upagraha_aliases: list[UpagrahaAliasOut]
