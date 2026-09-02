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
    #: 0 to 12. Zero is a real answer, not a failure: Example 71 prints
    #: Sagittarius at zero years and gives the rasi 12 in the second cycle.
    years: int
    #: Exceptions applied, in the order §18.2.2 lists them.
    applied: tuple[str, ...]
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
        applied=tuple(applied), why=why,
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


def dasa_lagna(dasa_rasi: int, seed: int, natal_lagna: int,
               divisions: int = 1) -> int:
    """The rasi read as lagna during one dasa. Rasi chart only.

    :param dasa_rasi: the rasi whose dasa is running.
    :param seed: the dasa seed, from :func:`dasa_seed`.
    :param natal_lagna: the chart's own lagna.
    :param divisions: the *n* of the chart this dasa was computed on. Anything
        but 1 is refused — §18.5 says a varga's Narayana dasa progresses
        neither lagna nor the 7th, so there is no dasa lagna to have. Every
        §18.4 reading hangs off this function, so refusing here refuses them
        all, :func:`paaka_rasi` and :func:`dasa_thirds` included.
    :returns: the dasa rasi when the seed was lagna; the 7th from it when the
        seed was the 7th house.
    :raises NarayanaError: on a varga, or if the seed is neither lagna nor the
        7th from it, which §18.2.1 does not allow.
    """
    rasi = validate.in_range("dasa_rasi", dasa_rasi, 0, 11)
    seed_index = validate.in_range("seed", seed, 0, 11)
    lagna_index = validate.in_range("natal_lagna", natal_lagna, 0, 11)
    if int(divisions) != 1:
        raise NarayanaError(
            f"D-{int(divisions)} has no dasa lagna. "
            f"{VARGA_INTERPRETATION_WARNING}")

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

    There is no varga guard here because there is no way past
    :func:`dasa_lagna` to reach it: a paaka rasi is the dasa lagna's lord's
    rasi, and on a varga §18.5 says there is no dasa lagna.
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
#: are recorded rather than inferred into the principles themselves. See
#: OI-122, which gathers every reading the sixteen do not carry.
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
#: reaches the 12th only for Rahu. See OI-122.
UNLISTED_DASA_LAGNA_READINGS: tuple[str, ...] = (
    ("In particular, planetary conglomeration in the 12th house shows "
     "constant fear and turbulence. It signals instability."),
    ("Rahu in the 10th house from dasa lagna denies stable and capable "
     "leadership."),
)

#: A second way to read an antardasa, and a fourth reference point in the
#: chapter. §18.4 judges an antardasa by the house its *lord* occupies from
#: the dasa rasi; this judges the antardasa **rasi** by what it aspects, and
#: what it aspects is a natal arudha rather than anything in the dasa. See
#: OI-122.
ANTARDASA_ASPECT_RULE = (
    "Antardasas aspecting A3 can bring weapons, just as antardasas aspecting "
    "UL can bring marriage."
)

#: §18.4 states principle 13 in one direction only — a **debilitated** lord of
#: a dusthana from dasa lagna gives good results. Exercise 28 applies its
#: converse without saying so: of the three dusthana lords from its dasa lagna
#: Vi, two are exalted, and the answer reads that as hard times. The converse
#: is not in the sixteen, so it is recorded here rather than added to them.
#: See OI-122.
EXALTED_DUSTHANA_LORD_CONVERSE = (
    "Lords of two dusthanas - Mars and Sun - are exalted and that suggests "
    "hard times."
)

#: Ketu in the 11th from dasa lagna. Principle 5 gives any planet there
#: "gains"; both Example 69 and Exercise 28 make Ketu's gains specifically
#: foreign ones, in the same words, so the reading is the book's and not a
#: one-off turn of phrase. See OI-122.
KETU_IN_THE_ELEVENTH_IS_FOREIGN = (
    "Ketu in the 11th house shows gains from foreign sources."
)


# --------------------------------------------------------------------------
# §18.5 Narayana Dasa of Vargas
# --------------------------------------------------------------------------

