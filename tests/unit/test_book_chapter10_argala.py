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
    ARGALA_DEFINITION,
    ARGALA_EXAMPLES,
    ARGALA_HOUSE_KIND,
    ARGALA_HOUSE_ROLE,
    ARGALA_IS_ADDITIONAL,
    ARGALA_IS_IMPORTANT,
    ARGALA_MEANS,
    ARGALA_NATURE_EXAMPLE,
    ARGALA_NATURE_RULE,
    ARGALA_NATURE_SPELLING_VARIANTS,
    ARGALA_PAIRS,
    ARGALA_ROLE_EXAMPLES,
    ARGALA_USE_CONCLUSION,
    ARGALA_USE_PROCEDURE,
    ASPECT_SOURCE,
    EXAMPLE_35_PREMISE,
    EXAMPLE_35_RULE,
    INFLUENCE_RANKING,
    KETU_NOTE_EXAMPLE,
    KETU_REVERSES_ARGALA,
    PRIMARY_ARGALA_RULE,
    SECONDARY_ARGALA_EXAMPLES,
    SECONDARY_ARGALA_RULE,
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


# --------------------------------------------------------------------------
# 10.5 Argala proper
# --------------------------------------------------------------------------


def test_10_5_argala_is_a_third_influence_beside_the_two_drishtis():
    """"In addition to the influence caused by planets with graha drishti and
    rasi drishti, there is another influence called "argala"."

    So chapter 10 has three mechanisms, not two — which is why argala lives in
    its own service rather than beside drishti.
    """
    assert "graha drishti and rasi drishti" in ARGALA_IS_ADDITIONAL
    assert "another influence" in ARGALA_IS_ADDITIONAL
    assert "very important" in ARGALA_IS_IMPORTANT


def test_10_5_argala_means_a_bolt():
    """"Literally speaking, argala means "a bolt". Argala on a house shows the
    influences that intervene in its affairs, decide some parts of it and
    close the bolt on it, so to speak."

    The image is the definition: a bolt is what *closes* a matter, which is
    why the influence is called decisive rather than merely strong.
    """
    assert ARGALA_MEANS == "a bolt"
    assert "close the bolt on it" in ARGALA_DEFINITION
    assert "decide some parts of it" in ARGALA_DEFINITION


@pytest.mark.parametrize(
    "rank,influence,strength",
    [(1, "rasi drishti", "small"), (2, "graha drishti", "more concrete"),
     (3, "argala", "decisive")],
)
def test_10_5_ranks_all_three_influences(rank, influence, strength):
    """"Planet having rasi drishti have a small influence. Planets having graha
    drishti have a more concrete influence... The influence caused by argala is
    decisive."

    The first time the book ranks all three in one passage, and it settles
    §10.4's comparison: rasi drishti "limited", graha drishti "greater", and
    now argala above both.
    """
    entry = INFLUENCE_RANKING[rank - 1]
    assert entry["influence"] == influence
    assert entry["strength"] == strength
    assert entry["rank"] == rank


def test_10_5_the_ranking_agrees_with_10_4s_comparison():
    """§10.4 called graha drishti "greater influence" and rasi drishti
    "limited influence on the neighbors". §10.5 puts them in the same order
    and adds argala on top. The two sections agree.
    """
    assert "limited influence" in ASPECT_SOURCE["rasi_drishti"]["scope"]
    assert "greater influence" in ASPECT_SOURCE["graha_drishti"]["scope"]
    order = [r["influence"] for r in INFLUENCE_RANKING]
    assert order.index("rasi drishti") < order.index("graha drishti")
    assert order.index("graha drishti") < order.index("argala")


def test_10_5_the_ranking_is_ordinal_and_carries_no_number():
    """"small", "more concrete", "decisive" — three words, no weights. §10.5
    ranks the influences and still declines to quantify them, so nothing here
    may become a multiplier. See OI-64.
    """
    for entry in INFLUENCE_RANKING:
        assert isinstance(entry["strength"], str)
        assert not any(ch.isdigit() for ch in entry["strength"])
    assert [r["rank"] for r in INFLUENCE_RANKING] == [1, 2, 3]


def test_10_5_argala_closes_the_forward_reference_from_chapter_7():
    """§7.4.6's quick summary listed "Argala sthanas: **Decisive influences**",
    and footnote 18 deferred it to "the chapter on Aspects and Argalas".

    §10.5 uses the same word: "The influence caused by argala is decisive."
    The forward reference resolves, and the two chapters agree.
    """
    from hora.core.const import ARGALA_STHANA_FORWARD_REFERENCE, ARGALA_STHANA_SHOWS

    assert ARGALA_STHANA_SHOWS == "Decisive influences"
    assert "Aspects and Argalas" in ARGALA_STHANA_FORWARD_REFERENCE
    argala = next(r for r in INFLUENCE_RANKING if r["influence"] == "argala")
    assert argala["strength"] == "decisive"
    assert "decisive" in argala["text"]


# --------------------------------------------------------------------------
# Primary and secondary argala
# --------------------------------------------------------------------------


