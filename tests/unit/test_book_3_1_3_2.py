"""Sections 3.1 and 3.2.1–3.2.7 — grahas, statement by statement.

The tables were already right. What this file adds is the two conditional
rules of §3.2.2, which nothing implemented, and the internal evidence in
§3.2.7 that settles D-6.
"""

from __future__ import annotations

from itertools import pairwise

import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.benefic import (
    BENEFIC,
    CONDITIONAL,
    MALEFIC,
    NEUTRAL,
    BeneficError,
    mercury_nature,
    moon_nature,
    nature,
)
from hora.core import const as c
from hora.core.const import Graha
from hora.core.validate import InputError
from hora.services import benefic_service

client = TestClient(app)


# --------------------------------------------------------------------------
# 3.1 Introduction
# --------------------------------------------------------------------------


def test_3_1_there_are_seven_grahas():
    """"There are 7 grahas (planets) in Vedic astrology: Sun, Moon, Mars,
    Mercury, Jupiter, Venus and Saturn."""
    assert [c.GRAHA_NAMES[i] for i in range(7)] == [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    ]


def test_3_1_rahu_and_ketu_are_the_two_shadow_grahas():
    """"There are two more chaayaa grahas (shadow planets): Rahu and Ketu."""
    assert c.CHAAYAA_GRAHAS == frozenset({Graha.RAHU, Graha.KETU})
    assert "shadow planet" in c.CHAAYAA_GRAHA_NAME


def test_3_1_the_nodes_are_mathematical_points():
    """"Rahu and Ketu are mathematical points."""
    assert "mathematical points" in c.NODES_ARE_MATHEMATICAL_POINTS


def test_3_1_the_nodes_other_names():
    """"They are also called the north and south nodes or the head and tail of
    dragon."""
    assert c.NODE_ALIASES[Graha.RAHU] == ["north node", "head of dragon"]
    assert c.NODE_ALIASES[Graha.KETU] == ["south node", "tail of dragon"]


def test_3_1_planets_represent_vishnus_avataras():
    """"Just as the whole zodiac represents Lord Vishnu and rasis represent
    His limbs, planets represent Vishnu's avataras (incarnations)."

    All three levels exist: ZODIAC_AS_VISHNU from §2.2.1, RASI_LIMB from
    §2.2.1, GRAHA_AVATARA here.
    """
    assert "Lord Vishnu's body" in c.ZODIAC_AS_VISHNU
    assert len(c.RASI_LIMB) == 12
    assert len(c.GRAHA_AVATARA) == 9


# --------------------------------------------------------------------------
# 3.2.1 Vishnu's Avataras
# --------------------------------------------------------------------------

AVATARAS = [
    (Graha.KETU, "Matsya", ["Meena"], "fish"),
    (Graha.SATURN, "Koorma", [], "tortoise"),
    (Graha.RAHU, "Varaaha", ["Sookara"], "boar"),
    (Graha.MARS, "Narasimha", ["Nrisimha"], "half-man, half-lion"),
    (Graha.JUPITER, "Vaamana", [], "learned dwarf"),
    (Graha.VENUS, "Parasu Rama", ["Bhaargava Rama"], None),
    (Graha.SUN, "Rama", [], None),
    (Graha.MOON, "Krishna", [], None),
    (Graha.MERCURY, "Buddha", [], None),
]


@pytest.mark.parametrize("graha,avatara,aliases,description", AVATARAS)
def test_3_2_1_each_avatara(graha, avatara, aliases, description):
    """"Meena/Matsya avatara (fish) came from Ketu." and the eight that
    follow."""
    assert c.GRAHA_AVATARA[graha] == avatara
    assert c.AVATARA_ALIASES.get(avatara, []) == aliases
    assert c.AVATARA_DESCRIPTIONS.get(avatara) == description


def test_3_2_1_all_nine_grahas_have_an_avatara():
    assert sorted(c.GRAHA_AVATARA) == list(range(9))
    assert len(set(c.GRAHA_AVATARA.values())) == 9


def test_3_2_1_only_five_avataras_are_described():
    """The book parenthesises fish, tortoise, boar, half-man half-lion and
    learned dwarf. Rama, Krishna, Buddha and Parasu Rama get none, so none is
    invented for them."""
    assert set(c.AVATARA_DESCRIPTIONS) == {
        "Matsya", "Koorma", "Varaaha", "Narasimha", "Vaamana",
    }


def test_3_2_1_the_two_essences():
    """"This world contains two essences - jeevaamsa (living essence) and
    paramaatmaamsa (absolute and supreme essence)."""
    assert "living essence" in c.ESSENCE_NAMES["jeeva"]
    assert "absolute and supreme essence" in c.ESSENCE_NAMES["paramaatma"]


def test_3_2_1_four_avataras_had_only_supreme_essence():
    """"Rama, Krishna, Narasimha and Varaha avataras had only
    paramaatmaamsa."

    The book spells it "Varaha" here and "Varaaha" in the list above; we store
    the list's spelling.
    """
    assert set(c.PURE_PARAMATMAMSA_AVATARAS) == {
        "Rama", "Krishna", "Narasimha", "Varaaha",
    }
    for name in c.PURE_PARAMATMAMSA_AVATARAS:
        assert name in c.GRAHA_AVATARA.values()


# --------------------------------------------------------------------------
# 3.2.2 Benefics and Malefics — the part nothing implemented
# --------------------------------------------------------------------------


def test_3_2_2_jupiter_and_venus_are_fixed_benefics():
    """"Jupiter and Venus are natural benefics (saumya grahas or subha
    grahas)."""
    assert c.NATURAL_BENEFIC == {Graha.JUPITER, Graha.VENUS}
    assert c.BENEFIC_CLASS_NAMES == ("saumya grahas", "subha grahas")
    for g in (Graha.JUPITER, Graha.VENUS):
        assert nature(g).nature == BENEFIC
        assert nature(g).conditional is False


def test_3_2_2_the_fixed_malefics_and_the_saturn_departure():
    """"Sun, Mars, Rahu and Ketu are natural malefics (kroora grahas or paapa
    grahas)."

    The printed list omits Saturn. PVR-2: page 102 corroborates that Saturn is
    a malefic, so it is kept. This asserts the departure explicitly rather
    than letting it look like a transcription of the list.
    """
    assert c.MALEFIC_CLASS_NAMES == ("kroora grahas", "paapa grahas")
    printed = {Graha.SUN, Graha.MARS, Graha.RAHU, Graha.KETU}
    assert printed < c.NATURAL_MALEFIC
    assert c.NATURAL_MALEFIC - printed == {Graha.SATURN}
    assert nature(Graha.SATURN).nature == MALEFIC


def test_3_2_2_moon_and_mercury_are_in_neither_fixed_set():
    """The reason this module exists. A caller reading only NATURAL_BENEFIC
    and NATURAL_MALEFIC finds Moon and Mercury in neither and silently treats
    them as nothing. See OI-45."""
    for g in (Graha.MOON, Graha.MERCURY):
        assert g not in c.NATURAL_BENEFIC
        assert g not in c.NATURAL_MALEFIC
    assert CONDITIONAL == frozenset({Graha.MOON, Graha.MERCURY})


