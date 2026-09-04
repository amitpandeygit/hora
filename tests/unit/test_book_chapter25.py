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

    built = {number for number, row in STANDARD_RESULT_TABLES.items()
             if row["built"]}
    assert built == set(), f"registered as built but untested: {built}"
    for row in STANDARD_RESULT_TABLES.values():
        assert (row["for"] is None) == (not row["built"])


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
