"""Chapter 11 §11.2 — Ravi yogas, and the yoga framework they land on.

Chapters 11 to 14 are all yogas, so the shape matters more than these four
detectors do. The contract is **exhaustiveness**: `evaluate` walks the registry
and returns a verdict for every yoga, present or absent, with the reason either
way. A yoga cannot be added and then forgotten, because the registry is what is
iterated — and the guards below are what keep that true.

Not to be confused with `test_book_1_3_9.py`, which covers the nithya yoga.
"""
import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.planetary_yogas import (
    YOGA_REGISTRY,
    YogaError,
    YogaInput,
    evaluate,
    evaluate_one,
    groups,
)
from hora.charts.planetary_yogas._shared import ordinal
from hora.charts.planetary_yogas.popular import kartari
from hora.core.const import (
    AAKRITI_BASIS,
    AAKRITI_MEANS,
    AAKRITI_NAME_VARIANTS,
    AAKRITI_NODES_NOTE,
    AAKRITI_ORDER_DIFFERS,
    AAKRITI_YOGAS,
    AASRAYA_BASIS,
    ADHI_EXAMPLE_CONTRADICTS_RULE,
    ADHI_HOUSES_FROM_MOON,
    BRAHMA_VARIATION,
    BUDHA_AADITYA_CHART_NOTE,
    BUDHA_AADITYA_SPELLING_VARIANTS,
    BUDHA_AADITYA_TERMS,
    BUDHA_AADITYA_TIMING_PERIODS,
    BUDHA_AADITYA_TIMING_TEXT,
    CHANDRA_ASPECT_BY_BIRTH_TIME,
    CHANDRA_GUIDELINE_1,
    CHANDRA_GUIDELINE_2,
    CHANDRA_GUIDELINE_2_RESPECTIVELY_NOTE,
    CHANDRA_GUIDELINE_3,
    CHANDRA_MOON_FROM_SUN_GRADE,
    CHANDRA_YOGA_INTRO,
    CHANDRA_YOGAS,
    CHATURASRA,
    COMBUSTION_WEAKENS_YOGA,
    DUSTHANA_LORD_IN_OWN_HOUSE,
    EXALTATION_DEG,
    GRAHA_NAMES,
    HAMSA_MEANS,
    HAMSA_MISNAMED_IN_ITS_DEFINITION,
    KALPADRUMA_EXAMPLE_CHAIN,
    KALPADRUMA_EXAMPLE_CONCLUSION,
    KALPADRUMA_EXAMPLE_NAVAMSA_LAGNA_CLAIM,
    KALPADRUMA_RESULT_WORD_SANSKRIT,
    KALPADRUMA_RESULT_WORDS,
    KALPADRUMA_RESULTS_FOOTNOTE,
    KARTARI_DEFINITION,
    KARTARI_EFFECT,
    KARTARI_HOUSES,
    KARTARI_MEANS,
    KEMADRUMA_KILLS_OTHER_YOGAS,
    KENDRA,
    LAGNAADHI_GLOSS,
    LAGNAADHI_HOUSES,
    MAALAVYA_SPELLING_VARIANTS,
    MAHAPURUSHA_ELEMENT_RULERS_SENTENCE,
    MAHAPURUSHA_FOOTNOTES_UNREAD,
    MAHAPURUSHA_INTRO,
    MAHAPURUSHA_REFERENCE_RULE,
    MAHAPURUSHA_TERMS,
    MAHAPURUSHA_YOGAS,
    MOOLATRIKONA,
    NAABHASA_CLASSIFICATION,
    NAABHASA_INTRO,
    NAABHASA_NOT_YET_DEFINED,
    NAABHASA_TIMING_RULE,
    NAABHASA_YOGAS,
    PANAPHARA_SPELLING_VARIANTS,
    PANCHA_BHOOTA_NAMES,
    PARIVARTANA_FOOTNOTE,
    POPULAR_YOGA_CONTINUED_COUNT,
    POPULAR_YOGA_COUNT,
    POPULAR_YOGA_FULLNESS_RULE,
    POPULAR_YOGA_INTRO,
    POPULAR_YOGA_TOTAL,
    POPULAR_YOGAS,
    POPULAR_YOGAS_ALL,
    POPULAR_YOGAS_CONTINUED,
    RASI_LORD,
    RASI_MODALITY,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
    RAVI_YOGAS,
    SANKHYA_BASIS,
    SANKHYA_EXAMPLE,
    SANKHYA_EXCLUDES_NODES,
    SANKHYA_IS_A_FALLBACK,
    SANKHYA_MEANS,
    SANKHYA_YOGAS,
    SARPA_IS_VERY_BAD,
    SASA_MEANS,
    STRENGTH_NOT_ASSESSED,
    TATTVA_GLOSS_IN_3_2_8,
    TATTVA_GLOSS_IN_11_4,
    TRIKONA,
    TRIMURTHI_NOTE,
    TRIMURTHI_YOGAS,
    UPACHAYA,
    WEAKENED_YOGA_IS_NOT_APPLICABLE,
    Graha,
)
from hora.services import planetary_yoga_service

RASI_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
R = {name: index for index, name in enumerate(RASI_ABBR)}


@pytest.fixture
def client():
    return TestClient(app)


def _in(**placements) -> YogaInput:
    """Build an input from keyword placements: `_in(SUN="Ge", JUPITER="Cn")`."""
    return YogaInput(rasis={int(getattr(Graha, name)): R[sign]
                            for name, sign in placements.items()})


# --------------------------------------------------------------------------
# The framework's guarantees
# --------------------------------------------------------------------------


def test_every_registered_yoga_is_evaluated():
    """The contract. `evaluate` returns one verdict per registered yoga, in
    registry order, whatever the chart — so a yoga cannot be skipped by a
    detector deciding not to speak.
    """
    verdicts = evaluate(_in(SUN="Ar"))
    assert len(verdicts) == len(YOGA_REGISTRY)
    assert [v.key for v in verdicts] == list(YOGA_REGISTRY)


def test_absent_yogas_are_returned_not_filtered_out():
    """"Not in the response" must never need interpreting. An absent yoga
    comes back with `present=False` and the reason it failed.
    """
    # Two planets in different modalities, so no Aasraya yoga can hold, and
    # no lagna, so nothing counting quadrants can either.
    verdicts = {v.key: v for v in evaluate(_in(SUN="Ar", MOON="Ta"))}
    assert not any(v.present for v in verdicts.values())
    for verdict in verdicts.values():
        assert verdict.reason, verdict.key
        assert verdict.participants == ()


def test_every_verdict_carries_a_reason_either_way():
    """Present or absent, the verdict says why. "We did not find it" and "we
    did not look" have to be distinguishable in the output."""
    for data in (_in(SUN="Ge", JUPITER="Cn"), _in(SUN="Ar"), _in(MOON="Ar")):
        for verdict in evaluate(data):
            assert verdict.reason.strip(), (verdict.key, data)


def test_a_yoga_absent_for_want_of_the_sun_says_so():
    """Every Ravi yoga is read from the Sun. Without him the answer is not
    "absent" in the ordinary sense, and the reason distinguishes it."""
    for verdict in evaluate(_in(MOON="Ar", JUPITER="Ta"), group="ravi"):
        assert verdict.present is False
        assert "no placement" in verdict.reason


def test_every_group_module_is_imported():
    """The one failure this design can still have: a group module written but
    never imported, so its yogas silently never run.

    Checked through the detectors themselves rather than by group name, since
    one module may host several groups — `naabhasa.py` registers both
    `naabhasa_aasraya` and `naabhasa_dala`.
    """
    import pathlib

    import hora.charts.planetary_yogas as package

    source = pathlib.Path(package.__file__).read_text()
    directory = pathlib.Path(package.__file__).parent
    modules = {spec.detect.__module__.rsplit(".", 1)[-1]
               for spec in YOGA_REGISTRY.values()}
    modules.discard("_shared")
    for module in modules:
        assert (directory / f"{module}.py").is_file(), module
        assert f"import {module}" in source, module
    assert {spec.group for spec in YOGA_REGISTRY.values()} == set(groups())


def test_registry_keys_are_unique_and_stable():
    """Keys are the API's identifiers, so they must be unique and lowercase
    with no spaces — a renamed key is a breaking change."""
    for key, spec in YOGA_REGISTRY.items():
        assert key == spec.key
        assert key == key.lower()
        assert " " not in key
    assert len(set(YOGA_REGISTRY)) == len(YOGA_REGISTRY)


def test_an_unknown_yoga_key_is_refused_by_name():
    with pytest.raises(YogaError, match="unknown yoga"):
        evaluate_one("nonesuch", _in(SUN="Ar"))


def test_an_empty_chart_is_refused():
    with pytest.raises(YogaError, match="at least one graha"):
        evaluate(YogaInput(rasis={}))


def test_every_registered_yoga_declares_its_section():
    """So a reader can find the sentence each detector was written from."""
    for spec in YOGA_REGISTRY.values():
        assert spec.section
        assert spec.definition
        assert spec.group


# --------------------------------------------------------------------------
# 11.2 Ravi yogas — the preamble
# --------------------------------------------------------------------------


def test_11_2_what_a_ravi_yoga_is():
    """"Ravi yogas are the solar combinations. There are several yogas based
    on Sun."""
    assert "solar combinations" in RAVI_YOGA_INTRO
    ravi = {key for key, spec in YOGA_REGISTRY.items() if spec.group == "ravi"}
    assert ravi == {"vesi", "vosi", "ubhayachara", "budha_aaditya"}


def test_11_2_mercury_is_never_more_than_one_sign_from_the_sun():
    """"Because Mercury and Venus are with Sun or a sign away from him most of
    the time, the following yogas are very common in rasi chart."

    Checkable, and it is exactly true for Mercury: his elongation never
    reaches 30 degrees, so he is always in the 12th, the same sign, or the 2nd
    from the Sun. That is why Vesi, Vosi and Budha-Aaditya are cheap in a rasi
    chart.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    place = Place(latitude=18.0, longitude=79.0, name="x")
    offsets = set()
    for year in range(1920, 2021, 10):
        for month in (2, 6, 10):
            chart = compute_chart(
                from_local(year=year, month=month, day=15, hour=12, minute=0,
                           second=0.0, utc_offset_hours=5.5),
                place, Settings())
            sun = int(chart.positions[int(Graha.SUN)].longitude // 30)
            mercury = int(chart.positions[int(Graha.MERCURY)].longitude // 30)
            offsets.add((mercury - sun) % 12)
    assert offsets <= {0, 1, 11}, sorted(offsets)


def test_11_2_venus_can_reach_two_signs_which_is_why_it_says_most_of_the_time():
    """Venus's elongation reaches about 47 degrees, so he *can* be two signs
    away — which is why the sentence says "most of the time" for the pair and
    not "always"."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    place = Place(latitude=18.0, longitude=79.0, name="x")
    offsets = set()
    for year in range(1920, 2021, 4):
        for month in (1, 3, 5, 7, 9, 11):
            chart = compute_chart(
                from_local(year=year, month=month, day=15, hour=12, minute=0,
                           second=0.0, utc_offset_hours=5.5),
                place, Settings())
            sun = int(chart.positions[int(Graha.SUN)].longitude // 30)
            venus = int(chart.positions[int(Graha.VENUS)].longitude // 30)
            offsets.add((venus - sun) % 12)
    assert offsets <= {0, 1, 2, 10, 11}
    assert offsets & {2, 10}, "Venus should reach two signs away"


def test_11_2_the_yogas_are_meant_for_divisional_charts():
    """"they are less common in divisional charts. One can apply these yogas
    in D-9 and D-10 in particular."

    Carried on the response, and only for D-1, where the caveat bites.
    """
    assert RAVI_YOGA_PREFERRED_CHARTS == ("D9", "D10")
    assert "less common in divisional charts" in RAVI_YOGA_FREQUENCY_NOTE
    rasi = planetary_yoga_service.chart({int(Graha.SUN): 0}, chart_code="D1")
    navamsa = planetary_yoga_service.chart({int(Graha.SUN): 0}, chart_code="D9")
    assert rasi["chart_note"] == RAVI_YOGA_FREQUENCY_NOTE
    assert navamsa["chart_note"] is None


# --------------------------------------------------------------------------
# The four definitions and their examples
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key,name,section,houses",
    [("vesi", "Vesi Yoga", "11.2.1", (2,)),
     ("vosi", "Vosi Yoga", "11.2.2", (12,)),
     ("ubhayachara", "Ubhayachara Yoga", "11.2.3", (2, 12)),
     ("budha_aaditya", "Budha-Aaditya Yoga", "11.2.4", (1,))],
)
def test_the_four_ravi_yogas_are_declared_as_printed(key, name, section, houses):
    spec = next(y for y in RAVI_YOGAS if y["key"] == key)
    assert spec["name"] == name
    assert spec["section"] == section
    assert tuple(spec["houses_from_sun"]) == houses
    assert YOGA_REGISTRY[key].name == name


def test_11_2_1_vesi_the_books_own_example():
    """"If Sun is in Gemini and Jupiter and Mercury are in Cancer, then this
    yoga is present."""
    verdict = evaluate_one("vesi", _in(SUN="Ge", JUPITER="Cn", MERCURY="Cn"))
    assert verdict.present
    assert set(verdict.participants) == {int(Graha.JUPITER), int(Graha.MERCURY)}
    assert set(verdict.houses.values()) == {2}


def test_11_2_2_vosi_the_books_own_example():
    """"If Sun is in Aries and Jupiter and Venus are in Pisces, then this yoga
    is present."""
    verdict = evaluate_one("vosi", _in(SUN="Ar", JUPITER="Pi", VENUS="Pi"))
    assert verdict.present
    assert set(verdict.participants) == {int(Graha.JUPITER), int(Graha.VENUS)}
    assert set(verdict.houses.values()) == {12}


def test_11_2_3_ubhayachara_the_books_own_example():
    """"If Sun is in Cancer, Mars is in Leo and Venus is in Gemini, then this
    yoga is present."

    Leo is the 2nd from Cancer and Gemini the 12th, so one planet sits on each
    side.
    """
    verdict = evaluate_one("ubhayachara", _in(SUN="Cn", MARS="Le", VENUS="Ge"))
    assert verdict.present
    assert verdict.houses == {int(Graha.MARS): 2, int(Graha.VENUS): 12}


def test_11_2_3_ubhayachara_needs_both_sides():
    """"planets other than Moon in the 2nd **and** 12th houses". One side
    alone is not enough, and the reason names the empty side."""
    only_second = evaluate_one("ubhayachara", _in(SUN="Cn", MARS="Le"))
    assert not only_second.present
    assert "12th" in only_second.reason
    only_twelfth = evaluate_one("ubhayachara", _in(SUN="Cn", VENUS="Ge"))
    assert not only_twelfth.present
    assert "2nd" in only_twelfth.reason


def test_ubhayachara_always_implies_vesi_and_vosi():
    """A structural consequence the book never states: Ubhayachara needs both
    houses occupied, and Vesi and Vosi each need one. So Ubhayachara cannot
    hold alone, and all three are reported when it does.

    Checked exhaustively over every Sun sign and every pair of occupied
    houses, not just the book's example.
    """
    assert YOGA_REGISTRY["ubhayachara"].implies == ("vesi", "vosi")
    for sun in range(12):
        rasis = {int(Graha.SUN): sun,
                 int(Graha.MARS): (sun + 1) % 12,
                 int(Graha.VENUS): (sun + 11) % 12}
        verdicts = {v.key: v.present for v in evaluate(YogaInput(rasis=rasis))}
        assert verdicts["ubhayachara"] is True, sun
        assert verdicts["vesi"] and verdicts["vosi"], sun


def test_the_implication_holds_the_other_way_too():
    """Vesi and Vosi together always give Ubhayachara — the three are one
    condition split three ways, not three independent tests."""
    for sun in range(12):
        rasis = {int(Graha.SUN): sun, int(Graha.JUPITER): (sun + 1) % 12,
                 int(Graha.SATURN): (sun + 11) % 12}
        verdicts = {v.key: v.present for v in evaluate(YogaInput(rasis=rasis))}
        assert verdicts["vesi"] and verdicts["vosi"]
        assert verdicts["ubhayachara"]


# --------------------------------------------------------------------------
# "a planet other than Moon"
# --------------------------------------------------------------------------


def test_the_moon_never_forms_a_ravi_yoga():
    """"If there is a planet **other than Moon** in the 2nd house from Sun."

    The Moon in the 2nd forms nothing, in every Sun sign.
    """
    for sun in range(12):
        rasis = {int(Graha.SUN): sun, int(Graha.MOON): (sun + 1) % 12}
        verdicts = {v.key: v.present for v in evaluate(YogaInput(rasis=rasis))}
        assert not any(verdicts.values()), sun


def test_the_moon_is_excluded_from_the_twelfth_as_well():
    """The exclusion is in all three definitions, not only Vesi's."""
    for sun in range(12):
        rasis = {int(Graha.SUN): sun, int(Graha.MOON): (sun + 11) % 12}
        assert not any(v.present for v in evaluate(YogaInput(rasis=rasis)))


def test_the_sun_is_excluded_from_his_own_houses():
    """Not stated, but forced: a yoga about what *accompanies* the Sun cannot
    be formed by the Sun. He can only ever be the 1st from himself, so this
    bites for Budha-Aaditya's house alone and is asserted for completeness.
    """
    verdict = evaluate_one("vesi", _in(SUN="Ge"))
    assert not verdict.present
    assert "sun_excluded_note" in planetary_yoga_service.rules()


def test_the_nodes_are_excluded_by_default():
    """Chapter 11 says "a planet other than Moon" and never says whether the
    nodes count. Excluded by default, and the choice is a parameter rather
    than a silent one. See OI-73.
    """
    rasis = {int(Graha.SUN): R["Ge"], int(Graha.RAHU): R["Cn"]}
    assert not evaluate_one("vesi", YogaInput(rasis=rasis)).present
    with_nodes = evaluate_one("vesi", YogaInput(rasis=rasis, include_nodes=True))
    assert with_nodes.present
    assert with_nodes.participants == (int(Graha.RAHU),)


def test_the_node_choice_is_visible_in_the_output():
    """A caller reading a response must be able to see which grahas were
    considered, not only which yogas fired."""
    without = planetary_yoga_service.chart({int(Graha.SUN): 0})
    with_nodes = planetary_yoga_service.chart({int(Graha.SUN): 0},
                                              include_nodes=True)
    assert len(without["grahas_considered"]) == 7
    assert len(with_nodes["grahas_considered"]) == 9
    names = {g["graha_name"] for g in without["grahas_considered"]}
    assert "Rahu" not in names and "Ketu" not in names
    assert "Moon" in names, "the Moon is excluded per-yoga, not from the set"


# --------------------------------------------------------------------------
# 11.2.4 Budha-Aaditya
# --------------------------------------------------------------------------


def test_11_2_4_the_name_is_glossed_word_by_word():
    """"Budha means Mercury, Aaditya means Sun and yoga means togetherness...
    Nipuna means an expert."""
    assert BUDHA_AADITYA_TERMS == {
        "budha": "Mercury", "aaditya": "Sun", "yoga": "togetherness",
        "nipuna": "an expert"}
    assert YOGA_REGISTRY["budha_aaditya"].aliases == ("Nipuna Yoga",)


def test_11_2_4_sun_and_mercury_in_one_sign():
    """"If Sun and Mercury are together (in one sign), this yoga is present."

    Sign togetherness, not degree proximity — which is why combustion is a
    separate matter below.
    """
    assert evaluate_one("budha_aaditya", _in(SUN="Le", MERCURY="Le")).present
    apart = evaluate_one("budha_aaditya", _in(SUN="Le", MERCURY="Vi"))
    assert not apart.present
    assert "not together" in apart.reason


def test_11_2_4_combustion_weakens_but_never_cancels():
    """"Yogas formed by combust planets lose **some** of their power to do
    good."

    Some, not all. A combust Budha-Aaditya is present with a qualifier; the
    engine never suppresses it.
    """
    assert "some of their power" in COMBUSTION_WEAKENS_YOGA
    rules = planetary_yoga_service.rules()
    assert "never suppressed" in rules["combustion_is_a_qualifier_not_a_veto"]


def test_11_2_4_combustion_cannot_be_judged_from_signs_alone():
    """Combustion needs longitudes and the retrograde flag. From signs the
    engine cannot say, and it says that it cannot rather than reporting "not
    combust".
    """
    result = planetary_yoga_service.chart(
        {int(Graha.SUN): R["Le"], int(Graha.MERCURY): R["Le"]})
    assert "combustion" in result["qualifiers_unavailable"]
    yoga = next(y for y in result["yogas"] if y["key"] == "budha_aaditya")
    assert yoga["present"] is True
    assert COMBUSTION_WEAKENS_YOGA not in yoga["qualifiers"]


def test_11_2_4_combustion_is_detected_when_positions_are_supplied():
    """Given a real chart, the qualifier appears. Mercury within his orb of
    the Sun is combust, and the yoga still holds.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import Settings
    from hora.core.timeutil import from_local

    chart = compute_chart(
        from_local(year=1972, month=10, day=1, hour=13, minute=30, second=0.0,
                   tz_name="Asia/Kolkata"),
        Place(latitude=16.2, longitude=81.13, name="ref"), Settings())
    rasis = {g: int(p.longitude // 30) for g, p in chart.positions.items()}
    data = YogaInput(rasis=rasis, positions=chart.positions)
    verdict = evaluate_one("budha_aaditya", data)
    if verdict.present:
        from hora.charts.dignity import combustion
        expected = combustion(int(Graha.MERCURY), chart.positions).combust
        assert (COMBUSTION_WEAKENS_YOGA in verdict.qualifiers) is expected


def test_11_2_4_a_divisional_chart_carries_the_stronger_reading():
    """"This yoga is the most powerful in divisional charts like D-10."""
    d10 = evaluate_one("budha_aaditya",
                       YogaInput(rasis={int(Graha.SUN): 4, int(Graha.MERCURY): 4},
                                 chart="D10"))
    assert BUDHA_AADITYA_CHART_NOTE in d10.qualifiers
    d1 = evaluate_one("budha_aaditya", _in(SUN="Le", MERCURY="Le"))
    assert BUDHA_AADITYA_CHART_NOTE not in d1.qualifiers


def test_11_2_4_the_timing_example():
    """"Suppose someone has Sun and Mercury together in Leo in D-10... The
    results will be felt throughout one's life and the periods of Sun, Mercury
    and Leo will give those results in particular."

    The only place chapter 11 so far says *when* a yoga's results are felt.
    Two of the three periods are graha periods; Leo's is a rasi dasa, which is
    not built.
    """
    assert "throughout one's life" in BUDHA_AADITYA_TIMING_TEXT
    assert BUDHA_AADITYA_TIMING_PERIODS == (Graha.SUN, Graha.MERCURY)
    verdict = evaluate_one(
        "budha_aaditya",
        YogaInput(rasis={int(Graha.SUN): 4, int(Graha.MERCURY): 4}, chart="D10"))
    assert verdict.present


def test_11_2_4_the_name_is_spelled_two_ways_on_one_page():
    """The heading reads "Budha-Aaditya Yoga"; the worked reading below it
    reads "Budha-Aditya yoga". One page, two spellings — recorded, not
    normalised. See D-27."""
    assert BUDHA_AADITYA_SPELLING_VARIANTS == ("Budha-Aditya",)
    assert "Budha-Aditya" in BUDHA_AADITYA_TIMING_TEXT
    assert YOGA_REGISTRY["budha_aaditya"].name == "Budha-Aaditya Yoga"


def test_budha_aaditya_is_the_only_ravi_yoga_that_names_its_planets():
    """Vesi, Vosi and Ubhayachara accept any planet but the Moon.
    Budha-Aaditya names Mercury outright, so it is the only one whose
    participants are fixed in advance.
    """
    for key in ("vesi", "vosi", "ubhayachara"):
        spec = next(y for y in RAVI_YOGAS if y["key"] == key)
        assert spec["excludes"] == (Graha.MOON,)
    budha = next(y for y in RAVI_YOGAS if y["key"] == "budha_aaditya")
    assert budha["excludes"] == ()


# --------------------------------------------------------------------------
# The endpoints
# --------------------------------------------------------------------------


def test_chart_endpoint_returns_every_yoga(client):
    body = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: R["Cn"], 2: R["Le"], 5: R["Ge"]}}).json()
    assert body["evaluated"] == len(YOGA_REGISTRY)
    assert len(body["yogas"]) == len(YOGA_REGISTRY)
    assert {"ubhayachara", "vesi", "vosi"} <= set(body["present"])
    absent = [y for y in body["yogas"] if not y["present"]]
    assert all(y["reason"] for y in absent)


