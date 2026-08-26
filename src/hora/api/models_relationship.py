"""Models for the planetary relationship endpoints — book §3.4."""
from __future__ import annotations

from pydantic import BaseModel, Field


class NaturalIn(BaseModel):
    """Two of the classical seven. Section 3.4 does not use the nodes."""

    graha: int = Field(..., ge=0, le=6, examples=[0])
    other: int = Field(..., ge=0, le=6, examples=[5])


class NaturalOut(BaseModel):
    graha: int
    graha_name: str
    other: int
    other_name: str
    relation: str = Field(..., examples=["friend", "neutral", "enemy"])
    relation_name: str = Field(..., examples=["mitra", "sama", "satru"])
    table_7_relation: str = Field(
        ..., description="Table 7's printed value; must equal `relation`"
    )
    from_exaltation_lord: bool
    friend_houses: list[int] = Field(
        ..., description="Houses from the moolatrikona that `other` lords, of 2/4/5/8/9/12"
    )
    enemy_houses: list[int]
    reason: str


class TemporaryIn(BaseModel):
    """A graha and the rasi every graha occupies."""

    graha: int = Field(..., ge=0, le=8, examples=[0])
    rasis: dict[int, int] = Field(
        ...,
        description="Graha id to occupied rasi, 0-11",
        examples=[{0: 0, 1: 3, 2: 9, 3: 1, 4: 3, 5: 11, 6: 6}],
    )
    include_nodes: bool = Field(
        False,
        description=(
            "Count Rahu and Ketu. Off by default: Example 4 calls Saturn the "
            "only temporary enemy of the Sun though Rahu sits in the 9th."
        ),
    )


class TemporaryOut(BaseModel):
    graha: int
    graha_name: str
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    friend_rasis: list[int] = Field(..., min_length=6, max_length=6)
    friend_rasi_names: list[str] = Field(..., min_length=6, max_length=6)
    friends: list[int]
    friend_names: list[str]
    enemies: list[int]
    enemy_names: list[str]
    includes_nodes: bool


class CompoundIn(BaseModel):
    """A graha, the chart, and optionally one other graha to judge."""

    graha: int = Field(..., ge=0, le=6, examples=[0])
    rasis: dict[int, int] = Field(
        ..., description="Graha id to occupied rasi, 0-11"
    )
    other: int | None = Field(
        None, ge=0, le=6,
        description="Omit for every other classical graha's relation",
    )


class CompoundRelationOut(BaseModel):
    graha: int
    graha_name: str
    other: int
    other_name: str
    natural: str = Field(..., examples=["friend", "neutral", "enemy"])
    temporary: str = Field(
        ..., description="Section 3.4.2 has no neutral", examples=["friend", "enemy"]
    )
    compound: str = Field(..., examples=["great_friend", "neutral", "great_enemy"])
    compound_name: str = Field(..., examples=["adhimitra", "sama", "adhisatru"])
    compound_gloss: str = Field(..., examples=["good friend", "bad enemy"])


class CompoundOut(BaseModel):
    graha: int
    relations: list[CompoundRelationOut]


class Table8RowOut(BaseModel):
    natural: str
    temporary_friend: str
    temporary_friend_gloss: str
    temporary_enemy: str
    temporary_enemy_gloss: str


class CompoundRulesOut(BaseModel):
    section: str
    rule: str
    names: dict[str, str]
    glosses: dict[str, str]
    table_8: list[Table8RowOut] = Field(..., min_length=3, max_length=3)
    six_cells_five_outcomes: str


class ChartIn(BaseModel):
    """A whole chart. One call returns every relationship in it."""

    rasis: dict[int, int] = Field(
        ...,
        description="Graha id to occupied rasi, 0-11",
        examples=[{0: 0, 1: 3, 2: 9, 3: 1, 4: 3, 5: 11, 6: 6}],
    )
    include_nodes: bool = Field(
        False, description="Count Rahu and Ketu in the temporary lists. See OI-49."
    )


class NaturalGroupsOut(BaseModel):
    friend: list[int]
    neutral: list[int]
    enemy: list[int]


class TemporaryGroupsOut(BaseModel):
    friends: list[int]
    enemies: list[int]


class CompoundGroupsOut(BaseModel):
    great_friends: list[int]
    friends: list[int]
    neutrals: list[int]
    enemies: list[int]
    great_enemies: list[int]


class HouseStandingOut(BaseModel):
    lord: int
    lord_name: str
    owns_the_rasi: bool
    relation_to_lord: str | None = None
    standing: str = Field(
        ...,
        description=(
            '"neither" means the rule applied and the lord is a sama, or the '
            'graha owns the rasi. "unknown" means the lord is not placed in '
            "the chart given, so the rule could not be applied."
        ),
        examples=["friendly", "inimical", "neither", "unknown"],
    )


class PerGrahaOut(BaseModel):
    graha: int
    graha_name: str
    rasi: int = Field(..., ge=0, le=11)
    rasi_name: str
    natural: NaturalGroupsOut
    temporary: TemporaryGroupsOut
    compound: CompoundGroupsOut
    house: HouseStandingOut


class MatrixRowOut(BaseModel):
    graha: int
    graha_name: str
    relations: list[CompoundRelationOut | None] = Field(
        ..., description="One per graha in `grahas`; null on the diagonal"
    )


class ChartOut(BaseModel):
    grahas: list[int]
    matrix: list[MatrixRowOut]
    per_graha: list[PerGrahaOut]
    friendly_house_note: str
    includes_nodes: bool


class Table7RowOut(BaseModel):
    graha: int
    graha_name: str
    friends: list[int]
    neutrals: list[int]
    enemies: list[int]
    column_names: dict[int, str]


class NaturalRulesOut(BaseModel):
    section: str
    derivation: str
    counted_from: str
    friend_houses: list[int] = Field(..., min_length=6, max_length=6)
    names: dict[str, str]
    table_7: list[Table7RowOut] = Field(..., min_length=7, max_length=7)
    derivation_reproduces_table_7: bool


class TemporaryRulesOut(BaseModel):
    section: str
    rule: str
    sanskrit_name: str
    counted_from: str
    friend_houses: list[int] = Field(..., min_length=6, max_length=6)
    has_no_neutral: str
    nodes_excluded: str


class RelationshipRulesOut(BaseModel):
    section: str = Field(..., examples=["3.4"])
    title: str
    natural: NaturalRulesOut
    temporary: TemporaryRulesOut
    compound: CompoundRulesOut
    house_sets_differ: str
