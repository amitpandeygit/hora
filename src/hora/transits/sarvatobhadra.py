"""§26.8 — the Sarvatobhadra chakra, a 9 x 9 grid of 81 squares.

Figure 3 as printed, cell by cell. The grid holds four kinds of thing: 28
nakshatras round the border, 12 rasis and 20 consonants inside it, 16 vowels
on the two diagonals, and 5 squares of tithis and weekdays at the centre. The
section's own arithmetic — 16 + 20 + 12 + 28 + 5 = 81 — is the check on the
transcription, and it is asserted rather than trusted.

The section's own split of those 81 into 16 vowels and 20 consonants is
**wrong** — see `THE_TALLY_MISCOUNTS_THE_LETTERS` and D-77. The figure has 17
vowel squares, the vowel *a* being on two of them, and 19 consonant squares.
The two errors cancel, so the 81 closes and the slip is easy to miss.
"""
from __future__ import annotations

from hora.core import validate


class SarvatobhadraError(validate.InputError):
    """A Sarvatobhadra input that cannot be resolved."""


SARVATAH_MEANS = "everywhere, or entirely"
BHADRA_MEANS = "auspicious, or well"

SARVATOBHADRA_DEFINITION = (
    "Sarvatah means \"everywhere\" or \"entirely\". Bhadra means "
    "\"auspicious\" or \"well\". Sarvatobhadra chakra is a chart that shows "
    "all-round well-being and all kinds of auspicious and inauspicious "
    "results.")

SARVATOBHADRA_COMPOSITION = (
    "There are 9 x 9 = 81 squares in the chart. Middle 7 squares on the "
    "outer borders contains 7 nakshatras each. Abhijit (the last quarter of "
    "Uttarashadha) is included among the nakshatras. The innermost 5 squares "
    "contains weekdays and tithis (lunar days).")

#: The section's own tally, which the grid must satisfy exactly.
SARVATOBHADRA_TALLY = (
    "We see that 16 (vowels) + 20 (consonants) + 12 (rasis) + 28 "
    "(nakshtras) + 5 (tithis and weekdays) = 81.")

DIAGONALS_HOLD_THE_VOWELS = (
    "Some consonants are listed in the squres just inside the border "
    "squares. All the squares lying on diagonals of the chart, except the "
    "central square of the chart, contain vowels.")

#: **Finding.** Row 2, column 7 holds the vowel **a**, which is also in the
#: north-east corner — the only letter in the figure to occupy two squares.
#: It was left blank until Exercise 46 read it out: that answer's northward
#: line from Makha lists "uu, d (alveolar), h, k, v, **a**, u and Bharani",
#: and the sixth of those is this square. It is off both diagonals, so §26.8's
#: rule that the diagonals hold vowels is a one-way statement, not a
#: definition of where vowels may be.
A_IS_THE_ONE_LETTER_ON_TWO_SQUARES = (
    "The vowel a is at the north-east corner and again at row 2, column 7. "
    "No other letter in Figure 3 is repeated, and the second of the two is "
    "on neither diagonal."
)

#: **Book defect.** The section's closing sum is right in total and wrong in
#: its split: Figure 3 has **17** vowel squares over 16 distinct vowels, and
#: **19** consonant squares, not 20. The two slips cancel — both pairs sum to
#: 36 — so the 81 still closes. The tally is held verbatim and is not used as
#: a check on the grid. See D-77.
THE_TALLY_MISCOUNTS_THE_LETTERS = (
    "Section 26.8 counts 16 vowels and 20 consonants. Figure 3 has 17 vowel "
    "squares, because a is on two of them, and 19 consonant squares. The "
    "totals agree at 36 and the section's 81 is unaffected."
)

#: Figure 3, row by row from NORTH, column by column from WEST.
FIGURE_3: tuple[tuple[str, ...], ...] = (
    ("ee", "Dhanishtha", "Satabhisha", "P.Bhadra", "U.Bhadra", "Revati",
     "Aswini", "Bharani", "a"),
    ("Sravana", "rii", "g", "s", "d", "ch", "l", "u", "Krittika"),
    ("Abhijit", "kh", "ai", "Aq", "Pi", "Ar", "lu", "a", "Rohini"),
    ("U.Shadha", "j", "Cp", "ah", "Rikta", "o", "Ta", "v", "Mriga"),
    ("P.Shadha", "bh", "Sg", "Jaya", "Poorna", "Nanda", "Ge", "k", "Ardra"),
    ("Moola", "y", "Sc", "am", "Bhadra", "au", "Cn", "h", "Punar"),
    ("Jyeshtha", "n", "e", "Li", "Vi", "Le", "luu", "d.", "Pushya"),
    ("Anuradha", "ri", "t", "r", "p", "t.", "m", "uu", "Asresha"),
    ("i", "Visakha", "Swaati", "Chitra", "Hasta", "U.Pha", "Poo.Pha",
     "Makha", "aa"),
)

#: The 28 nakshatras, by border. Each border's middle seven squares.
BORDER_NAKSHATRAS: dict[str, tuple[str, ...]] = {
    "north": tuple(str(cell) for cell in FIGURE_3[0][1:8]),
    "south": tuple(str(cell) for cell in FIGURE_3[8][1:8]),
    "west": tuple(str(FIGURE_3[row][0]) for row in range(1, 8)),
    "east": tuple(str(FIGURE_3[row][8]) for row in range(1, 8)),
}

#: The 16 vowels, in the order they sit on the two diagonals.
VOWELS: tuple[str, ...] = (
    "ee", "rii", "ai", "ah", "au", "luu", "uu", "aa",
    "a", "u", "lu", "o", "am", "e", "ri", "i")

