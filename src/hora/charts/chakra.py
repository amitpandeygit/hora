"""Chakras (charts) — book §1.3.4.

    "A 'chart' (Sanskrit name: chakra) is prepared with the information of
    rasis occupied by all planets. For preparing any chart, we need to first
    determine the rasis occupied by all planets, upagrahas, lagna and special
    lagnas."

**This module does not draw anything.** Drawing is presentation; what the
section defines that a calculation layer owns is two things:

* **occupancy** — which bodies fall in which of the twelve rasis, and
* the **rasi-based / bhava-based** distinction, which is the only respect in
  which the three drawing styles differ in substance rather than in looks.

    "Out of the three chart formats, (1) and (3) are rasi-based and (2) is
    bhava-based. In rasi-based chart drawing formats, a rasi is always at a
    fixed position... In bhava-based chart drawing formats, a bhava (house) is
    always at a fixed position."

A rasi-based renderer needs the rasi of each cell; a bhava-based one needs the
house. A :class:`Chakra` carries both, so either can be drawn from the same
object without recomputation — and so a caller that never draws anything can
still ask "what is in the 7th?" without building a layout.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from hora.charts.house import house_of_rasi
from hora.core import validate
from hora.core.const import (
    GRAHA_NAMES,
    RASI_ABBR,
    RASI_NAMES,
    UPAGRAHA_NAMES,
)


class ChakraError(validate.InputError):
    """A chart input that cannot be resolved.

    A subclass of :class:`~hora.core.validate.InputError`, which the shared
    range checks raise directly. Catch ``InputError`` to catch both.
    """


#: The kinds of body §1.3.4 says a chart is prepared from.
BODY_KINDS = ("graha", "upagraha", "lagna", "special_lagna")

#: §1.3.4's three styles. ``rasi_based`` is the distinction that matters to a
#: caller: it decides whether a cell is identified by its rasi or its house.
CHART_STYLES: dict[str, dict] = {
    "south_indian": {
        "name": "South Indian style chart",
        "ruled_by": "Jupiter",
        "rasi_based": True,
        "note": "A rasi is always at a fixed position",
    },
    "north_indian": {
        "name": "North Indian style diamond chart",
        "ruled_by": "Venus",
        "rasi_based": False,
        "note": (
            "A bhava is always at a fixed position. Lagna, marked \"Asc\", is "
            "always in the same visual area, and the rasi number is written in "
            "the box"
        ),
    },
    "east_indian": {
        "name": "East Indian style Sun chart",
        "ruled_by": "Sun",
        "rasi_based": True,
        "note": (
            "A rasi is always at a fixed position, as in the South Indian "
            "format. Some people draw it with an enclosing rectangle"
        ),
    },
}

#: "In this book, all the charts will be given in formats (1) and (2)."
STYLES_USED_IN_THE_BOOK = ("south_indian", "north_indian")

#: "Lagna (denoted by 'Asc' for ascendant)".
LAGNA_MARK = "Asc"

#: Sentinel for "the caller did not choose a reference", so the lagna default
#: of §1.3.3 can be applied where possible and quietly skipped where not —
#: while an *explicitly* named reference that cannot be resolved still raises.
DEFAULT_REFERENCE = "__default__"


@dataclass(frozen=True)
class Body:
    """One thing placed in a chart cell."""

    kind: str
    #: The body's id within its kind — a Graha or Upagraha value, or the
    #: SpecialLagna value. None for the lagna, which is a singleton.
    id: int | None
    name: str
    rasi: int
    #: Present when the caller gave a longitude rather than a bare rasi.
    longitude: float | None = None
    degrees_in_rasi: float | None = None


@dataclass(frozen=True)
class ChakraCell:
    """One of the twelve cells, whatever style it is later drawn in."""

    rasi: int
    rasi_name: str
    abbreviation: str
    #: 1 for Aries. "The number corresponding to the rasi (1 for Ar, 2 for Ta,
    #: 3 for Ge and so on) is shown in the box" of a North Indian chart.
    rasi_number: int
    #: The cell's house, counted from the reference. None when no reference
    #: was given, which is the only case in which a bhava-based style cannot
    #: be drawn from this object.
    house: int | None
    bodies: tuple[Body, ...] = ()

    @property
    def is_empty(self) -> bool:
        return not self.bodies


@dataclass(frozen=True)
class Chakra:
    """A chart: twelve cells in zodiacal order, plus what they are counted from."""

    cells: tuple[ChakraCell, ...]
    reference: str | None
    reference_rasi: int | None
    #: Bodies that were supplied, in the order they were placed.
    bodies: tuple[Body, ...] = field(default_factory=tuple)

    def cell_for_rasi(self, rasi: int) -> ChakraCell:
        """The cell a rasi-based style would draw at that rasi's fixed position."""
        return self.cells[validate.in_range("rasi", rasi, 0, 11)]

    def cell_for_house(self, house: int) -> ChakraCell:
        """The cell a bhava-based style would draw at that house's fixed position.

        :raises ChakraError: if the chart has no reference, in which case
            houses are undefined rather than assumed to start at Aries.
        """
        number = validate.in_range("house", house, 1, 12)
        if self.reference_rasi is None:
            raise ChakraError(
                "this chart has no reference point, so it has no houses; "
                "section 1.3.3 says an unspecified reference means the lagna, "
                "so supply one"
            )
        return self.cells[(self.reference_rasi + number - 1) % 12]

    def bodies_in_rasi(self, rasi: int) -> tuple[Body, ...]:
        return self.cell_for_rasi(rasi).bodies

    def bodies_in_house(self, house: int) -> tuple[Body, ...]:
        return self.cell_for_house(house).bodies

    @property
    def occupied_rasis(self) -> tuple[int, ...]:
        return tuple(c.rasi for c in self.cells if not c.is_empty)

    @property
    def empty_rasis(self) -> tuple[int, ...]:
        return tuple(c.rasi for c in self.cells if c.is_empty)


