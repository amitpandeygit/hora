"""Chapter 10 §10.6 — Virodhargala, and Exercise 16.

§10.5 (Argala proper) has not been supplied yet. §10.6 names the four argala
houses outright — the 2nd, 4th, 11th and 5th — so the computation is complete
without it, but §10.5's own statements still need a pass. See OI-66.

Exercise 16 is solved in Chart 5's **navamsa**, like Exercises 14 and 15: its
house labels run 1st (Sc) to 12th (Li), which is Scorpio lagna. All twelve
rows of the printed answer reproduce, including the starred 4th row where
Ketu reverses the direction of counting.
"""
import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.argala import (
    argalas_on_sign,
    counts_anti_zodiacally,
    house_sign,
    ketu_sign_of,
)
from hora.charts.vargas import d9_navamsa
from hora.core.const import (
    ARGALA_BY_NATURE,
    ARGALA_PAIRS,
    KETU_NOTE_EXAMPLE,
    KETU_REVERSES_ARGALA,
    SEVERAL_MALEFICS,
    THIRD_HOUSE_MALEFIC_RULE,
    VIRODHARGALA_DEFINITION,
    VIRODHARGALA_EXAMPLE,
    VIRODHARGALA_RULE,
    Graha,
)
from hora.services import argala_service
from tests.unit.test_book_chapter10 import CHART_5, RASI_ABBR, R, lon

_NAME_TO_GRAHA = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
    "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU,
}

#: Abbreviations exactly as Exercise 16's answer table prints them.
ABBR = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars", "Mercury": "Merc",
        "Jupiter": "Jup", "Venus": "Ven", "Saturn": "Sat", "Rahu": "Rahu",
        "Ketu": "Ketu"}


@pytest.fixture
def client():
    return TestClient(app)


def _navamsa():
    return {int(_NAME_TO_GRAHA[name]): d9_navamsa(lon(text)).sign
            for name, text in CHART_5.items() if name in _NAME_TO_GRAHA}


def _exercise_16():
    return argala_service.chart(_navamsa(), d9_navamsa(lon(CHART_5["Asc"])).sign)


# --------------------------------------------------------------------------
# 10.6 The obstruction pairing
# --------------------------------------------------------------------------


def test_10_6_what_virodhargala_is():
    """"Virodhargala shows the obstruction of argala."""
    assert VIRODHARGALA_DEFINITION == "Virodhargala shows the obstruction of argala."


@pytest.mark.parametrize("argala,virodha", ARGALA_PAIRS)
def test_10_6_the_four_pairs(argala, virodha):
    """"Planets and houses in the 12th, 10th, 3rd and 9th houses from a house
    or planet cause virodhargala and obstruct the argala on it from the 2nd,
    4th, 11th and 5th houses from it (**respectively**)."

    "Respectively" is the whole content of the rule, so the houses are stored
    as pairs. Two parallel lists could drift; a pair cannot.
    """
    assert (argala, virodha) in ARGALA_PAIRS
    assert "respectively" in VIRODHARGALA_RULE


def test_10_6_the_pairing_is_the_printed_order():
    """12th-2nd, 10th-4th, 3rd-11th, 9th-5th, in that order. Exercise 16's
    answer table prints its columns 2nd, 4th, 5th, 11th and 12th, 10th, 9th,
    3rd — a different order, which is exactly why the pairing has to be stored
    rather than inferred from column position.
    """
    assert ARGALA_PAIRS == ((2, 12), (4, 10), (11, 3), (5, 9))
    assert [a for a, _ in ARGALA_PAIRS] != sorted(a for a, _ in ARGALA_PAIRS)


def test_10_6_each_obstructor_mirrors_its_argala_across_the_target():
    """The four pairs are one relation, not four cases: every pair sums to 14.

    2+12, 4+10, 11+3, 5+9. Summing to 14 means the obstructor sits the **same
    distance from the target in the opposite direction** — the 12th is the 2nd
    counted backwards, the 10th is the 4th backwards, and so on.

    That is also why §10.6's Ketu note can say "Virodhargala is also counted
    similarly" without further explanation: reversing the direction simply
    swaps each house with its own obstructor.
    """
    for argala, virodha in ARGALA_PAIRS:
        assert argala + virodha == 14, (argala, virodha)
        for target in range(12):
            assert house_sign(target, argala, reverse=True) == \
                house_sign(target, virodha)


