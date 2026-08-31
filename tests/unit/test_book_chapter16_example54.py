"""Example 54 — Navin Patnaik's rasi chart, and why Mercury dasa gave office.

Elected Chief Minister of Orissa in early 2000, which dates the event the
example explains. Like Example 53 the dasa only lands under savana years, and
here it lands to the month. See OI-115.

One claim is unchecked: Rajya saham. See OI-116.
"""
from __future__ import annotations

import pytest
import swisseph as swe

from hora.charts.arudha import all_arudha_padas
from hora.charts.aspects import graha_aspects_sign, rasi_drishti
from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.colord import stronger
from hora.charts.functional import from_rules
from hora.charts.planetary_yogas.registry import YogaInput, evaluate_one
from hora.charts.special_lagna import all_special_lagnas
from hora.charts.vargas import d10_dasamsa
from hora.core.const import RASI_LORD, Graha
from hora.core.ephemeris.swiss import SwissEphemeris
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
CANCER, LIBRA, VIRGO, GEMINI, TAURUS, ARIES = 3, 6, 5, 2, 1, 0
ELECTED = swe.julday(2000, 3, 5, 12.0)          # "early 2000"


@pytest.fixture(scope="module")
def chart19():
    record = book_chart(19)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 19", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def rasis(chart19):
    return {int(g): int(chart19.positions[int(g)].longitude // 30) for g in GRAHAS}


def test_the_chart_recomputes_and_matches_its_drawn_rasi(chart19, rasis):
    """Unlike Charts 17 and 18, the drawn diagram here is the rasi itself."""
    from hora.charts.book import chart, longitudes
    from hora.core.const import RASI_ABBR

    printed = longitudes(19)
    assert abs(chart19.lagna_longitude - printed["Asc"]) < 1.0 / 60
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert abs(chart19.positions[int(graha)].longitude - printed[body]) < 1.0 / 60
        assert RASI_ABBR[rasis[int(graha)]] == chart(19)["drawn"][body], body


def test_the_first_dasa_is_mars(chart19):
    """"First dasa is of Mars." Only six months of it remained."""
    lord, balance = balance_at_birth(
        V, chart19.positions[int(Graha.MOON)].longitude)
    assert lord == int(Graha.MARS)
    assert balance < 0.5


def test_mercury_dasa_began_in_july_1999_under_savana(chart19):
    """"Mercury dasa started in July 1999."

    Sidereal is nine months late — the drift accumulated over the four
    mahadasas before it — so this example dates the year length to the month.
    """
    moon = chart19.positions[int(Graha.MOON)].longitude

    def start(year_length):
        periods = compute_nakshatra_dasha(
            V, moon, chart19.instant.jd_ut, year_length, levels=1, cycles=1)
        mercury = next(p for p in periods if p.lord == int(Graha.MERCURY))
        return swe.revjul(mercury.start_jd)[:2]

    assert start(DashaYearLength.SAVANA) == (1999, 7)
    assert start(DashaYearLength.SIDEREAL) == (2000, 4)


def test_mercury_ad_in_mercury_md_was_running_at_the_election(chart19):
    """"Mercury antardasa in Mercury mahadasa was running when he became
    Orissa's CM." Under sidereal an entirely different pair is running."""
    moon = chart19.positions[int(Graha.MOON)].longitude

    def chain(year_length):
        periods = compute_nakshatra_dasha(
            V, moon, chart19.instant.jd_ut, year_length, levels=2, cycles=1)
        return [p.lord for p in find_running(periods, ELECTED)]

    assert chain(DashaYearLength.SAVANA) == [int(Graha.MERCURY), int(Graha.MERCURY)]
    assert chain(DashaYearLength.SIDEREAL) != [int(Graha.MERCURY), int(Graha.MERCURY)]


def test_mercury_and_gl_share_libra(chart19, rasis):
    """"Mercury is in Libra. Rajya saham and GL are also in Libra."

    GL checks out. The saham does not — we compute no sahams; see OI-116.
    """
    assert rasis[int(Graha.MERCURY)] == LIBRA

    settings = Settings(node_type=NodeType.MEAN)
    eph = SwissEphemeris(settings)
    record = book_chart(19)
    lat, lon = record["place"]["latitude"], record["place"]["longitude"]
    sunrise = eph.sunrise(chart19.instant.jd_ut - 1.5, lat, lon)
    while True:
        nxt = eph.sunrise(sunrise + 0.5, lat, lon)
        if nxt is None or nxt > chart19.instant.jd_ut:
            break
        sunrise = nxt
    lagnas = all_special_lagnas(
        sunrise_jd=sunrise, jd_ut=chart19.instant.jd_ut,
        lagna_longitude=chart19.lagna_longitude,
        moon_longitude=chart19.positions[int(Graha.MOON)].longitude,
        settings=settings)
    assert int(lagnas[2].longitude // 30) == LIBRA


def test_mercury_is_the_sixth_from_the_arudha_lagna(chart19, rasis):
    """"From AL, Mercury is in the 6th house. Upachayas from AL bring gains in
    status.\""""
    lagna = int(chart19.lagna_longitude // 30)
    lons = {int(g): chart19.positions[int(g)].longitude for g in GRAHAS}
    strongest = {r: stronger(r, lons, purpose="arudha").winner for r in (7, 10)}
    padas = {p.house: p.sign for p in
             all_arudha_padas(lagna, rasis, stronger_lord=strongest)}
    assert padas[1] == TAURUS                              # AL, as drawn
    assert (rasis[int(Graha.MERCURY)] - padas[1]) % 12 + 1 == 6


def test_the_tripod_reading_gives_a_powerful_vesi_yoga(chart19, rasis):
    """"Sun is in Vi. We should judge mahadasa from Sun... Mercury is Sun's
    dispositor and he is in the 2nd from Sun. This results in a powerful Vesi
    yoga."

    "Powerful" is not decoration: three planets sit in that 2nd house, and our
    detector names all three.
    """
    assert rasis[int(Graha.SUN)] == VIRGO
    assert int(RASI_LORD[VIRGO]) == int(Graha.MERCURY)     # Sun's dispositor
    assert (rasis[int(Graha.MERCURY)] - rasis[int(Graha.SUN)]) % 12 + 1 == 2

    verdict = evaluate_one("vesi", YogaInput(rasis=rasis))
    assert verdict.present is True
    for name in ("Mars", "Mercury", "Jupiter"):
        assert name in verdict.reason


def test_mercury_is_first_lord_from_the_moon_and_sits_in_a_trine(rasis):
    """"Even taking Moon as the reference, Mercury is 1st lord and he is in a
    trine.\""""
    moon = rasis[int(Graha.MOON)]
    assert moon == GEMINI
    assert int(RASI_LORD[moon]) == int(Graha.MERCURY)
    assert (rasis[int(Graha.MERCURY)] - moon) % 12 + 1 in (1, 5, 9)


def test_the_three_dasamsa_reasons(chart19):
    """"Mercury is a functional benefic in dasamsa, aspects GL and occupies
    rajya pada (A10) in a quadrant from lagna."

    The aspect is rasi drishti, not graha drishti — the same reading Example
    52 used without saying so, which makes it a habit of the chapter rather
    than a one-off.
    """
    d10 = {int(g): d10_dasamsa(chart19.positions[int(g)].longitude).sign
           for g in GRAHAS}
    d10_lon = {int(g): d10_dasamsa(chart19.positions[int(g)].longitude).longitude
               for g in GRAHAS}
    lagna10 = d10_dasamsa(chart19.lagna_longitude).sign
    mercury = d10[int(Graha.MERCURY)]

    assert from_rules("Mercury", lagna10) == "functional benefic"

    # "aspects GL" — by rasi drishti only, as in Example 52.
    settings = Settings(node_type=NodeType.MEAN)
    eph = SwissEphemeris(settings)
    record = book_chart(19)
    lat, lon = record["place"]["latitude"], record["place"]["longitude"]
    sunrise = eph.sunrise(chart19.instant.jd_ut - 1.5, lat, lon)
    while True:
        nxt = eph.sunrise(sunrise + 0.5, lat, lon)
        if nxt is None or nxt > chart19.instant.jd_ut:
            break
        sunrise = nxt
    gl = all_special_lagnas(
        sunrise_jd=sunrise, jd_ut=chart19.instant.jd_ut,
        lagna_longitude=chart19.lagna_longitude,
        moon_longitude=chart19.positions[int(Graha.MOON)].longitude,
        settings=settings)[2].longitude
    gl10 = d10_dasamsa(gl).sign
    assert graha_aspects_sign(int(Graha.MERCURY), mercury, gl10) is False
    assert gl10 in rasi_drishti(mercury)

    strongest = {r: stronger(r, d10_lon, purpose="arudha").winner for r in (7, 10)}
    padas = {p.house: p.sign for p in
             all_arudha_padas(lagna10, d10, stronger_lord=strongest)}
    assert mercury == padas[10]                            # occupies A10
    assert (mercury - lagna10) % 12 + 1 in (1, 4, 7, 10)   # a quadrant
