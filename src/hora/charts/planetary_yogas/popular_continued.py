"""§11.6, continued — thirty more popular yogas.

The section's list runs on past the Shivaji example. **These are not
Shivaji's yogas**; his chart is used for Kalpadruma alone.

§11.6's preamble binds these thirty exactly as it binds the first eighteen:
the combinations are not fullness without strength, and strength is not
built. Every verdict here carries `STRENGTH_NOT_ASSESSED` too. See OI-81.

Four of them read the navamsa and two turn on "deep exaltation". Where the
book gives no threshold for how deep is deep, the verdict says so rather than
inventing one — see OI-83.
"""
from __future__ import annotations

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.popular import (
    JUPITER,
    KENDRA_OR_TRIKONA,
    MARS,
    MERCURY,
    MOON,
    SATURN,
    VENUS,
    benefic_set,
    conjoins_or_aspects,
    dispositor,
    houses_of,
    in_exaltation,
    in_friendly_sign,
    in_own_sign,
    is_debilitated,
    lord_of_house,
    mutual_quadrants,
    occupants_of_house,
)
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.charts.relationship import GREAT_FRIEND, compound_in_chart
from hora.charts.vargas import d9_navamsa
from hora.core.const import (
    EXALTATION_DEG,
    GRAHA_NAMES,
    KENDRA,
    MOOLATRIKONA,
    POPULAR_YOGAS_CONTINUED,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
    STRENGTH_NOT_ASSESSED,
    TRIKONA,
    UPACHAYA,
    Graha,
)

SUN = int(Graha.SUN)

_SPEC = {entry["key"]: entry for entry in POPULAR_YOGAS_CONTINUED}


# --------------------------------------------------------------------------
# Verdict plumbing, shared with the first eighteen
# --------------------------------------------------------------------------


def _strength_note(key: str) -> tuple[str, ...]:
    spec = _SPEC[key]
    named = spec.get("strength", ())
    if not named:
        return (STRENGTH_NOT_ASSESSED,)
    who = ", ".join(named)
    return (STRENGTH_NOT_ASSESSED,
            (f"section 11.6 requires the {who} to be strong for this yoga; "
             f"that is not assessed"))


def _verdict(key: str, present: bool, reason: str, **kw) -> YogaVerdict:
    qualifiers = tuple(kw.pop("extra_qualifiers", ())) + _strength_note(key)
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=present,
                       reason=reason, qualifiers=qualifiers, **kw)


def _needs_lagna(key: str) -> YogaVerdict:
    return YogaVerdict(
        key=key, name=_SPEC[key]["name"], present=False,
        reason=("no lagna was supplied, and this yoga counts houses from "
                "lagna; it cannot be decided"))


def _needs_longitudes(key: str, why: str) -> YogaVerdict:
    return YogaVerdict(
        key=key, name=_SPEC[key]["name"], present=False,
        reason=f"{why}; that needs longitudes, which were not supplied",
        qualifiers=_strength_note(key))


# --------------------------------------------------------------------------
# Predicates this half needs
# --------------------------------------------------------------------------


def exchange(data: YogaInput, house_a: int, house_b: int) -> bool:
    """Footnote 35's parivartana: each house's lord sits in the other."""
    lord_a, lord_b = lord_of_house(data, house_a), lord_of_house(data, house_b)
    return houses_of(data, lord_a) == house_b and houses_of(data, lord_b) == house_a


def benefics_in(data: YogaInput, base_sign: int, houses: tuple[int, ...]
                ) -> tuple[bool, dict[int, tuple[int, ...]]]:
    """Does each named house *from base_sign* hold at least one benefic?"""
    good = benefic_set(data)
    found: dict[int, tuple[int, ...]] = {}
    for house in houses:
        sign = house_sign(base_sign, house)
        found[house] = tuple(g for g in sorted(data.rasis)
                             if data.rasis[g] == sign and g in good)
    return all(found[h] for h in houses), found


def _missing(found: dict[int, tuple[int, ...]]) -> str:
    empty = [ordinal(h) for h, grahas in sorted(found.items()) if not grahas]
    return ", ".join(empty)


def navamsa_sign_of(data: YogaInput, graha: int) -> int | None:
    """The sign a graha occupies in D-9, or None without longitudes."""
    if not data.positions or graha not in data.positions:
        return None
    return d9_navamsa(data.positions[graha].longitude).sign


def navamsa_dispositor(data: YogaInput, graha: int) -> int | None:
    """"the lord of the sign occupied in navamsa by X"."""
    sign = navamsa_sign_of(data, graha)
    return None if sign is None else int(RASI_LORD[sign])


