"""Chapter 31 — Sudarsana Chakra dasa. §31.1, Chart 72 and §31.2."""

import pytest

from hora.charts.chart import Place, compute_chart
from hora.core.const import RASI_ABBR, Graha
from hora.core.settings import NodeType, Settings
from hora.core.timeutil import from_local
from hora.dasha import sudarsana

_PLACE = Place(name="SC Example", latitude=21 + 27 / 60,
               longitude=83 + 58 / 60)
_SETTINGS = Settings(node_type=NodeType.MEAN)
_PRINTED = from_local(1963, 8, 7, 21, 14, 0.0, utc_offset_hours=5.5)
_SOLVED = from_local(1963, 8, 7, 21, 14, 48.0, utc_offset_hours=5.5)


def _chart(instant=_SOLVED):
    return compute_chart(instant, _PLACE, _SETTINGS)


def _rasis(chart):
    return {g: int(chart.positions[g].longitude // 30) for g in range(9)}


# --------------------------------------------------------------------------
# §31.1 Introduction
# --------------------------------------------------------------------------


def test_the_introduction_is_transcribed():
    assert sudarsana.CHAPTER_TITLE == "Sudarsana Chakra Dasa"
    assert "taught by Brahma" in sudarsana.INTRODUCTION
    assert "daily, monthly and annual fortune" in sudarsana.INTRODUCTION
    assert "rather than the part on \"Dasa Analysis\"" in sudarsana.INTRODUCTION
    assert "this is a dasa applicable to natal charts" in sudarsana.INTRODUCTION


def test_the_chapter_explains_its_own_placement():
    """It says why a natal dasa sits in the Tajaka part, then says twice that
    it is natal.
    """
    text = sudarsana.INTRODUCTION
    assert text.count("natal") >= 2
    assert "Tajaka annual, monthly and sixty-hour charts" in text
    assert "No other chapter explains" in (
        sudarsana.THE_CHAPTER_EXPLAINS_ITS_OWN_PLACEMENT)


def test_the_three_peers_are_one_from_each_family():
    from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

    assert sudarsana.NAMED_ALONGSIDE == (
        "Vimsottari dasa", "Narayana dasa", "Kalachakra dasa")
    assert "vimshottari" in NAKSHATRA_DASHA_SYSTEMS       # a nakshatra dasa
    from hora.dasha.rasi import narayana  # a rasi dasa

    assert callable(narayana.dasa_length)
    from hora.dasha.nakshatra import kalachakra  # neither

    assert kalachakra is not None
    assert "a fourth kind" in sudarsana.THE_THREE_PEERS_ARE_ONE_FROM_EACH_FAMILY


# --------------------------------------------------------------------------
# Chart 72
# --------------------------------------------------------------------------


def test_chart_72_is_the_only_nativity_in_part_4():
    from hora.charts.book import chart

    record = chart(72)
    assert record["title"] == "SC Example"
    assert record["birth"] == "August 7, 1963, 9:14 pm (IST), 83 E 58, 21 N 27"
    assert record["retrograde"] == ("Sat",)
    for annual in (66, 67, 68, 69, 70, 71):
        assert "annual chart" in chart(annual)["note"]
    assert "nativity rather than an annual chart" in record["note"]


def test_every_graha_reproduces_from_the_printed_minute():
    """Nine of the ten printed longitudes are inside an arcminute at 9:14:00.
    """
    from hora.charts.book import longitudes

    chart = _chart(_PRINTED)
    printed = longitudes(72)
    ids = {"Sun": 0, "Moon": 1, "Mars": 2, "Merc": 3, "Jup": 4, "Ven": 5,
           "Sat": 6, "Rahu": 7, "Ketu": 8}
    for name, index in ids.items():
        gap = abs(((chart.positions[index].longitude - printed[name] + 180)
                    % 360) - 180) * 60
        assert gap < 1.0, (name, gap)


def test_the_ascendant_needs_forty_eight_seconds():
    """It moves 19.7 arcminutes a clock minute here, so the printed minute
    cannot pin it closer than about ten.
    """
    from hora.charts.book import longitudes

    printed = longitudes(72)["Asc"]
    at_zero = _chart(_PRINTED).lagna_longitude
    at_solved = _chart(_SOLVED).lagna_longitude

    assert (at_zero - printed) * 60 == pytest.approx(-15.8, abs=0.1)
    assert abs(at_solved - printed) * 60 < 0.05

    a_minute_later = compute_chart(
        from_local(1963, 8, 7, 21, 15, 0.0, utc_offset_hours=5.5),
        _PLACE, _SETTINGS).lagna_longitude
    rate = (a_minute_later - at_zero) * 60
    assert rate == pytest.approx(19.7, abs=0.1)
    assert 15.8 / rate * 60 == pytest.approx(48, abs=1)

    # And every graha is still inside an arcminute at the solved instant.
    chart = _chart(_SOLVED)
    for index in range(9):
        gap = abs(((chart.positions[index].longitude
                     - longitudes(72)[["Sun", "Moon", "Mars", "Merc", "Jup",
                                       "Ven", "Sat", "Rahu", "Ketu"][index]]
                     + 180) % 360) - 180) * 60
        assert gap < 1.0
    assert "19.7 arcminutes a clock minute" in (
        sudarsana.THE_ASCENDANT_NEEDS_FORTY_EIGHT_SECONDS)


def test_the_drawn_diagram_agrees_with_the_longitudes():
    from hora.charts.book import chart, signs

    found = signs(72)
    for body, rasi in chart(72)["drawn"].items():
        if body == "AL":
            continue
        assert RASI_ABBR[found[body]] == rasi, body


# --------------------------------------------------------------------------
# §31.2 Sudarsana Chakra
# --------------------------------------------------------------------------


def test_the_three_references_are_transcribed():
    assert "Lagna represents the physical body" in sudarsana.THE_THREE_REFERENCES
    assert "Moon represents the mind" in sudarsana.THE_THREE_REFERENCES
    assert "Sun represents the soul" in sudarsana.THE_THREE_REFERENCES
    assert "all the three references are important" in (
        sudarsana.THE_THREE_REFERENCES)
    assert "3 concentric circles" in sudarsana.THE_THREE_CIRCLES

    rows = sudarsana.SUDARSANA_REFERENCES
    assert [row["reference"] for row in rows] == ["lagna", "Moon", "Sun"]
    assert [row["stands_for"] for row in rows] == [
        "the physical body", "the mind", "the soul"]
    assert [row["circle"] for row in rows] == ["inner", "middle", "outer"]


def test_the_chakra_has_three_circles_of_twelve_houses():
    chart = _chart()
    got = sudarsana.sudarsana_chakra(
        lagna_rasi=chart.lagna_rasi,
        moon_rasi=int(chart.positions[1].longitude // 30),
        sun_rasi=int(chart.positions[0].longitude // 30),
        graha_rasis=_rasis(chart))
    assert got["order"] == ("lagna", "Moon", "Sun")
    for name in got["order"]:
        circle = got["circles"][name]
        assert len(circle["houses"]) == 12
        assert [h["house"] for h in circle["houses"]] == list(range(1, 13))
        # every rasi appears exactly once in each circle
        assert len({h["rasi"] for h in circle["houses"]}) == 12
        assert circle["houses"][0]["rasi"] == circle["rasi"]


def test_the_tenth_house_reading_reproduces():
    """Sg with Ketu from the lagna, Sc empty from the Moon, Ar empty from the
    Sun.
    """
    chart = _chart()
    got = sudarsana.sudarsana_chakra(
        lagna_rasi=chart.lagna_rasi,
        moon_rasi=int(chart.positions[1].longitude // 30),
        sun_rasi=int(chart.positions[0].longitude // 30),
        graha_rasis=_rasis(chart))
    tenth = sudarsana.the_same_house_everywhere(got, 10)
    assert [RASI_ABBR[row["rasi"]] for row in tenth] == ["Sg", "Sc", "Ar"]
    assert tenth[0]["graha_names"] == ("Ketu",)
    assert tenth[0]["empty"] is False
    assert tenth[1]["empty"] is True
    assert tenth[2]["empty"] is True
    assert "exactly as section 31.2 reads them" in (
        sudarsana.THE_TENTH_HOUSE_READING_REPRODUCES)


def test_empty_means_no_graha_and_a_node_counts():
    """Scorpio holds GL and HL and is called empty; Sagittarius holds Ketu and
    AL and is said to have Ketu.
    """
    from hora.charts.book import chart as record
    from hora.charts.book import signs

    found = signs(72)
    assert RASI_ABBR[found["GL"]] == RASI_ABBR[found["HL"]] == "Sc"
    assert RASI_ABBR[found["Ketu"]] == "Sg"
    assert record(72)["drawn"]["AL"] == "Sg"
    assert "The 10th house from Moon is Sc and it is empty" in (
        sudarsana.THE_TENTH_FROM_ALL_THREE)
    assert "in Sg and it has Ketu" in sudarsana.THE_TENTH_FROM_ALL_THREE
    assert "the nodes are" in sudarsana.EMPTY_MEANS_NO_GRAHA_AND_A_NODE_COUNTS


def test_house_from_walks_the_zodiac():
    for reference in range(12):
        assert sudarsana.house_from(reference, 1) == reference
        assert sudarsana.house_from(reference, 12) == (reference + 11) % 12
        assert {sudarsana.house_from(reference, h)
                for h in range(1, 13)} == set(range(12))


def test_the_three_circles_differ_unless_the_references_coincide():
    """Chart 72's lagna, Moon and Sun are in three different rasis, so the
    same house means three different rasis.
    """
    chart = _chart()
    seats = {chart.lagna_rasi,
             int(chart.positions[1].longitude // 30),
             int(chart.positions[0].longitude // 30)}
    assert len(seats) == 3
    got = sudarsana.sudarsana_chakra(
        lagna_rasi=chart.lagna_rasi,
        moon_rasi=int(chart.positions[1].longitude // 30),
        sun_rasi=int(chart.positions[0].longitude // 30),
        graha_rasis=_rasis(chart))
    for house in range(1, 13):
        rasis = {row["rasi"]
                 for row in sudarsana.the_same_house_everywhere(got, house)}
        assert len(rasis) == 3, house


def test_the_chakra_rejects_bad_input():
    with pytest.raises(sudarsana.SudarsanaError, match="unknown graha"):
        sudarsana.sudarsana_chakra(lagna_rasi=0, moon_rasi=1, sun_rasi=2,
                                   graha_rasis={99: 0})
    for bad in ({"lagna_rasi": 12}, {"moon_rasi": -1}, {"sun_rasi": 12}):
        kwargs = {"lagna_rasi": 0, "moon_rasi": 1, "sun_rasi": 2, **bad}
        with pytest.raises(Exception, match="rasi"):
            sudarsana.sudarsana_chakra(**kwargs)


def test_the_section_levels_the_three_references():
    assert "Though we typically give importance to lagna" in (
        sudarsana.THE_THREE_REFERENCES)
    assert "judged together rather than the lagna" in (
        sudarsana.THE_SECTION_LEVELS_THE_THREE_REFERENCES)
    assert int(Graha.SUN) == 0 and int(Graha.MOON) == 1
