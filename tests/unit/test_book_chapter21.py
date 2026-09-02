"""Chapter 21 — Drigdasa, the aspect dasa.

The sixth of Part 2's nine, and the first rasi dasa whose groups come from
aspects rather than houses. What is tested here is the part that is its own:
three groups of four, three separate directions, a footedness test that
chapters 19 and 20 explicitly were not using, and groups that do not always
cover the zodiac.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_NAMES

R = {name: i for i, name in enumerate(RASI_NAMES)}
ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

#: The four lagnas whose groups overlap — see OI-127.
DUAL_LAGNAS = ("Gemini", "Virgo", "Sagittarius", "Pisces")


def test_the_name_is_the_rule():
    """"Drik means vision and drigdasa is a dasa based on aspects."

    Part 2's map calls it "phalita - spirituality"; §21.1 is the sentence
    behind that.
    """
    from hora.core.constants.dasha import PART_2_DASA_SYSTEMS
    from hora.dasha.rasi.drigdasa import DRIK_MEANS_VISION, SHOWS_SPIRITUAL_VISION

    assert "based on aspects" in DRIK_MEANS_VISION
    assert "spiritual vision" in SHOWS_SPIRITUAL_VISION
    assert "evolution of one's soul" in SHOWS_SPIRITUAL_VISION

    entry = next(s for s in PART_2_DASA_SYSTEMS if s["name"] == "Drigdasa")
    assert entry["kind"] == "rasi"
    assert "spirituality" in entry["purpose"]


def test_dasas_start_from_the_ninth_and_the_groups_are_9_10_11():
    """"Dasas start from the 9th house... First 4 dasas belong to the 9th
    house and the 3 signs aspected by it... Next 4... the 10th house...
    Last 4... the 11th house."
    """
    from hora.dasha.rasi.drigdasa import GROUP_HOUSES, progression

    assert GROUP_HOUSES == (9, 10, 11)
    for lagna in range(12):
        got = progression(lagna)
        assert [g.house for g in got.groups] == [9, 10, 11]
        for group in got.groups:
            assert group.leader == (lagna + group.house - 1) % 12
            assert group.signs[0] == group.leader
            assert len(group.signs) == 4
        assert got.signs[0] == (lagna + 8) % 12       # the 9th takes the first


def test_each_group_is_a_leader_and_the_three_signs_it_aspects():
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.drigdasa import progression

    for lagna in range(12):
        for group in progression(lagna).groups:
            assert set(group.signs[1:]) == set(rasi_drishti(group.leader))
            assert len(rasi_drishti(group.leader)) == 3


def test_the_direction_is_footedness_not_the_odd_even_sign_test():
    """"Order of reckoning is forward or backward based on whether the 9th
    house is **odd-footed** or even-footed."

    Chapters 19 and 20 both used odd/even **signs** and each printed a NOTE
    saying it was not the footed test. Chapter 21 goes back to the footed one
    without a note, and the two disagree on a third of the zodiac — so
    carrying either earlier chapter's rule here is wrong for Taurus, Leo,
    Scorpio and Aquarius.
    """
    from hora.core.const import RASI_IS_ODD, RASI_IS_ODD_FOOTED
    from hora.dasha.rasi import kendradi, sudasa
    from hora.dasha.rasi.drigdasa import (
        FOOTEDNESS_DECIDES_THE_DIRECTION,
        direction_of,
    )

    assert "odd-footed" in FOOTEDNESS_DECIDES_THE_DIRECTION
    disagree = {RASI_NAMES[i] for i in range(12)
                if bool(RASI_IS_ODD[i]) != bool(RASI_IS_ODD_FOOTED[i])}
    assert disagree == {"Taurus", "Leo", "Scorpio", "Aquarius"}

    for rasi in range(12):
        expected = "forward" if RASI_IS_ODD_FOOTED[rasi] else "backward"
        assert direction_of(rasi) == expected
        by_sign = kendradi.direction_of(rasi)
        assert sudasa.direction_of(rasi) == by_sign
        if RASI_NAMES[rasi] in disagree:
            assert direction_of(rasi) != by_sign      # they really do differ


def test_one_run_carries_three_directions():
    """Every earlier rasi dasa had a single direction for all twelve periods.
    Here each group takes its own, from its own leader — and on most charts
    they are not all the same.
    """
    from hora.dasha.rasi.drigdasa import progression

    mixed = 0
    for lagna in range(12):
        directions = {g.direction for g in progression(lagna).groups}
        if len(directions) > 1:
            mixed += 1
    assert mixed >= 8                                  # most lagnas


def test_a_group_runs_from_its_leader_in_its_own_direction():
    """§21.2 says only "forward or backward", so the reading is: the leader
    takes the first dasa — the section says dasas start from the 9th — and the
    three it aspects follow in zodiacal order from it, or anti-zodiacal.

    Aries lagna, where all three groups partition, shows all three shapes: a
    dual leader with three duals, a movable with three fixed, a fixed with
    three movable.
    """
    from hora.dasha.rasi.drigdasa import group_signs, progression

    got = progression(R["Aries"])
    assert [g.leader_name for g in got.groups] == ["Sagittarius", "Capricorn",
                                                   "Aquarius"]
    assert [g.direction for g in got.groups] == ["forward", "backward",
                                                 "backward"]
    assert [ABBR[s] for s in got.groups[0].signs] == ["Sg", "Pi", "Ge", "Vi"]
    assert [ABBR[s] for s in got.groups[1].signs] == ["Cp", "Sc", "Le", "Ta"]
    assert [ABBR[s] for s in got.groups[2].signs] == ["Aq", "Li", "Cn", "Ar"]

    # forward and backward are each other's reverse, after the leader
    forward = group_signs(R["Sagittarius"], "forward")
    backward = group_signs(R["Sagittarius"], "backward")
    assert forward[0] == backward[0] == R["Sagittarius"]
    assert forward[1:] == tuple(reversed(backward[1:]))


def test_the_groups_partition_the_zodiac_for_eight_lagnas():
    """See OI-127. The three leaders are consecutive houses, so one of each
    modality — and rasi drishti excludes the adjacent sign. When the 9th is
    movable or dual the movable and fixed leaders are adjacent and keep each
    other out; when it is fixed they are two apart and both land twice.
    """
    from hora.core.const import MODALITY_NAMES, RASI_MODALITY
    from hora.dasha.rasi.drigdasa import progression

    covering, overlapping = [], []
    for lagna in range(12):
        got = progression(lagna)
        (covering if got.covers_every_rasi else overlapping).append(
            RASI_NAMES[lagna])
        if got.covers_every_rasi:
            assert set(got.signs) == set(range(12))
            assert got.repeated == got.omitted == ()
        else:
            assert len(got.repeated) == len(got.omitted) == 2

    assert len(covering) == 8
    assert overlapping == list(DUAL_LAGNAS)

    # and it is exactly the lagnas whose 9th house is fixed
    for name in DUAL_LAGNAS:
        ninth = (R[name] + 8) % 12
        assert str(MODALITY_NAMES[RASI_MODALITY[ninth]]) == "sthira"


def test_the_overlap_is_reported_rather_than_removed():
    """Deduplicating would invent an order §21.2 does not give, and dropping a
    repeat would leave eleven dasas where the section asks for twelve. So the
    twelve stand and the result says which rasis take two and which none.
    """
    from hora.dasha.rasi.drigdasa import progression

    got = progression(R["Gemini"])
    assert len(got.signs) == 12                       # still twelve dasas
    assert len(set(got.signs)) == 10                  # of ten rasis
    assert {RASI_NAMES[s] for s in got.repeated} == {"Aries", "Aquarius"}
    assert {RASI_NAMES[s] for s in got.omitted} == {"Taurus", "Capricorn"}
    assert "OI-127" in got.why


@pytest.mark.parametrize("name,twice,never", [
    ("Gemini", {"Aquarius", "Aries"}, {"Taurus", "Capricorn"}),
    ("Virgo", {"Cancer", "Taurus"}, {"Aries", "Leo"}),
    ("Sagittarius", {"Leo", "Libra"}, {"Cancer", "Scorpio"}),
    ("Pisces", {"Capricorn", "Scorpio"}, {"Aquarius", "Libra"}),
])
def test_which_rasis_double_and_which_vanish(name, twice, never):
    """OI-127's table, held so the four cases cannot drift."""
    from hora.dasha.rasi.drigdasa import progression

    got = progression(R[name])
    assert {RASI_NAMES[s] for s in got.repeated} == twice
    assert {RASI_NAMES[s] for s in got.omitted} == never


