"""Section 1.3.9, Yogas — the procedure, Table 5, and Example 3.

Table 5 is transcribed row by row, both columns, because the meanings are
content and not derivable. Example 3 is checked at every intermediate the book
prints, including its arcminute arithmetic (7870' / 800' = 9.8375).

The boundary tests are the reason this module exists rather than reusing
`panchanga.core.yoga_at`: dividing by 360/27 as a float lands one yoga early
at nine of the twenty-seven boundaries. See OI-39.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.yoga import (
    MINUTES_PER_DEGREE,
    YOGA_SPAN,
    YOGA_SPAN_MINUTES,
    YOGAS_PER_CIRCLE,
    Yoga,
    completed_spans,
    raw_sum,
    reduced_sum,
    to_minutes,
    yoga,
    yoga_of_index,
)
from hora.core import const as c
from hora.core.validate import InputError
from hora.services import yoga_service

client = TestClient(app)


def lon(deg: float, rasi: int, minutes: float = 0.0) -> float:
    """A longitude written the book's way: degrees within a 0-based rasi."""
    return rasi * 30.0 + deg + minutes / 60.0


# --------------------------------------------------------------------------
# The procedure
# --------------------------------------------------------------------------


def test_a_yoga_uses_the_sum_of_the_longitudes():
    """"Add the longitudes of Sun and Moon."

    This is the one thing that separates a yoga from a tithi, which takes the
    difference. Asserted directly so no one later "shares" the two.
    """
    assert raw_sum(100.0, 30.0) == 130.0
    assert yoga(100.0, 30.0).index == yoga(30.0, 100.0).index, "the sum commutes"


def test_the_sum_is_reduced_by_360_when_it_exceeds_360():
    """"Remove 360° from the sum if it is greater than 360°."""
    assert reduced_sum(300.0, 200.0) == pytest.approx(140.0)
    assert reduced_sum(100.0, 30.0) == pytest.approx(130.0), "not over 360, untouched"


def test_the_divisor_is_one_nakshatra():
    """"Divide the sum by the length of one nakshatra (13°20' or 800')."""
    assert YOGA_SPAN == pytest.approx(13 + 20 / 60)
    assert YOGA_SPAN_MINUTES == 800
    assert YOGA_SPAN * MINUTES_PER_DEGREE == pytest.approx(YOGA_SPAN_MINUTES)
    assert YOGA_SPAN == c.NAKSHATRA_SPAN


def test_there_are_twenty_seven_yogas():
    assert YOGAS_PER_CIRCLE == 27
    assert len(c.YOGA_NAMES_BOOK) == len(c.YOGA_MEANINGS) == 27
    assert YOGA_SPAN * YOGAS_PER_CIRCLE == pytest.approx(360.0)


def test_fractions_are_ignored_then_one_is_added():
    """"Ignore fractions and take the integer part. Add 1 to it and the result
    is the index of the yoga running."""
    assert completed_spans(0.0) == 0
    assert yoga(0.0, 0.0).index == 1, "zero is inside the first yoga, not the zeroth"
    assert yoga(0.0, 359.999).index == 27


def test_the_index_never_leaves_one_to_twenty_seven():
    for tenth in range(3600):
        assert 1 <= yoga(tenth / 10.0, 0.0).index <= 27


# --------------------------------------------------------------------------
# Boundary arithmetic — the reason for completed_spans
# --------------------------------------------------------------------------


@pytest.mark.parametrize("k", range(27))
def test_every_boundary_starts_its_own_yoga(k):
    """A sum of exactly k nakshatra spans starts the (k+1)th yoga.

    ``k * YOGA_SPAN // YOGA_SPAN`` returns k-1 at nine of these because
    360/27 is not representable in binary. Nine of twenty-seven is not an
    edge case worth waving through, and book exercises use round values.
    """
    assert completed_spans(k * YOGA_SPAN) == k
    assert yoga(k * YOGA_SPAN, 0.0).index == k + 1


