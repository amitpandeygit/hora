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
from hora.core.const import RASI_ABBR, RASI_LORD, RASI_NAMES, Graha


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

#: Footnotes 63, 64 and 65 hang off Example 95 and are not on the pages read
#: so far. Nothing here depends on them; recorded so their absence is not
#: mistaken for their having said nothing.
EXAMPLE_95_FOOTNOTES_UNSEEN = (
    "Example 95 carries footnotes 63, 64 and 65 -- on the pada fraction, on "
    "the seven dasas it lists, and on their lengths. None has been read."
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
