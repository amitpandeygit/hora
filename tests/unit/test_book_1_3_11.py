"""Section 1.3.11, Hora — the definitions, the cycle, and the worked example.

Two things in this section are easy to get subtly wrong, and both are pinned
here. The cycle is entered at the **weekday lord**, not at Saturn, so the
speed order alone is not enough. And the section's own worked example treats a
hora as exactly one clock hour, which its first paragraph does not — see
OI-40 and `test_the_section_contradicts_its_own_example`.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.hora import (
    HORA_LORD_CYCLE,
    HORAS_PER_DAY,
    NOMINAL_DAY_HOURS,
    HoraError,
    HoraResult,
    hora,
    hora_index,
    hora_length,
    horas_of_weekday,
    lord_of,
    position_in_cycle,
)
from hora.core import const as c
from hora.core.validate import InputError
from hora.services import hora_service

client = TestClient(app)

#: "Saturn, Jupiter, Mars, Sun, Venus, Mercury and Moon."
SPEED_ORDER = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

#: "Sun for Sunday, Moon for Monday, Mars for Tuesday, Mercury for Wednesday,
#: Jupiter for Thursday, Venus for Friday and Saturn for Saturday."
WEEKDAY_LORDS = [
    ("Sunday", "Sun"), ("Monday", "Moon"), ("Tuesday", "Mars"),
    ("Wednesday", "Mercury"), ("Thursday", "Jupiter"), ("Friday", "Venus"),
    ("Saturday", "Saturn"),
]


# --------------------------------------------------------------------------
# The definitions
# --------------------------------------------------------------------------


def test_the_day_runs_sunrise_to_sunrise_in_twenty_four_parts():
    """"Each day starts at sunrise and ends at next day's sunrise. This period
    is divided into 24 equal parts and they are called horas."""
    assert HORAS_PER_DAY == 24
    assert hora_length(24.0) == 1.0
    assert hora_length(23.5) == pytest.approx(23.5 / 24)


def test_a_hora_is_almost_but_not_exactly_an_hour():
    """"A hora is almost equal to an hour."

    On a real day the sunrise-to-sunrise interval is not 24 hours, so the hora
    is not 60 minutes. The word is "almost".
    """
    assert hora_length(24.6) != 1.0
    assert hora_length(24.6) == pytest.approx(1.025)


def test_the_lords_run_in_order_of_decreasing_speed():
    """"The lords of hora come in the order of decreasing speed with respect
    to earth: Saturn, Jupiter, Mars, Sun, Venus, Mercury and Moon."""
    assert [c.GRAHA_NAMES[g] for g in c.HORA_LORD_ORDER] == SPEED_ORDER


def test_after_moon_we_go_back_to_saturn():
    """"After Moon, we go back to Saturn and repeat the 7 planets."""
    assert HORA_LORD_CYCLE == 7
    # Saturday's first hora is Saturn, so its 8th is Saturn again.
    saturday = horas_of_weekday(6)
    assert c.GRAHA_NAMES[saturday[0]] == "Saturn"
    assert c.GRAHA_NAMES[saturday[7]] == "Saturn"
    assert c.GRAHA_NAMES[saturday[6]] == "Moon", "the 7th, just before the wrap"


@pytest.mark.parametrize("weekday,name,lord", [
    (i, n, g) for i, (n, g) in enumerate(WEEKDAY_LORDS)
])
def test_the_first_hora_belongs_to_the_lord_of_the_weekday(weekday, name, lord):
    """"The first hora of any day ... is ruled by the lord of the weekday
    (Sun for Sunday, Moon for Monday, ...)."""
    assert c.VAARA_NAMES[weekday] == name
    assert c.GRAHA_NAMES[lord_of(weekday, 1)] == lord
    assert c.GRAHA_NAMES[c.VAARA_LORD[weekday]] == lord


def test_the_cycle_is_entered_at_the_weekday_lord_not_at_saturn():
    """"After that, we list planets in the order mentioned above."

    Starting every day at Saturn would make all seven days identical. Sunday's
    second hora is Venus — the planet after Sun in the speed order.
    """
    assert c.GRAHA_NAMES[lord_of(0, 2)] == "Venus"
    assert c.GRAHA_NAMES[lord_of(1, 2)] == "Saturn", "after Moon comes Saturn"
    assert len({tuple(horas_of_weekday(w)) for w in range(7)}) == 7


def test_the_lord_sequence_of_a_day_follows_the_speed_order():
    """Whatever the weekday, consecutive horas step through SPEED_ORDER."""
    for weekday in range(7):
        lords = [c.GRAHA_NAMES[g] for g in horas_of_weekday(weekday)]
        start = SPEED_ORDER.index(lords[0])
        assert lords == [SPEED_ORDER[(start + i) % 7] for i in range(24)]


def test_position_in_cycle_never_returns_zero():
    """"After subtracting multiples of 7 from 16, we get 2."

    Subtracting multiples of 7 from 7 leaves 7, not 0 — the book counts the
    7th planet, not the 0th.
    """
    assert position_in_cycle(7) == 7
    assert position_in_cycle(14) == 7
    assert position_in_cycle(1) == 1
    assert position_in_cycle(16) == 2
    assert all(1 <= position_in_cycle(i) <= 7 for i in range(1, 25))


def test_the_twenty_fifth_hora_would_be_the_next_day():
    with pytest.raises(InputError):
        lord_of(0, 25)
    with pytest.raises(InputError):
        lord_of(7, 1)