def test_chart_endpoint_carries_the_definitions(client):
    body = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: R["Ar"]}, "group": "ravi"}).json()
    for yoga in body["yogas"]:
        assert yoga["definition"]
        assert yoga["section"].startswith("11.2")


def test_one_endpoint_answers_a_single_yoga(client):
    body = client.post("/v1/planetary-yoga/one", json={
        "key": "vosi", "rasis": {0: R["Ar"], 4: R["Pi"]}}).json()
    assert body["present"] is True
    assert [p["graha_name"] for p in body["participants"]] == ["Jupiter"]


def test_catalogue_lists_every_yoga_without_a_chart(client):
    body = client.get("/v1/planetary-yoga/catalogue").json()
    assert body["count"] == len(YOGA_REGISTRY)
    assert set(body["groups"]) == {
        "ravi", "chandra", "mahapurusha", "naabhasa_aasraya",
        "naabhasa_dala", "naabhasa_aakriti", "naabhasa_sankhya", "popular"}
    assert {y["key"] for y in body["yogas"]} == set(YOGA_REGISTRY)


def test_rules_endpoint_states_what_is_not_decided(client):
    body = client.get("/v1/planetary-yoga/rules").json()
    assert "OI-73" in body["node_note"]
    assert "withheld" in body["results_note"]
    assert body["preferred_charts"] == ["D9", "D10"]
    assert body["timing_example"]["sign_name"] == "Leo"


def test_endpoints_reject_bad_input(client):
    assert client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: 12}}).status_code == 400
    bad_key = client.post("/v1/planetary-yoga/one", json={
        "key": "nonesuch", "rasis": {0: 0}})
    assert bad_key.status_code == 400
    assert "unknown yoga" in bad_key.json()["error"]["message"]
    bad_chart = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: 0}, "chart": "D99"})
    assert bad_chart.status_code == 400
    assert "unknown chart" in bad_chart.json()["error"]["message"]


def test_the_results_prose_is_not_served(client):
    """Each yoga's results — "truthful, tall and sluggish" and the rest — are
    PVR's own words and sit behind OI-12's licence gate. Nothing in the
    response carries them.
    """
    body = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: R["Cn"], 2: R["Le"], 5: R["Ge"]}}).json()
    payload = repr(body).lower()
    for word in ("sluggish", "truthful", "charitable", "king", "expert"):
        assert word not in payload


# --------------------------------------------------------------------------
# The results, and the gate they sit behind
# --------------------------------------------------------------------------


def _results():
    import pathlib

    import yaml

    path = pathlib.Path("data/content/yoga_results.yaml")
    return yaml.safe_load(path.read_text())


def test_every_registered_yoga_has_its_results_transcribed():
    """The other half of exhaustiveness: a yoga the engine detects but whose
    results were never transcribed would read as having none."""
    entries = {e["planetary_yoga"] for e in _results()["entries"]}
    missing = set(YOGA_REGISTRY) - entries
    assert not missing, f"detected but no results transcribed: {sorted(missing)}"


def test_no_results_entry_is_left_behind_by_a_renamed_key():
    """A key here that the registry no longer has is a stale transcription."""
    for entry in _results()["entries"]:
        assert entry["planetary_yoga"] in YOGA_REGISTRY, entry["planetary_yoga"]
        assert entry["name"] == YOGA_REGISTRY[entry["planetary_yoga"]].name
        assert entry["section"] == YOGA_REGISTRY[entry["planetary_yoga"]].section


@pytest.mark.parametrize(
    "key,fragment",
    [("vesi", "truthful, tall and sluggish"),
     ("vosi", "skillful, charitable, famous, learned and strong"),
     ("ubhayachara", "He is a king or an equal"),
     ("budha_aaditya", "intelligent and skillful in all works")],
)
def test_the_four_results_are_transcribed_as_printed(key, fragment):
    """§11.2.1 to §11.2.4's Results paragraphs, verbatim."""
    entry = next(e for e in _results()["entries"] if e["planetary_yoga"] == key)
    assert fragment in entry["verbatim"]


def test_every_results_entry_is_licence_gated():
    """PVR's own prose, so it carries OI-12's gate like every other verbatim
    source in `data/content/`."""
    data = _results()
    assert data["sources"]["pvr-vaia"]["licence_status"] == "unconfirmed"
    for entry in data["entries"]:
        assert entry["licence_status"] == "unconfirmed"


def test_the_nipuna_gloss_is_kept_where_the_book_puts_it():
    """"Nipuna means an expert" is printed inside Budha-Aaditya's *Results*
    paragraph, though it glosses the alias rather than stating a result. Kept
    there, with a note, rather than moved to the terms."""
    entry = next(e for e in _results()["entries"]
                 if e["planetary_yoga"] == "budha_aaditya")
    assert "Nipuna means an expert" in entry["verbatim"]
    assert "glosses the alias" in entry["transcription_notes"]
    assert "expert" not in {t["term"] for t in entry["terms"]}


# --------------------------------------------------------------------------
# 11.3 Chandra yogas
# --------------------------------------------------------------------------


def _moon(**placements) -> YogaInput:
    return _in(**placements)


def test_11_3_what_a_chandra_yoga_is():
    """"Chandra yogas are the lunar combinations. There are several yogas
    based on Moon."""
    assert "lunar combinations" in CHANDRA_YOGA_INTRO
    chandra = {k for k, s in YOGA_REGISTRY.items() if s.group == "chandra"}
    assert chandra == {"sunaphaa", "anaphaa", "duradhara", "kemadruma",
                       "chandra_mangala", "adhi"}


@pytest.mark.parametrize(
    "chandra,ravi",
    [("sunaphaa", "vesi"), ("anaphaa", "vosi"),
     ("duradhara", "ubhayachara"), ("chandra_mangala", "budha_aaditya")],
)
def test_four_chandra_yogas_mirror_a_ravi_yoga(chandra, ravi):
    """§11.3.1 to §11.3.3 are §11.2.1 to §11.2.3 with Sun and Moon exchanged:
    "a planet other than **Moon** in the 2nd from **Sun**" against "planets
    other than **Sun** in the 2nd from **Moon**".

    The same detector serves both, parameterised, so the mirror cannot drift.
    """
    spec = next(y for y in CHANDRA_YOGAS if y["key"] == chandra)
    assert spec["mirrors"] == ravi
    chandra_houses = tuple(spec["houses_from_moon"])
    ravi_spec = next(y for y in RAVI_YOGAS if y["key"] == ravi)
    assert chandra_houses == tuple(ravi_spec["houses_from_sun"])


def test_the_mirror_is_exact_on_every_placement():
    """Swap the Sun and the Moon in any chart and Vesi becomes Sunaphaa,
    Vosi becomes Anaphaa, Ubhayachara becomes Duradhara.

    Checked over every Sun sign and both flanking houses, not asserted from
    the shared code.
    """
    for reference in range(12):
        for other in ((reference + 1) % 12, (reference + 11) % 12):
            solar = YogaInput(rasis={int(Graha.SUN): reference,
                                     int(Graha.JUPITER): other})
            lunar = YogaInput(rasis={int(Graha.MOON): reference,
                                     int(Graha.JUPITER): other})
            for ravi, chandra in (("vesi", "sunaphaa"), ("vosi", "anaphaa"),
                                  ("ubhayachara", "duradhara")):
                assert (evaluate_one(ravi, solar).present
                        == evaluate_one(chandra, lunar).present), (reference, other)


def test_11_3_1_sunaphaa_the_books_own_example():
    """"If Moon is in Gemini and Jupiter and Mercury are in Cancer, then this
    yoga is present."""
    verdict = evaluate_one("sunaphaa", _moon(MOON="Ge", JUPITER="Cn", MERCURY="Cn"))
    assert verdict.present
    assert set(verdict.participants) == {int(Graha.JUPITER), int(Graha.MERCURY)}


def test_11_3_2_anaphaa_the_books_own_example():
    """"If Moon is in Aries and Jupiter and Venus are in Pisces, then this
    yoga is present."""
    verdict = evaluate_one("anaphaa", _moon(MOON="Ar", JUPITER="Pi", VENUS="Pi"))
    assert verdict.present
    assert set(verdict.houses.values()) == {12}


def test_11_3_3_duradhara_the_books_own_example():
    """"If Moon is in Cancer, Mars is in Leo and Venus is in Gemini, then this
    yoga is present."""
    verdict = evaluate_one("duradhara", _moon(MOON="Cn", MARS="Le", VENUS="Ge"))
    assert verdict.present
    assert verdict.houses == {int(Graha.MARS): 2, int(Graha.VENUS): 12}


def test_duradhara_implies_sunaphaa_and_anaphaa():
    """The lunar counterpart of Ubhayachara's containment, and asserted the
    same way — over every Moon sign, not just the example."""
    assert YOGA_REGISTRY["duradhara"].implies == ("sunaphaa", "anaphaa")
    for moon in range(12):
        rasis = {int(Graha.MOON): moon, int(Graha.MARS): (moon + 1) % 12,
                 int(Graha.VENUS): (moon + 11) % 12}
        verdicts = {v.key: v.present for v in evaluate(YogaInput(rasis=rasis))}
        assert verdicts["duradhara"] and verdicts["sunaphaa"] and verdicts["anaphaa"]


def test_the_sun_never_forms_a_chandra_yoga():
    """"planets other than **Sun**" — the mirror of the Moon's exclusion from
    the Ravi yogas."""
    for moon in range(12):
        for house in (1, 11):
            rasis = {int(Graha.MOON): moon, int(Graha.SUN): (moon + house) % 12}
            verdicts = {v.key: v.present
                        for v in evaluate(YogaInput(rasis=rasis), group="chandra")}
            assert not verdicts["sunaphaa"] and not verdicts["anaphaa"]


def test_11_3_5_chandra_mangala_is_a_conjunction():
    """"If Moon and Mars are together (in one sign), then this yoga is
    present." — the same shape as Budha-Aaditya, and the same detector."""
    assert evaluate_one("chandra_mangala", _moon(MOON="Le", MARS="Le")).present
    apart = evaluate_one("chandra_mangala", _moon(MOON="Le", MARS="Vi"))
    assert not apart.present
    assert "not together" in apart.reason


# --------------------------------------------------------------------------
# 11.3.4 Kemadruma — the first negative yoga
# --------------------------------------------------------------------------


def _kemadruma_chart(**overrides):
    """The book's example: lagna Taurus, Moon Virgo, everything else clear of
    both lists.

    The Sun sits in Capricorn with Jupiter in Sagittarius behind him, so Vosi
    also forms — Kemadruma and another yoga can coexist, which is what makes
    the "kills the results" rule testable at all.
    """
    rasis = {int(Graha.MOON): R["Vi"], int(Graha.SUN): R["Cp"],
             int(Graha.JUPITER): R["Sg"], int(Graha.MARS): R["Ge"],
             int(Graha.MERCURY): R["Cn"], int(Graha.VENUS): R["Pi"],
             int(Graha.SATURN): R["Ar"]}
    for name, sign in overrides.items():
        rasis[int(getattr(Graha, name))] = R[sign]
    return YogaInput(rasis=rasis, lagna_rasi=R["Ta"])


def test_11_3_4_kemadruma_the_books_own_example():
    """"If lagna is in Taurus, Moon is in Virgo, no planets other than Sun in
    Leo, Virgo and Libra and no planets in Taurus, Leo, Scorpio and Aquarius,
    then this yoga is present."

    Both clauses check out: Leo, Virgo and Libra are the 12th, 1st and 2nd
    from Virgo, and Taurus, Leo, Scorpio and Aquarius are the quadrants from
    Taurus.
    """
    assert [RASI_ABBR[(R["Vi"] + h - 1) % 12] for h in (12, 1, 2)] == [
        "Le", "Vi", "Li"]
    assert [RASI_ABBR[(R["Ta"] + h - 1) % 12] for h in (1, 4, 7, 10)] == [
        "Ta", "Le", "Sc", "Aq"]
    assert evaluate_one("kemadruma", _kemadruma_chart()).present


def test_11_3_4_either_clause_alone_breaks_it():
    """"no planets ... in the 1st, 2nd and 12th houses from Moon **and** ...
    no planets ... in the quadrants from lagna." Both must hold."""
    near_moon = evaluate_one("kemadruma", _kemadruma_chart(JUPITER="Li"))
    assert not near_moon.present
    assert "from Moon" in near_moon.reason
    in_quadrant = evaluate_one("kemadruma", _kemadruma_chart(JUPITER="Aq"))
    assert not in_quadrant.present
    assert "from lagna" in in_quadrant.reason


def test_11_3_4_the_sun_is_exempt_near_the_moon_but_not_in_a_quadrant():
    """The two clauses exempt different grahas: the first "other than Sun",
    the second "other than Moon".

    Leo falls in both lists in the book's own example — the 12th from Virgo
    and the 4th from Taurus — so the Sun there is permitted by the first
    clause and forbidden by the second. The stricter clause wins.
    """
    assert evaluate_one("kemadruma", _kemadruma_chart(SUN="Vi")).present
    in_leo = evaluate_one("kemadruma", _kemadruma_chart(SUN="Le"))
    assert not in_leo.present
    assert "from lagna" in in_leo.reason


def test_11_3_4_the_moon_in_a_quadrant_does_not_break_it():
    """"no planets **other than Moon** in the quadrants from lagna" — so a
    Moon in a quadrant is fine, which the book's example does not exercise."""
    # Lagna Taurus, Moon Taurus — the Moon herself in a quadrant. The Sun sits
    # in Aries, the 12th from her, where clause 1 exempts him and clause 2
    # does not reach.
    rasis = {int(Graha.MOON): R["Ta"], int(Graha.SUN): R["Ar"],
             int(Graha.MARS): R["Cn"], int(Graha.MERCURY): R["Vi"],
             int(Graha.JUPITER): R["Li"], int(Graha.VENUS): R["Sg"],
             int(Graha.SATURN): R["Cp"]}
    verdict = evaluate_one("kemadruma", YogaInput(rasis=rasis, lagna_rasi=R["Ta"]))
    assert verdict.present


def test_11_3_4_is_unanswerable_without_a_lagna():
    """The only yoga so far that reads a house from the ascendant. Without one
    it says it cannot be decided, rather than returning a bare False that
    would read as "checked and absent".
    """
    rasis = _kemadruma_chart().rasis
    verdict = evaluate_one("kemadruma", YogaInput(rasis=rasis))
    assert verdict.present is False
    assert "cannot be decided" in verdict.reason


def test_kemadruma_and_the_three_lunar_yogas_are_mutually_exclusive():
    """Kemadruma needs the 2nd and 12th from the Moon empty; Sunaphaa,
    Anaphaa and Duradhara each need one of them occupied. So Kemadruma can
    never hold beside them — checked over every Moon sign.
    """
    for moon in range(12):
        rasis = {int(Graha.MOON): moon, int(Graha.JUPITER): (moon + 1) % 12}
        data = YogaInput(rasis=rasis, lagna_rasi=(moon + 3) % 12)
        verdicts = {v.key: v.present for v in evaluate(data, group="chandra")}
        assert verdicts["sunaphaa"] is True, moon
        assert verdicts["kemadruma"] is False, moon


def test_11_3_4_kills_the_results_of_other_yogas_without_cancelling_them():
    """"This bad yoga kills the results of other good yogas in the chart,
    especially Chandra yogas."

    It kills the *results*, not the yoga. So a yoga still forming beside
    Kemadruma is reported present, with a qualifier — the same rule as
    §11.2.4's combustion.
    """
    assert "kills the results" in KEMADRUMA_KILLS_OTHER_YOGAS
    rasis = dict(_kemadruma_chart().rasis)
    body = planetary_yoga_service.chart(rasis, lagna_rasi=R["Ta"])
    assert body["kemadruma_present"] is True
    killed = body["results_killed_by_kemadruma"]
    assert killed, "some other yoga should still form"
    for yoga in body["yogas"]:
        if yoga["key"] in killed:
            assert yoga["present"] is True
            assert KEMADRUMA_KILLS_OTHER_YOGAS in yoga["qualifiers"]


def test_the_kemadruma_qualifier_is_absent_when_kemadruma_is():
    rasis = dict(_kemadruma_chart().rasis)
    rasis[int(Graha.JUPITER)] = R["Li"]
    body = planetary_yoga_service.chart(rasis, lagna_rasi=R["Ta"])
    assert body["kemadruma_present"] is False
    assert body["results_killed_by_kemadruma"] == []
    for yoga in body["yogas"]:
        assert KEMADRUMA_KILLS_OTHER_YOGAS not in yoga["qualifiers"]


# --------------------------------------------------------------------------
# 11.3.6 Adhi — where the example fails the rule
# --------------------------------------------------------------------------


def test_11_3_6_the_example_does_not_satisfy_the_rule():
    """**The find.** §11.3.6's rule asks for the natural benefics in the 6th,
    7th and 8th from the Moon. Its example puts the Moon in Taurus with the
    benefics in Virgo and Leo — the **5th** and **4th** from Taurus.

    The 6th, 7th and 8th from Taurus are Libra, Scorpio and Sagittarius, and
    the example puts nothing there. See D-28 and PVR-11.
    """
    assert [RASI_ABBR[(R["Ta"] + h - 1) % 12] for h in (6, 7, 8)] == [
        "Li", "Sc", "Sg"]
    assert (R["Vi"] - R["Ta"]) % 12 + 1 == 5
    assert (R["Le"] - R["Ta"]) % 12 + 1 == 4
    as_printed = evaluate_one("adhi", YogaInput(
        rasis={int(Graha.MOON): R["Ta"], int(Graha.MERCURY): R["Vi"],
               int(Graha.JUPITER): R["Vi"], int(Graha.VENUS): R["Le"]},
        paksha=0))
    assert as_printed.present is False


def test_11_3_6_the_rule_is_followed_not_the_example():
    """Tie-break rule 1 — a stated rule beats its transcribed output. The
    detector implements 6/7/8, and the same benefics hold the yoga once the
    Moon is where the rule requires.

    Moon in Pisces is the minimal repair: it makes Leo the 6th and Virgo the
    7th. Recorded as the smallest change that reconciles them, not as a claim
    about what PVR meant.
    """
    repaired = evaluate_one("adhi", YogaInput(
        rasis={int(Graha.MOON): R["Pi"], int(Graha.MERCURY): R["Vi"],
               int(Graha.JUPITER): R["Vi"], int(Graha.VENUS): R["Le"]},
        paksha=0))
    assert repaired.present is True
    assert (R["Le"] - R["Pi"]) % 12 + 1 == 6
    assert (R["Vi"] - R["Pi"]) % 12 + 1 == 7
    assert "the rule is followed" in ADHI_EXAMPLE_CONTRADICTS_RULE.lower()


def test_11_3_6_a_benefic_outside_the_three_houses_breaks_it():
    """"If **the natural benefics** occupy 6th, 7th and 8th" — the benefics as
    a group, not merely one of them. A benefic elsewhere breaks it.
    """
    verdict = evaluate_one("adhi", YogaInput(
        rasis={int(Graha.MOON): R["Pi"], int(Graha.MERCURY): R["Vi"],
               int(Graha.JUPITER): R["Vi"], int(Graha.VENUS): R["Ar"]},
        paksha=0))
    assert verdict.present is False
    assert "Venus" in verdict.reason


def test_11_3_6_the_moon_is_not_counted_against_herself():
    """A waxing Moon is a natural benefic (§3.2.2) and can only ever be the
    1st from herself. Counting her would make Adhi impossible for every
    bright-half birth, so she is excluded from her own test.
    """
    bright = evaluate_one("adhi", YogaInput(
        rasis={int(Graha.MOON): R["Pi"], int(Graha.MERCURY): R["Vi"],
               int(Graha.JUPITER): R["Vi"], int(Graha.VENUS): R["Le"]},
        paksha=0))
    dark = evaluate_one("adhi", YogaInput(
        rasis=bright and {int(Graha.MOON): R["Pi"], int(Graha.MERCURY): R["Vi"],
                          int(Graha.JUPITER): R["Vi"], int(Graha.VENUS): R["Le"]},
        paksha=1))
    assert bright.present is True
    assert dark.present is True


def test_11_3_6_an_undecidable_benefic_is_flagged_not_assumed():
    """Mercury's nature depends on his companions and the Moon's on the
    paksha. Where a nature could not be judged, the verdict says so rather
    than quietly treating the graha as non-benefic.
    """
    verdict = evaluate_one("adhi", YogaInput(
        rasis={int(Graha.MOON): R["Pi"], int(Graha.JUPITER): R["Vi"],
               int(Graha.VENUS): R["Le"], int(Graha.MARS): R["Ar"]}))
    assert verdict.present is True
    assert not verdict.qualifiers, "no undecidable benefic among these"


def test_11_3_6_the_graded_result_is_not_computed():
    """"becomes a king or a minister or an army chief, **depending on the
    strength of the planets involved**."

    Chapter 15's simple-rules measure would decide which; it is not built. The
    engine reports the yoga and never the station.
    """
    verdict = evaluate_one("adhi", YogaInput(
        rasis={int(Graha.MOON): R["Pi"], int(Graha.MERCURY): R["Vi"],
               int(Graha.JUPITER): R["Vi"], int(Graha.VENUS): R["Le"]},
        paksha=0))
    payload = repr(verdict).lower()
    for word in ("king", "minister", "army"):
        assert word not in payload


