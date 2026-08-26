"""Chapter 10 — Aspects and Argalas.

Sections 10.1 and 10.2 only: graha drishti. Argalas are later in the chapter
and are not covered here.

Chart 5's twelve navamsa positions are **derived** from the printed rasi
longitudes rather than transcribed, and all twelve match the printed navamsa
diagram. Exercise 14 is then solved from those derived positions, so the
exercise tests the aspect rules and the D-9 mapping together.
"""
import re

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.aspects import (
    graha_aspects_sign,
    graha_drishti_houses,
    rasi_drishti,
)
from hora.charts.vargas import d9_navamsa
from hora.core.const import (
    ASPECT_DEFINITION,
    ASPECT_KINDS,
    ASPECTED_PLANET_EXAMPLE,
    ASPECTED_PLANET_RULE,
    ASPECTS_ARE_A_SKILL_NOTE,
    DRISHTI_MEANS,
    GRAHA_DRISHTI_HEADING_AS_PRINTED,
    SEVENTH_HOUSE_EXAMPLES,
    SEVENTH_HOUSE_RULE,
    SPECIAL_ASPECT_BULLETS,
    SPECIAL_ASPECT_GRAHAS,
    SPECIAL_ASPECT_RULE,
    Graha,
)
from hora.services import aspect_service

RASI_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
R = {name: index for index, name in enumerate(RASI_ABBR)}


@pytest.fixture
def client():
    return TestClient(app)


def lon(text: str) -> float:
    """Parse the book's "5 Li 23" notation into a sidereal longitude."""
    match = re.fullmatch(r"(\d+) ?([A-Za-z]{2}) ?(\d+)", text)
    assert match, text
    return (
        R[match.group(2)] * 30 + int(match.group(1)) + int(match.group(3)) / 60
    )


# --------------------------------------------------------------------------
# 10.1 Introduction
# --------------------------------------------------------------------------


def test_10_1_what_an_aspect_is():
    """"Planets aspect other planets, rasis and houses in astrology. A planet
    aspecting a house or a planet has some influence on the matters signified
    by that house or planet."

    Three kinds of target — planets, rasis and houses — and the engine returns
    all three.
    """
    assert "other planets, rasis and houses" in ASPECT_DEFINITION
    result = aspect_service.graha(
        Graha.JUPITER, R["Ge"], lagna_rasi=R["Sc"],
        others={Graha.SATURN: R["Sg"]})
    assert result["aspected_rasis"]
    assert result["aspected_grahas"]
    assert all(r["house"] for r in result["aspected_rasis"])


def test_10_1_the_outcome_is_not_claimed_to_be_fixed():
    """"The nature of the influence exerted and the degree to which that
    influence succeeds depends on the individual situation."

    So the engine computes *whether* a graha aspects, never how strongly or to
    what effect. Nothing in the response claims an outcome.
    """
    assert "depends on the individual situation" in ASPECT_DEFINITION
    result = aspect_service.between(Graha.SUN, R["Ta"], R["Sc"])
    assert set(result) >= {"aspects", "house_from_graha"}
    assert "effect" not in result and "strength" not in result


def test_10_1_there_are_exactly_two_kinds():
    """"There are 2 kinds of aspects: (1) graha drishti and (2) rasi drishti.
    Drishti means aspect."""
    assert DRISHTI_MEANS == "aspect"
    assert list(ASPECT_KINDS) == ["graha_drishti", "rasi_drishti"]
    assert ASPECT_KINDS["graha_drishti"]["gloss"] == "planetary aspect"
    assert ASPECT_KINDS["rasi_drishti"]["gloss"] == "sign aspect"


