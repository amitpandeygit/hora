"""§11.6 Other popular yogas — eighteen combinations.

**Nothing here is ever reported as fully present.** §11.6's preamble binds the
whole section: "for a yoga to be fully present, all the required combinations
must be present *and the participating planets must be strong*." Chapter 15's
simple-rules strength measure is not built, so every verdict carries
`STRENGTH_NOT_ASSESSED` and reports the combinations only. Five of the
eighteen name a strength requirement outright, and those name it in their
reason as well. See OI-81.

Footnote 31's **kartari** is built here as its own function rather than inside
the two yogas that use it, because the footnote says so: "they can be seen
with reference to any house or planet."
"""
from __future__ import annotations

from dataclasses import replace

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import house_sign, ordinal
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.charts.relationship import natural
from hora.charts.vargas import d9_navamsa
from hora.core.const import (
    DEBILITATION_RASI,
    EXALTATION_DEG,
    GRAHA_NAMES,
    KARTARI_HOUSES,
    KENDRA,
    POPULAR_YOGAS,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
    STRENGTH_NOT_ASSESSED,
    TRIKONA,
    Graha,
)

__all__ = [
    "dispositor", "houses_of", "in_exaltation", "in_own_sign", "kartari",
    "lord_of_house", "occupants_of_house",
]


def lord_of_house(data: YogaInput, house: int) -> int:
    """The lord of the Nth house from lagna. `lagna_rasi` must be set."""
    assert data.lagna_rasi is not None
    return int(RASI_LORD[house_sign(data.lagna_rasi, house)])


def occupants_of_house(data: YogaInput, house: int) -> tuple[int, ...]:
    """Every placed graha in the Nth house from lagna, nodes included.

    §11.6 speaks of "planets" occupying houses and of "benefics"/"malefics"
    by nature, and §3.2.2 makes the nodes natural malefics — so they count
    here, as they do for the Dala yogas. `include_nodes` governs the
    unresolved phrase "a planet" in §11.2, §11.3 and §11.5.1 only.
    """
    assert data.lagna_rasi is not None
    sign = house_sign(data.lagna_rasi, house)
    return tuple(int(g) for g in sorted(data.rasis) if data.rasis[g] == sign)


def houses_of(data: YogaInput, graha: int) -> int | None:
    """Which house from lagna a graha occupies, or None if unplaced."""
    sign = data.sign_of(graha)
    if sign is None or data.lagna_rasi is None:
        return None
    return (sign - data.lagna_rasi) % 12 + 1


def dispositor(data: YogaInput, graha: int) -> int | None:
    """The lord of the sign a graha occupies."""
    sign = data.sign_of(graha)
    return None if sign is None else int(RASI_LORD[sign])


def in_own_sign(data: YogaInput, graha: int) -> bool:
    sign = data.sign_of(graha)
    return sign is not None and int(RASI_LORD[sign]) == int(graha)


