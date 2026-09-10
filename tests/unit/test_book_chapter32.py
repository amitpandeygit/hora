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
    assert "unresolved controversies" in birthtime.FOOTNOTE_90


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


# --------------------------------------------------------------------------
# Footnote 90 — the ephemeris itself
# --------------------------------------------------------------------------


def test_footnote_90_is_transcribed_and_its_two_knobs_already_exist():
    from hora.core.settings import Ayanamsa

    assert "computation of Moon's longitude is very accurate" in (
        birthtime.FOOTNOTE_90)
    assert "(1) ayanamsa and (2) geocentric positions vs topocentric" in (
        birthtime.FOOTNOTE_90)
    assert "consider both the rasis in border-line situations" in (
        birthtime.FOOTNOTE_90)

    controversies = birthtime.FOOTNOTE_90_CONTROVERSIES
    assert [c["number"] for c in controversies] == [1, 2]
    # Both are settings we already carry, and both defaults stand.
    fresh = Settings()
    assert fresh.ayanamsa is Ayanamsa.LAHIRI
    assert fresh.topocentric is False
    assert controversies[0]["our_default"] == "lahiri"
    assert controversies[1]["our_default"] == "geocentric"
    assert "nothing here proposes changing either" in (
        birthtime.THE_FOOTNOTE_NAMES_NO_WINNER)


def test_the_ayanamsa_spread_in_the_moon_is_measured():
    """FINDING: 5.8 arcminutes inside the Lahiri family, 139.8 across six."""
    from hora.core.settings import Ayanamsa

    when = from_local(2000, 4, 9, 13, 35, 0.0, utc_offset_hours=-5.0)

    def moon(ayanamsa: Ayanamsa) -> float:
        return compute_chart(
            when, _PLACE,
            Settings(node_type=NodeType.MEAN, ayanamsa=ayanamsa),
        ).positions[int(Graha.MOON)].longitude

    family = [moon(a) for a in (Ayanamsa.LAHIRI, Ayanamsa.LAHIRI_ICRC,
                                Ayanamsa.KRISHNAMURTI, Ayanamsa.TRUE_CITRA)]
    assert (max(family) - min(family)) * 60 == pytest.approx(5.8, abs=0.1)

    wider = family + [moon(a) for a in (Ayanamsa.RAMAN, Ayanamsa.YUKTESHWAR,
                                        Ayanamsa.FAGAN_BRADLEY)]
    assert (max(wider) - min(wider)) * 60 == pytest.approx(139.8, abs=0.5)

    # Against the one arcminute the section's own border turns on.
    assert (max(wider) - min(wider)) * 60 > 100
    assert "one arcminute" in (
        birthtime.THE_TWO_CONTROVERSIES_DWARF_THE_BORDER_THEY_ANNOTATE)


def test_parallax_is_a_moon_problem_and_reaches_fifty_five_arcminutes():
    """FINDING: geocentric against topocentric, over thirty days."""
    from hora.core.timeutil import norm180

    geocentric = Settings(node_type=NodeType.MEAN)
    topocentric = Settings(node_type=NodeType.MEAN, topocentric=True)
    when = from_local(2000, 4, 9, 13, 35, 0.0, utc_offset_hours=-5.0)

    # Every other graha is unmoved; the Moon is not.
    here = compute_chart(when, _PLACE, geocentric)
    there = compute_chart(when, _PLACE, topocentric)
    for graha in (Graha.SUN, Graha.MARS, Graha.JUPITER, Graha.SATURN):
        shift = abs(there.positions[int(graha)].longitude
                    - here.positions[int(graha)].longitude) * 60
        assert shift < 0.2, graha
    moon_shift = abs(there.positions[int(Graha.MOON)].longitude
                     - here.positions[int(Graha.MOON)].longitude) * 60
    assert moon_shift > 20

    base = from_local(2000, 4, 9, 0, 0, 0.0, utc_offset_hours=-5.0).jd_ut
    peak = 0.0
    for index in range(30 * 24):                   # hourly over thirty days
        at = from_jd(base + index / 24.0)
        difference = norm180(
            compute_chart(at, _PLACE, topocentric).positions[
                int(Graha.MOON)].longitude
            - compute_chart(at, _PLACE, geocentric).positions[
                int(Graha.MOON)].longitude) * 60
        peak = max(peak, abs(difference))
    assert peak == pytest.approx(55.0, abs=1.0)
    assert "reaches 55" in (
        birthtime.THE_TWO_CONTROVERSIES_DWARF_THE_BORDER_THEY_ANNOTATE)


def test_the_footnote_widens_the_rule_from_time_to_position():
    """FINDING: same instruction, second and larger reason."""
    assert "if a planet is at a border" in birthtime.THE_MOON_AT_A_DASAMSA_BORDER
    assert "consider both the positions" in (
        birthtime.CONSIDER_BOTH_SIDES_OF_A_BORDER)
    assert "consider both the rasis" in birthtime.FOOTNOTE_90
    # The helper does not care where the uncertainty came from.
    scorpio = RASI_ABBR.index("Sc") * 30
    from_time = birthtime.signs_across_the_uncertainty(
        scorpio + 23 + 59.5 / 60, vargas.d10_dasamsa, arcminutes=1.0)
    from_ephemeris = birthtime.signs_across_the_uncertainty(
        scorpio + 23 + 59.5 / 60, vargas.d10_dasamsa, arcminutes=5.8)
    assert from_time == from_ephemeris
    assert "the second reason is the larger one" in (
        birthtime.THE_FOOTNOTE_WIDENS_THE_RULE_FROM_TIME_TO_POSITION)


def test_d69_is_the_footnotes_own_case():
    """FINDING: 1.5 arcminutes of ayanamsa, a whole sign in D-20."""
    from pathlib import Path

    text = Path("docs/book-deviations.md").read_text(encoding="utf-8")
    assert "D-69 · Chart 49 restates Chart 37's nativity" in text
    assert "Venus in D-20" in text

    from hora.charts.book import longitudes

    thirty_seven, forty_nine = longitudes(37), longitudes(49)
    for name in ("Sun", "Moon", "Mars"):
        apart = abs(forty_nine[name] - thirty_seven[name]) * 60
        assert apart == pytest.approx(1.0, abs=0.2)

    # And an arcminute of it is enough to move a D-20 sign.
    a = int(vargas.d20_vimsamsa(thirty_seven["Ven"]).sign)
    b = int(vargas.d20_vimsamsa(forty_nine["Ven"]).sign)
    assert RASI_ABBR[a] == "Ar"
    assert RASI_ABBR[b] == "Ta"
    assert "D-69 is the instance" in birthtime.D69_IS_THE_FOOTNOTES_OWN_CASE


def test_oi_182_is_open_and_says_what_it_needs():
    from pathlib import Path

    text = Path("docs/open-items.md").read_text(encoding="utf-8")
    assert "### OI-182 — footnote 90 says the ephemeris itself is uncertain" in (
        text)
    assert "| OI-182 |" in text
    entry = text.split("### OI-182")[1].split("### ")[0]
    assert "**Closes when:**" in entry
    assert "nothing here proposes\nchanging either" in entry


# --------------------------------------------------------------------------
# Example 129
# --------------------------------------------------------------------------

_SG = RASI_ABBR.index("Sg") * 30


def test_example_129_is_transcribed():
    text = birthtime.EXAMPLE_129
    assert "Suppose lagna is at 4Sg39" in text
    assert "3Sg24-3Sg45: Li" in text
    assert "81x4 sec = 324 sec = 5 min 24 sec" in text
    assert "it has to be more than 5 minutes in this case" in text
    assert "That is not the case in reality" in text
    assert "That familiarity is a necessity for quick birthtime rectification" in (
        text)
    assert len(text.split("\n\n")) == 7


def test_the_three_lagnas_as_reported_reproduce():
    stated = birthtime.EXAMPLE_129_STATED
    degree = float(stated["lagna_degree_in_rasi"])
    assert degree == pytest.approx(4 + 39 / 60)
    for number, expected in dict(stated["lagnas_as_reported"]).items():
        got = _VARGAS[int(number)](_SG + degree)
        assert RASI_ABBR[int(got.sign)] == expected, number


