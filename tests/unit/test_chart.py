"""Natal chart assembly."""
from hora.charts.chart import nakshatra_of
from hora.core.const import Graha


def test_lagna_and_grahas_are_populated(pvr_chart):
    assert 0 <= pvr_chart.lagna_rasi <= 11
    assert set(pvr_chart.grahas) == set(range(9))


def test_ayanamsa_is_lahiri_scale(pvr_chart):
    # Lahiri ayanamsa was ~23 deg 28' in late 1972.
    assert 23.0 < pvr_chart.ayanamsa < 24.0


def test_ketu_is_exactly_opposite_rahu(pvr_chart):
    rahu = pvr_chart.positions[Graha.RAHU].longitude
    ketu = pvr_chart.positions[Graha.KETU].longitude
    assert abs((ketu - rahu) % 360.0 - 180.0) < 1e-9


def test_nodes_are_reported_retrograde(pvr_chart):
    assert pvr_chart.grahas[Graha.RAHU].retrograde
    assert pvr_chart.grahas[Graha.KETU].retrograde


def test_houses_are_whole_sign_by_default(pvr_chart):
    for state in pvr_chart.grahas.values():
        expected = (state.rasi - pvr_chart.lagna_rasi) % 12 + 1
        assert state.house == expected


def test_nakshatra_and_pada_boundaries():
    assert nakshatra_of(0.0) == (0, 1)
    assert nakshatra_of(3.4) == (0, 2)
    assert nakshatra_of(13.0) == (0, 4)
    assert nakshatra_of(13.4) == (1, 1)
    assert nakshatra_of(359.9) == (26, 4)


def test_moon_is_in_pushya_for_the_reference_chart(pvr_chart):
    """Cross-check against the published chart in PVR's own book."""
    assert pvr_chart.grahas[Graha.MOON].nakshatra_name == "Pushya"
    assert pvr_chart.grahas[Graha.MOON].rasi_name == "Cancer"


def test_lord_of_house_is_consistent_with_lagna(pvr_chart):
    from hora.core.const import RASI_LORD

    for house in range(1, 13):
        sign = (pvr_chart.lagna_rasi + house - 1) % 12
        assert pvr_chart.lord_of_house(house) == RASI_LORD[sign]


def test_dms_formatting_carries_on_rounding():
    from hora.core.timeutil import format_dms

    assert format_dms(12.0) == "12-00-00"
    assert format_dms(12.5) == "12-30-00"
    # 12 deg 34' 59.7" must carry rather than print an invalid 60 seconds.
    assert format_dms(12 + 34 / 60 + 59.7 / 3600) == "12-35-00"
    # And a carry that cascades into the degree.
    assert format_dms(12 + 59 / 60 + 59.7 / 3600) == "13-00-00"
    assert format_dms(-12.5) == "-12-30-00"
    assert format_dms(12 + 59 / 60 + 59.7 / 3600, seconds=False) == "13-00"
