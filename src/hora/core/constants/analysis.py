"""Section 13.4.1 — the basic guidelines for analyzing a chart.

Six factors, each with the worked correspondences §13.4.1 gives. The matters
below are only the ones the section names. Anything else gets a stated verdict
rather than a guess: this is a method, not a lookup table of every question a
chart can be asked.
"""
from __future__ import annotations

ANALYZING_CHARTS_INTRO = (
    "When we analyze the charts, we should remember all the concepts we "
    "learnt in the previous chapters. The following factors must be "
    "remembered:")

#: The six factors, in order, with §13.4.1's own headings.
BASIC_GUIDELINES: tuple[tuple[str, str], ...] = (
    (
        "Divisional Chart",
        "Use the correct divisional chart for the matter of interest.",
    ),
    (
        "House",
        (
            "We should choose the correct house after choosing the correct "
            "divisional chart."
        ),
    ),
    (
        "Reference",
        "We should choose the correct reference for counting houses.",
    ),
    (
        "House vs Arudha",
        (
            "Sometimes, an arudha pada is more appropriate to see a matter than a "
            "house."
        ),
    ),
    (
        "Influences",
        (
            "After we choose a house/arudha in a divisional chart to represent the "
            "matter of interest, the next step is to analyze the influences on it."
        ),
    ),
    (
        "Standard Results",
        (
            "There are many standard results given in literature for various "
            "planets and house lords in various houses. These results should be "
            "mastered."
        ),
    ),
)

#: Factor 1's worked list: matter -> the chart §13.4.1 names for it.
DIVISIONAL_CHART_FOR: tuple[tuple[str, str, str], ...] = (
    ("happiness from a vehicle", "D16", "D-16 is the best chart"),
    ("a criminal's psychology", "D30", "D-30 is the best chart"),
    ("marriage", "D9", "D-9 is the best chart"),
    (
        "marriage as merely living together",
        "D1",
        (
            "in a culture where marriage is not a dharma (duty) and a union of "
            "souls, but it is merely living together of two people, then rasi "
            "chart may be better than D-9"
        ),
    ),
    ("religious activities", "D20", "then D-20 is the chart"),
    ("learning", "D24", "if we want to study one's learning, D-24 is the chart"),
    (
        "career and achievements in society",
        "D10",
        "D-10 chart is the correct chart",
    ),
)

#: §13.4.1 draws factors 2, 3 and 4 out of one worked chart, D-24. Each entry
#: is ``(matter, house, references, arudha, note)``. A reference of "lagna"
#: means the true self and "AL" the perceived self; a graha name means
#: §13.4.1's "when the relevant karakas are stronger, we can use them as
#: references instead of lagna".
D24_MATTERS: tuple[tuple[str, int, tuple[str, ...], str | None, str], ...] = (
    ("education", 4, ("lagna",), None, "we see the 4th house"),
    (
        "intelligence", 5, ("lagna", "Jupiter"), None,
        (
            "related to the true self, so seen from the 5th from lagna; "
            "intelligence can be seen from the 5th from Jupiter"
        ),
    ),
    (
        "scholarship", 5, ("lagna", "Mercury"), None,
        (
            "related to the true self, so seen from the 5th from lagna; "
            "scholarship can be seen from the 5th from Mercury"
        ),
    ),
    (
        "academic reputation", 5, ("AL", "Sun"), None,
        (
            "related more to the perceived self (AL) than the true self (lagna), "
            "so it is seen from the 5th from arudha lagna; academic reputation "
            "can be seen in D-24 from the 5th from Sun"
        ),
    ),
    (
        "academic distinctions and awards", 5, ("lagna",), "A5",
        (
            "we can see one's academic distinctions/awards in A5, because they "
            "are maya (illusion) related to intelligence and scholarship"
        ),
    ),
    (
        "students", 5, ("the 5th lord",), None,
        "students can be seen from the 5th lord",
    ),
    (
        "the people one interacts with while learning", 7, ("lagna",), "A7",
        (
            "we can see darapada (A7) in D-24 to figure out what kind of people "
            "one typically interacts with in one's learning related activities"
        ),
    ),
)

REFERENCE_RULE = (
    "We should choose the correct reference for counting houses. In the above "
    "example of D-24, academic reputation is related more to the perceived "
    "self (AL) than the true self (lagna). So it is seen from the 5th from "
    "arudha lagna (AL). Intelligence and scholarship, on the other hand, are "
    "related to the true self and they are seen from the 5th from lagna. When "
    "the relevant karakas are stronger, we can use them as references instead "
    "of lagna.")

