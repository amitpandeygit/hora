"""Planetary relationships — book §3.4.

**§3.4.1 natural (naisargika).** The book gives a derivation, then prints its
result as Table 7:

    "Take the moolatrikona of the planet. Lord of the rasi where it is exalted
    is its friend. Lords of 2nd, 4th, 5th, 8th, 9th and 12th rasis from it are
    also its natural friends. Lords of other rasis are its natural enemies. If
    a planet becomes a friend and an enemy on account of owning two rasis,
    then it is a neutral planet."

:func:`derive_natural` implements the derivation rather than reading the
table, and `test_3_4_1_the_derivation_reproduces_table_7` asserts the two agree
in all seven rows. A transcribed table can be mistyped; a table that its own
stated rule reproduces cannot be, silently.

**§3.4.3 compound.** Table 8 crosses the two into five outcomes. It is not a
sum of two scores that happens to work: a natural friend who is a temporary
enemy and a natural enemy who is a temporary friend both land on *sama*, so the
grid folds six cells into five names. :data:`TABLE_8` is the grid as printed.

**§3.4.2 temporary (tatkaala).** Chart-specific:

    "Planets occupying the 2nd, 3rd, 4th, 10th, 11th and 12th rasis counted
    from the rasi occupied by a planet are its temporary friends. Planet
    occupying other rasis are its temporary enemies."

Note the two house sets are **different** — 2/4/5/8/9/12 for natural,
2/3/4/10/11/12 for temporary — and they are counted from different things: the
moolatrikona for natural, the occupied rasi for temporary. See
:data:`NATURAL_FRIEND_HOUSES` and :data:`TEMPORARY_FRIEND_HOUSES`.

Temporary relationship is a two-way split with no neutral. A graha is never
its own friend or enemy; asking about itself raises.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    EXALTATION_RASI,
    GRAHA_NAMES,
    MOOLATRIKONA,
    NATURAL_RELATION,
    NATURAL_RELATION_NAMES,
    RASI_LORD,
    RASI_NAMES,
)


class RelationshipError(validate.InputError):
    """A relationship input that cannot be resolved."""


#: §3.4.1: "Lords of 2nd, 4th, 5th, 8th, 9th and 12th rasis from it are also
#: its natural friends", counted from the **moolatrikona**.
NATURAL_FRIEND_HOUSES = (2, 4, 5, 8, 9, 12)

#: §3.4.2: "Planets occupying the 2nd, 3rd, 4th, 10th, 11th and 12th rasis
#: counted from the rasi occupied by a planet are its temporary friends."
#: A different set, counted from a different place. Do not merge the two.
TEMPORARY_FRIEND_HOUSES = (2, 3, 4, 10, 11, 12)

#: The seven §3.4 speaks of. The nodes have no moolatrikona rule here.
CLASSICAL_SEVEN = tuple(range(7))

FRIEND = "friend"
NEUTRAL = "neutral"
ENEMY = "enemy"

#: §3.4.1's own labels, from Table 7's column headings.
NATURAL_NAMES = {FRIEND: "mitra", NEUTRAL: "sama", ENEMY: "satru"}

#: Table 7's heading prints "Nuetral" for "Neutral". Recorded so the typo is
#: known and is not reproduced in a published field.
TABLE_7_HEADING_TYPO = "Nuetral"

GREAT_FRIEND = "great_friend"
GREAT_ENEMY = "great_enemy"

#: §3.4.3 Table 8, keyed (natural, temporary). Six cells, five outcomes —
#: natural-friend/temporary-enemy and natural-enemy/temporary-friend both give
#: sama, which is why this is a table and not arithmetic.
TABLE_8: dict[tuple[str, str], str] = {
    (FRIEND, FRIEND): GREAT_FRIEND,
    (FRIEND, ENEMY): NEUTRAL,
    (NEUTRAL, FRIEND): FRIEND,
    (NEUTRAL, ENEMY): ENEMY,
    (ENEMY, FRIEND): NEUTRAL,
    (ENEMY, ENEMY): GREAT_ENEMY,
}

#: Table 8's own names, in the order it prints them.
COMPOUND_NAMES = {
    GREAT_FRIEND: "adhimitra",
    FRIEND: "mitra",
    NEUTRAL: "sama",
    ENEMY: "satru",
    GREAT_ENEMY: "adhisatru",
}

#: Table 8's English gloss for each.
COMPOUND_GLOSS = {
    GREAT_FRIEND: "good friend",
    FRIEND: "friend",
    NEUTRAL: "neutral",
    ENEMY: "enemy",
    GREAT_ENEMY: "bad enemy",
}


@dataclass(frozen=True)
class NaturalRelation:
    """One graha's natural relation to another, with how it was derived."""

    graha: int
    other: int
    relation: str
    relation_name: str
    from_exaltation_lord: bool
    friend_houses: tuple[int, ...]
    enemy_houses: tuple[int, ...]


