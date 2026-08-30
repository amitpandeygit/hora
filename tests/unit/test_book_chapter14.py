"""Chapter 14 — topics related to longevity.

Section 14.2's marakas. The chapter's own framing on how the subject is used
is transcribed and served with every answer; it is the book's paragraph and
the first thing the chapter says.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.maraka import (
    MALEFICS,
    MarakaError,
    additional_marakas,
    houses_of_life,
    maraka_grahas,
    maraka_houses,
    maraka_sthanas,
    marakas,
)
from hora.core.const import (
    ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED,
    ADDITIONAL_MARAKA_RULE,
    ADDITIONAL_MARAKA_TARGETS,
    CHAPTER_14_INTRO,
    CHAPTER_14_NOT_COVERED,
    CHAPTER_14_SCOPE,
    GOOD_LONGEVITY_RULE,
    HOUSES_OF_LIFE,
    MARAKA_CHART_ORDER,
    MARAKA_DERIVATION,
    MARAKA_EXAMPLES,
    MARAKA_HOUSES,
    MARAKA_STRONGER_NOT_A_RULE,
    MARAKA_STRONGER_REMARK,
    MARAKA_USE,
    RASI_ABBR,
    RASI_LORD,
    Graha,
)

R = {name: index for index, name in enumerate(RASI_ABBR)}
G = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
     "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
     "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU}


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# --------------------------------------------------------------------------
# §14.1 — what the chapter says about itself
# --------------------------------------------------------------------------

def test_the_chapters_own_framing_is_transcribed_whole():
    """§14.1's first paragraph, not paraphrased and not dropped."""
    assert "will not scare a client by predicting death" in CHAPTER_14_INTRO
    assert "caution a client gently before critical periods" in CHAPTER_14_INTRO
    assert "helpful in matchmaking" in CHAPTER_14_INTRO


def test_the_chapter_states_what_it_does_not_cover():
    assert "will not be covered in this book" in CHAPTER_14_SCOPE
    assert len(CHAPTER_14_NOT_COVERED) == 2
    what = {item for item, _ in CHAPTER_14_NOT_COVERED}
    assert "ashtakavarga longevity formulas" in what
    assert "dasas other than Shoola dasa" in what


def test_the_three_charts_in_the_order_14_2_weights_them():
    assert [code for code, _ in MARAKA_CHART_ORDER] == ["D1", "D11", "D30"]
    assert "most important chart is the rasi chart" in MARAKA_CHART_ORDER[0][1]


# --------------------------------------------------------------------------
# §14.2 — the derivation
# --------------------------------------------------------------------------

def test_the_houses_of_life_are_the_third_and_the_eighth():
    assert set(houses_of_life()) == {3, 8}
    assert HOUSES_OF_LIFE[3] == "the vitality of one's existence"
    assert HOUSES_OF_LIFE[8] == "the longevity"


def test_the_maraka_houses_are_derived_as_the_twelfth_from_each():
    """§14.2 does not assert the 2nd and 7th — it derives them. "The 12th
    house from any house shows losses related to the matters signified by
    that house." The 12th from the 3rd is the 2nd; from the 8th, the 7th."""
    for life, death in MARAKA_DERIVATION:
        assert ((life + 12 - 2) % 12) + 1 == death
    assert maraka_houses() == (2, 7)


def test_the_derivation_confirms_chapter_11s_bare_label():
    """Chapter 11 carried MARAKA_HOUSES = (2, 7) as a label with no reasoning
    behind it — that was OI-23. Chapter 14 supplies the reasoning, and the two
    agree."""
    assert tuple(sorted(MARAKA_HOUSES)) == maraka_houses()


def test_good_longevity_wants_the_life_houses_strong_and_the_death_ones_weak():
    assert "3rd and 8th houses and their lords should be strong" \
        in GOOD_LONGEVITY_RULE
    assert "2nd and 7th houses and their lords should be weak" \
        in GOOD_LONGEVITY_RULE


# --------------------------------------------------------------------------
# Sthanas and grahas
# --------------------------------------------------------------------------

@pytest.mark.parametrize("lagna", range(12))
def test_every_lagna_has_two_maraka_sthanas_and_they_are_rasis(lagna):
    sthanas = maraka_sthanas(lagna)
    assert set(sthanas) == {2, 7}
    assert sthanas[2] == (lagna + 1) % 12
    assert sthanas[7] == (lagna + 6) % 12


