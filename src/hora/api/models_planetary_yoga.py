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
    weakened: bool = Field(
        False,
        description=(
            "True when the book itself says this yoga 'may not operate well' "
            "— section 11.5.2's Dala clause. Distinct from `qualifiers`: a "
            "weakened yoga does not block a Sankhya yoga under section "
            "11.5.4's fallback. See OI-80."
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
        None, examples=["ravi", "chandra"],
        description="Restrict to one group of yogas; omit for all",
    )
    lagna_rasi: int | None = Field(
        None, ge=0, le=11,
        description=(
            "Needed by section 11.3.4's Kemadruma, the only yoga so far that "
            "counts houses from the ascendant. Without it that yoga reports "
            "that it cannot be decided, rather than a bare absent."
        ),
    )
    paksha: int | None = Field(
        None, ge=0, le=1,
        description=(
            "0 Sukla, 1 Krishna. The Moon has no benefic nature without it "
            "(section 3.2.2), which section 11.3.6's Adhi and guideline 3 need."
        ),
    )


class YogaChartOut(BaseModel):
    chart: str
    group: str | None = None
    include_nodes: bool
    lagna_rasi: int | None = None
    paksha: int | None = None
    inputs_missing: list[str] = Field(
        default_factory=list,
        description=(
            "Optional inputs that were not supplied. A yoga needing one of "
            "these says so in its own `reason`; this is the summary."
        ),
    )
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
    kemadruma_present: bool = Field(
        False,
        description=(
            "Section 11.3.4's Kemadruma 'kills the results of other good "
            "yogas'. When present, every other holding yoga carries that as a "
            "qualifier — it kills the results, never the yoga."
        ),
    )
    results_killed_by_kemadruma: list[str] = Field(default_factory=list)
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


class MahapurushaElementOut(BaseModel):
    tattva: str = Field(..., examples=["agni tattva"])
    gloss_in_11_4: str = Field(..., examples=["fiery nature"])
    gloss_in_3_2_8: str = Field(
        ..., examples=["fiery element"],
        description="Section 3.2.8 glosses the same five with 'element'; see D-32",
    )
    graha: int
    graha_name: str


class NaabhasaFamilyOut(BaseModel):
    family: str = Field(..., examples=["aasraya"])
    count: int
    names: list[str]
    section: str
    means: str | None = None
    basis: str | None = None


class KalpadrumaExampleOut(BaseModel):
    """Section 11.6's worked example — Chart 9, Chatrapati Shivaji."""

    chart: str
    native: str
    walkthrough: str
    conclusion: str
    chain: list[str] = Field(
        description="The four planets the example arrives at, in its order. "
                    "The fourth repeats the second's navamsa dispositor.",
    )
    navamsa_lagna_claim: str
    navamsa_lagna_note: str


class RaajaAssociationOut(BaseModel):
    """One of the three associations section 11.7.1 names."""

    key: str
    text: str


class PlanetaryYogaRulesOut(BaseModel):
    ravi_intro: str
    chandra_intro: str
    kemadruma_kills_other_yogas: str
    kemadruma_effort_note: str
    kemadruma_is_a_qualifier_not_a_veto: str
    adhi_example_note: str = Field(
        ...,
        description=(
            "Section 11.3.6's example does not satisfy its own rule. The rule "
            "is followed — see docs/book-deviations.md D-28."
        ),
    )
    panaphara_spelling_variants: list[str]
    mahapurusha_terms: dict[str, str]
    mahapurusha_intro: str
    pancha_bhoota_names: dict[str, str]
    mahapurusha_element_rulers: str
    mahapurusha_element_role: str
    mahapurusha_reference_rule: str = Field(
        ...,
        description=(
            "Two restrictions section 11.4 repeats for each of the five: the "
            "yoga does not apply from the Moon — the first place in the book "
            "that rules a reference out — and it applies mainly in the rasi "
            "chart, the opposite of section 11.2's preference."
        ),
    )
    mahapurusha_elements: list[MahapurushaElementOut]
    maalavya_spelling_variants: list[str]
    hamsa_misnamed_in_its_definition: str
    hamsa_name_note: str
    footnotes_unread: list[int] = Field(
        ...,
        description="Footnotes referenced in the text whose wording we do not have",
    )
    sasa_means: str
    hamsa_means: str
    naabhasa_intro: str
    naabhasa_timing_rule: str = Field(
        ...,
        description=(
            "Section 11.5: other yogas are felt mainly in the dasas of the "
            "planets and signs involved; Naabhasa results are felt in all "
            "dasas."
        ),
    )
    aasraya_basis: str
    sarpa_is_very_bad: str
    naabhasa_classification: list[NaabhasaFamilyOut]
    naabhasa_not_yet_defined: list[str] = Field(
        ...,
        description=(
            "Named by section 11.5's classification and defined in no section "
            "we have read. Listed so the gap is visible."
        ),
    )
    aakriti_means: str
    aakriti_basis: str
    aakriti_nodes_note: str = Field(
        ...,
        description=(
            "Section 11.5.3 is the closest the book comes to settling whether "
            "the nodes count as planets, and it settles it by attribution: "
            "'not counted as planets by many authors'. See OI-73."
        ),
    )
    aakriti_reading_rule: str = Field(
        ...,
        description=(
            "The book's own grammar decides eighteen of the twenty: subject "
            "'all the planets' means confinement, subject 'the house is "
            "occupied by' means the house must hold something."
        ),
    )
    aakriti_name_variants: dict[str, list[str]]
    aakriti_order_differs: str
    sankhya_means: str
    sankhya_basis: str
    sankhya_excludes_nodes: str = Field(
        ...,
        description=(
            "Section 11.5.4 rules the nodes out outright, where section 11.5.3 "
            "only reported that many authors do. The clearest statement in the "
            "book on the question OI-73 asks."
        ),
    )
    sankhya_is_a_fallback: str = Field(
        ...,
        description=(
            "Sankhya yogas apply only when no earlier Naabhasa yoga does. The "
            "one place in chapter 11 where a yoga's presence depends on "
            "another's absence, rather than on its results being killed."
        ),
    )
    weakened_yoga_is_not_applicable: str = Field(
        ...,
        description=(
            "What 'applicable' means in section 11.5.4's fallback. Forced by "
            "the section's own example — see docs/open-items.md OI-80."
        ),
    )
    sankhya_unreachable: list[str]
    sankhya_unreachable_note: str
    naabhasa_gap_note: str
    frequency_note: str
    preferred_charts: list[str]
    budha_aaditya_terms: dict[str, str]
    budha_aaditya_spelling_variants: list[str]
    combustion_note: str
    combustion_is_a_qualifier_not_a_veto: str
    timing_example: TimingExampleOut
    node_note: str
    results_note: str
    popular_fullness_rule: str = Field(
        description="Section 11.6's preamble. It binds all eighteen popular "
                    "yogas: the combinations alone are not fullness.",
    )
    popular_strength_note: str = Field(
        description="Why no section 11.6 verdict is ever reported as fully "
                    "present. See docs/open-items.md OI-81.",
    )
    popular_yogas_needing_a_named_lord: dict[str, list[str]]
    popular_intro: str
    popular_count: int = Field(
        description="Every yoga section 11.6 defines, both sides of the "
                    "Shivaji example.",
    )
    popular_count_before_the_example: int
    popular_count_after_the_example: int
    trimurthi_note: str
    trimurthi_yogas: list[str]
    trimurthi_combined_name: str
    brahma_variation: str = Field(
        description="NOTE (2)'s second definition of Brahma yoga. Carried, "
                    "not detected — the first definition is the one used.",
    )
    brahma_variation_note: str
    parivartana_footnote: str
    parivartana_sanskrit: str
    parivartana_yogas: list[str]
    lagnaadhi_gloss: str
    lagnaadhi_note: str
    lagnaadhi_houses: list[int]
    adhi_houses_from_moon: list[int]
    dusthana_lord_in_own_house: list[str]
    deep_exaltation_note: str = Field(
        description="Why Jaya and Vidyut are never reported present. See "
                    "docs/open-items.md OI-83.",
    )
    vasumati_reference_note: str
    raaja_intro: str
    raaja_count: int
    raaja_definitions: dict[str, str]
    dharma_karmadhipati_results: str | None = Field(
        description="Withheld under the licence gate of OI-12. The printed "
                    "sentence breaks off mid-clause — see OI-87.",
    )
    raaja_means: str
    raaja_basic_premise: str
    raaja_association_rule: str
    raaja_associations: list[RaajaAssociationOut]
    lagna_is_both_quadrant_and_trine: bool
    raaja_lagna_note: str
    mutual_drishti_is_both_ways_note: str
    dharma_sthana: int
    karma_sthana: int
    dharma_karmadhipati_reason: str
    trik_sthana_names: list[str]
    dusthanas: list[int]
    vipareeta_means: str
    vipareeta_reason: str
    vipareeta_ideal_case: str
    vipareeta_ideal_houses: list[int]
    vipareeta_ideal_note: str = Field(
        description="Why the ideal case can name two houses that are not "
                    "dusthanas. See docs/open-items.md OI-86.",
    )
    advanced_raaja_intro: str
    advanced_raaja_count: int
    advanced_raaja_numbering: dict[str, int] = Field(
        description="Section 11.7.3 numbers its yogas (1) to (18); this maps "
                    "each registry key back to that number.",
    )
    shadvarga_named_in_11_7_3: list[str]
    trivarga_named_in_11_7_3: list[str]
    arudha_effectiveness_rule: str
    arudha_effectiveness_note: str
    advanced_raaja_input_note: str = Field(
        description="What to supply so section 11.7.3's yogas can be decided "
                    "rather than reported undecidable.",
    )
    raaja_orb_footnote: str
    vargottamaamsa_definition: str = Field(
        description="Footnote 40, supplied with section 11.8. It closes what "
                    "section 11.7.3 (15) left undecidable.",
    )
    vargottamaamsa_spellings: list[str]
    raaja_sambandha_intro: str
    raaja_sambandha_count: int
    sambandha_means: str
    sambandha_karaka_names: dict[str, str]
    raaja_sambandha_numbering: dict[str, int]
    raaja_sambandha_are_common: str
    raaja_sambandha_magnitude_rule: str
    dhana_intro: str
    dhana_means: str
    dhana_basic_principle: str
    dhana_printed_oddity: str = Field(
        description="\"They give dasas in their dasas\" is printed exactly "
                    "so. Transcribed as found; nothing is computed from it.",
    )
    dhana_parasara_note: str
    dhana_exalted_in_second: list[str]
    dhana_exalted_in_second_rule: str
    dhana_count: int
    dhana_structure: list[str]
    dhana_structure_note: str = Field(
        description="What the twelve entries have in common, checked against "
                    "all twelve lagnas rather than assumed.",
    )
    dhana_by_lagna: dict[str, dict]
    dhana_two_combinations_note: str
    dhana_results: dict[str, str]
    dhana_results_note: str
    dhana_pisces_printed: str
    dhana_pisces_note: str = Field(
        description="Why entry (12) is undecidable rather than absent.",
    )
    raaja_sambandha_note: str = Field(
        description="Why a present verdict in section 11.8 weighs less than "
                    "one in section 11.7 — the section says so itself.",
    )
    worked_charts: list[dict]
    yogakaraka_note: str = Field(
        description="What the engine does about one planet lording both a "
                    "quadrant and a trine. See docs/open-items.md OI-85.",
    )
    kalpadruma_example: KalpadrumaExampleOut
    kalpadruma_results_footnote: str | None = Field(
        description="Footnote 34. PVR's own prose, so it is withheld under "
                    "the licence gate of OI-12 unless releasing is allowed.",
    )
    kalpadruma_result_words: list[str]
    kalpadruma_result_word_sanskrit: str | None
    kartari_means: str
    kartari_houses: list[int]
    kartari_definition: str = Field(
        description="Footnote 31, as printed.",
    )
    kartari_effect: str
    kartari_is_general: str = Field(
        description="Footnote 31's closing sentence: kartari is not confined "
                    "to the two yogas of section 11.6 that use it.",
    )
    kartari_note: str
    sun_excluded_note: str


class GuidelineIn(BaseModel):
    rasis: dict[int, int] = Field(..., examples=[{0: 0, 1: 2}])
    paksha: int | None = Field(None, ge=0, le=1)


class GuidelineOneOut(BaseModel):
    text: str
    verdict: str | None
    category: str | None = None
    house: int | None = None
    reason: str


class GuidelineAspectRowOut(BaseModel):
    graha: str
    birth_time: str
    effect: str


class GuidelineTwoOut(BaseModel):
    text: str
    aspect_table: list[GuidelineAspectRowOut]
    respectively_note: str
    verdict: str | None
    reason: str


class GuidelineThreeOut(BaseModel):
    text: str
    verdict: str | None
    benefics_in_upachaya: list[GrahaRefOut] = Field(default_factory=list)
    benefics_placed: list[GrahaRefOut] = Field(default_factory=list)
    undecidable: list[GrahaRefOut] = Field(
        default_factory=list,
        description="Grahas whose benefic nature could not be judged from the input",
    )
    reason: str


class GuidelinesOut(BaseModel):
    """Section 11.3's three General Guidelines.

    Not yogas. Each is a graded reading — guideline 1 always yields one of
    three verdicts, because kendras, panapharas and apoklimas partition the
    twelve houses — so they are returned apart from the registry.
    """

    guideline_1: GuidelineOneOut
    guideline_2: GuidelineTwoOut
    guideline_3: GuidelineThreeOut


class RaajaMagnitudeIn(BaseModel):
    """Section 11.7.2 grades a Raaja yoga by degrees, so it needs them."""

    longitudes: dict[int, float] = Field(
        ..., description="Graha id to sidereal longitude in degrees",
        examples=[{3: 32.0, 5: 33.0}],
    )
    lagna_rasi: int = Field(
        ..., ge=0, le=11,
        description="Every quadrant and trine is counted from here",
    )
    lagna_longitude: float | None = Field(
        None, description=(
            "The ascendant in degrees. Section 11.7.3's yogas 7 and 9 read "
            "the lagna of a divisional chart, which the sign cannot give."
        ),
    )
    special_lagnas: dict[str, float] | None = Field(
        None, examples=[{"HL": 147.05, "GL": 18.30}],
        description=(
            "HL, GL and any other special lagna, in degrees. Section "
            "11.7.3's yogas 6 and 8 turn on them."
        ),
    )


class RaajaFactorOut(BaseModel):
    key: str
    satisfied: bool | None = Field(
        description="null where section 11.7.2 gives no way to decide — see "
                    "`not_assessed`",
    )
    detail: str


class RaajaPairMagnitudeOut(BaseModel):
    quadrant_lord: int
    quadrant_lord_name: str
    quadrant_houses: list[int]
    trine_lord: int
    trine_lord_name: str
    trine_houses: list[int]
    association: str
    orb_degrees: float | None = Field(
        description="null for a parivartana, which has no orb",
    )
    factors: list[RaajaFactorOut]
    amsa: dict


class RaajaMagnitudeOut(BaseModel):
    """No overall verdict, by design: "None of the above factors influences
    the end result completely." """

    lagna_rasi: int
    lagna_rasi_name: str
    intro: str
    factors: list[dict]
    close_orb_degrees: float
    close_orb_is_approximate: bool
    blemish_rule: str
    orb_example: str = Field(
        description="Section 11.7.2's worked example of the 6° rule.",
    )
    dasa_varga_rule: str
    amsa_results: list[dict]
    amsa_count_not_discussed: int
    amsa_divine_counts: list[int]
    amsa_divine_rule: str
    amsa_divine_persons: list[str]
    simhaasanaamsa_rule: str
    simhaasanaamsa_emperors: list[str]
    simhaasanaamsa_footnote_unread: str = Field(
        description="Footnote 36 hangs off Saalivaahana and was not supplied.",
    )
    amsa_spellings_in_11_7_2: dict[str, str]
    amsa_spelling_note: str
    dharma_karmadhipati_pair: list[GrahaRefOut] | None
    pairs: list[RaajaPairMagnitudeOut] = Field(
        description="Empty when no Raaja yoga is present: magnitude grades a "
                    "yoga that already exists.",
    )
    arudha_effectiveness_rule: str
    arudha_effectiveness: dict = Field(
        description="Section 11.7.3 (18). A modifier on the chart's Raaja "
                    "yogas, so it is returned beside them, never among them.",
    )
    final_judgment: str
    not_assessed: list[dict]
