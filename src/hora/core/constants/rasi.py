"""Rasis and their attributes (book chapters 1 and 2).

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant — that facade is the
stable internal surface and keeps call sites independent of how the tables are
filed.
"""
from __future__ import annotations

from enum import IntEnum

# --------------------------------------------------------------------------
# Rasis (signs)
# --------------------------------------------------------------------------

RASI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
RASI_NAMES_SA = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrischika", "Dhanus", "Makara", "Kumbha", "Meena",
]
RASI_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

#: Sanskrit rasi names exactly as printed in Table 1 of the book. Where the
#: book gives two forms ("Vrishabha/Vrisha"), the first is used.
RASI_NAMES_SA_BOOK = [
    "Mesha", "Vrishabha", "Mithuna", "Karkataka", "Simha", "Kanya",
    "Thula", "Vrischika", "Dhanus", "Makara", "Kumbha", "Meena",
]

# 0 = movable (chara), 1 = fixed (sthira), 2 = dual (dwisvabhava)
RASI_MODALITY = [0, 1, 2] * 4
# 0 = fire, 1 = earth, 2 = air, 3 = water
RASI_ELEMENT = [0, 1, 2, 3] * 3
# True when the sign is odd (vishama / male); Aries is index 0 and is odd.
RASI_IS_ODD = [i % 2 == 0 for i in range(12)]


# --------------------------------------------------------------------------
# Rasi attributes (book chapter 2)
#
# Every table below is transcribed from "Vedic Astrology: An Integrated
# Approach", chapter 2, and follows the book exactly. Where the book departs
# from a convention held elsewhere, the departure is kept and flagged rather
# than silently corrected — see docs/book-deviations.md.
# --------------------------------------------------------------------------

#: 2.2.1's opening claim, which the limb table rests on.
ZODIAC_AS_VISHNU = (
    "The whole zodiac is nothing but a manifestation of Lord Vishnu's body."
)

#: 2.2.1: why the limbs bear on a chart at all. "Because we are all part of
#: the Supreme energy governing this world, the above mapping applies to us
#: too. For example, we should pay attention to Leo for analyzing stomach
#: problems and to Pisces for analyzing problems related to feet and so on."
LIMB_APPLIES_TO_NATIVE = (
    "Because we are all part of the Supreme energy governing this world, the "
    "above mapping applies to us too."
)

#: 2.2.1 Limbs of the kaala purusha (Vishnu's body), by rasi.
#: PVR-1: section 2.3 calls Gemini's limb "chest"; 2.2.1 defines it as "arms"
#: and a definitional section wins. See docs/precedence.md.
RASI_LIMB = [
    "head", "face", "arms", "heart", "stomach", "hip",
    "space below navel", "private parts", "thighs", "knees", "ankles", "feet",
]

#: 2.2.2 gives *four* names for each half, not two. "Ar, Ge, Le, Li, Sg and
#: Aq are called odd rasis or vishama rasis or oja rasis. They are also known
#: as male rasis." Index 0 is the odd half, index 1 the even half.
#: Do not confuse this split with 2.2.3's odd-footed/even-footed, which is a
#: different partition of the same twelve signs.
ODD_EVEN_NAMES = [
    ["odd", "vishama", "oja", "male"],
    ["even", "sama", "yugma", "female"],
]

#: 2.2.2: "This division is used in some dasas and in the determination of
#: the sex of children."
ODD_EVEN_USE = (
    "This division is used in some dasas and in the determination of the sex "
    "of children."
)

#: 2.2.3 Odd-footed (vishamapada) vs even-footed (samapada).
#: Ar, Ta, Ge, Li, Sc, Sg are odd-footed; the rest are even-footed.
#: Note this is NOT the same split as odd/even rasis in 2.2.2.
RASI_IS_ODD_FOOTED = [i in (0, 1, 2, 6, 7, 8) for i in range(12)]

#: 1.3.2: "Many western astrologers consider Sayana or tropical (moving)
#: zodiac, whereas Nirayana or sidereal (fixed) zodiac is considered in Vedic
#: astrology." Hora computes in the nirayana zodiac throughout; sayana is
#: recorded only so the distinction the book draws has a name in the code.
ZODIAC_NAMES = {
    "nirayana": "sidereal (fixed) zodiac — the one Vedic astrology uses",
    "sayana": "tropical (moving) zodiac",
}
ZODIAC_USED = "nirayana"

