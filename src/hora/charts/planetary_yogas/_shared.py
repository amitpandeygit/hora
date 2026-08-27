"""Detector shapes used by more than one group.

§11.2 and §11.3 are the same construction twice: houses counted from a
reference graha, with one other graha excluded by name. Vesi is "a planet
other than Moon in the 2nd from Sun"; Sunaphaa is "planets other than Sun in
the 2nd from Moon". Writing that twice would let the two drift, so it is
written once and parameterised.
"""
from __future__ import annotations

from hora.charts.planetary_yogas.registry import YogaInput, YogaVerdict
from hora.core.const import GRAHA_NAMES, RASI_NAMES

_ORDINAL = {1: "1st", 2: "2nd", 3: "3rd", 12: "12th"}


def ordinal(house: int) -> str:
    return _ORDINAL.get(house, f"{house}th")


def house_sign(reference_sign: int, house: int) -> int:
    """Inclusive: the 1st house from a sign is that sign."""
    return (reference_sign + house - 1) % 12


def qualifying(
    data: YogaInput, reference: int, reference_sign: int, house: int,
    excluded: int,
) -> tuple[int, ...]:
    """Grahas in a house from the reference that the definition admits.

    Two are always out: the graha the definition excludes by name, and the
    reference graha himself — a yoga about what *accompanies* a graha cannot
    be formed by that graha.
    """
    target = house_sign(reference_sign, house)
    out = {int(excluded), int(reference)}
    return tuple(
        g for g in data.considered()
        if int(g) not in out and data.sign_of(g) == target
    )


def make_house_detector(
    key: str, name: str, *, reference: int, excluded: int,
    houses: tuple[int, ...],
):
    """A detector for "planets other than X in the Nth house(s) from Y".

    All the named houses must be occupied — which is what makes Ubhayachara
    and Duradhara stricter than the single-house yogas beside them.
    """
    reference_name = GRAHA_NAMES[reference]

    def detect(data: YogaInput) -> YogaVerdict:
        reference_sign = data.sign_of(reference)
        if reference_sign is None:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"{reference_name} has no placement; this yoga is read "
                        f"from him"),
            )
        per_house = {
            house: qualifying(data, reference, reference_sign, house, excluded)
            for house in houses
        }
        found = {int(g): house for house, grahas in per_house.items()
                 for g in grahas}
        present = all(per_house[house] for house in houses)
        if present:
            named = ", ".join(GRAHA_NAMES[g] for g in sorted(found))
            where = " and ".join(
                f"the {ordinal(h)} from {reference_name} "
                f"({RASI_NAMES[house_sign(reference_sign, h)]})"
                for h in houses
            )
            reason = f"{named} in {where}"
        else:
            reason = "; ".join(
                f"the {ordinal(h)} from {reference_name} is "
                f"{RASI_NAMES[house_sign(reference_sign, h)]} and holds no "
                f"qualifying planet"
                for h in houses if not per_house[h]
            )
        return YogaVerdict(
            key=key, name=name, present=present, reason=reason,
            participants=tuple(sorted(found)) if present else (),
            houses=found if present else {},
        )

    return detect


def make_conjunction_detector(key: str, name: str, *, first: int, second: int):
    """A detector for "X and Y are together (in one sign)"."""

    def detect(data: YogaInput) -> YogaVerdict:
        a = data.sign_of(first)
        b = data.sign_of(second)
        for graha, sign in ((first, a), (second, b)):
            if sign is None:
                return YogaVerdict(
                    key=key, name=name, present=False,
                    reason=f"{GRAHA_NAMES[graha]} has no placement")
        assert a is not None and b is not None
        if a != b:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"{GRAHA_NAMES[first]} is in {RASI_NAMES[a]} and "
                        f"{GRAHA_NAMES[second]} in {RASI_NAMES[b]}; they are "
                        f"not together"),
            )
        return YogaVerdict(
            key=key, name=name, present=True,
            reason=(f"{GRAHA_NAMES[first]} and {GRAHA_NAMES[second]} are "
                    f"together in {RASI_NAMES[a]}"),
            participants=(int(first), int(second)),
            houses={int(first): 1, int(second): 1},
        )

    return detect
