"""Section 3.4, Planetary Relationships — §3.4.1, §3.4.2 and Example 4.

§3.4.1 gives a derivation and then prints its result as Table 7. Both are
implemented, and `test_3_4_1_the_derivation_reproduces_table_7` asserts they
agree in all 42 ordered pairs. A transcribed table can be mistyped; a table its
own stated rule reproduces cannot be, silently. That check earned its place
immediately — it caught a real bug in the first cut of `derive_natural`, which
let "lords the exaltation rasi" short-circuit the both-sides rule and so called
Moon/Venus, Mars/Saturn and Venus/Jupiter friends instead of neutral.

Example 4 exposed a second thing: §3.4.2 counts **only the classical seven**.
See `test_example_4_shows_the_nodes_are_not_counted`.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.relationship import (
    CLASSICAL_SEVEN,
    COMPOUND_GLOSS,
    COMPOUND_NAMES,
    ENEMY,
    FRIEND,
    GREAT_ENEMY,
    GREAT_FRIEND,
    NATURAL_FRIEND_HOUSES,
    NEUTRAL,
    TABLE_8,
    TEMPORARY_FRIEND_HOUSES,
    RelationshipError,
    compound,
    compound_row,
    derive_natural,
    house_standing,
    natural,
    natural_row,
    table_7,
    temporary,
    temporary_friends,
    temporary_in_chart,
)
from hora.core import const as c
from hora.core.const import Graha
from hora.core.validate import InputError
from hora.services import relationship_service

client = TestClient(app)

A = list(c.RASI_ABBR)
N = {str(c.GRAHA_NAMES[g]): g for g in range(9)}


# --------------------------------------------------------------------------
# 3.4.1 Natural Relationships — Table 7
# --------------------------------------------------------------------------

#: Table 7 exactly as printed.
TABLE_7 = [
    ("Sun", ["Moon", "Mars", "Jupiter"], ["Mercury"], ["Venus", "Saturn"]),
    ("Moon", ["Sun", "Mercury"], ["Mars", "Jupiter", "Venus", "Saturn"], []),
    ("Mars", ["Sun", "Moon", "Jupiter"], ["Venus", "Saturn"], ["Mercury"]),
    ("Mercury", ["Sun", "Venus"], ["Mars", "Jupiter", "Saturn"], ["Moon"]),
    ("Jupiter", ["Sun", "Moon", "Mars"], ["Saturn"], ["Mercury", "Venus"]),
    ("Venus", ["Mercury", "Saturn"], ["Mars", "Jupiter"], ["Sun", "Moon"]),
    ("Saturn", ["Mercury", "Venus"], ["Jupiter"], ["Sun", "Moon", "Mars"]),
]


@pytest.mark.parametrize("name,friends,neutrals,enemies", TABLE_7)
def test_3_4_1_table_7_row_by_row(name, friends, neutrals, enemies):
    row = natural_row(N[name])
    assert [str(c.GRAHA_NAMES[g]) for g in row[FRIEND]] == friends
    assert [str(c.GRAHA_NAMES[g]) for g in row[NEUTRAL]] == neutrals
    assert [str(c.GRAHA_NAMES[g]) for g in row[ENEMY]] == enemies


def test_3_4_1_the_moon_has_no_enemies():
    """Table 7's Moon row prints a dash in the enemy column. The only graha
    with an empty group, so a "three non-empty columns" assumption is wrong."""
    assert natural_row(Graha.MOON)[ENEMY] == []
    assert all(natural_row(g)[FRIEND] for g in CLASSICAL_SEVEN)


def test_3_4_1_every_row_accounts_for_the_other_six():
    for g in CLASSICAL_SEVEN:
        row = natural_row(g)
        assert sorted(row[FRIEND] + row[NEUTRAL] + row[ENEMY]) == [
            o for o in CLASSICAL_SEVEN if o != g
        ]


def test_3_4_1_the_friend_houses():
    """"Lords of 2nd, 4th, 5th, 8th, 9th and 12th rasis from it are also its
    natural friends."""
    assert NATURAL_FRIEND_HOUSES == (2, 4, 5, 8, 9, 12)


def test_3_4_1_the_derivation_reproduces_table_7():
    """The check this module exists for. §3.4.1 states a rule and prints its
    result; if the two disagree, one of them is wrong."""
    mismatches = [
        (str(c.GRAHA_NAMES[a]), str(c.GRAHA_NAMES[b]))
        for a in CLASSICAL_SEVEN
        for b in CLASSICAL_SEVEN
        if a != b and derive_natural(a, b).relation != natural(a, b)
    ]
    assert mismatches == []


@pytest.mark.parametrize("graha,other", [
    (Graha.MOON, Graha.VENUS), (Graha.MARS, Graha.SATURN),
    (Graha.VENUS, Graha.JUPITER),
])
def test_3_4_1_owning_the_exaltation_rasi_does_not_win_outright(graha, other):
    """The three pairs where the exaltation lord also lords two non-friend
    houses. §3.4.1's last sentence makes them **neutral**, not friends.

    Treating "lord of the exaltation rasi" as decisive gets exactly these three
    wrong, which is what the first cut of `derive_natural` did.
    """
    derived = derive_natural(graha, other)
    assert derived.from_exaltation_lord is True
    assert derived.enemy_houses
    assert derived.relation == NEUTRAL
    assert natural(graha, other) == NEUTRAL


def test_3_4_1_a_neutral_always_comes_from_owning_two_rasis():
    """"If a planet becomes a friend and an enemy on account of owning two
    rasis, then it is a neutral planet." So every neutral must have a foot in
    both camps — no other route to neutral exists."""
    for a in CLASSICAL_SEVEN:
        for b in CLASSICAL_SEVEN:
            if a == b or natural(a, b) != NEUTRAL:
                continue
            derived = derive_natural(a, b)
            assert derived.enemy_houses, (a, b)
            assert derived.friend_houses or derived.from_exaltation_lord, (a, b)


def test_3_4_1_relationships_are_not_symmetric():
    """Mercury counts the Moon an enemy; the Moon counts Mercury a friend.
    A caller that cached one direction and reused it would be wrong."""
    assert natural(Graha.MERCURY, Graha.MOON) == ENEMY
    assert natural(Graha.MOON, Graha.MERCURY) == FRIEND
    asymmetric = [
        (a, b) for a in CLASSICAL_SEVEN for b in CLASSICAL_SEVEN
        if a != b and natural(a, b) != natural(b, a)
    ]
    assert asymmetric, "the table is not symmetric and must not be assumed so"


def test_3_4_1_the_column_names():
    """Table 7's headings: "Friends (mitra)", "Nuetral (sama)",
    "Enemies (satru)". The heading misprints "Neutral"; the published field
    uses the Sanskrit, so the typo is not reproduced."""
    assert c.NATURAL_RELATION_NAMES == {2: "mitra", 1: "sama", 0: "satru"}


def test_3_4_1_rejects_the_nodes_and_self():
    with pytest.raises(RelationshipError, match="classical seven"):
        derive_natural(Graha.RAHU, Graha.SUN)
    with pytest.raises(RelationshipError, match="itself"):
        derive_natural(Graha.SUN, Graha.SUN)
    with pytest.raises(InputError):
        derive_natural(9, 0)


def test_3_4_1_table_7_is_served_whole():
    rows = table_7()
    assert len(rows) == 7
    assert [r["graha_name"] for r in rows] == [t[0] for t in TABLE_7]


# --------------------------------------------------------------------------
# 3.4.2 Temporary Relationships
# --------------------------------------------------------------------------


def test_3_4_2_the_friend_houses():
    """"Planets occupying the 2nd, 3rd, 4th, 10th, 11th and 12th rasis counted
    from the rasi occupied by a planet are its temporary friends."""
    assert TEMPORARY_FRIEND_HOUSES == (2, 3, 4, 10, 11, 12)


def test_3_4_2_the_two_house_sets_are_different():
    """2/4/5/8/9/12 from the moolatrikona for natural; 2/3/4/10/11/12 from the
    occupied rasi for temporary. Different sets, different origins. Sharing one
    constant between them would be wrong in four places."""
    assert set(NATURAL_FRIEND_HOUSES) != set(TEMPORARY_FRIEND_HOUSES)
    assert set(NATURAL_FRIEND_HOUSES) ^ set(TEMPORARY_FRIEND_HOUSES) == {
        5, 8, 9, 3, 10, 11,
    }


def test_3_4_2_has_no_neutral():
    """Two outcomes, not three. Every rasi is either a friend house or not."""
    results = {temporary(0, r) for r in range(12) if r != 0}
    assert results == {FRIEND, ENEMY}
    assert NEUTRAL not in results


def test_3_4_2_six_rasis_are_friends_and_six_are_not():
    friends = temporary_friends(0)
    assert len(friends) == 6
    assert len(set(friends)) == 6
    assert 0 not in friends, "the occupied rasi is the 1st, not a friend house"


def test_3_4_2_is_symmetric_only_by_accident():
    """The 2nd from A puts A in the 12th from B — both friend houses. But the
    3rd from A puts A in the 11th, also both. The set happens to be closed
    under reflection, which is worth pinning rather than assuming."""
    for a in range(12):
        for b in range(12):
            if a != b:
                assert temporary(a, b) == temporary(b, a), (a, b)


@pytest.mark.parametrize("house", TEMPORARY_FRIEND_HOUSES)
def test_3_4_2_each_friend_house(house):
    assert temporary(0, (house - 1) % 12) == FRIEND


@pytest.mark.parametrize("house", [1, 5, 6, 7, 8, 9])
def test_3_4_2_each_enemy_house(house):
    assert temporary(0, (house - 1) % 12) == ENEMY


# --------------------------------------------------------------------------
# Example 4 — Lord Sree Rama's chart
# --------------------------------------------------------------------------

#: Figure 1, as §1.3.4 gives it and `test_book_1_3_4.py` already stores.
RAMA = {
    int(Graha.SUN): A.index("Ar"), int(Graha.MERCURY): A.index("Ta"),
    int(Graha.KETU): A.index("Ge"), int(Graha.MOON): A.index("Cn"),
    int(Graha.JUPITER): A.index("Cn"), int(Graha.SATURN): A.index("Li"),
    int(Graha.RAHU): A.index("Sg"), int(Graha.MARS): A.index("Cp"),
    int(Graha.VENUS): A.index("Pi"),
}


def test_example_4_the_chart_matches_figure_1():
    """The same placements §1.3.4's Example 1 gives, so the two examples are
    read from one chart and cannot drift apart."""
    from tests.unit.test_book_1_3_4 import RAMA_GRAHAS

    assert {g: A[r] for g, r in RAMA.items()} == RAMA_GRAHAS


def test_example_4_sun_the_six_friend_rasis():
    """"Sun is in Ar. The 2nd, 3rd, 4th, 10th, 11th and 12th rasis counted from
    Ar are Ta, Ge, Cn, Cp, Aq and Pi."""
    result = temporary_in_chart(Graha.SUN, RAMA)
    assert result.rasi_name == "Aries"
    assert list(result.friend_rasi_names) == [
        c.RASI_NAMES[A.index(x)] for x in ("Ta", "Ge", "Cn", "Cp", "Aq", "Pi")
    ]


def test_example_4_sun_the_temporary_friends():
    """"Planets in those rasis are Mercury, Moon, Jupiter, Mars and Venus. They
    are temporary friends of Sun in this chart."""
    result = temporary_in_chart(Graha.SUN, RAMA)
    assert {str(c.GRAHA_NAMES[g]) for g in result.friends} == {
        "Mercury", "Moon", "Jupiter", "Mars", "Venus",
    }


def test_example_4_sun_saturn_is_the_only_temporary_enemy():
    """"Saturn is the only temporary enemy."""
    result = temporary_in_chart(Graha.SUN, RAMA)
    assert [str(c.GRAHA_NAMES[g]) for g in result.enemies] == ["Saturn"]


