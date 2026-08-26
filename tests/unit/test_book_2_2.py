"""Section 2.2, Characteristics of Rasis — §2.2.1 through §2.2.5.

Every membership list is transcribed from the book and asserted by name, not
derived from an index formula. Three of these five partitions look like they
should follow from the sign number and two of them do not:

  - §2.2.2 odd/even alternates, so it *is* index % 2.
  - §2.2.3 odd-footed does **not**: Ar, Ta, Ge, Li, Sc, Sg — the first three
    of each half of the zodiac. Taurus is an even rasi and an odd-footed one.
  - §2.2.4 and §2.2.5 cycle by 3 and by 4, which do follow, but are still
    written out so a wrong cycle cannot hide behind a matching formula.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.content.store import get_store
from hora.core import const as c

client = TestClient(app)

A = list(c.RASI_ABBR)


def rasis(*abbr: str) -> list[int]:
    """Indices for the book's two-letter abbreviations."""
    return [A.index(x) for x in abbr]


# --------------------------------------------------------------------------
# 2.2.1 Limbs of Vishnu
# --------------------------------------------------------------------------

#: "Aries is the head. Taurus is the face. ..." in the book's own order.
LIMBS = [
    ("Ar", "head"), ("Ta", "face"), ("Ge", "arms"), ("Cn", "heart"),
    ("Le", "stomach"), ("Vi", "hip"), ("Li", "space below navel"),
    ("Sc", "private parts"), ("Sg", "thighs"), ("Cp", "knees"),
    ("Aq", "ankles"), ("Pi", "feet"),
]


@pytest.mark.parametrize("abbr,limb", LIMBS)
def test_2_2_1_each_limb(abbr, limb):
    assert c.RASI_LIMB[A.index(abbr)] == limb


def test_2_2_1_the_zodiac_is_vishnus_body():
    """"The whole zodiac is nothing but a manifestation of Lord Vishnu's
    body."""
    assert "Lord Vishnu's body" in c.ZODIAC_AS_VISHNU


def test_2_2_1_the_mapping_applies_to_the_native():
    """"Because we are all part of the Supreme energy governing this world,
    the above mapping applies to us too."""
    assert "applies to us too" in c.LIMB_APPLIES_TO_NATIVE


def test_2_2_1_the_two_worked_examples():
    """"we should pay attention to Leo for analyzing stomach problems and to
    Pisces for analyzing problems related to feet"."""
    assert c.RASI_LIMB[A.index("Le")] == "stomach"
    assert c.RASI_LIMB[A.index("Pi")] == "feet"


def test_2_2_1_every_limb_is_distinct():
    assert len(set(c.RASI_LIMB)) == 12


# --------------------------------------------------------------------------
# 2.2.2 Odd and Even
# --------------------------------------------------------------------------

ODD = ("Ar", "Ge", "Le", "Li", "Sg", "Aq")
EVEN = ("Ta", "Cn", "Vi", "Sc", "Cp", "Pi")


def test_2_2_2_the_odd_rasis():
    """"Ar, Ge, Le, Li, Sg and Aq are called odd rasis."""
    assert [i for i in range(12) if c.RASI_IS_ODD[i]] == rasis(*ODD)


def test_2_2_2_the_even_rasis():
    """"Ta, Cn, Vi, Sc, Cp and Pi are called even rasis."""
    assert [i for i in range(12) if not c.RASI_IS_ODD[i]] == rasis(*EVEN)


def test_2_2_2_four_names_for_each_half():
    """"odd rasis or vishama rasis or oja rasis. They are also known as male
    rasis." — four names, not two."""
    assert c.ODD_EVEN_NAMES[0] == ["odd", "vishama", "oja", "male"]
    assert c.ODD_EVEN_NAMES[1] == ["even", "sama", "yugma", "female"]


def test_2_2_2_what_the_division_is_used_for():
    """"This division is used in some dasas and in the determination of the
    sex of children."""
    assert "sex of children" in c.ODD_EVEN_USE
    assert "dasas" in c.ODD_EVEN_USE


def test_2_2_2_the_two_halves_partition_the_zodiac():
    assert len(rasis(*ODD)) == len(rasis(*EVEN)) == 6
    assert set(rasis(*ODD)) | set(rasis(*EVEN)) == set(range(12))


# --------------------------------------------------------------------------
# 2.2.3 Odd-footed and Even-footed
# --------------------------------------------------------------------------