#: §18.5's rule for a varga's seed house, and the six worked cases it gives.
#: Read it carefully: it is **not** ``n % 12``. The section works D-24 out to
#: the 12th house, not the 0th, and does the same for D-30 by subtracting 24
#: rather than 24 leaving nothing. See :func:`seed_house`.
VARGA_SEED_HOUSE_RULE = (
    "To get the seed of D-n, just take the nth house. For example, the seed "
    "of D-11 is the 11th house. If n is greater than 12, subtract multiples "
    "of 12 from n. For example, the seed of D-16 is 16-12=4th house. The seed "
    "of D-27 is 27-24=3rd house. The seed of D-30 is 30-24=6th house. The "
    "seed of D-24 is 24-12=12th house. The seed of D-40 is 40-36=4th house."
)

#: The six the section works out longhand, so the formula has an answer key.
VARGA_SEED_HOUSE_EXAMPLES: dict[int, int] = {
    11: 11, 16: 4, 27: 3, 30: 6, 24: 12, 40: 4,
}

#: §18.5's four steps, verbatim. Step 2 reads the **rasi** chart and step 4
#: the varga, which is the whole of the method and easy to collapse.
VARGA_PROCEDURE: tuple[str, ...] = (
    "Find the seed house of the divisional chart of interest.",
    "Take that house in rasi chart.",
    "Find its lord. Take the stronger lord in the case of Aq and Sc.",
    ("Take the rasi occupied by him in the divisional chart of interest as "
     "lagna and find Narayana dasa of the divisional chart just as if it "
     "were a rasi chart. Use the rules explained in the previous sections."),
)

#: Why each varga has the seed house it has. The section gives these as
#: meaning, not as a rule to compute with -- the arithmetic above is the rule.
VARGA_SEED_RATIONALE: tuple[dict, ...] = (
    {"vargas": ("D9",), "house": 9, "shows": "dharma (duty)",
     "text": ("D-9 shows dharma (duty). To get married, to live with one's "
              "spouse and to perform religious ceremonies with spouse are "
              "one's duties or dharma. This is why Navamsa is also called "
              "Dharmamsa.")},
    {"vargas": ("D10",), "house": 10, "shows": "karma or action in society",
     "text": ("The seed of D-10 is the 10th house. That is why D-10 shows "
              "one's karma or action in society.")},
    {"vargas": ("D7",), "house": 7, "shows": "procreation",
     "text": ("The seed of D-7 is the 7th house. Sex is for procreation and "
              "begetting progeny.")},
    {"vargas": ("D4", "D16"), "house": 4,
     "shows": "house, and vehicles and pleasures",
     "text": ("The seed of D-4 (house) and D-16 (vehicles and pleasures) is "
              "the 4th house.")},
    {"vargas": ("D12", "D24"), "house": 12, "shows": "the evolution of self",
     "text": ("D-12 in the physical plane (it shows the lineage one belongs "
              "to) and D-24 in the mental plane (it shows one's learning) "
              "show the evolution of one's self in the respective planes. "
              "They are both based on the 12th house as the seed, which "
              "shows the evolution of self.")},
)

#: What §18.5 says each varga's Narayana dasa times.
VARGA_DASA_USES: dict[str, str] = {
    "D4": "changes in residence, happiness from home and stay in foreign countries",
    "D10": "events in career",
    "D24": "events related to learning and knowledge",
    "D9": "marriage and events in marital life",
    "D7": "happiness from children",
    "D12": "relations with parents",
}

#: Example 70 states outright what the procedure only implies: the varga's own
#: ascendant plays no part. It is not compared with the derived lagna, and it
#: is not a fallback -- it is discarded. :func:`varga_lagna` cannot use it
#: even by accident, taking only a graha-to-rasi map.
VARGA_OWN_LAGNA_IS_IGNORED = (
    "We ignore lagna in D-10 and treat the rasi containing Mars in D-10 as "
    "lagna and use the rules of Narayana dasa of rasi chart."
)

#: Example 71 reads dignity in the **varga**, not the rasi chart, and never
#: says so. Its note (1) calls Saturn exalted; in the rasi chart that Saturn is
#: at 15 Ar 06, his *debilitation*, and only in D-4 does he stand in Libra.
#: Three of Chart 27's lords change dignity between the two charts and two of
#: the changes move a dasa length, so the rasi chart's dignities get three of
#: the six printed answers wrong. :func:`dasa_length` takes the dignity from
#: its caller, so the caller must read it in the same chart it counts in.
VARGA_DIGNITY_IS_READ_IN_THE_VARGA = (
    "Saturn is in the 4th house from Cp, reckoned in the backward direction "
    "because Cp is an even-footed rasi. We get 4-1=3. However, Saturn is "
    "exalted and we have to add one year. So Cp dasa is of 4 years."
)

