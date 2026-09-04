"""Chapter 25 — transits read against natal reference points.

§25.1 names the vocabulary and §25.2 takes the first and most popular
reference, natal Moon. The seven result tables it promises, Table 53 to Table
59, arrive one at a time; :data:`STANDARD_RESULT_TABLES` tracks which are in.

The house count itself is `charts.house.house_of_rasi` — §7.1's rule, reused
rather than repeated, because a house from janma rasi is a house like any
other.
"""
from __future__ import annotations

from hora.charts.house import house_of_rasi
from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_NAMES, Graha


class GocharaError(validate.InputError):
    """A transit input that cannot be resolved."""


# --------------------------------------------------------------------------
# §25.1 Introduction — the vocabulary
# --------------------------------------------------------------------------

#: §25.1's definition of the moving half.
TRANSIT_MEANS = (
    "By transits or gochaara, we mean the motion of planets in the skies. By "
    "the transit or chaara or gochaara position of a planet, we mean the "
    "position occupied by a planet at a given time."
)

#: And of the fixed half.
NATAL_MEANS = (
    "By the natal or radical or birth or janma position of a planet, we mean "
    "the position occupied by a planet at the time of one's birth."
)

#: The book's own synonyms for each half, in the order §25.1 gives them. Held
#: because the chapter uses them interchangeably and a reader of our output
#: should not have to guess that "chaara" and "gochaara" are the same thing.
TRANSIT_SYNONYMS: tuple[str, ...] = ("transit", "chaara", "gochaara")
NATAL_SYNONYMS: tuple[str, ...] = ("natal", "radical", "birth", "janma")

#: What the chapter does with the two halves, and its own statement of scope.
#: "Several reference points" is the chapter's structure: natal Moon first.
CORRELATION_IS_THE_METHOD = (
    "By correlating the transit positions on a given day with the natal "
    "positions of several reference points, we can draw some conclusions "
    "about the nature of results experienced by the native then. Some methods "
    "normally employed in such correlation will be studied in this chapter."
)


# --------------------------------------------------------------------------
# §25.2 Transits from Moon
# --------------------------------------------------------------------------

#: Why Moon is taken first, and what a transit read from it shows.
MOON_IS_THE_MOST_POPULAR_REFERENCE = (
    "The most popular natal reference in transit analysis is Moon. Moon is "
    "the significator of mind and analysis of planetary positions with "
    "respect to Moon shows the mental state. Depending on the houses occupied "
    "by transit planets with respect to natal Moon, they exert different "
    "influences on one's mental state."
)

#: A cross-link the chapter makes itself, and one that agrees with §24.5:
#: Vimsottari is the dasa that focusses on mind, so its lord's transit is the
#: one that matters most to a reference that also shows mind.
THE_DASA_LORDS_TRANSIT_MATTERS_MOST = (
    "The transit of Vimsottari dasa lord is particularly important, because "
    "he is the one who has the greatest influence on one's mental state "
    "during a period."
)

JANMA_RASI_MEANS = (
    "The rasi occupied by Moon in the natal chart is called \"janma rasi\" and "
    "planets give different results when transiting in different houses from "
    "janma rasi."
)


