"""Karakas (significators) — book chapter 8.

§8.1: "The word karaka means 'one who causes'. Karaka of a matter is the
significator of the matter."

Three kinds, and the chapter is emphatic that they are not interchangeable:

    "One should not use the three types of karakas in a mixed-up way. Karakas
    of each type have a specific purpose."

===================  =====  ========  ==================================
Kind                 Count  Presides  Used for
===================  =====  ========  ==================================
naisargika (natural)     9  Brahma    general results (phalita jyotish)
chara (variable)         8  Vishnu    raja yogas, sustenance, spiritual
sthira (fixed)           7  Shiva     timing the death of relatives
===================  =====  ========  ==================================

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

#: §8.1 and its footnote 20. The word is spelled "karaka" throughout the book
#: but the footnote is explicit about how it sounds.
KARAKA_MEANING = "one who causes"
KARAKA_PRONUNCIATION = "kaaraka"
#: §8.1's definition, in full. The literal meaning above is only half of it.
KARAKA_DEFINITION = (
    "Karaka of a matter is the significator of the matter. He is the one who "
    "causes events related to that matter."
)

#: §8.1's warning in full. Its third sentence is the one that says what to do,
#: not merely what to avoid.
KARAKA_WARNING = (
    "One should not use the three types of karakas in a mixed-up way. Karakas "
    "of each type have a specific purpose. One should understand the "
    "distinction between chara, sthira and naisargika karakas clearly and use "
    "them accordingly."
)

#: Which fields in this module are **transcribed from the book** and must match
#: it character for character, as ``(constant, field)`` pairs.
#:
#: Everything else here — glosses, ``used_for``, ``read_as_note``, the usage
#: rules, the choosing guide — is *our* summary of the chapter, not the
#: author's wording. Mixing the two without saying which is which is how a
#: "verbatim" field quietly stops being verbatim; chapter 2 lost three of the
#: author's typos that way before anyone noticed.
#:
#: ``test_declared_verbatim_fields_are_verbatim`` enforces this against the PDF.
VERBATIM_FIELDS: tuple[tuple[str, str], ...] = (
    ("CHARA_KARAKAS", "name"),
    ("CHARA_KARAKAS", "shows"),
    ("STHIRA_KARAKAS", "relative"),
    ("NAISARGIKA_KARAKA", "signifies"),
    ("NAISARGIKA_KARAKATWAS", "matters"),
)

#: Whole constants that are a single transcribed sentence or passage.
VERBATIM_CONSTANTS: tuple[str, ...] = (
    "KARAKA_DEFINITION",
    "KARAKA_WARNING",
)

# --------------------------------------------------------------------------
# §8.1 The three kinds
# --------------------------------------------------------------------------

#: Which grahas each kind ranges over, and why the others are left out.
KARAKA_KINDS: dict[str, dict] = {
    "naisargika": {
        "name": "Naisargika karaka",
        "gloss": "natural significator",
        "count": 9,
        "presiding": "Brahma",
        "grahas": (
            Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
            Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU,
        ),
        "shows": (
            "everything that exists in Brahma's creation and affects a person, "
            "impersonal things and matters included"
        ),
        # 8.1: "Naisargika karakas show **not only human beings**, but they
        # show various impersonal things and matters." The contrast is the
        # point — it is what separates naisargika from chara, which shows
        # people. Dropping it leaves the warning against mixing the kinds
        # without its clearest illustration.
        "not_limited_to": "human beings",
        "shows_contrast": (
            "Naisargika karakas show not only human beings, but they show "
            "various impersonal things and matters."
        ),
        "presiding_because": "Brahma is the creator of everything that exists",
        "used_for": "phalita jyotish — analysis of general results",
        # 8.3: "we must take the relevant house from the karaka."
        "read_as": "house_from_karaka",
        "read_as_note": (
            "Take the relevant house counted from the karaka, not the karaka "
            "himself: the 7th from Venus shows husband, not Venus"
        ),
    },
    "chara": {
        "name": "Chara karaka",
        "gloss": "variable significator",
        "count": 8,
        "presiding": "Vishnu",
        "grahas": (
            Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
            Graha.VENUS, Graha.SATURN, Graha.RAHU,
        ),
        "shows": "people who play an important role in one's sustenance and achievements",
        # 8.1 makes the broader claim first — "they show people who play a
        # role in one's life" — and narrows it afterwards. Both are kept: the
        # broad one is what contrasts with naisargika.
        "shows_broadly": "people who play a role in one's life",
        # 8.1 gives the reason, not just the fact: "As Vishnu presides over
        # activities related to sustenance, achievements and spiritual
        # progress, chara karakas show these aspects of one's life."
        "presiding_because": (
            "Vishnu presides over activities related to sustenance, "
            "achievements and spiritual progress"
        ),
        "used_for": "raja yogas and spiritual progress",
        # 8.3: "We do not take the 7th from DK for spouse, but DK himself
        # shows spouse."
        "read_as": "karaka_himself",
        "read_as_note": (
            "The karaka himself shows the matter: DK himself shows spouse, "
            "not the 7th from DK"
        ),
        # 8.1: "Examples are - mother, father, wife, advisors etc."
        "examples": ("mother", "father", "wife", "advisors"),
        "also_shows": (
            "how our karma (cumulative sum of actions) is carried from one "
            "life to another"
        ),
        # 8.1: "They do not include Ketu, as Ketu stands for moksha
        # (emancipation) and does not stand for any person who affects one's
        # sustenance."
        # The qualifier is load-bearing: Ketu is not excluded for failing to
        # be a person, but for failing to be a person **who affects one's
        # sustenance** — which is Vishnu's domain, and so the reason follows
        # from who presides. The gloss "(emancipation)" is the book's own.
        "excludes": {
            int(Graha.KETU): (
                "Ketu stands for moksha (emancipation) and does not stand for "
                "any person who affects one's sustenance"
            )
        },
    },
    "sthira": {
        "name": "Sthira karaka",
        "gloss": "fixed significator",
        "count": 7,
        "presiding": "Shiva",
        "grahas": (
            Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
            Graha.VENUS, Graha.SATURN,
        ),
        "shows": "the physical bodies of relatives",
        "presiding_because": "Shiva presides over death",
        # Footnote 21 links the name to the function: sthira means "fixed",
        # and death is life becoming fixed. Without it, "sthira karakas time
        # death" looks arbitrary.
        "name_explained": (
            "In Indian philosophy, death is nothing but praana (life) becoming "
            "sthira (fixed)."
        ),
        "used_for": "timing the death of various near relatives",
        # 8.3: "sthira karakas themselves represent the physical bodies."
        "read_as": "karaka_himself",
        "read_as_note": (
            "The karaka himself represents the relative's physical body: "
            "Jupiter is the husband's body in a female chart"
        ),
        # 8.1: "As Shiva presides over death, they show the destruction of body."
        "also_shows": "the destruction of the body, as Shiva presides over death",
        # 8.1: "include only 7 planets because only they have physical bodies."
        "excludes": {
            int(Graha.RAHU): "only the seven have physical bodies",
            int(Graha.KETU): "only the seven have physical bodies",
        },
    },
}

# --------------------------------------------------------------------------
# §8.2 Chara karakas — Table 13
# --------------------------------------------------------------------------

#: Table 13, in order of decreasing advancement. Index 0 is the highest
#: advancement (Atma Karaka) and index 7 the lowest (Dara Karaka).
CHARA_KARAKAS: tuple[dict, ...] = (
    {"symbol": "AK", "name": "Atma Karaka", "shows": "Self"},
    {"symbol": "AmK", "name": "Amatya Karaka", "shows": "Ministers"},
    {"symbol": "BK", "name": "Bhratri Karaka", "shows": "Siblings"},
    {"symbol": "MK", "name": "Matri Karaka", "shows": "Mother"},
    {"symbol": "PiK", "name": "Pitri Karaka", "shows": "Father"},
    {"symbol": "PK", "name": "Putra Karaka", "shows": "Children"},
    {"symbol": "GK", "name": "Jnaati Karaka", "shows": "Rivals"},
    {"symbol": "DK", "name": "Dara Karaka", "shows": "Spouse"},
)

#: §8.2's procedure, verbatim. It lived only in a docstring until now, so no
#: caller could read the rule the engine applies. Step 1's last sentence is the
#: whole of Rahu's special case.
CHARA_KARAKA_PROCEDURE: tuple[str, ...] = (
    "Take the eight planets \u2013 Sun, Moon, Mars, Mercury, Jupiter, Venus, "
    "Saturn and Rahu. For each planet, find its advancement from the beginning "
    "of the rasi occupied by it. For Rahu, measure the advancement from the "
    "end of his rasi.",
    "Arrange them in the decreasing order of advancement.",
    "The planet with the highest advancement is Atma Karaka (significator of "
    "self). We will denote him by AK. Find other chara karakas using Table 13.",
)

#: §8.2's tie-break, distinct from the exact-tie case below: it says the
#: comparison runs to arcseconds before two grahas count as equal.
CHARA_KARAKA_TIE_BREAK = (
    "If two planets have the same degrees, we should compare minutes. If "
    "minutes are same, we should compare the seconds."
)

#: Table 13's first column. Only the two extreme rows are labelled; the label
#: is on the advancement, not on the karaka, which is why AK is "highest"
#: rather than "first".
CHARA_KARAKA_ADVANCEMENT_LABELS: dict[str, str] = {"AK": "Highest", "DK": "Lowest"}

#: Table 13's footnote 24: "Some people approximate it as 'gnaati' or
#: 'gyaati'", and the symbol is written both ways.
CHARA_KARAKA_ALIASES: dict[str, list[str]] = {
    "GK": ["JK"],
}
CHARA_KARAKA_NAME_ALIASES: dict[str, list[str]] = {
    "Jnaati Karaka": ["Gnaati Karaka", "Gyaati Karaka"],
}

#: Footnote 24 in full: "In the symbol 'jn' here, 'j' is the voiced palatal
#: consonant and 'n' is the palatal nasal. This is a tough sound to pronounce
#: correctly."
JNAATI_PRONUNCIATION_NOTE = (
    "In 'jn', 'j' is the voiced palatal consonant and 'n' is the palatal "
    "nasal. A tough sound to pronounce correctly; some approximate it as "
    "'gnaati' or 'gyaati'."
)

#: Footnotes 22 and 25 add meanings the "Persons shown" column does not carry.
CHARA_KARAKA_NOTES: dict[str, str] = {
    "AK": "throws light on the inner self of a native",
    "AmK": (
        "in practical terms, people who give advice — advisors and counsellors"
    ),
    "PK": "can also show subordinates and followers",
    "PiK": "can show a boss",
    "GK": (
        "commonly used for enemies or rivals; the literal meaning of "
        "'jnaati' is 'paternal cousin'"
    ),
}

#: §8.2 on the exact-tie case: "However, this rarely becomes necessary, as two
#: planets are rarely at exactly the same longitude."
SHARED_KARAKATWA_NOTE = (
    "Two grahas at exactly the same longitude hold a karakatwa together and "
    "the next karakatwa has no ruler; use the corresponding sthira karaka. "
    "This rarely becomes necessary, as two planets are rarely at exactly the "
    "same longitude."
)

#: §8.2 step 1: "For Rahu, measure the advancement from the end of his rasi."
#: Every other graha is measured from the beginning.
MEASURED_FROM_END_OF_RASI = frozenset({Graha.RAHU})

# --------------------------------------------------------------------------
# §8.3 Sthira karakas
# --------------------------------------------------------------------------

#: The fixed significators. Father and mother are each given as a *pair*, the
#: stronger of the two taking the role — not one fixed graha, so those two
#: entries carry two grahas and the caller must supply a strength comparison.
STHIRA_KARAKAS: tuple[dict, ...] = (
    {
        "relative": "father",
        "grahas": (Graha.SUN, Graha.VENUS),
        "rule": "stronger",
        "note": (
            "Footnote 26: some take Sun for daytime births and Venus for "
            "nighttime births"
        ),
    },
    {
        "relative": "mother",
        "grahas": (Graha.MOON, Graha.MARS),
        "rule": "stronger",
        "note": (
            "Footnote 26: some take Moon for nighttime births and Mars for "
            "daytime births"
        ),
    },
    {
        "relative": (
            "younger siblings, brother-in-law and sister-in-law "
            "(spouses of siblings)"
        ),
        "grahas": (Graha.MARS,), "rule": "fixed", "note": None,
    },
    {
        "relative": "maternal relatives (uncles and aunts)",
        "grahas": (Graha.MERCURY,), "rule": "fixed", "note": None,
    },
    {
        "relative": (
            "husband, sons, paternal grandparents and other paternal relatives "
            "(uncles and aunts)"
        ),
        "grahas": (Graha.JUPITER,), "rule": "fixed", "note": None,
    },
    {
        "relative": "wife, father-in-law, mother-in-law & maternal grandparents",
        "grahas": (Graha.VENUS,), "rule": "fixed", "note": None,
    },
    {
        "relative": "elder siblings",
        "grahas": (Graha.SATURN,), "rule": "fixed",
        "note": (
            "Footnote 27: some scholars give Saturn as the sthira karaka for "
            "children instead of elder siblings"
        ),
    },
)

#: §8.3: "When predicting the death of spouse, we use Jupiter in female charts
#: and Venus in male charts." Footnote 28 records the dissent.
STHIRA_KARAKA_OF_SPOUSE: dict[str, int] = {
    "female": Graha.JUPITER,
    "male": Graha.VENUS,
}
STHIRA_KARAKA_OF_SPOUSE_NOTE = (
    "Footnote 28: some scholars take Jupiter as the sthira karaka of spouse in "
    "male charts also"
)

# --------------------------------------------------------------------------
# §8.4 Naisargika karakas — Tables 15 and 16
# --------------------------------------------------------------------------

#: Table 15, the primary naisargika karakas. Keyed by house number 1..12.
#: §8.4 reads these as "the Nth house *from* the karaka": "the 4th house from
#: Moon shows mother", not the 4th house of the chart.
NAISARGIKA_KARAKA: dict[int, dict] = {
    1: {"graha": Graha.SUN, "signifies": "Self, physical constitution, soul, health"},
    2: {"graha": Graha.JUPITER, "signifies": "Family, wealth"},
    3: {"graha": Graha.MARS, "signifies": "Younger siblings, courage"},
    4: {"graha": Graha.MOON, "signifies": "Mother"},
    5: {"graha": Graha.JUPITER, "signifies": "Children"},
    6: {"graha": Graha.MARS, "signifies": "Enemies"},
    7: {"graha": Graha.VENUS, "signifies": "Wife, husband, marital bliss, relationships"},
    8: {"graha": Graha.SATURN, "signifies": "Longevity, troubles"},
    9: {"graha": Graha.JUPITER, "signifies": "Teacher, religion, fortune"},
    10: {"graha": Graha.MERCURY, "signifies": "Work, achievements, honors"},
    11: {"graha": Graha.JUPITER, "signifies": "Elder siblings"},
    12: {"graha": Graha.SATURN, "signifies": "Losses"},
}

#: Table 16, every natural signification with the house it pairs with.
#: "Mercury and 5th house show memory and so the 5th house from Mercury shows
#: memory." Each entry is (house, matters).
NAISARGIKA_KARAKATWAS: dict[int, tuple[tuple[int, str], ...]] = {
    Graha.SUN: (
        (1, "Self, soul, constitution, health"),
        (5, "fame, power"),
        (9, "father, boss"),
        (10, "career, achievements"),
    ),
    Graha.MOON: (
        (1, "Mind"),
        (4, "mother, peace of mind"),
        (11, "friends"),
    ),
    Graha.MARS: (
        (3, "Courage, younger siblings"),
        (4, "real estate"),
        (5, "scholarship in Nyaya sastra, speculation"),
        (6, "enemies, diseases, accidents, loans"),
    ),
    Graha.MERCURY: (
        (2, "Speech"),
        (4, "learning"),
        (5, "memory, scholarship, students"),
        (10, "work, achievements, honors"),
        (11, "credits"),
    ),
    Graha.JUPITER: (
        (2, "Family, wealth"),
        (4, "traditional learning"),
        (5, "children, intelligence"),
        (9, "teacher, religion, fortune"),
        (11, "elder brother, gains"),
    ),
    Graha.VENUS: (
        (4, "Vehicles"),
        (7, "wife, husband, marital bliss"),
        (12, "bed pleasures"),
    ),
    Graha.SATURN: (
        (5, "Following"),
        (6, "servants"),
        (8, "Longevity, troubles"),
        (12, "losses, hospitalization"),
    ),
    Graha.RAHU: (
        (6, "Accidents"),
        (8, "occult knowledge"),
        (9, "pilgrimages, going abroad"),
    ),
    Graha.KETU: (
        (8, "Occult knowledge"),
        (9, "pilgrimages, going abroad"),
        (12, "moksha"),
    ),
}

# --------------------------------------------------------------------------
#: §8.4's own definition, and where the significations are used.
NAISARGIKA_DEFINITION = (
    "Naisargika karakas are the natural significators of various matters."
)
NAISARGIKA_USED_IN = "These significations are used in general Phalita Jyotish."

#: §8.4 attributes Table 16 to the classics, not to itself: "we have various
#: other matters allotted to different planets in classics." Table 15 is the
#: chapter's own primary list; Table 16 is compiled. The distinction matters
#: for precedence, since a classical allotment and PVR's own statement are not
#: the same rank.
TABLE_16_SOURCE_NOTE = (
    "In addition, we have various other matters allotted to different planets "
    "in classics. The list of the natural significations of various planets is "
    "listed in Table 16."
)

#: §8.4's three worked readings, each "the Nth house from the graha". The last
#: is the one that states the rule: a matter shared by a graha and a house is
#: read at that house counted from that graha.
NAISARGIKA_WORKED_EXAMPLES: tuple[dict, ...] = (
    {"house": 4, "graha": Graha.MOON, "shows": "mother", "table": 15},
    {"house": 5, "graha": Graha.JUPITER, "shows": "sons", "table": 15},
    {"house": 5, "graha": Graha.MERCURY, "shows": "memory", "table": 16},
)

#: §8.4's statement of how Table 16 is used: "Mercury and 5th house show memory
#: and so the 5th house from Mercury shows memory."
NAISARGIKA_TABLE_16_RULE = (
    "Mercury and 5th house show memory and so the 5th house from Mercury "
    "shows memory."
)

# --------------------------------------------------------------------------
# §8.3 and §8.4 — choosing between the three kinds
#
# The tables above say what each karaka *is*. These say which kind to reach
# for, which is the part the chapter spends its prose on and the part that is
# easiest to leave out of an engine.
# --------------------------------------------------------------------------

#: §8.4's worked comparison, using children as the matter. The same subject
#: routes to a different kind depending on the question being asked.
CHOOSING_A_KARAKA: tuple[dict, ...] = (
    {
        "matter": "children",
        "question": "birth of children, or simple events from their lives",
        "kind": "naisargika",
        "use": "the 5th from Jupiter",
    },
    {
        "matter": "children",
        "question": (
            "children-related troubles that punish one's soul, or achievements "
            "and happiness related to children"
        ),
        "kind": "chara",
        "use": "PK (putra karaka)",
    },
    {
        "matter": "children",
        "question": "timing the death of a child",
        "kind": "sthira",
        "use": "the sthira karaka for children (Jupiter)",
    },
)

#: §8.3's explicit corrections. Each is a mistake the chapter names and the
#: reading it says to use instead.
KARAKA_USAGE_RULES: tuple[dict, ...] = (
    {
        "rule": (
            "Sthira karakas should not be used in general predictive astrology "
            "in the place of naisargika karakas"
        ),
        "wrong": "the 7th from Jupiter to predict marriage",
        "right": "the 7th from Venus to predict marriage",
        "because": (
            "Venus is the natural significator of marriage, and the 7th from "
            "Venus applies in both male and female charts"
        ),
    },
    {
        "rule": (
            "Use the sthira karaka only for timing death, where the karaka is "
            "the relative's body"
        ),
        "wrong": "Venus for the death of a husband in a female chart",
        "right": "Jupiter for the death of a husband in a female chart",
        "because": (
            "sthira karakas represent physical bodies; Jupiter is the husband's "
            "body, while the 7th from Venus is what shows the husband for "
            "timing marriage"
        ),
    },
)

#: Footnote 26 defers the "stronger of the two" comparison to a later chapter,
#: so the sthira karakas for father and mother cannot be resolved from this
#: chapter alone.
STRENGTH_COMPARISON_CHAPTER = "Strength of Planets and Rasis"