def test_10_6_the_eight_houses_are_all_distinct():
    """Four argala houses and four obstructors, no overlap — so no house is
    both. The 1st, 6th, 7th and 8th take no part at all.
    """
    argalas = {a for a, _ in ARGALA_PAIRS}
    virodhas = {v for _, v in ARGALA_PAIRS}
    assert argalas & virodhas == set()
    assert argalas | virodhas == {2, 3, 4, 5, 9, 10, 11, 12}
    assert set(range(1, 13)) - (argalas | virodhas) == {1, 6, 7, 8}


@pytest.mark.parametrize(
    "nature,name", [("malefic", "paapaargala"), ("benefic", "subhaargala")])
def test_10_6_argala_is_named_by_the_intervening_grahas_nature(nature, name):
    """"With Saturn being a malefic, this is a paapaargala (malefic
    intervention)... With Venus being a benefic, it is a subhaargala (benefic
    intervention)."""
    assert ARGALA_BY_NATURE[nature]["name"] == name
    assert "intervention" in ARGALA_BY_NATURE[nature]["gloss"]


# --------------------------------------------------------------------------
# 10.6's worked example
# --------------------------------------------------------------------------


def test_10_6_the_worked_example_saturns_argala_is_obstructed():
    """"Saturn is in the 4th from Mercury and Ge and he causes argala on them...
    But Jupiter is in the 10th from Mercury and Ge. So he obstructs Saturn's
    argala and averts the troubles."

    Mercury, Jupiter, Venus and Saturn in Ge, Pi, Ar and Vi.
    """
    result = argala_service.on_sign(R["Ge"], {
        Graha.MERCURY: R["Ge"], Graha.JUPITER: R["Pi"],
        Graha.VENUS: R["Ar"], Graha.SATURN: R["Vi"]})
    fourth = next(a for a in result["argalas"] if a["house"] == 4)
    assert [g["graha_name"] for g in fourth["grahas"]] == ["Saturn"]
    assert fourth["obstructed"] is True
    assert fourth["paired_house"] == 10
    tenth = next(v for v in result["virodhargalas"] if v["house"] == 10)
    assert [g["graha_name"] for g in tenth["grahas"]] == ["Jupiter"]


def test_10_6_the_worked_example_venus_argala_is_unobstructed():
    """"Venus is in the 11th from Mercury and Ge and so he causes argala on
    them... If Le (3rd from Ge) is empty, this argala is unobstructed."

    The conditional is the point: an argala is obstructed only when its paired
    house is actually occupied. An empty obstructor leaves it standing.
    """
    result = argala_service.on_sign(R["Ge"], {
        Graha.MERCURY: R["Ge"], Graha.JUPITER: R["Pi"],
        Graha.VENUS: R["Ar"], Graha.SATURN: R["Vi"]})
    eleventh = next(a for a in result["argalas"] if a["house"] == 11)
    assert [g["graha_name"] for g in eleventh["grahas"]] == ["Venus"]
    assert eleventh["obstructed"] is False
    assert eleventh["paired_house"] == 3
    third = next(v for v in result["virodhargalas"] if v["house"] == 3)
    assert third["sign"] == R["Le"]
    assert third["grahas"] == []
    assert third["present"] is False


def test_10_6_the_example_puts_a_planet_on_its_own_sign():
    """"Saturn is in the 4th from **Mercury and Ge**" — argala falls on a
    house *and* on the planets in it, so Mercury in Ge receives whatever Ge
    receives. One computation serves both.
    """
    assert VIRODHARGALA_EXAMPLE["target_sign"] == R["Ge"]
    assert VIRODHARGALA_EXAMPLE["rasis"]["Mercury"] == R["Ge"]
    assert "Mercury and Ge" in VIRODHARGALA_EXAMPLE["text"]


# --------------------------------------------------------------------------
# The Ketu note
# --------------------------------------------------------------------------


def test_10_6_ketu_reverses_the_direction_of_counting():
    """"If a sign contains Ketu, argalas and virodhargalas on it are counted
    anti-zodiacally."""
    assert "anti-zodiacally" in KETU_REVERSES_ARGALA
    assert counts_anti_zodiacally(R["Vi"], R["Vi"]) is True
    assert counts_anti_zodiacally(R["Ge"], R["Vi"]) is False


def test_10_6_the_ketu_note_worked_example():
    """"let us say Ketu is in Vi. Then Le, Ge, Sc and Ta are the 2nd, 4th,
    11th and 5th from Vi (counted anti-zodiacally)."""
    assert KETU_NOTE_EXAMPLE["ketu_sign"] == R["Vi"]
    for house, sign in zip(KETU_NOTE_EXAMPLE["houses"],
                           KETU_NOTE_EXAMPLE["signs"], strict=True):
        assert house_sign(R["Vi"], house, reverse=True) == sign
    assert [RASI_ABBR[s] for s in KETU_NOTE_EXAMPLE["signs"]] == [
        "Le", "Ge", "Sc", "Ta"]


