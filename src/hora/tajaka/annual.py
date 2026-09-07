"""§27.1 — casting a Tajaka annual chart.

The rule is a moment and a place, and the section is exact about both. The
moment is when the Sun returns to the **exact** position he held at birth —
the section italicises it and bolds both words — so the chart is not cast for
the birthday, nor for a fixed number of days after the last return. It is
solved for. The place is the **birthplace**, whatever the native's address at
the time, which is the one thing here that a solar-return chart in another
tradition would get differently.

One question the section does not answer: "the position occupied by him at the
time of one's birth" is a longitude, and a longitude is sidereal or tropical.
This engine is sidereal everywhere, so the return is solved against the natal
**sidereal** longitude, which makes the interval a sidereal year. A tropical
reading would place each return about twenty minutes earlier per year of age,
which is some five degrees of ascendant. See OI-151; the section's own example
is what settles it.
"""
from __future__ import annotations

from collections.abc import Callable

from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.panchanga.solver import scan_for_crossing

#: The section's own approximation, kept as printed. It is the reason a year
#: is a year and not the reason a return is where it is: the chart is solved
#: for, never stepped to.
SUN_MOVES_30_DEGREES_A_MONTH = (
    "Sun moves with respect to earth at the rate of 30° per month. He takes "
    "one year to complete one cycle through the zodiac. He returns to the "
    "position occupied by him at the time of one's birth after every one-year "
    "period."
)

#: The rule itself. The book italicises the whole sentence and bolds "exact
#: moment" and "exact position".
VARSHA_PRAVESH_RULE = (
    "At the exact moment when Sun returns to the exact position he occupied "
    "at the time of a person's birth, a new year is said to commence in the "
    "life of that person. A chart can be cast for the commencement of the new "
    "year. This is called a Tajaka varsha chakra or a Tajaka annual chart."
)

#: The place rule, and the only part of the casting that is not the ephemeris.
BIRTHPLACE_RULE = (
    "The longitude and latitude of the birthplace must be used in casting "
    "this chart, irrespective of the place of living at the commencement of "
    "the new year."
)

VARSHA_PRAVESH_NAME = (
    "The commencement of a new year is called \"varsha pravesh\" by some "
    "people. Varsha means a year and pravesh means entry.")

#: The gloss, as two words.
VARSHA_PRAVESH_MEANS: dict[str, str] = {"varsha": "a year", "pravesh": "entry"}

#: **Finding.** The place rule is the sharpest thing on the page and the
#: easiest to get wrong. A solar return cast for the native's **current**
#: residence is a different chart — the same instant against a different
#: horizon — and the ascendant can land anywhere. §27.1 forecloses that
#: reading in one sentence, so `varsha_pravesh` takes no place at all and the
#: caller supplies the birth place to `compute_chart` as it would for a natal.
THE_PLACE_IS_THE_BIRTHPLACE_AND_NOT_THE_RESIDENCE = (
    "Section 27.1 says the birthplace's longitude and latitude must be used "
    "irrespective of where the native lives when the year begins. Only the "
    "moment is recomputed; the horizon is the natal one."
)

#: **Finding.** "At the exact moment" rules out the two shortcuts a reader
#: might take. The chart is not cast for the birthday — the return drifts
#: through the calendar day by day — and it is not cast a fixed 365 days after
#: the last one, which Part 4's opening could be read as licensing. It is
#: solved for, which is why this function searches rather than adds.
THE_RETURN_IS_SOLVED_FOR_NOT_STEPPED_TO = (
    "The section bolds \"exact moment\" and \"exact position\". Neither the "
    "birthday nor a fixed 365-day step gives that instant, so the crossing is "
    "found by search."
)

#: Not supplied. Footnote 75 hangs off "Tajaka annual chart" and its text has
#: not been printed here.
FOOTNOTE_75_NOT_SUPPLIED = (
    "Section 27.1 marks footnote 75 on the words \"Tajaka annual chart\". The "
    "footnote itself is not on the page supplied.")


class TajakaError(validate.InputError):
    """A Tajaka input that cannot be resolved."""


def varsha_pravesh(sun_longitude_at: Callable[[float], float],
                   natal_sun_longitude: float, birth_jd: float,
                   year: int, *, step: float = 0.5) -> dict:
    """The instant the native's `year`-th Tajaka year begins.

    :param sun_longitude_at: julian day -> the Sun's sidereal longitude.
        Passed in so this stays independent of how positions are sourced.
    :param natal_sun_longitude: the Sun's longitude in the natal chart. The
        target is this value exactly; §27.1 says "the exact position".
    :param birth_jd: the julian day of birth, universal time.
    :param year: 1 is the year that begins at birth itself, 2 the first
        return, and so on — the count the book uses when it speaks of a
        native's nth year.
    :returns: the julian day of the varsha pravesh, with the search window
        used, or ``jd`` ``None`` and a reason when no crossing is bracketed.
    """
    index = validate.in_range("year", int(year), 1, 200)
    target = validate.longitude("natal_sun_longitude",
                                float(natal_sun_longitude))
    returns = index - 1
    if returns == 0:
        return {
            "year": index, "returns_completed": 0, "jd": birth_jd,
            "found": True, "target_longitude": target,
            "is_birth_itself": True,
            "searched": None,
            "rule": VARSHA_PRAVESH_RULE,
            "place": BIRTHPLACE_RULE,
            "reason": None,
        }

    # A sidereal year is about 365.2564 days; bracket generously on both
    # sides so a crossing is never missed at the window edge.
    approximate = birth_jd + returns * 365.2564
    jd_from, jd_to = approximate - 20.0, approximate + 20.0
    found = scan_for_crossing(sun_longitude_at, target, jd_from, jd_to,
                              step=step)
    return {
        "year": index,
        "returns_completed": returns,
        "jd": found,
        "found": found is not None,
        "target_longitude": target,
        "is_birth_itself": False,
        "searched": {"from": jd_from, "to": jd_to, "step_days": step},
        "rule": VARSHA_PRAVESH_RULE,
        "place": BIRTHPLACE_RULE,
        "reason": (None if found is not None else
                   "no crossing of the natal solar longitude in the window; "
                   "widen it or check the natal longitude"),
    }


def rasi_of(longitude: float) -> str:
    """The rasi a longitude falls in, by name."""
    return str(RASI_NAMES[int(validate.longitude("longitude",
                                                 float(longitude)) // 30)])