def test_3_2_2_waxing_moon_is_benefic_and_waning_moon_is_malefic():
    """"Waxing Moon of Sukla paksha is a natural benefic. Waning Moon of
    Krishna paksha is a natural malefic."""
    assert moon_nature(0) == BENEFIC
    assert moon_nature(1) == MALEFIC
    assert c.PAKSHA_NAMES[0].startswith("Sukla")
    assert nature(Graha.MOON, paksha=0).nature == BENEFIC
    assert nature(Graha.MOON, paksha=1).nature == MALEFIC


def test_3_2_2_the_moon_cannot_be_judged_without_a_paksha():
    """§3.2.2 gives the Moon no nature independent of its phase, so asking
    without one is an error rather than a guess."""
    with pytest.raises(BeneficError, match="paksha"):
        nature(Graha.MOON)


def test_3_2_2_mercury_alone_is_a_benefic():
    """"Mercury becomes a natural benefic when he is alone"."""
    assert mercury_nature() == BENEFIC
    assert mercury_nature(set()) == BENEFIC
    assert "alone" in nature(Graha.MERCURY).reason


def test_3_2_2_mercury_with_more_benefics_is_a_benefic():
    """"...or with more natural benefics."""
    assert mercury_nature({Graha.JUPITER}) == BENEFIC
    assert mercury_nature({Graha.JUPITER, Graha.VENUS, Graha.SUN}) == BENEFIC


def test_3_2_2_mercury_with_more_malefics_is_a_malefic():
    """"Mercury becomes a natural malefic when he is joined by more natural
    malefics."""
    assert mercury_nature({Graha.SUN}) == MALEFIC
    assert mercury_nature({Graha.SUN, Graha.MARS, Graha.JUPITER}) == MALEFIC


def test_3_2_2_an_equal_split_is_covered_by_neither_clause():
    """One benefic and one malefic is neither "more benefics" nor "more
    malefics". Reported as neutral rather than forced either way. OI-45."""
    assert mercury_nature({Graha.JUPITER, Graha.SUN}) == NEUTRAL
    assert "OI-45" in nature(Graha.MERCURY, companions={Graha.JUPITER, Graha.SUN}).reason


def test_3_2_2_mercury_ignores_itself_in_its_own_company():
    """A caller passing the whole rasi's occupants includes Mercury; it must
    not count itself as a companion."""
    assert mercury_nature({Graha.MERCURY}) == BENEFIC
    assert mercury_nature({Graha.MERCURY, Graha.SUN}) == MALEFIC


def test_3_2_2_the_moon_does_not_count_toward_mercurys_company():
    """The Moon is in neither fixed set, so it cannot tip Mercury either way
    without a paksha. Two conditional grahas together stay undecided."""
    assert mercury_nature({Graha.MOON}) == NEUTRAL


def test_3_2_2_why_the_classification_matters():
    """"This information is important because the results given by planets are
    based on their inherent nature."""
    assert "inherent nature" in benefic_service.rules()["inherent_nature_note"]


# --------------------------------------------------------------------------
# 3.2.3 Main Governance
# --------------------------------------------------------------------------

GOVERNS = [
    (Graha.SUN, "soul"), (Graha.MOON, "mind"), (Graha.MARS, "strength"),
    (Graha.MERCURY, "speech"), (Graha.JUPITER, "knowledge and happiness"),
    (Graha.VENUS, "potency"), (Graha.SATURN, "grief"),
]


@pytest.mark.parametrize("graha,governs", GOVERNS)
def test_3_2_3_each_governance(graha, governs):
    assert c.GRAHA_GOVERNS[graha] == governs


def test_3_2_3_the_nodes_govern_nothing_here():
    """§3.2.3 lists the seven only."""
    assert Graha.RAHU not in c.GRAHA_GOVERNS
    assert Graha.KETU not in c.GRAHA_GOVERNS


# --------------------------------------------------------------------------
# 3.2.4 Planets and Colors
# --------------------------------------------------------------------------

GRAHA_COLORS = [
    (Graha.SUN, "blood-red color"), (Graha.MOON, "tawny color"),
    (Graha.MARS, "blood-red color"), (Graha.MERCURY, "grass green color"),
    (Graha.JUPITER, "tawny color"), (Graha.VENUS, "variegated"),
    (Graha.SATURN, "black color"),
]


@pytest.mark.parametrize("graha,color", GRAHA_COLORS)
def test_3_2_4_each_color(graha, color):
    assert c.GRAHA_COLOR[graha] == color


def test_3_2_4_two_pairs_share_a_color():
    """Sun and Mars are both blood-red; Moon and Jupiter are both tawny. So a
    uniqueness check would be wrong here, as it would be for the rasis."""
    assert c.GRAHA_COLOR[Graha.SUN] == c.GRAHA_COLOR[Graha.MARS]
    assert c.GRAHA_COLOR[Graha.MOON] == c.GRAHA_COLOR[Graha.JUPITER]
    assert len(set(c.GRAHA_COLOR.values())) == 5


def test_3_2_4_the_stated_use():
    """"These colors can be useful, for example, when predicting the color of
    one's car."""
    assert "color of one's car" in c.GRAHA_COLOR_USE


def test_3_2_4_blood_red_and_variegated_match_the_rasi_colors():
    """§2.2.9 uses the same wording for Aries and Virgo. Same vocabulary, so
    the two tables can be compared without normalising."""
    assert c.RASI_COLOR[0] == c.GRAHA_COLOR[Graha.SUN] == "blood-red color"
    assert c.RASI_COLOR[5] == c.GRAHA_COLOR[Graha.VENUS] == "variegated"


# --------------------------------------------------------------------------
# 3.2.5 Planetary Cabinet
# --------------------------------------------------------------------------

CABINET = [
    (Graha.SUN, "king"), (Graha.MOON, "king"), (Graha.MARS, "leader (army chief)"),
    (Graha.MERCURY, "prince"), (Graha.JUPITER, "minister"),
    (Graha.VENUS, "minister"), (Graha.SATURN, "servant"),
    (Graha.RAHU, "army"), (Graha.KETU, "army"),
]


@pytest.mark.parametrize("graha,role", CABINET)
def test_3_2_5_each_cabinet_role(graha, role):
    """"Sun and Moon are kings. Mars is the leader (army chief). Mercury is the
    prince. Jupiter and Venus are the ministers. Saturn is the servant. Rahu
    and Ketu form the army."""
    assert c.GRAHA_CABINET[graha] == role


def test_3_2_5_all_nine_have_a_role():
    """Unlike §3.2.3, the cabinet covers the nodes too."""
    assert sorted(c.GRAHA_CABINET) == list(range(9))


# --------------------------------------------------------------------------
# 3.2.6 Planetary Deities
# --------------------------------------------------------------------------