def test_10_5_the_2nd_4th_and_11th_cause_primary_argala():
    """"A planet or house in the 2nd, 4th and 11th houses from a planet or
    house causes **primary** argala on the latter."""
    assert "primary argala" in PRIMARY_ARGALA_RULE
    assert {h for h, k in ARGALA_HOUSE_KIND.items() if k == "primary"} == {2, 4, 11}


def test_10_5_the_5th_causes_secondary_argala():
    """"Apart from the 2nd, 4th and 11th houses from a house, the 5th house
    from a house has a **secondary** argala on it."

    A separate sentence, several paragraphs later, and the only house the
    chapter qualifies. §10.6 then lists all four together — "the 2nd, 4th,
    11th and 5th" — in that order, primary first.
    """
    assert "secondary argala" in SECONDARY_ARGALA_RULE
    assert [h for h, k in ARGALA_HOUSE_KIND.items() if k == "secondary"] == [5]
    assert [a for a, _ in ARGALA_PAIRS] == [2, 4, 11, 5]


def test_10_5_the_kind_is_carried_on_every_row():
    """Not a footnote: each argala the engine returns says whether it is
    primary or secondary, because §10.5 draws the distinction and a reading
    built on the four as equals would be wrong.
    """
    result = argala_service.on_sign(R["Ge"], {Graha.MERCURY: R["Ge"]})
    kinds = {a["house"]: a["argala_kind"] for a in result["argalas"]}
    assert kinds == {2: "primary", 4: "primary", 11: "primary", 5: "secondary"}


def test_10_5_a_virodhargala_inherits_the_kind_it_obstructs():
    """The 9th obstructs the 5th, which is secondary; the other three obstruct
    primary argalas. So the 9th-house obstruction is a secondary matter too,
    and the response says so rather than leaving a caller to derive it.
    """
    result = argala_service.on_sign(R["Ge"], {Graha.MERCURY: R["Ge"]})
    kinds = {v["house"]: v["argala_kind"] for v in result["virodhargalas"]}
    assert kinds == {12: "primary", 10: "primary", 3: "primary", 9: "secondary"}
    for a, v in ARGALA_PAIRS:
        assert ARGALA_HOUSE_KIND[a] == kinds[v]


def test_10_5_the_secondary_argala_still_obstructs_and_is_obstructed():
    """Secondary does not mean exempt. §10.6 pairs the 9th with the 5th like
    any other, and Exercise 16's answer table carries a 9th column."""
    assert (5, 9) in ARGALA_PAIRS
    row = next(h for h in _exercise_16()["houses"] if h["house"] == 5)
    ninth = next(v for v in row["virodhargalas"] if v["house"] == 9)
    assert [ABBR[g["graha_name"]] for g in ninth["grahas"]] == ["Mars", "Sat"]


# --------------------------------------------------------------------------
# 10.5's worked examples
# --------------------------------------------------------------------------


@pytest.mark.parametrize("example", ARGALA_EXAMPLES,
                         ids=[e["matter"][:9] for e in ARGALA_EXAMPLES])
def test_10_5_each_worked_example_counts_correctly(example):
    """"The 2nd, 4th and 11th from the 4th house are 5th, 7th and 2nd houses
    respectively." And for the 3rd house: "the 4th and 6th houses cause argala
    on the 3rd house, being the 2nd and 4th from it".

    Each example's arithmetic is checked rather than trusted.
    """
    for cause in example["causes"]:
        expected = (example["house"] + cause["from_house"] - 2) % 12 + 1
        assert cause["house"] == expected, cause


def test_10_5_the_education_example():
    """"One's intelligence (5th), interaction with others (7th) and overall
    character and samskara (2nd) make or break one education."

    The chapter's argument that the argala houses are not arbitrary: each one
    signifies something that genuinely decides the matter.
    """
    education = ARGALA_EXAMPLES[0]
    assert education["house"] == 4
    assert [c["house"] for c in education["causes"]] == [5, 7, 2]
    assert [c["shows"] for c in education["causes"]] == [
        "intelligence", "interaction with others",
        "overall character and samskara"]
    assert "decisive role" in education["conclusion"]


def test_10_5_the_journey_example_uses_only_two_of_the_three():
    """"the 4th and 6th houses cause argala on the 3rd house, being the 2nd and
    4th from it respectively!"

    The 11th from the 3rd is the 1st, and the chapter simply does not use it
    here. So an example naming fewer than three causes is not an omission —
    it is the chapter choosing what is relevant.
    """
    journey = ARGALA_EXAMPLES[1]
    assert journey["house"] == 3
    assert len(journey["causes"]) == 2
    assert [c["from_house"] for c in journey["causes"]] == [2, 4]
    assert (3 + 11 - 2) % 12 + 1 == 1


def test_10_5_the_same_house_reads_differently_for_different_matters():
    """The 4th house appears twice — education and domestic harmony — with the
    **same** three argala houses and completely different meanings: the 5th is
    intelligence in one and children in the other, the 7th is interaction and
    then a wife.

    So the argala houses are fixed and their meaning is not. Nothing in the
    engine assigns a meaning, and this is why.
    """
    education, _, domestic = ARGALA_EXAMPLES
    assert education["house"] == domestic["house"] == 4
    assert [c["house"] for c in education["causes"]] == \
        [c["house"] for c in domestic["causes"]]
    assert [c["shows"] for c in education["causes"]] != \
        [c["shows"] for c in domestic["causes"]]