def _house_from(base: int, house: int) -> int:
    return (base + house - 1) % 12


def houses_owned_from(graha: int, base_rasi: int) -> dict[int, tuple[int, ...]]:
    """Which houses from ``base_rasi`` each graha lords.

    A graha owning two rasis can land in both the friend and the enemy set,
    which is exactly the case §3.4.1's last sentence resolves.
    """
    out: dict[int, list[int]] = {}
    for house in range(1, 13):
        lord = int(RASI_LORD[_house_from(base_rasi, house)])
        out.setdefault(lord, []).append(house)
    return {g: tuple(h) for g, h in out.items()}


def derive_natural(graha: int, other: int) -> NaturalRelation:
    """§3.4.1's derivation, run rather than looked up.

    :param graha: the graha whose friends are being found, 0 to 6.
    :param other: the graha being judged, 0 to 6.
    :raises RelationshipError: if either is a node, or if the two are the same.
    """
    for name, value in (("graha", graha), ("other", other)):
        validate.in_range(name, value, 0, 8)
        if value not in CLASSICAL_SEVEN:
            raise RelationshipError(
                f"section 3.4.1 derives relationships from a moolatrikona, "
                f"which Table 6 gives the nodes but section 3.4 does not use; "
                f"{name}={GRAHA_NAMES[value]} is outside the classical seven"
            )
    if graha == other:
        raise RelationshipError(
            f"{GRAHA_NAMES[graha]} has no relationship to itself; section 3.4.1 "
            f"derives relations to the lords of other rasis"
        )

    moolatrikona = int(MOOLATRIKONA[graha][0])
    owned = houses_owned_from(graha, moolatrikona).get(other, ())
    friend_houses = tuple(h for h in owned if h in NATURAL_FRIEND_HOUSES)
    enemy_houses = tuple(h for h in owned if h not in NATURAL_FRIEND_HOUSES)
    exalt_lord = int(RASI_LORD[int(EXALTATION_RASI[graha])]) == other

    # The exaltation-lord friendship joins the friend set; it does not
    # short-circuit the last sentence. Moon's exaltation lord is Venus, and
    # Venus also lords two non-friend houses from Taurus — Table 7 calls that
    # neutral, not friend. Treating "exalted lord" as decisive gets Moon/Venus,
    # Mars/Saturn and Venus/Jupiter wrong.
    is_friend = bool(friend_houses) or exalt_lord
    is_enemy = bool(enemy_houses)
    if is_friend and is_enemy:
        # "If a planet becomes a friend and an enemy on account of owning two
        # rasis, then it is a neutral planet."
        relation = NEUTRAL
    elif is_friend:
        relation = FRIEND
    else:
        relation = ENEMY

    return NaturalRelation(
        graha=graha,
        other=other,
        relation=relation,
        relation_name=NATURAL_NAMES[relation],
        from_exaltation_lord=exalt_lord,
        friend_houses=friend_houses,
        enemy_houses=enemy_houses,
    )


def natural(graha: int, other: int) -> str:
    """Table 7's value, read from the stored table."""
    validate.in_range("graha", graha, 0, 6)
    validate.in_range("other", other, 0, 6)
    if graha == other:
        raise RelationshipError(f"{GRAHA_NAMES[graha]} has no relation to itself")
    return {2: FRIEND, 1: NEUTRAL, 0: ENEMY}[NATURAL_RELATION[graha][other]]


def natural_row(graha: int) -> dict[str, list[int]]:
    """One row of Table 7 — friends, neutrals and enemies of a graha."""
    validate.in_range("graha", graha, 0, 6)
    row: dict[str, list[int]] = {FRIEND: [], NEUTRAL: [], ENEMY: []}
    for other in CLASSICAL_SEVEN:
        if other != graha:
            row[natural(graha, other)].append(other)
    return row


def temporary(graha_rasi: int, other_rasi: int) -> str:
    """§3.4.2 — friend or enemy from where the two sit. No neutral.

    :param graha_rasi: rasi occupied by the graha being judged from.
    :param other_rasi: rasi occupied by the other graha.
    """
    validate.in_range("graha_rasi", graha_rasi, 0, 11)
    validate.in_range("other_rasi", other_rasi, 0, 11)
    house = (other_rasi - graha_rasi) % 12 + 1
    return FRIEND if house in TEMPORARY_FRIEND_HOUSES else ENEMY


