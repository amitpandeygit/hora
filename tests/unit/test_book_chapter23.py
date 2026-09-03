"""Chapter 23 — Shoola dasa, the other one.

The eighth of Part 2's nine and the simplest rasi dasa in the book. What is
tested here is what makes it simple: no direction rule, a flat length, and
antardasas that are the dasa rules applied to themselves.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_NAMES

R = {name: i for i, name in enumerate(RASI_NAMES)}
ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


# --------------------------------------------------------------------------
# §23.1 Introduction
# --------------------------------------------------------------------------

def test_this_is_the_dasa_22_1_renamed_the_other_one_to_avoid():
    """§22.1: "some scholars use the name Shoola dasa to denote a different
    dasa. We will learn it in another chapter." This is that chapter, and Part
    2's map has carried both systems since before either was built.
    """
    from hora.core.constants.dasha import PART_2_DASA_SYSTEMS
    from hora.dasha.rasi.niryaana_shoola import THE_NAME_IS_DISAMBIGUATED
    from hora.dasha.rasi.shoola import THE_OTHER_SHOOLA_DASA

    assert "another chapter" in THE_NAME_IS_DISAMBIGUATED
    assert "There is another dasa called Shoola dasa" in THE_OTHER_SHOOLA_DASA

    by_name = {s["name"]: s for s in PART_2_DASA_SYSTEMS}
    assert by_name["Shoola dasa"]["module"] == "hora.dasha.rasi.shoola"
    assert by_name["Niryaana Shoola dasa"]["module"] == (
        "hora.dasha.rasi.niryaana_shoola")
    assert by_name["Shoola dasa"]["purpose"] == "ayur"


def test_its_scope_is_wider_than_chapter_22s():
    """"It shows death, diseases, suffering and death of relatives."

    Niryaana Shoola dasa times the native's own death and nothing else; this
    one reaches disease, suffering, and other people's deaths.
    """
    from hora.dasha.rasi.niryaana_shoola import NIRYAANA_MEANS_DEATH
    from hora.dasha.rasi.shoola import SHOWS

    assert "death of relatives" in SHOWS
    assert "diseases" in SHOWS and "suffering" in SHOWS
    assert "relatives" not in NIRYAANA_MEANS_DEATH


# --------------------------------------------------------------------------
# §23.2 Computation
# --------------------------------------------------------------------------

def test_the_seed_pair_is_narayanas_not_chapter_22s():
    """"Find the stronger of lagna and the 7th house."

    Chapter 18 seeds from the same pair, chapter 22 from the 2nd and 8th. A
    shared pair is not a shared comparison: Narayana dasa is phalita and this
    one times death.
    """
    from hora.dasha.rasi.narayana import DASA_SEED_RULE
    from hora.dasha.rasi.niryaana_shoola import SEED_RULE as CH22_SEED
    from hora.dasha.rasi.shoola import SEED_RULE

    assert SEED_RULE == "Find the stronger of lagna and the 7th house."
    assert "lagna or the 7th house, whichever is stronger" in DASA_SEED_RULE
    assert "2nd and 8th houses" in CH22_SEED


def test_the_seed_is_left_open_for_the_same_reason_chapter_22s_is():
    """OI-131, now covering two systems. Shoola dasa times death, so its seed
    needs §15.5.2's ayur adaptation, which the section will not supply.
    """
    from hora.charts.rasi_strength import RasiStrengthError, stronger
    from hora.dasha.rasi.shoola import ShoolaError, seed

    with pytest.raises(RasiStrengthError, match="not implemented"):
        stronger(R["Leo"], R["Aquarius"], {}, purpose="ayur")

    got = seed(R["Leo"])
    assert (got.lagna_name, got.seventh_name) == ("Leo", "Aquarius")
    assert got.sign is None
    assert "OI-131" in got.undecided

    assert seed(R["Leo"], stronger_house=1).sign == R["Leo"]
    assert seed(R["Leo"], stronger_house=7).sign == R["Aquarius"]
    with pytest.raises(ShoolaError, match="must be 1 or 7"):
        seed(R["Leo"], stronger_house=8)


@pytest.mark.parametrize("lagna", range(12))
def test_the_seed_candidates_are_always_lagna_and_the_seventh(lagna):
    """Six apart, so the pair never collapses — and unlike chapter 22's, one
    of the two candidates is lagna itself.
    """
    from hora.dasha.rasi.shoola import seed

    got = seed(lagna)
    assert got.lagna == lagna
    assert (got.seventh - got.lagna) % 12 == 6


def test_the_direction_is_always_forward_and_the_book_italicises_always():
    """"Dasas start there and *always* go in the regular zodiacal order."

    The first rasi dasa in the book with no direction test at all — no
    odd/even sign, no odd-footedness, and none of the Saturn or Ketu
    exceptions chapters 19, 20 and 22 carry.
    """
    from hora.dasha.rasi import drigdasa, kendradi, niryaana_shoola
    from hora.dasha.rasi.shoola import DIRECTION_RULE, progression

    assert "always go in the regular zodiacal order" in DIRECTION_RULE

    for seed_sign in range(12):
        assert progression(seed_sign).direction == "forward"

    # The tests the other chapters use, which this one does not.
    assert kendradi.direction_of(R["Taurus"]) == "backward"
    assert drigdasa.direction_of(R["Taurus"]) == "forward"
    assert niryaana_shoola.direction_of(R["Taurus"]) == "backward"


@pytest.mark.parametrize("case", (0, 1))
def test_23_2s_two_direction_illustrations(case):
    """"if lagna is in Sc and Ta is stronger than Sc, dasas go as Ta, Ge, Cn,
    Le etc. If lagna is in Le and Aq is stronger than Le, dasas go as Aq, Pi,
    Ar, Ta etc."

    Both seed from the 7th, and both run forward — which is the point of
    printing two.
    """
    from hora.dasha.rasi.shoola import DIRECTION_EXAMPLES, progression, seed

    example = DIRECTION_EXAMPLES[case]
    lagna = ABBR.index(example["lagna"])
    seed_sign = ABBR.index(example["seed"])

    assert seed(lagna).seventh == seed_sign          # the 7th won both times
    got = progression(seed_sign)
    assert tuple(ABBR[s] for s in got.signs[:4]) == example["order"]


@pytest.mark.parametrize("seed_sign", range(12))
def test_every_run_is_the_twelve_rasis_from_the_seed(seed_sign):
    from hora.dasha.rasi.shoola import progression

    got = progression(seed_sign)
    assert len(set(got.signs)) == 12
    assert got.signs[0] == seed_sign
    assert got.signs == tuple((seed_sign + n) % 12 for n in range(12))


def test_every_dasa_is_nine_years_and_the_cycle_is_108():
    """"Each dasa is of 9 years." Flat — not §18.2.2's chart-dependent lengths
    and not chapter 22's 7/8/9 by modality.
    """
    from hora.dasha.rasi.niryaana_shoola import MODALITY_YEARS
    from hora.dasha.rasi.shoola import cycle_years, dasa_years, progression

    assert dasa_years() == 9
    assert cycle_years() == 108
    assert set(MODALITY_YEARS.values()) == {7, 8, 9}     # chapter 22's

    got = progression(R["Aries"])
    assert got.years == (9,) * 12
    assert got.starts == tuple(range(0, 108, 9))
    assert sum(got.years) == 108


def test_the_cycle_is_the_paramaayush_and_23_2_never_says_so():
    """Twelve nines are 108, which is the top of §14.4's long-life range and
    the paramaayush its table works from. §23.2 states the 108 only in the
    mundane rule, as a number to compress.
    """
    from hora.core.constants.maraka import LONGEVITY_RANGES
    from hora.dasha.rasi.shoola import (
        LENGTH_RULE,
        MUNDANE_COMPRESSION_RULE,
        THE_CYCLE_IS_THE_PARAMAAYUSH,
        cycle_years,
    )

    assert LONGEVITY_RANGES["long"][1] == cycle_years() == 108
    assert "108" in MUNDANE_COMPRESSION_RULE
    assert "108" not in LENGTH_RULE
    assert "never connects it to longevity" in THE_CYCLE_IS_THE_PARAMAAYUSH


def test_the_nine_is_the_gestation_period_and_generalises():
    """"Human beings live in the womb for an average of 9 months. For animals
    with an average gestation period of n months, each dasa and antardasa will
    be of n years and n months respectively."

    So 9 is a value, not a constant of the system — an elephant's 22 months
    would give 22-year dasas and a 264-year cycle.
    """
    from hora.dasha.rasi.shoola import (
        GESTATION_RULE,
        HUMAN_GESTATION_MONTHS,
        antardasa_months,
        cycle_years,
        dasa_years,
        progression,
    )

    assert HUMAN_GESTATION_MONTHS == 9
    assert "gestation period of n months" in GESTATION_RULE

    for months in (2, 9, 22):
        assert dasa_years(months) == months
        assert antardasa_months(months) == months
        assert cycle_years(months) == 12 * months
        assert progression(R["Aries"], months).years == (months,) * 12


def test_a_non_positive_gestation_is_refused():
    from hora.core.validate import InputError
    from hora.dasha.rasi.shoola import dasa_years

    with pytest.raises(InputError, match="must be positive"):
        dasa_years(0)


def test_the_antardasas_are_the_dasa_rules_applied_to_themselves():
    """"Antardasas are found using the same rules as dasas, but treating dasa
    rasi as lagna. If Cn dasa is running and Cn is stronger than Cp, then
    antardasas go as Cn, Le, Vi, Li etc and each antardasa will last 9
    months."

    Self-similar, where chapter 22 borrowed §18.3 from Narayana dasa — and it
    inherits the same unsettled comparison one level down.
    """
    from hora.dasha.rasi.shoola import (
        ANTARDASA_EXAMPLE,
        ANTARDASA_RULE,
        antardasa_progression,
    )

    assert "treating dasa rasi as lagna" in ANTARDASA_RULE
    assert "12 equal antardasas" in ANTARDASA_RULE

    got = antardasa_progression(R["Cancer"], stronger_house=1)
    assert [ABBR[s] for s in got["signs"][:4]] == ["Cn", "Le", "Vi", "Li"]
    assert got["months_each"] == 9
    assert got["undecided"] is None
    assert "Cn, Le, Vi, Li" in ANTARDASA_EXAMPLE

    seventh = antardasa_progression(R["Cancer"], stronger_house=7)
    assert [ABBR[s] for s in seventh["signs"][:2]] == ["Cp", "Aq"]


def test_an_unsettled_antardasa_seed_returns_no_order_rather_than_a_guess():
    """The refusal propagates: with the comparison unmade there is no first
    antardasa, and the answer says which comparison is missing.
    """
    from hora.dasha.rasi.shoola import antardasa_progression

    got = antardasa_progression(R["Cancer"])
    assert got["signs"] == ()
    assert "lagna and the 7th" in got["undecided"]
    assert got["months_each"] == 9
    assert "treated as lagna" in got["why"]


def test_twelve_antardasas_of_nine_months_fill_the_nine_year_dasa():
    """"Each dasa is divided into 12 equal antardasas." Nine years is 108
    months, and twelve nine-month antardasas fill it exactly — the same 108
    the cycle has, one unit down.
    """
    from hora.dasha.rasi.shoola import antardasa_months, dasa_years

    for months in (9, 22):
        assert 12 * antardasa_months(months) == 12 * months
        assert dasa_years(months) * 12 == 12 * months


def test_the_mundane_rule_compresses_the_term_not_the_108():
    """"108 years of Shoola dasa are compressed to 5 years or 60 months...
    and a dasa of 9 years is compressed 60/12 = 5 months."

    The book's own arithmetic divides the *term* by twelve; the 108 is the
    cycle being scaled and drops out.
    """
    from hora.dasha.rasi.shoola import (
        MUNDANE_COMPRESSION_EXAMPLE,
        compressed_dasa_months,
        cycle_years,
    )

    assert compressed_dasa_months(60) == 5.0
    assert "60/12 = 5 months" in MUNDANE_COMPRESSION_EXAMPLE
    assert cycle_years() == 108

    # A one-year term and a ten-year one, to show the 108 plays no part.
    assert compressed_dasa_months(12) == 1.0
    assert compressed_dasa_months(120) == 10.0


def test_a_non_positive_term_is_refused():
    from hora.core.validate import InputError
    from hora.dasha.rasi.shoola import compressed_dasa_months

    with pytest.raises(InputError, match="must be positive"):
        compressed_dasa_months(0)


def test_shoola_is_the_only_rasi_dasa_with_no_direction_test():
    """The chapter-by-chapter contrast in one place, so a later reader does
    not carry a direction rule into the one system that has none.
    """
    from hora.dasha.rasi import (
        drigdasa,
        kendradi,
        narayana,
        niryaana_shoola,
        shoola,
    )

    for module in (narayana, kendradi, drigdasa, niryaana_shoola):
        assert hasattr(module, "direction_of"), module.__name__
    assert not hasattr(shoola, "direction_of")

    # And they disagree with each other, which is why it matters. Narayana
    # reads the 9th from the seed, not the seed, so it is a fourth rule again.
    assert drigdasa.direction_of(R["Taurus"]) == "forward"       # odd-footed
    assert kendradi.direction_of(R["Taurus"]) == "backward"      # even sign
    assert narayana.direction_of(R["Taurus"]) == "backward"      # its 9th

    assert shoola.progression(R["Taurus"]).direction == "forward"
    assert shoola.progression(R["Aries"]).direction == "forward"
