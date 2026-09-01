"""§18.2.1 — Narayana dasa's progression of signs.

Narayana dasa progresses the lagna: each dasa makes a different rasi the
native's lagna, so a chart is read twelve times over a life. This module
settles which rasi holds each period and in what order; the lengths are a
separate question.

Three things decide the order, all from §18.2.1:

* the **dasa seed** — lagna or the 7th, whichever is stronger by §15.5.2;
* the **movement**, from the seed's modality, each governed by one of the
  Trimurthis: Brahma for movable, Shiva for fixed, Vishnu for dual;
* the **direction**, from whether the 9th house from the seed is odd- or
  even-footed.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    MODALITY_NAMES,
    RASI_IS_ODD,
    RASI_IS_ODD_FOOTED,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
    Graha,
)


class NarayanaError(validate.InputError):
    """A Narayana dasa input that cannot be resolved."""


#: §18.2.1 assigns each modality to one of the Trimurthis, and each god to a
#: movement. Keyed by our modality name.
MOVEMENTS: dict[str, dict] = {
    "chara": {
        "god": "Brahma", "modality": "movable",
        "movement": "regular",
        "text": "Brahma is associated with the regular movement of 1st, 2nd, 3rd etc.",
    },
    "sthira": {
        "god": "Shiva", "modality": "fixed",
        "movement": "sixth",
        "text": ("Shiva ... is associated with the 6th movment. We take dasa "
                 "seed, 6th from there, 6th from there and so on."),
    },
    "dwiswabhava": {
        "god": "Vishnu", "modality": "dual",
        "movement": "trinal",
        "text": ("Vishnu is associated with the trinal movement, i.e. 1st, "
                 "5th, 9th, then 10th, 2nd, 6th and so on. We cover the "
                 "trines from dasa seed first, go to another quadrant and "
                 "cover its trines and so on."),
    },
}

#: §18.2.1's direction rule, as printed.
DIRECTION_RULE = (
    "The direction of reckoning these houses is based on the 9th house from "
    "dasa seed. If the 9th house from dasa seed is an odd-footed sign (Ar, "
    "Ta, Ge and Li, Sc, Sg), the direction is forward. If the 9th house from "
    "dasa seed is an even-footed sign (Cn, Le, Vi and Cp, Aq, Pi), the "
    "direction is backward."
)

#: §18.2.1 prints the trinal movement only as far as "1st, 5th, 9th, then
#: 10th, 2nd, 6th and so on", leaving the quadrant order after the 10th open.
#: Example 64 closes it outright: "then count the same houses from the 10th
#: house, then from the 7th house and finally from the 4th house." Each next
#: quadrant is the 10th from the previous, which is what this module does.
VISHNU_QUADRANT_ORDER = (
    "We count the 1st, 5th, 9th houses from dasa seed, then count the same "
    "houses from the 10th house, then from the 7th house and finally from "
    "the 4th house."
)


#: §18.2.1's two exceptions, both keyed on who occupies the dasa seed. They
#: do not override the same thing: Saturn replaces the movement *and* fixes
#: the direction, while Ketu leaves the movement alone and only flips the
#: direction. Nothing in the section says what happens when both sit in the
#: seed, so that case is reported undecided rather than resolved.
SEED_EXCEPTIONS: dict[str, dict] = {
    "Saturn": {
        "graha": int(Graha.SATURN),
        "overrides": ("movement", "direction"),
        "text": ("If Saturn occupies dasa seed, dasa progression becomes "
                 "regular and zodiacal. ... We basically make the direction "
                 "\"forward\" and use Brahma's progression."),
    },
    "Ketu": {
        "graha": int(Graha.KETU),
        "overrides": ("direction",),
        "text": ("If Ketu occupies dasa seed, the basic direction of dasa "
                 "progression becomes reversed. If it is normally forward, it "
                 "becomes backward. If it is normally backward, it becomes "
                 "forward."),
    },
}

#: **Gap.** Saturn forces forward and Ketu reverses whatever the direction
#: would be. §18.2.1 never says which wins when both occupy the seed, and no
#: example shows it. See docs/open-items.md.
BOTH_EXCEPTIONS_UNDEFINED = (
    "Section 18.2.1 gives a Saturn exception and a Ketu exception separately "
    "and never says what happens when both occupy the dasa seed. Saturn makes "
    "the direction forward and the movement regular; Ketu reverses whatever "
    "the direction would otherwise be. Whether Ketu then reverses Saturn's "
    "forward, or Saturn's override stands alone, is not stated."
)


def movement_of(sign: int) -> dict:
    """Which of §18.2.1's three movements a sign takes, and whose it is."""
    index = validate.in_range("sign", sign, 0, 11)
    return MOVEMENTS[str(MODALITY_NAMES[RASI_MODALITY[index]])]


