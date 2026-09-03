"""Chapter 22 — Niryaana Shoola dasa.

The seventh of Part 2's nine and the first **ayur** rasi dasa. What is tested
here is the part that is its own: a seed pair no earlier dasa uses, lengths
that read nothing but the modality, and an interpretation that leans on
chapter 14's marakas and Rudra rather than on anything in this chapter.
"""
from __future__ import annotations

import pytest

from hora.core.const import RASI_NAMES

R = {name: i for i, name in enumerate(RASI_NAMES)}
ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


# --------------------------------------------------------------------------
# §22.1 Introduction
# --------------------------------------------------------------------------

def test_the_name_is_two_words_of_the_rule():
    """"Niryaana means death and shoola is a weapon of Lord Shiva, who is the
    lord of destruction."

    Part 2's map gives its purpose as "ayur"; this is the sentence behind it,
    and the first rasi dasa in the book with that purpose.
    """
    from hora.core.constants.dasha import PART_2_DASA_SYSTEMS
    from hora.dasha.rasi.niryaana_shoola import (
        NIRYAANA_MEANS_DEATH,
        ONE_OF_THE_MOST_RELIABLE,
    )

    assert "Niryaana means death" in NIRYAANA_MEANS_DEATH
    assert "timing of death" in ONE_OF_THE_MOST_RELIABLE

    by_name = {s["name"]: s for s in PART_2_DASA_SYSTEMS}
    assert by_name["Niryaana Shoola dasa"]["purpose"] == "ayur"
    assert by_name["Niryaana Shoola dasa"]["kind"] == "rasi"

    earlier = ("Narayana dasa", "Lagna Kendradi Rasi dasa", "Sudasa",
               "Drigdasa")
    assert all(by_name[n]["purpose"].startswith("phalita") for n in earlier)


