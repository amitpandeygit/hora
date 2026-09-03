"""Section 14.2 — marakas.

Two kinds, and the book keeps them apart because they feed different dasas.
A **maraka sthana** is a rasi — the one holding the 2nd or 7th house — and
matters for rasi-ruled dasas. A **maraka graha** is a planet, and matters for
planet-ruled dasas.

Beyond the two house lords, §14.2 admits any malefic that "powerfully"
conjoins or aspects the 2nd or 7th house or their lords. It never says what
makes a contact powerful, so every contact is reported with what made it and
nothing is filtered on a threshold the section does not give.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.aspects import graha_aspects_sign, rasi_drishti
from hora.core import validate
from hora.core.const import (
    ADDITIONAL_MARAKA_TARGETS,
    CO_OWNED_EIGHTH_LORD_IS_UNSETTLED,
    DEBILITATION_RASI,
    EIGHTH_LORD_GROUPS,
    EXALTATION_RASI,
    GRAHA_NAMES,
    HOUSES_OF_LIFE,
    LONGEVITY_RANGES,
    MAHESWARA_NODE_SUBSTITUTES,
    MARAKA_DERIVATION,
    MARAKA_HOUSES,
    MODALITY_NAMES_EN,
    RASI_ABBR,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
    RUDRA_AFFLICTION_RULE,
    RUDRA_TABLE_32_SATURN_EXCEPTION,
    TABLE_32_EIGHTH,
    TABLE_33_LONGEVITY,
    TABLE_34_PARAMAAYUSH,
    Graha,
)

_RASI_INDEX = {abbr: index for index, abbr in enumerate(RASI_ABBR)}
_GRAHA_BY_NAME = {str(GRAHA_NAMES[int(g)]): int(g) for g in Graha}

#: §14.2's own list, less the two whose nature is conditional. The Moon's
#: depends on his phase and Mercury's on his association, and neither worked
#: example uses either — see OI-105.
MALEFICS: frozenset[int] = frozenset({
    int(Graha.SUN), int(Graha.MARS), int(Graha.SATURN),
    int(Graha.RAHU), int(Graha.KETU),
})

def _ordinal(n: int) -> str:
    """2 -> "2nd", 7 -> "7th". The book writes them out, so we do too."""
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }"


#: Scorpio and Aquarius have two lords each, so a maraka house falling in one
#: yields two maraka grahas rather than one. §14.2 names only Saturn for
#: Aquarius in its first example and does not discuss co-lordship, so the
#: co-lord is included and labelled rather than assumed away. See OI-108.
CO_LORDS: dict[int, tuple[int, int]] = {
    7: (int(Graha.MARS), int(Graha.KETU)),
    10: (int(Graha.SATURN), int(Graha.RAHU)),
}


class MarakaError(validate.InputError):
    """Raised when a maraka question cannot be answered."""


@dataclass(frozen=True)
class Maraka:
    """One maraka graha, and how it qualified."""

    graha: int
    graha_name: str
    #: "house lord" or "malefic contact".
    kind: str
    #: Every reason it qualified. A planet can qualify more than one way.
    reasons: tuple[str, ...]


def houses_of_life() -> dict[int, str]:
    """§14.2: the 3rd and the 8th, and what each shows."""
    return dict(HOUSES_OF_LIFE)


def maraka_houses() -> tuple[int, ...]:
    """The 2nd and 7th, derived as the 12th from each house of life."""
    derived = tuple(sorted(
        ((life + 12 - 2) % 12) + 1 for life in HOUSES_OF_LIFE))
    if derived != tuple(sorted(MARAKA_HOUSES)):  # pragma: no cover
        raise MarakaError(
            f"the 12th from {sorted(HOUSES_OF_LIFE)} is {derived}, not "
            f"{sorted(MARAKA_HOUSES)}")
    return derived


def maraka_sthanas(lagna: int) -> dict[int, int]:
    """The rasis holding the 2nd and 7th houses. House number -> rasi."""
    index = validate.in_range("lagna", lagna, 0, 11)
    return {house: (index + house - 1) % 12 for house in maraka_houses()}


def _lords_of(sign: int) -> tuple[int, ...]:
    return CO_LORDS.get(sign, (int(RASI_LORD[sign]),))


def maraka_grahas(lagna: int) -> dict[int, tuple[int, ...]]:
    """The lords of the 2nd and 7th. House number -> its lord or co-lords."""
    return {house: _lords_of(sign)
            for house, sign in maraka_sthanas(lagna).items()}


def additional_marakas(lagna: int, graha_signs: dict[int, int],
                       malefic: frozenset[int] | None = None
                       ) -> dict[int, tuple[str, ...]]:
    """Malefics reaching a maraka house or its lord, and how.

    §14.2's second kind. Contacts are conjunction and graha drishti only —
    the section says "using graha drishti" outright, so rasi drishti does not
    qualify a maraka here.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    for graha, place in graha_signs.items():
        validate.in_range(f"graha {graha} sign", int(place), 0, 11)
    positions = {int(g): int(s) for g, s in graha_signs.items()}
    evil = MALEFICS if malefic is None else malefic

    sthanas = maraka_sthanas(index)
    lords = maraka_grahas(index)
    targets: list[tuple[str, int, int | None]] = []
    for house, sign in sthanas.items():
        targets.append(
            (f"the {_ordinal(house)} house ({RASI_NAMES[sign]})", sign, None))
        for lord in lords[house]:
            if lord in positions:
                targets.append(
                    (f"the {_ordinal(house)} lord {GRAHA_NAMES[lord]}",
                     positions[lord], lord))

    found: dict[int, list[str]] = {}
    for graha, place in sorted(positions.items()):
        if graha not in evil:
            continue
        for label, target, owner in targets:
            if owner == graha:
                continue  # a planet does not reach itself
            if place == target:
                found.setdefault(graha, []).append(f"conjoins {label}")
            elif graha_aspects_sign(graha, place, target):
                found.setdefault(graha, []).append(f"aspects {label}")
    return {graha: tuple(reasons) for graha, reasons in found.items()}


