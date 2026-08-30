"""Avasthas (states of a planet) — book §15.4.

"Avastha literally means 'state'." A planet gives results according to the
state it is in, so these feed anything that needs to know how effective a
planet is — including §9.2's "take the stronger lord".

Four families, of which three are defined well enough to compute:

* §15.4.1 age (Table 35) — from the longitude alone
* §15.4.2 alertness — from the dignity of the occupied rasi
* §15.4.3 attitude and mood — 9 states, plus 6 more

The chapter's own caution belongs with the data:

    "One should not be carried away with these avasthas. Just as there are some
    child prodigies and wizards with wrinkles, a planet can give good results
    irrespective of its age-related state."

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# §15.4.1 — Table 35, avasthas related to age
# --------------------------------------------------------------------------

#: Table 35, in the printed order. ``odd`` and ``even`` are the degree ranges
#: within the rasi, as ``(start, end)`` with end exclusive.
#:
#: ``fraction`` quantifies ``results`` **only where the book does**. Vriddha's
#: result is given as "Some", which is not a number, so its fraction is None
#: rather than an invented 0.75.
AGE_AVASTHAS: tuple[dict, ...] = (
    {"name": "Saisava", "meaning": "Child", "results": "Quarter",
     "fraction": 0.25, "odd": (0.0, 6.0), "even": (24.0, 30.0)},
    {"name": "Kumaara", "meaning": "Adolescent", "results": "Half",
     "fraction": 0.5, "odd": (6.0, 12.0), "even": (18.0, 24.0)},
    {"name": "Yuva", "meaning": "Youth", "results": "Full",
     "fraction": 1.0, "odd": (12.0, 18.0), "even": (12.0, 18.0)},
    {"name": "Vriddha", "meaning": "Old", "results": "Some",
     "fraction": None, "odd": (18.0, 24.0), "even": (6.0, 12.0)},
    {"name": "Mrita", "meaning": "Dead", "results": "None",
     "fraction": 0.0, "odd": (24.0, 30.0), "even": (0.0, 6.0)},
)

#: §15.4.1's closing caution, which the table on its own does not carry.
AGE_AVASTHA_CAUTION = (
    "One should not be carried away with these avasthas. Just as there are "
    "some child prodigies and wizards with wrinkles, a planet can give good "
    "results irrespective of its age-related state. Age is just one of the "
    "factors deciding a person's productivity. Similarly, age-related state is "
    "just one of the factors deciding a planet's effectiveness."
)

# --------------------------------------------------------------------------
# §15.4.2 — the three alertness states
# --------------------------------------------------------------------------

#: Keyed by the dignity of the rasi the planet occupies.
ALERTNESS_AVASTHAS: tuple[dict, ...] = (
    {"name": "Jaagrita", "meaning": "awake", "results": "full",
     "when": "in its exaltation rasi or an own rasi"},
    {"name": "Swapna", "meaning": "dreaming", "results": "medium",
     "when": "in a rasi owned by a neutral or friendly planet"},
    {"name": "Sushupta", "meaning": "asleep", "results": "negligible",
     "when": "in its debilitation rasi or a rasi owned by an enemy"},
)

# --------------------------------------------------------------------------
# §15.4.3 — nine states of attitude and mood
#
# These are NOT mutually exclusive. A planet can be exalted (Deepta) and also
# joined by malefics (Vikala) at the same time, so they are evaluated as a set
# rather than resolved to one.
# --------------------------------------------------------------------------

MOOD_AVASTHAS: tuple[dict, ...] = (
    {"name": "Deepta", "meaning": "bright",
     "when": "in its exaltation rasi", "needs": ()},
    {"name": "Swastha", "meaning": "doing well, contented, comfortable, natural",
     "when": "in its own rasi", "needs": ()},
    {"name": "Mudita", "meaning": "delighted",
     "when": "in a good friend's rasi", "needs": ()},
    {"name": "Saanta", "meaning": "peaceful",
     "when": "in a friend's rasi", "needs": ()},
    {"name": "Deena", "meaning": "sad, depressed",
     "when": "in a neutral planet's rasi", "needs": ()},
    {"name": "Duhkhita", "meaning": "distressed, miserable",
     "when": "in an enemy's rasi", "needs": ()},
    {"name": "Vikala", "meaning": "crippled, confused",
     "when": "joined by malefic planets", "needs": ()},
    {"name": "Khala", "meaning": "mischievous, scheming",
     "when": "in a malefic planet's rasi", "needs": ()},
    {"name": "Kopita", "meaning": "angry",
     "when": "joined closely by Sun", "needs": ()},
)

# --------------------------------------------------------------------------
# §15.4.3 — six additional states of attitude and mood
#
# ``needs`` names inputs beyond the planets' longitudes. "aspects" means the
# state cannot be decided without knowing what aspects the planet, which this
# engine does not compute (see docs/open-items.md OI-18).
# --------------------------------------------------------------------------

ADDITIONAL_MOOD_AVASTHAS: tuple[dict, ...] = (
    {"name": "Lajjita", "meaning": "ashamed",
     "when": "in the 5th house joined by Sun, Mars, Saturn, Rahu and Ketu",
     "needs": ("house",)},
    {"name": "Garvita", "meaning": "proud",
     "when": "in its exaltation rasi or moolatrikona rasi", "needs": ()},
    {"name": "Kshudhita", "meaning": "hungry",
     "when": "in an enemy's rasi or conjoined by enemies or aspected by "
             "enemies or conjoined by Saturn",
     "needs": ("aspects",)},
    {"name": "Trishita", "meaning": "thirsty",
     "when": "stationed in a watery rasi and aspected by enemies without the "
             "aspect of benefics",
     "needs": ("aspects",)},
    {"name": "Mudita", "meaning": "delighted",
     "when": "in a friend's sign, conjoined or aspected by friends and "
             "conjoined by Jupiter",
     "needs": ("aspects",)},
    {"name": "Kshobhita", "meaning": "shaken, agitated",
     "when": "conjoined by Sun and aspected by malefics or enemies",
     "needs": ("aspects",)},
)

#: What the chapter says these states do to a house's significations.
AVASTHA_EFFECTS: tuple[dict, ...] = (
    {"avastha": "Kshudhita",
     "effect": "the significations of the house containing the planet are affected"},
    {"avastha": "Kshobhita",
     "effect": "the significations of the house containing the planet are affected"},
    {"avastha": "Lajjita", "house": 5,
     "effect": "there may be losses related to progeny"},
    {"avastha": "Kshobhita", "house": 7,
     "effect": "there may be loss of spouse"},
)

# --------------------------------------------------------------------------
# The other measures of strength the chapter names
#
# None of these is computed here. They are recorded so that an API can say
# what exists and why it is absent, rather than leaving a caller to guess that
# "strength" means the one measure that happens to be implemented.
# --------------------------------------------------------------------------

STRENGTH_MEASURES: tuple[dict, ...] = (
    {
        "key": "shadbala",
        "name": "Shadbala",
        "shows": (
            "the strength of a planet from six sources — placement, time, "
            "directions, aspects, motion and inherent nature"
        ),
        "used_for": (
            "deciding which planet gives the results when two or more "
            "influence the same house or take part in a yoga; the strongest "
            "acts like a group leader on the group's behalf"
        ),
        "available": False,
        "why_not": (
            "the book states that explaining the computation of shadbalas is "
            "beyond its scope, and refers the reader to Brihat Parasara Hora "
            "Sastram or 'Graha and Bhava Balas' by Dr. B.V. Raman"
        ),
        "note": (
            "Most computer software programs give shadbala, though there are "
            "minor differences between the definitions used by them"
        ),
    },
    {
        "key": "ashtakavarga",
        "name": "Ashtakavarga bala",
        "shows": (
            "how other planets support or oppose a planet — its ability to "
            "give its own results in harmony with other planetary forces, not "
            "its ability to lead a group"
        ),
        "used_for": (
            "judging whether a planet can deliver in a given area of life; a "
            "planet may be strong in one divisional chart and weak in another, "
            "and gives its results more effectively in the area of the first"
        ),
        "available": True,
        "why_not": None,
        "note": (
            "Chapter 12 supplies the measure: a planet's rekhas in its own "
            "BAV, in whichever divisional chart is being read, and section "
            "12.4's bands for a rasi's SAV. Example 44 already reads it that "
            "way — 'Mercury ... has 6 rekhas in his D-20 BAV'. What chapter "
            "15 has not given us is a scored bala derived from those counts"
        ),
    },
    {
        "key": "avastha",
        "name": "Avastha bala",
        "shows": "the state a planet is in — its age, alertness, mood and activity",
        "used_for": "judging whether a planet is in a fit state to give good results",
        "available": True,
        "why_not": None,
        "note": (
            "All four families the chapter names are implemented: age "
            "(baaladi), alertness (jagradadi), mood (deeptadi) and activity "
            "(sayanadi)"
        ),
    },
    {
        "key": "vimsopaka",
        "name": "Vimsopaka bala",
        "shows": (
            "the overall strength of a planet and its ability to play an "
            "important role in one's life, rather than in a specific area"
        ),
        "used_for": "judging a planet's overall effectiveness in a life",
        "available": False,
        "why_not": "not yet implemented",
        "note": (
            "The varga groupings it is computed over — shadvarga, "
            "sapthavarga, dasavarga, shodasavarga — already exist in "
            "charts/vargas.py, so what is missing is the weighting, not the "
            "charts"
        ),
    },
    {
        "key": "simple_rules",
        "name": "Simple comparison rules",
        "shows": "which of two planets or rasis is stronger, by short rules",
        "used_for": (
            "trivial determinations such as which planet initiates dasas and "
            "antardasas"
        ),
        "available": True,
        "why_not": None,
        "note": (
            "Section 15.5.1's cascade for the stronger co-lord and section "
            "15.5.2's for the stronger rasi are both implemented, in "
            "charts/colord.py and charts/rasi_strength.py. These, not "
            "shadbala, are the rules section 9.2 needs for choosing the "
            "stronger of Mars and Ketu as lord of Scorpio, and the rules a "
            "rasi dasa needs to pick between lagna and the 7th"
        ),
    },
)

#: Fields transcribed from the book, which must match it character for
#: character. Everything else in this module is our own summary. The same
#: discipline as chapter 8's VERBATIM_FIELDS; see docs/verification-standard.md.
AVASTHA_VERBATIM_FIELDS: tuple[tuple[str, str], ...] = (
    ("SAYANAADI_AVASTHAS", "name"),
    ("SAYANAADI_AVASTHAS", "meaning"),
    ("SAYANAADI_TERMS", "text"),
    ("SOUND_NUMBERS", "roman"),
    ("AGE_AVASTHAS", "name"),
    ("AGE_AVASTHAS", "meaning"),
    ("AGE_AVASTHAS", "results"),
    ("SAYANAADI_SPECIAL_RESULTS", "verbatim"),
)

#: Whole constants that are a transcribed sentence or passage.
AVASTHA_VERBATIM_CONSTANTS: tuple[str, ...] = (
    "ACTIVITY_IS_MOST_IMPORTANT",
    "AGE_AVASTHA_CAUTION",
    "SAYANAADI_ARE_MOST_IMPORTANT",
    "SAYANAADI_CAUTION",
    "GHATI_NOTE",
    "NAVAMSA_INDEX_NOTE",
    "SAYANAADI_FORMULA",
)

# --------------------------------------------------------------------------
# §15.4.4 — states related to activity (sayanaadi avasthas)
#
# "There are 12 possible states of a planet related to its activity. This
# state is the most important of all states."
# --------------------------------------------------------------------------

#: §15.4.4's own ranking of this family against the other three.
ACTIVITY_IS_MOST_IMPORTANT = (
    "There are 12 possible states of a planet related to its activity. This "
    "state is the most important of all states."
)

#: §15.4.4 writes the vicheshta case as "A value of 3 (or 0)". A remainder on
#: division by 3 is never 3, so only 0 can occur; the table is keyed on 0.
VICHESHTA_REMAINDER_NOTE = (
    "The book writes this case as \"A value of 3 (or 0)\". A remainder on "
    "division by 3 cannot be 3, so in practice only 0 arises."
)

#: Table 36, indexed 1 to 12 as the book indexes it.
SAYANAADI_AVASTHAS: dict[int, dict] = {
    1: {"name": "Sayana", "meaning": "Lying down, resting"},
    2: {"name": "Upavesana", "meaning": "Sitting down"},
    3: {"name": "Netrapaani", "meaning": "Eyes and hands"},
    4: {"name": "Prakaasana", "meaning": "Shining"},
    5: {"name": "Gamana", "meaning": "Going (on the move)"},
    6: {"name": "Aagamana", "meaning": "Coming, returning"},
    7: {"name": "Sabhaa", "meaning": "Being at an assembly",
        "aliases": ["Sabhaa vasati"]},
    8: {"name": "Aagama", "meaning": "Coming/Acquiring"},
    9: {"name": "Bhojana", "meaning": "Eating"},
    # The book spells this one BOTH ways: Table 36 prints "Nriyalipsaa", and
    # the results heading later in 15.4.4 prints "Nrityalipsaa". Both are the
    # author's, so both are stored. Recorded as D-20.
    10: {"name": "Nriyalipsaa", "meaning": "Longing to dance",
         "aliases": ["Nrityalipsaa"]},
    11: {"name": "Kautuka", "meaning": "Being eager"},
    12: {"name": "Nidraa", "meaning": "Sleeping"},
}

#: The formula's terms, named as §15.4.4 names them. Kept as data so the API
#: can show its working rather than presenting a bare number.
SAYANAADI_TERMS: tuple[dict, ...] = (
    {"symbol": "C", "name": "constellation",
     "text": "the number of the constellation occupied by the planet "
             "(1 for Aswini, 2 for Bharani and so on)", "range": (1, 27)},
    {"symbol": "P", "name": "planet_index",
     "text": "the index of the planet whose avastha we are finding "
             "(1 for Sun, 2 for Moon)", "range": (1, 9)},
    {"symbol": "A", "name": "navamsa_index",
     "text": "the index of the amsa (navamsa) occupied by the planet in its "
             "rasi", "range": (1, 9)},
    {"symbol": "M", "name": "moon_constellation",
     "text": "the constellation occupied by Moon", "range": (1, 27)},
    {"symbol": "G", "name": "ghati",
     "text": "the ghati running at birth", "range": (1, 60)},
    {"symbol": "L", "name": "lagna_rasi",
     "text": "the rasi occupied by lagna (1 for Ar, 2 for Ta and so on)",
     "range": (1, 12)},
)

SAYANAADI_FORMULA = "((C x P x A) + M + G + L) mod 12"

#: §15.4.4's footnote 51, which pins what A is *not*.
NAVAMSA_INDEX_NOTE = (
    "For example, let us say Mercury is in 22Ge14. Each navamsa has a length "
    "of 3°20' (1/9th of 30°) and 22°14' in Ge is in the 7th navamsa of Ge "
    "(please note that we are not talking about the rasi occupied by the "
    "planet in navamsa). Then we use A = 7 for Mercury."
)

#: §15.4.4's footnote 52 — how the ghati at birth is counted.
GHATI_NOTE = (
    "Suppose sunrise was at 6 am and someone was born at 11 pm. So 17 hours "
    "were over. Each hour has 2.5 ghatis and 17 hours = 17 x 2.5 = 42.5. So "
    "the 43rd ghati was running at birth."
)
GHATIS_PER_HOUR = 2.5

# --------------------------------------------------------------------------
# §15.4.4 — the strength of the activity
# --------------------------------------------------------------------------

#: Table 37. The Devanagari is the source of truth; the Roman transliteration
#: is the book's own and is **ambiguous** — "d" appears as alveolar in group 1
#: and dental in group 5, "dh" as dental in 1 and alveolar in 2, and so on. A
#: caller giving a Roman syllable may therefore be asking an unanswerable
#: question; see :func:`hora.charts.avastha.sound_number`.
SOUND_NUMBERS: dict[int, dict] = {
    1: {"devanagari": ["अ", "क", "छ", "ड", "ध", "भ", "व"],
        "roman": "a, ka, chh, d (alveolar), dh (dental), bh, v"},
    2: {"devanagari": ["इ", "ख", "ज", "ढ", "न", "म", "श"],
        "roman": "i, kh, j, dh (alveolar), n (dental), m, s/sh (palatal)"},
    3: {"devanagari": ["उ", "ग", "झ", "त", "प", "य", "ष"],
        "roman": "u, g, jh, t, p, y, sh (alveolar)"},
    4: {"devanagari": ["ए", "घ", "ट", "थ", "फ", "र", "स"],
        "roman": "e, gh, t (alveolar), th (dental), ph, r, s (dental)"},
    5: {"devanagari": ["ओ", "च", "ठ", "द", "ब", "ल", "ह"],
        "roman": "o, ch, th (alveolar), d (dental), b, l, h"},
}

#: "We use 5 for Sun and Jupiter, 2 Moon and Mars, 3 for Mercury, Venus and
#: Saturn and 4 for Rahu and Ketu."
PLANETARY_ADJUSTMENT: dict[int, int] = {
    0: 5, 4: 5,        # Sun, Jupiter
    1: 2, 2: 2,        # Moon, Mars
    3: 3, 5: 3, 6: 3,  # Mercury, Venus, Saturn
    7: 4, 8: 4,        # Rahu, Ketu
}

#: The remainder mod 3, and what it means. Note 3 and 0 are the same case:
#: "A value of 3 (or 0) means 'vicheshta'".
ACTIVITY_STRENGTH: dict[int, dict] = {
    1: {"name": "drishti", "results": "medium"},
    2: {"name": "cheshta", "results": "full"},
    0: {"name": "vicheshta", "results": "very little"},
}

# --------------------------------------------------------------------------
# §15.4.4 — "Importance of Sayanaadi Avasthas"
#
# Eight special results the section attributes to Parasara, on top of the
# per-graha results. Each turns on the graha's nature, its sayanaadi avastha
# and often the house it occupies. `verbatim` is the sentence as printed;
# everything beside it is our reading of it.
# --------------------------------------------------------------------------

#: §15.4.4's ranking of this family against the other three avastha families.
SAYANAADI_ARE_MOST_IMPORTANT = (
    "Sayanaadi (Sayana etc) avasthas are the most important of all avasthas."
)

#: Parasara's special results. `actor` is who the rule is about, `avasthas`
#: the Table 36 indices it fires in, `houses` the houses it is confined to
#: (empty means any house), and `needs` the inputs without which it cannot be
#: decided. Numbered in the order the section states them.
SAYANAADI_SPECIAL_RESULTS: tuple[dict, ...] = (
    {
        "rule": 1,
        "verbatim": (
            "If a benefic is in Sayana avastha, the house benefits from his "
            "presence."
        ),
        "actor": "benefic",
        "avasthas": (1,),
        "houses": (),
        "effect": "the house benefits from his presence",
        "auspicious": True,
        "needs": ("nature",),
    },
    {
        "rule": 2,
        "verbatim": (
            "If a malefic is in Nidraa avastha in the 7th house without the "
            "conjunction or aspect of another malefic, it is auspicious."
        ),
        "actor": "malefic",
        "avasthas": (12,),
        "houses": (7,),
        "unless_associated_with": "malefics",
        "effect": "auspicious",
        "auspicious": True,
        "needs": ("nature", "house", "association with malefics"),
    },
    {
        "rule": 3,
        "verbatim": (
            "If a malefic is in Bhojana avastha, the house containing it is "
            "destroyed."
        ),
        "actor": "malefic",
        "avasthas": (9,),
        "houses": (),
        "effect": "the house containing it is destroyed",
        "auspicious": False,
        "needs": ("nature",),
    },
    {
        "rule": 4,
        "verbatim": (
            "If a malefic is in the 5th house in Sayana or Nidraa avastha, it "
            "is auspicious."
        ),
        "actor": "malefic",
        "avasthas": (1, 12),
        "houses": (5,),
        "effect": "auspicious",
        "auspicious": True,
        "needs": ("nature", "house"),
    },
    {
        "rule": 5,
        "verbatim": (
            "If a malefic is in the 8th house in Sayana or Nidraa avastha, it "
            "brings death by royal wrath."
        ),
        "actor": "malefic",
        "avasthas": (1, 12),
        "houses": (8,),
        "effect": "death by royal wrath",
        "auspicious": False,
        "needs": ("nature", "house"),
    },
    {
        "rule": 6,
        "verbatim": (
            "If a malefic occupies the 10th house in Bhojana or Sayana "
            "avastha, all kinds of miseries may be expected."
        ),
        "actor": "malefic",
        "avasthas": (1, 9),
        "houses": (10,),
        "effect": "all kinds of miseries may be expected",
        "auspicious": False,
        "needs": ("nature", "house"),
    },
    {
        "rule": 7,
        "verbatim": (
            "If a benefic or a planet in own or exaltation rasi occupies in "
            "the 1st, 5th, 7th or 10th house in Prakasana, Nrityalipsaa or "
            "Kautuka avasthas, it brings Raja Yoga."
        ),
        "actor": "benefic or a planet in own or exaltation rasi",
        "avasthas": (4, 10, 11),
        "houses": (1, 5, 7, 10),
        "effect": "Raja Yoga",
        "auspicious": True,
        "needs": ("nature or dignity", "house"),
    },
    {
        "rule": 8,
        "verbatim": (
            "Parasara specifically mentioned Moon in the 10th house in "
            "Kautuka or Prakaasana avasthas."
        ),
        "actor": "Moon",
        "avasthas": (4, 11),
        "houses": (10,),
        "effect": "Raja Yoga",
        "auspicious": True,
        "needs": ("house",),
        "note": (
            "An emphasis of rule 7, not a rule beside it — but rule 7 wants a "
            "benefic or a graha in its own or exaltation rasi, and by section "
            "3.2.2 the Moon has no nature apart from its phase. A waning Moon "
            "is a malefic and fails rule 7's own precondition, yet this "
            "sentence names the Moon without qualifying the phase. The book "
            "does not resolve it; see docs/open-items.md."
        ),
    },
)

#: The section's closing warning, which qualifies everything above it.
SAYANAADI_CAUTION = (
    "However, one should not be carried away with avasthas and one should "
    "remember that they are only the \"states\" of the planet. The state of a "
    "planet related to age, alertness, mood and activity will have a role in "
    "the results given by it, but the houses influenced by it in various "
    "divisional charts are more important in deciding the results. We should "
    "avoid the temptation to make predictions based on thumbrules and "
    "look-up tables."
)
