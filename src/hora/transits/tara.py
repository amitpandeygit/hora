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


# --------------------------------------------------------------------------
# §26.4.2 — the eleven special nakshatras
# --------------------------------------------------------------------------

SPECIAL_NAKSHATRAS_INTRO = (
    "In addition to the above general classification, we have a few special "
    "nakshatras for each person.")

#: §26.4.2's eleven, in the order the section numbers them.
SPECIAL_NAKSHATRAS: tuple[dict[str, object], ...] = (
    {"offset": 1, "name": "Janma", "means": "birth",
     "shows": "general well-being"},
    {"offset": 10, "name": "Karma", "means": "profession",
     "shows": "profession and workplace"},
    {"offset": 18, "name": "Saamudaayika", "means": "related to a crowd",
     "shows": "group activities"},
    {"offset": 16, "name": "Sanghaatika", "means": "belonging to group",
     "shows": "group/social activities"},
    {"offset": 4, "name": "Jaati", "means": "community",
     "shows": "one's community — people who belong to the same class, "
              "nature and profession"},
    {"offset": 7, "name": "Naidhana", "means": "death",
     "shows": "death and suffering"},
    {"offset": 12, "name": "Desa", "means": "country", "shows": "one's country"},
    {"offset": 13, "name": "Abhisheka", "means": "coronation",
     "shows": "power and authority", "also_called": "Raajya (kingdom)"},
    {"offset": 19, "name": "Aadhaana", "means": "epoch/conception",
     "shows": "well-being of family"},
    {"offset": 22, "name": "Vainaasika", "means": "destructive",
     "shows": "one's destruction", "also_called": "Vinaasana"},
    {"offset": 25, "name": "Maanasa", "means": "mind",
     "shows": "one's mental state"},
)

SPECIAL_NAKSHATRA_RULE = (
    "Benefics or malefics situated in these constellations in their transit "
    "bring good or bad results related to the area covered by the nakshatra.")

#: The section's caution, and the reason it gives — the sharpest statement in
#: the book of why a transit result is personal and not worldly.
RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE = (
    "However, it should be kept in mind that the results will be with "
    "respect to the native. For example, malefics transiting in desa "
    "nakshatra may not ruin one's country. After all, any country has almost "
    "the same number of people with desa nakshatra in each constellation. "
    "When many malefics are transiting in desa nakshatra, one may be driven "
    "away from one's country or start hating one's country.")

SPECIAL_NAKSHATRAS_REACH_BEYOND_THE_VARGAS = (
    "Sometimes, using these nakshtras gives special insights that cannot be "
    "gained by looking at any divisional chart.")

#: **Finding.** Nine of the eleven fall into **three complete tara triples**,
#: each triple being one Vimsottari lord's whole holding: Janma, Karma and
#: Aadhaana are the 1st, 10th and 19th; Jaati, Abhisheka and Vainaasika the
#: 4th, 13th and 22nd; Naidhana, Sanghaatika and Maanasa the 7th, 16th and
#: 25th. Only Desa (12th) and Saamudaayika (18th) stand alone.
NINE_OF_THE_ELEVEN_FORM_THREE_COMPLETE_TRIPLES = (
    "The special nakshatras at offsets 1, 10 and 19 are one tara; 4, 13 and "
    "22 another; 7, 16 and 25 a third. Each triple is the three nakshatras a "
    "single Vimsottari lord owns. Desa and Saamudaayika have no partners "
    "among the eleven."
)

#: **Finding, and a caution.** The two classifications are independent and
#: must not be read off one another. **Vainaasika**, which shows one's
#: destruction, sits in **Kshema** tara, which Table 64 grades good; and
#: **Sanghaatika** and **Maanasa**, which show social life and the mind, sit
#: in **Naidhana** tara, which it grades bad. So a special nakshatra's subject
#: says nothing about its tara's grade.
THE_TWO_CLASSIFICATIONS_ARE_INDEPENDENT = (
    "Vainaasika shows destruction and falls in the good Kshema tara; "
    "Sanghaatika and Maanasa show group life and the mind and fall in the "
    "bad Naidhana tara. A special nakshatra's meaning and its tara's grade "
    "are separate readings of the same position."
)

