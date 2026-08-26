"""Comparing the strength of two planets — book chapter 15.

§9.2 needs this: "we have to take the stronger of Mars and Ketu as the lord of
Scorpio". So do rasi dasas, which "start from the stronger of lagna and the 7th
house", and any house influenced by planets suggesting contradictory results.

**What this module will not do is invent a number.** The chapter names five
measures of strength and derives one of them:

===============  =========  ==================================================
Measure          Available  Why
===============  =========  ==================================================
shadbala             no     "beyond the scope of this book"
ashtakavarga         no     not implemented
avastha bala        yes     §15.4 defines age, alertness and mood
vimsopaka bala       no     not implemented
simple rules         no     named but not stated in the material transcribed
===============  =========  ==================================================

The last row is the one §9.2 actually wants — the chapter says the rules for
"trivial things like determining who initiates dasas" are "very simple rules
that are different from shadbala, ashtakavarga bala, avastha bala, Vimsopaka
bala". Until those rules are in hand, :func:`compare` reports what avastha
says and marks the verdict as coming from a measure the book did not nominate
for this purpose. It is a defensible input to a decision, not the decision.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.avastha import all_avasthas
from hora.core import validate
from hora.core.const import GRAHA_NAMES
from hora.core.ephemeris.base import PlanetPosition


class StrengthError(validate.InputError):
    """A strength comparison that cannot be made."""


#: §15.4.2's three levels, ordered. This is the one ranking the material states
#: outright — "full", "medium", "negligible" results.
ALERTNESS_RANK: dict[str, int] = {"Jaagrita": 3, "Swapna": 2, "Sushupta": 1}

#: §15.4.1's results as an order. Vriddha is omitted, not ranked: its result is
#: given as "Some", which cannot be placed against "Quarter" without inventing
#: a value the book does not supply.
AGE_RANK: dict[str, int] = {"Yuva": 4, "Kumaara": 3, "Saisava": 2, "Mrita": 0}


@dataclass(frozen=True)
class AxisVerdict:
    """What one measure says about which of two planets is stronger."""

    axis: str
    #: The winning graha, or None when the axis ties or cannot rank them.
    winner: int | None
    winner_name: str | None
    left: str
    right: str
    determined: bool
    reason: str


@dataclass(frozen=True)
class Comparison:
    """The full comparison of two grahas, axis by axis."""

    left: int
    left_name: str
    right: int
    right_name: str
    axes: tuple[AxisVerdict, ...]
    #: The agreed winner, or None when the axes disagree or cannot decide.
    winner: int | None
    winner_name: str | None
    determined: bool
    reason: str
    #: Always present: the measure the book nominates for this is not available.
    caveat: str


BOOK_CAVEAT = (
    "The book decides this kind of comparison with shadbala, or with the "
    "'very simple rules' it mentions for trivial determinations. Neither is "
    "implemented — shadbala is explicitly beyond the scope of the book, and "
    "the simple rules are not in the material transcribed so far. This verdict "
    "rests on avastha alone, which the book does not nominate for this "
    "purpose. Treat it as evidence, not as the answer."
)


def _age_axis(a, b, left: int, right: int) -> AxisVerdict:
    la, lb = a.age.name, b.age.name
    if la not in AGE_RANK or lb not in AGE_RANK:
        unranked = [n for n in (la, lb) if n not in AGE_RANK]
        return AxisVerdict(
            "age", None, None, la, lb, False,
            f"{', '.join(unranked)} gives 'Some' results, which the book does "
            f"not quantify, so it cannot be ranked",
        )
    if AGE_RANK[la] == AGE_RANK[lb]:
        return AxisVerdict("age", None, None, la, lb, True, "both in the same state")
    winner = left if AGE_RANK[la] > AGE_RANK[lb] else right
    return AxisVerdict(
        "age", winner, GRAHA_NAMES[winner], la, lb, True,
        f"{la} gives {a.age.results.lower()} results, {lb} gives "
        f"{b.age.results.lower()}",
    )


def _alertness_axis(a, b, left: int, right: int) -> AxisVerdict:
    la, lb = a.alertness.name, b.alertness.name
    if ALERTNESS_RANK[la] == ALERTNESS_RANK[lb]:
        return AxisVerdict("alertness", None, None, la, lb, True,
                           "both in the same state")
    winner = left if ALERTNESS_RANK[la] > ALERTNESS_RANK[lb] else right
    return AxisVerdict(
        "alertness", winner, GRAHA_NAMES[winner], la, lb, True,
        f"{la} gives {a.alertness.results} results, {lb} gives {b.alertness.results}",
    )


def compare(
    left: int,
    right: int,
    positions: dict[int, PlanetPosition],
) -> Comparison:
    """Compare two grahas on every measure this book defines.

    :returns: a :class:`Comparison` whose ``winner`` is set only when every
        axis that could decide agrees. Disagreement leaves it None with the
        reason — the caller decides, rather than being handed a coin flip.
    :raises StrengthError: if either graha has no position.
    """
    for graha in (left, right):
        if graha not in positions:
            raise StrengthError(f"no position given for {GRAHA_NAMES[graha]}")
    if left == right:
        raise StrengthError("cannot compare a graha with itself")

    a = all_avasthas(left, positions)
    b = all_avasthas(right, positions)
    axes = (_age_axis(a, b, left, right), _alertness_axis(a, b, left, right))

    decided = [ax for ax in axes if ax.determined and ax.winner is not None]
    if not decided:
        winner, reason = None, "no measure could separate them"
    else:
        winners = {ax.winner for ax in decided}
        if len(winners) == 1:
            winner = decided[0].winner
            reason = "agreed by " + " and ".join(ax.axis for ax in decided)
        else:
            winner = None
            reason = "the measures disagree: " + "; ".join(
                f"{ax.axis} favours {ax.winner_name}" for ax in decided
            )

    return Comparison(
        left=int(left), left_name=GRAHA_NAMES[left],
        right=int(right), right_name=GRAHA_NAMES[right],
        axes=axes,
        winner=winner,
        winner_name=GRAHA_NAMES[winner] if winner is not None else None,
        determined=winner is not None,
        reason=reason,
        caveat=BOOK_CAVEAT,
    )


def stronger(
    left: int, right: int, positions: dict[int, PlanetPosition]
) -> int | None:
    """Just the winner, or None when undetermined.

    Convenience for building §9.2's ``stronger_lord`` map. Returning None
    rather than picking arbitrarily is the point: the arudha endpoint will
    then say it cannot resolve the lord, which is the truth.
    """
    return compare(left, right, positions).winner
