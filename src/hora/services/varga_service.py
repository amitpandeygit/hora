"""Divisional chart service.

Exposes the varga rules as a computation in their own right, independent of a
birth chart: give it a longitude and it returns where that longitude falls in
any divisional chart, together with the rule that put it there.

That separation matters because a varga is a pure function of a longitude. Being
able to call it directly is what makes the chapter 6 rules testable and
auditable without an ephemeris in the way.
"""
from __future__ import annotations

from hora.charts.vargas import (
    AMSA_NAMES,
    VARGA_GROUPS,
    VARGA_REGISTRY,
    VARGA_RULES,
    VARGA_SIGNIFICATIONS,
    charts_for_matter,
    part_index,
    part_size_degrees,
    varga,
)
from hora.core import const as c
from hora.core import validate
from hora.core.const import RASI_NAMES
from hora.core.notation import NotationError, all_forms, parse
from hora.core.timeutil import format_dms

#: Re-exported so routers catch the service's error, not the engine's.
InputError = validate.InputError

class UnknownVarga(ValueError):
    """Raised when a varga code is neither registered nor a valid D<N>."""


def _divisions(code: str) -> int:
    entry = VARGA_REGISTRY.get(code)
    if entry is not None:
        return entry[2]
    if code.startswith("D") and code[1:].isdigit():
        return int(code[1:])
    raise UnknownVarga(f"unknown varga {code!r}")


def resolve_longitude(value: str | float) -> float:
    """Accept decimal degrees or either classical notation."""
    if isinstance(value, int | float):
        return float(value) % 360.0
    try:
        return float(value) % 360.0
    except ValueError:
        try:
            return parse(value) % 360.0
        except NotationError as exc:
            raise UnknownVarga(str(exc)) from exc


def _input_echo(longitude: float) -> dict:
    """The longitude as given, in every notation, plus its rasi."""
    rasi = int(longitude // 30.0)
    return {
        **all_forms(longitude),
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "degrees_in_rasi": round(longitude % 30.0, 8),
    }


def compute(longitude: float, codes: list[str], variants: dict[str, str]) -> dict:
    """Where a longitude falls in each requested divisional chart."""
    out = []
    for raw in codes:
        code = raw.upper()
        divisions = _divisions(code)
        try:
            position = varga(longitude, code, variants.get(code))
        except ValueError as exc:
            raise UnknownVarga(str(exc)) from exc
        rule = VARGA_RULES.get(code, {})
        out.append({
            "chart": code,
            "name": VARGA_REGISTRY[code][1] if code in VARGA_REGISTRY else f"D-{divisions}",
            "divisions": divisions,
            "part_size_degrees": round(part_size_degrees(divisions), 10),
            "part_index": part_index(longitude, divisions),
            "rasi": position.sign,
            "rasi_name": RASI_NAMES[position.sign],
            "varga_longitude": round(position.longitude, 8),
            "degrees_in_rasi": round(position.longitude % 30.0, 8),
            "dms": format_dms(position.longitude % 30.0),
            "counts_from": rule.get("counts_from"),
            "variant": variants.get(code),
        })
    return {"input": _input_echo(longitude), "charts": out}


def for_matter(matter: str) -> dict:
    """§6.5 — which chart to analyse for a matter, and how.

    Table 11 is published chart-first; §6.5 uses it matter-first. The index is
    built from Table 11's own wording, so a matter the book does not name
    returns nothing rather than a guess.
    """
    codes = charts_for_matter(matter)
    return {
        "matter": matter,
        "charts": [
            {
                "chart": code,
                "name": VARGA_REGISTRY[code][1],
                "divisions": VARGA_REGISTRY[code][2],
                "signifies": VARGA_SIGNIFICATIONS[code],
                "cautioned": code in c.HIGHER_CHARTS_CAUTIONED,
            }
            for code in codes
        ],
        "method": c.FIND_LINKS_METHOD,
        "no_match_note": (
            "The index is built from Table 11's own wording. A matter the book "
            "does not name returns no charts rather than a guess."
        ),
    }


def rules() -> dict:
    """Every named divisional chart, its rule and its aliases."""
    return {
        "choose_by_matter": c.CHOOSE_CHART_BY_MATTER,
        "method": c.FIND_LINKS_METHOD,
        "key_to_analysis": c.KEY_TO_CHART_ANALYSIS,
        "analysis_patterns": [dict(p) for p in c.MATTER_ANALYSIS_PATTERNS],
        "planes": [dict(p) for p in c.VARGA_PLANES],
        "higher_charts_caution": {
            "note": c.HIGHER_CHARTS_CAUTION,
            "charts": list(c.HIGHER_CHARTS_CAUTIONED),
        },
        "charts": [
            {
                "chart": code,
                "name": entry[1],
                "divisions": entry[2],
                "part_size_degrees": round(part_size_degrees(entry[2]), 10),
                "aliases": VARGA_RULES.get(code, {}).get("aliases", []),
                "counts_from": VARGA_RULES.get(code, {}).get("counts_from"),
                "worked_example_in_book": VARGA_RULES.get(code, {}).get("example", False),
                "signifies": VARGA_SIGNIFICATIONS.get(code),
            }
            for code, entry in VARGA_REGISTRY.items()
        ],
        "groups": {name: list(codes) for name, codes in VARGA_GROUPS.items()},
        "amsa_names": {g: {str(k): v for k, v in names.items()}
                       for g, names in AMSA_NAMES.items()},
        "generic": "Any D<N> for N in 1..300 falls back to the cyclic rule.",
        "note": (
            "Charts with no worked example in the book are the ones a "
            "transcription error can hide in: D-5's rule was wrong until "
            "chapter 6 was audited, and it has no example to catch it."
        ),
    }


def amsabala(longitude: float, graha: int) -> dict:
    """Vaiseshikamsa — §6.6.

    "In each group of divisional charts, we can count the divisional charts in
    which a planet occupies its moolatrikona or an own rasi or its rasi of
    exaltation. Based on the count of such good divisional charts for the
    planet, we say that the planet is in a particular amsa."

    The named amsas start at a count of two; below that the book names nothing,
    and nothing is invented.
    """
    from hora.charts.dignity import sign_dignity
    from hora.charts.vargas import AMSA_NAMES, VARGA_GROUPS
    from hora.core.const import GRAHA_NAMES

    GOOD = {"moolatrikona", "own", "exalted"}
    out = {}
    for group, codes in VARGA_GROUPS.items():
        strong = []
        for code in codes:
            position = varga(longitude, code)
            dignity = sign_dignity(graha, position.longitude)
            if dignity in GOOD:
                strong.append({"chart": code, "rasi_name": RASI_NAMES[position.sign],
                               "dignity": dignity})
        count = len(strong)
        out[group] = {
            "charts_in_group": len(codes),
            "strong_in": strong,
            "count": count,
            "amsa": AMSA_NAMES[group].get(count),
        }
    return {
        "graha": graha,
        "graha_name": GRAHA_NAMES[graha],
        "input": _input_echo(longitude),
        "groups": out,
    }
