"""Calculation settings.

Every knob that Jagannatha Hora exposes under Preferences has a counterpart
here.  The defaults are chosen to reproduce JHora 8.0's factory settings so
that a bare request matches the benchmark without tuning.

Anything whose JHora default has not yet been confirmed empirically is tagged
``PARITY`` in a comment and tracked in docs/parity.md.
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from hora.core.names import NameScheme


class Ayanamsa(str, Enum):
    LAHIRI = "lahiri"
    LAHIRI_1940 = "lahiri_1940"
    LAHIRI_ICRC = "lahiri_icrc"
    RAMAN = "raman"
    KRISHNAMURTI = "krishnamurti"
    KRISHNAMURTI_VP291 = "krishnamurti_vp291"
    YUKTESHWAR = "yukteshwar"
    JN_BHASIN = "jn_bhasin"
    FAGAN_BRADLEY = "fagan_bradley"
    TRUE_CITRA = "true_citra"
    TRUE_REVATI = "true_revati"
    TRUE_PUSHYA = "true_pushya"
    TRUE_MULA = "true_mula"
    SURYASIDDHANTA = "suryasiddhanta"
    ARYABHATA = "aryabhata"
    SS_CITRA = "ss_citra"
    SS_REVATI = "ss_revati"
    SASSANIAN = "sassanian"
    USHA_SHASHI = "usha_shashi"
    DEVA_DATTA = "deva_datta"
    TROPICAL = "tropical"
    CUSTOM = "custom"


class NodeType(str, Enum):
    """Whether Rahu/Ketu use the mean or the osculating (true) lunar node."""

    MEAN = "mean"
    TRUE = "true"


class KetuMode(str, Enum):
    """How Ketu's longitude is derived."""

    OPPOSITE_RAHU = "opposite_rahu"
    TRUE_SOUTH_NODE = "true_south_node"


class SunriseMode(str, Enum):
    """Sunrise definitions.

    ``DISC_UPPER_LIMB`` is the default, because §5.5 comment (3) of the book
    recommends it outright: "the time when the upper tip of the visual disk
    representing Sun appears to be rising … The latter approach is recommended."

    ``TRADITIONAL_HINDU`` is Swiss Ephemeris's ``SE_BIT_HINDU_RISING`` — centre
    of the disc, no refraction, ecliptic latitude disregarded — and is what
    PyJHora uses. It was the default until chapter 5 was read; the book
    outranks PyJHora, so it no longer is. See docs/book-deviations.md D-10.
    """

    #: SE_BIT_HINDU_RISING. Disc centre, no refraction, no ecliptic latitude.
    TRADITIONAL_HINDU = "traditional_hindu"
    #: Centre of the solar disc on the true horizon, with refraction.
    DISC_CENTER = "disc_center"
    #: Upper limb of the disc on the true horizon, with refraction (IAU standard).
    DISC_UPPER_LIMB = "disc_upper_limb"
    #: Centre of the disc on the true horizon, ignoring refraction (geometric).
    GEOMETRIC_CENTER = "geometric_center"


class UpagrahaRisePoint(str, Enum):
    """Where inside its ruling graha's part a time-based upagraha rises.

    Book §4.3 puts them at the middle of the part, except Maandi which rises at
    the beginning. Footnote 9 records that "some scholars suggest that Kaala
    rises at the beginning of Sun's part. The same thing applies to others."
    """

    #: The book's main text: middle of the part (Maandi still at the beginning).
    MIDDLE = "middle"
    #: Footnote 9's variant: all of them at the beginning of the part.
    BEGINNING = "beginning"


class HouseSystem(str, Enum):
    """Bhava (house) division schemes. JHora offers 17."""

    EQUAL_LAGNA = "equal_lagna"          # whole-sign-from-lagna-degree (JHora "Equal housing")
    WHOLE_SIGN = "whole_sign"            # rasi = bhava (Parashari default for chart drawing)
    SRIPATI = "sripati"
    KP_PLACIDUS = "kp"
    PLACIDUS = "placidus"
    KOCH = "koch"
    PORPHYRY = "porphyry"
    REGIOMONTANUS = "regiomontanus"
    CAMPANUS = "campanus"
    VEHLOW_EQUAL = "vehlow"
    AXIAL_ROTATION = "axial_rotation"
    HORIZONTAL = "horizontal"
    TOPOCENTRIC = "topocentric"
    ALCABITUS = "alcabitus"
    MORINUS = "morinus"
    KN_RAO = "kn_rao"
    PVR = "pvr"


class NodeDirection(str, Enum):
    """Whether the nodes are reported with their (always retrograde) motion."""

    RETROGRADE = "retrograde"
    DIRECT = "direct"


class MonthReckoning(str, Enum):
    """How a lunar month is bounded.

    Both are computed and reported; no default is chosen, because the two
    conventions disagree on the month name for roughly a third of the year
    around an adhika maasa.
    """

    #: Month runs Amavasya to Amavasya (South Indian). Chapter 1's convention.
    AMANTA = "amanta"
    #: Month runs Purnima to Purnima (North Indian).
    PURNIMANTA = "purnimanta"


