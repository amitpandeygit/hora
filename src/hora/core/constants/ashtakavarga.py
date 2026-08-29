"""Chapter 12 — Ashtakavarga.

**Shape.** Each table is stored in the orientation the book prints it: twelve
rows, one per house, each row holding eight entries in the column order
`ASHTAKAVARGA_REFERENCES`. That is what a reader checks against the page. The
computational form — reference to the houses it makes benefic — is derived
from it in `charts/ashtakavarga.py`, never typed twice.

Only Table 19 has been supplied. `ASHTAKAVARGA_TABLES` holds what exists and
`ASHTAKAVARGA_TABLES_PENDING` names what does not, so nothing reads a missing
table as an empty one.
"""
from __future__ import annotations

ASHTAKAVARGA_MEANS = (
    "Ashtaka means “consisting of eight” and varga means “a group”. "
    "Ashtakavarga is the system of analyzing a chart with respect to a group "
    "of 8 reference points.")

ASHTAKAVARGA_INTRO = (
    "Analyzing a chart and making correct predictions requires mixing many "
    "different principles and making fine compromises and judgments. Sage "
    "Parasara said that it is difficult for even great Maharshis. In Kali "
    "Yuga, human beings become sinful and the sins kill their intelligence. "
    "Parasara said that the intellectual pygmies of Kali Yuga cannot cope "
    "with too many complicated principles and presented ashtakavarga as a "
    "simple technique that lets them make reasonable predictions without much "
    "fuss.")

ASHTAKAVARGA_REFERENCE_POINT_NOTE = (
    "When we analyze the positions of planets with respect to lagna, we have "
    "the concept of good and bad placements. For example, Jupiter in the 9th "
    "from lagna will be well placed and Jupiter in the 3rd will be badly "
    "placed. Mars in the 3rd from lagna will be well placed and Mars in the "
    "9th will be badly placed.")

ASHTAKAVARGA_ALL_PLANETS_ARE_REFERENCES = (
    "However, lagna is not the only reference point in a chart. We have Sun "
    "and Moon. In fact, all the planets serve as reference points in a chart "
    "and they represent the sources of various energies that are present in a "
    "native. Based on the houses in which different planets are placed in "
    "transit, they can be benefic with respect to some energy sources and "
    "malefic with respect to some. If a transiting planet is benefic with "
    "respect to more energy sources, then it brings good results.")

ASHTAKAVARGA_PURPOSE = (
    "So ashtakavarga is essentially a system that tells us the benefic "
    "positions of lagna and seven planets with respect to each other. This "
    "can be used to analyze the strength of a natal chart, but it is much "
    "more important in analyzing transits.")

#: Footnote 41.
YUGA_FOOTNOTE = (
    "As per Vedic science, time is divided into a cycle of four Yugas that "
    "keep repeating. Those are: Krita yuga (1,728,000 years), Treta yuga "
    "(1,296,000 years), Dwapara yuga (864,000 years) and Kali yuga (432,000 "
    "years). In Krita yuga, religiousness and virtuosity of human beings is "
    "exemplary. It is the worst in Kali yuga. It gradually worsens from Krita "
    "yuga to Kali yuga. We are currently in Kali yuga. It started about 5,000 "
    "years back.")

YUGA_YEARS: tuple[tuple[str, int], ...] = (
    ("Krita", 1_728_000), ("Treta", 1_296_000),
    ("Dwapara", 864_000), ("Kali", 432_000),
)

#: The eight reference points, in the column order every table prints.
ASHTAKAVARGA_REFERENCES: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna")

#: The eight tables, by the planet (or lagna) whose ashtakavarga they define.
ASHTAKAVARGA_TABLE_NUMBERS: dict[str, int] = {
    "Sun": 19, "Moon": 20, "Mars": 21, "Mercury": 22,
    "Jupiter": 23, "Venus": 24, "Saturn": 25, "Lagna": 26,
}

# --------------------------------------------------------------------------
# What 0 and 1 mean — and the naming trap in footnote 42
# --------------------------------------------------------------------------

ASHTAKAVARGA_NOTATION = (
    "In Table 19, an entry of 0 denotes a malefic position or a “karana” or a "
    "bindu (dot). An entry of 1 denotes a benefic position or a “sthana” or a "
    "rekha (line).")

