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


# --------------------------------------------------------------------------
# Examples 63, 64 and 65 — one per movement, between them both directions.
# --------------------------------------------------------------------------

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
BY_ABBR = {a: i for i, a in enumerate(ABBR)}


@pytest.mark.parametrize(
    "seed,god,movement,ninth,direction,sequence",
    [
        # Example 63: fixed seed, Shiva's 6th movement, backward.
        ("Sc", "Shiva", "sixth", "Cn", "backward",
         "Sc Ge Cp Le Pi Li Ta Sg Cn Aq Vi Ar"),
        # Example 64: dual seed, Vishnu's trines, forward.
        ("Pi", "Vishnu", "trinal", "Sc", "forward",
         "Pi Cn Sc Sg Ar Le Vi Cp Ta Ge Li Aq"),
        # Example 65: movable seed, Brahma's regular order, backward.
        ("Cp", "Brahma", "regular", "Vi", "backward",
         "Cp Sg Sc Li Vi Le Cn Ge Ta Ar Pi Aq"),
    ],
)
def test_the_three_worked_progressions(seed, god, movement, ninth, direction,
                                       sequence):
    """Examples 63, 64 and 65, each checked on all twelve rasis rather than
    the first few — the movements diverge late as well as early."""
    got = progression(BY_ABBR[seed])
    assert got.god == god
    assert got.movement == movement
    assert ABBR[got.ninth_from_seed] == ninth
    assert got.direction == direction
    assert " ".join(ABBR[s] for s in got.signs) == sequence


def test_example_64_settles_vishnus_quadrant_order():
    """§18.2.1 stops at "1st, 5th, 9th, then 10th, 2nd, 6th and so on", which
    leaves the quadrants after the 10th open. Example 64 states them:

        "then count the same houses from the 10th house, then from the 7th
        house and finally from the 4th house"

    So the quadrants run 1, 10, 7, 4 — each the 10th from the last — and the
    module's continuation was right rather than merely consistent.
    """
    from hora.dasha.rasi.narayana import VISHNU_QUADRANT_ORDER

    assert "from the 10th house, then from the 7th house and finally from" \
        in VISHNU_QUADRANT_ORDER

    quadrant_starts = house_order(BY_ABBR["Pi"])[::3]
    assert quadrant_starts == (1, 10, 7, 4)


def test_example_64s_two_named_trine_groups():
    """"Trines from Pi are Pi, Cn and Sc. Trines from the 10th (Sg) are Sg,
    Ar and Le." Both groups are named outright, so both are checked."""
    got = progression(BY_ABBR["Pi"])
    names = [ABBR[s] for s in got.signs]
    assert names[0:3] == ["Pi", "Cn", "Sc"]
    assert names[3:6] == ["Sg", "Ar", "Le"]


def test_the_three_examples_cover_every_movement_and_both_directions():
    """Between them the examples exercise all three gods and both directions,
    which is why they can settle the module rather than merely sample it."""
    seeds = [BY_ABBR[s] for s in ("Sc", "Pi", "Cp")]
    assert {progression(s).god for s in seeds} == {"Brahma", "Shiva", "Vishnu"}
    assert {progression(s).direction for s in seeds} == {"forward", "backward"}


# --------------------------------------------------------------------------
# §18.2.1's two seed exceptions
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "seed,opening",
    [("Sc", "Sc Sg Cp Aq Pi Ar"), ("Pi", "Pi Ar Ta Ge Cn Le")],
)
def test_the_saturn_exception(seed, opening):
    """"If Saturn occupies dasa seed, dasa progression becomes regular and
    zodiacal... We basically make the direction 'forward' and use Brahma's
    progression."

    It overrides both halves at once. Scorpio is fixed and Pisces dual, so
    without the exception neither would take Brahma's movement, and both
    would run backward or forward by their own 9th house.
    """
    from hora.core.const import Graha

    got = progression(BY_ABBR[seed], {int(Graha.SATURN)})
    assert got.exception == "Saturn"
    assert got.god == "Brahma"
    assert got.movement == "regular"
    assert got.direction == "forward"
    assert " ".join(ABBR[s] for s in got.signs[:6]) == opening
    assert got.houses == tuple(range(1, 13))


