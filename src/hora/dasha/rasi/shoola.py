"""Chapter 23 — Shoola dasa, the *other* one.

§22.1 renamed the previous chapter's system "Niryaana Shoola dasa" precisely to
leave this name free: "some scholars use the name Shoola dasa to denote a
different dasa. We will learn it in another chapter." This is that chapter.

The eighth of Part 2's nine, and the simplest rasi dasa in the book. Three
things it does that nothing before it does:

* it has **no direction rule** — "dasas start there and *always* go in the
  regular zodiacal order", the word italicised in the book. No odd/even test,
  no odd-footed test, and no Saturn or Ketu exception;
* every dasa is **9 years flat**, so the cycle is 108 — the paramaayush of
  §14.4's longevity table, which is unlikely to be a coincidence;
* its antardasas are **self-similar**: "the same rules as dasas, but treating
  dasa rasi as lagna", where chapter 22 borrowed §18.3 from Narayana.

The 9 is not arbitrary either. §23.2 grounds it in gestation and generalises
it to other species — see :data:`GESTATION_RULE`.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.dasha.rasi.narayana import NarayanaError


class ShoolaError(NarayanaError):
    """A Shoola dasa input that cannot be resolved."""


# --------------------------------------------------------------------------
# §23.1 Introduction
# --------------------------------------------------------------------------

#: §23.1's scope, and it is wider than chapter 22's. Niryaana Shoola dasa times
#: death; this one also shows disease, suffering, and **other people's** deaths.
SHOWS = (
    "There is another dasa called Shoola dasa that can also be used for "
    "timing death. It shows death, diseases, suffering and death of relatives."
)

#: The two systems are two, and §22.1 said so before this chapter arrived.
THE_OTHER_SHOOLA_DASA = (
    "We looked at \"Niryaana Shoola dasa\" used for timing one's death. There "
    "is another dasa called Shoola dasa that can also be used for timing "
    "death."
)


# --------------------------------------------------------------------------
# §23.2 Computation
# --------------------------------------------------------------------------

#: Rule 1. The same pair Narayana dasa seeds from, and not chapter 22's 2nd and
#: 8th — three different pairs across the six rasi dasas built so far.
SEED_RULE = "Find the stronger of lagna and the 7th house."

#: Rule 2, and the book italicises the word. No rasi dasa before this one runs
#: in a fixed direction: §18.2.1 tests odd-footedness, §19.2 and §20.2 test the
#: odd/even sign and carry Saturn and Ketu exceptions, §21.2 tests footedness
#: per group, and §22.2.1 tests the odd/even sign with a Saturn exception.
DIRECTION_RULE = (
    "Dasas start there and always go in the regular zodiacal order."
)

#: §23.2's own two illustrations of rule 2. Both seed from the 7th, and both
#: run forward, which is the point of them.
DIRECTION_EXAMPLES: tuple[dict, ...] = (
    {"lagna": "Sc", "seed": "Ta", "order": ("Ta", "Ge", "Cn", "Le"),
     "text": ("if lagna is in Sc and Ta is stronger than Sc, dasas go as Ta, "
              "Ge, Cn, Le etc")},
    {"lagna": "Le", "seed": "Aq", "order": ("Aq", "Pi", "Ar", "Ta"),
     "text": ("If lagna is in Le and Aq is stronger than Le, dasas go as Aq, "
              "Pi, Ar, Ta etc")},
)

#: Rule 3. Flat, where chapter 22 read the modality and chapters 18 to 21 read
#: §18.2.2.
LENGTH_RULE = "Each dasa is of 9 years."

#: Rule 4, and rule 5 — the antardasas are this dasa applied to itself.
ANTARDASA_RULE = (
    "Each dasa is divided into 12 equal antardasas. Antardasas are found "
    "using the same rules as dasas, but treating dasa rasi as lagna."
)

#: §23.2's illustration of the antardasa rule.
ANTARDASA_EXAMPLE = (
    "If Cn dasa is running and Cn is stronger than Cp, then antardasas go as "
    "Cn, Le, Vi, Li etc and each antardasa will last 9 months."
)

#: Where the 9 comes from, and what it becomes for a chart that is not human.
GESTATION_RULE = (
    "Human beings live in the womb for an average of 9 months. For animals "
    "with an average gestation period of n months, each dasa and antardasa "
    "will be of n years and n months respectively."
)

#: The human gestation period in months, which is the dasa length in years and
#: the antardasa length in months.
HUMAN_GESTATION_MONTHS = 9

#: §23.2's mundane use.
MUNDANE_COMPRESSION_RULE = (
    "In mundane astrology, we can use Shoola dasa by compressing 108 years to "
    "the time period of effect of the chart."
)

#: Its worked case, which is also the arithmetic check on
#: :func:`compressed_dasa_months`.
MUNDANE_COMPRESSION_EXAMPLE = (
    "Suppose we want compressed Shoola dasa for the swearing-in chart of an "
    "Indian Prime Minister. Then, 108 years of Shoola dasa are compressed to "
    "5 years or 60 months (which is the term of an Indian Prime Minister) and "
    "a dasa of 9 years is compressed 60/12 = 5 months."
)

#: **Finding.** Twelve dasas of nine years is 108, which is the upper bound of
#: §14.4's longevity table — "long life means 72-108 years" — and the
#: paramaayush the three-pairs method works from. §23.2 never says so, and the
#: mundane rule compresses "108 years" as though the number were the system's
#: own rather than a coincidence of 12 x 9.
THE_CYCLE_IS_THE_PARAMAAYUSH = (
    "Twelve dasas of nine years give a 108-year cycle, which is the upper "
    "bound of section 14.4's long-life range and the paramaayush its table "
    "works from. Section 23.2 states the 108 only in the mundane rule and "
    "never connects it to longevity."
)


def dasa_years(gestation_months: int = HUMAN_GESTATION_MONTHS) -> int:
    """A dasa's length in years, which is the gestation period in months.

    Nine for a human chart. §23.2 generalises it rather than fixing it, so the
    parameter is the rule and 9 is its human value.
    """
    validate.positive("gestation_months", gestation_months)
    return int(gestation_months)


def antardasa_months(gestation_months: int = HUMAN_GESTATION_MONTHS) -> int:
    """An antardasa's length in months — the same number, in months.

    A twelfth of the dasa, which for the human 9 years is 9 months exactly.
    """
    validate.positive("gestation_months", gestation_months)
    return int(gestation_months)


def cycle_years(gestation_months: int = HUMAN_GESTATION_MONTHS) -> int:
    """The whole twelve-dasa cycle. 108 years for a human chart."""
    return 12 * dasa_years(gestation_months)


def compressed_dasa_months(term_months: float) -> float:
    """§23.2's mundane compression: a dasa is a twelfth of the chart's term.

    :param term_months: the period the chart governs, in months. The example
        uses an Indian Prime Minister's 60.

    The rule says "compressing 108 years to the time period of effect", and
    then divides the *term* by twelve — 60/12 = 5 — so the 108 is only the
    cycle being scaled and drops out of the arithmetic.
    """
    return validate.positive("term_months", term_months) / 12.0


@dataclass(frozen=True, slots=True)
class Seed:
    """Which of lagna and the 7th starts the run, or why it is unsettled."""

    lagna: int
    lagna_name: str
    seventh: int
    seventh_name: str
    sign: int | None
    sign_name: str | None
    undecided: str | None
    why: str


def seed(lagna: int, *, stronger_house: int | None = None) -> Seed:
    """§23.2's starting rasi — the stronger of lagna and the 7th.

    :param stronger_house: 1 or 7, when the caller has settled the comparison.

    Not computed here, for the reason OI-131 gives for chapter 22: this is an
    ayur dasa, §15.5.2's ayur adaptation reads the luminaries without saying
    how to weigh the other aspects, and
    :func:`hora.charts.rasi_strength.stronger` refuses that purpose. Narayana
    dasa seeds from the same pair and *is* phalita, so the pair being shared
    does not make the comparison shared.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    seventh = (index + 6) % 12
    houses = {1: index, 7: seventh}

    if stronger_house is None:
        return Seed(
            lagna=index, lagna_name=str(RASI_NAMES[index]),
            seventh=seventh, seventh_name=str(RASI_NAMES[seventh]),
            sign=None, sign_name=None,
            undecided=(
                "which of lagna and the 7th is stronger. Shoola dasa times "
                "death, and §15.5.2's ayur adaptation cannot be computed from "
                "the text; see OI-131"),
            why=(f"lagna is {RASI_NAMES[index]} and the 7th is "
                 f"{RASI_NAMES[seventh]}"))

    if stronger_house not in houses:
        raise ShoolaError(
            f"stronger_house must be 1 or 7, got {stronger_house!r}")
    chosen = houses[stronger_house]
    return Seed(
        lagna=index, lagna_name=str(RASI_NAMES[index]),
        seventh=seventh, seventh_name=str(RASI_NAMES[seventh]),
        sign=chosen, sign_name=str(RASI_NAMES[chosen]), undecided=None,
        why=(f"the caller made {'lagna' if stronger_house == 1 else 'the 7th'}"
             f" ({RASI_NAMES[chosen]}) the stronger"))


