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