def house_order(sign: int) -> tuple[int, ...]:
    """The houses, in the order this sign's movement visits them.

    Always a permutation of 1 to 12: every rasi holds exactly one dasa.
    """
    movement = movement_of(sign)["movement"]
    if movement == "regular":
        return tuple(1 + k for k in range(12))
    if movement == "sixth":
        houses, house = [], 1
        for _ in range(12):
            houses.append(house)
            house = (house - 1 + 5) % 12 + 1        # the 6th from here
        return tuple(houses)

    houses, quadrant = [], 1                        # trinal
    for _ in range(4):
        houses += [(quadrant - 1 + 4 * k) % 12 + 1 for k in range(3)]
        quadrant = (quadrant - 1 + 9) % 12 + 1      # the 10th from here
    return tuple(houses)


def direction_of(seed: int) -> str:
    """``forward`` or ``backward``, from the 9th house from the seed.

    The rule reads the 9th **zodiacally**, before any direction is known —
    the direction is what it decides, so it cannot also depend on it.
    """
    index = validate.in_range("seed", seed, 0, 11)
    ninth = (index + 8) % 12
    return "forward" if RASI_IS_ODD_FOOTED[ninth] else "backward"


@dataclass(frozen=True, slots=True)
class Progression:
    """The order in which rasis take their Narayana dasa."""

    seed: int
    seed_name: str
    god: str
    movement: str
    direction: str
    ninth_from_seed: int
    ninth_name: str
    #: Sign index per period, in order. Twelve entries, each rasi once.
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    #: The house numbers those signs answer to, before direction is applied.
    houses: tuple[int, ...]
    #: Which of §18.2.1's seed exceptions applied, if any.
    exception: str | None
    why: str


def progression(seed: int, occupants: set[int] | None = None) -> Progression:
    """§18.2.1's full order of rasis for one dasa seed.

    :param seed: the stronger of lagna and the 7th, as a sign index.
    :param occupants: grahas in the seed rasi. Needed only for §18.2.1's two
        exceptions; omitted, neither can apply and the answer says so.
    :raises NarayanaError: on a sign outside 0-11, or when both Saturn and
        Ketu occupy the seed, which the section does not resolve.
    """
    index = validate.in_range("seed", seed, 0, 11)
    movement = movement_of(index)
    direction = direction_of(index)
    houses = house_order(index)

    present = set() if occupants is None else {int(g) for g in occupants}
    saturn = int(Graha.SATURN) in present
    ketu = int(Graha.KETU) in present
    exception = None
    if saturn and ketu:
        raise NarayanaError(
            f"{RASI_NAMES[index]} holds both Saturn and Ketu. "
            f"{BOTH_EXCEPTIONS_UNDEFINED}")
    if saturn:
        exception = "Saturn"
        movement = MOVEMENTS["chara"]          # Brahma's regular progression
        direction = "forward"
        houses = tuple(1 + k for k in range(12))
    elif ketu:
        exception = "Ketu"
        direction = "backward" if direction == "forward" else "forward"
    step = 1 if direction == "forward" else -1
    signs = tuple((index + step * (house - 1)) % 12 for house in houses)
    ninth = (index + 8) % 12
    return Progression(
        seed=index, seed_name=str(RASI_NAMES[index]),
        god=str(movement["god"]), movement=str(movement["movement"]),
        direction=direction, ninth_from_seed=ninth,
        ninth_name=str(RASI_NAMES[ninth]),
        signs=signs, sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        houses=houses, exception=exception,
        why=_why(index, movement, ninth, direction, exception),
    )


