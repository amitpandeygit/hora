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
SODHYA_PINDA_WHERE_DEFINED = (
    "Section 12.5 names sodhya pindas beside ashtakavarga as a second family "
    "of principles without defining them. Section 12.7 defines the whole "
    "pipeline — BAV, then Trikona Sodhana (12.7.1), then Ekaadhipatya "
    "Sodhana (12.7.2), giving a Sodhita Ashtakavarga, then the pinda "
    "(12.7.3). It is served at /v1/sodhana/pinda, which runs all four steps "
    "and returns every intermediate.")


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

#: Chart 3 holds Vajpayee's birth data. It was supplied, and both printed SAVs
#: recompute from it exactly — all 24 figures. OI-102 is closed; see
#: docs/closed-items.md.
EXAMPLE_39_VERIFIED = (
    "Example 39 cites Chart 3 for Sri A.B. Vajpayee's birth data. Both printed "
    "SAVs — rasi and D-10 — recompute from Chart 3's longitudes exactly, and "
    "every claim the example makes about them holds.")

#: The example's D-10 claims, each with the figure that decides it. The lagna
#: and arudha lagna signs are derived, not printed, so they are recorded here
#: as what the text's wording resolves to.
EXAMPLE_39_D10_CLAIMS: tuple[tuple[str, str, int], ...] = (
    ("Lagna in D-10 is Sc and it contains 35 rekhas", "Sc", 35),
    ("Arudha lagna also contains more than 30 rekhas", "Vi", 33),
    ("The 3rd house in D-10 also has more than 30 rekhas", "Cp", 31),
)

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


# --------------------------------------------------------------------------
# Chart 3 — Sri A.B. Vajpayee, the birth data Example 39 cites
# --------------------------------------------------------------------------

#: Chart 3's printed longitudes. Example 39 works from this chart without
#: reprinting it, so both of its SAVs are recomputed from here.
CHART_3: dict[str, str] = {
    "Asc": "14 Sc 18", "Sun": "9 Sg 35", "Moon": "15 Le 28",
    "Mars": "13 Ar 39", "Merc": "20 Sc 59", "Jup": "2 Aq 05",
    "Ven": "17 Sg 42", "Sat": "9 Sc 41", "Rahu": "14 Ge 30",
    "Ketu": "14 Sg 30", "HL": "13 Li 46", "GL": "21 Cn 25",
}

CHART_3_TITLE = "Rasi — A.B. Vajpayee"
CHART_3_BIRTH = "December 25, 1926, 5:12 am (IST), 78 E 10, 26 N 14"

#: The drawn rasi diagram, read box by box. It prints AL, which the printed
#: longitudes do not — so it is an independent check on §9.2's procedure.
CHART_3_DRAWN: dict[str, str] = {
    "Mars": "Ar", "Rahu": "Ge", "GL": "Cn", "Moon": "Le", "HL": "Li",
    "Merc": "Sc", "Asc": "Sc", "Sat": "Sc",
    "Ven": "Sg", "Sun": "Sg", "Ketu": "Sg", "AL": "Cp", "Jup": "Aq",
}

CHART_3_CHARA_KARAKAS: dict[str, str] = {
    "Merc": "AK", "Ven": "AmK", "Rahu": "BK", "Moon": "MK",
    "Mars": "PiK", "Sat": "PK", "Sun": "GK", "Jup": "DK",
}


# --------------------------------------------------------------------------
# Exercise 21 — the D-10 SAV of Chart 12, and what it says about her career
# --------------------------------------------------------------------------

EXERCISE_21 = (
    "Consider the D-10 chart of a lady, shown in Chart 12. Compute the SAV of "
    "this D-10. Suppose we are told that she has an unsuccessful career as a "
    "waiter in a small restaurant. Based on D-10's SAV, does it make sense? "
    "If not, guess her career.")

EXERCISE_21_HINT = (
    "Look at the number of rekhas in lagna and the 10th house.")

#: The printed answer, Aries first. We computed it before the answer was
#: supplied and it matched digit for digit.
EXERCISE_21_ANSWER: tuple[int, ...] = (
    24, 25, 31, 28, 27, 39, 33, 29, 26, 22, 28, 25)

#: The two figures the hint sends the reader to, from a Virgo D-10 lagna.
EXERCISE_21_LAGNA = "Vi"
EXERCISE_21_LAGNA_REKHAS = 39
EXERCISE_21_TENTH = "Ge"
EXERCISE_21_TENTH_REKHAS = 31

EXERCISE_21_VERDICT = (
    "Lagna is in Vi in Chart 12. Vi it has 39 rekhas. That's a lot more than "
    "30! The 10th house (Ge) also has more than 30 rekhas. So this D-10 is "
    "very powerful and it possibly cannot belong to an unsuccessful waiter at "
    "a small restaurant. This has to be someone pretty successful.")

EXERCISE_21_GUESS = (
    "Apart from the 1st and 10th houses, the 2nd house is strong in D-10's "
    "SAV, with 33 rekhas. This shows the importance of speech and voice in "
    "her career. Ghati lagna is in Taurus and its lord Venus occupies it. "
    "This makes ghati lagna and 9th house very powerful. This shows a "
    "fortunate (9th) and famous (GL) entertainer (Venus). Saturn's 11th house "
    "argala on GL suggests popular mass support as a catalyst in her success. "
    "Rahu's unobstructed 2nd house argala on lagna shows unconventional "
    "behavior in public life.")

