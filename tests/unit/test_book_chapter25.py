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


def test_the_seven_promised_tables_are_tracked_and_none_is_built_yet():
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
    assert registered == {"Sun"}                 # Table 53 only, so far


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

    for graha in (Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
                  Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU):
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
        int(Graha.MARS): R["Pi"] * 30 + 1.0,     # the 8th
    })
    assert len(got) == 2

    sun = next(row for row in got if row["graha"] == int(Graha.SUN))
    assert (sun["house"], sun["snapshot"]) == (3, "Good")
    assert sun["results"] == "Wealth, good health, victory"
    assert sun["undecided"] is None

    mars = next(row for row in got if row["graha"] == int(Graha.MARS))
    assert mars["house"] == 8                    # the house is known
    assert mars["snapshot"] is None              # the verdict is not
    assert "have not been supplied" in mars["undecided"]


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
