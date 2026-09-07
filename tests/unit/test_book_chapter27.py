"""Chapter 27 — Tajaka chart basics.

§27.1 is the first page of Part 4 that computes anything: a moment and a
place. The moment is solved for rather than stepped to, and the place is the
birthplace whatever the native's address. Both are checked against the
ephemeris here; the section's worked example checks them against the book.
"""
from __future__ import annotations

import pytest

TZ = 5.5
#: The nativity used throughout, until the section's own example arrives.
BIRTH = (1978, 5, 7, 12, 55, 0.0)
LAT, LON = 19 + 5 / 60, 72 + 55 / 60


def _natal():
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    place = Place(name="Ghatkopar", latitude=LAT, longitude=LON)
    chart = compute_chart(from_local(*BIRTH, utc_offset_hours=TZ), place,
                          Settings())
    return chart, place


def _sun_at(place):
    from hora.charts.chart import compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_jd

    def at(jd: float) -> float:
        return compute_chart(from_jd(jd, utc_offset_hours=TZ), place,
                             Settings()).positions[0].longitude

    return at


def test_27_1_states_the_rule_and_the_place_separately():
    from hora.tajaka.annual import (
        BIRTHPLACE_RULE,
        SUN_MOVES_30_DEGREES_A_MONTH,
        VARSHA_PRAVESH_RULE,
    )

    assert "30° per month" in SUN_MOVES_30_DEGREES_A_MONTH
    assert "one year to complete one cycle" in SUN_MOVES_30_DEGREES_A_MONTH
    assert "exact moment" in VARSHA_PRAVESH_RULE
    assert "exact position" in VARSHA_PRAVESH_RULE
    for name in ("Tajaka varsha chakra", "Tajaka annual chart"):
        assert name in VARSHA_PRAVESH_RULE
    assert "irrespective of the place of living" in BIRTHPLACE_RULE


def test_varsha_pravesh_is_two_words_and_the_book_glosses_both():
    from hora.tajaka.annual import VARSHA_PRAVESH_MEANS, VARSHA_PRAVESH_NAME

    assert "by some people" in VARSHA_PRAVESH_NAME
    assert VARSHA_PRAVESH_MEANS == {"varsha": "a year", "pravesh": "entry"}
    for word, gloss in VARSHA_PRAVESH_MEANS.items():
        assert f"{word} means {gloss}" in VARSHA_PRAVESH_NAME.lower()


def test_the_first_year_begins_at_birth_itself():
    """Year 1 is the birth. Nothing is searched for, and nothing is invented
    for a native who has had no return yet.
    """
    from hora.tajaka.annual import varsha_pravesh

    chart, place = _natal()
    got = varsha_pravesh(_sun_at(place), chart.positions[0].longitude,
                         chart.instant.jd_ut, 1)
    assert got["is_birth_itself"] is True
    assert got["returns_completed"] == 0
    assert got["jd"] == chart.instant.jd_ut
    assert got["searched"] is None


def test_the_sun_is_at_his_natal_longitude_at_every_varsha_pravesh():
    """The whole of the rule, checked against the ephemeris: at the returned
    instant the Sun must be at the natal longitude, not near it.
    """
    from hora.core.timeutil import norm180
    from hora.tajaka.annual import varsha_pravesh

    chart, place = _natal()
    natal_sun = chart.positions[0].longitude
    sun_at = _sun_at(place)
    for year in (2, 10, 25, 49, 50, 51):
        got = varsha_pravesh(sun_at, natal_sun, chart.instant.jd_ut, year)
        assert got["found"], year
        error = abs(norm180(sun_at(got["jd"]) - natal_sun)) * 3600.0
        assert error < 1.0, (year, error)