class DashaYearLength(str, Enum):
    """Length of a 'year' when converting dasha durations to calendar time."""

    SIDEREAL = "sidereal"      # 365.256360417 days
    TROPICAL = "tropical"      # 365.242190 days
    CIVIL = "civil"            # 365.25 days
    SAVANA = "savana"          # 360 days


class Settings(BaseModel):
    """A complete calculation configuration.

    Instances are hashable-by-value and cheap to pass around; the ephemeris
    layer keys its Swiss Ephemeris mode switches off these fields.
    """

    model_config = {"frozen": True}

    ayanamsa: Ayanamsa = Ayanamsa.LAHIRI
    #: Only consulted when ``ayanamsa`` is CUSTOM; degrees at J2000.
    custom_ayanamsa_deg: float | None = None

    node_type: NodeType = NodeType.TRUE
    ketu_mode: KetuMode = KetuMode.OPPOSITE_RAHU
    node_direction: NodeDirection = NodeDirection.RETROGRADE

    #: Topocentric (observer-corrected) rather than geocentric positions.
    topocentric: bool = False
    #: Apparent positions (light-time, aberration, deflection) vs true
    #: geometric positions. Sets SEFLG_TRUEPOS when False.
    #:
    #: Defaults to true positions, the traditional convention: classical
    #: siddhantic astronomy computes the true geocentric longitude and knows
    #: nothing of aberration, which is a telescope-era optical correction.
    #: This also reproduces PyJHora exactly on every body.
    #: PARITY: confirmed at tier 2 (PyJHora), not yet against JHora itself.
    apparent_positions: bool = False

    sunrise_mode: SunriseMode = SunriseMode.DISC_UPPER_LIMB
    #: Rise point for the six time-based upagrahas (book section 4.3).
    upagraha_rise_point: UpagrahaRisePoint = UpagrahaRisePoint.MIDDLE
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN

    #: Include Uranus, Neptune and Pluto in chart output.
    include_outer_planets: bool = False
    #: Give Rahu and Ketu the 5th/9th special aspects.
    rahu_ketu_aspects: bool = False

    dasha_year_length: DashaYearLength = DashaYearLength.SIDEREAL

    #: Language for name fields in API responses.
    language: str = Field(default="en", pattern=r"^[a-z]{2}$")
    #: Emit Sanskrit rather than English names for signs and planets.
    sanskrit_names: bool = False
    #: Transliteration scheme for tithi/nakshatra/yoga/karana/masa names.
    #: Display only — integer indices remain the stable contract.
    name_scheme: NameScheme = NameScheme.BOOK


DEFAULT_SETTINGS = Settings()


#: Mapping from our ayanamsa enum onto Swiss Ephemeris sidereal mode constants.
#: Populated lazily in ephemeris.swiss to avoid importing swisseph here.
AYANAMSA_SWE_NAME: dict[Ayanamsa, str] = {
    Ayanamsa.LAHIRI: "SIDM_LAHIRI",
    Ayanamsa.LAHIRI_1940: "SIDM_LAHIRI_1940",
    Ayanamsa.LAHIRI_ICRC: "SIDM_LAHIRI_ICRC",
    Ayanamsa.RAMAN: "SIDM_RAMAN",
    Ayanamsa.KRISHNAMURTI: "SIDM_KRISHNAMURTI",
    Ayanamsa.KRISHNAMURTI_VP291: "SIDM_KRISHNAMURTI_VP291",
    Ayanamsa.YUKTESHWAR: "SIDM_YUKTESHWAR",
    Ayanamsa.JN_BHASIN: "SIDM_JN_BHASIN",
    Ayanamsa.FAGAN_BRADLEY: "SIDM_FAGAN_BRADLEY",
    Ayanamsa.TRUE_CITRA: "SIDM_TRUE_CITRA",
    Ayanamsa.TRUE_REVATI: "SIDM_TRUE_REVATI",
    Ayanamsa.TRUE_PUSHYA: "SIDM_TRUE_PUSHYA",
    Ayanamsa.TRUE_MULA: "SIDM_TRUE_MULA",
    Ayanamsa.SURYASIDDHANTA: "SIDM_SURYASIDDHANTA",
    Ayanamsa.ARYABHATA: "SIDM_ARYABHATA",
    Ayanamsa.SS_CITRA: "SIDM_SS_CITRA",
    Ayanamsa.SS_REVATI: "SIDM_SS_REVATI",
    Ayanamsa.SASSANIAN: "SIDM_SASSANIAN",
    Ayanamsa.USHA_SHASHI: "SIDM_USHASHASHI",
    Ayanamsa.DEVA_DATTA: "SIDM_DJWHAL_KHUL",  # PARITY: JHora "Deva-datta" mapping unverified
}
