"""Longitude notations used in the classical literature (book section 1.3.2).

Three forms appear in the book and in JHora output:

* decimal degrees from 0 Aries — ``94.3167``
* sign-degree-minute — ``7s 11d 37'``, meaning 7 whole signs completed then
  11 degrees 37 minutes into the 8th
* rasi-relative — ``25 Li 31``, meaning 25 degrees 31 minutes in Libra

All three denote the same quantity; these helpers convert between them.
"""
from __future__ import annotations

import re

from hora.core.const import RASI_ABBR, RASI_NAMES
from hora.core.timeutil import dms_rounded

#: Plain degrees from the start of the zodiac — the form §1.3.2 states first:
#: "measured in degrees, minutes and seconds from the start of the zodiac".
#: Requires no letters, so it cannot swallow "5s 17 45" or "25 Li 31".
_DMS_RE = re.compile(
    r"^\s*(\d+(?:\.\d+)?)\s*(?:d|deg|°)?\s*"
    r"(?:(\d+(?:\.\d+)?)\s*(?:m|')?)?\s*"
    r"(?:(\d+(?:\.\d+)?)\s*(?:s|\"|'')?)?\s*$"
)

_SDM_RE = re.compile(
    r"^\s*(\d+)\s*s\s*(\d+(?:\.\d+)?)\s*(?:d|deg|°)?\s*(?:(\d+(?:\.\d+)?)\s*(?:m|')?)?"
    r"\s*(?:(\d+(?:\.\d+)?)\s*(?:s|\"|'')?)?\s*$",
    re.IGNORECASE,
)
_RASI_RE = re.compile(
    r"^\s*(\d+(?:\.\d+)?)\s*(?:d|deg|°)?\s*([A-Za-z]{2,12})\s*"
    r"(\d+(?:\.\d+)?)?\s*(?:m|')?\s*(\d+(?:\.\d+)?)?\s*(?:s|\"|'')?\s*$"
)

_ABBR_LOOKUP = {a.lower(): i for i, a in enumerate(RASI_ABBR)}
_NAME_LOOKUP = {n.lower(): i for i, n in enumerate(RASI_NAMES)}


class NotationError(ValueError):
    """Raised when a longitude string cannot be parsed or is out of range."""


#: §1.3.2: "the longitude of any planet in the skies can be from 0°0'0" ... to
#: 359°59'59"". A full circle is the same point as zero, so 360 is excluded.
MIN_LONGITUDE = 0.0
MAX_LONGITUDE = 360.0


def _checked(longitude: float, text: str) -> float:
    """Reject a longitude outside the zodiac rather than wrapping it silently.

    Wrapping would turn a typo into a plausible position in another sign,
    which is worse than an error.
    """
    if not MIN_LONGITUDE <= longitude < MAX_LONGITUDE:
        raise NotationError(
            f"longitude {longitude:g}° from {text!r} is outside the zodiac; "
            f"section 1.3.2 gives the range as 0°0'0\" to 359°59'59\""
        )
    return longitude


def parse(text: str) -> float:
    """Parse any supported notation into decimal degrees from 0 Aries.

    >>> parse("94\u00b019")
    94.31666666666666
    >>> parse("5s 17 45")
    167.75
    >>> parse("25 Li 31")
    205.51666666666668

    :raises NotationError: if the text cannot be parsed, names an unknown
        rasi, or denotes a longitude outside 0 to 360 degrees.
    """
    if not isinstance(text, str):
        raise NotationError(f"expected a string, got {type(text).__name__}")

    m = _SDM_RE.match(text)
    if m:
        signs = int(m.group(1))
        if signs > 11:
            raise NotationError(f"sign count {signs} out of range in {text!r}")
        deg = float(m.group(2))
        minutes = float(m.group(3) or 0.0)
        seconds = float(m.group(4) or 0.0)
        return _checked(
            signs * 30.0 + deg + minutes / 60.0 + seconds / 3600.0, text
        )

    m = _RASI_RE.match(text)
    if m:
        deg = float(m.group(1))
        token = m.group(2).lower()
        rasi = _ABBR_LOOKUP.get(token, _NAME_LOOKUP.get(token))
        if rasi is None:
            raise NotationError(f"unknown rasi {m.group(2)!r} in {text!r}")
        minutes = float(m.group(3) or 0.0)
        seconds = float(m.group(4) or 0.0)
        return _checked(
            rasi * 30.0 + deg + minutes / 60.0 + seconds / 3600.0, text
        )

    # Plain degrees last: it is the most permissive pattern, so the two
    # sign-bearing forms get first refusal.
    m = _DMS_RE.match(text)
    if m:
        deg = float(m.group(1))
        minutes = float(m.group(2) or 0.0)
        seconds = float(m.group(3) or 0.0)
        return _checked(deg + minutes / 60.0 + seconds / 3600.0, text)

    raise NotationError(f"cannot parse longitude {text!r}")


def to_sign_dm(longitude: float, *, seconds: bool = False) -> str:
    """Render as ``7s 11d 37'`` — signs completed, then position in the next."""
    lon = longitude % 360.0
    signs = int(lon // 30.0)
    d, m, s = dms_rounded(lon - signs * 30.0, seconds=seconds)
    if seconds:
        return f"{signs}s {d}d {m:02d}' {s:02d}\""
    return f"{signs}s {d}d {m:02d}'"


def to_rasi_dm(longitude: float, *, seconds: bool = False) -> str:
    """Render as ``25 Li 31`` — degrees, rasi abbreviation, minutes."""
    lon = longitude % 360.0
    rasi = int(lon // 30.0)
    d, m, s = dms_rounded(lon - rasi * 30.0, seconds=seconds)
    if seconds:
        return f"{d} {RASI_ABBR[rasi]} {m:02d}:{s:02d}"
    return f"{d} {RASI_ABBR[rasi]} {m:02d}"


def all_forms(longitude: float) -> dict[str, object]:
    """Every notation for one longitude, for API responses."""
    return {
        "degrees": round(longitude % 360.0, 8),
        "sign_dm": to_sign_dm(longitude),
        "rasi_dm": to_rasi_dm(longitude),
    }
