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

#: Footnote 72, on Exercise 42's disclaimer. The broadest limit the chapter
#: puts on itself: it scopes the whole nakshatra family, not just the death
#: reading footnote 74 qualifies.
FOOTNOTE_72 = (
    "These transit principles based on nakshtra give good insight into "
    "future, but one cannot make predictions just based on them.")

#: **Finding.** The chapter carries two disclaimers and they do different
#: work. Footnote 72 covers **all** the nakshatra transit principles —
#: §26.4.1's taras, §26.4.2's special nakshatras and §26.5's aspects — and
#: says only that they are insufficient. Footnote 74 narrows to death
#: predictions and names **what** must corroborate: the dasas and the Tajaka
#: chart. So the general limit comes first and the specific remedy second.
THE_TWO_FOOTNOTES_SCOPE_AND_THEN_SHARPEN = (
    "Footnote 72 says the nakshatra transit principles cannot carry a "
    "prediction on their own. Footnote 74 says what a death prediction needs "
    "beside them, the dasas and the Tajaka chart. The first bounds the "
    "family; the second names the corroboration."
)

#: **Book defect.** Footnote 72 prints "nakshtra" for "nakshatra". The same
#: kind of one-letter slip as §26.4.1's "Maksha" for "Makha"; recorded rather
#: than silently corrected.
NAKSHTRA_IS_A_SLIP_FOR_NAKSHATRA = (
    "Footnote 72 reads \"transit principles based on nakshtra\". Nothing "
    "turns on it, and the word is spelt correctly everywhere else in the "
    "chapter."
)

