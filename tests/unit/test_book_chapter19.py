"""Chapter 19 — Lagna Kendradi Rasi Dasa.

The book's second rasi dasa. It shares §18.2.1's dasa seed and §18.2.2's
lengths outright, so what is tested here is the part that differs: a fixed
walk through quadrants, succedents and cadents, and a direction rule that
reads a different thing from a different sign classification.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_NAMES

R = {name: i for i, name in enumerate(RASI_NAMES)}
ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def test_the_three_groups_in_the_order_the_dasas_take_them():
    """"First 4 dasas will belong to the kendras (1st, 4th, 7th and 10th) from
    dasa seed... Next 4 dasas will belong to the panapharas (2nd, 5th, 8th and
    11th)... Last 4 dasas will belong to the apoklimas (3rd, 6th, 9th and
    12th)."

    Unlike Narayana's three movements this never varies with the seed. Only
    the direction does.
    """
    from hora.dasha.rasi.kendradi import GROUPS, HOUSE_ORDER

    assert [g["name"] for g in GROUPS] == ["kendra", "panaphara", "apoklima"]
    assert [g["houses"] for g in GROUPS] == [(1, 4, 7, 10), (2, 5, 8, 11),
                                             (3, 6, 9, 12)]
    assert HOUSE_ORDER == (1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 12)
    assert sorted(HOUSE_ORDER) == list(range(1, 13))


def test_the_forward_order_the_section_prints():
    """"Suppose lagna is in Ge and Ge is stronger than Sg. Then dasas start
    from Ge. Because Ge is an odd sign, we go in the forward order and get
    dasa order as: Ge (1st), Vi (4th), Sg (7th), Pi (10th), Cn (2nd), Li
    (5th), Cp (8th), Ar (11th), Le (3rd), Sc (6th), Aq (9th), Ta (12th)."
    """
    from hora.dasha.rasi.kendradi import progression

    got = progression(R["Gemini"], R["Gemini"])
    assert got.direction == "forward"
    assert [ABBR[s] for s in got.signs] == [
        "Ge", "Vi", "Sg", "Pi", "Cn", "Li", "Cp", "Ar", "Le", "Sc", "Aq", "Ta"]
    assert got.houses == (1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 12)
    assert got.group_names[:4] == ("kendra",) * 4
    assert got.group_names[8:] == ("apoklima",) * 4


def test_the_backward_order_the_section_prints():
    """"Suppose lagna is in Ta and Ta is stronger than Sc... Because Ta is an
    even sign, we go in the backward order and count houses in the backward
    direction. We get dasa order as: Ta (1st), Aq (4th), Sc (7th), Le (10th),
    Ar (2nd), Cp (5th), Li (8th), Cn (11th), Pi (3rd), Sg (6th), Vi (9th), Ge
    (12th)."

    "Backward" reverses the counting, not the list: the 4th from Taurus is
    Aquarius, not Leo, and the house numbers stay in the same order.
    """
    from hora.dasha.rasi.kendradi import progression

    got = progression(R["Taurus"], R["Taurus"])
    assert got.direction == "backward"
    assert [ABBR[s] for s in got.signs] == [
        "Ta", "Aq", "Sc", "Le", "Ar", "Cp", "Li", "Cn", "Pi", "Sg", "Vi", "Ge"]
    assert got.houses == (1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 12)


@pytest.mark.parametrize("seed", range(12))
@pytest.mark.parametrize("direction", ["forward", "backward"])
def test_every_rasi_takes_exactly_one_dasa(seed, direction):
    from hora.dasha.rasi.kendradi import house_signs

    signs = house_signs(seed, direction)
    assert len(signs) == 12
    assert set(signs) == set(range(12))
    assert signs[0] == seed


def test_the_direction_reads_odd_and_even_signs_not_odd_footed_ones():
    """"NOTE: We are talking about odd and even signs here and not about
    odd-footed and even-footed signs."

    The third time the book makes this distinction — §18.3 warned about it for
    antardasas and §18.2 uses the other one. The two classifications disagree
    on a third of the zodiac, so the note earns its place.
    """
    from hora.core.const import RASI_IS_ODD, RASI_IS_ODD_FOOTED
    from hora.dasha.rasi.kendradi import DIRECTION_RULE, direction_of

    assert "not about odd-footed" in DIRECTION_RULE
    disagree = {RASI_NAMES[i] for i in range(12)
                if bool(RASI_IS_ODD[i]) != bool(RASI_IS_ODD_FOOTED[i])}
    assert disagree == {"Taurus", "Leo", "Scorpio", "Aquarius"}

    for rasi in range(12):
        expected = "forward" if RASI_IS_ODD[rasi] else "backward"
        assert direction_of(rasi) == expected


def test_reading_the_direction_from_lagna_or_the_seed_can_never_differ():
    """Rule 2 says the direction comes from **lagna**; rule 1 has just named
    the **dasa seed**, and rule 2's own exceptions read the seed. That looks
    like it could matter on a 7th-seeded chart — and it never can.

    Lagna and the 7th are six signs apart and six is even, so they always
    share their parity. The mismatch in the wording is harmless by
    construction, not by luck.
    """
    from hora.dasha.rasi.kendradi import (
        direction_of,
        lagna_and_seventh_always_agree,
        progression,
    )

    for lagna in range(12):
        assert lagna_and_seventh_always_agree(lagna)
        seventh = (lagna + 6) % 12
        assert direction_of(lagna) == direction_of(seventh)
        # and so the progression is the same whichever of the two seeds it is
        assert progression(lagna, lagna).direction == \
            progression(seventh, lagna).direction


def test_saturn_in_the_seed_forces_the_order_forward():
    """"If Saturn is in the stronger of lagna and 7th, dasa order is
    forward." Taurus would otherwise run backward.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.kendradi import progression

    plain = progression(R["Taurus"], R["Taurus"])
    assert plain.direction == "backward"
    assert plain.exception is None

    got = progression(R["Taurus"], R["Taurus"], {int(Graha.SATURN)})
    assert got.exception == "Saturn"
    assert got.direction == "forward"
    assert [ABBR[s] for s in got.signs][:4] == ["Ta", "Le", "Sc", "Aq"]


