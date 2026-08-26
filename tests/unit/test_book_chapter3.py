"""Every claim in Chapter 3 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 3 (Planets),
book pages 28-40.

Unlike Chapter 2 this chapter carries real calculation: Table 6 dignities, the
derivation rule for natural relationships, temporary relationships, and the
compound table. Those are exercised through production code — never re-derived
here — using Lord Sree Rama's chart, which the book uses for Examples 4 and 5
and Exercises 5 and 6.

Deviations are recorded in docs/book-deviations.md (D-4 to D-7).
"""
import pytest

from hora.charts.dignity import compound_relation, sign_dignity, temporal_relation
from hora.core.const import (
    DEBILITATION_RASI,
    DIG_BALA_STRONG_HOUSE,
    DIGNITY_BY_DEGREE,
    EXALTATION_DEG,
    EXALTATION_RASI,
    GRAHA_NAMES,
    GRAHA_OWNS,
    MOOLATRIKONA,
    NATURAL_BENEFIC,
    NATURAL_MALEFIC,
    NATURAL_RELATION,
    RASI_ABBR,
    RASI_LORD,
    Graha,
    Rasi,
)
from hora.core.ephemeris.base import PlanetPosition

RASI_BY_ABBR = {a: i for i, a in enumerate(RASI_ABBR)}


def rasi(abbr: str) -> int:
    return RASI_BY_ABBR[abbr]


# --------------------------------------------------------------------------
# Lord Sree Rama's chart — book Figure 1, used by Examples 4/5, Exercises 5/6
#
# Ar Sun; Ta Mercury; Ge Ketu; Cn lagna, Moon and Jupiter; Li Saturn;
# Sg Rahu; Cp Mars; Pi Venus.
# --------------------------------------------------------------------------

RAMA_PLACEMENTS = {
    Graha.SUN: "Ar", Graha.MERCURY: "Ta", Graha.KETU: "Ge",
    Graha.MOON: "Cn", Graha.JUPITER: "Cn", Graha.SATURN: "Li",
    Graha.RAHU: "Sg", Graha.MARS: "Cp", Graha.VENUS: "Pi",
}

#: The book's relationship analysis covers the seven classical planets only —
#: Example 4 lists Ketu's rasi among Sun's friendly rasis but omits Ketu from
#: the friend list.
SEVEN = [Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
         Graha.JUPITER, Graha.VENUS, Graha.SATURN]


@pytest.fixture(scope="module")
def rama():
    """Positions dict for Rama's chart, at mid-sign longitudes."""
    return {
        g: PlanetPosition(
            graha=int(g), longitude=rasi(abbr) * 30.0 + 15.0, latitude=0.0,
            distance=1.0, speed_longitude=1.0, speed_latitude=0.0, speed_distance=0.0,
        )
        for g, abbr in RAMA_PLACEMENTS.items()
    }


def names(grahas) -> set[str]:
    return {GRAHA_NAMES[g] for g in grahas}


# --------------------------------------------------------------------------
# 3.2.2 Benefics and malefics
# --------------------------------------------------------------------------

def test_natural_benefics():
    """3.2.2: Jupiter and Venus. Mercury and Moon are conditional."""
    assert names(NATURAL_BENEFIC) == {"Jupiter", "Venus"}


