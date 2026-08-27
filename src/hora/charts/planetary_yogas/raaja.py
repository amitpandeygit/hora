"""§11.7.1 — the three Raaja yogas.

"Raaja means a king. Raaja yogas are the combinations that give power and
prosperity to a native. They make one the best in something."

The first is not one combination but a family: **every** quadrant lord paired
with **every** trine lord, tested for the three associations §11.7.1 names.
Lagna counts on both sides — "It is both" — so the lagna lord is a quadrant
lord and a trine lord at once.

Unlike §11.6, nothing here asks for strength, so these verdicts carry no
strength note.
"""
from __future__ import annotations

from hora.charts.aspects import graha_aspects_sign
from hora.charts.planetary_yogas._shared import ordinal
from hora.charts.planetary_yogas.popular import (
    houses_of,
    lord_of_house,
    occupants_of_house,
)
from hora.charts.planetary_yogas.registry import (
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import (
    DUSTHANA,
    GRAHA_NAMES,
    KENDRA,
    RAAJA_YOGAS,
    RASI_LORD,
    RASI_NAMES,
    TRIKONA,
    VIPAREETA_IDEAL_HOUSES,
)

_SPEC = {entry["key"]: entry for entry in RAAJA_YOGAS}


def _verdict(key: str, present: bool, reason: str, **kw) -> YogaVerdict:
    return YogaVerdict(key=key, name=_SPEC[key]["name"], present=present,
                       reason=reason, **kw)


def _needs_lagna(key: str) -> YogaVerdict:
    return YogaVerdict(
        key=key, name=_SPEC[key]["name"], present=False,
        reason=("no lagna was supplied, and this yoga counts houses from "
                "lagna; it cannot be decided"))


# --------------------------------------------------------------------------
# The three associations
# --------------------------------------------------------------------------


def conjoined(data: YogaInput, a: int, b: int) -> bool:
    """Association (1): "The two planets are conjoined"."""
    sign_a, sign_b = data.sign_of(a), data.sign_of(b)
    return sign_a is not None and sign_a == sign_b


def mutual_drishti(data: YogaInput, a: int, b: int) -> bool:
    """Association (2): "aspect **each other** with graha drishti".

    Both ways. Graha drishti is not symmetric — Saturn's 3rd and 10th, Mars's
    4th and 8th, Jupiter's 5th and 9th are one-sided — so a single aspect is
    not an association.
    """
    sign_a, sign_b = data.sign_of(a), data.sign_of(b)
    if sign_a is None or sign_b is None:
        return False
    return (graha_aspects_sign(a, sign_a, sign_b)
            and graha_aspects_sign(b, sign_b, sign_a))


def parivartana(data: YogaInput, a: int, b: int) -> bool:
    """Association (3): each sits in a sign the other owns."""
    sign_a, sign_b = data.sign_of(a), data.sign_of(b)
    if sign_a is None or sign_b is None or a == b:
        return False
    return int(RASI_LORD[sign_a]) == b and int(RASI_LORD[sign_b]) == a


def association(data: YogaInput, a: int, b: int) -> str | None:
    """Which of the three, or None. Conjunction is checked first, as printed."""
    if a == b:
        return None
    if conjoined(data, a, b):
        return "conjunction"
    if mutual_drishti(data, a, b):
        return "mutual graha drishti"
    if parivartana(data, a, b):
        return "parivartana"
    return None


def kendra_lords(data: YogaInput) -> dict[int, tuple[int, ...]]:
    """Which quadrants each planet lords. Lagna is a quadrant."""
    return _lords_of(data, KENDRA)


def trikona_lords(data: YogaInput) -> dict[int, tuple[int, ...]]:
    """Which trines each planet lords. Lagna is a trine too."""
    return _lords_of(data, TRIKONA)


def _lords_of(data: YogaInput, houses: tuple[int, ...]) -> dict[int, tuple[int, ...]]:
    out: dict[int, list[int]] = {}
    for house in houses:
        out.setdefault(lord_of_house(data, house), []).append(house)
    return {graha: tuple(sorted(where)) for graha, where in out.items()}


def yogakaraka(data: YogaInput) -> dict[int, tuple[tuple[int, ...], tuple[int, ...]]]:
    """Planets lording a quadrant **and** a trine, neither of them the 1st.

    The lagna lord is excluded because the book has already accounted for
    him: "Lagna can be taken as a quadrant or a trine here. It is both." So
    every chart's lagna lord holds both sides trivially, and saying so on
    every chart would be noise. What is left is the genuine case — one planet
    lording a quadrant and a trine that are different houses.

    §11.7.1 does not discuss it: an association needs two planets, and such a
    planet cannot associate with himself. The fact is reported, not acted on.
    See docs/open-items.md OI-85.
    """
    kendras, trikonas = kendra_lords(data), trikona_lords(data)
    out = {}
    for graha in sorted(set(kendras) & set(trikonas)):
        quadrants = tuple(h for h in kendras[graha] if h != 1)
        trines = tuple(h for h in trikonas[graha] if h != 1)
        if quadrants and trines:
            out[graha] = (quadrants, trines)
    return out


# --------------------------------------------------------------------------
# The three yogas
# --------------------------------------------------------------------------


def _describe(data: YogaInput, a: int, b: int, kind: str,
              kendras: dict, trikonas: dict) -> str:
    where_a = ", ".join(ordinal(h) for h in kendras[a])
    where_b = ", ".join(ordinal(h) for h in trikonas[b])
    return (f"{GRAHA_NAMES[a]} (lord of the {where_a}) and {GRAHA_NAMES[b]} "
            f"(lord of the {where_b}) by {kind}")


def _detect_raaja_basic(data: YogaInput) -> YogaVerdict:
    key = "raaja_basic"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    kendras, trikonas = kendra_lords(data), trikona_lords(data)
    found = []
    pairs: set[tuple[int, int]] = set()
    for quadrant_lord in sorted(kendras):
        for trine_lord in sorted(trikonas):
            kind = association(data, quadrant_lord, trine_lord)
            if kind is None:
                continue
            pair = (min(quadrant_lord, trine_lord), max(quadrant_lord, trine_lord))
            if pair in pairs:
                continue
            pairs.add(pair)
            found.append(_describe(data, quadrant_lord, trine_lord, kind,
                                   kendras, trikonas))

    both = yogakaraka(data)
    extra = []
    for graha, (quadrants, trines) in both.items():
        extra.append(
            f"{GRAHA_NAMES[graha]} lords both a quadrant "
            f"({', '.join(ordinal(h) for h in quadrants)}) and a trine "
            f"({', '.join(ordinal(h) for h in trines)}); section 11.7.1 asks "
            f"for an association between two planets and does not say whether "
            f"one planet holding both sides is itself a Raaja Yoga. See "
            f"docs/open-items.md OI-85")

    if not found:
        return _verdict(
            key, False,
            "no quadrant lord is conjoined with, in mutual graha drishti "
            "with, or in parivartana with a trine lord",
            qualifiers=tuple(extra))
    participants = tuple(sorted({g for pair in pairs for g in pair}))
    return _verdict(key, True, "; ".join(found),
                    participants=participants, qualifiers=tuple(extra))


def _detect_dharma_karmadhipati(data: YogaInput) -> YogaVerdict:
    """"a special case of the above yoga" — the 9th and 10th lords."""
    key = "dharma_karmadhipati"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    ninth, tenth = lord_of_house(data, 9), lord_of_house(data, 10)
    if ninth == tenth:
        note = (f"{GRAHA_NAMES[ninth]} lords the most important trine and the "
                f"most important quadrant at once; section 11.7.1 does not "
                f"say what that alone amounts to. See docs/open-items.md "
                f"OI-85")
        return _verdict(
            key, False,
            f"the 9th and 10th are both lorded by {GRAHA_NAMES[ninth]}, so "
            f"there are not two planets to associate",
            qualifiers=(note,))
    kind = association(data, tenth, ninth)
    if kind is None:
        return _verdict(
            key, False,
            f"the 9th lord {GRAHA_NAMES[ninth]} and the 10th lord "
            f"{GRAHA_NAMES[tenth]} are neither conjoined, nor in mutual graha "
            f"drishti, nor in parivartana")
    return _verdict(key, True,
                    f"the 9th lord {GRAHA_NAMES[ninth]} and the 10th lord "
                    f"{GRAHA_NAMES[tenth]} are associated by {kind}",
                    participants=tuple(sorted({ninth, tenth})))


def _detect_vipareeta_raaja(data: YogaInput) -> YogaVerdict:
    """"If their lords occupies dusthanas or conjoin dusthanas".

    Both clauses are tested. The second is why the ideal case can name the
    3rd and the 11th, which are not dusthanas at all: three dusthana lords
    heaped together there conjoin no dusthana but do conjoin each other.
    See OI-86.
    """
    key = "vipareeta_raaja"
    if data.lagna_rasi is None:
        return _needs_lagna(key)
    lords = {house: lord_of_house(data, house) for house in DUSTHANA}
    inside = {house: lord for house, lord in lords.items()
              if houses_of(data, lord) in DUSTHANA}
    together = []
    ordered = sorted(set(lords.values()))
    for index, first in enumerate(ordered):
        for second in ordered[index + 1:]:
            if conjoined(data, first, second):
                together.append((first, second))

    ideal = _ideal_case(data, lords)
    qualifiers = (ideal,) if ideal else ()

    if not inside and not together:
        return _verdict(
            key, False,
            "no lord of the 6th, 8th or 12th occupies a dusthana, and no two "
            "of them are conjoined",
            qualifiers=qualifiers)

    parts = []
    if inside:
        parts.append(", ".join(
            f"the {ordinal(house)} lord {GRAHA_NAMES[lord]} is in the "
            f"{ordinal(houses_of(data, lord) or 0)}"
            for house, lord in sorted(inside.items())))
    if together:
        parts.append(", ".join(
            f"{GRAHA_NAMES[a]} and {GRAHA_NAMES[b]} are conjoined"
            for a, b in together))
    participants = tuple(sorted(
        set(inside.values()) | {g for pair in together for g in pair}))
    return _verdict(key, True, "; ".join(parts),
                    participants=participants, qualifiers=qualifiers)


def _ideal_case(data: YogaInput, lords: dict[int, int]) -> str | None:
    """"all together in one of the three houses (or the 3rd or the 11th),
    with no other planets conjoining them"."""
    distinct = sorted(set(lords.values()))
    signs = {data.sign_of(lord) for lord in distinct}
    if len(distinct) != 3 or len(signs) != 1 or None in signs:
        return None
    sign = signs.pop()
    if sign is None or data.lagna_rasi is None:
        return None
    house = (sign - data.lagna_rasi) % 12 + 1
    if house not in VIPAREETA_IDEAL_HOUSES:
        return (f"all three dusthana lords are together in {RASI_NAMES[sign]}, "
                f"but that is the {ordinal(house)}, which the ideal case does "
                f"not name")
    intruders = [GRAHA_NAMES[g] for g in occupants_of_house(data, house)
                 if g not in distinct]
    if intruders:
        return (f"all three dusthana lords are together in the "
                f"{ordinal(house)}, but {', '.join(intruders)} "
                f"{'joins' if len(intruders) == 1 else 'join'} them, so this "
                f"is not the ideal case")
    return (f"this is the ideal case: all three dusthana lords together in "
            f"the {ordinal(house)} ({RASI_NAMES[sign]}), with no other planet "
            f"conjoining them")


_DETECTORS = {
    "raaja_basic": _detect_raaja_basic,
    "dharma_karmadhipati": _detect_dharma_karmadhipati,
    "vipareeta_raaja": _detect_vipareeta_raaja,
}

for _key, _entry in _SPEC.items():
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=tuple(_entry.get("aliases", ())),
        section="11.7.1",
        group="raaja",
        definition=_entry["definition"],
        detect=_DETECTORS[_key],
        # "This is a special case of the above yoga."
        implies=("raaja_basic",) if _key == "dharma_karmadhipati" else (),
    ))
