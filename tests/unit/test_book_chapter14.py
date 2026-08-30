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


# --------------------------------------------------------------------------
# §14.3 — Rudra, Trishoola and Maheswara
# --------------------------------------------------------------------------

from hora.charts.maraka import (
    maheswara,
    ordinary_eighth,
    rudra_candidates,
    rudra_eighth,
    trishoola_rasis,
)
from hora.core.const import (
    FOOTNOTE_50,
    MAHESWARA_EXAMPLES,
    MAHESWARA_EXCEPTIONS,
    MAHESWARA_NODE_SUBSTITUTES,
    MAHESWARA_USES_THE_ORDINARY_EIGHTH,
    MODALITY_NAMES_EN,
    RASI_MODALITY,
    RUDRA_AFFLICTION_MALEFICS,
    RUDRA_AFFLICTION_RULE,
    RUDRA_STRENGTH_CASCADE,
    SIXTH_IS_THE_ANTIZODIACAL_EIGHTH,
    TABLE_32_CONSTRUCTION,
    TABLE_32_EIGHTH,
)


def test_table_32_covers_every_rasi():
    assert set(TABLE_32_EIGHTH) == set(RASI_ABBR)
    assert set(TABLE_32_EIGHTH.values()) <= set(RASI_ABBR)


def test_footnote_50s_stated_rule_accounts_for_eight_of_the_twelve():
    """"For odd rasis, we count houses zodiacally. For even rasis, we count
    houses anti-zodiacally." That gives eight entries and misses four."""
    follows, breaks = [], []
    for abbr, eighth in TABLE_32_EIGHTH.items():
        sign = R[abbr]
        expected = (sign + 7) % 12 if sign % 2 == 0 else (sign - 7) % 12
        (follows if expected == R[eighth] else breaks).append(abbr)
    assert len(follows) == 8
    assert sorted(breaks) == ["Aq", "Le", "Sc", "Ta"]


def test_the_four_that_break_it_are_exactly_the_fixed_rasis():
    """Which identifies footnote 50's "Shiva rasis". Its Brahma and Vishnu
    rasis are then the movable and dual ones, which do follow the rule."""
    breaks = {abbr for abbr, eighth in TABLE_32_EIGHTH.items()
              if ((R[abbr] + 7) % 12 if R[abbr] % 2 == 0
                  else (R[abbr] - 7) % 12) != R[eighth]}
    fixed = {abbr for abbr in RASI_ABBR
             if MODALITY_NAMES_EN[RASI_MODALITY[R[abbr]]] == "fixed"}
    assert breaks == fixed == {"Ta", "Le", "Sc", "Aq"}
    assert "Shiva rasis" in FOOTNOTE_50
    assert "the fixed rasis" in TABLE_32_CONSTRUCTION


def test_shivas_motion_is_deferred_so_table_32_stays_as_data():
    """Footnote 50 says Shiva's motion "will be discussed in Narayana Dasa",
    so four entries cannot be derived here and the table is transcribed."""
    assert "Narayana Dasa" in FOOTNOTE_50
    assert "held as data" in TABLE_32_CONSTRUCTION


def test_table_32_differs_from_the_ordinary_eighth_in_eight_rasis():
    """§14.3 warns of this outright: "Find the 8th house using Table 32 and
    not in the normal way"."""
    differ = [s for s in range(12) if rudra_eighth(s) != ordinary_eighth(s)]
    assert len(differ) == 8
    assert sorted(RASI_ABBR[s] for s in differ) == [
        "Aq", "Cn", "Cp", "Le", "Pi", "Sc", "Ta", "Vi"]


def test_rudra_has_two_candidates_from_the_lagna_and_the_seventh():
    """"the lord of the 8th house from (i) lagna and (ii) the 7th house"."""
    result = rudra_candidates(R["Le"])
    assert RASI_ABBR[result.from_lagna[0]] == TABLE_32_EIGHTH["Le"] == "Cn"
    assert RASI_ABBR[result.from_seventh[0]] == TABLE_32_EIGHTH["Aq"] == "Cp"
    assert result.from_lagna[1] == int(Graha.MOON)
    assert result.from_seventh[1] == int(Graha.SATURN)