#: §26.4.2's worked case. The window is ours, from the ephemeris; the section
#: gives no dates.
SPECIAL_NAKSHATRA_WORKED_CASE = {
    "chart": 24, "native": "Bill Gates",
    "natal_nakshatra": "Uttara Bhadrapada",
    "jaati": "Bharani", "karma": "Pushya",
    "readings": (
        {"graha": "Saturn", "nakshatra": "Bharani", "special": "Jaati",
         "result": "several people in the software community turned against "
                   "Bill Gates and gave damaging testimonies ... He was more "
                   "or less alienated in the community of software "
                   "entrepreneurs"},
        {"graha": "Rahu", "nakshatra": "Pushya", "special": "Karma",
         "result": "that brought tension related to litigation at his "
                   "workplace"},
    ),
}

#: **Finding.** §26.4.2 dates nothing, and the two transits it names overlap
#: for a definite window: Saturn is in Bharani from 30 April 1999 to 11 May
#: 2000 and Rahu in Pushya from 20 September 1999 to 28 May 2000, so "at the
#: same time" runs **20 September 1999 to 11 May 2000**. That window holds the
#: findings of fact and the conclusions of law, and closes a month before the
#: breakup order of 8 June 2000 that §26.3 and §26.4.1 read — so the section
#: is reading an earlier phase, not the same event again.
THE_TWO_SPECIAL_TRANSITS_OVERLAP_FOR_EIGHT_MONTHS = (
    "Saturn is in Bharani from 30 April 1999 to 11 May 2000 and Rahu in "
    "Pushya from 20 September 1999 to 28 May 2000. Both hold together from "
    "20 September 1999 to 11 May 2000, which ends before the 8 June 2000 "
    "ruling the other two sections read."
)


def special_nakshatra(name: str, natal_moon_longitude: float) -> dict:
    """Where one of §26.4.2's eleven falls, for a nativity."""
    row = next((r for r in SPECIAL_NAKSHATRAS if r["name"] == name), None)
    if row is None:
        raise TaraError(
            f"{name!r} is not one of section 26.4.2's special nakshatras; "
            f"the eleven are "
            f"{', '.join(str(r['name']) for r in SPECIAL_NAKSHATRAS)}")
    natal = nakshatra_of(natal_moon_longitude)
    offset = int(row["offset"])  # type: ignore[call-overload]
    index = (natal + offset - 1) % 27
    return {
        **row,
        "janma_nakshatra": str(NAKSHATRA_NAMES[natal]),
        "index": index,
        "nakshatra": str(NAKSHATRA_NAMES[index]),
        "tara": tara_of_count(offset)["name"],
    }


def special_nakshatras(natal_moon_longitude: float) -> tuple[dict, ...]:
    """All eleven, for a nativity, in §26.4.2's own order."""
    return tuple(special_nakshatra(str(row["name"]), natal_moon_longitude)
                 for row in SPECIAL_NAKSHATRAS)


def special_transits(natal_moon_longitude: float,
                     transit_longitudes: Mapping[int, float]) -> dict:
    """Which of the eleven each transiting graha is sitting in.

    A graha may be in none of them, and most are: the eleven cover eleven of
    twenty-seven nakshatras. No verdict is returned — §26.4.2 grades by the
    graha's own benefic or malefic nature and by how *many* are there, and
    the caller supplies both.
    """
    if not transit_longitudes:
        raise TaraError("name at least one transiting graha")
    by_index = {int(entry["index"]): entry
                for entry in special_nakshatras(natal_moon_longitude)}
    hits: list[dict] = []
    elsewhere: list[str] = []
    for graha, longitude in transit_longitudes.items():
        index = validate.in_range("graha", int(graha), 0, 8)
        name = str(GRAHA_NAMES[index])
        where = nakshatra_of(float(longitude))
        entry = by_index.get(where)
        if entry is None:
            elsewhere.append(name)
            continue
        hits.append({"graha": name, "nakshatra": entry["nakshatra"],
                     "special": entry["name"], "shows": entry["shows"]})
    return {
        "of": len(transit_longitudes),
        "in_special_nakshatras": hits,
        "elsewhere": elsewhere,
        "rule": SPECIAL_NAKSHATRA_RULE,
        "caution": RESULTS_ARE_WITH_RESPECT_TO_THE_NATIVE,
        "verdict": None,
        "undecided": (
            "Section 26.4.2 grades by the transiting graha's benefic or "
            "malefic nature and by how many are present — \"many malefics\", "
            "\"many benefics\" — and gives no number for \"many\". The "
            "placements are returned without a grading."),
    }


