"""§11.7.3 — the eighteen advanced Raaja yogas.

"Some advanced Raaja Yogas will be listed below."

Seventeen of them are combinations and are registered. The eighteenth is not:
it says how *effective* the chart's Raaja yogas are, so it is computed by
`arudha_effectiveness` and reported beside them, never among them.

**Nothing is decided from an input that cannot decide it.** These yogas reach
past signs — into chara karakas, the navamsa, the divisional lagnas, HL and
GL — and each of those needs something a sign-only chart does not carry. A
detector missing what it needs returns ``present=False`` with a reason naming
exactly what was absent, so an unanswerable question never reads as a
negative finding.
"""
from __future__ import annotations

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.popular import (
    MOON,
    benefic_set,
    houses_of,
    in_exaltation,
    in_own_sign,
    is_debilitated,
    lord_of_house,
    occupants_of_house,
)
from hora.charts.planetary_yogas.raaja import conjoined, mutual_drishti
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.charts.vargas import varga
from hora.core.const import (
    ADVANCED_RAAJA_STRENGTH_NOT_ASSESSED,
    ADVANCED_RAAJA_YOGAS,
    ARUDHA_EFFECTIVENESS_BAD_PAIRS,
    DUSTHANA,
    GRAHA_NAMES,
    KENDRA,
    MOOLATRIKONA,
    RASI_LORD,
    RASI_NAMES,
    VARGOTTAMAMSA_FOOTNOTE_UNREAD,
    Graha,
)

_SPEC = {entry["key"]: entry for entry in ADVANCED_RAAJA_YOGAS}

#: §11.7.3 (7)'s six, in the order the book names them.
SHADVARGA_CODES: tuple[str, ...] = ("D1", "D9", "D2", "D3", "D12", "D30")

#: §11.7.3 (9)'s three.
TRIVARGA_CODES: tuple[str, ...] = ("D1", "D9", "D3")


def _verdict(key: str, present: bool, reason: str, **kw) -> YogaVerdict:
    spec = _SPEC[key]
    qualifiers = tuple(kw.pop("extra_qualifiers", ()))
    if spec.get("strength"):
        who = ", ".join(spec["strength"])
        qualifiers += (
            ADVANCED_RAAJA_STRENGTH_NOT_ASSESSED,
            f"the planet section 11.7.3 asks to be strong here is {who}",
        )
    return YogaVerdict(key=key, name=spec["name"], present=present,
                       reason=reason, qualifiers=qualifiers, **kw)


def _cannot(key: str, why: str) -> YogaVerdict:
    """An unanswerable question, never a negative finding."""
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=False,
                       reason=f"this yoga cannot be decided: {why}")


def _needs_lagna(key: str) -> YogaVerdict:
    return _cannot(key, "no lagna was supplied, and it counts houses from "
                        "the ascendant")


# --------------------------------------------------------------------------
# What these yogas reach for beyond signs
# --------------------------------------------------------------------------

#: The eight grahas §8.2's chara karakas are assigned over.
_KARAKA_GRAHAS = (Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
                  Graha.JUPITER, Graha.VENUS, Graha.SATURN, Graha.RAHU)


def chara_karaka(data: YogaInput, symbol: str) -> tuple[int | None, str]:
    """AK, PK and the rest, from longitudes. §8.2's assignment, reused.

    :returns: ``(graha, "")`` or ``(None, why not)``.
    """
    from hora.charts.karaka import chara_karakas

    if not data.positions:
        return None, ("chara karakas are assigned by degrees within a sign "
                      "and no longitudes were supplied")
    missing = [GRAHA_NAMES[int(g)] for g in _KARAKA_GRAHAS
               if int(g) not in data.positions]
    if missing:
        return None, (f"chara karakas need all eight of section 8.2's grahas; "
                      f"{', '.join(missing)} "
                      f"{'is' if len(missing) == 1 else 'are'} missing")
    longitudes = {int(g): data.positions[int(g)].longitude
                  for g in _KARAKA_GRAHAS}
    for karaka in chara_karakas(longitudes):
        if karaka.symbol == symbol:
            return int(karaka.graha), ""
    return None, f"no {symbol} was assigned"


def aspected_by_a_benefic(data: YogaInput, graha: int) -> tuple[bool, tuple[int, ...]]:
    """"aspected by benefics" — at least one, by graha drishti or conjunction."""
    sign = data.sign_of(graha)
    if sign is None:
        return False, ()
    good = benefic_set(data) - {graha}
    found = tuple(g for g in sorted(good)
                  if data.rasis[g] == sign
                  or graha_aspects_sign(g, data.rasis[g], sign))
    return bool(found), found