def test_10_5_benefic_and_malefic_argala_on_the_same_house():
    """"If Jupiter is in 5th house... his subhargala on 4th will help one's
    education. If Rahu is in 5th house, his papargala on 4th will cause
    obstacles."

    Same house, same argala, opposite reading — decided entirely by the nature
    of the graha sitting there.
    """
    assert "subhargala" in ARGALA_NATURE_EXAMPLE
    assert "papargala" in ARGALA_NATURE_EXAMPLE
    assert ARGALA_BY_NATURE["benefic"]["name"] == "subhaargala"
    assert ARGALA_BY_NATURE["malefic"]["name"] == "paapaargala"
    assert "good and bad intervention" in ARGALA_NATURE_RULE


def test_10_5_spells_both_terms_two_ways():
    """The definitions read "subhaargala" and "paapaargala"; every example
    afterwards reads "subhargala" and "papargala".

    The definitional spellings are kept as primary — §7.5's tie-break rule 2,
    a definitional section beats a passing mention — and the variants are
    recorded so a reader matching text against the book is not surprised.
    """
    assert ARGALA_NATURE_SPELLING_VARIANTS["subhaargala"] == ["subhargala"]
    assert "papargala" in ARGALA_NATURE_SPELLING_VARIANTS["paapaargala"]
    for primary, variants in ARGALA_NATURE_SPELLING_VARIANTS.items():
        assert primary not in variants
        assert all(len(v) < len(primary) for v in variants)


@pytest.mark.parametrize("example", SECONDARY_ARGALA_EXAMPLES,
                         ids=[e["matter"] for e in SECONDARY_ARGALA_EXAMPLES])
def test_10_5_the_secondary_argala_examples(example):
    """"argala of 8th house on 4th (8th is the 5th from 4th) shows the
    influence of hard work in learning... argala of 7th house on 3rd (7th is
    the 5th from 3rd) shows the influence of partners in a journey."""
    assert (example["house"] + 5 - 2) % 12 + 1 == example["causing_house"]
    assert ARGALA_HOUSE_KIND[5] == "secondary"


def test_10_5_the_secondary_examples_extend_the_primary_ones():
    """Both secondary examples reuse a matter the primary examples already
    worked — learning from the 4th, journeys from the 3rd — and add one more
    decider each. So the 5th is presented as a supplement, which is what
    "secondary" means here.
    """
    primary_houses = {e["house"] for e in ARGALA_EXAMPLES}
    assert {e["house"] for e in SECONDARY_ARGALA_EXAMPLES} <= primary_houses
    assert "Hard work is another decider." == SECONDARY_ARGALA_EXAMPLES[0]["note"]


# --------------------------------------------------------------------------
# 10.5 on the endpoints
# --------------------------------------------------------------------------


def test_rules_endpoint_carries_the_10_5_half(client):
    body = client.get("/v1/argala/rules").json()
    assert body["argala_means"] == "a bolt"
    assert "close the bolt on it" in body["argala_definition"]
    assert "primary argala" in body["primary_rule"]
    assert "secondary argala" in body["secondary_rule"]
    assert body["house_kinds"] == {"2": "primary", "4": "primary",
                                   "11": "primary", "5": "secondary"}
    assert [r["strength"] for r in body["influence_ranking"]] == [
        "small", "more concrete", "decisive"]
    assert [p["argala_kind"] for p in body["pairs"]] == [
        "primary", "primary", "primary", "secondary"]


def test_chart_endpoint_marks_primary_and_secondary(client):
    body = client.post("/v1/argala/chart", json={
        "rasis": _navamsa(), "lagna_rasi": R["Sc"]}).json()
    for house in body["houses"]:
        kinds = {a["house"]: a["argala_kind"] for a in house["argalas"]}
        assert kinds == {2: "primary", 4: "primary", 11: "primary",
                         5: "secondary"}


# --------------------------------------------------------------------------
# 10.7 Use of argala
# --------------------------------------------------------------------------


def test_10_7_the_procedure_has_five_steps():
    """"Depending on the matter of interest, take the relevant house or the
    relevant karaka. Find argalas and virodhargalas on it. If there are both,
    see if more planets cause argala or virodhargala. If they are caused by the
    same number of planets, compare the strengths and decide whether argala
    dominates or virodhargala. Based on the signs, houses and planets involved,
    guess the meaning of the argala or virodhargala."

    The first thing in chapter 10 that is a procedure rather than a lookup.
    """
    assert [s["step"] for s in ARGALA_USE_PROCEDURE] == [1, 2, 3, 4, 5]
    assert "relevant house or the relevant karaka" in ARGALA_USE_PROCEDURE[0]["text"]
    assert "more planets cause argala" in ARGALA_USE_PROCEDURE[2]["text"]


