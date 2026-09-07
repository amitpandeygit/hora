"""§27.2 — the approximate method, and Table 71.

The exact method solves for the Sun. This one adds a stored offset to the
birth data, and the section is candid about why: "this can be a laborious
calculation to do manually". It is a hand method, and it survives here because
the book prints it and because it is a second opinion on `annual.varsha_pravesh`
— Example 118 is worked both ways and the two land a minute apart.

Table 71 is stored exactly as printed. It is **not** recomputed from the year
length the section states, because the two disagree: the sentence gives the
sidereal year as 365 days 6 hours 9 minutes 12 seconds, and every row of the
table from age 2 to age 100 is built from a year about 2.3 seconds shorter.
See `THE_STATED_YEAR_AND_THE_TABLE_DISAGREE` and D-78.
"""
from __future__ import annotations

import datetime as dt

from hora.core import validate

SECTION_INTRO = (
    "The exact time of the commencement of new year is determined by finding "
    "the exact time when Sun enters the exact position occupied by him at the "
    "time of one's birth. However, this can be a laborious calculation to do "
    "manually. To make this task less challenging, some scholars devised "
    "approximate methods based on the number of days in an average solar "
    "year. A sidereal solar year has 365 days 6 hours 9 minutes and 12 "
    "seconds. Based on this, the amount of time to be added to the birthdata "
    "to find the varsha pravesh data is given in Table 71.")

#: The section's stated length of a sidereal solar year, in days.
STATED_SIDEREAL_YEAR_DAYS = 365 + (6 * 3600 + 9 * 60 + 12) / 86400.0

#: Table 71 exactly as printed: age in years -> (days, hours, minutes,
#: seconds). The days column is already reduced modulo seven, which is why
#: age 6 shows zero days.
TABLE_71: dict[int, tuple[int, int, int, int]] = {
    1: (1, 6, 9, 12),
    2: (2, 12, 18, 18),
    3: (3, 18, 27, 30),
    4: (5, 0, 36, 36),
    5: (6, 6, 45, 48),
    6: (0, 12, 55, 0),
    7: (1, 19, 4, 6),
    8: (3, 1, 13, 18),
    9: (4, 7, 22, 30),
    10: (5, 13, 31, 36),
    20: (4, 3, 3, 12),
    30: (2, 16, 34, 54),
    40: (1, 6, 6, 30),
    50: (6, 19, 38, 6),
    60: (5, 9, 9, 42),
    70: (3, 22, 41, 24),
    80: (2, 12, 13, 0),
    90: (1, 1, 44, 36),
    100: (6, 15, 16, 12),
}

TABLE_71_TITLE = "Approximate Annual Chart Data"

#: §27.2's five steps, verbatim and in order.
PROCEDURE: tuple[str, ...] = (
    "Find the birthday as per western calendar in the required year.",
    ("Find the years completed. Find the corresponding days, hours, minutes "
     "and seconds from Table 71. If the age is not in the list, express it as "
     "a sum of entries found in the table and add their values. For example, "
     "suppose someone finished 46 years. Then add the values given for 40 "
     "years and 6 years."),
    ("Add the days found above to the weekday of birth and find the resulting "
     "weekday. Find the nearest date to the birthday found in (1) that falls "
     "on this weekday. A time equal to the birthtime on this date is taken as "
     "a reference."),
    ("Add the hours, minutes and seconds found in (2) to the reference date "
     "and time found in (3). The result is the date and time of the "
     "commencement of new year."),
    ("Find the planetary positions, lagna etc at this time for the longitude "
     "and latitude of the birthplace."),
)

FOOTNOTE_77 = (
    "Remember that the weekday in Hindu calendar changes at sunrise and not "
    "at 12:00 midnight.")

ACCURACY_REMARK = (
    "Please note that the time found here is wrong only by 1 minute. In some "
    "examples, the error resulting from the approximation can be higher. "
    "However, this approximate method is very convenient and quick.")

