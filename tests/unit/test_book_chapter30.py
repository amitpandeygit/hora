"""Chapter 30 — Annual dasas. §30.1 and footnotes 85 and 86."""

import pytest

from hora.dasha.annual import intro

# --------------------------------------------------------------------------
# §30.1 Introduction
# --------------------------------------------------------------------------


def test_the_introduction_is_transcribed():
    assert intro.CHAPTER_TITLE == "Annual Dasas"
    assert "when in the year will (s)he get married?" in intro.WHY_ANNUAL_DASAS
    assert "paramayush is of the order of 100 years" in (
        intro.WHY_THEY_MUST_BE_COMPRESSED)
    assert "compressed to a one-year period" in intro.WHY_THEY_MUST_BE_COMPRESSED
    assert "one constellation per year" in (
        intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED)
    assert "one sign per year" in intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED


def test_the_three_dasas_are_named_in_the_chapters_order():
    names = [row["name"] for row in intro.ANNUAL_DASAS]
    assert names == ["Patyayini dasa", "Mudda dasa", "Varsha Narayana dasa"]
    assert [row["number"] for row in intro.ANNUAL_DASAS] == [1, 2, 3]
    mudda = intro.ANNUAL_DASAS[1]
    assert mudda["also_called"] == ("Varsha Vimsottari dasa",)
    assert intro.ANNUAL_DASAS[0]["source"] == "mentioned by Tajaka writers"


def test_footnote_85_gives_ramans_name_for_patyayini():
    assert intro.FOOTNOTE_85 == (
        'Dr. B.V. Raman simply called this "Varsha dasa" (annual dasa).')
    assert "Varsha dasa" in intro.ANNUAL_DASAS[0]["also_called"]


def test_vimsottaris_paramayush_is_the_120_the_chapter_names():
    assert intro.paramayush("vimshottari") == 120
    assert "paramayush of 120 years" in (
        intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED)


def test_narayana_dasas_paramayush_is_144_not_120():
    """Every rasi's first cycle plus its second is twelve years, and there are
    twelve rasis. Derived from chapter 18's own rule, not asserted. OI-174.
    """
    from hora.dasha.rasi.narayana import second_cycle_length

    for first in range(1, 13):
        assert first + second_cycle_length(first) == 12
    assert intro.narayana_full_cycle_years() == 144
    assert intro.narayana_full_cycle_years() != 120
    assert "144 years" in intro.NARAYANA_DASAS_PARAMAYUSH_IS_144_NOT_120


def test_the_first_narayana_cycle_alone_is_not_a_fixed_total_either():
    """So 120 is not the first cycle's sum under any chart."""
    from hora.dasha.rasi.narayana import second_cycle_length

    # A rasi's first-cycle length runs 1 to 12, so twelve rasis sum anywhere
    # from 12 to 144. Nothing pins it to 120.
    assert 12 * 1 == 12
    assert 12 * 12 == 144
    assert second_cycle_length(12) == 0
    assert "not a fixed total at all" in (
        intro.NARAYANA_DASAS_PARAMAYUSH_IS_144_NOT_120)


def test_the_order_of_a_hundred_covers_the_dasas_the_book_taught():
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    totals = sorted(spec.total_years
                    for spec in NAKSHATRA_DASHA_SYSTEMS.values())
    assert totals[0] == 36 and totals[-1] == 120
    assert sum(1 for t in totals if 84 <= t <= 120) == 7
    assert "from 36 years to 120" in (
        intro.THE_ORDER_OF_A_HUNDRED_IS_A_RANGE_NOT_A_FIGURE)


# --------------------------------------------------------------------------
# The seeding choice, and footnote 86
# --------------------------------------------------------------------------


def test_both_seeds_come_from_the_natal_chart_not_the_annual_one():
    seeds = intro.SEEDING_CHOICES
    assert [row["dasa"] for row in seeds] == ["Mudda dasa",
                                              "Varsha Narayana dasa"]
    for row in seeds:
        assert "annual chart" in row["declined"]
        assert "natal chart" in row["taken"]
    assert [row["rate"] for row in seeds] == ["one constellation per year",
                                              "one sign per year"]
    assert "named and declined in both cases" in (
        intro.THE_ANNUAL_CHART_IS_NOT_THE_SEED)


def test_the_two_progressions_cycle_on_different_schedules():
    """27 constellations at one a year, 12 signs at one a year."""
    from hora.core.const import NAKSHATRA_COUNT

    assert NAKSHATRA_COUNT == 27
    assert intro.SEEDING_CHOICES[0]["rate"] == "one constellation per year"
    assert intro.SEEDING_CHOICES[1]["rate"] == "one sign per year"
    assert "cycles in 27 years and one sign a year in 12" in (
        intro.THE_TWO_PROGRESSIONS_HAVE_DIFFERENT_PERIODS)


