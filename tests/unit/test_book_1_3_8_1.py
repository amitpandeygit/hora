"""§1.3.8.1 Tithis — the definition, Table 3, the four-step procedure.

Example 2 is the section's worked case and is checked at every intermediate,
not only at the answer: the difference, the sign flip, the normalised
elongation, the quotient, the index and the paksha-qualified name.
"""
import pytest

from hora.charts.tithi import (
    PAKSHA_ELONGATION,
    TITHI_SPAN,
    TITHIS_PER_MONTH,
    TITHIS_PER_PAKSHA,
    elongation,
    tithi,
)
from hora.core import const as c
from hora.services import tithi_service


def lon(degrees: float, rasi_index: int, minutes: float = 0.0) -> float:
    return rasi_index * 30 + degrees + minutes / 60


# --------------------------------------------------------------------------
# The definition
# --------------------------------------------------------------------------

def test_a_tithi_is_twelve_degrees_of_elongation():
    """"a period in which the difference between the longitudes of Moon and
    Sun changes by exactly 12 degrees"."""
    assert TITHI_SPAN == 12.0
    assert TITHIS_PER_MONTH == 30
    assert TITHI_SPAN * TITHIS_PER_MONTH == 360.0


def test_fifteen_tithis_repeat_in_each_fortnight():
    """"There are 15 tithis and the same tithis repeat in the brigher and
    darker fortnights."""
    assert TITHIS_PER_PAKSHA == 15
    assert len(c.TITHI_NAMES_BOOK) == TITHIS_PER_MONTH
    assert TITHIS_PER_PAKSHA * 2 == TITHIS_PER_MONTH
    # Fourteen of the fifteen names repeat; the 15th and 30th are unique.
    first, second = c.TITHI_NAMES_BOOK[:15], c.TITHI_NAMES_BOOK[15:]
    assert first[:14] == second[:14]
    assert first[14] == "Paurnami" and second[14] == "Amavasya"


def test_the_pakshas_span_the_halves_of_the_elongation():
    """"During Sukla ... between 0 and 180 degrees. During Krishna ... between
    180 and 360 degrees."""
    assert PAKSHA_ELONGATION == ((0.0, 180.0), (180.0, 360.0))
    assert tithi(0.0, 90.0).paksha_name == "Sukla"       # 90 deg ahead, waxing
    assert tithi(0.0, 270.0).paksha_name == "Krishna"    # 270 deg ahead, waning


def test_a_month_starts_when_sun_and_moon_share_a_longitude():
    """"When Sun and Moon are at the same longitude, a new lunar month of 30
    tithis starts."""
    first = tithi(100.0, 100.0)
    assert first.index == 1
    assert first.elongation == 0.0
    assert first.completed == 0


def test_the_differential_is_twelve_n_after_n_tithis():
    """"Sun-Moon longitude differential will be (12 x n) after exactly n
    tithis."""
    for n in range(1, 30):
        # Just past the boundary, the (n+1)th tithi is running.
        assert tithi(0.0, n * TITHI_SPAN + 1e-6).index == n + 1
        # Just before it, the nth is.
        assert tithi(0.0, n * TITHI_SPAN - 1e-6).index == n


# --------------------------------------------------------------------------
# Table 3
# --------------------------------------------------------------------------

#: Table 3 as printed: sukla number, name, lord.
TABLE_3 = [
    (1, "Pratipada", "Sun"), (2, "Dwitiya", "Moon"), (3, "Tritiya", "Mars"),
    (4, "Chaturthi", "Mercury"), (5, "Panchami", "Jupiter"),
    (6, "Shashti", "Venus"), (7, "Saptami", "Saturn"), (8, "Ashtami", "Rahu"),
    (9, "Navami", "Sun"), (10, "Dasami", "Moon"), (11, "Ekadasi", "Mars"),
    (12, "Dwadasi", "Mercury"), (13, "Trayodasi", "Jupiter"),
    (14, "Chaturdasi", "Venus"), (15, "Paurnami", "Saturn"),
]


@pytest.mark.parametrize("number,name,lord", TABLE_3)
def test_table_3_names_and_lords(number, name, lord):
    assert c.TITHI_NAMES_BOOK[number - 1] == name
    assert c.GRAHA_NAMES[c.TITHI_LORD[number - 1]] == lord


@pytest.mark.parametrize("number,name,lord", TABLE_3)
def test_table_3_rows_reach_the_rules_endpoint(number, name, lord):
    row = tithi_service.rules()["table_3"][number - 1]
    assert row["sukla"] == number
    assert row["name"] == name
    assert row["lord_name"] == lord
    # The darker fortnight repeats each name fifteen later, except the 15th.
    assert row["krishna"] == (number + 15 if number < 15 else None)


