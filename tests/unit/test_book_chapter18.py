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


def test_exception_1_is_terminal_so_virgo_is_never_thirteen_years():
    """See OI-121, which Example 68 closes on this side.

    Virgo is the only rasi a planet both owns and exalts in, so it is the only
    place exceptions 1 and 2 can meet. Bill Gates has Mercury there, and the
    example prints Vi 12 years -- not 13. It needs that same Mercury exalted
    for its Ge dasa of 4 years, so the two cannot be told apart by what
    "exalted" means. Exception 1 simply ends the calculation.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length, second_cycle_length

    virgo = dasa_length(R["Virgo"], int(Graha.MERCURY), R["Virgo"], "exalted")
    assert virgo.count == 1
    assert virgo.years == 12
    assert virgo.applied == ("contains its lord, so 12 rather than 0",)
    assert virgo.out_of_range is None
    assert second_cycle_length(virgo.years) == 0


def test_a_debilitated_lord_can_still_leave_a_rasi_no_dasa():
    """The half of OI-121 that stays open. Exception 3 cannot meet exception
    1 -- a lord in its own sign is never debilitated there -- so it meets the
    base rule instead, and a count of 2 gives a dasa of no years at all.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

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


# --------------------------------------------------------------------------
# Example 67 — antardasas worked from stated positions, with the exceptions.
# --------------------------------------------------------------------------

#: Example 67 states positions rather than giving a chart: "Lords of Cp and Cn
#: are Saturn and Moon respectively. Suppose Saturn is in Le and Moon is in
#: Ta." The seed is Cancer, so the Moon's Taurus is where antardasas begin.
EX67_LONGITUDES = {6: 4 * 30 + 10.0, 1: 1 * 30 + 10.0}     # Saturn Le, Moon Ta