def test_saturn_is_kept_as_a_natural_malefic():
    """3.2.2 omits Saturn, but page 102 says "Malefics like Mars, Saturn and
    nodes". The omission is a slip. See book-deviations.md D-7."""
    assert names(NATURAL_MALEFIC) == {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


# --------------------------------------------------------------------------
# 3.3 Table 6 — dignities
# --------------------------------------------------------------------------

TABLE_6 = {
    Graha.SUN:     (["Le"], "Ar", 10.0, "Li", "Le"),
    Graha.MOON:    (["Cn"], "Ta", 3.0, "Sc", "Ta"),
    Graha.MARS:    (["Ar", "Sc"], "Cp", 28.0, "Cn", "Ar"),
    Graha.MERCURY: (["Ge", "Vi"], "Vi", 15.0, "Pi", "Vi"),
    Graha.JUPITER: (["Sg", "Pi"], "Cn", 5.0, "Cp", "Sg"),
    Graha.VENUS:   (["Ta", "Li"], "Pi", 27.0, "Vi", "Li"),
    Graha.SATURN:  (["Cp", "Aq"], "Li", 20.0, "Ar", "Aq"),
    Graha.RAHU:    (["Aq"], "Ge", None, "Sg", "Vi"),
    Graha.KETU:    (["Sc"], "Sg", None, "Ge", "Pi"),
}


@pytest.mark.parametrize("graha", list(TABLE_6))
def test_table_6_owned_rasis(graha):
    own, _, _, _, _ = TABLE_6[graha]
    assert [RASI_ABBR[r] for r in GRAHA_OWNS[graha]] == own


@pytest.mark.parametrize("graha", list(TABLE_6))
def test_table_6_exaltation_and_debilitation_rasi(graha):
    _, ex, _, deb, _ = TABLE_6[graha]
    assert RASI_ABBR[EXALTATION_RASI[graha]] == ex
    assert RASI_ABBR[DEBILITATION_RASI[graha]] == deb


@pytest.mark.parametrize("graha", list(TABLE_6))
def test_table_6_deep_exaltation_degree(graha):
    _, _, deg, _, _ = TABLE_6[graha]
    if deg is None:
        # Table 6 gives no degree for the nodes; none may be invented.
        assert graha not in EXALTATION_DEG
    else:
        assert EXALTATION_DEG[graha] % 30.0 == pytest.approx(deg)


@pytest.mark.parametrize("graha", list(TABLE_6))
def test_table_6_moolatrikona_rasi(graha):
    _, _, _, _, mt = TABLE_6[graha]
    assert RASI_ABBR[MOOLATRIKONA[graha][0]] == mt


def test_node_exaltations_follow_the_book_not_the_common_reading():
    """D-4: the book gives Gemini and Sagittarius, not Taurus and Scorpio."""
    assert EXALTATION_RASI[Graha.RAHU] == Rasi.GEMINI
    assert EXALTATION_RASI[Graha.KETU] == Rasi.SAGITTARIUS
    assert sign_dignity(Graha.RAHU, 65.0) == "exalted"        # Ge 5
    assert sign_dignity(Graha.KETU, 245.0) == "exalted"       # Sg 5
    assert sign_dignity(Graha.RAHU, 35.0) != "exalted"        # Ta 5


def test_node_ownership_never_overrides_rasi_lordship():
    """D-4: the nodes co-own Aquarius and Scorpio; the rasi lords are unchanged.

    If this ever regresses, two of every twelve house lords go wrong and
    lordship, argala and dasa lords break with them.
    """
    assert Rasi.AQUARIUS in GRAHA_OWNS[Graha.RAHU]
    assert Rasi.SCORPIO in GRAHA_OWNS[Graha.KETU]
    assert RASI_LORD[Rasi.AQUARIUS] == Graha.SATURN
    assert RASI_LORD[Rasi.SCORPIO] == Graha.MARS


# --------------------------------------------------------------------------
# 3.3 The seven degree-refined dignity rules
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "graha,sign,start,end",
    [
        (Graha.SUN, "Le", 0.0, 20.0),        # rule 1
        (Graha.MOON, "Ta", 3.0, 30.0),       # rule 2
        (Graha.MARS, "Ar", 0.0, 12.0),       # rule 3 (Table 6 says Ar; the rule text misprints Le)
        (Graha.MERCURY, "Vi", 15.0, 20.0),   # rule 4 — D-5
        (Graha.JUPITER, "Sg", 0.0, 10.0),    # rule 5
        (Graha.VENUS, "Li", 0.0, 15.0),      # rule 6
        (Graha.SATURN, "Aq", 0.0, 20.0),     # rule 7
    ],
)
def test_moolatrikona_degree_ranges(graha, sign, start, end):
    got = MOOLATRIKONA[graha]
    assert RASI_ABBR[got[0]] == sign
    assert (got[1], got[2]) == (start, end)


