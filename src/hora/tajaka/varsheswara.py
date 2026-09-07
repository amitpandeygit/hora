"""§28.6 — varsheswara, the lord of the year.

Five candidates and a cascade that picks one of them. The candidates are found
from the annual chart, the natal lagna, the muntha and Table 73; the cascade
ranks them by §28.2's aspects on lagna and §28.4's pancha vargeeya bala, so
this section is where the chapter's earlier machinery is first used together.

Two things in the cascade do not close, and both are refused rather than
guessed. Its opening sentence and its operational paragraph can disagree about
which candidate wins — see OI-156 — and its last two steps are stated with
different tests, "an aspect" against "a strong aspect", so a chart with only
weak aspects on lagna satisfies both. `varsheswara` reports the shortlists and
says which step it stopped at, and returns no lord when the section does not
settle one.
"""
from __future__ import annotations

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_LORD, RASI_NAMES
from hora.tajaka.aspects import aspect_on_house

VARSHESWARA_RULE = (
    "Varsheswara or lord of the year is the most important planet during the "
    "year. His dasa brings important results. The following are the "
    "candidates:")

#: §28.6's five candidates, in its own order and words.
VARSHESWARA_CANDIDATES: tuple[dict[str, str], ...] = (
    {"number": "1",
     "candidate": "Lord of the rasi occupied by Sun or Moon in the annual "
                  "chart, based on whether the new year starts during the "
                  "day or the night"},
    {"number": "2", "candidate": "Lord of natal lagna"},
    {"number": "3", "candidate": "Lord of Muntha"},
    {"number": "4", "candidate": "Lord of lagna in the annual chart"},
    {"number": "5", "candidate": "Triraasi lord of lagna in the annual chart "
                                 "(see Table 73)"},
)

TABLE_73_TITLE = "Triraasi Lords"

#: Table 73 as printed: lagna rasi -> (day lord, night lord).
TABLE_73_TRIRAASI_LORDS: dict[int, tuple[int, int]] = {
    0:  (0, 4),   # Ar  Sun     / Jupiter
    1:  (5, 1),   # Ta  Venus   / Moon
    2:  (6, 3),   # Ge  Saturn  / Mercury
    3:  (5, 2),   # Cn  Venus   / Mars
    4:  (4, 0),   # Le  Jupiter / Sun
    5:  (1, 5),   # Vi  Moon    / Venus
    6:  (3, 6),   # Li  Mercury / Saturn
    7:  (2, 5),   # Sc  Mars    / Venus
    8:  (6, 6),   # Sg  Saturn  / Saturn
    9:  (2, 2),   # Cp  Mars    / Mars
    10: (4, 4),   # Aq  Jupiter / Jupiter
    11: (1, 1),   # Pi  Moon    / Moon
}

SELECTION_RULE = (
    "If a candidate is strong as per panchavargeeya bala and has a benefic "
    "aspect on lagna, it becomes the lord of the year.")

SELECTION_PROCEDURE = (
    "After the five candidates are found, the candidates having a benefic "
    "aspect on lagna are short-listed. Out of those, the planet having the "
    "highest panchavargeeya bala becomes the lord of the year. If two "
    "candidates have similar panchavargeeya bala, the one becoming a "
    "candidate in more of the five categories listed above becomes the lord "
    "of the year.")

SELECTION_FALLBACKS = (
    "If none of the planet has a benefic aspect on lagna, even a malefic "
    "aspect may be accepted. If none of the planets has an aspect on lagna, "
    "we may take a candidate that is very strong as per panchavargeeya bala. "
    "If none of the candidates has a strong aspect on lagna and none of the "
    "candidates is very strong as per panchavargeeya bala, then we may take "
    "the first candidate (lord of the rasi occupied by Sun or Moon in the "
    "annual chart, based on whether the new year starts during the day or "
    "the night).")

