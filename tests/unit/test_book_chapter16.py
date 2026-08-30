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


# --------------------------------------------------------------------------
# Example 50 — the chapter's worked example. See D-50 and OI-115.
# --------------------------------------------------------------------------

#: "born at 5:50 am on 2000 April 28 (time zone: 4 hours west of GMT).
#: Moon is at 2°23' in Aq at the time of birth."
EX50_MOON = 10 * 30 + 2 + 23 / 60
EX50_BIRTH = (2000, 4, 28, 5 + 50 / 60)


def test_example_50_steps_1_and_2_place_the_moon_in_dhanishtha():
    """"the 3rd pada of Dhanishtha... starts at 23°20' in Cp and ends at
    6°40' in Aq", and the advancement in it is 2Aq23 - 23Cp20 = 9°3'."""
    start = 9 * 30 + 23 + 20 / 60                  # 23 Cp 20
    assert EX50_MOON - start == pytest.approx(9 + 3 / 60)
    assert start + NAKSHATRA_SPAN == pytest.approx(10 * 30 + 6 + 40 / 60)
    pada = int((EX50_MOON - start) / (NAKSHATRA_SPAN / 4)) + 1
    assert pada == 3


def test_example_50_step_3_fraction_yet_to_be_traversed():
    """"(13°20' - 9°3')/13°20' = 4°17'/13°20' = 257/800 = 0.32125\""""
    left = NAKSHATRA_SPAN - (9 + 3 / 60)
    assert left == pytest.approx(4 + 17 / 60)
    assert left / NAKSHATRA_SPAN == pytest.approx(257 / 800)
    assert left / NAKSHATRA_SPAN == pytest.approx(0.32125)


def test_example_50_steps_4_to_6_give_mars_and_its_balance():
    """"First dasa belongs to the lord of Dhanishtha. It is Mars." and
    "7 x 0.32125 = 2.24875 years\""""
    lord, balance = balance_at_birth(V, EX50_MOON)
    assert lord == int(Graha.MARS)
    assert balance == pytest.approx(2.24875)


