"""Panchanga limbs and the sunrise-anchored day."""
import pytest

from hora.core.timeutil import from_local
from hora.panchanga.core import compute_panchanga

BANGALORE = (12.9716, 77.5946)


@pytest.fixture(scope="module")
def bangalore_panchanga(settings=None):
    from hora.core.settings import Settings

    inst = from_local(2026, 8, 25, 10, 0, 0, tz_name="Asia/Kolkata")
    return compute_panchanga(inst, *BANGALORE, Settings())


def test_weekday_is_derived_at_sunrise(bangalore_panchanga):
    assert bangalore_panchanga.vaara_name == "Tuesday"   # 25 Aug 2026


def test_sunrise_precedes_sunset_precedes_next_sunrise(bangalore_panchanga):
    d = bangalore_panchanga.day
    assert d.sunrise < d.sunset < d.next_sunrise
    assert 0.4 < d.day_length < 0.6      # tropical latitude, always near 12h


def test_all_five_limbs_are_present(bangalore_panchanga):
    p = bangalore_panchanga
    for limb in (p.tithis, p.nakshatras, p.yogas, p.karanas):
        assert limb
        assert all(e.name for e in limb)


def test_element_end_times_are_ordered_and_after_sunrise(bangalore_panchanga):
    p = bangalore_panchanga
    for limb in (p.tithis, p.nakshatras, p.yogas, p.karanas):
        ends = [e.end_jd for e in limb if e.end_jd is not None]
        assert ends == sorted(ends)
        assert all(e > p.day.sunrise for e in ends)


def test_karana_boundaries_align_with_tithi_boundaries(bangalore_panchanga):
    """Every tithi end is also a karana end, since a karana is half a tithi."""
    p = bangalore_panchanga
    karana_ends = {round(e.end_jd, 6) for e in p.karanas if e.end_jd}
    for t in p.tithis:
        if t.end_jd and t.end_jd < p.day.next_sunrise:
            assert round(t.end_jd, 6) in karana_ends


def test_karana_naming_covers_fixed_and_movable():
    """Book section 1.3.10: 4 fixed karanas, 7 movable repeating 8 times."""
    from hora.core.names import NameScheme
    from hora.panchanga.core import _karana_name

    assert _karana_name(0) == "Kimstughna"
    assert _karana_name(1) == "Bava"
    assert _karana_name(57) == "Sakuna"          # book spelling
    assert _karana_name(57, NameScheme.STANDARD) == "Shakuni"
    assert _karana_name(58) == "Chatushpada"
    assert _karana_name(59) == "Naga"
    # The seven movable karanas repeat eight times in between.
    assert _karana_name(8) == _karana_name(1)
    assert [_karana_name(i) for i in range(1, 57)] == [
        _karana_name(1 + i % 7) for i in range(56)
    ]


def test_polar_latitude_is_rejected_rather_than_silently_wrong():
    from hora.core.settings import Settings

    inst = from_local(2026, 6, 21, 12, 0, 0, tz_name="UTC")
    with pytest.raises(ValueError):
        compute_panchanga(inst, 78.0, 15.0, Settings())


def test_local_time_string_rounds_to_nearest_second():
    """A time 0.2 ms short of the next second must not report a second early."""
    from hora.core.timeutil import from_local, jd_to_local_str

    jd = from_local(2026, 8, 25, 6, 11, 47, tz_name="Asia/Kolkata").jd_ut
    assert jd_to_local_str(jd - 0.0002 / 86400.0, 5.5).endswith("06:11:47")
    assert jd_to_local_str(jd + 0.0002 / 86400.0, 5.5).endswith("06:11:47")


def test_sunrise_defaults_to_the_upper_limb_as_the_book_recommends():
    """Book 5.5 comment (3): "the time when the upper tip of the visual disk
    representing Sun appears to be rising ... The latter approach is
    recommended."

    This was BIT_HINDU_RISING until chapter 5 was read, on PyJHora's evidence.
    The book outranks PyJHora in docs/precedence.md, so it no longer is.
    See docs/book-deviations.md D-10.
    """
    from hora.core.settings import Settings, SunriseMode

    assert Settings().sunrise_mode is SunriseMode.DISC_UPPER_LIMB


def test_moonrise_honours_the_configured_sunrise_definition():
    """Moonrise moves by minutes between definitions; it must not be hardcoded."""
    import swisseph as swe

    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import Settings, SunriseMode

    inst = from_local(2026, 8, 25, 0, 0, 0, tz_name="Asia/Kolkata")
    times = {
        mode: get_ephemeris(Settings(sunrise_mode=mode)).body_rise(
            inst.jd_ut, swe.MOON, *BANGALORE
        )
        for mode in (SunriseMode.TRADITIONAL_HINDU, SunriseMode.DISC_CENTER)
    }
    a, b = times.values()
    assert abs(a - b) * 86400 > 60      # more than a minute apart
