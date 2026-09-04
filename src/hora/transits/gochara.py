"""Chapter 25 — transits read against natal reference points.

§25.1 names the vocabulary and §25.2 takes the first and most popular
reference, natal Moon. The seven result tables it promises, Table 53 to Table
59, arrive one at a time; :data:`STANDARD_RESULT_TABLES` tracks which are in.

The house count itself is `charts.house.house_of_rasi` — §7.1's rule, reused
rather than repeated, because a house from janma rasi is a house like any
other.
"""
from __future__ import annotations

from collections.abc import Sequence

from hora.charts.house import house_of_rasi
from hora.core import validate
from hora.core.const import GRAHA_NAMES, NAKSHATRA_NAMES, RASI_NAMES, Graha
from hora.core.constants.nakshatra import NAKSHATRA_LORD


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
    58: {"for": "Venus", "built": True},
    59: {"for": "Saturn", "built": True},
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

#: **Finding.** Mars in the 10th is marked **Bad** and reads "Change of place,
#: unexpected wealth". Held as printed — the snapshot column is a one-word
#: summary and "change of place" may be what it summarises, but the row is not
#: self-consistent and a reader should be told rather than have it smoothed
#: over. It was the only such row until Table 58; see :data:`MIXED_ROWS`.
MARS_IN_THE_TENTH_IS_MARKED_BAD_AND_READS_GOOD = (
    "Table 55 marks Mars in the 10th Bad and gives its typical results as "
    "\"Change of place, unexpected wealth\"."
)

#: **Finding.** Rows whose typical results pull against their own snapshot,
#: curated by reading every row rather than by matching words — a lexicon
#: cannot tell "success of enemies" from "success", or "discomfort" from
#: "comfort". Three of the four are Venus's.
MIXED_ROWS: tuple[dict[str, object], ...] = (
    {"graha": "Mars", "house": 10, "snapshot": "Bad",
     "against_it": "unexpected wealth"},
    {"graha": "Venus", "house": 4, "snapshot": "Good",
     "against_it": "success of enemies"},
    {"graha": "Venus", "house": 10, "snapshot": "Bad",
     "against_it": "Virtuous acts"},
    {"graha": "Venus", "house": 12, "snapshot": "Bad",
     "against_it": "New friends, money, pleasures, gains -- the whole row"},
    {"graha": "Saturn", "house": 2, "snapshot": "Bad", "against_it": "wealth"},
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
    "Across Tables 53 to 58 the 11th is Good six times and the 12th Bad six "
    "times. They are the only two houses no table disagrees about."
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

#: **Finding.** The six tables fall into two groups, and Jupiter and Venus have
#: **identical** agreement profiles against the other four — five houses each
#: with the Sun, the Moon and Mercury, six with Mars — while agreeing with each
#: other on eight. Every cross-group pair scores 5 or 6; every pair inside
#: {Sun, Moon, Mars, Mercury} scores 6 to 11.
#:
#: Read against Table 57 alone this looked like Jupiter being an outlier. Venus
#: shows it is a **pair**: the two great benefics against the rest.
THE_TWO_BENEFICS_FORM_A_PAIR = (
    "Tables 57 and 58 agree with Tables 53, 54 and 56 on five houses each and "
    "with Tables 55 and 59 on six -- the same five numbers -- and with each "
    "other on eight. No cross-group pair exceeds six."
)

#: The grouping the agreement scores fall into, ours and not the book's.
#: Mercury is a natural benefic and sits with the first group, so this is not
#: the benefic/malefic split.
TABLE_GROUPS: tuple[tuple[str, ...], ...] = (
    ("Sun", "Moon", "Mars", "Mercury", "Saturn"),
    ("Jupiter", "Venus"),
)


# --------------------------------------------------------------------------
# Table 58 — Venus's transit from janma rasi
# --------------------------------------------------------------------------

#: Table 58 exactly as printed, in house order.
TABLE_58_VENUS: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Good",
     "results": "Comforts, pleasures, happiness, good spirits"},
    {"house": 2, "snapshot": "Good",
     "results": "Money, fortune, erotic pleasures, childbirth"},
    {"house": 3, "snapshot": "Good", "results": "Respect, wealth, good spirits"},
    {"house": 4, "snapshot": "Good",
     "results": "Prosperity, success of enemies, comforts"},
    {"house": 5, "snapshot": "Good", "results": "Fame, power, good name"},
    {"house": 6, "snapshot": "Bad",
     "results": "Loss of fame, bad name, quarrels"},
    {"house": 7, "snapshot": "Bad", "results": "Humiliation, disease, troubles"},
    {"house": 8, "snapshot": "Bad",
     "results": "Fears, mental worries, injuries, troubles from women"},
    {"house": 9, "snapshot": "Good",
     "results": "Fortune, luxuries, marital happiness"},
    {"house": 10, "snapshot": "Bad",
     "results": "Virtuous acts, troubles, unpleasant events, disgrace"},
    {"house": 11, "snapshot": "Good",
     "results": "Gains, happiness, prosperity, comforts"},
    {"house": 12, "snapshot": "Bad",
     "results": "New friends, money, pleasures, gains"},
)

#: **Finding.** Venus is the most generous table — seven Good houses against
#: the Moon's and Mercury's six — and the only one whose Good houses open with
#: an unbroken run, the 1st to the 5th.
VENUS_IS_THE_MOST_GENEROUS_TABLE = (
    "Table 58 marks the 1st, 2nd, 3rd, 4th, 5th, 9th and 11th Good. No other "
    "table has seven, and none other opens with five Good houses in a row."
)

#: **Finding.** Venus's 12th keeps the verdict every table gives the 12th and
#: contradicts it in the same row: **Bad**, reading "New friends, money,
#: pleasures, gains" — four items, none of them a harm. So the section's last
#: undisputed house survives as a verdict and is undercut as a reading, in the
#: table that supplies it.
THE_TWELFTH_IS_BAD_EVERYWHERE_AND_READS_WELL_HERE = (
    "The 12th is Bad in all six tables read so far. Table 58's 12th row is "
    "the only one of the six whose typical results contain no harm at all."
)


# --------------------------------------------------------------------------
# Table 59 — Saturn's transit from janma rasi, and the nodes
# --------------------------------------------------------------------------

#: Table 59 exactly as printed, in house order.
TABLE_59_SATURN: tuple[dict[str, object], ...] = (
    {"house": 1, "snapshot": "Bad",
     "results": "Fear of incarceration, worries, foreign trips"},
    {"house": 2, "snapshot": "Bad",
     "results": "Physical weakness, discomfort, wealth, unhappiness"},
    {"house": 3, "snapshot": "Good",
     "results": "Wealth, health, happiness, all-round success"},
    {"house": 4, "snapshot": "Bad",
     "results": "Stomach problems, wickedness, separation from family"},
    {"house": 5, "snapshot": "Bad",
     "results": "Separation from children, uneasiness, quarrels"},
    {"house": 6, "snapshot": "Good",
     "results": "Freedom from disease and enemies, success"},
    {"house": 7, "snapshot": "Bad",
     "results": "Wandering, quarrels with spouse, trouble from authorities"},
    {"house": 8, "snapshot": "Bad",
     "results": "Suffering, loss of status and balance, imprisonment"},
    {"house": 9, "snapshot": "Bad",
     "results": "Diseases, suffering, loss of status"},
    {"house": 10, "snapshot": "Bad",
     "results": "Loss of money, bad name, changes in career, laziness"},
    {"house": 11, "snapshot": "Good", "results": "Wealth, success, gains"},
    {"house": 12, "snapshot": "Bad",
     "results": "Grief, misery, losses, ill-health, frustration"},
)

#: **Finding.** Tables 55 and 59 have **identical** snapshot columns — Mars and
#: Saturn agree on all twelve houses, the only pair in the section to do so.
#: Their typical results differ throughout, so it is the verdicts alone that
#: coincide.
MARS_AND_SATURN_HAVE_THE_SAME_VERDICTS = (
    "Table 55 and Table 59 give the same Good or Bad in every one of the "
    "twelve houses, and no other pair of tables agrees on more than eleven. "
    "No house has the same typical results in both."
)

#: §25.2's closing sentence, which places the two grahas that get no table.
RAHU_AND_KETU_HAVE_NO_TABLE_OF_THEIR_OWN = (
    "Rahu's behavior is similar to that of Saturn's and Ketu's behavior to "
    "Mars's."
)

#: The mapping that sentence gives. Read through
#: :func:`transit_result`, which marks the result as an analogy rather than
#: passing off Saturn's row as Rahu's.
NODES_FOLLOW: dict[int, int] = {
    int(Graha.RAHU): int(Graha.SATURN),
    int(Graha.KETU): int(Graha.MARS),
}

#: **Finding.** Because Mars and Saturn share a verdict column, the analogy
#: gives Rahu and Ketu the same Good houses as each other — the 3rd, 6th and
#: 11th — and all four of the section's malefics end up with one set. The book
#: does not point this out; it follows from the two facts side by side.
THE_FOUR_MALEFICS_SHARE_ONE_GOOD_SET = (
    "Mars, Saturn, and through §25.2's analogy Rahu and Ketu, are Good in the "
    "3rd, 6th and 11th and Bad in the other nine."
)