def janma_rasi(natal_moon_longitude: float) -> int:
    """§25.2's janma rasi — the sign natal Moon occupies."""
    longitude = validate.longitude("natal_moon_longitude",
                                   natal_moon_longitude)
    return int(longitude // 30.0)


def house_from_janma(natal_moon_longitude: float,
                     transit_longitude: float) -> dict:
    """Which house from janma rasi a transiting body occupies.

    The count is §7.1's, so janma rasi itself is the 1st house.
    """
    janma = janma_rasi(natal_moon_longitude)
    sign = int(validate.longitude("transit_longitude", transit_longitude)
               // 30.0)
    return {
        "janma_rasi": janma, "janma_rasi_name": str(RASI_NAMES[janma]),
        "transit_rasi": sign, "transit_rasi_name": str(RASI_NAMES[sign]),
        "house": house_of_rasi(janma, sign),
    }


def houses_from_janma(natal_moon_longitude: float,
                      transit_longitudes: dict[int, float]) -> dict[int, int]:
    """The house from janma rasi for each transiting graha."""
    janma = janma_rasi(natal_moon_longitude)
    return {
        int(graha): house_of_rasi(janma, int(
            validate.longitude(f"transit_longitudes[{graha}]", longitude)
            // 30.0))
        for graha, longitude in transit_longitudes.items()
    }


# --------------------------------------------------------------------------
# §25.2's caveat on its own tables
# --------------------------------------------------------------------------

#: **The rule that governs every table in this section.** The tables give a
#: valence; the natal chart supplies the subject. §25.2 says so before printing
#: a single one of them.
THE_TABLES_ARE_REFERENCE_ONLY = (
    "These results are given only for reference. In reality, not everyone "
    "with the same janma rasi experiences the same results on a given day (or "
    "week or month). The results given by planets depend on what they stand "
    "for in the natal chart."
)

#: §25.2's own illustration, twice over on one transit: Mars in the 8th from
#: janma rasi gives worries either way, and *what* the worries are about comes
#: from the house Mars lords natally.
THE_SUBJECT_COMES_FROM_NATAL_LORDSHIP: tuple[dict[str, object], ...] = (
    {"graha": "Mars", "natal_lordship": 5, "transit_house": 8,
     "result": "worries", "about": "children"},
    {"graha": "Mars", "natal_lordship": 10, "transit_house": 8,
     "result": "worries", "about": "career"},
)

#: **Finding.** This is §18.4's shape again. There the sixteen dasa principles
#: gave a placement's valence and the subject came from the house (OI-122);
#: here the seven transit tables give the valence and the subject comes from
#: natal lordship. Both sections say the table is not the reading.
THE_TABLE_IS_NOT_THE_READING = (
    "§25.2's tables give what a transit does -- worries, gains, illness -- and "
    "never what it is about. The subject comes from what the graha lords in "
    "the natal chart, which is the same division of labour §18.4 makes for "
    "dasas."
)

#: The seven tables §25.2 promises, filled in as each is supplied. A test
#: asserts this matches :data:`STANDARD_RESULTS`, so the section cannot be
#: called finished early or a table registered without being built.
STANDARD_RESULT_TABLES: dict[int, dict[str, object]] = {
    53: {"for": "Sun", "built": True},
    54: {"for": "Moon", "built": True},
    55: {"for": "Mars", "built": True},
    56: {"for": "Mercury", "built": True},
    57: {"for": "Jupiter", "built": True},
    58: {"for": None, "built": False},
    59: {"for": None, "built": False},
}


# --------------------------------------------------------------------------
# Table 53 — Sun's transit from janma rasi
# --------------------------------------------------------------------------

#: The two verdicts the "Snapshot" column uses. Nothing finer is offered, and
#: nothing finer is invented: a house is Good or it is Bad.
SNAPSHOTS: tuple[str, ...] = ("Good", "Bad")

#: Table 53 exactly as printed, in house order.
TABLE_53_SUN: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Bad",
     "results": "Financial loss, many travels, discomfort"},
    {"house": 2, "snapshot": "Bad",
     "results": "Unhappiness, eye troubles, fear"},
    {"house": 3, "snapshot": "Good",
     "results": "Wealth, good health, victory"},
    {"house": 4, "snapshot": "Bad",
     "results": "Marital disharmony, loss of name"},
    {"house": 5, "snapshot": "Bad",
     "results": "Bad health, fear from enemies"},
    {"house": 6, "snapshot": "Good",
     "results": "Success over enemies, good health"},
    {"house": 7, "snapshot": "Bad", "results": "Travels, physical pain"},
    {"house": 8, "snapshot": "Bad",
     "results": "Disease, setbacks in marriage"},
    {"house": 9, "snapshot": "Bad", "results": "Mental worries, obstacles"},
    {"house": 10, "snapshot": "Good", "results": "Success, honors, gains"},
    {"house": 11, "snapshot": "Good",
     "results": "Good health, prosperity, honors"},
    {"house": 12, "snapshot": "Bad", "results": "Expenditure, losses"},
)

#: **Finding.** Sun's four Good houses are the **upachayas** — 3, 6, 10 and 11
#: — exactly, and its eight Bad houses are exactly the rest. §7's upachaya set
#: is defined for natal placement and growth over time; Table 53 never says
#: the word, so the identity is ours and not the book's.
SUNS_GOOD_HOUSES_ARE_THE_UPACHAYAS = (
    "Table 53 marks the 3rd, 6th, 10th and 11th Good and the other eight Bad. "
    "Those four are §7's upachaya houses, which Table 53 does not name."
)

# --------------------------------------------------------------------------
# Table 54 — Moon's transit from janma rasi
# --------------------------------------------------------------------------

#: Table 54 exactly as printed, in house order.
TABLE_54_MOON: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Good", "results": "Comfort, good spirits"},
    {"house": 2, "snapshot": "Bad", "results": "Obstacles, losses"},
    {"house": 3, "snapshot": "Good", "results": "Gains, happiness"},
    {"house": 4, "snapshot": "Bad",
     "results": "Lack of peace of mind, distrust"},
    {"house": 5, "snapshot": "Bad",
     "results": "Failures, disappointments, sadness"},
    {"house": 6, "snapshot": "Good", "results": "Happiness, health, wealth"},
    {"house": 7, "snapshot": "Good", "results": "Respect, gains"},
    {"house": 8, "snapshot": "Bad", "results": "Losses, tension, worries"},
    {"house": 9, "snapshot": "Bad", "results": "Mental uneasiness"},
    {"house": 10, "snapshot": "Good", "results": "Success, gains, authority"},
    {"house": 11, "snapshot": "Good", "results": "Prosperity, comforts, gains"},
    {"house": 12, "snapshot": "Bad",
     "results": "Injuries, expenditure, sadness"},
)

#: **Finding.** Tables 53 and 54 agree on ten of twelve houses and differ only
#: on the **1st and the 7th** — the axis through janma rasi itself. The Sun is
#: Bad in both and the Moon Good in both; every other house has the same
#: verdict in the two tables. So Moon's Good set is Sun's plus that axis, and
#: Sun's four Good houses are a strict subset of Moon's six.
SUN_AND_MOON_DIFFER_ONLY_ON_THE_1_7_AXIS = (
    "Table 53 and Table 54 give the same verdict in ten of twelve houses. The "
    "two exceptions are the 1st and the 7th, Bad for the Sun and Good for the "
    "Moon -- janma rasi itself and the house opposite it."
)

#: **Finding.** The verdicts agreeing does not make the rows copies: where both
#: tables say Good or both say Bad, the typical results are still different
#: words. The 3rd is "Wealth, good health, victory" for the Sun and "Gains,
#: happiness" for the Moon.
AGREEING_SNAPSHOTS_ARE_NOT_THE_SAME_RESULTS = (
    "No house has the same typical results in Tables 53 and 54, including the "
    "ten where the snapshots agree."
)


# --------------------------------------------------------------------------
# Table 55 — Mars's transit from janma rasi
# --------------------------------------------------------------------------

#: Table 55 exactly as printed, in house order.
TABLE_55_MARS: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Bad", "results": "Troubles, bodily afflictions"},
    {"house": 2, "snapshot": "Bad",
     "results": "Accidents, losses, thefts, quarrels"},
    {"house": 3, "snapshot": "Good", "results": "Gains, power, wealth"},
    {"house": 4, "snapshot": "Bad",
     "results": "Stomach problems, fevers, bad health"},
    {"house": 5, "snapshot": "Bad",
     "results": "Troubles from enemies, trouble with children"},
    {"house": 6, "snapshot": "Good",
     "results": "Success over enemies, wealth, success, well-being"},
    {"house": 7, "snapshot": "Bad",
     "results": "Quarrels, marital troubles, eye problems"},
    {"house": 8, "snapshot": "Bad",
     "results": "Worries, accidents, bad name, losses"},
    {"house": 9, "snapshot": "Bad", "results": "Losses, insults, illness"},
    {"house": 10, "snapshot": "Bad",
     "results": "Change of place, unexpected wealth"},
    {"house": 11, "snapshot": "Good", "results": "Authority,  gains, good name"},
    {"house": 12, "snapshot": "Bad",
     "results": "Expenses, quarrels with wife, diseases"},
)

