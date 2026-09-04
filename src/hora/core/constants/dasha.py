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
#:
#: ``key`` names a nakshatra system in ``NAKSHATRA_DASHA_SYSTEMS``; ``module``
#: names a rasi dasa's module. A system with neither is not built.
PART_2_DASA_SYSTEMS: tuple[dict, ...] = (
    {"name": "Vimsottari dasa", "kind": "nakshatra",
     "purpose": "phalita/ayur", "key": "vimshottari"},
    {"name": "Ashtottari dasa", "kind": "nakshatra",
     "purpose": "ayur/phalita", "key": "ashtottari"},
    {"name": "Narayana dasa", "kind": "rasi",
     "purpose": "phalita - general", "key": None,
     "module": "hora.dasha.rasi.narayana"},
    {"name": "Lagna Kendradi Rasi dasa", "kind": "rasi",
     "purpose": "phalita - material fortune", "key": None,
     "module": "hora.dasha.rasi.kendradi"},
    {"name": "Sudasa", "kind": "rasi",
     "purpose": "phalita - material fortune", "key": None,
     "module": "hora.dasha.rasi.sudasa"},
    {"name": "Drigdasa", "kind": "rasi",
     "purpose": "phalita - spirituality", "key": None,
     "module": "hora.dasha.rasi.drigdasa"},
    {"name": "Niryaana Shoola dasa", "kind": "rasi",
     "purpose": "ayur", "key": None,
     "module": "hora.dasha.rasi.niryaana_shoola"},
    {"name": "Shoola dasa", "kind": "rasi", "purpose": "ayur", "key": None,
     "module": "hora.dasha.rasi.shoola"},
    {"name": "Kalachakra dasa", "kind": "nakshatra",
     "purpose": "phalita", "key": None,
     "module": "hora.dasha.nakshatra.kalachakra"},
)

#: §24.5's boxed ranking, and the only place Part 2 says which of its nine
#: matter most. Three of the nine are named, each with what it specialises in.
THE_THREE_MOST_IMPORTANT_PHALITA_DASAS = (
    "Narayana dasa specializes in showing what happens in one's life; "
    "Vimsottari dasa specializes in showing how one's mind views what happens "
    "in one's life; and, Kalachakra dasa specializes in showing how one "
    "relates to what happens in one's life and how connected one feels. These "
    "three are the most important of all general purpose phalita dasas."
)

#: The same three as data, with what §24.5 says each is built on and what it
#: therefore shows. ``rank`` is the box's own order.
DASA_SPECIALISATIONS: tuple[dict[str, str | int], ...] = (
    {"rank": 1, "name": "Narayana dasa", "built_on": "the progress of lagna",
     "shows": "what happens in one's life",
     "focus": "the real happenings and the direction taken by one's life"},
    {"rank": 2, "name": "Vimsottari dasa",
     "built_on": "the nakshatra of Moon",
     "shows": "how one's mind views what happens in one's life",
     "focus": "the state of the native's mind as time progresses"},
    {"rank": 3, "name": "Kalachakra dasa", "built_on": "Moon's navamsa",
     "shows": "how one relates to what happens in one's life and how "
              "connected one feels",
     "focus": "the state of the inner self and the sense of connectedness"},
)

#: §24.5's methodological rule, and the reason the three above are not
#: alternatives to one another.
DASAS_ARE_NOT_INTERCHANGEABLE = (
    "It is illogical to use 10 different dasas interchangably. Mixing up "
    "various dasas without knowing the subtle differences between them "
    "results in vague explanations."
)

#: The sentence §24.5 sets in bold, and the whole argument in one line.
DIFFERENT_ANGLES_ON_THE_SAME_EVENT = (
    "Even when different dasas show the same event, they show it from "
    "different angles and focus on different aspects of the same event."
)

#: Why there are so many systems at all — §24.5's answer to a question the
#: part opened with and never answered until here.
WHY_THE_MAHARSHIS_DESCRIBED_HUNDREDS = (
    "Without appreciating this, one cannot understand why maharshis described "
    "tens, if not hundreds, of dasa systems."
)

