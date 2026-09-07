"""Chapter 28 — techniques of Tajaka charts.

§28.1's muntha is arithmetic on rasis: the natal lagna progressed one rasi a
year. The section works one case and these tests hold it, along with the two
things it states and defers — why muntha ranks with lagna, and what the
author's own monthly rate is.
"""
from __future__ import annotations

import pytest


def test_28_1s_worked_case_reproduces():
    """"the natal chart has lagna in Sc ... So muntha is in Ge." """
    from hora.core.const import RASI_ABBR
    from hora.tajaka.muntha import MUNTHA_WORKED_CASE, muntha_rasi

    scorpio = RASI_ABBR.index("Sc")
    got = muntha_rasi(scorpio, 32)
    # "the 8th house from Sc (after expunging multiples of 12 from 32)"
    assert got["house_from_natal_lagna"] == 8
    assert RASI_ABBR[got["rasi"]] == "Ge"
    assert "So muntha is in Ge" in MUNTHA_WORKED_CASE
    # 32 mod 12 is 8, which is the section's own shortcut.
    assert 32 % 12 == got["house_from_natal_lagna"]


def test_the_first_year_puts_muntha_on_the_natal_lagna():
    from hora.tajaka.muntha import muntha_house_from_lagna, muntha_rasi

    for lagna in range(12):
        got = muntha_rasi(lagna, 1)
        assert got["rasi"] == lagna
        assert got["house_from_natal_lagna"] == 1
    assert muntha_house_from_lagna(1) == 1


def test_muntha_repeats_on_a_twelve_year_cycle():
    from hora.tajaka.muntha import (
        MUNTHA_REPEATS_ON_A_TWELVE_YEAR_CYCLE,
        muntha_house_from_lagna,
        muntha_rasi,
    )

    # A multiple of twelve puts it back, and the twelfth year is the 12th
    # house rather than the first — the count is inclusive.
    assert muntha_house_from_lagna(12) == 12
    assert muntha_house_from_lagna(13) == 1
    assert muntha_house_from_lagna(24) == 12
    for year in (1, 13, 25, 37):
        assert muntha_rasi(4, year)["rasi"] == 4
    seen = {muntha_rasi(4, year)["rasi"] for year in range(1, 13)}
    assert len(seen) == 12                    # every rasi once in a cycle
    assert "back to the natal lagna in the thirteenth year" in (
        MUNTHA_REPEATS_ON_A_TWELVE_YEAR_CYCLE)


def test_every_house_has_a_reading_and_the_grades_are_the_sections_own():
    from hora.tajaka.muntha import MUNTHA_HOUSE_RESULTS, MUNTHA_IN_HOUSES

    assert sorted(MUNTHA_HOUSE_RESULTS) == list(range(1, 13))
    grades = {house: row["grade"] for house, row in MUNTHA_HOUSE_RESULTS.items()}
    assert [h for h, g in grades.items() if g == "excellent"] == [9, 10, 11]
    assert [h for h, g in grades.items() if g == "good"] == [1, 2, 3, 5]
    assert [h for h, g in grades.items() if g == "bad"] == [4, 6, 7, 8, 12]

    # The "respectively" lists, in the order the section gives them.
    assert [MUNTHA_HOUSE_RESULTS[h]["gives"] for h in (9, 10, 11)] == [
        "prosperity", "status", "gains"]
    assert [MUNTHA_HOUSE_RESULTS[h]["gives"] for h in (1, 2, 3, 5)] == [
        "health", "wealth", "success", "fame"]
    assert [MUNTHA_HOUSE_RESULTS[h]["gives"] for h in (6, 8, 12)] == [
        "illness", "troubles", "expenditures"]
    for house in range(1, 13):
        assert MUNTHA_HOUSE_RESULTS[house]["gives"] in MUNTHA_IN_HOUSES


def test_the_muntha_houses_are_not_the_house_categories():
    """The trikonas and dusthanas follow chapter 7; the kendras and upachayas
    do not, so four houses have to be read from §28.1's own list.
    """
    from hora.core.const import DUSTHANA, KENDRA, TRIKONA, UPACHAYA
    from hora.tajaka.muntha import (
        MUNTHA_HOUSE_RESULTS,
        THE_MUNTHA_HOUSES_ARE_NOT_THE_HOUSE_CATEGORIES,
    )

    def grade(house: int) -> str:
        return MUNTHA_HOUSE_RESULTS[house]["grade"]

    assert all(grade(h) in ("good", "excellent") for h in TRIKONA)
    assert all(grade(h) == "bad" for h in DUSTHANA)
    # Kendras and upachayas each split.
    assert {grade(h) for h in KENDRA} == {"good", "bad", "excellent"}
    assert {grade(h) for h in UPACHAYA} == {"good", "bad", "excellent"}
    assert grade(4) == grade(7) == "bad"           # kendras, and bad
    assert grade(6) == "bad"                       # an upachaya, and bad
    assert "cannot be read off the category" in (
        THE_MUNTHA_HOUSES_ARE_NOT_THE_HOUSE_CATEGORIES)


def test_muntha_is_read_from_the_annual_lagna_not_the_natal_one():
    """"Position of muntha in various houses with respect to lagna in the
    annual chart."  Two different annual lagnas, two different readings.
    """
    from hora.core.const import RASI_ABBR
    from hora.tajaka.muntha import muntha

    scorpio, gemini = RASI_ABBR.index("Sc"), RASI_ABBR.index("Ge")
    # §28.1's own case: muntha in Ge for the 32nd year.
    from_gemini = muntha(scorpio, 32, gemini)
    assert from_gemini["house_from_annual_lagna"] == 1
    assert from_gemini["grade"] == "good"
    assert from_gemini["gives"] == "health"

    from_capricorn = muntha(scorpio, 32, RASI_ABBR.index("Cp"))
    assert from_capricorn["rasi"] == from_gemini["rasi"]      # same muntha
    assert from_capricorn["house_from_annual_lagna"] == 6     # different house
    assert from_capricorn["grade"] == "bad"


def test_the_grahas_in_muntha_are_reported_and_never_graded():
    """§28.1 says the strength of the planets influencing muntha matters and
    gives no measure, so occupants are listed and not weighed.
    """
    from hora.core.const import RASI_ABBR
    from hora.tajaka.muntha import MUNTHA_OCCUPANT_EXAMPLES, muntha

    gemini = RASI_ABBR.index("Ge")
    scorpio = RASI_ABBR.index("Sc")
    got = muntha(scorpio, 32, gemini, occupants={4: gemini, 6: 0, 0: gemini})
    assert got["grahas_in_muntha"] == (0, 4)          # Sun and Jupiter
    assert "no occupant is graded here" in got["strength_note"]

    # Not asked is not the same as nobody there.
    assert muntha(scorpio, 32, gemini)["grahas_in_muntha"] is None
    assert muntha(scorpio, 32, gemini,
                  occupants={6: 0})["grahas_in_muntha"] == ()

    assert len(MUNTHA_OCCUPANT_EXAMPLES) == 3
    assert MUNTHA_OCCUPANT_EXAMPLES[0]["graha"] == "Jupiter"
    assert MUNTHA_OCCUPANT_EXAMPLES[-1]["gives"] == (
        "loss of position, bad name and scandals")


def test_the_disputed_monthly_rate_is_the_annual_rate_interpolated():
    """2°30' a month is 30° a year, which is §28.1's own one rasi a year.

    The author declines that interpolation and does not replace it, so no
    monthly muntha is computed. See OI-152.
    """
    from hora.tajaka.muntha import (
        MONTHLY_MUNTHA_IS_DISPUTED,
        THE_DISPUTED_RATE_IS_THE_ANNUAL_RATE_INTERPOLATED,
    )
    from hora.tajaka.shashti_hora import SHASHTI_HORA_ARC_DEGREES

    assert 2.5 * 12 == 30.0
    assert "2°30' per month" in MONTHLY_MUNTHA_IS_DISPUTED
    assert "takes a different stand" in MONTHLY_MUNTHA_IS_DISPUTED
    # The same number as the shashti-hora arc, and a different thing.
    assert SHASHTI_HORA_ARC_DEGREES == 2.5
    assert "arc of the **Sun**" not in THE_DISPUTED_RATE_IS_THE_ANNUAL_RATE_INTERPOLATED
    assert "the author declines it" in (
        THE_DISPUTED_RATE_IS_THE_ANNUAL_RATE_INTERPOLATED)

    # Nothing computes one.
    import hora.tajaka.muntha as module

    assert not [name for name in dir(module)
                if "monthly" in name.lower() and callable(getattr(module, name))]


def test_muntha_checks_its_inputs():
    from hora.core import validate
    from hora.tajaka.muntha import MunthaError, muntha, muntha_rasi

    assert issubclass(MunthaError, validate.InputError)
    for bad in (-1, 12):
        with pytest.raises(validate.InputError):
            muntha_rasi(bad, 5)
        with pytest.raises(validate.InputError):
            muntha(0, 5, bad)
    for bad in (0, 201):
        with pytest.raises(validate.InputError):
            muntha_rasi(0, bad)


def test_28_1_is_transcribed_with_what_it_defers():
    from hora.tajaka.muntha import (
        MUNTHA_IS_AS_IMPORTANT_AS_LAGNA,
        MUNTHA_RULE,
        PLANETS_IN_MUNTHA,
    )

    assert "one rasi per year" in MUNTHA_RULE
    assert "specific to Tajaka charts" in MUNTHA_RULE
    assert "as important a reference point in an annual chart as lagna" in (
        MUNTHA_IS_AS_IMPORTANT_AS_LAGNA)
    # Both deferrals point at the same later chapter.
    assert "Sudarsana Chakra Dasa" in MUNTHA_IS_AS_IMPORTANT_AS_LAGNA
    assert "strength of the planets influencing muntha also matters" in (
        PLANETS_IN_MUNTHA)


# --------------------------------------------------------------------------
# §28.2 — the Tajaka aspects, and deeptamsa
# --------------------------------------------------------------------------


def test_the_six_aspects_are_transcribed_with_their_natures_and_strengths():
    from hora.tajaka.aspects import TAJAKA_ASPECTS, TAJAKA_ASPECTS_INTRO

    assert "we consider the following aspects" in TAJAKA_ASPECTS_INTRO
    assert len(TAJAKA_ASPECTS) == 6
    named = {entry["name"]: entry for entry in TAJAKA_ASPECTS}
    assert named["Trinal aspect"]["houses"] == (5, 9)
    assert named["Sextile aspect"]["houses"] == (3, 11)
    assert named["Square aspect"]["houses"] == (4, 10)
    assert named["Conjunction"]["houses"] == (1,)
    assert named["Opposition"]["houses"] == (7,)
    assert named["Semi-sextile aspect"]["houses"] == (2, 12)

    assert named["Trinal aspect"]["nature"] == "benefic"
    assert named["Trinal aspect"]["strength"] == "strong"
    assert named["Sextile aspect"]["strength"] == "weak"
    assert named["Square aspect"]["nature"] == "malefic"
    assert named["Square aspect"]["strength"] == "weak"
    assert named["Semi-sextile aspect"]["nature"] == "neutral"
    for entry in TAJAKA_ASPECTS:
        for house in entry["houses"]:
            assert f"{house}" in entry["text"] or house == 1