def test_the_five_minute_window_is_one_and_a_quarter_degrees():
    stated = birthtime.EXAMPLE_129_STATED
    assert float(stated["maximum_error_minutes"]) == 5.0
    # The Lesson's rate, inverted: 4 minutes a degree.
    assert 5 / 4 == 1.25
    low, high = (float(x) for x in stated["range_degrees_in_rasi"])
    assert low == pytest.approx(4 + 39 / 60 - 1.25)
    assert high == pytest.approx(4 + 39 / 60 + 1.25)
    assert stated["range"] == ("3 Sg 24", "5 Sg 54")


def test_the_windows_in_all_three_vargas_reproduce():
    """FINDING: one D-10 sign, two D-12 signs, three D-24 signs."""
    stated = birthtime.EXAMPLE_129_STATED
    low, high = (float(x) for x in stated["range_degrees_in_rasi"])
    for number, printed in dict(stated["windows"]).items():
        got = birthtime.lagna_windows(_SG + low, _SG + high,
                                      _VARGAS[int(number)])
        assert len(got) == len(printed), number
        for ours, (bounds, sign) in zip(got, printed, strict=True):
            assert RASI_ABBR[int(ours["sign"])] == sign, (number, sign)
            assert float(ours["from"]) - _SG == pytest.approx(
                bounds[0], abs=1e-6)
            assert float(ours["to"]) - _SG == pytest.approx(
                bounds[1], abs=1e-6)

    # The borders themselves are where the example says they are.
    d12 = birthtime.lagna_windows(_SG + low, _SG + high, _VARGAS[12])
    assert float(d12[0]["to"]) - _SG == pytest.approx(5.0, abs=1e-6)
    d24 = birthtime.lagna_windows(_SG + low, _SG + high, _VARGAS[24])
    assert [round(float(w["to"]) - _SG, 4) for w in d24[:2]] == [3.75, 5.0]
    assert "No ephemeris is needed" in (
        birthtime.EXAMPLE_129_REPRODUCES_FROM_BORDERS_ALONE)


def test_the_shift_to_the_next_d10_border_reproduces():
    stated = birthtime.EXAMPLE_129_STATED
    # 6 Sg 00 is the next D-10 border above 4 Sg 39, and it gives Aquarius.
    assert float(stated["next_d10_border"]) == 6.0
    assert RASI_ABBR[int(_VARGAS[10](_SG + 6.0).sign)] == "Aq"
    assert RASI_ABBR[int(_VARGAS[10](_SG + 6.0 - 1e-9).sign)] == "Cp"

    shortfall = (6.0 - float(stated["lagna_degree_in_rasi"])) * 60
    assert shortfall == pytest.approx(81.0)
    assert birthtime.seconds_to_move(shortfall) == pytest.approx(324.0)
    assert 324 == 5 * 60 + 24
    assert stated["rectified_birthtime"] == "9:10:24"


def test_the_answer_leaves_the_reported_window_and_the_example_says_so():
    """FINDING: the known past outranks the reported bound."""
    # 9:05 plus 5 min 24 sec is 9:10:24; the native's window ended at 9:10.
    assert 9 * 3600 + 5 * 60 + 324 == 9 * 3600 + 10 * 60 + 24
    assert "birthtime can be 9:00-9:10" in birthtime.EXAMPLE_129
    assert "it has to be more than 5 minutes" in birthtime.EXAMPLE_129
    # It is the four causes of section 32.1 that make a reported bound soft.
    assert len(birthtime.BIRTHTIME_ERROR_CAUSES) == 4
    assert "outranks the reported bound" in (
        birthtime.THE_ANSWER_LEAVES_THE_REPORTED_WINDOW_AND_THE_EXAMPLE_SAYS_SO)


def test_the_uniform_lagna_caveat_measured_at_four_latitudes():
    """FINDING: 5 min 24 sec always lands short of 6 Sg 00, by 5 to 10
    arcminutes, and always needs another 21 to 42 seconds.
    """
    from hora.core.timeutil import norm180

    target = _SG + 4 + 39 / 60
    six = _SG + 6.0
    shortfalls, extras = [], []
    for latitude, longitude in ((16 + 15 / 60, 81 + 12 / 60),
                                (42.5, -(71 + 12 / 60)),
                                (0.0, 0.0),
                                (60.0, 0.0)):
        place = Place(name="E129", latitude=latitude, longitude=longitude)
        offset = round(longitude / 15 * 2) / 2

        def at(jd: float, place: Place = place) -> float:
            return compute_chart(from_jd(jd), place, _SETTINGS).lagna_longitude

        # An instant where the lagna really is 4 Sg 39 at 9:05 local.
        start = from_local(2000, 1, 1, 9, 5, 0.0,
                           utc_offset_hours=offset).jd_ut
        best = min(((start + day, abs(norm180(at(start + day) - target)))
                    for day in range(366)), key=lambda pair: pair[1])
        jd = best[0]
        for second in range(-1800, 1800, 5):
            here = jd + second / 86400.0
            if abs(norm180(at(here) - target)) < best[1]:
                jd, best = here, (here, abs(norm180(at(here) - target)))
        assert best[1] * 60 < 3.0                     # within 3 arcminutes

        after = at(jd + 324 / 86400.0)
        assert after < six                            # always short
        shortfalls.append((six - after) * 60)

        low, high = 0.0, 900.0
        for _ in range(50):
            middle = (low + high) / 2
            if at(jd + middle / 86400.0) < six:
                low = middle
            else:
                high = middle
        extras.append(high - 324.0)

    assert 5.0 < min(shortfalls) and max(shortfalls) < 10.0
    assert 20.0 < min(extras) and max(extras) < 45.0
    assert "5 to 10 arcminutes short" in (
        birthtime.THE_UNIFORM_LAGNA_IS_THE_SECTIONS_OWN_CAVEAT)


def test_the_book_states_the_mean_is_not_a_rate():
    """FINDING: what 32.1 stated flatly, Example 129 withdraws."""
    assert "Lagna in D-1 changes rasi once in 2 hours" in (
        birthtime.WE_MUST_FIRST_HAVE_AN_ACCURATE_BIRTHTIME)
    assert "**approximate**" in birthtime.ROBUSTNESS_IS_APPROXIMATE
    assert ("lagna moves uniformly. That is not the case in reality" in
            birthtime.EXAMPLE_129)
    assert "119.7 minutes" in birthtime.THE_TWO_HOURS_IS_A_MEAN_NOT_A_RATE
    assert "The remedy offered is to iterate" in (
        birthtime.THE_BOOK_STATES_THE_MEAN_IS_NOT_A_RATE)


def test_the_closing_sentence_is_a_requirement_and_we_answer_it():
    """FINDING: what the astrologer is asked to memorise, we compute —
    including D-30, whose borders are not multiples of anything.
    """
    assert "familiar with the longitudes at which lagna changes rasi" in (
        birthtime.EXAMPLE_129)
    # An equal varga: the borders are multiples, as the example expects.
    equal = birthtime.lagna_windows(_SG, _SG + 30.0, _VARGAS[24])
    assert len(equal) == 24
    for index, window in enumerate(equal):
        assert float(window["from"]) - _SG == pytest.approx(index * 1.25,
                                                            abs=1e-6)
    # D-30's are not.
    unequal = birthtime.lagna_windows(_SG, _SG + 30.0, _VARGAS[30])
    edges = [round(float(w["to"]) - _SG, 4) for w in unequal]
    assert edges == [5.0, 10.0, 18.0, 25.0, 30.0]
    assert len(unequal) == 5
    assert 30 in birthtime.UNEQUAL_VARGAS
    assert "D-30's unequal borders included" in (
        birthtime.THE_CLOSING_SENTENCE_IS_A_REQUIREMENT_NOT_ADVICE)


def test_lagna_windows_rejects_a_bad_range():
    with pytest.raises(birthtime.BirthtimeError, match="must not precede"):
        birthtime.lagna_windows(20.0, 10.0, _VARGAS[9])
    with pytest.raises(birthtime.BirthtimeError, match="one rasi"):
        birthtime.lagna_windows(0.0, 40.0, _VARGAS[9])


# --------------------------------------------------------------------------
# §32.2.1 continued — Special Lagnas and the second Lesson
# --------------------------------------------------------------------------


