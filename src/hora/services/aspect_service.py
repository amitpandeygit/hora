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
    ASPECT_SOURCE,
    ASPECTED_PLANET_EXAMPLE,
    ASPECTED_PLANET_RULE,
    ASPECTS_ARE_A_SKILL_NOTE,
    DRISHTI_MEANS,
    FIGURE_2_NOTE,
    GRAHA_NAMES,
    INFLUENCE_DEPENDS_ON_RECEIVER,
    INFLUENCE_MAY_NOT_LAND,
    MALEFIC_INFLUENCE_ANALOGY,
    MODALITY_NAMES_EN,
    NAVAGRAHA,
    PRIEST_AND_BROTHER_ANALOGY,
    RASI_DRISHTI_GRAHA_EXAMPLE,
    RASI_DRISHTI_GRAHA_RULE,
    RASI_DRISHTI_INTRO,
    RASI_DRISHTI_IS_MUTUAL,
    RASI_DRISHTI_RULES,
    RASI_DRISHTI_SAME_TARGETS_DIFFERENT_NATURE,
    RASI_MODALITY,
    RASI_NAMES,
    SEVENTH_HOUSE_ANALOGY,
    SEVENTH_HOUSE_RULE,
    SPECIAL_ASPECT_BULLETS,
    SPECIAL_ASPECT_GRAHAS,
    SPECIAL_ASPECT_RULE,
    Graha,
)

#: §10.3 names the modalities in English — "movable", "fixed", "dual" — which
#: is exactly `MODALITY_NAMES_EN`, indexed the same way as `RASI_MODALITY`.
#: Reusing it rather than restating the three words keeps one source.
MODALITY_INDEX = {name: index for index, name in enumerate(MODALITY_NAMES_EN)}

InputError = validate.InputError

__all__ = [
    "InputError", "between", "chart", "graha", "rasi", "rules",
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
        # §10.4: the two kinds are not interchangeable, and a caller reading
        # both flat would treat them as if they were. Each block says what its
        # aspect is *due to* and whether a co-located graha would share it.
        "graha_drishti_due_to": ASPECT_SOURCE["graha_drishti"]["due_to"],
        "rasi_drishti_due_to": ASPECT_SOURCE["rasi_drishti"]["due_to"],
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
        # §10.3: "A planet aspects the signs aspected by the sign it occupies.
        # It also aspects the houses and planets in those signs." Same three
        # columns as graha drishti, because Exercise 15 asks for all three.
        "rasi_drishti_rasis": [
            {"rasi": r, "rasi_name": RASI_NAMES[r],
             "house": None if lagna_rasi is None else (r - int(lagna_rasi)) % 12 + 1}
            for r in rasi_drishti(rasi)
        ],
        "rasi_drishti_grahas": [
            {"graha": g, "graha_name": GRAHA_NAMES[g], "rasi": sign,
             "rasi_name": RASI_NAMES[sign]}
            for g, sign in sorted(others.items())
            if g != graha_id and sign in rasi_drishti(rasi)
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

    graha_drishti_casters = ASPECTING_GRAHAS
    if rahu_ketu_aspects:
        graha_drishti_casters = tuple(NAVAGRAHA)

    # Every graha present casts rasi drishti, nodes included: §10.3 makes it a
    # property of the rasi, so nothing can be exempt. Exercise 15 asks about
    # all nine where Exercise 14 asks about seven, for exactly that reason.
    return {
        "lagna_rasi": None if lagna_rasi is None else int(lagna_rasi),
        "lagna_rasi_name": None if lagna_rasi is None else RASI_NAMES[int(lagna_rasi)],
        "aspecting_grahas": [int(g) for g in graha_drishti_casters if g in rasis],
        "rasi_drishti_grahas": [int(g) for g in NAVAGRAHA if g in rasis],
        "grahas": [
            graha(g, rasis[g], lagna_rasi=lagna_rasi, others=rasis,
                  rahu_ketu_aspects=rahu_ketu_aspects)
            for g in NAVAGRAHA if g in rasis
        ],
        "note": ASPECTED_PLANET_RULE,
        # §10.4, so the two kinds in `grahas` are read as the chapter means
        # them rather than as one flat list of aspects.
        "aspect_sources": {k: dict(v) for k, v in ASPECT_SOURCE.items()},
        "influence_caveat": INFLUENCE_DEPENDS_ON_RECEIVER,
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


def rasi(rasi_index: int) -> dict:
    """§10.3's rule for one rasi, with the rule and the excluded sign named.

    No graha involved: rasi drishti is a property of the sign, and this is the
    form Figure 2 draws.
    """
    validate.in_range("rasi", int(rasi_index), 0, 11)
    rasi_index = int(rasi_index)
    modality = MODALITY_NAMES_EN[RASI_MODALITY[rasi_index]]
    rule = next(r for r in RASI_DRISHTI_RULES if r["modality"] == modality)
    aspected = rasi_drishti(rasi_index)

    # The one sign of the aspected modality that is left out. A dual rasi
    # excludes only itself, which is why this is None there.
    excluded = None
    if modality != "dual":
        target = MODALITY_INDEX[rule["aspects"]]
        excluded = next(
            s for s in range(12)
            if RASI_MODALITY[s] == target and s not in aspected
        )

    return {
        "rasi": rasi_index,
        "rasi_name": RASI_NAMES[rasi_index],
        "modality": modality,
        "rule": rule["text"],
        "aspects_modality": rule["aspects"],
        "aspected_rasis": [
            {"rasi": r, "rasi_name": RASI_NAMES[r]} for r in aspected
        ],
        "excluded_rasi": excluded,
        "excluded_rasi_name": None if excluded is None else RASI_NAMES[excluded],
        "excluded_because": rule["excludes"],
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
        "rasi_drishti_intro": RASI_DRISHTI_INTRO,
        "rasi_drishti_rules": [dict(r) for r in RASI_DRISHTI_RULES],
        "rasi_drishti_is_mutual": RASI_DRISHTI_IS_MUTUAL,
        "rasi_drishti_graha_rule": RASI_DRISHTI_GRAHA_RULE,
        "rasi_drishti_graha_example": RASI_DRISHTI_GRAHA_EXAMPLE,
        "figure_2_note": FIGURE_2_NOTE,
        # Figure 2 draws one undirected line per aspecting pair. Computed, so
        # the count cannot drift from the rule.
        "figure_2_line_count": len({
            frozenset((s, t)) for s in range(12) for t in rasi_drishti(s)
        }),
        # §10.4. Comparative only — the chapter says "greater" and "limited",
        # never a number, and quantifying it would be our invention.
        "aspect_sources": {k: dict(v) for k, v in ASPECT_SOURCE.items()},
        "same_sign_note": RASI_DRISHTI_SAME_TARGETS_DIFFERENT_NATURE,
        "seventh_house_analogy": SEVENTH_HOUSE_ANALOGY,
        "priest_and_brother_analogy": PRIEST_AND_BROTHER_ANALOGY,
        "malefic_influence_analogy": MALEFIC_INFLUENCE_ANALOGY,
        "influence_may_not_land": INFLUENCE_MAY_NOT_LAND,
        "influence_caveat": INFLUENCE_DEPENDS_ON_RECEIVER,
    }
