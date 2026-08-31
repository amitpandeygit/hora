"""Example 57 — the ayur variation chosen, not assumed.

This is the chart §16.5.2's longevity path was built for. Its 4th star
straddles two signs so the pada rule decides which; and the section's maraka
criterion is actually used to pick between the candidate signs, where §16.5.2
itself only stated it. Reading from the Moon's own star gives a different pair
at death, which is what makes the choice matter.
"""
from __future__ import annotations

import pytest
import swisseph as swe

from hora.charts.aspects import rasi_drishti
from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.dignity import sign_dignity
from hora.charts.maraka import maraka_sthanas
from hora.core.const import NAKSHATRA_SPAN, RASI_LORD, Graha
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
ARIES, TAURUS, CANCER, VIRGO, LIBRA, PISCES = 0, 1, 3, 5, 6, 11
DEATH = swe.julday(1988, 4, 6, 12.0)


@pytest.fixture(scope="module")
def chart22():
    record = book_chart(22)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 22", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def signs(chart22):
    return {int(g): int(chart22.positions[int(g)].longitude // 30) for g in GRAHAS}


def test_the_chart_recomputes(chart22, signs):
    """Every body agrees to within an arcminute except the Sun, which is out
    by 1.00' — the book prints to the arcminute, so that is its own precision
    rather than a disagreement. The bound is set just above it deliberately,
    so a real drift would still fail.
    """
    from hora.charts.book import chart, longitudes
    from hora.core.const import RASI_ABBR

    printed = longitudes(22)
    assert abs(chart22.lagna_longitude - printed["Asc"]) < 1.0 / 60
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        error = abs(chart22.positions[int(graha)].longitude - printed[body]) * 60
        assert error <= 1.01, f"{body} is {error:.2f}' out"
        assert RASI_ABBR[signs[int(graha)]] == chart(22)["drawn"][body], body

    # The Sun is the worst of them, and only just.
    sun = abs(chart22.positions[int(Graha.SUN)].longitude - printed["Sun"]) * 60
    assert 0.9 < sun <= 1.01


def test_the_two_marakas_the_example_names(chart22, signs):
    """"Jupiter is the 7th lord here and he is exalted... Venus is 2nd lord in
    2nd and he can kill too."

    Jupiter's exaltation is unambiguous here, unlike D-52's Moon: Cancer is
    his exaltation sign and his moolatrikona is Sagittarius, so no degree
    boundary is in play.
    """
    lagna = int(chart22.lagna_longitude // 30)
    assert lagna == VIRGO
    sthanas = maraka_sthanas(lagna)

    assert sthanas[7] == PISCES
    assert int(RASI_LORD[PISCES]) == int(Graha.JUPITER)
    assert sign_dignity(int(Graha.JUPITER),
                        chart22.positions[int(Graha.JUPITER)].longitude) == "exalted"

    assert sthanas[2] == LIBRA
    assert int(RASI_LORD[LIBRA]) == int(Graha.VENUS)
    assert signs[int(Graha.VENUS)] == LIBRA          # 2nd lord in the 2nd


def test_the_moons_pada_decides_the_fourth_stars_sign(chart22):
    """"Moon is in the 1st quarter of Bharani constellation. The 4th
    constellation is Mrigasira. Because the 1st quarter of Mrigasira is in
    Taurus, we should take Taurus as the sign of 4th star."

    Mrigasira begins in Taurus and ends in Gemini, so without the pada rule
    the sign is undetermined. The Moon's own quarter picks it.
    """
    moon = chart22.positions[int(Graha.MOON)].longitude
    star = int(moon // NAKSHATRA_SPAN)
    pada = int((moon - star * NAKSHATRA_SPAN) / (NAKSHATRA_SPAN / 4)) + 1
    assert pada == 1

    candidates = {v.star: v for v in variation_candidates(moon, "longevity")}
    assert candidates[1].nakshatra_name == "Bharani"
    assert candidates[1].rasi == ARIES

    fourth = candidates[4]
    assert fourth.nakshatra_name == "Mrigashira"
    assert fourth.spans_two_signs is True
    assert fourth.rasi == TAURUS
    assert "pada 1" in fourth.reason

    eighth = candidates[8]
    assert eighth.nakshatra_name == "Ashlesha"
    assert eighth.rasi == CANCER
    assert eighth.spans_two_signs is False


def test_the_maraka_criterion_picks_taurus_over_cancer(signs):
    """"Cancer contains 7th lord Jupiter, a maraka. However, it is not
    aspected by 2nd lord. Taurus, on the other hand, has the rasi aspect of
    both Jupiter and Venus. Aspect of marakas makes a sign stronger."

    The comparison counts maraka *aspects*, not occupancy — Cancer holds a
    maraka and still loses. §16.5.2 gave the criterion without applying it;
    this is the only place in the chapter where it is worked.
    """
    jupiter, venus = signs[int(Graha.JUPITER)], signs[int(Graha.VENUS)]
    assert jupiter == CANCER                        # Cancer contains a maraka
    assert CANCER not in rasi_drishti(venus)        # but the 2nd lord misses it

    assert TAURUS in rasi_drishti(jupiter)
    assert TAURUS in rasi_drishti(venus)            # both marakas aspect Taurus


def test_the_fourth_star_gives_mars_and_the_book_s_pair_at_death(chart22):
    """"First dasa belongs to Mars and Jupiter-Venus antardasa was running at
    death. Both the planets are marakas.\""""
    moon = chart22.positions[int(Graha.MOON)].longitude
    lord, _balance = balance_at_birth(V, moon, start_star=4)
    assert lord == int(Graha.MARS)

    for year_length in (DashaYearLength.SAVANA, DashaYearLength.SIDEREAL):
        periods = compute_nakshatra_dasha(
            V, moon, chart22.instant.jd_ut, year_length,
            levels=2, cycles=1, start_star=4)
        chain = [p.lord for p in find_running(periods, DEATH)]
        assert chain == [int(Graha.JUPITER), int(Graha.VENUS)]


def test_the_moons_own_star_would_have_named_a_different_pair(chart22):
    """Why the variation is not decoration: the plain reckoning gives Venus as
    the first dasa and Moon-Venus at death, neither of which the example
    could have explained by marakas."""
    moon = chart22.positions[int(Graha.MOON)].longitude
    lord, _balance = balance_at_birth(V, moon, start_star=1)
    assert lord == int(Graha.VENUS)

    periods = compute_nakshatra_dasha(
        V, moon, chart22.instant.jd_ut, DashaYearLength.SAVANA,
        levels=2, cycles=1, start_star=1)
    chain = [p.lord for p in find_running(periods, DEATH)]
    assert chain == [int(Graha.MOON), int(Graha.VENUS)]
