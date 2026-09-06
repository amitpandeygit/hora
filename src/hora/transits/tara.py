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


# --------------------------------------------------------------------------
# Exercise 42 — a naidhana transit that agrees with chapter 14
# --------------------------------------------------------------------------

EXERCISE_42 = (
    "For a native with lagna in Leo, natal Moon is in the 4th quarter of "
    "Dhanishtha. When the transit chart contains Saturn in Bharani, identify "
    "a possible result.")

EXERCISE_42_ANSWER = (
    "Bharani is the 7th constellation from Dhanishtha, i.e. it is the "
    "naidhana nakshatra (death). Saturn is a malefic and the 7th lord - and "
    "hence a maraka - here. So this transit has the potential to bring "
    "death. Of course, not everyone with lagna in Leo and Moon in Dhanishtha "
    "dies then, but death is a possibility during the transit.")

EXERCISE_42_FINAL = (
    "The details belong to John F. Kennedy, Jr. He died in a plane crash "
    "during the said transit. We gave his birthdata earlier.")

#: **Finding.** The reading needs **three** things to line up, and the
#: exercise says so by ruling itself out: the nakshatra is naidhana, the
#: transiting graha is a natural malefic, **and** he is a maraka lord from the
#: lagna. Chapter 14's maraka houses are the 2nd and 7th, and Saturn owns
#: Aquarius, the 7th from Leo. So §26.4.2's special nakshatra and §14's maraka
#: are two independent systems agreeing on one graha.
THE_NAIDHANA_READING_NEEDS_A_MARAKA_TOO = (
    "Bharani is the naidhana nakshatra for this Moon, Saturn is a natural "
    "malefic, and Saturn is the 7th lord from a Leo lagna and so a maraka "
    "under section 14. The exercise leans on all three, not on the nakshatra "
    "alone."
)

#: **Finding.** The exercise disowns its own rule in the same breath — "not
#: everyone with lagna in Leo and Moon in Dhanishtha dies then". A Leo lagna
#: with the Moon in Dhanishtha is roughly one nativity in 324, so the
#: qualifying population is large, and the section is saying the transit
#: raises a possibility rather than picking a person. It is the same caution
#: §26.4.2 gave about desa nakshatra and a whole country.
THE_TRANSIT_NAMES_A_POSSIBILITY_NOT_A_PERSON = (
    "Not everyone with lagna in Leo and Moon in Dhanishtha dies then, but "
    "death is a possibility during the transit."
)

#: **Not supplied.** The disclaimer carries footnote 72 and the note itself
#: was not on the page given. Nothing is inferred from the marker.
FOOTNOTE_72_IS_NOT_SUPPLIED = (
    "Exercise 42's answer marks its disclaimer with footnote 72. The "
    "footnote's text has not been supplied and nothing here stands in for it."
)

#: **Finding.** JFK Jr's death is now read twice by the book through two
#: different mechanisms — Example 107 through §25.4's interaction (2), the
#: natal rasi chart against the transit D-11, and Exercise 42 through the
#: naidhana nakshatra. Same nativity, same instant, two chapters.
JFK_JRS_DEATH_IS_READ_TWICE = (
    "Chart 56 and Chart 57 read the crash through a natal rasi chart and a "
    "transit D-11; Exercise 42 reads the same moment through the nakshatra "
    "Saturn occupies from the natal Moon's."
)

#: Exercise 42's checkable claims, each asserted against Chart 56.
EXERCISE_42_CLAIMS: tuple[str, ...] = (
    "lagna is Leo",
    "the natal Moon is in the 4th quarter of Dhanishtha",
    "Bharani is the 7th constellation from Dhanishtha",
    "so Bharani is this nativity's naidhana nakshatra",
    "Saturn is a natural malefic",
    "Saturn owns the 7th from Leo and is therefore a maraka",
    "Saturn was in Bharani at the recorded moment of death",
)


# --------------------------------------------------------------------------
# Exercise 43 — the special nakshatra supplies the subject, not the verdict
# --------------------------------------------------------------------------

EXERCISE_43 = (
    "For a native with natal Moon in the 3rd quarter of Poorvabhadrapada and "
    "lagna in Virgo, transit of Mars in Aasresha constellation in Cancer "
    "brought material gains. Cancer is the 6th from natal Moon and 11th from "
    "natal lagna. Both are favorable transits and so it makes sense that this "
    "transit gave material gains. Now find out if Mars occupies a special "
    "constellation and, based on it, guess the nature of the gains.")

EXERCISE_43_ANSWER = (
    "Aasresha is the 12th constellation from Poorvabhaadrapada, i.e. Desa "
    "nakshatra. Being a debilitated malefic in desa nakshatra (country), Mars "
    "can drive him out of his country. That was indeed how Mars gave gains to "
    "the native of Chart 63 in the second week of November 1994. The native "
    "left his motherland India then.")

