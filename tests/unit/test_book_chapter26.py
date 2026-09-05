"""Chapter 26 — transits: miscellaneous topics.

§26.1 sets out two threads, rasi principles chapter 25 left and nakshatra
interactions it never touched, and names not one of them. The last test here
is the coverage line, and it stays failing-by-omission until the chapter's own
sections arrive: nothing is built ahead of a page.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_ABBR

A = list(RASI_ABBR)
R = {abbr: index for index, abbr in enumerate(RASI_ABBR)}


def test_26_1_names_chapter_25_by_its_own_title():
    """"In the chapter "Transits and Natal References", we concentrated on
    correlating the natal chart and the transit chart using the rasis."
    """
    from hora.core.const import CHAPTER_26_LOOKS_BACK_AT_25

    assert "Transits and Natal References" in CHAPTER_26_LOOKS_BACK_AT_25
    assert "using the rasis" in CHAPTER_26_LOOKS_BACK_AT_25
    assert "haven't yet covered" in CHAPTER_26_LOOKS_BACK_AT_25


def test_26_1_sets_out_two_threads_and_names_no_principle():
    from hora.core.const import (
        CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER,
        CHAPTER_26_THREADS,
        PART_3_IS_KNOWINGLY_PARTIAL,
    )

    assert len(CHAPTER_26_THREADS) == 2
    assert [t["thread"] for t in CHAPTER_26_THREADS] == [
        "rasi transits", "nakshatra transits"]
    assert CHAPTER_26_THREADS[0]["scope"] == "a couple of concepts"
    assert CHAPTER_26_THREADS[1]["scope"] == "a few principles"
    assert "names none of them" in CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER
    assert "Some of those techniques" in PART_3_IS_KNOWINGLY_PARTIAL


def test_nakshatras_are_put_level_with_rasis():
    from hora.core.const import NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS

    assert "as important as rasis" in NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS
    assert "natal and transit charts" in NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS


def test_chapter_25_correlated_by_rasi_throughout():
    """The claim §26.1 makes about chapter 25, checked against what chapter 25
    actually built rather than taken on trust.
    """
    from hora.core.const import CHAPTER_26_IS_THE_FIRST_TO_PAIR_NAKSHATRAS
    from hora.transits import gochara

    # every chapter 25 entry point takes or returns rasis, not nakshatras
    for name in ("janma_rasi", "house_from_janma", "houses_from_janma",
                 "transit_result", "read_transits", "influenced_rasis",
                 "influences", "transits_over", "divisional_interaction"):
        assert callable(getattr(gochara, name))
    # only §25.6 produces a nakshatra anywhere in chapter 25
    callables = {name for name in dir(gochara)
                 if "nakshatra" in name.lower()
                 and callable(getattr(gochara, name))}
    assert callables == {"timing_nakshatra", "companion_nakshatras"}

    # and it comes from a product, not from a graha's own nakshatra
    got = gochara.timing_nakshatra(430)
    assert got["nakshatra"] == "Purva Bhadrapada"
    assert got["product"] == 430
    assert "times a sodhya pinda" in (
        CHAPTER_26_IS_THE_FIRST_TO_PAIR_NAKSHATRAS)


def test_only_the_sections_supplied_have_modules():
    """The coverage line. §26.2 has arrived and has one; the nakshatra thread
    §26.1 promises has not, and nothing is built ahead of a page.
    """
    import importlib

    importlib.import_module("hora.transits.murthi")
    for module in ("hora.transits.nakshatra", "hora.transits.misc"):
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        raise AssertionError(f"{module} exists before its section arrived")


# --------------------------------------------------------------------------
# §26.2 — murthis, and Table 62
# --------------------------------------------------------------------------

def _ephemeris():
    """A longitude callable and the tools to read a julian day back."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_jd

    place = Place(name="New Delhi", latitude=28 + 36 / 60,
                  longitude=77 + 12 / 60)
    settings = Settings(node_type=NodeType.MEAN)

    def longitude_of(graha):
        def at(jd):
            chart = compute_chart(from_jd(jd), place, settings)
            return chart.positions[int(graha)].longitude
        return at

    return longitude_of


