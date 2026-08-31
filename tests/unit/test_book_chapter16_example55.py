"""Example 55 — the example where the author's own prediction failed.

He read the chart from the Moon's star, predicted the man would win his
lawsuit in Mars antardasa, and was wrong. The example's point is that the
utpanna variation — §16.4.1's 5th star — fits the events and the Moon's star
does not. Both readings are checked here, since the example rests on them
differing.
"""
from __future__ import annotations

import pytest
import swisseph as swe

from hora.charts.arudha import all_arudha_padas
from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.colord import CO_LORDS, stronger
from hora.charts.dignity import sign_dignity
from hora.charts.functional import is_yogakaraka
from hora.charts.planetary_yogas.registry import YogaInput, evaluate_one
from hora.core.const import (
    NAKSHATRA_NAMES,
    NAKSHATRA_SPAN,
    RASI_LORD,
    Graha,
)
from hora.core.settings import DashaYearLength, NodeType, Settings
from hora.core.timeutil import from_local
from hora.dasha.base import (
    balance_at_birth,
    compute_nakshatra_dasha,
    find_running,
)
from hora.dasha.nakshatra.systems import VIMSHOTTARI as V

GRAHAS = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
          Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU)
SCORPIO, TAURUS, PISCES, CANCER = 7, 1, 11, 3
CRISIS = swe.julday(1995, 12, 20, 12.0)