#: Footnote 42. PVR's naming is the reverse of the one most modern software
#: and most south Indian practice uses, and he says which he follows.
BINDU_REKHA_FOOTNOTE = (
    "Some astrologers (especially south Indian astrologers) use a different "
    "notation. They use “bindu” to describe a benefic house (1) and “rekha” "
    "to describe malefic house (0). Let us follow Parasara.")

#: Under PVR's naming a **rekha** is the benefic entry. Anything that counts
#: "bindus in a sign" in the ordinary modern sense is counting rekhas here.
ASHTAKAVARGA_BENEFIC_TERM = "rekha"
ASHTAKAVARGA_MALEFIC_TERM = "bindu"
ASHTAKAVARGA_BENEFIC_SANSKRIT = "sthana"
ASHTAKAVARGA_MALEFIC_SANSKRIT = "karana"

# --------------------------------------------------------------------------
# Table 19 — the Sun's ashtakavarga
#
# Transcribed in the printed orientation: one row per house, eight columns in
# ASHTAKAVARGA_REFERENCES order.
# --------------------------------------------------------------------------

SUN_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (1,  0,  1,  0,  0,  0,  1,  0),   # 1st
    (1,  0,  1,  0,  0,  0,  1,  0),   # 2nd
    (0,  1,  0,  1,  0,  0,  0,  1),   # 3rd
    (1,  0,  1,  0,  0,  0,  1,  1),   # 4th
    (0,  0,  0,  1,  1,  0,  0,  0),   # 5th
    (0,  1,  0,  1,  1,  1,  0,  1),   # 6th
    (1,  0,  1,  0,  0,  1,  1,  0),   # 7th
    (1,  0,  1,  0,  0,  0,  1,  0),   # 8th
    (1,  0,  1,  1,  1,  0,  1,  0),   # 9th
    (1,  1,  1,  1,  0,  0,  1,  1),   # 10th
    (1,  1,  1,  1,  1,  0,  1,  1),   # 11th
    (0,  0,  0,  1,  0,  1,  0,  1),   # 12th
)


MOON_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (0,  1,  0,  1,  1,  0,  0,  0),   # 1st
    (0,  0,  1,  0,  1,  0,  0,  0),   # 2nd
    (1,  1,  1,  1,  0,  1,  1,  1),   # 3rd
    (0,  0,  0,  1,  1,  1,  0,  0),   # 4th
    (0,  0,  1,  1,  0,  1,  1,  0),   # 5th
    (1,  1,  1,  0,  0,  0,  1,  1),   # 6th
    (1,  1,  0,  1,  1,  1,  0,  0),   # 7th
    (1,  0,  0,  1,  1,  0,  0,  0),   # 8th
    (0,  1,  0,  0,  0,  1,  0,  0),   # 9th
    (1,  1,  1,  1,  1,  1,  0,  1),   # 10th
    (1,  1,  1,  1,  1,  1,  1,  1),   # 11th
    (0,  0,  0,  0,  0,  0,  0,  0),   # 12th
)

MARS_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (0,  0,  1,  0,  0,  0,  1,  1),   # 1st
    (0,  0,  1,  0,  0,  0,  0,  0),   # 2nd
    (1,  1,  0,  1,  0,  0,  0,  1),   # 3rd
    (0,  0,  1,  0,  0,  0,  1,  0),   # 4th
    (1,  0,  0,  1,  0,  0,  0,  0),   # 5th
    (1,  1,  0,  1,  1,  1,  0,  1),   # 6th
    (0,  0,  1,  0,  0,  0,  1,  0),   # 7th
    (0,  0,  1,  0,  0,  1,  1,  0),   # 8th
    (0,  0,  0,  0,  0,  0,  1,  0),   # 9th
    (1,  0,  1,  0,  1,  0,  1,  1),   # 10th
    (1,  1,  1,  1,  1,  1,  1,  1),   # 11th
    (0,  0,  0,  0,  1,  1,  0,  0),   # 12th
)


MERCURY_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (0,  0,  1,  1,  0,  1,  1,  1),   # 1st
    (0,  1,  1,  0,  0,  1,  1,  1),   # 2nd
    (0,  0,  0,  1,  0,  1,  0,  0),   # 3rd
    (0,  1,  1,  0,  0,  1,  1,  1),   # 4th
    (1,  0,  0,  1,  0,  1,  0,  0),   # 5th
    (1,  1,  0,  1,  1,  0,  0,  1),   # 6th
    (0,  0,  1,  0,  0,  0,  1,  0),   # 7th
    (0,  1,  1,  0,  1,  1,  1,  1),   # 8th
    (1,  0,  1,  1,  0,  1,  1,  0),   # 9th
    (0,  1,  1,  1,  0,  0,  1,  1),   # 10th
    (1,  1,  1,  1,  1,  1,  1,  1),   # 11th
    (1,  0,  0,  1,  1,  0,  0,  0),   # 12th
)

