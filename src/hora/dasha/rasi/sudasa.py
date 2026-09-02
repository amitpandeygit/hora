"""Chapter 20 — Sudasa, the Sree Lagna Kendradi Rasi Dasa.

§19.3 named it before it arrived: "Sudasa is also a Kendradi Rasi Dasa, but
started from Sree Lagna instead of lagna", and §19.4 ranked it above Lagna
Kendradi for the matter both read. So the walk is chapter 19's and the lengths
are §18.2.2's, and what chapter 20 adds is three things:

* the seed is the **Sree Lagna's rasi** outright — no §15.5.2 comparison, so
  no stronger-of-lagna-and-7th and nothing for §15.5.1 to settle;
* the direction comes from **SL's** own oddity rather than lagna's;
* the first dasa is only **partly left at birth**, by a fraction §20.2 gives —
  the first balance the book has put on a rasi dasa.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import RASI_IS_ODD, RASI_NAMES
from hora.dasha.rasi.kendradi import (
    GROUPS,
    HOUSE_ORDER,
    KendradiError,
    house_signs,
)


class SudasaError(KendradiError):
    """A Sudasa input that cannot be resolved."""


#: §20.1's three names for one dasa. "Rasi Dasa" unqualified means this one,
#: which is worth knowing before reading it as a category.
NAMES: tuple[str, ...] = (
    "Sudasa", "Sree Lagna Kendradi Rasi Dasa", "Rasi Dasa",
)

#: What §20.1 says it is for. Narayana is general purpose (§18.6), Lagna
#: Kendradi shows material success (§19.1), and this is the sharpest of the
#: three — money, power and authority specifically.
SHOWS = (
    "Sudasa is important for materialistic things like money, power and "
    "authority. It can be used to predict financial matters and matters "
    "related to status and power."
)

#: §20.1's three claims, stated as consequences rather than tendencies — "he
#: **must** be enjoying a favorable dasa". They are the strongest falsifiable
#: statements the book makes about any dasa, and a reading layer that softens
#: them says less than the book does.
DIAGNOSTIC_CLAIMS: tuple[dict, ...] = (
    {"observed": "a political leader occupies a post of power",
     "implies": "a favorable dasa as per Sudasa"},
    {"observed": "a businessman sees increasing profits",
     "implies": "a favorable dasa as per Sudasa"},
    {"observed": "someone struggles with tight finances",
     "implies": "an unfavorable dasa as per Sudasa"},
)

#: §20.2 rule 2, which is §19.2's sentence with SL for lagna and the NOTE
#: kept. The odd/even **sign** test again, not the odd-footed one.
DIRECTION_RULE = (
    "The direction of reckoning dasas is forward or backward based on whether "
    "SL is in an odd sign or an even sign. NOTE: We are talking about odd and "
    "even signs here and not about odd-footed and even-footed signs."
)

#: §19.2's rule 2 carried two exceptions — Saturn in the seed forces the order
#: forward, Ketu reverses it. §20.2's rule 2 is the same sentence with those
#: two dropped. They were phrased "in the stronger of lagna and 7th", which
#: Sudasa has no analogue for, so the omission may be because the phrase does
#: not apply rather than because the exceptions do not. Nothing is applied
#: here either way. See OI-126.
SEED_EXCEPTIONS_NOT_RESTATED = (
    "If Saturn is in the stronger of lagna and 7th, dasa order is forward. If "
    "Ketu is in the stronger of lagna and 7th, dasa order is reversed."
)

#: §20.2 rule 6, the same borrowing §19.2 made.
LENGTHS_ARE_NARAYANAS = (
    "Dasa periods of various rasis in this dasa system are found just like in "
    "Narayana dasa."
)

#: §20.2 rule 7. The first balance the book puts on a rasi dasa — Narayana and
#: Lagna Kendradi both start their first period whole.
FIRST_DASA_IS_PARTLY_SPENT = (
    "But there is an exception in the case of first dasa. Only a fraction of "
    "first dasa is left at birth. This fraction is found using the formula: "
    "(30 - SL's advancement in its sign)/30."
)


def direction_of(sree_lagna_sign: int) -> str:
    """§20.2 rule 2's direction, from whether SL's sign is odd.

    Unlike §19.2's, this rule has nothing it could be read two ways: chapter
    19 named lagna where its own rule 1 had named the dasa seed, and the two
    happened always to agree. Here the seed *is* SL, so the rule names it.
    """
    index = validate.in_range("sree_lagna_sign", sree_lagna_sign, 0, 11)
    return "forward" if RASI_IS_ODD[index] else "backward"


def first_dasa_fraction(sree_lagna_longitude: float) -> float:
    """§20.2 rule 7: how much of the first dasa is left at birth.

    ``(30 - SL's advancement in its sign) / 30``. SL at the very start of a
    rasi leaves the whole dasa; at its very end, almost none.

    :param sree_lagna_longitude: SL's sidereal longitude, from
        :func:`hora.charts.special_lagna.sree_lagna`.
    :returns: a fraction in (0, 1].
    """
    longitude = validate.longitude("sree_lagna_longitude",
                                   sree_lagna_longitude)
    return (30.0 - longitude % 30.0) / 30.0


@dataclass(frozen=True, slots=True)
class Progression:
    """The order in which rasis take their Sudasa."""

    sree_lagna: int
    sree_lagna_name: str
    direction: str
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    houses: tuple[int, ...]
    group_names: tuple[str, ...]
    #: The share of the first dasa left at birth, per §20.2 rule 7. None when
    #: SL's longitude was not supplied, in which case the caller must not
    #: assume a whole first period.
    first_dasa_fraction: float | None
    why: str


def progression(
    sree_lagna_sign: int,
    sree_lagna_longitude: float | None = None,
) -> Progression:
    """§20.2's full order of rasis, and the first dasa's balance.

    :param sree_lagna_sign: SL's rasi — the seed, per rule 1.
    :param sree_lagna_longitude: SL's longitude, for rule 7. Omitted, the
        result's ``first_dasa_fraction`` is None rather than 1.0: a caller
        with only a sign cannot know how much of the first dasa is left, and
        §20.2 says some of it is always spent.
    :raises SudasaError: when the longitude given does not lie in the sign
        given, which would make rule 7 and rule 1 disagree.
    """
    index = validate.in_range("sree_lagna_sign", sree_lagna_sign, 0, 11)
    fraction = None
    if sree_lagna_longitude is not None:
        longitude = validate.longitude("sree_lagna_longitude",
                                       sree_lagna_longitude)
        if int(longitude // 30) != index:
            raise SudasaError(
                f"sree_lagna_longitude {longitude:.4f} is in "
                f"{RASI_NAMES[int(longitude // 30)]} but sree_lagna_sign says "
                f"{RASI_NAMES[index]}")
        fraction = first_dasa_fraction(longitude)

    direction = direction_of(index)
    signs = house_signs(index, direction)
    groups = tuple(group["name"] for group in GROUPS for _ in group["houses"])
    why = (f"Sree Lagna is in {RASI_NAMES[index]}, an "
           f"{'odd' if RASI_IS_ODD[index] else 'even'} sign, so the order is "
           f"{direction}; the quadrants from {RASI_NAMES[index]} come first, "
           f"then its panapharas, then its apoklimas")
    if fraction is not None:
        why += f"; {fraction:.4f} of the first dasa is left at birth"
    return Progression(
        sree_lagna=index, sree_lagna_name=str(RASI_NAMES[index]),
        direction=direction, signs=signs,
        sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        houses=HOUSE_ORDER, group_names=groups,
        first_dasa_fraction=fraction, why=why,
    )
