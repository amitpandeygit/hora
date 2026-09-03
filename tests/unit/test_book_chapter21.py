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

    section = [r for r in SPIRITUAL_READINGS
               if r["source"].startswith("\u00a721.3")]
    assert [r["rule"] for r in section] == list(range(1, 9))
    assert {r["reads"] for r in section} == {
        "AL", "lagna", "A5", "A8", "Ketu", "Rahu"}

    conditional = {r["rule"]: r["needs"] for r in section if r["needs"]}
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
    on §21.3's eight alone two of the twelve rasis reach none, which the
    section allows for by naming only six references.
    """
    from hora.dasha.rasi.drigdasa import progression, spiritual_readings

    points = _chart_36_points()
    assert points["arudha_lagna"] == R["Gemini"]
    assert points["mantrapada"] == R["Libra"]
    assert points["mrityupada"] == R["Leo"]

    reached = {}
    for sign in progression(points["lagna"]).signs:
        rules = {r["rule"] for r in spiritual_readings(sign, **points)
                 if r["source"].startswith("\u00a721.3")}
        if rules:
            reached[ABBR[sign]] = rules

    assert reached["Li"] == {3, 4, 5}
    assert reached["Ar"] == {3}                    # the 7th, rule 3 only
    assert reached["Ge"] == {1}                    # the arudha lagna
    assert reached["Le"] == {5, 6}
    assert set(reached) == set(EX80_ORDER) - {"Cn", "Cp"}


def test_the_examples_rules_leave_no_rasi_of_chart_36_unread():
    """The same chart with rules 9, 10 and 11 added: Cancer and Capricorn, the
    two the section leaves blank, both take Ketu's argala, and every one of the
    twelve reaches something. A reason to keep them, and a reason OI-129 is
    open rather than decorative.
    """
    from hora.dasha.rasi.drigdasa import progression, spiritual_readings

    points = _chart_36_points()
    reached = {ABBR[sign]: {r["rule"]
                            for r in spiritual_readings(sign, **points)}
               for sign in progression(points["lagna"]).signs}

    assert all(reached.values())
    assert reached["Cn"] == {11}
    assert reached["Cp"] == {11}
    assert reached["Sg"] == {2, 10}


# --------------------------------------------------------------------------
# Example 81 — the same chart's Taurus dasa, and a reading §21.3 never printed.
# --------------------------------------------------------------------------

def test_example_81_taurus_runs_24_to_27_from_example_80s_own_table():
    """"Let us analyze Ta dasa that comes during 24-27 years of age."

    The example gives no dates, only the ages, and they are a check on
    everything Example 80 built: run the twelve lengths along the twelve-dasa
    order and Taurus must open at 24 and close at 27. That is §21.2's walk,
    its three directions and all twelve §18.2.2 lengths confirmed at once by a
    number the chapter states independently.
    """
    from hora.dasha.rasi.drigdasa import progression

    elapsed = 0
    spans = {}
    for sign in progression(R["Libra"]).signs:
        length = EX80_LENGTHS[ABBR[sign]]
        spans[ABBR[sign]] = (elapsed, elapsed + length)
        elapsed += length

    assert spans["Ta"] == (24, 27)
    assert elapsed == 78


def test_example_81s_three_reasons_all_fire():
    """"Ta has mokshakaraka Ketu in it. Lagna and mantrapada are in Li and Ta
    aspects both."

    Three reasons for one dasa, and they land on three different rules —
    Ketu's placement, an aspect on the mantrapada, and an aspect on lagna.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import MOKSHAKARAKA_KETU, spiritual_readings

    points = _chart_36_points()
    assert points["signs"][int(Graha.KETU)] == R["Taurus"]
    assert points["lagna"] == points["mantrapada"] == R["Libra"]

    got = {r["rule"]: r for r in spiritual_readings(R["Taurus"], **points)}
    assert set(got) == {5, 7, 9}
    assert got[7]["why"] == "Ketu is in Taurus"
    assert got[5]["why"] == "Taurus aspects the mantrapada Libra"
    assert got[9]["why"] == "Taurus aspects lagna Libra"
    assert "mokshakaraka" in MOKSHAKARAKA_KETU