def in_exaltation(data: YogaInput, graha: int) -> bool:
    sign = data.sign_of(graha)
    exalted = EXALTATION_DEG.get(graha)
    return sign is not None and exalted is not None and int(exalted // 30) == sign


def kartari(data: YogaInput, sign: int) -> dict:
    """Footnote 31 — what the 2nd and 12th from a sign cast on it.

    "The 12th and 2nd houses from a house cast kartari on it. If the 2nd and
    12th from a house have benefics, it is said to have a subha (benefic)
    kartari. Malefics in the same places cause paapa (malefic) kartari."

    **Both** flanking houses must carry the nature — "the 2nd *and* 12th" —
    so a benefic on one side and a malefic on the other is neither.

    :returns: ``{"subha": bool, "paapa": bool, "flanks": {house: (grahas,)}}``
    """
    benefics, _ = data.benefics()
    benefic_set = {int(g) for g in benefics}

    flanks: dict[int, tuple[int, ...]] = {}
    for house in KARTARI_HOUSES:
        target = house_sign(sign, house)
        flanks[house] = tuple(
            int(g) for g in sorted(data.rasis) if data.rasis[g] == target)

    def _all(nature_is_benefic: bool) -> bool:
        return all(
            grahas and all((g in benefic_set) is nature_is_benefic
                           for g in grahas)
            for grahas in flanks.values()
        )

    return {"subha": _all(True), "paapa": _all(False), "flanks": flanks}


def describe_flanks(flanks: dict[int, tuple[int, ...]], sign: int) -> str:
    parts = []
    for house, grahas in sorted(flanks.items()):
        where = RASI_NAMES[house_sign(sign, house)]
        who = ", ".join(GRAHA_NAMES[g] for g in grahas) or "empty"
        parts.append(f"the {ordinal(house)} ({where}) {who}")
    return "; ".join(parts)


#: Grahas §11.6 names by name, for the yogas that do.
JUPITER = int(Graha.JUPITER)
VENUS = int(Graha.VENUS)
MERCURY = int(Graha.MERCURY)
MARS = int(Graha.MARS)
MOON = int(Graha.MOON)
SATURN = int(Graha.SATURN)


# --------------------------------------------------------------------------
# Shared predicates
# --------------------------------------------------------------------------

_SPEC = {entry["key"]: entry for entry in POPULAR_YOGAS}

#: §11.6's Mridanga and Khadga read "quadrants and trines" as one region.
KENDRA_OR_TRIKONA: tuple[int, ...] = tuple(sorted(set(KENDRA) | set(TRIKONA)))


def benefic_set(data: YogaInput) -> set[int]:
    benefics, _ = data.benefics()
    return {int(g) for g in benefics}


def mutual_quadrants(sign_a: int, sign_b: int) -> bool:
    """Footnote 17's definition, reused: one is in a quadrant from the other."""
    return (sign_b - sign_a) % 12 + 1 in KENDRA


def conjoins_or_aspects(data: YogaInput, graha: int, target_sign: int) -> bool:
    """"conjoins or aspects" — the same sign, or graha drishti onto it."""
    sign = data.sign_of(graha)
    if sign is None:
        return False
    return sign == target_sign or graha_aspects_sign(graha, sign, target_sign)


def is_debilitated(data: YogaInput, graha: int) -> bool:
    sign = data.sign_of(graha)
    return sign is not None and DEBILITATION_RASI.get(graha) == sign


def in_enemy_sign(data: YogaInput, graha: int) -> bool:
    sign = data.sign_of(graha)
    if sign is None:
        return False
    lord = int(RASI_LORD[sign])
    return lord != int(graha) and natural(int(graha), lord) == "enemy"


def in_friendly_sign(data: YogaInput, graha: int) -> bool:
    sign = data.sign_of(graha)
    if sign is None:
        return False
    lord = int(RASI_LORD[sign])
    return lord != int(graha) and natural(int(graha), lord) == "friend"


def _needs_lagna(key: str) -> YogaVerdict:
    return YogaVerdict(
        key=key, name=_SPEC[key]["name"], present=False,
        reason=("no lagna was supplied, and this yoga counts houses from "
                "lagna; it cannot be decided"),
    )


def _strength_note(key: str) -> tuple[str, ...]:
    """Every §11.6 verdict carries it; the five that name a lord say which."""
    spec = _SPEC[key]
    named = spec.get("strength", ())
    if not named:
        return (STRENGTH_NOT_ASSESSED,)
    who = ", ".join(named)
    return (
        STRENGTH_NOT_ASSESSED,
        (f"section 11.6 requires the {who} to be strong for this yoga; "
         f"that is not assessed"),
    )


def _verdict(key: str, present: bool, reason: str, **kw) -> YogaVerdict:
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=present,
                       reason=reason, qualifiers=_strength_note(key), **kw)


# --------------------------------------------------------------------------
# The eighteen
# --------------------------------------------------------------------------


def _subha_or_asubha(key: str, want_benefic: bool):
    """§11.6's first two: "If lagna **has** benefics **or has** kartari"."""
    word = "benefic" if want_benefic else "malefic"
    kind = "subha" if want_benefic else "paapa"

    def detect(data: YogaInput) -> YogaVerdict:
        if data.lagna_rasi is None:
            return _needs_lagna(key)
        good = benefic_set(data)
        inside = [g for g in occupants_of_house(data, 1)
                  if (g in good) is want_benefic]
        cut = kartari(data, data.lagna_rasi)
        if inside:
            named = ", ".join(GRAHA_NAMES[g] for g in inside)
            return _verdict(key, True, f"lagna holds {named}",
                            participants=tuple(sorted(inside)),
                            houses=dict.fromkeys(inside, 1))
        if cut[kind]:
            flanking = tuple(sorted(g for gs in cut["flanks"].values() for g in gs))
            return _verdict(
                key, True,
                f"lagna has {kind} kartari — "
                f"{describe_flanks(cut['flanks'], data.lagna_rasi)}",
                participants=flanking)
        return _verdict(
            key, False,
            f"lagna holds no {word} and has no {kind} kartari — "
            f"{describe_flanks(cut['flanks'], data.lagna_rasi)}")

    return detect


