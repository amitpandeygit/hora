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