JUPITER_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (1,  0,  1,  1,  1,  0,  0,  1),   # 1st
    (1,  1,  1,  1,  1,  1,  0,  1),   # 2nd
    (1,  0,  0,  0,  1,  0,  1,  0),   # 3rd
    (1,  0,  1,  1,  1,  0,  0,  1),   # 4th
    (0,  1,  0,  1,  0,  1,  1,  1),   # 5th
    (0,  0,  0,  1,  0,  1,  1,  1),   # 6th
    (1,  1,  1,  0,  1,  0,  0,  1),   # 7th
    (1,  0,  1,  0,  1,  0,  0,  0),   # 8th
    (1,  1,  0,  1,  0,  1,  0,  1),   # 9th
    (1,  0,  1,  1,  1,  1,  0,  1),   # 10th
    (1,  1,  1,  1,  1,  1,  0,  1),   # 11th
    (0,  0,  0,  0,  0,  0,  1,  0),   # 12th
)


VENUS_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (0,  1,  0,  0,  0,  1,  0,  1),   # 1st
    (0,  1,  0,  0,  0,  1,  0,  1),   # 2nd
    (0,  1,  1,  1,  0,  1,  1,  1),   # 3rd
    (0,  1,  1,  0,  0,  1,  1,  1),   # 4th
    (0,  1,  0,  1,  1,  1,  1,  1),   # 5th
    (0,  0,  1,  1,  0,  0,  0,  0),   # 6th
    (0,  0,  0,  0,  0,  0,  0,  0),   # 7th
    (1,  1,  0,  0,  1,  1,  1,  1),   # 8th
    (0,  1,  1,  1,  1,  1,  1,  1),   # 9th
    (0,  0,  0,  0,  1,  1,  1,  0),   # 10th
    (1,  1,  1,  1,  1,  1,  1,  1),   # 11th
    (1,  1,  1,  0,  0,  0,  0,  0),   # 12th
)

SATURN_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (1,  0,  0,  0,  0,  0,  0,  1),   # 1st
    (1,  0,  0,  0,  0,  0,  0,  0),   # 2nd
    (0,  1,  1,  0,  0,  0,  1,  1),   # 3rd
    (1,  0,  0,  0,  0,  0,  0,  1),   # 4th
    (0,  0,  1,  0,  1,  0,  1,  0),   # 5th
    (0,  1,  1,  1,  1,  1,  1,  1),   # 6th
    (1,  0,  0,  0,  0,  0,  0,  0),   # 7th
    (1,  0,  0,  1,  0,  0,  0,  0),   # 8th
    (0,  0,  0,  1,  0,  0,  0,  0),   # 9th
    (1,  0,  1,  1,  0,  0,  0,  1),   # 10th
    (1,  1,  1,  1,  1,  1,  1,  1),   # 11th
    (0,  0,  1,  1,  1,  1,  0,  0),   # 12th
)


LAGNA_ASHTAKAVARGA_ROWS: tuple[tuple[int, ...], ...] = (
    #  Sun Moon Mars Merc  Jup  Ven  Sat  Lag        house
    (0,  0,  1,  1,  1,  1,  1,  0),   # 1st
    (0,  0,  0,  1,  1,  1,  0,  0),   # 2nd
    (1,  1,  1,  0,  0,  1,  1,  1),   # 3rd
    (1,  0,  0,  1,  1,  1,  1,  0),   # 4th
    (0,  0,  0,  0,  1,  1,  0,  0),   # 5th
    (1,  1,  1,  1,  1,  0,  1,  1),   # 6th
    (0,  0,  0,  0,  1,  0,  0,  0),   # 7th
    (0,  0,  0,  1,  0,  1,  0,  0),   # 8th
    (0,  0,  0,  0,  1,  1,  0,  0),   # 9th
    (1,  1,  1,  1,  1,  0,  1,  1),   # 10th
    (1,  1,  1,  1,  1,  0,  1,  1),   # 11th
    (1,  1,  0,  0,  0,  0,  0,  0),   # 12th
)