def test_footnote_86_is_a_provenance_mark():
    assert intro.FOOTNOTE_86 == "This is a result of the author's own researches."
    assert "the author's own research" in intro.FOOTNOTE_86_IS_A_PROVENANCE_MARK


def test_25_4s_note_no_longer_claims_to_be_the_only_such_mark():
    """It said "the only section in the book to label its own technique".
    Footnote 86 does the same thing.
    """
    import inspect

    from hora.transits import gochara

    source = inspect.getsource(gochara)
    assert "the only section in the book to label its own" not in source
    assert "one of\n#: two places in the book that label the author's own" in (
        source)
    assert "footnote 86 of §30.1" in source


def test_precedence_covers_both_places(tmp_path):
    import pathlib

    text = pathlib.Path("docs/precedence.md").read_text()
    assert "When PVR marks his own research" in text
    assert "§25.4 and §30.1's footnote 86" in text
    assert "seeds two of chapter 30's three annual dasas" in text


def test_whether_footnote_86_covers_both_rules_is_not_marked():
    """It sits on the Narayana sentence; the Vimsottari sentence one earlier
    makes the same claim and carries none.
    """
    paragraph = intro.HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED
    vimsottari = paragraph.index("compressed Vimsottari dasa")
    narayana = paragraph.index("compressed Narayana dasa")
    assert vimsottari < narayana
    assert "Similarly" in paragraph
    assert "carries no footnote" in (
        intro.WHETHER_FOOTNOTE_86_COVERS_BOTH_RULES_IS_NOT_MARKED)


def test_the_compressed_dasas_point_at_systems_we_already_have():
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    mudda = intro.ANNUAL_DASAS[1]
    assert mudda["compressed_from"] == "vimshottari"
    assert mudda["compressed_from"] in NAKSHATRA_DASHA_SYSTEMS
    assert intro.ANNUAL_DASAS[2]["compressed_from"] == "narayana"
    assert intro.ANNUAL_DASAS[0]["compressed_from"] is None


def test_nothing_is_computed_from_the_introduction_yet():
    """§30.1 states the plan; the three dasas arrive in §30.2 onwards."""
    with pytest.raises(KeyError):
        intro.paramayush("patyayini")


# --------------------------------------------------------------------------
# Example 122 and Chart 67
# --------------------------------------------------------------------------

from hora.charts.chart import Place, compute_chart
from hora.core.const import RASI_ABBR, Graha
from hora.core.settings import NodeType, Settings
from hora.core.timeutil import from_local
from hora.dasha.annual import example

_PLACE = Place(name="Example 122", latitude=16 + 15 / 60, longitude=81 + 12 / 60)
_SETTINGS = Settings(node_type=NodeType.MEAN)
_PRAVESH = from_local(1993, 6, 1, 13, 30, 4.0, utc_offset_hours=5.5)
_BIRTH = from_local(1972, 6, 1, 4, 16, 0.0, utc_offset_hours=5.5)


def _annual():
    return compute_chart(_PRAVESH, _PLACE, _SETTINGS)


def _annual_longitudes():
    chart = _annual()
    names = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
    return ({name: chart.positions[i].longitude
             for i, name in enumerate(names)}, chart.lagna_longitude)


def test_the_example_and_its_varsha_pravesh_line_are_transcribed():
    assert "born on 1st June 1972 at 4:16 am" in example.EXAMPLE_122
    assert "married on 24th July 1993" in example.EXAMPLE_122
    assert "1:30:04 pm (IST)" in example.VARSHA_PRAVESH_DATA
    assert example.CHART_NUMBER == 67


def test_the_nativity_is_chart_18_and_the_example_does_not_say_so():
    from hora.charts.book import chart

    eighteen = chart(18)
    assert eighteen["birth"] == "June 1, 1972, 4:16 am (IST), 81 E 12, 16 N 15"
    assert eighteen["longitudes"]["Sun"] == "17 Ta 04"
    assert chart(67)["longitudes"]["Sun"] == "17 Ta 04"
    assert "Chart 18" not in example.EXAMPLE_122
    assert "does not name the chart" in example.THE_NATIVITY_IS_CHART_18_UNNAMED


