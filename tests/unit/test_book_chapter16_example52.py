"""Example 52 — Sanjay Rath's dasamsa, read as a phalita dasa (§16.6.1).

The chapter's first practical example, and the first that reads a chart rather
than computing a period. Everything it asserts is checked: the chart itself,
the D-10 it is drawn in, the arudha pada the reading turns on, both argalas,
the special lagna, the yoga, and the dasa dates.
"""
from __future__ import annotations

import pytest

from hora.charts.argala import argalas_on_sign, ketu_sign_of, occupants_from
from hora.charts.arudha import all_arudha_padas
from hora.charts.aspects import graha_aspects_sign, rasi_drishti
from hora.charts.book import chart as book_chart
from hora.charts.chart import Place, compute_chart
from hora.charts.colord import stronger
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    dasa_level,
    evaluate_one,
)
from hora.charts.vargas import d10_dasamsa
from hora.core.const import RASI_LORD, Graha
from hora.core.settings import DashaYearLength, NodeType, Settings
from hora.core.timeutil import from_local
from hora.dasha.base import balance_at_birth, compute_nakshatra_dasha
from hora.dasha.nakshatra.systems import VIMSHOTTARI as V

GRAHAS = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
          Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU)
VIRGO, CANCER, LEO = 5, 3, 4


@pytest.fixture(scope="module")
def chart17():
    record = book_chart(17)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 17", **record["place"]),
        Settings(node_type=NodeType.MEAN))


@pytest.fixture(scope="module")
def d10_signs(chart17):
    return {int(g): d10_dasamsa(chart17.positions[int(g)].longitude).sign
            for g in GRAHAS}


def test_the_printed_longitudes_are_the_rasi_chart_and_recompute(chart17):
    """The diagram is the D-10, so the printed positions must be the rasi —
    and they are, within an arcminute for every graha."""
    from hora.charts.book import longitudes

    printed = longitudes(17)
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        got = chart17.positions[int(graha)].longitude
        assert abs(got - printed[body]) < 1.0 / 60, body


def test_the_ascendant_is_sixteen_arcminutes_out(chart17):
    """About a minute of birth time, against a time printed to the minute.
    Recorded rather than hidden behind a loose tolerance, as with Chart 3."""
    from hora.charts.book import longitudes

    error = abs(chart17.lagna_longitude - longitudes(17)["Asc"]) * 60
    assert 15.0 < error < 17.0


def test_the_d10_reproduces_the_drawn_diagram(chart17, d10_signs):
    """All ten bodies, against the positions the chart is drawn in."""
    from hora.charts.book import divisional
    from hora.core.const import RASI_ABBR

    drawn = divisional(17, "D10")
    assert RASI_ABBR[d10_dasamsa(chart17.lagna_longitude).sign] == drawn["Asc"]
    for body, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        assert RASI_ABBR[d10_signs[int(graha)]] == drawn[body], body


def test_a3_is_in_virgo_in_the_dasamsa(chart17, d10_signs):
    """"A3 (arudha pada of 3rd house) shows the books authored by one. A3 is
    in Vi here."

    Reaching it needs §15.5.1 first: the D-10 has co-owned rasis, and the
    arudha engine refuses to guess a lord rather than picking one.
    """
    d10_lon = {int(g): d10_dasamsa(chart17.positions[int(g)].longitude).longitude
               for g in GRAHAS}
    strongest = {r: stronger(r, d10_lon, purpose="arudha").winner for r in (7, 10)}

    lagna10 = d10_dasamsa(chart17.lagna_longitude).sign
    padas = {p.house: p.sign for p in
             all_arudha_padas(lagna10, d10_signs, stronger_lord=strongest)}
    assert padas[3] == VIRGO                       # A3, and the reading's subject
    assert padas[1] == 7                           # AL in Scorpio, per the diagram


