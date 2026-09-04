"""Chapter 25 — transits read against natal reference points.

§25.1 gives the vocabulary and §25.2 the first reference, natal Moon. The seven
result tables it promises arrive one at a time; the last test here fails the
moment `STANDARD_RESULT_TABLES` and the built tables disagree, so the section
cannot be called finished early.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_ABBR

A = list(RASI_ABBR)
R = {abbr: index for index, abbr in enumerate(RASI_ABBR)}


def test_25_1_names_three_words_for_one_thing_and_four_for_the_other():
    """"By the transit or chaara or gochaara position..." and "By the natal or
    radical or birth or janma position..."
    """
    from hora.transits.gochara import (
        NATAL_MEANS,
        NATAL_SYNONYMS,
        TRANSIT_MEANS,
        TRANSIT_SYNONYMS,
    )

    assert TRANSIT_SYNONYMS == ("transit", "chaara", "gochaara")
    assert NATAL_SYNONYMS == ("natal", "radical", "birth", "janma")
    for word in TRANSIT_SYNONYMS:
        assert word in TRANSIT_MEANS
    for word in NATAL_SYNONYMS:
        assert word in NATAL_MEANS
    assert not set(TRANSIT_SYNONYMS) & set(NATAL_SYNONYMS)


def test_the_chapter_states_its_own_scope():
    """"Some methods normally employed in such correlation will be studied in
    this chapter."  Partial, and organised by reference point.
    """
    from hora.transits.gochara import CORRELATION_IS_THE_METHOD

    assert "several reference points" in CORRELATION_IS_THE_METHOD
    assert "Some methods" in CORRELATION_IS_THE_METHOD


def test_janma_rasi_is_natal_moons_sign():
    from hora.transits.gochara import JANMA_RASI_MEANS, janma_rasi

    assert janma_rasi(0.0) == R["Ar"]
    assert janma_rasi(359.99) == R["Pi"]
    assert janma_rasi(120.0) == R["Le"]
    assert "janma rasi" in JANMA_RASI_MEANS

    # Chart 3's Moon is 15 Le 28
    from hora.charts.book import longitudes
    assert janma_rasi(longitudes(3)["Moon"]) == R["Le"]


def test_the_house_from_janma_rasi_is_7_1s_ordinary_count():
    """Janma rasi itself is the 1st house, and the count is the one every
    other chapter uses -- `charts.house.house_of_rasi`, not a new rule.
    """
    from hora.charts.house import house_of_rasi
    from hora.transits.gochara import house_from_janma

    moon = R["Le"] * 30 + 15.0                   # janma rasi Leo
    got = house_from_janma(moon, R["Le"] * 30 + 2.0)
    assert got["house"] == 1                     # its own rasi
    assert got["janma_rasi_name"] == "Leo"

    assert house_from_janma(moon, R["Pi"] * 30 + 1.0)["house"] == 8
    assert house_from_janma(moon, R["Cn"] * 30 + 1.0)["house"] == 12

    for sign in range(12):
        assert house_from_janma(moon, sign * 30 + 5.0)["house"] == (
            house_of_rasi(R["Le"], sign))


def test_houses_from_janma_takes_a_whole_transit_chart():
    from hora.core.const import Graha
    from hora.transits.gochara import houses_from_janma

    moon = R["Le"] * 30 + 15.0
    got = houses_from_janma(moon, {
        int(Graha.SUN): R["Le"] * 30 + 1.0,
        int(Graha.MARS): R["Pi"] * 30 + 1.0,
        int(Graha.SATURN): R["Cn"] * 30 + 29.0,
    })
    assert got == {int(Graha.SUN): 1, int(Graha.MARS): 8,
                   int(Graha.SATURN): 12}


def test_the_dasa_lords_transit_agrees_with_24_5():
    """§25.2 singles out the Vimsottari dasa lord's transit because Vimsottari
    is the dasa of mind -- which is exactly what §24.5 said it specialises in.
    """
    from hora.core.const import DASA_SPECIALISATIONS
    from hora.transits.gochara import (
        MOON_IS_THE_MOST_POPULAR_REFERENCE,
        THE_DASA_LORDS_TRANSIT_MATTERS_MOST,
    )

    assert "significator of mind" in MOON_IS_THE_MOST_POPULAR_REFERENCE
    assert "mental state" in THE_DASA_LORDS_TRANSIT_MATTERS_MOST
    assert "Vimsottari dasa lord" in THE_DASA_LORDS_TRANSIT_MATTERS_MOST

    vimsottari = next(row for row in DASA_SPECIALISATIONS
                      if row["name"] == "Vimsottari dasa")
    assert "mind" in str(vimsottari["shows"])
    assert vimsottari["built_on"] == "the nakshatra of Moon"
    assert "mind" in str(vimsottari["focus"])


def test_the_tables_give_a_valence_and_the_natal_chart_the_subject():
    """"The results given by planets depend on what they stand for in the
    natal chart."  One transit, two subjects, decided by natal lordship.
    """
    from hora.transits.gochara import (
        THE_SUBJECT_COMES_FROM_NATAL_LORDSHIP,
        THE_TABLE_IS_NOT_THE_READING,
        THE_TABLES_ARE_REFERENCE_ONLY,
    )

    rows = THE_SUBJECT_COMES_FROM_NATAL_LORDSHIP
    assert len(rows) == 2
    assert {row["graha"] for row in rows} == {"Mars"}
    assert {row["transit_house"] for row in rows} == {8}      # one transit
    assert {row["result"] for row in rows} == {"worries"}     # one valence
    assert [row["natal_lordship"] for row in rows] == [5, 10]
    assert [row["about"] for row in rows] == ["children", "career"]

    assert "only for reference" in THE_TABLES_ARE_REFERENCE_ONLY
    assert "what the graha lords in" in THE_TABLE_IS_NOT_THE_READING


def test_the_seven_promised_tables_are_tracked_against_what_is_built():
    """§25.2 promises Table 53 to Table 59. This fails the moment a table is
    supplied and not registered, or registered and not built.
    """
    from hora.transits.gochara import (
        SEVEN_TABLES_ARE_PROMISED,
        STANDARD_RESULT_TABLES,
    )

    assert sorted(STANDARD_RESULT_TABLES) == list(range(53, 60))
    assert len(STANDARD_RESULT_TABLES) == 7
    assert "Table 53 - Table 59" in SEVEN_TABLES_ARE_PROMISED

    from hora.core.const import GRAHA_NAMES
    from hora.transits.gochara import STANDARD_RESULTS

    for row in STANDARD_RESULT_TABLES.values():
        assert (row["for"] is None) == (not row["built"])

    registered = {row["for"] for row in STANDARD_RESULT_TABLES.values()
                  if row["built"]}
    supplied = {str(GRAHA_NAMES[graha]) for graha in STANDARD_RESULTS}
    assert registered == supplied, (
        f"registered {registered} but built {supplied}")
    assert registered == {"Sun", "Moon", "Mars", "Mercury", "Jupiter",
                          "Venus", "Saturn"}            # all seven


def test_part_3s_opening_gave_no_roadmap_but_25_2_does():
    """Part 3 named no techniques; §25.2 names seven tables. So the section
    has a finish line even though the part does not.
    """
    from hora.core.const import PART_3_IS_KNOWINGLY_PARTIAL
    from hora.transits.gochara import STANDARD_RESULT_TABLES

    assert "Some of those techniques" in PART_3_IS_KNOWINGLY_PARTIAL
    assert len(STANDARD_RESULT_TABLES) == 7


def test_gochara_computes_no_positions():
    """Part 3's scope: both inputs come from elsewhere. Nothing in this module
    touches the ephemeris.
    """
    import ast
    import pathlib

    source = pathlib.Path("src/hora/transits/gochara.py").read_text()
    imported = {
        node.module for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert not any("ephemeris" in name or "swisseph" in name
                   for name in imported), imported
    assert "hora.charts.house" in imported          # reuses §7.1's count


@pytest.mark.parametrize(("longitude", "expected"),
                         [(-1.0, "Pi"), (360.0, "Ar"), (400.0, "Ta")])
def test_janma_rasi_wraps_rather_than_raising(longitude, expected):
    """`validate.longitude` reduces into 0-360 deliberately -- the zodiac is a
    circle and the book says to "expunge multiples of 360". A transit chart is
    the place that matters: a longitude accumulated across a year should wrap,
    not fail.
    """
    from hora.core.validate import InputError
    from hora.transits.gochara import janma_rasi

    assert A[janma_rasi(longitude)] == expected
    with pytest.raises(InputError):
        janma_rasi(float("nan"))


# ---------------------------------------------------------------------------
# Table 53 — Sun's transit from janma rasi
# ---------------------------------------------------------------------------

#: Table 53 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_53 = (
    (1, "Bad", "Financial loss, many travels, discomfort"),
    (2, "Bad", "Unhappiness, eye troubles, fear"),
    (3, "Good", "Wealth, good health, victory"),
    (4, "Bad", "Marital disharmony, loss of name"),
    (5, "Bad", "Bad health, fear from enemies"),
    (6, "Good", "Success over enemies, good health"),
    (7, "Bad", "Travels, physical pain"),
    (8, "Bad", "Disease, setbacks in marriage"),
    (9, "Bad", "Mental worries, obstacles"),
    (10, "Good", "Success, honors, gains"),
    (11, "Good", "Good health, prosperity, honors"),
    (12, "Bad", "Expenditure, losses"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_53)
def test_table_53_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.SUN, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Sun"


def test_table_53_is_twelve_rows_in_house_order_and_two_verdicts():
    from hora.transits.gochara import SNAPSHOTS, TABLE_53_SUN

    assert len(TABLE_53_SUN) == 12
    assert [row["house"] for row in TABLE_53_SUN] == list(range(1, 13))
    assert {row["snapshot"] for row in TABLE_53_SUN} == set(SNAPSHOTS)
    assert SNAPSHOTS == ("Good", "Bad")


def test_suns_good_houses_are_exactly_the_upachayas():
    """Table 53 marks the 3rd, 6th, 10th and 11th Good and the other eight
    Bad. Those four are §7's upachaya houses -- which Table 53 never names, so
    the identity is ours.
    """
    from hora.core.const import UPACHAYA, Graha
    from hora.transits.gochara import (
        SUNS_GOOD_HOUSES_ARE_THE_UPACHAYAS,
        TABLE_53_SUN,
        good_houses,
    )

    assert good_houses(Graha.SUN) == (3, 6, 10, 11)
    assert good_houses(Graha.SUN) == UPACHAYA

    bad = tuple(row["house"] for row in TABLE_53_SUN
                if row["snapshot"] == "Bad")
    assert set(bad) == set(range(1, 13)) - set(UPACHAYA)
    assert len(bad) == 8
    assert "does not name" in SUNS_GOOD_HOUSES_ARE_THE_UPACHAYAS


def test_every_row_carries_25_2s_caveat():
    """The table gives a valence; the caveat says the subject comes from the
    natal chart. A caller cannot get one without the other.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        THE_TABLES_ARE_REFERENCE_ONLY,
        transit_result,
    )

    for house in range(1, 13):
        assert transit_result(Graha.SUN, house)["caveat"] == (
            THE_TABLES_ARE_REFERENCE_ONLY)


