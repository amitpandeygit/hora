"""Chapter 22 — Niryaana Shoola dasa, the dasa that times death.

The seventh of Part 2's nine, and the first **ayur** rasi dasa: chapters 18 to
21 all showed what life brings, this one shows when it ends. Four things make
it unlike every rasi dasa before it, and none of them can be carried over:

* its seed is the stronger of the **2nd and 8th** houses — not lagna and the
  7th (chapter 18), not Sree Lagna (chapter 20), and not the maraka pair
  either, which §14.2 gives as the 2nd and **7th**;
* the twelve rasis run in one plain sequence, forward or backward, with no
  groups — chapter 21's three groups were the exception, not the rule;
* its lengths are **fixed by modality**, 7, 8 and 9 years, so §18.2.2 is not
  used at all. Every chart's cycle is therefore the same 96 years;
* the comparison its seed needs is an **ayur** one, and §15.5.2 does not say
  how to make it. See :func:`seed` and OI-131.

Only the antardasas come from chapter 18, and they come from the author rather
than from the classics — see :data:`ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION`.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    MODALITY_NAMES,
    RASI_IS_ODD,
    RASI_MODALITY,
    RASI_NAMES,
)
from hora.dasha.rasi.narayana import NarayanaError


class NiryaanaShoolaError(NarayanaError):
    """A Niryaana Shoola input that cannot be resolved."""


# --------------------------------------------------------------------------
# §22.1 Introduction
# --------------------------------------------------------------------------

#: §22.1's derivation of the name.
NIRYAANA_MEANS_DEATH = (
    "Niryaana means death and shoola is a weapon of Lord Shiva, who is the "
    "lord of destruction."
)

#: What the chapter claims for it. Part 2's map calls its purpose "ayur"; this
#: is the sentence behind that.
ONE_OF_THE_MOST_RELIABLE = (
    "Niryaana Shoola dasa is one of the most reliable dasa systems for the "
    "timing of death."
)

#: §22.1's naming problem, and the reason the chapter's title is not the name
#: Parasara used. Part 2's map lists "Shoola dasa" separately, so the two are
#: two systems here as well.
THE_NAME_IS_DISAMBIGUATED = (
    "Parasara simply called it \"Shoola dasa\", but some scholars use the name "
    "Shoola dasa to denote a different dasa. We will learn it in another "
    "chapter. In order to avoid confusion, we will call the dasa to be learnt "
    "in this chapter as \"Niryaana Shoola dasa\"."
)

#: Footnote 59, which names the scholars — the author's own guru.
THE_OTHER_SHOOLA_DASAS_SCHOLARS = (
    "An example is my guru Pundit Sanjay Rath, author of \"Jaimini "
    "Maharishi's Upadesa Sutras\" and \"Crux of Vedic Astrology: Timing of "
    "Events\"."
)

#: Both names the chapter admits for this system, the classical one first.
NAMES = ("Shoola dasa", "Niryaana Shoola dasa")


# --------------------------------------------------------------------------
# §22.2.1 Computation
# --------------------------------------------------------------------------

#: Rule 1. The pair is the 2nd and the **8th**.
SEED_RULE = (
    "Find the stronger of the 2nd and 8th houses. Start from the rasi "
    "containing that house."
)

#: **Finding.** Easy to mistake for §14.2's maraka pair, which is the 2nd and
#: the **7th**. The 2nd is in both; the second house is not. §22.2.2 then reads
#: the maraka pair for the *interpretation*, so one chart uses both pairs for
#: different jobs.
SEED_PAIR_IS_NOT_THE_MARAKA_PAIR = (
    "Section 22.2.1 seeds from the stronger of the 2nd and 8th houses. "
    "Section 14.2's maraka sthanas are the 2nd and the 7th. The two pairs "
    "share only the 2nd, and this chapter uses both — the 2nd/8th to start "
    "the sequence and the 2nd/7th to read it."
)

#: Rule 2. Odd/even **sign**, as chapters 19 and 20 use, not the odd-footed
#: test of §18.2.1 and chapter 21. The two disagree on Taurus, Leo, Scorpio
#: and Aquarius.
DIRECTION_RULE = (
    "If the rasi is odd, go in the forward (zodiacal) direction and cover the "
    "12 rasis. If the rasi is even, go in the backward (anti-zodiacal) "
    "direction and cover the 12 rasis."
)

#: Rule 3, which replaces §18.2.2 outright.
LENGTH_RULE = (
    "Dasas of movable, fixed and dual rasis have 7, 8 and 9 years "
    "respectively."
)

#: Footnote 60. Two more systems share these lengths, so the years are not
#: this dasa's signature — the sequence is.
SHARED_DASA_YEARS = (
    "Sthira dasa, Mandooka dasa etc also use the same dasa years, though dasa "
    "sequences are different under those dasa systems."
)

#: Modality to years, from :data:`LENGTH_RULE`. Keyed by the names
#: ``MODALITY_NAMES`` uses.
MODALITY_YEARS: dict[str, int] = {"chara": 7, "sthira": 8, "dwiswabhava": 9}

#: Rule 4, and the reason it is tagged rather than merged into chapter 18's.
#: This is the author's suggestion, not Parasara's and not any classic's —
#: docs/precedence.md puts the book above BPHS but this sentence puts itself
#: below both by admitting there is nothing to be above.
ANTARDASAS_ARE_THE_AUTHORS_SUGGESTION = (
    "Classics are not clear about how we go about finding antardasas. This "
    "author suggests using the same rules used for Narayana dasa."
)


def direction_of(seed_sign: int) -> str:
    """The run's direction, from the seed rasi being an odd or even **sign**.

    Not the odd-footed test §18.2.1 and §21.2 use; they disagree on Taurus,
    Leo, Scorpio and Aquarius.
    """
    index = validate.in_range("seed_sign", seed_sign, 0, 11)
    return "forward" if RASI_IS_ODD[index] else "backward"


def dasa_years(rasi: int) -> int:
    """A rasi's dasa length in years — 7, 8 or 9, by its modality alone.

    Nothing about the chart enters: no lord, no dignity, no exceptions. A
    Niryaana Shoola dasa length is the same on every chart ever cast.
    """
    index = validate.in_range("rasi", rasi, 0, 11)
    return MODALITY_YEARS[str(MODALITY_NAMES[RASI_MODALITY[index]])]


def cycle_years() -> int:
    """The whole twelve-dasa cycle, which is the same for every chart.

    Four rasis of each modality, so 4 * (7 + 8 + 9).
    """
    return sum(dasa_years(rasi) for rasi in range(12))


@dataclass(frozen=True, slots=True)
class Seed:
    """Which of the 2nd and 8th houses starts the run, or why it is unsettled."""

    lagna: int
    second: int
    second_name: str
    eighth: int
    eighth_name: str
    #: The winner, when the caller supplied one. None while §15.5.2 cannot say.
    sign: int | None
    sign_name: str | None
    undecided: str | None
    why: str


def seed(lagna: int, *, stronger_house: int | None = None) -> Seed:
    """§22.2.1's starting rasi — the stronger of the 2nd and the 8th.

    :param stronger_house: 2 or 8, when the caller has settled the comparison.
        Omitted, both candidates are returned with the reason it is open.

    The comparison itself is not made here, and that is not an omission.
    §15.5.2 carries its own warning that its rules must be adapted to the
    purpose, and names **ayur dasas** — dasas that show longevity — as a
    purpose whose rule 2 reads the luminaries instead of Jupiter, Mercury and
    the lord. It does not say how to weigh those aspects, so
    :func:`hora.charts.rasi_strength.stronger` refuses ``purpose="ayur"``
    rather than guessing. Answering with the phalita cascade would be
    answering a different question. See OI-131.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    second = (index + 1) % 12
    eighth = (index + 7) % 12
    houses = {2: second, 8: eighth}

    if stronger_house is None:
        return Seed(
            lagna=index, second=second, second_name=str(RASI_NAMES[second]),
            eighth=eighth, eighth_name=str(RASI_NAMES[eighth]),
            sign=None, sign_name=None,
            undecided=(
                "which of the 2nd and 8th is stronger. This is an ayur dasa "
                "and §15.5.2's ayur adaptation reads the luminaries without "
                "saying how to weigh the other aspects, so the cascade cannot "
                "be run for it; see OI-131"),
            why=(f"the 2nd from {RASI_NAMES[index]} is {RASI_NAMES[second]} "
                 f"and the 8th is {RASI_NAMES[eighth]}"))

    if stronger_house not in houses:
        raise NiryaanaShoolaError(
            f"stronger_house must be 2 or 8, got {stronger_house!r}")
    chosen = houses[stronger_house]
    return Seed(
        lagna=index, second=second, second_name=str(RASI_NAMES[second]),
        eighth=eighth, eighth_name=str(RASI_NAMES[eighth]),
        sign=chosen, sign_name=str(RASI_NAMES[chosen]), undecided=None,
        why=(f"the caller made the {stronger_house}th house "
             f"({RASI_NAMES[chosen]}) the stronger"))