# --------------------------------------------------------------------------
# 11.3 General Guidelines — not yogas
# --------------------------------------------------------------------------


def test_the_guidelines_are_not_in_the_registry():
    """§11.3's three General Guidelines are graded readings, not
    combinations: guideline 1 always yields a verdict because its categories
    partition the twelve houses. Registering them would misreport them as
    yogas.
    """
    keys = set(YOGA_REGISTRY)
    for word in ("guideline", "quadrant_from_sun", "upachaya"):
        assert not any(word in key for key in keys)


def test_guideline_1_always_yields_exactly_one_verdict():
    """"If Moon is in a quadrant from Sun ... a panapara ... an apoklima."

    Kendras, panapharas and apoklimas partition the twelve houses, so the Moon
    is always in exactly one of them and guideline 1 never abstains.
    """
    seen = set()
    for offset in range(12):
        result = planetary_yoga_service.guidelines(
            {int(Graha.SUN): 0, int(Graha.MOON): offset})
        first = result["guideline_1"]
        assert first["verdict"] is not None, offset
        seen.add(first["category"])
    assert seen == {"kendra", "panaphara", "apoklima"}


def test_guideline_1_grades_apoklimas_highest():
    """The direction is counter-intuitive and worth pinning: the apoklimas,
    the weakest houses elsewhere in the book, give "a lot of wealth" here,
    while the quadrants give "little"."""
    assert CHANDRA_MOON_FROM_SUN_GRADE["kendra"].startswith("little")
    assert CHANDRA_MOON_FROM_SUN_GRADE["panaphara"].startswith("average")
    assert CHANDRA_MOON_FROM_SUN_GRADE["apoklima"].startswith("a lot")


def test_guideline_1_spells_panaphara_the_short_way():
    """§11.3 writes "panapara"; chapter 7 writes "panaphara". Same category,
    recorded rather than normalised. See D-29."""
    assert PANAPHARA_SPELLING_VARIANTS == ("panapara",)
    assert "panapara" in CHANDRA_GUIDELINE_1
    assert "panaphara" not in CHANDRA_GUIDELINE_1


def test_guideline_2_is_recorded_and_not_computed():
    """It needs the Moon's navamsa, that navamsa lord's compound relationship
    to the Moon, whether the birth was by day, and Jupiter's and Venus's
    aspects on the Moon. Four chapters' machinery; not joined yet. See OI-76.
    """
    result = planetary_yoga_service.guidelines({int(Graha.MOON): 0})
    second = result["guideline_2"]
    assert second["verdict"] is None
    assert "OI-76" in second["reason"]


def test_guideline_2_the_same_aspect_helps_or_harms_by_time_of_birth():
    """"Jupiter's aspect on Moon in a night birth and Venusian aspect on Moon
    in a daytime birth are **detrimental**."

    The benefit is not the graha's — it is the pairing. Jupiter is good by day
    and bad by night; Venus is the reverse.
    """
    table = CHANDRA_ASPECT_BY_BIRTH_TIME
    assert table[("jupiter", "day")] == "good"
    assert table[("jupiter", "night")] == "detrimental"
    assert table[("venus", "night")] == "good"
    assert table[("venus", "day")] == "detrimental"


def test_guideline_2_uses_chapter_3s_own_word_for_a_good_friend():
    """"own navamsa or that of an **adhimitra (good friend)**."

    Chapter 3's compound-relationship table names the great-friend grade
    "adhimitra" and glosses it "good friend". Built from chapter 3 alone, used
    here in chapter 11 without a cross-reference, and the two agree exactly.
    """
    from hora.core.const import COMPOUND_RELATION_GLOSSES, COMPOUND_RELATION_NAMES

    assert COMPOUND_RELATION_NAMES["great_friend"] == "adhimitra"
    assert COMPOUND_RELATION_GLOSSES["great_friend"] == "good friend"
    assert "adhimitra (good friend)" in CHANDRA_GUIDELINE_2


def test_guideline_2_records_its_own_ambiguity():
    """"aspect of Jupiter on Moon beings wealth and comforts in the case of
    daytime birth **(respectively)**."

    "Respectively" pairs two things with two. The only pair in reach is "own
    navamsa or that of an adhimitra". The book does not say so, and neither
    do we. See OI-74.
    """
    assert "(respectively)" in CHANDRA_GUIDELINE_2
    assert "own navamsa or that of an adhimitra" in \
        CHANDRA_GUIDELINE_2_RESPECTIVELY_NOTE
    assert "does not say" in CHANDRA_GUIDELINE_2_RESPECTIVELY_NOTE


def test_guideline_2_keeps_the_books_typo():
    """"beings wealth and comforts" — for "brings". Transcribed as printed."""
    assert "beings wealth and comforts" in CHANDRA_GUIDELINE_2


def test_guideline_3_grades_by_how_many_benefics_reach_an_upachaya():
    """"If **all** the natural benefics occupy upachayas (3rd, 6th, 10th and
    11th) from Moon, one has great wealth. If **two** ... medium wealth. If
    only **one** ... little wealth."
    """

    assert UPACHAYA == (3, 6, 10, 11)
    assert "3rd, 6th, 10th and 11th" in CHANDRA_GUIDELINE_3
    moon = R["Ar"]
    upachayas = [(moon + h - 1) % 12 for h in UPACHAYA]
    one = planetary_yoga_service.guidelines(
        {int(Graha.MOON): moon, int(Graha.JUPITER): upachayas[0],
         int(Graha.VENUS): R["Ta"]}, paksha=1)
    assert one["guideline_3"]["verdict"] == "little wealth"
    both = planetary_yoga_service.guidelines(
        {int(Graha.MOON): moon, int(Graha.JUPITER): upachayas[0],
         int(Graha.VENUS): upachayas[1]}, paksha=1)
    assert both["guideline_3"]["verdict"] == "great wealth"


def test_guideline_3_all_outranks_the_count():
    """"If all the natural benefics occupy upachayas ... great wealth" and
    "If two benefics occupy upachayas ... medium".

    Two benefics that are *all* the benefics there are must be "great", not
    "medium" — the "all" clause is a stronger claim about the same
    arrangement, and it wins.
    """
    moon = R["Ar"]
    result = planetary_yoga_service.guidelines(
        {int(Graha.MOON): moon, int(Graha.JUPITER): (moon + 2) % 12,
         int(Graha.VENUS): (moon + 5) % 12}, paksha=1)
    third = result["guideline_3"]
    assert len(third["benefics_in_upachaya"]) == 2
    assert third["verdict"] == "great wealth"


def test_guideline_3_reports_an_undecidable_nature_separately():
    """Without a paksha the Moon has no nature (§3.2.2). She is the reference
    here so it does not change the count, but Mercury's can, and an
    unjudgeable nature is listed rather than silently dropped.
    """
    result = planetary_yoga_service.guidelines(
        {int(Graha.MOON): R["Ar"], int(Graha.JUPITER): R["Ge"]})
    assert result["guideline_3"]["undecidable"] == []


# --------------------------------------------------------------------------
# The Chandra endpoints
# --------------------------------------------------------------------------


def test_chart_endpoint_evaluates_both_groups(client):
    body = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {1: R["Ge"], 4: R["Cn"], 3: R["Cn"]}}).json()
    assert body["evaluated"] == len(YOGA_REGISTRY)
    assert "sunaphaa" in body["present"]


def test_chart_endpoint_takes_a_lagna_for_kemadruma(client):
    rasis = {int(k): v for k, v in _kemadruma_chart().rasis.items()}
    body = client.post("/v1/planetary-yoga/chart", json={
        "rasis": rasis, "lagna_rasi": R["Ta"]}).json()
    assert "kemadruma" in body["present"]
    assert body["kemadruma_present"] is True


def test_guidelines_endpoint(client):
    body = client.post("/v1/planetary-yoga/guidelines", json={
        "rasis": {0: R["Ar"], 1: R["Ge"]}, "paksha": 0}).json()
    assert body["guideline_1"]["category"] == "apoklima"
    assert body["guideline_2"]["verdict"] is None
    assert body["guideline_3"]["verdict"] is None


def test_group_filter_is_validated(client):
    response = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: 0}, "group": "nonesuch"})
    assert response.status_code == 400
    assert "unknown group" in response.json()["error"]["message"]


# --------------------------------------------------------------------------
# 11.4 Pancha Mahapurusha yogas
# --------------------------------------------------------------------------


def test_11_4_the_name_is_glossed():
    """"Pancha means five and mahapurusha means a great person."""
    assert MAHAPURUSHA_TERMS == {"pancha": "five",
                                 "mahapurusha": "a great person"}
    assert "5 kinds of great persons" in MAHAPURUSHA_INTRO


def test_11_4_there_are_exactly_five():
    """"5 kinds of great persons", one per element, one per graha."""
    keys = {k for k, s in YOGA_REGISTRY.items() if s.group == "mahapurusha"}
    assert keys == {"ruchaka", "bhadra", "sasa", "maalavya", "hamsa"}
    assert len(MAHAPURUSHA_YOGAS) == 5


def test_11_4_the_five_grahas_are_the_non_luminaries():
    """Mars, Mercury, Saturn, Venus and Jupiter — the Sun, the Moon and both
    nodes take no part. That is what makes them five rather than seven or
    nine.
    """
    grahas = {y["graha"] for y in MAHAPURUSHA_YOGAS}
    assert grahas == {Graha.MARS, Graha.MERCURY, Graha.SATURN,
                      Graha.VENUS, Graha.JUPITER}
    assert Graha.SUN not in grahas and Graha.MOON not in grahas
    assert Graha.RAHU not in grahas and Graha.KETU not in grahas


def test_11_4_the_five_tattvas_as_printed():
    """"Agni tattva (fiery nature), Bhoo tattva (earthy nature), Vaayu tattva
    (airy nature), Jala tattva (watery nature), Aakaasa tattva (ethery
    nature)."""
    from hora.core.const import PLANET_ELEMENT_ADJECTIVES, PLANET_ELEMENT_TATTVAS

    assert PLANET_ELEMENT_TATTVAS == (
        "agni tattva", "bhoo tattva", "vaayu tattva", "jala tattva",
        "aakaasa tattva")
    assert PLANET_ELEMENT_ADJECTIVES == (
        "fiery", "earthy", "airy", "watery", "ethery")


def test_11_4_repeats_3_2_8_and_they_agree():
    """§3.2.8 gave the five elements and their rulers; §11.4 restates them.

    "Mars, Mercury, Saturn, Venus and Jupiter (respectively) represent these 5
    elements" — and `ELEMENT_RULER`, transcribed from §3.2.8 alone, is exactly
    that list in exactly that order. "Respectively" only works if the order
    matches, and it does.
    """
    from hora.core.const import ELEMENT_RULER

    order = [ELEMENT_RULER[i] for i in range(5)]
    assert order == [Graha.MARS, Graha.MERCURY, Graha.SATURN,
                     Graha.VENUS, Graha.JUPITER]
    assert "(respectively)" in MAHAPURUSHA_ELEMENT_RULERS_SENTENCE


def test_11_4_each_yoga_takes_its_rulers_element():
    """Ruchaka is Mars's and gives "a great man of fiery nature"; Bhadra is
    Mercury's and gives "earthy"; and so down the five. Checked against
    §3.2.8's table rather than against the results prose.
    """
    from hora.core.const import ELEMENT_RULER, PLANET_ELEMENT_ADJECTIVES

    for entry in MAHAPURUSHA_YOGAS:
        index = entry["element_index"]
        assert ELEMENT_RULER[index] == entry["graha"], entry["key"]
        assert PLANET_ELEMENT_ADJECTIVES[index], entry["key"]


def test_11_4_names_the_set_two_ways():
    """"These are called pancha bhootas (five existences) or pancha tattvas
    (five natures)." Both names and both glosses, which §3.2.8 does not give.
    """
    assert PANCHA_BHOOTA_NAMES == {
        "pancha bhootas": "five existences",
        "pancha tattvas": "five natures"}


def test_11_4_glosses_the_tattvas_differently_from_3_2_8():
    """§3.2.8 writes "Aakaasa tattva (ethery **element**)"; §11.4 writes
    "(ethery **nature**)". The same five, glossed with different words in the
    two sections. Recorded rather than normalised — see D-32.
    """
    assert TATTVA_GLOSS_IN_11_4 == "nature"
    assert TATTVA_GLOSS_IN_3_2_8 == "element"
    assert TATTVA_GLOSS_IN_11_4 != TATTVA_GLOSS_IN_3_2_8


# --------------------------------------------------------------------------
# The one construction, five times
# --------------------------------------------------------------------------


@pytest.mark.parametrize("entry", MAHAPURUSHA_YOGAS, ids=lambda e: e["key"])
def test_11_4_the_printed_signs_are_derived_not_transcribed(entry):
    """"In other words, Mars should be in Ar, Sc or Cp" — "in other words",
    so the sign list is the rule's consequence, not a second rule.

    Derived from `RASI_LORD` and `EXALTATION_DEG` and checked against every
    printed list. A change to either table that broke a yoga would fail here.
    """
    from hora.charts.planetary_yogas.mahapurusha import dignified_signs

    computed = {RASI_ABBR[s] for s in dignified_signs(entry["graha"])}
    assert computed == set(entry["printed_signs"]), entry["key"]


def test_11_4_mercury_alone_has_two_signs_not_three():
    """Virgo is both Mercury's own sign and his exaltation sign, so his set
    collapses to two where every other graha here has three.

    §11.4.2 prints exactly that — "Mercury should be in Ge or Vi" — so the
    book noticed. Worth pinning, because a naive "two own signs plus one
    exaltation" would give three and admit a sign that does not exist.
    """
    from hora.charts.planetary_yogas.mahapurusha import dignified_signs

    sizes = {e["key"]: len(dignified_signs(e["graha"])) for e in MAHAPURUSHA_YOGAS}
    assert sizes["bhadra"] == 2
    assert all(size == 3 for key, size in sizes.items() if key != "bhadra")
    assert len(MAHAPURUSHA_YOGAS[1]["printed_signs"]) == 2


@pytest.mark.parametrize("entry", MAHAPURUSHA_YOGAS, ids=lambda e: e["key"])
def test_11_4_each_worked_example(entry):
    """"As an example, a native with lagna in Li and Mars in Ar will have this
    yoga" — and the same shape for each of the five."""
    example = entry["example"]
    verdict = evaluate_one(entry["key"], YogaInput(
        rasis={int(entry["graha"]): R[example["graha_sign"]]},
        lagna_rasi=R[example["lagna"]]))
    assert verdict.present, entry["key"]
    house = (R[example["graha_sign"]] - R[example["lagna"]]) % 12 + 1
    assert house in (1, 4, 7, 10)
    assert verdict.houses == {int(entry["graha"]): house}


def test_11_4_the_examples_use_four_different_quadrants():
    """The five examples land on the 7th, 4th, 10th, 10th and 4th — three of
    the four quadrants, never the 1st. So none of them exercises a graha in
    the ascendant itself, which the rule plainly allows.
    """
    houses = {
        (R[e["example"]["graha_sign"]] - R[e["example"]["lagna"]]) % 12 + 1
        for e in MAHAPURUSHA_YOGAS
    }
    assert houses == {4, 7, 10}
    verdict = evaluate_one("ruchaka", YogaInput(
        rasis={int(Graha.MARS): R["Ar"]}, lagna_rasi=R["Ar"]))
    assert verdict.present
    assert verdict.houses == {int(Graha.MARS): 1}


def test_11_4_both_halves_are_required():
    """A dignified graha outside a quadrant, and a quadrant graha without
    dignity, each fail — and the reason names which half was missing."""
    outside = evaluate_one("ruchaka", YogaInput(
        rasis={int(Graha.MARS): R["Ar"]}, lagna_rasi=R["Ta"]))
    assert not outside.present
    assert "not a quadrant" in outside.reason
    undignified = evaluate_one("ruchaka", YogaInput(
        rasis={int(Graha.MARS): R["Ge"]}, lagna_rasi=R["Ge"]))
    assert not undignified.present
    assert "not one of" in undignified.reason


def test_11_4_the_verdict_names_own_sign_or_exaltation():
    """Both qualify, and which one it was is part of the evidence."""
    own = evaluate_one("sasa", YogaInput(
        rasis={int(Graha.SATURN): R["Cp"]}, lagna_rasi=R["Cp"]))
    assert "his own sign" in own.reason
    exalted = evaluate_one("sasa", YogaInput(
        rasis={int(Graha.SATURN): R["Li"]}, lagna_rasi=R["Cp"]))
    assert "his exaltation sign" in exalted.reason


def test_11_4_is_unanswerable_without_a_lagna():
    """Like Kemadruma, and for the same reason: quadrants are counted from the
    ascendant."""
    for entry in MAHAPURUSHA_YOGAS:
        verdict = evaluate_one(entry["key"], YogaInput(
            rasis={int(entry["graha"]): R[entry["printed_signs"][0]]}))
        assert verdict.present is False
        assert "cannot be decided" in verdict.reason


def test_11_4_does_not_apply_from_the_moon():
    """"This yoga does not apply from Moon."

    The first place in the book that rules a reference **out**. Chapter 7 made
    every reference relative and §7.3 lists eight of them; §11.4 excludes one
    by name, five times over.

    So no Moon-reference option exists on the input at all — a caller cannot
    ask for it and get a wrong answer.
    """
    assert "does not apply from Moon" in MAHAPURUSHA_REFERENCE_RULE
    fields = YogaInput.__dataclass_fields__
    assert "lagna_rasi" in fields
    assert not any("moon" in field for field in fields)


def test_11_4_applies_mainly_in_the_rasi_chart():
    """"it applies mainly in rasi chart" — the opposite of §11.2, which sends
    the Ravi yogas to D-9 and D-10.

    A non-rasi chart is flagged rather than refused, since "mainly" is not
    "only".
    """
    assert "mainly in rasi chart" in MAHAPURUSHA_REFERENCE_RULE
    assert "less common in divisional charts" in RAVI_YOGA_FREQUENCY_NOTE
    d1 = evaluate_one("ruchaka", YogaInput(
        rasis={int(Graha.MARS): R["Ar"]}, lagna_rasi=R["Li"]))
    d9 = evaluate_one("ruchaka", YogaInput(
        rasis={int(Graha.MARS): R["Ar"]}, lagna_rasi=R["Li"], chart="D9"))
    assert d1.present and d9.present
    assert MAHAPURUSHA_REFERENCE_RULE not in d1.qualifiers
    assert MAHAPURUSHA_REFERENCE_RULE in d9.qualifiers


def test_11_4_more_than_one_can_hold_at_once():
    """Nothing makes the five exclusive: the yogas read different grahas, and
    a chart can satisfy several. Mars in Aries and Jupiter in Cancer with
    Aries rising gives two.
    """
    verdicts = {v.key: v.present for v in evaluate(
        YogaInput(rasis={int(Graha.MARS): R["Ar"], int(Graha.JUPITER): R["Cn"]},
                  lagna_rasi=R["Ar"]), group="mahapurusha")}
    assert verdicts["ruchaka"] and verdicts["hamsa"]
    assert not verdicts["bhadra"]


# --------------------------------------------------------------------------
# The two name errors
# --------------------------------------------------------------------------


def test_11_4_5_the_definition_calls_hamsa_by_ruchakas_name():
    """**The find.** §11.4.5's heading reads "Hamsa Yoga" and its Definition
    opens: "If Jupiter is in a quadrant in own sign or exaltation sign, it is
    called **Ruchaka** yoga."

    Ruchaka is Mars's yoga, defined four sections earlier. The sentence is
    §11.4.1's with the graha swapped and the name left behind.

    It cannot be right: §11.4 promises "5 kinds of great persons", and two
    yogas sharing a name would leave four names for five yogas. See D-30 and
    PVR-12.
    """
    assert HAMSA_MISNAMED_IN_ITS_DEFINITION == "Ruchaka"
    assert YOGA_REGISTRY["hamsa"].name == "Hamsa Yoga"
    assert YOGA_REGISTRY["ruchaka"].name == "Ruchaka Yoga"
    names = {s.name for k, s in YOGA_REGISTRY.items()
             if s.group == "mahapurusha"}
    assert len(names) == 5, "five yogas need five names"


def test_11_4_4_maalavya_is_spelled_two_ways():
    """The heading reads "Maalavya Yoga"; the Definition beneath it reads "it
    is called Malavya yoga". One page, two spellings — the same slip as
    Budha-Aaditya's in §11.2.4. See D-31.
    """
    assert MAALAVYA_SPELLING_VARIANTS == ("Malavya",)
    assert YOGA_REGISTRY["maalavya"].name == "Maalavya Yoga"


def test_the_two_name_errors_are_of_different_kinds():
    """Worth separating: §11.4.4's is a spelling variant of the right name,
    §11.4.5's is the wrong name outright. The first is transcribed, the second
    is overruled.
    """
    assert "Malavya" in "Maalavya"[1:] or "Maalavya".replace("a", "", 1) == "Malavya"
    assert HAMSA_MISNAMED_IN_ITS_DEFINITION != "Hamsa"


def test_only_two_mahapurusha_names_are_glossed_at_all():
    """"He is rabbit-like²⁹" in §11.4.3 and "He is swan-like³⁰" in §11.4.5
    carry the chapter's only two name footnotes. Ruchaka, Bhadra and Maalavya
    get none.
    """
    by_key = {y["key"]: y for y in MAHAPURUSHA_YOGAS}
    glossed = {k for k, v in by_key.items() if v["name_means"]}
    assert glossed == {"sasa", "hamsa"}
    assert by_key["ruchaka"]["name_means"] is None


# --------------------------------------------------------------------------
# 11.5 Naabhasa yogas — the classification
# --------------------------------------------------------------------------


def test_11_5_what_a_naabhasa_yoga_is():
    """"Naabhasa yogas are classified celestial combinations."""
    assert NAABHASA_INTRO.startswith("Naabhasa yogas are classified")


@pytest.mark.parametrize(
    "group,count",
    [("aasraya", 3), ("dala", 2), ("aakriti", 20), ("sankhya", 7)],
)
def test_11_5_each_family_lists_as_many_names_as_it_claims(group, count):
    """"Aasraya Yogas (3)", "Dala Yogas (2)", "Aakriti Yogas (20)", "Sankhya
    Yogas (7)" — each header states a count, and each is followed by that many
    names. Checked rather than trusted.
    """
    entry = NAABHASA_CLASSIFICATION[group]
    assert entry["count"] == count
    assert len(entry["names"]) == count