def test_10_1_the_two_kinds_are_counted_from_different_things():
    """Graha drishti: "Each planet aspects certain houses from it... The houses
    aspected are fixed based on the **planet**."

    Rasi drishti: "a planet aspects the rasis aspected by the **rasi occupied**
    by it."

    That is the whole distinction — one varies by graha and is counted from the
    graha, the other varies by rasi and is counted from the rasi. Two grahas in
    the same rasi therefore share their rasi drishti but not their graha
    drishti.
    """
    assert ASPECT_KINDS["graha_drishti"]["varies_by"] == "graha"
    assert ASPECT_KINDS["rasi_drishti"]["varies_by"] == "rasi"
    jupiter = aspect_service.graha(Graha.JUPITER, R["Sc"])
    saturn = aspect_service.graha(Graha.SATURN, R["Sc"])
    assert jupiter["rasi_drishti_rasis"] == saturn["rasi_drishti_rasis"]
    assert jupiter["aspected_rasis"] != saturn["aspected_rasis"]


def test_10_1_rasi_drishti_is_a_property_of_the_rasi_not_the_graha():
    """"rasis aspect each other and a planet aspects the rasis aspected by the
    rasi occupied by it" — the graha inherits, it does not contribute."""
    for rasi in range(12):
        inherited = {r["rasi"] for r in
                     aspect_service.graha(Graha.SUN, rasi)["rasi_drishti_rasis"]}
        assert inherited == set(rasi_drishti(rasi))


# --------------------------------------------------------------------------
# 10.2 Graha drishti
# --------------------------------------------------------------------------


def test_10_2_the_heading_is_printed_with_a_typo():
    """The section heading reads "Graha Drishri". §10.1's own sentence and
    every other use spell it "drishti". Recorded so the misprint is not
    mistaken for a second term.
    """
    assert GRAHA_DRISHTI_HEADING_AS_PRINTED == "Graha Drishri"
    assert "drishti" in ASPECT_KINDS["graha_drishti"]["name"]
    assert GRAHA_DRISHTI_HEADING_AS_PRINTED.lower() != "graha drishti"


def test_10_2_all_planets_aspect_the_seventh():
    """"All planets aspect the 7th house from them."

    All nine, including the nodes: the 7th is the one aspect nothing is
    exempt from.
    """
    assert "All planets aspect the 7th house" in SEVENTH_HOUSE_RULE
    for graha in Graha:
        assert 7 in graha_drishti_houses(graha)


@pytest.mark.parametrize("graha,rasi,target", SEVENTH_HOUSE_EXAMPLES)
def test_10_2_the_five_worked_one_liners(graha, rasi, target):
    """"Sun in Ta aspects Sc. Mars in Ge aspects Sg. Moon in Le aspects Aq.
    Jupiter in Pi aspects Vi. Saturn in Cp aspects Cn."

    Note the last two are chosen so the 7th is the *only* thing being checked
    even though Jupiter and Saturn have special aspects.
    """
    assert graha_aspects_sign(graha, rasi, target)
    assert (target - rasi) % 12 + 1 == 7


def test_10_2_the_seventh_is_always_the_opposite_rasi():
    """"Find the 7th house from the planet and the planet aspects that house."
    Six signs away, in both directions — so the 7th-house aspect is mutual for
    any two grahas in opposite rasis.
    """
    for rasi in range(12):
        seventh = (rasi + 6) % 12
        assert graha_aspects_sign(Graha.SUN, rasi, seventh)
        assert graha_aspects_sign(Graha.SUN, seventh, rasi)


@pytest.mark.parametrize(
    "graha,special", [(Graha.JUPITER, (5, 9)), (Graha.MARS, (4, 8)),
                      (Graha.SATURN, (3, 10))])
def test_10_2_the_three_special_aspect_bullets(graha, special):
    """"Jupiter aspects the 5th and 9th houses from him, in addition to the 7th
    house." And the same shape for Mars (4th, 8th) and Saturn (3rd, 10th)."""
    bullet = next(b for b in SPECIAL_ASPECT_BULLETS if b["graha"] == graha)
    assert bullet["houses"] == special
    assert "in addition to the 7th house" in bullet["text"]
    assert graha_drishti_houses(graha) == tuple(sorted({7, *special}))


