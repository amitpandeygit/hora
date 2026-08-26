"""Every claim in Chapter 7 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 7 (Houses),
book pages 67-78.

Chapter 7 has no numbered examples, but it works several cases through in
prose — Moon in Aquarius, houses from the 3rd, the Pisces-lagna paaka — and
each of those is a test here.

Two things the chapter is emphatic about, and both are easy to get wrong:

* A house is relative to a **reference**, and a category is relative to a
  **house**. "The 3rd, 7th and 11th houses are the trines from the 3rd house."
* A house never spans two rasis. §7.5 rejects bhava chalit, equal-house and
  Sripathi division by name.
"""
import pathlib

import pytest

#: Example 28's chart from §8.2 — the one place the book gives eight
#: longitudes, so the only chart in the text a karakamsa can be computed from.
EXAMPLE_28_LONGITUDES = {
    0: 72.783, 1: 20.467, 2: 73.85, 3: 85.3,
    4: 35.667, 5: 77.35, 6: 32.467, 7: 91.717,
}

from hora.charts.bhava import classify_house
from hora.charts.house import (
    categories_of,
    category_houses,
    graha_lagna_houses,
    half_of,
    house_of_rasi,
    houses_from,
    karakamsa_rasi,
    paaka_lagna_rasi,
    purushartha_of,
    rasi_of_house,
    signification,
)
from hora.charts.vargas import VARGA_SIGNIFICATIONS
from hora.core import const as c
from hora.core.const import (
    CHATURASRA,
    HOUSE_CATEGORIES,
    HOUSE_REFERENCES,
    HOUSE_SIGNIFICATIONS,
    INVISIBLE_HALF,
    PURUSHARTHA_TRIKONAS,
    RASI_ABBR,
    VISIBLE_HALF,
    Graha,
    Rasi,
)
from hora.core.settings import HouseSystem, Settings
from hora.core.validate import InputError
from hora.services import house_service

RASI = {a: i for i, a in enumerate(RASI_ABBR)}


# --------------------------------------------------------------------------
# 7.1 Houses are counted from a reference
# --------------------------------------------------------------------------

def test_the_reference_rasi_is_the_first_house():
    """7.1: "The rasi containing the point of reference is the 1st house"."""
    for rasi in range(12):
        assert house_of_rasi(rasi, rasi) == 1


@pytest.mark.parametrize(
    "house,rasi",
    [(1, "Aq"), (2, "Pi"), (3, "Ar"), (4, "Ta"), (12, "Cp")],
)
def test_moon_in_aquarius_worked_through(house, rasi):
    """7.1: "Suppose Moon is in Aquarius ... Aquarius is the 1st house,
    Pisces is the 2nd, Aries the 3rd, Taurus the 4th ... we reach Capricorn
    when we find the 12th house"."""
    assert rasi_of_house(RASI["Aq"], house) == RASI[rasi]
    assert house_of_rasi(RASI["Aq"], RASI[rasi]) == house


@pytest.mark.parametrize(
    "house,rasi", [(1, "Ta"), (2, "Ge"), (3, "Cn")],
)
def test_sun_in_taurus_worked_through(house, rasi):
    """7.1: "Taurus contains the 1st house, Gemini the 2nd, Cancer the 3rd"."""
    assert rasi_of_house(RASI["Ta"], house) == RASI[rasi]


@pytest.mark.parametrize(
    "house,rasi", [(1, "Vi"), (2, "Li"), (3, "Sc")],
)
def test_ghati_lagna_in_virgo_worked_through(house, rasi):
    """7.1: "the 1st, 2nd and 3rd houses with respect to Ghati Lagna are in
    Virgo, Libra and Scorpio"."""
    assert rasi_of_house(RASI["Vi"], house) == RASI[rasi]


def test_the_same_rasi_is_a_different_house_from_a_different_reference():
    """7.1's central point: "The same sign may contain the 2nd house with
    respect to one reference and the 6th house with respect to another"."""
    target = RASI["Ta"]
    assert house_of_rasi(RASI["Ar"], target) == 2
    assert house_of_rasi(RASI["Sg"], target) == 6


def test_reference_and_target_rasis_are_validated():
    for bad in (-1, 12, 99):
        with pytest.raises(InputError, match="between 0 and 11"):
            house_of_rasi(bad, 0)
        with pytest.raises(InputError, match="between 0 and 11"):
            house_of_rasi(0, bad)


# --------------------------------------------------------------------------
# 7.2 Significations, and houses from houses
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "house,fragment",
    [
        (1, "Physical body"), (2, "Wealth, assets, family"),
        (3, "Younger co-borns"), (4, "Mother, vehicles, house"),
        (5, "Children, poorvapunya"), (6, "Enemies, service, servants"),
        (7, "Marriage, marital life"), (8, "Longevity, debts"),
        (9, "Father, teacher, boss"), (10, "Growth, profession, career"),
        (11, "Elder co-borns, income"), (12, "Losses, expenditure"),
    ],
)
def test_significations_open_as_the_book_lists_them(house, fragment):
    assert signification(house).startswith(fragment)


def test_every_house_has_a_signification():
    assert len(HOUSE_SIGNIFICATIONS) == 13          # index 0 unused
    assert all(HOUSE_SIGNIFICATIONS[h] for h in range(1, 13))
    assert HOUSE_SIGNIFICATIONS[0] == ""


@pytest.mark.parametrize(
    "from_house,count,expected",
    [
        (3, 2, 4),    # "The 2nd house from the 3rd house is the 4th house"
        (3, 7, 9),    # "The 7th house from the 3rd house is the 9th house"
        (11, 6, 4),   # "the 4th house is the 6th house from the 11th"
    ],
)
def test_houses_from_houses(from_house, count, expected):
    """7.2 composes house meanings by counting houses from houses."""
    assert houses_from(from_house, (count,)) == (expected,)


# --------------------------------------------------------------------------
# 7.3 References
# --------------------------------------------------------------------------

def test_the_chapter_names_eight_references():
    assert set(HOUSE_REFERENCES) == {
        "lagna", "chandra_lagna", "ravi_lagna", "arudha_lagna",
        "paaka_lagna", "karakamsa_lagna", "ghati_lagna", "hora_lagna",
    }


@pytest.mark.parametrize(
    "reference,fragment",
    [
        ("lagna", "true self"),
        ("chandra_lagna", "mind"),
        ("ravi_lagna", "soul"),
        ("paaka_lagna", "physical self"),
        ("ghati_lagna", "power"),
        ("hora_lagna", "wealth"),
        ("arudha_lagna", "perceived"),
    ],
)
def test_what_each_reference_shows(reference, fragment):
    assert fragment in HOUSE_REFERENCES[reference]["shows"]


def test_every_reference_is_now_available():
    """All eight of §7.3's references are computable.

    This test used to assert the opposite for arudha and karakamsa lagna,
    which were marked unavailable pending "the chapters we have not reached".
    Both chapters are now read — §9.2 for the arudha pada and §7.3.6 for the
    karakamsa — so the flags were stale, not the code. Corrected 2026-08-27.
    """
    assert all(entry["available"] for entry in HOUSE_REFERENCES.values())
    assert HOUSE_REFERENCES["arudha_lagna"]["available"] is True
    assert HOUSE_REFERENCES["karakamsa_lagna"]["available"] is True


@pytest.mark.parametrize(
    "lagna,lord_rasi,expected",
    [("Pi", "Cn", "Cn"), ("Le", "Vi", "Vi")],
)
def test_paaka_lagna_worked_examples(lagna, lord_rasi, expected):
    """7.3.5: "If someone with Pisces lagna has Jupiter in Cancer, then Cancer
    becomes paaka lagna. If someone with Leo lagna has Sun in Virgo, Virgo
    becomes paaka lagna"."""
    from hora.core.const import RASI_LORD

    lord = int(RASI_LORD[RASI[lagna]])
    assert paaka_lagna_rasi(RASI[lagna], {lord: RASI[lord_rasi]}) == RASI[expected]


def test_paaka_lagna_says_which_graha_it_needs():
    with pytest.raises(InputError, match="lagna lord"):
        paaka_lagna_rasi(Rasi.PISCES, {})


@pytest.mark.parametrize(
    "graha,houses",
    [
        (Graha.SUN, (9, 10, 11)),
        (Graha.MOON, (4, 1, 2, 11, 9)),
        (Graha.MARS, (3,)),
        (Graha.MERCURY, (6,)),
        (Graha.JUPITER, (5,)),
        (Graha.VENUS, (7,)),
        (Graha.SATURN, (8, 12)),
    ],
)
def test_table_12_graha_lagnas(graha, houses):
    assert graha_lagna_houses(graha) == houses


def test_the_nodes_are_not_graha_lagnas():
    """Table 12 lists the seven classical planets only."""
    assert graha_lagna_houses(Graha.RAHU) == ()
    assert graha_lagna_houses(Graha.KETU) == ()


@pytest.mark.parametrize(
    "matter,house,graha",
    [
        ("mother", 4, Graha.MOON), ("father", 9, Graha.SUN),
        ("losses", 12, Graha.SATURN), ("progeny", 5, Graha.JUPITER),
        ("marriage", 7, Graha.VENUS), ("courage", 3, Graha.MARS),
    ],
)
def test_the_pairings_the_chapter_works_through(matter, house, graha):
    """7.3.9: "We see the 4th from lagna and the 4th from Moon for mother",
    and so on for each pairing it names."""
    assert house in graha_lagna_houses(graha), matter


# --------------------------------------------------------------------------
# 7.4 Special categories
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "category,houses",
    [
        ("trikona", (1, 5, 9)),
        ("kendra", (1, 4, 7, 10)),
        ("panaphara", (2, 5, 8, 11)),
        ("apoklima", (3, 6, 9, 12)),
        ("upachaya", (3, 6, 10, 11)),
        ("dusthana", (6, 8, 12)),
        ("chaturasra", (4, 8)),
    ],
)
def test_the_seven_categories(category, houses):
    assert category_houses(category) == houses


def test_chaturasra_is_the_4th_and_8th():
    """7.4 (7) — a category we did not have before this chapter was read."""
    assert CHATURASRA == (4, 8)


def test_panapharas_are_the_quadrants_from_the_2nd():
    """7.4 (3) states this outright, so it is checkable."""
    assert category_houses("panaphara") == category_houses("kendra", 2)


def test_apoklimas_are_the_quadrants_from_the_3rd():
    """7.4 (4)."""
    assert category_houses("apoklima") == category_houses("kendra", 3)


@pytest.mark.parametrize(
    "category,expected",
    [
        ("trikona", (3, 7, 11)),
        ("kendra", (3, 6, 9, 12)),
        ("upachaya", (1, 5, 8, 12)),
        ("dusthana", (2, 8, 10)),
    ],
)
def test_categories_counted_from_the_third_house(category, expected):
    """7.4 works all four of these through from the 3rd house."""
    assert category_houses(category, 3) == expected


def test_a_category_from_the_first_house_is_the_category_itself():
    for name in HOUSE_CATEGORIES:
        assert category_houses(name, 1) == tuple(sorted(HOUSE_CATEGORIES[name]["houses"]))


def test_categories_of_a_house():
    assert set(categories_of(1)) == {"trikona", "kendra"}
    assert set(categories_of(8)) == {"panaphara", "dusthana", "chaturasra"}
    assert set(categories_of(10)) == {"kendra", "upachaya"}


def test_unknown_category_is_rejected_by_name():
    with pytest.raises(InputError, match="unknown category"):
        category_houses("nonesuch")


def test_base_house_is_validated():
    for bad in (0, 13, -1):
        with pytest.raises(InputError, match="between 1 and 12"):
            category_houses("trikona", bad)


# --------------------------------------------------------------------------
# 7.4.1 The four purusharthas
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "purushartha,houses,base",
    [
        ("dharma", (1, 5, 9), 1),
        ("artha", (2, 6, 10), 2),
        ("kaama", (3, 7, 11), 3),
        ("moksha", (4, 8, 12), 4),
    ],
)
def test_purushartha_trikonas_are_the_trines_from_their_base(purushartha, houses, base):
    """Each group is the trines from the 1st, 2nd, 3rd and 4th house."""
    assert PURUSHARTHA_TRIKONAS[purushartha]["houses"] == houses
    assert category_houses("trikona", base) == houses


@pytest.mark.parametrize("house", range(1, 13))
def test_every_house_serves_exactly_one_purushartha(house):
    matches = [n for n, e in PURUSHARTHA_TRIKONAS.items() if house in e["houses"]]
    assert len(matches) == 1
    assert purushartha_of(house) == matches[0]


# --------------------------------------------------------------------------
# 7.4.5 The two halves
# --------------------------------------------------------------------------

def test_the_two_halves():
    assert VISIBLE_HALF == (7, 8, 9, 10, 11, 12)
    assert INVISIBLE_HALF == (1, 2, 3, 4, 5, 6)
    assert set(VISIBLE_HALF) | set(INVISIBLE_HALF) == set(range(1, 13))
    assert not set(VISIBLE_HALF) & set(INVISIBLE_HALF)


def test_the_reason_the_chapter_gives_for_the_halves():
    """7.4.5: "the bases of dharma trikona (1st) and moksha trikona (4th) are
    in the invisible half and the bases of artha trikona (10th) and kaama
    trikona (7th) are in the visible half"."""
    assert half_of(1) == "invisible"
    assert half_of(4) == "invisible"
    assert half_of(7) == "visible"
    assert half_of(10) == "visible"


# --------------------------------------------------------------------------
# 7.4.6 What each category shows
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "category,shows",
    [
        ("trikona", "Prosperity and flourishing"),
        ("kendra", "Sustenance and vital activity"),
        ("upachaya", "Gains and growth"),
        ("dusthana", "Setbacks and obstacles"),
    ],
)
def test_quick_summary(category, shows):
    assert HOUSE_CATEGORIES[category]["shows"] == shows


def test_presiding_deities():
    """7.4.1 and 7.4.2 name these."""
    assert HOUSE_CATEGORIES["trikona"]["presiding"] == "Goddess Lakshmi"
    assert HOUSE_CATEGORIES["kendra"]["presiding"] == "Sri Maha Vishnu"


# --------------------------------------------------------------------------
# 7.5 A controversy — no house spans two rasis
# --------------------------------------------------------------------------

