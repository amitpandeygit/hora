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


# --------------------------------------------------------------------------
# Table 40 — every seed against every case, as printed.
# --------------------------------------------------------------------------

#: Table 40 verbatim: twelve seeds, each with (a) the normal progression,
#: (b) the Saturn exception and (c) the Ketu exception. It is kept here rather
#: than in `core/constants` because it is derivable from §18.2.1's rules — it
#: is the book's check on our arithmetic, not an input to it, and holding it
#: as a constant would make two sources of truth for one thing.
TABLE_40: dict[str, dict[str, str]] = {
    "Ar": {"a": "Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi",
           "b": "Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi",
           "c": "Ar Pi Aq Cp Sg Sc Li Vi Le Cn Ge Ta"},
    "Ta": {"a": "Ta Sg Cn Aq Vi Ar Sc Ge Cp Le Pi Li",
           "b": "Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi Ar",
           "c": "Ta Li Pi Le Cp Ge Sc Ar Vi Aq Cn Sg"},
    "Ge": {"a": "Ge Aq Li Vi Ta Cp Sg Le Ar Pi Sc Cn",
           "b": "Ge Cn Le Vi Li Sc Sg Cp Aq Pi Ar Ta",
           "c": "Ge Li Aq Pi Cn Sc Sg Ar Le Vi Cp Ta"},
    "Cn": {"a": "Cn Ge Ta Ar Pi Aq Cp Sg Sc Li Vi Le",
           "b": "Cn Le Vi Li Sc Sg Cp Aq Pi Ar Ta Ge",
           "c": "Cn Le Vi Li Sc Sg Cp Aq Pi Ar Ta Ge"},
    "Le": {"a": "Le Cp Ge Sc Ar Vi Aq Cn Sg Ta Li Pi",
           "b": "Le Vi Li Sc Sg Cp Aq Pi Ar Ta Ge Cn",
           "c": "Le Pi Li Ta Sg Cn Aq Vi Ar Sc Ge Cp"},
    "Vi": {"a": "Vi Cp Ta Ge Li Aq Pi Cn Sc Sg Ar Le",
           "b": "Vi Li Sc Sg Cp Aq Pi Ar Ta Ge Cn Le",
           "c": "Vi Ta Cp Sg Le Ar Pi Sc Cn Ge Aq Li"},
    "Li": {"a": "Li Sc Sg Cp Aq Pi Ar Ta Ge Cn Le Vi",
           "b": "Li Sc Sg Cp Aq Pi Ar Ta Ge Cn Le Vi",
           "c": "Li Vi Le Cn Ge Ta Ar Pi Aq Cp Sg Sc"},
    "Sc": {"a": "Sc Ge Cp Le Pi Li Ta Sg Cn Aq Vi Ar",
           "b": "Sc Sg Cp Aq Pi Ar Ta Ge Cn Le Vi Li",
           "c": "Sc Ar Vi Aq Cn Sg Ta Li Pi Le Cp Ge"},
    "Sg": {"a": "Sg Le Ar Pi Sc Cn Ge Aq Li Vi Ta Cp",
           "b": "Sg Cp Aq Pi Ar Ta Ge Cn Le Vi Li Sc",
           "c": "Sg Ar Le Vi Cp Ta Ge Li Aq Pi Cn Sc"},
    "Cp": {"a": "Cp Sg Sc Li Vi Le Cn Ge Ta Ar Pi Aq",
           "b": "Cp Aq Pi Ar Ta Ge Cn Le Vi Li Sc Sg",
           "c": "Cp Aq Pi Ar Ta Ge Cn Le Vi Li Sc Sg"},
    "Aq": {"a": "Aq Cn Sg Ta Li Pi Le Cp Ge Sc Ar Vi",
           "b": "Aq Pi Ar Ta Ge Cn Le Vi Li Sc Sg Cp",
           "c": "Aq Vi Ar Sc Ge Cp Le Pi Li Ta Sg Cn"},
    "Pi": {"a": "Pi Cn Sc Sg Ar Le Vi Cp Ta Ge Li Aq",
           "b": "Pi Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq",
           "c": "Pi Sc Cn Ge Aq Li Vi Ta Cp Sg Le Ar"},
}

