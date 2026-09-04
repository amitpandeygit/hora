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
                          "Venus"}                      # 53 to 58


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


def test_an_unsupplied_table_raises_and_names_the_graha():
    """Tables 54 to 59 have not arrived. Asking for one says so rather than
    returning a neutral verdict.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import GocharaError, good_houses, transit_result

    for graha in (Graha.SATURN, Graha.RAHU, Graha.KETU):
        with pytest.raises(GocharaError, match="have not been supplied"):
            transit_result(graha, 1)
        with pytest.raises(GocharaError, match="have not been supplied"):
            good_houses(graha)


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
    assert saturn["house"] == 8                  # the house is known
    assert saturn["snapshot"] is None            # the verdict is not
    assert "have not been supplied" in saturn["undecided"]


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
    with pytest.raises(GocharaError, match="have not been supplied"):
        agreement(Graha.SUN, Graha.SATURN)


def test_read_transits_now_verdicts_two_grahas():
    from hora.core.const import Graha
    from hora.transits.gochara import read_transits

    moon = R["Le"] * 30 + 15.0                   # janma rasi Leo
    got = {row["graha"]: row for row in read_transits(moon, {
        int(Graha.SUN): R["Li"] * 30 + 1.0,      # the 3rd
        int(Graha.MOON): R["Le"] * 30 + 20.0,    # the 1st
        int(Graha.SATURN): R["Pi"] * 30 + 1.0,   # the 8th, still unsupplied
    })}

    assert got[int(Graha.SUN)]["snapshot"] == "Good"
    assert got[int(Graha.MOON)]["house"] == 1
    assert got[int(Graha.MOON)]["snapshot"] == "Good"
    assert got[int(Graha.MOON)]["results"] == "Comfort, good spirits"
    assert got[int(Graha.SATURN)]["undecided"] is not None


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
        ("Mars", 10), ("Venus", 4), ("Venus", 10), ("Venus", 12)]
    assert sum(1 for row in MIXED_ROWS if row["graha"] == "Venus") == 3

    named = {"Mars": Graha.MARS, "Venus": Graha.VENUS}
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
    """With six tables in, only the 11th is Good in all of them and only the
    12th Bad in all. `tables` says how many were compared, so "always" cannot
    be read as more than it is.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import common_ground

    got = common_ground()
    assert got["tables"] == 6
    assert got["grahas"] == (int(Graha.SUN), int(Graha.MOON), int(Graha.MARS),
                             int(Graha.MERCURY), int(Graha.JUPITER),
                             int(Graha.VENUS))
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
    """Six tables in, the 11th is Good in every one and the 12th Bad in every
    one, and they are the only two houses left undisputed.
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
             "Venus": Graha.VENUS}
    first = {int(named[name]) for name in TABLE_GROUPS[0]}
    second = {int(named[name]) for name in TABLE_GROUPS[1]}
    assert first | second == set(STANDARD_RESULTS)
    assert not first & second

    def profile(graha):
        return sorted(len(agreement(graha, other)["agree"])
                      for other in first)

    assert profile(Graha.JUPITER) == profile(Graha.VENUS) == [5, 5, 5, 6]
    assert len(agreement(Graha.JUPITER, Graha.VENUS)["agree"]) == 8

    cross, within = [], []
    for a, b in itertools.combinations(sorted(STANDARD_RESULTS), 2):
        score = len(agreement(a, b)["agree"])
        (cross if (a in first) != (b in first) else within).append(score)
    assert max(cross) == 6
    assert min(within) == 6 and max(within) == 11

    assert "the same four numbers" in THE_TWO_BENEFICS_FORM_A_PAIR


def test_only_the_11th_and_12th_survive_six_tables():
    """The section's agreements narrowed table by table -- three Good and six
    Bad after Mars, two and three after Mercury, one and one after Jupiter --
    and Venus leaves them where Jupiter did.
    """
    from hora.transits.gochara import STANDARD_RESULTS, common_ground

    got = common_ground()
    assert got["tables"] == len(STANDARD_RESULTS) == 6
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