def test_the_house_distances_are_the_western_angles():
    """Each aspect's houses are 30 degrees apart per house, and the pairs are
    symmetric about the planet.
    """
    from hora.tajaka.aspects import TAJAKA_ASPECTS

    for entry in TAJAKA_ASPECTS:
        houses = entry["houses"]
        degrees = entry["degrees"]
        for house in houses:
            forward = (house - 1) * 30
            assert min(forward, 360 - forward) == degrees, entry["name"]
        if len(houses) == 2:
            assert sum(houses) == 14           # symmetric about the planet


def test_the_sixth_and_eighth_houses_receive_no_aspect():
    """Ten of twelve houses are covered. The two left out are at 150 degrees,
    which is western astrology's quincunx.
    """
    from hora.tajaka.aspects import (
        THE_SIXTH_AND_EIGHTH_RECEIVE_NO_ASPECT,
        aspect_on_house,
        aspects_from,
    )

    missing = [house for house in range(1, 13)
               if aspect_on_house(house) is None]
    assert missing == [6, 8]
    for house in missing:
        forward = (house - 1) * 30
        assert min(forward, 360 - forward) == 150

    # And every other multiple of thirty up to 180 is present.
    covered = {aspect_on_house(h)["degrees"] for h in range(1, 13)
               if aspect_on_house(h) is not None}
    assert covered == {0, 30, 60, 90, 120, 180}

    reached = {row["house"] for row in aspects_from(0)}
    assert reached == set(range(1, 13)) - {6, 8}
    assert "the quincunx" in THE_SIXTH_AND_EIGHTH_RECEIVE_NO_ASPECT


def test_the_conjunction_is_malefic_here_and_an_association_elsewhere():
    from hora.tajaka.aspects import (
        THE_CONJUNCTION_IS_MALEFIC_HERE_AND_NOWHERE_ELSE,
        aspect_on_house,
    )

    own = aspect_on_house(1)
    assert own["name"] == "Conjunction"
    assert own["nature"] == "malefic"
    assert own["strength"] == "strong"
    # Graded with the opposition, and nothing else is a strong malefic.
    opposition = aspect_on_house(7)
    assert (opposition["nature"], opposition["strength"]) == (
        own["nature"], own["strength"])

    # §11.7.1 counts a conjunction as one of the ways a Raaja Yoga forms.
    from hora.core.const import RAAJA_ASSOCIATIONS

    assert "conjunction" in {row["key"] for row in RAAJA_ASSOCIATIONS}
    assert "an association whose nature comes from the planets" in (
        THE_CONJUNCTION_IS_MALEFIC_HERE_AND_NOWHERE_ELSE)


def test_deeptamsa_is_per_planet_and_the_nodes_have_none():
    from hora.core import validate
    from hora.tajaka.aspects import (
        DEEPTAMSA,
        DEEPTAMSA_MEANS,
        DEEPTAMSA_RULE,
        THE_NODES_HAVE_NO_DEEPTAMSA,
        TajakaAspectError,
        deeptamsa,
    )

    assert issubclass(TajakaAspectError, validate.InputError)
    assert DEEPTAMSA_MEANS == "the orb of an aspect"
    assert sorted(DEEPTAMSA) == [0, 1, 2, 3, 4, 5, 6]
    assert [DEEPTAMSA[g] for g in range(7)] == [15, 12, 8, 7, 9, 7, 9]
    for graha, value in DEEPTAMSA.items():
        assert f"{int(value)}°" in DEEPTAMSA_RULE
        assert deeptamsa(graha) == value
    for node in (7, 8):
        with pytest.raises(TajakaAspectError):
            deeptamsa(node)
    assert "Deeptamsa is the same for all kinds of aspects" in DEEPTAMSA_RULE
    assert "not given one" in THE_NODES_HAVE_NO_DEEPTAMSA


def test_28_2s_venus_example_reproduces_exactly():
    """"If Venus is at 13° in Li ... Venus mainly influences 6°-20° in Ge." """
    from hora.charts import book
    from hora.tajaka.aspects import (
        THE_ORB_IS_PER_PLANET_AND_IS_A_HALF_WIDTH,
        aspect_span,
    )

    venus, gemini_from_libra = 5, 9
    got = aspect_span(venus, book.longitude("13 Li 00"), gemini_from_libra)
    assert got["aspect"] == "Trinal aspect"
    assert got["exact_rasi"] == "Gemini"
    assert got["exact"] % 30 == pytest.approx(13.0)
    assert got["deeptamsa"] == 7.0
    assert got["from"] % 30 == pytest.approx(6.0)
    assert got["to"] % 30 == pytest.approx(20.0)
    # Fourteen degrees wide, so the orb is a half-width.
    assert (got["to"] - got["from"]) % 360 == pytest.approx(14.0)
    assert "moderate aspectual influence on the entire rasi" in (
        got["whole_rasi_note"])
    assert "6 to 20 Ge" in THE_ORB_IS_PER_PLANET_AND_IS_A_HALF_WIDTH


def test_one_orb_serves_all_six_aspects():
    """"Deeptamsa is the same for all kinds of aspects." """
    from hora.tajaka.aspects import aspect_span

    orbs = {aspect_span(5, 193.0, house)["deeptamsa"]
            for house in range(1, 13)}
    assert orbs == {7.0}
    # Including the two houses that carry no aspect.
    for house in (6, 8):
        blank = aspect_span(5, 193.0, house)
        assert blank["aspect"] is None
        assert blank["exact"] is None
        assert blank["deeptamsa"] == 7.0
        assert "quincunx" in blank["reason"]


def test_three_aspect_systems_and_the_book_reconciles_none_of_them():
    """A planet can aspect a rasi in one scheme and not another."""
    from hora.charts.aspects import graha_drishti_houses
    from hora.tajaka.aspects import (
        THREE_ASPECT_SYSTEMS_AND_NO_RECONCILIATION,
        aspect_on_house,
    )

    # Graha drishti is asymmetric between planets; the Tajaka set is not.
    assert graha_drishti_houses(4) != graha_drishti_houses(6)
    tajaka = {house for house in range(1, 13)
              if aspect_on_house(house) is not None}
    assert all(set(graha_drishti_houses(g)) != tajaka for g in range(7))

    # Every planet aspects the 7th in both schemes, and only there do they
    # always agree.
    assert all(7 in graha_drishti_houses(g) for g in range(7))
    assert aspect_on_house(7)["name"] == "Opposition"

    # The 5th and 9th are a strong benefic here and Jupiter's alone there.
    assert 5 in graha_drishti_houses(4) and 9 in graha_drishti_houses(4)
    assert 5 not in graha_drishti_houses(6)
    assert aspect_on_house(5)["nature"] == "benefic"
    assert "states no rule for using them together" in (
        THREE_ASPECT_SYSTEMS_AND_NO_RECONCILIATION)


def test_footnote_79_qualifies_the_whole_system():
    """The second time Part 4 says its material has no maharshi behind it."""
    from hora.core.const import TAJAKA_PROVENANCE
    from hora.tajaka.aspects import FOOTNOTE_79

    assert "similar to the ones used in western astrology" in FOOTNOTE_79
    assert "graha and rasi aspects were mentioned by maharshis" in FOOTNOTE_79
    assert "needs to be further researched" in FOOTNOTE_79
    assert "current understanding of scholars may be incomplete" in FOOTNOTE_79
    assert "Rishi prokta" in FOOTNOTE_79
    # Part 4's opening said the same of the system as a whole.
    assert "no references to it in the works of Parasara" in TAJAKA_PROVENANCE


def test_the_aspect_helpers_check_their_inputs():
    from hora.core import validate
    from hora.tajaka.aspects import aspect_on_house, aspects_from

    for bad in (0, 13):
        with pytest.raises(validate.InputError):
            aspect_on_house(bad)
    for bad in (-1, 12):
        with pytest.raises(validate.InputError):
            aspects_from(bad)


# --------------------------------------------------------------------------
# §28.3 — harsha bala
# --------------------------------------------------------------------------


def test_the_four_sources_are_transcribed_and_each_is_worth_five():
    from hora.tajaka.harsha import (
        BALA_MEANS,
        FOOTNOTE_80,
        HARSHA_MAXIMUM,
        HARSHA_MEANS,
        HARSHA_SOURCES,
        HARSHA_UNITS_PER_SOURCE,
    )

    assert len(HARSHA_SOURCES) == 4
    assert HARSHA_UNITS_PER_SOURCE == 5
    assert HARSHA_MAXIMUM == len(HARSHA_SOURCES) * HARSHA_UNITS_PER_SOURCE
    assert "exaltation or own sign" in HARSHA_SOURCES[1]
    assert "Feminine planets" in HARSHA_SOURCES[2]
    assert "starts in the daytime" in HARSHA_SOURCES[3]
    assert HARSHA_MEANS == "cheerful" and BALA_MEANS == "strength"
    assert "strength of cheerfulness" in FOOTNOTE_80


def test_source_one_gives_each_planet_exactly_one_house():
    from hora.tajaka.harsha import HARSHA_HOUSES, HARSHA_SOURCES, harsha_bala

    assert sorted(HARSHA_HOUSES) == list(range(7))
    assert len(set(HARSHA_HOUSES.values())) == 7      # no house shared
    for graha, house in HARSHA_HOUSES.items():
        scored = harsha_bala(graha, house, dignified=False, daytime=True)
        assert scored["sources"][0]["units"] == 5
        elsewhere = [h for h in range(1, 13) if h != house]
        for other in elsewhere:
            assert harsha_bala(graha, other, dignified=False,
                               daytime=True)["sources"][0]["units"] == 0
    for house in HARSHA_HOUSES.values():
        assert str(house) in HARSHA_SOURCES[0]


def test_the_harsha_houses_are_the_planetary_joys():
    """An observation about the seven numbers, recorded and used for nothing.
    """
    from hora.tajaka.harsha import (
        HARSHA_HOUSES,
        THE_HARSHA_HOUSES_ARE_THE_PLANETARY_JOYS,
    )

    assert HARSHA_HOUSES == {0: 9, 1: 3, 2: 6, 3: 1, 4: 11, 5: 5, 6: 12}
    assert "the planets' joys" in THE_HARSHA_HOUSES_ARE_THE_PLANETARY_JOYS
    assert "footnote 80 glosses harsha as cheerful" in (
        THE_HARSHA_HOUSES_ARE_THE_PLANETARY_JOYS)