#: A varga dasa has no dasa lagna, but its chart still has houses, and they
#: are counted from the **varga's own lagna** -- the one Example 70 discards
#: for building the dasas. Two examples pin it between them, and neither could
#: alone. Example 71's D-4 lagna and seed house rasi are the same sign, but it
#: names the rasi chart's lagna separately ("owns the 9th house in D-4 and
#: owns the 12th house in rasi chart"), ruling that out. Example 72's D-9
#: lagna is Li while its seed rasi is Ge, and it says "Here Li is lagna",
#: ruling out the seed rasi and the derived lagna together. Only the varga's
#: own lagna survives both. See OI-123 in docs/closed-items.md.
VARGA_HOUSES_ARE_READ_FROM_THE_VARGA_LAGNA: tuple[str, ...] = (
    "Sun owns the 9th house in D-4 and owns the 12th house in rasi chart.",
    "Here Li is lagna. So its dasa can certainly bring marriage.",
)


def varga_house(varga_lagna_sign: int, rasi: int) -> int:
    """Which house a rasi holds in a varga, counted from the varga's lagna.

    The positive counterpart to :func:`dasa_lagna` refusing a varga: §18.5
    takes away the *progressed* lagna, not the chart's own one.

    :param varga_lagna_sign: the varga's ascendant sign — **not** the lagna
        :func:`varga_lagna` derives, which only says where the dasas begin.
    """
    reference = validate.in_range("varga_lagna_sign", varga_lagna_sign, 0, 11)
    sign = validate.in_range("rasi", rasi, 0, 11)
    return (sign - reference) % 12 + 1


#: Example 72's rules for reading a navamsa Narayana dasa for marriage. The
#: first reference point is the navamsa's own lagna; the rest count from the
#: upapada, whose 1st, 3rd and 8th are read as a bhava's own birth, vitality
#: and longevity, and whose 2nd and 7th are its marakas. Nothing in §18.4's
#: sixteen reaches any of this, so it is a register of its own. See OI-122.
NAVAMSA_MARRIAGE_DASA_RULES: tuple[dict, ...] = (
    {"from": "lagna", "houses": (1,), "gives": "favorable for marriage",
     "why": ("Lagna in navamsa shows self, from the point of view of dharma "
             "and marital life.")},
    {"from": "lagna", "houses": (6,),
     "gives": "troubles in marriage and even a divorce", "why": None},
    {"from": "UL", "houses": (1, 3, 8), "gives": "favorable for marriage",
     "why": ("Because UL shows marriage, the 1st, 3rd and 8th houses from it "
             "show its birth, vitality and life (longevity).")},
    {"from": "UL", "houses": (2, 7),
     "gives": "troubles in marriage and even a divorce",
     "why": "The 2nd and 7th houses from it show its end."},
)

#: Example 73 picks an antardasa by what its **rasi holds** -- lagna, the
#: upapada, the upapada's lord, or the karaka of the matter. §18.4 reads an
#: antardasa by the house its *lord* occupies from the dasa rasi, so this is
#: another mechanism the sixteen do not carry. See OI-122.
ANTARDASA_CANDIDATE_BY_CONTENTS = (
    "Certainly, Aq with lagna and UL lord is a strong candidate and Pi with "
    "UL and exalted Venus (significator of marriage) is an even stronger "
    "candidate."
)

#: Example 74's readings for a D-10 Narayana dasa and career. As with the
#: navamsa's marriage rules, the reference is the varga's own lagna, and the
#: rest count from the arudha lagna or from an arudha pada. None is in §18.4's
#: sixteen. See OI-122.
CAREER_DASA_READINGS: tuple[dict, ...] = (
    {"from": "lagna", "houses": (8,),
     "gives": "tension, frustration, worries and setbacks (related to career)"},
    {"from": "lagna", "houses": (2, 5),
     "gives": "recognition from authorities",
     "why": ("The 2nd and 5th houses and also Sun show recognition from "
             "authorities in a chart.")},
    {"from": "AL", "houses": (12,),
     "gives": "setbacks in professional status",
     "why": "It is the 12th house of losses from AL."},
    {"from": "A6", "houses": (1,), "gives": "trouble from enemies",
     "why": ("Aquarius has Satru pada (arudha pada of 6th house) and it can "
             "show trouble from enemies.")},
)