def test_ketu_in_the_seed_reverses_whatever_the_order_would_be():
    """"If Ketu is in the stronger of lagna and 7th, dasa order is reversed."

    Reversed, not forced — so it turns Gemini's forward into backward and
    Taurus' backward into forward.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.kendradi import progression

    odd = progression(R["Gemini"], R["Gemini"], {int(Graha.KETU)})
    assert odd.exception == "Ketu"
    assert odd.direction == "backward"

    even = progression(R["Taurus"], R["Taurus"], {int(Graha.KETU)})
    assert even.exception == "Ketu"
    assert even.direction == "forward"
    assert even.signs == progression(R["Taurus"], R["Taurus"],
                                     {int(Graha.SATURN)}).signs


def test_a_seed_holding_both_saturn_and_ketu_is_refused():
    """Here the two exceptions contradict outright — one forces forward, the
    other reverses — where §18.2.1's pair acted on different things and could
    at least be argued to compose. §19.2 states no precedence either way, so
    the seed is refused rather than an order being guessed. Same question as
    OI-120, one chapter on.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.kendradi import KendradiError, progression

    with pytest.raises(KendradiError, match="both Saturn and Ketu"):
        progression(R["Taurus"], R["Taurus"],
                    {int(Graha.SATURN), int(Graha.KETU)})


