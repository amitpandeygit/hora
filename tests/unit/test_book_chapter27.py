"""Chapter 27 — Tajaka chart basics.

§27.1 is the first page of Part 4 that computes anything: a moment and a
place. The moment is solved for rather than stepped to, and the place is the
birthplace whatever the native's address. Both are checked against the
ephemeris here; the section's worked example checks them against the book.
"""
from __future__ import annotations

from itertools import pairwise

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


#: §27.2 works entirely in the birthplace's own clock and never converts, so
#: the datetimes here are deliberately naive. One helper carries the waiver.
def _local(year, month, day, hour, minute, second=0):
    import datetime as dt

    return dt.datetime(year, month, day, hour, minute, second)  # noqa: DTZ001


# --------------------------------------------------------------------------
# §27.2 — the approximate method, Table 71, and the note on ayanamsa
# --------------------------------------------------------------------------


def test_table_71_is_transcribed_with_its_nineteen_ages():
    from hora.tajaka.approximate import TABLE_71

    assert sorted(TABLE_71) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                20, 30, 40, 50, 60, 70, 80, 90, 100]
    for age, (days, hours, minutes, seconds) in TABLE_71.items():
        assert 0 <= days <= 6, age
        assert 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59
    # The days column is a weekday offset, which is why age 6 shows zero.
    assert TABLE_71[6][0] == 0


def test_the_stated_year_and_the_table_disagree_from_age_two_onwards():
    """BOOK DEFECT, D-78. The section says the table is built on a year of
    365d 6h 9m 12s. Every row but the first implies 365d 6h 9m 9.7s.
    """
    from hora.tajaka.approximate import (
        STATED_SIDEREAL_YEAR_DAYS,
        TABLE_71,
        THE_STATED_YEAR_AND_THE_TABLE_DISAGREE,
    )

    def implied(age: int) -> float:
        _days, hours, minutes, seconds = TABLE_71[age]
        fraction = (hours * 3600 + minutes * 60 + seconds) / 86400.0
        whole = round(age * 365.2563625 - fraction)
        return (whole + fraction) / age

    assert implied(1) == pytest.approx(STATED_SIDEREAL_YEAR_DAYS, abs=1e-9)
    others = [implied(age) for age in TABLE_71 if age != 1]
    # The larger rows pin the year to a fifth of a second; the small ones
    # carry the table's own rounding to whole seconds.
    large = [implied(age) for age in TABLE_71 if age >= 30]
    assert (max(large) - min(large)) * 86400 < 0.15
    # ...and none of them agrees with the sentence above the table.
    for value in others:
        assert value < STATED_SIDEREAL_YEAR_DAYS
    gap = (STATED_SIDEREAL_YEAR_DAYS - sum(others) / len(others)) * 86400
    assert gap == pytest.approx(2.27, abs=0.1)
    assert gap * 100 == pytest.approx(227, abs=10)      # 3m 47s by age 100
    assert "Only the age-1 row follows the stated figure" in (
        THE_STATED_YEAR_AND_THE_TABLE_DISAGREE)


def test_the_tables_own_year_is_the_real_sidereal_year():
    """What the eighteen rows are actually built from, to a quarter-second."""
    from hora.core.constants.timespan import SIDEREAL_YEAR_DAYS
    from hora.tajaka.approximate import TABLE_71

    _days, hours, minutes, seconds = TABLE_71[100]
    fraction = (hours * 3600 + minutes * 60 + seconds) / 86400.0
    implied = (round(100 * 365.2563625 - fraction) + fraction) / 100
    assert (implied - SIDEREAL_YEAR_DAYS) * 86400 == pytest.approx(0.18,
                                                                   abs=0.05)


def test_the_decomposition_is_the_sections_own():
    """"suppose someone finished 46 years. Then add the values given for 40
    years and 6 years."
    """
    from hora.core import validate
    from hora.tajaka.approximate import ApproximateError, decompose

    assert issubclass(ApproximateError, validate.InputError)

    assert decompose(46) == (40, 6)
    assert decompose(33) == (30, 3)
    assert decompose(100) == (100,)
    assert decompose(7) == (7,)
    assert decompose(0) == ()
    assert decompose(119) == (100, 10, 9)
    with pytest.raises(validate.InputError):
        decompose(200)


def test_the_offsets_add_the_way_the_table_says_they_do():
    """Example 118's own sum, digit for digit: 33 = 30 + 3 gives 6d 11h 2m 24s.
    """
    from hora.tajaka.approximate import TABLE_71, offset_for

    assert TABLE_71[30] == (2, 16, 34, 54)
    assert TABLE_71[3] == (3, 18, 27, 30)
    got = offset_for(33)
    assert got["parts"] == (30, 3)
    assert (got["days"], got["hours"], got["minutes"], got["seconds"]) == (
        6, 11, 2, 24)
    assert got["in_table"] is False