def _detect_gaja_kesari(data: YogaInput) -> YogaVerdict:
    """Three clauses, all computable except combustion without positions."""
    key = "gaja_kesari"
    jupiter_sign = data.sign_of(JUPITER)
    moon_sign = data.sign_of(MOON)
    if jupiter_sign is None or moon_sign is None:
        missing = "Jupiter" if jupiter_sign is None else "Moon"
        return _verdict(key, False, f"{missing} has no placement")

    failures = []
    if not mutual_quadrants(moon_sign, jupiter_sign):
        house = (jupiter_sign - moon_sign) % 12 + 1
        failures.append(f"Jupiter is the {ordinal(house)} from Moon, not a quadrant")

    good = benefic_set(data) - {JUPITER}
    helpers = [g for g in sorted(good) if conjoins_or_aspects(data, g, jupiter_sign)]
    if not helpers:
        failures.append("no benefic conjoins or aspects Jupiter")

    if is_debilitated(data, JUPITER):
        failures.append(f"Jupiter is debilitated in {RASI_NAMES[jupiter_sign]}")
    if in_enemy_sign(data, JUPITER):
        failures.append(f"Jupiter is in an enemy's house, {RASI_NAMES[jupiter_sign]}")

    combust = None
    if data.positions and JUPITER in data.positions and int(Graha.SUN) in data.positions:
        from hora.charts.dignity import combustion
        combust = combustion(JUPITER, data.positions).combust
        if combust:
            failures.append("Jupiter is combust")

    if failures:
        return _verdict(key, False, "; ".join(failures))
    reason = (f"Jupiter is in a quadrant from Moon, "
              f"{', '.join(GRAHA_NAMES[g] for g in helpers)} "
              f"{'conjoins or aspects' if len(helpers) == 1 else 'conjoin or aspect'} "
              f"him, and he is neither debilitated nor in an enemy's house")
    verdict = _verdict(key, True, reason,
                       participants=(JUPITER, *helpers),
                       houses={JUPITER: (jupiter_sign - moon_sign) % 12 + 1})
    if combust is None:
        verdict = replace(
            verdict,
            qualifiers=(*verdict.qualifiers,
                        "combustion could not be judged without longitudes"))
    return verdict


def _detect_guru_mangala(data: YogaInput) -> YogaVerdict:
    key = "guru_mangala"
    jupiter, mars = data.sign_of(JUPITER), data.sign_of(MARS)
    if jupiter is None or mars is None:
        return _verdict(key, False,
                        f"{'Jupiter' if jupiter is None else 'Mars'} has no placement")
    house = (mars - jupiter) % 12 + 1
    if house in (1, 7):
        how = "together" if house == 1 else "in the 7th from each other"
        return _verdict(key, True,
                        f"Jupiter in {RASI_NAMES[jupiter]} and Mars in "
                        f"{RASI_NAMES[mars]} are {how}",
                        participants=(JUPITER, MARS))
    return _verdict(key, False,
                    f"Mars is the {ordinal(house)} from Jupiter, neither "
                    f"together nor the 7th")


def _only_benefics_in(data: YogaInput, house: int, base_sign: int) -> tuple[bool, tuple[int, ...]]:
    """Occupied, and every occupant a natural benefic."""
    sign = house_sign(base_sign, house)
    grahas = tuple(int(g) for g in sorted(data.rasis) if data.rasis[g] == sign)
    good = benefic_set(data)
    return bool(grahas) and all(g in good for g in grahas), grahas


