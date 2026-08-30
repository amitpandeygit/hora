"""Shared dasha machinery.

Every nakshatra-based dasha (Vimshottari, Ashtottari, Yogini, Shodasottari and
the rest) is the same algorithm with a different lord cycle, different period
lengths and a different rule for which nakshatra starts the cycle.  That
skeleton lives here; the individual systems are thin descriptors.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from hora.core import validate
from hora.core.const import (
    CIVIL_YEAR_DAYS,
    GRAHA_NAMES,
    NAKSHATRA_SPAN,
    SAVANA_YEAR_DAYS,
    SIDEREAL_YEAR_DAYS,
    TROPICAL_YEAR_DAYS,
)
from hora.core.settings import DashaYearLength

_YEAR_DAYS = {
    DashaYearLength.SIDEREAL: SIDEREAL_YEAR_DAYS,
    DashaYearLength.TROPICAL: TROPICAL_YEAR_DAYS,
    DashaYearLength.CIVIL: CIVIL_YEAR_DAYS,
    DashaYearLength.SAVANA: SAVANA_YEAR_DAYS,
}


def year_days(mode: DashaYearLength) -> float:
    return _YEAR_DAYS[mode]


@dataclass(frozen=True, slots=True)
class DashaPeriod:
    """One period at any level of the hierarchy."""

    lord: int
    lord_name: str
    level: int              # 1 = mahadasha, 2 = antardasha, ...
    start_jd: float
    end_jd: float
    children: list[DashaPeriod] = field(default_factory=list)

    @property
    def duration_days(self) -> float:
        return self.end_jd - self.start_jd


@dataclass(frozen=True, slots=True)
class NakshatraDashaSpec:
    """Descriptor for a nakshatra-based dasha system."""

    key: str
    display_name: str
    #: Lords in cycle order.
    order: tuple[int, ...]
    #: Period length in years, parallel to ``order``.
    years: tuple[float, ...]
    #: How the starting lord is chosen from the Moon's nakshatra index (0-26).
    #: ``mod`` walks ``order`` by ``nakshatra % len(order)``.
    start_rule: str = "mod"
    #: Nakshatra count the cycle is laid over — 27 for most, 28 when
    #: Abhijit is included (Ashtottari, Yogini variants).
    nakshatra_count: int = 27

    @property
    def total_years(self) -> float:
        return sum(self.years)


def _sub_periods(
    spec: NakshatraDashaSpec,
    lord: int,
    start_jd: float,
    span_days: float,
    level: int,
    max_level: int,
) -> list[DashaPeriod]:
    """Recursively divide a period among all lords, starting from ``lord``.

    Each sub-period takes the same proportion of its parent that the sub-lord's
    period takes of the whole cycle — the standard proportional rule.
    """
    if level > max_level:
        return []
    idx = spec.order.index(lord)
    total = spec.total_years
    out: list[DashaPeriod] = []
    cursor = start_jd
    for k in range(len(spec.order)):
        sub_lord = spec.order[(idx + k) % len(spec.order)]
        sub_years = spec.years[(idx + k) % len(spec.order)]
        sub_days = span_days * sub_years / total
        period = DashaPeriod(
            lord=int(sub_lord),
            lord_name=GRAHA_NAMES[sub_lord],
            level=level,
            start_jd=cursor,
            end_jd=cursor + sub_days,
            children=_sub_periods(spec, sub_lord, cursor, sub_days, level + 1, max_level),
        )
        out.append(period)
        cursor = period.end_jd
    return out


def compute_nakshatra_dasha(
    spec: NakshatraDashaSpec,
    moon_longitude: float,
    birth_jd: float,
    year_length: DashaYearLength,
    *,
    levels: int = 2,
    cycles: int = 1,
    start_star: int = 1,
) -> list[DashaPeriod]:
    """Build the dasha tree from the Moon's longitude at birth.

    The first mahadasha is truncated: the elapsed fraction of the Moon's
    nakshatra is the fraction of that dasha already consumed at birth.  Its
    sub-periods are still laid out over the *full* mahadasha, so that antardashas
    running at birth are reported with their true boundaries — this is what
    JHora does, and it is why the first mahadasha's children can start before
    the birth moment.

    :param start_star: which constellation from the Moon's begins the cycle,
        counted inclusively. 1 is the Moon's own and the default; §16.4.1
        allows the 4th, 5th and 8th — the kshema, utpanna and adhana stars.
        The fraction left at birth always comes from the Moon's own star
        whichever is chosen, so only the lord and the sequence move.
    """
    days_per_year = year_days(year_length)
    lon = moon_longitude % 360.0
    nak = int(lon // NAKSHATRA_SPAN)
    elapsed_fraction = (lon - nak * NAKSHATRA_SPAN) / NAKSHATRA_SPAN

    n = len(spec.order)
    start_index = (nak + validate.in_range("start_star", start_star, 1, 27) - 1) % n
    first_years = spec.years[start_index]

    # Wind back to the notional start of the running mahadasha.
    cursor = birth_jd - elapsed_fraction * first_years * days_per_year

    periods: list[DashaPeriod] = []
    for _cycle in range(cycles):
        for k in range(n):
            i = (start_index + k) % n
            lord = spec.order[i]
            span = spec.years[i] * days_per_year
            periods.append(
                DashaPeriod(
                    lord=int(lord),
                    lord_name=GRAHA_NAMES[lord],
                    level=1,
                    start_jd=cursor,
                    end_jd=cursor + span,
                    children=_sub_periods(spec, lord, cursor, span, 2, levels),
                )
            )
            cursor += span
    return periods


def balance_at_birth(
    spec: NakshatraDashaSpec, moon_longitude: float, start_star: int = 1
) -> tuple[int, float]:
    """Lord of the birth mahadasha and the years of it remaining at birth.

    :param start_star: see :func:`compute_nakshatra_dasha`. §16.4.1 keeps the
        fraction from the Moon's own star and moves only the lord, so the
        balance is that lord's dasa length times the same fraction.
    """
    lon = moon_longitude % 360.0
    nak = int(lon // NAKSHATRA_SPAN)
    i = (nak + validate.in_range("start_star", start_star, 1, 27) - 1) % len(spec.order)
    remaining_fraction = 1.0 - (lon - nak * NAKSHATRA_SPAN) / NAKSHATRA_SPAN
    return int(spec.order[i]), spec.years[i] * remaining_fraction


def find_running(periods: list[DashaPeriod], jd: float) -> list[DashaPeriod]:
    """Walk the tree returning the chain of periods active at ``jd``."""
    chain: list[DashaPeriod] = []
    level = periods
    while level:
        match = next((p for p in level if p.start_jd <= jd < p.end_jd), None)
        if match is None:
            break
        chain.append(match)
        level = match.children
    return chain