# --------------------------------------------------------------------------
# Exercise 41 — a special nakshatra read on a chart already in the register
# --------------------------------------------------------------------------

EXERCISE_41 = (
    "Consider a native born in Leo lagna. He has Moon also in Leo in Poorva "
    "Phalguni constellation. Let us say Jupiter is transiting in Sg in "
    "Poorvaashaadha constellation with Mars. Mars is a yogakaraka from natal "
    "lagna. Jupiter is transiting in his moolatrikona, in the 5th house from "
    "natal lagna and Moon. That's very favorable transit. Find out if transit "
    "Jupiter and transit Mars are in a special nakshatra. Based on it, try to "
    "guess the area in which the transit did good to the native.")

EXERCISE_41_ANSWER = (
    "Poorvaashaadha is the 10th constellation from Poorva Phalguni. So the "
    "favorable transit of Jupiter and Mars happens to be in the Karma "
    "nakshatra, which shows profession. So the good results to be experienced "
    "may be related to profession.")

EXERCISE_41_FINAL = (
    "The details belong to Rajiv Gandhi. He suddenly became India's Prime "
    "Minister during the said transit. We gave his birthdata earlier.")

#: **Finding.** The exercise is Chart 60 read a third way. Exercise 40 read it
#: with §25.5's ashtakavarga, §26.2's murthi discussion used its ingress
#: neighbour, and this reads it with §26.4.2's special nakshatras — the same
#: nativity and the same instant, 31 October 1984, through three chapters.
EXERCISE_41_IS_CHART_60_A_THIRD_TIME = (
    "Leo lagna, the Moon in Leo in Purva Phalguni, and Jupiter with Mars in "
    "Purva Ashadha on the accession day are Chart 60's own figures. Exercise "
    "40 read the same chart and instant through ashtakavarga."
)

#: **Finding.** §26.4.2 and §26.5 both grade by *natural* benefic and malefic.
#: Exercise 41 reads **Mars** — a natural malefic — as part of a "favorable
#: transit", and the only reason it gives is that he is a **yogakaraka from
#: natal lagna**. So functional nature is used where the rules say natural,
#: and the exercise does not say it is doing so.
A_YOGAKARAKA_MALEFIC_IS_READ_AS_FAVOURABLE = (
    "Mars is a natural malefic and a yogakaraka for a Leo lagna. Section "
    "26.4.2 says malefics in a special nakshatra bring bad results related to "
    "it; Exercise 41 calls his karma-nakshatra transit favourable on the "
    "strength of the lordship alone."
)

#: **Finding.** The transit is the **Karma** nakshatra and the **Janma** tara
#: at once — the 10th from janma nakshatra is both. Table 64 grades Janma
#: mixed, and the exercise reads the placement as decidedly good, which is
#: `THE_TWO_CLASSIFICATIONS_ARE_INDEPENDENT` happening in a worked case rather
#: than argued from the tables.
KARMA_IS_ALSO_JANMA_TARA_AND_THE_READING_IGNORES_THE_TARA = (
    "The 10th constellation from the natal Moon's is Karma among the special "
    "nakshatras and Janma among the taras. Exercise 41 reads the special "
    "nakshatra and says nothing about the tara, whose grade is mixed."
)

#: Exercise 41's checkable claims, each asserted against Chart 60.
EXERCISE_41_CLAIMS: tuple[str, ...] = (
    "lagna is Leo",
    "the Moon is in Leo, in Poorva Phalguni",
    "Jupiter and Mars both transit Sg in Poorvaashaadha",
    "Mars is a yogakaraka from the natal lagna",
    "Sg is the 5th house from the natal lagna and from the Moon",
    "Poorvaashaadha is the 10th constellation from Poorva Phalguni",
    "so the transit falls in the Karma nakshatra, which shows profession",
)
