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


# --------------------------------------------------------------------------
# §30.2 Patyayini dasa
# --------------------------------------------------------------------------

from hora.dasha.annual import patyayini


def _patyayini():
    chart = _annual()
    return patyayini.patyayini_dasa(
        lagna=chart.lagna_longitude,
        longitudes={g: chart.positions[g].longitude for g in range(7)},
        start_jd=_PRAVESH.jd_ut)


def _minutes(text: str) -> float:
    degrees, arcminutes = text.split()
    return float(degrees) + float(arcminutes) / 60.0


def test_the_procedure_and_footnote_87_are_transcribed():
    assert "specifically meant for Tajaka charts" in patyayini.PATYAYINI_SCOPE
    steps = [row["step"] for row in patyayini.PATYAYINI_PROCEDURE]
    assert steps == [1, 2, 3, 4]
    assert "Krisamsas" in str(patyayini.PATYAYINI_PROCEDURE[0]["text"])
    assert "Patyamsas" in str(patyayini.PATYAYINI_PROCEDURE[1]["text"])
    assert "365.2425" in str(patyayini.PATYAYINI_PROCEDURE[2]["text"])
    assert "First antardasa is the same as dasa" in str(
        patyayini.PATYAYINI_PROCEDURE[3]["text"])
    assert "largest krisamsa" in patyayini.FOOTNOTE_87
    assert patyayini.PATYAYINI_YEAR_DAYS == 365.2425


def test_the_order_matches_table_75():
    got = _patyayini()
    assert got["order"] == tuple(str(row["body"]) for row in patyayini.TABLE_75)
    assert got["order"] == ("Venus", "Mercury", "Moon", "Saturn", "Lagna",
                            "Jupiter", "Sun", "Mars")


def test_footnote_87_is_an_identity_not_an_observation():
    """The patyamsas telescope, so their sum is the largest krisamsa in every
    chart — checked here and over random charts.
    """
    import random

    got = _patyayini()
    assert got["footnote_87_holds"] is True
    assert got["sum_of_patyamsas"] == pytest.approx(got["largest_krisamsa"])
    assert _minutes(patyayini.TABLE_75_DENOMINATOR) == pytest.approx(
        _minutes(str(patyayini.TABLE_75[-1]["krisamsa"])))

    random.seed(302)
    for _ in range(300):
        rolled = patyayini.patyayini_dasa(
            lagna=random.uniform(0, 360),
            longitudes={g: random.uniform(0, 360) for g in range(7)})
        assert rolled["footnote_87_holds"] is True
    assert "in every chart" in patyayini.THE_SUM_TELESCOPES_TO_THE_LARGEST_KRISAMSA


def test_table_75_reproduces_cell_for_cell_from_its_own_krisamsas():
    """Separates the arithmetic from the ephemeris: fed the book's own
    rounded krisamsas, every fraction and every day count comes back.
    """
    total = _minutes(patyayini.TABLE_75_DENOMINATOR)
    previous = 0.0
    for row in patyayini.TABLE_75:
        krisamsa = _minutes(str(row["krisamsa"]))
        patyamsa = krisamsa - previous
        previous = krisamsa
        assert patyamsa == pytest.approx(_minutes(str(row["patyamsa"])),
                                         abs=1e-9), row["body"]
        fraction = patyamsa / total
        assert fraction == pytest.approx(float(row["fraction"]), abs=5e-5)
        days = patyayini.PATYAYINI_YEAR_DAYS * fraction
        assert days == pytest.approx(float(row["days"]), abs=0.006)
    assert "confirmed separately from the ephemeris" in (
        patyayini.TABLE_75_REPRODUCES_FROM_ITS_OWN_KRISAMSAS)


def test_the_dasa_lengths_sum_to_the_year_the_section_names():
    got = _patyayini()
    assert got["total_days"] == pytest.approx(365.2425)
    assert sum(float(row["fraction"]) for row in got["rows"]) == pytest.approx(1.0)


def test_table_75_rounds_where_chart_67_truncates():
    """Five of the eight differ by an arcminute, and our value is between
    every pair. D-80, from inside one example.
    """
    from hora.charts.book import longitudes

    chart = _annual()
    printed = longitudes(67)
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3, "Jupiter": 4,
           "Venus": 5, "Saturn": 6}
    disagree = 0
    for row in patyayini.TABLE_75:
        body = str(row["body"])
        ours = (chart.lagna_longitude if body == "Lagna"
                else chart.positions[ids[body]].longitude) % 30
        short = {"Mercury": "Merc", "Jupiter": "Jup", "Venus": "Ven",
                 "Saturn": "Sat", "Lagna": "Asc"}
        diagram = printed[short.get(body, body)] % 30
        table = _minutes(str(row["krisamsa"]))
        assert int(ours * 60) % 60 == round(diagram * 60) % 60, body
        assert round(ours * 60) % 60 == round(table * 60) % 60, body
        if abs(table - diagram) > 1e-9:
            disagree += 1
            assert diagram < ours < table, body
    assert disagree == 5
    assert "truncates to the diagram and" in (
        patyayini.TABLE_75_ROUNDS_WHERE_CHART_67_TRUNCATES)


def test_the_two_dasa_spans_the_section_states():
    """Venus June 1-26, Mercury June 26 - Aug 13, and the marriage inside
    Mercury's.
    """
    import swisseph as swe

    got = _patyayini()
    rows = {str(row["body"]): row for row in got["rows"]}
    assert float(rows["Venus"]["days"]) == pytest.approx(25.0, abs=0.1)
    assert float(rows["Mercury"]["days"]) == pytest.approx(48.0, abs=0.3)

    def day(jd):
        year, month, dom, _ = swe.revjul(jd + 5.5 / 24.0)
        return int(year), int(month), int(dom)

    assert day(float(rows["Venus"]["from_jd"])) == (1993, 6, 1)
    assert day(float(rows["Venus"]["to_jd"])) == (1993, 6, 26)
    assert day(float(rows["Mercury"]["to_jd"])) == (1993, 8, 13)

    wedding = from_local(1993, 7, 24, 12, 0, 0.0, utc_offset_hours=5.5).jd_ut
    assert (float(rows["Mercury"]["from_jd"]) < wedding
            < float(rows["Mercury"]["to_jd"]))


def test_the_four_worked_antardasas_in_venus_dasa_reproduce():
    got = _patyayini()
    legs = patyayini.antardasas(got, "Venus")
    assert [leg["antardasa"] for leg in legs[:4]] == [
        "Venus", "Mercury", "Moon", "Saturn"]
    for leg, want in zip(legs[:4], patyayini.VENUS_ANTARDASAS, strict=False):
        assert leg["antardasa"] == want["antardasa"]
        assert leg["days"] == pytest.approx(float(want["days"]), abs=0.11)
    # And the antardasas partition the dasa exactly.
    rows = {str(row["body"]): row for row in got["rows"]}
    assert sum(leg["days"] for leg in legs) == pytest.approx(
        float(rows["Venus"]["days"]))
    assert "sum to its length" in patyayini.THE_ANTARDASAS_PARTITION_THE_DASA_EXACTLY


def test_the_first_antardasa_is_the_dasa_lord_in_every_dasa():
    got = _patyayini()
    for body in got["order"]:
        legs = patyayini.antardasas(got, body)
        assert legs[0]["antardasa"] == body
        assert [leg["antardasa"] for leg in legs] == sorted(
            got["order"], key=lambda n: (list(got["order"]).index(n)
                                         - list(got["order"]).index(body)) % 8)


def test_the_shortest_dasa_is_the_least_robust_to_the_books_rounding():
    got = _patyayini()
    rows = {str(row["body"]): row for row in got["rows"]}
    printed = {str(row["body"]): float(row["days"]) for row in patyayini.TABLE_75}
    gaps = {name: abs(float(rows[name]["days"]) - printed[name])
            for name in printed}
    assert max(gaps, key=lambda n: gaps[n] / printed[n]) == "Moon"
    assert printed["Moon"] == 0.51
    assert float(rows["Moon"]["days"]) == pytest.approx(0.40, abs=0.02)
    for name in printed:
        if name != "Moon":
            assert gaps[name] < 0.25, name
    assert "No other dasa moves by more than" in (
        patyayini.THE_SHORTEST_DASA_IS_THE_LEAST_ROBUST)


def test_the_first_patyamsa_is_the_whole_krisamsa():
    got = _patyayini()
    first = got["rows"][0]
    assert first["patyamsa"] == pytest.approx(first["krisamsa"])
    assert patyayini.TABLE_75[0]["krisamsa"] == patyayini.TABLE_75[0]["patyamsa"]
    assert "both columns" in patyayini.THE_FIRST_PATYAMSA_IS_THE_WHOLE_KRISAMSA


def test_a_tie_gives_a_dasa_of_zero_days():
    got = patyayini.patyayini_dasa(
        lagna=15.0, longitudes={0: 45.0, 1: 75.0, 2: 105.0, 3: 135.0,
                                4: 165.0, 5: 195.0, 6: 225.0})
    assert got["ties"]
    zero = [row for row in got["rows"] if row["days"] == 0.0]
    assert zero
    assert "no length" in patyayini.A_TIE_GIVES_A_DASA_OF_ZERO_DAYS


def test_the_divisor_is_the_calendar_year_not_the_sidereal_one():
    """The dasas run 365.2425 days; the year between two varsha praveshes is
    a sidereal year, about 20 minutes longer.
    """
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_BIRTH, _PLACE, _SETTINGS).positions[0].longitude

    def sun(jd):
        return eph.positions(jd, [0])[0].longitude

    this_year = varsha_pravesh(sun, natal_sun, _BIRTH.jd_ut, 22)["jd"]
    next_year = varsha_pravesh(sun, natal_sun, _BIRTH.jd_ut, 23)["jd"]
    real = next_year - this_year
    assert real == pytest.approx(365.256, abs=0.01)
    shortfall = (real - patyayini.PATYAYINI_YEAR_DAYS) * 24 * 60
    assert 15 < shortfall < 30                    # about twenty minutes
    assert "twenty minutes early" in (
        patyayini.THE_DIVISOR_IS_THE_CALENDAR_YEAR_NOT_THE_REAL_ONE)


def test_patyayini_needs_all_seven_grahas_and_uses_no_node():
    from hora.core.const import Graha

    assert int(Graha.RAHU) not in patyayini.PATYAYINI_BODIES
    assert int(Graha.KETU) not in patyayini.PATYAYINI_BODIES
    assert len(patyayini.PATYAYINI_BODIES) == 7
    with pytest.raises(patyayini.PatyayiniError, match="missing"):
        patyayini.patyayini_dasa(lagna=0.0, longitudes={0: 1.0})


# --------------------------------------------------------------------------
# §30.2's "Timing of marriage" — why Mercury
# --------------------------------------------------------------------------