def marakas(lagna: int, graha_signs: dict[int, int] | None = None) -> dict:
    """Every maraka §14.2 admits, with how each qualified.

    :param graha_signs: needed for the second kind. Without it only the house
        lords are returned, and the answer says so rather than implying the
        list is complete.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    sthanas = maraka_sthanas(index)
    lords = maraka_grahas(index)

    found: dict[int, Maraka] = {}
    for house, owners in lords.items():
        for lord in owners:
            reason = (f"owns the {_ordinal(house)} house "
                      f"({RASI_NAMES[sthanas[house]]})")
            if len(owners) > 1:
                reason += " as co-lord"
            if lord in found:
                found[lord] = Maraka(
                    lord, found[lord].graha_name, found[lord].kind,
                    found[lord].reasons + (reason,))
            else:
                found[lord] = Maraka(
                    lord, str(GRAHA_NAMES[lord]), "house lord", (reason,))

    complete = graha_signs is not None
    if complete:
        assert graha_signs is not None
        for graha, reasons in additional_marakas(index, graha_signs).items():
            if graha in found:
                found[graha] = Maraka(
                    graha, found[graha].graha_name, found[graha].kind,
                    found[graha].reasons + reasons)
            else:
                found[graha] = Maraka(
                    graha, str(GRAHA_NAMES[graha]), "malefic contact", reasons)

    return {
        "lagna": index,
        "lagna_name": str(RASI_NAMES[index]),
        "houses_of_life": {
            house: {"shows": shows,
                    "rasi": str(RASI_NAMES[(index + house - 1) % 12])}
            for house, shows in HOUSES_OF_LIFE.items()
        },
        "derivation": [
            {"house_of_life": life, "twelfth_from_it": death}
            for life, death in MARAKA_DERIVATION
        ],
        "maraka_sthanas": [
            {"house": house, "rasi": sign,
             "rasi_name": str(RASI_NAMES[sign])}
            for house, sign in sorted(sthanas.items())
        ],
        "maraka_grahas": [
            {"graha": m.graha, "graha_name": m.graha_name, "kind": m.kind,
             "reasons": list(m.reasons)}
            for m in sorted(found.values(), key=lambda m: m.graha)
        ],
        "malefic_contacts_included": complete,
        "targets": list(ADDITIONAL_MARAKA_TARGETS),
        "incomplete_note": (
            None if complete else
            "Only the lords of the 2nd and 7th are listed. Section 14.2 also "
            "admits any malefic that conjoins or aspects those houses or "
            "their lords, which needs the chart's graha positions."
        ),
    }


# --------------------------------------------------------------------------
# §14.3 — Rudra, Trishoola and Maheswara
# --------------------------------------------------------------------------

def rudra_eighth(sign: int) -> int:
    """Table 32's 8th house from `sign` — not the ordinary 8th.

    §14.3 is explicit: "Find the 8th house using Table 32 and not in the
    normal way." The two differ for eight of the twelve rasis.
    """
    index = validate.in_range("sign", sign, 0, 11)
    return _RASI_INDEX[TABLE_32_EIGHTH[RASI_ABBR[index]]]


def ordinary_eighth(sign: int) -> int:
    """The 8th counted the usual way — what Maheswara uses."""
    return (validate.in_range("sign", sign, 0, 11) + 7) % 12


@dataclass(frozen=True)
class Rudra:
    """The two candidates for Rudra, and which the strength cascade picks."""

    #: The 8th from lagna by Table 32, and its lord.
    from_lagna: tuple[int, int]
    #: The 8th from the 7th house by Table 32, and its lord.
    from_seventh: tuple[int, int]
    #: Both candidate lords, deduplicated.
    candidates: tuple[int, ...]
    #: The stronger, when positions allowed the cascade to decide.
    rudra: int | None
    #: Which cascade step decided it, 1 to 5.
    decided_by: int | None
    why: str


def rudra_candidates(lagna: int) -> Rudra:
    """§14.3's two candidates, before any strength test.

    The cascade needs positions; `rudra` is None here and `why` says so.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    seventh = (index + 6) % 12
    first, second = rudra_eighth(index), rudra_eighth(seventh)
    lords = (_lords_of(first), _lords_of(second))
    candidates = tuple(dict.fromkeys(lords[0] + lords[1]))
    return Rudra(
        from_lagna=(first, int(RASI_LORD[first])),
        from_seventh=(second, int(RASI_LORD[second])),
        candidates=candidates,
        rudra=None,
        decided_by=None,
        why=(
            f"Table 32 puts the 8th from {RASI_NAMES[index]} in "
            f"{RASI_NAMES[first]} and the 8th from the 7th house "
            f"({RASI_NAMES[seventh]}) in {RASI_NAMES[second]}; their lords "
            f"are {', '.join(GRAHA_NAMES[g] for g in candidates)}. Section "
            f"14.3's strength cascade needs the chart's positions, so which "
            f"of them is Rudra is not decided here"
        ),
    )