DEITIES = [
    (Graha.SUN, "Agni", "fire god"),
    (Graha.MOON, "Varuna", "rain god"),
    (Graha.MARS, "Subrahmanya", "army chief of gods"),
    (Graha.MERCURY, "Maha Vishnu", "supreme sustaining force"),
    (Graha.JUPITER, "Indra", "ruler of gods"),
    (Graha.VENUS, "Sachi Devi", "Indra's wife"),
    (Graha.SATURN, "Brahma", "Creator"),
]


@pytest.mark.parametrize("graha,deity,role", DEITIES)
def test_3_2_6_each_deity_and_its_office(graha, deity, role):
    assert c.GRAHA_DEITY[graha] == deity
    assert c.GRAHA_DEITY_ROLE[graha] == role


def test_3_2_6_saturns_deity_is_brahma_the_creator():
    """§2.2.4 also calls Brahma the Creator, of the movable rasis. Same deity,
    same office, two different things ruled — asserted so the two tables stay
    consistent in wording."""
    assert c.GRAHA_DEITY_ROLE[Graha.SATURN] == "Creator"
    assert c.MODALITY_DEITY_ROLE[c.MODALITY_NAMES.index("chara")] == "Creator"
    assert c.MODALITY_DEITY[c.MODALITY_NAMES.index("chara")] == "Brahma"


def test_3_2_6_only_the_seven_have_deities():
    assert sorted(c.GRAHA_DEITY) == list(range(7))


# --------------------------------------------------------------------------
# 3.2.7 Sex of Planets — D-6
# --------------------------------------------------------------------------


def test_3_2_7_the_male_planets():
    """"Sun, Mars and Jupiter are male."""
    male = c.SEX_NAMES.index("male")
    assert {g for g, s in c.GRAHA_SEX.items() if s == male} == {
        Graha.SUN, Graha.MARS, Graha.JUPITER,
    }


def test_3_2_7_the_female_planets():
    """"Moon and Venus are female."""
    female = c.SEX_NAMES.index("female")
    assert {g for g, s in c.GRAHA_SEX.items() if s == female} == {
        Graha.MOON, Graha.VENUS,
    }


def test_3_2_7_mercury_and_saturn_are_recorded_as_neuter():
    """The book's third sentence prints "Saturn and Mercury are female", which
    would make two disjoint sentences both name the female group. We record
    neuter. This is the one place we depart from the printed text — D-6."""
    neuter = c.SEX_NAMES.index("neuter")
    assert {g for g, s in c.GRAHA_SEX.items() if s == neuter} == {
        Graha.MERCURY, Graha.SATURN,
    }
    assert c.SEX_NAMES == ("male", "female", "neuter")


def test_3_2_7_the_sections_own_example_requires_mercury_to_be_neuter():
    """The evidence that settles D-6, from inside §3.2.7 itself:

    "if the house ruling the first child is influenced by Jupiter, Mars and
    Mercury, we may predict a son. If it is influenced by Moon and Mercury, we
    may predict a daughter."

    **Mercury appears on both sides.** With male planets it points to a son;
    with a female planet it points to a daughter. That only works if Mercury
    takes the sex of its company — which is what neuter means. If Mercury were
    female, as the printed sentence says, it could not contribute to a son.
    """
    note = c.SEX_PREDICTION_NOTE
    son = note.split("we may predict a son")[0]
    daughter = note.split("we may predict a son")[1]
    assert "Mercury" in son and "Mercury" in daughter
    assert "Jupiter" in son and "Mars" in son
    assert "Moon" in daughter
    male = c.SEX_NAMES.index("male")
    assert c.GRAHA_SEX[Graha.JUPITER] == c.GRAHA_SEX[Graha.MARS] == male
    assert c.GRAHA_SEX[Graha.MOON] == c.SEX_NAMES.index("female")
    assert c.GRAHA_SEX[Graha.MERCURY] == c.SEX_NAMES.index("neuter")


def test_3_2_7_only_the_seven_have_a_sex():
    """The nodes are not given one."""
    assert sorted(c.GRAHA_SEX) == list(range(7))


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_the_nature_endpoint_covers_both_conditionals():
    for body, expected in (
        ({"graha": 3}, "benefic"),
        ({"graha": 3, "companions": [0, 2]}, "malefic"),
        ({"graha": 3, "companions": [4, 0]}, "neutral"),
        ({"graha": 1, "paksha": 0}, "benefic"),
        ({"graha": 1, "paksha": 1}, "malefic"),
        ({"graha": 6}, "malefic"),
    ):
        assert client.post("/v1/benefic/nature", json=body).json()["nature"] == expected


def test_the_nature_endpoint_rejects_the_moon_without_a_paksha():
    r = client.post("/v1/benefic/nature", json={"graha": 1})
    assert r.status_code == 400
    assert "paksha" in r.json()["error"]["message"]


def test_the_rules_endpoint_names_both_departures():
    body = client.get("/v1/benefic/rules").json()
    assert "PVR-2" in body["saturn_note"]
    assert "OI-45" in body["equal_split_note"]
    assert body["counts"] == {
        "fixed_benefic": 2, "fixed_malefic": 5, "conditional": 2,
    }


def test_the_graha_table_publishes_the_new_fields():
    grahas = client.get("/v1/util/tables/grahas").json()["grahas"]
    by_name = {g["name"]: g for g in grahas}
    assert by_name["Mercury"]["natural_nature"] == "conditional"
    assert by_name["Moon"]["natural_nature"] == "conditional"
    assert by_name["Saturn"]["natural_nature"] == "malefic"
    assert by_name["Mars"]["deity_role"] == "army chief of gods"
    assert by_name["Mars"]["avatara_description"] == "half-man, half-lion"
    assert by_name["Sun"]["avatara_description"] is None


def test_an_out_of_range_graha_is_rejected():
    with pytest.raises(InputError):
        nature(9)


# --------------------------------------------------------------------------
# 3.2.8 Planets & Five Elements
# --------------------------------------------------------------------------

TATTVAS = [
    ("agni tattva", "fire", Graha.MARS, Graha.SUN, "leadership, enterprise"),
    ("bhoo tattva", "earth", Graha.MERCURY, None, "memory, logical abilities"),
    ("vaayu tattva", "air", Graha.SATURN, None, "wandering and free spirit"),
    ("aakaasa tattva", "ether", Graha.JUPITER, None,
     "wisdom, intelligence and perceiving knowledge"),
    ("jala tattva", "water", Graha.VENUS, Graha.MOON,
     "imaginative and creative work"),
]


@pytest.mark.parametrize("tattva,english,ruler,sharer,governs", TATTVAS)
def test_3_2_8_each_tattva(tattva, english, ruler, sharer, governs):
    """"Agni tattva (fiery element) is ruled by Mars. Sun also has the same
    nature." and the four that follow."""
    index = c.PLANET_ELEMENT_NAMES.index(english)
    assert c.PLANET_ELEMENT_TATTVAS[index] == tattva
    assert c.ELEMENT_RULER[index] == ruler
    assert c.GRAHA_ELEMENT[ruler] == index
    assert c.ELEMENT_GOVERNANCE[ruler] == governs
    if sharer is not None:
        assert c.GRAHA_ELEMENT[sharer] == index