def _pancha_vargeeya_bounds():
    """Each graha's pancha vargeeya bala as a range, because §28.4 prices no
    neutral grade. OI-153.
    """
    from hora.charts.vargas import d3_drekkana, d9_navamsa
    from hora.core.const import RASI_LORD
    from hora.core.constants.graha import NATURAL_RELATION
    from hora.tajaka.panchavargeeya import (
        NAVAMSA_BALA_UNITS,
        drekkana_bala,
        hadda_bala,
        hadda_lord,
        kshetra_bala,
        navamsa_bala,
        uchcha_bala,
    )

    chart = _annual()
    names = {2: "friend", 1: "neutral", 0: "enemy"}

    def relation(graha, lord):
        return ("own" if lord == graha
                else names[int(NATURAL_RELATION[graha][lord])])

    best = max(v for v in NAVAMSA_BALA_UNITS.values() if v is not None)
    out = {}
    for graha in range(7):
        place = chart.positions[graha].longitude
        parts = {
            "kshetra": kshetra_bala(
                relation(graha, int(RASI_LORD[int(place // 30)]))).get("units"),
            "uchcha": uchcha_bala(graha, place)["units"],
            "hadda": hadda_bala(
                relation(graha, int(hadda_lord(place)["lord"]))).get("units"),
            "drekkana": drekkana_bala(relation(
                graha, int(RASI_LORD[int(d3_drekkana(place).sign)]))).get("units"),
            "navamsa": navamsa_bala(relation(
                graha, int(RASI_LORD[int(d9_navamsa(place).sign)]))).get("units"),
        }
        known = sum(v for v in parts.values() if v is not None)
        unpriced = [k for k, v in parts.items() if v is None]
        out[graha] = (known / 4.0, (known + best * len(unpriced)) / 4.0,
                      tuple(unpriced))
    return out


def test_the_five_reasons_are_recorded_and_four_are_checked_here():
    numbers = [row["number"] for row in example.WHY_MERCURY_GAVE_MARRIAGE]
    assert numbers == [1, 2, 3, 4, 5]
    holds = [row["holds"] for row in example.WHY_MERCURY_GAVE_MARRIAGE]
    assert holds == [True, True, None, True, True]      # (3) is OI-156


def test_mercury_is_very_strong_whatever_oi_153_decides():
    """Own in four of five sources; only his navamsa lord is a neutral."""
    from hora.core.const import Graha
    from hora.tajaka.panchavargeeya import pancha_vargeeya_grade

    bounds = _pancha_vargeeya_bounds()
    low, high, unpriced = bounds[int(Graha.MERCURY)]
    assert unpriced == ("navamsa",)
    assert low == pytest.approx(15.97, abs=0.02)
    assert high == pytest.approx(17.22, abs=0.02)
    assert pancha_vargeeya_grade(low) == pancha_vargeeya_grade(high) == (
        "very strong")

    # And highest in the chart under either bound.
    others = [bounds[g][1] for g in range(7) if g != int(Graha.MERCURY)]
    assert low > max(others)
    assert "both beat every other planet" in (
        example.MERCURY_IS_VERY_STRONG_WHATEVER_OI_153_DECIDES)


def test_mercury_aspects_the_vivaha_saham_within_three_degrees():
    from hora.core.const import Graha
    from hora.tajaka.aspects import aspect_on_house
    from hora.tajaka.sahams import sahams

    longitudes, lagna = _annual_longitudes()
    saham = sahams(longitudes=longitudes, lagna=lagna,
                   daytime=True)["Vivaha"]["longitude"]
    mercury = longitudes["Mercury"]
    house = (int(saham // 30) - int(mercury // 30)) % 12 + 1
    assert house == 7
    assert aspect_on_house(house)["name"] == "Opposition"
    exact = (mercury + 30.0 * (house - 1)) % 360.0
    gap = abs(((saham - exact + 180) % 360) - 180)
    assert gap == pytest.approx(2 + 25 / 60, abs=0.02)
    assert gap < 3.0
    from hora.tajaka.aspects import deeptamsa

    assert gap < deeptamsa(int(Graha.MERCURY))
    assert "2 degrees 25 minutes" in (
        example.MERCURY_ASPECTS_THE_SAHAM_BY_TWO_AND_A_HALF_DEGREES)


def test_28_6s_cascade_gives_mars_where_the_section_says_mercury():
    """OI-156's first worked case, and it disagrees with our reading."""
    from hora.core.const import Graha
    from hora.tajaka.varsheswara import varsheswara

    chart = _annual()
    bounds = _pancha_vargeeya_bounds()
    got = varsheswara(
        sun_rasi=int(chart.positions[0].longitude // 30),
        moon_rasi=int(chart.positions[1].longitude // 30),
        natal_lagna_rasi=0, muntha_rasi=9,
        annual_lagna_rasi=chart.lagna_rasi, daytime=True,
        rasis={g: int(chart.positions[g].longitude // 30) for g in range(7)},
        pancha_vargeeya={g: bounds[g][0] for g in range(7)})
    assert got["lord_name"] == "Mars"
    assert [row["graha"] for row in got["candidates"]] == [
        int(Graha.VENUS), int(Graha.MARS), int(Graha.SATURN),
        int(Graha.MERCURY), int(Graha.MOON)]
    assert "Section 30.2 says Mercury is varsheswara" in (
        example.EXAMPLE_122_RUNS_28_6S_CASCADE_AND_DISAGREES_WITH_US)


def test_two_of_the_three_readings_give_the_books_mercury():
    from hora.core.const import Graha
    from hora.tajaka.aspects import aspect_on_house

    chart = _annual()
    bounds = _pancha_vargeeya_bounds()
    rasis = {g: int(chart.positions[g].longitude // 30) for g in range(7)}
    lagna_rasi = chart.lagna_rasi
    pool = {}
    for graha in (int(Graha.VENUS), int(Graha.MARS), int(Graha.SATURN),
                  int(Graha.MERCURY), int(Graha.MOON)):
        house = (lagna_rasi - rasis[graha]) % 12 + 1
        aspect = aspect_on_house(house)
        pool[graha] = {"aspect_nature": None if aspect is None
                       else aspect["nature"], "bala": bounds[graha][0]}

    got = example.varsheswara_readings(candidates_with=pool)
    assert got["by_benefic_aspect"] == "Mars"
    assert got["by_any_aspect"] == "Mercury"
    assert got["by_very_strong_bala"] == "Mercury"

    matching = [row for row in example.VARSHESWARA_READINGS
                if row["matches_the_book"]]
    assert len(matching) == 2
    assert got["undecided"] is not None


def test_28_6_is_not_changed_on_the_strength_of_one_example():
    """`varsheswara` still returns what §28.6's procedure says. OI-156."""
    import inspect

    from hora.tajaka import varsheswara as module

    source = inspect.getsource(module)
    assert "benefic aspect on lagna" in source
    assert "Example 122" not in source
    assert "OI-156" in inspect.getsource(example)


# --------------------------------------------------------------------------
# §30.3 Mudda dasa (Varsha Vimsottari dasa)
# --------------------------------------------------------------------------

from hora.dasha.annual import mudda


def _natal_moon():
    return compute_chart(_BIRTH, _PLACE, _SETTINGS).positions[1].longitude


def _mudda():
    return mudda.mudda_dasa(moon_longitude=_natal_moon(), completed_years=21,
                            start_jd=_PRAVESH.jd_ut)


def test_the_mudda_rules_are_transcribed():
    assert "120 years compressed to a solar year" in mudda.MUDDA_LENGTH_RULE
    assert "Sun moves by exactly 1 degree" in mudda.MUDDA_LENGTH_RULE
    assert "6 x 3 = 18 days" in mudda.MUDDA_LENGTH_RULE
    assert "one constellation per year" in mudda.MUDDA_ORDER_RULE
    assert "Remainder of 0 is equivalent to 9" in mudda.MUDDA_ORDER_RULE
    assert "yet to be traversed" in mudda.MUDDA_BALANCE_RULE
    assert mudda.MUDDA_YEAR_DAYS == 360
    assert mudda.MUDDA_MULTIPLIER == 3


def test_table_76_is_three_times_vimsottari_and_sums_to_360():
    from hora.core.const import GRAHA_NAMES
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    spec = NAKSHATRA_DASHA_SYSTEMS["vimshottari"]
    years = {str(GRAHA_NAMES[int(lord)]): y
             for lord, y in zip(spec.order, spec.years, strict=True)}
    for name, days in mudda.TABLE_76:
        assert days == years[name] * 3, name
        assert mudda.mudda_days(
            next(g for g in range(9) if str(GRAHA_NAMES[g]) == name)) == days
    assert sum(days for _, days in mudda.TABLE_76) == 360
    assert spec.total_years * 3 == 360
    assert "sum to 360" in mudda.TABLE_76_IS_THREE_TIMES_VIMSOTTARI


def test_the_numbering_is_the_vimsottari_cycle_started_from_the_sun():
    from hora.core.const import GRAHA_NAMES, Graha
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    spec = NAKSHATRA_DASHA_SYSTEMS["vimshottari"]
    cycle = [int(lord) for lord in spec.order]
    start = cycle.index(int(Graha.SUN))
    assert list(mudda.MUDDA_NUMBERS) == cycle[start:] + cycle[:start]
    assert [str(GRAHA_NAMES[g]) for g in mudda.MUDDA_NUMBERS] == [
        name for name, _ in mudda.TABLE_76]
    assert mudda.mudda_number(int(Graha.SUN)) == 1
    assert mudda.mudda_number(int(Graha.VENUS)) == 9
    assert mudda.mudda_number(int(Graha.KETU)) == 8


def test_the_natal_moon_is_in_uttarashadha_with_the_sun_as_lord():
    from hora.core.const import GRAHA_NAMES, Graha

    got = mudda.natal_nakshatra_lord(_natal_moon())
    assert got["nakshatra_name"] == "Uttara Ashadha"
    assert got["lord"] == int(Graha.SUN)
    assert str(GRAHA_NAMES[got["lord"]]) == "Sun"
    assert got["yet_to_traverse"] == pytest.approx(0.79, abs=0.005)


def test_the_first_dasa_lord_is_rahu_by_both_methods():
    """1 + 21 = 22, 22 mod 9 = 4, which is Rahu; and Uttarashadha progressed
    21 constellations is Swati, which is Rahu's.
    """
    from hora.core.const import Graha

    got = mudda.first_dasa_lord(moon_longitude=_natal_moon(),
                                completed_years=21)
    assert got["natal_lord_number"] == 1
    assert got["sum"] == 22
    assert got["remainder"] == 4
    assert got["by_arithmetic"] == int(Graha.RAHU)
    assert got["progressed_nakshatra_name"] == "Swati"
    assert got["by_progression"] == int(Graha.RAHU)
    assert got["agree"] is True


def test_the_shortcut_is_exact_not_approximate():
    """27 is a multiple of 9, so progressing and the arithmetic are the same
    operation. Checked over every constellation and forty years.
    """
    for index in range(27):
        longitude = index * mudda.NAKSHATRA_SPAN + 5.0
        for years in range(40):
            got = mudda.first_dasa_lord(moon_longitude=longitude,
                                        completed_years=years)
            assert got["agree"] is True, (index, years)
    assert "not an approximation" in mudda.THE_SHORTCUT_IS_EXACT_NOT_APPROXIMATE


def test_a_remainder_of_zero_shows_venus():
    from hora.core.const import Graha

    # Venus is number 9, so nine completed years from a Venus-lorded
    # constellation gives 9 + 9 = 18, a remainder of 0.
    venus_star = 1 * mudda.NAKSHATRA_SPAN + 5.0          # Bharani, Venus's
    got = mudda.first_dasa_lord(moon_longitude=venus_star, completed_years=9)
    assert got["natal_lord_number"] == 9
    assert got["remainder"] == 0
    assert got["by_arithmetic"] == int(Graha.VENUS)
    assert got["agree"] is True
    assert "Remainder of 0 is equivalent to 9" in mudda.MUDDA_ORDER_RULE


def test_rahus_balance_and_the_july_14_date():
    """0.79 x 54 = 42.66 solar days, and the section's own date counts them as
    calendar days.
    """
    import swisseph as swe

    from hora.core.const import Graha

    got = _mudda()
    first = got["rows"][0]
    assert first["graha"] == int(Graha.RAHU)
    assert first["full_days"] == 54
    assert first["is_balance"] is True
    assert first["days"] == pytest.approx(42.66, abs=0.05)

    year, month, day, _ = swe.revjul(float(first["to_jd"]) + 5.5 / 24.0)
    assert (int(year), int(month), int(day)) == (1993, 7, 14)


def test_jupiter_dasa_holds_the_marriage():
    import swisseph as swe

    from hora.core.const import Graha

    got = _mudda()
    jupiter = got["rows"][1]
    assert jupiter["graha"] == int(Graha.JUPITER)
    assert jupiter["days"] == 48.0
    wedding = from_local(1993, 7, 24, 12, 0, 0.0, utc_offset_hours=5.5).jd_ut
    assert float(jupiter["from_jd"]) < wedding < float(jupiter["to_jd"])
    year, month, day, _ = swe.revjul(float(jupiter["to_jd"]) + 5.5 / 24.0)
    assert (int(year), int(month), int(day)) == (1993, 8, 31)


def test_the_dates_use_calendar_days_not_the_solar_days_defined():
    """In true solar days Rahu's balance would end on 16 July. OI-175."""
    from hora.core.ephemeris import get_ephemeris

    eph = get_ephemeris(_SETTINGS)
    start = _PRAVESH.jd_ut
    balance = float(_mudda()["rows"][0]["days"])
    at_start = eph.positions(start, [0])[0].longitude

    low, high = start, start + 60.0
    for _ in range(60):
        middle = (low + high) / 2.0
        moved = (eph.positions(middle, [0])[0].longitude - at_start) % 360.0
        if moved < balance:
            low = middle
        else:
            high = middle
    in_solar_days = (low + high) / 2.0 - start
    assert in_solar_days == pytest.approx(44.7, abs=0.2)
    assert in_solar_days - balance > 1.9              # two days later
    assert "In solar days it would be 16 July" in (
        mudda.THE_DATES_USE_CALENDAR_DAYS_NOT_THE_SOLAR_DAYS_DEFINED)


def test_the_two_dasas_use_two_different_years():
    from hora.dasha.annual import patyayini

    assert patyayini.PATYAYINI_YEAR_DAYS == 365.2425
    assert mudda.MUDDA_YEAR_DAYS == 360
    assert patyayini.PATYAYINI_YEAR_DAYS - mudda.MUDDA_YEAR_DAYS == (
        pytest.approx(5.2425))
    assert "all different" in mudda.THE_TWO_DASAS_USE_TWO_DIFFERENT_YEARS


def test_the_nine_dasas_from_a_balance_do_not_fill_the_cycle():
    """The opening dasa is only its balance, so the nine total 360 less the
    part already spent, and the sequence has to wrap.
    """
    got = _mudda()
    spent = 54 * (1.0 - got["balance_fraction"])
    assert got["total_days"] == pytest.approx(360.0 - spent, abs=1e-9)
    assert got["total_days"] == pytest.approx(348.69, abs=0.05)
    assert len(got["rows"]) == 9
    assert sum(row["full_days"] for row in got["rows"]) == 360


def test_the_annual_chart_contributes_only_the_start_date():
    """Seed and balance both come from the natal Moon, so a different annual
    chart for the same nativity and year changes nothing but the start.
    """
    here = mudda.mudda_dasa(moon_longitude=_natal_moon(), completed_years=21,
                            start_jd=_PRAVESH.jd_ut)
    elsewhere = mudda.mudda_dasa(moon_longitude=_natal_moon(),
                                 completed_years=21,
                                 start_jd=_PRAVESH.jd_ut + 3.0)
    assert here["order"] == elsewhere["order"]
    assert here["balance_fraction"] == elsewhere["balance_fraction"]
    assert [row["days"] for row in here["rows"]] == [
        row["days"] for row in elsewhere["rows"]]
    assert "supplies the start date alone" in (
        mudda.THE_ANNUAL_CHART_CONTRIBUTES_ONLY_THE_START_DATE)


def test_30_3s_natal_moon_is_cited_an_arcminute_high():
    """29 Sg 27 in Chart 18, 29 Sg 28 in §30.3's text, 29 Sg 27.49 in ours —
    which truncates and rounds to 27 alike, so this is not D-80's convention.
    """
    from hora.charts.book import chart, longitudes

    ours = _natal_moon() % 30
    diagram = longitudes(18)["Moon"] % 30
    assert chart(18)["longitudes"]["Moon"] == "29 Sg 27"
    arcminutes = (ours % 1) * 60
    assert int(ours) == int(diagram) == 29
    assert int(arcminutes) == round(arcminutes) == 27
    assert "not the convention D-80 records" in (
        mudda.THE_NATAL_MOON_IS_CITED_AN_ARCMINUTE_HIGH)

    # And nothing turns on it: the balance is 0.79 under either figure.
    ours_left = mudda.natal_nakshatra_lord(_natal_moon())["yet_to_traverse"]
    theirs = 240.0 + 29.0 + 28.0 / 60.0
    theirs_left = mudda.natal_nakshatra_lord(theirs)["yet_to_traverse"]
    assert round(ours_left, 2) == round(theirs_left, 2) == 0.79


def test_the_marriage_reading_repeats_the_setups_own_facts():
    """"Jupiter is 7th lord and vivaha saham lord in rasi chart. He is in
    lagna. In navamsa, he is lagna lord and occupies the 2nd with Venus."
    """
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import GRAHA_NAMES, RASI_LORD, Graha

    chart = _annual()
    assert int(chart.positions[int(Graha.JUPITER)].longitude // 30) == (
        chart.lagna_rasi)
    seventh = (chart.lagna_rasi + 6) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[seventh])]) == "Jupiter"

    nav_lagna = int(d9_navamsa(chart.lagna_longitude).sign)
    assert str(GRAHA_NAMES[int(RASI_LORD[nav_lagna])]) == "Jupiter"
    jupiter = int(d9_navamsa(chart.positions[int(Graha.JUPITER)].longitude).sign)
    venus = int(d9_navamsa(chart.positions[int(Graha.VENUS)].longitude).sign)
    assert jupiter == venus
    assert (jupiter - nav_lagna) % 12 + 1 == 2


# --------------------------------------------------------------------------
# §30.4 Varsha Narayana dasa
# --------------------------------------------------------------------------

from hora.dasha.annual import varsha_narayana as vn


def _navamsa_longitudes():
    """Navamsa positions carrying the degree inside the navamsa sign."""
    from hora.charts.vargas import d9_navamsa

    chart = _annual()
    out = {}
    for graha in range(9):
        place = chart.positions[graha].longitude
        out[graha] = (int(d9_navamsa(place).sign) * 30.0
                      + (place % (30 / 9)) * 9)
    return out


def test_the_rules_and_footnote_88_are_transcribed():
    assert "compressed from 120 years to 360 solar days" in vn.DURATION_RULE
    assert "Sun moves by (3 x n) degrees" in vn.DURATION_RULE
    assert "we take muntha as lagna" in vn.ORDER_RULE
    assert "link between the natal chart and the Tajaka chart" in vn.ORDER_RULE
    assert "12 x 12 = 144 years" in vn.FOOTNOTE_88
    assert "paramayush of human beings is 120 years" in vn.FOOTNOTE_88
    assert vn.VARSHA_NARAYANA_MULTIPLIER == 3
    assert vn.VARSHA_NARAYANA_YEAR_DAYS == 360


def test_footnote_88_answers_oi_174():
    """§30.1's 120 is deliberate, and the 144 behind it is the book's own."""
    assert intro.narayana_full_cycle_years() == 144
    assert "12 x 12 = 144" in vn.FOOTNOTE_88
    assert "only the first 120" in vn.FOOTNOTE_88
    assert "deliberate" in vn.FOOTNOTE_88_ANSWERS_THE_144
    assert 120 * vn.VARSHA_NARAYANA_MULTIPLIER == vn.VARSHA_NARAYANA_YEAR_DAYS


def test_the_progressed_lagna_is_the_muntha():
    """§28.1's rule and §30.4's give the same rasi in every chart and year."""
    from hora.tajaka.muntha import muntha_rasi

    for natal in range(12):
        for year in range(1, 61):
            assert vn.progressed_lagna(natal, year)["rasi"] == int(
                muntha_rasi(natal, year)["rasi"]), (natal, year)
    got = vn.progressed_lagna(0, 22)
    assert got["house_from_natal_lagna"] == 10
    assert got["rasi_name"] == "Capricorn"
    assert "the same rasi in every chart" in vn.THE_PROGRESSED_LAGNA_IS_THE_MUNTHA


def test_the_ninth_from_the_muntha_is_virgo_owned_by_mercury():
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha

    muntha = vn.progressed_lagna(0, 22)["rasi"]
    ninth = (muntha + 8) % 12
    assert RASI_ABBR[ninth] == "Vi"
    assert str(GRAHA_NAMES[int(RASI_LORD[ninth])]) == "Mercury"

    chart = _annual()
    mercury = int(d9_navamsa(chart.positions[int(Graha.MERCURY)].longitude).sign)
    assert RASI_ABBR[mercury] == "Sc"


def test_scorpio_is_stronger_than_taurus():
    """The seed choice, computed from §15.5 rather than taken on trust."""
    from hora.charts.rasi_strength import stronger

    verdict = stronger(7, 1, _navamsa_longitudes())
    assert verdict.winner == 7                          # Scorpio


def test_both_dasa_orders_reproduce_and_saturn_decides():
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import progression

    normal = progression(7, occupants=set())
    assert list(normal.sign_names[:6]) == [
        "Scorpio", "Gemini", "Capricorn", "Leo", "Pisces", "Libra"]
    assert normal.movement == "sixth"

    with_saturn = progression(7, occupants={int(Graha.SATURN)})
    assert list(with_saturn.sign_names[:6]) == [
        "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces", "Aries"]
    assert with_saturn.exception == "Saturn"
    assert "Both come back exactly" in vn.BOTH_ORDERS_REPRODUCE_AND_SATURN_DECIDES


def test_saturn_really_is_in_scorpio_in_the_navamsa():
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import RASI_ABBR, Graha

    chart = _annual()
    saturn = int(d9_navamsa(chart.positions[int(Graha.SATURN)].longitude).sign)
    assert RASI_ABBR[saturn] == "Sc"


def test_the_five_dasa_lengths_reproduce_and_scorpio_needs_ketu():
    """Sc 7, Sg 4, Cp 2, Aq 3, Pi 11 — and Scorpio's 7 is Ketu's figure."""
    from hora.charts.colord import stronger as co_lord
    from hora.core.const import RASI_ABBR, RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_length

    navamsa = {g: int(place // 30) for g, place in _navamsa_longitudes().items()}
    want = {"Sc": 7, "Sg": 4, "Cp": 2, "Aq": 3, "Pi": 11}
    for abbr, years in want.items():
        rasi = RASI_ABBR.index(abbr)
        lord = (int(Graha.KETU) if abbr == "Sc" else int(RASI_LORD[rasi]))
        assert dasa_length(rasi=rasi, lord=lord,
                           lord_sign=navamsa[lord]).years == years, abbr

    # Mars, the other co-lord, would give 3 — so the printed 7 fixes Ketu.
    assert dasa_length(rasi=7, lord=int(Graha.MARS),
                       lord_sign=navamsa[int(Graha.MARS)]).years == 3
    # And §15.5.1's own comparison picks Ketu independently.
    assert co_lord(7, _navamsa_longitudes()).winner == int(Graha.KETU)
    assert "makes Ketu the stronger" in vn.SCORPIOS_CO_LORD_HAS_TO_BE_KETU_HERE


def test_the_compressed_lengths_are_three_times_the_years():
    assert [vn.compressed_days(y) for y in (7, 4, 2, 3)] == [21, 12, 6, 9]
    assert sum(vn.compressed_days(y) for y in (7, 4, 2, 3)) == 48
    assert vn.compressed_days(11) == 33


def test_pisces_dasa_holds_the_marriage_under_every_reading():
    """19 July as calendar days, 21 July as solar days, 20 July printed — and
    24 July is inside Pisces dasa on all three.
    """
    from hora.core.ephemeris import get_ephemeris

    eph = get_ephemeris(_SETTINGS)
    start = _PRAVESH.jd_ut
    at_start = eph.positions(start, [0])[0].longitude

    def after(degrees):
        low, high = start, start + 200.0
        for _ in range(70):
            middle = (low + high) / 2.0
            moved = (eph.positions(middle, [0])[0].longitude - at_start) % 360.0
            if moved < degrees:
                low = middle
            else:
                high = middle
        return (low + high) / 2.0

    wedding = from_local(1993, 7, 24, 12, 0, 0.0, utc_offset_hours=5.5).jd_ut
    for opens, closes in ((start + 48, start + 81),          # calendar days
                          (after(48), after(81))):           # solar days
        assert opens < wedding < closes
    assert "under every reading" not in vn.DURATION_RULE
    assert "one day from each" in vn.THE_DATE_FITS_NEITHER_READING_OF_A_SOLAR_DAY


def test_the_printed_date_sits_between_the_two_readings():
    import swisseph as swe

    from hora.core.ephemeris import get_ephemeris

    eph = get_ephemeris(_SETTINGS)
    start = _PRAVESH.jd_ut
    at_start = eph.positions(start, [0])[0].longitude
    low, high = start, start + 120.0
    for _ in range(70):
        middle = (low + high) / 2.0
        moved = (eph.positions(middle, [0])[0].longitude - at_start) % 360.0
        if moved < 48.0:
            low = middle
        else:
            high = middle

    def day(jd):
        year, month, dom, _ = swe.revjul(jd + 5.5 / 24.0)
        return int(year), int(month), int(dom)

    assert day(start + 48.0) == (1993, 7, 19)          # calendar days
    assert day((low + high) / 2.0) == (1993, 7, 21)    # solar days
    # The section prints 20 July, between the two.


def test_pisces_holds_the_navamsa_lagna_and_takes_argala_from_the_second():
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha

    chart = _annual()
    nav_lagna = int(d9_navamsa(chart.lagna_longitude).sign)
    assert RASI_ABBR[nav_lagna] == "Pi"
    assert str(GRAHA_NAMES[int(RASI_LORD[nav_lagna])]) == "Jupiter"

    for graha in (Graha.JUPITER, Graha.VENUS):
        where = int(d9_navamsa(chart.positions[int(graha)].longitude).sign)
        assert (where - nav_lagna) % 12 + 1 == 2       # the 2nd gives argala


def test_the_two_compressed_dasas_progress_the_same_way():
    assert "one constellation per year" in mudda.MUDDA_ORDER_RULE
    assert "one rasi per year" in vn.ORDER_RULE
    assert "Just as we progress Moon by one constellation per year" in (
        vn.ORDER_RULE)
    assert "Neither reads the annual chart" in (
        vn.THE_TWO_COMPRESSED_DASAS_PROGRESS_THE_SAME_WAY)


def test_the_book_ranks_its_three_dasas():
    assert "Varsha Narayana dasa is, however, the best" in vn.THE_BOOKS_OWN_RANKING
    assert "Patyayini dasa gives better results than Mudda" in (
        vn.THE_BOOKS_OWN_RANKING)
    assert "argues for it nowhere" in (
        vn.THE_BOOK_RANKS_ITS_THREE_DASAS_AND_GIVES_NO_REASON)


# --------------------------------------------------------------------------
# Exercise 48
# --------------------------------------------------------------------------

from hora.dasha.annual import exercise_48 as ex48

_EX48_BIRTH = from_local(**ex48.BIRTH)
_EX48_PRAVESH = from_local(**ex48.VARSHA_PRAVESH)
_EX48_PLACE = Place(name="Exercise 48", **ex48.PLACE)
_EX48_WEDDING = from_local(1993, 8, 1, 12, 0, 0.0, utc_offset_hours=5.5).jd_ut


def _ex48_annual():
    return compute_chart(_EX48_PRAVESH, _EX48_PLACE, _SETTINGS)


def _ex48_navamsa():
    """Navamsa positions carrying the degree inside the navamsa sign."""
    from hora.charts.vargas import d9_navamsa

    chart = _ex48_annual()
    return {g: int(d9_navamsa(chart.positions[g].longitude).sign) * 30.0
            + (chart.positions[g].longitude % (30 / 9)) * 9 for g in range(9)}


def test_exercise_48_and_its_answer_are_transcribed():
    assert "born on 4th April 1970 at 5:50 pm" in ex48.EXERCISE_48
    assert "got married on 1st August 1993" in ex48.EXERCISE_48
    assert "navamsa lagna's dasa as per varsha Narayana dasa of navamsa" in (
        ex48.EXERCISE_48)
    assert "lagna/7th lord in rasi/navamsa" in ex48.EXERCISE_48
    assert ex48.EXERCISE_48_ANSWER.startswith("Try yourself.")
    assert "3:19:03 pm (IST)" in ex48.EXERCISE_48_ANSWER
    assert ex48.ANNUAL_YEAR == ex48.COMPLETED_YEARS + 1


def test_the_varsha_pravesh_reproduces_to_eleven_seconds():
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                              _SETTINGS).positions[0].longitude
    got = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                         natal_sun, _EX48_BIRTH.jd_ut, ex48.ANNUAL_YEAR)
    assert got["found"] is True
    seconds = (got["jd"] - _EX48_PRAVESH.jd_ut) * 86400.0
    assert 0.0 < seconds < 12.0
    assert "10.6 seconds" in (
        ex48.THE_VARSHA_PRAVESH_REPRODUCES_TO_ELEVEN_SECONDS)


def test_the_four_qualifying_lords_are_four_different_planets():
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD

    chart = _ex48_annual()
    nav_lagna = int(d9_navamsa(chart.lagna_longitude).sign)
    assert RASI_ABBR[chart.lagna_rasi] == "Le"
    assert RASI_ABBR[nav_lagna] == "Ge"
    lords = {}
    for label, rasi in (("rasi lagna", chart.lagna_rasi),
                        ("rasi 7th", (chart.lagna_rasi + 6) % 12),
                        ("navamsa lagna", nav_lagna),
                        ("navamsa 7th", (nav_lagna + 6) % 12)):
        lords[label] = str(GRAHA_NAMES[int(RASI_LORD[rasi])])
    assert lords == {"rasi lagna": "Sun", "rasi 7th": "Saturn",
                     "navamsa lagna": "Mercury", "navamsa 7th": "Jupiter"}
    assert len(set(lords.values())) == 4
    assert "four distinct planets" in (
        ex48.THE_FOUR_QUALIFYING_LORDS_ARE_FOUR_DIFFERENT_PLANETS)


def test_the_navamsa_lagnas_dasa_is_running_at_the_marriage():
    """The first of the exercise's three verifications."""
    from hora.charts.colord import stronger as co_lord
    from hora.charts.rasi_strength import stronger as rasi_stronger
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import RASI_ABBR, RASI_LORD, Graha
    from hora.dasha.annual.varsha_narayana import (
        compressed_days,
        progressed_lagna,
    )
    from hora.dasha.rasi.narayana import dasa_length, progression

    chart = _ex48_annual()
    navamsa = _ex48_navamsa()
    signs = {g: int(place // 30) for g, place in navamsa.items()}
    nav_lagna = int(d9_navamsa(chart.lagna_longitude).sign)

    muntha = progressed_lagna(5, ex48.ANNUAL_YEAR)["rasi"]   # natal lagna Vi
    assert RASI_ABBR[muntha] == "Le"
    ninth_lord = int(RASI_LORD[(muntha + 8) % 12])
    assert ninth_lord == int(Graha.MARS)

    here = signs[ninth_lord]
    seed = rasi_stronger(here, (here + 6) % 12, navamsa).winner
    assert RASI_ABBR[seed] == "Ta"

    occupants = {g for g in range(9) if signs[g] == seed}
    order = progression(seed, occupants=occupants)
    assert order.exception is None
    assert list(order.sign_names[:8]) == [
        "Taurus", "Sagittarius", "Cancer", "Aquarius", "Virgo", "Aries",
        "Scorpio", "Gemini"]

    running = _EX48_PRAVESH.jd_ut
    at_wedding = None
    for rasi in order.signs:
        lord = (int(Graha.KETU) if rasi == 7
                and co_lord(7, navamsa).winner == int(Graha.KETU)
                else int(RASI_LORD[rasi]))
        days = compressed_days(
            dasa_length(rasi=rasi, lord=lord, lord_sign=signs[lord]).years)
        if running <= _EX48_WEDDING < running + days:
            at_wedding = rasi
        running += days
    assert at_wedding is not None
    assert at_wedding == nav_lagna
    assert RASI_ABBR[at_wedding] == "Ge"
    assert ex48.EXERCISE_48_VERDICTS[0]["running"] == "Gemini"
    assert ex48.EXERCISE_48_VERDICTS[0]["holds"] is True


def test_this_seed_takes_no_exception_where_example_122s_did():
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import progression

    signs = {g: int(place // 30) for g, place in _ex48_navamsa().items()}
    occupants = {g for g in range(9) if signs[g] == 1}       # Taurus
    assert occupants == {int(Graha.MARS), int(Graha.JUPITER)}
    assert progression(1, occupants=occupants).exception is None
    assert progression(7, occupants={int(Graha.SATURN)}).exception == "Saturn"
    assert "took the exception" in (
        ex48.THIS_SEED_TAKES_NO_EXCEPTION_WHERE_EXAMPLE_122S_DID)


def test_patyayinis_dasa_and_antardasa_qualify():
    """The dasa is the Lagna's own and the antardasa is the rasi 7th lord."""
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    chart = _ex48_annual()
    got = patyayini.patyayini_dasa(
        lagna=chart.lagna_longitude,
        longitudes={g: chart.positions[g].longitude for g in range(7)},
        start_jd=_EX48_PRAVESH.jd_ut)
    dasa = next(row for row in got["rows"]
                if row["from_jd"] <= _EX48_WEDDING < row["to_jd"])
    assert dasa["body"] == "Lagna"

    leg = next(l for l in patyayini.antardasas(got, "Lagna")
               if _EX48_PRAVESH.jd_ut + l["from_day"] <= _EX48_WEDDING
               < _EX48_PRAVESH.jd_ut + l["to_day"])
    assert leg["antardasa"] == "Saturn"
    seventh = (chart.lagna_rasi + 6) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[seventh])]) == "Saturn"

    verdict = ex48.EXERCISE_48_VERDICTS[1]
    assert verdict["running"] == "Lagna" and verdict["antardasa"] == "Saturn"
    assert verdict["holds"] is True


def test_the_phrase_means_the_lagna_itself():
    """Patyayini's answer settles the parse: only patyayini has a Lagna dasa.
    """
    assert "Lagna" in patyayini.patyayini_dasa(
        lagna=10.0,
        longitudes=dict.fromkeys(range(7), 20.0))["order"]
    assert "not the lagna lord" in ex48.THE_PHRASE_MEANS_THE_LAGNA_ITSELF


def test_muddas_dasa_and_antardasa_qualify():
    """Jupiter is the navamsa 7th lord and Saturn the rasi 7th lord."""
    from hora.core.const import GRAHA_NAMES, Graha

    natal_moon = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                               _SETTINGS).positions[1].longitude
    got = mudda.mudda_dasa(moon_longitude=natal_moon,
                           completed_years=ex48.COMPLETED_YEARS,
                           start_jd=_EX48_PRAVESH.jd_ut)
    seed = got["seed"]
    assert seed["natal"]["nakshatra_name"] == "Purva Bhadrapada"
    assert seed["natal_lord_number"] == 5                    # Jupiter
    assert seed["sum"] == 28 and seed["remainder"] == 1
    assert seed["lord"] == int(Graha.SUN)
    assert seed["agree"] is True

    dasa = next(row for row in got["rows"]
                if row["from_jd"] <= _EX48_WEDDING < row["to_jd"])
    assert dasa["graha"] == int(Graha.JUPITER)

    leg = next(l for l in mudda.mudda_antardasas(got, int(Graha.JUPITER))
               if l["from_jd"] <= _EX48_WEDDING < l["to_jd"])
    assert leg["antardasa"] == int(Graha.SATURN)
    assert str(GRAHA_NAMES[leg["antardasa"]]) == "Saturn"

    verdict = ex48.EXERCISE_48_VERDICTS[2]
    assert verdict["running"] == "Jupiter" and verdict["antardasa"] == "Saturn"
    assert verdict["holds"] is True


def test_the_mudda_antardasa_needed_a_rule_the_section_does_not_give():
    """§30.2 gave patyayini one; §30.3 gives mudda none. OI-176."""
    assert "First antardasa is the same as dasa" in str(
        patyayini.PATYAYINI_PROCEDURE[3]["text"])
    assert "antardasa" not in mudda.MUDDA_LENGTH_RULE.lower()
    assert "antardasa" not in mudda.MUDDA_ORDER_RULE.lower()
    assert "antardasa" not in mudda.MUDDA_BALANCE_RULE.lower()
    assert "no antardasa rule" in mudda.MUDDA_HAS_NO_ANTARDASA_RULE
    assert "satisfies the exercise" in (
        ex48.THE_MUDDA_ANTARDASA_NEEDED_A_RULE_THE_SECTION_DOES_NOT_GIVE)


def test_all_three_of_the_exercises_verifications_hold():
    assert [row["holds"] for row in ex48.EXERCISE_48_VERDICTS] == [
        True, True, True]
    assert [row["dasa"] for row in ex48.EXERCISE_48_VERDICTS] == [
        "Varsha Narayana of navamsa", "Patyayini", "Mudda"]


# --------------------------------------------------------------------------
# Example 123 and Chart 68
# --------------------------------------------------------------------------

from hora.dasha.annual import example_123 as ex123

_E123_PRAVESH = from_local(**ex123.VARSHA_PRAVESH)
_E123_TRIP = from_local(1991, 8, 15, 12, 0, 0.0, utc_offset_hours=5.5).jd_ut


def _e123_annual():
    return compute_chart(_E123_PRAVESH, _EX48_PLACE, _SETTINGS)


def _e123_d4():
    """D-4 positions carrying the degree inside the chaturthamsa sign."""
    from hora.charts.vargas import d4_chaturthamsa

    chart = _e123_annual()
    out = {g: int(d4_chaturthamsa(chart.positions[g].longitude).sign) * 30.0
           + (chart.positions[g].longitude % 7.5) * 4 for g in range(9)}
    return out, int(d4_chaturthamsa(chart.lagna_longitude).sign)


def test_example_123_is_transcribed():
    assert "went from India to US for his masters degree" in ex123.EXAMPLE_123
    assert "Varsha Narayana dasa of D-4" in ex123.EXAMPLE_123
    assert "3:05:33 am (IST)" in ex123.VARSHA_PRAVESH_DATA
    assert "Ar with two planets is stronger than Li" in ex123.THE_DASA_PARAGRAPH
    assert "Virgo dasa, Gemini antardasa" in ex123.THE_TIMING_PARAGRAPH
    assert ex123.CHART_NUMBER == 68
    assert ex123.ANNUAL_YEAR == 22


def test_chart_68_draws_a_varga_and_prints_the_rasi():
    from hora.charts.book import chart

    record = chart(68)
    assert "D4" in record["divisional"]
    assert record["longitudes"]["Asc"] == "27 Cp 20"        # the rasi lagna
    assert record["divisional"]["D4"]["Asc"] == "Li"        # the drawn lagna
    assert "Though rasi chart has lagna in Cp" in ex123.THE_DASA_PARAGRAPH
    assert "No other chart in the register" in (
        ex123.CHART_68_DRAWS_A_VARGA_AND_PRINTS_THE_RASI)


def test_the_closest_varsha_pravesh_in_the_book():
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                              _SETTINGS).positions[0].longitude
    got = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                         natal_sun, _EX48_BIRTH.jd_ut, ex123.ANNUAL_YEAR)
    seconds = (got["jd"] - _E123_PRAVESH.jd_ut) * 86400.0
    assert -3.0 < seconds < 0.0
    assert abs(seconds) < 3.0
    assert "2.3 seconds" in ex123.THE_CLOSEST_VARSHA_PRAVESH_IN_THE_BOOK


def test_chart_68s_longitudes_reproduce_within_an_arcminute():
    from hora.charts.book import longitudes

    chart = _e123_annual()
    printed = longitudes(68)
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    for name, index in ids.items():
        gap = (((chart.positions[index].longitude - printed[name] + 180) % 360)
               - 180) * 60
        assert 0.0 < gap < 1.1, (name, gap)
    lagna_gap = (((chart.lagna_longitude - printed["Asc"] + 180) % 360)
                 - 180) * 60
    assert 0.0 < lagna_gap < 1.0
    assert chart.positions[3].is_retrograde is True          # Merc (R)


def test_the_printed_moon_fits_our_instant_not_the_printed_one():
    """25 Sc 03.01 at the book's instant and 25 Sc 02.99 at ours."""
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                              _SETTINGS).positions[0].longitude
    solved = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                            natal_sun, _EX48_BIRTH.jd_ut, ex123.ANNUAL_YEAR)

    at_printed = eph.positions(_E123_PRAVESH.jd_ut, [1])[1].longitude
    at_solved = eph.positions(solved["jd"], [1])[1].longitude
    assert int((at_printed % 1) * 60) == 3
    assert int((at_solved % 1) * 60) == 2                    # what is printed
    assert abs(at_printed - at_solved) * 60 < 0.05
    assert "two hundredths of an arcminute" in (
        ex123.THE_PRINTED_MOON_FITS_OUR_INSTANT_NOT_THE_PRINTED_ONE)


def test_the_d4_reproduces_box_for_box():
    from hora.charts.book import chart as record
    from hora.core.const import RASI_ABBR

    d4, lagna = _e123_d4()
    drawn = record(68)["divisional"]["D4"]
    names = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
             "Sat": 6, "Rahu": 7, "Ketu": 8}
    for name, index in names.items():
        assert RASI_ABBR[int(d4[index] // 30)] == drawn[name], name
    assert RASI_ABBR[lagna] == drawn["Asc"] == "Li"


def test_the_three_house_claims_from_the_d4_lagna_hold():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha

    d4, lagna = _e123_d4()
    house = {g: (int(d4[g] // 30) - lagna) % 12 + 1 for g in d4}
    assert house[int(Graha.MERCURY)] == 7
    assert house[int(Graha.MARS)] == 9
    assert house[int(Graha.SUN)] == 12
    # Mercury owns the 9th and the 12th from Libra.
    for offset in (8, 11):
        assert str(GRAHA_NAMES[int(RASI_LORD[(lagna + offset) % 12])]) == (
            "Mercury")
    # Mars owns the 7th.
    assert str(GRAHA_NAMES[int(RASI_LORD[(lagna + 6) % 12])]) == "Mars"
    assert RASI_ABBR[(lagna + 11) % 12] == "Vi"
    assert RASI_ABBR[(lagna + 8) % 12] == "Ge"


def test_the_muntha_is_gemini_and_the_fourth_lord_is_mercury():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha
    from hora.dasha.annual.varsha_narayana import progressed_lagna

    muntha = progressed_lagna(5, ex123.ANNUAL_YEAR)["rasi"]  # natal lagna Vi
    assert RASI_ABBR[muntha] == "Ge"
    fourth = (muntha + 3) % 12
    assert RASI_ABBR[fourth] == "Vi"
    assert str(GRAHA_NAMES[int(RASI_LORD[fourth])]) == "Mercury"

    d4, _ = _e123_d4()
    assert RASI_ABBR[int(d4[int(Graha.MERCURY)] // 30)] == "Ar"


def test_the_seed_is_decided_by_counting_planets():
    from hora.charts.rasi_strength import stronger
    from hora.core.const import Graha

    d4, _ = _e123_d4()
    signs = {g: int(place // 30) for g, place in d4.items()}
    aries = {g for g in range(9) if signs[g] == 0}
    libra = {g for g in range(9) if signs[g] == 6}
    assert aries == {int(Graha.MERCURY), int(Graha.SATURN)}
    assert libra == {int(Graha.JUPITER)}
    assert len(aries) == 2 and len(libra) == 1
    assert stronger(0, 6, d4).winner == 0
    assert "the ascendant not counting" in (
        ex123.THE_SEED_IS_DECIDED_BY_COUNTING_PLANETS)


def test_the_dasa_order_and_the_saturn_exception():
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import progression

    d4, _ = _e123_d4()
    signs = {g: int(place // 30) for g, place in d4.items()}
    occupants = {g for g in range(9) if signs[g] == 0}
    order = progression(0, occupants=occupants)
    assert list(order.sign_names[:4]) == ["Aries", "Taurus", "Gemini",
                                          "Cancer"]
    assert order.exception == "Saturn"
    assert int(Graha.SATURN) in occupants
    # And Aries alone would have run the same way.
    assert progression(0, occupants=set()).sign_names[:4] == (
        order.sign_names[:4])
    assert "The order is unchanged" in (
        ex123.THE_SATURN_EXCEPTION_FIRES_AND_CHANGES_NOTHING)


def test_virgo_dasa_holds_the_departure_under_every_reading():
    import swisseph as swe

    from hora.core.const import RASI_ABBR, RASI_LORD
    from hora.core.ephemeris import get_ephemeris
    from hora.dasha.annual.varsha_narayana import compressed_days
    from hora.dasha.rasi.narayana import dasa_length, progression

    d4, _ = _e123_d4()
    signs = {g: int(place // 30) for g, place in d4.items()}
    order = progression(0, occupants={g for g in range(9) if signs[g] == 0})

    elapsed, virgo = 0, None
    for rasi in order.signs:
        days = compressed_days(dasa_length(
            rasi=rasi, lord=int(RASI_LORD[rasi]),
            lord_sign=signs[int(RASI_LORD[rasi])]).years)
        if RASI_ABBR[rasi] == "Vi":
            virgo = (elapsed, elapsed + days)
            break
        elapsed += days
    assert virgo == (126, 141)

    eph = get_ephemeris(_SETTINGS)
    at_start = eph.positions(_E123_PRAVESH.jd_ut, [0])[0].longitude

    def after(degrees):
        low, high = _E123_PRAVESH.jd_ut, _E123_PRAVESH.jd_ut + 400.0
        for _ in range(70):
            middle = (low + high) / 2.0
            moved = (eph.positions(middle, [0])[0].longitude - at_start) % 360.0
            if moved < degrees:
                low = middle
            else:
                high = middle
        return (low + high) / 2.0

    printed = (from_local(1991, 8, 10, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
               from_local(1991, 8, 26, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut)
    calendar = (_E123_PRAVESH.jd_ut + 126, _E123_PRAVESH.jd_ut + 141)
    solar = (after(126), after(141))
    for opens, closes in (printed, calendar, solar):
        assert opens < _E123_TRIP < closes

    def day(jd):
        year, month, dom, _ = swe.revjul(jd + 5.5 / 24.0)
        return int(year), int(month), int(dom)

    assert day(calendar[0]) == (1991, 8, 9)
    assert day(calendar[1]) == (1991, 8, 24)
    assert day(solar[0]) == (1991, 8, 14)
    assert "inside it under every reading" in (
        ex123.THE_VIRGO_DASA_DATES_ARE_A_DAY_OR_TWO_OUT)


def test_the_antardasa_does_not_reproduce():
    """§18.3 puts Gemini third, on 11-12 August. OI-177."""
    from hora.core.const import RASI_ABBR
    from hora.dasha.rasi.narayana import antardasas

    d4, _ = _e123_d4()
    legs = antardasas(5, 5, d4)                    # Virgo dasa, 5 years
    assert legs.start_name == "Aries"
    assert list(legs.sign_names[:3]) == ["Aries", "Taurus", "Gemini"]
    assert legs.sign_names.index("Gemini") == 2

    for opens, closes, expected in (
            (_E123_PRAVESH.jd_ut + 126, _E123_PRAVESH.jd_ut + 141, "Vi"),
            (from_local(1991, 8, 10, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
             from_local(1991, 8, 26, 0, 0, 0.0, utc_offset_hours=5.5).jd_ut,
             "Le")):
        span = (closes - opens) / 12.0
        index = int((_E123_TRIP - opens) / span)
        assert RASI_ABBR[legs.signs[index]] == expected
        assert RASI_ABBR[legs.signs[index]] != "Ge"

    assert "The example says Gemini" in ex123.THE_ANTARDASA_DOES_NOT_REPRODUCE


def test_two_lagnas_do_two_different_jobs():
    from hora.core.const import RASI_ABBR
    from hora.dasha.annual.varsha_narayana import progressed_lagna

    muntha = progressed_lagna(5, ex123.ANNUAL_YEAR)["rasi"]
    _, d4_lagna = _e123_d4()
    assert RASI_ABBR[muntha] == "Ge"
    assert RASI_ABBR[d4_lagna] == "Li"
    assert muntha != d4_lagna
    # The paragraph counts Virgo as the 12th and Gemini as the 9th, both
    # from Libra and neither from Gemini.
    assert (RASI_ABBR.index("Vi") - d4_lagna) % 12 + 1 == 12
    assert (RASI_ABBR.index("Ge") - d4_lagna) % 12 + 1 == 9
    assert (RASI_ABBR.index("Vi") - muntha) % 12 + 1 == 4
    assert "without naming the difference" in (
        ex123.TWO_LAGNAS_DO_TWO_DIFFERENT_JOBS)


def test_the_rasi_chart_reasons_hold_too():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha

    chart = _e123_annual()
    lagna = chart.lagna_rasi
    assert RASI_ABBR[lagna] == "Cp"
    for graha in (Graha.SATURN, Graha.RAHU):
        assert int(chart.positions[int(graha)].longitude // 30) == lagna
    twelfth = (lagna + 11) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[twelfth])]) == "Jupiter"
    jupiter = int(chart.positions[int(Graha.JUPITER)].longitude // 30)
    assert (jupiter - lagna) % 12 + 1 == 7
    assert RASI_ABBR[jupiter] == "Cn"              # Jupiter's exaltation


# --------------------------------------------------------------------------
# Example 124 and Chart 69
# --------------------------------------------------------------------------

from hora.dasha.annual import example_124 as ex124

_E124_PRAVESH = from_local(**ex124.VARSHA_PRAVESH)


def _e124_annual():
    return compute_chart(_E124_PRAVESH, _EX48_PLACE, _SETTINGS)


def _e124_d24():
    from hora.charts.vargas import d24_chaturvimsamsa

    chart = _e124_annual()
    signs = {g: int(d24_chaturvimsamsa(chart.positions[g].longitude).sign)
             for g in range(9)}
    lagna = int(d24_chaturvimsamsa(chart.lagna_longitude).sign)
    return signs, lagna


def _e124_dignity(graha, signs):
    from hora.core.constants.graha import DEBILITATION_RASI, EXALTATION_RASI

    if graha in (7, 8):                       # the nodes take none
        return None
    if signs[graha] == int(EXALTATION_RASI[graha]):
        return "exalted"
    if signs[graha] == int(DEBILITATION_RASI[graha]):
        return "debilitated"
    return None


def test_example_124_is_transcribed():
    assert "stood State First in Intermediate" in ex124.EXAMPLE_124
    assert "Varsha Narayana dasa of D-24" in ex124.EXAMPLE_124
    assert "2:15:41 am (IST)" in ex124.VARSHA_PRAVESH_DATA
    assert "Vidya saham lord Mars is in the 5th house" in ex124.WHY_EDUCATION
    assert "Cn dasa runs during May 26-June 17, 1987" in (
        ex124.THE_DASA_PARAGRAPH)
    assert [row["number"] for row in ex124.WHY_CANCER] == [1, 2, 3, 4]
    assert ex124.VARGA == 24 and ex124.ANNUAL_YEAR == 18


def test_chart_69_and_its_d24_reproduce():
    from hora.charts.book import chart as record
    from hora.charts.book import longitudes
    from hora.core.const import RASI_ABBR

    chart = _e124_annual()
    printed = longitudes(69)
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    for name, index in ids.items():
        gap = (((chart.positions[index].longitude - printed[name] + 180) % 360)
               - 180) * 60
        assert 0.0 < gap <= 1.0, (name, gap)
    assert chart.positions[6].is_retrograde is True          # Sat (R)

    signs, lagna = _e124_d24()
    drawn = record(69)["divisional"]["D24"]
    for name, index in ids.items():
        assert RASI_ABBR[signs[index]] == drawn[name], name
    assert RASI_ABBR[lagna] == drawn["Asc"] == "Ta"


def test_the_varsha_pravesh_reproduces_to_five_seconds():
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                              _SETTINGS).positions[0].longitude
    got = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                         natal_sun, _EX48_BIRTH.jd_ut, ex124.ANNUAL_YEAR)
    assert 0.0 < (got["jd"] - _E124_PRAVESH.jd_ut) * 86400.0 < 6.0


def test_the_vidya_saham_reproduces_and_its_lord_is_mars():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD
    from hora.tajaka.harsha import year_began_in_daytime
    from hora.tajaka.sahams import TABLE_74_SAHAMS, sahams

    night = year_began_in_daytime(_E124_PRAVESH.jd_ut,
                                  latitude=_EX48_PLACE.latitude,
                                  longitude=_EX48_PLACE.longitude)
    assert night["daytime"] is False

    chart = _e124_annual()
    names = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
    got = sahams(longitudes={name: chart.positions[i].longitude
                             for i, name in enumerate(names)},
                 lagna=chart.lagna_longitude, daytime=False)["Vidya"]
    rasi = int(got["longitude"] // 30)
    assert RASI_ABBR[rasi] == "Ar"
    assert got["longitude"] % 30 == pytest.approx(27 + 38 / 60, abs=0.02)
    assert str(GRAHA_NAMES[int(RASI_LORD[rasi])]) == "Mars"

    # It is the row Table 74 prints without a number.
    vidya = next(r for r in TABLE_74_SAHAMS if r["name"] == "Vidya")
    assert vidya["number"] is None
    assert "first use in the book" in (
        ex124.THE_VIDYA_SAHAM_REPRODUCES_AND_ITS_LORD_IS_MARS)


def test_marss_two_placements_hold():
    from hora.charts.arudha import arudha_pada
    from hora.core.const import RASI_ABBR, RASI_LORD, Graha

    chart = _e124_annual()
    mars = int(chart.positions[int(Graha.MARS)].longitude // 30)
    assert (mars - chart.lagna_rasi) % 12 + 1 == 5          # 5th in rasi

    signs, lagna = _e124_d24()
    assert int(RASI_LORD[signs[int(Graha.MARS)]]) == int(Graha.MARS)
    al = arudha_pada(1, lagna, signs).sign
    assert RASI_ABBR[al] == "Vi"
    assert (signs[int(Graha.MARS)] - al) % 12 + 1 == 3      # 3rd from AL


def test_the_varga_number_picks_the_house_modulo_twelve():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha
    from hora.dasha.annual.varsha_narayana import (
        house_for_varga,
        progressed_lagna,
    )

    assert house_for_varga(9) == 9
    assert house_for_varga(4) == 4
    assert house_for_varga(24) == 12
    assert house_for_varga(12) == 12

    muntha = progressed_lagna(5, ex124.ANNUAL_YEAR)["rasi"]
    assert RASI_ABBR[muntha] == "Aq"
    house = house_for_varga(ex124.VARGA)
    seat = (muntha + house - 1) % 12
    assert RASI_ABBR[seat] == "Cp"
    assert str(GRAHA_NAMES[int(RASI_LORD[seat])]) == "Saturn"

    signs, _ = _e124_d24()
    assert RASI_ABBR[signs[int(Graha.SATURN)]] == "Ar"
    assert "reduced by twelves" in (
        ex124.THREE_EXAMPLES_THREE_VARGAS_ONE_RULE)


def test_the_seed_and_the_dasa_order():
    from hora.charts.rasi_strength import stronger
    from hora.charts.vargas import d24_chaturvimsamsa
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import progression

    chart = _e124_annual()
    d24 = {g: int(d24_chaturvimsamsa(chart.positions[g].longitude).sign) * 30.0
           + (chart.positions[g].longitude % 1.25) * 24 for g in range(9)}
    signs, _ = _e124_d24()
    assert stronger(signs[int(Graha.SATURN)],
                    (signs[int(Graha.SATURN)] + 6) % 12, d24).winner == 0
    order = progression(0, occupants={g for g in range(9) if signs[g] == 0})
    assert list(order.sign_names[:4]) == ["Aries", "Taurus", "Gemini",
                                          "Cancer"]


def test_the_dignities_are_what_make_the_date_come_out():
    """Without them Cancer opens 29 May; with them 26 May, as printed."""
    import swisseph as swe

    from hora.core.const import RASI_ABBR, RASI_LORD
    from hora.dasha.annual.varsha_narayana import compressed_days
    from hora.dasha.rasi.narayana import dasa_length, progression

    signs, _ = _e124_d24()
    order = progression(0, occupants={g for g in range(9) if signs[g] == 0})

    def cancer_opens(use_dignity):
        elapsed = 0
        for rasi in order.signs:
            if RASI_ABBR[rasi] == "Cn":
                return elapsed
            lord = int(RASI_LORD[rasi])
            elapsed += compressed_days(dasa_length(
                rasi=rasi, lord=lord, lord_sign=signs[lord],
                lord_dignity=_e124_dignity(lord, signs)
                if use_dignity else None).years)
        raise AssertionError("no Cancer dasa")

    def day(offset):
        year, month, dom, _ = swe.revjul(
            _E124_PRAVESH.jd_ut + offset + 5.5 / 24.0)
        return int(year), int(month), int(dom)

    assert day(cancer_opens(False)) == (1987, 5, 29)
    assert day(cancer_opens(True)) == (1987, 5, 26)          # as printed

    # Both events fall inside only with the dignities applied.
    opens = cancer_opens(True)
    lord = int(RASI_LORD[3])                                 # Cancer's Moon
    length = compressed_days(dasa_length(
        rasi=3, lord=lord, lord_sign=signs[lord],
        lord_dignity=_e124_dignity(lord, signs)).years)
    for event in ex124.EVENTS.values():
        when = from_local(*event, 12, 0, 0.0, utc_offset_hours=5.5).jd_ut
        assert (_E124_PRAVESH.jd_ut + opens <= when
                < _E124_PRAVESH.jd_ut + opens + length), event
    assert day(opens + length) == (1987, 6, 16)              # printed: 17
    assert "the only Varsha Narayana date in the chapter whose opening is" in (
        ex124.THE_OPENING_IS_EXACT_AND_THE_CLOSE_IS_A_DAY_SHORT)


def test_example_122_forbids_the_dignity_on_the_nodes():
    """Its printed Scorpio dasa of 7 years needs Ketu's debilitation ignored.
    """
    from hora.charts.vargas import d9_navamsa
    from hora.core.const import Graha
    from hora.core.constants.graha import DEBILITATION_RASI
    from hora.dasha.annual.varsha_narayana import (
        DIGNITY_APPLIES_TO_THE_SEVEN_AND_NOT_THE_NODES,
    )
    from hora.dasha.rasi.narayana import dasa_length

    chart = _annual()                       # Example 122's annual chart
    navamsa = {g: int(d9_navamsa(chart.positions[g].longitude).sign)
               for g in range(9)}
    ketu = int(Graha.KETU)
    assert navamsa[ketu] == int(DEBILITATION_RASI[ketu])
    plain = dasa_length(rasi=7, lord=ketu, lord_sign=navamsa[ketu]).years
    with_it = dasa_length(rasi=7, lord=ketu, lord_sign=navamsa[ketu],
                          lord_dignity="debilitated").years
    assert plain == 7                       # what §30.4 prints
    assert with_it == 6
    assert _e124_dignity(ketu, navamsa) is None
    assert "the seven grahas only" in (
        DIGNITY_APPLIES_TO_THE_SEVEN_AND_NOT_THE_NODES)


def test_all_four_reasons_for_cancer_hold():
    from hora.charts.arudha import arudha_pada
    from hora.core.const import RASI_ABBR, RASI_LORD, Graha

    signs, lagna = _e124_d24()
    cancer = RASI_ABBR.index("Cn")

    # (1) Cancer holds the D-24 lagna lord.
    assert RASI_ABBR[lagna] == "Ta"
    lagna_lord = int(RASI_LORD[lagna])
    assert lagna_lord == int(Graha.VENUS)
    assert signs[lagna_lord] == cancer

    # (2) Cancer is the 11th from the arudha lagna.
    al = arudha_pada(1, lagna, signs).sign
    assert (cancer - al) % 12 + 1 == 11

    # (3) Cancer's lord, the Moon, is in the 5th from it.
    assert int(RASI_LORD[cancer]) == int(Graha.MOON)
    assert (signs[int(Graha.MOON)] - cancer) % 12 + 1 == 5

    # (4) That 5th holds Mars in his own sign.
    fifth = (cancer + 4) % 12
    assert RASI_ABBR[fifth] == "Sc"
    assert signs[int(Graha.MARS)] == fifth
    assert int(RASI_LORD[fifth]) == int(Graha.MARS)
    assert "Scorpio holds Mars in his own sign" in (
        ex124.ALL_FOUR_REASONS_FOR_CANCER_HOLD)


# --------------------------------------------------------------------------
# Example 125 and Chart 70
# --------------------------------------------------------------------------

from hora.dasha.annual import example_125 as ex125

_E125_PRAVESH = from_local(**ex125.VARSHA_PRAVESH)
_E125_SON = from_local(*ex125.BIRTH_OF_SON, 12, 0, 0.0,
                       utc_offset_hours=5.5).jd_ut


def _e125_annual():
    return compute_chart(_E125_PRAVESH, _EX48_PLACE, _SETTINGS)


def _e125_d7():
    from hora.charts.vargas import d7_saptamsa

    chart = _e125_annual()
    signs = {g: int(d7_saptamsa(chart.positions[g].longitude).sign)
             for g in range(9)}
    full = {g: signs[g] * 30.0 + (chart.positions[g].longitude % (30 / 7)) * 7
            for g in range(9)}
    return signs, full, int(d7_saptamsa(chart.lagna_longitude).sign)


def test_example_125_is_transcribed():
    assert "had a son on 21st August 1998" in ex125.EXAMPLE_125
    assert "Varsha Narayana dasa of D-7" in ex125.EXAMPLE_125
    assert "9:59:49 pm (IST)" in ex125.VARSHA_PRAVESH_DATA
    assert "putra saham is in Ar" in ex125.WHY_A_CHILD
    assert "Ge dasa of 24 solar days" in ex125.THE_DASA_PARAGRAPH
    assert [row["number"] for row in ex125.WHY_GEMINI] == [1, 2, 3, 4, 5, 6]
    assert ex125.VARGA == 7 and ex125.ANNUAL_YEAR == 29


def test_chart_70_and_its_d7_reproduce():
    from hora.charts.book import chart as record
    from hora.charts.book import longitudes
    from hora.core.const import RASI_ABBR

    chart = _e125_annual()
    printed = longitudes(70)
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    for name, index in ids.items():
        gap = (((chart.positions[index].longitude - printed[name] + 180) % 360)
               - 180) * 60
        assert 0.0 <= gap < 1.0, (name, gap)
    assert chart.positions[3].is_retrograde is True         # Merc (R)

    signs, _, lagna = _e125_d7()
    drawn = record(70)["divisional"]["D7"]
    for name, index in ids.items():
        assert RASI_ABBR[signs[index]] == drawn[name], name
    assert RASI_ABBR[lagna] == drawn["Asc"] == "Le"


def test_example_125s_varsha_pravesh_reproduces():
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                              _SETTINGS).positions[0].longitude
    got = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                         natal_sun, _EX48_BIRTH.jd_ut, ex125.ANNUAL_YEAR)
    assert 0.0 < (got["jd"] - _E125_PRAVESH.jd_ut) * 86400.0 < 12.0


def test_the_putra_saham_reproduces():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha
    from hora.tajaka.harsha import year_began_in_daytime
    from hora.tajaka.sahams import sahams

    night = year_began_in_daytime(_E125_PRAVESH.jd_ut,
                                  latitude=_EX48_PLACE.latitude,
                                  longitude=_EX48_PLACE.longitude)
    assert night["daytime"] is False

    chart = _e125_annual()
    names = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
    got = sahams(longitudes={name: chart.positions[i].longitude
                             for i, name in enumerate(names)},
                 lagna=chart.lagna_longitude, daytime=False)["Putra"]
    rasi = int(got["longitude"] // 30)
    assert RASI_ABBR[rasi] == "Ar"
    assert got["longitude"] % 30 == pytest.approx(23 + 33 / 60, abs=0.02)
    assert str(GRAHA_NAMES[int(RASI_LORD[rasi])]) == "Mars"

    assert RASI_ABBR[chart.lagna_rasi] == "Sc"
    mars = int(chart.positions[int(Graha.MARS)].longitude // 30)
    assert (mars - chart.lagna_rasi) % 12 + 1 == 5
    assert "in the 5th from the Scorpio lagna" in ex125.THE_PUTRA_SAHAM_REPRODUCES


def test_the_varga_house_rule_holds_a_fourth_time():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha
    from hora.dasha.annual.varsha_narayana import (
        house_for_varga,
        progressed_lagna,
    )

    assert house_for_varga(7) == 7
    muntha = progressed_lagna(5, ex125.ANNUAL_YEAR)["rasi"]
    assert RASI_ABBR[muntha] == "Cp"
    seat = (muntha + house_for_varga(ex125.VARGA) - 1) % 12
    assert RASI_ABBR[seat] == "Cn"
    assert str(GRAHA_NAMES[int(RASI_LORD[seat])]) == "Moon"

    signs, _, _ = _e125_d7()
    assert RASI_ABBR[signs[int(Graha.MOON)]] == "Cp"
    assert "four vargas and one rule" in (
        ex125.THE_VARGA_HOUSE_RULE_HOLDS_A_FOURTH_TIME)


def test_example_125s_seed_and_dasa_order():
    from hora.charts.rasi_strength import stronger
    from hora.core.const import RASI_ABBR, Graha
    from hora.dasha.rasi.narayana import progression

    signs, full, _ = _e125_d7()
    moon = signs[int(Graha.MOON)]
    assert stronger(moon, (moon + 6) % 12, full).winner == moon
    order = progression(moon, occupants={g for g in range(9)
                                         if signs[g] == moon})
    assert list(order.sign_names[:4]) == ["Capricorn", "Sagittarius",
                                          "Scorpio", "Libra"]
    assert RASI_ABBR[order.signs[7]] == "Ge"           # the eighth dasa


def test_gemini_runs_24_solar_days_and_opens_the_day_before_the_birth():
    import swisseph as swe

    from hora.core.const import RASI_ABBR, RASI_LORD
    from hora.core.constants.graha import DEBILITATION_RASI, EXALTATION_RASI
    from hora.dasha.annual.varsha_narayana import compressed_days
    from hora.dasha.rasi.narayana import dasa_length, progression

    signs, _full, _ = _e125_d7()
    from hora.core.const import Graha

    seed = signs[int(Graha.MOON)]
    order = progression(seed, occupants={g for g in range(9)
                                         if signs[g] == seed})

    def dignity(graha):
        if graha in (7, 8):                            # not the nodes
            return None
        if signs[graha] == int(EXALTATION_RASI[graha]):
            return "exalted"
        if signs[graha] == int(DEBILITATION_RASI[graha]):
            return "debilitated"
        return None

    elapsed, gemini = 0, None
    for rasi in order.signs:
        lord = int(RASI_LORD[rasi])
        days = compressed_days(dasa_length(
            rasi=rasi, lord=lord, lord_sign=signs[lord],
            lord_dignity=dignity(lord)).years)
        if RASI_ABBR[rasi] == "Ge":
            gemini = (elapsed, days)
            break
        elapsed += days
    assert gemini is not None
    opens, length = gemini
    assert length == 24                                # the printed figure

    def day(offset):
        year, month, dom, _ = swe.revjul(
            _E125_PRAVESH.jd_ut + offset + 5.5 / 24.0)
        return int(year), int(month), int(dom)

    assert day(opens) == (1998, 8, 20)                 # just before the birth
    assert (_E125_PRAVESH.jd_ut + opens < _E125_SON
            < _E125_PRAVESH.jd_ut + opens + length)
    assert "lands to the day" in (
        ex125.THE_ONLY_EXAMPLE_WHOSE_LENGTH_AND_OPENING_BOTH_COME_OUT)


def test_all_six_reasons_for_gemini_hold():
    from hora.charts.arudha import arudha_pada
    from hora.charts.aspects import graha_drishti_houses, rasi_drishti
    from hora.core.const import RASI_ABBR, RASI_LORD, Graha
    from hora.core.constants.graha import EXALTATION_RASI

    signs, _, lagna = _e125_d7()
    gemini = RASI_ABBR.index("Ge")
    fifth = (lagna + 4) % 12

    # (1) Gemini is the 11th.
    assert (gemini - lagna) % 12 + 1 == 11
    # (2)(3) Jupiter is there, owns the 5th and aspects it.
    assert signs[int(Graha.JUPITER)] == gemini
    assert int(RASI_LORD[fifth]) == int(Graha.JUPITER)
    reach = [(gemini + h - 1) % 12
             for h in graha_drishti_houses(int(Graha.JUPITER))]
    assert fifth in reach
    # (4) The 3rd is the 11th from the 5th; its exalted lord Venus aspects Ge.
    third = (lagna + 2) % 12
    assert (third - fifth) % 12 + 1 == 11
    assert int(RASI_LORD[third]) == int(Graha.VENUS)
    venus = signs[int(Graha.VENUS)]
    assert venus == int(EXALTATION_RASI[int(Graha.VENUS)])
    assert gemini in rasi_drishti(venus)
    # (5) Mars aspects Gemini, by his special 4th.
    mars = signs[int(Graha.MARS)]
    assert gemini in [(mars + h - 1) % 12
                      for h in graha_drishti_houses(int(Graha.MARS))]
    # (6) The putra pada aspects Gemini from Virgo.
    pada = arudha_pada(5, lagna, signs).sign
    assert RASI_ABBR[pada] == "Vi"
    assert gemini in rasi_drishti(pada)


def test_the_paragraph_mixes_two_kinds_of_aspect():
    kinds = [row["aspect"] for row in ex125.WHY_GEMINI]
    assert kinds == [None, None, "graha drishti", "rasi drishti",
                     "graha drishti", "rasi drishti"]
    assert "An arudha pada has no graha" in (
        ex125.THE_PARAGRAPH_MIXES_TWO_KINDS_OF_ASPECT)


def test_the_section_rests_on_two_of_the_six():
    assert "simply because it is 11th and 5th lord Jupiter occupies it" in (
        ex125.THE_CLEAR_CANDIDATE)
    assert "sets aside" not in ex125.THE_CLEAR_CANDIDATE
    assert "resting on two of them" in (
        ex125.THE_SECTION_SAYS_THREE_OF_THE_SIX_WOULD_HAVE_DONE)


def test_the_chapter_works_four_vargas():
    from hora.dasha.annual.varsha_narayana import house_for_varga

    worked = {9: 9, 4: 4, 24: 12, 7: 7}
    for varga, house in worked.items():
        assert house_for_varga(varga) == house
    assert len(set(worked)) == 4


# --------------------------------------------------------------------------
# Exercise 49 and Chart 71
# --------------------------------------------------------------------------

from hora.dasha.annual import exercise_49 as ex49

_E49_PRAVESH = from_local(**ex49.VARSHA_PRAVESH)


def _e49_annual():
    return compute_chart(_E49_PRAVESH, _EX48_PLACE, _SETTINGS)


def _e49_d16():
    from hora.charts.vargas import d16_shodasamsa

    chart = _e49_annual()
    signs = {g: int(d16_shodasamsa(chart.positions[g].longitude).sign)
             for g in range(9)}
    full = {g: signs[g] * 30.0 + (chart.positions[g].longitude % 1.875) * 16
            for g in range(9)}
    return signs, full, int(d16_shodasamsa(chart.lagna_longitude).sign)


def test_exercise_49_is_transcribed():
    assert "bought a car in 1995-96" in ex49.EXERCISE_49
    assert "Varsha Narayana dasa of D-16" in ex49.EXERCISE_49
    assert "3:28:36 am (IST)" in ex49.EXERCISE_49_ANSWER
    assert "Pi is stronger than Vi" in ex49.THE_SOLUTION
    assert "Cancer dasa in the second cycle ran during Jan 16-Feb 9, 1996" in (
        ex49.THE_SOLUTION)
    assert ex49.VARGA == 16 and ex49.ANNUAL_YEAR == 26


def test_chart_71_and_its_d16_reproduce():
    from hora.charts.book import chart as record
    from hora.charts.book import longitudes
    from hora.core.const import RASI_ABBR

    chart = _e49_annual()
    printed = longitudes(71)
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    for name, index in ids.items():
        gap = (((chart.positions[index].longitude - printed[name] + 180) % 360)
               - 180) * 60
        assert 0.0 < gap < 1.0, (name, gap)
    assert chart.positions[4].is_retrograde is True          # Jup (R)

    signs, _, lagna = _e49_d16()
    drawn = record(71)["divisional"]["D16"]
    for name, index in ids.items():
        assert RASI_ABBR[signs[index]] == drawn[name], name
    assert RASI_ABBR[lagna] == drawn["Asc"] == "Li"


def test_exercise_49s_varsha_pravesh_reproduces():
    from hora.core.ephemeris import get_ephemeris
    from hora.tajaka.annual import varsha_pravesh

    eph = get_ephemeris(_SETTINGS)
    natal_sun = compute_chart(_EX48_BIRTH, _EX48_PLACE,
                              _SETTINGS).positions[0].longitude
    got = varsha_pravesh(lambda jd: eph.positions(jd, [0])[0].longitude,
                         natal_sun, _EX48_BIRTH.jd_ut, ex49.ANNUAL_YEAR)
    assert 0.0 < (got["jd"] - _E49_PRAVESH.jd_ut) * 86400.0 < 8.0


def test_every_reading_in_the_solution_reproduces():
    from hora.core.const import GRAHA_NAMES, RASI_ABBR, RASI_LORD, Graha
    from hora.core.constants.graha import EXALTATION_RASI
    from hora.dasha.annual.varsha_narayana import (
        house_for_varga,
        progressed_lagna,
    )

    signs, _, lagna = _e49_d16()
    assert RASI_ABBR[lagna] == "Li"
    fourth = (lagna + 3) % 12
    assert RASI_ABBR[fourth] == "Cp"
    assert [g for g in range(9) if signs[g] == fourth] == []   # not strong

    venus = signs[int(Graha.VENUS)]
    assert RASI_ABBR[venus] == "Ar"
    from_venus = (venus + 3) % 12
    assert RASI_ABBR[from_venus] == "Cn"
    assert signs[int(Graha.JUPITER)] == from_venus
    assert from_venus == int(EXALTATION_RASI[int(Graha.JUPITER)])

    third = (lagna + 2) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[third])]) == "Jupiter"

    muntha = progressed_lagna(5, ex49.ANNUAL_YEAR)["rasi"]
    assert RASI_ABBR[muntha] == "Li"
    assert house_for_varga(ex49.VARGA) == 4
    seat = (muntha + 3) % 12
    assert RASI_ABBR[seat] == "Cp"
    assert str(GRAHA_NAMES[int(RASI_LORD[seat])]) == "Saturn"
    assert RASI_ABBR[signs[int(Graha.SATURN)]] == "Vi"
    assert "whose lord Saturn is in Virgo" in (
        ex49.EVERY_READING_IN_THE_SOLUTION_REPRODUCES)


def test_the_seed_comparison_closes_oi_124():
    """Rules 1-5 tie in the D-16; only the rasi chart's rule 6 gives Pisces.
    """
    from hora.charts.rasi_strength import (
        ADVANCEMENT_IS_READ_IN_THE_RASI_CHART,
        stronger,
    )
    from hora.core.const import RASI_ABBR

    chart = _e49_annual()
    rasi = {g: chart.positions[g].longitude for g in range(9)}
    _, d16, _ = _e49_d16()
    virgo, pisces = RASI_ABBR.index("Vi"), RASI_ABBR.index("Pi")

    in_varga = stronger(virgo, pisces, d16)
    assert in_varga.decided_by == "6"
    assert in_varga.winner == virgo                          # not the book's

    mixed = stronger(virgo, pisces, d16, advancement_longitudes=rasi)
    assert mixed.decided_by == "6"
    assert mixed.winner == pisces                            # the book's
    assert "11" in mixed.reason and "21" in mixed.reason
    assert "reads the rasi chart" in ADVANCEMENT_IS_READ_IN_THE_RASI_CHART


def test_the_other_four_seeds_are_decided_in_the_varga_at_rule_one():
    """Three of the four come out wrong from the rasi chart, so rules 1 to 5
    read the varga.
    """
    from hora.charts.rasi_strength import stronger
    from hora.charts.vargas import (
        d4_chaturthamsa,
        d7_saptamsa,
        d9_navamsa,
        d24_chaturvimsamsa,
    )
    from hora.core.const import RASI_ABBR

    cases = (
        (_PRAVESH, d9_navamsa, 30 / 9, "Sc", "Ta"),
        (_E123_PRAVESH, d4_chaturthamsa, 7.5, "Ar", "Li"),
        (_E124_PRAVESH, d24_chaturvimsamsa, 1.25, "Ar", "Li"),
        (_E125_PRAVESH, d7_saptamsa, 30 / 7, "Cp", "Cn"),
    )
    wrong_from_rasi = 0
    for instant, varga, width, printed, other in cases:
        chart = compute_chart(instant, _EX48_PLACE, _SETTINGS)
        rasi = {g: chart.positions[g].longitude for g in range(9)}
        divided = {g: int(varga(rasi[g]).sign) * 30.0
                   + (rasi[g] % width) * (30 / width) for g in range(9)}
        a, b = RASI_ABBR.index(printed), RASI_ABBR.index(other)
        in_varga = stronger(a, b, divided)
        assert in_varga.decided_by == "1"
        assert RASI_ABBR[in_varga.winner] == printed
        if RASI_ABBR[stronger(a, b, rasi).winner] != printed:
            wrong_from_rasi += 1
    assert wrong_from_rasi == 3


def test_the_seed_decides_the_movement_too():
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import progression

    signs, _, _ = _e49_d16()
    pisces = progression(11, occupants={g for g in range(9) if signs[g] == 11})
    assert pisces.movement == "trinal"
    assert pisces.exception is None
    assert list(pisces.sign_names[:6]) == [
        "Pisces", "Cancer", "Scorpio", "Sagittarius", "Aries", "Leo"]

    virgo = progression(5, occupants={g for g in range(9) if signs[g] == 5})
    assert int(Graha.SATURN) in {g for g in range(9) if signs[g] == 5}
    assert virgo.exception == "Saturn"
    assert list(virgo.sign_names[:3]) != list(pisces.sign_names[:3])
    assert "would have taken the Saturn exception" in (
        ex49.THE_SEED_DECIDES_THE_MOVEMENT_TOO)


def test_the_second_cycle_length_reproduces_and_its_position_does_not():
    import swisseph as swe

    from hora.core.const import RASI_ABBR, RASI_LORD
    from hora.core.constants.graha import DEBILITATION_RASI, EXALTATION_RASI
    from hora.dasha.annual.varsha_narayana import compressed_days
    from hora.dasha.rasi.narayana import (
        dasa_length,
        progression,
        second_cycle_length,
    )

    signs, _, _ = _e49_d16()
    order = progression(11, occupants={g for g in range(9) if signs[g] == 11})

    def dignity(graha):
        if graha in (7, 8):
            return None
        if signs[graha] == int(EXALTATION_RASI[graha]):
            return "exalted"
        if signs[graha] == int(DEBILITATION_RASI[graha]):
            return "debilitated"
        return None

    firsts, elapsed = {}, 0
    for rasi in order.signs:
        lord = int(RASI_LORD[rasi])
        firsts[rasi] = dasa_length(rasi=rasi, lord=lord, lord_sign=signs[lord],
                                   lord_dignity=dignity(lord)).years
        elapsed += compressed_days(firsts[rasi])

    cancer = RASI_ABBR.index("Cn")
    assert firsts[cancer] == 4
    assert second_cycle_length(firsts[cancer]) == 8
    assert compressed_days(8) == ex49.PRINTED_CANCER["days"] == 24

    # The printed window is 24 days wide.
    opens = from_local(*ex49.PRINTED_CANCER["from"], 0, 0, 0.0,
                       utc_offset_hours=5.5).jd_ut
    closes = from_local(*ex49.PRINTED_CANCER["to"], 0, 0, 0.0,
                        utc_offset_hours=5.5).jd_ut
    assert closes - opens == 24.0

    # But ours opens twenty-five days earlier.
    for rasi in order.signs:
        if rasi == cancer:
            break
        elapsed += compressed_days(second_cycle_length(firsts[rasi]))

    def day(offset):
        year, month, dom, _ = swe.revjul(
            _E49_PRAVESH.jd_ut + offset + 5.5 / 24.0)
        return int(year), int(month), int(dom)

    assert day(elapsed) == (1995, 12, 22)
    assert day(elapsed + 24) == (1996, 1, 15)
    gap = opens - (_E49_PRAVESH.jd_ut + elapsed)
    assert 24 < gap < 26
    assert "twenty-five days early" in (
        ex49.THE_SECOND_CYCLE_POSITION_IS_TWENTY_FIVE_DAYS_OUT)


def test_the_varga_house_rule_holds_a_fifth_time():
    from hora.dasha.annual.varsha_narayana import house_for_varga

    worked = {9: 9, 4: 4, 24: 12, 7: 7, 16: 4}
    for varga, house in worked.items():
        assert house_for_varga(varga) == house
    assert len(worked) == 5
    assert "five vargas and one rule" in (
        ex49.THE_VARGA_HOUSE_RULE_HOLDS_A_FIFTH_TIME)


# --------------------------------------------------------------------------
# Chapter 30's conclusion
# --------------------------------------------------------------------------


def test_the_conclusion_is_transcribed():
    assert "three dasa systems that are applicable to Tajaka annual charts" in (
        intro.CHAPTER_CONCLUSION)
    assert "Patyayini dasa is applicable to Tajaka monthly charts also" in (
        intro.CHAPTER_CONCLUSION)
    assert "Varsha Narayana dasa and Patyayini dasa give the best results" in (
        intro.CHAPTER_CONCLUSION)
    assert "exact month or week of the event" in intro.CHAPTER_CONCLUSION


def test_the_ranking_is_stated_three_times_and_loosens():
    from hora.dasha.annual import varsha_narayana as vn

    # §30.3's ranking, §30.4's, and the conclusion's.
    assert "Patyayini dasa shows the event better than Mudda dasa" not in (
        intro.CHAPTER_CONCLUSION)
    assert "Varsha Narayana dasa is, however, the best" in (
        vn.THE_BOOKS_OWN_RANKING)
    assert "Varsha Narayana dasa and Patyayini dasa give the best" in (
        intro.CHAPTER_CONCLUSION)
    # Mudda is last every time and never named at the top.
    assert "Mudda" not in intro.CHAPTER_CONCLUSION.split("best results")[0]
    assert "argues for the order" in (
        intro.THE_RANKING_IS_STATED_THREE_TIMES_AND_LOOSENS)


def test_only_patyayini_can_go_monthly():
    """It reads the chart's own longitudes; the other two need a yearly
    progression of the natal chart.
    """
    from hora.dasha.annual import mudda
    from hora.dasha.annual import varsha_narayana as vn

    assert "based on the longitudes of lagna and all planets" in (
        patyayini.PATYAYINI_SCOPE)
    assert "one constellation per year" in mudda.MUDDA_ORDER_RULE
    assert "one rasi per year" in vn.ORDER_RULE
    assert "a month has no such step" in intro.ONLY_PATYAYINI_CAN_GO_MONTHLY

    # And patyayini needs nothing from the natal chart at all.
    import inspect

    source = inspect.getsource(patyayini.patyayini_dasa)
    assert "natal" not in source


def test_the_monthly_divisor_is_not_given():
    """§27.3 makes a month 30° of solar motion; §30.2 divides a year by
    365.2425. The conclusion picks neither figure. OI-179.
    """
    from hora.dasha.annual import mudda
    from hora.tajaka.monthly import YEAR_AND_MONTH_ARE_SOLAR_ARCS

    assert "A month is the period in which Sun moves by 30" in (
        YEAR_AND_MONTH_ARE_SOLAR_ARCS)
    assert patyayini.PATYAYINI_YEAR_DAYS == 365.2425
    assert mudda.MUDDA_YEAR_DAYS == 360
    assert patyayini.PATYAYINI_YEAR_DAYS / 12 == pytest.approx(30.4369,
                                                              abs=5e-5)
    assert mudda.MUDDA_YEAR_DAYS / 12 == 30
    assert "monthly" not in patyayini.PATYAYINI_SCOPE
    for row in patyayini.PATYAYINI_PROCEDURE:
        assert "month" not in str(row["text"]).lower()
    assert "30.4369 days and 30" in intro.THE_MONTHLY_DIVISOR_IS_NOT_GIVEN


def test_the_resolution_claim_is_generous_for_patyayini():
    """Example 122's dasas ran from 0.4 days to 104."""
    got = _patyayini()
    lengths = [float(row["days"]) for row in got["rows"]]
    assert min(lengths) == pytest.approx(0.40, abs=0.02)
    assert max(lengths) == pytest.approx(104.2, abs=0.3)
    assert max(lengths) / min(lengths) > 250
    assert "a factor of" in intro.THE_RESOLUTION_CLAIM_IS_GENEROUS_FOR_PATYAYINI


def test_chapter_30_is_complete():
    from hora.dasha.annual import (
        example_123,
        example_124,
        example_125,
        exercise_48,
        exercise_49,
        mudda,
        patyayini,
        varsha_narayana,
    )

    marker = intro.CHAPTER_30_IS_COMPLETE
    assert "30.1 to §30.4" in marker.replace("§30.1", "30.1")
    assert "Tables 75 and 76" in marker
    assert "Charts 67 to 71" in marker
    assert "Examples 122 to 125" in marker
    assert "Exercises 48 and 49" in marker
    assert "Footnotes 85 to 88" in marker
    assert "OI-124 and OI-174" in marker

    # The three dasas, all built.
    assert callable(patyayini.patyayini_dasa)
    assert callable(mudda.mudda_dasa)
    assert callable(varsha_narayana.progressed_lagna)
    # And the five worked cases, all held as data.
    for module in (exercise_48, example_123, example_124, example_125,
                   exercise_49):
        assert module.PLACE == {"latitude": 16 + 15 / 60,
                                "longitude": 81 + 12 / 60}

    # All four footnotes.
    assert "B.V. Raman" in intro.FOOTNOTE_85
    assert "own researches" in intro.FOOTNOTE_86
    assert "largest krisamsa" in patyayini.FOOTNOTE_87
    assert "12 x 12 = 144" in varsha_narayana.FOOTNOTE_88
