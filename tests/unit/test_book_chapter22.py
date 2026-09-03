"""Chapter 22 — Niryaana Shoola dasa.

The seventh of Part 2's nine and the first **ayur** rasi dasa. What is tested
here is the part that is its own: a seed pair no earlier dasa uses, lengths
that read nothing but the modality, and an interpretation that leans on
chapter 14's marakas and Rudra rather than on anything in this chapter.
"""
from __future__ import annotations

import pathlib

import pytest

from hora.core.const import RASI_NAMES

OPEN_ITEMS = pathlib.Path(__file__).resolve().parents[2] / "docs" / "open-items.md"

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


def test_whether_a_dasa_rasi_is_a_trishoola_is_separate_from_which_one():
    """§22.2.2 asks two things of the Trishoolas — is this dasa rasi one of
    them, and which of the three the longevity category takes. The first needs
    only Rudra; the second needs the dasa spans, so it lives in
    `select_trishoola`. Example 84 settled the second; see OI-132 (closed).
    """
    from hora.dasha.rasi.niryaana_shoola import (
        NiryaanaShoolaError,
        trishoola_readings,
    )

    # Rudra in Aries: the trines are Aries, Leo, Sagittarius.
    got = trishoola_readings(R["Leo"], R["Aries"], longevity="middle")
    assert got["trishoola_names"] == ("Aries", "Leo", "Sagittarius")
    assert got["applies"] and got["position"] == 1
    assert got["longevity"] == "middle"

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


# --------------------------------------------------------------------------
# Example 84 — Chart 8, the only worked Niryaana Shoola dasa.
# --------------------------------------------------------------------------

EX84_ORDER = ["Sg", "Cp", "Aq", "Pi", "Ar", "Ta", "Ge"]
EX84_YEARS = [9, 7, 8, 9, 7, 8, 9]


def _chart_8():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(8).items()},
            {int(g): sign for g, sign in graha_signs(8).items()},
            lagna(8))


def _chart_8_rudra():
    from hora.charts.maraka import rudra

    longitudes, signs, lagna_sign = _chart_8()
    return rudra(lagna_sign, signs, longitudes)


def test_example_84s_seed_pair_is_sagittarius_and_gemini():
    """"We have to find the stronger of 2nd (Sg) and 8th (Ge)." Chart 8's
    lagna is Scorpio, so the pair is exactly those two.
    """
    from hora.dasha.rasi.niryaana_shoola import seed

    _longitudes, _signs, lagna_sign = _chart_8()
    assert lagna_sign == R["Scorpio"]

    got = seed(lagna_sign)
    assert (got.second_name, got.eighth_name) == ("Sagittarius", "Gemini")
    assert got.sign is None          # OI-131: not ours to decide


def test_15_5_2s_cascade_picks_the_other_one():
    """D-62. "Sg is stronger", says the example, with no working shown.
    §15.5.2's cascade ties on rules 1 to 5 and decides for **Gemini** on rule
    6 — the same rule Exercise 23 used on these same two lords to make Mercury
    Rudra, "as he is more advanced in his rasi".
    """
    from hora.charts.rasi_strength import stronger

    longitudes, _signs, lagna_sign = _chart_8()
    verdict = stronger((lagna_sign + 1) % 12, (lagna_sign + 7) % 12,
                       longitudes, purpose="phalita")

    assert verdict.winner == R["Gemini"]
    assert verdict.decided_by == "6"
    assert [r.winner for r in verdict.rules[:5]] == [None] * 5
    assert "Mercury advanced 28" in verdict.reason


def test_the_ayur_reading_of_rule_2_does_not_rescue_sagittarius():
    """D-62 again, from the other side. §15.5.2's ayur note changes rule 2 to
    the luminaries. Neither luminary occupies or aspects either rasi, so rule
    2 ties there too — and read as *graha* drishti instead, the two grahas
    that reach anything reach **Gemini**. Every route we can compute agrees
    against the example.
    """
    from hora.charts.aspects import graha_aspects_sign, rasi_drishti
    from hora.core.const import Graha

    _longitudes, signs, _lagna = _chart_8()
    luminaries = (int(Graha.SUN), int(Graha.MOON))

    for target in (R["Sagittarius"], R["Gemini"]):
        assert not [g for g in luminaries
                    if signs[g] == target or target in rasi_drishti(signs[g])]

    reaching = {
        target: [g for g, place in signs.items()
                 if graha_aspects_sign(g, place, target)]
        for target in (R["Sagittarius"], R["Gemini"])
    }
    assert reaching[R["Sagittarius"]] == []
    assert {int(Graha.MARS), int(Graha.JUPITER)} == set(reaching[R["Gemini"]])


def test_the_cascades_seed_would_break_the_examples_own_reasoning():
    """Why D-62 is NEEDS YOU rather than a footnote. Both candidates are odd,
    so the direction survives the swap and only the starting rasi moves — and
    that is enough: seeding from Gemini puts the native's death at 50 in
    **Sagittarius** dasa, which is not one of his Trishoolas, so §22.2.2's
    main reading would have nothing to say about the death it is explaining.
    """
    from hora.dasha.rasi.niryaana_shoola import direction_of, progression

    assert direction_of(R["Gemini"]) == direction_of(R["Sagittarius"])

    counterfactual = progression(R["Gemini"])
    at_50 = [ABBR[s] for s, start, years in zip(
        counterfactual.signs, counterfactual.starts, counterfactual.years)
        if start <= 50 < start + years]
    assert at_50 == ["Sg"]

    trishoolas = {t["rasi"] for t in _chart_8_rudra()["trishoola"]}
    assert "Sagittarius" not in trishoolas
    assert "Gemini" in trishoolas


@pytest.mark.parametrize("position", range(7))
def test_example_84s_printed_sequence_and_lengths(position):
    """"So dasas start from Sg and go as Sg (9 years), Cp (7 years), Aq (8
    years), Pi (9 years), Ar (7 years), Ta (8 years), Ge (9 years) etc."

    Sagittarius is odd, so forward; the lengths are the modality rule and
    nothing else.
    """
    from hora.dasha.rasi.niryaana_shoola import progression

    got = progression(R["Sagittarius"])
    assert got.direction == "forward"
    assert ABBR[got.signs[position]] == EX84_ORDER[position]
    assert got.years[position] == EX84_YEARS[position]


def test_gemini_dasa_starts_at_48_and_runs_to_57():
    """"It may be seen that Ge dasa starts after 9+7+8+9+7+8 = 48 years. It
    runs till the age of 57 years. The native died at an age of 50 years."

    Both the sum the example spells out and the age it puts the death in.
    """
    from hora.dasha.rasi.niryaana_shoola import progression

    got = progression(R["Sagittarius"])
    index = got.signs.index(R["Gemini"])
    assert sum(EX84_YEARS[:6]) == 48
    assert got.starts[index] == 48
    assert got.starts[index] + got.years[index] == 57
    assert got.starts[index] <= 50 < got.starts[index] + got.years[index]


def test_example_84_settles_how_the_longevity_category_chooses():
    """"Ge is the only Trishoola rasi whose dasa comes in the middle life
    range (36-72 years)."

    Closed OI-132, and it shows the question had the wrong shape: the category
    owns no position among the three. It names a range of years, and the
    Trishoola whose *dasa* falls in it is the one — so the answer depends on
    the seed.
    """
    from hora.core.constants.maraka import LONGEVITY_RANGES
    from hora.dasha.rasi.niryaana_shoola import (
        THE_TRISHOOLA_IS_THE_ONE_WHOSE_DASA_IS_IN_RANGE,
        progression,
        select_trishoola,
    )

    body = _chart_8_rudra()
    assert {t["rasi"] for t in body["trishoola"]} == {
        "Gemini", "Libra", "Aquarius"}

    assert LONGEVITY_RANGES["middle"] == (36, 72)
    got = select_trishoola(body["rudra_sign"], progression(R["Sagittarius"]),
                           "middle")

    spans = {row["rasi"]: (row["starts"], row["ends"])
             for row in got["trishoolas"]}
    assert spans == {"Aquarius": (16, 24), "Gemini": (48, 57),
                     "Libra": (81, 88)}
    assert [row["rasi"] for row in got["trishoolas"] if row["in_range"]] == [
        "Gemini"]
    assert got["selected"]["rasi"] == "Gemini"
    assert got["undecided"] is None
    assert "only Trishoola" in THE_TRISHOOLA_IS_THE_ONE_WHOSE_DASA_IS_IN_RANGE


def test_exercise_23s_middle_life_is_what_selects_gemini():
    """The category is not asserted by Example 84 — it was computed in
    Exercise 23, and chapter 14's three-pairs method already gives it. Feeding
    the wrong category picks a different spike or none.
    """
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    body = _chart_8_rudra()
    run = progression(R["Sagittarius"])

    short = select_trishoola(body["rudra_sign"], run, "short")
    assert short["selected"]["rasi"] == "Aquarius"      # 16-24, inside 0-36

    long_life = select_trishoola(body["rudra_sign"], run, "long")
    assert long_life["selected"]["rasi"] == "Libra"     # 81-88, inside 72-108


def test_two_trishoolas_can_land_in_one_range():
    """OI-133. Example 84's "only" is not guaranteed: the three are trines, so
    their dasas are about thirty-two years apart in a ninety-six year cycle,
    and every range is thirty-six years wide. A quarter of all combinations do
    not resolve.
    """
    from collections import Counter

    from hora.dasha.rasi.niryaana_shoola import (
        MORE_THAN_ONE_TRISHOOLA_CAN_FALL_IN_RANGE,
        progression,
        select_trishoola,
    )

    tally = Counter()
    for seed_sign in range(12):
        run = progression(seed_sign)
        for rudra_sign in range(12):
            for category in ("short", "middle", "long"):
                got = select_trishoola(rudra_sign, run, category)
                tally[sum(r["in_range"] for r in got["trishoolas"])] += 1

    assert dict(tally) == {1: 324, 2: 72, 0: 36}
    assert sum(tally.values()) == 432

    run = progression(R["Sagittarius"])
    ambiguous = next(
        select_trishoola(rudra_sign, run, cat)
        for rudra_sign in range(12) for cat in ("short", "middle", "long")
        if sum(r["in_range"]
               for r in select_trishoola(rudra_sign, run, cat)["trishoolas"])
        == 2)
    assert ambiguous["selected"] is None
    assert "OI-133" in ambiguous["undecided"]
    assert "thirty-six years wide" in MORE_THAN_ONE_TRISHOOLA_CAN_FALL_IN_RANGE


