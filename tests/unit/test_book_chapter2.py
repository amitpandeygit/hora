"""Every classification in Chapter 2 of PVR Narasimha Rao's textbook.

Source: "Vedic Astrology: An Integrated Approach", Chapter 2 (Rasis),
book pages 21-27. Chapter 2 is a data chapter — no formulas, no worked
examples — so these tests assert the tables themselves.

Section 2.3 (Indications) is editorial content, not calculation. It lives in
data/content/ and is tested in tests/content/.
"""
import pytest

from hora.core import const as c

A = c.RASI_ABBR


def group(values, target):
    """Abbreviations of the rasis whose attribute equals ``target``."""
    return [A[i] for i in range(12) if values[i] == target]


# --------------------------------------------------------------------------
# 2.2.1 Limbs of the kaala purusha
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "rasi,limb",
    list(enumerate([
        "head", "face", "arms", "heart", "stomach", "hip",
        "space below navel", "private parts", "thighs", "knees", "ankles", "feet",
    ])),
)
def test_limbs_of_vishnu(rasi, limb):
    assert c.RASI_LIMB[rasi] == limb


# --------------------------------------------------------------------------
# 2.2.2 Odd and even
# --------------------------------------------------------------------------

def test_odd_and_even_rasis():
    assert group(c.RASI_IS_ODD, True) == ["Ar", "Ge", "Le", "Li", "Sg", "Aq"]
    assert group(c.RASI_IS_ODD, False) == ["Ta", "Cn", "Vi", "Sc", "Cp", "Pi"]


# --------------------------------------------------------------------------
# 2.2.3 Odd-footed and even-footed
# --------------------------------------------------------------------------

def test_odd_footed_and_even_footed():
    assert group(c.RASI_IS_ODD_FOOTED, True) == ["Ar", "Ta", "Ge", "Li", "Sc", "Sg"]
    assert group(c.RASI_IS_ODD_FOOTED, False) == ["Cn", "Le", "Vi", "Cp", "Aq", "Pi"]


def test_odd_footed_is_not_the_same_split_as_odd():
    """Easy to conflate; the book gives two different six-six divisions."""
    assert c.RASI_IS_ODD_FOOTED != c.RASI_IS_ODD


# --------------------------------------------------------------------------
# 2.2.4 Movable, fixed and dual
# --------------------------------------------------------------------------

def test_modalities_and_their_deities():
    assert group(c.RASI_MODALITY, 0) == ["Ar", "Cn", "Li", "Cp"]
    assert group(c.RASI_MODALITY, 1) == ["Ta", "Le", "Sc", "Aq"]
    assert group(c.RASI_MODALITY, 2) == ["Ge", "Vi", "Sg", "Pi"]
    assert c.MODALITY_DEITY == ["Brahma", "Shiva", "Vishnu"]
    assert c.MODALITY_NAMES == ["chara", "sthira", "dwiswabhava"]


# --------------------------------------------------------------------------
# 2.2.5 Five elements
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "element,rasis",
    [(0, ["Ar", "Le", "Sg"]), (1, ["Ta", "Vi", "Cp"]),
     (2, ["Ge", "Li", "Aq"]), (3, ["Cn", "Sc", "Pi"])],
)
def test_elements(element, rasis):
    assert group(c.RASI_ELEMENT, element) == rasis


def test_element_names_match_the_book():
    assert c.ELEMENT_NAMES == ["fire", "earth", "air", "water"]
    assert c.ELEMENT_NAMES_SA == ["agni", "bhoo", "vaayu", "jala"]


# --------------------------------------------------------------------------
# 2.2.6 Pitta, vaata, kapha
# --------------------------------------------------------------------------

def test_doshas_follow_the_book_not_conventional_ayurveda():
    """See docs/book-deviations.md D-1.

    The book puts earthy signs in vaata and watery signs in kapha. Deriving
    from the classical compositions it states (vaata = air + ether,
    kapha = earth + water) would give a different answer. The book wins.
    """
    assert group(c.RASI_DOSHA, 0) == ["Ar", "Le", "Sg"]      # pitta, fiery
    assert group(c.RASI_DOSHA, 1) == ["Ta", "Vi", "Cp"]      # vaata, earthy
    assert group(c.RASI_DOSHA, 2) == ["Cn", "Sc", "Pi"]      # kapha, watery
    assert group(c.RASI_DOSHA, 3) == ["Ge", "Li", "Aq"]      # mixed, airy
    assert c.DOSHA_NAMES == ["pitta", "vaata", "kapha", "mixed"]


# --------------------------------------------------------------------------
# 2.2.7 Trigunas
# --------------------------------------------------------------------------

def test_gunas():
    assert group(c.RASI_GUNA, 0) == ["Cn", "Le", "Sg", "Pi"]   # sattwa
    assert group(c.RASI_GUNA, 1) == ["Ar", "Ta", "Li", "Sc"]   # rajas
    assert group(c.RASI_GUNA, 2) == ["Ge", "Vi", "Cp", "Aq"]   # tamas
    assert c.GUNA_NAMES == ["sattwa", "rajas", "tamas"]