def test_the_naive_float_division_really_does_fail():
    """Guards the guard: if this ever stops failing, the boundary tests above
    have stopped proving anything and can be simplified away."""
    naive = [k for k in range(27) if int((k * YOGA_SPAN) // YOGA_SPAN) != k]
    assert naive == [3, 6, 9, 12, 15, 18, 19, 21, 24], (
        "the float-division defect this module avoids"
    )


def test_a_hair_below_a_boundary_is_still_the_previous_yoga():
    assert yoga(4 * YOGA_SPAN - 1e-9, 0.0).index == 4
    assert yoga(4 * YOGA_SPAN, 0.0).index == 5


# --------------------------------------------------------------------------
# Table 5, transcribed
# --------------------------------------------------------------------------

#: Table 5 exactly as printed: index, yoga, meaning.
TABLE_5 = [
    (1, "Vishkambha", "Door bolt/supporting pillar"),
    (2, "Preeti", "Love/affection"),
    (3, "Aayushmaan", "Long-lived"),
    (4, "Saubhaagya", "Long life of spouse (good fortune)"),
    (5, "Sobhana", "Splendid, bright"),
    (6, "Atiganda", "Great danger"),
    (7, "Sukarman", "One with good deeds"),
    (8, "Dhriti", "Firmness"),
    (9, "Shoola", "Shiva's weapon of destruction (pain)"),
    (10, "Ganda", "Danger"),
    (11, "Vriddhi", "Growth"),
    (12, "Dhruva", "Fixed, constant"),
    (13, "Vyaaghaata", "Great blow"),
    (14, "Harshana", "Cheerful"),
    (15, "Vajra", "Diamond (strong)"),
    (16, "Siddhi", "Accomplishment"),
    (17, "Vyatipaata", "Great fall"),
    (18, "Variyan", "Chief/best"),
    (19, "Parigha", "Obstacle/hindrance"),
    (20, "Shiva", "Lord Shiva (purity)"),
    (21, "Siddha", "Accomplished/ready"),
    (22, "Saadhya", "Possible"),
    (23, "Subha", "Auspicious"),
    (24, "Sukla", "White, bright"),
    (25, "Brahma", "Creator (good knowledge and purity)"),
    (26, "Indra", "Ruler of gods"),
    (27, "Vaidhriti", "A class of gods"),
]


@pytest.mark.parametrize("index,name,meaning", TABLE_5)
def test_table_5_row_by_row(index, name, meaning):
    assert yoga_of_index(index) == (name, meaning)


@pytest.mark.parametrize("index,name,meaning", TABLE_5)
def test_table_5_is_reached_by_calculation_not_only_by_lookup(index, name, meaning):
    """Each row is also produced by a sum that lands inside that yoga."""
    result = yoga((index - 1) * YOGA_SPAN + 1.0, 0.0)
    assert result.index == index
    assert result.name_book == name
    assert result.meaning == meaning


def test_table_5_is_served_whole():
    rows = yoga_service.table_5()
    assert [(r["index"], r["name"], r["meaning"]) for r in rows] == TABLE_5


def test_every_yoga_name_is_distinct():
    assert len(set(c.YOGA_NAMES_BOOK)) == 27


def test_siddhi_and_siddha_are_two_different_yogas():
    """Rows 16 and 21 are near-homographs with different meanings."""
    assert yoga_of_index(16) == ("Siddhi", "Accomplishment")
    assert yoga_of_index(21) == ("Siddha", "Accomplished/ready")


def test_shiva_is_both_a_yoga_name_and_inside_another_meaning():
    """Row 20 is named Shiva; row 9's meaning also mentions Shiva. A substring
    match on "Shiva" would confuse the two — the guard that OI-35 was about."""
    assert yoga_of_index(20)[0] == "Shiva"
    assert "Shiva" in yoga_of_index(9)[1]
    assert yoga_of_index(9)[0] == "Shoola"


def test_an_index_outside_the_table_is_rejected():
    for bad in (0, 28, -1):
        with pytest.raises(InputError):
            yoga_of_index(bad)


# --------------------------------------------------------------------------
# Example 3
# --------------------------------------------------------------------------

#: "Suppose Sun is at 23°50' in Cp and Moon is at 17°20' in Li."
EXAMPLE_3_SUN = lon(23, 9, 50)      # 293 deg 50'
EXAMPLE_3_MOON = lon(17, 6, 20)     # 197 deg 20'


def test_example_3_the_longitudes_from_the_beginning_of_the_zodiac():
    """"Sun's longitude is 23°50' + 9 x 30° = 293°50' and Moon's longitude is
    17°20' + 6 x 30° = 197°20'."""
    assert EXAMPLE_3_SUN == pytest.approx(293 + 50 / 60)
    assert EXAMPLE_3_MOON == pytest.approx(197 + 20 / 60)


def test_example_3_step_1_the_sum_and_its_reduction():
    """"The sum is 293°50' + 197°20' = 491°10'. By subtracting 360°, we get
    131°10'."""
    result = yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON)
    assert result.raw_sum == pytest.approx(491 + 10 / 60)
    assert result.total == pytest.approx(131 + 10 / 60)


def test_example_3_step_2_the_sum_in_arcminutes():
    """"This is equivalent to 131 x 60 + 10 = 7870'."

    The book divides in arcminutes, so the arcminute value is published and
    asserted, not only the degrees it came from.
    """
    result = yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON)
    assert result.total_minutes == pytest.approx(7870.0)
    assert to_minutes(131 + 10 / 60) == pytest.approx(131 * 60 + 10)


