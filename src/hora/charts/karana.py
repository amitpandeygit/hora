"""Karanas — book §1.3.10.

    "Each tithi is divided into 2 karanas. There are 11 karanas: (1) Bava,
    (2) Balava, (3) Kaulava, (4) Taitula, (5) Garija, (6) Vanija, (7) Vishti,
    (8) Sakuna, (9) Chatushpada, (10) Naga, and, (11) Kimstughna."

Sixty half-tithis, eleven names. The distribution is stated, not derived:

    "The first 7 karanas repeat 8 times starting from the 2nd half of the
    first lunar day of a month. The last 4 karanas come just once in a month,
    starting from the 2nd half of the 29th lunar day and ending at the 1st
    half of the first lunar day."

Which accounts for all sixty: 7 x 8 = 56 repeating, plus 4 that come once.
The four that come once **wrap around the month boundary** — Sakuna,
Chatushpada and Naga close it and Kimstughna opens it — so the very first
half-tithi of a month carries the *last* of the eleven names, not the first.
Getting that backwards puts every repeating karana off by one.

    slot 1   = 1st half of tithi 1   -> Kimstughna   (11th name)
    slot 2   = 2nd half of tithi 1   -> Bava         (repeating begins)
    slot 57  = 1st half of tithi 29  -> Vishti       (repeating ends)
    slot 58  = 2nd half of tithi 29  -> Sakuna
    slot 60  = 2nd half of tithi 30  -> Naga
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import KARANA_NAMES, KARANA_NAMES_BOOK

#: "Each tithi is divided into 2 karanas."
KARANAS_PER_TITHI = 2

#: 30 tithis x 2 = 60 half-tithis in a lunar month.
KARANA_SLOTS = 60

#: "Each tithi ... 12 degrees", so half of one is 6.
KARANA_SPAN = 6.0

#: "There are 11 karanas".
KARANA_COUNT = 11

#: "The first 7 karanas repeat 8 times."
REPEATING_COUNT = 7
REPETITIONS = 8

#: "The last 4 karanas come just once in a month."
ONCE_ONLY_COUNT = 4

#: Slot (1-based) of the first repeating karana: "the 2nd half of the first
#: lunar day of a month".
FIRST_REPEATING_SLOT = 2

#: Slot of the first of the four that come once: "the 2nd half of the 29th
#: lunar day".
FIRST_ONCE_ONLY_SLOT = 58


class KaranaError(validate.InputError):
    """A karana input that cannot be resolved."""


@dataclass(frozen=True)
class Karana:
    """One karana, with the half-tithi it occupies."""

    slot: int
    tithi: int
    half: int
    index: int
    name: str
    name_book: str
    repeats: bool
    occurrences: int


def slot_of(tithi: int, half: int) -> int:
    """The 1-based half-tithi slot for a tithi and which half of it.

    :param tithi: 1 to 30.
    :param half: 1 for the first half, 2 for the second.
    """
    validate.in_range("tithi", tithi, 1, 30)
    validate.in_range("half", half, 1, KARANAS_PER_TITHI)
    return (tithi - 1) * KARANAS_PER_TITHI + half


def slot_from_elongation(elongation: float) -> int:
    """The slot from Moon minus Sun, the same quantity a tithi divides by 12."""
    reduced = validate.longitude("elongation", elongation)
    # Multiply before dividing, for the reason given in charts/yoga.py: this
    # divisor is exact, but the same shape is used everywhere for consistency.
    return int(reduced * KARANA_SLOTS / 360.0) + 1


def index_of_slot(slot: int) -> int:
    """The 1-based karana name (1 to 11) occupying a slot.

    §1.3.10 in three clauses, in the order it states them.
    """
    validate.in_range("slot", slot, 1, KARANA_SLOTS)
    if slot == 1:
        # "...ending at the 1st half of the first lunar day."
        return KARANA_COUNT
    if slot >= FIRST_ONCE_ONLY_SLOT:
        # "...starting from the 2nd half of the 29th lunar day."
        return REPEATING_COUNT + 1 + (slot - FIRST_ONCE_ONLY_SLOT)
    # "The first 7 karanas repeat 8 times starting from the 2nd half of the
    # first lunar day."
    return (slot - FIRST_REPEATING_SLOT) % REPEATING_COUNT + 1


def karana(slot: int) -> Karana:
    """The karana occupying a half-tithi slot, 1 to 60."""
    validate.in_range("slot", slot, 1, KARANA_SLOTS)
    index = index_of_slot(slot)
    repeats = index <= REPEATING_COUNT
    return Karana(
        slot=slot,
        tithi=(slot - 1) // KARANAS_PER_TITHI + 1,
        half=(slot - 1) % KARANAS_PER_TITHI + 1,
        index=index,
        name=str(KARANA_NAMES[index - 1]),
        name_book=str(KARANA_NAMES_BOOK[index - 1]),
        repeats=repeats,
        occurrences=REPETITIONS if repeats else 1,
    )


def karana_at(sun_longitude: float, moon_longitude: float) -> Karana:
    """The karana running for a Sun and Moon longitude."""
    return karana(slot_from_elongation(moon_longitude - sun_longitude))


def slots_of_index(index: int) -> tuple[int, ...]:
    """Every slot in a month at which a given karana name falls."""
    validate.in_range("index", index, 1, KARANA_COUNT)
    return tuple(s for s in range(1, KARANA_SLOTS + 1) if index_of_slot(s) == index)
