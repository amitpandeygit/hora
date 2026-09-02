"""Chapter 20 — Sudasa, the Sree Lagna Kendradi Rasi Dasa.

Chapter 19 promised this one twice: §19.3 said it is Lagna Kendradi seeded
from Sree Lagna, §19.4 said it outranks Lagna Kendradi for the matter both
read. So the walk and the lengths are borrowed, and what is tested here is
what chapter 20 adds — a seed that needs no comparison, a direction taken
from SL itself, and a first dasa that is already partly spent at birth.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_NAMES

R = {name: i for i, name in enumerate(RASI_NAMES)}
ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def _chart(number):
    """A recomputable book chart, with its Sree Lagna."""
    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.charts.special_lagna import sree_lagna
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(number)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name=f"Chart {number}", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    longitudes = {int(g): p.longitude for g, p in computed.positions.items()}
    return (longitudes,
            {g: int(lon // 30) for g, lon in longitudes.items()},
            computed.lagna_rasi,
            sree_lagna(longitudes[int(Graha.MOON)], computed.lagna_longitude))


def test_the_three_names_the_chapter_gives_it():
    """"Sudasa is a rasi dasa. It is also called 'Sree Lagna Kendradi Rasi
    Dasa' or simply 'Rasi Dasa'."

    The third is a trap: "Rasi Dasa" unqualified means this one specifically,
    not the category Narayana and Lagna Kendradi also belong to.
    """
    from hora.dasha.rasi.sudasa import NAMES

    assert NAMES == ("Sudasa", "Sree Lagna Kendradi Rasi Dasa", "Rasi Dasa")


def test_what_the_three_rasi_dasas_are_each_for():
    """Narayana is general purpose, Lagna Kendradi shows material success, and
    Sudasa is the sharpest of the three — money, power and authority.
    """
    from hora.dasha.rasi.kendradi import SHOWS_MATERIAL_SUCCESS
    from hora.dasha.rasi.narayana import NARAYANA_IS_THE_MOST_IMPORTANT_PHALITA_DASA
    from hora.dasha.rasi.sudasa import SHOWS

    assert "general purpose" in NARAYANA_IS_THE_MOST_IMPORTANT_PHALITA_DASA or \
        "most important phalita dasa" in NARAYANA_IS_THE_MOST_IMPORTANT_PHALITA_DASA
    assert "material success" in SHOWS_MATERIAL_SUCCESS
    assert "money, power and authority" in SHOWS
    assert "financial matters" in SHOWS


def test_the_three_claims_are_stated_as_consequences():
    """"If a political leader occupies a post of power, he **must** be
    enjoying a favorable dasa as per Sudasa."

    Three of them, and all three say "must". They are the strongest
    falsifiable statements the book makes about any dasa, and a layer that
    softens them to a tendency says less than the book does.
    """
    from hora.dasha.rasi.sudasa import DIAGNOSTIC_CLAIMS

    assert len(DIAGNOSTIC_CLAIMS) == 3
    favourable = [c for c in DIAGNOSTIC_CLAIMS if "favorable" in c["implies"]
                  and "unfavorable" not in c["implies"]]
    assert len(favourable) == 2
    unfavourable = [c for c in DIAGNOSTIC_CLAIMS
                    if "unfavorable" in c["implies"]]
    assert len(unfavourable) == 1
    assert "tight finances" in unfavourable[0]["observed"]


def test_the_seed_is_sree_lagnas_rasi_with_no_comparison():
    """"In Sudasa, dasas start from the sign containing Sree Lagna."

    §18.2.1 and §19.2 both send their seed to §15.5.2's stronger-of-lagna-and-
    7th cascade. This one does not: the seed is where SL falls, full stop, so
    there is nothing for §15.5.2 to decide and nothing for §15.5.1 either.
    """
    import inspect

    from hora.dasha.rasi import sudasa

    source = inspect.getsource(sudasa)
    assert "dasa_seed" not in source
    assert "rasi_strength" not in source
    assert "colord" not in source

    _lon, _signs, _lagna, sl = _chart(34)
    got = sudasa.progression(int(sl // 30), sl)
    assert got.sree_lagna == int(sl // 30)
    assert got.signs[0] == got.sree_lagna


def test_the_direction_comes_from_sree_lagnas_own_oddity():
    """"The direction of reckoning dasas is forward or backward based on
    whether SL is in an odd sign or an even sign. NOTE: We are talking about
    odd and even signs here and not about odd-footed and even-footed signs."

    §19.2 had the same sentence with lagna in place of SL, and named lagna
    where its own rule 1 had named the seed — harmlessly, since the two always
    share parity. Here the seed *is* SL, so the rule names it and there is
    nothing to reconcile.
    """
    from hora.core.const import RASI_IS_ODD
    from hora.dasha.rasi.sudasa import DIRECTION_RULE, direction_of, progression

    assert "not about odd-footed" in DIRECTION_RULE
    for rasi in range(12):
        expected = "forward" if RASI_IS_ODD[rasi] else "backward"
        assert direction_of(rasi) == expected
        assert progression(rasi).direction == expected


def test_the_walk_is_chapter_19s_unchanged():
    """Rules 3 to 5 are §19.2's rules 3 to 5 with SL for the dasa seed, so the
    order comes from `kendradi.house_signs` rather than being restated.
    """
    from hora.dasha.rasi.kendradi import HOUSE_ORDER, house_signs
    from hora.dasha.rasi.sudasa import progression

    for rasi in range(12):
        got = progression(rasi)
        assert got.houses == HOUSE_ORDER == (1, 4, 7, 10, 2, 5, 8, 11,
                                             3, 6, 9, 12)
        assert got.signs == house_signs(rasi, got.direction)
        assert set(got.signs) == set(range(12))
        assert got.group_names[:4] == ("kendra",) * 4
        assert got.group_names[4:8] == ("panaphara",) * 4
        assert got.group_names[8:] == ("apoklima",) * 4


def test_only_a_fraction_of_the_first_dasa_is_left_at_birth():
    """"Only a fraction of first dasa is left at birth. This fraction is found
    using the formula: (30 - SL's advancement in its sign)/30."

    The first balance the book has put on a rasi dasa — Narayana and Lagna
    Kendradi both start their first period whole. It behaves like a nakshatra
    dasa's balance: SL at the very start of a rasi leaves the whole dasa, at
    the very end almost none.
    """
    from hora.dasha.rasi.sudasa import (
        FIRST_DASA_IS_PARTLY_SPENT,
        first_dasa_fraction,
    )

    assert "(30 - SL's advancement in its sign)/30" in FIRST_DASA_IS_PARTLY_SPENT

    assert first_dasa_fraction(0.0) == 1.0
    assert first_dasa_fraction(15.0) == 0.5
    assert first_dasa_fraction(30.0) == 1.0            # 0 degrees of Taurus
    assert first_dasa_fraction(45.0) == 0.5
    assert 0.0 < first_dasa_fraction(29.9999) < 0.001

    for degrees in (0.0, 7.5, 15.0, 22.5, 29.0):
        assert first_dasa_fraction(degrees) == pytest.approx((30 - degrees) / 30)


def test_a_progression_without_a_longitude_refuses_to_assume_a_whole_first_dasa():
    """§20.2 says some of the first dasa is always spent, so a caller with
    only a sign cannot be handed 1.0 — that would be the one answer the rule
    rules out. `first_dasa_fraction` on the result is None instead.
    """
    from hora.dasha.rasi.sudasa import progression

    assert progression(R["Taurus"]).first_dasa_fraction is None
    assert progression(R["Taurus"], 32.3581).first_dasa_fraction == \
        pytest.approx((30 - 2.3581) / 30)


def test_a_longitude_that_contradicts_the_sign_is_refused():
    from hora.dasha.rasi.sudasa import SudasaError, progression

    with pytest.raises(SudasaError, match="Taurus"):
        progression(R["Taurus"], 200.0)


def test_the_lengths_are_still_18_2_2s():
    """Rule 6 is §19.2's rule 6 again — "just like in Narayana dasa" — so the
    only thing chapter 20 changes about a length is that the first one is
    scaled by rule 7's fraction.
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length
    from hora.dasha.rasi.sudasa import LENGTHS_ARE_NARAYANAS, progression

    assert "just like in Narayana dasa" in LENGTHS_ARE_NARAYANAS

    longitudes, signs, _lagna, sl = _chart(34)
    got = progression(int(sl // 30), sl)
    first = got.signs[0]
    lord = int(RASI_LORD[first])
    whole = dasa_length(first, lord, signs[lord],
                        sign_dignity(lord, longitudes[lord])).years
    assert whole == 9                                   # Table 41's Taurus
    assert got.first_dasa_fraction is not None
    assert whole * got.first_dasa_fraction < whole


def test_chapter_19s_two_forward_references_now_resolve():
    """§19.3: "Sudasa is also a Kendradi Rasi Dasa, but started from Sree
    Lagna instead of lagna." §5.7 had recorded `SREE_LAGNA_USED_IN = "Sudasa"`
    before either chapter existed. Both now point at something built.
    """
    from hora.charts.special_lagna import SREE_LAGNA_USED_IN
    from hora.dasha.rasi.kendradi import (
        SUDASA_IS_KENDRADI_FROM_SREE_LAGNA,
        SUDASA_IS_SUPERIOR,
    )
    from hora.dasha.rasi.sudasa import NAMES, progression

    assert SREE_LAGNA_USED_IN == "Sudasa"
    assert NAMES[0] == "Sudasa"
    assert "Kendradi Rasi Dasa" in NAMES[1]
    assert "also a Kendradi Rasi Dasa" in SUDASA_IS_KENDRADI_FROM_SREE_LAGNA
    assert "superior dasa" in SUDASA_IS_SUPERIOR
    assert callable(progression)


def test_20_2_does_not_restate_19_2s_saturn_and_ketu_exceptions():
    """See OI-126, and it is not hypothetical.

    §19.2 rule 2 carried two exceptions; §20.2 rule 2 is the same sentence
    with SL for lagna, the NOTE kept, and both exceptions dropped. On Chart 8
    that decides the whole order: its Sree Lagna and its Lagna Kendradi seed
    are both Scorpio, Ketu sits there, and chapter 19's exception reverses
    Lagna Kendradi to forward. Sudasa, restating no exception, runs backward —
    and the two orders share only the first period.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi import kendradi, sudasa
    from hora.dasha.rasi.narayana import dasa_seed

    longitudes, signs, lagna_sign, sl = _chart(8)
    seed = dasa_seed(lagna_sign, longitudes)["seed"]
    assert seed == int(sl // 30) == R["Scorpio"]

    occupants = {g for g, s in signs.items() if s == seed}
    assert int(Graha.KETU) in occupants

    by_kendradi = kendradi.progression(seed, lagna_sign, occupants)
    assert by_kendradi.exception == "Ketu"
    assert by_kendradi.direction == "forward"

    by_sudasa = sudasa.progression(int(sl // 30), sl)
    assert by_sudasa.direction == "backward"
    assert by_sudasa.signs[0] == by_kendradi.signs[0]
    assert by_sudasa.signs[1:] != by_kendradi.signs[1:]

    # and if the exception did carry over, the two would be identical
    assert kendradi.house_signs(int(sl // 30), "forward") == by_kendradi.signs


def test_sudasa_and_lagna_kendradi_usually_walk_differently():
    """The two dasas coincide only when SL happens to fall in the sign
    §15.5.2 would have chosen anyway, and then only if no exception fires.
    Across the book's recomputable charts they differ far more often than not,
    so they are two readings rather than one under two names.
    """
    from hora.charts.book import recomputable
    from hora.dasha.rasi import kendradi, sudasa
    from hora.dasha.rasi.narayana import dasa_seed

    agree = disagree = 0
    for number in recomputable():
        longitudes, signs, lagna_sign, sl = _chart(number)
        seed = dasa_seed(lagna_sign, longitudes)["seed"]
        if seed is None:
            continue
        occupants = {g for g, s in signs.items() if s == seed}
        by_kendradi = kendradi.progression(seed, lagna_sign, occupants)
        by_sudasa = sudasa.progression(int(sl // 30), sl)
        if by_sudasa.signs == by_kendradi.signs:
            agree += 1
        else:
            disagree += 1

    assert agree + disagree >= 20
    assert disagree > agree * 3