EXERCISE_21_FINAL_ANSWER = (
    "The chart belongs to Madonna, a pop diva of USA.")

#: Every checkable step of the guess, as ``(claim, what decides it)``. The
#: identification itself is not derivable and is not claimed to be — the
#: chain stops at "famous entertainer", and the name is the book's knowledge.
EXERCISE_21_GUESS_STEPS: tuple[tuple[str, str], ...] = (
    ("the 2nd house is strong in D-10's SAV, with 33 rekhas",
     "2nd from Vi is Li, which holds 33"),
    ("Ghati lagna is in Taurus",
     "GL's D-10 sign, as Chart 12's diagram draws it"),
    ("its lord Venus occupies it",
     "Venus owns Taurus and sits in it in the D-10"),
    ("This makes ghati lagna and 9th house very powerful",
     "9th from the Vi lagna is Ta, so GL sits in the 9th house"),
    ("Saturn's 11th house argala on GL",
     "11th from Ta is Pi, where Saturn is"),
    ("Rahu's unobstructed 2nd house argala on lagna",
     "2nd from Vi is Li, where Rahu is; the 12th, Le, is empty"),
)

#: Footnote 47 hangs off the last sentence of the guess and has not been
#: supplied. Nothing in the reading depends on it.
EXERCISE_21_FOOTNOTE_47_UNSEEN = (
    "Footnote 47 is cited after 'unconventional behavior in public life' and "
    "has not been supplied.")


# --------------------------------------------------------------------------
# §12.6 — Prastaara Ashtakavarga
# --------------------------------------------------------------------------

PRASTAARA_WHY = (
    "Using the Bhinna Ashtakavarga (BAV) of a planet, we can find out the "
    "rasis in which it is benefic with respect to more references and the "
    "rasis in which it is malefic with respect to more references. To "
    "interpret transits, this is sometimes not enough. For example, if we "
    "know that a planet is benefic in Ta with respect to 5 references, that "
    "may not be enough. We may need to know exactly what those 5 references "
    "are. If we are looking for Jupiter's transit that brings marriage, for "
    "example, we may want Jupiter to be benefic in his transit rasi with "
    "respect to certain planets (Venus or DK or 7th lord in navamsa, for "
    "example). In such situations, we need to know exactly which references a "
    "planet is benefic from.")

PRASTAARA_MEANS = "spread-out"

PRASTAARA_DEFINITION = (
    "For this purpose, we prepare “Prastaara Astakavarga”. It will be "
    "denoted with PAV. Prastaara means “spread-out”. PAV is a "
    "spreadsheet that shows the exact references from which a planet is "
    "benefic in a rasi. We prepare one PAV for each planet. Different people "
    "may represent PAV differently. Some people may cast a chart and write "
    "the list of benefic references in each rasi. For some people, the answer "
    "to Exercise 18 may qualify as Mercury's PAV. Some people may prefer to "
    "represent the same information as shown in Table 27.")

PRASTAARA_PURPOSE = (
    "The basic purpose of a planet's PAV is to show the references with "
    "respect to which the planet is benefic in each rasi.")

#: §12.6's closing note, and the invariant it states.
PRASTAARA_COLUMN_NOTE = (
    "From PAV, we can construct BAV easily. From Table 27, we may note that "
    "the sum of all the entries in each column – rasi – in a PAV "
    "gives the number of rekhas in that rasi in BAV. This is shown in the "
    "last row.")

#: The book's own note that Exercise 18's answer already *is* a PAV, in a
#: different representation. Our code holds both and they are checked against
#: each other rather than typed twice.
PRASTAARA_REPRESENTATIONS = (
    "a chart with the benefic references written into each rasi",
    "the answer to Exercise 18 — one list of rasis per reference",
    "Table 27's grid — one row per reference, one column per rasi",
)

#: Table 27, Mercury's PAV for Exercise 18, row-wise in the printed
#: orientation: reference -> 0/1 for Ar..Pi. Chart 6 is the chart.
TABLE_27_MERCURY_PAV: dict[str, tuple[int, ...]] = {
    #             Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi
    "Sun":       (1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0),
    "Moon":      (1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0),
    "Mars":      (1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1),
    "Mercury":   (1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1),
    "Jupiter":   (0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1),
    "Venus":     (1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0),
    "Saturn":    (1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1),
    "Lagna":     (1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0),
}

#: Table 27's printed last row. It must equal the column sums *and* Mercury's
#: BAV in Chart 6 — the note above says so, and both are checked.
TABLE_27_TOTALS: tuple[int, ...] = (7, 4, 7, 4, 4, 3, 4, 4, 4, 3, 6, 4)

TABLE_27_OWNER = "Mercury"
TABLE_27_CHART = "Chart 6"

#: The transit question §12.6 exists to answer, kept as the book phrases it so
#: the endpoint's shape can be justified against it.
PRASTAARA_TRANSIT_EXAMPLE = (
    "If we are looking for Jupiter's transit that brings marriage, for "
    "example, we may want Jupiter to be benefic in his transit rasi with "
    "respect to certain planets (Venus or DK or 7th lord in navamsa, for "
    "example).")

#: §12.6 names three candidate references for that example. Only the first is
#: an ashtakavarga reference; the other two are ways of *choosing* which
#: reference to ask about, and they resolve to a graha before PAV sees them.
PRASTAARA_TRANSIT_REFERENCES = ("Venus", "DK", "7th lord in navamsa")