def test_the_chapter_renames_the_dasa_to_avoid_a_collision():
    """"Parasara simply called it 'Shoola dasa', but some scholars use the
    name Shoola dasa to denote a different dasa."

    Footnote 59 names the scholars, and it is the author's own guru — so the
    rename is not a dismissal of the other usage. Both systems stay in Part 2's
    map, and only this one is built.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        NAMES,
        THE_NAME_IS_DISAMBIGUATED,
        THE_OTHER_SHOOLA_DASAS_SCHOLARS,
    )

    assert NAMES[0] == "Shoola dasa"             # what Parasara called it
    assert NAMES[1] == "Niryaana Shoola dasa"    # what this chapter calls it
    assert "avoid confusion" in THE_NAME_IS_DISAMBIGUATED
    assert "Sanjay Rath" in THE_OTHER_SHOOLA_DASAS_SCHOLARS


# --------------------------------------------------------------------------
# §22.2.1 Computation — the seed
# --------------------------------------------------------------------------

def test_the_seed_pair_is_the_2nd_and_8th_not_the_maraka_pair():
    """"Find the stronger of the 2nd and 8th houses."

    §14.2's maraka sthanas are the 2nd and the **7th**. The two pairs share
    only the 2nd, and this chapter uses both — the 2nd/8th to start the
    sequence and the 2nd/7th to read it. Nor is it chapter 18's lagna and 7th
    or chapter 20's Sree Lagna.
    """
    from hora.charts.maraka import maraka_houses
    from hora.dasha.rasi.niryaana_shoola import (
        SEED_PAIR_IS_NOT_THE_MARAKA_PAIR,
        SEED_RULE,
        seed,
    )

    assert maraka_houses() == (2, 7)
    assert "2nd and 8th houses" in SEED_RULE
    assert "share only the 2nd" in SEED_PAIR_IS_NOT_THE_MARAKA_PAIR

    got = seed(R["Aries"])
    assert (got.second_name, got.eighth_name) == ("Taurus", "Scorpio")


@pytest.mark.parametrize("lagna", range(12))
def test_the_two_seed_candidates_are_always_distinct_and_never_lagna(lagna):
    """The 2nd and the 8th are six apart, so no chart can collapse the choice
    — unlike chapter 18's lagna/7th, which §15.5.2 must always decide.
    """
    from hora.dasha.rasi.niryaana_shoola import seed

    got = seed(lagna)
    assert got.second != got.eighth
    assert lagna not in (got.second, got.eighth)
    assert (got.eighth - got.second) % 12 == 6


def test_the_seed_comparison_is_one_15_5_2_refuses_to_make():
    """§15.5.2's warning names ayur dasas as a purpose whose rule 2 reads the
    luminaries, and does not say how to weigh the other aspects. This is the
    first system that actually needs that purpose, so the refusal stops being
    theoretical. See OI-131.
    """
    from hora.charts.rasi_strength import (
        PURPOSE_ADAPTATIONS,
        RasiStrengthError,
        stronger,
    )
    from hora.dasha.rasi.niryaana_shoola import seed

    ayur = PURPOSE_ADAPTATIONS["ayur"]
    assert ayur["applies_to"] == "dasas that show longevity"
    assert not ayur["implemented"]
    assert "luminaries" in ayur["rule_2_planets"]

    with pytest.raises(RasiStrengthError, match="not implemented"):
        stronger(R["Taurus"], R["Scorpio"], {}, purpose="ayur")

    got = seed(R["Aries"])
    assert got.sign is None
    assert "ayur dasa" in got.undecided
    assert "OI-131" in got.undecided


def test_a_caller_can_settle_the_seed_but_must_say_which_house():
    """Reported open, not guessed — and once the caller decides, the answer
    says it was the caller who did.
    """
    from hora.dasha.rasi.niryaana_shoola import NiryaanaShoolaError, seed

    second = seed(R["Aries"], stronger_house=2)
    assert (second.sign, second.sign_name) == (R["Taurus"], "Taurus")
    assert second.undecided is None
    assert "the caller made" in second.why

    eighth = seed(R["Aries"], stronger_house=8)
    assert eighth.sign == R["Scorpio"]

    with pytest.raises(NiryaanaShoolaError, match="must be 2 or 8"):
        seed(R["Aries"], stronger_house=7)


# --------------------------------------------------------------------------
# §22.2.1 Computation — direction, lengths, sequence
# --------------------------------------------------------------------------

def test_the_direction_is_the_odd_even_sign_test_not_odd_footed():
    """"If the rasi is odd, go in the forward (zodiacal) direction... If the
    rasi is even, go in the backward (anti-zodiacal) direction."

    Chapters 19 and 20 use this test and chapter 21 uses odd-**footed**. The
    two disagree on Taurus, Leo, Scorpio and Aquarius, which is a third of
    all charts.
    """
    from hora.core.const import RASI_IS_ODD, RASI_IS_ODD_FOOTED
    from hora.dasha.rasi.drigdasa import direction_of as footed
    from hora.dasha.rasi.niryaana_shoola import direction_of

    differ = [ABBR[s] for s in range(12)
              if bool(RASI_IS_ODD[s]) != bool(RASI_IS_ODD_FOOTED[s])]
    assert differ == ["Ta", "Le", "Sc", "Aq"]

    for name in differ:
        sign = ABBR.index(name)
        assert direction_of(sign) != footed(sign)

    assert direction_of(R["Aries"]) == "forward"
    assert direction_of(R["Taurus"]) == "backward"


@pytest.mark.parametrize("modality,years,members", [
    ("chara", 7, ["Ar", "Cn", "Li", "Cp"]),
    ("sthira", 8, ["Ta", "Le", "Sc", "Aq"]),
    ("dwiswabhava", 9, ["Ge", "Vi", "Sg", "Pi"]),
])
def test_lengths_come_from_the_modality_alone(modality, years, members):
    """"Dasas of movable, fixed and dual rasis have 7, 8 and 9 years
    respectively."

    §18.2.2 is not used at all here — no lord, no dignity, no exceptions. A
    Niryaana Shoola length is the same on every chart ever cast, which is why
    `dasa_years` takes nothing but the rasi.
    """
    from hora.core.const import MODALITY_NAMES, RASI_MODALITY
    from hora.dasha.rasi.niryaana_shoola import MODALITY_YEARS, dasa_years

    assert MODALITY_YEARS[modality] == years
    for abbr in members:
        sign = ABBR.index(abbr)
        assert str(MODALITY_NAMES[RASI_MODALITY[sign]]) == modality
        assert dasa_years(sign) == years


def test_the_cycle_is_96_years_on_every_chart():
    """Four rasis of each modality, so 4 * (7 + 8 + 9). Narayana's twelve vary
    chart to chart and can total anything; these never move.
    """
    from hora.dasha.rasi.niryaana_shoola import cycle_years, progression

    assert cycle_years() == 4 * (7 + 8 + 9) == 96
    for lagna in range(12):
        assert sum(progression(lagna).years) == 96


def test_the_lengths_are_shared_with_two_systems_the_book_names():
    """Footnote 60: "Sthira dasa, Mandooka dasa etc also use the same dasa
    years, though dasa sequences are different under those dasa systems."

    So the years are not this dasa's signature — the sequence is. Mandooka
    dasa was already named in chapter 19, where §19.3's gati naming was
    misattributed to it.
    """
    from hora.dasha.rasi.kendradi import MANDOOKA_DASA_MISATTRIBUTION
    from hora.dasha.rasi.niryaana_shoola import SHARED_DASA_YEARS

    assert "Sthira dasa, Mandooka dasa" in SHARED_DASA_YEARS
    assert "sequences are different" in SHARED_DASA_YEARS
    assert "Mandooka" in MANDOOKA_DASA_MISATTRIBUTION


@pytest.mark.parametrize("seed_sign", range(12))
def test_every_run_is_twelve_distinct_rasis(seed_sign):
    """"cover the 12 rasis", said of each direction. One plain sequence, so
    chapter 21's OI-127 — groups that do not partition the zodiac — has no
    analogue here.
    """
    from hora.dasha.rasi.niryaana_shoola import progression

    got = progression(seed_sign)
    assert len(set(got.signs)) == 12
    assert got.signs[0] == seed_sign
    assert got.starts[0] == 0
    assert got.starts[-1] + got.years[-1] == 96


def test_a_backward_run_reads_as_the_section_describes_it():
    """Taurus is an even sign, so its run is anti-zodiacal: Ta, Ar, Pi, Aq...
    and the lengths follow the rasis, not the positions.
    """
    from hora.dasha.rasi.niryaana_shoola import progression

    got = progression(R["Taurus"])
    assert got.direction == "backward"
    assert [ABBR[s] for s in got.signs[:4]] == ["Ta", "Ar", "Pi", "Aq"]
    assert got.years[:4] == (8, 7, 9, 8)
    assert "even sign" in got.why


def test_the_antardasa_rule_is_the_authors_and_says_so():
    """"Classics are not clear about how we go about finding antardasas. This
    author suggests using the same rules used for Narayana dasa."

    docs/precedence.md ranks the book above BPHS, but this sentence puts
    itself below both by admitting there is nothing to be above. Tagged rather
    than merged into chapter 18's rule, so a caller can tell the two apart.
    """
    from hora.dasha.rasi.narayana import antardasas
    from hora.dasha.rasi.niryaana_shoola import (
        ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION,
    )

    assert "Classics are not clear" in ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION
    assert "This author suggests" in ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION
    assert antardasas.__doc__ is not None      # the rules being borrowed


# --------------------------------------------------------------------------
# §22.2.2 Interpretation
# --------------------------------------------------------------------------

def test_the_three_death_readings_and_that_the_third_is_a_fallback():
    """Marakas, then the Trishoolas, then Rudra — and the third opens "If
    Trishoolas don't bring death", so it is explicitly the second's fallback
    rather than a fourth independent test.
    """
    from hora.dasha.rasi.niryaana_shoola import DEATH_READINGS

    assert [r["rule"] for r in DEATH_READINGS] == [1, 2, 3]
    assert [r["reads"] for r in DEATH_READINGS] == [
        "marakas", "Trishoola", "Rudra"]
    assert DEATH_READINGS[2]["text"].startswith("If Trishoolas don't")
    assert all(r["needs"] for r in DEATH_READINGS)


def test_rule_1_reports_marakas_without_ranking_them():
    """"Dasa of strong maraka rasis and dasas of rasis containing strong
    maraka grahas can bring death."

    §14.2 gives no ranking and says so, so "strong" is reported unjudged. An
    Aries lagna puts the 2nd in Taurus and the 7th in Libra.
    """
    from hora.core.const import Graha
    from hora.core.constants.maraka import MARAKA_STRONGER_NOT_A_RULE
    from hora.dasha.rasi.niryaana_shoola import maraka_readings

    signs = {int(Graha.VENUS): R["Taurus"], int(Graha.MARS): R["Aries"]}

    taurus = maraka_readings(R["Taurus"], R["Aries"], signs)
    assert taurus["is_maraka_sthana"] == (2,)
    assert taurus["applies"]
    assert "ranks none" in taurus["undecided"]
    # Venus owns both maraka houses here and sits in the 2nd.
    assert [e["graha_name"] for e in taurus["holds_maraka_grahas"]] == ["Venus"]

    gemini = maraka_readings(R["Gemini"], R["Aries"], signs)
    assert gemini["is_maraka_sthana"] == ()
    assert not gemini["applies"]
    assert gemini["undecided"] is None
    assert "do not order them" in MARAKA_STRONGER_NOT_A_RULE


def test_rule_2_is_the_other_half_of_14_3s_sentence():
    """§14.3 already said one of the three Trishoolas "kills the native during
    its Shoola dasa" — a forward reference to this chapter, eight chapters
    early. §22.2.2 is the half that says which dasa system that is.
    """
    from hora.core.constants.maraka import TRISHOOLA_RULE
    from hora.dasha.rasi.niryaana_shoola import (
        DEATH_READINGS,
        TRISHOOLA_WAS_PROMISED_IN_14_3,
    )

    assert "Shoola dasa" in TRISHOOLA_RULE
    assert TRISHOOLA_WAS_PROMISED_IN_14_3 in TRISHOOLA_RULE
    assert "Trishoola rasi" in DEATH_READINGS[1]["text"]


def test_which_trishoola_the_longevity_category_takes_is_never_said():
    """Both sections make the category choose and neither says which takes
    which. The category is carried through and not used. See OI-132.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        WHICH_TRISHOOLA_IS_NOT_MAPPED,
        NiryaanaShoolaError,
        trishoola_readings,
    )

    # Rudra in Aries: the trines are Aries, Leo, Sagittarius.
    got = trishoola_readings(R["Leo"], R["Aries"], longevity="middle")
    assert got["trishoola_names"] == ("Aries", "Leo", "Sagittarius")
    assert got["applies"] and got["position"] == 1
    assert got["longevity"] == "middle"
    assert got["undecided"] == WHICH_TRISHOOLA_IS_NOT_MAPPED

    outside = trishoola_readings(R["Taurus"], R["Aries"])
    assert not outside["applies"] and outside["position"] is None

    with pytest.raises(NiryaanaShoolaError, match="longevity must be"):
        trishoola_readings(R["Leo"], R["Aries"], longevity="very long")