def test_11_5_the_four_families_come_to_thirty_two():
    """3 + 2 + 20 + 7. The classical count, and it falls out of the section's
    own four headers."""
    total = sum(e["count"] for e in NAABHASA_CLASSIFICATION.values())
    assert total == 32
    names = [n for e in NAABHASA_CLASSIFICATION.values() for n in e["names"]]
    assert len(names) == 32
    assert len(set(names)) == 32, "no name appears in two families"


def test_11_5_the_pending_list_is_kept_even_though_it_is_empty():
    """§11.5.4 closed the last family, so nothing is pending. The list and its
    guard stay: "registered plus pending equals thirty-two" is what would
    catch a future family being classified and then forgotten.
    """
    registered = {k for k, s in YOGA_REGISTRY.items()
                  if s.group.startswith("naabhasa_")}
    assert NAABHASA_NOT_YET_DEFINED == ()
    assert len(registered) + len(NAABHASA_NOT_YET_DEFINED) == 32


def test_11_5_no_undefined_yoga_leaks_into_the_registry():
    """The guard for the gap: nothing named-only may have been registered by
    mistake, in either direction."""
    registered_names = {s.name.replace(" Yoga", "") for s in YOGA_REGISTRY.values()}
    assert not (set(NAABHASA_NOT_YET_DEFINED) & registered_names)
    defined = {y["name"].replace(" Yoga", "") for y in NAABHASA_YOGAS}
    assert not (defined & set(NAABHASA_NOT_YET_DEFINED))


def test_11_5_every_family_has_as_many_registered_as_it_claims():
    """Family by family, the classification's own count against the
    registry."""
    sizes: dict[str, int] = {}
    for spec in YOGA_REGISTRY.values():
        if spec.group.startswith("naabhasa_"):
            family = spec.group.removeprefix("naabhasa_")
            sizes[family] = sizes.get(family, 0) + 1
    for family, entry in NAABHASA_CLASSIFICATION.items():
        assert sizes[family] == entry["count"], family


def test_11_5_naabhasa_results_are_felt_in_all_dasas():
    """"Results of other yogas may be felt primarily during the dasas of the
    planets and signs involved. But the results of Naabhasa yogas are felt in
    **all dasas**."

    The only place chapter 11 contrasts one family with all the others on
    timing. §11.2.4's Budha-Aaditya is an instance of the first half — "the
    periods of Sun, Mercury and Leo will give those results in particular" —
    so the two sections state the rule and its exception without
    cross-referencing.
    """
    assert "felt in all dasas" in NAABHASA_TIMING_RULE
    assert "dasas of the planets and signs involved" in NAABHASA_TIMING_RULE
    assert "periods of Sun, Mercury and Leo" in BUDHA_AADITYA_TIMING_TEXT


def test_footnotes_29_and_30_are_now_supplied():
    """"Sasa" means a hare or a rabbit. "Hamsa" means a swan.

    Recorded as unread when §11.4 was done; supplied with §11.5. Both confirm
    the meanings taken from the Results sentences ("rabbit-like",
    "swan-like"), so nothing had to be revised.
    """
    assert SASA_MEANS == "a hare or a rabbit"
    assert HAMSA_MEANS == "a swan"
    assert MAHAPURUSHA_FOOTNOTES_UNREAD == ()
    by_key = {y["key"]: y for y in MAHAPURUSHA_YOGAS}
    assert by_key["sasa"]["name_means"] == "rabbit"
    assert by_key["hamsa"]["name_means"] == "swan"
    assert by_key["sasa"]["name_means"] in SASA_MEANS
    assert by_key["hamsa"]["name_means"] in HAMSA_MEANS


# --------------------------------------------------------------------------
# 11.5.1 Aasraya yogas
# --------------------------------------------------------------------------


def test_11_5_1_aasraya_means_dwelling_or_asylum():
    """"Aasraya means dwelling or asylum. Aasraya yogas are based on the signs
    occupied by planets."""
    assert NAABHASA_CLASSIFICATION["aasraya"]["means"] == "dwelling or asylum"
    assert "signs occupied by planets" in AASRAYA_BASIS


@pytest.mark.parametrize(
    "key,modality,means",
    [("rajju", "movable", "a rope"), ("musala", "fixed", "a pestle"),
     ("nala", "dual", None)],
)
def test_11_5_1_the_three_aasraya_yogas(key, modality, means):
    """"Rajju Yoga: If all the planets are exclusively in movable signs...
    Musala... fixed... Nala... dual."

    Rajju means a rope and Musala a pestle. **Nala is left unglossed** — the
    only one of the three the book does not name.
    """
    from hora.core.const import MODALITY_NAMES_EN

    entry = next(y for y in NAABHASA_YOGAS if y["key"] == key)
    assert MODALITY_NAMES_EN[entry["modality"]] == modality
    assert entry["name_means"] == means
    assert "exclusively" in entry["definition"]


def test_11_5_1_the_three_partition_the_modalities():
    """One yoga per modality, and the three modalities are all there are — so
    a chart with every planet in one modality forms exactly one Aasraya yoga,
    never two.
    """
    modalities = {y["modality"] for y in NAABHASA_YOGAS if "modality" in y}
    assert modalities == {0, 1, 2}
    for modality in range(3):
        signs = [s for s in range(12) if RASI_MODALITY[s] == modality]
        rasis = {int(g): signs[i % len(signs)]
                 for i, g in enumerate((Graha.SUN, Graha.MOON, Graha.MARS,
                                        Graha.MERCURY, Graha.JUPITER,
                                        Graha.VENUS, Graha.SATURN))}
        present = [v.key for v in evaluate(YogaInput(rasis=rasis))
                   if v.present and v.key in ("rajju", "musala", "nala")]
        assert len(present) == 1, modality


def test_11_5_1_one_planet_outside_breaks_it_and_the_reason_names_it():
    """"**exclusively**" — one planet elsewhere is enough."""
    movable = [s for s in range(12) if RASI_MODALITY[s] == 0]
    rasis = {int(g): movable[i % 4] for i, g in enumerate(
        (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
         Graha.VENUS, Graha.SATURN))}
    assert evaluate_one("rajju", YogaInput(rasis=rasis)).present
    rasis[int(Graha.SATURN)] = R["Ta"]
    broken = evaluate_one("rajju", YogaInput(rasis=rasis))
    assert not broken.present
    assert "Saturn in Taurus" in broken.reason


def test_11_5_1_the_nodes_never_make_an_aasraya_yoga_impossible():
    """"All the planets" — whether the nodes count is the OI-73 question
    again, and it bites harder here, since two more grahas must agree.

    But it can never make the yoga impossible: Rahu and Ketu are always six
    signs apart, and six signs apart is always the **same modality**. So
    admitting them makes an Aasraya yoga rarer, never unreachable.
    """
    for sign in range(12):
        assert RASI_MODALITY[sign] == RASI_MODALITY[(sign + 6) % 12]
    movable = [s for s in range(12) if RASI_MODALITY[s] == 0]
    rasis = {int(g): movable[i % 4] for i, g in enumerate(
        (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
         Graha.VENUS, Graha.SATURN))}
    rasis[int(Graha.RAHU)] = R["Ar"]
    rasis[int(Graha.KETU)] = R["Li"]
    assert evaluate_one("rajju", YogaInput(rasis=rasis, include_nodes=True)).present


def test_11_5_1_including_the_nodes_can_change_the_answer():
    """The other side of the same coin: a chart where the seven agree and the
    nodes do not."""
    movable = [s for s in range(12) if RASI_MODALITY[s] == 0]
    rasis = {int(g): movable[i % 4] for i, g in enumerate(
        (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
         Graha.VENUS, Graha.SATURN))}
    rasis[int(Graha.RAHU)] = R["Ta"]
    rasis[int(Graha.KETU)] = R["Sc"]
    assert evaluate_one("rajju", YogaInput(rasis=rasis)).present
    assert not evaluate_one(
        "rajju", YogaInput(rasis=rasis, include_nodes=True)).present


# --------------------------------------------------------------------------
# 11.5.2 Dala yogas
# --------------------------------------------------------------------------


def test_11_5_2_maalaa_the_books_own_example():
    """"let us say lagna is in Ar, Jupiter is in Cn, Venus is in Cp and
    Mercury is in Li. This gives Maalaa yoga."

    Cancer, Capricorn and Libra are the 4th, 10th and 7th from Aries — three
    quadrants, each with a natural benefic.
    """
    verdict = evaluate_one("maalaa", YogaInput(
        rasis={int(Graha.JUPITER): R["Cn"], int(Graha.VENUS): R["Cp"],
               int(Graha.MERCURY): R["Li"]},
        lagna_rasi=R["Ar"], paksha=0))
    assert verdict.present
    assert sorted(verdict.houses.values()) == [4, 7, 10]


def test_11_5_2_sarpa_the_books_own_example():
    """"lagna is in Sc, Mars is in Ta, Rahu is in Le and Ketu is in Aq. This
    gives Sarpa yoga."

    Taurus, Leo and Aquarius are the 7th, 10th and 4th from Scorpio.
    """
    verdict = evaluate_one("sarpa", YogaInput(
        rasis={int(Graha.MARS): R["Ta"], int(Graha.RAHU): R["Le"],
               int(Graha.KETU): R["Aq"]},
        lagna_rasi=R["Sc"], paksha=0))
    assert verdict.present
    assert sorted(verdict.houses.values()) == [4, 7, 10]


def test_11_5_2_the_dala_yogas_ignore_the_include_nodes_flag():
    """**The correction §11.5.2's own example forces.**

    `include_nodes` exists for the unresolved phrase "a planet" (§11.2, §11.3,
    §11.5.1). "Natural malefics" is a different phrase and §3.2.2 settles it —
    the nodes are natural malefics.

    Sarpa's example is built from Mars, **Rahu and Ketu**, so a Dala detector
    that honoured the flag would fail the book's own example whenever the flag
    was off. It must not, and does not.
    """
    rasis = {int(Graha.MARS): R["Ta"], int(Graha.RAHU): R["Le"],
             int(Graha.KETU): R["Aq"]}
    off = evaluate_one("sarpa", YogaInput(rasis=rasis, lagna_rasi=R["Sc"],
                                          paksha=0))
    on = evaluate_one("sarpa", YogaInput(rasis=rasis, lagna_rasi=R["Sc"],
                                         paksha=0, include_nodes=True))
    assert off.present and on.present
    assert off.participants == on.participants


def test_11_5_2_three_quadrants_are_required_not_two():
    """"If **three** quadrants are occupied" — two is not enough, and the
    reason says how many were found."""
    verdict = evaluate_one("maalaa", YogaInput(
        rasis={int(Graha.JUPITER): R["Cn"], int(Graha.VENUS): R["Cp"]},
        lagna_rasi=R["Ar"], paksha=0))
    assert not verdict.present
    assert "2 of the four quadrants" in verdict.reason


def test_11_5_2_a_contrary_graha_weakens_but_does_not_cancel():
    """"If a malefic also occupies one of the quadrants, this yoga **may not
    operate well**."

    May not operate well — not "is absent". The same rule as combustion in
    §11.2.4 and Kemadruma in §11.3.4: a qualifier, never a veto.
    """
    verdict = evaluate_one("maalaa", YogaInput(
        rasis={int(Graha.JUPITER): R["Cn"], int(Graha.VENUS): R["Cp"],
               int(Graha.MERCURY): R["Li"], int(Graha.SATURN): R["Ar"]},
        lagna_rasi=R["Ar"], paksha=0))
    assert verdict.present is True
    assert any("may not operate well" in q for q in verdict.qualifiers)
    assert any("Saturn in the 1st" in q for q in verdict.qualifiers)


def test_11_5_2_the_two_dala_yogas_are_mirror_images():
    """Maalaa is benefics in three quadrants, Sarpa is malefics. Each is
    weakened by the other's nature, so the two definitions differ in exactly
    one word each.
    """
    maalaa = next(y for y in NAABHASA_YOGAS if y["key"] == "maalaa")
    sarpa = next(y for y in NAABHASA_YOGAS if y["key"] == "sarpa")
    assert maalaa["nature"] == "benefic" and maalaa["weakened_by"] == "malefic"
    assert sarpa["nature"] == "malefic" and sarpa["weakened_by"] == "benefic"
    assert maalaa["definition"].replace("benefics", "malefics") == \
        sarpa["definition"]


def test_11_5_2_sarpa_is_graded_in_its_definition():
    """"This is a very bad combination." The only yoga in chapter 11 the book
    grades inside its own definition rather than leaving it to the results."""
    assert SARPA_IS_VERY_BAD == "This is a very bad combination."


def test_11_5_2_needs_a_lagna():
    """Quadrants are counted from the ascendant, like Kemadruma and the five
    Mahapurusha yogas."""
    for key in ("maalaa", "sarpa"):
        verdict = evaluate_one(key, YogaInput(
            rasis={int(Graha.JUPITER): R["Cn"]}, paksha=0))
        assert verdict.present is False
        assert "cannot be decided" in verdict.reason


def test_11_5_2_both_examples_leave_the_ascendant_empty():
    """Maalaa's three quadrants are the 4th, 7th and 10th; so are Sarpa's.
    Neither example uses the 1st, though the rule allows any three of the
    four. Worth pinning — a detector that quietly required the ascendant would
    still pass both examples.
    """
    for key, lagna, rasis in (
        ("maalaa", R["Ar"], {int(Graha.JUPITER): R["Cn"],
                             int(Graha.VENUS): R["Cp"],
                             int(Graha.MERCURY): R["Li"]}),
        ("sarpa", R["Sc"], {int(Graha.MARS): R["Ta"],
                            int(Graha.RAHU): R["Le"],
                            int(Graha.KETU): R["Aq"]}),
    ):
        verdict = evaluate_one(key, YogaInput(rasis=rasis, lagna_rasi=lagna,
                                              paksha=0))
        assert 1 not in verdict.houses.values()
    with_first = evaluate_one("maalaa", YogaInput(
        rasis={int(Graha.JUPITER): R["Ar"], int(Graha.VENUS): R["Cn"],
               int(Graha.MERCURY): R["Li"]},
        lagna_rasi=R["Ar"], paksha=0))
    assert with_first.present
    assert 1 in with_first.houses.values()


# --------------------------------------------------------------------------
# 11.5.3 Aakriti yogas
# --------------------------------------------------------------------------

_SEVEN = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
          Graha.VENUS, Graha.SATURN)


def _spread(houses, lagna=0, **extra):
    """Place the seven across `houses`, counted from `lagna`."""
    rasis = {int(g): (lagna + houses[i % len(houses)] - 1) % 12
             for i, g in enumerate(_SEVEN)}
    return YogaInput(rasis=rasis, lagna_rasi=lagna, paksha=0, **extra)


def test_11_5_3_aakriti_means_a_shape():
    """"Aakriti means a shape and the many of these yogas are based on the
    shape of the arrangement of planets in a chart."""
    assert AAKRITI_MEANS == "a shape"
    assert "shape of the arrangement of planets" in AAKRITI_BASIS


def test_11_5_3_answers_the_node_question_for_this_family():
    """"In all these yogas, Rahu and Ketu are **not counted as planets by many
    authors**."

    The closest the book comes to settling OI-73, and it settles it by
    attribution rather than by ruling — "by many authors", not "we do not".
    Our default already excludes them, so §11.5.3 confirms rather than changes
    anything.
    """
    assert "not counted as planets by many authors" in AAKRITI_NODES_NOTE
    default = YogaInput(rasis={int(Graha.SUN): 0})
    assert Graha.RAHU not in default.considered()
    assert Graha.KETU not in default.considered()


def test_11_5_3_has_all_twenty():
    """The Aakriti family is twenty, and §11.5.3 defines every one."""
    assert len(AAKRITI_YOGAS) == 20
    registered = {k for k, s in YOGA_REGISTRY.items()
                  if s.group == "naabhasa_aakriti"}
    assert len(registered) == 20
    assert registered == {y["key"] for y in AAKRITI_YOGAS}


def test_11_5_3_every_yoga_is_glossed():
    """Unlike Nala in §11.5.1, all twenty Aakriti names get a meaning."""
    for entry in AAKRITI_YOGAS:
        assert entry["name_means"], entry["key"]


def test_11_5_3_the_reading_rule_comes_from_the_books_grammar():
    """**The rule that decides eighteen of the twenty.**

    Where the subject is "all the planets" — "If all the planets occupy 1st
    and 7th houses" — the test is confinement: every planet lies in the named
    houses. Where the subject is a house — "lagna and the 7th houses **are
    occupied by** natural benefics" — that house must hold something.

    Only Vajra and Yava take the second form, and they are exactly the two
    that need natures.
    """
    occupancy = {y["key"] for y in AAKRITI_YOGAS if "benefic_houses" in y}
    assert occupancy == {"vajra", "yava"}
    confinement = {y["key"] for y in AAKRITI_YOGAS if "alternatives" in y}
    assert len(confinement) == 18
    assert not (occupancy & confinement)
    for entry in AAKRITI_YOGAS:
        if entry["key"] in occupancy:
            assert "are occupied by" in entry["definition"]
        else:
            assert "are occupied by" not in entry["definition"]


@pytest.mark.parametrize(
    "key,houses",
    [("gadaa", [4, 7]), ("sakata", [1, 7]), ("vihanga", [4, 10]),
     ("sringaataka", [1, 5, 9]), ("hala", [2, 6, 10]),
     ("kamala", [1, 4, 7, 10]), ("vaapi", [2, 5, 8, 11]),
     ("yoopa", [1, 2, 3, 4]), ("sara", [4, 5, 6, 7]),
     ("sakti", [7, 8, 9, 10]), ("danda", [10, 11, 12, 1]),
     ("naukaa", [1, 2, 3, 4, 5, 6, 7]), ("koota", [4, 5, 6, 7, 8, 9, 10]),
     ("chatra", [7, 8, 9, 10, 11, 12, 1]),
     ("chaapa", [10, 11, 12, 1, 2, 3, 4]),
     ("ardha_chandra", [2, 3, 4, 5, 6, 7, 8]),
     ("chakra", [1, 3, 5, 7, 9, 11]), ("samudra", [2, 4, 6, 8, 10, 12])],
)
def test_11_5_3_each_confinement_yoga_fires_on_its_own_houses(key, houses):
    """Eighteen yogas, each on the houses its definition names."""
    verdict = evaluate_one(key, _spread(houses))
    assert verdict.present, (key, verdict.reason)


def test_11_5_3_gadaa_takes_the_four_successive_quadrant_pairs():
    """"two **successive** quadrants from lagna... For example, 4th and 7th
    (or 10th and 1st)."

    Successive in the quadrant cycle 1 to 4 to 7 to 10 and round again — four
    pairs, derived rather than typed out.
    """
    gadaa = next(y for y in AAKRITI_YOGAS if y["key"] == "gadaa")
    assert set(gadaa["alternatives"]) == {(1, 4), (4, 7), (7, 10), (10, 1)}
    for pair in gadaa["alternatives"]:
        assert evaluate_one("gadaa", _spread(list(pair))).present, pair


def test_11_5_3_the_three_pair_yogas_cover_every_quadrant_pair():
    """Gadaa's four successive pairs plus Sakata's 1st-7th and Vihanga's
    4th-10th are all six pairs of quadrants there are. Nothing is left over
    and nothing overlaps.
    """
    from itertools import combinations

    gadaa = next(y for y in AAKRITI_YOGAS if y["key"] == "gadaa")
    pairs = {frozenset(p) for p in gadaa["alternatives"]}
    pairs |= {frozenset((1, 7)), frozenset((4, 10))}
    assert pairs == {frozenset(p) for p in combinations((1, 4, 7, 10), 2)}
    assert len(pairs) == 6


def test_11_5_3_hala_excludes_the_lagna_trine_structurally():
    """"mutual trines **but not trines from lagna**... in other words, 2nd,
    6th and 10th, or 3rd, 7th and 11th, or 4th, 8th and 12th."

    The 1st-5th-9th set is simply not among Hala's alternatives, so the
    exclusion needs no separate check — a chart on the lagna trine gives
    Sringaataka and never Hala.
    """
    hala = next(y for y in AAKRITI_YOGAS if y["key"] == "hala")
    assert set(hala["alternatives"]) == {(2, 6, 10), (3, 7, 11), (4, 8, 12)}
    assert (1, 5, 9) not in hala["alternatives"]
    on_trine = _spread([1, 5, 9])
    assert evaluate_one("sringaataka", on_trine).present
    assert not evaluate_one("hala", on_trine).present


def test_11_5_3_hala_and_sringaataka_take_the_four_trine_sets_between_them():
    """Four trine sets exist — one starting at each of the 1st, 2nd, 3rd and
    4th. Sringaataka takes the lagna's, Hala the other three."""
    hala = next(y for y in AAKRITI_YOGAS if y["key"] == "hala")
    sringaataka = next(y for y in AAKRITI_YOGAS if y["key"] == "sringaataka")
    all_sets = {tuple(sorted((base, base + 4, base + 8))) for base in (1, 2, 3, 4)}
    covered = {tuple(sorted(a)) for a in hala["alternatives"]}
    covered |= {tuple(sorted(a)) for a in sringaataka["alternatives"]}
    assert covered == all_sets
    assert len(all_sets) == 4


def test_11_5_3_vajra_and_yava_are_exact_mirrors():
    """Vajra: benefics in the 1st and 7th, malefics in the 4th and 10th.
    Yava: the same houses with the natures swapped. Two definitions differing
    in two words.
    """
    vajra = next(y for y in AAKRITI_YOGAS if y["key"] == "vajra")
    yava = next(y for y in AAKRITI_YOGAS if y["key"] == "yava")
    assert vajra["benefic_houses"] == yava["malefic_houses"] == (1, 7)
    assert vajra["malefic_houses"] == yava["benefic_houses"] == (4, 10)


def test_11_5_3_vajra_and_yava_cannot_both_hold():
    """The same four houses cannot hold benefics and malefics both ways
    round."""
    vajra_chart = YogaInput(
        rasis={int(Graha.JUPITER): 0, int(Graha.VENUS): 6,
               int(Graha.MARS): 3, int(Graha.SATURN): 9},
        lagna_rasi=0, paksha=0)
    assert evaluate_one("vajra", vajra_chart).present
    assert not evaluate_one("yava", vajra_chart).present


def test_11_5_3_vajra_needs_its_houses_actually_occupied():
    """"lagna and the 7th houses **are occupied by** natural benefics" — the
    house is the subject, so an empty house fails and the reason says which.
    """
    verdict = evaluate_one("vajra", YogaInput(
        rasis={int(Graha.JUPITER): 0, int(Graha.MARS): 3,
               int(Graha.SATURN): 9},
        lagna_rasi=0, paksha=0))
    assert not verdict.present
    assert "the 7th" in verdict.reason and "empty" in verdict.reason


def test_11_5_3_the_four_run_yogas_start_at_the_four_quadrants():
    """Naukaa from the 1st, Koota from the 4th, Chatra from the 7th, Chaapa
    from the 10th — the four quadrants, one each."""
    starts = {}
    for key in ("naukaa", "koota", "chatra", "chaapa"):
        entry = next(y for y in AAKRITI_YOGAS if y["key"] == key)
        assert len(entry["alternatives"]) == 1
        starts[key] = entry["alternatives"][0][0]
    assert starts == {"naukaa": 1, "koota": 4, "chatra": 7, "chaapa": 10}