def navamsa_lord_or_why(data: YogaInput, graha: int) -> tuple[int | None, str]:
    """The navamsa dispositor, or why it could not be had.

    Two different failures, kept apart: no longitudes were supplied at all,
    or this particular graha was never placed.
    """
    lord = navamsa_dispositor(data, graha)
    if lord is not None:
        return lord, ""
    if not data.positions:
        return None, "no longitudes were supplied, so navamsa cannot be read"
    return None, f"{GRAHA_NAMES[graha]} has no placement"


def deep_exaltation(data: YogaInput, graha: int) -> tuple[bool | None, str]:
    """"deep exaltation" — the exact degree, with no tolerance printed.

    Returns ``(False, why)`` when the graha is not even in its exaltation
    sign, which settles most charts. When he *is* there, the book gives no
    rule for how near the exact degree counts as deep, so this returns
    ``(None, why)`` with the distance named rather than picking a threshold.
    See OI-83.
    """
    exact = EXALTATION_DEG.get(graha)
    name = GRAHA_NAMES[graha]
    if exact is None:
        return False, f"{name} has no exaltation degree"
    sign = data.sign_of(graha)
    if sign is None:
        return False, f"{name} has no placement"
    if sign != int(exact // 30):
        return False, (f"{name} is in {RASI_NAMES[sign]}, not his exaltation "
                       f"sign {RASI_NAMES[int(exact // 30)]}")
    if not data.positions or graha not in data.positions:
        return None, (f"{name} is in his exaltation sign, but deep exaltation "
                      f"is a degree and no longitude was supplied")
    distance = abs(data.positions[graha].longitude - exact)
    return None, (f"{name} is {distance:.2f}° from his exact exaltation "
                  f"degree ({exact % 30:.0f}° {RASI_NAMES[int(exact // 30)]}); "
                  f"section 11.6 gives no threshold for “deep”")


def in_moolatrikona(data: YogaInput, graha: int) -> bool:
    """Sign-level unless longitudes are supplied, when the arc is used too."""
    entry = MOOLATRIKONA.get(Graha(graha))
    if entry is None:
        return False
    sign, start, end = int(entry[0]), float(entry[1]), float(entry[2])
    if data.sign_of(graha) != sign:
        return False
    if not data.positions or graha not in data.positions:
        return True
    return start <= data.positions[graha].longitude % 30 < end


def aspects_sign(data: YogaInput, graha: int, target_sign: int) -> bool:
    sign = data.sign_of(graha)
    return sign is not None and graha_aspects_sign(graha, sign, target_sign)


def in_adhimitra_house(data: YogaInput, graha: int) -> bool:
    """"in the house of an adhimitra (good friend)" — the compound relation."""
    sign = data.sign_of(graha)
    if sign is None:
        return False
    lord = int(RASI_LORD[sign])
    if lord == graha:
        return False
    relation = compound_in_chart(graha, lord, data.rasis)
    return relation.compound == GREAT_FRIEND


def mutual_trines(*signs: int) -> bool:
    return all((signs[j] - signs[i]) % 12 + 1 in TRIKONA
               for i in range(len(signs)) for j in range(i + 1, len(signs)))


# --------------------------------------------------------------------------
# The thirty
# --------------------------------------------------------------------------


def _detect_lagnaadhi(data: YogaInput) -> YogaVerdict:
    """Named for §11.3.6's Adhi but not the same rule: that one takes the
    6th, 7th and 8th from Moon; this takes only the 7th and 8th from lagna.
    The definition is followed. See docs/book-deviations.md D-35."""
    key = "lagnaadhi"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ok, found = benefics_in(data, data.lagna_rasi, (7, 8))
    if not ok:
        return _verdict(key, False,
                        f"no benefic in the {_missing(found)}")
    inside = tuple(sorted({g for grahas in found.values() for g in grahas}))
    bad = benefic_set(data)
    spoilers = []
    for malefic in sorted(data.rasis):
        if malefic in bad:
            continue
        for good in inside:
            target = data.rasis[good]
            if conjoins_or_aspects(data, malefic, target):
                how = ("joins" if data.rasis[malefic] == target else "aspects")
                spoilers.append(f"{GRAHA_NAMES[malefic]} {how} "
                                f"{GRAHA_NAMES[good]}")
    if spoilers:
        return _verdict(key, False,
                        "a malefic reaches the benefics: "
                        + "; ".join(sorted(set(spoilers))))
    named = ", ".join(GRAHA_NAMES[g] for g in inside)
    return _verdict(key, True,
                    f"benefics hold the 7th and 8th — {named} — and no "
                    f"malefic conjoins or aspects them",
                    participants=inside)


def _from_a_lord(key: str, from_house: int, houses: tuple[int, ...]):
    """Hari, Hara and Brahma: benefics in named houses counted from a lord."""
    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return _needs_lagna(key)
        lord = lord_of_house(data, from_house)
        base = data.sign_of(lord)
        if base is None:
            return _verdict(key, False,
                            f"the {ordinal(from_house)} lord "
                            f"{GRAHA_NAMES[lord]} has no placement")
        ok, found = benefics_in(data, base, houses)
        where = f"the {ordinal(from_house)} lord {GRAHA_NAMES[lord]} in {RASI_NAMES[base]}"
        if not ok:
            return _verdict(key, False,
                            f"counted from {where}, no benefic in the "
                            f"{_missing(found)}")
        inside = tuple(sorted({g for grahas in found.values() for g in grahas}))
        return _verdict(key, True,
                        f"counted from {where}, benefics hold the "
                        f"{', '.join(ordinal(h) for h in houses)}",
                        participants=inside)
    return detect


def _detect_vishnu(data: YogaInput) -> YogaVerdict:
    key = "vishnu"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ninth, tenth = lord_of_house(data, 9), lord_of_house(data, 10)
    failures = [f"the {ordinal(h)} lord {GRAHA_NAMES[g]} is not in the 2nd"
                for h, g in ((9, ninth), (10, tenth))
                if houses_of(data, g) != 2]
    navamsa_lord, why = navamsa_lord_or_why(data, ninth)
    if navamsa_lord is None:
        return _needs_longitudes(
            key, f"clause 2 reads the navamsa sign of the 9th lord, but {why}")
    if houses_of(data, navamsa_lord) != 2:
        failures.append(f"{GRAHA_NAMES[navamsa_lord]}, lord of the 9th lord's "
                        f"navamsa sign, is not in the 2nd")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"the 9th lord {GRAHA_NAMES[ninth]}, the 10th lord "
                    f"{GRAHA_NAMES[tenth]} and {GRAHA_NAMES[navamsa_lord]} — "
                    f"lord of the 9th lord's navamsa sign — all hold the 2nd",
                    participants=tuple(sorted({ninth, tenth, navamsa_lord})))