@dataclass(frozen=True, slots=True)
class Progression:
    """The twelve Niryaana Shoola dasas of one chart, in order."""

    seed: int
    seed_name: str
    direction: str
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    years: tuple[int, ...]
    #: Cumulative age in years at which each dasa opens.
    starts: tuple[int, ...]
    why: str


def progression(seed_sign: int) -> Progression:
    """§22.2.1's twelve dasas from a seed rasi.

    One plain run of twelve, unlike chapter 21's three groups — "cover the 12
    rasis" is said of each direction, so the run is always all twelve distinct
    rasis and OI-127 has no analogue here.
    """
    index = validate.in_range("seed_sign", seed_sign, 0, 11)
    direction = direction_of(index)
    step = 1 if direction == "forward" else -1
    signs = tuple((index + step * offset) % 12 for offset in range(12))
    years = tuple(dasa_years(sign) for sign in signs)

    starts, elapsed = [], 0
    for length in years:
        starts.append(elapsed)
        elapsed += length

    return Progression(
        seed=index, seed_name=str(RASI_NAMES[index]), direction=direction,
        signs=signs, sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        years=years, starts=tuple(starts),
        why=(f"{RASI_NAMES[index]} is an "
             f"{'odd' if RASI_IS_ODD[index] else 'even'} sign, so the twelve "
             f"rasis run {direction}"))