@pytest.fixture(scope="module")
def chart20():
    record = book_chart(20)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 20", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def rasis(chart20):
    return {int(g): int(chart20.positions[int(g)].longitude // 30) for g in GRAHAS}


def test_the_chart_recomputes(chart20, rasis):
    from hora.charts.book import chart, longitudes
    from hora.core.const import RASI_ABBR

    printed = longitudes(20)
    assert abs(chart20.lagna_longitude - printed["Asc"]) < 1.0 / 60
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert abs(chart20.positions[int(graha)].longitude - printed[body]) < 1.0 / 60
        assert RASI_ABBR[rasis[int(graha)]] == chart(20)["drawn"][body], body


def test_the_moons_star_and_the_utpanna_star(chart20):
    """"Moon is in Rohini. The 5th star Pushyami is in Cancer.\""""
    star = int(chart20.positions[int(Graha.MOON)].longitude // NAKSHATRA_SPAN)
    assert NAKSHATRA_NAMES[star] == "Rohini"
    fifth = (star + 4) % 27
    assert NAKSHATRA_NAMES[fifth] == "Pushya"
    assert int(fifth * NAKSHATRA_SPAN // 30) == CANCER


def test_cancer_is_strong_by_the_reason_the_example_gives(chart20, rasis):
    """"Occupied by an exalted planet and owned by another exalted planet,
    Cancer is very strong."

    Jupiter is exalted in Cancer and we agree. The other planet is Cancer's
    lord, the Moon, and there the words part company — see D-52. Taurus is
    his exaltation sign, but his exaltation degree is Taurus 3 and his
    moolatrikona runs from there to the end of the sign, so at 17 Ta 12 our
    dignity is moolatrikona. The example's point stands either way; only the
    label differs.
    """
    assert rasis[int(Graha.JUPITER)] == CANCER
    assert sign_dignity(int(Graha.JUPITER),
                        chart20.positions[int(Graha.JUPITER)].longitude) == "exalted"

    assert int(RASI_LORD[CANCER]) == int(Graha.MOON)
    moon_lon = chart20.positions[int(Graha.MOON)].longitude
    assert rasis[int(Graha.MOON)] == TAURUS            # his exaltation sign
    assert sign_dignity(int(Graha.MOON), moon_lon) == "moolatrikona"


def test_the_moons_star_gives_the_reading_that_misled(chart20):
    """"He was then running Jupiter-Moon antardasa... This author's prediction
    went wrong because he blindly used Vimsottari dasa started from Moon's
    star.\""""
    moon = chart20.positions[int(Graha.MOON)].longitude
    periods = compute_nakshatra_dasha(
        V, moon, chart20.instant.jd_ut, DashaYearLength.SAVANA,
        levels=2, cycles=1, start_star=1)
    chain = [p.lord for p in find_running(periods, CRISIS)]
    assert chain == [int(Graha.JUPITER), int(Graha.MOON)]


def test_the_utpanna_star_gives_saturn_first_and_venus_from_1987_to_2006(chart20):
    """"First dasa belongs to Saturn. Venus dasa of 20 years runs from
    February 1987 to October 2006." Both months land exactly."""
    moon = chart20.positions[int(Graha.MOON)].longitude
    lord, _balance = balance_at_birth(V, moon, start_star=5)
    assert lord == int(Graha.SATURN)

    periods = compute_nakshatra_dasha(
        V, moon, chart20.instant.jd_ut, DashaYearLength.SAVANA,
        levels=1, cycles=1, start_star=5)
    venus = next(p for p in periods if p.lord == int(Graha.VENUS))
    assert swe.revjul(venus.start_jd)[:2] == (1987, 2)
    assert swe.revjul(venus.end_jd)[:2] == (2006, 10)


def test_the_sub_periods_of_the_crisis(chart20):
    """"Rahu's antardasa runs during 1994-1997"; "Ketu's pratyantardasa ran
    during December 1995-February 1996"; Sun's when he went back to India in
    mid-1996; Jupiter's antardasa when he returned in 1998.

    Ketu's boundaries fall on 27 November and 29 January, four days and two
    days short of the months the example names, so its range is the example's
    rounded outward. Everything else lands inside the stated period.
    """
    moon = chart20.positions[int(Graha.MOON)].longitude
    periods = compute_nakshatra_dasha(
        V, moon, chart20.instant.jd_ut, DashaYearLength.SAVANA,
        levels=3, cycles=1, start_star=5)
    venus = next(p for p in periods if p.lord == int(Graha.VENUS))

    rahu = next(a for a in venus.children if a.lord == int(Graha.RAHU))
    assert swe.revjul(rahu.start_jd)[0] == 1994
    assert swe.revjul(rahu.end_jd)[0] == 1997

    ketu = next(p for p in rahu.children if p.lord == int(Graha.KETU))
    assert swe.revjul(ketu.start_jd)[:3] == (1995, 11, 27)
    assert swe.revjul(ketu.end_jd)[:3] == (1996, 1, 29)

    sun = next(p for p in rahu.children if p.lord == int(Graha.SUN))
    assert swe.revjul(sun.start_jd)[0] == 1996          # "mid-1996"

    jupiter = next(a for a in venus.children if a.lord == int(Graha.JUPITER))
    assert jupiter.start_jd < swe.julday(1998, 7, 1, 12.0) < jupiter.end_jd


def test_sidereal_years_put_the_crisis_in_the_wrong_periods(chart20):
    """A fourth chart where the example's dates need savana. Under sidereal
    Ketu's pratyantardasa falls in July 1996, seven months late."""
    moon = chart20.positions[int(Graha.MOON)].longitude
    periods = compute_nakshatra_dasha(
        V, moon, chart20.instant.jd_ut, DashaYearLength.SIDEREAL,
        levels=3, cycles=1, start_star=5)
    venus = next(p for p in periods if p.lord == int(Graha.VENUS))
    rahu = next(a for a in venus.children if a.lord == int(Graha.RAHU))
    ketu = next(p for p in rahu.children if p.lord == int(Graha.KETU))
    assert swe.revjul(ketu.start_jd)[:2] == (1996, 7)


# --------------------------------------------------------------------------
# The reading, and the one claim in it that is wrong. See D-51.
# --------------------------------------------------------------------------


def test_venus_occupies_the_lagna_but_does_not_rule_it(chart20, rasis):
    """See D-51. "Venus is lagna lord" — he is not; he is in the lagna.

    The rest of the sentence holds, and the example itself later gets the
    lordship right when it says "Ketu is lagna lord".
    """
    lagna = int(chart20.lagna_longitude // 30)
    assert lagna == SCORPIO
    assert set(CO_LORDS[SCORPIO]) == {int(Graha.MARS), int(Graha.KETU)}
    assert int(Graha.VENUS) not in CO_LORDS[SCORPIO]
    assert rasis[int(Graha.VENUS)] == lagna            # in it, not ruling it

    # What the same sentence gets right.
    verdict = evaluate_one("vesi", YogaInput(rasis=rasis))
    assert verdict.present is True
    assert (rasis[int(Graha.VENUS)] - rasis[int(Graha.SUN)]) % 12 + 1 == 2


def test_venus_is_the_eighth_lord_from_the_arudha_lagna(chart20, rasis):
    """"However, being the 8th lord from AL, he can also give a fall in
    status." This half is right."""
    lagna = int(chart20.lagna_longitude // 30)
    lons = {int(g): chart20.positions[int(g)].longitude for g in GRAHAS}
    strongest = {r: stronger(r, lons, purpose="arudha").winner for r in (7, 10)}
    padas = {p.house: p.sign for p in
             all_arudha_padas(lagna, rasis, stronger_lord=strongest)}
    assert padas[1] == PISCES                          # AL, as drawn
    assert int(RASI_LORD[(padas[1] + 7) % 12]) == int(Graha.VENUS)


def test_the_tripod_reading_of_each_level(chart20, rasis):
    """Rahu judged from the Moon, Ketu and Sun from the lagna — §16.5.3's
    pairing applied, an antardasa from Moon and pratyantardasas from lagna."""
    lagna = int(chart20.lagna_longitude // 30)
    moon = rasis[int(Graha.MOON)]

    assert (rasis[int(Graha.RAHU)] - moon) % 12 + 1 == 8
    assert sign_dignity(int(Graha.RAHU),
                        chart20.positions[int(Graha.RAHU)].longitude) == "debilitated"

    assert int(Graha.KETU) in CO_LORDS[lagna]
    assert (rasis[int(Graha.KETU)] - lagna) % 12 + 1 == 8

    assert int(RASI_LORD[(lagna + 9) % 12]) == int(Graha.SUN)      # 10th lord
    assert sign_dignity(int(Graha.SUN),
                        chart20.positions[int(Graha.SUN)].longitude) == "debilitated"
    assert (rasis[int(Graha.SUN)] - lagna) % 12 + 1 == 12


def test_jupiter_and_saturn_from_the_moon(chart20, rasis):
    """"Jupiter is the 8th and 11th lord from Moon. He is in the 3rd from
    Moon." and "Saturn is an exalted yogakaraka from Moon.\""""
    moon = rasis[int(Graha.MOON)]
    assert moon == TAURUS
    assert int(RASI_LORD[(moon + 7) % 12]) == int(Graha.JUPITER)
    assert int(RASI_LORD[(moon + 10) % 12]) == int(Graha.JUPITER)
    assert (rasis[int(Graha.JUPITER)] - moon) % 12 + 1 == 3

    assert sign_dignity(int(Graha.SATURN),
                        chart20.positions[int(Graha.SATURN)].longitude) == "exalted"
    assert is_yogakaraka("Saturn", moon) is True
