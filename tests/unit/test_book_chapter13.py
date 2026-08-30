"""Chapter 13 — interpreting charts.

Section 13.2's functional nature. Table 30 is the authority and is
transcribed; §13.2's five rules are implemented separately and checked against
it, so the places where PVR exercised judgement are named rather than hidden.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.functional import (
    BENEFIC,
    FUNCTIONAL_PLANETS,
    MALEFIC,
    NEUTRAL,
    FunctionalError,
    divergences,
    for_moon,
    from_rules,
    from_table,
    houses_owned,
    is_yogakaraka,
    yogakaraka_of,
)
from hora.core.const import (
    CHAPTER_13_INTRO,
    FUNCTIONAL_NATURE_RULES,
    KENDRA,
    MOON_MOVABLE_WORDING,
    MOON_NOT_LISTED_FOR_MOVABLE,
    MOON_OMITTED_FROM,
    NATURAL_VERSUS_FUNCTIONAL,
    PLACEMENT_RULE,
    RAMAN_REFERENCE,
    RASI_ABBR,
    TABLE_30_FUNCTIONAL_NATURE,
    TRIKONA,
    YOGADA_KINDS,
    YOGADA_LINKS,
    YOGADA_RULE,
)

R = {name: index for index, name in enumerate(RASI_ABBR)}


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# --------------------------------------------------------------------------
# §13.1 — the chapter's own framing
# --------------------------------------------------------------------------

def test_13_1_says_there_is_no_substitute_for_experience():
    assert "no substitute for experience" in CHAPTER_13_INTRO
    assert RAMAN_REFERENCE in CHAPTER_13_INTRO


# --------------------------------------------------------------------------
# §13.2 — Table 30 as transcribed
# --------------------------------------------------------------------------

def test_table_30_covers_twelve_lagnas_and_eighty_one_cells():
    assert set(TABLE_30_FUNCTIONAL_NATURE) == set(RASI_ABBR)
    cells = sum(len(b) + len(n) + len(m)
                for _, b, n, m in TABLE_30_FUNCTIONAL_NATURE.values())
    assert cells == 81, "84 minus the three Moons left out"
    assert 12 * 7 - len(MOON_OMITTED_FROM) == 81


@pytest.mark.parametrize("abbr", sorted(TABLE_30_FUNCTIONAL_NATURE))
def test_each_lagnas_row_partitions_the_planets(abbr):
    """No planet may be in two columns, and only the Moon may be missing."""
    _, benefics, neutrals, malefics = TABLE_30_FUNCTIONAL_NATURE[abbr]
    listed = list(benefics) + list(neutrals) + list(malefics)
    assert len(listed) == len(set(listed)), "a planet appears twice"
    missing = set(FUNCTIONAL_PLANETS) - set(listed)
    assert missing in ({"Moon"}, set())
    if missing:
        assert abbr in MOON_OMITTED_FROM


def test_the_moon_is_omitted_from_exactly_three_lagnas():
    omitted = [abbr for abbr, (_, b, n, m) in TABLE_30_FUNCTIONAL_NATURE.items()
               if "Moon" not in list(b) + list(n) + list(m)]
    assert omitted == list(MOON_OMITTED_FROM) == ["Ar", "Li", "Cp"]


def test_the_moon_is_omitted_exactly_where_he_owns_a_quadrant_but_not_lagna():
    """D-45. §13.2 says "movable rasis", but Cancer is movable and its Moon is
    listed. The condition that actually holds is owning a quadrant other than
    the 1st — and Cancer being the exception is the proof that the 1st counts
    as a trine here."""
    for sign, abbr in enumerate(RASI_ABBR):
        house = houses_owned("Moon", sign)[0]
        omitted = abbr in MOON_OMITTED_FROM
        assert omitted == (house in KENDRA and house != 1), abbr
    assert houses_owned("Moon", R["Cn"]) == (1,)
    assert "Cancer is movable" in MOON_MOVABLE_WORDING


@pytest.mark.parametrize("abbr", MOON_OMITTED_FROM)
def test_the_omitted_moon_gets_a_verdict_once_the_phase_is_known(abbr):
    """Never a bare absence: both branches are answered."""
    sign = R[abbr]
    undecided = from_table("Moon", sign)
    assert undecided.nature is None
    assert undecided.depends_on_phase == {"waxing": MALEFIC, "waning": NEUTRAL}
    assert "waxing" in undecided.why and "waning" in undecided.why

    assert for_moon(sign, waxing=True).nature == MALEFIC
    assert for_moon(sign, waxing=False).nature == NEUTRAL
    assert "natural benefic" in MOON_NOT_LISTED_FOR_MOVABLE


def test_a_listed_moon_ignores_the_phase():
    """Cancer's Moon owns the 1st, so no branch applies."""
    for waxing in (True, False):
        assert for_moon(R["Cn"], waxing).nature == BENEFIC