def test_the_approximate_method_reproduces_example_118_step_by_step():
    """Every printed intermediate, not only the answer."""
    import datetime as dt

    from hora.tajaka.approximate import approximate_varsha_pravesh

    # "Birthday (8th March 1967) is a Wednesday."
    assert dt.date(1967, 3, 8).strftime("%A") == "Wednesday"

    got = approximate_varsha_pravesh(_local(1967, 3, 8, 17, 40),
                                     "Wednesday", 33)
    assert got["years_completed"] == 33
    assert got["year_entered"] == 34
    assert got["birthday"] == dt.date(2000, 3, 8)
    # "Adding 6 days to it, we get a Tuesday."
    assert got["target_weekday"] == "Tuesday"
    # "It is 7th March 2000 ... we now take 5:40 pm on 7th March 2000."
    assert got["reference"] == _local(2000, 3, 7, 17, 40)
    assert got["days_from_birthday"] == -1
    # "We get 4:42:24 am on 8th March 2000."
    assert got["commencement"] == _local(2000, 3, 8, 4, 42, 24)


def test_the_approximation_is_wrong_by_one_minute_as_the_section_says():
    """"the time found here is wrong only by 1 minute." Against the exact
    method, not against the book's printed figure.
    """

    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.approximate import (
        ACCURACY_REMARK,
        approximate_varsha_pravesh,
    )

    natal, place = _e118()
    exact = varsha_pravesh(_sun_at(place), natal.positions[0].longitude,
                           natal.instant.jd_ut, 34)
    solved = from_jd(exact["jd"], utc_offset_hours=5.5).local
    approximate = approximate_varsha_pravesh(
        _local(1967, 3, 8, 17, 40), "Wednesday", 33)["commencement"]
    error = abs((approximate - solved).total_seconds())
    assert 60.0 <= error < 120.0, error
    assert "wrong only by 1 minute" in ACCURACY_REMARK


def test_the_method_needs_the_hindu_weekday_and_says_so():
    """Footnote 77, and why the weekday is an argument rather than derived."""

    from hora.tajaka.approximate import (
        FOOTNOTE_77,
        FOOTNOTE_77_IS_THE_SECOND_STATEMENT_OF_THE_SUNRISE_RULE,
        ApproximateError,
        approximate_varsha_pravesh,
    )
    from hora.transits.sarvatobhadra import FOOTNOTE_71

    assert "changes at sunrise and not at 12:00 midnight" in FOOTNOTE_77
    assert "a new day starts at sunrise" in FOOTNOTE_71
    assert "wrong weekday and the wrong reference date" in (
        FOOTNOTE_77_IS_THE_SECOND_STATEMENT_OF_THE_SUNRISE_RULE)

    with pytest.raises(ApproximateError):
        approximate_varsha_pravesh(_local(1967, 3, 8, 17, 40),
                                   "Budhavara", 33)

    # Taking the wrong weekday moves the whole answer by a day.
    right = approximate_varsha_pravesh(_local(1967, 3, 8, 17, 40),
                                       "Wednesday", 33)["commencement"]
    wrong = approximate_varsha_pravesh(_local(1967, 3, 8, 17, 40),
                                       "Tuesday", 33)["commencement"]
    assert abs((right - wrong).days) >= 1


def test_our_ayanamsa_is_nonlinear_as_the_note_requires():
    """"As long as one takes the correct nonlinear nature of ayanamsa change
    into account, there will not be any considerable discrepancy."

    Measured on our own ephemeris: the rate is not constant.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local
    from hora.tajaka.approximate import (
        AYANAMSA_NOTE,
        THE_NOTE_IS_A_CONSTRAINT_ON_THE_EPHEMERIS,
    )

    place = Place(name="b", latitude=26 + 18 / 60, longitude=73 + 4 / 60)
    values = {year: compute_chart(
        from_local(year, 3, 8, 12, 0, 0.0, utc_offset_hours=5.5), place,
        Settings()).ayanamsa for year in (1900, 1950, 2000, 2050, 2100)}
    rates = [(values[b] - values[a]) * 3600 / (b - a)
             for a, b in ((1900, 1950), (1950, 2000), (2000, 2050),
                          (2050, 2100))]
    assert all(50.2 < rate < 50.4 for rate in rates)
    assert rates == sorted(rates)                 # rising, so not linear
    assert max(rates) - min(rates) > 0.02
    assert "nonlinear nature of ayanamsa" in AYANAMSA_NOTE
    assert "nonlinear nature of ayanamsa change" in (
        THE_NOTE_IS_A_CONSTRAINT_ON_THE_EPHEMERIS)


def test_the_lagna_really_does_move_360_times_faster_than_the_sun():
    """The note's amplification factor, measured over a day and within it.

    The 360 is a daily average. Instantaneously the ratio swings widely with
    the rising sign, which makes the amplification worse in places, never
    better.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_jd, from_local
    from hora.tajaka.approximate import LAGNA_IS_360_TIMES_FASTER_THAN_SUN

    place = Place(name="b", latitude=26 + 18 / 60, longitude=73 + 4 / 60)
    start = from_local(2000, 3, 8, 4, 41, 21.0, utc_offset_hours=5.5).jd_ut

    def chart(jd: float):
        return compute_chart(from_jd(jd, utc_offset_hours=5.5), place,
                             Settings())

    daily = 360.0 / ((chart(start + 1.0).positions[0].longitude
                      - chart(start).positions[0].longitude) % 360)
    assert daily == pytest.approx(LAGNA_IS_360_TIMES_FASTER_THAN_SUN, abs=1.0)

    ratios = []
    for hour in range(0, 24, 2):
        before = chart(start + hour / 24)
        after = chart(start + hour / 24 + 1 / 1440)
        ratios.append(((after.lagna_longitude - before.lagna_longitude) % 360)
                      / ((after.positions[0].longitude
                          - before.positions[0].longitude) % 360))
    assert min(ratios) < LAGNA_IS_360_TIMES_FASTER_THAN_SUN < max(ratios)


