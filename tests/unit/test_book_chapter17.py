"""Chapter 17 — Ashtottari dasa, sections 17.1 and 17.2.1.

Table 39 is the whole chapter. Ashtottari does not lay equal spans over its
lords the way Vimsottari does, and it does not begin at Ashwini, so reusing
Vimsottari's machinery gets 24 of 27 nakshatras wrong. This pins the table and
the arc arithmetic that follows from it.
"""
from __future__ import annotations

import pytest

from hora.core.const import (
    ASHTOTTARI_ARCS,
    GRAHA_NAMES,
    NAKSHATRA_NAMES,
    NAKSHATRA_SPAN,
    Graha,
)
from hora.core.settings import DashaYearLength
from hora.dasha.base import balance_at_birth, compute_nakshatra_dasha
from hora.dasha.nakshatra.systems import ASHTOTTARI as A


def _table_lord(longitude: float) -> str:
    """Table 39's planet for a longitude, read straight off the printed arcs."""
    lon = longitude % 360.0
    for i, arc in enumerate(ASHTOTTARI_ARCS):
        start = arc["start"]
        end = ASHTOTTARI_ARCS[(i + 1) % len(ASHTOTTARI_ARCS)]["start"]
        inside = (start <= lon < end) if start < end else (lon >= start or lon < end)
        if inside:
            return str(arc["planet"])
    raise AssertionError(f"no arc holds {longitude}")


def test_table_39_closes_on_all_three_totals():
    """360 degrees, 27 nakshatras, 108 years. Any transcription slip in the
    arcs shows up in at least one of them."""
    assert sum(a["length"] for a in ASHTOTTARI_ARCS) == pytest.approx(360.0)
    assert sum(a["nakshatras"] for a in ASHTOTTARI_ARCS) == 27
    assert sum(a["years"] for a in ASHTOTTARI_ARCS) == 108


def test_ashtottari_means_one_hundred_and_eight():
    """§17.1: "the sum of all dasas is 108 years"."""
    assert sum(A.years) == 108


def test_the_arcs_are_unequal_which_is_the_point():
    """"Each planet covers an arc of either 53°20' (4 nakshatras) or 40°0'
    (3 nakshatras)." Three lords take the wider arc, five the narrower."""
    wide = [a for a in ASHTOTTARI_ARCS if a["nakshatras"] == 4]
    narrow = [a for a in ASHTOTTARI_ARCS if a["nakshatras"] == 3]
    assert [a["planet"] for a in wide] == ["Sun", "Mars", "Rahu"]
    assert len(narrow) == 5
    for arc in wide:
        assert arc["length"] == pytest.approx(53 + 20 / 60)
    for arc in narrow:
        assert arc["length"] == pytest.approx(40.0)


def test_the_cycle_begins_at_ardra_not_ashwini():
    """The table's first row starts at 66°40', which is Ardra's own start.

    This is what parity question 7 flagged as unverified, and it is why the
    plain modulo rule cannot be used: under it Ashwini would begin the Sun's
    dasa, where Table 39 gives Ashwini to Rahu.
    """
    assert ASHTOTTARI_ARCS[0]["start"] == pytest.approx(66 + 40 / 60)
    assert ASHTOTTARI_ARCS[0]["planet"] == "Sun"
    assert NAKSHATRA_NAMES[int((66 + 40 / 60) / NAKSHATRA_SPAN)] == "Ardra"

    ashwini_lord, _balance = balance_at_birth(A, 1.0)
    assert ashwini_lord == int(Graha.RAHU)


def test_rahus_arc_wraps_zero():
    """"333°20' – 386°40' (333°20' – 26°40')" — the only row that crosses the
    start of the zodiac, and it covers Aswini and Bharani on the far side."""
    rahu = next(a for a in ASHTOTTARI_ARCS if a["planet"] == "Rahu")
    assert rahu["start"] == pytest.approx(333 + 20 / 60)
    for longitude in (334.0, 359.9, 0.1, 20.0):
        assert _table_lord(longitude) == "Rahu"
        assert balance_at_birth(A, longitude)[0] == int(Graha.RAHU)