# --------------------------------------------------------------------------
# §12.7 — Sodhya Pindas
# --------------------------------------------------------------------------

SODHYA_PINDAS_INTRO = (
    "We discussed the computation of BAV before. By applying some reductions "
    "on the values in BAV, we get “Sodhita Ashtakavarga” (SoAV). Using "
    "it, we find Sodhya Pindas of different planets. These pindas are very "
    "important in predicting key events and we will talk about them again in "
    "the part “Transit Analysis”.")

SOAV_MEANS = "Sodhita Ashtakavarga"
SOAV_IS_A_REDUCED_BAV = (
    "A SoAV is a BAV with reductions applied. The pindas are computed from "
    "the SoAV, not from the BAV.")

# -- §12.7.1 Trikona Sodhana ------------------------------------------------

TRIKONA_SODHANA_MEANS = "Trinal Reduction"

TRIKONA_SODHANA_RULE = (
    "Consider the BAV of a planet. Look at different sets of mutual trines "
    "separately (e.g. First set: Ar, Le and Sg, Second set: Ta, Vi and Cp) "
    "and apply the following rules on each set:")

#: The three rules as printed. Footnote 44 says (1) and (2) are special cases
#: of (3), and `trikona_sodhana` implements only (3) for exactly that reason —
#: `test_rules_one_and_two_fall_out_of_rule_three` proves it over all 729
#: possible triples.
TRIKONA_SODHANA_RULES: tuple[str, ...] = (
    "If atleast one rasi has zero, no reduction is necessary.",
    "If the three rasis have the same value, make them all zero.",
    "Take the lowest value out of the three. Subtract it from all the values.",
)

#: Footnote 44 — PVR rejecting a rival reading of rule (1). See
#: docs/precedence.md PVR-15.
TRIKONA_SODHANA_FOOTNOTE_44 = (
    "Some authors suggest that this applies only if there is zero in exactly "
    "one rasi. If two rasis have a zero, they suggest making the third one "
    "also zero. But this is inconsistent with the spirit of the other rules. "
    "The idea is to subtract the lowest value from others. In that sense, (1) "
    "and (2) are special cases cases of (3). The change suggested by these "
    "authors is inconsistent with this. Let us follow Parasara.")

#: The rejected reading differs from Parasara's on exactly the triples with
#: two zeros and a non-zero third — 24 of the 729 possible, enumerated by
#: `test_footnote_44s_dispute_is_confined_to_two_zero_triples`.
TRIKONA_SODHANA_DISPUTED_CASE = (
    "two rasis at zero and the third above zero")

#: What Example 40 calls each trine set. §2.2.5's element names are nouns
#: ("fire"); the example uses the adjective ("fiery trines").
TRINE_SET_NAMES: dict[str, str] = {
    "fire": "fiery", "earth": "earthy", "air": "airy", "water": "watery",
}

EXAMPLE_40 = (
    "As an example, let us take Mercury's BAV given in Chart 11. Let us takes "
    "fiery trines. Ar, Le and Sg have 7, 4 and 4 rekhas. Rules (1) and (2) "
    "don't apply and we go to (3). The lowest value is 4. Subtracting it from "
    "the three values, we write 3, 0 and 0 in Ar, Le and Sg respectively. Let "
    "us take the watery trines now. Cn, Sc and Pi have 4 rekhas each. Rule "
    "(2) applies and we write zero in all the three rasis. Readers may carry "
    "out the reduction for the remaining two sets of trines and verify that "
    "we get the following table after Trikona Sodhana:")

EXAMPLE_40_OWNER = "Mercury"
EXAMPLE_40_CHART = "Chart 11"

#: The printed answer, Aries first.
EXAMPLE_40_ANSWER: tuple[int, ...] = (3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0)

#: The two trine sets the example works longhand, and which rule it names.
#: The other two it leaves to the reader; our tests do all four.
EXAMPLE_40_WORKED: tuple[tuple[str, tuple[str, ...], tuple[int, ...],
                              tuple[int, ...], int], ...] = (
    ("fiery", ("Ar", "Le", "Sg"), (7, 4, 4), (3, 0, 0), 3),
    ("watery", ("Cn", "Sc", "Pi"), (4, 4, 4), (0, 0, 0), 2),
)


# -- §12.7.2 Ekaadhipatya Sodhana ------------------------------------------

EKAADHIPATYA_SODHANA_MEANS = "Co-owned Reduction"

EKAADHIPATYA_SODHANA_RULE = (
    "After we carry out Trikona Sodhana, we carry out another reduction on "
    "the pairs of signs that are owned by the same planet. Ar and Sc are "
    "owned by Mars; Ta and Li are owned by Venus; Ge and Vi are owned by "
    "Mercury; Sg and Pi are owned by Jupiter; and, Cp and Aq are owned by "
    "Saturn. We apply a reduction on these pairs of rasis separately, using "
    "the following rules:")

