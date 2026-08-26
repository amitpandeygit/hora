"""Varga chakra vocabulary — book §1.3.5.

The section that says what a divisional chart *is*, before chapter 6 says how
each one is built. The rules themselves live in :mod:`hora.charts.vargas`,
which cannot be re-exported from :mod:`hora.core.const` because it imports
from it; this module holds the naming and the two general statements chapter 6
assumes without restating.

Split out of the other constants files because §1.3.5 is the only section that
defines these, and they belong to no existing domain file.
"""
from __future__ import annotations

#: §1.3.5: "divisional charts" (Sanskrit name: varga chakras)".
VARGA_CHAKRA_NAME = "varga chakra"

#: §1.3.5 gives a third name in passing: "we draw divisional charts (or
#: harmonic charts)".
VARGA_ALIASES: tuple[str, ...] = ("divisional chart", "harmonic chart")

#: §6.2.1 gives the rasi chart a second name: "It is also called "kshetra
#: chakra"." The only varga in the book with its own name.
D1_ALIAS = "kshetra chakra"

#: §6.2.1 defines what a varga chart places. Worth storing because it is the
#: only place the book says the upagrahas and special lagnas belong in a
#: divisional chart at all, not only the nine grahas.
VARGA_BODY_DEFINITION = (
    "By \u201cbody\u201d here, we mean planets, upagrahas, lagna or special lagnas "
    "\u2013 basically a physical or a mathematical point in the zodiac that has a "
    "longitude associated with it."
)

#: §6.2.2's NOTE. The rule it gives is right as far as it goes; the book
#: declines to complete it. See OI-52.
D2_INCOMPLETE_NOTE = (
    "Though absolutely correct, the above is not quite complete. Proper use "
    "of hora chart is beyond the scope of this book. So we will ignore and "
    "not use hora chart in this book."
)

#: §1.3.5's general definition. Chapter 6 gives a rule per chart and never
#: restates the thing they all are.
VARGA_DEFINITION = (
    "We divide each rasi into n parts and map each part to a rasi again"
)

#: §6.6's definition of amsabala \u2014 the only strength in the chapter, and the
#: one every varga group scores.
AMSABALA_RULE = (
    "If a planet is in its moolatrikona or an own rasi or its rasi of "
    "exaltation in a chart, it makes the planet very strong in that chart. In "
    "each group of divisional charts, we can count the divisional charts in "
    "which a planet occupies its moolatrikona or an own rasi or its rasi of "
    "exaltation."
)

#: §6.6: "the higher this number is, the stronger the planet is."
AMSABALA_IS_MONOTONIC = "the higher this number is, the stronger the planet is"

#: The three dignities that count towards amsabala. Debilitation does not
#: subtract \u2014 the count only ever goes up.
AMSABALA_DIGNITIES = ("moolatrikona", "own", "exalted")

#: §6.6.1 to §6.6.4 each gloss their group's name literally.
VARGA_GROUP_MEANINGS = {
    "shadvarga": "six divisions",
    "saptavarga": "seven divisions",
    "dasavarga": "ten divisions",
    "shodasavarga": "sixteen divisions",
}

#: §6.6.3's NOTE, the only place the chapter says what an amsa is *for*.
DASAVARGA_NOTE = (
    "This group is very important and some yogas \u2013 special combinations \u2013 "
    "make use of these amsas. For example, lagna lord or ghati lagna lord in "
    "Simhaasanaamsa would make one very famous. A quadrant lord with good "
    "amsabala in dasavarga makes one very successful. Readers should memorize "
    "the above amsas."
)

#: The two combinations §6.6.3's NOTE names. Neither is implemented \u2014 both
#: need yogas, which are a later chapter. See OI-54.
DASAVARGA_COMBINATIONS = (
    {
        "condition": "lagna lord or ghati lagna lord in Simhaasanaamsa",
        "amsa": "Simhaasanaamsa",
        "group": "dasavarga",
        "result": "very famous",
    },
    {
        "condition": "a quadrant lord with good amsabala in dasavarga",
        "amsa": None,
        "group": "dasavarga",
        "result": "very successful",
    },
)

#: §6.5's method, and the reason Table 11 is an index rather than a list.
CHOOSE_CHART_BY_MATTER = (
    "We should choose the divisional chart to analyze, based on the matter we "
    "are interested in."
)

#: §6.5's general procedure, which every later chapter applies.
FIND_LINKS_METHOD = (
    "We should remember which planets, rasis and houses show a particular "
    "matter and find links between them in the divisional chart of interest."
)

#: §6.5's closing claim.
KEY_TO_CHART_ANALYSIS = (
    "In this manner, we should analyze the divisional chart that signifies "
    "the sphere of life that we are interested in and analyze the houses that "
    "show the matter of interest. This is the key to correct chart analysis."
)

