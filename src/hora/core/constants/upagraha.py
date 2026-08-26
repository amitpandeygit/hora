"""Upagrahas — the eleven sub-planets (book chapter 4).

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant — that facade is the
stable internal surface and keeps call sites independent of how the tables are
filed.
"""
from __future__ import annotations

from enum import IntEnum

from hora.core.constants.graha import Graha

# --------------------------------------------------------------------------
# Upagrahas (book chapter 4)
# --------------------------------------------------------------------------

class Upagraha(IntEnum):
    """The eleven upagrahas of section 4.1, in the book's order."""

    DHUMA = 0
    VYATIPAATA = 1
    PARIVESHA = 2
    INDRACHAAPA = 3
    UPAKETU = 4
    KAALA = 5
    MRITYU = 6
    ARTHA_PRAHARAKA = 7
    YAMA_GHANTAKA = 8
    GULIKA = 9
    MAANDI = 10


#: 1.3.1: "there are 11 moving mathematical points known as Upagrahas
#: (sub-planets or satellites)". The count is a fact about the set and is
#: asserted against the table rather than left for a reader to count.
UPAGRAHA_DEFINITION = "moving mathematical points"
UPAGRAHA_GLOSS = "sub-planets or satellites"
UPAGRAHA_COUNT = 11

#: 4.1 attributes the set: "There are 11 upagrahas (sub-planets or satellites)
#: defined by Sage Parasara."
UPAGRAHA_SOURCE = "Sage Parasara"

#: 4.1: "They do not appear to correspond to any physical bodies (planets,
#: stars etc). From Sage Parasara's definition, they appear to be some
#: significant mathematical points."
UPAGRAHA_NOT_PHYSICAL = (
    "They do not appear to correspond to any physical bodies (planets, stars "
    "etc). From Sage Parasara's definition, they appear to be some significant "
    "mathematical points."
)

#: 4.1: "They will be defined in two groups." Five Sun-based in 4.2, six
#: time-based in 4.3 — which is why UPAGRAHA_NAMES splits 5 + 6.
UPAGRAHA_GROUP_COUNT = 2
UPAGRAHA_GROUPS = {
    "sun_based": "4.2 Sun-based Upagrahas",
    "time_based": "4.3 Time-based Upagrahas",
}

UPAGRAHA_NAMES = [
    "Dhuma", "Vyatipaata", "Parivesha", "Indrachaapa", "Upaketu",
    "Kaala", "Mrityu", "Artha Praharaka", "Yama Ghantaka", "Gulika", "Maandi",
]

#: 4.2 The five Sun-based upagrahas.
SUN_BASED_UPAGRAHAS = (
    Upagraha.DHUMA, Upagraha.VYATIPAATA, Upagraha.PARIVESHA,
    Upagraha.INDRACHAAPA, Upagraha.UPAKETU,
)
#: 4.3 The six that need the time of birth.
TIME_BASED_UPAGRAHAS = (
    Upagraha.KAALA, Upagraha.MRITYU, Upagraha.ARTHA_PRAHARAKA,
    Upagraha.YAMA_GHANTAKA, Upagraha.GULIKA, Upagraha.MAANDI,
)

#: 4.2 Dhuma's offset from the Sun, 133 degrees 20 minutes.
DHUMA_OFFSET = 133.0 + 20.0 / 60.0
#: 4.2 spells it "Indrachapa" in the worked example and "Indrachaapa" in
#: Table 9. Same upagraha; the table spelling is the one we store.
UPAGRAHA_ALIASES: dict[str, list[str]] = {"Indrachaapa": ["Indrachapa"]}

#: 4.2 Upaketu's offset from Indrachaapa, 16 degrees 40 minutes.
UPAKETU_OFFSET = 16.0 + 40.0 / 60.0

#: 4.3 Which graha's part each time-based upagraha rises in, and whether it
#: rises at the middle of that part or at its beginning.
#: Maandi alone rises at the beginning; footnote 9 notes that some scholars
#: put all of them at the beginning, which is offered as a setting.
UPAGRAHA_PART_LORD: dict[int, int] = {
    Upagraha.KAALA: Graha.SUN,
    Upagraha.MRITYU: Graha.MARS,
    Upagraha.ARTHA_PRAHARAKA: Graha.MERCURY,
    Upagraha.YAMA_GHANTAKA: Graha.JUPITER,
    Upagraha.GULIKA: Graha.SATURN,
    Upagraha.MAANDI: Graha.SATURN,
}
UPAGRAHA_RISES_AT_BEGINNING = frozenset({Upagraha.MAANDI})

#: 4.2 "All these upagrahas are very malefic in nature. Any houses occupied by
#: them in rasi chart or divisional charts are spoiled by them."
VERY_MALEFIC_UPAGRAHAS = frozenset(SUN_BASED_UPAGRAHAS)

#: 4.3 names Kaala and Mrityu as malefic explicitly; for the other four it
#: gives only the graha they resemble. Nothing is inferred for those.
MALEFIC_UPAGRAHAS = frozenset({Upagraha.KAALA, Upagraha.MRITYU})

