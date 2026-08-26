"""Dignity, temporal friendship, combustion and planetary war."""
from __future__ import annotations

from dataclasses import dataclass

from hora.core.const import (
    CLASSICAL_SEVEN,
    COMBUSTION_ORB,
    DEBILITATION_RASI,
    DIGNITY_BY_DEGREE,
    EXALTATION_DEG,
    EXALTATION_RASI,
    GRAHA_OWNS,
    MOOLATRIKONA,
    NATURAL_RELATION,
    RASI_LORD,
    Graha,
)
from hora.core.ephemeris.base import PlanetPosition
from hora.core.timeutil import norm180


def sign_dignity(graha: int, longitude: float) -> str:
    """Classical dignity of a graha by sign: exalted, moolatrikona, own, etc.

    Uses the exaltation *rasi* rather than the deep-exaltation degree, because
    book Table 6 gives the nodes an exaltation sign but no degree.
    """
    rasi = int(longitude // 30.0)
    deg = longitude % 30.0

    # The section 3.3 degree rules win where they apply: for Moon in Taurus and
    # Mercury in Virgo the exaltation rasi and the moolatrikona rasi coincide,
    # so only the degree separates them.
    for rule_rasi, start, end, dignity in DIGNITY_BY_DEGREE.get(graha, ()):
        if rule_rasi == rasi and start <= deg < end:
            return dignity

    if graha in EXALTATION_RASI:
        if EXALTATION_RASI[graha] == rasi:
            return "exalted"
        if DEBILITATION_RASI[graha] == rasi:
            return "debilitated"
    mt = MOOLATRIKONA.get(graha)
    if mt is not None and mt[0] == rasi and mt[1] <= deg < mt[2]:
        return "moolatrikona"
    if rasi in GRAHA_OWNS.get(graha, ()):
        return "own"
    return "neutral"


def exaltation_score(graha: int, longitude: float) -> float:
    """Fractional exaltation, 1.0 at the deep exaltation point and 0.0 at debilitation.

    This is the quantity uchcha bala is built from. Returns the neutral 0.5 for
    Rahu and Ketu: the book names their exaltation rasi but gives no deep
    exaltation degree, so any fraction would be invented.
    """
    if graha not in EXALTATION_DEG:
        return 0.5
    diff = abs(norm180(longitude - EXALTATION_DEG[graha]))
    return (180.0 - diff) / 180.0


def temporal_relation(graha: int, other: int, positions: dict[int, PlanetPosition]) -> int:
    """Tatkalika (temporal) friendship: 1 = friend, 0 = enemy.

    A graha is a temporal friend of anything in the 2nd, 3rd, 4th, 10th, 11th
    or 12th house from itself.
    """
    a = positions[graha].rasi
    b = positions[other].rasi
    house = (b - a) % 12 + 1
    return 1 if house in (2, 3, 4, 10, 11, 12) else 0


def compound_relation(graha: int, other: int, positions: dict[int, PlanetPosition]) -> str:
    """Panchadha (five-fold) relationship combining natural and temporal.

    Natural friend + temporal friend = great friend; natural enemy + temporal
    enemy = great enemy; and so on.
    """
    natural = NATURAL_RELATION.get(graha, {}).get(other)
    if natural is None:
        return "neutral"
    temporal = temporal_relation(graha, other, positions) * 2  # 0 or 2
    total = natural + temporal
    return {4: "great_friend", 3: "friend", 2: "neutral", 1: "enemy", 0: "great_enemy"}[total]


def dignity_with_relations(graha: int, positions: dict[int, PlanetPosition]) -> str:
    """Full dignity including the sign lord's relationship to the graha."""
    lon = positions[graha].longitude
    base = sign_dignity(graha, lon)
    if base != "neutral":
        return base
    lord = int(RASI_LORD[positions[graha].rasi])
    if lord == graha:
        return "own"
    if graha not in NATURAL_RELATION or lord not in CLASSICAL_SEVEN:
        return "neutral"
    return compound_relation(graha, lord, positions)


@dataclass(frozen=True, slots=True)
class Combustion:
    combust: bool
    separation: float
    orb: float


def combustion(graha: int, positions: dict[int, PlanetPosition]) -> Combustion:
    """Astangata — proximity to the Sun that burns a graha's significations."""
    orbs = COMBUSTION_ORB.get(graha)
    if orbs is None or graha == Graha.SUN:
        return Combustion(False, 0.0, 0.0)
    sep = abs(norm180(positions[graha].longitude - positions[Graha.SUN].longitude))
    orb = orbs[1] if positions[graha].is_retrograde else orbs[0]
    return Combustion(sep <= orb, sep, orb)


def graha_yuddha(positions: dict[int, PlanetPosition], orb: float = 1.0) -> list[tuple[int, int, int]]:
    """Planetary war: pairs of the five taras within ``orb`` degrees.

    Returns ``(graha_a, graha_b, winner)``. The northern (higher-latitude)
    planet wins, which is the rule JHora uses.
    """
    taras = [Graha.MARS, Graha.MERCURY, Graha.JUPITER, Graha.VENUS, Graha.SATURN]
    wars: list[tuple[int, int, int]] = []
    for i, a in enumerate(taras):
        for b in taras[i + 1:]:
            if a not in positions or b not in positions:
                continue
            if abs(norm180(positions[a].longitude - positions[b].longitude)) <= orb:
                winner = a if positions[a].latitude > positions[b].latitude else b
                wars.append((int(a), int(b), int(winner)))
    return wars