def test_every_graha_now_resolves_to_a_table():
    """All seven tables are in, and §25.2's closing sentence sends the two
    nodes to Saturn's and Mars's. So nothing raises any more -- the guard is
    that the raise is still reachable, which a graha outside 0-8 proves.
    """
    from hora.core.const import Graha
    from hora.core.validate import InputError
    from hora.transits.gochara import good_houses, transit_result

    for graha in range(9):                       # Sun to Ketu
        assert transit_result(graha, 1)["snapshot"] in ("Good", "Bad")
        assert good_houses(graha)
    assert int(Graha.KETU) == 8

    with pytest.raises(InputError):
        transit_result(9, 1)


def test_read_transits_reports_what_is_missing_rather_than_dropping_it():
    """A whole transit chart read from janma rasi: the Sun gets a verdict and
    the rest are `undecided`, not absent.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import read_transits

    moon = R["Le"] * 30 + 15.0                   # janma rasi Leo
    got = read_transits(moon, {
        int(Graha.SUN): R["Li"] * 30 + 1.0,      # the 3rd from Leo
        int(Graha.SATURN): R["Pi"] * 30 + 1.0,   # the 8th
    })
    assert len(got) == 2

    sun = next(row for row in got if row["graha"] == int(Graha.SUN))
    assert (sun["house"], sun["snapshot"]) == (3, "Good")
    assert sun["results"] == "Wealth, good health, victory"
    assert sun["undecided"] is None

    saturn = next(row for row in got if row["graha"] == int(Graha.SATURN))
    assert saturn["house"] == 8
    assert saturn["snapshot"] == "Bad"           # every table is in now
    assert saturn["undecided"] is None


def test_the_suns_own_transit_of_a_real_chart():
    """Chart 3's janma rasi is Leo. On the day he became Prime Minister the
    Sun stood in Pisces -- the 8th from janma rasi, which Table 53 calls Bad.
    The caveat is the point: a snapshot is not the reading.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local
    from hora.transits.gochara import house_from_janma, transit_result

    record = chart(3)
    sworn_in = compute_chart(
        from_local(year=1998, month=3, day=19, hour=12, minute=0,
                   second=0.0, utc_offset_hours=5.5),
        Place(name="Chart 3", **record["place"]), Settings())

    natal_moon = longitudes(3)["Moon"]
    transit_sun = sworn_in.positions[int(Graha.SUN)].longitude
    where = house_from_janma(natal_moon, transit_sun)

    assert where["janma_rasi_name"] == "Leo"
    assert where["transit_rasi_name"] == "Pisces"
    assert where["house"] == 8
    assert transit_result(Graha.SUN, where["house"])["snapshot"] == "Bad"


# ---------------------------------------------------------------------------
# Table 54 — Moon's transit from janma rasi
# ---------------------------------------------------------------------------

#: Table 54 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_54 = (
    (1, "Good", "Comfort, good spirits"),
    (2, "Bad", "Obstacles, losses"),
    (3, "Good", "Gains, happiness"),
    (4, "Bad", "Lack of peace of mind, distrust"),
    (5, "Bad", "Failures, disappointments, sadness"),
    (6, "Good", "Happiness, health, wealth"),
    (7, "Good", "Respect, gains"),
    (8, "Bad", "Losses, tension, worries"),
    (9, "Bad", "Mental uneasiness"),
    (10, "Good", "Success, gains, authority"),
    (11, "Good", "Prosperity, comforts, gains"),
    (12, "Bad", "Injuries, expenditure, sadness"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_54)
def test_table_54_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.MOON, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Moon"


def test_table_54_is_twelve_rows_and_splits_the_houses_evenly():
    """Six Good and six Bad, where the Sun's table was four and eight."""
    from hora.core.const import Graha
    from hora.transits.gochara import SNAPSHOTS, TABLE_54_MOON, good_houses

    assert len(TABLE_54_MOON) == 12
    assert [row["house"] for row in TABLE_54_MOON] == list(range(1, 13))
    assert {row["snapshot"] for row in TABLE_54_MOON} == set(SNAPSHOTS)

    assert good_houses(Graha.MOON) == (1, 3, 6, 7, 10, 11)
    assert len(good_houses(Graha.MOON)) == 6
    assert len(good_houses(Graha.SUN)) == 4


def test_sun_and_moon_differ_only_on_the_1_7_axis():
    """Ten of twelve houses carry the same verdict in Tables 53 and 54. The
    two that do not are janma rasi itself and the house opposite it.
    """
    from hora.core.const import UPACHAYA, Graha
    from hora.transits.gochara import (
        SUN_AND_MOON_DIFFER_ONLY_ON_THE_1_7_AXIS,
        agreement,
        good_houses,
    )

    got = agreement(Graha.SUN, Graha.MOON)
    assert got["differ"] == (1, 7)
    assert len(got["agree"]) == 10
    assert set(got["agree"]) | set(got["differ"]) == set(range(1, 13))

    # and the difference goes one way only: Bad for Sun, Good for Moon
    for house in got["differ"]:
        assert house not in good_houses(Graha.SUN)
        assert house in good_houses(Graha.MOON)

    # so Sun's Good houses are a strict subset of Moon's, and both hold the
    # upachayas
    assert set(good_houses(Graha.SUN)) < set(good_houses(Graha.MOON))
    assert set(good_houses(Graha.MOON)) - set(good_houses(Graha.SUN)) == {1, 7}
    assert set(UPACHAYA) < set(good_houses(Graha.MOON))

    assert "1st and the 7th" in SUN_AND_MOON_DIFFER_ONLY_ON_THE_1_7_AXIS