def _detect_amala(data: YogaInput) -> YogaVerdict:
    """"only natural benefics in the 10th house from lagna **or** Moon"."""
    key = "amala"
    bases = []
    if data.lagna_rasi is not None:
        bases.append(("lagna", data.lagna_rasi))
    moon = data.sign_of(MOON)
    if moon is not None:
        bases.append(("Moon", moon))
    if not bases:
        return _verdict(key, False, "neither a lagna nor the Moon was supplied")

    for label, base in bases:
        ok, grahas = _only_benefics_in(data, 10, base)
        if ok:
            named = ", ".join(GRAHA_NAMES[g] for g in grahas)
            return _verdict(key, True,
                            f"the 10th from {label} holds only natural "
                            f"benefics — {named}",
                            participants=grahas,
                            houses=dict.fromkeys(grahas, 10))
    parts = []
    for label, base in bases:
        _, grahas = _only_benefics_in(data, 10, base)
        who = ", ".join(GRAHA_NAMES[g] for g in grahas) or "empty"
        parts.append(f"the 10th from {label} is {who}")
    return _verdict(key, False, "; ".join(parts))


def _detect_parvata(data: YogaInput) -> YogaVerdict:
    key = "parvata"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    offenders = []
    for house in KENDRA:
        for graha in occupants_of_house(data, house):
            if graha not in good:
                offenders.append(f"{GRAHA_NAMES[graha]} in the {ordinal(house)}")
    for house in (7, 8):
        for graha in occupants_of_house(data, house):
            if graha not in good:
                offenders.append(f"{GRAHA_NAMES[graha]} in the {ordinal(house)}")
    if offenders:
        return _verdict(key, False,
                        "a malefic occupies " + ", ".join(sorted(set(offenders))))
    inside = tuple(sorted({g for h in (*KENDRA, 8)
                           for g in occupants_of_house(data, h)}))
    return _verdict(key, True,
                    "the quadrants hold only benefics, and the 7th and 8th are "
                    "vacant or hold only benefics",
                    participants=inside)


def _detect_kaahala(data: YogaInput) -> YogaVerdict:
    key = "kaahala"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fourth_lord = lord_of_house(data, 4)
    fourth_sign = data.sign_of(fourth_lord)
    jupiter = data.sign_of(JUPITER)
    if fourth_sign is not None and jupiter is not None \
            and mutual_quadrants(fourth_sign, jupiter):
        return _verdict(key, True,
                        f"the 4th lord {GRAHA_NAMES[fourth_lord]} and Jupiter "
                        f"are in mutual quadrants",
                        participants=tuple(sorted({fourth_lord, JUPITER})))
    tenth_lord = lord_of_house(data, 10)
    if (in_exaltation(data, fourth_lord) or in_own_sign(data, fourth_lord)) \
            and fourth_sign is not None \
            and data.sign_of(tenth_lord) == fourth_sign:
        kind = "exalted" if in_exaltation(data, fourth_lord) else "in own sign"
        return _verdict(key, True,
                        f"the 4th lord {GRAHA_NAMES[fourth_lord]} is {kind} in "
                        f"{RASI_NAMES[fourth_sign]} and the 10th lord "
                        f"{GRAHA_NAMES[tenth_lord]} joins him",
                        participants=tuple(sorted({fourth_lord, tenth_lord})))
    return _verdict(key, False,
                    "neither the 4th lord and Jupiter in mutual quadrants, nor "
                    "the 4th lord dignified with the 10th lord joining him")


def _detect_chaamara(data: YogaInput) -> YogaVerdict:
    key = "chaamara"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    lagna_lord = lord_of_house(data, 1)
    lord_sign = data.sign_of(lagna_lord)
    if lord_sign is not None and in_exaltation(data, lagna_lord):
        house = (lord_sign - data.lagna_rasi) % 12 + 1
        if house in KENDRA and conjoins_or_aspects(data, JUPITER, lord_sign) \
                and data.sign_of(JUPITER) != lord_sign:
            return _verdict(key, True,
                            f"the lagna lord {GRAHA_NAMES[lagna_lord]} is "
                            f"exalted in {RASI_NAMES[lord_sign]}, the "
                            f"{ordinal(house)}, with Jupiter's aspect",
                            participants=(lagna_lord, JUPITER))
    good = benefic_set(data)
    for house in (7, 9, 10):
        grahas = [g for g in occupants_of_house(data, house) if g in good]
        if len(grahas) >= 2:
            named = ", ".join(GRAHA_NAMES[g] for g in grahas)
            return _verdict(key, True,
                            f"{named} — two benefics — join in the "
                            f"{ordinal(house)}",
                            participants=tuple(grahas),
                            houses=dict.fromkeys(grahas, house))
    return _verdict(key, False,
                    "the lagna lord is not exalted in a quadrant with "
                    "Jupiter's aspect, and no two benefics join in the 7th, "
                    "9th or 10th")