def occupied_or_aspected_by_a_malefic(
        data: YogaInput, sign: int) -> tuple[bool, tuple[int, ...]]:
    good = benefic_set(data)
    found = tuple(g for g in sorted(data.rasis)
                  if g not in good
                  and (data.rasis[g] == sign
                       or graha_aspects_sign(g, data.rasis[g], sign)))
    return bool(found), found


def benefics_occupy(data: YogaInput, sign: int) -> tuple[int, ...]:
    good = benefic_set(data)
    return tuple(g for g in sorted(good) if data.rasis[g] == sign)


def in_own_amsa(data: YogaInput, graha: int) -> bool | None:
    """"own ... amsa" — the navamsa sign is one the graha owns."""
    if not data.positions or graha not in data.positions:
        return None
    sign = varga(data.positions[graha].longitude, "D9").sign
    return int(RASI_LORD[sign]) == graha


def dignified_by_sign(data: YogaInput, graha: int) -> bool:
    return in_own_sign(data, graha) or in_exaltation(data, graha)


def in_moolatrikona_or_exaltation(data: YogaInput, graha: int) -> bool:
    entry = MOOLATRIKONA.get(Graha(graha))
    sign = data.sign_of(graha)
    if sign is None:
        return False
    if in_exaltation(data, graha):
        return True
    if entry is None or int(entry[0]) != sign:
        return False
    if not data.positions or graha not in data.positions:
        return True
    return float(entry[1]) <= data.positions[graha].longitude % 30 < float(entry[2])


def varga_lagna_sign(data: YogaInput, code: str) -> int | None:
    if data.lagna_longitude is None:
        return None
    return varga(data.lagna_longitude, code).sign


def varga_sign(data: YogaInput, graha: int, code: str) -> int | None:
    if not data.positions or graha not in data.positions:
        return None
    return varga(data.positions[graha].longitude, code).sign


def associates_with_sign(data: YogaInput, graha: int, sign: int) -> str | None:
    """§11.7.3 (6)'s three: ownership, conjunction, aspect."""
    if int(RASI_LORD[sign]) == graha:
        return "ownership"
    where = data.sign_of(graha)
    if where is None:
        return None
    if where == sign:
        return "conjunction"
    if graha_aspects_sign(graha, where, sign):
        return "aspect"
    return None


# --------------------------------------------------------------------------
# (1) to (5) — the ones that need chara karakas
# --------------------------------------------------------------------------


def _detect_1(data: YogaInput) -> YogaVerdict:
    """Two conditions, and the book grades the halfway case explicitly."""
    key = "raaja_pk_ak_and_lords"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why_ak = chara_karaka(data, "AK")
    pk, why_pk = chara_karaka(data, "PK")
    if ak is None or pk is None:
        return _cannot(key, why_ak or why_pk)

    first = ak != pk and conjoined(data, ak, pk)
    lagna_lord, fifth = lord_of_house(data, 1), lord_of_house(data, 5)
    second = lagna_lord != fifth and conjoined(data, lagna_lord, fifth)

    describe_a = (f"AK {GRAHA_NAMES[ak]} and PK {GRAHA_NAMES[pk]} "
                  + ("are conjoined" if first else
                     "are the same planet" if ak == pk else "are not conjoined"))
    describe_b = (f"the lagna lord {GRAHA_NAMES[lagna_lord]} and 5th lord "
                  f"{GRAHA_NAMES[fifth]} "
                  + ("conjoin" if second else
                     "are the same planet" if lagna_lord == fifth
                     else "do not conjoin"))
    if first and second:
        return _verdict(key, True, f"{describe_a}; {describe_b}",
                        participants=tuple(sorted({ak, pk, lagna_lord, fifth})))
    extra: tuple[str, ...] = ()
    if first or second:
        extra = ((f"only one of the two conditions holds — {describe_a if first else describe_b}. "
                  f"Section 11.7.3 says the results may still be felt, but "
                  f"not fully, so the yoga is reported absent and the half "
                  f"that holds is named here"),)
    return _verdict(key, False, f"{describe_a}; {describe_b}",
                    extra_qualifiers=extra)