#: **Gap.** "Similar" is not "identical", and §25.2 says nothing about where
#: the nodes depart from their models. The typical results returned for a node
#: are the model's own words, so they are marked with the graha they came from
#: and the book's hedge rather than presented as the node's.
SIMILAR_IS_NOT_IDENTICAL = (
    "§25.2 gives the nodes no table and no list of differences. A node's "
    "result here is its model's, carried across under the book's own word "
    "\"similar\"."
)


#: Every supplied table, keyed by graha. Tables 54 to 59 join it as they come.
STANDARD_RESULTS: dict[int, tuple[dict[str, object], ...]] = {
    int(Graha.SUN): TABLE_53_SUN,
    int(Graha.MOON): TABLE_54_MOON,
    int(Graha.MARS): TABLE_55_MARS,
    int(Graha.MERCURY): TABLE_56_MERCURY,
    int(Graha.JUPITER): TABLE_57_JUPITER,
    int(Graha.VENUS): TABLE_58_VENUS,
    int(Graha.SATURN): TABLE_59_SATURN,
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
    source = NODES_FOLLOW.get(index, index)
    if source not in STANDARD_RESULTS:
        raise GocharaError(
            f"§25.2's standard results for {GRAHA_NAMES[index]} have not been "
            f"supplied; Table 53 to Table 59 arrive one at a time")
    row = STANDARD_RESULTS[source][place - 1]
    return {
        "graha": index, "graha_name": str(GRAHA_NAMES[index]),
        "house": place,
        "snapshot": row["snapshot"], "results": row["results"],
        "from_graha": None if source == index else source,
        "from_graha_name": None if source == index else str(GRAHA_NAMES[source]),
        "analogy": None if source == index else "similar",
        "caveat": THE_TABLES_ARE_REFERENCE_ONLY,
    }


def good_houses(graha: int) -> tuple[int, ...]:
    """The houses a graha's table marks Good, in order."""
    index = validate.in_range("graha", int(graha), 0, 8)
    source = NODES_FOLLOW.get(index, index)
    if source not in STANDARD_RESULTS:
        raise GocharaError(
            f"§25.2's standard results for {GRAHA_NAMES[index]} have not been "
            f"supplied")
    return tuple(int(str(row["house"])) for row in STANDARD_RESULTS[source]
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


# --------------------------------------------------------------------------
# Example 103 — a transit chart read against a Gemini janma rasi
# --------------------------------------------------------------------------

#: **Finding.** §25.2 said the subject of a transit comes from "what they
#: stand for in the natal chart" and illustrated it with lordship alone.
#: Example 103 uses **three** sources, and one of them is not natal at all:
#: the houses a graha *rules*, the houses it *occupies*, and its **karakatva**
#: — its natural signification, which is the same for every chart.
THE_SUBJECT_COMES_FROM_THREE_THINGS = (
    "The native may have gains in the matters signified by the houses ruled "
    "and occupied by Jupiter and Saturn in natal rasi chart and natal "
    "divisional charts. Because Jupiter signifies children and tradition and "
    "Saturn signifies livelihood, the gains may also be related to children, "
    "traditional cermemonies, livelihood etc."
)

#: The karakatvas Example 103 leans on, as it gives them.
EXAMPLE_103_KARAKATVAS: tuple[dict[str, str], ...] = (
    {"graha": "Jupiter", "signifies": "children and tradition"},
    {"graha": "Saturn", "signifies": "livelihood"},
    {"graha": "Sun", "signifies": "authorities and health"},
)

#: **Finding.** Example 103 also lets the table's verdict be **softened**,
#: which no earlier rule allowed. Mercury in janma rasi draws Table 56's
#: harshest row, and the example sets it aside because Mercury is in its own
#: sign: the transiting graha's dignity **in the sign it is transiting**
#: changes the reading. §25.2's caveat gave the subject; this changes the
#: substance.
DIGNITY_IN_THE_TRANSITED_SIGN_SOFTENS_THE_RESULT = (
    "Mercury is in janma rasi (Ge). This suggests \"quarrels, imprisonment, "
    "losses, poor advice\". However, Mercury is strong being in own house "
    "(intellectual Gemini). So the results may be intellectual debates and "
    "arguments."
)

#: Example 103's three worked readings, in the order it gives them.
EXAMPLE_103_READINGS: tuple[dict[str, object], ...] = (
    {"grahas": ("Jupiter", "Saturn"), "rasi": "Aries", "house": 11,
     "snapshot": "Good", "reading": "gains"},
    {"grahas": ("Sun",), "rasi": "Taurus", "house": 12, "snapshot": "Bad",
     "reading": "expenditure and losses"},
    {"grahas": ("Mercury",), "rasi": "Gemini", "house": 1, "snapshot": "Bad",
     "reading": "intellectual debates and arguments"},
)

#: §25.2's closing instruction, and the plainest statement of what the seven
#: tables are for.
ADAPT_THEM_INTELLIGENTLY = (
    "In this manner, we can analyze transits of all the planets. We can use "
    "the results given in literature, but we should adapt them intelligently "
    "to the chart at hand. We should understand what each planet stands for "
    "in a chart."
)

#: The forward pointer that closes §25.2 and opens the rest of the chapter.
THERE_ARE_OTHER_NATAL_REFERENCES = (
    "In addition, there are natal references other than Moon, though Moon is "
    "the most important natal reference when interpreting transits."
)


# --------------------------------------------------------------------------
# §25.3 Other natal references
# --------------------------------------------------------------------------

#: §25.1 promised "several reference points" and §25.2 gave one. This is the
#: rest, each with what §25.3 says it stands for. ``computable`` says whether
#: the reference itself can be produced today — sahams cannot; the book calls
#: them a Tajaka topic and defers them.
OTHER_REFERENCES: tuple[dict[str, object], ...] = (
    {"reference": "lagna",
     "stands_for": "the hub of vitality and one's personality",
     "computable": True},
    {"reference": "paaka lagna", "stands_for": "the physical self",
     "computable": True},
    {"reference": "natal houses", "stands_for": "the matters of that house",
     "computable": True},
    {"reference": "natal planets",
     "stands_for": "what each planet stands for in the chart",
     "computable": True},
    {"reference": "arudha padas",
     "stands_for": "the appearance of their houses' matters",
     "computable": True},
    {"reference": "sahams", "stands_for": "significant points in the zodiac",
     "computable": False},
)

#: §25.3's opening, and its use of the ashtakavarga — from **lagna**, where
#: §25.2 read everything from janma rasi.
ASHTAKAVARGA_JUDGES_A_TRANSIT_FROM_LAGNA = (
    "We can analyze transits with respect to lagna and paaka lagna. Lagna is "
    "the hub of vitality and one's personality in a chart. Using the "
    "ashtakavarga tables, we can decipher whether the transit of a planet in "
    "a house from lagna is favorable or not."
)

#: **The section's master rule**, and the only sentence §25.3 sets in bold.
THE_MASTER_RULE = (
    "A planet occupying or aspecting a rasi in transit influences the matters "
    "signified by the houses and planets stationed in that rasi in the natal "
    "chart."
)

#: And its qualifier, which is §25.2's caveat again in another form.
THE_NATURE_OF_THE_INFLUENCE = (
    "The exact nature of the influence exerted by a planet depends on its "
    "inherent nature and the matters it stands for in the natal chart."
)


def influenced_rasis(graha: int, transit_sign: int) -> dict:
    """The rasis a transiting graha reaches — the one it occupies and the ones
    it aspects, which is what :data:`THE_MASTER_RULE` puts together.
    """
    from hora.charts.aspects import graha_aspects_sign

    index = validate.in_range("graha", int(graha), 0, 8)
    sign = validate.in_range("transit_sign", transit_sign, 0, 11)
    aspected = tuple(other for other in range(12)
                     if other != sign
                     and graha_aspects_sign(index, sign, other))
    return {
        "graha": index, "graha_name": str(GRAHA_NAMES[index]),
        "occupies": sign, "occupies_rasi": str(RASI_NAMES[sign]),
        "aspects": aspected,
        "reaches": (sign, *aspected),
    }


def influences(graha: int, transit_sign: int, lagna_sign: int,
               natal_signs: dict[int, int] | None = None) -> tuple[dict, ...]:
    """§25.3's master rule, applied: for each rasi a transiting graha reaches,
    the natal house it is and the natal grahas standing in it.

    :param natal_signs: graha -> sign in the **natal** chart. Omitted means
        the houses are reported and the planets are not.
    """
    reach = influenced_rasis(graha, transit_sign)
    lagna = validate.in_range("lagna_sign", lagna_sign, 0, 11)
    occupants: dict[int, list[int]] = {}
    for body, sign in (natal_signs or {}).items():
        occupants.setdefault(
            validate.in_range("natal_signs", int(sign), 0, 11), []).append(
                int(body))

    out = []
    for sign in reach["reaches"]:
        standing = sorted(occupants.get(sign, []))
        out.append({
            "rasi": sign, "rasi_name": str(RASI_NAMES[sign]),
            "how": "occupies" if sign == reach["occupies"] else "aspects",
            "natal_house": house_of_rasi(lagna, sign),
            "natal_grahas": tuple(standing),
            "natal_graha_names": tuple(str(GRAHA_NAMES[g]) for g in standing),
        })
    return tuple(out)


#: §25.3's four worked illustrations, in the order it gives them. The first
#: two are occupation and the last two are aspect.
EXAMPLE_TRANSITS: tuple[dict[str, object], ...] = (
    {"graha": "Jupiter", "transits": "Ta", "lagna": "Sc", "how": "occupies",
     "house": 7, "gives": "marriage"},
    {"graha": "Saturn", "transits": "Ar", "lagna": "Li", "how": "occupies",
     "house": 7, "gives": "relationship problems or marital problems"},
    {"graha": "Jupiter", "transits": "Vi", "lagna": "Sc", "how": "aspects",
     "house": 7, "gives": "marriage"},
    {"graha": "Jupiter", "transits": "Vi", "lagna": "Sc", "how": "aspects",
     "house": 7, "also_reaches": "natal Venus in Pi", "gives": "marriage"},
)

#: §25.3's two illustrations of the qualifier, both keyed on natal lordship.
NATAL_LORDSHIP_EXAMPLES: tuple[dict[str, object], ...] = (
    {"natal_lord_of": 5, "in_transit": "occupies the 8th house from natal "
                                       "lagna",
     "expect": "some troubles related to children"},
    {"graha": "Mars", "natal_lord_of": 8,
     "in_transit": "aspects the rasis occupied by Venus and the 7th lord",
     "expect": "some disturbances in marital life"},
)

#: **Finding.** §25.3 gives three self-points and a different harm for each: a
#: malefic in **janma rasi** troubles the mind, in **natal lagna** the vitality,
#: in **paaka lagna** the body. The three references the chapter reads the
#: native's own self through are thus mind, life-force and flesh — and the
#: paaka-lagna half agrees word for word with what §7.3.5 said paaka lagna
#: shows, eighteen chapters earlier.
MALEFIC_OVER_THE_THREE_SELF_POINTS: tuple[dict[str, str], ...] = (
    {"reference": "janma rasi", "gives": "mental worries"},
    {"reference": "natal lagna",
     "gives": "may affect the vitality of the native and create obstacles in "
              "his efforts"},
    {"reference": "paaka lagna", "gives": "bodily complaints"},
)

THE_THREE_SELF_POINTS_DIVIDE_MIND_VITALITY_AND_BODY = (
    "A malefic transiting janma rasi troubles the mind, natal lagna the "
    "vitality, paaka lagna the body. §25.3 says paaka lagna \"explicitly "
    "stands for the physical self\", which is what §7.3.5 already said."
)

#: §25.3's arudha-pada transits, and the two it names.
ARUDHA_PADA_TRANSITS = (
    "Similarly planets occupying or aspecting arudha padas in transit may "
    "give relevant results. For example, Saturn's transit in A10 can be bad "
    "for career, Jupiter's transit in A9 is good for fortune."
)

ARUDHA_PADA_TRANSIT_EXAMPLES: tuple[dict[str, object], ...] = (
    {"graha": "Saturn", "pada": "A10", "house": 10, "reading": "bad for career"},
    {"graha": "Jupiter", "pada": "A9", "house": 9,
     "reading": "good for fortune"},
)

#: §25.3's saham rules, which we cannot compute.
SAHAMS_ARE_USEFUL = (
    "Sahams are useful in transit analysis. Sahams are the significant points "
    "in the zodiac. For example, when the 7th lord or Venus transits close to "
    "vivaha saham, one may get married. When the 6th lord or 8th lord or Mars "
    "or Rahu transits close to kali saham, one may have an accident."
)

SAHAM_TRANSIT_EXAMPLES: tuple[dict[str, object], ...] = (
    {"saham": "vivaha", "transiting": ("the 7th lord", "Venus"),
     "gives": "marriage"},
    {"saham": "kali",
     "transiting": ("the 6th lord", "the 8th lord", "Mars", "Rahu"),
     "gives": "an accident"},
)

#: **Gap.** Two things stop the saham rules being built. Sahams are a Tajaka
#: topic the book defers to a later part, so neither vivaha saham nor kali
#: saham can be computed here; and "transits **close to**" is given no orb, so
#: even with the point we would not know how near is near. Both must arrive
#: before this is more than recorded. See OI-116.
SAHAM_TRANSITS_NEED_TAJAKA_AND_AN_ORB = (
    "§25.3 reads transits against vivaha saham and kali saham. Sahams are "
    "deferred to the Tajaka part and are not computed, and \"close to\" is "
    "given no orb."
)


# --------------------------------------------------------------------------
# Example 104 — a wedding read against four natal reference points
# --------------------------------------------------------------------------

#: Example 104's four natal reference points for a marriage, and what makes
#: each one a reference. It is §25.3's list applied: a house, that house's
#: lord, a karaka, and a saham.
EXAMPLE_104_REFERENCE_POINTS: tuple[dict[str, str], ...] = (
    {"point": "the 7th house", "at": "Virgo", "why": "marriage is its matter"},
    {"point": "the 7th lord", "at": "Cancer", "why": "Mercury lords Virgo"},
    {"point": "Venus", "at": "Leo", "why": "the significator of marriage"},
    {"point": "vivaha saham", "at": "1 Cp", "why": "the saham of marriage"},
)

#: And the rule that makes them worth listing.
INFLUENCE_THESE_AND_THEY_CAN_GIVE_MARRIAGE = (
    "If important planets influence these reference points in transit, they "
    "can give marriage."
)

#: Why Jupiter's transit is the one watched, which is two reasons and not one.
JUPITER_TIMES_AUSPICIOUS_EVENTS = (
    "Jupiter is a natural benefic and also lagna lord here. His transit is "
    "important for timing auspicious events."
)

#: Example 104's four transit hits, in the order it gives them. Every one is
#: :data:`THE_MASTER_RULE` — a transiting graha occupying or aspecting a rasi
#: that holds a natal reference point.
EXAMPLE_104_HITS: tuple[dict[str, object], ...] = (
    {"transiting": "Jupiter", "in": "Pi", "how": "aspects", "reaches": "Vi",
     "which_is": "the natal 7th house"},
    {"transiting": "Jupiter", "in": "Pi", "how": "aspects", "reaches": "Cn",
     "which_is": "the rasi of the natal 7th lord"},
    {"transiting": "Mercury", "in": "Cp", "how": "aspects", "reaches": "Cn",
     "which_is": "his own natal rasi"},
    {"transiting": "Venus", "in": "Aq", "how": "aspects", "reaches": "Le",
     "which_is": "his own natal rasi"},
)

#: **Finding.** Two of the four hits are a graha aspecting **its own natal
#: position** — Mercury from Capricorn onto Cancer, Venus from Aquarius onto
#: Leo. §25.3's master rule covers it without saying so, a natal planet being
#: one of the things stationed in a rasi; Example 104 is where it is used.
A_GRAHA_CAN_ASPECT_ITS_OWN_NATAL_POSITION = (
    "Transit Mercury aspected Cn, the rasi he occupies in the natal chart, "
    "and transit Venus aspected his own natal Leo. Both are the seventh "
    "aspect, which every graha has."
)

#: **Finding.** The saham half of Example 104 is the one thing in it we cannot
#: check. The book prints vivaha saham at 1 Cp and says transit Mercury stood
#: "about 1° away"; our Mercury is at about 2.5 Cp on the day, so the gap is
#: 1.4° to 1.5° — consistent with a saham printed to the whole degree, and not
#: a confirmation, because we cannot compute the saham to compare against.
THE_SAHAM_CLAIM_IS_CONSISTENT_BUT_UNCHECKED = (
    "Transit Mercury is at about 2.5 Cp through the wedding window, so it "
    "stands 1.4° to 1.5° from a vivaha saham printed at 1 Cp. The book says "
    "\"about 1° away\". The saham itself is not computed."
)


# --------------------------------------------------------------------------
# §25.4 Transits and divisional charts — PVR's own research
# --------------------------------------------------------------------------

#: **Provenance, and the only section in the book to carry one.** §25.4 says
#: outright that it is not classical. Recorded because it changes what a
#: disagreement with this section would mean, not what we implement — see
#: docs/precedence.md.
SECTION_25_4_IS_THE_AUTHORS_OWN_RESEARCH = (
    "Though the motivation for the approach described here comes from some "
    "principles described in classics, the actual approach is essentially "
    "based on this author's own researches."
)

#: The tradition it may or may not touch. The book does not claim the link.
BHRIGU_TRANSITS = (
    "This author heard about \"Bhrigu transits\", which correlate the transit "
    "positions in navamsa chart with the natal positions in rasi chart. "
    "However, he does not know much about the tradition of Bhrigu transits to "
    "conclude whether or not his findings are loosely related to that "
    "tradition."
)

#: Why it is taught anyway, and the caution attached to it.
WHY_IT_IS_TAUGHT_ANYWAY = (
    "Though this author prefers to teach only those approaches that have the "
    "sanction of maharshis, he finds this particular approach superior to "
    "most other techniques of transit analysis. Moreover, this approach does "
    "not violate any teachings of maharshis. This is also a fertile area for "
    "research and deserves our attention. Hence it will be covered here."
)

THE_AUTHORS_OWN_CAVEAT = (
    "Readers are advised to keep in mind that what follows is a product of "
    "the very limited intelligence of this author and hence prone to errors. "
    "Readers are encouraged to question and to conduct further researches in "
    "this area."
)

#: Footnote 69's definition of a phrase §25.3 and §25.4 both use without it.
FOOTNOTE_69 = (
    "We say that \"Jupiter transits over Venus\", if Jupiter, in his transit, "
    "occupies the rasi occupied by Venus in the natal chart."
)


def transits_over(transit_sign: int, natal_sign: int) -> bool:
    """Footnote 69 — whether a transiting graha "transits over" a natal one.

    Occupation only: the aspect cases of :data:`THE_MASTER_RULE` are a
    different relation, and the footnote defines the narrower one.
    """
    return (validate.in_range("transit_sign", transit_sign, 0, 11)
            == validate.in_range("natal_sign", natal_sign, 0, 11))


#: **§25.4's whole argument, in one move.** Every divisional chart is drawn on
#: the same zodiac, so a sign in a natal varga and the same sign in the transit
#: rasi chart are one sign — and a transit that can reach what stands in that
#: sign in the rasi chart can reach what stands in it in any varga.
ONE_ZODIAC_FOR_EVERY_DIVISIONAL_CHART = (
    "We do not have different zodiacs for different divisional charts. All "
    "the divisional charts use the same zodiac. So Cancer in natal navamsa "
    "chart and Cancer in transit rasi chart are not different. They are one "
    "and the same. If Jupiter transiting in Cancer can influence the house "
    "and planets stationed in Cancer in rasi chart, he should be able to "
    "influence the house and planets stationed in Cancer in navamsa chart "
    "too! We can extend this logic to all the divisional charts."
)

#: The two axes §25.4 sets up, which is what makes four combinations.
THE_TWO_AXES: tuple[dict[str, str], ...] = (
    {"axis": "rasi vs divisional",
     "rasi": "everything that exists at the physical level",
     "divisional": "various areas of life",
     "interaction": "how events in various areas of life materialize at the "
                    "physical level"},
    {"axis": "natal vs transit", "natal": "the innate potential",
     "transit": "the temporary influences",
     "interaction": "how temporary influences convert innate potential into "
                    "actions and life events"},
)

#: The two of the four combinations §25.4 calls most important — the **crossed**
#: pairs. It never mentions natal-rasi against transit-rasi, which is §25.2 and
#: §25.3, nor natal-varga against transit-varga at all.
THE_TWO_IMPORTANT_INTERACTIONS: tuple[dict[str, object], ...] = (
    {"number": 1, "natal": "a natal divisional chart",
     "transit": "the transit rasi chart",
     "shows": "how innate potential in a particular area of life is "
              "influenced at a given time to result in action at the "
              "physical level",
     "timing": "coarse"},
    {"number": 2, "natal": "the natal rasi chart",
     "transit": "a transit divisional chart",
     "shows": "how the potential at the physical level is transformed into an "
              "event in a particular area of life",
     "timing": "fine-tune"},
)

#: **Finding.** §25.4 says (1) gives coarse timing and (2) fine-tunes it, and
#: never says why. The reason is arithmetic: a transit **rasi** sign changes
#: once in 30° of a graha's motion, while a transit **D-9** sign changes every
#: 3°20' — nine times as often, and a D-60 sign sixty times. So the chart that
#: moves in (2) resolves time N times finer than the chart that moves in (1),
#: where N is the varga's divisor.
WHY_THE_SECOND_INTERACTION_FINE_TUNES = (
    "In interaction (1) the moving chart is the transit rasi chart, whose "
    "signs change once per 30 degrees of motion. In (2) it is a transit "
    "divisional chart, whose signs change every 30/N degrees. The second "
    "therefore resolves time N times more finely, N being the divisor."
)


def divisional_interaction(interaction: int, graha: int, transit_sign: int,
                           natal_lagna: int, natal_signs: dict[int, int],
                           *, varga_code: str) -> dict:
    """§25.4's two interactions, which are :func:`influences` given a varga on
    one side or the other.

    :param interaction: 1 for a natal divisional chart against the transit
        rasi chart, 2 for the natal rasi chart against a transit divisional
        chart.
    :param transit_sign: the transiting graha's sign **in whichever chart the
        interaction moves in** — the rasi chart for (1), the varga for (2).
    :param natal_lagna, natal_signs: the natal side, likewise in the varga for
        (1) and in the rasi chart for (2).

    The caller supplies both sides already reduced to signs, because §25.4's
    point is that a sign is a sign: there is one zodiac, so no conversion
    happens here. What this adds over :func:`influences` is the label — which
    interaction it is, and how finely it times.
    """
    if interaction not in (1, 2):
        raise GocharaError(
            f"§25.4 names two interactions, 1 and 2; got {interaction!r}")
    row = THE_TWO_IMPORTANT_INTERACTIONS[interaction - 1]
    return {
        "interaction": interaction,
        "natal": row["natal"], "transit": row["transit"],
        "shows": row["shows"], "timing": row["timing"],
        "varga": varga_code,
        "reaches": influences(graha, transit_sign, natal_lagna, natal_signs),
    }


# --------------------------------------------------------------------------
# Example 105 — a wedding read from the natal navamsa
# --------------------------------------------------------------------------

#: **A navamsa-specific reading rule**, given nowhere else. The 9th lord is
#: read in *every* chart as the lord of dharma; §25.4 says that in the navamsa
#: it is the one to look at, because the navamsa is the chart of dharma.
THE_NINTH_LORD_IN_NAVAMSA_SHOWS_THE_DHARMA_FOLLOWED = (
    "When we look at navamsa, we should look at the 9th lord. The 9th lord in "
    "navamsa shows the dharma followed. In Hindu life, the marriage ceremony "
    "is an act of dharma."
)

#: Example 105's four transit hits. Every one is §25.4's interaction (1) — a
#: transit **rasi** position landing on a natal **navamsa** position — and
#: none of them would be visible in the rasi chart alone.
EXAMPLE_105_HITS: tuple[dict[str, object], ...] = (
    {"transiting": "Jupiter", "in": "Pi", "how": "occupies",
     "navamsa_point": "the 7th house", "note": "and in his own sign"},
    {"transiting": "Jupiter", "in": "Pi", "how": "aspects",
     "navamsa_point": "Vi, the navamsa lagna", "note": None},
    {"transiting": "Venus", "in": "Aq", "how": "occupies",
     "navamsa_point": "the rasi of Jupiter, the navamsa 7th lord",
     "note": "Venus lords the navamsa 9th, so he shows dharma"},
    {"transiting": "Moon", "in": "Ar", "how": "occupies",
     "navamsa_point": "the navamsa upapada",
     "note": "Moon lords the navamsa 11th, so he shows gains"},
    {"transiting": "Mercury", "in": "Cp", "how": "occupies",
     "navamsa_point": "his own navamsa rasi",
     "note": "Mercury lords the navamsa lagna"},
)

#: §25.4's summary of the same, numbered as it numbers them.
EXAMPLE_105_SUMMARY: tuple[str, ...] = (
    ("Jupiter is in Pi in transit rasi chart and aspects Vi. Lagna is in Vi "
     "and the 7th house is in Pi in the natal navamsa chart."),
    ("Venus is the significator of marriage and the lord of the 9th house "
     "(dharma) in natal navamsa. He is in Aq in the transit rasi chart. The "
     "7th lord Jupiter occupies Aq in the natal navamsa chart."),
    ("Mercury is the lord of lagna and occupies Cp, in the natal navamsa "
     "chart. He is in Cp in the transit rasi chart also."),
)

#: **Finding.** Charts 53 and 54 print **the same transit chart**: the same
#: date, and every graha, the Ascendant and the AL identical. Chart 53 gave a
#: date only; Chart 54 gives 9:30 am IST at 78 E 30, 17 N 20, which falls
#: inside the window Chart 53's own diagram implied. The natural reading is
#: that Examples 104 and 105 are the bride and the groom of one wedding. The
#: book never says so, and two charts being identical does not prove it.
EXAMPLES_104_AND_105_SHARE_A_WEDDING_CHART = (
    "Chart 53's transit chart and Chart 54's are the same chart. Chart 54 "
    "supplies the time and place Chart 53 withheld, and it lies inside the "
    "window Chart 53's Ascendant and AL already implied."
)

#: **Finding, superseded.** Examples 104, 105 and 106 all work interaction (1)
#: — a transit rasi position against a natal chart, in the D-1, D-9 and D-7
#: respectively. Through those three it looked as though the fine-tuning half
#: was described and never demonstrated. **Example 107 demonstrates it**; see
#: :data:`INTERACTION_2_IS_WORKED_ONCE`.
INTERACTION_1_CARRIES_THE_FIRST_THREE_EXAMPLES = (
    "Examples 104, 105 and 106 each read a transit rasi position against a "
    "natal chart -- the rasi chart, the D-9 and the D-7 in turn. All three "
    "are interaction (1)."
)


# --------------------------------------------------------------------------
# Example 106 — a birth read from the natal D-7; Chart 55 not yet supplied
# --------------------------------------------------------------------------

#: What the D-7 is read for, stated here rather than in §25.4's own text.
D7_SHOWS = "D-7 shows children and happiness from them."

#: **Chart 55 has not been printed.** Everything Example 106 states about it,
#: so the chart can be checked against its own example when it arrives rather
#: than merely transcribed.
EXAMPLE_106_AWAITS_CHART_55: tuple[str, ...] = (
    ("The natal D-7 of a gentleman, and the transit rasi chart at the birth "
     "of his daughter."),
    "The 5th house of the D-7 is Virgo, so the D-7 lagna is Taurus.",
    ("Natal D-7: Jupiter and Mercury both occupy Virgo, and Mercury is "
     "exalted there."),
    ("Mercury is therefore both the 5th lord of the D-7 and an occupant of "
     "the 5th house."),
    "Transit rasi chart at the birth: Jupiter and Mercury are both in Virgo.",
    ("So the D-7's 5th lord and the karaka of children both transited the "
     "D-7's 5th house, and that gave a child."),
)

#: The reading itself, in the book's words.
EXAMPLE_106_READING = (
    "So 5th lord in D-7 and significator of children activated the 5th house "
    "of D-7 in their rasi chart transit and that gave a child."
)

#: **Finding.** Example 106 is §25.4's interaction (1) a third time — a
#: transit rasi position against a natal divisional chart — and the third
#: different varga: D-9 in Example 105, and now D-7. Interaction (2) is still
#: never worked.
A_THIRD_VARGA_AND_STILL_INTERACTION_ONE = (
    "Examples 104, 105 and 106 read a transit rasi chart against the natal "
    "rasi chart, the natal D-9 and the natal D-7 in turn. All three are "
    "interaction (1)."
)

#: **Finding.** What makes Example 106's hit tight is a coincidence the text
#: does not name: Mercury is the D-7's 5th **lord** and also **occupies** its
#: 5th house, so one graha carries two of the three claims on that house, and
#: Jupiter the karaka carries the third from the same rasi.
MERCURY_IS_BOTH_LORD_AND_OCCUPANT_OF_THE_D7_FIFTH = (
    "Virgo is the D-7's 5th house, Mercury lords it, and Mercury stands in "
    "it exalted. Jupiter, the karaka of children, stands there too."
)


# --------------------------------------------------------------------------
# Example 107, part 1 — the natal D-11 against the transit rasi chart
# --------------------------------------------------------------------------

#: Why the D-11 is the chart chosen, and the only place the book names the
#: varga by its other name in a transit context.
D11_IS_RUDRAMSA = (
    "D-11 or Rudramsa is the chart that shows death and destruction. "
    "Considering that the native had a violent death in a plane crash, D-11 "
    "is the apt chart to see his death."
)

#: **A reading device introduced here.** §25.4 splits the grahas of a chart
#: into those that carry **life** and those that carry **death**, by what they
#: lord in the chart being read, and then asks how each fares in transit.
#: Nothing earlier in the book divides a chart's grahas this way.
PLANETS_OF_LIFE_AND_DEATH: tuple[dict[str, object], ...] = (
    {"side": "life", "graha": "Mercury", "because": "1st lord"},
    {"side": "life", "graha": "Sun",
     "because": "3rd lord, which shows physical vitality"},
    {"side": "life", "graha": "Saturn", "because": "8th lord"},
    {"side": "death", "graha": "Jupiter", "because": "7th lord"},
    {"side": "death", "graha": "Moon", "because": "2nd lord"},
    {"side": "death", "graha": "Rahu", "because": "a malefic in lagna"},
)

#: The natal D-11's own features, before any transit is brought to it.
EXAMPLE_107_NATAL_D11: tuple[str, ...] = (
    ("Natal D-11 has lagna in Ge and Rahu occupies it. That is consistent "
     "with a violent death."),
    "The 2nd house in Cn is strong with its lord Moon occupying it.",
    ("Sun is the 3rd lord -- which shows physical vitality -- and he joins the "
     "house of death, 7th, with 7th lord Jupiter."),
    "Mercury owns lagna and he is in 12th.",
    "This D-11 chart has unfavorable features.",
)

#: And how the transit rasi chart finds them, which is §25.4's interaction (1).
EXAMPLE_107_TRANSIT_AGAINST_THE_D11: tuple[str, ...] = (
    ("Two planets of life, Mercury and Sun, are in Cn, afflicted by Rahu. Cn "
     "is the 2nd house and stands for death in the natal D-11."),
    ("Planet of death Moon is in Le (a house of life from natal D-11 lagna) "
     "and Jupiter aspects him, as well as his own 7th house (Sg)."),
    "Saturn is debilitated.",
    ("On the whole, the houses and planets of life in D-11 are afflicted or "
     "weak in the transit rasi chart."),
)

#: **Finding.** The 2nd and the 7th are the maraka houses everywhere in the
#: book, and §25.4 uses them here without saying so: the two "planets of
#: death" that are lords are the **2nd** lord and the **7th** lord, and the
#: house Mercury and the Sun are found in is the **2nd**. So the life/death
#: split is the maraka doctrine applied to a varga rather than a new rule.
THE_LIFE_DEATH_SPLIT_IS_THE_MARAKA_HOUSES = (
    "Jupiter and Moon are called planets of death as lords of the 7th and the "
    "2nd, which are the maraka houses; Rahu joins them as a malefic in lagna. "
    "The life side is the 1st, 3rd and 8th lords."
)


# --------------------------------------------------------------------------
# Example 107, part 2 — the natal rasi chart against the transit D-11
# --------------------------------------------------------------------------

#: §25.4's rule for reading the place and manner of death from the rasi chart.
THE_THIRD_FROM_AL_SHOWS_THE_PLACE_OF_DEATH = (
    "In rasi chart, the 3rd house from AL shows the place and nature of "
    "death. It must have the aspect of a cruel planet for a violent death."
)

#: **Finding.** "It is aspected by Rahu from Le" is **rasi** drishti, not graha
#: drishti. Rahu in Leo does not reach Capricorn by the 5th, 7th or 9th; Leo
#: reaches it because a fixed rasi aspects the movable rasis but its own
#: neighbour. The sentence names the graha and uses the sign's aspect.
THE_CRUEL_ASPECT_HERE_IS_RASI_DRISHTI = (
    "Leo aspects Capricorn by rasi drishti, a fixed sign aspecting the "
    "movable ones other than its neighbour. Rahu standing in Leo does not "
    "aspect Capricorn by graha drishti, whose 5th, 7th and 9th from Leo are "
    "Sagittarius, Aquarius and Aries."
)

#: **Book defect.** Capricorn is called watery here and earthy in §2.2.5 and
#: §12.6. Held as printed; `RASI_ELEMENT` is unchanged. See D-73.
CAPRICORN_IS_CALLED_WATERY_HERE = (
    "§25.4 calls Capricorn \"a watery sign\". §2.2.5's element cycle makes it "
    "earthy and §12.6 names the watery trine as Cn, Sc and Pi."
)

#: What each point of the natal rasi chart stands for, as §25.4 assigns them
#: before bringing the transit D-11 to bear.
EXAMPLE_107_NATAL_RASI_POINTS: tuple[dict[str, str], ...] = (
    {"point": "Le, the lagna", "stands_for": "the native"},
    {"point": "Cp, the 6th", "stands_for": "his accidents"},
    {"point": "Sun, the lagna lord", "stands_for": "the physical body"},
    {"point": "Aq, the 7th, and Saturn its lord", "stands_for": "death"},
    {"point": "Jupiter, the 8th lord", "stands_for": "longevity"},
)

#: And how the transit D-11 finds each of them. This is §25.4's interaction
#: (2), and the only place in the book it is worked.
EXAMPLE_107_TRANSIT_D11_HITS: tuple[dict[str, str], ...] = (
    {"natal_point": "Le, the native", "transit_d11": "Rahu and Moon stand in "
     "it", "reading": "afflicted, the Moon being the natal 12th lord"},
    {"natal_point": "Jupiter, longevity", "transit_d11": "stands in Cn",
     "reading": "the 12th house from the natal lagna"},
    {"natal_point": "Sun, the physical body", "transit_d11": "stands in Cp "
     "with exalted Mars", "reading": "the 6th house of accidents"},
    {"natal_point": "Saturn, the killer", "transit_d11": "stands in Sc",
     "reading": "the sign holding the lagna lord in the natal rasi chart"},
)

#: §25.4's own summary of the last of those.
THE_KILLER_MEETS_THE_BODY = (
    "So the killer of the natal rasi chart (Saturn) interacts with the "
    "physical body (Sun) in the chart showing momentary forces of destruction "
    "(transit D-11)."
)

#: **Finding.** The transit Moon's ekadamsa cannot be got from the printed
#: longitude. 21 Le 49 sits **5.5 arcseconds** below the 9th amsa of Leo, which
#: opens at 21°49.09', and gives Cancer; the ephemeris position is 47
#: arcseconds above it and gives Leo, which is what Chart 57 draws. A D-11 amsa
#: is 2°43'38" wide, so an arcminute of print is a fortieth of one — usually
#: harmless, and here decisive, because the Moon lands on a boundary.
THE_TRANSIT_MOONS_AMSA_NEEDS_THE_UNROUNDED_POSITION = (
    "Chart 57 draws the transit Moon's D-11 in Leo. The printed 21 Le 49 "
    "gives Cancer and the ephemeris gives Leo; the boundary lies between "
    "them, 5.5 arcseconds above the printed value."
)

#: **Correction.** Recorded after Examples 104 to 106 that interaction (2) was
#: described and never worked. Chart 57 works it: the natal rasi chart against
#: the transit D-11, which is exactly that pairing. It is the only instance in
#: the book, and it arrives in the same example as the interaction (1) reading
#: it is meant to fine-tune.
INTERACTION_2_IS_WORKED_ONCE = (
    "Example 107 reads the natal rasi chart against the transit D-11, which "
    "is §25.4's interaction (2). Charts 56 and 57 give the same nativity and "
    "the same instant through both interactions, one after the other."
)


# --------------------------------------------------------------------------
# §25.5 Transits and ashtakavarga
# --------------------------------------------------------------------------

#: **A claim about what ashtakavarga is for**, made only here. Chapter 12
#: built the BAVs and the SAV to grade a natal chart; §25.5 says that is the
#: lesser use.
ASHTAKAVARGAS_MOST_IMPORTANT_PURPOSE = (
    "Though one of the purposes of ashtakavarga is to assess the strength of "
    "planets and houses in natal charts, its most important purpose is the "
    "interpretation of transits."
)

#: **Finding.** §25.2 read transits from natal Moon and §25.3 added natal
#: lagna. Both are among the **eight** references the ashtakavarga already
#: uses, so §25.5 is not a new technique but the same one against all eight at
#: once — and the BAV count *is* the tally of how many of the eight approve.
THE_EIGHT_REFERENCES_GENERALISE_THE_EARLIER_SECTIONS = (
    "Just as we look at the house occupied by a transit planet with respect "
    "to natal Moon and natal lagna, we can look at the houses occupied by a "
    "transit planet with respect to all the eight references used in "
    "ashtakavarga."
)

#: §25.5's transit reading of a BAV count, in its own words.
BAV_TRANSIT_RULE = (
    "If a planet is benefic in its transit rasi with respect to 5 or more "
    "natal references, out of eight, then it will produce good results. If a "
    "planet is benefic in its transit rasi with respect to 3 or less natal "
    "references, out of eight, then it will produce bad results."
)

#: And the extremes, which are new: §12.3 graded 5-8 alike and 0-3 alike.
BAV_TRANSIT_EXTREMES = (
    "A planet with 6 or 7 rekhas in its transit rasi in its BAV invariably "
    "brings excellent results. A planet with 1 or 0 rekhas in its transit "
    "rasi in its BAV invariably brings very poor results."
)

#: **Finding.** §25.5's bands are §12.3's, restated for transits — 5 or more
#: is §12.3's "favorable", 3 or less its "unfavorable" — and the 4 that §25.5
#: passes over in silence is §12.3's **neutral**. So there is no gap at 4; the
#: earlier section already named it.
THE_BAV_BANDS_ARE_12_3S = (
    "§25.5 gives 5-or-more and 3-or-less and says nothing about 4. §12.3 "
    "grades 5 to 8 favorable, 4 neutral and 3 to 0 unfavorable, so 4 is "
    "already answered."
)

#: **Finding.** What §25.5 *adds* to §12.3 is a finer band inside each side:
#: 6 or 7 are singled out from the favorable five-to-eight, and 1 or 0 from
#: the unfavorable nought-to-three, both with "invariably". §12.3 grades all
#: of 5 to 8 alike and all of 0 to 3 alike.
THE_EXTREMES_ARE_NEW = (
    "§12.3's grade is one of three. §25.5 keeps it and marks 6 and 7 as "
    "invariably excellent and 1 and 0 as invariably very poor, which §12.3 "
    "does not distinguish from 5 and 8, or from 2 and 3."
)


def bav_transit_verdict(rekhas: int) -> dict:
    """§25.5's reading of a transiting graha's own BAV count in its transit
    rasi, with §12.3's grade beside it.

    ``emphasis`` carries §25.5's "invariably" for the extremes and is ``None``
    elsewhere; ``verdict`` is ``"neutral"`` at 4, which §25.5 leaves unsaid and
    §12.3 supplies.
    """
    from hora.charts.ashtakavarga import grade

    count = validate.in_range("rekhas", int(rekhas), 0, 8)
    verdict = "good" if count >= 5 else "bad" if count <= 3 else "neutral"
    emphasis = ("invariably excellent" if count in (6, 7) else
                "invariably very poor" if count in (0, 1) else None)
    return {
        "rekhas": count, "verdict": verdict, "emphasis": emphasis,
        "grade_12_3": grade(count),
        "references_approving": count, "of": 8,
    }


#: §25.5's worked pair — one in the rasi chart, one carried into a varga,
#: which is §25.4's interaction (1) with an ashtakavarga behind it.
BAV_TRANSIT_EXAMPLES: tuple[dict[str, object], ...] = (
    {"graha": "Saturn", "bav_of": "the natal rasi chart", "rasi": "Ta",
     "rekhas": 5, "gives": "good results when he transits Taurus"},
    {"graha": "Jupiter", "bav_of": "the natal D-10 chart", "rasi": "Ar",
     "rekhas": 8,
     "gives": "excellent results in career on his rasi transit of Aries"},
)

#: Why the varga case works, in §25.4's terms.
WHY_A_VARGA_BAV_READS_A_RASI_TRANSIT = (
    "Basically, Jupiter's rasi transit in Aries activates the manifestation "
    "of Jovian energy at the physical level in Aries. If Jupiter has many "
    "rekhas in his D-10 BAV, it shows that Jovian energy in Aries goes well "
    "with most sources of energy in D-10 and thus it can have a significant "
    "impact on a native's career."
)


# --------------------------------------------------------------------------
# §25.5.1 Samudaaya Ashtakavarga
# --------------------------------------------------------------------------

#: §25.5.1's transit bands for the SAV. §12.4 already stated the same
#: consequence — "planets transiting in such a rasi bring good results" — so
#: this is that rule restated, with the boundary written the other way. See
#: D-40.
SAV_TRANSIT_RULE = (
    "Planets transiting in rasis with more than 30 rekhas in SAV usually "
    "bring favorable results. Planets transiting in rasis with less than 25 "
    "rekhas in SAV usually bring unfavorable results."
)

#: **The rule that is genuinely new.** Chapter 12 never says which of the two
#: wins when a BAV and the SAV disagree about a rasi; §25.5.1 does.
SAV_DOMINATES_THE_BAVS = (
    "Rekhas in the individual BAVs of planets also matter, but SAV will "
    "dominate over the BAVs if it has too many or too few rekhas."
)

#: Its illustration, which keeps the BAV meaningful inside a dominant SAV.
SAV_DOMINATES_BUT_THE_BAV_STILL_ORDERS = (
    "If SAV has 40 bindus in Pisces, then it means that Pisces is very strong "
    "in the chart. Planets transiting in Pisces, tend to give good results "
    "irrespective of their strength. Of course, if a planet with 6 rekhas in "
    "Pi in its own BAV and a planet with 2 rekhas in Pi in its own BAV are "
    "transiting Pi, the former planet will produce better results than the "
    "latter planet."
)


def transit_strength(bav_rekhas: int, sav_rekhas: int) -> dict:
    """§25.5 and §25.5.1 together: the transiting graha's own BAV count and
    the rasi's SAV count, with §25.5.1's precedence applied.

    "SAV will dominate over the BAVs if it has too many or too few rekhas" —
    so a SAV above 30 or below 25 decides, and the BAV still orders two grahas
    inside the same rasi. Between 25 and 30 the SAV is not dominant and
    ``decided_by`` is the BAV.
    """
    from hora.charts.ashtakavarga import sav_grade

    bav = bav_transit_verdict(bav_rekhas)
    total = validate.in_range("sav_rekhas", int(sav_rekhas), 0, 56)
    dominant = total > 30 or total < 25
    sav_verdict = ("favorable" if total > 30 else
                   "unfavorable" if total < 25 else None)
    return {
        "bav": bav,
        "sav": {"rekhas": total, "verdict": sav_verdict,
                "grade_12_4": sav_grade(total), "dominant": dominant},
        "decided_by": "SAV" if dominant else "BAV",
        "verdict": sav_verdict if dominant else bav["verdict"],
        "note": SAV_DOMINATES_THE_BAVS,
    }


# --------------------------------------------------------------------------
# Example 108 — a whole transit chart weighed against a natal D-10 ashtakavarga
# --------------------------------------------------------------------------

#: **Finding.** Example 108 is the only place the book prints **every** BAV of
#: a chart alongside its SAV — seven rows of twelve and a total row, ninety-six
#: figures for one D-10. Everything before it printed an SAV alone or a few
#: named counts, so this is the widest single check on the ashtakavarga engine
#: anywhere in the text, and all ninety-six reproduce.
THE_ONLY_COMPLETE_ASHTAKAVARGA_IN_THE_BOOK = (
    "Example 108 prints all seven bhinnashtakavargas of Vajpayee's D-10 and "
    "their samudaaya, ninety-six figures in one table."
)

#: **Finding.** The example settles §12.4's boundary from inside. It counts "6
#: out of 7 planets ... in rasis that are very strong in D-10 SAV", and six is
#: reached only by counting Pisces at **exactly 30**. Under §25.5.1's own "more
#: than 30" the count would be two. See D-40.
EXAMPLE_108_COUNTS_THIRTY_AS_VERY_STRONG = (
    "Four grahas transit Pisces, whose D-10 SAV is 30, one Capricorn at 31 "
    "and one Scorpio at 35. The example calls that six of seven in very "
    "strong rasis, so 30 counts."
)

#: Example 108's reading, in the order it gives it.
EXAMPLE_108_READING: tuple[dict[str, object], ...] = (
    {"grahas": ("Sun", "Mars", "Mercury", "Saturn"), "rasi": "Pi",
     "sav": 30, "note": "none of them is too weak in individual BAV"},
    {"grahas": ("Venus",), "rasi": "Cp", "sav": 31, "bav": 6,
     "note": "GL lord in natal D-10, an important planet for power and "
             "authority"},
    {"grahas": ("Moon",), "rasi": "Sc", "sav": 35, "note": None},
    {"grahas": ("Jupiter",), "rasi": "Aq", "sav": 24, "bav": 7,
     "note": "not strong in SAV but strong in his own BAV; the Vimsottari "
             "dasa lord"},
)

#: **Finding.** "None of them is too weak in individual BAV" covers a Mercury
#: with **3** rekhas in Pisces, which §25.5's own band calls bad results. The
#: sentence is only consistent if "too weak" means §25.5's extreme — 1 or 0,
#: "invariably very poor" — rather than the band. It is the extremes the
#: example is ruling out, not the bad side.
TOO_WEAK_MEANS_THE_EXTREME_NOT_THE_BAND = (
    "Mercury has 3 rekhas in Pisces in his D-10 BAV, which §25.5 grades bad, "
    "and Example 108 still says none of the four is too weak. \"Too weak\" "
    "therefore means the 1-or-0 extreme."
)

#: Jupiter is the case §25.5.1's precedence rule was written for, and the
#: example takes the BAV side of it: a rasi the SAV calls weak, carried by the
#: transiting graha's own count.
JUPITER_IS_CARRIED_BY_HIS_OWN_BAV = (
    "Jupiter is in Aq. Though Aq is not strong in SAV, it is strong in "
    "Jupiter's BAV. It has 7 rekhas in Jupiter's natal D-10 BAV. Jupiter's "
    "strength is important, as he is the Vimsottari dasa lord."
)

#: **Finding.** Aquarius has 24 rekhas, which is **below** §25.5.1's 25, so the
#: SAV is dominant there and by the section's own precedence should decide
#: against Jupiter. The example reads it the other way, on the strength of a
#: 7-rekha BAV and Jupiter being the dasa lord. So the domination rule is not
#: absolute, and what overrides it here is stated as importance rather than as
#: a count.
THE_DOMINATION_RULE_IS_SET_ASIDE_FOR_JUPITER = (
    "§25.5.1 makes the SAV dominant below 25 rekhas and Aquarius has 24. "
    "Example 108 nonetheless reads Jupiter there as strong, because his own "
    "BAV has 7 and he is the Vimsottari dasa lord."
)

EXAMPLE_108_CONCLUSION = (
    "So, as per ashtakavarga, transits are very favorable to Sri Vajpayee's "
    "career on March 19, 1998."
)


# --------------------------------------------------------------------------
# §25.6 — Timing with sodhya pindas
# --------------------------------------------------------------------------

SODHYA_TIMING_SOURCE = (
    "Parasara taught some techniques of timing events based on sodhya "
    "pindas.")

#: §25.6's core rule, verbatim.
SODHYA_TIMING_RULE = (
    "We can take the number of rekhas in any house from a planet and "
    "multiply the count with the planet's sodhya pinda. We can get a "
    "nakshatra from that product by dividing it with 27, taking the "
    "remainder and counting nakshatras from Aswini. Benefics and malefics "
    "transiting in the nakshatra will give good or bad results "
    "(respectively) relating to the original house. Especially Saturn's "
    "transit is important. Saturn's transit in the nakshatra corresponding "
    "to a particular house makes the signified matters suffer. Jupiter's "
    "transit is beneficial.")

#: The rasi half of the same rule, with its own ranking clause.
SODHYA_TIMING_RASI_RULE = (
    "We can also find a rasi by dividing the product with 12 instead of 27 "
    "and counting rasis from Aries. Saturn's transit in the resultant rasi "
    "brings misfortune relating to the original house. However, nakshatras "
    "are more important.")

#: §25.6's other name for the sodhya pinda, given only here.
YOGA_PINDA_IS_THE_SAME_THING = (
    "We should multiply it by the sodhya pinda of the planet (also called "
    "yoga pinda).")

#: The companion nakshatras some readers add, and the book's reason.
SODHYA_TIMING_COMPANIONS = (
    "Some people also take the 10th or 19th nakshatra from the nakshtra "
    "found above. A nakshatra and the 10th and 19th nakshatras from it are "
    "owned by the same planet under Vimsottari dasa scheme and they go "
    "together.")

#: **Finding.** The companion rule is an identity, not an observation. The
#: 10th from a nakshatra counted inclusively is the 9th after it, Vimsottari
#: lordship repeats every 9 nakshatras, and 27 is three nines — so *every*
#: nakshatra shares its lord with its 10th and 19th, all 27 of them, and the
#: three always partition into one lord's whole holding.
THE_TENTH_AND_NINETEENTH_ARE_ALWAYS_THE_SAME_LORD = (
    "Vimsottari lordship repeats every 9 nakshatras and there are 27, so a "
    "nakshatra, the 10th from it and the 19th from it are the complete set "
    "of nakshatras one planet owns. The rule holds for all 27, not for some."
)

#: §25.6's matters per planet, verbatim and in its order.
SODHYA_TIMING_MATTERS: dict[str, str] = {
    "Sun": "soul, inherent nature, personality, will power and father",
    "Moon": "mind, wisdom, peace, happiness and mother",
    "Mars": "siblings, land and strength",
    "Mercury": "business, commerce, profession, friends and good behavior",
    "Jupiter": "the nourishment of body, learning, children and wealth",
    "Venus": "marriage, comforts, luxuries, vehicles and sexual pleasures",
    "Saturn": "longevity, livelihood, fears, sadness, dangers and sorrows",
}

#: §25.6's four-step procedure, in its own words.
SODHYA_TIMING_PROCEDURE: tuple[str, ...] = (
    ("When we want to time events relating to a particular matter, we should "
     "first fix the relevant planet."),
    "Then we should fix the relevant house.",
    ("We should then find the number of rekhas in that house from that "
     "planet in that planet's BAV."),
    ("We should multiply it by the sodhya pinda of the planet (also called "
     "yoga pinda). By dividing the product with 27 or 12 and taking the "
     "remainder, we should find the associated nakshatra or rasi. Then we "
     "can time key events based on the transits in that nakshatra and rasi."),
)

#: Table 61 — the seven pairings Parasara gave as specific examples, with the
#: area of life each reads. Planet -> (house, area).
TABLE_61_TIMING: dict[str, tuple[int, str]] = {
    "Sun": (9, "Father"),
    "Moon": (4, "Mother"),
    "Mars": (3, "Siblings"),
    "Mercury": (10, "Profession"),
    "Jupiter": (5, "Children"),
    "Venus": (7, "Marriage"),
    "Saturn": (8, "Longevity"),
}

#: **Finding.** Table 61 is a shortlist, not the method's scope. §25.6 says
#: outright that "we can take **any** house from **any** planet", and the
#: table is only where Parasara worked examples. So `sodhya_timing` takes any
#: (planet, house) pair and Table 61 is served beside it as the seven that
#: are attested.
TABLE_61_IS_A_SHORTLIST_NOT_THE_SCOPE = (
    "Though Parasara indicated that we can take any house from any planet "
    "and gave a long list of matters to be seen from each planet, he gave a "
    "few specific examples. A list of the matters is given in Table 61."
)

#: §25.6's worked illustration. It supposes its inputs rather than reading a
#: chart, so it is arithmetic to be reproduced and not a chart fixture.
ILLUSTRATION_INPUTS = {"planet": "Sun", "house": 9, "planet_sign": "Aq",
                       "house_sign": "Li", "rekhas": 5, "pinda": 86}
ILLUSTRATION_WORKING = (
    "Suppose Sun is in Aq. Suppose Sun's BAV contains 5 rekhas in Li (the "
    "9th from Aq). Suppose Sun's sodhya pinda is 86. Multiplying 86 with 5, "
    "we get 430. If we divide 430 by 27, the quotient is 15 and the "
    "remainder is 25. The 25th constellation is Poorvabhadrapada. So "
    "Saturn's transit in Poorvabhadrapada is bad for father and Jupiter's "
    "transit in the same nakshatra is good. Now let us find the rasi. By "
    "dividing 430 by 12, we get a quotient of 35 and a remainder of 10. So "
    "Saturn's transit in Cp (the 10th rasi of the zodiac) is bad for father "
    "and Jupiter's transit in Cp is good.")

#: PVR's own warning about the whole section, and the reason it is here at
#: all. Nothing built on §25.6 may present its output as settled.
SODHYA_TIMING_IS_OPEN_TO_RESEARCH = (
    "However, this approach does not give consistent results. Readers should "
    "realize that the topic of sodhya pindas is open to research.")

#: The four questions §25.6 leaves open, in its own words.
SODHYA_TIMING_OPEN_QUESTIONS: tuple[str, ...] = (
    ("Most astrologers use these principles with only the rasi chart. If "
     "matters relating to father have to be seen from D-12, as taught by "
     "Parasara, should we use D-12 when timing events related to father?"),
    "Should we use the sodhya pinda and rekha count from D-12?",
    "Should we take the 9th from Sun in rasi chart or take it in D-12?",
    ("Moreover, as we have learnt, there are some inconsistencies between "
     "Parasara and Varahamihira in the definition of ashtakavarga and this "
     "can alter the sodhya pindas of Moon and Venus. In addition, we have "
     "some controversies in the exact definitions of the reductions to be "
     "done to get Sodhita Ashtakavarga from Bhinna Ashtakavarga. That can "
     "again alter sodhya pindas."),
)

SODHYA_TIMING_CLOSING = (
    "Timing of events with sodhya pindas is a very important topic, but what "
    "the readers learn here may not be the final word. It is hoped that "
    "readers will experiment with an open mind and share their findings with "
    "other astrologers.")

#: §25.6 states the remainder rule only for a non-zero remainder: 25 gives the
#: 25th nakshatra, 10 the 10th rasi. **Example 111 supplies the rest** — 0 is
#: "equivalent to 27" and "equivalent to 12" — which closed OI-143 in the
#: direction already implemented. The zero is reachable two ways: a house with
#: **no** rekhas makes the product 0 outright, and an ordinary product can
#: land on a multiple.
THE_ZERO_REMAINDER_MEANS_THE_LAST = (
    "A remainder of 0 counts as the 27th nakshatra and the 12th rasi, which "
    "Example 111 states outright. It arises whenever the house holds no "
    "rekhas, since the product is then 0, and whenever the product is a "
    "multiple of 27 or 12."
)


def timing_nakshatra(product: int) -> dict:
    """§25.6's nakshatra from a product: the remainder mod 27, from Aswini.

    A remainder of 0 is **not** defined by the section. It is returned as the
    27th, the only reading that keeps the cycle closed, and flagged as ours —
    see `THE_ZERO_REMAINDER_MEANS_THE_LAST` and OI-143.
    """
    value = int(validate.non_negative("product", int(product)))
    remainder = value % 27
    ordinal = remainder if remainder else 27
    return {
        "product": value,
        "divisor": 27,
        "quotient": value // 27,
        "remainder": remainder,
        "ordinal": ordinal,
        "index": ordinal - 1,
        "nakshatra": str(NAKSHATRA_NAMES[ordinal - 1]),
        "lord": str(GRAHA_NAMES[NAKSHATRA_LORD[ordinal - 1]]),
        "remainder_was_zero": remainder == 0,
        "zero_reading": (
            None if remainder else THE_ZERO_REMAINDER_MEANS_THE_LAST),
    }


def timing_rasi(product: int) -> dict:
    """§25.6's rasi from the same product: the remainder mod 12, from Aries.

    "However, nakshatras are more important" — said so in the result.
    """
    value = int(validate.non_negative("product", int(product)))
    remainder = value % 12
    ordinal = remainder if remainder else 12
    return {
        "product": value,
        "divisor": 12,
        "quotient": value // 12,
        "remainder": remainder,
        "ordinal": ordinal,
        "sign": ordinal - 1,
        "rasi": str(RASI_NAMES[ordinal - 1]),
        "remainder_was_zero": remainder == 0,
        "zero_reading": (
            None if remainder else THE_ZERO_REMAINDER_MEANS_THE_LAST),
        "ranked_below_the_nakshatra": (
            "However, nakshatras are more important."),
    }


def companion_nakshatras(index: int) -> dict:
    """The 10th and 19th from a nakshatra — counted inclusively, so the 9th
    and 18th after it. All three share a Vimsottari lord, always.
    """
    start = validate.in_range("nakshatra index", int(index), 0, 26)
    trio = tuple((start + step) % 27 for step in (0, 9, 18))
    lords = {str(GRAHA_NAMES[NAKSHATRA_LORD[n]]) for n in trio}
    return {
        "nakshatra": str(NAKSHATRA_NAMES[start]),
        "indexes": trio,
        "nakshatras": [str(NAKSHATRA_NAMES[n]) for n in trio],
        "lord": lords.pop(),
        "counted": "inclusively — the 10th from a nakshatra is the 9th after "
                   "it",
        "why": THE_TENTH_AND_NINETEENTH_ARE_ALWAYS_THE_SAME_LORD,
        "optional": SODHYA_TIMING_COMPANIONS,
    }


def sodhya_timing(planet: str, house: int, *, planet_sign: int,
                  bav_rekhas: Sequence[int], pinda: int) -> dict:
    """§25.6's four steps for one (planet, house) pair.

    :param planet: one of the seven; the nodes and lagna have no sodhya pinda.
    :param house: 1 to 12, counted from `planet_sign`.
    :param planet_sign: where the planet is, 0 = Aries.
    :param bav_rekhas: the planet's twelve BAV counts, Aries first.
    :param pinda: the planet's sodhya pinda, also called its yoga pinda.
    """
    if planet not in SODHYA_TIMING_MATTERS:
        raise GocharaError(
            f"{planet!r} has no sodhya pinda; the seven are "
            f"{', '.join(SODHYA_TIMING_MATTERS)}")
    validate.in_range("house", int(house), 1, 12)
    validate.in_range("planet sign", int(planet_sign), 0, 11)
    validate.non_negative("pinda", int(pinda))
    if len(bav_rekhas) != 12:
        raise GocharaError(
            f"a BAV has twelve counts, one per rasi; got {len(bav_rekhas)}")

    sign = (int(planet_sign) + int(house) - 1) % 12
    rekhas = validate.in_range(
        f"{planet}'s rekhas in {RASI_NAMES[sign]}", int(bav_rekhas[sign]),
        0, 8)
    product = rekhas * int(pinda)
    attested = TABLE_61_TIMING.get(planet)
    return {
        "planet": planet,
        "house": int(house),
        "house_sign": sign,
        "house_rasi": str(RASI_NAMES[sign]),
        "planet_sign": int(planet_sign),
        "rekhas": rekhas,
        "pinda": int(pinda),
        "product": product,
        "nakshatra": timing_nakshatra(product),
        "rasi": timing_rasi(product),
        "matters": SODHYA_TIMING_MATTERS[planet],
        "in_table_61": bool(attested and attested[0] == int(house)),
        "table_61_house": None if attested is None else attested[0],
        "table_61_area": None if attested is None else attested[1],
        "reading": (
            "Saturn's transit in the nakshatra makes the signified matters "
            "suffer; Jupiter's transit is beneficial. Benefics and malefics "
            "transiting there give good or bad results respectively."),
        "caveat": SODHYA_TIMING_IS_OPEN_TO_RESEARCH,
    }


# --------------------------------------------------------------------------
# Example 111 — the zero remainder, answered by the book
# --------------------------------------------------------------------------

#: **The rule for a zero remainder, stated at last.** §25.6 gave the mapping
#: only for non-zero remainders; Example 111 supplies the rest, and it is the
#: reading `timing_nakshatra` and `timing_rasi` already return.
EXAMPLE_111_DEFINES_THE_ZERO_REMAINDER = (
    "Le has 0 rekhas in Saturn's BAV. Saturn's sodhya pinda is 203. The "
    "product is 0. By dividing it with 27, we get 0 which is equivalent to "
    "27. So we get Revathi star. By dividing 0 with 12, we get 0 which is "
    "equivalent to 12. So we get Pisces.")

#: **Finding.** The example reaches zero by the route §25.6's arithmetic makes
#: unavoidable rather than by a multiple: the 8th house from Saturn simply has
#: **no rekhas**, so the product is 0 whatever the pinda is. A planet with an
#: empty house therefore always times to Revati and Pisces, for every native
#: and every matter — the one output of §25.6 that carries no information
#: about the chart it came from.
AN_EMPTY_HOUSE_ALWAYS_TIMES_TO_REVATI = (
    "When the chosen house holds no rekhas the product is 0 regardless of the "
    "sodhya pinda, so the answer is Revati and Pisces on every chart. The "
    "pinda drops out of the calculation entirely."
)

#: **Finding.** The zero case is the one remainder where the two halves cannot
#: disagree. Revati is the last nakshatra and Pisces the last rasi, and Revati
#: lies wholly inside Pisces — so "Revathi star in Pisces" names one span
#: twice. §25.6 ranks the nakshatra above the rasi precisely because they can
#: point elsewhere; here they cannot.
THE_ZERO_CASE_IS_THE_ONE_WHERE_BOTH_HALVES_AGREE = (
    "A remainder of 0 gives the 27th nakshatra and the 12th rasi. Revati "
    "occupies the last 13º 20' of Pisces, so the nakshatra reading and the "
    "rasi reading name the same stretch of the zodiac."
)

#: Example 111's inputs and answer, as printed.
EXAMPLE_111 = {
    "planet": "Saturn", "house": 8, "matter": "longevity",
    "planet_sign": "Cp", "house_sign": "Le", "rekhas": 0, "pinda": 203,
    "product": 0, "nakshatra": "Revati", "rasi": "Pisces",
}

#: Saturn's BAV as Example 111 prints it, Aries first.
EXAMPLE_111_SATURN_BAV: tuple[int, ...] = (
    3, 4, 6, 3, 0, 2, 2, 5, 4, 3, 2, 5)

EXAMPLE_111_OUTCOME = (
    "When Saturn was transiting in Revathi star in Pisces, she passed away.")

#: **Finding.** The example names no date. Saturn was in Revati from **4
#: April 1997 to 17 April 1998** — a thirteen-month stay, because his
#: retrograde loop crosses the nakshatra three times — and the crash of 31
#: August 1997 falls inside it. So the transit is confirmed, and the window it
#: picks out is a year wide, which is the resolution §25.6's own warning is
#: about.
THE_REVATI_TRANSIT_WINDOW_IS_THIRTEEN_MONTHS = (
    "Saturn entered Revati on 4 April 1997 and left on 17 April 1998, his "
    "retrograde loop keeping him there for thirteen months. The technique "
    "names that window, not a day."
)