# --------------------------------------------------------------------------
# The yogakaraka rule
# --------------------------------------------------------------------------

def test_the_six_yogakarakas_derive_exactly():
    """Derived from lordship, checked against Table 30's own column."""
    ours = {abbr: yogakaraka_of(R[abbr]) for abbr in RASI_ABBR}
    printed = {abbr: yoga
               for abbr, (yoga, *_) in TABLE_30_FUNCTIONAL_NATURE.items()}
    assert ours == printed
    assert sorted(a for a, y in ours.items() if y) == [
        "Aq", "Cn", "Cp", "Le", "Li", "Ta"]


def test_the_first_house_counts_as_neither_for_the_yogakaraka_rule():
    """Letting the 1st serve as the trine would name ten yogakarakas where
    Table 30 names six — Gemini's and Virgo's Mercury and Sagittarius's and
    Pisces's Jupiter would join, each owning the lagna and one quadrant."""
    def loosely(planet: str, sign: int) -> bool:
        """The 1st allowed to serve as the trine, the other house as the
        quadrant — a pair of *different* houses either way."""
        houses = set(houses_owned(planet, sign))
        return any(a != b and a in KENDRA and b in TRIKONA
                   for a in houses for b in houses)

    would_add = sorted(
        (abbr, planet)
        for sign, abbr in enumerate(RASI_ABBR)
        for planet in FUNCTIONAL_PLANETS
        if loosely(planet, sign) and not is_yogakaraka(planet, sign)
    )
    assert would_add == [
        ("Ge", "Mercury"), ("Pi", "Jupiter"), ("Sg", "Jupiter"),
        ("Vi", "Mercury")]

    loose_lagnas = {abbr for sign, abbr in enumerate(RASI_ABBR)
                    if any(loosely(p, sign) for p in FUNCTIONAL_PLANETS)}
    assert len(loose_lagnas) == 10, "against Table 30's six"


def test_every_yogakaraka_is_a_functional_benefic_in_table_30():
    """§13.2 calls a yogakaraka an "excellent planet", and the table agrees
    without exception."""
    for abbr, (yoga, benefics, _, _) in TABLE_30_FUNCTIONAL_NATURE.items():
        if yoga:
            assert yoga in benefics, abbr


def test_no_lagna_has_two_yogakarakas():
    for sign in range(12):
        found = [p for p in FUNCTIONAL_PLANETS if is_yogakaraka(p, sign)]
        assert len(found) <= 1, (sign, found)


# --------------------------------------------------------------------------
# The stated rules against the table
# --------------------------------------------------------------------------

def test_the_rules_reproduce_seventy_two_of_the_eighty_one_cells():
    agree = sum(
        1
        for sign in range(12)
        for planet in FUNCTIONAL_PLANETS
        if (t := from_table(planet, sign)).nature is not None
        and from_rules(planet, sign) == t.nature
    )
    assert agree == 72
    assert len(divergences()) == 9
    assert agree + len(divergences()) == 81


def test_eight_of_the_nine_divergences_are_planets_owning_two_rasis():
    """Which is exactly what §13.2 warns about: "In the case of planets owning
    two rasis, we need to judiciously combine the two indications." The table
    records a judgement the rules do not determine."""
    two_rasi = [d for d in divergences() if len(d[2]) == 2]
    one_rasi = [d for d in divergences() if len(d[2]) == 1]
    assert len(two_rasi) == 8
    assert len(one_rasi) == 1
    assert one_rasi[0][:2] == ("Ta", "Sun")


def test_the_one_single_rasi_divergence_is_taurus_sun():
    """D-46. Sun owns only Leo, the 4th from Taurus. The rule for a quadrant
    lord who is a natural malefic is "functionally neutral"; Table 30 lists
    him as a functional benefic. No combining is involved, so this is a
    straight disagreement between the rules and the table."""
    assert houses_owned("Sun", R["Ta"]) == (4,)
    assert from_rules("Sun", R["Ta"]) == NEUTRAL
    assert from_table("Sun", R["Ta"]).nature == BENEFIC