def test_the_thirtieth_tithi_is_amavasya():
    """Table 3's last row: the new moon has no counterpart in Sukla paksha.

    Naming it by its position in the paksha gives "Krishna Paurnami", which is
    not a tithi. The first cut of this engine did exactly that.
    """
    new_moon = tithi(0.0, 29 * TITHI_SPAN + 1.0)
    assert new_moon.index == 30
    assert new_moon.paksha_name == "Krishna"
    assert new_moon.name == "Amavasya"
    assert new_moon.full_name == "Amavasya", "written unqualified — it occurs once"
    assert tithi_service.rules()["new_moon"]["name"] == "Amavasya"


def test_the_two_unique_tithis_are_written_unqualified():
    """Paurnami and Amavasya each occur once, so they take no fortnight
    prefix. Every other tithi does."""
    from hora.charts.tithi import UNIQUE_TITHIS

    assert set(UNIQUE_TITHIS) == {15, 30}
    for index in range(1, 31):
        result = tithi(0.0, (index - 1) * TITHI_SPAN + 1.0)
        if index in UNIQUE_TITHIS:
            assert result.full_name == result.name, index
        else:
            assert result.full_name.startswith(result.paksha_name + " "), index


def test_the_fifteenth_tithi_is_the_full_moon():
    full = tithi(0.0, 14 * TITHI_SPAN + 1.0)
    assert full.index == 15
    assert full.name == "Paurnami"
    assert full.full_name == "Paurnami"
    assert full.paksha_name == "Sukla"
    assert "Poornima" in full.alternate_names


# --------------------------------------------------------------------------
# The naming convention
# --------------------------------------------------------------------------

def test_the_fortnight_comes_first_in_the_name():
    """"We write the classification of fortnight (Sukla or Krishna) first and
    then write tithi name."

    "Sukla Saptami" is the 7th tithi; "Krishna Saptami" is the 22nd.
    """
    sukla = tithi(0.0, 6 * TITHI_SPAN + 1.0)
    assert sukla.index == 7
    assert sukla.full_name == "Sukla Saptami"

    krishna = tithi(0.0, 21 * TITHI_SPAN + 1.0)
    assert krishna.index == 22
    assert krishna.full_name == "Krishna Saptami"
    assert krishna.name == sukla.name, "the same fifteen names repeat"


# --------------------------------------------------------------------------
# Example 2
# --------------------------------------------------------------------------

#: "Moon is at 24 deg 12' in Gemini... Sun is at 17 deg 46' in Scorpio."
EXAMPLE_2_MOON = lon(24, 2, 12)      # 84 deg 12'
EXAMPLE_2_SUN = lon(17, 7, 46)       # 227 deg 46'


def test_example_2_the_longitudes_from_the_beginning_of_the_zodiac():
    """"This is (2 x 30) + 24 deg 12' = 84 deg 12'" and "(7 x 30) + 17 deg
    46' = 227 deg 46'"."""
    assert EXAMPLE_2_MOON == pytest.approx(84 + 12 / 60)
    assert EXAMPLE_2_SUN == pytest.approx(227 + 46 / 60)


def test_example_2_step_1_the_difference_is_negative_and_is_corrected():
    """"Moon - Sun = 84 deg 12' - 227 deg 46' = -(143 deg 34'). It is negative
    because Sun is at a higher longitude. We have to add 360 to it... It
    becomes 216 deg 26'."""
    result = tithi(EXAMPLE_2_SUN, EXAMPLE_2_MOON)
    assert result.raw_difference == pytest.approx(-(143 + 34 / 60))
    assert result.elongation == pytest.approx(216 + 26 / 60)
    assert elongation(EXAMPLE_2_SUN, EXAMPLE_2_MOON) == pytest.approx(result.elongation)


def test_example_2_step_2_the_quotient_is_eighteen():
    """"Converting this to a decimal number, we get 216.43... We find
    216.43 / 12 and the quotient is 18. So 18 tithis are over."""
    result = tithi(EXAMPLE_2_SUN, EXAMPLE_2_MOON)
    assert result.elongation == pytest.approx(216.43, abs=0.005)
    assert result.completed == 18


def test_example_2_step_3_the_nineteenth_tithi_is_running():
    """"Adding 1 to it, we get 19 and so the 19th tithi is running."""
    assert tithi(EXAMPLE_2_SUN, EXAMPLE_2_MOON).index == 19


def test_example_2_step_4_is_krishna_chaturthi():
    """"Referring to Table 3, we see that this is 'Chaturthi' tithi of Krishna
    paksha (darker fortnight). So it is 'Krishna Chaturthi'."""
    result = tithi(EXAMPLE_2_SUN, EXAMPLE_2_MOON)
    assert result.name == "Chaturthi"
    assert result.paksha_name == "Krishna"
    assert result.number_in_paksha == 4
    assert result.full_name == "Krishna Chaturthi"
    assert result.lord_name == "Mercury", "Table 3 gives Mercury for the 4th"


def test_example_2_reports_all_four_steps():
    result = tithi(EXAMPLE_2_SUN, EXAMPLE_2_MOON)
    assert [s.number for s in result.steps] == [1, 2, 3, 4]
    assert all(s.description and s.detail for s in result.steps)
    assert "+ 360" in result.steps[0].detail, "the sign correction is shown"