def test_rudra_is_not_decided_without_the_charts_positions():
    """The strength cascade needs them, and the answer says so instead of
    picking one."""
    result = rudra_candidates(R["Le"])
    assert result.rudra is None
    assert result.decided_by is None
    assert "needs the chart's positions" in result.why


def test_the_strength_cascade_is_transcribed_in_order():
    assert len(RUDRA_STRENGTH_CASCADE) == 5
    assert "conjoins more planets" in RUDRA_STRENGTH_CASCADE[0]
    assert "exaltation or own rasi" in RUDRA_STRENGTH_CASCADE[1]
    assert "more advanced in its rasi" in RUDRA_STRENGTH_CASCADE[4]


def test_the_affliction_rule_can_override_the_stronger_planet():
    """"if the weaker planet is debilitated or in an inimical sign and
    conjoined/aspected by malefics ... then it becomes Rudra"."""
    assert "weaker planet is debilitated" in RUDRA_AFFLICTION_RULE
    assert RUDRA_AFFLICTION_MALEFICS == ("Mars", "Saturn", "Rahu", "Ketu")
    assert "Sun" not in RUDRA_AFFLICTION_MALEFICS, "shorter than 14.2's list"


@pytest.mark.parametrize("sign", range(12))
def test_the_three_trishoola_rasis_are_trines_from_rudra(sign):
    trines = trishoola_rasis(sign)
    assert len(set(trines)) == 3
    assert trines[0] == sign
    assert all((t - sign) % 4 == 0 for t in trines)


# -- Maheswara --------------------------------------------------------------

def test_maheswara_uses_the_ordinary_eighth_not_table_32():
    """§14.3's second exception settles it: "AK is Mars and he is in Taurus.
    Then Sg is the 8th house from Mars." The ordinary 8th from Taurus is
    Sagittarius; Table 32 gives Gemini."""
    assert RASI_ABBR[ordinary_eighth(R["Ta"])] == "Sg"
    assert TABLE_32_EIGHTH["Ta"] == "Ge"
    body = maheswara(R["Ta"], {int(Graha.KETU): R["Ar"]})
    assert body["maheswara_name"] == "Jupiter"
    assert "Sagittarius" in body["steps"][0]
    assert "for Rudra only" in MAHESWARA_USES_THE_ORDINARY_EIGHTH


def test_the_first_exceptions_example_cannot_decide_which_eighth():
    """Its Gemini gives Capricorn either way, which is why exception 2 is the
    one that settles it."""
    assert RASI_ABBR[ordinary_eighth(R["Ge"])] == TABLE_32_EIGHTH["Ge"] == "Cp"


def test_maheswara_base_rule_from_an_ak_in_gemini():
    """"the 8th house from AK is Cp and Saturn is Maheswara"."""
    body = maheswara(R["Ge"])
    assert body["maheswara_name"] == "Saturn"
    assert body["house_used"] == 8


def test_exception_1_offers_the_eighth_and_twelfth_lords_from_him():
    """"Saturn is exalted in Li. From Saturn (Li), Venus owns the 8th house
    (Ta) and Mercury owns the 12th house (Vi)." Both are returned, because
    §14.3 asks for the stronger and gives no cascade here."""
    body = maheswara(R["Ge"], {int(Graha.SATURN): R["Li"]})
    assert body["maheswara"] is None
    assert body["needs_strength_comparison"] is True
    assert [(c["graha_name"], c["house"], c["rasi"])
            for c in body["candidates"]] == [
        ("Venus", 8, "Taurus"), ("Mercury", 12, "Virgo")]


@pytest.mark.parametrize("node_sign", ["Ta", "Sg"])
def test_exception_2_reads_the_sixth_when_a_node_joins_ak_or_the_eighth(
        node_sign):
    """"Suppose Ketu is in Ta or Sg" — the AK's own rasi, or the 8th from
    him. Either way the 6th is read and Venus becomes Maheswara."""
    body = maheswara(R["Ta"], {int(Graha.KETU): R[node_sign]})
    assert body["house_used"] == 6
    assert body["maheswara_name"] == "Venus"
    assert "anti-zodiacally" in body["steps"][-1]