def trishoola_rasis(rudra_sign: int) -> tuple[int, ...]:
    """The three trines from the rasi Rudra occupies, ascending from it."""
    index = validate.in_range("rudra_sign", rudra_sign, 0, 11)
    return tuple((index + step) % 12 for step in (0, 4, 8))


def maheswara(ak_sign: int, graha_signs: dict[int, int] | None = None
              ) -> dict:
    """§14.3's Maheswara — the lord of the 8th from AK, with its exceptions.

    :param ak_sign: the rasi the atma karaka occupies.
    :param graha_signs: needed for exceptions 1 and 2, which turn on where
        the node and the 8th lord sit. Without them only the base rule runs
        and the answer says which exceptions could not be tested.
    """
    index = validate.in_range("ak_sign", ak_sign, 0, 11)
    eighth = ordinary_eighth(index)
    base = int(RASI_LORD[eighth])
    steps = [(
        f"the 8th from the AK's {RASI_NAMES[index]} is {RASI_NAMES[eighth]}, "
        f"whose lord {GRAHA_NAMES[base]} is Maheswara"
    )]
    untested: list[str] = []
    result = base
    house_used = 8

    if graha_signs is None:
        untested += [
            "exception 1 needs the 8th lord's position",
            "exception 2 needs the nodes' positions",
        ]
    else:
        positions = {int(g): int(s) for g, s in graha_signs.items()}
        for graha, place in positions.items():
            validate.in_range(f"graha {graha} sign", place, 0, 11)

        # Exception 2 first: it changes which house is read at all.
        node_on_ak = any(
            positions.get(int(node)) in (index, eighth)
            for node in (Graha.RAHU, Graha.KETU) if int(node) in positions)
        if node_on_ak:
            house_used = 6
            sixth = (index + 5) % 12
            result = int(RASI_LORD[sixth])
            steps.append(
                f"exception 2: a node joins the AK or the 8th from him, so "
                f"the 6th from {RASI_NAMES[index]} — {RASI_NAMES[sixth]} — is "
                f"read instead, and its lord {GRAHA_NAMES[result]} is "
                f"Maheswara. That is the 8th counted anti-zodiacally"
            )
        elif result in positions:
            seat = positions[result]
            own = int(RASI_LORD[seat]) == result
            exalted = EXALTATION_RASI.get(result) == seat
            if own or exalted:
                pair = (ordinary_eighth(seat), (seat + 11) % 12)
                lords = tuple(int(RASI_LORD[s]) for s in pair)
                steps.append(
                    f"exception 1: {GRAHA_NAMES[result]} is in "
                    f"{'his own rasi' if own else 'exaltation'} "
                    f"({RASI_NAMES[seat]}), so the stronger of the 8th and "
                    f"12th lords from him — {GRAHA_NAMES[lords[0]]} of "
                    f"{RASI_NAMES[pair[0]]} and {GRAHA_NAMES[lords[1]]} of "
                    f"{RASI_NAMES[pair[1]]} — becomes Maheswara"
                )
                return {
                    "ak_sign": index, "ak_rasi": str(RASI_NAMES[index]),
                    "house_used": house_used,
                    "maheswara": None,
                    "maheswara_name": None,
                    "candidates": [
                        {"graha": g, "graha_name": str(GRAHA_NAMES[g]),
                         "house": h, "rasi": str(RASI_NAMES[s])}
                        for g, h, s in zip(lords, (8, 12), pair, strict=True)
                    ],
                    "steps": steps,
                    "untested_exceptions": untested,
                    "needs_strength_comparison": True,
                }
        else:
            untested.append(
                f"exception 1 needs {GRAHA_NAMES[result]}'s position")

    substitute = MAHESWARA_NODE_SUBSTITUTES.get(str(GRAHA_NAMES[result]))
    if substitute is not None:
        steps.append(
            f"exception 3: {GRAHA_NAMES[result]} became Maheswara, so "
            f"{substitute} is taken instead")
        result = _GRAHA_BY_NAME[substitute]

    return {
        "ak_sign": index,
        "ak_rasi": str(RASI_NAMES[index]),
        "house_used": house_used,
        "maheswara": result,
        "maheswara_name": str(GRAHA_NAMES[result]),
        "candidates": [],
        "steps": steps,
        "untested_exceptions": untested,
        "needs_strength_comparison": False,
    }


