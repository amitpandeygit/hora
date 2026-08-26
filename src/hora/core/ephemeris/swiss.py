"""Swiss Ephemeris backend.

Jagannatha Hora is itself built on Swiss Ephemeris, so this backend is what
makes bit-level parity achievable.  Mode switches (sidereal mode, node type,
topocentric flag) are derived from :class:`~hora.core.settings.Settings`.

Licensing note: Swiss Ephemeris is dual-licensed AGPL / commercial.  Running
it behind a public API triggers one of the two; see docs/licensing.md.
"""
from __future__ import annotations

import os
import threading
from functools import lru_cache
from pathlib import Path

import swisseph as swe

from hora.core.const import Graha
from hora.core.ephemeris.base import Houses, PlanetPosition
from hora.core.settings import (
    AYANAMSA_SWE_NAME,
    Ayanamsa,
    HouseSystem,
    KetuMode,
    NodeDirection,
    NodeType,
    Settings,
    SunriseMode,
)

#: swisseph keeps global state, so every call that touches mode must hold this.
_SWE_LOCK = threading.RLock()

_EPHE_DIR = Path(os.environ.get("HORA_EPHE_PATH", Path(__file__).resolve().parents[4] / "data" / "ephe"))

_SWE_BODY: dict[int, int] = {
    Graha.SUN: swe.SUN,
    Graha.MOON: swe.MOON,
    Graha.MARS: swe.MARS,
    Graha.MERCURY: swe.MERCURY,
    Graha.JUPITER: swe.JUPITER,
    Graha.VENUS: swe.VENUS,
    Graha.SATURN: swe.SATURN,
    Graha.URANUS: swe.URANUS,
    Graha.NEPTUNE: swe.NEPTUNE,
    Graha.PLUTO: swe.PLUTO,
}

_HOUSE_CODE = {
    HouseSystem.EQUAL_LAGNA: b"A",
    HouseSystem.WHOLE_SIGN: b"W",
    HouseSystem.SRIPATI: b"O",       # Sripati is Porphyry cusps re-centred; see bhava.py
    HouseSystem.KP_PLACIDUS: b"P",
    HouseSystem.PLACIDUS: b"P",
    HouseSystem.KOCH: b"K",
    HouseSystem.PORPHYRY: b"O",
    HouseSystem.REGIOMONTANUS: b"R",
    HouseSystem.CAMPANUS: b"C",
    HouseSystem.VEHLOW_EQUAL: b"V",
    HouseSystem.AXIAL_ROTATION: b"X",
    HouseSystem.HORIZONTAL: b"H",
    HouseSystem.TOPOCENTRIC: b"T",
    HouseSystem.ALCABITUS: b"B",
    HouseSystem.MORINUS: b"M",
    HouseSystem.KN_RAO: b"W",        # KN Rao and PVR bhavas are post-processed
    HouseSystem.PVR: b"W",
}

#: swe.rise_trans flag bits for each sunrise definition.
#: BIT_HINDU_RISING is 896 = BIT_DISC_CENTER | BIT_NO_REFRACTION | 128, the
#: last bit disregarding the body's ecliptic latitude. That final bit is what
#: separates it from GEOMETRIC_CENTER, and it matters most for the Moon —
#: moonrise moves by several minutes.
_RISE_FLAGS = {
    SunriseMode.TRADITIONAL_HINDU: swe.BIT_HINDU_RISING,
    SunriseMode.DISC_CENTER: swe.BIT_DISC_CENTER,
    SunriseMode.DISC_UPPER_LIMB: 0,
    SunriseMode.GEOMETRIC_CENTER: swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION,
}


def _ephemeris_flag() -> int:
    """Prefer the Swiss Ephemeris data files; fall back to Moshier if absent.

    JHora ships the ``sepl``/``semo`` files, so parity work should install them
    too — ``scripts/fetch_ephemeris.sh`` does that.  Moshier stays as a
    zero-download default that is still sub-arcsecond for the classical seven.
    """
    if _EPHE_DIR.is_dir() and any(_EPHE_DIR.glob("sepl*.se1")):
        swe.set_ephe_path(str(_EPHE_DIR))
        return swe.FLG_SWIEPH
    return swe.FLG_MOSEPH