def test_gemini_dasa_runs_dec_1994_to_dec_2003():
    """"Ge dasa ran during Dec 1994-Dec 2003." Chart 8 is born 2 December
    1946, and the dasas are whole years, so each opens on the birth month.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.niryaana_shoola import progression

    born = chart(8)["birth_data"]
    assert (born["year"], born["month"]) == (1946, 12)

    got = progression(R["Sagittarius"])
    index = got.signs.index(R["Gemini"])
    assert born["year"] + got.starts[index] == 1994
    assert born["year"] + got.starts[index] + got.years[index] == 2003
    assert chart(8)["events"]["died"] == "July 1997, aged 50"


def test_the_antardasas_are_nine_months_each_by_narayanas_rule():
    """"each antardasa is of 9 months". §18.3 gives each antardasa a length in
    dasa months equal to the dasa's length in years, and Gemini's dasa is 9
    years — so the borrowed rule reproduces the example's figure.
    """
    from hora.dasha.rasi.narayana import antardasas

    longitudes, _signs, _lagna = _chart_8()
    got = antardasas(R["Gemini"], 9, longitudes)
    assert got.months_each == 9
    assert len(got.signs) == 12
    assert got.months_each * 12 == 9 * 12    # the whole dasa, in months


def test_the_antardasas_start_from_libra_and_run_forward():
    """"Antardasas in Ge dasa start from Li and go as Li, Sc, Sg, Cp etc. The
    4th antardasa is Cp."

    §18.3's rule reproduces it: the seed is the stronger of Gemini and the 7th
    from it, its lord sits in Libra, and Libra is odd so the run is forward.
    """
    from hora.dasha.rasi.narayana import antardasas

    longitudes, _signs, _lagna = _chart_8()
    got = antardasas(R["Gemini"], 9, longitudes)

    assert got.start == R["Libra"]
    assert got.direction == "forward"
    assert [ABBR[s] for s in got.signs[:4]] == ["Li", "Sc", "Sg", "Cp"]
    assert got.signs[3] == R["Capricorn"]


def test_july_1997_falls_in_the_fourth_antardasa():
    """"When he died in July 1997, the 4th antardasa was running."

    Three nine-month antardasas from December 1994 end in March 1997, so the
    4th runs March to December. §18.6's solar-arc measure would open it in
    late February instead — both put July inside it, so this example does not
    part them.
    """
    born_months = 1994 * 12 + 11              # December 1994, zero-based
    fourth_opens = born_months + 3 * 9
    fourth_closes = fourth_opens + 9
    death = 1997 * 12 + 6                      # July 1997

    assert divmod(fourth_opens, 12) == (1997, 2)      # March 1997
    assert fourth_opens <= death < fourth_closes
    assert divmod(fourth_closes, 12) == (1997, 11)    # December 1997


def test_capricorn_meets_both_antardasa_principles():
    """"Cp is the 8th house from Ge and Cp aspects Le, which contains Saturn
    in navamsa. Saturn is the 8th lord from dasa rasi."

    Both of §22.2.2's principles on one rasi, which is what the section calls
    a strong candidate — and the example's own conclusion, "Ge-Cp antardasa
    brought death". Asserted on the example's stated Leo; D-63 is that the
    navamsa is Scorpio, and the next test shows Capricorn qualifies either way.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Gemini"], {int(Graha.SATURN): R["Leo"]})

    assert got["eighth_name"] == "Capricorn"
    assert got["eighth_lord_name"] == "Saturn"
    assert R["Capricorn"] in got["from_dasa_rasi"]
    assert R["Capricorn"] in got["aspecting_the_navamsa_rasi"]
    assert R["Capricorn"] in got["strong_candidates"]
    assert "Saturn" in got["why"] and "Leo" in got["why"]


def test_chart_8s_saturn_is_in_scorpio_in_navamsa_not_leo():
    """D-63. Saturn is printed at 15 Cn 39. Cancer is movable, so its navamsas
    run from Cancer, and 15°39' is the fifth of them — **Scorpio**. The
    example says Leo, which is the rasi §22.2.2's own generic illustration
    used two paragraphs earlier.
    """
    from hora.charts.book import longitudes as book_longitudes
    from hora.charts.vargas import varga

    printed = book_longitudes(8)
    assert printed["Sat"] == 3 * 30 + 15 + 39 / 60
    got = varga(printed["Sat"], "D9")
    assert got.sign == R["Scorpio"]
    assert got.amsa_index == 4          # the fifth navamsa of Cancer


def test_the_conclusion_survives_the_navamsa_slip():
    """Why D-63 is a slip and not a wrong reading: Capricorn is movable, so it
    aspects Taurus, Leo **and Scorpio**. It reaches the navamsa rasi under
    either sign, and stays a strong candidate — the computed Scorpio simply
    admits a second one alongside it.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    assert set(rasi_drishti(R["Capricorn"])) == {
        R["Taurus"], R["Leo"], R["Scorpio"]}

    printed = antardasa_candidates(R["Gemini"], {int(Graha.SATURN): R["Leo"]})
    computed = antardasa_candidates(R["Gemini"],
                                    {int(Graha.SATURN): R["Scorpio"]})

    assert printed["strong_candidate_names"] == ("Capricorn",)
    assert set(computed["strong_candidate_names"]) == {"Scorpio", "Capricorn"}
    assert printed["from_dasa_rasi"] == computed["from_dasa_rasi"]


# --------------------------------------------------------------------------
# Example 85 — Rajiv Gandhi, the seed the book shows its working for.
# --------------------------------------------------------------------------

EX85_ORDER = ["Vi", "Le", "Cn", "Ge", "Ta", "Ar"]
EX85_YEARS = [9, 8, 7, 9, 8, 7]


def _chart_39():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(39).items()},
            {int(g): sign for g, sign in graha_signs(39).items()},
            lagna(39))


def _chart_39_rudra():
    from hora.charts.maraka import rudra

    longitudes, signs, lagna_sign = _chart_39()
    return rudra(lagna_sign, signs, longitudes)


def test_chart_39s_grahas_recompute_and_its_ascendant_is_a_rounded_minute():
    """Every graha inside one arcminute. The ascendant is 8.6' out, the widest
    residual in the register — and it is birth-time precision, not ephemeris
    disagreement: the lagna moves about 7' per half-minute here, so a birth at
    7:11:37 rather than the printed 7:11 closes it exactly. Leo lagna is
    secure either way, and Niryaana Shoola reads only the rasi.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(39)
    place = Place(name="Chart 39", **record["place"])
    printed = longitudes(39)

    computed = compute_chart(from_local(**record["birth_data"]), place,
                             Settings(node_type=NodeType.MEAN))
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"

    assert 8.0 < abs(computed.lagna_longitude - printed["Asc"]) * 60 < 9.0

    later = compute_chart(
        from_local(**{**record["birth_data"], "minute": 11, "second": 37.0}),
        place, Settings(node_type=NodeType.MEAN))
    assert abs(later.lagna_longitude - printed["Asc"]) * 60 < 1.0
    assert int(computed.lagna_longitude // 30) == R["Leo"]


def test_chart_39_is_a_twelfth_vote_and_the_widest_margin_yet():
    """OI-68. Rahu is 96' out under `true` — more than three rasi-degrees, and
    wider than Chart 24's 79'. Twelve charts, none favouring our default.
    """
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(39)
    printed = longitudes(39)["Rahu"]
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name="Chart 39", **record["place"]), Settings(node_type=node))
        errors[node] = abs(
            computed.positions[int(Graha.RAHU)].longitude - printed) * 60

    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 90.0


def test_example_85_shows_the_working_example_84_withheld():
    """"The 2nd house is stronger than the 8th house, **as it is occupied by a
    planet (Mars)**."

    That is §15.5.2 rule 1 word for word, and the cascade returns Virgo by rule
    1 with the same count. So the chapter does reach for §15.5.2 for this seed
    — which is what makes Example 84's contradiction D-62 rather than evidence
    of some other method.
    """
    from hora.charts.rasi_strength import stronger
    from hora.core.const import Graha

    longitudes, signs, lagna_sign = _chart_39()
    assert lagna_sign == R["Leo"]
    assert signs[int(Graha.MARS)] == R["Virgo"]

    verdict = stronger((lagna_sign + 1) % 12, (lagna_sign + 7) % 12,
                       longitudes, purpose="phalita")
    assert verdict.winner == R["Virgo"]
    assert verdict.decided_by == "1"
    assert "Virgo contains 1 planet; Pisces contains 0 planets" in (
        verdict.reason)


def test_the_two_chapter_22_seeds_disagree_about_the_cascade():
    """D-62 in one place. Example 85's seed is the cascade's answer; Example
    84's is not, and the two are the only worked seeds the chapter gives.
    """
    from hora.charts.book import graha_longitudes, lagna
    from hora.charts.rasi_strength import stronger

    said = {8: R["Sagittarius"], 39: R["Virgo"]}
    computed = {}
    for number in (8, 39):
        longitudes = {int(g): lon
                      for g, lon in graha_longitudes(number).items()}
        lagna_sign = lagna(number)
        computed[number] = stronger((lagna_sign + 1) % 12,
                                    (lagna_sign + 7) % 12,
                                    longitudes, purpose="phalita").winner

    assert computed[39] == said[39]      # Example 85 agrees
    assert computed[8] != said[8]        # Example 84 does not


@pytest.mark.parametrize("position", range(6))
def test_example_85s_printed_sequence_runs_backward_from_virgo(position):
    """"Dasas start from Vi. It is an even rasi and so dasas go backwards. We
    get Vi dasa of 9 years, Le dasa of 8 years, Cn dasa of 7 years, Ge dasa of
    9 years, Ta dasa is of 8 years and Ar dasa of 7 years."

    The chapter's only backward run, and its only dual-rasi seed.
    """
    from hora.dasha.rasi.niryaana_shoola import progression

    got = progression(R["Virgo"])
    assert got.direction == "backward"
    assert ABBR[got.signs[position]] == EX85_ORDER[position]
    assert got.years[position] == EX85_YEARS[position]