def test_10_6_the_reversal_belongs_to_the_target_sign_not_the_counter():
    """"argalas and virodhargalas **on it**" — on the sign holding Ketu. A
    different sign counts normally even when the house it counts *to* holds
    Ketu.

    Easy to implement the wrong way round, and Exercise 16 proves it: only its
    4th row is starred, though every other row counts to Aquarius at some
    point.
    """
    ketu = R["Aq"]
    assert counts_anti_zodiacally(R["Aq"], ketu) is True
    assert counts_anti_zodiacally(R["Cp"], ketu) is False
    starred = [h["house"] for h in _exercise_16()["houses"]
               if h["counted_anti_zodiacally"]]
    assert starred == [4]


def test_10_6_virodhargala_reverses_too():
    """"Virodhargala is also counted similarly." Both halves flip together, so
    the pairing survives the reversal."""
    assert "Virodhargala is also counted similarly" in KETU_REVERSES_ARGALA
    row = next(h for h in _exercise_16()["houses"] if h["house"] == 4)
    for entry in row["argalas"] + row["virodhargalas"]:
        assert entry["sign"] == house_sign(R["Aq"], entry["house"], reverse=True)


def test_10_6_reversal_is_an_involution():
    """Counting forward then backward by the same house returns to the start,
    for every sign and house — so the reversed direction is the plain mirror
    and not an off-by-one variant."""
    for sign in range(12):
        for house in range(1, 13):
            forward = house_sign(sign, house)
            back = house_sign(forward, house, reverse=True)
            assert back == sign, (sign, house)


# --------------------------------------------------------------------------
# The 3rd-house special principle
# --------------------------------------------------------------------------


def test_10_6_several_malefics_in_the_third_cause_argala_instead():
    """"If there are several malefics in the 3rd house from a house or a
    planet, they cause argala instead of virodhargala on that house or
    planet."""
    assert "argala instead of virodhargala" in THIRD_HOUSE_MALEFIC_RULE
    occupants = {R["Le"]: (Graha.SUN, Graha.MARS, Graha.SATURN)}
    rows = argalas_on_sign(
        R["Ge"], occupants,
        malefic=frozenset({Graha.SUN, Graha.MARS, Graha.SATURN}), several=3)
    third = next(r for r in rows if r.house == 3)
    assert third.kind == "argala"
    assert third.promoted_from_virodhargala is True


def test_10_6_the_rule_needs_malefics_and_never_guesses_one():
    """Chapter 3 makes the Moon and Mercury conditionally malefic, so the
    default set is the five that are fixed. A caller who wants otherwise
    supplies `malefics`; the service does not decide it.
    """
    assert argala_service.FIXED_MALEFICS == frozenset(
        {Graha.SUN, Graha.MARS, Graha.SATURN, Graha.RAHU, Graha.KETU})
    assert Graha.MOON not in argala_service.FIXED_MALEFICS
    assert Graha.MERCURY not in argala_service.FIXED_MALEFICS


def test_10_6_the_rule_never_fires_without_a_malefic_set():
    """`argalas_on_sign` with no `malefic` leaves every 3rd-house row a
    virodhargala, whatever sits there — the rule cannot fire on a guess."""
    occupants = {R["Le"]: (Graha.SUN, Graha.MARS, Graha.SATURN)}
    rows = argalas_on_sign(R["Ge"], occupants)
    third = next(r for r in rows if r.house == 3)
    assert third.kind == "virodhargala"
    assert third.promoted_from_virodhargala is False


def test_the_book_does_not_fire_the_rule_on_two_malefics():
    """**The evidence for the threshold.** Exercise 16's 11th house is Vi, and
    the 3rd from Vi is Sc, which holds **Mars and Saturn** — two unambiguous
    malefics. The printed answer still lists them under *virodhargalas*, not
    argalas.

    So two is not "several" by the book's own worked output, and three is the
    smallest threshold reproducing Exercise 16. The book never states a
    number. See OI-65.
    """
    assert SEVERAL_MALEFICS == 3
    row = next(h for h in _exercise_16()["houses"] if h["house"] == 11)
    third = next(v for v in row["virodhargalas"] if v["house"] == 3)
    assert [ABBR[g["graha_name"]] for g in third["grahas"]] == ["Mars", "Sat"]
    assert third["kind"] == "virodhargala"
    assert not any(a["promoted_from_virodhargala"] for a in row["argalas"])