class SwissEphemeris:
    """Settings-bound view over the Swiss Ephemeris library."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._base_flag = _ephemeris_flag()
        self._topo: tuple[float, float, float] | None = None

    # -- mode management ---------------------------------------------------

    def _apply_mode(self) -> None:
        """Push this instance's sidereal mode into swisseph's global state.

        Must be called under ``_SWE_LOCK`` by every public method.
        """
        s = self.settings
        if s.ayanamsa is Ayanamsa.TROPICAL:
            return
        if s.ayanamsa is Ayanamsa.CUSTOM:
            swe.set_sid_mode(swe.SIDM_USER, 2451545.0, s.custom_ayanamsa_deg or 0.0)
            return
        swe.set_sid_mode(getattr(swe, AYANAMSA_SWE_NAME[s.ayanamsa]), 0, 0)

    def _calc_flags(self) -> int:
        s = self.settings
        flag = self._base_flag | swe.FLG_SPEED
        if s.ayanamsa is not Ayanamsa.TROPICAL:
            flag |= swe.FLG_SIDEREAL
        if not s.apparent_positions:
            flag |= swe.FLG_TRUEPOS | swe.FLG_NOABERR | swe.FLG_NOGDEFL
        if s.topocentric:
            flag |= swe.FLG_TOPOCTR
        return flag

    def set_observer(self, latitude: float, longitude: float, altitude: float = 0.0) -> None:
        """Record the observer position used for topocentric positions."""
        self._topo = (longitude, latitude, altitude)

    # -- core queries ------------------------------------------------------

    def ayanamsa(self, jd_ut: float) -> float:
        if self.settings.ayanamsa is Ayanamsa.TROPICAL:
            return 0.0
        with _SWE_LOCK:
            self._apply_mode()
            return swe.get_ayanamsa_ut(jd_ut)

    def position(self, jd_ut: float, graha: int) -> PlanetPosition:
        return self.positions(jd_ut, (graha,))[graha]

    def positions(self, jd_ut: float, grahas: tuple[int, ...]) -> dict[int, PlanetPosition]:
        out: dict[int, PlanetPosition] = {}
        with _SWE_LOCK:
            self._apply_mode()
            if self.settings.topocentric and self._topo is not None:
                swe.set_topo(*self._topo)
            flags = self._calc_flags()

            node_needed = Graha.RAHU in grahas or Graha.KETU in grahas
            rahu: PlanetPosition | None = None
            ketu_true: PlanetPosition | None = None
            if node_needed:
                rahu, ketu_true = self._nodes(jd_ut, flags)

            for g in grahas:
                if g == Graha.RAHU:
                    out[g] = rahu  # type: ignore[assignment]
                elif g == Graha.KETU:
                    out[g] = self._ketu(rahu, ketu_true)  # type: ignore[arg-type]
                else:
                    body = _SWE_BODY[g]
                    vals, _ = swe.calc_ut(jd_ut, body, flags)
                    out[g] = PlanetPosition(
                        graha=int(g),
                        longitude=vals[0] % 360.0,
                        latitude=vals[1],
                        distance=vals[2],
                        speed_longitude=vals[3],
                        speed_latitude=vals[4],
                        speed_distance=vals[5],
                    )
        return out

    def _nodes(self, jd_ut: float, flags: int) -> tuple[PlanetPosition, PlanetPosition]:
        """Compute Rahu (north node) and the true south node.

        The nodes are conventionally reported as retrograde; swisseph gives the
        mean node a genuinely negative speed but the true node oscillates, so
        the reported direction is forced by ``settings.node_direction``.
        """
        body = swe.TRUE_NODE if self.settings.node_type is NodeType.TRUE else swe.MEAN_NODE
        vals, _ = swe.calc_ut(jd_ut, body, flags)
        speed = vals[3]
        if self.settings.node_direction is NodeDirection.RETROGRADE:
            speed = -abs(speed)
        else:
            speed = abs(speed)
        rahu = PlanetPosition(
            graha=int(Graha.RAHU),
            longitude=vals[0] % 360.0,
            latitude=vals[1],
            distance=vals[2],
            speed_longitude=speed,
            speed_latitude=vals[4],
            speed_distance=vals[5],
        )
        # swisseph exposes no separate south-node body; it is the exact opposite
        # point of the osculating node, which is what JHora also uses.
        ketu = PlanetPosition(
            graha=int(Graha.KETU),
            longitude=(vals[0] + 180.0) % 360.0,
            latitude=-vals[1],
            distance=vals[2],
            speed_longitude=speed,
            speed_latitude=-vals[4],
            speed_distance=vals[5],
        )
        return rahu, ketu

    def _ketu(self, rahu: PlanetPosition, ketu_true: PlanetPosition) -> PlanetPosition:
        if self.settings.ketu_mode is KetuMode.OPPOSITE_RAHU:
            return PlanetPosition(
                graha=int(Graha.KETU),
                longitude=(rahu.longitude + 180.0) % 360.0,
                latitude=-rahu.latitude,
                distance=rahu.distance,
                speed_longitude=rahu.speed_longitude,
                speed_latitude=-rahu.speed_latitude,
                speed_distance=rahu.speed_distance,
            )
        return ketu_true

    def houses(self, jd_ut: float, latitude: float, longitude: float) -> Houses:
        code = _HOUSE_CODE[self.settings.house_system]
        with _SWE_LOCK:
            self._apply_mode()
            flags = swe.FLG_SIDEREAL if self.settings.ayanamsa is not Ayanamsa.TROPICAL else 0
            cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, code, flags)
        return Houses(
            ascendant=ascmc[0] % 360.0,
            midheaven=ascmc[1] % 360.0,
            cusps=tuple(c % 360.0 for c in cusps[:12]),
            armc=ascmc[2] % 360.0,
            vertex=ascmc[3] % 360.0,
            equatorial_ascendant=ascmc[4] % 360.0,
        )

    # -- risings -----------------------------------------------------------

    def _rise_trans(self, jd_ut: float, latitude: float, longitude: float, altitude: float, rsmi: int) -> float | None:
        flags = _RISE_FLAGS[self.settings.sunrise_mode]
        with _SWE_LOCK:
            self._apply_mode()
            res, tret = swe.rise_trans(
                jd_ut, swe.SUN, rsmi | flags,
                (longitude, latitude, altitude),
                0.0, 0.0, self._base_flag,
            )
        if res < 0:
            return None
        return tret[0]

    def sunrise(self, jd_ut: float, latitude: float, longitude: float, altitude: float = 0.0) -> float | None:
        return self._rise_trans(jd_ut, latitude, longitude, altitude, swe.CALC_RISE)

    def sunset(self, jd_ut: float, latitude: float, longitude: float, altitude: float = 0.0) -> float | None:
        return self._rise_trans(jd_ut, latitude, longitude, altitude, swe.CALC_SET)

    def body_rise(self, jd_ut: float, body: int, latitude: float, longitude: float, altitude: float = 0.0, *, setting: bool = False) -> float | None:
        """Rise or set time for any body — used for moonrise/moonset.

        Uses the same definition as sunrise; for the Moon the choice moves the
        time by several minutes, so it must not be hardcoded.
        """
        rsmi = swe.CALC_SET if setting else swe.CALC_RISE
        flags = _RISE_FLAGS[self.settings.sunrise_mode]
        with _SWE_LOCK:
            self._apply_mode()
            res, tret = swe.rise_trans(
                jd_ut, body, rsmi | flags,
                (longitude, latitude, altitude),
                0.0, 0.0, self._base_flag,
            )
        if res < 0:
            return None
        return tret[0]


@lru_cache(maxsize=64)
def get_ephemeris(settings: Settings) -> SwissEphemeris:
    """Cached provider per settings object.

    ``Settings`` is frozen, so identical configurations share one instance and
    avoid re-probing the ephemeris directory on every request.
    """
    return SwissEphemeris(settings)