@pytest.mark.parametrize("nakshatra", range(27))
def test_every_nakshatra_maps_to_table_39s_lord(nakshatra):
    """All 27, not a sample. The previous implementation got 24 of them wrong
    by reusing Vimsottari's equal-span rule."""
    longitude = nakshatra * NAKSHATRA_SPAN + 1.0
    lord, _balance = balance_at_birth(A, longitude)
    assert GRAHA_NAMES[lord] == _table_lord(longitude)


@pytest.mark.parametrize("arc", ASHTOTTARI_ARCS)
def test_the_whole_dasa_remains_at_each_arcs_start(arc):
    """§17.2.1: "The fraction of the arc that is yet to be traversed by natal
    Moon is calculated and the same fraction of the dasa length of the first
    dasa lord is left at birth." At the start of an arc, all of it is left."""
    lord, balance = balance_at_birth(A, arc["start"] + 1e-6)
    assert GRAHA_NAMES[lord] == arc["planet"]
    assert balance == pytest.approx(arc["years"], abs=1e-3)


@pytest.mark.parametrize("arc", ASHTOTTARI_ARCS)
def test_the_balance_is_measured_over_the_arc_not_the_nakshatra(arc):
    """Halfway through a lord's arc leaves half its dasa — which for the wide
    arcs is two nakshatras in, not half of one."""
    midpoint = (arc["start"] + arc["length"] / 2) % 360.0
    lord, balance = balance_at_birth(A, midpoint)
    assert GRAHA_NAMES[lord] == arc["planet"]
    assert balance == pytest.approx(arc["years"] / 2, rel=1e-6)


def test_ketu_has_no_dasa():
    """§17.1: "only chara karakas, i.e. Rahu and the seven planets, have dasas
    under the Ashtottari dasa scheme"."""
    assert len(A.order) == 8
    assert int(Graha.KETU) not in [int(g) for g in A.order]
    assert int(Graha.RAHU) in [int(g) for g in A.order]


def test_the_order_follows_the_table_and_returns_to_the_sun():
    """"After Venus, we come back to Sun at the beginning of the table.\""""
    assert [GRAHA_NAMES[g] for g in A.order] == [
        a["planet"] for a in ASHTOTTARI_ARCS]

    periods = compute_nakshatra_dasha(
        A, 70.0, 2451545.0, DashaYearLength.SAVANA, levels=1, cycles=2)
    names = [GRAHA_NAMES[p.lord] for p in periods]
    assert names[:8] == [a["planet"] for a in ASHTOTTARI_ARCS]
    assert names[8] == "Sun"                       # the cycle comes round


def test_the_star_variations_do_not_apply_to_ashtottari():
    """§16.4.1's 4th/5th/8th-star variations assume equal spans. Refusing them
    is better than silently returning a lord from the wrong arc."""
    with pytest.raises(ValueError, match="unequal arcs"):
        balance_at_birth(A, 70.0, start_star=5)
    with pytest.raises(ValueError, match="unequal arcs"):
        compute_nakshatra_dasha(A, 70.0, 2451545.0, DashaYearLength.SAVANA,
                                start_star=4)


# --------------------------------------------------------------------------
# Example 59, and the NOTE on Rahu's wrapping arc
# --------------------------------------------------------------------------


def test_example_59_moon_at_24_leo():
    """"Suppose Moon is at 24° in Leo... 144° is between 120°0' and 160°0'.
    So it is in the 2nd arc of Table 39, which is ruled by Moon... the part of
    the arc that is yet to be traversed by Moon is (160°0' - 144°0') = 16°. As
    a fraction of the arc length (40°), this is 16°/40° = 0.4. The same
    fraction of the full dasa length of Moon is 15 x 0.4 = 6 years."

    Every figure the example prints, including the fraction.
    """
    from hora.dasha.base import _arc_index

    longitude = 24.0 + 120.0
    assert longitude == 144.0

    index, remaining = _arc_index(A, longitude)
    assert index == 1                                  # the 2nd arc
    assert ASHTOTTARI_ARCS[index]["planet"] == "Moon"
    assert ASHTOTTARI_ARCS[index]["length"] == pytest.approx(40.0)
    assert remaining == pytest.approx(16.0 / 40.0)
    assert remaining == pytest.approx(0.4)

    lord, balance = balance_at_birth(A, longitude)
    assert lord == int(Graha.MOON)
    assert balance == pytest.approx(6.0)