def test_aries_dasa_ran_aug_1985_to_aug_1992():
    """"Ar dasa ran during Aug 1985-Aug 1992. Mr. Gandhi died in this dasa."

    Born August 1944; the five dasas before Aries total 41 years.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.niryaana_shoola import progression

    born = chart(39)["birth_data"]
    assert (born["year"], born["month"]) == (1944, 8)

    got = progression(R["Virgo"])
    index = got.signs.index(R["Aries"])
    assert sum(EX85_YEARS[:5]) == 41
    assert got.starts[index] == 41
    assert born["year"] + got.starts[index] == 1985
    assert born["year"] + got.starts[index] + got.years[index] == 1992
    assert chart(39)["events"]["assassinated"] == "May 1991, aged 46"


def test_example_85s_rudra_is_decided_by_the_first_cascade_test():
    """"Rudra is the stronger of the 8th lords from Le and Aq. So Rudra is the
    stronger of Moon and Saturn (see Table 32). Moon is stronger and he
    becomes Rudra. He is in Le. So Trishoola spikes are in Ar, Le and Sg."

    Table 32's 8th from Leo is Cancer and from Aquarius is Capricorn, and the
    Moon wins on conjunctions — he sits in a Leo holding four other grahas.
    """
    from hora.charts.maraka import rudra_eighth

    assert rudra_eighth(R["Leo"]) == R["Cancer"]
    assert rudra_eighth(R["Aquarius"]) == R["Capricorn"]

    body = _chart_39_rudra()
    assert body["candidates"] == ["Moon", "Saturn"]
    assert body["rudra"] == "Moon"
    assert body["rudra_rasi"] == "Leo"
    assert body["decided_by"] == 1
    assert "Moon conjoins 4 planets" in body["why"]
    assert {t["rasi"] for t in body["trishoola"]} == {
        "Aries", "Leo", "Sagittarius"}


def test_aries_is_the_trishoola_the_longevity_range_selects():
    """"Being a Trishoola rasi, Ar can kill." The example does not name the
    category, but Example 84's rule picks Aries unaided: of the three spikes
    only its dasa, 41-48, falls in the 36-72 a middle life gives — and he died
    at 46, inside it. A second chart confirming closed OI-132.
    """
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    body = _chart_39_rudra()
    got = select_trishoola(body["rudra_sign"], progression(R["Virgo"]),
                           "middle")

    spans = {row["rasi"]: (row["starts"], row["ends"])
             for row in got["trishoolas"]}
    assert spans == {"Leo": (9, 17), "Sagittarius": (72, 81),
                     "Aries": (41, 48)}
    assert got["selected"]["rasi"] == "Aries"
    assert got["undecided"] is None
    assert got["selected"]["starts"] <= 46 < got["selected"]["ends"]


def test_aries_is_not_a_maraka_sthana_so_rule_1_does_not_carry_it():
    """§22.2.2's first reading is the marakas, and it has nothing to say here
    — from Leo the maraka sthanas are Virgo and Aquarius. The Trishoola
    reading is doing all the work, which is what "usually death occurs in the
    dasa of a Trishoola rasi" claims.
    """
    from hora.dasha.rasi.niryaana_shoola import maraka_readings

    _longitudes, signs, lagna_sign = _chart_39()
    got = maraka_readings(R["Aries"], lagna_sign, signs)
    assert got["is_maraka_sthana"] == ()
    assert not got["applies"]


def test_the_antardasa_seed_is_decided_by_venus_aspecting_libra():
    """"In Ar dasa, antardasas start from the lord of the stronger of Ar and
    Li. Li is stronger as its lord Venus aspects it."

    §15.5.2 rule 2. Jupiter and Mercury reach both rasis from Leo, so they
    cancel; Venus is the third count Libra has and Aries does not — which is
    exactly the reason the example gives.
    """
    from hora.charts.rasi_strength import stronger

    longitudes, _signs, _lagna = _chart_39()
    verdict = stronger(R["Aries"], R["Libra"], longitudes, purpose="phalita")

    assert verdict.winner == R["Libra"]
    assert verdict.decided_by == "2"
    assert "Aries count 2" in verdict.reason
    assert "Libra count 3" in verdict.reason
    assert "lord (Venus) aspects from Leo" in verdict.reason


def test_the_tenth_antardasa_of_aries_is_taurus():
    """"So dasas start from Le, which contains Venus. The 10th from Le is Ta."

    §18.3 again: the antardasas begin in the rasi holding the seed's lord, and
    Leo is odd so they run forward. Seven months each, from a seven-year dasa.
    """
    from hora.dasha.rasi.narayana import antardasas

    longitudes, _signs, _lagna = _chart_39()
    got = antardasas(R["Aries"], 7, longitudes)

    assert got.seed == R["Libra"]
    assert got.start == R["Leo"]
    assert got.direction == "forward"
    assert got.months_each == 7
    assert got.signs[9] == R["Taurus"]


def test_may_1991_falls_in_the_tenth_antardasa():
    """"During May 1991, the 10th antardasa was running." Nine seven-month
    antardasas from August 1985 end in November 1990, so the 10th runs
    November 1990 to June 1991.
    """
    opens = 1985 * 12 + 7 + 9 * 7          # August 1985, zero-based, plus nine
    death = 1991 * 12 + 4                   # May 1991

    assert divmod(opens, 12) == (1990, 10)          # November 1990
    assert opens <= death < opens + 7
    assert divmod(opens + 7, 12) == (1991, 5)       # June 1991


def test_the_eighth_lord_from_aries_is_ketu_by_15_5_1():
    """"From Ar, the 8th lord is Ketu." The 8th from Aries is Scorpio, which
    §15.5.1 must settle — and it settles it the book's way, on the same rule 2
    count that decided the antardasa seed.
    """
    from hora.charts.colord import CO_LORDS
    from hora.charts.colord import stronger as stronger_co_lord
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import (
        NiryaanaShoolaError,
        antardasa_candidates,
    )

    longitudes, _signs, _lagna = _chart_39()
    assert set(CO_LORDS[R["Scorpio"]]) == {int(Graha.MARS), int(Graha.KETU)}

    verdict = stronger_co_lord(R["Scorpio"], longitudes, purpose="arudha")
    assert verdict.winner == int(Graha.KETU)

    with pytest.raises(NiryaanaShoolaError, match="15.5.1"):
        antardasa_candidates(R["Aries"], {int(Graha.KETU): R["Capricorn"]})


def test_ketu_and_mars_are_both_in_capricorn_in_navamsa():
    """"he is in Cp with Mars in navamsa" — both of them, computed rather than
    taken on trust. Ketu at 2 Cp 48 and Mars at 1 Vi 12 each fall in the first
    navamsa of their rasi, and both of those are Capricorn.
    """
    from hora.charts.book import longitudes as book_longitudes
    from hora.charts.vargas import varga

    printed = book_longitudes(39)
    for name in ("Ketu", "Mars"):
        got = varga(printed[name], "D9")
        assert got.sign == R["Capricorn"], name
        assert got.amsa_index == 0, name


def test_taurus_reaches_death_by_the_second_principle_alone():
    """"Ta aspects Cp."

    The antardasa that killed satisfies §22.2.2's second principle and **not**
    its first — Taurus is not the 6th, 7th, 8th or 12th from Aries. So the
    intersection the section calls "a strong candidate" is not a requirement:
    here the strong candidate is Scorpio, and Taurus is what ran.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Aries"], {int(Graha.KETU): R["Capricorn"]},
                               eighth_lord=int(Graha.KETU))

    assert got["eighth_name"] == "Scorpio"
    assert got["navamsa_rasi"] == "Capricorn"
    assert R["Taurus"] in got["aspecting_the_navamsa_rasi"]
    assert R["Taurus"] not in got["from_dasa_rasi"]
    assert got["strong_candidate_names"] == ("Scorpio",)


def test_chapter_22s_two_deaths_use_the_two_principles_differently():
    """Example 84's Capricorn met both principles; Example 85's Taurus meets
    only the second. Between them they show the section's "can be" is the
    whole of its claim — neither principle is necessary on its own, and the
    intersection is not necessary either.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    ex84 = antardasa_candidates(R["Gemini"], {int(Graha.SATURN): R["Leo"]})
    ex85 = antardasa_candidates(R["Aries"], {int(Graha.KETU): R["Capricorn"]},
                                eighth_lord=int(Graha.KETU))

    assert R["Capricorn"] in ex84["strong_candidates"]
    assert R["Taurus"] not in ex85["strong_candidates"]
    assert R["Taurus"] in ex85["aspecting_the_navamsa_rasi"]


# --------------------------------------------------------------------------
# Example 86 — Indira Gandhi, whose chart the book prints eight chapters later.
# --------------------------------------------------------------------------

#: The nine dasas the example's dates require, from a Leo seed running forward.
EX86_ORDER = ["Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi", "Ar"]

#: Its four dated antardasas of Aries, seven months each.
EX86_ANTARDASAS = [("Le", 1982, 11), ("Vi", 1983, 6), ("Li", 1984, 1),
                   ("Sc", 1984, 8)]


def test_chart_61_has_not_been_supplied_yet():
    """"Chart 61 (in a later chapter)". The coverage line for Example 86:
    everything on `EXAMPLE_86_AWAITS_CHART_61` waits on it, and this fails
    loudly when the chart lands so the list gets worked through.
    """
    from hora.charts.book import BookChartError, chart, numbers
    from hora.dasha.rasi.niryaana_shoola import EXAMPLE_86_AWAITS_CHART_61

    assert 61 not in numbers()
    assert max(numbers()) < 61
    with pytest.raises(BookChartError, match="there is no Chart"):
        chart(61)

    assert len(EXAMPLE_86_AWAITS_CHART_61) == 9
    assert any("Saturn is in Cancer" in item
               for item in EXAMPLE_86_AWAITS_CHART_61)
    # Example 91 reads the same chart with chapter 23's dasa, so its claims
    # wait on the same page.
    assert any("Example 91" in item for item in EXAMPLE_86_AWAITS_CHART_61)


def test_example_86_reveals_a_table_32_exception_14_3_never_states():
    """"Because Saturn is in Cn, we take the 8th houses from Cn and Cp in the
    normal way, instead of using Table 32."

    §14.3 says the opposite with no exception — "find the 8th house using
    Table 32 and **not** in the normal way". See OI-134.
    """
    from hora.core.constants.maraka import (
        RUDRA_RULE,
        RUDRA_TABLE_32_SATURN_EXCEPTION,
    )

    assert "not in the normal way" in RUDRA_RULE
    assert "Table 32" in RUDRA_RULE
    assert "in the normal way, instead of using Table 32" in (
        RUDRA_TABLE_32_SATURN_EXCEPTION)
    assert "Because Saturn is in Cn" in RUDRA_TABLE_32_SATURN_EXCEPTION


def test_what_the_exception_undoes_is_footnote_50s_direction():
    """Cancer and Capricorn are even rasis, so footnote 50 counts their 8th
    anti-zodiacally — which is exactly what Table 32 holds for them. "The
    normal way" is the zodiacal count. So Saturn reverses the direction here,
    as §18.2.1's exception reverses a Narayana dasa's.
    """
    from hora.charts.maraka import ordinary_eighth, rudra_eighth
    from hora.core.const import RASI_IS_ODD
    from hora.core.constants.maraka import TABLE_32_EXCEPTION_REVERSES_THE_COUNT

    for sign in (R["Cancer"], R["Capricorn"]):
        assert not RASI_IS_ODD[sign]
        assert rudra_eighth(sign) == (sign - 7) % 12       # anti-zodiacal
        assert ordinary_eighth(sign) == (sign + 7) % 12    # zodiacal

    assert rudra_eighth(R["Cancer"]) == R["Sagittarius"]
    assert ordinary_eighth(R["Cancer"]) == R["Aquarius"]
    assert rudra_eighth(R["Capricorn"]) == R["Gemini"]
    assert ordinary_eighth(R["Capricorn"]) == R["Leo"]
    assert "anti-zodiacal 8th" in TABLE_32_EXCEPTION_REVERSES_THE_COUNT


def test_the_two_routes_give_different_rudra_candidates():
    """Why OI-134 is not a refinement. Table 32 would make the candidates the
    lords of Sagittarius and Gemini; the normal count makes them the lords of
    Aquarius and Leo — and the example names Rahu and the Sun, which are
    Aquarius's co-lord and Leo's lord.
    """
    from hora.charts.colord import CO_LORDS
    from hora.core.const import GRAHA_NAMES, RASI_LORD, Graha

    by_table = {str(GRAHA_NAMES[int(RASI_LORD[s])])
                for s in (R["Sagittarius"], R["Gemini"])}
    assert by_table == {"Jupiter", "Mercury"}

    assert set(CO_LORDS[R["Aquarius"]]) == {int(Graha.SATURN), int(Graha.RAHU)}
    assert int(RASI_LORD[R["Leo"]]) == int(Graha.SUN)


def test_rudra_reports_the_exception_beside_the_affliction_override():
    """Both are rules §14.3's neighbourhood states and we do not apply — the
    affliction override because "malefics **like**" leaves its list open
    (OI-109), this one because its trigger is unsaid (OI-134). Reported, so a
    caller is never told a Rudra is settled when a stated rule was skipped.
    """
    from hora.charts.book import graha_longitudes, graha_signs, lagna
    from hora.charts.maraka import rudra

    signs = {int(g): sign for g, sign in graha_signs(39).items()}
    longitudes = {int(g): lon for g, lon in graha_longitudes(39).items()}
    body = rudra(lagna(39), signs, longitudes)

    assert "Because Saturn is in Cn" in body["table_32_exception"]
    assert "malefics like" in body["affliction_override"]
    assert body["rudra"] == "Moon"


def test_example_86s_reasoning_needs_the_books_own_node_exaltations():
    """"The 8th lord Rahu is debilitated... So Trishoola is in the trines from
    Sg."

    Rudra is Rahu and his rasi is Sagittarius, so the example calls Rahu
    debilitated **in Sagittarius**. Table 6 does; the Taurus/Scorpio
    convention many texts use makes him neither. Independent confirmation of
    D-4 from eight chapters away, and the first place the book *reasons* from
    it rather than tabulating it. See OI-14.
    """
    from hora.charts.maraka import trishoola_rasis
    from hora.core.const import DEBILITATION_RASI, EXALTATION_RASI, Graha

    assert DEBILITATION_RASI[int(Graha.RAHU)] == R["Sagittarius"]
    assert EXALTATION_RASI[int(Graha.RAHU)] == R["Gemini"]
    assert DEBILITATION_RASI[int(Graha.RAHU)] not in (R["Taurus"],
                                                      R["Scorpio"])
    assert set(trishoola_rasis(R["Sagittarius"])) == {
        R["Sagittarius"], R["Aries"], R["Leo"]}


def test_a_debilitated_candidate_is_preferred_which_oi_109_had_no_example_for():
    """"But debilitated 8th lord is a better candidate for being Rudra."

    §14.3's override says the weaker planet takes over if it is "debilitated
    or in an inimical sign **and** conjoined/aspected by malefics like Mars,
    Saturn, Rahu and Ketu". Example 86 prefers the debilitated candidate but
    never mentions the affliction half, and the malefic it would need cannot
    be checked without Chart 61 — so this is evidence for OI-109, not its
    close.
    """
    from hora.core.constants.maraka import (
        RUDRA_AFFLICTION_MALEFICS,
        RUDRA_AFFLICTION_RULE,
    )
    from hora.dasha.rasi.niryaana_shoola import EXAMPLE_86_AWAITS_CHART_61

    assert "debilitated or in an inimical sign and" in RUDRA_AFFLICTION_RULE
    assert "Sun" not in RUDRA_AFFLICTION_MALEFICS
    assert any("join another planet" in item
               for item in EXAMPLE_86_AWAITS_CHART_61)


def test_the_seed_is_15_5_2_rule_1_for_the_third_time_in_the_chapter():
    """"Because the 2nd house with a planet is stronger than the empty 8th
    house, dasas start from the 2nd house."

    Word for word Example 85's reason, on a different chart. Two of the
    chapter's three worked seeds use rule 1 and agree with the cascade;
    Example 84 is the one that does not (D-62).
    """
    from hora.charts.rasi_strength import stronger

    verdict = stronger(R["Leo"], R["Pisces"],
                       {}, purpose="phalita")
    assert verdict.rules[0].rule == "1"
    assert "contains" in verdict.rules[0].description


def test_the_printed_dasa_list_drops_libra_and_its_own_dates_restore_it():
    """"Dasas go as Le, Vi, **Sc**, Sg etc" — Libra is missing, and the walk is
    zodiacal, so it cannot be. D-64. The example's dates settle it: Aries has
    to be the ninth dasa, opening at 65 years, for a seven-year Aries dasa to
    contain October 1984 while running to November 1989.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        PRINTED_SEQUENCES_DROP_LIBRA,
        progression,
    )

    got = progression(R["Leo"])
    assert got.direction == "forward"
    assert [ABBR[s] for s in got.signs[:9]] == EX86_ORDER
    assert ABBR[got.signs[2]] == "Li"

    index = got.signs.index(R["Aries"])
    assert index == 8
    assert got.starts[index] == 65
    assert got.years[index] == 7
    assert 1917 + got.starts[index] == 1982        # "Nov 1982-Nov 1989"
    assert 1917 + got.starts[index] + got.years[index] == 1989

    assert "Le, Vi, Sc, Sg" in PRINTED_SEQUENCES_DROP_LIBRA