def _detect_2(data: YogaInput) -> YogaVerdict:
    """Four clauses. Clause (d)'s "those planets" is not defined — both
    readings are computed and neither is chosen. See OI-93."""
    key = "raaja_maharajah"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why_ak = chara_karaka(data, "AK")
    pk, why_pk = chara_karaka(data, "PK")
    if ak is None or pk is None:
        return _cannot(key, why_ak or why_pk)

    lagna_lord, fifth = lord_of_house(data, 1), lord_of_house(data, 5)
    failures = []
    if houses_of(data, lagna_lord) != 5:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not in "
                        f"the 5th")
    if houses_of(data, fifth) != 1:
        failures.append(f"the 5th lord {GRAHA_NAMES[fifth]} is not in lagna")
    for label, graha in (("AK", ak), ("PK", pk)):
        if houses_of(data, graha) not in (1, 5):
            failures.append(f"{label} {GRAHA_NAMES[graha]} is in neither "
                            f"lagna nor the 5th")

    def qualifies(graha: int) -> tuple[bool | None, str]:
        if dignified_by_sign(data, graha):
            kind = "own sign" if in_own_sign(data, graha) else "exaltation"
            return True, f"{GRAHA_NAMES[graha]} is in his {kind}"
        amsa = in_own_amsa(data, graha)
        if amsa:
            return True, f"{GRAHA_NAMES[graha]} is in his own navamsa"
        aspected, by = aspected_by_a_benefic(data, graha)
        if aspected:
            named = ", ".join(GRAHA_NAMES[g] for g in by)
            return True, f"{GRAHA_NAMES[graha]} is aspected by {named}"
        if amsa is None:
            return None, (f"{GRAHA_NAMES[graha]} has no longitude, so his "
                          f"navamsa cannot be read")
        return False, f"{GRAHA_NAMES[graha]} meets none of clause (d)"

    narrow = {g: qualifies(g) for g in dict.fromkeys((ak, pk))}
    wide = {g: qualifies(g) for g in dict.fromkeys((ak, pk, lagna_lord, fifth))}
    narrow_ok = all(v is True for v, _ in narrow.values())
    wide_ok = all(v is True for v, _ in wide.values())
    note = (
        f"clause (d) says “those planets” without saying which. Read as AK "
        f"and PK alone it {'holds' if narrow_ok else 'fails'}; read as all "
        f"four planets named in (a) to (c) it "
        f"{'holds' if wide_ok else 'fails'}. The wider reading is what "
        f"decides this verdict. See docs/open-items.md OI-93")

    if not wide_ok:
        failures.extend(detail for value, detail in wide.values() if value is not True)
    if failures:
        return _verdict(key, False, "; ".join(failures),
                        extra_qualifiers=(note,))
    return _verdict(key, True,
                    "; ".join(detail for _, detail in wide.values()),
                    participants=tuple(sorted({ak, pk, lagna_lord, fifth})),
                    extra_qualifiers=(note,))


def _detect_3(data: YogaInput) -> YogaVerdict:
    key = "raaja_ninth_lord_and_ak"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ak, why = chara_karaka(data, "AK")
    if ak is None:
        return _cannot(key, why)
    ninth = lord_of_house(data, 9)
    failures = []
    for label, graha in ((f"the 9th lord {GRAHA_NAMES[ninth]}", ninth),
                         (f"AK {GRAHA_NAMES[ak]}", ak)):
        house = houses_of(data, graha)
        if house not in (1, 5, 7):
            failures.append(f"{label} is in the {ordinal(house)}, not lagna, "
                            f"the 5th or the 7th" if house
                            else f"{label} has no placement")
            continue
        aspected, _ = aspected_by_a_benefic(data, graha)
        if not aspected:
            failures.append(f"{label} is not aspected by a benefic")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"the 9th lord {GRAHA_NAMES[ninth]} and AK "
                    f"{GRAHA_NAMES[ak]} both hold lagna, the 5th or the 7th, "
                    f"and both are aspected by a benefic",
                    participants=tuple(sorted({ninth, ak})))