def test_agreeing_snapshots_are_never_the_same_words():
    """The verdicts agreeing does not make the rows copies -- no house has the
    same typical results in both tables, including the ten that agree.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        AGREEING_SNAPSHOTS_ARE_NOT_THE_SAME_RESULTS,
        transit_result,
    )

    for house in range(1, 13):
        sun = transit_result(Graha.SUN, house)["results"]
        moon = transit_result(Graha.MOON, house)["results"]
        assert sun != moon, house
    assert "No house has the same typical results" in (
        AGREEING_SNAPSHOTS_ARE_NOT_THE_SAME_RESULTS)


def test_agreement_needs_both_tables_supplied():
    from hora.core.const import Graha
    from hora.transits.gochara import GocharaError, agreement

    assert agreement(Graha.SUN, Graha.SUN)["differ"] == ()
    # the nodes have no table of their own, so agreement() refuses them
    with pytest.raises(GocharaError, match="have not been supplied"):
        agreement(Graha.SUN, Graha.RAHU)


def test_read_transits_now_verdicts_two_grahas():
    from hora.core.const import Graha
    from hora.transits.gochara import read_transits

    moon = R["Le"] * 30 + 15.0                   # janma rasi Leo
    got = {row["graha"]: row for row in read_transits(moon, {
        int(Graha.SUN): R["Li"] * 30 + 1.0,      # the 3rd
        int(Graha.MOON): R["Le"] * 30 + 20.0,    # the 1st
        int(Graha.KETU): R["Pi"] * 30 + 1.0,     # the 8th, via Mars
    })}

    assert got[int(Graha.SUN)]["snapshot"] == "Good"
    assert got[int(Graha.MOON)]["house"] == 1
    assert got[int(Graha.MOON)]["snapshot"] == "Good"
    assert got[int(Graha.MOON)]["results"] == "Comfort, good spirits"
    assert got[int(Graha.KETU)]["from_graha_name"] == "Mars"


# ---------------------------------------------------------------------------
# Table 55 — Mars's transit from janma rasi
# ---------------------------------------------------------------------------

#: Table 55 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_55 = (
    (1, "Bad", "Troubles, bodily afflictions"),
    (2, "Bad", "Accidents, losses, thefts, quarrels"),
    (3, "Good", "Gains, power, wealth"),
    (4, "Bad", "Stomach problems, fevers, bad health"),
    (5, "Bad", "Troubles from enemies, trouble with children"),
    (6, "Good", "Success over enemies, wealth, success, well-being"),
    (7, "Bad", "Quarrels, marital troubles, eye problems"),
    (8, "Bad", "Worries, accidents, bad name, losses"),
    (9, "Bad", "Losses, insults, illness"),
    (10, "Bad", "Change of place, unexpected wealth"),
    (11, "Good", "Authority,  gains, good name"),
    (12, "Bad", "Expenses, quarrels with wife, diseases"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_55)
def test_table_55_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.MARS, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Mars"


def test_table_55_is_the_harshest_so_far():
    """Three Good houses against the Sun's four and the Moon's six."""
    from hora.core.const import Graha
    from hora.transits.gochara import TABLE_55_MARS, good_houses

    assert len(TABLE_55_MARS) == 12
    assert [row["house"] for row in TABLE_55_MARS] == list(range(1, 13))
    assert good_houses(Graha.MARS) == (3, 6, 11)
    assert [len(good_houses(g)) for g in
            (Graha.MARS, Graha.SUN, Graha.MOON)] == [3, 4, 6]


def test_the_rows_whose_results_fight_their_verdict():
    """Curated by reading every row, not by matching words -- a lexicon cannot
    tell "success of enemies" from "success", nor "discomfort" from "comfort".
    Three of the four are Venus's.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        MARS_IN_THE_TENTH_IS_MARKED_BAD_AND_READS_GOOD,
        MIXED_ROWS,
        transit_result,
    )

    assert [(row["graha"], row["house"]) for row in MIXED_ROWS] == [
        ("Mars", 10), ("Venus", 4), ("Venus", 10), ("Venus", 12),
        ("Saturn", 2)]
    assert sum(1 for row in MIXED_ROWS if row["graha"] == "Venus") == 3

    named = {"Mars": Graha.MARS, "Venus": Graha.VENUS,
             "Saturn": Graha.SATURN}
    for row in MIXED_ROWS:
        got = transit_result(named[str(row["graha"])], int(str(row["house"])))
        assert got["snapshot"] == row["snapshot"]
        fragment = str(row["against_it"]).split(" -- ")[0]
        assert fragment in str(got["results"])

    assert "unexpected wealth" in (
        MARS_IN_THE_TENTH_IS_MARKED_BAD_AND_READS_GOOD)


def test_the_three_tables_nest():
    """Mars's Good houses sit inside the Sun's, which sit inside the Moon's,
    and the steps between them are single houses.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        THE_FIRST_THREE_TABLES_NEST,
        agreement,
        good_houses,
    )

    mars = set(good_houses(Graha.MARS))
    sun = set(good_houses(Graha.SUN))
    moon = set(good_houses(Graha.MOON))
    assert mars < sun < moon

    assert sun - mars == {10}
    assert moon - sun == {1, 7}
    assert agreement(Graha.SUN, Graha.MARS)["differ"] == (10,)
    assert agreement(Graha.MOON, Graha.MARS)["differ"] == (1, 7, 10)
    assert "is inside" in THE_FIRST_THREE_TABLES_NEST


def test_common_ground_across_every_supplied_table():
    """With all seven in, only the 11th is Good in all of them and only the
    12th Bad in all. `tables` says how many were compared, so "always" cannot
    be read as more than it is.
    """
    from hora.transits.gochara import common_ground

    got = common_ground()
    assert got["tables"] == 7
    assert got["grahas"] == tuple(range(7))
    assert got["always_good"] == (11,)
    assert got["always_bad"] == (12,)
    assert got["varies"] == tuple(range(1, 11))

    assert len(got["always_good"]) + len(got["always_bad"]) + len(
        got["varies"]) == 12


# ---------------------------------------------------------------------------
# Table 56 — Mercury's transit from janma rasi
# ---------------------------------------------------------------------------

#: Table 56 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_56 = (
    (1, "Bad", "Quarrels, imprisonment, losses, poor advice"),
    (2, "Good", "Success, wealth, gains"),
    (3, "Bad", "Wandering, losses, trouble from authorities"),
    (4, "Good", "Prosperity in family, gains"),
    (5, "Bad", "Quarrels with wife and children, suffering"),
    (6, "Good", "Renown, success, ornaments"),
    (7, "Bad", "Quarrels, mental discomfort, addictions"),
    (8, "Good", "Childbirth, happiness, gains, success"),
    (9, "Bad", "Mental worries, obstacles"),
    (10, "Good", "Money, happiness, domestic harmony, success"),
    (11, "Good", "Childbirth, happiness, wealth"),
    (12, "Bad", "Disease, domestic disharmony, disease, losses"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_56)
def test_table_56_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.MERCURY, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Mercury"


def test_mercury_alternates_through_the_first_ten_houses():
    """Bad, Good, Bad, Good... for houses 1 to 10 -- the only periodic column
    in the section -- then Good and Bad, which every table gives 11 and 12.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        MERCURY_ALTERNATES_FOR_TEN_HOUSES,
        TABLE_56_MERCURY,
        good_houses,
    )

    verdicts = [row["snapshot"] for row in TABLE_56_MERCURY]
    assert verdicts[:10] == ["Bad", "Good"] * 5
    assert verdicts[10:] == ["Good", "Bad"]
    # the 11th breaks the run: alternation would have made it Bad
    assert verdicts[10] == verdicts[9] == "Good"

    assert good_houses(Graha.MERCURY) == (2, 4, 6, 8, 10, 11)
    assert "1 to 10" in MERCURY_ALTERNATES_FOR_TEN_HOUSES


