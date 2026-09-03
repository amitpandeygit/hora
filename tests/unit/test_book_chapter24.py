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
