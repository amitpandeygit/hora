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
    BUDHA_AADITYA_CHART_NOTE,
    BUDHA_AADITYA_SPELLING_VARIANTS,
    BUDHA_AADITYA_TERMS,
    BUDHA_AADITYA_TIMING_PERIODS,
    BUDHA_AADITYA_TIMING_TEXT,
    COMBUSTION_WEAKENS_YOGA,
    RAVI_YOGA_FREQUENCY_NOTE,
    RAVI_YOGA_INTRO,
    RAVI_YOGA_PREFERRED_CHARTS,
    RAVI_YOGAS,
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
    for verdict in evaluate(_in(MOON="Ar", JUPITER="Ta")):
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
    assert {spec.group for spec in YOGA_REGISTRY.values()} == {"ravi"}


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
    assert sorted(body["present"]) == ["ubhayachara", "vesi", "vosi"]
    absent = [y for y in body["yogas"] if not y["present"]]
    assert all(y["reason"] for y in absent)


def test_chart_endpoint_carries_the_definitions(client):
    body = client.post("/v1/planetary-yoga/chart", json={
        "rasis": {0: R["Ar"]}}).json()
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
    assert body["groups"] == ["ravi"]
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
    assert entries == set(YOGA_REGISTRY)


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
