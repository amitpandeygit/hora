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


# --------------------------------------------------------------------------
# §23.3 Interpretation
# --------------------------------------------------------------------------

def _chart_42():
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.charts.colord import stronger

    longitudes = {int(g): lon for g, lon in graha_longitudes(42).items()}
    signs = {int(g): sign for g, sign in graha_signs(42).items()}
    lagna_sign = lagna(42)
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}
    return signs, lagna_sign, arudha_pada(1, lagna_sign, signs,
                                          overrides).sign


def test_the_trishoola_reading_is_carried_then_demoted():
    """§23.3 opens "like in Niryana Shoola dasa, dasa of a Trishoola rasi can
    bring death" and a page later says that hit is "less significant" here.
    Both sentences are the chapter's; the second is the one the Lesson keeps.
    """
    from hora.dasha.rasi.shoola import (
        LESSON,
        TRISHOOLA_ALSO_APPLIES,
        TRISHOOLA_IS_LESS_SIGNIFICANT_HERE,
    )

    assert "can bring death" in TRISHOOLA_ALSO_APPLIES
    assert "Niryana" in TRISHOOLA_ALSO_APPLIES          # the printed spelling
    assert "less significant" in TRISHOOLA_IS_LESS_SIGNIFICANT_HERE
    assert "Trishoola" not in LESSON.split("Shoola dasa is the reverse")[1]


def test_the_lesson_states_the_two_systems_against_each_other():
    """The boxed Lesson, which is the chapter's own summary: praana against
    Shiva, Rudra's trines against AL's.
    """
    from hora.dasha.rasi.shoola import LESSON

    praana, shiva = LESSON.split("Shoola dasa is the reverse.")
    assert "motion of praana" in praana
    assert "maraka rasis and the trines from Rudra" in praana
    assert "motion of Shiva" in shiva
    assert "trines from AL or the 3rd house from AL or the 8th house" in shiva
    assert "primarily" in shiva                        # the hedge is kept


def test_rudra_yoga_arises_exactly_when_the_moon_is_in_a_movable_rasi():
    """"Because the 2nd and 8th rasis in the natural zodiac are owned by Mars
    and Venus, rasi aspect on either of them by Moon generates Rudra yoga."

    Taurus and Scorpio are fixed, so what aspects them is movable — and every
    movable rasi reaches at least one. The section never says this; it falls
    out of the rule.
    """
    from hora.core.const import MODALITY_NAMES, RASI_MODALITY
    from hora.dasha.rasi.shoola import (
        RUDRA_YOGA_IS_A_MOON_IN_A_MOVABLE_RASI,
        rudra_yoga,
    )

    movable = {s for s in range(12)
               if str(MODALITY_NAMES[RASI_MODALITY[s]]) == "chara"}
    assert movable == {R["Aries"], R["Cancer"], R["Libra"], R["Capricorn"]}

    applies = {s for s in range(12) if rudra_yoga(s)["applies"]}
    assert applies == movable
    assert "any movable rasi" in RUDRA_YOGA_IS_A_MOON_IN_A_MOVABLE_RASI


@pytest.mark.parametrize("moon,reaches", [
    ("Ar", ["Scorpio"]),
    ("Cn", ["Taurus", "Scorpio"]),
    ("Li", ["Taurus"]),
    ("Cp", ["Taurus", "Scorpio"]),
])
def test_which_of_the_two_natural_houses_each_movable_moon_reaches(moon,
                                                                   reaches):
    """Cancer and Capricorn reach both; Aries reaches only Scorpio and Libra
    only Taurus, each being adjacent to the one it misses.
    """
    from hora.core.const import GRAHA_NAMES, RASI_LORD
    from hora.dasha.rasi.shoola import rudra_yoga

    got = rudra_yoga(ABBR.index(moon))
    assert [row["rasi"] for row in got["reaches"]] == reaches
    for row in got["reaches"]:
        assert row["owner"] == str(GRAHA_NAMES[int(RASI_LORD[row["sign"]])])
    assert {row["owner"] for row in got["reaches"]} <= {"Venus", "Mars"}


def test_rudra_yoga_names_no_planets_and_no_aspect():
    """OI-137. "Rasis aspected by Rudra yoga planets can give death" — but the
    section never says which planets the yoga is, nor whether their aspect is
    the rasi one it named for the Moon or graha drishti.
    """
    from hora.dasha.rasi.shoola import (
        RUDRA_YOGA_PLANETS_ARE_NOT_NAMED,
        RUDRA_YOGA_RULE,
        rudra_yoga,
    )

    assert "rasi aspect on either of them by Moon" in RUDRA_YOGA_RULE
    assert "rasis aspected by Rudra yoga planets" in RUDRA_YOGA_RULE

    fires = rudra_yoga(R["Cancer"])
    assert fires["undecided"] == RUDRA_YOGA_PLANETS_ARE_NOT_NAMED
    assert rudra_yoga(R["Taurus"])["undecided"] is None   # it does not arise