def test_3_2_8_only_sun_and_moon_share_an_element_without_ruling_it():
    """Two of the five tattvas get a second graha, and only those two: "Sun
    also has the same nature" for fire, "Moon also has the same nature" for
    water. Neither rules its element."""
    assert c.SHARES_ELEMENT_WITHOUT_RULING == frozenset({Graha.SUN, Graha.MOON})
    rulers = {int(g) for g in c.ELEMENT_RULER.values()}
    for g in c.SHARES_ELEMENT_WITHOUT_RULING:
        assert int(g) not in rulers
    assert len(rulers) == 5, "one ruler per tattva"


def test_3_2_8_the_sharers_get_no_governance_clause():
    """The prose gives a clause to each *ruler* only — Mars, Mercury, Saturn,
    Venus, Jupiter. Sun and Moon get none, so none is invented."""
    assert set(c.ELEMENT_GOVERNANCE) == {int(g) for g in c.ELEMENT_RULER.values()}
    for g in c.SHARES_ELEMENT_WITHOUT_RULING:
        assert g not in c.ELEMENT_GOVERNANCE


def test_3_2_8_ether_is_ruled_here_but_belongs_to_every_rasi_in_2_2_5():
    """§2.2.5 says ether "is present in every rasi" and gives it no signs;
    §3.2.8 gives it a ruling planet. Both hold, and neither is the other."""
    ether = c.PLANET_ELEMENT_NAMES.index("ether")
    assert c.ELEMENT_RULER[ether] == Graha.JUPITER
    assert "ether" not in c.ELEMENT_NAMES, "no rasi carries it in 2.2.5"


def test_3_2_8_all_seven_grahas_have_an_element():
    assert sorted(c.GRAHA_ELEMENT) == list(range(7))


def test_3_2_8_the_stated_purpose():
    """"These rulerships throw light on the basic nature of planets."""
    assert "basic nature of planets" in c.ELEMENT_GOVERNANCE_NOTE


# --------------------------------------------------------------------------
# 3.2.9 Planets & Varnas
# --------------------------------------------------------------------------

GRAHA_VARNAS = [
    ((Graha.JUPITER, Graha.VENUS), "brahmana", "learned",
     "Learning and intelligence"),
    ((Graha.SUN, Graha.MARS), "kshatriya", "warriors", "Bravery"),
    ((Graha.MOON, Graha.MERCURY), "vaisya", "traders", "Getting along"),
    ((Graha.SATURN,), "sudra", "worker", "Hard work"),
]


@pytest.mark.parametrize("grahas,varna,english,forte", GRAHA_VARNAS)
def test_3_2_9_each_varna(grahas, varna, english, forte):
    """"Jupiter and Venus are Brahmanas (learned)." and the three that
    follow."""
    index = c.VARNA_NAMES.index(varna)
    assert {g for g, v in c.GRAHA_VARNA.items() if v == index} == set(grahas)
    assert c.VARNA_NAMES_EN_3_2_9[index] == english
    assert c.VARNA_FORTE[index].startswith(forte)


def test_3_2_9_glosses_the_varnas_differently_from_2_2_12():
    """2.2.12: "Brahmanas (scholars) ... Sudras (workers)".
    3.2.9:  "Brahmanas (learned) ... a Sudra (worker)".

    Both are PVR's. Neither is normalised into the other, so both are stored
    and this pins the difference rather than letting one quietly win.
    """
    assert c.VARNA_NAMES_EN == ["scholars", "warriors", "traders", "workers"]
    assert c.VARNA_NAMES_EN_3_2_9 == ["learned", "warriors", "traders", "worker"]
    differ = [
        i for i in range(4) if c.VARNA_NAMES_EN[i] != c.VARNA_NAMES_EN_3_2_9[i]
    ]
    assert differ == [0, 3], "brahmana and sudra"


def test_3_2_9_varna_shows_nature_not_family_caste():
    """"we should understand varnas to show one's basic nature rather than the
    caste of one's family."""
    assert "rather than the caste" in c.VARNA_MEANS_NATURE_NOT_CASTE


def test_3_2_9_resolves_its_own_clash_with_the_cabinet():
    """"It should be noted that Moon, who was earlier classified in the
    planetary cabinet as a king, is said here to be of Vaisya varna."

    Both tables stand: §3.2.5 makes the Moon a king, §3.2.9 makes it a Vaisya.
    The book says so explicitly, so this is not a deviation to record.
    """
    assert c.GRAHA_CABINET[Graha.MOON] == "king"
    assert c.VARNA_NAMES[c.GRAHA_VARNA[Graha.MOON]] == "vaisya"
    assert "planetary cabinet as a king" in c.VARNA_CABINET_NOTE
    assert "gets along well with everyone" in c.VARNA_CABINET_NOTE


def test_3_2_9_the_suns_varna_agrees_with_the_cabinet():
    """"Sun is a king who is also a warrior." Kshatriya in §3.2.9, king in
    §3.2.5 — the note says the two are compatible for the Sun and need
    explaining only for the Moon."""
    assert c.VARNA_NAMES[c.GRAHA_VARNA[Graha.SUN]] == "kshatriya"
    assert c.GRAHA_CABINET[Graha.SUN] == "king"


def test_3_2_9_covers_only_the_seven():
    assert sorted(c.GRAHA_VARNA) == list(range(7))


# --------------------------------------------------------------------------
# 3.2.10 Planets & Gunas
# --------------------------------------------------------------------------

GRAHA_GUNAS = [
    ((Graha.SUN, Graha.MOON, Graha.JUPITER), "sattwa"),
    ((Graha.MERCURY, Graha.VENUS), "rajas"),
    ((Graha.MARS, Graha.SATURN), "tamas"),
]


@pytest.mark.parametrize("grahas,guna", GRAHA_GUNAS)
def test_3_2_10_each_guna(grahas, guna):
    """"Sun, Moon and Jupiter are saattwik planets. Mercury and Venus are
    raajasik planets. Mars and Saturn are taamasik planets."""
    index = c.GUNA_NAMES.index(guna)
    assert {g for g, v in c.GRAHA_GUNA.items() if v == index} == set(grahas)


def test_3_2_10_the_three_definitions():
    """"Sattva guna simply means purity and truthfulness ... Rajo guna shows
    some passion, energy and impurity ... Tamo guna shows a dark, mean and
    depraved spirit in thoughts and actions."""
    sattwa, rajas, tamas = c.GUNA_DEFINITIONS
    assert "purity and truthfulness" in sattwa
    assert "passion, energy and impurity" in rajas
    assert "dark, mean and depraved" in tamas


def test_3_2_10_sattwa_means_the_state_of_being_true():
    """"sattwa simply means "the state of being true"." The NOTE exists to
    correct a common reading, so the phrase is stored on its own."""
    assert c.SATTWA_MEANING == "the state of being true"
    assert c.SATTWA_MEANING in c.SATTWA_MISCONCEPTION_NOTE