def test_example_59_continues_moon_mars_mercury_saturn():
    """"The native will run Moon dasa of 6 years from his birth. Then 8 years
    of Mars dasa will run. Then 17 years of Mercury dasa will run. Then 10
    years of Saturn dasa will run.\""""
    import swisseph as swe

    birth = swe.julday(2000, 1, 1, 12.0)
    periods = compute_nakshatra_dasha(
        A, 144.0, birth, DashaYearLength.SAVANA, levels=1, cycles=1)

    assert [GRAHA_NAMES[p.lord] for p in periods[:4]] == [
        "Moon", "Mars", "Mercury", "Saturn"]
    assert [(p.end_jd - p.start_jd) / 360 for p in periods[1:4]] == [
        pytest.approx(8.0), pytest.approx(17.0), pytest.approx(10.0)]
    # The first is truncated: 6 of its 15 years remain at birth.
    assert (periods[0].end_jd - periods[0].start_jd) / 360 == pytest.approx(15.0)
    assert (periods[0].end_jd - birth) / 360 == pytest.approx(6.0)


@pytest.mark.parametrize(
    "longitude,degrees_left,label",
    [
        (10.0, 16 + 40 / 60, "10 deg Aries, past the wrap"),
        (350.0, 36 + 40 / 60, "20 deg Pisces, before it"),
    ],
)
def test_the_note_on_rahus_wrapping_arc(longitude, degrees_left, label):
    """"One has to be careful with the calculation if the first dasa is Rahu
    dasa... we should use either 26°40' or 386°40' based on Moon's longitude."

    The note exists because the arc's end is numerically below its start. Our
    arithmetic takes the difference modulo 360 instead of choosing between two
    written forms of the same point, which gets both sides right without the
    bookkeeping the note describes.
    """
    from hora.dasha.base import _arc_index

    index, remaining = _arc_index(A, longitude)
    assert ASHTOTTARI_ARCS[index]["planet"] == "Rahu"

    span = ASHTOTTARI_ARCS[index]["length"]
    assert remaining * span == pytest.approx(degrees_left, abs=1e-6)

    lord, balance = balance_at_birth(A, longitude)
    assert lord == int(Graha.RAHU)
    assert balance == pytest.approx(12.0 * degrees_left / span)


def test_the_wrap_is_continuous_across_zero():
    """A Moon a hair either side of 0° must give balances a hair apart, not a
    jump — the failure the note is warning about."""
    _lord, before = balance_at_birth(A, 359.999)
    _lord, after = balance_at_birth(A, 0.001)
    assert before > after
    assert before - after == pytest.approx(0.0, abs=1e-3)


# --------------------------------------------------------------------------
# §17.2.2 Antardasas
# --------------------------------------------------------------------------


def _antardasas(lord_name: str) -> list[str]:
    import swisseph as swe

    periods = compute_nakshatra_dasha(
        A, 300.0, swe.julday(2000, 1, 1, 12.0), DashaYearLength.SAVANA,
        levels=2, cycles=1)
    period = next(p for p in periods if GRAHA_NAMES[p.lord] == lord_name)
    return [GRAHA_NAMES[c.lord] for c in period.children]


@pytest.mark.parametrize(
    "lord,expected",
    [
        ("Jupiter", ["Rahu", "Venus", "Sun", "Moon", "Mars", "Mercury",
                     "Saturn", "Jupiter"]),
        ("Moon", ["Mars", "Mercury", "Saturn", "Jupiter", "Rahu", "Venus",
                  "Sun", "Moon"]),
    ],
)
def test_the_two_antardasa_runs_the_section_prints(lord, expected):
    """"antardasas in Jupiter dasa go as: Rahu, Venus, Sun, Moon, Mars,
    Mercury, Saturn and Jupiter. Antardasas in Moon dasa go as: Mars, Mercury,
    Saturn, Jupiter, Rahu, Venus, Sun and Moon.\""""
    assert _antardasas(lord) == expected


