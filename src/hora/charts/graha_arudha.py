"""Graha arudhas — book §9.5.

    "Just as arudha padas of all houses (bhavas) are defined, arudha padas of
    all the nine planets (grahas) are also defined and they are called graha
    arudhas."

The dual of §9.2. A bhava arudha starts from a house's sign and looks up its
**lord**; a graha arudha starts from a planet's sign and looks up the sign that
planet **owns**. Steps 3 to 6 are then identical, and are reused from
:mod:`hora.charts.arudha` rather than restated.

    1  the sign containing the planet, in the divisional chart of interest
    2  the sign owned by that planet — the stronger, where it owns two
    3  count from the planet's sign to that owned sign, zodiacally
    4  the same count again from the owned sign
    5  1st or 7th from the original -> take the 10th
    6  the resulting sign holds the planet's arudha pada

Step 2's NOTE sends the two-sign case to §15.5.2, and that section's own note
guarantees it always resolves: "the two rasis owned by each planet have a
different oddity", so rule 4 settles any tie that survives rules 1 to 3. No
dasa input is ever needed — see docs/open-items.md OI-29.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.arudha import Step, advance_from_lord, apply_exception, count_to_lord
from hora.charts.rasi_strength import stronger as stronger_rasi
from hora.core import validate
from hora.core.const import GRAHA_NAMES, GRAHA_OWNS, RASI_NAMES, Graha


class GrahaArudhaError(validate.InputError):
    """A graha arudha input that cannot be resolved.

    A subclass of :class:`~hora.core.validate.InputError`, which the shared
    range checks raise directly. Catch ``InputError`` to catch both.
    """


#: §9.5's NOTE: "Mars, Mercury, Jupiter, Venus and Saturn own 2 signs each."
#: The Sun and Moon own one; Rahu and Ketu co-own one each, per §9.2's note.
TWO_SIGN_OWNERS = frozenset(
    graha for graha, signs in GRAHA_OWNS.items() if len(signs) == 2
)

#: §9.5 denotes these the way §9.2 denotes bhava arudhas, by the graha.
GRAHA_ARUDHA_SYMBOLS: dict[int, str] = {
    int(Graha.SUN): "AL(Su)", int(Graha.MOON): "AL(Mo)",
    int(Graha.MARS): "AL(Ma)", int(Graha.MERCURY): "AL(Me)",
    int(Graha.JUPITER): "AL(Ju)", int(Graha.VENUS): "AL(Ve)",
    int(Graha.SATURN): "AL(Sa)", int(Graha.RAHU): "AL(Ra)",
    int(Graha.KETU): "AL(Ke)",
}


@dataclass(frozen=True)
class GrahaArudha:
    """A planet's arudha pada with the derivation that produced it."""

    graha: int
    graha_name: str
    symbol: str
    graha_sign: int
    graha_sign_name: str
    #: Every sign the planet owns, in order.
    owned: tuple[int, ...]
    owned_names: tuple[str, ...]
    #: The one step 2 selects.
    owned_sign: int
    owned_sign_name: str
    #: How the stronger of two owned signs was chosen, or None when the planet
    #: owns only one.
    owned_decided_by: str | None
    owned_reason: str
    count: int
    before_exception: int
    before_exception_name: str
    exception_applied: bool
    exception_position: int | None
    sign: int
    sign_name: str
    steps: tuple[Step, ...]


def owned_sign(
    graha: int,
    graha_signs: dict[int, int],
    graha_longitudes: dict[int, float] | None = None,
) -> tuple[int, str | None, str]:
    """Step 2 — the sign owned by the planet, stronger of two where it owns two.

    :returns: ``(sign, decided_by, explanation)``. ``decided_by`` is None when
        the planet owns a single sign and no comparison was needed.
    :raises GrahaArudhaError: if the planet owns no sign, or if §15.5.2 cannot
        separate the two — which its own note says cannot happen, so this
        signals a defect rather than a missing input.
    """
    signs = GRAHA_OWNS.get(graha, ())
    if not signs:
        raise GrahaArudhaError(f"{GRAHA_NAMES[graha]} owns no sign")
    if len(signs) == 1:
        return int(signs[0]), None, (
            f"{GRAHA_NAMES[graha]} owns only {RASI_NAMES[signs[0]]}"
        )

    longitudes = graha_longitudes or {
        other: sign * 30.0 for other, sign in graha_signs.items()
    }
    verdict = stronger_rasi(int(signs[0]), int(signs[1]), longitudes)
    if verdict.winner is None:
        raise GrahaArudhaError(
            f"section 15.5.2 could not separate {RASI_NAMES[signs[0]]} and "
            f"{RASI_NAMES[signs[1]]}, the two signs {GRAHA_NAMES[graha]} owns. "
            f"Its own note says rule 4 always resolves this case, so this is a "
            f"defect, not a missing input: {verdict.reason}"
        )
    return verdict.winner, verdict.decided_by, (
        f"{verdict.winner_name} is the stronger of "
        f"{RASI_NAMES[signs[0]]} and {RASI_NAMES[signs[1]]}, by section 15.5.2 "
        f"rule {verdict.decided_by}"
    )


