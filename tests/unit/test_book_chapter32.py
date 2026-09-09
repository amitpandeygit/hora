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


# --------------------------------------------------------------------------
# §32.1 continued — rectification defined, and the acid test of twins
# --------------------------------------------------------------------------


def test_rectification_and_the_quantum_family_are_transcribed():
    assert "**Birthtime rectification** is the process of correcting" in (
        birthtime.RECTIFICATION_DEFINED)
    assert "human births happen in certain quanta" in (
        birthtime.RECTIFICATION_DEFINED)
    assert '"human birth can happen now" quantum' in (
        birthtime.RECTIFICATION_DEFINED)
    assert birthtime.QUANTUM_CLOSED_MINUTES == 3.0
    assert birthtime.QUANTUM_OPEN_MINUTES == 0.5
    assert birthtime.QUANTUM_CYCLE_MINUTES == 3.5
    assert "period of 3 minutes" in birthtime.RECTIFICATION_DEFINED
    assert "period of half a minute" in birthtime.RECTIFICATION_DEFINED


def test_the_three_named_methods_and_what_becomes_of_each():
    assert "(a) Tattva siddhaanta" in birthtime.THE_THREE_REASONABLE_METHODS
    assert "fail the acid test of twins" in (
        birthtime.THE_THREE_REASONABLE_METHODS)
    methods = birthtime.NAMED_METHODS
    assert [m["label"] for m in methods] == ["a", "b", "c"]
    assert methods[0]["fails_the_acid_test"] is None      # out of scope
    assert methods[1]["fails_the_acid_test"] is True
    assert methods[2]["fails_the_acid_test"] is True
    # None of the three is taught, so none of the verdicts is reproducible.
    assert all(m["taught_here"] is False for m in methods)
    assert "cannot be checked" in (
        birthtime.THE_ACID_TEST_IS_STATED_ON_METHODS_THE_BOOK_NEVER_TEACHES)


def test_the_only_correct_way_is_transcribed_and_its_five_demands_listed():
    assert "The only correct way to rectify a birthtime" in (
        birthtime.THE_ONLY_CORRECT_WAY)
    assert "This is a laborious process, but there is no other way" in (
        birthtime.THE_ONLY_CORRECT_WAY)
    demands = birthtime.WHAT_A_RECTIFIED_TIME_MUST_EXPLAIN
    assert len(demands) == 5
    for word in ("nature", "credentials", "attitude", "aptitude"):
        assert any(word in d for d in demands)
        assert word in birthtime.THE_ONLY_CORRECT_WAY
    assert demands[-1] == "the known events from the native's past"
    assert "the dated past" in (
        birthtime.THE_ONLY_ACCEPTED_METHOD_IS_THE_ONE_THAT_CANNOT_BE_AUTOMATED)


def test_the_scan_paragraphs_are_transcribed():
    text = birthtime.THE_SCAN_OVER_THE_REPORTED_RANGE
    assert "born between 9:02 and 9:08 am" in text
    assert "thousands of people born in that range" in text
    assert "we should look at 9:02, 9:03, 9:04 etc" in text
    assert "the known life events of the native make sense" in text
    assert len(text.split("\n\n")) == 3


# --------------------------------------------------------------------------
# The quantum family, run
# --------------------------------------------------------------------------


def test_the_nearest_quantum_snaps_to_a_window_centre():
    """The book's numbers: three minutes shut, half a minute open."""
    # Windows [0, 0.5), [3.5, 4.0), [7.0, 7.5) ... so the centres are 0.25,
    # 3.75, 7.25.
    assert birthtime.nearest_quantum(0.0) == pytest.approx(0.25)
    assert birthtime.nearest_quantum(0.4) == pytest.approx(0.25)
    assert birthtime.nearest_quantum(3.6) == pytest.approx(3.75)
    assert birthtime.nearest_quantum(7.2) == pytest.approx(7.25)
    # Every answer is a whole number of cycles from the first centre.
    for reported in (0.0, 1.9, 2.1, 5.0, 11.3, 100.0):
        offset = birthtime.nearest_quantum(reported) - 0.25
        assert offset % birthtime.QUANTUM_CYCLE_MINUTES == pytest.approx(
            0.0, abs=1e-9)