# --------------------------------------------------------------------------
# The worked example
# --------------------------------------------------------------------------

#: "let us take 9:40 pm on a Wednesday on which sunrise was at 6:10 am"
WEDNESDAY = 3
EXAMPLE_ELAPSED = (21 + 40 / 60) - (6 + 10 / 60)


def test_example_the_elapsed_time_since_sunrise():
    """"The time elapsed since sunrise is 21:40 - 6:10 = 15:30."""
    assert EXAMPLE_ELAPSED == pytest.approx(15.5)


def test_example_the_sixteenth_hour_since_sunrise_was_running():
    """"So the 16th hour since sunrise was running then."""
    assert hora_index(EXAMPLE_ELAPSED) == 16


def test_example_it_is_the_sixteenth_planet_from_mercury():
    """"This is ruled by the 16th planet from Mercury."

    Wednesday, so the weekday lord is Mercury.
    """
    result = hora(WEDNESDAY, EXAMPLE_ELAPSED)
    assert result.weekday_name == "Wednesday"
    assert result.weekday_lord_name == "Mercury"
    assert result.index == 16


def test_example_subtracting_multiples_of_seven_gives_two():
    """"After subtracting multiples of 7 from 16, we get 2."""
    assert hora(WEDNESDAY, EXAMPLE_ELAPSED).position_in_cycle == 2


def test_example_the_second_planet_from_mercury_is_moon():
    """"From the list given above, we see that the 2nd planet from Mercury is
    Moon. So Moon's hora runs at 9:40 pm."""
    assert hora(WEDNESDAY, EXAMPLE_ELAPSED).lord_name == "Moon"


def test_example_reports_all_five_steps():
    result = hora(WEDNESDAY, EXAMPLE_ELAPSED)
    assert [s.number for s in result.steps] == [1, 2, 3, 4, 5]
    assert all(s.description and s.detail for s in result.steps)
    assert "16th" in result.steps[1].detail
    assert "2nd planet from Mercury is Moon" in result.steps[4].detail


def test_example_through_the_service_and_the_endpoint():
    payload = hora_service.hora(WEDNESDAY, EXAMPLE_ELAPSED)
    assert payload["lord_name"] == "Moon"
    body = client.post(
        "/v1/hora/compute",
        json={"weekday": WEDNESDAY, "elapsed_hours": EXAMPLE_ELAPSED},
    ).json()
    assert body["lord_name"] == "Moon"
    assert body["index"] == 16
    assert body["position_in_cycle"] == 2


def test_example_agrees_with_the_panchanga_implementation():
    """`panchanga.hora.hora_lord` predates this module."""
    from hora.panchanga.hora import hora_lord

    assert c.GRAHA_NAMES[hora_lord(WEDNESDAY, 16)] == "Moon"
    for weekday in range(7):
        for index in range(1, 25):
            assert hora_lord(weekday, index) == lord_of(weekday, index)


def test_the_section_contradicts_its_own_example():
    """The first paragraph divides the actual sunrise-to-sunrise interval into
    24; the example reads the 16th hora off a 15:30 clock elapsed, which only
    works if a hora is exactly one hour.

    On a 24h36m day the same instant falls in the 16th hora still, but on a
    23h30m day it is the 16th too — while at 15:30 of a 25-hour day it is the
    15th. The two readings are not interchangeable, so both are supported and
    neither is silently chosen. See OI-40.
    """
    assert hora(WEDNESDAY, 15.5, 24.0).index == 16
    assert hora(WEDNESDAY, 15.5, 25.0).index == 15
    assert hora(WEDNESDAY, 15.5, 25.0).lord_name != "Moon"
    assert NOMINAL_DAY_HOURS == 24.0, "the default reproduces the example"


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_day_endpoint_lists_all_twenty_four():
    body = client.get("/v1/hora/day/3").json()
    assert body["weekday_name"] == "Wednesday"
    assert len(body["horas"]) == 24
    assert body["horas"][0]["lord_name"] == "Mercury"
    assert body["horas"][15]["lord_name"] == "Moon", "the 16th"


def test_day_endpoint_rejects_an_eighth_weekday():
    assert client.get("/v1/hora/day/7").status_code == 422


def test_rules_endpoint_serves_the_whole_section():
    body = client.get("/v1/hora/rules").json()
    assert body["section"] == "1.3.11"
    assert [s["name"] for s in body["speed_order"]] == SPEED_ORDER
    assert [(w["weekday_name"], w["lord_name"]) for w in body["weekday_lords"]] == (
        WEEKDAY_LORDS
    )
    assert body["horas_per_day"] == 24
    assert "OI-40" in body["day_length_note"]


def test_an_elapsed_time_past_the_end_of_the_day_is_rejected():
    with pytest.raises(HoraError):
        hora(0, 24.0)
    assert client.post(
        "/v1/hora/compute", json={"weekday": 0, "elapsed_hours": 25.0}
    ).status_code == 400


def test_a_negative_elapsed_time_is_rejected():
    with pytest.raises(InputError):
        hora(0, -0.5)


def test_sunrise_itself_is_the_first_hora():
    assert hora(0, 0.0).index == 1
    assert hora(0, 0.0).lord_name == "Sun"


def test_the_result_is_immutable():
    result = hora(WEDNESDAY, EXAMPLE_ELAPSED)
    assert isinstance(result, HoraResult)
    with pytest.raises(AttributeError):
        result.index = 1  # type: ignore[misc]