# --------------------------------------------------------------------------
# §14.4 — The Method of Three Pairs
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Pair:
    """One of §14.4's three pairs, and the category it yields."""

    name: str
    #: What the two members are, named.
    members: tuple[str, str]
    #: The rasi each occupies.
    signs: tuple[int, int]
    #: Their modalities.
    modalities: tuple[str, str]
    #: "short", "middle" or "long", from Table 33.
    category: str
    why: str


def _modality(sign: int) -> str:
    return MODALITY_NAMES_EN[RASI_MODALITY[validate.in_range(
        "sign", sign, 0, 11)]]


def pair_category(first: int, second: int) -> str:
    """Table 33's category for two rasis. Exhaustive — all six pairs appear."""
    key = frozenset({_modality(first), _modality(second)})
    if key not in TABLE_33_LONGEVITY:  # pragma: no cover - unreachable
        raise MarakaError(f"Table 33 has no entry for {sorted(key)}")
    return TABLE_33_LONGEVITY[key]


def _pair(name: str, members: tuple[str, str], signs: tuple[int, int]) -> Pair:
    modalities = (_modality(signs[0]), _modality(signs[1]))
    category = pair_category(*signs)
    return Pair(
        name=name, members=members, signs=signs, modalities=modalities,
        category=category,
        why=(
            f"{members[0]} is in {RASI_NAMES[signs[0]]} ({modalities[0]}) and "
            f"{members[1]} in {RASI_NAMES[signs[1]]} ({modalities[1]}); "
            f"Table 33 gives {category} life"
        ),
    )