def test_the_two_rules_are_the_authors_own_and_say_so():
    """"This author found the following rules to hold true in many cases",
    then a quotation. Not classical and not attributed to a maharshi — the
    same shape as §22.2.1's antardasa suggestion.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION,
    )
    from hora.dasha.rasi.shoola import AUTHORS_RULES, AUTHORS_RULES_ARE_HIS_OWN

    assert "This author found" in AUTHORS_RULES_ARE_HIS_OWN
    assert "in many cases" in AUTHORS_RULES_ARE_HIS_OWN
    assert "This author suggests" in ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION
    assert "AL or the trines from it" in AUTHORS_RULES


def test_the_trines_from_al_are_unconditional_and_the_3rd_and_8th_are_not():
    """"AL or the trines from it can give death. **If** malefics or marakas
    occupy or aspect the 3rd from AL or the 8th from AL, those 2 houses can
    give death."

    Five houses in two groups, and only the second group carries a condition.
    """
    from hora.dasha.rasi.shoola import DEATH_HOUSES_FROM_AL, death_rasis

    assert [row["houses"] for row in DEATH_HOUSES_FROM_AL] == [(1, 5, 9),
                                                              (3, 8)]
    assert DEATH_HOUSES_FROM_AL[0]["needs"] is None
    assert "malefics or marakas" in DEATH_HOUSES_FROM_AL[1]["needs"]

    got = death_rasis(R["Cancer"])
    assert [row["house_from_al"] for row in got] == [1, 5, 9, 3, 8]
    # The 8th is Table 32's, per Example 92 — Sagittarius, not Aquarius.
    assert [ABBR[row["sign"]] for row in got] == ["Cn", "Sc", "Pi", "Vi", "Sg"]
    assert got[-1]["by"] == "Table 32"
    assert got[-1]["ordinary_eighth"] == "Aquarius"
    for row in got[:3]:
        assert row["applies"] is True
    for row in got[3:]:
        assert row["applies"] is None                  # no chart was given
        assert "no chart given" in row["undecided"]


def test_the_condition_reports_both_aspects_because_23_3_names_neither():
    """§14.2 said "using graha drishti" outright when it meant it; §23.3 says
    only "occupy or aspect". Occupants, graha drishti and rasi drishti are
    returned separately and the row says the section does not choose.
    """
    from hora.dasha.rasi.shoola import death_rasis

    signs, lagna_sign, al = _chart_42()
    got = {row["house_from_al"]: row
           for row in death_rasis(al, signs, lagna=lagna_sign)}

    for house in (3, 8):
        row = got[house]
        assert set(row) >= {"occupied_by", "aspected_by_graha_drishti",
                            "aspected_by_rasi_drishti"}
        assert row["applies"] is True
        assert "which aspect" in row["undecided"]


def test_marakas_are_not_counted_unless_lagna_is_given():
    """"Malefics **or marakas**" — and which grahas are marakas depends on
    lagna, so without it the row says so rather than counting malefics alone
    and calling the rule satisfied.
    """
    from hora.dasha.rasi.shoola import death_rasis

    signs, _lagna, al = _chart_42()
    without = {row["house_from_al"]: row for row in death_rasis(al, signs)}
    assert "marakas were not computed" in without[3]["undecided"]


def test_al_is_read_instead_of_lagna_and_23_3_says_why():
    """"AL is involved instead of lagna, because our existence is a maya
    (illusion) and what Lord Shiva destroys is the illusion of our existence."

    The one place in Part 2 where a rule's *reference* is argued for rather
    than stated, and it is the reason every reading here counts from AL.
    """
    from hora.dasha.rasi.shoola import DEATH_HOUSES_FROM_AL, WHY_AL_AND_NOT_LAGNA

    assert "maya (illusion)" in WHY_AL_AND_NOT_LAGNA
    assert "physical body (lagna) simply merges" in WHY_AL_AND_NOT_LAGNA
    assert all("AL" in row["text"] for row in DEATH_HOUSES_FROM_AL)


def test_23_3_re_describes_chapter_22s_seed_as_the_8th_from_the_self():
    """"Lagna and 7th house both show the self of a person... Niryaana Shoola
    dasa starts from the 8th house from one of them."

    That makes §22.2.1's odd 2nd-and-8th pair chapter 18's lagna-and-7th pair
    shifted by eight: the 8th from lagna is the 8th house and the 8th from the
    7th is the 2nd. The two systems seed from the same two points.
    """
    from hora.dasha.rasi.niryaana_shoola import seed as niryaana_seed
    from hora.dasha.rasi.shoola import (
        NIRYAANA_SEEDS_FROM_THE_EIGHTH_OF_THE_SELF,
    )
    from hora.dasha.rasi.shoola import seed as shoola_seed

    assert "8th house from one of them" in (
        NIRYAANA_SEEDS_FROM_THE_EIGHTH_OF_THE_SELF)

    for lagna in range(12):
        ours = shoola_seed(lagna)
        theirs = niryaana_seed(lagna)
        assert (ours.lagna + 7) % 12 == theirs.eighth
        assert (ours.seventh + 7) % 12 == theirs.second


def test_the_theory_explains_chapter_22s_irregularity_and_this_ones_absence():
    """"That is why it has an uneven motion... the lengths of dasas can be 7,
    8 or 9 years... In Shoola dasa, however, the motion has a constant rate of
    9 years per dasa and the order of dasas is always fixed."

    §23.3 is the only place either chapter says *why* its computation rules
    look the way they do, and it accounts for both at once.
    """
    from hora.dasha.rasi.niryaana_shoola import MODALITY_YEARS
    from hora.dasha.rasi.shoola import THE_TWO_MOTIONS, cycle_years, dasa_years

    assert "7, 8 or 9 years" in THE_TWO_MOTIONS
    assert sorted(set(MODALITY_YEARS.values())) == [7, 8, 9]
    assert "constant rate of 9 years per dasa" in THE_TWO_MOTIONS
    assert dasa_years() == 9
    assert "quartz crystal" in THE_TWO_MOTIONS
    assert cycle_years() == 108


def test_criterion_2_limits_the_answer_to_four_dasas():
    """"The first 4 Shoola dasas (0-36 years) bring death to a person of the
    short life category", and likewise the middle and last four.
    """
    from hora.core.constants.maraka import LONGEVITY_RANGES
    from hora.dasha.rasi.shoola import ShoolaError, longevity_block

    assert longevity_block("short")["positions"] == (0, 1, 2, 3)
    assert longevity_block("middle")["positions"] == (4, 5, 6, 7)
    assert longevity_block("long")["positions"] == (8, 9, 10, 11)

    for category in LONGEVITY_RANGES:
        got = longevity_block(category)
        assert tuple(got["range"]) == tuple(LONGEVITY_RANGES[category])
        assert len(got["positions"]) == 4

    with pytest.raises(ShoolaError, match="longevity must be"):
        longevity_block("very long")


def test_the_blocks_fall_exactly_on_dasa_boundaries_where_chapter_22s_do_not():
    """Four nines are thirty-six, so 0-36, 36-72 and 72-108 are dasa
    boundaries and no Shoola dasa straddles a longevity range. Chapter 22's 7,
    8 and 9 year dasas do straddle them, which is OI-133 — the flat length is
    what makes criterion 2 exact here.
    """
    from hora.dasha.rasi.niryaana_shoola import progression as niryaana_run
    from hora.dasha.rasi.shoola import (
        THE_BLOCKS_PARTITION_THE_CYCLE_EXACTLY,
        longevity_block,
        progression,
    )

    run = progression(R["Aries"])
    for category in ("short", "middle", "long"):
        block = longevity_block(category)
        low, high = block["range"]
        spans = [(run.starts[p], run.starts[p] + run.years[p])
                 for p in block["positions"]]
        assert spans[0][0] == low and spans[-1][1] == high
        assert all(low <= a and b <= high for a, b in spans)

    # The same test on a Niryaana Shoola run finds dasas that straddle.
    other = niryaana_run(R["Aries"])
    straddling = [i for i, start in enumerate(other.starts)
                  if start < 36 < start + other.years[i]]
    assert straddling, "chapter 22's lengths do cut across 36"
    assert "OI-133" in THE_BLOCKS_PARTITION_THE_CYCLE_EXACTLY


def test_criterion_1_shields_a_rasi_unless_the_shield_is_rudra():
    """"Usually a rasi occupied or aspected by AK or Jupiter does not kill a
    native, unless that planet happens to be Rudra."

    Chart 42 is the exception in one chart: Venus is the AK, occupies Aries,
    and Venus is Rudra there — so the shield is cancelled by its own clause.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import SELECTION_CRITERIA, protected_by

    signs, _lagna, _al = _chart_42()
    ak = int(Graha.VENUS)

    unshielded = protected_by(R["Aries"], signs, ak, rudra=ak)
    assert not unshielded["protected"]
    assert [s["role"] for s in unshielded["rudra_cancels"]] == ["AK"]

    shielded = protected_by(R["Aries"], signs, ak, rudra=int(Graha.MARS))
    assert shielded["protected"]
    assert [s["how"] for s in shielded["shields"]] == ["occupies"]

    assert "unless that planet happens to be Rudra" in SELECTION_CRITERIA[0]


def test_criterion_1_keeps_its_hedge_and_its_missing_input():
    """"Usually" is reported, not applied as a certainty — and without knowing
    who Rudra is, a shield cannot be confirmed either.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import protected_by

    signs, _lagna, _al = _chart_42()
    got = protected_by(R["Aries"], signs, int(Graha.VENUS))
    assert got["hedge"] == "usually"
    assert "whether either shield is Rudra" in got["undecided"]

    # A rasi neither reaches has nothing to decide. On Chart 42 the AK is in
    # Aries and Jupiter in Sagittarius, and Taurus is outside both.
    quiet = protected_by(R["Taurus"], signs, int(Graha.VENUS))
    assert quiet["shields"] == () and not quiet["protected"]
    assert quiet["undecided"] is None


# --------------------------------------------------------------------------
# §23.4 Examples 89 and 90 — the same two charts chapter 22 already read.
# --------------------------------------------------------------------------

def _chart(number):
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.charts.colord import stronger

    longitudes = {int(g): lon for g, lon in graha_longitudes(number).items()}
    signs = {int(g): sign for g, sign in graha_signs(number).items()}
    lagna_sign = lagna(number)
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}
    return longitudes, signs, lagna_sign, arudha_pada(
        1, lagna_sign, signs, overrides).sign


@pytest.mark.parametrize("number,seed,order", [
    (8, "Sc", ["Sc", "Sg", "Cp", "Aq"]),
    (39, "Le", ["Le", "Vi", "Li", "Sc"]),
])
def test_both_examples_seed_from_lagna_and_the_cascade_agrees(number, seed,
                                                              order):
    """"Lagna is stronger and dasas start from Sc"; "...from Le."

    Neither shows its working, but §15.5.2's cascade reaches both on rule 1 —
    Scorpio holds three planets to Taurus's one, Leo five to Aquarius's none.
    Two more agreements for OI-131, on the pair chapter 18 also uses.
    """
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.shoola import progression

    longitudes, _signs, lagna_sign, _al = _chart(number)
    assert ABBR[lagna_sign] == seed

    verdict = stronger(lagna_sign, (lagna_sign + 6) % 12, longitudes,
                       purpose="phalita")
    assert verdict.winner == lagna_sign
    assert verdict.decided_by == "1"

    got = progression(lagna_sign)
    assert [ABBR[s] for s in got.signs[:4]] == order


@pytest.mark.parametrize("number,killer", [(8, "Ar"), (39, "Cp")])
def test_the_sixth_dasa_runs_45_to_54_and_holds_the_death(number, killer):
    """"First 5 dasas are over after 45 years... From his 45th year, the 6th
    dasa was running."

    Five nines are forty-five on every chart, which is the point of a flat
    length — the arithmetic does not depend on the nativity at all.
    """
    from hora.dasha.rasi.shoola import progression

    _longitudes, _signs, lagna_sign, _al = _chart(number)
    got = progression(lagna_sign)

    assert sum(got.years[:5]) == 45
    assert got.starts[5] == 45
    assert got.starts[5] + got.years[5] == 54
    assert ABBR[got.signs[5]] == killer


@pytest.mark.parametrize("number,age", [(8, 50), (39, 46)])
def test_both_deaths_fall_in_that_sixth_dasa(number, age):
    """Chart 8's native died at 50 and Chart 39's at 46, and 45-54 holds
    both — which is why one dasa answers two charts here.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.shoola import progression

    _longitudes, _signs, lagna_sign, _al = _chart(number)
    got = progression(lagna_sign)
    assert got.starts[5] <= age < got.starts[5] + got.years[5]
    assert str(age) in " ".join(chart(number)["events"].values())