def _why(index: int, movement: dict, ninth: int, direction: str,
         exception: str | None) -> str:
    """One sentence saying how the movement and direction were arrived at."""
    if exception == "Saturn":
        return (f"{GRAHA_NAMES[Graha.SATURN]} occupies the seed "
                f"{RASI_NAMES[index]}, so §18.2.1 makes the progression "
                f"regular and zodiacal whatever the rasi's modality")
    footed = "odd" if RASI_IS_ODD_FOOTED[ninth] else "even"
    base = (f"{RASI_NAMES[index]} is {movement['modality']}, so "
            f"{movement['god']} governs it and the movement is "
            f"{movement['movement']}; the 9th from it is {RASI_NAMES[ninth]}, "
            f"{footed}-footed")
    if exception == "Ketu":
        natural = "forward" if RASI_IS_ODD_FOOTED[ninth] else "backward"
        return (f"{base}, so the direction would be {natural} — but "
                f"{GRAHA_NAMES[Graha.KETU]} occupies the seed, which reverses "
                f"it to {direction}")
    return f"{base}, so the direction is {direction}"


#: §18.2.1's own name for the stronger of lagna and the 7th.
DASA_SEED_RULE = (
    "Dasas start from lagna or the 7th house, whichever is stronger. We use "
    "the rules of strength explained in the chapter \"Strength of Planets and "
    "Rasis\". Let us denote the stronger of lagna and 7th house by the "
    "expression \"dasa seed\"."
)


def dasa_seed(lagna: int, longitudes: dict[int, float]) -> dict:
    """The stronger of lagna and the 7th, by §15.5.2's cascade.

    Narayana is a phalita dasa, and §15.5.2 says the Mercury/Jupiter/lord
    reading is "important for Narayana dasa and other phalita dasas", so that
    is the purpose used.

    :returns: the seed, the pair compared, and which rule settled it. When the
        cascade cannot decide, ``seed`` is None and the reason says so rather
        than a side being picked.
    """
    from hora.charts.rasi_strength import stronger

    index = validate.in_range("lagna", lagna, 0, 11)
    seventh = (index + 6) % 12
    verdict = stronger(index, seventh, longitudes, purpose="phalita")
    return {
        "lagna": index,
        "lagna_name": str(RASI_NAMES[index]),
        "seventh": seventh,
        "seventh_name": str(RASI_NAMES[seventh]),
        "seed": verdict.winner,
        "seed_name": None if verdict.winner is None else str(RASI_NAMES[verdict.winner]),
        "decided_by": verdict.decided_by,
        "reason": verdict.reason,
    }


#: §18.2.2's base rule and its three exceptions, as printed.
DASA_LENGTH_RULE = (
    "The length of a dasa is determined by the position of the lord of dasa "
    "rasi with respect to dasa rasi. Counting is forward if dasa rasi is "
    "odd-footed. Counting is backward if dasa rasi is even-footed. Count "
    "houses from dasa rasi to its lord. Subtract one from the count. That "
    "gives dasa length in years."
)

#: §18.2.2's second special note.
SECOND_CYCLE_RULE = (
    "After dasas of all the rasis are over, the second cycle starts. In the "
    "second cycle, dasa lengths of various rasis are obtained by subtracting "
    "the dasa length in the first cycle from 12 years."
)