#: Arudha padas are the chapter's most-used reading mechanism outside §18.4's
#: sixteen, and they arrive one example at a time. Exercise 30 states the
#: principle behind all of them: an arudha shows the *appearance* of its
#: house's matter -- "the things based on which people form impression" -- so
#: a dasa of A-n gives that matter's outward form. Exercise 30 also notes the
#: meaning is narrowed by the chart it is read in: "the illusion associated
#: with fortune (in career, because this is D-10)". See OI-122.
ARUDHA_PADA_DASA_READINGS: tuple[dict, ...] = (
    {"pada": "A1", "also": "arudha lagna", "house": 1, "where": "Ex 74, Ex 30",
     "gives": "status; the 12th from it shows setbacks in professional status"},
    {"pada": "A3", "also": None, "house": 3, "where": "Ex 69",
     "gives": ("the illusion related to boldness or the things based on which "
               "the world forms impression about one's boldness, i.e. one's "
               "weapons")},
    {"pada": "A4", "also": "vahanapada", "house": 4, "where": "Ex 75",
     "gives": "vehicles; the 12th from it gives losses to the vehicle"},
    {"pada": "A6", "also": "satru pada", "house": 6, "where": "Ex 74",
     "gives": "trouble from enemies"},
    {"pada": "A8", "also": "mrityu pada", "house": 8, "where": "Ex 75",
     "gives": "trouble in the matters of the chart it is read in"},
    {"pada": "A9", "also": "bhaagya pada", "house": 9, "where": "Ex 30",
     "gives": ("the illusion associated with fortune... the trappings of "
               "fortune, like good position and money")},
    {"pada": "A10", "also": "raajya pada", "house": 10, "where": "Ex 68",
     "gives": "success in career"},
    {"pada": "UL", "also": "upapada", "house": 12, "where": "Ex 72, Ex 73",
     "gives": "marriage; the 1st, 3rd and 8th from it favour it, the 2nd and "
              "7th end it"},
)

#: Exercise 30's statement of what an arudha pada is for, which the chapter
#: had been using since Example 68 without ever saying.
ARUDHA_SHOWS_THE_APPEARANCE_OF_ITS_MATTER = (
    "A9 shows the illusion associated with fortune (in career, because this "
    "is D-10). It shows the things based on which people form impression "
    "about one's fortune. It essentially shows the trappings of fortune, like "
    "good position and money. Dasa of A9 in D-10 can give excellent position "
    "in career."
)

#: A structural consequence of §18.5 that no section states. In the rasi chart
#: the dasa lagna moves every dasa, so §18.4's whole house frame rotates and
#: its occupancy principles say something different each time. In a varga
#: there is no dasa lagna: houses come from the varga's own ascendant, which
#: never moves. So principles 1 to 10 give the **same** verdict in every dasa
#: of that varga, and principles 11 to 16 name a dasa lagna that does not
#: exist. What tells one varga dasa from another is the dasa rasi's own house,
#: its lord, its occupants and what aspects it -- which is exactly what
#: Examples 71 and 74 read, and nothing else.
VARGA_HOUSE_FRAME_DOES_NOT_ROTATE = (
    "Narayana dasa of vargas is not the progression of lagna or the 7th "
    "house."
)

#: Example 74's reading of an afflicted karaka in the dasa rasi itself, which
#: is neither a house nor a lordship. See OI-122.
AFFLICTED_KARAKA_IN_THE_DASA_RASI = (
    "Sun owns the 2nd house here and he is in Aq, afflicted by enemy Rahu. "
    "Affliction of Sun by Rahu in dasa rasi can show scandals and making a "
    "bad name with authorities."
)

#: The qualification Example 72 attaches to both unfavourable readings, which
#: keeps them from being read as predictions on their own.
MARRIAGE_TROUBLE_NEEDS_CORROBORATION = (
    "dasas of 6th house from lagna, dasas of the 2nd and 7th houses from UL "
    "can bring troubles in marriage and even a divorce when the chart has "
    "such indications"
)