def test_10_7_the_engine_performs_the_first_three_steps_only():
    """Steps 1 to 3 are arithmetic. Step 4 needs a strength comparison, and
    step 5 says "**guess**".

    Marked per step rather than left implicit, so a caller can see where the
    computation stops.
    """
    computable = [s["step"] for s in ARGALA_USE_PROCEDURE if s["computable"]]
    assert computable == [1, 2, 3]
    assert "compare the strengths" in ARGALA_USE_PROCEDURE[3]["text"]
    assert "guess" in ARGALA_USE_PROCEDURE[4]["text"]


def test_10_7_step_3_counts_planets_and_names_a_winner():
    """"If there are both, see if more planets cause argala or virodhargala."

    §10.6's own example: Saturn and Venus cause argala on Ge, Jupiter causes
    virodhargala. Two against one, so argala dominates — which is what §10.6
    concluded in words.
    """
    result = argala_service.on_sign(R["Ge"], {
        Graha.MERCURY: R["Ge"], Graha.JUPITER: R["Pi"],
        Graha.VENUS: R["Ar"], Graha.SATURN: R["Vi"]})
    assert result["argala_graha_count"] == 2
    assert result["virodhargala_graha_count"] == 1
    assert result["dominant"] == "argala"
    assert "more planets cause argala" in result["dominance_reason"]


def test_10_7_step_4_stops_rather_than_guessing_a_winner():
    """"If they are caused by the same number of planets, compare the
    strengths and decide whether argala dominates or virodhargala."

    Chapter 15's simple-rules strength measure is not built, so on a tie the
    engine returns no winner and says why. Picking one would invent the
    answer.
    """
    result = argala_service.on_sign(R["Ge"], {
        Graha.MERCURY: R["Ge"], Graha.JUPITER: R["Pi"], Graha.VENUS: R["Ar"]})
    assert result["argala_graha_count"] == result["virodhargala_graha_count"] == 1
    assert result["dominant"] is None
    assert "compare the strengths" in result["dominance_reason"]


def test_10_7_an_empty_target_is_reported_as_neither():
    """No argala and no virodhargala is a third case, distinct from a tie —
    §10.7's step 3 begins "If there are both". Reported separately so a caller
    cannot read absence as a stalemate.
    """
    result = argala_service.on_sign(R["Ge"], {Graha.MERCURY: R["Ge"]})
    assert result["argala_graha_count"] == result["virodhargala_graha_count"] == 0
    assert result["dominant"] is None
    assert "neither argala nor virodhargala" in result["dominance_reason"]


def test_10_7_step_5_guesses_and_the_engine_does_not():
    """"Based on the signs, houses and planets involved, **guess** the meaning
    of the argala or virodhargala."

    The book's own verb. Nothing in the response assigns a meaning to an
    argala.
    """
    result = argala_service.on_sign(R["Ge"], {
        Graha.MERCURY: R["Ge"], Graha.SATURN: R["Vi"]})
    for row in result["argalas"] + result["virodhargalas"]:
        for field in ("meaning", "shows", "signifies", "interpretation"):
            assert field not in row


# --------------------------------------------------------------------------
# 10.7's four roles
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "house,role_fragment",
    [(2, "basic ingredient for the sustenance"),
     (4, "basic factor that drives the mood, state and progress"),
     (11, "catalyst that can result in gains"),
     (5, "additional contributing factors")],
)
def test_10_7_each_argala_house_has_its_own_role(house, role_fragment):
    """"Argala from the 2nd house shows the basic ingredient for the sustenance
    of a matter... from the 4th house shows the basic factor that drives the
    mood, state and progress... from the 11th house shows the catalyst that can
    result in gains... Secondary argala from the 5th house shows the additional
    contributing factors."

    §10.5 showed the four houses matter. §10.7 is the only place that says how
    they differ from one another.
    """
    assert role_fragment in ARGALA_HOUSE_ROLE[house]["role"]


def test_10_7_the_roles_cover_exactly_the_four_argala_houses():
    """No fifth role, and none for a virodhargala house. The roles attach to
    the argala houses alone."""
    assert set(ARGALA_HOUSE_ROLE) == {2, 4, 11, 5}
    assert set(ARGALA_HOUSE_ROLE) == {a for a, _ in ARGALA_PAIRS}
    virodhas = {v for _, v in ARGALA_PAIRS}
    assert not (set(ARGALA_HOUSE_ROLE) & virodhas)


def test_10_7_the_roles_agree_with_10_5s_primary_and_secondary():
    """The 5th's role is the only one qualified as "**Secondary** argala from
    the 5th house", and it is the only one §10.5 calls secondary. The two
    sections agree without either cross-referencing the other.
    """
    for house, entry in ARGALA_HOUSE_ROLE.items():
        assert entry["kind"] == ARGALA_HOUSE_KIND[house], house
    assert ARGALA_HOUSE_ROLE[5]["kind"] == "secondary"
    assert "additional" in ARGALA_HOUSE_ROLE[5]["role"]