def test_mercury_dignity_across_virgo_follows_rule_4():
    """Exaltation 0-15, moolatrikona 15-20, own 20-30 — all through production code."""
    vi = Rasi.VIRGO * 30.0
    assert sign_dignity(Graha.MERCURY, vi + 7.0) == "exalted"
    assert sign_dignity(Graha.MERCURY, vi + 15.5) == "moolatrikona"
    assert sign_dignity(Graha.MERCURY, vi + 25.0) == "own"


def test_the_degree_that_D5_actually_changes():
    """D-5: 15-16 Virgo is moolatrikona under the book, own-sign under BPHS's 16."""
    assert sign_dignity(Graha.MERCURY, Rasi.VIRGO * 30.0 + 15.5) == "moolatrikona"


def test_sun_and_moon_degree_rules():
    assert sign_dignity(Graha.SUN, Rasi.LEO * 30.0 + 10.0) == "moolatrikona"
    assert sign_dignity(Graha.SUN, Rasi.LEO * 30.0 + 25.0) == "own"
    assert sign_dignity(Graha.MOON, Rasi.TAURUS * 30.0 + 1.0) == "exalted"
    assert sign_dignity(Graha.MOON, Rasi.TAURUS * 30.0 + 10.0) == "moolatrikona"


# --------------------------------------------------------------------------
# 3.2.15 Digbala
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "graha,house",
    [(Graha.MERCURY, 1), (Graha.JUPITER, 1), (Graha.SUN, 10), (Graha.MARS, 10),
     (Graha.MOON, 4), (Graha.VENUS, 4), (Graha.SATURN, 7)],
)
def test_digbala_directions(graha, house):
    assert DIG_BALA_STRONG_HOUSE[graha] == house


# --------------------------------------------------------------------------
# 3.4.1 Natural relationships — Table 7 and the rule that generates it
# --------------------------------------------------------------------------

TABLE_7 = {
    Graha.SUN:     ({"Moon", "Mars", "Jupiter"}, {"Mercury"}, {"Venus", "Saturn"}),
    Graha.MOON:    ({"Sun", "Mercury"}, {"Mars", "Jupiter", "Venus", "Saturn"}, set()),
    Graha.MARS:    ({"Sun", "Moon", "Jupiter"}, {"Venus", "Saturn"}, {"Mercury"}),
    Graha.MERCURY: ({"Sun", "Venus"}, {"Mars", "Jupiter", "Saturn"}, {"Moon"}),
    Graha.JUPITER: ({"Sun", "Moon", "Mars"}, {"Saturn"}, {"Mercury", "Venus"}),
    Graha.VENUS:   ({"Mercury", "Saturn"}, {"Mars", "Jupiter"}, {"Sun", "Moon"}),
    Graha.SATURN:  ({"Mercury", "Venus"}, {"Jupiter"}, {"Sun", "Moon", "Mars"}),
}


@pytest.mark.parametrize("graha", list(TABLE_7))
def test_table_7_natural_relationships(graha):
    friends, neutral, enemies = TABLE_7[graha]
    row = NATURAL_RELATION[graha]
    assert names(o for o in row if o != graha and row[o] == 2) == friends
    assert names(o for o in row if o != graha and row[o] == 1) == neutral
    assert names(o for o in row if o != graha and row[o] == 0) == enemies


@pytest.mark.parametrize("graha", list(TABLE_7))
def test_table_7_is_reproduced_by_the_books_own_derivation_rule(graha):
    """3.4.1 states how to derive the table; deriving it must give the table.

    "Take the moolatrikona. The lord of its exaltation rasi is a friend. Lords
    of the 2nd, 4th, 5th, 8th, 9th and 12th from it are friends. Lords of other
    rasis are enemies. A planet landing in both camps is neutral."
    """
    mt = MOOLATRIKONA[graha][0]
    friendly_rasis = {(mt + h - 1) % 12 for h in (2, 4, 5, 8, 9, 12)}
    friendly_rasis.add(EXALTATION_RASI[graha])

    friend_lords, enemy_lords = set(), set()
    for r in range(12):
        (friend_lords if r in friendly_rasis else enemy_lords).add(int(RASI_LORD[r]))

    for other in SEVEN:
        if other == graha:
            continue
        if other in friend_lords and other in enemy_lords:
            expected = 1
        elif other in friend_lords:
            expected = 2
        else:
            expected = 0
        assert NATURAL_RELATION[graha][other] == expected, GRAHA_NAMES[other]


