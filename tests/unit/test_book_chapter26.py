"""Chapter 26 — transits: miscellaneous topics.

§26.1 sets out two threads, rasi principles chapter 25 left and nakshatra
interactions it never touched, and names not one of them. The last test here
is the coverage line, and it stays failing-by-omission until the chapter's own
sections arrive: nothing is built ahead of a page.
"""
from __future__ import annotations

from itertools import pairwise

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


# --------------------------------------------------------------------------
# §26.3 — rasi gochara vedha, and Table 63
# --------------------------------------------------------------------------

def test_table_63s_auspicious_houses_agree_with_chapter_25_except_for_venus():
    """"the good and bad houses ... in a previous chapter." Six rows are
    Tables 53 to 59 exactly; Venus adds the 8th and the 12th. D-74.
    """
    from hora.core.const import Graha
    from hora.transits.gochara import good_houses
    from hora.transits.vedha import TABLE_63_VEDHA

    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Mercury": Graha.MERCURY, "Jupiter": Graha.JUPITER,
             "Venus": Graha.VENUS, "Saturn": Graha.SATURN}
    assert set(TABLE_63_VEDHA) == set(named)

    disagreed = {}
    for name, graha in named.items():
        listed = tuple(sorted(TABLE_63_VEDHA[name]))
        chapter_25 = tuple(sorted(good_houses(int(graha))))
        if listed != chapter_25:
            disagreed[name] = (listed, chapter_25)
    assert set(disagreed) == {"Venus"}
    listed, chapter_25 = disagreed["Venus"]
    assert set(listed) - set(chapter_25) == {8, 12}
    assert set(chapter_25) - set(listed) == set()


def test_venus_8th_and_12th_are_flagged_not_reconciled():
    from hora.transits.vedha import vedha_sthana

    for house in (8, 12):
        got = vedha_sthana("Venus", house)
        assert got["auspicious"] is True
        assert got["disputed_by_chapter_25"] is True
        assert "D-74" in got["dispute"]
    for house in (1, 2, 3, 4, 5, 9, 11):
        assert vedha_sthana("Venus", house)["disputed_by_chapter_25"] is False
    # and no other graha has a disputed house at all
    from hora.transits.vedha import TABLE_63_VEDHA

    for name, row in TABLE_63_VEDHA.items():
        if name == "Venus":
            continue
        assert not any(vedha_sthana(name, h)["disputed_by_chapter_25"]
                       for h in row), name


def test_the_twelfth_dispute_is_the_mixed_row_chapter_25_already_flagged():
    """Table 58 marks Venus's 12th Bad and reads it well. Table 63 sides with
    the results text, so §26.3 resolves a row §25.2 left contradicting itself.
    """
    from hora.transits.gochara import (
        MIXED_ROWS,
        THE_TWELFTH_IS_BAD_EVERYWHERE_AND_READS_WELL_HERE,
    )
    from hora.transits.vedha import TABLE_63_VEDHA

    twelfth = next(row for row in MIXED_ROWS
                   if row["graha"] == "Venus" and row["house"] == 12)
    assert twelfth["snapshot"] == "Bad"
    assert "New friends, money, pleasures, gains" in str(twelfth["against_it"])
    assert 12 in TABLE_63_VEDHA["Venus"]
    assert "no harm at all" in THE_TWELFTH_IS_BAD_EVERYWHERE_AND_READS_WELL_HERE


def test_only_the_suns_row_has_a_constant_vedha_offset():
    from hora.transits.vedha import (
        ONLY_THE_SUNS_ROW_HAS_A_CONSTANT_OFFSET,
        TABLE_63_VEDHA,
    )

    offsets = {name: {(v - h) % 12 for h, v in row.items()}
               for name, row in TABLE_63_VEDHA.items()}
    assert offsets["Sun"] == {6}                # always the 7th from it
    assert all(len(o) > 1 for name, o in offsets.items() if name != "Sun")

    # and one house takes different partners for different grahas
    third = {name: row[3] for name, row in TABLE_63_VEDHA.items() if 3 in row}
    assert third == {"Sun": 9, "Moon": 9, "Mars": 12, "Venus": 1, "Saturn": 12}
    assert "the 7th from the auspicious house" in (
        ONLY_THE_SUNS_ROW_HAS_A_CONSTANT_OFFSET)


def test_mars_and_saturn_share_a_row_because_chapter_25_gave_them_one():
    from hora.core.const import Graha
    from hora.transits.gochara import good_houses
    from hora.transits.vedha import MARS_AND_SATURN_SHARE_A_ROW, TABLE_63_VEDHA

    assert TABLE_63_VEDHA["Mars"] == TABLE_63_VEDHA["Saturn"]
    assert good_houses(int(Graha.MARS)) == good_houses(int(Graha.SATURN))
    assert "Tables 55 and 59" in MARS_AND_SATURN_SHARE_A_ROW


def test_the_two_father_and_son_pairs_are_exempt():
    from hora.core.const import Graha
    from hora.transits.vedha import (
        VEDHA_EXCEPTIONS_ARE_FATHER_AND_SON,
        VEDHA_EXEMPT_PAIRS,
        causes_vedha,
    )

    assert len(VEDHA_EXEMPT_PAIRS) == 2
    for first, second in ((Graha.SUN, Graha.SATURN),
                          (Graha.MOON, Graha.MERCURY)):
        for a, b in ((first, second), (second, first)):
            got = causes_vedha(int(a), int(b))
            assert got["causes_vedha"] is False
            assert got["exempt"] is True
    # everyone else obstructs everyone else
    for a in range(7):
        for b in range(7):
            if a == b or frozenset({a, b}) in VEDHA_EXEMPT_PAIRS:
                continue
            assert causes_vedha(a, b)["causes_vedha"] is True
    assert causes_vedha(0, 0)["causes_vedha"] is False
    assert "father and son pairs" in VEDHA_EXCEPTIONS_ARE_FATHER_AND_SON


