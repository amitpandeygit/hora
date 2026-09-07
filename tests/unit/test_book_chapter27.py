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


# --------------------------------------------------------------------------
# Example 118 — the rule run once, end to end, and Chart 66
# --------------------------------------------------------------------------

E118_BIRTH = (1967, 3, 8, 17, 40, 0.0)
E118_LAT, E118_LON = 26 + 18 / 60, 73 + 4 / 60


def _e118():
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    place = Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON)
    natal = compute_chart(from_local(*E118_BIRTH, utc_offset_hours=5.5),
                          place, Settings())
    return natal, place


def test_example_118s_natal_sun_reproduces():
    """"Sun occupies 23° 50' 25" in Aq in his birthchart." """
    from hora.charts import book

    natal, _place = _e118()
    printed = book.longitude("23 Aq 50") + 25 / 3600.0
    error = abs(natal.positions[0].longitude - printed) * 3600.0
    assert error < 5.0, error


def test_example_118s_varsha_pravesh_reproduces_to_within_ten_seconds():
    """"Sun enters this position at 4:41:21 am on 8th March 2000." """
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import EXAMPLE_118_NATIVITY, varsha_pravesh

    natal, place = _e118()
    got = varsha_pravesh(_sun_at(place), natal.positions[0].longitude,
                         natal.instant.jd_ut,
                         int(EXAMPLE_118_NATIVITY["year_entered"]))
    assert got["found"]
    local = from_jd(got["jd"], utc_offset_hours=5.5).local
    assert (local.year, local.month, local.day) == (2000, 3, 8)
    printed = local.replace(hour=4, minute=41, second=21, microsecond=0)
    assert abs((local - printed).total_seconds()) < 10.0


def test_the_example_settles_oi_151_the_zodiac_is_sidereal():
    """The one thing §27.1 does not say, decided by arithmetic.

    A tropical target lands on the previous day, eleven hours out. There is
    no reading of "the exact position" but the sidereal one.
    """
    from hora.charts.chart import compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import (
        THE_EXAMPLE_SETTLES_THE_ZODIAC_AS_SIDEREAL,
        varsha_pravesh,
    )

    natal, place = _e118()

    def tropical_at(jd: float) -> float:
        chart = compute_chart(from_jd(jd, utc_offset_hours=5.5), place,
                              Settings())
        return (chart.positions[0].longitude + chart.ayanamsa) % 360.0

    natal_tropical = (natal.positions[0].longitude + natal.ayanamsa) % 360.0
    other = varsha_pravesh(tropical_at, natal_tropical, natal.instant.jd_ut,
                           34)
    assert other["found"]
    local = from_jd(other["jd"], utc_offset_hours=5.5).local
    assert (local.month, local.day) == (3, 7)          # the day before
    assert "the only one that reproduces the example" in (
        THE_EXAMPLE_SETTLES_THE_ZODIAC_AS_SIDEREAL)


def test_the_book_counts_years_the_way_varsha_pravesh_does():
    """"The native finishes 33 years and enters his 34th year at that time."
    """
    from hora.tajaka.annual import (
        EXAMPLE_118_NATIVITY,
        THE_NTH_YEAR_BEGINS_AT_THE_N_MINUS_ONE_TH_RETURN,
        varsha_pravesh,
    )

    assert EXAMPLE_118_NATIVITY["years_finished"] == 33
    assert EXAMPLE_118_NATIVITY["year_entered"] == 34

    natal, place = _e118()
    got = varsha_pravesh(_sun_at(place), natal.positions[0].longitude,
                         natal.instant.jd_ut, 34)
    assert got["returns_completed"] == 33
    assert "the first year begins at birth" in (
        THE_NTH_YEAR_BEGINS_AT_THE_N_MINUS_ONE_TH_RETURN)


def test_chart_66_reproduces_from_the_varsha_pravesh_moment():
    """Every printed longitude, against the book's own instant.

    Rahu and Ketu need the mean node — OI-68's eighteenth chart. HL and GL
    are left to their own test; they turn on the sunrise, which is OI-103.
    """
    from hora.charts import book
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local, norm180

    place = Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON)
    instant = from_local(2000, 3, 8, 4, 41, 21.0, utc_offset_hours=5.5)
    printed = book.longitudes(66)
    graha = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
             "Sat": 6, "Rahu": 7, "Ketu": 8}

    true_node = compute_chart(instant, place, Settings())
    assert abs(norm180(true_node.lagna_longitude - printed["Asc"])) * 60 < 1.0
    for name in ("Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat"):
        error = abs(norm180(
            true_node.positions[graha[name]].longitude - printed[name])) * 60
        assert error < 1.0, (name, error)
    assert true_node.positions[3].is_retrograde          # "Merc (R)"

    # The nodes, and only the nodes, need the mean node.
    for node in ("Rahu", "Ketu"):
        astray = abs(norm180(
            true_node.positions[graha[node]].longitude - printed[node])) * 60
        assert astray > 60.0, (node, astray)
    mean = compute_chart(instant, place, Settings(node_type=NodeType.MEAN))
    for node in ("Rahu", "Ketu"):
        error = abs(norm180(
            mean.positions[graha[node]].longitude - printed[node])) * 60
        assert error < 1.0, (node, error)