def test_example_4_moon_the_six_friend_rasis():
    """"Moon is in Cn. The 2nd, 3rd, 4th, 10th, 11th and 12th rasis counted
    from Cn are Le, Vi, Li, Ar, Ta and Ge."""
    result = temporary_in_chart(Graha.MOON, RAMA)
    assert result.rasi_name == "Cancer"
    assert list(result.friend_rasi_names) == [
        c.RASI_NAMES[A.index(x)] for x in ("Le", "Vi", "Li", "Ar", "Ta", "Ge")
    ]


def test_example_4_moon_the_temporary_friends_and_enemies():
    """"Planets in those rasis are Saturn, Sun and Mercury. They are temporary
    friends of Moon in this chart. Temporary enemies are Mars, Jupiter,
    Venus."""
    result = temporary_in_chart(Graha.MOON, RAMA)
    assert {str(c.GRAHA_NAMES[g]) for g in result.friends} == {
        "Saturn", "Sun", "Mercury",
    }
    assert {str(c.GRAHA_NAMES[g]) for g in result.enemies} == {
        "Mars", "Jupiter", "Venus",
    }


def test_example_4_shows_the_nodes_are_not_counted():
    """The finding this example produced.

    Rahu is in Sg, the **9th** from the Sun's Aries — not a temporary friend
    house — so counting the nodes would make Rahu a temporary enemy. The book
    says "Saturn is the **only** temporary enemy". Ketu is in Ge, the 3rd, and
    is likewise absent from the friend list. So §3.4.2 counts the seven, and
    `include_nodes` is off by default.
    """
    assert temporary(A.index("Ar"), A.index("Sg")) == ENEMY
    assert temporary(A.index("Ar"), A.index("Ge")) == FRIEND

    with_nodes = temporary_in_chart(Graha.SUN, RAMA, include_nodes=True)
    assert {str(c.GRAHA_NAMES[g]) for g in with_nodes.enemies} == {"Saturn", "Rahu"}
    assert int(Graha.KETU) in with_nodes.friends

    without = temporary_in_chart(Graha.SUN, RAMA)
    assert [str(c.GRAHA_NAMES[g]) for g in without.enemies] == ["Saturn"]
    assert without.includes_nodes is False