def test_the_trishoolas_are_the_trines_from_rudras_rasi():
    """Chapter 14's own function, reused rather than re-derived — one
    definition of the three, so the two chapters cannot drift.
    """
    from hora.charts.maraka import trishoola_rasis
    from hora.dasha.rasi.niryaana_shoola import trishoola_readings

    for rudra in range(12):
        assert trishoola_readings(0, rudra)["trishoolas"] == trishoola_rasis(
            rudra)


def test_rule_3s_sentence_has_two_readings_and_one_that_is_ruled_out():
    """"If Trishoolas don't bring death, the rasi containing Rudra in the 12th
    house can bring death."

    The premise does real work: Rudra's own rasi is the first Trishoola, so a
    reading that returns it is excluded by the sentence's own opening clause,
    not by preference. See OI-130.
    """
    from hora.dasha.rasi.niryaana_shoola import rudra_fallback

    got = rudra_fallback(R["Aries"], lagna=R["Cancer"])
    readings = {r["reading"]: r for r in got["readings"]}
    assert len(readings) == 2

    from_rudra = readings["the 12th from the rasi containing Rudra"]
    assert from_rudra["rasi"] == "Pisces"
    assert not from_rudra["is_a_trishoola"]

    from_lagna = readings["the 12th house from lagna"]
    assert from_lagna["rasi"] == "Gemini"

    assert got["ruled_out"]["rasi"] == "Aries"
    assert "first Trishoola" in got["ruled_out"]["why"]
    assert "OI-130" in got["undecided"]


