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


# --------------------------------------------------------------------------
# §21.3 Interpretation
# --------------------------------------------------------------------------

def _chart_36_points():
    """Chart 36's lagna and the three arudhas §21.3 reads."""
    from hora.charts.arudha import arudha_pada
    from hora.charts.colord import stronger

    longitudes, signs, lagna_sign = _chart_36()
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}
    return {
        "lagna": lagna_sign,
        "arudha_lagna": arudha_pada(1, lagna_sign, signs, overrides).sign,
        "mantrapada": arudha_pada(5, lagna_sign, signs, overrides).sign,
        "mrityupada": arudha_pada(8, lagna_sign, signs, overrides).sign,
        "signs": signs,
    }


def test_the_eight_readings_and_which_two_are_conditional():
    """§21.3's eight, and the two the section leaves hanging on something it
    does not settle — rule 1 on parivraja yogas, rule 8 on Rahu's
    favourability.
    """
    from hora.dasha.rasi.drigdasa import SPIRITUAL_READINGS

    assert [r["rule"] for r in SPIRITUAL_READINGS] == list(range(1, 9))
    assert {r["reads"] for r in SPIRITUAL_READINGS} == {
        "AL", "lagna", "A5", "A8", "Ketu", "Rahu"}

    conditional = {r["rule"]: r["needs"] for r in SPIRITUAL_READINGS
                   if r["needs"]}
    assert set(conditional) == {1, 8}
    assert "parivraja yogas" in conditional[1]
    assert "favorable" in conditional[8]


def test_rule_1_waits_on_parivraja_yogas_which_nothing_here_detects():
    """"Dasa of arudha lagna can bring renunciation **if** there are parivraja
    yogas in the chart."

    No chapter so far has taught them and nothing in the engine finds them, so
    the reading is reported with its condition unmet rather than asserted or
    dropped. Told the condition holds it fires; told it fails it does not.
    """
    from hora.dasha.rasi.drigdasa import (
        PARIVRAJA_YOGAS_NOT_BUILT,
        spiritual_readings,
    )

    points = _chart_36_points()
    al = points["arudha_lagna"]

    undecided = spiritual_readings(al, **points)
    rule_1 = next(r for r in undecided if r["rule"] == 1)
    assert "parivraja yogas" in rule_1["undecided"]
    assert rule_1["gives"] == "renunciation"

    holds = spiritual_readings(al, **points, parivraja_yogas=True)
    assert "undecided" not in next(r for r in holds if r["rule"] == 1)

    fails = spiritual_readings(al, **points, parivraja_yogas=False)
    assert not [r for r in fails if r["rule"] == 1]

    assert "if there are parivraja yogas" in PARIVRAJA_YOGAS_NOT_BUILT


def test_rule_8_branches_and_reports_both_when_rahu_is_unjudged():
    """"Dasa of the sign containing Rahu can create progress after internal
    turmoil if Rahu is favorable. If Rahu is unfavorable, it can take the
    native in the direction of materialism."

    Opposite results from one placement, and §21.3 never says what settles it.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_36_points()
    rahu_sign = points["signs"][int(Graha.RAHU)]

    unjudged = next(r for r in spiritual_readings(rahu_sign, **points)
                    if r["rule"] == 8)
    assert "undecided" in unjudged
    assert "materialism" in unjudged["gives"] and "progress" in unjudged["gives"]

    good = next(r for r in spiritual_readings(rahu_sign, **points,
                                              rahu_favourable=True)
                if r["rule"] == 8)
    assert good["gives"] == "progress after internal turmoil"
    assert "undecided" not in good

    bad = next(r for r in spiritual_readings(rahu_sign, **points,
                                             rahu_favourable=False)
               if r["rule"] == 8)
    assert "materialism" in bad["gives"]


def test_lagna_reaches_two_readings_and_the_seventh_only_one():
    """Rules 3 and 4 both concern lagna's dasa and give different things —
    "internal awakening and self-realization", and "fame and power related to
    spreading spiritual knowledge". The 7th shares only the first.
    """
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_36_points()
    lagna_sign = points["lagna"]

    at_lagna = {r["rule"] for r in spiritual_readings(lagna_sign, **points)}
    assert {3, 4} <= at_lagna

    seventh = (lagna_sign + 6) % 12
    at_seventh = {r["rule"] for r in spiritual_readings(seventh, **points)}
    assert 3 in at_seventh
    assert 4 not in at_seventh


def test_rule_5_takes_an_aspect_and_rule_6_does_not():
    """"Dasas of signs **containing or aspecting** mantrapada" against "Dasa
    of the sign **containing** mrityupada". The asymmetry is the section's.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_36_points()
    a5, a8 = points["mantrapada"], points["mrityupada"]

    assert 5 in {r["rule"] for r in spiritual_readings(a5, **points)}
    for aspecting in (s for s in range(12) if a5 in rasi_drishti(s)):
        assert 5 in {r["rule"] for r in spiritual_readings(aspecting, **points)}

    assert 6 in {r["rule"] for r in spiritual_readings(a8, **points)}
    for aspecting in (s for s in range(12)
                      if a8 in rasi_drishti(s) and s != a8):
        assert 6 not in {r["rule"]
                         for r in spiritual_readings(aspecting, **points)}