#: 2.2.3 gives *three* names for each half, not two. "Ar, Ta, Ge, Li, Sc and
#: Sg are called odd-footed rasis or vishamapada rasis or ojapada rasis."
#: Index 0 is the odd-footed half, index 1 the even-footed half.
FOOTED_NAMES = [
    ["odd-footed", "vishamapada", "ojapada"],
    ["even-footed", "samapada", "yugmapada"],
]

#: 2.2.3: "This division is used in some dasas." Note it says only dasas,
#: where 2.2.2 also names the sex of children.
FOOTED_USE = "This division is used in some dasas."

#: 2.2.4 Presiding deity of each modality: movable Brahma, fixed Shiva,
#: dual Vishnu.
MODALITY_DEITY = ["Brahma", "Shiva", "Vishnu"]
MODALITY_NAMES = ["chara", "sthira", "dwiswabhava"]

#: 2.2.4 names each deity by role: "Brahma, the Creator", "Shiva, the
#: Destroyer", "Vishnu, the Sustainer". Indexed as MODALITY_DEITY.
MODALITY_DEITY_ROLE = ["Creator", "Destroyer", "Sustainer"]

#: 2.2.4's English name for each modality, indexed as MODALITY_NAMES.
MODALITY_NAMES_EN = ["movable", "fixed", "dual"]

#: 2.2.4 states a nature for each modality, not only a deity.
MODALITY_NATURE = [
    "Their nature is to move and to be dynamic.",
    "Their nature is to be stable and constant.",
    "They are stable sometimes and dynamic sometimes.",
]

#: Footnote 3 to 2.2.4, which explains the three deities.
TRINITY_NOTE = (
    "Brahma, Vishnu and Shiva together form the Trinity of Hindu Gods. "
    "Brahma creates the world. Vishnu sustains it. Shiva destroys it."
)

#: 2.2.5 Element names, indexed as RASI_ELEMENT. Ether (aakaasa) is said to
#: be present in every rasi and so is not a separate index.
ELEMENT_NAMES = ["fire", "earth", "air", "water"]
ELEMENT_NAMES_SA = ["agni", "bhoo", "vaayu", "jala"]

#: 2.2.5 (5): "The 5th element of aakaasa or ether is present in every rasi."
#: It is deliberately not an index in RASI_ELEMENT — it belongs to all twelve,
#: so a rasi's element is one of four while ether is universal.
ETHER_NAME = "ether"
ETHER_NAME_SA = "aakaasa"
ETHER_IN_EVERY_RASI = (
    "The 5th element of aakaasa or ether is present in every rasi."
)

#: 2.2.5 defines each element by the *state* it describes, which is what makes
#: the classification usable. Keyed by element name, ether included.
ELEMENT_DEFINITIONS = {
    "fire": "Fire is a substance that transforms the state of things.",
    "earth": "Earth is a substance with a constant and solid state.",
    "air": "Air is a substance with a varying state.",
    "water": "Water is a substance with a flexible state.",
    "ether": "Ether is something that is present everywhere.",
}

#: 2.2.5: "These 5 elements are behind every material substance, every action,
#: every thought, every emotion and every happening in this universe."
ELEMENTS_UNDERLIE_EVERYTHING = (
    "These 5 elements are behind every material substance, every action, "
    "every thought, every emotion and every happening in this universe."
)

#: The five as the book lists them: "fire, water, air, earth and ether".
#: This order is the book's prose order, not RASI_ELEMENT's index order.
FIVE_ELEMENTS_BOOK_ORDER = ["fire", "water", "air", "earth", "ether"]

#: 2.2.6: "Ayurveda is India's Vedic medical system that recognizes human body
#: and everything else in the universe as having 3 natures that are formed
#: with the above 5 elements."
AYURVEDA_NOTE = (
    "Ayurveda is India's Vedic medical system that recognizes human body and "
    "everything else in the universe as having 3 natures that are formed with "
    "the above 5 elements."
)