#: The total rekhas each table carries, as the wider tradition records them.
#:
#: **A check, not a source.** These figures are not PVR's — the book prints
#: the tables and no totals. They are used only to test a transcription of
#: ninety-six hand-typed entries, and a mismatch is reported, never silently
#: corrected. Their sum, 337, is the classical sarvashtakavarga total.
CLASSICAL_TABLE_TOTALS: dict[str, int] = {
    "Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
    "Jupiter": 56, "Venus": 52, "Saturn": 39, "Lagna": 49,
}

CLASSICAL_TABLE_TOTALS_PROVENANCE = (
    "Not from this book. The chapter prints the tables and gives no totals. "
    "These figures come from the wider tradition and are used only as a check "
    "on the transcription; a mismatch would be reported, never corrected.")

#: Tables supplied so far, by owner.
ASHTAKAVARGA_TABLES: dict[str, tuple[tuple[int, ...], ...]] = {
    "Sun": SUN_ASHTAKAVARGA_ROWS,
    "Moon": MOON_ASHTAKAVARGA_ROWS,
    "Mars": MARS_ASHTAKAVARGA_ROWS,
    "Mercury": MERCURY_ASHTAKAVARGA_ROWS,
    "Jupiter": JUPITER_ASHTAKAVARGA_ROWS,
    "Venus": VENUS_ASHTAKAVARGA_ROWS,
    "Saturn": SATURN_ASHTAKAVARGA_ROWS,
    "Lagna": LAGNA_ASHTAKAVARGA_ROWS,
}

#: Tables 20 to 26, named by the book and not yet supplied. Listed so a
#: missing table is a stated gap rather than a silent zero.
ASHTAKAVARGA_TABLES_PENDING: tuple[str, ...] = tuple(
    owner for owner in ASHTAKAVARGA_TABLE_NUMBERS
    if owner not in ASHTAKAVARGA_TABLES)

#: The book's own worked reading of Table 19, kept as a check on the
#: transcription's orientation.
TABLE_19_WORKED_READING = (
    "To understand how to read this table, let us go to the column titled "
    "“Merc” in Table 19. This shows benefic houses for Sun to occupy, with "
    "respect to Mercury. The 1st and 2nd houses have 0 and the 3rd house has "
    "1. So the first 2 houses from Mercury are malefic for Sun and the 3rd "
    "house is benefic for Sun.")

TABLES_20_TO_26_NOTE = (
    "Table 20-Table 26 give the benefic and malefic houses of Moon, Mars, "
    "Mercury, Jupiter, Venus, Saturn and lagna (respectively).")


# --------------------------------------------------------------------------
# §12.2's worked example and exercise
# --------------------------------------------------------------------------

EXAMPLE_37 = (
    "Let us say Venus is in Ge. Find the rasis in which Jupiter is benefic "
    "with respect to Venus.")

EXAMPLE_37_WORKING = (
    "To find the rasis in which Jupiter is benefic, we should look at "
    "Jupiter's ashtakavarga (see Table 23). To find the rasis in which "
    "Jupiter is benefic with respect to Venus, we should look at the column "
    "of Venus. Only the 2nd, 5th, 6th, 9th, 10th and 11th houses have a 1 "
    "(rekha – benefic point) against them. Venus is in Ge and finding these "
    "houses with respect to Venus, we get Cn, Li, Sc, Aq, Pi and Ar. So "
    "Jupiter is benefic with respect to Venus in these rasis.")

EXAMPLE_37_HOUSES: tuple[int, ...] = (2, 5, 6, 9, 10, 11)
EXAMPLE_37_RASIS: tuple[str, ...] = ("Cn", "Li", "Sc", "Aq", "Pi", "Ar")

EXERCISE_18 = (
    "Consider the rasi chart in Chart 6. Find the rasis in which Mercury is "
    "benefic with respect to different planets and lagna.")

EXERCISE_18_HINT = (
    "See Table 22 for Mercury's ashtakavarga. Looking at the columns of "
    "different planets, find the houses from the planets in which Mercury is "
    "benefic. Count those houses from the respective planets and find the "
    "rasis.")

