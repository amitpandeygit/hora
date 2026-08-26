"""Sun-Moon yogas — book §1.3.9.

    "Add the longitudes of Sun and Moon. Remove 360° from the sum if it is
    greater than 360°. Divide the sum by the length of one nakshatra (13°20'
    or 800'). Ignore fractions and take the integer part. Add 1 to it and the
    result is the index of the yoga running. Refer to Table 5 and find the
    yoga corresponding to the index."

Five steps, kept as five, each returning its intermediate. This is the *sum*
of the longitudes, where a tithi takes the difference — the one thing worth
getting right, since both divide a 0-360 quantity and both look alike.

**Boundary arithmetic.** The book divides by 800 arcminutes, not by 13°20',
and that choice matters. One nakshatra span is 360/27 = 13.333... degrees,
which no binary float represents exactly, so ``x // (360/27)`` returns the
*previous* yoga at nine of the twenty-seven exact boundaries — 40° gives yoga
3, not 4. :func:`completed_spans` multiplies before dividing, which is exact
for every boundary, and the module is tested at all 27. See OI-39: the same
pattern is still live in `panchanga/core.py`, `charts/chart.py` and
`dasha/base.py`.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    NAKSHATRA_SPAN,
    YOGA_MEANINGS,
    YOGA_NAMES,
    YOGA_NAMES_BOOK,
)


class YogaError(validate.InputError):
    """A yoga input that cannot be resolved."""


#: "Divide the sum by the length of one nakshatra (13°20' or 800')."
YOGA_SPAN = NAKSHATRA_SPAN

#: The same span written the book's way, in arcminutes. The example works in
#: these: "131 x 60 + 10 = 7870'. By dividing this with 800', we get 9.8375."
YOGA_SPAN_MINUTES = 800

#: Table 5 has 27 rows, one per nakshatra span of the 360-degree circle.
YOGAS_PER_CIRCLE = 27

MINUTES_PER_DEGREE = 60


@dataclass(frozen=True)
class Step:
    """One numbered step, with what it produced and why."""

    number: int
    description: str
    detail: str
    value: float | int | str


@dataclass(frozen=True)
class Yoga:
    """A Sun-Moon yoga, with every intermediate the procedure went through."""

    sun_longitude: float
    moon_longitude: float
    raw_sum: float
    total: float
    total_minutes: float
    quotient: float
    completed: int
    index: int
    name: str
    name_book: str
    meaning: str
    steps: tuple[Step, ...]


def raw_sum(sun_longitude: float, moon_longitude: float) -> float:
    """Step 1a — "Add the longitudes of Sun and Moon", before any reduction."""
    return validate.finite("sun_longitude", sun_longitude) + validate.finite(
        "moon_longitude", moon_longitude
    )


def reduced_sum(sun_longitude: float, moon_longitude: float) -> float:
    """Step 1b — "Remove 360° from the sum if it is greater than 360°"."""
    return raw_sum(sun_longitude, moon_longitude) % 360.0


def to_minutes(degrees: float) -> float:
    """The book's own conversion: "131 x 60 + 10 = 7870'"."""
    return degrees * MINUTES_PER_DEGREE


def completed_spans(total: float) -> int:
    """Step 2 — "Divide the sum ... Ignore fractions and take the integer part".

    Multiplies before dividing. ``total // (360/27)`` is not exact: at
    total = 40 degrees, the true quotient is 3 but the float result is
    2.9999999999999996, so the caller lands one yoga early. Multiplying first
    keeps every boundary on an integer. Verified at all 27.
    """
    return int(total * YOGAS_PER_CIRCLE / 360.0)


def yoga(sun_longitude: float, moon_longitude: float) -> Yoga:
    """The yoga running for a Sun and Moon longitude.

    :param sun_longitude: sidereal longitude in degrees.
    :param moon_longitude: sidereal longitude in degrees.
    :raises hora.core.validate.InputError: if either value is not finite.
    """
    added = raw_sum(sun_longitude, moon_longitude)
    total = added % 360.0
    minutes = to_minutes(total)
    completed = completed_spans(total)
    index = completed + 1
    name_book = str(YOGA_NAMES_BOOK[completed])
    removed = added > 360.0
    steps = (
        Step(
            1,
            "Add the longitudes of Sun and Moon, removing 360 if the sum "
            "exceeds it",
            f"{sun_longitude:.4f} + {moon_longitude:.4f} = {added:.4f}"
            + (f", - 360 = {total:.4f}" if removed else ", which is not over 360"),
            total,
        ),
        Step(
            2,
            "Divide the sum by the length of one nakshatra (13 deg 20', or 800')",
            f"{minutes:.2f}' / {YOGA_SPAN_MINUTES}' = "
            f"{minutes / YOGA_SPAN_MINUTES:.4f}",
            minutes / YOGA_SPAN_MINUTES,
        ),
        Step(
            3,
            "Ignore fractions and take the integer part",
            f"{minutes / YOGA_SPAN_MINUTES:.4f} gives {completed}",
            completed,
        ),
        Step(
            4,
            "Add 1 to it, and the result is the index of the yoga running",
            f"{completed} + 1 = {index}",
            index,
        ),
        Step(
            5,
            "Refer to Table 5 and find the yoga corresponding to the index",
            f"the {index}th yoga is {name_book!r} ({YOGA_MEANINGS[completed]})",
            name_book,
        ),
    )
    return Yoga(
        sun_longitude=float(sun_longitude),
        moon_longitude=float(moon_longitude),
        raw_sum=added,
        total=total,
        total_minutes=minutes,
        quotient=minutes / YOGA_SPAN_MINUTES,
        completed=completed,
        index=index,
        name=str(YOGA_NAMES[completed]),
        name_book=name_book,
        meaning=str(YOGA_MEANINGS[completed]),
        steps=steps,
    )


def yoga_of_index(index: int) -> tuple[str, str]:
    """Table 5's row for an index, 1 to 27: the book's name and its meaning."""
    validate.in_range("index", index, 1, YOGAS_PER_CIRCLE)
    return str(YOGA_NAMES_BOOK[index - 1]), str(YOGA_MEANINGS[index - 1])