ODD_FOOTED = ("Ar", "Ta", "Ge", "Li", "Sc", "Sg")
EVEN_FOOTED = ("Cn", "Le", "Vi", "Cp", "Aq", "Pi")


def test_2_2_3_the_odd_footed_rasis():
    """"Ar, Ta, Ge, Li, Sc and Sg are called odd-footed rasis."""
    assert [i for i in range(12) if c.RASI_IS_ODD_FOOTED[i]] == rasis(*ODD_FOOTED)


def test_2_2_3_the_even_footed_rasis():
    """"Cn, Le, Vi, Cp, Aq and Pi are called even-footed rasis."""
    assert [i for i in range(12) if not c.RASI_IS_ODD_FOOTED[i]] == rasis(*EVEN_FOOTED)


def test_2_2_3_three_names_for_each_half():
    """"odd-footed rasis or vishamapada rasis or ojapada rasis."

    Three, where 2.2.2 gives four — there is no male/female pair here.
    """
    assert c.FOOTED_NAMES[0] == ["odd-footed", "vishamapada", "ojapada"]
    assert c.FOOTED_NAMES[1] == ["even-footed", "samapada", "yugmapada"]
    assert len(c.FOOTED_NAMES[0]) == 3


def test_2_2_3_is_a_different_partition_from_2_2_2():
    """The trap. Taurus is an *even* rasi but an *odd-footed* one, and Leo is
    an odd rasi but even-footed.

    The two splits disagree on exactly four signs — and those four are
    precisely the sthira rasis of 2.2.4. Nothing in the book says so; it falls
    out of the two lists, and it is asserted here because it is the cheapest
    way to catch either list being mistyped.
    """
    assert not c.RASI_IS_ODD[A.index("Ta")]
    assert c.RASI_IS_ODD_FOOTED[A.index("Ta")]
    assert c.RASI_IS_ODD[A.index("Le")]
    assert not c.RASI_IS_ODD_FOOTED[A.index("Le")]
    disagree = [i for i in range(12) if c.RASI_IS_ODD[i] != c.RASI_IS_ODD_FOOTED[i]]
    assert [A[i] for i in disagree] == ["Ta", "Le", "Sc", "Aq"]
    sthira = c.MODALITY_NAMES.index("sthira")
    assert disagree == [i for i in range(12) if c.RASI_MODALITY[i] == sthira]


def test_2_2_3_is_the_first_three_of_each_half_of_the_zodiac():
    """Odd-footed is Ar-Ta-Ge and Li-Sc-Sg — not an alternating pattern."""
    assert rasis(*ODD_FOOTED) == [0, 1, 2, 6, 7, 8]


def test_2_2_3_names_only_dasas_as_its_use():
    """"This division is used in some dasas." — no mention of sex of children,
    unlike 2.2.2."""
    assert c.FOOTED_USE == "This division is used in some dasas."
    assert "children" not in c.FOOTED_USE


# --------------------------------------------------------------------------
# 2.2.4 Movable, Fixed and Dual
# --------------------------------------------------------------------------

MODALITIES = [
    (("Ar", "Cn", "Li", "Cp"), "chara", "movable", "Brahma", "Creator"),
    (("Ta", "Le", "Sc", "Aq"), "sthira", "fixed", "Shiva", "Destroyer"),
    (("Ge", "Vi", "Sg", "Pi"), "dwiswabhava", "dual", "Vishnu", "Sustainer"),
]


@pytest.mark.parametrize("signs,sanskrit,english,deity,role", MODALITIES)
def test_2_2_4_each_modality(signs, sanskrit, english, deity, role):
    index = c.MODALITY_NAMES.index(sanskrit)
    assert [i for i in range(12) if c.RASI_MODALITY[i] == index] == rasis(*signs)
    assert c.MODALITY_NAMES_EN[index] == english
    assert c.MODALITY_DEITY[index] == deity
    assert c.MODALITY_DEITY_ROLE[index] == role


def test_2_2_4_the_natures():
    """"Their nature is to move and to be dynamic." / "to be stable and
    constant." / "They are stable sometimes and dynamic sometimes."""
    chara, sthira, dual = c.MODALITY_NATURE
    assert "move" in chara and "dynamic" in chara
    assert "stable and constant" in sthira
    assert "sometimes" in dual


