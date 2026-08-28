"""§11.8 — the Raaja Sambandha yogas.

"Raaja means a king. Sambandha means relation or association... Those who have
these yogas are typically powerful ministers, secretaries, counsellors and
bureaucrats, associated with the rulers and powerful men."

The section warns about itself before listing one: **"these yogas are very
common."** So a present verdict here means less than a present verdict in
§11.7, and every one of them carries that sentence, along with the section's
own pointer back to §11.7.2 — "the magnitude of success depends on the
strength of the planets involved".

Eleven of the fifteen need a chara karaka and two need an arudha pada, so the
same contract as §11.7.3 applies: an input that cannot decide a yoga gets a
reason saying so, never a bare absence.
"""
from __future__ import annotations

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.popular import (
    MOON,
    VENUS,
    benefic_set,
    dispositor,
    houses_of,
    in_exaltation,
    in_own_sign,
    lord_of_house,
    occupants_of_house,
)
from hora.charts.planetary_yogas.raaja import conjoined
from hora.charts.planetary_yogas.raaja_advanced import chara_karaka
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    ADVANCED_RAAJA_STRENGTH_NOT_ASSESSED,
    GRAHA_NAMES,
    KENDRA,
    RAAJA_SAMBANDHA_ARE_COMMON,
    RAAJA_SAMBANDHA_MAGNITUDE_RULE,
    RAAJA_SAMBANDHA_YOGAS,
    RASI_NAMES,
    TRIKONA,
)

_SPEC = {entry["key"]: entry for entry in RAAJA_SAMBANDHA_YOGAS}

#: Carried on every §11.8 verdict, present or absent. The section says it of
#: itself, so a caller weighing one of these should see it.
COMMONNESS_NOTE = (
    f"{RAAJA_SAMBANDHA_ARE_COMMON} {RAAJA_SAMBANDHA_MAGNITUDE_RULE} "
    f"Section 11.7.2's factors apply — see "
    f"/v1/planetary-yoga/raaja-magnitude.")


def _verdict(key: str, present: bool, reason: str, **kw) -> YogaVerdict:
    spec = _SPEC[key]
    qualifiers = (*tuple(kw.pop("extra_qualifiers", ())), COMMONNESS_NOTE)
    if spec.get("strength"):
        qualifiers += (
            ADVANCED_RAAJA_STRENGTH_NOT_ASSESSED,
            (f"section 11.8 asks {', '.join(spec['strength'])} to be “very "
             f"strong” here, over and above the placement"),
        )
    return YogaVerdict(key=key, name=spec["name"], present=present,
                       reason=reason, qualifiers=qualifiers, **kw)


def _cannot(key: str, why: str) -> YogaVerdict:
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=False,
                       reason=f"this yoga cannot be decided: {why}",
                       qualifiers=(COMMONNESS_NOTE,))


def _needs_lagna(key: str) -> YogaVerdict:
    return _cannot(key, "no lagna was supplied, and it counts houses from "
                        "the ascendant")


def arudha_sign(data: YogaInput, house: int) -> tuple[int | None, str]:
    """AL (house 1) and bhagyapada (house 9), by §9.2."""
    if data.lagna_rasi is None:
        return None, "no lagna was supplied"
    from hora.charts.arudha import arudha_pada

    try:
        pada = arudha_pada(house, data.lagna_rasi,
                           {int(g): s for g, s in data.rasis.items()})
    except Exception as exc:  # noqa: BLE001 - reported, never swallowed
        return None, str(exc)
    return pada.sign, ""


def reaches(data: YogaInput, graha: int, target: int) -> str | None:
    """"conjoined or aspected by" — the phrase §11.8 uses six times."""
    where = data.sign_of(graha)
    target_sign = data.sign_of(target)
    if where is None or target_sign is None:
        return None
    if where == target_sign:
        return "conjunction"
    if graha_aspects_sign(graha, where, target_sign):
        return "aspect"
    return None


def malefics_reaching_house(data: YogaInput, house: int) -> tuple[int, ...]:
    assert data.lagna_rasi is not None
    sign = house_sign(data.lagna_rasi, house)
    good = benefic_set(data)
    return tuple(g for g in sorted(data.rasis)
                 if g not in good
                 and (data.rasis[g] == sign
                      or graha_aspects_sign(g, data.rasis[g], sign)))


def malefics_occupying(data: YogaInput, sign: int) -> tuple[int, ...]:
    good = benefic_set(data)
    return tuple(g for g in sorted(data.rasis)
                 if g not in good and data.rasis[g] == sign)


