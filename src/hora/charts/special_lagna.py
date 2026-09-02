"""Special lagnas — book chapter 5.

Three of the four share one form: start from **the Sun's longitude at sunrise**
and advance at a fixed rate for every minute elapsed since. They differ only in
the rate.

===========  =====================  ==============
Lagna        Rate                   Degrees/minute
===========  =====================  ==============
Bhaava (BL)  one rasi per 2 hours   0.25
Hora (HL)    one rasi per hour      0.5
Ghati (GL)   one rasi per ghati     1.25
===========  =====================  ==============

Sree Lagna (SL) is unrelated: the fraction of its nakshatra that the Moon has
traversed, applied to the whole zodiac, added to the lagna.

Which sunrise? The one that opened the current vaara, which for a pre-dawn
birth is *yesterday's*. Exercise 8 makes this explicit — a birth at 03:11 on
28 May 1961 is worked from the sunrise of 27 May.

§5.5 warns that Ghati Lagna moves 1.25° for every minute of birthtime error,
making it the most birthtime-sensitive point in the chart.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from hora.core import validate
from hora.core.const import NAKSHATRA_SPAN, Graha
from hora.core.ephemeris import get_ephemeris
from hora.core.settings import Settings
from hora.core.timeutil import norm360

#: Minutes in a day, for converting a Julian Day difference to minutes.
MINUTES_PER_DAY = 1440.0

#: §5.4: "one rasi per ghati (ghati=1/60th of a day, i.e., 24 minutes)".
#: Both halves of that definition are stored, because the rate 1d15' per
#: minute follows from them and from nothing else.
GHATIS_PER_DAY = 60
MINUTES_PER_GHATI = MINUTES_PER_DAY / GHATIS_PER_DAY      # 24.0


class SpecialLagna(IntEnum):
    BHAAVA = 0
    HORA = 1
    GHATI = 2
    SREE = 3


SPECIAL_LAGNA_NAMES = ["Bhaava Lagna", "Hora Lagna", "Ghati Lagna", "Sree Lagna"]
#: §5.4: "Ghati lagna is also called 'ghatika lagna'."
SPECIAL_LAGNA_ALIASES = [[], [], ["Ghatika Lagna"], []]
SPECIAL_LAGNA_ABBR = ["BL", "HL", "GL", "SL"]

#: Degrees advanced per minute elapsed since sunrise.
#:
#: PVR-6: §5.2's numbered method and Example 7 treat the elapsed minutes as
#: degrees directly, which is 1.0 and would make Bhaava Lagna move twice as
#: fast as Hora Lagna. The section's stated rate ("one rasi per 2 hours",
#: "1 degree per 4 minutes, i.e. 15 degrees per hour") and its own worked
#: illustration both give 0.25, and that is what is used.
#: See docs/precedence.md.
#: §5.2's illustration paragraph opens "then, **horalagna** is at 6s 4d47' at
#: 6:00 am..." but closes "**Bhavalagna** moves at the rate of 1d per 4
#: minutes". The numbers settle which is meant: 6s 4d47' at 6:00 to 6s 19d47'
#: at 7:00 is 15 degrees an hour, which is Bhaava Lagna's rate. Hora Lagna
#: moves 30 degrees an hour, so the illustration cannot be its.
#:
#: A fourth strand of evidence for PVR-6, and one more transcription oddity in
#: a section that already has several. See D-11.
ILLUSTRATION_NAMES_HORALAGNA = (
    "Section 5.2's illustration says \u201choralagna\u201d where its own numbers, and "
    "its own closing sentence, mean bhavalagna."
)

ADVANCE_PER_MINUTE = {
    SpecialLagna.BHAAVA: 0.25,     # one rasi per 2 hours
    SpecialLagna.HORA: 0.5,        # one rasi per hour
    SpecialLagna.GHATI: 1.25,      # one rasi per ghati (24 minutes)
}

#: §5.6: what each lagna shows, in the book's own framing — every one of them
#: shows *self*, seen through a different lens.
SPECIAL_LAGNA_VIEWPOINT = {
    SpecialLagna.HORA: "self, from the point of view of money, wealth and prosperity",
    SpecialLagna.GHATI: "self, from the point of view of fame, power and authority",
}
NORMAL_LAGNA_SHOWS = "self"

#: §5.6's two worked cases for when each matters.
SPECIAL_LAGNA_USE_EXAMPLES = {
    SpecialLagna.HORA: "timing good and bad periods for a businessman",
    SpecialLagna.GHATI: "timing good and bad periods for a politician",
}

#: §5.7: "In Sanskrit, the word "Sree" means wealth. It also means Lakshmi,
#: wife of Lord Narayana and goddess of wealth."
SREE_MEANING = "wealth"
SREE_ALSO_MEANS = "Lakshmi, wife of Lord Narayana and goddess of wealth"

#: §5.7: "Its use will be shown in the chapter on Sudasa." Recorded so the
#: forward reference is findable when that chapter is reached.
SREE_LAGNA_USED_IN = "Sudasa"

#: §5.7's closing warning. See OI-51.
MORE_PARASARA_LAGNAS_WARNING = (
    "There are some more special lagnas defined by Parasara, but they are "
    "beyond the scope of this book. We will restrict ourselves to the ones "
    "defined in this book."
)

#: What each special lagna is said to show (§5.6).
SPECIAL_LAGNA_SIGNIFIES = {
    SpecialLagna.BHAAVA: None,     # 5.2: "defined only for the sake of completeness"
    SpecialLagna.HORA: "money, wealth and prosperity",
    SpecialLagna.GHATI: "fame, power and authority",
    SpecialLagna.SREE: "prosperity",
}


@dataclass(frozen=True, slots=True)
class SpecialLagnaPosition:
    lagna: int
    name: str
    abbreviation: str
    longitude: float
    signifies: str | None = None

    @property
    def rasi(self) -> int:
        return int(self.longitude // 30.0)

    @property
    def degrees_in_rasi(self) -> float:
        return self.longitude % 30.0


#: Chapter 5's errors are the shared input errors; the alias is kept so the
#: service layer and its tests can name the concept locally.
SpecialLagnaError = validate.InputError


def advance_from_sunrise(
    sun_at_sunrise: float, minutes_since_sunrise: float, degrees_per_minute: float
) -> float:
    """The shared formula for Bhaava, Hora and Ghati lagna.

    §5.2/5.3/5.4 step (4): add the advancement to the Sun's longitude at
    sunrise, then reduce into 0-360.

    Elapsed time may not be negative — a special lagna is measured forward from
    sunrise, and a negative value silently produced a plausible-looking answer
    before this was checked.
    """
    sun = validate.finite("sun_at_sunrise", sun_at_sunrise)
    elapsed = validate.non_negative("minutes_since_sunrise", minutes_since_sunrise)
    rate = validate.positive("degrees_per_minute", degrees_per_minute)
    return norm360(sun + elapsed * rate)


def sree_lagna(moon_longitude: float, lagna_longitude: float) -> float:
    """§5.7: the Moon's progress through its nakshatra, mapped onto the zodiac.

    Take the fraction of the nakshatra the Moon has traversed, take the same
    fraction of 360 degrees, and add it to the lagna.
    """
    moon = validate.longitude("moon_longitude", moon_longitude)
    validate.finite("lagna_longitude", lagna_longitude)
    nakshatra = int(moon // NAKSHATRA_SPAN)
    fraction = (moon - nakshatra * NAKSHATRA_SPAN) / NAKSHATRA_SPAN
    return norm360(lagna_longitude + fraction * 360.0)


def minutes_since(sunrise_jd: float, jd_ut: float) -> float:
    """Elapsed minutes between sunrise and the moment in question."""
    return (jd_ut - sunrise_jd) * MINUTES_PER_DAY


def sun_longitude_at(jd_ut: float, settings: Settings) -> float:
    """The Sun's sidereal longitude at an instant — used at sunrise."""
    eph = get_ephemeris(settings)
    return eph.positions(jd_ut, (Graha.SUN,))[Graha.SUN].longitude


