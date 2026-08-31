"""Example 53 — a lady's saptamsa, and why Rahu dasa gave children.

The first example in the book that can be checked against events outside the
chart: two childbirths with dates. That makes it the strongest test of the
savana-versus-sidereal question, because the two year lengths disagree about
which periods were running when the children were born. See OI-115.
"""
from __future__ import annotations

import pytest
import swisseph as swe

from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.colord import CO_LORDS, stronger
from hora.charts.karaka import karaka_of, naisargika_karaka
from hora.charts.vargas import d7_saptamsa
from hora.core.const import RASI_LORD, Graha
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
LIBRA, LEO, AQUARIUS = 6, 4, 10
FIRST_CHILD = swe.julday(1994, 11, 15, 12.0)
SECOND_CHILD = swe.julday(1996, 12, 15, 12.0)


@pytest.fixture(scope="module")
def chart18():
    record = book_chart(18)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 18", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def d7(chart18):
    return {int(g): d7_saptamsa(chart18.positions[int(g)].longitude).sign
            for g in GRAHAS}


def test_the_rasi_chart_recomputes_including_the_ascendant(chart18):
    from hora.charts.book import longitudes

    printed = longitudes(18)
    assert abs(chart18.lagna_longitude - printed["Asc"]) < 1.0 / 60
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert abs(chart18.positions[int(graha)].longitude - printed[body]) < 1.0 / 60


def test_the_d7_reproduces_the_drawn_diagram(chart18, d7):
    from hora.charts.book import divisional
    from hora.core.const import RASI_ABBR

    drawn = divisional(18, "D7")
    assert RASI_ABBR[d7_saptamsa(chart18.lagna_longitude).sign] == drawn["Asc"]
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert RASI_ABBR[d7[int(graha)]] == drawn[body], body


def test_the_fifth_house_of_the_saptamsa_is_aquarius(chart18):
    """"The 5th house shows children and it is in Aq here." The D-7 lagna is
    Libra, whose lord Venus matters two claims later."""
    lagna = d7_saptamsa(chart18.lagna_longitude).sign
    assert lagna == LIBRA
    assert int(RASI_LORD[lagna]) == int(Graha.VENUS)
    assert (lagna + 4) % 12 == AQUARIUS


def test_parasaras_rule_here_is_section_15_5_1s_basic_rule(chart18, d7):
    """"It is owned by Saturn and Rahu. If one of the owners occupies the
    sign, the other owner acts as the main owner, according to Parasara.
    Saturn is in Aq. So Rahu acts as the 5th lord in this chart."

    That is word for word what §15.5.1 calls its basic rule, and this example
    supplies the attribution the earlier section did not.
    """
    assert set(CO_LORDS[AQUARIUS]) == {int(Graha.SATURN), int(Graha.RAHU)}
    assert d7[int(Graha.SATURN)] == AQUARIUS

    d7_lon = {int(g): d7_saptamsa(chart18.positions[int(g)].longitude).longitude
              for g in GRAHAS}
    verdict = stronger(AQUARIUS, d7_lon, purpose="arudha")
    assert verdict.winner == int(Graha.RAHU)
    assert verdict.decided_by == "basic"


def test_rahu_sits_in_the_eleventh_with_the_lagna_lord(chart18, d7):
    """"He is in the 11th house of gains, with lagna lord Venus. His
    conjunction with Venus — conjunction of 1st and 5th lords — consists of a
    raja yoga in the house of gains.\""""
    lagna = d7_saptamsa(chart18.lagna_longitude).sign
    house = (d7[int(Graha.RAHU)] - lagna) % 12 + 1
    assert house == 11
    assert d7[int(Graha.RAHU)] == d7[int(Graha.VENUS)] == LEO


def test_jupiter_is_both_putra_karakas_and_sits_in_the_fifth(chart18, d7):
    """"Jupiter is the naisargika and chara puttra karaka and he is in the
    5th house here.\""""
    lons = {int(g): chart18.positions[int(g)].longitude
            for g in GRAHAS if g is not Graha.KETU}
    assert karaka_of(lons, "PK").graha == int(Graha.JUPITER)
    assert naisargika_karaka(5)["graha"] == int(Graha.JUPITER)
    assert d7[int(Graha.JUPITER)] == AQUARIUS


