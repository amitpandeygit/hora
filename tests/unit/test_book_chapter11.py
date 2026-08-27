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
from hora.core.const import (
    ADHI_EXAMPLE_CONTRADICTS_RULE,
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
    COMBUSTION_WEAKENS_YOGA,
    HAMSA_MISNAMED_IN_ITS_DEFINITION,
    KEMADRUMA_KILLS_OTHER_YOGAS,
    MAALAVYA_SPELLING_VARIANTS,
    MAHAPURUSHA_ELEMENT_RULERS_SENTENCE,
    MAHAPURUSHA_FOOTNOTES_UNREAD,
    MAHAPURUSHA_INTRO,
    MAHAPURUSHA_REFERENCE_RULE,
    MAHAPURUSHA_TERMS,
    MAHAPURUSHA_YOGAS,
    PANAPHARA_SPELLING_VARIANTS,
    PANCHA_BHOOTA_NAMES,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
    RAVI_YOGAS,
    TATTVA_GLOSS_IN_3_2_8,
    TATTVA_GLOSS_IN_11_4,
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
    verdicts = {v.key: v for v in evaluate(_in(SUN="Ar"))}
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

    Every `group` named by a registered spec must have a module of that name
    under `charts/planetary_yogas/`, and the package must import it.
    """
    import pathlib

    import hora.charts.planetary_yogas as package

    source = pathlib.Path(package.__file__).read_text()
    directory = pathlib.Path(package.__file__).parent
    for group in groups():
        assert (directory / f"{group}.py").is_file(), group
        assert f"import {group}" in source, group


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
    assert body["groups"] == ["chandra", "mahapurusha", "ravi"]
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
    from hora.core.const import UPACHAYA

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


def test_footnotes_29_and_30_have_not_been_supplied():
    """"He is rabbit-like²⁹" in §11.4.3 and "He is swan-like³⁰" in §11.4.5.
    The footnote text has not been given to us; the name meanings recorded
    come from the results sentences themselves, not from the footnotes.
    """
    assert MAHAPURUSHA_FOOTNOTES_UNREAD == (29, 30)
    by_key = {y["key"]: y for y in MAHAPURUSHA_YOGAS}
    assert by_key["sasa"]["name_means"] == "rabbit"
    assert by_key["hamsa"]["name_means"] == "swan"
    assert by_key["ruchaka"]["name_means"] is None
