"""Aspect endpoints — book chapter 10.

§10.2 computes three things from one placement, and a caller wants all three:
the rasis a graha aspects, the houses those rasis are (which needs a lagna),
and the grahas sitting in them (which needs the other placements). Splitting
them across three calls would make the caller re-derive the chart each time,
so :func:`chart` answers all three at once and the smaller endpoints exist for
a single graha or for the rules in isolation.
"""
from __future__ import annotations

from hora.charts.aspects import (
    graha_aspects_sign,
    graha_drishti_houses,
    rasi_drishti,
)
from hora.core import validate
from hora.core.const import (
    ASPECT_DEFINITION,
    ASPECT_KINDS,
    ASPECTED_PLANET_EXAMPLE,
    ASPECTED_PLANET_RULE,
    ASPECTS_ARE_A_SKILL_NOTE,
    DRISHTI_MEANS,
    GRAHA_NAMES,
    NAVAGRAHA,
    RASI_NAMES,
    SEVENTH_HOUSE_RULE,
    SPECIAL_ASPECT_BULLETS,
    SPECIAL_ASPECT_GRAHAS,
    SPECIAL_ASPECT_RULE,
    Graha,
)

InputError = validate.InputError

__all__ = [
    "InputError", "chart", "graha", "rules",
]

#: §10.2's own list of aspecting grahas, which is the seven. The nodes are not
#: given aspects by this chapter; they can still be *aspected*, because that
#: depends only on where they sit.
ASPECTING_GRAHAS: tuple[int, ...] = tuple(
    g for g in NAVAGRAHA if g not in (Graha.RAHU, Graha.KETU)
)


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


def graha(
    graha_id: int,
    rasi: int,
    *,
    lagna_rasi: int | None = None,
    others: dict[int, int] | None = None,
    rahu_ketu_aspects: bool = False,
) -> dict:
    """What one graha aspects from one rasi.

    ``lagna_rasi`` turns the aspected rasis into house numbers; ``others``
    turns them into aspected grahas. Both are optional because §10.2's own
    examples work from a bare placement — "Sun in Ta aspects Sc" needs
    neither.
    """
    if int(graha_id) not in set(NAVAGRAHA):
        raise InputError(f"unknown graha {graha_id!r}")
    graha_id = int(graha_id)
    validate.in_range("rasi", int(rasi), 0, 11)
    rasi = int(rasi)
    if lagna_rasi is not None:
        validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    others = _validate_rasis(others) if others else {}

    houses_aspected = graha_drishti_houses(graha_id, rahu_ketu_aspects=rahu_ketu_aspects)
    # Ordered by distance from the graha, which is the order the chapter
    # prints them in: the 5th before the 7th before the 9th.
    rasis = [(rasi + h - 1) % 12 for h in houses_aspected]

    return {
        "graha": graha_id,
        "graha_name": GRAHA_NAMES[graha_id],
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "aspects_houses_from_itself": list(houses_aspected),
        "has_special_aspect": graha_id in SPECIAL_ASPECT_GRAHAS,
        "aspected_rasis": [
            {"rasi": r, "rasi_name": RASI_NAMES[r],
             "house_from_graha": (r - rasi) % 12 + 1,
             "house": None if lagna_rasi is None else (r - int(lagna_rasi)) % 12 + 1}
            for r in rasis
        ],
        "aspected_grahas": [
            {"graha": g, "graha_name": GRAHA_NAMES[g], "rasi": s,
             "rasi_name": RASI_NAMES[s]}
            for g, s in sorted(others.items())
            if g != graha_id and s in rasis
        ],
        "rasi_drishti_rasis": [
            {"rasi": r, "rasi_name": RASI_NAMES[r]} for r in rasi_drishti(rasi)
        ],
    }


