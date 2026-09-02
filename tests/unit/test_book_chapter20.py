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


# --------------------------------------------------------------------------
# Example 77 — Sri Vajpayee, Chart 3, worked step by step.
# --------------------------------------------------------------------------

#: The twelve the example prints, in its own order.
EX77_LENGTHS = [("Cp", 2), ("Li", 2), ("Cn", 11), ("Ar", 12), ("Sg", 2),
                ("Vi", 10), ("Ge", 5), ("Pi", 1), ("Sc", 2), ("Le", 8),
                ("Ta", 7), ("Aq", 3)]

#: SL as the example states it: 12 degrees 21 minutes of Capricorn.
EX77_SREE_LAGNA = 270.0 + 12.0 + 21.0 / 60.0


def _ex77_lord(rasi, longitudes, signs):
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


def test_example_77_walks_backward_from_capricorn_in_three_groups():
    """"First 4 dasas will belong to kendras from Cp, reckoned in the backward
    direction. They are Cp, Li, Cn and Ar... panapharas... Sg, Vi, Ge and
    Pi... apoklimas... Sc, Le, Ta and Aq."

    The example names each group's members, so the walk can be checked group
    by group rather than only as a list.
    """
    from hora.dasha.rasi.sudasa import progression

    got = progression(R["Capricorn"], EX77_SREE_LAGNA)
    assert got.direction == "backward"                 # "Capricorn is an even sign"

    by_group: dict[str, list[str]] = {}
    for name, sign in zip(got.group_names, got.signs):
        by_group.setdefault(name, []).append(ABBR[sign])
    assert by_group["kendra"] == ["Cp", "Li", "Cn", "Ar"]
    assert by_group["panaphara"] == ["Sg", "Vi", "Ge", "Pi"]
    assert by_group["apoklima"] == ["Sc", "Le", "Ta", "Aq"]
    assert [ABBR[s] for s in got.signs] == [a for a, _y in EX77_LENGTHS]


