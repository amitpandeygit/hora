"""§11.3 Chandra yogas — the lunar combinations.

Four of the six mirror a Ravi yoga exactly, with the references swapped:
Sunaphaa is Vesi with Moon and Sun exchanged, and so on down to
Chandra-Mangala against Budha-Aaditya. Those four use the shared detectors, so
the mirror cannot drift.

Two do not mirror anything:

* **Kemadruma** is the first *negative* yoga, and the first that reads a house
  from the lagna rather than from a graha. Without a lagna it is unanswerable,
  and it says so rather than guessing.
* **Adhi** needs to know which grahas are benefic, which §3.2.2 makes
  conditional for the Moon and Mercury. Its printed example does not satisfy
  its printed rule; the rule is followed. See docs/book-deviations.md D-28.
"""
from __future__ import annotations

from hora.charts.planetary_yogas._shared import (
    house_sign,
    make_conjunction_detector,
    make_house_detector,
    ordinal,
    qualifying,
)
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    CHANDRA_YOGAS,
    GRAHA_NAMES,
    KENDRA,
    RASI_NAMES,
    Graha,
)

_SPEC = {entry["key"]: entry for entry in CHANDRA_YOGAS}

#: §11.3.6's houses, and §11.3.4's.
_ADHI_HOUSES = (6, 7, 8)


def _detect_kemadruma(data: YogaInput) -> YogaVerdict:
    """§11.3.4, in two clauses that must both hold.

    "If there are **no** planets other than Sun in the 1st, 2nd and 12th
    houses from Moon **and** if there are **no** planets other than Moon in
    the quadrants from lagna, this bad yoga is present."

    The Sun is exempt in the first clause and the Moon in the second, so the
    Moon sitting in a quadrant does not break it — which is what lets the
    book's own example hold with the Moon in Virgo and Taurus rising.
    """
    key, name = "kemadruma", _SPEC["kemadruma"]["name"]
    moon_sign = data.sign_of(Graha.MOON)
    if moon_sign is None:
        return YogaVerdict(key=key, name=name, present=False,
                           reason="Moon has no placement; this yoga is read from her")
    if data.lagna_rasi is None:
        return YogaVerdict(
            key=key, name=name, present=False,
            reason=("no lagna was supplied, and the second clause counts "
                    "quadrants from lagna; this yoga cannot be decided"),
        )

    around_moon: dict[int, tuple[int, ...]] = {}
    for house in _SPEC["kemadruma"]["houses_from_moon"]:
        around_moon[house] = qualifying(
            data, Graha.MOON, moon_sign, house, Graha.SUN)
    occupied_near_moon = {h: g for h, g in around_moon.items() if g}

    in_quadrants: dict[int, tuple[int, ...]] = {}
    for house in KENDRA:
        target = house_sign(data.lagna_rasi, house)
        grahas = tuple(
            g for g in data.considered()
            if int(g) != int(Graha.MOON) and data.sign_of(g) == target
        )
        if grahas:
            in_quadrants[house] = grahas

    if occupied_near_moon or in_quadrants:
        parts = []
        for house, grahas in sorted(occupied_near_moon.items()):
            named = ", ".join(GRAHA_NAMES[g] for g in grahas)
            parts.append(f"{named} in the {ordinal(house)} from Moon")
        for house, grahas in sorted(in_quadrants.items()):
            named = ", ".join(GRAHA_NAMES[g] for g in grahas)
            parts.append(f"{named} in the {ordinal(house)} from lagna")
        return YogaVerdict(key=key, name=name, present=False,
                           reason="; ".join(parts))

    return YogaVerdict(
        key=key, name=name, present=True,
        reason=(
            f"the 1st, 2nd and 12th from Moon "
            f"({', '.join(RASI_NAMES[house_sign(moon_sign, h)] for h in (1, 2, 12))}) "
            f"hold no planet but the Sun, and the quadrants from lagna "
            f"({', '.join(RASI_NAMES[house_sign(data.lagna_rasi, h)] for h in KENDRA)}) "
            f"hold no planet but the Moon"
        ),
    )