#: The printed answer, reference by reference.
EXERCISE_18_ANSWER: dict[str, tuple[str, ...]] = {
    "Sun": ("Ar", "Ta", "Li", "Sc", "Aq"),
    "Moon": ("Ar", "Ge", "Le", "Li", "Sg", "Cp"),
    "Mars": ("Ar", "Ge", "Cn", "Vi", "Sg", "Cp", "Aq", "Pi"),
    "Mercury": ("Ar", "Ta", "Ge", "Le", "Li", "Sc", "Aq", "Pi"),
    "Jupiter": ("Ge", "Cn", "Cp", "Pi"),
    "Venus": ("Ar", "Ta", "Ge", "Cn", "Le", "Sc", "Sg", "Aq"),
    "Saturn": ("Ar", "Ta", "Ge", "Le", "Vi", "Sc", "Aq", "Pi"),
    "Lagna": ("Ar", "Ge", "Cn", "Vi", "Li", "Sg", "Aq"),
}


# --------------------------------------------------------------------------
# 12.3 Bhinna Ashtakavarga
# --------------------------------------------------------------------------

BHINNA_MEANS = "separate"

BAV_DEFINITION = (
    "In this book, we will denote ashtakavarga with AV. We prepare what is "
    "known as “Bhinna Ashtakavarga” for each planet. It is denoted with BAV. "
    "Bhinna means “separate”. When preparing the BAV of a planet, we count "
    "the number of references from which the planet is benefic in each rasi "
    "and put that count in that rasi. For each planet, we prepare a different "
    "BAV. Sometimes we may simply use the word “ashtakavarga” (AV) to "
    "represent a BAV.")

BAV_GRADING = (
    "The count in each rasi is between 0 to 8. It is called the number of "
    "rekhas (benefic points) in that rasi. If a planet is in a sign with a "
    "count of 5, 6, 7 or 8, it means that the planet is benefic in that rasi "
    "with respect to more references. So the planet is favorable. If a planet "
    "is in a sign with a count of 3, 2, 1 or 0, it means that the planet is "
    "malefic in that rasi with respect to more references. So the planet is "
    "unfavorable. If the count is 4, the planet is neutral. We can use this "
    "analysis in natal charts and also transit charts.")

#: §12.3 names the count "rekhas", which is footnote 42's benefic term. The
#: two passages agree, so nothing here rests on our reading of the footnote
#: alone.
BAV_COUNT_IS_CALLED_REKHAS = (
    "It is called the number of rekhas (benefic points) in that rasi.")

BAV_COUNT_RANGE: tuple[int, int] = (0, 8)

#: The grade for each possible count, exactly as §12.3 partitions them.
BAV_FAVOURABLE_COUNTS: tuple[int, ...] = (5, 6, 7, 8)
BAV_NEUTRAL_COUNTS: tuple[int, ...] = (4,)
BAV_UNFAVOURABLE_COUNTS: tuple[int, ...] = (0, 1, 2, 3)

BAV_GRADES: dict[int, str] = {
    **{count: "unfavorable" for count in BAV_UNFAVOURABLE_COUNTS},
    **{count: "neutral" for count in BAV_NEUTRAL_COUNTS},
    **{count: "favorable" for count in BAV_FAVOURABLE_COUNTS},
}

#: The book's own spelling. Kept rather than anglicised to "favourable".
BAV_GRADE_NAMES: tuple[str, ...] = ("favorable", "neutral", "unfavorable")

BAV_APPLIES_TO_TRANSITS = (
    "We can use this analysis in natal charts and also transit charts.")

AV_ABBREVIATIONS: dict[str, str] = {
    "AV": "ashtakavarga",
    "BAV": "Bhinna Ashtakavarga",
}


# --------------------------------------------------------------------------
# §12.3's Example 38 and Chart 11
# --------------------------------------------------------------------------

EXAMPLE_38_WORKING = (
    "Let us go further with Exercise 18 now. After finding the rasis in which "
    "Mercury is benefic with respect to various references, let us count the "
    "references with respect to which Mercury is benefic in each rasi. From "
    "the answer to Exercise 18, we see that Mercury is benefic in Ar with "
    "respect to Sun, Moon, Mars, Mercury, Venus, Saturn and lagna. In other "
    "words, Mercury is benefic in Ar with respect to 7 references. So we "
    "write 7 in Ar. We see that Mercury is benefic in Ta with respect to Sun, "
    "Mercury, Venus and Saturn. In other words, Mercury is benefic in Ta with "
    "respect to 4 references. So we write 4 in Ta. We find the count of "
    "references for each rasi and prepare a chart. This is called Mercury's "
    "BAV or simply Mercury's AV. Readers may complete the calculations and "
    "verify with Chart 11.")

