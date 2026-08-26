"""Special lagna service — chapter 5, callable without a nativity.

A special lagna is a pure function of three numbers: the Sun's longitude at
sunrise, the minutes elapsed since, and a rate. The book's own worked examples
supply exactly those, so the calculation is exposed the same way — no birth
data, no ephemeris, no settings.

`/v1/chart/special-lagnas` remains the way to get them for an actual birth.
"""
from __future__ import annotations

from hora.charts.special_lagna import (
    ADVANCE_PER_MINUTE,
    SPECIAL_LAGNA_ABBR,
    SPECIAL_LAGNA_NAMES,
    SPECIAL_LAGNA_SIGNIFIES,
    SpecialLagna,
    SpecialLagnaError,
    advance_from_sunrise,
    ghati_lagna_birthtime_sensitivity,
    sree_lagna,
)

#: Re-exported so the HTTP layer never has to import an engine module;
#: `test_routers_do_not_import_calculation_modules` enforces that boundary.
__all__ = ["SpecialLagnaError", "compute", "resolve_longitude", "rules"]
from hora.core.const import RASI_NAMES
from hora.core.notation import NotationError, all_forms, parse
from hora.core.timeutil import format_dms

BY_ABBR = {abbr: SpecialLagna(i) for i, abbr in enumerate(SPECIAL_LAGNA_ABBR)}


def resolve_longitude(name: str, value: str | float) -> float:
    """Accept decimal degrees or either classical notation."""
    try:
        return float(value) % 360.0
    except (TypeError, ValueError):
        pass
    try:
        return parse(str(value)) % 360.0
    except NotationError as exc:
        raise SpecialLagnaError(f"{name}: {exc}") from exc


def _placement(lagna: SpecialLagna, longitude: float) -> dict:
    rasi = int(longitude // 30.0)
    return {
        "id": int(lagna),
        "name": SPECIAL_LAGNA_NAMES[lagna],
        "abbreviation": SPECIAL_LAGNA_ABBR[lagna],
        "longitude": round(longitude, 8),
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "degrees_in_rasi": round(longitude % 30.0, 8),
        "dms": format_dms(longitude % 30.0),
        "rasi_dm": all_forms(longitude)["rasi_dm"],
        "signifies": SPECIAL_LAGNA_SIGNIFIES[lagna],
        "degrees_per_minute": ADVANCE_PER_MINUTE.get(lagna),
    }


def compute(
    *,
    sun_at_sunrise: str | float | None,
    minutes_since_sunrise: float | None,
    moon: str | float | None,
    lagna: str | float | None,
    lagnas: list[str],
) -> dict:
    """The requested special lagnas from the book's own inputs.

    Bhaava, Hora and Ghati need ``sun_at_sunrise`` and ``minutes_since_sunrise``;
    Sree needs ``moon`` and ``lagna``. Asking for one without its inputs is an
    error rather than a silent omission.
    """
    wanted = []
    for raw in lagnas:
        key = raw.upper()
        if key not in BY_ABBR:
            raise SpecialLagnaError(
                f"unknown special lagna {raw!r}; expected one of "
                f"{', '.join(SPECIAL_LAGNA_ABBR)}"
            )
        wanted.append(BY_ABBR[key])

    time_based = [x for x in wanted if x in ADVANCE_PER_MINUTE]
    if time_based and (sun_at_sunrise is None or minutes_since_sunrise is None):
        names = ", ".join(SPECIAL_LAGNA_ABBR[x] for x in time_based)
        raise SpecialLagnaError(
            f"{names} need both sun_at_sunrise and minutes_since_sunrise"
        )
    if SpecialLagna.SREE in wanted and (moon is None or lagna is None):
        raise SpecialLagnaError("SL needs both moon and lagna")

    echo: dict = {}
    sun_deg = elapsed = None
    if time_based:
        sun_deg = resolve_longitude("sun_at_sunrise", sun_at_sunrise)  # type: ignore[arg-type]
        elapsed = float(minutes_since_sunrise)  # type: ignore[arg-type]
        echo["sun_at_sunrise"] = all_forms(sun_deg)
        echo["minutes_since_sunrise"] = elapsed
    if SpecialLagna.SREE in wanted:
        echo["moon"] = all_forms(resolve_longitude("moon", moon))  # type: ignore[arg-type]
        echo["lagna"] = all_forms(resolve_longitude("lagna", lagna))  # type: ignore[arg-type]

    out = []
    for item in wanted:
        if item is SpecialLagna.SREE:
            longitude = sree_lagna(
                resolve_longitude("moon", moon),        # type: ignore[arg-type]
                resolve_longitude("lagna", lagna),      # type: ignore[arg-type]
            )
        else:
            longitude = advance_from_sunrise(
                sun_deg, elapsed, ADVANCE_PER_MINUTE[item]  # type: ignore[arg-type]
            )
        out.append(_placement(item, longitude))
    return {"input": echo, "special_lagnas": out}


def rules() -> dict:
    """Each special lagna, its rate and what it shows."""
    return {
        "lagnas": [
            {
                "id": int(x),
                "name": SPECIAL_LAGNA_NAMES[x],
                "abbreviation": SPECIAL_LAGNA_ABBR[x],
                "degrees_per_minute": ADVANCE_PER_MINUTE.get(x),
                "one_rasi_per_minutes": (
                    round(30.0 / ADVANCE_PER_MINUTE[x], 6)
                    if x in ADVANCE_PER_MINUTE else None
                ),
                "signifies": SPECIAL_LAGNA_SIGNIFIES[x],
                "derived_from": (
                    "the Moon's progress through its nakshatra, applied to the lagna"
                    if x is SpecialLagna.SREE
                    else "the Sun's longitude at sunrise, advanced by elapsed time"
                ),
            }
            for x in SpecialLagna
        ],
        "birthtime_sensitivity_per_minute": {
            SPECIAL_LAGNA_ABBR[x]: ADVANCE_PER_MINUTE[x] for x in ADVANCE_PER_MINUTE
        },
        "note": (
            "Ghati Lagna moves "
            f"{ghati_lagna_birthtime_sensitivity(1.0)} degrees for every minute of "
            "birthtime error (section 5.5), the most birthtime-sensitive point in "
            "the chart. Bhaava Lagna's rate follows the book's stated rate, not "
            "its numbered method — see docs/book-deviations.md D-11."
        ),
    }