#: "If neither Saturn nor Ketu occupies dasa seed, we should use the normal
#: progression. If Saturn occupies dasa seed, we should apply the Saturn
#: exception. If Ketu occupies dasa seed, we should apply the Ketu exception."
_CASE_OCCUPANTS = {"a": None, "b": {6}, "c": {8}}      # Saturn is 6, Ketu 8


def test_table_40_is_internally_consistent():
    """Before comparing anything: every row must list all twelve signs once
    and open on its own seed. A transcription slip would otherwise be read as
    a defect in the engine."""
    assert len(TABLE_40) == 12
    for seed, cases in TABLE_40.items():
        assert set(cases) == {"a", "b", "c"}
        for case, sequence in cases.items():
            signs = sequence.split()
            assert len(signs) == 12, (seed, case)
            assert sorted(signs) == sorted(ABBR), (seed, case)
            assert signs[0] == seed, (seed, case)


@pytest.mark.parametrize("seed", sorted(TABLE_40))
@pytest.mark.parametrize("case", ["a", "b", "c"])
def test_table_40(seed, case):
    """All twelve seeds against all three cases — 36 sequences, 432 signs."""
    got = progression(BY_ABBR[seed], _CASE_OCCUPANTS[case])
    assert " ".join(ABBR[s] for s in got.signs) == TABLE_40[seed][case]


def test_the_saturn_column_is_the_plain_zodiac_from_every_seed():
    """Column (b) should be twelve rotations of the zodiac and nothing else,
    since the exception forces Brahma's movement and a forward direction."""
    for seed, cases in TABLE_40.items():
        start = BY_ABBR[seed]
        expected = " ".join(ABBR[(start + k) % 12] for k in range(12))
        assert cases["b"] == expected, seed


def test_the_rows_where_two_cases_coincide_are_the_movable_seeds():
    """Table 40 has four rows where two cases are identical, and each follows
    from the rules rather than being a coincidence to memorise.

    Aries and Libra are movable and already run forward, so Saturn — which
    imposes exactly those two things — changes nothing and (a) equals (b).
    Cancer and Capricorn are movable but run backward, so their movement is
    already regular and Ketu's flip to forward lands on Saturn's own result,
    making (b) equal (c). No row has (a) equal to (c), which would mean Ketu
    had failed to reverse anything.
    """
    same_ab = {s for s, c in TABLE_40.items() if c["a"] == c["b"]}
    same_bc = {s for s, c in TABLE_40.items() if c["b"] == c["c"]}
    same_ac = {s for s, c in TABLE_40.items() if c["a"] == c["c"]}

    assert same_ab == {"Ar", "Li"}
    assert same_bc == {"Cn", "Cp"}
    assert same_ac == set()

    for seed in same_ab:
        assert movement_of(BY_ABBR[seed])["modality"] == "movable"
        assert direction_of(BY_ABBR[seed]) == "forward"
    for seed in same_bc:
        assert movement_of(BY_ABBR[seed])["modality"] == "movable"
        assert direction_of(BY_ABBR[seed]) == "backward"

    # Between them they are exactly the four movable signs.
    assert same_ab | same_bc == {"Ar", "Cn", "Li", "Cp"}


def test_the_three_examples_agree_with_table_40():
    """Examples 63, 64 and 65 give normal progressions for Sc, Pi and Cp, and
    the table gives the same three. Two independent printings of one fact."""
    assert TABLE_40["Sc"]["a"] == "Sc Ge Cp Le Pi Li Ta Sg Cn Aq Vi Ar"
    assert TABLE_40["Pi"]["a"] == "Pi Cn Sc Sg Ar Le Vi Cp Ta Ge Li Aq"
    assert TABLE_40["Cp"]["a"] == "Cp Sg Sc Li Vi Le Cn Ge Ta Ar Pi Aq"


