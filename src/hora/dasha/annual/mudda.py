"""§30.3 — Mudda dasa, or Varsha Vimsottari dasa.

Vimsottari's 120 years compressed to a solar year of 360 days, seeded from the
**natal** Moon's constellation progressed one constellation a year.
"""

from __future__ import annotations

from hora.core import validate
from hora.core.const import NAKSHATRA_NAMES, Graha
from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

#: §30.3's "Dasa length" paragraph, verbatim.
MUDDA_LENGTH_RULE = (
    "This is essentially Vimsottari dasa with 120 years compressed to a solar "
    "year. If we take a solar year to be of 360 days, with each day "
    "corresponding to the time period in which Sun moves by exactly 1 degree, "
    "we get the dasa of days of a planet by multiplying normal dasa years by "
    "3. For example, Sun dasa is normally for 6 years. By compressing 120 "
    "years to 360 solar days, we find Sun's Varsha Vimsottari dasa to be "
    "6 x 3 = 18 days.")

#: §30.3's "Dasa order" paragraphs, verbatim.
MUDDA_ORDER_RULE = (
    "To initiate dasas, we should progress Moon's natal constellation at the "
    "rate of one constellation per year and use the resulting constellation. "
    "Instead of progressing the constellation, we can also do the following: "
    "Consider (1) Sun, (2) Moon, (3) Mars, (4) Rahu, (5) Jupiter, (6) Saturn, "
    "(7) Mercury, (8) Ketu and (9) Venus. Take the number corresponding to "
    "the lord of Moon's natal constellation (i.e. the lord of the first "
    "Vimsottari dasa in natal chart). Add the number of completed years to "
    "this number. Divide the number by 9 and take the remainder. See the "
    "planet corresponding to that number. First dasa belongs to that planet. "
    "After that, dasas will follow the normal order. Remainder of 0 is "
    "equivalent to 9 and hence shows Venus.")

#: §30.3's "Dasa balance" rule, verbatim.
MUDDA_BALANCE_RULE = (
    "For finding the dasa balance, the fraction of the natal Moon's "
    "constellation yet to be traversed is taken.")

MUDDA_YEAR_DAYS = 360
MUDDA_MULTIPLIER = 3

TABLE_76_TITLE = "Varsha Vimsottari Dasa Days"

#: Table 76 exactly as printed, in its own column order.
TABLE_76: tuple[tuple[str, int], ...] = (
    ("Sun", 18), ("Moon", 30), ("Mars", 21), ("Rahu", 54), ("Jupiter", 48),
    ("Saturn", 57), ("Mercury", 51), ("Ketu", 21), ("Venus", 60))

#: §30.3's numbering, 1 to 9. It is the Vimsottari cycle rotated to start at
#: the Sun, which is Table 76's column order too.
MUDDA_NUMBERS: tuple[int, ...] = (
    int(Graha.SUN), int(Graha.MOON), int(Graha.MARS), int(Graha.RAHU),
    int(Graha.JUPITER), int(Graha.SATURN), int(Graha.MERCURY),
    int(Graha.KETU), int(Graha.VENUS))

NAKSHATRA_SPAN = 360.0 / 27.0


class MuddaError(validate.InputError):
    """A mudda input that cannot be resolved."""


def mudda_days(graha: int) -> int:
    """A planet's Varsha Vimsottari dasa in days: its Vimsottari years x 3."""
    spec = NAKSHATRA_DASHA_SYSTEMS["vimshottari"]
    for lord, years in zip(spec.order, spec.years, strict=True):
        if int(lord) == int(graha):
            return int(years) * MUDDA_MULTIPLIER
    raise MuddaError(f"{graha!r} has no Vimsottari period")


def mudda_number(graha: int) -> int:
    """§30.3's 1-to-9 number for a planet."""
    if int(graha) not in MUDDA_NUMBERS:
        raise MuddaError(f"{graha!r} is not one of the nine")
    return MUDDA_NUMBERS.index(int(graha)) + 1


