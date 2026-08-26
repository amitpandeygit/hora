"""Upagrahas — the eleven sub-planets of book chapter 4.

Two groups with nothing in common but the name:

* **Sun-based** (§4.2) — Dhuma, Vyatipaata, Parivesha, Indrachaapa and Upaketu
  are pure functions of the Sun's longitude, chained off Dhuma.
* **Time-based** (§4.3) — Kaala, Mrityu, Artha Praharaka, Yama Ghantaka, Gulika
  and Maandi need the birth time: the day or night is cut into eight parts, each
  ruled by a graha, and the upagraha is the *lagna rising* at a point inside its
  ruler's part.

All five Sun-based upagrahas are described as "very malefic".
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core.const import (
    DHUMA_OFFSET,
    PART_LORD_CYCLE,
    UPAGRAHA_NAMES,
    UPAGRAHA_PART_LORD,
    UPAGRAHA_RISES_AT_BEGINNING,
    UPAKETU_OFFSET,
    Upagraha,
)
from hora.core.ephemeris import get_ephemeris
from hora.core.settings import Settings, UpagrahaRisePoint
from hora.core.timeutil import norm360


@dataclass(frozen=True, slots=True)
class BirthPeriod:
    """The day or night a birth falls in, and the vaara that governs it."""

    is_night: bool
    start_jd: float          # sunrise for a day birth, sunset for a night one
    end_jd: float            # sunset, or the following sunrise
    vaara: int               # 0 = Sunday
    sunrise_jd: float        # the sunrise that opened this vaara


@dataclass(frozen=True, slots=True)
class UpagrahaPosition:
    """One upagraha's longitude, and how it was arrived at."""

    upagraha: int
    name: str
    longitude: float
    #: Only for the time-based six: which graha's part it rose in, the part
    #: number 1-8, and the instant used.
    part_lord: int | None = None
    part_index: int | None = None
    rise_jd: float | None = None

    @property
    def rasi(self) -> int:
        return int(self.longitude // 30.0)

    @property
    def degrees_in_rasi(self) -> float:
        return self.longitude % 30.0


# --------------------------------------------------------------------------
# 4.2 Sun-based upagrahas
# --------------------------------------------------------------------------


def sun_based(sun_longitude: float) -> dict[int, float]:
    """The five Sun-based upagraha longitudes, per Table 9.

    The chain is Dhuma from the Sun, then each of the rest from the one before:

        Dhuma       = Sun + 133 deg 20 min
        Vyatipaata  = 360 - Dhuma
        Parivesha   = Vyatipaata + 180
        Indrachaapa = 360 - Parivesha
        Upaketu     = Indrachaapa + 16 deg 40 min

    Table 9 also gives ``Upaketu = Sun - 30``, and the two agree identically:
    unrolling the chain gives ``Sun + 330``, which is ``Sun - 30``.
    """
    dhuma = norm360(sun_longitude + DHUMA_OFFSET)
    vyatipaata = norm360(360.0 - dhuma)
    parivesha = norm360(vyatipaata + 180.0)
    indrachaapa = norm360(360.0 - parivesha)
    upaketu = norm360(indrachaapa + UPAKETU_OFFSET)
    return {
        int(Upagraha.DHUMA): dhuma,
        int(Upagraha.VYATIPAATA): vyatipaata,
        int(Upagraha.PARIVESHA): parivesha,
        int(Upagraha.INDRACHAAPA): indrachaapa,
        int(Upagraha.UPAKETU): upaketu,
    }


# --------------------------------------------------------------------------
# 4.3 Time-based upagrahas
# --------------------------------------------------------------------------


def birth_period(
    jd_ut: float, latitude: float, longitude: float, altitude: float, settings: Settings
) -> BirthPeriod:
    """Which day or night a birth falls in, per §4.3.

    "A day starts at the time of sunrise and ends at the time of sunset. A night
    starts at the time of sunset and ends at the time of next day's sunrise."

    Three cases, and the pre-dawn one is the awkward one:

    * **After sunset** — the night runs from today's sunset to tomorrow's sunrise.
    * **Between sunrise and sunset** — the day.
    * **Before sunrise** — the night began at *yesterday's* sunset, and because
      the vaara turns at sunrise, the birth still belongs to yesterday's vaara.

    That last case cannot be approximated from today's figures: yesterday's
    sunset is a separate calculation, and getting it wrong displaces all eight
    parts and therefore every time-based upagraha.
    """
    eph = get_ephemeris(settings)
    sunrise = eph.sunrise(jd_ut - 1.5, latitude, longitude, altitude)
    if sunrise is None:
        raise ValueError("no sunrise at this latitude/date (polar day or night)")
    # Walk forward to the last sunrise at or before the birth.
    while True:
        nxt = eph.sunrise(sunrise + 0.5, latitude, longitude, altitude)
        if nxt is None or nxt > jd_ut:
            break
        sunrise = nxt

    sunset = eph.sunset(sunrise, latitude, longitude, altitude)
    if sunset is None:
        raise ValueError("no sunset at this latitude/date (polar day or night)")

    if jd_ut < sunset:
        return BirthPeriod(False, sunrise, sunset, _vaara_of(sunrise, settings), sunrise)

    next_sunrise = eph.sunrise(sunset, latitude, longitude, altitude)
    if next_sunrise is None:
        raise ValueError("no sunrise following this sunset (polar day or night)")
    return BirthPeriod(True, sunset, next_sunrise, _vaara_of(sunrise, settings), sunrise)


def _vaara_of(sunrise_jd: float, settings: Settings) -> int:
    """Weekday of the vaara opened by a given sunrise. 0 = Sunday.

    Taken at local noon of that sunrise's civil date to stay clear of the
    midnight boundary.
    """
    import swisseph as swe

    y, m, d, _ = swe.revjul(sunrise_jd, swe.GREG_CAL)
    return int(swe.day_of_week(swe.julday(y, m, d, 12.0, swe.GREG_CAL)) + 1) % 7


def part_lords(vaara: int, *, night: bool) -> tuple[int | None, ...]:
    """Lords of the eight parts of a day or night, reproducing Table 10.

    Every row of Table 10 is the same eight-slot cycle — the seven grahas in
    weekday order followed by one lord-less slot — rotated to a starting point:

    * by day, it starts at the lord of the weekday;
    * by night, at the **fifth graha from** the lord of the weekday, counted
      through the seven grahas without the lord-less slot.
    """
    start = (vaara + 4) % 7 if night else vaara
    return tuple(PART_LORD_CYCLE[(start + i) % 8] for i in range(8))


def part_index_of(lord: int, vaara: int, *, night: bool) -> int | None:
    """Which of the eight parts a graha rules, 1-based. None if it rules none."""
    lords = part_lords(vaara, night=night)
    for i, owner in enumerate(lords):
        if owner is not None and int(owner) == int(lord):
            return i + 1
    return None


def part_bounds(
    part_index: int, start_jd: float, end_jd: float
) -> tuple[float, float]:
    """Julian Day bounds of one of the eight equal parts, 1-based."""
    span = (end_jd - start_jd) / 8.0
    begin = start_jd + (part_index - 1) * span
    return begin, begin + span


def time_based(
    vaara: int,
    *,
    night: bool,
    period_start_jd: float,
    period_end_jd: float,
    latitude: float,
    longitude: float,
    settings: Settings,
) -> dict[int, UpagrahaPosition]:
    """The six time-based upagrahas.

    ``period_start_jd``/``period_end_jd`` bound the day (sunrise to sunset) or
    the night (sunset to next sunrise), whichever the birth falls in.

    Each upagraha is the lagna rising at a point inside its ruling graha's part:
    the middle of that part, except Maandi which rises at its beginning. The
    ``upagraha_rise_point`` setting moves them all to the beginning, which is the
    variant footnote 9 attributes to "some scholars".
    """
    eph = get_ephemeris(settings)
    all_at_beginning = settings.upagraha_rise_point is UpagrahaRisePoint.BEGINNING

    out: dict[int, UpagrahaPosition] = {}
    for upagraha, lord in UPAGRAHA_PART_LORD.items():
        index = part_index_of(lord, vaara, night=night)
        if index is None:  # pragma: no cover - every graha rules one part
            continue
        begin, end = part_bounds(index, period_start_jd, period_end_jd)
        at_beginning = all_at_beginning or upagraha in UPAGRAHA_RISES_AT_BEGINNING
        jd = begin if at_beginning else (begin + end) / 2.0
        houses = eph.houses(jd, latitude, longitude)
        out[int(upagraha)] = UpagrahaPosition(
            upagraha=int(upagraha),
            name=UPAGRAHA_NAMES[upagraha],
            longitude=houses.ascendant,
            part_lord=int(lord),
            part_index=index,
            rise_jd=jd,
        )
    return out


def all_upagrahas(
    sun_longitude: float,
    vaara: int,
    *,
    night: bool,
    period_start_jd: float,
    period_end_jd: float,
    latitude: float,
    longitude: float,
    settings: Settings,
) -> dict[int, UpagrahaPosition]:
    """All eleven upagrahas for a chart."""
    out = {
        u: UpagrahaPosition(upagraha=u, name=UPAGRAHA_NAMES[u], longitude=lon)
        for u, lon in sun_based(sun_longitude).items()
    }
    out.update(
        time_based(
            vaara,
            night=night,
            period_start_jd=period_start_jd,
            period_end_jd=period_end_jd,
            latitude=latitude,
            longitude=longitude,
            settings=settings,
        )
    )
    return out