#: The 12 rasis, and where each sits.
RASI_CELLS: dict[str, tuple[int, int]] = {
    "Aq": (2, 3), "Pi": (2, 4), "Ar": (2, 5),
    "Cp": (3, 2), "Ta": (3, 6),
    "Sg": (4, 2), "Ge": (4, 6),
    "Sc": (5, 2), "Cn": (5, 6),
    "Li": (6, 3), "Vi": (6, 4), "Le": (6, 5),
}

#: The five central squares, each with its tithi group and its weekdays.
CENTRE_CELLS: dict[tuple[int, int], dict[str, object]] = {
    (3, 4): {"tithi_group": "Rikta", "weekdays": ("Friday",)},
    (4, 3): {"tithi_group": "Jaya", "weekdays": ("Thursday",)},
    (4, 4): {"tithi_group": "Poorna", "weekdays": ("Saturday",)},
    (4, 5): {"tithi_group": "Nanda", "weekdays": ("Sunday", "Tuesday")},
    (5, 4): {"tithi_group": "Bhadra", "weekdays": ("Monday", "Wednesday")},
}

#: §26.8's five tithi groups, exactly as printed. Poorna's list is the one
#: that is short — see `THE_TWENTY_FIFTH_TITHI_IS_MISSING` and D-76.
TITHI_GROUPS: dict[str, tuple[int, ...]] = {
    "Nanda": (1, 6, 11, 16, 21, 26),
    "Bhadra": (2, 7, 12, 17, 22, 27),
    "Jaya": (3, 8, 13, 18, 23, 28),
    "Rikta": (4, 9, 14, 19, 24, 29),
    "Poorna": (5, 10, 15, 20, 30),
}

#: **Book defect.** Four of the five groups step by 5 and hold six tithis;
#: Poorna holds five and steps 5, 5, 5, **10**. The **25th tithi belongs to no
#: group**, and by every other row's pattern it is Poorna's. Held as printed;
#: see D-76.
THE_TWENTY_FIFTH_TITHI_IS_MISSING = (
    "Nanda, Bhadra, Jaya and Rikta each list six tithis five apart. Poorna "
    "lists 5, 10, 15, 20 and 30 — five tithis, with a gap of ten between the "
    "last two — so the 25th is in no group at all."
)

VEDHA_RULE = (
    "When a planet occupies a nakshatra, it causes vedha (obstruction) on "
    "the contents of the squares along 3 lines. We can draw one vertical or "
    "horizontal line and two crossward lines starting at the nakshatra. "
    "Contents of the squares on the lines have vedha from the planet.")

#: **Finding — Example 114 settles it.** The rule reads ambiguously on its
#: own: "one vertical **or** horizontal line" does not say which, and
#: "crossward" is undefined. The worked case fixes both. Saturn in Punarvasu,
#: on the **east** border, draws its straight line **west** — perpendicular to
#: its own border, into the grid — and its two crossward lines **northwest**
#: and **southwest**, the two diagonals that also run inward. So the straight
#: line is decided by which border the nakshatra sits on, and crossward means
#: the grid's diagonals.
THE_LINES_RUN_INWARD_FROM_THE_NAKSHATRAS_OWN_BORDER = (
    "A nakshatra on the east border draws west, northwest and southwest; the "
    "straight line is perpendicular to its border and the two crossward "
    "lines are the diagonals, all three running into the grid. Example 114 "
    "shows all three for Punarvasu."
)


def cell(row: int, column: int) -> str:
    """One square of Figure 3."""
    r = validate.in_range("row", int(row), 0, 8)
    c = validate.in_range("column", int(column), 0, 8)
    return FIGURE_3[r][c]


def tithi_group(tithi: int) -> str | None:
    """The group a tithi belongs to, or ``None`` for the 25th."""
    index = validate.in_range("tithi", int(tithi), 1, 30)
    for name, members in TITHI_GROUPS.items():
        if index in members:
            return name
    return None


# --------------------------------------------------------------------------
# Example 114 — the three lines, drawn
# --------------------------------------------------------------------------

#: Which way each border's squares draw, as (straight, crossward, crossward).
#: Read off Example 114's east-border case and applied to the other three by
#: the symmetry the figure is built on — the chakra is "sarvatobhadra",
#: auspicious *from every side*, and nothing in §26.8 privileges one border.
BORDER_DIRECTIONS: dict[str, tuple[str, str, str]] = {
    "east": ("west", "northwest", "southwest"),
    "west": ("east", "northeast", "southeast"),
    "north": ("south", "southwest", "southeast"),
    "south": ("north", "northwest", "northeast"),
}

_STEPS: dict[str, tuple[int, int]] = {
    "north": (-1, 0), "south": (1, 0), "east": (0, 1), "west": (0, -1),
    "northeast": (-1, 1), "northwest": (-1, -1),
    "southeast": (1, 1), "southwest": (1, -1),
}

EXAMPLE_114 = (
    "Let us say Saturn is in Punarvasu. We see that Punarvasu is on the "
    "eastern border.")

#: Example 114's three lines, as it lists their contents.
EXAMPLE_114_LINES: dict[str, tuple[str, ...]] = {
    "west": ("h", "Cn", "au", "Bhadra", "am", "Sc", "y", "Moola"),
    "northwest": ("k", "Ta", "Ar", "d", "P.Bhadra"),
    "southwest": ("d.", "m", "U.Pha"),
}

#: **Finding.** Example 114 checks sixteen of Figure 3's squares against the
#: book's own reading, in three directions, and every one matches — including
#: the two that would be easy to confuse, the plain **d** at row 1 and the
#: **alveolar d** at row 6, which the example distinguishes in words.
EXAMPLE_114_VERIFIES_SIXTEEN_SQUARES = (
    "The three lines from Punarvasu name sixteen squares, and the "
    "transcription of Figure 3 reproduces all sixteen in the order the "
    "example gives them. It calls the row-6 square \"d (alveolar)\", "
    "distinguishing it from the plain d in row 1."
)