def natal_nakshatra_lord(moon_longitude: float) -> dict:
    """The lord of the Moon's natal constellation — the first Vimsottari dasa
    lord in the natal chart, which is what §30.3 asks for.
    """
    place = validate.longitude("moon_longitude", float(moon_longitude))
    index = int(place // NAKSHATRA_SPAN)
    spec = NAKSHATRA_DASHA_SYSTEMS["vimshottari"]
    lord = int(spec.order[index % 9])
    travelled = place - index * NAKSHATRA_SPAN
    return {
        "longitude": place,
        "nakshatra": index,
        "nakshatra_name": str(NAKSHATRA_NAMES[index]),
        "lord": lord,
        "traversed": travelled / NAKSHATRA_SPAN,
        "yet_to_traverse": 1.0 - travelled / NAKSHATRA_SPAN,
    }


def first_dasa_lord(*, moon_longitude: float, completed_years: int) -> dict:
    """§30.3's first dasa lord, both ways, with the two answers side by side.

    The section gives a progression and an arithmetic shortcut for it. They
    are the same thing — see `THE_SHORTCUT_IS_EXACT_NOT_APPROXIMATE`.
    """
    years = validate.non_negative("completed_years", float(completed_years))
    natal = natal_nakshatra_lord(moon_longitude)
    spec = NAKSHATRA_DASHA_SYSTEMS["vimshottari"]

    progressed_index = (int(natal["nakshatra"]) + int(years)) % 27
    by_progression = int(spec.order[progressed_index % 9])

    number = mudda_number(int(natal["lord"])) + int(years)
    remainder = number % 9
    by_arithmetic = MUDDA_NUMBERS[(remainder or 9) - 1]

    return {
        "natal": natal,
        "progressed_nakshatra": progressed_index,
        "progressed_nakshatra_name": str(NAKSHATRA_NAMES[progressed_index]),
        "by_progression": by_progression,
        "natal_lord_number": mudda_number(int(natal["lord"])),
        "sum": number,
        "remainder": remainder,
        "by_arithmetic": by_arithmetic,
        "agree": by_progression == by_arithmetic,
        "lord": by_progression,
    }


def mudda_dasa(*, moon_longitude: float, completed_years: int,
               start_jd: float | None = None) -> dict:
    """§30.3's nine dasas, from the first lord with its balance applied."""
    seed = first_dasa_lord(moon_longitude=moon_longitude,
                           completed_years=completed_years)
    order = list(MUDDA_NUMBERS)
    start = order.index(int(seed["lord"]))
    rotated = order[start:] + order[:start]

    balance = float(seed["natal"]["yet_to_traverse"])
    rows = []
    running = 0.0
    for position, graha in enumerate(rotated):
        full = mudda_days(graha)
        span = full * balance if position == 0 else float(full)
        row = {
            "graha": graha, "full_days": full, "days": span,
            "is_balance": position == 0,
            "from_day": running, "to_day": running + span,
        }
        if start_jd is not None:
            row["from_jd"] = float(start_jd) + running
            row["to_jd"] = float(start_jd) + running + span
        rows.append(row)
        running += span

    return {
        "seed": seed,
        "order": tuple(rotated),
        "rows": tuple(rows),
        "balance_fraction": balance,
        "total_days": running,
        "full_cycle_days": MUDDA_YEAR_DAYS,
        "rule": MUDDA_LENGTH_RULE,
    }


# --------------------------------------------------------------------------
# What §30.3 leaves, and what it gets exactly right
# --------------------------------------------------------------------------

#: **Finding.** Table 76 is three times the Vimsottari years for all nine
#: planets and sums to **360 exactly**, which is what "120 years compressed to
#: 360 days" requires: 120 x 3 = 360. The table's column order is the
#: Vimsottari cycle rotated to begin at the Sun, and §30.3's 1-to-9 numbering
#: is the same rotation.
TABLE_76_IS_THREE_TIMES_VIMSOTTARI = (
    "Every entry in Table 76 is three times the planet's Vimsottari years and "
    "the nine sum to 360. The column order is the Vimsottari cycle started "
    "from the Sun, which is also the section's numbering."
)

#: **Finding.** §30.3 offers the arithmetic as a substitute for progressing
#: the constellation, and the two are **identical**, not close. Progressing
#: adds the completed years to the nakshatra index modulo 27; the lord is that
#: index modulo 9; and 27 is a multiple of 9, so the two reductions commute.
#: The numbering rotation cancels the same way. `first_dasa_lord` computes both
#: and reports whether they agree, which they do in every chart.
THE_SHORTCUT_IS_EXACT_NOT_APPROXIMATE = (
    "Progressing the constellation adds the years modulo 27 and takes the "
    "lord modulo 9, and 27 is a multiple of 9, so the section's arithmetic is "
    "the same operation and not an approximation."
)

#: **Finding, and the section's own date settles it.** §30.3 defines a solar
#: day precisely — "the time period in which Sun moves by exactly 1 degree" —
#: and then works its date in **calendar** days. Rahu's balance of 42.66 days
#: from 1 June 1993 lands on **14 July** as calendar days, which is what the
#: section prints, and on **16 July** if the days are the solar days it just
#: defined. Under the definition 360 solar days is exactly one sidereal year;
#: under the worked usage the nine dasas run **5.26 days short**, ending 27 May
#: 1994 where the next annual chart begins on 1 June. See OI-175.
THE_DATES_USE_CALENDAR_DAYS_NOT_THE_SOLAR_DAYS_DEFINED = (
    "Section 30.3 defines a solar day as one degree of solar motion and then "
    "counts Rahu's 42.66-day balance in calendar days to reach 14 July. In "
    "solar days it would be 16 July, and the nine dasas would fill the year "
    "instead of ending 5.26 days early."
)

#: **Finding.** Patyayini's year and mudda's disagree, and neither is the year
#: the annual chart actually covers. §30.2 divides 365.2425 calendar days —
#: the Gregorian year, twenty minutes short. §30.3 uses 360 days that are
#: calendar days in its own worked date — 5.26 days short. The real interval
#: between two varsha praveshes is 365.2564 days.
THE_TWO_DASAS_USE_TWO_DIFFERENT_YEARS = (
    "Patyayini fills 365.2425 days and mudda 360, and the year between two "
    "varsha praveshes is 365.2564. The three figures are all different."
)

#: **Finding.** The mudda seed is the **natal** Moon and the balance is the
#: **natal** Moon's unspent constellation, so the whole dasa is fixed by the
#: nativity: the same fraction seeds every year of the native's life, and only
#: the starting lord rotates. The annual chart contributes nothing but the
#: date the sequence starts from. §30.1 said as much — the annual chart is not
#: the seed — and this is the section where it bites hardest.
THE_ANNUAL_CHART_CONTRIBUTES_ONLY_THE_START_DATE = (
    "Both the seed and the balance come from the natal Moon, so the same "
    "balance fraction opens every year of the native's life and only the "
    "first lord moves on. The annual chart supplies the start date alone."
)


#: **Book defect, and not the usual one.** §30.3 says "natal Moon is at 29 Sg
#: 28". Chart 18 prints **29 Sg 27**, and our own value is 29 Sg 27.49, which
#: truncates *and* rounds to 27. So this arcminute is **not** D-80's
#: truncate-against-round convention — under that convention both printings
#: should read 27. One of the two figures is simply a minute out.
#:
#: Nothing turns on it: the fraction of the constellation left to traverse is
#: 0.7906 from our value and 0.7900 from the book's, and §30.3 rounds to "about
#: 0.79" either way. Recorded rather than corrected.
THE_NATAL_MOON_IS_CITED_AN_ARCMINUTE_HIGH = (
    "Section 30.3 gives the natal Moon as 29 Sg 28 where Chart 18 prints 29 "
    "Sg 27. Our value is 29 Sg 27.49, which both truncates and rounds to 27, "
    "so this is not the convention D-80 records. The balance is 0.79 either "
    "way."
)
