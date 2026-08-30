"""§11.10 — the Daridra yogas.

"One experiences poverty if the following yogas (combinations) are present in
one's chart."

The section's NOTE is the first place the book defines **maraka**, and it
confirms the `MARAKA = (2, 7)` label `charts/bhava.py` had been carrying on
general classical knowledge — see OI-23, now closed.

**The maraka set is deliberately narrow.** The NOTE's third sentence reads
"Any malefics occupying 2nd and 7th or associating with 2nd and 7th lords also
become **malefics**", which is circular. In context it must be "marakas", and
that extension is computed — but presence is decided on the base set alone,
the two lords, which is the part the NOTE states without ambiguity. Eight of
the thirteen turn on marakas, and these are poverty combinations: a false
present is worse here than a false absent. Every affected verdict reports what
the wider reading would add and whether it would change the answer. See
OI-96.
"""
from __future__ import annotations

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.popular import (
    benefic_set,
    dispositor,
    houses_of,
    in_enemy_sign,
    is_debilitated,
    lord_of_house,
    occupants_of_house,
)
from hora.charts.planetary_yogas.raaja_advanced import varga_sign
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    DARIDRA_YOGAS,
    DUSTHANA,
    GRAHA_NAMES,
    MARAKA_HOUSES,
    RASI_LORD,
    RASI_NAMES,
    TRIKONA,
    Graha,
)

_SPEC = {entry["key"]: entry for entry in DARIDRA_YOGAS}

KETU = int(Graha.KETU)
MOON = int(Graha.MOON)
SUN = int(Graha.SUN)
MARS = int(Graha.MARS)
MERCURY = int(Graha.MERCURY)
SATURN = int(Graha.SATURN)


def _verdict(key: str, present: bool, reason: str, **kw) -> YogaVerdict:
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=present,
                       reason=reason,
                       qualifiers=tuple(kw.pop("extra_qualifiers", ())), **kw)


def _cannot(key: str, why: str) -> YogaVerdict:
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=False,
                       reason=f"this yoga cannot be decided: {why}")


def _needs_lagna(key: str) -> YogaVerdict:
    return _cannot(key, "no lagna was supplied, and it counts houses from the "
                        "ascendant")


# --------------------------------------------------------------------------
# Maraka, as the NOTE defines it
# --------------------------------------------------------------------------


def marakas(data: YogaInput) -> tuple[tuple[int, ...], tuple[int, ...], str]:
    """The NOTE's two readings, kept apart.

    :returns: ``(base, extension, note)`` — the 2nd and 7th lords; the planets
        the NOTE's circular third sentence would add if "malefics" is read as
        "marakas"; and a sentence naming that difference.
    """
    assert data.lagna_rasi is not None
    base = tuple(sorted({lord_of_house(data, h) for h in MARAKA_HOUSES}))
    good = benefic_set(data)
    extension: set[int] = set()
    for house in MARAKA_HOUSES:
        sign = house_sign(data.lagna_rasi, house)
        extension |= {g for g in data.rasis
                      if g not in good and data.rasis[g] == sign}
    for lord in base:
        lord_sign = data.sign_of(lord)
        if lord_sign is None:
            continue
        extension |= {
            g for g in data.rasis
            if g not in good and g != lord
            and (data.rasis[g] == lord_sign
                 or graha_aspects_sign(g, data.rasis[g], lord_sign))
        }
    extension -= set(base)
    added = tuple(sorted(extension))
    note = (
        f"marakas are taken as the 2nd and 7th lords "
        f"({', '.join(GRAHA_NAMES[g] for g in base)}), which the NOTE states "
        f"plainly. Its third sentence would add "
        + (", ".join(GRAHA_NAMES[g] for g in added) if added else "no planet")
        + " under the reading that “also become malefics” means “also become "
          "marakas” — computed, not applied. See docs/open-items.md OI-96")
    return base, added, note


