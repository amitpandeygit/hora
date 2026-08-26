"""Grahas, their dignities, relationships and attributes (chapters 1 and 3).

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant — that facade is the
stable internal surface and keeps call sites independent of how the tables are
filed.
"""
from __future__ import annotations

from enum import IntEnum

from hora.core.constants.rasi import Rasi

# --------------------------------------------------------------------------
# Grahas (planets)
# --------------------------------------------------------------------------

class Graha(IntEnum):
    SUN = 0
    MOON = 1
    MARS = 2
    MERCURY = 3
    JUPITER = 4
    VENUS = 5
    SATURN = 6
    RAHU = 7
    KETU = 8
    URANUS = 9
    NEPTUNE = 10
    PLUTO = 11


GRAHA_NAMES = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]
GRAHA_NAMES_SA = [
    "Surya", "Chandra", "Mangala", "Budha", "Guru", "Shukra", "Shani",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]
GRAHA_ABBR = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke", "Ur", "Ne", "Pl"]

#: The seven visible grahas plus the two nodes — the Parashari set.
NAVAGRAHA = tuple(range(9))
#: Grahas that own signs and take part in dignity/aspect logic.
CLASSICAL_SEVEN = tuple(range(7))

#: Sign lordship, indexed by rasi. Parashari (no outer-planet co-lordship).
RASI_LORD = [
    Graha.MARS, Graha.VENUS, Graha.MERCURY, Graha.MOON, Graha.SUN, Graha.MERCURY,
    Graha.VENUS, Graha.MARS, Graha.JUPITER, Graha.SATURN, Graha.SATURN, Graha.JUPITER,
]

#: Signs owned by each graha for dignity purposes (book Table 6).
#:
#: CRITICAL: the nodes are *co-lords* here, not rasi lords. ``RASI_LORD`` still
#: gives Aquarius to Saturn and Scorpio to Mars, and must never be changed —
#: house lordship, argala and dasa lords all depend on it. This table only
#: decides whether a node sits in "its own" sign.
GRAHA_OWNS: dict[int, tuple[int, ...]] = {
    Graha.SUN: (Rasi.LEO,),
    Graha.MOON: (Rasi.CANCER,),
    Graha.MARS: (Rasi.ARIES, Rasi.SCORPIO),
    Graha.MERCURY: (Rasi.GEMINI, Rasi.VIRGO),
    Graha.JUPITER: (Rasi.SAGITTARIUS, Rasi.PISCES),
    Graha.VENUS: (Rasi.TAURUS, Rasi.LIBRA),
    Graha.SATURN: (Rasi.CAPRICORN, Rasi.AQUARIUS),
    Graha.RAHU: (Rasi.AQUARIUS,),
    Graha.KETU: (Rasi.SCORPIO,),
}

#: Grahas whose "ownership" above is secondary. Used to keep node co-lordship
#: from leaking into anything that needs the true rasi lord.
CO_LORDS_ONLY = frozenset({Graha.RAHU, Graha.KETU})

#: 1.3.1's definition of the word: the section is explicit that this is not
#: the astronomical sense — the Sun is a star and the Moon a satellite, and
#: both are grahas.
GRAHA_DEFINITION = (
    "a graha or a planet is a body that has considerable influence on the "
    "living beings on earth"
)
GRAHA_DEFINITION_NOTE = (
    'The words "planet" and "star" are used in a slightly different sense in '
    "astrology than in astronomy. Distant stars have negligible influence on "
    "us, but Sun, Moon and planets in the solar system have a great influence "
    "on our activities."
)

#: 1.3.1: "Rahu and Ketu are not real planets; they are just some mathematical
#: points." Worth storing because it is the reason behind several absences in
#: this codebase — the nodes have no disc, no combustion and no
#: deep-exaltation degree.
NODES_ARE_MATHEMATICAL_POINTS = (
    "Rahu and Ketu are not real planets; they are just some mathematical points"
)

#: 1.3.1: "two 'chaayaa grahas' (shadow planets) are considered in Indian
#: astrology - Rahu and Ketu. These are also called 'the north node' and 'the
#: south node' respectively (or the head and tail of dragon)."
CHAAYAA_GRAHAS = frozenset({Graha.RAHU, Graha.KETU})
CHAAYAA_GRAHA_NAME = "chaayaa graha (shadow planet)"
#: The other names 1.3.1 gives the two nodes.
NODE_ALIASES: dict[int, list[str]] = {
    Graha.RAHU: ["north node", "head of dragon"],
    Graha.KETU: ["south node", "tail of dragon"],
}

