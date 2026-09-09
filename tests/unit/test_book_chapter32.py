"""Chapter 32 — Impact of Birthtime Error. §32.1 and footnote 89."""

import pytest

from hora.charts import vargas
from hora.charts.chart import Place, compute_chart
from hora.charts.special_lagna import (
    ADVANCE_PER_MINUTE,
    SPECIAL_LAGNA_ABBR,
    all_special_lagnas,
)
from hora.core.const import RASI_ABBR, Graha
from hora.core.ephemeris import SwissEphemeris
from hora.core.settings import NodeType, Settings
from hora.core.timeutil import from_jd, from_local
from hora.rectification import birthtime

_SETTINGS = Settings()

#: The twenty-three vargas the book teaches, by number.
_VARGAS = {
    1: vargas.d1_rasi, 2: vargas.d2_hora, 3: vargas.d3_drekkana,
    4: vargas.d4_chaturthamsa, 5: vargas.d5_panchamsa,
    6: vargas.d6_shashtamsa, 7: vargas.d7_saptamsa, 8: vargas.d8_ashtamsa,
    9: vargas.d9_navamsa, 10: vargas.d10_dasamsa, 11: vargas.d11_rudramsa,
    12: vargas.d12_dwadasamsa, 16: vargas.d16_shodasamsa,
    20: vargas.d20_vimsamsa, 24: vargas.d24_chaturvimsamsa,
    27: vargas.d27_nakshatramsa, 30: vargas.d30_trimsamsa,
    40: vargas.d40_khavedamsa, 45: vargas.d45_akshavedamsa,
    60: vargas.d60_shashtyamsa, 81: vargas.d81_nava_navamsa,
    108: vargas.d108_ashtottaramsa, 144: vargas.d144_dwadas_dwadasamsa,
}

# Chart 1, the book's reference chart.
_PLACE = Place(name="Chart 1", latitude=42.5, longitude=-(71 + 12 / 60))


def _fast_points(minute_offset: int) -> dict[str, float]:
    """The ascendant and chapter 5's four special lagnas, cast `minute_offset`
    minutes after Chart 1's recorded birthtime.
    """
    chart = compute_chart(
        from_local(2000, 4, 9, 13, 35 + minute_offset, 0.0,
                   utc_offset_hours=-5.0), _PLACE, _SETTINGS)
    eph = SwissEphemeris(_SETTINGS)
    sunrise = eph.sunrise(chart.instant.jd_ut - 1.5, _PLACE.latitude,
                          _PLACE.longitude)
    while True:
        nxt = eph.sunrise(sunrise + 0.5, _PLACE.latitude, _PLACE.longitude)
        if nxt is None or nxt > chart.instant.jd_ut:
            break
        sunrise = nxt
    lagnas = all_special_lagnas(
        sunrise_jd=sunrise, jd_ut=chart.instant.jd_ut,
        lagna_longitude=chart.lagna_longitude,
        moon_longitude=chart.positions[int(Graha.MOON)].longitude,
        settings=_SETTINGS)
    points = {"Asc": chart.lagna_longitude}
    points.update({SPECIAL_LAGNA_ABBR[k]: v.longitude
                   for k, v in lagnas.items()})
    return points


# --------------------------------------------------------------------------
# §32.1 transcription
# --------------------------------------------------------------------------


def test_the_chapter_is_titled_and_the_section_transcribed():
    assert birthtime.CHAPTER_TITLE == "Impact of Birthtime Error"
    assert "born 1-2 minutes apart" in birthtime.TWINS_PROVE_THE_VARGAS_MATTER
    assert "*proves*" in birthtime.TWINS_PROVE_THE_VARGAS_MATTER
    assert "his hypothetical twin!" in (
        birthtime.A_WRONG_BIRTHTIME_IS_A_HYPOTHETICAL_TWIN)
    assert "**we must first make sure that we are working with an accurate " \
           "birthtime**" in birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME
    assert "only as accurate as our data!" in (
        birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME)
    assert "seldom accurate" in birthtime.BIRTHTIMES_ARE_SELDOM_ACCURATE