#: The four rules as printed, with (3) and (4) carrying their two branches.
EKAADHIPATYA_SODHANA_RULES: tuple[tuple[str, str], ...] = (
    ("1", ("If atleast one of the rasis has a zero in it, no reduction is "
           "necessary and stop here.")),
    ("2", ("If both the rasis are occupied by a planet (or planets), again no "
           "reduction is necessary and stop here.")),
    ("3", ("If one rasi is occupied by a planet (or planets) and the other is "
           "empty, then do the following:")),
    ("3a", ("If the empty rasi has a lower value, replace the value with a "
            "zero.")),
    ("3b", ("If the empty rasi has a higher value, replace the value with the "
            "value in the other rasi.")),
    ("4", "If both the rasis are empty, then do the following:"),
    ("4a", "If both the rasis have the same value, replace both with zero."),
    ("4b", ("If they have different values, replace the higher value with the "
            "lower value.")),
)

#: Cancer and Leo have one owner each, so they are in no pair and §12.7.2
#: never touches them. The book's list of five pairs says so by omission.
EKAADHIPATYA_UNPAIRED = ("Cn", "Le")

#: **Gap.** Rule (3a) fires when the empty rasi is *lower*, (3b) when it is
#: *higher*. Neither covers equal, which is reachable after Trikona Sodhana.
#: See docs/book-deviations.md D-41.
EKAADHIPATYA_TIE_IS_UNCOVERED = (
    "Rule (3) splits on whether the empty rasi's value is lower or higher "
    "than the occupied one's. It does not say what to do when they are "
    "equal, and equal values survive Trikona Sodhana routinely.")

#: The reading we implement, and why. Not confirmed — see D-41.
EKAADHIPATYA_TIE_READING = (
    "We read equal as (3a) and write zero. The book zeroes ties everywhere "
    "else it faces one: rule (4a) here zeroes two empty rasis holding the "
    "same value, and section 12.7.1's rule (2) zeroes three trines holding "
    "the same value. Reading equal as (3b) instead would leave the value "
    "standing, which is the only place in either reduction where a tie "
    "survives.")

#: **Gap.** "Occupied by a planet (or planets)" — Example 42 names only Mars,
#: Jupiter and Saturn. Whether Rahu and Ketu occupy a rasi for this purpose is
#: not stated. See docs/open-items.md OI-104.
EKAADHIPATYA_OCCUPANCY_UNDEFINED = (
    "Section 12.7.2 says 'occupied by a planet (or planets)' without saying "
    "whether Rahu and Ketu count. Example 42's occupants are Mars, Jupiter "
    "and Saturn only, so it does not settle the question. Our API makes the "
    "caller state which rasis are occupied rather than choosing for them.")


EXAMPLE_41 = (
    "Let us continue with Example 40. Let us take Ar and Sc. Sc has zero in "
    "it and (1) applies. So there is no reduction. In fact, (1) applies to "
    "all pairs and so all the values remain unchanged after Ekaadhipatya "
    "reduction.")

#: Example 41's answer is Example 40's answer — nothing moves.
EXAMPLE_41_ANSWER: tuple[int, ...] = EXAMPLE_40_ANSWER

EXAMPLE_42 = (
    "Let us consider some other hypothetical examples to understand all the "
    "rules correctly.")

#: Example 42's five hypothetical pairs, all Ta/Li:
#: ``(label, (Ta, Li) before, occupied signs, (Ta, Li) after, rule)``.
#: Between them they exercise rules (2), (3a), (3b), (4b) and (4a) — every
#: rule except (1), which Example 41 covers.
EXAMPLE_42_CASES: tuple[tuple[str, tuple[int, int], tuple[str, ...],
                             tuple[int, int], str, str], ...] = (
    ("a", (4, 2), ("Ta", "Li"), (4, 2), "2",
     ("Ta is occupied by Mars and Li by Jupiter and Saturn. In this case, rule "
     "(2) applies and we do not alter the values.")),
    ("b", (4, 2), ("Ta",), (4, 0), "3a",
     ("Ta is occupied by Mars and Li is empty. In this case, rule (3a) applies "
     "and we write zero in Li, as Li is empty and it has a lower value than "
     "Ta.")),
    ("c", (4, 2), ("Li",), (2, 2), "3b",
     ("Ta is empty and Li is occupied by Jupiter and Saturn. In this case, "
     "rule (3b) applies and we write 2 in Ta, as Ta is empty and it has a "
     "higher value than Li.")),
    ("d", (4, 2), (), (2, 2), "4b",
     ("Ta and Li are empty. In this case, rule (4b) applies and we replace the "
     "higher value 4 with the lower value 2. So we write 2 in Ta.")),
    ("e", (2, 2), (), (0, 0), "4a",
     ("Ta and Li are empty. In this case, rule (4a) applies and we write zero "
     "in Ta and Li.")),
)

#: Example 41 covers rule (1) and Example 42 the other five branches, so
#: between them the book works every rule it states. Nothing is untested.
EKAADHIPATYA_RULES_ALL_EXERCISED = ("1", "2", "3a", "3b", "4a", "4b")


# -- §12.7.3 Sodhya Pindas --------------------------------------------------

SODHYA_PINDA_DEFINITION = (
    "After carrying out Trikona sodhana and then Ekaadhipatya sodhana on the "
    "BAV of a planet, we get the “Sodhita Ashtakavarga” of that planet. "
    "We denote Sodhita Ashtakavarga with SoAV. From it, we find “Sodhya "
    "Pinda” of each planet. This will be used in transit analysis.")

RASI_PINDA_RULE = (
    "For each rasi, we multiply the number in that rasi in SoAV with the "
    "multiplier of that rasi (shown in Table 28). We find such a product for "
    "all the 12 rasis. We find the sum of the products of all the 12 rasis "
    "and the sum is called rasi pinda.")