def test_a_threshold_of_two_would_break_exercise_16():
    """Stated as a failing case rather than an opinion: lower the threshold to
    two and the 11th house row stops matching the book."""
    chart = argala_service.chart(
        _navamsa(), d9_navamsa(lon(CHART_5["Asc"])).sign, several=2)
    row = next(h for h in chart["houses"] if h["house"] == 11)
    promoted = [a for a in row["argalas"] if a["promoted_from_virodhargala"]]
    assert len(promoted) == 1
    assert [ABBR[g["graha_name"]] for g in promoted[0]["grahas"]] == ["Mars", "Sat"]


def test_the_threshold_is_the_only_place_the_rule_can_bite_in_exercise_16():
    """Across all twelve houses only one has two or more malefics in its 3rd,
    so the whole disagreement rests on that single cell — which is why the
    exercise is weak evidence and OI-65 stays open.
    """
    chart = argala_service.chart(
        _navamsa(), d9_navamsa(lon(CHART_5["Asc"])).sign, several=2)
    promoted = [h["house"] for h in chart["houses"]
                if any(a["promoted_from_virodhargala"] for a in h["argalas"])]
    assert promoted == [11]


# --------------------------------------------------------------------------
# Exercise 16
# --------------------------------------------------------------------------

#: The answer table, exactly as printed. Argala columns 2nd, 4th, 5th, 11th;
#: virodhargala columns 12th, 10th, 9th, 3rd.
EXERCISE_16 = [
    (1, "Sc", ["Merc"], ["Ketu"], [], ["Jup"], [], ["Rahu"], [], ["Ven"]),
    (2, "Sg", ["Ven"], [], ["Moon"], [], ["Mars", "Sat"], ["Jup"], ["Rahu"],
     ["Ketu"]),
    (3, "Cp", ["Ketu"], ["Moon"], ["Sun"], ["Mars", "Sat"], ["Merc"], [],
     ["Jup"], []),
    (4, "Aq", ["Ven"], ["Mars", "Sat"], [], ["Moon"], [], ["Sun"], [],
     ["Merc"]),
    (5, "Pi", ["Moon"], [], [], ["Ven"], ["Ketu"], ["Merc"], ["Mars", "Sat"],
     ["Sun"]),
    (6, "Ar", ["Sun"], [], ["Rahu"], ["Ketu"], [], ["Ven"], ["Merc"], []),
    (7, "Ta", [], ["Rahu"], ["Jup"], [], ["Moon"], ["Ketu"], ["Ven"], []),
    (8, "Ge", [], ["Jup"], [], ["Moon"], ["Sun"], [], ["Ketu"], ["Rahu"]),
    (9, "Cn", ["Rahu"], [], ["Mars", "Sat"], ["Sun"], [], ["Moon"], [],
     ["Jup"]),
    (10, "Le", ["Jup"], ["Mars", "Sat"], ["Merc"], [], [], ["Sun"], ["Moon"],
     []),
    (11, "Vi", [], ["Merc"], ["Ven"], [], ["Rahu"], [], ["Sun"],
     ["Mars", "Sat"]),
    (12, "Li", ["Mars", "Sat"], ["Ven"], ["Ketu"], ["Rahu"], ["Jup"], [], [],
     ["Merc"]),
]


@pytest.mark.parametrize(
    "house,sign,a2,a4,a5,a11,v12,v10,v9,v3",
    EXERCISE_16, ids=[str(row[0]) for row in EXERCISE_16])
def test_exercise_16_reproduces_the_answer_table(
        house, sign, a2, a4, a5, a11, v12, v10, v9, v3):
    """All twelve rows, all eight columns — 96 cells."""
    row = next(h for h in _exercise_16()["houses"] if h["house"] == house)
    assert RASI_ABBR[row["sign"]] == sign
    argalas = {a["house"]: [ABBR[g["graha_name"]] for g in a["grahas"]]
               for a in row["argalas"]}
    virodhas = {v["house"]: [ABBR[g["graha_name"]] for g in v["grahas"]]
                for v in row["virodhargalas"]}
    assert argalas == {2: a2, 4: a4, 5: a5, 11: a11}
    assert virodhas == {12: v12, 10: v10, 9: v9, 3: v3}


