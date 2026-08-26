"""Arudha padas — book §9.2, the six-step procedure.

The chapter states the computation as six numbered steps. This module keeps
them as six named functions rather than collapsing them into the one-line
formula they reduce to, so that every intermediate value the book names is a
value the API can return and a test can pin.

    step 1  house_sign          sign containing the house of interest
    step 2  lord_sign           sign occupied by that house's lord
    step 3  count_to_lord       signs from the house to its lord, zodiacal
    step 4  advance_from_lord   the same count again, from the lord's sign
    step 5  apply_exception     1st or 7th from the original -> take the 10th
    step 6  arudha_pada         the resulting sign

The closed form is ``2 * lord_sign - house_sign`` before the exception, and
``test_arudha.py`` asserts the steps agree with it for all 144 combinations.
The steps remain the implementation because the book's wording is the
specification, and because a caller debugging a chart needs the intermediates.

**Dual lordship is not resolved here.** §9.2's note says Aquarius is owned by
Saturn and Rahu, Scorpio by Mars and Ketu, and to "take the stronger lord" —
with the comparison deferred to the chapter on Strength of Planets and Rasis.
That chapter is not implemented, so :func:`lord_sign` requires the caller to
say which lord is stronger and raises if it cannot know. It never guesses.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import GRAHA_NAMES, RASI_LORD, RASI_NAMES, Graha, Rasi


class ArudhaError(validate.InputError):
    """An arudha input that cannot be resolved.

    A subclass of :class:`~hora.core.validate.InputError`, which the shared
    range checks raise directly. Catch ``InputError`` to catch both.
    """


#: §9.2's note. The nodes co-own these two signs, so the lord is ambiguous
#: until a strength comparison picks one.
DUAL_LORDED: dict[int, tuple[int, int]] = {
    Rasi.AQUARIUS: (Graha.SATURN, Graha.RAHU),
    Rasi.SCORPIO: (Graha.MARS, Graha.KETU),
}

#: The chapter that defines the comparison §9.2 defers to. §15.5.1 is the
#: section within it, and `charts/colord.py` implements it.
STRENGTH_COMPARISON_CHAPTER = "Strength of Planets and Rasis"

#: Table 18 — the specific names each arudha goes by, as printed.
#:
#: Transcribed verbatim, including the book's own inconsistency in row A3,
#: which writes "Bhatrarudha" and "Bhratri pada" — the first missing the r
#: that the second has. Not corrected; see docs/book-deviations.md D-21.
ARUDHA_SPECIFIC_NAMES: dict[int, tuple[str, ...]] = {
    1: ("Arudha lagna", "Pada lagna", "Arudha", "Pada"),
    2: ("Dhanarudha", "Vittarudha", "Dhana pada", "Vitta pada"),
    3: ("Bhatrarudha", "Bhratri pada", "Vikramarudha", "Vikrama pada"),
    4: ("Matri pada", "Vahana pada", "Sukha pada", "Matrarudha",
        "Vahanarudha", "Sukharudha"),
    5: ("Mantra pada", "Mantrarudha", "Putrarudha", "Putra pada",
        "Buddhi pada"),
    6: ("Roga pada", "Satru pada", "Rogarudha", "Satrarudha"),
    7: ("Dara pada", "Dararudha"),
    8: ("Mrityu pada", "Kashta pada", "Kashtarudha", "Randhrarudha"),
    9: ("Bhagya pada", "Bhagyarudha", "Pitri pada", "Pitrarudha",
        "Dharma pada", "Guru pada"),
    10: ("Karma pada", "Karmarudha", "Swarga pada", "Swargarudha",
         "Rajya pada"),
    11: ("Labha pada", "Labharudha"),
    12: ("Upapada lagna", "Upapada", "Gaunapada", "Vyayarudha", "Moksha pada"),
}

#: §9.2: "Arudha pada of a house is simply called arudha or pada also."
ARUDHA_GENERIC_NAMES: tuple[str, ...] = ("arudha pada", "arudha", "pada")

#: §9.2: "we will denote the arudha pada on nth house with An", with two
#: special cases — A1 is the arudha lagna and A12 the upapada lagna.
ARUDHA_SYMBOLS: dict[int, str] = {n: f"A{n}" for n in range(1, 13)}
ARUDHA_SPECIAL_SYMBOLS: dict[int, str] = {1: "AL", 12: "UL"}
ARUDHA_SPECIAL_NAMES: dict[int, str] = {1: "Arudha Lagna", 12: "Upapada Lagna"}


@dataclass(frozen=True)
class Step:
    """One numbered step of §9.2, with what it produced and why."""

    number: int
    name: str
    description: str
    #: The sign this step lands on, where the step produces one.
    sign: int | None = None
    sign_name: str | None = None
    #: The count this step produces, where it produces one.
    count: int | None = None
    #: Extra detail — the lord chosen, whether the exception fired.
    detail: str | None = None


@dataclass(frozen=True)
class ArudhaPada:
    """An arudha pada with the full derivation that produced it."""

    house: int
    symbol: str
    #: The generic names §9.2 gives the concept, the same for every house.
    generic_names: tuple[str, ...]
    #: Table 18's specific names for this house's arudha.
    specific_names: tuple[str, ...]
    special_symbol: str | None
    special_name: str | None
    house_sign: int
    house_sign_name: str
    lord: int
    lord_name: str
    lord_sign: int
    lord_sign_name: str
    count: int
    #: The sign step 4 lands on, before the step 5 exception is considered.
    before_exception: int
    before_exception_name: str
    exception_applied: bool
    #: Which of the two exception conditions fired: 1, 7, or None.
    exception_position: int | None
    sign: int
    sign_name: str
    steps: tuple[Step, ...]


# --------------------------------------------------------------------------
# Step 1
# --------------------------------------------------------------------------

def house_sign(house: int, lagna_sign: int) -> int:
    """Step 1 — the sign containing the house of interest.

    Houses are counted from the lagna, so the 1st house is the lagna's sign
    and the nth is ``n - 1`` signs on from it.

    :param house: 1 to 12.
    :param lagna_sign: 0 = Aries. In a divisional chart, the lagna's sign *in
        that chart* — §9.2 applies "in the divisional chart of interest", so
        the caller passes the divisional lagna and gets the divisional arudha.
    :raises InputError: if either argument is out of range. Range checks
        come from :mod:`hora.core.validate`; :class:`ArudhaError` is a subclass,
        so catching ``InputError`` catches both.
    """
    number = validate.in_range("house", house, 1, 12)
    lagna = validate.in_range("lagna_sign", lagna_sign, 0, 11)
    return (lagna + number - 1) % 12


# --------------------------------------------------------------------------
# Step 2
# --------------------------------------------------------------------------

def lord_of(sign: int, stronger_lord: dict[int, int] | None = None) -> int:
    """The lord of a sign, resolving §9.2's note for the two dual-lorded ones.

    :param sign: 0 = Aries.
    :param stronger_lord: for Aquarius and Scorpio only — sign to the graha the
        caller has determined is stronger. Required when ``sign`` is one of
        those two.
    :raises ArudhaError: if a dual-lorded sign is given with no choice, or with
        a graha that does not own it.
    """
    index = validate.in_range("sign", sign, 0, 11)
    if index not in DUAL_LORDED:
        return int(RASI_LORD[index])

    owners = DUAL_LORDED[index]
    names = " or ".join(GRAHA_NAMES[g] for g in owners)
    chosen = (stronger_lord or {}).get(index)
    if chosen is None:
        raise ArudhaError(
            f"{RASI_NAMES[index]} is owned by {names}; section 9.2 says to "
            f"take the stronger lord, and section 15.5.1's cascade could not "
            f"decide between them from what was given. Supply "
            f"graha_longitudes so the cascade can reach its last rule, or "
            f"stronger_lord={{{index}: <graha>}} to name one yourself."
        )
    if chosen not in owners:
        raise ArudhaError(
            f"{GRAHA_NAMES[chosen]} does not own {RASI_NAMES[index]}; "
            f"expected {names}"
        )
    return int(chosen)


def lord_sign(lord: int, graha_signs: dict[int, int]) -> int:
    """Step 2 — the sign occupied by that lord.

    :param graha_signs: graha id -> the sign it occupies **in the same chart**
        the house was taken from.
    :raises ArudhaError: if the lord's position was not supplied.
    """
    if lord not in graha_signs:
        raise ArudhaError(
            f"no position given for {GRAHA_NAMES[lord]}, the lord of the house"
        )
    return validate.in_range(f"graha_signs[{GRAHA_NAMES[lord]}]", graha_signs[lord], 0, 11)


# --------------------------------------------------------------------------
# Steps 3 and 4
# --------------------------------------------------------------------------

def count_to_lord(from_sign: int, to_sign: int) -> int:
    """Step 3 — signs from the house to its lord, counting zodiacally.

    Inclusive of the starting sign, so a lord in its own house counts 1 and a
    lord in the 12th from it counts 12. "Counting is in the zodiacal direction
    always" — there is no shorter-way-round.

    §9.2's example: Gemini to Aquarius is 9.
    """
    start = validate.in_range("from_sign", from_sign, 0, 11)
    end = validate.in_range("to_sign", to_sign, 0, 11)
    return ((end - start) % 12) + 1


def advance_from_lord(lord_sign_index: int, count: int) -> int:
    """Step 4 — the same count again, starting from the lord's sign.

    Inclusive in the same sense as step 3, so a count of 1 stays put.

    §9.2's example: 9 signs from Aquarius ends in Libra.
    """
    start = validate.in_range("lord_sign", lord_sign_index, 0, 11)
    steps = validate.in_range("count", count, 1, 12)
    return (start + steps - 1) % 12


# --------------------------------------------------------------------------
# Step 5
# --------------------------------------------------------------------------

def exception_position(landed: int, original: int) -> int | None:
    """Where step 4's sign falls from step 1's, if it is one the rule names.

    :returns: 1 or 7 when the exception applies, otherwise ``None``.

    These are the only two positions it can land on, and not by coincidence:
    step 4's sign is ``2L - H``, which is congruent to ``H`` exactly when the
    lord sits in the house itself or in the 7th from it.
    """
    position = count_to_lord(original, landed)
    return position if position in (1, 7) else None


def apply_exception(landed: int, original: int) -> tuple[int, int | None]:
    """Step 5 — if step 4's sign is the 1st or 7th from step 1's, take the 10th.

    "Otherwise we don't make any change."

    :returns: ``(sign, exception_position)`` where the position is 1, 7 or
        ``None``.
    """
    position = exception_position(landed, original)
    if position is None:
        return landed, None
    return (landed + 9) % 12, position


# --------------------------------------------------------------------------
# Step 6 — the whole procedure
# --------------------------------------------------------------------------

def arudha_pada(
    house: int,
    lagna_sign: int,
    graha_signs: dict[int, int],
    stronger_lord: dict[int, int] | None = None,
) -> ArudhaPada:
    """Run all six steps of §9.2 for one house, keeping every intermediate.

    :param house: 1 to 12.
    :param lagna_sign: the lagna's sign in the chart of interest, 0 = Aries.
    :param graha_signs: graha id -> occupied sign, in that same chart.
    :param stronger_lord: sign -> graha, for Aquarius and Scorpio only.
    :raises ArudhaError: on any out-of-range input, a missing graha position,
        or an unresolved dual lordship.
    """
    steps: list[Step] = []

    # Step 1
    origin = house_sign(house, lagna_sign)
    steps.append(Step(
        1, "house_sign",
        "Take the sign containing the house of interest",
        sign=origin, sign_name=RASI_NAMES[origin],
        detail=f"house {house} from lagna in {RASI_NAMES[lagna_sign]}",
    ))

    # Step 2
    lord = lord_of(origin, stronger_lord)
    occupied = lord_sign(lord, graha_signs)
    detail = f"lord of {RASI_NAMES[origin]} is {GRAHA_NAMES[lord]}"
    if origin in DUAL_LORDED:
        other = next(g for g in DUAL_LORDED[origin] if g != lord)
        detail += f", taken as stronger than {GRAHA_NAMES[other]}"
    steps.append(Step(
        2, "lord_sign", "Find the sign occupied by the lord of that house",
        sign=occupied, sign_name=RASI_NAMES[occupied], detail=detail,
    ))

    # Step 3
    count = count_to_lord(origin, occupied)
    steps.append(Step(
        3, "count_to_lord",
        "Count signs from the house of interest to the sign containing its "
        "lord, zodiacally",
        count=count,
        detail=f"{RASI_NAMES[origin]} to {RASI_NAMES[occupied]} is {count}",
    ))

    # Step 4
    landed = advance_from_lord(occupied, count)
    steps.append(Step(
        4, "advance_from_lord",
        "Count the same number of signs from the sign containing the lord",
        sign=landed, sign_name=RASI_NAMES[landed], count=count,
        detail=f"{count} signs from {RASI_NAMES[occupied]} ends in {RASI_NAMES[landed]}",
    ))

    # Step 5
    final, position = apply_exception(landed, origin)
    if position is None:
        detail = (
            f"{RASI_NAMES[landed]} is the "
            f"{count_to_lord(origin, landed)}th from {RASI_NAMES[origin]}, "
            f"neither 1st nor 7th — no change"
        )
    else:
        detail = (
            f"{RASI_NAMES[landed]} is the {position}th from {RASI_NAMES[origin]}, "
            f"so take the 10th from it and get {RASI_NAMES[final]}"
        )
    steps.append(Step(
        5, "apply_exception",
        "If the sign found is the 1st or 7th from the original, take the 10th "
        "sign from it; otherwise no change",
        sign=final, sign_name=RASI_NAMES[final], detail=detail,
    ))

    # Step 6
    steps.append(Step(
        6, "arudha_pada",
        "The resulting sign contains the arudha pada of the house of interest",
        sign=final, sign_name=RASI_NAMES[final],
    ))

    return ArudhaPada(
        house=house,
        symbol=ARUDHA_SYMBOLS[house],
        generic_names=ARUDHA_GENERIC_NAMES,
        specific_names=ARUDHA_SPECIFIC_NAMES[house],
        special_symbol=ARUDHA_SPECIAL_SYMBOLS.get(house),
        special_name=ARUDHA_SPECIAL_NAMES.get(house),
        house_sign=origin, house_sign_name=RASI_NAMES[origin],
        lord=lord, lord_name=GRAHA_NAMES[lord],
        lord_sign=occupied, lord_sign_name=RASI_NAMES[occupied],
        count=count,
        before_exception=landed, before_exception_name=RASI_NAMES[landed],
        exception_applied=position is not None,
        exception_position=position,
        sign=final, sign_name=RASI_NAMES[final],
        steps=tuple(steps),
    )


def all_arudha_padas(
    lagna_sign: int,
    graha_signs: dict[int, int],
    stronger_lord: dict[int, int] | None = None,
) -> list[ArudhaPada]:
    """All twelve arudha padas, A1 to A12."""
    return [
        arudha_pada(house, lagna_sign, graha_signs, stronger_lord)
        for house in range(1, 13)
    ]
