"""Horas — the planetary hour, book §1.3.11.

    "Each day starts at sunrise and ends at next day's sunrise. This period is
    divided into 24 equal parts and they are called horas. A hora is almost
    equal to an hour."

    "The lords of hora come in the order of decreasing speed with respect to
    earth: Saturn, Jupiter, Mars, Sun, Venus, Mercury and Moon. After Moon, we
    go back to Saturn and repeat the 7 planets."

    "The first hora of any day ... is ruled by the lord of the weekday ...
    After that, we list planets in the order mentioned above."

So the cycle is entered at the weekday lord's position, not at Saturn.

**The section contradicts its own example, and the difference is real.** The
first paragraph divides the *actual* sunrise-to-sunrise interval into 24, so a
hora is "almost equal to an hour" and not exactly one. The worked example then
calls a hora "a period of one hour following sunrise" and reads the 16th hora
straight off a 15:30 clock elapsed. Both readings are supported here:
``day_length_hours`` defaults to 24, which reproduces the example exactly, and
a caller with a real sunrise pair passes the true length. See OI-40.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import GRAHA_NAMES, HORA_LORD_ORDER, VAARA_LORD, VAARA_NAMES


class HoraError(validate.InputError):
    """A hora input that cannot be resolved."""


#: "This period is divided into 24 equal parts and they are called horas."
HORAS_PER_DAY = 24

#: "After Moon, we go back to Saturn and repeat the 7 planets."
HORA_LORD_CYCLE = 7

#: A civil day, used when the caller does not give a real sunrise interval.
#: The book's example assumes exactly this: "a period of one hour".
NOMINAL_DAY_HOURS = 24.0


def _ordinal(n: int) -> str:
    """1st, 2nd, 3rd, 4th ... for the step wording."""
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }".replace(" ", "")


@dataclass(frozen=True)
class Step:
    """One step of §1.3.11's worked procedure."""

    number: int
    description: str
    detail: str
    value: float | int | str


@dataclass(frozen=True)
class HoraResult:
    """The hora running at some elapsed time after sunrise."""

    weekday: int
    weekday_name: str
    weekday_lord: int
    weekday_lord_name: str
    elapsed_hours: float
    day_length_hours: float
    hora_length_hours: float
    index: int
    position_in_cycle: int
    lord: int
    lord_name: str
    steps: tuple[Step, ...]


def hora_length(day_length_hours: float = NOMINAL_DAY_HOURS) -> float:
    """"This period is divided into 24 equal parts"."""
    return validate.positive("day_length_hours", day_length_hours) / HORAS_PER_DAY


def hora_index(
    elapsed_hours: float, day_length_hours: float = NOMINAL_DAY_HOURS
) -> int:
    """Which hora since sunrise, 1 to 24.

    "The time elapsed since sunrise is 21:40 - 6:10 = 15:30. So the 16th hour
    since sunrise was running then."
    """
    validate.non_negative("elapsed_hours", elapsed_hours)
    length = hora_length(day_length_hours)
    if elapsed_hours >= day_length_hours:
        raise HoraError(
            f"elapsed_hours must be less than the day length "
            f"{day_length_hours}, got {elapsed_hours}"
        )
    return int(elapsed_hours / length) + 1


def position_in_cycle(index: int) -> int:
    """"After subtracting multiples of 7 from 16, we get 2."

    The book subtracts rather than taking a remainder, which matters at
    multiples of seven: the 7th hora is the 7th planet from the weekday lord,
    not the 0th. So this returns 1 to 7, never 0.
    """
    validate.in_range("index", index, 1, HORAS_PER_DAY)
    return (index - 1) % HORA_LORD_CYCLE + 1


def lord_of(weekday: int, index: int) -> int:
    """The graha ruling the ``index``-th hora of a weekday.

    :param weekday: 0 for Sunday through 6 for Saturday.
    :param index: 1 to 24, counted from sunrise.
    """
    validate.in_range("weekday", weekday, 0, 6)
    validate.in_range("index", index, 1, HORAS_PER_DAY)
    start = HORA_LORD_ORDER.index(VAARA_LORD[weekday])
    return int(HORA_LORD_ORDER[(start + index - 1) % HORA_LORD_CYCLE])


def hora(
    weekday: int,
    elapsed_hours: float,
    day_length_hours: float = NOMINAL_DAY_HOURS,
) -> HoraResult:
    """The hora running ``elapsed_hours`` after sunrise on a weekday.

    :param weekday: 0 for Sunday through 6 for Saturday.
    :param elapsed_hours: time since sunrise, in hours.
    :param day_length_hours: sunrise to next sunrise. Defaults to 24, which
        is what §1.3.11's worked example assumes; pass the real interval for
        the "24 equal parts" reading of the same section.
    :raises HoraError: if the elapsed time is not inside the day.
    """
    validate.in_range("weekday", weekday, 0, 6)
    index = hora_index(elapsed_hours, day_length_hours)
    place = position_in_cycle(index)
    lord = lord_of(weekday, index)
    day_lord = int(VAARA_LORD[weekday])
    steps = (
        Step(
            1,
            "Find the time elapsed since sunrise",
            f"{elapsed_hours:.4f} hours after sunrise",
            elapsed_hours,
        ),
        Step(
            2,
            "Divide the sunrise-to-sunrise period into 24 equal parts and see "
            "which one is running",
            f"{elapsed_hours:.4f} / {hora_length(day_length_hours):.4f} gives "
            f"the {_ordinal(index)} hora since sunrise",
            index,
        ),
        Step(
            3,
            "The first hora belongs to the lord of the weekday, so this is the "
            "index-th planet from that lord",
            f"{VAARA_NAMES[weekday]} belongs to "
            f"{GRAHA_NAMES[day_lord]}, so this is the {_ordinal(index)} planet from "
            f"{GRAHA_NAMES[day_lord]}",
            index,
        ),
        Step(
            4,
            "Subtract multiples of 7, since the 7 planets repeat",
            f"{index} reduces to {place}",
            place,
        ),
        Step(
            5,
            "Read that position in the order of decreasing speed",
            f"the {_ordinal(place)} planet from {GRAHA_NAMES[day_lord]} is "
            f"{GRAHA_NAMES[lord]}",
            str(GRAHA_NAMES[lord]),
        ),
    )
    return HoraResult(
        weekday=weekday,
        weekday_name=str(VAARA_NAMES[weekday]),
        weekday_lord=day_lord,
        weekday_lord_name=str(GRAHA_NAMES[day_lord]),
        elapsed_hours=float(elapsed_hours),
        day_length_hours=float(day_length_hours),
        hora_length_hours=hora_length(day_length_hours),
        index=index,
        position_in_cycle=place,
        lord=lord,
        lord_name=str(GRAHA_NAMES[lord]),
        steps=steps,
    )


def horas_of_weekday(weekday: int) -> tuple[int, ...]:
    """All 24 hora lords of a weekday, in order from sunrise."""
    return tuple(lord_of(weekday, i) for i in range(1, HORAS_PER_DAY + 1))
