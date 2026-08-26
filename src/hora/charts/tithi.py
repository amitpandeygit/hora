"""Tithis — book §1.3.8.1.

    "Tithi or lunar day is a period in which the difference between the
    longitudes of Moon and Sun changes by exactly 12°."

§1.3.8.1 states the computation as four numbered steps, so they are kept as
four, with every intermediate returned. A caller checking a date against
JHora needs to see which step diverged, not only that the tithi did.

    1  elongation = Moon - Sun, plus 360 if negative
    2  divide by 12, take the quotient
    3  add 1, giving 1 to 30
    4  look up Table 3, qualified by the paksha

The naming convention matters and is easy to get half right. "We write the
classification of fortnight (Sukla or Krishna) first and then write tithi
name" — so the 22nd tithi is "Krishna Saptami", not "Saptami" or "22nd
Saptami".

**But only fourteen of the fifteen names repeat.** Table 3's last two rows are
unique: the 15th is Paurnami, the full moon, with a dash in the Krishna
column, and the 30th is Amavasya, the new moon, with a dash in the Sukla
column. Naming the 30th by its position within the paksha gives "Krishna
Paurnami", which is not a tithi. See :data:`UNIQUE_TITHIS`.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    PAKSHA_NAMES,
    TITHI_ALTERNATE_NAMES,
    TITHI_LORD,
    TITHI_NAMES_BOOK,
)


class TithiError(validate.InputError):
    """A tithi input that cannot be resolved.

    A subclass of :class:`~hora.core.validate.InputError`, which the shared
    range checks raise directly. Catch ``InputError`` to catch both.
    """


#: §1.3.8.1: "a period in which the difference between the longitudes of Moon
#: and Sun changes by exactly 12°".
TITHI_SPAN = 12.0

#: "A lunar month consists of 30 tithis."
TITHIS_PER_MONTH = 30

#: "There are 15 tithis and the same tithis repeat in the brigher and darker
#: fortnights."
TITHIS_PER_PAKSHA = 15

#: Table 3's two rows that do not repeat: the full moon closes the brighter
#: fortnight and the new moon closes the darker one, and neither has a
#: counterpart in the other. Indexed by tithi number, 1 to 30.
UNIQUE_TITHIS = {15: "the full moon", 30: "the new moon"}

#: The elongation each paksha spans. "During Sukla/Suddha paksha ... Moon is
#: ahead of Sun by an amount that is between 0° and 180°. During
#: Krishna/Bahula paksha ... between 180° and 360°."
PAKSHA_ELONGATION = ((0.0, 180.0), (180.0, 360.0))


@dataclass(frozen=True)
class TithiStep:
    """One of §1.3.8.1's four numbered steps."""

    number: int
    name: str
    description: str
    value: float | int | None = None
    detail: str | None = None


@dataclass(frozen=True)
class Tithi:
    """A tithi with the derivation that produced it."""

    #: 1 to 30, counted from the new moon.
    index: int
    #: 1 to 15, the number within its own paksha.
    number_in_paksha: int
    name: str
    #: The name qualified by the fortnight, as §1.3.8.1 says to write it.
    full_name: str
    alternate_names: tuple[str, ...]
    paksha: int
    paksha_name: str
    lord: int
    lord_name: str
    #: Moon minus Sun, before normalising. Negative when the Sun is ahead.
    raw_difference: float
    #: The same after adding 360 where needed: how advanced the Moon is.
    elongation: float
    #: Whole tithis completed — step 2's quotient.
    completed: int
    #: How far into the current tithi, in degrees, and as a fraction.
    elapsed_in_tithi: float
    fraction_elapsed: float
    #: The elongation at which this tithi starts and ends.
    starts_at: float
    ends_at: float
    steps: tuple[TithiStep, ...]


