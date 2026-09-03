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


# --------------------------------------------------------------------------
# §23.3 Interpretation
# --------------------------------------------------------------------------

#: §23.3's opening, which then spends a page qualifying itself. Note the
#: printed "Niryana".
TRISHOOLA_ALSO_APPLIES = (
    "Like in Niryana Shoola dasa, dasa of a Trishoola rasi can bring death."
)

#: ...and the qualification. The Trishoola reading is **demoted** here, and the
#: reason is the whole theory of §23.3: a fixed motion is not praana's motion.
TRISHOOLA_IS_LESS_SIGNIFICANT_HERE = (
    "So Shoola dasa rasi hitting Trishoola rasis is less significant than "
    "Niryaana Shoola dasa rasi hitting Trishoola rasis."
)

#: §23.3's Rudra yoga, derived from the natural zodiac rather than the chart.
RUDRA_YOGA_RULE = (
    "Because the 2nd and 8th rasis in the natural zodiac are owned by Mars "
    "and Venus, rasi aspect on either of them by Moon generates Rudra yoga "
    "and rasis aspected by Rudra yoga planets can give death."
)

#: **Finding.** The condition reduces to one sentence the section does not
#: write: Taurus and Scorpio are both fixed, so the rasis aspecting them are
#: movable, and every movable rasi aspects at least one of the two. **Rudra
#: yoga arises exactly when the Moon is in a movable rasi** — a third of all
#: charts. Cancer and Capricorn reach both; Aries reaches only Scorpio and
#: Libra only Taurus.
RUDRA_YOGA_IS_A_MOON_IN_A_MOVABLE_RASI = (
    "The natural 2nd and 8th are Taurus and Scorpio, both fixed, so the rasis "
    "that aspect them are movable — and each of the four movable rasis "
    "aspects at least one. Section 23.3's condition is therefore satisfied by "
    "a Moon in any movable rasi and by no other Moon."
)

#: **Gap.** Two things the sentence leaves open, and no example in the chapter
#: settles either. See OI-137.
RUDRA_YOGA_PLANETS_ARE_NOT_NAMED = (
    "Section 23.3 says the aspect \"generates Rudra yoga\" and that \"rasis "
    "aspected by Rudra yoga planets can give death\", without saying which "
    "planets the yoga consists of — the Moon alone, or the Moon with the "
    "owner it aspected — and without saying whether their aspect on those "
    "rasis is rasi drishti or graha drishti."
)

#: §23.3's own rules, and it says whose they are. Not classical, not attributed
#: to any maharshi — "this author found the following rules to hold true in
#: many cases", and then a quotation.
AUTHORS_RULES = (
    "AL or the trines from it can give death. If malefics or marakas occupy "
    "or aspect the 3rd from AL or the 8th from AL, those 2 houses can give "
    "death."
)

AUTHORS_RULES_ARE_HIS_OWN = (
    "This author found the following rules to hold true in many cases."
)

#: §23.3's account of what the two systems are, which is also its account of
#: why chapter 22's rules are irregular and this chapter's are not.
THE_TWO_MOTIONS = (
    "Niryaana Shoola dasa essentially shows the progress of the 8th house. It "
    "shows the motion of praana (life). That is why it has an uneven motion. "
    "It goes forward in some charts and backward in some charts. Also the "
    "lengths of dasas can be 7, 8 or 9 years. All this shows that different "
    "people have different motion of praana. ... In Shoola dasa, however, the "
    "motion has a constant rate of 9 years per dasa and the order of dasas is "
    "always fixed. This fixed motion is like the motion of a quartz crystal. "
    "It is not the motion of praana and it must be a universal motion. It is "
    "suggested that Shoola dasas show the force of Lord Shiva."
)