def _example_67(seed_occupants):
    """Example 67's antardasas, driven by its own stated positions.

    The example fixes the seed by fiat — "Let us say Cn is stronger than Cp" —
    so the strength comparison is short-circuited and only §18.3's counting is
    under test here.
    """
    from hora.core.const import RASI_IS_ODD

    start = int(EX67_LONGITUDES[1] // 30)          # where the Moon sits
    direction = "forward" if RASI_IS_ODD[start] else "backward"
    if 6 in seed_occupants:                        # Saturn in the seed
        direction = "forward"
    elif 8 in seed_occupants:                      # Ketu in the seed
        direction = "backward" if direction == "forward" else "forward"
    step = 1 if direction == "forward" else -1
    return direction, [ABBR[(start + step * k) % 12] for k in range(12)]


def test_example_67_normal_sequence():
    """"Then antardasas start from Ta, which contains Moon. Because Ta is an
    even sign, counting is backward. So antardasas go as — Ta, Ar, Pi, Aq, Cp,
    Sg, Sc, Li, Vi, Le, Cn and Ge."
    """
    direction, signs = _example_67(set())
    assert direction == "backward"
    assert " ".join(signs) == "Ta Ar Pi Aq Cp Sg Sc Li Vi Le Cn Ge"


def test_example_67_each_antardasa_is_five_months():
    """"Cp dasa of 5 years is running... Each antardasa is of 5 months."""
    from hora.dasha.rasi.narayana import antardasas

    got = antardasas(R["Capricorn"], 5, EX67_LONGITUDES, seed_lord=1)
    assert got.months_each == 5
    assert len(got.signs) == 12


def test_example_67_ketu_reverses_and_the_book_drops_a_sign():
    """See D-55. "antardasa sequence becomes Ta, Ge, Cn, Le, Vi, Li, Sc, Sg,
    Cp, Aq and Pi, if Ketu occupies Cn."

    Eleven signs are printed where twelve are required, §18.3 having opened by
    saying each dasa is divided into twelve. Counting forward from Taurus, the
    missing one is Aries.
    """
    printed = ["Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
    assert len(printed) == 11

    direction, signs = _example_67({8})            # Ketu in the seed
    assert direction == "forward"
    assert signs[:11] == printed
    assert signs[11] == "Ar"
    assert set(ABBR) - set(printed) == {"Ar"}


def test_example_67_saturn_forces_forward():
    """"If Saturn occupies antardasa seed rasi, antardasas go in the forward
    direction." Taurus would count backward on its own, so the exception is
    doing the work rather than agreeing by chance."""
    plain, _signs = _example_67(set())
    assert plain == "backward"

    direction, signs = _example_67({6})
    assert direction == "forward"
    assert " ".join(signs) == "Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi Ar"


def test_the_antardasa_exceptions_read_the_seed_not_the_starting_rasi():
    """"If Saturn occupies antardasa seed rasi..." — the seed, which is
    Cancer here, not Taurus where the antardasas begin. The two are different
    rasis whenever a seed's lord sits outside it, which is the usual case.
    """
    from hora.dasha.rasi.narayana import antardasas

    seed_has_ketu = antardasas(R["Capricorn"], 5, EX67_LONGITUDES,
                               seed_lord=1, seed_occupants={8})
    assert seed_has_ketu.exception == "Ketu"
    assert seed_has_ketu.start == R["Taurus"]      # where counting begins
    assert seed_has_ketu.start != seed_has_ketu.seed
    assert seed_has_ketu.direction == "forward"

    none = antardasas(R["Capricorn"], 5, EX67_LONGITUDES, seed_lord=1)
    assert none.exception is None
    assert none.direction == "backward"


def test_an_antardasa_seed_holding_both_saturn_and_ketu_is_refused():
    """The same ambiguity as §18.2.1's, and unresolved for the same reason —
    Saturn imposes forward, Ketu reverses whatever there is."""
    from hora.dasha.rasi.narayana import NarayanaError, antardasas

    with pytest.raises(NarayanaError, match="both Saturn and Ketu"):
        antardasas(R["Capricorn"], 5, EX67_LONGITUDES, seed_lord=1,
                   seed_occupants={6, 8})


def test_choosing_the_seed_by_comparing_lords_is_not_implemented():
    """Example 67 offers an alternative: "If Cp is stronger than Cn (or Saturn
    is much stronger than Moon)". No section grades strength by margin, and
    "much stronger" is unquantified, so the rasi comparison is used."""
    from hora.dasha.rasi.narayana import ANTARDASA_SEED_BY_LORDS_UNQUANTIFIED

    assert "much" in ANTARDASA_SEED_BY_LORDS_UNQUANTIFIED
    assert "we compare the rasis" in ANTARDASA_SEED_BY_LORDS_UNQUANTIFIED


# --------------------------------------------------------------------------
# §18.4 Interpretation
# --------------------------------------------------------------------------


def test_dasa_lagna_is_the_dasa_rasi_only_when_the_seed_was_lagna():
    """§18.4: "If dasas are started from the 7th house from lagna, then
    Narayana dasa gives the progression of the 7th house. So the 7th from dasa
    rasi gives the progressed lagna."

    The distinction is silent and six signs wide. Every principle in the
    section counts houses from the dasa lagna, so reading it from the dasa
    rasi instead would invert most of them — the 3rd would become the 9th, the
    trines would land on the dusthanas.
    """
    from hora.dasha.rasi.narayana import dasa_lagna

    # Seeded from lagna: the dasa rasi is read as lagna.
    for rasi in range(12):
        assert dasa_lagna(rasi, R["Aries"], R["Aries"]) == rasi

    # Seeded from the 7th: the 7th from the dasa rasi is.
    for rasi in range(12):
        assert dasa_lagna(rasi, R["Libra"], R["Aries"]) == (rasi + 6) % 12


def test_both_charts_worked_in_this_chapter_use_the_shifted_reading():
    """Charts 21 and 23 are both seeded from the 7th house, so neither reads
    its dasa lagna as the dasa rasi. A test that only exercised lagna-seeded
    charts would have missed the rule entirely.
    """
    from hora.charts.book import graha_longitudes, lagna
    from hora.dasha.rasi.narayana import dasa_lagna, dasa_seed

    for number in (21, 23):
        longitudes = {int(g): lon for g, lon in graha_longitudes(number).items()}
        natal = lagna(number)
        seed = dasa_seed(natal, longitudes)["seed"]
        assert seed == (natal + 6) % 12
        for rasi in range(12):
            assert dasa_lagna(rasi, seed, natal) == (rasi + 6) % 12


def test_a_seed_that_is_neither_lagna_nor_the_seventh_is_refused():
    """§18.2.1 admits only those two, so a third would mean the seed was
    computed wrongly upstream and should not be quietly accommodated."""
    from hora.dasha.rasi.narayana import NarayanaError, dasa_lagna

    with pytest.raises(NarayanaError, match="neither the lagna"):
        dasa_lagna(R["Aries"], R["Gemini"], R["Aries"])


def test_paaka_rasi_is_where_the_dasa_lagnas_lord_sits():
    """"We will denote the rasi containing the lord of dasa lagna with 'paaka
    rasi'." Not the dasa lagna itself, and not the dasa rasi's lord."""
    from hora.charts.book import graha_longitudes
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import paaka_rasi

    longitudes = {int(g): lon for g, lon in graha_longitudes(23).items()}
    for sign in range(12):
        if sign in (R["Scorpio"], R["Aquarius"]):
            continue                               # needs §15.5.1's lord
        lord = int(RASI_LORD[sign])
        assert paaka_rasi(sign, longitudes) == int(longitudes[lord] // 30)


def test_paaka_rasi_needs_the_stronger_lord_for_the_co_owned_signs():
    """Scorpio and Aquarius have two lords and give two different paaka rasis,
    so the caller must resolve them rather than a default being taken."""
    from hora.charts.book import graha_longitudes
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import paaka_rasi

    longitudes = {int(g): lon for g, lon in graha_longitudes(23).items()}
    by_mars = paaka_rasi(R["Scorpio"], longitudes, int(Graha.MARS))
    by_ketu = paaka_rasi(R["Scorpio"], longitudes, int(Graha.KETU))
    assert by_mars != by_ketu


def test_a_missing_lord_longitude_is_refused_not_defaulted():
    from hora.dasha.rasi.narayana import NarayanaError, paaka_rasi

    with pytest.raises(NarayanaError, match="no longitude given"):
        paaka_rasi(R["Aries"], {})


def test_parasaras_principles_are_recorded_as_a_register():
    """Sixteen readings, each naming what it looks at and what it gives. They
    are a register rather than a calculation: nothing here predicts, and the
    houses are counted from the dasa lagna unless an entry says otherwise.
    """
    from hora.dasha.rasi.narayana import PARASARA_DASA_PRINCIPLES

    assert len(PARASARA_DASA_PRINCIPLES) == 16
    for principle in PARASARA_DASA_PRINCIPLES:
        assert principle["who"] and principle["gives"]
        if principle["houses"]:
            assert all(1 <= h <= 12 for h in principle["houses"])


def test_the_third_and_sixth_reverse_the_usual_benefic_reading():
    """"Natural malefics in the 3rd and 6th from dasa lagna give success in
    ventures. Natural benefics in those houses give failures."

    The inversion is the point, and it is the opposite of the trines-and-8th
    rule two sentences later, so both are asserted together.
    """
    from hora.dasha.rasi.narayana import PARASARA_DASA_PRINCIPLES

    by_key = {(p["houses"], p["who"]): p["gives"]
              for p in PARASARA_DASA_PRINCIPLES if p["houses"]}
    assert by_key[((3, 6), "natural malefics")] == "success in ventures"
    assert by_key[((3, 6), "natural benefics")] == "failures"
    assert by_key[((1, 5, 9, 8), "natural benefics")] == "happiness and success"
    assert by_key[((1, 5, 9, 8), "natural malefics")].startswith("failures")


def test_each_dasa_divides_into_three_equal_parts():
    """"divide each dasa into three equal parts. The rasi dominates in the
    first part. Its lord dominates in the second part... Occupants of the rasi
    and those who aspect it dominate in the third part."
    """
    from hora.dasha.rasi.narayana import dasa_thirds

    thirds = dasa_thirds(0.0, 9.0)
    assert [t["part"] for t in thirds] == [1, 2, 3]
    assert [t["from_years"] for t in thirds] == [0.0, 3.0, 6.0]
    assert [t["to_years"] for t in thirds] == [3.0, 6.0, 9.0]
    assert "rasi" in thirds[0]["dominates"]
    assert "lord" in thirds[1]["dominates"]
    assert "aspect" in thirds[2]["dominates"]

    offset = dasa_thirds(12.5, 3.0)
    assert offset[0]["from_years"] == 12.5
    assert offset[2]["to_years"] == 15.5


def test_antardasa_results_are_read_from_the_dasa_rasi_not_the_dasa_lagna():
    """"We also judge the results given in antardasas by looking at the house
    occupied by antardasa lord from dasa rasi."

    A third reference point in one section — dasa lagna for the dasa, dasa
    rasi for the antardasa, and the natal points below for their own readings.
    """
    from hora.dasha.rasi.narayana import ANTARDASA_RESULT_RULE

    assert "from dasa rasi" in ANTARDASA_RESULT_RULE
    assert "dasa lagna" not in ANTARDASA_RESULT_RULE


def test_the_natal_reference_readings_are_recorded():
    """"dasa of raajya pada gives success in career. Dasa of upapada may bring
    marriage..." — read from natal points, not from the dasa lagna."""
    from hora.dasha.rasi.narayana import NATAL_REFERENCE_READINGS

    subjects = {r["of"] for r in NATAL_REFERENCE_READINGS}
    assert "raajya pada" in subjects
    assert "upapada" in subjects
    assert "GL" in subjects
    assert len(NATAL_REFERENCE_READINGS) == 6


# --------------------------------------------------------------------------
# Example 68 — Bill Gates, Chart 24. The first lagna-seeded chart in the
# chapter, and the one that settles two of its open questions at once.
# --------------------------------------------------------------------------

#: The seven dasas the example prints, in order, with the years it gives.
EX68_LENGTHS = [("Ge", 4), ("Aq", 5), ("Li", 12), ("Vi", 12), ("Ta", 5),
                ("Cp", 4), ("Sg", 8)]

#: And the dates, which are a second reading of the same seven lengths.
EX68_DATES = [("Ge", 1955, 1959), ("Aq", 1959, 1964), ("Li", 1964, 1976),
              ("Vi", 1976, 1988), ("Ta", 1988, 1993), ("Cp", 1993, 1997),
              ("Sg", 1997, 2005)]


def _chart_24():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(24).items()},
            {int(g): sign for g, sign in graha_signs(24).items()},
            lagna(24))


def _house_from(reference, sign):
    """Houses counted the ordinary way, the reference itself being the 1st."""
    return (sign - reference) % 12 + 1


def test_chart_24_recomputes_from_bill_gates_birth_data():
    """The chart is transcribed, so it is worth knowing it is the right one.
    Every graha inside about an arcminute of what the book prints.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(24)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 24", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(24)
    for name, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.1, f"{name}: {error:.2f}'"


def test_chart_24_is_a_seventh_chart_favouring_the_mean_node():
    """OI-68 again, and this one is not close: the true node is over a degree
    away and lands Rahu in a different sign from the one the book draws."""
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record, printed = chart(24), longitudes(24)["Rahu"]
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name="Chart 24", **record["place"]),
            Settings(node_type=node))
        errors[node] = abs(
            computed.positions[int(Graha.RAHU)].longitude - printed) * 60
    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 60.0


def test_chart_24_chara_karakas_derive_from_the_printed_longitudes():
    """The chart labels all eight. Saturn at 28 Li 21 is the most advanced and
    takes AK; Rahu counts backwards from 30 and lands last, as DK."""
    from hora.charts.book import chart
    from hora.charts.karaka import chara_karakas
    from hora.core.const import Graha

    longitudes, _signs, _lagna = _chart_24()
    eight = {g: lon for g, lon in longitudes.items() if g != int(Graha.KETU)}
    ours = {k.graha: k.symbol for k in chara_karakas(eight)}

    by_short = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
                "Merc": Graha.MERCURY, "Jup": Graha.JUPITER,
                "Ven": Graha.VENUS, "Sat": Graha.SATURN, "Rahu": Graha.RAHU}
    for short, symbol in chart(24)["chara_karakas"].items():
        assert ours[int(by_short[short])] == symbol, short


def test_chart_24_arudha_lagna_needs_the_seventh_house_exception():
    """The chart draws AL in Vi, which the plain rule does not give. Lagna Ge
    counts 4 houses to Mercury in Vi, and 4 from Vi is Sg -- the 7th from
    lagna, which the arudha rule forbids. The 10th from there is Vi.
    """
    from hora.charts.arudha import arudha_pada

    _longitudes, signs, lagna_sign = _chart_24()
    got = arudha_pada(1, lagna_sign, signs)
    assert got.sign == R["Virgo"]
    assert got.before_exception == R["Sagittarius"]
    assert got.exception_applied is True
    assert got.exception_position == 7


def test_example_68_raajya_pada_is_capricorn():
    """"Cp contains raajya pada (A10 - arudha pada of the 10th house)." The
    one thing point (1) rests on, and the chart does not draw it.
    """
    from hora.charts.arudha import arudha_pada

    _longitudes, signs, lagna_sign = _chart_24()
    assert arudha_pada(10, lagna_sign, signs).sign == R["Capricorn"]


def test_example_68_seed_is_lagna_because_its_lord_aspects_it():
    """"Lagna is stronger than the 7th house as its exalted lord aspects it.
    So dasas start from Ge."

    Section 15.5.2's rule 2 counts Jupiter, Mercury and the rasi's own lord.
    Mercury in Vi aspects both Ge and Sg by rasi drishti, so he is one mark
    each way; what parts them is that for Ge he is also the lord, and counts
    again. Nothing above rule 2 separates them -- neither holds a planet.
    """
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign = _chart_24()
    assert lagna_sign == R["Gemini"]
    assert not [g for g, s in signs.items() if s in (R["Gemini"], R["Sagittarius"])]

    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["seed"] == R["Gemini"]
    assert seed["decided_by"] == "2"
    assert "lord (Mercury) aspects from Virgo" in seed["reason"]


def test_example_68_progression_is_vishnus_backward_trine():
    """"So dasas start from Ge", and the printed order runs Ge, Aq, Li, Vi,
    Ta, Cp, Sg. Gemini is dual, so Vishnu; the 9th from it is Aq, even-footed,
    so backward. Neither Saturn nor Ketu is in Ge, so no exception fires.
    """
    from hora.dasha.rasi.narayana import progression

    _longitudes, signs, lagna_sign = _chart_24()
    assert lagna_sign == R["Gemini"]                 # and the seed is lagna
    occupants = {g for g, sign in signs.items() if sign == lagna_sign}
    assert not occupants

    got = progression(lagna_sign, occupants)
    assert got.god == "Vishnu"
    assert got.direction == "backward"
    assert got.exception is None
    assert [ABBR[s] for s in got.signs][:7] == [a for a, _y in EX68_LENGTHS]


@pytest.mark.parametrize("abbr,years", EX68_LENGTHS)
def test_example_68_lengths_the_books_way(abbr, years):
    """All seven, with Mercury read as exalted in Virgo -- which is what the
    example does, in its arithmetic and twice in its prose. See D-52.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_24()
    lord = int(RASI_LORD[BY_ABBR[abbr]])
    dignity = ("exalted" if lord == int(Graha.MERCURY)
               else sign_dignity(lord, longitudes[lord]))
    got = dasa_length(BY_ABBR[abbr], lord, signs[lord], dignity)
    assert got.years == years, got.why


def test_example_68_settles_oi_121_and_d_52_together():
    """The example turns on one planet, and only one reading of him fits.

    Mercury sits at 23 Vi 19 and rules both Ge and Vi:

    * Ge counts 4 houses forward to him. 4 - 1 = 3, and the example says 4, so
      exception 2 fired and he is exalted -- though by degree he is past his
      exaltation and his moolatrikona both, and `sign_dignity` says "own".
      That is D-52, and it is decided here at sign level.
    * Vi contains him, so exception 1 gives 12. Were exception 2 then to add
      its year the answer would be 13, and the example prints 12. That is
      OI-121, and exception 1 is terminal.

    Neither can be traded against the other: it is the same planet in the same
    degree in both dasas, so no reading of "exalted" makes both come out.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_24()
    mercury = int(Graha.MERCURY)
    assert signs[mercury] == R["Virgo"]
    assert sign_dignity(mercury, longitudes[mercury]) == "own"

    by_degree = dasa_length(R["Gemini"], mercury, signs[mercury], "own")
    assert by_degree.count == 4
    assert by_degree.years == 3                    # not the example's 4
    by_sign = dasa_length(R["Gemini"], mercury, signs[mercury], "exalted")
    assert by_sign.years == 4                      # the example's

    virgo = dasa_length(R["Virgo"], mercury, signs[mercury], "exalted")
    assert virgo.count == 1
    assert virgo.years == 12                       # not 13
    assert virgo.applied == ("contains its lord, so 12 rather than 0",)


def test_example_68_the_dates_the_example_prints():
    """"Ge (04 years): Oct 1955 - Oct 1959" and on to "Sg (08 years): Oct 1997
    - Oct 2005." A running total from an October 1955 birth, so the dates
    check the lengths a second way. Every boundary is an October, so this
    example says nothing about OI-115's savana year.
    """
    year = 1955
    for (abbr, years), (also, start, end) in zip(EX68_LENGTHS, EX68_DATES):
        assert abbr == also
        assert (year, year + years) == (start, end)
        year += years
    assert year == 2005


def test_example_68_is_the_first_chart_whose_dasa_lagna_is_the_dasa_rasi():
    """Section 18.4's rule read from the other side. Charts 21 and 23 were
    both seeded from the 7th house, so on both the dasa lagna sat six signs
    from the dasa rasi. Gates is seeded from lagna, and the example duly says
    "During Cp dasa, dasa lagna is Cp" and "Dasa lagna is Sg".
    """
    from hora.dasha.rasi.narayana import dasa_lagna, progression

    _longitudes, signs, lagna_sign = _chart_24()
    occupants = {g for g, sign in signs.items() if sign == lagna_sign}
    for rasi in progression(lagna_sign, occupants).signs:
        assert dasa_lagna(rasi, lagna_sign, lagna_sign) == rasi

    assert dasa_lagna(R["Capricorn"], lagna_sign, lagna_sign) == R["Capricorn"]
    assert dasa_lagna(R["Sagittarius"], lagna_sign, lagna_sign) == R["Sagittarius"]


def test_example_68_capricorn_dasa_paaka_rasi_and_raja_yoga():
    """"During Cp dasa, dasa lagna is Cp and paaka rasi is Li. Lord of dasa
    lagna is Saturn. He is exalted in the 10th house with the 10th lord Venus
    (from dasa lagna). They form a powerful raja yoga w.r.t. dasa lagna as
    well as paaka rasi."

    From the paaka rasi Li, Saturn owns the 4th and the 5th -- a kendra and a
    trine, which is what makes him Libra's yoga karaka -- and Venus is its
    lord. So the same pair reads as a raja yoga from either reference.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_lagna, paaka_rasi

    longitudes, signs, lagna_sign = _chart_24()
    saturn, venus = int(Graha.SATURN), int(Graha.VENUS)

    lagna_of_dasa = dasa_lagna(R["Capricorn"], lagna_sign, lagna_sign)
    assert lagna_of_dasa == R["Capricorn"]
    assert int(RASI_LORD[lagna_of_dasa]) == saturn
    assert paaka_rasi(lagna_of_dasa, longitudes) == R["Libra"]

    assert sign_dignity(saturn, longitudes[saturn]) == "exalted"
    assert _house_from(lagna_of_dasa, signs[saturn]) == 10
    assert signs[venus] == signs[saturn]
    tenth = (lagna_of_dasa + 9) % 12
    assert int(RASI_LORD[tenth]) == venus

    # ... and w.r.t. the paaka rasi, where Saturn is the yoga karaka.
    assert {h for h in (4, 5)
            if int(RASI_LORD[(R["Libra"] + h - 1) % 12]) == saturn} == {4, 5}
    assert int(RASI_LORD[R["Libra"]]) == venus


def test_example_68_capricorn_dasa_placements_from_the_dasa_lagna():
    """"Exalted Mercury is in a trine from dasa lagna and Jupiter is in 8th
    from dasa lagna. Rahu is in 11th. Two powerful planets are in 10th. All
    these are favorable placements." And "Sun owns the 8th house from dasa
    lagna and he is debilitated."

    Every one of these is a house counted from Cp, which is only the dasa
    rasi because this chart happens to be seeded from lagna.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_lagna

    longitudes, signs, lagna_sign = _chart_24()
    cp = dasa_lagna(R["Capricorn"], lagna_sign, lagna_sign)

    assert _house_from(cp, signs[int(Graha.MERCURY)]) == 9        # a trine
    assert _house_from(cp, signs[int(Graha.JUPITER)]) == 8
    assert _house_from(cp, signs[int(Graha.RAHU)]) == 11

    tenth = (cp + 9) % 12
    powerful = {g for g, sign in signs.items() if sign == tenth
                and sign_dignity(g, longitudes[g]) in ("exalted", "own")}
    assert powerful == {int(Graha.SATURN), int(Graha.VENUS)}

    eighth = (cp + 7) % 12
    assert eighth == R["Leo"]
    assert int(RASI_LORD[eighth]) == int(Graha.SUN)
    assert sign_dignity(int(Graha.SUN), longitudes[int(Graha.SUN)]) == "debilitated"


def test_example_68_sagittarius_dasa_reads_from_a_different_lagna():
    """"Dasa lagna is Sg and paaka rasi is Le... Dasa lagna lord Jupiter
    occupies the 9th house... Rahu occupies the 12th house... Sun, the lord of
    the 9th house from dasa lagna, is debilitated. He is also the lord of
    paaka rasi."

    The same nine placements as the Cp dasa above, read from a lagna one sign
    away: Rahu moves from the 11th to the 12th, and Jupiter from the 8th to
    the 9th. Nothing in the chart changed.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_lagna, paaka_rasi

    longitudes, signs, lagna_sign = _chart_24()
    sg = dasa_lagna(R["Sagittarius"], lagna_sign, lagna_sign)
    assert sg == R["Sagittarius"]
    assert int(RASI_LORD[sg]) == int(Graha.JUPITER)

    paaka = paaka_rasi(sg, longitudes)
    assert paaka == R["Leo"]
    assert _house_from(sg, signs[int(Graha.JUPITER)]) == 9
    assert _house_from(sg, signs[int(Graha.RAHU)]) == 12

    ninth = (sg + 8) % 12
    assert ninth == paaka                       # "He is also the lord of paaka rasi"
    assert int(RASI_LORD[ninth]) == int(Graha.SUN)
    assert sign_dignity(int(Graha.SUN), longitudes[int(Graha.SUN)]) == "debilitated"


def test_example_68_sagittarius_dasa_tenth_and_eleventh_are_strong():
    """"The 10th and 11th houses from dasa lagna are particularly strong.
    Exalted Mercury occupies the 10th house from dasa lagna and he has a raaja
    yoga with Mars w.r.t. dasa lagna."

    Mercury owns the 7th and the 10th from Sg, both kendras; Mars owns the
    5th, a trine. They are conjoined in Vi, which is the kendra-trine pairing
    a raaja yoga asks for -- and it exists only w.r.t. this dasa lagna.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_lagna

    longitudes, signs, _lagna = _chart_24()
    sg = dasa_lagna(R["Sagittarius"], R["Gemini"], R["Gemini"])
    mercury, mars = int(Graha.MERCURY), int(Graha.MARS)

    assert _house_from(sg, signs[mercury]) == 10
    assert signs[mars] == signs[mercury]

    owned = lambda g: {h for h in range(1, 13)
                       if int(RASI_LORD[(sg + h - 1) % 12]) == g}
    assert owned(mercury) == {7, 10}                # both kendras
    assert 5 in owned(mars)                         # a trine

    eleventh = (sg + 10) % 12
    assert eleventh == R["Libra"]
    strong = {g for g, sign in signs.items() if sign == eleventh
              and sign_dignity(g, longitudes[g]) in ("exalted", "own")}
    assert strong == {int(Graha.SATURN), int(Graha.VENUS)}


def test_example_68_ranks_the_two_dasa_lagna_lords_the_way_the_example_does():
    """"The lord of dasa lagna is not particularly strong (not as strong as
    the previous dasa's dasa lagna lord). But he is not weak either."

    Cp's lord Saturn is exalted; Sg's lord Jupiter is in Leo, a friend's sign
    -- neither dignified nor debilitated. Our own dignities give exactly that
    ordering, which is the whole of the example's claim.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import Graha

    longitudes, signs, _lagna = _chart_24()
    assert sign_dignity(int(Graha.SATURN), longitudes[int(Graha.SATURN)]) == "exalted"
    assert sign_dignity(int(Graha.JUPITER), longitudes[int(Graha.JUPITER)]) == "neutral"
    assert signs[int(Graha.JUPITER)] == R["Leo"]


# --------------------------------------------------------------------------
# Example 69 — India's independence, Chart 25. A mundane chart, twelve
# lengths, three dasas interpreted, and the chapter's first worked antardasa.
# --------------------------------------------------------------------------

#: The eleven dasas the example prints, in order. The twelfth, Li, runs past
#: the span the example covers and is not printed.
EX69_LENGTHS = [("Ta", 2), ("Sg", 10), ("Cn", 12), ("Aq", 7), ("Vi", 2),
                ("Ar", 2), ("Sc", 7), ("Ge", 1), ("Cp", 6), ("Le", 1),
                ("Pi", 5)]


def _chart_25():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(25).items()},
            {int(g): sign for g, sign in graha_signs(25).items()},
            lagna(25))