def test_the_gender_houses_partition_all_twelve():
    from hora.tajaka.harsha import (
        FEMININE_HOUSES,
        HARSHA_FEMININE,
        HARSHA_MASCULINE,
        MASCULINE_HOUSES,
    )

    assert set(FEMININE_HOUSES) | set(MASCULINE_HOUSES) == set(range(1, 13))
    assert not set(FEMININE_HOUSES) & set(MASCULINE_HOUSES)
    assert len(FEMININE_HOUSES) == len(MASCULINE_HOUSES) == 6
    assert set(HARSHA_FEMININE) | set(HARSHA_MASCULINE) == set(range(7))
    assert not set(HARSHA_FEMININE) & set(HARSHA_MASCULINE)
    assert len(HARSHA_FEMININE) == 4 and len(HARSHA_MASCULINE) == 3


def test_the_gender_split_is_not_chapter_threes():
    """BOOK DEVIATION, D-79. §28.3 calls Mercury and Saturn feminine; §3's
    own table makes both neuter.
    """
    from hora.core.const import GRAHA_SEX, SEX_NAMES
    from hora.tajaka.harsha import (
        THE_GENDER_SPLIT_IS_NOT_CHAPTER_THREES,
        is_feminine,
    )

    neuter = SEX_NAMES.index("neuter")
    chapter_three_neuter = {int(g) for g, sex in GRAHA_SEX.items()
                            if sex == neuter}
    assert chapter_three_neuter == {3, 6}             # Mercury and Saturn
    for graha in chapter_three_neuter:
        assert is_feminine(graha) is True

    female = SEX_NAMES.index("female")
    chapter_three_female = {int(g) for g, sex in GRAHA_SEX.items()
                            if sex == female}
    assert chapter_three_female == {1, 5}             # Moon and Venus only
    assert "makes Mercury and Saturn neuter" in (
        THE_GENDER_SPLIT_IS_NOT_CHAPTER_THREES)


def test_sources_three_and_four_both_turn_on_gender():
    from hora.tajaka.harsha import (
        HARSHA_FEMININE,
        HARSHA_MASCULINE,
        SOURCES_THREE_AND_FOUR_BOTH_TURN_ON_GENDER,
        harsha_bala,
    )

    # In a daytime year exactly the three masculine planets take source (4).
    daytime = {graha: harsha_bala(graha, 1, dignified=False,
                                  daytime=True)["sources"][3]["units"]
               for graha in range(7)}
    assert {g for g, units in daytime.items() if units == 5} == set(
        HARSHA_MASCULINE)
    night = {graha: harsha_bala(graha, 1, dignified=False,
                                daytime=False)["sources"][3]["units"]
             for graha in range(7)}
    assert {g for g, units in night.items() if units == 5} == set(
        HARSHA_FEMININE)
    assert "take none of it" in SOURCES_THREE_AND_FOUR_BOTH_TURN_ON_GENDER


def test_three_planets_can_never_be_exceedingly_strong():
    """The Sun's joy house is feminine and he is masculine; Venus's and
    Saturn's are masculine and they are feminine. Fifteen is their ceiling.
    """
    from hora.tajaka.harsha import (
        HARSHA_GRADES,
        THREE_PLANETS_CAN_NEVER_SCORE_TWENTY,
        harsha_bala,
    )

    best = {}
    for graha in range(7):
        best[graha] = max(
            harsha_bala(graha, house, dignified=dignified,
                        daytime=daytime)["units"]
            for house in range(1, 13)
            for dignified in (True, False)
            for daytime in (True, False))
    assert {g for g, top in best.items() if top == 15} == {0, 5, 6}
    assert {g for g, top in best.items() if top == 20} == {1, 2, 3, 4}
    assert HARSHA_GRADES[20] == "exceedingly strong"
    assert HARSHA_GRADES[15] == "fully strong"
    assert "tops out at fifteen" in THREE_PLANETS_CAN_NEVER_SCORE_TWENTY


def test_every_attainable_total_has_a_grade():
    from hora.tajaka.harsha import HARSHA_GRADE_RULE, HARSHA_GRADES, harsha_bala

    totals = {harsha_bala(graha, house, dignified=dignified,
                          daytime=daytime)["units"]
              for graha in range(7) for house in range(1, 13)
              for dignified in (True, False) for daytime in (True, False)}
    assert totals <= set(HARSHA_GRADES)
    assert totals == {0, 5, 10, 15, 20}
    for grade in HARSHA_GRADES.values():
        assert grade in HARSHA_GRADE_RULE


def test_an_unsupplied_dignity_is_undecided_and_not_a_zero():
    from hora.tajaka.harsha import harsha_bala

    got = harsha_bala(0, 9, dignified=None, daytime=True)
    assert got["undecided"] is True
    assert got["grade"] is None
    assert got["sources"][1]["units"] is None
    assert "undecided" in got["sources"][1]["detail"]
    assert (got["at_least"], got["at_most"]) == (10, 15)

    # Said to be undignified, the same chart is decided and scores less.
    decided = harsha_bala(0, 9, dignified=False, daytime=True)
    assert decided["undecided"] is False
    assert decided["units"] == 10
    assert decided["grade"] == "average strength"


def test_harsha_bala_checks_its_inputs():
    from hora.core import validate
    from hora.tajaka.harsha import HarshaError, harsha_bala, is_feminine

    assert issubclass(HarshaError, validate.InputError)
    for node in (7, 8):
        with pytest.raises(validate.InputError):
            is_feminine(node)
        with pytest.raises(validate.InputError):
            harsha_bala(node, 1, dignified=True, daytime=True)
    for bad in (0, 13):
        with pytest.raises(validate.InputError):
            harsha_bala(0, bad, dignified=True, daytime=True)


# --------------------------------------------------------------------------
# Example 119 — harsha bala for Chart 66
# --------------------------------------------------------------------------

E118_LAT, E118_LON = 26 + 18 / 60, 73 + 4 / 60
CHART_66 = (2000, 3, 8, 4, 41, 21.0)


def _chart_66():
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    return compute_chart(
        from_local(*CHART_66, utc_offset_hours=5.5),
        Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON),
        Settings())