@dataclass(frozen=True, slots=True)
class Progression:
    """The twelve Shoola dasas of one chart, in order."""

    seed: int
    seed_name: str
    #: Always "forward". Kept as a field so the six rasi dasas answer alike.
    direction: str
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    years: tuple[int, ...]
    starts: tuple[int, ...]
    why: str


def progression(seed_sign: int,
                gestation_months: int = HUMAN_GESTATION_MONTHS
                ) -> Progression:
    """§23.2's twelve dasas from a seed rasi. Always zodiacal."""
    index = validate.in_range("seed_sign", seed_sign, 0, 11)
    length = dasa_years(gestation_months)
    signs = tuple((index + offset) % 12 for offset in range(12))
    return Progression(
        seed=index, seed_name=str(RASI_NAMES[index]), direction="forward",
        signs=signs, sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        years=(length,) * 12,
        starts=tuple(length * n for n in range(12)),
        why=(f"dasas start from {RASI_NAMES[index]} and always go in the "
             f"regular zodiacal order, {length} years each"))


def antardasa_progression(dasa_rasi: int, *, stronger_house: int | None = None,
                          gestation_months: int = HUMAN_GESTATION_MONTHS
                          ) -> dict:
    """§23.2's antardasas — the dasa rules again, with the dasa rasi as lagna.

    :param stronger_house: 1 or 7 **from the dasa rasi**, when the caller has
        settled that comparison. The same refusal as :func:`seed`.

    :returns: the seed verdict, the twelve rasis when it is settled, and each
        antardasa's length in months.
    """
    rasi = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    verdict = seed(rasi, stronger_house=stronger_house)
    months = antardasa_months(gestation_months)
    signs = (() if verdict.sign is None
             else progression(verdict.sign, gestation_months).signs)
    return {
        "dasa_rasi": rasi,
        "dasa_rasi_name": str(RASI_NAMES[rasi]),
        "seed": verdict,
        "signs": signs,
        "sign_names": tuple(str(RASI_NAMES[s]) for s in signs),
        "months_each": months,
        "undecided": verdict.undecided,
        "why": (f"the dasa rasi {RASI_NAMES[rasi]} is treated as lagna, so "
                f"the antardasas seed from the stronger of it and "
                f"{RASI_NAMES[(rasi + 6) % 12]} and run zodiacally, "
                f"{months} months each"),
    }
