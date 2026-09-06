"""§26.7 — latta, the nakshatra a transiting graha kicks.

Each graha kicks one constellation, counted from where it stands in transit.
The kick matters when it lands on the nakshatra the **natal** Moon or lagna
occupies, and what it spoils is that graha's significations **in the natal
chart** — not its natural ones.

Two things separate this from the chapter's other nakshatra techniques, and
both are recorded below. Its origin is the **transit** position where §26.4
and §26.6 count from the natal Moon's; and it admits the **lagna's** nakshatra
as an alternative target, which nothing before it in the chapter has done.

Only the **forward** kicks have been supplied — the Sun's, Mars's, Jupiter's
and Saturn's. `LATTA_GRAHAS_PENDING` names the rest and `latta` refuses them,
so nothing here guesses a kick.
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

PUROLATTA_MEANS = "forward kick"

#: The forward kicks, as §26.7 lists them. Each is an **inclusive** count
#: forward from the graha's own transit nakshatra.
PUROLATTA_OFFSETS: dict[str, int] = {
    "Sun": 12,
    "Mars": 3,
    "Jupiter": 6,
    "Saturn": 8,
}

#: §26.7's own check on each forward kick, as (graha, from, kicked).
PUROLATTA_EXAMPLES: tuple[tuple[str, str, str], ...] = (
    ("Sun", "Mrigashira", "Vishakha"),
    ("Mars", "Mrigashira", "Punarvasu"),
    ("Jupiter", "Krittika", "Pushya"),
    ("Saturn", "Krittika", "Magha"),
)

#: Every kick supplied so far, as graha -> offset and direction. Grows as the
#: section's other groups arrive.
LATTA_KICKS: dict[str, dict[str, object]] = {
    graha: {"offset": offset, "direction": "forward", "name": "purolatta"}
    for graha, offset in PUROLATTA_OFFSETS.items()
}

#: The nine bodies §26.6 covers, for measuring what §26.7 has still to give.
_ALL_BODIES: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu")

LATTA_GRAHAS_PENDING: tuple[str, ...] = tuple(
    graha for graha in _ALL_BODIES if graha not in LATTA_KICKS)

#: **Finding.** Calling this group the **forward** kick implies a backward one,
#: and the grahas left over are exactly the ones a savya/apasavya split would
#: put in the other group. Which they are, and whether the nodes are included
#: at all, the section has not said — `LATTA_GRAHAS_PENDING` names them and
#: nothing is assumed.
PUROLATTA_IMPLIES_A_BACKWARD_GROUP = (
    "The heading is \"Purolatta (forward kick)\" and every one of its four "
    "rules says \"reckoned in the forward direction\", so a backward kick is "
    "implied for the rest. The Moon, Mercury and Venus have no kick yet, and "
    "whether Rahu and Ketu have one at all is not stated."
)

#: **Finding.** The four forward offsets are 12, 3, 6 and 8 — all different,
#: none of them 1, so no graha kicks the nakshatra it stands in. They match
#: nothing else in the chapter: §26.5 gives Mars a 3rd aspect too, and that
#: is the only coincidence among the four.
THE_FORWARD_OFFSETS_ARE_DATA = (
    "Sun 12, Mars 3, Jupiter 6, Saturn 8. Four distinct offsets, none equal "
    "to 1, and no relation to the nakshatra aspects of section 26.5 beyond "
    "Mars's 3rd appearing in both."
)

LATTA_OFFSETS_ARE_NOT_SUPPLIED = (
    "Section 26.7 has given the forward kicks only. The Moon, Mercury and "
    "Venus have no kick yet and the nodes are unmentioned, so a latta is "
    "computed for the four supplied and refused for the rest."
)


def nakshatra_of(longitude: float) -> int:
    """The nakshatra index a longitude falls in, 0 = Aswini."""
    value = validate.longitude("longitude", float(longitude))
    return min(int(value // (360.0 / 27.0)), 26)


def latta(graha: str, transit_longitude: float) -> dict:
    """The nakshatra `graha` kicks from where it stands.

    :raises LattaError: for a graha whose kick §26.7 has not yet given.
    """
    kick = LATTA_KICKS.get(graha)
    if kick is None:
        raise LattaError(
            f"section 26.7 has not given a latta for {graha!r}; "
            f"{LATTA_OFFSETS_ARE_NOT_SUPPLIED}")
    offset = int(kick["offset"])  # type: ignore[call-overload]
    start = nakshatra_of(transit_longitude)
    index = ((start + offset - 1) if kick["direction"] == "forward"
             else (start - offset + 1)) % 27
    return {
        "graha": graha,
        "from_nakshatra": str(NAKSHATRA_NAMES[start]),
        "from_index": start,
        "offset": offset,
        "direction": kick["direction"],
        "kick": kick["name"],
        "kicks": str(NAKSHATRA_NAMES[index]),
        "kicks_index": index,
    }


def latta_hits(graha: str, transit_longitude: float,
               natal_moon_longitude: float,
               natal_lagna_longitude: float | None = None) -> dict:
    """Does `graha`'s kick land on a natal point §26.7 names?

    :param natal_lagna_longitude: optional. §26.7 offers the lagna's
        nakshatra as an alternative to the Moon's, so a caller with only the
        Moon gets a verdict on the Moon alone and is told so.
    """
    kicked = latta(graha, transit_longitude)
    moon = nakshatra_of(natal_moon_longitude)
    lagna = (None if natal_lagna_longitude is None
             else nakshatra_of(natal_lagna_longitude))
    hits = [name for name, index in (("natal Moon", moon),
                                     ("natal lagna", lagna))
            if index is not None and index == kicked["kicks_index"]]
    return {
        **kicked,
        "natal_moon_nakshatra": str(NAKSHATRA_NAMES[moon]),
        "natal_lagna_nakshatra": (
            None if lagna is None else str(NAKSHATRA_NAMES[lagna])),
        "hits": hits,
        "kicked": bool(hits),
        "lagna_not_supplied": lagna is None,
        "results": (
            "unfavorable results related to the signification of the planet "
            "in natal chart" if hits else None),
        "significations_are_natal": THE_HARM_IS_READ_FROM_THE_NATAL_SIGNIFICATION,
    }
