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
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    BUDHA_AADITYA_CHART_NOTE,
    COMBUSTION_WEAKENS_YOGA,
    GRAHA_NAMES,
    RASI_NAMES,
    RAVI_YOGAS,
    Graha,
)

_SPEC = {entry["key"]: entry for entry in RAVI_YOGAS}


def _house_sign(sun_sign: int, house: int) -> int:
    """Inclusive: the 1st house from a sign is that sign."""
    return (sun_sign + house - 1) % 12


def _qualifying(data: YogaInput, sun_sign: int, house: int) -> tuple[int, ...]:
    """Grahas in a house from the Sun that a "planet other than Moon" admits.

    The Sun is excluded from his own houses for the same reason the Moon is
    named: a yoga about what accompanies the Sun cannot be formed by the Sun.
    He can only ever occupy the 1st from himself, so this bites for
    Budha-Aaditya alone.
    """
    target = _house_sign(sun_sign, house)
    excluded = {int(Graha.MOON), int(Graha.SUN)}
    return tuple(
        g for g in data.considered()
        if int(g) not in excluded and data.sign_of(g) == target
    )


def _absent_reason(data: YogaInput, sun_sign: int, houses: tuple[int, ...]) -> str:
    parts = [
        f"the {house}{'nd' if house == 2 else 'th'} from Sun is "
        f"{RASI_NAMES[_house_sign(sun_sign, house)]} and holds no qualifying planet"
        for house in houses
    ]
    return "; ".join(parts)


def _no_sun() -> YogaVerdict:
    return YogaVerdict(
        key="", name="", present=False,
        reason="the Sun has no placement; every Ravi yoga is read from him",
    )


def _make_house_detector(key: str):
    spec = _SPEC[key]
    houses = tuple(spec["houses_from_sun"])

    def detect(data: YogaInput) -> YogaVerdict:
        sun_sign = data.sign_of(Graha.SUN)
        if sun_sign is None:
            return YogaVerdict(key=key, name=spec["name"], present=False,
                               reason=_no_sun().reason)
        found: dict[int, int] = {}
        per_house = {}
        for house in houses:
            grahas = _qualifying(data, sun_sign, house)
            per_house[house] = grahas
            for graha in grahas:
                found[int(graha)] = house
        # §11.2.3 needs **both** houses occupied; §11.2.1 and §11.2.2 need one.
        present = all(per_house[house] for house in houses)
        if present:
            named = ", ".join(GRAHA_NAMES[g] for g in sorted(found))
            where = " and ".join(
                f"the {h}{'nd' if h == 2 else 'th'} from Sun "
                f"({RASI_NAMES[_house_sign(sun_sign, h)]})"
                for h in houses
            )
            reason = f"{named} in {where}"
        else:
            missing = tuple(h for h in houses if not per_house[h])
            reason = _absent_reason(data, sun_sign, missing)
        return YogaVerdict(
            key=key, name=spec["name"], present=present,
            reason=reason,
            participants=tuple(sorted(found)) if present else (),
            houses=found if present else {},
        )

    return detect


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
        detect=_make_house_detector(_key),
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
