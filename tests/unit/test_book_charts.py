"""The register of every chart the book prints.

Charts grew where they were first needed — Chart 6 in chapter 10's tests,
Chart 3 in chapter 12's constants. `core.constants.book_charts` is now the
single register, and the tests here check it against every one of those
fixtures so the two cannot drift apart.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.book import (
    GRAHA_OF,
    BookChartError,
    chart,
    describe,
    divisional,
    graha_signs,
    is_recomputable,
    lagna,
    longitude,
    longitudes,
    numbers,
    recomputable,
    signs,
    unnumbered_chart,
    unnumbered_labels,
)
from hora.core.const import (
    BOOK_CHARTS,
    CHART_3,
    CHART_12,
    CHARTS_NOT_SUPPLIED,
    RASI_ABBR,
)

R = {name: index for index, name in enumerate(RASI_ABBR)}


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_the_register_holds_every_chart_supplied_so_far():
    assert numbers() == (
        1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 36, 37, 38, 39, 40)
    assert CHARTS_NOT_SUPPLIED == (4,)
    assert 4 not in numbers()


def test_asking_for_chart_4_says_it_was_never_printed():
    """Distinguished from a number that is not a chart at all."""
    with pytest.raises(BookChartError, match="never been printed"):
        chart(4)
    with pytest.raises(BookChartError, match="there is no Chart"):
        chart(99)


@pytest.mark.parametrize("number", sorted(BOOK_CHARTS))
def test_every_record_has_a_title_and_parsable_longitudes(number):
    record = chart(number)
    assert record["title"]
    assert record["longitudes"]
    parsed = longitudes(number)
    assert len(parsed) == len(record["longitudes"])
    assert all(0 <= value < 360 for value in parsed.values())


@pytest.mark.parametrize("number", sorted(BOOK_CHARTS))
def test_every_chart_prints_the_nine_grahas(number):
    """Some omit HL, GL or AL; none omits a graha."""
    assert set(GRAHA_OF) <= set(chart(number)["longitudes"])


@pytest.mark.parametrize("number", sorted(BOOK_CHARTS))
def test_every_charts_nodes_are_exactly_opposite(number):
    parsed = longitudes(number)
    assert abs((parsed["Rahu"] - parsed["Ketu"]) % 360 - 180) < 1e-9


@pytest.mark.parametrize("number", sorted(BOOK_CHARTS))
def test_a_drawn_diagram_agrees_with_the_printed_longitudes(number):
    """AL is excluded: it is derived, not a body with a longitude."""
    drawn = chart(number).get("drawn")
    if not drawn:
        pytest.skip("no rasi diagram transcribed for this chart")
    found = signs(number)
    for body, rasi in drawn.items():
        if body == "AL":
            continue
        assert RASI_ABBR[found[body]] == rasi, body


@pytest.mark.parametrize("number", sorted(BOOK_CHARTS))
def test_a_recomputable_chart_has_a_place_and_the_others_say_why(number):
    record = chart(number)
    if is_recomputable(number):
        assert record.get("place")
        assert record.get("birth")
        assert set(record["birth_data"]) == {
            "year", "month", "day", "hour", "minute", "second",
            "utc_offset_hours"}
    else:
        assert record.get("note"), f"Chart {number} must say why not"


def test_the_recomputable_charts_are_the_ones_with_full_birth_lines():
    assert recomputable() == (
        3, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 37, 38, 39,
        40)


# --------------------------------------------------------------------------
# Drift: the register against the fixtures that predate it
# --------------------------------------------------------------------------

def test_the_register_matches_chapter_12s_own_constants():
    assert CHART_3 == chart(3)["longitudes"]
    assert CHART_12 == chart(12)["longitudes"]


@pytest.mark.parametrize("module,constant,number", [
    ("tests.unit.test_book_chapter10", "CHART_5", 5),
    ("tests.unit.test_book_chapter10_argala", "CHART_6", 6),
    ("tests.unit.test_book_chapter10_argala", "CHART_7", 7),
    ("tests.unit.test_book_chapter10_argala", "CHART_8", 8),
    ("tests.unit.test_book_chapter11", "CHART_9", 9),
    ("tests.unit.test_book_chapter11", "CHART_10", 10),
    ("tests.unit.test_book_chapter12", "CHART_11", 11),
])
def test_the_register_matches_the_fixture_that_predates_it(
        module, constant, number):
    """One typo in either place shows up here."""
    import importlib

    fixture = getattr(importlib.import_module(module), constant)
    assert fixture == chart(number)["longitudes"]


def test_charts_6_and_11_are_the_same_native_at_two_times():
    """D-38. Recorded in the register itself so the pair is not mistaken for
    two people."""
    assert "same native as Chart 6" in chart(11)["note"]
    assert "Chart 11 is the same" in chart(6)["note"]
    assert longitudes(6) != longitudes(11), "the two printings do differ"
    assert graha_signs(6) == graha_signs(11), "but no graha changes sign"
    assert signs(6)["GL"] != signs(11)["GL"], "the GL does — Sg against Cp"


# --------------------------------------------------------------------------
# Chart 13
# --------------------------------------------------------------------------

def test_chart_13_is_transcribed():
    record = chart(13)
    assert record["title"] == "Rasi — Swami Chandrasekhara Saraswathi"
    assert record["birth"] == "May 20, 1894, 1:22 pm (IST), 79 E 32, 11 N 57"
    assert record["retrograde"] == ("Sat",)
    assert lagna(13) == R["Le"]


def test_chart_13_recomputes_from_its_own_birth_data():
    """Every graha inside one arcminute."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(13)
    computed = compute_chart(
        from_local(**record["birth_data"]),
        Place(name="Chart 13", **record["place"]),
        Settings(node_type=NodeType.MEAN))
    printed = longitudes(13)
    for name, graha in GRAHA_OF.items():
        error = abs(computed.positions[int(graha)].longitude
                    - printed[name]) * 60
        assert error < 1.0, f"{name}: {error:.2f}'"


