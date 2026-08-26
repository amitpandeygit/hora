"""Solar and lunar calendars (book sections 1.3.7 and 1.3.8.2).

The lunar month is bounded by Sun-Moon conjunctions. Two reckonings are in
use and they disagree for half of every month, so both are computed and
returned; nothing here picks one.

* **Amanta** — the month runs from one Amavasya to the next (South Indian).
  This is the convention Chapter 1 describes.
* **Purnimanta** — the month runs from one Purnima to the next (North Indian).
  Its sukla paksha coincides with amanta's; its krishna paksha belongs to the
  *previous* amanta month, so the purnimanta name runs one ahead there.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core.const import (
    MASA_FROM_CONJUNCTION_RASI,
    RASI_NAMES,
    Graha,
)
from hora.core.ephemeris import get_ephemeris
from hora.core.names import NameScheme, name
from hora.core.settings import Settings
from hora.core.timeutil import norm360
from hora.panchanga.solver import scan_for_crossing

#: A synodic month is ~29.53 days; these bracket a search comfortably.
_SYNODIC = 29.530588853


@dataclass(frozen=True, slots=True)
class SolarDate:
    """Book 1.3.7: a solar month is 30 degrees of Sun, a solar day is 1 degree."""

    month: int              # 0 = Aries, the rasi the Sun occupies
    month_name: str
    day: int                # 1..30
    sun_longitude: float


@dataclass(frozen=True, slots=True)
class LunarMonth:
    """One lunar month under one reckoning."""

    reckoning: str
    index: int              # 0..11 into the masa name table
    name: str
    paksha: int             # 0 = sukla, 1 = krishna
    paksha_name: str
    is_adhika: bool
    start_jd: float
    end_jd: float
    conjunction_rasi: int
    conjunction_rasi_name: str


def solar_date(jd_ut: float, settings: Settings) -> SolarDate:
    """Solar month and day for an instant."""
    eph = get_ephemeris(settings)
    sun = eph.positions(jd_ut, (Graha.SUN,))[Graha.SUN]
    return SolarDate(
        month=sun.rasi,
        month_name=RASI_NAMES[sun.rasi],
        day=int(sun.degrees_in_rasi) + 1,
        sun_longitude=sun.longitude,
    )


def _elongation_fn(settings: Settings):
    eph = get_ephemeris(settings)

    def f(jd: float) -> float:
        p = eph.positions(jd, (Graha.SUN, Graha.MOON))
        return norm360(p[Graha.MOON].longitude - p[Graha.SUN].longitude)

    return f


def new_moon_before(jd_ut: float, settings: Settings) -> float:
    """Julian Day of the last Sun-Moon conjunction at or before ``jd_ut``."""
    f = _elongation_fn(settings)
    found = scan_for_crossing(f, 0.0, jd_ut - _SYNODIC - 2.0, jd_ut + 0.01, step=0.25)
    if found is None:  # pragma: no cover - only if the search window is wrong
        raise ValueError("no conjunction found before the given instant")
    later = scan_for_crossing(f, 0.0, found + 1.0, jd_ut + 0.01, step=0.25)
    return later if later is not None else found


def new_moon_after(jd_ut: float, settings: Settings) -> float:
    """Julian Day of the next Sun-Moon conjunction strictly after ``jd_ut``."""
    f = _elongation_fn(settings)
    found = scan_for_crossing(f, 0.0, jd_ut + 0.01, jd_ut + _SYNODIC + 2.0, step=0.25)
    if found is None:  # pragma: no cover
        raise ValueError("no conjunction found after the given instant")
    return found


def _rasi_at(jd: float, settings: Settings) -> int:
    eph = get_ephemeris(settings)
    return eph.positions(jd, (Graha.SUN,))[Graha.SUN].rasi


def _has_sankranti(start_jd: float, end_jd: float, settings: Settings) -> bool:
    """Whether the Sun enters a new rasi between two conjunctions.

    A lunar month containing no sankranti is adhika (intercalary). This is the
    classical test and it is equivalent to Chapter 1's observation that the two
    conjunctions then fall in the same rasi.
    """
    return _rasi_at(start_jd, settings) != _rasi_at(end_jd - 1e-6, settings)


def lunar_months(jd_ut: float, settings: Settings) -> dict[str, LunarMonth]:
    """Both reckonings of the lunar month containing ``jd_ut``."""
    scheme = settings.name_scheme
    start = new_moon_before(jd_ut, settings)
    end = new_moon_after(jd_ut, settings)

    conj_rasi = _rasi_at(start, settings)
    amanta_index = MASA_FROM_CONJUNCTION_RASI[conj_rasi]
    adhika = not _has_sankranti(start, end, settings)

    # Paksha: the Moon is ahead of the Sun by 0-180 in sukla, 180-360 in krishna.
    f = _elongation_fn(settings)
    paksha = 0 if f(jd_ut) < 180.0 else 1

    amanta = LunarMonth(
        reckoning="amanta",
        index=amanta_index,
        name=name("masa", amanta_index, scheme),
        paksha=paksha,
        paksha_name=name("paksha", paksha, scheme),
        is_adhika=adhika,
        start_jd=start,
        end_jd=end,
        conjunction_rasi=conj_rasi,
        conjunction_rasi_name=RASI_NAMES[conj_rasi],
    )

    # Purnimanta shares sukla paksha with amanta; in krishna paksha it has
    # already rolled over to the next month's name.
    p_index = amanta_index if paksha == 0 else (amanta_index + 1) % 12
    purnimanta = LunarMonth(
        reckoning="purnimanta",
        index=p_index,
        name=name("masa", p_index, scheme),
        paksha=paksha,
        paksha_name=name("paksha", paksha, scheme),
        is_adhika=adhika,
        start_jd=start,
        end_jd=end,
        conjunction_rasi=conj_rasi,
        conjunction_rasi_name=RASI_NAMES[conj_rasi],
    )
    return {"amanta": amanta, "purnimanta": purnimanta}


__all__ = [
    "LunarMonth", "NameScheme", "SolarDate",
    "lunar_months", "new_moon_after", "new_moon_before", "solar_date",
]