#: **Finding.** §23.3 re-describes chapter 22's seed and the description is
#: worth more than the rule: "Lagna and 7th house both show the self of a
#: person... Niryaana Shoola dasa starts from the 8th house from one of them."
#:
#: The 8th from lagna is the 8th house and the 8th from the 7th is the **2nd**,
#: so §22.2.1's odd-looking 2nd-and-8th pair is chapter 18's lagna-and-7th
#: pair shifted by eight. The two systems seed from the same two points, one
#: directly and one through the 8th.
NIRYAANA_SEEDS_FROM_THE_EIGHTH_OF_THE_SELF = (
    "Lagna and 7th house both show the self of a person. They stand for the "
    "invisible and visible selves. Niryaana Shoola dasa starts from the 8th "
    "house from one of them."
)

#: Why the readings hang on the arudha lagna rather than on lagna.
WHY_AL_AND_NOT_LAGNA = (
    "AL is involved instead of lagna, because our existence is a maya "
    "(illusion) and what Lord Shiva destroys is the illusion of our "
    "existence. The physical body (lagna) simply merges with the material "
    "universe, when burnt or buried, and the perceived self or the maya of "
    "existence (AL) is what is completely destroyed by Lord Shiva."
)

#: §23.3's boxed Lesson, which states the two systems against each other.
LESSON = (
    "Niryaana Shoola dasa shows the motion of praana (life). Death occurs "
    "when praana hits maraka rasis and the trines from Rudra (Trishoola "
    "rasis). Shoola dasa is the reverse. It shows the motion of Shiva. Death "
    "occurs primarily when Shiva's motion hits the trines from AL or the 3rd "
    "house from AL or the 8th house from AL."
)

#: The houses §23.3 reads from AL, and how each is qualified.
DEATH_HOUSES_FROM_AL: tuple[dict, ...] = (
    {"houses": (1, 5, 9), "name": "the trines from AL", "needs": None,
     "text": "AL or the trines from it can give death."},
    {"houses": (3, 8), "name": "the houses of vitality from AL",
     "needs": "malefics or marakas occupying or aspecting them",
     "text": ("If malefics or marakas occupy or aspect the 3rd from AL or "
              "the 8th from AL, those 2 houses can give death.")},
)

#: §23.3's two criteria for choosing one rasi from the list it has built.
SELECTION_CRITERIA: tuple[str, ...] = (
    ("Usually a rasi occupied or aspected by AK or Jupiter does not kill a "
     "native, unless that planet happens to be Rudra."),
    ("Based on whether the native is of short/middle/long life, we are "
     "limited to just 4 dasas. The first 4 Shoola dasas (0-36 years) bring "
     "death to a person of the short life category. The middle 4 Shoola "
     "dasas (36-72 years) bring death to a person of the middle life "
     "category. The last 4 Shoola dasas (72-108 years) bring death to a "
     "person of the long life category."),
)

#: **Finding.** Criterion 2 is exact here and cannot be, in chapter 22. Four
#: dasas of nine years are thirty-six, so the three longevity ranges fall on
#: dasa boundaries and every dasa lies wholly inside one block. Chapter 22's
#: 7/8/9 lengths cut across the ranges instead, which is OI-133.
THE_BLOCKS_PARTITION_THE_CYCLE_EXACTLY = (
    "Four dasas of nine years are thirty-six, so 0-36, 36-72 and 72-108 fall "
    "exactly on Shoola dasa boundaries and no dasa straddles a longevity "
    "range. Niryaana Shoola dasa's 7, 8 and 9 year dasas do straddle them, "
    "which is what OI-133 is about."
)