def test_mercury_ends_the_nesting():
    """Tables 53 to 55 nested. Mercury is inside none of them and contains
    none of them, so the nesting was about the luminaries and Mars.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        THE_FIRST_THREE_TABLES_NEST,
        good_houses,
    )

    mercury = set(good_houses(Graha.MERCURY))
    for other in (Graha.SUN, Graha.MOON, Graha.MARS):
        theirs = set(good_houses(other))
        assert not mercury < theirs
        assert not theirs < mercury

    # what it disagrees with the other three about
    assert {2, 4, 8} <= mercury                  # all three call these Bad
    assert 3 not in mercury                      # all three call it Good
    assert "inside none of them" in THE_FIRST_THREE_TABLES_NEST


def test_the_11th_and_12th_have_not_varied_yet():
    """All seven tables in, the 11th is Good in every one and the 12th Bad in
    every one, and they are the only two houses undisputed.
    """
    from hora.transits.gochara import (
        THE_11TH_AND_12TH_HAVE_NOT_VARIED,
        common_ground,
    )

    got = common_ground()
    assert got["always_good"] == (11,)
    assert got["always_bad"] == (12,)
    assert "the only" in THE_11TH_AND_12TH_HAVE_NOT_VARIED


def test_the_twelfth_row_repeats_a_word_and_is_kept_that_way():
    """"Disease, domestic disharmony, disease, losses."  D-72 -- held as
    printed, because the repetition is likelier a slip for a fourth
    signification than a real duplicate.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        STANDARD_RESULTS,
        THE_TWELFTH_ROW_REPEATS_A_WORD,
        transit_result,
    )

    results = str(transit_result(Graha.MERCURY, 12)["results"])
    items = [item.strip().lower() for item in results.split(",")]
    assert items == ["disease", "domestic disharmony", "disease", "losses"]
    assert len(items) == 4 and len(set(items)) == 3      # kept, not collapsed

    # and it is the only such row in the four tables
    repeats = [
        (graha, row["house"]) for graha, rows in STANDARD_RESULTS.items()
        for row in rows
        if len({item.strip().lower()
                for item in str(row["results"]).split(",")})
        != len(str(row["results"]).split(","))
    ]
    assert repeats == [(int(Graha.MERCURY), 12)]
    assert "No other row" in THE_TWELFTH_ROW_REPEATS_A_WORD


def test_mercury_is_the_only_table_that_calls_the_eighth_good():
    """The 8th is Bad for the Sun, Moon and Mars and Good for Mercury --
    "Childbirth, happiness, gains, success".
    """
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    assert transit_result(Graha.MERCURY, 8)["snapshot"] == "Good"
    for other in (Graha.SUN, Graha.MOON, Graha.MARS):
        assert transit_result(other, 8)["snapshot"] == "Bad"


# ---------------------------------------------------------------------------
# Table 57 — Jupiter's transit from janma rasi
# ---------------------------------------------------------------------------

#: Table 57 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_57 = (
    (1, "Bad", "Loss of money and intelligence, Wandering"),
    (2, "Good", "Happiness, domestic harmony, success"),
    (3, "Bad", "Obstacles, loss of position, travels"),
    (4, "Bad", "Troubles, defeat, losses"),
    (5, "Good", "Childbirth, intelligence, prosperity, wealth"),
    (6, "Bad", "Mental uneasiness, enemies, worries"),
    (7, "Good", "Health, happiness, erotic pleasures, sense of well-being"),
    (8, "Bad", "Disease, imprisonment, illness, grief"),
    (9, "Good", "Success, wealth, childbirth, religiousness"),
    (10, "Bad", "Loss of position and money, ill-health, wandering"),
    (11, "Good", "Recovery of health and position, happiness"),
    (12, "Bad", "Fall from grace, misconduct, grief"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_57)
def test_table_57_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.JUPITER, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Jupiter"


def test_jupiter_overturns_three_standing_agreements():
    """The 6th had been Good in four tables and the 5th and 9th Bad in four.
    Table 57 reverses all three at once.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        JUPITER_OVERTURNS_THREE_STANDING_AGREEMENTS,
        transit_result,
    )

    earlier = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY)
    for other in earlier:
        assert transit_result(other, 6)["snapshot"] == "Good"
        assert transit_result(other, 5)["snapshot"] == "Bad"
        assert transit_result(other, 9)["snapshot"] == "Bad"

    assert transit_result(Graha.JUPITER, 6)["snapshot"] == "Bad"
    assert transit_result(Graha.JUPITER, 5)["snapshot"] == "Good"
    assert transit_result(Graha.JUPITER, 9)["snapshot"] == "Good"
    assert "first to call the 6th Bad" in (
        JUPITER_OVERTURNS_THREE_STANDING_AGREEMENTS)


def test_the_two_benefics_have_identical_agreement_profiles():
    """Jupiter and Venus each agree with the Sun, Moon and Mercury on five
    houses and with Mars on six -- the same four numbers -- and with each
    other on eight. Every cross-group pair is 5 or 6.

    Read against Table 57 alone this looked like Jupiter being an outlier;
    Table 58 shows it is a pair.
    """
    import itertools

    from hora.core.const import Graha
    from hora.transits.gochara import (
        STANDARD_RESULTS,
        TABLE_GROUPS,
        THE_TWO_BENEFICS_FORM_A_PAIR,
        agreement,
    )

    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Mercury": Graha.MERCURY, "Jupiter": Graha.JUPITER,
             "Venus": Graha.VENUS, "Saturn": Graha.SATURN}
    first = {int(named[name]) for name in TABLE_GROUPS[0]}
    second = {int(named[name]) for name in TABLE_GROUPS[1]}
    assert first | second == set(STANDARD_RESULTS)
    assert not first & second

    def profile(graha):
        return sorted(len(agreement(graha, other)["agree"])
                      for other in first)

    assert profile(Graha.JUPITER) == profile(Graha.VENUS) == [5, 5, 5, 6, 6]
    assert len(agreement(Graha.JUPITER, Graha.VENUS)["agree"]) == 8

    cross, within = [], []
    for a, b in itertools.combinations(sorted(STANDARD_RESULTS), 2):
        score = len(agreement(a, b)["agree"])
        (cross if (a in first) != (b in first) else within).append(score)
    assert max(cross) == 6
    assert min(within) == 6 and max(within) == 12

    assert "the same five numbers" in THE_TWO_BENEFICS_FORM_A_PAIR


def test_only_the_11th_and_12th_survive_all_seven_tables():
    """The section's agreements narrowed table by table -- three Good and six
    Bad after Mars, two and three after Mercury, one and one after Jupiter --
    and Venus leaves them where Jupiter did.
    """
    from hora.transits.gochara import STANDARD_RESULTS, common_ground

    got = common_ground()
    assert got["tables"] == len(STANDARD_RESULTS) == 7
    assert got["always_good"] == (11,)
    assert got["always_bad"] == (12,)
    assert len(got["varies"]) == 10

    for graha, rows in STANDARD_RESULTS.items():
        assert rows[10]["snapshot"] == "Good", graha      # the 11th
        assert rows[11]["snapshot"] == "Bad", graha       # the 12th


# ---------------------------------------------------------------------------
# Table 58 — Venus's transit from janma rasi
# ---------------------------------------------------------------------------

#: Table 58 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_58 = (
    (1, "Good", "Comforts, pleasures, happiness, good spirits"),
    (2, "Good", "Money, fortune, erotic pleasures, childbirth"),
    (3, "Good", "Respect, wealth, good spirits"),
    (4, "Good", "Prosperity, success of enemies, comforts"),
    (5, "Good", "Fame, power, good name"),
    (6, "Bad", "Loss of fame, bad name, quarrels"),
    (7, "Bad", "Humiliation, disease, troubles"),
    (8, "Bad", "Fears, mental worries, injuries, troubles from women"),
    (9, "Good", "Fortune, luxuries, marital happiness"),
    (10, "Bad", "Virtuous acts, troubles, unpleasant events, disgrace"),
    (11, "Good", "Gains, happiness, prosperity, comforts"),
    (12, "Bad", "New friends, money, pleasures, gains"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_58)
def test_table_58_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.VENUS, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Venus"


def test_venus_is_the_most_generous_table():
    """Seven Good houses, and the only table opening with five in a row."""
    from hora.core.const import Graha
    from hora.transits.gochara import (
        STANDARD_RESULTS,
        VENUS_IS_THE_MOST_GENEROUS_TABLE,
        good_houses,
    )

    assert good_houses(Graha.VENUS) == (1, 2, 3, 4, 5, 9, 11)
    assert len(good_houses(Graha.VENUS)) == 7
    assert all(len(good_houses(other)) < 7 for other in STANDARD_RESULTS
               if other != int(Graha.VENUS))

    # the opening run, and nobody else has one that long
    def leading_run(graha):
        run = 0
        for row in STANDARD_RESULTS[graha]:
            if row["snapshot"] != "Good":
                break
            run += 1
        return run

    assert leading_run(int(Graha.VENUS)) == 5
    assert all(leading_run(other) <= 1 for other in STANDARD_RESULTS
               if other != int(Graha.VENUS))
    assert "five Good houses in a row" in VENUS_IS_THE_MOST_GENEROUS_TABLE


def test_venuss_twelfth_keeps_the_verdict_and_contradicts_it():
    """The 12th is Bad in all six tables. Venus's is the only one whose
    typical results contain no harm at all -- "New friends, money, pleasures,
    gains".
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        MIXED_ROWS,
        STANDARD_RESULTS,
        THE_TWELFTH_IS_BAD_EVERYWHERE_AND_READS_WELL_HERE,
        common_ground,
        transit_result,
    )

    assert 12 in common_ground()["always_bad"]
    for rows in STANDARD_RESULTS.values():
        assert rows[11]["snapshot"] == "Bad"

    got = transit_result(Graha.VENUS, 12)
    assert got["snapshot"] == "Bad"
    assert got["results"] == "New friends, money, pleasures, gains"
    assert ("Venus", 12) in [(row["graha"], row["house"]) for row in MIXED_ROWS]
    assert "no harm at all" in THE_TWELFTH_IS_BAD_EVERYWHERE_AND_READS_WELL_HERE


