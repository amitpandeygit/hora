"""Section 1.3.10, Karanas — all four statements.

The section is four sentences and every one is load-bearing. The trap is the
last: the four once-only karanas **wrap the month boundary**, so slot 1 (the
first half of the first tithi) carries Kimstughna, the *eleventh* name. Read
naively — first slot gets the first name — every repeating karana shifts by
one and the arithmetic still looks plausible.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.karana import (
    FIRST_ONCE_ONLY_SLOT,
    FIRST_REPEATING_SLOT,
    KARANA_COUNT,
    KARANA_SLOTS,
    KARANA_SPAN,
    KARANAS_PER_TITHI,
    ONCE_ONLY_COUNT,
    REPEATING_COUNT,
    REPETITIONS,
    Karana,
    index_of_slot,
    karana,
    karana_at,
    slot_from_elongation,
    slot_of,
    slots_of_index,
)
from hora.core import const as c
from hora.core.validate import InputError
from hora.services import karana_service

client = TestClient(app)

#: "There are 11 karanas: (1) Bava, (2) Balava, (3) Kaulava, (4) Taitula,
#: (5) Garija, (6) Vanija, (7) Vishti, (8) Sakuna, (9) Chatushpada,
#: (10) Naga, and, (11) Kimstughna."
ELEVEN = [
    "Bava", "Balava", "Kaulava", "Taitula", "Garija", "Vanija", "Vishti",
    "Sakuna", "Chatushpada", "Naga", "Kimstughna",
]


def test_each_tithi_is_divided_into_two_karanas():
    """"Each tithi is divided into 2 karanas."""
    assert KARANAS_PER_TITHI == 2
    assert KARANA_SLOTS == 30 * KARANAS_PER_TITHI == 60
    assert KARANA_SPAN * 2 == 12.0, "half a tithi's 12 degrees"


def test_there_are_eleven_karanas_named_in_this_order():
    """The list is transcribed, index for index."""
    assert KARANA_COUNT == 11
    assert list(c.KARANA_NAMES_BOOK) == ELEVEN


@pytest.mark.parametrize("index,name", list(enumerate(ELEVEN, start=1)))
def test_each_karana_name_by_index(index, name):
    assert c.KARANA_NAMES_BOOK[index - 1] == name


def test_the_first_seven_repeat_eight_times():
    """"The first 7 karanas repeat 8 times starting from the 2nd half of the
    first lunar day of a month."""
    assert REPEATING_COUNT == 7
    assert REPETITIONS == 8
    for index in range(1, REPEATING_COUNT + 1):
        assert len(slots_of_index(index)) == REPETITIONS, ELEVEN[index - 1]


def test_the_repeating_run_starts_at_the_second_half_of_the_first_tithi():
    assert FIRST_REPEATING_SLOT == slot_of(1, 2) == 2
    assert karana(slot_of(1, 2)).name_book == "Bava"


def test_the_last_four_come_just_once():
    """"The last 4 karanas come just once in a month."""
    assert ONCE_ONLY_COUNT == 4
    for index in range(REPEATING_COUNT + 1, KARANA_COUNT + 1):
        assert len(slots_of_index(index)) == 1, ELEVEN[index - 1]


def test_the_once_only_run_starts_at_the_second_half_of_the_twenty_ninth():
    """"...starting from the 2nd half of the 29th lunar day..."""
    assert FIRST_ONCE_ONLY_SLOT == slot_of(29, 2) == 58
    assert karana(slot_of(29, 2)).name_book == "Sakuna"


def test_the_once_only_run_ends_at_the_first_half_of_the_first():
    """"...and ending at the 1st half of the first lunar day."

    This is the wrap. Slot 1 is the *last* of the eleven names, not the first.
    """
    assert karana(slot_of(1, 1)).name_book == "Kimstughna"
    assert karana(slot_of(1, 1)).index == KARANA_COUNT == 11


def test_the_four_once_only_karanas_are_consecutive_across_the_boundary():
    """Sakuna, Chatushpada, Naga close the month; Kimstughna opens the next."""
    assert [karana(s).name_book for s in (58, 59, 60, 1)] == [
        "Sakuna", "Chatushpada", "Naga", "Kimstughna",
    ]