def test_example_4_through_the_service():
    for graha, friends, enemies in (
        (Graha.SUN, {"Mercury", "Moon", "Jupiter", "Mars", "Venus"}, {"Saturn"}),
        (Graha.MOON, {"Saturn", "Sun", "Mercury"}, {"Mars", "Jupiter", "Venus"}),
    ):
        payload = relationship_service.temporary_relation(int(graha), RAMA)
        assert set(payload["friend_names"]) == friends
        assert set(payload["enemy_names"]) == enemies


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_natural_endpoint_returns_the_derivation_and_the_table():
    body = client.post(
        "/v1/relationship/natural", json={"graha": 1, "other": 5}
    ).json()
    assert body["relation"] == body["table_7_relation"] == "neutral"
    assert body["from_exaltation_lord"] is True
    assert body["enemy_houses"] == [1, 6]
    assert "owning two rasis" in body["reason"]


def test_natural_endpoint_rejects_a_node():
    assert client.post(
        "/v1/relationship/natural", json={"graha": 7, "other": 0}
    ).status_code == 422


def test_temporary_endpoint_reproduces_example_4():
    body = client.post(
        "/v1/relationship/temporary", json={"graha": 0, "rasis": RAMA}
    ).json()
    assert body["enemy_names"] == ["Saturn"]
    assert len(body["friend_rasis"]) == 6


def test_temporary_endpoint_rejects_a_graha_not_in_the_chart():
    r = client.post(
        "/v1/relationship/temporary", json={"graha": 0, "rasis": {1: 3}}
    )
    assert r.status_code == 400
    assert "no rasi" in r.json()["error"]["message"]


def test_rules_endpoint_serves_both_schemes():
    body = client.get("/v1/relationship/rules").json()
    assert body["section"] == "3.4"
    assert body["natural"]["friend_houses"] == [2, 4, 5, 8, 9, 12]
    assert body["temporary"]["friend_houses"] == [2, 3, 4, 10, 11, 12]
    assert body["natural"]["derivation_reproduces_table_7"] is True
    assert body["temporary"]["sanskrit_name"] == "tatkaala"
    assert "Rahu" in body["temporary"]["nodes_excluded"]
    assert "different" in body["house_sets_differ"].lower()


def test_the_existing_chart_code_agrees_with_this_module():
    """`charts/dignity.py:temporal_relation` predates this. If the two ever
    disagree, /v1/chart's compound relations drift from §3.4.2."""
    from hora.charts.dignity import temporal_relation
    from hora.core.ephemeris.base import PlanetPosition

    positions = {
        g: PlanetPosition(
            graha=g,
            longitude=r * 30.0 + 5.0,
            latitude=0.0,
            distance=1.0,
            speed_longitude=1.0,
            speed_latitude=0.0,
            speed_distance=0.0,
        )
        for g, r in RAMA.items()
    }
    for a, rasi_a in RAMA.items():
        for b, rasi_b in RAMA.items():
            if a == b:
                continue
            expected = 1 if temporary(rasi_a, rasi_b) == FRIEND else 0
            assert temporal_relation(a, b, positions) == expected, (a, b)


# --------------------------------------------------------------------------
# Exercise 5 — Jupiter and Venus in the same chart
# --------------------------------------------------------------------------


def test_exercise_5_jupiter_the_six_friend_rasis():
    """"Jupiter is in Cn. The 2nd, 3rd, 4th, 10th, 11th and 12th rasis counted
    from Cn are Le, Vi, Li, Ar, Ta and Ge."""
    result = temporary_in_chart(Graha.JUPITER, RAMA)
    assert result.rasi_name == "Cancer"
    assert list(result.friend_rasi_names) == [
        c.RASI_NAMES[A.index(x)] for x in ("Le", "Vi", "Li", "Ar", "Ta", "Ge")
    ]