def reached_by(data: YogaInput, reachers: tuple[int, ...],
               target: int) -> list[tuple[int, str]]:
    """"conjoined or aspected by" — every reacher that gets there.

    **Aspect here means graha drishti only.** The book does not say which
    drishti its unqualified "aspected" means, and nineteen of chapter 11's
    definitions use that wording. Every detector in this package reads it the
    same way, which is at least consistent, but it is a choice and not a
    quotation — see docs/open-items.md OI-113.
    """
    target_sign = data.sign_of(target)
    if target_sign is None:
        return []
    out = []
    for graha in reachers:
        if graha == target:
            continue
        where = data.sign_of(graha)
        if where is None:
            continue
        if where == target_sign:
            out.append((graha, "conjunction"))
        elif graha_aspects_sign(graha, where, target_sign):
            out.append((graha, "aspect"))
    return out


def _maraka_clause(data: YogaInput, targets: tuple[int, ...],
                   ) -> tuple[bool, str, str]:
    """The clause eight of the thirteen share: "They are conjoined or aspected
    by a maraka planet."

    **Read as "at least one of them", and that is forced.** Three readings are
    possible — one maraka reaching every named planet, each named planet
    reached by some maraka, or a maraka reaching any one of them. Combination
    (1) is reachable on 2, 8 and 12 of the twelve lagnas under those three.
    A rule Parasara states for all charts cannot be dead on ten of them, so
    the loose reading is the only viable one. See docs/open-items.md OI-98.

    Every verdict reports which named planets were reached and which were not,
    so the stricter readings are reconstructable from the answer.
    """
    base, added, note = marakas(data)
    hits = {t: reached_by(data, base, t) for t in targets}
    holds = any(hits[t] for t in targets)
    reached = [t for t in targets if hits[t]]
    missed = [t for t in targets if not hits[t]]
    if holds:
        detail = "; ".join(
            f"{GRAHA_NAMES[t]} is reached by "
            + ", ".join(f"{GRAHA_NAMES[g]} by {how}" for g, how in hits[t])
            for t in reached)
    else:
        detail = (f"no maraka conjoins or aspects "
                  f"{' or '.join(GRAHA_NAMES[t] for t in targets)}")
    extras = [note]
    if len(targets) > 1:
        extras.append(
            "section 11.10 says a maraka reaches “them”; read as at least "
            "one, which OI-98 shows is the only reading that leaves this "
            "combination reachable. Reached: "
            + (", ".join(GRAHA_NAMES[t] for t in reached) or "none")
            + "; not reached: "
            + (", ".join(GRAHA_NAMES[t] for t in missed) or "none"))
    if added and not holds:
        wider = {t: reached_by(data, added, t) for t in targets}
        if any(wider[t] for t in targets):
            extras.append(
                "under the wider reading of the NOTE this clause **would** "
                "hold, so this verdict turns on OI-96")
    return holds, detail, "\n".join(extras)


# --------------------------------------------------------------------------
# The thirteen
# --------------------------------------------------------------------------


def _exchange(key: str, other_house: int):
    """(1) and (2): the lagna lord and another lord swapped, reached by a
    maraka."""
    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return _needs_lagna(key)
        lagna_lord = lord_of_house(data, 1)
        other = lord_of_house(data, other_house)
        failures = []
        if houses_of(data, lagna_lord) != other_house:
            failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not "
                            f"in the {ordinal(other_house)}")
        if houses_of(data, other) != 1:
            failures.append(f"the {ordinal(other_house)} lord "
                            f"{GRAHA_NAMES[other]} is not in lagna")
        holds, detail, note = _maraka_clause(data, (lagna_lord, other))
        if not holds:
            failures.append(detail)
        if failures:
            return _verdict(key, False, "; ".join(failures),
                            extra_qualifiers=(note,))
        return _verdict(key, True,
                        f"the lagna lord {GRAHA_NAMES[lagna_lord]} and the "
                        f"{ordinal(other_house)} lord {GRAHA_NAMES[other]} "
                        f"have exchanged, and {detail}",
                        participants=tuple(sorted({lagna_lord, other})),
                        extra_qualifiers=(note,))
    return detect