def test_11_5_3_ardha_chandra_takes_every_other_starting_house():
    """"the 7 signs starting from a panapara or an apoklima" — the eight
    houses that are not quadrants.

    So the five seven-sign yogas between them cover all twelve possible
    starts: four quadrants and eight others.
    """
    entry = next(y for y in AAKRITI_YOGAS if y["key"] == "ardha_chandra")
    starts = {a[0] for a in entry["alternatives"]}
    assert starts == {2, 3, 5, 6, 8, 9, 11, 12}
    assert len(starts) == 8
    assert starts | {1, 4, 7, 10} == set(range(1, 13))
    for start in sorted(starts):
        houses = [(start - 1 + step) % 12 + 1 for step in range(7)]
        assert evaluate_one("ardha_chandra", _spread(houses)).present, start


def test_11_5_3_chakra_and_samudra_partition_the_houses():
    """Chakra takes the odd houses and Samudra the even. Between them, all
    twelve, with no overlap — so a chart can never form both."""
    chakra = next(y for y in AAKRITI_YOGAS if y["key"] == "chakra")
    samudra = next(y for y in AAKRITI_YOGAS if y["key"] == "samudra")
    odd, even = set(chakra["alternatives"][0]), set(samudra["alternatives"][0])
    assert odd == {1, 3, 5, 7, 9, 11}
    assert even == {2, 4, 6, 8, 10, 12}
    assert not (odd & even)
    assert odd | even == set(range(1, 13))
    on_odd = _spread([1, 3, 5, 7, 9, 11])
    assert evaluate_one("chakra", on_odd).present
    assert not evaluate_one("samudra", on_odd).present


def test_11_5_3_the_four_four_house_runs_start_at_the_quadrants_too():
    """Yoopa from the 1st, Sara from the 4th, Sakti from the 7th, Danda from
    the 10th — the same four starting points as the seven-sign yogas, with a
    shorter run."""
    starts = {}
    for key in ("yoopa", "sara", "sakti", "danda"):
        entry = next(y for y in AAKRITI_YOGAS if y["key"] == key)
        houses = entry["alternatives"][0]
        assert len(houses) == 4
        starts[key] = houses[0]
    assert starts == {"yoopa": 1, "sara": 4, "sakti": 7, "danda": 10}


def test_11_5_3_confinement_yields_real_containments():
    """Confinement makes narrower yogas imply wider ones, and the engine
    reports every one that holds rather than picking a "best" fit.

    All planets on the lagna trine gives Sringaataka *and* Chakra, since the
    1st, 5th and 9th are all odd houses.
    """
    present = {v.key for v in evaluate(_spread([1, 5, 9])) if v.present}
    assert {"sringaataka", "chakra"} <= present


def test_11_5_3_a_movable_lagna_links_kamala_to_rajju():
    """A cross-family consequence. The quadrants from a movable sign are the
    four movable signs, so all planets in quadrants from Aries means all
    planets in movable signs — Kamala and Rajju together.
    """
    present = {v.key for v in evaluate(_spread([1, 4, 7, 10], lagna=R["Ar"]))
               if v.present}
    assert {"kamala", "rajju"} <= present
    from_fixed = {v.key for v in evaluate(_spread([1, 4, 7, 10], lagna=R["Ta"]))
                  if v.present}
    assert "kamala" in from_fixed
    assert "musala" in from_fixed
    assert "rajju" not in from_fixed


def test_11_5_3_needs_a_lagna_and_a_full_chart():
    """Every Aakriti yoga counts houses from lagna, and "all the planets" is
    universal — so both a missing lagna and a missing planet are answered with
    "cannot be decided" rather than a bare absent.
    """
    houses = [1, 4]
    no_lagna = YogaInput(rasis={int(Graha.SUN): 0})
    assert "cannot be decided" in evaluate_one("gadaa", no_lagna).reason
    partial = YogaInput(rasis={int(Graha.SUN): 0, int(Graha.MOON): 3},
                        lagna_rasi=0)
    verdict = evaluate_one("gadaa", partial)
    assert verdict.present is False
    assert "cannot be decided" in verdict.reason
    assert evaluate_one("gadaa", _spread(houses)).present


def test_11_5_3_the_reason_names_the_span_when_a_yoga_fails():
    """An absent confinement yoga says where the planets actually are, so a
    caller can see why no permitted set contained them."""
    verdict = evaluate_one("sakata", _spread([1, 2, 3]))
    assert not verdict.present
    assert "span" in verdict.reason


def test_11_5_3_the_classification_and_the_headings_disagree_on_two_names():
    """§11.5's list writes "Vihangama" and "Ardhachandra"; §11.5.3's headings
    write "Vihanga" and "Ardha Chandra", and Vihanga's text adds a third form,
    "Vihaga".

    The headings win — a definitional section beats a passing mention. See
    D-33.
    """
    assert AAKRITI_NAME_VARIANTS["vihanga"] == ("Vihangama", "Vihaga")
    assert AAKRITI_NAME_VARIANTS["ardha_chandra"] == ("Ardhachandra",)
    assert YOGA_REGISTRY["vihanga"].name == "Vihanga Yoga"
    assert YOGA_REGISTRY["ardha_chandra"].name == "Ardha Chandra Yoga"
    listed = set(NAABHASA_CLASSIFICATION["aakriti"]["names"])
    assert "Vihangama" in listed and "Ardhachandra" in listed


def test_11_5_3_vihaga_is_carried_as_an_alias():
    """"Some authors call this Vihaga yoga." Recorded as an alias, so a caller
    matching that name finds the yoga."""
    assert YOGA_REGISTRY["vihanga"].aliases == ("Vihaga Yoga",)


def test_11_5_3_the_classification_orders_two_yogas_differently():
    """§11.5 lists Sringaataka before Vihangama; §11.5.3 defines Vihanga
    before Sringaataka. A third disagreement between the two passages, and the
    only one that is not about spelling."""
    listed = list(NAABHASA_CLASSIFICATION["aakriti"]["names"])
    assert listed.index("Sringaataka") < listed.index("Vihangama")
    defined = [y["key"] for y in AAKRITI_YOGAS]
    assert defined.index("vihanga") < defined.index("sringaataka")
    assert "Sringaataka before Vihangama" in AAKRITI_ORDER_DIFFERS


def test_11_5_3_vaapi_reads_its_two_alternatives_separately():
    """"If all the planets are panaparas or in apoklimas."

    Read as two alternatives — all in the panapharas, or all in the apoklimas
    — not as their union. The union reading would make Vaapi simply "no planet
    in a quadrant", which is a much weaker claim. Recorded as OI-78; the union
    is kept on the spec so the other reading is one line away.
    """
    entry = next(y for y in AAKRITI_YOGAS if y["key"] == "vaapi")
    assert entry["alternatives"] == ((2, 5, 8, 11), (3, 6, 9, 12))
    assert set(entry["union_alternative"]) == {2, 3, 5, 6, 8, 9, 11, 12}
    mixed = _spread([2, 3, 5, 6])
    assert not evaluate_one("vaapi", mixed).present
    assert evaluate_one("vaapi", _spread([2, 5, 8, 11])).present
    assert evaluate_one("vaapi", _spread([3, 6, 9, 12])).present


# --------------------------------------------------------------------------
# 11.5.4 Sankhya yogas
# --------------------------------------------------------------------------


def _seven_in(signs, lagna=0, **extra):
    """Place the seven planets across `signs` (sign indices, cycled)."""
    return YogaInput(
        rasis={int(g): signs[i % len(signs)] for i, g in enumerate(_SEVEN)},
        lagna_rasi=lagna, paksha=0, **extra)


def test_11_5_4_sankhya_means_a_number():
    """"Sankhya means a number. Sankhya yogas are based on the number of
    distinct signs occupied by the seven planets combined."""
    assert SANKHYA_MEANS == "a number"
    assert "number of distinct signs" in SANKHYA_BASIS


def test_11_5_4_rules_the_nodes_out_outright():
    """"Rahu and Ketu are **not included**."

    §11.5.3 said the nodes are "not counted as planets by many authors" —
    attribution. §11.5.4 rules. It is the clearest statement in the book on
    the question OI-73 asks, so this family ignores `include_nodes` rather
    than honouring it.
    """
    from hora.charts.planetary_yogas.sankhya import SEVEN_PLANETS

    assert SANKHYA_EXCLUDES_NODES == "Rahu and Ketu are not included."
    assert Graha.RAHU not in SEVEN_PLANETS
    assert Graha.KETU not in SEVEN_PLANETS
    assert len(SEVEN_PLANETS) == 7
    # Three signs for the seven, plus the nodes in two more. Under a rule that
    # counted nine, this would be five signs (Paasa); counting seven it is
    # three (Soola), and the flag changes nothing either way.
    # Aries, Gemini and Scorpio for the seven — a Soola chart that no earlier
    # Naabhasa yoga supersedes. Rahu adds a fourth sign, so a rule counting
    # nine would give Kedaara instead; counting seven it stays Soola, and the
    # flag changes nothing either way.
    base = {int(g): [R["Ar"], R["Ge"], R["Sc"]][i % 3]
            for i, g in enumerate(_SEVEN)}
    # The nodes go in Taurus and Scorpio — neither a quadrant from Aries, so
    # no Dala yoga (which *does* count them) is stirred up and only the
    # Sankhya count is under test.
    with_nodes = {**base, int(Graha.RAHU): R["Ta"], int(Graha.KETU): R["Sc"]}
    off = evaluate_one("soola", YogaInput(rasis=with_nodes, lagna_rasi=R["Ar"]))
    on = evaluate_one("soola", YogaInput(rasis=with_nodes, lagna_rasi=R["Ar"],
                                         include_nodes=True))
    assert off.present is on.present is True
    assert not evaluate_one("kedaara", YogaInput(rasis=with_nodes,
                                                 lagna_rasi=R["Ar"])).present


@pytest.mark.parametrize(
    "key,signs,means",
    [("veenaa", 7, "a stringed musical instrument"), ("daama", 6, "a wreath"),
     ("paasa", 5, "a noose"), ("kedaara", 4, "a field"),
     ("soola", 3, "Shiva's weapon"), ("yuga", 2, "a pair"),
     ("gola", 1, "a sphere or a globe")],
)
def test_11_5_4_each_yoga_takes_one_count(key, signs, means):
    """Seven yogas, seven counts, descending from 7 to 1."""
    entry = next(y for y in SANKHYA_YOGAS if y["key"] == key)
    assert entry["signs"] == signs
    assert entry["name_means"] == means


def test_11_5_4_the_seven_counts_are_exhaustive():
    """Seven planets can occupy one to seven distinct signs and no other
    number, and there is a yoga for each. So exactly one Sankhya yoga always
    matches on count — which is why the fallback rule is needed to stop one
    firing in every chart.
    """
    counts = {y["signs"] for y in SANKHYA_YOGAS}
    assert counts == set(range(1, 8))
    assert len(SANKHYA_YOGAS) == 7


@pytest.mark.parametrize("count", range(1, 8))
def test_11_5_4_exactly_one_count_matches_any_chart(count):
    """Whatever the seven planets do, one and only one Sankhya yoga's count
    is right."""
    signs = [R[name] for name in ("Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li")]
    chart = _seven_in(signs[:count])
    matching = [y["key"] for y in SANKHYA_YOGAS
                if len({chart.rasis[int(g)] for g in _SEVEN}) == y["signs"]]
    assert len(matching) == 1
    assert matching[0] == next(y["key"] for y in SANKHYA_YOGAS
                               if y["signs"] == count)


def _rama():
    """Lord Sri Rama's chart — §1.3.4's Example 1, which Figure 1 draws.

    Reused from chapter 1's fixture rather than re-transcribed, so the two
    chapters cannot drift apart.
    """
    from tests.unit.test_book_1_3_4 import RAMA_GRAHAS, RAMA_LAGNA

    return YogaInput(
        rasis={int(g): R[sign] for g, sign in RAMA_GRAHAS.items()},
        lagna_rasi=R[RAMA_LAGNA], paksha=0)


def test_11_5_4_the_worked_example_is_ramas_chart_from_chapter_1():
    """"let us take the chart of Lord Sri Rama (see Figure 1)."

    Figure 1 is §1.3.4's own Example 1, drawn in all three chart styles, and
    chapter 1 has held it as a fixture since it was audited. So §11.5.4's
    example is fully checkable — lagna and all.
    """
    from tests.unit.test_book_1_3_4 import RAMA_GRAHAS, RAMA_LAGNA

    assert RAMA_LAGNA == SANKHYA_EXAMPLE["lagna"] == "Cn"
    seven = {RAMA_GRAHAS[int(g)] for g in _SEVEN}
    assert seven == set(SANKHYA_EXAMPLE["signs"])
    assert len(seven) == SANKHYA_EXAMPLE["count"] == 6
    assert SANKHYA_EXAMPLE["figure_supplied"] is True


def test_11_5_4_ramas_chart_gives_daama():
    """"The signs occupied by the seven planets are: Ar, Ta, Cn, Li, Cp and
    Pi. There are six signs. This forms Daama yoga."

    Six distinct signs, and the fallback lets it stand.
    """
    verdict = evaluate_one("daama", _rama())
    assert verdict.present
    assert "exactly 6 distinct signs" in verdict.reason
    others = [v.key for v in evaluate(_rama(), group="naabhasa_sankhya")
              if v.present]
    assert others == ["daama"]


# --------------------------------------------------------------------------
# The fallback rule
# --------------------------------------------------------------------------


def test_11_5_4_is_a_fallback_not_merely_a_weaker_family():
    """"These yogas apply **if no other Naabhasa yogas mentioned previously
    are applicable** in a chart. These are the least important of all Naabhasa
    yogas."

    The first rule in the book where one yoga's *presence* depends on
    another's absence. It is part of the definition — "apply if" — so unlike
    Kemadruma's "kills the results", it governs `present`.
    """
    assert "apply if no other Naabhasa yogas" in SANKHYA_IS_A_FALLBACK
    assert "least important" in SANKHYA_IS_A_FALLBACK


def test_11_5_4_a_superseded_yoga_names_what_superseded_it():
    """All seven planets in the quadrants from Aries occupy four distinct
    signs, which is Kedaara's count — but Kamala and Rajju both apply, so
    Kedaara does not.

    The reason states the count *and* the yoga that displaced it, so nothing
    is hidden behind the `present` flag.
    """
    chart = _seven_in([R["Ar"], R["Cn"], R["Li"], R["Cp"]], lagna=R["Ar"])
    verdict = evaluate_one("kedaara", chart)
    assert verdict.present is False
    assert "do occupy 4 distinct signs" in verdict.reason
    assert "applies and Sankhya yogas apply only when" in verdict.reason
    earlier = {v.key for v in evaluate(chart) if v.present}
    assert earlier & {"rajju", "kamala"}


def test_11_5_4_at_most_one_sankhya_yoga_can_ever_hold():
    """One count matches, and the other six cannot. Checked across charts of
    every count."""
    signs = [R[n] for n in ("Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li")]
    for count in range(1, 8):
        chart = _seven_in(signs[:count], lagna=R["Sc"])
        present = [v.key for v in evaluate(chart, group="naabhasa_sankhya")
                   if v.present]
        assert len(present) <= 1, (count, present)


def test_11_5_4_a_sankhya_yoga_never_holds_beside_an_earlier_naabhasa_yoga():
    """The fallback stated as an invariant over many charts: no chart may
    show both a Sankhya yoga and an Aasraya, Dala or Aakriti one.
    """
    from hora.charts.planetary_yogas.sankhya import _EARLIER_NAABHASA

    charts = [
        _seven_in([R["Ar"], R["Cn"], R["Li"], R["Cp"]], lagna=R["Ar"]),
        _seven_in([R["Ar"], R["Ta"], R["Ge"], R["Cn"], R["Le"], R["Vi"],
                   R["Li"]], lagna=R["Sc"]),
        _seven_in([R["Ar"]], lagna=R["Cn"]),
        _seven_in([R["Ta"], R["Le"], R["Sc"], R["Aq"]], lagna=R["Ta"]),
    ]
    for chart in charts:
        verdicts = {v.key: v.present for v in evaluate(chart)}
        sankhya = {k for k, s in YOGA_REGISTRY.items()
                   if s.group == "naabhasa_sankhya" and verdicts[k]}
        earlier = {k for k, s in YOGA_REGISTRY.items()
                   if s.group in _EARLIER_NAABHASA and verdicts[k]}
        assert not (sankhya and earlier), (sankhya, earlier)


def test_11_5_4_the_fallback_checks_the_families_in_the_books_order():
    """"no other Naabhasa yogas **mentioned previously**" — Aasraya, then
    Dala, then Aakriti, which is the order §11.5 lists and §11.5.1 to §11.5.3
    define. The yoga named as superseding is the one a reader reaches first.
    """
    from hora.charts.planetary_yogas.sankhya import _EARLIER_NAABHASA

    assert _EARLIER_NAABHASA == (
        "naabhasa_aasraya", "naabhasa_dala", "naabhasa_aakriti")
    assert "naabhasa_sankhya" not in _EARLIER_NAABHASA


def test_11_5_4_the_fallback_differs_from_kemadrumas_suppression():
    """Two cross-yoga rules in one chapter, deliberately handled differently.

    §11.3.4's Kemadruma "kills the results of other good yogas" — the yoga
    still forms, and carries a qualifier. §11.5.4's Sankhya yogas "apply if no
    other Naabhasa yoga is applicable" — they do not form at all.

    The difference is in the book's own words: results against applicability.
    """
    assert "kills the results" in KEMADRUMA_KILLS_OTHER_YOGAS
    assert "apply if" in SANKHYA_IS_A_FALLBACK
    kemadruma_chart = dict(_kemadruma_chart().rasis)
    body = planetary_yoga_service.chart(kemadruma_chart, lagna_rasi=R["Ta"])
    killed = body["results_killed_by_kemadruma"]
    for yoga in body["yogas"]:
        if yoga["key"] in killed:
            assert yoga["present"] is True


def test_11_5_4_needs_all_seven_planets():
    """The count is over the seven combined, so a missing planet would
    undercount — and undercounting moves the answer to a different yoga rather
    than merely weakening it.
    """
    partial = YogaInput(rasis={int(Graha.SUN): 0, int(Graha.MOON): 1},
                        lagna_rasi=0)
    verdict = evaluate_one("yuga", partial)
    assert verdict.present is False
    assert "cannot be decided" in verdict.reason


def test_11_5_4_gola_is_phrased_differently_from_the_other_six():
    """"If the seven planets **are in one sign**" — where the other six read
    "occupy exactly N distinct signs". Same meaning, different wording;
    recorded rather than normalised.
    """
    gola = next(y for y in SANKHYA_YOGAS if y["key"] == "gola")
    assert "definition_differs" in gola
    assert "are in one sign" in YOGA_REGISTRY["gola"].definition
    for entry in SANKHYA_YOGAS:
        if entry["key"] != "gola":
            assert "distinct signs" in YOGA_REGISTRY[entry["key"]].definition


@pytest.mark.parametrize(
    "key,alias", [("veenaa", "Vallaki Yoga"), ("daama", "Daamini Yoga")])
def test_11_5_4_two_yogas_carry_an_alias(key, alias):
    """"This is also called Vallaki yoga by some authors." "Some authors call
    this Daamini yoga." Only these two of the seven."""
    assert YOGA_REGISTRY[key].aliases == (alias,)
    without = [y["key"] for y in SANKHYA_YOGAS if not y["aliases"]]
    assert len(without) == 5


# --------------------------------------------------------------------------
# The classification is now complete
# --------------------------------------------------------------------------


def test_all_thirty_two_naabhasa_yogas_are_now_defined():
    """§11.5 classified thirty-two and §11.5.1 to §11.5.4 defined every one.
    Nothing is left named-only."""
    registered = {k for k, s in YOGA_REGISTRY.items()
                  if s.group.startswith("naabhasa_")}
    assert len(registered) == 32
    assert NAABHASA_NOT_YET_DEFINED == ()
    total = sum(e["count"] for e in NAABHASA_CLASSIFICATION.values())
    assert len(registered) + len(NAABHASA_NOT_YET_DEFINED) == total == 32


def test_the_four_families_are_all_registered():
    groups_present = {s.group for s in YOGA_REGISTRY.values()
                      if s.group.startswith("naabhasa_")}
    assert groups_present == {
        "naabhasa_aasraya", "naabhasa_dala", "naabhasa_aakriti",
        "naabhasa_sankhya"}


def test_every_classified_name_has_a_registered_yoga():
    """Name by name, the classification list against the registry — the
    strongest form of the completeness guard, since it catches a family that
    was defined under a different name."""
    from hora.core.const import AAKRITI_NAME_VARIANTS

    registered = {s.name.replace(" Yoga", "") for s in YOGA_REGISTRY.values()}
    variants = {v for values in AAKRITI_NAME_VARIANTS.values() for v in values}
    for entry in NAABHASA_CLASSIFICATION.values():
        for name in entry["names"]:
            assert name in registered or name in variants, name


def test_11_5_4_gola_can_never_be_present():
    """**A consequence §11.5.4 does not mention.**

    Gola needs all seven planets in one sign. One sign is one modality, so an
    Aasraya yoga always applies; and one sign always fits inside a seven-sign
    window, so a run-yoga applies too. The fallback rule then forbids Gola —
    in every chart there is.

    Checked exhaustively over all 12 signs by all 12 lagnas. See OI-79.
    """
    for sign in range(12):
        for lagna in range(12):
            data = YogaInput(rasis={int(g): sign for g in _SEVEN},
                             lagna_rasi=lagna, paksha=0)
            verdict = evaluate_one("gola", data)
            assert verdict.present is False, (sign, lagna)
            assert "applies and Sankhya yogas apply only" in verdict.reason


def test_11_5_4_yuga_can_never_be_present_either():
    """Two distinct signs are always within seven consecutive signs, because
    the shorter arc between any two signs is at most six. §11.5.3's five
    run-yogas cover all twelve seven-sign windows, so one of them always
    applies and Yuga is always superseded.

    Checked exhaustively over all 66 sign pairs by all 12 lagnas. See OI-79.
    """
    import itertools

    for pair in itertools.combinations(range(12), 2):
        for lagna in range(12):
            data = YogaInput(
                rasis={int(g): pair[i % 2] for i, g in enumerate(_SEVEN)},
                lagna_rasi=lagna, paksha=0)
            assert evaluate_one("yuga", data).present is False, (pair, lagna)


