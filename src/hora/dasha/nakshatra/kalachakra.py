"""Chapter 24 — Kalachakra dasa, the wheel of Time.

The last of Part 2's nine, and the only one whose periods are rasis chosen by
the **Moon's nakshatra pada** rather than by a house. Parasara calls it "the
most respectable of all dasa systems".

Its machinery is four printed tables, and three of them are redundant: Table
43's two 24-rasi wheels generate all sixteen pada sequences of Tables 44 to 47,
and Table 48's dasa years reproduce all sixteen paramayush figures. Both are
derived here and checked against the print rather than transcribed, so a typo
in either place shows up as a failing test.

What is *not* derivable is which sub-group a nakshatra belongs to. Those lists
are held as printed, and §24.2's savya lists are one nakshatra short — see
:data:`SAVYA_SUB_GROUPS_LOSE_A_NAKSHATRA`.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    RASI_ABBR,
    RASI_LORD,
    RASI_NAMES,
    Graha,
)


class KalachakraError(validate.InputError):
    """A Kalachakra input that cannot be resolved."""


_RASI = {abbr: index for index, abbr in enumerate(RASI_ABBR)}


# --------------------------------------------------------------------------
# §24.1 Introduction
# --------------------------------------------------------------------------

#: Parasara's half-verse, as §24.1 prints it in Devanagari.
PARASARA_VERSE = "कालचक्रदशा चान्या मान्या सर्वदशासु या"

#: §24.1's translation, and the strongest claim made for any dasa in the book.
#: Chapter 22 said Niryaana Shoola dasa was "the best for timing death"; this
#: is Parasara's own, and unrestricted.
PARASARA_VERSE_MEANS = (
    "There is another dasa called Kalachakra dasa, which is the most "
    "respectable of all dasa systems."
)

KALACHAKRA_MEANS = (
    "Kalachakra literally means \"the wheel of Time\". It shows how the wheel "
    "of time unfolds events in the life of an individual."
)

#: Its provenance, which §24.1 gives before any rule.
SHIVA_EXPLAINED_IT_TO_PARVATI = (
    "Parasara said that Lord Shiva explained this dasa to Goddess Parvati."
)


# --------------------------------------------------------------------------
# §24.2 Table 42 — the two nakshatra groups
# --------------------------------------------------------------------------

SAVYA_MEANS = "zodiacal"
APASAVYA_MEANS = "anti-zodiacal"

#: §24.2's rule for Table 42, which is the whole table in one sentence.
GROUPING_RULE = (
    "Note that the first 3 nakshatras belong to the savya group, the next 3 "
    "constellations to the apasavya group and so on."
)

#: Table 42 as printed, nakshatra numbers 1-based, for checking the rule.
TABLE_42_SAVYA: tuple[int, ...] = (
    1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21, 25, 26, 27)
TABLE_42_APASAVYA: tuple[int, ...] = (
    4, 5, 6, 10, 11, 12, 16, 17, 18, 22, 23, 24)


def is_savya(nakshatra: int) -> bool:
    """Whether a nakshatra is savya, from §24.2's alternating-triples rule.

    :param nakshatra: 1 to 27.
    """
    index = validate.in_range("nakshatra", nakshatra, 1, 27)
    return ((index - 1) // 3) % 2 == 0


def group_of(nakshatra: int) -> str:
    """``"savya"`` or ``"apasavya"``."""
    return "savya" if is_savya(nakshatra) else "apasavya"


# --------------------------------------------------------------------------
# §24.2 Table 43 — the two wheels
# --------------------------------------------------------------------------

#: §24.2's mirror rule, which builds the second row of each half of Table 43.
MIRROR_RULE = (
    "In the other set, we write their mirror images, i.e. the other sign "
    "owned by the same planet. The mirror image of Ar is Sc. The mirror image "
    "of Ta is Li. The mirror image of Cp is Aq. However, the mirror image of "
    "Cn is Cn itself and that of Le is Le itself, as they are the only signs "
    "owned by their lords."
)


def mirror(rasi: int) -> int:
    """The other rasi owned by the same graha; Cancer and Leo mirror to
    themselves, being their lords' only signs."""
    index = validate.in_range("rasi", rasi, 0, 11)
    lord = int(RASI_LORD[index])
    others = [r for r in range(12) if int(RASI_LORD[r]) == lord and r != index]
    return others[0] if others else index


#: Table 43's four rows, keyed by group and row name. The **main** row is
#: zodiacal from Aries for savya and anti-zodiacal from Pisces for apasavya;
#: the mirrored row is :func:`mirror` applied to it.
def _main_row(group: str) -> tuple[int, ...]:
    if group == "savya":
        return tuple(range(12))
    return tuple((11 - step) % 12 for step in range(12))


#: **Finding.** Table 43 prints Main above Mirrored for savya and Mirrored
#: above Main for apasavya, and that printed order *is* the reading order: the
#: savya wheel runs main-then-mirrored and the apasavya wheel
#: mirrored-then-main. §24.2 never says so; the pada sequences of Tables 44 to
#: 47 only come out with the rows read in the order they are printed.
THE_ROW_ORDER_IN_TABLE_43_IS_THE_READING_ORDER = (
    "Table 43 prints the savya group as Main then Mirrored and the apasavya "
    "group as Mirrored then Main. Concatenated in that printed order, the two "
    "wheels generate every pada sequence in Tables 44 to 47; concatenated the "
    "other way round, neither does."
)


def wheel(group: str) -> tuple[int, ...]:
    """One group's 24-rasi wheel — "the main sequence and the mirrored
    sequence together form a sequence of 24 rasis"."""
    if group not in ("savya", "apasavya"):
        raise KalachakraError(
            f"group must be 'savya' or 'apasavya', got {group!r}")
    main = _main_row(group)
    mirrored = tuple(mirror(rasi) for rasi in main)
    return main + mirrored if group == "savya" else mirrored + main


# --------------------------------------------------------------------------
# §24.2 Tables 44 to 47 — nine rasis per nakshatra pada
# --------------------------------------------------------------------------

#: A sub-group's offset into its wheel. Consecutive nakshatras of one group
#: consume 36 wheel positions — four padas of nine — and 36 mod 24 is 12, which
#: is why there are exactly two sub-groups and why they sit half a wheel apart.
SUB_GROUP_OFFSET = {1: 0, 2: 12}

#: The nakshatras each table names, exactly as printed.
PRINTED_SUB_GROUPS: dict[str, tuple[int, ...]] = {
    # Table 44: Aswini, Krittika, Punarvasu, Aasresha, Hasta, Swaati, Moola,
    # Uttarashadha, Poorvabhadrapada
    "savya-1": (1, 3, 7, 9, 13, 15, 19, 21, 25),
    # Table 45: Bharani, Pushyami, Chitra, Poorvashadha, Revati
    "savya-2": (2, 8, 14, 20, 27),
    # Table 46: Rohini, Makha, Visakha, Sravanam
    "apasavya-1": (4, 10, 16, 22),
    # Table 47: Mrigasira, Ardra, Poorvaphalguni, Uttaraphalguni, Anuradha,
    # Jyeshtha, Dhanishtha, Satabhisha
    "apasavya-2": (5, 6, 11, 12, 17, 18, 23, 24),
}

#: **Book defect.** Table 42 puts fifteen nakshatras in the savya group and
#: Tables 44 and 45 between them name **fourteen**. Uttarabhadrapada (26)
#: appears in neither. The apasavya tables are complete: four plus eight is
#: twelve. See D-67.
SAVYA_SUB_GROUPS_LOSE_A_NAKSHATRA = (
    "Table 42's savya group holds fifteen nakshatras. Table 44 names nine and "
    "Table 45 names five, and Uttarabhadrapada is in neither."
)

#: **Gap.** Which sub-group Uttarabhadrapada belongs to cannot be read off the
#: other three tables, because savya and apasavya are grouped on different
#: patterns: savya-1 takes the 1st and 3rd of each triple and savya-2 the 2nd,
#: while apasavya-1 takes only the 1st and apasavya-2 the 2nd and 3rd. The
#: savya pattern would put Uttarabhadrapada in savya-2 and move Revati to
#: savya-1, which is not what Table 45 prints. See OI-139.
THE_SUB_GROUP_PATTERNS_DISAGREE = (
    "Savya-1 holds the 1st and 3rd nakshatra of each savya triple and savya-2 "
    "the 2nd, except that Table 45 prints Revati, the 3rd of its triple. "
    "Apasavya-1 holds only the 1st of each triple and apasavya-2 the 2nd and "
    "3rd. No single rule produces both."
)


def sub_group_of(nakshatra: int) -> int:
    """Which sub-group a nakshatra is in, from Tables 44 to 47 as printed.

    :raises KalachakraError: for Uttarabhadrapada, which no table names. See
        D-67 and OI-139 — the sub-group decides the whole dasa, so guessing
        one would decide it silently.
    """
    index = validate.in_range("nakshatra", nakshatra, 1, 27)
    group = group_of(index)
    for sub in (1, 2):
        if index in PRINTED_SUB_GROUPS[f"{group}-{sub}"]:
            return sub
    raise KalachakraError(
        f"nakshatra {index} is in Table 42's {group} group but in neither of "
        f"its sub-group tables, so its 9-rasi sequences are unknown; "
        f"see D-67")


def pada_sequence(group: str, sub_group: int, pada: int) -> tuple[int, ...]:
    """The nine rasis of one nakshatra pada, from the wheel.

    :param sub_group: 1 or 2.
    :param pada: 1 to 4.

    Tables 44 to 47 are this function's output; they are checked against it
    rather than stored.
    """
    if sub_group not in SUB_GROUP_OFFSET:
        raise KalachakraError(
            f"sub_group must be 1 or 2, got {sub_group!r}")
    validate.in_range("pada", pada, 1, 4)
    ring = wheel(group)
    start = SUB_GROUP_OFFSET[sub_group] + (pada - 1) * 9
    return tuple(ring[(start + step) % 24] for step in range(9))


# --------------------------------------------------------------------------
# §24.2 Table 48 — dasa years, and the paramayush
# --------------------------------------------------------------------------

#: Table 48. "The duration of a dasa is based in its owner... Two rasis owned
#: by the same planet have the same duration."
DASA_YEARS_BY_LORD: dict[int, int] = {
    int(Graha.SUN): 5, int(Graha.MOON): 21, int(Graha.MARS): 7,
    int(Graha.MERCURY): 9, int(Graha.JUPITER): 10, int(Graha.VENUS): 16,
    int(Graha.SATURN): 4,
}


def dasa_years(rasi: int) -> int:
    """A rasi's dasa length, from its lord alone."""
    index = validate.in_range("rasi", rasi, 0, 11)
    return DASA_YEARS_BY_LORD[int(RASI_LORD[index])]


def paramayush(sequence: tuple[int, ...]) -> int:
    """"The sum of the dasas of the nine rasis associated with the
    constellation quarter." Tables 44 to 47's last column."""
    if len(sequence) != 9:
        raise KalachakraError(
            f"a nakshatra pada has nine rasis, got {len(sequence)}")
    return sum(dasa_years(rasi) for rasi in sequence)


