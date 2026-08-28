"""§11.9 — the Dhana yogas.

"Dhana means wealth. Dhana yogas are combinations that give one abundant
riches."

The section prints a Basic Principle and then twelve lagna-specific entries,
each carrying **two** independent combinations — the second introduced with
"then *also* one becomes very rich". They are registered as twenty-four, so a
caller is told which of the two a chart has rather than only that it has one.

A combination belongs to one lagna. On any other lagna the verdict says which
lagna it is for and which the chart has, rather than reporting a bare absence
that would read as a finding.

Checked against all twelve rather than assumed — see `DHANA_STRUCTURE`:

- every first combination puts the **5th lord** in the 5th house;
- the planets it wants in the 11th always include the **11th lord**;
- every second combination puts the **lagna lord** in lagna.

Entry (12), for Pisces, is printed "If Moon is in the 5th house and in the
11th house" and names no planet for the 11th, so no chart can satisfy it. It
is reported undecidable, never absent. See docs/book-deviations.md D-37.
"""
from __future__ import annotations

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import house_sign
from hora.charts.planetary_yogas.popular import houses_of, in_exaltation
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    DHANA_EXALTED_IN_SECOND,
    DHANA_PARASARA_NOTE,
    DHANA_PISCES_LIKELY_MISSING,
    DHANA_YOGAS,
    GRAHA_NAMES,
    RASI_ABBR,
    RASI_NAMES,
    Graha,
)

_BY_LAGNA = {entry["lagna"]: entry for entry in DHANA_YOGAS}
_RASI = {name: index for index, name in enumerate(RASI_ABBR)}

#: §11.9's closing sentence binds every one of the twenty-four.
STRENGTH_DECIDES_MAGNITUDE = (
    f"{DHANA_PARASARA_NOTE} Strength is not computed — chapter 15's "
    f"simple-rules measure is not built — so this verdict reports the "
    f"placements only. See docs/open-items.md OI-81.")


def _spec(key: str) -> dict:
    lagna, half = key.rsplit("_", 1)
    return {"entry": _BY_LAGNA[lagna.removeprefix("dhana_")], "half": half}


def _name(entry: dict, half: str) -> str:
    which = "first" if half == "first" else "second"
    return (f"Dhana Yoga (11.9 #{entry['number']}, {which}) — "
            f"for {RASI_NAMES[_RASI[entry['lagna']]]} lagna")


def _verdict(key: str, entry: dict, half: str, present: bool, reason: str,
             **kw) -> YogaVerdict:
    qualifiers = (*tuple(kw.pop("extra_qualifiers", ())),
                  STRENGTH_DECIDES_MAGNITUDE)
    return YogaVerdict(key=key, name=_name(entry, half), present=present,
                       reason=reason, qualifiers=qualifiers, **kw)


def _wrong_lagna(key: str, entry: dict, half: str,
                 data: YogaInput) -> YogaVerdict | None:
    """A combination for one lagna, met by a chart with another."""
    wanted = _RASI[entry["lagna"]]
    if data.lagna_rasi is None:
        return YogaVerdict(
            key=key, name=_name(entry, half), present=False,
            reason=("this yoga cannot be decided: no lagna was supplied, and "
                    "section 11.9's combinations are each for one lagna"))
    if data.lagna_rasi != wanted:
        return YogaVerdict(
            key=key, name=_name(entry, half), present=False,
            reason=(f"this combination is for {RASI_NAMES[wanted]} lagna; the "
                    f"chart's lagna is {RASI_NAMES[data.lagna_rasi]}"))
    return None


def _graha(name: str) -> int:
    return int(getattr(Graha, name.upper()))


def _detect_first(key: str, entry: dict):
    def detect(data: YogaInput) -> YogaVerdict:
        wrong = _wrong_lagna(key, entry, "first", data)
        if wrong is not None:
            return wrong
        if entry.get("eleventh_is_broken"):
            return YogaVerdict(
                key=key, name=_name(entry, "first"), present=False,
                reason=(
                    "this yoga cannot be decided: section 11.9 (12) is "
                    "printed “If Moon is in the 5th house and in the 11th "
                    "house”, which names no planet for the 11th and so cannot "
                    "be satisfied by any chart. The other eleven entries all "
                    f"name the 11th lord there, which for Pisces lagna is "
                    f"{DHANA_PISCES_LIKELY_MISSING} — recorded as an "
                    f"inference and not applied. See "
                    f"docs/book-deviations.md D-37"))
        fifth = _graha(entry["fifth"])
        failures = []
        if houses_of(data, fifth) != 5:
            failures.append(f"{GRAHA_NAMES[fifth]} is not in the 5th house")
        for name in entry["eleventh"]:
            graha = _graha(name)
            if houses_of(data, graha) != 11:
                failures.append(f"{GRAHA_NAMES[graha]} is not in the 11th house")
        if failures:
            return _verdict(key, entry, "first", False, "; ".join(failures))
        inside = (fifth, *(_graha(n) for n in entry["eleventh"]))
        return _verdict(
            key, entry, "first", True,
            f"{GRAHA_NAMES[fifth]} — the 5th lord — holds the 5th, and "
            f"{', '.join(GRAHA_NAMES[_graha(n)] for n in entry['eleventh'])} "
            f"hold the 11th",
            participants=inside)
    return detect