#: **Finding.** A line stops at the edge of the grid, and the three lines from
#: one nakshatra reach different distances — eight squares west of Punarvasu,
#: five northwest, three southwest. So the number of things a graha obstructs
#: depends on where along its border it sits, which §26.8 never mentions.
LINES_ARE_UNEQUAL_IN_LENGTH = (
    "From Punarvasu the westward line crosses eight squares, the northwest "
    "five and the southwest three. A nakshatra nearer a corner obstructs "
    "fewer squares on one diagonal and more on the other."
)


def border_of(row: int, column: int) -> str:
    """Which border a square sits on, for a nakshatra square."""
    r = validate.in_range("row", int(row), 0, 8)
    c = validate.in_range("column", int(column), 0, 8)
    sides = [name for name, test in (("north", r == 0), ("south", r == 8),
                                     ("west", c == 0), ("east", c == 8))
             if test]
    if not sides:
        raise SarvatobhadraError(
            f"square ({r}, {c}) is not on a border; only the border squares "
            f"hold nakshatras")
    if len(sides) > 1:
        raise SarvatobhadraError(
            f"square ({r}, {c}) is a corner and holds a vowel, not a "
            f"nakshatra")
    return sides[0]


def vedha_lines(row: int, column: int) -> dict:
    """§26.8's three lines from a nakshatra square, as Example 114 draws them.

    :returns: the border the square sits on, and the three lines by
        direction, each a list of ``{"row", "column", "content"}`` running
        inward until it leaves the grid. A square left untranscribed appears
        with ``content`` ``None`` — see `UNCERTAIN_CELL`.
    """
    side = border_of(row, column)
    r, c = int(row), int(column)
    lines = {}
    for direction in BORDER_DIRECTIONS[side]:
        step_r, step_c = _STEPS[direction]
        squares = []
        rr, cc = r + step_r, c + step_c
        while 0 <= rr <= 8 and 0 <= cc <= 8:
            squares.append({"row": rr, "column": cc,
                            "content": FIGURE_3[rr][cc]})
            rr, cc = rr + step_r, cc + step_c
        lines[direction] = squares
    return {
        "square": {"row": r, "column": c, "content": FIGURE_3[r][c]},
        "border": side,
        "straight": BORDER_DIRECTIONS[side][0],
        "crossward": BORDER_DIRECTIONS[side][1:],
        "lines": lines,
        "obstructs": [square["content"]
                      for direction in BORDER_DIRECTIONS[side]
                      for square in lines[direction]],
        "rule": VEDHA_RULE,
    }


def find(content: str) -> tuple[int, int]:
    """Where a named square sits in Figure 3."""
    for r in range(9):
        for c in range(9):
            if FIGURE_3[r][c] == content:
                return (r, c)
    raise SarvatobhadraError(f"{content!r} is not in Figure 3")


EXERCISE_46 = (
    "Find all the consonants, vowels, tithis, weekdays, rasis and "
    "constellations on which Venus in Makha has vedha.")

#: Exercise 46's three lines, as its answer lists them. Makha is on the south
#: border, so the straight line runs north and the two crossward lines run
#: northeast and northwest.
EXERCISE_46_LINES: dict[str, tuple[str, ...]] = {
    "north": ("uu", "d.", "h", "k", "v", "a", "u", "Bharani"),
    "northeast": ("Asresha",),
    "northwest": ("m", "Le", "Bhadra", "Jaya", "Cp", "kh", "Sravana"),
}

#: **Finding.** Makha sits one square from the south-east corner, and its
#: north-east crossward line is a **single** square — Asresha — where its
#: north-west line crosses seven. Example 114's Punarvasu had 8, 5 and 3.
#: So the same rule gives one nakshatra sixteen obstructions and another nine,
#: and §26.8 nowhere says the count varies.
A_CORNER_NAKSHATRA_OBSTRUCTS_FAR_LESS = (
    "Venus in Makha obstructs sixteen squares: eight north, seven northwest "
    "and one northeast. A nakshatra beside a corner has one crossward line "
    "of a single square."
)


# --------------------------------------------------------------------------
# §26.8's four special principles
# --------------------------------------------------------------------------

CORNER_VOWEL_RULE = (
    "A planet in the first quarter of Krittika or the last quarter of "
    "Bharani has vedha on the vowel \"a\" which is in the northeastern "
    "corner. A similar thing applies to all the vowels in corners.")

#: Each corner vowel and the two padas that reach it: the **last quarter of
#: the nakshatra before it** in the border sequence and the **first quarter of
#: the one after**. The book states the north-east case and says a similar
#: thing applies to the rest; these three are ours, read off the figure.
CORNER_VOWELS: dict[str, dict[str, object]] = {
    "a": {"corner": "northeast", "square": (0, 8),
          "last_quarter_of": "Bharani", "first_quarter_of": "Krittika"},
    "aa": {"corner": "southeast", "square": (8, 8),
           "last_quarter_of": "Asresha", "first_quarter_of": "Makha"},
    "i": {"corner": "southwest", "square": (8, 0),
          "last_quarter_of": "Visakha", "first_quarter_of": "Anuradha"},
    "ee": {"corner": "northwest", "square": (0, 0),
           "last_quarter_of": "Sravana", "first_quarter_of": "Dhanishtha"},
}