GRAHA_PINDA_RULE = (
    "For each planet, we multiply the number in the rasi containing that "
    "planet with the multiplier of that planet (shown in Table 29). We find "
    "such a product for all the 7 planets. We find the sum of the products of "
    "all the 7 planets and the sum is called graha pinda.")

SODHYA_PINDA_RULE = (
    "By adding rasi pinda and graha pinda, we get “Sodhya Pinda” of the "
    "planet whose SoAV we are working with.")

#: Table 28 — the rasimana multipliers, Aries first.
TABLE_28_RASIMANA: tuple[int, ...] = (7, 10, 8, 4, 10, 6, 7, 8, 9, 5, 11, 12)

#: Table 29 — the grahamana multipliers. Seven planets; lagna and the nodes
#: are not among them, and §12.7.3 says "all the 7 planets" outright.
TABLE_29_GRAHAMANA: dict[str, int] = {
    "Sun": 5, "Moon": 5, "Mars": 8, "Mercury": 5,
    "Jupiter": 10, "Venus": 7, "Saturn": 5,
}

#: A graha pinda runs over seven planets, not the eight ashtakavarga
#: references. Lagna has a multiplier in neither table.
GRAHA_PINDA_EXCLUDES_LAGNA = (
    "A graha pinda sums over the seven planets. Lagna is an ashtakavarga "
    "reference but has no multiplier in Table 29, and section 12.7.3 says "
    "'all the 7 planets'. Rahu and Ketu are absent for the same reason.")

#: Footnote 45 — the SoAV's other use, which the book states and then declines
#: to develop. Transcribed, not implemented.
SODHYA_PINDA_FOOTNOTE_45 = (
    "This chart has several purposes which will not be covered in this book. "
    "An example is Vaastu or Sthaapatya Veda or the Vedic Science of "
    "Architecture. The direction signified by the rasis containing most "
    "rekhas in the SoAV of a planet should contain the room in which the "
    "activity related to the planet takes place. For example, we should look "
    "at the SoAV of Venus to decide where bedroom should be. We should look "
    "Jupiter's SoAV to decide where money and jewels should be kept. We "
    "should look at Moon's SoAV to decide the living room (hall). Mercury is "
    "important for the study room. Sun is important for the pooja room.")

#: The five rooms footnote 45 assigns. Recorded because it is concrete; not
#: computed, because the book says the subject is out of its scope.
FOOTNOTE_45_ROOMS: dict[str, str] = {
    "Venus": "bedroom",
    "Jupiter": "where money and jewels should be kept",
    "Moon": "the living room (hall)",
    "Mercury": "the study room",
    "Sun": "the pooja room",
}

FOOTNOTE_45_NOT_IMPLEMENTED = (
    "Footnote 45 gives a complete Vaastu rule — the direction of the rasi "
    "holding the most rekhas in a planet's SoAV — but says the subject 'will "
    "not be covered in this book'. It is transcribed and its five room "
    "assignments are served, and nothing computes a direction from it.")

EXAMPLE_43 = (
    "Let us continue with Mercury's SoAV found in Example 40 and Example 41.")

#: Example 43's input is Example 41's output, which is Example 40's output.
EXAMPLE_43_SOAV: tuple[int, ...] = EXAMPLE_41_ANSWER

EXAMPLE_43_RASI_PINDA = 77
EXAMPLE_43_GRAHA_PINDA = 75
EXAMPLE_43_SODHYA_PINDA = 152

#: The products the example writes out, so the working is checked and not
#: only the total. ``(what, rekhas, multiplier, product)``.
EXAMPLE_43_RASI_PRODUCTS: tuple[tuple[str, int, int, int], ...] = (
    ("Ar", 3, 7, 21), ("Ta", 1, 10, 10), ("Ge", 3, 8, 24), ("Aq", 2, 11, 22),
)
EXAMPLE_43_GRAHA_PRODUCTS: tuple[tuple[str, str, int, int, int], ...] = (
    ("Sun", "Ge", 3, 5, 15), ("Mars", "Ge", 3, 8, 24),
    ("Mercury", "Ge", 3, 5, 15), ("Venus", "Ar", 3, 7, 21),
)


# -- Exercise 22 — the whole chapter over Chart 7 ---------------------------

EXERCISE_22 = "Find BAV, SoAV and sodhya pinda of all planets in Chart 7."

EXERCISE_22_PREAMBLE = (
    "Readers should carefully go through the examples given in this chapter "
    "and understand the calculations. This exercise covers most of the "
    "calculations defined in this chapter and it will be a good idea to "
    "attempt this exercise and verify the calculations.")

#: The printed BAVs, Aries first. Each sums to its classical total.
EXERCISE_22_BAV: dict[str, tuple[int, ...]] = {
    #          Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi
    "Sun":     (4, 2, 3, 4, 6, 5, 5, 3, 2, 6, 6, 2),
    "Moon":    (6, 3, 5, 3, 5, 5, 6, 3, 3, 4, 4, 2),
    "Mars":    (3, 2, 3, 4, 2, 5, 4, 3, 3, 4, 3, 3),
    "Mercury": (4, 6, 4, 3, 4, 7, 4, 5, 6, 3, 5, 3),
    "Jupiter": (4, 4, 3, 5, 6, 5, 6, 4, 6, 4, 3, 6),
    "Venus":   (3, 5, 5, 4, 6, 2, 3, 6, 5, 2, 7, 4),
    "Saturn":  (3, 2, 2, 3, 5, 6, 3, 4, 1, 3, 6, 1),
}