def test_chart_13_is_a_sixth_chart_favouring_the_mean_node():
    """OI-68 again. Six charts now, spanning 1542 to 1958."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.const import Graha
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(13)
    printed = longitudes(13)["Rahu"]
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        computed = compute_chart(
            from_local(**record["birth_data"]),
            Place(name="Chart 13", **record["place"]),
            Settings(node_type=node))
        errors[node] = abs(
            computed.positions[int(Graha.RAHU)].longitude - printed) * 60
    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.MEAN] < errors[NodeType.TRUE]


def test_chart_13s_drawn_d20_reproduces_from_our_varga():
    """Thirteen boxes, AL aside. The D-20 is printed beside the rasi chart,
    so it checks the varga as well as the transcription."""
    from hora.charts.vargas import varga

    printed = divisional(13, "D20")
    parsed = longitudes(13)
    for body, rasi in printed.items():
        if body == "AL":
            continue
        assert RASI_ABBR[varga(parsed[body], "D20").sign] == rasi, body


def test_chart_13s_two_arudha_lagnas_are_derived_not_transcribed():
    """The rasi diagram prints AL in Sc and the D-20 prints it in Cn.
    Neither is a longitude, so §9.2 has to produce both."""
    from hora.charts.vargas import varga
    from hora.core.const import RASI_NAMES
    from hora.services import arudha_service

    parsed = longitudes(13)
    for code, printed in (("D1", chart(13)["drawn"]["AL"]),
                          ("D20", divisional(13, "D20")["AL"])):
        lons = {
            int(graha): (parsed[name] if code == "D1"
                         else varga(parsed[name], code).longitude)
            for name, graha in GRAHA_OF.items()
        }
        asc = (parsed["Asc"] if code == "D1"
               else varga(parsed["Asc"], code).longitude)
        pada = arudha_service.one(
            1, int(asc // 30), {k: int(v // 30) for k, v in lons.items()},
            graha_longitudes=lons)
        assert RASI_ABBR[RASI_NAMES.index(pada["sign_name"])] == printed, code


def test_the_longitude_parser_rejects_nonsense():
    assert longitude("23 Le 10") == R["Le"] * 30 + 23 + 10 / 60
    for bad in ("23 Zz 10", "Leo", "23 10"):
        with pytest.raises(BookChartError, match="printed longitude"):
            longitude(bad)


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------

def test_the_index_endpoint_lists_every_chart(client):
    body = client.get("/v1/book-charts").json()
    assert len(body["charts"]) == len(numbers())
    assert body["not_supplied"] == [4]
    assert body["recomputable"] == [
        3, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 37, 38, 39,
        40]


def test_the_chart_endpoint_derives_signs_and_lagna(client):
    body = client.get("/v1/book-charts/13").json()
    assert body["lagna"] == "Le"
    assert body["signs"]["Sat"] == "Vi"
    assert body["divisional"]["D20"]["Asc"] == "Pi"
    assert body["recomputable"] is True


def test_the_chart_endpoint_404s_on_chart_4(client):
    response = client.get("/v1/book-charts/4")
    assert response.status_code == 404
    assert "never been printed" in response.json()["error"]["message"]


def test_describe_never_omits_a_key():
    """A caller can rely on the shape even where the book is silent."""
    for number in numbers():
        body = describe(number)
        assert set(body) >= {
            "number", "title", "birth", "place", "recomputable", "longitudes",
            "signs", "lagna", "drawn", "divisional", "chara_karakas",
            "retrograde", "first_seen", "note"}


# --------------------------------------------------------------------------
# Chart 14 — Rajiv Gandhi's rasi and D-3, with Sanjay Gandhi's rasi beside it
# --------------------------------------------------------------------------

def test_chart_14_is_transcribed_with_its_related_chart():
    record = chart(14)
    assert record["title"] == "Rasi and D-3 — Rajiv Gandhi"
    assert lagna(14) == R["Le"]
    assert set(record["related"]) == {"His younger brother"}
    assert record["related"]["His younger brother"]["title"] == (
        "Rasi — Sanjay Gandhi")


def test_chart_14_needs_footnote_37s_seconds_to_reproduce():
    """The chart prints 7:11 am; chapter 11's footnote 37 gives 7:11:40. Only
    the seconds put the ascendant inside an arcminute — 0.8' against 8.6'."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    record = chart(14)
    printed = longitudes(14)
    errors = {}
    for label, second in (("printed", 0.0), ("footnote 37", 40.0)):
        data = dict(record["birth_data"], second=second)
        computed = compute_chart(
            from_local(**data), Place(name="Chart 14", **record["place"]),
            Settings(node_type=NodeType.MEAN))
        errors[label] = abs(computed.lagna_longitude - printed["Asc"]) * 60
        if label == "footnote 37":
            for name, graha in GRAHA_OF.items():
                gap = abs(computed.positions[int(graha)].longitude
                          - printed[name]) * 60
                assert gap < 1.0, f"{name}: {gap:.2f}'"
    assert errors["footnote 37"] < 1.0 < errors["printed"]
    assert "footnote 37" in record["note"]