def test_10_7_the_roles_are_ordered_by_how_essential_they_are():
    """"basic ingredient" for sustenance, "basic factor" that drives, then a
    "catalyst" for gains, then "additional" contributing factors.

    The 2nd and 4th are both called *basic*; the 11th is a catalyst, which acts
    on a process rather than constituting it; the 5th is merely additional. So
    the wording ranks them, and the ranking matches primary before secondary.
    """
    assert "basic" in ARGALA_HOUSE_ROLE[2]["role"]
    assert "basic" in ARGALA_HOUSE_ROLE[4]["role"]
    assert "basic" not in ARGALA_HOUSE_ROLE[11]["role"]
    assert "additional" in ARGALA_HOUSE_ROLE[5]["role"]


@pytest.mark.parametrize("example", ARGALA_ROLE_EXAMPLES,
                         ids=lambda e: f"{e['from_house']}from{e['target']}")
def test_10_7_each_worked_instance_lands_on_the_house_it_names(example):
    """"the 2nd house shows food and it is a basic ingredient for the
    sustenance of self (1st). The 5th house shows intelligence and it is a
    basic ingredient for the sustenance of learning (4th)."

    Seven instances across the four roles, each checked arithmetically.
    """
    landed = (example["target"] + example["from_house"] - 2) % 12 + 1
    assert landed == example["house"], example


def test_10_7_the_learning_examples_reproduce_10_5s_education_example():
    """§10.5 said the 5th (intelligence), 7th (interaction) and 2nd (character
    and samskara) make or break education, reading from the 4th house.

    §10.7 names the same three houses for the same target and assigns each a
    role: the 5th sustains, the 7th drives, the 2nd catalyses. Two sections,
    the same three houses, and §10.7 explains why each is there.
    """
    education = next(e for e in ARGALA_EXAMPLES if e["matter"] == "education")
    from_10_5 = {c["house"]: c["from_house"] for c in education["causes"]}
    from_10_7 = {e["house"]: e["from_house"]
                 for e in ARGALA_ROLE_EXAMPLES
                 if e["target"] == 4 and e["from_house"] != 5}
    assert from_10_5 == from_10_7 == {5: 2, 7: 4, 2: 11}
    assert ARGALA_HOUSE_ROLE[2]["verb"] == "sustains"
    assert ARGALA_HOUSE_ROLE[4]["verb"] == "drives"
    assert ARGALA_HOUSE_ROLE[11]["verb"] == "catalyses"


def test_10_7_the_meanings_mostly_agree_between_10_5_and_10_7():
    """The 5th shows "intelligence" in both. The 7th shows "interaction with
    others" in §10.5 and "interaction" in §10.7 — the shorter form.

    The 2nd is the interesting one. §10.5: "overall character and samskara".
    §10.7: "character, **grooming** and samskara". §10.7 adds a word §10.5
    does not have, so the two lists are not interchangeable and neither is a
    subset of the other in wording.

    Both are kept as printed. Recorded here so nobody normalises one into the
    other on the assumption that they are the same sentence twice.
    """
    education = next(e for e in ARGALA_EXAMPLES if e["matter"] == "education")
    by_house = {c["house"]: c["shows"] for c in education["causes"]}
    role_by_house = {e["house"]: e["shows"] for e in ARGALA_ROLE_EXAMPLES
                     if e["target"] == 4}

    assert by_house[5] == role_by_house[5] == "intelligence"
    assert by_house[7] == "interaction with others"
    assert role_by_house[7] == "interaction"

    assert by_house[2] == "overall character and samskara"
    assert role_by_house[2] == "character, grooming and samskara"
    shared = {"character", "samskara"}
    assert shared <= set(by_house[2].split())
    assert shared <= {w.strip(",") for w in role_by_house[2].split()}
    assert "grooming" not in by_house[2]


def test_10_7_the_secondary_examples_agree_with_10_5_too():
    """§10.5: "argala of 8th house on 4th ... shows the influence of hard work
    in learning". §10.7: "The 8th house shows hard work and that contributes to
    one's learning". Same house, same matter, same word."""
    hard_work = next(e for e in ARGALA_ROLE_EXAMPLES if e["house"] == 8)
    assert hard_work["shows"] == "hard work"
    assert hard_work["from_house"] == 5
    learning = next(e for e in SECONDARY_ARGALA_EXAMPLES if e["matter"] == "learning")
    assert learning["causing_house"] == 8
    assert "hard work" in learning["shows"]


def test_10_7_the_self_examples_use_the_first_house_as_target():
    """Three of the seven read from the 1st house, where the argala house and
    the house it lands on are the same number — the 2nd from the 1st is the
    2nd. The simplest case, and the one that makes the roles legible.
    """
    self_examples = [e for e in ARGALA_ROLE_EXAMPLES if e["target"] == 1]
    assert len(self_examples) == 3
    for example in self_examples:
        assert example["house"] == example["from_house"]
    assert {e["from_house"] for e in self_examples} == {2, 4, 5}


def test_10_7_no_worked_instance_is_given_for_the_eleventh_from_the_first():
    """The 11th from the 1st is the 11th, and §10.7 gives no example for it —
    its catalyst example reads from the 4th instead. Pinned so the gap is
    known to be the book's, not a transcription loss.
    """
    assert not [e for e in ARGALA_ROLE_EXAMPLES
                if e["target"] == 1 and e["from_house"] == 11]
    catalyst = [e for e in ARGALA_ROLE_EXAMPLES if e["from_house"] == 11]
    assert len(catalyst) == 1
    assert catalyst[0]["target"] == 4


