"""Chapter 16 — Vimsottari dasa, sections 16.1 and 16.2.

Table 38 and the six computation steps. The chapter's controversy box picks
savana years for every calculation in the book, where our default is sidereal;
that divergence is OI-115 and is measured here rather than papered over.
"""
from __future__ import annotations

import pytest

from hora.core.const import GRAHA_NAMES, NAKSHATRA_SPAN, Graha
from hora.core.settings import DashaYearLength
from hora.dasha.base import balance_at_birth, compute_nakshatra_dasha, year_days
from hora.dasha.nakshatra.systems import VIMSHOTTARI as V

#: Table 38, as printed.
TABLE_38 = {
    "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16,
    "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20,
}


def test_table_38_lengths():
    ours = {GRAHA_NAMES[g]: y for g, y in zip(V.order, V.years)}
    assert ours == TABLE_38


def test_vimsottari_means_120():
    """"the sum of *all* dasas is 120 years", and the name says so."""
    assert sum(V.years) == 120
    assert sum(TABLE_38.values()) == 120


def test_the_order_cycles_back_to_the_first_entry():
    """§16.2: "let us say that the first dasa is of Jupiter. Then the order of
    dasas will be Jupiter, Saturn, Mercury, Ketu, Venus, Sun (go back), Moon,
    Mars and Rahu.\""""
    start = list(V.order).index(int(Graha.JUPITER))
    cycle = [GRAHA_NAMES[V.order[(start + k) % 9]] for k in range(9)]
    assert cycle == ["Jupiter", "Saturn", "Mercury", "Ketu", "Venus",
                     "Sun", "Moon", "Mars", "Rahu"]


def test_step_3s_constellation_length():
    """"[NOTE: Length of each constellation is 13 deg 20'.]\""""
    assert NAKSHATRA_SPAN == pytest.approx(13 + 20 / 60)


@pytest.mark.parametrize("fraction", [0.0, 0.25, 0.5, 0.75])
def test_steps_4_and_6_give_the_lord_and_the_unspent_part(fraction):
    """Step (4) takes the constellation's lord; step (6) multiplies that dasa's
    length by the part still to be traversed. Ashwini is Ketu's, 7 years."""
    lord, balance = balance_at_birth(V, NAKSHATRA_SPAN * fraction)
    assert lord == int(Graha.KETU)
    assert balance == pytest.approx(7 * (1 - fraction))


def test_the_six_levels_the_chapter_names_all_exist():
    """MD, AD, PD, SD, PAD and DAD — mahadasa down to deha-antardasa."""
    periods = compute_nakshatra_dasha(
        V, 5.0, 2451545.0, DashaYearLength.SAVANA, levels=6, cycles=1)

    def depth(node, at=1):
        return at if not node.children else max(depth(c, at + 1) for c in node.children)

    assert depth(periods[0]) == 6
    assert len(periods) == 9                       # nine mahadasas
    assert len(periods[0].children) == 9           # "divided into 9 sub-periods"


# --------------------------------------------------------------------------
# The controversy box. See OI-115.
# --------------------------------------------------------------------------


def test_a_savana_year_is_360_days():
    assert year_days(DashaYearLength.SAVANA) == 360.0


def test_the_book_and_our_default_are_different_years():
    """The chapter uses savana throughout; we default to sidereal. Both are
    supported, and the gap is real rather than rounding."""
    savana = year_days(DashaYearLength.SAVANA)
    sidereal = year_days(DashaYearLength.SIDEREAL)
    assert sidereal - savana == pytest.approx(5.2564, abs=1e-3)


def test_the_two_year_lengths_move_mahadasa_boundaries_by_months():
    """Measured so OI-115 carries a number, not an impression.

    Over the first cycle the second mahadasa starts about ten weeks apart and
    the ninth about eighteen months apart, which is far more than a worked
    example's rounding could absorb.
    """
    from hora.charts.book import chart as book_chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = book_chart(12)
    chart = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 12", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    moon = chart.positions[int(Graha.MOON)].longitude

    def starts(mode):
        return [p.start_jd for p in compute_nakshatra_dasha(
            V, moon, chart.instant.jd_ut, mode, levels=1, cycles=1)]

    drift = [abs(a - b) for a, b in zip(starts(DashaYearLength.SIDEREAL),
                                        starts(DashaYearLength.SAVANA))]
    assert drift[1] == pytest.approx(71, abs=1)      # 2nd mahadasa
    assert drift[8] == pytest.approx(560, abs=1)     # 9th