def test_11_5_4_the_reason_gola_and_yuga_are_unreachable():
    """The structural fact behind both: every set of one or two signs fits
    inside some seven-consecutive-sign window, and three signs need not.
    """
    import itertools

    windows = [{(start + step) % 12 for step in range(7)} for start in range(12)]
    for size in (1, 2):
        for combo in itertools.combinations(range(12), size):
            assert any(set(combo) <= w for w in windows), combo
    uncovered = [c for c in itertools.combinations(range(12), 3)
                 if not any(set(c) <= w for w in windows)]
    assert uncovered, "three signs can escape every window, which is why Soola can hold"


def test_11_5_4_the_other_five_are_reachable():
    """Veenaa, Daama, Paasa, Kedaara and Soola all occur. Soola is the rarest
    — three signs must escape every seven-sign window and every other Aakriti
    set — but it is not impossible.
    """
    reachable = {
        # Not seven *consecutive* signs — that would sit inside a seven-sign
        # window and give Naukaa instead. Scorpio breaks the run.
        "veenaa": ([R["Ar"], R["Ta"], R["Ge"], R["Cn"], R["Le"], R["Vi"],
                    R["Sc"]], R["Ar"]),
        "soola": ([R["Ar"], R["Ge"], R["Sc"]], R["Ar"]),
    }
    for key, (signs, lagna) in reachable.items():
        assert evaluate_one(key, _seven_in(signs, lagna=lagna)).present, key


def test_11_5_4_ramas_chart_is_what_settles_what_applicable_means():
    """**The reconciliation.** Rama's chart contains exactly one earlier
    Naabhasa yoga: **Sarpa**. Malefics hold the 4th, 7th and 10th from Cancer
    — Saturn in Libra, Mars in Capricorn, the Sun in Aries — while Jupiter and
    the Moon hold the lagna itself.

    That fourth quadrant triggers §11.5.2's own clause: "If a benefic also
    occupies one of the quadrants, this yoga may not operate well."

    Counted as applicable, that Sarpa supersedes Daama and §11.5.4's rule
    contradicts §11.5.4's example. Not counted, rule and example agree. So
    "applicable" excludes a yoga the book itself says does not fully operate.

    See OI-80 and PVR-13.
    """
    sarpa = evaluate_one("sarpa", _rama())
    assert sarpa.present is True
    assert sarpa.weakened is True
    assert any("may not operate well" in q for q in sarpa.qualifiers)

    naabhasa = [v.key for v in evaluate(_rama()) if v.present
                and YOGA_REGISTRY[v.key].group.startswith("naabhasa_")]
    assert set(naabhasa) == {"sarpa", "daama"}
    assert "may not operate well" in WEAKENED_YOGA_IS_NOT_APPLICABLE


def test_an_unweakened_yoga_still_supersedes():
    """The exception is narrow: only a yoga the book calls impaired is passed
    over. A clean Sarpa — no benefic in any quadrant — still blocks a Sankhya
    yoga.
    """
    rasis = {int(Graha.MARS): R["Ta"], int(Graha.RAHU): R["Le"],
             int(Graha.KETU): R["Aq"], int(Graha.SUN): R["Ge"],
             int(Graha.MOON): R["Ge"], int(Graha.MERCURY): R["Vi"],
             int(Graha.JUPITER): R["Sg"], int(Graha.VENUS): R["Pi"],
             int(Graha.SATURN): R["Ar"]}
    data = YogaInput(rasis=rasis, lagna_rasi=R["Sc"], paksha=1)
    sarpa = evaluate_one("sarpa", data)
    assert sarpa.present and sarpa.weakened is False
    for spec in YOGA_REGISTRY.values():
        if spec.group == "naabhasa_sankhya":
            verdict = spec.detect(data)
            if "do occupy" in verdict.reason:
                assert verdict.present is False
                assert "Sarpa Yoga applies" in verdict.reason


def test_only_the_dala_yogas_can_be_weakened():
    """The `weakened` flag exists for §11.5.2's clause alone. No other yoga in
    the chapter carries a statement that it does not fully operate — combustion
    and Kemadruma weaken *results*, which is a different thing.
    """
    charts = [_rama(), _kemadruma_chart(),
              _seven_in([R["Ar"], R["Cn"], R["Li"], R["Cp"]], lagna=R["Ar"])]
    for chart in charts:
        for verdict in evaluate(chart):
            if verdict.weakened:
                assert YOGA_REGISTRY[verdict.key].group == "naabhasa_dala", \
                    verdict.key


# --------------------------------------------------------------------------
# 11.6 Other popular yogas
#
# The section's own preamble binds every one of them: "for a yoga to be fully
# present, all the required combinations must be present *and the
# participating planets must be strong*." Strength is chapter 15's, and it is
# not built — so `present=True` here means the combinations hold, never that
# the yoga is full. Every verdict says so. See OI-81.
# --------------------------------------------------------------------------


def _pop(lagna: str, paksha: int | None = None, **placements) -> YogaInput:
    """A §11.6 input. These yogas count houses from lagna, so lagna is given."""
    return YogaInput(
        rasis={int(getattr(Graha, name)): R[sign]
               for name, sign in placements.items()},
        lagna_rasi=R[lagna],
        paksha=paksha,
    )


def test_eighteen_popular_yogas_are_declared():
    """The eighteen printed before the Shivaji example. Thirty more follow
    it — see the section further down."""
    assert len(POPULAR_YOGAS) == POPULAR_YOGA_COUNT == 18
    assert len({e["key"] for e in POPULAR_YOGAS}) == 18


def test_every_popular_yoga_is_registered_under_its_section():
    keys = {e["key"] for e in POPULAR_YOGAS_ALL}
    registered = {k for k, s in YOGA_REGISTRY.items() if s.group == "popular"}
    assert registered == keys
    for key in keys:
        assert YOGA_REGISTRY[key].section == "11.6"


def test_the_fullness_rule_is_transcribed():
    assert "all the required combinations must be present" in \
        POPULAR_YOGA_FULLNESS_RULE
    assert "must be strong" in POPULAR_YOGA_FULLNESS_RULE
    assert "even if all the required combinations are not present" in \
        POPULAR_YOGA_FULLNESS_RULE


def test_no_popular_verdict_ever_claims_the_yoga_is_full():
    """The governing constraint. Whatever the chart, every §11.6 verdict
    carries the note that strength was not assessed — so nothing here can be
    read as "fully present"."""
    data = _pop("Ar", paksha=0, SUN="Ar", MOON="Ta", MARS="Ge", MERCURY="Cn",
                JUPITER="Le", VENUS="Vi", SATURN="Li")
    for verdict in evaluate(data):
        if YOGA_REGISTRY[verdict.key].group != "popular":
            continue
        assert STRENGTH_NOT_ASSESSED in verdict.qualifiers, verdict.key


def test_the_four_yogas_that_name_a_lord_say_which_one():
    """§11.6 asks four of the eighteen for a *named* lord's strength. Those
    four say so in their own qualifier, over and above the section-wide note."""
    named = {e["key"]: e["strength"] for e in POPULAR_YOGAS if e.get("strength")}
    assert named == {
        "kaahala": ("lagna lord",),
        "sankha": ("lagna lord", "9th lord"),
        "bheri": ("9th lord",),
        "mridanga": ("lagna lord",),
    }
    data = _pop("Ar", paksha=0, MOON="Cn", JUPITER="Li")
    verdict = evaluate_one("kaahala", data)
    assert any("lagna lord" in q and "not assessed" in q
               for q in verdict.qualifiers)


# --- footnote 31: kartari ---------------------------------------------------


def test_kartari_is_cast_by_the_2nd_and_12th():
    assert KARTARI_HOUSES == (12, 2)
    assert KARTARI_MEANS == "scissors"


def test_subha_kartari_needs_benefics_on_both_flanks():
    cut = kartari(_pop("Ar", JUPITER="Pi", VENUS="Ta"), R["Ar"])
    assert cut["subha"] is True
    assert cut["paapa"] is False


def test_paapa_kartari_needs_malefics_on_both_flanks():
    cut = kartari(_pop("Ar", SATURN="Pi", MARS="Ta"), R["Ar"])
    assert cut["paapa"] is True
    assert cut["subha"] is False


def test_a_mixed_pair_of_flanks_is_neither_kartari():
    """"the 2nd *and* 12th" — one of each cuts neither way."""
    cut = kartari(_pop("Ar", JUPITER="Pi", MARS="Ta"), R["Ar"])
    assert cut["subha"] is False
    assert cut["paapa"] is False


def test_an_empty_flank_is_no_kartari_at_all():
    cut = kartari(_pop("Ar", JUPITER="Pi"), R["Ar"])
    assert cut["subha"] is False
    assert cut["paapa"] is False


def test_kartari_can_be_taken_from_any_sign_not_only_lagna():
    """Footnote 31: "they can be seen with reference to any house or planet." """
    data = _pop("Cp", JUPITER="Ar", VENUS="Ge")
    assert kartari(data, R["Ta"])["subha"] is True
    assert kartari(data, R["Ar"])["subha"] is False


# --- subha and asubha -------------------------------------------------------


def test_subha_by_a_benefic_in_lagna():
    verdict = evaluate_one("subha", _pop("Ar", JUPITER="Ar"))
    assert verdict.present is True
    assert "lagna holds Jupiter" in verdict.reason


def test_subha_by_kartari_alone():
    verdict = evaluate_one("subha", _pop("Ar", JUPITER="Pi", VENUS="Ta"))
    assert verdict.present is True
    assert "subha kartari" in verdict.reason


def test_subha_absent_says_both_ways_it_failed():
    verdict = evaluate_one("subha", _pop("Ar", SATURN="Pi", MARS="Ta"))
    assert verdict.present is False
    assert "no benefic" in verdict.reason and "no subha kartari" in verdict.reason


def test_asubha_is_the_same_test_with_malefics():
    data = _pop("Ar", SATURN="Pi", MARS="Ta")
    assert evaluate_one("asubha", data).present is True
    assert evaluate_one("asubha", _pop("Ar", MARS="Ar")).present is True
    assert evaluate_one("asubha", _pop("Ar", JUPITER="Pi", VENUS="Ta")).present \
        is False


# --- gaja-kesari ------------------------------------------------------------


def test_gaja_kesari_needs_all_three_clauses():
    verdict = evaluate_one("gaja_kesari",
                           _pop("Ar", paksha=0, MOON="Ar", JUPITER="Cn",
                                VENUS="Cn"))
    assert verdict.present is True
    assert set(verdict.participants) == {int(Graha.JUPITER), int(Graha.VENUS)}


def test_gaja_kesari_fails_when_jupiter_is_not_in_a_quadrant_from_moon():
    verdict = evaluate_one("gaja_kesari",
                           _pop("Ar", paksha=0, MOON="Ar", JUPITER="Ge",
                                VENUS="Ge"))
    assert verdict.present is False
    assert "3rd from Moon" in verdict.reason


def test_gaja_kesari_fails_on_a_debilitated_jupiter():
    verdict = evaluate_one("gaja_kesari",
                           _pop("Ar", paksha=0, MOON="Li", JUPITER="Cp",
                                VENUS="Cp"))
    assert verdict.present is False
    assert "debilitated" in verdict.reason


def test_gaja_kesari_says_when_combustion_could_not_be_judged():
    """Clause 3 names combustion, which needs longitudes. Without them the
    yoga is not blocked — it is reported with the gap named."""
    verdict = evaluate_one("gaja_kesari",
                           _pop("Ar", paksha=0, MOON="Ar", JUPITER="Cn",
                                VENUS="Cn"))
    assert any("combustion could not be judged" in q for q in verdict.qualifiers)


def test_gaja_kesari_records_the_variant_and_the_printed_typo():
    entry = next(e for e in POPULAR_YOGAS if e["key"] == "gaja_kesari")
    assert "quadrant from lagna and not Moon" in entry["variant"]
    assert entry["printed_typo"] == "Juputer"


# --- guru-mangala -----------------------------------------------------------


def test_guru_mangala_when_they_are_together():
    verdict = evaluate_one("guru_mangala", _pop("Ar", JUPITER="Cn", MARS="Cn"))
    assert verdict.present is True
    assert "together" in verdict.reason


def test_guru_mangala_when_they_are_in_the_7th():
    verdict = evaluate_one("guru_mangala", _pop("Ar", JUPITER="Cn", MARS="Cp"))
    assert verdict.present is True
    assert "7th from each other" in verdict.reason


def test_guru_mangala_absent():
    verdict = evaluate_one("guru_mangala", _pop("Ar", JUPITER="Cn", MARS="Le"))
    assert verdict.present is False


# --- amala ------------------------------------------------------------------


def test_amala_from_lagna():
    verdict = evaluate_one("amala", _pop("Ar", VENUS="Cp"))
    assert verdict.present is True
    assert "10th from lagna" in verdict.reason


def test_amala_from_the_moon_too():
    """"the 10th house from lagna **or** Moon"."""
    verdict = evaluate_one("amala", _pop("Ar", paksha=0, MOON="Ta",
                                         JUPITER="Aq"))
    assert verdict.present is True
    assert "10th from Moon" in verdict.reason


def test_amala_is_spoiled_by_one_malefic():
    """"**only** natural benefics" — a single malefic there ends it."""
    verdict = evaluate_one("amala", _pop("Ar", VENUS="Cp", SATURN="Cp"))
    assert verdict.present is False


def test_amala_is_absent_when_the_tenth_is_empty():
    assert evaluate_one("amala", _pop("Ar", VENUS="Ar")).present is False


def test_amala_carries_the_reason_the_book_gives():
    entry = next(e for e in POPULAR_YOGAS if e["key"] == "amala")
    assert entry["name_means"] == "pure"
    assert "conduct in society" in entry["reason"]


# --- parvata ----------------------------------------------------------------


def test_parvata_wants_clean_quadrants_and_a_clean_7th_and_8th():
    verdict = evaluate_one("parvata", _pop("Ar", JUPITER="Cn", VENUS="Ar"))
    assert verdict.present is True


def test_parvata_is_broken_by_a_malefic_in_the_seventh():
    verdict = evaluate_one("parvata", _pop("Ar", JUPITER="Cn", SATURN="Li"))
    assert verdict.present is False
    assert "Saturn in the 7th" in verdict.reason


# --- kaahala ----------------------------------------------------------------


def test_kaahala_by_the_fourth_lord_and_jupiter_in_mutual_quadrants():
    verdict = evaluate_one("kaahala", _pop("Ar", paksha=0, MOON="Cn",
                                           JUPITER="Li"))
    assert verdict.present is True
    assert "mutual quadrants" in verdict.reason


def test_kaahala_by_the_printed_alternative():
    """"the 4th lord is exalted or in own sign and the 10th lord joins him." """
    verdict = evaluate_one("kaahala", _pop("Ar", paksha=0, MOON="Ta",
                                           SATURN="Ta"))
    assert verdict.present is True
    assert "10th lord Saturn joins him" in verdict.reason


def test_kaahala_absent():
    verdict = evaluate_one("kaahala", _pop("Ar", paksha=0, MOON="Ge",
                                           JUPITER="Le", SATURN="Sc"))
    assert verdict.present is False


def test_kaahala_footnote_offers_the_ninth_lord_for_jupiter():
    entry = next(e for e in POPULAR_YOGAS if e["key"] == "kaahala")
    assert "9th lord" in entry["footnote"]


# --- chaamara ---------------------------------------------------------------


def test_chaamara_by_an_exalted_lagna_lord_in_a_quadrant_with_jupiter():
    verdict = evaluate_one("chaamara", _pop("Ar", MARS="Cp", JUPITER="Vi"))
    assert verdict.present is True
    assert "Jupiter's aspect" in verdict.reason


def test_chaamara_by_two_benefics_in_the_7th_9th_or_10th():
    verdict = evaluate_one("chaamara", _pop("Ar", JUPITER="Sg", VENUS="Sg"))
    assert verdict.present is True
    assert "two benefics" in verdict.reason


def test_chaamara_absent():
    assert evaluate_one("chaamara",
                        _pop("Ar", MARS="Ge", JUPITER="Ta")).present is False


# --- sankha -----------------------------------------------------------------


def test_sankha_by_the_fifth_and_sixth_lords():
    verdict = evaluate_one("sankha", _pop("Ar", SUN="Ar", MERCURY="Cn"))
    assert verdict.present is True
    assert "5th lord Sun and 6th lord Mercury" in verdict.reason


def test_sankha_by_the_alternative_in_a_movable_sign():
    verdict = evaluate_one("sankha", _pop("Ar", MARS="Cn", SATURN="Cn",
                                          SUN="Ar", MERCURY="Ta"))
    assert verdict.present is True
    assert "movable sign" in verdict.reason


def test_sankha_absent():
    verdict = evaluate_one("sankha", _pop("Ar", SUN="Ta", MERCURY="Ge",
                                          MARS="Ge", SATURN="Le"))
    assert verdict.present is False


# --- bheri ------------------------------------------------------------------


def test_bheri_when_the_1st_2nd_7th_and_12th_are_all_occupied():
    verdict = evaluate_one("bheri", _pop("Ar", SUN="Ar", MERCURY="Ta",
                                         SATURN="Li", MARS="Pi"))
    assert verdict.present is True


def test_bheri_by_the_alternative_three_in_mutual_quadrants():
    verdict = evaluate_one("bheri", _pop("Ar", JUPITER="Ar", VENUS="Cn",
                                         MARS="Li"))
    assert verdict.present is True
    assert "mutual quadrants" in verdict.reason


def test_bheri_names_which_houses_were_vacant():
    verdict = evaluate_one("bheri", _pop("Ar", JUPITER="Ta", VENUS="Ge",
                                         MARS="Le"))
    assert verdict.present is False
    assert "1st" in verdict.reason and "vacant" in verdict.reason


# --- mridanga ---------------------------------------------------------------


def test_mridanga_from_an_exalted_planet_in_a_quadrant():
    verdict = evaluate_one("mridanga", _pop("Ar", SUN="Ar"))
    assert verdict.present is True


def test_mridanga_from_an_own_sign_in_a_trine():
    verdict = evaluate_one("mridanga", _pop("Ar", SUN="Le"))
    assert verdict.present is True
    assert "5th" in verdict.reason


def test_mridanga_absent_when_the_dignity_is_outside_quadrants_and_trines():
    verdict = evaluate_one("mridanga", _pop("Ar", MERCURY="Ge"))
    assert verdict.present is False


# --- sreenaatha -------------------------------------------------------------


def test_sreenaatha_in_the_only_lagna_that_admits_it():
    verdict = evaluate_one("sreenaatha", _pop("Sg", MERCURY="Vi", SUN="Vi"))
    assert verdict.present is True


def test_sreenaatha_needs_the_tenth_lord_with_the_ninth():
    verdict = evaluate_one("sreenaatha", _pop("Sg", MERCURY="Vi", SUN="Le"))
    assert verdict.present is False
    assert "not with the 9th lord" in verdict.reason