#: **Finding.** Mars in the 10th is the only row in the three tables so far
#: whose results contradict its own snapshot: it is marked **Bad** and reads
#: "Change of place, unexpected wealth". Every other Bad row is unmixed. Held
#: as printed — the snapshot column is a one-word summary and "change of
#: place" may be what it summarises, but the row is not self-consistent and a
#: reader should be told rather than have it smoothed over.
MARS_IN_THE_TENTH_IS_MARKED_BAD_AND_READS_GOOD = (
    "Table 55 marks Mars in the 10th Bad and gives its typical results as "
    "\"Change of place, unexpected wealth\". No other Bad row in Tables 53 to "
    "55 contains a benefit."
)

#: **Finding, and its limit.** Tables 53 to 55 nest — Mars's Good houses are a
#: strict subset of the Sun's, which are a strict subset of the Moon's, with
#: single-house steps. **Table 56 ends it**: Mercury is Good in the 2nd, 4th
#: and 8th, which all three of the others call Bad, and Bad in the 3rd, which
#: all three call Good. So the nesting was a fact about the luminaries and
#: Mars, not about the section.
THE_FIRST_THREE_TABLES_NEST = (
    "Mars {3, 6, 11} is inside Sun {3, 6, 10, 11} is inside Moon "
    "{1, 3, 6, 7, 10, 11}, with single-house steps. Mercury {2, 4, 6, 8, 10, "
    "11} is inside none of them and contains none of them."
)