#: **Finding.** Table 73's last four rasis carry the **same lord by day and by
#: night** — Sagittarius Saturn, Capricorn Mars, Aquarius Jupiter, Pisces the
#: Moon — while the first eight all differ. So the day/night distinction that
#: candidates (1) and (5) both turn on stops mattering for a third of lagnas.
THE_LAST_FOUR_RASIS_HAVE_ONE_TRIRAASI_LORD = (
    "Sagittarius, Capricorn, Aquarius and Pisces have the same triraasi lord "
    "in both columns of Table 73. The other eight rasis have different ones."
)

#: **Finding.** The twenty-four cells of Table 73 are shared **four apiece**
#: among Jupiter, Venus, the Moon, Saturn and Mars, and **two apiece** between
#: the Sun and Mercury. So five planets have twice the reach of the other two
#: as triraasi lords, and every one of the seven appears.
THE_SUN_AND_MERCURY_GET_HALF_A_SHARE = (
    "Table 73 gives Jupiter, Venus, the Moon, Saturn and Mars four cells "
    "each and the Sun and Mercury two each, which is twenty-four in all."
)

#: **Finding.** §28.6 is the first section to use the chapter's own earlier
#: machinery on both sides at once: the shortlist is §28.2's aspects and the
#: ranking is §28.4's pancha vargeeya bala. Its words for strength — "strong",
#: "very strong" — are §28.4.6's own grades and not new ones, so the cascade
#: reads directly off that scale.
THE_CASCADE_USES_28_2_AND_28_4_6S_OWN_VOCABULARY = (
    "Section 28.6 shortlists by a benefic aspect on lagna, which is section "
    "28.2's classification, and ranks by pancha vargeeya bala, whose grades "
    "strong and very strong are section 28.4.6's."
)

#: **Finding.** A candidate has **no aspect on lagna at all** exactly when it
#: stands in the 6th or 8th from lagna, those being the two houses §28.2
#: leaves out. So the cascade's third step — "if none of the planets has an
#: aspect on lagna" — is reachable only when every candidate sits in one of
#: those two houses, which is a narrow case and not the common one the
#: wording suggests.
NO_ASPECT_ON_LAGNA_MEANS_THE_SIXTH_OR_EIGHTH = (
    "Section 28.2 gives no aspect to the 6th and 8th houses from a planet, so "
    "a candidate aspects lagna unless lagna is the 6th or 8th from it."
)

#: **Finding.** The cascade's last two steps are stated with different tests.
#: The third says "if none of the planets has **an** aspect on lagna"; the
#: fourth says "if none of the candidates has a **strong** aspect on lagna".
#: §28.2 grades aspects strong, weak and neutral, so a chart whose candidates
#: aspect lagna only weakly satisfies the fourth condition and not the third,
#: and the two steps prescribe different answers for it. See OI-156.
THE_LAST_TWO_STEPS_TEST_DIFFERENT_THINGS = (
    "The third fallback asks whether any candidate has an aspect on lagna and "
    "the fourth whether any has a strong one. A weak aspect answers the first "
    "yes and the second no, and the section gives no order between them."
)


class VarsheswaraError(validate.InputError):
    """A varsheswara input that cannot be resolved."""


def triraasi_lord(lagna_rasi: int, *, daytime: bool) -> dict:
    """Table 73's triraasi lord for a lagna, by day or by night."""
    index = validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    day, night = TABLE_73_TRIRAASI_LORDS[index]
    lord = day if daytime else night
    return {
        "lagna_rasi": index,
        "lagna_rasi_name": str(RASI_NAMES[index]),
        "daytime": bool(daytime),
        "lord": lord,
        "lord_name": str(GRAHA_NAMES[lord]),
        "same_both_ways": day == night,
    }


def aspect_on_lagna(candidate_rasi: int, lagna_rasi: int) -> dict:
    """§28.2's aspect a candidate casts on the annual chart's lagna.

    :returns: the aspect and its nature, or ``aspect`` ``None`` when lagna is
        the 6th or 8th from the candidate — see
        `NO_ASPECT_ON_LAGNA_MEANS_THE_SIXTH_OR_EIGHTH`.
    """
    where = validate.in_range("candidate_rasi", int(candidate_rasi), 0, 11)
    lagna = validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    house = (lagna - where) % 12 + 1
    found = aspect_on_house(house)
    return {
        "house_to_lagna": house,
        "aspect": None if found is None else found["name"],
        "nature": None if found is None else found["nature"],
        "strength": None if found is None else found["strength"],
    }