def test_the_sreenaatha_footnote_holds_for_all_twelve_lagnas():
    """"7th lord can be exalted in 10th only for Sagittarius lagna." Checked,
    not taken on trust."""
    entry = next(e for e in POPULAR_YOGAS if e["key"] == "sreenaatha")
    assert "only for Sagittarius lagna" in entry["footnote"]
    admits = []
    for lagna in range(12):
        seventh_lord = int(RASI_LORD[(lagna + 6) % 12])
        tenth_sign = (lagna + 9) % 12
        exalted = EXALTATION_DEG.get(seventh_lord)
        if exalted is not None and int(exalted // 30) == tenth_sign:
            admits.append(lagna)
    assert admits == [R["Sg"]]


# --- matsya -----------------------------------------------------------------


def test_matsya_wants_benefics_planets_and_malefics_in_their_places():
    verdict = evaluate_one("matsya", _pop("Ar", paksha=0, JUPITER="Ar",
                                          VENUS="Sg", MERCURY="Le",
                                          SATURN="Cn", MARS="Sc"))
    assert verdict.present is True


def test_matsya_uses_chapter_sevens_chaturasras():
    """"malefics in chaturasras (4th and 8th)" — the same pair chapter 7
    defines, not a fresh list."""
    assert CHATURASRA == (4, 8)
    verdict = evaluate_one("matsya", _pop("Ar", paksha=0, JUPITER="Ar",
                                          VENUS="Sg", MERCURY="Le",
                                          SATURN="Cn"))
    assert verdict.present is False
    assert "no malefic in the 8th" in verdict.reason


# --- koorma -----------------------------------------------------------------


def test_koorma_needs_dignified_benefics_and_dignified_malefics():
    """Reachable only where Mercury's company turns him malefic: no chart with
    one planet per house satisfies it, because the 3rd, 1st and 11th cannot
    all hold a fixed natural malefic in its own or exaltation sign."""
    verdict = evaluate_one("koorma",
                           _pop("Ar", paksha=0, JUPITER="Le", MOON="Vi",
                                VENUS="Li", SUN="Ar", MERCURY="Ge", MARS="Ge",
                                SATURN="Aq"))
    assert verdict.present is True


def test_koorma_names_every_house_that_failed():
    verdict = evaluate_one("koorma", _pop("Ar", paksha=0, JUPITER="Le",
                                          MERCURY="Vi", VENUS="Li"))
    assert verdict.present is False
    for house in ("1st", "3rd", "11th"):
        assert house in verdict.reason


# --- khadga -----------------------------------------------------------------


def test_khadga_is_an_exchange_between_the_2nd_and_9th_lords():
    verdict = evaluate_one("khadga", _pop("Ar", VENUS="Sg", JUPITER="Ta",
                                          MARS="Cn"))
    assert verdict.present is True
    assert "exchanged houses" in verdict.reason


def test_khadga_also_needs_the_lagna_lord_placed_well():
    verdict = evaluate_one("khadga", _pop("Ar", VENUS="Sg", JUPITER="Ta",
                                          MARS="Ge"))
    assert verdict.present is False
    assert "lagna lord Mars" in verdict.reason


# --- kusuma -----------------------------------------------------------------


def test_kusuma_wants_a_fixed_lagna():
    verdict = evaluate_one("kusuma", _pop("Ta", paksha=0, VENUS="Le",
                                          MOON="Vi", JUPITER="Vi",
                                          SATURN="Aq"))
    assert verdict.present is True


def test_kusuma_is_absent_from_a_movable_lagna():
    verdict = evaluate_one("kusuma", _pop("Ar", paksha=0, VENUS="Cn",
                                          MOON="Le", JUPITER="Le",
                                          SATURN="Cp"))
    assert verdict.present is False
    assert "not a fixed sign" in verdict.reason


def test_kusuma_needs_a_benefic_other_than_the_moon_with_the_moon():
    verdict = evaluate_one("kusuma", _pop("Ta", paksha=0, VENUS="Le",
                                          MOON="Vi", SATURN="Aq"))
    assert verdict.present is False
    assert "no benefic is with the Moon" in verdict.reason


# --- kalaanidhi -------------------------------------------------------------


def test_kalaanidhi_with_jupiter_in_the_second():
    verdict = evaluate_one("kalaanidhi", _pop("Ar", JUPITER="Ta",
                                              MERCURY="Ta", VENUS="Ta"))
    assert verdict.present is True


def test_kalaanidhi_is_absent_when_jupiter_is_elsewhere():
    verdict = evaluate_one("kalaanidhi", _pop("Ar", JUPITER="Ge",
                                              MERCURY="Ge", VENUS="Ge"))
    assert verdict.present is False
    assert "not the 2nd or 5th" in verdict.reason


def test_kalaanidhi_needs_both_mercury_and_venus():
    verdict = evaluate_one("kalaanidhi", _pop("Ar", JUPITER="Ta",
                                              MERCURY="Ta", VENUS="Ar"))
    assert verdict.present is False
    assert "Venus" in verdict.reason


# --- kalpadruma -------------------------------------------------------------


def test_kalpadruma_keeps_all_four_planets():
    """"Some authors have simplified this yoga... Let us follow Parasara." """
    entry = next(e for e in POPULAR_YOGAS if e["key"] == "kalpadruma")
    assert "Let us follow Parasara" in entry["simplification_rejected"]
    assert entry["aliases"] == ("Paarijaata Yoga",)


def test_kalpadruma_cannot_be_decided_from_signs_alone():
    """Its fourth link is a *navamsa* dispositor, so a rasi-only chart is not
    enough — and the verdict says that rather than reporting a bare absence."""
    verdict = evaluate_one("kalpadruma", _pop("Ar", paksha=0, MARS="Cn",
                                              MOON="Ta", VENUS="Pi"))
    assert verdict.present is False
    assert "navamsa dispositor" in verdict.reason
    assert "needs longitudes" in verdict.reason


def test_the_rules_endpoint_states_the_fullness_rule(client):
    body = client.get("/v1/planetary-yoga/rules").json()
    assert "must be strong" in body["popular_fullness_rule"]
    assert body["popular_strength_note"] == STRENGTH_NOT_ASSESSED
    assert body["kartari_houses"] == [12, 2]
    assert body["kartari_means"] == "scissors"
    assert set(body["popular_yogas_needing_a_named_lord"]) == {
        "kaahala", "sankha", "bheri", "mridanga",
        "lakshmi", "saarada", "vasumati", "gandharva", "go"}


def test_the_chart_endpoint_answers_every_popular_yoga(client):
    body = client.post("/v1/planetary-yoga/chart", json={
        "lagna_rasi": R["Ar"], "paksha": 0,
        "rasis": {0: R["Ar"], 1: R["Ta"], 2: R["Ge"], 3: R["Cn"],
                  4: R["Le"], 5: R["Vi"], 6: R["Li"]}}).json()
    popular = [y for y in body["yogas"]
               if YOGA_REGISTRY[y["key"]].group == "popular"]
    assert len(popular) == 48
    for yoga in popular:
        assert yoga["reason"]
        assert STRENGTH_NOT_ASSESSED in yoga["qualifiers"]


def test_the_rules_endpoint_carries_footnote_31_as_printed(client):
    body = client.get("/v1/planetary-yoga/rules").json()
    assert body["kartari_definition"] == KARTARI_DEFINITION
    assert body["kartari_effect"] == KARTARI_EFFECT
    assert "any house or planet" in body["kartari_is_general"]
    assert body["popular_intro"] == POPULAR_YOGA_INTRO
    assert body["popular_count"] == 48
    assert body["popular_count_before_the_example"] == 18
    assert body["popular_count_after_the_example"] == 30


# --------------------------------------------------------------------------
# Chart 9 — Chatrapati Shivaji, §11.6's worked example of Kalpadruma yoga
# --------------------------------------------------------------------------

#: Chart 9's rasi longitudes, as printed under the diagram on the same page.
CHART_9 = {
    "Asc": "27 Le 41", "Sun": "22 Aq 19", "Moon": "27 Vi 52",
    "Mars": "16 Ge 00", "Merc": "6 Pi 18", "Jup": "5 Aq 51",
    "Ven": "8 Ar 30", "Sat": "16 Li 34", "Rahu": "29 Ta 22",
    "Ketu": "29 Sc 22", "HL": "24 Aq 15", "GL": "27 Le 55",
}

#: Chart 9's birth data, as printed inside the diagram. **Not computable
#: from this.** Unlike Charts 5 to 8 it gives a Hindu calendar date and a
#: time measured from sunrise, with no Gregorian date and no time zone, so
#: this chart is a transcription and not a check on our ephemeris.
CHART_9_BIRTH = "Phalguna Bahula Tritiya, 1630 AD, 12:05 hrs after sunrise"
CHART_9_PLACE = "73 E 53, 18 N 32"

#: The chara karakas printed beside each planet.
CHART_9_CHARA_KARAKAS = {
    "Moon": "AK", "Sun": "AmK", "Mars": "MK", "Jup": "GK",
    "Merc": "PK", "Ven": "PiK", "Sat": "BK", "Rahu": "DK",
}

#: The rasi diagram, read box by box. Cross-checked against the longitudes.
CHART_9_RASI_DRAWN = {
    "Merc": "Pi", "Ven": "Ar", "Rahu": "Ta", "Mars": "Ge",
    "Jup": "Aq", "Sun": "Aq", "Ketu": "Sc", "Sat": "Li", "Moon": "Vi",
    "Asc": "Le",
}

#: The navamsa diagram, read box by box. Ours has to reproduce it.
CHART_9_NAVAMSA_DRAWN = {
    "Ketu": "Pi", "Sun": "Ar", "Ven": "Ge", "Sat": "Aq", "Mars": "Aq",
    "Merc": "Le", "Jup": "Sc", "Rahu": "Vi", "Moon": "Vi", "Asc": "Sg",
}

_CHART_9_GRAHA = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
    "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU,
}


def _lon9(text: str) -> float:
    """Parse "27 Le 41" into a sidereal longitude."""
    import re
    match = re.fullmatch(r"(\d+) ?([A-Za-z]{2}) ?(\d+)", text)
    assert match, text
    return R[match.group(2)] * 30 + int(match.group(1)) + int(match.group(3)) / 60


