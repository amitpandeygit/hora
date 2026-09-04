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
     "other sub-group in the same group)."),
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

#: **Gap.** "He afflicts Sun" is not defined at this site, and the Moon is not
#: a natural malefic in general. It is one *here*: this birth falls in Krishna
#: paksha, and §3.2.1 makes a waning Moon a natural malefic. That reconciles
#: the sentence with the book's own definitions, but the book does not say so,
#: and the affliction's mechanism -- conjunction in Taurus in the D-12 --
#: is inferred from the chart rather than stated.
AFFLICTS_IS_NOT_DEFINED_HERE = (
    "§24.3 does not say what afflicting is. The Moon of this chart is waning "
    "and so a natural malefic by §3.2.1, and it shares Taurus with the Sun in "
    "the D-12; neither fact is stated in the example."
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