def _detect_3(data: YogaInput) -> YogaVerdict:
    key = "daridra_ketu_and_eighth"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ketu = data.sign_of(KETU)
    moon = data.sign_of(MOON)
    failures = []
    if ketu is None:
        failures.append("Ketu has no placement")
    elif ketu != data.lagna_rasi and ketu != moon:
        failures.append("Ketu is with neither lagna nor Moon")
    lagna_lord = lord_of_house(data, 1)
    if houses_of(data, lagna_lord) != 8:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not in "
                        f"the 8th")
    holds, detail, note = _maraka_clause(data, (lagna_lord,))
    if not holds:
        failures.append(detail)
    if failures:
        return _verdict(key, False, "; ".join(failures),
                        extra_qualifiers=(note,))
    where = "lagna" if ketu == data.lagna_rasi else "Moon"
    return _verdict(key, True,
                    f"Ketu is with {where}, the lagna lord "
                    f"{GRAHA_NAMES[lagna_lord]} is in the 8th, and {detail}",
                    participants=(KETU, lagna_lord),
                    extra_qualifiers=(note,))


def _detect_4(data: YogaInput) -> YogaVerdict:
    key = "daridra_lord_with_malefic_in_dusthana"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    lagna_lord = lord_of_house(data, 1)
    house = houses_of(data, lagna_lord)
    failures = []
    with_him: list[int] = []
    if house is None:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} has no "
                        f"placement")
    elif house not in DUSTHANA:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is in the "
                        f"{ordinal(house)}, not a dusthana")
    else:
        good = benefic_set(data)
        with_him = [g for g in occupants_of_house(data, house)
                    if g not in good and g != lagna_lord]
        if not with_him:
            failures.append(f"no malefic is with the lagna lord "
                            f"{GRAHA_NAMES[lagna_lord]} in the "
                            f"{ordinal(house)}")
    second = lord_of_house(data, 2)
    if not (is_debilitated(data, second) or in_enemy_sign(data, second)):
        failures.append(f"the 2nd lord {GRAHA_NAMES[second]} is neither "
                        f"debilitated nor in an enemy's sign")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    assert house is not None
    return _verdict(key, True,
                    f"the lagna lord {GRAHA_NAMES[lagna_lord]} is in the "
                    f"{ordinal(house)} with "
                    f"{', '.join(GRAHA_NAMES[g] for g in with_him)}, and the "
                    f"2nd lord {GRAHA_NAMES[second]} is afflicted by sign",
                    participants=tuple(sorted({lagna_lord, second, *with_him})))


def _detect_5(data: YogaInput) -> YogaVerdict:
    key = "daridra_fifth_and_ninth_lords_fallen"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fifth, ninth = lord_of_house(data, 5), lord_of_house(data, 9)
    failures = []
    if houses_of(data, fifth) != 6:
        failures.append(f"the 5th lord {GRAHA_NAMES[fifth]} is not in the 6th")
    if houses_of(data, ninth) != 12:
        failures.append(f"the 9th lord {GRAHA_NAMES[ninth]} is not in the 12th")
    holds, detail, note = _maraka_clause(data, (fifth, ninth))
    if not holds:
        failures.append(detail)
    if failures:
        return _verdict(key, False, "; ".join(failures),
                        extra_qualifiers=(note,))
    return _verdict(key, True,
                    f"the 5th lord {GRAHA_NAMES[fifth]} is in the 6th, the "
                    f"9th lord {GRAHA_NAMES[ninth]} in the 12th, and {detail}",
                    participants=tuple(sorted({fifth, ninth})),
                    extra_qualifiers=(note,))