def test_chart_25_recomputes_from_the_independence_moment():
    """Midnight IST on 15 August 1947 at 78 E 30, 27 N 00. Every graha inside
    an arcminute and the ascendant inside a fifth of one, which is as close as
    any chart in the book has come.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(25)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 25", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(25)
    for name, graha in (("Sun", Graha.SUN), ("Moon", Graha.MOON),
                        ("Mars", Graha.MARS), ("Merc", Graha.MERCURY),
                        ("Jup", Graha.JUPITER), ("Ven", Graha.VENUS),
                        ("Sat", Graha.SATURN), ("Rahu", Graha.RAHU),
                        ("Ketu", Graha.KETU)):
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 0.5


def test_charts_25_and_26_are_the_eighth_and_ninth_votes_for_the_mean_node():
    """OI-68. Chart 25's Rahu is 0.2' out under mean and 41' out under true."""
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    for number in (25, 26):
        record, printed = chart(number), longitudes(number)["Rahu"]
        errors = {}
        for node in (NodeType.MEAN, NodeType.TRUE):
            computed = compute_chart(
                from_local(**record["birth_data"]),
                Place(name=f"Chart {number}", **record["place"]),
                Settings(node_type=node))
            errors[node] = abs(
                computed.positions[int(Graha.RAHU)].longitude - printed) * 60
        assert errors[NodeType.MEAN] < 1.0, number
        assert errors[NodeType.MEAN] < errors[NodeType.TRUE], number