def test_the_four_causes_are_the_four_the_section_numbers():
    causes = birthtime.BIRTHTIME_ERROR_CAUSES
    assert len(causes) == 4
    assert [c["number"] for c in causes] == [1, 2, 3, 4]
    for row in causes:
        assert str(row["lies_with"]) in (
            "the instrument", "the recording", "the reporting",
            "the definition")
    lies = [c["lies_with"] for c in causes]
    assert len(set(lies)) == 4
    for number in ("(1)", "(2)", "(3)", "(4)"):
        assert number in birthtime.BIRTHTIMES_ARE_SELDOM_ACCURATE


def test_footnote_89_is_transcribed_and_its_technique_held_as_rejected():
    assert "illogical, irrational and against the teachings of maharshis" in (
        birthtime.FOOTNOTE_89)
    rejected = birthtime.THE_REJECTED_THIRD_HOUSE_TWIN_LAGNA
    assert rejected["implemented"] is False
    assert rejected["source"] is birthtime.FOOTNOTE_89
    worked = dict(rejected["worked_example"])
    assert worked == {"first_twin_lagna": "Aquarius",
                      "second_twin_lagna": "Aries"}
    # The example's own arithmetic: Aries is the 3rd from Aquarius.
    aquarius = RASI_ABBR.index("Aq")
    assert RASI_ABBR[(aquarius + 2) % 12] == "Ar"


def test_the_same_objection_is_made_to_both_practices():
    """FINDING: one appeal used against two different methods."""
    phrase = "against the teachings of maharshis"
    assert phrase in birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME
    assert phrase in birthtime.FOOTNOTE_89
    assert "It is the only reason given against either" in (
        birthtime.THE_SAME_OBJECTION_IS_MADE_TO_BOTH_PRACTICES)


def test_the_section_grants_the_results_and_rejects_the_method():
    text = birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME
    assert "one can be successful in one's predictions only using D-1" in text
    assert "but that is clearly unscientific" in text
    assert "reproducibility, not" in (
        birthtime.THE_SECTION_GRANTS_THE_RESULTS_AND_REJECTS_THE_METHOD)


def test_only_the_fourth_cause_is_ours_to_answer():
    """FINDING: three causes are unobservable; the fourth is definitional."""
    causes = {int(c["number"]): c for c in birthtime.BIRTHTIME_ERROR_CAUSES}
    assert causes[4]["lies_with"] == "the definition"
    assert "definition of 'birth'" in causes[4]["cause"]
    # The section names it and does not define it.
    for text in (birthtime.TWINS_PROVE_THE_VARGAS_MATTER,
                 birthtime.A_WRONG_BIRTHTIME_IS_A_HYPOTHETICAL_TWIN,
                 birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME,
                 birthtime.BIRTHTIMES_ARE_SELDOM_ACCURATE):
        assert "first breath" not in text
    assert "without defining it" in (
        birthtime.ONLY_THE_FOURTH_CAUSE_IS_OURS_TO_ANSWER)


# --------------------------------------------------------------------------
# What the section claims, measured
# --------------------------------------------------------------------------