def test_10_2_only_three_grahas_have_special_aspects():
    """"In addition, **Mars, Jupiter and Saturn** have special aspects."

    Three, and the chapter names no others — so every other graha aspects the
    7th alone.
    """
    assert set(SPECIAL_ASPECT_GRAHAS) == {Graha.MARS, Graha.JUPITER, Graha.SATURN}
    assert "Mars, Jupiter and Saturn" in SPECIAL_ASPECT_RULE
    for graha in Graha:
        if graha not in SPECIAL_ASPECT_GRAHAS:
            assert graha_drishti_houses(graha) == (7,), graha


def test_10_2_the_bullets_are_printed_jupiter_mars_saturn():
    """Not the graha order, and not the house order — the chapter lists Jupiter
    first. Kept as printed so a reader comparing side by side is not
    confused."""
    assert [b["graha"] for b in SPECIAL_ASPECT_BULLETS] == [
        Graha.JUPITER, Graha.MARS, Graha.SATURN]


def test_10_2_only_jupiters_special_pair_is_symmetric_about_the_seventh():
    """Two houses are symmetric about the 7th when they sum to 14. Jupiter's
    5 and 9 do. Mars's 4 and 8 sum to 12 and Saturn's 3 and 10 sum to 13 —
    neither is symmetric.

    So the three rows follow no derivable pattern and the table has to be
    transcribed. A coder who spotted Jupiter's symmetry and generalised it
    would give Mars the 4th and 10th and Saturn the 3rd and 11th.
    """
    sums = {b["graha"]: sum(b["houses"]) for b in SPECIAL_ASPECT_BULLETS}
    assert sums[Graha.JUPITER] == 14
    assert sums[Graha.MARS] == 12
    assert sums[Graha.SATURN] == 13
    assert len(set(sums.values())) == 3


def test_10_2_no_graha_aspects_its_own_rasi():
    """1 is not among any graha's aspected houses, so nothing aspects
    itself."""
    for graha in Graha:
        assert 1 not in graha_drishti_houses(graha, rahu_ketu_aspects=True)
        assert not graha_aspects_sign(graha, 3, 3, rahu_ketu_aspects=True)


def test_10_2_the_nodes_get_no_special_aspect_from_this_chapter():
    """§10.2 names Mars, Jupiter and Saturn. It gives Rahu and Ketu nothing
    beyond the 7th that "all planets" get.

    `SPECIAL_ASPECTS` carries 5 and 9 for both nodes — not from this chapter —
    behind `rahu_ketu_aspects`, which is off by default. See OI-63.
    """
    assert graha_drishti_houses(Graha.RAHU) == (7,)
    assert graha_drishti_houses(Graha.KETU) == (7,)
    assert graha_drishti_houses(Graha.RAHU, rahu_ketu_aspects=True) == (5, 7, 9)
    assert Graha.RAHU not in SPECIAL_ASPECT_GRAHAS


def test_10_2_a_planet_is_aspected_because_of_where_it_sits():
    """"If any planet occupies the aspected houses, then the planet is also
    aspected."

    So being aspected is a property of the rasi, not of the graha — the nodes
    are aspected like anything else even though they aspect nothing.
    """
    assert "occupies the aspected houses" in ASPECTED_PLANET_RULE
    result = aspect_service.graha(
        Graha.MARS, R["Sc"], others={Graha.KETU: R["Aq"], Graha.RAHU: R["Le"]})
    assert [g["graha_name"] for g in result["aspected_grahas"]] == ["Ketu"]


def test_10_2_the_jupiter_saturn_example():
    """"Jupiter in Ta will aspect Saturn in Cp, because Cp is the 9th house
    from Ta and Jupiter aspects the 9th from him."

    The chapter's own worked chain, checked link by link.
    """
    result = aspect_service.between(Graha.JUPITER, R["Ta"], R["Cp"])
    assert result["house_from_graha"] == 9
    assert result["aspects"] is True
    assert 9 in result["graha_aspects_houses"]
    assert "9th house from Ta" in ASPECTED_PLANET_EXAMPLE