#: **Finding.** The corner rule is the border sequence closing up. Walking the
#: border clockwise gives the 28 nakshatras in zodiacal order — Dhanishtha
#: round to Sravana — with the four corner vowels **inserted between**
#: consecutive nakshatras, at every eighth square. So a corner vowel is simply
#: the join between two nakshatras, and the two padas that touch it are the
#: last of one and the first of the next. That is why no line reaches a
#: corner, and why the rule needs stating separately.
THE_CORNERS_ARE_JOINS_IN_THE_NAKSHATRA_SEQUENCE = (
    "The border reads Dhanishtha, Satabhisha ... Abhijit, Sravana in "
    "zodiacal order, and the four corner vowels sit between Bharani and "
    "Krittika, Asresha and Makha, Visakha and Anuradha, and Sravana and "
    "Dhanishtha — one every eight squares."
)

SIMILAR_VOWEL_RULE = (
    "If an vowel has vedha, its similar vowel (e.g. a and aa, i and ee, u "
    "and uu) also has vedha from the same planet.")

#: The similar-vowel pairs §26.8 names. It gives three "e.g." pairs and no
#: closed list, so only these three are held.
SIMILAR_VOWELS: tuple[tuple[str, str], ...] = (
    ("a", "aa"), ("i", "ee"), ("u", "uu"))

#: **Finding.** The three pairs the section names are exactly the short and
#: long forms of the same vowel, and they are the only three of Figure 3's
#: sixteen vowels that have such a partner **in the figure** — ri and rii, and
#: lu and luu, are also short-long pairs and are **not** named. So the list is
#: either incomplete or deliberately confined to the three; the section's
#: "e.g." leaves it open. See OI-148.
THE_SIMILAR_VOWEL_LIST_IS_OPEN = (
    "Section 26.8 gives a and aa, i and ee, u and uu as examples. Figure 3 "
    "also holds ri with rii and lu with luu, which are short and long forms "
    "of one vowel in the same way, and the section does not name them."
)

UNCOVERED_CONSONANT_RULE = (
    "Some consonants are not covered in this chart.")

#: The four nakshatras that carry consonants Figure 3 has no square for.
UNCOVERED_CONSONANTS: dict[str, tuple[str, ...]] = {
    "Ardra": ("g", "chh", "ng (nasal)"),
    "Hasta": ("h", "n (alveolar)", "th (alveolar)"),
    "Poorvashadha": ("dh (dental)", "ph", "dh (alveolar)"),
    "Uttara Bhadrapada": ("th (dental)", "jh", "nch (nasal)"),
}

#: **Finding.** Each of the four carries **three** extra consonants, twelve in
#: all, and the four nakshatras are spread one to a border — Ardra on the
#: east, Hasta on the south, Poorvashadha on the west, Uttara Bhadrapada on
#: the north. Two of the twelve, **g** and **h**, already have squares of
#: their own in Figure 3, so those two are reachable both by a line and by
#: this rule.
THE_UNCOVERED_CONSONANTS_ARE_ONE_TRIPLE_PER_BORDER = (
    "Ardra, Hasta, Poorvashadha and Uttara Bhadrapada each carry three "
    "consonants the chart has no square for, and the four sit one to each "
    "border. g and h are in the figure as well as on this list."
)

PAIRED_CONSONANT_RULE = (
    "If a planet has vedha on one of the following pairs of consonants, it "
    "has vedha on the other one too: b & v; s & sh (palatal); kh & sh "
    "(alveolar); j & y; ng & tr.")

#: The five consonant pairs that share a vedha.
PAIRED_CONSONANTS: tuple[tuple[str, str], ...] = (
    ("b", "v"), ("s", "sh (palatal)"), ("kh", "sh (alveolar)"),
    ("j", "y"), ("ng", "tr"))

#: **Finding.** Only **four** of the ten paired consonants have a square in
#: Figure 3 — v, s, kh, j and y, of which j and y are a pair, so the pairing
#: reaches b, sh twice, ng and tr from outside the grid. `ng` is also on
#: Ardra's uncovered list, so it can be reached two ways.
THE_PAIRS_REACH_CONSONANTS_THE_GRID_LACKS = (
    "Of b, v, s, sh, kh, sh, j, y, ng and tr, only v, s, kh, j and y are "
    "squares in Figure 3. The pairing is how a planet reaches b, the two "
    "sh's, ng and tr, none of which the chart draws."
)


# --------------------------------------------------------------------------
# Using the chakra
# --------------------------------------------------------------------------

#: The five natal points §26.8 says to watch for vedha, in its order. Each is
#: named with an alternative, so the chakra is read against a matter and not
#: only against a birth.
NATAL_POINTS_TO_WATCH: tuple[dict[str, str], ...] = (
    {"point": "the constellation occupied by Moon",
     "alternative": "any special tara"},
    {"point": "the rasi occupied by lagna",
     "alternative": "any house of interest"},
    {"point": "the first/prominent consonant and vowel in the native's name",
     "alternative": ""},
    {"point": "the tithi of birth (janma tithi)",
     "alternative": "a special tithi"},
    {"point": "the weekday of birth (janma vaara)", "alternative": ""},
)

#: **Finding.** The third point is the only place in the whole book where a
#: native's **name** enters a calculation. Everything else in Part 3 is read
#: from positions; this asks for a letter, which is why the chakra carries
#: sixteen vowels and nineteen consonants at all.
THE_NAME_IS_THE_ONLY_NON_ASTRONOMICAL_INPUT = (
    "Section 26.8 asks for the first or prominent consonant and vowel in the "
    "native's name. No other technique in the book takes an input that is "
    "not a position or a moment."
)

SARVATOBHADRA_READING = (
    "Vedha by benefics (Moon, Mercury, Jupiter and Venus) is favorable and "
    "vedha by malefics (Sun, Mars, Saturn, Rahu and Ketu) is unfavorable. If "
    "several transiting benefics have simultaneous vedha on several natal "
    "points listed above, then good results may be expected. Malefics, on "
    "the other hand, give bad results.")