def _detect_siva(data: YogaInput) -> YogaVerdict:
    key = "siva"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    wanted = ((5, 9), (9, 10), (10, 5))
    failures = []
    for lord_house, target in wanted:
        lord = lord_of_house(data, lord_house)
        if houses_of(data, lord) != target:
            failures.append(f"the {ordinal(lord_house)} lord "
                            f"{GRAHA_NAMES[lord]} is not in the "
                            f"{ordinal(target)}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the 5th lord holds the 9th, the 9th lord the 10th and "
                    "the 10th lord the 5th",
                    participants=tuple(sorted(
                        {lord_of_house(data, h) for h, _ in wanted})))


def _detect_trilochana(data: YogaInput) -> YogaVerdict:
    key = "trilochana"
    signs = [data.sign_of(g) for g in (SUN, MOON, MARS)]
    if any(s is None for s in signs):
        missing = [GRAHA_NAMES[g] for g, s in zip((SUN, MOON, MARS), signs)
                   if s is None]
        return _verdict(key, False,
                        f"{', '.join(missing)} has no placement")
    placed = [s for s in signs if s is not None]
    if not mutual_trines(*placed):
        return _verdict(key, False,
                        "Sun in {}, Moon in {} and Mars in {} are not in "
                        "mutual trines".format(*(RASI_NAMES[s] for s in placed)))
    return _verdict(key, True,
                    "Sun, Moon and Mars are in mutual trines",
                    participants=(SUN, MOON, MARS))


def _detect_gouri(data: YogaInput) -> YogaVerdict:
    key = "gouri"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    tenth = lord_of_house(data, 10)
    navamsa_lord, why = navamsa_lord_or_why(data, tenth)
    if navamsa_lord is None:
        return _needs_longitudes(
            key, f"the yoga starts from the navamsa sign of the 10th lord, "
                 f"but {why}")
    failures = []
    if not in_exaltation(data, navamsa_lord):
        failures.append(f"{GRAHA_NAMES[navamsa_lord]}, lord of the 10th "
                        f"lord's navamsa sign, is not exalted")
    elif houses_of(data, navamsa_lord) != 10:
        failures.append(f"{GRAHA_NAMES[navamsa_lord]} is exalted but not in "
                        f"the 10th")
    lagna_lord = lord_of_house(data, 1)
    if data.sign_of(lagna_lord) != data.sign_of(navamsa_lord):
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} does not "
                        f"join him")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    itself = navamsa_lord == lagna_lord
    _note = ("the lord of the 10th lord's navamsa sign is the lagna lord "
             "himself, so “lagna lord joins him” is met by identity rather "
             "than by a second planet; section 11.6 does not say whether it "
             "intends one")
    extra: tuple[str, ...] = (_note,) if itself else ()
    return _verdict(key, True,
                    f"{GRAHA_NAMES[navamsa_lord]}, lord of the 10th lord's "
                    f"navamsa sign, is exalted in the 10th"
                    + (" and is himself the lagna lord" if itself else
                       f" with the lagna lord {GRAHA_NAMES[lagna_lord]}"),
                    participants=tuple(sorted({navamsa_lord, lagna_lord})),
                    extra_qualifiers=extra)