def test_the_two_examples_count_the_year_of_death_differently():
    """"The native died in the 50th year" for a native aged 50, and "died in
    his 47th year" for one aged 46. One example counts completed years and the
    other the year in progress.

    It changes nothing — 45-54 holds 46, 47, 50 and 51 alike — but the two
    sentences are not using "Nth year" the same way.
    """
    from hora.dasha.rasi.shoola import progression

    _longitudes, _signs, lagna_sign, _al = _chart(8)
    sixth = progression(lagna_sign)
    start, end = sixth.starts[5], sixth.starts[5] + sixth.years[5]
    for year in (46, 47, 50, 51):
        assert start <= year < end


def test_example_89_selects_aries_as_the_only_trine_in_the_block():
    """"One can see that Ar is a trine from AL. It is the only trine in the
    middle life range."

    Chart 8's AL is Leo, so the trines are Ar, Le and Sg; the middle block is
    Pi, Ar, Ta, Ge; and Aries is the intersection. Exercise 23 computed the
    middle category, so this example needs no assumption.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import three_pairs
    from hora.dasha.rasi.shoola import select_dasa

    _longitudes, signs, lagna_sign, al = _chart(8)
    assert ABBR[al] == "Le"
    assert three_pairs(lagna_sign, signs, book_signs(8)["HL"])[
        "category"] == "middle"

    got = select_dasa(al, lagna_sign, "middle", signs, lagna=lagna_sign)
    assert [c["rasi"] for c in got["candidates"]] == [
        "Pisces", "Aries", "Taurus", "Gemini"]
    assert [c["rasi"] for c in got["trines_from_al"]] == ["Aries"]
    assert got["selected"]["rasi"] == "Aries"
    assert got["selected"]["position"] == 5           # the 6th dasa
    assert got["selected"]["starts"] == 45


def test_example_90_selects_capricorn_the_same_way():
    """"One can see that Cp is the only trine from AL in the middle life
    range."

    Chart 39's AL is Taurus, so the trines are Ta, Vi and Cp; the middle block
    is Sg, Cp, Aq, Pi; and Capricorn is the intersection — the 6th dasa again.
    """
    from hora.dasha.rasi.shoola import select_dasa

    _longitudes, signs, lagna_sign, al = _chart(39)
    assert ABBR[al] == "Ta"

    got = select_dasa(al, lagna_sign, "middle", signs, lagna=lagna_sign)
    assert [c["rasi"] for c in got["candidates"]] == [
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    assert [c["rasi"] for c in got["trines_from_al"]] == ["Capricorn"]
    assert got["selected"]["rasi"] == "Capricorn"
    assert got["selected"]["position"] == 5


def test_example_90_needs_a_category_14_4_does_not_give():
    """D-65. Example 90 says "the middle life range" and §14.4's three pairs
    give **short** on Chart 39 — two fixed+fixed pairs against one fixed+dual,
    with a 40-year paramaayush against a death at 46.

    The category is not a shade here: it picks the four candidates, and under
    short the only trine from AL is **Virgo**, ages 9-18.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import three_pairs
    from hora.dasha.rasi.shoola import select_dasa

    _longitudes, signs, lagna_sign, al = _chart(39)
    computed = three_pairs(lagna_sign, signs, book_signs(39)["HL"])
    assert computed["category"] == "short"
    assert [p["category"] for p in computed["pairs"]] == [
        "short", "long", "short"]

    short = select_dasa(al, lagna_sign, "short", signs, lagna=lagna_sign)
    assert [c["rasi"] for c in short["candidates"]] == [
        "Leo", "Virgo", "Libra", "Scorpio"]
    assert short["selected"]["rasi"] == "Virgo"
    assert short["selected"]["starts"] == 9
    assert short["selected"]["rasi"] != "Capricorn"


def test_the_ordinary_eighth_does_not_rescue_the_category():
    """D-65 again, from the other side. The first pair uses Table 32's 8th;
    the ordinary 8th from Leo is Pisces, whose lord Jupiter is also in Leo, so
    the pair stays fixed+fixed and the verdict stays short.
    """
    from hora.charts.maraka import ordinary_eighth, rudra_eighth
    from hora.core.const import MODALITY_NAMES, RASI_LORD, RASI_MODALITY

    _longitudes, signs, _lagna, _al = _chart(39)
    assert rudra_eighth(R["Leo"]) == R["Cancer"]
    assert ordinary_eighth(R["Leo"]) == R["Pisces"]

    for eighth in (R["Cancer"], R["Pisces"]):
        lord = int(RASI_LORD[eighth])
        assert signs[lord] == R["Leo"]
        assert str(MODALITY_NAMES[RASI_MODALITY[signs[lord]]]) == "sthira"


def test_the_two_examples_take_the_category_as_given():
    """Neither derives it — Example 89's happens to match §14.4 and Example
    90's does not. `select_dasa` therefore takes it as an argument rather than
    computing it, which is what keeps D-65 visible instead of resolving it
    one way silently.
    """
    from hora.dasha.rasi.shoola import select_dasa

    _longitudes, signs, lagna_sign, al = _chart(39)
    picks = {category: select_dasa(al, lagna_sign, category, signs,
                                   lagna=lagna_sign)["selected"]["rasi"]
             for category in ("short", "middle")}
    assert picks == {"short": "Virgo", "middle": "Capricorn"}


def _ak_of(number):
    from hora.charts.book import GRAHA_OF, chart

    karakas = chart(number)["chara_karakas"]
    return int(GRAHA_OF[next(name for name, role in karakas.items()
                             if role == "AK")])


def test_criterion_1_survives_neither_aspect_reading():
    """OI-138. "Usually a rasi occupied or aspected by AK or Jupiter does not
    kill a native", and §23.3 never says which aspect. The two examples pull
    opposite ways on their own killing dasas.
    """
    from hora.charts.aspects import graha_aspects_sign, rasi_drishti
    from hora.core.const import Graha

    reach = {}
    for number, killer in ((8, R["Aries"]), (39, R["Capricorn"])):
        _longitudes, signs, _lagna, _al = _chart(number)
        shields = (_ak_of(number), int(Graha.JUPITER))
        reach[number] = {
            "rasi": [g for g in shields
                     if killer in rasi_drishti(signs[g])],
            "graha": [g for g in shields
                      if graha_aspects_sign(g, signs[g], killer)],
        }

    assert reach[8]["rasi"] == []            # Example 89 needs this
    assert len(reach[8]["graha"]) == 2       # ...and graha drishti breaks it
    assert len(reach[39]["rasi"]) == 2       # Example 90 is broken by this
    assert reach[39]["graha"] == []          # ...and needs graha drishti


def test_chart_8_is_the_one_place_the_ak_is_rudra():
    """Criterion 1's own exception, "unless that planet happens to be Rudra",
    fires on Chart 8: Exercise 23 made Mercury Rudra and Mercury is also its
    AK. It rescues half of Example 89 under graha drishti — but Jupiter is not
    Rudra and still reaches Aries, so the reading stays broken.
    """
    from hora.charts.book import graha_longitudes, lagna
    from hora.charts.maraka import rudra
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import protected_by

    _longitudes, signs, _lagna, _al = _chart(8)
    longitudes = {int(g): lon for g, lon in graha_longitudes(8).items()}
    body = rudra(lagna(8), signs, longitudes)

    assert body["rudra"] == "Mercury"
    assert _ak_of(8) == int(Graha.MERCURY)

    got = protected_by(R["Aries"], signs, _ak_of(8), rudra=int(Graha.MERCURY))
    assert [s["is_rudra"] for s in got["shields"]] == []   # rasi drishti misses
    assert not got["protected"]


def test_criterion_1_is_never_reached_in_either_example():
    """§23.3 frames both criteria as ways to choose from a list — "we have
    listed several rasis above. How do we choose one answer from the list?"

    In both examples the trine rule leaves exactly one candidate inside the
    longevity block, so there is no list to choose from and criterion 1 never
    has to fire. `select_dasa` reports the shields and filters on none.
    """
    from hora.dasha.rasi.shoola import SELECTION_CRITERIA, select_dasa

    for number in (8, 39):
        _longitudes, signs, lagna_sign, al = _chart(number)
        got = select_dasa(al, lagna_sign, "middle", signs, lagna=lagna_sign,
                          atma_karaka=_ak_of(number))
        assert len(got["trines_from_al"]) == 1, number
        assert got["selected"] is not None
        # Shields are reported on every candidate and filter none out.
        assert all("protection" in c for c in got["candidates"])
        assert got["selected"]["rasi"] in [c["rasi"] for c in
                                           got["can_kill"]]

    assert len(SELECTION_CRITERIA) == 2


# --------------------------------------------------------------------------
# Examples 91 and 92 — the 7th wins a seed, and Table 32 reaches the 8th.
# --------------------------------------------------------------------------