def test_example_81_reads_a_sign_that_only_aspects_lagna():
    """§21.3 rule 3 is "Dasa of lagna **and the 7th house**". Taurus is
    neither — it is the 8th from Libra, and it does not aspect Aries either.
    The example takes rule 3's result from an aspect on lagna alone, which the
    printed rule does not reach. See OI-128.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.drigdasa import (
        EXAMPLE_81_READS_A_SIGN_ASPECTING_LAGNA,
        SPIRITUAL_READINGS,
    )

    assert R["Taurus"] not in (R["Libra"], R["Aries"])
    assert R["Aries"] not in rasi_drishti(R["Taurus"])
    assert R["Libra"] in rasi_drishti(R["Taurus"])

    rule_3 = next(r for r in SPIRITUAL_READINGS if r["rule"] == 3)
    assert rule_3["test"] == "the dasa sign is lagna or the 7th from it"
    assert "internal progress" in EXAMPLE_81_READS_A_SIGN_ASPECTING_LAGNA


def test_the_ninth_reading_is_sourced_to_the_example_not_the_section():
    """Eight rules are §21.3's; the ninth is Example 81's. Kept apart and
    labelled rather than folded into rule 3, the way chapter 20's
    STATUS_FROM_ARUDHA_LAGNA rows carry their source.
    """
    from hora.dasha.rasi.drigdasa import SPIRITUAL_READINGS, spiritual_readings
    from hora.dasha.rasi.sudasa import STATUS_FROM_ARUDHA_LAGNA

    sources = {r["rule"]: r["source"] for r in SPIRITUAL_READINGS}
    assert all(sources[n] == f"\u00a721.3 rule {n}" for n in range(1, 9))
    assert sources[9] == "Example 81"

    points = _chart_36_points()
    got = spiritual_readings(R["Taurus"], **points)
    assert {r["source"] for r in got} == {
        "\u00a721.3 rule 5", "\u00a721.3 rule 7", "Example 81"}

    assert all("source" in row for row in STATUS_FROM_ARUDHA_LAGNA)


def test_the_aspect_extension_is_the_chapters_habit_but_not_in_every_rule():
    """Rule 2 extends to signs aspecting AL and rule 5 to signs "containing or
    aspecting" the mantrapada, so reading an aspect is the chapter's own way.
    Rules 3, 4 and 6 are printed without it, and Example 81 supplies it for
    lagna only — leaving 4 and 6 open. See OI-128.
    """
    from hora.dasha.rasi.drigdasa import SPIRITUAL_READINGS

    by_rule = {r["rule"]: r["test"] for r in SPIRITUAL_READINGS}
    assert "aspects" in by_rule[2]
    assert "aspects" in by_rule[5]
    assert "aspects" in by_rule[9]
    for rule in (3, 4, 6):
        assert "aspect" not in by_rule[rule]


def test_lagna_itself_does_not_pick_up_the_ninth_reading():
    """A sign never aspects itself under rasi drishti, so Libra reaches rules
    3 and 4 and not 9. The ninth adds signs the printed rules miss; it does
    not double-count the ones they catch.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_36_points()
    assert R["Libra"] not in rasi_drishti(R["Libra"])
    rules = {r["rule"] for r in spiritual_readings(R["Libra"], **points)}
    assert rules == {3, 4, 5}


def test_example_81s_two_stated_outcomes_come_from_the_rules_that_fire():
    """"Ta dasa can bring internal progress and spiritual evolution. It can
    make the native learn and use mantras."

    Two sentences, three rules: the first is rule 9's wording joined to rule
    7's liberation, the second is rule 5's mantra.
    """
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_36_points()
    gives = {r["rule"]: r["gives"]
             for r in spiritual_readings(R["Taurus"], **points)}

    assert gives[9] == "internal progress and spiritual evolution"
    assert "liberation" in gives[7]
    assert "mantra" in gives[5]