def three_pairs(lagna: int, graha_signs: dict[int, int], hl_sign: int,
                overrides: dict[int, int] | None = None) -> dict:
    """§14.4's method, end to end.

    :param lagna: the lagna's rasi.
    :param graha_signs: graha id -> rasi. The lagna lord, the 8th lord by
        Table 32, the Moon and Saturn must all be present.
    :param hl_sign: Horalagna's rasi.
    :param overrides: rasi -> the lord to use for it, for a co-owned 8th
        house. Without one the first co-lord is taken and the answer says so;
        Example 87 shows the choice can flip the whole category. See OI-135.
    """
    index = validate.in_range("lagna", lagna, 0, 11)
    validate.in_range("hl_sign", hl_sign, 0, 11)
    positions = {int(g): int(s) for g, s in graha_signs.items()}
    for graha, place in positions.items():
        validate.in_range(f"graha {graha} sign", place, 0, 11)

    lagna_lord = int(RASI_LORD[index])
    eighth_sign = rudra_eighth(index)
    eighth_lords = _lords_of(eighth_sign)
    eighth_lord = _chosen_lord(eighth_sign, eighth_lords, overrides)

    needed = {
        "the lagna lord": lagna_lord,
        "the 8th lord": eighth_lord,
        "the Moon": int(Graha.MOON),
        "Saturn": int(Graha.SATURN),
    }
    missing = [name for name, g in needed.items() if g not in positions]
    if missing:
        raise MarakaError(
            f"the method of three pairs needs {', '.join(missing)}; supply "
            f"their rasis in graha_signs")

    pairs = (
        _pair("lagna lord and 8th lord",
              (str(GRAHA_NAMES[lagna_lord]), str(GRAHA_NAMES[eighth_lord])),
              (positions[lagna_lord], positions[eighth_lord])),
        _pair("Moon and Saturn", ("Moon", "Saturn"),
              (positions[int(Graha.MOON)], positions[int(Graha.SATURN)])),
        _pair("lagna and Horalagna", ("lagna", "HL"), (index, hl_sign)),
    )

    categories = [p.category for p in pairs]
    counts = {c: categories.count(c) for c in set(categories)}
    paramaayush: int | None = None
    paramaayush_note: str | None = None

    if len(counts) == 1:
        category = categories[0]
        reason = "all three pairs agree"
        paramaayush_note = (
            "Section 14.4 gives Table 34 for the case where two pairs agree "
            "and one differs. With all three agreeing there is no odd pair, "
            "so no paramaayush is stated.")
    elif len(counts) == 2:
        category = max(counts, key=lambda c: counts[c])
        odd = next(c for c in counts if counts[c] == 1)
        paramaayush = TABLE_34_PARAMAAYUSH[odd][category]
        reason = (
            f"two pairs give {category} life and one gives {odd}; the two "
            f"dominate, and Table 34 puts the paramaayush at "
            f"{paramaayush} years")
    else:
        moon = positions[int(Graha.MOON)]
        moon_on_axis = moon in (index, (index + 6) % 12)
        preferred = pairs[1] if moon_on_axis else pairs[2]
        category = preferred.category
        reason = (
            f"all three pairs differ, so section 14.4 prefers "
            f"{'the Moon and Saturn, because the Moon is in ' + ('lagna' if moon == index else 'the 7th house') if moon_on_axis else 'lagna and Horalagna'}"
        )
        paramaayush_note = (
            "Table 34 needs a majority and an odd pair. With three different "
            "results section 14.4 names a preferred pair and stops at a "
            "category, so no paramaayush is stated.")

    low, high = LONGEVITY_RANGES[category]
    return {
        "lagna": index,
        "lagna_rasi": str(RASI_NAMES[index]),
        "eighth_house": {
            "rasi": str(RASI_NAMES[eighth_sign]),
            "by": "Table 32",
            "lords": [str(GRAHA_NAMES[g]) for g in eighth_lords],
            "lord_used": str(GRAHA_NAMES[eighth_lord]),
            "lord_was_chosen": len(eighth_lords) > 1,
            "co_lord_note": (
                CO_OWNED_EIGHTH_LORD_IS_UNSETTLED
                if len(eighth_lords) > 1 else None),
        },
        "pairs": [
            {"name": p.name, "members": list(p.members),
             "rasis": [str(RASI_NAMES[s]) for s in p.signs],
             "modalities": list(p.modalities), "category": p.category,
             "why": p.why}
            for p in pairs
        ],
        "category": category,
        "range_years": [low, high],
        "reason": reason,
        "paramaayush_years": paramaayush,
        "paramaayush_note": paramaayush_note,
    }


# --------------------------------------------------------------------------
# §14.5 — The Eighth Lord Method
# --------------------------------------------------------------------------

def house_group(house: int) -> tuple[str, str]:
    """Which of §14.5's three groups a house falls in, and its category."""
    number = validate.in_range("house", house, 1, 12)
    for name, houses, category in EIGHTH_LORD_GROUPS:
        if number in houses:
            return name, category
    raise MarakaError(  # pragma: no cover - the three groups tile 1..12
        f"house {number} is in none of section 14.5's three groups")


