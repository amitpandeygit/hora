"""§18.2.1 — Narayana dasa's progression of signs.

Narayana dasa progresses the lagna: each dasa makes a different rasi the
native's lagna, so a chart is read twelve times over a life. This module
settles which rasi holds each period and in what order; the lengths are a
separate question.

Three things decide the order, all from §18.2.1:

* the **dasa seed** — lagna or the 7th, whichever is stronger by §15.5.2;
* the **movement**, from the seed's modality, each governed by one of the
  Trimurthis: Brahma for movable, Shiva for fixed, Vishnu for dual;
* the **direction**, from whether the 9th house from the seed is odd- or
  even-footed.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    MODALITY_NAMES,
    RASI_IS_ODD_FOOTED,
    RASI_MODALITY,
    RASI_NAMES,
)


class NarayanaError(validate.InputError):
    """A Narayana dasa input that cannot be resolved."""


#: §18.2.1 assigns each modality to one of the Trimurthis, and each god to a
#: movement. Keyed by our modality name.
MOVEMENTS: dict[str, dict] = {
    "chara": {
        "god": "Brahma", "modality": "movable",
        "movement": "regular",
        "text": "Brahma is associated with the regular movement of 1st, 2nd, 3rd etc.",
    },
    "sthira": {
        "god": "Shiva", "modality": "fixed",
        "movement": "sixth",
        "text": ("Shiva ... is associated with the 6th movment. We take dasa "
                 "seed, 6th from there, 6th from there and so on."),
    },
    "dwiswabhava": {
        "god": "Vishnu", "modality": "dual",
        "movement": "trinal",
        "text": ("Vishnu is associated with the trinal movement, i.e. 1st, "
                 "5th, 9th, then 10th, 2nd, 6th and so on. We cover the "
                 "trines from dasa seed first, go to another quadrant and "
                 "cover its trines and so on."),
    },
}

#: §18.2.1's direction rule, as printed.
DIRECTION_RULE = (
    "The direction of reckoning these houses is based on the 9th house from "
    "dasa seed. If the 9th house from dasa seed is an odd-footed sign (Ar, "
    "Ta, Ge and Li, Sc, Sg), the direction is forward. If the 9th house from "
    "dasa seed is an even-footed sign (Cn, Le, Vi and Cp, Aq, Pi), the "
    "direction is backward."
)

#: §18.2.1 prints the trinal movement only as far as "1st, 5th, 9th, then
#: 10th, 2nd, 6th and so on", leaving the quadrant order after the 10th open.
#: Example 64 closes it outright: "then count the same houses from the 10th
#: house, then from the 7th house and finally from the 4th house." Each next
#: quadrant is the 10th from the previous, which is what this module does.
VISHNU_QUADRANT_ORDER = (
    "We count the 1st, 5th, 9th houses from dasa seed, then count the same "
    "houses from the 10th house, then from the 7th house and finally from "
    "the 4th house."
)


def movement_of(sign: int) -> dict:
    """Which of §18.2.1's three movements a sign takes, and whose it is."""
    index = validate.in_range("sign", sign, 0, 11)
    return MOVEMENTS[str(MODALITY_NAMES[RASI_MODALITY[index]])]


def house_order(sign: int) -> tuple[int, ...]:
    """The houses, in the order this sign's movement visits them.

    Always a permutation of 1 to 12: every rasi holds exactly one dasa.
    """
    movement = movement_of(sign)["movement"]
    if movement == "regular":
        return tuple(1 + k for k in range(12))
    if movement == "sixth":
        houses, house = [], 1
        for _ in range(12):
            houses.append(house)
            house = (house - 1 + 5) % 12 + 1        # the 6th from here
        return tuple(houses)

    houses, quadrant = [], 1                        # trinal
    for _ in range(4):
        houses += [(quadrant - 1 + 4 * k) % 12 + 1 for k in range(3)]
        quadrant = (quadrant - 1 + 9) % 12 + 1      # the 10th from here
    return tuple(houses)


def direction_of(seed: int) -> str:
    """``forward`` or ``backward``, from the 9th house from the seed.

    The rule reads the 9th **zodiacally**, before any direction is known —
    the direction is what it decides, so it cannot also depend on it.
    """
    index = validate.in_range("seed", seed, 0, 11)
    ninth = (index + 8) % 12
    return "forward" if RASI_IS_ODD_FOOTED[ninth] else "backward"


@dataclass(frozen=True, slots=True)
class Progression:
    """The order in which rasis take their Narayana dasa."""

    seed: int
    seed_name: str
    god: str
    movement: str
    direction: str
    ninth_from_seed: int
    ninth_name: str
    #: Sign index per period, in order. Twelve entries, each rasi once.
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    #: The house numbers those signs answer to, before direction is applied.
    houses: tuple[int, ...]
    why: str


def progression(seed: int) -> Progression:
    """§18.2.1's full order of rasis for one dasa seed.

    :param seed: the stronger of lagna and the 7th, as a sign index.
    :raises NarayanaError: on a sign outside 0-11.
    """
    index = validate.in_range("seed", seed, 0, 11)
    movement = movement_of(index)
    direction = direction_of(index)
    houses = house_order(index)
    step = 1 if direction == "forward" else -1
    signs = tuple((index + step * (house - 1)) % 12 for house in houses)
    ninth = (index + 8) % 12
    return Progression(
        seed=index, seed_name=str(RASI_NAMES[index]),
        god=str(movement["god"]), movement=str(movement["movement"]),
        direction=direction, ninth_from_seed=ninth,
        ninth_name=str(RASI_NAMES[ninth]),
        signs=signs, sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        houses=houses,
        why=(f"{RASI_NAMES[index]} is {movement['modality']}, so "
             f"{movement['god']} governs it and the movement is "
             f"{movement['movement']}; the 9th from it is {RASI_NAMES[ninth]}, "
             f"{'odd' if RASI_IS_ODD_FOOTED[ninth] else 'even'}-footed, so the "
             f"direction is {direction}"),
    )


#: §18.2.1's own name for the stronger of lagna and the 7th.
DASA_SEED_RULE = (
    "Dasas start from lagna or the 7th house, whichever is stronger. We use "
    "the rules of strength explained in the chapter \"Strength of Planets and "
    "Rasis\". Let us denote the stronger of lagna and 7th house by the "
    "expression \"dasa seed\"."
)


def dasa_seed(lagna: int, longitudes: dict[int, float]) -> dict:
    """The stronger of lagna and the 7th, by §15.5.2's cascade.

    Narayana is a phalita dasa, and §15.5.2 says the Mercury/Jupiter/lord
    reading is "important for Narayana dasa and other phalita dasas", so that
    is the purpose used.

    :returns: the seed, the pair compared, and which rule settled it. When the
        cascade cannot decide, ``seed`` is None and the reason says so rather
        than a side being picked.
    """
    from hora.charts.rasi_strength import stronger

    index = validate.in_range("lagna", lagna, 0, 11)
    seventh = (index + 6) % 12
    verdict = stronger(index, seventh, longitudes, purpose="phalita")
    return {
        "lagna": index,
        "lagna_name": str(RASI_NAMES[index]),
        "seventh": seventh,
        "seventh_name": str(RASI_NAMES[seventh]),
        "seed": verdict.winner,
        "seed_name": None if verdict.winner is None else str(RASI_NAMES[verdict.winner]),
        "decided_by": verdict.decided_by,
        "reason": verdict.reason,
    }