def test_exception_2s_equivalence_holds_from_every_rasi():
    """"this is equivalent to taking the 8th lord in the anti-zodiacal
    order." Six forward and eight backward land together, always."""
    for sign in range(12):
        assert (sign + 5) % 12 == (sign - 7) % 12
    assert "anti-zodiacal order" in MAHESWARA_EXCEPTIONS[1]
    assert "same rasi" in SIXTH_IS_THE_ANTIZODIACAL_EIGHTH


def test_exception_2_fires_for_rahu_as_well_as_ketu():
    """"If Rahu or Ketu joins AK or the 8th from him"."""
    for node in (Graha.RAHU, Graha.KETU):
        assert maheswara(R["Ta"], {int(node): R["Ta"]})["house_used"] == 6


def test_exception_3_substitutes_mercury_for_rahu_and_jupiter_for_ketu():
    """A node can only become Maheswara through co-lordship of Scorpio or
    Aquarius, and then it is swapped out."""
    assert MAHESWARA_NODE_SUBSTITUTES == {
        "Rahu": "Mercury", "Ketu": "Jupiter"}
    assert "we take Mercury instead" in MAHESWARA_EXCEPTIONS[2]
    assert "we take Jupiter instead" in MAHESWARA_EXCEPTIONS[2]


def test_without_positions_maheswara_names_the_exceptions_it_could_not_test():
    """Never silently returns the base answer as though it were final."""
    body = maheswara(R["Ge"])
    assert len(body["untested_exceptions"]) == 2
    assert any("exception 1" in note for note in body["untested_exceptions"])
    assert any("exception 2" in note for note in body["untested_exceptions"])


@pytest.mark.parametrize("which,setup,result", MAHESWARA_EXAMPLES,
                         ids=[f"ex{e[0]}-{i}" for i, e
                              in enumerate(MAHESWARA_EXAMPLES)])
def test_each_of_14_3s_worked_examples_is_recorded(which, setup, result):
    assert which in (1, 2)
    assert setup and result


# -- endpoints --------------------------------------------------------------

def test_the_14_3_endpoints(client):
    body = client.get("/v1/marakas/rudra-rules").json()
    assert len(body["table_32"]) == 12
    assert len(body["maheswara_exceptions"]) == 3
    assert len(body["maheswara_examples"]) == 4
    assert "predicting death" in body["framing"]

    rudra = client.get("/v1/marakas/rudra", params={"lagna": R["Le"]}).json()
    assert rudra["candidates"] == ["Moon", "Saturn"]
    assert rudra["rudra"] is None

    trishoola = client.get("/v1/marakas/trishoola",
                           params={"rudra_sign": R["Sc"]}).json()
    assert [t["rasi"] for t in trishoola["trishoola"]] == [
        "Scorpio", "Pisces", "Cancer"]

    mahes = client.post("/v1/marakas/maheswara", json={
        "ak_sign": R["Ta"], "graha_signs": {str(int(Graha.KETU)): R["Sg"]},
    }).json()
    assert mahes["maheswara_name"] == "Venus"
    assert mahes["house_used"] == 6


# --------------------------------------------------------------------------
# §14.4 — The Method of Three Pairs
# --------------------------------------------------------------------------

from fractions import Fraction
from itertools import combinations_with_replacement

from hora.charts.maraka import pair_category, three_pairs
from hora.core.const import (
    LONGEVITY_RANGES,
    PARAMAAYUSH_CAN_EXCEED_THE_RANGE,
    PARAMAAYUSH_ONLY_FOR_THE_SPLIT_CASE,
    TABLE_33_LONGEVITY,
    TABLE_33_PRINTED,
    TABLE_34_FACTORS,
    TABLE_34_PARAMAAYUSH,
    TABLE_34_STRUCTURE,
    THREE_PAIRS,
    THREE_PAIRS_TIEBREAK_RULE,
)

_MODALITIES = ("movable", "fixed", "dual")
#: One rasi of each modality, for building cases by hand.
_OF = {"movable": "Ar", "fixed": "Ta", "dual": "Ge"}


def test_the_three_pairs_are_transcribed_in_order():
    names = [name for name, _ in THREE_PAIRS]
    assert names == ["lagna lord and 8th lord", "Moon and Saturn",
                     "lagna and Horalagna (HL)"]
    assert "Table 32" in THREE_PAIRS[0][1]