AYANAMSA_NOTE = (
    "Errors due to ayanamsa and approximations in the calculation of Sun's "
    "longitude cause greater errors than this approximation. As long as one "
    "takes the correct nonlinear nature of ayanamsa change into account, "
    "there will not be any considerable discrepancy in the varsha pravesh "
    "times found by people using different ayanamsas. But ignoring the "
    "nonlinear nature of ayanamsa results in considerable errors in varsha "
    "pravesh time. This is because lagna moves 360 times faster than Sun. Any "
    "small errors in Sun's longitude result in errors in lagna which are 360 "
    "times as large.")

#: The ratio the note turns on: the lagna crosses the zodiac once a day and
#: the Sun once a year.
LAGNA_IS_360_TIMES_FASTER_THAN_SUN = 360


class ApproximateError(validate.InputError):
    """An input §27.2's method cannot take."""


#: **Book defect.** The section states the sidereal solar year as 365 days
#: 6 hours 9 minutes 12 seconds and says Table 71 is built "based on this".
#: Only the age-1 row is. Solving each of the other eighteen rows for the year
#: it implies gives **365.2563623 days** every time — an excess of about
#: 6h 9m 9.7s, some 2.3 seconds shorter than the stated figure, and within a
#: quarter-second of the true sidereal year. The stated figure is a rounding
#: of that, and the age-1 row was computed from the rounding rather than from
#: the year the rest of the table uses. The gap reaches **3m 48s at age 100**,
#: which by the section's own 360:1 rule is nearly a whole rasi of lagna. See
#: D-78; the table is stored as printed and nothing is recomputed.
THE_STATED_YEAR_AND_THE_TABLE_DISAGREE = (
    "Section 27.2 gives the sidereal year as 365d 6h 9m 12s. Every Table 71 "
    "row from age 2 to age 100 implies 365d 6h 9m 9.7s instead. Only the "
    "age-1 row follows the stated figure."
)

#: **Finding.** The days column is reduced modulo seven, which is why age 6
#: reads zero days, and that is what makes step (3) a weekday step rather
#: than a date step. It also makes the table's decomposition exact rather
#: than approximate: entries add, because both the day count and the
#: fractional part of a multiple of the year add.
THE_DAYS_COLUMN_IS_MODULO_SEVEN = (
    "Table 71's days run 0 to 6, so age 6 shows zero days. The column is a "
    "weekday offset, not an elapsed count."
)

#: **Finding.** Footnote 77 is the **second** footnote in the book to state
#: the rule our own `day_structure` gets wrong — footnote 71 was the first.
#: Here it is load-bearing rather than incidental: step (3) starts from the
#: weekday of birth, so a native born between midnight and sunrise takes the
#: previous day's weekday and the whole method shifts by a day if that is
#: missed. `approximate_varsha_pravesh` therefore takes the weekday as an
#: argument rather than deriving it. See OI-149.
FOOTNOTE_77_IS_THE_SECOND_STATEMENT_OF_THE_SUNRISE_RULE = (
    "Footnote 71 said a new day starts at sunrise; footnote 77 says it again "
    "for the weekday this method starts from. Our day_structure takes the "
    "first sunrise after local midnight, so it would give a pre-dawn birth "
    "the wrong weekday and the wrong reference date."
)

#: **Finding.** The note is a statement about **our** implementation and not
#: only about hand calculation. It says ayanamsa error dominates the
#: approximation, that a **nonlinear** ayanamsa keeps different ayanamsas in
#: agreement, and that the lagna amplifies any solar error 360-fold. Both
#: claims are checked against this engine rather than taken on trust.
THE_NOTE_IS_A_CONSTRAINT_ON_THE_EPHEMERIS = (
    "Section 27.2 says ayanamsa error exceeds the approximation error, that "
    "the nonlinear nature of ayanamsa change must be taken into account, and "
    "that the lagna magnifies a solar longitude error 360 times."
)


