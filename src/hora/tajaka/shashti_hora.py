"""§27.4 — casting sixty-hour charts, the Tajaka shashti-hora chakra.

The nesting continues by the same rule. A year is 360° of solar motion, a
month is 30°, and a shashti-hora is **2°30'** — twelve to the month, a hundred
and forty-four to the year. A chart cast at each is read for the period
commencing then.

The section names the period "sixty hours, i.e. 2.5 days", and that is a name
rather than a duration: 144 x 2.5 days is 360 days and the year is 365.26, so
the average is nearer 60 hours 53 minutes and no single one is 60. See
`SIXTY_HOURS_IS_A_NAME_AND_THE_ARC_IS_THE_RULE`. The section's own worked
example is the demonstration — its first shashti-hora runs 61 hours.
"""
from __future__ import annotations

from collections.abc import Callable

from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.panchanga.solver import scan_for_crossing
from hora.tajaka.monthly import month_target

SHASHTI_HORA_RULE = (
    "A month is again divided into 12 shashti-horas. Each shashti-hora period "
    "consists of 60 hours, i.e. 2.5 days. At the beginning of every "
    "shashti-hora, a Tajaka shashti-hora chakra (Tajaka sixty-hour chart) is "
    "cast. In the period corresponding to each Tajaka sixty-hour chart, Sun "
    "moves by 2°30'.")

SHASHTI_HORA_IS_AN_ARC = (
    "In other words, we can cast a chart after every 2°30' motion of Sun and "
    "use that Tajaka sixty-hour chart to predict events in the 2.5-day period "
    "commencing then. There are exactly 12 such charts in a one-month period.")

FOOTNOTE_78 = "This is popularly known as just \"Tajaka Hora Chakra\"."

#: The names the section and its footnote give one chart.
SHASHTI_HORA_NAMES: tuple[str, ...] = ("Tajaka shashti-hora chakra",
                                       "Tajaka sixty-hour chart",
                                       "Tajaka Hora Chakra")

#: The arc a shashti-hora covers, in degrees. This is the definition that
#: governs; the sixty hours is the label.
SHASHTI_HORA_ARC_DEGREES = 2.5

#: Twelve to a month, and so a hundred and forty-four to a year.
SHASHTI_HORAS_PER_MONTH = 12
SHASHTI_HORAS_PER_YEAR = 144

#: **Finding.** "Sixty hours, i.e. 2.5 days" cannot be a duration and an arc
#: at once. Twelve times 2.5 days is 30 days and a Tajaka month runs 29.46 to
#: 31.44; a hundred and forty-four times 2.5 days is 360 days and the year is
#: 365.26. Measured across Example 118's 34th year the 144 shashti-horas run
#: from **58.86 to 62.94 hours**, averaging **60.88**, and **not one of them
#: is within a minute of sixty**. The section's own worked example is the
#: demonstration: its first shashti-hora is **61.05 hours** long.
SIXTY_HOURS_IS_A_NAME_AND_THE_ARC_IS_THE_RULE = (
    "A shashti-hora is defined twice over, as sixty hours and as 2°30' of "
    "solar motion, and the two disagree by about one and a half percent "
    "because 144 x 2.5 days is 360 days and a year is 365.26. The arc is what "
    "the section computes with, including in its own example."
)

#: **Finding.** The same shape now three times in one chapter. D-78 has a
#: stated year length the table does not use; §27.3 has months the section
#: calls twelve equal parts and then shows are not; §27.4 has a period named
#: for a duration it never has. Each time a round figure sits beside an arc
#: rule, and each time the arc rule is what the worked example follows.
THE_ROUND_FIGURE_NEVER_GOVERNS = (
    "Section 27.2's stated year, section 27.3's twelve months and section "
    "27.4's sixty hours are all round figures printed beside an exact arc "
    "rule. The arc rule is what every worked example uses."
)


class ShashtiHoraError(validate.InputError):
    """A shashti-hora input that cannot be resolved."""


def shashti_hora_target(natal_sun_longitude: float, month: int,
                        index: int) -> float:
    """The Sun's longitude at the start of one shashti-hora.

    :param month: 1 to 12, the Tajaka month within the year.
    :param index: 1 to 12, the shashti-hora within that month. Index 1 is the
        month's own beginning — "The first shashti-hora of the month also
        starts then."
    """
    place = validate.in_range("index", int(index), 1,
                              SHASHTI_HORAS_PER_MONTH)
    base = month_target(natal_sun_longitude, month)
    return (base + SHASHTI_HORA_ARC_DEGREES * (place - 1)) % 360.0


def shashti_hora(sun_longitude_at: Callable[[float], float],
                 natal_sun_longitude: float, maasa_jd: float, month: int,
                 index: int, *, step: float = 0.1) -> dict:
    """The instant one shashti-hora of one Tajaka month begins.

    :param maasa_jd: the julian day of that month's maasa pravesh, which is
        the first shashti-hora's own beginning.
    """
    place = validate.in_range("index", int(index), 1,
                              SHASHTI_HORAS_PER_MONTH)
    target = shashti_hora_target(natal_sun_longitude, month, place)
    rasi = str(RASI_NAMES[int(target // 30)])
    if place == 1:
        return {"month": int(month), "index": 1, "jd": maasa_jd,
                "found": True, "target_longitude": target, "rasi": rasi,
                "is_maasa_pravesh": True, "searched": None,
                "rule": SHASHTI_HORA_IS_AN_ARC, "reason": None}

    # The arc takes between 58 and 63 hours anywhere in the year, so a window
    # of a day and a half either side of the nominal position brackets it.
    nominal = maasa_jd + (place - 1) * 2.5
    jd_from, jd_to = nominal - 1.5, nominal + 1.5
    found = scan_for_crossing(sun_longitude_at, target, jd_from, jd_to,
                              step=step)
    return {
        "month": int(month),
        "index": place,
        "jd": found,
        "found": found is not None,
        "target_longitude": target,
        "rasi": rasi,
        "is_maasa_pravesh": False,
        "searched": {"from": jd_from, "to": jd_to, "step_days": step},
        "rule": SHASHTI_HORA_IS_AN_ARC,
        "reason": (None if found is not None else
                   "no crossing of the shashti-hora's longitude in the "
                   "window"),
    }


def shashti_horas(sun_longitude_at: Callable[[float], float],
                  natal_sun_longitude: float, maasa_jd: float, month: int,
                  *, step: float = 0.1) -> tuple[dict, ...]:
    """All twelve shashti-horas of one Tajaka month, in order."""
    return tuple(shashti_hora(sun_longitude_at, natal_sun_longitude,
                              maasa_jd, month, index, step=step)
                 for index in range(1, SHASHTI_HORAS_PER_MONTH + 1))