def test_example_2_through_the_service():
    payload = tithi_service.tithi(EXAMPLE_2_SUN, EXAMPLE_2_MOON)
    assert payload["index"] == 19
    assert payload["full_name"] == "Krishna Chaturthi"
    assert payload["completed"] == 18
    assert payload["alternate_names"] == ["Chaviti", "Chauth"]


# --------------------------------------------------------------------------
# The whole range behaves
# --------------------------------------------------------------------------

def test_every_elongation_yields_a_tithi_between_one_and_thirty():
    for tenth in range(3600):
        result = tithi(0.0, tenth / 10.0)
        assert 1 <= result.index <= 30
        assert 1 <= result.number_in_paksha <= 15
        assert 0.0 <= result.fraction_elapsed < 1.0


def test_the_index_and_the_paksha_agree_everywhere():
    """Tithis 1-15 are Sukla, 16-30 Krishna, with no off-by-one at 180."""
    for tenth in range(3600):
        result = tithi(0.0, tenth / 10.0)
        expected = 0 if result.index <= 15 else 1
        assert result.paksha == expected, result.elongation


def test_a_non_finite_longitude_is_refused():
    from hora.core.validate import InputError

    with pytest.raises(InputError):
        tithi(float("nan"), 100.0)


@pytest.mark.parametrize("index,lord", [
    (1, "Sun"), (7, "Saturn"), (8, "Rahu"), (15, "Saturn"), (19, "Mercury"),
    (22, "Saturn"), (23, "Rahu"), (30, "Rahu"),
])
def test_the_lord_is_taken_by_tithi_number_not_paksha_position(index, lord):
    """Table 3's Planet column, checked at both ends and at the two unique rows.

    The 30th is Rahu. Indexing by position within the paksha gives Saturn —
    Paurnami's lord — which the first cut of this engine did.
    """
    assert tithi(0.0, (index - 1) * TITHI_SPAN + 1.0).lord_name == lord


def test_every_tithi_name_and_lord_come_from_the_same_row():
    """Name and lord must never disagree about which row they read."""
    for index in range(1, 31):
        result = tithi(0.0, (index - 1) * TITHI_SPAN + 1.0)
        assert result.name == c.TITHI_NAMES_BOOK[index - 1], index
        assert result.lord == int(c.TITHI_LORD[index - 1]), index


# --------------------------------------------------------------------------
# Exercise 3
# --------------------------------------------------------------------------

#: "Moon is at 14 deg 43' in Leo. Sun is at 28 deg 13' in Capricorn."
EXERCISE_3_MOON = lon(14, 4, 43)     # 134 deg 43'
EXERCISE_3_SUN = lon(28, 9, 13)      # 298 deg 13'


def test_exercise_3_the_longitudes_from_the_beginning_of_the_zodiac():
    """Leo is the 5th sign and Capricorn the 10th, so (4 x 30) and (9 x 30)."""
    assert EXERCISE_3_MOON == pytest.approx(134 + 43 / 60)
    assert EXERCISE_3_SUN == pytest.approx(298 + 13 / 60)


def test_exercise_3_step_1_the_difference_is_negative_and_is_corrected():
    """134 deg 43' - 298 deg 13' = -(163 deg 30'), + 360 = 196 deg 30'."""
    result = tithi(EXERCISE_3_SUN, EXERCISE_3_MOON)
    assert result.raw_difference == pytest.approx(-(163 + 30 / 60))
    assert result.elongation == pytest.approx(196.5)


def test_exercise_3_step_2_the_quotient_is_sixteen():
    """196.5 / 12 = 16.375, so 16 tithis are over."""
    assert tithi(EXERCISE_3_SUN, EXERCISE_3_MOON).completed == 16


def test_exercise_3_step_3_the_seventeenth_tithi_is_running():
    """The answer names it: "17th tithi"."""
    assert tithi(EXERCISE_3_SUN, EXERCISE_3_MOON).index == 17


def test_exercise_3_is_krishna_dwitiya():
    """"Krishna Dwitiya (17th tithi or the 2nd tithi in the darker fortnight)."""
    result = tithi(EXERCISE_3_SUN, EXERCISE_3_MOON)
    assert result.index == 17
    assert result.paksha_name == "Krishna"
    assert result.number_in_paksha == 2, "the answer states the 2nd of the fortnight"
    assert result.name == "Dwitiya"
    assert result.full_name == "Krishna Dwitiya"


def test_exercise_3_through_the_service():
    payload = tithi_service.tithi(EXERCISE_3_SUN, EXERCISE_3_MOON)
    assert payload["index"] == 17
    assert payload["full_name"] == "Krishna Dwitiya"
    assert payload["number_in_paksha"] == 2
    assert payload["lord_name"] == "Moon", "Table 3 gives Moon for the 2nd"
