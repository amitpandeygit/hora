"""Chapter 24 — Kalachakra dasa, the wheel of Time.

The last of Part 2's nine. Its four printed tables are largely redundant, and
the point of these tests is to prove it: Table 43's mirror rule generates every
pada sequence of Tables 44 to 47, and Table 48's dasa years reproduce every
paramayush figure. What is *not* derivable — which sub-group a nakshatra sits
in — is held as printed and checked for completeness.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_ABBR

A = list(RASI_ABBR)
R = {abbr: index for index, abbr in enumerate(RASI_ABBR)}

#: Tables 44 to 47 exactly as printed: sequences, paramayush, deha and jeeva.
PRINTED_TABLES = {
    ("savya", 1): (
        (("Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg"),
         ("Cp", "Aq", "Pi", "Sc", "Li", "Vi", "Cn", "Le", "Ge"),
         ("Ta", "Ar", "Pi", "Aq", "Cp", "Sg", "Ar", "Ta", "Ge"),
         ("Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi")),
        (100, 85, 83, 86),
        (("Ar", "Sg"), ("Cp", "Ge"), ("Ta", "Ge"), ("Cn", "Pi"))),
    ("savya", 2): (
        (("Sc", "Li", "Vi", "Cn", "Le", "Ge", "Ta", "Ar", "Pi"),
         ("Aq", "Cp", "Sg", "Ar", "Ta", "Ge", "Cn", "Le", "Vi"),
         ("Li", "Sc", "Sg", "Cp", "Aq", "Pi", "Sc", "Li", "Vi"),
         ("Cn", "Le", "Ge", "Ta", "Ar", "Pi", "Aq", "Cp", "Sg")),
        (100, 85, 83, 86),
        (("Sc", "Pi"), ("Aq", "Vi"), ("Li", "Vi"), ("Cn", "Sg"))),
    ("apasavya", 1): (
        (("Sg", "Cp", "Aq", "Pi", "Ar", "Ta", "Ge", "Le", "Cn"),
         ("Vi", "Li", "Sc", "Pi", "Aq", "Cp", "Sg", "Sc", "Li"),
         ("Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg", "Cp", "Aq"),
         ("Pi", "Ar", "Ta", "Ge", "Le", "Cn", "Vi", "Li", "Sc")),
        (86, 83, 85, 100),
        (("Cn", "Sg"), ("Li", "Vi"), ("Aq", "Vi"), ("Sc", "Pi"))),
    ("apasavya", 2): (
        (("Pi", "Aq", "Cp", "Sg", "Sc", "Li", "Vi", "Le", "Cn"),
         ("Ge", "Ta", "Ar", "Sg", "Cp", "Aq", "Pi", "Ar", "Ta"),
         ("Ge", "Le", "Cn", "Vi", "Li", "Sc", "Pi", "Aq", "Cp"),
         ("Sg", "Sc", "Li", "Vi", "Le", "Cn", "Ge", "Ta", "Ar")),
        (86, 83, 85, 100),
        (("Cn", "Pi"), ("Ta", "Ge"), ("Cp", "Ge"), ("Ar", "Sg"))),
}

CASES = [(group, sub, pada)
         for (group, sub) in PRINTED_TABLES for pada in (1, 2, 3, 4)]


# --------------------------------------------------------------------------
# §24.1 Introduction
# --------------------------------------------------------------------------

def test_parasaras_claim_is_the_strongest_in_part_2():
    """"There is another dasa called Kalachakra dasa, which is the most
    respectable of all dasa systems."

    Chapter 22 called Niryaana Shoola dasa "the best for timing death" — a
    claim about one purpose, and the author's own. This one is Parasara's and
    unrestricted.
    """
    from hora.dasha.nakshatra.kalachakra import (
        KALACHAKRA_MEANS,
        PARASARA_VERSE,
        PARASARA_VERSE_MEANS,
        SHIVA_EXPLAINED_IT_TO_PARVATI,
    )
    from hora.dasha.rasi.niryaana_shoola import (
        THIS_DASA_IS_THE_BEST_FOR_TIMING_DEATH,
    )

    assert "कालचक्रदशा" in PARASARA_VERSE
    assert "most respectable of all dasa systems" in PARASARA_VERSE_MEANS
    assert "humble opinion" in THIS_DASA_IS_THE_BEST_FOR_TIMING_DEATH
    assert "wheel of Time" in KALACHAKRA_MEANS
    assert "Goddess Parvati" in SHIVA_EXPLAINED_IT_TO_PARVATI


def test_kalachakra_completes_part_2():
    """The ninth of nine, and the only nakshatra dasa in the book whose
    periods are rasis.
    """
    from hora.core.constants.dasha import PART_2_DASA_SYSTEMS

    by_name = {s["name"]: s for s in PART_2_DASA_SYSTEMS}
    assert by_name["Kalachakra dasa"]["kind"] == "nakshatra"
    assert by_name["Kalachakra dasa"]["purpose"] == "phalita"
    assert all(s.get("module") or s["key"] for s in PART_2_DASA_SYSTEMS)


# --------------------------------------------------------------------------
# §24.2 Table 42 — the two groups
# --------------------------------------------------------------------------

def test_table_42_is_one_sentence_and_the_sentence_computes():
    """"The first 3 nakshatras belong to the savya group, the next 3
    constellations to the apasavya group and so on."

    Fifteen savya against twelve apasavya, because 27 is not a multiple of six
    and the last triple falls savya.
    """
    from hora.dasha.nakshatra.kalachakra import (
        TABLE_42_APASAVYA,
        TABLE_42_SAVYA,
        group_of,
        is_savya,
    )

    assert tuple(n for n in range(1, 28) if is_savya(n)) == TABLE_42_SAVYA
    assert tuple(n for n in range(1, 28) if not is_savya(n)) == (
        TABLE_42_APASAVYA)
    assert len(TABLE_42_SAVYA) == 15
    assert len(TABLE_42_APASAVYA) == 12
    assert set(TABLE_42_SAVYA) | set(TABLE_42_APASAVYA) == set(range(1, 28))
    assert group_of(1) == "savya" and group_of(4) == "apasavya"
    assert group_of(27) == "savya"


def test_savya_and_apasavya_are_named_for_their_direction():
    from hora.dasha.nakshatra.kalachakra import APASAVYA_MEANS, SAVYA_MEANS

    assert SAVYA_MEANS == "zodiacal"
    assert APASAVYA_MEANS == "anti-zodiacal"


# --------------------------------------------------------------------------
# §24.2 Table 43 — the two wheels
# --------------------------------------------------------------------------

def test_the_mirror_rule_and_its_two_fixed_points():
    """"The other sign owned by the same planet... However, the mirror image
    of Cn is Cn itself and that of Le is Le itself, as they are the only signs
    owned by their lords."
    """
    from hora.dasha.nakshatra.kalachakra import MIRROR_RULE, mirror

    assert mirror(R["Ar"]) == R["Sc"]
    assert mirror(R["Ta"]) == R["Li"]
    assert mirror(R["Cp"]) == R["Aq"]
    assert mirror(R["Cn"]) == R["Cn"]
    assert mirror(R["Le"]) == R["Le"]

    for rasi in range(12):
        assert mirror(mirror(rasi)) == rasi
    fixed = [A[r] for r in range(12) if mirror(r) == r]
    assert fixed == ["Cn", "Le"]
    assert "the only signs owned by their lords" in MIRROR_RULE


def test_the_two_wheels_reproduce_table_43():
    """Table 43's four rows, derived from the mirror rule rather than typed."""
    from hora.dasha.nakshatra.kalachakra import wheel

    savya = [A[r] for r in wheel("savya")]
    assert savya[:12] == ["Ar", "Ta", "Ge", "Cn", "Le", "Vi",
                          "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
    assert savya[12:] == ["Sc", "Li", "Vi", "Cn", "Le", "Ge",
                          "Ta", "Ar", "Pi", "Aq", "Cp", "Sg"]

    apasavya = [A[r] for r in wheel("apasavya")]
    assert apasavya[:12] == ["Sg", "Cp", "Aq", "Pi", "Ar", "Ta",
                             "Ge", "Le", "Cn", "Vi", "Li", "Sc"]
    assert apasavya[12:] == ["Pi", "Aq", "Cp", "Sg", "Sc", "Li",
                             "Vi", "Le", "Cn", "Ge", "Ta", "Ar"]


def test_table_43s_printed_row_order_is_the_reading_order():
    """Savya prints Main above Mirrored and apasavya prints Mirrored above
    Main, and that is not decoration: concatenated the other way round,
    neither wheel produces Tables 44 to 47. §24.2 never says so.
    """
    from hora.dasha.nakshatra.kalachakra import (
        THE_ROW_ORDER_IN_TABLE_43_IS_THE_READING_ORDER,
        pada_sequence,
        wheel,
    )

    for group in ("savya", "apasavya"):
        ring = wheel(group)
        swapped = ring[12:] + ring[:12]
        printed = PRINTED_TABLES[(group, 1)][0][0]
        assert tuple(A[r] for r in pada_sequence(group, 1, 1)) == printed
        assert tuple(A[r] for r in swapped[:9]) != printed

    assert "printed order" in THE_ROW_ORDER_IN_TABLE_43_IS_THE_READING_ORDER


def test_a_bad_group_name_is_refused():
    from hora.dasha.nakshatra.kalachakra import KalachakraError, wheel

    with pytest.raises(KalachakraError, match="savya"):
        wheel("dakshina")


# --------------------------------------------------------------------------
# §24.2 Tables 44 to 47 — every pada, derived
# --------------------------------------------------------------------------

@pytest.mark.parametrize("group,sub,pada", CASES)
def test_every_printed_pada_sequence_comes_out_of_the_wheel(group, sub, pada):
    """All sixteen sequences of Tables 44 to 47, generated from Table 43. The
    tables are a convenience — "for the sake of those who do not understand
    the above logic well enough" — and this is that claim, tested.
    """
    from hora.dasha.nakshatra.kalachakra import pada_sequence

    expected = PRINTED_TABLES[(group, sub)][0][pada - 1]
    assert tuple(A[r] for r in pada_sequence(group, sub, pada)) == expected


@pytest.mark.parametrize("group,sub,pada", CASES)
def test_every_printed_paramayush_is_the_sum_of_its_nine(group, sub, pada):
    """Table 48's dasa years reproduce all sixteen paramayush figures, so that
    column checks the sequences rather than adding anything.
    """
    from hora.dasha.nakshatra.kalachakra import pada_sequence, paramayush

    expected = PRINTED_TABLES[(group, sub)][1][pada - 1]
    assert paramayush(pada_sequence(group, sub, pada)) == expected


@pytest.mark.parametrize("group,sub,pada", CASES)
def test_every_printed_deha_and_jeeva_follows_the_reversal(group, sub, pada):
    """Savya takes the first of the nine as Deha and the last as Jeeva;
    apasavya reverses it, which §24.2 flags in its own parenthesis.
    """
    from hora.dasha.nakshatra.kalachakra import deha_and_jeeva, pada_sequence

    deha, jeeva = PRINTED_TABLES[(group, sub)][2][pada - 1]
    got = deha_and_jeeva(group, pada_sequence(group, sub, pada))
    assert (A[got["deha"]], A[got["jeeva"]]) == (deha, jeeva)
    assert got["reversed"] is (group == "apasavya")


def test_the_paramayush_column_is_four_values_read_two_ways():
    """100, 85, 83, 86 down the savya tables and the same four reversed down
    the apasavya ones. Both total 354.
    """
    from hora.dasha.nakshatra.kalachakra import (
        PARAMAYUSH_IS_FOUR_VALUES_READ_TWO_WAYS,
        pada_sequence,
        paramayush,
    )

    savya = [paramayush(pada_sequence("savya", 1, p)) for p in (1, 2, 3, 4)]
    apasavya = [paramayush(pada_sequence("apasavya", 1, p))
                for p in (1, 2, 3, 4)]
    assert savya == [100, 85, 83, 86]
    assert apasavya == list(reversed(savya))
    assert sum(savya) == sum(apasavya) == 354
    assert "same four figures reversed" in (
        PARAMAYUSH_IS_FOUR_VALUES_READ_TWO_WAYS)


def test_the_two_sub_groups_sit_half_a_wheel_apart():
    """Four padas of nine rasis are thirty-six wheel positions, and 36 mod 24
    is 12 — which is why there are exactly two sub-groups and why the second
    starts halfway round.
    """
    from hora.dasha.nakshatra.kalachakra import SUB_GROUP_OFFSET, pada_sequence

    assert SUB_GROUP_OFFSET == {1: 0, 2: 12}
    assert (4 * 9) % 24 == 12

    for group in ("savya", "apasavya"):
        first = pada_sequence(group, 1, 1)
        second = pada_sequence(group, 2, 1)
        assert first != second
        # Sub-group 2's first pada is sub-group 1's wheel shifted by twelve.
        assert second == pada_sequence(group, 1, 2)[3:] + tuple(
            pada_sequence(group, 1, 3)[:3])


# --------------------------------------------------------------------------
# Table 48
# --------------------------------------------------------------------------

def test_table_48_is_keyed_on_the_lord_so_mirrored_rasis_agree():
    """"Two rasis owned by the same planet have the same duration" — which is
    what makes the mirrored wheel consistent with the dasa lengths.
    """
    from hora.dasha.nakshatra.kalachakra import dasa_years, mirror

    printed = {"Le": 5, "Cn": 21, "Ar": 7, "Sc": 7, "Ge": 9, "Vi": 9,
               "Sg": 10, "Pi": 10, "Ta": 16, "Li": 16, "Cp": 4, "Aq": 4}
    for abbr, years in printed.items():
        assert dasa_years(R[abbr]) == years
    for rasi in range(12):
        assert dasa_years(rasi) == dasa_years(mirror(rasi))
    assert sum(dasa_years(r) for r in range(12)) == 118


# --------------------------------------------------------------------------
# D-67 and OI-139 — the sub-group memberships
# --------------------------------------------------------------------------

def test_the_savya_sub_group_tables_lose_a_nakshatra():
    """D-67. Table 42 puts fifteen nakshatras in the savya group; Tables 44
    and 45 name nine and five. Uttarabhadrapada is in neither, and the
    apasavya tables are complete.
    """
    from hora.dasha.nakshatra.kalachakra import (
        PRINTED_SUB_GROUPS,
        SAVYA_SUB_GROUPS_LOSE_A_NAKSHATRA,
        TABLE_42_APASAVYA,
        TABLE_42_SAVYA,
    )

    savya = set(PRINTED_SUB_GROUPS["savya-1"]) | set(
        PRINTED_SUB_GROUPS["savya-2"])
    assert len(savya) == 14
    assert set(TABLE_42_SAVYA) - savya == {26}      # Uttarabhadrapada

    apasavya = set(PRINTED_SUB_GROUPS["apasavya-1"]) | set(
        PRINTED_SUB_GROUPS["apasavya-2"])
    assert apasavya == set(TABLE_42_APASAVYA)
    assert "is in neither" in SAVYA_SUB_GROUPS_LOSE_A_NAKSHATRA


def test_the_two_groups_are_sub_divided_on_different_patterns():
    """OI-139. Savya-1 takes the 1st and 3rd of each triple and savya-2 the
    2nd; apasavya-1 takes only the 1st and apasavya-2 the 2nd and 3rd. No one
    rule gives both, and it decides the whole dasa for the 3rd of each
    apasavya triple.
    """
    from hora.dasha.nakshatra.kalachakra import (
        PRINTED_SUB_GROUPS,
        THE_SUB_GROUP_PATTERNS_DISAGREE,
    )

    def positions(members, triples):
        return {tuple(sorted(t.index(n) for n in members if n in t))
                for t in triples}

    savya_triples = [(1, 2, 3), (7, 8, 9), (13, 14, 15), (19, 20, 21)]
    assert positions(PRINTED_SUB_GROUPS["savya-1"], savya_triples) == {(0, 2)}
    assert positions(PRINTED_SUB_GROUPS["savya-2"], savya_triples) == {(1,)}

    apasavya_triples = [(4, 5, 6), (10, 11, 12), (16, 17, 18), (22, 23, 24)]
    assert positions(PRINTED_SUB_GROUPS["apasavya-1"],
                     apasavya_triples) == {(0,)}
    assert positions(PRINTED_SUB_GROUPS["apasavya-2"],
                     apasavya_triples) == {(1, 2)}

    assert "No single rule produces both" in THE_SUB_GROUP_PATTERNS_DISAGREE


def test_uttarabhadrapada_is_refused_rather_than_guessed():
    """Its sub-group fixes its four sequences, so a guess would decide the
    whole dasa silently. Every other nakshatra resolves.
    """
    from hora.dasha.nakshatra.kalachakra import KalachakraError, sub_group_of

    with pytest.raises(KalachakraError, match="D-67"):
        sub_group_of(26)

    for nakshatra in range(1, 28):
        if nakshatra != 26:
            assert sub_group_of(nakshatra) in (1, 2)


# --------------------------------------------------------------------------
# §24.2's five-step procedure
# --------------------------------------------------------------------------

def test_the_procedure_is_five_steps_and_the_last_two_are_the_hard_ones():
    from hora.dasha.nakshatra.kalachakra import PROCEDURE

    assert len(PROCEDURE) == 5
    assert PROCEDURE[0].startswith("Find the nakshatra pada")
    assert "other sub-group in the same group" in PROCEDURE[3]
    assert "proportionally" in PROCEDURE[4]


def test_step_1_and_2_read_the_moons_pada_and_how_far_into_it():
    """Aswini spans 0 to 13°20', so its first pada ends at 3°20'. A Moon at
    1°40' is halfway through pada 1 of nakshatra 1.
    """
    from hora.dasha.nakshatra.kalachakra import pada_of

    got = pada_of(1.0 + 40.0 / 60.0)
    assert got["nakshatra"] == 1
    assert got["group"] == "savya"
    assert got["pada"] == 1
    assert abs(got["elapsed_fraction"] - 0.5) < 1e-9

    # The last pada of Revati ends the zodiac.
    end = pada_of(359.999)
    assert end["nakshatra"] == 27 and end["pada"] == 4


def test_step_3_picks_the_dasa_running_at_birth_and_its_balance():
    """"Find the same fraction of the paramayush... Based on this, we can find
    which of the nine dasas runs at birth and how much of the dasa remains."

    §24.2's own illustration: a Moon at the *beginning* of Aswini's first pada
    runs Aries; in the *middle* it may run Leo; towards the *end*,
    Sagittarius.
    """
    from hora.dasha.nakshatra.kalachakra import (
        first_dasa,
        pada_sequence,
        paramayush,
    )

    nine = pada_sequence("savya", 1, 1)
    assert paramayush(nine) == 100

    start = first_dasa(nine, 0.0)
    assert start["rasi"] == "Aries"
    assert start["balance_years"] == 7

    # Ar 0-7, Ta 7-23, Ge 23-32, Cn 32-53, Le 53-58, Vi 58-67, Li 67-83,
    # Sc 83-90, Sg 90-100. Half the paramayush is 50 years, which is Cancer —
    # the book says a middling Moon "**may**" run Leo, and Leo starts at 53.
    middle = first_dasa(nine, 0.5)
    assert middle["rasi"] == "Cancer"
    assert middle["elapsed_years"] == pytest.approx(50 - 32)
    assert middle["balance_years"] == pytest.approx(53 - 50)
    assert first_dasa(nine, 0.55)["rasi"] == "Leo"

    late = first_dasa(nine, 0.95)
    assert late["rasi"] == "Sagittarius"
    assert first_dasa(nine, 1.0)["rasi"] == "Sagittarius"


def test_24_2s_three_illustrations_of_the_starting_dasa():
    """"One born with Moon at the beginning of the first pada of Aswini will
    run Ar dasa at birth and run Ta, Ge, Cn, Le, Vi, Li, Sc and Sg dasas after
    it." The other two illustrations name Le and Sg as the starting dasa, and
    both are in the same nine.
    """
    from hora.dasha.nakshatra.kalachakra import pada_sequence

    nine = [A[r] for r in pada_sequence("savya", 1, 1)]
    assert nine == ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg"]
    for named in ("Ar", "Le", "Sg"):
        assert named in nine


def test_the_fraction_and_the_sequence_length_are_both_checked():
    from hora.dasha.nakshatra.kalachakra import (
        KalachakraError,
        first_dasa,
        pada_sequence,
        paramayush,
    )

    nine = pada_sequence("savya", 1, 1)
    with pytest.raises(KalachakraError, match="between 0 and 1"):
        first_dasa(nine, 1.5)
    with pytest.raises(KalachakraError, match="nine rasis"):
        paramayush(nine[:8])


# --------------------------------------------------------------------------
# Example 95 — a Moon at 15 Ta 50, worked end to end.
# --------------------------------------------------------------------------

EX95_MOON = 30.0 + 15.0 + 50.0 / 60.0          # 15 Ta 50
EX95_NINE = ("Vi", "Li", "Sc", "Pi", "Aq", "Cp", "Sg", "Sc", "Li")
EX95_YEARS = (9, 16, 7, 10, 4, 4, 10, 7, 16)
EX95_CUMULATIVE = (9, 25, 32, 42, 46, 50, 60, 67, 83)


def test_example_95_step_1_the_moons_pada():
    """"Moon is in Rohini 2nd pada, which runs from 13Ta20 to 16Ta40."

    Rohini is nakshatra 4, so apasavya — and Table 46 is Apasavya-1, which is
    where the example goes.
    """
    from hora.dasha.nakshatra.kalachakra import pada_of, sub_group_of

    got = pada_of(EX95_MOON)
    assert got["nakshatra"] == 4
    assert got["group"] == "apasavya"
    assert got["pada"] == 2
    assert sub_group_of(4) == 1

    # The pada's own bounds, as the example states them.
    assert 40.0 + 3.0 + 20.0 / 60.0 == pytest.approx(13.0 + 20.0 / 60.0 + 30)
    assert 43.0 + 20.0 / 60.0 < EX95_MOON < 46.0 + 40.0 / 60.0


def test_example_95_step_1_the_nine_rasis_and_their_years():
    """"From Table 46, we find that the 9 rasis associated with this nakshatra
    pada are: Vi, Li, Sc, Pi, Aq, Cp, Sg, Sc, Li."

    And Table 49's own two rows — the Table 48 lengths and their running sum,
    ending at the paramayush of 83.
    """
    from hora.dasha.nakshatra.kalachakra import (
        dasa_years,
        pada_sequence,
        paramayush,
    )

    nine = pada_sequence("apasavya", 1, 2)
    assert tuple(A[r] for r in nine) == EX95_NINE
    assert tuple(dasa_years(r) for r in nine) == EX95_YEARS

    running, cumulative = 0, []
    for rasi in nine:
        running += dasa_years(rasi)
        cumulative.append(running)
    assert tuple(cumulative) == EX95_CUMULATIVE
    assert paramayush(nine) == 83 == EX95_CUMULATIVE[-1]


def test_example_95_step_2_the_fraction_is_three_quarters():
    """"The amount of the nakshatra pada traversed by Moon is 15°50' - 13°20'
    = 2°30'. The fraction ... is (2°30')/(3°20') = 150'/200' = 0.75."
    """
    from hora.dasha.nakshatra.kalachakra import pada_of

    assert pada_of(EX95_MOON)["elapsed_fraction"] == pytest.approx(0.75)
    assert (2 * 60 + 30) / (3 * 60 + 20) == 0.75


def test_example_95_step_3_scorpio_runs_at_birth_with_4_75_left():
    """"0.75 x 83 = 62.25 years... 60 years were over by the end of Sg dasa
    and 2.25 years of Sc dasa added to it makes it 62.25. So Sc dasa was
    running at birth and 7 - 2.25 = 4.75 years of Sc dasa were remaining."
    """
    from hora.dasha.nakshatra.kalachakra import first_dasa, pada_sequence

    nine = pada_sequence("apasavya", 1, 2)
    got = first_dasa(nine, 0.75)

    assert got["consumed_years"] == pytest.approx(62.25)
    assert got["rasi"] == "Scorpio"
    assert got["position"] == 7                 # the 8th of the nine
    assert got["years"] == 7
    assert got["elapsed_years"] == pytest.approx(2.25)
    assert got["balance_years"] == pytest.approx(4.75)


def test_example_95_the_dates_the_balance_gives():
    """"By adding 4 years 9 months to the birthdate, we get the date on which
    Sc dasa ends. Then Li dasa of 16 years will run till an age of 20 years 9
    months."
    """
    from hora.dasha.nakshatra.kalachakra import dasa_years

    balance = 7 - 2.25
    assert balance == 4.75
    assert balance * 12 == 57                    # 4 years 9 months
    assert balance + dasa_years(R["Li"]) == 20.75
    assert 20.75 * 12 == 249                     # 20 years 9 months


def test_example_95_step_4_crosses_into_the_next_pada():
    """"With Li dasa, we finish the nine rasis associated with the 2nd pada of
    Rohini (Apasavya-1). So we go to the 3rd pada in the same table. The next
    7 dasas will be Vi, Le, Cn, Ge, Ta, Ar, Sg."

    Note the crossing stays in the **same** table: rule (4) sends you to the
    other sub-group only after a nakshatra's *4th* pada.
    """
    from hora.dasha.nakshatra.kalachakra import dasa_order, pada_sequence

    following = dasa_order(4, 2, 7, skip=9)
    assert [row["rasi"][:2] for row in following] == [
        "Vi", "Le", "Ca", "Ge", "Ta", "Ar", "Sa"]
    assert [A[row["sign"]] for row in following] == [
        "Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg"]

    # They are the opening of Table 46's third pada, same sub-group.
    third = pada_sequence("apasavya", 1, 3)
    assert [A[r] for r in third[:7]] == [A[row["sign"]] for row in following]


def test_rule_4_is_one_walk_of_the_wheel():
    """The rule reads as three cases and is one. A pada is nine consecutive
    wheel positions; four padas are thirty-six, a wheel and a half, which
    lands the next nakshatra on the other sub-group without being told to.
    """
    from hora.dasha.nakshatra.kalachakra import (
        RULE_4_IS_JUST_WALKING_THE_WHEEL,
        SUB_GROUP_OFFSET,
        dasa_order,
        pada_sequence,
        wheel,
    )

    ring = wheel("apasavya")
    walk = dasa_order(4, 1, 40)
    for step, row in enumerate(walk):
        assert row["sign"] == ring[step % 24]

    # Positions 0-8, 9-17, 18-26, 27-35 are the four padas; 36 is offset 12.
    for pada in (1, 2, 3, 4):
        start = (pada - 1) * 9
        assert tuple(row["sign"] for row in walk[start:start + 9]) == (
            pada_sequence("apasavya", 1, pada))
    assert walk[36]["position"] == SUB_GROUP_OFFSET[2]
    assert "repeating these 24-rasi sequences" in (
        RULE_4_IS_JUST_WALKING_THE_WHEEL)


def test_rule_5_shares_a_dasa_out_in_table_48_proportion():
    """"We take 9 rasis starting from dasa rasi... We distribute the dasa
    length among the 9 antardasas proportionally."

    Example 95's Scorpio dasa is seven years, and the nine from Scorpio's
    wheel position share it out in proportion to their own lengths — the
    first antardasa being Scorpio itself.
    """
    from hora.dasha.nakshatra.kalachakra import antardasas, wheel_position

    scorpio = wheel_position(4, 2) + 7          # the 8th of the pada's nine
    got = antardasas(4, scorpio % 24, 7.0)

    assert len(got) == 9
    assert got[0]["rasi"] == "Scorpio"          # antardasas start from it
    assert [A[row["sign"]] for row in got] == [
        "Sc", "Li", "Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg"]
    assert sum(row["years"] for row in got) == pytest.approx(7.0)

    total = sum(row["share_years"] for row in got)
    for row in got:
        assert row["years"] == pytest.approx(7.0 * row["share_years"] / total)


def test_rule_5_runs_past_the_padas_end_without_being_told_to():
    """"If we reach the end of the nine rasis corresponding to the nakshatra
    pada when counting 9 rasis from dasa rasi, we proceed to the next
    nakshatra pada as described in rule (4)."

    Scorpio is the 8th of its pada, so seven of its nine antardasas fall in
    the following pada — and the wheel supplies them with no special case.
    """
    from hora.dasha.nakshatra.kalachakra import (
        antardasas,
        pada_sequence,
        wheel_position,
    )

    pada = set(pada_sequence("apasavya", 1, 2))
    scorpio = (wheel_position(4, 2) + 7) % 24
    got = antardasas(4, scorpio, 7.0)

    inside = [row for row in got if row["position"] in
              range(wheel_position(4, 2), wheel_position(4, 2) + 9)]
    assert len(inside) == 2                     # Scorpio and Libra
    assert pada                                  # the pada is non-empty


def test_footnote_63_is_the_denominator_both_examples_divide_by():
    """"The complete length of each nakshatra pada is 3\u00b020'." Examples 95
    and 96 both divide by 200 minutes without saying where it comes from.
    """
    from hora.core.constants.nakshatra import PADA_SPAN
    from hora.dasha.nakshatra.kalachakra import FOOTNOTE_63

    assert "3\u00b020'" in FOOTNOTE_63
    assert PADA_SPAN == pytest.approx(10.0 / 3.0)
    assert PADA_SPAN * 60 == pytest.approx(200.0)


def test_footnote_64_explains_a_count_neither_example_states():
    """Parasara displays nine dasas starting from the one running at birth, so
    the number taken from the next pada is the running dasa's own position.
    """
    from hora.dasha.nakshatra.kalachakra import (
        FOOTNOTE_64,
        THE_LISTED_COUNT_IS_NINE_LESS_WHAT_THE_PADA_STILL_HOLDS,
        nine_from_birth,
    )

    assert "nine rasis starting from the rasi" in FOOTNOTE_64
    assert "seven" in THE_LISTED_COUNT_IS_NINE_LESS_WHAT_THE_PADA_STILL_HOLDS

    # Example 95: Scorpio is 8th of Rohini's 2nd pada, so Sc and Li remain.
    got = nine_from_birth(4, 2, 7)
    assert (got["from_this_pada"], got["from_next_pada"]) == (2, 7)
    assert [A[row["sign"]] for row in got["dasas"]] == [
        "Sc", "Li", "Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg"]

    # Example 96: Pisces is 9th of Punarvasu's 4th pada, so Pi alone remains.
    got = nine_from_birth(7, 4, 8)
    assert (got["from_this_pada"], got["from_next_pada"]) == (1, 8)
    assert [A[row["sign"]] for row in got["dasas"]] == [
        "Pi", "Sc", "Li", "Vi", "Cn", "Le", "Ge", "Ta", "Ar"]


def test_the_listed_count_is_a_display_convention_not_a_boundary():
    """Nine is where the *printing* stops, not the walk. A tenth dasa follows
    and it is simply the next rasi on the wheel.
    """
    from hora.dasha.nakshatra.kalachakra import dasa_order, nine_from_birth

    nine = nine_from_birth(7, 4, 8)["dasas"]
    ten = dasa_order(7, 4, 10, skip=8)
    assert ten[:9] == nine
    assert A[ten[9]["sign"]] == "Pi"             # savya-2 pada 1's ninth


def test_footnote_65_is_16_2s_controversy_again_naming_kalachakra():
    """It does not open a new question; it is fresh evidence for OI-115, whose
    scope is nakshatra dasas and which Kalachakra is now stated to be.
    """
    from hora.dasha.nakshatra.kalachakra import FOOTNOTE_65

    assert "prefers savana years with all nakshatra dasas" in FOOTNOTE_65
    assert "Kalachakra dasa is a nakshatra dasa" in FOOTNOTE_65


def test_nine_from_birth_checks_its_position():
    from hora.core.validate import InputError
    from hora.dasha.nakshatra.kalachakra import nine_from_birth

    with pytest.raises(InputError, match="between 0 and 8"):
        nine_from_birth(7, 4, 9)
    with pytest.raises(InputError, match="between 0 and 8"):
        nine_from_birth(7, 4, -1)


# ---------------------------------------------------------------------------
# Example 96 — Moon at 3Cn00, Punarvasu 4th pada
# ---------------------------------------------------------------------------

def test_example_96_finds_punarvasu_4th_pada():
    """"Moon is in Punarvasu 4th pada, which runs from 0Cn00 to 3Cn20."
    """
    from hora.core.constants.nakshatra import NAKSHATRA_SPAN, PADA_SPAN
    from hora.dasha.nakshatra.kalachakra import pada_of, sub_group_of

    got = pada_of(3.0 + 90.0)
    assert got["nakshatra"] == 7                 # Punarvasu
    assert got["group"] == "savya"
    assert got["pada"] == 4
    assert sub_group_of(7) == 1                  # Table 44

    start = 6 * NAKSHATRA_SPAN + 3 * PADA_SPAN
    assert start == pytest.approx(90.0)          # 0Cn00
    assert start + PADA_SPAN == pytest.approx(93.0 + 1.0 / 3.0)   # 3Cn20


def test_example_96_reproduces_table_50():
    """"From Table 44, we find that the 9 rasis associated with this nakshatra
    pada are: Cn, Le, Vi, Li, Sc, Sg, Cp, Aq, Pi."
    """
    from hora.dasha.nakshatra.kalachakra import (
        dasa_years,
        pada_sequence,
        paramayush,
    )

    nine = pada_sequence("savya", 1, 4)
    assert [A[rasi] for rasi in nine] == [
        "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

    years = [dasa_years(rasi) for rasi in nine]
    assert years == [21, 5, 9, 16, 7, 10, 4, 4, 10]

    cumulative, running = [], 0
    for span in years:
        running += span
        cumulative.append(running)
    assert cumulative == [21, 26, 35, 51, 58, 68, 72, 76, 86]
    assert paramayush(nine) == 86


def test_example_96_pisces_runs_at_birth_with_8_point_6_years_left():
    """"The fraction of the pada traversed by Moon is (3\u00b00')/(3\u00b020')
    = 180'/200' = 0.9. ... 0.9 x 86 = 77.4 years. ... So Pi dasa was running at
    birth and 10 - 1.4 = 8.6 years of Pi dasa were remaining at birth."
    """
    from hora.dasha.nakshatra.kalachakra import (
        first_dasa,
        pada_of,
        pada_sequence,
    )

    moon = pada_of(93.0)
    assert moon["elapsed_fraction"] == pytest.approx(180.0 / 200.0)

    got = first_dasa(pada_sequence("savya", 1, 4), moon["elapsed_fraction"])
    assert got["consumed_years"] == pytest.approx(77.4)
    assert got["rasi"] == "Pisces"
    assert got["position"] == 8                  # the last of the nine
    assert got["years"] == 10
    assert got["elapsed_years"] == pytest.approx(1.4)
    assert got["balance_years"] == pytest.approx(8.6)


def test_example_96s_months_and_days_do_not_separate_the_year_lengths():
    """"By adding 8 years 7 months 6 days to the birthdate, we get the date on
    which Pi dasa ends." The figure comes out the same under savana and under
    365.25 days, so it is no evidence either way for OI-115.
    """
    from hora.core.const import SAVANA_YEAR_DAYS
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_96S_MONTHS_AND_DAYS_DECIDE_NOTHING,
    )
    from hora.dasha.rasi.sudasa import years_to_dasa_ymdh

    assert years_to_dasa_ymdh(8.6)[:3] == (8, 7, 6)
    assert "360-day year" in EXAMPLE_96S_MONTHS_AND_DAYS_DECIDE_NOTHING

    for year_days in (SAVANA_YEAR_DAYS, 365.25):
        days = 0.6 * year_days
        month = year_days / 12.0
        assert int(days // month) == 7
        assert round(days - 7 * month) == 6


def test_example_96_crosses_into_savya_2_by_walking_the_wheel():
    """"With Pi dasa, we finish the nine rasis associated with the 4th pada of
    Punarvasu (Savya-1). So we go to the 1st pada of Savya-2 nakshatras (Table
    45). The next 8 dasas will be Sc, Li, Vi, Cn, Le, Ge, Ta, Ar."

    Rule (4)'s hardest case, and the walk needs no help with it: the eight sit
    at wheel positions 12 to 19, which is exactly where Savya-2's first pada
    begins.
    """
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        pada_sequence,
        wheel_position,
    )

    got = dasa_order(7, 4, 8, skip=9)
    assert [A[row["sign"]] for row in got] == [
        "Sc", "Li", "Vi", "Cn", "Le", "Ge", "Ta", "Ar"]
    assert [row["years"] for row in got] == [7, 16, 9, 21, 5, 9, 16, 7]

    assert [row["position"] for row in got] == list(range(12, 20))
    assert wheel_position(8, 1) == 12             # Pushyami, Savya-2
    assert [A[rasi] for rasi in pada_sequence("savya", 2, 1)][:8] == [
        A[row["sign"]] for row in got]


def test_the_four_padas_of_a_nakshatra_land_on_the_other_sub_group():
    """Thirty-six wheel steps is a wheel and a half, so a nakshatra's four
    padas end exactly half a wheel on -- which is the other sub-group's offset.
    Example 96 is the case in point; this asserts it for every savya nakshatra
    a table names.
    """
    from hora.dasha.nakshatra.kalachakra import (
        PRINTED_SUB_GROUPS,
        SUB_GROUP_OFFSET,
        wheel_position,
    )

    for group in ("savya", "apasavya"):
        for sub in (1, 2):
            for nakshatra in PRINTED_SUB_GROUPS[f"{group}-{sub}"]:
                after = (wheel_position(nakshatra, 4) + 9) % 24
                assert after == SUB_GROUP_OFFSET[2 if sub == 1 else 1]


def test_dasa_order_and_antardasas_check_their_inputs():
    from hora.dasha.nakshatra.kalachakra import (
        KalachakraError,
        antardasas,
        dasa_order,
    )

    with pytest.raises(KalachakraError, match="count must be positive"):
        dasa_order(4, 2, 0)
    with pytest.raises(KalachakraError, match="skip cannot be negative"):
        dasa_order(4, 2, 3, skip=-1)
    with pytest.raises(KalachakraError, match="must be positive"):
        antardasas(4, 0, 0.0)
    with pytest.raises(KalachakraError, match="D-67"):
        dasa_order(26, 1, 3)


# ---------------------------------------------------------------------------
# Exercise 34 — Moon at 5Aq50, Dhanishtha 4th pada
# ---------------------------------------------------------------------------

def test_exercise_34_finds_dhanishtha_4th_pada():
    """"Moon at 5Aq50 is in Dhanishtha 4th pada, which runs from 3Aq20 to
    6Aq40."
    """
    from hora.core.constants.nakshatra import NAKSHATRA_SPAN, PADA_SPAN
    from hora.dasha.nakshatra.kalachakra import pada_of, sub_group_of

    got = pada_of(300.0 + 5.0 + 50.0 / 60.0)
    assert got["nakshatra"] == 23                # Dhanishtha
    assert got["group"] == "apasavya"
    assert got["pada"] == 4
    assert sub_group_of(23) == 2                 # Table 47

    start = 22 * NAKSHATRA_SPAN + 3 * PADA_SPAN
    assert start == pytest.approx(303.0 + 1.0 / 3.0)          # 3Aq20
    assert start + PADA_SPAN == pytest.approx(306.0 + 2.0 / 3.0)   # 6Aq40


def test_exercise_34_reproduces_table_52():
    """"From Table 47, we find that the 9 rasis associated with this nakshatra
    pada are: Sg, Sc, Li, Vi, Le, Cn, Ge, Ta, Ar."
    """
    from hora.dasha.nakshatra.kalachakra import (
        dasa_years,
        pada_sequence,
        paramayush,
    )

    nine = pada_sequence("apasavya", 2, 4)
    assert [A[rasi] for rasi in nine] == [
        "Sg", "Sc", "Li", "Vi", "Le", "Cn", "Ge", "Ta", "Ar"]

    years = [dasa_years(rasi) for rasi in nine]
    assert years == [10, 7, 16, 9, 5, 21, 9, 16, 7]

    cumulative, running = [], 0
    for span in years:
        running += span
        cumulative.append(running)
    assert cumulative == [10, 17, 33, 42, 47, 68, 77, 93, 100]
    assert paramayush(nine) == 100               # the longest of the sixteen


def test_exercise_34_gemini_runs_at_birth_with_2_years_left():
    """"0.75 x 100 = 75 years. ... 68 years were over by the end of Cn dasa and
    7 years of Ge dasa added to it makes it 75 years. So Ge dasa was running at
    birth and 9 - 7 = 2 years of Ge dasa were remaining at birth."
    """
    from hora.dasha.nakshatra.kalachakra import (
        first_dasa,
        pada_of,
        pada_sequence,
    )

    moon = pada_of(300.0 + 5.0 + 50.0 / 60.0)
    assert moon["elapsed_fraction"] == pytest.approx(150.0 / 200.0)

    got = first_dasa(pada_sequence("apasavya", 2, 4), moon["elapsed_fraction"])
    assert got["consumed_years"] == pytest.approx(75.0)
    assert got["rasi"] == "Gemini"
    assert got["position"] == 6
    assert got["years"] == 9
    assert got["elapsed_years"] == pytest.approx(7.0)
    assert got["balance_years"] == pytest.approx(2.0)


def test_exercise_34_crosses_from_apasavya_2_to_apasavya_1():
    """"With Ar dasa, we finish the nine rasis associated with the 4th pada of
    Dhanishtha (Apasavya-2). So we go to the 1st pada of Apasavya-1 nakshatras
    (Table 46). The next 7 dasas will be Sg, Cp, Aq, Pi, Ar, Ta, Ge."

    The crossing Example 96 made in the savya group, made here in the apasavya
    group and in the other direction -- sub-group 2 to sub-group 1, over the
    wheel's own end. Still one walk.
    """
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        pada_sequence,
        wheel_position,
    )

    assert wheel_position(23, 4) == 15           # positions 15 to 23
    got = dasa_order(23, 4, 7, skip=9)
    assert [A[row["sign"]] for row in got] == [
        "Sg", "Cp", "Aq", "Pi", "Ar", "Ta", "Ge"]
    assert [row["position"] for row in got] == list(range(7))

    assert wheel_position(4, 1) == 0             # Rohini, Apasavya-1
    assert [A[rasi] for rasi in pada_sequence("apasavya", 1, 1)][:7] == [
        A[row["sign"]] for row in got]