def test_10_2_the_reverse_of_that_example_does_not_hold():
    """Saturn in Cp does **not** aspect Jupiter in Ta: Ta is the 5th from Cp,
    and Saturn aspects the 3rd, 7th and 10th. Graha drishti is not mutual in
    general, unlike the 7th-house aspect and unlike rasi drishti.
    """
    assert aspect_service.between(Graha.SATURN, R["Cp"], R["Ta"])["aspects"] is False
    assert (R["Ta"] - R["Cp"]) % 12 + 1 == 5


def test_10_2_the_practice_note_is_recorded():
    """"Look at a few charts and figure out which planets are aspecting which
    houses and which planets are aspecting which planets... this is an
    important skill required in interpreting charts."""
    assert "important skill" in ASPECTS_ARE_A_SKILL_NOTE


# --------------------------------------------------------------------------
# Example 34
# --------------------------------------------------------------------------

EXAMPLE_34 = [
    (Graha.JUPITER, "Ge", (5, 7, 9), ["Li", "Sg", "Aq"]),
    (Graha.MARS, "Le", (4, 7, 8), ["Sc", "Aq", "Pi"]),
    (Graha.SATURN, "Sg", (3, 7, 10), ["Aq", "Ge", "Vi"]),
]


@pytest.mark.parametrize("graha,rasi,houses,expected", EXAMPLE_34)
def test_example_34(graha, rasi, houses, expected):
    """"Jupiter in Ge will aspect the 5th, 7th and 9th from Ge. So Jupiter in
    Ge will aspect Li, Sg and Aq." And the same for Mars in Le and Saturn in
    Sg."""
    result = aspect_service.graha(graha, R[rasi])
    assert tuple(result["aspects_houses_from_itself"]) == houses
    assert [RASI_ABBR[r["rasi"]] for r in result["aspected_rasis"]] == expected


def test_example_34_lists_the_rasis_in_house_order_not_zodiacal_order():
    """Saturn in Sg gives Aq (3rd), Ge (7th), Vi (10th) — which is *not*
    zodiacal order, since Ge precedes Vi precedes Aq in the zodiac. The book
    prints them by house, and so does the engine.
    """
    result = aspect_service.graha(Graha.SATURN, R["Sg"])
    names = [RASI_ABBR[r["rasi"]] for r in result["aspected_rasis"]]
    assert names == ["Aq", "Ge", "Vi"]
    assert [r["house_from_graha"] for r in result["aspected_rasis"]] == [3, 7, 10]
    assert names != sorted(names, key=lambda n: R[n])


def test_example_34_all_three_grahas_aspect_aquarius():
    """Jupiter from Ge, Mars from Le and Saturn from Sg all reach Aq — the
    three special-aspect grahas converging on one rasi. A useful cross-check
    that the three house sets really are different.
    """
    for graha, rasi, _, _ in EXAMPLE_34:
        assert graha_aspects_sign(graha, R[rasi], R["Aq"])
    house_sets = {graha_drishti_houses(g) for g, _, _, _ in EXAMPLE_34}
    assert len(house_sets) == 3


# --------------------------------------------------------------------------
# Chart 5 — the aspects exercise chart
# --------------------------------------------------------------------------

#: Chart 5's printed rasi longitudes.
CHART_5 = {
    "Asc": "5 Li 23", "Sun": "6 Ar 20", "Moon": "20 Li 50", "Mars": "26 Ar 22",
    "Merc": "17 Pi 21", "Jup": "19 Ar 42", "Ven": "22 Pi 25", "Sat": "23 Ar 55",
    "Rahu": "5 Cn 23", "Ketu": "5 Cp 23", "HL": "17 Ta 16", "GL": "19 Cp 30",
}

