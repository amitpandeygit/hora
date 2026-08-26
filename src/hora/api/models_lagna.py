"""Models for the special-lagna endpoints that take longitudes, not a birth."""
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class SpecialLagnaIn(BaseModel):
    """The book's own inputs for a special lagna.

    Bhaava, Hora and Ghati need the Sun at sunrise and the minutes since;
    Sree needs the Moon and the lagna. Ask for a lagna without its inputs and
    the request is rejected rather than quietly answered short.
    """

    lagnas: list[str] = Field(
        default_factory=lambda: ["BL", "HL", "GL", "SL"],
        min_length=1,
        max_length=4,
        examples=[["HL", "GL"]],
        description="Any of BL, HL, GL, SL. At least one.",
    )
    sun_at_sunrise: str | float | None = Field(
        None,
        examples=["24 Cp 17"],
        description="Sun's longitude at sunrise, decimal or classical notation",
    )
    minutes_since_sunrise: float | None = Field(
        None, ge=0.0, le=1500.0,
        examples=[766],
        description=(
            "Elapsed minutes from the sunrise that opened the vaara. A pre-dawn "
            "birth is measured from the previous day's sunrise, so this can "
            "exceed 1440 only marginally; it is never negative."
        ),
    )
    moon: str | float | None = Field(None, examples=["13 Li 06"], description="For SL")
    lagna: str | float | None = Field(None, examples=["25 Vi 05"], description="For SL")

    @model_validator(mode="after")
    def _inputs_match_the_lagnas_asked_for(self) -> SpecialLagnaIn:
        """Reject a request whose inputs cannot answer what it asks for.

        Caught at the schema so it is a 422 with a field location, and
        documented in the OpenAPI contract. The service guards the same thing
        again, because it can be called without going through HTTP.
        """
        wanted = {x.upper() for x in self.lagnas}
        if wanted & {"BL", "HL", "GL"} and (
            self.sun_at_sunrise is None or self.minutes_since_sunrise is None
        ):
            raise ValueError(
                "BL, HL and GL need both sun_at_sunrise and minutes_since_sunrise"
            )
        if "SL" in wanted and (self.moon is None or self.lagna is None):
            raise ValueError("SL needs both moon and lagna")
        return self


class LongitudeFormsOut(BaseModel):
    degrees: float
    sign_dm: str
    rasi_dm: str


class SpecialLagnaEchoOut(BaseModel):
    """Only the inputs the requested lagnas actually needed."""

    sun_at_sunrise: LongitudeFormsOut | None = None
    minutes_since_sunrise: float | None = None
    moon: LongitudeFormsOut | None = None
    lagna: LongitudeFormsOut | None = None


class SpecialLagnaPlacementOut(BaseModel):
    id: int
    name: str
    abbreviation: str
    longitude: float
    rasi: int
    rasi_name: str
    degrees_in_rasi: float
    dms: str
    rasi_dm: str
    signifies: str | None = Field(
        None, description="Bhaava Lagna carries none; the book defines it for completeness"
    )
    degrees_per_minute: float | None = Field(
        None, description="Null for Sree Lagna, which is not time-based"
    )


class SpecialLagnaComputeOut(BaseModel):
    input: SpecialLagnaEchoOut
    special_lagnas: list[SpecialLagnaPlacementOut]


class SpecialLagnaRuleOut(BaseModel):
    id: int
    name: str
    abbreviation: str
    degrees_per_minute: float | None = None
    one_rasi_per_minutes: float | None = None
    signifies: str | None = None
    derived_from: str


class SpecialLagnaRulesOut(BaseModel):
    lagnas: list[SpecialLagnaRuleOut]
    birthtime_sensitivity_per_minute: dict[str, float] = Field(
        ..., description="Degrees moved per minute of birthtime error"
    )
    note: str
