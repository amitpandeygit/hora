"""§27.1 — casting a Tajaka annual chart.

The rule is a moment and a place, and the section is exact about both. The
moment is when the Sun returns to the **exact** position he held at birth —
the section italicises it and bolds both words — so the chart is not cast for
the birthday, nor for a fixed number of days after the last return. It is
solved for. The place is the **birthplace**, whatever the native's address at
the time, which is the one thing here that a solar-return chart in another
tradition would get differently.

One question the section does not answer: "the position occupied by him at the
time of one's birth" is a longitude, and a longitude is sidereal or tropical.
This engine is sidereal everywhere, so the return is solved against the natal
**sidereal** longitude, which makes the interval a sidereal year. A tropical
reading would place each return about twenty minutes earlier per year of age,
which is some five degrees of ascendant. See OI-151; the section's own example
is what settles it.
"""
from __future__ import annotations

from collections.abc import Callable

from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.panchanga.solver import scan_for_crossing

#: The section's own approximation, kept as printed. It is the reason a year
#: is a year and not the reason a return is where it is: the chart is solved
#: for, never stepped to.
SUN_MOVES_30_DEGREES_A_MONTH = (
    "Sun moves with respect to earth at the rate of 30° per month. He takes "
    "one year to complete one cycle through the zodiac. He returns to the "
    "position occupied by him at the time of one's birth after every one-year "
    "period."
)

#: The rule itself. The book italicises the whole sentence and bolds "exact
#: moment" and "exact position".
VARSHA_PRAVESH_RULE = (
    "At the exact moment when Sun returns to the exact position he occupied "
    "at the time of a person's birth, a new year is said to commence in the "
    "life of that person. A chart can be cast for the commencement of the new "
    "year. This is called a Tajaka varsha chakra or a Tajaka annual chart."
)

#: The place rule, and the only part of the casting that is not the ephemeris.
BIRTHPLACE_RULE = (
    "The longitude and latitude of the birthplace must be used in casting "
    "this chart, irrespective of the place of living at the commencement of "
    "the new year."
)

VARSHA_PRAVESH_NAME = (
    "The commencement of a new year is called \"varsha pravesh\" by some "
    "people. Varsha means a year and pravesh means entry.")

#: The gloss, as two words.
VARSHA_PRAVESH_MEANS: dict[str, str] = {"varsha": "a year", "pravesh": "entry"}

#: **Finding.** The place rule is the sharpest thing on the page and the
#: easiest to get wrong. A solar return cast for the native's **current**
#: residence is a different chart — the same instant against a different
#: horizon — and the ascendant can land anywhere. §27.1 forecloses that
#: reading in one sentence, so `varsha_pravesh` takes no place at all and the
#: caller supplies the birth place to `compute_chart` as it would for a natal.
THE_PLACE_IS_THE_BIRTHPLACE_AND_NOT_THE_RESIDENCE = (
    "Section 27.1 says the birthplace's longitude and latitude must be used "
    "irrespective of where the native lives when the year begins. Only the "
    "moment is recomputed; the horizon is the natal one."
)

#: **Finding.** "At the exact moment" rules out the two shortcuts a reader
#: might take. The chart is not cast for the birthday — the return drifts
#: through the calendar day by day — and it is not cast a fixed 365 days after
#: the last one, which Part 4's opening could be read as licensing. It is
#: solved for, which is why this function searches rather than adds.
THE_RETURN_IS_SOLVED_FOR_NOT_STEPPED_TO = (
    "The section bolds \"exact moment\" and \"exact position\". Neither the "
    "birthday nor a fixed 365-day step gives that instant, so the crossing is "
    "found by search."
)

#: Not supplied. Footnote 75 hangs off "Tajaka annual chart" and its text has
#: not been printed here.
FOOTNOTE_75_NOT_SUPPLIED = (
    "Section 27.1 marks footnote 75 on the words \"Tajaka annual chart\". The "
    "footnote itself is not on the page supplied.")


class TajakaError(validate.InputError):
    """A Tajaka input that cannot be resolved."""