#: §24.5's closing image, and the shape of any reading layer built on these
#: nine: not a choice between systems but several views of one thing.
DASAS_ARE_VANTAGE_POINTS = (
    "Different dasas do not provide different alternatives that can be used "
    "interchangeably to understand what happens in one's life, but they "
    "provide different angles - or vantage points - to view the same "
    "kaleidoscope that life is."
)

#: The first question §24.5 says to ask of any dasa, and the one Part 2's
#: ``purpose`` column answers for each of the nine.
THE_FIRST_QUESTION_TO_ASK_OF_A_DASA = (
    "When we learn a new dasa, the first question we should ask is \"when "
    "should it be applied and what results should be seen in it\"."
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
    "USE_THE_VARIATIONS",
    "KENDRADI_GRAHA_DASA_INSTEAD",
    "DASA_ERROR_RULE",
    "ASHTOTTARI_IS_CONDITIONAL",
    "ASHTOTTARI_MEANS_108",
    "ASHTOTTARI_HAS_NO_KETU",
    "ASHTOTTARI_ANTARDASA_RULE",
    "ASHTOTTARI_CAVEAT",
    "THE_THREE_MOST_IMPORTANT_PHALITA_DASAS",
    "DASAS_ARE_NOT_INTERCHANGEABLE",
    "DIFFERENT_ANGLES_ON_THE_SAME_EVENT",
    "WHY_THE_MAHARSHIS_DESCRIBED_HUNDREDS",
    "DASAS_ARE_VANTAGE_POINTS",
    "THE_FIRST_QUESTION_TO_ASK_OF_A_DASA",
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


#: §16.7's advice about the variations, which is the chapter's own summary of
#: why §16.4.1 exists.
USE_THE_VARIATIONS = (
    "Though many people limit themselves to Vimsottari dasa started from the "
    "birthstar, one is advised to use the variations mentioned in this "
    "chapter for the best results."
)

#: §16.7's condition for preferring a different dasa system altogether. The
#: comparison it rests on — the stronger of lagna and Moon — is not defined
#: there, and Kendradi Graha Dasa is not among Part 2's nine systems either.
KENDRADI_GRAHA_DASA_INSTEAD = (
    "If all the quadrants from the stronger of lagna and Moon are occupied by "
    "planets, \"Kendradi Graha Dasa\" is more appropriate than Vimsottari "
    "dasa. Results from Vimsottari dasa may not be very good in such cases."
)

#: §16.7's rule of thumb for how birthtime error propagates into dasa dates:
#: about ``m * n / 4`` days, for ``m`` minutes of error and a first dasa of
#: ``n`` years. It is a mean-motion approximation — the true figure scales
#: with the Moon's speed at birth, which ranges roughly ±13% around the mean.
BIRTHTIME_ERROR_DAYS_PER_MINUTE = 0.25

#: Why the rule of thumb matters.
DASA_ERROR_RULE = (
    "the error in the start/end dates of dasas have an error of approximately "
    "m.n/4 days, if there is an error of m minutes in birthtime and the "
    "complete duration of the first dasa is n years. ... Considering this, we "
    "cannot use low level sub-periods of Vimsottari dasa (like sookshma "
    "dasas) confidently, unless we rectify the birthtime."
)


#: Table 39, as printed. Ashtottari does not lay equal nakshatra spans over
#: its lords the way Vimsottari does: three lords cover four nakshatras
#: (53°20') and five cover three (40°0'), and the cycle begins at Ardra rather
#: than Ashwini. Each row is (start degree, arc length, nakshatra count,
#: planet name, dasa years); the arcs run in the table's own order and Rahu's
#: wraps 0°.
ASHTOTTARI_ARCS: tuple[dict, ...] = (
    {"start": 66 + 40 / 60, "length": 53 + 20 / 60, "nakshatras": 4,
     "planet": "Sun", "years": 6},
    {"start": 120.0, "length": 40.0, "nakshatras": 3,
     "planet": "Moon", "years": 15},
    {"start": 160.0, "length": 53 + 20 / 60, "nakshatras": 4,
     "planet": "Mars", "years": 8},
    {"start": 213 + 20 / 60, "length": 40.0, "nakshatras": 3,
     "planet": "Mercury", "years": 17},
    {"start": 253 + 20 / 60, "length": 40.0, "nakshatras": 3,
     "planet": "Saturn", "years": 10},
    {"start": 293 + 20 / 60, "length": 40.0, "nakshatras": 3,
     "planet": "Jupiter", "years": 19},
    {"start": 333 + 20 / 60, "length": 53 + 20 / 60, "nakshatras": 4,
     "planet": "Rahu", "years": 12},
    {"start": 26 + 40 / 60, "length": 40.0, "nakshatras": 3,
     "planet": "Venus", "years": 21},
)

#: §17.1's own account of what the system is for, and how unsettled that is.
ASHTOTTARI_IS_CONDITIONAL = (
    "Sage Parasara listed it as a conditional dasa applicable only in some "
    "charts. The conditions for its applicability are highly controversial."
)

#: Why 108, and why some read it as an ayur dasa.
ASHTOTTARI_MEANS_108 = (
    "the sum of all dasas is 108 years. Ashtottari means \"ashtottara sata\", "
    "i.e. one hundred and eight. Because poornaayush (full life) of a man is "
    "108 years, some scholars have suggested that ashtottari dasa is best "
    "used as an ayur dasa, i.e. a dasa that shows longevity."
)

#: §17.1's reason for reading it through the chara karakas: Ketu has no dasa.
ASHTOTTARI_HAS_NO_KETU = (
    "Because only chara karakas, i.e. Rahu and the seven planets, have dasas "
    "under the Ashtottari dasa scheme, it may also be suggested that it shows "
    "events related to sustenance, achievements, raja yogas and moksha (just "
    "like chara karakas do)."
)


#: §17.2.2's antardasa rule, which differs from Vimsottari's. Kept as a
#: sentence because the difference is easy to read past.
ASHTOTTARI_ANTARDASA_RULE = (
    "The first antardasa belongs to the planet that comes in the table "
    "*after* the dasa lord. Then antardasas go in the same order as dasas and "
    "the last antardasa belongs to dasa lord."
)

#: §17.2.3's three views on when Ashtottari applies. The section gives them
#: without choosing, and §17.1 calls the conditions "highly controversial", so
#: nothing here gates anything — a caller who wants one applies it themselves.
#: ``computable`` says whether the condition can be evaluated from a chart at
#: all; view 1 is vacuous rather than computable.
ASHTOTTARI_APPLICABILITY_VIEWS: tuple[dict, ...] = (
    {"view": 1, "computable": False,
     "text": "Ashtottari dasa is applicable in all charts."},
    {"view": 2, "computable": True,
     "needs": ("Rahu's house from lagna", "Rahu's house from the lagna lord"),
     "text": ("Ashtottari dasa is applicable if Rahu, who is not in lagna, is "
              "in a quadrant or a trine from lagna lord.")},
    {"view": 3, "computable": True,
     "needs": ("whether the birth was by day or night", "the paksha"),
     "text": ("Ashtottari dasa is applicable for daytime births in Krishna "
              "paksha (darker fortnight) and night time births in Sukla "
              "paksha (brighter fortnight).")},
)


#: Chapter 17's own closing caution. It is attached to every Ashtottari
#: response rather than left in a document, because the section says the
#: warning applies with special force to this dasa and a caller reading a
#: result is exactly who needs to see it.
ASHTOTTARI_CAVEAT = (
    "Ashtottari dasa is a popular dasa, but its applicability as well as "
    "application are controversial. Readers should keep this in mind and keep "
    "their minds open to alternative views. What is taught in this book is "
    "not the final truth. Of course, this applies to everything taught in "
    "this book, but it is especially applicable to this chapter."
)