# --------------------------------------------------------------------------
# Table 56 — Mercury's transit from janma rasi
# --------------------------------------------------------------------------

#: Table 56 exactly as printed, in house order. The 12th's "disease" twice is
#: the book's; see :data:`THE_TWELFTH_ROW_REPEATS_A_WORD`.
TABLE_56_MERCURY: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Bad",
     "results": "Quarrels, imprisonment, losses, poor advice"},
    {"house": 2, "snapshot": "Good", "results": "Success, wealth, gains"},
    {"house": 3, "snapshot": "Bad",
     "results": "Wandering, losses, trouble from authorities"},
    {"house": 4, "snapshot": "Good", "results": "Prosperity in family, gains"},
    {"house": 5, "snapshot": "Bad",
     "results": "Quarrels with wife and children, suffering"},
    {"house": 6, "snapshot": "Good", "results": "Renown, success, ornaments"},
    {"house": 7, "snapshot": "Bad",
     "results": "Quarrels, mental discomfort, addictions"},
    {"house": 8, "snapshot": "Good",
     "results": "Childbirth, happiness, gains, success"},
    {"house": 9, "snapshot": "Bad", "results": "Mental worries, obstacles"},
    {"house": 10, "snapshot": "Good",
     "results": "Money, happiness, domestic harmony, success"},
    {"house": 11, "snapshot": "Good", "results": "Childbirth, happiness, wealth"},
    {"house": 12, "snapshot": "Bad",
     "results": "Disease, domestic disharmony, disease, losses"},
)

#: **Finding.** Mercury's verdicts **alternate** Bad, Good, Bad, Good through
#: the first ten houses — the only table so far with a periodic column — and
#: then stop alternating at the 11th, which is Good where the run would make it
#: Bad. What replaces the pattern is the section's own fixed pair: the 11th is
#: Good and the 12th Bad in every table read so far.
MERCURY_ALTERNATES_FOR_TEN_HOUSES = (
    "Table 56 runs Bad, Good, Bad, Good, Bad, Good, Bad, Good, Bad, Good "
    "through houses 1 to 10, then gives Good to the 11th and Bad to the 12th "
    "-- which is what every other table gives them too."
)

#: **Finding.** The 11th is Good and the 12th Bad in every table read so far,
#: and after five tables they are the **only** two houses left that no table
#: has disagreed about. The 6th survived four tables and fell to Jupiter; the
#: 5th and 9th survived four and fell to the same table.
THE_11TH_AND_12TH_HAVE_NOT_VARIED = (
    "Across Tables 53 to 57 the 11th is Good five times and the 12th Bad five "
    "times. Every other house now has at least one table against it."
)