def graha_arudha(
    graha: int,
    graha_signs: dict[int, int],
    graha_longitudes: dict[int, float] | None = None,
) -> GrahaArudha:
    """Run all six steps of §9.5 for one planet, keeping every intermediate.

    :param graha_signs: graha id -> occupied sign, in the chart of interest.
        For a divisional graha arudha, pass that chart's signs.
    :param graha_longitudes: optional; lets §15.5.2's rule 6 run if the
        comparison ever reaches it.
    :raises InputError: on an out-of-range graha or a missing position.
    """
    index = validate.in_range("graha", graha, 0, 8)
    if index not in graha_signs:
        raise GrahaArudhaError(f"no position given for {GRAHA_NAMES[index]}")
    origin = validate.in_range(
        f"graha_signs[{GRAHA_NAMES[index]}]", graha_signs[index], 0, 11
    )

    steps: list[Step] = []

    # Step 1
    steps.append(Step(
        1, "graha_sign",
        "Take the sign containing the planet of interest in the divisional "
        "chart of interest",
        sign=origin, sign_name=RASI_NAMES[origin],
        detail=f"{GRAHA_NAMES[index]} is in {RASI_NAMES[origin]}",
    ))

    # Step 2
    owned, decided_by, why = owned_sign(index, graha_signs, graha_longitudes)
    steps.append(Step(
        2, "owned_sign", "Find the sign owned by that planet",
        sign=owned, sign_name=RASI_NAMES[owned], detail=why,
    ))

    # Step 3
    count = count_to_lord(origin, owned)
    steps.append(Step(
        3, "count_to_owned",
        "Count signs from the sign containing the planet of interest to the "
        "stronger sign owned by it, zodiacally",
        count=count,
        detail=f"{RASI_NAMES[origin]} to {RASI_NAMES[owned]} is {count}",
    ))

    # Step 4
    landed = advance_from_lord(owned, count)
    steps.append(Step(
        4, "advance_from_owned",
        "Count the same number of signs from the stronger sign owned",
        sign=landed, sign_name=RASI_NAMES[landed], count=count,
        detail=f"{count} signs from {RASI_NAMES[owned]} ends in {RASI_NAMES[landed]}",
    ))

    # Step 5
    final, position = apply_exception(landed, origin)
    if position is None:
        detail = (
            f"{RASI_NAMES[landed]} is the {count_to_lord(origin, landed)}th "
            f"from {RASI_NAMES[origin]}, neither 1st nor 7th — no change"
        )
    else:
        detail = (
            f"{RASI_NAMES[landed]} is the {position}th from {RASI_NAMES[origin]}, "
            f"so take the 10th from it and get {RASI_NAMES[final]}"
        )
    steps.append(Step(
        5, "apply_exception",
        "If the sign found is the 1st or 7th from the original sign containing "
        "the planet, take the 10th sign from it; otherwise no change",
        sign=final, sign_name=RASI_NAMES[final], detail=detail,
    ))

    # Step 6
    steps.append(Step(
        6, "graha_arudha",
        "The resulting sign contains the arudha pada of the planet of interest",
        sign=final, sign_name=RASI_NAMES[final],
    ))

    all_owned = tuple(int(s) for s in GRAHA_OWNS[index])
    return GrahaArudha(
        graha=index, graha_name=GRAHA_NAMES[index],
        symbol=GRAHA_ARUDHA_SYMBOLS[index],
        graha_sign=origin, graha_sign_name=RASI_NAMES[origin],
        owned=all_owned,
        owned_names=tuple(RASI_NAMES[s] for s in all_owned),
        owned_sign=owned, owned_sign_name=RASI_NAMES[owned],
        owned_decided_by=decided_by, owned_reason=why,
        count=count,
        before_exception=landed, before_exception_name=RASI_NAMES[landed],
        exception_applied=position is not None,
        exception_position=position,
        sign=final, sign_name=RASI_NAMES[final],
        steps=tuple(steps),
    )


def all_graha_arudhas(
    graha_signs: dict[int, int],
    graha_longitudes: dict[int, float] | None = None,
) -> list[GrahaArudha]:
    """All nine graha arudhas — §9.5 defines them for every planet."""
    return [
        graha_arudha(graha, graha_signs, graha_longitudes)
        for graha in range(9)
    ]