def test_the_exception_examples_agree_with_table_40():
    """The Saturn and Ketu paragraphs print four openings, and Table 40
    prints the same four in full."""
    assert TABLE_40["Sc"]["b"].startswith("Sc Sg Cp Aq Pi Ar")
    assert TABLE_40["Pi"]["b"].startswith("Pi Ar Ta Ge Cn Le")
    assert TABLE_40["Sc"]["c"].startswith("Sc Ar Vi Aq Cn Sg")
    assert TABLE_40["Pi"]["c"].startswith("Pi Sc Cn Ge Aq Li")


# --------------------------------------------------------------------------
# §18.2.2 Dasa Length
# --------------------------------------------------------------------------


def test_the_counting_direction_is_the_dasa_rasis_not_the_seeds():
    """§18.2.2: "Counting is forward if dasa rasi is odd-footed."

    §18.2.1's direction came from the 9th house from the *seed* and governs
    the whole progression; this one is per dasa rasi and governs only its own
    length. Conflating them would be easy and silent, so both are asserted
    against each other here.
    """
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    for rasi in range(12):
        got = dasa_length(rasi, int(RASI_LORD[rasi]), rasi)
        expected = "forward" if RASI_IS_ODD_FOOTED[rasi] else "backward"
        assert got.counting == expected

    # Aries: the progression runs forward, but Cancer's own length counts back.
    assert progression(R["Aries"]).direction == "forward"
    assert dasa_length(R["Cancer"], 1, 1).counting == "backward"


@pytest.mark.parametrize("rasi", range(12))
def test_a_rasi_holding_its_own_lord_gives_twelve_years(rasi):
    """Exception 1: "we get zero by subtracting one from one. However, dasa
    length becomes 12 years then." Zero would silently drop the period."""
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    got = dasa_length(rasi, int(RASI_LORD[rasi]), rasi)
    assert got.count == 1
    assert got.years == 12
    assert "12 rather than 0" in got.applied[0]


def test_exaltation_adds_a_year_and_debilitation_takes_one():
    """Exceptions 2 and 3, against the same placement with no dignity given."""
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    # Aries is odd-footed, so forward: Ar, Ta, Ge, Cn is a count of four,
    # and four less one is three years.
    plain = dasa_length(R["Aries"], int(Graha.MARS), R["Cancer"])
    assert plain.count == 4
    assert plain.years == 3 and plain.applied == ()

    assert dasa_length(R["Aries"], int(Graha.MARS), R["Cancer"],
                       "exalted").years == 4
    assert dasa_length(R["Aries"], int(Graha.MARS), R["Cancer"],
                       "debilitated").years == 2


def test_an_unstated_dignity_fires_neither_exception():
    """Omitting the dignity must not be read as "neither exalted nor
    debilitated" by accident — it happens to give the same number, so the
    test checks that no exception was recorded as applied."""
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    got = dasa_length(R["Aries"], int(Graha.MARS), R["Cancer"], None)
    assert got.applied == ()
    for dignity in ("own", "moolatrikona", "friend", "neutral", "enemy"):
        assert dasa_length(R["Aries"], int(Graha.MARS), R["Cancer"],
                           dignity).years == got.years


def test_the_base_rule_spans_one_to_twelve_years():
    """Every count from 1 to 12 must give a usable length, and the twelve
    lengths must be distinct — a dasa of 0 would drop a rasi from the cycle."""
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    years = {dasa_length(R["Aries"], int(Graha.MARS), place).years
             for place in range(12)}
    assert years == set(range(1, 13))


def test_the_second_cycle_is_twelve_less_the_first():
    """Special note 2. A 12-year first dasa gives none in the second, which is
    ordinary rather than an error."""
    from hora.dasha.rasi.narayana import second_cycle_length

    assert second_cycle_length(1) == 11
    assert second_cycle_length(7) == 5
    assert second_cycle_length(12) == 0