def _from_lord_and_ak(key: str, houses: tuple[int, ...], want_benefic: bool):
    """(4) and (5): houses counted from the lagna lord **and** from AK."""
    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return _needs_lagna(key)
        ak, why = chara_karaka(data, "AK")
        if ak is None:
            return _cannot(key, why)
        lagna_lord = lord_of_house(data, 1)
        failures: list[str] = []
        found: list[int] = []
        for label, base_graha in ((f"the lagna lord {GRAHA_NAMES[lagna_lord]}",
                                   lagna_lord),
                                  (f"AK {GRAHA_NAMES[ak]}", ak)):
            base = data.sign_of(base_graha)
            if base is None:
                failures.append(f"{label} has no placement")
                continue
            for house in houses:
                sign = house_sign(base, house)
                if want_benefic:
                    grahas = benefics_occupy(data, sign)
                    ok = bool(grahas)
                else:
                    ok, grahas = occupied_or_aspected_by_a_malefic(data, sign)
                if ok:
                    found.extend(grahas)
                else:
                    failures.append(
                        f"the {ordinal(house)} from {label} "
                        f"({RASI_NAMES[sign]}) has no "
                        f"{'benefic' if want_benefic else 'malefic'}")
        if failures:
            return _verdict(key, False, "; ".join(failures))
        where = ", ".join(ordinal(h) for h in houses)
        return _verdict(key, True,
                        f"the {where} from the lagna lord "
                        f"{GRAHA_NAMES[lagna_lord]} and from AK "
                        f"{GRAHA_NAMES[ak]} all carry "
                        f"{'benefics' if want_benefic else 'malefics'}",
                        participants=tuple(sorted(set(found))))
    return detect


# --------------------------------------------------------------------------
# (6) to (9) — HL, GL and the divisional lagnas
# --------------------------------------------------------------------------


def _detect_6(data: YogaInput) -> YogaVerdict:
    """"joined or aspected by the same planet. One may add 'owned'."

    The book's own loosened form is computed too, and reported as a qualifier
    rather than as presence — it says the results "may be experienced", not
    that the yoga is present.
    """
    key = "raaja_lagna_hl_gl_one_planet"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    hl, gl = data.special_lagna_sign("HL"), data.special_lagna_sign("GL")
    missing = [name for name, sign in (("HL", hl), ("GL", gl)) if sign is None]
    if missing:
        return _cannot(key, f"{' and '.join(missing)} "
                            f"{'was' if len(missing) == 1 else 'were'} not "
                            f"supplied; they are computed from birth data, "
                            f"not from a graha")
    assert hl is not None and gl is not None
    targets = {"lagna": data.lagna_rasi, "HL": hl, "GL": gl}

    strict = []
    for graha in sorted(data.rasis):
        how = {label: associates_with_sign(data, graha, sign)
               for label, sign in targets.items()}
        if all(how.values()):
            strict.append((graha, how))

    loose = []
    for graha in sorted(data.rasis):
        if any(graha == g for g, _ in strict):
            continue
        how = {}
        for label, sign in targets.items():
            direct = associates_with_sign(data, graha, sign)
            lord = int(RASI_LORD[sign])
            via_lord = (None if lord == graha
                        else ("conjunction" if conjoined(data, graha, lord)
                              else "aspect" if (data.sign_of(graha) is not None
                                                and data.sign_of(lord) is not None
                                                and graha_aspects_sign(
                                                    graha, data.rasis[graha],
                                                    data.rasis[lord]))
                              else None))
            how[label] = direct or (f"via its lord ({via_lord})" if via_lord else None)
        if all(how.values()):
            loose.append((graha, how))

    extra = tuple(
        f"{GRAHA_NAMES[graha]} reaches lagna, HL and GL only in the loosened "
        f"form section 11.7.3 allows — "
        + ", ".join(f"{label} by {kind}" for label, kind in how.items())
        + ". The book says the results “may be experienced”, not that the "
          "yoga is present, so it is reported here and not as presence"
        for graha, how in loose)

    if not strict:
        return _verdict(key, False,
                        "no planet owns, joins or aspects all three of lagna, "
                        "HL and GL", extra_qualifiers=extra)
    named = "; ".join(
        f"{GRAHA_NAMES[graha]} by "
        + ", ".join(f"{label}: {kind}" for label, kind in how.items())
        for graha, how in strict)
    return _verdict(key, True, named,
                    participants=tuple(g for g, _ in strict),
                    extra_qualifiers=extra)


