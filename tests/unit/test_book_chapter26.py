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