def test_table_62_partitions_the_twelve_houses():
    from hora.transits.murthi import MURTHI_OF_HOUSE, TABLE_62_MURTHIS

    assert len(TABLE_62_MURTHIS) == 4
    houses = [h for row in TABLE_62_MURTHIS for h in row["houses"]]
    assert sorted(houses) == list(range(1, 13))
    assert all(len(row["houses"]) == 3 for row in TABLE_62_MURTHIS)
    assert [row["murthi"] for row in TABLE_62_MURTHIS] == [
        "Swarna", "Rajata", "Taamra", "Loha"]
    assert [row["rank"] for row in TABLE_62_MURTHIS] == [1, 2, 3, 4]
    assert [row["favourable"] for row in TABLE_62_MURTHIS] == [
        True, True, False, False]
    assert len(MURTHI_OF_HOUSE) == 12


def test_the_iron_form_is_exactly_the_moksha_trikona():
    from hora.core.const import PURUSHARTHA_TRIKONAS
    from hora.transits.murthi import (
        LOHA_IS_THE_MOKSHA_TRIKONA,
        TABLE_62_MURTHIS,
    )

    loha = next(row for row in TABLE_62_MURTHIS if row["murthi"] == "Loha")
    assert set(loha["houses"]) == set(PURUSHARTHA_TRIKONAS["moksha"]["houses"])

    # and no other murthi is a purushartha trikona of any kind
    trikonas = {name: set(entry["houses"])
                for name, entry in PURUSHARTHA_TRIKONAS.items()}
    for row in TABLE_62_MURTHIS:
        if row["murthi"] == "Loha":
            continue
        assert set(row["houses"]) not in trikonas.values(), row["murthi"]
    assert "moksha trikona" in LOHA_IS_THE_MOKSHA_TRIKONA


def test_every_quadrant_but_the_lagna_is_unfavourable():
    from hora.transits.murthi import (
        EVERY_QUADRANT_BUT_THE_FIRST_IS_UNFAVOURABLE,
        murthi_of_house,
    )

    assert murthi_of_house(1)["murthi"] == "Swarna"
    assert murthi_of_house(4)["murthi"] == "Loha"
    assert murthi_of_house(7)["murthi"] == "Taamra"
    assert murthi_of_house(10)["murthi"] == "Taamra"
    assert all(not murthi_of_house(h)["favourable"] for h in (4, 7, 10))
    assert "only the lagna is favourable" in (
        EVERY_QUADRANT_BUT_THE_FIRST_IS_UNFAVOURABLE)