def _detect_7(data: YogaInput) -> YogaVerdict:
    key = "raaja_shadvarga_lagna_aspect"
    if data.lagna_longitude is None:
        return _cannot(key, "it reads the lagna of six divisional charts and "
                            "no lagna longitude was supplied")
    if not data.positions:
        return _cannot(key, "it reads six divisional charts and no longitudes "
                            "were supplied")
    winners = []
    for graha in sorted(data.positions):
        every = True
        for code in SHADVARGA_CODES:
            lagna = varga_lagna_sign(data, code)
            sign = varga_sign(data, graha, code)
            if lagna is None or sign is None or not graha_aspects_sign(
                    graha, sign, lagna):
                every = False
                break
        if every:
            winners.append(graha)
    if not winners:
        return _verdict(key, False,
                        "no planet aspects the lagna in all six shadvarga "
                        "charts (D-1, D-9, D-2, D-3, D-12, D-30)")
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in winners)} "
                    f"{'aspects' if len(winners) == 1 else 'aspect'} the "
                    f"lagna in all six shadvarga charts",
                    participants=tuple(winners))


def _detect_8(data: YogaInput) -> YogaVerdict:
    """"It can be different planets" — so each of the three is asked
    separately, not of one planet."""
    key = "raaja_dignified_on_lagna_hl_gl"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    hl, gl = data.special_lagna_sign("HL"), data.special_lagna_sign("GL")
    missing = [name for name, sign in (("HL", hl), ("GL", gl)) if sign is None]
    if missing:
        return _cannot(key, f"{' and '.join(missing)} "
                            f"{'was' if len(missing) == 1 else 'were'} not "
                            f"supplied")
    assert hl is not None and gl is not None
    failures, found = [], []
    for label, sign in (("lagna", data.lagna_rasi), ("HL", hl), ("GL", gl)):
        dignified = [g for g in sorted(data.rasis)
                     if data.rasis[g] == sign and dignified_by_sign(data, g)]
        if dignified:
            found.extend(dignified)
        else:
            failures.append(f"{label} ({RASI_NAMES[sign]}) holds no planet in "
                            f"an own or exaltation sign")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"lagna, HL and GL each hold a dignified planet — "
                    f"{', '.join(GRAHA_NAMES[g] for g in dict.fromkeys(found))}",
                    participants=tuple(dict.fromkeys(found)))


def _detect_9(data: YogaInput) -> YogaVerdict:
    key = "raaja_dignified_on_three_lagnas"
    if data.lagna_longitude is None:
        return _cannot(key, "it reads the lagna of three charts and no lagna "
                            "longitude was supplied")
    if not data.positions:
        return _cannot(key, "it reads three divisional charts and no "
                            "longitudes were supplied")
    from hora.charts.dignity import sign_dignity

    failures, found = [], []
    for code in TRIVARGA_CODES:
        lagna = varga_lagna_sign(data, code)
        dignified = []
        for graha in sorted(data.positions):
            position = varga(data.positions[graha].longitude, code)
            if position.sign == lagna and sign_dignity(
                    graha, position.longitude) in ("own", "exalted"):
                dignified.append(graha)
        if dignified:
            found.extend(dignified)
        else:
            failures.append(f"the {code} lagna holds no planet in an own or "
                            f"exaltation sign")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the lagna of D-1, D-9 and D-3 each hold a planet in an "
                    "own or exaltation sign",
                    participants=tuple(dict.fromkeys(found)))


# --------------------------------------------------------------------------
# (10) to (17)
# --------------------------------------------------------------------------


def _lagna_lord_dignified_and_aspecting(data: YogaInput) -> tuple[bool, str]:
    """The clause (b) that (10) and (11) share, word for word."""
    lord = lord_of_house(data, 1)
    assert data.lagna_rasi is not None
    if not dignified_by_sign(data, lord):
        return False, (f"the lagna lord {GRAHA_NAMES[lord]} is in neither an "
                       f"own nor an exaltation sign")
    where = data.sign_of(lord)
    assert where is not None
    if where == data.lagna_rasi:
        return True, (f"the lagna lord {GRAHA_NAMES[lord]} is dignified in "
                      f"lagna itself")
    if not graha_aspects_sign(lord, where, data.lagna_rasi):
        return False, (f"the lagna lord {GRAHA_NAMES[lord]} is dignified but "
                       f"does not aspect lagna")
    return True, (f"the lagna lord {GRAHA_NAMES[lord]} is dignified and "
                  f"aspects lagna")