# --------------------------------------------------------------------------
# Example 82 — Chart 37, three forward groups, and rule 3's other half.
# --------------------------------------------------------------------------

EX82_ORDER = ["Li", "Aq", "Ta", "Le", "Sc", "Cp", "Ar", "Cn",
              "Sg", "Pi", "Ge", "Vi"]

#: Only four are printed — the example stops once it reaches Leo.
EX82_LENGTHS = {"Li": 1, "Aq": 9, "Ta": 6, "Le": 7}


def _chart_37():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(37).items()},
            {int(g): sign for g, sign in graha_signs(37).items()},
            lagna(37))


def _chart_37_points():
    from hora.charts.arudha import arudha_pada
    from hora.charts.colord import stronger

    longitudes, signs, lagna_sign = _chart_37()
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}
    return {
        "lagna": lagna_sign,
        "arudha_lagna": arudha_pada(1, lagna_sign, signs, overrides).sign,
        "mantrapada": arudha_pada(5, lagna_sign, signs, overrides).sign,
        "mrityupada": arudha_pada(8, lagna_sign, signs, overrides).sign,
        "signs": signs,
    }


def test_chart_37_recomputes_from_its_own_birth_data():
    """Unlike Chart 36 this one prints a full birth line, so the whole example
    stands on Swiss Ephemeris rather than on a transcription. Every graha and
    the ascendant land inside one arcminute.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(37)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 37", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(37)

    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 1.0


def test_chart_37_is_a_tenth_vote_for_the_mean_node():
    """OI-68 again, and the second-widest margin in the register — Rahu is
    57' out under `true`, against Chart 24's 79'. Ten charts now, none of them
    favouring our default.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(37)
    printed = longitudes(37)["Rahu"]
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name="Chart 37", **record["place"]),
            Settings(node_type=node))
        errors[node] = abs(
            computed.positions[int(Graha.RAHU)].longitude - printed) * 60

    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 50.0


def test_chart_37s_arudha_lagna_reproduces_the_drawn_diagram():
    """AL is the one thing in the diagram with no longitude behind it, so the
    chart-wide diagram test skips it. Chart 37 draws it in Gemini and
    `arudha_pada` puts it there.
    """
    from hora.charts.book import chart

    assert chart(37)["drawn"]["AL"] == "Ge"
    assert _chart_37_points()["arudha_lagna"] == R["Gemini"]


def test_example_82s_three_groups_all_run_forward():
    """"The 9th house is in Li. It is an odd-footed sign... The 10th house is
    in Sc. It is an odd-footed sign... The 11th house is in Sg. It is an
    odd-footed sign."

    The opposite extreme from Chart 36, which ran one group forward and two
    backward. Three forward is possible because the 9th, 10th and 11th from
    Aquarius are Libra, Scorpio and Sagittarius — three consecutive
    odd-footed signs.
    """
    from hora.core.const import RASI_IS_ODD_FOOTED
    from hora.dasha.rasi.drigdasa import progression

    _longitudes, _signs, lagna_sign = _chart_37()
    assert lagna_sign == R["Aquarius"]

    got = progression(lagna_sign)
    assert [g.leader_name for g in got.groups] == [
        "Libra", "Scorpio", "Sagittarius"]
    assert all(RASI_IS_ODD_FOOTED[g.leader] for g in got.groups)
    assert [g.direction for g in got.groups] == ["forward"] * 3

    assert [g.direction for g in progression(R["Libra"]).groups] == [
        "forward", "backward", "backward"]


def test_chart_37_separates_the_two_sign_classifications():
    """Scorpio is odd-**footed** but an even **sign**. Chapter 19's rule would
    send the 10th group backward here and chapter 21's sends it forward, so
    this chart alone shows the two classifications are not interchangeable —
    which is why §19.2 and §20.2 both printed a NOTE against confusing them.
    """
    from hora.dasha.rasi import kendradi
    from hora.dasha.rasi.drigdasa import direction_of, group_signs

    assert direction_of(R["Scorpio"]) == "forward"
    assert kendradi.direction_of(R["Scorpio"]) == "backward"

    forward = group_signs(R["Scorpio"], "forward")
    backward = group_signs(R["Scorpio"], "backward")
    assert [ABBR[s] for s in forward] == ["Sc", "Cp", "Ar", "Cn"]
    assert [ABBR[s] for s in backward] == ["Sc", "Cn", "Ar", "Cp"]


