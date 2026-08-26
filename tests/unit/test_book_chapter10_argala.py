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
    ARGALA_IS_ADDITIONAL,
    ARGALA_IS_IMPORTANT,
    ARGALA_MEANS,
    ARGALA_NATURE_EXAMPLE,
    ARGALA_NATURE_RULE,
    ARGALA_NATURE_SPELLING_VARIANTS,
    ARGALA_PAIRS,
    ASPECT_SOURCE,
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