def test_example_91_is_the_first_seed_the_7th_house_wins():
    """"The 7th house Cp is stronger and dasas start from Cp."

    Every other worked seed in chapters 22 and 23 goes to lagna or to the 2nd
    — this is the only one that goes to the 7th. It also confirms Example 86's
    lagna: the 7th being Capricorn makes lagna Cancer, which is what Example
    86's "8th houses from Cn and Cp" needs.
    """
    from hora.dasha.rasi.niryaana_shoola import EXAMPLE_86_AWAITS_CHART_61
    from hora.dasha.rasi.shoola import progression, seed

    got = seed(R["Cancer"], stronger_house=7)
    assert got.sign == R["Capricorn"]
    assert "the 7th" in got.why

    run = progression(R["Capricorn"])
    assert [ABBR[s] for s in run.signs[:4]] == ["Cp", "Aq", "Pi", "Ar"]
    assert any("7th house Capricorn is stronger" in item
               for item in EXAMPLE_86_AWAITS_CHART_61)


def test_example_91s_eighth_dasa_is_leo_and_holds_her_67th_year():
    """"First 7 dasas are over after 63 years... So the 8th dasa of Le killed
    the native", who "died in her 67th year".

    Seven nines are sixty-three on any chart, and the 8th from Capricorn is
    Leo. Indira Gandhi was 66 at her death, so her 67th year — the same
    year-in-progress count Example 90 used and Example 89 did not.
    """
    from hora.dasha.rasi.shoola import progression

    run = progression(R["Capricorn"])
    assert sum(run.years[:7]) == 63
    assert ABBR[run.signs[7]] == "Le"
    assert run.starts[7] == 63
    assert run.starts[7] + run.years[7] == 72
    assert run.starts[7] <= 66 < run.starts[7] + run.years[7]


def test_example_91_adds_a_reason_23_3_never_lists():
    """"Le is a trine from AL **and it contains the lord of AL**."

    §23.3's rules read the trines from AL and the 3rd and 8th from it. Where
    AL's own lord sits is a further strengthener the section does not mention,
    and this is the only place it is used.
    """
    from hora.dasha.rasi.shoola import (
        AL_LORD_IN_THE_RASI_STRENGTHENS_IT,
        AUTHORS_RULES,
        DEATH_HOUSES_FROM_AL,
    )

    assert "contains the lord of AL" in AL_LORD_IN_THE_RASI_STRENGTHENS_IT
    assert "lord" not in AUTHORS_RULES
    assert not any("lord" in row["text"] for row in DEATH_HOUSES_FROM_AL)


def test_example_92_seeds_from_lagna_and_the_cascade_agrees():
    """"Lagna is stronger and dasas start from Ar. They go as Ar, Ta, Ge, Cn
    etc."

    Aries holds one planet and Libra none, so §15.5.2 reaches it on rule 1 —
    a third agreement for OI-131 in this chapter.
    """
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.shoola import progression

    longitudes, _signs, lagna_sign, _al = _chart(40)
    assert lagna_sign == R["Aries"]

    verdict = stronger(lagna_sign, (lagna_sign + 6) % 12, longitudes,
                       purpose="phalita")
    assert verdict.winner == R["Aries"]
    assert verdict.decided_by == "1"
    assert "Aries contains 1 planet; Libra contains 0" in verdict.reason

    run = progression(lagna_sign)
    assert [ABBR[s] for s in run.signs[:4]] == ["Ar", "Ta", "Ge", "Cn"]


def test_example_92s_third_dasa_is_gemini_and_holds_the_death():
    """"First 2 dasas are over after 18 years. The native died in the 23rd
    year. From his 18th year, the 3rd dasa was running."

    Gemini runs 18-27 and the native died at 22, towards the end of 1949.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.shoola import progression

    run = progression(R["Aries"])
    assert sum(run.years[:2]) == 18
    assert ABBR[run.signs[2]] == "Ge"
    assert (run.starts[2], run.starts[2] + run.years[2]) == (18, 27)
    assert run.starts[2] <= 22 < run.starts[2] + run.years[2]
    assert "aged 22" in chart(40)["events"]["expired"]


def test_example_92_settles_which_eighth_from_al_23_3_means():
    """"Ge is the 8th house from AL **(see Table 32)** and it contains Rahu."

    §23.3 says only "the 8th from AL". Chart 40's AL is Capricorn: Table 32
    sends it to Gemini and the ordinary count to Leo — and Gemini is where
    Rahu sits. Under the ordinary 8th the example has no reason at all, since
    Gemini is not a trine from Capricorn either.
    """
    from hora.charts.maraka import ordinary_eighth, rudra_eighth
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import (
        THE_EIGHTH_FROM_AL_IS_TABLE_32S,
        death_rasis,
    )

    _longitudes, signs, _lagna, al = _chart(40)
    assert al == R["Capricorn"]
    assert rudra_eighth(al) == R["Gemini"]
    assert ordinary_eighth(al) == R["Leo"]
    assert signs[int(Graha.RAHU)] == R["Gemini"]

    trines = {(al + k) % 12 for k in (0, 4, 8)}
    assert R["Gemini"] not in trines

    rows = {row["house_from_al"]: row for row in death_rasis(al)}
    assert rows[8]["rasi"] == "Gemini"
    assert rows[8]["by"] == "Table 32"
    assert rows[8]["ordinary_eighth"] == "Leo"
    assert "(see Table 32)" in THE_EIGHTH_FROM_AL_IS_TABLE_32S


def test_the_third_from_al_stays_the_ordinary_count():
    """Table 32 is titled for the 8th alone and no example reads a 3rd, so
    the other house of vitality is counted the usual way.
    """
    from hora.dasha.rasi.shoola import death_rasis

    rows = {row["house_from_al"]: row for row in death_rasis(R["Capricorn"])}
    assert rows[3]["sign"] == (R["Capricorn"] + 2) % 12
    assert "by" not in rows[3]


def test_example_92s_gemini_is_reached_only_by_the_8th_rule():
    """Gemini is not a trine from Capricorn, so §23.3's unconditional rule
    misses it entirely — the conditional one carries the whole reading, and
    Rahu is what satisfies it. "Ge is afflicted and it is the house of
    longevity of material self."
    """
    from hora.dasha.rasi.shoola import death_rasis

    _longitudes, signs, lagna_sign, al = _chart(40)
    rows = {row["sign"]: row for row in death_rasis(al, signs,
                                                    lagna=lagna_sign)}

    gemini = rows[R["Gemini"]]
    assert gemini["house_from_al"] == 8
    assert gemini["group"] == "the houses of vitality from AL"
    assert gemini["applies"] is True
    assert "Rahu" in gemini["occupied_by"]


def test_example_92s_dasa_survives_the_selection_machinery():
    """The chart end to end: Example 87 computed short life for this native,
    the short block is the first four dasas, and Gemini is the third of them
    — reached by the 8th-from-AL rule rather than by a trine.

    Unlike Example 90's chart, the category here does agree with §14.4 once
    OI-135's co-lord is settled the way Example 87 settles it.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import three_pairs
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import select_dasa

    _longitudes, signs, lagna_sign, al = _chart(40)
    # Example 87 printed its own three pairs and they need Ketu for Scorpio,
    # which is OI-135; the default lord gives long life instead.
    as_printed = three_pairs(lagna_sign, signs, book_signs(40)["HL"],
                             {R["Scorpio"]: int(Graha.KETU)})
    assert as_printed["category"] == "short"

    got = select_dasa(al, lagna_sign, "short", signs, lagna=lagna_sign)
    assert [c["rasi"] for c in got["candidates"]] == [
        "Aries", "Taurus", "Gemini", "Cancer"]
    gemini = got["candidates"][2]
    assert gemini["can_kill"] and gemini["house_from_al"] == 8
    assert gemini["starts"] == 18
    assert got["trines_from_al"] == () or "Gemini" not in [
        c["rasi"] for c in got["trines_from_al"]]


# --------------------------------------------------------------------------
# Footnote 62, which belongs to Example 92 and states a general rule.
# --------------------------------------------------------------------------

def test_footnote_62_names_three_uses_of_table_32s_eighth():
    """"The 8th house for the purpose of Rudra, the principle of 3 pairs and
    ayur dasa interpretation should be found from Table 32."

    Two of the three we already had: §14.3 says it for Rudra outright and
    §14.4's first pair takes it. The third is what Example 92 applies.
    """
    from hora.charts.maraka import three_pairs
    from hora.core.constants.maraka import RUDRA_RULE, THREE_PAIRS
    from hora.dasha.rasi.shoola import FOOTNOTE_62

    assert "Rudra, the principle of 3 pairs and ayur dasa" in FOOTNOTE_62
    assert "using Table 32" in RUDRA_RULE
    assert "using Table 32" in THREE_PAIRS[0][1]

    _longitudes, signs, lagna_sign, _al = _chart(43)
    from hora.charts.book import signs as book_signs
    got = three_pairs(lagna_sign, signs, book_signs(43)["HL"])
    assert got["eighth_house"]["by"] == "Table 32"


