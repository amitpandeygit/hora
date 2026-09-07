"""§28.1 — muntha, the progressed lagna of a Tajaka chart.

The rule is one line: progress the **natal** lagna by one rasi for every year
of life. It is arithmetic on rasis and needs no ephemeris — the annual chart
supplies only the lagna the muntha is then read against.

Two things the section says and does not settle are carried as they stand. It
calls muntha "as important a reference point in an annual chart as lagna" and
defers the reason to the Sudarsana Chakra Dasa chapter; and it records that
"some people" progress the lagna by 2°30' a month for monthly charts while
"this author takes a different stand", without saying what that stand is. See
OI-152; no monthly muntha is computed.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import RASI_NAMES

MUNTHA_RULE = (
    "Muntha is a concept specific to Tajaka charts. Progress lagna in the "
    "natal chart at the rate of one rasi per year to get muntha in an annual "
    "chart.")

MUNTHA_WORKED_CASE = (
    "Suppose someone finishes 31 years and starts the 32nd year on a given "
    "date. Suppose we are casting the annual chart of the 32nd year. Suppose "
    "the natal chart has lagna in Sc. Then muntha in the annual chart will be "
    "the 32nd house from Sc, i.e. the 8th house from Sc (after expunging "
    "multiples of 12 from 32). So muntha is in Ge.")

MUNTHA_IS_AS_IMPORTANT_AS_LAGNA = (
    "Muntha is very important in Tajaka charts. Muntha is as important a "
    "reference point in an annual chart as lagna. The reason may be obvious "
    "in the chapter on \"Sudarsana Chakra Dasa\".")

MONTHLY_MUNTHA_IS_DISPUTED = (
    "Some people find muntha in monthly charts by progressing natal lagna by "
    "2°30' per month. This author takes a different stand and the readers may "
    "be able to appreciate this after reading the same chapter.")

PLANETS_IN_MUNTHA = (
    "Look at the planets in muntha. They tell us the nature of events in the "
    "year or month. For example, Jupiter in muntha may give good results, "
    "happiness from children and knowledge. Saturn in muntha may make one "
    "sluggish, unhealthy, frustrated and sorrowful. Of course, the strength "
    "of the planets influencing muntha also matters. For example, an "
    "afflicted and weak Jupiter in muntha may give loss of position, bad name "
    "and scandals.")

#: The two grahas §28.1 illustrates with, and what each gives from muntha.
MUNTHA_OCCUPANT_EXAMPLES: tuple[dict[str, str], ...] = (
    {"graha": "Jupiter",
     "gives": "good results, happiness from children and knowledge"},
    {"graha": "Saturn",
     "gives": "sluggishness, ill-health, frustration and sorrow"},
    {"graha": "Jupiter, afflicted and weak",
     "gives": "loss of position, bad name and scandals"},
)

MUNTHA_IN_HOUSES = (
    "Position of muntha in various houses with respect to lagna in the annual "
    "chart also tells us the nature of events in a year. Situation of muntha "
    "in the 9th, 10th and 11th houses is excellent. It gives prosperity, "
    "status and gains respectively. Situation of muntha in the 1st, 2nd, 3rd "
    "and 5th houses is also good. It gives health, wealth, success and fame "
    "respectively. Situation of muntha in the 6th, 8th and 12th houses is "
    "bad. It gives illness, troubles and expenditures respectively. Situation "
    "of muntha in the 4th house gives disputes and loss of position. "
    "Situation of muntha in the 7th house also gives troubles in marriage and "
    "many hardships.")

#: §28.1's reading of muntha by house from the annual chart's lagna. Every
#: house is covered; the grades are the section's own words.
MUNTHA_HOUSE_RESULTS: dict[int, dict[str, str]] = {
    1: {"grade": "good", "gives": "health"},
    2: {"grade": "good", "gives": "wealth"},
    3: {"grade": "good", "gives": "success"},
    4: {"grade": "bad", "gives": "disputes and loss of position"},
    5: {"grade": "good", "gives": "fame"},
    6: {"grade": "bad", "gives": "illness"},
    7: {"grade": "bad", "gives": "troubles in marriage and many hardships"},
    8: {"grade": "bad", "gives": "troubles"},
    9: {"grade": "excellent", "gives": "prosperity"},
    10: {"grade": "excellent", "gives": "status"},
    11: {"grade": "excellent", "gives": "gains"},
    12: {"grade": "bad", "gives": "expenditures"},
}

#: **Finding.** The section's list is not the house-category scheme, though
#: it looks like it. The **trikonas** (1, 5, 9) are all good or excellent and
#: the **dusthanas** (6, 8, 12) are all bad, exactly as chapter 7 would have
#: it. But the **kendras** split — the 1st good and the 10th excellent while
#: the 4th and 7th are bad — and the **upachayas** split too, the 3rd good and
#: the 10th and 11th excellent while the 6th is bad. So four of the twelve
#: cannot be predicted from the category and have to be read from this list.
THE_MUNTHA_HOUSES_ARE_NOT_THE_HOUSE_CATEGORIES = (
    "Muntha's trikonas are all favourable and its dusthanas all bad, as the "
    "categories would have it. Its kendras and upachayas each split, so the "
    "4th, 6th and 7th cannot be read off the category."
)

#: **Finding.** Muntha returns to the natal lagna every twelve years — one
#: rasi a year through twelve rasis — so the first, thirteenth, twenty-fifth
#: and thirty-seventh years all carry it in the same rasi. In the first year
#: it **is** the natal lagna.
MUNTHA_REPEATS_ON_A_TWELVE_YEAR_CYCLE = (
    "One rasi a year through twelve rasis brings muntha back to the natal "
    "lagna in the thirteenth year, and it sits on the natal lagna in the "
    "first."
)

#: **Finding.** The disputed monthly rate is not arbitrary: 2°30' a month
#: over twelve months is thirty degrees, which is §28.1's own one rasi a
#: year. So "some people" are interpolating the section's own rule linearly,
#: and the author rejects that interpolation without giving another. Note
#: also that the same 2°30' is §27.4's shashti-hora arc — but that is an arc
#: of the **Sun** and this would be one of the **lagna**, so the two are
#: unrelated beyond the number.
THE_DISPUTED_RATE_IS_THE_ANNUAL_RATE_INTERPOLATED = (
    "Two degrees thirty minutes a month is thirty degrees a year, which is "
    "section 28.1's one rasi a year. The monthly method some people use is "
    "the annual rule spread evenly, and the author declines it."
)


class MunthaError(validate.InputError):
    """A muntha input that cannot be resolved."""


def muntha_house_from_lagna(year: int) -> int:
    """Which house from the **natal** lagna muntha occupies in `year`.

    §28.1 counts inclusively: the 32nd year puts muntha in the 32nd house
    from the natal lagna, which is the 8th "after expunging multiples of 12".
    """
    index = validate.in_range("year", int(year), 1, 200)
    return (index - 1) % 12 + 1


def muntha_rasi(natal_lagna_rasi: int, year: int) -> dict:
    """Muntha's rasi in the annual chart of the native's `year`-th year.

    :param natal_lagna_rasi: 0 = Aries.
    :param year: 1 is the year that begins at birth, so muntha sits on the
        natal lagna in it.
    """
    lagna = validate.in_range("natal_lagna_rasi", int(natal_lagna_rasi), 0, 11)
    house = muntha_house_from_lagna(year)
    rasi = (lagna + house - 1) % 12
    return {
        "year": int(year),
        "natal_lagna_rasi": lagna,
        "natal_lagna_rasi_name": str(RASI_NAMES[lagna]),
        "house_from_natal_lagna": house,
        "rasi": rasi,
        "rasi_name": str(RASI_NAMES[rasi]),
        "rule": MUNTHA_RULE,
    }


def muntha(natal_lagna_rasi: int, year: int, annual_lagna_rasi: int,
           occupants: dict[int, int] | None = None) -> dict:
    """Muntha for one annual chart, with its house and the section's reading.

    :param annual_lagna_rasi: the lagna of the annual chart, which is what
        §28.1 reads muntha's house from.
    :param occupants: graha id to rasi in the annual chart. Given, the grahas
        standing in muntha are reported; omitted, that list is ``None`` rather
        than empty, because "no graha there" and "not asked" differ.
    """
    where = muntha_rasi(natal_lagna_rasi, year)
    annual = validate.in_range("annual_lagna_rasi", int(annual_lagna_rasi),
                               0, 11)
    house = (where["rasi"] - annual) % 12 + 1
    result = MUNTHA_HOUSE_RESULTS[house]
    standing = (None if occupants is None else
                tuple(sorted(graha for graha, rasi in occupants.items()
                             if int(rasi) == where["rasi"])))
    return {
        **where,
        "annual_lagna_rasi": annual,
        "annual_lagna_rasi_name": str(RASI_NAMES[annual]),
        "house_from_annual_lagna": house,
        "grade": result["grade"],
        "gives": result["gives"],
        "grahas_in_muntha": standing,
        "occupant_rule": PLANETS_IN_MUNTHA,
        "strength_note": (
            "Section 28.1 says the strength of the planets influencing "
            "muntha also matters and gives no measure for it; chapter 15's "
            "simple rules are not built, so no occupant is graded here."),
    }