def test_exercise_34_reproduces_every_age_in_the_answer():
    """The answer's ten rows, in years of age, from the balance at birth and
    Table 48 alone.
    """
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        first_dasa,
        pada_of,
        pada_sequence,
    )

    moon = pada_of(300.0 + 5.0 + 50.0 / 60.0)
    birth = first_dasa(pada_sequence("apasavya", 2, 4), moon["elapsed_fraction"])
    walk = dasa_order(23, 4, 10, skip=birth["position"])

    rows, age = [], 0.0
    for position, row in enumerate(walk):
        span = birth["balance_years"] if position == 0 else float(row["years"])
        rows.append((A[row["sign"]], round(span), round(age), round(age + span)))
        age += span

    assert rows == [
        ("Ge", 2, 0, 2), ("Ta", 16, 2, 18), ("Ar", 7, 18, 25),
        ("Sg", 10, 25, 35), ("Cp", 4, 35, 39), ("Aq", 4, 39, 43),
        ("Pi", 10, 43, 53), ("Ar", 7, 53, 60), ("Ta", 16, 60, 76),
        ("Ge", 9, 76, 85),
    ]


def test_exercise_34_prints_a_tenth_dasa_footnote_64_does_not_allow():
    """Gemini sits 7th of its pada, leaving three, so footnote 64 gives six
    from the next pada and nine in all. The answer prints seven and ten. D-68.
    """
    from hora.dasha.nakshatra.kalachakra import (
        EXERCISE_34_PRINTS_A_TENTH_DASA,
        dasa_order,
        nine_from_birth,
    )

    by_the_rule = nine_from_birth(23, 4, 6)
    assert (by_the_rule["from_this_pada"], by_the_rule["from_next_pada"]) == (3, 6)
    assert len(by_the_rule["dasas"]) == 9
    assert A[by_the_rule["dasas"][-1]["sign"]] == "Ta"        # age 76, not 85

    printed = dasa_order(23, 4, 10, skip=6)
    assert printed[:9] == by_the_rule["dasas"]                # the ten hold the
    assert A[printed[9]["sign"]] == "Ge"                      # nine unchanged
    assert len({row["sign"] for row in printed}) == 7         # only 7 distinct
    assert "ten dasas" in EXERCISE_34_PRINTS_A_TENTH_DASA