def _detect_sankha(data: YogaInput) -> YogaVerdict:
    key = "sankha"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    fifth, sixth = lord_of_house(data, 5), lord_of_house(data, 6)
    a, b = data.sign_of(fifth), data.sign_of(sixth)
    if a is not None and b is not None and mutual_quadrants(a, b):
        return _verdict(key, True,
                        f"the 5th lord {GRAHA_NAMES[fifth]} and 6th lord "
                        f"{GRAHA_NAMES[sixth]} are in mutual quadrants",
                        participants=tuple(sorted({fifth, sixth})))
    lagna_lord, tenth = lord_of_house(data, 1), lord_of_house(data, 10)
    x, y = data.sign_of(lagna_lord), data.sign_of(tenth)
    if x is not None and x == y and RASI_MODALITY[x] == 0:
        return _verdict(key, True,
                        f"the lagna lord {GRAHA_NAMES[lagna_lord]} and 10th "
                        f"lord {GRAHA_NAMES[tenth]} are together in "
                        f"{RASI_NAMES[x]}, a movable sign",
                        participants=tuple(sorted({lagna_lord, tenth})))
    return _verdict(key, False,
                    "neither the 5th and 6th lords in mutual quadrants, nor "
                    "the lagna and 10th lords together in a movable sign")


def _detect_bheri(data: YogaInput) -> YogaVerdict:
    key = "bheri"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    wanted = (1, 2, 7, 12)
    empty = [h for h in wanted if not occupants_of_house(data, h)]
    if not empty:
        inside = tuple(sorted({g for h in wanted
                               for g in occupants_of_house(data, h)}))
        return _verdict(key, True,
                        "the 1st, 2nd, 7th and 12th are all occupied",
                        participants=inside)
    lagna_lord = lord_of_house(data, 1)
    raw = [data.sign_of(g) for g in (JUPITER, VENUS, lagna_lord)]
    signs = [s for s in raw if s is not None]
    if len(signs) == 3 and all(
            mutual_quadrants(signs[i], signs[j])
            for i in range(3) for j in range(i + 1, 3)):
        return _verdict(key, True,
                        f"Jupiter, Venus and the lagna lord "
                        f"{GRAHA_NAMES[lagna_lord]} are in mutual quadrants",
                        participants=tuple(sorted({JUPITER, VENUS, lagna_lord})))
    return _verdict(key, False,
                    f"the {', '.join(ordinal(h) for h in empty)} "
                    f"{'is' if len(empty) == 1 else 'are'} vacant, and "
                    f"Jupiter, Venus and the lagna lord are not in mutual "
                    f"quadrants")


def _detect_mridanga(data: YogaInput) -> YogaVerdict:
    key = "mridanga"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    dignified = []
    for graha in sorted(data.rasis):
        if not (in_own_sign(data, graha) or in_exaltation(data, graha)):
            continue
        house = houses_of(data, graha)
        if house in KENDRA_OR_TRIKONA:
            dignified.append((graha, house))
    if dignified:
        named = ", ".join(f"{GRAHA_NAMES[g]} in the {ordinal(h)}"
                          for g, h in dignified)
        return _verdict(key, True,
                        f"{named} — in own or exaltation signs, in quadrants "
                        f"or trines",
                        participants=tuple(g for g, _ in dignified),
                        houses=dict(dignified))
    return _verdict(key, False,
                    "no planet is in its own or exaltation sign in a quadrant "
                    "or a trine")