def _detect_chandikaa(data: YogaInput) -> YogaVerdict:
    key = "chandikaa"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    # Clause 1 is decidable from signs alone, and a movable or dual lagna
    # settles the yoga — no need to reach for the navamsa at all.
    if RASI_MODALITY[data.lagna_rasi] != 1:
        return _verdict(key, False,
                        f"lagna is in {RASI_NAMES[data.lagna_rasi]}, not a "
                        f"fixed sign")
    failures = []
    sixth, ninth = lord_of_house(data, 6), lord_of_house(data, 9)
    if not aspects_sign(data, sixth, data.lagna_rasi):
        failures.append(f"the 6th lord {GRAHA_NAMES[sixth]} does not aspect "
                        f"lagna")
    resolved = [navamsa_lord_or_why(data, g) for g in (sixth, ninth)]
    lords = [lord for lord, _ in resolved]
    if any(x is None for x in lords):
        why = "; ".join(w for lord, w in resolved if lord is None)
        return _needs_longitudes(
            key, f"clause 2 reads the navamsa signs of the 6th and 9th "
                 f"lords, but {why}")
    sun_sign = data.sign_of(SUN)
    apart = [GRAHA_NAMES[x] for x in lords if x is not None
             and data.sign_of(x) != sun_sign]
    if apart:
        failures.append(f"Sun does not join {' and '.join(apart)}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    distinct = sorted({x for x in lords if x is not None})
    named = " and ".join(GRAHA_NAMES[x] for x in distinct)
    if len(distinct) == 1:
        named += " — the 6th and 9th lords share a navamsa dispositor"
    return _verdict(key, True,
                    f"a fixed lagna aspected by the 6th lord "
                    f"{GRAHA_NAMES[sixth]}, and Sun joins {named} — the lords "
                    f"of the navamsa signs of the 6th and 9th lords",
                    participants=tuple(sorted(
                        {SUN, *(x for x in lords if x is not None)})))


def _detect_lakshmi(data: YogaInput) -> YogaVerdict:
    key = "lakshmi"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ninth = lord_of_house(data, 9)
    house = houses_of(data, ninth)
    if house is None:
        return _verdict(key, False,
                        f"the 9th lord {GRAHA_NAMES[ninth]} has no placement")
    dignified = in_own_sign(data, ninth) or in_exaltation(data, ninth)
    if not dignified:
        return _verdict(key, False,
                        f"the 9th lord {GRAHA_NAMES[ninth]} is in "
                        f"{RASI_NAMES[data.rasis[ninth]]}, neither his own "
                        f"sign nor his exaltation sign")
    if house not in KENDRA:
        return _verdict(key, False,
                        f"the 9th lord {GRAHA_NAMES[ninth]} is dignified but "
                        f"in the {ordinal(house)}, not a quadrant")
    kind = "his own sign" if in_own_sign(data, ninth) else "his exaltation sign"
    return _verdict(key, True,
                    f"the 9th lord {GRAHA_NAMES[ninth]} is in {kind}, "
                    f"{RASI_NAMES[data.rasis[ninth]]}, the "
                    f"{ordinal(house)} — a quadrant from lagna",
                    participants=(ninth,), houses={ninth: house})


def _detect_saarada(data: YogaInput) -> YogaVerdict:
    key = "saarada"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    tenth = lord_of_house(data, 10)
    if houses_of(data, tenth) != 5:
        failures.append(f"the 10th lord {GRAHA_NAMES[tenth]} is not in the 5th")
    if houses_of(data, MERCURY) not in KENDRA:
        failures.append("Mercury is not in a quadrant")
    if data.sign_of(SUN) != 4:
        failures.append("Sun is not in Leo")
    moon_sign = data.sign_of(MOON)
    if moon_sign is None:
        failures.append("Moon has no placement")
    else:
        trine = [GRAHA_NAMES[g] for g in (MERCURY, JUPITER)
                 if data.sign_of(g) is not None
                 and (data.rasis[g] - moon_sign) % 12 + 1 in TRIKONA]
        if not trine:
            failures.append("neither Mercury nor Jupiter is in a trine from Moon")
    if houses_of(data, MARS) != 11:
        failures.append("Mars is not in the 11th")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the 10th lord in the 5th, Mercury in a quadrant, Sun in "
                    "Leo, Mercury or Jupiter in a trine from Moon, and Mars "
                    "in the 11th",
                    participants=tuple(sorted(
                        {tenth, MERCURY, SUN, MOON, MARS})))