def _detect_6(data: YogaInput) -> YogaVerdict:
    """"Malefics occupy lagna **without** 9th and 10th lords" — the two lords
    must not be there."""
    key = "daridra_malefics_in_lagna"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    inside = occupants_of_house(data, 1)
    bad = [g for g in inside if g not in good]
    failures = []
    if not bad:
        failures.append("no malefic occupies lagna")
    ninth, tenth = lord_of_house(data, 9), lord_of_house(data, 10)
    present_lords = [GRAHA_NAMES[g] for g, label in
                     ((ninth, "9th"), (tenth, "10th")) if g in inside]
    if present_lords:
        failures.append(f"{', '.join(present_lords)} — a 9th or 10th lord — "
                        f"is in lagna, which this combination excludes")
    holds, detail, note = _maraka_clause(data, tuple(bad)) if bad else (
        False, "no malefic in lagna to be reached", "")
    if bad and not holds:
        failures.append(detail)
    if failures:
        return _verdict(key, False, "; ".join(failures),
                        extra_qualifiers=(note,) if note else ())
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in bad)} occupy lagna "
                    f"without the 9th or 10th lord, and {detail}",
                    participants=tuple(bad), extra_qualifiers=(note,))


def _detect_7(data: YogaInput) -> YogaVerdict:
    key = "daridra_dispositors_in_dusthanas"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    failures, found = [], []
    for house in DUSTHANA:
        lord = lord_of_house(data, house)
        disp = dispositor(data, lord)
        if disp is None:
            failures.append(f"the {ordinal(house)} lord {GRAHA_NAMES[lord]} "
                            f"has no placement, so he has no dispositor")
            continue
        where = houses_of(data, disp)
        if where not in DUSTHANA:
            failures.append(f"{GRAHA_NAMES[disp]}, dispositor of the "
                            f"{ordinal(house)} lord, is in the "
                            f"{ordinal(where)}, not a dusthana" if where else
                            f"{GRAHA_NAMES[disp]} has no placement")
            continue
        reachers = tuple(g for g in sorted(data.rasis) if g not in good)
        if not reached_by(data, reachers, disp):
            failures.append(f"no malefic conjoins or aspects "
                            f"{GRAHA_NAMES[disp]}")
            continue
        found.append(disp)
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in dict.fromkeys(found))}"
                    f" — the dispositors of the 6th, 8th and 12th lords — all "
                    f"hold dusthanas and are reached by malefics",
                    participants=tuple(dict.fromkeys(found)))


def _detect_8(data: YogaInput) -> YogaVerdict:
    key = "daridra_moons_navamsa_dispositor"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    navamsa = varga_sign(data, MOON, "D9")
    if navamsa is None:
        return _cannot(key, "it reads the Moon's navamsa sign and no "
                            "longitude was supplied for her")
    lord = int(RASI_LORD[navamsa])
    base, _, note = marakas(data)
    house = houses_of(data, lord)
    if house in MARAKA_HOUSES:
        return _verdict(key, True,
                        f"{GRAHA_NAMES[lord]}, lord of the Moon's navamsa "
                        f"sign ({RASI_NAMES[navamsa]}), occupies the "
                        f"{ordinal(house)} — a maraka house",
                        participants=(lord,), extra_qualifiers=(note,))
    with_maraka = [g for g in base
                   if g != lord and data.sign_of(g) == data.sign_of(lord)]
    if with_maraka:
        return _verdict(key, True,
                        f"{GRAHA_NAMES[lord]}, lord of the Moon's navamsa "
                        f"sign, is with the maraka "
                        f"{', '.join(GRAHA_NAMES[g] for g in with_maraka)}",
                        participants=(lord, *with_maraka),
                        extra_qualifiers=(note,))
    return _verdict(key, False,
                    f"{GRAHA_NAMES[lord]}, lord of the Moon's navamsa sign, "
                    f"is neither with a maraka nor in the 2nd or 7th",
                    extra_qualifiers=(note,))


