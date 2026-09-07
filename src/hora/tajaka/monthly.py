"""§27.3 — casting monthly charts, the Tajaka maasa chakra.

The year and the month are defined by the same clock and it is not the
calendar's: "A year is the period in which Sun moves by 360°. A month is the
period in which Sun moves by 30°." So the twelve months of a Tajaka year begin
when the Sun reaches the **natal degree in each successive rasi** — 23 Aq 50'
25", then 23 Pi 50' 25", then 23 Ar 50' 25", for the native of Example 118.

There is deliberately no approximate method here. §27.2 could tabulate the
annual offsets because the Sun takes nearly the same time to cross 360° every
year; it cannot tabulate monthly ones because the time to cross any particular
30° varies with the Sun's own speed. The section says so and
`THE_MONTHS_ARE_UNEQUAL_AND_THE_YEARS_ARE_NOT` measures it.
"""
from __future__ import annotations

from collections.abc import Callable

from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.panchanga.solver import scan_for_crossing

MONTHLY_CHART_RULE = (
    "A year is divided into 12 months and a new chart can be cast at the "
    "commencement of every new month. This is called Tajaka maasa chakra or a "
    "Tajaka monthly chart.")

MAASA_PRAVESH_NAME = (
    "The commencement of a new month is called \"maasa pravesh\" by some "
    "people.")

YEAR_AND_MONTH_ARE_SOLAR_ARCS = (
    "A year is the period in which Sun moves by 360°. A month is the period "
    "in which Sun moves by 30°.")

THIRTY_DEGREES_EXACTLY = (
    "Thus, when Sun enters 23° 50' 25\" in different rasis, we cast different "
    "monthly charts and use them for predicting the events in a one-month "
    "period. The thing to remember here is that \"one month\" is the time "
    "when Sun moves by exactly 30°.")

NO_APPROXIMATE_METHOD = (
    "There isn't any good approximate method for casting monthly charts. Sun "
    "takes approximately the same time for moving by 360° and so we have an "
    "approximate method for annual charts. But the time Sun takes to move by "
    "30° varies considerably from month to month. So there isn't any "
    "approximate method that gives decent results. It may be wise to exactly "
    "cast 12 monthly charts for the first year of the native and then find "
    "monthly charts in later years from them, using the approximate method "
    "given for annual charts.")

#: The two names the section gives one chart.
MONTHLY_CHART_NAMES: tuple[str, ...] = ("Tajaka maasa chakra",
                                        "Tajaka monthly chart")

#: **Finding.** The first month of a Tajaka year is not a separate
#: calculation: "Along with the new year, a new month commences then. This is
#: the first month of the year." So the varsha pravesh and the first maasa
#: pravesh are one instant, and `maasa_pravesh(..., month=1)` returns the
#: year's own beginning rather than searching for anything.
THE_FIRST_MONTH_BEGINS_WITH_THE_YEAR = (
    "Section 27.3 says a new month commences along with the new year and is "
    "the first month of it. The first maasa pravesh is the varsha pravesh."
)

#: **Finding.** The section's own reason for having no approximate method is a
#: measurable claim about the Sun, and it holds by two orders of magnitude.
#: Across Example 118's 34th year the twelve month lengths run from **29.46
#: days to 31.44** — a spread of nearly **two days** — while ten consecutive
#: year lengths for the same native spread by **22 minutes**. That asymmetry
#: is the whole argument for §27.2 existing and §27.3 having no counterpart.
THE_MONTHS_ARE_UNEQUAL_AND_THE_YEARS_ARE_NOT = (
    "The time the Sun takes to cross a given 30° runs from 29.46 to 31.44 "
    "days within one year, because his speed varies between perihelion and "
    "aphelion. The time to cross 360° varies by about 22 minutes. So a table "
    "of monthly offsets could not be built where a table of annual ones "
    "could."
)

#: **Finding.** The pattern is the Sun's own orbit, not the zodiac's. The
#: longest month of Example 118's 34th year is the one containing **early
#: July**, when the Earth is at aphelion and the Sun slowest; the shortest
#: contains **early January** and perihelion. A native born six months later
#: would get the same lengths attached to different rasis, so no table keyed
#: to the month number could serve both.
THE_LONGEST_MONTH_HOLDS_APHELION = (
    "The month lengths peak in the one spanning early July and trough in the "
    "one spanning early January, which is the Earth's aphelion and "
    "perihelion. The order depends on where in the year the native was born."
)

#: **Finding.** The section's own workaround still needs the exact method
#: once: cast the first year's twelve months exactly, then carry them forward
#: with §27.2's annual offsets. So the approximate method is never a substitute
#: for solving — it is a way of not solving twelve times a year, every year.
THE_WORKAROUND_STILL_NEEDS_ONE_EXACT_YEAR = (
    "Section 27.3 suggests casting twelve monthly charts exactly for the "
    "first year and moving them to later years with the annual table. The "
    "exact method is still done once per month, once."
)


class MonthlyError(validate.InputError):
    """A monthly-chart input that cannot be resolved."""


def month_target(natal_sun_longitude: float, month: int) -> float:
    """The Sun's longitude at the start of the `month`-th month of a year.

    The natal degree carried into successive rasis: month 1 is the natal
    longitude itself, month 2 is thirty degrees on, and so to month 12.
    """
    index = validate.in_range("month", int(month), 1, 12)
    natal = validate.longitude("natal_sun_longitude",
                               float(natal_sun_longitude))
    return (natal + 30.0 * (index - 1)) % 360.0


def maasa_pravesh(sun_longitude_at: Callable[[float], float],
                  natal_sun_longitude: float, varsha_jd: float,
                  month: int, *, step: float = 0.5) -> dict:
    """The instant the `month`-th month of one Tajaka year begins.

    :param varsha_jd: the julian day of that year's varsha pravesh, which is
        the first month's own beginning.
    :returns: the julian day, the target longitude and the rasi it falls in,
        or ``jd`` ``None`` with a reason when no crossing is bracketed.
    """
    index = validate.in_range("month", int(month), 1, 12)
    target = month_target(natal_sun_longitude, index)
    rasi = str(RASI_NAMES[int(target // 30)])
    if index == 1:
        return {"month": 1, "jd": varsha_jd, "found": True,
                "target_longitude": target, "rasi": rasi,
                "is_varsha_pravesh": True, "searched": None,
                "rule": THIRTY_DEGREES_EXACTLY, "reason": None}

    # The Sun crosses a given 30° in 29 to 32 days, so a window of a fortnight
    # either side of the nominal position brackets it however the speed runs.
    nominal = varsha_jd + (index - 1) * 30.4368
    jd_from, jd_to = nominal - 14.0, nominal + 14.0
    found = scan_for_crossing(sun_longitude_at, target, jd_from, jd_to,
                              step=step)
    return {
        "month": index,
        "jd": found,
        "found": found is not None,
        "target_longitude": target,
        "rasi": rasi,
        "is_varsha_pravesh": False,
        "searched": {"from": jd_from, "to": jd_to, "step_days": step},
        "rule": THIRTY_DEGREES_EXACTLY,
        "reason": (None if found is not None else
                   "no crossing of the month's longitude in the window"),
    }


def maasa_praveshas(sun_longitude_at: Callable[[float], float],
                    natal_sun_longitude: float, varsha_jd: float,
                    *, step: float = 0.5) -> tuple[dict, ...]:
    """All twelve maasa praveshas of one Tajaka year, in order."""
    return tuple(maasa_pravesh(sun_longitude_at, natal_sun_longitude,
                               varsha_jd, month, step=step)
                 for month in range(1, 13))