def test_the_first_antardasa_is_the_planet_after_the_dasa_lord():
    """"The first antardasa belongs to the planet that comes in the table
    *after* the dasa lord... and the last antardasa belongs to dasa lord."

    This is where Ashtottari parts company with Vimsottari, whose §16.3 rule
    is that the first antardasa belongs to the dasa lord himself. Getting it
    wrong leaves the right set of antardasas in the wrong time slots.
    """
    names = [GRAHA_NAMES[g] for g in A.order]
    for i, lord in enumerate(names):
        run = _antardasas(lord)
        assert run[0] == names[(i + 1) % len(names)]
        assert run[-1] == lord
        assert set(run) == set(names)


def test_vimsottari_still_begins_on_its_own_lord():
    """The fix must not leak into the system that does it the other way."""
    import swisseph as swe

    from hora.dasha.nakshatra.systems import VIMSHOTTARI

    periods = compute_nakshatra_dasha(
        VIMSHOTTARI, 5.0, swe.julday(2000, 1, 1, 12.0),
        DashaYearLength.SAVANA, levels=2, cycles=1)
    assert periods[0].children[0].lord == periods[0].lord


def test_the_antardasa_lengths_the_section_prints():
    """"Sun dasa is of 6 years. Moon antardasa in Sun dasa is of 6 x 15/108 =
    0.8333 year = 10 months. Mars antardasa ... 0.4444 year = 5 months 10
    days. Mercury antardasa ... 0.9444 years = 11 months 10 days.\""""
    import swisseph as swe

    periods = compute_nakshatra_dasha(
        A, 70.0, swe.julday(2000, 1, 1, 12.0), DashaYearLength.SAVANA,
        levels=2, cycles=1)
    sun = next(p for p in periods if GRAHA_NAMES[p.lord] == "Sun")
    assert (sun.end_jd - sun.start_jd) / 360 == pytest.approx(6.0)

    years = {GRAHA_NAMES[c.lord]: (c.end_jd - c.start_jd) / 360
             for c in sun.children}
    assert years["Moon"] == pytest.approx(6 * 15 / 108)
    assert years["Mars"] == pytest.approx(6 * 8 / 108)
    assert years["Mercury"] == pytest.approx(6 * 17 / 108)
    assert sum(years.values()) == pytest.approx(6.0)


def test_the_antardasas_divide_in_the_ratio_of_the_dasa_lengths():
    """"The length of a dasa is divided into eight antardasas in the ratio of
    the dasa lengths." Checked for every dasa, not just the Sun's."""
    import swisseph as swe

    periods = compute_nakshatra_dasha(
        A, 70.0, swe.julday(2000, 1, 1, 12.0), DashaYearLength.SAVANA,
        levels=2, cycles=1)
    for period in periods:
        span = period.end_jd - period.start_jd
        for child in period.children:
            share = A.years[list(A.order).index(child.lord)] / 108
            assert (child.end_jd - child.start_jd) == pytest.approx(span * share)


# --------------------------------------------------------------------------
# §17.2.3 Application
# --------------------------------------------------------------------------


def test_the_three_applicability_views_are_recorded_without_choosing():
    """§17.2.3 lists three views and picks none, and §17.1 calls the
    conditions "highly controversial". Nothing gates on them."""
    from hora.core.const import (
        ASHTOTTARI_APPLICABILITY_VIEWS,
        ASHTOTTARI_IS_CONDITIONAL,
    )

    assert len(ASHTOTTARI_APPLICABILITY_VIEWS) == 3
    assert [v["view"] for v in ASHTOTTARI_APPLICABILITY_VIEWS] == [1, 2, 3]
    assert "highly controversial" in ASHTOTTARI_IS_CONDITIONAL

    # View 1 is vacuous; the other two name what a chart must supply.
    first, second, third = ASHTOTTARI_APPLICABILITY_VIEWS
    assert first["computable"] is False
    assert second["computable"] and second["needs"]
    assert third["computable"] and third["needs"]