def test_the_special_lagna_paragraph_and_lesson_are_transcribed():
    assert "Hora lagna moves twice as fast as lagna" in (
        birthtime.SPECIAL_LAGNAS_ARE_FASTER_STILL)
    assert "Ghati lagna moves 5 times as fast as lagna" in (
        birthtime.SPECIAL_LAGNAS_ARE_FASTER_STILL)
    assert "HL moves by 1 degree in 2 min" in birthtime.LESSON_SPECIAL_LAGNAS
    assert "GL moves by 10' in 4.8 seconds" in birthtime.LESSON_SPECIAL_LAGNAS
    assert "less than half a second" in birthtime.LESSON_SPECIAL_LAGNAS
    assert len(birthtime.LESSON_SPECIAL_LAGNA_ROWS) == 7


def test_the_special_lagna_rates_are_exact_where_the_lagnas_is_a_mean():
    """FINDING: HL and GL advance by definition; the ascendant does not."""
    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    assert ADVANCE_PER_MINUTE[SpecialLagna.HORA] == 0.5
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] == 1.25
    # The section's two claims, against the nominal quarter-degree a minute.
    nominal = 30.0 / 120.0
    assert ADVANCE_PER_MINUTE[SpecialLagna.HORA] / nominal == 2.0
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] / nominal == 5.0
    # And the rates are exact, so the caveat Example 129 raises does not apply.
    assert "not the case in reality" in birthtime.EXAMPLE_129
    assert "only a mean" in (
        birthtime.THE_SPECIAL_LAGNA_RATES_ARE_EXACT_AND_THE_LAGNAS_IS_NOT)


def test_the_two_ratios_hold_only_against_the_mean_lagna():
    """FINDING: at 60 N the ascendant sometimes outruns Hora Lagna."""
    base = from_local(2000, 3, 20, 0, 0, 0.0, utc_offset_hours=0.0).jd_ut
    measured = {}
    for latitude in (42.5, 60.0):
        place = Place(name="ratio", latitude=latitude, longitude=0.0)
        rates = []
        for minute in range(0, 1440, 5):
            here = compute_chart(from_jd(base + minute / 1440.0), place,
                                 _SETTINGS).lagna_longitude
            later = compute_chart(from_jd(base + (minute + 1) / 1440.0), place,
                                  _SETTINGS).lagna_longitude
            rates.append((later - here) % 360)
        measured[latitude] = (min(rates), max(rates))

    slow, fast = measured[42.5]
    assert 0.5 / fast == pytest.approx(1.10, abs=0.05)
    assert 0.5 / slow == pytest.approx(2.59, abs=0.05)
    assert 1.25 / fast == pytest.approx(2.76, abs=0.05)

    slow, fast = measured[60.0]
    assert 0.5 / fast < 1.0                # the ascendant outruns Hora Lagna
    assert 1.25 / fast < 1.5               # and nearly matches Ghati Lagna
    assert "sometimes outruns Hora Lagna" in (
        birthtime.THE_TWO_RATIOS_HOLD_ONLY_AGAINST_THE_MEAN_LAGNA)


def test_bhava_lagna_is_omitted_because_its_row_would_repeat_the_lagnas():
    """FINDING: BL's rate is the ascendant's nominal rate exactly."""
    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    assert ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA] == 30.0 / 120.0
    for name in ("BL", "Bhava", "SL", "Sree"):
        assert name not in birthtime.LESSON_SPECIAL_LAGNAS
        assert name not in birthtime.SPECIAL_LAGNAS_ARE_FASTER_STILL
    # BL's row would be the first Lesson's rows, second for second.
    for row in birthtime.LESSON_ROWS:
        arc, seconds = float(row["arc_arcseconds"]), float(row["seconds"])
        assert arc / seconds == pytest.approx(15.0)
        assert arc / (ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA] * 3600 / 60) == (
            pytest.approx(seconds))
    assert "no fixed rate at all" in (
        birthtime.BHAVA_LAGNA_IS_OMITTED_BECAUSE_ITS_ROW_WOULD_REPEAT_THE_LAGNAS)


def test_d85_the_two_gl_rows_divide_a_degree_into_ten_arcminutes():
    """BOOK DEFECT D-85. The first GL row is right; the next two are it
    divided by ten and then ten again, and are the truth times 3/5.
    """
    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    rows = birthtime.LESSON_SPECIAL_LAGNA_ROWS
    hl = [r for r in rows if r["lagna"] == "HL"]
    gl = [r for r in rows if r["lagna"] == "GL"]

    # Every HL row is the same rate, and it is the one ADVANCE_PER_MINUTE has.
    hl_rate = ADVANCE_PER_MINUTE[SpecialLagna.HORA] * 3600 / 60   # "/sec
    assert hl_rate == pytest.approx(30.0)
    for row in hl:
        assert float(row["arc_arcseconds"]) / float(
            row["printed_seconds"]) == pytest.approx(hl_rate), row["as_printed"]

    gl_rate = ADVANCE_PER_MINUTE[SpecialLagna.GHATI] * 3600 / 60
    assert gl_rate == pytest.approx(75.0)
    # The first GL row agrees; the other two do not, and both by 5/3.
    assert float(gl[0]["arc_arcseconds"]) / float(
        gl[0]["printed_seconds"]) == pytest.approx(gl_rate)
    for row in gl[1:]:
        printed = float(row["printed_seconds"])
        correct = float(row["arc_arcseconds"]) / gl_rate
        assert printed != pytest.approx(correct)
        assert correct / printed == pytest.approx(5.0 / 3.0)
    assert [float(r["printed_seconds"]) for r in gl] == [48.0, 4.8, 0.48]
    assert [float(r["arc_arcseconds"]) / gl_rate for r in gl] == [
        pytest.approx(48.0), pytest.approx(8.0), pytest.approx(0.8)]

    # And the parenthesis goes with them.
    assert "less than half a second" in birthtime.LESSON_SPECIAL_LAGNAS
    assert 60.0 / gl_rate > 0.5

    from pathlib import Path

    text = Path("docs/book-deviations.md").read_text(encoding="utf-8")
    assert "## D-85 · §32.2.1's Lesson divides a degree into ten arcminutes" in (
        text)


# --------------------------------------------------------------------------
# Exercise 50
# --------------------------------------------------------------------------

_LE = RASI_ABBR.index("Le") * 30
_GL_DEGREES_PER_MINUTE = 1.25


def test_exercise_50_and_its_answer_are_transcribed():
    assert "has GL at 20Le37" in birthtime.EXERCISE_50
    assert "periods of power and authority" in birthtime.EXERCISE_50
    assert "3 deg 21' = 201'" in birthtime.EXERCISE_50_ANSWER
    assert "201 x 0.48 sec = 96.48 sec = 1 min 6.48 sec" in (
        birthtime.EXERCISE_50_ANSWER)
    assert "between 9:06:07 am and 9:08:31 am" in birthtime.EXERCISE_50_ANSWER
    assert "several inequations like the above" in birthtime.EXERCISE_50_ANSWER
    assert len(birthtime.EXERCISE_50_ANSWER.split("\n\n")) == 4


def test_every_rasi_and_border_the_exercise_names_is_right():
    """FINDING: Leo's 7th to 10th dasamsas are Aq, Pi, Ar, Ta."""
    stated = birthtime.EXERCISE_50_STATED
    here = float(stated["gl_degree_in_rasi"])
    assert RASI_ABBR[int(vargas.d10_dasamsa(_LE + here).sign)] == "Aq"
    borders = dict(stated["borders"])
    for degree, sign in ((float(borders["Aq_to_Pi"]), "Pi"),
                         (float(borders["Pi_to_Ar"]), "Ar"),
                         (float(borders["Ar_to_Ta"]), "Ta")):
        assert RASI_ABBR[int(vargas.d10_dasamsa(_LE + degree).sign)] == sign
        assert RASI_ABBR[int(
            vargas.d10_dasamsa(_LE + degree - 1e-9).sign)] != sign

    windows = birthtime.lagna_windows(_LE + here, _LE + here + 30.0,
                                      vargas.d10_dasamsa)
    aries = next(w for w in windows if RASI_ABBR[int(w["sign"])] == "Ar")
    assert float(aries["from"]) - _LE == pytest.approx(24.0, abs=1e-6)
    assert float(aries["to"]) - _LE == pytest.approx(27.0, abs=1e-6)
    assert "right throughout" in birthtime.EXERCISE_50S_RASIS_ARE_ALL_CORRECT


