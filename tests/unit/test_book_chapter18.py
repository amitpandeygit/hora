"""Chapter 18 — Narayana dasa, sections 18.1 and 18.2.1.

The first rasi dasa in the book, and the first thing `dasha/rasi/` holds. This
covers the progression only: which rasi takes each period and in what order.
Lengths are a later section.
"""
from __future__ import annotations

from collections import Counter

import pytest

from hora.core.const import (
    MODALITY_NAMES,
    RASI_IS_ODD_FOOTED,
    RASI_MODALITY,
    RASI_NAMES,
)
from hora.dasha.rasi.narayana import (
    MOVEMENTS,
    direction_of,
    house_order,
    movement_of,
    progression,
)

R = {name: i for i, name in enumerate(RASI_NAMES)}


def test_the_odd_footed_signs_are_the_ones_the_section_lists():
    """"odd-footed sign (Ar, Ta, Ge and Li, Sc, Sg)" against "even-footed sign
    (Cn, Le, Vi and Cp, Aq, Pi)".

    `RASI_IS_ODD_FOOTED` had sat unconsumed since chapter 2, where §2.2.3 said
    only that it was "used in some dasas". This is the dasa.
    """
    odd = {RASI_NAMES[r] for r in range(12) if RASI_IS_ODD_FOOTED[r]}
    assert odd == {"Aries", "Taurus", "Gemini", "Libra", "Scorpio", "Sagittarius"}


def test_each_modality_has_its_god_and_movement():
    """"Movable signs are governed by Brahma. Fixed signs are governed by
    Shiva. Dual signs are govenred by Vishnu.\""""
    assert MOVEMENTS["chara"]["god"] == "Brahma"
    assert MOVEMENTS["sthira"]["god"] == "Shiva"
    assert MOVEMENTS["dwiswabhava"]["god"] == "Vishnu"
    assert MOVEMENTS["chara"]["movement"] == "regular"
    assert MOVEMENTS["sthira"]["movement"] == "sixth"
    assert MOVEMENTS["dwiswabhava"]["movement"] == "trinal"

    for sign in range(12):
        modality = str(MODALITY_NAMES[RASI_MODALITY[sign]])
        assert movement_of(sign) is MOVEMENTS[modality]


def test_brahmas_regular_movement():
    """"the regular movement of 1st, 2nd, 3rd etc.\""""
    assert house_order(R["Aries"]) == tuple(range(1, 13))


def test_shivas_sixth_movement():
    """"We take dasa seed, 6th from there, 6th from there and so on.\""""
    assert house_order(R["Taurus"]) == (1, 6, 11, 4, 9, 2, 7, 12, 5, 10, 3, 8)


def test_vishnus_trinal_movement_matches_the_six_houses_printed():
    """"1st, 5th, 9th, then 10th, 2nd, 6th and so on."

    The section prints six and leaves the rest to "and so on". Taking each
    next quadrant as the 10th from the previous reproduces those six; the last
    six are our inference and are marked as such in the module.
    """
    order = house_order(R["Gemini"])
    assert order[:6] == (1, 5, 9, 10, 2, 6)
    assert order == (1, 5, 9, 10, 2, 6, 7, 11, 3, 4, 8, 12)


@pytest.mark.parametrize("sign", range(12))
def test_every_movement_visits_each_house_exactly_once(sign):
    """A movement that repeated or skipped a house would give one rasi two
    dasas and another none."""
    assert sorted(house_order(sign)) == list(range(1, 13))


@pytest.mark.parametrize("sign", range(12))
def test_every_progression_gives_each_rasi_exactly_one_dasa(sign):
    got = progression(sign)
    assert sorted(got.signs) == list(range(12))
    assert got.signs[0] == sign                    # the seed takes the first
    assert len(got.signs) == 12


def test_the_direction_comes_from_the_ninth_house_from_the_seed():
    """"If the 9th house from dasa seed is an odd-footed sign... the direction
    is forward... even-footed... backward."

    The 9th is counted zodiacally, because the direction is what it decides
    and so cannot also depend on it.
    """
    for sign in range(12):
        ninth = (sign + 8) % 12
        expected = "forward" if RASI_IS_ODD_FOOTED[ninth] else "backward"
        assert direction_of(sign) == expected
        assert progression(sign).ninth_from_seed == ninth


def test_both_directions_actually_occur():
    """Six seeds each way. A rule that always returned one answer would pass
    the test above and still be wrong."""
    tally = Counter(direction_of(sign) for sign in range(12))
    assert tally == {"forward": 6, "backward": 6}


@pytest.mark.parametrize(
    "seed,expected",
    [
        # Taurus is fixed, so Shiva's 6th movement; its 9th is Capricorn,
        # even-footed, so backward. 1st, 6th, 11th, 4th counted backwards.
        ("Taurus", ["Taurus", "Sagittarius", "Cancer", "Aquarius"]),
        # Gemini is dual, so Vishnu's trines; its 9th is Aquarius, backward.
        ("Gemini", ["Gemini", "Aquarius", "Libra", "Virgo"]),
        # Aries is movable and forward, so the plain zodiacal order.
        ("Aries", ["Aries", "Taurus", "Gemini", "Cancer"]),
    ],
)
def test_worked_progressions_by_hand(seed, expected):
    """Three seeds worked out by hand, one per movement, covering both
    directions — the arithmetic is easy to get subtly wrong."""
    assert list(progression(R[seed]).sign_names[:4]) == expected


def test_a_backward_progression_is_the_forward_one_mirrored():
    """Direction only reflects the house-to-sign mapping; it must not disturb
    which houses the movement visits."""
    for sign in range(12):
        got = progression(sign)
        step = 1 if got.direction == "forward" else -1
        for house, rasi in zip(got.houses, got.signs):
            assert rasi == (sign + step * (house - 1)) % 12


def test_the_seed_is_the_stronger_of_lagna_and_the_seventh():
    """"Dasas start from lagna or the 7th house, whichever is stronger. We use
    the rules of strength explained in the chapter 'Strength of Planets and
    Rasis'." That chapter is §15.5.2, and Narayana is phalita.
    """
    from hora.charts.book import graha_longitudes, lagna
    from hora.dasha.rasi.narayana import dasa_seed

    for number in (6, 17, 23):
        longitudes = {int(g): lon for g, lon in graha_longitudes(number).items()}
        got = dasa_seed(lagna(number), longitudes)
        assert got["seventh"] == (got["lagna"] + 6) % 12
        assert got["seed"] in (got["lagna"], got["seventh"])
        assert got["decided_by"]


def test_an_undecidable_seed_is_reported_rather_than_guessed():
    """§15.5.2's cascade can run out, and Narayana must not default to lagna
    when it does.

    Rules 1 to 3 read only which rasi holds a graha, so they survive a partial
    chart; rule 4 onwards needs the lords' own longitudes. Given none, the
    cascade now stops there and names the grahas it wanted, where it used to
    raise a bare KeyError from inside chapter 15's module.
    """
    from hora.dasha.rasi.narayana import dasa_seed

    got = dasa_seed(0, {})
    assert got["seed"] is None
    assert got["seed_name"] is None
    assert "rule 4 needs the longitude" in got["reason"]
    assert "Mars" in got["reason"] and "Venus" in got["reason"]
