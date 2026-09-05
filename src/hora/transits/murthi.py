"""§26.2 — murthis, the form a planet takes for a whole rasi transit.

The rule fixes one verdict per (planet, rasi transit, nativity): find the
moment the planet enters the rasi, see which house the **transit Moon** then
occupies from the **natal Moon**, and read Table 62. That verdict then holds
for the entire stay in the rasi, however long it runs.

Two things follow from the shape of the rule and are stated here because the
section does not spell them out. It is a **modifier**, not a verdict — §26.2's
own words are that a favourable transit "may not give his full results" under
a bad murthi — so nothing here overrides a chapter 25 reading. And it is
**per nativity**: the same ingress gives different murthis to different
people, which is what the section's two suppositions demonstrate.
"""
from __future__ import annotations

from collections.abc import Callable

from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.panchanga.solver import scan_for_crossing
from hora.transits.gochara import house_from_janma


class MurthiError(validate.InputError):
    """A murthi input that cannot be resolved."""


MURTHI_RULE = (
    "To judge the results given by a planet during its transit in a "
    "particular rasi, find exactly when the planet enters the rasi. Find the "
    "house occupied by transit Moon at that time with respect to his own "
    "(Moon's) natal position. Based on the house, we say that the planet is "
    "a golden or silver or copper or iron form during its transit in the "
    "rasi.")

MURTHI_MEANS = "form or idol"

#: Table 62, in the printed order: houses, the murthi's name, its meaning and
#: its result.
TABLE_62_MURTHIS: tuple[dict[str, object], ...] = (
    {"houses": (1, 6, 11), "murthi": "Swarna", "meaning": "Golden form",
     "results": "Highly favorable", "rank": 1, "favourable": True},
    {"houses": (2, 5, 9), "murthi": "Rajata", "meaning": "Silver form",
     "results": "Favorable", "rank": 2, "favourable": True},
    {"houses": (3, 7, 10), "murthi": "Taamra", "meaning": "Copper form",
     "results": "Unfavorable", "rank": 3, "favourable": False},
    {"houses": (4, 8, 12), "murthi": "Loha", "meaning": "Iron form",
     "results": "Highly unfavorable", "rank": 4, "favourable": False},
)

def _houses(row: dict[str, object]) -> tuple[int, ...]:
    houses = row["houses"]
    assert isinstance(houses, tuple)
    return houses


#: House to its row in Table 62, built from the table rather than typed twice.
MURTHI_OF_HOUSE: dict[int, str] = {
    house: str(row["murthi"])
    for row in TABLE_62_MURTHIS
    for house in _houses(row)
}

#: **Finding.** Table 62's worst group is exactly the **moksha trikona** —
#: the 4th, 8th and 12th, the three houses §7's own classification groups
#: together. None of the other three rows is a trikona of any kind, so this is
#: the one row with a name already in the book.
LOHA_IS_THE_MOKSHA_TRIKONA = (
    "The iron form's houses are the 4th, 8th and 12th, which are the moksha "
    "trikona. The other three murthis do not line up with any trine."
)

#: **Finding.** Every quadrant but the lagna is unfavourable: the 4th is Loha,
#: the 7th and 10th are Taamra, and only the 1st is Swarna. So the strongest
#: houses of a chart are the weakest positions for the Moon to be caught in
#: when a planet changes rasi.
EVERY_QUADRANT_BUT_THE_FIRST_IS_UNFAVOURABLE = (
    "The 1st house gives the golden form; the 4th gives iron and the 7th and "
    "10th copper. Of the four quadrants only the lagna is favourable here."
)

#: **Finding.** The murthi is a **modifier on an existing verdict**, not a
#: verdict of its own. §26.2 says a bad murthi means a favourable transit "may
#: not give his full results" and an unfavourable one "will make the native
#: suffer much" — so it scales what chapter 25 already said rather than
#: replacing it. `murthi` therefore returns no favourable/unfavourable call
#: about the transit itself.
THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE = (
    "Even if it is a favorable transit otherwise, Mercury may not give his "
    "full results. If it is an unfavorable transit otherwise, then Mercury "
    "will make the native suffer much."
)