def test_ketus_claim_is_stronger_than_the_rule_it_justifies():
    """"Ketu is the significator of moksha... Ketu is the **only** planet who
    can give real spiritual awakening and liberation."

    Rule 7 needs only the first half. The second is the sharpest claim in the
    chapter and is kept whole, because a reading layer that paraphrases it
    into "Ketu favours liberation" says something much weaker.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import (
        KETU_IS_THE_ONLY_LIBERATOR,
        spiritual_readings,
    )

    points = _chart_36_points()
    ketu_sign = points["signs"][int(Graha.KETU)]
    assert 7 in {r["rule"] for r in spiritual_readings(ketu_sign, **points)}

    assert "only planet" in KETU_IS_THE_ONLY_LIBERATOR
    assert "real spiritual awakening and liberation" in KETU_IS_THE_ONLY_LIBERATOR


def test_a5_is_the_mantrapada_here_and_showed_power_in_chapter_20():
    """§21.3 names A5 "mantrapada"; Example 78 read the same pada as showing
    one's following and the trappings of power.

    Not a conflict. Exercise 30 stated the principle — an arudha shows the
    appearance of its house's matter, narrowed by what is being asked, "in
    career, because this is D-10". Asked about mantras the 5th's arudha is the
    mantrapada; asked about power it is a following.
    """
    from hora.dasha.rasi.drigdasa import A5_IS_ALSO_THE_MANTRAPADA
    from hora.dasha.rasi.narayana import ARUDHA_SHOWS_THE_APPEARANCE_OF_ITS_MATTER
    from hora.dasha.rasi.sudasa import A5_SHOWS_ONES_FOLLOWING

    assert "mantrapada" in A5_IS_ALSO_THE_MANTRAPADA
    assert "arudha pada of the 5th house" in A5_IS_ALSO_THE_MANTRAPADA
    assert "following" in A5_SHOWS_ONES_FOLLOWING
    assert "because this is D-10" in ARUDHA_SHOWS_THE_APPEARANCE_OF_ITS_MATTER


def test_a8_keeps_its_chapter_18_name_too():
    """Example 75 wrote "mrityu pada", §21.3 writes "mrityupada". Same pada,
    same house, and both spellings are the book's — so both are stored rather
    than one being regularised, as D-24 and D-25 do for other variants.
    """
    from hora.dasha.rasi.drigdasa import SPIRITUAL_READINGS
    from hora.dasha.rasi.narayana import ARUDHA_PADA_DASA_READINGS

    from_18 = next(r for r in ARUDHA_PADA_DASA_READINGS if r["pada"] == "A8")
    assert from_18["also"] == "mrityu pada"
    assert from_18["house"] == 8

    from_21 = next(r for r in SPIRITUAL_READINGS if r["reads"] == "A8")
    assert "mrityupada" in from_21["text"]
    assert "arudha pada of 8th house" in from_21["text"]


def test_21_3_applied_across_chart_36s_drigdasa():
    """The section on the chapter's own chart. Libra reaches three readings at
    once — it is lagna, so rules 3 and 4, and it holds the mantrapada — while
    two of the twelve rasis reach none at all, which the section allows for by
    naming only six references.
    """
    from hora.dasha.rasi.drigdasa import progression, spiritual_readings

    points = _chart_36_points()
    assert points["arudha_lagna"] == R["Gemini"]
    assert points["mantrapada"] == R["Libra"]
    assert points["mrityupada"] == R["Leo"]

    reached = {}
    for sign in progression(points["lagna"]).signs:
        rules = {r["rule"] for r in spiritual_readings(sign, **points)}
        if rules:
            reached[ABBR[sign]] = rules

    assert reached["Li"] == {3, 4, 5}
    assert reached["Ar"] == {3}                    # the 7th, rule 3 only
    assert reached["Ge"] == {1}                    # the arudha lagna
    assert reached["Le"] == {5, 6}
    assert set(reached) == set(EX80_ORDER) - {"Cn", "Cp"}