def test_chart_14s_drawn_d3_reproduces_from_our_varga():
    """Twelve boxes, AL aside — the D-3 is printed beside the rasi chart."""
    from hora.charts.vargas import varga

    printed = divisional(14, "D3")
    parsed = longitudes(14)
    for body, rasi in printed.items():
        if body == "AL":
            continue
        assert RASI_ABBR[varga(parsed[body], "D3").sign] == rasi, body


def test_sanjay_gandhis_chart_is_drawn_only_and_says_so():
    """No longitudes and no birth line are printed for it."""
    related = chart(14)["related"]["His younger brother"]
    assert "longitudes" not in related
    assert "cannot be recomputed" in related["note"]
    assert len(related["drawn"]) == 13


def test_charts_15_and_16_are_the_same_twins_seen_two_ways():
    """Chart 15 prints their D-24, Chart 16 their D-27, from one pair of
    rasi charts. So the two records share longitudes and differ only in the
    divisional printed beside them."""
    assert longitudes(15) == longitudes(16)
    assert set(chart(15)["divisional"]) == {"D24"}
    assert set(chart(16)["divisional"]) == {"D27"}
    for number in (15, 16):
        related = chart(number)["related"]["Shivam Gaur"]
        assert related["birth_data"]["minute"] == 6 + 2


