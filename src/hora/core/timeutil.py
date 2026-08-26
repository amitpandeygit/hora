"""Civil time <-> Julian Day conversions and small angular helpers.

All internal computation is done in Julian Day (UT).  Callers supply local
civil time plus either an IANA timezone name or a fixed UTC offset; the
timezone name is preferred because it resolves historical DST correctly, which
JHora also does via its own city database.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import swisseph as swe


class TimeError(ValueError):
    """Raised when a civil time cannot be resolved to a unique instant."""


@dataclass(frozen=True, slots=True)
class Instant:
    """A fully resolved moment in time.

    ``jd_ut`` is the canonical value; the rest is retained for echoing back to
    the caller and for panchanga output that needs local wall-clock time.
    """

    jd_ut: float
    utc: datetime
    local: datetime
    utc_offset_hours: float
    tz_name: str | None

    @property
    def jd_tt(self) -> float:
        """Terrestrial Time Julian Day (UT + Delta-T)."""
        return self.jd_ut + swe.deltat(self.jd_ut)


def resolve_offset(local_naive: datetime, tz_name: str | None, utc_offset_hours: float | None) -> tuple[float, str | None]:
    """Determine the UTC offset in hours for a local civil time.

    An explicit ``utc_offset_hours`` always wins — JHora lets the user override
    the zone, and reproducing a JHora chart sometimes requires it.
    """
    if utc_offset_hours is not None:
        return float(utc_offset_hours), tz_name
    if tz_name is None:
        raise TimeError("either tz_name or utc_offset_hours must be supplied")
    try:
        zone = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError as exc:
        raise TimeError(f"unknown timezone {tz_name!r}") from exc
    aware = local_naive.replace(tzinfo=zone)
    offset = aware.utcoffset()
    if offset is None:
        raise TimeError(f"timezone {tz_name!r} yielded no offset for {local_naive}")
    return offset.total_seconds() / 3600.0, tz_name


def from_local(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: float = 0.0,
    *,
    tz_name: str | None = None,
    utc_offset_hours: float | None = None,
) -> Instant:
    """Build an :class:`Instant` from local civil date/time.

    Proleptic Gregorian is used throughout, matching JHora's default for dates
    after 1582; callers needing Julian-calendar input should convert first.
    """
    whole_second = int(second)
    micro = round((second - whole_second) * 1_000_000)
    # Deliberately naive: this is wall-clock time whose zone is resolved next.
    local = datetime(year, month, day, hour, minute, whole_second, micro)  # noqa: DTZ001
    offset_hours, resolved_tz = resolve_offset(local, tz_name, utc_offset_hours)
    utc = (local - timedelta(hours=offset_hours)).replace(tzinfo=UTC)
    jd = swe.julday(
        utc.year, utc.month, utc.day,
        utc.hour + utc.minute / 60.0 + (utc.second + utc.microsecond / 1e6) / 3600.0,
        swe.GREG_CAL,
    )
    return Instant(jd_ut=jd, utc=utc, local=local, utc_offset_hours=offset_hours, tz_name=resolved_tz)


def from_jd(jd_ut: float, *, utc_offset_hours: float = 0.0, tz_name: str | None = None) -> Instant:
    """Rebuild an :class:`Instant` from a Julian Day, for iterative solvers."""
    y, m, d, frac = swe.revjul(jd_ut, swe.GREG_CAL)
    utc = datetime(y, m, d, tzinfo=UTC) + timedelta(hours=frac)
    local = (utc + timedelta(hours=utc_offset_hours)).replace(tzinfo=None)
    return Instant(jd_ut=jd_ut, utc=utc, local=local, utc_offset_hours=utc_offset_hours, tz_name=tz_name)


def jd_to_local_str(jd_ut: float, utc_offset_hours: float) -> str:
    """Format a Julian Day as local ``YYYY-MM-DD HH:MM:SS``.

    Rounds to the nearest second rather than truncating: a sunrise at
    06:11:46.9998 is 06:11:47, and truncation would report it a second early.
    PARITY: whether JHora rounds or truncates is unconfirmed.
    """
    inst = from_jd(jd_ut + 0.5 / 86400.0, utc_offset_hours=utc_offset_hours)
    return inst.local.strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------------
# Angular helpers
# --------------------------------------------------------------------------

def norm360(x: float) -> float:
    """Normalise an angle into [0, 360)."""
    return x % 360.0


def norm180(x: float) -> float:
    """Normalise a difference into (-180, 180]."""
    x = (x + 180.0) % 360.0 - 180.0
    return x + 360.0 if x <= -180.0 else x


def dms(deg: float) -> tuple[int, int, float]:
    """Split a positive angle into degrees, arcminutes and arcseconds."""
    d = int(deg)
    rem = (deg - d) * 60.0
    m = int(rem)
    s = (rem - m) * 60.0
    return d, m, s


def dms_rounded(deg: float, *, seconds: bool = True) -> tuple[int, int, int]:
    """Split an angle into d/m/s with rounding carried upward.

    Truncating instead would print 4 deg 18' for a value of 4 deg 18' 59.99",
    losing most of a minute. Returns ``(d, m, s)``; ``s`` is 0 when
    ``seconds`` is False and the rounding is applied at the minute instead.
    """
    d, m, s = dms(abs(deg))
    if seconds:
        sec = round(s)
        if sec == 60:
            sec, m = 0, m + 1
    else:
        sec = 0
        if s >= 30.0:
            m += 1
    if m == 60:
        m, d = 0, d + 1
    return d, m, sec


def format_dms(deg: float, *, seconds: bool = True) -> str:
    """Render an angle the way JHora prints it, e.g. ``12-34-56``.

    Rounding carries upward, so 12 deg 34' 59.7" prints as ``12-35-00`` rather
    than the invalid ``12-34-60``.
    """
    sign = "-" if deg < 0 else ""
    d, m, sec = dms_rounded(deg, seconds=seconds)
    if not seconds:
        return f"{sign}{d}-{m:02d}"
    return f"{sign}{d}-{m:02d}-{sec:02d}"