#: **Book defect.** Table 56's 12th row lists "disease" twice: "Disease,
#: domestic disharmony, disease, losses". Held as printed rather than
#: de-duplicated, because a repeated word may be a printing slip for a second
#: signification we cannot recover. See D-72.
THE_TWELFTH_ROW_REPEATS_A_WORD = (
    "Mercury's 12th reads \"Disease, domestic disharmony, disease, losses\". "
    "No other row in Tables 53 to 56 repeats a word."
)


# --------------------------------------------------------------------------
# Table 57 — Jupiter's transit from janma rasi
# --------------------------------------------------------------------------

#: Table 57 exactly as printed, in house order. The 1st row's mid-sentence
#: capital in "Wandering" is the book's and is kept.
TABLE_57_JUPITER: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Bad",
     "results": "Loss of money and intelligence, Wandering"},
    {"house": 2, "snapshot": "Good",
     "results": "Happiness, domestic harmony, success"},
    {"house": 3, "snapshot": "Bad",
     "results": "Obstacles, loss of position, travels"},
    {"house": 4, "snapshot": "Bad", "results": "Troubles, defeat, losses"},
    {"house": 5, "snapshot": "Good",
     "results": "Childbirth, intelligence, prosperity, wealth"},
    {"house": 6, "snapshot": "Bad",
     "results": "Mental uneasiness, enemies, worries"},
    {"house": 7, "snapshot": "Good",
     "results": "Health, happiness, erotic pleasures, sense of well-being"},
    {"house": 8, "snapshot": "Bad",
     "results": "Disease, imprisonment, illness, grief"},
    {"house": 9, "snapshot": "Good",
     "results": "Success, wealth, childbirth, religiousness"},
    {"house": 10, "snapshot": "Bad",
     "results": "Loss of position and money, ill-health, wandering"},
    {"house": 11, "snapshot": "Good",
     "results": "Recovery of health and position, happiness"},
    {"house": 12, "snapshot": "Bad",
     "results": "Fall from grace, misconduct, grief"},
)

#: **Finding.** Jupiter is the first table to call the **6th** Bad and the
#: first to call the **5th and 9th** Good. Those three were the section's
#: longest-standing agreements — the 6th Good in four tables, the 5th and 9th
#: Bad in four — and one table overturns all three. After it, only the 11th
#: and the 12th remain undisputed.
JUPITER_OVERTURNS_THREE_STANDING_AGREEMENTS = (
    "Table 57 is the first to call the 6th Bad and the first to call the 5th "
    "and 9th Good. All three had held across Tables 53 to 56."
)

#: **Finding.** Jupiter is the section's outlier. It agrees with the Sun, the
#: Moon and Mercury on five houses of twelve each and with Mars on six, while
#: every pair among the other four agrees on six to eleven. On the upachayas
#: it is the Sun's near-opposite: the Sun is Good in all four, Jupiter in the
#: 11th only.
JUPITER_IS_THE_OUTLIER_TABLE = (
    "Table 57 agrees with each of Tables 53, 54 and 56 on five houses of "
    "twelve and with Table 55 on six. Every pair among the other four agrees "
    "on at least six, and Tables 53 and 55 agree on eleven."
)


#: Every supplied table, keyed by graha. Tables 54 to 59 join it as they come.
STANDARD_RESULTS: dict[int, tuple[dict[str, object], ...]] = {
    int(Graha.SUN): TABLE_53_SUN,
    int(Graha.MOON): TABLE_54_MOON,
    int(Graha.MARS): TABLE_55_MARS,
    int(Graha.MERCURY): TABLE_56_MERCURY,
    int(Graha.JUPITER): TABLE_57_JUPITER,
}