def _detect_10(data: YogaInput) -> YogaVerdict:
    """"the 3rd, 6th and 8th houses are occupied by one or two planets in
    debilitation" — a count across the three, not one per house."""
    key = "raaja_debilitated_in_dusthanas"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fallen = [g for house in (3, 6, 8)
              for g in occupants_of_house(data, house)
              if is_debilitated(data, g)]
    failures = []
    if not 1 <= len(fallen) <= 2:
        failures.append(
            f"the 3rd, 6th and 8th hold {len(fallen)} debilitated planets, "
            f"not one or two"
            + (f" ({', '.join(GRAHA_NAMES[g] for g in fallen)})" if fallen else ""))
    ok, detail = _lagna_lord_dignified_and_aspecting(data)
    if not ok:
        failures.append(detail)
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in fallen)} "
                    f"{'is' if len(fallen) == 1 else 'are'} debilitated in "
                    f"the 3rd, 6th or 8th, and {detail}",
                    participants=tuple(sorted({*fallen, lord_of_house(data, 1)})))


def _detect_11(data: YogaInput) -> YogaVerdict:
    key = "raaja_afflicted_dusthana_lords"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    from hora.charts.planetary_yogas.popular import in_enemy_sign

    failures, afflicted = [], []
    combustion_unknown = []
    for house in DUSTHANA:
        lord = lord_of_house(data, house)
        reasons = []
        if is_debilitated(data, lord):
            reasons.append("debilitated")
        if in_enemy_sign(data, lord):
            reasons.append("in an inimical sign")
        sun = int(Graha.SUN)
        if data.positions and lord in data.positions and sun in data.positions:
            from hora.charts.dignity import combustion

            if lord != sun and combustion(lord, data.positions).combust:
                reasons.append("combust")
        elif lord != sun:
            combustion_unknown.append(GRAHA_NAMES[lord])
        if reasons:
            afflicted.append(lord)
        else:
            failures.append(f"the {ordinal(house)} lord {GRAHA_NAMES[lord]} "
                            f"is neither debilitated nor combust nor in an "
                            f"inimical sign")
    ok, detail = _lagna_lord_dignified_and_aspecting(data)
    if not ok:
        failures.append(detail)
    extra: tuple[str, ...] = ()
    if combustion_unknown:
        extra = ((f"combustion could not be judged for "
                  f"{', '.join(dict.fromkeys(combustion_unknown))}; the Sun's "
                  f"longitude or theirs was not supplied"),)
    if failures:
        return _verdict(key, False, "; ".join(failures),
                        extra_qualifiers=extra)
    return _verdict(key, True,
                    f"the 6th, 8th and 12th lords are all afflicted, and "
                    f"{detail}",
                    participants=tuple(sorted({*afflicted,
                                               lord_of_house(data, 1)})),
                    extra_qualifiers=extra)


def _detect_12(data: YogaInput) -> YogaVerdict:
    """Both are trine lords, so §11.7.1's quadrant-and-trine rule never
    reaches this pair. A separate rule, not a special case of that one."""
    key = "raaja_fifth_and_ninth_lords"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fifth, ninth = lord_of_house(data, 5), lord_of_house(data, 9)
    if fifth == ninth:
        return _verdict(key, False,
                        f"the 5th and 9th are both lorded by "
                        f"{GRAHA_NAMES[fifth]}, so there are not two planets")
    if conjoined(data, fifth, ninth):
        kind = "a conjunction"
    elif mutual_drishti(data, fifth, ninth):
        kind = "a mutual aspect"
    else:
        return _verdict(key, False,
                        f"the 5th lord {GRAHA_NAMES[fifth]} and 9th lord "
                        f"{GRAHA_NAMES[ninth]} are in neither a conjunction "
                        f"nor a mutual aspect")
    return _verdict(key, True,
                    f"the 5th lord {GRAHA_NAMES[fifth]} and 9th lord "
                    f"{GRAHA_NAMES[ninth]} are in {kind}",
                    participants=tuple(sorted({fifth, ninth})))


def _detect_13(data: YogaInput) -> YogaVerdict:
    key = "raaja_fourth_tenth_exchange"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fourth, tenth = lord_of_house(data, 4), lord_of_house(data, 10)
    failures = []
    if houses_of(data, fourth) != 10:
        failures.append(f"the 4th lord {GRAHA_NAMES[fourth]} is not in the 10th")
    if houses_of(data, tenth) != 4:
        failures.append(f"the 10th lord {GRAHA_NAMES[tenth]} is not in the 4th")
    aspectors = []
    if not failures:
        for house in (5, 9):
            lord = lord_of_house(data, house)
            where = data.sign_of(lord)
            if where is None:
                continue
            if all(graha_aspects_sign(lord, where, data.rasis[g])
                   or data.rasis[g] == where
                   for g in (fourth, tenth)):
                aspectors.append((house, lord))
        if not aspectors:
            failures.append("neither the 5th lord nor the 9th lord reaches "
                            "both of them")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    named = ", ".join(f"the {ordinal(h)} lord {GRAHA_NAMES[g]}"
                      for h, g in aspectors)
    return _verdict(key, True,
                    f"the 4th and 10th lords have exchanged houses and "
                    f"{named} reaches both",
                    participants=tuple(sorted({fourth, tenth,
                                               *(g for _, g in aspectors)})))