#: §18.5's closing warning, and the reason :func:`dasa_lagna` refuses a varga.
#: Printed with two slips -- "analyzing dasas is has no technical basis" and
#: "It applies only the rasi chart" -- and kept as printed.
VARGA_INTERPRETATION_WARNING = (
    "Narayana dasa of vargas is not the progression of lagna or the 7th "
    "house. So taking dasa rasi or the 7th from it as lagna and analyzing "
    "dasas is has no technical basis. It applies only the rasi chart."
)


def seed_house(divisions: int) -> int:
    """§18.5's seed house for D-*n*, as a house number 1 to 12.

    "Just take the nth house... If n is greater than 12, subtract multiples of
    12 from n." That is ``1 + (n - 1) % 12`` and **not** ``n % 12``: the
    section's own D-24 works out to the 12th house, where ``24 % 12`` would
    give none at all. D-12, D-36, D-108 and D-144 hit the same case.

    :param divisions: the *n* of D-*n*, one or more.
    """
    n = int(validate.positive("divisions", divisions))
    return 1 + (n - 1) % 12


def varga_lagna(
    divisions: int,
    natal_lagna: int,
    varga_signs: dict[int, int],
    lord: int | None = None,
) -> dict:
    """§18.5's four steps: the rasi a varga's Narayana dasa treats as lagna.

    The seed house is counted in the **rasi** chart and its lord is then found
    in the **varga**. Both halves matter: the same lord usually sits in
    different rasis in the two charts, and using the varga throughout would
    silently give another answer.

    :param divisions: the *n* of D-*n*.
    :param natal_lagna: the rasi chart's lagna, which the seed house counts
        from.
    :param varga_signs: rasi per graha **in the varga of interest**.
    :param lord: **required** when the seed house's rasi is Scorpio or
        Aquarius, whose lord step 3 sends to §15.5.1. It is not defaulted:
        Chart 26's D-9 seeds on Aquarius, where §15.5.1 gives Rahu and
        `RASI_LORD` gives Saturn, and the two put the varga lagna seven signs
        apart -- a different dasa sequence, not a different shade of one.
    :raises NarayanaError: when a co-owned seed rasi is given no lord, or when
        the lord has no place in the varga.
    """
    lagna_index = validate.in_range("natal_lagna", natal_lagna, 0, 11)
    house = seed_house(divisions)
    rasi = (lagna_index + house - 1) % 12
    from hora.charts.colord import CO_LORDS

    if lord is None and rasi in CO_LORDS:
        pair = " and ".join(GRAHA_NAMES[g] for g in CO_LORDS[rasi])
        raise NarayanaError(
            f"D-{int(divisions)}'s seed is the {house}th house, which is "
            f"{RASI_NAMES[rasi]} -- owned by both {pair}. Step 3 sends that "
            f"to section 15.5.1; pass the lord it chooses rather than "
            f"letting one be assumed")
    ruler = int(RASI_LORD[rasi]) if lord is None else int(lord)
    if ruler not in varga_signs:
        raise NarayanaError(
            f"no place in D-{int(divisions)} for {GRAHA_NAMES[ruler]}, the "
            f"lord of {RASI_NAMES[rasi]} -- the {house}th house, which is "
            f"D-{int(divisions)}'s seed")
    return {
        "divisions": int(divisions),
        "seed_house": house,
        "seed_rasi": rasi,
        "seed_rasi_name": str(RASI_NAMES[rasi]),
        "lord": ruler,
        "lord_name": str(GRAHA_NAMES[ruler]),
        "lagna": int(varga_signs[ruler]),
        "lagna_name": str(RASI_NAMES[varga_signs[ruler]]),
        "why": (f"D-{int(divisions)}'s seed is the {house}th house, which is "
                f"{RASI_NAMES[rasi]} in the rasi chart; its lord "
                f"{GRAHA_NAMES[ruler]} occupies "
                f"{RASI_NAMES[varga_signs[ruler]]} in D-{int(divisions)}"),
    }


# --------------------------------------------------------------------------
# Pratyantardasas — a third level §18.3 never described.
# --------------------------------------------------------------------------