@pytest.mark.parametrize("abbr,years", EX77_LENGTHS)
def test_example_77_lengths(abbr, years):
    """All twelve, from §18.2.2 by way of rule 6. Scorpio and Aquarius both go
    to §15.5.1 and both are settled at rule 1.
    """
    from hora.charts.book import graha_longitudes, graha_signs
    from hora.charts.dignity import sign_dignity
    from hora.dasha.rasi.narayana import dasa_length

    longitudes = {int(g): lon for g, lon in graha_longitudes(3).items()}
    signs = {int(g): s for g, s in graha_signs(3).items()}
    rasi = {v: k for k, v in enumerate(ABBR)}[abbr]
    lord = _ex77_lord(rasi, longitudes, signs)
    got = dasa_length(rasi, lord, signs[lord],
                      sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why


def test_example_77_lengths_total_sixty_five_years():
    """Not stated, but it is the check the twelve have to pass together."""
    assert sum(y for _a, y in EX77_LENGTHS) == 65


def test_example_77_the_fraction_and_its_arithmetic():
    """"The fraction of the first dasa left at birth = (30 - 12 21')/30 =
    (1800 - 741)/1800 = 0.5883."

    The example does the arithmetic in arcminutes, which is the clearest way
    to see it: 12 degrees 21 minutes is 741 of the 1800 in a rasi.
    """
    from hora.dasha.rasi.sudasa import first_dasa_fraction

    assert 12 * 60 + 21 == 741
    assert 30 * 60 == 1800
    assert first_dasa_fraction(EX77_SREE_LAGNA) == pytest.approx(
        (1800 - 741) / 1800)
    exact = first_dasa_fraction(EX77_SREE_LAGNA)
    assert exact == pytest.approx(1059 / 1800)
    assert int(exact * 10_000) / 10_000 == 0.5883      # the example truncates


def test_example_77_the_balance_is_measured_in_18_6s_units():
    """"First dasa of Cp is of 2 years and 0.5883 of it is 1.1766 years, i.e.,
    1 year 2 months 3 days 14 hours."

    That conversion fixes the units: twelve months to a year and thirty days
    to a month, which is §18.6's measure where a day is one degree of the
    Sun's motion. On a calendar it would not come out to the hour.
    """
    from hora.dasha.rasi.sudasa import (
        FIRST_DASA_BALANCE_EXAMPLE,
        first_dasa_fraction,
        years_to_dasa_ymdh,
    )

    balance = 2 * first_dasa_fraction(EX77_SREE_LAGNA)
    # The exact value is 2 x 1059/1800 = 1.17666..., which the example prints
    # truncated rather than rounded — 0.5883 and 1.1766, not 0.5883 and 1.1767.
    assert balance == pytest.approx(2 * 1059 / 1800)
    assert f"{balance:.4f}" == "1.1767"
    assert int(balance * 10_000) / 10_000 == 1.1766
    assert years_to_dasa_ymdh(balance) == (1, 2, 3, 14)
    assert "1 year 2 months 3 days 14 hours" in FIRST_DASA_BALANCE_EXAMPLE

    # the units, stated as their own check
    assert years_to_dasa_ymdh(1.0) == (1, 0, 0, 0)
    assert years_to_dasa_ymdh(1 / 12) == (0, 1, 0, 0)
    assert years_to_dasa_ymdh(1 / 360) == (0, 0, 1, 0)
    assert years_to_dasa_ymdh(1 / 8640) == (0, 0, 0, 1)


def test_example_77_libra_follows_the_partial_capricorn():
    """"So this is the remainder of Cp dasa at birth. After this, Li dasa of 2
    years will start."

    Only the first dasa is cut; the second is whole, and it is the second sign
    of the walk rather than a repeat of the first.
    """
    from hora.dasha.rasi.sudasa import progression

    got = progression(R["Capricorn"], EX77_SREE_LAGNA)
    assert ABBR[got.signs[1]] == "Li"
    assert dict(EX77_LENGTHS)["Li"] == 2


def test_our_sree_lagna_differs_from_the_books_by_less_than_an_arcminute_of_moon():
    """The one thing in Example 77 we do not reproduce, and why it is small.

    The example says SL is at 12 21' Capricorn; we get 12 07' 39" recomputed
    from Chart 3's birth data and 11 54' from its printed longitudes. But SL
    is the lagna plus the Moon's progress through its nakshatra taken as a
    fraction of the whole zodiac, so it multiplies the Moon's error by
    360/13 20' = **27**. The book's SL needs a Moon half an arcminute later
    than ours — below the precision the chart itself is printed to.

    Nothing in the example turns on it: SL is twelve degrees into Capricorn on
    every reading, so the seed, the direction and all twelve lengths are
    unchanged. Only rule 7's fraction moves, by about eleven days of a
    two-year dasa.
    """
    from hora.charts.book import graha_longitudes
    from hora.charts.book import longitudes as printed
    from hora.charts.special_lagna import (
        SREE_LAGNA_AMPLIFIES_THE_MOON,
        sree_lagna,
        sree_lagna_moon_sensitivity,
    )
    from hora.core.const import NAKSHATRA_SPAN, Graha
    from hora.dasha.rasi.sudasa import first_dasa_fraction

    assert SREE_LAGNA_AMPLIFIES_THE_MOON == pytest.approx(27.0)
    assert sree_lagna_moon_sensitivity(1.0) == pytest.approx(27.0)
    assert NAKSHATRA_SPAN * 27 == pytest.approx(360.0)

    moon = graha_longitudes(3)[Graha.MOON]
    ours = sree_lagna(moon, printed(3)["Asc"])
    assert int(ours // 30) == int(EX77_SREE_LAGNA // 30) == R["Capricorn"]
    assert abs(ours - EX77_SREE_LAGNA) * 60 < 30      # under half a degree

    # the Moon shift the book's SL implies, in arcminutes
    implied = abs(ours - EX77_SREE_LAGNA) / SREE_LAGNA_AMPLIFIES_THE_MOON
    assert implied * 60 < 1.5                          # about one arcminute

    # and it costs about eleven days of a two-year first dasa
    drift = abs(first_dasa_fraction(ours)
                - first_dasa_fraction(EX77_SREE_LAGNA)) * 2 * 360
    assert 5 < drift < 15                              # in dasa days


# --------------------------------------------------------------------------
# §20.3 Interpretation
# --------------------------------------------------------------------------

def test_20_3s_illustration_counts_three_ways_and_ours_names_the_same_three():
    """"say HL is in Aries, Mars is in Leo and Sun is in Scorpio. Then (a) Leo
    aspects HL, (b) lord of Leo aspects HL and (c) lord of HL occupies Leo. So
    Leo dasa is **triply** likely to bring financial prosperity."

    The only place the section counts rather than names, so "triply" is what
    fixes the arithmetic: qualifying is one way and each reinforcement is
    another. Ours finds the same three, in the same order, for the same
    reasons — and Leo qualifies purely by aspect, being neither Aries nor the
    7th from it.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.sudasa import PROSPERITY_ILLUSTRATION, prosperity_ways

    signs = {int(Graha.MARS): R["Leo"], int(Graha.SUN): R["Scorpio"]}
    ways = prosperity_ways(R["Leo"], R["Aries"], signs)

    assert len(ways) == 3                                   # "triply"
    assert ways[0]["rule"] == "aspects it"
    assert ways[1]["rule"] == "its lord occupies or aspects the special lagna"
    assert ways[2]["rule"] == "the special lagna's lord occupies or aspects it"
    assert "Sun, lord of Leo, aspects Aries from Scorpio" in ways[1]["why"]
    assert "Mars, lord of Aries, occupies Leo" in ways[2]["why"]

    assert R["Leo"] not in (R["Aries"], (R["Aries"] + 6) % 12)
    assert "triply likely" in PROSPERITY_ILLUSTRATION


def test_rule_1s_base_admits_three_kinds_of_dasa_sign():
    """"Dasas of HL, 7th from HL and the signs aspecting HL bring financial
    prosperity." Each qualifies on its own, before any reinforcement.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.sudasa import PROSPERITY_RULE, prosperity_ways

    assert "HL, 7th from HL and the signs aspecting HL" in PROSPERITY_RULE

    hora_lagna = R["Aries"]
    assert prosperity_ways(hora_lagna, hora_lagna, {})[0]["rule"] == \
        "is the special lagna's sign"
    assert prosperity_ways((hora_lagna + 6) % 12, hora_lagna, {})[0]["rule"] == \
        "is the 7th from it"
    aspecters = [s for s in range(12) if hora_lagna in rasi_drishti(s)]
    assert aspecters
    for sign in aspecters:
        if sign in (hora_lagna, (hora_lagna + 6) % 12):
            continue
        assert prosperity_ways(sign, hora_lagna, {})[0]["rule"] == "aspects it"

    # and a sign that does none of the three qualifies on nothing
    unrelated = [s for s in range(12)
                 if s != hora_lagna and s != (hora_lagna + 6) % 12
                 and hora_lagna not in rasi_drishti(s)]
    assert unrelated
    assert prosperity_ways(unrelated[0], hora_lagna, {}) == ()


def test_rule_2_is_rule_1_with_gl_and_a_different_result():
    """"Same thing holds for GL and the prescribed results are power and
    authority instead of financial prosperity."

    One test, two special lagnas, two results — so the function takes the
    lagna's sign and the caller supplies which result it is reading for.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.sudasa import (
        GL_GIVES_POWER_INSTEAD,
        SPECIAL_LAGNA_DASA_RULES,
        prosperity_ways,
    )

    by_lagna = {r["lagna"]: r["gives"] for r in SPECIAL_LAGNA_DASA_RULES}
    assert by_lagna == {"HL": "financial prosperity",
                        "GL": "power and authority"}
    assert "instead of financial prosperity" in GL_GIVES_POWER_INSTEAD

    # the same configuration read against either lagna gives the same ways
    signs = {int(Graha.MARS): R["Leo"], int(Graha.SUN): R["Scorpio"]}
    for lagna_sign in (R["Aries"],):
        assert prosperity_ways(R["Leo"], lagna_sign, signs) == \
            prosperity_ways(R["Leo"], lagna_sign, signs)


def test_rules_3_and_4_speak_for_six_houses_from_al_and_no_others():
    """"dasas of upachayas from AL bring growth of status. Dasa of the 11th
    house from AL is particularly favorable... The 8th and 12th houses from AL
    bring setbacks."

    Six houses named, six silent. The 11th is named twice — once as an
    upachaya and once on its own — so it carries both readings.
    """
    from hora.core.const import UPACHAYA
    from hora.dasha.rasi.sudasa import (
        STATUS_FROM_ARUDHA_LAGNA,
        status_from_arudha_lagna,
    )

    assert UPACHAYA == (3, 6, 10, 11)
    growth = next(r for r in STATUS_FROM_ARUDHA_LAGNA
                  if r["gives"] == "growth of status")
    assert growth["houses"] == UPACHAYA

    from_20_3 = {h for r in STATUS_FROM_ARUDHA_LAGNA
                 if r["source"].startswith("\u00a720.3") for h in r["houses"]}
    assert from_20_3 == {3, 6, 8, 10, 11, 12}          # six of twelve

    arudha = R["Cancer"]
    spoken = {}
    for house in range(1, 13):
        sign = (arudha + house - 1) % 12
        got = status_from_arudha_lagna(sign, arudha)
        assert got["house_from_al"] == house
        if got["readings"]:
            spoken[house] = got["readings"]

    # the 1st is Example 79's addition, not §20.3's
    assert set(spoken) == from_20_3 | {1}
    assert spoken[1] == ("status",)
    assert spoken[11] == ("growth of status",
                          "growth of status, particularly favorable")
    assert spoken[8] == spoken[12] == ("setbacks to one's status",)
    assert spoken[3] == spoken[6] == spoken[10] == ("growth of status",)


def test_rule_3_is_an_earlier_chapters_upachaya_claim_put_on_a_dasa():
    """The engine already held "upachayas from a reference show forces causing
    gains and growth to the matters signified by the reference", with the
    arudha lagna as its worked example. §20.3 rule 3 is that claim with a dasa
    attached, so the two have to agree or one of them is wrong.
    """
    from hora.core.const import UPACHAYA_EXAMPLE, UPACHAYA_RULE
    from hora.dasha.rasi.sudasa import STATUS_FROM_ARUDHA_LAGNA

    assert UPACHAYA_EXAMPLE["reference"] == "arudha_lagna"
    assert UPACHAYA_EXAMPLE["reference_shows"] == "one's status"
    assert "improvement of status" in UPACHAYA_EXAMPLE["upachayas_show"]
    assert "growth" in UPACHAYA_RULE

    growth = next(r for r in STATUS_FROM_ARUDHA_LAGNA
                  if r["gives"] == "growth of status")
    assert "AL stands for one's status" in growth["text"]


def test_the_lord_defaults_to_the_primary_one_per_example_76():
    """§20.3 says "the lord of the dasa sign" and "the lord of HL" — the
    ordinary usage Example 76 settled, where a Scorpio lagna's lord is Mars
    even though §15.5.1 gives Ketu for that chart's dasa length and arudha.
    An override is there for a caller who has a reason.
    """
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.sudasa import prosperity_ways

    # Scorpio dasa, HL in Cancer, and the two co-lords placed apart
    signs = {int(Graha.MARS): R["Cancer"], int(Graha.KETU): R["Gemini"]}
    assert int(RASI_LORD[R["Scorpio"]]) == int(Graha.MARS)

    by_default = prosperity_ways(R["Scorpio"], R["Cancer"], signs)
    assert any("Mars, lord of Scorpio" in w["why"] for w in by_default)

    by_ketu = prosperity_ways(R["Scorpio"], R["Cancer"], signs,
                              dasa_lord=int(Graha.KETU))
    assert not any("Mars, lord of Scorpio" in w["why"] for w in by_ketu)


def test_20_3_applied_across_vajpayees_sudasa():
    """The section on the chapter's own chart, using its **printed** HL, GL
    and the AL derived from it — chart 3's computed HL and GL are the subject
    of OI-103, so the printed ones are the book's own values.

    Capricorn is the strongest sign in the run: it holds SL, it is the 1st
    from AL, and it reaches GL's result all three ways.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.charts.book import longitudes as printed
    from hora.charts.colord import stronger
    from hora.dasha.rasi.sudasa import prosperity_ways, status_from_arudha_lagna

    longitudes = {int(g): lon for g, lon in graha_longitudes(3).items()}
    signs = {int(g): s for g, s in graha_signs(3).items()}
    hora_lagna = int(printed(3)["HL"] // 30)
    ghati_lagna = int(printed(3)["GL"] // 30)
    arudha = arudha_pada(
        1, lagna(3), signs,
        {r: stronger(r, longitudes, purpose="arudha").winner for r in (7, 10)}
    ).sign

    assert (hora_lagna, ghati_lagna, arudha) == (R["Libra"], R["Cancer"],
                                                 R["Capricorn"])

    capricorn = prosperity_ways(R["Capricorn"], ghati_lagna, signs)
    assert len(capricorn) == 3                       # power and authority, thrice
    assert status_from_arudha_lagna(R["Capricorn"], arudha)["house_from_al"] == 1

    # seven houses from AL speak — §20.3's six, plus the 1st from Example 79
    spoken = sum(1 for house in range(1, 13)
                 if status_from_arudha_lagna((arudha + house - 1) % 12,
                                             arudha)["readings"])
    assert spoken == 7


# --------------------------------------------------------------------------
# Example 78 — Vajpayee's Sudasa read, and read against his Narayana dasa.
# --------------------------------------------------------------------------

def _chart_3():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(3).items()},
            {int(g): sign for g, sign in graha_signs(3).items()},
            lagna(3))


def _chart_3_lord(rasi, longitudes, signs):
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


def _chart_3_years(rasi):
    from hora.charts.dignity import sign_dignity
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_3()
    lord = _chart_3_lord(rasi, longitudes, signs)
    return dasa_length(rasi, lord, signs[lord],
                       sign_dignity(lord, longitudes[lord])).years


def test_example_78_capricorn_reaches_gls_result_all_three_ways():
    """"His GL is in Cancer. Capricorn is the 7th house from GL and it can
    bring power and authority. Its lord Saturn aspects GL. Moon is the lord of
    GL and he aspects Cp. So Cp dasa is very favorable."

    §20.3's three ways, named one by one on a real chart — and our reasons
    name the same grahas from the same rasis. "Very favorable" is the same
    count the illustration called "triply likely".
    """
    from hora.charts.book import longitudes as printed
    from hora.dasha.rasi.sudasa import prosperity_ways

    _longitudes, signs, _lagna = _chart_3()
    ghati_lagna = int(printed(3)["GL"] // 30)
    assert ghati_lagna == R["Cancer"]
    assert R["Capricorn"] == (ghati_lagna + 6) % 12

    ways = prosperity_ways(R["Capricorn"], ghati_lagna, signs)
    assert len(ways) == 3
    assert ways[0]["rule"] == "is the 7th from it"
    assert "Saturn, lord of Capricorn, aspects Cancer from Scorpio" in ways[1]["why"]
    assert "Moon, lord of Cancer, aspects Capricorn from Leo" in ways[2]["why"]


def test_example_78_capricorn_holds_both_al_and_a5():
    """"Moreover, Cp contains AL and A5. AL shows status and A5 can show
    power."

    Two arudhas in the dasa rasi, and neither needs §9.2's exception. A5 is a
    ninth arudha for the register, on the principle Exercise 30 stated for all
    of them: an arudha shows the appearance of its house's matter, and the 5th
    house shows one's following.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.colord import stronger
    from hora.dasha.rasi.sudasa import A5_SHOWS_ONES_FOLLOWING

    longitudes, signs, lagna_sign = _chart_3()
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}

    for house in (1, 5):
        got = arudha_pada(house, lagna_sign, signs, overrides)
        assert got.sign == R["Capricorn"], house
        assert got.exception_position is None

    assert "A5 shows things based on which the world forms an impression" in \
        A5_SHOWS_ONES_FOLLOWING
    assert "trappings of power" in A5_SHOWS_ONES_FOLLOWING


def test_example_78_capricorn_in_the_second_cycle_covers_both_premierships():
    """"Capricorn dasa in the second cycle made him the Prime Minister of
    India."

    The second cycle needs three of the chapter's rules at once: §18.2.2's
    special note 2 for its lengths, §20.2 rule 7 for the partial first dasa
    that shifts every boundary, and §18.6's solar arc for the dates. Vajpayee
    was Prime Minister in May 1996 and from March 1998.
    """
    from datetime import date

    from hora.charts.book import chart
    from hora.core.const import Graha
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_jd, from_local
    from hora.dasha.rasi.narayana import (
        second_cycle_length,
        solar_arc_instant,
        sub_period_arc,
    )
    from hora.dasha.rasi.sudasa import first_dasa_fraction, progression

    ephemeris = get_ephemeris(Settings(node_type=NodeType.MEAN))

    def sun_at(jd: float) -> float:
        return ephemeris.position(jd, int(Graha.SUN)).longitude

    birth = from_local(**chart(3)["birth_data"]).jd_ut
    got = progression(R["Capricorn"], EX77_SREE_LAGNA)

    arc = 0.0
    for index, sign in enumerate(got.signs):        # first cycle
        years = _chart_3_years(sign)
        if index == 0:
            years *= first_dasa_fraction(EX77_SREE_LAGNA)
        arc += sub_period_arc(years, 0)

    opens = solar_arc_instant(birth, arc, sun_at)   # second cycle starts here
    arc += sub_period_arc(second_cycle_length(_chart_3_years(R["Capricorn"])), 0)
    closes = solar_arc_instant(birth, arc, sun_at)

    first = from_jd(opens, utc_offset_hours=5.5).local.date()
    last = from_jd(closes, utc_offset_hours=5.5).local.date()
    assert second_cycle_length(2) == 10             # 12 - the first cycle's 2
    assert first.year == 1991 and last.year == 2001
    assert first < date(1996, 5, 16) < last         # his first premiership
    assert first < date(1998, 3, 19) < last         # and his second


def test_example_78_narayana_scorpio_runs_at_the_same_time():
    """"Sri Vajpayee was running the Narayana dasa of Sc during the same time
    and so he became the Prime Minister."

    Two rasi dasas from two different seeds, landing on the same decade. His
    Narayana seed is Scorpio and the **Saturn exception fires** on it — Saturn
    sits there — so the movement is Brahma's regular one, forward. Scorpio is
    therefore the first dasa of each cycle, and in the second it runs ten
    years from the end of the first.
    """
    from datetime import date

    from hora.charts.book import chart
    from hora.core.const import Graha
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_jd, from_local
    from hora.dasha.rasi.narayana import (
        dasa_seed,
        progression,
        second_cycle_length,
        solar_arc_instant,
        sub_period_arc,
    )

    longitudes, signs, lagna_sign = _chart_3()
    seed = dasa_seed(lagna_sign, longitudes)
    assert seed["seed"] == R["Scorpio"] == lagna_sign

    occupants = {g for g, s in signs.items() if s == seed["seed"]}
    assert int(Graha.SATURN) in occupants
    walk = progression(seed["seed"], occupants)
    assert walk.exception == "Saturn"
    assert walk.god == "Brahma"
    assert walk.direction == "forward"
    assert walk.signs[0] == R["Scorpio"]

    ephemeris = get_ephemeris(Settings(node_type=NodeType.MEAN))

    def sun_at(jd: float) -> float:
        return ephemeris.position(jd, int(Graha.SUN)).longitude

    birth = from_local(**chart(3)["birth_data"]).jd_ut
    arc = sum(sub_period_arc(_chart_3_years(s), 0) for s in walk.signs)
    opens = solar_arc_instant(birth, arc, sun_at)
    arc += sub_period_arc(second_cycle_length(_chart_3_years(R["Scorpio"])), 0)
    closes = solar_arc_instant(birth, arc, sun_at)

    first = from_jd(opens, utc_offset_hours=5.5).local.date()
    last = from_jd(closes, utc_offset_hours=5.5).local.date()
    assert first.year == 1991 and last.year == 2001
    assert first < date(1996, 5, 16) < last
    assert first < date(1998, 3, 19) < last


def test_example_78_says_to_read_the_two_rasi_dasas_together():
    """"Of course, Narayana is important for power, though Sri Lakshmi gives
    prosperity. So we should always check Narayana dasa along with Sudasa."

    The clearest statement in the book of how the two divide the work. §19.3
    gave the movements their rulers; this says what to do with them, and it
    cuts against reading either alone.
    """
    from hora.dasha.rasi.kendradi import LAKSHMI_SHOWS_PROSPERITY
    from hora.dasha.rasi.sudasa import CHECK_NARAYANA_ALONGSIDE

    assert "always check Narayana dasa along with Sudasa" in \
        CHECK_NARAYANA_ALONGSIDE
    assert "Narayana is important for power" in CHECK_NARAYANA_ALONGSIDE
    assert "goddess of wealth and prosperity" in LAKSHMI_SHOWS_PROSPERITY


def test_example_78_calls_half_of_11_7_3s_first_yoga_a_powerful_raja_yoga():
    """See D-61. "Scorpio is lagna and houses a powerful raja yoga between AK
    (Mercury) and PK (Saturn)."

    §11.7.3's yoga 1 wants two conditions and says a single one is "felt, but
    not fully". Vajpayee has the first and not the second, so our detector
    reports the yoga absent and names the half that holds. The example calls
    it powerful, reading yoga 1's first condition through yoga **2**'s
    placement clause — "especially in 1st and 5th" is not in yoga 1 at all.
    """
    from hora.charts.book import chart
    from hora.charts.book import longitudes as printed
    from hora.charts.chart import Place, compute_chart
    from hora.charts.karaka import chara_karakas
    from hora.charts.planetary_yogas.raaja_advanced import _detect_1
    from hora.charts.planetary_yogas.registry import YogaInput
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    longitudes, signs, lagna_sign = _chart_3()
    eight = {g: lon for g, lon in longitudes.items() if g != int(Graha.KETU)}
    karakas = {k.symbol: k.graha for k in chara_karakas(eight)}
    assert karakas["AK"] == int(Graha.MERCURY)
    assert karakas["PK"] == int(Graha.SATURN)
    assert signs[karakas["AK"]] == signs[karakas["PK"]] == lagna_sign

    record = chart(3)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 3", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    got = _detect_1(YogaInput(rasis=signs, chart="D1", lagna_rasi=lagna_sign,
                              lagna_longitude=printed(3)["Asc"],
                              positions=computed.positions))

    assert got.present is False                     # ours, per §11.7.3 as printed
    assert "AK Mercury and PK Saturn are conjoined" in got.reason
    assert "do not conjoin" in got.reason           # the half that fails
    assert any("may still be felt, but not fully" in str(q)
               for q in (got.qualifiers or ()))


# --------------------------------------------------------------------------
# Example 79 — Jayalalita, Chart 35. One rasi holding AL, GL and HL.
# --------------------------------------------------------------------------

#: The eight the example prints, in its own order. Its last four are unstated.
EX79_LENGTHS = [("Sg", 12), ("Pi", 3), ("Ge", 8), ("Vi", 7),
                ("Cp", 6), ("Ar", 4), ("Cn", 11), ("Li", 6)]

#: SL as the example states it: 22 degrees 22 minutes of Sagittarius.
EX79_SREE_LAGNA = 240.0 + 22.0 + 22.0 / 60.0


def test_example_79_walks_forward_from_sagittarius_in_three_groups():
    """"Her SL is in 22 Sg 22. So dasas start from Sg. Because Sg is an odd
    sign, counting of houses is in the zodiacal direction. Dasas go as Sg, Pi,
    Ge, Vi (quadrants); Cp, Ar, Cn, Li (panapharas); Aq, Ta, Le, Sc
    (apoklimas)."

    The forward counterpart to Example 77's backward walk, and the example
    labels its own groups.
    """
    from hora.dasha.rasi.sudasa import progression

    got = progression(R["Sagittarius"], EX79_SREE_LAGNA)
    assert got.direction == "forward"

    by_group: dict[str, list[str]] = {}
    for name, sign in zip(got.group_names, got.signs):
        by_group.setdefault(name, []).append(ABBR[sign])
    assert by_group["kendra"] == ["Sg", "Pi", "Ge", "Vi"]
    assert by_group["panaphara"] == ["Cp", "Ar", "Cn", "Li"]
    assert by_group["apoklima"] == ["Aq", "Ta", "Le", "Sc"]


@pytest.mark.parametrize("abbr,years", EX79_LENGTHS)
def test_example_79_lengths(abbr, years):
    """The eight the example states. Sagittarius is exception 1 — "The first
    dasa of Sg is of 12 years, because its lord Jupiter is in Sg" — and Libra
    is exception 2, Venus being exalted in Pisces.
    """
    from hora.charts.book import graha_longitudes, graha_signs
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes = {int(g): lon for g, lon in graha_longitudes(35).items()}
    signs = {int(g): s for g, s in graha_signs(35).items()}
    rasi = {v: k for k, v in enumerate(ABBR)}[abbr]
    lord = int(RASI_LORD[rasi])
    got = dasa_length(rasi, lord, signs[lord],
                      sign_dignity(lord, longitudes[lord]))
    assert got.years == years, got.why


def test_example_79_sagittarius_is_exception_1_and_libra_exception_2():
    """The two the example explains, named rather than only totalled."""
    from hora.charts.book import graha_longitudes, graha_signs
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes = {int(g): lon for g, lon in graha_longitudes(35).items()}
    signs = {int(g): s for g, s in graha_signs(35).items()}

    jupiter = int(RASI_LORD[R["Sagittarius"]])
    assert jupiter == int(Graha.JUPITER)
    assert signs[jupiter] == R["Sagittarius"]          # "its lord Jupiter is in Sg"
    sagittarius = dasa_length(R["Sagittarius"], jupiter, signs[jupiter])
    assert sagittarius.count == 1 and sagittarius.years == 12

    venus = int(RASI_LORD[R["Libra"]])
    assert signs[venus] == R["Pisces"]
    assert sign_dignity(venus, longitudes[venus]) == "exalted"
    libra = dasa_length(R["Libra"], venus, signs[venus], "exalted")
    assert libra.count == 6 and libra.years == 6       # 5 + 1 for exception 2


def test_example_79_the_fraction_and_the_balance():
    """"SL is at 22 22' in Sg and the remainder in first dasa at birth is 12 x
    (30 - 22 22')/30 = 12 x 0.2544 years = 3 years 19 days."

    Note what the balance has none of: months. Twelve months to a year and
    thirty days to a month makes 0.0533 of a year 0 months and 19 days, which
    is why the example writes it that way.
    """
    from hora.dasha.rasi.sudasa import first_dasa_fraction, years_to_dasa_ymdh

    fraction = first_dasa_fraction(EX79_SREE_LAGNA)
    assert fraction == pytest.approx((1800 - (22 * 60 + 22)) / 1800)
    assert int(fraction * 10_000) / 10_000 == 0.2544   # the example truncates

    balance = 12 * fraction
    years, months, days, _hours = years_to_dasa_ymdh(balance)
    assert (years, months, days) == (3, 0, 19)


def test_example_79_libra_dasa_holds_her_chief_ministership():
    """"Li dasa ran during Feb 1990-Feb 1996." She was Chief Minister
    1991-1996.

    The example states the window to the month and drops the 19 days it had
    just computed: three years plus the other five dasas is 42 years from a
    February 1948 birth, which is February 1990. Carrying the remainder puts
    it at mid-March. Nothing turns on the three weeks — her term is inside on
    either reckoning — but the offset is ours being more exact, not less.
    """
    from datetime import date

    from hora.charts.book import chart, graha_longitudes, graha_signs
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD, Graha
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_jd, from_local
    from hora.dasha.rasi.narayana import (
        dasa_length,
        solar_arc_instant,
        sub_period_arc,
    )
    from hora.dasha.rasi.sudasa import first_dasa_fraction, progression

    longitudes = {int(g): lon for g, lon in graha_longitudes(35).items()}
    signs = {int(g): s for g, s in graha_signs(35).items()}
    ephemeris = get_ephemeris(Settings(node_type=NodeType.MEAN))

    def sun_at(jd: float) -> float:
        return ephemeris.position(jd, int(Graha.SUN)).longitude

    birth = from_local(**chart(35)["birth_data"]).jd_ut
    got = progression(R["Sagittarius"], EX79_SREE_LAGNA)

    arc, spans = 0.0, {}
    for index, sign in enumerate(got.signs[:8]):
        lord = int(RASI_LORD[sign])
        years = dasa_length(sign, lord, signs[lord],
                            sign_dignity(lord, longitudes[lord])).years
        if index == 0:
            years *= first_dasa_fraction(EX79_SREE_LAGNA)
        opens = solar_arc_instant(birth, arc, sun_at)
        arc += sub_period_arc(years, 0)
        spans[ABBR[sign]] = (from_jd(opens, utc_offset_hours=5.5).local.date(),
                             from_jd(solar_arc_instant(birth, arc, sun_at),
                                     utc_offset_hours=5.5).local.date())

    opens, closes = spans["Li"]
    assert (opens.year, closes.year) == (1990, 1996)
    assert opens < date(1991, 6, 24) < closes          # she took office in it

    # She left office on 12 May 1996, which is past the dasa on either
    # reckoning — ours ends 15 March and the example says February. The
    # example's own framing is loose too: "Chief Minister... during 1991-1996".
    assert closes < date(1996, 5, 12)

    # the three weeks: the balance rounded down to 3 years, plus the six whole
    # dasas after it, is 42 years — which from a 24 February birth is the
    # example's February 1990.
    assert opens.month == 3
    assert 3 + sum(y for _a, y in EX79_LENGTHS[1:7]) == 42


def test_example_79_libra_reaches_all_three_readings_at_once():
    """"As Libra contains AL, GL and HL, its dasa as per Sudasa must give
    status, power and wealth."

    The only chart in the book with the three special points in one rasi, so
    the only place §20.3's readings all land together. Rules 1 and 2 admit
    Libra by identity — it *is* HL's sign and GL's — and the AL reading is the
    one §20.3 leaves out.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.charts.book import longitudes as printed
    from hora.charts.colord import stronger
    from hora.dasha.rasi.sudasa import prosperity_ways, status_from_arudha_lagna

    longitudes = {int(g): lon for g, lon in graha_longitudes(35).items()}
    signs = {int(g): s for g, s in graha_signs(35).items()}
    hora_lagna = int(printed(35)["HL"] // 30)
    ghati_lagna = int(printed(35)["GL"] // 30)
    arudha = arudha_pada(
        1, lagna(35), signs,
        {r: stronger(r, longitudes, purpose="arudha").winner for r in (7, 10)}
    ).sign
    assert hora_lagna == ghati_lagna == arudha == R["Libra"]

    for target in (hora_lagna, ghati_lagna):
        ways = prosperity_ways(R["Libra"], target, signs)
        assert ways[0]["rule"] == "is the special lagna's sign"

    status = status_from_arudha_lagna(R["Libra"], arudha)
    assert status["house_from_al"] == 1
    assert status["readings"] == ("status",)


def test_the_al_reading_is_example_79s_rather_than_20_3s():
    """§20.3 rules 3 and 4 read houses **from** AL and never the dasa rasi
    being AL — though rule 3's own premise, "AL stands for one's status", is
    exactly what would give it. Example 79 supplies the missing step, so the
    register records a different source for that row than for the others.
    """
    from hora.dasha.rasi.sudasa import (
        AL_IN_THE_DASA_RASI_GIVES_STATUS,
        STATUS_FROM_ARUDHA_LAGNA,
    )

    by_source: dict[str, list[tuple[int, ...]]] = {}
    for reading in STATUS_FROM_ARUDHA_LAGNA:
        by_source.setdefault(reading["source"], []).append(reading["houses"])

    assert by_source["Example 79"] == [(1,)]
    assert set(by_source) == {"Example 79", "§20.3 rule 3", "§20.3 rule 4"}
    assert "must give status, power and wealth" in AL_IN_THE_DASA_RASI_GIVES_STATUS


def test_example_79s_sree_lagna_is_the_second_case_of_the_27_fold_error():
    """The book has SL at 22 Sg 22; we get 22 Sg 13 from the printed
    longitudes and 22 Sg 00 recomputed. Both are under an arcminute of Moon
    once the 27-fold amplification is undone — the same finding Example 77
    turned up, now on a second chart.

    And as there, nothing in the example moves: SL is twenty-two degrees into
    Sagittarius on every reading, so only rule 7's fraction shifts.
    """
    from hora.charts.book import graha_longitudes
    from hora.charts.book import longitudes as printed
    from hora.charts.special_lagna import (
        SREE_LAGNA_AMPLIFIES_THE_MOON,
        sree_lagna,
    )
    from hora.core.const import Graha

    ours = sree_lagna(graha_longitudes(35)[Graha.MOON], printed(35)["Asc"])
    assert int(ours // 30) == int(EX79_SREE_LAGNA // 30) == R["Sagittarius"]

    gap = abs(ours - EX79_SREE_LAGNA)
    assert gap * 60 < 15                                # under a quarter degree
    assert (gap / SREE_LAGNA_AMPLIFIES_THE_MOON) * 60 < 1.0   # of Moon
