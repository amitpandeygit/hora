"""Ephemeris abstraction.

Everything above this layer talks only to :class:`EphemerisProvider`.  The
Swiss Ephemeris backend is the one that reproduces Jagannatha Hora exactly,
but it is AGPL/commercial-dual-licensed, so the seam exists to let a
permissively-licensed backend (JPL DE440 via Skyfield) be dropped in without
touching the astrology code.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class PlanetPosition:
    """A graha's state at one instant, in the sidereal zodiac."""

    graha: int
    longitude: float          # sidereal ecliptic longitude, degrees [0, 360)
    latitude: float           # ecliptic latitude, degrees
    distance: float           # AU
    speed_longitude: float    # degrees/day; negative means retrograde
    speed_latitude: float
    speed_distance: float

    @property
    def is_retrograde(self) -> bool:
        return self.speed_longitude < 0.0

    @property
    def rasi(self) -> int:
        """Sign index, 0 = Aries."""
        return int(self.longitude // 30.0)

    @property
    def degrees_in_rasi(self) -> float:
        return self.longitude % 30.0


@dataclass(frozen=True, slots=True)
class Houses:
    """Ascendant, MC and the twelve bhava cusps in sidereal longitude."""

    ascendant: float
    midheaven: float
    cusps: tuple[float, ...]   # 12 entries, cusp of bhava 1..12
    armc: float
    vertex: float
    equatorial_ascendant: float


@runtime_checkable
class EphemerisProvider(Protocol):
    """The minimal surface the astrology layer needs from an ephemeris."""

    def ayanamsa(self, jd_ut: float) -> float:
        """Ayanamsa in degrees for the configured mode."""

    def position(self, jd_ut: float, graha: int) -> PlanetPosition:
        """Sidereal position of one graha."""

    def positions(self, jd_ut: float, grahas: tuple[int, ...]) -> dict[int, PlanetPosition]:
        """Sidereal positions of several grahas at one instant."""

    def houses(self, jd_ut: float, latitude: float, longitude: float) -> Houses:
        """Sidereal ascendant and bhava cusps."""

    def sunrise(self, jd_ut: float, latitude: float, longitude: float, altitude: float) -> float | None:
        """Julian Day of the next sunrise at or after ``jd_ut``."""

    def sunset(self, jd_ut: float, latitude: float, longitude: float, altitude: float) -> float | None:
        """Julian Day of the next sunset at or after ``jd_ut``."""
