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


# --------------------------------------------------------------------------
# Example 44 — §13.4.1 and §13.4.2 worked over Chart 13
# --------------------------------------------------------------------------

EXAMPLE_44 = (
    "Let us consider the rasi chart given in Chart 13 and start making some "
    "observations."
)

EXAMPLE_44_RASI = (
    "Lagna in Leo can show someone royal and authoritative. Lagna lord Sun is "
    "in the 10th house with 5th lord Jupiter. This forms a raaja yoga. With "
    "Jupiter in Uttamaamsa, this yoga is powerful. Moreover, this yoga takes "
    "place in the 7th from AL. That makes it more powerful. However, we note "
    "that debilitated Moon occupies AL in a Martian sign and Saturn aspects "
    "him. Debilitated Moon in AL shows that the mind is turned away from the "
    "material world. Saturn is the significator of hard-work, service and "
    "austerity and he also signifies renunciation. His aspect on Moon can "
    "give renunciation. Moreover, Saturn is with Ketu here. Overall, there "
    "are parivraaja yogas here. So this native is likely to have renounced "
    "the world."
)

TAPASWI_YOGA_RULE = (
    "Saturn is the planet of hard-work. Ketu is the planet of selflessness, "
    "evolution and rising above the shackles of the material world. Venus is "
    "the planet of passion. If two of these planets are together and the "
    "third planet aspects them, it gives Tapaswi yoga. If AK (chara atma "
    "karaka – soul) also aspects or conjoins the planets involved in Tapaswi "
    "yoga, this tapas will be more fruitful and will be a continuation of the "
    "efforts of the past lives (AK is one's link with the past lives)."
)

#: Tapaswi yoga's three planets and what each stands for.
TAPASWI_PLANETS: dict[str, str] = {
    "Saturn": "hard-work",
    "Ketu": "selflessness, evolution and rising above the shackles of the "
            "material world",
    "Venus": "passion",
}

TAPASWI_STRENGTHENERS = (
    "Tapaswi yoga is particularly powerful when formed with a planet in the "
    "8th house (hard-work, research, discovery and occult knowledge). AK "
    "being involved makes the tapas a continuation of past lives."
)

FOOTNOTE_49 = (
    "Tapaswi is a person who performs tapas. He forgets everything and "
    "pursues something single-mindedly. Tapaswis usually dedicate themselves "
    "to research and uncover the secrets of the world. A tapaswi can be into "
    "yoga, mantra, tantra, astrology or even physics or chemistry."
)

EXAMPLE_44_TAPASWI = (
    "Here Saturn and Ketu are together in Virgo and exalted Venus aspects "
    "them from Pisces. This gives Tapaswi yoga. Tapaswi yoga is particularly "
    "powerful when formed with a planet in the 8th house (hard-work, "
    "research, discovery and occult knowledge). Here Venus is in the 8th "
    "house. AK is also involved in Tapaswi yoga."
)

EXAMPLE_44_D20 = (
    "Let us consider his D-20 now (see Chart 13). D-20 shows religious and "
    "spiritual activities. Lagna is in Pisces and lord Jupiter is in the 9th "
    "house. This shows religiousness and also being guided by a brilliant "
    "guru/parampara. GL in D-20 is in Sc and Jupiter occupies it. It shows a "
    "powerful position in religion."
)

EXAMPLE_44_D20_CONTINUED = (
    "If the 5th and 9th lords conjoin and aspect lagna, we learnt that it "
    "forms a rajayoga. Here 5th lord Moon and 9th lord Mars join in Vi and "
    "aspect lagna in Pi. This shows a powerful rajayoga giving a powerful and "
    "prosperous position related to religious matters. Venus, the planet of "
    "passion, is in the 8th house in own rasi. That shows sincere efforts and "
    "hard-work in religious matters. The 2nd house has Sun and Mercury in it. "
    "The 2nd house shows speech among other things. Mercury is the planet of "
    "speech and he has 6 rekhas in his D-20 BAV. Sun is a charismatic planet "
    "and he has 5 rekhas in D-20 BAV. They together give Budha-Aaditya yoga "
    "in the house of speech. The native is likely to be an excellent orator "
    "of religious matters."
)

EXAMPLE_44_NATIVE = (
    "This chart belongs to Swami Chandrasekhara Saraswathi, who was the chief "
    "pontiff of Kanchi Kama Koti Peetham. He was a great scholar and a keen "
    "student of many subjects. He was a true tapaswi and made a Herculean "
    "contribution in restoring the place of Vedic knowledge in Indian "
    "society. He was a brilliant orator. He commanded the respect of "
    "presidents, prime ministers, chief ministers and millions of Indians."
)

#: Every checkable claim Example 44 makes, as ``(claim, chart, what settles
#: it)``. Each is verified against Chart 13 rather than transcribed.
EXAMPLE_44_CLAIMS: tuple[tuple[str, str, str], ...] = (
    ("Lagna in Leo", "rasi", "Asc 23 Le 10"),
    ("Lagna lord Sun is in the 10th house", "rasi",
     "10th from Leo is Taurus, where the Sun is"),
    ("with 5th lord Jupiter", "rasi",
     "5th from Leo is Sagittarius, whose lord Jupiter is also in Taurus"),
    ("this yoga takes place in the 7th from AL", "rasi",
     "AL is in Scorpio and the 7th from it is Taurus"),
    ("debilitated Moon occupies AL", "rasi",
     "the Moon debilitates in Scorpio, which is where AL falls"),
    ("in a Martian sign", "rasi", "Scorpio is owned by Mars"),
    ("Saturn is with Ketu here", "rasi", "both are in Virgo"),
    ("exalted Venus aspects them from Pisces", "rasi",
     "Venus exalts in Pisces, and Pisces is the 7th from Virgo"),
    ("Here Venus is in the 8th house", "rasi",
     "8th from Leo is Pisces"),
    ("Lagna is in Pisces and lord Jupiter is in the 9th house", "D20",
     "9th from Pisces is Scorpio, where Jupiter falls in the D-20"),
    ("GL in D-20 is in Sc and Jupiter occupies it", "D20",
     "both fall in Scorpio in the D-20"),
    ("5th lord Moon and 9th lord Mars join in Vi", "D20",
     "5th from Pisces is Cancer and 9th is Scorpio; both lords fall in Virgo"),
    ("and aspect lagna in Pi", "D20", "Virgo is the 7th from Pisces"),
    ("Venus ... is in the 8th house in own rasi", "D20",
     "8th from Pisces is Libra, which Venus owns and occupies"),
    ("The 2nd house has Sun and Mercury in it", "D20",
     "2nd from Pisces is Aries, where both fall"),
    ("he has 6 rekhas in his D-20 BAV", "D20",
     "Mercury's own BAV holds 6 in Aries, where he sits"),
    ("he has 5 rekhas in D-20 BAV", "D20",
     "the Sun's own BAV holds 5 in Aries, where he sits"),
)

#: The two figures Example 44 quotes from D-20 ashtakavarga.
EXAMPLE_44_D20_BAV: dict[str, int] = {"Mercury": 6, "Sun": 5}

#: Footnote 48 is cited after "parivraaja yogas" and has not been supplied.
EXAMPLE_44_FOOTNOTE_48_UNSEEN = (
    "Footnote 48 is cited after 'there are parivraaja yogas here' and has not "
    "been supplied. Parivraaja yoga is not defined in any section read so far."
)