def test_2_2_4_footnote_3_the_trinity():
    """"Brahma, Vishnu and Shiva together form the Trinity of Hindu Gods.
    Brahma creates the world. Vishnu sustains it. Shiva destroys it."""
    assert "Trinity" in c.TRINITY_NOTE
    for name in ("Brahma", "Vishnu", "Shiva"):
        assert name in c.TRINITY_NOTE


def test_2_2_4_the_deity_roles_agree_with_the_footnote():
    """Brahma creates, Vishnu sustains, Shiva destroys — the roles in the body
    text and the footnote must not drift apart."""
    pairs = dict(zip(c.MODALITY_DEITY, c.MODALITY_DEITY_ROLE))
    assert pairs == {"Brahma": "Creator", "Shiva": "Destroyer", "Vishnu": "Sustainer"}


def test_2_2_4_the_dual_deity_is_vishnu_not_the_zodiac_of_2_2_1():
    """§2.2.1 calls the *whole* zodiac Vishnu's body; §2.2.4 gives Vishnu only
    the four dual signs. Both are true and neither should be read as the
    other."""
    dual = c.MODALITY_NAMES.index("dwiswabhava")
    assert c.MODALITY_DEITY[dual] == "Vishnu"
    assert len([i for i in range(12) if c.RASI_MODALITY[i] == dual]) == 4


def test_2_2_4_the_three_modalities_partition_the_zodiac():
    seen = [rasis(*m[0]) for m in MODALITIES]
    assert sorted(i for group in seen for i in group) == list(range(12))


# --------------------------------------------------------------------------
# 2.2.5 Rasis & Five Elements
# --------------------------------------------------------------------------

ELEMENTS = [
    (("Ar", "Le", "Sg"), "fire", "agni"),
    (("Ta", "Vi", "Cp"), "earth", "bhoo"),
    (("Ge", "Li", "Aq"), "air", "vaayu"),
    (("Cn", "Sc", "Pi"), "water", "jala"),
]


@pytest.mark.parametrize("signs,english,sanskrit", ELEMENTS)
def test_2_2_5_each_element(signs, english, sanskrit):
    index = c.ELEMENT_NAMES.index(english)
    assert [i for i in range(12) if c.RASI_ELEMENT[i] == index] == rasis(*signs)
    assert c.ELEMENT_NAMES_SA[index] == sanskrit


def test_2_2_5_the_five_in_the_books_prose_order():
    """"this world is made up of 5 elements - fire, water, air, earth and
    ether." That order is not RASI_ELEMENT's index order."""
    assert c.FIVE_ELEMENTS_BOOK_ORDER == ["fire", "water", "air", "earth", "ether"]
    assert c.FIVE_ELEMENTS_BOOK_ORDER[:4] != c.ELEMENT_NAMES


def test_2_2_5_each_element_is_defined_by_a_state():
    """"Water is a substance with a flexible state. Air is a substance with a
    varying state. Earth is a substance with a constant and solid state. Fire
    is a substance that transforms the state of things. Ether is something
    that is present everywhere."""
    d = c.ELEMENT_DEFINITIONS
    assert "flexible state" in d["water"]
    assert "varying state" in d["air"]
    assert "constant and solid state" in d["earth"]
    assert "transforms the state of things" in d["fire"]
    assert "present everywhere" in d["ether"]
    assert set(d) == set(c.FIVE_ELEMENTS_BOOK_ORDER)


def test_2_2_5_ether_belongs_to_every_rasi_and_is_not_an_index():
    """"The 5th element of aakaasa or ether is present in every rasi."

    So a rasi's element is one of four, while ether is universal. Making
    ether a fifth index would take three signs away from another element.
    """
    assert c.ETHER_NAME == "ether"
    assert c.ETHER_NAME_SA == "aakaasa"
    assert "every rasi" in c.ETHER_IN_EVERY_RASI
    assert len(c.ELEMENT_NAMES) == 4
    assert "ether" not in c.ELEMENT_NAMES
    assert len(set(c.RASI_ELEMENT)) == 4


def test_2_2_5_the_elements_underlie_everything():
    """"These 5 elements are behind every material substance, every action,
    every thought, every emotion and every happening in this universe."""
    assert "every thought" in c.ELEMENTS_UNDERLIE_EVERYTHING


def test_2_2_5_the_four_elements_partition_the_zodiac():
    seen = [rasis(*e[0]) for e in ELEMENTS]
    assert sorted(i for group in seen for i in group) == list(range(12))
    assert all(len(g) == 3 for g in seen)