def test_example_82_full_order():
    """"So dasas go as Li, Aq, Ta, Le, Sc, Cp, Ar, Cn, Sg, Pi, Ge, Vi."

    Aquarius is fixed, so its 9th is movable Libra and the three groups
    partition the zodiac — OI-127's overlap needs a *dual* lagna.
    """
    from hora.core.const import MODALITY_NAMES, RASI_MODALITY
    from hora.dasha.rasi.drigdasa import progression

    got = progression(R["Aquarius"])
    assert [ABBR[s] for s in got.signs] == EX82_ORDER
    assert got.covers_every_rasi
    assert not got.repeated and not got.omitted
    assert str(MODALITY_NAMES[RASI_MODALITY[R["Libra"]]]) == "chara"


@pytest.mark.parametrize("abbr", sorted(EX82_LENGTHS))
def test_example_82_lengths(abbr):
    """"Lengths of dasas are found as in Narayana dasa." Four are printed;
    the example stops at Leo because that is the dasa it reads.
    """
    from hora.charts.colord import CO_LORDS, stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, _lagna = _chart_37()
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
    assert got.years == EX82_LENGTHS[abbr], got.why


def test_example_82_leo_runs_jan_1987_to_jan_1994():
    """"Leo dasa runs during Jan 1987-Jan 1994."

    Born January 1971. Li 1 + Aq 9 + Ta 6 = 16 whole years to January 1987,
    and Leo's 7 carry it to January 1994 — the four printed lengths and the
    order confirmed together by dates the example states separately.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.drigdasa import progression

    assert chart(37)["birth_data"]["year"] == 1971
    assert chart(37)["birth_data"]["month"] == 1

    elapsed = 0
    for sign in progression(R["Aquarius"]).signs:
        if ABBR[sign] == "Le":
            break
        elapsed += EX82_LENGTHS[ABBR[sign]]

    assert elapsed == 16
    assert 1971 + elapsed == 1987
    assert 1987 + EX82_LENGTHS["Le"] == 1994


def test_the_1990_move_to_a_monastery_falls_inside_leo_dasa():
    """"He was introduced to ISKCON and moved to a monastery in 1990."

    The event the example is written around, and it lands inside the dasa the
    example reads rather than beside it.
    """
    from hora.charts.book import chart

    events = chart(37)["events"]
    assert list(events.values()) == ["1990"]
    assert "monastery" in next(iter(events))

    year = int(next(iter(events.values())))
    start = chart(37)["birth_data"]["year"] + 16
    assert start <= year < start + EX82_LENGTHS["Le"]


def test_example_82_reads_rule_3s_other_half_and_rule_7():
    """"Leo is the 7th from lagna and it contains Ketu. It can give spiritual
    awakening."

    Two reasons, and between them they finish rule 3: Example 81 reached its
    result through the aspect extension, Chart 36's Libra through being lagna
    itself, and this is the printed "and the 7th house" branch. Ketu is rule
    7, whose sentence is the chapter's sharpest.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import (
        KETU_IS_THE_ONLY_LIBERATOR,
        spiritual_readings,
    )

    points = _chart_37_points()
    assert points["signs"][int(Graha.KETU)] == R["Leo"]
    assert (points["lagna"] + 6) % 12 == R["Leo"]

    got = {r["rule"]: r for r in spiritual_readings(R["Leo"], **points)}
    assert set(got) == {3, 7}
    assert got[3]["why"] == "Leo is the 7th from lagna"
    assert got[7]["why"] == "Ketu is in Leo"
    assert "awakening" in got[3]["gives"]
    assert "only planet" in KETU_IS_THE_ONLY_LIBERATOR