# --------------------------------------------------------------------------
# The fifteen, in the order §11.8 prints them
# --------------------------------------------------------------------------


def _detect_1(data: YogaInput) -> YogaVerdict:
    """"conjoined or aspected by AmK ... **or his dispositor**" — two
    reachers, either of which does it."""
    key = "sambandha_tenth_lord_amk"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    amk, why = chara_karaka(data, "AmK")
    if amk is None:
        return _cannot(key, why)
    tenth = lord_of_house(data, 10)
    candidates: list[tuple[str, int]] = [(f"AmK {GRAHA_NAMES[amk]}", amk)]
    amk_lord = dispositor(data, amk)
    if amk_lord is not None and amk_lord != amk:
        candidates.append((f"AmK's dispositor {GRAHA_NAMES[amk_lord]}", amk_lord))
    for label, graha in candidates:
        if graha == tenth:
            continue
        how = reaches(data, graha, tenth)
        if how:
            return _verdict(key, True,
                            f"the 10th lord {GRAHA_NAMES[tenth]} is reached by "
                            f"{label} by {how}",
                            participants=tuple(sorted({tenth, graha})))
    tried = " nor ".join(label for label, _ in candidates)
    return _verdict(key, False,
                    f"the 10th lord {GRAHA_NAMES[tenth]} is neither conjoined "
                    f"nor aspected by {tried}")


def _detect_2(data: YogaInput) -> YogaVerdict:
    key = "sambandha_eleventh_lord_unafflicted"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    eleventh = lord_of_house(data, 11)
    where = data.sign_of(eleventh)
    target = house_sign(data.lagna_rasi, 11)
    failures = []
    if where is None:
        failures.append(f"the 11th lord {GRAHA_NAMES[eleventh]} has no placement")
    elif where != target and not graha_aspects_sign(eleventh, where, target):
        failures.append(f"the 11th lord {GRAHA_NAMES[eleventh]} does not "
                        f"aspect the 11th house")
    for house in (10, 11):
        bad = malefics_reaching_house(data, house)
        if bad:
            failures.append(f"{', '.join(GRAHA_NAMES[g] for g in bad)} "
                            f"{'is a malefic' if len(bad) == 1 else 'are malefics'} "
                            f"on the {ordinal(house)}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"the 11th lord {GRAHA_NAMES[eleventh]} aspects the 11th "
                    f"house and no malefic joins or aspects the 10th or 11th",
                    participants=(eleventh,))


def _detect_3(data: YogaInput) -> YogaVerdict:
    key = "sambandha_ak_amk_conjoin"
    ak, why_ak = chara_karaka(data, "AK")
    amk, why_amk = chara_karaka(data, "AmK")
    if ak is None or amk is None:
        return _cannot(key, why_ak or why_amk)
    if ak == amk:
        return _verdict(key, False,
                        f"AK and AmK are both {GRAHA_NAMES[ak]}, so there are "
                        f"not two planets to conjoin")
    if not conjoined(data, ak, amk):
        return _verdict(key, False,
                        f"AK {GRAHA_NAMES[ak]} and AmK {GRAHA_NAMES[amk]} do "
                        f"not conjoin")
    return _verdict(key, True,
                    f"AK {GRAHA_NAMES[ak]} and AmK {GRAHA_NAMES[amk]} conjoin "
                    f"in {RASI_NAMES[data.rasis[ak]]}",
                    participants=tuple(sorted({ak, amk})))


def _detect_4(data: YogaInput) -> YogaVerdict:
    key = "sambandha_amk_dignified"
    amk, why = chara_karaka(data, "AmK")
    if amk is None:
        return _cannot(key, why)
    if in_own_sign(data, amk):
        kind = "his own sign"
    elif in_exaltation(data, amk):
        kind = "his exaltation sign"
    else:
        return _verdict(key, False,
                        f"AmK {GRAHA_NAMES[amk]} is in "
                        f"{RASI_NAMES[data.rasis[amk]]}, neither his own sign "
                        f"nor his exaltation sign")
    return _verdict(key, True,
                    f"AmK {GRAHA_NAMES[amk]} is in {kind}, "
                    f"{RASI_NAMES[data.rasis[amk]]}",
                    participants=(amk,))