def _detect_sreenaatha(data: YogaInput) -> YogaVerdict:
    key = "sreenaatha"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    seventh = lord_of_house(data, 7)
    tenth_sign = house_sign(data.lagna_rasi, 10)
    failures = []
    if not (in_exaltation(data, seventh) and data.sign_of(seventh) == tenth_sign):
        failures.append(f"the 7th lord {GRAHA_NAMES[seventh]} is not exalted "
                        f"in the 10th ({RASI_NAMES[tenth_sign]})")
    tenth, ninth = lord_of_house(data, 10), lord_of_house(data, 9)
    if data.sign_of(tenth) is None or data.sign_of(tenth) != data.sign_of(ninth):
        failures.append(f"the 10th lord {GRAHA_NAMES[tenth]} is not with the "
                        f"9th lord {GRAHA_NAMES[ninth]}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    f"the 7th lord {GRAHA_NAMES[seventh]} is exalted in the "
                    f"10th and the 10th lord is with the 9th lord",
                    participants=tuple(sorted({seventh, tenth, ninth})))


def _detect_matsya(data: YogaInput) -> YogaVerdict:
    key = "matsya"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    failures = []
    for house in (1, 9):
        grahas = occupants_of_house(data, house)
        if not any(g in good for g in grahas):
            failures.append(f"no benefic in the {ordinal(house)}")
    if not occupants_of_house(data, 5):
        failures.append("no planet in the 5th")
    for house in (4, 8):
        grahas = occupants_of_house(data, house)
        if not any(g not in good for g in grahas):
            failures.append(f"no malefic in the {ordinal(house)}")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    inside = tuple(sorted({g for h in (1, 4, 5, 8, 9)
                           for g in occupants_of_house(data, h)}))
    return _verdict(key, True,
                    "benefics in lagna and the 9th, planets in the 5th, and "
                    "malefics in the chaturasras",
                    participants=inside)


def _detect_koorma(data: YogaInput) -> YogaVerdict:
    key = "koorma"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    good = benefic_set(data)
    failures = []
    for house in (5, 6, 7):
        grahas = occupants_of_house(data, house)
        ok = [g for g in grahas if g in good and (
            in_own_sign(data, g) or in_exaltation(data, g) or in_friendly_sign(data, g))]
        if not ok:
            failures.append(f"the {ordinal(house)} has no benefic in an own, "
                            f"exaltation or friendly sign")
    for house in (1, 3, 11):
        grahas = occupants_of_house(data, house)
        ok = [g for g in grahas if g not in good and (
            in_own_sign(data, g) or in_exaltation(data, g))]
        if not ok:
            failures.append(f"the {ordinal(house)} has no malefic in an own or "
                            f"exaltation sign")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    inside = tuple(sorted({g for h in (1, 3, 5, 6, 7, 11)
                           for g in occupants_of_house(data, h)}))
    return _verdict(key, True,
                    "dignified benefics hold the 5th, 6th and 7th, and "
                    "dignified malefics the 1st, 3rd and 11th",
                    participants=inside)


def _detect_khadga(data: YogaInput) -> YogaVerdict:
    key = "khadga"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    second, ninth = lord_of_house(data, 2), lord_of_house(data, 9)
    lagna_lord = lord_of_house(data, 1)
    failures = []
    if houses_of(data, second) != 9:
        failures.append(f"the 2nd lord {GRAHA_NAMES[second]} is not in the 9th")
    if houses_of(data, ninth) != 2:
        failures.append(f"the 9th lord {GRAHA_NAMES[ninth]} is not in the 2nd")
    house = houses_of(data, lagna_lord)
    if house not in KENDRA_OR_TRIKONA:
        failures.append(f"the lagna lord {GRAHA_NAMES[lagna_lord]} is not in a "
                        f"quadrant or a trine")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "the 2nd and 9th lords have exchanged houses and the lagna "
                    "lord is in a quadrant or a trine",
                    participants=tuple(sorted({second, ninth, lagna_lord})))


def _detect_kusuma(data: YogaInput) -> YogaVerdict:
    key = "kusuma"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    failures = []
    if RASI_MODALITY[data.lagna_rasi] != 1:
        failures.append(f"lagna is in {RASI_NAMES[data.lagna_rasi]}, not a fixed sign")
    if houses_of(data, VENUS) not in KENDRA:
        failures.append("Venus is not in a quadrant")
    moon_house = houses_of(data, MOON)
    moon_sign = data.sign_of(MOON)
    if moon_house not in TRIKONA:
        failures.append("Moon is not in a trine")
    else:
        good = benefic_set(data) - {MOON}
        with_moon = [g for g in sorted(data.rasis)
                     if g in good and data.rasis[g] == moon_sign]
        if not with_moon:
            failures.append("no benefic is with the Moon")
    if houses_of(data, SATURN) != 10:
        failures.append("Saturn is not in the 10th")
    if failures:
        return _verdict(key, False, "; ".join(failures))
    return _verdict(key, True,
                    "a fixed lagna, Venus in a quadrant, the Moon in a trine "
                    "with a benefic, and Saturn in the 10th",
                    participants=tuple(sorted({VENUS, MOON, SATURN})))