def candidates(*, sun_rasi: int, moon_rasi: int, natal_lagna_rasi: int,
               muntha_rasi: int, annual_lagna_rasi: int, daytime: bool,
               chart: str = "annual") -> tuple[dict, ...]:
    """§28.6's five candidates for one annual chart, in its own order.

    The same graha may appear more than once; the cascade's tie-break counts
    how many of the five categories each one takes.

    :param chart: "annual" or "monthly". §28.7 repeats these five with the
        word changed in candidates (1), (4) and (5) — exactly the three that
        name the chart — and (2) and (3) left alone.
    """
    luminary = validate.in_range(
        "sun_rasi" if daytime else "moon_rasi",
        int(sun_rasi if daytime else moon_rasi), 0, 11)
    natal = validate.in_range("natal_lagna_rasi", int(natal_lagna_rasi), 0, 11)
    muntha = validate.in_range("muntha_rasi", int(muntha_rasi), 0, 11)
    annual = validate.in_range("annual_lagna_rasi", int(annual_lagna_rasi),
                               0, 11)
    picks = (
        ("1", int(RASI_LORD[luminary]),
         (f"lord of {RASI_NAMES[luminary]}, held by the "
          f"{'Sun' if daytime else 'Moon'} in the {chart} chart")),
        ("2", int(RASI_LORD[natal]),
         f"lord of the natal lagna {RASI_NAMES[natal]}"),
        ("3", int(RASI_LORD[muntha]),
         f"lord of the muntha {RASI_NAMES[muntha]}"),
        ("4", int(RASI_LORD[annual]),
         f"lord of the {chart} lagna {RASI_NAMES[annual]}"),
        ("5", triraasi_lord(annual, daytime=daytime)["lord"],
         f"triraasi lord of the {chart} lagna {RASI_NAMES[annual]}"),
    )
    return tuple({"category": number, "graha": graha,
                  "graha_name": str(GRAHA_NAMES[graha]), "because": why}
                 for number, graha, why in picks)


def varsheswara(*, sun_rasi: int, moon_rasi: int, natal_lagna_rasi: int,
                muntha_rasi: int, annual_lagna_rasi: int, daytime: bool,
                rasis: dict[int, int],
                pancha_vargeeya: dict[int, float | None]) -> dict:
    """§28.6's cascade, run to whichever step settles it.

    :param rasis: graha id to the rasi it occupies in the annual chart, which
        is what §28.2's aspect on lagna is measured from.
    :param pancha_vargeeya: graha id to its pancha vargeeya bala, or ``None``
        where §28.4 left it undecided. A candidate whose bala is unknown
        cannot be ranked, and the result says so rather than dropping it.
    """
    found = candidates(sun_rasi=sun_rasi, moon_rasi=moon_rasi,
                       natal_lagna_rasi=natal_lagna_rasi,
                       muntha_rasi=muntha_rasi,
                       annual_lagna_rasi=annual_lagna_rasi, daytime=daytime)
    return _run_cascade(found, int(annual_lagna_rasi), rasis,
                        pancha_vargeeya)


