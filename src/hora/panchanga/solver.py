"""Root finding for angular events.

Tithi, nakshatra, yoga and karana boundaries are all "when does this angle next
reach a multiple of X" questions.  A single bracketed solver answers all of
them, and transit/ingress code reuses it.
"""
from __future__ import annotations

from collections.abc import Callable

from hora.core.timeutil import norm180

#: One second of time, in days — the convergence target for event times.
TIME_EPS = 1.0 / 86400.0


def solve_angle_crossing(
    angle_at: Callable[[float], float],
    target: float,
    jd_start: float,
    jd_end: float,
    *,
    max_iter: int = 100,
) -> float | None:
    """Find the JD in ``[jd_start, jd_end]`` where ``angle_at`` equals ``target``.

    ``angle_at`` returns a value in degrees; the difference from the target is
    wrapped into (-180, 180] so that the function is continuous across the
    0/360 seam.  Returns ``None`` when the interval does not bracket a root.
    """
    lo, hi = jd_start, jd_end
    f_lo = norm180(angle_at(lo) - target)
    f_hi = norm180(angle_at(hi) - target)
    if f_lo == 0.0:
        return lo
    if f_lo > 0.0 or f_hi < 0.0:
        return None

    for _ in range(max_iter):
        if hi - lo < TIME_EPS:
            break
        # Regula falsi with a bisection guard keeps this fast on the Moon's
        # near-linear motion without stalling on the Sun's slow arc.
        denom = f_hi - f_lo
        mid = (lo + hi) / 2.0 if denom == 0.0 else lo - f_lo * (hi - lo) / denom
        if not (lo < mid < hi):
            mid = (lo + hi) / 2.0
        f_mid = norm180(angle_at(mid) - target)
        if f_mid < 0.0:
            lo, f_lo = mid, f_mid
        else:
            hi, f_hi = mid, f_mid
    return (lo + hi) / 2.0


def scan_for_crossing(
    angle_at: Callable[[float], float],
    target: float,
    jd_from: float,
    jd_to: float,
    *,
    step: float = 0.25,
) -> float | None:
    """Step through a window looking for the first bracketed crossing."""
    jd = jd_from
    prev = norm180(angle_at(jd) - target)
    while jd < jd_to:
        nxt = min(jd + step, jd_to)
        cur = norm180(angle_at(nxt) - target)
        if prev <= 0.0 <= cur:
            found = solve_angle_crossing(angle_at, target, jd, nxt)
            if found is not None:
                return found
        jd, prev = nxt, cur
    return None