EXAMPLE_38_READING = (
    "In Ar and Ge, we have 7 rekhas. So Mercury is benefic in those rasis "
    "with respect to 7 references out of 8. In Aq, we have 6 rekhas. So these "
    "three rasis are particularly favorable for Mercury. In Vi and Cp, we "
    "have 3 rekhas and that is the lowest. So Mercury is particularly "
    "unfavorable in Vi and Cp.")

EXAMPLE_38_NATAL = (
    "Here Mercury is in Ge in the natal chart and Ge has 7 rekhas in "
    "Mercury's AV. That means that Mercury is a very favorable planet. Being "
    "the lagna lord and being in a quadrant from lagna in own sign (i.e. "
    "Bhadra yoga) makes him even stronger. Because of this, Mercury is "
    "extremely favorable in this chart.")

#: Chart 11: Mercury's BAV drawn as a chart, read sign by sign from the
#: south-Indian diagram. Aries first.
CHART_11_MERCURY_BAV: tuple[int, ...] = (7, 4, 7, 4, 4, 3, 4, 4, 4, 3, 6, 4)

#: The rasis §12.3's Example 38 singles out.
EXAMPLE_38_BEST_RASIS: tuple[str, ...] = ("Ar", "Ge", "Aq")
EXAMPLE_38_WORST_RASIS: tuple[str, ...] = ("Vi", "Cp")


EXERCISE_19 = (
    "Find the number of rekhas in all the rasis in the BAVs of Sun, Moon, "
    "Mars, Mercury, Jupiter, Venus and Saturn for the same rasi chart (see "
    "Chart 6).")

EXERCISE_19_CLOSING = (
    "Using the above values, one can prepare a chart for each planet's BAV, "
    "as shown in Chart 11.")

#: The printed answer, Aries first. Seven rows of twelve — every planetary
#: table exercised through one chart.
EXERCISE_19_ANSWER: dict[str, tuple[int, ...]] = {
    "Sun":     (5, 3, 5, 3, 4, 4, 2, 3, 5, 4, 5, 5),
    "Moon":    (3, 2, 5, 3, 6, 3, 4, 5, 5, 5, 3, 5),
    "Mars":    (4, 3, 4, 3, 4, 3, 2, 5, 1, 3, 3, 4),
    "Mercury": (7, 4, 7, 4, 4, 3, 4, 4, 4, 3, 6, 4),
    "Jupiter": (4, 3, 5, 6, 3, 7, 4, 3, 5, 6, 5, 5),
    "Venus":   (8, 7, 4, 3, 3, 2, 4, 6, 4, 4, 4, 3),
    "Saturn":  (3, 3, 4, 3, 2, 3, 2, 3, 4, 5, 3, 4),
}

#: The answer prints "5*" for the Moon in Pisces. Nothing on the page
#: explains the asterisk. It is not the planet's own position marked
#: generally — Venus in Aries and Mercury in Gemini carry none — and the
#: value 5 is right either way. Recorded, not interpreted.
EXERCISE_19_UNEXPLAINED_MARK = {
    "owner": "Moon", "rasi": "Pi", "printed": "5*", "value": 5,
}


# --------------------------------------------------------------------------
# 12.4 Samudaaya Ashtakavarga
# --------------------------------------------------------------------------

SAMUDAAYA_MEANS = "group"
SARVA_MEANS = "all"

SAV_DEFINITION = (
    "Samudaaya means “group”. Samudaaya Ashtakavarga is nothing but the sum "
    "of the ashtakavargas of seven planets. In each rasi, we add the number "
    "of rekhas in the BAVs of Sun, Moon, Mars, Mercury, Jupiter, Venus and "
    "Saturn. The sum denotes the number of rekhas in that rasi in Samudaaya "
    "Ashtakavarga. It will be denoted with SAV. It is also called “Sarva "
    "Ashtakavarga” (sarva = all).")

#: The sentence that settles it: seven planets, and lagna is not among them.
SAV_IS_SEVEN_PLANETS = (
    "Samudaaya Ashtakavarga is nothing but the sum of the ashtakavargas of "
    "seven planets.")

SAV_OWNERS: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

SAV_TOTAL = 337

SAV_WORKED_EXAMPLE = (
    "Let us continue with the rasi chart in Chart 6. From the answer to "
    "Exercise 19, we see that the BAVs of Sun, Moon, Mars, Mercury, Jupiter, "
    "Venus and Saturn have 5, 3, 4, 7, 4, 8 and 3 rekhas in Ar "
    "(respectively). Adding them all, we get 34. So SAV has 34 rekhas in Ar "
    "and we write 34 in Ar.")