def _run_cascade(found: tuple[dict, ...], lagna_rasi: int,
                 rasis: dict[int, int],
                 pancha_vargeeya: dict[int, float | None]) -> dict:
    """§28.6's selection, shared by the year and the month.

    §28.7 says "the rest of the rules are the same", so the cascade is
    written once and given a different candidate list.
    """
    from hora.tajaka.panchavargeeya import pancha_vargeeya_grade

    annual = int(lagna_rasi)
    seen: dict[int, dict] = {}
    for entry in found:
        graha = int(entry["graha"])
        if graha not in seen:
            where = rasis.get(graha)
            aspect = (None if where is None
                      else aspect_on_lagna(int(where), annual))
            bala = pancha_vargeeya.get(graha)
            seen[graha] = {
                "graha": graha,
                "graha_name": entry["graha_name"],
                "categories": [],
                "rasi": where,
                "aspect": aspect,
                "pancha_vargeeya": bala,
                "grade": None if bala is None else pancha_vargeeya_grade(bala),
            }
        seen[graha]["categories"].append(entry["category"])

    unique = tuple(seen.values())
    unranked = tuple(row["graha"] for row in unique
                     if row["pancha_vargeeya"] is None)

    def natured(*wanted: str) -> tuple[dict, ...]:
        return tuple(row for row in unique
                     if row["aspect"] and row["aspect"]["nature"] in wanted)

    benefic = natured("benefic")
    any_aspect = tuple(row for row in unique
                       if row["aspect"] and row["aspect"]["aspect"])
    strong_aspect = tuple(row for row in any_aspect
                          if row["aspect"]["strength"] == "strong")

    step: str | None = None
    shortlist: tuple[dict, ...] = ()
    if benefic:
        step, shortlist = "benefic aspect on lagna", benefic
    elif natured("malefic"):
        step, shortlist = "malefic aspect accepted", natured("malefic")
    elif not any_aspect:
        step = "no aspect on lagna; a very strong candidate"
        shortlist = tuple(row for row in unique if row["grade"] == "very strong")
    if not shortlist and not strong_aspect:
        very = tuple(row for row in unique if row["grade"] == "very strong")
        if very:
            step, shortlist = "no strong aspect; a very strong candidate", very
        else:
            step = "fallback to candidate (1)"
            first = int(found[0]["graha"])
            shortlist = tuple(row for row in unique if row["graha"] == first)

    lord, undecided = None, None
    if shortlist and any(row["pancha_vargeeya"] is None for row in shortlist):
        undecided = ("a shortlisted candidate has no pancha vargeeya bala, so "
                     "the ranking cannot be made")
    elif shortlist:
        best = max(row["pancha_vargeeya"] for row in shortlist)
        tied = [row for row in shortlist if row["pancha_vargeeya"] == best]
        if len(tied) == 1:
            lord = tied[0]
        else:
            most = max(len(row["categories"]) for row in tied)
            by_count = [row for row in tied if len(row["categories"]) == most]
            if len(by_count) == 1:
                lord = by_count[0]
            else:
                undecided = ("two candidates share both the highest pancha "
                             "vargeeya bala and the same number of "
                             "categories; section 28.6 gives no third rule")

    return {
        "candidates": found,
        "distinct": unique,
        "unranked": unranked,
        "step": step,
        "shortlist": shortlist,
        "lord": lord,
        "lord_name": None if lord is None else lord["graha_name"],
        "undecided": undecided,
        "rule": SELECTION_PROCEDURE,
        "fallbacks": SELECTION_FALLBACKS,
        "cascade_caveat": THE_LAST_TWO_STEPS_TEST_DIFFERENT_THINGS,
    }


# --------------------------------------------------------------------------
# Example 120 — the lord of the year for Chart 66
# --------------------------------------------------------------------------

EXAMPLE_120 = (
    "Let us consider the annual chart in Example 118. Let us find the "
    "candidates for the lord of the year:")

#: The example's five candidacies, verbatim and in order.
EXAMPLE_120_CANDIDACIES: tuple[str, ...] = (
    ("The new year started at 4:41 am, i.e. night time. So we should take "
     "Moon and find the lord of the rasi occupied by him. Moon is in Pisces "
     "owned by Jupiter. So Jupiter gets the first candidacy."),
    "Natal lagna is in Leo. So Sun gets the second candidacy.",
    "Muntha is in Taurus. So Venus gets the third candidacy.",
    ("Lagna in the annual chart is in Capricorn. So Saturn gets the fourth "
     "candidacy."),
    ("Triraasi lord for lagna in Cp at night time is Mars, from Table 73. So "
     "Mars gets the fifth candidacy."),
)