#: §6.5's two worked patterns. Not calculations \u2014 they are the shape an
#: analysis takes, and both name the chart, the houses and the significator.
MATTER_ANALYSIS_PATTERNS = (
    {
        "matter": "going abroad",
        "chart": "D4",
        "why": "It is related to residence and fortune.",
        "houses": [9, 12],
        "significator": "Rahu",
        "link": (
            "If 12th lord is with Rahu in the 9th house in D-4, it can suggest "
            "that one would live abroad, probably during the periods of Rahu "
            "or 12th lord or 9th house."
        ),
    },
    {
        "matter": "promotion at the office",
        "chart": "D10",
        "why": "D-10 shows one's career and achievements.",
        "houses": [5, 10],
        "significator": "GL",
        "link": (
            "Because GL (ghati lagna) shows power and authority, planets or "
            "rasis giving a promotion are usually connected with GL. Because "
            "AL shows status, planets associating with AL or the 5th or the "
            "10th from it are favorable. If the lord of AL is in the 10th from "
            "it and aspects GL, probably his period will give a promotion."
        ),
    },
)

#: Footnote 12, attached to \u00a76.4's kaarmic paragraph. A caution about the
#: three highest charts, not about the arithmetic \u2014 which we compute either
#: way. See OI-53 for the three charts beyond even these.
HIGHER_CHARTS_CAUTION = (
    "The content of this paragraph has philosophical undercurrents that may "
    "be difficult to understand for students without a good background in "
    "Hindu philosophy. This knowledge should be learnt directly from a "
    "competent guru. Readers are advised to leave these higher charts until "
    "they find one."
)
HIGHER_CHARTS_CAUTIONED = ("D40", "D45", "D60")

#: §6.4 groups the twenty charts into four planes by the **number of
#: divisions**, not by the chart's subject. The boundaries are 1-12, 13-24,
#: 25-36 and above 36, so a chart's plane follows from its n alone.
VARGA_PLANES = (
    {
        "plane": "physical",
        "divisions": "1 to 12",
        "low": 1,
        "high": 12,
        "shows": (
            "Body, wealth, residence, wife, children, parents \u2013 these are all "
            "matters relating to the physical self."
        ),
    },
    {
        "plane": "mental",
        "divisions": "13 to 24",
        "low": 13,
        "high": 24,
        "shows": (
            "Sense of pleasure and unhappiness, religiousness, learning and "
            "knowledge \u2013 these are all matters relating to the mind and "
            "intellect."
        ),
    },
    {
        "plane": "sub-conscious",
        "divisions": "25 to 36",
        "low": 25,
        "high": 36,
        "shows": (
            "One's strengths, weaknesses, inherent nature, evils, certain "
            "psychological imbalances \u2013 these are all matters relating to the "
            "sub-conscious self."
        ),
    },
    {
        "plane": "kaarmic",
        "divisions": "above 36",
        "low": 37,
        "high": None,
        "shows": (
            "Based on the karma from previous lives, we all have an existence "
            "at a level that goes beyond the levels of body, mind and "
            "sub-consciousness."
        ),
    },
)

#: §6.4: the kaarmic plane is "above physical self, mind and sub-conscious
#: self" \u2014 a hierarchy, not a fourth peer.
KAARMIC_PLANE_IS_ABOVE = (
    "a kaarmic plane of existence that is above physical self, mind and "
    "sub-conscious self"
)

#: §1.3.5's premise for the per-chart significations in chapter 6's Tables 11
#: and 20.
VARGA_SIGNIFIES_AN_AREA = (
    "Each divisional chart throws light on a specific area of one's life"
)

#: §1.3.5's rule, and the one that licenses computing houses, arudhas and the
#: rest *inside* a divisional chart from that chart's own lagna — as Exercises
#: 12 and 13 do in D-16. Without it, using the D-16 lagna rather than the rasi
#: lagna would be convention rather than instruction.
VARGA_INDEPENDENT_CHART_RULE = (
    "In each divisional chart, we find houses and analyze the chart as if it "
    "were an independent chart"
)

#: §1.3.5: "The science of Vedic astrology stands on the basis of 4 pillars -
#: (1) grahas or planets, (2) rasis or signs, (3) bhavas or houses, and,
#: (4) varga chakras or divisional charts."
#:
#: §6.7 states the same four in a **different order** — grahas, rasis, vargas,
#: bhavas — and then calls divisional charts "the third pillar". The two
#: orderings cannot both be indexed by number; see docs/book-deviations.md
#: D-23. This list follows §1.3.5, the section that defines them.
FOUR_PILLARS: tuple[dict, ...] = (
    {"number": 1, "sanskrit": "grahas", "english": "planets"},
    {"number": 2, "sanskrit": "rasis", "english": "signs"},
    {"number": 3, "sanskrit": "bhavas", "english": "houses"},
    {"number": 4, "sanskrit": "varga chakras", "english": "divisional charts"},
)

#: §6.7's ordering, kept so the discrepancy is visible rather than resolved by
#: silently preferring one.
FOUR_PILLARS_CONCLUSION_ORDER: tuple[str, ...] = (
    "grahas", "rasis", "vargas", "bhavas",
)
