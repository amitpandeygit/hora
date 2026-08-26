"""Argala and virodhargala endpoints — book chapter 10, §10.5 and §10.6.

Exercise 16 asks for every argala and virodhargala on all twelve houses at
once, so :func:`chart` answers in that shape. :func:`on_sign` answers one
target, which is the form §10.6's own worked example takes.

The 3rd-house malefic rule needs to know which grahas are malefic, and
chapter 3 makes that conditional for the Moon and Mercury. The caller supplies
the nature; this service never guesses one.
"""
from __future__ import annotations

from hora.charts.argala import (
    argalas_on_sign,
    counts_anti_zodiacally,
    ketu_sign_of,
    occupants_from,
)
from hora.core import validate
from hora.core.const import (
    ARGALA_BY_NATURE,
    ARGALA_PAIRS,
    GRAHA_NAMES,
    KETU_REVERSES_ARGALA,
    NAVAGRAHA,
    RASI_NAMES,
    SEVERAL_MALEFICS,
    THIRD_HOUSE_MALEFIC_RULE,
    VIRODHARGALA_DEFINITION,
    VIRODHARGALA_RULE,
    Graha,
)

InputError = validate.InputError

__all__ = ["InputError", "chart", "on_sign", "rules"]

#: The grahas chapter 3 fixes as malefic whatever the chart. The Moon and
#: Mercury are conditional there and are deliberately left out: a caller who
#: wants the 3rd-house rule to see them must say so.
FIXED_MALEFICS: frozenset[int] = frozenset(
    {Graha.SUN, Graha.MARS, Graha.SATURN, Graha.RAHU, Graha.KETU}
)


#: House ordinals as the book writes them — 1st, 2nd, 3rd, then -th.
_ORDINAL_SUFFIX = {1: "st", 2: "nd", 3: "rd"}


def _ordinal(house: int) -> str:
    return f"{house}{_ORDINAL_SUFFIX.get(house, 'th')}"


def _validate_rasis(rasis: dict[int, int]) -> dict[int, int]:
    if not rasis:
        raise InputError("no placements given; supply at least one graha and rasi")
    out = {}
    for graha, rasi in rasis.items():
        if int(graha) not in set(NAVAGRAHA):
            raise InputError(f"unknown graha {graha!r}")
        validate.in_range(f"rasi for {GRAHA_NAMES[int(graha)]}", int(rasi), 0, 11)
        out[int(graha)] = int(rasi)
    return out


def _resolve_malefics(malefics: list[int] | None) -> frozenset[int]:
    if malefics is None:
        return FIXED_MALEFICS
    out = set()
    for graha in malefics:
        if int(graha) not in set(NAVAGRAHA):
            raise InputError(f"unknown graha {graha!r} in malefics")
        out.add(int(graha))
    return frozenset(out)


def _row(entry, occupants) -> dict:
    return {
        "kind": entry.kind,
        "house": entry.house,
        "sign": entry.sign,
        "sign_name": RASI_NAMES[entry.sign],
        "grahas": [
            {"graha": g, "graha_name": GRAHA_NAMES[g]} for g in entry.grahas
        ],
        "obstructs" if entry.kind == "argala" else "obstructed_by":
            entry.paired_house,
        "paired_house": entry.paired_house,
        "present": bool(entry.grahas),
        "promoted_from_virodhargala": entry.promoted_from_virodhargala,
    }


def on_sign(
    sign: int,
    rasis: dict[int, int],
    *,
    malefics: list[int] | None = None,
    several: int | None = None,
) -> dict:
    """Every argala and virodhargala on one sign."""
    several = SEVERAL_MALEFICS if several is None else several
    validate.in_range("sign", int(sign), 0, 11)
    sign = int(sign)
    rasis = _validate_rasis(rasis)
    occupants = occupants_from(rasis)
    ketu = ketu_sign_of(rasis)
    malefic = _resolve_malefics(malefics)
    entries = argalas_on_sign(
        sign, occupants, ketu_sign=ketu, malefic=malefic, several=several)

    argalas = [e for e in entries if e.kind == "argala"]
    virodhas = [e for e in entries if e.kind == "virodhargala"]

    # §10.6: an argala is obstructed when its paired house is occupied. An
    # empty obstructor leaves it standing — "If Le (3rd from Ge) is empty,
    # this argala is unobstructed."
    obstructed = {v.house: bool(v.grahas) for v in virodhas}

    return {
        "sign": sign,
        "sign_name": RASI_NAMES[sign],
        "counted_anti_zodiacally": counts_anti_zodiacally(sign, ketu),
        "ketu_sign": ketu,
        "argalas": [
            {**_row(e, occupants),
             "obstructed": obstructed.get(e.paired_house, False)}
            for e in argalas
        ],
        "virodhargalas": [_row(e, occupants) for e in virodhas],
    }


def chart(
    rasis: dict[int, int],
    lagna_rasi: int,
    *,
    malefics: list[int] | None = None,
    several: int | None = None,
) -> dict:
    """Exercise 16's shape: all twelve houses, argalas and virodhargalas."""
    several = SEVERAL_MALEFICS if several is None else several
    rasis = _validate_rasis(rasis)
    validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    lagna_rasi = int(lagna_rasi)
    return {
        "lagna_rasi": lagna_rasi,
        "lagna_rasi_name": RASI_NAMES[lagna_rasi],
        "houses": [
            {"house": house,
             **on_sign((lagna_rasi + house - 1) % 12, rasis,
                       malefics=malefics, several=several)}
            for house in range(1, 13)
        ],
        "several_malefics_threshold": several,
    }


def rules() -> dict:
    """§10.6's rules, and what the engine does not decide."""
    return {
        "definition": VIRODHARGALA_DEFINITION,
        "rule": VIRODHARGALA_RULE,
        "pairs": [
            {"argala_house": a, "virodhargala_house": v,
             "text": f"the {_ordinal(v)} obstructs the argala from the {_ordinal(a)}"}
            for a, v in ARGALA_PAIRS
        ],
        "by_nature": {k: dict(v) for k, v in ARGALA_BY_NATURE.items()},
        "ketu_note": KETU_REVERSES_ARGALA,
        "third_house_rule": THIRD_HOUSE_MALEFIC_RULE,
        "several_malefics_threshold": SEVERAL_MALEFICS,
        "several_malefics_note": (
            "The book does not say how many malefics count as “several”. "
            "Exercise 16's own answer table leaves two malefics in the 3rd as "
            "virodhargala — Mars and Saturn in Sc, the 3rd from the 11th "
            "house — so three is the smallest threshold that reproduces "
            "it. Configurable per call. See docs/open-items.md OI-65."
        ),
        "fixed_malefics": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
            for g in sorted(FIXED_MALEFICS)
        ],
        "malefics_note": (
            "Chapter 3 makes the Moon and Mercury conditionally malefic, so "
            "they are not in the default set. Supply `malefics` to override it."
        ),
    }