def test_footnote_62_does_not_reach_chapter_22s_antardasa_houses():
    """Its third clause has a boundary and §22.2.2 draws it: "the 6th, 7th,
    8th and 12th houses from Ta (i.e. Li, Sc, **Sg** and Ar)". Sagittarius is
    the ordinary 8th from Taurus; Table 32 gives Gemini. So the footnote
    governs an 8th read off a *reference point* — Rudra's, the three pairs',
    AL's — not one counted from a dasa rasi.
    """
    from hora.charts.maraka import ordinary_eighth, rudra_eighth
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import (
        ANTARDASA_EXAMPLE,
        antardasa_candidates,
    )
    from hora.dasha.rasi.shoola import (
        FOOTNOTE_62_DOES_NOT_REACH_22_2_2S_ANTARDASAS,
    )

    assert ordinary_eighth(R["Taurus"]) == R["Sagittarius"]
    assert rudra_eighth(R["Taurus"]) == R["Gemini"]
    assert "Li, Sc, Sg and Ar" in ANTARDASA_EXAMPLE

    got = antardasa_candidates(R["Taurus"], {int(Graha.JUPITER): R["Leo"]})
    assert got["eighth_name"] == "Sagittarius"
    assert "ordinary 8th" in FOOTNOTE_62_DOES_NOT_REACH_22_2_2S_ANTARDASAS


# --------------------------------------------------------------------------
# Exercise 32 — Chart 43, solved before the book's answer.
# --------------------------------------------------------------------------

def test_chart_43_recomputes_and_is_a_sixteenth_vote_for_the_mean_node():
    """Every body inside one arcminute — Jupiter at 1.00' is the book's own
    rounding, as Chart 42's Sun was — and the ascendant to two seconds of arc.
    Rahu is 86' out under `true`. The first chart since Chart 12 born west of
    the Atlantic.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(43)
    place = Place(name="Chart 43", **record["place"])
    printed = longitudes(43)
    assert record["birth_data"]["utc_offset_hours"] == -5.0

    computed = compute_chart(from_local(**record["birth_data"]), place,
                             Settings(node_type=NodeType.MEAN))
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.01, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 0.1

    true_node = compute_chart(from_local(**record["birth_data"]), place,
                              Settings(node_type=NodeType.TRUE))
    assert abs(true_node.positions[int(Graha.RAHU)].longitude
               - printed["Rahu"]) * 60 > 80.0


def test_exercise_32_step_1_the_three_pairs_give_long_life():
    """"Using the method of three pairs, estimate whether he has short or
    middle or long life."

    Lagna lord Venus and the 8th lord — Table 32 sends Libra to Taurus, whose
    lord is also Venus — are both in Sagittarius, dual and dual, so middle.
    Moon in fixed Aquarius with Saturn in dual Gemini gives long, and lagna
    with HL, both movable, gives long. Two long dominate.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import rudra_eighth, three_pairs

    _longitudes, signs, lagna_sign, _al = _chart(43)
    assert lagna_sign == R["Libra"]
    assert rudra_eighth(R["Libra"]) == R["Taurus"]

    got = three_pairs(lagna_sign, signs, book_signs(43)["HL"])
    assert [p["category"] for p in got["pairs"]] == ["middle", "long", "long"]
    assert got["category"] == "long"
    assert tuple(got["range_years"]) == (72, 108)
    assert got["eighth_house"]["lord_used"] == "Venus"


def test_exercise_32_step_2_the_seventh_house_wins_the_seed():
    """Rule 1 ties — both Libra and Aries are empty — and rule 2 decides three
    to one: Jupiter reaches both from Aquarius, but Mercury reaches only
    Aries, and Aries' lord Mars aspects it from Leo while Libra's lord Venus
    does not reach Libra from Sagittarius.

    The second seed in the two chapters to go to the 7th, after Example 91,
    and the first that can be computed.
    """
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.shoola import progression

    longitudes, _signs, lagna_sign, _al = _chart(43)
    verdict = stronger(lagna_sign, (lagna_sign + 6) % 12, longitudes,
                       purpose="phalita")

    assert verdict.rules[0].winner is None
    assert verdict.winner == R["Aries"]
    assert verdict.decided_by == "2"
    assert "Libra count 1" in verdict.reason
    assert "Aries count 3" in verdict.reason

    run = progression(R["Aries"])
    assert [ABBR[s] for s in run.signs[:4]] == ["Ar", "Ta", "Ge", "Cn"]


def test_exercise_32_step_3_the_four_dasas_of_the_long_range():
    """"Identify the four dasas in the estimated longevity range."

    From Aries, positions 8 to 11 are Sagittarius, Capricorn, Aquarius and
    Pisces, running 72-81, 81-90, 90-99 and 99-108.
    """
    from hora.dasha.rasi.shoola import longevity_block, progression

    run = progression(R["Aries"])
    block = longevity_block("long")
    spans = [(ABBR[run.signs[p]], run.starts[p], run.starts[p] + 9)
             for p in block["positions"]]
    assert spans == [("Sg", 72, 81), ("Cp", 81, 90), ("Aq", 90, 99),
                     ("Pi", 99, 108)]


def test_exercise_32_step_4_two_of_the_four_are_reachable():
    """"Consider the trines from AL and the 3rd and 8th houses (using Table
    32)."

    AL is Aquarius, so its trines are Aq, Ge and Li; the 3rd is Aries and
    Table 32's 8th is Capricorn, where Rahu sits. Of the four long-life dasas
    only **Aquarius** and **Capricorn** are reached, so the exercise leaves a
    genuine choice.
    """
    from hora.charts.maraka import ordinary_eighth, rudra_eighth
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import select_dasa

    _longitudes, signs, lagna_sign, al = _chart(43)
    assert al == R["Aquarius"]
    assert rudra_eighth(al) == R["Capricorn"]
    assert ordinary_eighth(al) == R["Virgo"]
    assert signs[int(Graha.RAHU)] == R["Capricorn"]

    got = select_dasa(al, R["Aries"], "long", signs, lagna=lagna_sign)
    reachable = [c["rasi"] for c in got["can_kill"]]
    assert reachable == ["Capricorn", "Aquarius"]
    assert [c["rasi"] for c in got["trines_from_al"]] == ["Aquarius"]
    assert got["selected"]["rasi"] == "Aquarius"     # before criterion 1


def test_exercise_32_step_5_criterion_1_is_finally_needed():
    """"Think hard and choose the dasa that must have given death."

    This is the first chart in either chapter where §23.3's criterion 1 has
    work to do. The AK **is** Jupiter here, so its two shields are one planet,
    and that planet occupies Aquarius — which criterion 1 says usually does
    not kill. It is not Rudra (Venus is), so the exception does not rescue it.
    Capricorn is reached by neither shield.

    Our answer: **Capricorn**, the 8th from AL by Table 32, holding Rahu.
    """
    from hora.charts.book import GRAHA_OF, chart, graha_longitudes
    from hora.charts.maraka import rudra
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import protected_by

    _longitudes, signs, lagna_sign, _al = _chart(43)
    longitudes = {int(g): lon for g, lon in graha_longitudes(43).items()}
    karakas = chart(43)["chara_karakas"]
    ak = int(GRAHA_OF[next(n for n, r in karakas.items() if r == "AK")])
    assert ak == int(Graha.JUPITER)

    body = rudra(lagna_sign, signs, longitudes)
    assert body["rudra"] == "Venus"
    assert body["rudra_rasi"] == "Sagittarius"

    aquarius = protected_by(R["Aquarius"], signs, ak, rudra=int(Graha.VENUS))
    assert aquarius["protected"]
    assert {s["how"] for s in aquarius["shields"]} == {"occupies"}
    assert aquarius["rudra_cancels"] == ()

    capricorn = protected_by(R["Capricorn"], signs, ak, rudra=int(Graha.VENUS))
    assert not capricorn["protected"]
    assert capricorn["shields"] == ()


def test_exercise_32_the_demoted_trishoola_rule_points_elsewhere():
    """Rudra is Venus in Sagittarius, so the Trishoolas are Sg, Ar and Le —
    and **Sagittarius** is in the long-life block, at 72-81. §23.3 demoted
    that reading for Shoola dasa, and it reaches none of the AL rules, so the
    two readings disagree on this chart and the section says which wins.
    """
    from hora.charts.book import graha_longitudes
    from hora.charts.maraka import rudra
    from hora.dasha.rasi.shoola import (
        TRISHOOLA_IS_LESS_SIGNIFICANT_HERE,
        death_rasis,
    )

    _longitudes, signs, lagna_sign, al = _chart(43)
    longitudes = {int(g): lon for g, lon in graha_longitudes(43).items()}
    body = rudra(lagna_sign, signs, longitudes)
    spikes = {t["rasi"] for t in body["trishoola"]}
    assert spikes == {"Sagittarius", "Aries", "Leo"}

    reached = {row["rasi"] for row in death_rasis(al, signs, lagna=lagna_sign)}
    assert "Sagittarius" not in reached
    assert "less significant" in TRISHOOLA_IS_LESS_SIGNIFICANT_HERE