#: 4.3 opens by saying the six are "more difficult to compute" than the five
#: Sun-based ones — they need sunrise, sunset and the weekday, not a longitude.
TIME_BASED_HARDER_NOTE = (
    "Six upagrahas called Kaala, Mritya, Arthaprahaara, Yamaghantaka, Gulika "
    "and Maandi are more difficult to compute."
)

#: 4.3 spells two of the six differently in its opening list and in its
#: numbered procedure. Both are the book's own; UPAGRAHA_NAMES carries the
#: procedure's spelling because that is the section that defines them.
UPAGRAHA_NAME_VARIANTS: dict[int, str] = {
    Upagraha.ARTHA_PRAHARAKA: "Arthaprahaara",
    Upagraha.YAMA_GHANTAKA: "Yamaghantaka",
}

#: 4.3: "A day starts at the time of sunrise and ends at the time of sunset. A
#: night starts at the time of sunset and ends at the time of next day's
#: sunrise."
#:
#: Note this is **not** 1.3.11's day, which runs sunrise to next sunrise. A
#: hora divides that whole span into 24; a part divides only the daylight, or
#: only the night, into 8. Same words, different spans.
DAY_NIGHT_DEFINITION = (
    "A day starts at the time of sunrise and ends at the time of sunset. A "
    "night starts at the time of sunset and ends at the time of next day's "
    "sunrise."
)

#: "we divide the length of the day/night into 8 equal parts"
PARTS_PER_PERIOD = 8

#: Footnote 8, from 4.2: the reduction convention every longitude formula in
#: the book relies on.
LONGITUDE_REDUCTION_NOTE = (
    "When adding or subtracting longitudes, we should subtract 360\u00b0 if we get "
    "more than 360\u00b0 and we should add 360\u00b0 if we get less than 0\u00b0. Adding or "
    "subtracting 360\u00b0 means going around the zodiac once and coming to the "
    "same position. We should finally reduce all longitudes to a value between "
    "0\u00b0 and 360\u00b0, by adding or subtracting 360\u00b0 as many times as needed."
)

#: Footnote 9 to 4.3, which offers a variant for **all six**, not only Kaala.
#: Settings.upagraha_rise_point selects between them; the book's own text uses
#: the middle for five and the beginning for Maandi.
RISE_POINT_VARIANT_NOTE = (
    "Some scholars suggest that Kaala rises at the beginning of Sun's part. "
    "The same thing applies to others."
)

#: 4.3 Nature of each time-based upagraha, "similar to" a graha.
UPAGRAHA_NATURE: dict[int, int] = {
    Upagraha.KAALA: Graha.SUN,
    Upagraha.MRITYU: Graha.MARS,
    Upagraha.ARTHA_PRAHARAKA: Graha.MERCURY,
    Upagraha.YAMA_GHANTAKA: Graha.JUPITER,
    Upagraha.GULIKA: Graha.SATURN,
    Upagraha.MAANDI: Graha.SATURN,
}

#: 4.3 The eight-slot cycle behind Table 10: the seven grahas in weekday order,
#: then a lord-less slot. Every row of Table 10 is this cycle rotated.
PART_LORD_CYCLE: tuple[int | None, ...] = (
    Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
    Graha.JUPITER, Graha.VENUS, Graha.SATURN, None,
)

#: Table 10, transcribed as printed. Rows are weekdays Sunday..Saturday, each
#: giving the lords of the eight parts. ``None`` is the book's dash.
#: These are checked against the generated cycle in the chapter 4 tests, so a
#: transcription slip in either one is caught.
_S, _MO, _MA, _ME, _J, _V, _SA = (Graha.SUN, Graha.MOON, Graha.MARS,
                                  Graha.MERCURY, Graha.JUPITER, Graha.VENUS,
                                  Graha.SATURN)
TABLE_10_DAY = (
    (_S, _MO, _MA, _ME, _J, _V, _SA, None),      # Sunday
    (_MO, _MA, _ME, _J, _V, _SA, None, _S),      # Monday
    (_MA, _ME, _J, _V, _SA, None, _S, _MO),      # Tuesday
    (_ME, _J, _V, _SA, None, _S, _MO, _MA),      # Wednesday
    (_J, _V, _SA, None, _S, _MO, _MA, _ME),      # Thursday
    (_V, _SA, None, _S, _MO, _MA, _ME, _J),      # Friday
    (_SA, None, _S, _MO, _MA, _ME, _J, _V),      # Saturday
)
TABLE_10_NIGHT = (
    (_J, _V, _SA, None, _S, _MO, _MA, _ME),      # Sunday
    (_V, _SA, None, _S, _MO, _MA, _ME, _J),      # Monday
    (_SA, None, _S, _MO, _MA, _ME, _J, _V),      # Tuesday
    (_S, _MO, _MA, _ME, _J, _V, _SA, None),      # Wednesday
    (_MO, _MA, _ME, _J, _V, _SA, None, _S),      # Thursday
    (_MA, _ME, _J, _V, _SA, None, _S, _MO),      # Friday
    (_ME, _J, _V, _SA, None, _S, _MO, _MA),      # Saturday
)