def test_exercise_16_is_solved_in_the_navamsa_like_14_and_15():
    """Its house labels run 1st (Sc) through 12th (Li) — Scorpio lagna, which
    is Chart 5's navamsa. The rasi lagna is Libra."""
    assert next(row[1] for row in EXERCISE_16) == "Sc"
    assert RASI_ABBR[d9_navamsa(lon(CHART_5["Asc"])).sign] == "Sc"
    assert RASI_ABBR[int(lon(CHART_5["Asc"]) // 30)] == "Li"


def test_exercise_16_only_the_fourth_house_is_starred():
    """The footnote reads "Ketu is in Aq and the counting is in reverse", and
    Aq is the 4th from Scorpio. Exactly one row, which is what makes the
    reversal a property of the target sign.
    """
    ketu = ketu_sign_of(_navamsa())
    assert RASI_ABBR[ketu] == "Aq"
    assert [row[0] for row in EXERCISE_16 if row[1] == "Aq"] == [4]


def test_exercise_16_every_house_appears_exactly_once_as_a_sign():
    """Twelve houses, twelve distinct signs — the table covers the zodiac, so
    no placement is missed."""
    assert len({row[1] for row in EXERCISE_16}) == 12


def test_exercise_16_every_graha_appears_in_both_halves_of_the_table():
    """Each of the nine grahas causes at least one argala and at least one
    virodhargala somewhere in the table. A graha absent from one half would
    mean a placement never reached — worth knowing the exercise exercises all
    nine both ways.
    """
    argala_grahas, virodha_grahas = set(), set()
    for _, _, a2, a4, a5, a11, v12, v10, v9, v3 in EXERCISE_16:
        argala_grahas |= {g for cell in (a2, a4, a5, a11) for g in cell}
        virodha_grahas |= {g for cell in (v12, v10, v9, v3) for g in cell}
    assert argala_grahas == virodha_grahas == set(ABBR.values())


def test_exercise_16_mars_and_saturn_always_appear_together():
    """They share Scorpio in the navamsa, so no cell can hold one without the
    other. Fifteen appearances, every one a pair.
    """
    for _, _, *cells in EXERCISE_16:
        for cell in cells:
            assert ("Mars" in cell) == ("Sat" in cell), cell


# --------------------------------------------------------------------------
# The endpoints
# --------------------------------------------------------------------------


def test_chart_endpoint_answers_exercise_16(client):
    body = client.post("/v1/argala/chart", json={
        "rasis": _navamsa(), "lagna_rasi": R["Sc"]}).json()
    fourth = next(h for h in body["houses"] if h["house"] == 4)
    assert fourth["counted_anti_zodiacally"] is True
    argalas = {a["house"]: [ABBR[g["graha_name"]] for g in a["grahas"]]
               for a in fourth["argalas"]}
    assert argalas == {2: ["Ven"], 4: ["Mars", "Sat"], 5: [], 11: ["Moon"]}
    assert body["several_malefics_threshold"] == 3


def test_sign_endpoint_answers_the_worked_example(client):
    body = client.post("/v1/argala/sign", json={
        "sign": R["Ge"],
        "rasis": {3: R["Ge"], 4: R["Pi"], 5: R["Ar"], 6: R["Vi"]}}).json()
    by_house = {a["house"]: a for a in body["argalas"]}
    assert by_house[4]["obstructed"] is True
    assert by_house[11]["obstructed"] is False
    assert body["counted_anti_zodiacally"] is False


def test_rules_endpoint_states_the_pairing_and_both_special_rules(client):
    body = client.get("/v1/argala/rules").json()
    assert [(p["argala_house"], p["virodhargala_house"]) for p in body["pairs"]] == [
        (2, 12), (4, 10), (11, 3), (5, 9)]
    assert {p["argala_house"] for p in body["pairs"]} == {2, 4, 11, 5}
    assert {p["virodhargala_house"] for p in body["pairs"]} == {12, 10, 3, 9}
    assert body["by_nature"]["malefic"]["name"] == "paapaargala"
    assert "anti-zodiacally" in body["ketu_note"]
    assert body["several_malefics_threshold"] == 3
    assert "does not say" in body["several_malefics_note"]
    assert len(body["fixed_malefics"]) == 5


def test_endpoints_reject_bad_input(client):
    assert client.post("/v1/argala/sign", json={
        "sign": 12, "rasis": {0: 0}}).status_code == 422
    response = client.post("/v1/argala/chart", json={
        "rasis": {}, "lagna_rasi": 0})
    assert response.status_code == 400
    assert "at least one graha" in response.json()["error"]["message"]