def eighth_lord_method(reference: int, graha_signs: dict[int, int]) -> dict:
    """§14.5's method, from a reference the caller has chosen.

    :param reference: the rasi of whichever of lagna and the 7th house the
        caller judges stronger. §14.5 gives no way to compare them and both
        its worked cases state the winner as a premise, so this is not
        decided here.
    """
    index = validate.in_range("reference", reference, 0, 11)
    positions = {int(g): int(s) for g, s in graha_signs.items()}
    for graha, place in positions.items():
        validate.in_range(f"graha {graha} sign", place, 0, 11)

    eighth = ordinary_eighth(index)
    lords = _lords_of(eighth)
    lord = lords[0]
    if lord not in positions:
        raise MarakaError(
            f"{GRAHA_NAMES[lord]} owns the 8th from {RASI_NAMES[index]} "
            f"({RASI_NAMES[eighth]}), and the method reads where he sits, so "
            f"his rasi is needed")

    seat = positions[lord]
    house = ((seat - index) % 12) + 1
    group, category = house_group(house)
    low, high = LONGEVITY_RANGES[category]
    return {
        "reference": index,
        "reference_rasi": str(RASI_NAMES[index]),
        "eighth_house": {
            "rasi": str(RASI_NAMES[eighth]),
            "by": "the ordinary count",
            "lords": [str(GRAHA_NAMES[g]) for g in lords],
            "lord_used": str(GRAHA_NAMES[lord]),
        },
        "lord_sign": seat,
        "lord_rasi": str(RASI_NAMES[seat]),
        "house_from_reference": house,
        "group": group,
        "category": category,
        "range_years": [low, high],
        "why": (
            f"{GRAHA_NAMES[lord]} owns the 8th from {RASI_NAMES[index]}, "
            f"which is {RASI_NAMES[eighth]}; he sits in {RASI_NAMES[seat]}, "
            f"the {_ordinal(house)} from {RASI_NAMES[index]}, "
            f"{'an' if group[0] in 'aeiou' else 'a'} {group} — so {category} "
            f"life"
        ),
    }


# --------------------------------------------------------------------------
# §14.3's Rudra strength cascade, which Exercise 23 shows can be run
# --------------------------------------------------------------------------

def _cascade_step(first: int, second: int, positions: dict[int, int],
                  longitudes: dict[int, float] | None) -> tuple[int | None, int, str]:
    """§14.3's five tests in order. Returns (winner, step, detail)."""
    seats = (positions[first], positions[second])

    company = tuple(
        sum(1 for g, s in positions.items() if s == seat and g != who)
        for who, seat in zip((first, second), seats, strict=True))
    if company[0] != company[1]:
        winner = first if company[0] > company[1] else second
        return winner, 1, (
            f"{GRAHA_NAMES[first]} conjoins {company[0]} planets, "
            f"{GRAHA_NAMES[second]} conjoins {company[1]}")

    dignified = tuple(
        EXALTATION_RASI.get(who) == seat or int(RASI_LORD[seat]) == who
        for who, seat in zip((first, second), seats, strict=True))
    if dignified[0] != dignified[1]:
        winner = first if dignified[0] else second
        return winner, 2, (
            f"{GRAHA_NAMES[winner]} is in exaltation or his own rasi and the "
            f"other is not")

    with_exalted = tuple(
        any(EXALTATION_RASI.get(g) == s for g, s in positions.items()
            if s == seat and g != who)
        for who, seat in zip((first, second), seats, strict=True))
    if with_exalted[0] != with_exalted[1]:
        winner = first if with_exalted[0] else second
        return winner, 3, (
            f"{GRAHA_NAMES[winner]} joins an exalted planet and the other "
            f"does not")

    aspected = tuple(
        sum(1 for g, s in positions.items()
            if g != who and seat in rasi_drishti(s))
        for who, seat in zip((first, second), seats, strict=True))
    if aspected[0] != aspected[1]:
        winner = first if aspected[0] > aspected[1] else second
        return winner, 4, (
            f"{GRAHA_NAMES[first]} is rasi-aspected by {aspected[0]} planets, "
            f"{GRAHA_NAMES[second]} by {aspected[1]}")

    if longitudes is None:
        return None, 5, (
            "the first four tests tie, and the fifth — which planet is more "
            "advanced in its rasi — needs longitudes, which were not given")
    advance = tuple(longitudes[who] % 30 for who in (first, second))
    if advance[0] == advance[1]:  # pragma: no cover - a genuine dead heat
        return None, 5, "both planets are equally advanced in their rasis"
    winner = first if advance[0] > advance[1] else second
    return winner, 5, (
        f"{GRAHA_NAMES[first]} is at {advance[0]:.2f} degrees of his rasi and "
        f"{GRAHA_NAMES[second]} at {advance[1]:.2f}, so "
        f"{GRAHA_NAMES[winner]} is more advanced")