def _detect_5(data: YogaInput) -> YogaVerdict:
    key = "sambandha_amk_in_a_trine"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    amk, why = chara_karaka(data, "AmK")
    if amk is None:
        return _cannot(key, why)
    house = houses_of(data, amk)
    if house not in TRIKONA:
        return _verdict(key, False,
                        f"AmK {GRAHA_NAMES[amk]} is in the {ordinal(house)}, "
                        f"not a trine from lagna" if house else
                        f"AmK {GRAHA_NAMES[amk]} has no placement")
    return _verdict(key, True,
                    f"AmK {GRAHA_NAMES[amk]} is in the {ordinal(house)}, a "
                    f"trine from lagna",
                    participants=(amk,), houses={amk: house})


def _detect_6(data: YogaInput) -> YogaVerdict:
    key = "sambandha_amk_from_ak"
    ak, why_ak = chara_karaka(data, "AK")
    amk, why_amk = chara_karaka(data, "AmK")
    if ak is None or amk is None:
        return _cannot(key, why_ak or why_amk)
    ak_sign, amk_sign = data.sign_of(ak), data.sign_of(amk)
    if ak_sign is None or amk_sign is None:
        return _verdict(key, False, "AK or AmK has no placement")
    house = (amk_sign - ak_sign) % 12 + 1
    if house not in KENDRA and house not in TRIKONA:
        return _verdict(key, False,
                        f"AmK {GRAHA_NAMES[amk]} is the {ordinal(house)} from "
                        f"AK {GRAHA_NAMES[ak]}, neither a quadrant nor a trine")
    kind = "a quadrant" if house in KENDRA else "a trine"
    return _verdict(key, True,
                    f"AmK {GRAHA_NAMES[amk]} is the {ordinal(house)} from AK "
                    f"{GRAHA_NAMES[ak]} — {kind}",
                    participants=tuple(sorted({ak, amk})))


def _detect_7(data: YogaInput) -> YogaVerdict:
    """"the 3rd and 6th houses from lagna, AL **and** AK" — the book
    italicises the "and", so all three references are counted from."""
    key = "sambandha_malefics_from_three"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    al, why_al = arudha_sign(data, 1)
    if al is None:
        return _cannot(key, f"AL could not be computed: {why_al}")
    ak_sign = data.sign_of(ak)
    if ak_sign is None:
        return _verdict(key, False, f"AK {GRAHA_NAMES[ak]} has no placement")

    bases = (("lagna", data.lagna_rasi), ("AL", al),
             (f"AK {GRAHA_NAMES[ak]}", ak_sign))
    failures: list[str] = []
    found: list[int] = []
    for label, base in bases:
        for house in (3, 6):
            sign = house_sign(base, house)
            grahas = malefics_occupying(data, sign)
            if grahas:
                found.extend(grahas)
            else:
                failures.append(f"the {ordinal(house)} from {label} "
                                f"({RASI_NAMES[sign]}) holds no malefic")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "malefics occupy the 3rd and 6th from lagna, from AL and "
                    "from AK",
                    participants=tuple(sorted(set(found))))


def _detect_8(data: YogaInput) -> YogaVerdict:
    key = "sambandha_ak_dignified_and_ninth_lord"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    failures = []
    if not (in_own_sign(data, ak) or in_exaltation(data, ak)):
        failures.append(f"AK {GRAHA_NAMES[ak]} is in neither an own nor an "
                        f"exaltation sign")
    house = houses_of(data, ak)
    if house is None:
        failures.append(f"AK {GRAHA_NAMES[ak]} has no placement")
    elif house not in KENDRA and house not in TRIKONA:
        failures.append(f"AK {GRAHA_NAMES[ak]} is in the {ordinal(house)}, "
                        f"neither a quadrant nor a trine")
    ninth = lord_of_house(data, 9)
    how = None if ninth == ak else reaches(data, ak, ninth)
    if ninth == ak:
        failures.append(f"AK is the 9th lord {GRAHA_NAMES[ak]} himself, so he "
                        f"cannot conjoin or aspect the 9th lord")
    elif how is None:
        failures.append(f"AK {GRAHA_NAMES[ak]} neither conjoins nor aspects "
                        f"the 9th lord {GRAHA_NAMES[ninth]}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    assert house is not None
    return _verdict(key, True,
                    f"AK {GRAHA_NAMES[ak]} is dignified in the "
                    f"{ordinal(house)} and reaches the 9th lord "
                    f"{GRAHA_NAMES[ninth]} by {how}",
                    participants=tuple(sorted({ak, ninth})))


def _detect_9(data: YogaInput) -> YogaVerdict:
    key = "sambandha_ak_is_moons_dispositor"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    moon_lord = dispositor(data, MOON)
    failures = []
    if moon_lord is None:
        failures.append("Moon has no placement, so she has no dispositor")
    elif moon_lord != ak:
        failures.append(f"Moon's dispositor is {GRAHA_NAMES[moon_lord]}, not "
                        f"AK {GRAHA_NAMES[ak]}")
    if houses_of(data, ak) != 1:
        failures.append(f"AK {GRAHA_NAMES[ak]} does not occupy lagna")
    else:
        good = benefic_set(data) - {ak}
        with_him = [g for g in occupants_of_house(data, 1) if g in good]
        if not with_him:
            failures.append("no benefic is in lagna with him")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"AK {GRAHA_NAMES[ak]} is Moon's dispositor and occupies "
                    f"lagna with a benefic",
                    participants=(ak, MOON))