def all_special_lagnas(
    *,
    sunrise_jd: float,
    jd_ut: float,
    lagna_longitude: float,
    moon_longitude: float,
    settings: Settings,
) -> dict[int, SpecialLagnaPosition]:
    """All four special lagnas of chapter 5.

    ``sunrise_jd`` must be the sunrise that opened the current vaara — for a
    pre-dawn birth, the previous day's.
    """
    sun_at_sunrise = sun_longitude_at(sunrise_jd, settings)
    elapsed = minutes_since(sunrise_jd, jd_ut)

    out: dict[int, SpecialLagnaPosition] = {}
    for lagna, rate in ADVANCE_PER_MINUTE.items():
        out[int(lagna)] = SpecialLagnaPosition(
            lagna=int(lagna),
            name=SPECIAL_LAGNA_NAMES[lagna],
            abbreviation=SPECIAL_LAGNA_ABBR[lagna],
            longitude=advance_from_sunrise(sun_at_sunrise, elapsed, rate),
            signifies=SPECIAL_LAGNA_SIGNIFIES[lagna],
        )

    out[int(SpecialLagna.SREE)] = SpecialLagnaPosition(
        lagna=int(SpecialLagna.SREE),
        name=SPECIAL_LAGNA_NAMES[SpecialLagna.SREE],
        abbreviation=SPECIAL_LAGNA_ABBR[SpecialLagna.SREE],
        longitude=sree_lagna(moon_longitude, lagna_longitude),
        signifies=SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.SREE],
    )
    return out