def test_27_2_is_transcribed_with_its_five_steps():
    from hora.tajaka.approximate import PROCEDURE, SECTION_INTRO

    assert "laborious calculation to do manually" in SECTION_INTRO
    assert "365 days 6 hours 9 minutes and 12 seconds" in SECTION_INTRO
    assert len(PROCEDURE) == 5
    assert PROCEDURE[0].startswith("Find the birthday as per western calendar")
    assert "40 years and 6 years" in PROCEDURE[1]
    assert "nearest date to the birthday" in PROCEDURE[2]
    assert "commencement of new year" in PROCEDURE[3]
    assert "latitude of the birthplace" in PROCEDURE[4]


# --------------------------------------------------------------------------
# Exercise 47 — the same native's 27th year, both ways
# --------------------------------------------------------------------------


def test_exercise_47a_reproduces_the_approximate_method_step_by_step():
    """26 = 20 + 6, four days on to Sunday, and 9:38:12 am on 8 March 1993."""
    import datetime as dt

    from hora.tajaka.approximate import (
        EXERCISE_47_ANSWER,
        TABLE_71,
        approximate_varsha_pravesh,
        decompose,
        offset_for,
    )

    assert decompose(26) == (20, 6)
    assert TABLE_71[20] == (4, 3, 3, 12)
    assert TABLE_71[6] == (0, 12, 55, 0)
    got = offset_for(26)
    assert (got["days"], got["hours"], got["minutes"], got["seconds"]) == (
        4, 15, 58, 12)
    assert tuple(EXERCISE_47_ANSWER["offset"]) == (4, 15, 58, 12)

    answer = approximate_varsha_pravesh(_local(1967, 3, 8, 17, 40),
                                        "Wednesday", 26)
    assert answer["birthday"] == dt.date(1993, 3, 8)
    assert answer["target_weekday"] == "Sunday"
    assert answer["reference"] == _local(1993, 3, 7, 17, 40)
    assert answer["commencement"] == _local(1993, 3, 8, 9, 38, 12)
    assert answer["year_entered"] == 27


def test_exercise_47bs_sun_position_reproduces():
    """"At 9:38:12 am (IST) on 8th March 1993, Sun is at 23° 50' 29" in Aq."
    """
    from hora.charts import book
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    place = Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON)
    chart = compute_chart(
        from_local(1993, 3, 8, 9, 38, 12.0, utc_offset_hours=5.5), place,
        Settings())
    printed = book.longitude("23 Aq 50") + 29 / 3600.0
    assert abs(chart.positions[0].longitude - printed) * 3600 < 2.0


def test_exercise_47b_reproduces_the_exact_varsha_pravesh():
    """"The correct varshapravesh data is – 9:36:18 am (IST) on 8th March
    1993."  Our solve lands four seconds from it.
    """
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh

    natal, place = _e118()
    got = varsha_pravesh(_sun_at(place), natal.positions[0].longitude,
                         natal.instant.jd_ut, 27)
    assert got["found"]
    local = from_jd(got["jd"], utc_offset_hours=5.5).local
    assert (local.year, local.month, local.day) == (1993, 3, 8)
    printed = _local(1993, 3, 8, 9, 36, 18)
    assert abs((local - printed).total_seconds()) < 10.0


def test_the_exercises_exact_answer_is_a_hand_correction_not_a_solve():
    """Solving for the exercise's OWN printed natal position lands 39 seconds
    from the answer it prints. Our own solve lands 4 seconds from it.
    """
    from hora.charts import book
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.approximate import (
        THE_EXERCISES_EXACT_ANSWER_IS_A_HAND_CORRECTION,
    )

    natal, place = _e118()
    printed_answer = _local(1993, 3, 8, 9, 36, 18)
    sun_at = _sun_at(place)

    ours = from_jd(varsha_pravesh(sun_at, natal.positions[0].longitude,
                                  natal.instant.jd_ut, 27)["jd"],
                   utc_offset_hours=5.5).local
    theirs = from_jd(varsha_pravesh(sun_at,
                                    book.longitude("23 Aq 50") + 25 / 3600.0,
                                    natal.instant.jd_ut, 27)["jd"],
                     utc_offset_hours=5.5).local

    from_ours = abs((ours - printed_answer).total_seconds())
    from_theirs = abs((theirs - printed_answer).total_seconds())
    assert from_ours < 10.0
    assert from_theirs > 30.0
    assert from_theirs > from_ours
    assert "not a solution" in THE_EXERCISES_EXACT_ANSWER_IS_A_HAND_CORRECTION