#: **Finding.** Every technique chapter 26 introduces is hedged, and §26.5 is
#: the only one hedged by nothing of its own. §26.2's murthi and §26.3's vedha
#: are themselves brakes on a chapter 25 verdict rather than verdicts;
#: §26.4.1 says a bad tara means a graha "cannot give its full results";
#: §26.4.2 says the results are the native's and not the world's; and
#: footnotes 72 and 74 bound the family twice more.
EVERY_TECHNIQUE_IN_CHAPTER_26_IS_HEDGED = (
    "The murthi and the vedha modify a verdict rather than making one, a bad "
    "tara withholds full results rather than predicting harm, the special "
    "nakshatras are read against the native and not the country, and two "
    "footnotes say the nakshatra principles cannot carry a prediction alone."
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


# --------------------------------------------------------------------------
# §26.6 — constellations and body parts
# --------------------------------------------------------------------------

BODY_PART_RULE = (
    "When they are transiting in various constellations as counted from "
    "janma nakshatra, planets are said to dwell in different parts of one's "
    "body and correspondingly some standard results are attributed. These "
    "results are given in Table 65 - Table 69.")

#: §26.6's two uses, in its order. The second runs the rule **backwards** —
#: from an ailing body part to the graha responsible — which no other transit
#: technique in either chapter does.
BODY_PART_PURPOSES: tuple[str, ...] = (
    ("We can find the standard results for planetary transits in different "
     "constellations with respect to the constellation of natal Moon."),
    ("If a native has a disease or problem in a particular body part, we may "
     "be able to use these tables and figure out the planet causing it. That "
     "can help us in deciding the right remedial measures. We can also take "
     "preventive measures before the transit."),
)

#: **Finding.** Purpose (2) is the only **inverse** reading in Part 3. Every
#: other technique goes from a position to a result; this goes from an
#: observed symptom back to a graha, and then forward again to a remedy and to
#: a date to prepare for. That makes the tables a lookup in two directions,
#: and the second direction is many-to-one — several grahas may dwell in one
#: body part — so it narrows rather than identifies.
THE_SECOND_PURPOSE_READS_THE_TABLES_BACKWARDS = (
    "Section 26.6 is the only place in Part 3 that starts from a result and "
    "asks which graha caused it. The tables are consulted from the body part "
    "inwards, and more than one graha can dwell in a part, so the answer is "
    "a shortlist and not a name."
)

#: **Finding.** Five tables were promised for seven grahas and Table 68
#: answers how: it covers **Mercury, Jupiter and Venus** together. With the
#: Sun, Moon and Mars taking one table each that is six of the seven, so
#: Saturn is the only graha left for Table 69 — an inference from what
#: remains, not something the book has said.
FIVE_TABLES_FOR_SEVEN_GRAHAS = (
    "Table 65 is the Sun's, 66 the Moon's and 67 Mars's; Table 68 covers "
    "Mercury, Jupiter and Venus together. Saturn is the only graha not yet "
    "given a table, and Table 69 is the only table not yet supplied."
)

#: Tables 65 to 69, by number. A table moves from ``None`` to its content when
#: its page is supplied; `test_section_26_6_is_not_finished_early` fails while
#: any is still pending, so the section cannot be reported complete early.
#: This is the same shape as chapter 25's `STANDARD_RESULT_TABLES`, which was
#: filled one table at a time from Table 53 to Table 59.
#: Table 65, as printed. Rows in the table's own order; `counts` are
#: nakshatras counted inclusively from janma nakshatra.
TABLE_65_SUN: dict[str, object] = {
    "grahas": ("Sun",),
    "title": "Body Parts in the Transit of Sun",
    "rows": (
        {"counts": (1,), "part": "Mouth/Face", "result": "Destruction"},
        {"counts": (2, 3, 4, 5), "part": "Head",
         "result": "Influx of wealth"},
        {"counts": (6, 7, 8, 9), "part": "Chest", "result": "Victory"},
        {"counts": (10, 11, 12, 13), "part": "Right hand",
         "result": "Wealth"},
        {"counts": (14, 15, 16, 17, 18, 19), "part": "Two feet",
         "result": "Poverty"},
        {"counts": (20, 21, 22, 23), "part": "Left hand",
         "result": "Physical ailments"},
        {"counts": (24, 25), "part": "Eyes", "result": "Gains"},
        {"counts": (26, 27), "part": "Private parts", "result": "Death"},
    ),
}

#: Table 66, as printed. Its last two rows fall past a page break in the
#: source and are part of the same table.
TABLE_66_MOON: dict[str, object] = {
    "grahas": ("Moon",),
    "title": "Body Parts in the Transit of Moon",
    "rows": (
        {"counts": (1, 2), "part": "Face", "result": "Great fear"},
        {"counts": (3, 4, 5, 6), "part": "Head", "result": "Well-being"},
        {"counts": (7, 8), "part": "Back",
         "result": "Victory over enemies"},
        {"counts": (9, 10), "part": "Eyes", "result": "Money"},
        {"counts": (11, 12, 13, 14, 15), "part": "Heart",
         "result": "Comforts and peace"},
        {"counts": (16, 17, 18), "part": "Left hand", "result": "Quarrels"},
        {"counts": (19, 20, 21, 22, 23, 24), "part": "Two feet",
         "result": "Going abroad"},
        {"counts": (25, 26, 27), "part": "Right hand",
         "result": "Financial gains"},
    ),
}

#: Table 67, as printed. It is the table that proves Mouth/Face and Face are
#: two different parts: Mars dwells in both, at different counts and to
#: different effect.
TABLE_67_MARS: dict[str, object] = {
    "grahas": ("Mars",),
    "title": "Body Parts in the Transit of Mars",
    "rows": (
        {"counts": (1, 2), "part": "Mouth/Face", "result": "Death"},
        {"counts": (3, 4, 5, 6, 7, 8), "part": "Two feet",
         "result": "Separation"},
        {"counts": (9, 10, 11), "part": "Chest", "result": "Victory"},
        {"counts": (12, 13, 14, 15), "part": "Left hand",
         "result": "Poverty"},
        {"counts": (16, 17), "part": "Head", "result": "Gains"},
        {"counts": (18, 19, 20, 21), "part": "Face", "result": "Great fear"},
        {"counts": (22, 23, 24, 25), "part": "Right hand",
         "result": "Well-being"},
        {"counts": (26, 27), "part": "Eyes", "result": "Going abroad"},
    ),
}

#: Table 68, as printed. The first to cover **more than one graha**, and the
#: first with fewer than eight rows.
TABLE_68_MERCURY_JUPITER_VENUS: dict[str, object] = {
    "grahas": ("Mercury", "Jupiter", "Venus"),
    "title": "Body Parts in the Transit of Mercury, Jupiter and Venus",
    "rows": (
        {"counts": (1, 2, 3), "part": "Head", "result": "Grief"},
        {"counts": (4, 5, 6), "part": "Face", "result": "Gains"},
        {"counts": (7, 8, 9, 10, 11, 12), "part": "Two hands",
         "result": "Misfortune"},
        {"counts": (13, 14, 15, 16, 17), "part": "Stomach",
         "result": "Amassing of wealth"},
        {"counts": (18, 19), "part": "Private parts",
         "result": "Destruction"},
        {"counts": (20, 21, 22, 23, 24, 25, 26, 27), "part": "Two feet",
         "result": "Honor and fame"},
    ),
}

BODY_PART_TABLES: dict[int, dict[str, object] | None] = {
    65: TABLE_65_SUN,
    66: TABLE_66_MOON,
    67: TABLE_67_MARS,
    68: TABLE_68_MERCURY_JUPITER_VENUS,
    69: None,
}

#: **Ours, not the book's.** §26.6 prints no good/bad column, so this names
#: the results that are plainly harms. No row's wording pulls against itself
#: the way Venus's 12th did in Table 58, so reading the plain sense is safe —
#: but see `BODY_PART_NEUTRAL` for the results that are neither.
BODY_PART_HARMS: frozenset[str] = frozenset({
    "Destruction", "Poverty", "Physical ailments", "Death",
    "Great fear", "Quarrels", "Separation", "Grief", "Misfortune"})

#: **Ours.** Results that are neither a harm nor a benefit. Table 66's "Going
#: abroad" is the first: it is an event, not a verdict, and Exercise 43 read
#: one native's departure as the **gain** a favourable transit brought. So it
#: is left ungraded rather than forced onto a side.
BODY_PART_NEUTRAL: frozenset[str] = frozenset({"Going abroad"})

#: **Finding.** §26.6's results are not all verdicts. Table 65's eight all
#: read plainly good or bad; Table 66 introduces one that does not — "Going
#: abroad" — so `harm` is three-valued from here on and a caller must handle
#: `None`. Nothing decides it for them, because the book does not.
NOT_EVERY_STANDARD_RESULT_IS_A_VERDICT = (
    "Going abroad is an event and not a grade. Exercise 43 read a departure "
    "as the gain a favourable transit gave, so the same result can be "
    "welcome or not depending on the native, and section 26.6 says nothing."
)

#: **Finding.** Each table names eight parts and they are drawn from a larger
#: shared pool: five — Head, Eyes, Left hand, Right hand, Two feet — appear in
#: every table so far, and the rest vary. A reverse lookup by exact name will
#: therefore find some grahas and not others for closely-named parts, which is
#: why `grahas_dwelling_in` also reports parts whose names overlap.
THE_TABLES_DRAW_EIGHT_PARTS_FROM_A_LARGER_POOL = (
    "Head, Eyes, Left hand, Right hand and Two feet are in every table so "
    "far; Chest, Private parts, Back, Heart, Face and Mouth/Face appear in "
    "some. Each table names exactly eight."
)

#: **Correction, on Table 67's evidence.** Reading Tables 65 and 66 alone it
#: looked as though the Sun's **Mouth/Face** and the Moon's **Face** might be
#: one part under two names. Table 67 settles it: Mars dwells in **both**, at
#: the 1st and 2nd giving Death and at the 18th to 21st giving Great fear. So
#: they are two distinct parts, and nothing merges them.
MOUTH_FACE_AND_FACE_ARE_DIFFERENT_PARTS = (
    "Table 67 gives Mars Mouth/Face at the 1st and 2nd and Face at the 18th "
    "to 21st, with different results. They are not two spellings of one "
    "part."
)

#: **Finding, narrowed by Table 68.** Two feet is the **widest block** in
#: every table so far, which holds across all four. It took exactly **six**
#: counts in the three single-graha tables and takes **eight** in Table 68,
#: so the six belonged to those three and not to the rule. The counts move
#: and the results differ throughout — Poverty, Going abroad, Separation,
#: Honor and fame.
TWO_FEET_IS_THE_WIDEST_BLOCK_IN_EVERY_TABLE = (
    "Two feet takes six counts for the Sun, the Moon and Mars and eight in "
    "Table 68, and is the largest block in all four. Only its being the "
    "widest survives; the six did not."
)

#: **Finding.** Granularity tracks how many grahas share a table. The three
#: single-graha tables have **eight** rows each and split the hands into left
#: and right; Table 68, which covers three grahas at once, has **six**, merges
#: them into "Two hands", drops Eyes altogether and adds Stomach. So the
#: shared table is the coarser reading — which is what one would expect of a
#: rule stated once for three grahas, though the book does not say so.
THE_SHARED_TABLE_IS_THE_COARSER_ONE = (
    "Tables 65, 66 and 67 have eight rows and name Left hand and Right hand "
    "separately. Table 68 covers three grahas, has six rows, and says Two "
    "hands."
)

#: **Finding.** Table 65 has a different *shape* from Table 64, so neither can
#: be derived from the other. The taras repeat every nine nakshatras; the body
#: parts run in **contiguous blocks** of 1, 4, 4, 4, 6, 4, 2 and 2, which is
#: not periodic at all.
THE_BODY_PART_TABLE_IS_BLOCKS_NOT_A_CYCLE = (
    "Table 64 assigns a tara by the count modulo 9. Table 65 assigns a body "
    "part by which contiguous run of counts it falls in, and the runs are "
    "1, 4, 4, 4, 6, 4, 2, 2. No modulus reproduces that."
)

#: **Finding.** The two tables also disagree about *outcomes*, and not
#: slightly. Of the 24 counts Table 64 grades good or bad — Janma's three are
#: mixed — the plain sense of Table 65's result agrees with 12 and contradicts
#: 12. The sharpest are the **26th and 27th**, Mitra and Parama Mitra, Table
#: 64's two friendliest taras, which Table 65 calls **Death**; and the
#: **7th**, the naidhana tara, which it calls **Victory**.
THE_TWO_TABLES_AGREE_NO_BETTER_THAN_CHANCE = (
    "Table 64 and Table 65 agree on 12 of the 24 counts Table 64 grades, and "
    "contradict each other on the other 12. The 26th and 27th are Mitra and "
    "Parama Mitra and give Death; the 7th is Naidhana and gives Victory."
)

#: **Finding.** The Sun in one's **own** janma nakshatra gives Destruction —
#: the worst of the eight results, on the one count that has a block to
#: itself. Table 64 grades that same count mixed and §26.4.2 calls it the
#: Janma nakshatra, "general well-being". Three classifications, three
#: different verdicts on the 1st.
THE_FIRST_COUNT_IS_GRADED_THREE_WAYS = (
    "The 1st constellation from janma nakshatra is Janma Tara and mixed in "
    "Table 64, the Janma special nakshatra showing general well-being in "
    "section 26.4.2, and Mouth/Face giving Destruction in Table 65."
)

BODY_PART_TABLES_PENDING: tuple[int, ...] = tuple(
    number for number, table in BODY_PART_TABLES.items() if table is None)


def _rows_of(table: dict[str, object]) -> tuple[dict[str, object], ...]:
    rows = table["rows"]
    assert isinstance(rows, tuple)
    return rows


#: Words that say *which* or *how many* rather than what. Dropping them keeps
#: "Two feet" from matching "Two hands" while leaving the hands joined by the
#: word that matters.
_PART_QUALIFIERS = frozenset({"two", "left", "right"})


def _words(part: str) -> frozenset[str]:
    """A body part's naming words, singularised, for the near-match in
    `grahas_dwelling_in`. "Two hands" and "Left hand" must overlap — the
    tables use both, and a plural is all that separates them — while "Two
    feet" and "Two hands" must not."""
    return frozenset(
        word[:-1] if word.endswith("s") and len(word) > 2 else word
        for word in part.replace("/", " ").lower().split()
    ) - _PART_QUALIFIERS


def _grahas_of(table: dict[str, object]) -> tuple[str, ...]:
    grahas = table["grahas"]
    assert isinstance(grahas, tuple)
    return grahas


def body_part_table(number: int) -> dict:
    """One of §26.6's tables, or a refusal naming what is still pending."""
    index = validate.in_range("table", int(number), 65, 69)
    table = BODY_PART_TABLES[index]
    if table is None:
        raise TaraError(
            f"Table {index} of section 26.6 has not been supplied; "
            f"{', '.join(str(n) for n in BODY_PART_TABLES_PENDING)} "
            f"{'is' if len(BODY_PART_TABLES_PENDING) == 1 else 'are'} pending")
    return table


def body_part(graha: str, natal_moon_longitude: float,
              transit_longitude: float) -> dict:
    """Which body part `graha` dwells in, and §26.6's standard result.

    :param graha: the transiting graha's name, matched against the tables'
        own `graha` field.
    """
    for number, table in BODY_PART_TABLES.items():
        if table is not None and graha in _grahas_of(table):
            break
    else:
        pending = ", ".join(str(n) for n in BODY_PART_TABLES_PENDING)
        raise TaraError(
            f"no supplied table of section 26.6 covers {graha!r}; "
            f"Tables {pending} are still pending")

    counted = tara(natal_moon_longitude, transit_longitude)
    row = next(r for r in _rows_of(table)
               if counted["count"] in r["counts"])  # type: ignore[operator]
    return {
        "graha": graha,
        "table": number,
        "table_covers": list(_grahas_of(table)),
        "count": counted["count"],
        "natal_nakshatra": counted["natal_nakshatra"],
        "transit_nakshatra": counted["transit_nakshatra"],
        "part": row["part"],
        "result": row["result"],
        "harm": (None if row["result"] in BODY_PART_NEUTRAL
                 else row["result"] in BODY_PART_HARMS),
        "harm_is_ours": (
            "Section 26.6 prints no good/bad column; `harm` reads the plain "
            "sense of the result and is not the book's grading. It is None "
            "for a result that is an event rather than a verdict"),
        "tara": counted["tara"],
        "tara_grade": counted["grade"],
        "the_two_disagree_often": THE_TWO_TABLES_AGREE_NO_BETTER_THAN_CHANCE,
    }


def grahas_dwelling_in(part: str) -> dict:
    """§26.6's second purpose, run backwards: which grahas dwell in a part.

    Returns every (graha, counts) pair from the tables **supplied so far**,
    and names the ones still pending, because a shortlist drawn from two of
    five tables is not the answer the section promises.
    """
    found = []
    for number, table in BODY_PART_TABLES.items():
        if table is None:
            continue
        for row in _rows_of(table):
            if row["part"] == part:
                found.append({"grahas": list(_grahas_of(table)),
                              "table": number, "counts": row["counts"],
                              "result": row["result"]})
    wanted = _words(part)
    similar = []
    for number, table in BODY_PART_TABLES.items():
        if table is None:
            continue
        for row in _rows_of(table):
            name = str(row["part"])
            if name == part:
                continue
            if wanted & _words(name):
                similar.append({"part": name,
                                "grahas": list(_grahas_of(table)),
                                "table": number})
    return {
        "part": part,
        "grahas": found,
        "similar_parts": similar,
        "tables_supplied": [n for n, t in BODY_PART_TABLES.items()
                            if t is not None],
        "tables_pending": list(BODY_PART_TABLES_PENDING),
        "complete": not BODY_PART_TABLES_PENDING,
        "note": THE_SECOND_PURPOSE_READS_THE_TABLES_BACKWARDS,
        "vocabulary": THE_TABLES_DRAW_EIGHT_PARTS_FROM_A_LARGER_POOL,
    }
