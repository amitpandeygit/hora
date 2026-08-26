"""Lunar months — book §1.3.8.2.

    "We said that a new lunar month starts whenever Sun and Moon are at the
    same longitude."

The month is named for **where** the conjunction happened, not when:

    "The name of a lunar month is decided by the rasi in which Sun-Moon
    conjunction takes place. If Sun-Moon conjoin in Pisces, for example, it
    starts Chaitra maasa."

So the whole calculation is one lookup once the conjunction longitude is
known — Table 4, indexed by rasi, starting at Pisces. This module deliberately
takes the conjunction longitude rather than a date: finding the conjunction is
an ephemeris problem, already solved in :mod:`hora.panchanga.calendar`, and
mixing the two would make the naming rule untestable without Swiss Ephemeris.

The names come from a *likelihood*, not a rule:

    "These names come from the constellation that Moon is most likely to
    occupy on the full Moon day."

which is why Table 4's third column is transcribed rather than derived. Two
rows spell the month and the constellation differently (Kaarteeka/Krittika,
Maagha/Makha) and one does not match at all — Aaswayuja's constellation is
Aswini. See :data:`~hora.core.const.MASA_FULL_MOON_NAKSHATRA_BOOK`.

**Adhika maasa.** §1.3.8.2 gives the observation, not the algorithm:

    "A solar year has about 365.2425 days, but a lunar year only has about
    355 days. Once in every 3 years, this difference accumulates to one month
    and an extra lunar month comes. This results in Sun-Moon conjunction
    coming twice in the same rasi."

Two conjunctions in one rasi means that rasi's month occurs twice, "One is
called 'Nija' Jyeshtha maasa and the other is called 'Adhika' Jyeshtha
maasa." The book does **not** say which of the two is which, so
:func:`month_pair` labels a pair only when the caller states the order, and
never guesses. The running calendar's adhika flag comes from the no-sankranti
rule in :mod:`hora.panchanga.calendar`; see OI-3.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    ADHIKA_MAASA_INTERVAL_YEARS,
    MAASA_MEANING,
    MAASA_QUALIFIERS,
    MASA_APPROXIMATE_GREGORIAN_BOOK,
    MASA_FROM_CONJUNCTION_RASI,
    MASA_FULL_MOON_NAKSHATRA_BOOK,
    MASA_NAMES,
    MASA_NAMES_BOOK,
    RASI_NAMES,
)


class MaasaError(validate.InputError):
    """A lunar month input that cannot be resolved."""


#: "If Sun-Moon conjoin in Pisces, for example, it starts Chaitra maasa."
#: Table 4 therefore begins at Pisces, rasi index 11, not at Aries.
FIRST_MONTH_RASI = 11

#: "Nija means real and adhika means extra."
NIJA = "Nija"
ADHIKA = "Adhika"


@dataclass(frozen=True)
class Step:
    """One numbered step, with what it produced and why."""

    number: int
    description: str
    detail: str
    value: str


@dataclass(frozen=True)
class Maasa:
    """A lunar month, with every intermediate the lookup went through."""

    conjunction_longitude: float
    conjunction_rasi: int
    conjunction_rasi_name: str
    index: int
    name: str
    name_book: str
    full_moon_nakshatra: str
    approximate_gregorian: str
    qualifier: str | None
    full_name: str
    steps: tuple[Step, ...]


def conjunction_rasi(longitude: float) -> int:
    """Step 1 — the rasi the Sun-Moon conjunction falls in.

    Footnote 2 defines conjunction as *exactly* the same longitude, so there
    is a single longitude to place; the caller supplies it.
    """
    return int(validate.longitude("conjunction_longitude", longitude) // 30.0)


def month_index(rasi: int) -> int:
    """Step 2 — Table 4's row for that rasi, 0 (Chaitra) to 11 (Phaalguna).

    Pisces gives 0. The offset is a table, not arithmetic on the rasi, so
    that the Pisces-first ordering stays visible.
    """
    validate.in_range("rasi", rasi, 0, 11)
    return int(MASA_FROM_CONJUNCTION_RASI[rasi])


def qualified_name(name: str, qualifier: str | None) -> str:
    """Step 3 — prefix Nija or Adhika, when the caller knows which it is.

    "One is called 'Nija' Jyeshtha maasa and the other is called 'Adhika'
    Jyeshtha maasa." An unqualified month is the ordinary case and is
    returned bare.
    """
    if qualifier is None:
        return name
    if qualifier not in MAASA_QUALIFIERS:
        raise MaasaError(
            f"qualifier must be one of {sorted(MAASA_QUALIFIERS)} or None, "
            f"got {qualifier!r}"
        )
    return f"{qualifier} {name}"


def maasa(conjunction_longitude: float, qualifier: str | None = None) -> Maasa:
    """Name the lunar month started by a conjunction at this longitude.

    :param conjunction_longitude: sidereal longitude of the Sun-Moon
        conjunction that starts the month. Reduced into 0-360 before use, as
        everywhere else in the codebase; the reduced value is echoed back.
    :param qualifier: ``"Nija"`` or ``"Adhika"`` when the caller has already
        established that this rasi carries two conjunctions. Never inferred
        here — §1.3.8.2 does not say which of the pair is which.
    :raises MaasaError: if the qualifier is not one the book uses.
    :raises hora.core.validate.InputError: if the longitude is out of range.
    """
    # Wrap once, here, and use the wrapped value everywhere below. Echoing
    # the raw input while computing from the reduced one made step 1 read
    # "400.0000 deg falls in Taurus".
    reduced = validate.longitude("conjunction_longitude", conjunction_longitude)
    rasi = conjunction_rasi(reduced)
    index = month_index(rasi)
    name = str(MASA_NAMES_BOOK[index])
    full = qualified_name(name, qualifier)
    steps = (
        Step(
            1,
            "Find the rasi of the Sun-Moon conjunction that starts the month",
            f"{reduced:.4f} deg falls in {RASI_NAMES[rasi]}",
            RASI_NAMES[rasi],
        ),
        Step(
            2,
            "Look up Table 4: the rasi decides the name",
            f"{RASI_NAMES[rasi]} starts {name} maasa "
            f"({MAASA_MEANING}), month {index + 1} of 12",
            name,
        ),
        Step(
            3,
            "Qualify the name if this rasi carries two conjunctions",
            f"{qualifier} means {MAASA_QUALIFIERS[qualifier]}"
            if qualifier
            else "no second conjunction stated, so the name stands unqualified",
            full,
        ),
    )
    return Maasa(
        conjunction_longitude=reduced,
        conjunction_rasi=rasi,
        conjunction_rasi_name=str(RASI_NAMES[rasi]),
        index=index + 1,
        name=str(MASA_NAMES[index]),
        name_book=name,
        full_moon_nakshatra=str(MASA_FULL_MOON_NAKSHATRA_BOOK[index]),
        approximate_gregorian=str(MASA_APPROXIMATE_GREGORIAN_BOOK[index]),
        qualifier=qualifier,
        full_name=full,
        steps=steps,
    )


def month_pair(first: float, second: float) -> tuple[Maasa, Maasa]:
    """Two conjunctions in one rasi — the adhika maasa case of §1.3.8.2.

    "Sun-Moon conjunction took place at 0°23' in Taurus on May 15, 1999 ...
    and again at 28°29' in Taurus on June 14, 1999 ... So 1999 had 2 Jyeshtha
    maasas."

    Both are returned **unqualified**. The book names the pair Nija and Adhika
    but never says which is which, and this module does not decide it. A
    caller that knows the reckoning passes the qualifier to :func:`maasa`.

    :raises MaasaError: if the two conjunctions are not in the same rasi, in
        which case they start two different months and are not a pair at all.
    """
    a, b = maasa(first), maasa(second)
    if a.conjunction_rasi != b.conjunction_rasi:
        raise MaasaError(
            "a Nija/Adhika pair needs both conjunctions in one rasi, but "
            f"{a.conjunction_longitude:.4f} is in {a.conjunction_rasi_name} "
            f"and {b.conjunction_longitude:.4f} is in {b.conjunction_rasi_name}"
        )
    return a, b


def is_adhika_year_interval(years: int) -> bool:
    """"An adhika maasa (extra month) comes once in every 3 years."""
    return years >= ADHIKA_MAASA_INTERVAL_YEARS