def decompose(age: int) -> tuple[int, ...]:
    """Express `age` as the Table 71 entries §27.2 says to add.

    "If the age is not in the list, express it as a sum of entries found in
    the table and add their values ... suppose someone finished 46 years.
    Then add the values given for 40 years and 6 years." Hundreds, then tens,
    then units — which is the only decomposition the table admits, and the
    one the section's own example takes.
    """
    left = validate.in_range("age", int(age), 0, 199)
    parts: list[int] = []
    for unit in (100, 10, 1):
        while left >= unit and (left // unit) * unit in TABLE_71:
            step = (left // unit) * unit
            parts.append(step)
            left -= step
    # Every age from 0 to 199 is reachable as hundreds, tens and units, all
    # of which Table 71 lists, so nothing is left over. The range check above
    # is what refuses an age the table cannot express.
    assert not left, left
    return tuple(parts)


def offset_for(age: int) -> dict:
    """Table 71's offset for `age` completed years, decomposing if needed.

    :returns: the parts used, the days as a weekday step, and the hours,
        minutes and seconds to add after it.
    """
    parts = decompose(age)
    if not parts:
        return {"age": int(age), "parts": (), "days": 0, "hours": 0,
                "minutes": 0, "seconds": 0, "in_table": True,
                "total_seconds": 0}
    days = hours = minutes = seconds = 0
    for part in parts:
        d, h, m, s = TABLE_71[part]
        days, hours, minutes, seconds = days + d, hours + h, minutes + m, seconds + s
    minutes, seconds = minutes + seconds // 60, seconds % 60
    hours, minutes = hours + minutes // 60, minutes % 60
    days, hours = days + hours // 24, hours % 24
    return {
        "age": int(age),
        "parts": parts,
        "days": days % 7,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "in_table": len(parts) == 1,
        "total_seconds": hours * 3600 + minutes * 60 + seconds,
    }


#: Monday is 0 in :mod:`datetime`; the book counts weekdays by name, so the
#: names are carried and the arithmetic is done on the index.
WEEKDAYS: tuple[str, ...] = ("Monday", "Tuesday", "Wednesday", "Thursday",
                             "Friday", "Saturday", "Sunday")


def approximate_varsha_pravesh(birth_local: dt.datetime, birth_weekday: str,
                               years_completed: int) -> dict:
    """§27.2's five steps, with the birth weekday supplied rather than derived.

    :param birth_local: the birth date and time, in the birthplace's own
        clock. Only the date and the time of day are used.
    :param birth_weekday: the **Hindu** weekday of birth. Footnote 77: it
        changes at sunrise, so a birth between midnight and sunrise carries
        the previous day's weekday. It is an argument and not a derivation
        because `day_structure` gets that case wrong — see OI-149.
    :param years_completed: the years finished, which is the age Table 71 is
        entered with. Example 118's native has finished 33 and enters his
        34th year.
    """
    import datetime as dt

    if birth_weekday not in WEEKDAYS:
        raise ApproximateError(
            f"{birth_weekday!r} is not a weekday; the seven are "
            f"{', '.join(WEEKDAYS)}")
    offset = offset_for(years_completed)

    # (1) the birthday in the required year, by the western calendar.
    birthday = dt.date(birth_local.year + int(years_completed),
                       birth_local.month, birth_local.day)

    # (3) the weekday the days column lands on, and the nearest such date.
    start = WEEKDAYS.index(birth_weekday)
    target = (start + offset["days"]) % 7
    delta = (target - birthday.weekday()) % 7
    if delta > 3:
        delta -= 7
    reference_date = birthday + dt.timedelta(days=delta)
    reference = dt.datetime.combine(reference_date, birth_local.time())

    # (4) the hours, minutes and seconds on top of the reference.
    commencement = reference + dt.timedelta(hours=offset["hours"],
                                            minutes=offset["minutes"],
                                            seconds=offset["seconds"])
    return {
        "years_completed": int(years_completed),
        "year_entered": int(years_completed) + 1,
        "birthday": birthday,
        "offset": offset,
        "birth_weekday": birth_weekday,
        "target_weekday": WEEKDAYS[target],
        "reference": reference,
        "days_from_birthday": delta,
        "commencement": commencement,
        "place": "the longitude and latitude of the birthplace",
        "accuracy": ACCURACY_REMARK,
    }
