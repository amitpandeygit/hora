"""Response models — the API's published contract.

Before these existed every endpoint was declared as an untyped ``object``: the
OpenAPI document told a client nothing, no field was guaranteed, and a key
could disappear without anything failing.

Each model mirrors exactly what the service already returned, so adding them
changed no response. `tests/unit/test_golden_api.py` proves that, and will
fail on any future drift.

Conventions:

* Longitudes are decimal degrees from 0 Aries. Every one is accompanied by the
  human-readable forms (``dms``, ``sign_dm``, ``rasi_dm``) so a client never has
  to re-derive them.
* ``None`` means the book gives no value — Mars has no abode, the nodes have no
  deep-exaltation degree. It never means "not computed".
* Integer ids are the stable identity; names are display only and may change
  with ``name_scheme``.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from hora.core.settings import Settings

# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------


class PlaceOut(BaseModel):
    name: str | None = None
    latitude: float
    longitude: float
    altitude: float


class InputEcho(BaseModel):
    """The request as the engine resolved it — echoed so a result is reproducible."""

    local_time: str
    utc: str
    utc_offset_hours: float
    timezone: str | None = None
    julian_day_ut: float
    place: PlaceOut


class Angle(BaseModel):
    deg: float
    dms: str


class SignPosition(BaseModel):
    """A longitude, with its sign and every notation the book uses."""

    longitude: float
    rasi: int = Field(..., description="0 = Aries")
    rasi_name: str
    degrees_in_rasi: float
    dms: str = Field(..., description="Degrees-minutes-seconds within the rasi")
    sign_dm: str = Field(..., description='Signs completed, e.g. "7s 11d 37\'"')
    rasi_dm: str = Field(..., description='Rasi-relative, e.g. "25 Li 31"')


class CalculationEnvelope(BaseModel):
    """The header every calculation response carries.

    ``input`` is the request as the engine resolved it — zone applied, Julian
    Day computed — and ``settings`` is the configuration actually used. Together
    they make a response reproducible from its own body, without the caller
    having to remember what they sent or which defaults were in force.

    Reference and content endpoints do not carry it: they publish static tables
    and have no input to echo.
    """

    input: InputEcho
    settings: Settings


# --------------------------------------------------------------------------
# Rasi chart
# --------------------------------------------------------------------------


class LagnaOut(SignPosition):
    midheaven: float


class GrahaOut(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    speed: float = Field(..., description="Degrees per day; negative is retrograde")
    retrograde: bool
    rasi: int
    rasi_name: str
    degrees_in_rasi: float
    dms: str
    sign_dm: str
    rasi_dm: str
    nakshatra: int
    nakshatra_name: str
    pada: int
    house: int
    house_labels: list[str] = Field(
        ..., description="kendra, trikona, dusthana and the rest"
    )
    dignity: str
    combust: bool
    sun_separation: float
    lord_of_houses: list[int]


class BhavaOut(BaseModel):
    house: int
    start: float
    middle: float
    end: float
    rasi: int
    rasi_name: str


class PlanetaryWarOut(BaseModel):
    a: int
    b: int
    winner: int


class RasiChartOut(CalculationEnvelope):
    ayanamsa: Angle
    lagna: LagnaOut
    grahas: list[GrahaOut]
    bhavas: list[BhavaOut]
    planetary_war: list[PlanetaryWarOut]


# --------------------------------------------------------------------------
# Divisional charts
# --------------------------------------------------------------------------


class VargaLagnaOut(BaseModel):
    rasi: int
    rasi_name: str
    longitude: float


class VargaGrahaOut(BaseModel):
    id: int
    name: str
    rasi: int
    rasi_name: str
    longitude: float
    house: int
    retrograde: bool


class VargaChartOut(BaseModel):
    chart: str
    lagna: VargaLagnaOut
    grahas: list[VargaGrahaOut]


class VargaResponse(CalculationEnvelope):
    charts: dict[str, VargaChartOut] = Field(..., description="Keyed by varga code")


# --------------------------------------------------------------------------
# Upagrahas
# --------------------------------------------------------------------------


class UpagrahaPeriodOut(BaseModel):
    starts: str
    ends: str
    part_length_hours: float


class UpagrahaOut(SignPosition):
    id: int
    name: str
    house: int
    group: str = Field(..., description='"sun_based" or "time_based"')
    part_lord: str | None = Field(None, description="Time-based upagrahas only")
    part_index: int | None = Field(None, description="Which of the eight parts, 1-8")
    rises_at: str | None = None
    nature_like: str | None = Field(
        None, description='The graha it is "similar to" (section 4.3)'
    )


class UpagrahaResponse(CalculationEnvelope):
    born_at: str = Field(..., description='"day" or "night"')
    vaara: str
    vaara_opened_at: str = Field(..., description="The vaara turns at sunrise")
    period: UpagrahaPeriodOut
    part_lords: list[str | None] = Field(
        ..., description="Eight entries; one is null, the lord-less part"
    )
    upagrahas: list[UpagrahaOut]
    note: str


class SpecialLagnaOut(SignPosition):
    id: int
    name: str
    abbreviation: str = Field(..., description="BL, HL, GL or SL")
    house: int
    signifies: str | None = Field(
        None, description="Bhaava Lagna carries none; the book defines it for completeness"
    )
    degrees_per_minute: float | None = Field(
        None, description="Null for Sree Lagna, which is not time-based"
    )


class SpecialLagnaResponse(CalculationEnvelope):
    sunrise: str = Field(..., description="The sunrise that opened the current vaara")
    sun_at_sunrise: SignPosition
    minutes_since_sunrise: float
    lagna: SignPosition
    special_lagnas: list[SpecialLagnaOut]
    note: str


# --------------------------------------------------------------------------
# Panchanga
# --------------------------------------------------------------------------


class PakshaOut(BaseModel):
    index: int
    name: str


class ElementOut(BaseModel):
    """One limb of the panchanga, with the time it ends.

    ``lord`` is null on every limb but the tithi: the book gives lords in
    Table 3 for tithis and for nothing else. The keys are always present, so a
    client never has to test for their existence.
    """

    number: int = Field(..., description="1-based, as almanacs print it")
    index: int = Field(..., description="0-based")
    name: str
    name_standard: str
    ends_local: str | None = None
    ends_jd: float | None = None
    lord: int | None = Field(None, description="Tithis only")
    lord_name: str | None = Field(None, description="Tithis only")


class HoraOut(BaseModel):
    index: int
    lord: int
    lord_name: str
    start_local: str
    end_local: str


class LunarMonthOut(BaseModel):
    reckoning: str
    index: int
    name: str
    paksha: int
    paksha_name: str
    is_adhika: bool
    starts_local: str
    ends_local: str
    conjunction_rasi: int
    conjunction_rasi_name: str


class SolarDateOut(BaseModel):
    month: int
    month_name: str
    day: int


class PanchangaResponse(CalculationEnvelope):
    date_local: str
    vaara: dict[str, object]
    sunrise: str
    sunset: str
    next_sunrise: str
    moonrise: str | None = None
    moonset: str | None = None
    day_length_hours: float
    night_length_hours: float
    tithi: list[ElementOut]
    nakshatra: list[ElementOut]
    yoga: list[ElementOut]
    karana: list[ElementOut]
    paksha: PakshaOut
    hora: HoraOut
    lunar_month: dict[str, LunarMonthOut] = Field(
        ..., description="Keyed 'amanta' and 'purnimanta'; neither is the default"
    )
    solar_date: SolarDateOut
    abhijit_active: bool
    sun_longitude: float
    moon_longitude: float


# --------------------------------------------------------------------------
# Dashas
# --------------------------------------------------------------------------


class DashaPeriodOut(BaseModel):
    lord: int
    lord_name: str
    level: int = Field(..., description="1 = mahadasha, 2 = antardasha")
    start: str
    end: str
    start_jd: float
    end_jd: float
    duration_days: float
    children: list[DashaPeriodOut] = []


class DashaSystemOut(BaseModel):
    key: str
    name: str
    #: Whole years for every system implemented so far, but a spec may carry
    #: fractional years, so the int is not coerced away.
    total_years: int | float


class DashaBalanceOut(BaseModel):
    lord: int
    years: float


class RunningPeriodOut(BaseModel):
    level: int
    lord: int
    lord_name: str


class DashaResponse(CalculationEnvelope):
    system: DashaSystemOut
    moon_longitude: float
    balance_at_birth: DashaBalanceOut
    year_length: str
    periods: list[DashaPeriodOut]
    running: list[RunningPeriodOut]


class DashaCatalogOut(BaseModel):
    nakshatra_dashas: list[DashaSystemOut]


# --------------------------------------------------------------------------
# Ephemeris
# --------------------------------------------------------------------------


class EphemerisPositionOut(SignPosition):
    id: int
    name: str
    latitude: float
    distance_au: float
    speed: float
    retrograde: bool


class EphemerisResponse(CalculationEnvelope):
    julian_day_ut: float
    utc: str
    ayanamsa: Angle
    positions: list[EphemerisPositionOut]


# --------------------------------------------------------------------------
# Meta
# --------------------------------------------------------------------------


class HealthOut(BaseModel):
    status: str
    version: str


DashaPeriodOut.model_rebuild()

