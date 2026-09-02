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


#: §20.2 rule 7's own worked conversion, which fixes the units of the answer:
#: 1.1766 years is "1 year 2 months 3 days 14 hours". That is twelve months of
#: thirty days — §18.6's measure, where a day is one degree of the Sun's
#: motion — and not a calendar year.
FIRST_DASA_BALANCE_EXAMPLE = (
    "First dasa of Cp is of 2 years and 0.5883 of it is 1.1766 years, i.e., 1 "
    "year 2 months 3 days 14 hours."
)


def years_to_dasa_ymdh(years: float) -> tuple[int, int, int, int]:
    """A dasa length in years as years, months, days and whole hours.

    §18.6's units throughout: twelve months to a year, thirty days to a month,
    a day being one degree of the Sun's motion. Example 77 turns 1.1766 years
    into "1 year 2 months 3 days 14 hours" this way.
    """
    total = validate.non_negative("years", years)
    whole_years = int(total)
    months = (total - whole_years) * 12.0
    whole_months = int(months)
    days = (months - whole_months) * 30.0
    whole_days = int(days)
    hours = round((days - whole_days) * 24.0)
    if hours == 24:                                # carry, at a day boundary
        whole_days, hours = whole_days + 1, 0
    return whole_years, whole_months, whole_days, hours


# --------------------------------------------------------------------------
# §20.3 Interpretation
# --------------------------------------------------------------------------

#: §20.3's rules 1 and 2. The same three tests are run twice, against a
#: different special lagna each time, and only the result named differs.
SPECIAL_LAGNA_DASA_RULES: tuple[dict, ...] = (
    {"lagna": "HL", "name": "Hora Lagna", "gives": "financial prosperity"},
    {"lagna": "GL", "name": "Ghati Lagna", "gives": "power and authority"},
)

#: Rule 1's base, which says which dasa signs qualify at all.
PROSPERITY_RULE = (
    "Dasas of HL, 7th from HL and the signs aspecting HL bring financial "
    "prosperity."
)

#: Rule 1's two reinforcements. Each is a separate way of reaching the same
#: result, and the illustration counts them.
PROSPERITY_REINFORCEMENTS = (
    "If the lord of the dasa sign occupies or aspects HL, it will improve the "
    "chance of financial prosperity. Similarly, if the lord of HL occupies or "
    "aspects dasa sign, it will also improve the chances of financial "
    "prosperity."
)

#: §20.3's own worked case, and the answer key for :func:`prosperity_ways`.
#: It is the only place the book counts reinforcements rather than naming
#: them, so "triply" is what fixes the arithmetic.
PROSPERITY_ILLUSTRATION = (
    "For example, say HL is in Aries, Mars is in Leo and Sun is in Scorpio. "
    "Then (a) Leo aspects HL, (b) lord of Leo aspects HL and (c) lord of HL "
    "occupies Leo. So Leo dasa is triply likely to bring financial "
    "prosperity."
)

#: Rule 2, which carries rule 1 over to GL unchanged but for the result.
GL_GIVES_POWER_INSTEAD = (
    "Same thing holds for GL and the prescribed results are power and "
    "authority instead of financial prosperity."
)

#: §20.3 rules 3 and 4, read from the arudha lagna. The upachayas were
#: already recorded as showing growth of what their reference signifies, with
#: the arudha lagna as the example; rules 3 and 4 put that on a dasa and add
#: the 8th and 12th as its opposite.
STATUS_FROM_ARUDHA_LAGNA: tuple[dict, ...] = (
    {"houses": (3, 6, 10, 11), "gives": "growth of status",
     "text": ("Upachayas from any house stand for the growth of matters "
              "signified by that house. AL stands for one's status. So dasas "
              "of upachayas from AL bring growth of status.")},
    {"houses": (11,), "gives": "growth of status, particularly favorable",
     "text": "Dasa of the 11th house from AL is particularly favorable."},
    {"houses": (8, 12), "gives": "setbacks to one's status",
     "text": ("The 8th and 12th houses from AL bring setbacks to one's "
              "status. Their dasas can be unfavorable.")},
)