def _detect_kalaanidhi(data: YogaInput) -> YogaVerdict:
    key = "kalaanidhi"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    house = houses_of(data, JUPITER)
    if house not in (2, 5):
        return _verdict(key, False,
                        f"Jupiter is in the {ordinal(house)}, not the 2nd or 5th"
                        if house else "Jupiter has no placement")
    jupiter_sign = data.sign_of(JUPITER)
    assert jupiter_sign is not None
    missing = [GRAHA_NAMES[g] for g in (MERCURY, VENUS)
               if not conjoins_or_aspects(data, g, jupiter_sign)]
    if missing:
        return _verdict(key, False,
                        f"{' and '.join(missing)} neither "
                        f"{'conjoins nor aspects' if len(missing) == 1 else 'conjoin nor aspect'} "
                        f"Jupiter")
    return _verdict(key, True,
                    f"Jupiter is in the {ordinal(house)} and both Mercury and "
                    f"Venus conjoin or aspect him",
                    participants=(MERCURY, JUPITER, VENUS),
                    houses={JUPITER: house})


def _detect_kalpadruma(data: YogaInput) -> YogaVerdict:
    """The four-planet chain §11.6 insists on keeping whole.

    "Some authors have simplified this yoga... Taking all the four planets
    make this a less common yoga, which it ought to be. Let us follow
    Parasara."
    """
    key = "kalpadruma"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    lagna_lord = lord_of_house(data, 1)
    second = dispositor(data, lagna_lord)
    third = dispositor(data, second) if second is not None else None
    # Links 3 and 4 are both dispositors of "the latter" — the lagna lord's
    # own dispositor — one read in rasi, one in navamsa.
    navamsa_sign = None
    if second is not None and data.positions and second in data.positions:
        navamsa_sign = d9_navamsa(data.positions[second].longitude).sign
    if second is None or third is None:
        return _verdict(key, False,
                        "the dispositor chain from the lagna lord is "
                        "incomplete; some link has no placement")
    chain = [lagna_lord, second, third]
    fourth = int(RASI_LORD[navamsa_sign]) if navamsa_sign is not None else None
    if fourth is None:
        return _verdict(
            key, False,
            "the fourth link is a navamsa dispositor, which needs longitudes; "
            "it cannot be decided from signs alone")
    chain.append(fourth)

    failures = []
    for graha in chain:
        house = houses_of(data, graha)
        if house in KENDRA_OR_TRIKONA or in_exaltation(data, graha):
            continue
        failures.append(f"{GRAHA_NAMES[graha]} is in the {ordinal(house)}"
                        if house else f"{GRAHA_NAMES[graha]} has no placement")
    if failures:
        return _verdict(key, False,
                        "not every link is in a quadrant, trine or exaltation "
                        "sign: " + "; ".join(failures))
    return _verdict(key, True,
                    "the lagna lord, his dispositor, that one's rasi "
                    "dispositor and its navamsa dispositor are all in "
                    "quadrants, trines or exaltation signs",
                    participants=tuple(sorted(set(chain))))


_DETECTORS = {
    "subha": _subha_or_asubha("subha", True),
    "asubha": _subha_or_asubha("asubha", False),
    "gaja_kesari": _detect_gaja_kesari,
    "guru_mangala": _detect_guru_mangala,
    "amala": _detect_amala,
    "parvata": _detect_parvata,
    "kaahala": _detect_kaahala,
    "chaamara": _detect_chaamara,
    "sankha": _detect_sankha,
    "bheri": _detect_bheri,
    "mridanga": _detect_mridanga,
    "sreenaatha": _detect_sreenaatha,
    "matsya": _detect_matsya,
    "koorma": _detect_koorma,
    "khadga": _detect_khadga,
    "kusuma": _detect_kusuma,
    "kalaanidhi": _detect_kalaanidhi,
    "kalpadruma": _detect_kalpadruma,
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