def test_the_two_computable_views_disagree_by_construction():
    """View 2 turns on Rahu's placement, view 3 on the birth's time and
    paksha. They share no input, so they cannot be reconciled — which is why
    the section leaves the choice to the reader.
    """
    from hora.core.const import ASHTOTTARI_APPLICABILITY_VIEWS

    _first, second, third = ASHTOTTARI_APPLICABILITY_VIEWS
    assert set(second["needs"]).isdisjoint(third["needs"])


# --------------------------------------------------------------------------
# §17.3 Examples 60 and 62. Example 61 needs Chart 61 — see OI-119.
# --------------------------------------------------------------------------


def _chart(number):
    from hora.charts.book import chart as book_chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = book_chart(number)
    return compute_chart(
        from_local(**record["birth_data"]),
        Place(name=f"Chart {number}", **record["place"]),
        Settings(node_type=NodeType.MEAN))


def test_example_60_ashtottari_gives_rahu_mercury_at_ramans_death():
    """"Rahu-Mercury antardasa was running at the time of his death."

    Example 58 read the same death through Vimsottari from the 8th star and
    got Mercury-Rahu. The book calls it significant that the same two planets
    appear in both, and they do — with their roles swapped.
    """
    import swisseph as swe

    from hora.dasha.base import find_running
    from hora.dasha.nakshatra.systems import VIMSHOTTARI

    chart = _chart(23)
    moon = chart.positions[int(Graha.MOON)].longitude
    death = swe.julday(1998, 12, 20, 12.0)

    ashtottari = compute_nakshatra_dasha(
        A, moon, chart.instant.jd_ut, DashaYearLength.SAVANA, levels=2, cycles=1)
    assert [GRAHA_NAMES[p.lord] for p in find_running(ashtottari, death)] == [
        "Rahu", "Mercury"]

    vimsottari = compute_nakshatra_dasha(
        VIMSHOTTARI, moon, chart.instant.jd_ut, DashaYearLength.SAVANA,
        levels=2, cycles=1, start_star=8)
    assert [GRAHA_NAMES[p.lord] for p in find_running(vimsottari, death)] == [
        "Mercury", "Rahu"]


def test_example_60_needs_savana_years():
    """A fifth chart where the book's answer only comes out under savana; the
    sidereal default gives Rahu-Moon. See OI-115."""
    import swisseph as swe

    from hora.dasha.base import find_running

    chart = _chart(23)
    periods = compute_nakshatra_dasha(
        A, chart.positions[int(Graha.MOON)].longitude, chart.instant.jd_ut,
        DashaYearLength.SIDEREAL, levels=2, cycles=1)
    running = [GRAHA_NAMES[p.lord]
               for p in find_running(periods, swe.julday(1998, 12, 20, 12.0))]
    assert running != ["Rahu", "Mercury"]


def test_example_62_mercury_dasa_spans_1981_to_1997():
    """"Mercury dasa ran during 1981-1997."

    Savana puts it December 1980 to October 1997, so the printed range is its
    start rounded up by a month. Sidereal runs to November 1998 and misses the
    end by a year.
    """
    import swisseph as swe

    chart = _chart(6)
    moon = chart.positions[int(Graha.MOON)].longitude

    def span(year_length):
        periods = compute_nakshatra_dasha(
            A, moon, chart.instant.jd_ut, year_length, levels=1, cycles=1)
        mercury = next(p for p in periods if p.lord == int(Graha.MERCURY))
        return swe.revjul(mercury.start_jd)[:2], swe.revjul(mercury.end_jd)[:2]

    assert span(DashaYearLength.SAVANA) == ((1980, 12), (1997, 10))
    assert span(DashaYearLength.SIDEREAL)[1][0] == 1998