def test_chart_37s_lagna_dasa_is_the_one_rahu_leaves_unjudged():
    """Rahu sits in Aquarius, which is also lagna, so its dasa reaches rules 3
    and 4 outright and rule 8 only conditionally. §21.3 does not say what makes
    Rahu favorable, so both branches are reported — and this is the dasa that
    ran 1972-1980, which the example does not read.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_37_points()
    assert points["signs"][int(Graha.RAHU)] == R["Aquarius"]

    got = {r["rule"]: r for r in spiritual_readings(R["Aquarius"], **points)}
    assert set(got) == {3, 4, 8}
    assert "favorable" in got[8]["undecided"]

    judged = spiritual_readings(R["Aquarius"], **points, rahu_favourable=False)
    rule_8 = next(r for r in judged if r["rule"] == 8)
    assert rule_8["gives"] == "a turn in the direction of materialism"


# --------------------------------------------------------------------------
# Example 83 — Sri Aurobindo, and two references §21.3 never lists.
# --------------------------------------------------------------------------

EX83_ORDER = ["Pi", "Sg", "Vi", "Ge", "Ar", "Le", "Sc", "Aq",
              "Ta", "Cn", "Li", "Cp"]

#: The three the example dates, and the years it gives for them.
EX83_DATED = {"Sc": (1906, 1913), "Cn": (1918, 1925), "Li": (1925, 1935)}


def _chart_38():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(38).items()},
            {int(g): sign for g, sign in graha_signs(38).items()},
            lagna(38))


def _chart_38_points():
    from hora.charts.arudha import arudha_pada
    from hora.charts.colord import stronger

    longitudes, signs, lagna_sign = _chart_38()
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}
    return {
        "lagna": lagna_sign,
        "arudha_lagna": arudha_pada(1, lagna_sign, signs, overrides).sign,
        "mantrapada": arudha_pada(5, lagna_sign, signs, overrides).sign,
        "mrityupada": arudha_pada(8, lagna_sign, signs, overrides).sign,
        "signs": signs,
    }


def _chart_38_years():
    """Every Drigdasa of Chart 38 as (start year, end year)."""
    from hora.charts.colord import CO_LORDS, stronger
    from hora.charts.dignity import sign_dignity
    from hora.core.const import RASI_LORD
    from hora.dasha.rasi.drigdasa import progression
    from hora.dasha.rasi.narayana import dasa_length

    longitudes, signs, lagna_sign = _chart_38()
    elapsed, spans = 0, {}
    for rasi in progression(lagna_sign).signs:
        if rasi in CO_LORDS:
            years = {g: dasa_length(rasi, g, signs[g],
                                    sign_dignity(g, longitudes[g])).years
                     for g in CO_LORDS[rasi]}
            lord = stronger(rasi, longitudes, purpose="dasa",
                            dasa_years=years).winner
        else:
            lord = int(RASI_LORD[rasi])
        length = dasa_length(rasi, lord, signs[lord],
                             sign_dignity(lord, longitudes[lord])).years
        spans[ABBR[rasi]] = (1872 + elapsed, 1872 + elapsed + length)
        elapsed += length
    return spans


def test_chart_38_recomputes_on_a_local_time_offset():
    """"5:17 am (5:53 East)" — Calcutta local time, not a zone. The only
    non-round offset in the register, and every body still lands inside one
    arcminute.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(38)
    assert record["birth_data"]["utc_offset_hours"] == 5 + 53 / 60
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 38", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(38)

    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 1.0