def test_the_other_two_natural_malefic_quadrant_lords_follow_the_rule():
    """Sun owning a single quadrant elsewhere is neutral, as the rule says —
    so D-46 really is one cell and not a pattern."""
    for abbr in ("Sc", "Aq"):
        assert houses_owned("Sun", R[abbr])[0] in KENDRA
        assert from_rules("Sun", R[abbr]) == NEUTRAL
        assert from_table("Sun", R[abbr]).nature == NEUTRAL


def test_the_first_house_is_read_as_a_trine_for_a_planets_own_nature():
    """Forced by Cancer: its Moon owns only the 1st and is listed benefic. Read
    as a quadrant he would be phase-dependent and left out like the other
    three movable lagnas."""
    assert houses_owned("Moon", R["Cn"]) == (1,)
    assert from_table("Moon", R["Cn"]).nature == BENEFIC
    assert from_rules("Moon", R["Cn"]) == BENEFIC
    assert "Cn" not in MOON_OMITTED_FROM


@pytest.mark.parametrize("planet", FUNCTIONAL_PLANETS)
def test_every_planet_owns_one_or_two_houses_from_every_lagna(planet):
    for sign in range(12):
        houses = houses_owned(planet, sign)
        assert len(houses) in (1, 2)
        assert all(1 <= h <= 12 for h in houses)
    assert len(houses_owned(planet, 0)) == (1 if planet in ("Sun", "Moon")
                                            else 2)


def test_rahu_and_ketu_have_no_functional_nature():
    """Every rule in §13.2 turns on lordship, and they own nothing."""
    for name in ("Rahu", "Ketu"):
        with pytest.raises(FunctionalError, match="owns no rasi"):
            houses_owned(name, 0)


def test_an_out_of_range_lagna_is_refused():
    from hora.core.validate import InputError

    with pytest.raises(InputError):
        houses_owned("Sun", 12)


# --------------------------------------------------------------------------
# The rest of §13.2
# --------------------------------------------------------------------------

def test_the_placement_rule_inverts_for_functional_malefics():
    assert "quadrants (sustenance) and trines (prosperity)" in PLACEMENT_RULE
    assert "unless it is very strong" in PLACEMENT_RULE
    assert "3rd house and dusthanas" in PLACEMENT_RULE
    assert "spoiling the significations of the bad houses" in PLACEMENT_RULE


def test_the_two_yogadas_and_what_each_governs():
    assert YOGADA_KINDS == {
        "HL": "money matters",
        "GL": "the matters of power and authority"}
    assert YOGADA_LINKS == ("aspects", "conjoins", "owns")
    for link in YOGADA_LINKS:
        assert link in YOGADA_RULE
    assert "Irrespective of their functional nature" in YOGADA_RULE


def test_a_yogada_needs_lagna_as_well_as_the_special_lagna():
    """"aspects or conjoins or owns HL *and* lagna" — both, not either."""
    assert "owns HL and lagna" in YOGADA_RULE
    assert "owns GL and lagna" in YOGADA_RULE


def test_natural_and_functional_nature_are_independent():
    """§13.2's analogy, and the table bears it out: Jupiter and Venus are
    natural benefics yet functional malefics for several lagnas, and Saturn
    and Mars are natural malefics yet functional benefics for others."""
    assert "natural benefics can become functional malefics" \
        in NATURAL_VERSUS_FUNCTIONAL

    natural_benefic_but_functional_malefic = {
        abbr for abbr, (_, _, _, malefics) in TABLE_30_FUNCTIONAL_NATURE.items()
        if {"Jupiter", "Venus"} & set(malefics)}
    natural_malefic_but_functional_benefic = {
        abbr for abbr, (_, benefics, _, _) in TABLE_30_FUNCTIONAL_NATURE.items()
        if {"Saturn", "Mars", "Sun"} & set(benefics)}
    assert len(natural_benefic_but_functional_malefic) >= 6
    assert len(natural_malefic_but_functional_benefic) >= 6


def test_the_five_rules_are_transcribed_in_order():
    assert len(FUNCTIONAL_NATURE_RULES) == 5
    assert FUNCTIONAL_NATURE_RULES[0].startswith("The lords of trines")
    assert "8th house is more malefic" in FUNCTIONAL_NATURE_RULES[3]
    assert "yogakaraka" in FUNCTIONAL_NATURE_RULES[4]


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------