def test_the_quantum_family_needs_an_epoch_the_section_never_gives():
    """GAP: the windows' position is not stated, so the method is not
    reproducible from the section alone. It changes nothing here.
    """
    assert "period of 3 minutes" in birthtime.RECTIFICATION_DEFINED
    assert "period of half a minute" in birthtime.RECTIFICATION_DEFINED
    for word in ("begin", "epoch", "midnight", "sunrise"):
        assert word not in birthtime.RECTIFICATION_DEFINED

    # A different epoch gives a different answer for the same reported time.
    assert birthtime.nearest_quantum(2.0, epoch_minutes=0.0) != (
        birthtime.nearest_quantum(2.0, epoch_minutes=1.0))
    assert "cannot be run from the section alone" in (
        birthtime.THE_QUANTUM_FAMILY_HAS_NO_STATED_EPOCH)


def test_the_quantum_family_fails_the_acid_test_over_a_whole_cycle():
    """FINDING: the section's own example fails the section's own test —
    the same time 42.9% of the time and 3.5 minutes apart the rest.
    """
    gaps: dict[float, int] = {}
    steps = 3500
    for index in range(steps):
        got = birthtime.acid_test_of_twins(
            birthtime.nearest_quantum,
            index * birthtime.QUANTUM_CYCLE_MINUTES / steps)
        # Never returns the twins two minutes apart, whatever the instant.
        assert got["preserves_the_gap"] is False
        if got["collapsed_to_one_time"]:
            assert got["passes"] is False
        else:
            # "Too far apart" has no threshold in the section, so the verdict
            # is undecided rather than invented.
            assert got["passes"] is None
            assert got["reason"] is birthtime.THE_ACID_TEST_GIVES_NO_THRESHOLD
        gaps[round(float(got["rectified_gap_minutes"]), 6)] = (
            gaps.get(round(float(got["rectified_gap_minutes"]), 6), 0) + 1)

    assert set(gaps) == {0.0, 3.5}
    assert gaps[0.0] / steps == pytest.approx(3.0 / 7.0, abs=1e-3)   # 42.9%
    assert gaps[3.5] / steps == pytest.approx(4.0 / 7.0, abs=1e-3)   # 57.1%
    assert "42.9%" in (
        birthtime.THE_QUANTUM_FAMILY_FAILS_THE_ACID_TEST_BY_CONSTRUCTION)


def test_the_failure_is_structural_and_holds_at_every_epoch():
    """The rectified gap is always a whole number of cycles, so it can equal
    the true gap only when the true gap is one.
    """
    for epoch in (0.0, 0.37, 1.0, 2.9):
        for start in (0.0, 0.9, 1.7, 2.6, 3.2):
            def rectify(minutes: float, epoch: float = epoch) -> float:
                return birthtime.nearest_quantum(minutes, epoch_minutes=epoch)

            got = birthtime.acid_test_of_twins(rectify, start)
            gap = float(got["rectified_gap_minutes"])
            assert gap % birthtime.QUANTUM_CYCLE_MINUTES == pytest.approx(
                0.0, abs=1e-9)
            assert gap != 2.0
            assert got["preserves_the_gap"] is False

    # And a method that keeps the twins where they are does pass, on any
    # tolerance and even on none, because it preserves the gap exactly.
    passing = birthtime.acid_test_of_twins(lambda m: m + 0.1, 0.0,
                                           tolerance_minutes=0.5)
    assert passing["rectified_gap_minutes"] == pytest.approx(2.0)
    assert passing["collapsed_to_one_time"] is False
    assert passing["preserves_the_gap"] is True
    assert passing["passes"] is True
    assert passing["reason"] is None


def test_the_acid_test_rejects_a_gap_that_is_not_positive():
    with pytest.raises(birthtime.BirthtimeError, match="must be positive"):
        birthtime.acid_test_of_twins(birthtime.nearest_quantum, 0.0,
                                     gap_minutes=0.0)