def test_saturn_owns_the_fifth_and_occupies_it_with_jupiter(d7):
    """"Saturn also owns 5th and moreover he occupies 5th with Jupiter.\""""
    assert int(Graha.SATURN) in CO_LORDS[AQUARIUS]
    assert d7[int(Graha.SATURN)] == d7[int(Graha.JUPITER)] == AQUARIUS


def test_the_first_dasa_is_the_suns_with_the_balance_the_example_states(chart18):
    """"Moon is in Sun's constellation. First dasa belongs to Sun. About 1
    year and 3 months of Sun dasa was over before birth and the remainder of
    Sun dasa at birth was about 4 years and 9 months.\""""
    moon = chart18.positions[int(Graha.MOON)].longitude
    lord, balance = balance_at_birth(V, moon)
    assert lord == int(Graha.SUN)
    assert balance == pytest.approx(4 + 9 / 12, abs=0.02)
    assert 6 - balance == pytest.approx(1 + 3 / 12, abs=0.02)


# --------------------------------------------------------------------------
# The three points where savana and sidereal disagree. See OI-115.
# --------------------------------------------------------------------------


def _running(chart, jd, year_length):
    periods = compute_nakshatra_dasha(
        V, chart.positions[int(Graha.MOON)].longitude, chart.instant.jd_ut,
        year_length, levels=3, cycles=1)
    return [p.lord for p in find_running(periods, jd)]


def test_rahu_dasa_starts_at_the_end_of_1993_under_savana(chart18):
    """"Rahu dasa started at the end of 1993." Savana puts it in November;
    sidereal pushes it to the following February."""
    moon = chart18.positions[int(Graha.MOON)].longitude

    def rahu_start(year_length):
        periods = compute_nakshatra_dasha(
            V, moon, chart18.instant.jd_ut, year_length, levels=1, cycles=1)
        start = next(p for p in periods if p.lord == int(Graha.RAHU)).start_jd
        return swe.revjul(start)[:2]

    assert rahu_start(DashaYearLength.SAVANA) == (1993, 11)
    assert rahu_start(DashaYearLength.SIDEREAL) == (1994, 2)


def test_the_antardasas_at_the_two_births_were_rahus_and_jupiters(chart18):
    """"Antardasas at the time of childbirth belonged to Rahu and Jupiter."

    Both year lengths agree here, so the antardasa alone does not settle
    anything — it is the pratyantardasa below that does.
    """
    for year_length in (DashaYearLength.SAVANA, DashaYearLength.SIDEREAL):
        assert _running(chart18, FIRST_CHILD, year_length)[:2] == [
            int(Graha.RAHU), int(Graha.RAHU)]
        assert _running(chart18, SECOND_CHILD, year_length)[:2] == [
            int(Graha.RAHU), int(Graha.JUPITER)]


def test_saturn_ran_the_pratyantardasa_at_both_births_only_under_savana(chart18):
    """"Hence pratyantardasa at the time of both the childbirths belonged to
    Saturn."

    This is the sharpest evidence in the chapter for the year length. Under
    savana Saturn is running at both births, as the example says. Under our
    sidereal default Jupiter is running at both, and the example's conclusion
    — that the pratyantardasa belongs to the strongest planet influencing the
    house of interest — would not follow from the chart at all.
    """
    savana = DashaYearLength.SAVANA
    assert _running(chart18, FIRST_CHILD, savana)[2] == int(Graha.SATURN)
    assert _running(chart18, SECOND_CHILD, savana)[2] == int(Graha.SATURN)

    sidereal = DashaYearLength.SIDEREAL
    assert _running(chart18, FIRST_CHILD, sidereal)[2] == int(Graha.JUPITER)
    assert _running(chart18, SECOND_CHILD, sidereal)[2] == int(Graha.JUPITER)