# --------------------------------------------------------------------------
# 2.2.5's worked examples — licence-gated, like section 2.3
# --------------------------------------------------------------------------

FIFTH_HOUSE = [
    ("fire", "angry, aggressive or determined"),
    ("earth", "balanced, logical and stable"),
    ("air", "unstable and wandering emotions"),
    ("water", "imaginative and creative mind"),
]


@pytest.mark.parametrize("element,phrase", FIFTH_HOUSE)
def test_2_2_5_the_fifth_house_examples_are_stored(element, phrase):
    """"The 5th house in a fiery sign may show a normally angry, aggressive or
    determined person." and the three that follow.

    These are PVR's interpretation, so they live in the content store behind
    the same licence gate as section 2.3, not in the calculation constants.
    See OI-12.
    """
    index = c.ELEMENT_NAMES.index(element)
    entries = get_store().get("element", index)
    assert entries, element
    assert phrase in entries[0].verbatim


def test_2_2_5_the_fifth_house_examples_are_licence_gated():
    entries = get_store().get("element", 0)
    assert entries[0].licence_status == "unconfirmed"


def test_2_2_5_there_is_no_ether_example():
    """The book gives four, one per element a sign can have. Ether is in every
    rasi, so there is no fifth reading to give."""
    assert get_store().get("element", 4) == []


# --------------------------------------------------------------------------
# All of it is published
# --------------------------------------------------------------------------


def test_the_rasi_table_publishes_every_2_2_classification():
    body = client.get("/v1/util/tables/rasis").json()
    aries = body["rasis"][0]
    assert aries["limb"] == "head"
    assert aries["odd_even_names"] == ["odd", "vishama", "oja", "male"]
    assert aries["footed_names"] == ["odd-footed", "vishamapada", "ojapada"]
    assert aries["modality"] == "chara"
    assert aries["modality_english"] == "movable"
    assert aries["modality_deity_role"] == "Creator"
    assert "dynamic" in aries["modality_nature"]
    assert aries["element"] == "fire"
    assert "transforms" in aries["element_definition"]


def test_the_rasi_table_publishes_the_section_level_statements():
    body = client.get("/v1/util/tables/rasis").json()
    assert "Vishnu's body" in body["section_2_2_1"]["zodiac_as_vishnu"]
    assert "sex of children" in body["section_2_2_2"]["used_for"]
    assert body["section_2_2_3"]["used_for"] == "This division is used in some dasas."
    assert "Trinity" in body["section_2_2_4"]["trinity_note"]
    assert len(body["section_2_2_4"]["modalities"]) == 3
    assert body["section_2_2_5"]["ether_name_sanskrit"] == "aakaasa"
    assert len(body["section_2_2_5"]["five_elements"]) == 5


def test_every_rasi_row_carries_all_five_classifications():
    body = client.get("/v1/util/tables/rasis").json()
    assert len(body["rasis"]) == 12
    for row in body["rasis"]:
        for field in ("limb", "odd_even_names", "footed_names", "modality",
                      "modality_nature", "element", "element_definition"):
            assert row[field], (row["name"], field)


# --------------------------------------------------------------------------
# 2.2.6 Pitta, Vaata and Kapha
# --------------------------------------------------------------------------

HUMOURS = [
    (("Ar", "Le", "Sg"), "pitta", "bilious", ["fire", "water"], "digestion"),
    (("Ta", "Vi", "Cp"), "vaata", "windy", ["air", "ether"], "breathing"),
    (("Cn", "Sc", "Pi"), "kapha", "phlegmatic", ["earth", "water"],
     "bones, muscles, fat"),
]


@pytest.mark.parametrize("signs,dosha,english,elements,example", HUMOURS)
def test_2_2_6_each_humour(signs, dosha, english, elements, example):
    """"Ar, Le and Sg are of pitta nature." and the two that follow."""
    index = c.DOSHA_NAMES.index(dosha)
    assert [i for i in range(12) if c.RASI_DOSHA[i] == index] == rasis(*signs)
    assert c.DOSHA_NAMES_EN[index] == english
    assert c.DOSHA_ELEMENTS[index] == elements
    assert c.DOSHA_BODY_EXAMPLE[index] == example