EXAMPLE_120_CONCLUSION = (
    "The candidates are – Jupiter, Sun, Venus, Saturn and Mars. Of those, "
    "Venus occupies lagna and Jupiter and Saturn have a square aspect on "
    "lagna. All of them are malefic aspects. Sun has a semi-sextile aspect, "
    "which is neutral. Mars has a sextile aspect on Capricorn lagna from "
    "Pisces. He is also has the strongest panchavargeeya bala (13.7). So we "
    "conclude easily that Mars is the lord of the year.")

#: The example's own answers, as a fixture: candidate number to graha id.
EXAMPLE_120_CANDIDATES: dict[str, int] = {
    "1": 4, "2": 0, "3": 5, "4": 6, "5": 2}

#: And its reading of each candidate's aspect on the Capricorn lagna.
EXAMPLE_120_ASPECTS: dict[int, tuple[str, str]] = {
    5: ("Conjunction", "malefic"),
    4: ("Square aspect", "malefic"),
    6: ("Square aspect", "malefic"),
    0: ("Semi-sextile aspect", "neutral"),
    2: ("Sextile aspect", "benefic"),
}

EXAMPLE_120_LORD = 2
EXAMPLE_120_MARS_BALA = 13.7

#: **Finding.** The example never exercises the cascade past its first step.
#: Exactly one candidate has a benefic aspect on lagna, so the shortlist has
#: one member and the ranking by pancha vargeeya bala decides nothing — the
#: book cites Mars's 13.7 as corroboration, not as the deciding test. So
#: neither of OI-156's ambiguities is touched by the only worked example
#: §28.6 has.
THE_EXAMPLE_STOPS_AT_THE_SHORTLIST = (
    "Only Mars has a benefic aspect on the Capricorn lagna, so the shortlist "
    "has one member and nothing in Example 120 turns on the ranking, the "
    "tie-break or any of the fallbacks."
)

#: **Book defect.** The conclusion reads "He is also has the strongest
#: panchavargeeya bala" — an intruded "is". Recorded rather than corrected,
#: as the other slips are.
EXAMPLE_120_HAS_A_SLIP_IN_ITS_CONCLUSION = (
    "The conclusion prints \"He is also has the strongest panchavargeeya "
    "bala\" for \"He also has\". Nothing turns on it."
)


# --------------------------------------------------------------------------
# §28.7 — the lord of the month
# --------------------------------------------------------------------------

MONTH_LORD_RULE = (
    "We find the lord of the month in a monthly chart in the same manner. We "
    "have six candidates now:")

MONTH_LORD_REST = "The rest of the rules are the same."

#: §28.7's six candidates, verbatim and in order.
MONTH_LORD_CANDIDATES: tuple[dict[str, str], ...] = (
    {"number": "1",
     "candidate": "Lord of the rasi occupied by Sun or Moon in the monthly "
                  "chart, based on whether the new month starts during the "
                  "day or the night"},
    {"number": "2", "candidate": "Lord of natal lagna"},
    {"number": "3", "candidate": "Lord of Muntha"},
    {"number": "4", "candidate": "Lord of lagna in the monthly chart"},
    {"number": "5", "candidate": "Triraasi lord of lagna in the monthly chart "
                                 "(see Table 73)"},
    {"number": "6", "candidate": "Lord of the year"},
)

#: **Finding.** The six are §28.6's five with "annual" replaced by "monthly"
#: in three of them and one new candidate added. Candidates (2) and (3) are
#: word for word the same, so the natal lagna and the muntha are read the same
#: way for a month as for a year, and (6) brings the year's own lord into the
#: month's contest.
THE_SIX_ARE_THE_FIVE_WITH_ONE_ADDED = (
    "Candidates (1), (4) and (5) say monthly chart where section 28.6 said "
    "annual chart; (2) and (3) are unchanged; (6), the lord of the year, is "
    "new."
)

#: **Finding.** Candidate (6) is the output of another cascade, so it carries
#: every way that cascade can fail. If §28.6 returns no lord — because two
#: candidates tie on both tests, or because one has no pancha vargeeya bala —
#: then §28.7 has five candidates and not six, and the section does not say
#: what to do about it.
CANDIDATE_SIX_INHERITS_28_6S_FAILURES = (
    "The lord of the year is itself chosen by a cascade that can end without "
    "a lord. Section 28.7 lists it as a candidate and gives no reading for "
    "the case where there is none."
)