#: §26.8's own split of the nine, which it states without conditions.
SARVATOBHADRA_BENEFICS: tuple[str, ...] = (
    "Moon", "Mercury", "Jupiter", "Venus")
SARVATOBHADRA_MALEFICS: tuple[str, ...] = (
    "Sun", "Mars", "Saturn", "Rahu", "Ketu")

#: **Finding.** §26.8 puts the **Moon and Mercury** among the benefics flatly,
#: where §3.2.2 makes both conditional — the Moon by paksha and Mercury by
#: association — which is why `NATURAL_BENEFIC` holds only Jupiter and Venus.
#: So this section reads a fixed four-and-five split that the book's own
#: definition of benefic does not support.
THE_SPLIT_IGNORES_THE_CONDITIONAL_BENEFICS = (
    "Section 26.8 names the Moon and Mercury benefics without qualification. "
    "Section 3.2.2 makes the Moon's nature depend on the paksha and "
    "Mercury's on his associations, so neither is in NATURAL_BENEFIC."
)

FOOTNOTE_70 = (
    "This author's experience in the use of Sarvatobhadra Chakra is very "
    "very limited.")

#: **Finding.** Footnote 70 is the only place PVR disclaims his own
#: **experience** of a technique rather than its reliability. Footnotes 72 and
#: 74 bound what the nakshatra principles can carry; this one says the author
#: has hardly used the method. It is the strongest caveat in Part 3.
FOOTNOTE_70_IS_A_DISCLAIMER_OF_EXPERIENCE = (
    "Footnotes 72 and 74 limit what a technique may be used for. Footnote 70 "
    "limits the author's own acquaintance with it, which nothing else in "
    "Part 3 does."
)


# --------------------------------------------------------------------------
# Special tithis
# --------------------------------------------------------------------------

SPECIAL_TITHI_RULE = (
    "To find karma tithi, we multiply the difference between Moon's "
    "longitude and Sun's longitude with 10 and reduce the product to a value "
    "between 0º and 360º (by adding or subtracting multiples of 360º). We "
    "divide it by 12 and add 1 to the quotient. That gives a number between "
    "1 and 30 and that represents \"karma tithi\". Karma tithi changes 10 "
    "times as fast as normal tithi. Similarly \"dhana tithi\" (lunar day of "
    "wealth) changes twice as fast as normal tithi.")

#: The special tithis and their multipliers. §26.8 names karma and dhana;
#: Example 116 uses a third, the **tithi of power**, and names its house.
SPECIAL_TITHI_MULTIPLIERS: dict[str, int] = {
    "karma": 10, "dhana": 2, "power": 5}

#: **Finding.** The multiplier is the **house number** of the matter. Karma is
#: the 10th house and multiplies by 10; dhana is the 2nd and multiplies by 2;
#: Example 116's tithi of power multiplies by 5 and the same example calls Sg
#: "the 5th house of power". §26.8 states the first two multipliers and the
#: rule behind them nowhere, and Example 116 confirms it by arithmetic — a
#: multiplier of 5 on Rajiv Gandhi's birth gives the 6th tithi, which is the
#: Sukla Shashthi in the Nanda group the example names.
THE_MULTIPLIER_IS_THE_HOUSE_NUMBER = (
    "Karma tithi is the 10th house's and multiplies by 10, dhana tithi is "
    "the 2nd house's and multiplies by 2, and the tithi of power is the 5th "
    "house's and multiplies by 5. The book gives the first two multipliers "
    "and never the pattern."
)

#: The house each named tithi belongs to, which is also its multiplier.
SPECIAL_TITHI_HOUSES: dict[str, int] = {
    "karma": 10, "dhana": 2, "power": 5}

#: **Finding.** The rule generalises the ordinary tithi rather than replacing
#: it: a multiplier of **1** is §1.3.8's own tithi, so `special_tithi` with
#: ``multiplier=1`` and `panchanga.core.tithi_at` must agree everywhere. That
#: is asserted rather than assumed.
A_MULTIPLIER_OF_ONE_IS_THE_ORDINARY_TITHI = (
    "Karma tithi multiplies the Moon-Sun difference by 10 and dhana tithi by "
    "2. At 1 the formula is section 1.3.8's tithi unchanged."
)