#: 2.2.6 Ayurvedic humour: 0 pitta, 1 vaata, 2 kapha, 3 mixed.
#:
#: DEVIATION: §2.2.6 states the compositions itself — pitta is fire+water,
#: vaata is air+ether, kapha is earth+water — and then assigns *earthy* signs
#: to vaata and *watery* signs to kapha, which those compositions do not give.
#: Airy signs, which the composition would put in vaata, are called "mixed".
#: The inconsistency is inside the section, not between the book and modern
#: Ayurveda. The book's assignment is kept verbatim. See D-1 in
#: docs/book-deviations.md.
DOSHA_NAMES = ["pitta", "vaata", "kapha", "mixed"]
RASI_DOSHA = [0, 1, 3, 2, 0, 1, 3, 2, 0, 1, 3, 2]

#: 2.2.6's English name for each humour. "Mixed" has none — the book names it
#: only as a mixture, so the fourth entry is None rather than an invention.
DOSHA_NAMES_EN: list[str | None] = ["bilious", "windy", "phlegmatic", None]

#: 2.2.6's stated composition of each humour, indexed as DOSHA_NAMES. Note
#: these do **not** predict the sign assignment above; see D-1.
DOSHA_ELEMENTS: list[list[str] | None] = [
    ["fire", "water"], ["air", "ether"], ["earth", "water"], None,
]

#: 2.2.6: what each humour shows, and its example in a human body.
DOSHA_SHOWS: list[str | None] = [
    "It shows things that result in tranformation in a system.",
    "It shows things that move in and out of a system.",
    (
        "It shows things that bind a system together. It shows things that "
        "give a structure to a system."
    ),
    None,
]
DOSHA_BODY_EXAMPLE: list[str | None] = [
    "digestion", "breathing", "bones, muscles, fat", None,
]

#: The book prints "tranformation" for "transformation" in the pitta sentence.
#: Kept as printed in DOSHA_SHOWS; recorded here so it is a known typo and not
#: mistaken for ours.
DOSHA_SHOWS_TYPO = "tranformation"

#: 2.2.7: "everything in this universe has one of 3 gunas (qualities). They
#: are called trigunas."
TRIGUNA_NAME = "trigunas"
TRIGUNA_NOTE = (
    "In Hindu philosophy, everything in this universe has one of 3 gunas "
    "(qualities). They are called trigunas."
)

#: 2.2.7 Triguna: 0 sattwa, 1 rajas, 2 tamas.
GUNA_NAMES = ["sattwa", "rajas", "tamas"]

#: 2.2.7's second name for the last two: "Rajas or rajo guna", "Tamas or tamo
#: guna". Sattwa is given no alternate, so its entry is None.
GUNA_NAMES_ALT: list[str | None] = [None, "rajo guna", "tamo guna"]

#: 2.2.7's one-word gloss for each guna.
GUNA_MEANINGS = ["purity", "energy", "darkness"]

#: 2.2.7: what each guna does to a person.
GUNA_EFFECTS = [
    "a quality that gives truthfulness and purity",
    "a quality that makes one energetic and passionate",
    "a quality that makes one depraved",
]

#: The adjectival forms the book uses when describing a person or a graha —
#: "a saattwik person", "raajasik nature". Spelled several ways in the text;
#: the first entry is the dominant spelling and the rest are its variants.
GUNA_ADJECTIVES = [
    ["saattwik", "saattvic", "sattwik"],
    ["raajasik", "rajasik"],
    ["taamasik", "tamasik"],
]
RASI_GUNA = [1, 1, 2, 0, 0, 2, 1, 1, 0, 2, 2, 0]

#: 2.2.8 Direction: 0 east, 1 south, 2 west, 3 north.
#: Follows the element grouping exactly — fiery east, earthy south, airy west,
#: watery north.
DIRECTION_NAMES = ["east", "south", "west", "north"]
RASI_DIRECTION = [RASI_ELEMENT[i] for i in range(12)]

#: 2.2.9 Colours, in the book's own wording and spelling ("color", not
#: "colour"). The book's Pisces sentence reads "cream color or the the color of
#: fish" — the doubled article is a typo in the source and is dropped here.
RASI_COLOR = [
    "blood-red color", "white", "grass green", "pale red", "white", "variegated",
    "black", "reddish brown", "the color of the husk of grass", "variegated",
    "brown color (that of a mongoose)", "cream color or the color of fish",
]