def test_dropping_libra_would_move_aries_seven_years_earlier():
    """Why the dates settle D-64 rather than merely fitting it. Without Libra,
    Aries would be the eighth dasa and open at 58 — 1975, not 1982.
    """
    from hora.dasha.rasi.niryaana_shoola import dasa_years

    as_printed = ["Le", "Vi", "Sc", "Sg", "Cp", "Aq", "Pi"]
    elapsed = sum(dasa_years(ABBR.index(a)) for a in as_printed)
    assert elapsed == 58
    assert 1917 + elapsed != 1982


def test_the_printed_antardasa_list_repeats_leo_which_no_walk_does():
    """"Antardasas start from Mars in Le and go as Le, Vi, **Le**, Sc etc."

    A zodiacal walk never repeats, and the example's own prose names the third
    antardasa "of Li" four lines later. D-64's second half.
    """
    from hora.dasha.rasi.niryaana_shoola import PRINTED_SEQUENCES_DROP_LIBRA

    assert "Le, Vi, Le, Sc" in PRINTED_SEQUENCES_DROP_LIBRA
    assert "the third antardasa of Li" in PRINTED_SEQUENCES_DROP_LIBRA

    walk = [(R["Leo"] + step) % 12 for step in range(4)]
    assert [ABBR[s] for s in walk] == ["Le", "Vi", "Li", "Sc"]
    assert len(set(walk)) == 4


def test_the_antardasa_seed_is_aries_by_the_mirror_of_example_85s_reason():
    """"Ar is stronger than Li, as its lord Mars aspects it."

    Example 85 gave the same comparison the other way — "Li is stronger as its
    lord Venus aspects it". Same rule 2, same clause, opposite winner, because
    on that chart Venus reached Libra and here Mars reaches Aries.
    """
    from hora.charts.rasi_strength import PURPOSE_ADAPTATIONS

    assert "the rasi's lord" in PURPOSE_ADAPTATIONS["phalita"]["rule_2_planets"]

    longitudes, _signs, _lagna = _chart_39()
    from hora.charts.rasi_strength import stronger
    other_way = stronger(R["Aries"], R["Libra"], longitudes, purpose="phalita")
    assert other_way.winner == R["Libra"]
    assert "lord (Venus) aspects from Leo" in other_way.reason


@pytest.mark.parametrize("abbr,year,month", EX86_ANTARDASAS)
def test_example_86s_four_dated_antardasas(abbr, year, month):
    """"Nov 1982-June 1983 is the first antardasa of Le. June 1983-Jan 1984 is
    the second antardasa of Vi. Jan 1984-Aug 1984 is the third antardasa of
    Li. The fourth antardasa of Sc runs during Aug 1984-Mar 1985."

    Seven months each from November 1982, walking zodiacally from Leo — Libra
    included, which is where the printed list went wrong.
    """
    position = EX86_ORDER.index(abbr) if abbr in EX86_ORDER else None
    assert position is not None

    opens = 1982 * 12 + 10 + position * 7        # November 1982, zero-based
    assert divmod(opens, 12) == (year, month - 1)


def test_the_fourth_antardasa_holds_the_assassination():
    """"The fourth antardasa of Sc runs during Aug 1984-Mar 1985. This is the
    one that brought death." She was assassinated on 31 October 1984.
    """
    opens = 1982 * 12 + 10 + 3 * 7               # the fourth, from Nov 1982
    death = 1984 * 12 + 9                         # October 1984

    assert divmod(opens, 12) == (1984, 7)         # August 1984
    assert opens <= death < opens + 7
    assert divmod(opens + 7, 12) == (1985, 2)     # March 1985


def test_scorpio_meets_both_principles_as_the_example_says():
    """"Sc is the 8th from dasa rasi Ar. So the first antardasa principle we
    described is correct. Ketu owns the 8th from Ar and he is in Cp in
    navamsa. Sc aspects Cp and the second principle is also satisfied."

    Chapter 22's third reading of the antardasa rule, and the only one where
    the section's own "strong candidate" is the antardasa that ran — Example
    84's Capricorn met both but was one of three, and Example 85's Taurus met
    only the second.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Aries"], {int(Graha.KETU): R["Capricorn"]},
                               eighth_lord=int(Graha.KETU))

    assert got["eighth"] == R["Scorpio"]
    assert R["Scorpio"] in got["from_dasa_rasi"]
    assert R["Capricorn"] in rasi_drishti(R["Scorpio"])
    assert R["Scorpio"] in got["aspecting_the_navamsa_rasi"]
    assert got["strong_candidate_names"] == ("Scorpio",)


# --------------------------------------------------------------------------
# Example 87 — Chart 40, and the "Saturn exception" §22.2.1 never states.
# --------------------------------------------------------------------------

EX87_DASAS = [("Sc", 8, 1927, 1935), ("Sg", 9, 1935, 1944),
              ("Cp", 7, 1944, 1951)]


def _chart_40():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(40).items()},
            {int(g): sign for g, sign in graha_signs(40).items()},
            lagna(40))


def _chart_40_seed_occupants():
    _longitudes, signs, _lagna = _chart_40()
    return {g for g, sign in signs.items() if sign == R["Scorpio"]}


def test_chart_40_recomputes_including_its_ascendant():
    """Every graha and the ascendant inside one arcminute — the cleanest of
    the chapter's three recomputable charts.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(40)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 40", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(40)

    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 1.0


def test_chart_40_is_a_thirteenth_vote_for_the_mean_node():
    """OI-68. Rahu 67' out under `true`, 0.1' under `mean`."""
    from hora.charts.book import chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(40)
    printed = longitudes(40)["Rahu"]
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name="Chart 40", **record["place"]), Settings(node_type=node))
        errors[node] = abs(
            computed.positions[int(Graha.RAHU)].longitude - printed) * 60

    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 60.0


def test_example_87_names_a_saturn_exception_22_2_1_never_states():
    """"Sc is an even rasi and normally dasas should go as Sc, Li, Vi etc.
    However, Saturn occupies Sc and the "Saturn exception" applies. So dasas
    go as Sc, Sg, Cp etc."

    §22.2.1 gives the direction as odd/even sign and nothing else. Note what
    the module returns without the seed's occupants: Sc, Li, Vi — the very
    sequence the example calls "normal" before overriding it.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        DIRECTION_RULE,
        SATURN_EXCEPTION_NAMED_IN_EXAMPLE_87,
        progression,
    )

    assert "Saturn" not in DIRECTION_RULE
    assert '"Saturn exception"' in SATURN_EXCEPTION_NAMED_IN_EXAMPLE_87

    plain = progression(R["Scorpio"])
    assert plain.direction == "backward"
    assert [ABBR[s] for s in plain.signs[:3]] == ["Sc", "Li", "Vi"]
    assert plain.exception is None

    with_saturn = progression(R["Scorpio"], _chart_40_seed_occupants())
    assert with_saturn.direction == "forward"
    assert with_saturn.exception == "Saturn"
    assert [ABBR[s] for s in with_saturn.signs[:3]] == ["Sc", "Sg", "Cp"]
    assert "Example 87's exception makes the order forward" in with_saturn.why


def test_saturn_is_the_only_graha_in_the_seed():
    """The exception fires on Saturn's presence, so it matters that nothing
    else is there to confuse it — and that the seed's single planet is also
    what made Scorpio the seed in the first place.
    """
    from hora.core.const import Graha

    occupants = _chart_40_seed_occupants()
    assert occupants == {int(Graha.SATURN)}


def test_the_exception_is_applied_in_the_absolute_form_the_book_states():
    """§18.2.1 and §19.2 both say "dasa order is forward", not "is reversed".
    Example 87's seed is even, so it cannot part the two readings — the
    absolute form is used because that is how the book states this exception
    both other times. See OI-136.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.kendradi import EXCEPTIONS
    from hora.dasha.rasi.niryaana_shoola import (
        SATURN_MAKES_THE_ORDER_FORWARD,
        direction_of,
    )

    saturn = next(e for e in EXCEPTIONS if e["graha"] == "Saturn")
    assert saturn["gives"] == "forward"
    assert saturn["text"] == SATURN_MAKES_THE_ORDER_FORWARD

    # An odd seed is where the two readings would differ; nothing tests it yet.
    assert direction_of(R["Aries"], {int(Graha.SATURN)}) == "forward"
    assert direction_of(R["Aries"]) == "forward"