def test_d86_the_three_slips_in_exercise_50s_answer():
    """BOOK DEFECT D-86. The subtraction, the rate and the minute
    conversion are each wrong, and independently.
    """
    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    stated = birthtime.EXERCISE_50_STATED
    printed, correct = dict(stated["printed"]), dict(stated["correct"])

    # 1. the subtraction
    arc = (24.0 - float(stated["gl_degree_in_rasi"])) * 60
    assert arc == pytest.approx(203.0)
    assert float(printed["arc_arcminutes"]) == 201.0
    assert float(correct["arc_arcminutes"]) == pytest.approx(arc)

    # 2. the rate, which is D-85's
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] == _GL_DEGREES_PER_MINUTE
    seconds_per_arcminute = 60.0 / (_GL_DEGREES_PER_MINUTE * 60)
    assert seconds_per_arcminute == pytest.approx(0.8)
    assert 201 * 0.48 == pytest.approx(96.48)

    # 3. the minute conversion, in the book's own figures
    assert 96.48 - 60 == pytest.approx(36.48)
    assert "1 min 6.48 sec" in birthtime.EXERCISE_50_ANSWER

    assert float(correct["lower_seconds"]) == pytest.approx(
        arc * seconds_per_arcminute)
    assert float(correct["lower_seconds"]) == pytest.approx(162.4)

    # The upper bound uses the correct rate, so the width survives.
    assert 3 * 4 / 5 * 60 == pytest.approx(144.0)
    assert float(printed["width_seconds"]) == float(correct["width_seconds"])

    from pathlib import Path

    text = Path("docs/book-deviations.md").read_text(encoding="utf-8")
    assert "## D-86 · Exercise 50's answer puts GL in Pisces" in text


def test_d86_the_printed_birthtime_lands_in_pisces_on_a_real_chart():
    """BOOK DEFECT D-86, checked against the ephemeris. At +67 seconds the
    D-10 GL is still Pisces; at +162.4 it is 24 Le 00.
    """
    from hora.charts.special_lagna import SpecialLagna
    from hora.core.timeutil import norm180

    target = _LE + 20 + 37 / 60
    place = Place(name="E50", latitude=16 + 15 / 60, longitude=81 + 12 / 60)
    ephemeris = SwissEphemeris(_SETTINGS)

    def ghati(jd: float) -> float:
        chart = compute_chart(from_jd(jd), place, _SETTINGS)
        sunrise = ephemeris.sunrise(chart.instant.jd_ut - 1.5, place.latitude,
                                    place.longitude)
        while True:
            nxt = ephemeris.sunrise(sunrise + 0.5, place.latitude,
                                    place.longitude)
            if nxt is None or nxt > chart.instant.jd_ut:
                break
            sunrise = nxt
        return all_special_lagnas(
            sunrise_jd=sunrise, jd_ut=chart.instant.jd_ut,
            lagna_longitude=chart.lagna_longitude,
            moon_longitude=chart.positions[int(Graha.MOON)].longitude,
            settings=_SETTINGS)[int(SpecialLagna.GHATI)].longitude

    start = from_local(2000, 1, 1, 9, 5, 0.0, utc_offset_hours=5.5).jd_ut
    best = min(((start + day, abs(norm180(ghati(start + day) - target)))
                for day in range(400)), key=lambda pair: pair[1])
    jd = best[0]
    for second in range(-3000, 3000, 5):
        here = jd + second / 86400.0
        if abs(norm180(ghati(here) - target)) < best[1]:
            jd, best = here, (here, abs(norm180(ghati(here) - target)))
    assert best[1] * 60 < 0.1                       # within a tenth of a minute

    # The book's answer: +67 seconds.
    printed = ghati(jd + 67.0 / 86400.0)
    assert RASI_ABBR[int(vargas.d10_dasamsa(printed).sign)] == "Pi"

    # The corrected one lands on the border, and just past it gives Aries.
    corrected = ghati(jd + 162.4 / 86400.0)
    assert (corrected % 30) == pytest.approx(24.0, abs=0.01)
    assert RASI_ABBR[int(
        vargas.d10_dasamsa(ghati(jd + 170.0 / 86400.0)).sign)] == "Ar"


def test_the_ghati_lagna_method_needs_no_second_pass():
    """FINDING: Example 129 iterates because the ascendant is not uniform;
    Exercise 50 does not, because Ghati Lagna is.
    """
    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    assert "may be a little off" in birthtime.EXAMPLE_129
    assert "a little off" not in birthtime.EXERCISE_50_ANSWER
    assert "uniformly" not in birthtime.EXERCISE_50_ANSWER
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] == _GL_DEGREES_PER_MINUTE
    assert "needs iterating and Exercise 50's does not" in (
        birthtime.THE_GHATI_LAGNA_METHOD_NEEDS_NO_SECOND_PASS)


def test_window_for_varga_sign_reproduces_the_corrected_exercise():
    got = birthtime.window_for_varga_sign(
        _LE + 20 + 37 / 60, RASI_ABBR.index("Ar"), vargas.d10_dasamsa,
        degrees_per_minute=_GL_DEGREES_PER_MINUTE)
    assert got["found"] is True
    assert float(got["from_degrees"]) * 60 == pytest.approx(203.0, abs=1e-4)
    assert float(got["from_seconds"]) == pytest.approx(162.4, abs=1e-3)
    assert float(got["to_seconds"]) == pytest.approx(162.4 + 144.0, abs=1e-3)
    # 9:05 plus those is 9:07:42.4 to 9:10:06.4.
    assert 9 * 3600 + 5 * 60 + float(got["from_seconds"]) == pytest.approx(
        9 * 3600 + 7 * 60 + 42.4)


def test_window_for_varga_sign_reports_a_sign_it_cannot_reach():
    # A D-2 hora chart only ever holds Cancer and Leo.
    got = birthtime.window_for_varga_sign(
        0.0, RASI_ABBR.index("Sg"), vargas.d2_hora, degrees_per_minute=1.0)
    assert got["found"] is False
    assert got["from_seconds"] is None
    assert "not reached within one rasi" in str(got["reason"])

    with pytest.raises(birthtime.BirthtimeError, match="must be positive"):
        birthtime.window_for_varga_sign(0.0, 0, vargas.d9_navamsa,
                                        degrees_per_minute=0.0)


def test_narrow_down_is_the_last_lines_algorithm():
    """FINDING: several inequations intersected is the whole method."""
    assert "several inequations" in birthtime.EXERCISE_50_ANSWER

    gl = birthtime.window_for_varga_sign(
        _LE + 20 + 37 / 60, RASI_ABBR.index("Ar"), vargas.d10_dasamsa,
        degrees_per_minute=_GL_DEGREES_PER_MINUTE)
    # A second constraint on the same GL, in D-24, that overlaps it.
    d24 = birthtime.window_for_varga_sign(
        _LE + 20 + 37 / 60,
        int(vargas.d24_chaturvimsamsa(_LE + 24.5).sign),
        vargas.d24_chaturvimsamsa,
        degrees_per_minute=_GL_DEGREES_PER_MINUTE)
    both = birthtime.narrow_down([gl, d24])
    assert both["possible"] is True
    assert float(both["from_seconds"]) >= float(gl["from_seconds"])
    assert float(both["to_seconds"]) <= float(gl["to_seconds"])
    assert both["windows"] == 2

    # Constraints that cannot both hold say so rather than inventing a time.
    impossible = birthtime.narrow_down([
        {"found": True, "from_seconds": 0.0, "to_seconds": 10.0},
        {"found": True, "from_seconds": 20.0, "to_seconds": 30.0}])
    assert impossible["possible"] is False
    assert "do not overlap" in str(impossible["reason"])
    assert "narrow_down is that" in birthtime.THE_LAST_LINE_IS_THE_ALGORITHM


def test_narrow_down_rejects_nothing_and_unfound_windows():
    with pytest.raises(birthtime.BirthtimeError, match="at least one window"):
        birthtime.narrow_down([])
    with pytest.raises(birthtime.BirthtimeError, match="was not found"):
        birthtime.narrow_down([{"found": False}])


# --------------------------------------------------------------------------
# §32.2.2 Dasas
# --------------------------------------------------------------------------


