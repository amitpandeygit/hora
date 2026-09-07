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
               muntha_rasi: int, annual_lagna_rasi: int,
               daytime: bool) -> tuple[dict, ...]:
    """§28.6's five candidates for one annual chart, in its own order.

    The same graha may appear more than once; the cascade's tie-break counts
    how many of the five categories each one takes.
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
          f"{'Sun' if daytime else 'Moon'} in the annual chart")),
        ("2", int(RASI_LORD[natal]),
         f"lord of the natal lagna {RASI_NAMES[natal]}"),
        ("3", int(RASI_LORD[muntha]),
         f"lord of the muntha {RASI_NAMES[muntha]}"),
        ("4", int(RASI_LORD[annual]),
         f"lord of the annual lagna {RASI_NAMES[annual]}"),
        ("5", triraasi_lord(annual, daytime=daytime)["lord"],
         f"triraasi lord of the annual lagna {RASI_NAMES[annual]}"),
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
    from hora.tajaka.panchavargeeya import pancha_vargeeya_grade

    found = candidates(sun_rasi=sun_rasi, moon_rasi=moon_rasi,
                       natal_lagna_rasi=natal_lagna_rasi,
                       muntha_rasi=muntha_rasi,
                       annual_lagna_rasi=annual_lagna_rasi, daytime=daytime)
    annual = int(annual_lagna_rasi)
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