def test_ketu_in_the_seed_is_reported_not_applied():
    """Chapters 18 and 19 pair the Saturn exception with a Ketu one. §22.2.1
    states neither and Example 87 supplies only Saturn's, so a seed holding
    Ketu is flagged rather than reversed on chapter 19's authority. OI-136.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.kendradi import EXCEPTIONS
    from hora.dasha.rasi.niryaana_shoola import (
        KETU_EXCEPTION_IS_NOT_ATTESTED_HERE,
        progression,
    )

    ketu = next(e for e in EXCEPTIONS if e["graha"] == "Ketu")
    assert ketu["gives"] == "reversed"

    got = progression(R["Scorpio"], {int(Graha.KETU)})
    assert got.direction == "backward"            # unchanged
    assert got.exception is None
    assert got.undecided == KETU_EXCEPTION_IS_NOT_ATTESTED_HERE


@pytest.mark.parametrize("abbr,years,start,end", EX87_DASAS)
def test_example_87s_three_dated_dasas(abbr, years, start, end):
    """"Sc dasa of 8 years ran during 1927-1935. Sg dasa of 9 years ran during
    1935-1944. Cp dasa of 7 years ran during 1944-1951 and it brought death."
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.niryaana_shoola import progression

    born = chart(40)["birth_data"]["year"]
    assert born == 1927

    got = progression(R["Scorpio"], _chart_40_seed_occupants())
    index = got.signs.index(ABBR.index(abbr))
    assert got.years[index] == years
    assert born + got.starts[index] == start
    assert born + got.starts[index] + got.years[index] == end


def test_the_seed_is_15_5_2_rule_1_for_the_fourth_time():
    """"Niryaana Shoola dasa starts from the stronger of Ta and Sc. Sc is
    stronger as it has one planet."

    Rule 1 again, and the chapter's fourth worked seed. Three of the four use
    rule 1 and agree with the cascade; Example 84 is still the exception.
    """
    from hora.charts.rasi_strength import stronger

    longitudes, _signs, lagna_sign = _chart_40()
    assert lagna_sign == R["Aries"]

    verdict = stronger((lagna_sign + 1) % 12, (lagna_sign + 7) % 12,
                       longitudes, purpose="phalita")
    assert verdict.winner == R["Scorpio"]
    assert verdict.decided_by == "1"
    assert "Scorpio contains 1 planet" in verdict.reason


def test_example_87s_rudra_is_venus_and_its_candidates_name_ketu():
    """"The 8th lords from Ar and Li are Ketu and Venus. Venus is stronger
    than Ketu. So Venus is Rudra. He is in Cp and so Ta, Vi and Cp form
    Trishoola."

    Table 32 and the ordinary count agree for Aries and Libra — both odd — so
    this chart cannot part them, which is why OI-134 is untouched here. Venus
    wins on cascade step 1 whichever co-lord Scorpio contributes.
    """
    from hora.charts.maraka import ordinary_eighth, rudra, rudra_eighth
    from hora.core.const import Graha

    for sign in (R["Aries"], R["Libra"]):
        assert rudra_eighth(sign) == ordinary_eighth(sign)
    assert rudra_eighth(R["Aries"]) == R["Scorpio"]
    assert rudra_eighth(R["Libra"]) == R["Taurus"]

    longitudes, signs, lagna_sign = _chart_40()
    with_ketu = rudra(lagna_sign, signs, longitudes,
                      {R["Scorpio"]: int(Graha.KETU)})
    assert with_ketu["candidates"] == ["Ketu", "Venus"]
    assert with_ketu["rudra"] == "Venus"
    assert with_ketu["rudra_rasi"] == "Capricorn"
    assert {t["rasi"] for t in with_ketu["trishoola"]} == {
        "Capricorn", "Taurus", "Virgo"}

    default = rudra(lagna_sign, signs, longitudes)
    assert default["candidates"] == ["Mars", "Venus"]
    assert default["rudra"] == "Venus"          # the same Rudra either way


def test_the_co_lord_choice_flips_the_longevity_category():
    """OI-135, and why it is not cosmetic. §14.4's first pair is "lagna and
    8th lord": Mars in Aries with Mars in Aries is movable+movable and gives
    long life; Mars with Ketu in Sagittarius is movable+dual and gives short.
    Only the second matches the book — "lagna and 8th lord show short life" —
    and only short life selects the dasa the native died in.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import three_pairs
    from hora.core.const import Graha

    _longitudes, signs, lagna_sign = _chart_40()
    hl = book_signs(40)["HL"]

    default = three_pairs(lagna_sign, signs, hl)
    assert default["eighth_house"]["lord_used"] == "Mars"
    assert default["eighth_house"]["lord_was_chosen"] is True
    assert "Examples 85 and 87" in default["eighth_house"]["co_lord_note"]
    assert default["category"] == "long"

    as_printed = three_pairs(lagna_sign, signs, hl,
                             {R["Scorpio"]: int(Graha.KETU)})
    assert as_printed["eighth_house"]["lord_used"] == "Ketu"
    assert [p["category"] for p in as_printed["pairs"]] == [
        "short", "short", "long"]
    assert as_printed["category"] == "short"


def test_short_life_is_what_picks_capricorn_over_taurus_and_virgo():
    """"That is why death came in Cp dasa and not in Ta or Vi dasa."

    The book contrasts all three spikes outright — the clearest statement of
    closed OI-132's rule anywhere, and the third chart to confirm it. Of
    Capricorn 17-24, Taurus 48-56 and Virgo 80-89, only Capricorn falls in the
    0-36 a short life gives, and the native died at 22.
    """
    from hora.core.constants.maraka import LONGEVITY_RANGES
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    assert LONGEVITY_RANGES["short"] == (0, 36)
    run = progression(R["Scorpio"], _chart_40_seed_occupants())
    got = select_trishoola(R["Capricorn"], run, "short")

    spans = {row["rasi"]: (row["starts"], row["ends"])
             for row in got["trishoolas"]}
    assert spans == {"Capricorn": (17, 24), "Taurus": (48, 56),
                     "Virgo": (80, 89)}
    assert got["selected"]["rasi"] == "Capricorn"
    assert got["undecided"] is None
    assert got["selected"]["starts"] <= 22 < got["selected"]["ends"]


def test_a_long_life_would_have_selected_virgo_instead():
    """Why the co-lord choice and the longevity category are one question. Had
    the first pair been read with Mars, the category would be long life, and
    the rule would name Virgo at 80-89 — a dasa this native never reached.
    """
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    run = progression(R["Scorpio"], _chart_40_seed_occupants())
    long_life = select_trishoola(R["Capricorn"], run, "long")
    assert long_life["selected"]["rasi"] == "Virgo"
    assert long_life["selected"]["starts"] == 80


def test_example_87_states_a_negative_no_other_example_does():
    """"Antardasa at the time of death does not follow the principles
    explained here, but dasa follows the Trishoola principle."

    So §22.2.2's two antardasa principles are not necessary conditions — "can
    bring death" is the whole of that claim. Examples 84, 85 and 86 each had
    at least one of them; this one has neither, and the author says so.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        ANTARDASA_AT_DEATH_RULE,
        ANTARDASA_PRINCIPLES_CAN_FAIL,
    )

    assert "does not follow the principles" in ANTARDASA_PRINCIPLES_CAN_FAIL
    assert "dasa follows the Trishoola principle" in (
        ANTARDASA_PRINCIPLES_CAN_FAIL)
    assert "can be" in ANTARDASA_AT_DEATH_RULE


def test_chapter_22s_four_charts_and_what_each_settled():
    """The chapter end to end: one chart it cannot reach, and three it can.
    Chart 8 is the seed that contradicts the cascade, Chart 39 the one that
    shows the working, Chart 40 the one that adds a rule §22.2.1 omits.
    """
    from hora.charts.book import is_recomputable, numbers

    assert {8, 39, 40} <= set(numbers())
    assert all(is_recomputable(n) for n in (8, 39, 40))
    assert 61 not in numbers()


# --------------------------------------------------------------------------
# Example 88 — Chart 41, the Saturn exception again and footnote 61.
# --------------------------------------------------------------------------

EX88_ORDER = ["Cp", "Aq", "Pi", "Ar", "Ta", "Ge", "Cn", "Le", "Vi"]


def _chart_41():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(41).items()},
            {int(g): sign for g, sign in graha_signs(41).items()},
            lagna(41))


def _chart_41_run():
    from hora.dasha.rasi.niryaana_shoola import progression

    _longitudes, signs, _lagna = _chart_41()
    occupants = {g for g, sign in signs.items() if sign == R["Capricorn"]}
    return progression(R["Capricorn"], occupants)