# --------------------------------------------------------------------------
# §22.2.2 Interpretation
# --------------------------------------------------------------------------

#: §22.2.2's three ways a dasa can bring death, in the order the section gives
#: them — the third is explicitly the fallback for the second.
DEATH_READINGS: tuple[dict, ...] = (
    {"rule": 1, "reads": "marakas",
     "test": "the dasa rasi is a strong maraka rasi, or contains a strong "
             "maraka graha",
     "needs": "which marakas are strong; §14.2 gives no ranking",
     "text": ("Dasa of strong maraka rasis and dasas of rasis containing "
              "strong maraka grahas can bring death.")},
    {"rule": 2, "reads": "Trishoola",
     "test": "the dasa rasi is the Trishoola rasi its longevity category "
             "selects",
     "needs": "the longevity category and the chart's dasa spans; Example 84 "
              "selects the Trishoola whose dasa falls in the range",
     "text": ("Usually death occurs in the dasa of a Trishoola rasi. There "
              "are three Trishoola rasis and we can identify the correct rasi "
              "based on the longevity category (short, middle or long life).")},
    {"rule": 3, "reads": "Rudra",
     "test": "the dasa rasi is the one holding Rudra in the 12th house",
     "needs": "which rasi that sentence names; see OI-130",
     "text": ("If Trishoolas don't bring death, the rasi containing Rudra in "
              "the 12th house can bring death.")},
)

#: §14.3 already pointed forward to this chapter: its Trishoola rule says one
#: of the three "kills the native during its Shoola dasa". §22.2.2 is the other
#: half of that sentence.
TRISHOOLA_WAS_PROMISED_IN_14_3 = (
    "Depending on whether a native has short life or middle life or long "
    "life, one of the three Trishoola rasis kills the native during its "
    "Shoola dasa."
)

#: Example 84 settles how the category chooses. It is **not** a mapping of
#: short/middle/long onto the three positions: it is whichever Trishoola's
#: *dasa* falls inside the range the category names. So the answer depends on
#: the seed, and the same three Trishoolas can select differently on two charts.
THE_TRISHOOLA_IS_THE_ONE_WHOSE_DASA_IS_IN_RANGE = (
    "We found in Exercise 23 that Ge, Li and Aq form Trishoola and the native "
    "has middle life. Ge is the only Trishoola rasi whose dasa comes in the "
    "middle life range (36-72 years)."
)