def test_scorpio_and_aquarius_need_the_stronger_lord():
    """Special note 1: "If dasa rasi is Aq or Sc, it has two lords. We should
    take the stronger lord when computing Narayana dasa."

    The function takes the lord as given, so the caller resolves it — the same
    §15.5.1 cascade the dasa seed uses. Both co-lords give different lengths
    from the same chart, which is why the choice cannot be skipped.
    """
    from hora.charts.colord import CO_LORDS
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    assert set(CO_LORDS[R["Scorpio"]]) == {int(Graha.MARS), int(Graha.KETU)}
    assert set(CO_LORDS[R["Aquarius"]]) == {int(Graha.SATURN), int(Graha.RAHU)}

    mars = dasa_length(R["Scorpio"], int(Graha.MARS), R["Aries"])
    ketu = dasa_length(R["Scorpio"], int(Graha.KETU), R["Cancer"])
    assert mars.years != ketu.years


def test_the_two_reachable_out_of_range_lengths_are_flagged():
    """See OI-121. The exceptions can carry a length outside the 1-to-12 the
    base rule allows, and §18.2.2 does not say whether they may combine.

    Only two such cases are reachable, because the lord must actually exalt or
    debilitate where the count puts it. Virgo is the only rasi a planet both
    owns and exalts in, which is what lets exceptions 1 and 2 meet at all.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length, second_cycle_length

    virgo = dasa_length(R["Virgo"], int(Graha.MERCURY), R["Virgo"], "exalted")
    assert virgo.count == 1
    assert virgo.years == 13
    assert virgo.out_of_range is not None
    assert second_cycle_length(virgo.years) == -1

    sagittarius = dasa_length(R["Sagittarius"], int(Graha.JUPITER),
                              R["Capricorn"], "debilitated")
    assert sagittarius.count == 2
    assert sagittarius.years == 0
    assert sagittarius.out_of_range is not None


def test_ordinary_lengths_carry_no_flag():
    """The flag must be rare, or it says nothing. Every length the base rule
    gives, with or without a dignity that keeps it in range, is unflagged."""
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    for rasi in range(12):
        for place in range(12):
            got = dasa_length(rasi, int(RASI_LORD[rasi]), place)
            assert got.out_of_range is None, (rasi, place)


# --------------------------------------------------------------------------
# Example 66 — Narayana dasa worked in full over Chart 23.
# --------------------------------------------------------------------------

#: The twelve lengths the example prints, in progression order.
EX66_LENGTHS = [("Le", 1), ("Cp", 8), ("Ge", 2), ("Sc", 9), ("Ar", 4),
                ("Vi", 1), ("Aq", 9), ("Cn", 3), ("Sg", 11), ("Ta", 3),
                ("Li", 10), ("Pi", 4)]


def _chart_23():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(23).items()},
            {int(g): sign for g, sign in graha_signs(23).items()},
            lagna(23))


def test_example_66_seed_and_progression():
    """"Because the 7th house (Le) is stronger than lagna (Aq), dasa seed is
    Le... Neither Saturn nor Ketu occupies Le and the exceptions don't apply.
    Dasa sequence is — Le, Cp, Ge, Sc, Ar, Vi, Aq, Cn, Sg, Ta, Li, Pi."
    """
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign = _chart_23()
    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["lagna_name"] == "Aquarius"
    assert seed["seventh_name"] == "Leo"
    assert seed["seed"] == R["Leo"]

    occupants = {g for g, sign in signs.items() if sign == seed["seed"]}
    from hora.core.const import Graha
    assert int(Graha.SATURN) not in occupants
    assert int(Graha.KETU) not in occupants

    got = progression(seed["seed"], occupants)
    assert got.exception is None
    assert got.god == "Shiva"
    assert got.direction == "forward"
    assert " ".join(ABBR[s] for s in got.signs) == \
        "Le Cp Ge Sc Ar Vi Aq Cn Sg Ta Li Pi"


def test_example_66_uses_the_stronger_lord_for_the_two_co_owned_rasis():
    """Special note 1. The example counts Scorpio to Mars and Aquarius to
    Saturn, which is what §15.5.1's cascade gives for this chart."""
    from hora.charts.colord import stronger
    from hora.core.const import Graha

    longitudes, _signs, _lagna = _chart_23()
    assert stronger(R["Scorpio"], longitudes, purpose="arudha").winner == \
        int(Graha.MARS)
    assert stronger(R["Aquarius"], longitudes, purpose="arudha").winner == \
        int(Graha.SATURN)