#: 2.2.10 Strong by day (divaa) or by night (nishaa).
#: True means a night rasi. Ar, Ta, Ge, Cn, Sg, Cp are night rasis.
RASI_IS_NIGHT = [i in (0, 1, 2, 3, 8, 9) for i in range(12)]

#: 2.2.10's Sanskrit names. Index 0 is the night half, index 1 the day half,
#: matching RASI_IS_NIGHT being True first.
DAY_NIGHT_NAMES = [
    ["night time", "nishaa"],
    ["daytime", "divaa"],
]

#: 2.2.10: "Out of the two rasis owned by a planet, one is a day sign and one
#: is a night sign." True of all five two-sign lords; Sun and Moon own one
#: each and are the governors below rather than exceptions to the rule.
DAY_NIGHT_PAIR_RULE = (
    "Out of the two rasis owned by a planet, one is a day sign and one is a "
    "night sign."
)

#: 2.2.10: "Moon governs all the nishaa rasis and Sun governs all the divaa
#: rasis." Index 0 is the night half, matching DAY_NIGHT_NAMES.
#:
#: Written as plain ints, not Graha members: constants/graha.py imports Rasi
#: from this module, so importing Graha here would be circular.
#: test_2_2_10_the_governors_are_moon_and_sun pins the two values.
DAY_NIGHT_GOVERNOR = [1, 0]  # Graha.MOON, Graha.SUN

#: 2.2.11 Rising: 0 seershodaya (head first), 1 prishthodaya (feet first),
#: 2 ubhayodaya (both) — Pisces alone.
RISING_NAMES = ["seershodaya", "prishthodaya", "ubhayodaya"]
RASI_RISING = [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 2]

#: 2.2.11's description of each. Pisces "rises with both its head and feet",
#: which is why ubhayodaya has a row of its own.
RISING_DESCRIPTIONS = [
    "Some rasis rise with their head.",
    "Some rasis rise with their feet.",
    "Pi rises with both its head and feet.",
]

#: Footnote 4 to 2.2.11. See D-2 in docs/book-deviations.md.
PRISHTHODAYA_NOTE = (
    "Many scholars have interpreted \u201cprishthodaya\u201d as \u201crising with the "
    "feet\u201d. So we will use the same interpretation. However, strictly "
    "speaking, one should note that \u201cprishtha\u201d means \u201cback\u201d."
)

#: 2.2.11: "It is said that planets in Seershodaya rasi give their results in
#: the first half of their dasas and planets in Prishthodaya rasi give their
#: results in the second half of their dasas." Indexed as RISING_NAMES;
#: ubhayodaya is not given a half, so its entry is None.
RISING_DASA_HALF: list[str | None] = ["first", "second", None]
RISING_DASA_RULE = (
    "It is said that planets in Seershodaya rasi give their results in the "
    "first half of their dasas and planets in Prishthodaya rasi give their "
    "results in the second half of their dasas."
)

#: 2.2.12 Varna: 0 brahmana, 1 kshatriya, 2 vaisya, 3 sudra.
#: Watery brahmana, fiery kshatriya, earthy vaisya, airy sudra.
VARNA_NAMES = ["brahmana", "kshatriya", "vaisya", "sudra"]

#: 2.2.12's own one-word gloss in the numbered list: "Brahmanas (scholars)",
#: "Kshatriyas (warriors)", "Vaisyas (traders)", "Sudras (workers)".
VARNA_NAMES_EN = ["scholars", "warriors", "traders", "workers"]

#: 2.2.12's prose description of each class.
VARNA_DESCRIPTIONS = [
    "Brahmanas pursue knowledge and work as priests or ministers.",
    "Kshatriyas are valiant and they become kings, army chiefs and soldiers.",
    "Vaisyas are the traders and suppliers of various services.",
    "Sudras execute various menial tasks.",
]

#: 2.2.12 states the mapping by element, not by sign: watery brahmana, fiery
#: kshatriya, earthy vaisya, airy sudra.
VARNA_ELEMENT = ["water", "fire", "earth", "air"]

_ELEMENT_TO_VARNA = {0: 1, 1: 2, 2: 3, 3: 0}
RASI_VARNA = [_ELEMENT_TO_VARNA[RASI_ELEMENT[i]] for i in range(12)]


class Rasi(IntEnum):
    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICORN = 9
    AQUARIUS = 10
    PISCES = 11