def test_the_approximation_error_is_not_constant_across_one_nativity():
    """§27.2: "In some examples, the error resulting from the approximation
    can be higher."  Its own exercise, on its own native, is one.
    """
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.approximate import (
        ACCURACY_REMARK,
        THE_APPROXIMATION_ERROR_IS_NOT_CONSTANT,
        approximate_varsha_pravesh,
    )

    natal, place = _e118()
    sun_at = _sun_at(place)
    errors = {}
    for completed in (33, 26):
        approximate = approximate_varsha_pravesh(
            _local(1967, 3, 8, 17, 40), "Wednesday", completed)["commencement"]
        exact = from_jd(varsha_pravesh(sun_at, natal.positions[0].longitude,
                                       natal.instant.jd_ut,
                                       completed + 1)["jd"],
                        utc_offset_hours=5.5).local
        errors[completed] = (approximate - exact).total_seconds()

    assert 60 < errors[33] < 90                # the 34th year, about a minute
    assert 100 < errors[26] < 140              # the 27th, about two
    assert errors[26] > errors[33] * 1.5
    assert "can be higher" in ACCURACY_REMARK
    assert "72 seconds out in the 34th" in THE_APPROXIMATION_ERROR_IS_NOT_CONSTANT


def test_exercise_47_is_transcribed():
    from hora.tajaka.approximate import (
        EXERCISE_47,
        EXERCISE_47_APPROXIMATE,
        EXERCISE_47_EXACT,
    )

    assert "27th year of the native in Example 118" in EXERCISE_47
    assert len(EXERCISE_47_APPROXIMATE) == 4
    assert "8th March 1993" in EXERCISE_47_APPROXIMATE[0]
    assert "4 days 15 hr 58 min 12 sec" in EXERCISE_47_APPROXIMATE[1]
    assert "nearest Sunday" in EXERCISE_47_APPROXIMATE[2]
    assert "9:38:12 am" in EXERCISE_47_APPROXIMATE[3]
    assert "subtract about 2 minutes of time" in EXERCISE_47_EXACT
    assert "9:36:18 am (IST) on 8th March 1993" in EXERCISE_47_EXACT


# --------------------------------------------------------------------------
# §27.3 — casting monthly charts
# --------------------------------------------------------------------------

E118_NATAL_SUN_PRINTED = 300 + 23 + 50 / 60 + 25 / 3600
E118_VARSHA_34 = (2000, 3, 8, 4, 41, 21.0)


def _varsha_34_jd():
    from hora.core.timeutil import from_local

    return from_local(*E118_VARSHA_34, utc_offset_hours=5.5).jd_ut


def test_27_3_defines_a_year_and_a_month_as_solar_arcs():
    from hora.tajaka.monthly import (
        MAASA_PRAVESH_NAME,
        MONTHLY_CHART_NAMES,
        MONTHLY_CHART_RULE,
        THIRTY_DEGREES_EXACTLY,
        YEAR_AND_MONTH_ARE_SOLAR_ARCS,
    )

    assert "Sun moves by 360" in YEAR_AND_MONTH_ARE_SOLAR_ARCS
    assert "Sun moves by 30" in YEAR_AND_MONTH_ARE_SOLAR_ARCS
    assert "maasa pravesh" in MAASA_PRAVESH_NAME
    for name in MONTHLY_CHART_NAMES:
        assert name in MONTHLY_CHART_RULE
    assert "moves by exactly 30" in THIRTY_DEGREES_EXACTLY