# ---------------------------------------------------------------------------
# Example 97 — antardasa sequences in Example 95's first four dasas
# ---------------------------------------------------------------------------

#: The four sequences the example prints, in its own order.
EXAMPLE_97 = (
    (16, "Sc", ["Sc", "Li", "Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg"]),
    (17, "Li", ["Li", "Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg", "Cp"]),
    (18, "Vi", ["Vi", "Le", "Cn", "Ge", "Ta", "Ar", "Sg", "Cp", "Aq"]),
    (19, "Le", ["Le", "Cn", "Ge", "Ta", "Ar", "Sg", "Cp", "Aq", "Pi"]),
)


@pytest.mark.parametrize(("index", "dasa", "expected"), EXAMPLE_97)
def test_example_97_antardasa_sequences(index, dasa, expected):
    """"Antardasas in Li dasa (2nd dasa) go as Li, Vi, Le, Cn, Ge, Ta, Ar, Sg,
    Cp" -- and so for the 1st, 3rd and 4th. Each is nine steps of the apasavya
    wheel from the dasa rasi's own position.
    """
    from hora.dasha.nakshatra.kalachakra import antardasas, dasa_order

    got = antardasas(4, index, 1.0)
    assert [A[row["sign"]] for row in got] == expected
    assert A[got[0]["sign"]] == dasa            # they start from the dasa rasi

    # and that position is where Example 95's dasa walk puts this dasa
    order = dasa_order(4, 2, 4, skip=7)
    assert order[index - 16]["position"] == index
    assert A[order[index - 16]["sign"]] == dasa


def test_example_97_the_first_dasas_nine_end_the_pada_then_continue():
    """"After Sc, we have Li and the 9 rasis corresponding to the 2nd pada end
    there (see Table 46). So the next 7 rasis should be taken from the 9 rasis
    corresponding to the next pada, i.e. 3rd pada."
    """
    from hora.dasha.nakshatra.kalachakra import antardasas, wheel_position

    got = antardasas(4, 16, 7.0)
    second = [(wheel_position(4, 2) + step) % 24 for step in range(9)]
    third = [(wheel_position(4, 3) + step) % 24 for step in range(9)]

    assert [row["position"] for row in got][:2] == [16, 17]
    assert second[-2:] == [16, 17]                # Sc and Li end the 2nd pada
    assert all(row["position"] in third for row in got[2:])
    assert len(got[2:]) == 7                      # "the next 7 rasis"
    assert third[:7] == [row["position"] for row in got[2:]]


def test_example_97_le_dasa_is_divided_into_86_parts():
    """"By adding the dasa lengths of these 9 rasis (see Table 48), we get 86
    years. So we divide Le dasa of 5 years into 86 parts and give 5 parts to Le
    antardasa, 21 parts to Cn antardasa, 9 parts to Ge antardasa and so on."
    """
    from hora.dasha.nakshatra.kalachakra import antardasas

    got = antardasas(4, 19, 5.0)
    assert sum(row["share_years"] for row in got) == 86
    assert [row["share_years"] for row in got] == [5, 21, 9, 16, 7, 10, 4, 4, 10]

    assert got[0]["years"] == pytest.approx(5.0 * 5 / 86)
    assert got[1]["years"] == pytest.approx(5.0 * 21 / 86)
    assert got[2]["years"] == pytest.approx(5.0 * 9 / 86)
    assert sum(row["years"] for row in got) == pytest.approx(5.0)


def test_le_dasas_86_is_a_coincidence_not_a_paramayush():
    """Nine consecutive wheel positions do not always total a paramayush. Only
    the nine that begin a pada do.
    """
    from hora.dasha.nakshatra.kalachakra import (
        NINE_CONSECUTIVE_IS_NOT_ALWAYS_A_PARAMAYUSH,
        dasa_years,
        wheel,
    )

    totals = {
        sum(dasa_years(wheel(group)[(start + step) % 24]) for step in range(9))
        for group in ("savya", "apasavya") for start in range(24)
    }
    assert totals == {72, 83, 85, 86, 88, 97, 100}
    assert not totals <= {100, 85, 83, 86}
    assert "coincidence" not in NINE_CONSECUTIVE_IS_NOT_ALWAYS_A_PARAMAYUSH