#: The printed total row, which the exercise labels SAV.
EXERCISE_22_SAV: tuple[int, ...] = (
    27, 24, 25, 26, 34, 35, 31, 28, 26, 26, 34, 21)

#: The printed SoAVs — after Trikona and then Ekaadhipatya Sodhana.
EXERCISE_22_SOAV: dict[str, tuple[int, ...]] = {
    "Sun":     (2, 0, 0, 2, 4, 3, 2, 1, 0, 4, 3, 0),
    "Moon":    (3, 0, 1, 1, 2, 1, 2, 1, 0, 1, 0, 0),
    "Mars":    (1, 0, 0, 1, 0, 3, 1, 0, 1, 2, 0, 0),
    "Mercury": (0, 3, 0, 0, 0, 4, 0, 2, 2, 0, 1, 0),
    "Jupiter": (0, 0, 0, 1, 2, 1, 3, 0, 2, 0, 0, 0),
    "Venus":   (0, 3, 2, 0, 3, 0, 0, 2, 2, 0, 4, 0),
    "Saturn":  (2, 0, 0, 2, 4, 4, 1, 3, 0, 1, 4, 0),
}

#: The printed pindas: ``(rasi, graha, sodhya)``.
EXERCISE_22_PINDAS: dict[str, tuple[int, int, int]] = {
    "Sun": (152, 81, 233), "Moon": (85, 55, 140), "Mars": (52, 43, 95),
    "Mercury": (95, 33, 128), "Jupiter": (68, 56, 124),
    "Venus": (154, 54, 208), "Saturn": (162, 63, 225),
}

#: **Exercise 22 answers half of OI-104.** The printed SoAVs only reproduce if
#: the lagna's rasi counts as occupied, though §12.7.2 says "occupied by a
#: **planet** (or planets)". Scorpio holds Chart 7's lagna and nothing else,
#: and it is one of Mars's pair, so the Ar/Sc pair decides it — three times.
EKAADHIPATYA_LAGNA_OCCUPIES = (
    "Exercise 22 settles it for lagna: its printed SoAVs for the Sun, Moon "
    "and Saturn reproduce only when the lagna's rasi counts as occupied. "
    "Chart 7's Scorpio holds the lagna alone, and it pairs with Aries, so the "
    "Ar/Sc pair decides all three — twice through rule (3a) and once through "
    "(3b), so it is not an artefact of one branch. Rahu and Ketu are still "
    "undecided: they sit in Aries and Libra, which already hold planets.")

#: **Book defect.** Table 28 prints 6 for Virgo; Exercise 22's own seven rasi
#: pindas each require 5. See docs/book-deviations.md D-42.
TABLE_28_VIRGO_CONFLICT = (
    "Table 28 gives Virgo a multiplier of 6. Every one of Exercise 22's seven "
    "printed rasi pindas comes out exactly one Virgo-rekha too high with 6, "
    "and exactly right with 5 — seven independent equations in one unknown, "
    "fitting without residue. Example 43 cannot arbitrate: its SoAV holds "
    "zero in Virgo. We use the table as printed and record the conflict.")

#: What the seven rasi pindas would be with the table as printed, for
#: comparison against the printed answers.
EXERCISE_22_RASI_PINDAS_AS_TABLE_28_PRINTS: dict[str, int] = {
    "Sun": 155, "Moon": 86, "Mars": 55, "Mercury": 99,
    "Jupiter": 69, "Venus": 154, "Saturn": 166,
}

#: Footnote 47, cited back in Exercise 21 and printed here.
FOOTNOTE_47 = (
    "Argalas on lagna show decisive influences on one's nature and argalas on "
    "GL show decisive influences on one's fame.")


# --------------------------------------------------------------------------
# §12.8 — Controversies
# --------------------------------------------------------------------------

CONTROVERSY_NAMING = (
    "With some authors using the term bindu (dot) to denote a benefic house "
    "and the term rekha (line) to denote a malefic house – which is the "
    "opposite of what we learnt in this chapter – readers may be confused "
    "when reading other books. So they should keep in mind that there are "
    "different conventions in vogue. We are following Parasara's conventions "
    "in this book.")

CONTROVERSY_NAMING_IS_MINOR = (
    "The above is merely a problem of different naming conventions. It is not "
    "a serious issue at all. It is just a matter of getting used to different "
    "nomenclature.")

#: §12.8 restates footnote 42's naming trap in prose. Two passages, one fact —
#: so nothing rests on our reading of either alone.
NAMING_AGREES_WITH_FOOTNOTE_42 = (
    "Section 12.8 and footnote 42 state the same convention independently: in "
    "this book a rekha (line) is benefic and a bindu (dot) is malefic, which "
    "is the reverse of what some other authors use. Our tables store 1 for "
    "benefic and call the count 'rekhas', agreeing with both.")

PARASARA_VS_VARAHAMIHIRA = (
    "But there is another issue, which is far more serious. There are a few "
    "inconsistencies between the lists of benefic houses of Moon and Venus as "
    "given by Maharshi Parasara and the great astrologer Varahamihira, who is "
    "relatively modern, as he belongs to 600 AD. These inconsistencies may "
    "have arisen due to corruption of texts in time.")