def _detect_adhi(data: YogaInput) -> YogaVerdict:
    """§11.3.6: "If the natural benefics occupy 6th, 7th and 8th from Moon".

    Read as: every natural benefic is in one of those three houses, and at
    least one is there. A benefic elsewhere breaks it — which is what "the
    natural benefics occupy" says, as against "a benefic occupies".

    The Moon is excluded from her own test. A waxing Moon is a natural benefic
    (§3.2.2) and can only ever occupy the 1st from herself, so counting her
    would make the yoga impossible for every bright-half birth.

    Whether all three houses must be occupied is not settled by the book; its
    own example, once repaired, leaves the 8th empty. See OI-75.
    """
    key, name = "adhi", _SPEC["adhi"]["name"]
    moon_sign = data.sign_of(Graha.MOON)
    if moon_sign is None:
        return YogaVerdict(key=key, name=name, present=False,
                           reason="Moon has no placement; this yoga is read from her")

    benefics, undecidable = data.benefics()
    benefics = tuple(g for g in benefics if int(g) != int(Graha.MOON))
    undecidable = tuple(g for g in undecidable if int(g) != int(Graha.MOON))
    if not benefics:
        reason = "no natural benefic is placed"
        if undecidable:
            named = ", ".join(GRAHA_NAMES[g] for g in undecidable)
            reason += f"; the nature of {named} could not be judged"
        return YogaVerdict(key=key, name=name, present=False, reason=reason)

    targets = {house_sign(moon_sign, h): h for h in _ADHI_HOUSES}
    inside = {int(g): targets[data.rasis[g]]
              for g in benefics if data.rasis[g] in targets}
    outside = tuple(g for g in benefics if data.rasis[g] not in targets)

    if outside or not inside:
        if outside:
            named = ", ".join(GRAHA_NAMES[g] for g in outside)
            verb = "is a natural benefic" if len(outside) == 1 else "are natural benefics"
            reason = f"{named} {verb} outside the 6th, 7th and 8th from Moon"
        else:
            reason = "no natural benefic is in the 6th, 7th or 8th from Moon"
        return YogaVerdict(key=key, name=name, present=False, reason=reason)

    qualifiers: tuple[str, ...] = ()
    if undecidable:
        named = ", ".join(GRAHA_NAMES[g] for g in undecidable)
        qualifiers = (
            (f"the nature of {named} could not be judged from the input, so "
             f"this verdict assumes it is not a benefic"),
        )
    named = ", ".join(GRAHA_NAMES[g] for g in sorted(inside))
    return YogaVerdict(
        key=key, name=name, present=True,
        reason=(f"{named} — every placed natural benefic — occupy the "
                f"6th, 7th or 8th from Moon"),
        participants=tuple(sorted(inside)),
        houses=inside,
        qualifiers=qualifiers,
    )


for _key in ("sunaphaa", "anaphaa", "duradhara"):
    register(YogaSpec(
        key=_key,
        name=_SPEC[_key]["name"],
        aliases=tuple(_SPEC[_key]["aliases"]),
        section=_SPEC[_key]["section"],
        group="chandra",
        definition=_SPEC[_key]["definition"],
        detect=make_house_detector(
            _key, _SPEC[_key]["name"], reference=Graha.MOON,
            excluded=Graha.SUN,
            houses=tuple(_SPEC[_key]["houses_from_moon"])),
        implies=("sunaphaa", "anaphaa") if _key == "duradhara" else (),
    ))

register(YogaSpec(
    key="kemadruma", name=_SPEC["kemadruma"]["name"], aliases=(),
    section="11.3.4", group="chandra",
    definition=_SPEC["kemadruma"]["definition"], detect=_detect_kemadruma,
))

register(YogaSpec(
    key="chandra_mangala", name=_SPEC["chandra_mangala"]["name"], aliases=(),
    section="11.3.5", group="chandra",
    definition=_SPEC["chandra_mangala"]["definition"],
    detect=make_conjunction_detector(
        "chandra_mangala", _SPEC["chandra_mangala"]["name"],
        first=Graha.MOON, second=Graha.MARS),
))

register(YogaSpec(
    key="adhi", name=_SPEC["adhi"]["name"], aliases=(),
    section="11.3.6", group="chandra",
    definition=_SPEC["adhi"]["definition"], detect=_detect_adhi,
))
