"""§11.2 Ravi yogas — the solar combinations.

Four yogas, all read from the Sun. Three of them turn on one phrase:

    "If there is **a planet other than Moon** in the 2nd house from Sun..."

Two things in that phrase decide how often the yoga fires. The Moon is
excluded outright. Whether Rahu and Ketu count as "a planet" the chapter never
says, so it is a parameter — `include_nodes`, off by default — and the verdict
names which grahas were considered. See docs/open-items.md OI-73.
"""
from __future__ import annotations

from hora.charts.dignity import combustion
from hora.charts.planetary_yogas._shared import (
    make_house_detector,
)
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    BUDHA_AADITYA_CHART_NOTE,
    COMBUSTION_WEAKENS_YOGA,
    RASI_NAMES,
    RAVI_YOGAS,
    Graha,
)

_SPEC = {entry["key"]: entry for entry in RAVI_YOGAS}


def _detect_budha_aaditya(data: YogaInput) -> YogaVerdict:
    """§11.2.4: "If Sun and Mercury are together (in one sign)".

    Combustion is reported as a qualifier, never as a veto: the note says a
    combust yoga loses **some** of its power, not that it fails to form.
    """
    key = "budha_aaditya"
    spec = _SPEC[key]
    sun_sign = data.sign_of(Graha.SUN)
    mercury_sign = data.sign_of(Graha.MERCURY)
    if sun_sign is None or mercury_sign is None:
        missing = "Sun" if sun_sign is None else "Mercury"
        return YogaVerdict(key=key, name=spec["name"], present=False,
                           reason=f"{missing} has no placement")
    if sun_sign != mercury_sign:
        return YogaVerdict(
            key=key, name=spec["name"], present=False,
            reason=(f"Sun is in {RASI_NAMES[sun_sign]} and Mercury in "
                    f"{RASI_NAMES[mercury_sign]}; they are not together"),
        )

    qualifiers: tuple[str, ...] = ()
    if _mercury_is_combust(data):
        qualifiers = (COMBUSTION_WEAKENS_YOGA,)
    if data.chart != "D1":
        qualifiers = (*qualifiers, BUDHA_AADITYA_CHART_NOTE)

    return YogaVerdict(
        key=key, name=spec["name"], present=True,
        reason=(f"Sun and Mercury are together in {RASI_NAMES[sun_sign]}"),
        participants=(int(Graha.SUN), int(Graha.MERCURY)),
        houses={int(Graha.SUN): 1, int(Graha.MERCURY): 1},
        qualifiers=qualifiers,
    )


def _mercury_is_combust(data: YogaInput) -> bool:
    """Whether Mercury is combust, when the caller supplied enough to say.

    Combustion needs real longitudes and the retrograde flag, so it is
    unanswerable from signs alone. Returning False there is *not* a finding
    that Mercury is uncombust — the qualifier is simply absent, and
    `qualifiers_available` on the response says so.
    """
    if not data.positions:
        return False
    needed = (int(Graha.SUN), int(Graha.MERCURY))
    if any(g not in data.positions for g in needed):
        return False
    return bool(combustion(int(Graha.MERCURY), data.positions).combust)


for _key in ("vesi", "vosi", "ubhayachara"):
    register(YogaSpec(
        key=_key,
        name=_SPEC[_key]["name"],
        aliases=tuple(_SPEC[_key]["aliases"]),
        section=_SPEC[_key]["section"],
        group="ravi",
        definition=_SPEC[_key]["definition"],
        detect=make_house_detector(
            _key, _SPEC[_key]["name"], reference=Graha.SUN,
            excluded=Graha.MOON,
            houses=tuple(_SPEC[_key]["houses_from_sun"])),
        implies=("vesi", "vosi") if _key == "ubhayachara" else (),
    ))

register(YogaSpec(
    key="budha_aaditya",
    name=_SPEC["budha_aaditya"]["name"],
    aliases=tuple(_SPEC["budha_aaditya"]["aliases"]),
    section=_SPEC["budha_aaditya"]["section"],
    group="ravi",
    definition=_SPEC["budha_aaditya"]["definition"],
    detect=_detect_budha_aaditya,
))