def elongation(sun_longitude: float, moon_longitude: float) -> float:
    """Step 1 — how advanced the Moon is on the Sun, 0 to 360.

    "Find the difference: (Moon's longitude - Sun's longitude). Add 360° if
    the result is negative."
    """
    sun = validate.longitude("sun_longitude", sun_longitude)
    moon = validate.longitude("moon_longitude", moon_longitude)
    return (moon - sun) % 360.0


def tithi(sun_longitude: float, moon_longitude: float) -> Tithi:
    """Run §1.3.8.1's four steps for a pair of longitudes.

    :param sun_longitude: sidereal longitude in degrees; wrapped into 0-360.
    :param moon_longitude: likewise.
    :raises InputError: if either longitude is not finite.
    """
    sun = validate.longitude("sun_longitude", sun_longitude)
    moon = validate.longitude("moon_longitude", moon_longitude)

    steps: list[TithiStep] = []

    # Step 1
    raw = moon - sun
    advanced = raw % 360.0
    steps.append(TithiStep(
        1, "elongation",
        "Find the difference (Moon's longitude - Sun's longitude). Add 360 "
        "if the result is negative.",
        value=advanced,
        detail=(
            f"{moon:.4f} - {sun:.4f} = {raw:.4f}"
            + (f", + 360 = {advanced:.4f}" if raw < 0 else "")
        ),
    ))

    # Step 2
    completed = int(advanced // TITHI_SPAN)
    steps.append(TithiStep(
        2, "completed",
        "Divide this result by 12. Ignore the remainder and take the quotient.",
        value=completed,
        detail=f"{advanced:.4f} / 12 = {advanced / TITHI_SPAN:.4f}, quotient {completed}",
    ))

    # Step 3
    index = completed + 1
    steps.append(TithiStep(
        3, "index",
        "Add 1 to the quotient. You get a number from 1 to 30.",
        value=index, detail=f"{completed} + 1 = {index}",
    ))

    # Step 4
    paksha = 0 if advanced < 180.0 else 1
    number_in_paksha = ((index - 1) % TITHIS_PER_PAKSHA) + 1
    # Indexed by the tithi number, not by its position in the paksha: the
    # 30th is Amavasya, not the 15th name over again.
    name = TITHI_NAMES_BOOK[index - 1]
    # The full moon and the new moon occur once each, so the book writes them
    # unqualified — "Paurnami (Full Moon)", not "Sukla Paurnami".
    full_name = name if index in UNIQUE_TITHIS else f"{PAKSHA_NAMES[paksha]} {name}"
    steps.append(TithiStep(
        4, "name",
        "Refer to Table 3 and find the name of the tithi. Write the "
        "classification of fortnight first, then the tithi name.",
        value=index,
        detail=(
            f"the {index}th of 30 is {name}, {UNIQUE_TITHIS[index]}, which "
            f"occurs once and is written unqualified"
            if index in UNIQUE_TITHIS else
            f"the {index}th of 30 is the {number_in_paksha}th of "
            f"{PAKSHA_NAMES[paksha]} paksha, which is {name}, so {full_name}"
        ),
    ))

    starts_at = completed * TITHI_SPAN
    elapsed = advanced - starts_at
    # By tithi number, like the name above. TITHI_LORD is 30 long and its
    # last entry is Rahu for Amavasya, not Saturn repeated from Paurnami.
    lord = int(TITHI_LORD[index - 1])
    return Tithi(
        index=index,
        number_in_paksha=number_in_paksha,
        name=name,
        full_name=full_name,
        alternate_names=tuple(TITHI_ALTERNATE_NAMES[number_in_paksha]),
        paksha=paksha,
        paksha_name=PAKSHA_NAMES[paksha],
        lord=lord,
        lord_name=GRAHA_NAMES[lord],
        raw_difference=raw,
        elongation=advanced,
        completed=completed,
        elapsed_in_tithi=elapsed,
        fraction_elapsed=elapsed / TITHI_SPAN,
        starts_at=starts_at,
        ends_at=starts_at + TITHI_SPAN,
        steps=tuple(steps),
    )
