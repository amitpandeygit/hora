"""§26.3 — rasi gochara vedha, the obstruction of a good transit.

Chapter 25 said which houses from the natal Moon each graha does well in.
§26.3 adds that a graha in one of those houses can still be blocked: each
auspicious house has a partner, its **vedha sthana**, and a graha transiting
there stops the first from giving its good results.

Two things about the table are worth knowing before using it. Its auspicious
houses agree with Tables 53 to 59 exactly for six of the seven grahas and
**not for Venus**, where it adds the 8th and the 12th — see D-74, which is
recorded and not smoothed. And the vedha sthana is per-graha data, not a
formula: the same house takes a different partner for different grahas, so
nothing here is derived.
"""
from __future__ import annotations

from collections.abc import Mapping

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_NAMES, Graha
from hora.transits.gochara import good_houses, house_from_janma


class VedhaError(validate.InputError):
    """A vedha input that cannot be resolved."""


VEDHA_MEANS = "house of obstruction"

VEDHA_RULE = (
    "Even when a planet is transiting in a favorable house from natal Moon, "
    "it may be \"obstructed\" by another planet transiting in the vedha "
    "sthana (house of obstruction). In that case, the planet cannot give its "
    "good results.")

#: Table 63 — auspicious house to its vedha sthana, per transiting graha.
#: Transcribed as printed; nothing here is computed from anything else.
TABLE_63_VEDHA: dict[str, dict[int, int]] = {
    "Sun": {3: 9, 6: 12, 10: 4, 11: 5},
    "Moon": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
    "Mars": {3: 12, 6: 9, 11: 5},
    "Mercury": {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12},
    "Jupiter": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
    "Venus": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 6, 12: 3},
    "Saturn": {3: 12, 6: 9, 11: 5},
}

#: §26.3's two exceptions, and the reason it gives for them.
VEDHA_EXCEPTIONS_ARE_FATHER_AND_SON = (
    "Only exceptions are the father and son pairs: (1) Sun and Saturn do not "
    "cause vedha on each other. (2) Moon and Mercury do not cause vedha on "
    "each other.")

#: The two exempt pairs, by graha id. Unordered — neither obstructs the other.
VEDHA_EXEMPT_PAIRS: tuple[frozenset[int], ...] = (
    frozenset({int(Graha.SUN), int(Graha.SATURN)}),
    frozenset({int(Graha.MOON), int(Graha.MERCURY)}),
)

#: **Finding.** The vedha sthana is data, not a rule. Only the **Sun**'s row
#: has a pattern — every one of his vedha sthanas is the 7th from its
#: auspicious house. No other graha's row has a constant offset, and the same
#: house takes different partners for different grahas: the 3rd is blocked
#: from the 9th for the Sun and Moon, the 12th for Mars and Saturn, and the
#: 1st for Venus. So Table 63 cannot be derived and is transcribed.
ONLY_THE_SUNS_ROW_HAS_A_CONSTANT_OFFSET = (
    "The Sun's vedha sthana is the 7th from the auspicious house in all four "
    "of his rows. Every other graha's offsets differ within its own row, and "
    "one house takes different partners for different grahas."
)

#: **Finding.** Mars and Saturn have identical rows — the same three
#: auspicious houses and the same three vedha sthanas. That follows from
#: Tables 55 and 59 giving them identical good houses, which chapter 25
#: already showed.
MARS_AND_SATURN_SHARE_A_ROW = (
    "Mars and Saturn are both 3 (12), 6 (9), 11 (5). Their good houses in "
    "Tables 55 and 59 are the same three, so their vedha rows match too."
)

#: **Finding.** Vedha and murthi are the section's two brakes on a good
#: transit and it names them together — "it is important to consider vedhas
#: and murthis to understand why a planet expected to produce brilliant
#: results gives only marginal results sometimes". Both modify a verdict
#: chapter 25 made; neither makes one.
VEDHA_AND_MURTHI_ARE_BOTH_BRAKES = (
    "It is important to consider vedhas and murthis to understand why a "
    "planet expected to produce brilliant results gives only marginal "
    "results sometimes."
)

#: §26.3's worked case, and the event it reads.
VEDHA_WORKED_CASE = {
    "chart": 24, "native": "Bill Gates", "natal_moon": "Pi",
    "graha": "Mercury", "transit_rasi": "Ge", "house": 4,
    "vedha_house": 3, "vedha_rasi": "Ta",
    "date": "June 8, 2000",
    "event": "the company of Mr. Gates received a legal setback",
}