def temporary_friends(graha_rasi: int) -> tuple[int, ...]:
    """The six rasis that are temporary friends of a graha in ``graha_rasi``."""
    validate.in_range("graha_rasi", graha_rasi, 0, 11)
    return tuple(_house_from(graha_rasi, h) for h in TEMPORARY_FRIEND_HOUSES)


@dataclass(frozen=True)
class TemporaryResult:
    """§3.4.2 applied to a whole chart, from one graha's seat."""

    graha: int
    graha_name: str
    rasi: int
    rasi_name: str
    friend_rasis: tuple[int, ...]
    friend_rasi_names: tuple[str, ...]
    friends: tuple[int, ...]
    enemies: tuple[int, ...]
    includes_nodes: bool


def temporary_in_chart(
    graha: int, rasis: dict[int, int], *, include_nodes: bool = False
) -> TemporaryResult:
    """Every other graha's temporary relation to ``graha``, in one chart.

    **The nodes are excluded by default, because Example 4 excludes them.**
    In Lord Sree Rama's chart the Sun is in Aries and Rahu in Sagittarius, the
    9th — not a temporary friend house. The book nonetheless says "Saturn is
    the **only** temporary enemy". Ketu, in Gemini, is likewise absent from the
    friend list even though Gemini is the 3rd. So §3.4.2 is counting the seven.
    Including them reproduces neither half of the example.

    :param graha: the graha to judge from, 0 to 8.
    :param rasis: graha id to occupied rasi, for every graha in the chart.
    :param include_nodes: count Rahu and Ketu too. Off by default; the book
        gives no basis for it and Example 4 contradicts it.
    :raises RelationshipError: if ``graha`` is not placed in ``rasis``.
    """
    validate.in_range("graha", graha, 0, 8)
    if graha not in rasis:
        raise RelationshipError(
            f"{GRAHA_NAMES[graha]} has no rasi in the chart given"
        )
    seat = validate.in_range("rasi", int(rasis[graha]), 0, 11)
    friends: list[int] = []
    enemies: list[int] = []
    for other, rasi in sorted(rasis.items()):
        if other == graha:
            continue
        if not include_nodes and int(other) not in CLASSICAL_SEVEN:
            continue
        (friends if temporary(seat, int(rasi)) == FRIEND else enemies).append(
            int(other)
        )
    friend_rasis = temporary_friends(seat)
    return TemporaryResult(
        graha=graha,
        graha_name=str(GRAHA_NAMES[graha]),
        rasi=seat,
        rasi_name=str(RASI_NAMES[seat]),
        friend_rasis=friend_rasis,
        friend_rasi_names=tuple(str(RASI_NAMES[r]) for r in friend_rasis),
        friends=tuple(friends),
        enemies=tuple(enemies),
        includes_nodes=include_nodes,
    )


@dataclass(frozen=True)
class CompoundRelation:
    """§3.4.3's outcome for one ordered pair, with both inputs."""

    graha: int
    graha_name: str
    other: int
    other_name: str
    natural: str
    temporary: str
    compound: str
    compound_name: str
    compound_gloss: str


def compound(natural_relation: str, temporary_relation: str) -> str:
    """Table 8 — cross a natural relation with a temporary one.

    :raises RelationshipError: if either input is not one of the labels the
        two schemes produce. Temporary has no neutral, so passing one is a
        caller error rather than a silent lookup miss.
    """
    key = (natural_relation, temporary_relation)
    if key not in TABLE_8:
        raise RelationshipError(
            f"Table 8 is indexed by a natural relation "
            f"({FRIEND}/{NEUTRAL}/{ENEMY}) and a temporary one "
            f"({FRIEND}/{ENEMY}); got {key}"
        )
    return TABLE_8[key]


def compound_in_chart(
    graha: int, other: int, rasis: dict[int, int]
) -> CompoundRelation:
    """§3.4.3 for two grahas in one chart, showing both inputs.

    :param graha: the graha judging, one of the classical seven.
    :param other: the graha judged, one of the classical seven.
    :param rasis: graha id to occupied rasi.
    :raises RelationshipError: if either graha is a node, they are the same,
        or either is missing from the chart.
    """
    nat = natural(graha, other)
    for name, value in (("graha", graha), ("other", other)):
        if value not in rasis:
            raise RelationshipError(
                f"{name}={GRAHA_NAMES[value]} has no rasi in the chart given"
            )
    tmp = temporary(int(rasis[graha]), int(rasis[other]))
    result = compound(nat, tmp)
    return CompoundRelation(
        graha=graha,
        graha_name=str(GRAHA_NAMES[graha]),
        other=other,
        other_name=str(GRAHA_NAMES[other]),
        natural=nat,
        temporary=tmp,
        compound=result,
        compound_name=COMPOUND_NAMES[result],
        compound_gloss=COMPOUND_GLOSS[result],
    )