def test_example_69_seed_is_lagna_and_the_progression_is_shivas_sixth():
    """The printed order is Ta, Sg, Cn, Aq, Vi, Ar, Sc, Ge, Cp, Le, Pi.

    Ta is fixed, so Shiva's 6th movement; the 9th from Ta is Cp, even-footed,
    so backward -- and 6 backward from Ta is indeed Sg. Rahu occupies the
    seed, which is neither of §18.2.1's two exceptions.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_seed, progression

    longitudes, signs, lagna_sign = _chart_25()
    assert lagna_sign == R["Taurus"]

    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["seed"] == R["Taurus"]
    assert seed["decided_by"] == "2"

    occupants = {g for g, sign in signs.items() if sign == seed["seed"]}
    assert occupants == {int(Graha.RAHU)}

    got = progression(seed["seed"], occupants)
    assert got.god == "Shiva"
    assert got.direction == "backward"
    assert got.exception is None
    assert [ABBR[s] for s in got.signs][:11] == [a for a, _y in EX69_LENGTHS]
    assert ABBR[got.signs[11]] == "Li"          # the one the example stops before


def test_example_69_seed_rule_2_counts_three_against_two():
    """Both rasis hold exactly one graha, so rule 1 ties and rule 2 decides.

    Jupiter aspects Ta from Li, Mercury aspects it from Cn, and so does its own
    lord Venus -- three. Scorpio gets Mercury's aspect and its co-lord Ketu
    sitting in it -- two.
    """
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign = _chart_25()
    in_taurus = [g for g, s in signs.items() if s == R["Taurus"]]
    in_scorpio = [g for g, s in signs.items() if s == R["Scorpio"]]
    assert len(in_taurus) == len(in_scorpio) == 1        # rule 1 ties

    reason = dasa_seed(lagna_sign, longitudes)["reason"]
    assert "Taurus count 3" in reason
    assert "Scorpio count 2" in reason


@pytest.mark.parametrize("abbr,years", EX69_LENGTHS)
def test_example_69_lengths(abbr, years):
    """All eleven printed lengths, each from its own counting direction. No
    graha in this chart is exalted or debilitated where the counts land, so
    neither D-52 nor OI-121 touches this example -- it tests the base rule and
    exception 1 alone.
    """
    from hora.charts.colord import stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_25()
    rasi = BY_ABBR[abbr]
    lord = (stronger(rasi, longitudes, purpose="arudha").winner
            if rasi in (R["Scorpio"], R["Aquarius"]) else int(RASI_LORD[rasi]))
    got = dasa_length(rasi, lord, signs[lord],
                      sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why


def test_example_69_pins_the_co_lord_cascade_twice():
    """Special note 1 sends Scorpio and Aquarius to §15.5.1, and this is the
    first chart whose printed answers test what comes back. Both co-lords are
    in different rasis from their partners, so the wrong choice is not a near
    miss -- it is a different dasa length.

    | rasi | co-lords | book | the other co-lord would give |
    |---|---|---|---|
    | Aquarius | Saturn in Cn, Rahu in Ta | 7 | 9 |
    | Scorpio | Mars in Ge, Ketu in Sc | 7 | 12, by exception 1 |
    """
    from hora.charts.colord import stronger
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_25()
    saturn, rahu = int(Graha.SATURN), int(Graha.RAHU)
    mars, ketu = int(Graha.MARS), int(Graha.KETU)

    assert stronger(R["Aquarius"], longitudes, purpose="arudha").winner == saturn
    assert dasa_length(R["Aquarius"], saturn, signs[saturn]).years == 7
    assert dasa_length(R["Aquarius"], rahu, signs[rahu]).years == 9

    assert stronger(R["Scorpio"], longitudes, purpose="arudha").winner == mars
    assert dasa_length(R["Scorpio"], mars, signs[mars]).years == 7
    wrong = dasa_length(R["Scorpio"], ketu, signs[ketu])
    assert wrong.count == 1 and wrong.years == 12


def test_example_69_the_dates_the_example_prints():
    """"Ta (02 years): Aug 1947 - Aug 1949" through "Pi (05 years): Aug 1997 -
    Aug 2002." A running total from August 1947, so the printed dates check
    all eleven lengths a second way. Every boundary is an August, so this
    example says nothing about OI-115's savana year either.
    """
    year, spans = 1947, {}
    for abbr, years in EX69_LENGTHS:
        spans[abbr] = (year, year + years)
        year += years

    assert spans["Ta"] == (1947, 1949)
    assert spans["Cn"] == (1959, 1971)
    assert spans["Sc"] == (1982, 1989)
    assert spans["Cp"] == (1990, 1996)
    assert spans["Le"] == (1996, 1997)
    assert spans["Pi"] == (1997, 2002)
    assert year == 2002


def test_example_69_capricorn_dasa_placements():
    """"Mars in the 6th house, Jupiter in the 10th house and Ketu in the 11th
    house from dasa lagna are well-placed. Conglomeration of planets in the
    7th house... From paaka rasi also, Rahu is in the 11th house."

    Taurus was the seed and Taurus is lagna, so the dasa lagna is Cp itself --
    the second lagna-seeded chart in the chapter, after Chart 24.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_lagna, paaka_rasi

    longitudes, signs, lagna_sign = _chart_25()
    cp = dasa_lagna(R["Capricorn"], lagna_sign, lagna_sign)
    assert cp == R["Capricorn"]

    assert _house_from(cp, signs[int(Graha.MARS)]) == 6
    assert _house_from(cp, signs[int(Graha.JUPITER)]) == 10
    assert _house_from(cp, signs[int(Graha.KETU)]) == 11

    seventh = (cp + 6) % 12
    assert seventh == R["Cancer"]
    assert len([g for g, s in signs.items() if s == seventh]) == 5

    paaka = paaka_rasi(cp, longitudes)
    assert paaka == R["Cancer"]                       # Cp's lord Saturn is there
    assert _house_from(paaka, signs[int(Graha.RAHU)]) == 11