def test_10_7_the_conclusion_covers_houses_and_karakas_both():
    """"Using the above guidelines, we can understand the meaning of argalas on
    houses **and karakas**." — step 1's alternative, restated at the end."""
    assert "houses and karakas" in ARGALA_USE_CONCLUSION


# --------------------------------------------------------------------------
# Argala on a karaka
# --------------------------------------------------------------------------


def test_10_7_argala_on_a_karaka_is_argala_on_its_sign():
    """§10.6: planets in the argala houses "cause argala on Vi **and on the
    planets in Vi**". So a karaka receives whatever its sign receives, and the
    two endpoints must agree exactly.
    """
    rasis = {Graha.MERCURY: R["Ge"], Graha.JUPITER: R["Pi"],
             Graha.VENUS: R["Ar"], Graha.SATURN: R["Vi"]}
    by_karaka = argala_service.on_karaka(Graha.MERCURY, rasis)
    by_sign = argala_service.on_sign(R["Ge"], rasis)
    assert by_karaka["karaka_name"] == "Mercury"
    assert {k: v for k, v in by_karaka.items() if k not in
            ("karaka", "karaka_name")} == by_sign


def test_10_7_two_grahas_in_one_sign_receive_the_same_argala():
    """A consequence of the same rule: co-located karakas cannot differ. Mars
    and Saturn share Scorpio in Chart 5's navamsa.
    """
    rasis = _navamsa()
    mars = argala_service.on_karaka(Graha.MARS, rasis)
    saturn = argala_service.on_karaka(Graha.SATURN, rasis)
    assert mars["argalas"] == saturn["argalas"]
    assert mars["virodhargalas"] == saturn["virodhargalas"]
    assert mars["dominant"] == saturn["dominant"]


def test_10_7_a_karaka_without_a_placement_is_refused():
    """Rather than defaulting to Aries or dropping the graha silently."""
    with pytest.raises(argala_service.InputError, match="no placement"):
        argala_service.on_karaka(Graha.KETU, {Graha.MERCURY: R["Ge"]})


def test_10_7_the_karaka_endpoint_answers_the_10_6_example(client):
    body = client.post("/v1/argala/karaka", json={
        "graha": int(Graha.MERCURY),
        "rasis": {3: R["Ge"], 4: R["Pi"], 5: R["Ar"], 6: R["Vi"]}}).json()
    assert body["karaka_name"] == "Mercury"
    assert body["sign_name"] == "Gemini"
    assert body["dominant"] == "argala"


def test_10_7_the_karaka_endpoint_rejects_an_unplaced_graha(client):
    response = client.post("/v1/argala/karaka", json={
        "graha": int(Graha.KETU), "rasis": {3: R["Ge"]}})
    assert response.status_code == 400
    assert "no placement" in response.json()["error"]["message"]


def test_10_7_the_rules_endpoint_carries_the_procedure_and_roles(client):
    body = client.get("/v1/argala/rules").json()
    assert [s["step"] for s in body["use_procedure"]] == [1, 2, 3, 4, 5]
    assert [s["computable"] for s in body["use_procedure"]] == [
        True, True, True, False, False]
    roles = {r["house"]: r["verb"] for r in body["house_roles"]}
    assert roles == {2: "sustains", 4: "drives", 11: "catalyses",
                     5: "contributes to"}
    assert "houses and karakas" in body["use_conclusion"]
    assert "nothing here guesses" in body["dominance_note"]


def test_10_7_exercise_16_rows_carry_a_dominance_verdict(client):
    """Every house in Exercise 16 gets step 3 applied, so the procedure is
    reachable over a whole chart and not only one target."""
    body = client.post("/v1/argala/chart", json={
        "rasis": _navamsa(), "lagna_rasi": R["Sc"]}).json()
    verdicts = {h["house"]: h["dominant"] for h in body["houses"]}
    assert set(verdicts) == set(range(1, 13))
    assert all(v in (None, "argala", "virodhargala") for v in verdicts.values())
    for house in body["houses"]:
        counted = (house["argala_graha_count"], house["virodhargala_graha_count"])
        if counted[0] == counted[1]:
            assert house["dominant"] is None


# --------------------------------------------------------------------------
# Chart 6 — P.V. Narasimha Rao
# --------------------------------------------------------------------------

#: Chart 6's printed rasi longitudes.
CHART_6 = {
    "Asc": "24 Vi 19", "Sun": "13 Ge 16", "Moon": "10 Pi 33",
    "Mars": "13 Ge 33", "Merc": "27 Ge 40", "Jup": "20 Le 06",
    "Ven": "27 Ar 40", "Sat": "26 Le 26", "Rahu": "0 Li 47",
    "Ketu": "0 Ar 47", "HL": "24 Cp 11", "GL": "25 Sg 59",
}

#: Chart 6's birth data, as printed under the diagram. The offset is 5h17m
#: east, not the 5h30m of modern IST.
CHART_6_BIRTH = {
    "year": 1921, "month": 6, "day": 28, "hour": 12, "minute": 49,
    "second": 0.0, "utc_offset_hours": 5 + 17 / 60,
}
CHART_6_PLACE = {"latitude": 18 + 26 / 60, "longitude": 79 + 9 / 60}