def test_venus_is_good_in_the_fourth_and_wishes_the_enemies_well():
    """"Prosperity, success of enemies, comforts" under a Good snapshot -- the
    only Good row in six tables that carries a harm.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import MIXED_ROWS, transit_result

    got = transit_result(Graha.VENUS, 4)
    assert got["snapshot"] == "Good"
    assert "success of enemies" in str(got["results"])

    good_and_mixed = [row for row in MIXED_ROWS if row["snapshot"] == "Good"]
    assert good_and_mixed == [
        {"graha": "Venus", "house": 4, "snapshot": "Good",
         "against_it": "success of enemies"}]


# ---------------------------------------------------------------------------
# Table 59 — Saturn's transit, and the nodes
# ---------------------------------------------------------------------------

#: Table 59 exactly as printed, House / Snapshot / Typical results.
PRINTED_TABLE_59 = (
    (1, "Bad", "Fear of incarceration, worries, foreign trips"),
    (2, "Bad", "Physical weakness, discomfort, wealth, unhappiness"),
    (3, "Good", "Wealth, health, happiness, all-round success"),
    (4, "Bad", "Stomach problems, wickedness, separation from family"),
    (5, "Bad", "Separation from children, uneasiness, quarrels"),
    (6, "Good", "Freedom from disease and enemies, success"),
    (7, "Bad", "Wandering, quarrels with spouse, trouble from authorities"),
    (8, "Bad", "Suffering, loss of status and balance, imprisonment"),
    (9, "Bad", "Diseases, suffering, loss of status"),
    (10, "Bad", "Loss of money, bad name, changes in career, laziness"),
    (11, "Good", "Wealth, success, gains"),
    (12, "Bad", "Grief, misery, losses, ill-health, frustration"),
)


@pytest.mark.parametrize(("house", "snapshot", "results"), PRINTED_TABLE_59)
def test_table_59_row_by_row(house, snapshot, results):
    from hora.core.const import Graha
    from hora.transits.gochara import transit_result

    got = transit_result(Graha.SATURN, house)
    assert got["house"] == house
    assert got["snapshot"] == snapshot
    assert got["results"] == results
    assert got["graha_name"] == "Saturn"
    assert got["from_graha"] is None             # Saturn has its own table


def test_mars_and_saturn_have_identical_verdict_columns():
    """The only pair in the section to agree on all twelve houses -- and their
    typical results differ in every one of them.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        MARS_AND_SATURN_HAVE_THE_SAME_VERDICTS,
        agreement,
        good_houses,
        transit_result,
    )

    got = agreement(Graha.MARS, Graha.SATURN)
    assert got["differ"] == ()
    assert len(got["agree"]) == 12
    assert good_houses(Graha.MARS) == good_houses(Graha.SATURN) == (3, 6, 11)

    for house in range(1, 13):
        assert (transit_result(Graha.MARS, house)["results"]
                != transit_result(Graha.SATURN, house)["results"])
    assert "no other pair" in MARS_AND_SATURN_HAVE_THE_SAME_VERDICTS.lower()


def test_the_nodes_read_through_saturn_and_mars():
    """"Rahu's behavior is similar to that of Saturn's and Ketu's behavior to
    Mars's."  Marked as an analogy, not passed off as the node's own row.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        NODES_FOLLOW,
        RAHU_AND_KETU_HAVE_NO_TABLE_OF_THEIR_OWN,
        SIMILAR_IS_NOT_IDENTICAL,
        STANDARD_RESULTS,
        transit_result,
    )

    assert NODES_FOLLOW == {int(Graha.RAHU): int(Graha.SATURN),
                            int(Graha.KETU): int(Graha.MARS)}
    assert int(Graha.RAHU) not in STANDARD_RESULTS
    assert int(Graha.KETU) not in STANDARD_RESULTS

    for node, model in ((Graha.RAHU, Graha.SATURN), (Graha.KETU, Graha.MARS)):
        for house in range(1, 13):
            got = transit_result(node, house)
            theirs = transit_result(model, house)
            assert got["graha_name"] == str(Graha(node).name).title()
            assert got["snapshot"] == theirs["snapshot"]
            assert got["results"] == theirs["results"]
            # and it says whose words those are
            assert got["from_graha"] == int(model)
            assert got["analogy"] == "similar"

    assert "similar" in RAHU_AND_KETU_HAVE_NO_TABLE_OF_THEIR_OWN
    assert "no list of differences" in SIMILAR_IS_NOT_IDENTICAL


def test_the_four_malefics_end_up_with_one_good_set():
    """Mars and Saturn share a verdict column, and the analogy hands that
    column to Ketu and Rahu -- so all four are Good in the 3rd, 6th and 11th.
    The book never puts the two facts together.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        THE_FOUR_MALEFICS_SHARE_ONE_GOOD_SET,
        good_houses,
    )

    for graha in (Graha.MARS, Graha.SATURN, Graha.RAHU, Graha.KETU):
        assert good_houses(graha) == (3, 6, 11)

    # and no benefic shares it
    for graha in (Graha.SUN, Graha.MOON, Graha.MERCURY, Graha.JUPITER,
                  Graha.VENUS):
        assert good_houses(graha) != (3, 6, 11)
    assert "3rd, 6th and 11th" in THE_FOUR_MALEFICS_SHARE_ONE_GOOD_SET