def test_exercise_5_jupiter_friends_and_enemies():
    """"Planets in those rasis are Saturn, Sun and Mercury. They are temporary
    friends of Jupiter in this chart. Temporary enemies are Moon, Mars,
    Venus."""
    result = temporary_in_chart(Graha.JUPITER, RAMA)
    assert {str(c.GRAHA_NAMES[g]) for g in result.friends} == {
        "Saturn", "Sun", "Mercury",
    }
    assert {str(c.GRAHA_NAMES[g]) for g in result.enemies} == {
        "Moon", "Mars", "Venus",
    }


def test_exercise_5_venus_the_six_friend_rasis():
    """"Venus is in Pi. The 2nd, 3rd, 4th, 10th, 11th and 12th rasis counted
    from Pi are Ar, Ta, Ge, Sg, Cp and Aq."

    Note the wrap: the 2nd from Pisces is Aries, so the list starts at the
    beginning of the zodiac.
    """
    result = temporary_in_chart(Graha.VENUS, RAMA)
    assert result.rasi_name == "Pisces"
    assert list(result.friend_rasi_names) == [
        c.RASI_NAMES[A.index(x)] for x in ("Ar", "Ta", "Ge", "Sg", "Cp", "Aq")
    ]


def test_exercise_5_venus_friends_and_enemies():
    """"Planets in those rasis are Sun, Mercury and Mars. They are temporary
    friends of Venus in this chart. Temporary enemies are Moon, Jupiter,
    Saturn."""
    result = temporary_in_chart(Graha.VENUS, RAMA)
    assert {str(c.GRAHA_NAMES[g]) for g in result.friends} == {
        "Sun", "Mercury", "Mars",
    }
    assert {str(c.GRAHA_NAMES[g]) for g in result.enemies} == {
        "Moon", "Jupiter", "Saturn",
    }


def test_exercise_5_confirms_the_nodes_are_excluded():
    """A second, independent confirmation of OI-49. Rahu is in Sg — the 10th
    from Venus's Pisces, a friend house — and Ketu in Ge, the 4th, also a
    friend house. The answer lists neither among Venus's temporary friends.

    Example 4 showed a node wrongly appearing as an *enemy*; this shows one
    wrongly appearing as a *friend*. Both directions, same conclusion.
    """
    assert temporary(A.index("Pi"), A.index("Sg")) == FRIEND
    assert temporary(A.index("Pi"), A.index("Ge")) == FRIEND

    with_nodes = temporary_in_chart(Graha.VENUS, RAMA, include_nodes=True)
    assert {int(Graha.RAHU), int(Graha.KETU)} <= set(with_nodes.friends)

    without = temporary_in_chart(Graha.VENUS, RAMA)
    assert {str(c.GRAHA_NAMES[g]) for g in without.friends} == {
        "Sun", "Mercury", "Mars",
    }


def test_exercise_5_moon_and_jupiter_share_a_rasi_and_so_share_relations():
    """"Note that Moon and Jupiter have the same temporary friends and
    temporary enemies. That is because they occupy the same rasi and temporary
    relationships are based on the rasis occupied by planets."

    Stated precisely: the six friend **rasis** are identical, and every graha
    other than the two of them is classed the same way by both.
    """
    moon = temporary_in_chart(Graha.MOON, RAMA)
    jupiter = temporary_in_chart(Graha.JUPITER, RAMA)
    assert moon.rasi == jupiter.rasi
    assert moon.friend_rasis == jupiter.friend_rasis
    assert set(moon.friends) == set(jupiter.friends)

    pair = {int(Graha.MOON), int(Graha.JUPITER)}
    assert set(moon.enemies) - pair == set(jupiter.enemies) - pair


def test_exercise_5_two_grahas_in_one_rasi_are_temporary_enemies():
    """The one way the two lists are *not* identical, which the book's "same"
    glosses over: each excludes itself and each finds the other in the 1st
    house, which is not a friend house. So Moon is among Jupiter's enemies and
    Jupiter among Moon's.
    """
    assert temporary(A.index("Cn"), A.index("Cn")) == ENEMY
    assert 1 not in TEMPORARY_FRIEND_HOUSES

    moon = temporary_in_chart(Graha.MOON, RAMA)
    jupiter = temporary_in_chart(Graha.JUPITER, RAMA)
    assert int(Graha.JUPITER) in moon.enemies
    assert int(Graha.MOON) in jupiter.enemies
    assert int(Graha.MOON) not in moon.enemies + moon.friends


def test_exercise_5_through_the_endpoint():
    for graha, friends, enemies in (
        (Graha.JUPITER, {"Saturn", "Sun", "Mercury"}, {"Moon", "Mars", "Venus"}),
        (Graha.VENUS, {"Sun", "Mercury", "Mars"}, {"Moon", "Jupiter", "Saturn"}),
    ):
        body = client.post(
            "/v1/relationship/temporary", json={"graha": int(graha), "rasis": RAMA}
        ).json()
        assert set(body["friend_names"]) == friends
        assert set(body["enemy_names"]) == enemies


# --------------------------------------------------------------------------
# 3.4.3 Compound Relationships — Table 8
# --------------------------------------------------------------------------

#: Table 8 exactly as printed: (natural, temporary) -> name, gloss.
TABLE_8_PRINTED = [
    ("friend", "friend", "adhimitra", "good friend"),
    ("friend", "enemy", "sama", "neutral"),
    ("neutral", "friend", "mitra", "friend"),
    ("neutral", "enemy", "satru", "enemy"),
    ("enemy", "friend", "sama", "neutral"),
    ("enemy", "enemy", "adhisatru", "bad enemy"),
]


