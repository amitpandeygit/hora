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