def _detect_9(data: YogaInput) -> YogaVerdict:
    key = "daridra_both_lagna_lords"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    if data.lagna_longitude is None:
        return _cannot(key, "it reads the navamsa lagna and no lagna "
                            "longitude was supplied")
    from hora.charts.vargas import varga

    navamsa_lagna = varga(data.lagna_longitude, "D9").sign
    rasi_lord = lord_of_house(data, 1)
    navamsa_lord = int(RASI_LORD[navamsa_lagna])
    targets = tuple(dict.fromkeys((rasi_lord, navamsa_lord)))
    holds, detail, note = _maraka_clause(data, targets)
    if not holds:
        return _verdict(key, False, detail, extra_qualifiers=(note,))
    return _verdict(key, True,
                    f"the rasi lagna lord {GRAHA_NAMES[rasi_lord]} and the "
                    f"navamsa lagna lord {GRAHA_NAMES[navamsa_lord]} are both "
                    f"reached: {detail}",
                    participants=targets, extra_qualifiers=(note,))


def _detect_10(data: YogaInput) -> YogaVerdict:
    """"Benefics are in malefic houses and malefics are in benefic houses."

    No section read so far says which houses are malefic and which benefic.
    Chapter 7 names seven categories and neither term is among them, and the
    dusthanas are glossed "bad/evil houses" rather than malefic. Guessing
    would invent the rule. See docs/open-items.md OI-97.
    """
    key = "daridra_benefics_and_malefics_swapped"
    return _cannot(
        key,
        "it turns on “malefic houses” and “benefic houses”, and no section "
        "read so far defines either. See docs/open-items.md OI-97")


def _detect_11(data: YogaInput) -> YogaVerdict:
    """A statement about dasas, not about the chart as a whole: it names the
    planets whose dasas give loss of wealth."""
    key = "daridra_planets_with_dusthana_lords"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    dusthana_lords = {lord_of_house(data, h) for h in DUSTHANA}
    trine_lords = tuple(sorted({lord_of_house(data, h) for h in TRIKONA}))
    afflicted = []
    saved = []
    for graha in sorted(data.rasis):
        if graha in dusthana_lords:
            continue
        with_lord = [g for g in sorted(dusthana_lords)
                     if g != graha and data.sign_of(g) == data.sign_of(graha)]
        if not with_lord:
            continue
        if reached_by(data, trine_lords, graha):
            saved.append(graha)
        else:
            afflicted.append(graha)
    extra: tuple[str, ...] = ()
    if saved:
        extra = ((f"{', '.join(GRAHA_NAMES[g] for g in saved)} "
                  f"{'is' if len(saved) == 1 else 'are'} also conjoined by a "
                  f"dusthana lord but reached by a trine lord, which section "
                  f"11.10 makes the saving factor"),)
    if not afflicted:
        return _verdict(key, False,
                        "no planet is conjoined by a 6th, 8th or 12th lord "
                        "without a trine lord also reaching it",
                        extra_qualifiers=extra)
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in afflicted)} "
                    f"{'is' if len(afflicted) == 1 else 'are'} conjoined by a "
                    f"dusthana lord and not reached by any trine lord; "
                    f"section 11.10 says the loss falls in their dasas",
                    participants=tuple(afflicted), extra_qualifiers=extra)


def _detect_12(data: YogaInput) -> YogaVerdict:
    key = "daridra_mars_saturn_in_second"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    second = house_sign(data.lagna_rasi, 2)
    outside = [GRAHA_NAMES[g] for g in (MARS, SATURN)
               if data.sign_of(g) != second]
    if outside:
        return _verdict(key, False,
                        f"{' and '.join(outside)} "
                        f"{'is' if len(outside) == 1 else 'are'} not in the "
                        f"2nd house ({RASI_NAMES[second]})")
    mercury = data.sign_of(MERCURY)
    aspects = (mercury is not None
               and graha_aspects_sign(MERCURY, mercury, second))
    if aspects:
        return _verdict(
            key, False,
            "Mars and Saturn are in the 2nd, but Mercury aspects them — "
            "section 11.10's printed exception, under which “great wealth is "
            "generated”",
            extra_qualifiers=(_SPEC[key]["exception"],))
    return _verdict(key, True,
                    f"Mars and Saturn are in the 2nd house "
                    f"({RASI_NAMES[second]}) and Mercury does not aspect them",
                    participants=(MARS, SATURN))