def test_2_2_6_the_airy_signs_are_mixed():
    """"Ge, Li and Aq are of a mixed nature."

    "Mixed" is given no English name, no element pair and no body example —
    the book supplies none, so those entries are None rather than invented.
    """
    index = c.DOSHA_NAMES.index("mixed")
    assert [i for i in range(12) if c.RASI_DOSHA[i] == index] == rasis("Ge", "Li", "Aq")
    assert c.DOSHA_NAMES_EN[index] is None
    assert c.DOSHA_ELEMENTS[index] is None
    assert c.DOSHA_SHOWS[index] is None


def test_2_2_6_what_each_humour_shows():
    """"It shows things that result in tranformation in a system." /
    "things that move in and out of a system." / "things that bind a system
    together ... things that give a structure to a system."""
    pitta, vaata, kapha, _ = c.DOSHA_SHOWS
    assert "in a system" in pitta
    assert "move in and out" in vaata
    assert "bind a system together" in kapha and "structure" in kapha


def test_2_2_6_the_books_typo_is_kept_as_printed():
    """The pitta sentence prints "tranformation". Kept verbatim, and recorded
    so it is never mistaken for one of ours."""
    assert c.DOSHA_SHOWS_TYPO == "tranformation"
    assert c.DOSHA_SHOWS_TYPO in c.DOSHA_SHOWS[0]
    assert "transformation" not in c.DOSHA_SHOWS[0]


def test_2_2_6_the_compositions_do_not_give_the_sign_assignment():
    """D-1. §2.2.6 states vaata = air + ether, then assigns *earthy* signs to
    vaata and calls the airy signs mixed. The inconsistency is inside the
    section, not between the book and modern Ayurveda.

    Pinned so that nobody later "fixes" RASI_DOSHA to follow the formula.
    """
    vaata = c.DOSHA_NAMES.index("vaata")
    assert c.DOSHA_ELEMENTS[vaata] == ["air", "ether"]
    airy = [i for i in range(12) if c.ELEMENT_NAMES[c.RASI_ELEMENT[i]] == "air"]
    assert all(c.RASI_DOSHA[i] != vaata for i in airy), "airy signs are mixed"
    assert [i for i in range(12) if c.RASI_DOSHA[i] == vaata] == rasis("Ta", "Vi", "Cp")


def test_2_2_6_ayurveda_is_defined():
    """"Ayurveda is India's Vedic medical system that recognizes human body and
    everything else in the universe as having 3 natures ..."."""
    assert "3 natures" in c.AYURVEDA_NOTE
    assert "5 elements" in c.AYURVEDA_NOTE


def test_2_2_6_the_four_humours_partition_the_zodiac():
    seen = [rasis(*h[0]) for h in HUMOURS] + [rasis("Ge", "Li", "Aq")]
    assert sorted(i for g in seen for i in g) == list(range(12))


# --------------------------------------------------------------------------
# 2.2.7 Sattwa, Rajas and Tamas
# --------------------------------------------------------------------------

GUNAS = [
    (("Cn", "Le", "Sg", "Pi"), "sattwa", None, "purity", "truthfulness and purity"),
    (("Ar", "Ta", "Li", "Sc"), "rajas", "rajo guna", "energy",
     "energetic and passionate"),
    (("Ge", "Vi", "Cp", "Aq"), "tamas", "tamo guna", "darkness", "depraved"),
]


@pytest.mark.parametrize("signs,guna,alt,meaning,effect", GUNAS)
def test_2_2_7_each_guna(signs, guna, alt, meaning, effect):
    """"Saattwik signs ... are - Cn, Le, Sg, Pi." and the two that follow."""
    index = c.GUNA_NAMES.index(guna)
    assert [i for i in range(12) if c.RASI_GUNA[i] == index] == rasis(*signs)
    assert c.GUNA_NAMES_ALT[index] == alt
    assert c.GUNA_MEANINGS[index] == meaning
    assert effect in c.GUNA_EFFECTS[index]


def test_2_2_7_sattwa_alone_has_no_second_name():
    """"Rajas or rajo guna", "Tamas or tamo guna" — but sattwa is given only
    "Sattwa (purity)"."""
    assert c.GUNA_NAMES_ALT[0] is None
    assert all(a is not None for a in c.GUNA_NAMES_ALT[1:])


def test_2_2_7_they_are_called_trigunas():
    """"They are called trigunas."""
    assert c.TRIGUNA_NAME == "trigunas"
    assert "trigunas" in c.TRIGUNA_NOTE
    assert "3 gunas" in c.TRIGUNA_NOTE