def test_nearest_quantum_rejects_windows_that_are_not_positive():
    with pytest.raises(birthtime.BirthtimeError, match="must both be positive"):
        birthtime.nearest_quantum(1.0, open_minutes=0.0)


# --------------------------------------------------------------------------
# The scan the section actually prescribes
# --------------------------------------------------------------------------


def test_the_scan_reproduces_the_sections_own_candidates():
    """9:02 to 9:08, a minute at a time, is seven candidates."""
    nine_oh_two = 9 * 60 + 2
    candidates = birthtime.scan_over_range(nine_oh_two, 9 * 60 + 8)
    assert len(candidates) == 7
    assert candidates[0] == nine_oh_two
    assert candidates[-1] == 9 * 60 + 8
    assert [c - nine_oh_two for c in candidates[:3]] == [0.0, 1.0, 2.0]


def test_the_scan_step_is_coarser_than_the_argument():
    """FINDING: two minutes makes a different native, and the grid is one."""
    assert "wrong by 2 minutes" in birthtime.TWINS_PROVE_THE_VARGAS_MATTER
    assert "9:02, 9:03, 9:04" in birthtime.THE_SCAN_OVER_THE_REPORTED_RANGE
    coarse = birthtime.scan_over_range(9 * 60 + 2, 9 * 60 + 8)
    assert len(coarse) == 7
    # At the resolution the argument asks for there is more to try, not less.
    fine = birthtime.scan_over_range(9 * 60 + 2, 9 * 60 + 8,
                                     step_minutes=0.25)
    assert len(fine) == 25
    assert "half the resolution" not in birthtime.THE_SCAN_OVER_THE_REPORTED_RANGE
    assert "Seven candidates" in (
        birthtime.THE_SCAN_STEP_IS_COARSER_THAN_THE_ARGUMENT)


def test_scan_over_range_rejects_an_inverted_range_and_a_dead_step():
    with pytest.raises(birthtime.BirthtimeError, match="must not precede"):
        birthtime.scan_over_range(10.0, 5.0)
    with pytest.raises(birthtime.BirthtimeError, match="step_minutes"):
        birthtime.scan_over_range(5.0, 10.0, step_minutes=0.0)


def test_the_acid_test_leaves_too_far_apart_undecided():
    """GAP: "the same" is exact and "too far apart" has no threshold."""
    got = birthtime.acid_test_of_twins(birthtime.nearest_quantum, 0.5)
    assert got["rectified_gap_minutes"] == pytest.approx(3.5)
    assert got["collapsed_to_one_time"] is False
    assert got["passes"] is None
    assert got["reason"] is birthtime.THE_ACID_TEST_GIVES_NO_THRESHOLD
    assert got["tolerance_minutes"] is None

    # Supplying a tolerance decides it, in either direction.
    assert birthtime.acid_test_of_twins(
        birthtime.nearest_quantum, 0.5, tolerance_minutes=0.5)["passes"] is (
        False)
    assert birthtime.acid_test_of_twins(
        birthtime.nearest_quantum, 0.5, tolerance_minutes=2.0)["passes"] is (
        True)

    # A collapse needs no threshold: it is decided from the section itself.
    collapsed = birthtime.acid_test_of_twins(lambda m: 0.0, 0.0)
    assert collapsed["collapsed_to_one_time"] is True
    assert collapsed["passes"] is False
    assert "rectify to one time" in str(collapsed["reason"])

    assert "how far is too far" in birthtime.THE_ACID_TEST_GIVES_NO_THRESHOLD


def test_the_acid_test_rejects_a_negative_tolerance():
    with pytest.raises(birthtime.BirthtimeError, match="not be negative"):
        birthtime.acid_test_of_twins(birthtime.nearest_quantum, 0.0,
                                     tolerance_minutes=-1.0)


# --------------------------------------------------------------------------
# §32.2 Robustness of Computations — §32.2.1 Divisional Charts
# --------------------------------------------------------------------------