#: The navamsa diagram as printed beside it.
CHART_5_NAVAMSA_PRINTED = {
    "Asc": "Sc", "Sun": "Ta", "Moon": "Ar", "Mars": "Sc", "Merc": "Sg",
    "Jup": "Vi", "Ven": "Cp", "Sat": "Sc", "Rahu": "Le", "Ketu": "Aq",
    "HL": "Ge", "GL": "Ge",
}

CHART_5_CHARA_KARAKAS = {
    "Mars": "AK", "Rahu": "AmK", "Sat": "BK", "Ven": "MK",
    "Moon": "PiK", "Jup": "PK", "Merc": "GK", "Sun": "DK",
}

_NAME_TO_GRAHA = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
    "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU,
}


@pytest.mark.parametrize("body", list(CHART_5))
def test_chart_5_navamsa_derives_from_the_printed_longitudes(body):
    """All twelve navamsa positions, including both special lagnas, derive from
    the rasi longitudes and match the printed diagram.

    This is what makes Exercise 14 a real test: the positions it is solved from
    are computed, not transcribed.
    """
    assert RASI_ABBR[d9_navamsa(lon(CHART_5[body])).sign] == \
        CHART_5_NAVAMSA_PRINTED[body]


def test_chart_5_the_navamsa_lagna_is_scorpio():
    """5 Li 23 falls in the Scorpio navamsa. Every house number in Exercise
    14's answer is counted from there, so getting this wrong shifts the whole
    column.
    """
    assert RASI_ABBR[d9_navamsa(lon(CHART_5["Asc"])).sign] == "Sc"