def test_exercise_32_answer_confirms_every_step():
    """The answer, against what we derived before seeing it. Long life, the
    Aries seed, the four dasas, the elimination of Aquarius by criterion 1 and
    the move to Capricorn — every step matches. Capricorn dasa runs 11
    December 1996 to 11 December 2005 on the 365.25-day year, and Frank
    Sinatra died on 14 May 1998.
    """
    import swisseph as swe

    from hora.charts.book import chart
    from hora.core.timeutil import from_local
    from hora.dasha.rasi.shoola import dasa_periods

    record = chart(43)
    birth = from_local(**record["birth_data"])
    offset = record["birth_data"]["utc_offset_hours"] / 24.0

    def local(jd):
        year, month, day, _hour = swe.revjul(jd + offset)
        return (int(year), int(month), int(day))

    rows = {row["rasi"]: row
            for row in dasa_periods(R["Aries"], birth.jd_ut)}
    capricorn = rows["Capricorn"]
    assert capricorn["position"] == 9
    assert local(capricorn["start_jd"]) == (1996, 12, 11)
    assert local(capricorn["end_jd"]) == (2005, 12, 11)

    answer = {
        "longevity": ("long", (72, 108)),
        "seed": ("Aries", "the 7th house, by §15.5.2 rule 2"),
        "four_dasas": ("Sagittarius", "Capricorn", "Aquarius", "Pisces"),
        "reachable": ("Capricorn", "Aquarius"),
        "chosen": "Capricorn",
        "why": ("the 8th from AL by Table 32, holding Rahu; Aquarius is a "
                "trine from AL but is occupied by the AK Jupiter, which "
                "criterion 1 shields and which is not Rudra"),
        "dates": ("11 December 1996", "11 December 2005"),
    }
    assert answer["chosen"] in answer["reachable"]
    assert answer["chosen"] in answer["four_dasas"]

    death = swe.julday(1998, 5, 14, 12.0)
    assert capricorn["start_jd"] <= death < capricorn["end_jd"]
    assert chart(43)["events"] == {
        "died of a heart attack": "May 14, 1998, aged 82"}


def test_the_answer_eliminates_aquarius_with_criterion_1():
    """"Its dasa can give death. **However, it contains Jupiter who is also
    AK. So its dasa is unlikely to kill.** We can try the 8th house from AL."

    The first place either chapter applies criterion 1 to remove a candidate,
    which closes half of OI-138: it is not a tiebreaker that never fires. Its
    hedge survives too — "unlikely", not "cannot".
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import SELECTION_CRITERIA, protected_by

    _longitudes, signs, _lagna, al = _chart(43)
    assert al == R["Aquarius"]
    assert signs[int(Graha.JUPITER)] == R["Aquarius"]

    got = protected_by(R["Aquarius"], signs, int(Graha.JUPITER),
                       rudra=int(Graha.VENUS))
    assert got["protected"]
    assert got["hedge"] == "usually"
    assert "Usually" in SELECTION_CRITERIA[0]
    # The shield occupies rather than aspects, so OI-138's other half stands.
    assert {s["how"] for s in got["shields"]} == {"occupies"}


def test_the_answer_reaches_capricorn_through_table_32_as_example_92_did():
    """"From Table 32, we find that Cp is the 8th house from Aq. It is
    afflicted by Rahu here (just as in Example 92)."

    The answer links the two itself, which is the second use of footnote 62's
    rule and the second time Rahu is what afflicts the house.
    """
    from hora.charts.maraka import ordinary_eighth, rudra_eighth
    from hora.dasha.rasi.shoola import death_rasis

    _longitudes, signs, lagna_sign, al = _chart(43)
    assert rudra_eighth(al) == R["Capricorn"]
    assert ordinary_eighth(al) == R["Virgo"]

    rows = {row["house_from_al"]: row
            for row in death_rasis(al, signs, lagna=lagna_sign)}
    assert rows[8]["rasi"] == "Capricorn"
    assert rows[8]["by"] == "Table 32"
    assert "Rahu" in rows[8]["occupied_by"]

    # Example 92's chart did the same, from a different AL.
    _l40, signs40, lagna40, al40 = _chart(40)
    other = {row["house_from_al"]: row
             for row in death_rasis(al40, signs40, lagna=lagna40)}
    assert "Rahu" in other[8]["occupied_by"]
    assert other[8]["by"] == "Table 32"


def test_the_answers_seed_grounds_name_the_sun_where_rule_2_names_jupiter():
    """"The 7th house Aries is stronger as it has the aspect of Sun, Mercury
    and its lord Mars."

    §15.5.2's rule 2 counts Jupiter, Mercury and the lord — and Jupiter does
    aspect Aries from Aquarius, so it is the Sun standing in Jupiter's place
    rather than an extra. Nothing turns on it here: Aries wins under rule 2 as
    printed, under a plain count of every aspecting graha, and under the ayur
    adaptation that leads with the luminaries.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.charts.rasi_strength import stronger
    from hora.core.const import GRAHA_NAMES, Graha
    from hora.dasha.rasi.shoola import (
        THE_SEED_GROUNDS_NAME_THE_SUN_WHERE_RULE_2_NAMES_JUPITER,
    )

    longitudes, signs, _lagna, _al = _chart(43)
    named = {int(Graha.SUN), int(Graha.MERCURY), int(Graha.MARS)}
    aspecting = {g for g, place in signs.items()
                 if R["Aries"] in rasi_drishti(place)}
    assert named < aspecting
    assert {str(GRAHA_NAMES[g]) for g in aspecting - named} == {"Moon",
                                                               "Jupiter"}

    verdict = stronger(R["Libra"], R["Aries"], longitudes, purpose="phalita")
    assert verdict.winner == R["Aries"]
    assert "Jupiter" in verdict.reason

    libra = {g for g, place in signs.items()
             if R["Libra"] in rasi_drishti(place)}
    assert len(aspecting) > len(libra)          # 5 to 3, counting everything
    assert "Sun, Mercury and its lord Mars" in (
        THE_SEED_GROUNDS_NAME_THE_SUN_WHERE_RULE_2_NAMES_JUPITER)


def test_the_answer_counts_the_year_of_death_the_way_90_and_91_do():
    """"He died in his 83rd year" for a native aged 82 — the year in progress,
    as Examples 90 and 91 count and Example 89 does not. Three to one now.
    """
    from hora.dasha.rasi.shoola import progression

    run = progression(R["Aries"])
    start, end = run.starts[9], run.starts[9] + run.years[9]
    assert (start, end) == (81, 90)
    for year in (82, 83):
        assert start <= year < end


# --------------------------------------------------------------------------
# §23.5 Death of near relatives
# --------------------------------------------------------------------------

def test_23_5_widens_the_scope_a_second_time():
    """"Shoola dasa shows Shiva's punishment. It shows misfortune, suffering
    and death."

    §23.1 gave death, diseases, suffering and death of relatives; §23.5 adds
    misfortune and names the whole thing Shiva's punishment.
    """
    from hora.dasha.rasi.shoola import SHIVAS_PUNISHMENT, SHOWS

    assert "misfortune" in SHIVAS_PUNISHMENT
    assert "misfortune" not in SHOWS
    assert "Shiva's punishment" in SHIVAS_PUNISHMENT
    assert "death of near relatives can also be timed" in SHIVAS_PUNISHMENT


def test_the_relative_seed_rule_is_23_2s_with_a_different_house():
    """"We treat the house that shows him/her as lagna... Shoola dasa starts
    from the stronger of that rasi and the 7th from it."

    §23.2's own rule is this one with the 1st house, which is why Dara Shoola
    dasa turns out to be the ordinary dasa.
    """
    from hora.dasha.rasi.shoola import (
        RELATIVE_DASAS,
        RELATIVE_SEED_RULE,
        SEED_RULE,
    )

    assert "the stronger of that rasi and the 7th from it" in (
        RELATIVE_SEED_RULE)
    assert SEED_RULE == "Find the stronger of lagna and the 7th house."

    for row in RELATIVE_DASAS:
        first, second = row["pair"]
        assert (second - first) % 12 == 6, row["name"]
        assert row["house"] == first