# --------------------------------------------------------------------------
# 3.4.2 Temporary relationships — Example 4 and Exercise 5
# --------------------------------------------------------------------------

def temp_friends(graha, positions):
    return names(
        o for o in SEVEN
        if o != graha and temporal_relation(graha, o, positions) == 1
    )


def temp_enemies(graha, positions):
    return names(
        o for o in SEVEN
        if o != graha and temporal_relation(graha, o, positions) == 0
    )


@pytest.mark.parametrize(
    "graha,friends,enemies",
    [
        # Example 4
        (Graha.SUN, {"Mercury", "Moon", "Jupiter", "Mars", "Venus"}, {"Saturn"}),
        (Graha.MOON, {"Saturn", "Sun", "Mercury"}, {"Mars", "Jupiter", "Venus"}),
        # Exercise 5
        (Graha.JUPITER, {"Saturn", "Sun", "Mercury"}, {"Moon", "Mars", "Venus"}),
        (Graha.VENUS, {"Sun", "Mercury", "Mars"}, {"Moon", "Jupiter", "Saturn"}),
    ],
)
def test_temporary_relationships_in_ramas_chart(graha, friends, enemies, rama):
    assert temp_friends(graha, rama) == friends
    assert temp_enemies(graha, rama) == enemies


def test_moon_and_jupiter_share_temporary_relationships(rama):
    """The book notes this: they occupy the same rasi, so the sets coincide."""
    assert temp_friends(Graha.MOON, rama) - {"Jupiter"} == \
        temp_friends(Graha.JUPITER, rama) - {"Moon"}


# --------------------------------------------------------------------------
# 3.4.3 Compound relationships — Table 8, Example 5 and Exercise 6
# --------------------------------------------------------------------------

#: Table 8's Sanskrit names against our internal labels.
COMPOUND = {
    "adhimitra": "great_friend", "mitra": "friend", "sama": "neutral",
    "satru": "enemy", "adhisatru": "great_enemy",
}


@pytest.mark.parametrize(
    "graha,expected",
    [
        # Example 5 — Sun
        (Graha.SUN, {"Moon": "adhimitra", "Mars": "adhimitra", "Jupiter": "adhimitra",
                     "Mercury": "mitra", "Venus": "sama", "Saturn": "adhisatru"}),
        # Example 5 — Moon
        (Graha.MOON, {"Sun": "adhimitra", "Mercury": "adhimitra", "Saturn": "mitra",
                      "Mars": "satru", "Jupiter": "satru", "Venus": "satru"}),
        # Exercise 6 — Jupiter.
        # Venus is "adhisatru" here, not the "satru" the exercise prose gives:
        # the prose calls Venus a natural neutral, but Table 7 and the section
        # 3.4.1 derivation rule both make Venus a natural enemy of Jupiter.
        # See book-deviations.md D-8.
        (Graha.JUPITER, {"Sun": "adhimitra", "Saturn": "mitra", "Mercury": "sama",
                         "Moon": "sama", "Mars": "sama", "Venus": "adhisatru"}),
        # Exercise 6 — Venus
        (Graha.VENUS, {"Mercury": "adhimitra", "Mars": "mitra", "Sun": "sama",
                       "Saturn": "sama", "Jupiter": "satru", "Moon": "adhisatru"}),
    ],
)
def test_compound_relationships_in_ramas_chart(graha, expected, rama):
    for other_name, sanskrit in expected.items():
        other = GRAHA_NAMES.index(other_name)
        assert compound_relation(graha, other, rama) == COMPOUND[sanskrit], other_name