#: **Finding.** This is the clearest statement in either chapter of how the
#: two layers compose. The **houses** decide whether a transit is favourable —
#: Cancer is the 6th from the Moon and the 11th from the lagna, both among
#: Mars's good houses — and the **special nakshatra** decides what the results
#: are about. The exercise asks for exactly that split: it states the gains up
#: front and asks the reader only to "guess the nature of the gains".
THE_HOUSE_GIVES_THE_VALENCE_AND_THE_NAKSHATRA_THE_SUBJECT = (
    "Cancer is favourable for Mars by house from both the Moon and the "
    "lagna, which is why the transit gives gains. Ashlesha is the desa "
    "nakshatra, which is why the gains come through leaving the country. "
    "Neither layer decides the other."
)

#: **Finding.** §26.4.2's wording is "**many** malefics transiting in desa
#: nakshatra"; Exercise 43 reaches the same result from **one**, and the extra
#: weight it names is debilitation. So a debilitated malefic counts for what
#: the section otherwise wants several. The book states no exchange rate, and
#: none is coded — this is the second unquantified "many" in the chapter.
A_DEBILITATED_MALEFIC_COUNTS_FOR_MANY = (
    "Section 26.4.2 asks for many malefics in desa nakshatra to drive one "
    "from one's country. Exercise 43 gets there with a single Mars, and says "
    "only that he is debilitated."
)

#: **Finding.** A transit can be favourable and unwelcome at once. Mars is
#: **debilitated** in Cancer, and the exercise still calls the transit
#: favourable and its results gains — because the favourability is read from
#: the house and the debilitation from the sign. Nothing here treats a
#: debilitated graha's transit as bad on that ground alone.
DEBILITATION_DOES_NOT_MAKE_THE_TRANSIT_UNFAVOURABLE = (
    "Mars is debilitated in Cancer and Cancer is one of his good transit "
    "houses from both reference points. The exercise reads the transit as "
    "favourable and uses the debilitation only to sharpen what it does."
)

#: **Finding.** Chart 63's native is described leaving India twice — landing
#: in the USA on 16 August 1991 in Exercise 38, and leaving his motherland
#: again in the second week of November 1994 here. Both readings stand on
#: their own transits and neither is a misprint of the other; both are on the
#: chart's record so a reader does not take one for the other.
CHART_63S_NATIVE_LEAVES_INDIA_TWICE = (
    "Exercise 38 dates a departure to 16 August 1991 and Exercise 43 dates "
    "one to the second week of November 1994, three years apart, for the "
    "same nativity."
)

#: **Finding.** The transit window is ours, from the ephemeris: Mars is in
#: Ashlesha from **24 October to 23 November 1994**, so the second week of
#: November falls inside it with a fortnight to spare either side. The
#: exercise gives a week and no day.
MARS_IS_IN_ASHLESHA_FOR_A_MONTH_AROUND_THE_EVENT = (
    "Mars enters Ashlesha on 24 October 1994 and leaves on 23 November 1994. "
    "The second week of November is inside that month-long stay."
)

#: Exercise 43's checkable claims, each asserted against Chart 63.
EXERCISE_43_CLAIMS: tuple[str, ...] = (
    "the natal Moon is in the 3rd quarter of Poorvabhadrapada",
    "lagna is Virgo",
    "Cancer is the 6th from the natal Moon",
    "Cancer is the 11th from the natal lagna",
    "both are favourable houses for a Mars transit",
    "Aasresha is the 12th constellation from Poorvabhadrapada",
    "so Ashlesha is this nativity's desa nakshatra",
    "Mars is debilitated in Cancer",
)


# --------------------------------------------------------------------------
# Exercise 44 — a nakshatra aspect that lands on two special nakshatras
# --------------------------------------------------------------------------

EXERCISE_44 = (
    "For the native of Exercise 42, transit Mars was in Swaati when transit "
    "Saturn was in Bharani. Identify the constellations aspected by Mars and "
    "see if any special constellations are included. If so, predict the "
    "possible result.")

EXERCISE_44_ANSWER = (
    "Mars aspects the 1st, 3rd, 7th, 8th and 15th constellations from him. "
    "Mars in Swaati will aspect (1) Swaati, (2) Anooradha, (3) "
    "Uttaraashaadha, (4) Sravanam, and, (5) Bharani. Because natal Moon is in "
    "Dhanishtha, these are the 20th, 22nd, 26th, 27th and 7th constellations "
    "(respectively) from janma nakshatra. Out of these, 2 are special "
    "nakshatras. The 7th constellation is known as naidhana nakshatra and "
    "shows death. The 22nd nakshatra is known as vainaasika nakshatra and "
    "shows destruction. Mars aspects both. As seen in Exercise 42, maraka in "
    "the natal chart Saturn occupies naidhana nakshatra. The predicted result "
    "is death.")