def test_example_97_states_the_finding_the_wheel_is_the_whole_machinery():
    """The book says outright what rule (4) only implied, and names the one
    difference between the dasa walk and the antardasa walk.
    """
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_97_SAYS_THE_WHEEL_IS_THE_WHOLE_MACHINERY as SAID,
    )

    assert "all come from the two 24-rasi sequences" in SAID
    assert "the starting point is based on dasa rasi" in SAID


def test_footnote_66_puts_three_antardasas_before_birth():
    """"2.25 years of Sc dasa were over before birth. So some of these
    antardasas may be over before birth."

    Sc, Li and Vi are over by 2.24 years, so Le is running at birth -- with a
    hundredth of a year gone. The margin is a hundredth of a year, which is
    what makes it a check on the arithmetic rather than a restatement.
    """
    from hora.dasha.nakshatra.kalachakra import (
        FOOTNOTE_66,
        THE_FIRST_DASAS_ANTARDASAS_DIVIDE_ITS_WHOLE_LENGTH,
        antardasas,
        first_antardasa,
    )

    rows = antardasas(4, 16, 7.0)
    assert sum(row["years"] for row in rows[:3]) == pytest.approx(2.24)

    got = first_antardasa(rows, 2.25)
    assert got["over_before_birth"] == 3
    assert got["rasi"] == "Leo"
    assert got["elapsed_years"] == pytest.approx(0.01)
    assert got["balance_years"] == pytest.approx(0.34)

    assert "over before birth" in FOOTNOTE_66
    assert "whole dasa" in THE_FIRST_DASAS_ANTARDASAS_DIVIDE_ITS_WHOLE_LENGTH


def test_the_antardasas_divide_the_whole_dasa_not_the_balance():
    """Example 95 leaves 4.75 years of Sc dasa at birth. Dividing 4.75 among
    the nine would give a different Leo antardasa; footnote 66 rules it out by
    saying antardasas are already over.
    """
    from hora.dasha.nakshatra.kalachakra import antardasas

    whole = antardasas(4, 16, 7.0)
    balance = antardasas(4, 16, 4.75)
    assert sum(row["years"] for row in whole) == pytest.approx(7.0)
    assert sum(row["years"] for row in balance) == pytest.approx(4.75)
    assert whole[3]["years"] != pytest.approx(balance[3]["years"])


def test_first_antardasa_checks_its_inputs():
    from hora.dasha.nakshatra.kalachakra import (
        KalachakraError,
        antardasas,
        first_antardasa,
    )

    rows = antardasas(4, 16, 7.0)
    with pytest.raises(KalachakraError, match="cannot be empty"):
        first_antardasa((), 1.0)
    with pytest.raises(KalachakraError, match="cannot be negative"):
        first_antardasa(rows, -0.1)
    with pytest.raises(KalachakraError, match="exceeds"):
        first_antardasa(rows, 7.5)
    assert first_antardasa(rows, 7.0)["index"] == 8      # the last one


# ---------------------------------------------------------------------------
# §24.3.1 Interpretation — basics
# ---------------------------------------------------------------------------

def test_the_basics_read_across_the_vargas():
    """§24.3.1's six illustrations each name a different divisional chart, and
    that is the point of the section: a rasi's dasa gives the results of the
    house and planets it holds *in whichever varga is being read*.
    """
    from hora.dasha.nakshatra.kalachakra import (
        BASICS_EXAMPLES,
        HOUSE_AND_PLANETS_RULE,
        LORD_RULE,
        NATURAL_RESULTS_RULE,
    )

    assert "natural results of the rasi" in NATURAL_RESULTS_RULE
    assert "the house and planets in that rasi" in HOUSE_AND_PLANETS_RULE
    assert "results of its lord" in LORD_RULE

    vargas = [row["varga"] for row in BASICS_EXAMPLES]
    assert vargas == ["D7", "D6", "D24", "D10", "D10", "D7"]
    assert {row["rule"] for row in BASICS_EXAMPLES} == {
        "house", "house-and-planet", "lord"}

    lord = [row for row in BASICS_EXAMPLES if row["rule"] == "lord"]
    assert len(lord) == 1                        # "If Mars is in the 5th house
    assert lord[0]["gives"] == "children"        # in D-7, Aries dasa may give"


def test_the_eighth_from_al_here_has_no_table_32_pointer():
    """§23.3's "8th from AL" was Table 32's because Example 92 said so.
    §24.3.1's is unqualified, so it is the ordinary 8th. OI-140.
    """
    from hora.dasha.nakshatra.kalachakra import (
        BASICS_EXAMPLES,
        THE_EIGHTH_FROM_AL_HERE_IS_UNQUALIFIED,
    )
    from hora.dasha.rasi.shoola import THE_EIGHTH_FROM_AL_IS_TABLE_32S

    row = [r for r in BASICS_EXAMPLES if r["holds"] == "the 8th from AL"]
    assert len(row) == 1
    assert row[0]["varga"] == "D10"
    assert "Table 32" in THE_EIGHTH_FROM_AL_IS_TABLE_32S      # §23.3's
    assert "no reference to Table 32" in THE_EIGHTH_FROM_AL_HERE_IS_UNQUALIFIED


def test_sav_readings_are_held_per_varga_with_their_threshold():
    """"Usually dasas of rasis with 30 or more rekhas in D-10 SAV bring the
    best phases in one's career and dasas of rasis with 30 or more rekhas in
    D-24 SAV bring the best periods for learning."
    """
    from hora.dasha.nakshatra.kalachakra import (
        KEEP_SAV_OF_VARIOUS_VARGAS,
        SAV_STRONG_REKHAS,
        SAV_THRESHOLD_READINGS,
    )

    assert SAV_STRONG_REKHAS == 30
    assert [row["varga"] for row in SAV_THRESHOLD_READINGS] == ["D10", "D24"]
    assert all(row["rekhas"] == 30 for row in SAV_THRESHOLD_READINGS)
    assert all(row["hedge"] == "usually" for row in SAV_THRESHOLD_READINGS)
    assert "various divisional charts" in KEEP_SAV_OF_VARIOUS_VARGAS


# ---------------------------------------------------------------------------
# §24.3.2 Deha and Jeeva rasis
# ---------------------------------------------------------------------------

def test_deha_and_jeeva_come_from_the_dasas_not_the_table():
    """"In Example 95, the first dasa is Sc and the ninth dasa is Sg. Since
    Rohini is an apasavya nakshatra, Sc becomes jeeva rasi and Sg becomes deha
    rasi. In Example 96, the first dasa is Pi and the ninth dasa is Ar. Since
    Punarvasu is a savya nakshatra, Pi becomes deha rasi and Ar becomes jeeva
    rasi."
    """
    from hora.dasha.nakshatra.kalachakra import deha_and_jeeva_at_birth

    got = deha_and_jeeva_at_birth(4, 2, 7)               # Example 95
    assert (got["jeeva_rasi"], got["deha_rasi"]) == ("Scorpio", "Sagittarius")
    assert (A[got["first_dasa"]], A[got["ninth_dasa"]]) == ("Sc", "Sg")
    assert got["from_the_table"] is False

    got = deha_and_jeeva_at_birth(7, 4, 8)               # Example 96
    assert (got["deha_rasi"], got["jeeva_rasi"]) == ("Pisces", "Aries")
    assert (A[got["first_dasa"]], A[got["ninth_dasa"]]) == ("Pi", "Ar")
    assert got["from_the_table"] is False


def test_the_printed_tables_hold_only_for_birth_at_the_pada_start():
    """"However, these hold for one born at the beginning of the nakshatra
    pada." At position 0 the general rule and the tables agree, everywhere in
    all sixteen padas; at any other position they need not.
    """
    from hora.dasha.nakshatra.kalachakra import (
        PRINTED_SUB_GROUPS,
        TABLE_DEHA_AND_JEEVA_ASSUME_BIRTH_AT_THE_PADA_START,
        deha_and_jeeva,
        deha_and_jeeva_at_birth,
        pada_sequence,
    )

    assert "beginning of the nakshatra pada" in (
        TABLE_DEHA_AND_JEEVA_ASSUME_BIRTH_AT_THE_PADA_START)

    for group in ("savya", "apasavya"):
        for sub in (1, 2):
            nakshatra = PRINTED_SUB_GROUPS[f"{group}-{sub}"][0]
            for pada in (1, 2, 3, 4):
                table = deha_and_jeeva(group, pada_sequence(group, sub, pada))
                born = deha_and_jeeva_at_birth(nakshatra, pada, 0)
                assert born["from_the_table"] is True
                assert (born["deha"], born["jeeva"]) == (
                    table["deha"], table["jeeva"])

    # Example 95 is the counter-case: Rohini 2nd pada's table says Libra and
    # Virgo; born three-quarters of the way in, it is Sagittarius and Scorpio.
    table = deha_and_jeeva("apasavya", pada_sequence("apasavya", 1, 2))
    assert (table["deha_rasi"], table["jeeva_rasi"]) == ("Libra", "Virgo")
    born = deha_and_jeeva_at_birth(4, 2, 7)
    assert (born["deha_rasi"], born["jeeva_rasi"]) != (
        table["deha_rasi"], table["jeeva_rasi"])


def test_footnote_64s_nine_is_what_defines_deha_and_jeeva():
    """The nine-rasi set is not a printing habit: §24.3.2 takes deha and jeeva
    from its two ends, so the ninth dasa is the one that matters. Exercise 34's
    tenth changes nothing.
    """
    from hora.dasha.nakshatra.kalachakra import (
        deha_and_jeeva_at_birth,
        nine_from_birth,
    )

    nine = nine_from_birth(23, 4, 6)["dasas"]
    got = deha_and_jeeva_at_birth(23, 4, 6)
    assert got["first_dasa"] == nine[0]["sign"]
    assert got["ninth_dasa"] == nine[-1]["sign"]
    assert got["group"] == "apasavya"
    assert (A[got["jeeva"]], A[got["deha"]]) == ("Ge", "Ta")


@pytest.mark.parametrize(("rasi", "graha", "expected"), [
    ("jeeva", "JUPITER", "one may exhibit a positive spirit and be cheerful"),
    ("jeeva", "MERCURY", "one may exhibit a positive spirit and be cheerful"),
    ("jeeva", "VENUS", "one may exhibit a positive spirit and be cheerful"),
    ("jeeva", "MARS", "one may be without any enthusiasm"),
    ("jeeva", "SUN", "one may be without any enthusiasm"),
    ("jeeva", "SATURN", "one may be without any enthusiasm"),
    ("jeeva", "RAHU", "one may be without any enthusiasm"),
    ("deha", "MARS", "one may face accidents or death"),
    ("deha", "SATURN", "one may face accidents or death"),
])
def test_transit_readings(rasi, graha, expected):
    """§24.3.2's three filled cells, over every graha it names."""
    from hora.core.const import Graha
    from hora.dasha.nakshatra.kalachakra import transit_reading

    got = transit_reading(rasi, getattr(Graha, graha))
    assert got["reading"] == expected
    assert got["undecided"] is None


def test_benefics_in_the_deha_rasi_are_undecided_not_absent():
    """The fourth cell is empty. The general line about benefics and malefics
    would fill it; the section does not, and a blank is not a reading.
    """
    from hora.core.const import Graha
    from hora.dasha.nakshatra.kalachakra import (
        BENEFICS_IN_THE_DEHA_RASI_HAVE_NO_READING,
        transit_reading,
    )

    got = transit_reading("deha", Graha.JUPITER)
    assert got["kind"] == "benefic"
    assert got["reading"] is None
    assert got["undecided"] == BENEFICS_IN_THE_DEHA_RASI_HAVE_NO_READING


def test_ketu_and_the_moon_are_in_neither_list():
    """§24.3.2 names Rahu and not Ketu, and neither the Moon nor the lagna.
    Ketu is not added to the malefics here.
    """
    from hora.core.const import Graha
    from hora.dasha.nakshatra.kalachakra import (
        KETU_IS_NOT_IN_THE_TRANSIT_MALEFICS,
        TRANSIT_BENEFICS,
        TRANSIT_MALEFICS,
        transit_reading,
    )

    assert int(Graha.RAHU) in TRANSIT_MALEFICS
    assert int(Graha.KETU) not in TRANSIT_MALEFICS
    assert int(Graha.MOON) not in TRANSIT_BENEFICS + TRANSIT_MALEFICS
    assert "not added" in KETU_IS_NOT_IN_THE_TRANSIT_MALEFICS

    for graha in (Graha.KETU, Graha.MOON):
        got = transit_reading("jeeva", graha)
        assert got["kind"] is None
        assert "neither" in got["undecided"]


def test_transit_reading_checks_its_rasi():
    from hora.core.const import Graha
    from hora.dasha.nakshatra.kalachakra import KalachakraError, transit_reading

    with pytest.raises(KalachakraError, match="'deha' or 'jeeva'"):
        transit_reading("lagna", Graha.SUN)


# ---------------------------------------------------------------------------
# §24.3.3 Gatis
# ---------------------------------------------------------------------------

def test_the_gatis_fall_out_of_the_wheel():
    """§24.3.3 names the markati and mandooki rasis of both groups. None is
    transcribed: a trinal step is a lion's leap, a two-rasi step a frog's, and
    a single step against its half's direction a monkey's.
    """
    from hora.dasha.nakshatra.kalachakra import gati_rasis

    savya = gati_rasis("savya")
    assert [A[r] for r in savya["markati"]] == ["Le"]
    assert [A[r] for r in savya["mandooki"]] == ["Cn", "Ge"]

    apasavya = gati_rasis("apasavya")
    assert [A[r] for r in apasavya["markati"]] == ["Cn"]
    assert [A[r] for r in apasavya["mandooki"]] == ["Le", "Vi"]


def test_the_leaps_are_exactly_the_ones_24_3_3_describes():
    """Five irregular steps per wheel, and no others: two trinal leaps, one
    reversal and two jumps.
    """
    from hora.dasha.nakshatra.kalachakra import transitions

    seen = {}
    for group in ("savya", "apasavya"):
        rows = transitions(group)
        assert len(rows) == 24
        seen[group] = [(A[r["from"]], A[r["to"]], r["kind"], r["step"])
                       for r in rows if r["kind"] != "regular"]

    assert seen["savya"] == [
        ("Pi", "Sc", "simhaavalokana", -4),
        ("Vi", "Cn", "mandooki", -2),
        ("Cn", "Le", "markati", 1),
        ("Le", "Ge", "mandooki", -2),
        ("Sg", "Ar", "simhaavalokana", 4),
    ]
    assert seen["apasavya"] == [
        ("Ge", "Le", "mandooki", 2),
        ("Le", "Cn", "markati", -1),
        ("Cn", "Vi", "mandooki", 2),
        ("Sc", "Pi", "simhaavalokana", 4),
        ("Ar", "Sg", "simhaavalokana", -4),
    ]


def test_simhaavalokana_is_the_trinal_leap_both_ways():
    """"A trinal leap (from Sg to Ar or vice versa; from Pi to Sc or vice
    versa)." Each direction of each pair falls on a different wheel, which is
    what "or vice versa" is doing.
    """
    from hora.dasha.nakshatra.kalachakra import transitions

    pairs = {group: {(A[r["from"]], A[r["to"]]) for r in transitions(group)
                     if r["kind"] == "simhaavalokana"}
             for group in ("savya", "apasavya")}
    assert pairs["savya"] == {("Pi", "Sc"), ("Sg", "Ar")}
    assert pairs["apasavya"] == {("Sc", "Pi"), ("Ar", "Sg")}
    assert pairs["savya"] == {(b, a) for a, b in pairs["apasavya"]}


def test_the_gati_rasi_is_the_destination_of_the_leap():
    """"The rasis whose dasas come after an irregular leap go by special
    names." Vi-to-Cn names Cn, not Vi.
    """
    from hora.dasha.nakshatra.kalachakra import GATI_RULE, transitions

    assert "come after an irregular leap" in GATI_RULE
    jump = [r for r in transitions("savya")
            if (A[r["from"]], A[r["to"]]) == ("Vi", "Cn")]
    assert len(jump) == 1
    assert A[jump[0]["to"]] == "Cn"              # the named rasi


