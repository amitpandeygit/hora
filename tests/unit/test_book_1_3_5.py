"""§1.3.5 Varga chakras (divisional charts) — the vocabulary and the rule.

Most of the section recaps §1.3.2 and §1.3.4. Five statements are not recap,
and one of them is a rule this codebase already relies on: that a divisional
chart is analysed *as an independent chart*, which is why Exercises 12 and 13
take arudhas in D-16 from the D-16 lagna rather than the rasi lagna.
"""

from hora.core import const as c
from hora.services import reference_service

# --------------------------------------------------------------------------
# What a varga chakra is
# --------------------------------------------------------------------------

def test_the_sanskrit_name_and_the_third_name():
    """"divisional charts" (Sanskrit name: varga chakras)" and, later in the
    same sentence, "(or harmonic charts)"."""
    assert c.VARGA_CHAKRA_NAME == "varga chakra"
    assert c.VARGA_ALIASES == ("divisional chart", "harmonic chart")


def test_the_general_definition():
    """"We divide each rasi into n parts and map each part to a rasi again."

    Chapter 6 gives a rule per chart and never restates the thing they all
    are, so this is the only place the general form is stated.
    """
    assert "divide each rasi into n parts" in c.VARGA_DEFINITION
    assert "map each part to a rasi again" in c.VARGA_DEFINITION


def test_the_definition_describes_every_chart_in_the_registry():
    """Each varga divides a rasi into n parts, and n is its divisor."""
    from hora.charts.vargas import VARGA_REGISTRY

    for code, (_fn, _name, divisions) in VARGA_REGISTRY.items():
        assert divisions >= 1, code
        assert code == f"D{divisions}", code


def test_each_chart_signifies_an_area_of_life():
    """"Each divisional chart throws light on a specific area of one's life."

    The premise behind chapter 6's Tables 11 and 20.
    """
    from hora.charts.vargas import VARGA_SIGNIFICATIONS

    assert "specific area of one's life" in c.VARGA_SIGNIFIES_AN_AREA
    assert VARGA_SIGNIFICATIONS, "the per-chart significations this generalises"


# --------------------------------------------------------------------------
# The rule
# --------------------------------------------------------------------------

def test_a_divisional_chart_is_analysed_as_an_independent_chart():
    """"In each divisional chart, we find houses and analyze the chart as if
    it were an independent chart."

    This is what licenses taking the lagna, houses and arudhas of a divisional
    chart from *that chart*. Without it, using the D-16 lagna in Exercises 12
    and 13 would be convention rather than instruction.
    """
    rule = c.VARGA_INDEPENDENT_CHART_RULE
    assert "we find houses" in rule
    assert "as if it were an independent chart" in rule


def test_the_rule_is_what_exercises_12_and_13_rely_on():
    """The behaviour the rule justifies, exercised end to end.

    Houses inside D-16 are counted from the D-16 lagna, and differ from the
    houses the same bodies occupy in the rasi chart.
    """
    from hora.charts.chakra import build
    from hora.charts.vargas import d16_shodasamsa
    from hora.core.const import Graha

    longitudes = {int(g): g * 37.5 + 4.0 for g in range(9)}
    ascendant = 172.68333333333334               # 22 Vi 41

    rasi = build(
        graha_positions=longitudes, lagna=ascendant,
    )
    d16 = build(
        graha_positions={g: d16_shodasamsa(v).sign for g, v in longitudes.items()},
        lagna=d16_shodasamsa(ascendant).sign,
        positions_are_longitudes=False,
    )
    # Each chart has its own lagna, and so its own houses.
    assert rasi.reference_rasi != d16.reference_rasi
    sun = int(Graha.SUN)
    rasi_house = rasi.cell_for_rasi(rasi.bodies[sun].rasi).house
    d16_house = d16.cell_for_rasi(d16.bodies[sun].rasi).house
    assert rasi_house != d16_house


# --------------------------------------------------------------------------
# The four pillars
# --------------------------------------------------------------------------

def test_the_four_pillars_as_section_1_3_5_lists_them():
    """"(1) grahas or planets, (2) rasis or signs, (3) bhavas or houses, and,
    (4) varga chakras or divisional charts"."""
    assert [p["number"] for p in c.FOUR_PILLARS] == [1, 2, 3, 4]
    assert [p["sanskrit"] for p in c.FOUR_PILLARS] == [
        "grahas", "rasis", "bhavas", "varga chakras"
    ]
    assert [p["english"] for p in c.FOUR_PILLARS] == [
        "planets", "signs", "houses", "divisional charts"
    ]


def test_section_6_7_lists_the_same_four_in_a_different_order():
    """D-23. §6.7 has vargas third and bhavas fourth, and then calls
    divisional charts "the third pillar".

    Both orderings are kept so the discrepancy stays visible.
    """
    assert c.FOUR_PILLARS_CONCLUSION_ORDER == (
        "grahas", "rasis", "vargas", "bhavas"
    )
    by_number = {p["number"]: p["sanskrit"] for p in c.FOUR_PILLARS}
    assert by_number[3] == "bhavas", "1.3.5 makes bhavas third"
    assert c.FOUR_PILLARS_CONCLUSION_ORDER[2] == "vargas", "6.7 makes vargas third"


def test_the_two_orderings_name_the_same_four_pillars():
    """The disagreement is about order only, not membership."""
    first = {p["sanskrit"].rstrip("s").replace(" chakra", "")
             for p in c.FOUR_PILLARS}
    second = {name.rstrip("s") for name in c.FOUR_PILLARS_CONCLUSION_ORDER}
    assert first == second == {"graha", "rasi", "bhava", "varga"}


# --------------------------------------------------------------------------
# All of it reaches the API
# --------------------------------------------------------------------------

def test_the_section_is_published():
    terms = reference_service.terms()
    varga = terms["varga"]
    assert varga["sanskrit"] == c.VARGA_CHAKRA_NAME
    assert varga["aliases"] == list(c.VARGA_ALIASES)
    assert varga["definition"] == c.VARGA_DEFINITION
    assert varga["independent_chart_rule"] == c.VARGA_INDEPENDENT_CHART_RULE

    pillars = terms["four_pillars"]
    assert len(pillars["pillars"]) == 4
    assert pillars["conclusion_order"] == list(c.FOUR_PILLARS_CONCLUSION_ORDER)
    assert "D-23" in pillars["ordering_note"]


def test_the_ayana_names_are_published_in_both_values():
    """Not from this section, but found while testing it.

    `AYANA_NAMES` was registered as published and was not published at all.
    The guard passed because "uttara" matched inside the nakshatra names
    "Uttara Phalguni" and "Uttara Ashadha". See OI-35.
    """
    rasis = reference_service.rasi_table()["rasis"]
    assert {row["ayana"] for row in rasis} == {"uttara", "dakshina"}
    grahas = reference_service.graha_table()["grahas"]
    assert {row["strong_in_ayana"] for row in grahas} == {
        "uttara", "dakshina", None
    }