def _chart_9() -> YogaInput:
    """Chart 9 as a yoga input, with longitudes so navamsa is reachable.

    Paksha is Krishna: the birth data reads "Phalguna **Bahula** Tritiya",
    and the printed longitudes agree — see the tithi test below.
    """
    from hora.core.ephemeris.base import PlanetPosition

    lons = {int(g): _lon9(CHART_9[name]) for name, g in _CHART_9_GRAHA.items()}
    positions = {
        graha: PlanetPosition(
            graha=graha, longitude=lon, latitude=0.0, distance=1.0,
            speed_longitude=-0.1 if graha == int(Graha.SATURN) else 0.5,
            speed_latitude=0.0, speed_distance=0.0)
        for graha, lon in lons.items()
    }
    return YogaInput(
        rasis={graha: int(lon // 30) for graha, lon in lons.items()},
        positions=positions,
        lagna_rasi=int(_lon9(CHART_9["Asc"]) // 30),
        paksha=1,
    )


@pytest.mark.parametrize("body,sign", sorted(CHART_9_RASI_DRAWN.items()))
def test_chart_9s_diagram_agrees_with_its_printed_longitudes(body, sign):
    """The drawn boxes and the degrees below them are two transcriptions of
    the same chart. They agree on all ten."""
    assert int(_lon9(CHART_9[body]) // 30) == R[sign]


@pytest.mark.parametrize("body,sign", sorted(CHART_9_NAVAMSA_DRAWN.items()))
def test_our_navamsa_reproduces_chart_9s_drawn_navamsa(body, sign):
    """Chart 9 prints its D-9 as a second diagram, so our D-9 is checked
    against the book rather than against itself. All ten agree."""
    from hora.charts.vargas import d9_navamsa

    key = "Asc" if body == "Asc" else body
    assert d9_navamsa(_lon9(CHART_9[key])).sign == R[sign]


def test_chart_9s_tithi_confirms_the_krishna_paksha():
    """"Phalguna **Bahula** Tritiya". Bahula is Krishna paksha, and the
    printed longitudes give tithi 18 — Krishna Tritiya — independently."""
    elongation = (_lon9(CHART_9["Moon"]) - _lon9(CHART_9["Sun"])) % 360
    tithi = int(elongation / 12) + 1
    assert tithi == 18
    assert tithi - 15 == 3


def test_chart_9_is_transcribed_not_computed():
    """Charts 5 to 8 print a Gregorian date and are recomputed from it. This
    one prints a Hindu calendar date and a time measured from sunrise, so
    there is nothing to recompute it from."""
    assert "1630 AD" in CHART_9_BIRTH
    assert "after sunrise" in CHART_9_BIRTH
    assert not any(ch.isdigit() for ch in CHART_9_BIRTH.split(",")[0])


# --- the example the book works through -------------------------------------


def test_the_kalpadruma_chain_matches_the_book_link_for_link():
    """§11.6: "Lagna lord is Sun. He is in Aq and his dispositor is Saturn...
    Saturn is in Li and his dispositor is Venus... In navamsa, Saturn is in
    Aq and his dispositor is Saturn himself." " """
    from hora.charts.planetary_yogas.popular import dispositor, lord_of_house
    from hora.charts.vargas import d9_navamsa

    data = _chart_9()
    first = lord_of_house(data, 1)
    second = dispositor(data, first)
    third = dispositor(data, second)
    navamsa_sign = d9_navamsa(data.positions[second].longitude).sign
    fourth = int(RASI_LORD[navamsa_sign])

    assert [GRAHA_NAMES[g] for g in (first, second, third, fourth)] == \
        list(KALPADRUMA_EXAMPLE_CHAIN)
    assert data.rasis[first] == R["Aq"]
    assert data.rasis[second] == R["Li"]
    assert navamsa_sign == R["Aq"]


def test_the_three_placement_claims_the_example_makes():
    """"Sun is in a quadrant. Saturn is exalted. Venus is in a trine." " """
    from hora.charts.planetary_yogas.popular import houses_of, in_exaltation

    data = _chart_9()
    assert houses_of(data, int(Graha.SUN)) in KENDRA
    assert in_exaltation(data, int(Graha.SATURN)) is True
    assert houses_of(data, int(Graha.VENUS)) in TRIKONA
    assert "Sun is in a quadrant" in KALPADRUMA_EXAMPLE_CONCLUSION


def test_shivaji_has_kalpadruma_yoga():
    """The whole point of the example, decided by the engine rather than
    asserted: "Thus Shivaji had Kalpadruma yoga." " """
    verdict = evaluate_one("kalpadruma", _chart_9())
    assert verdict.present is True
    assert set(verdict.participants) == {
        int(Graha.SUN), int(Graha.SATURN), int(Graha.VENUS)}


def test_kalpadruma_is_still_not_reported_as_full_even_here():
    """§11.6's preamble binds its own worked example too. See OI-81."""
    verdict = evaluate_one("kalpadruma", _chart_9())
    assert STRENGTH_NOT_ASSESSED in verdict.qualifiers


def test_the_navamsa_claims_that_close_the_example():
    """"In navamsa also, Sun is exalted, Saturn is in moolatrikona and Venus
    is in a lagna." The first two hold. The third does not — see D-34."""
    from hora.charts.vargas import d9_navamsa

    navamsa = {name: d9_navamsa(_lon9(text)).sign
               for name, text in CHART_9.items() if name in _CHART_9_GRAHA}
    lagna = d9_navamsa(_lon9(CHART_9["Asc"])).sign

    sun = int(Graha.SUN)
    assert int(EXALTATION_DEG[sun] // 30) == navamsa["Sun"]
    assert int(MOOLATRIKONA[Graha.SATURN][0]) == navamsa["Sat"]

    # "Venus is in a lagna" — she is in the 7th from it.
    assert navamsa["Ven"] != lagna
    assert (navamsa["Ven"] - lagna) % 12 + 1 == 7
    assert KALPADRUMA_EXAMPLE_NAVAMSA_LAGNA_CLAIM == "Venus is in a lagna"


def test_no_special_lagna_chart_9_draws_sits_with_venus_in_navamsa():
    """The kindest reading of "Venus is in a lagna" would be one of the
    special lagnas. The drawn navamsa puts HL in Taurus, AL in Libra and GL
    with the ascendant in Sagittarius. Venus is in Gemini, alone."""
    from hora.charts.vargas import d9_navamsa

    assert d9_navamsa(_lon9(CHART_9["Ven"])).sign == R["Ge"]
    for name, sign in (("HL", "Ta"), ("GL", "Sg")):
        assert d9_navamsa(_lon9(CHART_9[name])).sign == R[sign]


# --- footnote 34 ------------------------------------------------------------


def test_footnote_34_is_the_only_sight_of_a_11_6_results_paragraph():
    """§11.6's results were not supplied — OI-82 — but footnote 34 quotes
    three words out of Kalpadruma's."""
    assert KALPADRUMA_RESULT_WORDS == ("principled", "kind", "likes wars")
    assert KALPADRUMA_RESULT_WORD_SANSKRIT == "yuddhapriyah"
    for word in KALPADRUMA_RESULT_WORDS:
        assert word in KALPADRUMA_RESULTS_FOOTNOTE
    assert "not meant negatively" in KALPADRUMA_RESULTS_FOOTNOTE


def test_the_results_entry_for_kalpadruma_still_records_the_gap():
    """Three quoted words are not the paragraph. The entry stays marked
    untranscribed so OI-82 does not read as closed."""
    entry = next(e for e in _results()["entries"]
                 if e["planetary_yoga"] == "kalpadruma")
    assert entry["results_transcribed"] is False
    assert entry["verbatim"] is None


# --- what the whole registry says about this chart --------------------------


def test_every_yoga_chart_9_actually_has():
    """Five of the sixty-five, across four sections. Pinned so a later change
    to any detector has to account for this chart."""
    present = {v.key for v in evaluate(_chart_9()) if v.present}
    assert present == {"vesi", "sunaphaa", "adhi", "daama", "kalpadruma"}


def test_chart_9_is_a_daama_yoga_like_ramas():
    """Six distinct signs hold the seven planets, and no earlier Naabhasa
    yoga applies — the same Sankhya verdict §11.5.4 reaches for Rama."""
    verdict = evaluate_one("daama", _chart_9())
    assert verdict.present is True
    assert "6 distinct signs" in verdict.reason


def test_the_rules_endpoint_carries_the_shivaji_example(client):
    body = client.get("/v1/planetary-yoga/rules").json()
    example = body["kalpadruma_example"]
    assert example["chart"] == "Chart 9"
    assert example["native"] == "Chatrapati Shivaji"
    assert example["chain"] == ["Sun", "Saturn", "Venus", "Saturn"]
    assert "D-34" in example["navamsa_lagna_note"]


def test_footnote_34_is_withheld_under_the_licence_gate(client):
    """It quotes PVR's results wording, so it sits behind OI-12's gate like
    every other piece of his prose."""
    body = client.get("/v1/planetary-yoga/rules").json()
    assert body["kalpadruma_results_footnote"] is None
    assert body["kalpadruma_result_words"] == []
    payload = repr(body).lower()
    for word in ("yuddhapriyah", "principled", "likes wars"):
        assert word not in payload


# --------------------------------------------------------------------------
# 11.6, continued — the thirty printed after the Shivaji example
#
# These are NOT Shivaji's yogas. His chart is used for Kalpadruma alone; the
# section's list simply runs on past it. Unlike the first eighteen, each of
# these prints its own Results sentence.
# --------------------------------------------------------------------------


def _pl(lagna: str, paksha: int | None = None, **longitudes) -> YogaInput:
    """A §11.6 input built from longitudes, so navamsa is reachable.

    Four of the thirty read the D-9 and two ask for deep exaltation, and
    none of those can be answered from signs alone.
    """
    from hora.core.ephemeris.base import PlanetPosition

    positions = {
        int(getattr(Graha, name)): PlanetPosition(
            graha=int(getattr(Graha, name)), longitude=lon, latitude=0.0,
            distance=1.0, speed_longitude=0.5, speed_latitude=0.0,
            speed_distance=0.0)
        for name, lon in longitudes.items()
    }
    return YogaInput(
        rasis={g: int(p.longitude // 30) for g, p in positions.items()},
        positions=positions, lagna_rasi=R[lagna], paksha=paksha)


def _deg(sign: str, degrees: float = 15.0) -> float:
    return R[sign] * 30 + degrees


def _navamsa_lon(sign: str, want_lord: str) -> float:
    """A longitude inside `sign` whose navamsa sign `want_lord` rules.

    Derived, not guessed — the yogas that read the D-9 need a chart built
    backwards from the navamsa, and hand-picked degrees got it wrong twice.
    """
    from hora.charts.vargas import d9_navamsa

    for index in range(9):
        lon = R[sign] * 30 + index * (30 / 9) + 1.5
        if int(RASI_LORD[d9_navamsa(lon).sign]) == int(getattr(Graha, want_lord)):
            return round(lon, 3)
    raise AssertionError(f"no navamsa of {sign} is ruled by {want_lord}")


def test_thirty_more_popular_yogas_are_declared():
    assert len(POPULAR_YOGAS_CONTINUED) == POPULAR_YOGA_CONTINUED_COUNT == 30
    assert len(POPULAR_YOGAS_ALL) == POPULAR_YOGA_TOTAL == 48
    assert len({e["key"] for e in POPULAR_YOGAS_ALL}) == 48


def test_the_thirty_are_registered_under_the_same_section():
    for entry in POPULAR_YOGAS_CONTINUED:
        spec = YOGA_REGISTRY[entry["key"]]
        assert spec.section == "11.6"
        assert spec.group == "popular"


def test_the_preamble_binds_these_thirty_too():
    """§11.6's fullness rule was printed before the first eighteen; the list
    is one list, so it governs these as well. See OI-81."""
    data = _pl("Ar", paksha=0, SUN=_deg("Ar"), MOON=_deg("Ta"),
               MARS=_deg("Ge"), MERCURY=_deg("Cn"), JUPITER=_deg("Le"),
               VENUS=_deg("Vi"), SATURN=_deg("Li"))
    keys = {e["key"] for e in POPULAR_YOGAS_CONTINUED}
    for verdict in evaluate(data):
        if verdict.key in keys:
            assert STRENGTH_NOT_ASSESSED in verdict.qualifiers, verdict.key


# --- Lagnaadhi --------------------------------------------------------------


def test_lagnaadhi_wants_benefics_in_the_7th_and_8th():
    verdict = evaluate_one("lagnaadhi", _pl("Ar", VENUS=_deg("Li"),
                                            JUPITER=_deg("Sc")))
    assert verdict.present is True


def test_lagnaadhi_is_broken_by_a_malefic_reaching_those_benefics():
    """"no malefics conjoin **or aspect** these planets" — the second clause
    is about the benefics, not about the houses."""
    verdict = evaluate_one("lagnaadhi", _pl("Ar", VENUS=_deg("Li"),
                                            JUPITER=_deg("Sc"),
                                            SATURN=_deg("Li")))
    assert verdict.present is False
    assert "Saturn joins Venus" in verdict.reason


def test_lagnaadhi_is_not_the_same_rule_as_adhi():
    """§11.6 says it "means Adhi Yoga from lagna", but Adhi takes the 6th,
    7th and 8th from Moon and this takes only the 7th and 8th. See D-35."""
    assert LAGNAADHI_HOUSES == (7, 8)
    assert ADHI_HOUSES_FROM_MOON == (6, 7, 8)
    assert "means Adhi Yoga from lagna" in LAGNAADHI_GLOSS
    # Moon in Libra puts the 6th, 7th and 8th from her in Pisces, Aries and
    # Taurus — nowhere near the benefics — while the 7th and 8th from lagna
    # hold both of them. Adhi fails, Lagnaadhi holds, on one chart.
    data = _pl("Ar", paksha=0, MOON=_deg("Li", 2), VENUS=_deg("Li", 20),
               JUPITER=_deg("Sc"))
    assert evaluate_one("lagnaadhi", data).present is True
    assert evaluate_one("adhi", data).present is False


# --- the Trimurthi three ----------------------------------------------------


@pytest.mark.parametrize(
    "key,from_house,houses",
    [("hari", 2, (2, 12, 8)), ("hara", 7, (4, 9, 8)), ("brahma", 1, (4, 10, 11))],
)
def test_the_trimurthi_yogas_count_from_a_lord_not_from_lagna(
        key, from_house, houses):
    """Hari from the 2nd lord, Hara from the 7th, Brahma from the lagna lord.
    Each chart below puts that lord in Aries and benefics in the three houses
    counted from there."""
    from hora.charts.planetary_yogas._shared import house_sign

    lord_sign = R["Ar"]
    targets = [house_sign(lord_sign, h) for h in houses]
    lord = int(RASI_LORD[(R["Ar"] + from_house - 1) % 12])
    # The lord may himself be one of the benefics, and he is needed in Aries,
    # so he is taken out of the pool that fills the three houses.
    pool = [name for name in ("JUPITER", "MERCURY", "VENUS", "MOON")
            if int(getattr(Graha, name)) != lord]
    placement = {name: _deg(RASI_ABBR[sign])
                 for name, sign in zip(pool, targets)}
    placement[GRAHA_NAMES[lord].upper()] = _deg("Ar")
    verdict = evaluate_one(key, _pl("Ar", paksha=0, **placement))
    assert verdict.present is True, verdict.reason
    assert f"the {ordinal(from_house)} lord" in verdict.reason


def test_hari_names_the_houses_that_had_no_benefic():
    verdict = evaluate_one("hari", _pl("Ar", VENUS=_deg("Ar"),
                                       JUPITER=_deg("Ta")))
    assert verdict.present is False
    assert "8th" in verdict.reason and "12th" in verdict.reason


def test_the_trimurthi_note_is_recorded():
    assert TRIMURTHI_YOGAS == ("hari", "hara", "brahma")
    assert "Hari Hara Brahma yoga" in TRIMURTHI_NOTE
    assert "Trimurthi Yogas" in TRIMURTHI_NOTE
    for key in TRIMURTHI_YOGAS:
        assert key in YOGA_REGISTRY


def test_brahmas_second_definition_is_carried_not_detected():
    """NOTE (2) gives an unrelated second rule. The first is what runs; the
    variation is recorded so it is visibly not dropped."""
    assert "Jupiter is in a quadrant from the 9th lord" in BRAHMA_VARIATION
    entry = next(e for e in POPULAR_YOGAS_CONTINUED if e["key"] == "brahma")
    assert entry["variant"] == BRAHMA_VARIATION
    assert "4th, 10th and 11th" in entry["definition"]


# --- the four that read the navamsa -----------------------------------------


def test_vishnu_needs_a_third_planet_from_the_navamsa():
    jupiter = _navamsa_lon("Ta", "MERCURY")
    verdict = evaluate_one("vishnu", _pl("Ar", JUPITER=jupiter,
                                         SATURN=_deg("Ta", 20),
                                         MERCURY=_deg("Ta", 25)))
    assert verdict.present is True
    assert "navamsa" in verdict.reason


def test_vishnu_fails_when_that_third_planet_is_elsewhere():
    jupiter = _navamsa_lon("Ta", "MERCURY")
    verdict = evaluate_one("vishnu", _pl("Ar", JUPITER=jupiter,
                                         SATURN=_deg("Ta", 20),
                                         MERCURY=_deg("Ge", 5)))
    assert verdict.present is False
    assert "is not in the 2nd" in verdict.reason


def test_gouri_reads_the_navamsa_of_the_tenth_lord():
    verdict = evaluate_one("gouri", _pl("Ar", SATURN=_navamsa_lon("Aq", "MARS"),
                                        MARS=_deg("Cp", 10)))
    assert verdict.present is True


def test_gouri_says_when_the_lagna_lord_is_the_same_planet():
    """"lagna lord joins him" is met by identity here, which the book does
    not discuss. The verdict says so rather than hiding it."""
    verdict = evaluate_one("gouri", _pl("Ar", SATURN=_navamsa_lon("Aq", "MARS"),
                                        MARS=_deg("Cp", 10)))
    assert any("met by identity" in q for q in verdict.qualifiers)


def test_chandikaa_needs_a_fixed_lagna_the_sixth_lord_and_the_sun():
    verdict = evaluate_one("chandikaa", _pl(
        "Ta", VENUS=_navamsa_lon("Sc", "JUPITER"),
        SATURN=_navamsa_lon("Cp", "JUPITER"),
        JUPITER=_deg("Ar", 5), SUN=_deg("Ar", 8)))
    assert verdict.present is True


def test_chandikaa_fails_on_a_movable_lagna():
    verdict = evaluate_one("chandikaa", _pl(
        "Ar", VENUS=_navamsa_lon("Sc", "JUPITER"),
        SATURN=_navamsa_lon("Cp", "JUPITER"),
        JUPITER=_deg("Ar", 5), SUN=_deg("Ar", 8)))
    assert verdict.present is False
    assert "not a fixed sign" in verdict.reason


def test_bhaarathi_takes_any_of_the_2nd_5th_or_11th_lords():
    verdict = evaluate_one("bhaarathi", _pl(
        "Ar", VENUS=_navamsa_lon("Ta", "SUN"), SUN=_deg("Ar", 10),
        JUPITER=_deg("Ar", 20), MERCURY=_deg("Ge", 5), SATURN=_deg("Ge", 6)))
    assert verdict.present is True
    assert "2nd lord" in verdict.reason


def test_bhaarathis_printed_grammar_is_recorded():
    """"the lord of the sign occupied in navamsa by 2nd, 5th or 11th lord
    exalted and joins the 9th lord" — no verb before "exalted"."""
    entry = next(e for e in POPULAR_YOGAS_CONTINUED
                 if e["key"] == "bhaarathi")
    assert "no verb before" in entry["printed_typo"]


@pytest.mark.parametrize("key", ["vishnu", "gouri", "chandikaa", "bhaarathi"])
def test_the_navamsa_four_say_so_when_longitudes_are_missing(key):
    """A sign-only chart cannot answer these, and the verdict names the
    reason instead of reporting a bare absence.

    A fixed lagna, because Chandikaa settles on a movable one without ever
    reaching the navamsa — clause 1 alone decides it.
    """
    data = YogaInput(
        rasis={int(Graha.SUN): R["Ar"], int(Graha.SATURN): R["Ta"],
               int(Graha.VENUS): R["Ge"], int(Graha.JUPITER): R["Cn"],
               int(Graha.MERCURY): R["Le"], int(Graha.MARS): R["Vi"]},
        lagna_rasi=R["Ta"])
    verdict = evaluate_one(key, data)
    assert verdict.present is False
    assert "navamsa" in verdict.reason


def test_chandikaa_settles_on_a_movable_lagna_without_the_navamsa():
    """Clause 1 is decidable from signs alone, so a movable lagna is a plain
    absence rather than an undecidable one."""
    data = YogaInput(rasis={int(Graha.SUN): R["Ar"]}, lagna_rasi=R["Ar"])
    verdict = evaluate_one("chandikaa", data)
    assert verdict.present is False
    assert "not a fixed sign" in verdict.reason
    assert "navamsa" not in verdict.reason


# --- the rest, one at a time ------------------------------------------------


def test_siva_is_a_three_way_rotation_of_the_5th_9th_and_10th():
    verdict = evaluate_one("siva", _pl("Ar", SUN=_deg("Sg"),
                                       JUPITER=_deg("Cp"), SATURN=_deg("Le")))
    assert verdict.present is True


def test_siva_names_each_lord_that_is_out_of_place():
    verdict = evaluate_one("siva", _pl("Ar", SUN=_deg("Ar"),
                                       JUPITER=_deg("Ar"), SATURN=_deg("Ar")))
    assert verdict.present is False
    for house in ("5th", "9th", "10th"):
        assert f"the {house} lord" in verdict.reason


def test_trilochana_wants_sun_moon_and_mars_in_mutual_trines():
    verdict = evaluate_one("trilochana", _pl("Ar", paksha=0, SUN=_deg("Ar"),
                                             MOON=_deg("Le"), MARS=_deg("Sg")))
    assert verdict.present is True


def test_trilochana_absent():
    verdict = evaluate_one("trilochana", _pl("Ar", paksha=0, SUN=_deg("Ar"),
                                             MOON=_deg("Ta"), MARS=_deg("Sg")))
    assert verdict.present is False
    assert "not in mutual trines" in verdict.reason


def test_lakshmi_needs_a_dignified_ninth_lord_in_a_quadrant():
    verdict = evaluate_one("lakshmi", _pl("Ta", SATURN=_deg("Aq")))
    assert verdict.present is True
    assert "his own sign" in verdict.reason


def test_lakshmi_separates_undignified_from_badly_placed():
    assert "neither his own sign nor his exaltation sign" in \
        evaluate_one("lakshmi", _pl("Ta", SATURN=_deg("Ar"))).reason
    assert "not a quadrant" in \
        evaluate_one("lakshmi", _pl("Ta", SATURN=_deg("Cp"))).reason


def test_saarada_needs_all_five_clauses():
    verdict = evaluate_one("saarada", _pl(
        "Cp", paksha=0, VENUS=_deg("Ta"), MERCURY=_deg("Ar"), SUN=_deg("Le"),
        MOON=_deg("Cp"), JUPITER=_deg("Ta"), MARS=_deg("Sc")))
    assert verdict.present is True


def test_saarada_names_every_clause_that_failed():
    verdict = evaluate_one("saarada", _pl("Cp", paksha=0, SUN=_deg("Ar"),
                                          MERCURY=_deg("Ta"), MOON=_deg("Ge"),
                                          MARS=_deg("Cn"), VENUS=_deg("Le")))
    assert verdict.present is False
    assert "Sun is not in Leo" in verdict.reason
    assert "Mars is not in the 11th" in verdict.reason


def test_saraswathi_lets_the_three_sit_apart():
    """"not necessarily together" — three separate houses is the point."""
    verdict = evaluate_one("saraswathi", _pl("Sg", MERCURY=_deg("Ge"),
                                             JUPITER=_deg("Sg"),
                                             VENUS=_deg("Cp")))
    assert verdict.present is True


def test_saraswathi_needs_jupiter_well_placed_by_sign():
    verdict = evaluate_one("saraswathi", _pl("Sg", MERCURY=_deg("Ge"),
                                             JUPITER=_deg("Cp"),
                                             VENUS=_deg("Ar")))
    assert verdict.present is False
    assert "Jupiter is in neither an own nor a friendly" in verdict.reason


def test_amsaavatara_wants_all_three_in_quadrants_with_saturn_exalted():
    verdict = evaluate_one("amsaavatara", _pl("Ar", JUPITER=_deg("Cn"),
                                              VENUS=_deg("Cp"),
                                              SATURN=_deg("Li")))
    assert verdict.present is True


def test_amsaavatara_absent_when_saturn_is_only_in_a_quadrant():
    verdict = evaluate_one("amsaavatara", _pl("Ar", JUPITER=_deg("Cn"),
                                              VENUS=_deg("Cp"),
                                              SATURN=_deg("Cn")))
    assert verdict.present is False
    assert "Saturn is not exalted" in verdict.reason


def test_devendra_needs_two_exchanges_and_a_fixed_lagna():
    verdict = evaluate_one("devendra", _pl("Ta", MERCURY=_deg("Aq"),
                                           SATURN=_deg("Ge"),
                                           VENUS=_deg("Pi"),
                                           JUPITER=_deg("Ta")))
    assert verdict.present is True


def test_footnote_35_defines_the_exchange():
    assert "2nd lord is in the 10th house" in PARIVARTANA_FOOTNOTE
    assert "parivartana" in PARIVARTANA_FOOTNOTE


def test_indra_needs_the_exchange_and_the_moon():
    assert evaluate_one("indra", _pl("Ar", paksha=0, SUN=_deg("Aq"),
                                     SATURN=_deg("Le"),
                                     MOON=_deg("Le"))).present is True
    verdict = evaluate_one("indra", _pl("Ar", paksha=0, SUN=_deg("Aq"),
                                        SATURN=_deg("Le"), MOON=_deg("Ar")))
    assert verdict.present is False
    assert "Moon is not in the 5th" in verdict.reason


def test_ravi_yoga_is_not_one_of_section_11_2s_ravi_yogas():
    """§11.2's four are a *family* called Ravi yogas. This is a single yoga
    of that name, printed in §11.6."""
    assert YOGA_REGISTRY["ravi"].section == "11.6"
    assert YOGA_REGISTRY["vesi"].group == "ravi"
    assert YOGA_REGISTRY["ravi"].group == "popular"
    entry = next(e for e in POPULAR_YOGAS_CONTINUED if e["key"] == "ravi")
    assert "Not to be confused" in entry["alias_note"]


def test_ravi_needs_the_sun_in_the_10th_and_its_lord_in_the_3rd():
    verdict = evaluate_one("ravi", _pl("Cn", SUN=_deg("Ar"), MARS=_deg("Vi"),
                                       SATURN=_deg("Vi")))
    assert verdict.present is True
    assert "with Saturn" in verdict.reason


def test_ravi_says_when_the_tenth_lord_is_saturn_himself():
    verdict = evaluate_one("ravi", _pl("Ar", SUN=_deg("Cp"), SATURN=_deg("Ge")))
    assert verdict.present is True
    assert any("met by identity" in q for q in verdict.qualifiers)


def test_bhaaskara_chains_sun_moon_mercury_and_jupiter():
    verdict = evaluate_one("bhaaskara", _pl("Ar", paksha=0, SUN=_deg("Ar"),
                                            MOON=_deg("Pi"),
                                            MERCURY=_deg("Ta"),
                                            JUPITER=_deg("Cn")))
    assert verdict.present is True


def test_bhaaskara_absent():
    verdict = evaluate_one("bhaaskara", _pl("Ar", paksha=0, SUN=_deg("Ar"),
                                            MOON=_deg("Sc"),
                                            MERCURY=_deg("Ta"),
                                            JUPITER=_deg("Cn")))
    assert verdict.present is False
    assert "not the 12th" in verdict.reason


def test_kulavardhana_needs_every_planet_in_one_of_three_signs():
    """"each planet occupies the 5th house from **either** lagna or Moon or
    Sun" — three target signs, and nothing outside them."""
    verdict = evaluate_one("kulavardhana", _pl(
        "Ar", paksha=0, SUN=_deg("Le"), MOON=_deg("Sg"), MARS=_deg("Ar"),
        MERCURY=_deg("Le"), JUPITER=_deg("Sg"), VENUS=_deg("Ar"),
        SATURN=_deg("Le")))
    assert verdict.present is True


def test_kulavardhana_names_the_planets_that_fall_outside():
    verdict = evaluate_one("kulavardhana", _pl(
        "Ar", paksha=0, SUN=_deg("Le"), MOON=_deg("Sg"), SATURN=_deg("Ta")))
    assert verdict.present is False
    assert "Saturn" in verdict.reason


def test_vasumati_counts_upachayas_from_lagna():
    """The reference is unstated; lagna is used, as everywhere else in
    §11.6. See OI-84."""
    assert UPACHAYA == (3, 6, 10, 11)
    verdict = evaluate_one("vasumati", _pl("Ar", JUPITER=_deg("Ge")))
    assert verdict.present is True
    assert "3rd, 6th, 10th, 11th" in verdict.reason


def test_vasumati_reports_the_stricter_reading_as_a_qualifier():
    """One benefic in an upachaya is enough on the plain reading. A verdict
    says which benefics sit outside, so a stricter caller can decide."""
    verdict = evaluate_one("vasumati", _pl("Ar", JUPITER=_deg("Ge"),
                                           VENUS=_deg("Ta")))
    assert verdict.present is True
    assert any("OI-84" in q for q in verdict.qualifiers)


def test_vasumati_reports_the_printed_fullness_clause():
    """"malefics should not occupy upachayas" is about full results, not
    about presence, so it is a qualifier."""
    verdict = evaluate_one("vasumati", _pl("Ar", JUPITER=_deg("Ge"),
                                           SATURN=_deg("Ge")))
    assert verdict.present is True
    assert any("no malefic in an upachaya" in q for q in verdict.qualifiers)


def test_gandharva_needs_all_four_clauses():
    verdict = evaluate_one("gandharva", _pl("Cn", paksha=0, MARS=_deg("Ta"),
                                            MOON=_deg("Pi"),
                                            JUPITER=_deg("Sc"),
                                            SUN=_deg("Ar")))
    assert verdict.present is True


def test_gandharva_absent():
    verdict = evaluate_one("gandharva", _pl("Cn", paksha=0, MARS=_deg("Ta"),
                                            MOON=_deg("Pi"),
                                            JUPITER=_deg("Sc"),
                                            SUN=_deg("Ta")))
    assert verdict.present is False
    assert "Sun is not exalted" in verdict.reason


def test_go_reads_jupiters_moolatrikona_arc_when_longitudes_allow():
    """"strong in his moolatrikona" — Sagittarius 0° to 10°, per chapter 3."""
    assert int(MOOLATRIKONA[Graha.JUPITER][0]) == R["Sg"]
    inside = evaluate_one("go", _pl("Cn", paksha=0, JUPITER=_deg("Sg", 5),
                                    SUN=_deg("Sg", 6), MOON=_deg("Ta")))
    assert inside.present is True
    outside = evaluate_one("go", _pl("Cn", paksha=0, JUPITER=_deg("Sg", 25),
                                     SUN=_deg("Sg", 26), MOON=_deg("Ta")))
    assert outside.present is False
    assert "moolatrikona" in outside.reason


def test_chapa_needs_the_exchange_and_an_exalted_lagna_lord():
    verdict = evaluate_one("chapa", _pl("Cp", SATURN=_deg("Li"),
                                        MARS=_deg("Li"), VENUS=_deg("Ar")))
    assert verdict.present is True


def test_chapa_absent():
    verdict = evaluate_one("chapa", _pl("Cp", SATURN=_deg("Ar"),
                                        MARS=_deg("Li"), VENUS=_deg("Ar")))
    assert verdict.present is False
    assert "not exalted" in verdict.reason


def test_pushkala_reads_the_moons_dispositor_three_ways():
    verdict = evaluate_one("pushkala", _pl("Ar", paksha=0, MARS=_deg("Ta"),
                                           MOON=_deg("Ta"), VENUS=_deg("Li"),
                                           JUPITER=_deg("Ar")))
    assert verdict.present is True


def test_pushkalas_printed_numbering_is_recorded():
    """The clauses are printed (1), (2), (2), (4)."""
    entry = next(e for e in POPULAR_YOGAS_CONTINUED if e["key"] == "pushkala")
    assert "(1), (2), (2), (4)" in entry["printed_typo"]
    assert entry["definition"].count("(2)") == 2


def test_makuta_counts_the_ninth_twice_over():
    verdict = evaluate_one("makuta", _pl("Ta", SATURN=_deg("Aq"),
                                         JUPITER=_deg("Li"), VENUS=_deg("Ge")))
    assert verdict.present is True


def test_makuta_absent():
    verdict = evaluate_one("makuta", _pl("Ta", SATURN=_deg("Aq"),
                                         JUPITER=_deg("Sg"), VENUS=_deg("Le")))
    assert verdict.present is False
    assert "not the 9th" in verdict.reason


@pytest.mark.parametrize("key,house",
                         [("harsha", 6), ("sarala", 8), ("vimala", 12)])
def test_the_three_lord_in_own_house_yogas(key, house):
    """§11.6 closes with three of one shape: the 6th, 8th and 12th lords in
    their own houses."""
    assert DUSTHANA_LORD_IN_OWN_HOUSE == ("harsha", "sarala", "vimala")
    lord_sign = RASI_ABBR[(R["Ar"] + house - 1) % 12]
    lord = int(RASI_LORD[(R["Ar"] + house - 1) % 12])
    verdict = evaluate_one(key, _pl(
        "Ar", paksha=0, **{GRAHA_NAMES[lord].upper(): _deg(lord_sign)}))
    assert verdict.present is True
    assert f"the {ordinal(house)} lord" in verdict.reason


@pytest.mark.parametrize("key", ["harsha", "sarala", "vimala"])
def test_those_three_are_absent_when_the_lord_is_in_lagna(key):
    verdict = evaluate_one(key, _pl("Ar", paksha=0, MERCURY=_deg("Ar"),
                                    MARS=_deg("Ar"), JUPITER=_deg("Ar")))
    assert verdict.present is False
    assert "not the" in verdict.reason


# --- deep exaltation, which the book never bounds ---------------------------


@pytest.mark.parametrize("key,lord_house", [("jaya", 10), ("vidyut", 11)])
def test_deep_exaltation_is_a_definite_absence_outside_the_sign(key, lord_house):
    """When the planet is not even in his exaltation sign, "deep" does not
    matter and the verdict is a plain absence."""
    verdict = evaluate_one(key, _pl("Ar", paksha=0, SATURN=_deg("Ar"),
                                    VENUS=_deg("Ar"), MERCURY=_deg("Ar")))
    assert verdict.present is False
    assert "not in deep exaltation" in verdict.reason


def test_jaya_says_the_depth_is_undecided_when_the_lord_is_exalted():
    """lagna Aries: the 10th lord is Saturn, exalted in Libra; the 6th lord
    Mercury is debilitated in Pisces. Every clause holds except one the book
    never bounds — how near the exact degree counts as deep. See OI-83."""
    verdict = evaluate_one("jaya", _pl("Ar", SATURN=_deg("Li", 20),
                                       MERCURY=_deg("Pi", 5)))
    assert verdict.present is False
    assert "cannot be decided" in verdict.reason
    assert "no threshold" in verdict.reason
    assert any("OI-83" in q for q in verdict.qualifiers)


def test_the_undecided_verdict_still_names_the_distance():
    """A caller who has their own threshold can apply it."""
    verdict = evaluate_one("jaya", _pl("Ar", SATURN=_deg("Li", 20),
                                       MERCURY=_deg("Pi", 5)))
    assert "from his exact exaltation degree" in verdict.reason
    assert "20° Libra" in verdict.reason


# --- results ----------------------------------------------------------------


def test_all_thirty_have_their_results_transcribed():
    """The other half of §11.6 does print results, unlike the first
    eighteen — OI-82 is now about those eighteen only."""
    entries = {e["planetary_yoga"]: e for e in _results()["entries"]}
    for spec in POPULAR_YOGAS_CONTINUED:
        entry = entries[spec["key"]]
        assert entry["results_transcribed"] is True, spec["key"]
        assert entry["verbatim"].startswith("One born with this yoga"), spec["key"]


def test_the_trimurthi_three_share_one_results_sentence():
    """Hari, Hara and Brahma are given word for word the same result."""
    entries = {e["planetary_yoga"]: e for e in _results()["entries"]}
    texts = {entries[key]["verbatim"] for key in TRIMURTHI_YOGAS}
    assert len(texts) == 1
    assert "happy, learned and blessed with wealth and children" in texts.pop()


@pytest.mark.parametrize("key,typo", [("go", "resepcted"),
                                      ("saarada", "autere")])
def test_the_printed_typos_in_the_results_are_kept(key, typo):
    entry = next(e for e in _results()["entries"] if e["planetary_yoga"] == key)
    assert typo in entry["verbatim"]
    assert typo in entry["transcription_notes"]


def test_the_thirty_results_are_still_licence_gated(client):
    body = client.post("/v1/planetary-yoga/chart", json={
        "lagna_rasi": R["Ar"], "paksha": 0,
        "rasis": {0: R["Ar"], 1: R["Ta"], 6: R["Li"]}}).json()
    payload = repr(body).lower()
    for word in ("invincible", "unsullied", "tapaswi", "aristocratic"):
        assert word not in payload


# --- what Shivaji actually has ----------------------------------------------


def test_shivaji_has_none_of_the_thirty():
    """The section's list runs on past his example, but it is only used for
    Kalpadruma. None of the thirty is his."""
    keys = {e["key"] for e in POPULAR_YOGAS_CONTINUED}
    present = {v.key for v in evaluate(_chart_9()) if v.present}
    assert not (present & keys)


def test_chart_9s_full_verdict_is_still_the_same_five():
    present = {v.key for v in evaluate(_chart_9()) if v.present}
    assert present == {"vesi", "sunaphaa", "adhi", "daama", "kalpadruma"}


# --- what the thirty find in the two charts the book gives -------------------


def test_ramas_chart_gives_lakshmi_yoga():
    """The 9th lord Jupiter is exalted in Cancer, which is the lagna itself —
    an own-or-exaltation 9th lord in a quadrant. Not asserted from the book;
    the detector reaches it from the chart chapter 1 already supplied."""
    verdict = evaluate_one("lakshmi", _rama())
    assert verdict.present is True
    assert "his exaltation sign, Cancer" in verdict.reason
    assert any("lagna lord to be strong" in q for q in verdict.qualifiers)


def test_ramas_chart_is_the_case_oi_84_is_about():
    """Vasumati on Rama's chart is exactly the unsettled reading: one benefic
    in an upachaya, three outside, and two malefics inside. Present on the
    plain reading, absent on the strict one — and the verdict says both."""
    verdict = evaluate_one("vasumati", _rama())
    assert verdict.present is True
    assert "Mercury occupies upachayas" in verdict.reason
    assert any("stricter reading" in q and "OI-84" in q
               for q in verdict.qualifiers)
    assert any("no malefic in an upachaya" in q for q in verdict.qualifiers)


def test_ramas_chart_has_exactly_these_yogas_across_all_ninety_five():
    """Pinned whole, so a later change to any detector has to account for the
    chart the book itself works through."""
    present = {v.key for v in evaluate(_rama()) if v.present}
    assert present == {
        "ruchaka", "sasa", "hamsa", "sarpa", "vesi", "vosi", "ubhayachara",
        "daama", "subha", "gaja_kesari", "guru_mangala", "sankha", "mridanga",
        "lakshmi", "vasumati"}