def test_the_month_targets_are_the_natal_degree_in_each_rasi():
    """"when Sun enters 23° 50' 25" in different rasis"."""
    from hora.core import validate
    from hora.core.const import RASI_ABBR
    from hora.tajaka.monthly import MonthlyError, month_target

    assert issubclass(MonthlyError, validate.InputError)
    degrees = [month_target(E118_NATAL_SUN_PRINTED, m) % 30
               for m in range(1, 13)]
    # The same degree in every rasi, to the limit of float arithmetic.
    assert max(degrees) - min(degrees) < 1e-9
    rasis = [RASI_ABBR[int(month_target(E118_NATAL_SUN_PRINTED, m) // 30)]
             for m in range(1, 13)]
    assert rasis[:3] == ["Aq", "Pi", "Ar"]       # the section's own three
    assert len(set(rasis)) == 12
    for bad in (0, 13):
        with pytest.raises(validate.InputError):
            month_target(E118_NATAL_SUN_PRINTED, bad)


def test_the_first_month_is_the_varsha_pravesh_itself():
    from hora.tajaka.monthly import (
        THE_FIRST_MONTH_BEGINS_WITH_THE_YEAR,
        maasa_pravesh,
    )

    _natal, place = _e118()
    varsha = _varsha_34_jd()
    got = maasa_pravesh(_sun_at(place), E118_NATAL_SUN_PRINTED, varsha, 1)
    assert got["is_varsha_pravesh"] is True
    assert got["jd"] == varsha
    assert got["searched"] is None
    assert "The first maasa pravesh is the varsha pravesh" in (
        THE_FIRST_MONTH_BEGINS_WITH_THE_YEAR)


def test_27_3s_second_month_reproduces_to_within_seconds():
    """"Sun enters 23° 50' 25" in Pi on 7th April 2000 at 10:38:06 am."""
    from hora.core.timeutil import from_jd
    from hora.tajaka.monthly import maasa_pravesh

    _natal, place = _e118()
    got = maasa_pravesh(_sun_at(place), E118_NATAL_SUN_PRINTED,
                        _varsha_34_jd(), 2)
    assert got["found"]
    assert got["rasi"] == "Pisces"
    local = from_jd(got["jd"], utc_offset_hours=5.5).local
    printed = _local(2000, 4, 7, 10, 38, 6)
    assert abs((local - printed).total_seconds()) < 10.0


def test_the_twelve_months_run_forward_and_close_on_the_next_year():
    """Twelve maasa praveshas, in order, and the thirteenth boundary is the
    next varsha pravesh — the year is the twelve months and nothing else.
    """
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.monthly import maasa_praveshas

    natal, place = _e118()
    sun_at = _sun_at(place)
    months = maasa_praveshas(sun_at, E118_NATAL_SUN_PRINTED, _varsha_34_jd())
    assert len(months) == 12
    assert all(entry["found"] for entry in months)
    jds = [entry["jd"] for entry in months]
    assert jds == sorted(jds)

    next_year = varsha_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                               natal.instant.jd_ut, 35)
    assert next_year["found"]
    twelfth = next_year["jd"] - jds[-1]
    assert 29.0 < twelfth < 32.0                 # a twelfth month, not a gap
    assert 365.0 < next_year["jd"] - jds[0] < 365.5


def test_the_months_are_unequal_where_the_years_are_not():
    """§27.3's own reason for having no approximate method, measured.

    "the time Sun takes to move by 30° varies considerably from month to
    month" against "Sun takes approximately the same time for moving by 360°".
    """
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.monthly import (
        NO_APPROXIMATE_METHOD,
        THE_MONTHS_ARE_UNEQUAL_AND_THE_YEARS_ARE_NOT,
        maasa_praveshas,
    )

    natal, place = _e118()
    sun_at = _sun_at(place)
    months = maasa_praveshas(sun_at, E118_NATAL_SUN_PRINTED, _varsha_34_jd())
    following = varsha_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                               natal.instant.jd_ut, 35)["jd"]
    edges = [entry["jd"] for entry in months] + [following]
    lengths = [b - a for a, b in pairwise(edges)]
    assert len(lengths) == 12
    month_spread = max(lengths) - min(lengths)
    assert month_spread > 1.9                    # nearly two days

    years = []
    previous = None
    for year in range(30, 41):
        jd = varsha_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                            natal.instant.jd_ut, year)["jd"]
        if previous is not None:
            years.append(jd - previous)
        previous = jd
    year_spread = max(years) - min(years)
    assert year_spread < 0.02                    # under half an hour

    # Two orders of magnitude apart, which is the section's whole argument.
    assert month_spread / year_spread > 100
    assert "varies considerably from month to month" in NO_APPROXIMATE_METHOD
    assert "two orders" not in THE_MONTHS_ARE_UNEQUAL_AND_THE_YEARS_ARE_NOT
    assert "29.46 to 31.44" in THE_MONTHS_ARE_UNEQUAL_AND_THE_YEARS_ARE_NOT


def test_the_longest_month_holds_aphelion_and_the_shortest_perihelion():
    """The pattern is the Earth's orbit, not the zodiac, so it cannot be
    tabulated against a month number.

    Checked by the mechanism rather than by a date: the longest month is the
    one over which the Sun moves slowest, and the shortest the one over which
    he moves fastest.
    """
    import datetime as dt

    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.monthly import (
        THE_LONGEST_MONTH_HOLDS_APHELION,
        maasa_praveshas,
    )

    natal, place = _e118()
    sun_at = _sun_at(place)
    months = maasa_praveshas(sun_at, E118_NATAL_SUN_PRINTED, _varsha_34_jd())
    following = varsha_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                               natal.instant.jd_ut, 35)["jd"]
    edges = [entry["jd"] for entry in months] + [following]
    lengths = [b - a for a, b in pairwise(edges)]

    longest = lengths.index(max(lengths))
    shortest = lengths.index(min(lengths))
    # Every month covers exactly 30 degrees, so its length is inverse to the
    # Sun's mean speed across it. That is the whole mechanism.
    assert 30.0 / lengths[longest] < 30.0 / lengths[shortest]

    def spans(index: int, when: dt.date) -> bool:
        start = from_jd(edges[index], utc_offset_hours=5.5).local.date()
        end = from_jd(edges[index + 1], utc_offset_hours=5.5).local.date()
        return start <= when <= end

    assert spans(longest, dt.date(2000, 7, 4))       # aphelion
    assert spans(shortest, dt.date(2001, 1, 3))      # perihelion
    assert "aphelion and perihelion" in THE_LONGEST_MONTH_HOLDS_APHELION