def test_the_houses_of_chart_66_are_what_example_119_uses():
    """"Venus in 1st, Mercury in 2nd, Moon in 3rd ... Jupiter in 4th"."""
    chart = _chart_66()
    lagna = chart.lagna_rasi
    houses = {graha: (int(chart.positions[graha].longitude // 30) - lagna) % 12
              + 1 for graha in range(7)}
    assert houses == {0: 2, 1: 3, 2: 3, 3: 2, 4: 4, 5: 1, 6: 4}


def test_source_one_finds_only_the_moon():
    """"Only Moon is in the prescribed house (the 3rd house in Moon's case)."
    """
    from hora.tajaka.harsha import EXAMPLE_119_STEPS, harsha_bala

    chart = _chart_66()
    lagna = chart.lagna_rasi
    scored = {}
    for graha in range(7):
        house = (int(chart.positions[graha].longitude // 30) - lagna) % 12 + 1
        scored[graha] = harsha_bala(graha, house, dignified=False,
                                    daytime=False)["sources"][0]["units"]
    assert [g for g, units in scored.items() if units == 5] == [1]
    assert "Only Moon is in the prescribed house" in EXAMPLE_119_STEPS[0]


def test_source_two_finds_nobody_exalted_or_in_own_sign():
    """"No planet is in exaltation or own sign."  Checked against the
    engine's own dignity rather than taken from the page.
    """
    from hora.charts.dignity import sign_dignity
    from hora.tajaka.harsha import EXAMPLE_119_STEPS

    chart = _chart_66()
    for graha in range(7):
        dignity = sign_dignity(graha, chart.positions[graha].longitude)
        assert dignity not in ("exalted", "own"), (graha, dignity)
    assert EXAMPLE_119_STEPS[1] == "No planet is in exaltation or own sign."


def test_the_year_began_in_the_night_and_the_panchanga_cannot_say_so():
    """Source (4), and the defect that blocks the ordinary route to it.

    Example 118's year begins at 4:41 am. `/v1/panchanga` rejects that
    instant — OI-149 — so day or night is read from sunrise and sunset.
    """
    from fastapi.testclient import TestClient

    from hora.api.main import app
    from hora.core.timeutil import from_local
    from hora.tajaka.harsha import (
        SOURCE_FOUR_IS_BLOCKED_BY_OI_149,
        year_began_in_daytime,
    )

    instant = from_local(*CHART_66, utc_offset_hours=5.5)
    got = year_began_in_daytime(instant.jd_ut, E118_LAT, E118_LON)
    assert got["daytime"] is False
    # The instant sits after a sunset and before the next sunrise.
    assert got["last_sunset_jd"] < instant.jd_ut
    assert got["last_sunrise_jd"] < got["last_sunset_jd"]

    rejected = TestClient(app).post("/v1/panchanga", json={
        "year": 2000, "month": 3, "day": 8, "hour": 4, "minute": 41,
        "second": 21, "tz_name": "Asia/Kolkata",
        "place": {"latitude": E118_LAT, "longitude": E118_LON, "name": "b"}})
    assert rejected.status_code != 200
    assert "cannot be answered" not in SOURCE_FOUR_IS_BLOCKED_BY_OI_149
    assert "rejects any instant before sunrise" in (
        SOURCE_FOUR_IS_BLOCKED_BY_OI_149)


def test_example_119s_totals_reproduce_for_all_seven_planets():
    """"15 for Moon, 10 for Mercury and Venus, 5 for Jupiter and Saturn and
    zero for Sun and Mars."
    """
    from hora.charts.dignity import sign_dignity
    from hora.core.timeutil import from_local
    from hora.tajaka.harsha import (
        EXAMPLE_119_TOTAL,
        EXAMPLE_119_UNITS,
        harsha_bala,
        year_began_in_daytime,
    )

    chart = _chart_66()
    lagna = chart.lagna_rasi
    daytime = year_began_in_daytime(
        from_local(*CHART_66, utc_offset_hours=5.5).jd_ut,
        E118_LAT, E118_LON)["daytime"]

    ours = {}
    for graha in range(7):
        longitude = chart.positions[graha].longitude
        house = (int(longitude // 30) - lagna) % 12 + 1
        ours[graha] = harsha_bala(
            graha, house,
            dignified=sign_dignity(graha, longitude) in ("exalted", "own"),
            daytime=daytime)["units"]
    assert ours == EXAMPLE_119_UNITS
    assert EXAMPLE_119_UNITS[1] == 15
    assert {g for g, units in EXAMPLE_119_UNITS.items() if units == 10} == {
        3, 5}
    assert {g for g, units in EXAMPLE_119_UNITS.items() if units == 0} == {
        0, 2}
    assert "15 for Moon" in EXAMPLE_119_TOTAL


def test_the_moon_misses_twenty_by_one_source_and_not_by_a_ceiling():
    from hora.tajaka.harsha import (
        EXAMPLE_119_UNITS,
        THE_MOON_MISSES_TWENTY_BY_ONE_SOURCE,
        harsha_bala,
    )

    # She takes 1, 3 and 4 and fails only 2.
    scored = harsha_bala(1, 3, dignified=False, daytime=False)
    assert [row["units"] for row in scored["sources"]] == [5, 0, 5, 5]
    assert scored["units"] == EXAMPLE_119_UNITS[1] == 15
    # And the Moon is one of the four that can reach twenty.
    assert harsha_bala(1, 3, dignified=True, daytime=False)["units"] == 20
    assert "a miss rather than a ceiling" in (
        THE_MOON_MISSES_TWENTY_BY_ONE_SOURCE)


def test_the_example_quotes_the_approximate_varsha_pravesh_time():
    from hora.tajaka.harsha import (
        EXAMPLE_119_STEPS,
        THE_EXAMPLE_QUOTES_THE_APPROXIMATE_TIME,
    )

    assert "4:42 am" in EXAMPLE_119_STEPS[3]
    # 4:42:24 is §27.2's approximate answer; 4:41:21 is §27.1's exact one.
    from hora.tajaka.annual import EXAMPLE_118_NATIVITY
    from hora.tajaka.approximate import EXERCISE_47_ANSWER

    assert "4:41:21" in str(EXAMPLE_118_NATIVITY["varsha_pravesh"])
    assert EXERCISE_47_ANSWER["approximate"]           # the method exists
    assert "source (4) is unaffected" in THE_EXAMPLE_QUOTES_THE_APPROXIMATE_TIME


def test_example_119s_two_slips_are_recorded_not_corrected():
    from hora.tajaka.harsha import (
        EXAMPLE_119_HAS_TWO_SLIPS_IN_STEP_THREE,
        EXAMPLE_119_STEPS,
    )

    assert "is in the masculine planet" in EXAMPLE_119_STEPS[2]
    assert "prescibed" in EXAMPLE_119_STEPS[2]
    assert "Neither changes a number" in EXAMPLE_119_HAS_TWO_SLIPS_IN_STEP_THREE


# --------------------------------------------------------------------------
# §28.4 — pancha vargeeya bala: kshetra, uchcha and hadda
# --------------------------------------------------------------------------


def test_the_group_of_five_is_named_and_only_three_have_arrived():
    from hora.tajaka.panchavargeeya import (
        FOOTNOTE_81,
        PANCHA_MEANS,
        PANCHA_VARGAS,
        PANCHA_VARGAS_PENDING,
        PANCHA_VARGEEYA_MEANS,
    )

    assert PANCHA_MEANS == "five"
    assert PANCHA_VARGEEYA_MEANS == "from the group of five"
    assert "from the group of five" in FOOTNOTE_81
    assert len(PANCHA_VARGAS) == 5
    supplied = [row for row in PANCHA_VARGAS if row["supplied"]]
    assert [row["name"] for row in supplied] == [
        "Kshetra bala", "Uchcha bala", "Hadda bala", "Drekkana bala",
        "Navamsa bala"]
    assert [row["maximum"] for row in supplied] == [30.0, 20.0, 15.0, 10.0,
                                                    5.0]
    assert PANCHA_VARGAS_PENDING == ()
    assert all(row["supplied"] for row in PANCHA_VARGAS)


def test_only_the_supplied_vargas_are_built():
    """The coverage line. It fails the moment a pending source appears."""
    import hora.tajaka.panchavargeeya as module

    for present in ("kshetra_bala", "uchcha_bala", "hadda_bala",
                    "hadda_lord", "drekkana_bala", "navamsa_bala",
                    "pancha_vargeeya_bala", "pancha_vargeeya_grade"):
        assert callable(getattr(module, present))


def test_kshetra_and_hadda_grade_three_places_and_halve_each_step():
    from hora.tajaka.panchavargeeya import (
        HADDA_BALA_UNITS,
        HADDA_IS_KSHETRA_HALVED,
        KSHETRA_BALA_UNITS,
        hadda_bala,
        kshetra_bala,
    )

    assert KSHETRA_BALA_UNITS == {"own": 30.0, "friend": 15.0, "enemy": 7.5}
    assert HADDA_BALA_UNITS == {"own": 15.0, "friend": 7.5, "enemy": 3.75}
    for units in (KSHETRA_BALA_UNITS, HADDA_BALA_UNITS):
        assert units["own"] == units["friend"] * 2
        assert units["friend"] == units["enemy"] * 2
    for grade in ("own", "friend", "enemy"):
        assert hadda_bala(grade)["units"] * 2 == kshetra_bala(grade)["units"]
    assert "half the" in HADDA_IS_KSHETRA_HALVED


def test_a_neutrals_place_is_undecided_and_not_a_zero():
    """OI-153. Both sections grade own, friend's and enemy's and stop, while
    chapter 3's relationships produce a neutral.
    """
    from hora.charts.relationship import natural
    from hora.core.const import COMPOUND_RELATION_NAMES
    from hora.tajaka.panchavargeeya import (
        THE_NEUTRAL_GRADE_IS_NOT_PRICED,
        PanchaVargeeyaError,
        hadda_bala,
        kshetra_bala,
    )

    # Chapter 3 really does produce a neutral, and the compound five grades.
    assert "neutral" in {natural(0, other) for other in range(1, 7)}
    assert set(COMPOUND_RELATION_NAMES) == {
        "great_friend", "friend", "neutral", "enemy", "great_enemy"}

    for scorer in (kshetra_bala, hadda_bala):
        got = scorer("neutral")
        assert got["undecided"] is True
        assert got["units"] is None
        assert "no value in either" in got["reason"]
        # And an unnamed grade is refused rather than defaulted.
        with pytest.raises(PanchaVargeeyaError):
            scorer("great_friend")
    assert "grade own, a friend's and an enemy's place and stop" in (
        THE_NEUTRAL_GRADE_IS_NOT_PRICED)


def test_the_deep_exaltation_points_are_chapter_threes():
    from hora.core.const import DEBILITATION_DEG, EXALTATION_DEG
    from hora.tajaka.panchavargeeya import (
        DEEP_EXALTATION,
        THE_EXALTATION_DEGREES_ARE_CHAPTER_THREES,
        deep_debilitation,
    )

    assert sorted(DEEP_EXALTATION) == list(range(7))
    for graha, degree in DEEP_EXALTATION.items():
        assert degree == EXALTATION_DEG[graha], graha
        assert deep_debilitation(graha) == DEBILITATION_DEG[graha], graha
    assert "to the degree" in THE_EXALTATION_DEGREES_ARE_CHAPTER_THREES


def test_28_4_2s_worked_case_reproduces_to_the_printed_hundredth():
    """"Jupiter is at 8Vi30 ... his uchcha bala is 12.94 (out of 20)." """
    from hora.charts import book
    from hora.tajaka.panchavargeeya import UCHCHA_BALA_WORKED_CASE, uchcha_bala

    got = uchcha_bala(4, book.longitude("8 Vi 30"))
    assert got["longitude"] == pytest.approx(158.5)
    assert got["deep_debilitation"] == pytest.approx(275.0)
    assert got["difference"] == pytest.approx(116.5)
    assert round(got["fraction"], 4) == 0.6472
    assert round(got["units"], 2) == 12.94
    assert "12.94 (out of 20)" in UCHCHA_BALA_WORKED_CASE


def test_uchcha_bala_runs_from_twenty_at_exaltation_to_zero_at_debilitation():
    from hora.tajaka.panchavargeeya import (
        DEEP_EXALTATION,
        UCHCHA_BALA_MAXIMUM,
        deep_debilitation,
        uchcha_bala,
    )

    for graha, exalted in DEEP_EXALTATION.items():
        assert uchcha_bala(graha, exalted)["units"] == pytest.approx(
            UCHCHA_BALA_MAXIMUM)
        assert uchcha_bala(graha, deep_debilitation(graha))["units"] == (
            pytest.approx(0.0))
        # Ninety degrees either side of the debilitation point is half.
        for side in (-90.0, 90.0):
            halfway = (deep_debilitation(graha) + side) % 360.0
            assert uchcha_bala(graha, halfway)["units"] == pytest.approx(
                UCHCHA_BALA_MAXIMUM / 2)
        # Never outside the range, wherever the planet is.
        for step in range(0, 360, 7):
            units = uchcha_bala(graha, float(step))["units"]
            assert 0.0 <= units <= UCHCHA_BALA_MAXIMUM


def test_the_wrap_case_the_section_mentions_but_does_not_work():
    """"Because this is less than 180°, we don't have to subtract it from
    360°."  The case it points at and skips, checked.
    """
    from hora.tajaka.panchavargeeya import (
        UCHCHA_BALA_WORKED_CASE,
        deep_debilitation,
        uchcha_bala,
    )

    assert "subtract it from 360" in UCHCHA_BALA_WORKED_CASE
    # Jupiter's debilitation is 275; a planet at 20 gives a raw gap of 255.
    got = uchcha_bala(4, 20.0)
    assert got["difference"] == pytest.approx(105.0)      # 360 - 255
    assert got["difference"] <= 180.0
    # And the symmetry the wrap enforces: equal distances either way score
    # alike.
    for offset in (30.0, 120.0, 179.0):
        below = uchcha_bala(4, (deep_debilitation(4) - offset) % 360.0)
        above = uchcha_bala(4, (deep_debilitation(4) + offset) % 360.0)
        assert below["units"] == pytest.approx(above["units"])


def test_table_72_is_transcribed_and_every_row_closes_on_thirty():
    from hora.core.const import GRAHA_NAMES
    from hora.tajaka.panchavargeeya import (
        HADDA_LORDS,
        HADDA_RULE,
        TABLE_72_HADDA_LORDS,
        TABLE_72_TITLE,
    )

    assert TABLE_72_TITLE == "Hadda Lords"
    assert "Table 72 can be used for finding the hadda lords" in HADDA_RULE
    assert "Hadda is similar to D-30" in HADDA_RULE
    assert sorted(TABLE_72_HADDA_LORDS) == list(range(12))
    for rasi, rows in TABLE_72_HADDA_LORDS.items():
        assert len(rows) == 5, rasi
        previous = 0.0
        for end, lord in rows:
            assert end > previous, (rasi, end)
            assert lord in HADDA_LORDS, (rasi, lord)
            previous = end
        assert previous == 30.0, rasi
    assert sorted(HADDA_LORDS) == [2, 3, 4, 5, 6]
    assert {str(GRAHA_NAMES[g]) for g in HADDA_LORDS} == {
        "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}


def test_28_4_2s_one_letter_slip_is_recorded():
    from hora.tajaka.panchavargeeya import BU_IS_A_SLIP_FOR_BY, UCHCHA_BALA_METHOD

    assert "Bu multiplying" in UCHCHA_BALA_METHOD
    assert "Nothing turns on it" in BU_IS_A_SLIP_FOR_BY


def test_the_pancha_vargeeya_helpers_check_their_inputs():
    from hora.core import validate
    from hora.tajaka.panchavargeeya import (
        PanchaVargeeyaError,
        deep_debilitation,
        kshetra_bala,
        uchcha_bala,
    )

    assert issubclass(PanchaVargeeyaError, validate.InputError)
    for node in (7, 8):
        with pytest.raises(validate.InputError):
            uchcha_bala(node, 100.0)
        with pytest.raises(validate.InputError):
            deep_debilitation(node)
    with pytest.raises(PanchaVargeeyaError):
        kshetra_bala("exalted")


def test_the_luminaries_can_never_hold_their_own_hadda():
    """Table 72's sixty haddas are shared among five grahas, and neither
    luminary is one of them — so hadda bala's own grade is out of reach.
    """
    from hora.tajaka.panchavargeeya import (
        HADDA_LORDS,
        TABLE_72_HADDA_LORDS,
        THE_LUMINARIES_CAN_NEVER_HOLD_THEIR_OWN_HADDA,
        hadda_bala,
        hadda_lord,
    )

    every = {lord for rows in TABLE_72_HADDA_LORDS.values()
             for _end, lord in rows}
    assert every == set(HADDA_LORDS)
    assert 0 not in every and 1 not in every
    # Sixty haddas in all, and no longitude ever hands one to a luminary.
    assert sum(len(rows) for rows in TABLE_72_HADDA_LORDS.values()) == 60
    for step in range(3600):
        assert hadda_lord(step / 10.0)["lord"] in HADDA_LORDS
    # The best either luminary can take is a friend's 7.5 of 15.
    assert hadda_bala("friend")["units"] == 7.5
    assert hadda_bala("own")["units"] == 15.0
    assert "unreachable for both" in (
        THE_LUMINARIES_CAN_NEVER_HOLD_THEIR_OWN_HADDA)


def test_the_hadda_totals_are_uneven_and_recorded_for_checking():
    """OI-154. The widths as printed, summed per lord."""
    from collections import Counter

    from hora.tajaka.panchavargeeya import (
        TABLE_72_HADDA_LORDS,
        THE_HADDA_TOTALS_ARE_UNEVEN,
    )

    spans: Counter = Counter()
    for rows in TABLE_72_HADDA_LORDS.values():
        previous = 0.0
        for end, lord in rows:
            spans[lord] += end - previous
            previous = end
    assert sum(spans.values()) == 360.0
    assert spans == {5: 83.0, 4: 78.0, 3: 76.0, 2: 67.0, 6: 56.0}
    for degrees in (83, 78, 76, 67, 56):
        assert str(degrees) in THE_HADDA_TOTALS_ARE_UNEVEN


def test_hadda_lord_finds_the_span_a_longitude_falls_in():
    from hora.charts import book
    from hora.tajaka.panchavargeeya import hadda_lord

    # The first hadda of Aries, and the last of Pisces.
    first = hadda_lord(0.0)
    assert (first["rasi"], first["hadda_from"], first["hadda_to"]) == (
        0, 0.0, 6.0)
    assert first["lord_name"] == "Jupiter"
    last = hadda_lord(359.99)
    assert (last["rasi"], last["hadda_from"], last["hadda_to"]) == (
        11, 28.0, 30.0)
    assert last["lord_name"] == "Saturn"

    # §28.4.2's own Jupiter, at 8 Vi 30.
    jupiter = hadda_lord(book.longitude("8 Vi 30"))
    assert jupiter["rasi"] == 5
    assert (jupiter["hadda_from"], jupiter["hadda_to"]) == (7.0, 17.0)
    assert jupiter["lord_name"] == "Venus"

    # A boundary belongs to the hadda it opens, not the one it closes.
    assert hadda_lord(6.0)["hadda_from"] == 6.0
    assert hadda_lord(5.999)["hadda_to"] == 6.0


def test_28_4_4s_drekkana_bala_and_28_4_5s_navamsa_bala():
    from hora.tajaka.panchavargeeya import (
        DREKKANA_BALA_RULE,
        DREKKANA_BALA_UNITS,
        NAVAMSA_BALA_RULE,
        NAVAMSA_BALA_UNITS,
        drekkana_bala,
        navamsa_bala,
    )

    assert DREKKANA_BALA_UNITS == {"own": 10.0, "friend": 5.0, "enemy": 2.5}
    assert NAVAMSA_BALA_UNITS == {"own": 5.0, "friend": 2.5, "enemy": 1.25}
    assert "drekkana chart (D-3)" in DREKKANA_BALA_RULE
    assert "navamsa chart (D-9)" in NAVAMSA_BALA_RULE
    for grade in ("own", "friend", "enemy"):
        assert drekkana_bala(grade)["units"] == DREKKANA_BALA_UNITS[grade]
        assert navamsa_bala(grade)["units"] == NAVAMSA_BALA_UNITS[grade]


def test_the_five_sources_are_in_the_ratio_six_four_three_two_one():
    """And the neat thirty-over-n of the first three does not survive
    navamsa, which is thirty over six rather than over four.
    """
    from hora.tajaka.panchavargeeya import (
        DREKKANA_BALA_UNITS,
        HADDA_BALA_UNITS,
        KSHETRA_BALA_UNITS,
        NAVAMSA_BALA_UNITS,
        THE_FIVE_SOURCES_ARE_IN_THE_RATIO_SIX_FOUR_THREE_TWO_ONE,
        UCHCHA_BALA_MAXIMUM,
    )

    maxima = [KSHETRA_BALA_UNITS["own"], UCHCHA_BALA_MAXIMUM,
              HADDA_BALA_UNITS["own"], DREKKANA_BALA_UNITS["own"],
              NAVAMSA_BALA_UNITS["own"]]
    assert maxima == [30.0, 20.0, 15.0, 10.0, 5.0]
    assert [value / 5.0 for value in maxima] == [6.0, 4.0, 3.0, 2.0, 1.0]
    assert sum(maxima) == 80.0

    # The place balas alone: thirty over one, two, three and six.
    places = [KSHETRA_BALA_UNITS["own"], HADDA_BALA_UNITS["own"],
              DREKKANA_BALA_UNITS["own"], NAVAMSA_BALA_UNITS["own"]]
    assert [30.0 / value for value in places] == [1.0, 2.0, 3.0, 6.0]
    assert 30.0 / places[-1] != 4.0
    # And every one still halves twice within itself.
    for units in (KSHETRA_BALA_UNITS, HADDA_BALA_UNITS, DREKKANA_BALA_UNITS,
                  NAVAMSA_BALA_UNITS):
        assert units["own"] == units["friend"] * 2 == units["enemy"] * 4
    assert "rather than over one to four" in (
        THE_FIVE_SOURCES_ARE_IN_THE_RATIO_SIX_FOUR_THREE_TWO_ONE)


def test_the_neutral_gap_repeats_in_all_three_place_balas():
    from hora.tajaka.panchavargeeya import (
        THE_NEUTRAL_GAP_REPEATS_IN_ALL_THREE_PLACE_BALAS,
        drekkana_bala,
        hadda_bala,
        kshetra_bala,
        navamsa_bala,
    )

    for scorer in (kshetra_bala, hadda_bala, drekkana_bala, navamsa_bala):
        got = scorer("neutral")
        assert got["undecided"] is True
        assert got["units"] is None
    assert "None of the three prices a neutral's" in (
        THE_NEUTRAL_GAP_REPEATS_IN_ALL_THREE_PLACE_BALAS)


# --------------------------------------------------------------------------
# §28.4.6 — the final computation
# --------------------------------------------------------------------------


def test_the_five_are_summed_and_divided_by_four():
    from hora.tajaka.panchavargeeya import (
        FINAL_COMPUTATION_RULE,
        PANCHA_VARGEEYA_DIVISOR,
        PANCHA_VARGEEYA_MAXIMUM,
        PANCHA_VARGEEYA_RAW_MAXIMUM,
        pancha_vargeeya_bala,
    )

    assert PANCHA_VARGEEYA_DIVISOR == 4
    assert "divide the sum by 4" in FINAL_COMPUTATION_RULE
    got = pancha_vargeeya_bala(kshetra=30.0, uchcha=20.0, hadda=15.0,
                               drekkana=10.0, navamsa=5.0)
    assert got["raw_sum"] == PANCHA_VARGEEYA_RAW_MAXIMUM == 80.0
    assert got["units"] == PANCHA_VARGEEYA_MAXIMUM == 20.0
    assert got["undecided"] is False


def test_the_top_grade_cannot_be_reached_by_any_chart():
    """"If it is above 20, the planet is extraordinarily strong."  The five
    maxima cap the quotient at exactly 20.
    """
    from hora.tajaka.panchavargeeya import (
        PANCHA_VARGEEYA_MAXIMUM,
        PANCHA_VARGEEYA_TOP_GRADE,
        THE_TOP_GRADE_CANNOT_BE_REACHED,
        drekkana_bala,
        hadda_bala,
        kshetra_bala,
        navamsa_bala,
        pancha_vargeeya_bala,
        uchcha_bala,
    )

    # The best each source can give, taken from the functions themselves.
    best = pancha_vargeeya_bala(
        kshetra=kshetra_bala("own")["units"],
        uchcha=max(uchcha_bala(4, step / 4.0)["units"]
                   for step in range(1440)),
        hadda=hadda_bala("own")["units"],
        drekkana=drekkana_bala("own")["units"],
        navamsa=navamsa_bala("own")["units"])
    assert best["units"] == pytest.approx(PANCHA_VARGEEYA_MAXIMUM, abs=1e-6)
    assert best["grade"] == "very strong"
    assert best["grade"] != PANCHA_VARGEEYA_TOP_GRADE
    assert "which nothing can reach" in THE_TOP_GRADE_CANNOT_BE_REACHED


def test_the_bands_are_read_so_that_every_attainable_value_has_a_grade():
    from hora.tajaka.panchavargeeya import (
        PANCHA_VARGEEYA_GRADES,
        PANCHA_VARGEEYA_MAXIMUM,
        THE_BAND_ENDPOINTS_ARE_SETTLED_BY_ARITHMETIC,
        pancha_vargeeya_grade,
    )

    assert [row[2] for row in PANCHA_VARGEEYA_GRADES] == [
        "weak", "ordinary strength", "strong", "very strong"]
    assert pancha_vargeeya_grade(4.999) == "weak"
    assert pancha_vargeeya_grade(5.0) == "ordinary strength"
    assert pancha_vargeeya_grade(10.0) == "strong"
    assert pancha_vargeeya_grade(15.0) == "very strong"
    # The one attainable maximum is graded rather than falling through.
    assert pancha_vargeeya_grade(PANCHA_VARGEEYA_MAXIMUM) == "very strong"
    # Every hundredth from zero to the maximum has exactly one grade.
    for step in range(2001):
        assert pancha_vargeeya_grade(step / 100.0)
    assert "the only way every attainable value has one grade" in (
        THE_BAND_ENDPOINTS_ARE_SETTLED_BY_ARITHMETIC)


def test_the_divisor_puts_the_total_on_uchcha_balas_scale():
    from hora.tajaka.panchavargeeya import (
        PANCHA_VARGEEYA_DIVISOR,
        PANCHA_VARGEEYA_MAXIMUM,
        PANCHA_VARGEEYA_RAW_MAXIMUM,
        THE_DIVISOR_PUTS_THE_TOTAL_ON_UCHCHA_BALAS_SCALE,
        UCHCHA_BALA_MAXIMUM,
    )

    assert PANCHA_VARGEEYA_RAW_MAXIMUM / PANCHA_VARGEEYA_DIVISOR == (
        PANCHA_VARGEEYA_MAXIMUM)
    assert PANCHA_VARGEEYA_MAXIMUM == UCHCHA_BALA_MAXIMUM
    # Uchcha is a quarter of the eighty; the four place balas are the rest.
    assert UCHCHA_BALA_MAXIMUM / PANCHA_VARGEEYA_RAW_MAXIMUM == 0.25
    assert "the other three quarters" in (
        THE_DIVISOR_PUTS_THE_TOTAL_ON_UCHCHA_BALAS_SCALE)


def test_an_undecided_source_gives_a_range_and_no_grade():
    """A neutral place leaves one source unpriced (OI-153), and the total
    then has to be a range.
    """
    from hora.tajaka.panchavargeeya import drekkana_bala, pancha_vargeeya_bala

    got = pancha_vargeeya_bala(kshetra=30.0, uchcha=20.0, hadda=7.5,
                               drekkana=drekkana_bala("neutral")["units"],
                               navamsa=2.5)
    assert got["undecided"] is True
    assert got["undecided_sources"] == ("drekkana",)
    assert got["grade"] is None
    assert got["at_least"] == 15.0
    assert got["at_most"] == 17.5           # the missing ten, over four
    # Nothing undecided, and the grade comes back.
    decided = pancha_vargeeya_bala(kshetra=30.0, uchcha=20.0, hadda=7.5,
                                   drekkana=2.5, navamsa=2.5)
    assert decided["undecided"] is False
    assert decided["units"] == pytest.approx(15.625)
    assert decided["grade"] == "very strong"


def test_mercurys_best_case_still_falls_short_of_the_maximum():
    """At 15 Vi Mercury is in his own rasi and at his deep exaltation point —
    the only graha for whom those coincide — and even so three sources are
    not his own.
    """
    from hora.charts.relationship import natural
    from hora.charts.vargas import d3_drekkana, d9_navamsa
    from hora.core.const import RASI_LORD
    from hora.tajaka.panchavargeeya import (
        DEEP_EXALTATION,
        hadda_lord,
        uchcha_bala,
    )

    mercury, longitude = 3, 165.0
    assert DEEP_EXALTATION[mercury] == longitude
    assert int(RASI_LORD[int(longitude // 30)]) == mercury      # own rasi
    assert uchcha_bala(mercury, longitude)["units"] == 20.0

    # The hadda there is Venus's, not his.
    assert hadda_lord(longitude)["lord"] != mercury
    for varga in (d3_drekkana, d9_navamsa):
        assert int(RASI_LORD[varga(longitude).sign]) != mercury
    # So at best he takes a friend's grade in those, never his own.
    assert natural(mercury, hadda_lord(longitude)["lord"]) in (
        "friend", "neutral", "enemy")


# --------------------------------------------------------------------------
# §28.5 — dwaadasa vargeeya bala
# --------------------------------------------------------------------------


def test_the_twelve_charts_are_d1_to_d12_consecutively():
    from hora.charts.vargas import VARGA_REGISTRY
    from hora.tajaka.dwadasavargeeya import (
        DWAADASA_MEANS,
        DWAADASAVARGEEYA_MEANS,
        DWADASA_VARGAS,
        DWADASA_VARGEEYA_CHARTS,
        FOOTNOTE_82,
    )

    assert DWADASA_VARGAS == tuple(f"D{n}" for n in range(1, 13))
    assert len(DWADASA_VARGAS) == 12
    for code in DWADASA_VARGAS:
        assert code in VARGA_REGISTRY, code
        assert code.replace("D", "D-") in DWADASA_VARGEEYA_CHARTS
    assert DWAADASA_MEANS == "twelve"
    assert DWAADASAVARGEEYA_MEANS == "from the 12 groups"
    assert "from the 12 groups" in FOOTNOTE_82


def test_four_of_the_twelve_belong_to_no_group_the_book_has_named():
    from hora.charts.vargas import VARGA_GROUPS
    from hora.tajaka.dwadasavargeeya import (
        DWADASA_VARGAS,
        THE_TWELVE_ARE_NOT_ANY_EARLIER_GROUP,
    )

    already = set().union(*VARGA_GROUPS.values())
    outside = sorted(set(DWADASA_VARGAS) - already, key=lambda c: int(c[1:]))
    assert outside == ["D5", "D6", "D8", "D11"]
    # And the twelve are not themselves one of the named groups.
    assert set(DWADASA_VARGAS) not in [set(v) for v in VARGA_GROUPS.values()]
    assert "taken consecutively, not a selection" in (
        THE_TWELVE_ARE_NOT_ANY_EARLIER_GROUP)


def test_the_five_conditions_are_tested_in_the_sections_own_order():
    from hora.core.const import DEBILITATION_RASI, EXALTATION_RASI, RASI_LORD
    from hora.tajaka.dwadasavargeeya import (
        STRONG_IN_A_CHART,
        WEAK_IN_A_CHART,
        strength_in_rasi,
    )

    assert len(STRONG_IN_A_CHART) == 3
    assert len(WEAK_IN_A_CHART) == 2

    for graha in range(7):
        exalted = int(EXALTATION_RASI[graha])
        fallen = int(DEBILITATION_RASI[graha])
        assert strength_in_rasi(graha, exalted)["verdict"] == "strong"
        assert strength_in_rasi(graha, exalted)["because"] == (
            "its exaltation rasi")
        assert strength_in_rasi(graha, fallen)["verdict"] == "weak"
        own = [r for r in range(12) if int(RASI_LORD[r]) == graha]
        for rasi in own:
            assert strength_in_rasi(graha, rasi)["verdict"] == "strong"

    # Every rasi gets exactly one of the three verdicts, for every graha.
    for graha in range(7):
        verdicts = {strength_in_rasi(graha, rasi)["verdict"]
                    for rasi in range(12)}
        assert verdicts <= {"strong", "weak", "neither"}


def test_a_neutrals_rasi_is_neither_and_that_is_coherent_here():
    """The gap OI-153 leaves open in §28.4 does not arise in §28.5."""
    from hora.charts.relationship import natural
    from hora.core.const import RASI_LORD
    from hora.tajaka.dwadasavargeeya import (
        THE_NEUTRAL_CASE_IS_COHERENT_HERE,
        strength_in_rasi,
    )
    from hora.tajaka.panchavargeeya import kshetra_bala

    found = False
    for graha in range(7):
        for rasi in range(12):
            owner = int(RASI_LORD[rasi])
            if owner == graha or natural(graha, owner) != "neutral":
                continue
            got = strength_in_rasi(graha, rasi)
            if got["verdict"] == "neither":
                found = True
                assert "counts neither way" in got["because"]
    assert found, "no neutral-owned rasi was reachable"

    # §28.4 has to call the same case undecided; §28.5 does not.
    assert kshetra_bala("neutral")["undecided"] is True
    assert "needed one and did not give it" in THE_NEUTRAL_CASE_IS_COHERENT_HERE


def test_the_count_runs_over_twelve_charts_and_the_difference_is_the_bala():
    from hora.charts.vargas import varga
    from hora.tajaka.dwadasavargeeya import (
        DWADASA_VARGAS,
        dwadasavargeeya_bala,
        strength_in_rasi,
    )

    got = dwadasavargeeya_bala(4, 165.0)
    assert len(got["charts"]) == 12
    assert [row["chart"] for row in got["charts"]] == list(DWADASA_VARGAS)
    assert got["strong"] + got["weak"] + got["neither"] == 12
    assert got["units"] == got["strong"] - got["weak"]
    assert -12 <= got["units"] <= 12
    # Each row is the varga's own sign, judged by the same rule.
    for row in got["charts"]:
        assert row["rasi"] == varga(165.0, row["chart"]).sign
        assert row["verdict"] == strength_in_rasi(4, row["rasi"])["verdict"]


def test_a_tie_gets_no_verdict_and_ties_are_common():
    """OI-155. The section reads a majority both ways and never a level
    count, which happens for roughly one longitude in twelve.
    """
    from hora.tajaka.dwadasavargeeya import (
        A_TIE_HAS_NO_VERDICT,
        dwadasavargeeya_bala,
    )

    ties = 0
    samples = 0
    for graha in range(7):
        for step in range(0, 3600, 7):
            got = dwadasavargeeya_bala(graha, step / 10.0)
            samples += 1
            if got["tie"]:
                ties += 1
                assert got["overall"] is None
                assert got["units"] == 0
                assert got["tie_note"] == A_TIE_HAS_NO_VERDICT
            else:
                assert got["overall"] in ("strong", "weak")
                assert got["tie_note"] is None
    assert ties > 0
    assert 0.03 < ties / samples < 0.20        # nearly one in twelve
    assert "gives no reading for equal counts" in A_TIE_HAS_NO_VERDICT


def test_exaltation_is_by_rasi_here_and_by_degree_in_28_4_2():
    from hora.core.const import EXALTATION_RASI
    from hora.tajaka.dwadasavargeeya import (
        EXALTATION_IS_BY_RASI_HERE_AND_BY_DEGREE_IN_28_4_2,
        strength_in_rasi,
    )
    from hora.tajaka.panchavargeeya import DEEP_EXALTATION, uchcha_bala

    for graha in range(7):
        rasi = int(EXALTATION_RASI[graha])
        # Anywhere in the rasi counts here...
        for degree in (0.5, 15.0, 29.5):
            assert strength_in_rasi(graha, rasi)["verdict"] == "strong"
            # ...but uchcha bala moves with the degree.
            longitude = rasi * 30 + degree
            assert uchcha_bala(graha, longitude)["units"] < 20.0 or (
                longitude == DEEP_EXALTATION[graha])
    assert "without reconciling them" in (
        EXALTATION_IS_BY_RASI_HERE_AND_BY_DEGREE_IN_28_4_2)


def test_the_natural_relationship_is_used_and_the_reason_is_recorded():
    from hora.charts.relationship import compound_in_chart, natural
    from hora.tajaka.dwadasavargeeya import (
        THE_NATURAL_RELATIONSHIP_IS_THE_ONLY_STABLE_ONE_HERE,
        strength_in_rasi,
    )

    # The natural relationship needs only the two grahas...
    assert natural(0, 6) == natural(0, 6)
    # ...where a compound one needs a chart, so it would differ per varga.
    assert callable(compound_in_chart)
    # A rasi owned by a natural friend is strong; by a natural enemy, weak.
    from hora.core.const import RASI_LORD

    for graha in range(7):
        for rasi in range(12):
            owner = int(RASI_LORD[rasi])
            got = strength_in_rasi(graha, rasi)
            if got["because"] == "a rasi owned by a friend":
                assert natural(graha, owner) == "friend"
            if got["because"] == "a rasi owned by an enemy":
                assert natural(graha, owner) == "enemy"
    assert "the natural one does not" in (
        THE_NATURAL_RELATIONSHIP_IS_THE_ONLY_STABLE_ONE_HERE)


def test_the_nodes_cannot_be_scored():
    from hora.core import validate
    from hora.tajaka.dwadasavargeeya import (
        THE_NODES_CANNOT_BE_SCORED,
        DwadasaVargeeyaError,
        dwadasavargeeya_bala,
        strength_in_rasi,
    )

    assert issubclass(DwadasaVargeeyaError, validate.InputError)
    for node in (7, 8):
        with pytest.raises(validate.InputError):
            strength_in_rasi(node, 0)
        with pytest.raises(validate.InputError):
            dwadasavargeeya_bala(node, 100.0)
    assert "own nothing" in THE_NODES_CANNOT_BE_SCORED


# --------------------------------------------------------------------------
# §28.6 — the lord of the year
# --------------------------------------------------------------------------


def test_the_five_candidates_are_transcribed_in_the_sections_order():
    from hora.tajaka.varsheswara import (
        VARSHESWARA_CANDIDATES,
        VARSHESWARA_RULE,
    )

    assert "most important planet during the year" in VARSHESWARA_RULE
    assert "His dasa brings important results" in VARSHESWARA_RULE
    assert len(VARSHESWARA_CANDIDATES) == 5
    assert [row["number"] for row in VARSHESWARA_CANDIDATES] == list("12345")
    assert "day or the night" in VARSHESWARA_CANDIDATES[0]["candidate"]
    assert VARSHESWARA_CANDIDATES[1]["candidate"] == "Lord of natal lagna"
    assert VARSHESWARA_CANDIDATES[2]["candidate"] == "Lord of Muntha"
    assert "Table 73" in VARSHESWARA_CANDIDATES[4]["candidate"]


def test_table_73_is_transcribed_and_has_a_lord_in_both_columns():
    from hora.tajaka.varsheswara import (
        TABLE_73_TITLE,
        TABLE_73_TRIRAASI_LORDS,
        triraasi_lord,
    )

    assert TABLE_73_TITLE == "Triraasi Lords"
    assert sorted(TABLE_73_TRIRAASI_LORDS) == list(range(12))
    for rasi, (day, night) in TABLE_73_TRIRAASI_LORDS.items():
        assert 0 <= day <= 6 and 0 <= night <= 6, rasi
        assert triraasi_lord(rasi, daytime=True)["lord"] == day
        assert triraasi_lord(rasi, daytime=False)["lord"] == night
    # The section's own first row: Aries is the Sun by day and Jupiter by night.
    assert TABLE_73_TRIRAASI_LORDS[0] == (0, 4)


def test_the_last_four_rasis_have_one_triraasi_lord():
    from hora.core.const import RASI_ABBR
    from hora.tajaka.varsheswara import (
        TABLE_73_TRIRAASI_LORDS,
        THE_LAST_FOUR_RASIS_HAVE_ONE_TRIRAASI_LORD,
        triraasi_lord,
    )

    same = [rasi for rasi, (day, night) in TABLE_73_TRIRAASI_LORDS.items()
            if day == night]
    assert same == [8, 9, 10, 11]
    assert [RASI_ABBR[r] for r in same] == ["Sg", "Cp", "Aq", "Pi"]
    for rasi in same:
        assert triraasi_lord(rasi, daytime=True)["same_both_ways"] is True
    for rasi in range(8):
        assert triraasi_lord(rasi, daytime=True)["same_both_ways"] is False
    assert "The other eight rasis have different ones" in (
        THE_LAST_FOUR_RASIS_HAVE_ONE_TRIRAASI_LORD)


def test_the_sun_and_mercury_get_half_a_share_of_table_73():
    from collections import Counter

    from hora.tajaka.varsheswara import (
        TABLE_73_TRIRAASI_LORDS,
        THE_SUN_AND_MERCURY_GET_HALF_A_SHARE,
    )

    cells: Counter = Counter()
    for day, night in TABLE_73_TRIRAASI_LORDS.values():
        cells[day] += 1
        cells[night] += 1
    assert sum(cells.values()) == 24
    assert set(cells) == set(range(7))            # every graha appears
    assert cells[0] == cells[3] == 2              # Sun and Mercury
    for graha in (1, 2, 4, 5, 6):
        assert cells[graha] == 4
    assert "four cells each and the Sun and Mercury two each" in (
        THE_SUN_AND_MERCURY_GET_HALF_A_SHARE)


def test_no_aspect_on_lagna_means_the_sixth_or_eighth_house():
    from hora.tajaka.varsheswara import (
        NO_ASPECT_ON_LAGNA_MEANS_THE_SIXTH_OR_EIGHTH,
        aspect_on_lagna,
    )

    blank = []
    for candidate in range(12):
        got = aspect_on_lagna(candidate, 0)
        if got["aspect"] is None:
            blank.append(got["house_to_lagna"])
    assert sorted(blank) == [6, 8]
    # And a trine on lagna is a strong benefic, as §28.2 has it.
    trine = aspect_on_lagna(0, 4)                 # lagna is the 5th from it
    assert trine["aspect"] == "Trinal aspect"
    assert (trine["nature"], trine["strength"]) == ("benefic", "strong")
    assert "unless lagna is the 6th or 8th from it" in (
        NO_ASPECT_ON_LAGNA_MEANS_THE_SIXTH_OR_EIGHTH)


def test_the_five_candidates_are_found_for_chart_66():
    """Example 118's native in his 34th year, with muntha from §28.1 and the
    day-or-night from the ephemeris.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import RASI_ABBR
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local
    from hora.tajaka.harsha import year_began_in_daytime
    from hora.tajaka.muntha import muntha_rasi
    from hora.tajaka.varsheswara import candidates

    place = Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON)
    instant = from_local(*CHART_66, utc_offset_hours=5.5)
    annual = compute_chart(instant, place, Settings())
    natal = compute_chart(
        from_local(1967, 3, 8, 17, 40, 0.0, utc_offset_hours=5.5), place,
        Settings())
    daytime = year_began_in_daytime(instant.jd_ut, E118_LAT,
                                    E118_LON)["daytime"]
    assert daytime is False
    assert RASI_ABBR[natal.lagna_rasi] == "Le"
    assert RASI_ABBR[annual.lagna_rasi] == "Cp"

    muntha = muntha_rasi(natal.lagna_rasi, 34)
    rasis = {graha: int(annual.positions[graha].longitude // 30)
             for graha in range(7)}
    found = candidates(sun_rasi=rasis[0], moon_rasi=rasis[1],
                       natal_lagna_rasi=natal.lagna_rasi,
                       muntha_rasi=muntha["rasi"],
                       annual_lagna_rasi=annual.lagna_rasi, daytime=daytime)
    assert [row["graha_name"] for row in found] == [
        "Jupiter", "Sun", "Venus", "Saturn", "Mars"]
    # Night, so candidate (1) is the Moon's dispositor and not the Sun's.
    assert "held by the Moon" in found[0]["because"]


def test_the_cascade_shortlists_by_aspect_and_ranks_by_bala():
    from hora.tajaka.varsheswara import varsheswara

    # Lagna in Aries; a benefic aspect on it comes from the 5th, 9th, 3rd
    # or 11th house back, so a candidate in Sagittarius trines it.
    got = varsheswara(
        sun_rasi=0, moon_rasi=8, natal_lagna_rasi=8, muntha_rasi=8,
        annual_lagna_rasi=0, daytime=False,
        rasis={0: 8, 1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8},
        pancha_vargeeya={g: 5.0 for g in range(7)} | {4: 18.0})
    assert got["step"] == "benefic aspect on lagna"
    assert got["lord_name"] == "Jupiter"
    assert got["lord"]["grade"] == "very strong"
    assert got["undecided"] is None


def test_a_tie_on_bala_is_broken_by_the_number_of_categories():
    from hora.tajaka.varsheswara import varsheswara

    # Mars is candidate (2), (3) and (4); Jupiter only (5). Equal balas.
    got = varsheswara(
        sun_rasi=0, moon_rasi=0, natal_lagna_rasi=0, muntha_rasi=7,
        annual_lagna_rasi=0, daytime=False,
        rasis={g: 8 for g in range(7)},
        pancha_vargeeya={g: 12.0 for g in range(7)})
    assert got["step"] == "benefic aspect on lagna"
    assert got["lord_name"] == "Mars"
    assert len(got["lord"]["categories"]) >= 3


def test_an_unranked_candidate_stops_the_cascade_rather_than_being_dropped():
    """A pancha vargeeya bala left undecided by OI-153 cannot be ranked."""
    from hora.tajaka.varsheswara import varsheswara

    got = varsheswara(
        sun_rasi=0, moon_rasi=8, natal_lagna_rasi=8, muntha_rasi=8,
        annual_lagna_rasi=0, daytime=False,
        rasis={g: 8 for g in range(7)},
        pancha_vargeeya={g: 5.0 for g in range(7)} | {4: None})
    assert 4 in got["unranked"]
    assert got["lord"] is None
    assert "cannot be made" in got["undecided"]


def test_the_last_two_fallbacks_test_different_things():
    """OI-156. "an aspect on lagna" against "a strong aspect on lagna"."""
    from hora.tajaka.varsheswara import (
        SELECTION_FALLBACKS,
        THE_LAST_TWO_STEPS_TEST_DIFFERENT_THINGS,
        aspect_on_lagna,
    )

    assert "none of the planets has an aspect on lagna" in SELECTION_FALLBACKS
    assert "none of the candidates has a strong aspect on lagna" in (
        SELECTION_FALLBACKS)
    # A weak aspect on lagna exists, so the two conditions really do differ.
    weak = aspect_on_lagna(0, 2)                  # lagna is the 3rd from it
    assert weak["aspect"] == "Sextile aspect"
    assert weak["strength"] == "weak"
    assert weak["nature"] == "benefic"
    assert "the section gives no order between them" in (
        THE_LAST_TWO_STEPS_TEST_DIFFERENT_THINGS)


def test_the_cascade_uses_the_chapters_own_earlier_machinery():
    from hora.tajaka.aspects import TAJAKA_ASPECTS
    from hora.tajaka.panchavargeeya import PANCHA_VARGEEYA_GRADES
    from hora.tajaka.varsheswara import (
        SELECTION_PROCEDURE,
        SELECTION_RULE,
        THE_CASCADE_USES_28_2_AND_28_4_6S_OWN_VOCABULARY,
    )

    assert "benefic aspect on lagna" in SELECTION_PROCEDURE
    assert "panchavargeeya bala" in SELECTION_PROCEDURE
    # "strong" and "very strong" are §28.4.6's grades, not new words.
    grades = {row[2] for row in PANCHA_VARGEEYA_GRADES}
    assert "strong" in grades and "very strong" in grades
    assert "strong as per panchavargeeya bala" in SELECTION_RULE
    # And "benefic" is §28.2's classification.
    assert "benefic" in {entry["nature"] for entry in TAJAKA_ASPECTS}
    assert "section 28.2's classification" in (
        THE_CASCADE_USES_28_2_AND_28_4_6S_OWN_VOCABULARY)


def test_the_varsheswara_helpers_check_their_inputs():
    from hora.core import validate
    from hora.tajaka.varsheswara import (
        VarsheswaraError,
        aspect_on_lagna,
        triraasi_lord,
    )

    assert issubclass(VarsheswaraError, validate.InputError)
    for bad in (-1, 12):
        with pytest.raises(validate.InputError):
            triraasi_lord(bad, daytime=True)
        with pytest.raises(validate.InputError):
            aspect_on_lagna(bad, 0)


# --------------------------------------------------------------------------
# Example 120 — the lord of the year for Chart 66
# --------------------------------------------------------------------------


def _annual_and_natal():
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    place = Place(name="birthplace", latitude=E118_LAT, longitude=E118_LON)
    annual = compute_chart(from_local(*CHART_66, utc_offset_hours=5.5), place,
                           Settings())
    natal = compute_chart(
        from_local(1967, 3, 8, 17, 40, 0.0, utc_offset_hours=5.5), place,
        Settings())
    return annual, natal


def test_example_120s_five_candidacies_reproduce():
    from hora.core.const import RASI_ABBR
    from hora.tajaka.muntha import muntha_rasi
    from hora.tajaka.varsheswara import EXAMPLE_120_CANDIDATES, candidates

    annual, natal = _annual_and_natal()
    rasis = {graha: int(annual.positions[graha].longitude // 30)
             for graha in range(7)}
    assert RASI_ABBR[rasis[1]] == "Pi"           # the Moon, for a night year
    assert RASI_ABBR[natal.lagna_rasi] == "Le"
    muntha = muntha_rasi(natal.lagna_rasi, 34)
    assert muntha["rasi_name"] == "Taurus"
    assert RASI_ABBR[annual.lagna_rasi] == "Cp"

    found = candidates(sun_rasi=rasis[0], moon_rasi=rasis[1],
                       natal_lagna_rasi=natal.lagna_rasi,
                       muntha_rasi=muntha["rasi"],
                       annual_lagna_rasi=annual.lagna_rasi, daytime=False)
    assert {row["category"]: row["graha"] for row in found} == (
        EXAMPLE_120_CANDIDATES)
    assert [row["graha_name"] for row in found] == [
        "Jupiter", "Sun", "Venus", "Saturn", "Mars"]


def test_example_120s_five_aspects_on_lagna_reproduce():
    """Venus conjoins, Jupiter and Saturn square, the Sun semi-sextiles and
    Mars sextiles the Capricorn lagna.
    """
    from hora.tajaka.varsheswara import EXAMPLE_120_ASPECTS, aspect_on_lagna

    annual, _natal = _annual_and_natal()
    lagna = annual.lagna_rasi
    for graha, (name, nature) in EXAMPLE_120_ASPECTS.items():
        where = int(annual.positions[graha].longitude // 30)
        got = aspect_on_lagna(where, lagna)
        assert got["aspect"] == name, graha
        assert got["nature"] == nature, graha
    # "All of them are malefic aspects" — Venus, Jupiter and Saturn.
    malefic = {g for g, (_n, nature) in EXAMPLE_120_ASPECTS.items()
               if nature == "malefic"}
    assert malefic == {4, 5, 6}
    # And Mars alone is benefic.
    benefic = {g for g, (_n, nature) in EXAMPLE_120_ASPECTS.items()
               if nature == "benefic"}
    assert benefic == {2}


def test_example_120s_lord_of_the_year_reproduces():
    from hora.tajaka.muntha import muntha_rasi
    from hora.tajaka.varsheswara import (
        EXAMPLE_120_LORD,
        EXAMPLE_120_MARS_BALA,
        varsheswara,
    )

    annual, natal = _annual_and_natal()
    rasis = {graha: int(annual.positions[graha].longitude // 30)
             for graha in range(7)}
    muntha = muntha_rasi(natal.lagna_rasi, 34)
    got = varsheswara(sun_rasi=rasis[0], moon_rasi=rasis[1],
                      natal_lagna_rasi=natal.lagna_rasi,
                      muntha_rasi=muntha["rasi"],
                      annual_lagna_rasi=annual.lagna_rasi, daytime=False,
                      rasis=rasis,
                      pancha_vargeeya={0: 8.4, 1: 6.2,
                                       2: EXAMPLE_120_MARS_BALA, 3: 5.3,
                                       4: 9.2, 5: 9.0, 6: 5.0})
    assert got["step"] == "benefic aspect on lagna"
    assert got["lord"]["graha"] == EXAMPLE_120_LORD == 2
    assert got["lord_name"] == "Mars"
    assert got["undecided"] is None


def test_the_example_never_exercises_the_cascade_past_the_shortlist():
    from hora.tajaka.muntha import muntha_rasi
    from hora.tajaka.varsheswara import (
        THE_EXAMPLE_STOPS_AT_THE_SHORTLIST,
        varsheswara,
    )

    annual, natal = _annual_and_natal()
    rasis = {graha: int(annual.positions[graha].longitude // 30)
             for graha in range(7)}
    got = varsheswara(sun_rasi=rasis[0], moon_rasi=rasis[1],
                      natal_lagna_rasi=natal.lagna_rasi,
                      muntha_rasi=muntha_rasi(natal.lagna_rasi, 34)["rasi"],
                      annual_lagna_rasi=annual.lagna_rasi, daytime=False,
                      rasis=rasis,
                      pancha_vargeeya={g: 10.0 for g in range(7)})
    # One member, so the ranking cannot decide anything.
    assert len(got["shortlist"]) == 1
    assert got["lord_name"] == "Mars"
    assert "nothing in Example 120 turns on the ranking" in (
        THE_EXAMPLE_STOPS_AT_THE_SHORTLIST)


def test_example_120_rules_out_reading_the_relationship_from_the_planet():
    """OI-153. Mars's 13.7 needs his navamsa rasi scored as an enemy's, and
    chapter 3 makes Saturn only neutral to Mars.
    """
    from hora.charts.relationship import compound, natural, temporary
    from hora.charts.vargas import d3_drekkana, d9_navamsa
    from hora.core.const import RASI_LORD
    from hora.tajaka.panchavargeeya import (
        EXAMPLE_120_RULES_OUT_THE_PLANETS_OWN_VIEW,
        drekkana_bala,
        hadda_bala,
        hadda_lord,
        kshetra_bala,
        navamsa_bala,
        pancha_vargeeya_bala,
        uchcha_bala,
    )
    from hora.tajaka.varsheswara import EXAMPLE_120_MARS_BALA

    annual, _natal = _annual_and_natal()
    mars, longitude = 2, annual.positions[2].longitude
    uchcha = uchcha_bala(mars, longitude)["units"]

    # Four of the five are not in dispute.
    assert int(RASI_LORD[int(longitude // 30)]) == 4          # Jupiter's Pisces
    assert natural(mars, 4) == "friend"
    assert hadda_lord(longitude)["lord"] == mars              # his own hadda
    assert int(RASI_LORD[d3_drekkana(longitude).sign]) == mars

    navamsa_owner = int(RASI_LORD[d9_navamsa(longitude).sign])
    assert navamsa_owner == 6                                 # Saturn's
    # Asymmetric, and that is the whole point.
    assert natural(mars, 6) == "neutral"
    assert natural(6, mars) == "enemy"

    def total(navamsa_grade):
        return pancha_vargeeya_bala(
            kshetra=kshetra_bala("friend")["units"], uchcha=uchcha,
            hadda=hadda_bala("own")["units"],
            drekkana=drekkana_bala("own")["units"],
            navamsa=navamsa_bala(navamsa_grade)["units"])

    # The planet's own view leaves it undecided and short of the printed value.
    from_planet = total(natural(mars, 6))
    assert from_planet["undecided"] is True
    assert round(from_planet["at_least"], 1) != EXAMPLE_120_MARS_BALA

    # The lord's view reaches it exactly.
    from_lord = total(natural(6, mars))
    assert round(from_lord["units"], 1) == EXAMPLE_120_MARS_BALA

    # And so does the compound relationship, which is why one number cannot
    # choose between them.
    navamsa_signs = {g: d9_navamsa(annual.positions[g].longitude).sign
                     for g in (mars, 6)}
    together = compound(natural(mars, 6),
                        temporary(navamsa_signs[mars], navamsa_signs[6]))
    assert together == "enemy"
    assert round(total(together)["units"], 1) == EXAMPLE_120_MARS_BALA
    assert "one printed number cannot choose between them" in (
        EXAMPLE_120_RULES_OUT_THE_PLANETS_OWN_VIEW)


def test_only_one_possible_combination_of_grades_reaches_13_7():
    """The uniqueness that makes the finding above evidence rather than a
    guess: with kshetra fixed at a friend's 15, nothing else lands on 13.7.
    """
    from hora.tajaka.panchavargeeya import uchcha_bala

    annual, _natal = _annual_and_natal()
    uchcha = uchcha_bala(2, annual.positions[2].longitude)["units"]
    hits = [
        (k, h, d, n)
        for k in (30.0, 15.0, 7.5)
        for h in (15.0, 7.5, 3.75)
        for d in (10.0, 5.0, 2.5)
        for n in (5.0, 2.5, 1.25)
        if abs((k + uchcha + h + d + n) / 4 - 13.7) < 0.05
    ]
    assert len(hits) == 4
    # Mars is in Pisces, so kshetra cannot be his own 30 — which leaves one.
    possible = [row for row in hits if row[0] != 30.0]
    assert possible == [(15.0, 15.0, 10.0, 1.25)]


def test_example_120_is_transcribed_with_its_slip():
    from hora.tajaka.varsheswara import (
        EXAMPLE_120,
        EXAMPLE_120_CANDIDACIES,
        EXAMPLE_120_CONCLUSION,
        EXAMPLE_120_HAS_A_SLIP_IN_ITS_CONCLUSION,
    )

    assert "annual chart in Example 118" in EXAMPLE_120
    assert len(EXAMPLE_120_CANDIDACIES) == 5
    assert "4:41 am, i.e. night time" in EXAMPLE_120_CANDIDACIES[0]
    assert "from Table 73" in EXAMPLE_120_CANDIDACIES[4]
    assert "Mars is the lord of the year" in EXAMPLE_120_CONCLUSION
    assert "He is also has" in EXAMPLE_120_CONCLUSION
    assert "Nothing turns on it" in EXAMPLE_120_HAS_A_SLIP_IN_ITS_CONCLUSION