def test_the_two_hours_is_a_mean_not_a_rate():
    """FINDING: twelve rasis in a sidereal day is 119.7 minutes on average,
    and no individual rasi takes that long.
    """
    assert "Lagna in D-1 changes rasi once in 2 hours" in (
        birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME)

    base = from_local(2000, 3, 20, 0, 0, 0.0, utc_offset_hours=0.0).jd_ut
    measured = {}
    for latitude in (0.0, 42.5):
        place = Place(name="span", latitude=latitude, longitude=0.0)
        previous, started, spans = None, 0, {}
        for minute in range(48 * 60 + 1):
            rasi = int(compute_chart(from_jd(base + minute / 1440.0), place,
                                     _SETTINGS).lagna_longitude // 30)
            if rasi != previous:
                if previous is not None:
                    spans[previous] = max(spans.get(previous, 0),
                                          minute - started)
                previous, started = rasi, minute
        assert len(spans) == 12
        # One sidereal day, to the minute.
        assert 1435 <= sum(spans.values()) <= 1438
        measured[latitude] = (min(spans.values()), max(spans.values()))

    # The mean is the two hours; the individual spans are not.
    assert 119 <= 1436 / 12 <= 120
    assert measured[0.0] == (110, 130)
    assert measured[42.5] == (67, 155)
    assert "119.7 minutes" in birthtime.THE_TWO_HOURS_IS_A_MEAN_NOT_A_RATE


def test_two_minutes_moves_fifty_four_of_a_hundred_and_fifteen_signs():
    """FINDING: the section's "some divisional charts" is an understatement."""
    before, after = _fast_points(0), _fast_points(2)
    assert set(before) == {"Asc", "BL", "HL", "GL", "SL"}
    assert len(_VARGAS) == 23

    changed = birthtime.varga_signs_that_change(before, after, _VARGAS)
    assert len(before) * len(_VARGAS) == 115
    assert len(changed) == 54

    # Not one of the five moves in D-1, which is why the claim is about
    # divisional charts and not about the rasi chart.
    assert not [row for row in changed if row["varga"] == 1]

    by_point: dict[str, list[int]] = {}
    for row in changed:
        by_point.setdefault(str(row["point"]), []).append(int(row["varga"]))
    assert min(by_point["Asc"]) == 27
    assert len(by_point["GL"]) == 18
    assert "54 of the 115" in (
        birthtime.FIFTY_FOUR_OF_A_HUNDRED_AND_FIFTEEN_SIGNS_MOVE)


def test_ghati_lagna_moves_furthest_because_of_its_own_rate():
    """GL is the fastest of the five, and that is section 5.5's rate."""
    from hora.charts.special_lagna import SpecialLagna

    before, after = _fast_points(0), _fast_points(2)
    moved = {point: after[point] - before[point] for point in before}
    assert moved["GL"] == pytest.approx(2.5, abs=1e-5)
    assert moved["GL"] == pytest.approx(
        2 * ADVANCE_PER_MINUTE[SpecialLagna.GHATI], abs=1e-5)
    assert moved["HL"] == pytest.approx(1.0, abs=1e-5)
    assert moved["BL"] == pytest.approx(0.5, abs=1e-5)
    # The ascendant is the slowest of them at this latitude and hour.
    assert moved["Asc"] < moved["BL"]


def test_the_chapter_explains_the_rounded_headers_of_charts_72_to_74():
    """FINDING: the three ascendants that needed seconds, and the reason."""
    for tag, lat, lon, when, seconds in (
            ("Chart 72", 21 + 27 / 60, 83 + 58 / 60,
             (1963, 8, 7, 21, 14), 48),
            ("Chart 73", 25 + 28 / 60, 81 + 52 / 60,
             (1976, 11, 20, 2, 10), 50),
            ("Chart 74", 16 + 13 / 60, 80 + 28 / 60,
             (1998, 7, 27, 7, 15), 48)):
        place = Place(name=tag, latitude=lat, longitude=lon)
        settings = Settings(node_type=NodeType.MEAN)
        y, mo, d, h, mi = when
        at_zero = compute_chart(
            from_local(y, mo, d, h, mi, 0.0, utc_offset_hours=5.5),
            place, settings).lagna_longitude
        a_minute_on = compute_chart(
            from_local(y, mo, d, h, mi + 1, 0.0, utc_offset_hours=5.5),
            place, settings).lagna_longitude
        rate = (a_minute_on - at_zero) * 60
        assert 13 < rate < 20, (tag, rate)
        # The seconds each figure needed are a real fraction of a minute.
        assert 0 < seconds < 60
    assert "section 32.1 is the section that says why that matters" in (
        birthtime.THE_CHAPTER_EXPLAINS_THE_ROUNDED_HEADERS)


# --------------------------------------------------------------------------
# The helper's own contract
# --------------------------------------------------------------------------


def test_varga_signs_that_change_rejects_mismatched_castings():
    with pytest.raises(birthtime.BirthtimeError, match="same points"):
        birthtime.varga_signs_that_change({"Asc": 10.0},
                                          {"Asc": 10.0, "GL": 20.0}, _VARGAS)


def test_varga_signs_that_change_needs_at_least_one_varga():
    with pytest.raises(birthtime.BirthtimeError, match="at least one varga"):
        birthtime.varga_signs_that_change({"Asc": 10.0}, {"Asc": 11.0}, {})


def test_an_identical_casting_changes_nothing():
    points = _fast_points(0)
    assert birthtime.varga_signs_that_change(points, dict(points),
                                             _VARGAS) == ()
