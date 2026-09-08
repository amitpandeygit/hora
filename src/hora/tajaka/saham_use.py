"""§28.8.2 — Use of sahams.

Two rules of use, one for the annual chart and one for the natal chart, and
a note on where the Tajaka system came from. The section is short and mostly
prose; what can be computed is computed here and what the section leaves open
is named rather than filled in.
"""

from __future__ import annotations

from hora.charts.aspects import graha_drishti_houses
from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_LORD, RASI_NAMES, Graha
from hora.tajaka.aspects import aspects_from

SECTION_TITLE = "Use of sahams"


# --------------------------------------------------------------------------
# The annual-chart rule
# --------------------------------------------------------------------------

#: §28.8.2's first sentence, verbatim.
USE_IN_ANNUAL_CHART = (
    "If there are good yogas in an annual chart involving the lord of the "
    "rasi containing an important saham and lagna lord, then important events "
    "related to the matter of the saham may materialize during the year."
)

#: **Gap.** The rule needs three things and supplies one. The lord of the
#: rasi containing the saham is computable, and so is the lagna lord. **Which
#: sahams are "important"** is not said — Table 74 prints thirty-six and ranks
#: none of them — and **which yogas are "good"** is not narrowed either. The
#: chapters on yogas run to hundreds; the section does not say whether it
#: means those, or the Tajaka yogas, or something looser.
THE_RULE_NAMES_NEITHER_THE_SAHAM_NOR_THE_YOGA = (
    "Section 28.8.2 asks for good yogas involving the lord of an important "
    "saham's rasi and the lagna lord. It does not say which of Table 74's "
    "thirty-six sahams are important, and it does not say which yogas count "
    "as good."
)

#: **Finding.** The two grahas the rule pairs can be the **same graha**, and
#: often are: the saham's dispositor is the lagna lord whenever the saham
#: falls in a rasi the lagna lord owns, which for the five two-rasi lords is
#: two signs in twelve. A yoga "involving" one graha and itself is not a yoga,
#: so the rule has no content in those charts and the section does not say
#: what to do instead.
THE_TWO_LORDS_CAN_BE_ONE_GRAHA = (
    "The lord of the saham's rasi and the lagna lord are the same graha "
    "whenever the saham falls in a rasi the lagna lord owns. The rule asks "
    "for a yoga between them, and a graha forms none with itself."
)