SAV_STRENGTH_RULE = (
    "A rasi with 30 or more rekhas becomes strong. Matters signified by the "
    "house falling in such a rasi flourish and planets transiting in such a "
    "rasi bring good results. A rasi with 25-30 rekhas is average. A rasi "
    "with less than 25 rekhas becomes weak. Matters signified by the house "
    "falling in such a rasi suffer and planets transiting in such a rasi "
    "bring bad results.")

#: §12.4's two ranges overlap at 30 — "30 or more becomes strong" and
#: "25-30 rekhas is average". Thirty is read as strong: that clause is
#: unambiguous and stated first, and the muhurta rule below repeats "30 or
#: more ... are favorable". See docs/book-deviations.md D-40.
SAV_STRONG_FROM = 30
SAV_AVERAGE_FROM = 25
SAV_OVERLAP_AT = 30

SAV_GRADE_NAMES: tuple[str, ...] = ("strong", "average", "weak")

SAV_MUHURTA_RULE = (
    "When choosing muhurtas for auspicious activities like a wedding or "
    "housewarming, one should look at the strengths, as per SAV of the natal "
    "chart, of the rasis containing lagna, Moon and Sun in the muhurta "
    "chart. Rasis containing 30 or more rekhas in SAV are favorable.")

#: The three positions in the muhurta chart §12.4 says to check.
SAV_MUHURTA_POSITIONS: tuple[str, ...] = ("Lagna", "Moon", "Sun")

#: Footnote 43, supplied with §12.5.
MUHURTA_FOOTNOTE = "43"

EXERCISE_20 = (
    "Find the number of rekhas in all the rasis in SAV for the same rasi "
    "chart (see Chart 6).")

#: The printed answer, Aries first.
EXERCISE_20_ANSWER: tuple[int, ...] = (
    34, 25, 34, 25, 26, 25, 22, 29, 28, 30, 29, 30)

EXERCISE_20_CLOSING = (
    "Using the above values, one can prepare a chart for SAV, as shown in "
    "Chart 11.")


# --------------------------------------------------------------------------
# 12.5 Divisional Charts
# --------------------------------------------------------------------------

AV_NOT_ONLY_RASI = (
    "There is a misconception that ashtakavarga is applicable only to rasi "
    "charts. Parasara does not say it. Parasara lists the divisional charts "
    "in which different areas of life are seen, at the very beginning of "
    "BPHS. So all the analysis in the rest of his classic applies to all the "
    "divisional charts, unless Parasara explicitly mentions rasi chart. For "
    "example, Parasara says that D-12 shows matters related to father. So any "
    "principles based on ashtakavarga and sodhya pindas that let us predict "
    "matters related to father must use D-12. This is a logical deduction and "
    "Parasara does not have to mention it explicitly each time.")

AV_IN_DIVISIONAL_CHARTS = (
    "If we can judge the benefic positions of various planets with respect to "
    "8 references in rasi chart, there is no reason why we should not do it "
    "in all the divisional charts. In fact, this becomes invaluable when we "
    "interpret transits in rasi chart with respect to the natal positions in "
    "divisional charts and transits in divisional charts with respect to the "
    "natal positions in rasi chart.")

#: The sentence that says the eight tables do not change from chart to chart.
AV_TABLES_ARE_THE_SAME = (
    "Ashtakavarga of divisional charts is prepared in the same manner as that "
    "of rasi chart. The benefic houses for each planet with respect to the 8 "
    "references are the same. We can apply the same rules and find the BAVs "
    "of all planets. In fact, we can find SAV of a divisional chart too.")

#: §12.5's worked illustration of the deduction.
AV_DIVISIONAL_EXAMPLE = {
    "chart": "D12",
    "matter": "matters related to father",
    "why": ("Parasara says that D-12 shows matters related to father, so any "
            "principles based on ashtakavarga and sodhya pindas that let us "
            "predict matters related to father must use D-12."),
}

#: Footnote 43, supplied with §12.5.
MUHURTA_DEFINITION = (
    "Muhurta is an auspicious pre-set time at which one begins important "
    "activities.")

#: §12.5 names "sodhya pindas" alongside ashtakavarga. Nothing read so far
#: defines them. See docs/open-items.md OI-101.
SODHYA_PINDA_NOT_YET_DEFINED = (
    "Section 12.5 names sodhya pindas beside ashtakavarga as a second family "
    "of principles. No section read so far defines them.")