def test_example_3_step_2_the_quotient():
    """"By dividing this with 800', we get 9.8375."""
    assert yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON).quotient == pytest.approx(9.8375)


def test_example_3_step_3_ignoring_the_fraction_gives_nine():
    """"Ignoring the fraction, we get 9."""
    assert yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON).completed == 9


def test_example_3_step_4_adding_one_gives_ten():
    """"Adding 1 to it, we get 10."""
    assert yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON).index == 10


def test_example_3_step_5_is_ganda_yoga():
    """"From Table 5, we see that the 10th yoga is "Ganda yoga"."""
    result = yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON)
    assert result.name_book == "Ganda"
    assert result.meaning == "Danger"


def test_example_3_reports_all_five_steps():
    result = yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON)
    assert [s.number for s in result.steps] == [1, 2, 3, 4, 5]
    assert all(s.description and s.detail for s in result.steps)
    assert "- 360" in result.steps[0].detail, "the reduction is shown"
    assert "7870" in result.steps[1].detail, "the book's arcminutes are shown"


def test_example_3_through_the_service():
    payload = yoga_service.yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON)
    assert payload["index"] == 10
    assert payload["name_book"] == "Ganda"
    assert payload["completed"] == 9
    assert payload["total_minutes"] == pytest.approx(7870.0)


def test_example_3_through_the_endpoint():
    body = client.post(
        "/v1/yoga/compute",
        json={"sun_longitude": EXAMPLE_3_SUN, "moon_longitude": EXAMPLE_3_MOON},
    ).json()
    assert body["index"] == 10
    assert body["name_book"] == "Ganda"
    assert body["meaning"] == "Danger"
    assert body["quotient"] == pytest.approx(9.8375)


def test_example_3_agrees_with_the_panchanga_yoga():
    """The existing one-line implementation gets this example right; it is the
    boundaries it misses. Kept so the two do not silently diverge elsewhere."""
    from hora.panchanga.core import yoga_at

    assert yoga_at(EXAMPLE_3_SUN, EXAMPLE_3_MOON) == 10


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_rules_endpoint_serves_the_whole_section():
    body = client.get("/v1/yoga/rules").json()
    assert body["section"] == "1.3.9"
    assert body["title"] == "Yogas"
    assert len(body["table_5"]) == 27
    assert body["span_minutes"] == 800
    assert body["count"] == 27
    assert len(body["procedure"]) == 6