def _detect_10(data: YogaInput) -> YogaVerdict:
    key = "sambandha_ak_with_a_benefic"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    house = houses_of(data, ak)
    if house not in (5, 7, 9, 10):
        return _verdict(key, False,
                        f"AK {GRAHA_NAMES[ak]} is in the {ordinal(house)}, "
                        f"not the 5th, 7th, 9th or 10th" if house else
                        f"AK {GRAHA_NAMES[ak]} has no placement")
    good = benefic_set(data) - {ak}
    with_him = [g for g in occupants_of_house(data, house) if g in good]
    if not with_him:
        return _verdict(key, False,
                        f"AK {GRAHA_NAMES[ak]} is in the {ordinal(house)} but "
                        f"no benefic is with him")
    return _verdict(key, True,
                    f"AK {GRAHA_NAMES[ak]} is in the {ordinal(house)} with "
                    f"{', '.join(GRAHA_NAMES[g] for g in with_him)}",
                    participants=(ak, *with_him), houses={ak: house})


def _detect_11(data: YogaInput) -> YogaVerdict:
    """"bhagyapada is in lagna **or** AK is in 9th" — either alone does it."""
    key = "sambandha_bhagyapada_or_ak_in_ninth"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    a9, why_a9 = arudha_sign(data, 9)
    if a9 is None:
        return _cannot(key, f"bhagyapada (A9) could not be computed: {why_a9}")
    if a9 == data.lagna_rasi:
        return _verdict(key, True,
                        f"bhagyapada (A9) is in lagna, {RASI_NAMES[a9]}",
                        participants=(ak,))
    house = houses_of(data, ak)
    if house == 9:
        return _verdict(key, True,
                        f"AK {GRAHA_NAMES[ak]} is in the 9th",
                        participants=(ak,), houses={ak: 9})
    return _verdict(key, False,
                    f"bhagyapada (A9) is in {RASI_NAMES[a9]}, not lagna "
                    f"({RASI_NAMES[data.lagna_rasi]}), and AK "
                    f"{GRAHA_NAMES[ak]} is in the {ordinal(house)}, not the "
                    f"9th" if house else
                    f"bhagyapada (A9) is in {RASI_NAMES[a9]}, not lagna, and "
                    f"AK {GRAHA_NAMES[ak]} has no placement")


def _detect_12(data: YogaInput) -> YogaVerdict:
    key = "sambandha_eleventh_lord_and_ak"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    eleventh = lord_of_house(data, 11)
    failures = []
    if houses_of(data, eleventh) != 11:
        failures.append(f"the 11th lord {GRAHA_NAMES[eleventh]} is not in the "
                        f"11th house")
    else:
        good = benefic_set(data)
        sign = data.rasis[eleventh]
        bad = [g for g in sorted(data.rasis)
               if g not in good and g != eleventh
               and graha_aspects_sign(g, data.rasis[g], sign)]
        if bad:
            failures.append(f"{', '.join(GRAHA_NAMES[g] for g in bad)} "
                            f"{'aspects' if len(bad) == 1 else 'aspect'} him")
    # "AK is with benefics" — plural, with no number given. One is taken to
    # satisfy it and the count is reported. See docs/open-items.md OI-95.
    good = benefic_set(data) - {ak}
    ak_sign = data.sign_of(ak)
    with_him = [g for g in sorted(good) if data.sign_of(g) == ak_sign]
    if not with_him:
        failures.append(f"AK {GRAHA_NAMES[ak]} is not with a benefic")
    plural_note = (
        f"section 11.8 says AK is “with benefic**s**” and gives no number; "
        f"{len(with_him)} "
        f"{'is' if len(with_him) == 1 else 'are'} with him. One is taken to "
        f"satisfy it — see docs/open-items.md OI-95")
    if failures:
        return _verdict(key, False, "; ".join(failures),
                        extra_qualifiers=(plural_note,))
    return _verdict(key, True,
                    f"the 11th lord {GRAHA_NAMES[eleventh]} holds the 11th "
                    f"unaspected by any malefic, and AK {GRAHA_NAMES[ak]} is "
                    f"with {', '.join(GRAHA_NAMES[g] for g in with_him)}",
                    participants=tuple(sorted({eleventh, ak, *with_him})),
                    extra_qualifiers=(plural_note,))


