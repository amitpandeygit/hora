"""Example 58 — B.V. Raman's chart, read from the Moon's star and the 8th.

The example gives both readings, so both are checked. It also names two
marakas §14.2's rule cannot reach; see OI-118.
"""
from __future__ import annotations

import pytest
import swisseph as swe

from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.maraka import maraka_sthanas, marakas
from hora.core.const import RASI_LORD, Graha
from hora.core.settings import DashaYearLength, NodeType, Settings
from hora.core.timeutil import from_local
from hora.dasha.base import (
    balance_at_birth,
    compute_nakshatra_dasha,
    find_running,
    variation_candidates,
)
from hora.dasha.nakshatra.systems import VIMSHOTTARI as V

GRAHAS = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
          Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU)
TAURUS, CANCER, LEO, VIRGO, AQUARIUS, PISCES = 1, 3, 4, 5, 10, 11
DEATH = swe.julday(1998, 12, 20, 12.0)


@pytest.fixture(scope="module")
def chart23():
    record = book_chart(23)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 23", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def signs(chart23):
    return {int(g): int(chart23.positions[int(g)].longitude // 30) for g in GRAHAS}


def test_the_chart_recomputes(chart23, signs):
    """Every graha inside an arcminute. The ascendant is 8' out, which is
    about half a minute of birth time against a time printed to the minute."""
    from hora.charts.book import chart, longitudes
    from hora.core.const import RASI_ABBR

    printed = longitudes(23)
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert abs(chart23.positions[int(graha)].longitude - printed[body]) < 1.0 / 60
        assert RASI_ABBR[signs[int(graha)]] == chart(23)["drawn"][body], body

    ascendant = abs(chart23.lagna_longitude - printed["Asc"]) * 60
    assert 7.0 < ascendant < 9.0


def test_the_pada_rule_fires_for_both_straddling_stars(chart23):
    """"The 4th star is Pushyami in Cancer. The 8th star is Uttaraphalguni and
    its 1st quarter is in Leo."

    Two of the three candidate stars straddle signs here — the Moon's own and
    the 8th — so the pada rule decides twice in one chart.
    """
    moon = chart23.positions[int(Graha.MOON)].longitude
    got = {v.star: v for v in variation_candidates(moon, "longevity")}

    assert got[1].nakshatra_name == "Mrigashira"
    assert got[1].spans_two_signs is True
    assert got[1].rasi == TAURUS

    assert got[4].nakshatra_name == "Pushya"
    assert got[4].spans_two_signs is False
    assert got[4].rasi == CANCER

    assert got[8].nakshatra_name == "Uttara Phalguni"
    assert got[8].spans_two_signs is True
    assert got[8].rasi == LEO
    assert "pada 1" in got[8].reason


def test_the_eighth_star_is_the_suns_and_starts_his_dasa(chart23):
    """"we can start dasas from Sun who owns Uttaraphalguni".

    Leo is chosen as the strongest sign, and Leo is where the example's three
    marakas sit — which is the maraka criterion of §16.5.2 again.
    """
    moon = chart23.positions[int(Graha.MOON)].longitude
    lord, _balance = balance_at_birth(V, moon, start_star=8)
    assert lord == int(Graha.SUN)


@pytest.mark.parametrize(
    "star,pair",
    [
        (1, (Graha.VENUS, Graha.SUN)),        # "he passed away in Venus-Sun"
        (8, (Graha.MERCURY, Graha.RAHU)),     # "Mercury-Rahu ... in December 1998"
    ],
)
def test_both_readings_the_example_gives(chart23, star, pair):
    moon = chart23.positions[int(Graha.MOON)].longitude
    periods = compute_nakshatra_dasha(
        V, moon, chart23.instant.jd_ut, DashaYearLength.SAVANA,
        levels=2, cycles=1, start_star=star)
    chain = [p.lord for p in find_running(periods, DEATH)]
    assert chain == [int(pair[0]), int(pair[1])]


def test_the_sun_is_placed_where_he_is_least_likely_to_kill(chart23, signs):
    """"Though Sun owns 7th, he is in 6th, i.e. in the 12th from 7th and the
    11th from 8th. The likelihood of Sun killing the native is small."

    All three descriptions have to land on the same rasi, and they do.
    """
    lagna = int(chart23.lagna_longitude // 30)
    assert lagna == AQUARIUS
    sthanas = maraka_sthanas(lagna)
    assert int(RASI_LORD[sthanas[7]]) == int(Graha.SUN)

    sun = signs[int(Graha.SUN)]
    assert (sun - lagna) % 12 + 1 == 6
    assert sun == (sthanas[7] - 1) % 12            # the 12th from the 7th
    assert sun == ((lagna + 7) % 12 + 10) % 12     # the 11th from the 8th


def test_two_of_the_examples_marakas_are_beyond_section_14_2s_rule(chart23, signs):
    """See OI-118. "Venus is a maraka being in the 7th house" and "Mercury ...
    owns 8th and occupies 7th".

    §14.2 gives lords of the 2nd and 7th, plus malefics contacting them.
    Neither reaches a benefic that merely occupies the 7th, so our list misses
    the two the example rates strongest and weakest. Pinned so the gap is a
    recorded fact rather than a surprise when the rule is revisited.
    """
    lagna = int(chart23.lagna_longitude // 30)
    ours = {m["graha_name"] for m in marakas(lagna, signs)["maraka_grahas"]}

    assert {"Sun", "Rahu", "Mars"} <= ours          # the three we do find
    assert "Venus" not in ours
    assert "Mercury" not in ours

    # Both sit in the 7th, which is what the example calls them marakas for.
    seventh = maraka_sthanas(lagna)[7]
    assert seventh == LEO
    assert signs[int(Graha.VENUS)] == seventh
    assert signs[int(Graha.MERCURY)] == seventh

    # And Mercury owns the 8th, a house of life, not one of §14.2's two.
    assert int(RASI_LORD[(lagna + 7) % 12]) == int(Graha.MERCURY)


def test_mars_is_reached_by_a_different_route_than_the_example_takes(chart23, signs):
    """"Mars is also a maraka, being the 3rd lord in 7th."

    We agree he is a maraka, but as a malefic conjoining the 7th house. The
    verdict matches; the reason does not, and that is worth knowing.
    """
    lagna = int(chart23.lagna_longitude // 30)
    found = {m["graha_name"]: m for m in marakas(lagna, signs)["maraka_grahas"]}
    assert "Mars" in found
    assert any("7th house" in r for r in found["Mars"]["reasons"])
    assert not any("3rd" in r for r in found["Mars"]["reasons"])
    assert int(RASI_LORD[(lagna + 2) % 12]) == int(Graha.MARS)