EXERCISE_44_FINAL = (
    "As already mentioned, Mr. Kennedy passed away during this transit.")

#: The five nakshatras Mars aspects from Swati, and their counts from a
#: Dhanishtha janma nakshatra, in the order the answer lists them.
EXERCISE_44_ASPECTED: tuple[tuple[str, int], ...] = (
    ("Swati", 20), ("Anuradha", 22), ("Uttara Ashadha", 26),
    ("Shravana", 27), ("Bharani", 7),
)

#: **Finding.** This is §26.5's aspect scheme doing work for the first time,
#: and what it needs is the **3rd** alongside the universal 15th. From Swati
#: the 15th is Bharani, this nativity's naidhana nakshatra, so every graha
#: reaches that one; the 3rd is Anuradha, its vainaasika, and only **Mars and
#: Saturn** have a 3rd in their lists. So exactly two of the seven reach both
#: special nakshatras from Swati, and they are the two the exercise involves.
ONLY_MARS_AND_SATURN_REACH_BOTH_SPECIAL_NAKSHATRAS = (
    "Bharani is the 15th from Swati and every graha aspects the 15th, so all "
    "seven reach the naidhana nakshatra. Anuradha is the 3rd, and Mars and "
    "Saturn are the only two whose lists contain a 3rd, so they alone also "
    "reach the vainaasika."
)

#: **Finding.** The reading stacks four independent things on one moment, and
#: the exercise names each: Saturn is a maraka lord **occupying** the naidhana
#: nakshatra, and Mars **aspects** the naidhana and the vainaasika. Occupation
#: and aspect are different mechanisms, and §26.4.2 gave a rule only for the
#: first — "benefics or malefics situated in these constellations". §26.5
#: supplies the second, and the exercise is where they are used together.
OCCUPATION_AND_ASPECT_ARE_COMBINED_HERE = (
    "Section 26.4.2 grades a graha situated in a special nakshatra and "
    "section 26.5 grades what a graha aspects. Exercise 44 reads Saturn "
    "occupying the naidhana nakshatra and Mars aspecting it, and treats the "
    "two as adding up."
)

#: Footnote 73 — a fifth factor, resting on a table the book has not printed.
FOOTNOTE_73 = (
    "In the natal chart, Mars occupies his Mritya Bhaga (part of death). So "
    "his aspect over the two special constellations is also significant.")

#: **Not defined.** Nothing read so far says what a mrityu bhaga is, and the
#: claim needs a degree per graha per rasi. Chart 56's Mars is printed at
#: **25 Ge 12**, which is the datum to test a table against when one arrives.
#: See OI-144; no table is written from outside the book.
MRITYU_BHAGA_IS_USED_WITHOUT_A_DEFINITION = (
    "Footnote 73 says Chart 56's Mars occupies his mrityu bhaga. No section "
    "supplied defines a mrityu bhaga or prints its degrees, so the claim is "
    "held as the book's and not checked."
)

#: Footnote 74 — the strongest caution in either transit chapter, and the one
#: that says what the technique needs alongside it.
FOOTNOTE_74 = (
    "It will be very hasty to predict someone's death just based on "
    "conjunctions and aspects on special nakshatras in transit. Out of the "
    "many people with the same nakshatra, only those people whose dasas and "
    "Tajaka charts also show death will die at the time of this "
    "death-inflicting transit.")

#: **Finding.** Footnote 74 makes the corroboration explicit where Exercise
#: 42's disclaimer only gestured at it, and one of the two things it names —
#: **Tajaka charts** — is a part of the book not yet reached. So §26.4's death
#: readings are, by the book's own statement, incomplete until then, and
#: nothing built on them may return a death verdict.
THE_TECHNIQUE_NEEDS_DASAS_AND_TAJAKA_TO_BE_USED_AT_ALL = (
    "Footnote 74 requires the dasas and the Tajaka chart to show death too. "
    "Tajaka has not been reached, so a transit reading of this kind is by "
    "the book's own rule never sufficient on its own."
)

#: Exercise 44's checkable claims.
EXERCISE_44_CLAIMS: tuple[str, ...] = (
    "Mars aspects the 1st, 3rd, 7th, 8th and 15th constellations from him",
    ("from Swaati those are Swaati, Anooradha, Uttaraashaadha, Sravanam "
     "and Bharani"),
    ("from a Dhanishtha janma nakshatra those are the 20th, 22nd, 26th, "
     "27th and 7th"),
    "exactly two of the five are special nakshatras",
    "the 7th is naidhana and the 22nd is vainaasika",
    "Saturn, the maraka, occupies the naidhana nakshatra",
)