#: **Gap.** Example 84's "only" is doing work its rule does not guarantee. The
#: three Trishoolas are four rasis apart, so in a run averaging eight years
#: each their dasas are about thirty-two years apart, and every longevity range
#: is thirty-six years wide. Two can land in one range. See OI-133.
MORE_THAN_ONE_TRISHOOLA_CAN_FALL_IN_RANGE = (
    "Example 84 selects the Trishoola whose dasa falls in the longevity range "
    "and its chart had exactly one. The three Trishoolas are trines, so their "
    "dasas are roughly thirty-two years apart in a ninety-six year cycle, "
    "while each longevity range is thirty-six years wide. Nothing in section "
    "22.2.2 or section 14.3 says which to take when two qualify."
)

#: **Gap.** Rule 3's sentence has more than one defensible reading. See
#: OI-130 and :func:`rudra_fallback`.
RUDRA_FALLBACK_IS_AMBIGUOUS = (
    "If Trishoolas don't bring death, the rasi containing Rudra in the 12th "
    "house can bring death."
)

#: §22.2.2's antardasa rule, the two principles and their intersection.
ANTARDASA_AT_DEATH_RULE = (
    "Antardasa at the time of death can be the 6th, 7th, 8th or 12th rasi "
    "from dasa rasi. It can also be a rasi that aspects the rasi that, in "
    "navamsa, contains the owner of the 8th house from dasa rasi. ... If "
    "there is a common rasi between these two principles, it can be a strong "
    "candidate."
)

#: The section's own worked illustration, as data.
ANTARDASA_EXAMPLE = (
    "Suppose dasa rasi at death is Ta and Jupiter is in Le in navamsa. Then "
    "the antardasas of the 6th, 7th, 8th and 12th houses from Ta (i.e. Li, "
    "Sc, Sg and Ar) can bring death. Also the antardasas of Ar, Le, Li and "
    "Cp - rasis that aspect Le, which contains Jupiter in navamsa - can bring "
    "death."
)

#: The houses principle 1 takes from the dasa rasi.
ANTARDASA_HOUSES: tuple[int, ...] = (6, 7, 8, 12)

#: **Finding.** "Rasis that aspect Le" is listed as "Ar, Le, Li and Cp" — Leo
#: itself included, though no rasi aspects itself under rasi drishti. The same
#: idiom appears in Example 80, where "the signs that aspect Ge" are given as
#: "Ge, Vi, Sg and Pi". So the book's phrase means the rasi together with
#: those that aspect it, in both chapters.
ASPECTING_INCLUDES_THE_RASI_ITSELF = (
    "Also the antardasas of Ar, Le, Li and Cp - rasis that aspect Le, which "
    "contains Jupiter in navamsa - can bring death."
)


def maraka_readings(dasa_rasi: int, lagna: int,
                    signs: dict[int, int] | None = None) -> dict:
    """Rule 1 — whether a dasa rasi is or holds a maraka.

    :param signs: rasi per graha. Needed to see which marakas the dasa rasi
        holds, and for §14.2's second kind of maraka graha.

    "Strong" is left unjudged: §14.2 gives no ranking and says so in
    ``MARAKA_STRONGER_NOT_A_RULE``. Every qualification is reported with how
    it was earned.
    """
    from hora.charts.maraka import maraka_sthanas, marakas

    rasi = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    index = validate.in_range("lagna", lagna, 0, 11)

    sthanas = maraka_sthanas(index)
    is_sthana = [house for house, sign in sthanas.items() if sign == rasi]

    found = marakas(index, signs)
    holds = tuple(
        entry for entry in found["maraka_grahas"]
        if signs is not None and signs.get(entry["graha"]) == rasi)

    return {
        "is_maraka_sthana": tuple(is_sthana),
        "holds_maraka_grahas": holds,
        "applies": bool(is_sthana or holds),
        "malefic_contacts_included": found["malefic_contacts_included"],
        "undecided": ("which marakas are strong; §14.2 ranks none"
                      if (is_sthana or holds) else None),
    }