def _placed(kind: str, body_id: int | None, name: str, position: float,
            *, is_longitude: bool) -> Body:
    if is_longitude:
        lon = validate.longitude(f"{kind} {name}", position)
        return Body(kind=kind, id=body_id, name=name, rasi=int(lon // 30.0),
                    longitude=lon, degrees_in_rasi=lon % 30.0)
    # A fractional value is not a rasi index. Catching it turns the most
    # likely misuse of this mode — a longitude passed with the flag off —
    # from a silent wrong answer into an error. A whole number below 12 stays
    # genuinely ambiguous and is accepted; see docs/api-contract.md D-1.
    if float(position) != int(position):
        raise ChakraError(
            f"{kind} {name}: {position} is not a rasi index. Rasi indices are "
            f"whole numbers 0 to 11; pass positions_are_longitudes=true if "
            f"this is a longitude"
        )
    rasi = validate.in_range(f"{kind} {name}", int(position), 0, 11)
    return Body(kind=kind, id=body_id, name=name, rasi=rasi)


def build(
    graha_positions: dict[int, float] | None = None,
    upagraha_positions: dict[int, float] | None = None,
    special_lagna_positions: dict[int, float] | None = None,
    lagna: float | None = None,
    *,
    positions_are_longitudes: bool = True,
    reference: str | None = DEFAULT_REFERENCE,
    reference_rasi: int | None = None,
) -> Chakra:
    """Build a chart from the bodies §1.3.4 says a chart is prepared from.

    Every group is optional: a chart of the nine grahas alone is a chart, and
    so is one of the lagna alone. Nothing is invented for a group left out.

    :param positions_are_longitudes: True if the values are sidereal
        longitudes, False if they are bare rasi indices. Mixing the two in one
        call is not offered, because a silent misreading of 5 as either Gemini
        or five degrees of Aries is the kind of error that looks plausible.
    :param reference: which reference the houses are counted from, for a
        bhava-based style. Left alone it applies §1.3.3's default — "If no
        reference point is specified when houses are mentioned, it means that
        lagna is used as the reference" — when a lagna was supplied, and
        yields a chart with no houses when none was. Naming a reference
        *explicitly* that cannot be resolved raises instead: not asking for
        houses and asking for impossible ones are different mistakes. Pass
        ``None`` to ask for no houses outright.
    :param reference_rasi: the reference's rasi, when it is not the lagna or
        when no lagna was supplied.
    :raises ChakraError: on an out-of-range position, or on a reference that
        cannot be resolved.
    """
    bodies: list[Body] = []

    for graha, position in sorted((graha_positions or {}).items()):
        index = validate.in_range("graha", graha, 0, 8)
        bodies.append(_placed("graha", index, GRAHA_NAMES[index], position,
                              is_longitude=positions_are_longitudes))

    for upagraha, position in sorted((upagraha_positions or {}).items()):
        index = validate.in_range("upagraha", upagraha, 0, len(UPAGRAHA_NAMES) - 1)
        bodies.append(_placed("upagraha", index, UPAGRAHA_NAMES[index], position,
                              is_longitude=positions_are_longitudes))

    lagna_body: Body | None = None
    if lagna is not None:
        lagna_body = _placed("lagna", None, "Lagna", lagna,
                             is_longitude=positions_are_longitudes)
        bodies.append(lagna_body)

    if special_lagna_positions:
        from hora.charts.special_lagna import SPECIAL_LAGNA_NAMES

        for special, position in sorted(special_lagna_positions.items()):
            index = validate.in_range(
                "special_lagna", special, 0, len(SPECIAL_LAGNA_NAMES) - 1
            )
            bodies.append(_placed(
                "special_lagna", index, SPECIAL_LAGNA_NAMES[index], position,
                is_longitude=positions_are_longitudes,
            ))

    # Resolve the reference the houses are counted from.
    defaulted = reference is DEFAULT_REFERENCE
    wanted = "lagna" if defaulted else reference

    if reference_rasi is not None:
        origin: int | None = validate.in_range(
            "reference_rasi", reference_rasi, 0, 11
        )
    elif wanted == "lagna" and lagna_body is not None:
        origin = lagna_body.rasi
    elif wanted is None or defaulted:
        # No reference asked for, or the default could not be applied because
        # no lagna was given. Either way the chart simply has no houses.
        origin = None
    else:
        raise ChakraError(
            f"reference {wanted!r} was requested but no rasi for it was "
            f"given; pass reference_rasi, or a lagna when the reference is "
            f"the lagna"
        )

    by_rasi: dict[int, list[Body]] = {rasi: [] for rasi in range(12)}
    for body in bodies:
        by_rasi[body.rasi].append(body)

    cells = tuple(
        ChakraCell(
            rasi=rasi,
            rasi_name=RASI_NAMES[rasi],
            abbreviation=RASI_ABBR[rasi],
            rasi_number=rasi + 1,
            house=None if origin is None else house_of_rasi(origin, rasi),
            bodies=tuple(by_rasi[rasi]),
        )
        for rasi in range(12)
    )
    return Chakra(
        cells=cells,
        reference=None if origin is None else wanted,
        reference_rasi=origin,
        bodies=tuple(bodies),
    )
