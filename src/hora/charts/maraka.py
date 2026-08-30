"""Section 14.2 — marakas.

Two kinds, and the book keeps them apart because they feed different dasas.
A **maraka sthana** is a rasi — the one holding the 2nd or 7th house — and
matters for rasi-ruled dasas. A **maraka graha** is a planet, and matters for
planet-ruled dasas.

Beyond the two house lords, §14.2 admits any malefic that "powerfully"
conjoins or aspects the 2nd or 7th house or their lords. It never says what
makes a contact powerful, so every contact is reported with what made it and
nothing is filtered on a threshold the section does not give.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.aspects import graha_aspects_sign
from hora.core import validate
from hora.core.const import (
    ADDITIONAL_MARAKA_TARGETS,
    GRAHA_NAMES,
    HOUSES_OF_LIFE,
    MARAKA_DERIVATION,
    MARAKA_HOUSES,
    RASI_LORD,
    RASI_NAMES,
    Graha,
)

#: §14.2's own list, less the two whose nature is conditional. The Moon's
#: depends on his phase and Mercury's on his association, and neither worked
#: example uses either — see OI-105.
MALEFICS: frozenset[int] = frozenset({
    int(Graha.SUN), int(Graha.MARS), int(Graha.SATURN),
    int(Graha.RAHU), int(Graha.KETU),
})

def _ordinal(n: int) -> str:
    """2 -> "2nd", 7 -> "7th". The book writes them out, so we do too."""
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }"


#: Scorpio and Aquarius have two lords each, so a maraka house falling in one
#: yields two maraka grahas rather than one. §14.2 names only Saturn for
#: Aquarius in its first example and does not discuss co-lordship, so the
#: co-lord is included and labelled rather than assumed away. See OI-108.
CO_LORDS: dict[int, tuple[int, int]] = {
    7: (int(Graha.MARS), int(Graha.KETU)),
    10: (int(Graha.SATURN), int(Graha.RAHU)),
}


class MarakaError(validate.InputError):
    """Raised when a maraka question cannot be answered."""


@dataclass(frozen=True)
class Maraka:
    """One maraka graha, and how it qualified."""

    graha: int
    graha_name: str
    #: "house lord" or "malefic contact".
    kind: str
    #: Every reason it qualified. A planet can qualify more than one way.
    reasons: tuple[str, ...]


def houses_of_life() -> dict[int, str]:
    """§14.2: the 3rd and the 8th, and what each shows."""
    return dict(HOUSES_OF_LIFE)


def maraka_houses() -> tuple[int, ...]:
    """The 2nd and 7th, derived as the 12th from each house of life."""
    derived = tuple(sorted(
        ((life + 12 - 2) % 12) + 1 for life in HOUSES_OF_LIFE))
    if derived != tuple(sorted(MARAKA_HOUSES)):  # pragma: no cover
        raise MarakaError(
            f"the 12th from {sorted(HOUSES_OF_LIFE)} is {derived}, not "
            f"{sorted(MARAKA_HOUSES)}")
    return derived


def maraka_sthanas(lagna: int) -> dict[int, int]:
    """The rasis holding the 2nd and 7th houses. House number -> rasi."""
    index = validate.in_range("lagna", lagna, 0, 11)
    return {house: (index + house - 1) % 12 for house in maraka_houses()}


def _lords_of(sign: int) -> tuple[int, ...]:
    return CO_LORDS.get(sign, (int(RASI_LORD[sign]),))


def maraka_grahas(lagna: int) -> dict[int, tuple[int, ...]]:
    """The lords of the 2nd and 7th. House number -> its lord or co-lords."""
    return {house: _lords_of(sign)
            for house, sign in maraka_sthanas(lagna).items()}


def additional_marakas(lagna: int, graha_signs: dict[int, int],
                       malefic: frozenset[int] | None = None
                       ) -> dict[int, tuple[str, ...]]:
    """Malefics reaching a maraka house or its lord, and how.

    §14.2's second kind. Contacts are conjunction and graha drishti only —
    the section says "using graha drishti" outright, so rasi drishti does not
    qualify a maraka here.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    for graha, place in graha_signs.items():
        validate.in_range(f"graha {graha} sign", int(place), 0, 11)
    positions = {int(g): int(s) for g, s in graha_signs.items()}
    evil = MALEFICS if malefic is None else malefic

    sthanas = maraka_sthanas(index)
    lords = maraka_grahas(index)
    targets: list[tuple[str, int, int | None]] = []
    for house, sign in sthanas.items():
        targets.append(
            (f"the {_ordinal(house)} house ({RASI_NAMES[sign]})", sign, None))
        for lord in lords[house]:
            if lord in positions:
                targets.append(
                    (f"the {_ordinal(house)} lord {GRAHA_NAMES[lord]}",
                     positions[lord], lord))

    found: dict[int, list[str]] = {}
    for graha, place in sorted(positions.items()):
        if graha not in evil:
            continue
        for label, target, owner in targets:
            if owner == graha:
                continue  # a planet does not reach itself
            if place == target:
                found.setdefault(graha, []).append(f"conjoins {label}")
            elif graha_aspects_sign(graha, place, target):
                found.setdefault(graha, []).append(f"aspects {label}")
    return {graha: tuple(reasons) for graha, reasons in found.items()}