def _detect_bhaarathi(data: YogaInput) -> YogaVerdict:
    key = "bhaarathi"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ninth = lord_of_house(data, 9)
    ninth_sign = data.sign_of(ninth)
    tried = []
    for house in (2, 5, 11):
        lord = lord_of_house(data, house)
        navamsa_lord, why = navamsa_lord_or_why(data, lord)
        if navamsa_lord is None:
            if not data.positions:
                return _needs_longitudes(
                    key, "the yoga reads the navamsa signs of the 2nd, 5th "
                         "and 11th lords")
            tried.append(f"{ordinal(house)} lord {GRAHA_NAMES[lord]}: {why}")
            continue
        if in_exaltation(data, navamsa_lord) and \
                data.sign_of(navamsa_lord) == ninth_sign:
            return _verdict(
                key, True,
                f"{GRAHA_NAMES[navamsa_lord]}, lord of the navamsa sign of "
                f"the {ordinal(house)} lord {GRAHA_NAMES[lord]}, is exalted "
                f"and joins the 9th lord {GRAHA_NAMES[ninth]}",
                participants=tuple(sorted({navamsa_lord, ninth})))
        tried.append(f"{ordinal(house)} lord {GRAHA_NAMES[lord]} → "
                     f"{GRAHA_NAMES[navamsa_lord]}")
    return _verdict(key, False,
                    "no navamsa dispositor is both exalted and with the 9th "
                    f"lord {GRAHA_NAMES[ninth]}: " + "; ".join(tried))


def _detect_saraswathi(data: YogaInput) -> YogaVerdict:
    key = "saraswathi"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    allowed = (*KENDRA_OR_TRIKONA, 2)
    failures = []
    for graha in (MERCURY, JUPITER, VENUS):
        house = houses_of(data, graha)
        if house not in allowed:
            failures.append(f"{GRAHA_NAMES[graha]} is in the {ordinal(house)}"
                            if house else
                            f"{GRAHA_NAMES[graha]} has no placement")
    if not (in_own_sign(data, JUPITER) or in_friendly_sign(data, JUPITER)
            or in_exaltation(data, JUPITER)):
        failures.append("Jupiter is in neither an own nor a friendly nor an "
                        "exaltation sign")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "Mercury, Jupiter and Venus each hold a quadrant, a trine "
                    "or the 2nd, and Jupiter is well placed by sign",
                    participants=(MERCURY, JUPITER, VENUS))


def _detect_amsaavatara(data: YogaInput) -> YogaVerdict:
    key = "amsaavatara"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    for graha in (JUPITER, VENUS, SATURN):
        house = houses_of(data, graha)
        if house not in KENDRA:
            failures.append(f"{GRAHA_NAMES[graha]} is in the {ordinal(house)}"
                            if house else
                            f"{GRAHA_NAMES[graha]} has no placement")
    if not in_exaltation(data, SATURN):
        failures.append("Saturn is not exalted")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "Jupiter, Venus and an exalted Saturn all hold quadrants",
                    participants=(JUPITER, VENUS, SATURN))


def _detect_devendra(data: YogaInput) -> YogaVerdict:
    key = "devendra"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    if RASI_MODALITY[data.lagna_rasi] != 1:
        failures.append(f"lagna is in {RASI_NAMES[data.lagna_rasi]}, not a "
                        f"fixed sign")
    if not exchange(data, 2, 10):
        failures.append("the 2nd and 10th lords have no exchange")
    if not exchange(data, 1, 11):
        failures.append("the lagna and 11th lords have no exchange")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "a fixed lagna, with the 2nd and 10th lords exchanged and "
                    "the lagna and 11th lords exchanged",
                    participants=tuple(sorted(
                        {lord_of_house(data, h) for h in (1, 2, 10, 11)})))


def _detect_indra(data: YogaInput) -> YogaVerdict:
    key = "indra"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    if not exchange(data, 5, 11):
        failures.append("the 5th and 11th lords have no exchange")
    if houses_of(data, MOON) != 5:
        failures.append("Moon is not in the 5th")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the 5th and 11th lords have exchanged, and Moon holds "
                    "the 5th",
                    participants=tuple(sorted(
                        {lord_of_house(data, 5), lord_of_house(data, 11), MOON})))