def test_example_69_mars_aspects_the_ninth_from_the_capricorn_dasa_lagna():
    """"Aspect of Mars on the analytical and tamasik rasi Vi containing the
    9th house from dasa lagna made the judiciary system relatively
    aggressive."

    Both aspect systems agree here, which is worth knowing because the example
    does not say which it means: Ge aspects Vi by rasi drishti, and Vi is also
    the 4th from Ge, one of Mars's three special graha aspects.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_lagna

    _longitudes, signs, lagna_sign = _chart_25()
    cp = dasa_lagna(R["Capricorn"], lagna_sign, lagna_sign)
    ninth = (cp + 8) % 12
    assert ninth == R["Virgo"]

    mars_sign = signs[int(Graha.MARS)]
    assert mars_sign == R["Gemini"]
    assert ninth in rasi_drishti(mars_sign)
    assert (ninth - mars_sign) % 12 + 1 == 4          # Mars's 4th aspect


def test_example_69_leo_dasa_leaves_only_mars_well_placed():
    """"Dasa lagna during Le dasa is Le itself. Except Mars, no planet is
    well-placed w.r.t. Le. In particular, planetary conglomeration in the 12th
    house... Rahu in the 10th house from dasa lagna denies stable and capable
    leadership."

    One sign on from Cp and the whole chart inverts: the five planets fall
    from the 7th to the 12th, Ketu from the 11th to the 4th, Jupiter from the
    10th to the 3rd. Only Mars improves, from the 6th to the 11th.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_lagna

    _longitudes, signs, lagna_sign = _chart_25()
    le = dasa_lagna(R["Leo"], lagna_sign, lagna_sign)
    assert le == R["Leo"]

    houses = {}
    for graha, sign in signs.items():
        houses.setdefault(_house_from(le, sign), set()).add(graha)

    assert houses[11] == {int(Graha.MARS)}
    assert len(houses[12]) == 5
    assert houses[10] == {int(Graha.RAHU)}
    assert houses[4] == {int(Graha.KETU)}
    assert houses[3] == {int(Graha.JUPITER)}


def test_example_69_pisces_dasa_placements():
    """"Most planets are well-placed w.r.t. Pisces... Jupiter owns the 10th
    house and Mars aspects it... Ketu in the 9th house... Mars in the 4th
    house... Rahu in the 3rd house from dasa lagna."

    The five-planet conglomeration lands in the 5th, a trine, which is what
    "most planets are well-placed" rests on.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_lagna, paaka_rasi

    longitudes, signs, lagna_sign = _chart_25()
    pi = dasa_lagna(R["Pisces"], lagna_sign, lagna_sign)
    assert pi == R["Pisces"]
    assert paaka_rasi(pi, longitudes) == R["Libra"]

    fifth = (pi + 4) % 12
    assert len([g for g, s in signs.items() if s == fifth]) == 5
    assert _house_from(pi, signs[int(Graha.KETU)]) == 9
    assert _house_from(pi, signs[int(Graha.MARS)]) == 4
    assert _house_from(pi, signs[int(Graha.RAHU)]) == 3

    tenth = (pi + 9) % 12
    assert tenth == R["Sagittarius"]
    assert int(RASI_LORD[tenth]) == int(Graha.JUPITER)
    assert tenth in rasi_drishti(signs[int(Graha.MARS)])


def test_example_69_pisces_antardasas_start_from_libra_going_forward():
    """"Antardasas in Pisces dasa start from Libra and proceed in the forward
    direction."

    The chapter's first worked antardasa, and it exercises §18.3 whole. The
    seed is the stronger of Pi and the 7th from it, Vi -- and nothing separates
    them until rule 4, where Pi's lord Jupiter sits in odd Libra while Vi's
    lord Mercury sits in even Cancer. So the seed is Pi, and the antardasas
    begin where its lord is: Libra. Libra is an odd *sign*, so forward.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import antardasas

    longitudes, signs, _lagna = _chart_25()
    occupants = {g for g, sign in signs.items() if sign == R["Pisces"]}
    assert not occupants                                # no exception fires

    got = antardasas(R["Pisces"], 5, longitudes, seed_occupants=occupants)
    assert got.seed == R["Pisces"]
    assert got.start == R["Libra"]
    assert got.direction == "forward"
    assert got.exception is None
    assert [ABBR[s] for s in got.signs[:3]] == ["Li", "Sc", "Sg"]
    assert signs[int(Graha.JUPITER)] == got.start       # Libra holds Jupiter


def test_example_69_scorpio_antardasa_holds_may_1998():
    """"Antardasa at the time of nuclear tests was Sc." India tested on 11 and
    13 May 1998.

    Pisces runs five years from August 1997, so each of the twelve antardasas
    is five months. Libra takes it to January 1998 and Scorpio to June, which
    is the only antardasa May 1998 can fall in.
    """
    from hora.dasha.rasi.narayana import antardasas

    longitudes, _signs, _lagna = _chart_25()
    got = antardasas(R["Pisces"], 5, longitudes, seed_occupants=set())
    assert got.months_each == 5

    start = 1997 * 12 + 7                               # August 1997
    spans = {ABBR[sign]: (start + i * got.months_each,
                          start + (i + 1) * got.months_each)
             for i, sign in enumerate(got.signs)}
    may_1998 = 1998 * 12 + 4
    running = [abbr for abbr, (a, b) in spans.items() if a <= may_1998 < b]
    assert running == ["Sc"]


