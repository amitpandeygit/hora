"""Bhava (house) construction across JHora's house-division schemes.

Two families exist and they answer different questions:

* **Whole-sign** — bhava *is* rasi. This is the Parashari default and what the
  chart diagram shows.
* **Cusp-based** — Placidus, Koch, Sripati and friends produce unequal bhavas,
  used for the chalit chakra and for KP work.

Indian schemes treat the computed cusp as the bhava *madhya* (midpoint) and
derive the bhava boundaries as midpoints between consecutive madhyas; Western
schemes treat it as the bhava *beginning*. That distinction is handled here.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core.ephemeris.base import Houses, PlanetPosition
from hora.core.settings import HouseSystem
from hora.core.timeutil import norm360

#: Schemes whose cusps are bhava midpoints rather than bhava beginnings.
_MIDPOINT_SCHEMES = {HouseSystem.SRIPATI, HouseSystem.KN_RAO, HouseSystem.PVR}


@dataclass(frozen=True, slots=True)
class Bhava:
    """One house: its span, midpoint and the sign it is counted as."""

    index: int          # 1..12
    start: float        # bhava sandhi (beginning), sidereal degrees
    middle: float       # bhava madhya
    end: float          # next sandhi
    sign: int           # rasi of the madhya

    def contains(self, longitude: float) -> bool:
        """True if a longitude falls inside this bhava, handling 0/360 wrap."""
        span = norm360(self.end - self.start)
        return norm360(longitude - self.start) < span


def _arc(a: float, b: float) -> float:
    """Forward arc from ``a`` to ``b`` in degrees, always positive."""
    return norm360(b - a)


def _midpoint(a: float, b: float) -> float:
    return norm360(a + _arc(a, b) / 2.0)


def build_bhavas(houses: Houses, system: HouseSystem) -> list[Bhava]:
    """Turn raw ephemeris cusps into twelve bhavas under the chosen scheme."""
    if system is HouseSystem.WHOLE_SIGN:
        lagna_sign = int(houses.ascendant // 30.0)
        return [
            Bhava(
                index=i + 1,
                start=((lagna_sign + i) % 12) * 30.0,
                middle=((lagna_sign + i) % 12) * 30.0 + 15.0,
                end=((lagna_sign + i + 1) % 12) * 30.0,
                sign=(lagna_sign + i) % 12,
            )
            for i in range(12)
        ]

    cusps = list(houses.cusps)

    if system in _MIDPOINT_SCHEMES:
        madhyas = cusps
        starts = [_midpoint(madhyas[i - 1], madhyas[i]) for i in range(12)]
        return [
            Bhava(
                index=i + 1,
                start=starts[i],
                middle=madhyas[i],
                end=starts[(i + 1) % 12],
                sign=int(madhyas[i] // 30.0),
            )
            for i in range(12)
        ]

    return [
        Bhava(
            index=i + 1,
            start=cusps[i],
            middle=_midpoint(cusps[i], cusps[(i + 1) % 12]),
            end=cusps[(i + 1) % 12],
            sign=int(cusps[i] // 30.0),
        )
        for i in range(12)
    ]


def house_of(longitude: float, bhavas: list[Bhava]) -> int:
    """Which bhava (1..12) a longitude falls in."""
    for b in bhavas:
        if b.contains(longitude):
            return b.index
    return 1  # unreachable for a well-formed set; keeps callers total


def house_from_sign(sign: int, lagna_sign: int) -> int:
    """Whole-sign house number of a rasi, counted from the lagna sign."""
    return (sign - lagna_sign) % 12 + 1


def assign_houses(
    positions: dict[int, PlanetPosition],
    bhavas: list[Bhava],
) -> dict[int, int]:
    """Map each graha to its bhava number."""
    return {g: house_of(p.longitude, bhavas) for g, p in positions.items()}


#: House classifications JHora reports alongside the chart.
KENDRA = (1, 4, 7, 10)
PANAPHARA = (2, 5, 8, 11)
APOKLIMA = (3, 6, 9, 12)
TRIKONA = (1, 5, 9)
DUSTHANA = (6, 8, 12)
UPACHAYA = (3, 6, 10, 11)
MARAKA = (2, 7)


def classify_house(house: int) -> list[str]:
    """All classical labels that apply to a house number."""
    labels = []
    for name, group in (
        ("kendra", KENDRA), ("panaphara", PANAPHARA), ("apoklima", APOKLIMA),
        ("trikona", TRIKONA), ("dusthana", DUSTHANA),
        ("upachaya", UPACHAYA), ("maraka", MARAKA),
    ):
        if house in group:
            labels.append(name)
    return labels
