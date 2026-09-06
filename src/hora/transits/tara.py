"""§26.4.1 — taras, the nakshatra a transit makes from the natal Moon's.

§26.1 promised a nakshatra thread and this is it. Count constellations from
the natal Moon's to the one a transiting graha occupies, inclusively, and
Table 64 grades the count. Unlike Table 63 the grading **is** a formula: the
nine taras repeat every nine nakshatras, so the count only matters modulo 9.

Janma Tara is graded **mixed**, not good and not bad, so a tally of good and
bad taras does not account for every graha and `tara_bala` says so rather than
forcing the first tara onto one side.
"""
from __future__ import annotations

from collections.abc import Mapping

from hora.core import validate
from hora.core.const import GRAHA_NAMES, NAKSHATRA_NAMES

#: One nakshatra, in degrees.
NAKSHATRA_SPAN = 360.0 / 27.0

#: Nine taras to a cycle, and 27 nakshatras — three of each.
TARA_CYCLE = 9


class TaraError(validate.InputError):
    """A tara input that cannot be resolved."""


TARA_MEANS = "star"

TARA_COUNTING_RULE = (
    "We can count constellations from the constellation of natal Moon to the "
    "constellation occupied by a planet in transit.")

TARA_RULE = (
    "If a planet is in a bad tara in its transit, it cannot give its full "
    "results. If dasa lord and antardasa lord as per Vimsottari dasa are in "
    "bad taras, bad results can be expected.")

TARA_IN_MUHURTA = (
    "Taras are also used in muhurtas. At the time of an auspicious effort or "
    "when a new project is launched, transit Moon should not be in a bad "
    "constellation with respect to the natal Moon's constellation.")

#: Table 64, in the printed order. `good` is True, False or **None** for the
#: one row the book calls mixed.
TABLE_64_TARAS: tuple[dict[str, object], ...] = (
    {"counts": (1, 10, 19), "name": "Janma Tara", "meaning": "Birth",
     "grade": "mixed", "good": None},
    {"counts": (2, 11, 20), "name": "Sampat Tara", "meaning": "Wealth",
     "grade": "good", "good": True},
    {"counts": (3, 12, 21), "name": "Vipat Tara", "meaning": "Danger",
     "grade": "bad", "good": False},
    {"counts": (4, 13, 22), "name": "Kshema Tara", "meaning": "Well-being",
     "grade": "good", "good": True},
    {"counts": (5, 14, 23), "name": "Pratyak Tara", "meaning": "Obstacles",
     "grade": "bad", "good": False},
    {"counts": (6, 15, 24), "name": "Saadhana Tara",
     "meaning": "Achievement", "grade": "good", "good": True},
    {"counts": (7, 16, 25), "name": "Naidhana/Vadha Tara",
     "meaning": "Death", "grade": "bad", "good": False},
    {"counts": (8, 17, 26), "name": "Mitra Tara", "meaning": "Friend",
     "grade": "good", "good": True},
    {"counts": (9, 18, 27), "name": "Parama Mitra Tara",
     "meaning": "Best friend", "grade": "good", "good": True},
)

#: **Finding.** Table 64 is derivable where Table 63 was not. Its rows are
#: nine consecutive counts repeated three times, so the tara is
#: ``((count - 1) mod 9) + 1`` and the printed table is a check on that
#: arithmetic rather than data to look up.
TABLE_64_IS_A_NINE_CYCLE = (
    "Each row of Table 64 is a count and the counts nine and eighteen after "
    "it, so the tara depends on the count only modulo 9."
)

#: **Finding.** A tara group is exactly one **Vimsottari lord's holding**.
#: §25.6 already proved that a nakshatra, the 10th from it and the 19th from
#: it share a lord; Table 64's rows are those same triples, taken from the
#: natal Moon's nakshatra instead of from an arbitrary one. Checked for all
#: 27 natal positions and all 9 taras.
A_TARA_GROUP_IS_ONE_VIMSOTTARI_LORDS_HOLDING = (
    "The three nakshatras of any tara are the three a single planet owns "
    "under Vimsottari. Section 25.6's companion rule and Table 64's rows are "
    "the same partition of the 27, read from different starting points."
)

#: **Finding.** Four of the nine taras are good, three bad and one mixed, so a
#: graha transiting at random is more likely to be in a good tara than a bad
#: one. Recorded because "tara bala was weak" is a judgement against that
#: baseline, not against an even split.
FOUR_GOOD_THREE_BAD_ONE_MIXED = (
    "Sampat, Kshema, Saadhana, Mitra and Parama Mitra are good — five of the "
    "nine. Vipat, Pratyak and Naidhana are bad. Janma alone is mixed."
)