def test_3_2_10_the_misconception_note_is_kept_whole():
    """Its argument runs across several sentences — aggression is not
    necessarily rajasik, a warrior without passion is still saattvic, the Sun
    is a warrior-king and still saattwik. Fragmenting it loses the point."""
    note = c.SATTWA_MISCONCEPTION_NOTE
    for phrase in ("misconception", "artificial goodness", "no passion or ego",
                   "Lord Rama", "Ravana"):
        assert phrase in note


def test_3_2_10_the_sun_is_a_warrior_and_still_saattwik():
    """"Sun is a king of the warrior class and yet he is saattwik."

    Checked against the two tables rather than restated: §3.2.9 makes the Sun
    a kshatriya and §3.2.10 makes it saattwik. The NOTE exists precisely
    because that pair looks contradictory.
    """
    assert c.VARNA_NAMES[c.GRAHA_VARNA[Graha.SUN]] == "kshatriya"
    assert c.GUNA_NAMES[c.GRAHA_GUNA[Graha.SUN]] == "sattwa"


def test_3_2_10_rama_came_from_the_sun():
    """"Lord Rama, who was born with his amsa, is a saattwik person."
    §3.2.1 assigns Rama to the Sun, so "his amsa" resolves."""
    assert c.GRAHA_AVATARA[Graha.SUN] == "Rama"


# --------------------------------------------------------------------------
# 3.2.11 Planetary Abodes
# --------------------------------------------------------------------------

ABODES = [
    (Graha.SUN, "temple"), (Graha.MOON, "watery place"),
    (Graha.MERCURY, "sports ground"), (Graha.JUPITER, "treasure house"),
    (Graha.VENUS, "bedroom"), (Graha.SATURN, "filthy area"),
]


@pytest.mark.parametrize("graha,abode", ABODES)
def test_3_2_11_each_abode(graha, abode):
    assert c.GRAHA_ABODE[graha] == abode


def test_3_2_11_mars_is_given_no_abode():
    """The section names six planets and skips Mars entirely. Recorded as an
    absence rather than filled in from another source."""
    assert c.GRAHA_ABODE.get(Graha.MARS) is None
    named = [g for g, v in c.GRAHA_ABODE.items() if v is not None]
    assert len(named) == 6
    assert Graha.MARS not in named


def test_3_2_11_the_stated_purpose():
    """"This description should give one an idea of the nature of planets."""
    assert "nature of planets" in c.ABODE_NOTE


# --------------------------------------------------------------------------
# 3.2.12 Seven Dhaatus
# --------------------------------------------------------------------------

DHATUS = [
    (Graha.SUN, "bones"), (Graha.MOON, "blood"), (Graha.MARS, "marrow"),
    (Graha.MERCURY, "skin"), (Graha.JUPITER, "fat"), (Graha.VENUS, "semen"),
    (Graha.SATURN, "muscles"),
]


@pytest.mark.parametrize("graha,dhatu", DHATUS)
def test_3_2_12_each_dhatu(graha, dhatu):
    """"Sun rules bones. Moon rules blood. Mars rules marrow. Mercury rules
    skin. Jupiter rules fat. Venus rules semen. Saturn rules muscles."""
    assert c.GRAHA_DHATU[graha] == dhatu


def test_3_2_12_there_are_seven_and_they_are_distinct():
    """"Sapta dhaatus or 7 matters make up human body."""
    assert len(c.GRAHA_DHATU) == 7
    assert len(set(c.GRAHA_DHATU.values())) == 7
    assert c.SAPTA_DHATU_NAME == "sapta dhaatus"
    assert "7 matters" in c.SAPTA_DHATU_NOTE


def test_3_2_12_only_venuss_dhatu_is_glossed():
    """"Venus rules semen (materials related to the reproductive system)." No
    other dhatu carries a parenthetical."""
    assert c.DHATU_DESCRIPTIONS == {
        Graha.VENUS: "materials related to the reproductive system"
    }


def test_3_2_12_the_affliction_examples():
    """"If Sun is afflicted, it can show some problems related to bones.
    Weakness of Moon may give blood related problems."

    Both examples name the dhatu the table assigns, which is the check that
    the prose and the table have not drifted apart.
    """
    assert c.GRAHA_DHATU[Graha.SUN] in c.DHATU_AFFLICTION_NOTE
    assert c.GRAHA_DHATU[Graha.MOON] in c.DHATU_AFFLICTION_NOTE


# --------------------------------------------------------------------------
# 3.2.13 Planets & Time Periods
# --------------------------------------------------------------------------

PERIODS = [
    (Graha.SUN, "ayana"), (Graha.MOON, "minute"), (Graha.MARS, "week"),
    (Graha.MERCURY, "ritu"), (Graha.JUPITER, "month"),
    (Graha.VENUS, "fortnight"), (Graha.SATURN, "year"),
]


@pytest.mark.parametrize("graha,period", PERIODS)
def test_3_2_13_each_time_period(graha, period):
    assert c.GRAHA_TIME_PERIOD[graha] == period


def test_3_2_13_the_two_footnoted_periods_are_defined_elsewhere():
    """Footnote 5 defines the ayana and footnote 6 the ritu. Both are the only
    two periods in the list that are not everyday units, and both already have
    their own constants."""
    assert len(c.AYANA_NAMES) == 2
    assert len(c.RITU_NAMES) == 6
    assert c.GRAHA_TIME_PERIOD[Graha.SUN] == "ayana"
    assert c.GRAHA_TIME_PERIOD[Graha.MERCURY] == "ritu"


def test_3_2_13_the_stated_use():
    """"These periods are very useful in prasna or horary astrology."""
    assert "prasna" in c.TIME_PERIOD_USE
    assert "horary" in c.TIME_PERIOD_USE


def test_3_2_13_covers_only_the_seven():
    assert sorted(c.GRAHA_TIME_PERIOD) == list(range(7))


# --------------------------------------------------------------------------
# 3.2.8 to 3.2.13 are published
# --------------------------------------------------------------------------


def test_the_graha_table_publishes_the_later_sections():
    grahas = client.get("/v1/util/tables/grahas").json()["grahas"]
    by_name = {g["name"]: g for g in grahas}
    assert by_name["Mars"]["element_governance"] == "leadership, enterprise"
    assert by_name["Mars"]["rules_element"] is True
    assert by_name["Sun"]["shares_element_without_ruling"] is True
    assert by_name["Sun"]["rules_element"] is False
    assert by_name["Sun"]["element_governance"] is None
    assert by_name["Jupiter"]["varna_english"] == "learned"
    assert "Learning" in by_name["Jupiter"]["varna_forte"]
    assert "purity" in by_name["Sun"]["guna_definition"]
    assert by_name["Venus"]["dhatu_description"] is not None
    assert by_name["Mars"]["abode"] is None


def test_the_later_section_blocks_are_published():
    body = client.get("/v1/util/tables/grahas").json()
    assert "basic nature of planets" in body["section_3_2_8"]["note"]
    assert body["section_3_2_8"]["shares_without_ruling"] == [0, 1]
    assert body["section_3_2_9"]["english_names"][0] == "learned"
    assert "2.2.12" in body["section_3_2_9"]["gloss_differs_from_2_2_12"]
    assert "king" in body["section_3_2_9"]["cabinet_note"]
    assert body["section_3_2_10"]["sattwa_meaning"] == "the state of being true"
    assert "nature of planets" in body["section_3_2_11"]["note"]
    assert "7 matters" in body["section_3_2_12"]["note"]
    assert "prasna" in body["section_3_2_13"]["use"]


