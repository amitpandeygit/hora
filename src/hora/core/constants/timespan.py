"""Year lengths used to convert dasa durations to calendar time.

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant — that facade is the
stable internal surface and keeps call sites independent of how the tables are
filed.
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# Time
# --------------------------------------------------------------------------

#: Length of the sidereal year used by JHora for dasha year conversion.
SIDEREAL_YEAR_DAYS = 365.256360417
SAVANA_YEAR_DAYS = 360.0
TROPICAL_YEAR_DAYS = 365.242190
#: JHora's default "365.25 day" civil year for Vimshottari.
CIVIL_YEAR_DAYS = 365.25


# --------------------------------------------------------------------------
# §1.3.7 The solar calendar
#
# Defined by the Sun's *motion*, not by elapsed days: "one year is the time in
# which Sun moves by 360 degrees and one month is the time in which Sun moves
# by 30 degrees". So a solar month is not a fixed number of days — it is 30
# degrees of the Sun, and the Sun does not move at a constant rate.
#
# Not to be confused with SAVANA_YEAR_DAYS above, which is 360 *days*.
# --------------------------------------------------------------------------

SOLAR_YEAR_DEGREES = 360.0
SOLAR_MONTH_DEGREES = 30.0

#: "Each solar month has 30 days, where one day stands for exactly 1 degree
#: motion of Sun."
SOLAR_DAY_DEGREES = 1.0
DAYS_PER_SOLAR_MONTH = 30

#: "This calendar will be used in dasas and in Tajaka analysis."
SOLAR_CALENDAR_USED_IN: tuple[str, ...] = ("dasas", "Tajaka analysis")