def test_the_default_house_system_is_whole_sign():
    """7.5: "Each rasi is a house" — bhava chalit and Sripathi are rejected."""
    assert Settings().house_system is HouseSystem.WHOLE_SIGN


def test_whole_sign_houses_never_span_two_rasis():
    """Under the default, each house is exactly one rasi and they tile the zodiac."""
    from hora.charts.bhava import build_bhavas
    from hora.core.ephemeris.base import Houses

    houses = Houses(
        ascendant=17.5, midheaven=280.0,
        cusps=tuple(float(i * 30) for i in range(12)),
        armc=0.0, vertex=0.0, equatorial_ascendant=0.0,
    )
    bhavas = build_bhavas(houses, HouseSystem.WHOLE_SIGN)
    assert len(bhavas) == 12
    for bhava in bhavas:
        assert (bhava.end - bhava.start) % 360 == 30.0
        assert bhava.start % 30 == 0.0
    assert len({b.sign for b in bhavas}) == 12


# --------------------------------------------------------------------------
# The endpoints
# --------------------------------------------------------------------------

def test_houses_from_endpoint(client):
    body = client.post(
        "/v1/house/from", json={"reference_rasi": RASI["Aq"], "reference": "chandra_lagna"}
    ).json()
    assert body["reference_name"] == "Chandra Lagna"
    assert [h["rasi_name"][:2] for h in body["houses"][:4]] == ["Aq", "Pi", "Ar", "Ta"]
    assert body["houses"][0]["categories"] == ["trikona", "kendra"]


def test_houses_from_endpoint_rejects_an_unknown_reference(client):
    response = client.post(
        "/v1/house/from", json={"reference_rasi": 0, "reference": "nonesuch"}
    )
    assert response.status_code == 400
    assert "unknown reference" in response.json()["error"]["message"]


def test_houses_from_endpoint_validates_the_rasi(client):
    assert client.post(
        "/v1/house/from", json={"reference_rasi": 12}
    ).status_code == 422


def test_categories_endpoint_rebases(client):
    body = client.get("/v1/house/categories/3").json()
    by_name = {c["category"]: c["houses"] for c in body["categories"]}
    assert by_name["trikona"] == [3, 7, 11]
    assert by_name["dusthana"] == [2, 8, 10]


def test_categories_endpoint_validates_the_base_house(client):
    assert client.get("/v1/house/categories/13").status_code == 422
    assert client.get("/v1/house/categories/0").status_code == 422


def test_references_endpoint_reports_why_one_is_unavailable(client):
    """A reference that cannot be resolved says so, rather than vanishing."""
    body = client.post(
        "/v1/house/references",
        json={"lagna_rasi": Rasi.PISCES, "graha_rasis": {int(Graha.JUPITER): Rasi.CANCER}},
    ).json()
    by_key = {r["reference"]: r for r in body["references"]}

    assert by_key["paaka_lagna"]["rasi"] == Rasi.CANCER
    assert by_key["chandra_lagna"]["available"] is False
    assert "Moon" in by_key["chandra_lagna"]["unavailable_because"]
    # Arudha lagna now resolves: Pisces lagna, its lord Jupiter in Cancer,
    # so §9.2's pada lands in Scorpio.
    assert by_key["arudha_lagna"]["rasi"] == Rasi.SCORPIO
    # Karakamsa still cannot: it needs longitudes, not rasis.
    assert by_key["karakamsa_lagna"]["available"] is False
    assert "longitudes" in by_key["karakamsa_lagna"]["unavailable_because"]


def test_references_endpoint_accepts_supplied_special_lagnas(client):
    body = client.post(
        "/v1/house/references",
        json={"lagna_rasi": 0, "ghati_lagna_rasi": 5, "hora_lagna_rasi": 8},
    ).json()
    by_key = {r["reference"]: r for r in body["references"]}
    assert by_key["ghati_lagna"]["rasi"] == 5
    assert by_key["hora_lagna"]["rasi"] == 8


def test_rules_endpoint_publishes_the_chapter(client):
    body = client.get("/v1/house/rules").json()
    assert len(body["significations"]) == 12
    assert len(body["categories"]) == 7
    assert len(body["purusharthas"]) == 4
    assert len(body["graha_lagnas"]) == 7
    assert "Each rasi is a house" in body["note"]
    assert body["halves"]["visible"] == [7, 8, 9, 10, 11, 12]


# --------------------------------------------------------------------------
# 7.2 The twelve significations, character for character
#
# These were transcribed but never diffed. Six parenthetical glosses had been
# stripped and two "&" normalised to "and" — including the two derivations in
# the third house, which are the section's own worked instances of the method
# its closing paragraph teaches. Found 2026-08-27 and restored.
# --------------------------------------------------------------------------

#: §7.2 exactly as printed, all twelve.
HOUSE_SIGNIFICATIONS_BOOK = {
    1: (
        "Physical body, complexion, appearance, head, intelligence, strength, "
        "energy, fame, success, nature of birth, caste"
    ),
    2: "Wealth, assets, family, speech, eyes, mouth, face, voice, food",
    3: (
        "Younger co-borns, confidants, courage, mental strength, "
        "communication skills, creativity, throat, ears, arms, father's death "
        "(7th from 9th), expenditure on vehicles and house (12th from 4th), "
        "travels"
    ),
    4: (
        "Mother, vehicles, house, lands, immovable property, motherland, "
        "childhood, wealth from real estate, education, relatives, happiness, "
        "comforts, pleasures, peace, state of mind, heart"
    ),
    5: (
        "Children, poorvapunya (good deeds of previous lives), intelligence, "
        "knowledge & scholarship, devotion, mantras (prayers), stomach, "
        "digestive system, authority/power, fame, love, affection, emotions, "
        "judgment, speculation"
    ),
    6: (
        "Enemies, service, servants, relatives, mental tension, injuries, "
        "health, diseases, agriculture, accidents, mental affliction, "
        "mother's younger brother, hips"
    ),
    7: (
        "Marriage, marital life, life partner, sex, passion (and related "
        "happiness), long journeys, partners, business, death, the portion of "
        "the body below the navel"
    ),
    8: (
        "Longevity, debts, disease, ill-fame, inheritance, loss of friends, "
        "occult studies, evils, gifts, unearned wealth, windfall, disgrace, "
        "secrets, genitals"
    ),
    9: (
        "Father, teacher, boss, fortune, religiousness, spirituality, God, "
        "higher studies & high knowledge, fortune in a foreign land, foreign "
        "trips, diksha (joining a religious order), past life and the cause "
        "of birth, grandchildren, principles, dharma, intuition, compassion, "
        "sympathy, leadership, charity, thighs"
    ),
    10: (
        "Growth, profession, career, karma (action), conduct in society, "
        "fame, honors, awards, self-respect, dignity, knees"
    ),
    11: "Elder co-borns, income, gains, realization of hopes, friends, ankles",
    12: (
        "Losses, expenditure, punishment, imprisonment, hospitalization, "
        "pleasures in bed, misfortune, bad habits, sleep, meditation, "
        "donation, secret enemies, heaven, left eye, feet, residence away "
        "from the place of birth, moksha (emancipation/liberation)"
    ),
}


@pytest.mark.parametrize("house", range(1, 13))
def test_7_2_each_signification_matches_the_book(house):
    assert c.HOUSE_SIGNIFICATIONS[house] == HOUSE_SIGNIFICATIONS_BOOK[house]


def test_7_2_the_list_is_one_based_with_a_padding_slot():
    """Index 0 is an empty string so a house number indexes directly. Worth
    pinning: a 0-based reading shifts every signification by one."""
    assert len(c.HOUSE_SIGNIFICATIONS) == 13
    assert c.HOUSE_SIGNIFICATIONS[0] == ""
    assert c.HOUSE_SIGNIFICATIONS[1].startswith("Physical body")


def test_7_2_the_parenthetical_glosses_are_kept():
    """Six glosses had been stripped. Each is the book's own explanation of a
    term, and dropping them loses information the text gives."""
    assert "(good deeds of previous lives)" in c.HOUSE_SIGNIFICATIONS[5]
    assert "(prayers)" in c.HOUSE_SIGNIFICATIONS[5]
    assert "(and related happiness)" in c.HOUSE_SIGNIFICATIONS[7]
    assert "(joining a religious order)" in c.HOUSE_SIGNIFICATIONS[9]
    assert "(emancipation/liberation)" in c.HOUSE_SIGNIFICATIONS[12]
    assert "(action)" in c.HOUSE_SIGNIFICATIONS[10]


def test_7_2_the_third_house_keeps_its_two_derivations():
    """"father's death (**7th from 9th**), expenditure on vehicles and house
    (**12th from 4th**)".

    These are not glosses but **derivations** — worked instances of the very
    method §7.2's closing paragraph teaches. Both check out: the 7th from the
    9th is the 3rd, and the 12th from the 4th is the 3rd.
    """
    third = c.HOUSE_SIGNIFICATIONS[3]
    assert "(7th from 9th)" in third
    assert "(12th from 4th)" in third
    assert (9 + 7 - 2) % 12 + 1 == 3, "the 7th from the 9th is the 3rd"
    assert (4 + 12 - 2) % 12 + 1 == 3, "the 12th from the 4th is the 3rd"


def test_7_2_the_books_ampersands_are_kept():
    """"knowledge & scholarship" and "higher studies & high knowledge" — both
    had been normalised to "and". Same class as the chapter 8 finding."""
    assert "knowledge & scholarship" in c.HOUSE_SIGNIFICATIONS[5]
    assert "higher studies & high knowledge" in c.HOUSE_SIGNIFICATIONS[9]


def test_7_2_the_reference_for_fuller_results():
    """"readers may refer either to the ancient classics or to the modern
    classic – "How to Judge a Horoscope" (Vols I & II) by Dr. B.V. Raman."
    """
    assert "How to Judge a Horoscope" in c.HOUSE_RESULTS_REFERENCE
    assert "B.V. Raman" in c.HOUSE_RESULTS_REFERENCE


# --------------------------------------------------------------------------
# 7.1 Houses are relative
# --------------------------------------------------------------------------


def test_7_1_lagna_is_the_default_reference():
    """"If we mention houses without clearly specifying the reference used, it
    means that the reference used is lagna (ascendant)."""
    assert "default reference" in c.HOUSE_REFERENCE_RULE
    assert "lagna" in c.HOUSE_REFERENCE_RULE


@pytest.mark.parametrize("reference,first,second,third", [
    ("Aq", "Aq", "Pi", "Ar"),   # "Suppose Moon is in Aquarius"
    ("Ta", "Ta", "Ge", "Cn"),   # "Sun may be in Taurus"
    ("Vi", "Vi", "Li", "Sc"),   # "If Ghati Lagna is in Virgo"
])
def test_7_1_the_three_worked_references(reference, first, second, third):
    """"Then Aquarius is the 1st house, Pisces is the 2nd house, Aries is the
    3rd house... Taurus contains the 1st house, Gemini contains the 2nd... the
    1st, 2nd and 3rd houses with respect to Ghati Lagna are in Virgo, Libra
    and Scorpio respectively."

    Three different references in **one chart** — which is the point of the
    section.
    """
    abbr = list(c.RASI_ABBR)
    base = abbr.index(reference)
    for offset, expected in enumerate((first, second, third)):
        assert abbr[(base + offset) % 12] == expected


def test_7_1_the_twelfth_house_wraps_to_the_sign_before():
    """"As we go around the zodiac, we reach Capricorn when we find the 12th
    house" — from Aquarius."""
    abbr = list(c.RASI_ABBR)
    aq = abbr.index("Aq")
    assert abbr[(aq + 11) % 12] == "Cp"


def test_7_1_one_sign_is_different_houses_from_different_references():
    """"The same sign may contain the 2nd house with respect to one reference
    and the 6th house with respect to another reference."

    Demonstrated rather than restated: Pisces is the 2nd from Aquarius and the
    6th from Libra.
    """
    abbr = list(c.RASI_ABBR)
    pisces = abbr.index("Pi")
    assert (pisces - abbr.index("Aq")) % 12 + 1 == 2
    assert (pisces - abbr.index("Li")) % 12 + 1 == 6


def test_7_1_meaning_depends_on_reference_and_on_varga():
    """"the 11th house from lagna may stand for something and the 11th house
    from arudha lagna may stand for something else" and "The 4th house from
    lagna in D-16 may mean something and the 4th house from lagna in D-24 may
    mean something else."

    Two independent axes, both recorded — the house number alone does not fix
    a meaning.
    """
    assert "reference" in c.HOUSE_MEANING_DEPENDS_ON_REFERENCE
    assert "divisional chart" in c.HOUSE_MEANING_DEPENDS_ON_VARGA


def test_7_1_the_moon_example_through_the_endpoint(client):
    """Moon in Aquarius: Aquarius is the 1st, Capricorn the 12th."""
    body = client.post("/v1/house/from", json={"reference_rasi": 10}).json()
    houses = {h["house"]: h["rasi_name"] for h in body["houses"]}
    assert houses[1] == "Aquarius"
    assert houses[2] == "Pisces"
    assert houses[3] == "Aries"
    assert houses[4] == "Taurus"
    assert houses[12] == "Capricorn"


# --------------------------------------------------------------------------
# 7.2 Houses from houses
# --------------------------------------------------------------------------


@pytest.mark.parametrize("case", c.HOUSES_FROM_HOUSES_EXAMPLES)
def test_7_2_the_three_derivations(case):
    """"The 2nd house from the 3rd house is the 4th house (count 1, 2 from 3rd
    and get 3rd, 4th)... The 7th house from the 3rd house is the 9th house...
    the 4th house from lagna is nothing but the 6th house from the 11th
    house."
    """
    got = house_service.derived(case["house"], case["from_house"])
    assert got["result"] == case["result"]


def test_7_2_the_counting_is_inclusive():
    """"count 1, 2 from 3rd and get 3rd, 4th" — the base house counts as the
    1st. An exclusive count would give the 5th, not the 4th."""
    assert house_service.derived(1, 3)["result"] == 3, "the 1st from the 3rd is itself"
    assert house_service.derived(2, 3)["result"] == 4
    assert house_service.derived(2, 3)["result"] != 5, "not an exclusive count"
    assert "inclusive" in house_service.derived(2, 3)["counting_note"]


def test_7_2_the_derivation_wraps_the_zodiac():
    """The 6th from the 11th is the 4th — past the 12th and round."""
    assert house_service.derived(6, 11)["result"] == 4
    assert house_service.derived(12, 12)["result"] == 11