@dataclass(frozen=True, slots=True)
class DasaLength:
    """One rasi's dasa length, and every step that produced it."""

    rasi: int
    rasi_name: str
    lord: int
    lord_name: str
    #: Which way houses were counted, from the *dasa rasi's* own footedness —
    #: not the progression's direction, which comes from the seed.
    counting: str
    #: Houses from the dasa rasi to its lord, counted that way. 1 to 12.
    count: int
    years: int
    #: Exceptions applied, in the order §18.2.2 lists them.
    applied: tuple[str, ...]
    #: Set when exception 3 takes a one-year period down to none, which
    #: §18.2.2 does not discuss. The 13-year case is gone: Example 68 shows
    #: exception 1 is terminal. None otherwise.
    out_of_range: str | None
    why: str


def dasa_length(
    rasi: int,
    lord: int,
    lord_sign: int,
    lord_dignity: str | None = None,
) -> DasaLength:
    """§18.2.2's length for one rasi's dasa, in years.

    :param rasi: the dasa rasi.
    :param lord: its lord — for Scorpio and Aquarius the stronger of the two,
        by §15.5.1, which special note 1 requires.
    :param lord_sign: the rasi the lord occupies.
    :param lord_dignity: the lord's dignity there. Omitted, exceptions 2 and
        3 cannot fire and the answer says so rather than assuming neither
        does. §18.2.2 reads exaltation at sign level and
        :func:`hora.charts.dignity.sign_dignity` reads it by degree, so the
        caller settles which it wants. See D-52.
    """
    index = validate.in_range("rasi", rasi, 0, 11)
    place = validate.in_range("lord_sign", lord_sign, 0, 11)

    forward = bool(RASI_IS_ODD_FOOTED[index])
    counting = "forward" if forward else "backward"
    step = (place - index) % 12 if forward else (index - place) % 12
    count = step + 1                                   # inclusive of the rasi

    applied: list[str] = []
    if count == 1:
        # Exception 1, and it is terminal: exceptions 2 and 3 do not then
        # adjust the 12. Example 68 settles this. Bill Gates' Mercury is at
        # 23 Vi 19, exalted in the Virgo he owns, and the example needs him
        # exalted -- Gemini's dasa is 4 years, which is 4 - 1 + 1. Yet the
        # same Mercury gives Virgo 12 years, not 13. Virgo is the only rasi
        # where exceptions 1 and 2 can meet, so this is the whole question.
        years = 12
        applied.append("contains its lord, so 12 rather than 0")
    else:
        years = count - 1
        if lord_dignity == "exalted":
            years += 1
            applied.append("lord exalted, so one year added")
        elif lord_dignity == "debilitated":
            years -= 1
            applied.append("lord debilitated, so one year taken away")

    out_of_range = None
    if years < 1:
        out_of_range = (
            f"{years} years leaves this rasi no dasa at all. Exception 3 took "
            f"a year from a one-year period; §18.2.2 does not say whether it "
            f"may. See docs/open-items.md."
        )

    why = (f"{RASI_NAMES[index]} is "
           f"{'odd' if forward else 'even'}-footed, so houses are counted "
           f"{counting}; its lord {GRAHA_NAMES[lord]} is in "
           f"{RASI_NAMES[place]}, {count} houses away")
    if applied:
        why += "; " + "; ".join(applied)
    return DasaLength(
        rasi=index, rasi_name=str(RASI_NAMES[index]),
        lord=int(lord), lord_name=str(GRAHA_NAMES[lord]),
        counting=counting, count=count, years=years,
        applied=tuple(applied), out_of_range=out_of_range, why=why,
    )


def second_cycle_length(first_cycle_years: int) -> int:
    """Special note 2: the second cycle's length is 12 less the first's."""
    return 12 - first_cycle_years


# --------------------------------------------------------------------------
# §18.3 Antardasas
# --------------------------------------------------------------------------

