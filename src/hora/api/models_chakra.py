"""Models for the chakra endpoints — book §1.3.4."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ChakraIn(BaseModel):
    """The bodies a chart is prepared from. Every group is optional.

    Section 1.3.4: "we need to first determine the rasis occupied by all
    planets, upagrahas, lagna and special lagnas". A chart of the nine grahas
    alone is still a chart; nothing is invented for a group left out.
    """

    graha_positions: dict[int, float] | None = Field(
        None, description="Graha id -> position. 0 = Sun."
    )
    upagraha_positions: dict[int, float] | None = Field(
        None, description="Upagraha id -> position. 0 = Dhuma."
    )
    special_lagna_positions: dict[int, float] | None = Field(
        None, description="Special lagna id -> position. 0 = Bhaava Lagna."
    )
    lagna: float | None = Field(None, description="The ascendant's position")
    positions_are_longitudes: bool = Field(
        True,
        description=(
            "True if the values are sidereal longitudes, False if they are "
            "bare rasi indices. Mixing the two in one request is not offered: "
            "reading 5 as either Gemini or five degrees of Aries is an error "
            "that looks plausible either way."
        ),
    )
    reference: str | None = Field(
        None,
        description=(
            "What the houses are counted from, for a bhava-based style. Omit "
            "it and section 1.3.3's default applies: the lagna, when one was "
            "supplied, and no houses when none was. Naming a reference that "
            "cannot be resolved is an error — not asking for houses and "
            "asking for impossible ones are different mistakes."
        ),
    )
    reference_rasi: int | None = Field(
        None, ge=0, le=11,
        description="The reference's rasi, when it is not the lagna",
    )


class BodyOut(BaseModel):
    kind: str = Field(..., examples=["graha", "upagraha", "lagna", "special_lagna"])
    id: int | None = Field(None, description="Null for the lagna, a singleton")
    name: str
    rasi: int
    longitude: float | None = Field(
        None, description="Null when the caller supplied a bare rasi"
    )
    degrees_in_rasi: float | None = None


class ChakraCellOut(BaseModel):
    rasi: int
    rasi_name: str
    abbreviation: str
    rasi_number: int = Field(
        ..., ge=1, le=12,
        description=(
            "1 for Aries. The number a North Indian chart writes in the box, "
            'so "the box with Asc has 4 in it and it shows Cn"'
        ),
    )
    house: int | None = Field(
        None,
        description=(
            "The cell's house from the reference, for a bhava-based style. "
            "Null when the chart has no reference."
        ),
    )
    is_empty: bool
    bodies: list[BodyOut]


class ChakraOut(BaseModel):
    reference: str | None
    reference_rasi: int | None
    reference_rasi_name: str | None
    has_houses: bool = Field(
        ..., description="False when no reference was given, so no cell has a house"
    )
    cells: list[ChakraCellOut] = Field(
        ..., description="Twelve, in zodiacal order from Aries"
    )
    occupied_rasis: list[int]
    empty_rasis: list[int]
    body_count: int


class ChartStyleOut(BaseModel):
    key: str = Field(..., examples=["south_indian", "north_indian", "east_indian"])
    name: str
    ruled_by: str = Field(..., examples=["Jupiter", "Venus", "Sun"])
    rasi_based: bool = Field(
        ...,
        description=(
            "True when a fixed position holds a rasi, False when it holds a "
            "bhava. The only substantive difference between the styles."
        ),
    )
    note: str


class ChartStylesOut(BaseModel):
    sanskrit: str = Field(..., examples=["chakra"])
    prepared_from: str
    cells: int = Field(..., description="Twelve, one per rasi")
    lagna_mark: str = Field(..., examples=["Asc"])
    bhava_name: str
    used_in_the_book: list[str]
    styles: list[ChartStyleOut]