#: **Finding.** One ingress, many murthis. The Moon's position at the moment
#: of entry is the same for everyone; the *house* it makes is counted from
#: each native's own natal Moon, so a single rasi transit is golden for one
#: person and iron for another. §26.2 shows exactly this with two suppositions
#: on one ingress.
ONE_INGRESS_GIVES_A_DIFFERENT_MURTHI_TO_EACH_NATIVE = (
    "Mercury's Gemini entry of 26 May 2000 is one moment with the Moon at 10 "
    "29 Aquarius. A native with the Moon in Aquarius gets Swarna from the "
    "1st house; Bill Gates, with the Moon in Pisces, gets Loha from the 12th."
)

#: §26.2's worked transit, and the two natives it reads it for.
MERCURY_IN_GEMINI_2000 = {
    "graha": "Mercury", "rasi": "Ge",
    "entered": "May 26, 2000, 3:06 pm (IST)",
    "window": "May 26, 2000 - Aug 3, 2000",
    "moon_at_entry": "10 29 Aquarius",
}
MURTHI_WORKED_CASES: tuple[dict[str, object], ...] = (
    {"natal_moon": "Aq", "house": 1, "murthi": "Swarna",
     "note": "will give full results"},
    {"natal_moon": "Pi", "house": 12, "murthi": "Loha",
     "note": "Bill Gates, whose chart was considered earlier",
     "chart": 24},
)


def murthi_of_house(house: int) -> dict:
    """Table 62's row for a house, 1 to 12."""
    index = validate.in_range("house", int(house), 1, 12)
    for row in TABLE_62_MURTHIS:
        if index in _houses(row):
            return {"house": index, **row}
    raise MurthiError(f"no murthi for house {index}")   # pragma: no cover


def murthi(natal_moon_longitude: float,
           moon_longitude_at_entry: float) -> dict:
    """The murthi a planet takes, from the two Moon positions §26.2 needs.

    :param natal_moon_longitude: the native's natal Moon.
    :param moon_longitude_at_entry: the transit Moon **at the moment the
        planet entered the rasi**, not at the moment being judged.
    :returns: the house, Table 62's row for it, and the scope and limits of
        the verdict. No favourable/unfavourable call is made about the
        transit itself — see
        `THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE`.
    """
    counted = house_from_janma(natal_moon_longitude, moon_longitude_at_entry)
    row = murthi_of_house(counted["house"])
    return {
        "house": counted["house"],
        "natal_moon_rasi": counted["janma_rasi_name"],
        "moon_rasi_at_entry": counted["transit_rasi_name"],
        "murthi": row["murthi"],
        "meaning": row["meaning"],
        "results": row["results"],
        "rank": row["rank"],
        "favourable": row["favourable"],
        "holds_for": (
            "the planet's whole transit of that rasi — the murthi is fixed "
            "at the moment of entry and does not change while it stays"),
        "modifies": THE_MURTHI_SCALES_A_VERDICT_IT_DOES_NOT_MAKE_ONE,
    }


def rasi_ingress(longitude_at: Callable[[float], float], sign: int,
                 jd_from: float, jd_to: float, *,
                 step: float = 0.25) -> dict:
    """When a graha next enters `sign`, within a window.

    :param longitude_at: julian day -> that graha's sidereal longitude. Given
        as a callable so this stays independent of how positions are sourced,
        the way `solve_angle_crossing` is.
    :param sign: the rasi being entered, 0 = Aries.
    :returns: the julian day of the crossing, or ``None`` with a reason. A
        **retrograde** entry is not found: the scan brackets forward crossings
        only, so a graha backing into a rasi is reported as not found rather
        than silently missed.
    """
    index = validate.in_range("sign", int(sign), 0, 11)
    if jd_to <= jd_from:
        raise MurthiError("the window must end after it starts")
    found = scan_for_crossing(longitude_at, index * 30.0, jd_from, jd_to,
                              step=step)
    return {
        "sign": index,
        "rasi": str(RASI_NAMES[index]),
        "jd": found,
        "found": found is not None,
        "searched": {"from": jd_from, "to": jd_to, "step_days": step},
        "reason": (
            None if found is not None else
            "no forward crossing of the rasi boundary in this window; a "
            "graha entering the rasi in retrograde motion is not detected"),
    }