def test_2_2_7_each_sign_has_exactly_one_guna():
    """"everything in this universe has one of 3 gunas"."""
    assert sorted(c.RASI_GUNA) == sorted([0] * 4 + [1] * 4 + [2] * 4)


def test_2_2_7_the_adjectival_forms_exist_for_all_three():
    """The book writes "Saattwik signs", "Raajasik signs", "Taamasik signs"."""
    assert len(c.GUNA_ADJECTIVES) == 3
    assert c.GUNA_ADJECTIVES[0][0] == "saattwik"
    assert c.GUNA_ADJECTIVES[1][0] == "raajasik"
    assert c.GUNA_ADJECTIVES[2][0] == "taamasik"


# --------------------------------------------------------------------------
# 2.2.8 Rasis and Directions
# --------------------------------------------------------------------------

DIRECTIONS = [
    (("Ar", "Le", "Sg"), "east"), (("Ta", "Vi", "Cp"), "south"),
    (("Ge", "Li", "Aq"), "west"), (("Cn", "Sc", "Pi"), "north"),
]


@pytest.mark.parametrize("signs,direction", DIRECTIONS)
def test_2_2_8_each_direction(signs, direction):
    index = c.DIRECTION_NAMES.index(direction)
    assert [i for i in range(12) if c.RASI_DIRECTION[i] == index] == rasis(*signs)


def test_2_2_8_direction_follows_the_element_grouping():
    """The four direction groups are the four element groups, in the order
    fire-east, earth-south, air-west, water-north."""
    assert list(c.RASI_DIRECTION) == list(c.RASI_ELEMENT)
    for i, (signs, _) in enumerate(DIRECTIONS):
        assert rasis(*signs) == rasis(*ELEMENTS[i][0])


# --------------------------------------------------------------------------
# 2.2.9 Rasis and Colors
# --------------------------------------------------------------------------

#: The colours as printed, sign by sign.
COLORS = [
    ("Ar", "blood-red color"), ("Ta", "white"), ("Ge", "grass green"),
    ("Cn", "pale red"), ("Le", "white"), ("Vi", "variegated"),
    ("Li", "black"), ("Sc", "reddish brown"),
    ("Sg", "the color of the husk of grass"), ("Cp", "variegated"),
    ("Aq", "brown color (that of a mongoose)"),
    ("Pi", "cream color or the color of fish"),
]


@pytest.mark.parametrize("abbr,color", COLORS)
def test_2_2_9_each_color(abbr, color):
    assert c.RASI_COLOR[A.index(abbr)] == color


def test_2_2_9_two_pairs_of_signs_share_a_color():
    """Ta and Le are both white; Vi and Cp are both variegated. So the colours
    are not twelve distinct values, and a uniqueness check would be wrong."""
    assert c.RASI_COLOR[A.index("Ta")] == c.RASI_COLOR[A.index("Le")] == "white"
    assert c.RASI_COLOR[A.index("Vi")] == c.RASI_COLOR[A.index("Cp")] == "variegated"
    assert len(set(c.RASI_COLOR)) == 10


def test_2_2_9_the_pisces_doubled_article_is_dropped():
    """The book prints "cream color or the the color of fish". The doubled
    "the" is a typo in the source and is not reproduced."""
    assert c.RASI_COLOR[A.index("Pi")] == "cream color or the color of fish"
    assert "the the" not in c.RASI_COLOR[A.index("Pi")]


def test_2_2_9_the_books_american_spelling_is_kept():
    """"color", not "colour" — the book's own spelling throughout."""
    assert not any("colour" in x for x in c.RASI_COLOR)


# --------------------------------------------------------------------------
# 2.2.10 Day and Night
# --------------------------------------------------------------------------

NIGHT = ("Ar", "Ta", "Ge", "Cn", "Sg", "Cp")
DAY = ("Le", "Vi", "Li", "Sc", "Aq", "Pi")


def test_2_2_10_the_night_rasis():
    """"Ar, Ta, Ge, Cn, Sg and Cp are night time rasis ... They are nishaa
    rasis."""
    assert [i for i in range(12) if c.RASI_IS_NIGHT[i]] == rasis(*NIGHT)
    assert c.DAY_NIGHT_NAMES[0] == ["night time", "nishaa"]


def test_2_2_10_the_day_rasis():
    """"Le, Vi, Li, Sc, Aq and Pi are daytime rasis ... They are divaa rasis."""
    assert [i for i in range(12) if not c.RASI_IS_NIGHT[i]] == rasis(*DAY)
    assert c.DAY_NIGHT_NAMES[1] == ["daytime", "divaa"]