def test_chart_5_the_rasi_lagna_is_libra_not_scorpio():
    """The trap in Exercise 14. Chart 5's rasi lagna is Libra and its navamsa
    lagna is Scorpio; the exercise is solved in the **navamsa**, as its own
    diagram caption "Navamsa / Aspects Exercise" says.

    Solved in the rasi chart, not one of the eight rows comes out right.
    """
    assert RASI_ABBR[int(lon(CHART_5["Asc"]) // 30)] == "Li"
    assert RASI_ABBR[d9_navamsa(lon(CHART_5["Asc"])).sign] == "Sc"


@pytest.mark.parametrize("body,symbol", list(CHART_5_CHARA_KARAKAS.items()))
def test_chart_5_confirms_the_chapter_8_chara_karakas(body, symbol):
    """Chart 5 prints a chara karaka beside each graha. Recomputing them from
    the longitudes with chapter 8's procedure reproduces all eight — so the
    chart is internally consistent and chapters 8 and 10 agree.
    """
    from hora.charts.karaka import chara_karakas

    positions = {_NAME_TO_GRAHA[name]: lon(CHART_5[name])
                 for name in CHART_5_CHARA_KARAKAS}
    assigned = {k.graha: k.symbol for k in chara_karakas(positions)}
    assert assigned[_NAME_TO_GRAHA[body]] == symbol


# --------------------------------------------------------------------------
# Exercise 14
# --------------------------------------------------------------------------

#: The answer table, exactly as printed.
EXERCISE_14 = [
    ("Sun", ["Sc"], [1], ["Mars", "Saturn"]),
    ("Moon", ["Li"], [12], []),
    ("Mars", ["Aq", "Ta", "Ge"], [4, 7, 8], ["Ketu", "Sun"]),
    ("Merc", ["Ge"], [8], []),
    ("Jup", ["Cp", "Pi", "Ta"], [3, 5, 7], ["Venus", "Sun"]),
    ("Ven", ["Cn"], [9], []),
    ("Sat", ["Cp", "Ta", "Le"], [3, 7, 10], ["Venus", "Sun", "Rahu"]),
]


def _exercise_14_chart():
    rasis = {_NAME_TO_GRAHA[name]: d9_navamsa(lon(text)).sign
             for name, text in CHART_5.items() if name in _NAME_TO_GRAHA}
    lagna = d9_navamsa(lon(CHART_5["Asc"])).sign
    return aspect_service.chart(rasis, lagna)


@pytest.mark.parametrize("body,rasis,houses,planets", EXERCISE_14)
def test_exercise_14_reproduces_the_answer_table(body, rasis, houses, planets):
    """Every cell of Exercise 14's answer: aspected rasis, aspected houses and
    aspected planets, for each of the seven grahas."""
    row = next(r for r in _exercise_14_chart()["grahas"]
               if r["graha"] == _NAME_TO_GRAHA[body])
    assert [RASI_ABBR[r["rasi"]] for r in row["aspected_rasis"]] == rasis
    assert [r["house"] for r in row["aspected_rasis"]] == houses
    assert sorted(g["graha_name"] for g in row["aspected_grahas"]) == sorted(planets)


def test_exercise_14_asks_about_seven_grahas_not_nine():
    """"...aspected with graha drishti by Sun, Moon, Mars, Mercury, Jupiter,
    Venus and Saturn" — the nodes are not asked about, matching §10.2 giving
    them no aspect."""
    chart = _exercise_14_chart()
    assert len(chart["grahas"]) == 7
    names = {r["graha_name"] for r in chart["grahas"]}
    assert "Rahu" not in names and "Ketu" not in names


def test_exercise_14_the_nodes_appear_as_aspected_though_they_aspect_nothing():
    """Ketu is aspected by Mars and Rahu by Saturn in the printed answer. Being
    aspected needs only a placement, which is the asymmetry §10.2 sets up.
    """
    rows = {r["graha_name"]: r for r in _exercise_14_chart()["grahas"]}
    assert "Ketu" in {g["graha_name"] for g in rows["Mars"]["aspected_grahas"]}
    assert "Rahu" in {g["graha_name"] for g in rows["Saturn"]["aspected_grahas"]}


def test_exercise_14_the_three_special_aspect_grahas_give_three_rasis_each():
    """Mars, Jupiter and Saturn return three aspected rasis; the other four
    return one. That split is visible in the answer table and is the whole of
    §10.2's exception.
    """
    rows = {r["graha_name"]: r for r in _exercise_14_chart()["grahas"]}
    three = {n for n, r in rows.items() if len(r["aspected_rasis"]) == 3}
    assert three == {"Mars", "Jupiter", "Saturn"}
    assert all(len(r["aspected_rasis"]) == 1 for n, r in rows.items()
               if n not in three)


def test_exercise_14_mars_and_saturn_share_a_rasi_but_not_their_aspects():
    """Both sit in Scorpio in the navamsa. Mars reaches Aq, Ta, Ge; Saturn
    reaches Cp, Ta, Le. Only Taurus — the 7th — is common.

    The clearest demonstration in the exercise that graha drishti varies by
    graha, not by rasi.
    """
    rows = {r["graha_name"]: r for r in _exercise_14_chart()["grahas"]}
    assert rows["Mars"]["rasi_name"] == rows["Saturn"]["rasi_name"] == "Scorpio"
    mars = {r["rasi_name"] for r in rows["Mars"]["aspected_rasis"]}
    saturn = {r["rasi_name"] for r in rows["Saturn"]["aspected_rasis"]}
    assert mars & saturn == {"Taurus"}
    assert rows["Mars"]["rasi_drishti_rasis"] == rows["Saturn"]["rasi_drishti_rasis"]


def test_exercise_14_the_sun_is_aspected_by_four_grahas():
    """The Sun sits in Taurus, the 7th from Scorpio and the 9th from Virgo, so
    Mars, Saturn and Jupiter all reach him — and he aspects Mars and Saturn
    back. Counted across the answer table's last column.
    """
    chart = _exercise_14_chart()
    aspecting_sun = {r["graha_name"] for r in chart["grahas"]
                     if any(g["graha_name"] == "Sun" for g in r["aspected_grahas"])}
    assert aspecting_sun == {"Mars", "Jupiter", "Saturn"}


def test_exercise_14_solved_in_the_rasi_chart_gives_the_wrong_answer():
    """Guarding the trap directly: run the same exercise on Chart 5's rasi
    positions and Libra lagna, and not one row matches."""
    rasis = {_NAME_TO_GRAHA[name]: int(lon(text) // 30)
             for name, text in CHART_5.items() if name in _NAME_TO_GRAHA}
    wrong = aspect_service.chart(rasis, int(lon(CHART_5["Asc"]) // 30))
    rows = {r["graha_name"]: r for r in wrong["grahas"]}
    for body, expected_rasis, _, _ in EXERCISE_14:
        name = {"Merc": "Mercury", "Jup": "Jupiter", "Ven": "Venus",
                "Sat": "Saturn"}.get(body, body)
        got = [RASI_ABBR[r["rasi"]] for r in rows[name]["aspected_rasis"]]
        assert got != expected_rasis, name


# --------------------------------------------------------------------------
# The endpoints
# --------------------------------------------------------------------------


def test_rules_endpoint_states_both_kinds_and_all_three_bullets(client):
    body = client.get("/v1/aspect/rules").json()
    assert [k["key"] for k in body["kinds"]] == ["graha_drishti", "rasi_drishti"]
    assert [s["graha_name"] for s in body["special_aspects"]] == [
        "Jupiter", "Mars", "Saturn"]
    assert [s["all_houses"] for s in body["special_aspects"]] == [
        [5, 7, 9], [4, 7, 8], [3, 7, 10]]
    assert len(body["aspecting_grahas"]) == 7
    assert "Rahu" in body["nodes_note"]


def test_chart_endpoint_answers_exercise_14(client):
    rasis = {int(_NAME_TO_GRAHA[name]): d9_navamsa(lon(text)).sign
             for name, text in CHART_5.items() if name in _NAME_TO_GRAHA}
    body = client.post("/v1/aspect/chart", json={
        "rasis": rasis, "lagna_rasi": R["Sc"]}).json()
    rows = {r["graha_name"]: r for r in body["grahas"]}
    assert [r["house"] for r in rows["Saturn"]["aspected_rasis"]] == [3, 7, 10]
    assert sorted(g["graha_name"] for g in rows["Saturn"]["aspected_grahas"]) == [
        "Rahu", "Sun", "Venus"]


def test_chart_endpoint_works_without_a_lagna(client):
    """§10.2 needs no lagna to say which rasis a graha aspects. The house
    column is null rather than the request being refused."""
    body = client.post("/v1/aspect/chart", json={"rasis": {"4": R["Ge"]}}).json()
    row = body["grahas"][0]
    assert [RASI_ABBR[r["rasi"]] for r in row["aspected_rasis"]] == ["Li", "Sg", "Aq"]
    assert all(r["house"] is None for r in row["aspected_rasis"])
    assert body["lagna_rasi"] is None


def test_graha_endpoint_answers_the_chapters_one_liner(client):
    body = client.post("/v1/aspect/graha",
                       json={"graha": int(Graha.SUN), "rasi": R["Ta"]}).json()
    assert [r["rasi_name"] for r in body["aspected_rasis"]] == ["Scorpio"]
    assert body["has_special_aspect"] is False


def test_between_endpoint_answers_the_jupiter_saturn_example(client):
    body = client.post("/v1/aspect/between", json={
        "graha": int(Graha.JUPITER), "graha_rasi": R["Ta"],
        "target_rasi": R["Cp"]}).json()
    assert body["aspects"] is True
    assert body["house_from_graha"] == 9


def test_endpoints_reject_a_bad_rasi(client):
    assert client.post("/v1/aspect/graha",
                       json={"graha": 0, "rasi": 12}).status_code == 422
    assert client.post("/v1/aspect/between", json={
        "graha": 0, "graha_rasi": 0, "target_rasi": -1}).status_code == 422


def test_chart_endpoint_rejects_an_empty_chart(client):
    response = client.post("/v1/aspect/chart", json={"rasis": {}})
    assert response.status_code == 400
    assert "at least one graha" in response.json()["error"]["message"]