#: **Finding.** Candidate (3) needs a muntha for a **monthly** chart, and that
#: is exactly what §28.1 declines to define: it records that "some people"
#: progress the natal lagna by 2°30' a month and says "this author takes a
#: different stand" without stating it. So §28.7's third candidate rests on
#: OI-152. Two readings are open — the year's own muntha carried through all
#: twelve months, or a monthly one under a rule not given — and the section
#: chooses neither. `lord_of_the_month` takes the muntha rasi as an argument
#: and does not derive it.
CANDIDATE_THREE_RESTS_ON_OI_152 = (
    "Section 28.7 asks for the lord of muntha in a monthly chart. Section "
    "28.1 gives muntha for an annual chart, records a monthly rate it "
    "rejects, and never gives its own. Whether the month uses the year's "
    "muntha or one of its own is unstated."
)

#: **Finding.** §28.6's tie-break reads "the one becoming a candidate in more
#: of the **five** categories listed above", and §28.7 has six. "The rest of
#: the rules are the same" carries the rule across, so the count is read from
#: the list in force rather than from the printed word.
THE_TIE_BREAK_COUNTS_SIX_CATEGORIES_HERE = (
    "Section 28.6's tie-break names five categories and section 28.7 has six. "
    "The rule transfers with the list, so a month's tie-break counts over six."
)


def month_candidates(*, sun_rasi: int, moon_rasi: int, natal_lagna_rasi: int,
                     muntha_rasi: int, monthly_lagna_rasi: int,
                     daytime: bool, year_lord: int | None) -> tuple[dict, ...]:
    """§28.7's six candidates for one monthly chart.

    :param year_lord: the lord of the year from §28.6, or ``None`` when that
        cascade settled none. Omitted, candidate (6) is absent and the result
        says so rather than inventing one.
    :param muntha_rasi: supplied by the caller, because §28.1 does not define
        a monthly muntha — see `CANDIDATE_THREE_RESTS_ON_OI_152`.
    """
    monthly = candidates(sun_rasi=sun_rasi, moon_rasi=moon_rasi,
                         natal_lagna_rasi=natal_lagna_rasi,
                         muntha_rasi=muntha_rasi,
                         annual_lagna_rasi=monthly_lagna_rasi,
                         daytime=daytime, chart="monthly")
    if year_lord is None:
        return monthly
    lord = validate.in_range("year_lord", int(year_lord), 0, 6)
    return (*monthly, {"category": "6", "graha": lord,
                       "graha_name": str(GRAHA_NAMES[lord]),
                       "because": "lord of the year"})


def lord_of_the_month(*, sun_rasi: int, moon_rasi: int, natal_lagna_rasi: int,
                      muntha_rasi: int, monthly_lagna_rasi: int,
                      daytime: bool, year_lord: int | None,
                      rasis: dict[int, int],
                      pancha_vargeeya: dict[int, float | None]) -> dict:
    """§28.7's lord of the month. The section gives no Sanskrit name for it.

    "The rest of the rules are the same", so §28.6's cascade is run unchanged
    over the six candidates.
    """
    found = month_candidates(
        sun_rasi=sun_rasi, moon_rasi=moon_rasi,
        natal_lagna_rasi=natal_lagna_rasi, muntha_rasi=muntha_rasi,
        monthly_lagna_rasi=monthly_lagna_rasi, daytime=daytime,
        year_lord=year_lord)
    out = _run_cascade(found, int(monthly_lagna_rasi), rasis, pancha_vargeeya)
    return {**out,
            "year_lord": year_lord,
            "year_lord_missing": year_lord is None,
            "categories": len(found),
            "rule": MONTH_LORD_RULE,
            "same_rules": MONTH_LORD_REST,
            "muntha_caveat": CANDIDATE_THREE_RESTS_ON_OI_152}