def marakas(lagna: int, graha_signs: dict[int, int] | None = None) -> dict:
    """Every maraka §14.2 admits, with how each qualified.

    :param graha_signs: needed for the second kind. Without it only the house
        lords are returned, and the answer says so rather than implying the
        list is complete.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    sthanas = maraka_sthanas(index)
    lords = maraka_grahas(index)

    found: dict[int, Maraka] = {}
    for house, owners in lords.items():
        for lord in owners:
            reason = (f"owns the {_ordinal(house)} house "
                      f"({RASI_NAMES[sthanas[house]]})")
            if len(owners) > 1:
                reason += " as co-lord"
            if lord in found:
                found[lord] = Maraka(
                    lord, found[lord].graha_name, found[lord].kind,
                    found[lord].reasons + (reason,))
            else:
                found[lord] = Maraka(
                    lord, str(GRAHA_NAMES[lord]), "house lord", (reason,))

    complete = graha_signs is not None
    if complete:
        assert graha_signs is not None
        for graha, reasons in additional_marakas(index, graha_signs).items():
            if graha in found:
                found[graha] = Maraka(
                    graha, found[graha].graha_name, found[graha].kind,
                    found[graha].reasons + reasons)
            else:
                found[graha] = Maraka(
                    graha, str(GRAHA_NAMES[graha]), "malefic contact", reasons)

    return {
        "lagna": index,
        "lagna_name": str(RASI_NAMES[index]),
        "houses_of_life": {
            house: {"shows": shows,
                    "rasi": str(RASI_NAMES[(index + house - 1) % 12])}
            for house, shows in HOUSES_OF_LIFE.items()
        },
        "derivation": [
            {"house_of_life": life, "twelfth_from_it": death}
            for life, death in MARAKA_DERIVATION
        ],
        "maraka_sthanas": [
            {"house": house, "rasi": sign,
             "rasi_name": str(RASI_NAMES[sign])}
            for house, sign in sorted(sthanas.items())
        ],
        "maraka_grahas": [
            {"graha": m.graha, "graha_name": m.graha_name, "kind": m.kind,
             "reasons": list(m.reasons)}
            for m in sorted(found.values(), key=lambda m: m.graha)
        ],
        "malefic_contacts_included": complete,
        "targets": list(ADDITIONAL_MARAKA_TARGETS),
        "incomplete_note": (
            None if complete else
            "Only the lords of the 2nd and 7th are listed. Section 14.2 also "
            "admits any malefic that conjoins or aspects those houses or "
            "their lords, which needs the chart's graha positions."
        ),
    }