def test_example_50_step_5_sequence_from_mars():
    """"Mars (7), Rahu (18), Jupiter (16), Saturn (19), Mercury (17),
    Ketu (7), Venus (20), Sun (6), Moon (10)\""""
    start = list(V.order).index(int(Graha.MARS))
    got = [(GRAHA_NAMES[V.order[(start + k) % 9]], V.years[(start + k) % 9])
           for k in range(9)]
    assert got == [("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19),
                   ("Mercury", 17), ("Ketu", 7), ("Venus", 20), ("Sun", 6),
                   ("Moon", 10)]


def test_example_50s_own_breakdown_is_in_savana_units():
    """"2 years 2 months 29 days 33 ghatis", with a ghati 1/60 of a day.

    Only savana reads this way: 720 + 60 + 29 + 0.55 = 809.55 days, which is
    2.24875 x 360 exactly. The same balance in sidereal years is 821.4 days and
    cannot be written as 2y 2m 29d in any month length the chapter uses.
    """
    days = 2.24875 * 360
    assert days == pytest.approx(2 * 360 + 2 * 30 + 29 + 33 / 60)
    assert days == pytest.approx(809.55)


def test_example_50_end_date_is_one_day_after_the_printed_one():
    """See D-50. The time of day matches; the day count does not.

    The balance is what remains of Mars dasa at birth, so it runs forward from
    birth: 809.55 days from 5:50 am on 2000 April 28 is 2002 July 16, 19:02.
    The example prints "about 7 pm on 2002 July 15", which is 808.55 days.
    """
    import swisseph as swe

    birth_jd = swe.julday(*EX50_BIRTH)
    year, month, day, hour = swe.revjul(birth_jd + 2.24875 * 360)
    assert (year, month, day) == (2002, 7, 16)
    assert int(hour) == 19                                   # the book's "7 pm"

    printed_jd = swe.julday(2002, 7, 15, 19.0)
    assert birth_jd + 2.24875 * 360 - printed_jd == pytest.approx(1.0, abs=0.01)


def test_example_50_rules_out_sidereal_years():
    """Under our default the same balance lands thirteen days later, so this
    example is evidence for savana rather than a reason to doubt it."""
    import swisseph as swe

    days = 2.24875 * year_days(DashaYearLength.SIDEREAL)
    year, month, day, _hour = swe.revjul(swe.julday(*EX50_BIRTH) + days)
    assert (year, month, day) == (2002, 7, 28)


# --------------------------------------------------------------------------
# §16.3 Antardasa Computation
# --------------------------------------------------------------------------


def _example_50_tree(levels=2):
    import swisseph as swe

    return compute_nakshatra_dasha(
        V, EX50_MOON, swe.julday(*EX50_BIRTH), DashaYearLength.SAVANA,
        levels=levels, cycles=1)


def test_antardasas_start_from_the_mahadasa_lord_and_keep_the_dasa_order():
    """"First antardasa will belong to the same planet and antardasas go in
    the same sequence as dasas." Checked for every mahadasa, not just Venus."""
    for mahadasa in _example_50_tree():
        assert mahadasa.children[0].lord == mahadasa.lord
        start = list(V.order).index(mahadasa.lord)
        expected = [V.order[(start + k) % 9] for k in range(9)]
        assert [ad.lord for ad in mahadasa.children] == expected


def test_the_venus_antardasa_lengths_the_section_prints():
    """"20x20/120 years = 3 years and 4 months... 20x6/120 years = 1 year...
    20x10/120 years = 1 year and 8 months... 20x7/120 years = 1 year and 2
    months.\""""
    venus = next(p for p in _example_50_tree() if p.lord == int(Graha.VENUS))
    years = {GRAHA_NAMES[ad.lord]: (ad.end_jd - ad.start_jd) / 360
             for ad in venus.children}
    assert years["Venus"] == pytest.approx(20 * 20 / 120)     # 3y 4m
    assert years["Sun"] == pytest.approx(20 * 6 / 120)        # 1y
    assert years["Moon"] == pytest.approx(20 * 10 / 120)      # 1y 8m
    assert years["Mars"] == pytest.approx(20 * 7 / 120)       # 1y 2m


def test_the_nine_antardasas_exhaust_their_mahadasa():
    """"The complete length of the mahadasa is ditributed among antardasas in
    the ratio of mahadasa years of planets." Nothing may be lost or invented."""
    for mahadasa in _example_50_tree():
        total = sum(ad.end_jd - ad.start_jd for ad in mahadasa.children)
        assert total == pytest.approx(mahadasa.end_jd - mahadasa.start_jd)


def test_the_first_dasa_divides_its_whole_length_not_the_birth_remainder():
    """The section's one real trap.

    "In the case of the first dasa, we don't divide the remainder at birth
    (2.24875 years of Mars dasa remainder...) into 9 antardasas. Instead, we
    divide the complete duration of the first dasa (7 years of Mars dasa...)
    into 9 antardasas. So a few antardasas may be over before birth."

    Dividing the remainder instead would give a Mars antardasa of
    2.24875 x 7/120 = 0.131 years rather than 7 x 7/120 = 0.408, and would put
    every antardasa after birth.
    """
    import swisseph as swe

    birth_jd = swe.julday(*EX50_BIRTH)
    mars = _example_50_tree()[0]
    assert mars.lord == int(Graha.MARS)

    assert (mars.end_jd - mars.start_jd) / 360 == pytest.approx(7.0)
    assert (birth_jd - mars.start_jd) / 360 == pytest.approx(7 - 2.24875)
    assert (mars.end_jd - birth_jd) / 360 == pytest.approx(2.24875)

    first = mars.children[0]
    assert (first.end_jd - first.start_jd) / 360 == pytest.approx(7 * 7 / 120)

    before = [ad for ad in mars.children if ad.end_jd <= birth_jd]
    assert len(before) == 5, "five antardasas are over before this native's birth"


def test_the_same_proportional_rule_recurses_into_pratyantardasas():
    """"We use the same procedure to divide each antardasa into 9
    pratyantardasas, each pratyantardasa into 9 sookshma dasas and so on.\""""
    venus = next(p for p in _example_50_tree(levels=3) if p.lord == int(Graha.VENUS))
    sun_ad = next(ad for ad in venus.children if ad.lord == int(Graha.SUN))
    assert sun_ad.children[0].lord == int(Graha.SUN)

    span = sun_ad.end_jd - sun_ad.start_jd
    for pd in sun_ad.children:
        share = V.years[list(V.order).index(pd.lord)] / 120
        assert (pd.end_jd - pd.start_jd) == pytest.approx(span * share)