@pytest.mark.parametrize(
    "seed,opening",
    [("Sc", "Sc Ar Vi Aq Cn Sg"), ("Pi", "Pi Sc Cn Ge Aq Li")],
)
def test_the_ketu_exception(seed, opening):
    """"If Ketu occupies dasa seed, the basic direction of dasa progression
    becomes reversed."

    Only the direction. The section makes the point itself by pairing each
    case with an earlier example: Scorpio's 6th house is now counted forward
    where Example 63 counted it backward, and Pisces' trines are counted
    backward where Example 64 counted them forward.
    """
    from hora.core.const import Graha

    plain = progression(BY_ABBR[seed])
    got = progression(BY_ABBR[seed], {int(Graha.KETU)})

    assert got.exception == "Ketu"
    assert got.movement == plain.movement          # movement is untouched
    assert got.houses == plain.houses
    assert got.direction != plain.direction        # only the direction flips
    assert " ".join(ABBR[s] for s in got.signs[:6]) == opening


def test_the_ketu_exception_inverts_the_examples_it_is_compared_with():
    """The section invites the comparison, so it is made: with Ketu in the
    seed each progression is the earlier example's, mirrored about it."""
    from hora.core.const import Graha

    for seed in ("Sc", "Pi"):
        plain = progression(BY_ABBR[seed])
        flipped = progression(BY_ABBR[seed], {int(Graha.KETU)})
        for house, plain_sign, flipped_sign in zip(
                plain.houses, plain.signs, flipped.signs):
            offset = house - 1
            assert plain_sign == (BY_ABBR[seed] + offset * (
                1 if plain.direction == "forward" else -1)) % 12
            assert flipped_sign == (BY_ABBR[seed] - offset * (
                1 if plain.direction == "forward" else -1)) % 12


def test_no_exception_applies_when_the_seed_is_not_named(): 
    """Both exceptions turn on who occupies the seed, so a caller who does not
    say cannot have either applied to them."""
    for seed in range(12):
        assert progression(seed).exception is None
        assert progression(seed, set()).exception is None
        assert progression(seed, occupants=None).exception is None


def test_other_grahas_in_the_seed_change_nothing():
    """Only Saturn and Ketu are named. A seed full of everything else must
    give the plain progression."""
    from hora.core.const import Graha

    others = {int(g) for g in (Graha.SUN, Graha.MOON, Graha.MARS,
                               Graha.MERCURY, Graha.JUPITER, Graha.VENUS,
                               Graha.RAHU)}
    for seed in range(12):
        assert progression(seed, others).signs == progression(seed).signs


def test_a_seed_holding_both_saturn_and_ketu_is_refused():
    """See OI-120. Saturn imposes forward; Ketu reverses whatever the
    direction would be. §18.2.1 never says which acts on the other, and no
    example shows a seed with both, so this is reported rather than resolved.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import BOTH_EXCEPTIONS_UNDEFINED, NarayanaError

    with pytest.raises(NarayanaError, match="both Saturn and Ketu"):
        progression(BY_ABBR["Sc"], {int(Graha.SATURN), int(Graha.KETU)})

    assert "never says" in BOTH_EXCEPTIONS_UNDEFINED


def test_the_two_exceptions_override_different_things():
    """Saturn replaces the movement and fixes the direction; Ketu touches only
    the direction. That asymmetry is why they compose rather than conflict,
    and why the collision above is ambiguous rather than merely undecided.
    """
    from hora.dasha.rasi.narayana import SEED_EXCEPTIONS

    assert SEED_EXCEPTIONS["Saturn"]["overrides"] == ("movement", "direction")
    assert SEED_EXCEPTIONS["Ketu"]["overrides"] == ("direction",)