def test_section_32_2_is_transcribed_and_labels_itself_approximate():
    assert birthtime.SECTION_32_2_TITLE == "Robustness of Computations"
    assert birthtime.SECTION_32_2_1_TITLE == "Divisional Charts"
    assert "**approximate** impact of birthtime change" in (
        birthtime.ROBUSTNESS_IS_APPROXIMATE)
    assert "Sun stays in one rasi for 30 days" in (
        birthtime.PLANETS_CHANGE_VERY_SLOWLY)
    assert "60/24=2.5" in birthtime.PLANETS_CHANGE_VERY_SLOWLY
    assert "most important consideration in birthtime rectification" in (
        birthtime.LAGNA_IS_THE_MOST_IMPORTANT_CONSIDERATION)
    assert "footnote 90" in birthtime.FOOTNOTE_90_NOT_SUPPLIED


def test_every_figure_the_section_prints_follows_from_its_own_rule():
    for row in birthtime.ROBUSTNESS_FIGURES:
        varga = int(row["varga"])
        if varga == 1:
            continue
        whole = next(r for r in birthtime.ROBUSTNESS_FIGURES
                     if r["body"] == row["body"] and r["varga"] == 1)
        got = birthtime.varga_rasi_change_interval(
            float(whole["rasi_interval_minutes"]), varga)
        assert got["interval"] == pytest.approx(
            float(row["rasi_interval_minutes"])), (row["body"], varga)
    # And the printed arithmetic itself.
    assert 30 / 10 == 3
    assert 30 / 24 == 1.25
    assert 60 / 10 == 6
    assert 60 / 24 == 2.5
    assert 120 / 10 == 12
    assert 120 / 24 == 5
    assert "12 min" in birthtime.LAGNA_CHANGES_RASI_IN_D10_IN_TWELVE_MINUTES
    assert "D-24 in 5" in birthtime.LAGNA_CHANGES_RASI_IN_D10_IN_TWELVE_MINUTES


def test_the_divide_by_n_rule_has_exactly_one_exception():
    """FINDING: every varga but D-30 cuts the rasi into equal parts."""
    step = 0.001
    for number, function in _VARGAS.items():
        for rasi in (0, 1):                       # one odd, one even
            bounds, previous, degree = [], None, 0.0
            while degree < 30.0:
                sign = int(function(rasi * 30 + degree).sign)
                if previous is not None and sign != previous:
                    bounds.append(degree)
                previous = sign
                degree += step
            spans = [b - a for a, b in
                     zip([0.0] + bounds, bounds + [30.0], strict=True)]
            spread = max(spans) - min(spans)
            if number in birthtime.UNEQUAL_VARGAS:
                assert spread > 1.0, number
                assert sorted(round(s) for s in spans) == [5, 5, 5, 7, 8]
            else:
                assert spread < 2 * step, (number, spread)

    assert birthtime.UNEQUAL_VARGAS == (30,)
    assert "all of them but D-30" in (
        birthtime.THE_DIVIDE_BY_N_RULE_HAS_ONE_EXCEPTION)


def test_d30_comes_back_as_a_range_and_not_a_figure():
    """The lagna's D-30 sign lasts 20 to 32 minutes, not the rule's 4."""
    got = birthtime.varga_rasi_change_interval(120.0, 30)
    assert got["equal_parts"] is False
    assert got["interval"] is None
    assert got["shortest"] == pytest.approx(20.0)
    assert got["longest"] == pytest.approx(32.0)
    # What the rule would have said, and what it is out by.
    assert 120.0 / 30 == 4.0
    assert float(got["shortest"]) / 4.0 == pytest.approx(5.0)
    assert float(got["longest"]) / 4.0 == pytest.approx(8.0)

    equal = birthtime.varga_rasi_change_interval(120.0, 24)
    assert equal["equal_parts"] is True
    assert equal["interval"] == equal["shortest"] == equal["longest"] == 5.0


