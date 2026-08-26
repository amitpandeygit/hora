"""House arithmetic — book chapter 7.

Two ideas, and everything else follows from them:

* **A house is a rasi counted from a reference.** §7.1. Change the reference and
  the same rasi becomes a different house.
* **A category is relative too.** §7.4 computes trines, quadrants and the rest
  *from any house*, not only from the 1st: "the 3rd, 7th and 11th houses are the
  trines from the 3rd house."

§7.5 rules out cusp-based houses outright — a house never spans two rasis. The
engine's default `house_system` is whole-sign for that reason.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.karaka import atma_karaka
from hora.charts.vargas import d9_navamsa
from hora.core import validate
from hora.core.const import (
    GRAHA_LAGNA_HOUSES,
    HOUSE_CATEGORIES,
    HOUSE_SIGNIFICATIONS,
    PURUSHARTHA_TRIKONAS,
    RASI_LORD,
    VISIBLE_HALF,
)


@dataclass(frozen=True, slots=True)
class HousePlacement:
    """Where a rasi falls, counted from one reference."""

    reference: str
    reference_rasi: int
    rasi: int
    house: int
    categories: list[str]
    purushartha: str | None
    half: str


def house_of_rasi(reference_rasi: int, target_rasi: int) -> int:
    """Which house a rasi is, counted from a reference rasi. 1-based.

    §7.1: the reference's own rasi is the 1st house.
    """
    validate.in_range("reference_rasi", reference_rasi, 0, 11)
    validate.in_range("target_rasi", target_rasi, 0, 11)
    return (target_rasi - reference_rasi) % 12 + 1


def rasi_of_house(reference_rasi: int, house: int) -> int:
    """The rasi holding a given house, counted from a reference rasi."""
    validate.in_range("reference_rasi", reference_rasi, 0, 11)
    validate.in_range("house", house, 1, 12)
    return (reference_rasi + house - 1) % 12


def houses_from(base_house: int, houses: tuple[int, ...]) -> tuple[int, ...]:
    """Re-base a category onto another house.

    §7.4 works this through: the trines from the 3rd house are the 1st, 5th and
    9th *from it*, which are the 3rd, 7th and 11th overall.
    """
    validate.in_range("base_house", base_house, 1, 12)
    return tuple(sorted((base_house + h - 2) % 12 + 1 for h in houses))


def category_houses(category: str, base_house: int = 1) -> tuple[int, ...]:
    """The houses of a named category, optionally counted from another house."""
    entry = HOUSE_CATEGORIES.get(category)
    if entry is None:
        raise validate.InputError(
            f"unknown category {category!r}; expected one of "
            f"{', '.join(sorted(HOUSE_CATEGORIES))}"
        )
    return houses_from(base_house, entry["houses"])


def categories_of(house: int, base_house: int = 1) -> list[str]:
    """Every category a house belongs to, relative to a base house."""
    validate.in_range("house", house, 1, 12)
    return [
        name for name in HOUSE_CATEGORIES
        if house in category_houses(name, base_house)
    ]


def purushartha_of(house: int) -> str | None:
    """Which of the four purusharthas a house serves (§7.4.1)."""
    validate.in_range("house", house, 1, 12)
    for name, entry in PURUSHARTHA_TRIKONAS.items():
        if house in entry["houses"]:
            return name
    return None


def half_of(house: int, base_house: int = 1) -> str:
    """Visible or invisible half (§7.4.5).

    §7.4.5 says "the houses in the visible half of the zodiac **with respect
    to a reference**", so the split is relative like every other category in
    §7.4. `base_house` defaults to 1, which is the absolute split the section
    prints.
    """
    validate.in_range("house", house, 1, 12)
    return "visible" if house in houses_from(base_house, VISIBLE_HALF) else "invisible"


def signification(house: int) -> str:
    """§7.2's list for a house."""
    validate.in_range("house", house, 1, 12)
    return HOUSE_SIGNIFICATIONS[house]


def karakamsa_rasi(longitudes: dict[int, float]) -> int:
    """§7.3.6 — the rasi the atma karaka occupies **in navamsa**.

    "Navamsa chart throws light on the inner self and the rasi occupied by
    atma karaka in it is called \u201cKarakamsa\u201d."

    Two chapters meet here: the atma karaka is §8.2's (the graha of highest
    advancement) and the navamsa is §6.2.9's. This section is what ties them
    together, which is why the reference could not be computed before it.

    :param longitudes: graha id to sidereal longitude, for the chara karaka
        scheme. §8.2 excludes Ketu, so passing it is harmless.
    :raises hora.core.validate.InputError: if no atma karaka can be found.
    """
    karaka = atma_karaka(longitudes)
    return d9_navamsa(longitudes[karaka.graha]).sign


def paaka_lagna_rasi(lagna_rasi: int, graha_rasis: dict[int, int]) -> int:
    """§7.3.5 — the rasi occupied by the lagna lord.

    "If someone with Pisces lagna has Jupiter in Cancer, then Cancer becomes
    paaka lagna."
    """
    validate.in_range("lagna_rasi", lagna_rasi, 0, 11)
    lord = int(RASI_LORD[lagna_rasi])
    if lord not in graha_rasis:
        raise validate.InputError(
            f"paaka lagna needs the rasi of the lagna lord (graha {lord})"
        )
    return validate.in_range("lord rasi", graha_rasis[lord], 0, 11)


def graha_lagna_houses(graha: int) -> tuple[int, ...]:
    """Table 12 — the houses a graha is a natural reference for."""
    return GRAHA_LAGNA_HOUSES.get(graha, ())


def place(reference: str, reference_rasi: int, target_rasi: int) -> HousePlacement:
    """A full placement of one rasi against one reference."""
    house = house_of_rasi(reference_rasi, target_rasi)
    return HousePlacement(
        reference=reference,
        reference_rasi=reference_rasi,
        rasi=target_rasi,
        house=house,
        categories=categories_of(house),
        purushartha=purushartha_of(house),
        half=half_of(house),
    )