def test_the_quoted_runs_are_stretches_of_the_wheel():
    """§24.3.3 quotes "Sc, Li, Vi, Cn, Le, Ge, Ta, Ar" for savya and "Ar, Ta,
    Ge, Le, Cn, Vi, Li, Sc" for apasavya. Both are eight consecutive wheel
    positions -- the mirrored halves, where the leaps live.
    """
    from hora.dasha.nakshatra.kalachakra import wheel

    savya = [A[r] for r in wheel("savya")]
    assert savya[12:20] == ["Sc", "Li", "Vi", "Cn", "Le", "Ge", "Ta", "Ar"]

    apasavya = [A[r] for r in wheel("apasavya")]
    assert apasavya[4:12] == ["Ar", "Ta", "Ge", "Le", "Cn", "Vi", "Li", "Sc"]


def test_table_51_has_all_six_cells():
    from hora.dasha.nakshatra.kalachakra import (
        GATI_NAMES,
        MANDOOKI_SAVYA_SINGLES_OUT_THE_LE_TO_GE_LEAP,
        TABLE_51,
        gati_results,
    )

    assert set(TABLE_51) == {(kind, group) for kind in GATI_NAMES
                             for group in ("savya", "apasavya")}
    assert "Death of father or elders" in gati_results(
        "simhaavalokana", "apasavya")
    assert "Loss of wealth" in gati_results("markati", "savya")
    assert "Distress to wife" in gati_results("mandooki", "apasavya")

    # the one cell that separates its two leaps
    assert MANDOOKI_SAVYA_SINGLES_OUT_THE_LE_TO_GE_LEAP in gati_results(
        "mandooki", "savya")
    assert "Le-to-Ge" not in gati_results("mandooki", "apasavya")


def test_gati_names_and_footnote_67():
    from hora.dasha.nakshatra.kalachakra import (
        FOOTNOTE_67,
        GATI_DEFINITIONS,
        GATI_NAMES,
    )

    assert GATI_NAMES["simhaavalokana"] == "lion's leap"
    assert GATI_NAMES["markati"] == "monkey's leap"
    assert GATI_NAMES["mandooki"] == "frog's leap"
    assert "Temporary reversal" in GATI_DEFINITIONS["markati"]
    assert "doesn't really mean a lion" in FOOTNOTE_67


@pytest.mark.parametrize(("origin", "target", "prefer", "avoid"), [
    ("Vi", "Cn", ("east", "north"), ()),
    ("Le", "Ge", ("southwest",), ("east",)),
    ("Cn", "Le", ("west",), ("south",)),
    ("Pi", "Sc", (), ("north",)),
    ("Sg", "Cp", (), ("north",)),
    ("Sg", "Ar", (), ("all",)),
    ("Sg", "Sc", ("all",), ()),
    ("Le", "Cn", (), ("west",)),
])
def test_parasaras_seven_direction_rules(origin, target, prefer, avoid):
    """The seven bullets, which cover eight transitions -- bullet 4 names two.
    Two of the eight are normal movements, not leaps.
    """
    from hora.dasha.nakshatra.kalachakra import directions_for

    got = directions_for(R[origin], R[target])
    assert got["prefer"] == prefer
    assert got["avoid"] == avoid
    assert got["undecided"] is None
    assert got["occurs_in"]                      # each really is on a wheel


def test_the_two_normal_movements_are_not_leaps():
    """"In the leap from Pi to Sc and in the normal movement from Sg to Cp" --
    and "In the normal movement from Sg to Sc". Both are regular steps, so the
    direction rules are keyed by the step and not by the gati.
    """
    from hora.dasha.nakshatra.kalachakra import transitions

    kinds = {(A[r["from"]], A[r["to"]]): r["kind"]
             for group in ("savya", "apasavya") for r in transitions(group)}
    assert kinds[("Sg", "Cp")] == "regular"
    assert kinds[("Sg", "Sc")] == "regular"
    assert kinds[("Pi", "Sc")] == "simhaavalokana"


def test_four_apasavya_leaps_get_no_direction_rule():
    """Of the ten irregular steps across the two wheels, six are advised. The
    four that are not are all apasavya.
    """
    from hora.dasha.nakshatra.kalachakra import (
        PARASARA_LEAVES_FOUR_APASAVYA_LEAPS_UNADVISED,
        directions_for,
        transitions,
    )

    unadvised = {
        group: [(A[r["from"]], A[r["to"]]) for r in transitions(group)
                if r["kind"] != "regular"
                and directions_for(r["from"], r["to"])["undecided"] is not None]
        for group in ("savya", "apasavya")
    }
    assert unadvised["savya"] == []
    assert unadvised["apasavya"] == [
        ("Ge", "Le"), ("Cn", "Vi"), ("Sc", "Pi"), ("Ar", "Sg")]
    assert "all apasavya" in PARASARA_LEAVES_FOUR_APASAVYA_LEAPS_UNADVISED


def test_directions_for_reports_a_transition_that_happens_on_neither_wheel():
    """An opposition step occurs nowhere on either wheel, and that is a
    different silence from a leap Parasara simply did not advise on.
    """
    from hora.dasha.nakshatra.kalachakra import directions_for

    got = directions_for(R["Ar"], R["Li"])
    assert got["occurs_in"] == ()
    assert got["undecided"] == "this transition occurs on neither wheel"

    got = directions_for(R["Ge"], R["Le"])
    assert got["occurs_in"] == ("apasavya",)
    assert "no direction rule" in got["undecided"]


def test_mandooki_is_the_third_eleventh_jump_19_4_pointed_at():
    """§19.4 called mandooki gati "the 3rd/11th jump" and sent the reader to
    "Parasara's discussion on Kalachakra dasa" for it. §24.3.3 is that
    discussion, and every frog's leap on either wheel is a 3rd or an 11th.
    """
    from hora.dasha.nakshatra.kalachakra import (
        MANDOOKI_IS_19_4S_THIRD_ELEVENTH_JUMP,
        transitions,
    )
    from hora.dasha.rasi.kendradi import GATI_NAMES as KENDRADI_GATIS

    named = [row for row in KENDRADI_GATIS if row["name"] == "mandooki gati"]
    assert named[0]["movement"] == "the 3rd/11th jump"
    assert named[0]["built"] is False             # the dasa, not the gati

    def ordinal(origin, target):
        return (target - origin) % 12 + 1

    savya = [ordinal(r["from"], r["to"]) for r in transitions("savya")
             if r["kind"] == "mandooki"]
    apasavya = [ordinal(r["from"], r["to"]) for r in transitions("apasavya")
                if r["kind"] == "mandooki"]
    assert savya == [11, 11]
    assert apasavya == [3, 3]
    assert "11ths" in MANDOOKI_IS_19_4S_THIRD_ELEVENTH_JUMP


def test_no_other_gati_is_a_third_or_an_eleventh():
    """The 3rd/11th picks out the frog's leaps alone: the lion's are trines and
    the monkey's a single sign, so §19.4's phrase is unambiguous.
    """
    from hora.dasha.nakshatra.kalachakra import transitions

    for group in ("savya", "apasavya"):
        for row in transitions(group):
            ordinal = (row["to"] - row["from"]) % 12 + 1
            if row["kind"] == "mandooki":
                assert ordinal in (3, 11)
            else:
                assert ordinal not in (3, 11)


# ---------------------------------------------------------------------------
# Example 98 — Chart 46, a male who married in Dec 1994
# ---------------------------------------------------------------------------

