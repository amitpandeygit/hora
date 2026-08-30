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

from hora.charts.aspects import graha_aspects_sign
from hora.core import validate
from hora.core.const import (
    ADDITIONAL_MARAKA_TARGETS,
    EXALTATION_RASI,
    GRAHA_NAMES,
    HOUSES_OF_LIFE,
    MAHESWARA_NODE_SUBSTITUTES,
    MARAKA_DERIVATION,
    MARAKA_HOUSES,
    RASI_ABBR,
    RASI_LORD,
    RASI_NAMES,
    TABLE_32_EIGHTH,
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