def _detect_second(key: str, entry: dict):
    """"X occupies lagna conjoined or aspected by A and B" — X is the lagna
    lord in every one of the twelve, and every named reacher must reach."""
    def detect(data: YogaInput) -> YogaVerdict:
        wrong = _wrong_lagna(key, entry, "second", data)
        if wrong is not None:
            return wrong
        assert data.lagna_rasi is not None
        lord = _graha(entry["lagna_planet"])
        failures, how = [], []
        if houses_of(data, lord) != 1:
            failures.append(f"the lagna lord {GRAHA_NAMES[lord]} does not "
                            f"occupy lagna")
        lagna_sign = data.lagna_rasi
        for name in entry["reachers"]:
            graha = _graha(name)
            where = data.sign_of(graha)
            if where is None:
                failures.append(f"{GRAHA_NAMES[graha]} has no placement")
            elif where == lagna_sign:
                how.append(f"{GRAHA_NAMES[graha]} joins him")
            elif graha_aspects_sign(graha, where, lagna_sign):
                how.append(f"{GRAHA_NAMES[graha]} aspects him")
            else:
                failures.append(f"{GRAHA_NAMES[graha]} neither joins nor "
                                f"aspects lagna")
        if failures:
            return _verdict(key, entry, "second", False, "; ".join(failures))
        return _verdict(
            key, entry, "second", True,
            f"the lagna lord {GRAHA_NAMES[lord]} occupies lagna and "
            + ", ".join(how),
            participants=(lord, *(_graha(n) for n in entry["reachers"])))
    return detect


def _detect_exalted_in_second(data: YogaInput) -> YogaVerdict:
    """The Basic Principle's one testable rule.

    "If Moon, Mercury, Jupiter or Venus is exalted in the 2nd house, it makes
    the native very rich." Four named planets, any one of which does it.
    """
    key = "dhana_exalted_benefic_in_second"
    name = "Dhana Yoga (11.9 Basic Principle) — a benefic exalted in the 2nd"
    if data.lagna_rasi is None:
        return YogaVerdict(
            key=key, name=name, present=False,
            reason=("this yoga cannot be decided: no lagna was supplied, and "
                    "it counts the 2nd house from the ascendant"))
    second = house_sign(data.lagna_rasi, 2)
    found = [g for g in (_graha(n) for n in DHANA_EXALTED_IN_SECOND)
             if data.sign_of(g) == second and in_exaltation(data, g)]
    if not found:
        named = ", ".join(GRAHA_NAMES[_graha(n)] for n in DHANA_EXALTED_IN_SECOND)
        return YogaVerdict(
            key=key, name=name, present=False,
            reason=(f"none of {named} is exalted in the 2nd house "
                    f"({RASI_NAMES[second]})"),
            qualifiers=(STRENGTH_DECIDES_MAGNITUDE,))
    return YogaVerdict(
        key=key, name=name, present=True,
        reason=(f"{', '.join(GRAHA_NAMES[g] for g in found)} "
                f"{'is' if len(found) == 1 else 'are'} exalted in the 2nd "
                f"house ({RASI_NAMES[second]})"),
        participants=tuple(found),
        qualifiers=(STRENGTH_DECIDES_MAGNITUDE,))


for _entry in DHANA_YOGAS:
    _lagna = _entry["lagna"].lower()
    for _half, _factory in (("first", _detect_first), ("second", _detect_second)):
        _key = f"dhana_{_lagna}_{_half}"
        register(YogaSpec(
            key=_key,
            name=_name(_entry, _half),
            aliases=(),
            section="11.9",
            group="dhana",
            definition=_entry[f"{_half}_definition"],
            detect=_factory(_key, _entry),
        ))

register(YogaSpec(
    key="dhana_exalted_benefic_in_second",
    name="Dhana Yoga (11.9 Basic Principle) — a benefic exalted in the 2nd",
    aliases=(),
    section="11.9",
    group="dhana",
    definition=("If Moon, Mercury, Jupiter or Venus is exalted in the 2nd "
                "house, it makes the native very rich."),
    detect=_detect_exalted_in_second,
))