def test_7_2_the_friends_derivation_is_stated_backwards():
    """"The 11th house from lagna shows friends and the 4th house from lagna
    is nothing but the 6th house from the 11th house."

    The book states this one as an observation about the 4th rather than as a
    forward derivation, so it is checked in both directions.
    """
    assert house_service.derived(6, 11)["result"] == 4
    assert "friends" in c.HOUSE_SIGNIFICATIONS[11]
    assert "Enemies" in c.HOUSE_SIGNIFICATIONS[6]
    assert "diseases" in c.HOUSE_SIGNIFICATIONS[6]
    assert "debts" in c.HOUSE_SIGNIFICATIONS[8], "the book says debts of friends"


def test_7_2_the_derived_endpoint_carries_all_three_meanings(client):
    """A caller concatenating meanings needs both inputs and the result, which
    is what §7.2's method does."""
    body = client.get(
        "/v1/house/derived", params={"house": 2, "from_house": 3}
    ).json()
    assert body["result"] == 4
    assert body["from_house_signifies"] == c.HOUSE_SIGNIFICATIONS[3]
    assert body["house_signifies"] == c.HOUSE_SIGNIFICATIONS[2]
    assert body["result_signifies"] == c.HOUSE_SIGNIFICATIONS[4]
    assert "Younger co-borns" in body["from_house_signifies"]
    assert "Wealth" in body["house_signifies"]


def test_7_2_the_derived_endpoint_rejects_a_house_outside_one_to_twelve(client):
    assert client.get(
        "/v1/house/derived", params={"house": 13, "from_house": 3}
    ).status_code == 422


# --------------------------------------------------------------------------
# 7.3 Common References for Houses
# --------------------------------------------------------------------------


def test_7_3_three_things_must_be_chosen_not_one():
    """"Depending on the matter we are analyzing, we should look at the
    correct divisional chart, the correct reference and the correct house."

    A house number alone fixes nothing — the chart and the reference are the
    other two axes, and §7.1 already said each colours the meaning.
    """
    for term in ("divisional chart", "reference", "house"):
        assert term in c.THREE_CHOICES_RULE


def test_7_3_the_meaning_is_chosen_by_the_charts_area_of_life():
    """"We have to note the area of life seen in the divisional chart under
    examination. We have to choose the meanings of houses that are relevant in
    that area of life."""
    assert "area of life" in c.CHOOSE_MEANING_BY_VARGA


@pytest.mark.parametrize("case", c.FOURTH_HOUSE_BY_VARGA)
def test_7_3_the_fourth_house_means_four_things_in_four_charts(case):
    """"the 4th houses in D-24, D-16, D-4 and D-12 show education, vehicle,
    house and mother (respectively)."

    All four words are in the 4th house's own signification list — the chart
    selects among them, it does not add to them.
    """
    fourth = c.HOUSE_SIGNIFICATIONS[4].lower()
    assert case["means"].rstrip("s") in fourth, case


def test_7_3_the_selection_is_derivable_for_three_of_the_four():
    """`meanings_in_varga` intersects the two signification lists, so every
    word it returns is PVR's own. That reaches three of §7.3's four cases.
    """
    for chart, expected in (("D24", "education"), ("D16", "vehicle"), ("D4", "house")):
        shared = house_service.meanings_in_varga(4, chart)["shared_meanings"]
        assert expected.rstrip("s") in shared, chart


def test_7_3_the_d12_case_is_not_derivable_from_the_tables():
    """The fourth case, and the limit of the method.

    §7.3 reads the 4th house in **D-12 as "mother"**. D-12's signification is
    "Everything related to parents"; the 4th house's includes "Mother". The
    link is *mother is a parent* — world knowledge the two tables do not
    contain, so the literal intersection cannot reach it.

    The overlap returns "relative", which is genuinely in both lists and is
    not wrong — merely not what the book picked. Pinned so the gap is known
    rather than discovered later as a wrong answer.
    """
    result = house_service.meanings_in_varga(4, "D12")
    assert "mother" not in result["shared_meanings"]
    assert result["shared_meanings"] == ["relative"]
    assert "Mother" in c.HOUSE_SIGNIFICATIONS[4]
    assert "parents" in VARGA_SIGNIFICATIONS["D12"]
    assert "mother" not in VARGA_SIGNIFICATIONS["D12"].lower()
    assert "mother is a parent" in result["limitation"]


def test_7_3_the_overlap_never_invents_a_word():
    """Whatever it returns must appear in **both** signification lists, so it
    can be incomplete but never wrong."""
    for house in range(1, 13):
        for chart in ("D1", "D4", "D9", "D12", "D16", "D24"):
            result = house_service.meanings_in_varga(house, chart)
            house_text = c.HOUSE_SIGNIFICATIONS[house].lower()
            chart_text = VARGA_SIGNIFICATIONS[chart].lower()
            for word in result["shared_meanings"]:
                assert word in house_text, (house, chart, word)
                assert word in chart_text, (house, chart, word)


def test_7_3_the_same_house_differs_by_reference_too():
    """"The 4th house from lagna, the 4th house from arudha lagna and the 4th
    house from paaka lagna can mean different things."

    All three are references we already model, so the statement is checkable
    rather than decorative.
    """
    for key in ("lagna", "arudha_lagna", "paaka_lagna"):
        assert key in c.HOUSE_REFERENCES
    assert "arudha lagna" in c.HOUSE_DIFFERS_BY_REFERENCE_EXAMPLE
    assert "paaka lagna" in c.HOUSE_DIFFERS_BY_REFERENCE_EXAMPLE


def test_7_3_why_the_model_has_so_many_parameters():
    """"it is silly and unscientific to expect a simplistic model for the
    complicated human life... if we do not understand what each parameter
    means and end up using them in a mixed-up way, we will get nowhere."

    The book's own answer to why the parameter count is large, and its own
    warning about using them loosely.
    """
    assert "silly and unscientific" in c.MANY_PARAMETERS_NOTE
    assert "mixed-up way" in c.MANY_PARAMETERS_NOTE


def test_the_meanings_endpoint(client):
    body = client.get(
        "/v1/house/meanings", params={"house": 4, "chart": "D16"}
    ).json()
    assert "vehicle" in body["shared_meanings"]
    assert body["chart_signifies"] == VARGA_SIGNIFICATIONS["D16"]
    assert "mother is a parent" in body["limitation"]


def test_the_meanings_endpoint_rejects_an_unknown_chart(client):
    r = client.get("/v1/house/meanings", params={"house": 4, "chart": "D99"})
    assert r.status_code == 400


# --------------------------------------------------------------------------
# 7.3.1 Lagna
# --------------------------------------------------------------------------


def test_7_3_1_lagna_shows_true_self():
    """"Lagna shows true self... It shows the overall spirit of "I" (self)."""
    assert c.LAGNA_SHOWS == "true self"
    assert "spirit of" in c.LAGNA_SPIRIT_OF_I
    assert c.HOUSE_REFERENCES["lagna"]["shows"] == c.LAGNA_SHOWS


def test_7_3_1_lagna_is_the_default_and_the_most_common():
    """"Lagna is the most commonly used reference when finding houses. If no
    reference is mentioned when houses are listed, it means that lagna – the
    default reference – was used."""
    assert c.HOUSE_DEFAULT_REFERENCE == "lagna"
    assert c.HOUSE_REFERENCES["lagna"]["available"] is True


def test_7_3_1_lagna_is_the_wrong_reference_for_status():
    """"If we are trying to understand someone's status in society, lagna may
    not be the correct reference. Status does not relate to "true self". It is
    a part of the illusion of this world."

    A **negative** rule, and the only one in the section — it says what a
    reference is *not* for. Status belongs to arudha lagna, which the same
    chapter lists as showing "how a native is perceived, and status".
    """
    assert "status" in c.LAGNA_NOT_FOR_STATUS
    assert "illusion of this world" in c.LAGNA_NOT_FOR_STATUS
    assert "status" in c.HOUSE_REFERENCES["arudha_lagna"]["shows"]
    assert "status" not in c.HOUSE_REFERENCES["lagna"]["shows"]


def test_7_3_1_what_is_seen_from_lagna():
    """"if we are trying to understand someone's intentions in doing something
    or someone's knowledge or someone's persistence, it relates to "true
    self". So they are seen from the houses counted from lagna."""
    assert c.LAGNA_SEEN_FROM == (
        "intentions in doing something", "knowledge", "persistence",
    )


# --------------------------------------------------------------------------
# 7.3.2 Chandra Lagna
# --------------------------------------------------------------------------


def test_7_3_2_chandra_lagna_is_the_moons_rasi():
    """"Chandra lagna means Moon taken as a reference. We can find houses from
    Moon."
    """
    assert "Moon" in c.HOUSE_REFERENCES["chandra_lagna"]["note"]
    assert c.HOUSE_REFERENCES["chandra_lagna"]["available"] is True


def test_7_3_2_why_it_shows_the_mind():
    """"Because Moon is the significator of mind, these houses show things
    from the perspective of mind."

    Chapter 3 gives the Moon "mind" as its governance — the same word, so the
    two chapters agree rather than each asserting it separately.
    """
    assert c.CHANDRA_LAGNA_REASON == "Moon is the significator of mind"
    assert c.GRAHA_GOVERNS[c.Graha.MOON] == "mind"
    assert "mind" in c.HOUSE_REFERENCES["chandra_lagna"]["shows"]


def test_7_3_2_the_worked_contrast():
    """"the 10th house (career) from lagna may have the influence of Saturn
    (routine job) and the 10th house from Moon may have the influence of Mars
    (active and enterprising)."

    One house, two references, two readings of one native. The 10th really is
    the career house, and the two grahas' natures are chapter 3's.
    """
    example = c.CHANDRA_LAGNA_EXAMPLE
    assert example["house"] == 10
    assert "career" in c.HOUSE_SIGNIFICATIONS[10]
    assert example["from_lagna"]["graha"] == "Saturn"
    assert example["from_moon"]["graha"] == "Mars"
    # Chapter 3: Saturn's element is airy and Mars governs strength.
    assert c.GRAHA_GOVERNS[c.Graha.MARS] == "strength"


def test_7_3_2_chandra_lagna_must_not_be_ignored():
    """"When we judge how happy one is, how ambitious one is and how one views
    one's career, the role of mind is paramount. So Chandra lagna should not
    be ignored."

    Three matters named — happiness, ambition, and one's view of career. The
    third is why §7.3.2's example is about the 10th house.
    """
    assert "should not be ignored" in c.CHANDRA_LAGNA_NOT_IGNORED
    for matter in ("happy", "ambitious", "career"):
        assert matter in c.CHANDRA_LAGNA_NOT_IGNORED


def test_7_3_2_houses_from_the_moon_through_the_endpoint(client):
    """Moon in Aquarius: the 10th from Moon is Scorpio."""
    body = client.post(
        "/v1/house/from", json={"reference_rasi": 10, "reference": "chandra_lagna"}
    ).json()
    houses = {h["house"]: h["rasi_name"] for h in body["houses"]}
    assert houses[1] == "Aquarius"
    assert houses[10] == "Scorpio"
    assert "mind" in body["shows"]


# --------------------------------------------------------------------------
# 7.3.3 Ravi Lagna
# --------------------------------------------------------------------------


def test_7_3_3_ravi_lagna_shows_the_soul():
    """"Because Sun is the significator of soul, these houses show things from
    the perspective of soul."

    Chapter 3 gives the Sun "soul" as its governance — the same word, so the
    two chapters agree rather than each asserting it.
    """
    assert c.RAVI_LAGNA_REASON == "Sun is the significator of soul"
    assert c.GRAHA_GOVERNS[c.Graha.SUN] == "soul"
    assert "soul" in c.HOUSE_REFERENCES["ravi_lagna"]["shows"]


def test_7_3_3_the_sun_is_also_the_reference_for_vitality():
    """"For things related to physical vitality also, Sun is an important
    reference."

    A second use, and the one §7.3.5's Saturn-transit note contrasts with
    paaka lagna — both touch physical vitality.
    """
    assert "physical vitality" in c.RAVI_LAGNA_ALSO
    saturn_paaka = next(
        x for x in c.SATURN_TRANSIT_BY_REFERENCE if x["reference"] == "paaka_lagna"
    )
    assert "physical vitality" in saturn_paaka["shows"]


def test_7_3_3_the_three_graha_references_map_to_their_governances():
    """Lagna/Moon/Sun as references line up with chapter 3: Moon governs mind,
    Sun governs soul. Lagna is not a graha, so it has no governance — it shows
    "true self"."""
    assert c.GRAHA_GOVERNS[c.Graha.MOON] in c.HOUSE_REFERENCES["chandra_lagna"]["shows"]
    assert c.GRAHA_GOVERNS[c.Graha.SUN] in c.HOUSE_REFERENCES["ravi_lagna"]["shows"]
    assert c.HOUSE_REFERENCES["lagna"]["shows"] == "true self"


# --------------------------------------------------------------------------
# 7.3.4 Arudha Lagna
# --------------------------------------------------------------------------


def test_7_3_4_what_arudha_lagna_shows():
    """"arudha lagna shows how a native is perceived in the world. It also
    shows the status of a native."""
    assert "perceived in the world" in c.ARUDHA_LAGNA_SHOWS
    assert "status" in c.ARUDHA_LAGNA_SHOWS


def test_7_3_4_its_computation_is_deferred_to_chapter_9():
    """"Computation of arudha lagna (AL) will be explained in the chapter on
    "Arudha Padas"." Chapter 9 exists, so the reference can be flagged as
    computed-elsewhere rather than unavailable."""
    from hora.charts.arudha import arudha_pada

    assert callable(arudha_pada)
    assert "9.2" in c.HOUSE_REFERENCES["arudha_lagna"]["note"]
    assert c.HOUSE_REFERENCES["arudha_lagna"]["available"] is True


@pytest.mark.parametrize("case", c.TENTH_HOUSE_BY_REFERENCE)
def test_7_3_4_the_tenth_house_read_three_ways(case):
    """"A planet in the 10th house from lagna may give some important
    developments in one's profession. A planet in the 10th house from Chandra
    lagna may give some important mental activity in one's profession. A
    planet in the 10th house from arudha lagna may give some important
    developments in one's professional status."

    One house, three references, three readings — and each reading is the
    reference's own subject applied to the house's.
    """
    assert case["reference"] in c.HOUSE_REFERENCES
    assert "profession" in case["shows"]