def test_table_8_covers_all_six_combinations():
    """Every natural x temporary pairing must land on the right label."""
    combos = {
        (2, 1): "great_friend",   # natural friend  + temporary friend
        (2, 0): "neutral",        # natural friend  + temporary enemy
        (1, 1): "friend",         # natural neutral + temporary friend
        (1, 0): "enemy",          # natural neutral + temporary enemy
        (0, 1): "neutral",        # natural enemy   + temporary friend
        (0, 0): "great_enemy",    # natural enemy   + temporary enemy
    }
    for (natural, temporary), label in combos.items():
        total = natural + temporary * 2
        assert {4: "great_friend", 3: "friend", 2: "neutral",
                1: "enemy", 0: "great_enemy"}[total] == label


def test_exercise_6_jupiter_venus_follows_table_7_not_the_prose():
    """D-8: the book's Exercise 6 answer contradicts its own Table 7.

    Table 7 makes Venus a natural enemy of Jupiter, and the section 3.4.1
    derivation rule independently agrees. The exercise prose calls Venus a
    natural neutral. We follow the table.
    """
    assert NATURAL_RELATION[Graha.JUPITER][Graha.VENUS] == 0     # enemy, not neutral


@pytest.mark.parametrize("graha", list(TABLE_6))
def test_moolatrikona_tables_cannot_drift_apart(graha):
    """MOOLATRIKONA and DIGNITY_BY_DEGREE both carry the moolatrikona arc.

    They are separate tables, so an edit to one could silently leave the other
    behind — a mutation of Mercury's 15 degrees in MOOLATRIKONA alone was caught
    by only one test before this existed.
    """
    rules = [r for r in DIGNITY_BY_DEGREE.get(graha, ()) if r[3] == "moolatrikona"]
    if not rules:
        # Only the seven classical planets have degree rules in section 3.3.
        assert graha in (Graha.RAHU, Graha.KETU)
        return
    assert len(rules) == 1
    rule_rasi, start, end, _ = rules[0]
    assert (rule_rasi, start, end) == MOOLATRIKONA[graha]


# --------------------------------------------------------------------------
# 3.2.15 Strength by time — the three rules
# --------------------------------------------------------------------------

def test_strength_by_time_of_day():
    from hora.core.const import STRONG_ALWAYS, STRONG_AT_NIGHT, STRONG_BY_DAY

    assert names(STRONG_AT_NIGHT) == {"Moon", "Mars", "Saturn"}
    assert names(STRONG_BY_DAY) == {"Sun", "Jupiter", "Venus"}
    assert names(STRONG_ALWAYS) == {"Mercury"}


def test_every_classical_planet_has_a_time_of_day_strength():
    from hora.core.const import STRONG_ALWAYS, STRONG_AT_NIGHT, STRONG_BY_DAY

    assert set(SEVEN) == set(STRONG_AT_NIGHT | STRONG_BY_DAY | STRONG_ALWAYS)


def test_paksha_strength():
    """3.2.15: benefics strong in Sukla paksha, malefics in Krishna."""
    from hora.core.const import (
        BENEFIC_STRONG_PAKSHA,
        MALEFIC_STRONG_PAKSHA,
        PAKSHA_NAMES,
    )

    assert PAKSHA_NAMES[BENEFIC_STRONG_PAKSHA] == "Sukla"
    assert PAKSHA_NAMES[MALEFIC_STRONG_PAKSHA] == "Krishna"


def test_ayana_strength():
    """3.2.15: benefics strong in Uttara ayana, malefics in Dakshina."""
    from hora.core.const import AYANA_NAMES, BENEFIC_STRONG_AYANA, MALEFIC_STRONG_AYANA

    assert AYANA_NAMES[BENEFIC_STRONG_AYANA] == "uttara"
    assert AYANA_NAMES[MALEFIC_STRONG_AYANA] == "dakshina"