def test_varga_rasi_change_interval_rejects_bad_inputs():
    with pytest.raises(birthtime.BirthtimeError, match="must be positive"):
        birthtime.varga_rasi_change_interval(0.0, 10)
    from hora.core.validate import InputError

    with pytest.raises(InputError, match="varga must be between"):
        birthtime.varga_rasi_change_interval(120.0, 0)


def test_the_sections_figures_are_means_measured_against_the_ephemeris():
    """FINDING: the Sun's 30 days is good to 2%, the Moon's 60 hours is 10%
    high, and the section bolds "approximate" in its own first sentence.
    """
    place = Place(name="mean", latitude=0.0, longitude=0.0)
    base = from_local(2000, 1, 1, 0, 0, 0.0, utc_offset_hours=0.0).jd_ut

    def spans(graha: int, steps: int, per_day: int) -> list[float]:
        previous, started, out = None, 0, []
        for index in range(steps):
            rasi = int(compute_chart(
                from_jd(base + index / per_day), place,
                _SETTINGS).positions[graha].longitude // 30)
            if rasi != previous:
                if previous is not None:
                    out.append((index - started) / per_day)
                previous, started = rasi, index
            
        return out[1:]                        # the first one starts mid-rasi

    sun = spans(int(Graha.SUN), 800 * 8, 8)
    assert 29.3 < min(sun) < 29.5
    assert 31.3 < max(sun) < 31.5
    assert sum(sun) / len(sun) == pytest.approx(30.4, abs=0.1)

    moon = [s * 24 for s in spans(int(Graha.MOON), 366 * 24 * 4, 96)]
    assert 47.0 < min(moon) < 48.0
    assert 61.0 < max(moon) < 62.0
    assert sum(moon) / len(moon) == pytest.approx(54.7, abs=0.2)
    # The section's 60 hours is nearer the maximum than the mean.
    assert abs(60 - max(moon)) < abs(60 - sum(moon) / len(moon))

    assert "approximate" in birthtime.ROBUSTNESS_IS_APPROXIMATE
    assert "47.5 to 61.2 hours" in (
        birthtime.THE_SECTIONS_FIGURES_ARE_MEANS_AND_IT_SAYS_SO)


def test_the_moon_paragraph_carries_two_speeds():
    """FINDING: 2.0 minutes per arcminute from one sentence, 1.8 from the
    next, and 1.82 measured. The section computes with the accurate one.
    """
    from_the_rasi_figure = (60 * 60.0) / (30 * 60)         # 3600 min / 1800'
    from_the_nakshatra_sentence = 360.0 / 200.0
    assert from_the_rasi_figure == pytest.approx(2.0)
    assert from_the_nakshatra_sentence == pytest.approx(1.8)
    assert "360/200=1.8 min" in birthtime.THE_MOON_AT_A_DASAMSA_BORDER
    assert "60/10=6 hours" in birthtime.PLANETS_CHANGE_VERY_SLOWLY

    # The measured mean, from the Moon's real rasi time.
    measured = (54.7 * 60.0) / (30 * 60)
    assert measured == pytest.approx(1.82, abs=0.01)
    assert abs(measured - from_the_nakshatra_sentence) < abs(
        measured - from_the_rasi_figure)
    assert "the accurate one" in birthtime.THE_MOON_PARAGRAPH_CARRIES_TWO_SPEEDS


def test_the_dasamsa_border_reproduces():
    """FINDING: 23 Sc 59 gives Aquarius and 24 Sc 00 gives Pisces."""
    from hora.core.const import RASI_LORD

    scorpio = RASI_ABBR.index("Sc") * 30
    below = vargas.d10_dasamsa(scorpio + 23 + 59 / 60)
    at = vargas.d10_dasamsa(scorpio + 24.0)
    assert RASI_ABBR[int(below.sign)] == "Aq"
    assert RASI_ABBR[int(at.sign)] == "Pi"

    # The 8th and the 9th dasamsa of a three-degree grid.
    assert int((23 + 59 / 60) // 3) + 1 == 8
    assert int(24.0 // 3) + 1 == 9

    # The lagna-lord argument: D-10 lagna in Cancer makes the Moon the lord,
    # so it is the Moon's own position that moves him between houses.
    cancer = RASI_ABBR.index("Cn")
    assert int(RASI_LORD[cancer]) == int(Graha.MOON)
    assert (int(below.sign) - cancer) % 12 + 1 == 8
    assert (int(at.sign) - cancer) % 12 + 1 == 9
    assert "the Moon himself" in birthtime.THE_DASAMSA_BORDER_REPRODUCES


def test_both_sides_of_the_border_come_back_for_the_sections_own_case():
    """The rule the section states: consider both positions."""
    scorpio = RASI_ABBR.index("Sc") * 30
    # One arcminute either side of 23 Sc 59.5 straddles the border.
    both = birthtime.signs_across_the_uncertainty(
        scorpio + 23 + 59.5 / 60, vargas.d10_dasamsa, arcminutes=1.0)
    assert [RASI_ABBR[s] for s in both] == ["Aq", "Pi"]

    # Away from the border, one sign comes back and there is nothing to weigh.
    alone = birthtime.signs_across_the_uncertainty(
        scorpio + 22.0, vargas.d10_dasamsa, arcminutes=1.0)
    assert [RASI_ABBR[s] for s in alone] == ["Aq"]

    # Zero uncertainty is the plain varga sign.
    assert birthtime.signs_across_the_uncertainty(
        scorpio + 24.0, vargas.d10_dasamsa, arcminutes=0.0) == (
        int(vargas.d10_dasamsa(scorpio + 24.0).sign),)

    assert "consider both the positions" in (
        birthtime.CONSIDER_BOTH_SIDES_OF_A_BORDER)


def test_signs_across_the_uncertainty_rejects_bad_inputs():
    with pytest.raises(birthtime.BirthtimeError, match="not be negative"):
        birthtime.signs_across_the_uncertainty(10.0, vargas.d9_navamsa,
                                               arcminutes=-1.0)
    with pytest.raises(birthtime.BirthtimeError, match="at least 2"):
        birthtime.signs_across_the_uncertainty(10.0, vargas.d9_navamsa,
                                               arcminutes=1.0, samples=1)


def test_the_lagna_outruns_the_fastest_graha_thirty_to_one():
    """FINDING: two minutes moves the lagna 30 arcminutes and the Moon one."""
    lagna_arcminutes = 2 * (60.0 / 4.0)                  # 1 degree in 4 min
    assert lagna_arcminutes == pytest.approx(30.0)
    moon_arcminutes = 2 / 1.8                            # the section's rate
    assert moon_arcminutes == pytest.approx(1.11, abs=0.01)
    assert lagna_arcminutes / moon_arcminutes == pytest.approx(27.0)

    # Against the Moon's measured speed the ratio is thirty to one.
    assert lagna_arcminutes / (2 / 1.82) == pytest.approx(27.3, abs=0.1)
    assert "the most important consideration" in (
        birthtime.LAGNA_IS_THE_MOST_IMPORTANT_CONSIDERATION)
    assert "30 arcminutes and the Moon moves 1.1" in (
        birthtime.THE_LAGNA_OUTRUNS_THE_FASTEST_GRAHA_THIRTY_TO_ONE)


def test_the_lesson_is_one_rate_stated_four_ways():
    """FINDING: fifteen arcseconds of lagna per second of clock, four times."""
    assert "Lagna moves by 1 degree in 4 min" in birthtime.LESSON
    assert len(birthtime.LESSON_ROWS) == 4
    for row in birthtime.LESSON_ROWS:
        rate = float(row["arc_arcseconds"]) / float(row["seconds"])
        assert rate == pytest.approx(15.0), row["as_printed"]
    # And that is the two-hour rasi the section starts from.
    assert 30 * 3600 / 15.0 == pytest.approx(120 * 60)
    assert "15 arcseconds of lagna per second of clock" in (
        birthtime.THE_LESSON_IS_ONE_RATE_STATED_FOUR_WAYS)