#: **Finding.** The sixteen paramayush figures are four values — 100, 85, 83
#: and 86 — in one order for savya and the reverse for apasavya. They total
#: 354 either way, and every one is the plain sum of its nine rasis' Table 48
#: years, so the column is a check on the sequences rather than new data.
PARAMAYUSH_IS_FOUR_VALUES_READ_TWO_WAYS = (
    "Savya padas 1 to 4 give 100, 85, 83 and 86 years; apasavya padas 1 to 4 "
    "give 86, 83, 85 and 100 — the same four figures reversed. Each is the sum "
    "of its pada's nine Table 48 dasa lengths."
)


# --------------------------------------------------------------------------
# §24.2's Deha and Jeeva rasis
# --------------------------------------------------------------------------

#: The definition, and the reversal §24.2 flags itself.
DEHA_AND_JEEVA_RULE = (
    "The first of the nine rasis is called \"Deha rasi\" (body sign) and the "
    "last one is called \"Jeeva rasi\" (spirit/life sign). ... In the case of "
    "apasavya nakshatras, the first rasi in the nine rasis corresponding to a "
    "nakshatra pada is called \"Jeeva rasi\" and the last one is called \"Deha "
    "rasi\" (note that the definition has reversed)."
)


def deha_and_jeeva(group: str, sequence: tuple[int, ...]) -> dict:
    """Which end of a pada's nine rasis is the body and which the life.

    Savya takes the first as Deha; apasavya reverses it, which §24.2 points
    out in its own parenthesis.
    """
    if group not in ("savya", "apasavya"):
        raise KalachakraError(
            f"group must be 'savya' or 'apasavya', got {group!r}")
    if len(sequence) != 9:
        raise KalachakraError(
            f"a nakshatra pada has nine rasis, got {len(sequence)}")
    first, last = sequence[0], sequence[-1]
    deha, jeeva = (first, last) if group == "savya" else (last, first)
    return {
        "group": group,
        "deha": deha, "deha_rasi": str(RASI_NAMES[deha]),
        "jeeva": jeeva, "jeeva_rasi": str(RASI_NAMES[jeeva]),
        "reversed": group == "apasavya",
    }


# --------------------------------------------------------------------------
# §24.2's five-step procedure
# --------------------------------------------------------------------------

#: The procedure, verbatim and numbered as §24.2 numbers it.
PROCEDURE: tuple[str, ...] = (
    ("Find the nakshatra pada occupied by natal Moon. Identify the 9-rasi "
     "sequence associated with it, using Table 44-Table 47. Also, note down "
     "the paramayush."),
    "Find the fraction of the nakshatra pada that was covered by Moon at birth.",
    ("Find the same fraction of the paramayush. That represents the portion "
     "of the paramayush (dasas of the nine rasis) that was over before birth. "
     "Based on this, we can find which of the nine dasas runs at birth and "
     "how much of the dasa remains at birth."),
    ("After this dasa, we go to the next rasi in the nine rasis. When we "
     "finish the nine rasis of the nakshatra pada, we go to the nine rasis of "
     "the next nakshatra pada. After the nine rasis of the 4th pada of a "
     "nakshatra, we go to the nine rasis corresponding to the 1st pada of the "
     "next nakshatra (i.e. 1st pada of the constellations belonging to the "
     "other sub-group in the same group). For example, after the nine rasis "
     "of the 4th pada of Savya-1 constellations, we go to the nine rasis of "
     "the 1st pada of Savya-2 constellations. After the nine rasis of the 4th "
     "pada of Apasavya-2 constellations, we go to the nine rasis of the 1st "
     "pada of Apasavya-1 constellations."),
    ("In each dasa, antardasas start from dasa rasi itself. After the first "
     "antardasa, we go to the next rasi. ... We take 9 rasis starting from "
     "dasa rasi and antardasas will belong to those rasis. We distribute the "
     "dasa length among the 9 antardasas proportionally (in proportion to "
     "their respective dasa lengths as given in Table 48). If we reach the "
     "end of the nine rasis corresponding to the nakshatra pada when counting "
     "9 rasis from dasa rasi, we proceed to the next nakshatra pada as "
     "described in rule (4) above."),
)