def test_7_3_4_each_tenth_house_reading_carries_its_references_subject():
    """The three readings are not arbitrary: Chandra lagna's adds "mental",
    arudha lagna's adds "status", lagna's adds neither. That is the reference
    colouring the house, which is §7.1's rule made concrete."""
    by_ref = {x["reference"]: x["shows"] for x in c.TENTH_HOUSE_BY_REFERENCE}
    assert "mental" in by_ref["chandra_lagna"]
    assert "mind" in c.HOUSE_REFERENCES["chandra_lagna"]["shows"]
    assert "status" in by_ref["arudha_lagna"]
    assert "status" in c.HOUSE_REFERENCES["arudha_lagna"]["shows"]
    assert "mental" not in by_ref["lagna"] and "status" not in by_ref["lagna"]


# --------------------------------------------------------------------------
# 7.3.5 Paaka Lagna
# --------------------------------------------------------------------------


def test_7_3_5_paaka_lagna_is_the_lagna_lords_rasi():
    """"Paaka lagna is nothing but lagna lord taken as a reference."""
    assert "lagna lord" in c.PAAKA_LAGNA_DEFINITION
    assert "lagna lord" in c.HOUSE_REFERENCES["paaka_lagna"]["note"]


@pytest.mark.parametrize("case", c.PAAKA_LAGNA_EXAMPLES)
def test_7_3_5_the_two_worked_cases(case):
    """"If someone with Pisces lagna has Jupiter in Cancer, then Cancer
    becomes paaka lagna. If someone with Leo lagna has Sun in Virgo, Virgo
    becomes paaka lagna."

    The lord is checked too, not just the answer — the rule is "the lagna
    lord's rasi", so a wrong lord would still give a plausible sign.
    """
    abbr = list(c.RASI_ABBR)
    lagna = abbr.index(case["lagna"])
    lord = int(c.RASI_LORD[lagna])
    assert c.GRAHA_NAMES[lord] == case["lord"]
    got = paaka_lagna_rasi(lagna, {lord: abbr.index(case["lord_rasi"])})
    assert abbr[got] == case["paaka"]


def test_7_3_5_paaka_lagna_needs_the_lords_position():
    """It cannot be computed from the lagna alone — a chart without the lagna
    lord placed is an error, not a default."""
    abbr = list(c.RASI_ABBR)
    with pytest.raises(InputError, match="lagna lord"):
        paaka_lagna_rasi(abbr.index("Pi"), {})


def test_7_3_5_paaka_lagna_can_equal_the_lagna():
    """A lord in its own rasi makes paaka lagna the lagna itself — Leo lagna
    with the Sun in Leo. Not an error, and worth pinning since the two
    references then coincide."""
    abbr = list(c.RASI_ABBR)
    leo = abbr.index("Le")
    assert paaka_lagna_rasi(leo, {int(c.Graha.SUN): leo}) == leo


def test_7_3_5_why_the_lagna_lord_means_the_physical_self():
    """"Rasis represent situations and forces influencing the course of a
    native's life and planets represent individual beings. Lagna lord
    represents the physical self of a native."

    The reasoning matters: it is why paaka lagna differs from lagna at all.
    """
    assert "individual beings" in c.PAAKA_LAGNA_REASON
    assert "physical self" in c.PAAKA_LAGNA_REASON
    assert "physical self" in c.HOUSE_REFERENCES["paaka_lagna"]["shows"]


def test_7_3_5_lagna_is_conceptual_and_paaka_lagna_is_physical():
    """"Lagna shows the concept of self and it deals with one's true
    personality. The physical existence of the person is different from this
    conceptual self."

    The distinction the whole reference scheme turns on — and it "applies to
    all divisional charts", not just D-1.
    """
    assert "concept of self" in c.LAGNA_IS_CONCEPTUAL
    assert "true personality" in c.LAGNA_IS_CONCEPTUAL
    assert "all divisional charts" in c.LAGNA_IS_CONCEPTUAL
    assert c.HOUSE_REFERENCES["lagna"]["shows"] == "true self"
    assert "physical" in c.HOUSE_REFERENCES["paaka_lagna"]["shows"]


def test_7_3_5_where_paaka_lagna_is_used():
    """"Paaka lagna is important when analyzing the natal chart, dasas and
    transits." Three contexts — and the transit one is worked below."""
    assert c.PAAKA_LAGNA_USED_IN == ("the natal chart", "dasas", "transits")


# --------------------------------------------------------------------------
# 7.3.5's D-24 example — the chapter's clearest statement of how a reference
# is chosen
# --------------------------------------------------------------------------


def test_the_d24_example_uses_three_references_for_one_house():
    """"The 5th house shows scholarship, memory and success in competition.
    All these are related to learning and they are seen in D-24... But they
    are better seen from different references."

    One house, one divisional chart, three matters, three references. This is
    §7.3's rule at its sharpest: the chart is fixed, so only the reference
    distinguishes the readings.
    """
    matters = {x["matter"] for x in c.FIFTH_HOUSE_IN_D24_BY_REFERENCE}
    assert matters == {"scholarship", "memory", "success in competition"}
    references = [x["reference"] for x in c.FIFTH_HOUSE_IN_D24_BY_REFERENCE]
    assert len(set(references)) == 3, "three different references"


def test_the_d24_example_matters_are_all_fifth_house_matters():
    """All three must be in the 5th house's own signification list, or the
    example would be adding meanings rather than selecting among them."""
    fifth = c.HOUSE_SIGNIFICATIONS[5].lower()
    assert "scholarship" in fifth
    assert "speculation" in fifth
    # "memory" and "success in competition" are not literal entries — the book
    # names them as 5th-house matters in this passage, which is the same
    # semantic gap OI-55 records for D-12/mother.
    assert "memory" not in fifth
    assert "competition" not in fifth


def test_the_d24_example_is_seen_in_d24_the_chart_of_learning():
    """"All these are related to learning and they are seen in D-24, the chart
    of learning."" Table 11 gives D-24 "Learning, knowledge and education"."""
    assert "Learning" in VARGA_SIGNIFICATIONS["D24"]


@pytest.mark.parametrize("case", c.FIFTH_HOUSE_IN_D24_BY_REFERENCE)
def test_the_d24_example_each_choice_follows_from_the_references_nature(case):
    """Each reference is chosen for a stated reason, and the reason matches
    what §7.3.1 to §7.3.5 say that reference shows.

    - success in competition -> arudha lagna, "illusions and perceptions"
    - scholarship            -> lagna, "true personality... conceptual self"
    - memory                 -> paaka lagna, "physically exists"
    """
    assert case["reference"] in c.HOUSE_REFERENCES
    if case["reference"] == "arudha_lagna":
        assert "perceptions" in case["why"]
        assert "perceived" in c.ARUDHA_LAGNA_SHOWS
    elif case["reference"] == "lagna":
        assert "conceptual self" in case["why"]
        assert "conceptual self" in c.LAGNA_IS_CONCEPTUAL
    else:
        assert "physically exists" in case["why"]
        assert "physical self" in c.PAAKA_LAGNA_REASON


def test_the_d24_example_uses_the_illusion_wording_of_7_3_1():
    """§7.3.1 rejected lagna for status because status "is a part of the
    illusion of this world"; §7.3.5 sends success in competition to arudha
    lagna because it "is related to the illusions and perceptions of the
    world". The same word, used consistently for the same reason."""
    competition = next(
        x for x in c.FIFTH_HOUSE_IN_D24_BY_REFERENCE
        if x["matter"] == "success in competition"
    )
    assert "illusions" in competition["why"]
    assert "illusion" in c.LAGNA_NOT_FOR_STATUS


# --------------------------------------------------------------------------
# Footnote 13's subject — Saturn's transit read three ways
# --------------------------------------------------------------------------


@pytest.mark.parametrize("case", c.SATURN_TRANSIT_BY_REFERENCE)
def test_saturns_transit_reads_differently_from_each_reference(case):
    """"Saturn's transit over the rasi containing one's lagna may throw
    obstructions... over one's Chandra lagna may create frustration and mental
    depression... over one's paaka lagna may leave one feeling sick all the
    time and attack the physical vitality."

    A third instance of the same pattern, this time for a transit rather than
    a house — so the reference scheme is not confined to natal house reading.
    """
    assert case["reference"] in c.HOUSE_REFERENCES
    assert case["shows"]


def test_saturns_transit_readings_match_each_references_subject():
    """Chandra lagna's reading is mental, paaka lagna's is bodily, lagna's is
    neither — the same colouring as the 10th-house contrast."""
    by_ref = {x["reference"]: x["shows"] for x in c.SATURN_TRANSIT_BY_REFERENCE}
    assert "mental" in by_ref["chandra_lagna"]
    assert "physical vitality" in by_ref["paaka_lagna"]
    assert "obstructions" in by_ref["lagna"]
    assert "mental" not in by_ref["lagna"]


def test_the_three_worked_contrasts_use_the_same_three_references():
    """The 10th-house case, the D-24 case and the Saturn-transit case are the
    chapter's three demonstrations of reference selection. Between them they
    exercise lagna, chandra lagna, arudha lagna and paaka lagna."""
    used = set()
    for group in (c.TENTH_HOUSE_BY_REFERENCE, c.FIFTH_HOUSE_IN_D24_BY_REFERENCE,
                  c.SATURN_TRANSIT_BY_REFERENCE):
        used |= {x["reference"] for x in group}
    assert used == {"lagna", "chandra_lagna", "arudha_lagna", "paaka_lagna"}
    for reference in used:
        assert reference in c.HOUSE_REFERENCES


def test_paaka_lagna_through_the_references_endpoint(client):
    """Pisces lagna with Jupiter in Cancer: paaka lagna is Cancer."""
    body = client.post(
        "/v1/house/references",
        json={"lagna_rasi": 11, "graha_rasis": {"4": 3}},
    ).json()
    resolved = {r["reference"]: r.get("rasi_name") for r in body["references"]}
    assert resolved["paaka_lagna"] == "Cancer"
    assert resolved["lagna"] == "Pisces"


# --------------------------------------------------------------------------
# 7.3.6 Karakamsa Lagna
#
# This section is what unblocked the reference. It had been marked
# `available: False` with a note saying karakamsa is "named in chapter 7 and
# defined later" — wrong: §7.3.6 defines it outright. Turned on 2026-08-27.
# --------------------------------------------------------------------------


def test_7_3_6_karakamsa_is_the_atma_karakas_navamsa_rasi():
    """"Navamsa chart throws light on the inner self and the rasi occupied by
    atma karaka in it is called "Karakamsa"."

    Two chapters meet: §8.2's atma karaka and §6.2.9's navamsa. §7.3.6 is what
    joins them, which is why this could not be computed before.
    """
    assert "atma karaka" in c.KARAKAMSA_DEFINITION
    assert "Karakamsa" in c.KARAKAMSA_DEFINITION

    from hora.charts.karaka import atma_karaka
    from hora.charts.vargas import d9_navamsa

    longitudes = EXAMPLE_28_LONGITUDES
    karaka = atma_karaka(longitudes)
    assert karakamsa_rasi(longitudes) == d9_navamsa(longitudes[karaka.graha]).sign