CHART_6_CHARA_KARAKAS = {
    "Rahu": "AK", "Merc": "AmK", "Ven": "BK", "Sat": "MK",
    "Jup": "PiK", "Mars": "PK", "Sun": "GK", "Moon": "DK",
}


def _chart_6_rasis():
    return {int(_NAME_TO_GRAHA[name]): int(lon(text) // 30)
            for name, text in CHART_6.items() if name in _NAME_TO_GRAHA}


def _chart_6_computed(node_type):
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    return compute_chart(
        from_local(**CHART_6_BIRTH),
        Place(name="Chart 6", **CHART_6_PLACE),
        Settings(node_type=node_type),
    )


@pytest.mark.parametrize(
    "body", [b for b in CHART_6 if b in _NAME_TO_GRAHA or b == "Asc"])
def test_chart_6_derives_from_its_own_birth_data(body):
    """Chart 6 is not transcribed — it is **computed** from the birth data
    printed under it: 28 June 1921, 12:49 pm, 5h17m east, 79 E 09, 18 N 26.

    Every body lands within one arcminute of the printed longitude, which is
    the rounding in the book's own display. The nodes need the mean node; see
    `test_chart_6_needs_the_mean_node`.
    """
    from hora.core.const import GRAHA_NAMES
    from hora.core.settings import NodeType

    chart = _chart_6_computed(NodeType.MEAN)
    expected = lon(CHART_6[body])
    if body == "Asc":
        got = chart.lagna_longitude
    else:
        graha = _NAME_TO_GRAHA[body]
        got = next(p.longitude for g, p in chart.positions.items()
                   if GRAHA_NAMES[g] == GRAHA_NAMES[graha])
    assert abs(got - expected) < 1.5 / 60, f"{body}: {got:.4f} vs {expected:.4f}"


def test_chart_6_needs_the_mean_node():
    """**Evidence on a live default.** Under the mean node, Rahu computes to
    0 Li 48 against the printed 0 Li 47 — one arcminute, like every other
    body. Under the true node it computes to 1 Li 26, thirty-nine arcminutes
    out.

    Our default is `node_type = TRUE`. Chart 6 is the first hard evidence in
    the project about which the book uses, and it points the other way. Not
    changed — see OI-68.
    """
    from hora.core.settings import NodeType

    printed = lon(CHART_6["Rahu"])
    mean = _chart_6_computed(NodeType.MEAN).positions[int(Graha.RAHU)].longitude
    true = _chart_6_computed(NodeType.TRUE).positions[int(Graha.RAHU)].longitude
    assert abs(mean - printed) < 1.5 / 60
    assert abs(true - printed) > 30 / 60


def test_chart_6_ketu_is_exactly_opposite_rahu():
    """0 Li 47 and 0 Ar 47 — the printed chart keeps them exactly 180 apart,
    which both node conventions do."""
    assert (lon(CHART_6["Rahu"]) - lon(CHART_6["Ketu"])) % 360 == 180.0


@pytest.mark.parametrize("body,symbol", list(CHART_6_CHARA_KARAKAS.items()))
def test_chart_6_confirms_its_printed_chara_karakas(body, symbol):
    """Chart 6 prints a chara karaka beside each graha. Recomputing them from
    the longitudes with chapter 8's procedure reproduces all eight."""
    from hora.charts.karaka import chara_karakas

    positions = {_NAME_TO_GRAHA[name]: lon(CHART_6[name])
                 for name in CHART_6_CHARA_KARAKAS}
    assigned = {k.graha: k.symbol for k in chara_karakas(positions)}
    assert assigned[_NAME_TO_GRAHA[body]] == symbol


def test_chart_6_is_read_in_the_rasi_chart_not_the_navamsa():
    """Unlike Chart 5's exercises, Example 35 works in the rasi chart: Saturn
    is at 26 Le 26 and the example puts the 11th from him in Gemini, which is
    only true of the rasi positions."""
    saturn = int(lon(CHART_6["Sat"]) // 30)
    assert RASI_ABBR[saturn] == "Le"
    assert RASI_ABBR[(saturn + 10) % 12] == "Ge"


# --------------------------------------------------------------------------
# Example 35
# --------------------------------------------------------------------------


def test_example_35_the_premise_is_not_in_chapter_8():
    """"Saturn is the significator of livelihood and karma."

    Chapter 8 does not say so. Table 15 gives the 10th house — whose §7.2
    signification includes "karma (action)" — to **Mercury**, and Table 16's
    Saturn row lists only the 5th, 6th, 8th and 12th. Neither assigns Saturn
    livelihood or karma.

    Kept as the example's own claim rather than folded into the karaka
    tables. See OI-68.
    """
    from hora.core.const import (
        HOUSE_SIGNIFICATIONS,
        NAISARGIKA_KARAKA,
        NAISARGIKA_KARAKATWAS,
    )

    assert "livelihood and karma" in EXAMPLE_35_PREMISE
    assert NAISARGIKA_KARAKA[10]["graha"] == Graha.MERCURY
    assert "karma (action)" in HOUSE_SIGNIFICATIONS[10]
    saturn_rows = dict(NAISARGIKA_KARAKATWAS[Graha.SATURN])
    assert set(saturn_rows) == {5, 6, 8, 12}
    assert not any("karma" in v or "livelihood" in v
                   for v in saturn_rows.values())


def test_example_35_argala_on_a_karaka_not_a_house():
    """"Argalas on **him** denote decisive influences on livelihood and
    karma."

    On Saturn, not on the 10th house. §10.7 step 1's "or the relevant karaka"
    in use, and the reason `/v1/argala/karaka` exists.
    """
    assert "Argalas on him" in EXAMPLE_35_RULE
    result = argala_service.on_karaka(Graha.SATURN, _chart_6_rasis())
    assert result["karaka_name"] == "Saturn"
    assert result["sign_name"] == "Leo"


def test_example_35_the_stated_answer():
    """"Mercury, Mars and Sun have an argala on Saturn, as they are in the 11th
    from him."

    Saturn is in Leo; the 11th from Leo is Gemini; Gemini holds the Sun at
    13 Ge 16, Mars at 13 Ge 33 and Mercury at 27 Ge 40.
    """
    result = argala_service.on_karaka(Graha.SATURN, _chart_6_rasis())
    eleventh = next(a for a in result["argalas"] if a["house"] == 11)
    assert RASI_ABBR[eleventh["sign"]] == "Ge"
    assert sorted(g["graha_name"] for g in eleventh["grahas"]) == [
        "Mars", "Mercury", "Sun"]
    assert eleventh["argala_kind"] == "primary"


def test_example_35_uses_the_catalyst_role():
    """The 11th is §10.7's catalyst — "the catalyst that can result in gains
    for a matter". So Mercury, Mars and the Sun are catalysts for Saturn's
    livelihood and karma, which fits the example's reading of writing,
    scholarliness and politics as things that *brought* his career about.
    """
    assert ARGALA_HOUSE_ROLE[11]["verb"] == "catalyses"
    assert "gains" in ARGALA_HOUSE_ROLE[11]["role"]


def test_example_35_is_the_only_argala_on_saturn():
    """The 2nd, 4th and 5th from Leo — Virgo, Scorpio and Sagittarius — are
    all empty in Chart 6, so the 11th is the whole of the argala. That is why
    the example names one house and stops.
    """
    result = argala_service.on_karaka(Graha.SATURN, _chart_6_rasis())
    occupied = {a["house"] for a in result["argalas"] if a["present"]}
    assert occupied == {11}


def test_example_35_the_book_does_not_run_step_3_here():
    """What the engine adds beyond the example.

    Rahu is in the 3rd from Saturn and Venus and Ketu in the 9th, so three
    planets cause virodhargala against the three causing argala. §10.7 step 3
    therefore ties, and step 4 — comparing strengths — is not available.

    The example says none of this: it names the argala and reads its meaning.
    Recorded so the engine's extra output is not mistaken for the book's.
    """
    result = argala_service.on_karaka(Graha.SATURN, _chart_6_rasis())
    assert result["argala_graha_count"] == 3
    assert result["virodhargala_graha_count"] == 3
    assert result["dominant"] is None
    assert "compare the strengths" in result["dominance_reason"]
    eleventh = next(a for a in result["argalas"] if a["house"] == 11)
    assert eleventh["obstructed"] is True


def test_example_35_the_third_house_rule_does_not_fire():
    """Rahu alone is in the 3rd from Saturn. One malefic is not "several" on
    any reading, so the obstruction stands as a virodhargala — and would flip
    to an argala only at a threshold of one.
    """
    rasis = _chart_6_rasis()
    result = argala_service.on_karaka(Graha.SATURN, rasis)
    third = next(v for v in result["virodhargalas"] if v["house"] == 3)
    assert [g["graha_name"] for g in third["grahas"]] == ["Rahu"]
    assert third["kind"] == "virodhargala"
    at_one = argala_service.on_karaka(Graha.SATURN, rasis, several=1)
    assert any(a["promoted_from_virodhargala"] for a in at_one["argalas"])


def test_example_35_the_meanings_are_the_books_and_are_not_computed():
    """"Mercury's influence indicates writing and scholarliness. Sun and Mars
    suggest politics."

    §10.7 step 5's "guess", worked. Nothing in the response says any of this —
    the engine names the three grahas and stops.
    """
    result = argala_service.on_karaka(Graha.SATURN, _chart_6_rasis())
    eleventh = next(a for a in result["argalas"] if a["house"] == 11)
    payload = repr(eleventh).lower()
    for word in ("writing", "scholar", "politics", "livelihood"):
        assert word not in payload


def test_example_35_through_the_endpoint(client):
    body = client.post("/v1/argala/karaka", json={
        "graha": int(Graha.SATURN), "rasis": _chart_6_rasis()}).json()
    eleventh = next(a for a in body["argalas"] if a["house"] == 11)
    assert sorted(g["graha_name"] for g in eleventh["grahas"]) == [
        "Mars", "Mercury", "Sun"]
    assert body["dominant"] is None
