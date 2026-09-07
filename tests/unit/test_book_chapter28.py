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