def test_section_32_2_2_is_transcribed():
    assert birthtime.SECTION_32_2_2_TITLE == "Dasas"
    assert "Because lagna changes rasi once in 2 hours" in (
        birthtime.RASI_DASAS_ARE_ROBUST)
    assert "unless a planet changes rasi in the divisional chart" in (
        birthtime.NARAYANA_DASA_OF_VARGAS_IS_ROBUST)
    assert "nx360xm/(24x60) = (n x m)/4" in birthtime.NAKSHATRA_DASA_DATE_ERROR
    assert "the complete duration (and not just the remainder at birth)" in (
        birthtime.NAKSHATRA_DASA_DATE_ERROR)
    assert "It is almost 7 months!" in birthtime.KALACHAKRA_DATE_ERROR
    assert "futile to use pratyantardasas" in birthtime.KALACHAKRA_DATE_ERROR
    assert len(birthtime.KALACHAKRA_DATE_ERROR.split("\n\n")) == 3


def test_the_three_worked_error_figures_reproduce():
    for row in birthtime.DASA_ERROR_CASES:
        years, minutes = float(row["full_years"]), float(row["minutes"])
        got = (birthtime.nakshatra_dasa_date_error(years, minutes)
               if row["system"] == "nakshatra"
               else birthtime.kalachakra_date_error(years, minutes))
        assert float(got["days"]) == pytest.approx(float(row["days"]))
        assert got["subtract_from_dasa_dates"] is True

    # The printed arithmetic itself.
    assert 20 * 2 / 4 == 10
    assert 10 * 2 / 4 == 5
    assert 100 * 2 == 200
    assert 200 / 30.44 == pytest.approx(6.57, abs=0.01)     # "almost 7 months"


def test_the_two_dasa_lengths_are_the_whole_vimsottari_periods():
    from hora.dasha.nakshatra.systems import VIMSHOTTARI

    periods = dict(zip(VIMSHOTTARI.order, VIMSHOTTARI.years, strict=True))
    assert periods[Graha.VENUS] == 20
    assert periods[Graha.MOON] == 10
    assert sum(VIMSHOTTARI.years) == 120
    for row in birthtime.DASA_ERROR_CASES:
        if row["system"] != "nakshatra":
            continue
        lord = Graha.VENUS if row["lord"] == "Venus" else Graha.MOON
        assert periods[lord] == int(row["full_years"])


def test_the_printed_balances_play_no_part():
    """FINDING: seven years of Venus and three of the Moon are decoys."""
    for row in birthtime.DASA_ERROR_CASES:
        if row["remaining_years"] is None:
            continue
        assert int(row["remaining_years"]) != int(row["full_years"])
        by_full = birthtime.nakshatra_dasa_date_error(
            float(row["full_years"]), float(row["minutes"]))["days"]
        assert float(by_full) == pytest.approx(float(row["days"]))
        # The balance, used instead, would give a different answer.
        by_balance = birthtime.nakshatra_dasa_date_error(
            float(row["remaining_years"]), float(row["minutes"]))["days"]
        assert float(by_balance) != pytest.approx(float(row["days"]))
    assert "7 years of Venus dasa remains" in (
        birthtime.NAKSHATRA_DASA_WORKED_CASES)
    assert "3 years of Moon dasa were remaining" in (
        birthtime.NAKSHATRA_DASA_WORKED_CASES)
    assert "printed and unused" in birthtime.THE_PRINTED_BALANCES_PLAY_NO_PART