def test_25_2_is_finished():
    """All seven promised tables are in, and every graha now resolves -- seven
    by their own table and two by §25.2's analogy.
    """
    from hora.transits.gochara import (
        NODES_FOLLOW,
        STANDARD_RESULT_TABLES,
        STANDARD_RESULTS,
        transit_result,
    )

    assert all(row["built"] for row in STANDARD_RESULT_TABLES.values())
    assert [STANDARD_RESULT_TABLES[n]["for"] for n in range(53, 60)] == [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    assert len(STANDARD_RESULTS) == 7
    assert len(STANDARD_RESULTS) + len(NODES_FOLLOW) == 9

    for graha in range(9):
        assert transit_result(graha, 11)["snapshot"] == "Good"
        assert transit_result(graha, 12)["snapshot"] == "Bad"


# ---------------------------------------------------------------------------
# Example 103 — Chart 52, a transit chart against a Gemini janma rasi
# ---------------------------------------------------------------------------

def test_chart_52_is_a_transit_chart_with_no_birth_data():
    """The register's first. A date and a diagram; nobody's nativity, so no
    time, no place and no degrees.
    """
    from hora.charts.book import chart, has_longitudes, signs

    record = chart(52)
    assert record["kind"] == "transit"
    assert "birth_data" not in record and "place" not in record
    assert not has_longitudes(52)
    assert signs(52)["Merc"] == R["Ge"]


def test_chart_52s_grahas_reproduce_for_any_time_that_day():
    """All nine, at every hour of 7 June 1999 -- the Moon included, which
    stays in Aquarius the whole day. That is what lets a chart with no time
    still be checked.
    """
    from hora.charts.book import signs
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    drawn = signs(52)

    for hour in (0, 6, 12, 18, 23):
        computed = compute_chart(
            from_local(year=1999, month=6, day=7, hour=hour, minute=0,
                       second=0.0, utc_offset_hours=5.5),
            Place(name="assumed", latitude=17.0, longitude=78.0),
            Settings(node_type=NodeType.MEAN))
        for name, graha in named.items():
            got = int(computed.positions[int(graha)].longitude // 30)
            assert got == drawn[name], f"{name} at {hour}:00"


def test_the_drawn_ascendant_and_special_lagnas_pin_the_unstated_time():
    """Asc, AL, HL and GL need a moment and a place. At an assumed 17 N 78 E
    all four land together only in a narrow early-afternoon window -- so the
    diagram is internally consistent, and our HL and GL reach it, which OI-103
    gave reason to doubt.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import signs
    from hora.charts.chart import Place, compute_chart
    from hora.charts.special_lagna import all_special_lagnas
    from hora.charts.upagraha import birth_period
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    drawn = signs(52)
    settings = Settings(node_type=NodeType.MEAN)
    place = Place(name="assumed", latitude=17.0, longitude=78.0)

    def matches(hour, minute):
        instant = from_local(year=1999, month=6, day=7, hour=hour,
                             minute=minute, second=0.0, utc_offset_hours=5.5)
        computed = compute_chart(instant, place, settings)
        if computed.lagna_rasi != drawn["Asc"]:
            return False
        period = birth_period(computed.instant.jd_ut, place.latitude,
                              place.longitude, place.altitude, settings)
        lagnas = all_special_lagnas(
            sunrise_jd=period.sunrise_jd, jd_ut=computed.instant.jd_ut,
            lagna_longitude=computed.lagna_longitude,
            moon_longitude=computed.positions[Graha.MOON].longitude,
            settings=settings)
        by_name = {v.abbreviation: int(v.longitude // 30)
                   for v in lagnas.values()}
        occupied = {int(g): int(computed.positions[int(g)].longitude // 30)
                    for g in list(Graha)[:9]}
        arudha = arudha_pada(1, computed.lagna_rasi, occupied).sign
        return (by_name["HL"] == drawn["HL"] and by_name["GL"] == drawn["GL"]
                and arudha == drawn["AL"])

    assert matches(14, 25)                       # inside the window
    assert not matches(12, 0)                    # Ascendant not yet Virgo
    assert not matches(16, 0)                    # long past it


def test_example_103s_three_readings_come_out_of_the_tables():
    """"Janma rasi is Ge."  Jupiter and Saturn in the 11th, the Sun in the
    12th, Mercury in the 1st -- each verdict is the printed table's.
    """
    from hora.charts.book import signs
    from hora.core.const import Graha
    from hora.transits.gochara import (
        EXAMPLE_103_READINGS,
        house_from_janma,
        transit_result,
    )

    janma = R["Ge"] * 30 + 15.0                  # Moon in Gemini
    drawn = signs(52)

    def house_of(name):
        return house_from_janma(janma, drawn[name] * 30 + 15.0)["house"]

    assert house_of("Jup") == house_of("Sat") == 11
    assert house_of("Sun") == 12
    assert house_of("Merc") == 1

    assert transit_result(Graha.JUPITER, 11)["snapshot"] == "Good"
    assert transit_result(Graha.SATURN, 11)["snapshot"] == "Good"
    assert "gains" in str(transit_result(Graha.SATURN, 11)["results"]).lower()

    sun = transit_result(Graha.SUN, 12)
    assert sun["snapshot"] == "Bad"
    assert sun["results"] == "Expenditure, losses"

    mercury = transit_result(Graha.MERCURY, 1)
    assert mercury["snapshot"] == "Bad"
    assert mercury["results"] == "Quarrels, imprisonment, losses, poor advice"

    assert [row["house"] for row in EXAMPLE_103_READINGS] == [11, 12, 1]


def test_the_subject_now_comes_from_three_things_not_one():
    """§25.2 illustrated the subject with lordship alone. Example 103 uses
    houses ruled, houses occupied and karakatva -- and karakatva is not natal
    at all, being the same in every chart.
    """
    from hora.transits.gochara import (
        EXAMPLE_103_KARAKATVAS,
        THE_SUBJECT_COMES_FROM_NATAL_LORDSHIP,
        THE_SUBJECT_COMES_FROM_THREE_THINGS,
    )

    assert "ruled and occupied" in THE_SUBJECT_COMES_FROM_THREE_THINGS
    assert "signifies" in THE_SUBJECT_COMES_FROM_THREE_THINGS

    # §25.2's own illustration used lordship and nothing else
    assert all("natal_lordship" in row
               for row in THE_SUBJECT_COMES_FROM_NATAL_LORDSHIP)

    assert [row["graha"] for row in EXAMPLE_103_KARAKATVAS] == [
        "Jupiter", "Saturn", "Sun"]
    for row in EXAMPLE_103_KARAKATVAS:
        assert row["signifies"]


def test_dignity_in_the_transited_sign_softens_the_verdict():
    """Mercury in janma rasi draws Table 56's harshest row, and the example
    sets it aside because Mercury is in its own sign. The first rule in the
    chapter that changes the substance rather than the subject.
    """
    from hora.core.const import RASI_LORD, Graha
    from hora.transits.gochara import (
        DIGNITY_IN_THE_TRANSITED_SIGN_SOFTENS_THE_RESULT,
        transit_result,
    )

    row = transit_result(Graha.MERCURY, 1)
    assert str(row["results"]).lower() in (
        DIGNITY_IN_THE_TRANSITED_SIGN_SOFTENS_THE_RESULT.lower())

    # and the dignity the example invokes is real: Gemini is Mercury's own
    assert int(RASI_LORD[R["Ge"]]) == int(Graha.MERCURY)
    assert "own house" in DIGNITY_IN_THE_TRANSITED_SIGN_SOFTENS_THE_RESULT
    assert "intellectual debates" in (
        DIGNITY_IN_THE_TRANSITED_SIGN_SOFTENS_THE_RESULT)


def test_25_2_closes_by_pointing_past_the_moon():
    """"There are natal references other than Moon, though Moon is the most
    important."  §25.1 promised several reference points; this is the first
    acknowledgement that Moon was only the first.
    """
    from hora.transits.gochara import (
        ADAPT_THEM_INTELLIGENTLY,
        CORRELATION_IS_THE_METHOD,
        THERE_ARE_OTHER_NATAL_REFERENCES,
    )

    assert "several reference points" in CORRELATION_IS_THE_METHOD
    assert "other than Moon" in THERE_ARE_OTHER_NATAL_REFERENCES
    assert "most important natal reference" in THERE_ARE_OTHER_NATAL_REFERENCES
    assert "adapt them intelligently" in ADAPT_THEM_INTELLIGENTLY


# ---------------------------------------------------------------------------
# §25.3 Other natal references
# ---------------------------------------------------------------------------

def test_25_3_names_the_rest_of_25_1s_reference_points():
    """§25.1 promised "several"; §25.2 gave one. Six more, and only sahams
    cannot be produced today.
    """
    from hora.transits.gochara import (
        ASHTAKAVARGA_JUDGES_A_TRANSIT_FROM_LAGNA,
        OTHER_REFERENCES,
    )

    named = [row["reference"] for row in OTHER_REFERENCES]
    assert named == ["lagna", "paaka lagna", "natal houses", "natal planets",
                     "arudha padas", "sahams"]
    uncomputable = [row["reference"] for row in OTHER_REFERENCES
                    if not row["computable"]]
    assert uncomputable == ["sahams"]

    assert "hub of vitality" in ASHTAKAVARGA_JUDGES_A_TRANSIT_FROM_LAGNA
    assert "from lagna" in ASHTAKAVARGA_JUDGES_A_TRANSIT_FROM_LAGNA


def test_paaka_lagnas_meaning_agrees_with_chapter_7():
    """§25.3 says paaka lagna "explicitly stands for the physical self".
    §7.3.5 said the same thing eighteen chapters earlier.
    """
    from hora.core.const import PAAKA_LAGNA_DEFINITION, PAAKA_LAGNA_SHOWS
    from hora.transits.gochara import OTHER_REFERENCES

    paaka = next(row for row in OTHER_REFERENCES
                 if row["reference"] == "paaka lagna")
    assert paaka["stands_for"] == "the physical self"
    assert "physical self" in PAAKA_LAGNA_SHOWS
    assert "lagna lord" in PAAKA_LAGNA_DEFINITION


def test_a_transiting_graha_reaches_the_rasi_it_occupies_and_those_it_aspects():
    """§25.3's master rule joins the two. Jupiter in Virgo reaches four rasis:
    Virgo itself and its 5th, 7th and 9th.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import THE_MASTER_RULE, influenced_rasis

    got = influenced_rasis(Graha.JUPITER, R["Vi"])
    assert got["occupies"] == R["Vi"]
    assert [A[r] for r in got["aspects"]] == ["Ta", "Cp", "Pi"]
    assert [A[r] for r in got["reaches"]] == ["Vi", "Ta", "Cp", "Pi"]

    assert "occupying or aspecting" in THE_MASTER_RULE
    assert "houses and planets stationed in that rasi" in THE_MASTER_RULE


@pytest.mark.parametrize(("graha", "transits", "lagna"), [
    ("JUPITER", "Ta", "Sc"),
    ("SATURN", "Ar", "Li"),
])
def test_25_3s_two_occupation_examples(graha, transits, lagna):
    """"Jupiter transiting in the Ta may give marriage to someone born in Sc
    lagna, because Ta is the 7th house from Sc."  And Saturn in Ar for Li.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import influences

    rows = influences(getattr(Graha, graha), R[transits], R[lagna])
    occupied = next(row for row in rows if row["how"] == "occupies")
    assert occupied["rasi"] == R[transits]
    assert occupied["natal_house"] == 7


def test_25_3s_two_aspect_examples():
    """"Jupiter aspects Ta, the 7th house from Sc, when he is in Vi."  And
    with natal Venus in Pi, the same transit reaches Venus too.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import EXAMPLE_TRANSITS, influences

    plain = influences(Graha.JUPITER, R["Vi"], R["Sc"])
    seventh = next(row for row in plain if row["natal_house"] == 7)
    assert seventh["rasi"] == R["Ta"]
    assert seventh["how"] == "aspects"

    with_venus = influences(Graha.JUPITER, R["Vi"], R["Sc"],
                            {int(Graha.VENUS): R["Pi"]})
    reached = {row["rasi_name"]: row for row in with_venus}
    assert reached["Taurus"]["natal_house"] == 7
    assert reached["Pisces"]["natal_graha_names"] == ("Venus",)
    assert reached["Pisces"]["how"] == "aspects"
    # both, from one transit -- which is why the example says it may give marriage
    assert reached["Taurus"]["how"] == "aspects"

    assert [row["how"] for row in EXAMPLE_TRANSITS] == [
        "occupies", "occupies", "aspects", "aspects"]


def test_the_master_rule_needs_no_natal_planets_to_report_houses():
    """`natal_signs` is optional: without it the houses come back and the
    planets are empty, rather than the call refusing.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import influences

    rows = influences(Graha.SATURN, R["Ar"], R["Li"])
    assert all(row["natal_grahas"] == () for row in rows)
    assert {row["natal_house"] for row in rows} == {7, 9, 1, 4}


def test_a_malefic_over_the_three_self_points_harms_three_things():
    """Mind at janma rasi, vitality at natal lagna, body at paaka lagna."""
    from hora.transits.gochara import (
        MALEFIC_OVER_THE_THREE_SELF_POINTS,
        THE_THREE_SELF_POINTS_DIVIDE_MIND_VITALITY_AND_BODY,
    )

    rows = MALEFIC_OVER_THE_THREE_SELF_POINTS
    assert [row["reference"] for row in rows] == [
        "janma rasi", "natal lagna", "paaka lagna"]
    assert rows[0]["gives"] == "mental worries"
    assert "vitality" in rows[1]["gives"]
    assert rows[2]["gives"] == "bodily complaints"
    assert len({row["gives"] for row in rows}) == 3

    assert "mind" in THE_THREE_SELF_POINTS_DIVIDE_MIND_VITALITY_AND_BODY
    assert "§7.3.5" in THE_THREE_SELF_POINTS_DIVIDE_MIND_VITALITY_AND_BODY


def test_arudha_pada_transits_name_two():
    """"Saturn's transit in A10 can be bad for career, Jupiter's transit in A9
    is good for fortune."
    """
    from hora.transits.gochara import (
        ARUDHA_PADA_TRANSIT_EXAMPLES,
        ARUDHA_PADA_TRANSITS,
    )

    assert [(row["graha"], row["pada"], row["house"])
            for row in ARUDHA_PADA_TRANSIT_EXAMPLES] == [
        ("Saturn", "A10", 10), ("Jupiter", "A9", 9)]
    assert "occupying or aspecting arudha padas" in ARUDHA_PADA_TRANSITS


def test_the_saham_rules_cannot_be_built_and_say_so():
    """Sahams are a Tajaka topic the book defers, and "close to" is given no
    orb. Two reasons, both recorded. OI-116.
    """
    from hora.transits.gochara import (
        OTHER_REFERENCES,
        SAHAM_TRANSIT_EXAMPLES,
        SAHAM_TRANSITS_NEED_TAJAKA_AND_AN_ORB,
        SAHAMS_ARE_USEFUL,
    )

    assert [row["saham"] for row in SAHAM_TRANSIT_EXAMPLES] == ["vivaha", "kali"]
    assert "close to" in SAHAMS_ARE_USEFUL
    assert "no orb" in SAHAM_TRANSITS_NEED_TAJAKA_AND_AN_ORB
    assert "Tajaka" in SAHAM_TRANSITS_NEED_TAJAKA_AND_AN_ORB

    sahams = next(row for row in OTHER_REFERENCES
                  if row["reference"] == "sahams")
    assert sahams["computable"] is False


def test_natal_lordship_qualifies_the_master_rule():
    """"The exact nature of the influence... depends on its inherent nature
    and the matters it stands for in the natal chart" -- §25.2's caveat again,
    with two worked cases.
    """
    from hora.transits.gochara import (
        NATAL_LORDSHIP_EXAMPLES,
        THE_NATURE_OF_THE_INFLUENCE,
        THE_TABLES_ARE_REFERENCE_ONLY,
    )

    assert [row["natal_lord_of"] for row in NATAL_LORDSHIP_EXAMPLES] == [5, 8]
    assert "children" in str(NATAL_LORDSHIP_EXAMPLES[0]["expect"])
    assert "marital life" in str(NATAL_LORDSHIP_EXAMPLES[1]["expect"])

    for text in (THE_NATURE_OF_THE_INFLUENCE, THE_TABLES_ARE_REFERENCE_ONLY):
        assert "natal chart" in text


# ---------------------------------------------------------------------------
# Example 104 — Chart 53, a nativity and its wedding-day transit
# ---------------------------------------------------------------------------

def _chart_53_natal_signs():
    from hora.charts.book import longitudes
    from hora.core.const import Graha

    printed = longitudes(53)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    return {int(g): int(printed[n] // 30) for n, g in named.items()}


def test_chart_53_holds_two_charts_under_one_number():
    """The nativity and the transit chart for her wedding day."""
    from hora.charts.book import chart

    record = chart(53)
    assert record["transit"]["for"] == "the wedding"
    assert record["transit"]["date"].startswith("January 24, 1999")
    assert record["transit"]["drawn"]["Jup"] == "Pi"
    assert record["drawn"]["Jup"] == "Cp"                # the natal one
    assert record["events"]["the lady married"] == "January 24, 1999"


def test_chart_53s_nativity_recomputes_within_an_arcminute():
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(53)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 53", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(53)
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 1.0


def test_the_wedding_transit_chart_pins_its_own_unstated_time():
    """A date and no time again. The Moon reaches Aries and the Ascendant
    Aquarius together only in a narrow morning window, and the AL comes out
    Gemini there, as drawn.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.charts.colord import stronger
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(53)
    drawn = record["transit"]["drawn"]
    place = Place(name="wedding", **record["place"])
    settings = Settings(node_type=NodeType.MEAN)

    def at(hour, minute):
        computed = compute_chart(
            from_local(year=1999, month=1, day=24, hour=hour, minute=minute,
                       second=0.0, utc_offset_hours=5.5), place, settings)
        longs = {int(g): computed.positions[int(g)].longitude
                 for g in list(Graha)[:9]}
        signs = {g: int(v // 30) for g, v in longs.items()}
        lords = {rasi: stronger(rasi, longs).winner for rasi in (7, 10)}
        return computed, signs, arudha_pada(1, computed.lagna_rasi, signs,
                                            lords).sign

    computed, signs, arudha = at(8, 45)
    assert A[computed.lagna_rasi] == drawn["Asc"] == "Aq"
    assert A[signs[int(Graha.MOON)]] == drawn["Moon"] == "Ar"
    assert A[arudha] == drawn["AL"] == "Ge"

    # outside the window one of the two moving points is wrong
    early, early_signs, _ = at(6, 0)
    assert (A[early.lagna_rasi] != "Aq"
            or A[early_signs[int(Graha.MOON)]] != "Ar")


def test_the_transit_grahas_match_the_drawn_chart_all_day():
    """The seven slow bodies and the nodes need no time; only the Moon and the
    Ascendant do.
    """
    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(53)
    drawn = record["transit"]["drawn"]
    named = {"Sun": Graha.SUN, "Mars": Graha.MARS, "Merc": Graha.MERCURY,
             "Jup": Graha.JUPITER, "Ven": Graha.VENUS, "Sat": Graha.SATURN,
             "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    for hour in (0, 8, 16, 23):
        computed = compute_chart(
            from_local(year=1999, month=1, day=24, hour=hour, minute=0,
                       second=0.0, utc_offset_hours=5.5),
            Place(name="wedding", **record["place"]),
            Settings(node_type=NodeType.MEAN))
        for name, graha in named.items():
            got = A[int(computed.positions[int(graha)].longitude // 30)]
            assert got == drawn[name], f"{name} at {hour}:00"


def test_example_104s_four_reference_points():
    """"The 7th house in the natal chart is in Vi. Mercury is the 7th lord and
    he is in Cn... Venus... is in Le... Vivaha saham is at 1 deg in Cp."
    """
    from hora.charts.book import chart, longitudes
    from hora.core.const import RASI_LORD, Graha
    from hora.transits.gochara import (
        EXAMPLE_104_REFERENCE_POINTS,
        INFLUENCE_THESE_AND_THEY_CAN_GIVE_MARRIAGE,
    )

    lagna = int(longitudes(53)["Asc"] // 30)
    natal = _chart_53_natal_signs()
    assert A[lagna] == "Pi"

    seventh = (lagna + 6) % 12
    assert A[seventh] == "Vi"
    assert int(RASI_LORD[seventh]) == int(Graha.MERCURY)
    assert A[natal[int(Graha.MERCURY)]] == "Cn"
    assert A[natal[int(Graha.VENUS)]] == "Le"
    assert chart(53)["sahams"]["vivaha"] == "1 Cp"

    assert [row["at"] for row in EXAMPLE_104_REFERENCE_POINTS] == [
        "Virgo", "Cancer", "Leo", "1 Cp"]
    assert "give marriage" in INFLUENCE_THESE_AND_THEY_CAN_GIVE_MARRIAGE


def test_jupiter_is_watched_for_two_reasons():
    """"Jupiter is a natural benefic and also lagna lord here." """
    from hora.charts.book import longitudes
    from hora.core.const import NATURAL_BENEFIC, RASI_LORD, Graha
    from hora.transits.gochara import JUPITER_TIMES_AUSPICIOUS_EVENTS

    lagna = int(longitudes(53)["Asc"] // 30)
    assert int(RASI_LORD[lagna]) == int(Graha.JUPITER)
    assert int(Graha.JUPITER) in set(NATURAL_BENEFIC)
    assert "timing auspicious events" in JUPITER_TIMES_AUSPICIOUS_EVENTS


def test_example_104s_transit_hits_are_the_master_rule():
    """Each of the four is a transiting graha reaching a rasi that holds a
    natal reference point -- which is exactly what `influences` computes.
    """
    from hora.charts.book import longitudes
    from hora.core.const import Graha
    from hora.transits.gochara import EXAMPLE_104_HITS, influences

    lagna = int(longitudes(53)["Asc"] // 30)
    natal = _chart_53_natal_signs()

    def reaches(graha, transit_sign):
        return {row["rasi_name"]: row
                for row in influences(graha, R[transit_sign], lagna, natal)}

    jupiter = reaches(Graha.JUPITER, "Pi")
    assert jupiter["Virgo"]["natal_house"] == 7
    assert jupiter["Virgo"]["how"] == "aspects"
    assert "Mercury" in jupiter["Cancer"]["natal_graha_names"]
    assert jupiter["Cancer"]["how"] == "aspects"

    mercury = reaches(Graha.MERCURY, "Cp")
    assert "Mercury" in mercury["Cancer"]["natal_graha_names"]

    venus = reaches(Graha.VENUS, "Aq")
    assert "Venus" in venus["Leo"]["natal_graha_names"]

    assert len(EXAMPLE_104_HITS) == 4
    assert all(row["how"] == "aspects" for row in EXAMPLE_104_HITS)


def test_two_of_the_four_hits_are_a_graha_on_its_own_natal_place():
    """Mercury from Capricorn onto Cancer, Venus from Aquarius onto Leo --
    both the seventh aspect, which every graha has.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import (
        A_GRAHA_CAN_ASPECT_ITS_OWN_NATAL_POSITION,
        influenced_rasis,
    )

    natal = _chart_53_natal_signs()
    for graha, transit_sign in ((Graha.MERCURY, "Cp"), (Graha.VENUS, "Aq")):
        own = natal[int(graha)]
        assert own in influenced_rasis(graha, R[transit_sign])["aspects"]
        assert (R[transit_sign] + 6) % 12 == own          # the 7th aspect

    assert "seventh aspect" in A_GRAHA_CAN_ASPECT_ITS_OWN_NATAL_POSITION


def test_the_saham_claim_is_consistent_but_cannot_be_checked():
    """The book prints vivaha saham at 1 Cp and says transit Mercury stood
    "about 1 deg away". Our Mercury is at about 2.5 Cp, so the gap is 1.4 to
    1.5 deg -- consistent, and not a confirmation, because the saham itself
    is a Tajaka quantity we do not compute.
    """
    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.gochara import (
        OTHER_REFERENCES,
        THE_SAHAM_CLAIM_IS_CONSISTENT_BUT_UNCHECKED,
    )

    record = chart(53)
    saham = R["Cp"] * 30 + 1.0
    for hour, minute in ((8, 0), (9, 30)):
        computed = compute_chart(
            from_local(year=1999, month=1, day=24, hour=hour, minute=minute,
                       second=0.0, utc_offset_hours=5.5),
            Place(name="wedding", **record["place"]),
            Settings(node_type=NodeType.MEAN))
        mercury = computed.positions[int(Graha.MERCURY)].longitude
        assert 1.3 < abs(mercury - saham) < 1.6

    # and the reference itself is still uncomputable
    sahams = next(row for row in OTHER_REFERENCES
                  if row["reference"] == "sahams")
    assert sahams["computable"] is False
    assert "not computed" in THE_SAHAM_CLAIM_IS_CONSISTENT_BUT_UNCHECKED