#: Deep exaltation point, measured from 0 Aries (book Table 6).
#:
#: The seven classical planets only. Table 6 gives no degree for Rahu or Ketu —
#: it names their exaltation rasi and nothing more — so the nodes are absent
#: here and their fractional exaltation is undefined rather than invented.
EXALTATION_DEG: dict[int, float] = {
    Graha.SUN: 10.0,           # Aries 10
    Graha.MOON: 33.0,          # Taurus 3
    Graha.MARS: 298.0,         # Capricorn 28
    Graha.MERCURY: 165.0,      # Virgo 15
    Graha.JUPITER: 95.0,       # Cancer 5
    Graha.VENUS: 357.0,        # Pisces 27
    Graha.SATURN: 200.0,       # Libra 20
}
#: Debilitation is exactly 180 degrees from exaltation.
DEBILITATION_DEG: dict[int, float] = {
    g: (d + 180.0) % 360.0 for g, d in EXALTATION_DEG.items()
}

#: Exaltation and debilitation *rasi* for all nine grahas (book Table 6).
#: This is what dignity-by-sign uses; the nodes appear only here.
#: DEVIATION: many texts exalt Rahu in Taurus and Ketu in Scorpio. Table 6
#: gives Gemini and Sagittarius. We follow the book. See book-deviations.md D-4.
EXALTATION_RASI: dict[int, int] = {
    **{g: int(d // 30) for g, d in EXALTATION_DEG.items()},
    Graha.RAHU: int(Rasi.GEMINI),
    Graha.KETU: int(Rasi.SAGITTARIUS),
}
DEBILITATION_RASI: dict[int, int] = {
    g: (r + 6) % 12 for g, r in EXALTATION_RASI.items()
}

#: Moolatrikona ranges as (rasi, start_deg_in_sign, end_deg_in_sign).
MOOLATRIKONA: dict[int, tuple[int, float, float]] = {
    Graha.SUN: (Rasi.LEO, 0.0, 20.0),
    Graha.MOON: (Rasi.TAURUS, 3.0, 30.0),
    # PVR-4: section 3.3 rule 3 misprints this as "the first 12 degrees of Le";
    # Table 6 says Aries and a table beats prose. See docs/precedence.md.
    Graha.MARS: (Rasi.ARIES, 0.0, 12.0),
    # DEVIATION: BPHS is commonly read as 16-20. Book section 3.3 rule 4 is
    # explicit that exaltation runs for the first 15 degrees and moolatrikona
    # for the next 5. See book-deviations.md D-5.
    Graha.MERCURY: (Rasi.VIRGO, 15.0, 20.0),
    Graha.JUPITER: (Rasi.SAGITTARIUS, 0.0, 10.0),
    Graha.VENUS: (Rasi.LIBRA, 0.0, 15.0),
    Graha.SATURN: (Rasi.AQUARIUS, 0.0, 20.0),
    # Table 6 gives a moolatrikona rasi for the nodes but no degree range,
    # so the whole sign is used.
    Graha.RAHU: (Rasi.VIRGO, 0.0, 30.0),
    Graha.KETU: (Rasi.PISCES, 0.0, 30.0),
}

#: The seven degree-refined dignity rules of book section 3.3.
#:
#: These matter where a graha's exaltation rasi and moolatrikona rasi are the
#: same sign — Moon in Taurus and Mercury in Virgo — because the degree, not
#: the sign, decides which dignity applies. Checking the sign alone reports
#: Moon as exalted throughout Taurus, which the book does not say.
#:
#: Each entry is an ordered tuple of ``(rasi, start_deg, end_deg, dignity)``
#: covering the whole sign.
DIGNITY_BY_DEGREE: dict[int, tuple[tuple[int, float, float, str], ...]] = {
    Graha.SUN: (
        (Rasi.LEO, 0.0, 20.0, "moolatrikona"),
        (Rasi.LEO, 20.0, 30.0, "own"),
    ),
    Graha.MOON: (
        (Rasi.TAURUS, 0.0, 3.0, "exalted"),
        (Rasi.TAURUS, 3.0, 30.0, "moolatrikona"),
    ),
    Graha.MARS: (
        (Rasi.ARIES, 0.0, 12.0, "moolatrikona"),
        (Rasi.ARIES, 12.0, 30.0, "own"),
    ),
    Graha.MERCURY: (
        (Rasi.VIRGO, 0.0, 15.0, "exalted"),
        (Rasi.VIRGO, 15.0, 20.0, "moolatrikona"),
        (Rasi.VIRGO, 20.0, 30.0, "own"),
    ),
    Graha.JUPITER: (
        (Rasi.SAGITTARIUS, 0.0, 10.0, "moolatrikona"),
        (Rasi.SAGITTARIUS, 10.0, 30.0, "own"),
    ),
    Graha.VENUS: (
        (Rasi.LIBRA, 0.0, 15.0, "moolatrikona"),
        (Rasi.LIBRA, 15.0, 30.0, "own"),
    ),
    Graha.SATURN: (
        (Rasi.AQUARIUS, 0.0, 20.0, "moolatrikona"),
        (Rasi.AQUARIUS, 20.0, 30.0, "own"),
    ),
}

#: Natural benefics/malefics before Moon-phase and association adjustments.
#: PVR-2: section 3.2.2 omits Saturn from the malefics; page 102 corroborates
#: that it is one. Saturn is kept. See docs/precedence.md.
#: 3.2.2's Sanskrit names for the two classes.
BENEFIC_CLASS_NAMES = ("saumya grahas", "subha grahas")
MALEFIC_CLASS_NAMES = ("kroora grahas", "paapa grahas")

NATURAL_BENEFIC = {Graha.JUPITER, Graha.VENUS}
NATURAL_MALEFIC = {Graha.SUN, Graha.MARS, Graha.SATURN, Graha.RAHU, Graha.KETU}
# Moon and Mercury are conditional; see charts.dignity.

#: PVR-3: the Exercise 6 answer calls Venus a natural neutral of Jupiter; this
#: table calls it an enemy, and section 3.4.1's derivation rule reproduces this
#: table in all seven rows. See docs/precedence.md.
#:
#: Naisargika (natural) friendship: 2 = friend, 1 = neutral, 0 = enemy.
#: Rows and columns are indexed by Graha for the classical seven.
NATURAL_RELATION: dict[int, dict[int, int]] = {
    Graha.SUN:     {Graha.SUN: 2, Graha.MOON: 2, Graha.MARS: 2, Graha.MERCURY: 1, Graha.JUPITER: 2, Graha.VENUS: 0, Graha.SATURN: 0},
    Graha.MOON:    {Graha.SUN: 2, Graha.MOON: 2, Graha.MARS: 1, Graha.MERCURY: 2, Graha.JUPITER: 1, Graha.VENUS: 1, Graha.SATURN: 1},
    Graha.MARS:    {Graha.SUN: 2, Graha.MOON: 2, Graha.MARS: 2, Graha.MERCURY: 0, Graha.JUPITER: 2, Graha.VENUS: 1, Graha.SATURN: 1},
    Graha.MERCURY: {Graha.SUN: 2, Graha.MOON: 0, Graha.MARS: 1, Graha.MERCURY: 2, Graha.JUPITER: 1, Graha.VENUS: 2, Graha.SATURN: 1},
    Graha.JUPITER: {Graha.SUN: 2, Graha.MOON: 2, Graha.MARS: 2, Graha.MERCURY: 0, Graha.JUPITER: 2, Graha.VENUS: 0, Graha.SATURN: 1},
    Graha.VENUS:   {Graha.SUN: 0, Graha.MOON: 0, Graha.MARS: 1, Graha.MERCURY: 2, Graha.JUPITER: 1, Graha.VENUS: 2, Graha.SATURN: 2},
    Graha.SATURN:  {Graha.SUN: 0, Graha.MOON: 0, Graha.MARS: 0, Graha.MERCURY: 2, Graha.JUPITER: 1, Graha.VENUS: 2, Graha.SATURN: 2},
}

# --------------------------------------------------------------------------
# Graha attributes (book chapter 3)
#
# Transcribed from "Vedic Astrology: An Integrated Approach", chapter 3.
# Departures from the printed text are listed in docs/book-deviations.md.
# Indices are Graha values; entries are None where the book gives nothing.
# --------------------------------------------------------------------------

#: 3.2.1 Incarnation of Vishnu each graha's essence produced.
GRAHA_AVATARA: dict[int, str] = {
    Graha.SUN: "Rama", Graha.MOON: "Krishna", Graha.MARS: "Narasimha",
    Graha.MERCURY: "Buddha", Graha.JUPITER: "Vaamana", Graha.VENUS: "Parasu Rama",
    Graha.SATURN: "Koorma", Graha.RAHU: "Varaaha", Graha.KETU: "Matsya",
}
#: 3.2.1's parenthetical description of each avatara. Four of the nine are
#: given none in the text — Parasu Rama, Rama, Krishna and Buddha — so those
#: entries are absent rather than invented.
AVATARA_DESCRIPTIONS: dict[str, str] = {
    "Matsya": "fish",
    "Koorma": "tortoise",
    "Varaaha": "boar",
    "Narasimha": "half-man, half-lion",
    "Vaamana": "learned dwarf",
}

#: 3.2.1 Avataras said to carry only paramaatmaamsa (supreme essence).
PURE_PARAMATMAMSA_AVATARAS = ("Rama", "Krishna", "Narasimha", "Varaaha")

#: 3.2.1 names several avataras twice, as "Meena/Matsya", "Varaaha/sookara",
#: "Narasimha/Nrisimha" and "Parasu Rama/Bhaargava Rama". Keyed by the name
#: stored in GRAHA_AVATARA above.
AVATARA_ALIASES: dict[str, list[str]] = {
    "Matsya": ["Meena"],
    "Varaaha": ["Sookara"],
    "Narasimha": ["Nrisimha"],
    "Parasu Rama": ["Bhaargava Rama"],
}

#: 3.2.6 names each ruling deity with its office. Keyed as GRAHA_DEITY.
GRAHA_DEITY_ROLE: dict[int, str] = {
    Graha.SUN: "fire god",
    Graha.MOON: "rain god",
    Graha.MARS: "army chief of gods",
    Graha.MERCURY: "supreme sustaining force",
    Graha.JUPITER: "ruler of gods",
    Graha.VENUS: "Indra's wife",
    Graha.SATURN: "Creator",
}

#: 3.2.4: "These colors can be useful, for example, when predicting the color
#: of one's car. For now, readers should just memorize these characteristics."
GRAHA_COLOR_USE = (
    "These colors can be useful, for example, when predicting the color of "
    "one's car."
)

#: 3.2.7's worked example, which is the strongest internal evidence that
#: Mercury is neuter and not female as the section's third sentence prints.
#: See D-6 in docs/book-deviations.md.
SEX_PREDICTION_NOTE = (
    "This information can be used for predicting the sex of children based on "
    "one's chart. For example, if the house ruling the first child is "
    "influenced by Jupiter, Mars and Mercury, we may predict a son. If it is "
    "influenced by Moon and Mercury, we may predict a daughter."
)

#: 3.2.3 Principal significations.
GRAHA_GOVERNS: dict[int, str] = {
    Graha.SUN: "soul", Graha.MOON: "mind", Graha.MARS: "strength",
    Graha.MERCURY: "speech", Graha.JUPITER: "knowledge and happiness",
    Graha.VENUS: "potency", Graha.SATURN: "grief",
}

#: 3.2.4 Colours, in the book's own wording.
GRAHA_COLOR: dict[int, str] = {
    Graha.SUN: "blood-red color", Graha.MOON: "tawny color",
    Graha.MARS: "blood-red color", Graha.MERCURY: "grass green color",
    Graha.JUPITER: "tawny color", Graha.VENUS: "variegated",
    Graha.SATURN: "black color",
}

#: 3.2.5 Planetary cabinet.
GRAHA_CABINET: dict[int, str] = {
    Graha.SUN: "king", Graha.MOON: "king", Graha.MARS: "leader (army chief)",
    Graha.MERCURY: "prince", Graha.JUPITER: "minister", Graha.VENUS: "minister",
    Graha.SATURN: "servant", Graha.RAHU: "army", Graha.KETU: "army",
}

#: 3.2.6 Ruling deities.
GRAHA_DEITY: dict[int, str] = {
    Graha.SUN: "Agni", Graha.MOON: "Varuna", Graha.MARS: "Subrahmanya",
    Graha.MERCURY: "Maha Vishnu", Graha.JUPITER: "Indra",
    Graha.VENUS: "Sachi Devi", Graha.SATURN: "Brahma",
}

#: 3.2.7 Sex of the grahas.
#:
#: DEVIATION FROM THE BOOK: section 3.2.7 prints "Saturn and Mercury are
#: female" immediately after "Moon and Venus are female". Two groups cannot
#: both be the female group, and the classical value is neuter (napumsaka).
#: Recorded as neuter by explicit decision. See book-deviations.md D-6.
SEX_NAMES = ("male", "female", "neuter")
GRAHA_SEX: dict[int, int] = {
    Graha.SUN: 0, Graha.MARS: 0, Graha.JUPITER: 0,
    Graha.MOON: 1, Graha.VENUS: 1,
    Graha.MERCURY: 2, Graha.SATURN: 2,
}

#: 3.2.8 Elements. Five here, not four: ether (aakaasa) is a graha element.
PLANET_ELEMENT_NAMES = ("fire", "earth", "air", "water", "ether")
PLANET_ELEMENT_NAMES_SA = ("agni", "bhoo", "vaayu", "jala", "aakaasa")
#: 3.2.8 writes each as "<Sanskrit> tattva (<adjective> element)", e.g.
#: "Aakaasa tattva (ethery element) is ruled by Jupiter".
PLANET_ELEMENT_ADJECTIVES = ("fiery", "earthy", "airy", "watery", "ethery")
PLANET_ELEMENT_TATTVAS = tuple(f"{name} tattva" for name in PLANET_ELEMENT_NAMES_SA)
#: The graha that *rules* each element.
ELEMENT_RULER: dict[int, int] = {
    0: Graha.MARS, 1: Graha.MERCURY, 2: Graha.SATURN, 3: Graha.VENUS, 4: Graha.JUPITER,
}
#: Element of each graha. Sun shares Mars's fiery nature and Moon shares
#: Venus's watery nature without ruling those elements.
GRAHA_ELEMENT: dict[int, int] = {
    Graha.MARS: 0, Graha.SUN: 0, Graha.MERCURY: 1, Graha.SATURN: 2,
    Graha.VENUS: 3, Graha.MOON: 3, Graha.JUPITER: 4,
}
#: Grahas that share an element's nature but do not rule it.
ELEMENT_SHARERS = frozenset({Graha.SUN, Graha.MOON})

#: 3.2.9 Varnas. Same four names as the rasi varnas.
GRAHA_VARNA: dict[int, int] = {
    Graha.JUPITER: 0, Graha.VENUS: 0,        # brahmana
    Graha.SUN: 1, Graha.MARS: 1,             # kshatriya
    Graha.MOON: 2, Graha.MERCURY: 2,         # vaisya
    Graha.SATURN: 3,                         # sudra
}

#: 3.2.10 Trigunas.
GRAHA_GUNA: dict[int, int] = {
    Graha.SUN: 0, Graha.MOON: 0, Graha.JUPITER: 0,     # sattwa
    Graha.MERCURY: 1, Graha.VENUS: 1,                  # rajas
    Graha.MARS: 2, Graha.SATURN: 2,                    # tamas
}

#: 3.2.11 Abodes. The book gives no abode for Mars; see book-deviations.md D-7.
GRAHA_ABODE: dict[int, str | None] = {
    Graha.SUN: "temple", Graha.MOON: "watery place", Graha.MARS: None,
    Graha.MERCURY: "sports ground", Graha.JUPITER: "treasure house",
    Graha.VENUS: "bedroom", Graha.SATURN: "filthy area",
}

#: 3.2.12 The seven dhaatus that make up the body.
GRAHA_DHATU: dict[int, str] = {
    Graha.SUN: "bones", Graha.MOON: "blood", Graha.MARS: "marrow",
    Graha.MERCURY: "skin", Graha.JUPITER: "fat", Graha.VENUS: "semen",
    Graha.SATURN: "muscles",
}

#: 3.2.8: "These rulerships throw light on the basic nature of planets", then
#: one clause per element ruler. Keyed by the ruling graha, not by element:
#: the book attaches each to the planet, and Sun and Moon get none because
#: they only "also have the same nature" as Mars and Venus.
ELEMENT_GOVERNANCE: dict[int, str] = {
    Graha.MARS: "leadership, enterprise",
    Graha.MERCURY: "memory, logical abilities",
    Graha.SATURN: "wandering and free spirit",
    Graha.VENUS: "imaginative and creative work",
    Graha.JUPITER: "wisdom, intelligence and perceiving knowledge",
}
ELEMENT_GOVERNANCE_NOTE = (
    "These rulerships throw light on the basic nature of planets."
)

#: 3.2.8 gives each tattva one ruler, then adds a second graha to two of them:
#: "Agni tattva ... is ruled by Mars. Sun also has the same nature." and
#: "Jala tattva ... is ruled by Venus. Moon also has the same nature." Those
#: two share the element without ruling it, which is why ELEMENT_RULER has one
#: entry per element while GRAHA_ELEMENT has seven.
SHARES_ELEMENT_WITHOUT_RULING = frozenset({Graha.SUN, Graha.MOON})
SHARES_ELEMENT_PHRASE = "also has the same nature"

#: 3.2.9's gloss for each varna, which is **not** the gloss 2.2.12 uses.
#: 2.2.12: "Brahmanas (scholars) ... Sudras (workers)".
#: 3.2.9:  "Brahmanas (learned) ... Saturn is a Sudra (worker)".
#: Both are the book's own; neither is normalised into the other.
VARNA_NAMES_EN_3_2_9 = ["learned", "warriors", "traders", "worker"]

#: 3.2.9: what each class is good at. Indexed as VARNA_NAMES.
VARNA_FORTE = [
    "Learning and intelligence is the forte of the learned class.",
    "Bravery is the forte of the warrior class.",
    "Getting along with others well is the forte of the trader class.",
    "Hard work is the forte of the working class.",
]

#: 3.2.9: "In this manner, we should understand varnas to show one's basic
#: nature rather than the caste of one's family."
VARNA_MEANS_NATURE_NOT_CASTE = (
    "In this manner, we should understand varnas to show one's basic nature "
    "rather than the caste of one's family."
)

#: 3.2.9 flags its own apparent contradiction with 3.2.5, and resolves it.
VARNA_CABINET_NOTE = (
    "It should be noted that Moon, who was earlier classified in the "
    "planetary cabinet as a king, is said here to be of Vaisya varna. Sun is "
    "a king who is also a warrior. He is a brave king, who asserts himself. "
    "But Moon is a king who gets along well with everyone."
)

#: 3.2.10's closing definitions, indexed as GUNA_NAMES.
GUNA_DEFINITIONS = [
    (
        "Sattva guna simply means purity and truthfulness in one's thoughts "
        "and action."
    ),
    (
        "Rajo guna shows some passion, energy and impurity in thoughts and "
        "actions."
    ),
    (
        "Tamo guna shows a dark, mean and depraved spirit in thoughts and "
        "actions."
    ),
]

#: 3.2.10's NOTE, which corrects a common reading of sattwa. Kept whole
#: because its point is the whole argument, not any one clause.
SATTWA_MISCONCEPTION_NOTE = (
    "There is a misconception today that sattwa guna means patience and not "
    "hurting others. An aggressive response to an offender is often thought "
    "to be raajasik. However, sattwa simply means \u201cthe state of being "
    "true\u201d. Pleasing others with artificial goodness is not sattwa guna. "
    "Punishing a person for his mistakes is not necessarily rajo guna. If "
    "there is some passion and impurity in one's energetic response, then it "
    "shows rajo guna. But, if a warrior fights a sinning person with no "
    "passion or ego, it can still be a saattvic act. Lord Sri Rama and Sun "
    "are examples for this. Sun is a king of the warrior class and yet he is "
    "saattwik. Lord Rama, who was born with his amsa, is a saattwik person "
    "despite killing Ravana and other demons."
)
SATTWA_MEANING = "the state of being true"

#: 3.2.11: "This description should give one an idea of the nature of planets."
ABODE_NOTE = "This description should give one an idea of the nature of planets."

#: 3.2.12: "Sapta dhaatus or 7 matters make up human body."
SAPTA_DHATU_NAME = "sapta dhaatus"
SAPTA_DHATU_NOTE = "Sapta dhaatus or 7 matters make up human body."

#: 3.2.12 glosses one of the seven and no others.
DHATU_DESCRIPTIONS: dict[int, str] = {
    Graha.VENUS: "materials related to the reproductive system",
}

#: 3.2.12: "If Sun is afflicted, it can show some problems related to bones.
#: Weakness of Moon may give blood related problems. And so on."
DHATU_AFFLICTION_NOTE = (
    "If Sun is afflicted, it can show some problems related to bones. "
    "Weakness of Moon may give blood related problems. And so on."
)

#: 3.2.13 Time period each graha rules. Used in prasna.
GRAHA_TIME_PERIOD: dict[int, str] = {
    Graha.SUN: "ayana", Graha.MOON: "minute", Graha.MARS: "week",
    Graha.MERCURY: "ritu", Graha.JUPITER: "month", Graha.VENUS: "fortnight",
    Graha.SATURN: "year",
}

#: 3.2.14 Tastes.
GRAHA_TASTE: dict[int, str] = {
    Graha.SUN: "pungent", Graha.MOON: "saline", Graha.MARS: "bitter",
    Graha.MERCURY: "mixed", Graha.JUPITER: "sweet", Graha.VENUS: "sour",
    Graha.SATURN: "astringent",
}

#: 3.2.15 Grahas strong at night, by day, and always. Feeds divaratri bala.
STRONG_AT_NIGHT = frozenset({Graha.MOON, Graha.MARS, Graha.SATURN})
STRONG_BY_DAY = frozenset({Graha.SUN, Graha.JUPITER, Graha.VENUS})
STRONG_ALWAYS = frozenset({Graha.MERCURY})

#: 3.2.15 Paksha strength: natural benefics are strong in Sukla paksha,
#: natural malefics in Krishna paksha. Indices match PAKSHA_NAMES.
BENEFIC_STRONG_PAKSHA = 0        # sukla
MALEFIC_STRONG_PAKSHA = 1        # krishna

#: 3.2.14's examples for each taste. Mercury's "mixed taste" is given none.
TASTE_EXAMPLES: dict[int, list[str]] = {
    Graha.SUN: ["onion", "ginger", "pepper"],
    Graha.MOON: ["sea salt", "rock salt"],
    Graha.MARS: ["karela/bitter melon", "dandelion root", "rhubarb root",
                 "neem leaves"],
    Graha.JUPITER: ["sugar", "dates"],
    Graha.VENUS: ["lemon", "tamarind"],
    Graha.SATURN: ["plantain", "pomegranate"],
}

#: 3.2.14: the 2nd house shows food preference, and a graha's taste is worth
#: avoiding while that graha is bringing trouble.
TASTE_USE = (
    "The 2nd house shows one's preference in food. The planets influencing it "
    "may decide one's favorite taste. In addition, one should avoid the "
    "tastes of the planets who are likely bring disease."
)

#: 3.2.15's name for the direction strengths, and what they mean.
DIG_BALA_NAME = "digbala"
DIG_BALA_NOTE = (
    "These are the digbalas (strengths associated with direction) of planets. "
    "These show the direction taken by one in one's life."
)

#: 3.2.15: "Mercury is always strong", the only graha with no day/night half.
ALWAYS_STRONG_NOTE = "Mercury is always strong."

#: 3.2.16 frames the ritu rulerships and glosses each season; RITU_MEANINGS
#: holds the glosses.
RITU_RULERSHIP_NOTE = "Planetary rulerships over ritus (seasons)."

#: 3.2.17's parenthetical for each of the three classes, indexed as
#: DHATU_MOOLA_JEEVA_NAMES.
DHATU_MOOLA_JEEVA_MEANINGS = (
    "metals and materials", "roots and vegetables", "living beings",
)

#: 3.3: "A planet is said to be strong in its own rasi or exaltation rasi or
#: moolatrikona."
DIGNITY_STRONG_PLACEMENTS = ("own", "exalted", "moolatrikona")
DIGNITY_STRONG_NOTE = (
    "A planet is said to be strong in its own rasi or exaltation rasi or "
    "moolatrikona."
)

#: 3.3's analogy for the four placements, which is what separates them. Keyed
#: by the dignity name used in DIGNITY_BY_DEGREE and DIGNITY_NAMES_SA.
DIGNITY_ANALOGY = {
    "own": "one's home — most natural and comfortable",
    "moolatrikona": "one's office — powerful and duty-minded",
    "exalted": "one's favorite party/picnic — excited",
    "debilitated": "one's worst party — unhappy, stuck at a place he hates",
}

#: 3.3's closing point, and the reason the analogy is worth storing at all.
DIGNITY_SUBTLE_DIFFERENCE = (
    "Though all the three are good placements, there is a subtle difference "
    "in the mood of the planet and the results given by it."
)

#: 3.2.13: "These periods are very useful in prasna or horary astrology."
TIME_PERIOD_USE = (
    "These periods are very useful in prasna or horary astrology."
)

#: Footnote 5: the year has two ayanas. The Sun's transit from Capricorn to
#: Gemini is Uttara (north) ayana; from Cancer to Sagittarius, Dakshina (south).
AYANA_NAMES = ("uttara", "dakshina")
RASI_AYANA = [0 if r in (9, 10, 11, 0, 1, 2) else 1 for r in range(12)]

#: 3.2.15 Ayana strength: natural benefics are strong in Uttara ayana,
#: natural malefics in Dakshina ayana.
BENEFIC_STRONG_AYANA = 0         # uttara
MALEFIC_STRONG_AYANA = 1         # dakshina

#: 3.2.16 Ritus (seasons), in the book's order.
RITU_NAMES = ("vasanta", "greeshma", "varsha", "hemanta", "seeta", "sisira")
RITU_MEANINGS = ("spring", "summer", "rainy season", "season of dew", "winter", "fall")
#: Footnote 6: six ritus in a year, each of two months.
RITU_MONTHS = 2
RITU_RULER: dict[int, int] = {
    0: Graha.VENUS, 1: Graha.MARS, 2: Graha.MOON,
    3: Graha.MERCURY, 4: Graha.JUPITER, 5: Graha.SATURN,
}

#: 3.2.17 Dhaatu (metals), moola (roots) and jeeva (living beings).
DHATU_MOOLA_JEEVA_NAMES = ("dhaatu", "moola", "jeeva")
GRAHA_DHATU_MOOLA_JEEVA: dict[int, int] = {
    Graha.RAHU: 0, Graha.MARS: 0, Graha.SATURN: 0, Graha.MOON: 0,
    Graha.SUN: 1, Graha.VENUS: 1,
    Graha.MERCURY: 2, Graha.JUPITER: 2, Graha.KETU: 2,
}

#: §3.4 names the three kinds of relationship and the five compound results.
#: Our internal labels are English; these are the book's own terms, so a client
#: can render either. Table 8 supplies the compound names.
RELATIONSHIP_KINDS = {
    "natural": "naisargika",
    "temporary": "tatkaala",
    "compound": "panchadha",
}

#: Table 7's column headings.
NATURAL_RELATION_NAMES = {2: "mitra", 1: "sama", 0: "satru"}

#: Table 8's five outcomes, keyed by our internal label.
COMPOUND_RELATION_NAMES = {
    "great_friend": "adhimitra",
    "friend": "mitra",
    "neutral": "sama",
    "enemy": "satru",
    "great_enemy": "adhisatru",
}

#: Table 8's own glosses for each outcome.
COMPOUND_RELATION_GLOSSES = {
    "great_friend": "good friend",
    "friend": "friend",
    "neutral": "neutral",
    "enemy": "enemy",
    "great_enemy": "bad enemy",
}

#: §3.3's Sanskrit dignity terms.
DIGNITY_NAMES_SA = {
    "exalted": "uchcha",
    "debilitated": "neecha",
    "moolatrikona": "moolatrikona",
    "own": "swakshetra",
}

#: §3.2.1 — the two essences a graha's amsa carries.
ESSENCE_NAMES = {
    "jeeva": "jeevaamsa (living essence)",
    "paramaatma": "paramaatmaamsa (absolute and supreme essence)",
}

#: §3.2.1 writes the living essence as "jeevaamsa" on its first use and
#: "jeevaatmaamsa" on the next page. Both refer to the same thing.
ESSENCE_ALIASES: dict[str, list[str]] = {
    "jeeva": ["jeevaatmaamsa"],
    "paramaatma": [],
}

#: Graha drishti (special aspects) in houses counted from the graha's own house.
#: Every graha aspects the 7th; these are the additional full aspects.
SPECIAL_ASPECTS: dict[int, tuple[int, ...]] = {
    Graha.MARS: (4, 8),
    Graha.JUPITER: (5, 9),
    Graha.SATURN: (3, 10),
    Graha.RAHU: (5, 9),   # optional in JHora; gated by settings.rahu_ketu_aspects
    Graha.KETU: (5, 9),
}

#: Combustion (astangata) orbs in degrees from the Sun, JHora defaults.
#: Separate orbs apply when the planet is retrograde.
COMBUSTION_ORB: dict[int, tuple[float, float]] = {
    Graha.MOON: (12.0, 12.0),
    Graha.MARS: (17.0, 17.0),
    Graha.MERCURY: (14.0, 12.0),
    Graha.JUPITER: (11.0, 11.0),
    Graha.VENUS: (10.0, 8.0),
    Graha.SATURN: (15.0, 15.0),
}

#: Directional strength (dig bala) — house of maximum strength, 1-indexed.
DIG_BALA_STRONG_HOUSE: dict[int, int] = {
    Graha.SUN: 10, Graha.MARS: 10,
    Graha.MOON: 4, Graha.VENUS: 4,
    Graha.MERCURY: 1, Graha.JUPITER: 1,
    Graha.SATURN: 7,
}
