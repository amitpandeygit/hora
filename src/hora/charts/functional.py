"""Section 13.2 — the functional nature of planets.

Two things live here and they are deliberately kept apart.

`from_table` reads Table 30, which is what §13.2 gives for use and therefore
what we serve. `from_rules` applies §13.2's five stated rules directly. They
agree on 70 of the table's 81 cells; `divergences` names the other eleven.
That is not a defect in either — §13.2 says two-rasi owners need their
indications "judiciously combined" and then prints the result, so the table
records a judgement the rules do not determine. Keeping both means the
judgement is visible instead of buried.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    KENDRA,
    MOON_OMITTED_FROM,
    NATURAL_BENEFIC,
    RASI_ABBR,
    RASI_LORD,
    RASI_NAMES,
    TABLE_30_FUNCTIONAL_NATURE,
    TRIKONA,
    Graha,
)

BENEFIC = "functional benefic"
NEUTRAL = "functionally neutral"
MALEFIC = "functional malefic"

#: The seven Table 30 covers. Rahu and Ketu own no rasi, so §13.2's rules —
#: all of which turn on lordship — never reach them.
FUNCTIONAL_PLANETS: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

_GRAHA = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Mercury": Graha.MERCURY, "Jupiter": Graha.JUPITER,
    "Venus": Graha.VENUS, "Saturn": Graha.SATURN,
}

#: §13.2 treats Mercury as a natural benefic here. Its opening sentence makes
#: that conditional — "well-associated Mercury" — but Table 30 has one row per
#: lagna and no branch for Mercury's association, so the table is built on the
#: benefic reading. See docs/open-items.md OI-105.
NATURAL_BENEFIC_FOR_13_2: frozenset[str] = frozenset(
    {"Jupiter", "Venus", "Mercury"})


class FunctionalError(validate.InputError):
    """Raised when a functional-nature question cannot be answered."""


@dataclass(frozen=True)
class FunctionalNature:
    """One planet's functional nature for one lagna."""

    planet: str
    lagna: int
    #: Houses it owns from that lagna, ascending. One or two.
    houses: tuple[int, ...]
    #: BENEFIC, NEUTRAL or MALEFIC — or None when the phase decides it.
    nature: str | None
    #: True when the planet owns a quadrant and a trine.
    yogakaraka: bool
    #: Present only when `nature` is None: the answer under each Moon phase.
    depends_on_phase: dict[str, str] | None = None
    #: Why, in words. Never absent, so a caller always gets a reason.
    why: str = ""


def houses_owned(planet: str, lagna: int) -> tuple[int, ...]:
    """The houses `planet` owns, counted from `lagna`. 0 = Aries."""
    if planet not in _GRAHA:
        raise FunctionalError(
            f"{planet!r} owns no rasi, so section 13.2's rules — which all "
            f"turn on lordship — cannot reach it; the seven are "
            f"{', '.join(FUNCTIONAL_PLANETS)}")
    validate.in_range("lagna", lagna, 0, 11)
    graha = int(_GRAHA[planet])
    return tuple(sorted(
        ((sign - lagna) % 12) + 1
        for sign in range(12) if int(RASI_LORD[sign]) == graha
    ))


def is_yogakaraka(planet: str, lagna: int) -> bool:
    """§13.2: "Planet owning a quadrant and a trine becomes a yogakaraka".

    The 1st counts as neither here. Table 30 names six yogakarakas; letting
    the 1st serve as the trine would add Gemini's and Virgo's Mercury and
    Sagittarius's and Pisces's Jupiter, each of which owns the lagna and one
    other quadrant. So the quadrant must be the 4th, 7th or 10th and the trine
    the 5th or 9th.

    Note this differs from `_house_nature`, where the 1st *is* read as a trine
    — Table 30's Cancer row forces that. The 1st behaves as a trine for a
    planet's own nature and as neither for the yogakaraka test, and both
    readings are the table's, not ours. See docs/book-deviations.md D-45.
    """
    houses = set(houses_owned(planet, lagna))
    return bool(houses & {4, 7, 10}) and bool(houses & {5, 9})


def yogakaraka_of(lagna: int) -> str | None:
    """The one planet that owns both a quadrant and a trine, if any."""
    found = [p for p in FUNCTIONAL_PLANETS if is_yogakaraka(p, lagna)]
    if len(found) > 1:  # pragma: no cover - impossible, asserted by test
        raise FunctionalError(
            f"more than one yogakaraka for {RASI_NAMES[lagna]}: {found}")
    return found[0] if found else None


def _house_nature(house: int, planet: str) -> str:
    """§13.2's rules for one house. The 1st is read as a trine — Table 30's
    Cancer row proves it, being the one movable lagna whose Moon is listed."""
    if house in TRIKONA:
        return BENEFIC
    if house in (3, 6, 11):
        return MALEFIC
    if house in KENDRA:
        return MALEFIC if planet in NATURAL_BENEFIC_FOR_13_2 else NEUTRAL
    return NEUTRAL