def test_26_3s_worked_case_finds_the_several_obstructing_planets():
    """"There were several planets causing vedha on Mercury on June 8, 2000."
    Four of them, all in Taurus, the 3rd from Bill Gates's Pisces Moon.
    """
    from hora.charts.book import longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.vedha import VEDHA_WORKED_CASE, vedha

    moon = longitudes(24)["Moon"]
    assert int(moon // 30) == R[str(VEDHA_WORKED_CASE["natal_moon"])] == R["Pi"]

    computed = compute_chart(
        from_local(2000, 6, 8, 12, 0, 0.0, utc_offset_hours=-7.0),
        Place(name="Seattle", latitude=47 + 36 / 60,
              longitude=-(122 + 20 / 60)),
        Settings(node_type=NodeType.MEAN))
    got = vedha(int(Graha.MERCURY), moon,
                {g: computed.positions[g].longitude for g in range(7)})

    assert got["house"] == 4 == VEDHA_WORKED_CASE["house"]
    assert got["transit_rasi"] == "Gemini"
    assert got["auspicious"] is True
    assert got["vedha_house"] == 3 == VEDHA_WORKED_CASE["vedha_house"]
    assert got["vedha_rasi"] == "Taurus"
    assert sorted(got["obstructors"]) == ["Jupiter", "Saturn", "Sun", "Venus"]
    assert got["exempt_in_the_vedha_sthana"] == []
    assert got["obstructed"] is True
    assert "cannot give its good results" in got["results"]


def test_the_moon_would_have_been_exempt_had_it_been_in_the_vedha_sthana():
    """Mercury's obstruction is judged with the Moon-Mercury exception live:
    on the day the Moon was in Leo, but if it were in Taurus it would be
    listed as exempt rather than as an obstructor.
    """
    from hora.core.const import Graha
    from hora.transits.vedha import vedha

    moon_natal = R["Pi"] * 30.0 + 14.0
    longitudes = {int(Graha.MERCURY): R["Ge"] * 30.0 + 10.0,
                  int(Graha.MOON): R["Ta"] * 30.0 + 5.0,
                  int(Graha.SUN): R["Ta"] * 30.0 + 20.0}
    got = vedha(int(Graha.MERCURY), moon_natal, longitudes)

    assert got["vedha_rasi"] == "Taurus"
    assert got["obstructors"] == ["Sun"]
    assert got["exempt_in_the_vedha_sthana"] == ["Moon"]
    assert got["obstructed"] is True


def test_an_unobstructed_good_transit_is_reported_as_standing():
    from hora.core.const import Graha
    from hora.transits.vedha import vedha

    got = vedha(int(Graha.MERCURY), R["Pi"] * 30.0 + 14.0,
                {int(Graha.MERCURY): R["Ge"] * 30.0 + 10.0,
                 int(Graha.SUN): R["Le"] * 30.0 + 1.0})
    assert got["obstructed"] is False
    assert got["obstructors"] == []
    assert "the good transit stands" in got["results"]


def test_a_house_table_63_does_not_call_auspicious_has_no_vedha():
    from hora.core.const import Graha
    from hora.transits.vedha import vedha, vedha_sthana

    got = vedha_sthana("Mercury", 12)
    assert got["auspicious"] is False
    assert got["vedha_house"] is None
    assert "does not arise" in got["reason"]

    run = vedha(int(Graha.MERCURY), R["Pi"] * 30.0 + 14.0,
                {int(Graha.MERCURY): R["Aq"] * 30.0 + 10.0})
    assert run["auspicious"] is False
    assert run["obstructed"] is None
    assert run["obstructors"] == []


def test_vedha_and_murthi_are_named_together_as_the_two_brakes():
    from hora.transits.murthi import (
        THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE,
    )
    from hora.transits.vedha import VEDHA_AND_MURTHI_ARE_BOTH_BRAKES

    assert "vedhas and murthis" in VEDHA_AND_MURTHI_ARE_BOTH_BRAKES
    assert "marginal results" in VEDHA_AND_MURTHI_ARE_BOTH_BRAKES
    assert "full results" in THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE


def test_vedha_helpers_check_their_inputs():
    from hora.core.const import Graha
    from hora.core.validate import InputError
    from hora.transits.vedha import VedhaError, causes_vedha, vedha, vedha_sthana

    with pytest.raises(VedhaError, match="no row in Table 63"):
        vedha_sthana("Rahu", 3)
    for bad in (0, 13):
        with pytest.raises(InputError):
            vedha_sthana("Sun", bad)
    for bad in (7, 8, -1):
        with pytest.raises(InputError):
            causes_vedha(bad, 0)
    with pytest.raises(VedhaError, match="graha being judged"):
        vedha(int(Graha.MERCURY), 0.0, {int(Graha.SUN): 10.0})


# --------------------------------------------------------------------------
# §26.4.1 — taras, and Table 64
# --------------------------------------------------------------------------

def test_table_64_grades_all_27_counts_in_a_nine_cycle():
    from hora.transits.tara import (
        TABLE_64_IS_A_NINE_CYCLE,
        TABLE_64_TARAS,
        tara_of_count,
    )

    assert len(TABLE_64_TARAS) == 9
    counts = [c for row in TABLE_64_TARAS for c in row["counts"]]
    assert sorted(counts) == list(range(1, 28))
    assert all(len(row["counts"]) == 3 for row in TABLE_64_TARAS)

    for count in range(1, 28):
        row = tara_of_count(count)
        assert count in row["counts"]
        assert row["position_in_cycle"] == (count - 1) % 9 + 1
        assert tara_of_count(count)["name"] == (
            tara_of_count((count - 1) % 9 + 1)["name"])
    assert "only modulo 9" in TABLE_64_IS_A_NINE_CYCLE


def test_janma_tara_is_mixed_and_the_rest_split_five_to_three():
    from hora.transits.tara import (
        FOUR_GOOD_THREE_BAD_ONE_MIXED,
        TABLE_64_TARAS,
        tara_of_count,
    )

    assert tara_of_count(1)["name"] == "Janma Tara"
    assert tara_of_count(1)["good"] is None
    assert tara_of_count(1)["grade"] == "mixed"

    good = [r["name"] for r in TABLE_64_TARAS if r["good"] is True]
    bad = [r["name"] for r in TABLE_64_TARAS if r["good"] is False]
    mixed = [r["name"] for r in TABLE_64_TARAS if r["good"] is None]
    assert len(good) == 5 and len(bad) == 3 and len(mixed) == 1
    assert bad == ["Vipat Tara", "Pratyak Tara", "Naidhana/Vadha Tara"]
    assert "Janma alone is mixed" in FOUR_GOOD_THREE_BAD_ONE_MIXED


def test_a_tara_group_is_exactly_one_vimsottari_lords_holding():
    """§25.6 proved a nakshatra shares its lord with the 10th and 19th from
    it. Table 64's rows are those triples counted from the natal Moon — the
    same partition of the 27, and this checks all 243 combinations.
    """
    from hora.core.constants.nakshatra import NAKSHATRA_LORD
    from hora.transits.tara import (
        A_TARA_GROUP_IS_ONE_VIMSOTTARI_LORDS_HOLDING,
        TABLE_64_TARAS,
    )

    for natal in range(27):
        for row in TABLE_64_TARAS:
            group = {(natal + count - 1) % 27 for count in row["counts"]}
            lords = {NAKSHATRA_LORD[n] for n in group}
            assert len(lords) == 1, (natal, row["name"])
            lord = lords.pop()
            assert {n for n in range(27)
                    if NAKSHATRA_LORD[n] == lord} == group
    assert "same partition of the 27" in (
        A_TARA_GROUP_IS_ONE_VIMSOTTARI_LORDS_HOLDING)


def test_the_counting_illustration_makes_swati_the_sixth_from_makha():
    """"Counting constellations from Makha ... Swaati is the 6th." And the
    list under it opens "Maksha", which is a slip.
    """
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.tara import (
        MAKSHA_IS_A_SLIP_FOR_MAKHA,
        NAKSHATRA_SPAN,
        TARA_COUNTING_EXAMPLE,
        tara,
    )

    names = [str(n) for n in NAKSHATRA_NAMES]
    makha, swati = names.index("Magha"), names.index("Swati")
    got = tara(makha * NAKSHATRA_SPAN + 1.0, swati * NAKSHATRA_SPAN + 1.0)
    assert got["count"] == 6
    assert got["tara"] == "Saadhana Tara"

    assert "(1) Maksha" in TARA_COUNTING_EXAMPLE
    assert TARA_COUNTING_EXAMPLE.count("Makha") == 2
    assert "not the book's own spelling" in MAKSHA_IS_A_SLIP_FOR_MAKHA


def test_bill_gates_natal_moon_is_in_uttarabhadrapada():
    from hora.charts.book import longitudes
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.tara import TARA_WORKED_CASE, nakshatra_of

    index = nakshatra_of(longitudes(24)["Moon"])
    assert index == 25                      # the 26th, 1-based
    assert str(NAKSHATRA_NAMES[index]) == "Uttara Bhadrapada"
    assert str(TARA_WORKED_CASE["natal_nakshatra"]) == "Uttara Bhadrapada"


def test_26_4_1s_worked_case_puts_five_planets_in_bad_taras():
    """"From Uttarabhadrapada, Krittika is the 5th star ... and Mrigasira is
    the 7th star ... With 5 planets transiting in bad taras."
    """
    from hora.charts.book import longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.tara import TARA_WORKED_CASE, tara_bala

    computed = compute_chart(
        from_local(2000, 6, 8, 12, 0, 0.0, utc_offset_hours=-7.0),
        Place(name="Seattle", latitude=47 + 36 / 60,
              longitude=-(122 + 20 / 60)),
        Settings(node_type=NodeType.MEAN))
    got = tara_bala(longitudes(24)["Moon"],
                    {g: computed.positions[g].longitude for g in range(7)})

    assert got["of"] == 7
    assert got["count_in_bad_taras"] == 5 == TARA_WORKED_CASE["in_bad_taras"]
    assert sorted(got["in_bad_taras"]) == [
        "Jupiter", "Mars", "Saturn", "Sun", "Venus"]
    assert sorted(got["in_good_taras"]) == ["Mercury", "Moon"]
    assert got["unaccounted"] == []

    for block in TARA_WORKED_CASE["placements"]:
        for graha in block["grahas"]:
            entry = got["per_graha"][graha]
            assert entry["transit_nakshatra"] == block["nakshatra"], graha
            assert entry["count"] == block["count"], graha
            assert entry["tara"] == block["tara"], graha
            assert entry["good"] is False


def test_a_graha_in_the_natal_moons_own_nakshatra_is_janma_tara():
    from hora.transits.tara import NAKSHATRA_SPAN, tara

    got = tara(10 * NAKSHATRA_SPAN + 2.0, 10 * NAKSHATRA_SPAN + 9.0)
    assert got["count"] == 1
    assert got["tara"] == "Janma Tara"
    assert got["good"] is None
    assert got["results"] is None


def test_the_tally_leaves_janma_tara_in_neither_column():
    from hora.core.const import Graha
    from hora.transits.tara import NAKSHATRA_SPAN, tara_bala

    natal = 10 * NAKSHATRA_SPAN + 2.0
    got = tara_bala(natal, {
        int(Graha.SUN): natal + 1.0,                       # Janma
        int(Graha.MARS): natal + 2 * NAKSHATRA_SPAN,       # Vipat, bad
        int(Graha.VENUS): natal + NAKSHATRA_SPAN,          # Sampat, good
    })
    assert got["unaccounted"] == ["Sun"]
    assert got["in_bad_taras"] == ["Mars"]
    assert got["in_good_taras"] == ["Venus"]
    assert (len(got["in_good_taras"]) + len(got["in_bad_taras"])
            + len(got["unaccounted"])) == got["of"]
    assert "neither column" in got["janma_is_mixed"]


def test_the_muhurta_use_asks_only_that_the_moon_is_not_in_a_bad_tara():
    from hora.transits.tara import (
        NAKSHATRA_SPAN,
        TARA_IN_MUHURTA,
        muhurta_moon_is_clear,
    )

    natal = 0.5
    assert muhurta_moon_is_clear(natal, NAKSHATRA_SPAN + 1)["clear"] is True
    assert muhurta_moon_is_clear(natal,
                                 2 * NAKSHATRA_SPAN + 1)["clear"] is False
    janma = muhurta_moon_is_clear(natal, 1.0)
    assert janma["clear"] is True and janma["mixed"] is True
    assert "new project is launched" in TARA_IN_MUHURTA


def test_tara_helpers_check_their_inputs():
    from hora.core.validate import InputError
    from hora.transits.tara import TaraError, tara_bala, tara_of_count

    for bad in (0, 28, -1):
        with pytest.raises(InputError):
            tara_of_count(bad)
    with pytest.raises(TaraError, match="at least one"):
        tara_bala(0.0, {})
    with pytest.raises(InputError):
        tara_bala(0.0, {9: 10.0})


# --------------------------------------------------------------------------
# §26.4.2 — the eleven special nakshatras
# --------------------------------------------------------------------------

def test_the_eleven_special_nakshatras_are_transcribed_as_numbered():
    from hora.transits.tara import SPECIAL_NAKSHATRAS

    assert len(SPECIAL_NAKSHATRAS) == 11
    assert [row["offset"] for row in SPECIAL_NAKSHATRAS] == [
        1, 10, 18, 16, 4, 7, 12, 13, 19, 22, 25]
    assert len({row["offset"] for row in SPECIAL_NAKSHATRAS}) == 11
    assert len({row["name"] for row in SPECIAL_NAKSHATRAS}) == 11
    assert all(1 <= int(row["offset"]) <= 27 for row in SPECIAL_NAKSHATRAS)

    named = {row["name"]: row for row in SPECIAL_NAKSHATRAS}
    assert named["Abhisheka"]["also_called"] == "Raajya (kingdom)"
    assert named["Vainaasika"]["also_called"] == "Vinaasana"
    assert named["Naidhana"]["offset"] == 7
    assert named["Janma"]["offset"] == 1


def test_nine_of_the_eleven_are_three_complete_vimsottari_holdings():
    """Janma/Karma/Aadhaana, Jaati/Abhisheka/Vainaasika and
    Naidhana/Sanghaatika/Maanasa are three whole tara triples; Desa and
    Saamudaayika stand alone.
    """
    from collections import defaultdict

    from hora.core.constants.nakshatra import NAKSHATRA_LORD
    from hora.transits.tara import (
        NINE_OF_THE_ELEVEN_FORM_THREE_COMPLETE_TRIPLES,
        SPECIAL_NAKSHATRAS,
        tara_of_count,
    )

    grouped = defaultdict(list)
    for row in SPECIAL_NAKSHATRAS:
        grouped[tara_of_count(int(row["offset"]))["name"]].append(
            str(row["name"]))

    complete = {t: sorted(names) for t, names in grouped.items()
                if len(names) == 3}
    singles = {t: names for t, names in grouped.items() if len(names) == 1}
    assert len(complete) == 3
    assert len(singles) == 2
    assert sorted(n for names in singles.values() for n in names) == [
        "Desa", "Saamudaayika"]
    assert complete["Janma Tara"] == ["Aadhaana", "Janma", "Karma"]
    assert complete["Kshema Tara"] == ["Abhisheka", "Jaati", "Vainaasika"]
    assert complete["Naidhana/Vadha Tara"] == [
        "Maanasa", "Naidhana", "Sanghaatika"]

    # each complete triple really is one Vimsottari lord's holding
    offsets = {str(row["name"]): int(row["offset"])
               for row in SPECIAL_NAKSHATRAS}
    for natal in range(27):
        for names in complete.values():
            group = {(natal + offsets[n] - 1) % 27 for n in names}
            assert len({NAKSHATRA_LORD[x] for x in group}) == 1
    assert "no partners among the eleven" in (
        NINE_OF_THE_ELEVEN_FORM_THREE_COMPLETE_TRIPLES)


def test_a_special_nakshatras_subject_says_nothing_about_its_taras_grade():
    """Vainaasika shows destruction and sits in a good tara; Sanghaatika and
    Maanasa show social life and the mind and sit in a bad one.
    """
    from hora.transits.tara import (
        THE_TWO_CLASSIFICATIONS_ARE_INDEPENDENT,
        special_nakshatra,
    )

    natal = 5.0
    destruction = special_nakshatra("Vainaasika", natal)
    assert destruction["tara"] == "Kshema Tara"
    for name in ("Sanghaatika", "Maanasa"):
        assert special_nakshatra(name, natal)["tara"] == "Naidhana/Vadha Tara"
    assert special_nakshatra("Naidhana", natal)["tara"] == (
        "Naidhana/Vadha Tara")
    assert "separate readings of the same position" in (
        THE_TWO_CLASSIFICATIONS_ARE_INDEPENDENT)


def test_bill_gatess_jaati_is_bharani_and_his_karma_is_pushya():
    """"His jaati nakshatra is the 4th from Uttarabhadrapada, i.e. Bharani.
    His karma nakshatra is the 10th ... i.e. Pushyami."
    """
    from hora.charts.book import longitudes
    from hora.transits.tara import (
        SPECIAL_NAKSHATRA_WORKED_CASE,
        special_nakshatra,
    )

    moon = longitudes(24)["Moon"]
    jaati = special_nakshatra("Jaati", moon)
    karma = special_nakshatra("Karma", moon)

    assert jaati["janma_nakshatra"] == "Uttara Bhadrapada"
    assert jaati["nakshatra"] == "Bharani"
    assert karma["nakshatra"] == "Pushya"          # the book writes Pushyami
    assert str(SPECIAL_NAKSHATRA_WORKED_CASE["jaati"]) == "Bharani"
    assert str(SPECIAL_NAKSHATRA_WORKED_CASE["karma"]) == "Pushya"


def test_the_two_named_transits_hold_together_for_eight_months():
    """§26.4.2 gives no dates. Saturn is in Bharani and Rahu in Pushya
    together from 20 September 1999 to 11 May 2000, which is before the
    8 June 2000 ruling the other two sections read.
    """
    from hora.charts.book import longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.tara import (
        THE_TWO_SPECIAL_TRANSITS_OVERLAP_FOR_EIGHT_MONTHS,
        nakshatra_of,
        special_nakshatra,
    )

    moon = longitudes(24)["Moon"]
    bharani = nakshatra_of_name = special_nakshatra("Jaati", moon)["index"]
    pushya = special_nakshatra("Karma", moon)["index"]
    place = Place(name="Seattle", latitude=47 + 36 / 60,
                  longitude=-(122 + 20 / 60))
    settings = Settings(node_type=NodeType.MEAN)

    def where(year, month, day, graha):
        computed = compute_chart(
            from_local(year, month, day, 12, 0, 0.0, utc_offset_hours=-8.0),
            place, settings)
        return nakshatra_of(computed.positions[int(graha)].longitude)

    # inside the window both hold
    for date in ((1999, 11, 5), (2000, 4, 3)):
        assert where(*date, Graha.SATURN) == bharani
        assert where(*date, Graha.RAHU) == pushya
    # outside it, at least one does not
    assert where(1999, 6, 1, Graha.RAHU) != pushya
    assert where(2000, 6, 8, Graha.SATURN) != bharani

    assert nakshatra_of_name == bharani
    assert "20 September 1999 to 11 May 2000" in (
        THE_TWO_SPECIAL_TRANSITS_OVERLAP_FOR_EIGHT_MONTHS)


def test_special_transits_places_both_grahas_the_section_names():
    from hora.charts.book import longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.tara import (
        SPECIAL_NAKSHATRA_WORKED_CASE,
        special_transits,
    )

    moon = longitudes(24)["Moon"]
    computed = compute_chart(
        from_local(1999, 11, 5, 12, 0, 0.0, utc_offset_hours=-8.0),
        Place(name="Seattle", latitude=47 + 36 / 60,
              longitude=-(122 + 20 / 60)),
        Settings(node_type=NodeType.MEAN))
    got = special_transits(moon,
                           {g: computed.positions[g].longitude
                            for g in range(9)})

    found = {hit["graha"]: hit for hit in got["in_special_nakshatras"]}
    for reading in SPECIAL_NAKSHATRA_WORKED_CASE["readings"]:
        hit = found[str(reading["graha"])]
        assert hit["nakshatra"] == reading["nakshatra"]
        assert hit["special"] == reading["special"]
    assert got["of"] == 9
    assert got["verdict"] is None
    assert "gives no number for \"many\"" in got["undecided"]


def test_the_section_says_the_results_are_the_natives_not_the_worlds():
    from hora.transits.tara import (
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE,
        SPECIAL_NAKSHATRAS_REACH_BEYOND_THE_VARGAS,
    )

    assert "may not ruin one's country" in RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE
    assert "almost the same number of people" in (
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE)
    assert "cannot be gained by looking at any divisional chart" in (
        SPECIAL_NAKSHATRAS_REACH_BEYOND_THE_VARGAS)


def test_special_nakshatra_helpers_check_their_inputs():
    from hora.core.validate import InputError
    from hora.transits.tara import (
        SPECIAL_NAKSHATRAS,
        TaraError,
        special_nakshatra,
        special_nakshatras,
        special_transits,
    )

    with pytest.raises(TaraError, match="not one of section 26.4.2's"):
        special_nakshatra("Rajya", 0.0)
    with pytest.raises(TaraError, match="at least one"):
        special_transits(0.0, {})
    with pytest.raises(InputError):
        special_transits(0.0, {9: 10.0})
    assert len(special_nakshatras(0.0)) == len(SPECIAL_NAKSHATRAS)


# --------------------------------------------------------------------------
# §26.5 — nakshatra-based aspects
# --------------------------------------------------------------------------

def test_26_5s_five_lists_are_transcribed_as_printed():
    from hora.charts.aspects import (
        NAKSHATRA_DRISHTI,
        NAKSHATRA_DRISHTI_RULE,
        nakshatra_drishti,
    )
    from hora.core.const import Graha

    assert NAKSHATRA_DRISHTI == {
        int(Graha.SUN): (14, 15),
        int(Graha.MOON): (14, 15),
        int(Graha.MARS): (1, 3, 7, 8, 15),
        int(Graha.MERCURY): (1, 15),
        int(Graha.JUPITER): (10, 15, 19),
        int(Graha.VENUS): (1, 15),
        int(Graha.SATURN): (3, 5, 15, 19),
    }
    assert nakshatra_drishti(int(Graha.SUN)) == nakshatra_drishti(
        int(Graha.MOON))
    assert nakshatra_drishti(int(Graha.MERCURY)) == nakshatra_drishti(
        int(Graha.VENUS))
    for offsets in NAKSHATRA_DRISHTI.values():
        assert all(1 <= o <= 27 for o in offsets)
        assert list(offsets) == sorted(set(offsets))
    assert "14th and 15th constellations" in NAKSHATRA_DRISHTI_RULE


def test_every_graha_aspects_the_fifteenth_and_that_is_the_opposition():
    """Half of 27 is 13.5, so 180 degrees from a nakshatra's midpoint lands
    exactly on the join between the 14th and 15th from it.
    """
    from hora.charts.aspects import (
        EVERY_GRAHA_ASPECTS_THE_FIFTEENTH,
        NAKSHATRA_DRISHTI,
    )

    assert all(15 in offsets for offsets in NAKSHATRA_DRISHTI.values())

    span = 360.0 / 27
    for index in range(27):
        midpoint = (index + 0.5) * span
        opposite = (midpoint + 180.0) % 360.0
        # the boundary between the 14th and the 15th from `index`
        boundary = ((index + 14) % 27) * span
        assert abs(opposite - boundary) < 1e-9, index
    assert "exactly on the join" in EVERY_GRAHA_ASPECTS_THE_FIFTEENTH


def test_only_the_luminaries_take_the_fourteenth():
    from hora.charts.aspects import NAKSHATRA_DRISHTI
    from hora.core.const import Graha

    takers = {g for g, offsets in NAKSHATRA_DRISHTI.items() if 14 in offsets}
    assert takers == {int(Graha.SUN), int(Graha.MOON)}


def test_three_grahas_aspect_their_own_nakshatra_which_drishti_never_does():
    from hora.charts.aspects import (
        NAKSHATRA_DRISHTI,
        THREE_GRAHAS_ASPECT_THEIR_OWN_NAKSHATRA,
        graha_drishti_houses,
    )
    from hora.core.const import Graha

    own = {g for g, offsets in NAKSHATRA_DRISHTI.items() if 1 in offsets}
    assert own == {int(Graha.MARS), int(Graha.MERCURY), int(Graha.VENUS)}
    for graha in range(7):
        assert 1 not in graha_drishti_houses(graha)
    assert "no counterpart there" in THREE_GRAHAS_ASPECT_THEIR_OWN_NAKSHATRA


def test_the_same_three_grahas_aspect_most_under_both_schemes():
    from hora.charts.aspects import (
        NAKSHATRA_DRISHTI,
        THE_SAME_THREE_GRAHAS_ASPECT_MOST_IN_BOTH_SCHEMES,
        graha_drishti_houses,
    )
    from hora.core.const import Graha

    many_nakshatras = {g for g, offsets in NAKSHATRA_DRISHTI.items()
                       if len(offsets) > 2}
    special_houses = {g for g in range(7)
                      if len(graha_drishti_houses(g)) > 1}
    assert many_nakshatras == special_houses == {
        int(Graha.MARS), int(Graha.JUPITER), int(Graha.SATURN)}

    assert len(NAKSHATRA_DRISHTI[int(Graha.MARS)]) == 5
    assert len(NAKSHATRA_DRISHTI[int(Graha.SATURN)]) == 4
    assert len(NAKSHATRA_DRISHTI[int(Graha.JUPITER)]) == 3
    assert max(len(graha_drishti_houses(g)) for g in range(7)) == len(
        graha_drishti_houses(int(Graha.MARS)))
    assert "Mars leads there too" in (
        THE_SAME_THREE_GRAHAS_ASPECT_MOST_IN_BOTH_SCHEMES)


def test_jupiters_tenth_and_nineteenth_are_his_own_vimsottari_triple():
    """§25.6 proved a nakshatra shares its lord with the 10th and 19th from
    it, so Jupiter aspects the rest of his own nakshatra's holding — from
    every one of the 27.
    """
    from hora.charts.aspects import (
        JUPITER_ASPECTS_HIS_OWN_VIMSOTTARI_TRIPLE,
        NAKSHATRA_DRISHTI,
        nakshatra_aspects,
    )
    from hora.core.const import Graha
    from hora.core.constants.nakshatra import NAKSHATRA_LORD

    for start in range(27):
        aspected = nakshatra_aspects(int(Graha.JUPITER), start)
        same_lord = {n for n in aspected
                     if NAKSHATRA_LORD[n] == NAKSHATRA_LORD[start]}
        assert len(same_lord) == 2, start
        assert same_lord | {start} == {n for n in range(27)
                                       if NAKSHATRA_LORD[n]
                                       == NAKSHATRA_LORD[start]}

    # Saturn takes the 19th of that pair and not the 10th
    assert 19 in NAKSHATRA_DRISHTI[int(Graha.SATURN)]
    assert 10 not in NAKSHATRA_DRISHTI[int(Graha.SATURN)]
    assert "Saturn aspects the 19th alone of that pair" in (
        JUPITER_ASPECTS_HIS_OWN_VIMSOTTARI_TRIPLE)


def test_nakshatra_aspects_counts_inclusively_and_wraps():
    from hora.charts.aspects import graha_aspects_nakshatra, nakshatra_aspects
    from hora.core.const import Graha

    # Mars aspects the 1st, so he aspects the nakshatra he stands in
    assert 5 in nakshatra_aspects(int(Graha.MARS), 5)
    assert graha_aspects_nakshatra(int(Graha.MARS), 5, 5) is True
    assert graha_aspects_nakshatra(int(Graha.SUN), 5, 5) is False

    # the 15th from Aswini is Swati, index 14
    assert 14 in nakshatra_aspects(int(Graha.SUN), 0)
    assert 13 in nakshatra_aspects(int(Graha.SUN), 0)      # the 14th
    # and it wraps
    assert nakshatra_aspects(int(Graha.SUN), 26) == tuple(sorted(
        (26 + off - 1) % 27 for off in (14, 15)))


def test_the_nodes_are_refused_rather_than_given_a_default():
    from hora.charts.aspects import (
        THE_NODES_ARE_NOT_GIVEN_NAKSHATRA_ASPECTS,
        nakshatra_aspects,
        nakshatra_drishti,
    )
    from hora.core.const import Graha

    for node in (Graha.RAHU, Graha.KETU):
        with pytest.raises(ValueError, match="seven planets only"):
            nakshatra_drishti(int(node))
        with pytest.raises(ValueError, match="seven planets only"):
            nakshatra_aspects(int(node), 0)
    assert "does not say whether they" in (
        THE_NODES_ARE_NOT_GIVEN_NAKSHATRA_ASPECTS)


def test_the_results_rule_is_by_natural_benefic_or_malefic():
    from hora.charts.aspects import NAKSHATRA_DRISHTI_RESULTS
    from hora.core.const import NATURAL_BENEFIC, NATURAL_MALEFIC, Graha

    assert "natural benefic" in NAKSHATRA_DRISHTI_RESULTS
    assert "natural malefic" in NAKSHATRA_DRISHTI_RESULTS
    # every graha the section covers has a natural nature to read it by
    covered = {Graha(g) for g in (0, 1, 2, 3, 4, 5, 6)}
    assert covered <= (NATURAL_BENEFIC | NATURAL_MALEFIC | {Graha.MERCURY,
                                                            Graha.MOON})


def test_nakshatra_aspects_check_their_inputs():
    from hora.charts.aspects import graha_aspects_nakshatra, nakshatra_aspects
    from hora.core.const import Graha

    for bad in (-1, 27):
        with pytest.raises(ValueError, match="between 0 and 26"):
            nakshatra_aspects(int(Graha.SUN), bad)
        with pytest.raises(ValueError, match="between 0 and 26"):
            graha_aspects_nakshatra(int(Graha.SUN), 0, bad)


# --------------------------------------------------------------------------
# Exercise 41 — Chart 60 read a third way
# --------------------------------------------------------------------------

def _chart_60_accession():
    """Chart 60's natal longitudes and the accession-day transit."""
    from hora.charts.book import longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    computed = compute_chart(
        from_local(1984, 10, 31, 12, 0, 0.0, utc_offset_hours=5.5),
        Place(name="New Delhi", latitude=28 + 36 / 60,
              longitude=77 + 12 / 60),
        Settings(node_type=NodeType.MEAN))
    return longitudes(60), computed


def test_every_claim_in_exercise_41_holds_against_chart_60():
    from hora.charts.functional import is_yogakaraka
    from hora.charts.house import house_of_rasi
    from hora.core.const import NAKSHATRA_NAMES, Graha
    from hora.transits.tara import (
        EXERCISE_41_CLAIMS,
        EXERCISE_41_IS_CHART_60_A_THIRD_TIME,
        nakshatra_of,
        special_nakshatra,
        tara,
    )

    natal, transit = _chart_60_accession()
    lagna = int(natal["Asc"] // 30)

    assert A[lagna] == "Le"
    assert A[int(natal["Moon"] // 30)] == "Le"
    assert str(NAKSHATRA_NAMES[nakshatra_of(natal["Moon"])]) == (
        "Purva Phalguni")

    for graha in (Graha.JUPITER, Graha.MARS):
        longitude = transit.positions[int(graha)].longitude
        assert A[int(longitude // 30)] == "Sg", graha
        assert str(NAKSHATRA_NAMES[nakshatra_of(longitude)]) == (
            "Purva Ashadha"), graha

    assert is_yogakaraka("Mars", lagna) is True
    assert house_of_rasi(lagna, R["Sg"]) == 5
    assert house_of_rasi(int(natal["Moon"] // 30), R["Sg"]) == 5

    jupiter = transit.positions[int(Graha.JUPITER)].longitude
    assert tara(natal["Moon"], jupiter)["count"] == 10
    assert special_nakshatra("Karma", natal["Moon"])["nakshatra"] == (
        "Purva Ashadha")

    assert len(EXERCISE_41_CLAIMS) == 7
    assert "Chart 60's own figures" in EXERCISE_41_IS_CHART_60_A_THIRD_TIME


def test_the_karma_nakshatra_is_also_janma_tara_and_the_reading_skips_it():
    from hora.transits.tara import (
        KARMA_IS_ALSO_JANMA_TARA_AND_THE_READING_IGNORES_THE_TARA,
        special_nakshatra,
        tara_of_count,
    )

    natal, _transit = _chart_60_accession()
    assert tara_of_count(10)["name"] == "Janma Tara"
    assert tara_of_count(10)["good"] is None            # mixed
    karma = special_nakshatra("Karma", natal["Moon"])
    assert karma["tara"] == "Janma Tara"
    assert karma["shows"] == "profession and workplace"
    assert "whose grade is mixed" in (
        KARMA_IS_ALSO_JANMA_TARA_AND_THE_READING_IGNORES_THE_TARA)


def test_a_natural_malefic_is_read_as_favourable_for_being_a_yogakaraka():
    """§26.4.2 and §26.5 both grade by natural nature. Exercise 41 reads Mars,
    a natural malefic, as part of a favourable transit because he is a
    yogakaraka — functional nature, unannounced.
    """
    from hora.charts.aspects import NAKSHATRA_DRISHTI_RESULTS
    from hora.charts.functional import is_yogakaraka
    from hora.core.const import NATURAL_MALEFIC, Graha
    from hora.transits.tara import (
        A_YOGAKARAKA_MALEFIC_IS_READ_AS_FAVOURABLE,
        SPECIAL_NAKSHATRA_RULE,
    )

    assert Graha.MARS in NATURAL_MALEFIC
    assert is_yogakaraka("Mars", R["Le"]) is True
    assert "Benefics or malefics" in SPECIAL_NAKSHATRA_RULE
    assert "natural malefic" in NAKSHATRA_DRISHTI_RESULTS
    assert "on the strength of the lordship alone" in (
        A_YOGAKARAKA_MALEFIC_IS_READ_AS_FAVOURABLE)


def test_jupiter_was_past_his_moolatrikona_arc_on_the_accession_day():
    """"Jupiter is transiting in his moolatrikona." The rasi is right and the
    degrees are not — §3.3 gives him the first 10 degrees of Sg. D-75.
    """
    from hora.core.const import MOOLATRIKONA, Graha

    _natal, transit = _chart_60_accession()
    rasi, start, end = MOOLATRIKONA[int(Graha.JUPITER)]
    assert (int(rasi), start, end) == (R["Sg"], 0.0, 10.0)

    jupiter = transit.positions[int(Graha.JUPITER)].longitude
    assert int(jupiter // 30) == int(rasi)            # own sign, as claimed
    assert not start <= jupiter % 30 < end            # but past the arc
    assert 15.0 < jupiter % 30 < 15.2


def test_exercise_41_reads_a_chart_the_register_already_held():
    from hora.charts.book import chart

    record = chart(60)
    assert "Rajiv Gandhi" in record["title"]
    assert "Exercise 41" in record["note"]
    assert record["events"] == {
        "he became Prime Minister of India": "October 31, 1984"}


# --------------------------------------------------------------------------
# Exercise 42 — Chart 56's death, read a second way
# --------------------------------------------------------------------------

def test_every_claim_in_exercise_42_holds_against_chart_56():
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.charts.maraka import maraka_houses, maraka_sthanas
    from hora.core.const import (
        NAKSHATRA_NAMES,
        NATURAL_MALEFIC,
        RASI_LORD,
        Graha,
    )
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.tara import (
        EXERCISE_42_CLAIMS,
        NAKSHATRA_SPAN,
        nakshatra_of,
        special_nakshatra,
        tara,
    )

    natal = longitudes(56)
    lagna = int(natal["Asc"] // 30)
    assert A[lagna] == "Le"

    moon = natal["Moon"]
    index = nakshatra_of(moon)
    assert str(NAKSHATRA_NAMES[index]) == "Dhanishta"
    pada = int((moon % NAKSHATRA_SPAN) // (NAKSHATRA_SPAN / 4)) + 1
    assert pada == 4

    bharani = [str(n) for n in NAKSHATRA_NAMES].index("Bharani")
    assert (bharani - index) % 27 + 1 == 7
    assert special_nakshatra("Naidhana", moon)["nakshatra"] == "Bharani"

    assert Graha.SATURN in NATURAL_MALEFIC
    assert maraka_houses() == (2, 7)
    seventh = maraka_sthanas(lagna)[7]
    assert A[seventh] == "Aq"
    assert RASI_LORD[seventh] == int(Graha.SATURN)

    block = chart(56)["transit"]
    computed = compute_chart(from_local(**block["birth_data"]),
                             Place(name="Martha's Vineyard", **block["place"]),
                             Settings(node_type=NodeType.MEAN))
    saturn = computed.positions[int(Graha.SATURN)].longitude
    assert nakshatra_of(saturn) == bharani
    assert tara(moon, saturn)["count"] == 7
    assert tara(moon, saturn)["tara"] == "Naidhana/Vadha Tara"

    assert len(EXERCISE_42_CLAIMS) == 7


def test_the_naidhana_reading_leans_on_a_maraka_lordship_as_well():
    from hora.transits.tara import (
        EXERCISE_42_ANSWER,
        THE_NAIDHANA_READING_NEEDS_A_MARAKA_TOO,
    )

    assert "7th lord" in EXERCISE_42_ANSWER
    assert "maraka" in EXERCISE_42_ANSWER
    assert "malefic" in EXERCISE_42_ANSWER
    assert "not on the nakshatra alone" in (
        THE_NAIDHANA_READING_NEEDS_A_MARAKA_TOO)


def test_the_naidhana_special_nakshatra_and_the_naidhana_tara_coincide_here():
    """The 7th from the natal Moon's nakshatra is Naidhana under both of
    §26.4's classifications — the one place they name the same thing.
    """
    from hora.transits.tara import (
        SPECIAL_NAKSHATRAS,
        TABLE_64_TARAS,
        special_nakshatra,
        tara_of_count,
    )

    naidhana = next(r for r in SPECIAL_NAKSHATRAS if r["name"] == "Naidhana")
    assert naidhana["offset"] == 7
    assert tara_of_count(7)["name"] == "Naidhana/Vadha Tara"
    assert special_nakshatra("Naidhana", 5.0)["tara"] == "Naidhana/Vadha Tara"

    # and it is the only name the two classifications share besides Janma
    special = {str(r["name"]) for r in SPECIAL_NAKSHATRAS}
    taras = {str(r["name"]).split()[0].split("/")[0] for r in TABLE_64_TARAS}
    assert special & taras == {"Janma", "Naidhana"}


def test_the_exercise_says_the_transit_names_a_possibility_not_a_person():
    from hora.transits.tara import (
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE,
        THE_TRANSIT_NAMES_A_POSSIBILITY_NOT_A_PERSON,
    )

    assert "Not everyone" in THE_TRANSIT_NAMES_A_POSSIBILITY_NOT_A_PERSON
    assert "a possibility during the transit" in (
        THE_TRANSIT_NAMES_A_POSSIBILITY_NOT_A_PERSON)
    assert "almost the same number of people" in (
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE)


def test_footnote_72_bounds_the_whole_nakshatra_family():
    """"These transit principles based on nakshtra give good insight into
    future, but one cannot make predictions just based on them."
    """
    from hora.transits.tara import (
        FOOTNOTE_72,
        NAKSHTRA_IS_A_SLIP_FOR_NAKSHATRA,
    )

    assert "cannot make predictions just based on them" in FOOTNOTE_72
    assert "good insight into future" in FOOTNOTE_72
    assert "nakshtra" in FOOTNOTE_72 and "nakshatra" not in FOOTNOTE_72
    assert "spelt correctly everywhere else" in NAKSHTRA_IS_A_SLIP_FOR_NAKSHATRA


def test_the_two_footnotes_do_different_work():
    """72 bounds every nakshatra transit principle; 74 narrows to death and
    names the corroboration it needs.
    """
    from hora.transits.tara import (
        FOOTNOTE_72,
        FOOTNOTE_74,
        THE_TWO_FOOTNOTES_SCOPE_AND_THEN_SHARPEN,
    )

    assert "death" not in FOOTNOTE_72
    assert "death" in FOOTNOTE_74
    assert "dasas and Tajaka charts" in FOOTNOTE_74
    assert "dasas" not in FOOTNOTE_72
    assert "The first bounds the family" in THE_TWO_FOOTNOTES_SCOPE_AND_THEN_SHARPEN


def test_every_technique_in_chapter_26_carries_a_limit_but_26_5():
    """Each section either states a limit on itself or is a limit on a
    chapter 25 verdict. §26.5 is the one that states none of its own.
    """
    from hora.charts.aspects import NAKSHATRA_DRISHTI_RESULTS
    from hora.transits.murthi import (
        THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE,
    )
    from hora.transits.tara import (
        EVERY_TECHNIQUE_IN_CHAPTER_26_IS_HEDGED,
        FOOTNOTE_72,
        FOOTNOTE_74,
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE,
        TARA_RULE,
    )
    from hora.transits.vedha import VEDHA_AND_MURTHI_ARE_BOTH_BRAKES, VEDHA_RULE

    assert "may not give his full results" in (
        THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE)
    assert "cannot give its good results" in VEDHA_RULE
    assert "marginal results" in VEDHA_AND_MURTHI_ARE_BOTH_BRAKES
    assert "cannot give its full results" in TARA_RULE
    assert "with respect to the native" in RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE
    assert "cannot make predictions" in FOOTNOTE_72
    assert "very hasty" in FOOTNOTE_74

    # §26.5 states a reading and no limit of its own
    assert "good results" in NAKSHATRA_DRISHTI_RESULTS
    for hedge in ("cannot", "not enough", "hasty", "only", "just"):
        assert hedge not in NAKSHATRA_DRISHTI_RESULTS
    assert "modify a verdict rather than making one" in (
        EVERY_TECHNIQUE_IN_CHAPTER_26_IS_HEDGED)


def test_jfk_jrs_death_is_now_read_through_two_mechanisms():
    from hora.charts.book import chart
    from hora.transits.tara import JFK_JRS_DEATH_IS_READ_TWICE

    assert chart(56)["transit"]["for"] == "his death"
    assert chart(56)["transit"]["date"].startswith("July 16, 1999")
    assert "Example 107" in chart(56)["title"]
    assert "transit D-11" in JFK_JRS_DEATH_IS_READ_TWICE


# --------------------------------------------------------------------------
# Exercise 43 — Chart 63's native, and the two layers separated
# --------------------------------------------------------------------------

def test_every_claim_in_exercise_43_holds_against_chart_63():
    from hora.charts.book import longitudes
    from hora.charts.house import house_of_rasi
    from hora.core.const import DEBILITATION_RASI, NAKSHATRA_NAMES, Graha
    from hora.transits.gochara import good_houses
    from hora.transits.tara import (
        EXERCISE_43_CLAIMS,
        NAKSHATRA_SPAN,
        nakshatra_of,
        special_nakshatra,
    )

    natal = longitudes(63)
    moon, lagna = natal["Moon"], int(natal["Asc"] // 30)

    index = nakshatra_of(moon)
    assert str(NAKSHATRA_NAMES[index]) == "Purva Bhadrapada"
    assert int((moon % NAKSHATRA_SPAN) // (NAKSHATRA_SPAN / 4)) + 1 == 3
    assert A[lagna] == "Vi"

    assert house_of_rasi(int(moon // 30), R["Cn"]) == 6
    assert house_of_rasi(lagna, R["Cn"]) == 11
    assert {6, 11} <= set(good_houses(int(Graha.MARS)))

    ashlesha = [str(n) for n in NAKSHATRA_NAMES].index("Ashlesha")
    assert (ashlesha - index) % 27 + 1 == 12
    assert special_nakshatra("Desa", moon)["nakshatra"] == "Ashlesha"
    assert DEBILITATION_RASI[int(Graha.MARS)] == R["Cn"]

    assert len(EXERCISE_43_CLAIMS) == 8


def test_mars_is_in_ashlesha_across_the_second_week_of_november_1994():
    import datetime

    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import NAKSHATRA_NAMES, Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.tara import (
        MARS_IS_IN_ASHLESHA_FOR_A_MONTH_AROUND_THE_EVENT,
        nakshatra_of,
    )

    place = Place(name="Machilipatnam", **chart(63)["place"])
    settings = Settings(node_type=NodeType.MEAN)
    ashlesha = [str(n) for n in NAKSHATRA_NAMES].index("Ashlesha")

    def where(date):
        computed = compute_chart(
            from_local(date.year, date.month, date.day, 12, 0, 0.0,
                       utc_offset_hours=5.5), place, settings)
        return nakshatra_of(computed.positions[int(Graha.MARS)].longitude)

    for day in range(8, 15):                      # the second week
        assert where(datetime.date(1994, 11, day)) == ashlesha, day
    assert where(datetime.date(1994, 10, 23)) != ashlesha
    assert where(datetime.date(1994, 11, 24)) != ashlesha
    assert "24 October 1994" in (
        MARS_IS_IN_ASHLESHA_FOR_A_MONTH_AROUND_THE_EVENT)


def test_the_house_gives_the_valence_and_the_nakshatra_the_subject():
    """The exercise states the gains up front and asks only for their nature,
    which is the two layers separated as plainly as the book ever does.
    """
    from hora.transits.tara import (
        EXERCISE_43,
        THE_HOUSE_GIVES_THE_VALENCE_AND_THE_NAKSHATRA_THE_SUBJECT,
    )

    assert "brought material gains" in EXERCISE_43
    assert "guess the nature of the gains" in EXERCISE_43
    assert "Neither layer decides the other" in (
        THE_HOUSE_GIVES_THE_VALENCE_AND_THE_NAKSHATRA_THE_SUBJECT)


def test_one_debilitated_malefic_does_what_the_section_asked_many_to_do():
    from hora.transits.tara import (
        A_DEBILITATED_MALEFIC_COUNTS_FOR_MANY,
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE,
    )

    assert "many malefics are transiting in desa nakshatra" in (
        RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE)
    assert "with a single Mars" in A_DEBILITATED_MALEFIC_COUNTS_FOR_MANY


def test_a_debilitated_graha_can_still_have_a_favourable_transit():
    from hora.core.const import DEBILITATION_RASI, Graha
    from hora.transits.gochara import good_houses, transit_result
    from hora.transits.tara import (
        DEBILITATION_DOES_NOT_MAKE_THE_TRANSIT_UNFAVOURABLE,
    )

    assert DEBILITATION_RASI[int(Graha.MARS)] == R["Cn"]
    for house in (6, 11):
        assert house in good_houses(int(Graha.MARS))
        assert transit_result(int(Graha.MARS), house)["snapshot"] == "Good"
    assert "only to sharpen what it does" in (
        DEBILITATION_DOES_NOT_MAKE_THE_TRANSIT_UNFAVOURABLE)


def test_chart_63s_native_is_recorded_as_leaving_india_twice():
    from hora.charts.book import chart
    from hora.transits.tara import CHART_63S_NATIVE_LEAVES_INDIA_TWICE

    events = chart(63)["events"]
    assert len(events) == 2
    assert events["he left India and landed in the USA"] == "August 16, 1991"
    assert "November 1994" in events["he left his motherland India again"]
    assert "three years apart" in CHART_63S_NATIVE_LEAVES_INDIA_TWICE


# --------------------------------------------------------------------------
# Exercise 44 — §26.5's aspects doing work, and two footnotes
# --------------------------------------------------------------------------

def test_mars_in_swati_aspects_the_five_the_answer_names():
    from hora.charts.aspects import nakshatra_aspects
    from hora.core.const import NAKSHATRA_NAMES, Graha
    from hora.transits.tara import EXERCISE_44_ASPECTED

    names = [str(n) for n in NAKSHATRA_NAMES]
    aspected = nakshatra_aspects(int(Graha.MARS), names.index("Swati"))
    assert sorted(names[n] for n in aspected) == sorted(
        nakshatra for nakshatra, _count in EXERCISE_44_ASPECTED)
    assert len(EXERCISE_44_ASPECTED) == 5


def test_the_counts_from_a_dhanishtha_janma_nakshatra_are_as_printed():
    from hora.charts.book import longitudes
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.tara import (
        EXERCISE_44_ASPECTED,
        NAKSHATRA_SPAN,
        nakshatra_of,
        tara,
    )

    moon = longitudes(56)["Moon"]
    assert str(NAKSHATRA_NAMES[nakshatra_of(moon)]) == "Dhanishta"
    names = [str(n) for n in NAKSHATRA_NAMES]
    for nakshatra, count in EXERCISE_44_ASPECTED:
        position = names.index(nakshatra) * NAKSHATRA_SPAN + 1.0
        assert tara(moon, position)["count"] == count, nakshatra
    assert [count for _n, count in EXERCISE_44_ASPECTED] == [
        20, 22, 26, 27, 7]


def test_exactly_two_of_the_five_are_special_nakshatras():
    from hora.transits.tara import EXERCISE_44_ASPECTED, SPECIAL_NAKSHATRAS

    offsets = {int(row["offset"]): str(row["name"])
               for row in SPECIAL_NAKSHATRAS}
    special = {nakshatra: offsets[count]
               for nakshatra, count in EXERCISE_44_ASPECTED
               if count in offsets}
    assert special == {"Bharani": "Naidhana", "Anuradha": "Vainaasika"}
    assert len(special) == 2


def test_mars_and_saturn_are_the_two_that_reach_both_special_nakshatras():
    """Bharani is the 15th from Swati, which every graha aspects. Anuradha is
    the 3rd, and only Mars and Saturn have a 3rd in their lists.
    """
    from hora.charts.aspects import NAKSHATRA_DRISHTI, nakshatra_aspects
    from hora.charts.book import longitudes
    from hora.core.const import NAKSHATRA_NAMES, Graha
    from hora.transits.tara import (
        ONLY_MARS_AND_SATURN_REACH_BOTH_SPECIAL_NAKSHATRAS,
        SPECIAL_NAKSHATRAS,
        nakshatra_of,
    )

    janma = nakshatra_of(longitudes(56)["Moon"])
    offsets = {int(row["offset"]) for row in SPECIAL_NAKSHATRAS}
    swati = [str(n) for n in NAKSHATRA_NAMES].index("Swati")

    def specials_reached(graha):
        return {n for n in nakshatra_aspects(graha, swati)
                if (n - janma) % 27 + 1 in offsets}

    both = {g for g in NAKSHATRA_DRISHTI if len(specials_reached(g)) == 2}
    assert both == {int(Graha.MARS), int(Graha.SATURN)}
    # everyone else still reaches the naidhana nakshatra, via the 15th
    for graha in NAKSHATRA_DRISHTI:
        assert len(specials_reached(graha)) >= 1, graha
    assert {g for g in NAKSHATRA_DRISHTI if 3 in NAKSHATRA_DRISHTI[g]} == both
    assert "Mars and Saturn are the only two" in (
        ONLY_MARS_AND_SATURN_REACH_BOTH_SPECIAL_NAKSHATRAS)


def test_occupation_and_aspect_are_read_together_here():
    """§26.4.2 grades a graha situated in a special nakshatra; §26.5 grades
    what a graha aspects. Exercise 44 uses both on one moment.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.tara import (
        OCCUPATION_AND_ASPECT_ARE_COMBINED_HERE,
        SPECIAL_NAKSHATRA_RULE,
        nakshatra_of,
        special_nakshatra,
        special_transits,
    )

    moon = longitudes(56)["Moon"]
    block = chart(56)["transit"]
    computed = compute_chart(from_local(**block["birth_data"]),
                             Place(name="Martha's Vineyard", **block["place"]),
                             Settings(node_type=NodeType.MEAN))

    # Saturn occupies the naidhana nakshatra
    occupied = special_transits(
        moon, {int(Graha.SATURN): computed.positions[
            int(Graha.SATURN)].longitude})
    assert occupied["in_special_nakshatras"] == [
        {"graha": "Saturn", "nakshatra": "Bharani", "special": "Naidhana",
         "shows": "death and suffering"}]

    # and Mars aspects it, from wherever he actually was
    mars = nakshatra_of(computed.positions[int(Graha.MARS)].longitude)
    assert isinstance(mars, int)
    assert special_nakshatra("Naidhana", moon)["nakshatra"] == "Bharani"

    assert "situated in these constellations" in SPECIAL_NAKSHATRA_RULE
    assert "treats the two as adding up" in (
        OCCUPATION_AND_ASPECT_ARE_COMBINED_HERE)


def test_footnote_73_uses_a_mrityu_bhaga_the_book_has_not_defined():
    """The claim needs a degree per graha per rasi and no section supplied
    prints one. Chart 56's Mars is at 25 Ge 12 — the datum to test against
    when a table arrives. OI-144.
    """
    from hora.charts.book import longitudes
    from hora.core.timeutil import format_dms
    from hora.transits.tara import (
        FOOTNOTE_73,
        MRITYU_BHAGA_IS_USED_WITHOUT_A_DEFINITION,
    )

    mars = longitudes(56)["Mars"]
    assert A[int(mars // 30)] == "Ge"
    assert format_dms(mars % 30, seconds=False) == "25-12"
    assert "Mritya Bhaga" in FOOTNOTE_73
    assert "not checked" in MRITYU_BHAGA_IS_USED_WITHOUT_A_DEFINITION

    # nothing in the codebase computes one
    import hora.transits.tara as module

    assert not any("bhaga" in name.lower() and callable(getattr(module, name))
                   for name in dir(module))


def test_footnote_74_makes_the_technique_insufficient_on_its_own():
    from hora.transits.tara import (
        FOOTNOTE_74,
        THE_TECHNIQUE_NEEDS_DASAS_AND_TAJAKA_TO_BE_USED_AT_ALL,
        THE_TRANSIT_NAMES_A_POSSIBILITY_NOT_A_PERSON,
    )

    assert "very hasty" in FOOTNOTE_74
    assert "dasas and Tajaka charts" in FOOTNOTE_74
    assert "only those people" in FOOTNOTE_74
    # Exercise 42 gestured at this; footnote 74 names what is required
    assert "Not everyone" in THE_TRANSIT_NAMES_A_POSSIBILITY_NOT_A_PERSON
    assert "never sufficient on its own" in (
        THE_TECHNIQUE_NEEDS_DASAS_AND_TAJAKA_TO_BE_USED_AT_ALL)


def test_exercise_44_claims_are_all_listed():
    from hora.transits.tara import EXERCISE_44_CLAIMS, EXERCISE_44_FINAL

    assert len(EXERCISE_44_CLAIMS) == 6
    assert "Mr. Kennedy passed away" in EXERCISE_44_FINAL


# --------------------------------------------------------------------------
# §26.6 — constellations and body parts, opened
# --------------------------------------------------------------------------

def test_26_6_counts_from_janma_nakshatra_like_the_rest_of_26_4():
    from hora.transits.tara import BODY_PART_RULE, TARA_COUNTING_RULE

    assert "as counted from janma nakshatra" in BODY_PART_RULE
    assert "Table 65 - Table 69" in BODY_PART_RULE
    assert "constellation of natal Moon" in TARA_COUNTING_RULE


def test_the_second_purpose_is_the_only_inverse_reading_in_part_3():
    from hora.transits.tara import (
        BODY_PART_PURPOSES,
        THE_SECOND_PURPOSE_READS_THE_TABLES_BACKWARDS,
    )

    forward, inverse = BODY_PART_PURPOSES
    assert "standard results for planetary transits" in forward
    assert "figure out the planet causing it" in inverse
    assert "remedial measures" in inverse
    assert "preventive measures before the transit" in inverse
    assert "a shortlist and not a name" in (
        THE_SECOND_PURPOSE_READS_THE_TABLES_BACKWARDS)


def test_five_tables_cover_nine_bodies_including_the_nodes():
    from hora.transits.tara import (
        BODY_PART_TABLES,
        FIVE_TABLES_COVER_NINE_BODIES_INCLUDING_THE_NODES,
    )

    assert sorted(BODY_PART_TABLES) == [65, 66, 67, 68, 69]
    covered = [g for table in BODY_PART_TABLES.values() if table is not None
               for g in table["grahas"]]
    assert covered == ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                       "Saturn", "Rahu", "Ketu"]
    assert len(covered) == len(set(covered)) == 9
    assert [len(t["grahas"]) for t in BODY_PART_TABLES.values()] == [
        1, 1, 1, 3, 3]
    assert "nine bodies" in (
        FIVE_TABLES_COVER_NINE_BODIES_INCLUDING_THE_NODES)


def test_section_26_6_is_not_finished_early():
    """The coverage line for §26.6. It fails while any of Tables 65 to 69 is
    still pending, so the section cannot be reported complete before its
    pages arrive — the same guard chapter 25 used for Tables 53 to 59.
    """
    from hora.transits.gochara import STANDARD_RESULT_TABLES
    from hora.transits.tara import BODY_PART_TABLES, BODY_PART_TABLES_PENDING

    built = {n for n, table in BODY_PART_TABLES.items() if table is not None}
    pending = set(BODY_PART_TABLES_PENDING)
    assert built | pending == set(BODY_PART_TABLES)
    assert not (built & pending)

    # chapter 25's registry is the precedent, and it is complete
    assert tuple(STANDARD_RESULT_TABLES) == (53, 54, 55, 56, 57, 58, 59)
    assert all(STANDARD_RESULT_TABLES.values())

    assert pending == set(), (
        f"Tables {sorted(pending)} of section 26.6 are still pending; "
        f"update this assertion as each is supplied")
    assert built == {65, 66, 67, 68, 69}


# --------------------------------------------------------------------------
# Table 65 — the Sun's body parts
# --------------------------------------------------------------------------

def test_table_65_partitions_the_27_into_contiguous_blocks():
    from hora.transits.tara import (
        THE_BODY_PART_TABLE_IS_BLOCKS_NOT_A_CYCLE,
        body_part_table,
    )

    table = body_part_table(65)
    assert table["grahas"] == ("Sun",)
    rows = table["rows"]
    assert len(rows) == 8

    counts = [c for row in rows for c in row["counts"]]
    assert sorted(counts) == list(range(1, 28))
    for row in rows:
        block = list(row["counts"])
        assert block == list(range(block[0], block[-1] + 1)), row["part"]
    assert [len(row["counts"]) for row in rows] == [1, 4, 4, 4, 6, 4, 2, 2]

    assert len({row["part"] for row in rows}) == 8
    assert len({row["result"] for row in rows}) == 8
    assert "No modulus reproduces that" in (
        THE_BODY_PART_TABLE_IS_BLOCKS_NOT_A_CYCLE)


def test_table_65s_rows_are_as_printed():
    from hora.transits.tara import body_part_table

    assert tuple((row["counts"], row["part"], row["result"])
                 for row in body_part_table(65)["rows"]) == (
        ((1,), "Mouth/Face", "Destruction"),
        ((2, 3, 4, 5), "Head", "Influx of wealth"),
        ((6, 7, 8, 9), "Chest", "Victory"),
        ((10, 11, 12, 13), "Right hand", "Wealth"),
        ((14, 15, 16, 17, 18, 19), "Two feet", "Poverty"),
        ((20, 21, 22, 23), "Left hand", "Physical ailments"),
        ((24, 25), "Eyes", "Gains"),
        ((26, 27), "Private parts", "Death"),
    )


def test_table_65_and_table_64_agree_no_better_than_chance():
    """Of the 24 counts Table 64 grades — Janma's three are mixed — twelve
    agree with Table 65's plain sense and twelve contradict it.
    """
    from hora.transits.tara import (
        BODY_PART_HARMS,
        THE_TWO_TABLES_AGREE_NO_BETTER_THAN_CHANCE,
        body_part_table,
        tara_of_count,
    )

    agree = disagree = mixed = 0
    for row in body_part_table(65)["rows"]:
        harm = row["result"] in BODY_PART_HARMS
        for count in row["counts"]:
            graded = tara_of_count(count)["good"]
            if graded is None:
                mixed += 1
            elif graded is not harm:
                agree += 1
            else:
                disagree += 1
    assert (agree, disagree, mixed) == (12, 12, 3)
    assert agree + disagree + mixed == 27
    assert "the 7th is Naidhana and gives Victory" in (
        THE_TWO_TABLES_AGREE_NO_BETTER_THAN_CHANCE)


def test_the_friendliest_taras_are_the_deadliest_body_parts():
    from hora.transits.tara import body_part_table, tara_of_count

    death = next(row for row in body_part_table(65)["rows"]
                 if row["result"] == "Death")
    assert death["counts"] == (26, 27)
    assert tara_of_count(26)["name"] == "Mitra Tara"
    assert tara_of_count(27)["name"] == "Parama Mitra Tara"
    assert tara_of_count(26)["good"] is tara_of_count(27)["good"] is True

    victory = next(row for row in body_part_table(65)["rows"]
                   if row["result"] == "Victory")
    assert 7 in victory["counts"]
    assert tara_of_count(7)["name"] == "Naidhana/Vadha Tara"
    assert tara_of_count(7)["good"] is False


def test_the_first_count_is_graded_three_different_ways():
    from hora.transits.tara import (
        THE_FIRST_COUNT_IS_GRADED_THREE_WAYS,
        body_part_table,
        special_nakshatra,
        tara_of_count,
    )

    first = next(row for row in body_part_table(65)["rows"]
                 if 1 in row["counts"])
    assert first["counts"] == (1,)
    assert (first["part"], first["result"]) == ("Mouth/Face", "Destruction")
    assert tara_of_count(1)["grade"] == "mixed"
    assert special_nakshatra("Janma", 5.0)["shows"] == "general well-being"
    assert "Destruction in Table 65" in THE_FIRST_COUNT_IS_GRADED_THREE_WAYS
    assert "Janma Tara and mixed" in THE_FIRST_COUNT_IS_GRADED_THREE_WAYS


def test_body_part_reads_a_transit_and_marks_its_own_grading_as_ours():
    from hora.transits.tara import NAKSHATRA_SPAN, body_part

    natal = 10 * NAKSHATRA_SPAN + 2.0
    got = body_part("Sun", natal, (10 + 6) % 27 * NAKSHATRA_SPAN + 2.0)
    assert got["count"] == 7
    assert (got["part"], got["result"]) == ("Chest", "Victory")
    assert got["harm"] is False
    assert got["table"] == 65
    assert "not the book's grading" in got["harm_is_ours"]
    assert got["tara"] == "Naidhana/Vadha Tara"


def test_a_body_not_covered_by_the_section_is_refused():
    from hora.transits.tara import TaraError, body_part, body_part_table

    with pytest.raises(TaraError, match="no supplied table"):
        body_part("Gulika", 5.0, 100.0)
    for number in (65, 66, 67, 68, 69):
        assert body_part_table(number)["rows"]


def test_the_reverse_lookup_says_how_much_of_the_section_it_has():
    from hora.transits.tara import grahas_dwelling_in

    got = grahas_dwelling_in("Eyes")
    assert got["grahas"] == [
        {"grahas": ["Sun"], "table": 65, "counts": (24, 25),
         "result": "Gains"},
        {"grahas": ["Moon"], "table": 66, "counts": (9, 10),
         "result": "Money"},
        {"grahas": ["Mars"], "table": 67, "counts": (26, 27),
         "result": "Going abroad"},
        {"grahas": ["Saturn", "Rahu", "Ketu"], "table": 69,
         "counts": (24, 25), "result": "Comforts"}]
    assert got["tables_supplied"] == [65, 66, 67, 68, 69]
    assert got["tables_pending"] == []
    assert got["complete"] is True

    assert grahas_dwelling_in("Left knee")["grahas"] == []


# --------------------------------------------------------------------------
# Table 66 — the Moon's body parts
# --------------------------------------------------------------------------

def test_table_66s_rows_are_as_printed_across_the_page_break():
    from hora.transits.tara import body_part_table

    table = body_part_table(66)
    assert table["grahas"] == ("Moon",)
    assert tuple((row["counts"], row["part"], row["result"])
                 for row in table["rows"]) == (
        ((1, 2), "Face", "Great fear"),
        ((3, 4, 5, 6), "Head", "Well-being"),
        ((7, 8), "Back", "Victory over enemies"),
        ((9, 10), "Eyes", "Money"),
        ((11, 12, 13, 14, 15), "Heart", "Comforts and peace"),
        ((16, 17, 18), "Left hand", "Quarrels"),
        ((19, 20, 21, 22, 23, 24), "Two feet", "Going abroad"),
        ((25, 26, 27), "Right hand", "Financial gains"),
    )


def test_table_66_partitions_the_27_in_blocks_of_its_own():
    from hora.transits.tara import body_part_table

    for number, sizes in ((65, [1, 4, 4, 4, 6, 4, 2, 2]),
                          (66, [2, 4, 2, 2, 5, 3, 6, 3])):
        rows = body_part_table(number)["rows"]
        counts = [c for row in rows for c in row["counts"]]
        assert sorted(counts) == list(range(1, 28)), number
        for row in rows:
            block = list(row["counts"])
            assert block == list(range(block[0], block[-1] + 1))
        assert [len(row["counts"]) for row in rows] == sizes
        assert len({row["part"] for row in rows}) == 8
        assert len({row["result"] for row in rows}) == 8


def test_each_table_draws_eight_parts_from_a_larger_pool():
    from hora.transits.tara import (
        BODY_PART_TABLES,
        THE_TABLES_DRAW_EIGHT_PARTS_FROM_A_LARGER_POOL,
        body_part_table,
    )

    supplied = [n for n, t in BODY_PART_TABLES.items() if t is not None]
    named = {n: {row["part"] for row in body_part_table(n)["rows"]}
             for n in supplied}
    assert {n: len(parts) for n, parts in named.items()} == {
        65: 8, 66: 8, 67: 8, 68: 6, 69: 9}

    everywhere = set.intersection(*named.values())
    assert everywhere == {"Head"}
    pool = set.union(*named.values())
    assert len(pool) == 15
    assert {"Two hands", "Stomach", "Right leg", "Left leg"} <= pool
    assert "Each table names exactly eight" in (
        THE_TABLES_DRAW_EIGHT_PARTS_FROM_A_LARGER_POOL)


def test_mouth_face_and_face_are_two_different_parts():
    """Reading Tables 65 and 66 alone they looked like one part under two
    names. Table 67 gives Mars both, with different counts and results.
    """
    from hora.transits.tara import (
        MOUTH_FACE_AND_FACE_ARE_DIFFERENT_PARTS,
        body_part_table,
    )

    rows = body_part_table(67)["rows"]
    mouth = next(r for r in rows if r["part"] == "Mouth/Face")
    face = next(r for r in rows if r["part"] == "Face")
    assert (mouth["counts"], mouth["result"]) == ((1, 2), "Death")
    assert (face["counts"], face["result"]) == ((18, 19, 20, 21),
                                                "Great fear")
    assert not set(mouth["counts"]) & set(face["counts"])
    assert "not two spellings of one part" in (
        MOUTH_FACE_AND_FACE_ARE_DIFFERENT_PARTS)


def test_the_reverse_lookup_reports_parts_whose_names_overlap():
    """Searching "Face" must not silently miss the Sun's "Mouth/Face"."""
    from hora.transits.tara import grahas_dwelling_in

    got = grahas_dwelling_in("Face")
    assert [entry["grahas"] for entry in got["grahas"]] == [
        ["Moon"], ["Mars"], ["Mercury", "Jupiter", "Venus"],
        ["Saturn", "Rahu", "Ketu"]]
    assert [entry["part"] for entry in got["similar_parts"]] == [
        "Mouth/Face", "Mouth/Face"]

    # "Two hands" must be reachable from "Left hand" — a plural apart
    hands = grahas_dwelling_in("Left hand")
    assert [entry["grahas"] for entry in hands["grahas"]] == [
        ["Sun"], ["Moon"], ["Mars"], ["Saturn", "Rahu", "Ketu"]]
    assert {entry["part"] for entry in hands["similar_parts"]} == {
        "Right hand", "Two hands"}

    # and "Two feet" must not be reachable from "Two hands"
    feet = grahas_dwelling_in("Two feet")
    assert all(entry["part"] != "Two hands"
               for entry in feet["similar_parts"])


def test_going_abroad_is_left_ungraded():
    """The first result that is an event rather than a verdict. Exercise 43
    read one native's departure as the gain a good transit gave.
    """
    from hora.transits.tara import (
        BODY_PART_NEUTRAL,
        NAKSHATRA_SPAN,
        NOT_EVERY_STANDARD_RESULT_IS_A_VERDICT,
        body_part,
        body_part_table,
    )

    assert BODY_PART_NEUTRAL == {"Going abroad", "Travels"}
    row = next(r for r in body_part_table(66)["rows"]
               if r["result"] == "Going abroad")
    assert row["counts"] == (19, 20, 21, 22, 23, 24)

    natal = 0.5
    got = body_part("Moon", natal, 19 * NAKSHATRA_SPAN + 1.0)
    assert got["count"] == 20
    assert got["result"] == "Going abroad"
    assert got["harm"] is None
    assert "None for a result that is an event" in got["harm_is_ours"]
    assert "welcome or not depending on the native" in (
        NOT_EVERY_STANDARD_RESULT_IS_A_VERDICT)


def test_every_other_result_so_far_is_graded_one_way_or_the_other():
    from hora.transits.tara import (
        BODY_PART_HARMS,
        BODY_PART_NEUTRAL,
        body_part_table,
    )

    graded = harms = 0
    for number in (65, 66):
        for row in body_part_table(number)["rows"]:
            result = str(row["result"])
            if result in BODY_PART_NEUTRAL:
                continue
            graded += 1
            harms += result in BODY_PART_HARMS
    assert graded == 15                      # 16 rows, one neutral
    assert harms == 6
    assert not (BODY_PART_HARMS & BODY_PART_NEUTRAL)


def test_table_66_also_disagrees_with_table_64():
    from hora.transits.tara import (
        BODY_PART_HARMS,
        BODY_PART_NEUTRAL,
        body_part_table,
        tara_of_count,
    )

    agree = disagree = mixed = neutral = 0
    for row in body_part_table(66)["rows"]:
        result = str(row["result"])
        if result in BODY_PART_NEUTRAL:
            neutral += len(row["counts"])
            continue
        harm = result in BODY_PART_HARMS
        for count in row["counts"]:
            graded = tara_of_count(count)["good"]
            if graded is None:
                mixed += 1
            elif graded is not harm:
                agree += 1
            else:
                disagree += 1
    assert (agree, disagree, mixed, neutral) == (10, 9, 2, 6)
    assert agree + disagree + mixed + neutral == 27


def test_only_the_head_appears_in_every_table():
    """Two feet looked like a fixture until Table 69, which has no such part
    at all — it splits the legs instead.
    """
    from hora.transits.tara import (
        BODY_PART_TABLES,
        ONLY_THE_HEAD_APPEARS_IN_EVERY_TABLE,
        body_part_table,
    )

    named = {n: {row["part"] for row in body_part_table(n)["rows"]}
             for n in BODY_PART_TABLES}
    assert set.intersection(*named.values()) == {"Head"}

    has_feet = {n for n, parts in named.items() if "Two feet" in parts}
    assert has_feet == {65, 66, 67, 68}
    widths = {n: len(next(r for r in body_part_table(n)["rows"]
                          if r["part"] == "Two feet")["counts"])
              for n in has_feet}
    assert widths == {65: 6, 66: 6, 67: 6, 68: 8}
    assert "Head is the one part named in all five" in (
        ONLY_THE_HEAD_APPEARS_IN_EVERY_TABLE)


# --------------------------------------------------------------------------
# Table 67 — Mars's body parts
# --------------------------------------------------------------------------

def test_table_67s_rows_are_as_printed():
    from hora.transits.tara import body_part_table

    table = body_part_table(67)
    assert table["grahas"] == ("Mars",)
    assert tuple((row["counts"], row["part"], row["result"])
                 for row in table["rows"]) == (
        ((1, 2), "Mouth/Face", "Death"),
        ((3, 4, 5, 6, 7, 8), "Two feet", "Separation"),
        ((9, 10, 11), "Chest", "Victory"),
        ((12, 13, 14, 15), "Left hand", "Poverty"),
        ((16, 17), "Head", "Gains"),
        ((18, 19, 20, 21), "Face", "Great fear"),
        ((22, 23, 24, 25), "Right hand", "Well-being"),
        ((26, 27), "Eyes", "Going abroad"),
    )


def test_every_supplied_table_partitions_the_27_in_blocks_of_its_own():
    from hora.transits.tara import BODY_PART_TABLES, body_part_table

    sizes = {}
    for number, table in BODY_PART_TABLES.items():
        if table is None:
            continue
        rows = body_part_table(number)["rows"]
        counts = [c for row in rows for c in row["counts"]]
        assert sorted(counts) == list(range(1, 28)), number
        for row in rows:
            block = list(row["counts"])
            assert block == list(range(block[0], block[-1] + 1))
        sizes[number] = [len(row["counts"]) for row in rows]

    assert sizes == {65: [1, 4, 4, 4, 6, 4, 2, 2],
                     66: [2, 4, 2, 2, 5, 3, 6, 3],
                     67: [2, 6, 3, 4, 2, 4, 4, 2],
                     68: [3, 3, 6, 5, 2, 8],
                     69: [1, 4, 3, 3, 4, 5, 3, 2, 2]}
    assert len({tuple(v) for v in sizes.values()}) == len(sizes)


def test_separation_joins_the_harms():
    from hora.transits.tara import (
        BODY_PART_HARMS,
        BODY_PART_NEUTRAL,
        body_part_table,
    )

    assert "Separation" in BODY_PART_HARMS
    assert "Going abroad" in BODY_PART_NEUTRAL
    results = {str(row["result"])
               for number in (65, 66, 67)
               for row in body_part_table(number)["rows"]}
    ungraded = results - BODY_PART_HARMS - BODY_PART_NEUTRAL
    assert ungraded == {"Influx of wealth", "Victory", "Wealth", "Gains",
                        "Well-being", "Victory over enemies", "Money",
                        "Comforts and peace", "Financial gains"}


# --------------------------------------------------------------------------
# Table 68 — Mercury, Jupiter and Venus share one table
# --------------------------------------------------------------------------

def test_table_68s_rows_are_as_printed():
    from hora.transits.tara import body_part_table

    table = body_part_table(68)
    assert table["grahas"] == ("Mercury", "Jupiter", "Venus")
    assert tuple((row["counts"], row["part"], row["result"])
                 for row in table["rows"]) == (
        ((1, 2, 3), "Head", "Grief"),
        ((4, 5, 6), "Face", "Gains"),
        ((7, 8, 9, 10, 11, 12), "Two hands", "Misfortune"),
        ((13, 14, 15, 16, 17), "Stomach", "Amassing of wealth"),
        ((18, 19), "Private parts", "Destruction"),
        ((20, 21, 22, 23, 24, 25, 26, 27), "Two feet", "Honor and fame"),
    )


def test_row_count_does_not_track_how_many_grahas_share_a_table():
    """After Table 68 it looked as though it did. Table 69 covers three
    grahas too and has the most rows of any table.
    """
    from hora.transits.tara import (
        BODY_PART_TABLES,
        ROW_COUNT_DOES_NOT_TRACK_HOW_MANY_GRAHAS_SHARE_A_TABLE,
        body_part_table,
    )

    shape = {n: (len(body_part_table(n)["grahas"]),
                 len(body_part_table(n)["rows"]))
             for n in BODY_PART_TABLES}
    assert shape == {65: (1, 8), 66: (1, 8), 67: (1, 8),
                     68: (3, 6), 69: (3, 9)}
    coarsest = min(shape, key=lambda n: shape[n][1])
    finest = max(shape, key=lambda n: shape[n][1])
    assert shape[coarsest][0] == shape[finest][0] == 3

    # Table 68 merges the hands, Table 69 splits the legs
    merged = {row["part"] for row in body_part_table(68)["rows"]}
    split = {row["part"] for row in body_part_table(69)["rows"]}
    assert "Two hands" in merged and "Left hand" not in merged
    assert {"Left leg", "Right leg"} <= split and "Two feet" not in split
    assert "coarsest and the finest" in (
        ROW_COUNT_DOES_NOT_TRACK_HOW_MANY_GRAHAS_SHARE_A_TABLE)


def test_one_table_answers_a_transit_for_each_of_its_three_grahas():
    from hora.transits.tara import NAKSHATRA_SPAN, body_part

    natal = 0.5
    for graha in ("Mercury", "Jupiter", "Venus"):
        got = body_part(graha, natal, 8 * NAKSHATRA_SPAN + 1.0)
        assert got["graha"] == graha
        assert got["table"] == 68
        assert got["table_covers"] == ["Mercury", "Jupiter", "Venus"]
        assert got["count"] == 9
        assert (got["part"], got["result"]) == ("Two hands", "Misfortune")
        assert got["harm"] is True


def test_grief_and_misfortune_join_the_harms():
    from hora.transits.tara import BODY_PART_HARMS, body_part_table

    assert {"Grief", "Misfortune"} <= BODY_PART_HARMS
    results = [str(row["result"]) for row in body_part_table(68)["rows"]]
    assert [r in BODY_PART_HARMS for r in results] == [
        True, False, True, False, True, False]


# --------------------------------------------------------------------------
# Table 69 — Saturn with both nodes, and §26.6 complete
# --------------------------------------------------------------------------

def test_table_69s_rows_are_as_printed_across_the_page_break():
    from hora.transits.tara import body_part_table

    table = body_part_table(69)
    assert table["grahas"] == ("Saturn", "Rahu", "Ketu")
    assert tuple((row["counts"], row["part"], row["result"])
                 for row in table["rows"]) == (
        ((1,), "Face", "Grief"),
        ((2, 3, 4, 5), "Right hand", "Comforts"),
        ((6, 7, 8), "Right leg", "Travels"),
        ((9, 10, 11), "Left leg", "Destruction"),
        ((12, 13, 14, 15), "Left hand", "Gains"),
        ((16, 17, 18, 19, 20), "Stomach", "Pleasures"),
        ((21, 22, 23), "Head", "Comforts"),
        ((24, 25), "Eyes", "Comforts"),
        ((26, 27), "Back", "Death"),
    )


def test_table_69_is_the_only_one_that_repeats_a_result():
    from hora.transits.tara import (
        BODY_PART_TABLES,
        TABLE_69_IS_THE_ONLY_ONE_THAT_REPEATS_A_RESULT,
        body_part_table,
    )

    for number in BODY_PART_TABLES:
        rows = body_part_table(number)["rows"]
        results = [str(row["result"]) for row in rows]
        distinct = len(set(results)) == len(results)
        assert distinct is (number != 69), number

    sixty_nine = [str(row["result"]) for row in body_part_table(69)["rows"]]
    assert sixty_nine.count("Comforts") == 3
    assert [row["part"] for row in body_part_table(69)["rows"]
            if row["result"] == "Comforts"] == ["Right hand", "Head", "Eyes"]
    assert "Comforts is the standard result" in (
        TABLE_69_IS_THE_ONLY_ONE_THAT_REPEATS_A_RESULT)


def test_the_nodes_get_a_body_part_reading_where_26_5_gave_them_no_aspect():
    """§26.5 names seven grahas and refuses the nodes. §26.6 covers all nine.
    """
    from hora.charts.aspects import nakshatra_drishti
    from hora.core.const import Graha
    from hora.transits.tara import NAKSHATRA_SPAN, body_part

    for node in ("Rahu", "Ketu"):
        got = body_part(node, 0.5, 25 * NAKSHATRA_SPAN + 1.0)
        assert got["table"] == 69
        assert got["count"] == 26
        assert (got["part"], got["result"]) == ("Back", "Death")
        assert got["harm"] is True
    for node in (Graha.RAHU, Graha.KETU):
        with pytest.raises(ValueError, match="seven planets only"):
            nakshatra_drishti(int(node))


def test_travels_joins_going_abroad_as_ungraded():
    from hora.transits.tara import (
        BODY_PART_NEUTRAL,
        NAKSHATRA_SPAN,
        body_part,
    )

    assert BODY_PART_NEUTRAL == {"Going abroad", "Travels"}
    got = body_part("Saturn", 0.5, 6 * NAKSHATRA_SPAN + 1.0)
    assert got["count"] == 7
    assert (got["part"], got["result"]) == ("Right leg", "Travels")
    assert got["harm"] is None


def test_section_26_6_is_complete():
    """All five tables supplied, all nine bodies covered, every table a
    contiguous partition of the 27.
    """
    from hora.transits.tara import (
        BODY_PART_TABLES,
        BODY_PART_TABLES_PENDING,
        body_part_table,
    )

    assert BODY_PART_TABLES_PENDING == ()
    assert all(table is not None for table in BODY_PART_TABLES.values())

    covered = [g for table in BODY_PART_TABLES.values()
               for g in table["grahas"]]
    assert len(covered) == len(set(covered)) == 9

    for number in BODY_PART_TABLES:
        rows = body_part_table(number)["rows"]
        counts = [c for row in rows for c in row["counts"]]
        assert sorted(counts) == list(range(1, 28)), number


# --------------------------------------------------------------------------
# §26.6's worked example — the symptom read backwards
# --------------------------------------------------------------------------

def _sun_longitude_at():
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_jd

    place = Place(name="New Delhi", latitude=28 + 36 / 60,
                  longitude=77 + 12 / 60)
    settings = Settings(node_type=NodeType.MEAN)

    def of(graha):
        def at(jd):
            return compute_chart(from_jd(jd), place,
                                 settings).positions[int(graha)].longitude
        return at

    return of, Graha


def test_a_visakha_first_pada_moon_is_a_libra_moon():
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.tara import BODY_PART_WORKED_CASE, NAKSHATRA_SPAN

    index = [str(n) for n in NAKSHATRA_NAMES].index("Vishakha")
    start = index * NAKSHATRA_SPAN
    first_pada_end = start + NAKSHATRA_SPAN / 4
    assert int(start // 30) == int(first_pada_end // 30) == R["Li"]
    assert str(BODY_PART_WORKED_CASE["natal_moon_rasi"]) == "Li"


def test_the_chest_counts_and_their_nakshatras_are_as_the_example_says():
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.tara import BODY_PART_WORKED_CASE, body_part_table

    chest = next(row for row in body_part_table(65)["rows"]
                 if row["part"] == "Chest")
    assert chest["counts"] == (6, 7, 8, 9)
    assert chest["result"] == "Victory"

    names = [str(n) for n in NAKSHATRA_NAMES]
    visakha = names.index("Vishakha")
    got = tuple(names[(visakha + count - 1) % 27] for count in chest["counts"])
    assert got == BODY_PART_WORKED_CASE["nakshatras"]
    assert got == ("Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha")


def test_the_suns_chest_window_is_the_printed_january_to_march_window():
    """The Sun enters Uttaraashaadha late on 11 January and leaves
    Satabhisha on the morning of 4 March, so the window's last full day is
    3 March — which is what §26.6 prints.
    """
    from hora.core.timeutil import from_local, jd_to_local_str
    from hora.panchanga.solver import scan_for_crossing
    from hora.transits.tara import (
        BODY_PART_WORKED_CASE,
        NAKSHATRA_SPAN,
        THE_WINDOW_IS_GIVEN_IN_WHOLE_DAYS,
    )

    of, Graha = _sun_longitude_at()
    sun = of(Graha.SUN)
    window = (from_local(2000, 1, 5, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
              from_local(2000, 3, 10, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)

    entered = scan_for_crossing(sun, 20 * NAKSHATRA_SPAN, *window)
    left = scan_for_crossing(sun, 24 * NAKSHATRA_SPAN, *window)
    assert jd_to_local_str(entered, 5.5).startswith("2000-01-11")
    assert jd_to_local_str(left, 5.5).startswith("2000-03-04")
    assert str(BODY_PART_WORKED_CASE["window"]) == "Jan 11-Mar 3, 2000"
    assert "stops at the last complete one" in THE_WINDOW_IS_GIVEN_IN_WHOLE_DAYS


def test_both_murthis_of_the_example_reproduce():
    """"At the time Sun entered Capricorn ... Moon was in Ar" and "At the
    time Sun entered Aquarius ... Moon was in Ta."
    """
    from hora.core.timeutil import from_local
    from hora.transits.murthi import murthi, rasi_ingress
    from hora.transits.tara import BODY_PART_WORKED_CASE

    of, Graha = _sun_longitude_at()
    natal_moon = R["Li"] * 30.0 + 21.0          # Visakha's 1st pada
    window = (from_local(2000, 1, 1, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
              from_local(2000, 3, 1, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)

    for block in BODY_PART_WORKED_CASE["murthis"]:
        found = rasi_ingress(of(Graha.SUN), R[str(block["rasi"])], *window)
        assert found["found"] is True
        moon = of(Graha.MOON)(found["jd"])
        assert A[int(moon // 30)] == block["moon_then"], block["rasi"]
        got = murthi(natal_moon, moon)
        assert got["house"] == block["house"]
        assert got["murthi"] == block["murthi"]
        assert got["favourable"] is False


def test_the_murthi_overturns_table_65s_standard_result():
    """Table 65 calls the Sun in the chest Victory; the native had chest
    pain. The murthi is what turns it.
    """
    from hora.transits.murthi import (
        THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE,
    )
    from hora.transits.tara import (
        BODY_PART_HARMS,
        NAKSHATRA_SPAN,
        THE_MURTHI_OVERTURNS_THE_STANDARD_RESULT,
        body_part,
    )

    natal_moon = R["Li"] * 30.0 + 21.0
    got = body_part("Sun", natal_moon, 20 * NAKSHATRA_SPAN + 1.0)
    assert got["count"] == 6
    assert got["part"] == "Chest"
    assert got["result"] == "Victory"
    assert got["harm"] is False
    assert "Victory" not in BODY_PART_HARMS

    assert "decides how the standard result lands" in (
        THE_MURTHI_OVERTURNS_THE_STANDARD_RESULT)
    assert "may not give his full results" in (
        THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE)


def test_a_body_part_window_is_not_a_murthi_window():
    """The chest window spans four nakshatras and two rasis, so the Sun's
    murthi changes inside it. The example carries both.
    """
    from hora.core.timeutil import from_local, jd_to_local_str
    from hora.transits.murthi import rasi_ingress
    from hora.transits.tara import (
        BODY_PART_WORKED_CASE,
        ONE_DWELLING_CAN_SPAN_TWO_MURTHIS,
    )

    of, Graha = _sun_longitude_at()
    aquarius = rasi_ingress(
        of(Graha.SUN), R["Aq"],
        from_local(2000, 1, 1, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
        from_local(2000, 3, 1, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)
    assert jd_to_local_str(aquarius["jd"], 5.5).startswith("2000-02-13")

    murthis = BODY_PART_WORKED_CASE["murthis"]
    assert len(murthis) == 2
    assert {block["murthi"] for block in murthis} == {"Taamra", "Loha"}
    assert "not a murthi window" in ONE_DWELLING_CAN_SPAN_TWO_MURTHIS


def test_the_other_modifier_path_is_aspect_and_vedha():
    """§26.6's opening sentence brings §26.5 and §26.3 into the body-part
    reading. The worked example takes the murthi path instead.
    """
    from hora.charts.aspects import NAKSHATRA_DRISHTI_RESULTS
    from hora.transits.tara import A_DWELLING_CAN_BE_AFFLICTED_BY_ASPECT_OR_VEDHA
    from hora.transits.vedha import VEDHA_RULE

    assert "natural malefics aspect it or cause vedha on it" in (
        A_DWELLING_CAN_BE_AFFLICTED_BY_ASPECT_OR_VEDHA)
    assert "injuries to the left hand" in (
        A_DWELLING_CAN_BE_AFFLICTED_BY_ASPECT_OR_VEDHA)
    assert "natural malefic" in NAKSHATRA_DRISHTI_RESULTS
    assert "vedha sthana" in VEDHA_RULE


# --------------------------------------------------------------------------
# §26.7 — latta, opened
# --------------------------------------------------------------------------

def test_26_7_states_the_rule_and_names_two_natal_targets():
    from hora.transits.latta import LATTA_MEANS, LATTA_RULE, LATTA_TARGETS

    assert LATTA_MEANS == "kick"
    assert "nakshatra-based planetary kick" in LATTA_RULE
    assert "based on its transit position" in LATTA_RULE
    assert "Moon (or lagna) in natal chart" in LATTA_RULE
    assert LATTA_TARGETS == ("natal Moon", "natal lagna")


def test_latta_is_the_first_of_the_chapter_to_admit_the_lagnas_nakshatra():
    """§26.4's taras, §26.4.2's special nakshatras and §26.6's body parts all
    read from the natal Moon's nakshatra alone.
    """
    from hora.transits.latta import LATTA_TARGETS
    from hora.transits.tara import (
        BODY_PART_RULE,
        SPECIAL_NAKSHATRAS_INTRO,
        TARA_COUNTING_RULE,
    )

    assert "natal lagna" in LATTA_TARGETS
    for earlier in (TARA_COUNTING_RULE, BODY_PART_RULE,
                    SPECIAL_NAKSHATRAS_INTRO):
        assert "lagna" not in earlier.lower()


def test_latta_counts_from_the_transit_where_the_others_count_to_it():
    from hora.transits.latta import (
        LATTA_COUNTS_FROM_THE_TRANSIT_NOT_THE_NATAL_POINT,
    )
    from hora.transits.tara import BODY_PART_RULE, TARA_COUNTING_RULE

    for earlier in (TARA_COUNTING_RULE, BODY_PART_RULE):
        assert "from janma nakshatra" in earlier or (
            "from the constellation of natal Moon" in earlier)
    assert "counted from the transit position" in (
        LATTA_COUNTS_FROM_THE_TRANSIT_NOT_THE_NATAL_POINT)


def test_the_harm_is_the_grahas_natal_signification_not_its_nature():
    from hora.charts.aspects import NAKSHATRA_DRISHTI_RESULTS
    from hora.transits.latta import (
        LATTA_RULE,
        THE_HARM_IS_READ_FROM_THE_NATAL_SIGNIFICATION,
    )

    assert "signification of the planet in natal chart" in LATTA_RULE
    assert "natural benefic" not in LATTA_RULE
    # §26.5 by contrast grades by natural nature
    assert "natural benefic" in NAKSHATRA_DRISHTI_RESULTS
    assert "spoils what that benefic signifies natally" in (
        THE_HARM_IS_READ_FROM_THE_NATAL_SIGNIFICATION)


def test_eight_kicks_are_supplied_and_ketu_has_none():
    """The coverage line for §26.7. It fails the moment a kick appears for a
    graha not declared here, so nothing is guessed.
    """
    from hora.transits.latta import (
        LATTA_GRAHAS_PENDING,
        LATTA_KICKS,
        LattaError,
        latta,
    )

    assert set(LATTA_KICKS) == {"Sun", "Mars", "Jupiter", "Saturn",
                                "Moon", "Mercury", "Venus", "Rahu"}
    assert LATTA_GRAHAS_PENDING == ("Ketu",)
    for graha in LATTA_GRAHAS_PENDING:
        with pytest.raises(LattaError, match="has not given a latta"):
            latta(graha, 100.0)
    assert {kick["direction"] for kick in LATTA_KICKS.values()} == {
        "forward", "backward"}


# --------------------------------------------------------------------------
# Purolatta — the forward kicks
# --------------------------------------------------------------------------

def test_all_four_of_the_sections_own_forward_examples_reproduce():
    """"If Sun is in Mrigasira ... i.e. Visakha", and the three like it."""
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import PUROLATTA_EXAMPLES, latta

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27
    assert len(PUROLATTA_EXAMPLES) == 4
    for graha, standing, kicked in PUROLATTA_EXAMPLES:
        got = latta(graha, names.index(standing) * span + 1.0)
        assert got["from_nakshatra"] == standing, graha
        assert got["kicks"] == kicked, graha
        assert got["direction"] == "forward"
        assert got["kick"] == "purolatta"


def test_the_forward_offsets_are_as_printed_and_are_data():
    from hora.charts.aspects import NAKSHATRA_DRISHTI
    from hora.core.const import Graha
    from hora.transits.latta import (
        PUROLATTA_MEANS,
        PUROLATTA_OFFSETS,
        THE_FORWARD_OFFSETS_ARE_DATA,
    )

    assert PUROLATTA_MEANS == "forward kick"
    assert PUROLATTA_OFFSETS == {"Sun": 12, "Mars": 3, "Jupiter": 6,
                                 "Saturn": 8}
    assert len(set(PUROLATTA_OFFSETS.values())) == 4
    assert 1 not in PUROLATTA_OFFSETS.values()      # never its own nakshatra

    # the only overlap with §26.5's aspect offsets is Mars's 3rd
    shared = {graha: offset for graha, offset in PUROLATTA_OFFSETS.items()
              if offset in NAKSHATRA_DRISHTI[int(getattr(Graha,
                                                         graha.upper()))]}
    assert shared == {"Mars": 3}
    assert "Mars's 3rd appearing in both" in THE_FORWARD_OFFSETS_ARE_DATA


def test_the_direction_alternates_down_the_standard_graha_order():
    """Sun forward, Moon backward, Mars forward, and so on. §26.7 never says
    so; it lists four and then four.
    """
    from hora.transits.latta import (
        LATTA_KICKS,
        THE_DIRECTION_ALTERNATES_DOWN_THE_STANDARD_ORDER,
    )

    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
             "Rahu", "Ketu"]
    for position, graha in enumerate(order, start=1):
        kick = LATTA_KICKS.get(graha)
        if kick is None:
            assert graha == "Ketu"
            continue
        expected = "forward" if position % 2 else "backward"
        assert kick["direction"] == expected, graha
    assert "every backward kick to an even one" in (
        THE_DIRECTION_ALTERNATES_DOWN_THE_STANDARD_ORDER)


def test_a_kick_landing_on_a_natal_point_is_reported_with_both_targets():
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import latta_hits

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27

    # Sun in Mrigasira kicks Visakha
    on_moon = latta_hits("Sun", names.index("Mrigashira") * span + 1.0,
                         names.index("Vishakha") * span + 2.0)
    assert on_moon["hits"] == ["natal Moon"]
    assert on_moon["kicked"] is True
    assert "signification of the planet in natal chart" in on_moon["results"]
    assert on_moon["lagna_not_supplied"] is True
    assert on_moon["natal_lagna_nakshatra"] is None

    on_lagna = latta_hits("Sun", names.index("Mrigashira") * span + 1.0,
                          names.index("Rohini") * span + 2.0,
                          names.index("Vishakha") * span + 3.0)
    assert on_lagna["hits"] == ["natal lagna"]
    assert on_lagna["lagna_not_supplied"] is False

    clear = latta_hits("Sun", names.index("Mrigashira") * span + 1.0,
                       names.index("Rohini") * span + 2.0)
    assert clear["hits"] == []
    assert clear["kicked"] is False
    assert clear["results"] is None


# --------------------------------------------------------------------------
# Prishtha latta — the backward kicks, and §26.7's applications
# --------------------------------------------------------------------------

def test_all_four_backward_examples_reproduce():
    """"If Moon is in Anuradha ... i.e. Dhanishtha", and the three like it."""
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import (
        PRISHTHA_EXAMPLES,
        PRISHTHA_LATTA_MEANS,
        latta,
    )

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27
    assert PRISHTHA_LATTA_MEANS == "backward kick"
    assert len(PRISHTHA_EXAMPLES) == 4
    for graha, standing, kicked in PRISHTHA_EXAMPLES:
        got = latta(graha, names.index(standing) * span + 1.0)
        assert got["from_nakshatra"] == standing, graha
        assert got["kicks"] == kicked, graha
        assert got["direction"] == "backward"
        assert got["kick"] == "prishtha latta"


def test_the_backward_offsets_are_as_printed():
    from hora.transits.latta import PRISHTHA_OFFSETS, PUROLATTA_OFFSETS

    assert PRISHTHA_OFFSETS == {"Moon": 22, "Mercury": 7, "Venus": 5,
                                "Rahu": 9}
    assert not set(PRISHTHA_OFFSETS) & set(PUROLATTA_OFFSETS)
    both = {**PUROLATTA_OFFSETS, **PRISHTHA_OFFSETS}
    assert len(both) == 8
    assert 1 not in both.values()          # never its own nakshatra
    assert max(both.values()) == 22 and min(both.values()) == 3


def test_two_grahas_can_kick_the_same_nakshatra_from_different_places():
    """Mercury from Punarvasu and Venus from Mrigasira both kick Aswini —
    the section's own two examples land on one nakshatra.
    """
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import PRISHTHA_EXAMPLES, latta

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27
    landings = {graha: latta(graha, names.index(standing) * span + 1.0)["kicks"]
                for graha, standing, _ in PRISHTHA_EXAMPLES}
    assert landings["Mercury"] == landings["Venus"] == "Ashwini"


def test_ketu_is_the_one_body_the_section_leaves_out():
    from hora.transits.latta import (
        KETU_IS_THE_ONE_BODY_WITH_NO_LATTA,
        LATTA_KICKS,
        LATTA_RULE,
        LattaError,
        latta,
    )

    assert "Each planet has latta" in LATTA_RULE
    assert "Rahu" in LATTA_KICKS
    assert "Ketu" not in LATTA_KICKS
    with pytest.raises(LattaError, match="has not given a latta"):
        latta("Ketu", 100.0)
    assert "Ketu is given none" in KETU_IS_THE_ONE_BODY_WITH_NO_LATTA


def test_the_watch_list_is_one_rule_illustrated_three_times():
    from hora.transits.latta import (
        JANMA_AND_LAGNA_NAKSHATRA_DEFINED,
        LATTA_GENERAL_RESULT,
        LATTA_WATCH_LIST,
        THE_WATCH_LIST_IS_ONE_RULE_ILLUSTRATED_THRICE,
    )

    assert len(LATTA_WATCH_LIST) == 3
    assert [entry["role"] for entry in LATTA_WATCH_LIST] == [
        "the 6th lord", "the 7th lord",
        "an important planet in the 10th house in natal chart"]
    assert LATTA_WATCH_LIST[0]["threatens"] == (
        "litigation or disease or enemies")
    assert "natal significations" in LATTA_GENERAL_RESULT
    assert "nakshatra occupied by natal Moon" in (
        JANMA_AND_LAGNA_NAKSHATRA_DEFINED)
    assert "nakshatra occupied by natal lagna" in (
        JANMA_AND_LAGNA_NAKSHATRA_DEFINED)
    assert "picked out by its natal role" in (
        THE_WATCH_LIST_IS_ONE_RULE_ILLUSTRATED_THRICE)


def test_latta_is_the_only_transit_section_told_to_be_memorised():
    from hora.transits.latta import (
        LATTA_IS_WORTH_MEMORISING,
        THE_BOOK_RATES_LATTA_HIGHLY,
    )
    from hora.transits.tara import FOOTNOTE_72

    assert "memorize the latta formulas" in LATTA_IS_WORTH_MEMORISING
    assert "no other transit section says of itself" in (
        THE_BOOK_RATES_LATTA_HIGHLY)
    # and it still sits under footnote 72's general warning
    assert "cannot make predictions just based on them" in FOOTNOTE_72


# --------------------------------------------------------------------------
# Example 113 — Table 70, and janma outranking lagna
# --------------------------------------------------------------------------

def test_all_eight_rows_of_table_70_reproduce():
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import TABLE_70_LATTAS, latta

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27
    assert len(TABLE_70_LATTAS) == 8
    for graha, standing, count, direction, kicked in TABLE_70_LATTAS:
        got = latta(graha, names.index(standing) * span + 1.0)
        assert got["offset"] == count, graha
        assert got["direction"] == direction, graha
        assert got["kicks"] == kicked, graha


def test_the_transit_positions_of_table_70_reproduce_for_that_evening():
    """Eight nakshatras on the evening of 5 December 1996, from the
    ephemeris rather than from the table.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import NAKSHATRA_NAMES, Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.transits.latta import TABLE_70_LATTAS, nakshatra_of

    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Mercury": Graha.MERCURY, "Jupiter": Graha.JUPITER,
             "Venus": Graha.VENUS, "Saturn": Graha.SATURN,
             "Rahu": Graha.RAHU}
    computed = compute_chart(
        from_local(1996, 12, 5, 18, 0, 0.0, utc_offset_hours=5.5),
        Place(name="New Delhi", latitude=28 + 36 / 60,
              longitude=77 + 12 / 60),
        Settings(node_type=NodeType.MEAN))

    for graha, standing, _count, _direction, _kicked in TABLE_70_LATTAS:
        index = nakshatra_of(
            computed.positions[int(named[graha])].longitude)
        assert str(NAKSHATRA_NAMES[index]) == standing, graha


def test_two_lattas_land_on_the_lagna_nakshatra_and_one_on_the_janma():
    from hora.transits.latta import TABLE_70_LATTAS

    by_target = {}
    for graha, _standing, _count, _direction, kicked in TABLE_70_LATTAS:
        by_target.setdefault(kicked, []).append(graha)
    assert by_target["Hasta"] == ["Mars", "Mercury"]
    assert by_target["Purva Bhadrapada"] == ["Jupiter"]


def test_the_lordships_the_example_names_hold_for_a_virgo_lagna():
    from hora.core.const import NAKSHATRA_NAMES, RASI_LORD, Graha

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27
    hasta = names.index("Hasta")
    assert int(hasta * span // 30) == int(((hasta + 1) * span - 0.001) // 30)
    assert A[int(hasta * span // 30)] == "Vi"

    virgo = R["Vi"]
    lords = {house: RASI_LORD[(virgo + house - 1) % 12]
             for house in (1, 4, 7, 8)}
    assert lords[1] == int(Graha.MERCURY)      # lagna lord
    assert lords[8] == int(Graha.MARS)         # 8th lord
    assert lords[4] == lords[7] == int(Graha.JUPITER)


def test_janma_nakshatra_outranks_lagna_nakshatra_and_not_by_count():
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import (
        JANMA_NAKSHATRA_OUTRANKS_LAGNA_NAKSHATRA,
        THE_RANKING_IS_BY_TARGET_NOT_BY_COUNT,
        latta_hits,
    )

    names = [str(n) for n in NAKSHATRA_NAMES]
    span = 360.0 / 27
    janma = names.index("Purva Bhadrapada") * span + 1.0
    lagna = names.index("Hasta") * span + 1.0

    jupiter = latta_hits("Jupiter", names.index("Purva Ashadha") * span + 1.0,
                         janma, lagna)
    assert jupiter["hits"] == ["natal Moon"]
    assert jupiter["on_janma_nakshatra"] is True
    assert jupiter["precedence"] == JANMA_NAKSHATRA_OUTRANKS_LAGNA_NAKSHATRA

    for graha, standing in (("Mars", "Purva Phalguni"), ("Mercury", "Mula")):
        got = latta_hits(graha, names.index(standing) * span + 1.0,
                         janma, lagna)
        assert got["hits"] == ["natal lagna"], graha
        assert got["on_janma_nakshatra"] is False

    assert "more important" in JANMA_NAKSHATRA_OUTRANKS_LAGNA_NAKSHATRA
    assert "outweighs two" in THE_RANKING_IS_BY_TARGET_NOT_BY_COUNT


def test_the_readings_matters_come_from_7_2s_own_lists_except_one_word():
    """Vehicle, house and marital life are all in §7.2's 4th and 7th.
    "Accidents" is in the 6th's list and not in the 8th's. OI-55 again.
    """
    from hora.core.const import HOUSE_SIGNIFICATIONS
    from hora.transits.latta import (
        A_GRAHA_CAN_CARRY_TWO_LORDSHIPS_INTO_THE_READING,
        ACCIDENTS_IS_NOT_IN_THE_EIGHTH_HOUSES_PRINTED_LIST,
    )

    fourth = str(HOUSE_SIGNIFICATIONS[4]).lower()
    seventh = str(HOUSE_SIGNIFICATIONS[7]).lower()
    assert "vehicles" in fourth and "house" in fourth
    assert "marital life" in seventh

    assert "accidents" in str(HOUSE_SIGNIFICATIONS[6]).lower()
    assert "accidents" not in str(HOUSE_SIGNIFICATIONS[8]).lower()
    assert "without the word" in (
        ACCIDENTS_IS_NOT_IN_THE_EIGHTH_HOUSES_PRINTED_LIST)
    assert "The event was the 4th's" in (
        A_GRAHA_CAN_CARRY_TWO_LORDSHIPS_INTO_THE_READING)


def test_example_113s_outcome_matches_the_house_it_named():
    from hora.core.const import HOUSE_SIGNIFICATIONS
    from hora.transits.latta import EXAMPLE_113, EXAMPLE_113_OUTCOME

    assert "5th December 1996" in EXAMPLE_113
    assert "vehicular accident" in EXAMPLE_113_OUTCOME
    assert "vehicles" in str(HOUSE_SIGNIFICATIONS[4]).lower()


# --------------------------------------------------------------------------
# Exercise 45 — two lattas meeting on one house
# --------------------------------------------------------------------------

def _gates_natal():
    from hora.charts.book import longitudes
    from hora.core.const import Graha

    printed = longitudes(24)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER,
             "Ven": Graha.VENUS, "Sat": Graha.SATURN, "Rahu": Graha.RAHU,
             "Ketu": Graha.KETU}
    return (printed,
            {int(graha): int(printed[name] // 30)
             for name, graha in named.items()})


def _gates_ruling_chart():
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    return compute_chart(
        from_local(2000, 6, 8, 12, 0, 0.0, utc_offset_hours=-7.0),
        Place(name="Seattle", latitude=47 + 36 / 60,
              longitude=-(122 + 20 / 60)),
        Settings(node_type=NodeType.MEAN))


def test_gatess_two_nakshatra_targets_are_punarvasu_and_uttarabhadrapada():
    from hora.core.const import NAKSHATRA_NAMES
    from hora.transits.latta import nakshatra_of

    printed, _signs = _gates_natal()
    assert str(NAKSHATRA_NAMES[nakshatra_of(printed["Asc"])]) == "Punarvasu"
    assert str(NAKSHATRA_NAMES[nakshatra_of(printed["Moon"])]) == (
        "Uttara Bhadrapada")


def test_rahu_kicks_the_janma_nakshatra_and_mars_the_lagna_nakshatra():
    """"Rahu had latta on janma nakshatra ... Mars ... i.e. lagna
    nakshatra!" Both at once, which Example 113 never had.
    """
    from hora.core.const import Graha
    from hora.transits.latta import latta_hits

    printed, _signs = _gates_natal()
    computed = _gates_ruling_chart()

    rahu = latta_hits("Rahu", computed.positions[int(Graha.RAHU)].longitude,
                      printed["Moon"], printed["Asc"])
    assert rahu["from_nakshatra"] == "Punarvasu"
    assert (rahu["offset"], rahu["direction"]) == (9, "backward")
    assert rahu["kicks"] == "Uttara Bhadrapada"
    assert rahu["hits"] == ["natal Moon"]
    assert rahu["on_janma_nakshatra"] is True

    mars = latta_hits("Mars", computed.positions[int(Graha.MARS)].longitude,
                      printed["Moon"], printed["Asc"])
    assert mars["from_nakshatra"] == "Mrigashira"
    assert (mars["offset"], mars["direction"]) == (3, "forward")
    assert mars["kicks"] == "Punarvasu"
    assert mars["hits"] == ["natal lagna"]
    assert mars["on_janma_nakshatra"] is False


def test_the_common_house_of_rahu_and_mars_is_the_sixth():
    """"Rahu occupies the 6th house in the natal chart and Mars owns it."
    Two different relations to one house.
    """
    from hora.core.const import Graha
    from hora.transits.latta import (
        OCCUPATION_AND_OWNERSHIP_BOTH_RELATE_A_GRAHA_TO_A_HOUSE,
        common_houses,
        houses_related_to,
    )

    printed, signs = _gates_natal()
    lagna = int(printed["Asc"] // 30)
    assert A[lagna] == "Ge"

    rahu = houses_related_to(int(Graha.RAHU), lagna, signs)
    mars = houses_related_to(int(Graha.MARS), lagna, signs)
    assert rahu["occupies"] == 6
    assert rahu["owns"] == []
    assert 6 in mars["owns"]
    assert mars["occupies"] != 6

    got = common_houses([int(Graha.RAHU), int(Graha.MARS)], lagna, signs)
    assert got["common"] == [6]
    assert got["relations"] == (
        OCCUPATION_AND_OWNERSHIP_BOTH_RELATE_A_GRAHA_TO_A_HOUSE)


def test_the_common_house_survives_oi_135s_other_co_lord_reading():
    """Our lord table gives Scorpio and Aquarius to Mars and Saturn. If the
    node were taken as Aquarius's lord, as the book does in every co-owned
    8th house it reads, Rahu would gain the 9th and the answer would not
    change.
    """
    from hora.core.const import Graha
    from hora.transits.latta import common_houses, houses_related_to

    printed, signs = _gates_natal()
    lagna = int(printed["Asc"] // 30)
    mars = set(houses_related_to(int(Graha.MARS), lagna, signs)["houses"])
    rahu = set(houses_related_to(int(Graha.RAHU), lagna, signs)["houses"])

    aquarius_house = (R["Aq"] - lagna) % 12 + 1
    assert aquarius_house == 9
    assert (rahu | {aquarius_house}) & mars == {6}
    assert common_houses([int(Graha.RAHU), int(Graha.MARS)],
                         lagna, signs)["common"] == [6]


def test_when_both_targets_are_struck_the_precedence_is_not_used_to_discard():
    from hora.transits.latta import (
        JANMA_NAKSHATRA_OUTRANKS_LAGNA_NAKSHATRA,
        WHEN_BOTH_TARGETS_ARE_STRUCK_THE_GRAHAS_ARE_INTERSECTED,
    )

    assert "more important" in JANMA_NAKSHATRA_OUTRANKS_LAGNA_NAKSHATRA
    assert "Rather than preferring the janma hit" in (
        WHEN_BOTH_TARGETS_ARE_STRUCK_THE_GRAHAS_ARE_INTERSECTED)


def test_the_sixth_house_matters_repeat_example_112s_missing_word():
    from hora.core.const import HOUSE_SIGNIFICATIONS
    from hora.transits.latta import EXERCISE_45_MATTERS

    assert EXERCISE_45_MATTERS == ("litigation", "enemies")
    sixth = str(HOUSE_SIGNIFICATIONS[6]).lower()
    assert "enemies" in sixth
    assert "litigation" not in sixth          # OI-55, a second time


def test_the_ruling_of_8_june_2000_is_now_read_four_ways():
    from hora.transits.gochara import EXAMPLE_112_RUNS
    from hora.transits.latta import THE_RULING_IS_READ_FOUR_TIMES
    from hora.transits.tara import TARA_WORKED_CASE
    from hora.transits.vedha import VEDHA_WORKED_CASE

    assert all(run[5] == "Krittika" for run in EXAMPLE_112_RUNS)
    assert str(VEDHA_WORKED_CASE["date"]) == "June 8, 2000"
    assert str(TARA_WORKED_CASE["date"]) == "June 8, 2000"
    assert TARA_WORKED_CASE["in_bad_taras"] == 5
    assert "One event, four techniques" in THE_RULING_IS_READ_FOUR_TIMES


def test_common_houses_checks_its_inputs():
    from hora.core.const import Graha
    from hora.core.validate import InputError
    from hora.transits.latta import LattaError, common_houses, houses_related_to

    _printed, signs = _gates_natal()
    with pytest.raises(LattaError, match="at least two grahas"):
        common_houses([int(Graha.MARS)], 0, signs)
    with pytest.raises(LattaError, match="no natal sign given"):
        houses_related_to(int(Graha.MARS), 0, {})
    with pytest.raises(InputError):
        houses_related_to(int(Graha.MARS), 12, signs)


# --------------------------------------------------------------------------
# §26.8 — the Sarvatobhadra chakra
# --------------------------------------------------------------------------

def test_figure_3_is_nine_by_nine_and_fully_transcribed():
    from hora.transits.sarvatobhadra import (
        A_IS_THE_ONE_LETTER_ON_TWO_SQUARES,
        FIGURE_3,
        cell,
    )

    assert len(FIGURE_3) == 9
    assert all(len(row) == 9 for row in FIGURE_3)
    squares = [c for row in FIGURE_3 for c in row]
    assert len(squares) == 81
    assert None not in squares

    # a is the one letter on two squares, and the second is off both diagonals
    assert cell(0, 8) == cell(2, 7) == "a"
    row, column = 2, 7
    assert row != column and row + column != 8      # off both diagonals
    assert squares.count("a") == 2
    assert all(squares.count(x) == 1 for x in squares if x != "a")
    assert "No other letter in Figure 3 is repeated" in (
        A_IS_THE_ONE_LETTER_ON_TWO_SQUARES)


def test_each_border_holds_seven_nakshatras_and_abhijit_is_among_them():
    from hora.transits.sarvatobhadra import (
        BORDER_NAKSHATRAS,
        SARVATOBHADRA_COMPOSITION,
    )

    assert set(BORDER_NAKSHATRAS) == {"north", "south", "east", "west"}
    assert all(len(side) == 7 for side in BORDER_NAKSHATRAS.values())
    every = [n for side in BORDER_NAKSHATRAS.values() for n in side]
    assert len(every) == len(set(every)) == 28
    assert "Abhijit" in every
    assert "Abhijit (the last quarter of Uttarashadha)" in (
        SARVATOBHADRA_COMPOSITION)


def test_every_diagonal_square_but_the_centre_holds_a_vowel():
    from hora.transits.sarvatobhadra import (
        DIAGONALS_HOLD_THE_VOWELS,
        FIGURE_3,
        VOWELS,
    )

    diagonal = {(r, c) for r in range(9) for c in range(9)
                if r == c or r + c == 8}
    diagonal.discard((4, 4))
    assert len(diagonal) == 16
    assert {FIGURE_3[r][c] for r, c in diagonal} == set(VOWELS)
    assert len(VOWELS) == len(set(VOWELS)) == 16
    assert "except the central square" in DIAGONALS_HOLD_THE_VOWELS


def test_the_sections_tally_is_right_in_total_and_wrong_in_its_split():
    """"16 (vowels) + 20 (consonants) + ... = 81". The figure has 17 vowel
    squares and 19 consonant squares. Both pairs sum to 36, so the 81 closes
    and the slip is easy to miss. D-77.
    """
    from hora.transits.sarvatobhadra import (
        BORDER_NAKSHATRAS,
        CENTRE_CELLS,
        FIGURE_3,
        RASI_CELLS,
        SARVATOBHADRA_TALLY,
        THE_TALLY_MISCOUNTS_THE_LETTERS,
        VOWELS,
    )

    nakshatras = {n for side in BORDER_NAKSHATRAS.values() for n in side}
    named = nakshatras | set(VOWELS) | set(RASI_CELLS)
    centres = set(CENTRE_CELLS)

    vowel_squares = [(r, c) for r in range(9) for c in range(9)
                     if (r, c) not in centres and FIGURE_3[r][c] in VOWELS]
    consonant_squares = [(r, c) for r in range(9) for c in range(9)
                         if (r, c) not in centres
                         and FIGURE_3[r][c] not in named]

    assert len(vowel_squares) == 17
    assert len({FIGURE_3[r][c] for r, c in vowel_squares}) == 16
    assert len(consonant_squares) == 19
    assert len({FIGURE_3[r][c] for r, c in consonant_squares}) == 19

    # the total still closes, which is why the split reads as right
    assert (len(vowel_squares) + len(consonant_squares) + len(RASI_CELLS)
            + len(nakshatras) + len(centres)) == 81
    assert 16 + 20 == len(vowel_squares) + len(consonant_squares) == 36

    assert "16 (vowels) + 20 (consonants)" in SARVATOBHADRA_TALLY
    assert "19 consonant squares" in THE_TALLY_MISCOUNTS_THE_LETTERS


def test_the_twelve_rasis_sit_where_figure_3_puts_them():
    from hora.transits.sarvatobhadra import FIGURE_3, RASI_CELLS

    assert len(RASI_CELLS) == 12
    for rasi, (row, column) in RASI_CELLS.items():
        assert FIGURE_3[row][column] == rasi
        assert rasi in A                      # all twelve, no duplicates
    assert set(RASI_CELLS) == set(A)


def test_the_five_central_squares_hold_the_tithi_groups_and_all_seven_days():
    from hora.transits.sarvatobhadra import CENTRE_CELLS, TITHI_GROUPS

    assert len(CENTRE_CELLS) == 5
    assert set(CENTRE_CELLS) == {(3, 4), (4, 3), (4, 4), (4, 5), (5, 4)}
    groups = {str(entry["tithi_group"]) for entry in CENTRE_CELLS.values()}
    assert groups == set(TITHI_GROUPS)

    weekdays = [day for entry in CENTRE_CELLS.values()
                for day in entry["weekdays"]]
    assert sorted(weekdays) == sorted([
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday"])


def test_the_twenty_fifth_tithi_belongs_to_no_group():
    """Four groups step by 5 and hold six tithis; Poorna holds five and steps
    5, 5, 5, 10. D-76.
    """
    from hora.transits.sarvatobhadra import (
        THE_TWENTY_FIFTH_TITHI_IS_MISSING,
        TITHI_GROUPS,
        tithi_group,
    )

    listed = sorted(t for group in TITHI_GROUPS.values() for t in group)
    assert len(listed) == len(set(listed)) == 29
    assert set(range(1, 31)) - set(listed) == {25}
    assert tithi_group(25) is None

    for name, group in TITHI_GROUPS.items():
        steps = {b - a for a, b in pairwise(group)}
        if name == "Poorna":
            assert steps == {5, 10}
            assert len(group) == 5
        else:
            assert steps == {5}
            assert len(group) == 6

    for tithi, expected in ((1, "Nanda"), (27, "Bhadra"), (28, "Jaya"),
                            (29, "Rikta"), (30, "Poorna")):
        assert tithi_group(tithi) == expected
    assert "in no group at all" in THE_TWENTY_FIFTH_TITHI_IS_MISSING


def test_the_vedha_rule_is_stated_ambiguously_and_example_114_fixes_it():
    from hora.transits.sarvatobhadra import (
        THE_LINES_RUN_INWARD_FROM_THE_NAKSHATRAS_OWN_BORDER,
        VEDHA_RULE,
    )

    assert "one vertical or horizontal line" in VEDHA_RULE
    assert "two crossward lines" in VEDHA_RULE
    assert "perpendicular to its border" in (
        THE_LINES_RUN_INWARD_FROM_THE_NAKSHATRAS_OWN_BORDER)


def test_the_chakras_definition_glosses_both_words():
    from hora.transits.sarvatobhadra import (
        BHADRA_MEANS,
        SARVATAH_MEANS,
        SARVATOBHADRA_DEFINITION,
    )

    assert SARVATAH_MEANS == "everywhere, or entirely"
    assert BHADRA_MEANS == "auspicious, or well"
    assert "all-round well-being" in SARVATOBHADRA_DEFINITION
    assert "auspicious and inauspicious results" in SARVATOBHADRA_DEFINITION


def test_sarvatobhadra_helpers_check_their_inputs():
    from hora.core.validate import InputError
    from hora.transits.sarvatobhadra import cell, tithi_group

    for bad in (-1, 9):
        with pytest.raises(InputError):
            cell(bad, 0)
        with pytest.raises(InputError):
            cell(0, bad)
    for bad in (0, 31):
        with pytest.raises(InputError):
            tithi_group(bad)


# --------------------------------------------------------------------------
# Example 114 — the three lines drawn, and sixteen squares confirmed
# --------------------------------------------------------------------------

def test_example_114s_three_lines_reproduce_square_for_square():
    """"Drawing a horizontal line to the west ... a crossward line to the
    northwest ... a crossward line to the southwest." Sixteen squares.
    """
    from hora.transits.sarvatobhadra import (
        EXAMPLE_114_LINES,
        EXAMPLE_114_VERIFIES_SIXTEEN_SQUARES,
        find,
        vedha_lines,
    )

    got = vedha_lines(*find("Punar"))
    assert got["border"] == "east"
    assert got["straight"] == "west"
    assert got["crossward"] == ("northwest", "southwest")

    for direction, expected in EXAMPLE_114_LINES.items():
        drawn = tuple(square["content"]
                      for square in got["lines"][direction])
        assert drawn == expected, direction

    assert sum(len(line) for line in EXAMPLE_114_LINES.values()) == 16
    assert len(got["obstructs"]) == 16
    assert "reproduces all sixteen" in EXAMPLE_114_VERIFIES_SIXTEEN_SQUARES


def test_the_two_d_squares_are_distinguished_as_the_example_distinguishes_them():
    from hora.transits.sarvatobhadra import EXAMPLE_114_LINES, FIGURE_3

    assert FIGURE_3[1][4] == "d"
    assert FIGURE_3[6][7] == "d."
    assert "d" in EXAMPLE_114_LINES["northwest"]
    assert "d." in EXAMPLE_114_LINES["southwest"]
    assert FIGURE_3[1][4] != FIGURE_3[6][7]


def test_the_lines_run_inward_from_whichever_border_the_nakshatra_is_on():
    from hora.transits.sarvatobhadra import (
        BORDER_DIRECTIONS,
        BORDER_NAKSHATRAS,
        border_of,
        find,
        vedha_lines,
    )

    for side, nakshatras in BORDER_NAKSHATRAS.items():
        for nakshatra in nakshatras:
            row, column = find(nakshatra)
            assert border_of(row, column) == side, nakshatra
            got = vedha_lines(row, column)
            assert got["border"] == side
            assert (got["straight"], *got["crossward"]) == (
                BORDER_DIRECTIONS[side])
            # every line runs inward and stays on the grid
            for line in got["lines"].values():
                assert line, nakshatra
                for square in line:
                    assert 0 <= square["row"] <= 8
                    assert 0 <= square["column"] <= 8


def test_a_nakshatras_three_lines_are_of_unequal_length():
    from hora.transits.sarvatobhadra import (
        LINES_ARE_UNEQUAL_IN_LENGTH,
        find,
        vedha_lines,
    )

    got = vedha_lines(*find("Punar"))
    assert [len(got["lines"][d]) for d in ("west", "northwest", "southwest")
            ] == [8, 5, 3]

    # a nakshatra at the far end of the same border reverses the diagonals
    other = vedha_lines(*find("Krittika"))
    assert other["border"] == "east"
    assert len(other["lines"]["northwest"]) < len(
        other["lines"]["southwest"])
    assert "nearer a corner obstructs fewer squares" in (
        LINES_ARE_UNEQUAL_IN_LENGTH)


def test_only_a_border_square_that_is_not_a_corner_draws_lines():
    from hora.transits.sarvatobhadra import (
        SarvatobhadraError,
        border_of,
        find,
        vedha_lines,
    )

    for corner in ((0, 0), (0, 8), (8, 0), (8, 8)):
        with pytest.raises(SarvatobhadraError, match="corner"):
            border_of(*corner)
    with pytest.raises(SarvatobhadraError, match="not on a border"):
        vedha_lines(4, 4)
    with pytest.raises(SarvatobhadraError, match="not in Figure 3"):
        find("Abhijeet")


# --------------------------------------------------------------------------
# Exercise 46 — Venus in Makha, and the square that was blank
# --------------------------------------------------------------------------

def test_exercise_46s_three_lines_reproduce_square_for_square():
    from hora.transits.sarvatobhadra import (
        EXERCISE_46_LINES,
        find,
        vedha_lines,
    )

    got = vedha_lines(*find("Makha"))
    assert find("Makha") == (8, 7)
    assert got["border"] == "south"
    assert got["straight"] == "north"
    assert got["crossward"] == ("northwest", "northeast")

    for direction, expected in EXERCISE_46_LINES.items():
        drawn = tuple(square["content"]
                      for square in got["lines"][direction])
        assert drawn == expected, direction


def test_exercise_46_is_what_read_the_square_that_was_left_blank():
    """"uu, d (alveolar), h, k, v, a, u and Bharani" — the sixth is row 2,
    column 7, which had no reading until this answer.
    """
    from hora.transits.sarvatobhadra import EXERCISE_46_LINES, cell

    northward = EXERCISE_46_LINES["north"]
    assert northward[5] == "a"
    assert cell(2, 7) == "a"
    # and it is the sixth square north of Makha
    assert northward.index("a") == 5


def test_a_nakshatra_beside_a_corner_obstructs_far_less():
    from hora.transits.sarvatobhadra import (
        A_CORNER_NAKSHATRA_OBSTRUCTS_FAR_LESS,
        find,
        vedha_lines,
    )

    makha = vedha_lines(*find("Makha"))
    assert [len(makha["lines"][d])
            for d in ("north", "northwest", "northeast")] == [8, 7, 1]
    assert len(makha["obstructs"]) == 16

    punarvasu = vedha_lines(*find("Punar"))
    assert len(punarvasu["obstructs"]) == 16
    # same total here, but distributed quite differently
    assert sorted(len(line) for line in makha["lines"].values()) != sorted(
        len(line) for line in punarvasu["lines"].values())
    assert "one crossward line of a single square" in (
        A_CORNER_NAKSHATRA_OBSTRUCTS_FAR_LESS)


def test_the_tithi_groups_named_on_the_line_carry_their_weekdays():
    from hora.transits.sarvatobhadra import CENTRE_CELLS, find, vedha_lines

    got = vedha_lines(*find("Makha"))
    on_line = {square["content"]
               for square in got["lines"]["northwest"]}
    assert {"Bhadra", "Jaya"} <= on_line

    by_group = {str(entry["tithi_group"]): entry["weekdays"]
                for entry in CENTRE_CELLS.values()}
    assert by_group["Bhadra"] == ("Monday", "Wednesday")
    assert by_group["Jaya"] == ("Thursday",)


# --------------------------------------------------------------------------
# §26.8's four special principles
# --------------------------------------------------------------------------

def test_the_corners_are_joins_in_the_nakshatra_sequence():
    """"A planet in the first quarter of Krittika or the last quarter of
    Bharani has vedha on the vowel a." The border read clockwise is the
    nakshatras in order with a corner vowel between every eighth pair.
    """
    from hora.transits.sarvatobhadra import (
        CORNER_VOWELS,
        FIGURE_3,
        THE_CORNERS_ARE_JOINS_IN_THE_NAKSHATRA_SEQUENCE,
    )

    ring = ([(0, c) for c in range(9)] + [(r, 8) for r in range(1, 9)]
            + [(8, c) for c in range(7, -1, -1)]
            + [(r, 0) for r in range(7, 0, -1)])
    assert len(ring) == 32
    sequence = [FIGURE_3[r][c] for r, c in ring]

    corners = [index for index, square in enumerate(sequence)
               if square in CORNER_VOWELS]
    assert corners == [0, 8, 16, 24]

    for vowel, entry in CORNER_VOWELS.items():
        index = sequence.index(vowel)
        assert sequence[index - 1] .startswith(
            str(entry["last_quarter_of"])[:4])
        assert sequence[(index + 1) % 32].startswith(
            str(entry["first_quarter_of"])[:4])
    assert CORNER_VOWELS["a"]["last_quarter_of"] == "Bharani"
    assert CORNER_VOWELS["a"]["first_quarter_of"] == "Krittika"
    assert "one every eight squares" in (
        THE_CORNERS_ARE_JOINS_IN_THE_NAKSHATRA_SEQUENCE)


def test_no_vedha_line_ever_reaches_a_corner():
    """Which is why principle (1) has to be stated separately."""
    from hora.transits.sarvatobhadra import (
        BORDER_NAKSHATRAS,
        CORNER_VOWELS,
        find,
        vedha_lines,
    )

    squares = {tuple(entry["square"]) for entry in CORNER_VOWELS.values()}
    for side in BORDER_NAKSHATRAS.values():
        for nakshatra in side:
            got = vedha_lines(*find(nakshatra))
            reached = {(s["row"], s["column"])
                       for line in got["lines"].values() for s in line}
            assert not reached & squares, nakshatra


def test_the_similar_vowel_list_is_open():
    from hora.transits.sarvatobhadra import (
        SIMILAR_VOWEL_RULE,
        SIMILAR_VOWELS,
        THE_SIMILAR_VOWEL_LIST_IS_OPEN,
        VOWELS,
    )

    assert SIMILAR_VOWELS == (("a", "aa"), ("i", "ee"), ("u", "uu"))
    assert "e.g." in SIMILAR_VOWEL_RULE
    for short, long in SIMILAR_VOWELS:
        assert short in VOWELS and long in VOWELS

    # two more short-long pairs sit in the figure and are not named
    unnamed = {("ri", "rii"), ("lu", "luu")}
    for short, long in unnamed:
        assert short in VOWELS and long in VOWELS
        assert (short, long) not in SIMILAR_VOWELS
    assert "does not name them" in THE_SIMILAR_VOWEL_LIST_IS_OPEN


def test_the_uncovered_consonants_are_one_triple_per_border():
    from hora.transits.sarvatobhadra import (
        FIGURE_3,
        THE_UNCOVERED_CONSONANTS_ARE_ONE_TRIPLE_PER_BORDER,
        UNCOVERED_CONSONANTS,
        border_of,
        find,
    )

    assert len(UNCOVERED_CONSONANTS) == 4
    assert all(len(extra) == 3 for extra in UNCOVERED_CONSONANTS.values())
    assert sum(len(e) for e in UNCOVERED_CONSONANTS.values()) == 12

    in_figure = {"Ardra": "Ardra", "Hasta": "Hasta",
                 "Poorvashadha": "P.Shadha",
                 "Uttara Bhadrapada": "U.Bhadra"}
    borders = {border_of(*find(square)) for square in in_figure.values()}
    assert borders == {"north", "south", "east", "west"}

    squares = {c for row in FIGURE_3 for c in row}
    extras = [c for triple in UNCOVERED_CONSONANTS.values() for c in triple]
    assert [c for c in extras if c in squares] == ["g", "h"]
    assert "g and h are in the figure as well" in (
        THE_UNCOVERED_CONSONANTS_ARE_ONE_TRIPLE_PER_BORDER)


def test_the_consonant_pairs_reach_letters_the_grid_lacks():
    from hora.transits.sarvatobhadra import (
        FIGURE_3,
        PAIRED_CONSONANTS,
        THE_PAIRS_REACH_CONSONANTS_THE_GRID_LACKS,
    )

    assert len(PAIRED_CONSONANTS) == 5
    squares = {c for row in FIGURE_3 for c in row}
    present = {c for pair in PAIRED_CONSONANTS for c in pair if c in squares}
    assert present == {"v", "s", "kh", "j", "y"}
    absent = {c for pair in PAIRED_CONSONANTS for c in pair
              if c not in squares}
    assert absent == {"b", "sh (palatal)", "sh (alveolar)", "ng", "tr"}
    assert "none of which the chart draws" in (
        THE_PAIRS_REACH_CONSONANTS_THE_GRID_LACKS)


# --------------------------------------------------------------------------
# Using the chakra, and the special tithis
# --------------------------------------------------------------------------

def test_the_five_natal_points_include_the_only_non_astronomical_input():
    from hora.transits.sarvatobhadra import (
        NATAL_POINTS_TO_WATCH,
        THE_NAME_IS_THE_ONLY_NON_ASTRONOMICAL_INPUT,
    )

    assert len(NATAL_POINTS_TO_WATCH) == 5
    points = [entry["point"] for entry in NATAL_POINTS_TO_WATCH]
    assert "the constellation occupied by Moon" in points[0]
    assert "native's name" in points[2]
    assert "janma tithi" in points[3]
    assert "janma vaara" in points[4]

    alternatives = [entry["alternative"] for entry in NATAL_POINTS_TO_WATCH]
    assert alternatives[0] == "any special tara"
    assert alternatives[3] == "a special tithi"
    assert "not a position or a moment" in (
        THE_NAME_IS_THE_ONLY_NON_ASTRONOMICAL_INPUT)


def test_the_benefic_split_ignores_the_books_own_conditional_cases():
    from hora.core.const import NATURAL_BENEFIC, NATURAL_MALEFIC, Graha
    from hora.transits.sarvatobhadra import (
        SARVATOBHADRA_BENEFICS,
        SARVATOBHADRA_MALEFICS,
        THE_SPLIT_IGNORES_THE_CONDITIONAL_BENEFICS,
    )

    assert len(SARVATOBHADRA_BENEFICS) + len(SARVATOBHADRA_MALEFICS) == 9
    assert set(SARVATOBHADRA_BENEFICS) == {"Moon", "Mercury", "Jupiter",
                                           "Venus"}
    assert {str(Graha[name.upper()]) for name in SARVATOBHADRA_MALEFICS} == {
        str(g) for g in NATURAL_MALEFIC}

    # but the book's own natural benefics are only two
    assert {str(g) for g in NATURAL_BENEFIC} == {str(Graha.JUPITER),
                                                 str(Graha.VENUS)}
    assert Graha.MOON not in NATURAL_BENEFIC
    assert Graha.MERCURY not in NATURAL_BENEFIC
    assert "neither is in NATURAL_BENEFIC" in (
        THE_SPLIT_IGNORES_THE_CONDITIONAL_BENEFICS)


def test_footnote_70_disclaims_the_authors_own_experience():
    from hora.transits.sarvatobhadra import (
        FOOTNOTE_70,
        FOOTNOTE_70_IS_A_DISCLAIMER_OF_EXPERIENCE,
    )
    from hora.transits.tara import FOOTNOTE_72, FOOTNOTE_74

    assert "very very limited" in FOOTNOTE_70
    assert "experience" in FOOTNOTE_70
    assert "experience" not in FOOTNOTE_72
    assert "experience" not in FOOTNOTE_74
    assert "the author's own acquaintance" in (
        FOOTNOTE_70_IS_A_DISCLAIMER_OF_EXPERIENCE)


def test_a_multiplier_of_one_is_the_ordinary_tithi():
    import random

    from hora.panchanga.core import tithi_at
    from hora.transits.sarvatobhadra import (
        A_MULTIPLIER_OF_ONE_IS_THE_ORDINARY_TITHI,
        special_tithi,
    )

    random.seed(26)
    for _ in range(500):
        sun = random.uniform(0.0, 360.0)
        moon = random.uniform(0.0, 360.0)
        assert special_tithi(sun, moon, 1)["tithi"] == tithi_at(sun, moon)
    assert "section 1.3.8's tithi unchanged" in (
        A_MULTIPLIER_OF_ONE_IS_THE_ORDINARY_TITHI)


def test_karma_tithi_changes_ten_times_as_fast_and_dhana_twice():
    from hora.transits.sarvatobhadra import (
        SPECIAL_TITHI_MULTIPLIERS,
        special_tithi,
    )

    assert SPECIAL_TITHI_MULTIPLIERS == {"karma": 10, "dhana": 2}

    def changes(multiplier):
        seen, previous = 0, None
        for step in range(3600):
            current = special_tithi(0.0, step * 0.1, multiplier)["tithi"]
            if previous is not None and current != previous:
                seen += 1
            previous = current
        return seen

    assert changes(1) == 29                # 30 tithis, no wrap
    assert changes(2) == 59
    assert changes(10) == 299

    named = special_tithi(0.0, 30.0, 10)
    assert named["name"] == "karma"
    assert 1 <= named["tithi"] <= 30
    assert special_tithi(0.0, 30.0, 2)["name"] == "dhana"
    assert special_tithi(0.0, 30.0, 3)["name"] is None


def test_a_special_tithi_carries_its_group():
    from hora.transits.sarvatobhadra import TITHI_GROUPS, special_tithi

    for multiplier in (1, 2, 10):
        for step in range(0, 360, 7):
            got = special_tithi(0.0, float(step), multiplier)
            assert 1 <= got["tithi"] <= 30
            if got["tithi"] == 25:
                assert got["group"] is None          # D-76
            else:
                assert got["group"] in TITHI_GROUPS


def test_special_tithi_checks_its_inputs():
    from hora.core.validate import InputError
    from hora.transits.sarvatobhadra import special_tithi

    for bad in (0, -1, 361):
        with pytest.raises(InputError):
            special_tithi(0.0, 10.0, bad)