def test_rules_warns_that_a_yoga_is_a_sum_not_a_difference():
    body = client.get("/v1/yoga/rules").json()
    assert "sum" in body["uses_sum_not_difference"]
    assert "difference" in body["uses_sum_not_difference"]


def test_a_non_finite_longitude_is_rejected():
    with pytest.raises(InputError):
        yoga(float("nan"), 0.0)
    with pytest.raises(InputError):
        yoga(0.0, float("inf"))


def test_the_result_is_immutable():
    result = yoga(EXAMPLE_3_SUN, EXAMPLE_3_MOON)
    assert isinstance(result, Yoga)
    with pytest.raises(AttributeError):
        result.index = 11  # type: ignore[misc]


# --------------------------------------------------------------------------
# Exercise 4
# --------------------------------------------------------------------------

#: "Moon is at 14°43' in Leo. Sun is at 28°13' in Capricorn."
#: The same pair as Exercise 3 in section 1.3.8.1, which asks for the tithi.
EXERCISE_4_MOON = lon(14, 4, 43)     # 134 deg 43'
EXERCISE_4_SUN = lon(28, 9, 13)      # 298 deg 13'


def test_exercise_4_the_longitudes_from_the_beginning_of_the_zodiac():
    """Leo is the 5th sign and Capricorn the 10th."""
    assert EXERCISE_4_MOON == pytest.approx(134 + 43 / 60)
    assert EXERCISE_4_SUN == pytest.approx(298 + 13 / 60)


def test_exercise_4_step_1_the_sum_and_its_reduction():
    """298°13' + 134°43' = 432°56', and 432°56' - 360° = 72°56'."""
    result = yoga(EXERCISE_4_SUN, EXERCISE_4_MOON)
    assert result.raw_sum == pytest.approx(432 + 56 / 60)
    assert result.total == pytest.approx(72 + 56 / 60)


def test_exercise_4_step_2_the_sum_in_arcminutes_and_the_quotient():
    """72 x 60 + 56 = 4376', and 4376 / 800 = 5.47."""
    result = yoga(EXERCISE_4_SUN, EXERCISE_4_MOON)
    assert result.total_minutes == pytest.approx(4376.0)
    assert result.quotient == pytest.approx(5.47)


def test_exercise_4_step_3_ignoring_the_fraction_gives_five():
    assert yoga(EXERCISE_4_SUN, EXERCISE_4_MOON).completed == 5


def test_exercise_4_is_atiganda_yoga():
    """"Exercise 4: Atiganda yoga."""
    result = yoga(EXERCISE_4_SUN, EXERCISE_4_MOON)
    assert result.index == 6
    assert result.name_book == "Atiganda"
    assert result.meaning == "Great danger"


def test_exercise_4_through_the_service():
    payload = yoga_service.yoga(EXERCISE_4_SUN, EXERCISE_4_MOON)
    assert payload["index"] == 6
    assert payload["name_book"] == "Atiganda"
    assert payload["total_minutes"] == pytest.approx(4376.0)


def test_exercise_4_uses_the_same_pair_as_the_tithi_exercise():
    """Section 1.3.8.1's Exercise 3 asks for the tithi of these very
    longitudes and answers Krishna Dwitiya. Same inputs, different question:
    the tithi takes the difference, the yoga takes the sum. Asserting both
    here would catch a day when one silently starts calling the other.
    """
    from hora.charts.tithi import tithi

    assert tithi(EXERCISE_4_SUN, EXERCISE_4_MOON).full_name == "Krishna Dwitiya"
    assert yoga(EXERCISE_4_SUN, EXERCISE_4_MOON).name_book == "Atiganda"