def from_rules(planet: str, lagna: int) -> str:
    """§13.2's five rules applied directly, combining two houses by score.

    Every scoring choice traces to a printed sentence: trines benefic, the
    3rd/6th/11th malefic, quadrants by the owner's natural nature, the
    2nd/8th/12th neutral, and a yogakaraka "excellent". Nothing is tuned to
    make more cells agree — that would be inventing a rule §13.2 does not
    state, which is worse than a divergence we can name.

    This is the derivation, not the answer. Where it disagrees with Table 30
    the table wins, because §13.2 prints the table as the result of a
    judgement the rules do not determine.
    """
    if is_yogakaraka(planet, lagna):
        return BENEFIC
    score = 0
    for house in houses_owned(planet, lagna):
        nature = _house_nature(house, planet)
        score += 1 if nature is BENEFIC else -1 if nature is MALEFIC else 0
    return BENEFIC if score > 0 else MALEFIC if score < 0 else NEUTRAL


def from_table(planet: str, lagna: int) -> FunctionalNature:
    """Table 30's verdict, with the Moon's phase branch where it applies."""
    houses = houses_owned(planet, lagna)
    abbr = RASI_ABBR[validate.in_range("lagna", lagna, 0, 11)]
    yoga = is_yogakaraka(planet, lagna)
    _, benefics, neutrals, malefics = TABLE_30_FUNCTIONAL_NATURE[abbr]

    if planet in benefics:
        nature: str | None = BENEFIC
    elif planet in neutrals:
        nature = NEUTRAL
    elif planet in malefics:
        nature = MALEFIC
    else:
        nature = None

    if nature is not None:
        why = (
            f"Table 30 lists {planet} as a {nature} for {RASI_NAMES[lagna]} "
            f"lagna, owning house{'s' if len(houses) > 1 else ''} "
            f"{', '.join(str(h) for h in houses)}"
        )
        if yoga:
            why += " — a quadrant and a trine, so a yogakaraka"
        return FunctionalNature(planet, lagna, houses, nature, yoga, None, why)

    if planet != "Moon" or abbr not in MOON_OMITTED_FROM:  # pragma: no cover
        raise FunctionalError(
            f"Table 30 has no entry for {planet} at {RASI_NAMES[lagna]} "
            f"lagna, and only the Moon at {', '.join(MOON_OMITTED_FROM)} is "
            f"meant to be missing")
    return FunctionalNature(
        planet, lagna, houses, None, yoga,
        depends_on_phase={"waxing": MALEFIC, "waning": NEUTRAL},
        why=(
            f"Table 30 omits the Moon at {RASI_NAMES[lagna]} lagna because he "
            f"owns the {houses[0]}th, a quadrant, and his natural nature "
            f"follows his phase: waxing he is a natural benefic and quadrant "
            f"ownership makes him a functional malefic; waning he is a "
            f"natural malefic and quadrant ownership makes him functionally "
            f"neutral"
        ),
    )


def for_moon(lagna: int, waxing: bool) -> FunctionalNature:
    """The Moon's functional nature once the phase is known."""
    result = from_table("Moon", lagna)
    if result.nature is not None:
        return result
    assert result.depends_on_phase is not None
    phase = "waxing" if waxing else "waning"
    return FunctionalNature(
        "Moon", lagna, result.houses, result.depends_on_phase[phase],
        result.yogakaraka, None,
        why=f"{result.why}; this Moon is {phase}",
    )


def divergences() -> tuple[tuple[str, str, tuple[int, ...], str, str], ...]:
    """Every cell where §13.2's rules and Table 30 disagree.

    Returns ``(lagna abbr, planet, houses, from rules, from table)``. All but
    one are two-rasi owners, which is exactly what "judiciously combine" warns
    about; the exception is registered as D-46.
    """
    out = []
    for lagna, abbr in enumerate(RASI_ABBR):
        for planet in FUNCTIONAL_PLANETS:
            table = from_table(planet, lagna)
            if table.nature is None:
                continue
            rules = from_rules(planet, lagna)
            if rules != table.nature:
                out.append((abbr, planet, table.houses, rules, table.nature))
    return tuple(out)


def for_lagna(lagna: int) -> dict:
    """Every planet's functional nature for one lagna, Table 30's way."""
    validate.in_range("lagna", lagna, 0, 11)
    return {
        "lagna": lagna,
        "lagna_name": str(RASI_NAMES[lagna]),
        "yogakaraka": yogakaraka_of(lagna),
        "planets": [from_table(planet, lagna)
                    for planet in FUNCTIONAL_PLANETS],
    }


assert NATURAL_BENEFIC  # imported for the docstring's claim; see OI-105