#: Footnote 46 — why corruption is the likely cause.
FOOTNOTE_46 = (
    "In India, books seldom existed on paper and classics were transmitted "
    "from one generation to the other, mostly by word of mouth. People got "
    "the classics by heart and recited them to their children and students. "
    "Books were written in poetry, using nice meters, to facilitate "
    "memorization.")

PARASARA_CHECKSUM_ARGUMENT = (
    "To define a planet's ashtakavarga, Parasara first gives the count of "
    "references from which the planet is malefic in the 1st house and then he "
    "lists the references. He does the same thing for all houses. So we can "
    "crosscheck. As if this isn't enough, the Sage then lists the references "
    "from which the planet is benefic. He does it in all the houses again. "
    "Just as “checksum” values are transmitted in today's digital "
    "communication schemes to provide resilience to transmission errors, the "
    "Sage, who normally uses words sparingly, takes plenty of care to ensure "
    "that his teachings on ashtakavarga remain difficult to corrupt. To "
    "corrupt one house value in Parasara's account of ashtakavarga, one has "
    "to consciously re-write the verses in three different places in a "
    "consistent fashion. With the direct approach adopted by other authors, "
    "one can change the table just by changing one word. For example, "
    "changing “sukha” (comfort – 4th) to “suta” (son – 5th) changes one "
    "value without affecting the meter used in the verses. With Parasara's "
    "indirect approach, consistent changes in multiple places are required "
    "for a single value change. So Parasara's indirect approach is superior "
    "in corruption resistance. We will follow Parasara in this book.")

#: The three places of conflict, as data. Each entry is
#: ``(owner, reference, house, parasara, varahamihira)`` — and each conflict
#: is a *swap* within one reference, so both readings leave the table's total
#: unchanged. Our tables hold Parasara's values, which is checked.
PARASARA_VARAHAMIHIRA_CONFLICTS: tuple[
        tuple[str, str, int, int, int], ...] = (
    ("Moon", "Moon", 9, 1, 0),
    ("Moon", "Mars", 9, 0, 1),
    ("Moon", "Jupiter", 2, 1, 0),
    ("Moon", "Jupiter", 12, 0, 1),
    ("Venus", "Mars", 4, 1, 0),
    ("Venus", "Mars", 5, 0, 1),
)

#: How §12.8 groups them — three conflicts, the middle one spanning two
#: houses of the same reference.
PARASARA_VARAHAMIHIRA_CONFLICT_TEXTS: tuple[str, ...] = (
    (
        "Moon's ashtakavarga: As per Parasara, Moon is benefic in the 9th "
        "from Moon and malefic in the 9th from Mars. As per Varahamihira, "
        "Moon is malefic in the 9th from Moon and benefic in the 9th from "
        "Mars."
    ),
    (
        "Moon's ashtakavarga: As per Parasara, Moon is benefic in the 2nd "
        "from Jupiter and malefic in the 12th from Jupiter. As per "
        "Varahamihira, Moon is malefic in the 2nd from Jupiter and benefic "
        "in the 12th from Jupiter."
    ),
    (
        "Venus's ashtakavarga: As per Parasara, Venus is benefic in the 4th "
        "from Mars and malefic in the 5th from Mars. As per Varahamihira, "
        "Venus is malefic in the 4th from Mars and benefic in the 5th from "
        "Mars."
    ),
)

CONTROVERSY_UNRESOLVED = (
    "The definitions and calculations given in this chapter strictly follow "
    "Parasara for the reasons already mentioned. However, readers are welcome "
    "to experiment and draw their own conclusions. Until authentic and "
    "conclusive researches are conducted into the use of sodhya pindas in the "
    "timing of events, we cannot conclusively resolve the above controversy.")

#: Varahamihira's readings are recorded but nothing computes them: §12.8 says
#: the chapter strictly follows Parasara.
VARAHAMIHIRA_NOT_IMPLEMENTED = (
    "Varahamihira's six differing cells are recorded as data so they are not "
    "lost, and nothing computes with them. Section 12.8 says the chapter "
    "strictly follows Parasara, and PVR's own calculations are our standard.")

BHAVA_CHAKRA_CONTROVERSY = (
    "Apart from this, there is another needless controversy related to "
    "ashtakavarga. Some people prepare “bhava chakra” or “chalit chakra” "
    "using Sripathi's (or Porphyry's) house devision method and use that "
    "chart to cast ashtakavarga. If Saturn is at 3° in Vi and lagna is at 27° "
    "in Le, they are very close and these people argue that Saturn is in the "
    "1st house from lagna and not in the 2nd house. These people make a bhava "
    "chakra accordingly and use it in ashtakavarga. However, if lagna is at "
    "15° in Le, Saturn is at 3° in Vi and Jupiter is at 27° in Le, they may "
    "take Saturn to be in the 2nd house from Jupiter. They compute a bhava "
    "chakra with multi-sign houses only with respect to lagna and not with "
    "respect to all the references used in ashtakavarga. So their approach is "
    "neither here nor there.")

WHOLE_SIGN_STAND = (
    "The stand of this book is very clear – each bhava (house) with respect "
    "to one reference can only be in one rasi. Even if Saturn is at 1° in Vi "
    "and lagna is at 29° in Le, we still say that the 1st house is in Le, the "
    "2nd house is in Li and Saturn is in the 2nd house (though he is only 2° "
    "away from lagna). We do not recognize the house division methods of "
    "Porphyry and others in this book. Each rasi is a house and the 1st house "
    "is the rasi containing the reference. Readers will do well to follow "
    "Maharshi Parasara and ignore the creations and borrowings of later day "
    "Indian astrologers.")