def test_the_two_rules_account_for_every_slot():
    """7 x 8 = 56 repeating, plus 4 once-only, is exactly 60."""
    assert REPEATING_COUNT * REPETITIONS + ONCE_ONLY_COUNT == KARANA_SLOTS
    counts = {i: len(slots_of_index(i)) for i in range(1, KARANA_COUNT + 1)}
    assert sum(counts.values()) == KARANA_SLOTS
    assert set(range(1, KARANA_SLOTS + 1)) == {
        s for i in range(1, KARANA_COUNT + 1) for s in slots_of_index(i)
    }


def test_the_repeating_seven_run_in_order_without_a_gap():
    """Slots 2 to 57 are the seven names, eight times over, in order."""
    run = [index_of_slot(s) for s in range(2, 58)]
    assert run == [((i) % 7) + 1 for i in range(56)]
    assert len(run) == REPEATING_COUNT * REPETITIONS


def test_slot_to_tithi_and_half():
    assert (karana(1).tithi, karana(1).half) == (1, 1)
    assert (karana(2).tithi, karana(2).half) == (1, 2)
    assert (karana(60).tithi, karana(60).half) == (30, 2)


def test_the_karana_follows_the_same_elongation_as_the_tithi():
    """A karana is half a tithi, so it divides Moon minus Sun by 6."""
    assert slot_from_elongation(0.0) == 1
    assert slot_from_elongation(6.0) == 2
    assert slot_from_elongation(359.999) == 60


@pytest.mark.parametrize("k", range(60))
def test_every_karana_boundary_starts_its_own_slot(k):
    """The same boundary discipline as yogas. This divisor is exact, but the
    property is asserted rather than assumed."""
    assert slot_from_elongation(k * KARANA_SPAN) == k + 1


def test_karana_at_longitudes_matches_the_slot():
    """Example 2's pair from §1.3.8.1 is the 19th tithi, so slots 37 and 38."""
    result = karana_at(227 + 46 / 60, 84 + 12 / 60)
    assert result.tithi == 19
    assert result.slot in (37, 38)


def test_this_agrees_with_the_mapping_panchanga_already_used():
    """`panchanga.core._karana_slot` predates this module. If the two ever
    disagree, one of them is wrong and /v1/panchanga would drift silently."""
    from hora.panchanga.core import _karana_slot

    for slot in range(1, KARANA_SLOTS + 1):
        assert index_of_slot(slot) - 1 == _karana_slot(slot - 1), slot


def test_out_of_range_inputs_are_rejected():
    for bad in (0, 61, -1):
        with pytest.raises(InputError):
            karana(bad)
    with pytest.raises(InputError):
        slot_of(31, 1)
    with pytest.raises(InputError):
        slot_of(1, 3)
    with pytest.raises(InputError):
        slots_of_index(12)


def test_the_result_is_immutable():
    result = karana(1)
    assert isinstance(result, Karana)
    with pytest.raises(AttributeError):
        result.name_book = "Bava"  # type: ignore[misc]


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_compute_by_slot():
    body = client.post("/v1/karana/compute", json={"slot": 58}).json()
    assert body["name_book"] == "Sakuna"
    assert body["repeats"] is False
    assert body["occurrences"] == 1


def test_compute_by_tithi_and_half():
    body = client.post("/v1/karana/compute", json={"tithi": 1, "half": 1}).json()
    assert body["name_book"] == "Kimstughna"


def test_compute_needs_a_complete_input():
    assert client.post("/v1/karana/compute", json={"tithi": 1}).status_code == 400
    assert client.post("/v1/karana/compute", json={}).status_code == 400


def test_at_longitudes_endpoint():
    body = client.post(
        "/v1/karana/at",
        json={"sun_longitude": 227.76666666666668, "moon_longitude": 84.2},
    ).json()
    assert body["tithi"] == 19


def test_rules_endpoint_serves_the_whole_section():
    body = client.get("/v1/karana/rules").json()
    assert body["section"] == "1.3.10"
    assert len(body["karanas"]) == 11
    assert body["repetitions"] == 8
    assert body["first_once_only_slot"] == 58
    assert [k["name"] for k in body["karanas"]] == ELEVEN


def test_rules_publishes_every_slot_each_karana_falls_on():
    body = client.get("/v1/karana/rules").json()
    rows = {k["name"]: k["slots"] for k in body["karanas"]}
    assert rows["Kimstughna"] == [1]
    assert rows["Bava"][0] == 2
    assert len(rows["Bava"]) == 8


def test_service_and_engine_agree():
    assert karana_service.for_slot(58)["name_book"] == karana(58).name_book
    assert karana_service.for_tithi_half(29, 2)["slot"] == 58