def _detect_ravi(data: YogaInput) -> YogaVerdict:
    """Not one of §11.2's four Ravi *yogas* — a yoga of this name."""
    key = "ravi"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    if houses_of(data, SUN) != 10:
        failures.append("Sun is not in the 10th")
    tenth = lord_of_house(data, 10)
    if houses_of(data, tenth) != 3:
        failures.append(f"the 10th lord {GRAHA_NAMES[tenth]} is not in the 3rd")
    elif data.sign_of(SATURN) != data.sign_of(tenth):
        failures.append(f"Saturn is not with the 10th lord "
                        f"{GRAHA_NAMES[tenth]}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    itself = tenth == SATURN
    _note = ("the 10th lord is Saturn himself, so “with Saturn” is met by "
             "identity rather than by a companion; section 11.6 does not say "
             "whether it intends a second planet")
    extra: tuple[str, ...] = (_note,) if itself else ()
    return _verdict(key, True,
                    f"Sun holds the 10th and the 10th lord "
                    f"{GRAHA_NAMES[tenth]} is in the 3rd"
                    + (" — he is Saturn himself" if itself else " with Saturn"),
                    participants=tuple(sorted({SUN, tenth, SATURN})),
                    extra_qualifiers=extra)


def _detect_bhaaskara(data: YogaInput) -> YogaVerdict:
    key = "bhaaskara"
    sun, moon = data.sign_of(SUN), data.sign_of(MOON)
    if sun is None or moon is None:
        return _verdict(key, False,
                        f"{'Sun' if sun is None else 'Moon'} has no placement")
    failures = []
    if (moon - sun) % 12 + 1 != 12:
        failures.append(f"Moon is the {ordinal((moon - sun) % 12 + 1)} from "
                        f"Sun, not the 12th")
    mercury = data.sign_of(MERCURY)
    if mercury is None or (mercury - sun) % 12 + 1 != 2:
        failures.append("Mercury is not in the 2nd from Sun")
    jupiter = data.sign_of(JUPITER)
    if jupiter is None or (jupiter - moon) % 12 + 1 not in (5, 9):
        failures.append("Jupiter is in neither the 5th nor the 9th from Moon")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "Moon in the 12th from Sun, Mercury in the 2nd from Sun, "
                    "and Jupiter in a trine from Moon",
                    participants=(SUN, MOON, MERCURY, JUPITER))


def _detect_kulavardhana(data: YogaInput) -> YogaVerdict:
    """"each planet occupies the 5th house from **either** lagna or Moon or
    Sun" — three signs, and every placed planet must be in one of them."""
    key = "kulavardhana"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    bases = {"lagna": data.lagna_rasi}
    for label, graha in (("Moon", MOON), ("Sun", SUN)):
        sign = data.sign_of(graha)
        if sign is None:
            return _verdict(key, False, f"{label} has no placement")
        bases[label] = sign
    targets = {house_sign(sign, 5) for sign in bases.values()}
    outside = [GRAHA_NAMES[g] for g in sorted(data.rasis)
               if data.rasis[g] not in targets]
    if outside:
        named = ", ".join(RASI_NAMES[s] for s in sorted(targets))
        return _verdict(key, False,
                        f"{', '.join(outside)} "
                        f"{'is' if len(outside) == 1 else 'are'} outside the "
                        f"5th from lagna, Moon or Sun ({named})")
    return _verdict(key, True,
                    "every planet holds the 5th from lagna, Moon or Sun",
                    participants=tuple(sorted(data.rasis)))


def _detect_vasumati(data: YogaInput) -> YogaVerdict:
    """"If benefics occupy upachayas." The reference is unstated; lagna is
    used, as everywhere else in §11.6. The fullness clause is reported as a
    qualifier, not as part of the test — see OI-84."""
    key = "vasumati"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    inside = tuple(g for g in sorted(good) if houses_of(data, g) in UPACHAYA)
    if not inside:
        return _verdict(key, False,
                        "no natural benefic occupies an upachaya (3rd, 6th, "
                        "10th or 11th) from lagna")
    malefics = [GRAHA_NAMES[g] for g in sorted(data.rasis)
                if g not in good and houses_of(data, g) in UPACHAYA]
    extra = []
    outside = [GRAHA_NAMES[g] for g in sorted(good) if g not in inside]
    if outside:
        extra.append(f"{', '.join(outside)} "
                     f"{'is' if len(outside) == 1 else 'are'} a benefic "
                     f"outside the upachayas; a stricter reading of "
                     f"“benefics occupy upachayas” would want all of them "
                     f"there. See OI-84")
    if malefics:
        extra.append(f"section 11.6 says full results need no malefic in an "
                     f"upachaya; {', '.join(malefics)} "
                     f"{'is' if len(malefics) == 1 else 'are'} there")
    verb = "occupies" if len(inside) == 1 else "occupy"
    return _verdict(key, True,
                    f"{', '.join(GRAHA_NAMES[g] for g in inside)} {verb} "
                    f"upachayas (3rd, 6th, 10th, 11th) from lagna",
                    participants=inside, extra_qualifiers=tuple(extra))