def test_example_69_a3_is_aries_by_the_arudha_exception():
    """"Sc aspects A3, which is in Ar." The example never derives it.

    The 3rd from Ta is Cn, whose lord the Moon sits in Cn itself, so the count
    is 1 and the arudha lands back on the house -- which §9.2's first exception
    forbids. The 10th from there is Ar.
    """
    from hora.charts.arudha import arudha_pada

    _longitudes, signs, lagna_sign = _chart_25()
    got = arudha_pada(3, lagna_sign, signs)
    assert got.before_exception == R["Cancer"]
    assert got.exception_position == 1
    assert got.sign == R["Aries"]


def test_example_69_the_scorpio_antardasa_aspects_a3():
    """"Sc aspects A3, which is in Ar. A3 shows the illusion related to
    boldness... Antardasas aspecting A3 can bring weapons, just as antardasas
    aspecting UL can bring marriage."

    A fourth reference point in the chapter, and a different mechanism from
    the other three. §18.4 reads an antardasa by the house its *lord* occupies
    from the dasa rasi; this reads the antardasa **rasi** by what it aspects,
    and the target is a natal arudha that has nothing to do with the dasa.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.narayana import ANTARDASA_ASPECT_RULE

    _longitudes, signs, lagna_sign = _chart_25()
    a3 = arudha_pada(3, lagna_sign, signs).sign
    assert a3 in rasi_drishti(R["Scorpio"])

    assert "A3" in ANTARDASA_ASPECT_RULE
    assert "UL" in ANTARDASA_ASPECT_RULE


def test_example_69s_mundane_readings_are_recorded_not_folded_in():
    """The book's first mundane Narayana dasa. §18.4's sixteen principles give
    a placement's valence; what it is *about* comes from the house, read for a
    nation. Both halves are needed and only the first is in the principles, so
    the pairings are kept as their own register.
    """
    from hora.dasha.rasi.narayana import (
        MUNDANE_HOUSE_READINGS,
        UNLISTED_DASA_LAGNA_READINGS,
    )

    houses = {r["house"] for r in MUNDANE_HOUSE_READINGS}
    assert houses == {3, 7, 9, 10}
    assert len(UNLISTED_DASA_LAGNA_READINGS) == 2


def test_example_69s_two_unlisted_readings_are_not_in_the_sixteen():
    """A conglomeration in the 12th giving "constant fear", and Rahu in the
    10th denying leadership. Principle 6 gives constant fear for **Rahu** in
    the 8th or 12th, and no principle reaches the 10th at all except through
    lordship. Neither reading follows from the list.
    """
    from hora.dasha.rasi.narayana import PARASARA_DASA_PRINCIPLES

    fear = [p for p in PARASARA_DASA_PRINCIPLES if "fear" in p["gives"]]
    assert len(fear) == 1
    assert fear[0]["who"] == "Rahu"
    assert fear[0]["houses"] == (8, 12)

    occupancy = [p for p in PARASARA_DASA_PRINCIPLES if p["houses"]]
    assert not any(10 in p["houses"] for p in occupancy)


# --------------------------------------------------------------------------
# Exercise 28 — Chart 26, and the first chart in the chapter whose dasa seed
# is settled by §15.5.2's rule 4.
# --------------------------------------------------------------------------

#: The five dasas the answer prints, in order.
EX28_LENGTHS = [("Sg", 11), ("Le", 5), ("Ar", 10), ("Pi", 4), ("Sc", 3)]


def _chart_26():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(26).items()},
            {int(g): sign for g, sign in graha_signs(26).items()},
            lagna(26))


def test_exercise_28_seed_is_the_first_settled_by_rule_4():
    """"Both Ge and Sg are unoccupied. Neither is occupied or aspected by
    Jupiter, Mercury or lord. Ge is an odd rasi and Mercury is also in an odd
    rasi. But Sg is an odd rasi and Jupiter is in an even rasi. So Sg is
    stronger."

    The answer walks §15.5.2 in order and names where it stops. Rule 1 ties on
    nothing, rule 2 ties on nothing, rule 3 cannot fire because neither rasi
    holds a planet at all -- and rule 4 separates them on the oddity of the
    rasis their lords sit in. Every other chart in the chapter stopped at
    rule 1 or 2, so this is the first test of the cascade this far down.
    """
    from hora.core.const import RASI_IS_ODD, Graha
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign = _chart_26()
    assert lagna_sign == R["Gemini"]
    assert not [g for g, s in signs.items()
                if s in (R["Gemini"], R["Sagittarius"])]        # both unoccupied

    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["seed"] == R["Sagittarius"]
    assert seed["decided_by"] == "4"

    # The oddities the answer spells out, in its own order.
    assert RASI_IS_ODD[R["Gemini"]] and RASI_IS_ODD[signs[int(Graha.MERCURY)]]
    assert RASI_IS_ODD[R["Sagittarius"]]
    assert not RASI_IS_ODD[signs[int(Graha.JUPITER)]]
    assert "same oddity" in seed["reason"]
    assert "different oddity" in seed["reason"]


def test_exercise_28_progression_is_vishnus_backward_trine():
    """The printed order is Sg, Le, Ar, Pi, Sc. Sg is dual, so Vishnu; the 9th
    from it is Le, even-footed, so backward. The trines of Sg run Sg, Le, Ar
    and then the next quadrant's, starting at Pi.
    """
    from hora.dasha.rasi.narayana import progression

    _longitudes, signs, _lagna = _chart_26()
    occupants = {g for g, sign in signs.items() if sign == R["Sagittarius"]}
    assert not occupants

    got = progression(R["Sagittarius"], occupants)
    assert got.god == "Vishnu"
    assert got.direction == "backward"
    assert [ABBR[s] for s in got.signs][:5] == [a for a, _y in EX28_LENGTHS]


@pytest.mark.parametrize("abbr,years", EX28_LENGTHS)
def test_exercise_28_lengths(abbr, years):
    """Three of the five need exception 2: Le for an exalted Sun, and Ar and
    Sc for an exalted Mars. All three exaltations are unambiguous by degree as
    well as by sign, so D-52 does not touch this answer.
    """
    from hora.charts.colord import stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_26()
    rasi = BY_ABBR[abbr]
    lord = (stronger(rasi, longitudes, purpose="arudha").winner
            if rasi in (R["Scorpio"], R["Aquarius"]) else int(RASI_LORD[rasi]))
    got = dasa_length(rasi, lord, signs[lord],
                      sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why


def test_exercise_28_pins_the_co_lord_cascade_a_third_time():
    """Scorpio again, and again the answer forces the choice. Mars in Cp is
    three houses on and exalted, giving 3; Ketu in Cn is nine, giving 8.
    """
    from hora.charts.colord import stronger
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_26()
    mars, ketu = int(Graha.MARS), int(Graha.KETU)
    assert stronger(R["Scorpio"], longitudes, purpose="arudha").winner == mars
    assert dasa_length(R["Scorpio"], mars, signs[mars], "exalted").years == 3
    assert dasa_length(R["Scorpio"], ketu, signs[ketu]).years == 8


def test_exercise_28_the_dates_the_answer_prints():
    """"Sg (11 years): May 1971 - May 1982" through "Sc (03 years): May 2001 -
    May 2004." The native's story is dated against these: an excellent career
    until 1997, which is exactly where Ar dasa ends.
    """
    year, spans = 1971, {}
    for abbr, years in EX28_LENGTHS:
        spans[abbr] = (year, year + years)
        year += years

    assert spans["Sg"] == (1971, 1982)
    assert spans["Le"] == (1982, 1987)
    assert spans["Ar"] == (1987, 1997)
    assert spans["Pi"] == (1997, 2001)
    assert spans["Sc"] == (2001, 2004)


def test_exercise_28_states_the_dasa_lagna_rule_for_a_seventh_seeded_chart():
    """"Because we started dasas from the 7th house instead of lagna, Narayana
    dasa shows the progression of the 7th house instead of lagna. So dasa
    lagna is the 7th from dasa rasi."

    The clearest statement of §18.4's rule anywhere in the chapter, and it
    arrives in an exercise answer rather than the section. It confirms from
    the other side what Chart 24 showed: seeded from lagna the dasa lagna is
    the dasa rasi; seeded from the 7th it is six signs away, always.
    """
    from hora.dasha.rasi.narayana import dasa_lagna, progression

    _longitudes, signs, lagna_sign = _chart_26()
    seed = R["Sagittarius"]
    assert seed == (lagna_sign + 6) % 12

    occupants = {g for g, sign in signs.items() if sign == seed}
    for rasi in progression(seed, occupants).signs:
        assert dasa_lagna(rasi, seed, lagna_sign) == (rasi + 6) % 12

    assert dasa_lagna(R["Aries"], seed, lagna_sign) == R["Libra"]
    assert dasa_lagna(R["Pisces"], seed, lagna_sign) == R["Virgo"]


def test_exercise_28_aries_dasa_was_good_because_libras_lord_is_exalted():
    """"During Ar dasa, dasa lagna is Li. Due to the exaltation of dasa lagna
    lord Venus (among other things), it was a very good dasa."

    Principle 11 -- the lord of dasa lagna exalted gives excellent results.
    Ar dasa runs May 1987 to May 1997, and the exercise says the career was
    excellent until 1997.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import (
        PARASARA_DASA_PRINCIPLES,
        dasa_lagna,
        paaka_rasi,
    )

    longitudes, _signs, lagna_sign = _chart_26()
    li = dasa_lagna(R["Aries"], R["Sagittarius"], lagna_sign)
    assert li == R["Libra"]

    venus = int(RASI_LORD[li])
    assert venus == int(Graha.VENUS)
    assert sign_dignity(venus, longitudes[venus]) == "exalted"
    assert paaka_rasi(li, longitudes) == R["Pisces"]

    eleventh = PARASARA_DASA_PRINCIPLES[10]
    assert "exalted" in eleventh["who"]
    assert eleventh["gives"] == "excellent results"


