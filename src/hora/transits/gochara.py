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
    54: {"for": None, "built": False},
    55: {"for": None, "built": False},
    56: {"for": None, "built": False},
    57: {"for": None, "built": False},
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

#: Every supplied table, keyed by graha. Tables 54 to 59 join it as they come.
STANDARD_RESULTS: dict[int, tuple[dict[str, object], ...]] = {
    int(Graha.SUN): TABLE_53_SUN,
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