def test_the_second_twin_is_recomputable_unlike_sanjay_gandhi():
    """A related chart may or may not carry its own birth line. Shivam's does;
    Sanjay Gandhi's does not, and each record says which."""
    assert "birth_data" in chart(15)["related"]["Shivam Gaur"]
    assert "birth_data" not in chart(14)["related"]["His younger brother"]


# --------------------------------------------------------------------------
# Charts the book prints inside an example, without a "Chart N".
# --------------------------------------------------------------------------


def test_example_49_chart_is_registered_and_marked_partial():
    """The book gives this native a birth line but never a chart number.

    It prints only the three longitudes its own computation needs, so the
    record must say what is missing rather than read as a whole chart.
    """
    record = unnumbered_chart("Example 49")
    assert record["birth"].startswith("April 4, 1970, 5:50 pm (IST)")
    assert set(record["longitudes"]) == {"Merc", "Jup", "Ven"}
    assert record["stated"]["moon_constellation"] == 25
    assert record["stated"]["lagna_rasi"] == "Vi"
    assert "cannot be drawn" in record["note"]
    with pytest.raises(BookChartError, match="does not supply a chart"):
        unnumbered_chart("Example 48")


def test_example_49_register_agrees_with_the_chapter_15_fixture():
    """The register and the worked-example test must not drift apart.

    Both encode the same three longitudes. If either is edited alone, the
    section 15.4.4 answers and the register stop describing one native.
    """
    from tests.unit.test_book_chapter15_avastha import lon

    registered = unnumbered_chart("Example 49")["longitudes"]
    assert longitude(registered["Merc"]) == pytest.approx(lon(3 + 8 / 60, "Ar"))
    assert longitude(registered["Jup"]) == pytest.approx(lon(9 + 46 / 60, "Li"))
    assert longitude(registered["Ven"]) == pytest.approx(lon(7 + 55 / 60, "Ar"))


def test_exercise_24_is_registered_as_a_chart_with_no_positions():
    """The book prints birth data and nothing else for this native.

    Registering it with an empty `longitudes` is the point: the record exists
    so the birth data is not re-keyed by hand, and its emptiness says the
    answers rest on our ephemeris rather than on the book's numbers.
    """
    record = unnumbered_chart("Exercise 24")
    assert record["longitudes"] == {}
    assert record["birth"].endswith("8:30 am (LMT), 67 E 03, 24 N 52")
    assert "check on the ephemeris" in record["note"]


def test_a_label_is_needed_because_example_and_exercise_numbers_collide():
    """Example 24 and Exercise 24 would be different natives under one key."""
    labels = unnumbered_labels()
    assert "Exercise 24" in labels
    assert "Example 24" not in labels          # a different, unseen native
    assert all(l.split()[0] in {"Example", "Exercise"} for l in labels)


def test_exercise_24_register_agrees_with_the_chapter_15_fixture():
    from tests.unit.test_book_chapter15_avastha import EX24_BIRTH, EX24_PLACE

    record = unnumbered_chart("Exercise 24")
    assert record["birth_data"] == EX24_BIRTH
    assert record["place"] == EX24_PLACE