def varsha_pravesh(sun_longitude_at: Callable[[float], float],
                   natal_sun_longitude: float, birth_jd: float,
                   year: int, *, step: float = 0.5) -> dict:
    """The instant the native's `year`-th Tajaka year begins.

    :param sun_longitude_at: julian day -> the Sun's sidereal longitude.
        Passed in so this stays independent of how positions are sourced.
    :param natal_sun_longitude: the Sun's longitude in the natal chart. The
        target is this value exactly; §27.1 says "the exact position".
    :param birth_jd: the julian day of birth, universal time.
    :param year: 1 is the year that begins at birth itself, 2 the first
        return, and so on — the count the book uses when it speaks of a
        native's nth year.
    :returns: the julian day of the varsha pravesh, with the search window
        used, or ``jd`` ``None`` and a reason when no crossing is bracketed.
    """
    index = validate.in_range("year", int(year), 1, 200)
    target = validate.longitude("natal_sun_longitude",
                                float(natal_sun_longitude))
    returns = index - 1
    if returns == 0:
        return {
            "year": index, "returns_completed": 0, "jd": birth_jd,
            "found": True, "target_longitude": target,
            "is_birth_itself": True,
            "searched": None,
            "rule": VARSHA_PRAVESH_RULE,
            "place": BIRTHPLACE_RULE,
            "reason": None,
        }

    # A sidereal year is about 365.2564 days; bracket generously on both
    # sides so a crossing is never missed at the window edge.
    approximate = birth_jd + returns * 365.2564
    jd_from, jd_to = approximate - 20.0, approximate + 20.0
    found = scan_for_crossing(sun_longitude_at, target, jd_from, jd_to,
                              step=step)
    return {
        "year": index,
        "returns_completed": returns,
        "jd": found,
        "found": found is not None,
        "target_longitude": target,
        "is_birth_itself": False,
        "searched": {"from": jd_from, "to": jd_to, "step_days": step},
        "rule": VARSHA_PRAVESH_RULE,
        "place": BIRTHPLACE_RULE,
        "reason": (None if found is not None else
                   "no crossing of the natal solar longitude in the window; "
                   "widen it or check the natal longitude"),
    }