@pytest.mark.parametrize("nat,tmp,name,gloss", TABLE_8_PRINTED)
def test_3_4_3_table_8_cell_by_cell(nat, tmp, name, gloss):
    result = compound(nat, tmp)
    assert COMPOUND_NAMES[result] == name
    assert COMPOUND_GLOSS[result] == gloss


def test_3_4_3_six_cells_carry_five_names():
    """Natural-friend/temporary-enemy and natural-enemy/temporary-friend both
    give sama. So the grid is not a score that happens to work — it folds, and
    a caller cannot invert a compound relation back to its two inputs."""
    assert len(TABLE_8) == 6
    assert len(set(TABLE_8.values())) == 5
    assert compound(FRIEND, ENEMY) == compound(ENEMY, FRIEND) == NEUTRAL


def test_3_4_3_the_extremes_need_both_halves_to_agree():
    """Only friend+friend gives adhimitra and only enemy+enemy adhisatru."""
    assert compound(FRIEND, FRIEND) == GREAT_FRIEND
    assert compound(ENEMY, ENEMY) == GREAT_ENEMY
    assert [k for k, v in TABLE_8.items() if v == GREAT_FRIEND] == [(FRIEND, FRIEND)]
    assert [k for k, v in TABLE_8.items() if v == GREAT_ENEMY] == [(ENEMY, ENEMY)]


def test_3_4_3_a_temporary_neutral_is_rejected():
    """§3.4.2 produces only friend or enemy. Passing a neutral is a caller
    error, not a lookup miss to swallow."""
    with pytest.raises(RelationshipError, match="Table 8"):
        compound(FRIEND, NEUTRAL)
    with pytest.raises(RelationshipError):
        compound("great_friend", FRIEND)


def test_3_4_3_the_five_names():
    """Table 8's own vocabulary, and the same names §3.4.1 uses for three of
    them — mitra, sama, satru — with adhi- prefixed for the extremes."""
    assert COMPOUND_NAMES == {
        GREAT_FRIEND: "adhimitra", FRIEND: "mitra", NEUTRAL: "sama",
        ENEMY: "satru", GREAT_ENEMY: "adhisatru",
    }
    assert COMPOUND_NAMES[GREAT_FRIEND] == "adhi" + COMPOUND_NAMES[FRIEND]
    assert COMPOUND_NAMES[GREAT_ENEMY] == "adhi" + COMPOUND_NAMES[ENEMY]


def test_3_4_3_agrees_with_the_existing_chart_code():
    """`charts/dignity.py:compound_relation` predates this and feeds
    /v1/chart. It computes Table 8 as a sum rather than a lookup; the two must
    give the same answer for every cell."""
    from hora.charts.dignity import compound_relation
    from hora.core.ephemeris.base import PlanetPosition

    for nat_value, nat_name in ((2, FRIEND), (1, NEUTRAL), (0, ENEMY)):
        for tmp_house, tmp_name in ((2, FRIEND), (1, ENEMY)):
            # Find a real pair with this natural relation, then seat it so the
            # temporary relation is the one wanted.
            pair = next(
                (a, b) for a in CLASSICAL_SEVEN for b in CLASSICAL_SEVEN
                if a != b and c.NATURAL_RELATION[a][b] == nat_value
            )
            a, b = pair
            seats = {a: 0, b: (tmp_house - 1) % 12}
            positions = {
                g: PlanetPosition(
                    graha=g, longitude=r * 30.0 + 5.0, latitude=0.0,
                    distance=1.0, speed_longitude=1.0, speed_latitude=0.0,
                    speed_distance=0.0,
                )
                for g, r in seats.items()
            }
            assert temporary(seats[a], seats[b]) == tmp_name
            assert compound_relation(a, b, positions) == compound(nat_name, tmp_name)


# --------------------------------------------------------------------------
# Example 5 — compound relations in Lord Sree Rama's chart
# --------------------------------------------------------------------------

#: "Sun: ... Moon, Mars and Jupiter ... become adhimitras ... Mercury ...
#: becomes a mitra ... Venus becomes a sama ... Saturn ... an adhisatru."
EXAMPLE_5_SUN = {
    "Moon": "adhimitra", "Mars": "adhimitra", "Jupiter": "adhimitra",
    "Mercury": "mitra", "Venus": "sama", "Saturn": "adhisatru",
}

#: "Moon: ... Sun and Mercury ... become adhimitras ... Saturn ... becomes a
#: mitra ... Mars, Jupiter and Venus ... become satru."
EXAMPLE_5_MOON = {
    "Sun": "adhimitra", "Mercury": "adhimitra", "Saturn": "mitra",
    "Mars": "satru", "Jupiter": "satru", "Venus": "satru",
}


@pytest.mark.parametrize("graha,expected", [
    (Graha.SUN, EXAMPLE_5_SUN), (Graha.MOON, EXAMPLE_5_MOON),
])
def test_example_5_every_compound_relation(graha, expected):
    got = {r.other_name: r.compound_name for r in compound_row(graha, RAMA)}
    assert got == expected


def test_example_5_sun_venus_is_the_folded_cell():
    """"Venus is a natural enemy. Being a temporary friend, Venus becomes a
    sama (neutral) planet."

    The cell where a natural enemy softens to neutral — the same output as a
    natural friend gone temporarily hostile. Worth its own test because it is
    the one place the grid is not monotonic in the obvious way.
    """
    rel = next(r for r in compound_row(Graha.SUN, RAMA) if r.other == Graha.VENUS)
    assert (rel.natural, rel.temporary) == (ENEMY, FRIEND)
    assert rel.compound_name == "sama"


def test_example_5_sun_saturn_is_doubly_hostile():
    """"Saturn is the only temporary enemy of Sun. Being a natural enemy too,
    he becomes an adhisatru (bad enemy) of Sun."""
    rel = next(r for r in compound_row(Graha.SUN, RAMA) if r.other == Graha.SATURN)
    assert (rel.natural, rel.temporary) == (ENEMY, ENEMY)
    assert rel.compound_name == "adhisatru"