def test_table_33_covers_every_possible_pair_of_modalities():
    """Six rows for six unordered pairs, so nothing can fall through."""
    possible = {frozenset(p) for p in
                combinations_with_replacement(_MODALITIES, 2)}
    assert len(possible) == 6
    assert set(TABLE_33_LONGEVITY) == possible
    assert len(TABLE_33_PRINTED) == 3, "printed as three rows of two"


@pytest.mark.parametrize("first,second,expected", [
    ("fixed", "dual", "long"), ("movable", "movable", "long"),
    ("movable", "fixed", "middle"), ("dual", "dual", "middle"),
    ("movable", "dual", "short"), ("fixed", "fixed", "short"),
])
def test_each_row_of_table_33(first, second, expected):
    assert pair_category(R[_OF[first]], R[_OF[second]]) == expected
    assert pair_category(R[_OF[second]], R[_OF[first]]) == expected, \
        "the pair is unordered"


def test_the_three_ranges_tile_zero_to_one_hundred_and_eight():
    assert LONGEVITY_RANGES == {
        "short": (0, 36), "middle": (36, 72), "long": (72, 108)}
    tops = [span[1] for span in LONGEVITY_RANGES.values()]
    assert sorted(tops) == [36, 72, 108]


def test_table_34_is_one_factor_triple_against_the_three_range_tops():
    """Not nine independent numbers. Every cell is the majority category's
    own upper bound times a factor fixed by the odd pair alone — 8/9, 1,
    10/9 — and all nine products are exact integers."""
    for odd, (num, den) in TABLE_34_FACTORS.items():
        for majority, (_low, high) in LONGEVITY_RANGES.items():
            product = Fraction(high * num, den)
            assert product.denominator == 1, (odd, majority)
            assert int(product) == TABLE_34_PARAMAAYUSH[odd][majority]
    assert "8/9" in TABLE_34_STRUCTURE


def test_table_34_is_complete_and_monotone():
    assert set(TABLE_34_PARAMAAYUSH) == {"short", "middle", "long"}
    for row in TABLE_34_PARAMAAYUSH.values():
        assert set(row) == {"short", "middle", "long"}
        assert row["short"] < row["middle"] < row["long"]
    for majority in ("short", "middle", "long"):
        column = [TABLE_34_PARAMAAYUSH[odd][majority]
                  for odd in ("short", "middle", "long")]
        assert column == sorted(column)


def test_the_paramaayush_can_exceed_its_own_categorys_range():
    """Long life is 72-108, yet long over long gives 120. Reported side by
    side rather than reconciled."""
    assert TABLE_34_PARAMAAYUSH["long"]["long"] == 120
    assert LONGEVITY_RANGES["long"][1] == 108
    assert "not a reading of the same range" in PARAMAAYUSH_CAN_EXCEED_THE_RANGE


def _chart(lagna: str, lagna_lord_sign: str, eighth_lord_sign: str,
           moon_sign: str, saturn_sign: str, hl_sign: str) -> dict:
    from hora.charts.maraka import rudra_eighth
    from hora.core.const import RASI_LORD

    lagna_i = R[lagna]
    lord = int(RASI_LORD[lagna_i])
    eighth_lord = int(RASI_LORD[rudra_eighth(lagna_i)])
    signs = {int(g): R["Ar"] for g in
             (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
              Graha.JUPITER, Graha.VENUS, Graha.SATURN)}
    signs[lord] = R[lagna_lord_sign]
    signs[eighth_lord] = R[eighth_lord_sign]
    signs[int(Graha.MOON)] = R[moon_sign]
    signs[int(Graha.SATURN)] = R[saturn_sign]
    return three_pairs(lagna_i, signs, R[hl_sign])


def test_the_first_pair_uses_table_32s_eighth_not_the_ordinary_one():
    """§14.4 says so in its own parenthesis, and it names the same table
    Rudra uses."""
    from hora.charts.maraka import ordinary_eighth, rudra_eighth

    body = _chart("Le", "Le", "Ar", "Ar", "Ar", "Ar")
    assert body["eighth_house"]["by"] == "Table 32"
    assert body["eighth_house"]["rasi"] == "Cancer"
    assert RASI_ABBR[rudra_eighth(R["Le"])] == "Cn"
    assert RASI_ABBR[ordinary_eighth(R["Le"])] == "Pi"