@pytest.mark.parametrize(
    "rasi_name,ayana",
    [("Cp", "uttara"), ("Aq", "uttara"), ("Pi", "uttara"),
     ("Ar", "uttara"), ("Ta", "uttara"), ("Ge", "uttara"),
     ("Cn", "dakshina"), ("Le", "dakshina"), ("Vi", "dakshina"),
     ("Li", "dakshina"), ("Sc", "dakshina"), ("Sg", "dakshina")],
)
def test_footnote_5_ayana_boundaries(rasi_name, ayana):
    """Footnote 5: Uttara runs Cp to Ge, Dakshina runs Cn to Sg."""
    from hora.core.const import AYANA_NAMES, RASI_AYANA

    assert AYANA_NAMES[RASI_AYANA[rasi(rasi_name)]] == ayana


def test_footnote_6_six_ritus_of_two_months_each():
    from hora.core.const import RITU_MEANINGS, RITU_MONTHS, RITU_NAMES, RITU_RULER

    assert len(RITU_NAMES) == len(RITU_MEANINGS) == len(RITU_RULER) == 6
    assert RITU_MONTHS == 2
    assert RITU_MONTHS * len(RITU_NAMES) == 12


@pytest.mark.parametrize(
    "index,name,meaning,ruler",
    [(0, "vasanta", "spring", "Venus"), (1, "greeshma", "summer", "Mars"),
     (2, "varsha", "rainy season", "Moon"), (3, "hemanta", "season of dew", "Mercury"),
     (4, "seeta", "winter", "Jupiter"), (5, "sisira", "fall", "Saturn")],
)
def test_ritu_rulers(index, name, meaning, ruler):
    from hora.core.const import RITU_MEANINGS, RITU_NAMES, RITU_RULER

    assert RITU_NAMES[index] == name
    assert RITU_MEANINGS[index] == meaning
    assert GRAHA_NAMES[RITU_RULER[index]] == ruler


# --------------------------------------------------------------------------
# 3.2.8 Elements — rulers versus sharers
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "element,ruler",
    [("fire", "Mars"), ("earth", "Mercury"), ("air", "Saturn"),
     ("water", "Venus"), ("ether", "Jupiter")],
)
def test_element_rulers(element, ruler):
    from hora.core.const import ELEMENT_RULER, PLANET_ELEMENT_NAMES

    index = PLANET_ELEMENT_NAMES.index(element)
    assert GRAHA_NAMES[ELEMENT_RULER[index]] == ruler


def test_sun_and_moon_share_an_element_without_ruling_it():
    """3.2.8: "Sun also has the same nature" as fiery Mars; Moon as watery Venus."""
    from hora.core.const import ELEMENT_SHARERS, GRAHA_ELEMENT, PLANET_ELEMENT_NAMES

    assert PLANET_ELEMENT_NAMES[GRAHA_ELEMENT[Graha.SUN]] == "fire"
    assert PLANET_ELEMENT_NAMES[GRAHA_ELEMENT[Graha.MOON]] == "water"
    assert names(ELEMENT_SHARERS) == {"Sun", "Moon"}


# --------------------------------------------------------------------------
# Attribute table completeness
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "table,expected_size",
    [("GRAHA_AVATARA", 9), ("GRAHA_GOVERNS", 7), ("GRAHA_COLOR", 7),
     ("GRAHA_CABINET", 9), ("GRAHA_DEITY", 7), ("GRAHA_SEX", 7),
     ("GRAHA_ELEMENT", 7), ("GRAHA_VARNA", 7), ("GRAHA_GUNA", 7),
     ("GRAHA_ABODE", 7), ("GRAHA_DHATU", 7), ("GRAHA_TIME_PERIOD", 7),
     ("GRAHA_TASTE", 7), ("GRAHA_DHATU_MOOLA_JEEVA", 9)],
)
def test_attribute_tables_have_the_expected_coverage(table, expected_size):
    from hora.core import const

    assert len(getattr(const, table)) == expected_size


def test_mars_has_no_abode_and_none_is_invented():
    """3.2.11 names six abodes and omits Mars. See book-deviations.md D-7."""
    from hora.core.const import GRAHA_ABODE

    assert GRAHA_ABODE[Graha.MARS] is None
    assert all(v for g, v in GRAHA_ABODE.items() if g != Graha.MARS)