def test_the_workaround_still_needs_one_exact_year():
    from hora.tajaka.monthly import (
        NO_APPROXIMATE_METHOD,
        THE_WORKAROUND_STILL_NEEDS_ONE_EXACT_YEAR,
    )

    assert "exactly cast 12 monthly charts for the first year" in (
        NO_APPROXIMATE_METHOD)
    assert "using the approximate method given for annual charts" in (
        NO_APPROXIMATE_METHOD)
    assert "once per month, once" in THE_WORKAROUND_STILL_NEEDS_ONE_EXACT_YEAR


def test_a_month_with_no_crossing_says_so_rather_than_guessing():
    from hora.tajaka.monthly import maasa_pravesh

    _natal, place = _e118()

    def never(_jd: float) -> float:
        return 0.0

    got = maasa_pravesh(never, E118_NATAL_SUN_PRINTED, _varsha_34_jd(), 6)
    assert got["found"] is False
    assert got["jd"] is None
    assert "no crossing" in got["reason"]
    assert _sun_at(place) is not None


# --------------------------------------------------------------------------
# §27.4 — casting sixty-hour charts
# --------------------------------------------------------------------------

E118_MAASA_2 = (2000, 4, 7, 10, 38, 6.0)


def _maasa_2_jd():
    from hora.core.timeutil import from_local

    return from_local(*E118_MAASA_2, utc_offset_hours=5.5).jd_ut


def test_27_4_defines_the_shashti_hora_as_an_arc_and_names_it_three_ways():
    from hora.tajaka.shashti_hora import (
        FOOTNOTE_78,
        SHASHTI_HORA_ARC_DEGREES,
        SHASHTI_HORA_IS_AN_ARC,
        SHASHTI_HORA_NAMES,
        SHASHTI_HORA_RULE,
        SHASHTI_HORAS_PER_MONTH,
        SHASHTI_HORAS_PER_YEAR,
    )

    assert SHASHTI_HORA_ARC_DEGREES == 2.5
    assert SHASHTI_HORAS_PER_MONTH == 12
    assert SHASHTI_HORAS_PER_YEAR == 144
    assert SHASHTI_HORAS_PER_MONTH * 12 == SHASHTI_HORAS_PER_YEAR
    assert "12 shashti-horas" in SHASHTI_HORA_RULE
    assert "2°30'" in SHASHTI_HORA_RULE
    assert "exactly 12 such charts in a one-month period" in (
        SHASHTI_HORA_IS_AN_ARC)
    assert SHASHTI_HORA_NAMES[:2] == ("Tajaka shashti-hora chakra",
                                      "Tajaka sixty-hour chart")
    assert SHASHTI_HORA_NAMES[2] in FOOTNOTE_78