@pytest.mark.parametrize("lagna", range(12))
def test_every_maraka_house_yields_at_least_one_lord(lagna):
    """Two when the house falls in Scorpio or Aquarius."""
    lords = maraka_grahas(lagna)
    for house, owners in lords.items():
        assert 1 <= len(owners) <= 2
        sign = maraka_sthanas(lagna)[house]
        assert int(RASI_LORD[sign]) in owners


def test_a_co_owned_maraka_house_yields_both_lords_and_says_so():
    """Leo's 7th is Aquarius. §14.2's first example names only Saturn and
    does not discuss co-lordship, so Rahu is included and labelled rather
    than assumed away."""
    body = marakas(R["Le"])
    saturn = next(m for m in body["maraka_grahas"]
                  if m["graha"] == int(Graha.SATURN))
    rahu = next(m for m in body["maraka_grahas"]
                if m["graha"] == int(Graha.RAHU))
    assert "as co-lord" in saturn["reasons"][0]
    assert "as co-lord" in rahu["reasons"][0]


# --------------------------------------------------------------------------
# The two worked examples
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "lagna,positions,expected", MARAKA_EXAMPLES,
    ids=[e[0] for e in MARAKA_EXAMPLES])
def test_14_2s_worked_examples_name_marakas_we_also_find(
        lagna, positions, expected):
    """The book names the marakas it is illustrating, not every one that
    qualifies — its first example gives positions for only two planets. So
    each named maraka must be among ours, with the same reason."""
    signs = {int(G[name]): R[sign] for name, sign in positions.items()}
    found = {m["graha_name"]: m for m in
             marakas(R[lagna], signs)["maraka_grahas"]}
    for name, _why in expected:
        assert name in found, name


def test_example_1s_saturn_qualifies_by_owning_the_seventh():
    """Lagna Le, so the 7th is Aquarius and Saturn owns it."""
    signs = {int(G["Sat"]): R["Sg"], int(G["Mars"]): R["Ge"]}
    body = marakas(R["Le"], signs)
    saturn = next(m for m in body["maraka_grahas"]
                  if m["graha_name"] == "Saturn")
    assert saturn["kind"] == "house lord"
    assert "owns the 7th house (Aquarius)" in saturn["reasons"][0]


def test_example_1s_mars_qualifies_by_two_aspects_and_owns_nothing():
    """"He aspects the 2nd house (Vi, with the 4th house aspect) and the 7th
    lord (Saturn in Sg — with the 7th house aspect)." Both, and no lordship."""
    signs = {int(G["Sat"]): R["Sg"], int(G["Mars"]): R["Ge"]}
    body = marakas(R["Le"], signs)
    mars = next(m for m in body["maraka_grahas"] if m["graha_name"] == "Mars")
    assert mars["kind"] == "malefic contact"
    assert set(mars["reasons"]) == {
        "aspects the 2nd house (Virgo)", "aspects the 7th lord Saturn"}
    assert (R["Ge"] + 3) % 12 == R["Vi"], "Mars's 4th aspect"
    assert (R["Ge"] + 6) % 12 == R["Sg"], "Mars's 7th aspect"


def test_example_2s_three_marakas_and_how_each_qualifies():
    """Mars and Mercury own the 2nd and 7th; Saturn reaches both lords and
    sits in the 2nd house."""
    signs = {int(G["Mars"]): R["Ge"], int(G["Merc"]): R["Cp"],
             int(G["Sat"]): R["Ar"]}
    body = marakas(R["Pi"], signs)
    found = {m["graha_name"]: m for m in body["maraka_grahas"]}
    assert set(found) == {"Mars", "Mercury", "Saturn"}
    assert found["Mars"]["kind"] == found["Mercury"]["kind"] == "house lord"
    assert found["Saturn"]["kind"] == "malefic contact"
    assert set(found["Saturn"]["reasons"]) == {
        "conjoins the 2nd house (Aries)",
        "aspects the 2nd lord Mars",
        "aspects the 7th lord Mercury"}
    assert (R["Ar"] + 2) % 12 == R["Ge"], "Saturn's 3rd aspect reaches Mars"
    assert (R["Ar"] + 9) % 12 == R["Cp"], "Saturn's 10th reaches Mercury"


def test_a_planet_never_qualifies_by_reaching_itself():
    """Example 2's Mars owns the 2nd and sits in Gemini. He must not be
    credited with "conjoins the 2nd lord Mars"."""
    signs = {int(G["Mars"]): R["Ge"], int(G["Merc"]): R["Cp"],
             int(G["Sat"]): R["Ar"]}
    mars = next(m for m in marakas(R["Pi"], signs)["maraka_grahas"]
                if m["graha_name"] == "Mars")
    assert not any("lord Mars" in reason and "conjoins" in reason
                   for reason in mars["reasons"])