#: §26.4.1's counting illustration.
TARA_COUNTING_EXAMPLE = (
    "Suppose natal Moon is in Makha and transit Mars is in Swaati. Counting "
    "constellations from Makha, we get (1) Maksha, (2) Poorva Phalguni, (3) "
    "Uttara Phalguni, (4) Hasta, (5) Chitra and (6) Swaati. So Swaati is the "
    "6th constellation from natal Moon's constellation.")

#: **Book defect.** The illustration lists its own first item as "Maksha",
#: one line after writing "Makha" twice. A one-letter slip in a list the
#: sentence around it gets right; recorded rather than silently corrected.
MAKSHA_IS_A_SLIP_FOR_MAKHA = (
    "The counting list opens \"(1) Maksha\" where the two sentences around "
    "it say Makha. Nothing turns on it — the count of six is right either "
    "way — but the word is not the book's own spelling of that nakshatra."
)

#: §26.4.1's worked case.
TARA_WORKED_CASE = {
    "chart": 24, "native": "Bill Gates", "natal_nakshatra": "Uttara Bhadrapada",
    "date": "June 8, 2000",
    "event": "an adverse ruling from a judge who ordered a breakup",
    "in_bad_taras": 5,
    "placements": (
        {"grahas": ("Saturn", "Jupiter"), "nakshatra": "Krittika",
         "count": 5, "tara": "Pratyak Tara", "meaning": "Obstacles"},
        {"grahas": ("Sun", "Venus", "Mars"), "nakshatra": "Mrigashira",
         "count": 7, "tara": "Naidhana/Vadha Tara", "meaning": "Death"},
    ),
    "verdict": "tara bala (strength of stars) was weak",
}


def nakshatra_of(longitude: float) -> int:
    """The nakshatra index a longitude falls in, 0 = Aswini."""
    value = validate.longitude("longitude", float(longitude))
    return min(int(value // NAKSHATRA_SPAN), 26)


def tara_of_count(count: int) -> dict:
    """Table 64's row for a count of constellations, 1 to 27."""
    index = validate.in_range("count", int(count), 1, 27)
    row = TABLE_64_TARAS[(index - 1) % TARA_CYCLE]
    return {"count": index, "position_in_cycle": (index - 1) % TARA_CYCLE + 1,
            **row}


def tara(natal_moon_longitude: float, transit_longitude: float) -> dict:
    """The tara a transiting position makes from the natal Moon's nakshatra.

    The count is inclusive, so a graha in the natal Moon's own nakshatra is
    the 1st and Janma Tara.
    """
    natal = nakshatra_of(natal_moon_longitude)
    transit = nakshatra_of(transit_longitude)
    count = (transit - natal) % 27 + 1
    row = tara_of_count(count)
    return {
        "natal_nakshatra": str(NAKSHATRA_NAMES[natal]),
        "natal_index": natal,
        "transit_nakshatra": str(NAKSHATRA_NAMES[transit]),
        "transit_index": transit,
        "count": count,
        "tara": row["name"],
        "meaning": row["meaning"],
        "grade": row["grade"],
        "good": row["good"],
        "results": (
            "it cannot give its full results" if row["good"] is False
            else None),
    }


def tara_bala(natal_moon_longitude: float,
              transit_longitudes: Mapping[int, float]) -> dict:
    """§26.4.1's tally — how many transiting grahas are in bad taras.

    Janma Tara is counted in neither column, because the book grades it mixed.
    `unaccounted` names any graha in it, so the three counts always sum to the
    number given.
    """
    if not transit_longitudes:
        raise TaraError("name at least one transiting graha")
    per_graha: dict[str, dict] = {}
    good: list[str] = []
    bad: list[str] = []
    mixed: list[str] = []
    for graha, longitude in transit_longitudes.items():
        index = validate.in_range("graha", int(graha), 0, 8)
        name = str(GRAHA_NAMES[index])
        got = tara(natal_moon_longitude, float(longitude))
        per_graha[name] = got
        (good if got["good"] else bad if got["good"] is False
         else mixed).append(name)
    return {
        "of": len(per_graha),
        "in_good_taras": good,
        "in_bad_taras": bad,
        "unaccounted": mixed,
        "count_in_bad_taras": len(bad),
        "per_graha": per_graha,
        "janma_is_mixed": (
            "Janma Tara is graded mixed, so a graha in it is in neither "
            "column"),
        "rule": TARA_RULE,
    }


def muhurta_moon_is_clear(natal_moon_longitude: float,
                          transit_moon_longitude: float) -> dict:
    """§26.4.1's muhurta use: is the transit Moon out of a bad tara?"""
    got = tara(natal_moon_longitude, transit_moon_longitude)
    return {
        **got,
        "clear": got["good"] is not False,
        "mixed": got["good"] is None,
        "rule": TARA_IN_MUHURTA,
    }
