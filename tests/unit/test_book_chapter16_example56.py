"""Example 56 — Vimsottari read as an ayur dasa, over JFK Jr's chart.

The first example in the book to print a Rudra, which turns out to disagree
with §14.3's own instruction about which 8th house to use. See D-53.
"""
from __future__ import annotations

import pytest
import swisseph as swe

from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.karaka import karaka_of
from hora.charts.maraka import (
    houses_of_life,
    maheswara,
    maraka_houses,
    maraka_sthanas,
    ordinary_eighth,
    rudra,
    rudra_eighth,
)
from hora.core.const import RASI_LORD, Graha
from hora.core.settings import DashaYearLength, NodeType, Settings
from hora.core.timeutil import from_local
from hora.dasha.base import compute_nakshatra_dasha, find_running
from hora.dasha.nakshatra.systems import VIMSHOTTARI as V

GRAHAS = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
          Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU)
LEO, VIRGO, LIBRA, AQUARIUS, GEMINI = 4, 5, 6, 10, 2
DEATH = swe.julday(1999, 7, 16, 22.0)


@pytest.fixture(scope="module")
def chart21():
    record = book_chart(21)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 21", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def signs(chart21):
    return {int(g): int(chart21.positions[int(g)].longitude // 30) for g in GRAHAS}


def test_the_chart_recomputes(chart21, signs):
    from hora.charts.book import chart, longitudes
    from hora.core.const import RASI_ABBR

    printed = longitudes(21)
    assert abs(chart21.lagna_longitude - printed["Asc"]) < 1.0 / 60
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert abs(chart21.positions[int(graha)].longitude - printed[body]) < 1.0 / 60
        assert RASI_ABBR[signs[int(graha)]] == chart(21)["drawn"][body], body


def test_parasaras_houses_of_life_and_death():
    """"the 3rd and 8th houses are the houses of life and the 2nd and 7th
    houses are the houses of death." Chapter 14 already held both."""
    assert sorted(houses_of_life()) == [3, 8]
    assert maraka_houses() == (2, 7)


def test_the_second_lord_and_the_seventh_lord(chart21, signs):
    """"Here the 2nd house is Virgo. Its lord Mercury is in ... the 3rd house
    ... Saturn is the 7th lord.\""""
    lagna = int(chart21.lagna_longitude // 30)
    assert lagna == LEO
    sthanas = maraka_sthanas(lagna)
    assert sthanas[2] == VIRGO
    assert int(RASI_LORD[VIRGO]) == int(Graha.MERCURY)
    assert (signs[int(Graha.MERCURY)] - lagna) % 12 + 1 == 3
    assert int(RASI_LORD[sthanas[7]]) == int(Graha.SATURN)


def test_saturn_is_maheswara_as_the_eighth_lord_from_the_atma_karaka(chart21, signs):
    """"He is also Maheswara, being the 8th lord from AK Mars."

    Maheswara uses the ordinary 8th, which is what makes the Rudra disagreement
    below worth noticing rather than assuming.
    """
    lons = {int(g): chart21.positions[int(g)].longitude
            for g in GRAHAS if g is not Graha.KETU}
    assert karaka_of(lons, "AK").graha == int(Graha.MARS)
    assert signs[int(Graha.MARS)] == GEMINI

    result = maheswara(signs[int(Graha.MARS)], signs)
    assert result["maheswara"] == int(Graha.SATURN)


def test_the_printed_rudra_needs_the_ordinary_eighth_not_table_32(chart21, signs):
    """See D-53. "He joins Jupiter, who is Rudra."

    §14.3 says to find the 8th "using Table 32 and not in the normal way".
    Under Table 32 Leo's 8th is Cancer and the 7th house's is Capricorn, so
    the candidates are the Moon and Saturn and Jupiter cannot be Rudra at all.
    Under the ordinary 8th the candidates are Jupiter and Mercury, and the
    same cascade picks Jupiter — the book's answer.
    """
    lagna = int(chart21.lagna_longitude // 30)
    seventh = (lagna + 6) % 12

    # What §14.3's instruction gives, and what we return today.
    table32 = {int(RASI_LORD[rudra_eighth(s)]) for s in (lagna, seventh)}
    assert table32 == {int(Graha.MOON), int(Graha.SATURN)}
    assert int(Graha.JUPITER) not in table32

    lons = {int(g): chart21.positions[int(g)].longitude for g in GRAHAS}
    assert rudra(lagna, signs, lons)["rudra"] == "Saturn"

    # What the book's answer requires.
    ordinary = {int(RASI_LORD[ordinary_eighth(s)]) for s in (lagna, seventh)}
    assert ordinary == {int(Graha.JUPITER), int(Graha.MERCURY)}

    # And the cascade's first rule picks Jupiter from those two.
    def co_tenants(graha):
        return sum(1 for o in signs if o != graha and signs[o] == signs[graha])

    assert co_tenants(int(Graha.JUPITER)) > co_tenants(int(Graha.MERCURY))


def test_saturn_joins_jupiter(signs):
    """"He joins Jupiter" — whichever of them turns out to be Rudra."""
    assert signs[int(Graha.SATURN)] == signs[int(Graha.JUPITER)]


def test_mritya_bhaga_is_not_something_we_hold():
    """See OI-117. The example calls Mercury a strong maraka partly because he
    is "in mritya bhaga", a table of fatal degrees we do not have.

    `Upagraha.MRITYU` is the time-based shadow planet and must not be mistaken
    for it, so this asserts they are different things rather than leaving the
    name to be confused later.
    """
    from hora.core.const import Upagraha

    assert Upagraha.MRITYU.name == "MRITYU"          # a time-based upagraha
    from hora.core import const

    assert not any("BHAGA" in name for name in dir(const))


@pytest.mark.parametrize("year_length", [DashaYearLength.SAVANA,
                                         DashaYearLength.SIDEREAL])
def test_saturn_mercury_was_running_at_death(chart21, year_length):
    """"Mr. Kennedy was running Saturn-Mercury antardasa when he passed away."

    Both year lengths agree here, so this example does not bear on OI-115.
    """
    periods = compute_nakshatra_dasha(
        V, chart21.positions[int(Graha.MOON)].longitude, chart21.instant.jd_ut,
        year_length, levels=2, cycles=1)
    chain = [p.lord for p in find_running(periods, DEATH)]
    assert chain == [int(Graha.SATURN), int(Graha.MERCURY)]