def _chosen_lord(sign: int, lords: tuple[int, ...],
                 overrides: dict[int, int] | None) -> int:
    """The lord to use for a rasi, honouring a caller's choice for a co-owned
    one. Without a choice the first co-lord is taken, as before."""
    if overrides and sign in overrides:
        chosen = int(overrides[sign])
        if chosen not in lords:
            raise MarakaError(
                f"{GRAHA_NAMES[chosen]} does not own {RASI_NAMES[sign]}; its "
                f"lords are {', '.join(str(GRAHA_NAMES[g]) for g in lords)}")
        return chosen
    return lords[0]


def rudra(lagna: int, graha_signs: dict[int, int],
          graha_longitudes: dict[int, float] | None = None,
          overrides: dict[int, int] | None = None) -> dict:
    """§14.3's Rudra, run through the strength cascade.

    The affliction override — the weaker planet taking over if it is
    debilitated or in an inimical sign *and* afflicted by "malefics like Mars,
    Saturn, Rahu and Ketu" — is not applied, because "like" leaves that list
    open. Whether the weaker candidate is debilitated is reported so a caller
    can apply it. See docs/open-items.md OI-109.

    :param overrides: rasi -> the lord to use, for a co-owned 8th house.
        Examples 85 and 87 both name Ketu for Scorpio; without an override the
        first co-lord is taken. See OI-135.
    """
    base = rudra_candidates(lagna)
    positions = {int(g): int(s) for g, s in graha_signs.items()}
    for graha, place in positions.items():
        validate.in_range(f"graha {graha} sign", place, 0, 11)

    first = _chosen_lord(base.from_lagna[0], _lords_of(base.from_lagna[0]),
                         overrides)
    second = _chosen_lord(base.from_seventh[0],
                          _lords_of(base.from_seventh[0]), overrides)
    if first == second:
        return {
            "candidates": [str(GRAHA_NAMES[first])],
            "rudra": str(GRAHA_NAMES[first]),
            "decided_by": None,
            "why": (
                f"both 8th houses have the same lord, {GRAHA_NAMES[first]}, "
                f"so no comparison is needed"),
            "trishoola": [],
            "weaker_is_debilitated": None,
        }
    missing = [g for g in (first, second) if g not in positions]
    if missing:
        raise MarakaError(
            f"the cascade needs the rasi of "
            f"{', '.join(GRAHA_NAMES[g] for g in missing)}")

    winner, step, detail = _cascade_step(
        first, second, positions, graha_longitudes)
    loser = None if winner is None else (
        second if winner == first else first)
    debilitated = (
        None if loser is None
        else DEBILITATION_RASI.get(loser) == positions[loser])
    return {
        "candidates": [str(GRAHA_NAMES[first]), str(GRAHA_NAMES[second])],
        "from_lagna": {
            "rasi": str(RASI_NAMES[base.from_lagna[0]]),
            "lord": str(GRAHA_NAMES[first])},
        "from_seventh": {
            "rasi": str(RASI_NAMES[base.from_seventh[0]]),
            "lord": str(GRAHA_NAMES[second])},
        "rudra": None if winner is None else str(GRAHA_NAMES[winner]),
        "rudra_sign": None if winner is None else positions[winner],
        "rudra_rasi": (None if winner is None
                       else str(RASI_NAMES[positions[winner]])),
        "decided_by": step,
        "why": detail,
        "trishoola": (
            [] if winner is None else
            [{"sign": s, "rasi": str(RASI_NAMES[s])}
             for s in trishoola_rasis(positions[winner])]),
        "weaker_is_debilitated": debilitated,
        "affliction_override": RUDRA_AFFLICTION_RULE,
        "table_32_exception": RUDRA_TABLE_32_SATURN_EXCEPTION,
    }
