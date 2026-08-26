"""Drishti — Parashari sign aspects and planetary aspects."""
from __future__ import annotations

from hora.core.const import RASI_MODALITY, SPECIAL_ASPECTS, Graha

#: Jaimini rasi drishti, as 0-based sign offsets.
#:
#: A movable rasi aspects the fixed rasis other than the one next to it; a
#: fixed rasi aspects the movable rasis other than the one before it; a dual
#: rasi aspects the other three dual rasis.
#:
#: **Corrected 2026-08-26.** These were previously ``{0: (4, 6, 8),
#: 1: (2, 4, 10), 2: (2, 6, 10)}``, which is wrong in all three rows: each sent
#: a rasi to targets of the wrong modality, and Leo did not aspect Aries, which
#: section 15.5.1's own worked example requires. See docs/open-items.md OI-27.
_RASI_DRISHTI_OFFSETS = {
    0: (4, 7, 10),   # movable -> the fixed rasis, except the next one
    1: (2, 5, 8),    # fixed -> the movable rasis, except the previous one
    2: (3, 6, 9),    # dual -> the other three dual rasis
}

#: Which modality a rasi of each modality aspects. Movable and fixed aspect
#: each other; dual aspects only dual.
_ASPECTED_MODALITY = {0: 1, 1: 0, 2: 2}


def rasi_drishti(sign: int) -> tuple[int, ...]:
    """Signs aspected by a sign under Jaimini's rasi drishti.

    Aspects are mutual: if A aspects B then B aspects A. No sign aspects
    itself. Both properties are asserted in
    ``tests/unit/test_rasi_drishti.py``.
    """
    return tuple((sign + o) % 12 for o in _RASI_DRISHTI_OFFSETS[RASI_MODALITY[sign]])


def graha_drishti_houses(graha: int, *, rahu_ketu_aspects: bool = False) -> tuple[int, ...]:
    """Houses (counted from the graha, 1-based) that a graha aspects fully."""
    if graha in (Graha.RAHU, Graha.KETU) and not rahu_ketu_aspects:
        return (7,)
    extra = SPECIAL_ASPECTS.get(graha, ())
    return tuple(sorted({7, *extra}))


def graha_aspects_sign(graha: int, graha_sign: int, target_sign: int, *, rahu_ketu_aspects: bool = False) -> bool:
    """Whether a graha in ``graha_sign`` casts a full aspect on ``target_sign``."""
    house = (target_sign - graha_sign) % 12 + 1
    return house in graha_drishti_houses(graha, rahu_ketu_aspects=rahu_ketu_aspects)


#: Parashari partial-aspect table (virupas out of 60) by house distance.
#: Index is the house counted from the graha, 1-based.
_PARTIAL: dict[int, dict[int, int]] = {
    Graha.MARS:    {4: 60, 7: 60, 8: 60, 5: 15, 9: 15, 3: 30, 10: 30},
    Graha.JUPITER: {5: 60, 7: 60, 9: 60, 4: 15, 8: 15, 3: 30, 10: 30},
    Graha.SATURN:  {3: 60, 7: 60, 10: 60, 4: 15, 8: 15, 5: 30, 9: 30},
}
_PARTIAL_DEFAULT = {7: 60, 4: 15, 8: 15, 5: 30, 9: 30, 3: 30, 10: 30}


def drishti_value(graha: int, from_sign: int, to_sign: int) -> int:
    """Aspect strength in virupas (0-60), used by drik bala and ashtakavarga."""
    house = (to_sign - from_sign) % 12 + 1
    table = _PARTIAL.get(graha, _PARTIAL_DEFAULT)
    return table.get(house, 0)