def special_tithi(sun_longitude: float, moon_longitude: float,
                  multiplier: int = 1) -> dict:
    """§26.8's tithi for a matter — 1 to 30, the ordinary tithi at 1.

    :param multiplier: 10 for karma tithi, 2 for dhana tithi. The section
        says a tithi can be found "for several matters" and names only those
        two, so any positive multiplier is accepted.
    """
    factor = validate.in_range("multiplier", int(multiplier), 1, 360)
    difference = (float(moon_longitude) - float(sun_longitude)) % 360.0
    reduced = (difference * factor) % 360.0
    index = int(reduced // 12.0) + 1
    named = [name for name, value in SPECIAL_TITHI_MULTIPLIERS.items()
             if value == factor]
    return {
        "multiplier": factor,
        "name": named[0] if named else None,
        "difference": difference,
        "reduced": reduced,
        "tithi": index,
        "group": tithi_group(index),
        "changes_faster_by": factor,
    }


# --------------------------------------------------------------------------
# How much evidence a reading needs, and Example 115
# --------------------------------------------------------------------------

HOW_MUCH_EVIDENCE_IS_NEEDED = (
    "If just one natal reference has vedha from just one planet, we cannot "
    "make any predictions. But, if 2-3 natal reference have vedha from a "
    "couple of benefic/malefic transit planets, then we can be more "
    "confident. However, a prediction should be made only if dasas and "
    "Tajaka charts also show an event.")

#: **Finding.** §26.8 is the only technique in Part 3 that states a **minimum
#: weight of evidence** — two or three natal references, each struck by a
#: couple of planets — before anything may be said. And it closes with the
#: same requirement footnote 74 gave for latta: dasas and Tajaka too. So the
#: chakra is bounded twice, by a floor of its own and by a corroboration it
#: cannot supply.
THE_CHAKRA_STATES_A_MINIMUM_WEIGHT_OF_EVIDENCE = (
    "One natal reference struck by one planet is explicitly not enough. Two "
    "or three struck by a couple of planets is, and even then a prediction "
    "waits on the dasas and the Tajaka chart."
)

EXAMPLE_115 = (
    "Let us consider the death of John F. Kennedy, Jr. The data of birth and "
    "death can be found in Example 107.")

#: Example 115's five natal reference points, and where each sits in Figure 3.
EXAMPLE_115_NATAL_POINTS: tuple[dict[str, str], ...] = (
    {"point": "janma tithi", "value": "Sukla Ashtami, the 8th",
     "square": "Jaya"},
    {"point": "janma vaara", "value": "Thursday", "square": "Jaya"},
    {"point": "janma nakshatra", "value": "Dhanishtha",
     "square": "Dhanishtha"},
    {"point": "vainaasika nakshatra", "value": "Anooradha",
     "square": "Anuradha"},
    {"point": "naidhana nakshatra", "value": "Bharani", "square": "Bharani"},
    {"point": "the house of accidents", "value": "Cp, the 3rd from AL",
     "square": "Cp"},
)

#: Which transiting graha strikes which natal point, as the example reads it.
EXAMPLE_115_VEDHAS: tuple[tuple[str, str, str], ...] = (
    ("Ketu", "Sravana", "Jaya"),
    ("Saturn", "Bharani", "Jaya"),
    ("Ketu", "Sravana", "Dhanishtha"),
    ("Rahu", "Asresha", "Dhanishtha"),
    ("Saturn", "Bharani", "Anuradha"),
    ("Rahu", "Asresha", "Anuradha"),
    ("Ketu", "Sravana", "Cp"),
    ("Mars", "Swaati", "Cp"),
)

EXAMPLE_115_CONCLUSION = (
    "Considering that several key natal references are coming under the "
    "vedha of a couple of malefics, unfavorable results are possible. "
    "Considering the involvement of naidhana and vainaasika nakshatras, "
    "death is possible.")

#: **Finding.** Every graha the example uses is a **malefic** — Saturn, Mars,
#: Rahu and Ketu, four of §26.8's five — and each of the four natal points is
#: struck by exactly **two** of them. That is the section's own floor of "2-3
#: natal references ... from a couple of planets" met precisely, which is why
#: the reading is allowed to stand at all.
THE_EXAMPLE_MEETS_ITS_OWN_EVIDENCE_FLOOR = (
    "Four natal points — the Jaya square carrying both janma tithi and janma "
    "vaara, janma nakshatra, vainaasika nakshatra and the house of accidents "
    "— each take vedha from exactly two malefics, and no benefic appears in "
    "the reading."
)

#: **Finding.** One square carries **two** natal references. Janma tithi is in
#: the Jaya group and janma vaara is Thursday, and Figure 3 puts Jaya and
#: Thursday in the same square, so a single vedha strikes both at once. That
#: is why the example's four struck squares yield five natal points.
ONE_SQUARE_CAN_CARRY_TWO_NATAL_POINTS = (
    "Jaya and Thursday share the square at row 4, column 3, so a planet "
    "striking it strikes both the janma tithi and the janma vaara of this "
    "nativity."
)

FOOTNOTE_71 = (
    "As per the western calendar, Friday came at midnight and the native was "
    "born at 12:22 am. However, a new day starts at sunrise for Hindus. So "
    "it was still Thursday.")

#: **Finding.** Footnote 71 states the rule our own `day_structure` gets
#: wrong. It searches for sunrise from local midnight, so for a 00:22 birth it
#: finds that morning's sunrise rather than the previous one, and
#: `compute_panchanga` raises before it can return a vaara at all. See OI-149;
#: nothing is changed here, because that function feeds every panchanga.
FOOTNOTE_71_NAMES_A_DEFECT_IN_OUR_OWN_CODE = (
    "A new day starts at sunrise, so a birth at 12:22 am belongs to the "
    "previous sunrise's weekday. Our day_structure takes the first sunrise "
    "after local midnight instead, and compute_panchanga raises for any "
    "instant before sunrise."
)


# --------------------------------------------------------------------------
# Example 116 — the same method read the other way
# --------------------------------------------------------------------------

EXAMPLE_116 = (
    "Let us consider Rajiv Gandhi's ascension to power in India on October "
    "31, 1984. It was covered in Exercise 40. Rasi chart of Mr. Gandhi can be "
    "found in Chart 39.")

#: Example 116's four vedhas, each a pair of benefics on one natal reference.
EXAMPLE_116_VEDHAS: tuple[tuple[str, str, str], ...] = (
    ("Jupiter", "P.Shadha", "Nanda"),
    ("Mercury", "Visakha", "Nanda"),
    ("Mercury", "Visakha", "Dhanishtha"),
    ("Moon", "Sravana", "Dhanishtha"),
    ("Jupiter", "P.Shadha", "Sg"),
    ("Venus", "Jyeshtha", "Sg"),
    ("Mercury", "Visakha", "Li"),
    ("Venus", "Jyeshtha", "Li"),
)

#: What each struck square stands for in the nativity.
EXAMPLE_116_NATAL_POINTS: tuple[dict[str, str], ...] = (
    {"square": "Nanda", "point": "janma vaara",
     "value": "Sunday, the weekday of birth"},
    {"square": "Nanda", "point": "the tithi of power",
     "value": "Sukla Shashthi, the 6th, in the Nanda group"},
    {"square": "Dhanishtha", "point": "abhisheka nakshatra",
     "value": "the constellation of coronation"},
    {"square": "Sg", "point": "the 5th house of power",
     "value": "Sagittarius, the 5th from a Leo lagna"},
    {"square": "Li", "point": "the rasi holding GL",
     "value": "Libra; GL is the seat of power"},
)

EXAMPLE_116_CONCLUSION = (
    "So janma vaara, an important tithi, an important nakshatra and two "
    "important rasis in natal chart have vedha from two benefic planets "
    "each. This is conducive to getting political power.")

#: **Finding.** Examples 115 and 116 are the same method run in mirror. Each
#: strikes **four** squares, each square by exactly **two** planets, and
#: neither mixes benefic with malefic: 115 is Saturn, Mars, Rahu and Ketu and
#: reads death; 116 is Jupiter, Mercury, Venus and the Moon and reads power.
#: So the chakra's verdict is carried entirely by the nature of the strikers,
#: and the evidence floor is met identically on both sides.
THE_TWO_EXAMPLES_ARE_THE_METHOD_IN_MIRROR = (
    "Example 115 has four malefics striking four squares two apiece and "
    "reads death; Example 116 has four benefics striking four squares two "
    "apiece and reads political power. Same shape, opposite natures."
)

#: **Finding.** The Nanda square carries **Sunday and Tuesday**, and the
#: example reads only Sunday, because that is this nativity's janma vaara. So
#: a square with two weekdays is read for whichever the chart makes relevant,
#: not for both — the same way Example 115's Jaya square was read for one
#: tithi group and one weekday at once.
A_SQUARE_IS_READ_FOR_WHAT_THE_CHART_MAKES_RELEVANT = (
    "The Nanda square holds Sunday and Tuesday. Example 116 takes Sunday "
    "alone, that being the janma vaara, and the Nanda tithi group, that "
    "being where the tithi of power falls."
)

#: **Finding.** Rajiv Gandhi's nativity is printed twice — Chart 39 for the
#: rasi chart in chapter 22 and Chart 60 for the D-10 and the transit in
#: chapter 25 — with identical longitudes. Example 116 cites the earlier one.
RAJIV_GANDHI_IS_PRINTED_AS_TWO_CHARTS = (
    "Chart 39 is his rasi chart and Chart 60 his D-10 with the accession "
    "transit. The birth data and every printed longitude agree."
)


# --------------------------------------------------------------------------
# Example 117 — the same native, the same natal points, the other verdict
# --------------------------------------------------------------------------

EXAMPLE_117 = (
    "Let us continue with the same native. Rajiv Gandhi's party lost "
    "majority in the elections of November 22, 1989.")

EXAMPLE_117_KARMA_NAKSHATRA = (
    "When he became India's Prime Minister in 1984, Jupiter was in "
    "Poorvashadha. Poorvashadha is karma nakshatra (constellation of "
    "profession). At the time of Mr. Gandhi's defeat in 1989, Saturn was in "
    "that constellation.")

#: Example 117's three natal points and the malefics on each. Unlike Examples
#: 115 and 116 this list mixes two kinds of evidence — see
#: `OCCUPATION_COUNTS_AS_WELL_AS_VEDHA` — so each strike carries its kind.
EXAMPLE_117_STRIKES: tuple[tuple[str, str, str, str], ...] = (
    ("Saturn", "P.Shadha", "Nanda", "vedha"),
    ("Rahu", "Dhanishtha", "Nanda", "vedha"),
    ("Ketu", "Asresha", "Nanda", "vedha"),
    ("Rahu", "Dhanishtha", "Dhanishtha", "occupation"),
    ("Ketu", "Asresha", "Dhanishtha", "vedha"),
    ("Mars", "Swaati", "Sg", "vedha"),
    ("Saturn", "P.Shadha", "Sg", "vedha"),
)

#: What each struck square stands for. These are Example 116's points read
#: again — "the same natal references considered in the last example" — minus
#: the Libra square, on which see `A_NATAL_POINT_WITH_NO_EVIDENCE_IS_DROPPED`.
EXAMPLE_117_NATAL_POINTS: tuple[dict[str, str], ...] = (
    {"square": "Nanda", "point": "janma vaara",
     "value": "Sunday, the weekday of birth"},
    {"square": "Nanda", "point": "the tithi of power",
     "value": "Sukla Shashthi, the 6th, in the Nanda group"},
    {"square": "Dhanishtha", "point": "abhisheka nakshatra",
     "value": "the constellation of coronation"},
    {"square": "Sg", "point": "the 5th house of power",
     "value": "Sagittarius, the 5th from a Leo lagna"},
)

EXAMPLE_117_CONCLUSION = (
    "For these reasons, transits were unfavorable from the point of view of "
    "political power. So Mr. Gandhi's party lost power.")

#: **Finding.** Clause (2) counts a planet **standing in** a square as
#: evidence on that square: "Dhanishtha ... is occupied by Rahu and Ketu has
#: vedha on it" is one abhisheka nakshatra carrying two malefics, one by
#: occupation and one by vedha. `SARVATOBHADRA_READING` speaks only of vedha
#: and Examples 115 and 116 used nothing else, so occupation as evidence
#: enters the book here and is never stated as a rule. `strike` reports the
#: two kinds separately rather than merging them.
OCCUPATION_COUNTS_AS_WELL_AS_VEDHA = (
    "Rahu occupies Dhanishtha and Ketu has vedha on it, and Example 117 "
    "counts both against the abhisheka nakshatra. Section 26.8 states the "
    "reading in terms of vedha alone."
)

#: **Finding.** The karma nakshatra changes hands between the two examples.
#: Poorvashadha is the 10th from this native's janma nakshatra; **Jupiter**
#: stood there when he took office in 1984 and **Saturn** stands there when
#: he loses it in 1989. Neither is a vedha — both are occupations — so this
#: paragraph is the second place in the example where sitting in a square is
#: the evidence.
THE_KARMA_NAKSHATRA_CHANGES_HANDS = (
    "Jupiter occupied Poorvashadha at the ascension and Saturn occupies it "
    "at the defeat. The same constellation of profession is read twice, by "
    "occupation both times and by vedha neither time."
)

#: **Finding.** Neither example prints this native's **janma nakshatra**, and
#: Example 117 fixes it twice over. Poorvashadha is the karma nakshatra, the
#: 10th, and Dhanishtha is the abhisheka nakshatra, the 13th; the only
#: constellation with both those offsets is **Poorva Phalguni**, which is
#: where his Moon at 17 Le 09 in Chart 14 actually falls.
THE_TWO_SPECIAL_NAKSHATRAS_FIX_THE_JANMA_NAKSHATRA = (
    "The 10th from Poorva Phalguni is Poorvashadha and the 13th is "
    "Dhanishtha. Chart 14 puts Rajiv Gandhi's Moon in Poorva Phalguni, so "
    "both special nakshatras the two examples name are consistent with it "
    "and with no other birth star."
)

#: **Finding.** Both examples name **only the strikes that carry the verdict
#: they reach.** On 31 October 1984 all four squares take malefic strikes as
#: well — Mars, Saturn and Rahu reach Nanda, Saturn reaches Dhanishtha, the
#: Sun and Mars reach Sg, Saturn and Rahu reach Li — and Example 116 lists
#: none of them. On 22 November 1989 all three squares take benefic strikes
#: as well — the Moon, Jupiter and Venus reach Nanda, Jupiter and Venus reach
#: Sg — and Example 117 lists none of those. Every strike the book does name
#: is confirmed by `vedha_lines`; the omissions are the point. §26.8 gives no
#: rule for weighing a square struck by both natures. See OI-150.
THE_EXAMPLES_NAME_ONLY_THE_STRIKES_THAT_CARRY_THE_VERDICT = (
    "Each of the two readings of this nativity lists strikes of one nature "
    "and is silent on the strikes of the other nature on the same squares, "
    "which our own vedha lines find in both charts."
)

#: **Finding.** Example 117 reads **three** natal points where Example 116
#: read four, and the one it drops is the Libra square holding GL. On that
#: date Libra is struck by the **Moon alone** and by no malefic, so the point
#: that carries nothing of the nature being read is simply not listed.
A_NATAL_POINT_WITH_NO_EVIDENCE_IS_DROPPED = (
    "Example 116 reads Nanda, Dhanishtha, Sg and Li. Example 117 says it "
    "takes the same natal references and reads only the first three; Li "
    "takes no malefic strike on the later date."
)

#: **Finding.** Clause (1) puts **three** malefics on one square. Examples 115
#: and 116 each put exactly two on every square they read, which is
#: `THE_CHAKRA_STATES_A_MINIMUM_WEIGHT_OF_EVIDENCE` met at its floor. This
#: one goes past the floor on its strongest point and stays at two on the
#: others, so the floor is a minimum and not a shape.
THREE_PLANETS_MAY_STRIKE_ONE_SQUARE = (
    "Nanda and Sunday take vedha from Saturn, Rahu and Ketu together. No "
    "earlier reading in the section puts more than two planets on a square."
)

#: **Finding.** A benefic sits in the karma nakshatra at the defeat too:
#: **Venus** is at 22 Sg 31 on 22 November 1989 and Saturn at 17 Sg 29, both
#: in Poorvashadha. The example names Saturn and not Venus, which is
#: `THE_EXAMPLES_NAME_ONLY_THE_STRIKES_THAT_CARRY_THE_VERDICT` showing up in
#: the occupation evidence as well as in the vedhas.
VENUS_IS_IN_THE_KARMA_NAKSHATRA_TOO = (
    "Saturn and Venus are both in Poorvashadha on 22 November 1989. The "
    "paragraph on the karma nakshatra names only Saturn."
)

#: **Finding.** Example 117 gives a date and no time, and it does not need
#: one: Mars, Saturn, Rahu and Ketu hold their constellations through the
#: whole of 22 November 1989, so every claim it makes is fixed by the date
#: alone. The **Moon** is not: it crosses from Poorva Phalguni into Uttara
#: Phalguni that morning, and the example cites it nowhere.
THE_UNDATED_HOUR_TOUCHES_NOTHING_THE_EXAMPLE_CLAIMS = (
    "The four grahas Example 117 names are slow enough that the date settles "
    "their constellations. The Moon changes nakshatra during the day and the "
    "example does not use the Moon."
)


def strike(square: str, nakshatra: str) -> dict:
    """Whether a graha in `nakshatra` bears on `square`, and how.

    §26.8 states the reading in terms of vedha; Example 117 counts a graha
    **standing in** the square as well — see `OCCUPATION_COUNTS_AS_WELL_AS_
    VEDHA`. The two are reported separately, because the section never says
    they weigh the same.

    :returns: ``{"square", "nakshatra", "kind", "obstructs"}`` where ``kind``
        is ``"occupation"``, ``"vedha"`` or ``None``.
    """
    target, from_ = str(square), str(nakshatra)
    find(target)
    obstructs = vedha_lines(*find(from_))["obstructs"]
    if target == from_:
        kind = "occupation"
    elif target in obstructs:
        kind = "vedha"
    else:
        kind = None
    return {"square": target, "nakshatra": from_, "kind": kind,
            "obstructs": obstructs}