def trishoola_readings(dasa_rasi: int, rudra_sign: int,
                       longevity: str | None = None) -> dict:
    """Rule 2 — whether a dasa rasi is one of the three Trishoolas.

    :param rudra_sign: the rasi Rudra occupies, from
        :func:`hora.charts.maraka.rudra`.
    :param longevity: "short", "middle" or "long". Recorded here; the
        selection among the three needs the dasa spans as well, so it lives in
        :func:`select_trishoola`.
    """
    from hora.charts.maraka import trishoola_rasis

    rasi = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    validate.in_range("rudra_sign", rudra_sign, 0, 11)
    three = trishoola_rasis(rudra_sign)

    from hora.core.constants.maraka import LONGEVITY_RANGES
    if longevity is not None and longevity not in LONGEVITY_RANGES:
        raise NiryaanaShoolaError(
            f"longevity must be one of {tuple(LONGEVITY_RANGES)}, "
            f"got {longevity!r}")

    return {
        "trishoolas": three,
        "trishoola_names": tuple(str(RASI_NAMES[s]) for s in three),
        "applies": rasi in three,
        "position": three.index(rasi) if rasi in three else None,
        "longevity": longevity,
    }


def select_trishoola(rudra_sign: int, run: Progression,
                     longevity: str) -> dict:
    """Which of the three Trishoolas the longevity category selects.

    Example 84's rule, and it is not the mapping it looks like: the category
    does not own a position among the three. It names a range of years, and
    the Trishoola whose **dasa falls in that range** is the one — "Ge is the
    only Trishoola rasi whose dasa comes in the middle life range (36-72
    years)". The answer therefore depends on the seed, so two charts with the
    same Rudra can select different spikes.

    :param run: the chart's :func:`progression`, which supplies the spans.
    :returns: every Trishoola with its span and whether it overlaps the range,
        the selection when exactly one does, and ``undecided`` otherwise. See
        OI-133 for why more than one can.
    """
    from hora.charts.maraka import trishoola_rasis
    from hora.core.constants.maraka import LONGEVITY_RANGES

    validate.in_range("rudra_sign", rudra_sign, 0, 11)
    if longevity not in LONGEVITY_RANGES:
        raise NiryaanaShoolaError(
            f"longevity must be one of {tuple(LONGEVITY_RANGES)}, "
            f"got {longevity!r}")
    low, high = LONGEVITY_RANGES[longevity]

    spans = {sign: (run.starts[i], run.starts[i] + run.years[i])
             for i, sign in enumerate(run.signs)}
    rows = []
    for sign in trishoola_rasis(rudra_sign):
        start, end = spans[sign]
        rows.append({
            "sign": sign, "rasi": str(RASI_NAMES[sign]),
            "starts": start, "ends": end,
            "in_range": start < high and end > low,
            "wholly_in_range": start >= low and end <= high,
        })

    qualifying = [row for row in rows if row["in_range"]]
    chosen = qualifying[0] if len(qualifying) == 1 else None
    return {
        "longevity": longevity,
        "range": (low, high),
        "trishoolas": tuple(rows),
        "selected": chosen,
        "undecided": (
            None if chosen is not None else
            (f"{len(qualifying)} of the three Trishoolas have their dasa in "
             f"the {longevity}-life range; §22.2.2 says which to take only "
             f"when there is one. See OI-133")),
    }