def _detect_gandharva(data: YogaInput) -> YogaVerdict:
    key = "gandharva"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    tenth = lord_of_house(data, 10)
    tenth_sign, seventh_sign = data.sign_of(tenth), house_sign(data.lagna_rasi, 7)
    if tenth_sign is None or (tenth_sign - seventh_sign) % 12 + 1 not in TRIKONA:
        failures.append(f"the 10th lord {GRAHA_NAMES[tenth]} is not in a "
                        f"trine from the 7th")
    lagna_lord = lord_of_house(data, 1)
    lord_sign = data.sign_of(lagna_lord)
    if lord_sign is None or not conjoins_or_aspects(data, JUPITER, lord_sign):
        failures.append(f"Jupiter neither joins nor aspects the lagna lord "
                        f"{GRAHA_NAMES[lagna_lord]}")
    if not in_exaltation(data, SUN):
        failures.append("Sun is not exalted")
    if houses_of(data, MOON) != 9:
        failures.append("Moon is not in the 9th")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the 10th lord in a trine from the 7th, Jupiter on the "
                    "lagna lord, an exalted Sun and Moon in the 9th",
                    participants=tuple(sorted(
                        {tenth, lagna_lord, JUPITER, SUN, MOON})))


def _detect_go(data: YogaInput) -> YogaVerdict:
    key = "go"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    if not in_moolatrikona(data, JUPITER):
        failures.append(f"Jupiter is not in his moolatrikona "
                        f"({RASI_NAMES[int(MOOLATRIKONA[Graha.JUPITER][0])]})")
    second = lord_of_house(data, 2)
    if data.sign_of(second) != data.sign_of(JUPITER):
        failures.append(f"the 2nd lord {GRAHA_NAMES[second]} is not with "
                        f"Jupiter")
    lagna_lord = lord_of_house(data, 1)
    if not in_exaltation(data, lagna_lord):
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not "
                        f"exalted")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"Jupiter in his moolatrikona with the 2nd lord "
                    f"{GRAHA_NAMES[second]}, and an exalted lagna lord "
                    f"{GRAHA_NAMES[lagna_lord]}",
                    participants=tuple(sorted({JUPITER, second, lagna_lord})))


def _detect_vidyut(data: YogaInput) -> YogaVerdict:
    key = "vidyut"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    eleventh = lord_of_house(data, 11)
    deep, why = deep_exaltation(data, eleventh)
    if deep is False:
        return _verdict(key, False,
                        f"the 11th lord is not in deep exaltation — {why}")
    failures = []
    if data.sign_of(eleventh) != data.sign_of(VENUS):
        failures.append(f"the 11th lord {GRAHA_NAMES[eleventh]} is not with "
                        f"Venus")
    lagna_lord = lord_of_house(data, 1)
    lord_sign = data.sign_of(lagna_lord)
    pair_sign = data.sign_of(eleventh)
    if lord_sign is None or pair_sign is None or \
            not mutual_quadrants(lord_sign, pair_sign):
        failures.append(f"they are not in a quadrant from the lagna lord "
                        f"{GRAHA_NAMES[lagna_lord]}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, False,
                    f"every clause but the first holds: the 11th lord "
                    f"{GRAHA_NAMES[eleventh]} is with Venus in a quadrant "
                    f"from the lagna lord. Whether he is in *deep* exaltation "
                    f"cannot be decided — {why}",
                    extra_qualifiers=(("depth of exaltation is undecided; "
                                       "see docs/open-items.md OI-83"),))


def _detect_chapa(data: YogaInput) -> YogaVerdict:
    key = "chapa"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    if not exchange(data, 4, 10):
        failures.append("the 4th and 10th lords have no exchange")
    lagna_lord = lord_of_house(data, 1)
    if not in_exaltation(data, lagna_lord):
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not "
                        f"exalted")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the 4th and 10th lords have exchanged, and the lagna "
                    "lord is exalted",
                    participants=tuple(sorted(
                        {lord_of_house(data, 4), lord_of_house(data, 10),
                         lagna_lord})))


def _detect_pushkala(data: YogaInput) -> YogaVerdict:
    """Four clauses, printed numbered (1), (2), (2), (4)."""
    key = "pushkala"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    lagna_lord = lord_of_house(data, 1)
    moon_sign = data.sign_of(MOON)
    if moon_sign is None:
        return _verdict(key, False, "Moon has no placement")
    if data.sign_of(lagna_lord) != moon_sign:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not "
                        f"with Moon")
    moon_lord = dispositor(data, MOON)
    if moon_lord is None:
        failures.append("Moon's dispositor has no placement")
    else:
        if houses_of(data, moon_lord) not in KENDRA and \
                not in_adhimitra_house(data, moon_lord):
            failures.append(f"Moon's dispositor {GRAHA_NAMES[moon_lord]} is "
                            f"in neither a quadrant nor an adhimitra's house")
        if not aspects_sign(data, moon_lord, data.lagna_rasi):
            failures.append(f"Moon's dispositor {GRAHA_NAMES[moon_lord]} does "
                            f"not aspect lagna")
    if not occupants_of_house(data, 1):
        failures.append("no planet is in lagna")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"the lagna lord {GRAHA_NAMES[lagna_lord]} is with Moon, "
                    f"Moon's dispositor is well placed and aspects lagna, and "
                    f"lagna is occupied",
                    participants=tuple(sorted(
                        {lagna_lord, MOON, *( () if moon_lord is None
                                              else (moon_lord,) )})))