def chart(
    rasis: dict[int, int],
    lagna_rasi: int | None = None,
    *,
    rahu_ketu_aspects: bool = False,
) -> dict:
    """Every graha drishti in one chart — the shape Exercise 14 asks for.

    Only the seven aspect under §10.2; Rahu and Ketu appear in
    ``aspected_grahas`` when they sit in an aspected rasi, which is how the
    chapter's own exercise answer lists them.
    """
    rasis = _validate_rasis(rasis)
    if lagna_rasi is not None:
        validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)

    aspecting = ASPECTING_GRAHAS
    if rahu_ketu_aspects:
        aspecting = tuple(NAVAGRAHA)

    return {
        "lagna_rasi": None if lagna_rasi is None else int(lagna_rasi),
        "lagna_rasi_name": None if lagna_rasi is None else RASI_NAMES[int(lagna_rasi)],
        "aspecting_grahas": [int(g) for g in aspecting if g in rasis],
        "grahas": [
            graha(g, rasis[g], lagna_rasi=lagna_rasi, others=rasis,
                  rahu_ketu_aspects=rahu_ketu_aspects)
            for g in aspecting if g in rasis
        ],
        "note": ASPECTED_PLANET_RULE,
    }


def between(
    graha_id: int, graha_rasi: int, target_rasi: int, *,
    rahu_ketu_aspects: bool = False,
) -> dict:
    """Whether one graha aspects one rasi, with the house that decides it."""
    if int(graha_id) not in set(NAVAGRAHA):
        raise InputError(f"unknown graha {graha_id!r}")
    validate.in_range("graha_rasi", int(graha_rasi), 0, 11)
    validate.in_range("target_rasi", int(target_rasi), 0, 11)
    graha_id, graha_rasi, target_rasi = int(graha_id), int(graha_rasi), int(target_rasi)
    house = (target_rasi - graha_rasi) % 12 + 1
    return {
        "graha": graha_id,
        "graha_name": GRAHA_NAMES[graha_id],
        "graha_rasi": graha_rasi,
        "graha_rasi_name": RASI_NAMES[graha_rasi],
        "target_rasi": target_rasi,
        "target_rasi_name": RASI_NAMES[target_rasi],
        "house_from_graha": house,
        "aspects": graha_aspects_sign(
            graha_id, graha_rasi, target_rasi, rahu_ketu_aspects=rahu_ketu_aspects),
        "graha_aspects_houses": list(
            graha_drishti_houses(graha_id, rahu_ketu_aspects=rahu_ketu_aspects)),
    }


def rules() -> dict:
    """Chapter 10's rules as the chapter states them."""
    return {
        "definition": ASPECT_DEFINITION,
        "drishti_means": DRISHTI_MEANS,
        "kinds": [
            {"key": key, **{k: v for k, v in entry.items()}}
            for key, entry in ASPECT_KINDS.items()
        ],
        "seventh_house_rule": SEVENTH_HOUSE_RULE,
        "special_aspect_rule": SPECIAL_ASPECT_RULE,
        "special_aspects": [
            {"graha": int(b["graha"]), "graha_name": GRAHA_NAMES[b["graha"]],
             "houses": list(b["houses"]),
             "all_houses": sorted({7, *b["houses"]}), "text": b["text"]}
            for b in SPECIAL_ASPECT_BULLETS
        ],
        "aspected_planet_rule": ASPECTED_PLANET_RULE,
        "aspected_planet_example": ASPECTED_PLANET_EXAMPLE,
        "aspecting_grahas": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g]} for g in ASPECTING_GRAHAS
        ],
        "nodes_note": (
            "Section 10.2 gives special aspects to Mars, Jupiter and Saturn "
            "only, and names no aspect for Rahu or Ketu. They are therefore "
            "not among the aspecting grahas by default, though they are "
            "aspected like any other graha when they occupy an aspected rasi. "
            "Exercise 14's own answer lists Ketu and Rahu as aspected."
        ),
        "skill_note": ASPECTS_ARE_A_SKILL_NOTE,
    }