#: §5.5 comment (1), the reason birthtime correction is worth having at all.
BIRTHTIME_SENSITIVITY_NOTE = (
    "If the birthtime changes by one minute, GL will change by 1.25\u00b0 (i.e., "
    "1\u00b015'). This is quite large and it can cause some error in the position "
    "of GL in some divisional charts. So, ghati lagna is more sensitive to "
    "birthtime errors than normal lagna. When using GL in divisional charts, "
    "we should keep this in mind and try to correct the birthtime based on "
    "known events first. Wrong data produces wrong results. Our analysis can "
    "only be as good as our data!"
)

#: §5.5 comment (2) — PVR's argument for why fine techniques matter despite
#: birthtime error, rather than choosing coarse ones that hide it.
BIRTHTIME_ERRORS_ARE_A_FACT_NOTE = (
    "Birthtime errors are a fact of life and we have to live with them. There "
    "are many people in this world who are born a few minutes apart in nearby "
    "places and yet lead significantly different lives."
)

#: §5.5 comment (3) — the two sunrise definitions and PVR's recommendation.
#: Encoded as the default in Settings; see D-10 and OI-19.
SUNRISE_DEFINITIONS = {
    "disc_centre": (
        "the time when the center of the visual disk representing Sun rises "
        "on the eastern horizon, i.e., the time when lagna and Sun are "
        "exactly at the same longitude"
    ),
    "disc_upper_limb": (
        "the time when the upper tip of the visual disk representing Sun "
        "appears to be rising on the eastern horizon, i.e., the time when the "
        "first ray of Sun is seen"
    ),
}
SUNRISE_RECOMMENDED = "disc_upper_limb"


@dataclass(frozen=True, slots=True)
class BirthtimeCorrection:
    """§5.5 comment (1) inverted: what birthtime a known GL range implies."""

    lagna: int
    observed_longitude: float
    target_low: float
    target_high: float
    earliest_shift_minutes: float
    latest_shift_minutes: float
    window_minutes: float


def birthtime_correction(
    observed_longitude: float,
    target_low: float,
    target_high: float,
    *,
    lagna: SpecialLagna = SpecialLagna.GHATI,
) -> BirthtimeCorrection:
    """How far the birthtime must move for a lagna to fall in a known range.

    §5.5 comment (1): "we should ... try to correct the birthtime based on
    known events first." Exercise 9 is exactly this — a past event fixes GL
    between two longitudes and the birthtime follows.

    A **negative** shift means the birth was earlier than recorded, a positive
    one later. The window is `(target_high - target_low) / rate` minutes wide
    regardless of where the observed value sits, because the lagna advances at
    a constant rate.

    :param observed_longitude: the lagna computed from the recorded birthtime.
    :param target_low: low end of the range the event implies.
    :param target_high: high end.
    :raises SpecialLagnaError: if the range is empty or inverted.
    """
    validate.longitude("observed_longitude", observed_longitude)
    low = validate.longitude("target_low", target_low)
    high = validate.longitude("target_high", target_high)
    if not high > low:
        raise SpecialLagnaError(
            f"target_high must exceed target_low; got {low} and {high}"
        )
    rate = ADVANCE_PER_MINUTE[lagna]
    return BirthtimeCorrection(
        lagna=int(lagna),
        observed_longitude=float(observed_longitude),
        target_low=low,
        target_high=high,
        earliest_shift_minutes=(low - observed_longitude) / rate,
        latest_shift_minutes=(high - observed_longitude) / rate,
        window_minutes=(high - low) / rate,
    )


#: Sree Lagna multiplies the Moon's error by 360/13°20' = 27. §5.7 does not
#: say so and no exercise depends on it, but Sudasa does: §20.2 rule 7 scales
#: the first dasa by SL's degrees within its sign, so a chart printed to the
#: arcminute pins that fraction only to about 27 arcminutes of SL.
SREE_LAGNA_AMPLIFIES_THE_MOON = 360.0 / NAKSHATRA_SPAN


def sree_lagna_moon_sensitivity(arcminutes_of_moon_error: float) -> float:
    """Arcminutes of Sree Lagna error for a given error in the Moon.

    SL is the lagna plus the Moon's progress through its nakshatra taken as a
    fraction of the whole zodiac. The fraction has 13°20' underneath it and
    360° on top, so every arcminute the Moon is out moves SL by 27.
    """
    return validate.finite("arcminutes_of_moon_error",
                           arcminutes_of_moon_error) * SREE_LAGNA_AMPLIFIES_THE_MOON


def ghati_lagna_birthtime_sensitivity(minutes_of_error: float) -> float:
    """Degrees of Ghati Lagna error for a given birthtime error (§5.5 comment 1).

    "If the birthtime changes by one minute, GL will change by 1.25 degrees."
    Exercise 9 inverts this to correct a birthtime from a known GL range.
    """
    return minutes_of_error * ADVANCE_PER_MINUTE[SpecialLagna.GHATI]
