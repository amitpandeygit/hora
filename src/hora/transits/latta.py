"""§26.7 — latta, the nakshatra a transiting graha kicks.

Each graha kicks one constellation, counted from where it stands in transit.
The kick matters when it lands on the nakshatra the **natal** Moon or lagna
occupies, and what it spoils is that graha's significations **in the natal
chart** — not its natural ones.

Two things separate this from the chapter's other nakshatra techniques, and
both are recorded below. Its origin is the **transit** position where §26.4
and §26.6 count from the natal Moon's; and it admits the **lagna's** nakshatra
as an alternative target, which nothing before it in the chapter has done.

The per-graha offsets have not been supplied. `LATTA_OFFSETS` is empty and
`latta` refuses until it is filled, so nothing here guesses a kick.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import NAKSHATRA_NAMES


class LattaError(validate.InputError):
    """A latta input that cannot be resolved, or a rule not yet supplied."""


LATTA_MEANS = "kick"

LATTA_RULE = (
    "Latta is a nakshatra-based planetary kick. Each planet has latta (kick) "
    "on a constellation based on its transit position. If a transit planet "
    "has latta on the constellation occupied by Moon (or lagna) in natal "
    "chart, then we may expect some unfavorable results related to the "
    "signification of the planet in natal chart.")

#: The two natal points a latta can land on. §26.4 and §26.6 read only from
#: the natal Moon's nakshatra; §26.7 is the first to offer the lagna's too,
#: and it offers it as an alternative rather than a second reading.
LATTA_TARGETS: tuple[str, ...] = ("natal Moon", "natal lagna")

#: **Finding.** Latta runs the opposite way round from the chapter's other
#: two counting techniques. §26.4's taras and §26.6's body parts count **from
#: the natal Moon's nakshatra to** the transiting graha; a latta is counted
#: **from the transiting graha** and asks whether it reaches a natal point.
#: §26.5's aspects share that origin, so latta is an aspect-shaped rule read
#: against a natal target.
LATTA_COUNTS_FROM_THE_TRANSIT_NOT_THE_NATAL_POINT = (
    "A tara and a body part are counted from the natal Moon's nakshatra to "
    "the transit. A latta is counted from the transit position, and the "
    "question is whether it falls on the natal Moon's nakshatra or the "
    "natal lagna's."
)

#: **Finding.** The harm is read from the graha's **natal** significations,
#: not from its nature. So a benefic can kick, and what it spoils is whatever
#: it owns or signifies in that chart — the same functional reading Exercise
#: 41 used without announcing it, here stated in the rule itself.
THE_HARM_IS_READ_FROM_THE_NATAL_SIGNIFICATION = (
    "Section 26.7 says the unfavourable results relate to \"the signification "
    "of the planet in natal chart\". Nothing in the rule turns on the "
    "graha's natural benefic or malefic nature, so a benefic's latta spoils "
    "what that benefic signifies natally."
)

#: **Not supplied.** §26.7 says each planet has a latta and does not say, on
#: this page, which constellation each kicks. Until that arrives nothing here
#: computes a latta; `LATTA_OFFSETS` stays empty and `latta` raises.
LATTA_OFFSETS: dict[str, int] = {}

LATTA_OFFSETS_ARE_NOT_SUPPLIED = (
    "Section 26.7's opening states the rule and not the offsets. Which "
    "constellation each graha kicks has not been given, so no latta is "
    "computed and none is guessed."
)


def nakshatra_of(longitude: float) -> int:
    """The nakshatra index a longitude falls in, 0 = Aswini."""
    value = validate.longitude("longitude", float(longitude))
    return min(int(value // (360.0 / 27.0)), 26)


def latta(graha: str, transit_longitude: float) -> dict:
    """The nakshatra `graha` kicks from where it stands.

    :raises LattaError: always, until §26.7's offsets are supplied.
    """
    if not LATTA_OFFSETS:
        raise LattaError(LATTA_OFFSETS_ARE_NOT_SUPPLIED)
    if graha not in LATTA_OFFSETS:                      # pragma: no cover
        raise LattaError(f"no latta offset for {graha!r}")
    start = nakshatra_of(transit_longitude)             # pragma: no cover
    index = (start + LATTA_OFFSETS[graha] - 1) % 27     # pragma: no cover
    return {                                            # pragma: no cover
        "graha": graha,
        "from_nakshatra": str(NAKSHATRA_NAMES[start]),
        "offset": LATTA_OFFSETS[graha],
        "kicks": str(NAKSHATRA_NAMES[index]),
        "kicks_index": index,
    }