def test_venus_and_jupiter_give_argala_on_a3_from_the_eleventh(d10_signs):
    """"It has argalas from the 11th from it by Venus and Jupiter.\""""
    got = argalas_on_sign(VIRGO, occupants_from(d10_signs),
                          ketu_sign=ketu_sign_of(d10_signs))
    eleventh = next(a for a in got if a.house == 11)
    assert eleventh.sign == CANCER
    assert set(eleventh.grahas) == {int(Graha.VENUS), int(Graha.JUPITER)}
    assert eleventh.kind == "argala"


def test_mercury_gives_argala_on_a3_from_the_fourth(d10_signs):
    """"Mercury is the significator of writing and communication and he has
    argala on A3 from the 4th from it.\""""
    got = argalas_on_sign(VIRGO, occupants_from(d10_signs),
                          ketu_sign=ketu_sign_of(d10_signs))
    fourth = next(a for a in got if a.house == 4)
    assert fourth.grahas == (int(Graha.MERCURY),)
    assert fourth.kind == "argala"


def test_virgo_is_the_third_from_gl_in_the_dasamsa():
    """"In addition to containing A3, Virgo is the 3rd from GL." The diagram
    puts GL in Cancer, and our GL lands there too."""
    from hora.charts.book import divisional

    assert divisional(17, "D10")["GL"] == "Cn"
    assert (CANCER + 2) % 12 == VIRGO


def test_mercury_owns_virgo_and_aspects_it_by_rasi_drishti_only(d10_signs):
    """"Mercury owns and aspects it."

    Worth pinning which aspect is meant. Mercury sits in Sagittarius in the
    D-10, from where graha drishti reaches only the 7th, Gemini. The claim
    holds by rasi drishti — Sagittarius is dual and aspects Virgo — which is
    the same drishti the argala reading above uses.
    """
    assert int(RASI_LORD[VIRGO]) == int(Graha.MERCURY)

    mercury = d10_signs[int(Graha.MERCURY)]
    assert graha_aspects_sign(int(Graha.MERCURY), mercury, VIRGO) is False
    assert VIRGO in rasi_drishti(mercury)


def test_vesi_yoga_is_present_in_the_rasi_chart(chart17):
    """"In rasi chart, Mercury gives Vesi yoga being in the 2nd from Sun.\""""
    rasis = {int(g): int(chart17.positions[int(g)].longitude // 30) for g in GRAHAS}
    assert rasis[int(Graha.SUN)] == CANCER
    assert rasis[int(Graha.MERCURY)] == LEO

    verdict = evaluate_one("vesi", YogaInput(rasis=rasis))
    assert verdict.present is True
    assert "2nd from Sun" in verdict.reason


def test_vesi_being_a_ravi_yoga_shows_in_the_mahadasa():
    """"So his dasa should bring the results of Vesi yoga."

    §16.5.3 sends ravi yogas to the mahadasa, and this example says the
    results come in his dasa. The rule and the reading agree, which is the
    only place in the chapter where they can be checked against each other.
    """
    assert dasa_level("vesi") == "mahadasa"


def test_only_days_of_rahu_dasa_remained_at_birth(chart17):
    """"Just a few days of Rahu dasa were left at birth."

    The Moon is 99.8% through Shatabhisha, which is Rahu's, so 18 years leaves
    under a fortnight.
    """
    moon = chart17.positions[int(Graha.MOON)].longitude
    lord, balance = balance_at_birth(V, moon)
    assert lord == int(Graha.RAHU)
    assert 0 < balance * 360 < 20                  # savana days


@pytest.mark.parametrize("year_length", [DashaYearLength.SAVANA,
                                         DashaYearLength.SIDEREAL])
def test_mercury_dasa_began_in_1998_either_way(chart17, year_length):
    """"Mercury dasa has been running since 1998."

    Both year lengths land in 1998 — February under savana, August under
    sidereal — so this example does not discriminate for OI-115.
    """
    import swisseph as swe

    moon = chart17.positions[int(Graha.MOON)].longitude
    periods = compute_nakshatra_dasha(
        V, moon, chart17.instant.jd_ut, year_length, levels=1, cycles=1)
    mercury = next(p for p in periods if p.lord == int(Graha.MERCURY))
    assert swe.revjul(mercury.start_jd)[0] == 1998
