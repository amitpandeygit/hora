"""Request and response models for the calculation API."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator

from hora.core.settings import Settings


class PlaceIn(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Degrees north of the equator")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Degrees east of Greenwich")
    altitude: float = Field(0.0, description="Metres above sea level")
    name: str | None = None


class BirthDataIn(BaseModel):
    """Local civil date and time plus a place.

    Supply either ``tz_name`` (preferred — historical DST is applied) or an
    explicit ``utc_offset_hours``. An explicit offset always wins, which is what
    you want when reproducing a chart someone cast with a fixed zone.
    """

    year: int = Field(..., ge=-5400, le=5400)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(0, ge=0, le=23)
    minute: int = Field(0, ge=0, le=59)
    second: float = Field(0.0, ge=0.0, lt=60.0)
    tz_name: str | None = Field(None, examples=["Asia/Kolkata"])
    utc_offset_hours: float | None = Field(None, ge=-14.0, le=14.0)
    place: PlaceIn

    @model_validator(mode="after")
    def _needs_a_zone(self) -> BirthDataIn:
        if self.tz_name is None and self.utc_offset_hours is None:
            raise ValueError("supply tz_name or utc_offset_hours")
        return self


class ChartRequest(BirthDataIn):
    settings: Settings = Field(default_factory=Settings)


class VargaRequest(ChartRequest):
    charts: list[str] = Field(
        default_factory=lambda: ["D1", "D9"],
        description='Varga codes, e.g. ["D1","D9","D10"]. Any D<N> up to D300 works.',
    )
    variants: dict[str, str] = Field(
        default_factory=dict,
        description='Per-chart variant override, e.g. {"D2":"parivritti"}',
    )


class DashaRequest(ChartRequest):
    system: str = Field("vimshottari", description="Dasha system key")
    levels: int = Field(2, ge=1, le=6, description="1=mahadasha, 2=+antardasha, ...")
    cycles: int = Field(1, ge=1, le=3)
    start_star: int = Field(
        1, ge=1, le=27,
        description=(
            "Which constellation from the Moon's starts the cycle, counted "
            "inclusively. 1 is the Moon's own. Section 16.4.1 allows 4, 5 and "
            "8 — the kshema, utpanna and adhana stars. The balance at birth "
            "always comes from the Moon's own star; only the lord moves."
        ),
    )
    as_of: str | None = Field(
        None, description="ISO datetime; when given, the running period chain is returned too"
    )


class PanchangaRequest(BirthDataIn):
    settings: Settings = Field(default_factory=Settings)


class ErrorOut(BaseModel):
    error: str
    detail: str | None = None


JsonDict = dict[str, Any]