def test_the_shashti_hora_targets_step_by_two_and_a_half_degrees():
    from hora.core import validate
    from hora.tajaka.monthly import month_target
    from hora.tajaka.shashti_hora import (
        ShashtiHoraError,
        shashti_hora_target,
    )

    assert issubclass(ShashtiHoraError, validate.InputError)
    # The first shashti-hora of a month is the month's own beginning.
    assert shashti_hora_target(E118_NATAL_SUN_PRINTED, 2, 1) == (
        month_target(E118_NATAL_SUN_PRINTED, 2))
    # "when Sun is advanced by 2°30', i.e. when Sun enters 26° 20' 25" in Pi"
    second = shashti_hora_target(E118_NATAL_SUN_PRINTED, 2, 2)
    assert second % 30 == pytest.approx(26 + 20 / 60 + 25 / 3600, abs=1e-9)
    assert int(second // 30) == 11                       # Pisces
    # Twelve of them span exactly one rasi's worth of motion.
    last = shashti_hora_target(E118_NATAL_SUN_PRINTED, 2, 12)
    assert (last - month_target(E118_NATAL_SUN_PRINTED, 2)) % 360 == (
        pytest.approx(27.5))
    for bad in (0, 13):
        with pytest.raises(validate.InputError):
            shashti_hora_target(E118_NATAL_SUN_PRINTED, 2, bad)


def test_27_4s_second_shashti_hora_reproduces_to_within_seconds():
    """"This happens at 11:40:51 pm (IST) on 9th April 2000." """
    from hora.core.timeutil import from_jd
    from hora.tajaka.shashti_hora import shashti_hora

    _natal, place = _e118()
    got = shashti_hora(_sun_at(place), E118_NATAL_SUN_PRINTED,
                       _maasa_2_jd(), 2, 2)
    assert got["found"]
    assert got["rasi"] == "Pisces"
    local = from_jd(got["jd"], utc_offset_hours=5.5).local
    printed = _local(2000, 4, 9, 23, 40, 51)
    assert abs((local - printed).total_seconds()) < 10.0


def test_the_first_shashti_hora_is_the_maasa_pravesh_itself():
    """"The first shashti-hora of the month also starts then." """
    from hora.tajaka.shashti_hora import shashti_hora

    _natal, place = _e118()
    got = shashti_hora(_sun_at(place), E118_NATAL_SUN_PRINTED,
                       _maasa_2_jd(), 2, 1)
    assert got["is_maasa_pravesh"] is True
    assert got["jd"] == _maasa_2_jd()
    assert got["searched"] is None


def test_twelve_shashti_horas_fill_the_month_and_none_of_them_is_sixty_hours():
    """The section's own example month, measured.

    "Each shashti-hora period consists of 60 hours" — its first is 61.05, and
    every one of the twelve is over sixty. The twelve add up to the month.
    """
    from hora.tajaka.monthly import maasa_pravesh
    from hora.tajaka.shashti_hora import (
        SIXTY_HOURS_IS_A_NAME_AND_THE_ARC_IS_THE_RULE,
        shashti_horas,
    )

    _natal, place = _e118()
    sun_at = _sun_at(place)
    horas = shashti_horas(sun_at, E118_NATAL_SUN_PRINTED, _maasa_2_jd(), 2)
    assert len(horas) == 12
    assert all(entry["found"] for entry in horas)

    third_month = maasa_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                                _varsha_34_jd(), 3)
    edges = [entry["jd"] for entry in horas] + [third_month["jd"]]
    assert edges == sorted(edges)
    hours = [(b - a) * 24 for a, b in pairwise(edges)]
    assert len(hours) == 12

    assert min(hours) > 60.0                     # not one is even sixty
    assert hours[0] == pytest.approx(61.05, abs=0.05)
    # And they sum to the month, which is what makes them a division of it.
    assert sum(hours) / 24 == pytest.approx(third_month["jd"]
                                            - _maasa_2_jd(), abs=1e-6)
    assert "disagree by about one and a half percent" in (
        SIXTY_HOURS_IS_A_NAME_AND_THE_ARC_IS_THE_RULE)


def test_across_a_whole_year_no_shashti_hora_is_sixty_hours():
    """144 of them, and the spread is four hours wide.

    12 x 2.5 days is 30 and a month is not; 144 x 2.5 is 360 and a year is
    365.26. The nominal figure is short by one and a half percent.
    """
    from hora.tajaka.annual import varsha_pravesh
    from hora.tajaka.shashti_hora import (
        SHASHTI_HORA_ARC_DEGREES,
        SHASHTI_HORAS_PER_YEAR,
        THE_ROUND_FIGURE_NEVER_GOVERNS,
    )

    natal, place = _e118()
    sun_at = _sun_at(place)
    start = _varsha_34_jd()

    edges, previous = [start], start
    for step in range(1, SHASHTI_HORAS_PER_YEAR + 1):
        from hora.panchanga.solver import scan_for_crossing

        target = (E118_NATAL_SUN_PRINTED
                  + SHASHTI_HORA_ARC_DEGREES * step) % 360.0
        found = scan_for_crossing(sun_at, target, previous + 1.5,
                                  previous + 4.0, step=0.1)
        assert found is not None, step
        edges.append(found)
        previous = found

    hours = [(b - a) * 24 for a, b in pairwise(edges)]
    assert len(hours) == SHASHTI_HORAS_PER_YEAR
    assert not any(abs(value - 60.0) < 1 / 60 for value in hours)
    assert min(hours) == pytest.approx(58.86, abs=0.1)
    assert max(hours) == pytest.approx(62.94, abs=0.1)
    assert sum(hours) / 24 == pytest.approx(365.26, abs=0.01)

    # The nominal year the "2.5 days" implies, against the real one.
    assert SHASHTI_HORAS_PER_YEAR * 2.5 == 360.0
    following = varsha_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                               natal.instant.jd_ut, 35)
    assert following["jd"] - start == pytest.approx(sum(hours) / 24,
                                                    abs=1e-4)
    assert "The arc rule is what every worked example uses" in (
        THE_ROUND_FIGURE_NEVER_GOVERNS)


def test_a_shashti_hora_with_no_crossing_says_so():
    from hora.tajaka.shashti_hora import shashti_hora

    def never(_jd: float) -> float:
        return 0.0

    got = shashti_hora(never, E118_NATAL_SUN_PRINTED, _maasa_2_jd(), 2, 7)
    assert got["found"] is False
    assert got["jd"] is None
    assert "no crossing" in got["reason"]


# --------------------------------------------------------------------------
# §27.5 — the chapter's conclusion
# --------------------------------------------------------------------------