def _chart_46():
    """Chart 46's rasi and navamsa positions, from the printed longitudes."""
    from hora.charts.book import longitudes
    from hora.charts.vargas import varga
    from hora.core.const import Graha

    printed = longitudes(46)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    return {
        "printed": printed,
        "rasi_lagna": int(printed["Asc"] // 30),
        "rasi": {int(g): int(printed[n] // 30) for n, g in named.items()},
        "d9_lagna": varga(printed["Asc"], "D9").sign,
        "d9": {int(g): varga(printed[n], "D9").sign for n, g in named.items()},
    }


def test_chart_46_recomputes_within_an_arcminute():
    """The fourth chart born at 81 E 12, 16 N 15, and the same native as the
    third: every body inside one arcminute under the mean node.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(46)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 46", **record["place"]),
        Settings(node_type=NodeType.MEAN))

    printed = longitudes(46)
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"


def test_chart_46_is_chart_44s_native():
    """Same birth data, same twelve longitudes, same eight chara karakas. One
    prints the rasi chart, the other the navamsa.
    """
    from hora.charts.book import chart
    from hora.dasha.nakshatra.kalachakra import CHART_46_IS_CHART_44S_NATIVE

    forty_four, forty_six = chart(44), chart(46)
    assert forty_four["birth_data"] == forty_six["birth_data"]
    assert forty_four["place"] == forty_six["place"]
    assert forty_four["longitudes"] == forty_six["longitudes"]
    assert forty_four["chara_karakas"] == forty_six["chara_karakas"]

    assert "drawn" in forty_four and "divisional" in forty_six
    assert "D9" in forty_six["divisional"]
    assert "one native" in CHART_46_IS_CHART_44S_NATIVE


def test_chart_46s_drawn_navamsa_reproduces_from_the_longitudes():
    """All twelve placements in the printed navamsa, from the rasi longitudes
    below the diagram and the D-9 rule alone.
    """
    from hora.charts.book import chart
    from hora.charts.vargas import varga
    from hora.core.const import RASI_ABBR

    drawn = dict(chart(46)["divisional"]["D9"])
    printed = chart(46)["longitudes"]
    arudha = drawn.pop("AL")                     # not a longitude; below

    assert len(drawn) == 12
    for name, abbr in drawn.items():
        got = str(RASI_ABBR[varga(_chart_46()["printed"][name], "D9").sign])
        assert got == abbr, f"{name}: printed {abbr}, computed {got}"
    assert set(drawn) == set(printed)
    assert arudha == "Sg"


def test_the_navamsa_arudha_lagna_needs_the_same_sign_exception():
    """AL in the drawn navamsa is Sagittarius, and it gets there only through
    §9.2's exception: Pisces' lord Jupiter is the 7th from it, the 7th from
    Jupiter is Pisces again, and an arudha in its own house moves to the 10th.
    """
    from hora.charts.arudha import arudha_pada
    from hora.core.const import RASI_NAMES

    chart = _chart_46()
    al = arudha_pada(1, chart["d9_lagna"], chart["d9"])
    assert str(RASI_NAMES[al.sign]) == "Sagittarius"
    assert str(RASI_NAMES[chart["d9_lagna"]]) == "Pisces"


def test_example_98s_first_two_reasons_are_the_navamsa_lagna_and_its_lord():
    """"It has lagna in navamsa and its lord Jupiter is in the 7th house!
    Naturally Pi and Vi are the front-runners for giving marriage."
    """
    from hora.core.const import RASI_LORD, RASI_NAMES, Graha
    from hora.dasha.nakshatra.kalachakra import EXAMPLE_98_REASONS

    chart = _chart_46()
    lagna = chart["d9_lagna"]
    assert str(RASI_NAMES[lagna]) == "Pisces"

    lord = int(RASI_LORD[lagna])
    assert lord == int(Graha.JUPITER)
    seventh = (lagna + 6) % 12
    assert chart["d9"][lord] == seventh
    assert str(RASI_NAMES[seventh]) == "Virgo"

    front_runners = [row["rasi"] for row in EXAMPLE_98_REASONS
                     if row["gives"] == "marriage"]
    assert front_runners == ["Pisces", "Virgo"]


def test_pisces_is_the_second_from_venus_in_the_navamsa():
    """"Pi is the 2nd from Venus. Venus symbolizes domestic happiness and
    marital bliss. The 2nd from him in navamsa can show the sense of family
    happiness."
    """
    from hora.core.const import RASI_NAMES, Graha
    from hora.dasha.nakshatra.kalachakra import (
        SECOND_FROM_VENUS_RULE,
        VENUS_SYMBOLIZES,
        second_from_venus,
    )

    chart = _chart_46()
    venus = chart["d9"][int(Graha.VENUS)]
    assert str(RASI_NAMES[venus]) == "Aquarius"
    assert str(RASI_NAMES[second_from_venus(venus)]) == "Pisces"

    assert VENUS_SYMBOLIZES == "domestic happiness and marital bliss"
    assert "new person coming into the family" in SECOND_FROM_VENUS_RULE
    assert second_from_venus(11) == 0            # it wraps


def test_venus_is_exalted_in_pisces_and_owns_the_darapada():
    """"In addition, one may note that exalted Venus occupies Pi in rasi chart
    and he owns darapada, which is in Libra."  -- both at rasi level, and the
    darapada needs the arudha of the 7th, not the 7th house.
    """
    from hora.charts.arudha import arudha_pada
    from hora.core.const import EXALTATION_RASI, RASI_LORD, RASI_NAMES, Graha

    chart = _chart_46()
    venus = int(Graha.VENUS)
    assert str(RASI_NAMES[chart["rasi"][venus]]) == "Pisces"
    assert int(EXALTATION_RASI[venus]) == chart["rasi"][venus]

    darapada = arudha_pada(7, chart["rasi_lagna"], chart["rasi"])
    assert str(RASI_NAMES[darapada.sign]) == "Libra"
    assert int(RASI_LORD[darapada.sign]) == venus

    seventh = (chart["rasi_lagna"] + 6) % 12     # Sagittarius, not the arudha
    assert str(RASI_NAMES[seventh]) == "Sagittarius"


def test_example_98s_kalachakra_dasas():
    """"Readers can verify that the native had about 5 years of Sc dasa left at
    birth and the next dasas are Sg, Cp, Aq, Pi, Sc, Li, Vi, Cn."

    Moon at 9 Li 29 is Swaati's 1st pada, savya-1, paramayush 100. The eight
    named dasas plus the one running make nine -- footnote 64's set exactly.
    """
    from hora.charts.book import longitudes
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        first_dasa,
        nine_from_birth,
        pada_of,
        pada_sequence,
        paramayush,
        sub_group_of,
    )

    moon = pada_of(longitudes(46)["Moon"])
    assert (moon["nakshatra"], moon["group"], moon["pada"]) == (
        15, "savya", 1)                          # Swaati
    assert sub_group_of(15) == 1

    nine = pada_sequence("savya", 1, 1)
    assert [A[rasi] for rasi in nine] == [
        "Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg"]
    assert paramayush(nine) == 100

    birth = first_dasa(nine, moon["elapsed_fraction"])
    assert birth["rasi"] == "Scorpio"
    assert birth["balance_years"] == pytest.approx(5.5)   # "about 5 years"
    assert birth["position"] == 7

    following = dasa_order(15, 1, 8, skip=birth["position"] + 1)
    assert [A[row["sign"]] for row in following] == [
        "Sg", "Cp", "Aq", "Pi", "Sc", "Li", "Vi", "Cn"]

    displayed = nine_from_birth(15, 1, birth["position"])
    assert (displayed["from_this_pada"], displayed["from_next_pada"]) == (2, 7)
    assert len(displayed["dasas"]) == 9          # the eight, plus Scorpio


def test_the_wedding_falls_in_pi_pi_and_the_affair_in_aquarius():
    """"At the time of wedding, the native was running Pi-Pi." Aq dasa runs
    from age 19.5 to 23.5 and Pi from 23.5, and Pi's own antardasa is the first
    and a full year long.
    """
    from hora.dasha.nakshatra.kalachakra import antardasas, dasa_order

    ages, age = {}, 5.5                          # Sc's balance at birth
    for row in dasa_order(15, 1, 5, skip=8):     # Sg, Cp, Aq, Pi, Sc
        ages[A[row["sign"]]] = (age, age + row["years"])
        age += row["years"]
    assert ages["Aq"] == (19.5, 23.5)
    assert ages["Pi"] == (23.5, 33.5)

    # born May 1971, so Aq spans late 1990 to 1994 and Pi opens in 1994
    for year_days in (360.0, 365.25):
        assert 1990 <= 1971 + (5 + 22 / 60) / 12 + 19.5 * year_days / 365.25
        assert 1971 + 23.5 * year_days / 365.25 < 1995

    pisces = antardasas(15, 11, 10.0)            # Pi at wheel position 11
    assert A[pisces[0]["sign"]] == "Pi"          # antardasas start from it
    assert pisces[0]["years"] == pytest.approx(1.0)
    assert sum(row["share_years"] for row in pisces) == 100


def test_aquarius_reached_him_at_the_navamsa_level_only():
    """Venus is in Pisces in the rasi chart and Aquarius in the navamsa, so
    Aquarius' dasa touched the inner self and Pisces' the physical.
    """
    from hora.core.const import RASI_NAMES, Graha
    from hora.dasha.nakshatra.kalachakra import (
        AQUARIUS_GAVE_ROMANCE_AND_PISCES_GAVE_MARRIAGE,
        RASI_IS_PHYSICAL_NAVAMSA_IS_INNER,
    )

    chart = _chart_46()
    venus = int(Graha.VENUS)
    assert str(RASI_NAMES[chart["rasi"][venus]]) == "Pisces"
    assert str(RASI_NAMES[chart["d9"][venus]]) == "Aquarius"

    assert "physical level" in RASI_IS_PHYSICAL_NAVAMSA_IS_INNER
    assert "inner self" in RASI_IS_PHYSICAL_NAVAMSA_IS_INNER
    assert "1990-1994" in AQUARIUS_GAVE_ROMANCE_AND_PISCES_GAVE_MARRIAGE


def test_example_98_dates_nothing_finely_enough_to_settle_oi_115():
    """Both year lengths put Aq in 1990-1994 and the wedding in Pi-Pi."""
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_98_DOES_NOT_SEPARATE_THE_YEAR_LENGTHS,
    )

    for year_days in (360.0, 365.25):
        aq_start = 19.5 * year_days
        aq_end = 23.5 * year_days
        pi_pi_end = aq_end + 1.0 * year_days
        wedding = (1994 + 11.5 / 12 - 1971 - (5 + 9 / 31) / 12) * 365.25
        assert aq_start < wedding                # Aq had opened
        assert aq_end < wedding < pi_pi_end      # and Pi-Pi was running
    assert "both year lengths" in EXAMPLE_98_DOES_NOT_SEPARATE_THE_YEAR_LENGTHS


# ---------------------------------------------------------------------------
# Example 99 — Chart 47, an astrologer's D-24
# ---------------------------------------------------------------------------

D24_REFERENCES = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars",
                  "Merc": "Mercury", "Jup": "Jupiter", "Ven": "Venus",
                  "Sat": "Saturn", "Asc": "Lagna"}


def _chart_47_d24():
    """Chart 47's D-24 signs, from the printed rasi longitudes."""
    from hora.charts.book import longitudes
    from hora.charts.vargas import varga
    from hora.core.const import Graha

    printed = longitudes(47)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    return {
        "printed": printed,
        "lagna": varga(printed["Asc"], "D24").sign,
        "signs": {int(g): varga(printed[n], "D24").sign
                  for n, g in named.items()},
        "references": {ref: varga(printed[name], "D24").sign
                       for name, ref in D24_REFERENCES.items()},
    }


def test_chart_47_recomputes_and_is_the_third_printing_of_one_native():
    """Charts 27, 33 and 47 share a birth line, twelve longitudes and eight
    chara karakas. The rasi chart has never been drawn for him.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import CHART_47_IS_THE_THIRD_PRINTING

    records = {n: chart(n) for n in (27, 33, 47)}
    assert (records[27]["birth_data"] == records[33]["birth_data"]
            == records[47]["birth_data"])
    assert (records[27]["longitudes"] == records[33]["longitudes"]
            == records[47]["longitudes"])
    assert (records[27]["chara_karakas"] == records[33]["chara_karakas"]
            == records[47]["chara_karakas"])
    assert [list(records[n]["divisional"]) for n in (27, 33, 47)] == [
        ["D4"], ["D16"], ["D24"]]
    assert all(records[n].get("drawn") is None for n in (27, 33, 47))

    computed = compute_chart(
        from_local(**records[47]["birth_data"]),
        Place(name="Chart 47", **records[47]["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(47)
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"

    assert "three" in CHART_47_IS_THE_THIRD_PRINTING or "27, 33 and 47" in (
        CHART_47_IS_THE_THIRD_PRINTING)


def test_chart_47s_drawn_d24_reproduces_from_the_longitudes():
    """All twelve placements in the printed D-24."""
    from hora.charts.book import chart
    from hora.charts.vargas import varga
    from hora.core.const import RASI_ABBR

    drawn = dict(chart(47)["divisional"]["D24"])
    arudha = drawn.pop("AL")
    printed = chart(47)["longitudes"]

    assert len(drawn) == 12
    assert set(drawn) == set(printed)
    for name, abbr in drawn.items():
        got = str(RASI_ABBR[varga(_chart_47_d24()["printed"][name],
                                  "D24").sign])
        assert got == abbr, f"{name}: printed {abbr}, computed {got}"
    assert arudha == "Aq"


def test_example_99s_first_three_reasons():
    """"Gemini contains lagna in D-24... Its lord Mercury is in the 5th house
    of scholarship from lagna... Mercury and Venus are in trines from Ge."
    """
    from hora.core.const import RASI_LORD, RASI_NAMES, Graha
    from hora.dasha.nakshatra.kalachakra import EXAMPLE_99_REASONS

    chart = _chart_47_d24()
    lagna = chart["lagna"]
    assert str(RASI_NAMES[lagna]) == "Gemini"

    mercury = int(Graha.MERCURY)
    assert int(RASI_LORD[lagna]) == mercury
    fifth = (lagna + 4) % 12
    assert chart["signs"][mercury] == fifth
    assert str(RASI_NAMES[fifth]) == "Libra"

    trines = {(lagna + step) % 12 for step in (0, 4, 8)}
    assert chart["signs"][mercury] in trines
    assert chart["signs"][int(Graha.VENUS)] in trines
    assert str(RASI_NAMES[chart["signs"][int(Graha.VENUS)]]) == "Aquarius"

    assert {row["rasi"] for row in EXAMPLE_99_REASONS} == {"Gemini"}
    assert [row["rule"] for row in EXAMPLE_99_REASONS] == [
        "house", "lord", "trines", "sav", "arudha"]


def test_the_d24_sav_reproduces_the_three_strongest_signs():
    """"The strongest houses in this D-24 SAV are Le (36 rekhas), Ge (34
    rekhas) and Pi (33 rekhas)."  The only worked SAV of a divisional chart in
    the book, and the whole of it comes out of §12.4's tables.
    """
    from hora.charts.ashtakavarga import sarvashtakavarga
    from hora.charts.book import chart
    from hora.core.const import RASI_ABBR

    sav = sarvashtakavarga(_chart_47_d24()["references"])
    ranked = sorted(sav["signs"], key=lambda row: -row["rekhas"])
    assert [(str(RASI_ABBR[row["sign"]]), row["rekhas"])
            for row in ranked[:3]] == [("Le", 36), ("Ge", 34), ("Pi", 33)]
    assert ranked[3]["rekhas"] < 30              # nothing else is strong
    assert sav["total"] == sav["expected_total"] == 337

    printed = chart(47)["sav_strongest"]["D24"]
    assert printed == {"Le": 36, "Ge": 34, "Pi": 33}


def test_the_three_strongest_are_the_2nd_5th_and_7th_from_al():
    """"They are the 7th, 5th and 2nd houses from AL. As these are the houses
    conducive to recognition and awards..."  A rule §24.3.1 did not give.
    """
    from hora.charts.arudha import arudha_pada
    from hora.core.const import RASI_ABBR
    from hora.dasha.nakshatra.kalachakra import (
        TWO_FIVE_AND_SEVEN_FROM_AL_ARE_RECOGNITION,
    )

    chart = _chart_47_d24()
    al = arudha_pada(1, chart["lagna"], chart["signs"]).sign
    assert str(RASI_ABBR[al]) == "Aq"

    houses = {house: str(RASI_ABBR[(al + house - 1) % 12])
              for house in (2, 5, 7)}
    assert houses == {2: "Pi", 5: "Ge", 7: "Le"}
    assert "recognition and awards" in TWO_FIVE_AND_SEVEN_FROM_AL_ARE_RECOGNITION


def test_gemini_is_both_the_5th_from_al_and_a5():
    """"With Ge being the 5th house from AL and also A5, this dasa can bring
    some reputation for his knowledge."  Two different counts landing on one
    sign, which is why the example bothers to say both.
    """
    from hora.charts.arudha import arudha_pada
    from hora.core.const import RASI_ABBR

    chart = _chart_47_d24()
    al = arudha_pada(1, chart["lagna"], chart["signs"]).sign
    a5 = arudha_pada(5, chart["lagna"], chart["signs"]).sign

    assert str(RASI_ABBR[(al + 4) % 12]) == "Ge"     # the 5th from AL
    assert str(RASI_ABBR[a5]) == "Ge"                # and A5 itself
    assert a5 != al


def test_example_99s_kalachakra_dasas():
    """"About 3 years and 2 months of Sg dasa was left at birth and Ar, Ta, Ge,
    Cn etc dasas run after it."  Moon at 28 Aq 35 is Poorvabhadrapada's 3rd
    pada, savya-1, paramayush 83.
    """
    from hora.charts.book import longitudes
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        first_dasa,
        pada_of,
        pada_sequence,
        paramayush,
        sub_group_of,
    )

    moon = pada_of(longitudes(47)["Moon"])
    assert (moon["nakshatra"], moon["group"], moon["pada"]) == (
        25, "savya", 3)                          # Poorvabhadrapada
    assert sub_group_of(25) == 1
    assert moon["elapsed_fraction"] == pytest.approx(115.0 / 200.0)

    nine = pada_sequence("savya", 1, 3)
    assert [A[rasi] for rasi in nine] == [
        "Ta", "Ar", "Pi", "Aq", "Cp", "Sg", "Ar", "Ta", "Ge"]
    assert paramayush(nine) == 83

    birth = first_dasa(nine, moon["elapsed_fraction"])
    assert birth["rasi"] == "Sagittarius"
    assert birth["position"] == 5

    following = dasa_order(25, 3, 4, skip=birth["position"] + 1)
    assert [A[row["sign"]] for row in following] == ["Ar", "Ta", "Ge", "Cn"]
    assert [row["position"] for row in following] == [0, 1, 2, 3]
    assert following[2]["years"] == 9            # "Gemini dasa of 9 years"


def test_gemini_dasa_starts_in_1996_under_either_year_length():
    """"One may find that Gemini dasa of 9 years started in 1996."  Born April
    1970, so Gemini opens at about 26.24 years of age.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        first_dasa,
        pada_of,
        pada_sequence,
    )

    record = chart(47)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 47", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    moon = computed.positions[int(Graha.MOON)].longitude

    nine = pada_sequence("savya", 1, 3)
    birth = first_dasa(nine, pada_of(moon)["elapsed_fraction"])
    age = birth["balance_years"] + 7 + 16        # Sg's balance, then Ar and Ta

    for year_days in (360.0, 365.25):
        year = 1970 + (4 - 1 + 4 / 30) / 12 + age * year_days / 365.25
        assert 1996 <= year < 1997

    assert 26.0 < age < 26.5
    # and the printed Moon puts it in 1996 too, being only 0.09' away
    printed = first_dasa(nine, pada_of(longitudes(47)["Moon"])["elapsed_fraction"])
    assert abs(printed["balance_years"] - birth["balance_years"]) < 0.05


def test_the_birth_balance_needs_the_unrounded_moon():
    """The book's "3 years and 2 months" comes from the ephemeris Moon. The
    printed 28 Aq 35 gives 3 years 3.3 months -- a difference of 0.09' of
    longitude, because one arcminute is worth paramayush/200 years.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        THE_BIRTH_BALANCE_NEEDS_THE_UNROUNDED_MOON,
        balance_per_arcminute,
        first_dasa,
        pada_of,
        pada_sequence,
    )

    nine = pada_sequence("savya", 1, 3)
    assert balance_per_arcminute(nine) == pytest.approx(83 / 200)
    assert 4.9 < balance_per_arcminute(nine) * 12 < 5.0      # months

    record = chart(47)
    moon = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 47", **record["place"]),
        Settings(node_type=NodeType.MEAN)
    ).positions[int(Graha.MOON)].longitude

    def months(longitude):
        balance = first_dasa(nine, pada_of(longitude)["elapsed_fraction"])
        return balance["balance_years"] % 1 * 12

    assert int(months(longitudes(47)["Moon"])) == 3          # printed: 3.3
    assert int(months(moon)) == 2                            # computed: 2.9
    assert abs(moon - longitudes(47)["Moon"]) * 60 < 0.1     # 0.09 arcminutes

    assert "paramayush/200" in THE_BIRTH_BALANCE_NEEDS_THE_UNROUNDED_MOON


def test_example_98s_balance_also_comes_from_the_computed_moon():
    """"About 5 years of Sc dasa left at birth."  The printed Moon gives 5.50
    years and the computed one 5.20, and 5.20 is what "about 5" describes.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        balance_per_arcminute,
        first_dasa,
        pada_of,
        pada_sequence,
    )

    nine = pada_sequence("savya", 1, 1)
    assert balance_per_arcminute(nine) == pytest.approx(0.5)   # 6 months

    record = chart(46)
    moon = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 46", **record["place"]),
        Settings(node_type=NodeType.MEAN)
    ).positions[int(Graha.MOON)].longitude

    printed = first_dasa(nine, pada_of(longitudes(46)["Moon"])["elapsed_fraction"])
    exact = first_dasa(nine, pada_of(moon)["elapsed_fraction"])
    assert printed["balance_years"] == pytest.approx(5.5)
    assert exact["balance_years"] == pytest.approx(5.20, abs=0.01)
    assert printed["rasi"] == exact["rasi"] == "Scorpio"


def test_example_99_drops_24_3_1s_hedge_on_the_sav_threshold():
    """§24.3.1 said "usually dasas of rasis with 30 or more rekhas"; Example 99
    says "any rasi 30 or more rekhas". The threshold is the same.
    """
    from hora.dasha.nakshatra.kalachakra import (
        SAV_STRONG_REKHAS,
        SAV_THRESHOLD_READINGS,
        SAV_THRESHOLD_RESTATED_WITHOUT_THE_HEDGE,
    )

    assert SAV_STRONG_REKHAS == 30
    assert "Any rasi" in SAV_THRESHOLD_RESTATED_WITHOUT_THE_HEDGE
    assert "usually" not in SAV_THRESHOLD_RESTATED_WITHOUT_THE_HEDGE.lower()
    assert all(row["hedge"] == "usually" for row in SAV_THRESHOLD_READINGS)


# ---------------------------------------------------------------------------
# Example 100 — Chart 48, a father's death
# ---------------------------------------------------------------------------

def _chart_48():
    """Chart 48's D-12, from the printed rasi longitudes."""
    from hora.charts.book import longitudes
    from hora.charts.vargas import varga
    from hora.core.const import Graha

    printed = longitudes(48)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    return {
        "printed": printed,
        "lagna": varga(printed["Asc"], "D12").sign,
        "signs": {int(g): varga(printed[n], "D12").sign
                  for n, g in named.items()},
    }


def _chart_48_moon():
    """The ephemeris Moon, which is what the example's balance needs."""
    from hora.charts.book import chart
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(48)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 48", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    return computed.positions[int(Graha.MOON)].longitude


def test_chart_48_recomputes_and_is_a_new_native():
    """The first chart in the register at 80 E 55, 16 N 05, and the first born
    in 1933.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes, numbers
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(48)
    others = [chart(n)["place"] for n in numbers() if n != 48
              and "place" in chart(n)]
    assert record["place"] not in others

    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 48", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(48)
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"


def test_chart_48s_drawn_d12_reproduces_from_the_longitudes():
    """All twelve placements, plus an AL that needs the same-sign exception:
    Virgo's lord Mercury is the 7th from it, the 7th from Mercury is Virgo
    again, so the arudha moves to the 10th -- Gemini.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import chart
    from hora.charts.vargas import varga
    from hora.core.const import RASI_ABBR

    drawn = dict(chart(48)["divisional"]["D12"])
    arudha = drawn.pop("AL")
    assert len(drawn) == 12
    assert set(drawn) == set(chart(48)["longitudes"])

    positions = _chart_48()
    for name, abbr in drawn.items():
        got = str(RASI_ABBR[varga(positions["printed"][name], "D12").sign])
        assert got == abbr, f"{name}: printed {abbr}, computed {got}"

    al = arudha_pada(1, positions["lagna"], positions["signs"]).sign
    assert str(RASI_ABBR[al]) == arudha == "Ge"
    assert al != positions["lagna"]


