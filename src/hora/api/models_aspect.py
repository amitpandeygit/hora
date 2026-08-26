"""Request and response schemas for the aspect endpoints — book chapter 10."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AspectedRasiOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    house_from_graha: int = Field(
        ..., ge=1, le=12,
        description="Which house the aspected rasi is, counted from the graha",
    )
    house: int | None = Field(
        None, ge=1, le=12,
        description=(
            "Which house of the chart the aspected rasi is. Null unless a "
            "lagna_rasi was given — section 10.2 needs no lagna to say which "
            "rasis are aspected, only to say which houses."
        ),
    )


class AspectedGrahaOut(BaseModel):
    graha: int
    graha_name: str
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str


class RasiRefOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str


class RasiDrishtiRasiOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    house: int | None = Field(
        None, ge=1, le=12,
        description="Null unless a lagna_rasi was given, as for graha drishti",
    )


class GrahaAspectOut(BaseModel):
    graha: int
    graha_name: str
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    graha_drishti_due_to: str = Field(
        "the inherent nature of a planet",
        description=(
            "Section 10.4. Graha drishti follows the graha, so two grahas in "
            "one rasi aspect different signs."
        ),
    )
    rasi_drishti_due_to: str = Field(
        "the sign a planet is in",
        description=(
            "Section 10.4. Rasi drishti follows the rasi, so two grahas in one "
            "rasi aspect the same signs — though 'the nature of the influence "
            "varies from planet to planet'."
        ),
    )
    aspects_houses_from_itself: list[int] = Field(
        ...,
        description='The 7th always; plus the graha\'s special aspects if it has any',
        examples=[[5, 7, 9]],
    )
    has_special_aspect: bool = Field(
        ...,
        description="True only for Mars, Jupiter and Saturn — section 10.2 names no others",
    )
    aspected_rasis: list[AspectedRasiOut]
    aspected_grahas: list[AspectedGrahaOut] = Field(
        ...,
        description=(
            "Grahas occupying the aspected rasis. Empty unless other "
            "placements were supplied, and it can include Rahu or Ketu: being "
            "aspected depends only on where a graha sits."
        ),
    )
    rasi_drishti_rasis: list[RasiDrishtiRasiOut] = Field(
        ...,
        description=(
            "Section 10.3's kind — the rasis aspected by the rasi this graha "
            "occupies, which the graha inherits. Every graha casts these, "
            "Rahu and Ketu included, because rasi drishti belongs to the sign."
        ),
    )
    rasi_drishti_grahas: list[AspectedGrahaOut] = Field(
        default_factory=list,
        description=(
            "Grahas in the rasi-drishti signs. Section 10.3: a planet "
            '"also aspects the houses and planets in those signs".'
        ),
    )


class GrahaAspectIn(BaseModel):
    graha: int = Field(..., ge=0, le=8, examples=[4])
    rasi: int = Field(..., ge=0, le=11, examples=[2])
    lagna_rasi: int | None = Field(None, ge=0, le=11)
    others: dict[int, int] | None = Field(
        None,
        description="Other placements, graha id to rasi, to resolve aspected grahas",
    )
    rahu_ketu_aspects: bool = Field(
        False,
        description=(
            "Give Rahu and Ketu the 5th and 9th as well. Off by default: "
            "section 10.2 names special aspects for Mars, Jupiter and Saturn "
            "only."
        ),
    )


class ChartAspectIn(BaseModel):
    rasis: dict[int, int] = Field(
        ..., description="Graha id to rasi index, 0 = Aries",
        examples=[{0: 1, 1: 0, 2: 7, 3: 8, 4: 5, 5: 9, 6: 7}],
    )
    lagna_rasi: int | None = Field(None, ge=0, le=11, examples=[7])
    rahu_ketu_aspects: bool = False


class ChartAspectOut(BaseModel):
    lagna_rasi: int | None = None
    lagna_rasi_name: str | None = None
    aspecting_grahas: list[int] = Field(
        ...,
        description=(
            "Grahas casting **graha** drishti — the seven, unless "
            "rahu_ketu_aspects is set. Exercise 14 asks about exactly these."
        ),
    )
    rasi_drishti_grahas: list[int] = Field(
        default_factory=list,
        description=(
            "Grahas casting **rasi** drishti — every graha present, nodes "
            "included. Exercise 15 asks about all nine, which is the "
            "difference section 10.1 sets up."
        ),
    )
    grahas: list[GrahaAspectOut]
    note: str
    aspect_sources: dict[str, AspectSourceOut] = Field(
        default_factory=dict,
        description=(
            "Section 10.4, so the two kinds returned per graha are read as the "
            "chapter means them rather than as one flat list of aspects."
        ),
    )
    influence_caveat: str | None = Field(
        None,
        description=(
            "Sections 10.1 and 10.4: whether an aspect takes effect depends on "
            "the aspected graha or house too. This response says an aspect "
            "exists, never that it succeeds."
        ),
    )


class BetweenIn(BaseModel):
    graha: int = Field(..., ge=0, le=8)
    graha_rasi: int = Field(..., ge=0, le=11)
    target_rasi: int = Field(..., ge=0, le=11)
    rahu_ketu_aspects: bool = False


class BetweenOut(BaseModel):
    graha: int
    graha_name: str
    graha_rasi: int
    graha_rasi_name: str
    target_rasi: int
    target_rasi_name: str
    house_from_graha: int = Field(..., ge=1, le=12)
    aspects: bool
    graha_aspects_houses: list[int]


class RasiDrishtiRuleOut(BaseModel):
    modality: str = Field(..., examples=["movable", "fixed", "dual"])
    aspects: str = Field(..., description="Which modality this one aspects")
    excludes: str = Field(..., examples=["adjacent", "itself"])
    text: str


class RasiAspectOut(BaseModel):
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    modality: str
    rule: str
    aspects_modality: str
    aspected_rasis: list[RasiRefOut]
    excluded_rasi: int | None = Field(
        None, ge=0, le=11,
        description=(
            "The one sign of the aspected modality left out. Null for a dual "
            "rasi, which excludes only itself."
        ),
    )
    excluded_rasi_name: str | None = None
    excluded_because: str


class AspectSourceOut(BaseModel):
    """Section 10.4: what one kind of aspect is due to, and how far it reaches.

    `scope` is the chapter's own comparative wording — "greater influence"
    against "limited influence on the neighbors". It is deliberately not a
    number: section 10.4 never gives one, and inventing a weight would put
    our judgement into PVR's rule.
    """

    due_to: str
    analogy: str
    scope: str
    targets_shared_by_co_located_grahas: bool = Field(
        ...,
        description=(
            "Whether two grahas in the same rasi aspect the same signs by this "
            "kind. True for rasi drishti, false for graha drishti."
        ),
    )
    nature_shared_by_co_located_grahas: bool = Field(
        ...,
        description=(
            "False for both. Even where the targets are shared, section 10.4 "
            "says the nature of the influence varies from planet to planet."
        ),
    )
    statement: str


class AspectKindOut(BaseModel):
    key: str
    name: str
    gloss: str
    rule: str
    counted_from: str
    varies_by: str


class SpecialAspectOut(BaseModel):
    graha: int
    graha_name: str
    houses: list[int] = Field(..., description="The special houses, without the 7th")
    all_houses: list[int] = Field(..., description="Including the 7th")
    text: str


class GrahaRefOut(BaseModel):
    graha: int
    graha_name: str


class AspectRulesOut(BaseModel):
    definition: str
    drishti_means: str = Field(..., examples=["aspect"])
    kinds: list[AspectKindOut]
    seventh_house_rule: str
    special_aspect_rule: str
    special_aspects: list[SpecialAspectOut]
    aspected_planet_rule: str
    aspected_planet_example: str
    aspecting_grahas: list[GrahaRefOut]
    nodes_note: str
    skill_note: str
    rasi_drishti_intro: str
    rasi_drishti_rules: list[RasiDrishtiRuleOut]
    rasi_drishti_is_mutual: str = Field(
        ...,
        description=(
            "Section 10.3 states mutuality outright. Section 10.2's graha "
            "drishti never does, and is not mutual in general."
        ),
    )
    rasi_drishti_graha_rule: str
    rasi_drishti_graha_example: str
    figure_2_note: str
    figure_2_line_count: int = Field(
        ...,
        description=(
            "How many lines Figure 2 draws — one per aspecting pair. Computed "
            "from the rules, not stored."
        ),
        examples=[18],
    )
    aspect_sources: dict[str, AspectSourceOut]
    same_sign_note: str = Field(
        ...,
        description=(
            "Section 10.4's central claim: grahas sharing a rasi share their "
            "rasi-drishti targets but not the nature of the influence."
        ),
    )
    seventh_house_analogy: str
    priest_and_brother_analogy: str
    malefic_influence_analogy: str = Field(
        ...,
        description=(
            "Section 10.4's second example. An aspect is not good news by "
            "default — the criminal influences his neighbours too."
        ),
    )
    influence_may_not_land: str
    influence_caveat: str
