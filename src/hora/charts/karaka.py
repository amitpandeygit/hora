"""Karaka computation — book chapter 8.

Only the chara (variable) karakas are computed; naisargika and sthira karakas
are fixed tables and are served straight from :mod:`hora.core.constants.karaka`.

§8.2 gives the whole procedure in three steps:

    (1) Take the eight planets - Sun, Moon, Mars, Mercury, Jupiter, Venus,
        Saturn and Rahu. For each planet, find its advancement from the
        beginning of the rasi occupied by it. For Rahu, measure the
        advancement from the end of his rasi.
    (2) Arrange them in the decreasing order of advancement.
    (3) The planet with the highest advancement is Atma Karaka.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    CHARA_KARAKAS,
    GRAHA_NAMES,
    KARAKA_KINDS,
    MEASURED_FROM_END_OF_RASI,
)


class KarakaError(validate.InputError):
    """A karaka input that cannot be resolved."""


@dataclass(frozen=True)
class CharaKaraka:
    """One graha's chara karaka assignment."""

    graha: int
    graha_name: str
    #: Degrees travelled within the occupied rasi, 0 to 30. For Rahu this is
    #: measured from the *end* of the rasi, per 8.2 step 1.
    advancement: float
    #: 1 for the highest advancement, 8 for the lowest.
    order: int
    symbol: str
    name: str
    shows: str
    #: True when this graha shares its karakatwa with another at exactly the
    #: same longitude. See 8.2's tie rule.
    shared: bool = False


def advancement(longitude: float, graha: int) -> float:
    """Degrees travelled within the occupied rasi.

    Measured from the start of the rasi for every graha except Rahu, which
    8.2 measures from the end — so Rahu at 1 deg 43' into Cancer advances
    30 deg - 1 deg 43' = 28 deg 17'.

    :param longitude: sidereal longitude in degrees; wrapped into 0-360.
    :param graha: a :class:`~hora.core.const.Graha` value.
    :raises KarakaError: if the longitude is not finite.
    """
    lon = validate.longitude("longitude", longitude)
    within = lon % 30.0
    if graha in MEASURED_FROM_END_OF_RASI:
        # 30.0 - 0.0 would be a full sign; a graha exactly on a cusp has
        # advanced nothing from the start, so it has advanced 30 from the end.
        return 30.0 - within
    return within


def chara_karakas(longitudes: dict[int, float]) -> list[CharaKaraka]:
    """Assign the eight chara karakas, highest advancement first.

    :param longitudes: sidereal longitude per graha. Must contain exactly the
        eight grahas 8.2 uses — the seven classical plus Rahu. Ketu is
        rejected rather than ignored, because silently dropping it would hide
        a caller's misunderstanding of 8.1.
    :returns: eight :class:`CharaKaraka`, ordered AK first and DK last.
    :raises KarakaError: on a missing, extra or non-finite entry.

    Ties are broken exactly as 8.2 says: "If two planets have the same
    degrees, we should compare minutes. If minutes are same, we should compare
    the seconds." Comparing the float advancement does all three at once.

    Two grahas at *exactly* the same longitude "hold a karakatwa together and
    the next karakatwa will have no ruler". Both are marked ``shared``; the
    book's instruction to fall back to the sthira karaka is left to the caller,
    since it needs a strength comparison this function does not have.
    """
    expected = set(KARAKA_KINDS["chara"]["grahas"])
    given = set(longitudes)
    if missing := expected - given:
        names = ", ".join(sorted(GRAHA_NAMES[g] for g in missing))
        raise KarakaError(f"chara karakas need all eight grahas; missing {names}")
    if extra := given - expected:
        names = ", ".join(sorted(GRAHA_NAMES[g] for g in extra))
        reason = KARAKA_KINDS["chara"].get("excludes", {})
        why = "; ".join(reason[g] for g in sorted(extra) if g in reason)
        raise KarakaError(
            f"chara karakas do not include {names}" + (f" — {why}" if why else "")
        )

    scored = [(advancement(longitudes[g], g), g) for g in expected]
    # Descending advancement. The graha index is a stable, deterministic
    # tie-break so that an exact tie does not depend on set iteration order.
    scored.sort(key=lambda pair: (-pair[0], pair[1]))

    tied = {adv for adv, _ in scored if sum(1 for a, _ in scored if a == adv) > 1}

    out = []
    for index, (adv, graha) in enumerate(scored):
        row = CHARA_KARAKAS[index]
        out.append(CharaKaraka(
            graha=int(graha),
            graha_name=GRAHA_NAMES[graha],
            advancement=adv,
            order=index + 1,
            symbol=row["symbol"],
            name=row["name"],
            shows=row["shows"],
            shared=adv in tied,
        ))
    return out


def atma_karaka(longitudes: dict[int, float]) -> CharaKaraka:
    """The graha with the highest advancement — 8.2 step 3.

    Named separately because it is the one chapter 9 and the karakamsa lagna
    need, and callers should not have to index into a list to get it.
    """
    return chara_karakas(longitudes)[0]


def karaka_of(longitudes: dict[int, float], symbol: str) -> CharaKaraka:
    """The graha holding a given karakatwa, by its Table 13 symbol.

    Accepts the alternate symbol for Jnaati Karaka: both "GK" and "JK" work.

    :raises KarakaError: if the symbol is not one of Table 13's eight.
    """
    from hora.core.const import CHARA_KARAKA_ALIASES

    wanted = symbol.strip()
    canonical = {row["symbol"]: row["symbol"] for row in CHARA_KARAKAS}
    for primary, aliases in CHARA_KARAKA_ALIASES.items():
        for alias in aliases:
            canonical[alias] = primary
    if wanted not in canonical:
        valid = ", ".join(sorted(canonical))
        raise KarakaError(f"unknown chara karaka {symbol!r}; expected one of {valid}")

    target = canonical[wanted]
    for karaka in chara_karakas(longitudes):
        if karaka.symbol == target:
            return karaka
    raise KarakaError(f"no graha holds {target}")  # pragma: no cover


def naisargika_karaka(house: int) -> dict:
    """Table 15's primary natural significator for a house.

    :param house: 1 to 12.
    :raises KarakaError: if the house is out of range.
    """
    from hora.core.const import NAISARGIKA_KARAKA

    number = validate.in_range("house", house, 1, 12)
    entry = NAISARGIKA_KARAKA[number]
    return {
        "house": number,
        "graha": int(entry["graha"]),
        "graha_name": GRAHA_NAMES[entry["graha"]],
        "signifies": entry["signifies"],
    }


def sthira_karaka_of_spouse(sex: str) -> dict:
    """§8.3: Jupiter in female charts, Venus in male charts.

    This is the one sthira karaka that depends on the native rather than being
    a fixed lookup, so it gets a function. ``sex`` is the chart's, matching the
    book's wording.

    :raises KarakaError: on any value other than "male" or "female".
    """
    from hora.core.const import STHIRA_KARAKA_OF_SPOUSE, STHIRA_KARAKA_OF_SPOUSE_NOTE

    key = sex.strip().lower()
    if key not in STHIRA_KARAKA_OF_SPOUSE:
        raise KarakaError(
            f"unknown chart sex {sex!r}; 8.3 distinguishes only 'male' and 'female'"
        )
    graha = STHIRA_KARAKA_OF_SPOUSE[key]
    return {
        "sex": key,
        "graha": int(graha),
        "graha_name": GRAHA_NAMES[graha],
        "note": STHIRA_KARAKA_OF_SPOUSE_NOTE,
    }