def test_example_5_moons_three_enemies_are_all_natural_neutrals():
    """"Moon's temporary enemies are Mars, Jupiter and Venus. They are all
    natural neutrals and they become satru (enemies)."

    Asserted as the book states it — that all three share the same natural
    relation — not just that the outcome is satru.
    """
    rows = {r.other_name: r for r in compound_row(Graha.MOON, RAMA)}
    for name in ("Mars", "Jupiter", "Venus"):
        assert rows[name].natural == NEUTRAL
        assert rows[name].temporary == ENEMY
        assert rows[name].compound_name == "satru"


def test_example_5_builds_on_example_4s_temporary_relations():
    """"We found in Example 4 that Sun's temporary friends are Mercury, Moon,
    Jupiter, Mars and Venus." The compound row must use exactly those."""
    temp = temporary_in_chart(Graha.SUN, RAMA)
    from_compound = {
        r.other for r in compound_row(Graha.SUN, RAMA) if r.temporary == FRIEND
    }
    assert from_compound == set(temp.friends)


def test_example_5_the_moon_has_no_adhisatru():
    """Table 7 gives the Moon no natural enemies, so no pair of the Moon's can
    reach adhisatru whatever the chart. A structural consequence worth pinning.
    """
    assert natural_row(Graha.MOON)[ENEMY] == []
    for rasi in range(12):
        chart = dict(RAMA) | {int(Graha.MOON): rasi}
        assert all(
            r.compound_name != "adhisatru" for r in compound_row(Graha.MOON, chart)
        )


# --------------------------------------------------------------------------
# The compound API
# --------------------------------------------------------------------------


def test_compound_endpoint_returns_the_whole_row_with_both_inputs():
    body = client.post(
        "/v1/relationship/compound", json={"graha": 0, "rasis": RAMA}
    ).json()
    got = {r["other_name"]: r["compound_name"] for r in body["relations"]}
    assert got == EXAMPLE_5_SUN
    saturn = next(r for r in body["relations"] if r["other_name"] == "Saturn")
    assert saturn["natural"] == "enemy"
    assert saturn["temporary"] == "enemy"
    assert saturn["compound_gloss"] == "bad enemy"


def test_compound_endpoint_takes_a_single_pair():
    body = client.post(
        "/v1/relationship/compound", json={"graha": 0, "rasis": RAMA, "other": 3}
    ).json()
    assert len(body["relations"]) == 1
    assert body["relations"][0]["compound_name"] == "mitra"


def test_compound_endpoint_rejects_a_graha_missing_from_the_chart():
    r = client.post(
        "/v1/relationship/compound", json={"graha": 0, "rasis": {0: 0}, "other": 3}
    )
    assert r.status_code == 400
    assert "no rasi" in r.json()["error"]["message"]


def test_rules_endpoint_serves_table_8():
    body = client.get("/v1/relationship/rules").json()["compound"]
    assert body["section"] == "3.4.3"
    assert len(body["table_8"]) == 3
    assert body["table_8"][0]["temporary_friend"] == "adhimitra"
    assert body["table_8"][0]["temporary_enemy"] == "sama"
    assert body["table_8"][2]["temporary_enemy"] == "adhisatru"
    assert "five" in body["six_cells_five_outcomes"]


# --------------------------------------------------------------------------
# Exercise 6 — compound relations of Jupiter and Venus
# --------------------------------------------------------------------------

#: "Jupiter: ... Sun becomes an adhimitra ... Saturn becomes a mitra ...
#: Mercury becomes a neutral ... Moon and Mars become sama ... Venus becomes
#: an enemy."
#:
#: The Venus cell is **not** what we return — see
#: test_exercise_6_jupiter_venus_is_pvr_3. Everything else matches.
EXERCISE_6_JUPITER_BOOK = {
    "Sun": "adhimitra", "Saturn": "mitra", "Mercury": "sama",
    "Moon": "sama", "Mars": "sama", "Venus": "satru",
}

#: "Venus: ... Mercury becomes an adhimitra ... Mars becomes a mitra ... Sun
#: becomes a sama ... Saturn becomes a sama ... Jupiter becomes a satru ...
#: Moon becomes an adhisatru." All six agree with Table 7.
EXERCISE_6_VENUS = {
    "Mercury": "adhimitra", "Mars": "mitra", "Sun": "sama",
    "Saturn": "sama", "Jupiter": "satru", "Moon": "adhisatru",
}


def test_exercise_6_venus_every_compound_relation():
    """Venus's whole row reproduces, all six."""
    got = {r.other_name: r.compound_name for r in compound_row(Graha.VENUS, RAMA)}
    assert got == EXERCISE_6_VENUS


@pytest.mark.parametrize("other", ["Sun", "Saturn", "Mercury", "Moon", "Mars"])
def test_exercise_6_jupiter_the_five_that_agree(other):
    """Five of Jupiter's six reproduce exactly."""
    got = {r.other_name: r.compound_name for r in compound_row(Graha.JUPITER, RAMA)}
    assert got[other] == EXERCISE_6_JUPITER_BOOK[other]


def test_exercise_6_jupiter_venus_is_pvr_3():
    """The one cell in Exercise 6 we do not reproduce, and why.

    The answer reads "Being a neutral planet in natural relationship, Venus
    becomes an enemy in compound relationship" — treating Venus as Jupiter's
    natural **neutral**. **Table 7 lists Venus among Jupiter's enemies**, and
    §3.4.1's derivation independently produces "enemy" for that pair, as it
    does for all 42.

    Two sources against one, and the two are the rule and its own printed
    output. So Venus is a natural enemy of Jupiter; a temporary enemy here
    too, which makes the compound **adhisatru**, not satru. PVR-3 / D-8.
    """
    rel = next(r for r in compound_row(Graha.JUPITER, RAMA) if r.other == Graha.VENUS)
    assert rel.natural == ENEMY, "Table 7"
    assert derive_natural(Graha.JUPITER, Graha.VENUS).relation == ENEMY, "3.4.1's rule"
    assert rel.temporary == ENEMY
    assert rel.compound_name == "adhisatru"
    assert EXERCISE_6_JUPITER_BOOK["Venus"] == "satru", "what the answer prints"


