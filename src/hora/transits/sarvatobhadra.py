"""§26.8 — the Sarvatobhadra chakra, a 9 x 9 grid of 81 squares.

Figure 3 as printed, cell by cell. The grid holds four kinds of thing: 28
nakshatras round the border, 12 rasis and 20 consonants inside it, 16 vowels
on the two diagonals, and 5 squares of tithis and weekdays at the centre. The
section's own arithmetic — 16 + 20 + 12 + 28 + 5 = 81 — is the check on the
transcription, and it is asserted rather than trusted.

One cell is **not** transcribed. See `UNCERTAIN_CELL`: the printed glyph at
row 2, column 7 reads to us as a vowel, and both the section's arithmetic and
its own rule about the diagonals say it must be a consonant. Rather than guess
a letter it is left as ``None`` and the count is checked around it.
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

#: **The one cell we do not transcribe.** Row 2, column 7 of Figure 3 reads to
#: us as the vowel "a", but it lies on neither diagonal, and the section says
#: the diagonals hold the vowels. Counting it as a vowel also gives 17 vowels
#: and 19 consonants, against the section's own 16 and 20. Both constraints
#: say it is a **consonant**; which consonant, we will not guess.
UNCERTAIN_CELL = (2, 7)

UNCERTAIN_CELL_NOTE = (
    "Figure 3's square at row 2, column 7 is left untranscribed. Our reading "
    "of the glyph is a vowel, and it is off both diagonals; the section's "
    "arithmetic and its diagonal rule both require a consonant there. The "
    "letter is not guessed."
)

#: Figure 3, row by row from NORTH, column by column from WEST. `None` marks
#: `UNCERTAIN_CELL`.
FIGURE_3: tuple[tuple[str | None, ...], ...] = (
    ("ee", "Dhanishtha", "Satabhisha", "P.Bhadra", "U.Bhadra", "Revati",
     "Aswini", "Bharani", "a"),
    ("Sravana", "rii", "g", "s", "d", "ch", "l", "u", "Krittika"),
    ("Abhijit", "kh", "ai", "Aq", "Pi", "Ar", "lu", None, "Rohini"),
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


def cell(row: int, column: int) -> str | None:
    """One square of Figure 3, or ``None`` for `UNCERTAIN_CELL`."""
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