#: **Book defect.** The stand's worked example says "the 2nd house is in Li",
#: but the 2nd from Leo is Virgo — which is where its own Saturn sits, and the
#: same sentence says Saturn is in the 2nd house. See docs/book-deviations.md
#: D-44.
WHOLE_SIGN_STAND_TYPO = (
    "Section 12.8's stand says 'the 1st house is in Le, the 2nd house is in "
    "Li and Saturn is in the 2nd house' for a Saturn at 1 Vi. The 2nd from "
    "Leo is Virgo, not Libra, and Virgo is where that Saturn is — so 'Li' is "
    "a slip for 'Vi'. Read as Vi, the sentence is self-consistent and states "
    "exactly the whole-sign rule the section is arguing for.")

#: What the stand means for us, and it is what we already do.
WHOLE_SIGN_IS_WHAT_WE_DO = (
    "Every house in this chapter is counted whole-sign from the reference, "
    "for all eight references and not only from lagna. That is what section "
    "12.8 mandates, and no house-division method is offered anywhere in the "
    "ashtakavarga code.")

#: PVR's checksum argument, made testable: Parasara encodes each house three
#: times, so benefic and malefic counts must sum to eight everywhere.
PARASARA_CHECKSUM_INVARIANT = (
    "Parasara states each house three times — the count of malefic "
    "references, the list of malefic references, and the list of benefic "
    "references. The machine-checkable residue is that benefic and malefic "
    "must account for all eight references in every house of every table: "
    "8 tables x 12 houses = 96 checks.")


# --------------------------------------------------------------------------
# §25.5.2 — Kakshyas
# --------------------------------------------------------------------------
# Chapter 25's subsection, kept here rather than with the transit rules: a
# kakshya is a division of a rasi, of the same family as the tables above, and
# this is where a reader looks for it. `transits/gochara.py` cites it.

KAKSHYA_MEANS = "orbit"

KAKSHYA_DEFINITION = (
    "Each rasi is divided into eight kakshyas of 3º 45' each. Kakshya "
    "literally means “orbit”.")

#: The rule that makes kakshyas worth computing at all — whose column of the
#: PAV to read first when a graha is transiting.
KAKSHYA_LORD_IS_THE_REFERENCE_THAT_MATTERS = (
    "When a planet is in Saturn's kakshya, its placement with respect to "
    "Saturn is the most important. When a planet is in Jupiter's kakshya, "
    "its placement with respect to Jupiter is the most important.")

KAKSHYA_ORIGIN = (
    "The first kakshya in each rasi starts from 0º in that rasi and ends at "
    "3º 45'. Saturn is the ruler of the first kakshya.")

#: Eight kakshyas to a rasi.
KAKSHYA_COUNT = 8

#: 30º / 8, in degrees. The book writes it 3º 45'.
KAKSHYA_SPAN = 3.75

#: Table 60, in the printed order: (start, end, lord). Degrees within the
#: rasi. The spans are contiguous and half-open — each row's end is the next
#: row's start, so a graha exactly on a boundary belongs to the later kakshya.
TABLE_60_KAKSHYAS: tuple[tuple[float, float, str], ...] = (
    (0.00, 3.75, "Saturn"),
    (3.75, 7.50, "Jupiter"),
    (7.50, 11.25, "Mars"),
    (11.25, 15.00, "Sun"),
    (15.00, 18.75, "Venus"),
    (18.75, 22.50, "Mercury"),
    (22.50, 26.25, "Moon"),
    (26.25, 30.00, "Lagna"),
)

#: Table 60's third column alone, first kakshya first.
KAKSHYA_LORDS: tuple[str, ...] = tuple(
    lord for _start, _end, lord in TABLE_60_KAKSHYAS)

#: **Finding.** The book prints Table 60 without saying where its order comes
#: from. It is `HORA_LORD_ORDER` — the classical sequence of decreasing
#: apparent speed, Saturn down to Moon, that §1.3.11 uses for planetary hours
#: — with Lagna, the fastest reference of all, appended. So the third column
#: is not an eighth arbitrary list to be typed from the page; it is a sequence
#: we already hold, and the test derives the column and compares.
THE_KAKSHYA_LORDS_ARE_THE_HORA_ORDER_PLUS_LAGNA = (
    "Table 60's lords run Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, "
    "Lagna. The first seven are HORA_LORD_ORDER exactly — slowest first — and "
    "Lagna, which is faster than all of them, closes the rasi.")

#: **Finding.** The kakshya order is *not* `ASHTAKAVARGA_REFERENCES`. Chapter
#: 12 numbers the eight references Sun first; Table 60 runs them Saturn first.
#: Both orders name the same eight, so a PAV row can be indexed either way and
#: nothing but the ordering changes — but the two must not be zipped together.
THE_TWO_ORDERINGS_OF_THE_EIGHT_MUST_NOT_BE_ZIPPED = (
    "ASHTAKAVARGA_REFERENCES is Sun, Moon, Mars, Mercury, Jupiter, Venus, "
    "Saturn, Lagna. KAKSHYA_LORDS is Saturn, Jupiter, Mars, Sun, Venus, "
    "Mercury, Moon, Lagna. The same eight names in different orders; only "
    "Mars and Lagna sit in the same position in both.")