# --------------------------------------------------------------------------
# §12.5's Example 39 — Vajpayee's rasi and D-10 SAVs
# --------------------------------------------------------------------------

EXAMPLE_39 = (
    "Let us consider the rasi chart and D-10 of India's Prime Minister Sri "
    "A.B. Vajpayee (see Chart 3 for birthdata). Readers may find SAV of rasi "
    "and D-10 and verify the following:")

#: The printed answers, Aries first.
EXAMPLE_39_RASI_SAV: tuple[int, ...] = (
    29, 22, 27, 29, 28, 38, 29, 26, 23, 34, 28, 24)
EXAMPLE_39_D10_SAV: tuple[int, ...] = (
    23, 26, 33, 20, 28, 33, 26, 35, 28, 31, 24, 30)

EXAMPLE_39_READING = (
    "In rasi chart, the 11th house has the maximum number of rekhas (38) "
    "showing excellent gains. The 3rd house of communication has 34 rekhas. "
    "With the significator of communication Mercury and the artistic Moon in "
    "the 3rd house, he is an excellent communicator, great orator and poet. "
    "With lagna and the 10th house in the SAV of rasi chart containing only "
    "26 and 28 rekhas – which is just average – why did he have such a "
    "successful career?")

EXAMPLE_39_ANSWER = (
    "The answer lies in the SAV of D-10. Lagna in D-10 is Sc and it contains "
    "35 rekhas – maximum in D-10's SAV. Arudha lagna also contains more than "
    "30 rekhas. These factors explain his success and good name. The 3rd "
    "house in D-10 also has more than 30 rekhas – like in the rasi chart – "
    "and that increases the chance of being an excellent communicator in "
    "public life. Though D-10 is powerful with lagna and arudha lagna "
    "containing more than 30 rekhas, one may notice that the 8th house in "
    "D-10 (Ge) has 33 rekhas in D-10's SAV. This explains the struggle in "
    "Vajpayee's career.")

#: The example never states the lagna, but every claim it makes fixes it:
#: the rasi maximum 38 is said to be the 11th, and the D-10 maximum 35 the
#: lagna. Both give Scorpio.
EXAMPLE_39_LAGNA = "Sc"

#: Chart 3 holds Vajpayee's birth data and has not been supplied, so the two
#: SAVs cannot be recomputed. See docs/open-items.md OI-102.
EXAMPLE_39_NEEDS_CHART_3 = (
    "Example 39 cites Chart 3 for Sri A.B. Vajpayee's birth data. Chart 3 has "
    "not been supplied, so the two printed SAVs are transcribed and checked "
    "for internal consistency, but not recomputed.")

# --------------------------------------------------------------------------
# Chart 12 — the D-10 SAV exercise chart
# --------------------------------------------------------------------------

#: Chart 12's printed rasi longitudes. Its drawn diagram is the **D-10**, not
#: the rasi chart, which is what makes it a check on the varga as well as on
#: the transcription.
CHART_12: dict[str, str] = {
    "Asc": "3 Le 29", "Sun": "29 Cn 47", "Moon": "17 Le 39",
    "Mars": "22 Ar 05", "Merc": "12 Le 23", "Jup": "3 Li 06",
    "Ven": "7 Cn 13", "Sat": "25 Sc 51", "Rahu": "2 Li 03",
    "Ketu": "2 Ar 03", "HL": "11 Le 38", "GL": "29 Le 25",
}

CHART_12_TITLE = "D-10 SAV Exercise"
CHART_12_BIRTH = "August 16, 1958, 7:05 am (4:00 West), 83 W 53, 43 N 36"

#: The drawn D-10, read box by box.
CHART_12_D10_DRAWN: dict[str, str] = {
    "Sat": "Pi", "Ketu": "Ar", "Ven": "Ta", "GL": "Ta", "Moon": "Cp",
    "Merc": "Sg", "Sun": "Sg", "Jup": "Sc", "Mars": "Sc", "HL": "Sc",
    "Rahu": "Li", "Asc": "Vi",
}

CHART_12_CHARA_KARAKAS: dict[str, str] = {
    "Sun": "AK", "Rahu": "AmK", "Sat": "BK", "Mars": "MK",
    "Merc": "PK", "Ven": "GK", "Jup": "DK", "Moon": "PiK",
}