def compound_row(graha: int, rasis: dict[int, int]) -> list[CompoundRelation]:
    """Every other classical graha's compound relation to ``graha``."""
    return [
        compound_in_chart(graha, other, rasis)
        for other in CLASSICAL_SEVEN
        if other != graha and other in rasis
    ]


#: §3.4.3: "A planet occupying a rasi owned by a mitra or adhimitra is in a
#: friendly house. A planet occupying a rasi owned by a satru or adhisatru is
#: in an inimical house." Sama is neither, so this is a two-way split with a
#: gap, not a three-way one.
FRIENDLY_HOUSE_RELATIONS = frozenset({GREAT_FRIEND, FRIEND})
INIMICAL_HOUSE_RELATIONS = frozenset({GREAT_ENEMY, ENEMY})

FRIENDLY_HOUSE = "friendly"
INIMICAL_HOUSE = "inimical"
NEITHER_HOUSE = "neither"

#: The rasi lord is not placed in the chart given, so its temporary relation
#: to the graha cannot be known and §3.4.3's test cannot be applied. Distinct
#: from "neither", which is a verdict the rule reached.
UNKNOWN_HOUSE = "unknown"


@dataclass(frozen=True)
class HouseStanding:
    """Where a graha stands relative to the lord of the rasi it occupies."""

    graha: int
    graha_name: str
    rasi: int
    rasi_name: str
    lord: int
    lord_name: str
    owns_the_rasi: bool
    relation_to_lord: str | None
    house: str


def house_standing(graha: int, rasis: dict[int, int]) -> HouseStanding:
    """§3.4.3's friendly/inimical house test, for one graha.

    The relation is to the **lord of the occupied rasi**, not to the grahas
    sitting alongside. A graha in its own rasi has no relation to itself, so
    ``relation_to_lord`` is None and the house is ``neither``.

    If the lord is not placed in ``rasis`` the house is ``unknown``.
    """
    if graha not in rasis:
        raise RelationshipError(
            f"{GRAHA_NAMES[graha]} has no rasi in the chart given"
        )
    seat = validate.in_range("rasi", int(rasis[graha]), 0, 11)
    lord = int(RASI_LORD[seat])
    if lord == graha or graha not in CLASSICAL_SEVEN or lord not in CLASSICAL_SEVEN:
        relation, house = None, NEITHER_HOUSE
    elif lord not in rasis:
        # The lord's seat is needed for the temporary half of Table 8. Without
        # it the rule cannot be applied at all, which is not the same as
        # applying it and reaching no verdict.
        relation, house = None, UNKNOWN_HOUSE
    else:
        relation = compound_in_chart(graha, lord, rasis).compound
        house = (
            FRIENDLY_HOUSE if relation in FRIENDLY_HOUSE_RELATIONS
            else INIMICAL_HOUSE if relation in INIMICAL_HOUSE_RELATIONS
            else NEITHER_HOUSE
        )
    return HouseStanding(
        graha=graha,
        graha_name=str(GRAHA_NAMES[graha]),
        rasi=seat,
        rasi_name=str(RASI_NAMES[seat]),
        lord=lord,
        lord_name=str(GRAHA_NAMES[lord]),
        owns_the_rasi=lord == graha,
        relation_to_lord=relation,
        house=house,
    )


def table_8() -> list[dict]:
    """Table 8 as printed: three natural rows, two temporary columns."""
    return [
        {
            "natural": nat,
            "temporary_friend": COMPOUND_NAMES[TABLE_8[(nat, FRIEND)]],
            "temporary_friend_gloss": COMPOUND_GLOSS[TABLE_8[(nat, FRIEND)]],
            "temporary_enemy": COMPOUND_NAMES[TABLE_8[(nat, ENEMY)]],
            "temporary_enemy_gloss": COMPOUND_GLOSS[TABLE_8[(nat, ENEMY)]],
        }
        for nat in (FRIEND, NEUTRAL, ENEMY)
    ]


def table_7() -> list[dict]:
    """Table 7, one row per graha, with the book's own column names."""
    return [
        {
            "graha": g,
            "graha_name": str(GRAHA_NAMES[g]),
            "friends": natural_row(g)[FRIEND],
            "neutrals": natural_row(g)[NEUTRAL],
            "enemies": natural_row(g)[ENEMY],
            "column_names": dict(NATURAL_RELATION_NAMES),
        }
        for g in CLASSICAL_SEVEN
    ]
