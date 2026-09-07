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
from hora.core.settings import Settings

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


#: **Finding.** Source (4) needs day or night for the varsha pravesh, and
#: Example 118's is **4:41 am** — before sunrise. `compute_panchanga` raises
#: for any such instant (OI-149), so the one worked example of harsha bala in
#: the book cannot be scored through the normal path. `year_began_in_daytime`
#: therefore reads sunrise and sunset from the ephemeris directly. It is a
#: workaround for a defect and says so; nothing in `panchanga` is changed.
SOURCE_FOUR_IS_BLOCKED_BY_OI_149 = (
    "Harsha bala's fourth source turns on whether the year began by day or by "
    "night, and Example 118's year begins at 4:41 am. Our compute_panchanga "
    "rejects any instant before sunrise, so the day-or-night question is "
    "answered from the ephemeris's own sunrise and sunset here."
)


def year_began_in_daytime(jd_ut: float, latitude: float, longitude: float,
                          *, altitude: float = 0.0,
                          settings: Settings | None = None) -> dict:
    """Whether `jd_ut` falls between a sunrise and the following sunset.

    Written against the ephemeris rather than `panchanga.day_structure`,
    which cannot answer for a pre-dawn instant — see
    `SOURCE_FOUR_IS_BLOCKED_BY_OI_149` and OI-149.

    :returns: ``daytime``, and the sunrise and sunset that bracket the
        instant, so the caller can check the answer rather than trust it.
    """
    from hora.core.ephemeris import get_ephemeris

    ephemeris = get_ephemeris(settings if settings is not None else Settings())
    # Step back far enough that both a sunrise and a sunset precede the
    # instant even inside a polar-free latitude's longest day.
    start = float(jd_ut) - 2.0
    last_rise = last_set = None
    probe = start
    while probe < float(jd_ut):
        rise = ephemeris.sunrise(probe, latitude, longitude, altitude)
        fall = ephemeris.sunset(probe, latitude, longitude, altitude)
        if rise is not None and rise < float(jd_ut):
            last_rise = rise if last_rise is None else max(last_rise, rise)
        if fall is not None and fall < float(jd_ut):
            last_set = fall if last_set is None else max(last_set, fall)
        probe += 1.0
    if last_rise is None or last_set is None:
        raise HarshaError(
            "no sunrise and sunset were found in the two days before this "
            "instant; section 28.3's fourth source cannot be answered")
    return {
        "jd_ut": float(jd_ut),
        "daytime": last_rise > last_set,
        "last_sunrise_jd": last_rise,
        "last_sunset_jd": last_set,
        "why": SOURCE_FOUR_IS_BLOCKED_BY_OI_149,
    }


# --------------------------------------------------------------------------
# Example 119 — harsha bala for Chart 66
# --------------------------------------------------------------------------

EXAMPLE_119 = (
    "Let us find Harsha bala of planets for the annual chart of Example 118.")

#: The example's four steps, verbatim. Two typographical slips in step (3)
#: are kept as printed — see `EXAMPLE_119_HAS_TWO_SLIPS_IN_STEP_THREE`.
EXAMPLE_119_STEPS: tuple[str, ...] = (
    ("Only Moon is in the prescribed house (the 3rd house in Moon's case). He "
     "gets 5 units."),
    "No planet is in exaltation or own sign.",
    ("Venus in 1st, Mercury in 2nd, Moon in 3rd are the feminine planets in "
     "prescribed houses. Jupiter in 4th is in the masculine planet in the "
     "prescibed house."),
    ("Because the new year started at 4:42 am, i.e. during the night, we give "
     "5 units each to the feminine planets – Moon, Mercury, Venus and "
     "Saturn."),
)

EXAMPLE_119_TOTAL = (
    "Adding all the sources, we get 15 for Moon, 10 for Mercury and Venus, 5 "
    "for Jupiter and Saturn and zero for Sun and Mars.")

#: The example's own answer, by graha id.
EXAMPLE_119_UNITS: dict[int, int] = {
    0: 0,    # Sun
    1: 15,   # Moon
    2: 0,    # Mars
    3: 10,   # Mercury
    4: 5,    # Jupiter
    5: 10,   # Venus
    6: 5,    # Saturn
}

#: **Book defect.** Step (3) reads "Jupiter in 4th is in the masculine planet
#: in the prescibed house" — an intruded "in the" and "prescibed" for
#: "prescribed". The sense is plain and the arithmetic is unaffected;
#: recorded rather than silently corrected.
EXAMPLE_119_HAS_TWO_SLIPS_IN_STEP_THREE = (
    "Step (3) prints \"is in the masculine planet\" for \"is the masculine "
    "planet\", and \"prescibed\" for \"prescribed\". Neither changes a "
    "number."
)

#: **Finding.** The example says the year "started at 4:42 am" where Example
#: 118 solved it to **4:41:21** and Chart 66 is drawn for 4:41. The 4:42 is
#: §27.2's **approximate** figure, which was 4:42:24. Nothing turns on it —
#: both are hours before sunrise and both are night — but the two methods'
#: answers are being used interchangeably a page apart.
THE_EXAMPLE_QUOTES_THE_APPROXIMATE_TIME = (
    "Example 118 gives 4:41:21 am and Chart 66 is drawn for 4:41 am. Example "
    "119 says 4:42 am, which is section 27.2's approximate answer. Both are "
    "well before sunrise, so source (4) is unaffected."
)

#: **Finding.** The Moon scores 15 here and 15 is not her ceiling — she is
#: one of the four planets that can reach 20. She misses only source (2), so
#: this chart's strongest planet is one dignity short of the top grade, and
#: the three planets that can never reach 20 are not the reason.
THE_MOON_MISSES_TWENTY_BY_ONE_SOURCE = (
    "The Moon takes sources (1), (3) and (4) and fails only (2), no planet "
    "in the chart being exalted or in its own sign. Her 15 is a miss rather "
    "than a ceiling."
)
