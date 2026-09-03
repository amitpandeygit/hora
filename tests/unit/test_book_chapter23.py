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
    assert [ABBR[row["sign"]] for row in got] == ["Cn", "Sc", "Pi", "Vi", "Aq"]
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