def test_the_return_is_not_the_birthday_and_not_a_365_day_step():
    """Both shortcuts the section's "exact moment" forecloses, measured.

    Casting on the birthday at the birth time is the tempting mistake, and it
    is wrong by hours, not minutes: the return advances about six hours of
    clock time each common year and a leap day pulls it back a day. A fixed
    365-day step is a quarter of a day short every year.
    """
    import datetime as dt

    from hora.charts.chart import compute_chart
    from hora.core.const import RASI_ABBR
    from hora.core.settings import Settings
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh

    chart, place = _natal()
    natal_sun = chart.positions[0].longitude
    sun_at = _sun_at(place)

    clock, dates = [], set()
    for year in (49, 50, 51, 52):
        got = varsha_pravesh(sun_at, natal_sun, chart.instant.jd_ut, year)
        local = from_jd(got["jd"], utc_offset_hours=TZ).local
        clock.append(local.hour + local.minute / 60.0)
        dates.add((local.month, local.day))
    # The calendar date is not fixed either, once a leap day intervenes.
    assert len(dates) > 1
    assert max(clock) - min(clock) > 5.0

    # And the ascendant at the true return is nothing like the natal one.
    fiftieth = varsha_pravesh(sun_at, natal_sun, chart.instant.jd_ut, 50)
    lagna = compute_chart(from_jd(fiftieth["jd"], utc_offset_hours=TZ),
                          place, Settings()).lagna_longitude
    assert RASI_ABBR[int(lagna // 30)] != RASI_ABBR[chart.lagna_rasi]

    stepped = chart.instant.jd_ut + 49 * 365.0
    drift = dt.timedelta(days=fiftieth["jd"] - stepped)
    assert drift > dt.timedelta(days=12)


def test_the_chart_is_cast_for_the_birthplace_and_the_difference_is_large():
    """§27.1's place rule, and what ignoring it would cost.

    The same instant read from a different horizon gives a different
    ascendant; the rule exists because that is the tempting mistake.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import RASI_ABBR
    from hora.core.settings import Settings
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import (
        THE_PLACE_IS_THE_BIRTHPLACE_AND_NOT_THE_RESIDENCE,
        varsha_pravesh,
    )

    chart, place = _natal()
    got = varsha_pravesh(_sun_at(place), chart.positions[0].longitude,
                         chart.instant.jd_ut, 50)
    instant = from_jd(got["jd"], utc_offset_hours=TZ)

    at_birthplace = compute_chart(instant, place, Settings()).lagna_longitude
    elsewhere = compute_chart(
        instant, Place(name="New York", latitude=40.71, longitude=-74.01),
        Settings()).lagna_longitude
    assert RASI_ABBR[int(at_birthplace // 30)] != RASI_ABBR[int(elsewhere // 30)]
    assert "the horizon is the natal one" in (
        THE_PLACE_IS_THE_BIRTHPLACE_AND_NOT_THE_RESIDENCE)


def test_the_return_interval_is_the_sidereal_year_not_365_days():
    """Which is the open question of the section, measured rather than
    asserted: consecutive returns of a sidereal longitude are 365.2564 days
    apart, and Part 4's opening called the year 365 days.
    """
    from hora.core.const import DASAS_WITHIN_THE_YEAR
    from hora.core.constants.timespan import SIDEREAL_YEAR_DAYS
    from hora.tajaka.annual import varsha_pravesh

    chart, place = _natal()
    natal_sun = chart.positions[0].longitude
    sun_at = _sun_at(place)
    first = varsha_pravesh(sun_at, natal_sun, chart.instant.jd_ut, 40)["jd"]
    last = varsha_pravesh(sun_at, natal_sun, chart.instant.jd_ut, 50)["jd"]
    measured = (last - first) / 10.0
    assert measured == pytest.approx(SIDEREAL_YEAR_DAYS, abs=0.01)
    assert measured > 365.0
    assert "365-day period" in DASAS_WITHIN_THE_YEAR


def test_a_window_with_no_crossing_says_so_rather_than_guessing():
    from hora.core import validate
    from hora.tajaka.annual import TajakaError, varsha_pravesh

    assert issubclass(TajakaError, validate.InputError)

    chart, place = _natal()
    sun_at = _sun_at(place)
    # A target the Sun never reaches at that offset from birth.
    wrong = (chart.positions[0].longitude + 180.0) % 360.0
    got = varsha_pravesh(sun_at, wrong, chart.instant.jd_ut, 5)
    assert got["found"] is False
    assert got["jd"] is None
    assert "no crossing" in got["reason"]

    for bad in (0, 201):
        with pytest.raises(validate.InputError):
            varsha_pravesh(sun_at, chart.positions[0].longitude,
                           chart.instant.jd_ut, bad)


def test_footnote_75_is_recorded_as_not_supplied():
    from hora.tajaka.annual import FOOTNOTE_75_NOT_SUPPLIED

    assert "not on the page supplied" in FOOTNOTE_75_NOT_SUPPLIED
