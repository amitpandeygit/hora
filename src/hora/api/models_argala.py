"""Request and response schemas for argala — book chapter 10, §10.5 and §10.6."""
from __future__ import annotations

from pydantic import BaseModel, Field


class GrahaRefOut(BaseModel):
    graha: int
    graha_name: str


class ArgalaRowOut(BaseModel):
    kind: str = Field(..., examples=["argala", "virodhargala"])
    house: int = Field(..., ge=1, le=12, description="Counted from the target sign")
    sign: int = Field(..., ge=0, le=11)
    sign_name: str
    grahas: list[GrahaRefOut]
    paired_house: int = Field(
        ..., ge=1, le=12,
        description=(
            "The house this one obstructs, or is obstructed by. Section 10.6 "
            "pairs 2nd/12th, 4th/10th, 11th/3rd and 5th/9th."
        ),
    )
    obstructs: int | None = Field(
        None, description="Set on a virodhargala row: the argala house it blocks"
    )
    obstructed_by: int | None = Field(
        None, description="Set on an argala row: the house that could block it"
    )
    argala_kind: str = Field(
        "primary",
        examples=["primary", "secondary"],
        description=(
            "Section 10.5: the 2nd, 4th and 11th cause **primary** argala, the "
            "5th a **secondary** one. A virodhargala inherits the kind of the "
            "argala it obstructs, so the 9th is secondary."
        ),
    )
    present: bool = Field(
        ..., description="False when the house is empty — no argala arises at all"
    )
    obstructed: bool | None = Field(
        None,
        description=(
            "Argala rows only. False when the obstructing house is empty: "
            '"If Le (3rd from Ge) is empty, this argala is unobstructed."'
        ),
    )
    promoted_from_virodhargala: bool = Field(
        False,
        description=(
            "True when section 10.6's special principle moved a 3rd-house "
            "obstruction to an argala because several malefics sit there."
        ),
    )


class ArgalaOnSignOut(BaseModel):
    sign: int = Field(..., ge=0, le=11)
    sign_name: str
    counted_anti_zodiacally: bool = Field(
        ...,
        description=(
            "Section 10.6's note: true when this sign contains Ketu, in which "
            "case its argalas and virodhargalas are counted in reverse."
        ),
    )
    ketu_sign: int | None = None
    argalas: list[ArgalaRowOut]
    virodhargalas: list[ArgalaRowOut]


class ArgalaHouseOut(ArgalaOnSignOut):
    house: int = Field(..., ge=1, le=12)


class ArgalaOnSignIn(BaseModel):
    sign: int = Field(..., ge=0, le=11, examples=[2])
    rasis: dict[int, int] = Field(
        ..., description="Graha id to rasi index, 0 = Aries",
        examples=[{3: 2, 4: 11, 5: 0, 6: 5}],
    )
    malefics: list[int] | None = Field(
        None,
        description=(
            "Which grahas count as malefic for the 3rd-house rule. Defaults to "
            "Sun, Mars, Saturn, Rahu and Ketu — chapter 3 makes the Moon and "
            "Mercury conditional, so they are excluded unless named here."
        ),
    )
    several_malefics: int | None = Field(
        None, ge=1, le=9,
        description=(
            "How many malefics in the 3rd count as “several”. The book never "
            "says; the default reproduces Exercise 16's own answer table."
        ),
    )


class ArgalaChartIn(BaseModel):
    rasis: dict[int, int] = Field(..., examples=[{0: 1, 1: 0, 2: 7}])
    lagna_rasi: int = Field(..., ge=0, le=11, examples=[7])
    malefics: list[int] | None = None
    several_malefics: int | None = Field(None, ge=1, le=9)


class ArgalaChartOut(BaseModel):
    lagna_rasi: int
    lagna_rasi_name: str
    houses: list[ArgalaHouseOut]
    several_malefics_threshold: int


class ArgalaPairOut(BaseModel):
    argala_house: int = Field(..., ge=1, le=12)
    virodhargala_house: int = Field(..., ge=1, le=12)
    argala_kind: str = Field(..., examples=["primary", "secondary"])
    text: str


class InfluenceRankOut(BaseModel):
    """Section 10.5 ranks the three influences in one passage.

    `strength` is the chapter's own word — "small", "more concrete",
    "decisive". Deliberately not a number: section 10.5 gives none, and a
    weight would be our judgement inside PVR's rule. See OI-64.
    """

    rank: int = Field(..., ge=1, le=3, description="1 weakest, 3 strongest")
    influence: str = Field(..., examples=["rasi drishti", "graha drishti", "argala"])
    strength: str
    text: str


class ArgalaNatureOut(BaseModel):
    name: str = Field(..., examples=["paapaargala", "subhaargala"])
    gloss: str


class ArgalaRulesOut(BaseModel):
    argala_means: str = Field(..., examples=["a bolt"])
    argala_definition: str
    primary_rule: str
    secondary_rule: str
    house_kinds: dict[int, str] = Field(
        ..., description="Which argala house is primary and which secondary"
    )
    nature_rule: str
    influence_ranking: list[InfluenceRankOut]
    definition: str
    rule: str
    pairs: list[ArgalaPairOut]
    by_nature: dict[str, ArgalaNatureOut]
    ketu_note: str
    third_house_rule: str
    several_malefics_threshold: int
    several_malefics_note: str = Field(
        ...,
        description=(
            "Why the threshold is what it is, and that the book does not "
            "state it."
        ),
    )
    fixed_malefics: list[GrahaRefOut]
    malefics_note: str
