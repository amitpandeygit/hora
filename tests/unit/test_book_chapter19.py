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