@pytest.mark.parametrize("rudra", range(12))
def test_the_12th_from_rudra_is_never_a_trishoola(rudra):
    """Why one reading always answers the case the sentence is about, and the
    other only sometimes does.
    """
    from hora.charts.maraka import trishoola_rasis
    from hora.dasha.rasi.niryaana_shoola import rudra_fallback

    got = rudra_fallback(rudra, lagna=0)
    from_rudra = got["readings"][0]
    assert from_rudra["sign"] not in trishoola_rasis(rudra)
    assert (rudra - from_rudra["sign"]) % 12 == 1


def test_the_12th_from_lagna_can_be_a_trishoola_and_is_flagged_when_it_is():
    """Rudra in Leo and a Sagittarius lagna: the 12th from lagna is Scorpio,
    which is not a trine from Leo. Move Rudra to Capricorn and it is — and the
    reading then hands back a rasi the premise excluded.
    """
    from hora.dasha.rasi.niryaana_shoola import rudra_fallback

    clear = rudra_fallback(R["Leo"], lagna=R["Sagittarius"])["readings"][1]
    assert clear["rasi"] == "Scorpio"
    assert not clear["is_a_trishoola"]

    clash = rudra_fallback(R["Capricorn"], lagna=R["Sagittarius"])["readings"][1]
    assert clash["rasi"] == "Scorpio"
    assert not clash["is_a_trishoola"]

    hit = rudra_fallback(R["Cancer"], lagna=R["Sagittarius"])["readings"][1]
    assert hit["rasi"] == "Scorpio"
    assert hit["is_a_trishoola"]
    assert "is on this chart" in hit["note"]


