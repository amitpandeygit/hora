"""Part 2's own map of the dasa systems it will teach.

The part opens by classifying dasa systems two ways and then naming the nine
it covers. That list is a roadmap, not a calculation, but it is worth holding
as data: it says which systems the book considers in scope, what each is for,
and — read against what is built — what is still missing.

Two classifications, both from the opening:

* **nakshatra** dasas run from the Moon's nakshatra; **rasi** dasas run from
  the rasis planets occupy, and their periods are owned by rasis.
* **phalita** dasas give general results; **ayur** dasas predict death.

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

#: Why the classics do not settle which dasa to use when.
DASA_USES_ARE_NOT_IN_THE_CLASSICS = (
    "Hundreds of dasa systems were enumerated by the seers of Vedic "
    "astrologey. Specific uses of these dasa systems weren't clearly "
    "mentioned in classics. These are hidden in remote corners of India as "
    "family secrets."
)

#: The nine systems Part 2 teaches, in the order it lists them. ``kind`` is
#: nakshatra or rasi; ``purpose`` is the part's own parenthesis, kept in its
#: printed order — Vimsottari reads "phalita/ayur" and Ashtottari
#: "ayur/phalita", which is the only thing distinguishing their emphasis.
PART_2_DASA_SYSTEMS: tuple[dict, ...] = (
    {"name": "Vimsottari dasa", "kind": "nakshatra",
     "purpose": "phalita/ayur", "key": "vimshottari"},
    {"name": "Ashtottari dasa", "kind": "nakshatra",
     "purpose": "ayur/phalita", "key": "ashtottari"},
    {"name": "Narayana dasa", "kind": "rasi",
     "purpose": "phalita - general", "key": None},
    {"name": "Lagna Kendradi Rasi dasa", "kind": "rasi",
     "purpose": "phalita - material fortune", "key": None},
    {"name": "Sudasa", "kind": "rasi",
     "purpose": "phalita - material fortune", "key": None},
    {"name": "Drigdasa", "kind": "rasi",
     "purpose": "phalita - spirituality", "key": None},
    {"name": "Niryaana Shoola dasa", "kind": "rasi",
     "purpose": "ayur", "key": None},
    {"name": "Shoola dasa", "kind": "rasi", "purpose": "ayur", "key": None},
    {"name": "Kalachakra dasa", "kind": "nakshatra",
     "purpose": "phalita", "key": None},
)

#: Named in Part 2 but deliberately deferred by it.
DEFERRED_TO_TAJAKA = (
    "Sudarsana Chakra dasa is one of the most important dasas mentioned by "
    "Parasara. However, for reasons that will become clear later, we will "
    "learn it in the part \"Tajaka Analysis\"."
)

#: Whole constants that are a transcribed sentence or passage.
DASHA_VERBATIM_CONSTANTS: tuple[str, ...] = (
    "DASA_USES_ARE_NOT_IN_THE_CLASSICS",
    "DEFERRED_TO_TAJAKA",
    "VARIATIONS_ARE_OFTEN_IGNORED",
    "DASA_FROM_LAGNA",
    "DASA_LORD_AS_TEMPORARY_LAGNA",
    "NO_GUIDELINES_FOR_SIGN_STRENGTH",
    "STAR_SPANNING_TWO_SIGNS",
    "TRIPOD_PRINCIPLE",
)


#: §16.4.1's three alternative starting constellations, counted inclusively
#: from the Moon's own. The fraction left at birth always comes from the
#: Moon's own star; only the lord of the first dasa and the sequence move.
VIMSOTTARI_VARIATIONS: tuple[dict, ...] = (
    {"star": 1, "name": "Moon's own", "note": "the usual reckoning"},
    {"star": 4, "name": "kshema", "note": None},
    {"star": 5, "name": "utpanna", "note": None},
    {"star": 8, "name": "adhana", "note": None},
)

#: Why the variations exist at all.
VARIATIONS_ARE_OFTEN_IGNORED = (
    "Many contemporary Vedic astrologers ignore these variations and always "
    "reckon dasas from the lord of the constellation occupied by Moon. "
    "However, this may not result in the best predictions always."
)


#: §16.4.2's alternative seed, and its own caveat.
DASA_FROM_LAGNA = (
    "Some authorities have also recommended Vimsottari dasa from the longitude "
    "of lagna instead of Moon. In practice, this will give better results only "
    "when lagna is considerably more powerful than Moon."
)

#: §16.5.1's nine illustrations of reading a dasa. The section calls them
#: "just a few examples", so this is a register of what a reading looks like,
#: not a lookup table — `divisional` is the chart each one reads, and `reads`
#: is the placement it looks for.
VIMSOTTARI_READING_EXAMPLES: tuple[dict, ...] = (
    {"n": 1, "divisional": "D-7", "reads": "the 5th lord",
     "gives": "a child", "certainty": "can"},
    {"n": 2, "divisional": "rasi", "reads": "the 8th lord",
     "gives": "some troubles and frustration", "certainty": "can"},
    {"n": 3, "divisional": "D-10", "reads": "a planet exalted in GL",
     "gives": "power and authority in career", "certainty": "can"},
    {"n": 4, "divisional": "D-9", "reads": "an exalted planet in the 12th from AK",
     "gives": "serious thoughts related to spiritual liberation",
     "certainty": "can"},
    {"n": 5, "divisional": "D-9", "reads": "the 7th lord",
     "gives": "marriage", "certainty": "can"},
    {"n": 6, "divisional": "D-4", "reads": "a planet with Rahu in the 9th",
     "gives": "foreign residence", "certainty": "can"},
    {"n": 7, "divisional": "rasi",
     "reads": "an exalted planet aspecting HL from the 11th from AL",
     "gives": "a lot of wealth", "certainty": "can"},
    {"n": 8, "divisional": "D-30",
     "reads": "a planet joined by Moon and Saturn in the 8th house",
     "gives": "serious psychological problems and suicidal tendencies",
     "certainty": "may"},
    {"n": 9, "divisional": "D-10",
     "reads": "a well-disposed planet aspecting A3",
     "gives": "writing some books", "certainty": "may"},
)

#: The section's closing technique, which is a rule rather than an example.
DASA_LORD_AS_TEMPORARY_LAGNA = (
    "Each planet gives the results indicated by it in its dasas and "
    "antardasas. When analyzing antardasas, we can take the dasa lord as a "
    "temporary lagna and analyze the charts."
)


#: §16.5.2 admits the comparison it depends on is not defined anywhere.
NO_GUIDELINES_FOR_SIGN_STRENGTH = (
    "How do we know which sign is stronger? There are no clear guidelines in "
    "the literature to compare the strengths."
)

#: §16.5.2's rule for choosing a variation, one entry per purpose. The two
#: `stronger_when` clauses are opposites, and deliberately so: a sign that is
#: stronger for reading general results is not the sign that is stronger for
#: reading longevity.
VARIATION_CHOICE: dict[str, dict] = {
    "general": {
        "compare": (1, 5),
        "prefer": "utpanna",
        "stronger_when": (
            "A sign aspected by Jupiter and occupied by more planets may be "
            "taken to be stronger."
        ),
        "fallback": (
            "We can also use known events to see which dasa is working better."
        ),
    },
    "longevity": {
        "compare": (1, 4, 8),
        "prefer": "kshema or adhana",
        "stronger_when": (
            "Here a sign aspected by marakas and malefics becomes stronger."
        ),
        "fallback": None,
    },
}

#: The pada rule that resolves a star straddling two signs.
STAR_SPANNING_TWO_SIGNS = (
    "If the 5th star spans across 2 signs, take the sign containing the same "
    "quarter as occupied by Moon in birthstar."
)


#: §16.5.3's tripod, innermost ring of the Sudarsana chakra first. `changes`
#: orders how fast each one's results turn over: the soul's last long and
#: change slowly, the mind's are shorter and faster, the body's faster still.
TRIPOD_OF_LIFE: tuple[dict, ...] = (
    {"reference": "lagna", "stands_for": "body", "ring": "innermost",
     "judges": "pratyantardasa", "changes": 3},
    {"reference": "Moon", "stands_for": "mind", "ring": "middle",
     "judges": "antardasa", "changes": 2},
    {"reference": "Sun", "stands_for": "soul", "ring": "outermost",
     "judges": "mahadasa", "changes": 1},
)

#: Which dasa level a yoga shows its results in, by the yoga's own group.
#: §16.5.3 names two groups and sends everything else to one place; the
#: mapping is on our registry's group names so it can actually be applied.
YOGA_LEVEL_BY_GROUP: dict[str, str] = {
    "ravi": "mahadasa",
    "chandra": "antardasa",
}

#: Where any other yoga shows, "primarily" being the section's own hedge.
YOGA_LEVEL_DEFAULT = "pratyantardasa"

#: The principle as printed, and whose it is.
TRIPOD_PRINCIPLE = (
    "Sun, Moon and lagna form the \"tripod of life\". Parasara clearly said "
    "that we should analyze all charts with respect to the positions of Sun, "
    "Moon and lagna."
)