def test_chart_38_is_an_eleventh_vote_for_the_mean_node():
    """OI-68. Rahu is 66' out under `true` — second only to Chart 24's 79',
    and this is the earliest birth of the three widest, 1872.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(38)
    printed = longitudes(38)["Rahu"]
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name="Chart 38", **record["place"]),
            Settings(node_type=node))
        errors[node] = abs(
            computed.positions[int(Graha.RAHU)].longitude - printed) * 60

    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 60.0


def test_example_83s_groups_run_backward_forward_forward():
    """Cancer lagna: the 9th is Pisces, even-footed, so that group alone runs
    backward, and the 10th and 11th — Aries and Taurus — run forward. A third
    pattern, after Chart 36's one-forward and Chart 37's three-forward.
    """
    from hora.dasha.rasi.drigdasa import progression

    _longitudes, _signs, lagna_sign = _chart_38()
    assert lagna_sign == R["Cancer"]

    got = progression(lagna_sign)
    assert [g.leader_name for g in got.groups] == ["Pisces", "Aries", "Taurus"]
    assert [g.direction for g in got.groups] == [
        "backward", "forward", "forward"]
    assert [ABBR[s] for s in got.groups[0].signs] == ["Pi", "Sg", "Vi", "Ge"]
    assert [ABBR[s] for s in got.groups[1].signs] == ["Ar", "Le", "Sc", "Aq"]
    assert [ABBR[s] for s in got.groups[2].signs] == ["Ta", "Cn", "Li", "Cp"]
    assert [ABBR[s] for s in got.signs] == EX83_ORDER
    assert got.covers_every_rasi


@pytest.mark.parametrize("abbr", sorted(EX83_DATED))
def test_example_83s_three_dated_dasas(abbr):
    """"During 1906-1913, he was running Scorpio's dasa"; "During 1918-1925,
    he ran Cn dasa"; "Libra's dasa started in August 1925."

    Three dates spread across the run, so they check the order and the lengths
    of everything before them as well as their own.
    """
    start, _end = EX83_DATED[abbr]
    assert _chart_38_years()[abbr][0] == start


def test_libras_dasa_starts_in_the_birth_month():
    """"Libra's dasa started in August 1925." Every Drigdasa here is a whole
    number of years, so each one opens on the birth anniversary — August.
    """
    from hora.charts.book import chart

    assert chart(38)["birth_data"]["month"] == 8
    assert _chart_38_years()["Li"][0] == 1925
    assert _chart_38_years()["Cn"][1] == 1925


def test_example_83s_scorpio_needs_all_three_of_its_reasons():
    """"Scorpio is the 7th house from AL; it aspects lagna; and, it contains
    its lord Ketu."

    One rule from §21.3 and two from the examples. Rule 2 cannot reach the
    first of them: Scorpio is fixed, so it aspects Cancer, Capricorn and
    Aries — not Taurus, where AL sits.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_38_points()
    assert points["arudha_lagna"] == R["Taurus"]
    assert points["signs"][int(Graha.KETU)] == R["Scorpio"]
    assert R["Taurus"] not in rasi_drishti(R["Scorpio"])
    assert R["Cancer"] in rasi_drishti(R["Scorpio"])

    got = {r["rule"]: r for r in spiritual_readings(R["Scorpio"], **points)}
    assert set(got) == {7, 9, 10}
    assert got[10]["why"].endswith("the 7th from the arudha lagna Taurus")
    assert got[9]["why"] == "Scorpio aspects lagna Cancer"
    assert got[7]["why"] == "Ketu is in Scorpio"


def test_the_book_calls_ketu_scorpios_lord():
    """"it contains **its lord** Ketu." Scorpio's co-lordship, stated as
    plainly here as §15.5.1 states it, and the reason rule 7 and rule 11 can
    both point at the same graha on this chart.
    """
    from hora.charts.colord import CO_LORDS
    from hora.core.const import Graha

    assert int(Graha.KETU) in CO_LORDS[R["Scorpio"]]


def test_example_83s_cancer_is_rule_3_and_rule_4_together():
    """"As Cn contains lagna, its dasa brings true enlightenment and also
    recognition. During lagna's dasa, a monk can become a chief of a
    monastery."

    The second sentence is rule 4's own printed example returned as a reading —
    "A monk may, for example, become the Chief Pontiff of a monastery."
    """
    from hora.dasha.rasi.drigdasa import SPIRITUAL_READINGS, spiritual_readings

    points = _chart_38_points()
    got = {r["rule"]: r for r in spiritual_readings(R["Cancer"], **points)}
    assert {3, 4} <= set(got)
    assert got[3]["why"] == "Cancer is lagna"

    rule_4 = next(r for r in SPIRITUAL_READINGS if r["rule"] == 4)
    assert "Chief Pontiff of a monastery" in rule_4["text"]