# --------------------------------------------------------------------------
# §22.2.2 — the antardasa at death, and the section's own illustration
# --------------------------------------------------------------------------

def test_the_sections_worked_illustration_reproduces_exactly():
    """"Suppose dasa rasi at death is Ta and Jupiter is in Le in navamsa. Then
    the antardasas of the 6th, 7th, 8th and 12th houses from Ta (i.e. Li, Sc,
    Sg and Ar) can bring death. Also the antardasas of Ar, Le, Li and Cp —
    rasis that aspect Le, which contains Jupiter in navamsa — can bring
    death."

    Both lists, and the 8th lord the example leaves the reader to find: the
    8th from Taurus is Sagittarius, whose lord is Jupiter.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Taurus"], {int(Graha.JUPITER): R["Leo"]})

    assert got["eighth_name"] == "Sagittarius"
    assert got["eighth_lord_name"] == "Jupiter"
    assert got["navamsa_rasi"] == "Leo"
    assert list(got["from_dasa_rasi_names"]) == [
        "Libra", "Scorpio", "Sagittarius", "Aries"]
    assert set(got["aspecting_names"]) == {"Aries", "Leo", "Libra",
                                           "Capricorn"}


def test_the_intersection_is_the_strong_candidate():
    """"If there is a common rasi between these two principles, it can be a
    strong candidate." The section does not work it out; on its own example
    there are two.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Taurus"], {int(Graha.JUPITER): R["Leo"]})
    assert set(got["strong_candidate_names"]) == {"Libra", "Aries"}
    assert set(got["strong_candidates"]) == (
        set(got["from_dasa_rasi"]) & set(got["aspecting_the_navamsa_rasi"]))


def test_rasis_that_aspect_a_rasi_include_it_in_both_chapters():
    """The section lists "Ar, Le, Li and Cp" as "rasis that aspect Le", though
    no rasi aspects itself under rasi drishti. Example 80 used the same idiom —
    "the signs that aspect Ge... Ge, Vi, Sg and Pi". So the phrase means the
    rasi together with those that aspect it, in chapter 21 and here alike.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import Graha
    from hora.dasha.rasi.drigdasa import group_signs
    from hora.dasha.rasi.niryaana_shoola import (
        ASPECTING_INCLUDES_THE_RASI_ITSELF,
        antardasa_candidates,
    )

    assert R["Leo"] not in rasi_drishti(R["Leo"])
    got = antardasa_candidates(R["Taurus"], {int(Graha.JUPITER): R["Leo"]})
    assert got["aspecting_the_navamsa_rasi"][0] == R["Leo"]

    assert group_signs(R["Gemini"], "forward")[0] == R["Gemini"]
    assert "Ar, Le, Li and Cp" in ASPECTING_INCLUDES_THE_RASI_ITSELF


def test_rasi_drishti_is_mutual_so_the_two_directions_agree():
    """"A rasi that aspects the rasi that... contains the owner" is the
    preimage; `rasi_drishti` gives the image. They coincide because rasi
    drishti is mutual, which is worth pinning rather than assuming.
    """
    from hora.charts.aspects import rasi_drishti

    for sign in range(12):
        preimage = {s for s in range(12) if sign in rasi_drishti(s)}
        assert preimage == set(rasi_drishti(sign))


def test_a_co_owned_8th_is_refused_rather_than_guessed():
    """The 8th from Aries is Scorpio and the 8th from Cancer is Aquarius, both
    of which §15.5.1 must settle. Refused the way `varga_lagna` refuses, not
    resolved to the sole classical lord.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import (
        NiryaanaShoolaError,
        antardasa_candidates,
    )

    navamsa = {int(g): 0 for g in range(9)}

    with pytest.raises(NiryaanaShoolaError, match="Scorpio"):
        antardasa_candidates(R["Aries"], navamsa)
    with pytest.raises(NiryaanaShoolaError, match="Aquarius"):
        antardasa_candidates(R["Cancer"], navamsa)

    settled = antardasa_candidates(R["Aries"], navamsa,
                                   eighth_lord=int(Graha.KETU))
    assert settled["eighth_lord_name"] == "Ketu"
    assert settled["navamsa_rasi"] == "Aries"


def test_a_missing_navamsa_position_is_named_not_silently_dropped():
    """The rule reads exactly one navamsa position; if it is absent the answer
    says whose it was.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        NiryaanaShoolaError,
        antardasa_candidates,
    )

    with pytest.raises(NiryaanaShoolaError, match="Jupiter"):
        antardasa_candidates(R["Taurus"], {})
