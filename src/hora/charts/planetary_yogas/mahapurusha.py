"""§11.4 Pancha Mahapurusha yogas — the five great persons.

Five yogas, one construction: a graha in a quadrant from lagna, in a sign he
owns or is exalted in. So there is one detector, parameterised by graha, and
the sign set is **derived** from `RASI_LORD` and `EXALTATION_DEG` rather than
transcribed — §11.4 prints the signs as "in other words", which makes them the
rule's consequence and not a second rule. A test checks the derivation against
every printed list.

Two restrictions each section repeats, and both matter:

* **"does not apply from Moon"** — the first place in the book that rules a
  reference *out*. Chapter 7 made every reference relative; this is the
  exception, so `include_moon_reference` does not exist and cannot be asked for.
* **"applies mainly in rasi chart"** — the opposite of §11.2, which sends the
  Ravi yogas to D-9 and D-10. A non-rasi chart is flagged, not refused.

Like Kemadruma, these need the lagna and say so when they lack it.
"""
from __future__ import annotations

from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    EXALTATION_DEG,
    GRAHA_NAMES,
    KENDRA,
    MAHAPURUSHA_REFERENCE_RULE,
    MAHAPURUSHA_YOGAS,
    RASI_LORD,
    RASI_NAMES,
)

_SPEC = {entry["key"]: entry for entry in MAHAPURUSHA_YOGAS}


def dignified_signs(graha: int) -> tuple[int, ...]:
    """The signs a graha owns, plus the one he is exalted in.

    Mercury's set has two, not three: Virgo is both his own sign and his
    exaltation sign, so the union collapses. Every other graha here has three.
    """
    signs = {s for s in range(12) if RASI_LORD[s] == graha}
    exalted = EXALTATION_DEG.get(graha)
    if exalted is not None:
        signs.add(int(exalted // 30))
    return tuple(sorted(signs))


def _make_detector(key: str):
    spec = _SPEC[key]
    graha = spec["graha"]
    name = spec["name"]
    graha_name = GRAHA_NAMES[graha]
    signs = dignified_signs(graha)

    def detect(data: YogaInput) -> YogaVerdict:
        sign = data.sign_of(graha)
        if sign is None:
            return YogaVerdict(key=key, name=name, present=False,
                               reason=f"{graha_name} has no placement")
        if data.lagna_rasi is None:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=("no lagna was supplied, and this yoga counts quadrants "
                        "from lagna; it cannot be decided"),
            )
        house = (sign - data.lagna_rasi) % 12 + 1
        dignified = sign in signs
        in_kendra = house in KENDRA

        qualifiers: tuple[str, ...] = ()
        if data.chart != "D1":
            qualifiers = (MAHAPURUSHA_REFERENCE_RULE,)

        if dignified and in_kendra:
            kind = "own sign" if RASI_LORD[sign] == graha else "exaltation sign"
            return YogaVerdict(
                key=key, name=name, present=True,
                reason=(f"{graha_name} is in {RASI_NAMES[sign]}, his {kind}, "
                        f"and the {ordinal(house)} from lagna"),
                participants=(int(graha),),
                houses={int(graha): house},
                qualifiers=qualifiers,
            )

        missing = []
        if not dignified:
            named = ", ".join(RASI_NAMES[s] for s in signs)
            missing.append(
                f"{graha_name} is in {RASI_NAMES[sign]}, not one of {named}")
        if not in_kendra:
            missing.append(
                f"{graha_name} is in the {ordinal(house)} from lagna, not a quadrant")
        return YogaVerdict(key=key, name=name, present=False,
                           reason="; ".join(missing))

    return detect


for _key in _SPEC:
    register(YogaSpec(
        key=_key,
        name=_SPEC[_key]["name"],
        aliases=(),
        section=_SPEC[_key]["section"],
        group="mahapurusha",
        definition=(
            f"If {GRAHA_NAMES[_SPEC[_key]['graha']]} is in a quadrant in own "
            f"sign or exaltation sign, it is called {_SPEC[_key]['name'][:-5]} "
            f"yoga."
        ),
        detect=_make_detector(_key),
    ))


__all__ = ["dignified_signs", "house_sign"]