def _graha_name(graha: int | str) -> str:
    if isinstance(graha, str):
        if graha not in TABLE_63_VEDHA:
            raise VedhaError(
                f"{graha!r} has no row in Table 63; the seven are "
                f"{', '.join(TABLE_63_VEDHA)}")
        return graha
    index = validate.in_range("graha", int(graha), 0, 6)
    return str(GRAHA_NAMES[index])


def vedha_sthana(graha: int | str, house: int) -> dict:
    """The vedha sthana for one graha's transit of one house.

    :returns: the obstructing house, or ``None`` with a reason when the house
        is not one Table 63 calls auspicious for that graha — there is no
        vedha to obstruct a transit that was not good to begin with.
    """
    name = _graha_name(graha)
    index = validate.in_range("house", int(house), 1, 12)
    row = TABLE_63_VEDHA[name]
    disputed = index in row and index not in good_houses(
        int(getattr(Graha, name.upper())))
    return {
        "graha": name,
        "house": index,
        "auspicious": index in row,
        "vedha_house": row.get(index),
        "reason": (
            None if index in row else
            f"Table 63 does not list the {index} as auspicious for {name}, "
            f"so §26.3's obstruction does not arise"),
        "disputed_by_chapter_25": disputed,
        "dispute": (
            None if not disputed else
            f"Table 63 calls the {index} auspicious for {name} and chapter "
            f"25's own table marks it Bad — see D-74"),
    }


def causes_vedha(obstructing: int, transiting: int) -> dict:
    """Whether one graha can obstruct another at all, before positions.

    §26.3's only exceptions are the two father-and-son pairs.
    """
    first = validate.in_range("obstructing", int(obstructing), 0, 6)
    second = validate.in_range("transiting", int(transiting), 0, 6)
    exempt = frozenset({first, second}) in VEDHA_EXEMPT_PAIRS
    return {
        "obstructing": str(GRAHA_NAMES[first]),
        "transiting": str(GRAHA_NAMES[second]),
        "causes_vedha": not exempt and first != second,
        "exempt": exempt,
        "reason": (
            VEDHA_EXCEPTIONS_ARE_FATHER_AND_SON if exempt else
            "a planet does not obstruct itself" if first == second else None),
    }


def vedha(graha: int, natal_moon_longitude: float,
          transit_longitudes: Mapping[int, float]) -> dict:
    """Is `graha`'s transit obstructed, for this nativity and this moment?

    :param graha: the transiting graha being judged, 0 to 6.
    :param natal_moon_longitude: the native's natal Moon.
    :param transit_longitudes: graha id to its transiting longitude. The
        judged graha's own entry is required; the others decide the vedha.
    """
    index = validate.in_range("graha", int(graha), 0, 6)
    if index not in transit_longitudes:
        raise VedhaError(
            f"a transiting longitude is needed for "
            f"{GRAHA_NAMES[index]}, the graha being judged")

    placed = house_from_janma(natal_moon_longitude,
                             transit_longitudes[index])
    sthana = vedha_sthana(index, placed["house"])
    if not sthana["auspicious"]:
        return {"graha": str(GRAHA_NAMES[index]), "house": placed["house"],
                "auspicious": False, "obstructed": None,
                "reason": sthana["reason"], "obstructors": [],
                "exempt_in_the_vedha_sthana": []}

    vedha_house = int(sthana["vedha_house"])
    janma = placed["janma_rasi"]
    vedha_sign = (janma + vedha_house - 1) % 12

    obstructors: list[str] = []
    exempt: list[str] = []
    for other, longitude in transit_longitudes.items():
        other = int(other)
        if other == index or other > 6:
            continue
        if int(validate.longitude("longitude", float(longitude)) // 30) != (
                vedha_sign):
            continue
        verdict = causes_vedha(other, index)
        (obstructors if verdict["causes_vedha"] else exempt).append(
            str(GRAHA_NAMES[other]))

    return {
        "graha": str(GRAHA_NAMES[index]),
        "house": placed["house"],
        "transit_rasi": placed["transit_rasi_name"],
        "auspicious": True,
        "vedha_house": vedha_house,
        "vedha_rasi": str(RASI_NAMES[vedha_sign]),
        "obstructors": obstructors,
        "exempt_in_the_vedha_sthana": exempt,
        "obstructed": bool(obstructors),
        "results": (
            "the planet cannot give its good results" if obstructors
            else "no planet occupies the vedha sthana, so the good transit "
                 "stands"),
        "disputed_by_chapter_25": sthana["disputed_by_chapter_25"],
        "dispute": sthana["dispute"],
    }