def rudra_yoga(moon_sign: int) -> dict:
    """§23.3's Rudra yoga, from the Moon's rasi alone.

    :returns: whether the yoga arises, which of Taurus and Scorpio the Moon's
        rasi aspects, their owners, and what §23.3 leaves unsaid.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    index = validate.in_range("moon_sign", moon_sign, 0, 11)
    natural = {1: "the natural 2nd", 7: "the natural 8th"}
    reached = tuple(sign for sign in natural if sign in rasi_drishti(index))

    return {
        "moon_sign": index,
        "moon_rasi": str(RASI_NAMES[index]),
        "applies": bool(reached),
        "reaches": tuple({
            "sign": sign, "rasi": str(RASI_NAMES[sign]),
            "which": natural[sign],
            "owner": str(GRAHA_NAMES[int(RASI_LORD[sign])]),
        } for sign in reached),
        "undecided": (None if not reached else
                      RUDRA_YOGA_PLANETS_ARE_NOT_NAMED),
        "why": (f"{RASI_NAMES[index]} aspects "
                f"{' and '.join(str(RASI_NAMES[s]) for s in reached)}"
                if reached else
                f"{RASI_NAMES[index]} aspects neither Taurus nor Scorpio"),
    }


def death_rasis(arudha_lagna: int, signs: dict[int, int] | None = None,
                lagna: int | None = None,
                malefic: frozenset[int] | None = None) -> tuple[dict, ...]:
    """§23.3's rasis that can bring death, read from the arudha lagna.

    :param arudha_lagna: AL's rasi.
    :param signs: rasi per graha, needed for the 3rd and 8th condition.
    :param lagna: needed to know which grahas are marakas, by §14.2.
    :param malefic: which grahas count as malefic; the natural set by default.

    The trines are unconditional. The 3rd and 8th need "malefics or marakas
    occupy or aspect" them, and §23.3 does not say which aspect — both are
    reported, and the row stays undecided when the caller gave no chart.
    """
    from hora.charts.aspects import graha_aspects_sign, rasi_drishti
    from hora.charts.maraka import MALEFICS, marakas
    from hora.core.const import GRAHA_NAMES

    al = validate.in_range("arudha_lagna", arudha_lagna, 0, 11)
    evil = MALEFICS if malefic is None else malefic
    maraka_grahas: set[int] = set()
    if lagna is not None:
        found = marakas(validate.in_range("lagna", lagna, 0, 11), signs)
        maraka_grahas = {m["graha"] for m in found["maraka_grahas"]}

    out: list[dict] = []
    for row in DEATH_HOUSES_FROM_AL:
        for house in row["houses"]:
            rasi = (al + house - 1) % 12
            entry = {
                "house_from_al": house, "sign": rasi,
                "rasi": str(RASI_NAMES[rasi]), "group": row["name"],
                "needs": row["needs"],
            }
            if row["needs"] is None:
                entry["applies"] = True
            elif signs is None:
                entry["applies"] = None
                entry["undecided"] = (
                    "whether malefics or marakas reach it; no chart given")
            else:
                occupy, by_graha, by_rasi = [], [], []
                for graha, place in sorted(signs.items()):
                    if graha not in evil and graha not in maraka_grahas:
                        continue
                    label = str(GRAHA_NAMES[graha])
                    if place == rasi:
                        occupy.append(label)
                    else:
                        if graha_aspects_sign(graha, place, rasi):
                            by_graha.append(label)
                        if rasi in rasi_drishti(place):
                            by_rasi.append(label)
                entry.update(occupied_by=tuple(occupy),
                             aspected_by_graha_drishti=tuple(by_graha),
                             aspected_by_rasi_drishti=tuple(by_rasi))
                entry["applies"] = bool(occupy or by_graha or by_rasi)
                if by_graha or by_rasi:
                    entry["undecided"] = (
                        "which aspect §23.3 means; it says only \"aspect\"")
                if lagna is None:
                    entry["undecided"] = (
                        "marakas were not computed; pass lagna")
            out.append(entry)
    return tuple(out)


def longevity_block(longevity: str) -> dict:
    """§23.3 criterion 2 — which four of the twelve dasas can kill.

    Exact, unlike chapter 22's: four nine-year dasas are thirty-six years, so
    the blocks fall on dasa boundaries. See
    :data:`THE_BLOCKS_PARTITION_THE_CYCLE_EXACTLY`.
    """
    from hora.core.constants.maraka import LONGEVITY_RANGES

    if longevity not in LONGEVITY_RANGES:
        raise ShoolaError(
            f"longevity must be one of {tuple(LONGEVITY_RANGES)}, "
            f"got {longevity!r}")
    order = ("short", "middle", "long")
    block = order.index(longevity)
    low, high = LONGEVITY_RANGES[longevity]
    return {
        "longevity": longevity,
        "range": (low, high),
        "positions": tuple(range(block * 4, block * 4 + 4)),
        "which": ("first", "middle", "last")[block],
    }


def protected_by(rasi: int, signs: dict[int, int], atma_karaka: int,
                 rudra: int | None = None) -> dict:
    """§23.3 criterion 1 — whether AK or Jupiter shields a rasi from killing.

    :param rudra: the graha that is Rudra, if known. The criterion's own
        exception: a shield that *is* Rudra does not shield.

    "Usually" is the section's word and is not applied as a certainty; the
    reasons are returned and the caller decides.
    """
    from hora.charts.aspects import rasi_drishti
    from hora.core.const import GRAHA_NAMES, Graha

    index = validate.in_range("rasi", rasi, 0, 11)
    ak = validate.in_range("atma_karaka", int(atma_karaka), 0, 8)

    shields: list[dict] = []
    for graha, role in ((ak, "AK"), (int(Graha.JUPITER), "Jupiter")):
        place = signs.get(graha)
        if place is None:
            continue
        how = ("occupies" if place == index
               else "aspects" if index in rasi_drishti(place) else None)
        if how is None:
            continue
        shields.append({
            "graha": graha, "graha_name": str(GRAHA_NAMES[graha]),
            "role": role, "how": how,
            "is_rudra": rudra is not None and int(rudra) == graha,
        })

    active = [s for s in shields if not s["is_rudra"]]
    return {
        "rasi": str(RASI_NAMES[index]),
        "shields": tuple(shields),
        "protected": bool(active),
        "rudra_cancels": tuple(s for s in shields if s["is_rudra"]),
        "hedge": "usually",
        "undecided": (None if rudra is not None or not shields else
                      "whether either shield is Rudra; pass rudra"),
    }


def select_dasa(arudha_lagna: int, seed_sign: int, longevity: str,
                signs: dict[int, int] | None = None,
                lagna: int | None = None,
                *, atma_karaka: int | None = None,
                rudra: int | None = None) -> dict:
    """§23.3's two criteria applied together — the dasas that can kill.

    Criterion 2 first: only the four dasas of the longevity block are
    candidates. Then §23.3's own rules, which rank them — the trines from AL
    are unconditional and the 3rd and 8th from AL need malefics or marakas.
    Criterion 1 is applied last and only as a report, since its own word is
    "usually".

    :param longevity: the category, from
        :func:`hora.charts.maraka.three_pairs` or from the caller. Examples 89
        and 90 both take it as given, and on Chart 39 the two disagree — see
        D-65.
    """
    al = validate.in_range("arudha_lagna", arudha_lagna, 0, 11)
    block = longevity_block(longevity)
    run = progression(validate.in_range("seed_sign", seed_sign, 0, 11))
    reachable = {row["sign"]: row
                 for row in death_rasis(al, signs, lagna=lagna)}

    candidates = []
    for position in block["positions"]:
        rasi = run.signs[position]
        row = reachable.get(rasi)
        entry = {
            "position": position, "sign": rasi,
            "rasi": str(RASI_NAMES[rasi]),
            "starts": run.starts[position],
            "ends": run.starts[position] + run.years[position],
            "reads": None if row is None else row["group"],
            "house_from_al": None if row is None else row["house_from_al"],
            "can_kill": row is not None and row.get("applies") is not False,
        }
        if row is not None and row.get("undecided"):
            entry["undecided"] = row["undecided"]
        if signs is not None and atma_karaka is not None:
            entry["protection"] = protected_by(rasi, signs, atma_karaka, rudra)
        candidates.append(entry)

    killers = [c for c in candidates if c["can_kill"]]
    trines = [c for c in killers if c["house_from_al"] in (1, 5, 9)]
    return {
        "longevity": longevity,
        "block": block,
        "candidates": tuple(candidates),
        "can_kill": tuple(killers),
        "trines_from_al": tuple(trines),
        #: The answer when the trines alone leave one, which is how both of
        #: §23.4's examples reach theirs.
        "selected": trines[0] if len(trines) == 1 else None,
        "why": (f"of the four {longevity}-life dasas from "
                f"{RASI_NAMES[run.seed]}, "
                f"{len(trines)} lie in the trines from {RASI_NAMES[al]}"),
    }
