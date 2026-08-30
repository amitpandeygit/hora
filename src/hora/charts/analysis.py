"""Section 13.4.1 — the basic guidelines, made runnable.

Factors 1 to 4 are a choice of chart, house, reference and arudha; §13.4.1
gives worked correspondences for them and nothing more, so `plan` serves those
and says so plainly for any matter the section does not name.

Factor 5 is the computable one. §13.4.1 lists five ways a planet reaches the
house or arudha under analysis — rasi drishti, graha drishti, argala, the four
house classes counted *from that house*, and baadhaka — and every one of them
already exists elsewhere in the project. `influences_on` composes them.

Factor 6 points at the classical literature the book does not reproduce.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.argala import argalas_on_sign, ketu_sign_of, occupants_from
from hora.charts.aspects import graha_aspects_sign, rasi_drishti
from hora.charts.baadhaka import baadhaka_of
from hora.core import validate
from hora.core.const import (
    D24_MATTERS,
    DIVISIONAL_CHART_FOR,
    GRAHA_NAMES,
    INFLUENCE_FRAME,
    RASI_NAMES,
)


class AnalysisError(validate.InputError):
    """Raised when an analysis question cannot be answered."""


@dataclass(frozen=True)
class Plan:
    """Factors 1 to 4 for one matter, as far as §13.4.1 names them."""

    matter: str
    #: The divisional chart, e.g. "D24".
    chart: str
    #: The house to read, when §13.4.1 names one.
    house: int | None
    #: The references to count that house from — "lagna", "AL", a graha, or a
    #: phrase like "the 5th lord". §13.4.1 gives more than one for several
    #: matters: the default, then the karaka "when the relevant karakas are
    #: stronger".
    references: tuple[str, ...]
    #: The arudha to prefer over the house, when §13.4.1 names one.
    arudha: str | None
    why: str


def _matter_index() -> dict[str, Plan]:
    """Every matter §13.4.1 names, and nothing else."""
    plans: dict[str, Plan] = {}
    for matter, chart, note in DIVISIONAL_CHART_FOR:
        plans[matter] = Plan(matter, chart, None, ("lagna",), None, note)
    for matter, house, references, arudha, note in D24_MATTERS:
        plans[matter] = Plan(matter, "D24", house, references, arudha, note)
    return plans


MATTERS: dict[str, Plan] = _matter_index()


def plan(matter: str) -> Plan:
    """Factors 1 to 4 for a matter §13.4.1 names.

    :raises AnalysisError: for anything else. §13.4.1 teaches a method and
        works two charts through it; it is not a lookup table of every
        question a chart can be asked, and pretending otherwise would invent
        correspondences the book does not give.
    """
    if matter not in MATTERS:
        raise AnalysisError(
            f"section 13.4.1 does not name {matter!r}. It gives a method and "
            f"works these matters through it: "
            f"{', '.join(sorted(MATTERS))}. For anything else, choose the "
            f"chart, house, reference and arudha yourself and use "
            f"influences_on"
        )
    return MATTERS[matter]


@dataclass(frozen=True)
class Influence:
    """One way a planet reaches the house or arudha under analysis."""

    #: "rasi drishti", "graha drishti", "argala", one of the four house
    #: classes, or "baadhaka".
    kind: str
    graha: int
    graha_name: str
    #: What §13.4.1 says this influence does.
    effect: str
    detail: str


def influence_frame(sign: int) -> dict[str, dict]:
    """§13.4.1's four house classes, counted **from `sign`** and not lagna.

    "We can also judge the influences on a house by finding houses *with
    respect to* that house."
    """
    index = validate.in_range("sign", sign, 0, 11)
    return {
        name: {
            "houses": list(houses),
            "signs": [(index + house - 1) % 12 for house in houses],
            "effect": effect,
        }
        for name, houses, effect in INFLUENCE_FRAME
    }


def influences_on(sign: int, graha_signs: dict[int, int]) -> dict:
    """Every influence §13.4.1 names, on one house or arudha.

    :param sign: the rasi the house or arudha under analysis falls in. Not
        the lagna — §13.4.1 analyses "a house/arudha in a divisional chart",
        and §13.3 says a baadhaka is taken from any of them.
    :param graha_signs: graha id -> occupied sign, in that same chart.
    """
    index = validate.in_range("sign", sign, 0, 11)
    if not graha_signs:
        raise AnalysisError(
            "influences need the chart's graha positions; without them none "
            "of section 13.4.1's five kinds — rasi drishti, graha drishti, "
            "argala, the house classes, baadhaka — can be decided")
    for graha, place in graha_signs.items():
        validate.in_range(f"graha {graha} sign", int(place), 0, 11)

    positions = {int(g): int(s) for g, s in graha_signs.items()}
    found: list[Influence] = []

    # Rasi drishti — signs that aspect this one, and whoever sits in them.
    aspecting = set(rasi_drishti(index))
    for graha, place in sorted(positions.items()):
        if place in aspecting:
            found.append(Influence(
                "rasi drishti", graha, str(GRAHA_NAMES[graha]),
                "influences it",
                f"{RASI_NAMES[place]} casts rasi drishti on "
                f"{RASI_NAMES[index]}"))

    # Graha drishti — planets whose own aspects reach this sign.
    for graha, place in sorted(positions.items()):
        if graha_aspects_sign(graha, place, index):
            found.append(Influence(
                "graha drishti", graha, str(GRAHA_NAMES[graha]),
                "influences it",
                f"{GRAHA_NAMES[graha]} in {RASI_NAMES[place]} aspects "
                f"{RASI_NAMES[index]}"))

    # Argala — intervention on this sign, and the obstruction of it.
    for row in argalas_on_sign(index, occupants_from(positions),
                               ketu_sign=ketu_sign_of(positions)):
        for graha in row.grahas:
            found.append(Influence(
                row.kind, int(graha), str(GRAHA_NAMES[int(graha)]),
                "intervenes" if row.kind == "argala" else "obstructs",
                f"{row.house}th from {RASI_NAMES[index]} "
                f"({RASI_NAMES[row.sign]})"))

    # The four house classes, counted from this sign.
    frame = influence_frame(index)
    for name, entry in frame.items():
        for graha, place in sorted(positions.items()):
            if place in entry["signs"]:
                found.append(Influence(
                    name, graha, str(GRAHA_NAMES[graha]), entry["effect"],
                    f"{GRAHA_NAMES[graha]} is in a {name.rstrip('s')} from "
                    f"{RASI_NAMES[index]}"))

    # Baadhaka — §13.3, taken from this house rather than from lagna.
    trouble = baadhaka_of(index, positions)
    for graha in tuple(trouble.lords) + tuple(trouble.occupants):
        found.append(Influence(
            "baadhaka", int(graha), str(GRAHA_NAMES[int(graha)]),
            "creates troubles",
            f"the baadhaka sthaana of {RASI_NAMES[index]} is "
            f"{RASI_NAMES[trouble.sthaana]}"))

    return {
        "sign": index,
        "sign_name": str(RASI_NAMES[index]),
        "frame": frame,
        "baadhaka": {
            "sthaana": trouble.sthaana,
            "sthaana_name": str(RASI_NAMES[trouble.sthaana]),
            "lords": [str(GRAHA_NAMES[g]) for g in trouble.lords],
            "occupants": [str(GRAHA_NAMES[g]) for g in trouble.occupants],
        },
        "influences": [
            {"kind": i.kind, "graha": i.graha, "graha_name": i.graha_name,
             "effect": i.effect, "detail": i.detail}
            for i in found
        ],
        "by_graha": {
            str(GRAHA_NAMES[graha]): sorted(
                {i.kind for i in found if i.graha == graha})
            for graha in sorted(positions)
        },
        "untouched": [
            str(GRAHA_NAMES[graha]) for graha in sorted(positions)
            if not any(i.graha == graha for i in found)
        ],
    }