def test_the_lagna_endpoint_serves_table_30s_row(client):
    body = client.get("/v1/functional/lagna", params={"sign": R["Ta"]}).json()
    assert body["lagna_name"] == "Taurus"
    assert body["yogakaraka"] == "Saturn"
    by_planet = {p["planet"]: p["nature"] for p in body["planets"]}
    assert by_planet["Saturn"] == BENEFIC
    assert by_planet["Venus"] == MALEFIC
    assert body["moon_needs_phase"] is False


def test_the_lagna_endpoint_flags_a_moon_that_needs_its_phase(client):
    body = client.get("/v1/functional/lagna", params={"sign": R["Ar"]}).json()
    assert body["moon_needs_phase"] is True
    moon = next(p for p in body["planets"] if p["planet"] == "Moon")
    assert moon["nature"] is None
    assert moon["depends_on_phase"] == {"waxing": MALEFIC, "waning": NEUTRAL}


def test_the_planet_endpoint_takes_the_moons_phase(client):
    for waxing, expected in ((True, MALEFIC), (False, NEUTRAL)):
        body = client.post("/v1/functional/planet", json={
            "planet": "Moon", "lagna": R["Li"], "waxing": waxing}).json()
        assert body["nature"] == expected


def test_the_planet_endpoint_refuses_a_node(client):
    response = client.post("/v1/functional/planet",
                           json={"planet": "Rahu", "lagna": 0})
    assert response.status_code == 400
    assert "owns no rasi" in response.json()["error"]["message"]


def test_the_rules_endpoint_carries_13_2(client):
    body = client.get("/v1/functional/rules").json()
    assert len(body["rules"]) == 5
    assert len(body["table_30"]) == 12
    assert len(body["divergences"]) == 9
    assert len(body["yogakarakas"]) == 6
    assert body["moon_omitted_from"] == ["Ar", "Li", "Cp"]
    assert "72 of the" in body["table_is_the_authority"]
    assert "Rahu and Ketu own no rasi" in body["planets_note"]


# --------------------------------------------------------------------------
# §13.3 — Baadhakas, and Table 31
# --------------------------------------------------------------------------

from hora.charts.baadhaka import (
    CO_LORDS,
    BaadhakaError,
    baadhaka_of,
    baadhaka_sthaana,
    baadhakas,
    is_baadhaka,
    table_31,
)
from hora.core.const import (
    BAADHAKA_EXAMPLE_STEPS,
    BAADHAKA_HOUSE_BY_MODALITY,
    BAADHAKA_INCLUDES_OCCUPANTS,
    BAADHAKA_SCOPE,
    BAADHAKA_TAKES_BOTH_CO_LORDS,
    GRAHA_NAMES,
    MODALITY_NAMES_EN,
    RASI_MODALITY,
    TABLE_31_BAADHAKAS,
    Graha,
)


def test_the_rule_is_eleventh_ninth_seventh_by_modality():
    """"For a house falling in a movable/fixed/dual rasi, the 11th/9th/7th
    house (respectively) from there becomes baadhaka sthaana"."""
    assert BAADHAKA_HOUSE_BY_MODALITY == (11, 9, 7)
    assert MODALITY_NAMES_EN == ["movable", "fixed", "dual"]


def test_table_31_derives_from_the_rule_above_it():
    """All twenty-four entries — twelve sthaanas and fourteen lords."""
    assert table_31() == TABLE_31_BAADHAKAS
    assert len(TABLE_31_BAADHAKAS) == 12
    assert sum(len(lords) for _, lords in TABLE_31_BAADHAKAS.values()) == 14


@pytest.mark.parametrize("abbr", sorted(TABLE_31_BAADHAKAS))
def test_each_baadhaka_sthaana_is_the_right_house_from_its_rasi(abbr):
    sign = R[abbr]
    house = BAADHAKA_HOUSE_BY_MODALITY[RASI_MODALITY[sign]]
    assert (sign + house - 1) % 12 == baadhaka_sthaana(sign)
    assert RASI_ABBR[baadhaka_sthaana(sign)] == TABLE_31_BAADHAKAS[abbr][0]


def test_a_baadhaka_sthaana_is_never_the_sign_itself():
    """11th, 9th and 7th are all distinct from the 1st, so nothing troubles
    itself."""
    for sign in range(12):
        assert baadhaka_sthaana(sign) != sign