def test_2_2_10_every_two_sign_lord_owns_one_of_each():
    """"Out of the two rasis owned by a planet, one is a day sign and one is a
    night sign."

    Checked against RASI_LORD rather than restated: this is a claim about the
    lordship table and the day/night table agreeing, and it is the cheapest
    check that either one has been mistyped.
    """
    owned: dict[int, list[int]] = {}
    for i in range(12):
        owned.setdefault(int(c.RASI_LORD[i]), []).append(i)
    two_sign = {g: v for g, v in owned.items() if len(v) == 2}
    assert len(two_sign) == 5, "Mars, Mercury, Jupiter, Venus, Saturn"
    for graha, signs in two_sign.items():
        assert c.RASI_IS_NIGHT[signs[0]] != c.RASI_IS_NIGHT[signs[1]], graha


def test_2_2_10_the_governors_are_moon_and_sun():
    """"Moon governs all the nishaa rasis and Sun governs all the divaa rasis."

    DAY_NIGHT_GOVERNOR holds plain ints because constants/graha.py imports
    Rasi from constants/rasi.py, so importing Graha there would be circular.
    This pins the two values to the enum members they stand for.
    """
    from hora.core.constants.graha import Graha

    assert c.DAY_NIGHT_GOVERNOR[0] == int(Graha.MOON)
    assert c.DAY_NIGHT_GOVERNOR[1] == int(Graha.SUN)


def test_2_2_10_the_sole_signs_of_sun_and_moon_match_their_governance():
    """Moon owns Cancer, a night sign; Sun owns Leo, a day sign. Consistent
    with them governing the nishaa and divaa halves respectively."""
    from hora.core.constants.graha import Graha

    assert c.RASI_LORD[A.index("Cn")] == Graha.MOON
    assert c.RASI_IS_NIGHT[A.index("Cn")]
    assert c.RASI_LORD[A.index("Le")] == Graha.SUN
    assert not c.RASI_IS_NIGHT[A.index("Le")]


# --------------------------------------------------------------------------
# 2.2.11 Rising of rasis
# --------------------------------------------------------------------------


def test_2_2_11_the_seershodaya_rasis():
    """"Ge, Le, Vi, Li, Sc, Aq are Seershodaya rasis." — six of them."""
    index = c.RISING_NAMES.index("seershodaya")
    assert [i for i in range(12) if c.RASI_RISING[i] == index] == rasis(
        "Ge", "Le", "Vi", "Li", "Sc", "Aq"
    )


def test_2_2_11_the_prishthodaya_rasis():
    """"Ar, Ta, Cn, Sg, Cp are Prishthodaya rasis." — five, not six."""
    index = c.RISING_NAMES.index("prishthodaya")
    assert [i for i in range(12) if c.RASI_RISING[i] == index] == rasis(
        "Ar", "Ta", "Cn", "Sg", "Cp"
    )


def test_2_2_11_pisces_alone_rises_both_ways():
    """"Pi rises with both its head and feet."

    Which is why the three groups are 6 + 5 + 1 and not 6 + 6.
    """
    index = c.RISING_NAMES.index("ubhayodaya")
    assert [i for i in range(12) if c.RASI_RISING[i] == index] == [A.index("Pi")]
    assert "both its head and feet" in c.RISING_DESCRIPTIONS[index]


def test_2_2_11_footnote_4_on_prishthodaya():
    """"Many scholars have interpreted "prishthodaya" as "rising with the
    feet". So we will use the same interpretation. However, strictly speaking,
    one should note that "prishtha" means "back"." See D-2."""
    assert "prishtha" in c.PRISHTHODAYA_NOTE
    assert "back" in c.PRISHTHODAYA_NOTE
    assert "rising with the feet" in c.PRISHTHODAYA_NOTE


def test_2_2_11_the_dasa_timing_rule():
    """"planets in Seershodaya rasi give their results in the first half of
    their dasas and planets in Prishthodaya rasi give their results in the
    second half"."""
    assert c.RISING_DASA_HALF[c.RISING_NAMES.index("seershodaya")] == "first"
    assert c.RISING_DASA_HALF[c.RISING_NAMES.index("prishthodaya")] == "second"
    assert c.RISING_DASA_HALF[c.RISING_NAMES.index("ubhayodaya")] is None
    assert "first half" in c.RISING_DASA_RULE
    assert "second half" in c.RISING_DASA_RULE