def test_example_100s_chain_from_the_ninth_house_to_the_eighth_from_a9():
    """"Lagna in D-12 is in Vi. The 9th house is in Ta... Here A9 is in Cp.
    Taking Cp as lagna, we see that Cn is the 7th house of death and its lord
    Moon is exalted... he afflicts Sun, who owns the 8th house from Cp."
    """
    from hora.charts.arudha import arudha_pada
    from hora.core.const import EXALTATION_RASI, RASI_LORD, RASI_NAMES, Graha
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_100_CHAIN,
        THE_HOUSE_IS_THE_CONCEPT_AND_THE_ARUDHA_IS_THE_BODY,
    )

    chart = _chart_48()
    lagna = chart["lagna"]
    assert str(RASI_NAMES[lagna]) == "Virgo"
    assert str(RASI_NAMES[(lagna + 8) % 12]) == "Taurus"      # the 9th house

    a9 = arudha_pada(9, lagna, chart["signs"]).sign
    assert str(RASI_NAMES[a9]) == "Capricorn"

    seventh = (a9 + 6) % 12
    assert str(RASI_NAMES[seventh]) == "Cancer"
    moon = int(Graha.MOON)
    assert int(RASI_LORD[seventh]) == moon
    assert chart["signs"][moon] == int(EXALTATION_RASI[moon])   # Taurus

    eighth = (a9 + 7) % 12
    assert str(RASI_NAMES[eighth]) == "Leo"
    assert int(RASI_LORD[eighth]) == int(Graha.SUN)
    assert chart["signs"][int(Graha.SUN)] == chart["signs"][moon]

    assert "A9 represents it" in THE_HOUSE_IS_THE_CONCEPT_AND_THE_ARUDHA_IS_THE_BODY
    assert [row["sign"] for row in EXAMPLE_100_CHAIN] == [
        "Capricorn", "Cancer", "Taurus", "Leo"]


def test_the_moon_that_afflicts_is_a_waning_moon():
    """"He afflicts Sun" is undefined here, and the Moon is no general malefic.
    This one is: the birth falls in Krishna paksha, which §3.2.1 makes a
    natural malefic. The book does not say so; recorded as inference.
    """
    from hora.charts.benefic import moon_nature
    from hora.charts.book import longitudes
    from hora.dasha.nakshatra.kalachakra import AFFLICTS_IS_NOT_DEFINED_HERE
    from hora.panchanga.core import paksha_at

    printed = longitudes(48)
    paksha = paksha_at(printed["Sun"], printed["Moon"])
    assert paksha == 1                            # Krishna, waning
    assert moon_nature(paksha) == "malefic"
    assert moon_nature(0) == "benefic"            # a waxing Moon would not be
    assert "does not say what afflicting is" in AFFLICTS_IS_NOT_DEFINED_HERE


def test_example_100_is_the_first_reading_to_use_a_gati():
    """"Cn dasa here comes after Vi and involves mandooki gati (frog's leap)...
    mandooki gati in savya nakshatras can bring distress to father."

    It confirms the named rasi is the leap's destination: the step is Vi to Cn
    and the dasa called mandooki is Cancer's, not Virgo's.
    """
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_100_USES_THE_FROGS_LEAP,
        gati_rasis,
        gati_results,
        transitions,
    )

    leap = [row for row in transitions("savya")
            if (A[row["from"]], A[row["to"]]) == ("Vi", "Cn")]
    assert len(leap) == 1
    assert leap[0]["kind"] == "mandooki"
    assert A[leap[0]["to"]] == "Cn"
    assert leap[0]["to"] in gati_rasis("savya")["mandooki"]

    assert "father" in gati_results("mandooki", "savya")
    assert "distress to father" in EXAMPLE_100_USES_THE_FROGS_LEAP


def test_example_100s_kalachakra_dasas():
    """"About 1 year and 8 months of Pi dasa was remaining at birth and the
    dasas coming after it are Sc, Li, Vi, Cn, Le, Ge, Ta and Ar."

    Moon at 3 Ar 58 is Aswini's 2nd pada, savya-1, paramayush 85 -- and the
    balance needs the ephemeris Moon: the printed one gives 1y 10.2m.
    """
    from hora.charts.book import longitudes
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        first_dasa,
        nine_from_birth,
        pada_of,
        pada_sequence,
        paramayush,
        sub_group_of,
    )

    moon = pada_of(_chart_48_moon())
    assert (moon["nakshatra"], moon["group"], moon["pada"]) == (1, "savya", 2)
    assert sub_group_of(1) == 1

    nine = pada_sequence("savya", 1, 2)
    assert [A[rasi] for rasi in nine] == [
        "Cp", "Aq", "Pi", "Sc", "Li", "Vi", "Cn", "Le", "Ge"]
    assert paramayush(nine) == 85

    birth = first_dasa(nine, moon["elapsed_fraction"])
    assert birth["rasi"] == "Pisces"
    assert birth["position"] == 2
    assert int(birth["balance_years"]) == 1
    assert round(birth["balance_years"] % 1 * 12) == 8        # 1y 8m

    printed = first_dasa(
        nine, pada_of(longitudes(48)["Moon"])["elapsed_fraction"])
    assert round(printed["balance_years"] % 1 * 12, 1) == 10.2

    following = dasa_order(1, 2, 8, skip=birth["position"] + 1)
    assert [A[row["sign"]] for row in following] == [
        "Sc", "Li", "Vi", "Cn", "Le", "Ge", "Ta", "Ar"]
    assert len(nine_from_birth(1, 2, birth["position"])["dasas"]) == 9


def test_cancer_dasa_opens_in_september_1966_only_under_savana():
    """"Cn dasa started in September 1966."  Savana gives 1966-09-20 and a
    solar year gives 1967-03-15. The first dated Kalachakra event that
    separates OI-115's two readings -- evidence, not a change of default.
    """
    import swisseph as swe

    from hora.charts.book import chart, longitudes
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_100_SEPARATES_THE_YEAR_LENGTHS,
        first_dasa,
        pada_of,
        pada_sequence,
    )

    birth = from_local(**chart(48)["birth_data"]).jd_ut
    nine = pada_sequence("savya", 1, 2)

    def cancer_opens(moon_longitude, year_days):
        balance = first_dasa(
            nine, pada_of(moon_longitude)["elapsed_fraction"])["balance_years"]
        # Pisces' balance, then Sc 7, Li 16 and Vi 9
        year, month, _day, _hour = swe.revjul(
            birth + (balance + 7 + 16 + 9) * year_days)
        return year, month

    exact = _chart_48_moon()
    assert cancer_opens(exact, 360.0) == (1966, 9)            # the book
    assert cancer_opens(exact, 365.25) == (1967, 3)
    assert cancer_opens(exact, 365.2564) == (1967, 3)

    # and the conclusion survives the Moon's arcminute rounding
    rounded = longitudes(48)["Moon"]
    assert cancer_opens(rounded, 360.0)[0] == 1966
    assert cancer_opens(rounded, 365.25)[0] == 1967

    assert "September 1966" in EXAMPLE_100_SEPARATES_THE_YEAR_LENGTHS


def test_cancer_cancer_antardasa_covers_the_fathers_death_in_1967():
    """"Cn-Cn antardasa was running at the time of his father's demise."
    Cancer's own antardasa is the first of its nine and over five years long.
    """
    from hora.charts.book import chart
    from hora.dasha.nakshatra.kalachakra import antardasas

    assert chart(48)["events"]["the native's father passed away"] == "1967"

    cancer = antardasas(1, 15, 21.0)             # Cn at wheel position 15
    assert A[cancer[0]["sign"]] == "Cn"
    assert sum(row["share_years"] for row in cancer) == 86
    assert cancer[0]["years"] == pytest.approx(21.0 * 21 / 86)
    assert cancer[0]["years"] > 5                # Sept 1966 well into 1971


# ---------------------------------------------------------------------------
# Example 101 — Chart 3, Vajpayee's Capricorn dasa
# ---------------------------------------------------------------------------

def _chart_3(code):
    """Chart 3 in one chart, with Scorpio's co-lord resolved by §15.5.1."""
    from hora.charts.book import longitudes
    from hora.charts.colord import stronger
    from hora.charts.vargas import varga
    from hora.core.const import Graha

    printed = longitudes(3)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    references = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars",
                  "Merc": "Mercury", "Jup": "Jupiter", "Ven": "Venus",
                  "Sat": "Saturn", "Asc": "Lagna"}

    def sign_of(longitude):
        return (int(longitude // 30) if code == "D1"
                else varga(longitude, code).sign)

    signs = {int(g): sign_of(printed[n]) for n, g in named.items()}
    in_chart = {graha: sign * 30.0 for graha, sign in signs.items()}
    return {
        "lagna": sign_of(printed["Asc"]),
        "gl": sign_of(printed["GL"]),
        "signs": signs,
        "references": {ref: sign_of(printed[n])
                       for n, ref in references.items()},
        "co_lords": {rasi: stronger(rasi, in_chart).winner for rasi in (7, 10)},
    }


def test_example_101s_two_sav_figures_for_capricorn():
    """"Cp has 31 rekhas in the SAV of D-10 and 34 rekhas in the SAV of rasi
    chart. Because Cp is strong in both charts, Cp dasa must be good."
    """
    from hora.charts.ashtakavarga import sarvashtakavarga
    from hora.dasha.nakshatra.kalachakra import (
        SAV_STRONG_REKHAS,
        STRONG_IN_BOTH_CHARTS,
    )

    capricorn = R["Cp"]
    rasi = sarvashtakavarga(_chart_3("D1")["references"])
    d10 = sarvashtakavarga(_chart_3("D10")["references"])

    assert rasi["rekhas"][capricorn] == 34
    assert d10["rekhas"][capricorn] == 31
    assert min(34, 31) >= SAV_STRONG_REKHAS
    assert rasi["total"] == d10["total"] == 337
    assert "strong in both charts" in STRONG_IN_BOTH_CHARTS


def test_the_strong_d10_houses_are_the_1st_3rd_5th_7th_and_10th_from_al():
    """"The houses having 30 or more rekhas are the 1st, 3rd, 5th, 7th and 10th
    houses from AL."  Five signs reach 30 in the D-10 SAV and they are exactly
    those five houses from a Virgo AL.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.ashtakavarga import sarvashtakavarga
    from hora.dasha.nakshatra.kalachakra import (
        AL_IS_THE_REFERENCE_FOR_FAME,
        SAV_STRONG_REKHAS,
    )

    chart = _chart_3("D10")
    al = arudha_pada(1, chart["lagna"], chart["signs"], chart["co_lords"]).sign
    assert A[al] == "Vi"

    sav = sarvashtakavarga(chart["references"])
    strong = {(sign - al) % 12 + 1: (A[sign], sav["rekhas"][sign])
              for sign in range(12)
              if sav["rekhas"][sign] >= SAV_STRONG_REKHAS}
    assert sorted(strong) == [1, 3, 5, 7, 10]
    assert strong[1] == ("Vi", 33)
    assert strong[3] == ("Sc", 35)
    assert strong[5] == ("Cp", 31)
    assert strong[7] == ("Pi", 30)
    assert strong[10] == ("Ge", 33)
    assert "most appropriate reference" in AL_IS_THE_REFERENCE_FOR_FAME


def test_the_fame_houses_from_al_are_not_a_fixed_list():
    """Example 99 named the 2nd, 5th and 7th from AL; Example 101 names the
    1st, 3rd, 5th, 7th and 10th, hedged with "most of these". Each describes
    the chart in hand.
    """
    from hora.dasha.nakshatra.kalachakra import (
        THE_FAME_HOUSES_FROM_AL_ARE_NOT_A_FIXED_LIST,
        TWO_FIVE_AND_SEVEN_FROM_AL_ARE_RECOGNITION,
    )

    ninety_nine = {2, 5, 7}
    hundred_one = {1, 3, 5, 7, 10}
    assert ninety_nine & hundred_one == {5, 7}
    assert ninety_nine - hundred_one == {2}

    assert "recognition and awards" in TWO_FIVE_AND_SEVEN_FROM_AL_ARE_RECOGNITION
    assert "most of these" in THE_FAME_HOUSES_FROM_AL_ARE_NOT_A_FIXED_LIST


def test_capricorns_lord_is_exalted_in_gl_in_the_d10():
    """"Moreover, the lord of Cp is exalted in GL."  Saturn sits in Libra in
    the D-10, which is both its exaltation and the sign GL occupies there --
    two conditions the rasi chart does not meet, where GL is in Cancer.
    """
    from hora.core.const import EXALTATION_RASI, RASI_LORD, Graha

    saturn = int(Graha.SATURN)
    assert int(RASI_LORD[R["Cp"]]) == saturn

    d10 = _chart_3("D10")
    assert A[d10["signs"][saturn]] == "Li"
    assert d10["signs"][saturn] == int(EXALTATION_RASI[saturn])
    assert d10["gl"] == d10["signs"][saturn]

    rasi = _chart_3("D1")
    assert A[rasi["gl"]] == "Cn"                 # not in the rasi chart
    assert rasi["signs"][saturn] != rasi["gl"]


def test_a5_is_in_capricorn_in_both_charts():
    """"Cp contains A5 in rasi chart and D-10."  Two different lagnas, two
    different lords' placements, one sign.
    """
    from hora.charts.arudha import arudha_pada
    from hora.dasha.nakshatra.kalachakra import (
        A5_IS_THE_ILLUSION_OF_THE_FIFTH,
        EXAMPLE_101_REASONS,
    )

    for code in ("D1", "D10"):
        chart = _chart_3(code)
        a5 = arudha_pada(5, chart["lagna"], chart["signs"],
                         chart["co_lords"]).sign
        assert A[a5] == "Cp", code

    assert "positions held and the power wielded" in A5_IS_THE_ILLUSION_OF_THE_FIFTH
    assert "academic distinctions and awards" in A5_IS_THE_ILLUSION_OF_THE_FIFTH
    assert [row["rule"] for row in EXAMPLE_101_REASONS] == [
        "sav", "arudha", "lord", "arudha"]


def test_example_101s_kalachakra_dasas():
    """"About 4.5 years of Vi dasa was left at birth. The dasas to follow are
    Le, Cn, Ge, Ta, Ar, Sg, Cp and Aq."

    Moon at 15 Le 28 is Poorvaphalguni's 1st pada, apasavya-2, paramayush 86 --
    and the balance again needs the ephemeris Moon, the printed one giving 4.96.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        first_dasa,
        nine_from_birth,
        pada_of,
        pada_sequence,
        paramayush,
        sub_group_of,
    )

    record = chart(3)
    moon = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 3", **record["place"]),
        Settings(node_type=NodeType.MEAN)
    ).positions[int(Graha.MOON)].longitude

    where = pada_of(moon)
    assert (where["nakshatra"], where["group"], where["pada"]) == (
        11, "apasavya", 1)                       # Poorvaphalguni
    assert sub_group_of(11) == 2

    nine = pada_sequence("apasavya", 2, 1)
    assert [A[rasi] for rasi in nine] == [
        "Pi", "Aq", "Cp", "Sg", "Sc", "Li", "Vi", "Le", "Cn"]
    assert paramayush(nine) == 86

    birth = first_dasa(nine, where["elapsed_fraction"])
    assert birth["rasi"] == "Virgo"
    assert birth["position"] == 6
    assert birth["balance_years"] == pytest.approx(4.65, abs=0.01)   # "about 4.5"

    printed = first_dasa(
        nine, pada_of(longitudes(3)["Moon"])["elapsed_fraction"])
    assert printed["balance_years"] == pytest.approx(4.96, abs=0.01)

    following = dasa_order(11, 1, 8, skip=birth["position"] + 1)
    assert [A[row["sign"]] for row in following] == [
        "Le", "Cn", "Ge", "Ta", "Ar", "Sg", "Cp", "Aq"]
    assert following[6]["years"] == 4            # "his 4-year Cp dasa"
    assert len(nine_from_birth(11, 1, birth["position"])["dasas"]) == 9