def _detect_makuta(data: YogaInput) -> YogaVerdict:
    key = "makuta"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    ninth = lord_of_house(data, 9)
    ninth_sign, jupiter_sign = data.sign_of(ninth), data.sign_of(JUPITER)
    if ninth_sign is None or jupiter_sign is None:
        return _verdict(key, False,
                        "the 9th lord or Jupiter has no placement")
    if (jupiter_sign - ninth_sign) % 12 + 1 != 9:
        failures.append(f"Jupiter is the "
                        f"{ordinal((jupiter_sign - ninth_sign) % 12 + 1)} "
                        f"from the 9th lord {GRAHA_NAMES[ninth]}, not the 9th")
    ok, found = benefics_in(data, jupiter_sign, (9,))
    if not ok:
        failures.append("the 9th from Jupiter holds no benefic")
    if houses_of(data, SATURN) != 10:
        failures.append("Saturn is not in the 10th")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"Jupiter is in the 9th from the 9th lord "
                    f"{GRAHA_NAMES[ninth]}, the 9th from Jupiter holds a "
                    f"benefic, and Saturn is in the 10th",
                    participants=tuple(sorted({JUPITER, SATURN, *found[9]})))


def _detect_jaya(data: YogaInput) -> YogaVerdict:
    key = "jaya"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    tenth, sixth = lord_of_house(data, 10), lord_of_house(data, 6)
    deep, why = deep_exaltation(data, tenth)
    if deep is False:
        return _verdict(key, False,
                        f"the 10th lord is not in deep exaltation — {why}")
    if not is_debilitated(data, sixth):
        return _verdict(key, False,
                        f"the 6th lord {GRAHA_NAMES[sixth]} is not debilitated")
    return _verdict(key, False,
                    f"the 6th lord {GRAHA_NAMES[sixth]} is debilitated, but "
                    f"whether the 10th lord is in *deep* exaltation cannot be "
                    f"decided — {why}",
                    extra_qualifiers=(("depth of exaltation is undecided; "
                                       "see docs/open-items.md OI-83"),))


def _lord_in_own_house(key: str, house: int):
    """Harsha (6th), Sarala (8th) and Vimala (12th) — one rule, three houses."""
    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return _needs_lagna(key)
        lord = lord_of_house(data, house)
        where = houses_of(data, lord)
        if where != house:
            return _verdict(key, False,
                            f"the {ordinal(house)} lord {GRAHA_NAMES[lord]} "
                            f"is in the {ordinal(where)}, not the "
                            f"{ordinal(house)}" if where else
                            f"the {ordinal(house)} lord {GRAHA_NAMES[lord]} "
                            f"has no placement")
        return _verdict(key, True,
                        f"the {ordinal(house)} lord {GRAHA_NAMES[lord]} "
                        f"occupies the {ordinal(house)}",
                        participants=(lord,), houses={lord: house})
    return detect


_DETECTORS = {
    "lagnaadhi": _detect_lagnaadhi,
    "hari": _from_a_lord("hari", 2, (2, 12, 8)),
    "hara": _from_a_lord("hara", 7, (4, 9, 8)),
    "brahma": _from_a_lord("brahma", 1, (4, 10, 11)),
    "vishnu": _detect_vishnu,
    "siva": _detect_siva,
    "trilochana": _detect_trilochana,
    "gouri": _detect_gouri,
    "chandikaa": _detect_chandikaa,
    "lakshmi": _detect_lakshmi,
    "saarada": _detect_saarada,
    "bhaarathi": _detect_bhaarathi,
    "saraswathi": _detect_saraswathi,
    "amsaavatara": _detect_amsaavatara,
    "devendra": _detect_devendra,
    "indra": _detect_indra,
    "ravi": _detect_ravi,
    "bhaaskara": _detect_bhaaskara,
    "kulavardhana": _detect_kulavardhana,
    "vasumati": _detect_vasumati,
    "gandharva": _detect_gandharva,
    "go": _detect_go,
    "vidyut": _detect_vidyut,
    "chapa": _detect_chapa,
    "pushkala": _detect_pushkala,
    "makuta": _detect_makuta,
    "jaya": _detect_jaya,
    "harsha": _lord_in_own_house("harsha", 6),
    "sarala": _lord_in_own_house("sarala", 8),
    "vimala": _lord_in_own_house("vimala", 12),
}

for _key, _entry in _SPEC.items():
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=tuple(_entry.get("aliases", ())),
        section="11.6",
        group="popular",
        definition=_entry["definition"],
        detect=_DETECTORS[_key],
    ))