# --------------------------------------------------------------------------
# 2.2.12 Varna or Class
# --------------------------------------------------------------------------

VARNAS = [
    (("Cn", "Sc", "Pi"), "brahmana", "scholars", "water", "priests or ministers"),
    (("Ar", "Le", "Sg"), "kshatriya", "warriors", "fire", "kings, army chiefs"),
    (("Ta", "Vi", "Cp"), "vaisya", "traders", "earth", "suppliers of various services"),
    (("Ge", "Li", "Aq"), "sudra", "workers", "air", "menial tasks"),
]


@pytest.mark.parametrize("signs,varna,english,element,phrase", VARNAS)
def test_2_2_12_each_varna(signs, varna, english, element, phrase):
    """"Brahmanas (scholars) are represented by watery signs - Cn, Sc, Pi."
    and the three that follow."""
    index = c.VARNA_NAMES.index(varna)
    assert [i for i in range(12) if c.RASI_VARNA[i] == index] == rasis(*signs)
    assert c.VARNA_NAMES_EN[index] == english
    assert c.VARNA_ELEMENT[index] == element
    assert phrase in c.VARNA_DESCRIPTIONS[index]


def test_2_2_12_varna_is_stated_by_element_not_by_sign():
    """The book gives the mapping as watery/fiery/earthy/airy, so the sign
    lists follow from RASI_ELEMENT. Asserted rather than assumed."""
    for signs, varna, _, element, _ in VARNAS:
        e = c.ELEMENT_NAMES.index(element)
        assert rasis(*signs) == [i for i in range(12) if c.RASI_ELEMENT[i] == e]
        assert c.VARNA_ELEMENT[c.VARNA_NAMES.index(varna)] == element


def test_2_2_12_the_four_varnas_are_in_the_books_numbered_order():
    """"(1) Brahmanas, (2) Kshatriyas, (3) Vaisyas and (4) Sudras."""
    assert c.VARNA_NAMES == ["brahmana", "kshatriya", "vaisya", "sudra"]


def test_2_2_12_the_varna_order_is_not_the_element_order():
    """VARNA_NAMES runs brahmana-kshatriya-vaisya-sudra, which is
    water-fire-earth-air; ELEMENT_NAMES runs fire-earth-air-water. Indexing
    one list with the other's index would be wrong for all four."""
    assert c.VARNA_ELEMENT != c.ELEMENT_NAMES
    assert c.VARNA_ELEMENT == ["water", "fire", "earth", "air"]


# --------------------------------------------------------------------------
# 2.2.6 to 2.2.12 are published
# --------------------------------------------------------------------------


def test_the_rasi_table_publishes_the_later_classifications():
    aries = client.get("/v1/util/tables/rasis").json()["rasis"][0]
    assert aries["dosha_english"] == "bilious"
    assert aries["guna_meaning"] == "energy"
    assert aries["day_night_names"] == ["night time", "nishaa"]
    assert aries["day_night_governor"] == 1
    assert aries["rising_dasa_half"] == "second"
    assert aries["varna_english"] == "warriors"
    assert "kings" in aries["varna_description"]


def test_the_mixed_dosha_publishes_a_null_english_name():
    gemini = client.get("/v1/util/tables/rasis").json()["rasis"][2]
    assert gemini["dosha"] == "mixed"
    assert gemini["dosha_english"] is None


def test_pisces_publishes_no_dasa_half():
    pisces = client.get("/v1/util/tables/rasis").json()["rasis"][11]
    assert pisces["rising"] == "ubhayodaya"
    assert pisces["rising_dasa_half"] is None


def test_the_later_section_blocks_are_published():
    body = client.get("/v1/util/tables/rasis").json()
    assert "3 natures" in body["section_2_2_6"]["ayurveda_note"]
    assert "tranformation" in body["section_2_2_6"]["note"]
    assert "trigunas" in body["section_2_2_7"]["triguna_note"]
    assert body["section_2_2_10"]["governors"][0]["graha_name"] == "Moon"
    assert body["section_2_2_10"]["governors"][1]["graha_name"] == "Sun"
    assert "prishtha" in body["section_2_2_11"]["prishthodaya_note"]
    assert [v["english"] for v in body["section_2_2_12"]["varnas"]] == [
        "scholars", "warriors", "traders", "workers",
    ]
