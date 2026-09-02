"""Chapter 21 — Drigdasa, the aspect dasa.

"Drik means vision and drigdasa is a dasa based on aspects." It is the first
rasi dasa whose groups come from **aspects** rather than from houses: each of
the 9th, 10th and 11th brings itself and the three signs it aspects.

Three things separate it from chapters 19 and 20, and all three are easy to
carry over wrongly:

* its direction is **odd-footed**, not odd/even sign — chapters 19 and 20 both
  used the sign test and printed a NOTE warning against this one;
* it has **three** directions in a single run, one per group, each from its own
  leader's footedness, where every earlier rasi dasa had one;
* its groups do **not** always cover the twelve rasis. See OI-127.

Rule 5 sends the lengths to §18.2.2, so those come from
:mod:`hora.dasha.rasi.narayana` as they do for chapters 19 and 20.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import RASI_IS_ODD_FOOTED, RASI_NAMES
from hora.dasha.rasi.narayana import NarayanaError


class DrigdasaError(NarayanaError):
    """A Drigdasa input that cannot be resolved."""


#: §21.1's derivation of the name, which is also the rule in miniature.
DRIK_MEANS_VISION = (
    "Drik means vision and drigdasa is a dasa based on aspects."
)

#: What §21.1 says it shows. Part 2's map calls it "phalita - spirituality",
#: and this is the sentence behind that.
SHOWS_SPIRITUAL_VISION = (
    "It shows how spiritual vision develops in a native and steers one's "
    "life. If a native's chart promises spiritual growth, this dasa shows "
    "religious and spiritual activities and the evolution of one's soul."
)

#: §21.2's three group leaders, in order. Consecutive houses, which is what
#: makes their modalities one of each — and what OI-127 turns on.
GROUP_HOUSES: tuple[int, ...] = (9, 10, 11)

#: §21.2's direction test. Back to odd-**footed**, which §18.2.1 and §18.2.2
#: use and which chapters 19 and 20 both took pains to say they were *not*
#: using. The two classifications disagree on Taurus, Leo, Scorpio and
#: Aquarius, so carrying either chapter's rule here is wrong a third of the
#: time.
FOOTEDNESS_DECIDES_THE_DIRECTION = (
    "Order of reckoning is forward or backward based on whether the 9th house "
    "is odd-footed or even-footed."
)

#: Rule 5, the same borrowing chapters 19 and 20 make.
LENGTHS_ARE_NARAYANAS = (
    "Dasa periods of various rasis in this dasa system are found just like in "
    "Narayana dasa."
)


def direction_of(leader_sign: int) -> str:
    """A group's direction, from its leader's **footedness**.

    Not the odd/even sign test chapters 19 and 20 use. They differ on Taurus,
    Leo, Scorpio and Aquarius.
    """
    index = validate.in_range("leader_sign", leader_sign, 0, 11)
    return "forward" if RASI_IS_ODD_FOOTED[index] else "backward"


def group_signs(leader_sign: int, direction: str) -> tuple[int, ...]:
    """A leader and the three signs it aspects, in dasa order.

    The leader takes the first dasa; the three it aspects follow in zodiacal
    order from it when forward, anti-zodiacal when backward. §21.2 says only
    "forward or backward" and does not spell out the order within a group,
    so this is the reading — the leader is where the group starts because the
    section says dasas start from the 9th.
    """
    from hora.charts.aspects import rasi_drishti

    index = validate.in_range("leader_sign", leader_sign, 0, 11)
    if direction not in ("forward", "backward"):
        raise DrigdasaError(
            f"direction must be 'forward' or 'backward', got {direction!r}")
    aspected = set(rasi_drishti(index))
    step = 1 if direction == "forward" else -1
    ordered = [index]
    for offset in range(1, 12):
        candidate = (index + step * offset) % 12
        if candidate in aspected:
            ordered.append(candidate)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class Group:
    """One of §21.2's three groups of four."""

    house: int
    leader: int
    leader_name: str
    direction: str
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Progression:
    """The order in which rasis take their Drigdasa."""

    lagna: int
    lagna_name: str
    groups: tuple[Group, ...]
    #: Twelve dasas in order. Not necessarily twelve *distinct* rasis — see
    #: `covers_every_rasi`.
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    #: True when the three groups partition the zodiac. False for the four
    #: dual lagnas, whose 9th house is fixed. See OI-127.
    covers_every_rasi: bool
    #: Rasis taking two dasas, and rasis taking none. Empty when it covers.
    repeated: tuple[int, ...]
    omitted: tuple[int, ...]
    why: str


def progression(lagna: int) -> Progression:
    """§21.2's twelve dasas for one lagna.

    Built as the section reads. Where its groups overlap — the four dual
    lagnas — the overlap is reported rather than removed: deduplicating would
    invent an order the section does not give, and dropping a repeat would
    leave eleven dasas where it asks for twelve.
    """
    index = validate.in_range("lagna", lagna, 0, 11)

    groups: list[Group] = []
    for house in GROUP_HOUSES:
        leader = (index + house - 1) % 12
        direction = direction_of(leader)
        signs = group_signs(leader, direction)
        groups.append(Group(
            house=house, leader=leader, leader_name=str(RASI_NAMES[leader]),
            direction=direction, signs=signs,
            sign_names=tuple(str(RASI_NAMES[s]) for s in signs)))

    order = tuple(s for group in groups for s in group.signs)
    seen = {s: order.count(s) for s in set(order)}
    repeated = tuple(sorted(s for s, n in seen.items() if n > 1))
    omitted = tuple(sorted(s for s in range(12) if s not in seen))
    covers = not repeated and not omitted

    why = "; ".join(
        f"the {group.house}th is {group.leader_name}, "
        f"{'odd' if RASI_IS_ODD_FOOTED[group.leader] else 'even'}-footed, so "
        f"{group.direction}" for group in groups)
    if not covers:
        why += (f" — but {', '.join(RASI_NAMES[s] for s in repeated)} take two "
                f"dasas each and {', '.join(RASI_NAMES[s] for s in omitted)} "
                f"take none; see OI-127")
    return Progression(
        lagna=index, lagna_name=str(RASI_NAMES[index]), groups=tuple(groups),
        signs=order, sign_names=tuple(str(RASI_NAMES[s]) for s in order),
        covers_every_rasi=covers, repeated=repeated, omitted=omitted, why=why,
    )