def test_the_seed_is_18_2_1s_seed_and_the_lengths_are_18_2_2s():
    """"Dasas start from the stronger of lagna and 7th house" is §18.2.1's
    rule word for word, and rule 6 says "dasa periods of various rasis in this
    dasa system are found just like in Narayana dasa".

    So chapter 19 adds a walk and a direction, and borrows everything else.
    Worked on Chart 24, whose Narayana dasa Example 68 prints.
    """
    from hora.charts.book import graha_longitudes, lagna
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.kendradi import LENGTHS_ARE_NARAYANAS, progression
    from hora.dasha.rasi.narayana import dasa_length, dasa_seed

    longitudes = {int(g): lon for g, lon in graha_longitudes(24).items()}
    lagna_sign = lagna(24)
    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["seed"] == lagna_sign == R["Gemini"]   # Example 68's own seed

    got = progression(seed["seed"], lagna_sign)
    assert got.direction == "forward"                  # Gemini is an odd sign
    assert [ABBR[s] for s in got.signs][:4] == ["Ge", "Vi", "Sg", "Pi"]

    # Example 68 prints Ge at 4 years; rule 6 keeps that length here.
    mercury = int(RASI_LORD[R["Gemini"]])
    assert mercury == int(Graha.MERCURY)
    assert dasa_length(R["Gemini"], mercury,
                       int(longitudes[mercury] // 30), "exalted").years == 4
    assert "just like in Narayana dasa" in LENGTHS_ARE_NARAYANAS


def test_the_same_seed_gives_a_different_order_from_narayanas():
    """The two dasas part company on the walk alone. Chart 24 seeds both from
    Gemini; Narayana takes Vishnu's trinal movement backward, this takes the
    quadrants forward, and they share only the first period.
    """
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.dasha.rasi import kendradi, narayana

    longitudes = {int(g): lon for g, lon in graha_longitudes(24).items()}
    signs = {int(g): s for g, s in graha_signs(24).items()}
    lagna_sign = lagna(24)
    seed = narayana.dasa_seed(lagna_sign, longitudes)["seed"]
    occupants = {g for g, s in signs.items() if s == seed}

    by_narayana = narayana.progression(seed, occupants).signs
    by_kendradi = kendradi.progression(seed, lagna_sign, occupants).signs

    assert by_narayana[0] == by_kendradi[0] == seed
    assert by_narayana[1:] != by_kendradi[1:]
    assert [ABBR[s] for s in by_narayana][:4] == ["Ge", "Aq", "Li", "Vi"]
    assert [ABBR[s] for s in by_kendradi][:4] == ["Ge", "Vi", "Sg", "Pi"]


def test_moola_dasa_is_described_and_deliberately_not_built():
    """"Moola dasa is beyond the scope of this book. But we will cover a
    similar dasa, which belongs to rasis instead of planets."

    §19.1 opens on a dasa it then declines to teach. Recorded so a reader
    meeting "Kendradi Graha Dasa" or "Moola dasa" elsewhere finds the book's
    position here, and so its absence is visibly deliberate.
    """
    from hora.dasha.rasi.kendradi import (
        MOOLA_DASA_OUT_OF_SCOPE,
        MOOLA_DASA_WHEN_IT_IS_BETTER,
        SHOWS_MATERIAL_SUCCESS,
    )

    assert "beyond the scope of this book" in MOOLA_DASA_OUT_OF_SCOPE
    assert "stronger of lagna and Moon" in MOOLA_DASA_OUT_OF_SCOPE
    assert "moolatrikona correction" in MOOLA_DASA_OUT_OF_SCOPE
    assert "4 planets in quadrants" in MOOLA_DASA_WHEN_IT_IS_BETTER
    assert "material success" in SHOWS_MATERIAL_SUCCESS


def test_house_signs_refuses_a_direction_it_does_not_know():
    from hora.dasha.rasi.kendradi import KendradiError, house_signs

    with pytest.raises(KendradiError, match="forward"):
        house_signs(R["Aries"], "widdershins")


# --------------------------------------------------------------------------
# §19.3 Interpretation — whose movement this is, and why that matters.
# --------------------------------------------------------------------------

def test_parasaras_two_rulers():
    """"Parasara taught that the quadrants are ruled by Sri Maha Vishnu and
    the trines are ruled by Sri Maha Lakshmi."
    """
    from hora.dasha.rasi.kendradi import PARASARA_MOVEMENT_RULERS

    by_houses = {r["houses"]: r["ruler"] for r in PARASARA_MOVEMENT_RULERS}
    assert by_houses == {"quadrants": "Sri Maha Vishnu",
                         "trines": "Sri Maha Lakshmi"}


def test_the_naming_is_the_inverse_of_what_the_steps_look_like():
    """"the sequence 1st, 5th, 9th, 10th etc is quadrant-based and it is ruled
    by Narayana. The sequence 1st, 4th, 7th, 10th is trine-based and it is
    ruled by Lakshmi."

    Read quickly this is backwards: the sequence made of **trines** is called
    quadrant-based, and the one made of **quadrants** is called trine-based.
    The label names the outer grouping, never the inner step. Pinned as a
    contradiction between the two so it cannot be silently "corrected".
    """
    from hora.dasha.rasi.kendradi import MOVEMENT_NAMING, MOVEMENT_NAMING_TEXT

    by_ruler = {m["ruler"]: m for m in MOVEMENT_NAMING}
    assert by_ruler["Narayana"]["steps"] == "trines"
    assert by_ruler["Narayana"]["grouping"] == "quadrant-based"
    assert by_ruler["Lakshmi"]["steps"] == "quadrants"
    assert by_ruler["Lakshmi"]["grouping"] == "trine-based"

    for movement in MOVEMENT_NAMING:                 # steps never match label
        assert not movement["grouping"].startswith(movement["steps"][:5])

    assert "1st, 5th, 9th, 10th etc is quadrant-based" in MOVEMENT_NAMING_TEXT
    assert "1st, 4th, 7th, 10th is trine-based" in MOVEMENT_NAMING_TEXT


def test_the_two_movements_classify_from_their_house_orders_alone():
    """§19.3's claim made checkable rather than only quoted.

    Narayana dasa's dual-sign order really is four trines whose leaders form a
    quadrant; Kendradi's really is three quadrants whose sets are a trine's.
    Neither classification is asserted by hand — both fall out of the orders
    the two chapters print.
    """
    from hora.dasha.rasi.kendradi import HOUSE_ORDER, movement_grouping
    from hora.dasha.rasi.narayana import house_order

    kendradi = movement_grouping(HOUSE_ORDER)
    assert kendradi["grouping"] == "trine-based"
    assert kendradi["ruler"] == "Lakshmi"
    assert kendradi["steps"] == "quadrants"
    assert kendradi["groups"] == ((1, 4, 7, 10), (2, 5, 8, 11), (3, 6, 9, 12))

    vishnu = movement_grouping(house_order(R["Gemini"]))   # a dual sign
    assert vishnu["grouping"] == "quadrant-based"
    assert vishnu["ruler"] == "Narayana"
    assert vishnu["steps"] == "trines"
    assert vishnu["groups"] == ((1, 5, 9), (10, 2, 6), (7, 11, 3), (4, 8, 12))


def test_narayanas_other_two_movements_are_neither():
    """"This progression is seen for dual signs in Narayana dasa" — only for
    dual signs. Brahma's regular walk and Shiva's 6th are neither of §19.3's
    two, so the classifier refuses them rather than forcing a ruler on them.
    """
    from hora.dasha.rasi.kendradi import KendradiError, movement_grouping
    from hora.dasha.rasi.narayana import house_order

    for movable_or_fixed in (R["Aries"], R["Taurus"]):
        with pytest.raises(KendradiError, match="neither"):
            movement_grouping(house_order(movable_or_fixed))


def test_the_two_sections_name_the_same_groups_from_different_members():
    """§19.2 rule 4 lists the second group as "2nd, 5th, 8th and 11th"; §19.3
    calls it "the quadrants of 5th/9th", which would start it at the 5th.

    The sets are identical — {2,5,8,11} is the quadrant-set of 5 — and §19.2's
    printed orders settle the order within each group. They look like they
    disagree and do not.
    """
    from hora.dasha.rasi.kendradi import (
        GROUPS,
        SECOND_GROUP_IS_LISTED_FROM_ITS_LOWEST,
        _quadrant_set,
    )

    assert set(GROUPS[1]["houses"]) == set(_quadrant_set(5))
    assert set(GROUPS[2]["houses"]) == set(_quadrant_set(9))
    assert set(GROUPS[0]["houses"]) == set(_quadrant_set(1))
    assert GROUPS[1]["houses"][0] == 2          # §19.2's listing, not §19.3's
    assert "2nd, 5th, 8th and 11th" in SECOND_GROUP_IS_LISTED_FROM_ITS_LOWEST


def test_lakshmis_movement_is_why_this_dasa_is_for_prosperity():
    """"Lakshmi is the goddess of wealth and prosperity. So this dasa shows
    the periods of prosperity."

    §19.1 said it shows material success; §19.3 says why. The two statements
    have to agree or one of them is a transcription slip.
    """
    from hora.dasha.rasi.kendradi import (
        LAKSHMI_SHOWS_PROSPERITY,
        SHOWS_MATERIAL_SUCCESS,
    )

    assert "material success" in SHOWS_MATERIAL_SUCCESS
    assert "periods of prosperity" in LAKSHMI_SHOWS_PROSPERITY
    assert "goddess of wealth and prosperity" in LAKSHMI_SHOWS_PROSPERITY
    assert "progression of lagna" in LAKSHMI_SHOWS_PROSPERITY


def test_sudasa_is_this_dasa_from_sree_lagna_and_chapter_5_already_said_so():
    """"Sudasa is also a Kendradi Rasi Dasa, but started from Sree Lagna
    instead of lagna."

    §5.7 recorded `SREE_LAGNA_USED_IN = "Sudasa"` before this chapter existed;
    this is the other end of that link, and it tells us Sudasa will reuse this
    module with a different seed. `progression` already takes the seed and the
    lagna separately, so it is ready for it.
    """
    import inspect

    from hora.charts.special_lagna import (
        SREE_ALSO_MEANS,
        SREE_LAGNA_USED_IN,
        sree_lagna,
    )
    from hora.dasha.rasi.kendradi import (
        SUDASA_IS_KENDRADI_FROM_SREE_LAGNA,
        progression,
    )

    assert SREE_LAGNA_USED_IN == "Sudasa"
    assert "Lakshmi" in SREE_ALSO_MEANS
    assert "Lakshmi sthana" in SUDASA_IS_KENDRADI_FROM_SREE_LAGNA
    assert "also a Kendradi Rasi Dasa" in SUDASA_IS_KENDRADI_FROM_SREE_LAGNA
    assert callable(sree_lagna)

    params = list(inspect.signature(progression).parameters)
    assert params[:2] == ["seed", "lagna"]      # seed and lagna are separable


# --------------------------------------------------------------------------
# Example 76 — Ronald Reagan, Chart 34. The lengths and dates below are our
# derivation, recorded before Table 41 was read.
# --------------------------------------------------------------------------

#: Our lengths, in progression order. Table 41 will confirm or contradict.
EX76_LENGTHS = [("Ta", 9), ("Aq", 10), ("Sc", 11), ("Le", 7), ("Ar", 8),
                ("Cp", 8), ("Li", 4), ("Cn", 3), ("Pi", 5), ("Sg", 10),
                ("Vi", 9), ("Ge", 6)]


def _chart_34():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(34).items()},
            {int(g): sign for g, sign in graha_signs(34).items()},
            lagna(34))