def test_exercise_6_the_deviation_is_one_cell_wide():
    """Jupiter/Venus is the only disagreement across both halves of Exercise
    6 — twelve relations. If a second ever appears, PVR-3 has grown and this
    fails rather than the new one passing unnoticed.
    """
    disagree = []
    for graha, expected in (
        (Graha.JUPITER, EXERCISE_6_JUPITER_BOOK), (Graha.VENUS, EXERCISE_6_VENUS)
    ):
        for r in compound_row(graha, RAMA):
            if r.compound_name != expected[r.other_name]:
                disagree.append((r.graha_name, r.other_name))
    assert disagree == [("Jupiter", "Venus")]


def test_exercise_6_the_reverse_direction_agrees_with_the_book():
    """Venus's own row calls Jupiter "a natural neutral", which **is** Table
    7's value for Venus to Jupiter. So the conflict is one-directional: only
    Jupiter's view of Venus is disputed, not Venus's view of Jupiter.
    """
    assert natural(Graha.VENUS, Graha.JUPITER) == NEUTRAL
    assert natural(Graha.JUPITER, Graha.VENUS) == ENEMY
    rel = next(r for r in compound_row(Graha.VENUS, RAMA) if r.other == Graha.JUPITER)
    assert rel.natural == NEUTRAL
    assert rel.compound_name == "satru" == EXERCISE_6_VENUS["Jupiter"]


def test_exercise_6_builds_on_exercise_5s_temporary_relations():
    """"We found in Exercise 5 that the temporary friends of Jupiter are Sun,
    Mercury and Saturn." The compound row must use exactly those."""
    for graha, friends in (
        (Graha.JUPITER, {"Sun", "Mercury", "Saturn"}),
        (Graha.VENUS, {"Sun", "Mars", "Mercury"}),
    ):
        from_compound = {
            r.other_name for r in compound_row(graha, RAMA) if r.temporary == FRIEND
        }
        assert from_compound == friends


# --------------------------------------------------------------------------
# The friendly/inimical house convention the book adopts here
# --------------------------------------------------------------------------


def test_a_friendly_house_is_defined_by_the_compound_relation():
    """"Whenever we refer to a planet being in a friendly house or an inimical
    house in the rest of this book, we mean the compound relationships. A
    planet occupying a rasi owned by a mitra or adhimitra is in a friendly
    house. A planet occupying a rasi owned by a satru or adhisatru is in an
    inimical house."

    So sama is **neither** — a rasi owned by a sama is neither friendly nor
    inimical, and a three-way split would be wrong.
    """
    friendly = {GREAT_FRIEND, FRIEND}
    inimical = {GREAT_ENEMY, ENEMY}
    assert friendly & inimical == set()
    assert NEUTRAL not in friendly | inimical
    assert friendly | inimical | {NEUTRAL} == set(COMPOUND_NAMES)


def test_the_friendly_house_convention_uses_the_rasi_lord():
    """A planet is in a friendly house by its relation to the **lord of the
    rasi it sits in** — not to the planets sitting with it. In Rama's chart
    the Sun is in Aries, lorded by Mars, and Mars is the Sun's adhimitra.
    """
    lord = int(c.RASI_LORD[RAMA[int(Graha.SUN)]])
    assert str(c.GRAHA_NAMES[lord]) == "Mars"
    rel = next(r for r in compound_row(Graha.SUN, RAMA) if r.other == lord)
    assert rel.compound in {GREAT_FRIEND, FRIEND}


def test_this_is_the_convention_the_chart_code_already_uses():
    """`charts/dignity.py:dignity_with_relations` resolves a neutral sign by
    the compound relation to the rasi lord, which is this rule. Asserted so
    the convention and the implementation stay tied together."""
    import inspect

    from hora.charts.dignity import dignity_with_relations

    source = inspect.getsource(dignity_with_relations)
    assert "RASI_LORD" in source
    assert "compound_relation" in source


# --------------------------------------------------------------------------
# The one-call chart view
# --------------------------------------------------------------------------
#
# The three pairwise endpoints answer a single question each and take three
# different input shapes. A caller building a reading wants the whole of §3.4
# for one chart without joining anything by hand — which is also how JHora
# presents it, as a single grid rather than a pair lookup.


def test_the_chart_view_returns_a_full_matrix():
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    assert body["grahas"] == list(CLASSICAL_SEVEN)
    assert len(body["matrix"]) == 7
    for row in body["matrix"]:
        assert len(row["relations"]) == 7


def test_the_matrix_diagonal_is_null():
    """A graha has no relationship to itself, so the diagonal is not a value
    to invent."""
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    for i, row in enumerate(body["matrix"]):
        assert row["relations"][i] is None
        assert all(r is not None for j, r in enumerate(row["relations"]) if j != i)


def test_the_matrix_agrees_with_the_pairwise_endpoint():
    """One call must give the same answers as forty-two."""
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    for row in body["matrix"]:
        for cell in row["relations"]:
            if cell is None:
                continue
            single = client.post(
                "/v1/relationship/compound",
                json={"graha": row["graha"], "rasis": RAMA, "other": cell["other"]},
            ).json()["relations"][0]
            assert cell == single


def test_the_matrix_is_not_symmetric():
    """Natural relations are asymmetric, so the grid is too. A caller that
    read only the upper triangle would be wrong."""
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    cells = {
        (row["graha"], c["other"]): c["compound"]
        for row in body["matrix"] for c in row["relations"] if c
    }
    assert any(cells[(a, b)] != cells[(b, a)] for a, b in cells)