HOUSE_VERSUS_ARUDHA_RULE = (
    "Sometimes, an arudha pada is more appropriate to see a matter than a "
    "house. For example, we can see darapada (A7) in D-24 to figure out what "
    "kind of people one typically interacts with in one's learning related "
    "activities. We can see one's academic distinctions/awards in A5, because "
    "they are maya (illusion) related to intelligence and scholarship. The "
    "world forms an impression about one's intelligence and scholarship based "
    "on one's scores, ranks, grades, distinctions and awards.")

#: The short form §13.4.1 gives for why an arudha is used at all.
ARUDHA_IS_MAYA = (
    "An arudha shows the world's impression of a matter rather than the "
    "matter itself — maya. Distinctions and awards are the impression others "
    "form of intelligence and scholarship, so they are read from A5 and not "
    "from the 5th house.")

INFLUENCES_RULE = (
    "After we choose a house/arudha in a divisional chart to represent the "
    "matter of interest, the next step is to analyze the influences on it. "
    "Planets influence it with rasi drishti and graha drishti. We should also "
    "check for argala. We should judge the meaning of each influence. We can "
    "also judge the influences on a house by finding houses with respect to "
    "that house.")

#: Factor 5's four house classes, counted **from the house or arudha under
#: analysis** rather than from lagna. Each is (houses, what planets there do).
INFLUENCE_FRAME: tuple[tuple[str, tuple[int, ...], str], ...] = (
    ("quadrants", (1, 4, 7, 10), "sustain it"),
    ("trines", (1, 5, 9), "let it prosper"),
    ("upachayas", (3, 6, 10, 11), "let it grow"),
    ("dusthanas", (6, 8, 12), "bring obstacles"),
)

#: The three ways §13.4.1 says a planet reaches a house directly.
INFLUENCE_KINDS = ("rasi drishti", "graha drishti", "argala")

#: §13.4.1's second worked example, in D-10 rather than D-24.
A3_BOOK_WRITING = (
    "Suppose we are analyzing A3 in an author's D-10. While the 3rd house "
    "shows one's writing skills, it is A3 that shows one's books. If a planet "
    "is in a quadrant from A3, its periods may result in book writing. If a "
    "planet is in the 8th house from A3, its periods may bring obstacles in "
    "book writing. If a planet is a baadhaka from A3, it can create troubles "
    "in book-writing.")

#: The A3 example as data: ``(where the planet is, from A3, what its periods
#: do)``. All three rows are computable: the first two are the influence frame
#: above, and the third is section 13.3's baadhaka taken from A3 rather than
#: from lagna.
A3_PERIODS: tuple[tuple[str, str], ...] = (
    ("in a quadrant from A3", "its periods may result in book writing"),
    (
        "in the 8th house from A3",
        "its periods may bring obstacles in book writing",
    ),
    ("a baadhaka from A3", "it can create troubles in book-writing"),
)

#: The 3rd house and A3 answer different questions about the same author.
THIRD_HOUSE_VERSUS_A3 = (
    "The 3rd house shows one's writing skills; A3 shows one's books.")

STANDARD_RESULTS_RULE = (
    "There are many standard results given in literature for various planets "
    "and house lords in various houses. These results should be mastered.")

#: Factor 6 points outside the book. Nothing computes it.
STANDARD_RESULTS_NOT_IMPLEMENTED = (
    "Factor 6 points at the standard results in the classical literature, "
    "which section 13.1 sources to Dr. B.V. Raman's 'How to Judge a "
    "Horoscope'. The book does not reproduce them, so nothing here computes "
    "them.")

ANALYSIS_CLOSING = (
    "Attention should be paid to the strength and avasthas of various planets "
    "and ashtakavarga strength of various houses. The presence of yogas "
    "should also be noted.")

#: What the closing sentence points at, all of it already built.
ANALYSIS_CLOSING_POINTS_AT: tuple[tuple[str, str], ...] = (
    ("strength", "chapter 15's graha bala, at /v1/strength"),
    ("avasthas", "chapter 4's avasthas, at /v1/avasthas"),
    ("ashtakavarga strength of houses", "chapter 12, at /v1/ashtakavarga"),
    ("yogas", "chapter 11's 168 yogas, at /v1/yogas"),
)