def _ex76_lord(rasi, longitudes, signs):
    """§15.5.1 with rule 5a's lengths supplied, as §19.2 rule 6 requires."""
    from hora.charts.colord import CO_LORDS, stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    if rasi not in CO_LORDS:
        return int(RASI_LORD[rasi])
    years = {g: dasa_length(rasi, g, signs[g],
                            sign_dignity(g, longitudes[g])).years
             for g in CO_LORDS[rasi]}
    got = stronger(rasi, longitudes, purpose="dasa", dasa_years=years)
    return got.winner if got.winner is not None else int(RASI_LORD[rasi])


def test_chart_34_is_chart_7_reprinted():
    """The book gives Reagan a second number for chapter 19 without changing a
    figure. Both entries carry the same twelve longitudes, and this pins them
    equal so an edit to one cannot silently diverge from the other.
    """
    from hora.charts.book import chart, longitudes

    assert longitudes(7) == longitudes(34)
    assert chart(7)["birth"] == chart(34)["birth"]
    assert chart(7)["chara_karakas"] == chart(34)["chara_karakas"]


def test_chart_34s_drawn_arudha_lagna_needs_15_5_1():
    """The diagram puts AL in Vi. Scorpio's lord goes to §15.5.1, which gives
    Ketu at rule 2 — Jupiter conjoins him in Libra and his dispositor Venus
    aspects from Aquarius, against Mercury's single conjunction with Mars.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import chart
    from hora.charts.colord import stronger
    from hora.core.const import Graha

    longitudes, signs, lagna_sign = _chart_34()
    chosen = stronger(R["Scorpio"], longitudes, purpose="arudha").winner
    assert chosen == int(Graha.KETU)

    got = arudha_pada(1, lagna_sign, signs, {R["Scorpio"]: chosen})
    assert ABBR[got.sign] == chart(34)["drawn"]["AL"] == "Vi"


def test_example_76_seed_is_taurus_by_jupiters_aspect():
    """"Lagna is in Sc. Ta is stronger than Sc, as it has Jupiter's aspect.
    So dasas start from Ta."

    §19.2 rule 1 is §18.2.1's seed rule, so `dasa_seed` serves both. Rule 1
    ties on nothing — neither rasi holds a graha — and rule 2 decides on the
    single aspect the example names.
    """
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign = _chart_34()
    assert lagna_sign == R["Scorpio"]
    assert not [g for g, s in signs.items()
                if s in (R["Scorpio"], R["Taurus"])]

    verdict = stronger(R["Taurus"], R["Scorpio"], longitudes, purpose="phalita")
    assert verdict.winner == R["Taurus"]
    assert verdict.decided_by == "2"
    assert "Taurus count 1 (Jupiter (Jupiter) aspects from Libra)" in verdict.reason
    assert "Scorpio count 0" in verdict.reason

    assert dasa_seed(lagna_sign, longitudes)["seed"] == R["Taurus"]


def test_example_76_reads_the_direction_from_the_seed_and_it_cannot_matter():
    """"Because Ta is an even rasi, we go anti-zodiacally."

    §19.2 rule 2 says the direction comes from **lagna**; the example reads it
    from the **seed**. Lagna is Scorpio and the seed is Taurus — and both are
    even, so the two readings agree, exactly as they must. This is the book
    itself taking the reading rule 2's wording does not, on a chart where it
    could not be caught.
    """
    from hora.core.const import RASI_IS_ODD
    from hora.dasha.rasi.kendradi import direction_of, progression

    _longitudes, signs, lagna_sign = _chart_34()
    seed = R["Taurus"]
    assert not RASI_IS_ODD[lagna_sign]
    assert not RASI_IS_ODD[seed]
    assert direction_of(lagna_sign) == direction_of(seed) == "backward"

    got = progression(seed, lagna_sign,
                      {g for g, s in signs.items() if s == seed})
    assert got.direction == "backward"
    assert got.exception is None
    assert [ABBR[s] for s in got.signs] == [
        "Ta", "Aq", "Sc", "Le", "Ar", "Cp", "Li", "Cn", "Pi", "Sg", "Vi", "Ge"]


def test_example_76_is_19_2s_own_worked_order():
    """"Suppose lagna is in Ta and Ta is stronger than Sc..." — §19.2's second
    illustration is this chart's order exactly, though the section reached it
    from a Taurus lagna and the example reaches it from a Scorpio one seeded
    on the 7th.
    """
    from hora.dasha.rasi.kendradi import progression

    illustration = progression(R["Taurus"], R["Taurus"])
    reagan = progression(R["Taurus"], R["Scorpio"])
    assert illustration.signs == reagan.signs


@pytest.mark.parametrize("abbr,years", EX76_LENGTHS)
def test_example_76_lengths_our_derivation(abbr, years):
    """§19.2 rule 6 sends lengths to §18.2.2 unchanged. Recorded before Table
    41 was read, so a disagreement is a finding rather than a fixture to
    adjust.
    """
    from hora.charts.dignity import sign_dignity
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_34()
    rasi = {v: k for k, v in enumerate(ABBR)}[abbr]
    lord = _ex76_lord(rasi, longitudes, signs)
    got = dasa_length(rasi, lord, signs[lord],
                      sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why


def test_example_76_scorpio_swings_the_whole_timeline_by_ten_years():
    """The sharpest §15.5.1 decision in the book so far.

    Scorpio's co-lords sit ten houses apart in the counting: Mars in Sg is one
    house on and gives **1 year**, Ketu in Li is eleven and gives **11**.
    §15.5.1 reaches Ketu at rule 2 — Jupiter conjoins him and his dispositor
    Venus aspects from Aquarius, against Mercury's single conjunction with
    Mars. Ten years ride on it: with Mars, every dasa after 1930 moves forward
    a decade and Reagan's presidency falls in Virgo rather than Sagittarius.
    """
    from hora.charts.colord import stronger
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_34()
    mars, ketu = int(Graha.MARS), int(Graha.KETU)

    by_mars = dasa_length(R["Scorpio"], mars, signs[mars])
    by_ketu = dasa_length(R["Scorpio"], ketu, signs[ketu])
    assert (by_mars.years, by_ketu.years) == (1, 11)

    got = stronger(R["Scorpio"], longitudes, purpose="dasa",
                   dasa_years={mars: by_mars.years, ketu: by_ketu.years})
    assert got.winner == ketu
    assert got.decided_by == "2"            # decided before rule 5a is needed
    assert "Ketu count 2" in got.reason
    assert "dispositor (Venus) aspects from Aquarius" in got.reason


def test_example_76_aquarius_is_rule_5as_second_firing_in_the_book():
    """Both of Aquarius' co-lords are in Aries, so everything above rule 5
    ties — same conjunctions, neither exalted, both in a movable rasi. Rule
    5a takes the longer dasa: Rahu's 10 over Saturn's 9, Saturn losing a year
    to his debilitation. Exercise 29 was the first time this rule fired.
    """
    from hora.charts.colord import stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_34()
    saturn, rahu = int(Graha.SATURN), int(Graha.RAHU)
    assert signs[saturn] == signs[rahu] == R["Aries"]
    assert sign_dignity(saturn, longitudes[saturn]) == "debilitated"

    by_saturn = dasa_length(R["Aquarius"], saturn, signs[saturn], "debilitated")
    by_rahu = dasa_length(R["Aquarius"], rahu, signs[rahu])
    assert (by_saturn.count, by_saturn.years) == (11, 9)     # 10, less a year
    assert (by_rahu.count, by_rahu.years) == (11, 10)

    got = stronger(R["Aquarius"], longitudes, purpose="dasa",
                   dasa_years={saturn: by_saturn.years, rahu: by_rahu.years})
    assert got.winner == rahu
    assert got.decided_by == "5a"


def test_example_76_dates_against_reagans_life():
    """Our derivation, on §18.6's solar arc — every boundary falls near his
    6 February birthday because that is his solar return.

    | dasa | span | what falls in it |
    |---|---|---|
    | Libra | Feb 1964 - Feb 1968 | elected Governor Nov 1966, took office Jan 1967 |
    | Sagittarius | Feb 1976 - Feb 1986 | elected Nov 1980, inaugurated Jan 1981, shot 30 March 1981 |
    | Virgo | Feb 1986 - Feb 1995 | left office Jan 1989, Alzheimer's letter Nov 1994 |
    """
    from hora.charts.book import chart
    from hora.charts.dignity import sign_dignity
    from hora.core.const import Graha
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_jd, from_local
    from hora.dasha.rasi.narayana import (
        dasa_length,
        solar_arc_instant,
        sub_period_arc,
    )

    longitudes, signs, _lagna = _chart_34()
    ephemeris = get_ephemeris(Settings(node_type=NodeType.MEAN))

    def sun_at(jd: float) -> float:
        return ephemeris.position(jd, int(Graha.SUN)).longitude

    birth = from_local(**chart(34)["birth_data"]).jd_ut
    spans, arc = {}, 0.0
    for abbr, _years in EX76_LENGTHS:
        rasi = {v: k for k, v in enumerate(ABBR)}[abbr]
        lord = _ex76_lord(rasi, longitudes, signs)
        years = dasa_length(rasi, lord, signs[lord],
                            sign_dignity(lord, longitudes[lord])).years
        opens = solar_arc_instant(birth, arc, sun_at)
        arc += sub_period_arc(years, 0)
        closes = solar_arc_instant(birth, arc, sun_at)
        spans[abbr] = (from_jd(opens, utc_offset_hours=-6.0).local.date(),
                       from_jd(closes, utc_offset_hours=-6.0).local.date())

    assert spans["Ta"][0].year == 1911
    assert (spans["Li"][0].year, spans["Li"][1].year) == (1964, 1968)
    assert (spans["Sg"][0].year, spans["Sg"][1].year) == (1976, 1986)
    assert (spans["Vi"][0].year, spans["Vi"][1].year) == (1986, 1995)
    assert spans["Ge"][1].year == 2001
    for opens, closes in spans.values():
        assert opens.month == 2 and closes.month == 2   # his solar return


def test_table_41_confirms_every_length_we_derived():
    """Table 41: Ta 9, Aq 10, Sc 11, Le 7, Ar 8, Cp 8, Li 4, Cn 3, Pi 5,
    Sg 10, Vi 9, Ge 6.

    All twelve, derived before the table was read. The two that were in doubt
    both land: Sc at 11 confirms Ketu over Mars and Aq at 10 confirms Rahu
    over Saturn, so §15.5.1's rule 2 and rule 5a are both vindicated on the
    same chart — and the ten-year swing on Scorpio goes the way our cascade
    said it would.
    """
    printed = {"Ta": 9, "Aq": 10, "Sc": 11, "Le": 7, "Ar": 8, "Cp": 8,
               "Li": 4, "Cn": 3, "Pi": 5, "Sg": 10, "Vi": 9, "Ge": 6}
    assert dict(EX76_LENGTHS) == printed
    assert [a for a, _y in EX76_LENGTHS] == list(printed)   # and in that order

    # "Dasas from Ta to Pi add up to 65 years and run during 1911-1976."
    to_pisces = [y for _a, y in EX76_LENGTHS[:9]]
    assert sum(to_pisces) == 65
    assert 1911 + 65 == 1976

    # "Sg dasa runs during 1976-1986. Mr. Reagan became US President in 1980."
    sagittarius_opens = 1911 + sum(to_pisces)
    sagittarius_closes = sagittarius_opens + dict(EX76_LENGTHS)["Sg"]
    assert (sagittarius_opens, sagittarius_closes) == (1976, 1986)
    assert sagittarius_opens <= 1980 < sagittarius_closes


def test_example_76_sagittarius_holds_the_atmakaraka():
    """"Usually rasis containing AK give success. Sg has AK." Mercury at
    28 Sg 49 is the most advanced graha in the chart."""
    from hora.charts.karaka import chara_karakas
    from hora.core.const import Graha

    longitudes, signs, _lagna = _chart_34()
    eight = {g: lon for g, lon in longitudes.items() if g != int(Graha.KETU)}
    karakas = {k.symbol: k.graha for k in chara_karakas(eight)}

    assert karakas["AK"] == int(Graha.MERCURY)
    assert signs[karakas["AK"]] == R["Sagittarius"]


def test_example_76_the_amk_argala_on_sagittarius_is_unobstructed():
    """"Here Sg has an unobstructed argala from AmK Sun, who is in the 2nd
    from Sg in Gopuramsa with 6 rekhas in ashtakavarga."

    Three separate strengths on one graha, and all three come out. The Sun is
    the amatyakaraka in the 2nd — a primary argala — and the 12th, which
    obstructs it, is empty. He is strong in four of the ten dasavarga charts,
    which is the count that names **Gopuraamsa**. And his own bhinnashtakavarga
    gives Capricorn **6** rekhas.
    """
    from hora.charts.argala import argalas_on_sign
    from hora.charts.ashtakavarga import bhinnashtakavarga
    from hora.charts.dignity import sign_dignity
    from hora.charts.karaka import chara_karakas
    from hora.charts.vargas import AMSA_NAMES, VARGA_GROUPS, varga
    from hora.core.const import NATURAL_MALEFIC, Graha

    longitudes, signs, lagna_sign = _chart_34()
    eight = {g: lon for g, lon in longitudes.items() if g != int(Graha.KETU)}
    amk = {k.symbol: k.graha for k in chara_karakas(eight)}["AmK"]
    assert amk == int(Graha.SUN)
    assert signs[amk] == R["Capricorn"]
    assert (signs[amk] - R["Sagittarius"]) % 12 + 1 == 2

    occupants: dict[int, tuple[int, ...]] = {}
    for graha, sign in signs.items():
        occupants[sign] = (*occupants.get(sign, ()), graha)
    found = {(e.kind, e.house): set(e.grahas)
             for e in argalas_on_sign(
                 R["Sagittarius"], occupants,
                 ketu_sign=signs[int(Graha.KETU)],
                 malefic=frozenset(int(g) for g in NATURAL_MALEFIC))}
    assert found[("argala", 2)] == {amk}
    assert found[("virodhargala", 12)] == set()        # nothing obstructs it

    good = {"moolatrikona", "own", "exalted"}
    strong = [code for code in VARGA_GROUPS["dasavarga"]
              if sign_dignity(amk, varga(longitudes[amk], code).longitude) in good]
    assert len(strong) == 4
    assert AMSA_NAMES["dasavarga"][4] == "Gopuraamsa"

    references = {"Sun": signs[int(Graha.SUN)], "Moon": signs[int(Graha.MOON)],
                  "Mars": signs[int(Graha.MARS)],
                  "Mercury": signs[int(Graha.MERCURY)],
                  "Jupiter": signs[int(Graha.JUPITER)],
                  "Venus": signs[int(Graha.VENUS)],
                  "Saturn": signs[int(Graha.SATURN)], "Lagna": lagna_sign}
    assert bhinnashtakavarga("Sun", references).rekhas[R["Capricorn"]] == 6


def test_example_76_sagittarius_holds_ghati_lagna_and_the_lagna_lord():
    """"More than anything else, Sg has GL. GL is the seat of power in a
    chart... Lagna lord Mars is in Sg and he connects lagna to GL."
    """
    from hora.charts.book import longitudes as printed_longitudes
    from hora.core.const import RASI_LORD, Graha

    _longitudes, signs, lagna_sign = _chart_34()
    assert int(printed_longitudes(34)["GL"] // 30) == R["Sagittarius"]

    mars = int(RASI_LORD[lagna_sign])
    assert mars == int(Graha.MARS)
    assert signs[mars] == R["Sagittarius"]


def test_the_stronger_co_lord_is_not_the_lord_everywhere():
    """Example 76 says "lagna lord Mars" of a Scorpio lagna — while the same
    chart's Scorpio dasa length and its arudha lagna both go to **Ketu** by
    §15.5.1.

    So the cascade answers only where a rule sends it, and `RASI_LORD` remains
    the lord everywhere else. That is what D-4 decided when the nodes gained
    co-lordship without gaining `RASI_LORD`, and this is the book confirming
    it on a chart.
    """
    from hora.charts.colord import stronger
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.kendradi import STRONGER_CO_LORD_IS_NOT_THE_LORD

    longitudes, signs, lagna_sign = _chart_34()
    assert lagna_sign == R["Scorpio"]
    assert int(RASI_LORD[R["Scorpio"]]) == int(Graha.MARS)      # the lord
    assert stronger(R["Scorpio"], longitudes,
                    purpose="arudha").winner == int(Graha.KETU)  # §15.5.1's
    assert _ex76_lord(R["Scorpio"], longitudes, signs) == int(Graha.KETU)
    assert "Lagna lord Mars" in STRONGER_CO_LORD_IS_NOT_THE_LORD


def test_chapter_19s_only_reading_rules_are_recorded_together():
    """Chapter 19 has no principle list — §19.3 is about whose movement this
    is, not about reading a period. These four are all it gives, and they
    arrive in Example 76 rather than in a section.

    Unlike OI-122's eleven these are not readings a principle list fails to
    carry; chapter 19 simply has no principle list.
    """
    from hora.dasha.rasi.kendradi import (
        SUCCESS_READINGS,
        WHY_AMK_ARGALA_GIVES_POWER,
    )

    looks_at = [r["looks_at"] for r in SUCCESS_READINGS]
    assert looks_at == ["AK", "AmK", "GL", "lagna lord"]
    assert all(r["text"] and r["gives"] and r["needs"] for r in SUCCESS_READINGS)

    amk = next(r for r in SUCCESS_READINGS if r["looks_at"] == "AmK")
    assert "unobstructed" in amk["needs"]
    assert amk["gives"] == "political power"
    assert "advisors, ministers, secretaries or bureaucrats" in \
        WHY_AMK_ARGALA_GIVES_POWER


# --------------------------------------------------------------------------
# §19.4 Conclusion
# --------------------------------------------------------------------------

def test_sudasa_outranks_this_dasa_for_the_same_matter():
    """"It may be used in conjunction with Sudasa to predict material success.
    However, Sudasa is a superior dasa."

    Chapter 19 points at Sudasa three times — §19.3 says it is this dasa from
    Sree Lagna, §19.4 says it outranks this one for the very matter this one
    is for. A layer weighing the two rasi dasas needs the ordering, and it is
    the book's, not ours.
    """
    from hora.dasha.rasi.kendradi import (
        SHOWS_MATERIAL_SUCCESS,
        SUDASA_IS_KENDRADI_FROM_SREE_LAGNA,
        SUDASA_IS_SUPERIOR,
    )

    assert "material success" in SHOWS_MATERIAL_SUCCESS
    assert "in conjunction with Sudasa" in SUDASA_IS_SUPERIOR
    assert "Sudasa is a superior dasa" in SUDASA_IS_SUPERIOR
    assert "Sree Lagna" in SUDASA_IS_KENDRADI_FROM_SREE_LAGNA


def test_the_two_gatis_are_named_and_only_one_is_built():
    """"the quadrants-panapharas-apoklimas movement is called 'kendraadi
    gati' and certainly not mandooki gati. Mandooki gati... is the 3rd/11th
    jump."

    This chapter's movement finally gets its name. The other is defined by a
    jump and a pointer to a Kalachakra discussion the book has not given, so
    it is recorded and not built — a twelve-sign walk cannot be derived from
    "3rd/11th" without inventing one. A 3rd-step walk alone never reaches
    twelve signs: stepping two at a time closes after six.
    """
    from hora.dasha.rasi.kendradi import GATI_NAMES, HOUSE_ORDER

    by_name = {g["name"]: g for g in GATI_NAMES}
    assert set(by_name) == {"kendraadi gati", "mandooki gati"}

    kendraadi = by_name["kendraadi gati"]
    assert kendraadi["built"] is True
    assert kendraadi["movement"] == "quadrants, panapharas, apoklimas"
    assert HOUSE_ORDER == (1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 12)

    mandooki = by_name["mandooki gati"]
    assert mandooki["built"] is False
    assert mandooki["movement"] == "the 3rd/11th jump"
    assert "Kalachakra" in mandooki["defined_in"]

    # why it is not built: a repeated 3rd-house step closes after six signs
    walk, sign = set(), 0
    for _ in range(12):
        walk.add(sign)
        sign = (sign + 2) % 12
    assert len(walk) == 6


def test_mandooki_gati_waits_on_the_kalachakra_chapter():
    """The book defines mandooki gati only by reference to its own Kalachakra
    discussion, and Kalachakra dasa is one of the five Part 2 systems still to
    come. So the two absences are the same absence.
    """
    from hora.core.constants.dasha import PART_2_DASA_SYSTEMS
    from hora.dasha.rasi.kendradi import GATI_NAMES

    unbuilt = {s["name"] for s in PART_2_DASA_SYSTEMS
               if s["key"] is None and not s.get("module")}
    assert "Kalachakra dasa" in unbuilt

    mandooki = next(g for g in GATI_NAMES if g["name"] == "mandooki gati")
    assert not mandooki["built"]
    assert "Kalachakra" in mandooki["defined_in"]


def test_the_mandooka_dasa_dispute_is_recorded_as_the_books_position():
    """"The dasa presented by the gentleman in question is certainly not
    Mandooka dasa. It is only a variation of the dasa discussed in this
    chapter."

    The only place the book disputes another author's dasa by name. It is a
    claim about naming and attribution, not a calculation, so it is stored
    whole rather than turned into a rule — and the real Mandooka dasa is named
    with the chart it wants, which we do have.
    """
    from hora.charts.vargas import VARGA_REGISTRY
    from hora.dasha.rasi.kendradi import (
        MANDOOKA_DASA_IS_OF_RUDRAMSA,
        MANDOOKA_DASA_MISATTRIBUTION,
    )

    assert "certainly not mandooki gati" in MANDOOKA_DASA_MISATTRIBUTION
    assert "only a variation" in MANDOOKA_DASA_MISATTRIBUTION

    assert "Rudramsa" in MANDOOKA_DASA_IS_OF_RUDRAMSA
    assert "wars and death" in MANDOOKA_DASA_IS_OF_RUDRAMSA
    assert VARGA_REGISTRY["D11"][1] == "Rudramsa"      # the chart exists