def _detect_13(data: YogaInput) -> YogaVerdict:
    key = "sambandha_first_tenth_exchange"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    lagna_lord, tenth = lord_of_house(data, 1), lord_of_house(data, 10)
    failures = []
    if houses_of(data, lagna_lord) != 10:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not in "
                        f"the 10th")
    if houses_of(data, tenth) != 1:
        failures.append(f"the 10th lord {GRAHA_NAMES[tenth]} is not in lagna")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"the lagna lord {GRAHA_NAMES[lagna_lord]} holds the 10th "
                    f"and the 10th lord {GRAHA_NAMES[tenth]} holds lagna",
                    participants=tuple(sorted({lagna_lord, tenth})))


def _detect_14(data: YogaInput) -> YogaVerdict:
    key = "sambandha_moon_venus_from_ak"
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    ak_sign = data.sign_of(ak)
    if ak_sign is None:
        return _verdict(key, False, f"AK {GRAHA_NAMES[ak]} has no placement")
    target = house_sign(ak_sign, 4)
    outside = [GRAHA_NAMES[g] for g in (MOON, VENUS)
               if data.sign_of(g) != target]
    if outside:
        return _verdict(key, False,
                        f"{' and '.join(outside)} "
                        f"{'is' if len(outside) == 1 else 'are'} not in the "
                        f"4th from AK {GRAHA_NAMES[ak]} ({RASI_NAMES[target]})")
    return _verdict(key, True,
                    f"Moon and Venus are both in {RASI_NAMES[target]}, the "
                    f"4th from AK {GRAHA_NAMES[ak]}",
                    participants=(MOON, VENUS))


def _detect_15(data: YogaInput) -> YogaVerdict:
    """"conjoins the 5th lord **in a quadrant or a trine**" — the sign they
    meet in has to be one, not merely the joining planet."""
    key = "sambandha_fifth_lord_joined"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    fifth = lord_of_house(data, 5)
    lagna_lord = lord_of_house(data, 1)
    tried = []
    for label, graha in ((f"the lagna lord {GRAHA_NAMES[lagna_lord]}", lagna_lord),
                         (f"AK {GRAHA_NAMES[ak]}", ak)):
        if graha == fifth:
            tried.append(f"{label} is the 5th lord himself")
            continue
        if not conjoined(data, graha, fifth):
            tried.append(f"{label} does not conjoin the 5th lord "
                         f"{GRAHA_NAMES[fifth]}")
            continue
        house = houses_of(data, fifth)
        if house is None:
            tried.append(f"the 5th lord {GRAHA_NAMES[fifth]} has no placement")
            continue
        if house not in KENDRA and house not in TRIKONA:
            tried.append(f"{label} conjoins the 5th lord in the "
                         f"{ordinal(house)}, neither a quadrant nor a trine")
            continue
        return _verdict(key, True,
                        f"{label} conjoins the 5th lord {GRAHA_NAMES[fifth]} "
                        f"in the {ordinal(house)}",
                        participants=tuple(sorted({graha, fifth})))
    return _verdict(key, False, "; ".join(tried))


_DETECTORS = {
    "sambandha_tenth_lord_amk": _detect_1,
    "sambandha_eleventh_lord_unafflicted": _detect_2,
    "sambandha_ak_amk_conjoin": _detect_3,
    "sambandha_amk_dignified": _detect_4,
    "sambandha_amk_in_a_trine": _detect_5,
    "sambandha_amk_from_ak": _detect_6,
    "sambandha_malefics_from_three": _detect_7,
    "sambandha_ak_dignified_and_ninth_lord": _detect_8,
    "sambandha_ak_is_moons_dispositor": _detect_9,
    "sambandha_ak_with_a_benefic": _detect_10,
    "sambandha_bhagyapada_or_ak_in_ninth": _detect_11,
    "sambandha_eleventh_lord_and_ak": _detect_12,
    "sambandha_first_tenth_exchange": _detect_13,
    "sambandha_moon_venus_from_ak": _detect_14,
    "sambandha_fifth_lord_joined": _detect_15,
}

for _key, _entry in _SPEC.items():
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=(),
        section="11.8",
        group="raaja_sambandha",
        definition=_entry["definition"],
        detect=_DETECTORS[_key],
    ))