def test_the_chart_view_reproduces_example_5_and_exercise_6():
    """The comprehensive call must not drift from the worked examples."""
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    by_graha = {r["graha_name"]: r for r in body["matrix"]}
    for name, expected in (
        ("Sun", EXAMPLE_5_SUN), ("Moon", EXAMPLE_5_MOON), ("Venus", EXERCISE_6_VENUS),
    ):
        got = {
            c["other_name"]: c["compound_name"]
            for c in by_graha[name]["relations"] if c
        }
        assert got == expected, name


def test_the_per_graha_rollup_carries_all_three_levels():
    """Natural, temporary and compound for each graha, so a caller never has
    to make three calls and join them."""
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    sun = next(p for p in body["per_graha"] if p["graha_name"] == "Sun")
    assert set(sun["natural"]) == {"friend", "neutral", "enemy"}
    assert set(sun["temporary"]) == {"friends", "enemies"}
    assert sun["temporary"]["enemies"] == [int(Graha.SATURN)], "Example 4"
    assert int(Graha.SATURN) in sun["compound"]["great_enemies"], "Example 5"


def test_the_rollup_groups_match_the_matrix():
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    by_graha = {r["graha"]: r for r in body["matrix"]}
    for entry in body["per_graha"]:
        cells = [c for c in by_graha[entry["graha"]]["relations"] if c]
        for key, label in (
            ("great_friends", "great_friend"), ("friends", "friend"),
            ("neutrals", "neutral"), ("enemies", "enemy"),
            ("great_enemies", "great_enemy"),
        ):
            assert sorted(entry["compound"][key]) == sorted(
                c["other"] for c in cells if c["compound"] == label
            ), (entry["graha_name"], key)


# --------------------------------------------------------------------------
# The friendly / inimical house standing — what the rest of the book consumes
# --------------------------------------------------------------------------

#: Rama's chart, worked from Table 7, §3.4.2 and Table 8.
RAMA_HOUSES = {
    "Sun": ("Mars", "great_friend", "friendly"),
    "Moon": ("Moon", None, "neither"),
    "Mars": ("Saturn", "friend", "friendly"),
    "Mercury": ("Venus", "great_friend", "friendly"),
    "Jupiter": ("Moon", "neutral", "neither"),
    "Venus": ("Jupiter", "enemy", "inimical"),
    "Saturn": ("Venus", "neutral", "neither"),
}


@pytest.mark.parametrize("name,expected", list(RAMA_HOUSES.items()))
def test_the_house_standing_of_each_graha(name, expected):
    """§3.4.3's convention, applied to the chart both examples use."""
    lord, relation, standing = expected
    result = house_standing(N[name], RAMA)
    assert result.lord_name == lord
    assert result.relation_to_lord == relation
    assert result.house == standing


def test_a_graha_in_its_own_rasi_is_in_neither_house():
    """The Moon is in Cancer, which it lords. It has no relationship to
    itself, so §3.4.3's test does not apply — reported as neither rather than
    forced into friendly."""
    result = house_standing(Graha.MOON, RAMA)
    assert result.owns_the_rasi is True
    assert result.relation_to_lord is None
    assert result.house == "neither"


def test_a_sama_lord_gives_neither_house():
    """"...owned by a mitra or adhimitra ... owned by a satru or adhisatru."
    Sama appears in neither clause, so a rasi owned by a sama is neither
    friendly nor inimical. Saturn in Libra, lorded by a sama Venus, is the
    case in this chart."""
    result = house_standing(Graha.SATURN, RAMA)
    assert result.relation_to_lord == NEUTRAL
    assert result.house == "neither"


def test_the_house_standing_is_published_in_the_chart_view():
    body = client.post("/v1/relationship/chart", json={"rasis": RAMA}).json()
    got = {
        p["graha_name"]: (
            p["house"]["lord_name"], p["house"]["relation_to_lord"],
            p["house"]["standing"],
        )
        for p in body["per_graha"]
    }
    assert got == RAMA_HOUSES
    assert "friendly house" in body["friendly_house_note"]


def test_the_house_standing_uses_the_rasi_lord_not_the_co_tenants():
    """Jupiter shares Cancer with the Moon. Its standing comes from the Moon
    *as lord of Cancer*, not from co-tenancy — and those are different
    questions: the Moon is a temporary enemy of Jupiter for sharing the rasi,
    yet the compound relation used here is neutral."""
    standing = house_standing(Graha.JUPITER, RAMA)
    assert standing.lord == int(Graha.MOON)
    assert standing.relation_to_lord == NEUTRAL
    assert temporary(RAMA[int(Graha.JUPITER)], RAMA[int(Graha.MOON)]) == ENEMY


def test_the_chart_view_rejects_a_chart_with_a_bad_rasi():
    r = client.post("/v1/relationship/chart", json={"rasis": {0: 0, 1: 99}})
    assert r.status_code in (400, 422)


def test_the_chart_view_works_with_a_partial_chart():
    """A caller with only some grahas placed gets those, not an error."""
    body = client.post(
        "/v1/relationship/chart", json={"rasis": {0: 0, 6: 6}}
    ).json()
    assert body["grahas"] == [0, 6]
    assert len(body["matrix"]) == 2
    assert body["matrix"][0]["relations"][1]["compound_name"] == "adhisatru"


def test_an_unplaced_rasi_lord_gives_unknown_not_neither():
    """The Sun in Aries needs Mars, its rasi lord, to have a seat before
    §3.4.3's test can run. In a partial chart without Mars the answer is
    **unknown** — the rule could not be applied.

    "neither" is a verdict: the rule ran and the lord turned out to be a sama,
    or the graha owns the rasi. Collapsing the two would tell a caller the
    Sun is in no particular house when the truth is that we cannot say.
    """
    partial = house_standing(Graha.SUN, {int(Graha.SUN): 0, int(Graha.SATURN): 6})
    assert partial.lord_name == "Mars"
    assert partial.relation_to_lord is None
    assert partial.house == "unknown"

    full = house_standing(Graha.SUN, RAMA)
    assert full.house == "friendly"

    own = house_standing(Graha.MOON, RAMA)
    assert own.house == "neither" and own.owns_the_rasi
