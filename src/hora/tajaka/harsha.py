"""§28.3 — harsha bala, the strength of cheerfulness.

Four sources, five units each, twenty at most. Three of the four are about
where a planet sits and the fourth about when the year began, so harsha bala
is a property of one annual chart and not of the nativity.

Two things fall out of the arithmetic and are recorded rather than smoothed
over. §28.3 sorts the seven into masculine and feminine where chapter 3's own
table makes Mercury and Saturn **neuter** — see D-79. And the joy houses of source
(1) sit in the wrong gender half for the Sun, Venus and Saturn, so those three
can never collect all four sources and can never be "exceedingly strong". See
`THREE_PLANETS_CAN_NEVER_SCORE_TWENTY`.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES

HARSHA_BALA_RULE = (
    "Harsha bala of seven planets is found by adding the strengths given by "
    "the following 4 sources of strength:")

FOOTNOTE_80 = (
    "Harsha means \"cheerful\" and bala means \"strength\". This is the "
    "strength of cheerfulness.")

HARSHA_MEANS = "cheerful"
BALA_MEANS = "strength"

#: Source (1): the house each planet scores in, and nowhere else.
HARSHA_HOUSES: dict[int, int] = {
    0: 9,    # Sun
    1: 3,    # Moon
    2: 6,    # Mars
    3: 1,    # Mercury
    4: 11,   # Jupiter
    5: 5,    # Venus
    6: 12,   # Saturn
}

#: §28.3's own split of the seven, which is not §3's.
HARSHA_FEMININE: tuple[int, ...] = (1, 3, 5, 6)      # Moon, Merc, Ven, Sat
HARSHA_MASCULINE: tuple[int, ...] = (0, 2, 4)        # Sun, Mars, Jupiter

#: Source (3): the houses each group scores in. Together they are all twelve.
FEMININE_HOUSES: tuple[int, ...] = (1, 2, 3, 7, 8, 9)
MASCULINE_HOUSES: tuple[int, ...] = (4, 5, 6, 10, 11, 12)

#: The four sources, verbatim and in order.
HARSHA_SOURCES: tuple[str, ...] = (
    ("Sun in the 9th house, Moon in the 3rd house, Mars in the 6th house, "
     "Mercury in the 1st house, Jupiter in the 11th house, Venus in the 5th "
     "house and Saturn in the 12th house get 5 units. They get zero units in "
     "other houses."),
    "A planet in exaltation or own sign gets 5 units (else zero units).",
    ("Feminine planets (Moon, Mercury, Venus and Saturn) get 5 units in the "
     "1st, 2nd, 3rd 7th, 8th and 9th houses. Masculine planets (Sun, Mars and "
     "Jupiter) get 5 units in the 4th, 5th, 6th, 10th, 11th and 12th "
     "houses."),
    ("If the new year starts in the daytime, masculine planets get 5 units "
     "each. If the new year starts in the night time, feminine planets get 5 "
     "units each."),
)

#: Units per source, and the ceiling four of them make.
HARSHA_UNITS_PER_SOURCE = 5
HARSHA_MAXIMUM = 20

HARSHA_GRADE_RULE = (
    "A planet with 20 units of strength is exceedingly strong. A planet with "
    "15 units of strength is fully strong. A planet with 10 units of strength "
    "is of average strength. A planet with 5 units of strength has only a "
    "little strength. A planet with zero units of strength has no strength at "
    "all.")

#: Every attainable total has a grade, and the section names all five.
HARSHA_GRADES: dict[int, str] = {
    20: "exceedingly strong",
    15: "fully strong",
    10: "average strength",
    5: "only a little strength",
    0: "no strength at all",
}

#: **Finding.** The seven houses of source (1) are the seven the western
#: tradition calls a planet's **joy** — Mercury the 1st, Moon the 3rd, Venus
#: the 5th, Mars the 6th, Sun the 9th, Jupiter the 11th, Saturn the 12th — and
#: footnote 80 glosses harsha as "cheerful". The correspondence is recorded as
#: an observation about the numbers; nothing here is decided from it, and the
#: book is the source for every value.
THE_HARSHA_HOUSES_ARE_THE_PLANETARY_JOYS = (
    "Source (1) gives Mercury the 1st, the Moon the 3rd, Venus the 5th, Mars "
    "the 6th, the Sun the 9th, Jupiter the 11th and Saturn the 12th. Those "
    "are the seven houses western astrology calls the planets' joys, and "
    "footnote 80 glosses harsha as cheerful."
)

#: **Finding.** Sources (3) and (4) both key on gender, so the two together
#: give a planet 10, 5 or 0 and never anything between. And (4) scores every
#: member of one group and no member of the other, so exactly three planets or
#: exactly four collect it in any given year — never a mixture.
SOURCES_THREE_AND_FOUR_BOTH_TURN_ON_GENDER = (
    "Source (3) pays a planet in its own gender's half of the houses and "
    "source (4) pays a whole gender for the time of day. In a daytime year "
    "the three masculine planets take source (4) and the four feminine ones "
    "take none of it."
)

#: **Finding.** The Sun, Venus and Saturn can never be "exceedingly strong".
#: Source (1) puts the Sun in the 9th, Venus in the 5th and Saturn in the
#: 12th, and source (3) puts the 9th in the feminine half while the Sun is
#: masculine, and the 5th and 12th in the masculine half while Venus and
#: Saturn are feminine. So for those three the two house sources are mutually
#: exclusive and fifteen is the ceiling. The other four can reach twenty.
THREE_PLANETS_CAN_NEVER_SCORE_TWENTY = (
    "The Sun's joy house is feminine and he is masculine; Venus's and "
    "Saturn's are masculine and they are feminine. Those three can collect "
    "source (1) or source (3) but never both, so their harsha bala tops out "
    "at fifteen and the top grade is out of their reach."
)

#: **Book deviation, D-79.** §28.3 calls Mercury and Saturn **feminine**;
#: chapter 3's own table of graha attributes makes both **neuter**, with only
#: Moon and Venus feminine. Harsha bala needs a two-way split and the section
#: supplies one, so the technique is computed on §28.3's grouping — but the
#: two classifications are the same author's and they disagree.
THE_GENDER_SPLIT_IS_NOT_CHAPTER_THREES = (
    "Section 28.3 groups Moon, Mercury, Venus and Saturn as feminine. "
    "Chapter 3's own table of graha attributes makes Mercury and Saturn "
    "neuter. Harsha bala uses section 28.3's grouping because it is the "
    "section that defines the technique."
)


def _ordinal(n: int) -> str:
    """1st, 2nd, 3rd, 4th ... — spelt out rather than built by pasting "th"."""
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }"


class HarshaError(validate.InputError):
    """A harsha bala input that cannot be resolved."""


def is_feminine(graha: int) -> bool:
    """§28.3's own grouping, which is not chapter 3's. See D-79."""
    index = validate.in_range("graha", int(graha), 0, 6)
    return index in HARSHA_FEMININE


def harsha_bala(graha: int, house: int, *, dignified: bool | None,
                daytime: bool) -> dict:
    """One planet's harsha bala in one annual chart.

    :param house: the house it occupies in the annual chart, 1 to 12.
    :param dignified: whether it is in exaltation or its own sign. ``None``
        leaves source (2) undecided rather than scoring it zero, because "not
        exalted" and "not asked" are different answers.
    :param daytime: whether the new year commenced in the daytime.
    """
    index = validate.in_range("graha", int(graha), 0, 6)
    place = validate.in_range("house", int(house), 1, 12)
    feminine = is_feminine(index)
    own_houses = FEMININE_HOUSES if feminine else MASCULINE_HOUSES

    units: list[int | None] = [
        HARSHA_UNITS_PER_SOURCE if HARSHA_HOUSES[index] == place else 0,
        (None if dignified is None else
         HARSHA_UNITS_PER_SOURCE if dignified else 0),
        HARSHA_UNITS_PER_SOURCE if place in own_houses else 0,
        HARSHA_UNITS_PER_SOURCE if feminine != bool(daytime) else 0,
    ]
    details = (
        (f"section 28.3 gives {GRAHA_NAMES[index]} the "
         f"{_ordinal(HARSHA_HOUSES[index])} house"),
        ("not supplied, so this source is undecided" if dignified is None else
         "in exaltation or own sign" if dignified else
         "neither exalted nor in its own sign"),
        (f"{'feminine' if feminine else 'masculine'} planets score in "
         f"{', '.join(str(h) for h in own_houses)}"),
        f"the year began in the {'daytime' if daytime else 'night time'}",
    )
    labels = ("its own house", "exaltation or own sign",
              "its gender's houses", "the time the year began")
    sources = tuple({"source": number, "for": label, "units": value,
                     "detail": detail}
                    for number, (label, value, detail)
                    in enumerate(zip(labels, units, details, strict=True), 1))
    total = sum(value for value in units if value is not None)
    undecided = any(value is None for value in units)
    return {
        "graha": index,
        "graha_name": str(GRAHA_NAMES[index]),
        "house": place,
        "feminine": feminine,
        "daytime": bool(daytime),
        "sources": sources,
        "units": total,
        "at_least": total,
        "at_most": total + (HARSHA_UNITS_PER_SOURCE if undecided else 0),
        "undecided": undecided,
        "grade": None if undecided else HARSHA_GRADES[total],
        "grade_rule": HARSHA_GRADE_RULE,
    }
