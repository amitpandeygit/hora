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


# --------------------------------------------------------------------------
# §16.4.1 Computation of Variations, and Example 51
# --------------------------------------------------------------------------


def test_the_three_variations_are_named_as_the_section_names_them():
    """"We can take the lord of the 4th, 5th or 8th constellation from Moon's
    constellation to start the first dasa. These 3 stars are called kshema,
    utpanna and adhana stars.\""""
    from hora.core.const import VIMSOTTARI_VARIATIONS

    by_star = {v["star"]: v["name"] for v in VIMSOTTARI_VARIATIONS}
    assert by_star[4] == "kshema"
    assert by_star[5] == "utpanna"
    assert by_star[8] == "adhana"
    assert by_star[1] == "Moon's own"


def test_example_51_stars_and_their_lords():
    """From Dhanishtha the 4th is Uttarabhadrapada (Saturn), the 5th Revathi
    (Mercury), the 8th Krittika (Sun). Counted inclusively."""
    from hora.core.const import NAKSHATRA_LORD, NAKSHATRA_NAMES

    moon_star = int(EX50_MOON // NAKSHATRA_SPAN)
    assert NAKSHATRA_NAMES[moon_star].startswith("Dhanish")
    for n, star, lord in ((4, "Uttara Bhadrapada", Graha.SATURN),
                          (5, "Revati", Graha.MERCURY),
                          (8, "Krittika", Graha.SUN)):
        idx = (moon_star + n - 1) % 27
        assert NAKSHATRA_NAMES[idx] == star
        assert int(NAKSHATRA_LORD[idx]) == int(lord)


@pytest.mark.parametrize(
    "star,lord,balance",
    [
        (1, Graha.MARS, 7 * 0.32125),          # 2.24875, Example 50
        (4, Graha.SATURN, 19 * 0.32125),       # 6.10375
        (5, Graha.MERCURY, 17 * 0.32125),      # 5.46125
        (8, Graha.SUN, 6 * 0.32125),           # 1.9275
    ],
)
def test_example_51_balances(star, lord, balance):
    """"Dasa lengths are the same as before, but the part of Saturn dasa left
    at birth is 19 x 0.32125 = 6.10375 years", and likewise for the others."""
    got_lord, got_balance = balance_at_birth(V, EX50_MOON, start_star=star)
    assert got_lord == int(lord)
    assert got_balance == pytest.approx(balance)


def test_the_fraction_never_moves_only_the_lord_does():
    """"We always compute the fraction left at birth in the first dasa based
    on the fraction of the constellation occupied by Moon."

    So every variation divides the same 0.32125 into a different planet's
    dasa length — which is the whole content of the rule.
    """
    for star in (1, 4, 5, 8):
        lord, balance = balance_at_birth(V, EX50_MOON, start_star=star)
        length = V.years[list(V.order).index(lord)]
        assert balance / length == pytest.approx(0.32125)


@pytest.mark.parametrize(
    "star,sequence",
    [
        (4, ["Saturn", "Mercury", "Ketu", "Venus"]),
        (5, ["Mercury", "Ketu", "Venus", "Sun"]),
        (8, ["Sun", "Moon", "Mars", "Rahu"]),
    ],
)
def test_example_51_sequences(star, sequence):
    """Each variation starts the Table 38 cycle at its own lord."""
    import swisseph as swe

    periods = compute_nakshatra_dasha(
        V, EX50_MOON, swe.julday(*EX50_BIRTH), DashaYearLength.SAVANA,
        levels=1, cycles=1, start_star=star)
    assert [GRAHA_NAMES[p.lord] for p in periods[:4]] == sequence


def test_the_default_is_unchanged_by_the_new_parameter():
    """Adding the variations must not move the reckoning everything else uses."""
    import swisseph as swe

    jd = swe.julday(*EX50_BIRTH)
    plain = compute_nakshatra_dasha(V, EX50_MOON, jd, DashaYearLength.SAVANA)
    explicit = compute_nakshatra_dasha(V, EX50_MOON, jd, DashaYearLength.SAVANA,
                                       start_star=1)
    assert [(p.lord, p.start_jd) for p in plain] == \
           [(p.lord, p.start_jd) for p in explicit]
    assert balance_at_birth(V, EX50_MOON) == balance_at_birth(V, EX50_MOON, 1)


def test_the_variations_are_reachable_through_the_api():
    """The engine supporting §16.4.1 is only half of it; a caller has to be
    able to ask for kshema, utpanna or adhana."""
    from fastapi.testclient import TestClient

    from hora.api.main import app

    client = TestClient(app)
    body = {"year": 2000, "month": 4, "day": 28, "hour": 5, "minute": 50,
            "utc_offset_hours": -4.0,
            "place": {"latitude": 42.5, "longitude": -71.2}, "levels": 1}

    names = {}
    for star in (1, 4, 5, 8):
        got = client.post("/v1/dasha", json=body | {"start_star": star}).json()
        assert got["start_star"] == star
        names[star] = got["start_star_name"]
        first = got["periods"][0]["lord_name"]
        ratio = got["balance_at_birth"]["years"] / dict(
            zip((GRAHA_NAMES[g] for g in V.order), V.years))[first]
        # The fraction is the Moon's own whichever star starts the cycle.
        assert ratio == pytest.approx(
            client.post("/v1/dasha", json=body | {"start_star": 1}).json()
            ["balance_at_birth"]["years"] / 7)

    assert names == {1: "Moon's own", 4: "kshema", 5: "utpanna", 8: "adhana"}


def test_an_out_of_range_start_star_is_refused():
    from fastapi.testclient import TestClient

    from hora.api.main import app

    body = {"year": 2000, "month": 4, "day": 28, "hour": 5, "minute": 50,
            "utc_offset_hours": -4.0,
            "place": {"latitude": 42.5, "longitude": -71.2}, "start_star": 28}
    assert TestClient(app).post("/v1/dasha", json=body).status_code == 422


# --------------------------------------------------------------------------
# §16.4.2 Dasa from Lagna, and §16.5.1 General Principles
# --------------------------------------------------------------------------


def test_dasa_can_be_reckoned_from_the_lagna_instead_of_the_moon():
    """§16.4.2: "Some authorities have also recommended Vimsottari dasa from
    the longitude of lagna instead of Moon."

    Everything downstream is unchanged; only which longitude seeds the cycle.
    """
    from fastapi.testclient import TestClient

    from hora.api.main import app

    client = TestClient(app)
    body = {"year": 2000, "month": 4, "day": 28, "hour": 5, "minute": 50,
            "utc_offset_hours": -4.0,
            "place": {"latitude": 42.5, "longitude": -71.2}, "levels": 1}

    moon = client.post("/v1/dasha", json=body).json()
    lagna = client.post("/v1/dasha", json=body | {"reckon_from": "lagna"}).json()

    assert moon["reckon_from"] == "moon"
    assert moon["seed_longitude"] == pytest.approx(moon["moon_longitude"])
    assert lagna["reckon_from"] == "lagna"
    assert lagna["seed_longitude"] != pytest.approx(moon["moon_longitude"])

    # The seed decides the lord, and the balance is still that lord's share.
    for got in (moon, lagna):
        lord = got["periods"][0]["lord_name"]
        length = dict(zip((GRAHA_NAMES[g] for g in V.order), V.years))[lord]
        assert 0 < got["balance_at_birth"]["years"] <= length


def test_only_moon_and_lagna_may_seed_the_cycle():
    """The section names one alternative, so the parameter admits one."""
    from fastapi.testclient import TestClient

    from hora.api.main import app

    body = {"year": 2000, "month": 4, "day": 28, "hour": 5, "minute": 50,
            "utc_offset_hours": -4.0,
            "place": {"latitude": 42.5, "longitude": -71.2},
            "reckon_from": "sun"}
    assert TestClient(app).post("/v1/dasha", json=body).status_code == 422


def test_the_lagna_caveat_is_kept_with_the_rule():
    """"this will give better results only when lagna is considerably more
    powerful than Moon" — a judgement the section leaves to the reader, and
    one we must not silently make for them."""
    from hora.core.const import DASA_FROM_LAGNA

    assert "considerably more powerful than Moon" in DASA_FROM_LAGNA


def test_the_nine_reading_examples_are_recorded_as_examples():
    """§16.5.1 calls them "just a few examples", so they are a register of
    what a reading looks like, not a lookup table to predict from."""
    from hora.core.const import VIMSOTTARI_READING_EXAMPLES as EXAMPLES

    assert len(EXAMPLES) == 9
    assert [e["n"] for e in EXAMPLES] == list(range(1, 10))
    assert {e["divisional"] for e in EXAMPLES} == {
        "rasi", "D-4", "D-7", "D-9", "D-10", "D-30"}
    # The section hedges two of the nine differently; that is kept.
    assert [e["n"] for e in EXAMPLES if e["certainty"] == "may"] == [8, 9]


def test_every_reading_example_names_a_chart_and_a_placement():
    """A reading with no chart, or no placement to look for, would be advice
    rather than a method."""
    from hora.core.const import VIMSOTTARI_READING_EXAMPLES as EXAMPLES

    for example in EXAMPLES:
        assert example["divisional"]
        assert example["reads"]
        assert example["gives"]


def test_the_dasa_lord_becomes_a_temporary_lagna_for_antardasas():
    """The section's closing rule, which is a technique rather than an
    illustration and is the one part of 16.5.1 that generalises."""
    from hora.core.const import DASA_LORD_AS_TEMPORARY_LAGNA

    assert "temporary lagna" in DASA_LORD_AS_TEMPORARY_LAGNA
    assert "antardasas" in DASA_LORD_AS_TEMPORARY_LAGNA


# --------------------------------------------------------------------------
# §16.5.2 Using Dasa Variations
# --------------------------------------------------------------------------

#: The section's own worked case: Moon in Makha 3rd pada.
MAKHA_3RD_PADA = 9 * NAKSHATRA_SPAN + 2.5 * (NAKSHATRA_SPAN / 4)


def test_a_star_lying_in_one_sign_needs_no_pada_rule():
    from hora.dasha.base import variation_sign

    got = variation_sign(MAKHA_3RD_PADA, 1)
    assert got.nakshatra_name == "Magha"
    assert got.rasi_name == "Leo"
    assert got.spans_two_signs is False


def test_a_star_spanning_two_signs_is_resolved_by_the_moons_pada():
    """"If Moon is in Makha 3rd pada, for example, 5th star is Chitra and it
    starts in Virgo and ends in Libra. So we should take the 3rd quarter of
    Chitra and we then get Libra."

    Not the star's start, not its midpoint — the Moon's own quarter.
    """
    from hora.dasha.base import variation_sign

    got = variation_sign(MAKHA_3RD_PADA, 5)
    assert got.nakshatra_name == "Chitra"
    assert got.spans_two_signs is True
    assert got.rasi_name == "Libra"
    assert "pada 3" in got.reason

    # Chitra begins in Virgo, so taking the star's start would give Virgo.
    assert int((got.nakshatra * NAKSHATRA_SPAN) // 30) != got.rasi


def test_the_general_comparison_is_leo_against_libra():
    """"So Leo's strength should be compared to Libra's.\""""
    from hora.dasha.base import variation_candidates

    got = variation_candidates(MAKHA_3RD_PADA, "general")
    assert [v.rasi_name for v in got] == ["Leo", "Libra"]
    assert [v.star for v in got] == [1, 5]


def test_the_longevity_comparison_is_leo_virgo_and_scorpio():
    """"If Moon is in Makha 3rd pada in Leo, 4th and 8th stars are Hasta
    (Virgo) and Anuradha (Scorpio). We should compare the strengths of Leo,
    Virgo and Scorpio.\""""
    from hora.dasha.base import variation_candidates

    got = variation_candidates(MAKHA_3RD_PADA, "longevity")
    assert [v.nakshatra_name for v in got] == ["Magha", "Hasta", "Anuradha"]
    assert [v.rasi_name for v in got] == ["Leo", "Virgo", "Scorpio"]


def test_the_two_purposes_call_opposite_signs_stronger():
    """The section's least obvious point.

    For general results "a sign aspected by Jupiter and occupied by more
    planets may be taken to be stronger"; for longevity "a sign aspected by
    marakas and malefics becomes stronger". Strength here is not one quantity
    read for two purposes — it is two different questions, and a single
    strength routine used for both would be wrong for one of them.
    """
    from hora.core.const import VARIATION_CHOICE

    general = VARIATION_CHOICE["general"]["stronger_when"]
    longevity = VARIATION_CHOICE["longevity"]["stronger_when"]
    assert "Jupiter" in general and "malefics" not in general
    assert "marakas and malefics" in longevity and "Jupiter" not in longevity
    assert VARIATION_CHOICE["general"]["compare"] == (1, 5)
    assert VARIATION_CHOICE["longevity"]["compare"] == (1, 4, 8)


def test_we_do_not_invent_the_comparison_the_book_says_is_undefined():
    """"There are no clear guidelines in the literature to compare the
    strengths." So the helper returns the candidate signs and stops; picking
    a winner is not ours to do."""
    from hora.core.const import NO_GUIDELINES_FOR_SIGN_STRENGTH
    from hora.dasha.base import variation_candidates

    assert "no clear guidelines" in NO_GUIDELINES_FOR_SIGN_STRENGTH
    got = variation_candidates(MAKHA_3RD_PADA, "general")
    assert all(not hasattr(v, "is_strongest") for v in got)
    assert all(not hasattr(v, "strength") for v in got)


def test_an_unknown_purpose_is_refused():
    from hora.dasha.base import variation_candidates

    with pytest.raises(ValueError, match="general.*longevity"):
        variation_candidates(MAKHA_3RD_PADA, "wealth")


# --------------------------------------------------------------------------
# §16.5.3 Rath's "Tripod of Life" Principle
# --------------------------------------------------------------------------


def test_the_tripod_rings_run_lagna_moon_sun_from_the_inside():
    """"the innermost chakra representing the houses with respect to lagna
    (body), next chakra representing the houses with respect to Moon (mind)
    and the outermost chakra representing the houses with respect to Sun
    (soul)." The order is the section's, and it is not alphabetical or by
    planet — it is body, mind, soul outward.
    """
    from hora.core.const import TRIPOD_OF_LIFE

    assert [t["reference"] for t in TRIPOD_OF_LIFE] == ["lagna", "Moon", "Sun"]
    assert [t["stands_for"] for t in TRIPOD_OF_LIFE] == ["body", "mind", "soul"]
    assert [t["ring"] for t in TRIPOD_OF_LIFE] == ["innermost", "middle", "outermost"]


def test_the_slowest_results_belong_to_the_soul_and_the_fastest_to_the_body():
    """"The results experienced due to soul (Sun) last long and change slowly.
    The results experienced due to mind (Moon) last shorter and change fast.
    The results experienced due to body (lagna) change even faster.\""""
    from hora.core.const import TRIPOD_OF_LIFE

    by_ref = {t["reference"]: t["changes"] for t in TRIPOD_OF_LIFE}
    assert by_ref["Sun"] < by_ref["Moon"] < by_ref["lagna"]


def test_each_reference_point_judges_its_own_dasa_level():
    """"Sun is an important reference point... when judging the results of a
    mahadasa. Moon... an antardasa. Lagna... a pratyantardasa."

    The pairing is the tripod's point: the slowest-changing reference judges
    the longest period.
    """
    from hora.core.const import TRIPOD_OF_LIFE

    assert {t["reference"]: t["judges"] for t in TRIPOD_OF_LIFE} == {
        "Sun": "mahadasa", "Moon": "antardasa", "lagna": "pratyantardasa"}


def test_ravi_and_chandra_yogas_show_at_their_own_levels():
    """"If a planet takes part in a Ravi yoga... it gives the results of the
    yoga in its mahadasa. If a planet takes part in a Chandra Yoga... in its
    antardasas.\""""
    from hora.charts.planetary_yogas.registry import YOGA_REGISTRY, dasa_level

    for key, spec in YOGA_REGISTRY.items():
        if spec.group == "ravi":
            assert dasa_level(key) == "mahadasa", key
        elif spec.group == "chandra":
            assert dasa_level(key) == "antardasa", key


def test_every_other_yoga_including_raja_yogas_shows_in_pratyantardasas():
    """"If a planet takes part in other yogas (e.g. a Raja Yoga), it gives the
    results of the yoga primarily in its pratyantardasas."

    The section picks raja yogas as its example of "other", so they must not
    be given a level of their own however important they are elsewhere.
    """
    from hora.charts.planetary_yogas.registry import YOGA_REGISTRY, dasa_level

    raja = [k for k, v in YOGA_REGISTRY.items() if v.group.startswith("raaja")]
    assert raja, "the registry should hold raja yogas"
    assert all(dasa_level(k) == "pratyantardasa" for k in raja)

    named = {"ravi", "chandra"}
    others = [k for k, v in YOGA_REGISTRY.items() if v.group not in named]
    assert all(dasa_level(k) == "pratyantardasa" for k in others)


def test_the_three_levels_partition_the_whole_registry():
    """Every yoga gets exactly one level, and only the two named groups leave
    the default — so a new yoga group cannot silently acquire a level."""
    from collections import Counter

    from hora.charts.planetary_yogas.registry import YOGA_REGISTRY, dasa_level

    counts = Counter(dasa_level(k) for k in YOGA_REGISTRY)
    assert set(counts) == {"mahadasa", "antardasa", "pratyantardasa"}
    assert sum(counts.values()) == len(YOGA_REGISTRY)
    assert counts["mahadasa"] == sum(
        1 for v in YOGA_REGISTRY.values() if v.group == "ravi")
    assert counts["antardasa"] == sum(
        1 for v in YOGA_REGISTRY.values() if v.group == "chandra")


def test_an_unknown_yoga_is_refused():
    from hora.charts.planetary_yogas.registry import YogaError, dasa_level

    with pytest.raises(YogaError, match="unknown yoga"):
        dasa_level("nonesuch")
