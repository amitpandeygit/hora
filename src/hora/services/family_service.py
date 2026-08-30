"""Section 13.4.2 — family members, service layer."""
from __future__ import annotations

from hora.charts.family import (
    CHART_FOR,
    HOUSE_FOR,
    FamilyError,
    child,
    named,
    relative,
    sibling,
)
from hora.core.const import (
    CHILDREN_RULE,
    DIRECTION_EXAMPLES,
    DIRECTION_RULE,
    DIRECTION_SCOPE,
    FAMILY_CHAIN_DEPTH,
    FAMILY_CHARTS,
    FAMILY_INTRO,
    FAMILY_METHOD,
    FAMILY_NOTE,
    FAMILY_NOTE_IS_UNDERSPECIFIED,
    GRAHA_NAMES,
    NESTED_HOUSE_CLAIMS,
    RASI_NAMES,
    SIBLINGS_RULE,
)
from hora.core.validate import InputError


def _relative(result) -> dict:
    return {
        "relation": result.relation,
        "index": result.index or None,
        "chart": result.chart,
        "house": result.house,
        "direction": result.direction,
        "house_sign": result.house_sign,
        "house_sign_name": str(RASI_NAMES[result.house_sign]),
        "lagna": result.lagna,
        "lagna_name": (None if result.lagna is None
                       else str(RASI_NAMES[result.lagna])),
        "lord": str(GRAHA_NAMES[result.lord]),
        "lords": [str(GRAHA_NAMES[g]) for g in result.lords],
        "lagna_candidates": (
            None if result.lagna_candidates is None else
            {str(GRAHA_NAMES[g]): str(RASI_NAMES[s])
             for g, s in result.lagna_candidates.items()}),
        "arudha": result.arudha,
        "arudha_sign": result.arudha_sign,
        "arudha_sign_name": (None if result.arudha_sign is None
                             else str(RASI_NAMES[result.arudha_sign])),
        "why": result.why,
    }


def parent(relation: str, lagna: int,
           graha_signs: dict[int, int] | None = None,
           stronger_lord: dict[int, int] | None = None) -> dict:
    return _relative(named(relation, lagna, graha_signs, stronger_lord))


def siblings(lagna: int, elder: bool, depth: int = FAMILY_CHAIN_DEPTH,
             graha_signs: dict[int, int] | None = None,
             stronger_lord: dict[int, int] | None = None) -> dict:
    return {
        "chart": "D3",
        "elder": elder,
        "lagna": lagna,
        "lagna_name": str(RASI_NAMES[lagna]),
        "siblings": [
            _relative(sibling(n, lagna, elder=elder,
                              graha_signs=graha_signs,
                              stronger_lord=stronger_lord))
            for n in range(1, min(depth, FAMILY_CHAIN_DEPTH) + 1)
        ],
        "depth_limit": FAMILY_CHAIN_DEPTH,
        "beyond_the_limit": FAMILY_NOTE_IS_UNDERSPECIFIED,
    }


def children(lagna: int, depth: int = FAMILY_CHAIN_DEPTH,
             graha_signs: dict[int, int] | None = None,
             stronger_lord: dict[int, int] | None = None) -> dict:
    return {
        "chart": "D7",
        "lagna": lagna,
        "lagna_name": str(RASI_NAMES[lagna]),
        "children": [
            _relative(child(n, lagna, graha_signs, stronger_lord))
            for n in range(1, min(depth, FAMILY_CHAIN_DEPTH) + 1)
        ],
        "depth_limit": FAMILY_CHAIN_DEPTH,
        "beyond_the_limit": FAMILY_NOTE_IS_UNDERSPECIFIED,
    }


def any_relative(relation: str, chart: str, house: int, lagna: int,
                 graha_signs: dict[int, int] | None = None,
                 stronger_lord: dict[int, int] | None = None,
                 directional: bool = False) -> dict:
    return _relative(relative(relation, chart, house, lagna, graha_signs,
                              stronger_lord, directional))


def rules() -> dict:
    """Section 13.4.2's charts, its method and its two worked examples."""
    return {
        "intro": FAMILY_INTRO,
        "charts": [{"chart": chart, "relations": list(relations)}
                   for chart, relations in FAMILY_CHARTS],
        "chart_for": dict(CHART_FOR),
        "method": FAMILY_METHOD,
        "named_relatives": [
            {"relation": name, "chart": chart, "house": house,
             "arudha": f"A{house}"}
            for name, (chart, house) in sorted(HOUSE_FOR.items())
        ],
        "siblings_rule": SIBLINGS_RULE,
        "children_rule": CHILDREN_RULE,
        "nested_house_claims": [
            {"from_house": inner, "then": step, "gives": result}
            for inner, step, result in NESTED_HOUSE_CLAIMS
        ],
        "direction_rule": DIRECTION_RULE,
        "direction_scope": DIRECTION_SCOPE,
        "direction_examples": [
            {"lagna": lagna, "direction": direction,
             "children": [{"sign": sign, "lord": lord}
                          for sign, lord in kids]}
            for lagna, direction, kids in DIRECTION_EXAMPLES
        ],
        "note": FAMILY_NOTE,
        "note_is_underspecified": FAMILY_NOTE_IS_UNDERSPECIFIED,
        "chain_depth": FAMILY_CHAIN_DEPTH,
    }


__all__ = ["FamilyError", "InputError", "any_relative", "children", "parent",
           "rules", "siblings"]