@pytest.mark.parametrize("abbr,years", [c for c in EX66_LENGTHS if c[0] != "Cn"])
def test_example_66_lengths(abbr, years):
    """Eleven of the twelve, each with its own counting direction and count.
    Cancer is the exception and is tested separately — see D-52.
    """
    from hora.charts.colord import stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_23()
    rasi = BY_ABBR[abbr]
    lord = (stronger(rasi, longitudes, purpose="arudha").winner
            if rasi in (R["Scorpio"], R["Aquarius"]) else int(RASI_LORD[rasi]))
    got = dasa_length(rasi, lord, signs[lord], sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why


def test_example_66_cancer_turns_on_what_exalted_means():
    """See D-52. "However, Moon is exalted and we add one year. We get 2+1=3."

    The Moon is at 23 Ta 38. Taurus is his exaltation sign, but his exaltation
    degree is 3 and his moolatrikona runs from there to the sign's end, so
    `sign_dignity` says moolatrikona and the year is not added. Both readings
    are reachable; which one §18.2.2 means is the open question.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_23()
    moon = int(Graha.MOON)
    assert int(RASI_LORD[R["Cancer"]]) == moon
    assert signs[moon] == R["Taurus"]
    assert sign_dignity(moon, longitudes[moon]) == "moolatrikona"

    by_degree = dasa_length(R["Cancer"], moon, signs[moon], "moolatrikona")
    assert by_degree.count == 3
    assert by_degree.years == 2                    # ours

    by_sign = dasa_length(R["Cancer"], moon, signs[moon], "exalted")
    assert by_sign.years == 3                      # the book's
    assert "exalted" in by_sign.applied[0]


def test_example_66_first_cycle_totals_sixty_five_years_the_books_way():
    """"Thus the first cycle of dasas ends in Aug 1977", from a birth in
    August 1912 — sixty-five years. Ours totals sixty-four, the whole
    difference being Cancer's one year.
    """
    assert sum(years for _abbr, years in EX66_LENGTHS) == 65
    ours = [(a, 2 if a == "Cn" else y) for a, y in EX66_LENGTHS]
    assert sum(y for _a, y in ours) == 64


def test_example_66_the_dates_the_example_prints():
    """Each dasa runs from the last one's end, so the printed dates are a
    running total and check the lengths a second way."""
    starts, year = {}, 1912
    for abbr, years in EX66_LENGTHS:
        starts[abbr] = (year, year + years)
        year += years

    assert starts["Le"] == (1912, 1913)
    assert starts["Cp"] == (1913, 1921)
    assert starts["Ge"] == (1921, 1923)
    assert starts["Sc"] == (1923, 1932)
    assert starts["Ar"] == (1932, 1936)
    assert starts["Vi"] == (1936, 1937)
    assert starts["Aq"] == (1937, 1946)
    assert starts["Cn"] == (1946, 1949)
    assert starts["Sg"] == (1949, 1960)
    assert starts["Ta"] == (1960, 1963)
    assert starts["Li"] == (1963, 1973)
    assert starts["Pi"] == (1973, 1977)


def test_example_66_second_cycle():
    """"Because Le dasa is of 1 year in the 1st cycle, it is 12-1=11 years in
    the 2nd cycle... Cp 12-8=4... Ge 12-2=10." The order repeats unchanged.
    """
    from hora.dasha.rasi.narayana import second_cycle_length

    assert second_cycle_length(1) == 11             # Leo, Aug 1977 to Aug 1988
    assert second_cycle_length(8) == 4              # Capricorn, to Aug 1992
    assert second_cycle_length(2) == 10             # Gemini, to Aug 2002

    year = 1977
    for abbr, first in EX66_LENGTHS[:3]:
        year += second_cycle_length(first)
    assert year == 2002


# --------------------------------------------------------------------------
# Exercise 27 — Chart 21, and the first real chart the Ketu exception fires on.
# --------------------------------------------------------------------------

#: The exercise's twelve first-cycle dasas, in order, with their lengths.
EX27_FIRST = [("Aq", 2), ("Vi", 11), ("Ar", 2), ("Sc", 3), ("Ge", 4),
              ("Cp", 1), ("Le", 9), ("Pi", 3), ("Li", 2), ("Ta", 7),
              ("Sg", 12), ("Cn", 5)]

#: The eight second-cycle dasas it prints before stopping at paramayush.
EX27_SECOND = [("Aq", 10), ("Vi", 1), ("Ar", 10), ("Sc", 9), ("Ge", 8),
               ("Cp", 11), ("Le", 3), ("Pi", 9)]


def _chart_21():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(21).items()},
            {int(g): sign for g, sign in graha_signs(21).items()},
            lagna(21))


def test_exercise_27_seed_is_the_seventh_for_holding_more_planets():
    """"The 7th house has 2 planets and lagna has only one. So the 7th house
    acts as dasa seed." That is §15.5.2's rule 1."""
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign = _chart_21()
    assert lagna_sign == R["Leo"]
    assert len([g for g, s in signs.items() if s == R["Leo"]]) == 1
    assert len([g for g, s in signs.items() if s == R["Aquarius"]]) == 2

    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["seed"] == R["Aquarius"]
    assert seed["decided_by"] == "1"


def test_exercise_27_hints_agree_with_section_15_5_1():
    """"Saturn is the stronger lord of Aq and Ketu is the stronger lord of
    Sc." The exercise gives these as hints; our cascade derives them."""
    from hora.charts.colord import stronger
    from hora.core.const import Graha

    longitudes, _signs, _lagna = _chart_21()
    assert stronger(R["Aquarius"], longitudes,
                    purpose="arudha").winner == int(Graha.SATURN)
    assert stronger(R["Scorpio"], longitudes,
                    purpose="arudha").winner == int(Graha.KETU)


def test_exercise_27_ketu_reverses_the_direction():
    """"Because Li (9th from Aq) is odd-footed, direction is normally
    'forward'. But Ketu's presence in Aq reverses it and makes it 'backward'."

    The first chart where the Ketu exception fires on real placements rather
    than a constructed one.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import progression

    _longitudes, signs, _lagna = _chart_21()
    seed = R["Aquarius"]
    occupants = {g for g, s in signs.items() if s == seed}
    assert int(Graha.KETU) in occupants

    got = progression(seed, occupants)
    assert got.exception == "Ketu"
    assert got.ninth_from_seed == R["Libra"]
    assert RASI_IS_ODD_FOOTED[got.ninth_from_seed]
    assert progression(seed).direction == "forward"      # without Ketu
    assert got.direction == "backward"                   # with him
    assert " ".join(ABBR[s] for s in got.signs) == \
        "Aq Vi Ar Sc Ge Cp Le Pi Li Ta Sg Cn"


@pytest.mark.parametrize("abbr,years", EX27_FIRST)
def test_exercise_27_first_cycle_lengths(abbr, years):
    """All twelve, each with its own counting direction and count."""
    from hora.charts.colord import stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_21()
    rasi = BY_ABBR[abbr]
    lord = (stronger(rasi, longitudes, purpose="arudha").winner
            if rasi in (R["Scorpio"], R["Aquarius"]) else int(RASI_LORD[rasi]))
    got = dasa_length(rasi, lord, signs[lord], sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why
    assert got.out_of_range is None


def test_exercise_27_sagittarius_holds_its_own_lord():
    """Sg's twelve years come from exception 1, not from a count of thirteen —
    Jupiter sits in Sagittarius, so the count is one and the exception turns
    the resulting zero into twelve. The first real chart to exercise it.
    """
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_length

    _longitudes, signs, _lagna = _chart_21()
    assert int(RASI_LORD[R["Sagittarius"]]) == int(Graha.JUPITER)
    assert signs[int(Graha.JUPITER)] == R["Sagittarius"]

    got = dasa_length(R["Sagittarius"], int(Graha.JUPITER), R["Sagittarius"])
    assert got.count == 1
    assert got.years == 12
    assert got.applied == ("contains its lord, so 12 rather than 0",)


def test_exercise_27_first_cycle_dates():
    """Nov 1960 to Nov 2021 — sixty-one years, checked as a running total."""
    assert sum(years for _abbr, years in EX27_FIRST) == 61

    year, dates = 1960, {}
    for abbr, years in EX27_FIRST:
        dates[abbr] = (year, year + years)
        year += years
    assert year == 2021

    assert dates["Aq"] == (1960, 1962)
    assert dates["Vi"] == (1962, 1973)
    assert dates["Le"] == (1983, 1992)
    assert dates["Sg"] == (2004, 2016)
    assert dates["Cn"] == (2016, 2021)


def test_exercise_27_second_cycle_dates():
    """Eight more, each 12 less its first-cycle length, ending Nov 2082."""
    from hora.dasha.rasi.narayana import second_cycle_length

    first = dict(EX27_FIRST)
    year = 2021
    for abbr, expected in EX27_SECOND:
        length = second_cycle_length(first[abbr])
        assert length == expected, abbr
        year += length
    assert year == 2082


def test_exercise_27_stops_past_paramayush_not_at_it():
    """"We stop here because 120 years is the paramayush of human beings."

    Nov 1960 plus 120 years is Nov 2080, and the list runs to Nov 2082 — the
    dasa straddling the limit is printed whole rather than cut at it.
    """
    from hora.dasha.rasi.narayana import second_cycle_length

    first = dict(EX27_FIRST)
    year = 1960 + sum(years for _a, years in EX27_FIRST)
    for abbr, _expected in EX27_SECOND[:-1]:
        year += second_cycle_length(first[abbr])
    assert year < 1960 + 120                       # the last dasa begins before
    year += second_cycle_length(first[EX27_SECOND[-1][0]])
    assert year > 1960 + 120                       # and ends after
    assert year == 2082


# --------------------------------------------------------------------------
# §18.3 Antardasas
# --------------------------------------------------------------------------


def _antardasa_inputs(chart_number):
    """A chart, with the co-lord resolution §18.3 needs when a seed is Sc/Aq."""
    from hora.charts.book import graha_longitudes
    from hora.charts.colord import stronger as co_lord

    longitudes = {int(g): lon for g, lon in graha_longitudes(chart_number).items()}
    stronger_co_lord = {r: co_lord(r, longitudes, purpose="arudha").winner
                        for r in (R["Scorpio"], R["Aquarius"])}
    return longitudes, stronger_co_lord


def _antardasas_for(chart_number, rasi, years=1):
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.narayana import antardasas

    longitudes, co_lords = _antardasa_inputs(chart_number)
    seed = stronger(rasi, (rasi + 6) % 12, longitudes, purpose="phalita").winner
    return antardasas(rasi, years, longitudes,
                      co_lords.get(seed) if seed in co_lords else None)


def test_a_dasa_of_n_years_gives_twelve_antardasas_of_n_months():
    """"If a dasa is of n years, then each antardasa in that dasa is for n
    months." Which closes exactly, a year being twelve months."""
    for years in (1, 2, 5, 11, 12):
        got = _antardasas_for(21, R["Aquarius"], years)
        assert len(got.signs) == 12
        assert got.months_each == years
        assert got.months_each * 12 == years * 12      # the dasa, in months


@pytest.mark.parametrize("rasi", range(12))
def test_every_dasas_antardasas_cover_the_twelve_rasis_once(rasi):
    assert sorted(_antardasas_for(21, rasi).signs) == list(range(12))


def test_the_antardasa_seed_is_the_stronger_of_the_dasa_rasi_and_its_seventh():
    """"Let us denote the stronger of dasa rasi and the 7th from it with the
    expression 'antardasa seed'." A second §15.5.2 comparison, per dasa —
    §18.2.1's seed compared lagna with the 7th from *lagna*.
    """
    for rasi in range(12):
        got = _antardasas_for(21, rasi)
        assert got.seed in (rasi, (rasi + 6) % 12)


def test_antardasas_begin_where_the_seeds_lord_sits_not_at_the_seed():
    """"Antardasas start from the rasi containing the lord of antardasa seed."

    The seed itself is not where they begin, and conflating the two would go
    unnoticed whenever a seed happens to hold its own lord.
    """
    from hora.core.const import RASI_LORD

    longitudes, _co_lords = _antardasa_inputs(23)
    moved = 0
    for rasi in range(12):
        got = _antardasas_for(23, rasi)
        lord = int(RASI_LORD[got.seed])
        if lord in longitudes:
            assert got.start == int(longitudes[lord] // 30)
            if got.start != got.seed:
                moved += 1
    assert moved, "no seed's lord sat outside it, so this proved nothing"


def test_the_direction_reads_odd_and_even_signs_not_odd_and_even_feet():
    """§18.3's own NOTE: "We are talking about odd and even signs here and
    *not* about odd-footed and even-footed signs."

    The two disagree on Taurus, Leo, Scorpio and Aquarius. Chart 23 supplies
    two of those as starting rasis, so the wrong rule would be caught rather
    than merely possible: Leo is an odd sign but even-footed, Scorpio an even
    sign but odd-footed, and each takes the direction its *sign* implies.
    """
    from hora.core.const import RASI_IS_ODD, RASI_IS_ODD_FOOTED

    starts = {}
    for rasi in range(12):
        got = _antardasas_for(23, rasi)
        starts.setdefault(got.start_name, got.direction)

    assert starts["Leo"] == "forward"
    assert RASI_IS_ODD[R["Leo"]] and not RASI_IS_ODD_FOOTED[R["Leo"]]

    assert starts["Scorpio"] == "backward"
    assert RASI_IS_ODD_FOOTED[R["Scorpio"]] and not RASI_IS_ODD[R["Scorpio"]]

    for name, direction in starts.items():
        odd = bool(RASI_IS_ODD[RASI_NAMES.index(name)])
        assert direction == ("forward" if odd else "backward"), name


def test_both_directions_arise_on_a_real_chart():
    """Chart 23 splits six and six. A chart giving only one direction would
    leave the rule half untested, which Chart 21 alone does."""
    from collections import Counter

    tally = Counter(_antardasas_for(23, rasi).direction for rasi in range(12))
    assert tally["forward"] == 6
    assert tally["backward"] == 6


def test_the_antardasa_movement_is_regular_unlike_the_dasa_progression():
    """"we take the 1st, 2nd, 3rd, 4th etc houses from there" — always the
    regular order, where §18.2.1's progression takes one of three movements
    from the seed's modality. Only the direction varies here.
    """
    for chart in (21, 23):
        for rasi in range(12):
            got = _antardasas_for(chart, rasi)
            step = 1 if got.direction == "forward" else -1
            expected = [(got.start + step * k) % 12 for k in range(12)]
            assert list(got.signs) == expected


def test_an_undecidable_antardasa_seed_is_refused():
    """§15.5.2 can run out of rules. When it does the antardasa seed is
    unknown, and guessing the dasa rasi would be invisible."""
    from hora.dasha.rasi.narayana import NarayanaError, antardasas

    with pytest.raises(NarayanaError, match="could not choose between"):
        antardasas(R["Aries"], 3, {})
