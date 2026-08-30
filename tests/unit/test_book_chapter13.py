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