def test_the_lengths_are_still_18_2_2s():
    """"Dasa periods of various rasis in this dasa system are found just like
    in Narayana dasa." The third chapter running to say so, so `dasa_length`
    serves all three and chapter 21 restates none of it.
    """
    import inspect

    from hora.charts.book import graha_longitudes, graha_signs
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi import drigdasa
    from hora.dasha.rasi.narayana import dasa_length

    assert "just like in Narayana dasa" in drigdasa.LENGTHS_ARE_NARAYANAS
    source = inspect.getsource(drigdasa)
    assert "def dasa_length" not in source

    longitudes = {int(g): lon for g, lon in graha_longitudes(24).items()}
    signs = {int(g): s for g, s in graha_signs(24).items()}
    mercury = int(RASI_LORD[R["Gemini"]])
    assert dasa_length(R["Gemini"], mercury, signs[mercury],
                       sign_dignity(mercury, longitudes[mercury])).years == 3


def test_group_signs_refuses_a_direction_it_does_not_know():
    from hora.dasha.rasi.drigdasa import DrigdasaError, group_signs

    with pytest.raises(DrigdasaError, match="forward"):
        group_signs(R["Aries"], "sunwise")


# --------------------------------------------------------------------------
# Example 80 — Chart 36, and the walk §21.2 leaves to be read.
# --------------------------------------------------------------------------