def test_chart_67_reproduces_within_one_arcminute_and_always_high():
    """Ten bodies, ten positive residuals under an arcminute. D-80 again."""
    from hora.charts.book import longitudes

    chart = _annual()
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    printed = longitudes(67)
    worst = 0.0
    for name, index in ids.items():
        got = chart.positions[index].longitude
        gap = (((got - printed[name] + 180) % 360) - 180) * 60
        assert 0.0 < gap < 1.0, (name, gap)
        worst = max(worst, gap)
    lagna_gap = (((chart.lagna_longitude - printed["Asc"] + 180) % 360)
                 - 180) * 60
    assert 0.0 < lagna_gap < 1.0
    assert worst < 1.0
    assert "every residual is positive" in example.CHART_67_TRUNCATES_LIKE_CHART_66


def test_the_varsha_pravesh_reproduces_to_seven_seconds():
    """§27.1's solar return on Chart 18, in her 22nd year."""
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_BIRTH, _PLACE, _SETTINGS).positions[0].longitude
    got = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                         natal_sun, _BIRTH.jd_ut, 22)
    assert got["found"] is True
    seconds = (got["jd"] - _PRAVESH.jd_ut) * 86400.0
    assert 0.0 < seconds < 10.0
    assert "6.6 seconds" in example.THE_VARSHA_PRAVESH_REPRODUCES_TO_SEVEN_SECONDS


def test_the_vivaha_saham_reproduces_and_needs_the_correction():
    """2 Sg 22, with the thirty degrees added."""
    from hora.tajaka.sahams import sahams

    longitudes, lagna = _annual_longitudes()
    got = sahams(longitudes=longitudes, lagna=lagna, daytime=True)["Vivaha"]
    assert got["correction"] == 30.0
    assert RASI_ABBR[got["rasi"]] == "Sg"
    assert got["longitude"] % 30 == pytest.approx(2 + 22 / 60, abs=0.01)
    # Without the correction it would fall in Scorpio, a whole rasi away.
    assert RASI_ABBR[int(got["uncorrected"] // 30)] == "Sc"
    assert "which is what the book prints" in (
        example.THE_VIVAHA_SAHAM_NEEDS_THE_CORRECTION)


def test_the_lagna_holds_the_seventh_lord_and_the_saham_lord():
    """Both are Jupiter, and Jupiter is in the lagna."""
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    chart = _annual()
    lagna_rasi = chart.lagna_rasi
    assert RASI_ABBR[lagna_rasi] == "Vi"
    seventh = (lagna_rasi + 6) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[seventh])]) == "Jupiter"
    saham_rasi = RASI_ABBR.index("Sg")
    assert str(GRAHA_NAMES[int(RASI_LORD[saham_rasi])]) == "Jupiter"
    assert int(chart.positions[int(Graha.JUPITER)].longitude // 30) == lagna_rasi


def test_lagna_lord_mercury_is_in_his_own_sign():
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    chart = _annual()
    assert str(GRAHA_NAMES[int(RASI_LORD[chart.lagna_rasi])]) == "Mercury"
    mercury_rasi = int(chart.positions[int(Graha.MERCURY)].longitude // 30)
    assert RASI_ABBR[mercury_rasi] == "Ge"
    assert int(RASI_LORD[mercury_rasi]) == int(Graha.MERCURY)


def test_mercury_has_an_ithasala_with_jupiter():
    """A square, 6.20° apart against a binding deeptamsa of 7 — the closest
    call in the paragraph.
    """
    from hora.tajaka.yogas import ithasala

    longitudes, _ = _annual_longitudes()
    got = ithasala(faster=int(Graha.MERCURY), slower=int(Graha.JUPITER),
                   faster_longitude=longitudes["Mercury"],
                   slower_longitude=longitudes["Jupiter"])
    assert got["aspect"] == "Square aspect"
    assert got["binding_deeptamsa"] == 7.0
    assert got["separation_from_exact"] == pytest.approx(6.20, abs=0.02)
    assert got["type"] == "Vartamaana"
    assert "the closest call" in example.EVERY_REASON_IN_THE_PARAGRAPH_CHECKS_OUT


def test_the_navamsa_claims_hold():
    """Jupiter with Venus in the 2nd from a Pisces lagna, Mercury in the 9th.
    """
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    chart = _annual()
    nav_lagna = int(d9_navamsa(chart.lagna_longitude).sign)
    assert RASI_ABBR[nav_lagna] == "Pi"
    assert str(GRAHA_NAMES[int(RASI_LORD[nav_lagna])]) == "Jupiter"
    seventh = (nav_lagna + 6) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[seventh])]) == "Mercury"

    where = {name: int(d9_navamsa(chart.positions[g].longitude).sign)
             for name, g in (("Jupiter", Graha.JUPITER), ("Venus", Graha.VENUS),
                             ("Mercury", Graha.MERCURY))}
    assert where["Jupiter"] == where["Venus"]
    assert RASI_ABBR[where["Jupiter"]] == "Ar"
    assert (where["Jupiter"] - nav_lagna) % 12 + 1 == 2      # the 2nd
    assert (where["Mercury"] - nav_lagna) % 12 + 1 == 9      # a trikona


