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
        "Kshetra bala", "Uchcha bala", "Hadda bala", "Drekkana bala"]
    assert [row["maximum"] for row in supplied] == [30.0, 20.0, 15.0, 10.0]
    assert len(PANCHA_VARGAS_PENDING) == 2
    assert "Final Computation" in PANCHA_VARGAS_PENDING[-1]


def test_only_the_supplied_vargas_are_built():
    """The coverage line. It fails the moment a pending source appears."""
    import hora.tajaka.panchavargeeya as module

    for absent in ("navamsa_bala", "pancha_vargeeya_bala"):
        assert not hasattr(module, absent), absent
    for present in ("kshetra_bala", "uchcha_bala", "hadda_bala",
                    "hadda_lord", "drekkana_bala"):
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


def test_28_4_4s_drekkana_bala_and_the_thirty_over_n_series():
    from hora.tajaka.panchavargeeya import (
        DREKKANA_BALA_RULE,
        DREKKANA_BALA_UNITS,
        HADDA_BALA_UNITS,
        KSHETRA_BALA_UNITS,
        THE_PLACE_BALAS_ARE_THIRTY_OVER_N,
        UCHCHA_BALA_MAXIMUM,
        drekkana_bala,
    )

    assert DREKKANA_BALA_UNITS == {"own": 10.0, "friend": 5.0, "enemy": 2.5}
    assert "drekkana chart (D-3)" in DREKKANA_BALA_RULE
    for grade in ("own", "friend", "enemy"):
        assert drekkana_bala(grade)["units"] == DREKKANA_BALA_UNITS[grade]
    # Thirty over one, two and three.
    tops = [KSHETRA_BALA_UNITS["own"], HADDA_BALA_UNITS["own"],
            DREKKANA_BALA_UNITS["own"]]
    assert tops == [30.0, 15.0, 10.0]
    for n, top in enumerate(tops, 1):
        assert top == pytest.approx(30.0 / n)
    # And each halves twice within itself.
    for units in (KSHETRA_BALA_UNITS, HADDA_BALA_UNITS, DREKKANA_BALA_UNITS):
        assert units["own"] == units["friend"] * 2 == units["enemy"] * 4
    # Uchcha's twenty is outside the series.
    assert UCHCHA_BALA_MAXIMUM not in tops
    assert "belongs to no such series" in THE_PLACE_BALAS_ARE_THIRTY_OVER_N


def test_the_neutral_gap_repeats_in_all_three_place_balas():
    from hora.tajaka.panchavargeeya import (
        THE_NEUTRAL_GAP_REPEATS_IN_ALL_THREE_PLACE_BALAS,
        drekkana_bala,
        hadda_bala,
        kshetra_bala,
    )

    for scorer in (kshetra_bala, hadda_bala, drekkana_bala):
        got = scorer("neutral")
        assert got["undecided"] is True
        assert got["units"] is None
    assert "None of the three prices a neutral's" in (
        THE_NEUTRAL_GAP_REPEATS_IN_ALL_THREE_PLACE_BALAS)