def test_only_graha_drishti_qualifies_an_additional_maraka():
    """§14.2 says "using graha drishti" outright, so a rasi drishti contact
    alone does not make a maraka."""
    assert "using graha drishti" in ADDITIONAL_MARAKA_RULE
    import inspect

    from hora.charts import maraka as module

    source = inspect.getsource(module)
    assert "rasi_drishti" not in source
    assert "graha_aspects_sign" in source


def test_a_benefic_never_becomes_an_additional_maraka():
    """The rule is "if a **malefic** planet ...". Jupiter and Venus cannot
    qualify this way however they are placed."""
    for sign in range(12):
        signs = {int(G["Jup"]): sign, int(G["Ven"]): sign}
        assert additional_marakas(R["Pi"], signs) == {}
    assert int(Graha.JUPITER) not in MALEFICS
    assert int(Graha.VENUS) not in MALEFICS


def test_the_moon_and_mercury_are_not_assumed_malefic():
    """Their natures are conditional — the Moon's on his phase, Mercury's on
    his association — and neither example uses either. See OI-105."""
    assert int(Graha.MOON) not in MALEFICS
    assert int(Graha.MERCURY) not in MALEFICS
    assert MALEFICS == frozenset({
        int(Graha.SUN), int(Graha.MARS), int(Graha.SATURN),
        int(Graha.RAHU), int(Graha.KETU)})


# --------------------------------------------------------------------------
# What §14.2 leaves open
# --------------------------------------------------------------------------

def test_powerfully_is_never_quantified_so_nothing_is_filtered_on_it():
    """OI-108. Both worked examples simply note the contacts and conclude."""
    assert "powerfully" in ADDITIONAL_MARAKA_RULE
    assert "does not say what makes the contact powerful" \
        in ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED
    assert "do not filter" in ADDITIONAL_MARAKA_POWERFULLY_UNDEFINED


def test_marakas_are_not_ranked_because_14_2_gives_no_rule_for_it():
    """It remarks that Saturn "may in fact be a stronger maraka" and stops."""
    assert "may in fact be a stronger maraka" in MARAKA_STRONGER_REMARK
    assert "gives no rule for ranking" in MARAKA_STRONGER_NOT_A_RULE


def test_without_positions_the_answer_says_the_list_is_incomplete():
    """Never implies the house lords are all there is."""
    body = marakas(R["Le"])
    assert body["malefic_contacts_included"] is False
    assert "needs the chart's graha positions" in body["incomplete_note"]

    with_positions = marakas(R["Le"], {int(G["Mars"]): R["Ge"]})
    assert with_positions["malefic_contacts_included"] is True
    assert with_positions["incomplete_note"] is None


def test_the_four_things_an_additional_maraka_can_reach():
    assert ADDITIONAL_MARAKA_TARGETS == (
        "the 2nd house", "the 7th house", "the 2nd lord", "the 7th lord")


def test_an_out_of_range_lagna_or_position_is_refused():
    from hora.core.validate import InputError

    with pytest.raises(InputError):
        maraka_sthanas(12)
    with pytest.raises(InputError):
        additional_marakas(0, {int(G["Sat"]): 12})
    assert issubclass(MarakaError, InputError)


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------

def test_every_answer_carries_the_chapters_own_framing(client):
    body = client.post("/v1/marakas", json={"lagna": R["Le"]}).json()
    assert "will not scare a client by predicting death" in body["framing"]
    assert body["use"] == MARAKA_USE


def test_the_endpoint_reproduces_the_second_worked_example(client):
    body = client.post("/v1/marakas", json={
        "lagna": R["Pi"],
        "graha_signs": {str(int(G["Mars"])): R["Ge"],
                        str(int(G["Merc"])): R["Cp"],
                        str(int(G["Sat"])): R["Ar"]},
    }).json()
    assert {m["graha_name"] for m in body["maraka_grahas"]} == {
        "Mars", "Mercury", "Saturn"}
    assert [s["rasi_name"] for s in body["maraka_sthanas"]] == [
        "Aries", "Virgo"]


def test_the_rules_endpoint_carries_chapter_14(client):
    body = client.get("/v1/marakas/rules").json()
    assert body["maraka_houses"] == [2, 7]
    assert len(body["examples"]) == 2
    assert len(body["not_covered"]) == 2
    assert body["malefics"] == ["Ketu", "Mars", "Rahu", "Saturn", "Sun"]
    assert "predicting death" in body["framing"]