EX80_ORDER = ["Ge", "Vi", "Sg", "Pi", "Cn", "Ta", "Aq", "Sc",
              "Le", "Ar", "Cp", "Li"]
EX80_LENGTHS = {"Ge": 4, "Vi": 11, "Sg": 2, "Pi": 1, "Cn": 6, "Ta": 3,
                "Aq": 8, "Sc": 10, "Le": 11, "Ar": 5, "Cp": 7, "Li": 10}


def _chart_36():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(36).items()},
            {int(g): sign for g, sign in graha_signs(36).items()},
            lagna(36))


def test_chart_36_is_printed_without_a_birth_line():
    """The only chart in the book given with no birth data at all — not even a
    date. Nothing here needs it: Drigdasa reads the rasi chart alone, and its
    lengths come from §18.2.2 which reads longitudes.
    """
    from hora.charts.book import chart, is_recomputable

    assert not is_recomputable(36)
    assert chart(36)["birth"] == "not given"
    assert "birth_data" not in chart(36)


def test_example_80_spells_out_the_walk_inside_a_group():
    """"Because Ge is an odd-footed sign, we should go forward as Ge, Cn, Le,
    Vi, Li etc and find the signs that aspect Ge. We get Ge, Vi, Sg and Pi."

    §21.2 said only "forward or backward". This is the walk it meant: step
    round the zodiac from the leader and take the signs that aspect it in the
    order met. Reproduced here as the example describes it rather than by
    calling the function, so the two agree independently.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.drigdasa import group_signs

    walked = [R["Gemini"]]
    for step in range(1, 12):
        sign = (R["Gemini"] + step) % 12
        if R["Gemini"] in rasi_drishti(sign):
            walked.append(sign)

    assert [ABBR[s] for s in walked] == ["Ge", "Vi", "Sg", "Pi"]
    assert group_signs(R["Gemini"], "forward") == tuple(walked)


def test_example_80s_three_groups_and_their_three_directions():
    """"Because Cn is an even-footed sign, we should go backward as Cn, Ge,
    Ta, Ar, Pi etc... We get Cn, Ta, Aq and Sc." And Leo likewise gives Le,
    Ar, Cp and Li.

    One Libra lagna, three groups, and not one direction between them — the
    9th forward and the other two backward.
    """
    from hora.dasha.rasi.drigdasa import progression

    _longitudes, _signs, lagna_sign = _chart_36()
    assert lagna_sign == R["Libra"]

    got = progression(lagna_sign)
    assert [g.leader_name for g in got.groups] == ["Gemini", "Cancer", "Leo"]
    assert [g.direction for g in got.groups] == ["forward", "backward",
                                                 "backward"]
    assert [ABBR[s] for s in got.groups[0].signs] == ["Ge", "Vi", "Sg", "Pi"]
    assert [ABBR[s] for s in got.groups[1].signs] == ["Cn", "Ta", "Aq", "Sc"]
    assert [ABBR[s] for s in got.groups[2].signs] == ["Le", "Ar", "Cp", "Li"]


def test_example_80_full_order():
    """"So dasas go as Ge, Vi, Sg, Pi, Cn, Ta, Aq, Sc, Le, Ar, Cp and Li."

    Twelve distinct rasis — Libra's 9th is Gemini, which is dual, so OI-127's
    overlap does not arise here.
    """
    from hora.core.const import MODALITY_NAMES, RASI_MODALITY
    from hora.dasha.rasi.drigdasa import progression

    got = progression(R["Libra"])
    assert [ABBR[s] for s in got.signs] == EX80_ORDER
    assert got.covers_every_rasi
    assert str(MODALITY_NAMES[RASI_MODALITY[R["Gemini"]]]) == "dwiswabhava"


@pytest.mark.parametrize("abbr", EX80_ORDER)
def test_example_80_lengths(abbr):
    """All twelve of the dasa table, from §18.2.2 by way of rule 5."""
    from hora.charts.colord import CO_LORDS, stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_36()
    rasi = {v: k for k, v in enumerate(ABBR)}[abbr]
    if rasi in CO_LORDS:
        years = {g: dasa_length(rasi, g, signs[g],
                                sign_dignity(g, longitudes[g])).years
                 for g in CO_LORDS[rasi]}
        lord = stronger(rasi, longitudes, purpose="dasa",
                        dasa_years=years).winner
    else:
        lord = int(RASI_LORD[rasi])
    got = dasa_length(rasi, lord, signs[lord],
                      sign_dignity(lord, longitudes[lord]))
    assert got.years == EX80_LENGTHS[abbr], got.why


def test_example_80s_two_co_owned_rasis_are_both_load_bearing():
    """Aquarius and Scorpio both go to §15.5.1, and the printed lengths force
    the choice each way — at two different rules.

    | rasi | co-lords | printed | the other gives | settled at |
    |---|---|---|---|---|
    | Aquarius | Saturn in Ge, Rahu in Sc | 8 | 3 | rule 4, dual beats fixed |
    | Scorpio | Mars in Vi, Ketu in Ta | 10 | 6 | rule 1, Mars is joined |
    """
    from hora.charts.colord import stronger
    from hora.core.const import Graha
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_36()
    saturn, rahu = int(Graha.SATURN), int(Graha.RAHU)
    mars, ketu = int(Graha.MARS), int(Graha.KETU)

    assert dasa_length(R["Aquarius"], saturn, signs[saturn]).years == 8
    assert dasa_length(R["Aquarius"], rahu, signs[rahu]).years == 3
    aquarius = stronger(R["Aquarius"], longitudes, purpose="dasa",
                        dasa_years={saturn: 8, rahu: 3})
    assert aquarius.winner == saturn
    assert aquarius.decided_by == "4"

    assert dasa_length(R["Scorpio"], mars, signs[mars]).years == 10
    assert dasa_length(R["Scorpio"], ketu, signs[ketu]).years == 6
    scorpio = stronger(R["Scorpio"], longitudes, purpose="dasa",
                       dasa_years={mars: 10, ketu: 6})
    assert scorpio.winner == mars
    assert scorpio.decided_by == "1"


def test_example_80_confirms_the_footedness_test_on_a_real_chart():
    """Gemini forward, Cancer and Leo backward — and Leo is one of the four
    signs where the footed test and the odd/even sign test disagree. Read
    chapter 19's or 20's rule here and Leo's group would run forward.
    """
    from hora.dasha.rasi import kendradi
    from hora.dasha.rasi.drigdasa import direction_of

    assert direction_of(R["Gemini"]) == "forward"
    assert direction_of(R["Cancer"]) == "backward"
    assert direction_of(R["Leo"]) == "backward"
    assert kendradi.direction_of(R["Leo"]) == "forward"    # the wrong rule
