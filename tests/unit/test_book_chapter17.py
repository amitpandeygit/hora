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