def test_mercurys_gemini_ingress_is_the_minute_the_book_prints():
    """"Mercury entered Gemini at 3:06 pm (IST) on May 26, 2000." Ours lands
    at 15:06:08, and the Moon is where the book says it is.
    """
    from hora.core.const import Graha
    from hora.core.timeutil import (
        format_dms,
        from_jd,
        from_local,
        jd_to_local_str,
    )
    from hora.transits.murthi import MERCURY_IN_GEMINI_2000, rasi_ingress

    longitude_of = _ephemeris()
    window = (from_local(2000, 5, 20, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
              from_local(2000, 6, 5, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)
    found = rasi_ingress(longitude_of(Graha.MERCURY), R["Ge"], *window)

    assert found["found"] is True
    assert found["rasi"] == "Gemini"
    assert found["reason"] is None
    stamp = jd_to_local_str(found["jd"], 5.5)
    assert stamp.startswith("2000-05-26 15:06")
    assert "3:06 pm (IST)" in str(MERCURY_IN_GEMINI_2000["entered"])

    moon = longitude_of(Graha.MOON)(found["jd"])
    assert int(moon // 30) == R["Aq"]
    assert format_dms(moon % 30, seconds=False) == "10-29"
    assert str(MERCURY_IN_GEMINI_2000["moon_at_entry"]) == "10 29 Aquarius"
    assert from_jd(found["jd"]).jd_ut == found["jd"]


def test_mercury_leaves_gemini_when_the_book_says_the_window_closes():
    """"May 26, 2000 - Aug 3, 2000"."""
    from hora.core.const import Graha
    from hora.core.timeutil import from_local, jd_to_local_str
    from hora.transits.murthi import MERCURY_IN_GEMINI_2000, rasi_ingress

    longitude_of = _ephemeris()
    found = rasi_ingress(
        longitude_of(Graha.MERCURY), R["Cn"],
        from_local(2000, 7, 20, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
        from_local(2000, 8, 20, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)

    assert found["found"] is True
    assert jd_to_local_str(found["jd"], 5.5).startswith("2000-08-03")
    assert "Aug 3, 2000" in str(MERCURY_IN_GEMINI_2000["window"])


def test_both_of_26_2s_worked_natives_get_the_murthi_the_book_gives():
    """One ingress, two nativities, two different forms — Swarna from an
    Aquarius Moon and Loha from Bill Gates's Pisces Moon.
    """
    from hora.charts.book import longitudes
    from hora.core.const import Graha
    from hora.core.timeutil import from_local
    from hora.transits.murthi import (
        MURTHI_WORKED_CASES,
        ONE_INGRESS_GIVES_A_DIFFERENT_MURTHI_TO_EACH_NATIVE,
        murthi,
        rasi_ingress,
    )

    longitude_of = _ephemeris()
    found = rasi_ingress(
        longitude_of(Graha.MERCURY), R["Ge"],
        from_local(2000, 5, 20, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
        from_local(2000, 6, 5, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)
    moon_at_entry = longitude_of(Graha.MOON)(found["jd"])

    first, second = MURTHI_WORKED_CASES
    got = murthi(R[str(first["natal_moon"])] * 30.0 + 5.0, moon_at_entry)
    assert (got["house"], got["murthi"]) == (1, "Swarna")
    assert got["results"] == "Highly favorable"

    gates = longitudes(24)["Moon"]                 # Chart 24, 14 Pi 35
    assert int(gates // 30) == R["Pi"] == R[str(second["natal_moon"])]
    got = murthi(gates, moon_at_entry)
    assert (got["house"], got["murthi"]) == (12, "Loha")
    assert got["results"] == "Highly unfavorable"
    assert second["chart"] == 24

    assert "Bill Gates" in ONE_INGRESS_GIVES_A_DIFFERENT_MURTHI_TO_EACH_NATIVE


def test_the_murthi_modifies_a_verdict_and_does_not_make_one():
    from hora.transits.murthi import (
        THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE,
        murthi,
    )

    got = murthi(R["Pi"] * 30.0 + 14.0, R["Aq"] * 30.0 + 10.0)
    assert got["modifies"] == THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE
    assert "may not give his full results" in got["modifies"]
    assert "suffer much" in got["modifies"]
    assert "whole transit of that rasi" in got["holds_for"]
    assert "verdict" not in got


def test_a_retrograde_entry_is_reported_not_silently_missed():
    """The scan brackets forward crossings only. Rather than returning a
    wrong moment it says it found none, and why.
    """
    from hora.core.timeutil import from_local
    from hora.transits.murthi import MurthiError, rasi_ingress

    def backwards(jd):
        return (100.0 - (jd % 30.0)) % 360.0

    start = from_local(2000, 1, 1, 0, 0, 0.0, utc_offset_hours=0.0).jd_ut
    got = rasi_ingress(backwards, 0, start, start + 20.0)
    assert got["found"] is False
    assert got["jd"] is None
    assert "retrograde" in got["reason"]

    with pytest.raises(MurthiError, match="must end after"):
        rasi_ingress(backwards, 0, start, start)


def test_murthi_helpers_check_their_inputs():
    from hora.core.validate import InputError
    from hora.transits.murthi import murthi_of_house

    for bad in (0, 13, -1):
        with pytest.raises(InputError):
            murthi_of_house(bad)