def test_the_modalities_map_to_three_disjoint_groups_of_four():
    groups: dict[int, list[str]] = {}
    for sign in range(12):
        groups.setdefault(RASI_MODALITY[sign], []).append(RASI_ABBR[sign])
    assert groups[0] == ["Ar", "Cn", "Li", "Cp"]
    assert groups[1] == ["Ta", "Le", "Sc", "Aq"]
    assert groups[2] == ["Ge", "Vi", "Sg", "Pi"]


def test_table_31_names_both_co_lords_where_the_sthaana_is_co_owned():
    """Aries' sthaana is Aquarius and Capricorn's is Scorpio. Table 31 gives
    "Saturn & Rahu" and "Mars & Ketu" — both, not the stronger one. §9.2's
    arudha needs exactly one of the same pair, which is the opposite."""
    assert TABLE_31_BAADHAKAS["Ar"] == ("Aq", ("Saturn", "Rahu"))
    assert TABLE_31_BAADHAKAS["Cp"] == ("Sc", ("Mars", "Ketu"))
    assert set(CO_LORDS) == {R["Sc"], R["Aq"]}
    assert "both co-lords" in BAADHAKA_TAKES_BOTH_CO_LORDS

    two_lord_rasis = {abbr for abbr, (_, lords) in TABLE_31_BAADHAKAS.items()
                      if len(lords) == 2}
    assert two_lord_rasis == {"Ar", "Cp"}


def test_the_co_lords_are_reused_from_section_15_5_1_not_retyped():
    from hora.charts.colord import CO_LORDS as SOURCE

    assert {int(k): tuple(int(g) for g in v) for k, v in SOURCE.items()} \
        == CO_LORDS


@pytest.mark.parametrize(
    "reads,rasi,sthaana,lords,trouble", BAADHAKA_EXAMPLE_STEPS,
    ids=[s[0] for s in BAADHAKA_EXAMPLE_STEPS])
def test_13_3s_worked_example(reads, rasi, sthaana, lords, trouble):
    """A D-10 with lagna in Gemini. Both halves derived, neither transcribed."""
    result = baadhaka_of(R[rasi])
    assert RASI_ABBR[result.sthaana] == sthaana
    assert tuple(str(GRAHA_NAMES[g]) for g in result.lords) == lords
    assert trouble


def test_13_3s_example_reads_the_ninth_house_not_only_lagna():
    """"Aq is the 9th house" — from a Gemini lagna. The example makes the
    point that a baadhaka is taken from any house, not just lagna."""
    assert (R["Ge"] + 9 - 1) % 12 == R["Aq"]
    assert "every house and arudha pada" in BAADHAKA_SCOPE


def test_a_baadhaka_troubles_by_occupancy_as_well_as_lordship():
    """"the periods of Jupiter **and planets in Sg**" — occupants count."""
    d10 = {int(Graha.SUN): R["Sg"], int(Graha.MARS): R["Sg"],
           int(Graha.VENUS): R["Li"], int(Graha.JUPITER): R["Ta"]}
    result = baadhaka_of(R["Ge"], d10)
    assert result.lords == (int(Graha.JUPITER),)
    assert result.occupants == tuple(sorted(
        (int(Graha.SUN), int(Graha.MARS))))

    mars = is_baadhaka(int(Graha.MARS), R["Ge"], d10)
    assert mars["is_baadhaka"] is True
    assert mars["by_occupancy"] is True and mars["by_lordship"] is False
    jupiter = is_baadhaka(int(Graha.JUPITER), R["Ge"], d10)
    assert jupiter["by_lordship"] is True and jupiter["by_occupancy"] is False
    assert "through whoever occupies it" in BAADHAKA_INCLUDES_OCCUPANTS


def test_without_positions_the_answer_says_what_it_could_not_decide():
    """Never a bare false: occupancy is unknown, and the reason says so."""
    verdict = is_baadhaka(int(Graha.MARS), R["Ge"])
    assert verdict["is_baadhaka"] is False
    assert verdict["occupancy_known"] is False
    assert "cannot be decided without graha positions" in verdict["why"]

    result = baadhaka_of(R["Ge"])
    assert result.occupants == ()
    assert "no positions were given" in result.why


def test_with_positions_and_an_empty_sthaana_the_answer_says_that_too():
    d10 = {int(Graha.VENUS): R["Li"]}
    result = baadhaka_of(R["Ge"], d10)
    assert result.occupants == ()
    assert "nothing occupies the sthaana" in result.why