def _detect_14(data: YogaInput) -> YogaVerdict:
    key = "raaja_fifth_lord_joined"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fifth = lord_of_house(data, 5)
    house = houses_of(data, fifth)
    if house not in (1, 4, 10):
        return _verdict(key, False,
                        f"the 5th lord {GRAHA_NAMES[fifth]} is in the "
                        f"{ordinal(house)}, not the 1st, 4th or 10th"
                        if house else
                        f"the 5th lord {GRAHA_NAMES[fifth]} has no placement")
    joined = [(label, lord) for label, lord in
              (("lagna lord", lord_of_house(data, 1)),
               ("9th lord", lord_of_house(data, 9)))
              if lord != fifth and conjoined(data, lord, fifth)]
    if not joined:
        return _verdict(key, False,
                        f"the 5th lord {GRAHA_NAMES[fifth]} is in the "
                        f"{ordinal(house)} but neither the lagna lord nor the "
                        f"9th lord joins him")
    named = " and ".join(f"the {label} {GRAHA_NAMES[g]}" for label, g in joined)
    return _verdict(key, True,
                    f"the 5th lord {GRAHA_NAMES[fifth]} is in the "
                    f"{ordinal(house)} and {named} joins him",
                    participants=tuple(sorted({fifth,
                                               *(g for _, g in joined)})))


def _detect_15(data: YogaInput) -> YogaVerdict:
    """Clause (a) needs vargottamamsa, which footnote 40 defines and which was
    not supplied. Clause (b) is computed anyway, so the gap is visible rather
    than swallowing the whole yoga. See OI-92."""
    key = "raaja_vargottama_moon"
    moon_sign = data.sign_of(MOON)
    if moon_sign is None:
        return _cannot(key, "Moon has no placement")
    aspecting = [g for g in sorted(data.rasis)
                 if g != MOON and graha_aspects_sign(g, data.rasis[g], moon_sign)]
    clause_b = len(aspecting) >= 4
    detail = (f"{len(aspecting)} planets aspect Moon"
              + (f" ({', '.join(GRAHA_NAMES[g] for g in aspecting)})"
                 if aspecting else ""))
    if not clause_b:
        return _verdict(key, False,
                        f"{detail}; section 11.7.3 asks for four or more")
    return _cannot(
        key,
        f"{detail}, which satisfies clause (b), but clause (a) asks for a "
        f"vargottamamsa Moon and footnote "
        f"{VARGOTTAMAMSA_FOOTNOTE_UNREAD} — which defines vargottamamsa — was "
        f"not supplied. See docs/open-items.md OI-92")


def _detect_16(data: YogaInput) -> YogaVerdict:
    key = "raaja_four_dignified"
    dignified = [g for g in sorted(data.rasis)
                 if in_moolatrikona_or_exaltation(data, g)]
    if len(dignified) < 4:
        return _verdict(key, False,
                        f"{len(dignified)} planets occupy a moolatrikona or "
                        f"exaltation sign, not four or more"
                        + (f" ({', '.join(GRAHA_NAMES[g] for g in dignified)})"
                           if dignified else ""))
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in dignified)} — "
                    f"{len(dignified)} planets — occupy a moolatrikona or "
                    f"exaltation sign",
                    participants=tuple(dignified))