def test_chart_41_recomputes_and_is_a_fourteenth_vote_for_the_mean_node():
    """Everything inside one arcminute, ascendant included — and Rahu is 98'
    out under `true`, the widest margin in the register, past Chart 39's 96'.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(41)
    place = Place(name="Chart 41", **record["place"])
    printed = longitudes(41)

    computed = compute_chart(from_local(**record["birth_data"]), place,
                             Settings(node_type=NodeType.MEAN))
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 1.0

    true_node = compute_chart(from_local(**record["birth_data"]), place,
                              Settings(node_type=NodeType.TRUE))
    error = abs(true_node.positions[int(Graha.RAHU)].longitude
                - printed["Rahu"]) * 60
    assert error > 90.0


def test_charts_40_and_41_share_a_birthplace():
    """Same coordinates, twenty-five years apart. Worth pinning because the
    two are the chapter's pair of Saturn-exception charts and a transposed
    place would quietly break one of them.
    """
    from hora.charts.book import chart

    assert chart(40)["place"] == chart(41)["place"]
    assert chart(40)["birth_data"]["year"] - chart(41)["birth_data"][
        "year"] == 25


def test_example_88s_rudra_is_saturn_by_conjunctions():
    """"The 8th lords from Ge and Sg are Saturn and Moon. Saturn is stronger
    and becomes Rudra. Trishoola is in Ta, Vi and Cp."

    Gemini and Sagittarius are both odd, so Table 32 and the ordinary count
    agree again and OI-134 stays untouched. Saturn wins on cascade step 1 with
    two companions in Capricorn against the Moon's one in Aries.
    """
    from hora.charts.maraka import ordinary_eighth, rudra, rudra_eighth

    for sign in (R["Gemini"], R["Sagittarius"]):
        assert rudra_eighth(sign) == ordinary_eighth(sign)
    assert rudra_eighth(R["Gemini"]) == R["Capricorn"]
    assert rudra_eighth(R["Sagittarius"]) == R["Cancer"]

    longitudes, signs, lagna_sign = _chart_41()
    assert lagna_sign == R["Gemini"]
    body = rudra(lagna_sign, signs, longitudes)

    assert body["candidates"] == ["Saturn", "Moon"]
    assert body["rudra"] == "Saturn"
    assert body["rudra_rasi"] == "Capricorn"
    assert body["decided_by"] == 1
    assert "Saturn conjoins 2 planets" in body["why"]
    assert {t["rasi"] for t in body["trishoola"]} == {
        "Capricorn", "Taurus", "Virgo"}


def test_the_eighth_house_wins_the_seed_for_the_first_time():
    """"The 8th house is stronger than the 2nd house and it starts dasas."

    §15.5.2 rule 1 for the fifth time in the chapter, and the first time the
    8th takes it — Capricorn holds three planets and Cancer none. The chapter
    has now seeded from both halves of its own pair.
    """
    from hora.charts.rasi_strength import stronger

    longitudes, _signs, lagna_sign = _chart_41()
    verdict = stronger((lagna_sign + 1) % 12, (lagna_sign + 7) % 12,
                       longitudes, purpose="phalita")

    assert verdict.winner == R["Capricorn"]
    assert verdict.decided_by == "1"
    assert "Capricorn contains 3 planets" in verdict.reason


def test_the_saturn_exception_fires_a_second_time():
    """"As Cp is an even rasi, dasas normally go as Cp, Sg, Sc etc. Here they
    go as Cp, Aq, Pi, Ar etc, due to Saturn's presence in Cp."

    The second chart to run it, and the second time the module's plain output
    is the sequence the example calls normal before overriding it.
    """
    from hora.dasha.rasi.niryaana_shoola import progression

    plain = progression(R["Capricorn"])
    assert plain.direction == "backward"
    assert [ABBR[s] for s in plain.signs[:3]] == ["Cp", "Sg", "Sc"]

    got = _chart_41_run()
    assert got.direction == "forward"
    assert got.exception == "Saturn"
    assert [ABBR[s] for s in got.signs[:4]] == ["Cp", "Aq", "Pi", "Ar"]


def test_saturn_shares_the_seed_here_where_he_had_it_alone_on_chart_40():
    """Chart 40's Scorpio held Saturn only; Chart 41's Capricorn holds him
    with Jupiter and Venus. The exception reads his presence, not his
    solitude, and the pair of charts shows it.
    """
    from hora.core.const import Graha

    _longitudes, signs, _lagna = _chart_41()
    occupants = {g for g, sign in signs.items() if sign == R["Capricorn"]}
    assert occupants == {int(Graha.JUPITER), int(Graha.VENUS),
                         int(Graha.SATURN)}
    assert _chart_41_run().exception == "Saturn"


def test_virgo_dasa_starts_after_63_years_and_holds_the_death():
    """"We can see that Vi dasa starts after 63 years (7+8+9+7+8+9+7+8). So Vi
    dasa runs during March 1965-March 1974."

    Born March 1902, died 1967 at 65 — inside it.
    """
    from hora.charts.book import chart

    born = chart(41)["birth_data"]
    assert (born["year"], born["month"]) == (1902, 3)

    got = _chart_41_run()
    assert [ABBR[s] for s in got.signs[:9]] == EX88_ORDER

    index = got.signs.index(R["Virgo"])
    assert sum(got.years[:index]) == 63 == 7 + 8 + 9 + 7 + 8 + 9 + 7 + 8
    assert got.starts[index] == 63
    assert got.years[index] == 9
    assert born["year"] + 63 == 1965
    assert born["year"] + 63 + 9 == 1974
    assert got.starts[index] <= 65 < got.starts[index] + got.years[index]

    # Vi is one of the three spikes, which is the whole of the example's claim.
    assert R["Virgo"] in (R["Capricorn"], R["Taurus"], R["Virgo"])


def test_footnote_61s_thumbrule_holds_for_every_block_of_three():
    """"The sum of the first 3 dasas is always 24 years (7+8+9). The sum of
    the next 3 dasas is also 24 years."

    It holds because any three **consecutive** rasis are one movable, one
    fixed and one dual, in either direction — so the block is 7+8+9 whatever
    the seed is and whichever way the Saturn exception sends the run.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import (
        CONSECUTIVE_TRIPLE_YEARS,
        THUMBRULE_FOOTNOTE_61,
        progression,
    )

    assert CONSECUTIVE_TRIPLE_YEARS == 24 == 7 + 8 + 9
    assert "always 24 years" in THUMBRULE_FOOTNOTE_61

    for seed in range(12):
        for occupants in (None, {int(Graha.SATURN)}):
            got = progression(seed, occupants)
            for start in range(10):
                assert sum(got.years[start:start + 3]) == 24, (seed, start)


def test_the_thumbrule_is_why_the_cycle_is_96_years():
    """Four blocks of three, each 24. Stated here because the two constants
    are otherwise two unrelated facts.
    """
    from hora.core.const import MODALITY_NAMES, RASI_MODALITY
    from hora.dasha.rasi.niryaana_shoola import (
        CONSECUTIVE_TRIPLE_YEARS,
        cycle_years,
    )

    assert cycle_years() == 4 * CONSECUTIVE_TRIPLE_YEARS == 96

    for start in range(12):
        block = {str(MODALITY_NAMES[RASI_MODALITY[(start + n) % 12]])
                 for n in range(3)}
        assert block == {"chara", "sthira", "dwiswabhava"}


def test_chart_41_is_the_first_with_two_trishoolas_in_one_range():
    """OI-133, which Example 84's "only" left open. Capricorn 0-7, Taurus
    31-39 and Virgo 63-72: a short life catches Capricorn *and* Taurus, and a
    middle life catches Taurus *and* Virgo. The loose reading selects neither.
    """
    from hora.charts.maraka import rudra
    from hora.dasha.rasi.niryaana_shoola import select_trishoola

    longitudes, signs, lagna_sign = _chart_41()
    rudra_sign = rudra(lagna_sign, signs, longitudes)["rudra_sign"]
    run = _chart_41_run()

    spans = {row["rasi"]: (row["starts"], row["ends"])
             for row in select_trishoola(rudra_sign, run, "short")[
                 "trishoolas"]}
    assert spans == {"Capricorn": (0, 7), "Taurus": (31, 39),
                     "Virgo": (63, 72)}

    for category, both in (("short", {"Capricorn", "Taurus"}),
                           ("middle", {"Taurus", "Virgo"})):
        got = select_trishoola(rudra_sign, run, category)
        assert {r["rasi"] for r in got["trishoolas"] if r["in_range"]} == both
        assert got["selected"] is None
        assert "2 of the three" in got["undecided"]


def test_reading_the_range_strictly_resolves_every_such_case():
    """OI-133's candidate fix. "Comes in the range" read as falling **wholly**
    inside it leaves exactly one in 396 of the 432 combinations and never two,
    where the loose reading leaves two on 72 of them. On Chart 41 it picks
    Virgo 63-72 out of a middle life — the dasa that killed at 65.

    Reported beside the loose reading, not substituted for it: no example
    tests a Trishoola dasa straddling a boundary.
    """
    from collections import Counter

    from hora.charts.maraka import rudra
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    longitudes, signs, lagna_sign = _chart_41()
    rudra_sign = rudra(lagna_sign, signs, longitudes)["rudra_sign"]
    middle = select_trishoola(rudra_sign, _chart_41_run(), "middle")
    assert middle["selected"] is None
    assert middle["selected_wholly_in_range"]["rasi"] == "Virgo"
    assert middle["selected_wholly_in_range"]["starts"] == 63

    loose, strict = Counter(), Counter()
    for seed in range(12):
        run = progression(seed)
        for rudra_rasi in range(12):
            for category in ("short", "middle", "long"):
                rows = select_trishoola(rudra_rasi, run, category)[
                    "trishoolas"]
                loose[sum(r["in_range"] for r in rows)] += 1
                strict[sum(r["wholly_in_range"] for r in rows)] += 1

    assert dict(loose) == {1: 324, 2: 72, 0: 36}
    assert dict(strict) == {1: 396, 0: 36}


def test_all_four_worked_trishoolas_are_wholly_inside_their_range():
    """Which is why the strict reading costs nothing: every Trishoola the book
    names sits entirely within its category's years.
    """
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    cases = [
        (R["Gemini"], progression(R["Sagittarius"]), "middle", "Gemini"),
        (R["Leo"], progression(R["Virgo"]), "middle", "Aries"),
        (R["Capricorn"], progression(R["Scorpio"],
                                     _chart_40_seed_occupants()), "short",
         "Capricorn"),
    ]
    for rudra_sign, run, category, expected in cases:
        got = select_trishoola(rudra_sign, run, category)
        assert got["selected"]["rasi"] == expected
        assert got["selected_wholly_in_range"] == got["selected"]


# --------------------------------------------------------------------------
# Exercise 31 — Chart 42, solved before the book's answer.
# --------------------------------------------------------------------------

#: The twelve dasas the exercise's chart produces, and the ages they open at.
EX31_RUN = [("Sc", 8, 0), ("Li", 7, 8), ("Vi", 9, 15), ("Le", 8, 24),
            ("Cn", 7, 32), ("Ge", 9, 39), ("Ta", 8, 48), ("Ar", 7, 56),
            ("Pi", 9, 63), ("Aq", 8, 72), ("Cp", 7, 80), ("Sg", 9, 87)]


def _chart_42():
    from hora.charts.book import graha_longitudes, graha_signs, lagna

    return ({int(g): lon for g, lon in graha_longitudes(42).items()},
            {int(g): sign for g, sign in graha_signs(42).items()},
            lagna(42))


def test_chart_42_recomputes_and_is_a_fifteenth_vote_for_the_mean_node():
    """Every body inside one arcminute bar the Sun at 1.02', which is the
    book's own arcminute rounding rather than a disagreement. Rahu is 58' out
    under `true`.
    """
    from hora.charts.book import GRAHA_OF, chart, longitudes
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(42)
    place = Place(name="Chart 42", **record["place"])
    printed = longitudes(42)

    computed = compute_chart(from_local(**record["birth_data"]), place,
                             Settings(node_type=NodeType.MEAN))
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.1, f"{name}: {error:.2f}'"
    assert abs(computed.lagna_longitude - printed["Asc"]) * 60 < 1.0

    true_node = compute_chart(from_local(**record["birth_data"]), place,
                              Settings(node_type=NodeType.TRUE))
    assert abs(true_node.positions[int(Graha.RAHU)].longitude
               - printed["Rahu"]) * 60 > 50.0