def test_every_sign_has_a_baadhaka_and_a_reason():
    for sign in range(12):
        result = baadhaka_of(sign)
        assert result.lords
        assert result.modality in MODALITY_NAMES_EN
        assert result.why
        assert baadhakas(sign) == result.lords


def test_an_out_of_range_sign_or_graha_position_is_refused():
    from hora.core.validate import InputError

    with pytest.raises(InputError):
        baadhaka_sthaana(12)
    with pytest.raises(InputError):
        baadhaka_of(0, {int(Graha.SUN): 12})
    assert issubclass(BaadhakaError, InputError)


def test_the_baadhakas_endpoint_serves_table_31(client):
    body = client.get("/v1/baadhakas/rules").json()
    assert body["derived_matches_printed"] is True
    assert body["house_by_modality"] == {
        "movable": 11, "fixed": 9, "dual": 7}
    assert body["table_31"]["Ar"] == {
        "sthaana": "Aq", "baadhakas": ["Saturn", "Rahu"]}
    assert len(body["example_steps"]) == 2


def test_the_sign_endpoint_answers_for_an_arudha_not_only_a_house(client):
    """§13.4.1 asks "if a planet is a baadhaka from A3" — the endpoint takes
    whatever rasi the arudha falls in, with no notion of lagna."""
    body = client.post("/v1/baadhakas/sign", json={"sign": R["Aq"]}).json()
    assert body["sthaana_name"] == "Libra"
    assert body["lords"] == ["Venus"]
    assert body["modality"] == "fixed"


def test_the_chart_endpoint_gives_all_twelve_houses(client):
    body = client.post("/v1/baadhakas/chart",
                       json={"lagna_sign": R["Ge"]}).json()
    assert len(body["houses"]) == 12
    first = body["houses"][0]
    ninth = body["houses"][8]
    assert first["sign_name"] == "Gemini" and first["lords"] == ["Jupiter"]
    assert ninth["sign_name"] == "Aquarius" and ninth["lords"] == ["Venus"]


def test_the_check_endpoint_reports_how_not_just_whether(client):
    body = client.post("/v1/baadhakas/check", json={
        "graha": int(Graha.MARS), "sign": R["Ge"],
        "graha_signs": {str(int(Graha.MARS)): R["Sg"]},
    }).json()
    assert body["is_baadhaka"] is True
    assert body["by_occupancy"] is True
    assert body["by_lordship"] is False


# --------------------------------------------------------------------------
# §13.4.1 — Basic Guidelines
# --------------------------------------------------------------------------

from hora.charts.analysis import (
    MATTERS,
    AnalysisError,
    influence_frame,
    influences_on,
)
from hora.charts.analysis import plan as analysis_plan
from hora.core.const import (
    A3_PERIODS,
    ANALYSIS_CLOSING,
    ANALYSIS_CLOSING_POINTS_AT,
    BASIC_GUIDELINES,
    D24_MATTERS,
    DIVISIONAL_CHART_FOR,
    INFLUENCE_FRAME,
    INFLUENCE_KINDS,
    STANDARD_RESULTS_NOT_IMPLEMENTED,
    STANDARD_RESULTS_RULE,
    THIRD_HOUSE_VERSUS_A3,
)

#: A whole D-10, so factor 5 has something to work on.
_D10 = {
    int(Graha.SUN): 3, int(Graha.MOON): 6, int(Graha.MARS): 1,
    int(Graha.MERCURY): 7, int(Graha.JUPITER): 9, int(Graha.VENUS): 10,
    int(Graha.SATURN): 2, int(Graha.RAHU): 5, int(Graha.KETU): 11,
}


def test_the_six_factors_are_transcribed_in_order():
    names = [name for name, _ in BASIC_GUIDELINES]
    assert names == ["Divisional Chart", "House", "Reference",
                     "House vs Arudha", "Influences", "Standard Results"]


@pytest.mark.parametrize("matter,chart,note", DIVISIONAL_CHART_FOR)
def test_factor_1s_chart_for_each_matter(matter, chart, note):
    result = analysis_plan(matter)
    assert result.chart == chart
    assert result.why == note


def test_factor_1_includes_the_case_where_the_rasi_chart_wins():
    """"in a culture where marriage is not a dharma ... then rasi chart may be
    better than D-9" — the same subject, two charts, decided by culture."""
    assert analysis_plan("marriage").chart == "D9"
    assert analysis_plan("marriage as merely living together").chart == "D1"