def rasi_of(longitude: float) -> str:
    """The rasi a longitude falls in, by name."""
    return str(RASI_NAMES[int(validate.longitude("longitude",
                                                 float(longitude)) // 30)])


# --------------------------------------------------------------------------
# Example 118 — the rule run once, end to end
# --------------------------------------------------------------------------

EXAMPLE_118 = (
    "Let us take a native with this birthdata: 8th March 1967, 5:40 pm (IST), "
    "73 E 04, 26 N 18. Sun occupies 23° 50' 25\" in Aq in his birthchart. "
    "Suppose we want analyze the one-year period of March 2000-March 2001 "
    "using Tajaka annual chart.")

EXAMPLE_118_METHOD = (
    "Then we should find the date and time when Sun enters 23° 50' 25\" in Aq "
    "in March 2000. We find that Sun enters this position at 4:41:21 am on "
    "8th March 2000. The native finishes 33 years and enters his 34th year at "
    "that time.")

EXAMPLE_118_CHART = (
    "We can erect a chart with the following data: 8th March 2000, 4:41:21 am "
    "(IST), 73 E 04, 26 N 18. That chart is called the native's Tajaka annual "
    "chart for 2000-2001. Rasi chart erected with this data is shown in Chart "
    "66. Along with this rasi chart, we can draw all the divisional charts at "
    "this time.")

EXAMPLE_118_USE = (
    "By analyzing this rasi chart and the associated divisional charts, we "
    "can find out the fortune of the native during the year. The matters "
    "shown by various divisional charts, houses, rasis, planets, arudha padas "
    "etc remain the same. To time events within this year, we have annual "
    "dasas. We will learn them in later chapters.")

#: The example's own numbers, as the fixture a test checks the search against.
EXAMPLE_118_NATIVITY: dict[str, object] = {
    "birth": "8th March 1967, 5:40 pm (IST), 73 E 04, 26 N 18",
    "natal_sun": "23 Aq 50 25",
    "varsha_pravesh": "8th March 2000, 4:41:21 am (IST)",
    "years_finished": 33,
    "year_entered": 34,
    "chart": 66,
}

FOOTNOTE_75 = (
    "Western astrologers also use similar charts and call them \"solar "
    "return\" charts. Some Indian astrologers call these \"varshaphal\" "
    "charts. Varshaphal means \"results for one year\".")

FOOTNOTE_76 = (
    "Even if the native is living on the other side of the globe, we must "
    "still cast the annual chart for birthplace co-ordinates. So we are using "
    "the longitude and latitude of his birthplace here.")

#: **Finding.** The example settles the zodiac, which §27.1 never states. Our
#: search against the natal **sidereal** longitude lands within nine seconds
#: of the printed 4:41:21 am. The same search against the **tropical**
#: longitude lands on 7 March at 17:37 — eleven hours early and a different
#: day. There is no reading of "the exact position" but the sidereal one.
#: OI-151 is closed by arithmetic, not by preference.
THE_EXAMPLE_SETTLES_THE_ZODIAC_AS_SIDEREAL = (
    "Solving for the Sun's return to his natal sidereal longitude gives "
    "4:41:12 am on 8 March 2000 against the book's 4:41:21. Solving for the "
    "tropical longitude gives 5:37 pm on 7 March. The sidereal reading is the "
    "only one that reproduces the example."
)

#: **Finding.** The example's year count is the one `varsha_pravesh` takes.
#: "The native finishes 33 years and enters his 34th year at that time" — so
#: the 34th year begins at the 33rd return, and year 1 is the birth itself.
#: That convention is the book's, checked rather than assumed.
THE_NTH_YEAR_BEGINS_AT_THE_N_MINUS_ONE_TH_RETURN = (
    "Example 118's native finishes 33 years and enters his 34th at the "
    "return, so the nth year begins at the (n-1)th return and the first year "
    "begins at birth."
)

#: **Finding.** Footnote 76 restates §27.1's place rule and sharpens it —
#: "even if the native is living on the other side of the globe". The section
#: said "irrespective of the place of living"; the footnote names the extreme
#: case, which is the only reason to state a rule twice.
FOOTNOTE_76_RESTATES_THE_PLACE_RULE_AT_ITS_EXTREME = (
    "Section 27.1 says the birthplace must be used irrespective of where the "
    "native lives. Footnote 76 says it again for a native on the other side "
    "of the globe."
)

#: **Finding.** Footnote 75 names the system's two other names and, with the
#: opening's provenance paragraph, completes the picture: this is the western
#: **solar return** chart, called **varshaphal** by some Indian astrologers.
#: The book has now said three times, in three ways, that the technique is
#: shared rather than Parasaran.
FOOTNOTE_75_NAMES_THE_WESTERN_AND_THE_INDIAN_ALIASES = (
    "Footnote 75 gives \"solar return\" for the western name and "
    "\"varshaphal\", results for one year, for the Indian one. Part 4's "
    "opening had already said the system is closer to western astrology and "
    "has no maharshi behind it."
)

#: The three names the book now has for one chart, and whose they are.
ANNUAL_CHART_ALIASES: tuple[dict[str, str], ...] = (
    {"name": "Tajaka varsha chakra", "from": "the book, §27.1"},
    {"name": "Tajaka annual chart", "from": "the book, §27.1"},
    {"name": "solar return chart", "from": "western astrologers, footnote 75"},
    {"name": "varshaphal chart",
     "from": "some Indian astrologers, footnote 75"},
)

#: **Finding.** Example 118's chart is a **pre-dawn** moment — 4:41 am — and
#: `compute_panchanga` raises for it, exactly as OI-149 predicts. So the
#: defect footnote 71 named now has a printed book chart as its test case and
#: not only Chart 56. Every other figure of Chart 66 reproduces.
CHART_66_IS_A_SECOND_TEST_CASE_FOR_OI_149 = (
    "Chart 66 is cast for 4:41:21 am, before sunrise. Our /v1/panchanga "
    "rejects that instant with \"hora index must be between 1 and 24\", which "
    "is OI-149 on a chart the book prints."
)