def test_exercise_28_pisces_dasa_is_read_entirely_from_virgo():
    """"During Pi dasa, dasa lagna is Vi. Lord of Vi is Mercury and he is in
    the 8th house from it... Jupiter in the 3rd from dasa lagna suggests
    failures. There are no malefics in the 3rd or 6th from dasa lagna. Saturn
    in the 9th house suggests loss of fortune... Ketu in the 11th house shows
    gains from foreign sources. Exalted 9th lord Venus is in the 7th house."

    Every house here is counted from Vi, which is six signs from the rasi
    whose dasa is running. Read from Pi instead, Saturn would sit in the 3rd
    and Ketu in the 5th, and none of the answer would follow.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_lagna

    longitudes, signs, lagna_sign = _chart_26()
    vi = dasa_lagna(R["Pisces"], R["Sagittarius"], lagna_sign)
    assert vi == R["Virgo"]

    mercury = int(RASI_LORD[vi])
    assert _house_from(vi, signs[mercury]) == 8
    assert _house_from(vi, signs[int(Graha.JUPITER)]) == 3
    assert _house_from(vi, signs[int(Graha.SATURN)]) == 9
    assert _house_from(vi, signs[int(Graha.KETU)]) == 11

    ninth = (vi + 8) % 12
    venus = int(RASI_LORD[ninth])
    assert venus == int(Graha.VENUS)
    assert sign_dignity(venus, longitudes[venus]) == "exalted"
    assert _house_from(vi, signs[venus]) == 7          # "he went abroad
                                                       # following his wife"

    # "There are no malefics in the 3rd or 6th from dasa lagna."
    malefics = {int(Graha.SUN), int(Graha.MARS), int(Graha.SATURN),
                int(Graha.RAHU), int(Graha.KETU)}
    for house in (3, 6):
        sign = (vi + house - 1) % 12
        assert not {g for g, s in signs.items() if s == sign} & malefics


def test_exercise_28_uses_principle_13_backwards():
    """"Lords of two dusthanas - Mars and Sun - are exalted and that suggests
    hard times."

    §18.4 states principle 13 one way only: a **debilitated** dusthana lord
    gives good results. The answer applies its converse. Of Virgo's three
    dusthana lords, the 8th's (Mars) and the 12th's (Sun) are exalted while
    the 6th's (Saturn) is not, which is why the answer says two and not three.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import (
        EXALTED_DUSTHANA_LORD_CONVERSE,
        PARASARA_DASA_PRINCIPLES,
        dasa_lagna,
    )

    longitudes, _signs, lagna_sign = _chart_26()
    vi = dasa_lagna(R["Pisces"], R["Sagittarius"], lagna_sign)

    lords = {house: int(RASI_LORD[(vi + house - 1) % 12])
             for house in (6, 8, 12)}
    exalted = {house for house, lord in lords.items()
               if sign_dignity(lord, longitudes[lord]) == "exalted"}
    assert exalted == {8, 12}
    assert lords[8] == int(Graha.MARS)
    assert lords[12] == int(Graha.SUN)

    thirteenth = PARASARA_DASA_PRINCIPLES[12]
    assert "debilitated" in thirteenth["who"]
    assert thirteenth["gives"] == "good results"
    assert "hard times" in EXALTED_DUSTHANA_LORD_CONVERSE