def _detect_13(data: YogaInput) -> YogaVerdict:
    key = "daridra_sun_in_second_aspected_by_saturn"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    second = house_sign(data.lagna_rasi, 2)
    if data.sign_of(SUN) != second:
        return _verdict(key, False,
                        f"Sun is not in the 2nd house ({RASI_NAMES[second]})")
    saturn = data.sign_of(SATURN)
    aspects = (saturn is not None
               and (saturn == second
                    or graha_aspects_sign(SATURN, saturn, second)))
    if not aspects:
        return _verdict(
            key, False,
            "Sun is in the 2nd but Saturn does not aspect him — section "
            "11.10's printed exception, under which the Sun in the 2nd "
            "“gives wealth”",
            extra_qualifiers=(_SPEC[key]["exception"],))
    return _verdict(key, True,
                    f"Sun is in the 2nd house ({RASI_NAMES[second]}) and "
                    f"Saturn aspects him",
                    participants=(SUN, SATURN))


def saving_factor(data: YogaInput) -> dict:
    """The general principles' one clause that runs the other way.

    "However, conjunction or aspect of trine lords is a saving factor." Not a
    yoga, so it is reported beside them.
    """
    if data.lagna_rasi is None:
        return {"decidable": False, "reason": "no lagna was supplied"}
    trine_lords = tuple(sorted({lord_of_house(data, h) for h in TRIKONA}))
    lagna_lord = lord_of_house(data, 1)
    reached = {}
    for label, target in (("lagna lord", lagna_lord),):
        hits = reached_by(data, trine_lords, target)
        reached[label] = [
            {"graha": g, "graha_name": str(GRAHA_NAMES[g]), "how": how}
            for g, how in hits
        ]
    lagna_hits = [
        {"graha": g, "graha_name": str(GRAHA_NAMES[g]),
         "how": "conjunction" if data.rasis[g] == data.lagna_rasi else "aspect"}
        for g in trine_lords
        if data.sign_of(g) is not None
        and (data.rasis[g] == data.lagna_rasi
             or graha_aspects_sign(g, data.rasis[g], data.lagna_rasi))
    ]
    return {
        "decidable": True,
        "trine_lords": [{"graha": g, "graha_name": str(GRAHA_NAMES[g])}
                        for g in trine_lords],
        "reaching_lagna": lagna_hits,
        "reaching_lagna_lord": reached["lagna lord"],
        "applies": bool(lagna_hits or reached["lagna lord"]),
    }


_DETECTORS = {
    "daridra_first_twelfth_exchange": _exchange(
        "daridra_first_twelfth_exchange", 12),
    "daridra_first_sixth_exchange": _exchange(
        "daridra_first_sixth_exchange", 6),
    "daridra_ketu_and_eighth": _detect_3,
    "daridra_lord_with_malefic_in_dusthana": _detect_4,
    "daridra_fifth_and_ninth_lords_fallen": _detect_5,
    "daridra_malefics_in_lagna": _detect_6,
    "daridra_dispositors_in_dusthanas": _detect_7,
    "daridra_moons_navamsa_dispositor": _detect_8,
    "daridra_both_lagna_lords": _detect_9,
    "daridra_benefics_and_malefics_swapped": _detect_10,
    "daridra_planets_with_dusthana_lords": _detect_11,
    "daridra_mars_saturn_in_second": _detect_12,
    "daridra_sun_in_second_aspected_by_saturn": _detect_13,
}

for _key, _entry in _SPEC.items():
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=(),
        section="11.10",
        group="daridra",
        definition=_entry["definition"],
        detect=_DETECTORS[_key],
    ))
