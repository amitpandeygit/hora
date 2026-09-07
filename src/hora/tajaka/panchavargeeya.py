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
    {"section": "28.4.4", "name": "Drekkana bala",
     "from": "the drekkana chart", "maximum": 10.0, "supplied": True},
    {"section": "28.4.5", "name": "Navamsa bala", "from": "the navamsa",
     "maximum": None, "supplied": False},
)

#: The sections still to come, including the one that adds the five up.
PANCHA_VARGAS_PENDING: tuple[str, ...] = (
    "28.4.5 Navamsa Bala", "28.4.6 Final Computation")


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

#: Table 72 as printed: for each rasi, the five haddas as (end degree, lord),
#: the first beginning at zero. Every row runs 0 to 30 and the whole table is
#: 360 degrees, both of which are asserted rather than trusted.
TABLE_72_HADDA_LORDS: dict[int, tuple[tuple[float, int], ...]] = {
    0:  ((6.0, 4), (12.0, 5), (20.0, 3), (25.0, 2), (30.0, 6)),    # Aries
    1:  ((8.0, 5), (14.0, 3), (22.0, 4), (27.0, 6), (30.0, 2)),    # Taurus
    2:  ((6.0, 3), (12.0, 5), (17.0, 4), (24.0, 2), (30.0, 6)),    # Gemini
    3:  ((7.0, 2), (13.0, 5), (19.0, 3), (26.0, 4), (30.0, 6)),    # Cancer
    4:  ((6.0, 4), (11.0, 5), (18.0, 6), (24.0, 3), (30.0, 2)),    # Leo
    5:  ((7.0, 3), (17.0, 5), (21.0, 4), (28.0, 2), (30.0, 6)),    # Virgo
    6:  ((6.0, 6), (14.0, 3), (21.0, 4), (28.0, 5), (30.0, 2)),    # Libra
    7:  ((7.0, 2), (11.0, 5), (19.0, 3), (24.0, 4), (30.0, 6)),    # Scorpio
    8:  ((12.0, 4), (17.0, 5), (21.0, 3), (26.0, 2), (30.0, 6)),   # Sagittarius
    9:  ((7.0, 3), (14.0, 4), (22.0, 5), (26.0, 6), (30.0, 2)),    # Capricorn
    10: ((7.0, 3), (13.0, 5), (20.0, 4), (25.0, 2), (30.0, 6)),    # Aquarius
    11: ((12.0, 5), (16.0, 4), (19.0, 3), (28.0, 2), (30.0, 6)),   # Pisces
}

TABLE_72_TITLE = "Hadda Lords"

#: The five grahas Table 72 uses. The luminaries are not among them.
HADDA_LORDS: tuple[int, ...] = (2, 3, 4, 5, 6)

#: **Finding.** Table 72 never gives a hadda to the **Sun or the Moon**, so
#: neither can ever stand in its own hadda and hadda bala's 15 units are out
#: of their reach. The most either can score is a friend's 7.5. That is the
#: same shape as §28.3's ceiling on the Sun, Venus and Saturn — a structural
#: limit the section does not mention.
THE_LUMINARIES_CAN_NEVER_HOLD_THEIR_OWN_HADDA = (
    "Table 72's sixty haddas are shared among Mars, Mercury, Jupiter, Venus "
    "and Saturn. The Sun and the Moon lord none of them, so hadda bala's own "
    "grade is unreachable for both."
)

#: **Finding.** The five lords do not share the zodiac evenly. Summing the
#: widths of Table 72 as printed gives **Venus 83°, Jupiter 78°, Mercury 76°,
#: Mars 67° and Saturn 56°**. Those four of five differ by a degree from the
#: figures usually quoted for the Egyptian bounds, which is recorded for
#: checking against JHora rather than corrected. See OI-154.
THE_HADDA_TOTALS_ARE_UNEVEN = (
    "Table 72 gives Venus 83 degrees of the zodiac, Jupiter 78, Mercury 76, "
    "Mars 67 and Saturn 56. Every rasi row runs 0 to 30 and the whole table "
    "closes on 360."
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

    :param relation: the planet's relationship to the **hadda lord**, which
        `hadda_lord` finds from a longitude.
    """
    return {**_graded(HADDA_BALA_UNITS, relation, "hadda"),
            "source": "Hadda bala", "rule": HADDA_BALA_RULE}


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


def hadda_lord(longitude: float) -> dict:
    """The hadda a longitude falls in, and its lord, from Table 72."""
    place = validate.longitude("longitude", float(longitude))
    rasi = int(place // 30)
    within = place - rasi * 30.0
    start = 0.0
    for end, lord in TABLE_72_HADDA_LORDS[rasi]:
        if within < end:
            return {
                "longitude": place,
                "rasi": rasi,
                "degrees_in_rasi": within,
                "hadda_from": start,
                "hadda_to": end,
                "lord": lord,
                "lord_name": str(GRAHA_NAMES[lord]),
                "rule": HADDA_RULE,
            }
        start = end
    raise PanchaVargeeyaError(                      # pragma: no cover
        f"{place} falls in no hadda of Table 72, which cannot happen")


# --------------------------------------------------------------------------
# §28.4.4 — drekkana bala
# --------------------------------------------------------------------------

DREKKANA_BALA_RULE = (
    "Drekkana bala shows the strength in drekkana chart (D-3). A planet in "
    "own rasi in D-3 gets 10 units of Drekkana bala. A planet in a friend's "
    "rasi in D-3 gets 5 units of Drekkana bala. A planet in an enemy's rasi "
    "in D-3 gets 2.5 units of Drekkana bala.")

DREKKANA_BALA_UNITS: dict[str, float] = {
    "own": 10.0, "friend": 5.0, "enemy": 2.5}

#: **Finding.** The three place balas are one scale divided by one, two and
#: three: kshetra 30, hadda 15, drekkana 10. Each also halves from own to
#: friend's to enemy's, so the whole family is 30 over n, then halved twice.
#: Uchcha bala's 20 is outside the series, and it is the one source that does
#: not read a relationship.
THE_PLACE_BALAS_ARE_THIRTY_OVER_N = (
    "Kshetra bala's own grade is 30, hadda bala's 15 and drekkana bala's 10 "
    "— thirty divided by one, two and three. Uchcha bala's 20 belongs to no "
    "such series, and it is the only source of the five that does not grade "
    "a relationship."
)

#: **Finding.** All three place balas leave a **neutral** unpriced, so the gap
#: OI-153 records is not a slip in one section but the shape of the whole
#: family. Three sections state three grades each and none states a fourth.
THE_NEUTRAL_GAP_REPEATS_IN_ALL_THREE_PLACE_BALAS = (
    "Kshetra, hadda and drekkana bala each grade own, a friend's and an "
    "enemy's place. None of the three prices a neutral's."
)


def drekkana_bala(relation: str) -> dict:
    """§28.4.4's strength from the rasi a planet occupies in D-3.

    :param relation: ``own``, ``friend`` or ``enemy``, judged in the drekkana
        chart. ``neutral`` returns undecided — see OI-153.
    """
    return {**_graded(DREKKANA_BALA_UNITS, relation, "drekkana"),
            "source": "Drekkana bala", "rule": DREKKANA_BALA_RULE}