def transit_result(graha: int, house: int) -> dict:
    """One row of §25.2's standard results.

    :param house: the house from janma rasi, 1 to 12, as
        :func:`house_from_janma` reports it.
    :raises GocharaError: for a graha whose table has not been supplied — the
        error names it rather than returning a neutral verdict.
    """
    index = validate.in_range("graha", int(graha), 0, 8)
    place = validate.in_range("house", house, 1, 12)
    if index not in STANDARD_RESULTS:
        raise GocharaError(
            f"§25.2's standard results for {GRAHA_NAMES[index]} have not been "
            f"supplied; Table 53 to Table 59 arrive one at a time")
    row = STANDARD_RESULTS[index][place - 1]
    return {
        "graha": index, "graha_name": str(GRAHA_NAMES[index]),
        "house": place,
        "snapshot": row["snapshot"], "results": row["results"],
        "caveat": THE_TABLES_ARE_REFERENCE_ONLY,
    }


def good_houses(graha: int) -> tuple[int, ...]:
    """The houses a graha's table marks Good, in order."""
    index = validate.in_range("graha", int(graha), 0, 8)
    if index not in STANDARD_RESULTS:
        raise GocharaError(
            f"§25.2's standard results for {GRAHA_NAMES[index]} have not been "
            f"supplied")
    return tuple(int(str(row["house"])) for row in STANDARD_RESULTS[index]
                 if row["snapshot"] == "Good")


def read_transits(natal_moon_longitude: float,
                  transit_longitudes: dict[int, float]) -> tuple[dict, ...]:
    """§25.2 applied: each transiting graha's house from janma rasi and the
    standard result for it.

    Grahas whose table has not been supplied are reported with ``undecided``
    rather than dropped, so a caller can see what is missing.
    """
    houses = houses_from_janma(natal_moon_longitude, transit_longitudes)
    out = []
    for graha, house in sorted(houses.items()):
        try:
            row = transit_result(graha, house)
        except GocharaError as missing:
            out.append({
                "graha": graha, "graha_name": str(GRAHA_NAMES[graha]),
                "house": house, "snapshot": None, "results": None,
                "undecided": str(missing),
            })
        else:
            row["undecided"] = None
            out.append(row)
    return tuple(out)

#: §25.2's own sentence naming them, which is the only roadmap Part 3 gives.
#: Part 3's opening named no techniques at all.
SEVEN_TABLES_ARE_PROMISED = (
    "The standard results given in literature are given in Table 53 - Table "
    "59."
)


def agreement(first: int, second: int) -> dict:
    """Where two supplied tables give the same verdict and where they part.

    Useful as Tables 53 to 59 accumulate: the tables are printed one per graha
    and never compared, so any structure across them is ours to find.
    """
    left = validate.in_range("first", int(first), 0, 8)
    right = validate.in_range("second", int(second), 0, 8)
    for graha in (left, right):
        if graha not in STANDARD_RESULTS:
            raise GocharaError(
                f"§25.2's standard results for {GRAHA_NAMES[graha]} have not "
                f"been supplied")

    agree: list[int] = []
    differ: list[int] = []
    for house in range(1, 13):
        a = STANDARD_RESULTS[left][house - 1]["snapshot"]
        b = STANDARD_RESULTS[right][house - 1]["snapshot"]
        (agree if a == b else differ).append(house)
    return {
        "first": left, "first_name": str(GRAHA_NAMES[left]),
        "second": right, "second_name": str(GRAHA_NAMES[right]),
        "agree": tuple(agree), "differ": tuple(differ),
    }


def common_ground() -> dict:
    """Which houses every supplied table agrees on, and which vary.

    §25.2 prints one table per graha and never sets them side by side, so any
    house that behaves the same way in all of them is a fact about the section
    rather than about a graha. ``tables`` says how many were compared, because
    "always" means only "in the tables supplied so far".
    """
    if not STANDARD_RESULTS:
        raise GocharaError("no standard results have been supplied yet")

    always_good, always_bad, varies = [], [], []
    for house in range(1, 13):
        verdicts = {rows[house - 1]["snapshot"]
                    for rows in STANDARD_RESULTS.values()}
        if verdicts == {"Good"}:
            always_good.append(house)
        elif verdicts == {"Bad"}:
            always_bad.append(house)
        else:
            varies.append(house)
    return {
        "tables": len(STANDARD_RESULTS),
        "grahas": tuple(sorted(STANDARD_RESULTS)),
        "always_good": tuple(always_good),
        "always_bad": tuple(always_bad),
        "varies": tuple(varies),
    }
