"""Section 13.4.2 — a family member's own lagna, read from one's chart.

The method is uniform: find the house that shows the person, take the rasi
holding that house's lord, and read it as their lagna. The arudha pada of the
same house is offered beside it, as §13.4.2 says it may be.

The one subtlety is direction. In D-3 and D-7 the sibling and child houses are
counted forward from an odd lagna and backward from an even one, which is why
a Gemini D-7 lagna gives Libra for the first child and a Cancer one gives
Pisces. Stepping by two then stays inside one parity class, so a chain runs
exactly six deep before §13.4.2's closing note takes over — and that note does
not say which sign of the other parity follows, so the seventh is refused.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.arudha import arudha_pada
from hora.core import validate
from hora.core.const import (
    FAMILY_CHAIN_DEPTH,
    FAMILY_CHARTS,
    FAMILY_NOTE,
    FAMILY_NOTE_IS_UNDERSPECIFIED,
    GRAHA_NAMES,
    NAMED_RELATIVES,
    RASI_LORD,
    RASI_NAMES,
)

#: relation -> chart, flattened from `FAMILY_CHARTS`.
CHART_FOR: dict[str, str] = {
    relation: chart
    for chart, relations in FAMILY_CHARTS
    for relation in relations
}

#: The relations whose house §13.4.2 fixes outright.
HOUSE_FOR: dict[str, tuple[str, int]] = {
    name: (chart, house) for name, chart, house in NAMED_RELATIVES
}


class FamilyError(validate.InputError):
    """Raised when a family question cannot be answered."""


@dataclass(frozen=True)
class Relative:
    """One family member, and the lagna to read their fortunes from."""

    relation: str
    #: 1 for the immediate sibling or first child, 2 for the next, and so on.
    index: int
    chart: str
    #: The house in that chart which shows them.
    house: int
    #: "forward" or "backward" — how the house was counted.
    direction: str
    #: The rasi that house falls in.
    house_sign: int
    #: The rasi holding that house's lord: their lagna.
    lagna: int
    lord: int
    #: The arudha pada of the same house, when graha positions allow it.
    arudha: str
    arudha_sign: int | None
    why: str


def counts_forward(lagna: int) -> bool:
    """§13.4.2: forward from an odd lagna, backward from an even one.

    Aries is the 1st sign and therefore odd, so sign index 0 counts forward.
    """
    return validate.in_range("lagna", lagna, 0, 11) % 2 == 0


def house_sign(house: int, lagna: int, *, directional: bool) -> int:
    """The rasi a house falls in.

    :param directional: True in D-3 and D-7, where §13.4.2's forward/backward
        rule applies. False everywhere else, including D-12's 9th and 4th.
    """
    validate.in_range("house", house, 1, 12)
    index = validate.in_range("lagna", lagna, 0, 11)
    step = house - 1
    if directional and not counts_forward(index):
        step = -step
    return (index + step) % 12


def sibling_house(index: int, *, elder: bool) -> int:
    """The house showing the `index`-th younger or elder sibling.

    Younger runs 3rd, 5th, 7th …; elder runs 11th, 9th, 7th …
    """
    _check_depth(index, "sibling")
    base, step = (11, -2) if elder else (3, 2)
    return ((base + step * (index - 1) - 1) % 12) + 1


def child_house(index: int) -> int:
    """The house showing the `index`-th child: 5th, 7th, 9th …"""
    _check_depth(index, "child")
    return ((5 + 2 * (index - 1) - 1) % 12) + 1


def _check_depth(index: int, what: str) -> None:
    validate.in_range(f"{what} index", index, 1, 99)
    if index > FAMILY_CHAIN_DEPTH:
        raise FamilyError(
            f"the {what} chain runs {FAMILY_CHAIN_DEPTH} deep before it would "
            f"return to its own first sign. Section 13.4.2's note says "
            f'"{FAMILY_NOTE}" — but not which sign of the other parity comes '
            f"next, and no example reaches a seventh. "
            f"{FAMILY_NOTE_IS_UNDERSPECIFIED}"
        )


def _relative(relation: str, index: int, chart: str, house: int, lagna: int,
              directional: bool, graha_signs: dict[int, int] | None,
              stronger_lord: dict[int, int] | None) -> Relative:
    sign = house_sign(house, lagna, directional=directional)
    lord = int(RASI_LORD[sign])
    direction = (
        "forward" if not directional or counts_forward(lagna) else "backward")

    arudha_sign: int | None = None
    if graha_signs is not None:
        arudha_sign = arudha_pada(
            house, lagna, graha_signs, stronger_lord).sign

    why = (
        f"in {chart} the {house}th house shows {relation}"
        f"{'' if index == 0 else f' number {index}'}; counting {direction} "
        f"from {RASI_NAMES[lagna]} that is {RASI_NAMES[sign]}, whose lord "
        f"{GRAHA_NAMES[lord]} sits in the rasi read as their lagna"
    )
    if arudha_sign is None:
        why += (f"; no graha positions were given, so A{house} "
                "was not computed")
    return Relative(
        relation=relation, index=index, chart=chart, house=house,
        direction=direction, house_sign=sign, lagna=sign, lord=lord,
        arudha=f"A{house}", arudha_sign=arudha_sign, why=why,
    )


def named(relation: str, lagna: int,
          graha_signs: dict[int, int] | None = None,
          stronger_lord: dict[int, int] | None = None) -> Relative:
    """Father or mother — the two §13.4.2 fixes a house for.

    The direction rule is scoped to D-3 and D-7, so these count forward.
    """
    if relation not in HOUSE_FOR:
        raise FamilyError(
            f"section 13.4.2 fixes a house only for "
            f"{', '.join(sorted(HOUSE_FOR))}; for a sibling or a child use "
            f"sibling() or child(), and for anything else choose the house "
            f"yourself and use relative()")
    chart, house = HOUSE_FOR[relation]
    return _relative(relation, 0, chart, house, lagna, False, graha_signs,
                     stronger_lord)


def sibling(index: int, lagna: int, *, elder: bool,
            graha_signs: dict[int, int] | None = None,
            stronger_lord: dict[int, int] | None = None) -> Relative:
    """The `index`-th elder or younger sibling, from a D-3 lagna."""
    house = sibling_house(index, elder=elder)
    return _relative(
        f"{'elder' if elder else 'younger'} sibling", index, "D3", house,
        lagna, True, graha_signs, stronger_lord)


def child(index: int, lagna: int,
          graha_signs: dict[int, int] | None = None,
          stronger_lord: dict[int, int] | None = None) -> Relative:
    """The `index`-th child, from a D-7 lagna."""
    return _relative("child", index, "D7", child_house(index), lagna, True,
                     graha_signs, stronger_lord)


def relative(relation: str, chart: str, house: int, lagna: int,
             graha_signs: dict[int, int] | None = None,
             stronger_lord: dict[int, int] | None = None,
             directional: bool = False) -> Relative:
    """Any relation, once the caller has chosen the chart and house.

    §13.4.2 names four charts and two houses; for a grandparent, an uncle or a
    spouse's brother it gives the chart and leaves the house to the reader.
    """
    if chart not in {c for c, _ in FAMILY_CHARTS}:
        raise FamilyError(
            f"section 13.4.2 names {', '.join(c for c, _ in FAMILY_CHARTS)}; "
            f"{chart!r} is not one of them")
    return _relative(relation, 0, chart, house, lagna, directional,
                     graha_signs, stronger_lord)