#: §18.3's own warning, which is worth keeping verbatim. This is the third
#: sign classification the chapter uses and the only one that reads odd/even
#: signs rather than odd/even *feet* — they disagree on Taurus, Leo, Scorpio
#: and Aquarius, a third of the zodiac.
ANTARDASA_DIRECTION_IS_ODD_EVEN_SIGN = (
    "The direction of counting houses is forward or backward based on whether "
    "the rasi from which antardasas start is an odd rasi or even rasi. (NOTE: "
    "We are talking about odd and even signs here and *not* about odd-footed "
    "and even-footed signs)."
)

#: §18.3's antardasa exceptions. They test who occupies the **antardasa
#: seed**, not the rasi the antardasas start from — those are usually
#: different rasis, the second being where the first's lord sits. Saturn
#: forces forward; Ketu reverses whatever the direction would be, exactly as
#: their §18.2.1 counterparts do for the progression.
ANTARDASA_EXCEPTIONS = (
    "If Saturn occupies antardasa seed rasi, antardasas go in the forward "
    "direction. If Ketu occupies antardasa seed rasi, antardasa direction is "
    "reversed (from forward to backward or from backward to forward)."
)

#: **Gap.** Example 67 offers a second way to pick the antardasa seed — "If
#: Cp is stronger than Cn (or Saturn is much stronger than Moon)" — comparing
#: the two lords instead of the two rasis. "Much stronger" is not quantified
#: and §15.5.2 grades no such margin, so only the rasi comparison is used.
ANTARDASA_SEED_BY_LORDS_UNQUANTIFIED = (
    "Example 67 allows the antardasa seed to be chosen by comparing the two "
    "rasis' lords rather than the rasis — \"or Saturn is much stronger than "
    "Moon\". It does not say what makes one lord *much* stronger, and no "
    "section grades strength by margin, so we compare the rasis."
)

#: §18.3's length rule. A dasa of n years gives twelve antardasas of n months,
#: which closes exactly because a year is twelve months.
ANTARDASA_LENGTH_RULE = (
    "Each dasa is divided into 12 antardasas. All the antardasas have an "
    "equal length. If a dasa is of n years, then each antardasa in that dasa "
    "is for n months."
)


@dataclass(frozen=True, slots=True)
class Antardasas:
    """The twelve antardasas of one dasa, in order."""

    dasa_rasi: int
    dasa_rasi_name: str
    #: The stronger of the dasa rasi and the 7th from it.
    seed: int
    seed_name: str
    #: The rasi holding that seed's lord — where the antardasas begin.
    start: int
    start_name: str
    #: forward when `start` is an odd *sign*, backward when even. Not the
    #: odd-footed test §18.2.1 and §18.2.2 use.
    direction: str
    signs: tuple[int, ...]
    sign_names: tuple[str, ...]
    #: Each antardasa's length in months, equal to the dasa's length in years.
    months_each: int
    #: Which of §18.3's seed exceptions applied, if any.
    exception: str | None
    why: str