def pada_of(moon_longitude: float) -> dict:
    """§24.2 step 1 and step 2 — the Moon's nakshatra pada and how far into it.

    :returns: the nakshatra (1-27), its group, the pada (1-4) and the elapsed
        fraction of that pada.
    """
    from hora.core.constants.nakshatra import NAKSHATRA_SPAN, PADA_SPAN

    longitude = validate.longitude("moon_longitude", moon_longitude)
    nakshatra = int(longitude // NAKSHATRA_SPAN) + 1
    into_nakshatra = longitude - (nakshatra - 1) * NAKSHATRA_SPAN
    pada = int(into_nakshatra // PADA_SPAN) + 1
    elapsed = (into_nakshatra - (pada - 1) * PADA_SPAN) / PADA_SPAN
    return {
        "nakshatra": nakshatra,
        "group": group_of(nakshatra),
        "pada": pada,
        "elapsed_fraction": elapsed,
    }


def first_dasa(sequence: tuple[int, ...], elapsed_fraction: float) -> dict:
    """§24.2 step 3 — which of the nine runs at birth, and what is left of it.

    "Find the same fraction of the paramayush. That represents the portion of
    the paramayush that was over before birth."
    """
    if len(sequence) != 9:
        raise KalachakraError(
            f"a nakshatra pada has nine rasis, got {len(sequence)}")
    fraction = float(elapsed_fraction)
    if not 0.0 <= fraction <= 1.0:
        raise KalachakraError(
            f"elapsed_fraction must be between 0 and 1, got {fraction}")
    total = paramayush(sequence)
    consumed = fraction * total

    running = 0.0
    for position, rasi in enumerate(sequence):
        length = dasa_years(rasi)
        if consumed < running + length or position == 8:
            return {
                "position": position,
                "sign": rasi, "rasi": str(RASI_NAMES[rasi]),
                "years": length,
                "elapsed_years": consumed - running,
                "balance_years": running + length - consumed,
                "paramayush": total,
                "consumed_years": consumed,
            }
        running += length
    raise AssertionError  # pragma: no cover - the loop always returns


#: **Finding.** Rule (4) reads as three cases — next rasi, next pada, next
#: nakshatra's first pada in the other sub-group — and it is one: **walk the
#: 24-rasi wheel a step at a time, for ever**. A pada is nine consecutive
#: positions, a nakshatra's four padas are thirty-six, and thirty-six is a
#: whole wheel and a half, which lands the next nakshatra on the other
#: sub-group by itself. §24.2 says as much in passing — "we find antardasas
#: and dasas by repeating these 24-rasi sequences and going through them" —
#: and then states the rule the long way.
RULE_4_IS_JUST_WALKING_THE_WHEEL = (
    "We find antardasas and dasas by repeating these 24-rasi sequences and "
    "going through them."
)

#: Example 97 states it outright, for dasas and antardasas together, and names
#: the only difference between them — where the walk starts.
EXAMPLE_97_SAYS_THE_WHEEL_IS_THE_WHOLE_MACHINERY = (
    "One can notice that dasa sequences and antardasa sequences all come from "
    "the two 24-rasi sequences given in Kalachakra (see Table 43). In the "
    "cases of dasas, the starting point in the 24-rasi sequence is determined "
    "by the nakshatra pada of Moon and the portion elapsed in it. In the case "
    "of antardasas, the starting point is based on dasa rasi."
)

#: Footnote 66, on the dasa running at birth: its antardasas are laid out over
#: the **whole** dasa, not over the balance, so the earliest of them fall
#: before birth. See :func:`first_antardasa`.
FOOTNOTE_66 = (
    "However, we see from Example 95 that 2.25 years of Sc dasa were over "
    "before birth. So some of these antardasas may be over before birth."
)

#: **Finding.** Footnote 66 settles a question §24.2's rule (5) leaves open —
#: whether the first dasa's antardasas divide its full length or the balance
#: remaining at birth. They divide the full length, and the answer is visible
#: only because the book says some of them are already over.
THE_FIRST_DASAS_ANTARDASAS_DIVIDE_ITS_WHOLE_LENGTH = (
    "The dasa running at birth has its nine antardasas laid out across the "
    "whole dasa, so those falling in the elapsed part are over before birth. "
    "They are not a proportional division of the balance."
)

#: **Caution.** Le dasa's nine antardasas sum to 86, which is also an apasavya
#: paramayush, and that is a coincidence of where they start. Nine consecutive
#: wheel positions sum to 72, 83, 85, 86, 88, 97 or 100; only the nine that
#: begin a pada are guaranteed to be a paramayush.
NINE_CONSECUTIVE_IS_NOT_ALWAYS_A_PARAMAYUSH = (
    "Nine consecutive rasis of a wheel total 72, 83, 85, 86, 88, 97 or 100 "
    "years depending on where they start. Only pada-aligned nines give the "
    "four paramayush figures."
)

#: Footnote 63, which supplies the denominator both examples divide by.
FOOTNOTE_63 = "The complete length of each nakshatra pada is 3\u00b020'."

#: Footnote 64 — why the examples list the number of dasas they do.
FOOTNOTE_64 = (
    "Parasara suggested taking the dasas of nine rasis starting from the rasi "
    "whose dasa is running at birth. Sc dasa was running at birth and Sc and "
    "Li dasas belong to the set of nine rasis associated with Rohini 2nd "
    "pada. We already have 2 rasis. So we just need 7 rasis from the next "
    "pada."
)

#: Footnote 65, which is §16.2's controversy again and settles it the same
#: way, this time naming Kalachakra. Evidence for OI-115, not a new question.
FOOTNOTE_65 = (
    "We again have the issue of solar years vs savana years. This author "
    "prefers savana years with all nakshatra dasas. Kalachakra dasa is a "
    "nakshatra dasa."
)

#: **Finding.** Footnote 64 gives the rule behind a count no worked example
#: states: a Kalachakra dasa is displayed as **nine** rasis beginning with the
#: one running at birth, so the number taken from the following pada is the
#: dasa's own 0-based position in its pada. Example 95's Sc sits 8th, leaving
#: Sc and Li, and lists 7; Example 96's Pi sits 9th, leaving Pi alone, and
#: lists 8. It is a display convention, not a boundary: the wheel runs on past
#: nine either way, and Exercise 34 does — see
#: :data:`EXERCISE_34_PRINTS_A_TENTH_DASA`.
THE_LISTED_COUNT_IS_NINE_LESS_WHAT_THE_PADA_STILL_HOLDS = (
    "The dasas an example lists after the one running at birth number nine "
    "less the rasis that pada still holds, counting the running dasa itself. "
    "Position 7 of 0-8 lists seven, position 8 lists eight."
)

#: **Book defect.** Exercise 34's Gemini sits 7th of its pada, leaving three,
#: so footnote 64 gives six from the next pada and nine in all. The answer
#: prints **seven and ten**, running to age 85 where the rule stops at 76.
#: Nothing printed is wrong -- the tenth is the next rasi on the wheel with its
#: Table 48 length -- and no other reading of "nine rasis" reaches ten, the ten
#: holding only seven distinct rasis. See D-68.
EXERCISE_34_PRINTS_A_TENTH_DASA = (
    "Exercise 34 lists ten dasas from birth where footnote 64's nine-rasi "
    "convention gives nine. The count departs from the convention; the dasas "
    "themselves are the wheel's own next ten."
)

#: **Finding.** Example 96 converts a balance of 8.6 years to "8 years 7
#: months 6 days", and that conversion does **not** separate OI-115's year
#: lengths. Savana gives 216 days exactly; 365.25 gives 219.15, which is 7
#: months 6.09 days at that year's own twelfth. Both print the same. Only
#: footnote 65's plain statement decides it.
EXAMPLE_96S_MONTHS_AND_DAYS_DECIDE_NOTHING = (
    "8.6 years prints as 8 years 7 months 6 days under a 360-day year and "
    "under a 365.25-day year alike, months being a twelfth of whichever year."
)


def wheel_position(nakshatra: int, pada: int) -> int:
    """Where a nakshatra pada starts on its group's wheel.

    :raises KalachakraError: through :func:`sub_group_of` for a nakshatra no
        table names.
    """
    validate.in_range("pada", pada, 1, 4)
    sub = sub_group_of(nakshatra)
    return (SUB_GROUP_OFFSET[sub] + (pada - 1) * 9) % 24


def dasa_order(nakshatra: int, pada: int, count: int,
               skip: int = 0) -> tuple[dict, ...]:
    """§24.2 rule (4) — successive dasas from a nakshatra pada.

    :param count: how many to return.
    :param skip: how many to pass over first, for starting mid-pada at the
        dasa running at birth.

    One walk of the wheel covers all three of rule (4)'s cases; see
    :data:`RULE_4_IS_JUST_WALKING_THE_WHEEL`.
    """
    if count < 1:
        raise KalachakraError(f"count must be positive, got {count}")
    if skip < 0:
        raise KalachakraError(f"skip cannot be negative, got {skip}")
    ring = wheel(group_of(nakshatra))
    start = wheel_position(nakshatra, pada) + skip
    return tuple({
        "position": (start + step) % 24,
        "sign": ring[(start + step) % 24],
        "rasi": str(RASI_NAMES[ring[(start + step) % 24]]),
        "years": dasa_years(ring[(start + step) % 24]),
    } for step in range(count))


def first_antardasa(rows: tuple[dict, ...], elapsed_years: float) -> dict:
    """Footnote 66 — which antardasa of the dasa running at birth is itself
    running, once the elapsed part of that dasa is taken off.

    :param rows: :func:`antardasas` for the dasa, laid out over its **whole**
        length; see :data:`THE_FIRST_DASAS_ANTARDASAS_DIVIDE_ITS_WHOLE_LENGTH`.
    :param elapsed_years: the part of the dasa over before birth, which
        :func:`first_dasa` reports as ``elapsed_years``.
    """
    if not rows:
        raise KalachakraError("antardasas cannot be empty")
    elapsed = float(elapsed_years)
    if elapsed < 0:
        raise KalachakraError(
            f"elapsed_years cannot be negative, got {elapsed}")
    total = sum(float(row["years"]) for row in rows)
    if elapsed > total:
        raise KalachakraError(
            f"elapsed_years {elapsed} exceeds the dasa's {total}")

    running = 0.0
    for position, row in enumerate(rows):
        length = float(row["years"])
        if elapsed < running + length or position == len(rows) - 1:
            return {
                "index": position,
                "over_before_birth": position,
                "sign": row["sign"], "rasi": row["rasi"],
                "years": length,
                "elapsed_years": elapsed - running,
                "balance_years": running + length - elapsed,
            }
        running += length
    raise AssertionError  # pragma: no cover - the loop always returns


def nine_from_birth(nakshatra: int, pada: int, position: int) -> dict:
    """Footnote 64 — the nine dasas an example displays, from birth onwards.

    :param position: the 0-based position within its pada of the dasa running
        at birth, as :func:`first_dasa` reports it.

    "Parasara suggested taking the dasas of nine rasis starting from the rasi
    whose dasa is running at birth." The split between the two padas is
    reported because both examples state it; see
    :data:`THE_LISTED_COUNT_IS_NINE_LESS_WHAT_THE_PADA_STILL_HOLDS`.
    """
    index = validate.in_range("position", position, 0, 8)
    return {
        "dasas": dasa_order(nakshatra, pada, 9, skip=index),
        "from_this_pada": 9 - index,
        "from_next_pada": index,
    }


def antardasas(nakshatra: int, wheel_index: int,
               dasa_length_years: float) -> tuple[dict, ...]:
    """§24.2 rule (5) — nine antardasas from the dasa rasi, proportionally.

    :param wheel_index: the dasa's own position on its group's wheel.
    :param dasa_length_years: the dasa's length, which the nine share out in
        proportion to their own Table 48 lengths.

    "If we reach the end of the nine rasis corresponding to the nakshatra pada
    when counting 9 rasis from dasa rasi, we proceed to the next nakshatra
    pada" — which the wheel does on its own.
    """
    ring = wheel(group_of(nakshatra))
    start = validate.in_range("wheel_index", wheel_index, 0, 23)
    length = float(dasa_length_years)
    if length <= 0:
        raise KalachakraError(
            f"dasa_length_years must be positive, got {length}")

    nine = [ring[(start + step) % 24] for step in range(9)]
    total = sum(dasa_years(rasi) for rasi in nine)
    return tuple({
        "position": (start + step) % 24,
        "sign": rasi, "rasi": str(RASI_NAMES[rasi]),
        "share_years": dasa_years(rasi),
        "years": length * dasa_years(rasi) / total,
    } for step, rasi in enumerate(nine))


# --------------------------------------------------------------------------
# §24.3.1 Interpretation — basics
# --------------------------------------------------------------------------

#: The first and weakest rule: the rasi's own nature.
NATURAL_RESULTS_RULE = (
    "Dasa of a rasi gives the natural results of the rasi. For example, dasa "
    "of Pisces may give saattwik religious activities. Dasa of Aries may give "
    "enterprise or quarrels or wounds."
)

#: The rule §24.3.1 itself calls more important, and the reason Kalachakra is
#: read across the vargas rather than in the rasi chart alone.
HOUSE_AND_PLANETS_RULE = (
    "More importantly, dasa of a rasi gives the results of the house and "
    "planets in that rasi."
)

#: And the third, which reads the lord wherever it sits.
LORD_RULE = "Dasa of a rasi may also give the results of its lord."

#: §24.3.1's own illustrations, each naming the divisional chart it reads in.
#: ``holds`` is what the dasa rasi carries in that varga; ``gives`` is the
#: result. Held as data because every one names a different varga, which is
#: the point being made.
BASICS_EXAMPLES: tuple[dict[str, str], ...] = (
    {"rasi": "Aries", "varga": "D7", "holds": "the 5th house",
     "gives": "children", "rule": "house"},
    {"rasi": "Pisces", "varga": "D6", "holds": "the 8th house",
     "gives": "diseases", "rule": "house"},
    {"rasi": "Gemini", "varga": "D24", "holds": "lagna",
     "gives": "all-round progress in the accumulation of knowledge",
     "rule": "house"},
    {"rasi": "Scorpio", "varga": "D10", "holds": "AL, with its lord Mars in it",
     "gives": "good developments related to career and status",
     "rule": "house-and-planet"},
    {"rasi": "any", "varga": "D10", "holds": "the 8th from AL",
     "gives": "a fall in status at workplace", "rule": "house"},
    {"rasi": "Aries", "varga": "D7", "holds": "its lord Mars in the 5th house",
     "gives": "children", "rule": "lord"},
)

#: **Gap.** §24.3.1's "the 8th from AL in D-10" carries no pointer to Table 32,
#: where §23.3's did — Example 92 sent the reader there in as many words. Read
#: as the ordinary 8th house from AL, which is what an unqualified "8th from"
#: means everywhere else in the book. See OI-140.
THE_EIGHTH_FROM_AL_HERE_IS_UNQUALIFIED = (
    "§24.3.1 says \"the 8th from AL in D-10\" with no reference to Table 32, "
    "unlike §23.3, which Example 92 sent to Table 32 explicitly. Taken as the "
    "ordinary 8th."
)

#: §24.3.1's fourth rule, and the only one with a number in it.
SAV_RULE = (
    "Samudaaya Ashtakavarga (SAV) plays an important role in deciding the "
    "results in a dasa. If a rasi has too many or too few rekhas in SAV of a "
    "particular divisional chart, then its dasa may bring favorable or "
    "unfavorable results, respectively, relating to the significations of that "
    "house in that divisional chart."
)

#: "Usually dasas of rasis with 30 or more rekhas in D-10 SAV bring the best
#: phases in one's career and dasas of rasis with 30 or more rekhas in D-24 SAV
#: bring the best periods for learning."
SAV_STRONG_REKHAS = 30

SAV_THRESHOLD_READINGS: tuple[dict[str, str | int], ...] = (
    {"varga": "D10", "rekhas": SAV_STRONG_REKHAS,
     "reading": "the best phases in one's career", "hedge": "usually"},
    {"varga": "D24", "rekhas": SAV_STRONG_REKHAS,
     "reading": "the best periods for learning", "hedge": "usually"},
)

#: The section's closing instruction, which is why the readings above are held
#: per-varga rather than folded into one.
KEEP_SAV_OF_VARIOUS_VARGAS = (
    "One should keep SAV of various divisional charts with one when "
    "interpreting Kalachakra dasa."
)


# --------------------------------------------------------------------------
# §24.3.2 Deha and Jeeva rasis, as the dasas give them
# --------------------------------------------------------------------------

#: §24.3.2's correction to Tables 44 to 47, and the reason footnote 64's
#: nine-rasi set matters: its two ends *are* deha and jeeva.
TABLE_DEHA_AND_JEEVA_ASSUME_BIRTH_AT_THE_PADA_START = (
    "In Table 44-Table 47, we listed the deha and jeeva rasis of different "
    "nakshatra padas. However, these hold for one born at the beginning of the "
    "nakshatra pada. One can have different deha and jeeva rasis based on the "
    "elapsed portion in the nakshatra pada."
)

#: §24.3.2's boxed rule, which is the general case.
DEHA_AND_JEEVA_FROM_THE_DASAS = (
    "Deha and jeeva rasis are simply the rasis of the first and the ninth "
    "dasas in the case of one born in a savya nakshatra. In the case of one "
    "born in an apasavya nakshatra, deha and jeeva rasis are the rasis of the "
    "ninth and the first dasas."
)


def deha_and_jeeva_at_birth(nakshatra: int, pada: int, position: int) -> dict:
    """§24.3.2 — deha and jeeva from the dasas actually run, not from the table.

    :param position: the 0-based position within its pada of the dasa running
        at birth, as :func:`first_dasa` reports it.

    At ``position`` 0 this reduces to :func:`deha_and_jeeva` on the pada's own
    nine, which is what Tables 44 to 47 print; anywhere else it does not.
    """
    nine = nine_from_birth(nakshatra, pada, position)["dasas"]
    group = group_of(nakshatra)
    first, ninth = nine[0]["sign"], nine[-1]["sign"]
    deha, jeeva = (first, ninth) if group == "savya" else (ninth, first)
    return {
        "group": group,
        "deha": deha, "deha_rasi": str(RASI_NAMES[deha]),
        "jeeva": jeeva, "jeeva_rasi": str(RASI_NAMES[jeeva]),
        "first_dasa": first, "ninth_dasa": ninth,
        "from_the_table": position == 0,
    }


DEHA_SHOWS = "body"
JEEVA_SHOWS = "the spirit"

#: §24.3.2's transiting benefics, as it names them.
TRANSIT_BENEFICS: tuple[int, ...] = (
    int(Graha.JUPITER), int(Graha.MERCURY), int(Graha.VENUS))

#: And its malefics. **Ketu is not among them.** Recorded as printed; the
#: section names Rahu alone of the two nodes.
TRANSIT_MALEFICS: tuple[int, ...] = (
    int(Graha.MARS), int(Graha.SUN), int(Graha.SATURN), int(Graha.RAHU))

KETU_IS_NOT_IN_THE_TRANSIT_MALEFICS = (
    "§24.3.2 names Mars, Sun, Saturn and Rahu. Ketu is not in the list, and "
    "is not added to it here."
)

#: The three readings §24.3.2 gives, keyed by which rasi is transited and by
#: benefic or malefic. There are four such cells and the section fills three.
TRANSIT_READINGS: tuple[dict[str, str], ...] = (
    {"rasi": "jeeva", "grahas": "benefic",
     "reading": "one may exhibit a positive spirit and be cheerful"},
    {"rasi": "jeeva", "grahas": "malefic",
     "reading": "one may be without any enthusiasm"},
    {"rasi": "deha", "grahas": "malefic",
     "reading": "one may face accidents or death"},
)

#: **Gap.** Benefics transiting the deha rasi have no reading. The general
#: line — "Benefics and malefics transiting in them affect them positively and
#: negatively (respectively)" — would supply one, but §24.3.2 does not, and
#: the three it does give are specific in a way that line is not.
BENEFICS_IN_THE_DEHA_RASI_HAVE_NO_READING = (
    "§24.3.2 gives readings for benefics in jeeva, malefics in jeeva and "
    "malefics in deha. Benefics in deha is the fourth cell and is empty."
)


def transit_reading(rasi: str, graha: int) -> dict:
    """§24.3.2 — what a graha transiting the deha or jeeva rasi shows.

    :param rasi: ``"deha"`` or ``"jeeva"``.

    Returns ``undecided`` for a benefic in the deha rasi, which §24.3.2 leaves
    empty, and for a graha it classes as neither — Ketu and the Moon.
    """
    if rasi not in ("deha", "jeeva"):
        raise KalachakraError(
            f"rasi must be 'deha' or 'jeeva', got {rasi!r}")
    index = validate.in_range("graha", int(graha), 0, 8)

    kind = ("benefic" if index in TRANSIT_BENEFICS else
            "malefic" if index in TRANSIT_MALEFICS else None)
    if kind is None:
        return {
            "rasi": rasi, "graha": index, "kind": None, "reading": None,
            "undecided": (
                f"§24.3.2 lists neither {GRAHA_NAMES[index]!s} among its "
                f"benefics nor among its malefics"),
        }
    for row in TRANSIT_READINGS:
        if row["rasi"] == rasi and row["grahas"] == kind:
            return {"rasi": rasi, "graha": index, "kind": kind,
                    "reading": row["reading"], "undecided": None}
    return {
        "rasi": rasi, "graha": index, "kind": kind, "reading": None,
        "undecided": BENEFICS_IN_THE_DEHA_RASI_HAVE_NO_READING,
    }


# --------------------------------------------------------------------------
# §24.3.3 Gatis — the special movements
# --------------------------------------------------------------------------

#: What a gati is, and which rasi carries its name.
GATI_RULE = (
    "We see that dasas progress in a regular fashion in Kalachakra dasa. We "
    "either go as Ar, Ta, Ge etc or as Pi, Aq, Cp etc. However, some "
    "irregularities can be found. The rasis whose dasas come after an "
    "irregular leap go by special names and special results are attributed to "
    "those dasas in classics."
)

GATI_NAMES: dict[str, str] = {
    "simhaavalokana": "lion's leap",
    "markati": "monkey's leap",
    "mandooki": "frog's leap",
}

GATI_DEFINITIONS: dict[str, str] = {
    "simhaavalokana": (
        "A trinal leap (from Sg to Ar or vice versa; from Pi to Sc or vice "
        "versa)."),
    "markati": "Temporary reversal of the direction.",
    "mandooki": "Leaving one rasi and jumping over it.",
}

#: Footnote 67, which corrects the translation the section itself gives.
FOOTNOTE_67 = (
    "Simhavalokana doesn't really mean a lion. It strictly means a lion's "
    "view of the jungle from an elevated vantage point."
)


def _half_direction(ring: tuple[int, ...], half: int) -> int:
    """Which way a wheel's half runs, from its own single-rasi steps."""
    total = 0
    for index in range(half * 12, half * 12 + 11):
        step = (ring[index + 1] - ring[index]) % 12
        if step == 1:
            total += 1
        elif step == 11:
            total -= 1
    return 1 if total > 0 else -1


def transitions(group: str) -> tuple[dict, ...]:
    """Every step of a group's wheel, classified as regular or as one of
    §24.3.3's three gatis.

    The gatis are read off the wheel rather than transcribed: a trinal step is
    a lion's leap, a two-rasi step a frog's leap, and a single-rasi step
    against its half's own direction a monkey's leap. The named rasi is the
    step's destination — "the rasis whose dasas come after an irregular leap".
    """
    ring = wheel(group)
    direction = {half: _half_direction(ring, half) for half in (0, 1)}
    rows = []
    for index in range(24):
        origin, target = ring[index], ring[(index + 1) % 24]
        step = (target - origin) % 12
        if step in (4, 8):
            kind = "simhaavalokana"
        elif step in (2, 10):
            kind = "mandooki"
        elif step in (1, 11) and index % 12 != 11 and (
                (1 if step == 1 else -1) != direction[index // 12]):
            kind = "markati"
        elif step in (1, 11):
            kind = "regular"
        else:  # pragma: no cover - no other step occurs on either wheel
            raise KalachakraError(
                f"unclassifiable step of {step} rasis in the {group} wheel")
        rows.append({
            "position": index, "next_position": (index + 1) % 24,
            "from": origin, "from_rasi": str(RASI_NAMES[origin]),
            "to": target, "to_rasi": str(RASI_NAMES[target]),
            "step": step if step <= 6 else step - 12,
            "kind": kind,
        })
    return tuple(rows)


def gati_rasis(group: str) -> dict[str, tuple[int, ...]]:
    """The rasis §24.3.3 names for each gati, in wheel order.

    §24.3.3 names the markati and mandooki rasis of both groups outright; the
    simhaavalokana rasis it gives only as leaps, one direction falling on each
    wheel.
    """
    found: dict[str, list[int]] = {name: [] for name in GATI_NAMES}
    for row in transitions(group):
        if row["kind"] in found:
            found[row["kind"]].append(int(row["to"]))
    return {name: tuple(rasis) for name, rasis in found.items()}


#: Table 51, keyed by gati and group.
TABLE_51: dict[tuple[str, str], str] = {
    ("simhaavalokana", "savya"): (
        "Fear of animals, loss of friends, distress to near relations, fall "
        "in dungeons, danger from poison and weapons, fall from a vehicle, "
        "fever, destruction of house"),
    ("simhaavalokana", "apasavya"): "Death of father or elders, loss of position",
    ("markati", "savya"): (
        "Loss of wealth, agriculture and animals, death of father or elders"),
    ("markati", "apasavya"): (
        "Danger from water, distress to father, loss of position, anger of "
        "rulers, wandering in the forests"),
    ("mandooki", "savya"): (
        "Distress to relatives, elders and father, trouble from poison, "
        "weapons, enemies, thieves. In Le-to-Ge leap, death of mother or, "
        "death of native, trouble from rulers and diseases are possible."),
    ("mandooki", "apasavya"): (
        "Distress to wife, loss of children, fever, sickness and loss of "
        "position"),
}


def gati_results(kind: str, group: str) -> str:
    """One cell of Table 51."""
    if (kind, group) not in TABLE_51:
        raise KalachakraError(
            f"no Table 51 entry for {kind!r} in the {group!r} group")
    return TABLE_51[(kind, group)]


#: **Finding.** §19.4 defined mandooki gati as "the 3rd/11th jump" and pointed
#: forward to "Parasara's discussion on Kalachakra dasa" for it. This is that
#: discussion, and the wheel bears the definition out exactly: every savya
#: frog's leap is an **11th** and every apasavya one a **3rd**. The pointer is
#: answered; Mandooka dasa itself is still only named, never constructed.
MANDOOKI_IS_19_4S_THIRD_ELEVENTH_JUMP = (
    "§19.4's \"the 3rd/11th jump\" is this: the savya wheel's two frog's "
    "leaps, Vi to Cn and Le to Ge, are both 11ths, and the apasavya wheel's, "
    "Ge to Le and Cn to Vi, are both 3rds."
)

#: **Finding.** Table 51's savya frog cell is the only one that separates its
#: two leaps: the Le-to-Ge jump carries three results the Vi-to-Cn jump does
#: not. Every other cell reads for the gati as a whole.
MANDOOKI_SAVYA_SINGLES_OUT_THE_LE_TO_GE_LEAP = (
    "In Le-to-Ge leap, death of mother or, death of native, trouble from "
    "rulers and diseases are possible."
)

#: The scope Parasara's direction rules are given for, which is narrower than
#: Table 51's results.
DIRECTIONS_ARE_FOR_TRAVEL_AND_RELOCATION = (
    "In addition, Parasara listed the directions to prefer and the directions "
    "avoid, while travelling and relocating, during different leaps."
)

#: Parasara's seven direction rules, keyed by the transition they apply to.
#: Two are for *normal* movements rather than leaps, which is why they are
#: keyed by the step and not by the gati.
PARASARA_DIRECTIONS: tuple[dict, ...] = (
    {"from": "Vi", "to": "Cn", "prefer": ("east", "north"), "avoid": (),
     "says": ("In the leap from Vi to Cn, east will give great results. One "
              "can take up an auspicious journey in the northern direction.")},
    {"from": "Le", "to": "Ge", "prefer": ("southwest",), "avoid": ("east",),
     "says": ("In the leap from Le to Ge, east should be avoided. A journey "
              "to the southwest will be fruitful.")},
    {"from": "Cn", "to": "Le", "prefer": ("west",), "avoid": ("south",),
     "says": ("In the leap from Cn to Le, a move in the southern direction "
              "results in losses. West is favorable.")},
    {"from": "Pi", "to": "Sc", "prefer": (), "avoid": ("north",),
     "says": ("In the leap from Pi to Sc and in the normal movement from Sg "
              "to Cp, there will be troubles in the northern direction.")},
    {"from": "Sg", "to": "Cp", "prefer": (), "avoid": ("north",),
     "says": ("In the leap from Pi to Sc and in the normal movement from Sg "
              "to Cp, there will be troubles in the northern direction.")},
    {"from": "Sg", "to": "Ar", "prefer": (), "avoid": ("all",),
     "says": ("In the leap from Sg to Ar, journeys should be avoided, as they "
              "may result in sickness, imprisonment or death.")},
    {"from": "Sg", "to": "Sc", "prefer": ("all",), "avoid": (),
     "says": ("In the normal movement from Sg to Sc, journeys will bring "
              "comforts, wealth and sexual pleasures.")},
    {"from": "Le", "to": "Cn", "prefer": (), "avoid": ("west",),
     "says": "In the leap from Le to Cn, western direction should be avoided."},
)


def directions_for(origin: int, target: int) -> dict:
    """Parasara's travel advice for one transition, if he gave any.

    Returns ``undecided`` rather than silence for a transition that occurs on
    a wheel and has no rule; see
    :data:`PARASARA_LEAVES_FOUR_APASAVYA_LEAPS_UNADVISED`.
    """
    start = validate.in_range("origin", origin, 0, 11)
    end = validate.in_range("target", target, 0, 11)
    occurs = tuple(
        group for group in ("savya", "apasavya")
        for row in transitions(group)
        if row["from"] == start and row["to"] == end)

    for row in PARASARA_DIRECTIONS:
        if (_RASI[row["from"]], _RASI[row["to"]]) == (start, end):
            return {
                "from_rasi": str(RASI_NAMES[start]),
                "to_rasi": str(RASI_NAMES[end]),
                "occurs_in": occurs,
                "prefer": row["prefer"], "avoid": row["avoid"],
                "says": row["says"], "undecided": None,
            }
    return {
        "from_rasi": str(RASI_NAMES[start]),
        "to_rasi": str(RASI_NAMES[end]),
        "occurs_in": occurs,
        "prefer": (), "avoid": (), "says": None,
        "undecided": (
            "§24.3.3 gives no direction rule for this transition"
            if occurs else
            "this transition occurs on neither wheel"),
    }


#: **Gap.** The seven rules cover five savya transitions and two apasavya
#: ones, and leave four apasavya leaps unadvised — both frog's leaps, Ge to Le
#: and Cn to Vi, and both lion's leaps, Sc to Pi and Ar to Sg. The savya wheel
#: has every one of its five irregular steps covered.
PARASARA_LEAVES_FOUR_APASAVYA_LEAPS_UNADVISED = (
    "Of the ten irregular steps on the two wheels, Parasara's direction rules "
    "reach six. The four unadvised are all apasavya: Ge to Le, Cn to Vi, Sc "
    "to Pi and Ar to Sg."
)


# --------------------------------------------------------------------------
# Example 98 — why Pisces gave marriage
# --------------------------------------------------------------------------

#: **Finding.** Chart 46 is Chart 44's native printed again: same birth data,
#: same twelve longitudes, same eight chara karakas. Chart 44 drew the rasi
#: chart for a Pitri Shoola dasa; Chart 46 draws the navamsa, which is the
#: chart Example 98 reads. Nothing recomputes differently.
CHART_46_IS_CHART_44S_NATIVE = (
    "Chart 46 and Chart 44 are one native, May 9 1971 at 81 E 12, 16 N 15. "
    "Chart 44 prints the rasi diagram and Chart 46 the navamsa; the twelve "
    "longitudes below both are identical."
)

#: The principle Example 98 turns on, and the reason one dasa gave a love
#: affair and the next a marriage. Stated nowhere else in the chapter.
RASI_IS_PHYSICAL_NAVAMSA_IS_INNER = (
    "While rasi shows what exists at the physical level, navamsa shows the "
    "inner self and the sense of connectedness."
)

#: Venus's significations as Example 98 uses them, and a rule §24.3.1 did not
#: give: a *karaka-relative* house, counted in the navamsa.
VENUS_SYMBOLIZES = "domestic happiness and marital bliss"

SECOND_FROM_VENUS_RULE = (
    "The 2nd from him in navamsa can show the sense of family happiness. It "
    "can show a new person coming into the family."
)


def second_from_venus(venus_sign: int) -> int:
    """The rasi Example 98's karaka rule points at, counted in the navamsa."""
    return (validate.in_range("venus_sign", venus_sign, 0, 11) + 1) % 12


#: Example 98's four reasons, in the order it gives them. ``chart`` is the
#: chart each is read in, which is the point of the example: three of the four
#: are navamsa readings and the third is not.
EXAMPLE_98_REASONS: tuple[dict[str, str], ...] = (
    {"rasi": "Pisces", "chart": "D9", "because": "it holds the navamsa lagna",
     "gives": "marriage", "rule": "house"},
    {"rasi": "Virgo", "chart": "D9",
     "because": "it is the 7th and holds Jupiter, the navamsa lagna's lord",
     "gives": "marriage", "rule": "house-and-lord"},
    {"rasi": "Pisces", "chart": "D9", "because": "it is the 2nd from Venus",
     "gives": "the sense of family happiness, a new person coming into the "
              "family", "rule": "karaka"},
    {"rasi": "Pisces", "chart": "D1",
     "because": "exalted Venus occupies it and he owns the darapada in Libra",
     "gives": "physical relationship and marital pleasures", "rule": "planet"},
)

#: The reading that separates the two dasas, and the one Example 98 exists to
#: make: Venus sits in Aquarius in the navamsa and in Pisces in the rasi
#: chart, so Aquarius's dasa reached him at the navamsa level only.
AQUARIUS_GAVE_ROMANCE_AND_PISCES_GAVE_MARRIAGE = (
    "Aq dasa can activate Venusian influence at navamsa level and give some "
    "romance. During Aq dasa (1990-1994), this native had a love affair with "
    "the lady he was to marry in December 1994."
)

#: **Finding.** Example 98 dates two events and separates neither year length.
#: Aq dasa is 1990-1994 under savana and under 365.25 days alike, and the
#: December 1994 wedding falls in Pi-Pi either way — Pi dasa opens in July 1994
#: under savana and November 1994 under 365.25, and its first antardasa is a
#: full year long. OI-115 gains nothing here.
EXAMPLE_98_DOES_NOT_SEPARATE_THE_YEAR_LENGTHS = (
    "Aq dasa spans 1990 to 1994 under both year lengths, and the wedding "
    "falls inside the Pi-Pi antardasa under both. The example dates nothing "
    "finely enough to choose."
)


# --------------------------------------------------------------------------
# Example 99 — why Gemini gave knowledge
# --------------------------------------------------------------------------

#: **Finding.** Chart 47 is the third printing of the native of Charts 27 and
#: 33. Chart 27 drew the D-4, Chart 33 the D-16 and Chart 47 the D-24; the
#: rasi chart has never been drawn for him, only its twelve longitudes.
CHART_47_IS_THE_THIRD_PRINTING = (
    "Charts 27, 33 and 47 are one native, April 4 1970 at 81 E 12, 16 N 15, "
    "printed as a D-4, a D-16 and a D-24."
)


def balance_per_arcminute(sequence: tuple[int, ...]) -> float:
    """How much the birth balance moves per arcminute of Moon longitude.

    A pada is 200 arcminutes and its paramayush is spread across them, so one
    arcminute is ``paramayush / 200`` years — between **4.98 and 6 months**
    for the four paramayush values. See
    :data:`THE_BIRTH_BALANCE_NEEDS_THE_UNROUNDED_MOON`.
    """
    return paramayush(sequence) / 200.0


#: **Finding.** Kalachakra's balance at birth cannot be reproduced from a
#: longitude printed to the arcminute. Example 99 says "about 3 years and 2
#: months of Sg dasa was left at birth"; the printed Moon of 28 Aq 35 gives
#: **3 years 3.3 months** and the ephemeris Moon, 0.09' further on, gives
#: **3 years 2.9 months**. Example 98 is the same story — its printed Moon
#: gives a balance of 5.50 years and the computed one 5.20, and the book says
#: "about 5 years". Both examples were worked from the unrounded Moon.
THE_BIRTH_BALANCE_NEEDS_THE_UNROUNDED_MOON = (
    "One arcminute of Moon longitude moves the balance at birth by "
    "paramayush/200 years -- five to six months. A longitude rounded to the "
    "arcminute is therefore worth +/- 2.5 months of balance, and near a dasa "
    "boundary it can change which dasa runs at birth."
)

#: Example 99's reading of the D-24, in the order it gives it.
EXAMPLE_99_REASONS: tuple[dict[str, str], ...] = (
    {"rasi": "Gemini", "because": "it contains lagna in D-24",
     "gives": "all-round progress related to learning and knowledge",
     "rule": "house"},
    {"rasi": "Gemini",
     "because": "its lord Mercury is in the 5th house of scholarship",
     "gives": "scholarship", "rule": "lord"},
    {"rasi": "Gemini",
     "because": "Mercury and Venus are in trines from it",
     "gives": "prosperity of the indications of Gemini", "rule": "trines"},
    {"rasi": "Gemini", "because": "it has 34 rekhas in the D-24 SAV",
     "gives": "favorable results related to that house", "rule": "sav"},
    {"rasi": "Gemini", "because": "it is the 5th from AL and also A5",
     "gives": "some reputation for his knowledge", "rule": "arudha"},
)

#: A rule §24.3.1 did not give, and the reason the three strongest signs of a
#: D-24 SAV were worth naming at all.
TWO_FIVE_AND_SEVEN_FROM_AL_ARE_RECOGNITION = (
    "The strongest houses in this D-24 SAV are Le (36 rekhas), Ge (34 rekhas) "
    "and Pi (33 rekhas). They are the 7th, 5th and 2nd houses from AL. As "
    "these are the houses conducive to recognition and awards, this D-24 "
    "shows a person with academic achievements and associated recognition."
)

#: Example 99 restates §24.3.1's threshold without the hedge §24.3.1 gave it.
#: §24.3.1 said "usually"; this says "any rasi".
SAV_THRESHOLD_RESTATED_WITHOUT_THE_HEDGE = (
    "Any rasi 30 or more rekhas brings favorable results related to that "
    "house in that divisional chart."
)


# --------------------------------------------------------------------------
# Example 100 — the death of a father, and the first date that separates
# OI-115's year lengths
# --------------------------------------------------------------------------

#: §24.3's rule for reading a relative through a varga, given in full only
#: here. The house is the *concept*; its arudha is the physical body.
THE_HOUSE_IS_THE_CONCEPT_AND_THE_ARUDHA_IS_THE_BODY = (
    "The 9th house in D-12 shows the relation with father and the associated "
    "happiness. It stands for the \"concept\" of father and paternal "
    "guidance. The \"physical body\" of the father is an illusion related to "
    "the concept of father and A9 represents it. So we can use the 9th lord "
    "or A9 to see the physical body of father."
)

#: Example 100's chain, in the order it is given. Each step is a house count
#: from the one before, which is why the arudha has to be found first.
EXAMPLE_100_CHAIN: tuple[dict[str, str], ...] = (
    {"step": "A9 in the D-12", "sign": "Capricorn",
     "means": "the physical body of the father"},
    {"step": "the 7th from A9", "sign": "Cancer",
     "means": "the house of death, taking Capricorn as lagna"},
    {"step": "its lord, the Moon", "sign": "Taurus",
     "means": "exalted, and afflicting the Sun"},
    {"step": "the 8th from A9", "sign": "Leo",
     "means": "owned by the Sun, whom the Moon afflicts"},
)

#: **Gap.** "He afflicts Sun" is not defined at this site. Exercise 35 uses the
#: word a second time on the same chart -- "exalted Venus ... afflicts the
#: debilitated 1st lord" -- and Venus is a natural benefic in every paksha, so
#: whatever affliction is here, it is **not** malefic influence. What the two
#: uses share is an **exalted graha conjoining** the graha it afflicts: the
#: exalted Moon with the Sun in Taurus, exalted Venus with debilitated Mercury
#: in Pisces. That the Moon is also waning, and so a natural malefic by
#: §3.2.1, looks incidental rather than the mechanism.
AFFLICTS_IS_NOT_DEFINED_HERE = (
    "§24.3 never says what afflicting is. Both uses on this chart are an "
    "exalted graha sharing a rasi with the one it afflicts, and one of the "
    "two is Venus, a natural benefic -- so it cannot mean malefic influence."
)

#: Recorded separately because it was my first reading of the sentence and
#: Exercise 35 supersedes it: the Moon of this chart *is* a natural malefic,
#: being waning, but that cannot be what "afflicts" means, since Venus is not.
THE_AFFLICTING_MOON_IS_ALSO_WANING = (
    "This birth falls in Krishna paksha, which §3.2.1 makes a natural "
    "malefic. True, and not the mechanism -- Exercise 35 afflicts with Venus."
)

#: The first reading in the book to use a gati, and it confirms that the named
#: rasi is the leap's **destination**: the leap is Vi to Cn and the dasa
#: called mandooki is Cancer's.
EXAMPLE_100_USES_THE_FROGS_LEAP = (
    "Moreover, Cn dasa here comes after Vi and involves mandooki gati (frog's "
    "leap). We see from the previous discussions that mandooki gati in savya "
    "nakshatras can bring distress to father."
)

#: **Finding.** Example 100 is the first dated Kalachakra event that separates
#: OI-115's two year lengths, and it lands on **savana**. "Cn dasa started in
#: September 1966": savana gives 1966-09-20 and a solar year gives 1967-03-15,
#: six months and a year out. The conclusion survives the Moon's rounding —
#: the printed Moon moves savana to November 1966 and the solar year to May
#: 1967, so savana keeps 1966 either way. Examples 96 and 98 separated
#: nothing; this one does, and it agrees with footnote 65.
#:
#: **Evidence only.** OI-115 stays open and the default is unchanged.
EXAMPLE_100_SEPARATES_THE_YEAR_LENGTHS = (
    "Cn dasa opens 1966-09-20 under a 360-day year and 1967-03-15 under "
    "365.25 days. The example says September 1966."
)


# --------------------------------------------------------------------------
# Example 101 — Vajpayee's Capricorn dasa
# --------------------------------------------------------------------------

#: §24.3's rule for reading one rasi across two charts, and the plainest
#: statement of why §24.3.1 said to keep several SAVs to hand.
STRONG_IN_BOTH_CHARTS = (
    "We can see that Cp has 31 rekhas in the SAV of D-10 and 34 rekhas in the "
    "SAV of rasi chart. Because Cp is strong in both charts, Cp dasa must be "
    "good."
)

#: Why the strong houses are counted from AL rather than from lagna.
AL_IS_THE_REFERENCE_FOR_FAME = (
    "AL is the most appropriate reference for judging fame and recognition."
)

#: **Finding.** Examples 99 and 101 each name the houses from AL that came out
#: strong and then call them houses of recognition, and the two lists are not
#: the same — 2nd, 5th and 7th there, 1st, 3rd, 5th, 7th and 10th here. Only
#: the 5th and 7th are in both. Example 101 hedges with "most of these", so
#: neither is a fixed list; each is an observation about the chart in hand.
THE_FAME_HOUSES_FROM_AL_ARE_NOT_A_FIXED_LIST = (
    "Example 99 calls the 2nd, 5th and 7th from AL conducive to recognition "
    "and awards; Example 101 calls the 1st, 3rd, 5th, 7th and 10th important "
    "for fame and recognition, hedged with \"most of these\". The 5th and 7th "
    "are the overlap."
)

#: Example 101's reading of A5, which extends Example 100's concept/body rule
#: to a second pada and names what it means in two vargas.
A5_IS_THE_ILLUSION_OF_THE_FIFTH = (
    "A5 shows the illusion associated with the 5th house matters. In D-24, A5 "
    "shows the illusion associated with scholarship (5th house), i.e. one's "
    "degrees, academic distinctions and awards. In D-10, it shows the "
    "illusion associated with one's following (5th house), i.e. the positions "
    "held and the power wielded by one."
)

#: Example 101's four reasons for Capricorn, in the order it gives them.
EXAMPLE_101_REASONS: tuple[dict[str, str], ...] = (
    {"because": "Cp has 31 rekhas in the D-10 SAV and 34 in the rasi SAV",
     "gives": "a good dasa", "rule": "sav"},
    {"because": "Cp is the 5th house from AL",
     "gives": "reputation and power", "rule": "arudha"},
    {"because": "the lord of Cp is exalted in GL",
     "gives": "power", "rule": "lord"},
    {"because": "Cp contains A5 in the rasi chart and in D-10",
     "gives": "the probability of power in Cp dasa", "rule": "arudha"},
)

#: **Finding.** Example 101 separates OI-115's year lengths a second time, and
#: more sharply than Example 100 did, because it gives both ends of the dasa.
#: "His 4-year Cp dasa runs during 1998-2002": savana gives 1998-08-04 to
#: 2002-07-14 and a solar year gives 1999-08-21 to 2003-08-21. The conclusion
#: survives the Moon's rounding — savana keeps 1998 and the solar year 1999.
#:
#: **Evidence only.** OI-115 stays open and the default is unchanged.
EXAMPLE_101_SEPARATES_THE_YEAR_LENGTHS = (
    "Cp dasa runs 1998-08-04 to 2002-07-14 under a 360-day year and "
    "1999-08-21 to 2003-08-21 under 365.25 days. The example says 1998-2002."
)


# --------------------------------------------------------------------------
# Example 102 — the ISKCON devotee's D-20, revisited from chapter 21
# --------------------------------------------------------------------------

#: **Book defect.** Chart 49 and Chart 37 are the same nativity printed twice
#: and they are not the same chart: Chart 49 is stated one minute earlier,
#: 10:43 against 10:44, and every graha is 1' to 2' further on, which is an
#: ayanamsa difference of about 1.5'. Our settings reproduce Chart 37 within an
#: arcminute and sit 1' to 1.8' below Chart 49. It is not cosmetic — the two
#: sets put **Venus** and **GL** in different D-20 signs, and only Chart 49's
#: own longitudes give the D-20 SAV figures Example 102 quotes. See D-69.
CHART_49_IS_NOT_CHART_37_RECAST = (
    "Chart 49 restates Chart 37's nativity one minute earlier and about 1.5' "
    "further on in every graha. Venus and GL land in different D-20 signs, "
    "and the D-20 SAV moves by up to 4 rekhas."
)

#: **Book defect.** "If one casts D-10 of this native, one will see that the
#: 3rd house and A3 have 30 or more rekhas, in D-10 SAV also." A3 does — the
#: D-10 arudha of the 3rd is Pisces with **31**. The 3rd house does not: the
#: D-10 lagna is Libra, its 3rd is Sagittarius, and Sagittarius has **25**.
#: Only Cn 36, Le 37, Sc 30 and Pi 31 reach thirty in that SAV, and no reading
#: of "the 3rd house" — the D-20's third sign, the third from AL, the third
#: from the rasi lagna — reaches it either. True under both printings of the
#: chart, so it is not the ayanamsa. See D-70.
THE_D10_THIRD_HOUSE_DOES_NOT_REACH_THIRTY = (
    "In the D-10 SAV the arudha of the 3rd reaches 30 and the 3rd house does "
    "not: Pisces has 31 and Sagittarius 25. The conclusion that both are "
    "strong in D-10 as well as D-20 is half-supported."
)

#: §24.3's D-20 readings, house by house, as Example 102 gives them. The
#: pattern is Example 100's: the house is the matter and its arudha pada the
#: impression the world forms of it.
D20_HOUSE_READINGS: tuple[dict[str, object], ...] = (
    {"house": 3, "shows": "communication skills as applicable in religious "
                          "activities",
     "arudha": "A3", "arudha_shows": "one's religious works, the books and "
                                     "articles authored by one"},
    {"house": 5, "shows": "one's devotion and bhakti in religious matters",
     "arudha": "A5", "arudha_shows": "the maya relating to devotion, i.e. "
                                     "practice of mantras and religious "
                                     "rituals"},
    {"house": 7, "shows": "relations with others",
     "arudha": "A7", "arudha_shows": "the people one associates with, in "
                                     "one's spiritual life"},
    {"house": 9, "shows": "one's spiritual guru or organized religion or "
                          "religious practices; it can also show pilgrimages "
                          "and moving to a monastery",
     "arudha": None, "arudha_shows": None},
    {"house": 12, "shows": "spiritual evolution and activities related to "
                           "moksha",
     "arudha": None, "arudha_shows": None},
)

#: A5's other name, given only here.
A5_IS_THE_MANTRA_PADA = "A5 (mantra pada, arudha pada of the 5th house)"

#: The authority §24.3.1's threshold rests on, named for the first time.
THIRTY_REKHAS_IS_PARASARAS = (
    "Houses with 30 or more rekhas in SAV are strengthened as per Parasara."
)

#: **Finding.** Example 102 does **not** separate OI-115's year lengths, and on
#: one reading it leans the other way from Examples 100 and 101. "Pi dasa
#: started in July 1987" needs a balance of 9.71 years under savana and 9.47
#: under 365.25, and the example says "about 9.5". But Chart 49's own printed
#: Moon gives 9.775, which puts Pi in August 1987 under savana and November
#: under 365.25. The chart does not reproduce under our ayanamsa, so the
#: balance cannot be pinned from the ephemeris the way Examples 100 and 101
#: were; and the arcminute of Moon is worth five months of balance here while
#: the year lengths differ by only three at this age. The uncertainty exceeds
#: the signal.
EXAMPLE_102_CANNOT_SEPARATE_THE_YEAR_LENGTHS = (
    "Taken with the stated balance of 9.5 years, July 1987 needs 365.25 days; "
    "taken with Chart 49's printed Moon, it is nearer savana. The truncated "
    "arcminute spans balances from 9.36 to 9.775, and both year lengths put "
    "Pi dasa in 1987 somewhere in that span."
)


# --------------------------------------------------------------------------
# Exercise 35 — the same native's mother, read from A4
# --------------------------------------------------------------------------

#: Exercise 35 confirms that Example 100's rule is general: the father was read
#: from **A9** and the mother is read from **A4**, each the arudha of the house
#: that signifies the relative. Nothing in Example 100 said the rule extended.
EXERCISE_35_READS_THE_MOTHER_FROM_A4 = (
    "The 4th house is in Sg. A4 or the arudha pada of 4th house is in Vi. "
    "From Vi, Li is the 2nd house. Its lord Venus is in exalted in the 7th "
    "house and afflicts the debilitated 1st lord (all from Vi). So Li is a "
    "strong maraka rasi from Vi. So Li-Li antardasa resulted in the death of "
    "mother."
)

#: **Finding.** What makes Libra a *strong* maraka is that Venus is a maraka
#: twice over from A4: it lords the 2nd and sits in the 7th, and §14 makes both
#: houses maraka. The exercise says only "the 2nd house" and "the 7th house"
#: and never joins them.
VENUS_IS_A_MARAKA_TWICE_OVER = (
    "Venus lords Libra, the 2nd from A4, and occupies Pisces, the 7th from A4. "
    "Both are maraka houses, which is what \"a strong maraka rasi\" rests on."
)

#: **Finding.** A4 comes out as Virgo, which is also the D-12 lagna, so the
#: exercise's "all from Vi" reads the same as reading from lagna. That is a
#: coincidence of this chart: Example 100's A9 was Capricorn and the D-12
#: lagna was Virgo, and the two parted company there.
A4_HAPPENS_TO_BE_THE_D12_LAGNA_HERE = (
    "A4 is Virgo and so is the D-12 lagna, so \"all from Vi\" cannot show "
    "which of the two the exercise is counting from. Example 100 counted from "
    "A9, which was not the lagna."
)

#: **Finding.** Three charts in a row have needed §9.2's same-sign exception:
#: Chart 46's navamsa AL, Chart 48's D-12 AL, and now Chart 48's A4. In each
#: the house's lord sits the 7th from it, which sends the arudha back onto the
#: house itself and then on to the 10th.
THE_SAME_SIGN_EXCEPTION_KEEPS_FIRING = (
    "Chart 46's navamsa AL, Chart 48's D-12 AL and Chart 48's A4 all reach "
    "their sign through §9.2's exception, the lord being the 7th from its own "
    "house each time."
)


# --------------------------------------------------------------------------
# Exercise 36 — the divorced lady, and the nakshatra no table names
# --------------------------------------------------------------------------

#: **The evidence that settles D-67 and OI-139.** Exercise 36's Moon is in
#: **Uttarabhadrapada**, which Tables 44 and 45 between them do not name, and
#: the exercise works its dasa anyway. Both stated events fall in **Sg dasa**,
#: and only one sub-group puts them there:
#:
#: ===========  ==========================  =====================
#: sub-group    Sg dasa runs at ages        Feb 1992 / late 1995
#: ===========  ==========================  =====================
#: savya-1      1.5 to 11.5                 both in Pisces dasa
#: savya-2      19.5 to 29.5                **both in Sg dasa**
#: ===========  ==========================  =====================
#:
#: The conclusion holds under the printed Moon and the ephemeris Moon alike,
#: and under both of OI-115's year lengths — savya-1 is out by seventeen years
#: however it is computed. It also confirms D-67's reconstruction, which
#: predicted savya-2 from the pattern of the other four triples.
#:
#: **NEEDS YOU.** :func:`sub_group_of` still raises for 26. Making it return 2
#: is a behaviour change and is not made here.
UTTARABHADRAPADA_IS_SAVYA_2 = (
    "Exercise 36's Moon is in Uttarabhadrapada's 1st pada. Under savya-2 its "
    "Sg dasa runs from age 19.5 to 29.5, which holds both the marriage and "
    "the divorce; under savya-1 Sg is over by age 11.5 and both events fall "
    "in Pisces dasa. Nothing else in the exercise distinguishes them."
)

#: §24.3's upapada rules, given in full only in this exercise's answer. UL is
#: the arudha of the 12th, and marriage is read from it rather than from the
#: 7th house.
UPAPADA_RULES: tuple[dict[str, object], ...] = (
    {"house": 3, "from": "UL", "shows": "the start of a marriage"},
    {"house": 2, "from": "UL", "shows": "the end of marriage"},
    {"house": 7, "from": "UL", "shows": "the end of marriage"},
    {"house": 6, "from": "lagna", "shows": "marital troubles and quarrels"},
    {"house": 8, "from": "lagna", "shows": "marital troubles and quarrels"},
)

#: **Finding.** The exercise's premise is that Venus owns both of UL's maraka
#: houses. UL is Aries in the rasi chart *and* in the navamsa, so the 2nd is
#: Taurus and the 7th is Libra in both — Venus's two signs. That is why one
#: dasa could give the marriage and its ending.
VENUS_OWNS_BOTH_MARAKAS_OF_THE_UPAPADA = (
    "Sg contains Venus, the significator of marriage. However, Venus also "
    "owns the 2nd and 7th from upapada in rasi and navamsa."
)

#: The qualification §24.3.1's rekha threshold needed and did not carry: a high
#: SAV count is not favourable in itself.
EVIL_HOUSES_WHEN_STRONG_BRING_EVIL_RESULTS = (
    "While the 7th house has only 22 rekhas, the 8th house has 30 rekhas and "
    "so the 8th house is strong. Evil houses, when strong, only bring evil "
    "results."
)

#: Exercise 36's five reasons for Gemini, in the order given. Every one is read
#: in the **navamsa**, which the answer opens by choosing.
EXERCISE_36_GEMINI_REASONS: tuple[str, ...] = (
    "Ge contains A7 in navamsa and can show a relationship",
    "it contains the 3rd from UL and can show the start of a marriage",
    "it is the 7th house from Venus",
    "it is the 4th house of harmony and bliss from lagna",
    "its lord Mercury is exalted in the 7th house",
    "Ge has 33 rekhas in SAV",
)

#: And the two for Libra, which is a maraka from two references at once.
EXERCISE_36_LIBRA_REASONS: tuple[str, ...] = (
    "Li is the 8th house from lagna",
    "it is the 7th house from upapada, in navamsa and in rasi",
    "it has 30 rekhas in the navamsa SAV, where the 7th house has only 22",
)

#: **Finding.** Exercise 36 points the *other* way on OI-115 from Examples 100
#: and 101. Its two dates land in the named antardasas only under **365.25**
#: days and only from the **printed** Moon: savana puts the February 1992
#: wedding after Ge antardasa has closed, and the ephemeris Moon — which is
#: 1.75' below the printed one here — misses the late-1995 divorce under both
#: year lengths. Chart 50 does not reproduce within an arcminute, so its dates
#: cannot be pinned the way Examples 100 and 101 were.
EXERCISE_36_FAVOURS_THE_SOLAR_YEAR = (
    "From the printed Moon, Ge antardasa runs to February 1992 under 365.25 "
    "days and closes in September 1991 under savana, while Li antardasa "
    "covers late 1995 under both. The stated Ge antardasa needs the solar "
    "year."
)


# --------------------------------------------------------------------------
# Exercise 37 — Bill Cosby's D-10
# --------------------------------------------------------------------------

#: The four reasons Exercise 37 gives for Cancer, all read in the D-10.
EXERCISE_37_CANCER_REASONS: tuple[str, ...] = (
    "Cn is the 10th from lagna",
    "its lord Moon is in the 5th from lagna",
    "Cn contains AL and shows status in career",
    "in SAV, Cn has 38 rekhas -- exceedingly strong",
)

#: **Finding.** Exercise 37 is the only place the book prints a **whole** SAV,
#: all twelve signs, and every one reproduces. It is therefore the strongest
#: single check on the ashtakavarga engine in the book — twelve independent
#: figures from one chart, summing to 337.
THE_ONLY_COMPLETE_SAV_IN_THE_BOOK = (
    "Ar 24, Ta 28, Ge 21, Cn 38, Le 34, Vi 21, Li 26, Sc 26, Sg 37, Cp 31, "
    "Aq 25, Pi 26. Twelve figures, all reproduced, totalling 337."
)

#: The question the exercise actually asks, and the answer's own words for 38.
#: §24.3.1 gave one threshold, 30; this reads a count well above it as more
#: than merely strong.
THIRTY_EIGHT_IS_EXCEEDINGLY_STRONG = (
    "In SAV, Cn has 38 rekhas. That is exceedingly strong. With the rasi "
    "containing AL having 38 rekhas in SAV, the status of this actor must be "
    "high."
)

#: **Finding.** Taurus occupies two of this pada's nine positions and the
#: balance at birth falls in the **second** of them, which is what puts Gemini,
#: Leo and Cancer next rather than Aries, Sagittarius and Capricorn. Reading
#: the nine as a set of rasis rather than as nine wheel positions would take
#: the wrong Taurus and the whole dasa sequence would be wrong.
A_PADA_CAN_HOLD_A_RASI_TWICE = (
    "Poorvaphalguni's 2nd pada runs Ge, Ta, Ar, Sg, Cp, Aq, Pi, Ar, Ta -- "
    "Taurus at positions 1 and 8, Aries at 2 and 7. The dasa running at birth "
    "is a position in that walk, not a rasi in a set."
)

#: **Finding.** Exercise 37 does not separate OI-115's year lengths. From the
#: printed Moon, Cn dasa opens June 1964 under savana and October 1964 under
#: 365.25 — both "1964". Its stated close, 1984, fits neither: twenty-one years
#: from mid-1964 is 1985 under any reckoning, so the label is loose.
EXERCISE_37_DOES_NOT_SEPARATE_THE_YEAR_LENGTHS = (
    "Cn dasa opens in 1964 under both year lengths and closes in 1985 under "
    "both. \"1964-1984\" is a loose label for a twenty-one-year dasa."
)


# --------------------------------------------------------------------------
# §24.5 Conclusion
# --------------------------------------------------------------------------

#: §24.5's opening, and PVR's own place in it. Parasara's praise was recorded
#: at §24.1; this adds the author's, which no other dasa in Part 2 gets.
PVRS_FAVOURITE_DASA = (
    "A significant percentage of this author's successful long-range "
    "life-phase predictions were made using Kalachakra dasa and that is his "
    "favorite dasa."
)

#: **Important.** §24.5 says outright that chapter 24 is *a* recension, not
#: *the* one. Everything the chapter's tables contain — including D-67's
#: missing nakshatra and OI-139's inconsistent sub-groups — is PVR's chosen
#: reading of BPHS, so a defect in them may be his source's rather than the
#: print's, and our precedence keeps his version either way.
THE_COMPUTATION_IS_CONTROVERSIAL = (
    "There are many controversies regarding its computation. This book "
    "follows the approach that this author found the most acceptable based on "
    "his study of \"Brihat Parasara Hora Sastram\" and his practical "
    "researches."
)

#: Footnote 68, which names the tool §24.5 does *not* use Kalachakra for.
#: Tajaka is a later part of the book and nothing of it has been read.
FOOTNOTE_68 = (
    "And, a significant percentage his successful short-term predictions "
    "(focussing on a period of one or two weeks) were made using Tajaka "
    "annual and monthly charts."
)

#: **Finding.** Footnote 68 divides the labour by *horizon*, which no earlier
#: section did: Kalachakra for long-range life phases, Tajaka annual and
#: monthly charts for one or two weeks. Part 2 has classified its nine by
#: kind and by purpose and never by timescale. Nothing of Tajaka has been
#: read, so this is recorded and not built.
DASAS_AND_TAJAKA_SPLIT_BY_HORIZON = (
    "Kalachakra dasa carries the long-range life-phase predictions and Tajaka "
    "annual and monthly charts the one-to-two-week ones. Part 2 classifies "
    "its nine systems by kind and purpose, never by horizon."
)

#: **A restriction the book rejects.** Some authors gate Kalachakra on the
#: Moon being stronger in the navamsa than in the rasi chart. PVR does not,
#: and says why. :func:`pada_of` therefore takes any Moon and no applicability
#: test exists in this module — deliberately.
APPLIES_TO_EVERYONE = (
    "Some authors suggested that Kalachakra dasa applies only when Moon is "
    "stronger in navamsa chart than in rasi chart. However, this author "
    "opines that Kalachakra dasa is applicable to all people, as Parasara did "
    "not impose any conditions on its applicability and went to the extent of "
    "calling it \"the most respectable dasa\"."
)

REJECTED_APPLICABILITY_TEST = (
    "Moon stronger in navamsa than in rasi -- not applied; see "
    "APPLIES_TO_EVERYONE."
)

#: §24.5's reason the dasa reads the inner self, and the identity behind it.
KALACHAKRA_DEPENDS_ON_MOONS_NAVAMSA = (
    "Kalachakra dasa depends on Moon's navamsa. Navamsa shows one's adherence "
    "of dharma or duty and throws light on the inner self. So the focus in "
    "Kalachakra dasa is state of the inner self and the sense of "
    "connectedness in one's mind."
)

#: **Finding.** "Moon's navamsa" and "Moon's nakshatra pada" are the same
#: thing, and §24.5 is the first place the book uses the navamsa name for it.
#: A pada is 3°20' and so is a navamsa; 27 × 4 and 12 × 9 are both 108; and
#: both partitions start at 0° Aries. So the *n*th pada of the zodiac **is**
#: its *n*th navamsa, and §24.2's whole procedure can be read as "find the
#: Moon's navamsa" without changing a figure.
A_PADA_IS_A_NAVAMSA = (
    "The zodiac's 108 nakshatra padas and its 108 navamsas are one partition: "
    "both are 3°20' wide, both begin at 0° Aries, and the nth pada is "
    "the nth navamsa."
)

#: §24.5's worked illustration of three dasas on one event, kept because it is
#: the only place the book shows them disagreeing rather than agreeing.
THREE_DASAS_ON_ONE_EVENT = (
    "A political leader may be running D-10 Narayana dasa of a yogakaraka "
    "rasi and he may land political power. He may be running the Vimsottari "
    "dasa of Sun who may be exalted in D-10 and so he may be feeling "
    "powerful. However, if Kalachakra dasa of a weak and afflicted house in "
    "D-10 runs at the same time, his inner self may not feel connected with "
    "the events in his career and he may feel a void. On the other hand, if "
    "Kalachakra dasa rasi is strong and occupied by benefics in D-10, then "
    "one may be successfully involved in activities that keep his inner self "
    "engaged."
)

#: Chapter 24 as read: §24.1 to §24.5 entire, nine examples, three exercises
#: and two charts of its own. What it leaves open is registered, not silent.
CHAPTER_24_IS_COMPLETE = (
    "§24.1 to §24.6, Examples 95 to 102 and Exercises 34 to 37, checked "
    "against the printed pages 289 to 312. Open: D-67 and OI-139 "
    "(Uttarabhadrapada's sub-group, deduced but not adopted), D-68, D-69, "
    "D-70, D-71 and OI-115's split evidence."
)


# --------------------------------------------------------------------------
# §24.2's own prose, which the tables are only a convenience for
# --------------------------------------------------------------------------

#: How §24.2 says Parasara built the thing, before any table appears.
PARASARA_DREW_TWO_SETS_OF_TWELVE = (
    "Parasara taught that we can draw Kalachakra (wheel of Time) by drawing 2 "
    "sets of 12 houses for savya and apasavya groups of nakshatras, then "
    "repeating them and distributing them between nakshatras."
)

#: §24.2's three illustrations of Aswini's 1st pada, given *before* the
#: numbered procedure. Each lists nine dasas in all, so **footnote 64's
#: nine-rasi rule is in the main text**, four pages before the footnote.
ASWINI_FIRST_PADA_ILLUSTRATIONS = (
    "The dasa running at birth will be one of these 9 rasis and one will run "
    "dasas of 9 rasis starting from that rasi. One born with Moon at the "
    "beginning of the first pada of Aswini will run Ar dasa at birth and run "
    "Ta, Ge, Cn, Le, Vi, Li, Sc and Sg dasas after it. One born with Moon in "
    "the middle of the first pada of Awini may run Le dasa at birth and run "
    "Vi, Li, Sc, Sg, Cp, Aq, Pi and Sc dasas after it. One born with Moon "
    "towards the end of the first pada of Aswini may run Sg dasa at birth and "
    "Cp, Aq, Pi, Sc, Li, Vi, Cn and Le dasas after it."
)

#: The same three as data — the fraction each describes, the dasa the book
#: names, and the dasa the arithmetic gives.
ASWINI_ILLUSTRATION_CASES: tuple[dict[str, object], ...] = (
    {"where": "beginning", "fraction": 0.0, "book": "Ar", "computed": "Ar"},
    {"where": "middle", "fraction": 0.5, "book": "Le", "computed": "Cn"},
    {"where": "end", "fraction": 1.0, "book": "Sg", "computed": "Sg"},
)

#: **Book defect.** The middle case does not compute. Aswini's 1st pada has a
#: paramayush of 100, so half of it is 50 years, which falls in **Cancer**
#: (32 to 53); Leo does not open until 53. The eight dasas the passage then
#: lists — Vi, Li, Sc, Sg, Cp, Aq, Pi, Sc — do follow **Leo**, so the sentence
#: is internally consistent and it is the word "middle" that is loose: the
#: fractions giving Leo are 0.53 to 0.58. Hedged with "may", and the beginning
#: and end cases are exact. See D-71.
THE_MIDDLE_OF_ASWINIS_FIRST_PADA_GIVES_CANCER = (
    "Half of a 100-year paramayush is 50 years, which falls in Cancer's dasa "
    "(32 to 53). Leo runs from 53 to 58, so \"the middle\" of the pada gives "
    "Cancer and Leo needs a fraction between 0.53 and 0.58."
)

#: The wheel's wrap, and the sentence that makes rule (4) a walk rather than a
#: table lookup.
THE_WHEEL_WRAPS = (
    "Like this, as we go from one nakshatra pada (constellation quarter) to "
    "the next in the savya group, we move from one set of 9 rasis to the "
    "next. When we reach the end of the 24 rasis, we go to the beginning."
)

#: And the nakshatra boundary, stated for Aswini and Bharani by name.
BHARANI_CONTINUES_ASWINI = (
    "At the end of the 4th quarter of Aswini, the 1st quarter of Bharani "
    "starts and we do the same thing. We go to the next 9 rasis in the set of "
    "24 rasis."
)

#: **Important.** §24.2 says the four pada tables exist only for readers who
#: cannot run the wheel, and that the sub-groups exist only to lay those
#: tables out. We derive Tables 44 to 47 from the wheel for exactly this
#: reason — and it bears on OI-139, because a sub-group is a presentation
#: device rather than a rule of the dasa.
THE_TABLES_ARE_A_CONVENIENCE = (
    "For the sake of those who do not understand the above logic well enough "
    "to list the nine rasis associated with each nakshatra pada, they are "
    "explicitly given in Table 44-Table 47. For the purpose of these tables, "
    "we will divide savya and apasavya groups of nakshatras into two "
    "sub-groups each."
)

#: §24.2's closing line on its own procedure, which is the same claim again.
IT_MUST_BE_OBVIOUS_FROM_TABLE_43 = (
    "All this may seem complicated to a casual reader, but it must be obvious "
    "to anyone who clearly understood Kalachakra shown in Table 43 and "
    "followed how Table 44-Table 47 are derived from it."
)

#: Example 95's two dated figures, which the first screenshot of it cropped.
#: Both come out of the balance alone under §18.6's units — 4.75 years is
#: 4 years 9 months, and 4.75 + 16 is 20 years 9 months.
EXAMPLE_95_DATES_ITS_FIRST_TWO_DASAS = (
    "By adding 4 years 9 months to the birthdate, we get the date on which Sc "
    "dasa ends. Then Li dasa of 16 years will run till an age of 20 years 9 "
    "months."
)

#: **Finding.** The savya sub-groups follow a rule the apasavya ones do not:
#: within each triple of savya nakshatras the **1st and 3rd** take sub-group 1
#: and the **2nd** takes sub-group 2. That rule reproduces Tables 44 and 45
#: exactly **except that 26 and 27 are swapped** — it wants Uttarabhadrapada in
#: savya-2, which Exercise 36 independently confirmed, and Revati in savya-1,
#: where Table 44 is one name short. One substitution restores both the
#: pattern and the count, 10 + 5 = 15. The apasavya group splits **1st to
#: sub-group 1, 2nd and 3rd to sub-group 2**, differing from the savya rule on
#: all four third-of-triple nakshatras. See D-67 and OI-139.
THE_SAVYA_SUB_GROUPS_FOLLOW_A_TRIPLE_RULE = (
    "Savya splits each triple 1st and 3rd to sub-group 1, 2nd to sub-group 2, "
    "which gives the printed tables but for 26 and 27 being swapped. Apasavya "
    "splits 1st to sub-group 1 and 2nd and 3rd to sub-group 2. No single rule "
    "produces both."
)
