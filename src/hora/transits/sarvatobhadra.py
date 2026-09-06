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

#: **Finding.** The vedha rule is stated and not yet usable. "One vertical
#: **or** horizontal line" does not say which of the two a given nakshatra
#: takes, and "two crossward lines" does not say whether they are the grid's
#: diagonals through the square or something else. No lines are computed until
#: a worked case fixes the reading — see OI-146.
THE_VEDHA_LINES_ARE_NOT_DETERMINED = (
    "Section 26.8 says a planet obstructs three lines from its nakshatra: "
    "one vertical or horizontal, and two crossward. Which of vertical and "
    "horizontal a given border square takes is not stated, so the lines are "
    "not drawn."
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
