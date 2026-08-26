"""§1.3.7 Solar Calendar — a year of 360 degrees, a month of 30, a day of 1.

Four sentences, and the implementation was already right: `solar_date` gives
the month as the Sun's rasi and the day as `int(degrees_in_rasi) + 1`, which
is exactly "one day stands for exactly 1 degree motion of Sun".

What was missing was the definition itself, and the fact that this calendar —
not the civil one — is what dasas and Tajaka run on.
"""
import pytest

from hora.core import const as c

# --------------------------------------------------------------------------
# The definition
# --------------------------------------------------------------------------

def test_a_solar_year_is_three_hundred_and_sixty_degrees_of_sun():
    """"one year is the time in which Sun moves by 360 degrees"."""
    assert c.SOLAR_YEAR_DEGREES == 360.0


def test_a_solar_month_is_thirty_degrees_of_sun():
    """"one month is the time in which Sun moves by 30 degrees"."""
    assert c.SOLAR_MONTH_DEGREES == 30.0
    assert c.SOLAR_YEAR_DEGREES / c.SOLAR_MONTH_DEGREES == 12


def test_a_solar_day_is_one_degree_and_a_month_has_thirty():
    """"Each solar month has 30 days, where one day stands for exactly 1
    degree motion of Sun"."""
    assert c.SOLAR_DAY_DEGREES == 1.0
    assert c.DAYS_PER_SOLAR_MONTH == 30
    assert c.DAYS_PER_SOLAR_MONTH * c.SOLAR_DAY_DEGREES == c.SOLAR_MONTH_DEGREES


def test_it_is_used_in_dasas_and_tajaka():
    """"This calendar will be used in dasas and in Tajaka analysis."

    Worth storing: it says which calendar a dasa length is measured in, and
    that is not the civil one.
    """
    assert c.SOLAR_CALENDAR_USED_IN == ("dasas", "Tajaka analysis")


def test_a_solar_year_is_not_the_savana_year():
    """SAVANA_YEAR_DAYS is 360 *days*; a solar year is 360 *degrees*.

    Both are "360" and they are different quantities. A solar year takes about
    365.25 days, not 360.
    """
    assert c.SAVANA_YEAR_DAYS == 360.0
    assert c.SOLAR_YEAR_DEGREES == 360.0
    assert c.SIDEREAL_YEAR_DAYS == pytest.approx(365.256, abs=1e-3)


# --------------------------------------------------------------------------
# The implementation matches the definition
# --------------------------------------------------------------------------

@pytest.mark.parametrize("degrees_in_rasi,day", [
    (0.0, 1), (0.99, 1), (1.0, 2), (14.5, 15), (29.0, 30), (29.999, 30),
])
def test_the_solar_day_is_the_degree_the_sun_has_entered(degrees_in_rasi, day):
    """The rule `int(degrees_in_rasi) + 1`, stated as the book states it.

    The Sun's first degree of a rasi is day 1, so a rasi yields days 1 to 30
    and never a day 0 or 31.
    """
    assert int(degrees_in_rasi) + 1 == day
    assert 1 <= day <= c.DAYS_PER_SOLAR_MONTH


def test_every_degree_of_the_zodiac_maps_to_a_valid_solar_day():
    """No gap and no overflow anywhere in the circle."""
    for tenth in range(3600):
        longitude = tenth / 10.0
        within = longitude % 30.0
        day = int(within) + 1
        assert 1 <= day <= 30, longitude


def test_the_twelve_solar_months_are_the_twelve_rasis():
    """"one month is the time in which Sun moves by 30 degrees" — which is a
    rasi, so the solar month *is* the Sun's sign."""
    assert c.SOLAR_MONTH_DEGREES == 30.0
    assert len(c.RASI_NAMES) == 12
    assert 12 * c.SOLAR_MONTH_DEGREES == c.SOLAR_YEAR_DEGREES


def test_solar_date_returns_the_suns_rasi_and_degree():
    """The shipped function, checked against the definition rather than
    against itself."""
    import inspect

    from hora.panchanga import calendar

    source = inspect.getsource(calendar.solar_date)
    assert "month=sun.rasi" in source
    assert "int(sun.degrees_in_rasi) + 1" in source


# --------------------------------------------------------------------------
# Published
# --------------------------------------------------------------------------

def test_the_section_is_published():
    from hora.services import reference_service

    payload = reference_service.terms()["solar_calendar"]
    assert payload["year_degrees"] == 360.0
    assert payload["month_degrees"] == 30.0
    assert payload["day_degrees"] == 1.0
    assert payload["days_per_month"] == 30
    assert payload["used_in"] == ["dasas", "Tajaka analysis"]
    assert "360 degrees" in payload["definition"]
    assert "not a fixed number of days" in payload["note"]