@pytest.mark.parametrize(
    "matter,house,references,arudha,note", D24_MATTERS,
    ids=[m[0] for m in D24_MATTERS])
def test_factors_2_to_4_from_the_d24_worked_example(
        matter, house, references, arudha, note):
    result = analysis_plan(matter)
    assert result.chart == "D24"
    assert result.house == house
    assert result.references == references
    assert result.arudha == arudha


def test_factor_2s_three_houses_of_the_d24_example():
    """4th education, 5th intelligence and its neighbours, 7th the people."""
    by_house: dict[int, set[str]] = {}
    for matter, house, *_ in D24_MATTERS:
        by_house.setdefault(house, set()).add(matter)
    assert set(by_house) == {4, 5, 7}
    assert by_house[4] == {"education"}
    assert "intelligence" in by_house[5] and "scholarship" in by_house[5]
    assert by_house[7] == {"the people one interacts with while learning"}


def test_factor_3_splits_the_true_self_from_the_perceived_self():
    """"academic reputation is related more to the perceived self (AL) than
    the true self (lagna)". Intelligence and scholarship go the other way."""
    assert analysis_plan("academic reputation").references[0] == "AL"
    assert analysis_plan("intelligence").references[0] == "lagna"
    assert analysis_plan("scholarship").references[0] == "lagna"


def test_factor_3_offers_a_karaka_as_a_second_reference():
    """"When the relevant karakas are stronger, we can use them as references
    instead of lagna." Each karaka the section names, against its matter."""
    assert analysis_plan("scholarship").references == ("lagna", "Mercury")
    assert analysis_plan("intelligence").references == ("lagna", "Jupiter")
    assert analysis_plan("academic reputation").references == ("AL", "Sun")
    assert analysis_plan("students").references == ("the 5th lord",)


def test_factor_4_prefers_an_arudha_for_exactly_two_matters():
    """A7 for the people one interacts with, A5 for distinctions and awards.
    Both are impressions others form, which is why they are arudhas."""
    with_arudha = {m.matter: m.arudha for m in MATTERS.values() if m.arudha}
    assert with_arudha == {
        "the people one interacts with while learning": "A7",
        "academic distinctions and awards": "A5",
    }


def test_a_matter_the_section_does_not_name_is_refused_with_the_reason():
    """§13.4.1 teaches a method and works two charts through it. Guessing a
    correspondence it never gives would be inventing doctrine."""
    with pytest.raises(AnalysisError, match="does not name"):
        analysis_plan("litigation")
    with pytest.raises(AnalysisError, match="influences_on"):
        analysis_plan("litigation")


# -- factor 5 ---------------------------------------------------------------

def test_the_influence_frame_is_counted_from_the_house_not_from_lagna():
    """"finding houses *with respect to* that house"."""
    frame = influence_frame(R["Ar"])
    assert frame["quadrants"]["signs"] == [R[a] for a in
                                           ("Ar", "Cn", "Li", "Cp")]
    assert frame["trines"]["signs"] == [R[a] for a in ("Ar", "Le", "Sg")]

    shifted = influence_frame(R["Cn"])
    assert shifted["quadrants"]["signs"] == [R[a] for a in
                                             ("Cn", "Li", "Cp", "Ar")]


@pytest.mark.parametrize("name,houses,effect", INFLUENCE_FRAME)
def test_each_house_class_carries_the_effect_13_4_1_gives_it(
        name, houses, effect):
    frame = influence_frame(0)
    assert frame[name]["houses"] == list(houses)
    assert frame[name]["effect"] == effect
    assert effect in (
        "sustain it", "let it prosper", "let it grow", "bring obstacles")


def test_influences_on_composes_all_five_kinds():
    """Rasi drishti, graha drishti, argala, the house classes, baadhaka —
    every kind §13.4.1 names, and every one already existed elsewhere."""
    out = influences_on(R["Cn"], _D10)
    kinds = {i["kind"] for i in out["influences"]}
    assert "rasi drishti" in kinds
    assert "graha drishti" in kinds
    assert {"argala", "virodhargala"} & kinds
    assert {"quadrants", "trines", "upachayas", "dusthanas"} & kinds
    assert "baadhaka" in kinds
    for kind in INFLUENCE_KINDS:
        assert kind in ("rasi drishti", "graha drishti", "argala")