def prosperity_ways(
    dasa_sign: int,
    special_lagna_sign: int,
    signs: dict[int, int],
    *,
    dasa_lord: int | None = None,
    lagna_lord: int | None = None,
) -> tuple[dict, ...]:
    """Every way §20.3 rule 1 gives a dasa sign of reaching its result.

    Three are possible and the illustration shows all three at once. The
    result is a tuple so a caller can count it — "Leo dasa is **triply**
    likely" is the only arithmetic the section does.

    :param dasa_sign: the rasi whose dasa is running.
    :param special_lagna_sign: HL's rasi for financial prosperity, GL's for
        power and authority. Rule 2 makes them the same test.
    :param signs: rasi per graha, for "occupies or aspects".
    :param dasa_lord: the dasa sign's lord, for Scorpio and Aquarius. Left
        None the primary lord is used — Example 76 showed the book means the
        primary lord by "the lord" outside the rules that send it to §15.5.1.
    :param lagna_lord: likewise for the special lagna's sign.
    :returns: dicts with ``rule`` and ``why``, in the order §20.3 gives them.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    dasa = validate.in_range("dasa_sign", dasa_sign, 0, 11)
    target = validate.in_range("special_lagna_sign", special_lagna_sign, 0, 11)
    ways: list[dict] = []

    if dasa == target:
        ways.append({"rule": "is the special lagna's sign",
                     "why": f"{RASI_NAMES[dasa]} holds it"})
    elif dasa == (target + 6) % 12:
        ways.append({"rule": "is the 7th from it",
                     "why": f"{RASI_NAMES[dasa]} is the 7th from "
                            f"{RASI_NAMES[target]}"})
    elif target in rasi_drishti(dasa):
        ways.append({"rule": "aspects it",
                     "why": f"{RASI_NAMES[dasa]} aspects "
                            f"{RASI_NAMES[target]}"})

    ruler = int(RASI_LORD[dasa]) if dasa_lord is None else int(dasa_lord)
    if ruler in signs and (signs[ruler] == target
                           or target in rasi_drishti(signs[ruler])):
        verb = "occupies" if signs[ruler] == target else "aspects"
        ways.append({"rule": "its lord occupies or aspects the special lagna",
                     "why": f"{GRAHA_NAMES[ruler]}, lord of "
                            f"{RASI_NAMES[dasa]}, {verb} "
                            f"{RASI_NAMES[target]} from "
                            f"{RASI_NAMES[signs[ruler]]}"})

    other = int(RASI_LORD[target]) if lagna_lord is None else int(lagna_lord)
    if other in signs and (signs[other] == dasa
                           or dasa in rasi_drishti(signs[other])):
        verb = "occupies" if signs[other] == dasa else "aspects"
        ways.append({"rule": "the special lagna's lord occupies or aspects it",
                     "why": f"{GRAHA_NAMES[other]}, lord of "
                            f"{RASI_NAMES[target]}, {verb} "
                            f"{RASI_NAMES[dasa]} from "
                            f"{RASI_NAMES[signs[other]]}"})
    return tuple(ways)


def status_from_arudha_lagna(dasa_sign: int, arudha_lagna_sign: int) -> dict:
    """§20.3 rules 3 and 4 — what a dasa says about status, read from AL.

    :returns: the house the dasa sign holds from AL, and the readings that
        reach it. ``readings`` is empty for a house §20.3 does not name, which
        is most of them — it speaks for six of the twelve.
    """
    dasa = validate.in_range("dasa_sign", dasa_sign, 0, 11)
    arudha = validate.in_range("arudha_lagna_sign", arudha_lagna_sign, 0, 11)
    house = (dasa - arudha) % 12 + 1
    return {
        "dasa_sign": dasa,
        "dasa_sign_name": str(RASI_NAMES[dasa]),
        "house_from_al": house,
        "readings": tuple(r["gives"] for r in STATUS_FROM_ARUDHA_LAGNA
                          if house in r["houses"]),
    }