def _detect_17(data: YogaInput) -> YogaVerdict:
    """"benefics are in quadrants and malefics are in the 3rd, 6th and 11th."

    Read as: every placed benefic is in a quadrant, and every placed malefic
    is in one of those three. Anything looser would be satisfied by almost
    every chart. See OI-94.
    """
    key = "raaja_benefics_in_quadrants"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    _, unknown = data.benefics()
    if unknown:
        return _cannot(key, f"the nature of "
                            f"{', '.join(GRAHA_NAMES[int(g)] for g in unknown)} "
                            f"could not be decided; the Moon needs a paksha")
    stray_benefics = [g for g in sorted(good) if houses_of(data, g) not in KENDRA]
    stray_malefics = [g for g in sorted(data.rasis)
                      if g not in good and houses_of(data, g) not in (3, 6, 11)]
    failures = []
    if stray_benefics:
        failures.append(
            f"{', '.join(GRAHA_NAMES[g] for g in stray_benefics)} "
            f"{'is a benefic' if len(stray_benefics) == 1 else 'are benefics'} "
            f"outside the quadrants")
    if stray_malefics:
        failures.append(
            f"{', '.join(GRAHA_NAMES[g] for g in stray_malefics)} "
            f"{'is a malefic' if len(stray_malefics) == 1 else 'are malefics'} "
            f"outside the 3rd, 6th and 11th")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "every benefic holds a quadrant and every malefic the "
                    "3rd, 6th or 11th",
                    participants=tuple(sorted(data.rasis)))


# --------------------------------------------------------------------------
# (18) — not a yoga
# --------------------------------------------------------------------------


def arudha_effectiveness(data: YogaInput) -> dict:
    """§11.7.3 (18). How effective the chart's Raaja yogas are, not whether
    one is present — so it is returned beside them and never among them."""
    if data.lagna_rasi is None:
        return {"decidable": False,
                "reason": "no lagna was supplied"}
    from hora.charts.arudha import arudha_pada

    signs = {int(g): s for g, s in data.rasis.items()}
    try:
        al = arudha_pada(1, data.lagna_rasi, signs)
        a7 = arudha_pada(7, data.lagna_rasi, signs)
    except Exception as exc:  # noqa: BLE001 - reported, never swallowed
        return {"decidable": False, "reason": str(exc)}
    forward = (a7.sign - al.sign) % 12 + 1
    backward = (al.sign - a7.sign) % 12 + 1
    bad = [pair for pair in ARUDHA_EFFECTIVENESS_BAD_PAIRS
           if {forward, backward} == set(pair)]
    return {
        "decidable": True,
        "arudha_lagna_sign": al.sign,
        "arudha_lagna_sign_name": str(RASI_NAMES[al.sign]),
        "darapada_sign": a7.sign,
        "darapada_sign_name": str(RASI_NAMES[a7.sign]),
        "mutual_positions": sorted({forward, backward}),
        "more_effective": not bad,
        "reason": (
            f"arudha lagna in {RASI_NAMES[al.sign]} and darapada in "
            f"{RASI_NAMES[a7.sign]} are in mutual "
            f"{ordinal(min(forward, backward))}/{ordinal(max(forward, backward))} "
            f"positions"
            + (", which section 11.7.3 (18) names, so the chart's Raaja yogas "
               "are not made more effective" if bad else
               ", which is neither the 2nd/12th nor the 6th/8th, so the "
               "chart's Raaja yogas will be more effective")
        ),
    }


_DETECTORS = {
    "raaja_pk_ak_and_lords": _detect_1,
    "raaja_maharajah": _detect_2,
    "raaja_ninth_lord_and_ak": _detect_3,
    "raaja_benefics_from_lord_and_ak":
        _from_lord_and_ak("raaja_benefics_from_lord_and_ak", (2, 4, 5), True),
    "raaja_malefics_from_lord_and_ak":
        _from_lord_and_ak("raaja_malefics_from_lord_and_ak", (3, 6), False),
    "raaja_lagna_hl_gl_one_planet": _detect_6,
    "raaja_shadvarga_lagna_aspect": _detect_7,
    "raaja_dignified_on_lagna_hl_gl": _detect_8,
    "raaja_dignified_on_three_lagnas": _detect_9,
    "raaja_debilitated_in_dusthanas": _detect_10,
    "raaja_afflicted_dusthana_lords": _detect_11,
    "raaja_fifth_and_ninth_lords": _detect_12,
    "raaja_fourth_tenth_exchange": _detect_13,
    "raaja_fifth_lord_joined": _detect_14,
    "raaja_vargottama_moon": _detect_15,
    "raaja_four_dignified": _detect_16,
    "raaja_benefics_in_quadrants": _detect_17,
}

for _key, _entry in _SPEC.items():
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=(),
        section="11.7.3",
        group="raaja_advanced",
        definition=_entry["definition"],
        detect=_DETECTORS[_key],
    ))
