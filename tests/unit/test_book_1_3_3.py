"""§1.3.3 Bhavas (houses) — the definition, the wrap, and Exercise 2.

The arithmetic has been right since chapter 7. What this section adds is the
*vocabulary*: that a house is called a bhava, that the count wraps from Pisces
to Aries, and — the consequential one — that an unspecified reference means
the lagna. Every function in `charts/house.py` defaults to the lagna, and this
is the sentence that licenses it.
"""
import pytest

from hora.charts.house import house_of_rasi, houses_from, rasi_of_house
from hora.core import const as c
from hora.services import house_service

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
R = {name: i for i, name in enumerate(ABBR)}


# --------------------------------------------------------------------------
# What a house is
# --------------------------------------------------------------------------

def test_a_house_is_called_a_bhava():
    """"Another important concept is 'house' (Sanskrit name: bhava)"."""
    assert c.BHAVA_NAME == "bhava"
    assert house_service.rules()["definition"]["sanskrit"] == "bhava"


def test_the_definition_is_the_books_wording():
    text = c.HOUSE_DEFINITION
    assert "Starting from the rasi occupied by the selected reference point" in text
    assert "proceeding in the regular order across the zodiac" in text
    assert "the rasi containing the reference point chosen is the 1st house" in text


def test_the_reference_point_is_always_the_first_house():
    for rasi in range(12):
        assert house_of_rasi(rasi, rasi) == 1
        assert rasi_of_house(rasi, 1) == rasi


def test_the_count_wraps_from_pisces_to_aries():
    """"Just remember that when we encounter Pisces, we go to Aries after it."

    The one step a reader gets wrong, so it is stated and tested.
    """
    assert "Pisces" in c.HOUSE_ORDER_WRAPS and "Aries" in c.HOUSE_ORDER_WRAPS
    # From Pisces, the 2nd house is Aries.
    assert rasi_of_house(R["Pi"], 2) == R["Ar"]
    # And a reference late in the zodiac still yields twelve distinct rasis.
    signs = [entry["rasi"] for entry in houses_from(1, 12)] if False else [
        rasi_of_house(R["Aq"], h) for h in range(1, 13)
    ]
    assert sorted(signs) == list(range(12))


@pytest.mark.parametrize("reference", range(12))
def test_twelve_houses_cover_every_rasi_exactly_once(reference):
    signs = [rasi_of_house(reference, h) for h in range(1, 13)]
    assert sorted(signs) == list(range(12))
    for house, sign in enumerate(signs, start=1):
        assert house_of_rasi(reference, sign) == house


# --------------------------------------------------------------------------
# The default reference
# --------------------------------------------------------------------------

def test_an_unspecified_reference_means_the_lagna():
    """"If no reference point is specified when houses are mentioned, it means
    that lagna is used as the reference."

    This is why every reference argument in charts/house.py defaults to the
    lagna. Recorded so the default is traceable to the book rather than to
    convention.
    """
    assert c.HOUSE_DEFAULT_REFERENCE == "lagna"
    rule = c.HOUSE_DEFAULT_REFERENCE_RULE
    assert "no reference point is specified" in rule
    assert "lagna is used as the reference" in rule

    definition = house_service.rules()["definition"]
    assert definition["default_reference"] == "lagna"
    assert definition["default_reference_rule"] == rule


def test_lagna_and_the_special_lagnas_are_the_common_references():
    """"the reference points most commonly employed are lagna and special
    lagnas"."""
    assert c.HOUSE_COMMON_REFERENCES == ("lagna", "special lagnas")
    available = {k for k, v in c.HOUSE_REFERENCES.items() if v["available"]}
    assert "lagna" in available
    # The special lagnas chapter 5 computes are all usable as references.
    assert {"ghati_lagna", "hora_lagna"} <= available


# --------------------------------------------------------------------------
# The section's worked example — horalagna in Cancer
# --------------------------------------------------------------------------