def test_all_three_pairs_agreeing_gives_that_category_and_no_paramaayush():
    """§14.4 gives Table 34 for the split case only, and the table's shape
    needs an odd pair. With none, no paramaayush is stated."""
    body = _chart("Ar", "Ar", "Cn", "Cn", "Li", "Cp")
    assert {p["category"] for p in body["pairs"]} == {"long"}
    assert body["category"] == "long"
    assert body["paramaayush_years"] is None
    assert "no odd pair" in body["paramaayush_note"]
    assert "gives no paramaayush when all three pairs agree" \
        in PARAMAAYUSH_ONLY_FOR_THE_SPLIT_CASE


def test_two_against_one_takes_the_majority_and_reads_table_34():
    body = _chart("Le", "Le", "Ar", "Ar", "Cn", "Ge")
    categories = [p["category"] for p in body["pairs"]]
    assert sorted(categories) == ["long", "long", "middle"]
    assert body["category"] == "long"
    assert body["paramaayush_years"] == TABLE_34_PARAMAAYUSH["middle"]["long"]
    assert body["paramaayush_years"] == 108


def test_three_different_results_prefer_the_lagna_and_horalagna_pair():
    """"we should give preference to the third pair of lagna and horalagna"."""
    body = _chart("Ta", "Ar", "Ar", "Ar", "Ta", "Ta")
    categories = [p["category"] for p in body["pairs"]]
    assert sorted(categories) == ["long", "middle", "short"]
    assert body["category"] == body["pairs"][2]["category"]
    assert "lagna and Horalagna" in body["reason"]
    assert body["paramaayush_years"] is None


def test_a_moon_on_the_lagna_axis_flips_the_preference_to_the_second_pair():
    """"However, if Moon is in lagna or the 7th house, then the second pair of
    Moon and Saturn should be given preference"."""
    assert "Moon is in lagna or the 7th house" in THREE_PAIRS_TIEBREAK_RULE
    for moon, where in (("Ar", "lagna"), ("Li", "the 7th house")):
        body = _chart("Ar", "Ta", "Ge", moon, "Cn", "Ge")
        if len({p["category"] for p in body["pairs"]}) != 3:
            continue
        assert body["category"] == body["pairs"][1]["category"]
        assert where in body["reason"]


def test_the_method_refuses_a_chart_missing_a_planet_it_needs():
    """Never guesses a position it was not given."""
    with pytest.raises(MarakaError, match="needs"):
        three_pairs(R["Le"], {int(Graha.MOON): R["Ar"]}, R["Ge"])


@pytest.mark.parametrize("lagna", range(12))
def test_every_lagna_yields_three_pairs_and_one_category(lagna):
    signs = {int(g): (lagna + i) % 12 for i, g in enumerate(
        (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
         Graha.JUPITER, Graha.VENUS, Graha.SATURN))}
    body = three_pairs(lagna, signs, (lagna + 3) % 12)
    assert len(body["pairs"]) == 3
    assert body["category"] in LONGEVITY_RANGES
    assert body["reason"]
    if body["paramaayush_years"] is None:
        assert body["paramaayush_note"]
    else:
        assert body["paramaayush_note"] is None


def test_a_co_owned_eighth_house_reports_both_lords():
    """Table 32 sends Aries to Scorpio and Virgo to Aquarius, both co-owned.
    §14.4 does not address co-lordship, so both are named and the primary is
    the one used."""
    body = _chart("Ar", "Ar", "Ar", "Ar", "Ar", "Ar")
    assert body["eighth_house"]["rasi"] == "Scorpio"
    assert body["eighth_house"]["lords"] == ["Mars", "Ketu"]
    assert body["eighth_house"]["lord_used"] == "Mars"