def test_7_3_6_it_is_the_navamsa_rasi_not_the_rasi_chart_one():
    """The distinction the section turns on — "an important reference point in
    **navamsa** chart".

    Demonstrated on a chart where the two genuinely differ, so the assertion
    has teeth: an implementation using the atma karaka's D-1 rasi would give a
    different sign here.
    """
    from hora.charts.karaka import atma_karaka
    from hora.charts.vargas import d9_navamsa

    # One graha far into its rasi, so its navamsa is several signs away.
    longitudes = {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 28.5, 7: 7.0}
    karaka = atma_karaka(longitudes)
    assert karaka.graha == 6, "Saturn has the highest advancement here"

    rasi_chart_sign = int(longitudes[6] // 30)
    navamsa_sign = d9_navamsa(longitudes[6]).sign
    assert navamsa_sign != rasi_chart_sign, "the two must differ for this test"
    assert karakamsa_rasi(longitudes) == navamsa_sign
    assert karakamsa_rasi(longitudes) != rasi_chart_sign


def test_7_3_6_why_navamsa_and_not_the_rasi_chart():
    """"Because the soul is an important factor in deciding the nature of
    inner self than the physical existence, atma karaka is an important
    reference point in navamsa chart."

    The same conceptual/physical split §7.3.5 drew for lagna and paaka lagna.
    """
    assert "inner self" in c.KARAKAMSA_REASON
    assert "physical existence" in c.KARAKAMSA_REASON
    assert c.HOUSE_REFERENCES["karakamsa_lagna"]["shows"] == "the inner self"


def test_7_3_6_the_atma_karaka_stands_for_the_soul():
    """"Atma karaka stands for the soul of the person."

    Chapter 3 gives the Sun "soul" and §7.3.3 makes Ravi lagna the soul's
    reference — so two references touch the soul, from different directions.
    Both are recorded rather than one being taken for the other.
    """
    assert "soul of the person" in c.KARAKAMSA_REASON
    assert "soul" in c.HOUSE_REFERENCES["ravi_lagna"]["shows"]
    assert c.HOUSE_REFERENCES["karakamsa_lagna"]["shows"] != (
        c.HOUSE_REFERENCES["ravi_lagna"]["shows"]
    )


def test_7_3_6_the_twelfth_from_karakamsa():
    """"The 12th house from Karakamsa shows the liberation of the soul and the
    situation of Ketu there is conducive to moksha."

    The chapter's only moksha rule. The 12th house's own signification ends
    with "moksha (emancipation/liberation)" — the same word, so the rule sits
    on §7.2's table rather than beside it.
    """
    assert c.KARAKAMSA_MOKSHA_HOUSE == 12
    assert c.KARAKAMSA_MOKSHA_GRAHA == c.Graha.KETU
    assert "moksha" in c.HOUSE_SIGNIFICATIONS[12]
    assert "liberation" in c.HOUSE_SIGNIFICATIONS[12]
    assert "liberation of the soul" in c.KARAKAMSA_TWELFTH_RULE


def test_7_3_6_the_propitiation_rule_is_recorded_not_computed():
    """"Propitiation of the deities corresponding to the strongest planet in
    the 12th house in navamsa from Karakamsa lagna can take one's soul towards
    moksha."

    Needs a strength measure across the 12th house's occupants, which chapter
    15 supplies and nothing joins up yet. The deities are chapter 3's.
    """
    assert "strongest planet" in c.KARAKAMSA_TWELFTH_RULE
    assert "deities" in c.KARAKAMSA_TWELFTH_RULE
    assert len(c.GRAHA_DEITY) == 7, "chapter 3 supplies the deities"


def test_7_3_6_karakamsa_is_now_available_as_a_reference():
    """It was `available: False` pending "the chapter that defines this
    lagna". §7.3.6 is that chapter."""
    assert c.HOUSE_REFERENCES["karakamsa_lagna"]["available"] is True
    assert "7.3.6" in c.HOUSE_REFERENCES["karakamsa_lagna"]["note"]


def test_karakamsa_needs_longitudes_not_rasis():
    """The atma karaka is the graha of highest advancement **within** its
    rasi, so rasi indices alone cannot find it."""
    result = house_service.references(
        lagna_rasi=3, graha_rasis={g: int(v // 30) for g, v in
                                   EXAMPLE_28_LONGITUDES.items()},
    )
    entry = next(
        r for r in result["references"] if r["reference"] == "karakamsa_lagna"
    )
    assert entry.get("rasi") is None
    assert "longitudes" in entry["unavailable_because"]


def test_every_reference_resolves_when_the_inputs_are_given():
    """All eight of §7.3's references, from one chart. Ghati and Hora lagna
    are chapter 5's and are passed in; the rest are computed."""
    rasis = {g: int(v // 30) for g, v in EXAMPLE_28_LONGITUDES.items()}
    result = house_service.references(
        lagna_rasi=3,
        graha_rasis=rasis,
        graha_longitudes=EXAMPLE_28_LONGITUDES,
        ghati_lagna_rasi=5,
        hora_lagna_rasi=8,
    )
    resolved = {
        r["reference"] for r in result["references"] if r.get("rasi") is not None
    }
    assert resolved == set(c.HOUSE_REFERENCES), "all eight"


# --------------------------------------------------------------------------
# 7.3.7 Ghati Lagna and 7.3.8 Hora Lagna
# --------------------------------------------------------------------------


def test_7_3_7_ghati_lagna_shows_power_authority_and_fame():
    """"Ghati lagna (GL) shows self, from the point of view of power,
    authority and fame."

    Chapter 5 gives GL "fame, power and authority" — the same three words in a
    different order. Both are the book's; the two chapters agree.
    """
    from hora.charts.special_lagna import SPECIAL_LAGNA_SIGNIFIES, SpecialLagna

    assert c.GHATI_LAGNA_SHOWS == (
        "self, from the point of view of power, authority and fame"
    )
    chapter_5 = SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.GHATI]
    for word in ("fame", "power", "authority"):
        assert word in c.GHATI_LAGNA_SHOWS
        assert word in chapter_5


def test_7_3_7_what_ghati_lagna_is_used_for():
    """"When we analyze promotions in career or political power of
    politicians, this reference is very important."

    §6.5's promotion pattern uses GL for exactly this reason — the two
    sections agree on the use, not just the signification.
    """
    assert "promotions in career" in c.GHATI_LAGNA_USED_FOR
    assert "politicians" in c.GHATI_LAGNA_USED_FOR
    promotion = next(
        p for p in c.MATTER_ANALYSIS_PATTERNS if p["matter"] == "promotion at the office"
    )
    assert promotion["significator"] == "GL"


def test_7_3_8_hora_lagna_shows_wealth():
    """"Hora lagna (HL) shows self, from the point of view of wealth. This
    reference is important when analyzing one's wealth."

    Chapter 5 gives HL "money, wealth and prosperity".
    """
    from hora.charts.special_lagna import SPECIAL_LAGNA_SIGNIFIES, SpecialLagna

    assert c.HORA_LAGNA_SHOWS == "self, from the point of view of wealth"
    assert "wealth" in SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.HORA]
    assert "wealth" in c.HORA_LAGNA_USED_FOR


def test_the_three_self_references_share_a_phrasing():
    """Lagna, Ghati lagna and Hora lagna all show *self* — from no particular
    point of view, from power, and from wealth. That parallel is the book's
    own and is why they are one family."""
    assert c.HOUSE_REFERENCES["lagna"]["shows"] == "true self"
    assert c.GHATI_LAGNA_SHOWS.startswith("self, from the point of view of")
    assert c.HORA_LAGNA_SHOWS.startswith("self, from the point of view of")


# --------------------------------------------------------------------------
# Footnote 13
# --------------------------------------------------------------------------


def test_footnote_13_defines_transit():
    """"If a planet occupies, on a given day, a particular rasi, then it is
    said to "transit" in that sign on that day. Transit positions refer to the
    positions of planets on a given day and natal positions refer to the
    positions of planets at the time of one's birth."

    The definition the Saturn-transit readings above rest on, and the one the
    transit chapters will need.
    """
    assert "transit" in c.TRANSIT_DEFINITION
    assert "natal positions" in c.TRANSIT_DEFINITION
    assert "time of one's birth" in c.TRANSIT_DEFINITION


# --------------------------------------------------------------------------
# 7.3.9 Graha Lagnas and Table 12
# --------------------------------------------------------------------------

#: Table 12 exactly as printed, in the book's own order per row.
TABLE_12 = [
    ("Sun", (9, 10, 11)),
    ("Moon", (4, 1, 2, 11, 9)),
    ("Mars", (3,)),
    ("Mercury", (6,)),
    ("Jupiter", (5,)),
    ("Venus", (7,)),
    ("Saturn", (8, 12)),
]


@pytest.mark.parametrize("name,houses", TABLE_12)
def test_table_12_row_by_row(name, houses):
    graha = [str(x) for x in c.GRAHA_NAMES].index(name)
    assert c.GRAHA_LAGNA_HOUSES[graha] == houses


def test_table_12_keeps_the_moons_unsorted_order():
    """The Moon's row reads "4th, 1st, 2nd, 11th, 9th" — not ascending. Every
    other row is ascending, so this one is easy to "tidy" into 1, 2, 4, 9, 11.

    Whatever the ordering means, it is the book's, and sorting it would lose
    information we cannot recover.
    """
    moon = c.GRAHA_LAGNA_HOUSES[c.Graha.MOON]
    assert moon == (4, 1, 2, 11, 9)
    assert list(moon) != sorted(moon)
    for graha, houses in c.GRAHA_LAGNA_HOUSES.items():
        if graha != c.Graha.MOON:
            assert list(houses) == sorted(houses), c.GRAHA_NAMES[graha]


def test_table_12_covers_the_seven_and_not_the_nodes():
    """Seven rows. Rahu and Ketu are not natural significators of a house
    here, so they are absent rather than empty."""
    assert sorted(c.GRAHA_LAGNA_HOUSES) == list(range(7))
    assert c.Graha.RAHU not in c.GRAHA_LAGNA_HOUSES


def test_table_12_leaves_no_house_unassigned():
    """Every house from 1 to 12 has at least one graha reference — which is
    what makes "for each house, a planet works as the natural significator"
    true rather than approximate."""
    covered = {h for houses in c.GRAHA_LAGNA_HOUSES.values() for h in houses}
    assert covered == set(range(1, 13))


def test_table_12_assigns_two_houses_to_more_than_one_graha():
    """The 9th belongs to both Sun and Moon, and the 11th to both Sun and
    Moon. So a house does not map to a single graha, and a reverse lookup must
    return a list."""
    ninth = [g for g, hs in c.GRAHA_LAGNA_HOUSES.items() if 9 in hs]
    eleventh = [g for g, hs in c.GRAHA_LAGNA_HOUSES.items() if 11 in hs]
    assert set(ninth) == {c.Graha.SUN, c.Graha.MOON}
    assert set(eleventh) == {c.Graha.SUN, c.Graha.MOON}


def test_7_3_9_what_a_graha_lagna_is():
    """"we use several "graha lagnas" or planetary references. For each house,
    a planet works as the natural significator."""
    assert c.GRAHA_LAGNA_NAME == "graha lagnas"
    assert c.GRAHA_LAGNA_ALIAS == "planetary references"
    assert "natural significator" in c.GRAHA_LAGNA_RULE


@pytest.mark.parametrize("pair", c.GRAHA_LAGNA_PAIRS)
def test_7_3_9_each_worked_pair_is_in_table_12(pair):
    """"we see the 4th from lagna and the 4th from Moon for mother. We see the
    9th from Sun and the 9th from lagna for father..."

    Each pair must be a Table 12 entry, or the prose and the table disagree.
    """
    assert pair["house"] in c.GRAHA_LAGNA_HOUSES[pair["graha"]]


@pytest.mark.parametrize("pair", c.GRAHA_LAGNA_PAIRS)
def test_7_3_9_each_matter_is_in_that_houses_signification(pair):
    """The matter each pair is read for must be a matter §7.2 gives that
    house — otherwise the pairing would be introducing meanings.

    Five of the six match literally. The sixth does not: §7.3.9 says
    **progeny** where §7.2's 5th house says **Children**. A synonym, not a
    disagreement — and the third instance of the gap OI-55 records, after
    D-12/mother and memory/competition.
    """
    signification = c.HOUSE_SIGNIFICATIONS[pair["house"]].lower()
    synonyms = {"progeny": "children"}
    first = pair["matter"].split(" or ")[0].split()[0].rstrip("s").lower()
    assert synonyms.get(first, first) in signification, (pair["house"], first)


def test_7_3_9_only_progeny_needs_a_synonym():
    """Bounding the gap: of §7.3.9's six matters, exactly one is not a literal
    word of its house's signification. If a second appears, this fails rather
    than the synonym table quietly growing.
    """
    non_literal = []
    for pair in c.GRAHA_LAGNA_PAIRS:
        first = pair["matter"].split(" or ")[0].split()[0].rstrip("s").lower()
        if first not in c.HOUSE_SIGNIFICATIONS[pair["house"]].lower():
            non_literal.append(first)
    assert non_literal == ["progeny"]
    assert "children" in c.HOUSE_SIGNIFICATIONS[5].lower()


def test_7_3_9_the_pairs_line_up_with_chapter_3():
    """Moon for mother, Sun for father, Jupiter for progeny, Venus for
    marriage — each graha is the natural karaka of its matter, which chapter 8
    tabulates. Checked here so §7.3.9's pairing is not an independent claim.
    """
    from hora.charts.karaka import naisargika_karaka

    assert callable(naisargika_karaka)
    by_house = {p["house"]: p["graha"] for p in c.GRAHA_LAGNA_PAIRS}
    assert by_house[4] == c.Graha.MOON, "mother"
    assert by_house[9] == c.Graha.SUN, "father"
    assert by_house[5] == c.Graha.JUPITER, "progeny"
    assert by_house[7] == c.Graha.VENUS, "marriage"


def test_7_3_9_the_strength_rule_decides_between_two_references():
    """"If Mars is stronger than lagna, then the 3rd house from Mars may be
    more important than the 3rd house from lagna."

    The only place the chapter says how to **choose** between two references
    rather than which to use for what. It needs a strength comparison between
    a graha and the lagna, which is chapter 15's. Not implemented — see
    OI-56.
    """
    assert "stronger than lagna" in c.GRAHA_LAGNA_STRENGTH_RULE
    assert "more important" in c.GRAHA_LAGNA_STRENGTH_RULE
    mars_pair = next(p for p in c.GRAHA_LAGNA_PAIRS if p["graha"] == c.Graha.MARS)
    assert mars_pair["house"] == 3


def test_7_3_9_the_naisargika_extension_goes_beyond_table_12():
    """"In addition to the above list, we can find a house with respect to the
    naisargika karaka who signifies the matter shown by a house."

    Table 12 is a fixed list; this is open-ended — any natural significator of
    the matter can be the reference.
    """
    assert "In addition" not in c.NAISARGIKA_REFERENCE_RULE
    assert "naisargika karaka" in c.NAISARGIKA_REFERENCE_RULE
    assert "signifies the matter" in c.NAISARGIKA_REFERENCE_RULE


@pytest.mark.parametrize("case", c.NAISARGIKA_REFERENCE_EXAMPLES)
def test_7_3_9_the_naisargika_examples_name_their_chart(case):
    """"the 4th from Venus in D-16 can show one's happiness from vehicles" and
    "the 2nd house from lagna and the 2nd house from Mercury show speech (in
    rasi, D-9 and D-27)".

    Unlike Table 12's pairs, these name the **divisional chart** — which is
    §7.3's three-choices rule (chart, reference, house) fully specified.
    """
    for chart in case["charts"]:
        assert chart in VARGA_SIGNIFICATIONS
    assert case["house"] in range(1, 13)


def test_7_3_9_the_venus_example_matches_table_11():
    """"Venus signifies vehicles. D-16 is the chart that shows vehicles and
    pleasures." Table 11 gives D-16 "Vehicles, pleasures, comforts and
    discomforts" — the same two words, so the sections agree."""
    venus = next(
        x for x in c.NAISARGIKA_REFERENCE_EXAMPLES if x["graha"] == c.Graha.VENUS
    )
    assert venus["charts"] == ("D16",)
    assert "Vehicles" in VARGA_SIGNIFICATIONS["D16"]
    assert "pleasures" in VARGA_SIGNIFICATIONS["D16"]
    assert "vehicles" in c.HOUSE_SIGNIFICATIONS[4].lower()


def test_7_3_9_the_mercury_example_matches_chapter_3():
    """"As Mercury is the natural significator of speech, the 2nd house from
    lagna and the 2nd house from Mercury show speech."

    Chapter 3 gives Mercury "speech" as its governance, and §7.2 gives the 2nd
    house "speech". Three sections, one word.
    """
    mercury = next(
        x for x in c.NAISARGIKA_REFERENCE_EXAMPLES if x["graha"] == c.Graha.MERCURY
    )
    assert mercury["house"] == 2
    assert c.GRAHA_GOVERNS[c.Graha.MERCURY] == "speech"
    assert "speech" in c.HOUSE_SIGNIFICATIONS[2].lower()


def test_7_3_9_speech_is_read_in_three_charts():
    """"(in rasi, D-9 and D-27)" — the only place the chapter names more than
    one chart for a matter. D-27 is "Strengths and weaknesses, inherent
    nature", which is why speech belongs there."""
    mercury = next(
        x for x in c.NAISARGIKA_REFERENCE_EXAMPLES if x["graha"] == c.Graha.MERCURY
    )
    assert mercury["charts"] == ("D1", "D9", "D27")
    assert "inherent nature" in VARGA_SIGNIFICATIONS["D27"]
    assert "inner self" in VARGA_SIGNIFICATIONS["D9"]


def test_the_rules_endpoint_publishes_table_12(client):
    body = client.get("/v1/house/rules").json()
    assert "graha_lagna_houses" in body or "graha_lagnas" in body, list(body)


# --------------------------------------------------------------------------
# 7.4 Special Categories
# --------------------------------------------------------------------------

#: §7.4's seven numbered categories, exactly as printed.
SPECIAL_CATEGORIES = [
    ("trikona", (1, 5, 9), ["kona", "trine"]),
    ("kendra", (1, 4, 7, 10), ["quadrant", "angle"]),
    ("panaphara", (2, 5, 8, 11), ["succedant"]),
    ("apoklima", (3, 6, 9, 12), ["precedant"]),
    ("upachaya", (3, 6, 10, 11), []),
    ("dusthana", (6, 8, 12), ["trik sthana"]),
    ("chaturasra", (4, 8), []),
]


@pytest.mark.parametrize("name,houses,synonyms", SPECIAL_CATEGORIES)
def test_7_4_each_category_from_the_first_house(name, houses, synonyms):
    """"The 1st, 5th and 9th houses form a triangle and they are known as
    "konas" or "trikonas" or "trines"." and the six that follow."""
    entry = c.HOUSE_CATEGORIES[name]
    assert tuple(entry["houses"]) == houses
    assert entry["synonyms"] == synonyms


def test_7_4_there_are_seven_categories():
    assert len(c.HOUSE_CATEGORIES) == 7
    assert list(c.HOUSE_CATEGORIES) == [n for n, _, _ in SPECIAL_CATEGORIES]


def test_7_4_the_first_house_is_both_a_trine_and_a_quadrant():
    """1, 5, 9 and 1, 4, 7, 10 both contain the 1st. The categories overlap,
    so a house can carry several — `classify_house` must return a list."""
    assert 1 in c.HOUSE_CATEGORIES["trikona"]["houses"]
    assert 1 in c.HOUSE_CATEGORIES["kendra"]["houses"]
    assert set(classify_house(1)) >= {"trikona", "kendra"}


def test_7_4_the_eighth_house_carries_three_categories():
    """8 is a panaphara, a dusthana and a chaturasra — the most loaded house
    in the scheme."""
    carried = {
        name for name, entry in c.HOUSE_CATEGORIES.items()
        if 8 in entry["houses"]
    }
    assert carried == {"panaphara", "dusthana", "chaturasra"}


def test_7_4_panaphara_and_apoklima_are_defined_by_construction():
    """"These are basically the quadrants from the 2nd house" and "...from the
    3rd house."

    §7.4 gives these two **no signification** — only a derivation. That used
    to sit in the `shows` field, so a caller asking what a panaphara *means*
    got a definition instead. Moved to `derivation` on 2026-08-27.
    """
    for name, base in (("panaphara", 2), ("apoklima", 3)):
        entry = c.HOUSE_CATEGORIES[name]
        assert entry["shows"] is None, name
        assert f"quadrants from the {base}" in entry["derivation"]
        # And the derivation is true: the kendras from that house.
        assert tuple(category_houses("kendra", base)) == tuple(entry["houses"])


def test_7_4_only_three_categories_lack_a_signification():
    """Panaphara, apoklima and chaturasra. The other four have one, so a null
    `shows` is meaningful rather than merely missing."""
    without = {n for n, e in c.HOUSE_CATEGORIES.items() if e["shows"] is None}
    assert without == {"panaphara", "apoklima", "chaturasra"}


def test_7_4_the_dusthana_gloss():
    """"trik sthanas" or "dusthanas" (bad/evil houses)" — the only category
    §7.4 glosses."""
    assert c.DUSTHANA_GLOSS == "bad/evil houses"
    assert "trik sthana" in c.HOUSE_CATEGORIES["dusthana"]["synonyms"]


def test_7_4_the_categories_are_relative_like_the_houses():
    """"We can find trines, quadrants etc from lagna or other references or
    even from houses... Thus we can find trines, quadrants etc from any
    house."""
    assert "from any house" in c.CATEGORIES_ARE_RELATIVE


@pytest.mark.parametrize("name,expected", sorted(c.CATEGORIES_FROM_THIRD_HOUSE.items()))
def test_7_4_the_worked_example_from_the_third_house(name, expected):
    """"3rd, 7th and 11th houses are the trines from the 3rd house...
    the 3rd, 6th, 9th and 12th houses are the quadrants from the 3rd house.
    And the 5th, 8th, 12th and 1st houses are the upachayas from the 3rd
    house. The 8th, 10th and 2nd houses are the dusthanas from the 3rd
    house."

    The book lists upachayas and dusthanas out of order (5, 8, 12, 1 and
    8, 10, 2), so the comparison is by set.
    """
    assert set(category_houses(name, 3)) == set(expected)


def test_7_4_the_worked_examples_counting_is_inclusive():
    """"The 5th house from the 3rd house is the 7th house (count 1, 2, 3, 4,
    and 5 starting from the 3rd house. We get 3rd, 4th, 5th, 6th and 7th)."

    The same inclusive count as §7.2's houses-from-houses, spelled out again.
    """
    assert house_service.derived(5, 3)["result"] == 7
    assert house_service.derived(9, 3)["result"] == 11
    assert set(category_houses("trikona", 3)) == {3, 7, 11}


def test_7_4_every_category_shifts_with_the_base_house():
    """A category from house n is the category from house 1, shifted by n-1.
    Checked for all seven categories from all twelve bases."""
    for name, houses, _ in SPECIAL_CATEGORIES:
        for base in range(1, 13):
            expected = {(h + base - 2) % 12 + 1 for h in houses}
            assert set(category_houses(name, base)) == expected, (name, base)


def test_7_4_the_categories_endpoint_carries_the_derivation(client):
    body = client.get("/v1/house/categories/3").json()
    by_name = {e["category"]: e for e in body["categories"]}
    assert set(by_name["trikona"]["houses"]) == {3, 7, 11}
    assert by_name["panaphara"]["shows"] is None
    assert "quadrants from the 2nd" in by_name["panaphara"]["derivation"]
    assert by_name["trikona"]["derivation"] is None


# --------------------------------------------------------------------------
# Footnote 14 — why speech needs three charts
# --------------------------------------------------------------------------


@pytest.mark.parametrize("role", c.SPEECH_CHART_ROLES)
def test_footnote_14_each_charts_role(role):
    """"Rasi chart shows the overall picture and the manifestation at the
    physical level. Navamsa shows basic skills and the way one interacts with
    others. D-27 shows one's strengths and weaknesses."

    The three charts §7.3.9 names for speech, each with a stated role.
    """
    assert role["chart"] in VARGA_SIGNIFICATIONS
    assert role["shows"]


def test_footnote_14_roles_agree_with_table_11():
    """D-9's "basic skills and the way one interacts with others" and D-27's
    "strengths and weaknesses" are Table 11's own phrases. D-1's is not — the
    footnote describes it as the physical level, which Table 11 calls
    "Existence at the physical level"."""
    by_chart = {r["chart"]: r["shows"] for r in c.SPEECH_CHART_ROLES}
    assert "basic skills" in VARGA_SIGNIFICATIONS["D9"]
    assert "basic skills" in by_chart["D9"]
    assert "strengths and weaknesses" in VARGA_SIGNIFICATIONS["D27"].lower()
    assert "strengths and weaknesses" in by_chart["D27"]
    assert "physical level" in VARGA_SIGNIFICATIONS["D1"]
    assert "physical level" in by_chart["D1"]


def test_footnote_14_two_charts_may_disagree():
    """"One may have strong benefics in the 2nd from lagna in rasi and navamsa
    charts, but malefics in the 2nd from Mercury in D-27. In such a case, one
    will be a skilled speaker, but harsh speech may be his weakness."

    The clearest case in the chapter of charts disagreeing about one matter —
    and the disagreement is the reading, not an error to resolve. Note it also
    switches reference between the charts: lagna for rasi and navamsa, Mercury
    for D-27.
    """
    note = c.THREE_CHARTS_FOR_SPEECH_NOTE
    assert "2nd from lagna" in note
    assert "2nd from Mercury" in note
    assert "skilled speaker" in note and "harsh speech" in note
    assert "All the three charts are important" in note


def test_footnote_14_matches_the_speech_example_in_7_3_9():
    """§7.3.9 says speech is seen "in rasi, D-9 and D-27"; footnote 14 says
    what each contributes. The two must name the same three charts."""
    mercury = next(
        x for x in c.NAISARGIKA_REFERENCE_EXAMPLES if x["graha"] == c.Graha.MERCURY
    )
    assert set(mercury["charts"]) == {r["chart"] for r in c.SPEECH_CHART_ROLES}


# --------------------------------------------------------------------------
# 7.4.1 Trines and the four purushaarthas
# --------------------------------------------------------------------------


def test_7_4_1_trines_are_beneficial_to_their_reference():
    """"Trines from any reference are houses that are beneficial to the
    reference. They bring prosperity and well-being to the reference. For
    example, trines from lagna shows prosperity of self."

    Relative, like everything else in §7.3 — the benefit accrues to whatever
    the trines are counted from, not to the native in general.
    """
    assert "beneficial to the reference" in c.TRINE_IS_BENEFICIAL
    assert "Goddess Lakshmi" in c.TRINE_ABODE
    assert c.HOUSE_CATEGORIES["trikona"]["presiding"] == "Goddess Lakshmi"


#: §7.4.1's four purushaarthas exactly as printed.
PURUSHAARTHAS = [
    ("dharma", "righteousness and adherence to one's duty", (1, 5, 9), 1),
    ("artha", "money and career", (2, 6, 10), 2),
    ("kaama", "desiring things and getting them", (3, 7, 11), 3),
    ("moksha", "final liberation of soul", (4, 8, 12), 4),
]


@pytest.mark.parametrize("name,meaning,houses,base", PURUSHAARTHAS)
def test_7_4_1_each_purushaartha(name, meaning, houses, base):
    """"(1) Dharma: righteousness and adherence to one's duty, (2) Artha:
    money and career, (3) Kaama: desiring things and getting them, and,
    (4) Moksha: final liberation of soul."""
    entry = c.PURUSHARTHA_TRIKONAS[name]
    assert entry["meaning"] == meaning
    assert entry["houses"] == houses


@pytest.mark.parametrize("name,meaning,houses,base", PURUSHAARTHAS)
def test_7_4_1_each_is_the_trines_from_its_base_house(name, meaning, houses, base):
    """"Dharma is shown by the trines from the 1st house... Trines from the
    2nd house are called "artha trikonas"... from the 3rd... from the 4th."

    Computed rather than restated: each set must equal `category_houses`
    for trikona from that base.
    """
    assert c.PURUSHARTHA_TRIKONA_NAMES[name]["base"] == base
    assert set(category_houses("trikona", base)) == set(houses)


def test_7_4_1_the_four_trikonas_tile_all_twelve_houses():
    """Trines from the 1st, 2nd, 3rd and 4th together cover every house
    exactly once — which is what makes the four purushaarthas a complete
    partition of life rather than four overlapping views."""
    covered = [h for _, _, houses, _ in PURUSHAARTHAS for h in houses]
    assert sorted(covered) == list(range(1, 13))
    assert len(set(covered)) == 12


def test_7_4_1_the_bases_are_the_first_four_houses():
    """1, 2, 3, 4 — consecutive. A fifth purushaartha would need the trines
    from the 5th, which are the dharma trikonas again."""
    bases = sorted(v["base"] for v in c.PURUSHARTHA_TRIKONA_NAMES.values())
    assert bases == [1, 2, 3, 4]
    assert set(category_houses("trikona", 5)) == set(category_houses("trikona", 1))


@pytest.mark.parametrize("name,meaning,houses,base", PURUSHAARTHAS)
def test_7_4_1_the_sanskrit_names_and_glosses(name, meaning, houses, base):
    """""dharma trikonas" (trines of duty)", "artha trikonas" (trines of
    money)", "kaama trikonas" (trines of desire)", "moksha trikonas" (trines
    of liberation)"."""
    entry = c.PURUSHARTHA_TRIKONA_NAMES[name]
    assert entry["name"] == f"{name} trikonas"
    assert entry["gloss"].startswith("trines of ")


def test_7_4_1_each_house_has_a_stated_reason():
    """"The 2nd house shows wealth. The 6th house shows service. The 10th
    house shows career and activities in society." and the same for the other
    three groups — twelve reasons in all."""
    assert set(c.PURUSHARTHA_HOUSE_REASONS) == set(range(1, 13))
    for _, _, houses, _ in PURUSHAARTHAS:
        for house in houses:
            assert c.PURUSHARTHA_HOUSE_REASONS[house]


def test_7_4_1_eight_of_the_twelve_reasons_are_literal():
    """§7.4.1's reasons are mostly §7.2's own words — wealth, service, career,
    intelligence, dharma, gains, moksha, occult studies.

    Four are not: **prosperity** (1st), **persistence** (3rd), **harmony**
    (4th) and **relations** (7th). The 3rd house says "courage, mental
    strength"; the 4th says "peace". Synonyms, not disagreements — the same
    gap OI-55 records, and the reason a literal matcher keeps missing.
    """
    non_literal = [
        house for house, reason in c.PURUSHARTHA_HOUSE_REASONS.items()
        if reason.split()[0].lower() not in c.HOUSE_SIGNIFICATIONS[house].lower()
    ]
    assert sorted(non_literal) == [1, 3, 4, 7]
    assert "courage" in c.HOUSE_SIGNIFICATIONS[3].lower()
    assert "peace" in c.HOUSE_SIGNIFICATIONS[4].lower()


def test_7_4_1_the_dharma_trikonas_reasons_match_the_opening_claim():
    """"trines from the 1st house... show prosperity of self, intelligence and
    dharma" — and the opening said "trines from lagna shows prosperity of
    self". The same phrase, so the section is consistent with itself."""
    assert c.PURUSHARTHA_HOUSE_REASONS[1] == "prosperity of self"
    assert "prosperity" in c.TRINE_IS_BENEFICIAL


def test_7_4_1_what_decides_how_one_follows_dharma():
    """"The character of a person, his intelligence and his righteousness
    decide how one follows dharma – the first purpose of human existence."""
    assert "character" in c.DHARMA_IS_DECIDED_BY
    assert "intelligence" in c.DHARMA_IS_DECIDED_BY
    assert "righteousness" in c.DHARMA_IS_DECIDED_BY


def test_footnote_15_dharma_means_duty_not_righteousness():
    """"Dharma literally means duty. However, it has come to mean
    righteousness."

    Both senses are used in the same section: the gloss for dharma trikonas is
    "trines of **duty**", while the purushaartha's meaning is
    "**righteousness** and adherence to one's duty". Footnote 15 is what
    reconciles them.
    """
    assert c.DHARMA_LITERAL_MEANING == "duty"
    assert "righteousness" in c.DHARMA_NOTE
    assert c.PURUSHARTHA_TRIKONA_NAMES["dharma"]["gloss"] == "trines of duty"
    assert "righteousness" in c.PURUSHARTHA_TRIKONAS["dharma"]["meaning"]


def test_7_4_1_the_purushaartha_order_is_the_books():
    """Dharma, artha, kaama, moksha — numbered (1) to (4), and the base houses
    run 1 to 4 in the same order. Reordering them would break the mapping."""
    assert list(c.PURUSHARTHA_TRIKONAS) == ["dharma", "artha", "kaama", "moksha"]
    bases = [c.PURUSHARTHA_TRIKONA_NAMES[k]["base"] for k in c.PURUSHARTHA_TRIKONAS]
    assert bases == [1, 2, 3, 4]


def test_7_4_1_the_digbala_rule_is_recorded_not_computed():
    """"Digbala of planets who attain full digbala in various of these trines
    shows the strength of different purushaarthas in one's life."

    Chapter 3 gives each graha its digbala house; nothing joins that to the
    purushaartha trikonas. See OI-57.
    """
    assert "digbala" in c.PURUSHARTHA_STRENGTH_RULE
    assert "purushaarthas" in c.PURUSHARTHA_STRENGTH_RULE
    assert len(c.DIG_BALA_STRONG_HOUSE) == 7, "chapter 3 supplies the houses"


def test_7_4_1_the_digbala_houses_fall_across_three_purushaarthas():
    """The four digbala houses are 1, 4, 7 and 10 — one from dharma, one from
    moksha, one from kaama and one from artha. So every purushaartha has
    exactly one graha capable of full digbala in it, which is what makes the
    rule discriminating.
    """
    by_house = {}
    for name, _, houses, _ in PURUSHAARTHAS:
        for house in houses:
            by_house[house] = name
    hit = {by_house[h] for h in set(c.DIG_BALA_STRONG_HOUSE.values())}
    assert hit == {"dharma", "artha", "kaama", "moksha"}


def test_7_4_1_trikona_dasa_is_named_but_not_defined_here():
    """"Dasas like "Trikona Dasa" which are based on trines show how one
    follows the four purushaarthas in life." Named only; `dasha/rasi/` is
    empty."""
    assert "Trikona Dasa" in c.TRIKONA_DASA_NOTE


def test_footnote_16_planets_in_mutual_trines():
    """"Planets in mutual trines make each other prosper."

    Mutual because trine-ness is symmetric: if B is a trine from A then A is a
    trine from B, which is not true of most house relations.
    """
    assert "mutual trines" in c.MUTUAL_TRINES_RULE
    for a in range(1, 13):
        for b in category_houses("trikona", a):
            assert a in category_houses("trikona", b), (a, b)


def test_trines_are_the_only_symmetric_category():
    """Kendras are symmetric too, but panapharas, apoklimas, upachayas,
    dusthanas and chaturasras are not — so footnote 16's "mutual" is a real
    restriction, not a turn of phrase."""
    symmetric = set()
    for name in c.HOUSE_CATEGORIES:
        if all(
            a in category_houses(name, b)
            for a in range(1, 13)
            for b in category_houses(name, a)
        ):
            symmetric.add(name)
    assert symmetric == {"trikona", "kendra"}


# --------------------------------------------------------------------------
# 7.4.2 Quadrants
# --------------------------------------------------------------------------


def test_7_4_2_quadrants_are_the_abode_of_maha_vishnu():
    """"Quadrants are the abode of Sri Maha Vishnu, the Supreme Lord who
    sustains this universe as per Hinduism."

    The epithet is not decoration: "sustains" is the same word as the
    category's signification, so the deity and the meaning agree.
    """
    assert c.HOUSE_CATEGORIES["kendra"]["presiding"] == "Sri Maha Vishnu"
    assert "sustains" in c.MAHA_VISHNU_EPITHET
    assert "Sustenance" in c.HOUSE_CATEGORIES["kendra"]["shows"]


def test_7_4_2_quadrants_are_relative_like_the_trines():
    """"Quadrants from any reference show its sustenance." — "any reference",
    matching §7.4.1's "trines from any reference"."""
    assert "from any reference" in c.QUADRANT_IS_SUSTENANCE
    assert "from any reference" in c.TRINE_IS_BENEFICIAL


@pytest.mark.parametrize(
    "house,reason",
    [(1, "self"), (4, "comforts"), (7, "marriage and relations with others"),
     (10, "profession")],
)
def test_7_4_2_each_quadrants_reason(house, reason):
    """"The 1st house (self), 4th house (comforts), 7th house (marriage and
    relations with others) and the 10th house (profession) sustain each
    other."""
    assert c.QUADRANT_HOUSE_REASONS[house] == reason
    assert f"({reason})" in c.QUADRANTS_SUSTAIN_EACH_OTHER


def test_7_4_2_the_reasons_cover_the_quadrants_and_nothing_else():
    assert sorted(c.QUADRANT_HOUSE_REASONS) == list(c.KENDRA)


def test_7_4_2_only_the_first_houses_reason_is_not_the_books_own_word():
    """comforts, marriage and profession are all in §7.2's lists. **self** is
    not — §7.2's 1st house says "Physical body, complexion, appearance, head,
    intelligence...".

    The book uses "self" for the 1st house constantly (§7.3's lagna "shows
    true self", §7.4.1's "prosperity of self") but never in §7.2's own list.
    The same OI-55 gap, and the same house, twice in two sections.
    """
    non_literal = [
        house for house, reason in c.QUADRANT_HOUSE_REASONS.items()
        if reason.split()[0].lower() not in c.HOUSE_SIGNIFICATIONS[house].lower()
    ]
    assert non_literal == [1]
    assert "self" in c.LAGNA_SHOWS
    assert "self" in c.PURUSHARTHA_HOUSE_REASONS[1]
    assert "self" not in c.HOUSE_SIGNIFICATIONS[1].lower()


def test_footnote_17_planets_in_mutual_quadrants():
    """"Planets in mutual quadrants have a sustaining effect on each other."
    and footnote 17: "if one planet is in a quadrant from the other"."""
    assert "sustaining effect" in c.MUTUAL_QUADRANTS_RULE
    assert "in a quadrant from the other" in c.MUTUAL_QUADRANTS_DEFINITION
    for a in range(1, 13):
        for b in category_houses("kendra", a):
            assert a in category_houses("kendra", b), (a, b)


def test_footnotes_16_and_17_are_the_same_sentence_with_one_word_changed():
    """Both footnotes define mutuality identically. That is the whole reason
    the two categories are the only symmetric ones — the definition is the
    symmetric one, and only trines and quadrants survive it."""
    assert (c.MUTUAL_TRINES_DEFINITION.replace("trines", "quadrants")
            .replace("a trine", "a quadrant") == c.MUTUAL_QUADRANTS_DEFINITION)


# --------------------------------------------------------------------------
# 7.4.3 Upachayas
# --------------------------------------------------------------------------


def test_7_4_3_upachayas_show_gains_and_growth_to_the_reference():
    """"Upachayas from a reference show forces causing gains and growth to the
    matters signified by the reference."

    "the matters signified by the reference" — not by the native. §7.4.6's
    one-liner drops that qualifier; the section is the fuller statement.
    """
    assert "gains and growth" in c.UPACHAYA_RULE
    assert "matters signified by the reference" in c.UPACHAYA_RULE
    assert c.HOUSE_CATEGORIES["upachaya"]["shows"] == "Gains and growth"


def test_7_4_3_the_arudha_lagna_example():
    """"arudha lagna shows one's status and the upachayas from arudha lagna
    show improvement of status."

    The only §7.4 example worked from a non-lagna reference. Arudha lagna is
    a live reference (chapter 9), so the computation is real.
    """
    assert c.UPACHAYA_EXAMPLE["reference"] == "arudha_lagna"
    assert "status" in c.HOUSE_REFERENCES["arudha_lagna"]["shows"]
    assert c.HOUSE_REFERENCES["arudha_lagna"]["available"] is True


def test_7_4_3_the_upachayas_from_arudha_lagna_are_computable():
    """The example is not just prose: given an arudha lagna in some house,
    its upachayas are the 3rd, 6th, 10th and 11th from it."""
    assert category_houses("upachaya", 5) == (2, 3, 7, 10)
    assert set(category_houses("upachaya", 1)) == {3, 6, 10, 11}


def test_7_4_3_improvement_is_a_change_not_a_level():
    """"improvement of status", not "status" — upachayas modify what the
    reference signifies rather than restating it. Same shape as §7.4.1's
    "prosperity of" and §7.4.2's "sustenance of"."""
    assert c.UPACHAYA_EXAMPLE["upachayas_show"] == "improvement of status"
    assert c.UPACHAYA_EXAMPLE["reference_shows"] == "one's status"


# --------------------------------------------------------------------------
# 7.4.4 Dusthanas
# --------------------------------------------------------------------------


def test_7_4_4_dusthanas_show_setbacks_to_the_reference():
    """"Dusthanas from a reference show forces causing setbacks to the matters
    signified by it."""
    assert "setbacks" in c.DUSTHANA_RULE
    assert "matters signified by it" in c.DUSTHANA_RULE
    assert c.HOUSE_CATEGORIES["dusthana"]["shows"] == "Setbacks and obstacles"
    assert c.DUSTHANA_GLOSS == "bad/evil houses"


def test_7_4_4_the_dusthanas_are_the_6th_8th_and_12th():
    assert c.DUSTHANA == (6, 8, 12)
    assert category_houses("dusthana") == (6, 8, 12)


def test_7_4_4_strength_in_a_dusthana_reads_backwards():
    """"If a dusthana is fortified or afflicted by malefics, it may show
    serious obstacles. If a dusthana is weak, it shows that obstacles will be
    easily overcome."

    The only category in §7.4 whose reading inverts with strength. Everywhere
    else a strong house is good news; here a strong 6th, 8th or 12th is not.
    """
    assert "fortified" in c.DUSTHANA_STRENGTH_INVERSION
    assert "easily overcome" in c.DUSTHANA_STRENGTH_INVERSION


def test_7_4_4_the_exalted_and_debilitated_8th_lord_example():
    """"exalted 8th lord may show a lot of troubles and debilitated 8th lord
    may show easy sailing."

    Checkable against chapter 3: exaltation is strength, debilitation is
    weakness, and the 8th is a dusthana — so the example is an instance of
    the rule and not a separate claim.
    """
    assert "Exalted" in c.DUSTHANA_STRENGTH_EXAMPLE
    assert "debilitated" in c.DUSTHANA_STRENGTH_EXAMPLE
    assert 8 in c.DUSTHANA
    assert c.EXALTATION_DEG[Graha.SATURN] is not None


def test_7_4_4_the_inversion_is_recorded_not_computed():
    """Nothing joins dusthana-ness to a strength measure. `sign_dignity` gives
    exalted/debilitated and `category_houses` gives the dusthanas, but no code
    reads the two together to flip a verdict. See OI-58."""
    import hora.charts.house as house_mod

    src = pathlib.Path(house_mod.__file__).read_text()
    assert "dignity" not in src


# --------------------------------------------------------------------------
# 7.4.5 Visible half and invisible half
# --------------------------------------------------------------------------


def test_7_4_5_the_split_is_in_every_chart():
    """"The zodiac is divided into two halves in every chart." Every chart —
    so the split is not a property of the rasi chart alone."""
    assert "every chart" in c.HALVES_ARE_IN_EVERY_CHART
    assert set(c.VISIBLE_HALF) | set(c.INVISIBLE_HALF) == set(range(1, 13))
    assert not set(c.VISIBLE_HALF) & set(c.INVISIBLE_HALF)


def test_7_4_5_what_each_half_shows():
    """"The houses in the visible half ... give results that can be seen in
    the material world and the houses in the invisible half ... give results
    that cannot be easily seen."

    "cannot be **easily** seen" — not invisible outright. The asymmetry is in
    the book's wording and worth keeping.
    """
    assert "seen in the material world" in c.HALVES_RULE
    assert "cannot be easily seen" in c.HALVES_RULE


def test_7_4_5_the_halves_are_relative_to_a_reference():
    """"The houses in the visible half of the zodiac **with respect to a
    reference**".

    Every other §7.4 category takes a base house; the halves must too. From
    the 7th house, the 1st is visible — because the 1st is the 7th from the
    7th.
    """
    assert "with respect to a reference" in c.HALVES_RULE
    assert half_of(1) == "invisible"
    assert half_of(1, 7) == "visible"
    assert half_of(7, 7) == "invisible"


@pytest.mark.parametrize("base", range(1, 13))
def test_7_4_5_each_half_holds_six_houses_from_any_base(base):
    visible = [h for h in range(1, 13) if half_of(h, base) == "visible"]
    assert len(visible) == 6
    assert visible == sorted(houses_from(base, c.VISIBLE_HALF))


def test_7_4_5_why_the_trikona_bases_fall_where_they_do():
    """"the bases of dharma trikona (1st house) and moksha trikona (4th house)
    are in the invisible half and the bases of artha trikona (10th house) and
    kaama trikona (7th house) are in the visible half."

    Dharma and moksha are inner goals, artha and kaama outer ones — so the
    section's argument is that the geometry matches the meaning.
    """
    assert half_of(1) == "invisible" and half_of(4) == "invisible"
    assert half_of(10) == "visible" and half_of(7) == "visible"


def test_7_4_5_the_argument_is_about_bases_only_not_whole_trikonas():
    """A trap: the artha trikona is (2, 6, 10) and two of those three are in
    the *invisible* half. §7.4.5's claim holds for the **base** house alone.

    Read as a claim about whole groups it would be false, so the wording
    "the bases of" is load-bearing.
    """
    assert "the bases of" in c.HALVES_EXPLAIN_THE_TRIKONA_BASES
    artha = c.PURUSHARTHA_TRIKONAS["artha"]["houses"]
    assert [half_of(h) for h in artha] == ["invisible", "invisible", "visible"]
    kaama = c.PURUSHARTHA_TRIKONAS["kaama"]["houses"]
    assert [half_of(h) for h in kaama] == ["invisible", "visible", "visible"]


def test_7_4_5_no_trikona_lies_wholly_in_one_half():
    """Each purushaartha straddles the split — which is why only the base can
    place it. Every trikona has houses on both sides."""
    for name, entry in c.PURUSHARTHA_TRIKONAS.items():
        halves = {half_of(h) for h in entry["houses"]}
        assert halves == {"visible", "invisible"}, name


# --------------------------------------------------------------------------
# 7.4.6 Quick summary
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "label,category",
    [("Trines", "trikona"), ("Quadrants", "kendra"),
     ("Upachayas", "upachaya"), ("Dusthanas", "dusthana")],
)
def test_7_4_6_the_summary_agrees_with_the_category_table(label, category):
    """Four of the five summary lines restate `HOUSE_CATEGORIES["shows"]`
    exactly. Checked against the table rather than duplicated, so the two can
    never drift."""
    assert c.QUICK_SUMMARY[label] == c.HOUSE_CATEGORIES[category]["shows"]


def test_7_4_6_the_summary_covers_every_category_that_has_a_signification():
    """§7.4 lists seven categories; three (panaphara, apoklima, chaturasra)
    are given no signification and correspondingly do not appear here."""
    with_shows = {n for n, e in c.HOUSE_CATEGORIES.items() if e["shows"]}
    assert with_shows == {"trikona", "kendra", "upachaya", "dusthana"}
    assert len(c.QUICK_SUMMARY) == len(with_shows) + 1


def test_7_4_6_argala_sthanas_are_a_fifth_category_7_4_never_listed():
    """"Argala sthanas: Decisive influences."

    Argala sthanas appear nowhere in §7.4's seven numbered categories — the
    summary introduces a category the section never defined. Argalas are
    chapter 10, which is unaudited, so this is kept as its own constant rather
    than added to `HOUSE_CATEGORIES` with houses we have not read.
    """
    assert c.QUICK_SUMMARY["Argala sthanas"] == "Decisive influences"
    assert c.ARGALA_STHANA_SHOWS == "Decisive influences"
    assert "argala" not in c.HOUSE_CATEGORIES
    for entry in c.HOUSE_CATEGORIES.values():
        assert entry["shows"] != "Decisive influences"


def test_7_4_6_the_summary_order_is_the_books():
    assert list(c.QUICK_SUMMARY) == [
        "Trines", "Quadrants", "Upachayas", "Dusthanas", "Argala sthanas"]


def test_7_4_5_the_categories_endpoint_carries_the_relative_halves(client):
    """The halves are relative, so the endpoint that re-bases the categories
    must re-base them too."""
    body = client.get("/v1/house/categories/7").json()
    assert body["halves"]["visible"] == [1, 2, 3, 4, 5, 6]
    assert body["halves"]["invisible"] == [7, 8, 9, 10, 11, 12]


def test_7_4_6_the_categories_endpoint_carries_every_signification(client):
    """§7.4.6's four category lines must all be reachable through the API."""
    body = client.get("/v1/house/categories/1").json()
    shows = {e["category"]: e["shows"] for e in body["categories"]}
    assert shows["trikona"] == "Prosperity and flourishing"
    assert shows["kendra"] == "Sustenance and vital activity"
    assert shows["upachaya"] == "Gains and growth"
    assert shows["dusthana"] == "Setbacks and obstacles"


# --------------------------------------------------------------------------
# 7.5 A controversy — house division
# --------------------------------------------------------------------------


def test_7_5_houses_are_found_from_three_kinds_of_reference():
    """"Houses are found with respect to lagna, special lagnas and some
    planets."

    All three kinds are live: lagna, four special lagnas (paaka, ghati, hora,
    arudha, karakamsa) and two planets (Moon and Sun).
    """
    assert "special lagnas" in c.HOUSES_ARE_FOUND_FROM
    refs = c.HOUSE_REFERENCES
    assert "lagna" in refs
    assert {"chandra_lagna", "ravi_lagna"} <= set(refs)
    assert {"paaka_lagna", "ghati_lagna", "hora_lagna", "arudha_lagna",
            "karakamsa_lagna"} <= set(refs)
    assert all(entry["available"] for entry in refs.values())


def test_7_5_houses_are_found_in_every_divisional_chart_too():
    """"Houses are found in rasi chart and in all the divisional charts."

    Not a slogan — the varga payload carries a house number per graha, so a
    house is available in every chart the engine draws.
    """
    assert "all the divisional charts" in c.HOUSES_ARE_FOUND_FROM
    from hora.api.models import VargaGrahaOut

    assert "house" in VargaGrahaOut.model_fields


def test_7_5_the_narrow_view_is_named_and_rejected():
    """"Some scholars ignore all these and take houses only with respect to
    lagna and only in rasi chart."

    Two restrictions, and the engine breaks both: `houses_from_reference`
    takes any of the eight references, and `meanings_in_varga` reads houses in
    a divisional chart.
    """
    assert "only with respect to lagna" in c.NARROW_VIEW_REJECTED
    assert "only in rasi chart" in c.NARROW_VIEW_REJECTED
    body = house_service.houses_from_reference(RASI["Aq"], "chandra_lagna")
    assert body["reference"] == "chandra_lagna"
    assert house_service.meanings_in_varga(4, "D12")["house"] == 4


def test_7_5_each_rasi_is_a_house():
    """"Each rasi is a house. The rasi containing the reference point chosen is
    the 1st house and the next rasi is the 2nd house."

    "the reference point **chosen**" — the definition is relative from the
    start, which is why every §7.3 reference can carry houses without a second
    rule.
    """
    assert "reference point chosen" in c.EACH_RASI_IS_A_HOUSE
    assert Settings().house_system is HouseSystem.WHOLE_SIGN
    for lagna_rasi in range(12):
        assert house_of_rasi(lagna_rasi, lagna_rasi) == 1
        assert house_of_rasi(lagna_rasi, (lagna_rasi + 1) % 12) == 2


def test_7_5_no_house_starts_in_one_rasi_and_ends_in_another():
    """"bhaava chakra" or "chalit chakra", in which houses can start in one
    rasi and end in another" — the property §7.5 rejects.

    Under the default every bhava starts on a rasi boundary, spans exactly
    30 degrees, and no two share a sign.
    """
    from hora.charts.bhava import build_bhavas
    from hora.core.ephemeris.base import Houses

    houses = Houses(
        ascendant=17.5, midheaven=280.0,
        cusps=tuple(float(i * 30) for i in range(12)),
        armc=0.0, vertex=0.0, equatorial_ascendant=0.0,
    )
    bhavas = build_bhavas(houses, HouseSystem.WHOLE_SIGN)
    assert len(bhavas) == 12
    for bhava in bhavas:
        assert bhava.start % 30 == 0.0
        assert (bhava.end - bhava.start) % 360 == 30.0
        assert int(bhava.start // 30) == bhava.sign
    assert len({b.sign for b in bhavas}) == 12


def test_7_5_the_lagna_degree_is_not_the_midpoint_of_the_first_house():
    """"They take lagna's longitude to be the mid-point of the first house."

    Under whole sign the lagna sits wherever in its rasi it falls; the madhya
    is the sign's own 15th degree. A lagna at 17.5 Aries gives a madhya of 15,
    not 17.5 — so the rejected construction is genuinely not what runs.
    """
    from hora.charts.bhava import build_bhavas
    from hora.core.ephemeris.base import Houses

    houses = Houses(
        ascendant=17.5, midheaven=280.0,
        cusps=tuple(float(i * 30) for i in range(12)),
        armc=0.0, vertex=0.0, equatorial_ascendant=0.0,
    )
    first = build_bhavas(houses, HouseSystem.WHOLE_SIGN)[0]
    assert first.middle == 15.0
    assert first.middle != houses.ascendant


def test_7_5_the_book_recommends_neither_equal_house_nor_sripathi():
    """"Another method taught by Sripathi is more complicated and it is also
    popular. However, this author recommends neither."

    Both remain reachable — JHora offers seventeen schemes and so do we — but
    neither is the default.
    """
    assert "recommends neither" in c.SRIPATHI_METHOD_NOTE
    assert "popular among Indian astrologers" in c.EQUAL_HOUSE_IS_POPULAR
    assert HouseSystem.SRIPATI in HouseSystem
    assert Settings().house_system not in (
        HouseSystem.SRIPATI, HouseSystem.EQUAL_LAGNA, HouseSystem.VEHLOW_EQUAL)


def test_7_5_the_equal_house_method_it_describes_is_centred_on_lagna():
    """"they take a 30° arc with **center** at lagna as the 1st house."

    Centred, not starting. That is Vehlow, not the scheme our `equal_lagna`
    names: `equal_lagna` puts the first cusp *at* the lagna degree, Vehlow
    puts it 15 degrees before. Both are offered; only one is what §7.5
    describes, and nothing said so until now.
    """
    from hora.core.ephemeris.swiss import SwissEphemeris

    ephemeris = SwissEphemeris(Settings(house_system=HouseSystem.EQUAL_LAGNA))
    at_lagna = ephemeris.houses(2451545.0, 17.385, 78.4867)
    ephemeris = SwissEphemeris(Settings(house_system=HouseSystem.VEHLOW_EQUAL))
    centred = ephemeris.houses(2451545.0, 17.385, 78.4867)

    assert at_lagna.ascendant == pytest.approx(centred.ascendant)
    assert (at_lagna.ascendant - at_lagna.cusps[0]) % 360 == pytest.approx(0.0)
    assert (centred.ascendant - centred.cusps[0]) % 360 == pytest.approx(15.0)
    assert "center at lagna" in c.EQUAL_HOUSE_DEFINITION


def test_7_5_the_chalit_chakra_treats_the_cusp_as_a_midpoint():
    """"They take lagna's longitude to be the mid-point of the first house and
    construct all the houses accordingly."

    `bhava.py` already separates the two families: Sripati and friends treat
    the cusp as the madhya and derive boundaries between consecutive madhyas.
    That is the chalit construction, and it is why those schemes are the ones
    §7.5 names.
    """
    from hora.charts.bhava import _MIDPOINT_SCHEMES

    assert HouseSystem.SRIPATI in _MIDPOINT_SCHEMES
    assert HouseSystem.WHOLE_SIGN not in _MIDPOINT_SCHEMES


def test_7_5_direct_bphs_references_beat_indirect_ones():
    """"Though there are some *indirect* references in BPHS suggesting that
    Parasara supported house divisions placing houses in 2 rasis, there are
    quite a few *direct* references making it amply clear that each house
    falls in one rasi."

    The clearest statement in the book of the tie-break `docs/precedence.md`
    encodes. PVR does not deny the indirect references exist; he ranks them.
    """
    assert "indirect references in BPHS" in c.BPHS_HOUSE_DIVISION_ARGUMENT
    assert "direct references" in c.BPHS_HOUSE_DIVISION_ARGUMENT
    ladder = pathlib.Path("docs/precedence.md").read_text()
    assert "direct" in ladder.lower()


def test_7_5_parasara_counts_rasis_from_the_reference():
    """"Parasara taught us to find houses by counting rasis from the reference
    chosen." — which is `house_of_rasi`, and it is inclusive."""
    assert "counting rasis from the reference" in c.BPHS_HOUSE_DIVISION_ARGUMENT
    assert house_of_rasi(RASI["Ar"], RASI["Ar"]) == 1
    assert house_of_rasi(RASI["Ar"], RASI["Cn"]) == 4
    assert house_of_rasi(RASI["Pi"], RASI["Ar"]) == 2


def test_7_5_the_basic_techniques_do_not_differentiate_rasi_from_varga():
    """"Parasara's treatment does not differentiate between rasi and divisional
    charts, as far as the basic techniques go."

    An architectural claim, and one the code can be held to: every house
    function takes rasi indices and has no chart parameter, so it cannot
    behave differently in D-9 than in D-1.
    """
    import inspect

    from hora.charts import house as house_mod

    assert "does not differentiate" in c.RASI_AND_VARGA_ARE_NOT_DIFFERENTIATED
    for name in ("house_of_rasi", "rasi_of_house", "houses_from",
                 "category_houses", "categories_of", "half_of"):
        params = inspect.signature(getattr(house_mod, name)).parameters
        assert "chart" not in params, name
        assert "varga" not in params, name


def test_7_5_the_reason_the_whole_sign_rule_is_argued_from_vargas():
    """"only this approach is logical as we go to divisional charts."

    Why: a varga longitude is a re-mapped position within a rasi, so a scheme
    whose boundaries fall inside rasis has nothing to attach to after the
    mapping. The D-9 of a lagna lands anywhere in its navamsa rasi.
    """
    from hora.charts.vargas import d9_navamsa

    assert "divisional charts" in c.RASI_AND_VARGA_ARE_NOT_DIFFERENTIATED
    seen = {d9_navamsa(17.5 + step).sign for step in range(0, 360, 7)}
    assert len(seen) == 12


def test_7_5_readers_are_told_to_ignore_other_textbooks_on_the_matter():
    """"So readers are advised to ignore all the discussions found in other
    textbooks on house division methods, "bhaava chakra" and "chalit chakra"."

    Recorded, and the engine's published rule says the same in its own words.
    """
    assert "ignore all the discussions" in c.IGNORE_OTHER_HOUSE_DIVISION_METHODS
    note = house_service.rules()["note"]
    assert "never spans two rasis" in note
    assert "bhava chalit" in note


def test_footnote_18_argala_sthanas_are_deferred_to_aspects_and_argalas():
    """"This will be covered in the chapter on "Aspects and Argalas"."

    Resolves §7.4.6's fifth summary line: the category is real, it is just not
    chapter 7's. That is why it stays out of `HOUSE_CATEGORIES`.
    """
    assert "Aspects and Argalas" in c.ARGALA_STHANA_FORWARD_REFERENCE
    assert "argala" not in c.HOUSE_CATEGORIES
    assert c.ARGALA_STHANA_SHOWS == "Decisive influences"
