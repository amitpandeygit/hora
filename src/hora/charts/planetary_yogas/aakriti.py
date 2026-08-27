"""§11.5.3 Aakriti yogas — twenty shapes.

"Aakriti means a shape and the many of these yogas are based on the shape of
the arrangement of planets in a chart."

**One rule decides eighteen of the twenty**, and it comes from the book's own
grammar. Where a definition's subject is "all the planets" — "If all the
planets occupy 1st and 7th houses" — the test is *confinement*: every planet
lies in the named houses. Where the subject is a house — "lagna and the 7th
houses **are occupied by** natural benefics" — that house must actually hold
something. Only Vajra and Yava take the second form, and only they need
natures.

Confinement is asked of a *set of alternatives*: Gadaa's four successive
quadrant pairs, Hala's three non-lagna trine sets, Vaapi's two, Ardha
Chandra's eight starting points. A yoga naming one list has one alternative,
so the same code serves all eighteen.

Like every yoga counting from lagna, these need one, and say so when they lack
it. And like the Aasraya yogas, "all the planets" is universal — a partial
chart cannot decide it.
"""
from __future__ import annotations

from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import AAKRITI_YOGAS, GRAHA_NAMES, RASI_NAMES

_SPEC = {entry["key"]: entry for entry in AAKRITI_YOGAS}


def _houses_of(data: YogaInput, grahas) -> dict[int, int]:
    """Each graha's house from lagna. `lagna_rasi` must not be None."""
    assert data.lagna_rasi is not None
    return {int(g): (data.rasis[g] - data.lagna_rasi) % 12 + 1 for g in grahas}


def _incomplete(data: YogaInput) -> tuple[int, ...]:
    return tuple(g for g in data.considered() if data.sign_of(g) is None)


def _make_confinement_detector(key: str):
    spec = _SPEC[key]
    name = spec["name"]
    alternatives = spec["alternatives"]

    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=("no lagna was supplied, and this yoga counts houses "
                        "from lagna; it cannot be decided"),
            )
        missing = _incomplete(data)
        if missing:
            named = ", ".join(GRAHA_NAMES[g] for g in missing)
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"this yoga needs every planet placed and {named} "
                        f"{'is' if len(missing) == 1 else 'are'} missing; it "
                        f"cannot be decided"),
            )

        placed = data.considered()
        houses = _houses_of(data, placed)
        for alternative in alternatives:
            allowed = set(alternative)
            if all(house in allowed for house in houses.values()):
                occupied = sorted({h for h in houses.values()})
                where = ", ".join(f"the {ordinal(h)}" for h in alternative)
                return YogaVerdict(
                    key=key, name=name, present=True,
                    reason=(f"all {len(placed)} planets lie in {where}; "
                            f"occupied: {', '.join(ordinal(h) for h in occupied)}"),
                    participants=tuple(sorted(houses)),
                    houses=houses,
                )

        outside = sorted({h for h in houses.values()})
        return YogaVerdict(
            key=key, name=name, present=False,
            reason=(f"the planets span {', '.join(ordinal(h) for h in outside)}, "
                    f"which no permitted set contains"),
        )

    return detect


def _make_nature_detector(key: str):
    """Vajra and Yava: two houses by benefics and two by malefics.

    The only two definitions in §11.5.3 whose subject is a house, so the only
    two where a house must actually be occupied.
    """
    spec = _SPEC[key]
    name = spec["name"]
    wanted = {
        **{h: "benefic" for h in spec["benefic_houses"]},
        **{h: "malefic" for h in spec["malefic_houses"]},
    }

    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=("no lagna was supplied, and this yoga counts houses "
                        "from lagna; it cannot be decided"),
            )
        benefics, undecidable = data.benefics()
        benefic_set = {int(g) for g in benefics}

        found: dict[int, int] = {}
        problems: list[str] = []
        for house, nature in sorted(wanted.items()):
            sign = house_sign(data.lagna_rasi, house)
            grahas = [int(g) for g in sorted(data.rasis) if data.rasis[g] == sign]
            if not grahas:
                problems.append(
                    f"the {ordinal(house)} ({RASI_NAMES[sign]}) is empty")
                continue
            wrong = [g for g in grahas
                     if (g in benefic_set) is not (nature == "benefic")]
            if wrong:
                named = ", ".join(GRAHA_NAMES[g] for g in wrong)
                problems.append(
                    f"{named} in the {ordinal(house)} is not a natural {nature}")
                continue
            for graha in grahas:
                found[graha] = house

        if problems:
            return YogaVerdict(key=key, name=name, present=False,
                               reason="; ".join(problems))

        qualifiers: tuple[str, ...] = ()
        if undecidable:
            named = ", ".join(GRAHA_NAMES[g] for g in undecidable)
            qualifiers = (
                f"the nature of {named} could not be judged from the input",
            )
        return YogaVerdict(
            key=key, name=name, present=True,
            reason=(f"the {', '.join(ordinal(h) for h in spec['benefic_houses'])} "
                    f"hold natural benefics and the "
                    f"{', '.join(ordinal(h) for h in spec['malefic_houses'])} "
                    f"hold natural malefics"),
            participants=tuple(sorted(found)), houses=found,
            qualifiers=qualifiers,
        )

    return detect


for _key, _entry in _SPEC.items():
    _detector = (_make_nature_detector if "benefic_houses" in _entry
                 else _make_confinement_detector)
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=tuple(_entry.get("aliases", ())),
        section="11.5.3",
        group="naabhasa_aakriti",
        definition=_entry["definition"],
        detect=_detector(_key),
    ))