def test_every_rasi_has_exactly_one_guna():
    assert sorted(c.RASI_GUNA.count(g) for g in range(3)) == [4, 4, 4]


# --------------------------------------------------------------------------
# 2.2.8 Directions
# --------------------------------------------------------------------------

def test_directions():
    assert group(c.RASI_DIRECTION, 0) == ["Ar", "Le", "Sg"]    # east
    assert group(c.RASI_DIRECTION, 1) == ["Ta", "Vi", "Cp"]    # south
    assert group(c.RASI_DIRECTION, 2) == ["Ge", "Li", "Aq"]    # west
    assert group(c.RASI_DIRECTION, 3) == ["Cn", "Sc", "Pi"]    # north


# --------------------------------------------------------------------------
# 2.2.9 Colours
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "rasi,color",
    [(0, "blood-red color"), (1, "white"), (2, "grass green"), (3, "pale red"),
     (4, "white"), (5, "variegated"), (6, "black"), (7, "reddish brown"),
     (8, "the color of the husk of grass"), (9, "variegated"),
     (10, "brown color (that of a mongoose)"),
     (11, "cream color or the color of fish")],
)
def test_colors(rasi, color):
    """Book 2.2.9, in its own wording and American spelling."""
    assert c.RASI_COLOR[rasi] == color


def test_colours_keep_the_books_spelling_not_ours():
    """The book writes "color". Anglicising it would be a silent edit."""
    assert not any("colour" in v for v in c.RASI_COLOR)


def test_every_rasi_has_a_colour():
    assert len(c.RASI_COLOR) == 12
    assert all(c.RASI_COLOR)


# --------------------------------------------------------------------------
# 2.2.10 Day and night
# --------------------------------------------------------------------------

def test_night_and_day_rasis():
    assert group(c.RASI_IS_NIGHT, True) == ["Ar", "Ta", "Ge", "Cn", "Sg", "Cp"]
    assert group(c.RASI_IS_NIGHT, False) == ["Le", "Vi", "Li", "Sc", "Aq", "Pi"]


def test_book_claim_each_two_sign_lord_owns_one_day_and_one_night_sign():
    """2.2.10 asserts this outright, so it is checkable against our lordships."""
    from collections import defaultdict

    owned = defaultdict(list)
    for r in range(12):
        owned[int(c.RASI_LORD[r])].append(r)
    for lord, rasis in owned.items():
        if len(rasis) == 2:
            assert {c.RASI_IS_NIGHT[r] for r in rasis} == {True, False}, lord


def test_book_claim_moon_governs_night_signs_and_sun_governs_day_signs():
    assert c.RASI_IS_NIGHT[c.Rasi.CANCER] is True     # Moon's sign
    assert c.RASI_IS_NIGHT[c.Rasi.LEO] is False       # Sun's sign


# --------------------------------------------------------------------------
# 2.2.11 Rising
# --------------------------------------------------------------------------

def test_rising_modes():
    assert group(c.RASI_RISING, 0) == ["Ge", "Le", "Vi", "Li", "Sc", "Aq"]
    assert group(c.RASI_RISING, 1) == ["Ar", "Ta", "Cn", "Sg", "Cp"]
    assert group(c.RASI_RISING, 2) == ["Pi"]          # rises both ways
    assert c.RISING_NAMES == ["seershodaya", "prishthodaya", "ubhayodaya"]


# --------------------------------------------------------------------------
# 2.2.12 Varna
# --------------------------------------------------------------------------

def test_varnas():
    assert group(c.RASI_VARNA, 0) == ["Cn", "Sc", "Pi"]     # brahmana, watery
    assert group(c.RASI_VARNA, 1) == ["Ar", "Le", "Sg"]     # kshatriya, fiery
    assert group(c.RASI_VARNA, 2) == ["Ta", "Vi", "Cp"]     # vaisya, earthy
    assert group(c.RASI_VARNA, 3) == ["Ge", "Li", "Aq"]     # sudra, airy


def test_varna_follows_the_element_grouping_exactly():
    """2.2.5 and 2.2.12 must agree; this catches a drift between the tables."""
    mapping = {}
    for i in range(12):
        mapping.setdefault(c.RASI_ELEMENT[i], set()).add(c.RASI_VARNA[i])
    assert all(len(v) == 1 for v in mapping.values())


# --------------------------------------------------------------------------
# Table completeness
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "table",
    ["RASI_LIMB", "RASI_IS_ODD", "RASI_IS_ODD_FOOTED", "RASI_MODALITY",
     "RASI_ELEMENT", "RASI_DOSHA", "RASI_GUNA", "RASI_DIRECTION",
     "RASI_COLOR", "RASI_IS_NIGHT", "RASI_RISING", "RASI_VARNA"],
)
def test_every_attribute_table_covers_all_twelve_rasis(table):
    assert len(getattr(c, table)) == 12