@pytest.mark.parametrize("name,means,pair", [
    ("Pitri Shoola dasa", "father", (9, 3)),
    ("Bhratri Shoola dasa", "brother", (3, 9)),
    ("Matri Shoola dasa", "mother", (4, 10)),
    ("Dara Shoola dasa", "wife", (7, 1)),
    ("Putra Shoola dasa", "son", (5, 11)),
])
def test_the_five_named_variants(name, means, pair):
    """§23.5's five, each with the house that shows the relative and the 7th
    from it. Named in Sanskrit with the gloss the section gives.
    """
    from hora.dasha.rasi.shoola import RELATIVE_DASAS, relative_dasa

    row = next(r for r in RELATIVE_DASAS if r["name"] == name)
    assert row["means"] == means
    assert row["pair"] == pair

    got = relative_dasa(name, R["Leo"])
    assert set(got["candidates"]) == set(pair)
    assert got["seed"] is None                # the comparison is OI-131's
    assert "see OI-131" in got["undecided"]


def test_pitri_and_bhratri_are_the_same_dasa_read_two_ways():
    """"Pitri Shoola dasa... starts from the stronger of 9th and 3rd houses"
    and "Bhratri Shoola dasa also starts from the stronger of 3rd and 9th
    houses".

    "Stronger of" is symmetric, so the two are one run. §23.5 prints them as
    separate entries and never says so; only the reading differs — the
    father's death against a younger sibling's.
    """
    from hora.dasha.rasi.shoola import (
        PITRI_AND_BHRATRI_ARE_ONE_DASA,
        relative_dasa,
    )

    for lagna in range(12):
        for house in (3, 9):
            pitri = relative_dasa("Pitri Shoola dasa", lagna,
                                  stronger_house=house)
            bhratri = relative_dasa("Bhratri Shoola dasa", lagna,
                                    stronger_house=house)
            assert pitri["seed"] == bhratri["seed"]
            assert pitri["run"].signs == bhratri["run"].signs

    assert "the same rasi and so the same twelve dasas" in (
        PITRI_AND_BHRATRI_ARE_ONE_DASA)


def test_dara_shoola_dasa_is_the_ordinary_one_and_the_book_says_so():
    """"(this dasa will be identical to the native's normal Shoola dasa)."

    The 7th and 1st are §23.2's own pair, so the wife's dasa and the native's
    are the same twelve periods.
    """
    from hora.dasha.rasi.shoola import (
        DARA_IS_THE_ORDINARY_SHOOLA_DASA,
        progression,
        relative_dasa,
        seed,
    )

    assert "identical to the native's normal Shoola dasa" in (
        DARA_IS_THE_ORDINARY_SHOOLA_DASA)

    for lagna in range(12):
        for house, sign in ((1, lagna), (7, (lagna + 6) % 12)):
            dara = relative_dasa("Dara Shoola dasa", lagna,
                                 stronger_house=house)
            ordinary = seed(lagna, stronger_house=house)
            assert dara["seed"] == ordinary.sign == sign
            assert dara["run"].signs == progression(sign).signs


def test_five_names_are_four_dasas():
    """The two identities together: Pitri and Bhratri share a pair, and Dara
    shares §23.2's. So §23.5's five names cover four distinct runs.
    """
    from hora.dasha.rasi.shoola import RELATIVE_DASAS

    pairs = {tuple(sorted(row["pair"])) for row in RELATIVE_DASAS}
    assert len(RELATIVE_DASAS) == 5
    assert pairs == {(1, 7), (3, 9), (4, 10), (5, 11)}
    assert len(pairs) == 4


def test_two_house_pairs_are_left_unnamed_and_matris_use_unstated():
    """Six pairs exist and §23.5 names four — nothing for the 2nd/8th or the
    6th/12th. And Matri Shoola dasa is the only variant with no "it shows..."
    clause; its use is left to its name.
    """
    from hora.dasha.rasi.shoola import (
        RELATIVE_DASAS,
        THE_UNNAMED_PAIRS_AND_THE_UNSTATED_USE,
    )

    every_pair = {tuple(sorted((h, (h + 5) % 12 + 1))) for h in range(1, 13)}
    named = {tuple(sorted(row["pair"])) for row in RELATIVE_DASAS}
    assert len(every_pair) == 6
    assert every_pair - named == {(2, 8), (6, 12)}

    without = [row["name"] for row in RELATIVE_DASAS if row["shows"] is None]
    assert without == ["Matri Shoola dasa"]
    assert "no stated reading" in THE_UNNAMED_PAIRS_AND_THE_UNSTATED_USE


def test_an_unknown_variant_or_house_is_refused():
    from hora.dasha.rasi.shoola import ShoolaError, relative_dasa

    with pytest.raises(ShoolaError, match="unknown variant"):
        relative_dasa("Guru Shoola dasa", R["Leo"])
    with pytest.raises(ShoolaError, match="must be one of"):
        relative_dasa("Matri Shoola dasa", R["Leo"], stronger_house=1)


def test_a_relative_is_read_from_the_sthira_karaka_not_from_al():
    """"When Shiva's force strikes trines from sthira karaka of father,
    father's death can take place. Trines from the corresponding arudha pada
    can also give death."

    Two references and both are trines. §23.3's 3rd and 8th houses do not
    appear for a relative, and AL is replaced by the karaka.
    """
    from hora.dasha.rasi.shoola import (
        DEATH_HOUSES_FROM_AL,
        RELATIVE_DEATH_RULE,
        relative_death_rasis,
    )

    assert "sthira karaka" in RELATIVE_DEATH_RULE
    assert "arudha pada" in RELATIVE_DEATH_RULE
    assert "3rd" not in RELATIVE_DEATH_RULE and "8th" not in (
        RELATIVE_DEATH_RULE)
    assert (3, 8) in [row["houses"] for row in DEATH_HOUSES_FROM_AL]

    got = relative_death_rasis(R["Aries"], R["Taurus"])
    assert got["names"]["from_sthira_karaka"] == (
        "Aries", "Leo", "Sagittarius")
    assert got["names"]["from_arudha_pada"] == ("Taurus", "Virgo", "Capricorn")
    assert len(got["all"]) == 6
    assert got["undecided"] is None


def test_the_arudha_pada_is_reported_missing_rather_than_dropped():
    """Half the rule needs a pada the caller may not have settled — the 3/9
    pair is shared by two variants, so "the corresponding arudha pada" is not
    self-evident there.
    """
    from hora.dasha.rasi.shoola import relative_death_rasis

    got = relative_death_rasis(R["Aries"])
    assert got["from_arudha_pada"] == ()
    assert "corresponding arudha pada was not given" in got["undecided"]
    assert got["all"] == tuple(sorted(got["from_sthira_karaka"]))


def test_23_5_points_back_to_8_3_for_the_karakas():
    """"We mentioned earlier that sthira karakas are useful in timing death."

    §8.3 said it, and said more than §23.5 recalls — which graha to take for a
    spouse depends on the native's sex. Father and mother are each a *pair*
    there, so those two readings need a strength comparison of their own.
    """
    from hora.core.constants.karaka import (
        STHIRA_KARAKA_OF_SPOUSE,
        STHIRA_KARAKAS,
    )
    from hora.dasha.rasi.shoola import (
        RELATIVE_DASAS,
        STHIRA_KARAKAS_WERE_PROMISED_FOR_DEATH,
    )

    assert "death of spouse" in STHIRA_KARAKAS_WERE_PROMISED_FOR_DEATH
    assert set(STHIRA_KARAKA_OF_SPOUSE) == {"male", "female"}

    by_relative = {row["relative"]: row for row in STHIRA_KARAKAS}
    for row in RELATIVE_DASAS:
        assert row["sthira_karaka"] in by_relative, row["name"]

    assert by_relative["father"]["rule"] == "stronger"
    assert by_relative["mother"]["rule"] == "stronger"
    assert len(by_relative["father"]["grahas"]) == 2


# --------------------------------------------------------------------------
# Example 93 — the only worked Pitri Shoola dasa.
# --------------------------------------------------------------------------