#: §18.3 stops at antardasas. Example 71 goes one level further and, without
#: naming a new rule, applies §18.3's own three steps to the antardasa rasi:
#: the seed is the stronger of it and the 7th from it, the periods begin where
#: that seed's lord sits, and the direction comes from whether that starting
#: rasi is an odd or even *sign*. So the level is a recursion, not a new rule.
PRATYANTARDASA_RULE = (
    "Vi is stronger than Pi, as it has a planet. Lord of Vi is Mercury. He is "
    "in Ar - an odd rasi. So pratyantardasas in Vi antardasa go as Ar, Ta, "
    "Ge, Cn, Le etc. Vi antardasa is of 11 months and it runs from 4th April "
    "1991 to 4th March 1992. Dividing it into 12 equal parts, we see that the "
    "5th pratyantardasa runs from 27th July 1991 to 25th August 1991."
)


def pratyantardasas(
    antardasa_rasi: int,
    longitudes: dict[int, float],
    seed_lord: int | None = None,
    seed_occupants: set[int] | None = None,
) -> Antardasas:
    """The twelve pratyantardasas of one antardasa, in order.

    Example 71 derives these exactly as §18.3 derives antardasas, one rasi
    down, so this delegates rather than restating the rules. Only the units
    differ: an antardasa is divided into twelve **equal parts** of itself
    rather than into a count of months, and the example gives no formula for
    them, so ``months_each`` on the result is not meaningful here — divide the
    antardasa's own span by twelve.

    :param antardasa_rasi: the rasi whose antardasa is being divided.
    :param longitudes: the chart the dasa is being run in. For a varga dasa
        that is the varga, not the rasi chart — Example 71 works in D-4
        throughout.
    :param seed_lord: the seed's lord, when the seed is Scorpio or Aquarius.
    :param seed_occupants: grahas in the seed, for §18.3's two exceptions.
    """
    return antardasas(antardasa_rasi, 0, longitudes,
                      seed_lord=seed_lord, seed_occupants=seed_occupants)

# --------------------------------------------------------------------------
# Example 75 — which dasa level an event belongs to.
# --------------------------------------------------------------------------

#: Example 75 closes the chapter's dasa material with the rule for choosing a
#: level, which no section had stated: match the level to how long the event
#: matters for. The spans are the book's own words, not arithmetic -- it gives
#: no lengths for the last two, and does not say which of them is deeper.
DASA_LEVEL_BY_EVENT_DURATION: tuple[dict, ...] = (
    {"level": "mahadasa", "depth": 1, "event_lasts": "longer periods",
     "shows": "the mood of longer periods"},
    {"level": "antardasa", "depth": 2, "event_lasts": "a few months",
     "shows": "events applicable to the antardasa's own span"},
    {"level": "pratyantardasa", "depth": 3, "event_lasts": "just a week",
     "shows": "events of about a week"},
    {"level": "praana-antardasa", "depth": None, "event_lasts": "just an hour",
     "shows": "a temporary activity that remains in the mind for an hour"},
    {"level": "deha-antardasa", "depth": None, "event_lasts": "just an hour",
     "shows": "a temporary activity that remains in the mind for an hour"},
)

#: The rule itself, and the two levels below pratyantardasa that only this
#: passage names. §18.3 gave antardasas and Example 71 gave pratyantardasas by
#: recursion; whether praana and deha continue the same recursion, and which
#: of them is deeper, the book does not say. Nothing computes them.
CHOOSE_THE_DASA_LEVEL_BY_THE_EVENT = (
    "Based on the event of interest, we should judiciously choose mahadasa or "
    "antardasa or pratyantardasa for examination. If an event plays a role in "
    "a native's life for just a week, it is probably shown in "
    "pratyantardasa. If an event plays a role in a native's life for a few "
    "months, it is probably shown in antardasa. Mahadasa shows the mood of "
    "longer periods. If we want to analyze a temporary activity that remains "
    "in a native's mind for just an hour, it is probably seen in the "
    "praana-antardasa or deha-antardasa running then. We should determine the "
    "effective period of an event and judiciously choose the dasa division in "
    "which it should be seen."
)

#: Example 75 reads the mahadasa and the antardasa as saying different things
#: at once, and neither cancels the other. The dasa gave the comfort of
#: vehicles for ten years; one ten-month antardasa inside it gave the crash.
MAHADASA_AND_ANTARDASA_COEXIST = (
    "With Li being the 4th house and having the argala of lord Venus, the "
    "native had the comfort of vehicles in Li dasa. However, Ta antardasa was "
    "bad due to Rahu and A8."
)
