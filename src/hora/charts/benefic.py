"""Natural benefics and malefics — book §3.2.2.

    "(1) Jupiter and Venus are natural benefics (saumya grahas or subha
    grahas). Mercury becomes a natural benefic when he is alone or with more
    natural benefics. Waxing Moon of Sukla paksha is a natural benefic.
    (2) Sun, Mars, Rahu and Ketu are natural malefics (kroora grahas or paapa
    grahas). Mercury becomes a natural malefic when he is joined by more
    natural malefics. Waning Moon of Krishna paksha is a natural malefic."

Five of the nine are fixed. **Two are not**, and that is the whole point of
the section: Mercury takes its nature from its company, and the Moon takes its
nature from its phase. `NATURAL_BENEFIC` and `NATURAL_MALEFIC` in
`core/constants/graha.py` are the fixed sets only — Moon and Mercury are in
**neither**, so a caller that reads those sets alone silently treats both as
though they were nothing at all. This module is the rule those sets are half
of; see OI-45.

Saturn is a malefic here even though §3.2.2's list omits it — PVR-2, page 102
corroborates. See docs/precedence.md.

    "This information is important because the results given by planets are
    based on their inherent nature."
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    NATURAL_BENEFIC,
    NATURAL_MALEFIC,
    Graha,
)

#: §3.2.2's Sanskrit names for the two classes.
BENEFIC_NAMES = ("saumya graha", "subha graha")
MALEFIC_NAMES = ("kroora graha", "paapa graha")

#: The two whose nature is not fixed. Both are named in §3.2.2 twice, once in
#: the benefic clause and once in the malefic clause.
CONDITIONAL = frozenset({Graha.MOON, Graha.MERCURY})

BENEFIC = "benefic"
MALEFIC = "malefic"
NEUTRAL = "neutral"

#: §3.2.2: "Waxing Moon of Sukla paksha is a natural benefic. Waning Moon of
#: Krishna paksha is a natural malefic." Paksha 0 is Sukla, 1 is Krishna,
#: matching PAKSHA_NAMES.
MOON_BY_PAKSHA = (BENEFIC, MALEFIC)

INHERENT_NATURE_NOTE = (
    "This information is important because the results given by planets are "
    "based on their inherent nature."
)


class BeneficError(validate.InputError):
    """A benefic-status input that cannot be resolved."""


@dataclass(frozen=True)
class Nature:
    """A graha's natural benefic status, with why it came out that way."""

    graha: int
    graha_name: str
    nature: str
    conditional: bool
    reason: str


def _fixed(graha: int) -> str | None:
    if graha in NATURAL_BENEFIC:
        return BENEFIC
    if graha in NATURAL_MALEFIC:
        return MALEFIC
    return None


def moon_nature(paksha: int) -> str:
    """The Moon's nature from its fortnight.

    :param paksha: 0 for Sukla (waxing), 1 for Krishna (waning).
    """
    validate.in_range("paksha", paksha, 0, 1)
    return MOON_BY_PAKSHA[paksha]


def mercury_nature(companions: frozenset[int] | set[int] | None = None) -> str:
    """Mercury's nature from its company.

    "Mercury becomes a natural benefic when he is alone or with more natural
    benefics. Mercury becomes a natural malefic when he is joined by more
    natural malefics."

    So: alone is benefic; more benefics than malefics is benefic; more
    malefics is malefic. **An equal split is covered by neither clause** and
    is reported as neutral rather than being forced one way — see OI-45.

    :param companions: grahas sharing Mercury's rasi. None or empty is "alone".
    """
    others = {int(g) for g in (companions or set()) if int(g) != Graha.MERCURY}
    benefics = len(others & set(NATURAL_BENEFIC))
    malefics = len(others & set(NATURAL_MALEFIC))
    if not others:
        return BENEFIC
    if benefics > malefics:
        return BENEFIC
    if malefics > benefics:
        return MALEFIC
    return NEUTRAL


def nature(
    graha: int,
    *,
    paksha: int | None = None,
    companions: frozenset[int] | set[int] | None = None,
) -> Nature:
    """The natural benefic status of a graha.

    :param graha: 0 (Sun) to 8 (Ketu).
    :param paksha: required for the Moon; 0 Sukla, 1 Krishna.
    :param companions: the grahas sharing Mercury's rasi. Omit for "alone".
    :raises BeneficError: if the Moon is asked for without a paksha, since
        §3.2.2 gives the Moon no nature independent of its phase.
    """
    validate.in_range("graha", graha, 0, 8)
    fixed = _fixed(graha)
    if fixed is not None:
        return Nature(
            graha=graha,
            graha_name=str(GRAHA_NAMES[graha]),
            nature=fixed,
            conditional=False,
            reason=f"{GRAHA_NAMES[graha]} is a natural {fixed} in every chart",
        )
    if graha == Graha.MOON:
        if paksha is None:
            raise BeneficError(
                "the Moon's nature depends on the paksha, which section 3.2.2 "
                "states as waxing/waning; pass paksha=0 for Sukla or 1 for "
                "Krishna"
            )
        result = moon_nature(paksha)
        phase = "Waxing Moon of Sukla paksha" if paksha == 0 else (
            "Waning Moon of Krishna paksha"
        )
        return Nature(graha, str(GRAHA_NAMES[graha]), result, True,
                      f"{phase} is a natural {result}")
    result = mercury_nature(companions)
    others = {int(g) for g in (companions or set()) if int(g) != Graha.MERCURY}
    if not others:
        reason = "Mercury is alone, so he is a natural benefic"
    elif result == NEUTRAL:
        reason = (
            "Mercury is joined by as many natural benefics as natural "
            "malefics; section 3.2.2 covers neither case, so no nature is "
            "asserted. See OI-45."
        )
    else:
        reason = f"Mercury is with more natural {result}s, so he is a natural {result}"
    return Nature(graha, str(GRAHA_NAMES[graha]), result, True, reason)


def fixed_grahas() -> dict[str, list[int]]:
    """The five whose nature never changes, and the two that do."""
    return {
        BENEFIC: sorted(int(g) for g in NATURAL_BENEFIC),
        MALEFIC: sorted(int(g) for g in NATURAL_MALEFIC),
        "conditional": sorted(int(g) for g in CONDITIONAL),
    }