def test_the_twenty_four_hour_nakshatra_is_the_accurate_figure():
    """FINDING, measured: mean 24.34 hours, implying 54.76 hours a rasi."""
    place = Place(name="nakshatra", latitude=0.0, longitude=0.0)
    base = from_local(2000, 1, 1, 0, 0, 0.0, utc_offset_hours=0.0).jd_ut
    span = 360.0 / 27.0
    previous, started, spans = None, 0, []
    for index in range(366 * 24 * 4):
        which = int(compute_chart(
            from_jd(base + index / 96.0), place,
            _SETTINGS).positions[int(Graha.MOON)].longitude // span)
        if which != previous:
            if previous is not None:
                spans.append((index - started) / 96.0 * 24)
            previous, started = which, index
    spans = spans[1:]                       # the first one starts mid-nakshatra
    assert 20.9 < min(spans) < 21.1
    assert 27.2 < max(spans) < 27.4
    mean = sum(spans) / len(spans)
    assert mean == pytest.approx(24.34, abs=0.05)

    # Which implies a rasi of 54.8 hours, not section 32.2.1's 60.
    assert mean * 27 / 12 == pytest.approx(54.76, abs=0.1)
    assert "60/10=6 hours" in birthtime.PLANETS_CHANGE_VERY_SLOWLY
    assert "only the 60 is loose" in (
        birthtime.THE_TWENTY_FOUR_HOUR_NAKSHATRA_IS_THE_ACCURATE_FIGURE)


def test_the_derivation_uses_savana_years():
    """FINDING: 360 days to the year, which is OI-115's savana."""
    assert "nx360xm" in birthtime.NAKSHATRA_DASA_DATE_ERROR
    # The clean quarter only appears with 360 days to a year.
    assert 360 / (24 * 60) == pytest.approx(0.25)
    assert 365.2564 / (24 * 60) != pytest.approx(0.25, abs=1e-3)

    from pathlib import Path

    text = Path("docs/open-items.md").read_text(encoding="utf-8")
    assert "OI-115 — §16.2 uses savana years" in text
    assert "Evidence on OI-115, no change" in (
        birthtime.THE_DERIVATION_USES_SAVANA_YEARS)


def test_the_kalachakra_factor_is_four_because_a_pada_is_a_quarter():
    """FINDING: a navamsa is a quarter of a nakshatra, and the 360s cancel."""
    nakshatra = birthtime.nakshatra_dasa_date_error(100.0, 2.0)["days"]
    kalachakra = birthtime.kalachakra_date_error(100.0, 2.0)["days"]
    assert float(kalachakra) / float(nakshatra) == pytest.approx(4.0)

    # A pada takes a quarter of 24x60 minutes, and 360 cancels 360.
    assert 24 * 60 / 4 == 360
    assert 100 * 360 * 2 / 360 == pytest.approx(200.0)

    # The same quantity per arcminute is already in the Kalachakra module:
    # a pada is 200 arcminutes, so paramayush / 200 years each.
    from hora.dasha.nakshatra.kalachakra import (
        balance_per_arcminute,
        group_of,
        pada_sequence,
        paramayush,
        sub_group_of,
    )

    sequence = pada_sequence(group_of(1), sub_group_of(1), 1)
    assert paramayush(sequence) == 100
    assert balance_per_arcminute(sequence) == pytest.approx(100 / 200)
    assert "no divisor" in (
        birthtime.THE_KALACHAKRA_FACTOR_IS_FOUR_BECAUSE_A_PADA_IS_A_QUARTER)


def test_even_antardasas_are_swamped_at_two_minutes():
    """FINDING: 715 of 729 pratyantardasas and 17 of 81 antardasas are
    shorter than the 200-day error the section itself computes. Built from
    section 24.2's own wheel, not from a proportional model.
    """
    from hora.dasha.nakshatra.kalachakra import (
        antardasas,
        dasa_years,
        group_of,
        pada_sequence,
        paramayush,
        sub_group_of,
        wheel,
        wheel_position,
    )

    nakshatra = 1                                   # Aswini, savya, pada 1
    sequence = pada_sequence(group_of(nakshatra), sub_group_of(nakshatra), 1)
    total = paramayush(sequence)
    assert total == 100

    error = float(birthtime.kalachakra_date_error(total, 2.0)["days"])
    assert error == 200.0

    ring = wheel(group_of(nakshatra))
    start = wheel_position(nakshatra, 1)
    dasas, antas, pratyantas = [], [], []
    for step in range(9):
        index = (start + step) % 24
        years = dasa_years(ring[index])
        dasas.append(years * 360)
        for anta in antardasas(nakshatra, index, years):
            antas.append(float(anta["years"]) * 360)
            for pratya in antardasas(nakshatra, int(anta["position"]),
                                     float(anta["years"])):
                pratyantas.append(float(pratya["years"]) * 360)

    assert (len(dasas), len(antas), len(pratyantas)) == (9, 81, 729)
    assert sum(1 for d in dasas if d < error) == 0
    assert sum(1 for a in antas if a < error) == 17
    assert sum(1 for p in pratyantas if p < error) == 715
    assert min(antas) == pytest.approx(100.0)
    assert min(dasas) == pytest.approx(1800.0)

    finding = birthtime.EVEN_ANTARDASAS_ARE_SWAMPED_AT_TWO_MINUTES
    assert "715 of the 729" in finding
    assert "17 of the 81" in finding
    assert "the shortest of which is 100 days" in finding


def test_the_varga_ascendant_plays_no_part_in_a_varga_narayana_dasa():
    """FINDING: section 18.5 never asks for it, which is why the claim is as
    safe as it is.
    """
    import inspect

    from hora.dasha.rasi.narayana import varga_lagna

    parameters = inspect.signature(varga_lagna).parameters
    assert list(parameters) == ["divisions", "natal_lagna", "varga_signs",
                                "lord", "seed_house_number"]
    assert "varga_lagna" not in parameters
    # The D-24 ascendant is the fastest thing in the chart and is not an input.
    assert birthtime.varga_rasi_change_interval(120.0, 24)["interval"] == 5.0
    assert "never uses the varga ascendant" in (
        birthtime.THE_VARGA_ASCENDANT_PLAYS_NO_PART_IN_A_VARGA_NARAYANA_DASA)


def test_d87_the_rasi_lagna_is_left_out_of_the_narayana_claim():
    """BOOK DEFECT D-87. Four minutes across a rasi-lagna boundary moves the
    D-24 varga lagna with no graha changing rasi in D-24.
    """
    from hora.core.timeutil import from_jd
    from hora.dasha.rasi.narayana import varga_lagna

    base = from_local(2000, 4, 9, 13, 35, 0.0, utc_offset_hours=-5.0).jd_ut
    leo = RASI_ABBR.index("Le")
    low, high = base - 3 / 24, base
    for _ in range(60):
        middle = (low + high) / 2
        if int(compute_chart(from_jd(middle), _PLACE,
                             _SETTINGS).lagna_longitude // 30) < leo:
            low = middle
        else:
            high = middle

    rows, graha_rasis = [], []
    for offset in (-2, +2):
        chart = compute_chart(from_jd(high + offset / 1440.0), _PLACE,
                              _SETTINGS)
        signs = {g: int(vargas.d24_chaturvimsamsa(
            chart.positions[g].longitude).sign) for g in range(9)}
        graha_rasis.append(tuple(signs[g] for g in range(9)))
        rows.append((RASI_ABBR[int(chart.lagna_longitude // 30)],
                     varga_lagna(24, int(chart.lagna_longitude // 30), signs)))

    # Not one graha changes D-24 rasi across the four minutes.
    assert len(set(graha_rasis)) == 1

    (before_lagna, before), (after_lagna, after) = rows
    assert (before_lagna, after_lagna) == ("Cn", "Le")
    assert before["seed_house"] == after["seed_house"] == 12
    assert (before["seed_rasi_name"], after["seed_rasi_name"]) == (
        "Gemini", "Cancer")
    assert (before["lord_name"], after["lord_name"]) == ("Mercury", "Moon")
    assert (before["lagna_name"], after["lagna_name"]) == ("Leo", "Libra")

    # The first paragraph names the lagna; the second does not.
    assert "lagna changes rasi" in birthtime.RASI_DASAS_ARE_ROBUST
    assert "lagna" not in birthtime.NARAYANA_DASA_OF_VARGAS_IS_ROBUST

    from pathlib import Path

    text = Path("docs/book-deviations.md").read_text(encoding="utf-8")
    assert "## D-87 · §32.2.2's varga Narayana claim leaves out the rasi lagna" in (
        text)
    assert "The conclusion survives" in (
        birthtime.THE_RASI_LAGNA_IS_LEFT_OUT_OF_THE_NARAYANA_CLAIM)


def test_the_dasa_error_helpers_reject_bad_inputs():
    with pytest.raises(birthtime.BirthtimeError, match="full_dasa_years"):
        birthtime.nakshatra_dasa_date_error(0.0, 2.0)
    with pytest.raises(birthtime.BirthtimeError, match="paramayush_years"):
        birthtime.kalachakra_date_error(-1.0, 2.0)
    # A negative error moves the dates the other way, as the section says.
    earlier = birthtime.nakshatra_dasa_date_error(20.0, -2.0)
    assert float(earlier["days"]) == pytest.approx(-10.0)
    assert earlier["subtract_from_dasa_dates"] is False
    assert "and vice versa" in birthtime.NAKSHATRA_DASA_DATE_ERROR


# --------------------------------------------------------------------------
# §32.2.3 Tajaka Charts
# --------------------------------------------------------------------------

_TAJAKA_PLACE = Place(name="Tajaka", latitude=16 + 15 / 60,
                      longitude=81 + 12 / 60)
_TAJAKA_SETTINGS = Settings(node_type=NodeType.MEAN)


def _annual(minute_offset: int, settings: Settings = _TAJAKA_SETTINGS):
    """A real nativity's eleventh annual chart, cast from a shifted birth."""
    from hora.tajaka.annual import varsha_pravesh

    natal = compute_chart(
        from_local(1970, 4, 4, 17, 50 + minute_offset, 0.0,
                   utc_offset_hours=5.5), _TAJAKA_PLACE, settings)

    def sun_at(jd: float) -> float:
        return compute_chart(from_jd(jd, utc_offset_hours=5.5), _TAJAKA_PLACE,
                             settings).positions[int(Graha.SUN)].longitude

    got = varsha_pravesh(sun_at, natal.positions[int(Graha.SUN)].longitude,
                         natal.instant.jd_ut, 11)
    annual = compute_chart(from_jd(got["jd"], utc_offset_hours=5.5),
                           _TAJAKA_PLACE, settings)
    return natal.lagna_longitude, float(got["jd"]), annual.lagna_longitude


def test_section_32_2_3_is_transcribed():
    assert birthtime.SECTION_32_2_3_TITLE == "Tajaka Charts"
    assert "will also change by approximately x" in (
        birthtime.THE_TAJAKA_LAGNA_MOVES_WITH_THE_NATAL_ONE)
    assert "is in the *middle* of the 8th dasamsa in Sc" in (
        birthtime.THE_TAJAKA_BORDER_EXAMPLE)
    assert "half a minute before the reported birthtime" in (
        birthtime.THE_TAJAKA_BORDER_EXAMPLE)
    assert "can help in some cases" in (
        birthtime.THE_TAJAKA_CHART_CAN_SHOW_WHAT_THE_NATAL_ONE_HIDES)
    # The book's own truncation, kept.
    assert "taught in this boo or" in birthtime.THE_ACCURACY_ASSUMPTION
    assert "multiplied by 360 in the longitude of lagna" in (
        birthtime.AYANAMSA_MUST_BE_NONLINEAR)
    assert "**nonlinear**" in birthtime.AYANAMSA_MUST_BE_NONLINEAR


def test_the_annual_instant_tracks_the_birthtime_almost_exactly():
    """FINDING, measured: a birthtime shift of m moves the return by m."""
    from hora.core.timeutil import norm180

    base_natal, base_jd, base_annual = _annual(0)
    moved = {}
    for minutes in (1, 3, 5):
        natal, jd, annual = _annual(minutes)
        moved[minutes] = ((jd - base_jd) * 1440.0,
                          norm180(natal - base_natal) * 60,
                          norm180(annual - base_annual) * 60)

    for minutes, (instant, _, _) in moved.items():
        assert instant == pytest.approx(minutes, abs=0.02), minutes

    # And the annual lagna moves by about what the natal one does.
    _, natal_arc, annual_arc = moved[1]
    assert natal_arc == pytest.approx(14.5, abs=0.2)
    assert annual_arc == pytest.approx(17.3, abs=0.2)
    assert 0.5 < annual_arc / natal_arc < 2.0
    assert "1.006, 3.007 and 5.003 minutes" in (
        birthtime.THE_ANNUAL_INSTANT_TRACKS_THE_BIRTHTIME_ALMOST_EXACTLY)


def test_changing_the_ayanamsa_does_not_move_the_return_instant():
    """FINDING, measured: the ayanamsa cancels out of the solar return."""
    from hora.core.settings import Ayanamsa

    lahiri_natal, lahiri_jd, lahiri_annual = _annual(0)
    raman = Settings(node_type=NodeType.MEAN, ayanamsa=Ayanamsa.RAMAN)
    raman_natal, raman_jd, raman_annual = _annual(0, raman)

    # The instant does not move at all, to a couple of thousandths of a second.
    assert abs(raman_jd - lahiri_jd) * 86400 < 0.01

    # And both lagnas shift by the same amount, which is the ayanamsa change.
    natal_shift = raman_natal - lahiri_natal
    annual_shift = raman_annual - lahiri_annual
    assert natal_shift == pytest.approx(1.4463, abs=1e-3)
    assert annual_shift == pytest.approx(natal_shift, abs=1e-4)
    assert "matters only to a small extent" in (
        birthtime.AYANAMSA_MUST_BE_NONLINEAR)
    assert "cancels out of the return" in (
        birthtime.CHANGING_THE_AYANAMSA_DOES_NOT_MOVE_THE_RETURN_INSTANT)


def test_the_times_360_is_exact_against_the_engine():
    """FINDING: one arcminute of Sun costs 24 minutes and nearly 7 degrees."""
    from hora.core.timeutil import norm180
    from hora.tajaka.annual import varsha_pravesh

    natal = compute_chart(
        from_local(1970, 4, 4, 17, 50, 0.0, utc_offset_hours=5.5),
        _TAJAKA_PLACE, _TAJAKA_SETTINGS)

    def sun_at(jd: float) -> float:
        return compute_chart(from_jd(jd, utc_offset_hours=5.5), _TAJAKA_PLACE,
                             _TAJAKA_SETTINGS).positions[
                                 int(Graha.SUN)].longitude

    def annual_for(offset_arcminutes: float) -> tuple[float, float]:
        got = varsha_pravesh(
            sun_at,
            natal.positions[int(Graha.SUN)].longitude + offset_arcminutes / 60,
            natal.instant.jd_ut, 11)
        chart = compute_chart(from_jd(float(got["jd"]), utc_offset_hours=5.5),
                              _TAJAKA_PLACE, _TAJAKA_SETTINGS)
        return float(got["jd"]), chart.lagna_longitude

    base_jd, base_lagna = annual_for(0.0)
    for arcminutes, minutes, degrees in ((0.1, 2.44, 0.70), (1.0, 24.38, 6.88)):
        jd, lagna = annual_for(arcminutes)
        assert (jd - base_jd) * 1440 == pytest.approx(minutes, abs=0.05)
        assert norm180(lagna - base_lagna) == pytest.approx(degrees, abs=0.05)

    # The helper says the same thing without an ephemeris.
    got = birthtime.solar_return_amplification(1.0)
    assert float(got["instant_error_minutes"]) == pytest.approx(24.4, abs=0.1)
    assert float(got["amplification"]) == pytest.approx(365.2564, abs=0.01)
    assert "6.88 degrees" in (
        birthtime.THE_TIMES_360_IS_EXACT_AND_THE_BASELINE_DECIDES_THE_DAMAGE)


def test_lahiri_is_nearly_linear_over_the_modern_era_and_less_so_before():
    """FINDING: the baseline decides how much a linear formula costs."""
    import swisseph as swe

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    def worst_residual(low: int, high: int) -> float:
        years = list(range(low, high + 1))
        values = [swe.get_ayanamsa_ut(swe.julday(y, 1, 1, 0.0)) for y in years]
        count = len(years)
        sum_x, sum_y = sum(years), sum(values)
        sum_xx = sum(y * y for y in years)
        sum_xy = sum(y * v for y, v in zip(years, values, strict=True))
        slope = ((count * sum_xy - sum_x * sum_y)
                 / (count * sum_xx - sum_x * sum_x))
        intercept = (sum_y - slope * sum_x) / count
        return max(abs(v - (intercept + slope * y)) * 60
                   for y, v in zip(years, values, strict=True))

    modern = worst_residual(1900, 2100)
    ancient = worst_residual(1000, 2100)
    assert modern == pytest.approx(0.014, abs=0.003)
    assert ancient == pytest.approx(0.371, abs=0.02)
    assert ancient > 20 * modern

    # What each is worth in annual lagna.
    assert float(birthtime.solar_return_amplification(modern)[
        "lagna_error_degrees"]) == pytest.approx(0.085, abs=0.02)
    assert float(birthtime.solar_return_amplification(ancient)[
        "lagna_error_degrees"]) == pytest.approx(2.26, abs=0.1)
    assert "0.014 arcminutes over 1900-2100" in (
        birthtime.THE_TIMES_360_IS_EXACT_AND_THE_BASELINE_DECIDES_THE_DAMAGE)


def test_the_books_own_approximate_method_misses_by_a_third_of_a_degree():
    """FINDING: section 27.2's method, measured in chapter 27, in annual
    lagna.
    """
    from hora.tajaka.approximate import THE_APPROXIMATION_ERROR_IS_NOT_CONSTANT

    assert "72 seconds" in THE_APPROXIMATION_ERROR_IS_NOT_CONSTANT
    assert "118 seconds" in THE_APPROXIMATION_ERROR_IS_NOT_CONSTANT
    assert "approximate method taught in this boo" in (
        birthtime.THE_ACCURACY_ASSUMPTION)

    for seconds, arcminutes in ((72, 18.0), (118, 29.5)):
        assert seconds / 60 * 15 == pytest.approx(arcminutes, abs=0.1)
    # Against the 5 arcminutes this section's own example turns on.
    assert 18.0 / 5 >= 3
    assert "several times" in (
        birthtime.THE_BOOKS_OWN_APPROXIMATE_METHOD_MISSES_BY_A_THIRD_OF_A_DEGREE)


def test_the_annual_half_of_the_example_reproduces_exactly():
    """Cancer just below 15 degrees and Leo just above, the 5th and 6th
    from Pisces as printed.
    """
    stated = birthtime.TAJAKA_BORDER_EXAMPLE_STATED
    cancer = RASI_ABBR.index("Cn") * 30
    border = float(stated["annual_border"])
    below = vargas.d10_dasamsa(cancer + border - 0.001)
    above = vargas.d10_dasamsa(cancer + float(
        stated["annual_lagna_degree_in_rasi"]))
    assert RASI_ABBR[int(below.sign)] == stated["below_the_border"] == "Cn"
    assert RASI_ABBR[int(above.sign)] == stated["above_the_border"] == "Le"

    # Counted from Pisces, Cancer is the 5th and Leo the 6th.
    pisces = RASI_ABBR.index("Pi")
    assert (int(below.sign) - pisces) % 12 + 1 == 5
    assert (int(above.sign) - pisces) % 12 + 1 == 6
    assert "the 5th from Pi" in birthtime.THE_TAJAKA_BORDER_EXAMPLE
    assert "the 6th from Pi" in birthtime.THE_TAJAKA_BORDER_EXAMPLE


def test_the_annual_margin_is_twenty_seconds_not_thirty():
    """FINDING: half a minute is a true sufficient condition, not the margin."""
    stated = birthtime.TAJAKA_BORDER_EXAMPLE_STATED
    above_border = (float(stated["annual_lagna_degree_in_rasi"])
                    - float(stated["annual_border"])) * 60
    assert above_border == pytest.approx(5.0)
    assert birthtime.seconds_to_move(above_border) == pytest.approx(20.0)
    assert float(stated["correct_margin_seconds"]) == 20.0
    assert float(stated["printed_margin_seconds"]) == 30.0
    # Half a minute is more than enough, so the sentence is true as printed.
    assert float(stated["printed_margin_seconds"]) > float(
        stated["correct_margin_seconds"])
    assert "sufficient" in birthtime.THE_ANNUAL_MARGIN_IS_TWENTY_SECONDS_NOT_THIRTY


def test_d88_the_middle_of_the_eighth_dasamsa_is_22_sc_30():
    """BOOK DEFECT D-88. Six minutes either way is right for 22 Sc 30; from
    the printed 23 Sc 30 it is ten minutes down and two up, and the two is
    inside the example's own bound.
    """
    stated = birthtime.TAJAKA_BORDER_EXAMPLE_STATED
    scorpio = RASI_ABBR.index("Sc") * 30
    low, high = (float(x) for x in stated["natal_dasamsa_span"])
    assert (low, high) == (21.0, 24.0)
    assert (low + high) / 2 == float(stated["the_middle_of_the_eighth"]) == 22.5

    # The 8th dasamsa really is 21 to 24, and the printed lagna is inside it.
    printed = float(stated["natal_lagna_degree_in_rasi"])
    assert printed == 23.5
    windows = birthtime.lagna_windows(scorpio + low, scorpio + high,
                                      vargas.d10_dasamsa)
    assert len(windows) == 1
    assert int(printed // 3) + 1 == int(stated["natal_dasamsa"]) == 8

    # Margins from the true middle, and from the printed value.
    assert birthtime.seconds_to_move((22.5 - low) * 60) / 60 == pytest.approx(
        float(stated["printed_margin_minutes"]))
    assert birthtime.seconds_to_move((high - 22.5) * 60) / 60 == pytest.approx(
        float(stated["printed_margin_minutes"]))
    down, up = (float(x) for x in stated["correct_margin_minutes"])
    assert birthtime.seconds_to_move((printed - low) * 60) / 60 == (
        pytest.approx(down))
    assert birthtime.seconds_to_move((high - printed) * 60) / 60 == (
        pytest.approx(up))
    assert (down, up) == (10.0, 2.0)

    # And two minutes is inside the error the example itself allows.
    assert up < float(stated["error_bound_minutes"])
    assert "error of upto 3 minutes" in birthtime.THE_TAJAKA_BORDER_EXAMPLE

    from pathlib import Path

    text = Path("docs/book-deviations.md").read_text(encoding="utf-8")
    assert '## D-88 · §32.2.3\'s "middle of the 8th dasamsa" is 22 Sc 30' in text


def test_solar_return_amplification_rejects_a_dead_rate():
    with pytest.raises(birthtime.BirthtimeError, match="must both be positive"):
        birthtime.solar_return_amplification(1.0, sun_degrees_per_day=0.0)


# --------------------------------------------------------------------------
# §32.3 A Practical Approach
# --------------------------------------------------------------------------


def test_section_32_3_is_transcribed():
    assert birthtime.SECTION_32_3_TITLE == "A Practical Approach"
    assert "first determine the correct D-9 lagna or D-10 lagna" in (
        birthtime.NARROW_DOWN_WITH_EACH_CRITERION)
    assert "narrow down further and further with each criterion" in (
        birthtime.NARROW_DOWN_WITH_EACH_CRITERION)
    assert "we can revisit D-9 and change the lagna" in (
        birthtime.SOMETIMES_WE_MUST_COME_BACK_TO_D9)
    assert "willing to come back to the first step" in birthtime.BROAD_THEN_FINE


def test_the_two_steps_are_the_two_stages_in_minutes():
    """FINDING: 10 minutes is a D-10 window and 4 is a D-20 or D-24 one."""
    first, second = birthtime.NARROWING_STEPS
    assert float(first["width_minutes"]) == 10.0
    assert float(second["width_minutes"]) == 4.0
    # The second window sits inside the first.
    assert first["from"] == "9:05" and first["to"] == "9:15"
    assert second["from"] == "9:07" and second["to"] == "9:11"

    def window(varga: int) -> float:
        return float(birthtime.varga_rasi_change_interval(120.0,
                                                          varga)["interval"])

    assert window(10) == 12.0
    assert window(20) == 6.0
    assert window(24) == 5.0
    assert abs(float(first["width_minutes"]) - window(10)) <= 2.0
    assert abs(float(second["width_minutes"]) - window(24)) <= 2.0
    assert "its own broad and fine stages" in (
        birthtime.THE_TWO_STEPS_ARE_THE_TWO_STAGES_IN_MINUTES)


def test_the_named_order_is_strictly_coarse_to_fine():
    """FINDING: D-9 13.3 min, D-10 12, D-20 6, then Kalachakra."""
    intervals = []
    for row in birthtime.THE_NAMED_INSTRUMENTS:
        if row["varga"] is None:
            continue
        intervals.append(float(birthtime.varga_rasi_change_interval(
            120.0, int(row["varga"]))["interval"]))
    assert intervals == [pytest.approx(13.333, abs=0.01), 12.0, 6.0]
    assert intervals == sorted(intervals, reverse=True)

    # Kalachakra is finer than any of them: a whole day of dasa date costs
    # 0.6 seconds of birthtime at paramayush 100.
    assert float(birthtime.kalachakra_date_error(100.0, 0.01)["days"]) == (
        pytest.approx(1.0))
    assert 0.01 * 60 == pytest.approx(0.6)

    stages = [row["stage"] for row in birthtime.THE_NAMED_INSTRUMENTS]
    assert stages == ["broad", "broad", "fine", "fine"]
    assert "in the order the section names them" in (
        birthtime.THE_NAMED_ORDER_IS_STRICTLY_COARSE_TO_FINE)


def test_the_backtracking_is_computable():
    """FINDING: D-9 in Li allows one D-24 lagna, D-9 in Sc allows two."""
    aries = RASI_ABBR.index("Ar") * 30
    centre = 23 + 20 / 60                       # the Li/Sc navamsa border
    got = birthtime.refine_windows(aries + centre - 0.75,
                                   aries + centre + 0.75,
                                   vargas.d9_navamsa,
                                   vargas.d24_chaturvimsamsa)
    assert [RASI_ABBR[int(row["sign"])] for row in got] == ["Li", "Sc"]

    libra, scorpio = got
    assert [RASI_ABBR[s] for s in libra["fine_signs"]] == ["Aq"]
    assert [RASI_ABBR[s] for s in scorpio["fine_signs"]] == ["Aq", "Pi"]

    # The example's own shape: one choice is "better" and the other is what
    # a D-24 answer of Pisces would force.
    assert "lagna in D-9 in Li or Sc" in birthtime.SOMETIMES_WE_MUST_COME_BACK_TO_D9
    assert "one D-24 candidate, Aquarius" in birthtime.THE_BACKTRACKING_IS_COMPUTABLE


def test_d9_and_d24_borders_coincide_only_at_ten_degree_marks():
    """FINDING: which is what decides whether backtracking is forced."""
    from fractions import Fraction

    nine = {Fraction(k * 10, 3) for k in range(10)}
    twentyfour = {Fraction(j * 5, 4) for j in range(25)}
    assert sorted(float(x) for x in nine & twentyfour) == [0.0, 10.0, 20.0,
                                                           30.0]

    aries = RASI_ABBR.index("Ar") * 30
    # At a coincident mark the two D-9 choices share nothing.
    at_twenty = birthtime.refine_windows(aries + 20.0 - 0.75,
                                         aries + 20.0 + 0.75,
                                         vargas.d9_navamsa,
                                         vargas.d24_chaturvimsamsa)
    first, second = (set(row["fine_signs"]) for row in at_twenty)
    assert not (first & second)

    # Away from one they share exactly one.
    off_mark = birthtime.refine_windows(aries + 23 + 20 / 60 - 0.75,
                                        aries + 23 + 20 / 60 + 0.75,
                                        vargas.d9_navamsa,
                                        vargas.d24_chaturvimsamsa)
    first, second = (set(row["fine_signs"]) for row in off_mark)
    assert len(first & second) == 1
    assert "only at 0, 10, 20 and 30 degrees" in (
        birthtime.D9_AND_D24_BORDERS_COINCIDE_ONLY_AT_TEN_DEGREE_MARKS)


def test_the_d9_criteria_are_section_18_5s_own_significations():
    """FINDING: the rectification criterion is the varga's signification."""
    from hora.dasha.rasi.narayana import VARGA_SEED_RATIONALE

    navamsa = next(row for row in VARGA_SEED_RATIONALE
                   if "D9" in row["vargas"])
    assert navamsa["shows"] == "dharma (duty)"
    assert "To get married" in str(navamsa["text"])
    assert "duty" in str(navamsa["text"])

    assert "If one's marriage has already taken place" in (
        birthtime.SOMETIMES_WE_MUST_COME_BACK_TO_D9)
    assert "one's general sense of duty" in (
        birthtime.SOMETIMES_WE_MUST_COME_BACK_TO_D9)
    assert "The criterion is the signification" in (
        birthtime.THE_D9_CRITERIA_ARE_SECTION_18_5S_OWN_SIGNIFICATIONS)


def test_refine_windows_carries_the_whole_range_through():
    aries = RASI_ABBR.index("Ar") * 30
    low, high = aries + 10.0, aries + 14.0
    got = birthtime.refine_windows(low, high, vargas.d9_navamsa,
                                   vargas.d24_chaturvimsamsa)
    # The coarse windows tile the range without gaps.
    assert float(got[0]["from"]) == pytest.approx(low)
    assert float(got[-1]["to"]) == pytest.approx(high)
    from itertools import pairwise

    for before, after in pairwise(got):
        assert float(before["to"]) == pytest.approx(float(after["from"]))
    # And each coarse window's fine windows tile it in turn.
    for row in got:
        inner = row["fine"]
        assert float(inner[0]["from"]) == pytest.approx(float(row["from"]))
        assert float(inner[-1]["to"]) == pytest.approx(float(row["to"]))