# --------------------------------------------------------------------------
# 3.2.14 Planets & Tastes
# --------------------------------------------------------------------------

TASTES = [
    (Graha.SUN, "pungent", ["onion", "ginger", "pepper"]),
    (Graha.MOON, "saline", ["sea salt", "rock salt"]),
    (Graha.MARS, "bitter", ["karela/bitter melon", "dandelion root",
                            "rhubarb root", "neem leaves"]),
    (Graha.MERCURY, "mixed", []),
    (Graha.JUPITER, "sweet", ["sugar", "dates"]),
    (Graha.VENUS, "sour", ["lemon", "tamarind"]),
    (Graha.SATURN, "astringent", ["plantain", "pomegranate"]),
]


@pytest.mark.parametrize("graha,taste,examples", TASTES)
def test_3_2_14_each_taste(graha, taste, examples):
    """"Sun governs the pungent taste (e.g. onion, ginger, pepper)." and the
    six that follow."""
    assert c.GRAHA_TASTE[graha] == taste
    assert c.TASTE_EXAMPLES.get(graha, []) == examples


def test_3_2_14_mercury_alone_gets_no_examples():
    """"Mercury governs a mixed taste." — no parenthetical, so none invented."""
    assert Graha.MERCURY not in c.TASTE_EXAMPLES
    assert len(c.TASTE_EXAMPLES) == 6
    assert len(c.GRAHA_TASTE) == 7


def test_3_2_14_the_stated_use():
    """"The 2nd house shows one's preference in food ... one should avoid the
    tastes of the planets who are likely bring disease."

    The last clause is the book's own wording, "likely bring", not "likely to
    bring". Kept as printed.
    """
    assert "2nd house shows" in c.TASTE_USE
    assert "likely bring disease" in c.TASTE_USE


def test_3_2_14_every_taste_is_distinct():
    assert len(set(c.GRAHA_TASTE.values())) == 7


# --------------------------------------------------------------------------
# 3.2.15 Planetary Strengths
# --------------------------------------------------------------------------

DIG_BALA = [
    ((Graha.MERCURY, Graha.JUPITER), 1, "east"),
    ((Graha.SUN, Graha.MARS), 10, "south"),
    ((Graha.MOON, Graha.VENUS), 4, "north"),
    ((Graha.SATURN,), 7, "west"),
]


@pytest.mark.parametrize("grahas,house,direction", DIG_BALA)
def test_3_2_15_each_digbala(grahas, house, direction):
    """"Mercury and Jupiter are strong in the eastern direction (lagna). Sun
    and Mars are strong in the southern direction (meridian - 10th house).
    Moon and Venus are strong in the northern direction (nadir - 4th house).
    Saturn is strong in the west (7th house)."""
    assert {g for g, h in c.DIG_BALA_STRONG_HOUSE.items() if h == house} == set(grahas)


def test_3_2_15_the_four_digbala_houses_are_the_kendras():
    """1, 4, 7, 10 — the book names each by both house and direction, and the
    four together are exactly the kendras."""
    assert sorted(set(c.DIG_BALA_STRONG_HOUSE.values())) == [1, 4, 7, 10]
    assert len(c.DIG_BALA_STRONG_HOUSE) == 7, "nodes get no digbala"


def test_3_2_15_the_digbala_name_and_purpose():
    """"These are the digbalas (strengths associated with direction) of
    planets. These show the direction taken by one in one's life."""
    assert c.DIG_BALA_NAME == "digbala"
    assert "direction taken by one" in c.DIG_BALA_NOTE


def test_3_2_15_day_and_night_strength():
    """"Moon, Mars and Saturn are strong in the night time. Sun, Jupiter and
    Venus are strong in the daytime. Mercury is always strong."""
    assert set(c.STRONG_AT_NIGHT) == {Graha.MOON, Graha.MARS, Graha.SATURN}
    assert set(c.STRONG_BY_DAY) == {Graha.SUN, Graha.JUPITER, Graha.VENUS}
    assert set(c.STRONG_ALWAYS) == {Graha.MERCURY}


def test_3_2_15_the_three_groups_cover_the_seven_exactly_once():
    """Mercury is the only graha with no half, which is why a day/night flag
    alone cannot express this section."""
    groups = [set(c.STRONG_AT_NIGHT), set(c.STRONG_BY_DAY), set(c.STRONG_ALWAYS)]
    assert sorted(int(g) for s in groups for g in s) == list(range(7))
    assert "always strong" in c.ALWAYS_STRONG_NOTE


def test_3_2_15_paksha_strength():
    """"Natural malefics are strong in Krishna paksha. Natural benefics are
    strong in Sukla paksha."""
    assert c.PAKSHA_NAMES[c.BENEFIC_STRONG_PAKSHA].startswith("Sukla")
    assert c.PAKSHA_NAMES[c.MALEFIC_STRONG_PAKSHA] == "Krishna"


def test_3_2_15_ayana_strength():
    """"Natural malefics are strong in Dakshina ayana. Natural benefics are
    strong in Uttara ayana."""
    assert c.AYANA_NAMES[c.BENEFIC_STRONG_AYANA] == "uttara"
    assert c.AYANA_NAMES[c.MALEFIC_STRONG_AYANA] == "dakshina"


def test_3_2_15_footnote_7_points_back_to_footnote_5():
    """"For the meaning of ayanas, see footnote 5." — the ayana definition is
    §1.3's, already stored, so nothing is duplicated here."""
    assert len(c.AYANA_NAMES) == 2
    assert set(c.AYANA_NAMES) == {"uttara", "dakshina"}


# --------------------------------------------------------------------------
# 3.2.16 Planets & Ritus
# --------------------------------------------------------------------------

RITUS = [
    ("vasanta", "spring", Graha.VENUS),
    ("greeshma", "summer", Graha.MARS),
    ("varsha", "rainy season", Graha.MOON),
    ("hemanta", "season of dew", Graha.MERCURY),
    ("seeta", "winter", Graha.JUPITER),
    ("sisira", "fall", Graha.SATURN),
]


@pytest.mark.parametrize("ritu,meaning,lord", RITUS)
def test_3_2_16_each_ritu(ritu, meaning, lord):
    """"Venus governs vasanta ritu (spring)." and the five that follow."""
    index = c.RITU_NAMES.index(ritu)
    assert c.RITU_MEANINGS[index] == meaning
    assert c.RITU_RULER[index] == lord


def test_3_2_16_six_ritus_in_the_books_order():
    """Footnote 6: "There are 6 ritus in a year. They are - vasanta (spring),
    greeshma (summer), varsha (rain), hemanta (dew), seeta (winter), sisira
    (fall). Each ritu consists of 2 months."

    §3.2.16 lists them in the same order, so the two agree.
    """
    assert list(c.RITU_NAMES) == [r[0] for r in RITUS]
    assert len(c.RITU_NAMES) == 6
    assert c.RITU_MONTHS == 2, "each ritu consists of 2 months"
    assert len(c.RITU_NAMES) * c.RITU_MONTHS == 12, "six ritus tile the year"