def test_27_5_summarises_all_three_kinds_of_chart():
    from hora.core.const import CHAPTER_27_CONCLUSION

    assert "re-enters every year the same longitude" in CHAPTER_27_CONCLUSION
    assert "that exact moment" in CHAPTER_27_CONCLUSION
    for kind in ("annual", "monthly charts", "sixty-hour charts"):
        assert kind in CHAPTER_27_CONCLUSION


def test_around_is_the_right_word_for_the_date_and_too_kind_for_the_hour():
    """"the commencement of new year is *around* one's birthday" — measured
    over ninety-nine years of one nativity.
    """
    from collections import Counter

    from hora.core.const import THE_DATE_IS_STEADY_AND_THE_HOUR_IS_NOT
    from hora.core.timeutil import from_jd
    from hora.tajaka.annual import varsha_pravesh

    natal, place = _e118()
    sun_at = _sun_at(place)
    dates: Counter = Counter()
    hours = []
    for year in range(2, 101):
        got = varsha_pravesh(sun_at, E118_NATAL_SUN_PRINTED,
                             natal.instant.jd_ut, year)
        assert got["found"], year
        local = from_jd(got["jd"], utc_offset_hours=5.5).local
        dates[(local.month, local.day)] += 1
        hours.append(local.hour + local.minute / 60.0)

    # The date is nearly always the western birthday, and never far from it.
    assert set(dates) <= {(3, 7), (3, 8), (3, 9)}
    assert dates[(3, 8)] > 70
    # The hour is anything at all, which is why the exact moment matters.
    assert min(hours) < 1.0
    assert max(hours) > 23.0
    assert "takes every hour of the day" in THE_DATE_IS_STEADY_AND_THE_HOUR_IS_NOT


def test_the_lunar_birthday_techniques_are_a_named_exclusion():
    from hora.core.const import (
        LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE,
        THE_LUNAR_RETURN_IS_A_NAMED_EXCLUSION,
    )

    assert "beyond the scope of this book" in LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE
    assert "restrict ourselves to solar birthday" in (
        LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE)
    assert "tithi" in LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE
    assert "No tithi-based annual chart is built" in (
        THE_LUNAR_RETURN_IS_A_NAMED_EXCLUSION)

    # And nothing in the Tajaka package computes a lunar return.
    import pkgutil

    import hora.tajaka

    for module in pkgutil.iter_modules(hora.tajaka.__path__):
        assert "tithi" not in module.name
        assert "lunar" not in module.name


def test_the_three_chapter_conclusions_do_different_work():
    from hora.core.const import (
        CHAPTER_26_CONCLUSION,
        CHAPTER_27_CONCLUSION,
        LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE,
        THE_THREE_CONCLUSIONS_DO_DIFFERENT_WORK,
        THE_TWENTY_SEVEN_GROUP_CRITERION,
    )
    from hora.transits.gochara import THE_CONCLUSION_INTRODUCES_NOTHING_NEW

    # §25.7 restated; §26.9 added a rule; §27.5 draws a boundary.
    assert "No rule appears here for the first time" in (
        THE_CONCLUSION_INTRODUCES_NOTHING_NEW)
    assert THE_TWENTY_SEVEN_GROUP_CRITERION in CHAPTER_26_CONCLUSION
    assert "beyond the scope" not in CHAPTER_26_CONCLUSION
    assert "beyond the scope" in LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE
    assert "beyond the scope" not in CHAPTER_27_CONCLUSION
    assert "Only 26.9 introduced a rule" in (
        THE_THREE_CONCLUSIONS_DO_DIFFERENT_WORK)


def test_chapter_27_is_complete_end_to_end():
    """The chapter's closing inventory. Every span it claims is asserted."""
    from hora.core.const import CHAPTER_27_IS_COMPLETE
    from hora.core.constants.book_charts import BOOK_CHARTS
    from hora.tajaka import annual, approximate, monthly, shashti_hora

    # §27.1 to §27.5: the casting, the table, the months, the sixty-hours.
    assert annual.VARSHA_PRAVESH_RULE and annual.BIRTHPLACE_RULE
    assert len(approximate.TABLE_71) == 19
    assert len(approximate.PROCEDURE) == 5
    assert monthly.YEAR_AND_MONTH_ARE_SOLAR_ARCS
    assert shashti_hora.SHASHTI_HORAS_PER_YEAR == 144

    # Chart 66, Example 118 and Exercise 47.
    assert 66 in BOOK_CHARTS
    assert annual.EXAMPLE_118 and annual.EXAMPLE_118_NATIVITY
    assert approximate.EXERCISE_47 and approximate.EXERCISE_47_ANSWER

    # Footnotes 75 to 78, one per section that carries one.
    assert annual.FOOTNOTE_75 and annual.FOOTNOTE_76
    assert approximate.FOOTNOTE_77 and shashti_hora.FOOTNOTE_78

    assert "Closed here: OI-151" in CHAPTER_27_IS_COMPLETE
    assert "Opened here: D-78" in CHAPTER_27_IS_COMPLETE
    assert "footnote 74's bar on death readings still stands" in (
        CHAPTER_27_IS_COMPLETE)