def antardasas(
    dasa_rasi: int,
    dasa_years: int,
    longitudes: dict[int, float],
    seed_lord: int | None = None,
    seed_occupants: set[int] | None = None,
) -> Antardasas:
    """§18.3's twelve antardasas for one Narayana dasa.

    :param dasa_rasi: the rasi whose dasa is being divided.
    :param dasa_years: that dasa's length, from :func:`dasa_length`.
    :param longitudes: the chart, for §15.5.2's comparison and to find the
        seed lord's rasi.
    :param seed_lord: the antardasa seed's lord. Supply it when the seed is
        Scorpio or Aquarius, whose lord §15.5.1 must settle; otherwise it is
        read from the seed itself.
    :param seed_occupants: grahas in the **antardasa seed** — not in the rasi
        the antardasas start from. Needed only for §18.3's two exceptions.
    :raises NarayanaError: when §15.5.2 cannot decide between the dasa rasi
        and the 7th from it, or when Saturn and Ketu share the seed.
    """
    from hora.charts.rasi_strength import stronger

    index = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    seventh = (index + 6) % 12
    verdict = stronger(index, seventh, longitudes, purpose="phalita")
    if verdict.winner is None:
        raise NarayanaError(
            f"section 15.5.2 could not choose between {RASI_NAMES[index]} and "
            f"{RASI_NAMES[seventh]} for the antardasa seed: {verdict.reason}")
    seed = verdict.winner

    lord = int(RASI_LORD[seed]) if seed_lord is None else int(seed_lord)
    if lord not in longitudes:
        raise NarayanaError(
            f"no longitude given for {GRAHA_NAMES[lord]}, the lord of the "
            f"antardasa seed {RASI_NAMES[seed]}")
    start = int(longitudes[lord] // 30)

    odd = bool(RASI_IS_ODD[start])
    direction = "forward" if odd else "backward"

    present = set() if seed_occupants is None else {int(g) for g in seed_occupants}
    saturn = int(Graha.SATURN) in present
    ketu = int(Graha.KETU) in present
    exception = None
    if saturn and ketu:
        raise NarayanaError(
            f"the antardasa seed {RASI_NAMES[seed]} holds both Saturn and "
            f"Ketu. {BOTH_EXCEPTIONS_UNDEFINED}")
    if saturn:
        exception, direction = "Saturn", "forward"
    elif ketu:
        exception = "Ketu"
        direction = "backward" if direction == "forward" else "forward"

    step = 1 if direction == "forward" else -1
    signs = tuple((start + step * k) % 12 for k in range(12))

    return Antardasas(
        dasa_rasi=index, dasa_rasi_name=str(RASI_NAMES[index]),
        seed=seed, seed_name=str(RASI_NAMES[seed]),
        start=start, start_name=str(RASI_NAMES[start]),
        direction=direction, signs=signs,
        sign_names=tuple(str(RASI_NAMES[s]) for s in signs),
        months_each=int(dasa_years), exception=exception,
        why=(f"the stronger of {RASI_NAMES[index]} and {RASI_NAMES[seventh]} "
             f"is {RASI_NAMES[seed]}, whose lord {GRAHA_NAMES[lord]} is in "
             f"{RASI_NAMES[start]}; {RASI_NAMES[start]} is an "
             f"{'odd' if odd else 'even'} sign, so counting would be "
             f"{'forward' if odd else 'backward'}"
             + (f" — but {exception} occupies the seed, making it {direction}"
                if exception else "")),
    )


# --------------------------------------------------------------------------
# §18.4 Interpretation
# --------------------------------------------------------------------------

#: §18.4's central move, and the one most easily skipped. The rasi read as
#: lagna during a dasa is the dasa rasi *only when the dasas were seeded from
#: lagna*. Seeded from the 7th house — which both charts worked in this
#: chapter are — it is the 7th from the dasa rasi instead, six signs away.
DASA_LAGNA_RULE = (
    "Narayana dasa gives the progression of lagna in life. During the dasa of "
    "a rasi, that rasi acts as lagna. If dasas are started from the 7th house "
    "from lagna, then Narayana dasa gives the progression of the 7th house. "
    "So the 7th from dasa rasi gives the progressed lagna."
)


def dasa_lagna(dasa_rasi: int, seed: int, natal_lagna: int) -> int:
    """The rasi read as lagna during one dasa.

    :param dasa_rasi: the rasi whose dasa is running.
    :param seed: the dasa seed, from :func:`dasa_seed`.
    :param natal_lagna: the chart's own lagna.
    :returns: the dasa rasi when the seed was lagna; the 7th from it when the
        seed was the 7th house.
    :raises NarayanaError: if the seed is neither lagna nor the 7th from it,
        which §18.2.1 does not allow.
    """
    rasi = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    seed_index = validate.in_range("seed", seed, 0, 11)
    lagna_index = validate.in_range("natal_lagna", natal_lagna, 0, 11)

    if seed_index == lagna_index:
        return rasi
    if seed_index == (lagna_index + 6) % 12:
        return (rasi + 6) % 12
    raise NarayanaError(
        f"the dasa seed {RASI_NAMES[seed_index]} is neither the lagna "
        f"{RASI_NAMES[lagna_index]} nor the 7th from it; §18.2.1 admits only "
        f"those two")


def paaka_rasi(lagna_of_dasa: int, longitudes: dict[int, float],
               lord: int | None = None) -> int:
    """The rasi holding the lord of the dasa lagna.

    :param lord: supply it when the dasa lagna is Scorpio or Aquarius, whose
        lord §15.5.1 must settle.
    :raises NarayanaError: when that lord's longitude was not given.
    """
    index = validate.in_range("dasa_lagna", lagna_of_dasa, 0, 11)
    ruler = int(RASI_LORD[index]) if lord is None else int(lord)
    if ruler not in longitudes:
        raise NarayanaError(
            f"no longitude given for {GRAHA_NAMES[ruler]}, the lord of the "
            f"dasa lagna {RASI_NAMES[index]}")
    return int(longitudes[ruler] // 30)


#: §18.4's list of Parasara's principles, each keyed to what it reads. They
#: are a register of how a dasa is judged, not a calculation: `houses` are
#: counted from the dasa lagna unless `reference` says otherwise.
PARASARA_DASA_PRINCIPLES: tuple[dict, ...] = (
    {"houses": (3, 6), "who": "natural malefics", "gives": "success in ventures"},
    {"houses": (3, 6), "who": "natural benefics", "gives": "failures"},
    {"houses": (1, 5, 9, 8), "who": "natural benefics",
     "gives": "happiness and success"},
    {"houses": (1, 5, 9, 8), "who": "natural malefics",
     "gives": "failures, obstructions and unhappiness"},
    {"houses": (11,), "who": "any planet, benefic or malefic",
     "gives": "gains"},
    {"houses": (8, 12), "who": "Rahu", "gives": "constant fear"},
    {"houses": (4,), "who": "malefics",
     "gives": "discomfort and lack of happiness"},
    {"houses": (4,), "who": "benefics",
     "gives": "happiness, well-being and pleasures"},
    {"houses": (2, 5), "who": "benefics",
     "gives": "good name, fame and favors from authorities"},
    {"houses": (2, 5), "who": "malefics", "gives": "bad results in those areas"},
    {"houses": None, "who": "the lord of dasa lagna, or of a trine or quadrant "
                            "from it, exalted or in own house",
     "gives": "excellent results"},
    {"houses": None, "who": "that lord debilitated", "gives": "bad results"},
    {"houses": None, "who": "the lord of a dusthana from dasa lagna, debilitated",
     "gives": "good results"},
    {"houses": (7,), "who": "malefics afflicting the 7th and the paaka rasi",
     "gives": "troubles in marriage", "reference": "dasa lagna and paaka rasi"},
    {"houses": None, "who": "raja yogas and dhana yogas from dasa lagna",
     "gives": "success"},
    {"houses": None,
     "who": "an exalted planet or one in own house, with dasa lagna or paaka rasi",
     "gives": "all-round success and accumulation of wealth"},
)

#: §18.4's readings that use natal reference points rather than the dasa lagna.
NATAL_REFERENCE_READINGS: tuple[dict, ...] = (
    {"of": "raajya pada", "gives": "success in career"},
    {"of": "upapada", "gives": "marriage"},
    {"of": "the 2nd or 7th from upapada", "gives": "troubles in marriage"},
    {"of": "GL", "gives": "power"},
    {"of": "antardasas aspected by GL", "gives": "promotions"},
    {"of": "antardasas aspecting upapada", "gives": "marriage"},
)

#: §18.4's division of each dasa into thirds, each with its own significator.
DASA_THIRDS: tuple[dict, ...] = (
    {"part": 1, "dominates": "the rasi"},
    {"part": 2, "dominates": "its lord, who gives his results"},
    {"part": 3, "dominates": "occupants of the rasi, and those who aspect it"},
)

#: How an antardasa's results are read, which is not from the dasa lagna.
ANTARDASA_RESULT_RULE = (
    "We also judge the results given in antardasas by looking at the house "
    "occupied by antardasa lord from dasa rasi."
)


def dasa_thirds(start_years: float, length_years: float) -> tuple[dict, ...]:
    """§18.4's three equal parts of one dasa, with their significators."""
    span = validate.finite("length_years", length_years) / 3.0
    return tuple(
        {**third, "from_years": start_years + i * span,
         "to_years": start_years + (i + 1) * span}
        for i, third in enumerate(DASA_THIRDS)
    )


# --------------------------------------------------------------------------
# Example 69 — readings §18.4's own list does not reach.
# --------------------------------------------------------------------------

#: Example 69 works India's independence chart, the book's first mundane
#: Narayana dasa. §18.4's sixteen principles supply the *valence* of a
#: placement; what it is actually about comes from the house's own
#: significations, read for a nation rather than a person. The example never
#: states this, but every reading it gives is built that way, so the pairs
#: are recorded rather than inferred into the principles themselves.
MUNDANE_HOUSE_READINGS: tuple[dict, ...] = (
    {"house": 3, "reads": "weapons",
     "text": "Rahu in the 3rd can also give aggressive weapon development, "
             "as the 3rd house shows weapons."},
    {"house": 7, "reads": "relations with other nations",
     "text": "Conglomeration of planets in the 7th house (relations with "
             "other nations) and Ketu in the 11th house gives gains from "
             "foreign sources."},
    {"house": 9, "reads": "religion",
     "text": "Ketu in the 9th house from dasa lagna may denote religious "
             "clashes and violence."},
    {"house": 10, "reads": "the head of government",
     "text": "Jupiter in the 10th house shows a versatile, intelligent and "
             "knowledgable Brahmin leader."},
)

#: Two readings Example 69 gives that no principle in §18.4 covers, even by
#: valence. Both are about the 10th and 12th from dasa lagna, and principle 6
#: reaches the 12th only for Rahu.
UNLISTED_DASA_LAGNA_READINGS: tuple[str, ...] = (
    ("In particular, planetary conglomeration in the 12th house shows "
     "constant fear and turbulence. It signals instability."),
    ("Rahu in the 10th house from dasa lagna denies stable and capable "
     "leadership."),
)

#: A second way to read an antardasa, and a fourth reference point in the
#: chapter. §18.4 judges an antardasa by the house its *lord* occupies from
#: the dasa rasi; this judges the antardasa **rasi** by what it aspects, and
#: what it aspects is a natal arudha rather than anything in the dasa.
ANTARDASA_ASPECT_RULE = (
    "Antardasas aspecting A3 can bring weapons, just as antardasas aspecting "
    "UL can bring marriage."
)

#: §18.4 states principle 13 in one direction only — a **debilitated** lord of
#: a dusthana from dasa lagna gives good results. Exercise 28 applies its
#: converse without saying so: of the three dusthana lords from its dasa lagna
#: Vi, two are exalted, and the answer reads that as hard times. The converse
#: is not in the sixteen, so it is recorded here rather than added to them.
EXALTED_DUSTHANA_LORD_CONVERSE = (
    "Lords of two dusthanas - Mars and Sun - are exalted and that suggests "
    "hard times."
)

#: Ketu in the 11th from dasa lagna. Principle 5 gives any planet there
#: "gains"; both Example 69 and Exercise 28 make Ketu's gains specifically
#: foreign ones, in the same words, so the reading is the book's and not a
#: one-off turn of phrase.
KETU_IN_THE_ELEVENTH_IS_FOREIGN = (
    "Ketu in the 11th house shows gains from foreign sources."
)