def test_3_2_16_the_sun_rules_no_ritu():
    """Six seasons, seven grahas. Mercury rules a ritu as a *time period* in
    §3.2.13 and also rules hemanta here; the Sun rules an ayana, not a ritu."""
    ruled = set(c.RITU_RULER.values())
    assert Graha.SUN not in ruled
    assert len(ruled) == 6


# --------------------------------------------------------------------------
# 3.2.17 Dhatu, Moola and Jeeva
# --------------------------------------------------------------------------

DMJ = [
    ("dhaatu", "metals and materials",
     (Graha.RAHU, Graha.MARS, Graha.SATURN, Graha.MOON)),
    ("moola", "roots and vegetables", (Graha.SUN, Graha.VENUS)),
    ("jeeva", "living beings", (Graha.MERCURY, Graha.JUPITER, Graha.KETU)),
]


@pytest.mark.parametrize("name,meaning,grahas", DMJ)
def test_3_2_17_each_class(name, meaning, grahas):
    """"Rahu, Mars, Saturn and Moon rule over dhaatus (metals and materials)."
    and the two that follow."""
    index = c.DHATU_MOOLA_JEEVA_NAMES.index(name)
    assert c.DHATU_MOOLA_JEEVA_MEANINGS[index] == meaning
    assert {g for g, v in c.GRAHA_DHATU_MOOLA_JEEVA.items() if v == index} == set(grahas)


def test_3_2_17_covers_all_nine_including_both_nodes():
    """Unlike most of §3.2, this section assigns Rahu and Ketu — and puts them
    in different classes."""
    assert sorted(c.GRAHA_DHATU_MOOLA_JEEVA) == list(range(9))
    dhaatu = c.DHATU_MOOLA_JEEVA_NAMES.index("dhaatu")
    jeeva = c.DHATU_MOOLA_JEEVA_NAMES.index("jeeva")
    assert c.GRAHA_DHATU_MOOLA_JEEVA[Graha.RAHU] == dhaatu
    assert c.GRAHA_DHATU_MOOLA_JEEVA[Graha.KETU] == jeeva


def test_3_2_17_the_dhatu_class_is_not_the_dhatu_of_3_2_12():
    """§3.2.12's "dhaatus" are the seven bodily matters (bones, blood, …);
    §3.2.17's "dhaatus" are metals and materials. Same word, different table,
    and both are keyed by graha — easy to conflate."""
    assert c.GRAHA_DHATU[Graha.SUN] == "bones"
    moola = c.DHATU_MOOLA_JEEVA_NAMES.index("moola")
    assert c.GRAHA_DHATU_MOOLA_JEEVA[Graha.SUN] == moola


# --------------------------------------------------------------------------
# 3.3 Planetary Dignities
# --------------------------------------------------------------------------

#: Table 6 exactly as printed: own, exaltation (deep point), debilitation
#: (deep point), moolatrikona.
TABLE_6 = [
    (Graha.SUN, ("Le",), ("Ar", 10), ("Li", 10), "Le"),
    (Graha.MOON, ("Cn",), ("Ta", 3), ("Sc", 3), "Ta"),
    (Graha.MARS, ("Ar", "Sc"), ("Cp", 28), ("Cn", 28), "Ar"),
    (Graha.MERCURY, ("Ge", "Vi"), ("Vi", 15), ("Pi", 15), "Vi"),
    (Graha.JUPITER, ("Sg", "Pi"), ("Cn", 5), ("Cp", 5), "Sg"),
    (Graha.VENUS, ("Ta", "Li"), ("Pi", 27), ("Vi", 27), "Li"),
    (Graha.SATURN, ("Cp", "Aq"), ("Li", 20), ("Ar", 20), "Aq"),
    (Graha.RAHU, ("Aq",), ("Ge", None), ("Sg", None), "Vi"),
    (Graha.KETU, ("Sc",), ("Sg", None), ("Ge", None), "Pi"),
]


@pytest.mark.parametrize("graha,own,exalt,debil,moola", TABLE_6)
def test_3_3_table_6_row_by_row(graha, own, exalt, debil, moola):
    abbr = list(c.RASI_ABBR)
    assert {int(r) for r in c.GRAHA_OWNS[graha]} == {abbr.index(x) for x in own}
    assert int(c.EXALTATION_RASI[graha]) == abbr.index(exalt[0])
    assert int(c.DEBILITATION_RASI[graha]) == abbr.index(debil[0])
    assert int(c.MOOLATRIKONA[graha][0]) == abbr.index(moola)


@pytest.mark.parametrize("graha,own,exalt,debil,moola", TABLE_6)
def test_3_3_deep_points_are_180_degrees_apart(graha, own, exalt, debil, moola):
    """Table 6 gives the same degree for exaltation and debilitation in every
    row that has one, and the two rasis are always opposite. The nodes are
    given no degree, so they are skipped."""
    if exalt[1] is None:
        assert graha in (Graha.RAHU, Graha.KETU)
        return
    assert exalt[1] == debil[1], "the book prints the same degree for both"
    abbr = list(c.RASI_ABBR)
    assert (abbr.index(exalt[0]) - abbr.index(debil[0])) % 12 == 6


def test_3_3_the_four_dignity_names():
    """"a sign where it is exalted (uchcha), a sign where it is debilitated
    (neecha), a sign that is called its moolatrikona and one or two rasis that
    are owned by it."""
    assert c.DIGNITY_NAMES_SA["exalted"] == "uchcha"
    assert c.DIGNITY_NAMES_SA["debilitated"] == "neecha"
    assert c.DIGNITY_NAMES_SA["moolatrikona"] == "moolatrikona"


def test_3_3_the_three_strong_placements():
    """"A planet is said to be strong in its own rasi or exaltation rasi or
    moolatrikona." Debilitation is not among them."""
    assert set(c.DIGNITY_STRONG_PLACEMENTS) == {"own", "exalted", "moolatrikona"}
    assert "debilitated" not in c.DIGNITY_STRONG_PLACEMENTS
    assert "own rasi or exaltation rasi or moolatrikona" in c.DIGNITY_STRONG_NOTE


ZONES = [
    (Graha.SUN, "Le", [(0, 20, "moolatrikona"), (20, 30, "own")]),
    (Graha.MOON, "Ta", [(0, 3, "exalted"), (3, 30, "moolatrikona")]),
    (Graha.MARS, "Ar", [(0, 12, "moolatrikona"), (12, 30, "own")]),
    (Graha.MERCURY, "Vi", [(0, 15, "exalted"), (15, 20, "moolatrikona"),
                           (20, 30, "own")]),
    (Graha.JUPITER, "Sg", [(0, 10, "moolatrikona"), (10, 30, "own")]),
    (Graha.VENUS, "Li", [(0, 15, "moolatrikona"), (15, 30, "own")]),
    (Graha.SATURN, "Aq", [(0, 20, "moolatrikona"), (20, 30, "own")]),
]