def test_the_drawn_navamsa_reproduces_body_for_body():
    from hora.charts.book import chart as record
    from hora.charts.vargas import d9_navamsa

    chart = _annual()
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    drawn = record(67)["divisional"]["D9"]
    for name, index in ids.items():
        got = int(d9_navamsa(chart.positions[index].longitude).sign)
        assert RASI_ABBR[got] == drawn[name], name
    assert RASI_ABBR[int(d9_navamsa(chart.lagna_longitude).sign)] == drawn["Asc"]


def test_the_muntha_in_capricorn_is_28_1s_rule():
    from hora.tajaka.muntha import muntha_rasi

    natal = compute_chart(_BIRTH, _PLACE, _SETTINGS)
    assert RASI_ABBR[natal.lagna_rasi] == "Ar"
    got = muntha_rasi(natal.lagna_rasi, 22)
    assert RASI_ABBR[int(got["rasi"])] == "Cp"

    from hora.charts.book import chart as record

    assert record(67)["drawn"]["Muntha"] == "Cp"
    assert "The diagram draws it in Capricorn" in (
        example.THE_MUNTHA_IN_CAPRICORN_IS_28_1S_RULE)


def test_all_eight_chara_karakas_match_and_one_pair_by_1_6_arcminutes():
    from hora.charts.book import chart as record
    from hora.charts.karaka import chara_karakas

    chart = _annual()
    got = chara_karakas({g: chart.positions[g].longitude for g in range(8)})
    printed = record(67)["chara_karakas"]
    short = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars", "Mercury": "Merc",
             "Jupiter": "Jup", "Venus": "Ven", "Saturn": "Sat", "Rahu": "Rahu"}
    for row in got:
        assert printed[short[row.graha_name]] == row.symbol, row.graha_name

    by_name = {row.graha_name: row.advancement for row in got}
    gap = abs(by_name["Moon"] - by_name["Mercury"]) * 60
    assert gap == pytest.approx(1.6, abs=0.2)
    assert "1.6 arcminutes apart" in (
        example.THE_KARAKA_ORDER_TURNS_ON_1_6_ARCMINUTES)


def test_one_sunrise_explains_both_hl_and_gl_and_it_is_not_ours():
    """OI-103's evidence from a fourth chart, and it removes the latitude
    hypothesis: 54% at 16 N against 23% at 26 N.
    """
    from hora.charts.book import longitudes
    from hora.charts.special_lagna import all_special_lagnas
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import SunriseMode

    chart = _annual()
    printed = longitudes(67)

    def lagnas(rise):
        got = all_special_lagnas(
            sunrise_jd=rise, jd_ut=_PRAVESH.jd_ut,
            lagna_longitude=chart.lagna_longitude,
            moon_longitude=chart.positions[1].longitude, settings=_SETTINGS)
        return got[1].longitude, got[2].longitude

    low, high = _PRAVESH.jd_ut - 0.6, _PRAVESH.jd_ut - 0.2
    for _ in range(60):
        middle = (low + high) / 2
        if lagnas(middle)[0] < printed["HL"]:
            high = middle
        else:
            low = middle
    solved = (low + high) / 2
    hl, gl = lagnas(solved)
    assert abs(hl - printed["HL"]) * 60 < 0.01
    # The free check: the same sunrise reproduces the GL as well.
    assert abs(gl - printed["GL"]) * 60 < 0.5

    times = {}
    for mode in (SunriseMode.DISC_UPPER_LIMB, SunriseMode.DISC_CENTER):
        eph = get_ephemeris(Settings(node_type=NodeType.MEAN,
                                     sunrise_mode=mode))
        eph.set_observer(_PLACE.latitude, _PLACE.longitude, 0.0)
        times[mode] = eph.sunrise(_PRAVESH.jd_ut - 0.5, _PLACE.latitude,
                                  _PLACE.longitude)
    span = times[SunriseMode.DISC_CENTER] - times[SunriseMode.DISC_UPPER_LIMB]
    fraction = (solved - times[SunriseMode.DISC_UPPER_LIMB]) / span
    assert 0.50 < fraction < 0.58              # 54% at 16 N 15
    assert "does not grow with latitude" in (
        example.THE_SUNRISE_OFFSET_IS_NOT_A_FUNCTION_OF_LATITUDE)