def test_exercise_31_step_1_the_three_pairs_all_disagree():
    """"Using the method of three pairs, estimate his longevity category."

    The only chart in the register whose three pairs give three different
    answers, which is the case §14.4 breaks with a preferred pair: the Moon is
    in neither lagna nor the 7th, so lagna and Horalagna decide — **middle
    life, 36-72**.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import three_pairs
    from hora.core.const import Graha

    _longitudes, signs, lagna_sign = _chart_42()
    assert lagna_sign == R["Libra"]

    got = three_pairs(lagna_sign, signs, book_signs(42)["HL"])
    assert [p["category"] for p in got["pairs"]] == ["long", "short", "middle"]
    assert len({p["category"] for p in got["pairs"]}) == 3

    assert signs[int(Graha.MOON)] not in (lagna_sign, (lagna_sign + 6) % 12)
    assert "prefers lagna and Horalagna" in got["reason"]
    assert got["category"] == "middle"
    assert tuple(got["range_years"]) == (36, 72)


def test_exercise_31_step_2_rudra_is_in_aries_whichever_co_lord_is_taken():
    """Rudra is the stronger of the 8th lords from Libra and Aries — Venus,
    and Scorpio's, which OI-135 leaves open. Venus and Mars both sit in Aries,
    and so does Ketu's alternative, so the **rasi** is Aries either way and
    the Trishoolas are Ar, Le and Sg. OI-135 does not bite here.
    """
    from hora.charts.maraka import rudra, rudra_eighth
    from hora.core.const import Graha

    longitudes, signs, lagna_sign = _chart_42()
    assert rudra_eighth(R["Libra"]) == R["Taurus"]
    assert rudra_eighth(R["Aries"]) == R["Scorpio"]

    default = rudra(lagna_sign, signs, longitudes)
    with_ketu = rudra(lagna_sign, signs, longitudes,
                      {R["Scorpio"]: int(Graha.KETU)})

    assert default["candidates"] == ["Venus", "Mars"]
    assert with_ketu["candidates"] == ["Venus", "Ketu"]
    assert default["rudra_rasi"] == with_ketu["rudra_rasi"] == "Aries"
    for body in (default, with_ketu):
        assert {t["rasi"] for t in body["trishoola"]} == {
            "Aries", "Leo", "Sagittarius"}


def test_exercise_31_step_3_the_seed_is_scorpio_by_rule_2():
    """Both candidates are empty of planets, so rule 1 ties for the first time
    in the chapter and rule 2 decides: Mercury and Scorpio's co-lord Mars both
    aspect it from Aries, and nothing reaches Taurus. No Saturn in the seed,
    so the run is the plain backward one an even rasi gives.
    """
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.niryaana_shoola import progression

    longitudes, signs, lagna_sign = _chart_42()
    verdict = stronger((lagna_sign + 1) % 12, (lagna_sign + 7) % 12,
                       longitudes, purpose="phalita")

    assert verdict.rules[0].winner is None            # rule 1 ties
    assert verdict.winner == R["Scorpio"]
    assert verdict.decided_by == "2"
    assert "co-lord (Mars) aspects from Aries" in verdict.reason

    occupants = {g for g, sign in signs.items() if sign == R["Scorpio"]}
    assert occupants == set()
    got = progression(R["Scorpio"], occupants)
    assert got.direction == "backward"
    assert got.exception is None
    assert [(ABBR[s], y, start) for s, y, start in
            zip(got.signs, got.years, got.starts)] == EX31_RUN


def test_exercise_31_step_4_aries_is_the_trishoola_in_the_middle_range():
    """"Then identify the dasa of a Trishoola rasi falling in that longevity
    category."

    Leo runs 24-32 and Sagittarius 87-96; only Aries at 56-63 lies in 36-72,
    and it lies wholly inside, so the loose and strict readings of OI-133
    agree. Born 20 April 1889, that dasa is **20 April 1945 to 20 April 1952**.
    """
    from hora.charts.book import chart
    from hora.dasha.rasi.niryaana_shoola import progression, select_trishoola

    born = chart(42)["birth_data"]
    assert (born["year"], born["month"], born["day"]) == (1889, 4, 20)

    run = progression(R["Scorpio"])
    got = select_trishoola(R["Aries"], run, "middle")
    spans = {row["rasi"]: (row["starts"], row["ends"])
             for row in got["trishoolas"]}
    assert spans == {"Aries": (56, 63), "Leo": (24, 32),
                     "Sagittarius": (87, 96)}

    assert got["selected"]["rasi"] == "Aries"
    assert got["selected_wholly_in_range"] == got["selected"]
    assert born["year"] + 56 == 1945
    assert born["year"] + 63 == 1952


def test_exercise_31_step_5_the_antardasas_of_aries():
    """§18.3 by way of §22.2.1's borrowing. Aries beats Libra on rule 1 with
    four planets to none, its lord Mars is in Aries itself, and Aries is odd —
    so the antardasas start there and run forward, seven months each.
    """
    from hora.charts.rasi_strength import stronger
    from hora.dasha.rasi.narayana import antardasas

    longitudes, _signs, _lagna = _chart_42()
    verdict = stronger(R["Aries"], R["Libra"], longitudes, purpose="phalita")
    assert verdict.winner == R["Aries"]
    assert "Aries contains 4 planets" in verdict.reason

    got = antardasas(R["Aries"], 7, longitudes)
    assert got.seed == got.start == R["Aries"]
    assert got.direction == "forward"
    assert got.months_each == 7
    assert [ABBR[s] for s in got.signs[:3]] == ["Ar", "Ta", "Ge"]
    assert got.signs[7] == R["Scorpio"]          # the 8th


def test_exercise_31_step_6_which_antardasa_the_principles_point_to():
    """"Try to guess the antardasa of death."

    §22.2.2's two principles pick **Scorpio** and nothing else: it is the 8th
    from Aries, and it is where the 8th lord sits in navamsa — Mars and Ketu
    both land in Scorpio there, so OI-135 does not bite here either. That is
    the section's "strong candidate", the 8th antardasa, **20 May 1949 to
    20 December 1949**.
    """
    from hora.charts.book import longitudes as book_longitudes
    from hora.charts.vargas import varga
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    printed = book_longitudes(42)
    for name in ("Mars", "Ketu"):
        assert varga(printed[name], "D9").sign == R["Scorpio"], name

    for lord in (int(Graha.MARS), int(Graha.KETU)):
        got = antardasa_candidates(R["Aries"], {lord: R["Scorpio"]},
                                   eighth_lord=lord)
        assert got["eighth_name"] == "Scorpio"
        assert got["from_dasa_rasi_names"] == (
            "Virgo", "Libra", "Scorpio", "Pisces")
        assert got["aspecting_names"] == (
            "Scorpio", "Aries", "Cancer", "Capricorn")
        assert got["strong_candidate_names"] == ("Scorpio",)

    opens = 1945 * 12 + 3 + 7 * 7      # April 1945 zero-based, plus seven
    assert divmod(opens, 12) == (1949, 4)          # May 1949
    assert divmod(opens + 7, 12) == (1949, 11)     # December 1949


def test_exercise_31_the_first_antardasa_meets_the_second_principle_only():
    """The other candidate worth naming. Aries itself is not the 6th, 7th, 8th
    or 12th from Aries, but it **does** aspect Scorpio, so it satisfies the
    second principle alone — the shape Example 85's Taurus had. It is the
    antardasa the dasa opens with, 20 April to 20 November 1945.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Aries"], {int(Graha.MARS): R["Scorpio"]},
                               eighth_lord=int(Graha.MARS))
    assert R["Aries"] not in got["from_dasa_rasi"]
    assert R["Aries"] in got["aspecting_the_navamsa_rasi"]

    opens = 1945 * 12 + 3
    assert divmod(opens, 12) == (1945, 3)          # April 1945
    assert divmod(opens + 7, 12) == (1945, 10)     # November 1945


# -- Exercise 31's answer ---------------------------------------------------

def test_exercise_31s_answer_confirms_every_step_but_the_antardasa():
    """The answer, against what we derived before seeing it.

    Longevity, Rudra, the Trishoolas, the seed, the direction and the dasa all
    match. The antardasa does not: we backed Scorpio, which the answer agrees
    is "the strongest candidate", and it then says the death fell in Aries for
    a reason outside §22.2.2's two principles.
    """
    from hora.charts.book import chart

    assert chart(42)["events"] == {
        "committed suicide": "April 30, 1945, aged 56"}

    ours = {
        "longevity": "middle", "rudra_rasi": "Aries",
        "trishoolas": ("Aries", "Leo", "Sagittarius"),
        "seed": "Scorpio", "direction": "backward", "dasa": "Aries",
        "antardasa": "Scorpio",
    }
    book = dict(ours, antardasa="Aries")
    assert {k: v for k, v in ours.items() if k != "antardasa"} == {
        k: v for k, v in book.items() if k != "antardasa"}
    assert ours["antardasa"] != book["antardasa"]


def test_the_answer_states_the_three_way_tiebreak_we_had_implemented():
    """"When there is a three-way tie, we use the Moon-Saturn pair if Moon is
    in lagna or 7th. That is not the case here. So we use the lagna and
    horalagna pair."

    Chapter 14 gave that rule and Exercise 31 is the first chart to need it.
    Our reason string says the same thing.
    """
    from hora.charts.book import signs as book_signs
    from hora.charts.maraka import three_pairs
    from hora.core.constants.maraka import THREE_PAIRS_TIEBREAK_RULE

    _longitudes, signs, lagna_sign = _chart_42()
    got = three_pairs(lagna_sign, signs, book_signs(42)["HL"])
    assert got["category"] == "middle"
    assert "prefers lagna and Horalagna" in got["reason"]
    assert "Moon" in THREE_PAIRS_TIEBREAK_RULE


def test_the_answer_takes_mars_not_ketu_as_the_second_rudra_candidate():
    """"The 8th lord, Venus, and 8th lord from 7th, Mars, are in Aries."

    Scorpio's co-lordship is OI-135's question and the answer does not raise
    it — it names Mars. §15.5.1 agrees here, and in any case both sit in
    Aries, which is all the Trishoolas need.
    """
    from hora.charts.colord import stronger as stronger_co_lord
    from hora.charts.maraka import rudra
    from hora.core.const import Graha

    longitudes, signs, lagna_sign = _chart_42()
    assert stronger_co_lord(R["Scorpio"], longitudes,
                            purpose="arudha").winner == int(Graha.MARS)

    body = rudra(lagna_sign, signs, longitudes)
    assert body["candidates"] == ["Venus", "Mars"]
    assert signs[int(Graha.VENUS)] == signs[int(Graha.MARS)] == R["Aries"]
    assert body["rudra_rasi"] == "Aries"


