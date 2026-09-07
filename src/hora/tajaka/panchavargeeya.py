"""§28.4 — pancha vargeeya bala, the strength from a group of five.

Five sources, of which §28.4.1 to §28.4.3 supply three: kshetra bala from the
rasi, uchcha bala from the distance to exaltation, and hadda bala from the
hadda. Drekkana bala, navamsa bala and the final computation are §28.4.4 to
§28.4.6 and have not arrived; `PANCHA_VARGAS_PENDING` names them and the
chapter's coverage test fails the moment one is built ahead of its page.

Two things are missing rather than merely absent, and both are refused rather
than guessed. §28.4.1 and §28.4.3 grade a planet in its own, a friend's or an
enemy's place and say nothing about a **neutral's** — see OI-153. And Table 72,
which gives the hadda lords, is cited and not printed, so no hadda can be found
from a longitude at all.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES

PANCHA_VARGEEYA_RULE = (
    "Panchavargeeya bala is found using the following procedure:")

FOOTNOTE_81 = (
    "Pancha means \"five\". Pancha vargeeya means \"from the group of "
    "five\".")

PANCHA_MEANS = "five"
PANCHA_VARGEEYA_MEANS = "from the group of five"

#: The five sources, in the order §28.4 numbers them. Three have arrived.
PANCHA_VARGAS: tuple[dict[str, object], ...] = (
    {"section": "28.4.1", "name": "Kshetra bala", "from": "the rasi",
     "maximum": 30.0, "supplied": True},
    {"section": "28.4.2", "name": "Uchcha bala",
     "from": "the distance from the exaltation point", "maximum": 20.0,
     "supplied": True},
    {"section": "28.4.3", "name": "Hadda bala", "from": "the hadda",
     "maximum": 15.0, "supplied": True},
    {"section": "28.4.4", "name": "Drekkana bala", "from": "the drekkana",
     "maximum": None, "supplied": False},
    {"section": "28.4.5", "name": "Navamsa bala", "from": "the navamsa",
     "maximum": None, "supplied": False},
)

#: The sections still to come, including the one that adds the five up.
PANCHA_VARGAS_PENDING: tuple[str, ...] = (
    "28.4.4 Drekkana Bala", "28.4.5 Navamsa Bala", "28.4.6 Final Computation")


# --------------------------------------------------------------------------
# §28.4.1 — kshetra bala
# --------------------------------------------------------------------------

KSHETRA_BALA_RULE = (
    "Kshetra bala shows the strength in rasi chart. A planet in own rasi gets "
    "30 units of Kshetra bala. A planet in a friend's rasi gets 15 units of "
    "Kshetra bala. A planet in an enemy's rasi gets 7.5 units of Kshetra "
    "bala.")

KSHETRA_BALA_UNITS: dict[str, float] = {
    "own": 30.0, "friend": 15.0, "enemy": 7.5}


# --------------------------------------------------------------------------
# §28.4.2 — uchcha bala
# --------------------------------------------------------------------------

UCHCHA_BALA_RULE = (
    "Uchcha bala shows how close a planet is from its exaltation point. A "
    "planet gets 20 units of uchcha bala if it is at its deep exaltation "
    "point (Sun: 10° Ar, Moon: 3° Ta, Mars: 28° Cp, Mercury: 15° Vi, "
    "Jupiter: 5° Cn, Venus: 27° Pi, Saturn: 20° Li). At 180° from its deep "
    "exaltation point, a planet is deeply debilitated and it gets 0 units of "
    "uchcha bala.")

UCHCHA_BALA_METHOD = (
    "We can find the longitude difference between a planet's position and its "
    "deep debilitation point and divide it by 180° to get the fraction that "
    "shows how far away it is from its debilitation point. Bu multiplying 20 "
    "units with this fraction, we get uchcha bala.")

UCHCHA_BALA_WORKED_CASE = (
    "For example, suppose Jupiter is at 8Vi30 (8°30' in Vi). So he is at "
    "158°30' from the start of the zodiac. His debilitation point is 5° in "
    "Cp, i.e. 275°0'. The difference is 275°0' – 158°30' = 116°30'. Because "
    "this is less than 180°, we don't have to subtract it from 360°. Now "
    "116°30'/180° = 0.6472. Multiply 20 with this fraction, we get 12.94. So "
    "Jupiter's uchcha bala is 12.94 (out of 20).")

UCHCHA_BALA_MAXIMUM = 20.0

#: §28.4.2's own list of deep exaltation points, transcribed from the section
#: rather than taken from chapter 3, so the two can be compared.
DEEP_EXALTATION: dict[int, float] = {
    0: 10.0,     # Sun, 10 Ar
    1: 33.0,     # Moon, 3 Ta
    2: 298.0,    # Mars, 28 Cp
    3: 165.0,    # Mercury, 15 Vi
    4: 95.0,     # Jupiter, 5 Cn
    5: 357.0,    # Venus, 27 Pi
    6: 200.0,    # Saturn, 20 Li
}

#: **Book defect.** §28.4.2 prints "Bu multiplying 20 units with this
#: fraction". One letter, and the sense is plain; recorded rather than
#: silently corrected, as the other one-letter slips are.
BU_IS_A_SLIP_FOR_BY = (
    "Section 28.4.2 reads \"Bu multiplying 20 units with this fraction\". "
    "Nothing turns on it."
)

#: **Finding.** §28.4.2's seven deep exaltation degrees are chapter 3's
#: exactly — the first place in Part 4 that reuses a table from the rest of
#: the book instead of introducing its own. Everything else here, from the
#: aspects to harsha bala's gender split, has been Tajaka's own.
THE_EXALTATION_DEGREES_ARE_CHAPTER_THREES = (
    "Section 28.4.2 lists the same seven deep exaltation points chapter 3 "
    "gives, to the degree. Part 4 has otherwise defined its own tables "
    "throughout."
)


# --------------------------------------------------------------------------
# §28.4.3 — hadda bala
# --------------------------------------------------------------------------

HADDA_RULE = (
    "Each rasi is divided into several haddas and different haddas have "
    "different lords. Hadda is similar to D-30. Table 72 can be used for "
    "finding the hadda lords of planets.")

HADDA_BALA_RULE = (
    "Hadda bala shows the strength in hadda. A planet in own hadda gets 15 "
    "units of Hadda bala. A planet in a friend's hadda gets 7.5 units of "
    "Hadda bala. A planet in an enemy's hadda gets 3.75 units of Hadda bala.")

HADDA_BALA_UNITS: dict[str, float] = {
    "own": 15.0, "friend": 7.5, "enemy": 3.75}

#: **Not supplied.** Table 72 is cited by §28.4.3 and is not on the page. No
#: hadda lord can be found from a longitude, so `hadda_bala` takes the
#: relationship to the hadda lord as an argument and there is no function to
#: derive it. §28.4.3's own comparison — "Hadda is similar to D-30" — is a
#: comparison and not a definition; D-30's lords are not borrowed for it.
TABLE_72_NOT_SUPPLIED = (
    "Section 28.4.3 says Table 72 gives the hadda lords. The table is not on "
    "the page supplied, so nothing here divides a rasi into haddas or names "
    "their lords."
)

#: **Finding.** Hadda bala is exactly half of kshetra bala at every grade —
#: 15 against 30, 7.5 against 15, 3.75 against 7.5 — so §28.4.3 is §28.4.1's
#: scale halved and not a separate one. Both also halve from grade to grade.
HADDA_IS_KSHETRA_HALVED = (
    "Own, friend's and enemy's are 30, 15 and 7.5 for kshetra bala and 15, "
    "7.5 and 3.75 for hadda bala. Each grade of hadda bala is half the "
    "corresponding grade of kshetra bala."
)

#: **Finding.** Neither §28.4.1 nor §28.4.3 gives a value for a **neutral's**
#: rasi or hadda. Chapter 3's natural relationship has three grades and the
#: compound has five, so a planet in a neutral's place is a case both
#: schemes produce and this one does not price. See OI-153; `kshetra_bala`
#: and `hadda_bala` return undecided for it rather than interpolating.
THE_NEUTRAL_GRADE_IS_NOT_PRICED = (
    "Sections 28.4.1 and 28.4.3 grade own, a friend's and an enemy's place "
    "and stop. A planet in a neutral's rasi or hadda has no value in either."
)


class PanchaVargeeyaError(validate.InputError):
    """A pancha vargeeya bala input that cannot be resolved."""


def _graded(units: dict[str, float], relation: str, what: str) -> dict:
    key = str(relation).strip().lower()
    if key in units:
        return {"relation": key, "units": units[key], "undecided": False,
                "maximum": units["own"], "reason": None}
    if key in ("neutral", "sama"):
        return {"relation": "neutral", "units": None, "undecided": True,
                "maximum": units["own"],
                "reason": THE_NEUTRAL_GRADE_IS_NOT_PRICED}
    raise PanchaVargeeyaError(
        f"{relation!r} is not a {what} grade section 28.4 prices; it gives "
        f"{', '.join(units)} and says nothing of a neutral's")


def kshetra_bala(relation: str) -> dict:
    """§28.4.1's strength from the rasi a planet occupies.

    :param relation: ``own``, ``friend`` or ``enemy``. ``neutral`` returns
        undecided — the section does not price it. See OI-153.
    """
    return {**_graded(KSHETRA_BALA_UNITS, relation, "rasi"),
            "source": "Kshetra bala", "rule": KSHETRA_BALA_RULE}


def hadda_bala(relation: str) -> dict:
    """§28.4.3's strength from the hadda a planet occupies.

    The hadda itself cannot be found here — Table 72 is not supplied — so the
    relationship to its lord is supplied by the caller.
    """
    return {**_graded(HADDA_BALA_UNITS, relation, "hadda"),
            "source": "Hadda bala", "rule": HADDA_BALA_RULE,
            "table_72": TABLE_72_NOT_SUPPLIED}


def deep_debilitation(graha: int) -> float:
    """The point 180° from a graha's deep exaltation."""
    index = validate.in_range("graha", int(graha), 0, 6)
    return (DEEP_EXALTATION[index] + 180.0) % 360.0


def uchcha_bala(graha: int, longitude: float) -> dict:
    """§28.4.2's strength from the distance to the exaltation point.

    Twenty units at the deep exaltation point, none at the deep debilitation
    point, and the fraction of 180° between them in between.
    """
    index = validate.in_range("graha", int(graha), 0, 6)
    place = validate.longitude("longitude", float(longitude))
    fallen = deep_debilitation(index)
    gap = abs(fallen - place)
    if gap > 180.0:
        gap = 360.0 - gap
    fraction = gap / 180.0
    return {
        "graha": index,
        "graha_name": str(GRAHA_NAMES[index]),
        "source": "Uchcha bala",
        "longitude": place,
        "deep_exaltation": DEEP_EXALTATION[index],
        "deep_debilitation": fallen,
        "difference": gap,
        "fraction": fraction,
        "units": UCHCHA_BALA_MAXIMUM * fraction,
        "maximum": UCHCHA_BALA_MAXIMUM,
        "undecided": False,
        "rule": UCHCHA_BALA_METHOD,
    }
