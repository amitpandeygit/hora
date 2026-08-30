"""Section 13.3 — baadhaka sthaanas and baadhakas.

The baadhaka of a house is relative to that house, not to lagna. §13.3 ends by
saying so outright: "we can consider baadhaka from every house and arudha pada
in every divisional chart". So every function here takes the sign of whatever
is being read and never assumes it is the lagna.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.colord import CO_LORDS as _CO_LORDS
from hora.core import validate
from hora.core.const import (
    BAADHAKA_HOUSE_BY_MODALITY,
    GRAHA_NAMES,
    MODALITY_NAMES_EN,
    RASI_ABBR,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
)

#: §15.5.1's two co-owned rasis, reused rather than retyped. Table 31 names
#: **both** lords of each as baadhakas, so no stronger-co-lord cascade runs
#: here — unlike §9.2's arudha, which needs exactly one of them.
CO_LORDS: dict[int, tuple[int, int]] = {
    int(rasi): (int(first), int(second))
    for rasi, (first, second) in _CO_LORDS.items()
}


class BaadhakaError(validate.InputError):
    """Raised when a baadhaka question cannot be answered."""


@dataclass(frozen=True)
class Baadhaka:
    """The baadhaka sthaana of one sign, and who troubles from it."""

    #: The sign being read — a house's sign or an arudha's, not necessarily
    #: the lagna's.
    sign: int
    #: "movable", "fixed" or "dual".
    modality: str
    #: 11, 9 or 7 — which house from `sign` the sthaana is.
    house: int
    #: The sthaana's sign.
    sthaana: int
    #: Its lord or lords. Two when the sthaana is co-owned.
    lords: tuple[int, ...]
    #: Grahas sitting in the sthaana, when the caller supplied positions.
    #: §13.3 troubles through these as well as through the lords.
    occupants: tuple[int, ...] = ()
    why: str = ""


def _lords_of(sign: int) -> tuple[int, ...]:
    if sign in CO_LORDS:
        return CO_LORDS[sign]
    return (int(RASI_LORD[sign]),)


def baadhaka_sthaana(sign: int) -> int:
    """The troubling spot for a house or arudha falling in `sign`."""
    index = validate.in_range("sign", sign, 0, 11)
    house = BAADHAKA_HOUSE_BY_MODALITY[RASI_MODALITY[index]]
    return (index + house - 1) % 12


def baadhakas(sign: int) -> tuple[int, ...]:
    """The lord or lords of `sign`'s baadhaka sthaana."""
    return _lords_of(baadhaka_sthaana(sign))


def baadhaka_of(sign: int, graha_signs: dict[int, int] | None = None
                ) -> Baadhaka:
    """§13.3 for one sign, with the sthaana's occupants when they are known.

    :param graha_signs: graha id -> occupied sign, in the *same* chart the
        sign came from. Omitted, `occupants` is empty and the answer covers
        the lords only — which is stated in `why` rather than left implicit.
    """
    index = validate.in_range("sign", sign, 0, 11)
    modality = MODALITY_NAMES_EN[RASI_MODALITY[index]]
    house = BAADHAKA_HOUSE_BY_MODALITY[RASI_MODALITY[index]]
    sthaana = baadhaka_sthaana(index)
    lords = _lords_of(sthaana)

    occupants: tuple[int, ...] = ()
    tail = (
        "; no positions were given, so this covers the lord"
        f"{'s' if len(lords) > 1 else ''} only and not the sthaana's occupants"
    )
    if graha_signs is not None:
        for graha, place in graha_signs.items():
            validate.in_range(f"graha {graha} sign", int(place), 0, 11)
        occupants = tuple(sorted(
            int(g) for g, place in graha_signs.items() if int(place) == sthaana
        ))
        tail = (
            f"; {', '.join(GRAHA_NAMES[g] for g in occupants)} "
            f"{'occupies' if len(occupants) == 1 else 'occupy'} it, and "
            f"section 13.3 troubles through occupants as well as lords"
            if occupants else
            "; nothing occupies the sthaana, so only the lord"
            f"{'s' if len(lords) > 1 else ''} trouble"
        )

    why = (
        f"{RASI_NAMES[index]} is {modality}, so the {house}th from it — "
        f"{RASI_NAMES[sthaana]} — is its baadhaka sthaana, and "
        f"{' and '.join(GRAHA_NAMES[g] for g in lords)} "
        f"{'is its lord' if len(lords) == 1 else 'are its co-lords'}"
        + tail
    )
    return Baadhaka(index, modality, house, sthaana, lords, occupants, why)


def is_baadhaka(graha: int, sign: int,
                graha_signs: dict[int, int] | None = None) -> dict:
    """Whether `graha` troubles whatever falls in `sign`, and why either way.

    Never a bare false: the reason is always given, and a graha that troubles
    only by occupancy is distinguished from one that troubles by lordship.
    """
    result = baadhaka_of(sign, graha_signs)
    by_lordship = int(graha) in result.lords
    by_occupancy = int(graha) in result.occupants
    if by_lordship or by_occupancy:
        how = " and ".join(
            part for part, on in (("lordship", by_lordship),
                                  ("occupancy", by_occupancy)) if on)
        why = (
            f"{GRAHA_NAMES[int(graha)]} is a baadhaka for "
            f"{RASI_NAMES[result.sign]} by {how}: the baadhaka sthaana is "
            f"{RASI_NAMES[result.sthaana]}"
        )
    elif graha_signs is None:
        why = (
            f"{GRAHA_NAMES[int(graha)]} does not own "
            f"{RASI_NAMES[result.sthaana]}, the baadhaka sthaana for "
            f"{RASI_NAMES[result.sign]}; whether it occupies that sthaana "
            f"cannot be decided without graha positions"
        )
    else:
        why = (
            f"{GRAHA_NAMES[int(graha)]} neither owns nor occupies "
            f"{RASI_NAMES[result.sthaana]}, the baadhaka sthaana for "
            f"{RASI_NAMES[result.sign]}"
        )
    return {
        "graha": int(graha),
        "graha_name": str(GRAHA_NAMES[int(graha)]),
        "sign": result.sign,
        "sign_name": str(RASI_NAMES[result.sign]),
        "sthaana": result.sthaana,
        "sthaana_name": str(RASI_NAMES[result.sthaana]),
        "by_lordship": by_lordship,
        "by_occupancy": by_occupancy,
        "occupancy_known": graha_signs is not None,
        "is_baadhaka": by_lordship or by_occupancy,
        "why": why,
    }


def table_31() -> dict[str, tuple[str, tuple[str, ...]]]:
    """Table 31, derived. Compared against the transcription by a test."""
    return {
        RASI_ABBR[sign]: (
            RASI_ABBR[baadhaka_sthaana(sign)],
            tuple(str(GRAHA_NAMES[g]) for g in baadhakas(sign)),
        )
        for sign in range(12)
    }