def test_the_answer_works_the_dasa_start_with_footnote_61s_thumbrule():
    """"Ar dasa starts after 56 years (56=24+24+8; 24 years for Sc, Li and Vi;
    24 years for Le, Cn and Ge; 8 years for Ta)."

    The thumbrule used rather than stated — two blocks of three and one
    remainder, which is how it is meant to save the arithmetic.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        CONSECUTIVE_TRIPLE_YEARS,
        progression,
    )

    got = progression(R["Scorpio"])
    assert sum(got.years[0:3]) == CONSECUTIVE_TRIPLE_YEARS == 24
    assert sum(got.years[3:6]) == 24
    assert got.years[6] == 8                       # Taurus, the remainder
    assert 24 + 24 + 8 == 56 == got.starts[got.signs.index(R["Aries"])]


def test_the_dasa_year_is_365_25_days_not_the_calendar_anniversary():
    """"So Ar dasa starts on April 21, 1945." Born 20 April 1889 at 18:30, so
    the 56th anniversary is the **20th**. Only a fixed 365.25-day year lands
    on the 21st — and it reproduces the birth time to the minute. Our sidereal
    default gives the 22nd, and savana lands more than eight months early.
    """
    import swisseph as swe

    from hora.charts.book import chart
    from hora.core.constants.timespan import (
        SAVANA_YEAR_DAYS,
        SIDEREAL_YEAR_DAYS,
    )
    from hora.core.timeutil import from_local
    from hora.dasha.rasi.niryaana_shoola import (
        THE_DASA_YEAR_IS_NOT_THE_CALENDAR_ANNIVERSARY,
        dasa_periods,
    )

    record = chart(42)
    birth = from_local(**record["birth_data"])
    offset = record["birth_data"]["utc_offset_hours"] / 24.0

    def local(jd):
        year, month, day, hour = swe.revjul(jd + offset)
        return (int(year), int(month), int(day), int(hour))

    aries = next(row for row in dasa_periods(R["Scorpio"], birth.jd_ut)
                 if row["rasi"] == "Aries")
    assert local(aries["start_jd"])[:3] == (1945, 4, 21)
    assert local(aries["start_jd"])[3] == 18            # the birth hour
    assert local(aries["end_jd"])[:3] == (1952, 4, 21)

    assert local(birth.jd_ut + 56 * SIDEREAL_YEAR_DAYS)[:3] == (1945, 4, 22)
    assert local(birth.jd_ut + 56 * SAVANA_YEAR_DAYS)[:2] == (1944, 7)

    assert "April 21, 1945" in THE_DASA_YEAR_IS_NOT_THE_CALENDAR_ANNIVERSARY


def test_the_death_falls_in_the_first_antardasa():
    """"the native died in Aries antardasa itself (April 21, 1945-Nov 21,
    1945)" and history puts the suicide on 30 April 1945 — nine days in.
    """
    import swisseph as swe

    from hora.charts.book import chart
    from hora.core.timeutil import from_local
    from hora.dasha.rasi.narayana import antardasas
    from hora.dasha.rasi.niryaana_shoola import (
        antardasa_periods,
        dasa_periods,
    )

    record = chart(42)
    birth = from_local(**record["birth_data"])
    longitudes, _signs, _lagna = _chart_42()

    aries = next(row for row in dasa_periods(R["Scorpio"], birth.jd_ut)
                 if row["rasi"] == "Aries")
    order = antardasas(R["Aries"], 7, longitudes).signs
    periods = antardasa_periods(aries, order)

    assert periods[0]["rasi"] == "Aries"
    death = swe.julday(1945, 4, 30, 12.0)
    assert periods[0]["start_jd"] <= death < periods[0]["end_jd"]
    assert periods[7]["rasi"] == "Scorpio"           # our answer, not reached
    assert death < periods[7]["start_jd"]


def test_the_antardasa_boundary_cannot_be_pinned_to_the_day():
    """OI-136. Equal twelfths put the first antardasa's end at 20 November
    19:59; seven calendar months put it at 21 November, which is what the
    answer prints. Four hours apart, so either rounds to it.
    """
    import swisseph as swe

    from hora.charts.book import chart
    from hora.core.timeutil import from_local
    from hora.dasha.rasi.narayana import antardasas
    from hora.dasha.rasi.niryaana_shoola import (
        ANTARDASA_BOUNDARY_IS_A_DAY_UNDECIDED,
        antardasa_periods,
        dasa_periods,
    )

    record = chart(42)
    birth = from_local(**record["birth_data"])
    longitudes, _signs, _lagna = _chart_42()
    aries = next(row for row in dasa_periods(R["Scorpio"], birth.jd_ut)
                 if row["rasi"] == "Aries")
    order = antardasas(R["Aries"], 7, longitudes).signs

    end = antardasa_periods(aries, order)[0]["end_jd"]
    offset = record["birth_data"]["utc_offset_hours"] / 24.0
    year, month, day, hour = swe.revjul(end + offset)
    assert (int(year), int(month), int(day)) == (1945, 11, 20)
    assert int(hour) == 19
    assert 24 - hour < 5                    # within four hours of the 21st

    assert "Nov 21, 1945" in ANTARDASA_BOUNDARY_IS_A_DAY_UNDECIDED


def test_the_answer_reads_marakas_at_the_antardasa_level():
    """"Aries not only contains Rudra, but it is also the 7th house and it
    contains 2nd, 7th and 8th lords. It is a strong maraka sthana."

    §22.2.2 gives rule 1 for **dasas** and two other principles for
    antardasas. The answer reaches back to rule 1 one level down, and adds
    Rudra's own rasi, which the section names only through the Trishoolas.
    `maraka_readings` already returns Aries as a maraka sthana holding Mars.
    """
    from hora.core.const import RASI_LORD, Graha
    from hora.dasha.rasi.niryaana_shoola import (
        EXERCISE_31_READS_MARAKAS_AT_THE_ANTARDASA_LEVEL,
        maraka_readings,
    )

    _longitudes, signs, lagna_sign = _chart_42()
    got = maraka_readings(R["Aries"], lagna_sign, signs)

    assert got["is_maraka_sthana"] == (7,)          # Aries is the 7th
    assert got["applies"]
    holders = {entry["graha_name"] for entry in got["holds_maraka_grahas"]}
    assert "Mars" in holders

    for house in (2, 7, 8):
        lord = int(RASI_LORD[(lagna_sign + house - 1) % 12])
        assert signs[lord] == R["Aries"], house
    assert signs[int(Graha.VENUS)] == R["Aries"]    # the 8th lord, not a maraka

    assert "strong maraka sthana" in (
        EXERCISE_31_READS_MARAKAS_AT_THE_ANTARDASA_LEVEL)


def test_the_answer_agrees_that_scorpio_was_the_methods_candidate():
    """"Of these, Sc is the strongest candidate as it is also the 8th from
    dasa rasi Aries."

    So the two principles were applied correctly and simply did not pick the
    antardasa that killed — which is why the exercise says "antardasa is tough
    to guess" rather than giving a rule.
    """
    from hora.core.const import Graha
    from hora.dasha.rasi.niryaana_shoola import antardasa_candidates

    got = antardasa_candidates(R["Aries"], {int(Graha.MARS): R["Scorpio"]},
                               eighth_lord=int(Graha.MARS))
    assert got["aspecting_names"] == (
        "Scorpio", "Aries", "Cancer", "Capricorn")
    assert got["strong_candidate_names"] == ("Scorpio",)


# --------------------------------------------------------------------------
# §22.3 Conclusion
# --------------------------------------------------------------------------

def test_22_3_claims_more_for_the_dasa_than_22_1_did():
    """§22.1: "one of the most reliable dasa systems for the timing of
    death". §22.3: "this dasa is the best for timing death."

    The chapter opens with a comparative and closes with a superlative. Both
    are stored — it says two things and neither is a slip.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        ONE_OF_THE_MOST_RELIABLE,
        THIS_DASA_IS_THE_BEST_FOR_TIMING_DEATH,
    )

    assert "one of the most reliable" in ONE_OF_THE_MOST_RELIABLE
    assert "is the best for timing death" in (
        THIS_DASA_IS_THE_BEST_FOR_TIMING_DEATH)
    assert "humble opinion" in THIS_DASA_IS_THE_BEST_FOR_TIMING_DEATH


def test_the_trishoola_claim_keeps_its_hedge_in_both_places():
    """"Usually death occurs in the dasa of a Trishoola rasi" in §22.2.2, and
    "usually dasa of one of the three Trishoola rasis brings death" in §22.3.
    The word survives the conclusion, and §22.2.2's rule 3 is the fallback it
    implies.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        DEATH_READINGS,
        USUALLY_A_TRISHOOLA_BRINGS_DEATH,
    )

    assert USUALLY_A_TRISHOOLA_BRINGS_DEATH.startswith("Usually")
    assert DEATH_READINGS[1]["text"].startswith("Usually")
    assert DEATH_READINGS[2]["text"].startswith("If Trishoolas don't")


def test_the_chapter_declares_itself_incomplete_and_says_where():
    """"However, many special cases, exceptions and special rules mentioned by
    Maharshis were omited in this book. Timing of the antardasa of death
    wasn't given due attention."

    Two admissions, and each covers gaps we had already recorded. The printed
    "omited" is kept as printed.
    """
    from hora.dasha.rasi.niryaana_shoola import CHAPTER_22_IS_KNOWINGLY_PARTIAL

    assert "were omited in this book" in CHAPTER_22_IS_KNOWINGLY_PARTIAL
    assert "wasn't given due attention" in CHAPTER_22_IS_KNOWINGLY_PARTIAL
    assert "tip of an iceberg" in CHAPTER_22_IS_KNOWINGLY_PARTIAL
    assert "omitted" not in CHAPTER_22_IS_KNOWINGLY_PARTIAL


def test_the_admission_explains_four_open_items_and_closes_none():
    """Each row names something we found before reading §22.3 and the clause
    that accounts for it. Accounting for a missing rule does not supply it, so
    every one of them stays open.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        CHAPTER_22_IS_KNOWINGLY_PARTIAL,
        USUALLY_A_TRISHOOLA_BRINGS_DEATH,
        WHAT_THE_ADMISSION_ACCOUNTS_FOR,
    )

    items = {row["item"] for row in WHAT_THE_ADMISSION_ACCOUNTS_FOR}
    assert items == {"OI-134", "OI-133", "OI-136", "Exercise 31"}

    section = (USUALLY_A_TRISHOOLA_BRINGS_DEATH + " "
               + CHAPTER_22_IS_KNOWINGLY_PARTIAL)
    for row in WHAT_THE_ADMISSION_ACCOUNTS_FOR:
        stem = row["covered_by"].split("...")[-1].strip()
        assert stem in section, row["item"]

    open_items = (OPEN_ITEMS.read_text(encoding="utf-8")
                  if OPEN_ITEMS.exists() else "")
    for name in ("OI-134", "OI-133", "OI-136"):
        assert f"### {name} " in open_items, name


def test_the_scorpio_against_aries_miss_is_the_books_own_admission():
    """Exercise 31's two principles pick Scorpio and the death came in Aries.
    §22.3 says why: "Timing of the antardasa of death wasn't given due
    attention." So the miss is the chapter describing itself, not a defect to
    be reconciled — and no antardasa rule is invented to cover it.
    """
    from hora.dasha.rasi.niryaana_shoola import (
        ANTARDASA_AT_DEATH_RULE,
        CHAPTER_22_IS_KNOWINGLY_PARTIAL,
        EXERCISE_31_READS_MARAKAS_AT_THE_ANTARDASA_LEVEL,
        WHAT_THE_ADMISSION_ACCOUNTS_FOR,
    )

    row = next(r for r in WHAT_THE_ADMISSION_ACCOUNTS_FOR
               if r["item"] == "Exercise 31")
    assert "Scorpio" in row["is"] and "Aries" in row["is"]
    assert row["covered_by"] in CHAPTER_22_IS_KNOWINGLY_PARTIAL

    # The two principles stay exactly as §22.2.2 prints them.
    assert "6th, 7th, 8th or 12th" in ANTARDASA_AT_DEATH_RULE
    assert "maraka" in EXERCISE_31_READS_MARAKAS_AT_THE_ANTARDASA_LEVEL


def test_chapter_22_is_finished_and_chapter_23_took_the_other_name():
    """§22.3 ends the chapter, and §22.1's "we will learn it in another
    chapter" is chapter 23. The two Shoola dasas live in two modules, which is
    the whole point of the rename.
    """
    from hora.core.constants.dasha import PART_2_DASA_SYSTEMS
    from hora.dasha.rasi.niryaana_shoola import THE_NAME_IS_DISAMBIGUATED

    assert "We will learn it in another chapter" in THE_NAME_IS_DISAMBIGUATED

    by_name = {s["name"]: s for s in PART_2_DASA_SYSTEMS}
    assert by_name["Shoola dasa"]["module"] == "hora.dasha.rasi.shoola"
    assert by_name["Niryaana Shoola dasa"]["module"] == (
        "hora.dasha.rasi.niryaana_shoola")