def test_every_influence_carries_an_effect_and_a_detail():
    """No bare list of planets: each row says what it does and why."""
    for row in influences_on(R["Cn"], _D10)["influences"]:
        assert row["effect"]
        assert row["detail"]
        assert row["graha_name"]


def test_influences_reports_which_grahas_touch_nothing():
    """The complement is as much an answer as the list."""
    out = influences_on(R["Cn"], _D10)
    touched = {i["graha_name"] for i in out["influences"]}
    for name in out["untouched"]:
        assert name not in touched
    assert set(out["by_graha"]) == touched | set(out["untouched"])


def test_influences_uses_13_3s_baadhaka_from_the_house_itself():
    """Not from lagna — §13.4.1 says "if a planet is a baadhaka from A3"."""
    out = influences_on(R["Aq"], _D10)
    assert out["baadhaka"]["sthaana_name"] == "Libra"
    assert out["baadhaka"]["lords"] == ["Venus"]


def test_influences_without_positions_is_refused_with_the_reason():
    with pytest.raises(AnalysisError, match="graha positions"):
        influences_on(0, {})


def test_the_a3_example_names_three_placements_including_a_baadhaka():
    """"While the 3rd house shows one's writing skills, it is A3 that shows
    one's books." Quadrant writes, the 8th obstructs, a baadhaka troubles."""
    assert len(A3_PERIODS) == 3
    where = [w for w, _ in A3_PERIODS]
    assert "in a quadrant from A3" in where
    assert "in the 8th house from A3" in where
    assert "a baadhaka from A3" in where
    assert "writing skills" in THIRD_HOUSE_VERSUS_A3
    assert "books" in THIRD_HOUSE_VERSUS_A3


def test_the_a3_examples_quadrant_and_eighth_agree_with_the_frame():
    """The example's own two placements are the frame's quadrants and
    dusthanas, so it is an instance of factor 5 rather than a separate rule."""
    frame = influence_frame(R["Cn"])
    assert 1 in frame["quadrants"]["houses"]
    assert 8 in frame["dusthanas"]["houses"]


def test_factor_6_points_outside_the_book_and_nothing_computes_it():
    assert "should be mastered" in STANDARD_RESULTS_RULE
    assert "does not reproduce them" in STANDARD_RESULTS_NOT_IMPLEMENTED
    assert "Raman" in STANDARD_RESULTS_NOT_IMPLEMENTED


def test_the_closing_sentence_points_at_four_things_we_already_built():
    assert "strength and avasthas" in ANALYSIS_CLOSING
    assert "ashtakavarga strength" in ANALYSIS_CLOSING
    assert "yogas" in ANALYSIS_CLOSING
    assert len(ANALYSIS_CLOSING_POINTS_AT) == 4
    for _, where in ANALYSIS_CLOSING_POINTS_AT:
        assert where.startswith("chapter")


# -- endpoints --------------------------------------------------------------

def test_the_analysis_rules_endpoint_carries_13_4_1(client):
    body = client.get("/v1/analysis/rules").json()
    assert len(body["factors"]) == 6
    assert len(body["divisional_chart_for"]) == 7
    assert len(body["d24_worked_example"]) == 7
    assert len(body["a3_periods"]) == 3
    assert len(body["closing_points_at"]) == 4
    assert "baadhaka" in body["influence_kinds"]


def test_the_matter_endpoint_answers_and_refuses(client):
    body = client.get("/v1/analysis/matter",
                      params={"name": "career and achievements in society"})
    assert body.json()["chart"] == "D10"

    refused = client.get("/v1/analysis/matter", params={"name": "litigation"})
    assert refused.status_code == 400
    assert "does not name" in refused.json()["error"]["message"]


def test_the_matters_endpoint_lists_them_all_with_the_caveat(client):
    body = client.get("/v1/analysis/matters").json()
    assert len(body["matters"]) == len(MATTERS) == 14
    assert "not a list of every question" in body["not_a_lookup_table"]


def test_the_influences_endpoint_composes_the_five_kinds(client):
    body = client.post("/v1/analysis/influences", json={
        "sign": R["Cn"],
        "graha_signs": {str(k): v for k, v in _D10.items()},
    }).json()
    kinds = {i["kind"] for i in body["influences"]}
    assert "baadhaka" in kinds and "rasi drishti" in kinds
    assert set(body["frame"]) == {"quadrants", "trines", "upachayas",
                                  "dusthanas"}