def test_chart_44_recomputes_and_is_the_narrowest_mean_node_margin():
    """Every body inside one arcminute. Rahu is only 9' out under `true` here
    — still mean by an order of magnitude, but the narrowest separating margin
    in the register, the nodes having been near-coincident in May 1971.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(44)
    place = Place(name="Chart 44", **record["place"])
    printed = longitudes(44)

    computed = compute_chart(from_local(**record["birth_data"]), place,
                             Settings(node_type=NodeType.MEAN))
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"

    true_node = compute_chart(from_local(**record["birth_data"]), place,
                              Settings(node_type=NodeType.TRUE))
    error = abs(true_node.positions[int(Graha.RAHU)].longitude
                - printed["Rahu"]) * 60
    assert 5.0 < error < 15.0


def test_three_charts_now_share_the_same_birthplace():
    """Charts 40, 41 and 44 are all 81 E 12, 16 N 15 — worth pinning, since a
    transposed coordinate would break three examples at once.
    """
    from hora.charts.book import chart

    places = {n: chart(n)["place"] for n in (40, 41, 44)}
    assert places[40] == places[41] == places[44]


def test_example_93_settles_the_father_karaka_with_8_3s_pair():
    """"Exalted Sun joins Mercury and Jupiter aspects him. So Sun is stronger
    than Venus. He becomes sthira pitri karaka."

    All three grounds check out — the Sun is exalted in Aries, Mercury is with
    him, and Jupiter's Scorpio rasi-aspects Aries. What the example does not
    say is that **Venus is exalted too**, in Pisces; the Sun wins on the other
    two, not on dignity.
    """
    from hora.charts.book import graha_longitudes, graha_signs
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import paired_sthira_karaka

    longitudes = {int(g): lon for g, lon in graha_longitudes(44).items()}
    signs = {int(g): sign for g, sign in graha_signs(44).items()}
    got = paired_sthira_karaka("father", longitudes, signs)

    sun, venus = got["candidates"]
    assert sun["graha_name"] == "Sun" and venus["graha_name"] == "Venus"
    assert sun["dignity"] == venus["dignity"] == "exalted"
    assert sun["joins"] == ("Mercury",)
    assert sun["rasi_aspected_by"] == ("Jupiter",)
    assert venus["joins"] == () and venus["rasi_aspected_by"] == ()
    assert got["undecided"].startswith("which of Sun and Venus")

    settled = paired_sthira_karaka("father", longitudes, signs,
                                   stronger=int(Graha.SUN))
    assert settled["karaka"]["rasi"] == "Aries"
    assert settled["undecided"] is None


def test_a_single_karaka_relative_is_refused_by_the_pair_helper():
    """§8.3 gives a pair only for father and mother; the rest are fixed."""
    from hora.charts.book import graha_longitudes, graha_signs
    from hora.dasha.rasi.shoola import ShoolaError, paired_sthira_karaka

    longitudes = {int(g): lon for g, lon in graha_longitudes(44).items()}
    signs = {int(g): sign for g, sign in graha_signs(44).items()}
    with pytest.raises(ShoolaError, match="single sthira karaka"):
        paired_sthira_karaka("wife", longitudes, signs)


def test_example_93_names_a9_as_the_corresponding_arudha_pada():
    """"Pitri pada (A9, arudha pada of 9th house) is in Sg."

    That settles what "the corresponding arudha pada" means for a variant
    whose pair holds two houses: the **9th**, which shows the father, not the
    3rd that Pitri Shoola dasa's pair also contains.
    """
    from hora.charts.arudha import arudha_pada
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.charts.colord import stronger
    from hora.dasha.rasi.shoola import PITRI_PADA_IS_A9, RELATIVE_DASAS

    longitudes = {int(g): lon for g, lon in graha_longitudes(44).items()}
    signs = {int(g): sign for g, sign in graha_signs(44).items()}
    lagna_sign = lagna(44)
    overrides = {r: stronger(r, longitudes, purpose="arudha").winner
                 for r in (7, 10)}

    assert lagna_sign == R["Gemini"]
    assert arudha_pada(9, lagna_sign, signs, overrides).sign == (
        R["Sagittarius"])
    assert "A9, arudha pada of 9th house" in PITRI_PADA_IS_A9

    pitri = next(r for r in RELATIVE_DASAS if r["name"] == "Pitri Shoola dasa")
    assert pitri["house"] == 9
    assert 3 in pitri["pair"]              # the other half, and not the pada


def test_example_93s_two_references_give_the_same_three_rasis():
    """"Death can occur in trines from him, i.e. Ar, Le and Sg. ... Trines
    from it are the same."

    The Sun is in Aries and A9 in Sagittarius, which are trines of each other,
    so both halves of §23.5's reading land on one set.
    """
    from hora.charts.book import graha_signs
    from hora.core.const import Graha
    from hora.dasha.rasi.shoola import relative_death_rasis

    signs = {int(g): sign for g, sign in graha_signs(44).items()}
    assert signs[int(Graha.SUN)] == R["Aries"]

    got = relative_death_rasis(R["Aries"], R["Sagittarius"])
    assert set(got["names"]["from_sthira_karaka"]) == {
        "Aries", "Leo", "Sagittarius"}
    assert set(got["names"]["from_arudha_pada"]) == set(
        got["names"]["from_sthira_karaka"])
    assert len(got["all"]) == 3
    assert got["undecided"] is None


def test_example_93s_dates_come_out_of_an_aquarius_seed():
    """"Dasa of Aq runs during 1971-1980. Dasa of Pi runs during 1980-1989.
    Dasa of Ar runs during 1989-1998."

    Born May 1971, nine years each, always zodiacal — and the father died in
    the second half of 1995, inside Aries.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.shoola import progression, relative_dasa

    got = relative_dasa("Pitri Shoola dasa", R["Gemini"], stronger_house=9)
    assert got["seed_rasi"] == "Aquarius"

    run = progression(R["Aquarius"])
    assert [ABBR[s] for s in run.signs[:3]] == ["Aq", "Pi", "Ar"]
    born = chart(44)["birth_data"]["year"]
    assert [(born + run.starts[i], born + run.starts[i] + 9)
            for i in range(3)] == [(1971, 1980), (1980, 1989), (1989, 1998)]
    assert run.starts[2] <= 1995 - born < run.starts[2] + 9


def test_the_cascade_seeds_the_other_house_and_the_reading_collapses():
    """D-66. Example 93 reaches §15.5.2 **rule 4** — "its lord Rahu is in a
    rasi with a different oddity" — but **rule 2 comes first and decides**:
    Mercury reaches both from Aries, and Leo's lord the Sun reaches Leo while
    Aquarius' lord Rahu, in adjacent Capricorn, does not reach Aquarius.

    Seeding from Leo puts the father's death in **Libra**, which is a trine
    from neither the karaka nor A9 — so the example would have nothing to say.
    """
    from hora.charts.book import graha_longitudes
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.shoola import progression

    longitudes = {int(g): lon for g, lon in graha_longitudes(44).items()}
    verdict = stronger(R["Aquarius"], R["Leo"], longitudes, purpose="phalita")

    assert verdict.winner == R["Leo"]
    assert verdict.decided_by == "2"
    assert "Aquarius count 1" in verdict.reason
    assert "Leo count 2" in verdict.reason

    # The cascade stops at rule 2, so rule 4 is never evaluated at all.
    assert [r.rule for r in verdict.rules] == ["1", "2"]

    counterfactual = progression(R["Leo"])
    at_24 = [ABBR[s] for s, start in zip(counterfactual.signs,
                                         counterfactual.starts, strict=True)
             if start <= 24 < start + 9]
    assert at_24 == ["Li"]
    assert R["Libra"] not in {(R["Aries"] + k) % 12 for k in (0, 4, 8)}


def test_rule_4_would_favour_aquarius_under_either_co_lord():
    """The book's own reason holds whichever way OI-135 goes: Saturn is in
    Taurus and Rahu in Capricorn, both even against an odd Aquarius, while
    Leo's lord the Sun is in odd Aries. So D-66 is about the cascade's order,
    not about which lord Aquarius has.
    """
    from hora.charts.book import graha_longitudes, graha_signs
    from hora.charts.colord import stronger as stronger_co_lord
    from hora.core.const import RASI_IS_ODD, Graha

    longitudes = {int(g): lon for g, lon in graha_longitudes(44).items()}
    signs = {int(g): sign for g, sign in graha_signs(44).items()}

    assert stronger_co_lord(R["Aquarius"], longitudes,
                            purpose="arudha").winner == int(Graha.RAHU)
    assert RASI_IS_ODD[R["Aquarius"]]
    for lord in (int(Graha.SATURN), int(Graha.RAHU)):
        assert not RASI_IS_ODD[signs[lord]]
    assert RASI_IS_ODD[signs[int(Graha.SUN)]]          # Leo's lord, same odd


def test_23_5_leaves_a_relatives_three_trines_unnarrowed():
    """§23.3 cuts the native's answer to four dasas by longevity category;
    §23.5 gives a relative no equivalent. Example 93's three trines run at
    18-27, 54-63 and 90-99, and it simply reports which held the death.
    """
    from hora.dasha.rasi.shoola import (
        NO_CRITERION_NARROWS_A_RELATIVES_TRINES,
        progression,
        relative_death_rasis,
    )

    run = progression(R["Aquarius"])
    trines = relative_death_rasis(R["Aries"], R["Sagittarius"])["all"]
    spans = {ABBR[run.signs[i]]: (run.starts[i], run.starts[i] + 9)
             for i in range(12) if run.signs[i] in trines}
    assert spans == {"Ar": (18, 27), "Le": (54, 63), "Sg": (90, 99)}
    assert "names no way to choose" in NO_CRITERION_NARROWS_A_RELATIVES_TRINES