def test_ketu_in_the_eleventh_reads_as_foreign_gains_in_both_charts():
    """Principle 5 gives any planet in the 11th "gains". Example 69 and
    Exercise 28 both make Ketu's gains foreign ones, in the same words, so it
    is the book's reading rather than a turn of phrase in one place.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import (
        KETU_IN_THE_ELEVENTH_IS_FOREIGN,
        dasa_lagna,
    )

    assert "foreign" in KETU_IN_THE_ELEVENTH_IS_FOREIGN

    _l25, signs_25, lagna_25 = _chart_25()
    cp = dasa_lagna(R["Capricorn"], lagna_25, lagna_25)
    assert _house_from(cp, signs_25[int(Graha.KETU)]) == 11

    _l26, signs_26, lagna_26 = _chart_26()
    vi = dasa_lagna(R["Pisces"], R["Sagittarius"], lagna_26)
    assert _house_from(vi, signs_26[int(Graha.KETU)]) == 11


def test_oi_122_names_every_reading_the_sixteen_principles_do_not_carry():
    """The gap has to be one register entry, not five constants nobody joins
    up. OI-122 tabulates all six readings and names every constant holding
    one, so a later chapter closing the gap closes it in one place.
    """
    from pathlib import Path

    from hora.dasha.rasi import narayana

    text = Path("docs/open-items.md").read_text(encoding="utf-8")
    start = text.index("### OI-122")
    entry = text[start:text.index("### OI-121", start)]

    for symbol in ("UNLISTED_DASA_LAGNA_READINGS",
                   "EXALTED_DUSTHANA_LORD_CONVERSE",
                   "KETU_IN_THE_ELEVENTH_IS_FOREIGN",
                   "MUNDANE_HOUSE_READINGS",
                   "ANTARDASA_ASPECT_RULE"):
        assert symbol in entry, symbol
        assert hasattr(narayana, symbol), symbol

    assert "Ex 69" in entry and "Exercise 28" in entry
    assert entry.count("\n|") >= 7          # header, divider and six readings


def test_every_reading_outside_the_sixteen_points_back_at_oi_122():
    """Each constant cites the entry, so reading the code leads to the gap
    rather than to a stray note.
    """
    from pathlib import Path

    source = Path("src/hora/dasha/rasi/narayana.py").read_text(encoding="utf-8")
    assert source.count("OI-122") == 5


# --------------------------------------------------------------------------
# §18.5 Narayana Dasa of Vargas
# --------------------------------------------------------------------------

def test_the_seed_house_of_a_varga_is_not_n_modulo_twelve():
    """"To get the seed of D-n, just take the nth house. If n is greater than
    12, subtract multiples of 12 from n."

    The section works six out longhand and one of them is the whole point:
    "The seed of D-24 is 24-12=12th house." `24 % 12` is 0, which is not a
    house. The rule is `1 + (n - 1) % 12`, and D-30 confirms it from the other
    side -- 30 - 24 = 6, two multiples subtracted, not one.
    """
    from hora.dasha.rasi.narayana import VARGA_SEED_HOUSE_EXAMPLES, seed_house

    assert VARGA_SEED_HOUSE_EXAMPLES == {11: 11, 16: 4, 27: 3, 30: 6,
                                         24: 12, 40: 4}
    for divisions, house in VARGA_SEED_HOUSE_EXAMPLES.items():
        assert seed_house(divisions) == house, divisions

    # The four named in the opening paragraph, all at or under 12.
    assert [seed_house(n) for n in (4, 7, 9, 10, 12)] == [4, 7, 9, 10, 12]

    # And the trap, stated as a difference rather than an assertion of ours.
    assert seed_house(24) == 12 != 24 % 12
    assert seed_house(12) == 12 != 12 % 12


def test_every_varga_we_compute_has_a_seed_house_in_range():
    """Five of our twenty-three divisions are multiples of twelve, so the
    naive reading would leave five charts with no seed house at all.
    """
    from hora.charts.vargas import VARGA_REGISTRY
    from hora.dasha.rasi.narayana import seed_house

    for code, entry in VARGA_REGISTRY.items():
        divisions = entry[2]
        assert 1 <= seed_house(divisions) <= 12, code

    naive = [code for code, entry in VARGA_REGISTRY.items()
             if entry[2] % 12 == 0]
    assert naive == ["D12", "D24", "D60", "D108", "D144"]


def test_the_seed_house_rationales_agree_with_the_arithmetic():
    """§18.5 explains why each varga has the seed it has -- D-9 dharma, D-10
    karma, D-7 procreation, D-4 and D-16 the home, D-12 and D-24 the evolution
    of self. The meanings are prose, but they have to match the formula or one
    of the two is wrong.
    """
    from hora.charts.vargas import VARGA_REGISTRY
    from hora.dasha.rasi.narayana import VARGA_SEED_RATIONALE, seed_house

    for entry in VARGA_SEED_RATIONALE:
        for code in entry["vargas"]:
            assert seed_house(VARGA_REGISTRY[code][2]) == entry["house"], code

    # The pairs the section makes a point of: same seed, different chart.
    paired = [e for e in VARGA_SEED_RATIONALE if len(e["vargas"]) == 2]
    assert {e["house"] for e in paired} == {4, 12}


def test_the_uses_the_section_names_for_each_vargas_dasa():
    """"We can use Narayana dasa of D-4 to time changes in residence... D-10
    to time events in career... D-24... learning and knowledge... D-9 to time
    marriage... D-7... happiness from children... D-12... relations with
    parents."
    """
    from hora.charts.vargas import VARGA_REGISTRY
    from hora.dasha.rasi.narayana import VARGA_DASA_USES

    assert set(VARGA_DASA_USES) == {"D4", "D10", "D24", "D9", "D7", "D12"}
    for code in VARGA_DASA_USES:
        assert code in VARGA_REGISTRY
    assert "career" in VARGA_DASA_USES["D10"]
    assert "parents" in VARGA_DASA_USES["D12"]


def test_the_varga_lagna_reads_the_seed_house_in_the_rasi_chart():
    """§18.5's procedure, steps 2 and 4: "Take that house in rasi chart...
    Take the rasi occupied by him in the divisional chart of interest as
    lagna."

    Two charts, one step apart, and collapsing them is the mistake the
    procedure is worded to prevent. On Chart 26, D-12 and D-24 share the 12th
    house as their seed and so share Taurus and Venus -- but Venus sits in
    different rasis in the two vargas, so their dasas start from different
    lagnas.
    """
    from hora.charts.vargas import varga
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import VARGA_PROCEDURE, varga_lagna

    longitudes, signs, lagna_sign = _chart_26()
    assert len(VARGA_PROCEDURE) == 4
    assert "in rasi chart" in VARGA_PROCEDURE[1]

    results = {}
    for code, divisions in (("D12", 12), ("D24", 24)):
        varga_signs = {g: varga(lon, code).sign for g, lon in longitudes.items()}
        got = varga_lagna(divisions, lagna_sign, varga_signs)
        assert got["seed_house"] == 12
        assert got["seed_rasi"] == R["Taurus"]           # from the rasi chart
        assert got["lord"] == int(Graha.VENUS)
        assert int(RASI_LORD[got["seed_rasi"]]) == got["lord"]
        results[code] = got["lagna"]

    assert results["D12"] != results["D24"]
    assert signs[int(Graha.VENUS)] == R["Pisces"]        # and neither is D-1's


def test_the_varga_lagna_refuses_a_co_owned_seed_rather_than_assuming():
    """Step 3: "Find its lord. Take the stronger lord in the case of Aq and
    Sc."

    Chart 26's D-9 seeds on the 9th house, which is Aquarius, so the caveat is
    live rather than hypothetical. §15.5.1 gives Rahu; `RASI_LORD` gives
    Saturn; the two put the varga lagna seven signs apart. Defaulting would
    not be a shade of wrong, it would be a different dasa sequence, so
    `varga_lagna` refuses instead.
    """
    import pytest as _pytest

    from hora.charts.colord import stronger
    from hora.charts.vargas import varga
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import NarayanaError, varga_lagna

    longitudes, _signs, lagna_sign = _chart_26()
    varga_signs = {g: varga(lon, "D9").sign for g, lon in longitudes.items()}

    with _pytest.raises(NarayanaError, match="Saturn and Rahu"):
        varga_lagna(9, lagna_sign, varga_signs)

    chosen = stronger(R["Aquarius"], longitudes, purpose="arudha").winner
    assert chosen == int(Graha.RAHU)
    by_rule = varga_lagna(9, lagna_sign, varga_signs, lord=chosen)
    by_default = varga_lagna(9, lagna_sign, varga_signs,
                             lord=int(Graha.SATURN))
    assert by_rule["lagna"] == R["Leo"]
    assert by_default["lagna"] == R["Capricorn"]
    assert (by_rule["lagna"] - by_default["lagna"]) % 12 == 7


def test_a_vargas_narayana_dasa_runs_the_ordinary_rules_from_that_lagna():
    """Step 4: "find Narayana dasa of the divisional chart just as if it were
    a rasi chart. Use the rules explained in the previous sections."

    Nothing about §18.2.1 to §18.3 changes; only where lagna is. So the
    varga's own dasa seed is still the stronger of that lagna and the 7th from
    it, and the progression still comes from its modality and the 9th house.
    """
    from hora.charts.vargas import varga
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_seed, progression, varga_lagna

    longitudes, _signs, lagna_sign = _chart_26()
    varga_signs = {g: varga(lon, "D10").sign for g, lon in longitudes.items()}
    varga_longitudes = {g: varga(lon, "D10").longitude
                        for g, lon in longitudes.items()}

    got = varga_lagna(10, lagna_sign, varga_signs)
    assert got["seed_house"] == 10
    assert got["lord"] == int(Graha.JUPITER)
    assert got["lagna"] == R["Libra"]

    seed = dasa_seed(got["lagna"], varga_longitudes)
    assert seed["seed"] in (got["lagna"], (got["lagna"] + 6) % 12)
    occupants = {g for g, s in varga_signs.items() if s == seed["seed"]}
    order = progression(seed["seed"], occupants).signs
    assert len(set(order)) == 12
    assert order[0] == seed["seed"]


def test_a_varga_dasa_has_no_dasa_lagna_and_saying_so_is_the_whole_warning():
    """"Narayana dasa of vargas is not the progression of lagna or the 7th
    house. So taking dasa rasi or the 7th from it as lagna and analyzing dasas
    is has no technical basis. It applies only the rasi chart."

    Every §18.4 reading hangs off `dasa_lagna`, so refusing there refuses the
    lot -- the paaka rasi, the thirds, and all sixteen principles. The rasi
    chart is untouched.
    """
    import pytest as _pytest

    from hora.dasha.rasi.narayana import (
        VARGA_INTERPRETATION_WARNING,
        NarayanaError,
        dasa_lagna,
    )

    for divisions in (2, 9, 10, 12, 24, 144):
        with _pytest.raises(NarayanaError, match="no dasa lagna"):
            dasa_lagna(R["Capricorn"], R["Taurus"], R["Taurus"],
                       divisions=divisions)

    assert dasa_lagna(R["Capricorn"], R["Taurus"], R["Taurus"]) == \
        R["Capricorn"]
    assert dasa_lagna(R["Capricorn"], R["Taurus"], R["Taurus"],
                      divisions=1) == R["Capricorn"]
    assert "no technical basis" in VARGA_INTERPRETATION_WARNING


def test_the_warning_is_kept_with_its_two_printed_slips():
    """"analyzing dasas is has no technical basis" and "It applies only the
    rasi chart". Both read as slips for "dasas has" and "only to the rasi
    chart". Kept as printed -- the meaning is not in doubt, and silently
    tidying a quotation is how a register stops being one.
    """
    from hora.dasha.rasi.narayana import VARGA_INTERPRETATION_WARNING

    assert "dasas is has no technical basis" in VARGA_INTERPRETATION_WARNING
    assert "It applies only the rasi chart" in VARGA_INTERPRETATION_WARNING
