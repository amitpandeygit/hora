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


# --------------------------------------------------------------------------
# §31.3 Dasa Computation
# --------------------------------------------------------------------------


def _chakra():
    chart = _chart()
    return sudarsana.sudarsana_chakra(
        lagna_rasi=chart.lagna_rasi,
        moon_rasi=int(chart.positions[1].longitude // 30),
        sun_rasi=int(chart.positions[0].longitude // 30),
        graha_rasis=_rasis(chart))


def test_the_dasa_computation_is_transcribed():
    assert "Each dasa is for one year" in sudarsana.THE_CYCLE_OF_TWELVE
    assert "return in the 13th year" in sudarsana.THE_CYCLE_OF_TWELVE
    assert "One year stands for a solar year here" in (
        sudarsana.THE_YEAR_AND_THE_REMAINDER)
    assert "if the remainder is zero, make it 12" in (
        sudarsana.THE_YEAR_AND_THE_REMAINDER)
    assert "Sc, Li and Pi" in sudarsana.THE_HOUSE_IS_READ_FROM_ALL_THREE
    assert "only an approximation" in sudarsana.THE_HOUSE_IS_READ_FROM_ALL_THREE
    assert "Sc, Sg, Cp, Aq etc" in sudarsana.ANTARDASA_RULE
    assert sudarsana.FIGURE_4_TITLE == "Sudarsana Chakra"


def test_the_house_is_the_year_modulo_twelve():
    assert sudarsana.dasa_house(1) == 1
    assert sudarsana.dasa_house(12) == 12
    assert sudarsana.dasa_house(13) == 1                 # returns in the 13th
    assert sudarsana.dasa_house(14) == 2
    assert sudarsana.dasa_house(24) == 12                # remainder zero
    assert sudarsana.dasa_house(45) == 9                 # the worked case
    for year in range(1, 121):
        assert sudarsana.dasa_house(year) == sudarsana.dasa_house(year + 12)


def test_the_forty_fifth_year_reproduces():
    want = sudarsana.THE_FORTY_FIFTH_YEAR
    assert want["completed"] + 1 == want["year"] == 45
    got = sudarsana.dasa_signs(lagna_rasi=RASI_ABBR.index("Pi"),
                               moon_rasi=RASI_ABBR.index("Aq"),
                               sun_rasi=RASI_ABBR.index("Cn"), year=45)
    assert got["house"] == want["house"] == 9
    assert {name: RASI_ABBR[rasi]
            for name, rasi in got["signs"].items()} == want["signs"]

    antardasas = sudarsana.antardasa_signs(got["signs"]["lagna"])
    assert tuple(RASI_ABBR[r] for r in antardasas[:4]) == (
        want["antardasas_from_lagna"])
    assert len(antardasas) == 12
    assert len(set(antardasas)) == 12


def test_figure_4_reproduces_ring_for_ring():
    """Chart 72's chakra: the inner ring runs from Pisces, the middle from
    Aquarius and the outer from Cancer.
    """
    got = _chakra()
    rings = {
        "lagna": ["Pi", "Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg",
                  "Cp", "Aq"],
        "Moon": ["Aq", "Pi", "Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc",
                 "Sg", "Cp"],
        "Sun": ["Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi", "Ar",
                "Ta", "Ge"],
    }
    for name, expected in rings.items():
        circle = got["circles"][name]
        assert [RASI_ABBR[h["rasi"]] for h in circle["houses"]] == expected

    # And the figure's own occupants, sector by sector.
    holders = {
        "Pi": ("Jupiter",), "Ge": ("Rahu",), "Aq": ("Moon",),
        "Cn": ("Sun", "Venus"), "Cp": ("Saturn",), "Le": ("Mercury",),
        "Sg": ("Ketu",), "Vi": ("Mars",),
    }
    for name in got["order"]:
        for house in got["circles"][name]["houses"]:
            abbr = RASI_ABBR[house["rasi"]]
            assert set(house["graha_names"]) == set(holders.get(abbr, ())), (
                name, abbr)


def test_the_muntha_is_the_sc_dasa_sign_from_lagna():
    """§28.1's muntha, §30.4's progressed lagna and §31.3's dasa sign from
    lagna are one rasi, in every chart and every year.
    """
    from hora.dasha.annual.varsha_narayana import progressed_lagna
    from hora.tajaka.muntha import muntha_rasi

    for lagna in range(12):
        for year in range(1, 121):
            house = sudarsana.dasa_house(year)
            from_lagna = sudarsana.house_from(lagna, house)
            assert from_lagna == int(muntha_rasi(lagna, year)["rasi"]), (
                lagna, year)
            assert from_lagna == progressed_lagna(lagna, year)["rasi"]
    assert "one rasi under three names" in (
        sudarsana.THE_MUNTHA_IS_THE_SC_DASA_SIGN_FROM_LAGNA)
    assert "always reckoned from lagna" in (
        sudarsana.THE_TAJAKA_CHARTS_ARE_ENTRY_CHARTS)


def test_the_three_chart_types_match_the_three_dasa_levels():
    """A year holds 12 months and a month 12 shashti-horas; a dasa holds 12
    antardasas and an antardasa 12 pratyantardasas.
    """
    from hora.tajaka.monthly import MONTHLY_CHART_RULE
    from hora.tajaka.shashti_hora import SHASHTI_HORA_RULE

    assert "divided into 12 months" in MONTHLY_CHART_RULE.replace(
        "A year is divided into 12 months", "divided into 12 months")
    assert "divided into 12 shashti-horas" in SHASHTI_HORA_RULE
    assert len(sudarsana.antardasa_signs(0)) == 12
    assert len(sudarsana.pratyantardasa_signs(0)) == 12
    assert 12 * 12 == 144
    assert "144 shashti-horas answer 144" in (
        sudarsana.THE_THREE_CHART_TYPES_MATCH_THE_THREE_DASA_LEVELS)
    assert "entry charts" in sudarsana.THE_TAJAKA_CHARTS_ARE_ENTRY_CHARTS


def test_antardasas_and_pratyantardasas_walk_the_zodiac():
    for seat in range(12):
        antardasas = sudarsana.antardasa_signs(seat)
        assert antardasas[0] == seat
        assert set(antardasas) == set(range(12))
        for leg in antardasas:
            pratyantardasas = sudarsana.pratyantardasa_signs(leg)
            assert pratyantardasas[0] == leg
            assert set(pratyantardasas) == set(range(12))


def test_the_simplification_is_labelled_and_then_becomes_the_varga_rule():
    assert "This is only an approximation" in (
        sudarsana.THE_HOUSE_IS_READ_FROM_ALL_THREE)
    assert "We take the strongest of lagna, Moon and Sun" in (
        sudarsana.SC_DASA_IN_A_VARGA)
    assert "one house per year" in sudarsana.SC_DASA_IN_A_VARGA
    assert "no three-sign version is offered" in (
        sudarsana.THE_SIMPLIFICATION_BECOMES_THE_RULE_FOR_VARGAS)


def test_which_reference_is_strongest_is_not_said():
    """OI-180. `dasa_signs` returns all three and picks none."""
    got = sudarsana.dasa_signs(lagna_rasi=11, moon_rasi=10, sun_rasi=3,
                               year=45)
    assert set(got["signs"]) == {"lagna", "Moon", "Sun"}
    assert "strongest" not in got
    assert "gives no test" in sudarsana.WHICH_REFERENCE_IS_STRONGEST_IS_NOT_SAID


def test_chapter_27s_three_charts_find_their_purpose_here():
    from hora.tajaka.monthly import MONTHLY_CHART_RULE
    from hora.tajaka.shashti_hora import SHASHTI_HORA_RULE

    # Neither section says what to read in the chart it casts.
    for rule in (MONTHLY_CHART_RULE, SHASHTI_HORA_RULE):
        assert "antardasa" not in rule.lower()
        assert "dasa" not in rule.lower()
    assert "antardasas and pratyantardasas" in (
        sudarsana.THE_TAJAKA_CHARTS_ARE_ENTRY_CHARTS)
    assert "Section 31.3 says" in (
        sudarsana.CHAPTER_27S_THREE_CHARTS_FIND_THEIR_PURPOSE_HERE)


def test_the_dasa_house_rejects_a_year_outside_a_lifetime():
    for bad in (0, -1, 201):
        with pytest.raises(Exception, match="year"):
            sudarsana.dasa_house(bad)