def test_capricorn_dasa_runs_1998_to_2002_only_under_savana():
    """"His 4-year Cp dasa runs during 1998-2002."  Savana gives 1998-08-04 to
    2002-07-14; a solar year gives 1999-08-21 to 2003-08-21. Both ends move,
    which makes this a sharper separation than Example 100's single date.
    """
    import swisseph as swe

    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_101_SEPARATES_THE_YEAR_LENGTHS,
        first_dasa,
        pada_of,
        pada_sequence,
    )

    record = chart(3)
    birth = from_local(**record["birth_data"]).jd_ut
    nine = pada_sequence("apasavya", 2, 1)

    def capricorn_runs(moon_longitude, year_days):
        balance = first_dasa(
            nine, pada_of(moon_longitude)["elapsed_fraction"])["balance_years"]
        # Vi's balance, then Le 5, Cn 21, Ge 9, Ta 16, Ar 7 and Sg 10
        start = birth + (balance + 5 + 21 + 9 + 16 + 7 + 10) * year_days
        return (swe.revjul(start)[0], swe.revjul(start + 4 * year_days)[0])

    exact = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 3", **record["place"]),
        Settings(node_type=NodeType.MEAN)
    ).positions[int(Graha.MOON)].longitude

    assert capricorn_runs(exact, 360.0) == (1998, 2002)       # the book
    assert capricorn_runs(exact, 365.25) == (1999, 2003)
    assert capricorn_runs(exact, 365.2564) == (1999, 2003)

    # and the conclusion survives the Moon's arcminute rounding
    rounded = longitudes(3)["Moon"]
    assert capricorn_runs(rounded, 360.0) == (1998, 2002)
    assert capricorn_runs(rounded, 365.25)[0] == 1999

    assert "1998-2002" in EXAMPLE_101_SEPARATES_THE_YEAR_LENGTHS
    assert record["events"]["India's Prime Minister since"] == "March 1998"


def test_both_kalachakra_datings_agree_and_neither_changes_the_default():
    """Examples 100 and 101 are independent charts and independent events, and
    both land on savana. The default stays sidereal; OI-115 is still open.
    """
    from hora.core.settings import DashaYearLength, Settings
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_100_SEPARATES_THE_YEAR_LENGTHS,
        EXAMPLE_101_SEPARATES_THE_YEAR_LENGTHS,
        FOOTNOTE_65,
    )

    assert "September 1966" in EXAMPLE_100_SEPARATES_THE_YEAR_LENGTHS
    assert "1998-2002" in EXAMPLE_101_SEPARATES_THE_YEAR_LENGTHS
    assert "prefers savana years" in FOOTNOTE_65

    assert Settings().dasha_year_length is DashaYearLength.SIDEREAL
    assert Settings().dasha_year_length is not DashaYearLength.SAVANA


# ---------------------------------------------------------------------------
# Example 102 — Chart 49, the ISKCON devotee's D-20
# ---------------------------------------------------------------------------

def _chart_49(code):
    """Chart 49 in one chart, from its own printed longitudes."""
    from hora.charts.book import longitudes
    from hora.charts.colord import stronger
    from hora.charts.vargas import varga
    from hora.core.const import Graha

    printed = longitudes(49)
    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
             "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}
    references = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars",
                  "Merc": "Mercury", "Jup": "Jupiter", "Ven": "Venus",
                  "Sat": "Saturn", "Asc": "Lagna"}

    def sign_of(longitude):
        return (int(longitude // 30) if code == "D1"
                else varga(longitude, code).sign)

    signs = {int(g): sign_of(printed[n]) for n, g in named.items()}
    return {
        "lagna": sign_of(printed["Asc"]),
        "signs": signs,
        "references": {ref: sign_of(printed[n])
                       for n, ref in references.items()},
        "co_lords": {rasi: stronger(rasi, {g: s * 30.0 for g, s in
                                           signs.items()}).winner
                     for rasi in (7, 10)},
    }


def test_chart_49_is_chart_37_recast_and_ours_reproduces_chart_37():
    """Same nativity, one minute earlier and about 1.5' further on in every
    graha. Our settings match Chart 37 within an arcminute and sit below Chart
    49 by more than that. D-69.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import CHART_49_IS_NOT_CHART_37_RECAST

    thirty_seven, forty_nine = chart(37), chart(49)
    assert thirty_seven["place"] == forty_nine["place"]
    assert thirty_seven["birth_data"]["minute"] == 44
    assert forty_nine["birth_data"]["minute"] == 43
    assert thirty_seven["chara_karakas"] == forty_nine["chara_karakas"]
    assert thirty_seven["longitudes"] != forty_nine["longitudes"]

    gaps = {name: (longitudes(49)[name] - longitudes(37)[name]) * 60
            for name in longitudes(37)}
    for name in ("Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat", "Rahu"):
        assert 0.5 < gaps[name] < 2.5, f"{name}: {gaps[name]:+.1f}'"
    assert gaps["Asc"] < -30                     # the minute of time

    for number, ceiling in ((37, 1.0), (49, 2.0)):
        record = chart(number)
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name=f"Chart {number}", **record["place"]),
            Settings(node_type=NodeType.MEAN))
        worst = max(abs(computed.positions[int(graha)].longitude
                        - longitudes(number)[name]) * 60
                    for name, graha in GRAHA_OF.items())
        assert worst < ceiling
        if number == 49:
            assert worst > 1.0                   # and NOT within an arcminute

    assert "1.5'" in CHART_49_IS_NOT_CHART_37_RECAST


def test_the_two_castings_give_different_d20_signs():
    """Venus sits an arcminute from an exact D-20 boundary -- 25 Sc 30 is
    17 x 1 deg 30' -- so the ayanamsa alone decides its amsa. GL moves too.
    The drawn diagram follows Chart 49.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.vargas import varga
    from hora.core.const import RASI_ABBR

    drawn = dict(chart(49)["divisional"]["D20"])
    drawn.pop("AL")
    differ = {}
    for name, abbr in drawn.items():
        from_49 = str(RASI_ABBR[varga(longitudes(49)[name], "D20").sign])
        from_37 = str(RASI_ABBR[varga(longitudes(37)[name], "D20").sign])
        assert from_49 == abbr, f"{name}: drawn {abbr}, from Chart 49 {from_49}"
        if from_37 != abbr:
            differ[name] = (from_37, abbr)

    assert differ == {"GL": ("Ge", "Ta"), "Ven": ("Ar", "Ta")}
    assert abs(longitudes(49)["Ven"] - (R["Sc"] * 30 + 25.5)) * 60 < 1.1


def test_example_102s_d20_sav_needs_chart_49s_own_longitudes():
    """"Pi ... has 33 rekhas in SAV", "Ar has 33 rekhas in D-20 SAV", and "the
    3rd house (Ge) and A3 (Li) have 30 or more rekhas". All four come out of
    Chart 49's longitudes; Chart 37's give 30, 32 and 28.
    """
    from hora.charts.ashtakavarga import sarvashtakavarga
    from hora.charts.book import chart, longitudes
    from hora.charts.vargas import varga
    from hora.core.const import Graha

    sav = sarvashtakavarga(_chart_49("D20")["references"])
    assert sav["total"] == 337
    assert sav["rekhas"][R["Pi"]] == 33
    assert sav["rekhas"][R["Ar"]] == 33
    assert sav["rekhas"][R["Ge"]] == 31
    assert sav["rekhas"][R["Li"]] == 30
    assert chart(49)["sav_strongest"]["D20"] == {
        "Ar": 33, "Pi": 33, "Ge": 31, "Li": 30}

    named = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
             "Merc": "Mercury", "Jup": "Jupiter", "Ven": "Venus",
             "Sat": "Saturn", "Asc": "Lagna"}
    other = sarvashtakavarga({
        ("Mercury" if n == "Merc" else "Jupiter" if n == "Jup" else
         "Venus" if n == "Ven" else "Saturn" if n == "Sat" else
         "Lagna" if n == "Asc" else n): varga(longitudes(37)[n], "D20").sign
        for n in named})
    assert other["rekhas"][R["Pi"]] == 30        # not 33
    assert other["rekhas"][R["Ar"]] == 32        # not 33
    assert other["rekhas"][R["Li"]] == 28        # below thirty


def test_example_102s_houses_and_arudha_padas_in_the_d20():
    """"Pi is the 12th house in D-20 and Sg is the 9th house."  "Darapada (A7)
    of D-20 is in Sg."  "Ar contains A5 (mantra pada)."  "A3 (Li)."
    """
    from hora.charts.arudha import arudha_pada
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.nakshatra.kalachakra import (
        A5_IS_THE_MANTRA_PADA,
        D20_HOUSE_READINGS,
    )

    chart = _chart_49("D20")
    lagna = chart["lagna"]
    assert A[lagna] == "Ar"
    assert A[(lagna + 11) % 12] == "Pi"          # the 12th
    assert A[(lagna + 8) % 12] == "Sg"           # the 9th
    assert A[(lagna + 2) % 12] == "Ge"           # the 3rd

    padas = {house: A[arudha_pada(house, lagna, chart["signs"],
                                  chart["co_lords"]).sign]
             for house in (3, 5, 7)}
    assert padas == {3: "Li", 5: "Ar", 7: "Sg"}

    jupiter = int(Graha.JUPITER)
    assert int(RASI_LORD[R["Pi"]]) == int(RASI_LORD[R["Sg"]]) == jupiter

    # Sg holds the Sun and both nodes in the D-20
    for graha in (Graha.SUN, Graha.RAHU, Graha.KETU):
        assert chart["signs"][int(graha)] == R["Sg"]

    assert "mantra pada" in A5_IS_THE_MANTRA_PADA
    assert [row["house"] for row in D20_HOUSE_READINGS] == [3, 5, 7, 9, 12]
    assert [row["arudha"] for row in D20_HOUSE_READINGS] == [
        "A3", "A5", "A7", None, None]


def test_the_d10_half_of_the_third_house_claim_fails():
    """"the 3rd house and A3 have 30 or more rekhas, in D-10 SAV also."  A3 is
    Pisces with 31; the 3rd house from a Libra D-10 lagna is Sagittarius with
    25, and no other reading of "the 3rd house" reaches thirty either. D-70.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.ashtakavarga import sarvashtakavarga
    from hora.dasha.nakshatra.kalachakra import (
        SAV_STRONG_REKHAS,
        THE_D10_THIRD_HOUSE_DOES_NOT_REACH_THIRTY,
    )

    d10 = _chart_49("D10")
    sav = sarvashtakavarga(d10["references"])
    assert A[d10["lagna"]] == "Li"

    a3 = arudha_pada(3, d10["lagna"], d10["signs"], d10["co_lords"]).sign
    assert A[a3] == "Pi"
    assert sav["rekhas"][a3] == 31 >= SAV_STRONG_REKHAS      # the half that holds

    third = (d10["lagna"] + 2) % 12
    assert A[third] == "Sg"
    assert sav["rekhas"][third] == 25 < SAV_STRONG_REKHAS    # the half that fails

    strong = {A[sign] for sign in range(12)
              if sav["rekhas"][sign] >= SAV_STRONG_REKHAS}
    assert strong == {"Cn", "Le", "Sc", "Pi"}
    for candidate in ("Ge",                       # the D-20's 3rd house
                      A[(_chart_49("D1")["lagna"] + 2) % 12]):   # rasi's 3rd
        assert candidate not in strong

    assert "half-supported" in THE_D10_THIRD_HOUSE_DOES_NOT_REACH_THIRTY


def test_example_102s_kalachakra_dasas():
    """"Ta dasa of about 9.5 years was left at birth. The dasas to follow are
    Ar, Pi, Aq, Cp, Sg, Ar, Ta and Ge."
    """
    from hora.charts.book import longitudes
    from hora.dasha.nakshatra.kalachakra import (
        dasa_order,
        first_dasa,
        nine_from_birth,
        pada_of,
        pada_sequence,
        paramayush,
        sub_group_of,
    )

    moon = pada_of(longitudes(49)["Moon"])
    assert (moon["nakshatra"], moon["group"], moon["pada"]) == (
        21, "savya", 3)                          # Uttarashadha
    assert sub_group_of(21) == 1

    nine = pada_sequence("savya", 1, 3)
    assert [A[rasi] for rasi in nine] == [
        "Ta", "Ar", "Pi", "Aq", "Cp", "Sg", "Ar", "Ta", "Ge"]
    assert paramayush(nine) == 83

    birth = first_dasa(nine, moon["elapsed_fraction"])
    assert birth["rasi"] == "Taurus"
    assert birth["position"] == 0
    assert birth["balance_years"] == pytest.approx(9.775)     # "about 9.5"

    following = dasa_order(21, 3, 8, skip=1)
    assert [A[row["sign"]] for row in following] == [
        "Ar", "Pi", "Aq", "Cp", "Sg", "Ar", "Ta", "Ge"]
    assert len(nine_from_birth(21, 3, 0)["dasas"]) == 9


def test_sagittarius_then_aries_are_the_antardasas_the_example_reads():
    """"Sg antardasa in it was running when he moved to the monastery" and
    "the next antardasa belonged to Ar".  Pisces sits at wheel position 20, so
    its nine antardasas run Pi, Aq, Cp, Sg, Ar and the walk crosses the wheel's
    end between the fourth and the fifth.
    """
    from hora.charts.book import chart
    from hora.dasha.nakshatra.kalachakra import antardasas

    pisces = antardasas(21, 20, 10.0)
    assert [A[row["sign"]] for row in pisces][:5] == [
        "Pi", "Aq", "Cp", "Sg", "Ar"]
    assert [row["position"] for row in pisces][:5] == [20, 21, 22, 23, 0]
    assert sum(row["years"] for row in pisces) == pytest.approx(10.0)

    # Sagittarius opens a little over two years into the ten-year dasa
    opens = sum(row["years"] for row in pisces[:3])
    assert 2.0 < opens < 2.2
    assert chart(49)["events"][
        "left mathematics, wandered in the forests, found ISKCON and "
        "moved to a monastery"] == "1990"


def test_example_102_cannot_separate_the_year_lengths():
    """"Pi dasa started in July 1987."  The truncated arcminute of Moon spans
    balances from 9.36 to 9.775 years, and both year lengths put Pi somewhere
    in 1987 inside that span -- so this example decides nothing, unlike
    Examples 100 and 101.
    """
    import swisseph as swe

    from hora.charts.book import chart
    from hora.core.timeutil import from_local
    from hora.dasha.nakshatra.kalachakra import (
        EXAMPLE_102_CANNOT_SEPARATE_THE_YEAR_LENGTHS,
        first_dasa,
        pada_of,
        pada_sequence,
    )

    birth = from_local(**chart(49)["birth_data"]).jd_ut
    nine = pada_sequence("savya", 1, 3)
    floor = R["Cp"] * 30 + 3 + 35 / 60.0         # 3 Cp 35, as printed
    ceiling = R["Cp"] * 30 + 3 + 36 / 60.0       # the next arcminute

    span = [first_dasa(nine, pada_of(moon)["elapsed_fraction"])["balance_years"]
            for moon in (floor, ceiling)]
    assert span[0] == pytest.approx(9.775)
    assert span[1] == pytest.approx(9.36)

    for year_days in (360.0, 365.25):
        years = {swe.revjul(birth + (balance + 7) * year_days)[0]
                 for balance in span}
        assert years == {1987}                   # both, either way

    assert "cannot" in EXAMPLE_102_CANNOT_SEPARATE_THE_YEAR_LENGTHS.lower() or (
        "both year lengths" in EXAMPLE_102_CANNOT_SEPARATE_THE_YEAR_LENGTHS)


def test_thirty_rekhas_is_attributed_to_parasara_here():
    """§24.3.1 gave the threshold with "usually"; Example 99 dropped the hedge;
    Example 102 names the authority.
    """
    from hora.dasha.nakshatra.kalachakra import (
        SAV_STRONG_REKHAS,
        THIRTY_REKHAS_IS_PARASARAS,
    )

    assert SAV_STRONG_REKHAS == 30
    assert "as per Parasara" in THIRTY_REKHAS_IS_PARASARAS