@pytest.mark.parametrize("graha,rasi,zones", ZONES)
def test_3_3_the_seven_special_points(graha, rasi, zones):
    """The seven numbered rules that split one rasi into dignity zones —
    "Sun gives the results of being in moolatrikona in the first 20 deg of Le
    and the results of being in own rasi in the remaining 10 deg", and so on.
    """
    index = list(c.RASI_ABBR).index(rasi)
    actual = [
        (int(r), start, end, name) for r, start, end, name in c.DIGNITY_BY_DEGREE[graha]
    ]
    assert actual == [(index, float(s), float(e), n) for s, e, n in zones]


@pytest.mark.parametrize("graha,rasi,zones", ZONES)
def test_3_3_each_zone_set_tiles_its_rasi(graha, rasi, zones):
    """Every rule accounts for all 30 degrees with no gap and no overlap."""
    edges = [(s, e) for s, e, _ in zones]
    assert edges[0][0] == 0 and edges[-1][1] == 30
    for (_, end), (start, _) in pairwise(edges):
        assert end == start


def test_3_3_mars_zone_is_aries_not_leo():
    """§3.3 rule 3 prints "the first 12 deg of **Le**", but Table 6 gives Mars
    own Ar & Sc and moolatrikona Ar — Mars neither owns Leo nor has it as a
    moolatrikona, and Leo is the Sun's in rule 1. Table beats prose. PVR-4,
    recorded as D-7."""
    rasi = c.DIGNITY_BY_DEGREE[Graha.MARS][0][0]
    assert list(c.RASI_ABBR)[int(rasi)] == "Ar"
    assert int(c.MOOLATRIKONA[Graha.MARS][0]) == list(c.RASI_ABBR).index("Ar")


def test_3_3_only_the_seven_have_degree_zones():
    """The nodes get a moolatrikona sign in Table 6 but no numbered rule."""
    assert sorted(c.DIGNITY_BY_DEGREE) == list(range(7))


def test_3_3_venus_zone_is_stated_as_halves_not_degrees():
    """Rule 6 is the only one given as "the first half" and "the second half"
    rather than in degrees. Fifteen either way."""
    zones = c.DIGNITY_BY_DEGREE[Graha.VENUS]
    assert zones[0][2] == 15.0 == zones[1][1]


def test_3_3_the_analogy_covers_all_four_placements():
    """"Own rasi ... is like one's home ... Moolatrikona ... is like one's
    office ... Exaltation sign ... is like a favorite party/picnic ...
    Debilitation sign ... is like one's worst party."

    Stored because it is what separates three placements that are all "good".
    """
    assert set(c.DIGNITY_ANALOGY) == {"own", "moolatrikona", "exalted", "debilitated"}
    assert "home" in c.DIGNITY_ANALOGY["own"]
    assert "office" in c.DIGNITY_ANALOGY["moolatrikona"]
    assert "picnic" in c.DIGNITY_ANALOGY["exalted"]
    assert "worst party" in c.DIGNITY_ANALOGY["debilitated"]


def test_3_3_the_analogy_keys_match_the_dignity_names():
    """The analogy must be indexable by the same label the calculation
    returns, or it cannot be attached to a result."""
    assert set(c.DIGNITY_ANALOGY) == set(c.DIGNITY_NAMES_SA)


def test_3_3_the_closing_point():
    """"Though all the three are good placements, there is a subtle difference
    in the mood of the planet and the results given by it."""
    assert "subtle difference" in c.DIGNITY_SUBTLE_DIFFERENCE


def test_3_3_jupiters_three_signs_illustrate_the_analogy():
    """The worked examples add no rule — they explain the analogy through
    Jupiter, Mercury and Ketu. Checked against the tables so the prose and the
    data cannot drift: Pisces home, Sagittarius office, Cancer picnic,
    Capricorn worst party.
    """
    abbr = list(c.RASI_ABBR)
    assert abbr.index("Pi") in {int(r) for r in c.GRAHA_OWNS[Graha.JUPITER]}
    assert int(c.MOOLATRIKONA[Graha.JUPITER][0]) == abbr.index("Sg")
    assert int(c.EXALTATION_RASI[Graha.JUPITER]) == abbr.index("Cn")
    assert int(c.DEBILITATION_RASI[Graha.JUPITER]) == abbr.index("Cp")


def test_3_3_mercury_has_virgo_as_both_moolatrikona_and_exaltation():
    """"So Virgo ... is not only his moolatrikona (office), but also his
    exaltation sign (favorite picnic spot)." The only graha where the two
    coincide, which is why rule 4 needs three zones and every other rule two.
    """
    assert c.MOOLATRIKONA[Graha.MERCURY][0] == c.EXALTATION_RASI[Graha.MERCURY]
    assert len(c.DIGNITY_BY_DEGREE[Graha.MERCURY]) == 3
    others = [g for g in range(7) if g != Graha.MERCURY]
    assert all(len(c.DIGNITY_BY_DEGREE[g]) == 2 for g in others)


def test_3_3_ketu_owns_scorpio_and_has_pisces_as_moolatrikona():
    """"he owns the 8th house of the natural zodiac, i.e. Scorpio ... his
    moolatrikona is in the 12th house of the natural zodiac, i.e. Pisces."""
    abbr = list(c.RASI_ABBR)
    assert abbr.index("Sc") in {int(r) for r in c.GRAHA_OWNS[Graha.KETU]}
    assert int(c.MOOLATRIKONA[Graha.KETU][0]) == abbr.index("Pi")


# --------------------------------------------------------------------------
# 3.2.14 to 3.3 are published
# --------------------------------------------------------------------------


def test_the_graha_table_publishes_the_last_sections():
    grahas = client.get("/v1/util/tables/grahas").json()["grahas"]
    by_name = {g["name"]: g for g in grahas}
    assert by_name["Sun"]["taste_examples"] == ["onion", "ginger", "pepper"]
    assert by_name["Mercury"]["taste_examples"] == []
    assert by_name["Saturn"]["dig_bala_house"] == 7
    assert by_name["Venus"]["ritu"] == "vasanta"
    assert by_name["Sun"]["ritu"] is None
    assert by_name["Rahu"]["dhatu_moola_jeeva_meaning"] == "metals and materials"


def test_the_last_section_blocks_are_published():
    body = client.get("/v1/util/tables/grahas").json()
    assert "2nd house" in body["section_3_2_14"]["use"]
    assert body["section_3_2_15"]["name"] == "digbala"
    assert body["section_3_2_15"]["always_strong"] == [3]
    assert body["section_3_2_15"]["malefic_strong_ayana"] == "dakshina"
    assert len(body["section_3_2_16"]["ritus"]) == 6
    assert body["section_3_2_16"]["ritus"][0]["lord_name"] == "Venus"
    assert len(body["section_3_2_17"]["classes"]) == 3
    assert body["section_3_3"]["sanskrit_names"]["exalted"] == "uchcha"
    assert "office" in body["section_3_3"]["analogy"]["moolatrikona"]