def test_example_62_mercury_is_lagna_lord_in_his_own_sign():
    """"Mercury is lagna lord and he occupies an own sign.\""""
    from hora.core.const import RASI_LORD

    chart = _chart(6)
    lagna = int(chart.lagna_longitude // 30)
    mercury = int(chart.positions[int(Graha.MERCURY)].longitude // 30)
    assert int(RASI_LORD[lagna]) == int(Graha.MERCURY)
    assert int(RASI_LORD[mercury]) == int(Graha.MERCURY)


def test_example_62_the_vipareeta_raja_yoga_pair():
    """"a powerful Vipareeta Raja yoga between 3rd and 8th lord Mars and 12th
    lord Sun, who are within a 17' from each other... Mercury is the dispositor
    of Mars and Sun and joins them in his own rasi.\""""
    from hora.core.const import RASI_LORD

    chart = _chart(6)
    lagna = int(chart.lagna_longitude // 30)
    signs = {g: int(chart.positions[int(g)].longitude // 30)
             for g in (Graha.SUN, Graha.MARS, Graha.MERCURY)}

    assert int(RASI_LORD[(lagna + 2) % 12]) == int(Graha.MARS)     # 3rd lord
    assert int(RASI_LORD[(lagna + 7) % 12]) == int(Graha.MARS)     # and 8th
    assert int(RASI_LORD[(lagna + 11) % 12]) == int(Graha.SUN)     # 12th lord

    separation = abs(chart.positions[int(Graha.MARS)].longitude
                     - chart.positions[int(Graha.SUN)].longitude) * 60
    assert separation < 17.0

    # All three share Gemini, which Mercury owns.
    assert signs[Graha.MARS] == signs[Graha.SUN] == signs[Graha.MERCURY]
    assert int(RASI_LORD[signs[Graha.MERCURY]]) == int(Graha.MERCURY)


def test_example_62_the_two_ashtakavarga_figures():
    """"He has 7 rekhas in BAV and his rasi Gemini has 34 rekhas in SAV."""
    from hora.charts.ashtakavarga import bhinnashtakavarga, sarvashtakavarga
    from hora.charts.book import graha_signs
    from hora.charts.book import lagna as book_lagna

    signs = graha_signs(6)
    reference = {
        "Sun": signs[int(Graha.SUN)], "Moon": signs[int(Graha.MOON)],
        "Mars": signs[int(Graha.MARS)], "Mercury": signs[int(Graha.MERCURY)],
        "Jupiter": signs[int(Graha.JUPITER)], "Venus": signs[int(Graha.VENUS)],
        "Saturn": signs[int(Graha.SATURN)], "Lagna": book_lagna(6),
    }
    gemini = 2
    assert bhinnashtakavarga("Mercury", reference).rekhas[gemini] == 7
    assert sarvashtakavarga(reference)["rekhas"][gemini] == 34


def test_example_62_calls_mercury_uttamaamsa_where_we_count_one_fewer():
    """See D-54. "Mercury is in Uttamamsa", which on the dasavarga scale is a
    count of three; we count two, from D1 and D9 both giving him his own sign.

    Pinned rather than hidden: everything else in the paragraph reproduces,
    so this is one figure out of several.
    """
    from hora.services.varga_service import amsabala

    chart = _chart(6)
    group = amsabala(chart.positions[int(Graha.MERCURY)].longitude,
                     int(Graha.MERCURY))["groups"]["dasavarga"]
    assert group["count"] == 2
    assert group["amsa"] == "Paarijaataamsa"
    assert [v["chart"] for v in group["strong_in"]] == ["D1", "D9"]


def test_the_caveat_travels_with_every_ashtottari_result():
    """Chapter 17 says its own warning applies with special force here, so it
    is attached to the response rather than left in a document. Vimsottari
    carries none, which keeps the field meaningful."""
    from fastapi.testclient import TestClient

    from hora.api.main import app
    from hora.core.const import ASHTOTTARI_CAVEAT

    client = TestClient(app)
    body = {"year": 1921, "month": 6, "day": 28, "hour": 12, "minute": 49,
            "utc_offset_hours": 5.283,
            "place": {"latitude": 18.43, "longitude": 79.15}, "levels": 1}

    ashtottari = client.post("/v1/dasha", json=body | {"system": "ashtottari"}).json()
    assert ashtottari["caveat"] == ASHTOTTARI_CAVEAT
    assert "applicability as well as application are controversial" in ASHTOTTARI_CAVEAT

    vimshottari = client.post("/v1/dasha", json=body | {"system": "vimshottari"}).json()
    assert vimshottari["caveat"] is None