def test_example_83s_libra_is_the_mrityupada_and_ketus_argala():
    """"Libra contains mrityupada and has the argala of Ketu."

    Rule 6 and rule 11. Ketu is in Scorpio, the 2nd from Libra, and the 12th
    that would obstruct it is Virgo, which is empty — so the argala stands
    without a question attached.
    """
    from hora.charts.argala import argalas_on_sign, ketu_sign_of, occupants_from
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_38_points()
    assert points["mrityupada"] == R["Libra"]

    signs = points["signs"]
    rows = argalas_on_sign(R["Libra"], occupants_from(signs),
                           ketu_sign=ketu_sign_of(signs))
    argala = next(r for r in rows
                  if r.kind == "argala" and int(Graha.KETU) in r.grahas)
    assert (argala.house, argala.argala_kind) == (2, "primary")
    obstruction = next(r for r in rows
                       if r.kind == "virodhargala" and r.house == 12)
    assert obstruction.grahas == ()

    got = {r["rule"]: r for r in spiritual_readings(R["Libra"], **points)}
    assert {6, 11} <= set(got)
    assert "unobstructed" in got[11]["why"]
    assert "undecided" not in got[11]


def test_rule_11_reports_an_obstructed_or_secondary_argala_as_undecided():
    """§10.6 obstructs an argala from its paired house and §10.5 makes the
    5th's a secondary one. Example 83 read an unobstructed primary, so neither
    case is settled — Chart 38's own Cancer has the secondary kind and is
    flagged rather than asserted. See OI-129.
    """
    from hora.dasha.rasi.drigdasa import spiritual_readings

    points = _chart_38_points()
    cancer = next(r for r in spiritual_readings(R["Cancer"], **points)
                  if r["rule"] == 11)
    assert "secondary" in cancer["why"]
    assert "secondary argala" in cancer["undecided"]

    leo = next(r for r in spiritual_readings(R["Leo"], **points)
               if r["rule"] == 11)
    assert "undecided" in leo


def test_the_eleven_readings_and_where_each_came_from():
    """Eight printed in §21.3, one from Example 81 and two from Example 83.
    Three of the chapter's four examples read a reference the section never
    lists, which is what OI-129 records.
    """
    from hora.dasha.rasi.drigdasa import (
        EXAMPLE_83_ADDS_TWO_REFERENCES,
        SPIRITUAL_READINGS,
    )

    sources = {r["rule"]: r["source"] for r in SPIRITUAL_READINGS}
    assert [r["rule"] for r in SPIRITUAL_READINGS] == list(range(1, 12))
    assert all(sources[n].startswith("\u00a721.3") for n in range(1, 9))
    assert sources[9] == "Example 81"
    assert sources[10] == sources[11] == "Example 83"

    printed = {r["reads"] for r in SPIRITUAL_READINGS
               if r["source"].startswith("\u00a721.3")}
    assert printed == {"AL", "lagna", "A5", "A8", "Ketu", "Rahu"}
    assert {r["reads"] for r in SPIRITUAL_READINGS} == printed

    assert "AL and the 7th from it" in EXAMPLE_83_ADDS_TWO_REFERENCES


def test_the_added_rules_read_the_same_six_references_differently():
    """None of the three added rules brings in a *new* point — they reach
    lagna, AL and Ketu by an aspect, by the 7th, and by argala. So §21.3's six
    references hold; it is the ways of reaching them that the section does not
    exhaust.
    """
    from hora.dasha.rasi.drigdasa import SPIRITUAL_READINGS

    added = {r["rule"]: r for r in SPIRITUAL_READINGS
             if not r["source"].startswith("\u00a721.3")}
    assert {r["reads"] for r in added.values()} == {"lagna", "AL", "Ketu"}
    assert "aspects" in added[9]["test"]
    assert "7th from" in added[10]["test"]
    assert "argala" in added[11]["test"]