def test_the_longevity_endpoints(client):
    body = client.get("/v1/marakas/longevity-rules").json()
    assert len(body["table_33"]) == 3
    assert body["table_34"]["long"]["long"] == 120
    assert body["table_34_factors"] == {
        "short": [8, 9], "middle": [1, 1], "long": [10, 9]}
    assert "Table 32" in body["eighth_uses_table_32"]
    assert "predicting death" in body["framing"]

    result = client.post("/v1/marakas/longevity", json={
        "lagna": R["Le"],
        "graha_signs": {"0": R["Le"], "1": R["Ar"], "2": R["Cn"],
                        "3": R["Vi"], "4": R["Sg"], "5": R["Ta"],
                        "6": R["Cp"]},
        "hl_sign": R["Ge"],
    }).json()
    assert result["category"] == "long"
    assert result["paramaayush_years"] == 108
    assert "predicting death" in result["framing"]


# --------------------------------------------------------------------------
# Example 47 — §14.4 worked through
# --------------------------------------------------------------------------

from hora.core.const import (
    EXAMPLE_47_CATEGORY,
    EXAMPLE_47_CHART,
    EXAMPLE_47_COVERS,
    EXAMPLE_47_PAIRS,
    EXAMPLE_47_PARAMAAYUSH,
)


def _example_47() -> dict:
    signs = {
        int(Graha.MOON): R[EXAMPLE_47_CHART["Moon"]],
        int(Graha.MERCURY): R[EXAMPLE_47_CHART["Merc"]],
        int(Graha.VENUS): R[EXAMPLE_47_CHART["Ven"]],
        int(Graha.SATURN): R[EXAMPLE_47_CHART["Sat"]],
    }
    return three_pairs(R[EXAMPLE_47_CHART["Lagna"]], signs,
                       R[EXAMPLE_47_CHART["HL"]])


def test_example_47s_eighth_house_comes_from_table_32():
    """"The 8th house is in Ge (see Table 32) and Mercury owns it." The
    ordinary 8th from Taurus is Sagittarius, so the example would have named
    Jupiter had it counted the usual way."""
    from hora.charts.maraka import ordinary_eighth

    body = _example_47()
    assert body["eighth_house"]["rasi"] == "Gemini"
    assert body["eighth_house"]["lord_used"] == "Mercury"
    assert RASI_ABBR[ordinary_eighth(R["Ta"])] == "Sg"


@pytest.mark.parametrize(
    "number,working,combination,result", EXAMPLE_47_PAIRS,
    ids=[f"pair{p[0]}" for p in EXAMPLE_47_PAIRS])
def test_each_of_example_47s_three_pairs(number, working, combination,
                                         result):
    """The modalities the example names, and the Table 33 row it looks up."""
    pair = _example_47()["pairs"][number - 1]
    assert pair["category"] == result
    printed = {word.strip().lower() for word in combination.split("+")}
    assert set(pair["modalities"]) == printed
    assert working


def test_example_47_combines_to_long_life_with_a_paramaayush_of_108():
    """Two pairs long and one middle, so long dominates and the paramaayush
    is 108 years."""
    body = _example_47()
    assert [p["category"] for p in body["pairs"]] == ["long", "long", "middle"]
    assert body["category"] == EXAMPLE_47_CATEGORY == "long"
    assert body["paramaayush_years"] == EXAMPLE_47_PARAMAAYUSH == 108
    assert body["range_years"] == [72, 108]


def test_example_47s_paramaayush_is_table_34s_middle_over_long_cell():
    """The odd pair is middle and the majority is long, so the figure comes
    from the row and column the combination rule picks — not from anywhere
    else in the table."""
    assert TABLE_34_PARAMAAYUSH["middle"]["long"] == 108
    assert _example_47()["paramaayush_years"] == \
        TABLE_34_PARAMAAYUSH["middle"]["long"]


def test_example_47_is_the_only_branch_of_14_4_the_book_works():
    """It exercises two-against-one. The unanimous and three-way-split
    branches have no worked example — see OI-110."""
    assert "two-against-one" in EXAMPLE_47_COVERS
    assert "only branch" in EXAMPLE_47_COVERS


def test_the_longevity_rules_endpoint_carries_example_47(client):
    body = client.get("/v1/marakas/longevity-rules").json()["example_47"]
    assert body["category"] == "long"
    assert body["paramaayush_years"] == 108
    assert len(body["pairs"]) == 3
    assert body["chart"]["Lagna"] == "Ta"