def test_chart_66s_chara_karakas_reproduce():
    from hora.charts.chart import Place, compute_chart
    from hora.charts.karaka import chara_karakas
    from hora.core.const import GRAHA_NAMES
    from hora.core.constants.book_charts import BOOK_CHARTS
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    place = Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON)
    chart = compute_chart(
        from_local(2000, 3, 8, 4, 41, 21.0, utc_offset_hours=5.5), place,
        Settings(node_type=NodeType.MEAN))
    abbreviation = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars",
                    "Mercury": "Merc", "Jupiter": "Jup", "Venus": "Ven",
                    "Saturn": "Sat", "Rahu": "Rahu"}
    ours = {abbreviation[str(GRAHA_NAMES[k.graha])]: k.symbol
            for k in chara_karakas({g: p.longitude
                                    for g, p in chart.positions.items()
                                    if g != 8})}
    printed = dict(BOOK_CHARTS[66]["chara_karakas"])  # type: ignore[arg-type]
    assert len(printed) == 8
    assert ours == printed


def test_hl_and_gl_are_closest_under_a_disc_centre_sunrise():
    """OI-103, measured on a chart the book prints.

    Both special lagnas are driven by sunrise. Under our default upper-limb
    sunrise they are 46' and 115' from the printed values; under disc-centre
    they are 10' and 25'. Neither is exact, so nothing is changed here.
    """
    from fastapi.testclient import TestClient

    from hora.api.main import app
    from hora.charts import book
    from hora.core.timeutil import norm180

    printed = book.longitudes(66)
    body = {"year": 2000, "month": 3, "day": 8, "hour": 4, "minute": 41,
            "second": 21, "tz_name": "Asia/Kolkata",
            "place": {"latitude": E118_LAT, "longitude": E118_LON,
                      "name": "birthplace"}}
    client = TestClient(app)
    errors = {}
    for mode in ("disc_upper_limb", "disc_center"):
        got = client.post("/v1/chart/special-lagnas",
                          json={**body, "settings": {"sunrise_mode": mode}})
        assert got.status_code == 200
        found = {e["abbreviation"]: e["longitude"]
                 for e in got.json()["special_lagnas"]}
        errors[mode] = {name: abs(norm180(found[name] - printed[name])) * 60
                        for name in ("HL", "GL")}
    for name in ("HL", "GL"):
        assert errors["disc_center"][name] < errors["disc_upper_limb"][name]
        assert errors["disc_center"][name] > 5.0        # still not exact


def test_chart_66_is_a_pre_dawn_instant_and_panchanga_still_rejects_it():
    """OI-149, now with a book chart behind it rather than only Chart 56."""
    from fastapi.testclient import TestClient

    from hora.api.main import app
    from hora.tajaka.annual import CHART_66_IS_A_SECOND_TEST_CASE_FOR_OI_149

    client = TestClient(app)
    got = client.post("/v1/panchanga", json={
        "year": 2000, "month": 3, "day": 8, "hour": 4, "minute": 41,
        "second": 21, "tz_name": "Asia/Kolkata",
        "place": {"latitude": E118_LAT, "longitude": E118_LON, "name": "b"}})
    assert got.status_code != 200
    assert "hora index" in str(got.json())
    assert "before sunrise" in CHART_66_IS_A_SECOND_TEST_CASE_FOR_OI_149


def test_the_two_footnotes_name_the_aliases_and_repeat_the_place_rule():
    from hora.tajaka.annual import (
        ANNUAL_CHART_ALIASES,
        BIRTHPLACE_RULE,
        FOOTNOTE_75,
        FOOTNOTE_75_NAMES_THE_WESTERN_AND_THE_INDIAN_ALIASES,
        FOOTNOTE_76,
        FOOTNOTE_76_RESTATES_THE_PLACE_RULE_AT_ITS_EXTREME,
    )

    assert "solar return" in FOOTNOTE_75
    assert "varshaphal" in FOOTNOTE_75
    assert "results for one year" in FOOTNOTE_75
    assert "other side of the globe" in FOOTNOTE_76
    assert "birthplace co-ordinates" in FOOTNOTE_76
    assert "irrespective of the place of living" in BIRTHPLACE_RULE

    assert len(ANNUAL_CHART_ALIASES) == 4
    for entry in ANNUAL_CHART_ALIASES:
        source = FOOTNOTE_75 if "footnote 75" in entry["from"] else None
        if source is not None:
            assert entry["name"].split()[0] in source
    assert "no maharshi behind it" in (
        FOOTNOTE_75_NAMES_THE_WESTERN_AND_THE_INDIAN_ALIASES)
    assert "other side of the globe" in (
        FOOTNOTE_76_RESTATES_THE_PLACE_RULE_AT_ITS_EXTREME)


def test_example_118_is_transcribed_with_what_it_defers():
    from hora.tajaka.annual import (
        EXAMPLE_118,
        EXAMPLE_118_CHART,
        EXAMPLE_118_METHOD,
        EXAMPLE_118_USE,
    )

    assert "8th March 1967, 5:40 pm (IST), 73 E 04, 26 N 18" in EXAMPLE_118
    assert "4:41:21 am on 8th March 2000" in EXAMPLE_118_METHOD
    assert "Chart 66" in EXAMPLE_118_CHART
    # The reading is deferred, which is why nothing reads an annual chart yet.
    assert "annual dasas" in EXAMPLE_118_USE
    assert "We will learn them in later chapters" in EXAMPLE_118_USE