def saham_dispositor(longitude: float) -> dict:
    """The lord of the rasi a saham falls in — the rule's first term."""
    seat = validate.longitude("longitude", float(longitude))
    rasi = int(seat // 30)
    lord = int(RASI_LORD[rasi])
    return {
        "longitude": seat,
        "rasi": rasi,
        "rasi_name": str(RASI_NAMES[rasi]),
        "lord": lord,
        "lord_name": str(GRAHA_NAMES[lord]),
    }


def annual_rule_terms(*, saham_longitude: float, lagna: float) -> dict:
    """The pair §28.8.2 asks for a yoga between, and whether it is a pair.

    Whether the yoga is present, and whether it is "good", is not decided
    here — the section narrows neither. See
    `THE_RULE_NAMES_NEITHER_THE_SAHAM_NOR_THE_YOGA`.
    """
    seat = validate.longitude("lagna", float(lagna))
    lagna_rasi = int(seat // 30)
    lagna_lord = int(RASI_LORD[lagna_rasi])
    disp = saham_dispositor(saham_longitude)
    same = disp["lord"] == lagna_lord
    return {
        "saham_dispositor": disp,
        "lagna_rasi": lagna_rasi,
        "lagna_rasi_name": str(RASI_NAMES[lagna_rasi]),
        "lagna_lord": lagna_lord,
        "lagna_lord_name": str(GRAHA_NAMES[lagna_lord]),
        "grahas": (disp["lord"],) if same else (disp["lord"], lagna_lord),
        "is_one_graha": same,
        "yoga_undecided": THE_RULE_NAMES_NEITHER_THE_SAHAM_NOR_THE_YOGA,
        "rule": USE_IN_ANNUAL_CHART,
    }


# --------------------------------------------------------------------------
# The natal-chart rule
# --------------------------------------------------------------------------

#: §28.8.2's second paragraph, verbatim.
USE_IN_NATAL_CHART = (
    "We can also use sahams in natal charts. When Saturn or Rahu transits "
    "close to natal paradesa saham or jalapatana saham, for example, one may "
    "go abroad. When Jupiter occupies or aspects natal vivaha saham in "
    "transit, one may get married. Thus we can use sahams in natal charts "
    "also."
)

#: The paragraph's two rules as data. ``test`` is the section's own wording,
#: and it differs between them — see `ONE_RULE_NEEDS_AN_ORB_AND_ONE_DOES_NOT`.
NATAL_SAHAM_TRANSITS: tuple[dict[str, object], ...] = (
    {"sahams": ("Paradesa", "Jalapatana"),
     "transiting": (int(Graha.SATURN), int(Graha.RAHU)),
     "test": "transits close to", "needs_an_orb": True,
     "gives": "one may go abroad"},
    {"sahams": ("Vivaha",),
     "transiting": (int(Graha.JUPITER),),
     "test": "occupies or aspects", "needs_an_orb": False,
     "gives": "one may get married"},
)

#: **Finding.** The paragraph states its two rules in **different frames**.
#: Saturn and Rahu must transit "close to" a point, which needs an orb the
#: book has never given — §25.3 said "close to" as well and OI-116 recorded
#: it. Jupiter must "occupy or aspect", which is a **rasi** test and needs no
#: orb at all. So one of the two saham-transit rules in the book is fully
#: decidable and the other is not, and the difference is in the wording, not
#: in the technique.
ONE_RULE_NEEDS_AN_ORB_AND_ONE_DOES_NOT = (
    "Saturn and Rahu transit \"close to\" a saham, which needs an orb the "
    "book does not give. Jupiter \"occupies or aspects\" it, which is a rasi "
    "test and needs none. The Jupiter rule is the only saham transit in the "
    "book that can be answered outright."
)

#: **Finding.** §25.3 and §28.8.2 both read **vivaha saham** for marriage and
#: they do not agree. §25.3: "when the 7th lord or Venus transits close to
#: vivaha saham, one may get married." §28.8.2: "when Jupiter occupies or
#: aspects natal vivaha saham in transit, one may get married." Different
#: grahas, a different test, the same saham and the same event. Neither
#: section mentions the other and neither is said to replace it, so both are
#: held.
TWO_SECTIONS_READ_VIVAHA_SAHAM_DIFFERENTLY = (
    "Section 25.3 gives the 7th lord or Venus transiting close to vivaha "
    "saham; section 28.8.2 gives Jupiter occupying or aspecting it. Three "
    "different grahas and two different tests for one event."
)

#: **Finding, and evidence on that gap.** §28.2's aspects cover every house
#: but the 6th and the 8th, so a Tajaka reading has Jupiter aspecting **nine
#: rasis of the eleven he does not occupy**, and the marriage rule would fire
#: in ten charts of twelve. Chapter 10's graha drishti gives him three. The
#: Tajaka reading does not make the rule wrong, but it makes it nearly
#: contentless, which is evidence for the natal reading and not proof of it.
#: Recorded; not decided. See OI-158.
THE_TAJAKA_READING_WOULD_FIRE_ALMOST_ALWAYS = (
    "Under section 28.2's aspects Jupiter reaches ten of the twelve rasis, "
    "so the vivaha rule would be satisfied in ten charts out of twelve. "
    "Under chapter 10's graha drishti he reaches four, counting his own."
)

#: **Gap.** "Aspects" is not qualified. The sentence says *natal* chart, which
#: points at chapter 10's graha drishti — Jupiter's 5th, 7th and 9th — but
#: §28.2 has just defined a different set of Tajaka aspects for the same
#: planet, and the reader is three pages past it. `jupiter_on_vivaha` returns
#: **both** answers and does not choose.
WHICH_ASPECT_SCHEME_IS_NOT_SAID = (
    "Section 28.8.2 says Jupiter aspects natal vivaha saham without saying "
    "under which scheme. Chapter 10's graha drishti and section 28.2's "
    "Tajaka aspects give different rasis for Jupiter."
)


def jupiter_on_vivaha(*, jupiter_rasi: int, vivaha_rasi: int) -> dict:
    """Whether transiting Jupiter occupies or aspects natal vivaha saham.

    Both aspect schemes are reported. §28.8.2 does not say which it means —
    see `WHICH_ASPECT_SCHEME_IS_NOT_SAID` — so neither is presented as the
    answer and `agree` says whether the choice matters in this chart.
    """
    here = validate.in_range("jupiter_rasi", int(jupiter_rasi), 0, 11)
    there = validate.in_range("vivaha_rasi", int(vivaha_rasi), 0, 11)
    occupies = here == there

    parasari = tuple((here + h - 1) % 12
                     for h in graha_drishti_houses(int(Graha.JUPITER)))
    # The 1st is the conjunction, which is `occupies` and is reported there,
    # so it is dropped to make the two schemes comparable — graha drishti
    # never counts a graha's own rasi.
    tajaka = tuple((here + int(row["house"]) - 1) % 12
                   for row in aspects_from(here) if int(row["house"]) != 1)

    by_graha_drishti = occupies or there in parasari
    by_tajaka = occupies or there in tajaka
    return {
        "occupies": occupies,
        "aspects_by_graha_drishti": there in parasari,
        "aspects_by_tajaka": there in tajaka,
        "hit_by_graha_drishti": by_graha_drishti,
        "hit_by_tajaka": by_tajaka,
        "agree": by_graha_drishti == by_tajaka,
        "undecided": None if by_graha_drishti == by_tajaka
                     else WHICH_ASPECT_SCHEME_IS_NOT_SAID,
    }


def saturn_or_rahu_near(*, graha_longitude: float, saham_longitude: float,
                        orb: float | None = None) -> dict:
    """How far a transiting Saturn or Rahu is from a saham.

    "Close to" is given no orb anywhere in the book, so `orb` has no default
    and the answer is **undecided** without one. The separation is returned
    either way, so a caller who has settled an orb can decide.
    """
    body = validate.longitude("graha_longitude", float(graha_longitude))
    point = validate.longitude("saham_longitude", float(saham_longitude))
    gap = abs(((body - point + 180.0) % 360.0) - 180.0)
    if orb is None:
        return {"separation": gap, "close": None,
                "undecided": ONE_RULE_NEEDS_AN_ORB_AND_ONE_DOES_NOT}
    width = validate.positive("orb", float(orb))
    return {"separation": gap, "close": gap <= width, "orb": width,
            "undecided": None}


# --------------------------------------------------------------------------
# The note on where Tajaka came from
# --------------------------------------------------------------------------

#: The section's note, verbatim.
ARABIAN_PARTS_NOTE = (
    "In western astrology, there are Arabian parts (e.g. part of fortune) "
    "which are similar to sahams. In fact, there are a lot of similarities "
    "between the techniques in Tajaka system and western astrology."
)

#: The paragraph that follows it, verbatim. It is the book's own view of where
#: the Tajaka system came from, and it is offered as speculation twice over —
#: "this is possible" and "one may speculate".
TAJAKA_ORIGIN_SPECULATION = (
    "Some people may suggest that Indians learnt Tajaka system from Arabs. "
    "This is possible. However, one must note that astrology as practiced in "
    "India is much superior in width and depth to astrology practiced in any "
    "other part of the world. Indian astrology is a big superset of which "
    "different astrological traditions of the world are but small subsets. "
    "One may speculate that Vedic astrology as taught by Parasara, Jaimini, "
    "Manu etc was very exhaustive in scope and experts in different branches "
    "of it traveled to different parts of the world in ancient times to "
    "establish the knowledge there."
)

#: **Finding, and a correction to §25.4's note.** §25.4 was recorded as the
#: only section carrying a provenance. It is the only one that labels its own
#: **technique** — "this author's own researches". §28.8.2 carries a
#: provenance of a different kind: where the **system** came from. Neither
#: changes what is computed, and this one changes nothing at all — it is a
#: historical claim with no calculation attached, so it is transcribed and
#: left there.
THE_ORIGIN_NOTE_CHANGES_NOTHING_COMPUTED = (
    "Section 28.8.2's closing paragraph is a claim about the history of the "
    "Tajaka system. No rule in the chapter depends on it and nothing is "
    "computed from it."
)