#: "If, for example, horalagna is in Cn, first house with respect to horalagna
#: is in Cn. Second house is in Le. Third house is in Vi. Ninth house is in Pi.
#: Tenth house is in Ar. Eleventh house is in Ta. Twelfth house is in Ge."
HORALAGNA_EXAMPLE = {1: "Cn", 2: "Le", 3: "Vi", 9: "Pi", 10: "Ar", 11: "Ta",
                     12: "Ge"}


@pytest.mark.parametrize("house,rasi", sorted(HORALAGNA_EXAMPLE.items()))
def test_the_horalagna_example(house, rasi):
    assert rasi_of_house(R["Cn"], house) == R[rasi]
    assert house_of_rasi(R["Cn"], R[rasi]) == house


def test_the_horalagna_example_crosses_the_wrap():
    """The 10th from Cancer is Aries, so the example itself exercises the wrap."""
    assert rasi_of_house(R["Cn"], 9) == R["Pi"]
    assert rasi_of_house(R["Cn"], 10) == R["Ar"]


# --------------------------------------------------------------------------
# Exercise 2
# --------------------------------------------------------------------------

#: "Lagna is in Cn, Sun is in Ar, Moon is in Ta and Mars is in Cp."
EXERCISE_2_CHART = {"Lagna": "Cn", "Sun": "Ar", "Moon": "Ta", "Mars": "Cp"}

#: (1) "No reference is mentioned. So reference is lagna (Cn). Sun in Ar: 10th
#: house. Moon in Ta: 11th house. Mars in Cp: 7th house."
EXERCISE_2_FROM_LAGNA = {"Sun": 10, "Moon": 11, "Mars": 7}

#: (2) "Sun: 12th house. Moon: 1st house. Mars: 9th house."
EXERCISE_2_FROM_MOON = {"Sun": 12, "Moon": 1, "Mars": 9}


@pytest.mark.parametrize("graha,house", sorted(EXERCISE_2_FROM_LAGNA.items()))
def test_exercise_2_part_1(graha, house):
    """No reference given, so the lagna is used — the rule above in action."""
    reference = R[EXERCISE_2_CHART["Lagna"]]
    assert house_of_rasi(reference, R[EXERCISE_2_CHART[graha]]) == house


@pytest.mark.parametrize("graha,house", sorted(EXERCISE_2_FROM_MOON.items()))
def test_exercise_2_part_2(graha, house):
    """"Repeat the exercise, taking Moon as the reference point"."""
    reference = R[EXERCISE_2_CHART["Moon"]]
    assert house_of_rasi(reference, R[EXERCISE_2_CHART[graha]]) == house


def test_exercise_2_the_moon_is_its_own_first_house():
    """Part 2's giveaway: the reference always occupies the 1st."""
    assert EXERCISE_2_FROM_MOON["Moon"] == 1


def test_exercise_2_changing_the_reference_changes_every_house():
    """The two parts must not agree anywhere except by arithmetic."""
    lagna = R[EXERCISE_2_CHART["Lagna"]]
    moon = R[EXERCISE_2_CHART["Moon"]]
    for graha in ("Sun", "Moon", "Mars"):
        target = R[EXERCISE_2_CHART[graha]]
        assert house_of_rasi(lagna, target) != house_of_rasi(moon, target)


def test_exercise_2_through_the_service():
    """The same answers through /v1/house/from, for both references."""
    for reference_name, expected in (
        ("Lagna", EXERCISE_2_FROM_LAGNA), ("Moon", EXERCISE_2_FROM_MOON),
    ):
        reference = R[EXERCISE_2_CHART[reference_name]]
        key = "lagna" if reference_name == "Lagna" else "chandra_lagna"
        payload = house_service.houses_from_reference(reference, key)
        by_rasi = {row["rasi"]: row["house"] for row in payload["houses"]}
        for graha, house in expected.items():
            assert by_rasi[R[EXERCISE_2_CHART[graha]]] == house, graha