def rudra_fallback(rudra_sign: int, lagna: int) -> dict:
    """Rule 3's rasi — as far as the sentence can be taken.

    "If Trishoolas don't bring death, the rasi containing Rudra in the 12th
    house can bring death" admits more than one reading, and the section gives
    no example. Two survive its own premise:

    * **the 12th from the rasi containing Rudra** — never a Trishoola, since
      the Trishoolas are the trines from that rasi and the 12th is not one, so
      it always answers the "if Trishoolas don't" case;
    * **the 12th house from lagna** — which may itself be a Trishoola on a
      given chart, and then the sentence would be offering back a rasi its own
      premise has just excluded.

    A third reading — Rudra's own rasi, when it falls in the 12th house — is
    reported as ruled out, not merely unlikely: Rudra's rasi is the first
    Trishoola, so the premise excludes it on every chart.

    Nothing is chosen here. See OI-130.
    """
    from hora.charts.maraka import trishoola_rasis

    rudra = validate.in_range("rudra_sign", rudra_sign, 0, 11)
    index = validate.in_range("lagna", lagna, 0, 11)

    twelfth_from_rudra = (rudra + 11) % 12
    twelfth_from_lagna = (index + 11) % 12
    three = trishoola_rasis(rudra)

    return {
        "readings": (
            {"reading": "the 12th from the rasi containing Rudra",
             "sign": twelfth_from_rudra,
             "rasi": str(RASI_NAMES[twelfth_from_rudra]),
             "is_a_trishoola": twelfth_from_rudra in three,
             "note": ("never a Trishoola, so it always answers the "
                      "\"if Trishoolas don't\" case")},
            {"reading": "the 12th house from lagna",
             "sign": twelfth_from_lagna,
             "rasi": str(RASI_NAMES[twelfth_from_lagna]),
             "is_a_trishoola": twelfth_from_lagna in three,
             "note": ("can itself be a Trishoola, and is on this chart"
                      if twelfth_from_lagna in three else
                      "not a Trishoola on this chart")},
        ),
        "ruled_out": {
            "reading": "Rudra's own rasi, when it falls in the 12th house",
            "sign": rudra, "rasi": str(RASI_NAMES[rudra]),
            "why": ("Rudra's rasi is the first Trishoola, so the rule's own "
                    "premise excludes it on every chart"),
        },
        "undecided": ("which rasi §22.2.2's last sentence names; the section "
                      "gives no example. See OI-130"),
    }


def antardasa_candidates(dasa_rasi: int, navamsa_signs: dict[int, int],
                         eighth_lord: int | None = None) -> dict:
    """§22.2.2's antardasas that can bring death, by both its principles.

    :param navamsa_signs: rasi per graha **in the navamsa**, from
        :func:`hora.charts.vargas.varga`. Only the 8th lord's is read.
    :param eighth_lord: supply it when the 8th from the dasa rasi is Scorpio
        or Aquarius, whose lord §15.5.1 must settle. Refused rather than
        guessed, as :func:`hora.dasha.rasi.narayana.varga_lagna` refuses.

    The second principle's "rasis that aspect" includes the rasi itself, which
    the section's own list shows — see
    :data:`ASPECTING_INCLUDES_THE_RASI_ITSELF`.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.charts.colord import CO_LORDS
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    rasi = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    eighth = (rasi + 7) % 12

    if eighth_lord is None:
        if eighth in CO_LORDS:
            raise NiryaanaShoolaError(
                f"the 8th from {RASI_NAMES[rasi]} is {RASI_NAMES[eighth]}, "
                f"which §15.5.1 must settle between "
                f"{' and '.join(str(GRAHA_NAMES[g]) for g in CO_LORDS[eighth])}"
                f"; pass eighth_lord")
        lord = int(RASI_LORD[eighth])
    else:
        lord = validate.in_range("eighth_lord", int(eighth_lord), 0, 8)

    if lord not in navamsa_signs:
        raise NiryaanaShoolaError(
            f"the navamsa rasi of {GRAHA_NAMES[lord]} was not given")
    in_navamsa = validate.in_range(
        "navamsa sign", int(navamsa_signs[lord]), 0, 11)

    from_dasa = tuple((rasi + house - 1) % 12 for house in ANTARDASA_HOUSES)
    aspecting = (in_navamsa,) + tuple(
        s for s in range(12) if in_navamsa in rasi_drishti(s))
    common = tuple(s for s in from_dasa if s in aspecting)

    return {
        "dasa_rasi": rasi,
        "eighth": eighth, "eighth_name": str(RASI_NAMES[eighth]),
        "eighth_lord": lord, "eighth_lord_name": str(GRAHA_NAMES[lord]),
        "navamsa_sign": in_navamsa,
        "navamsa_rasi": str(RASI_NAMES[in_navamsa]),
        "from_dasa_rasi": from_dasa,
        "from_dasa_rasi_names": tuple(str(RASI_NAMES[s]) for s in from_dasa),
        "aspecting_the_navamsa_rasi": aspecting,
        "aspecting_names": tuple(str(RASI_NAMES[s]) for s in aspecting),
        "strong_candidates": common,
        "strong_candidate_names": tuple(str(RASI_NAMES[s]) for s in common),
        "why": (f"the 8th from {RASI_NAMES[rasi]} is {RASI_NAMES[eighth]}, "
                f"whose lord {GRAHA_NAMES[lord]} is in "
                f"{RASI_NAMES[in_navamsa]} in navamsa"),
    }
