"""Stronger rasi — book §15.5.2.

    "When computing rasi dasas, we sometimes need to find the strongest rasi
    out of 2 or 3 or 4 rasis... We go from one rule to the next only if there
    is no winner after the rule. When we have a winner, we stop and do not go
    to the next rule."

Same cascade discipline as §15.5.1: stop at the first rule that decides, and a
rule that **cannot** be evaluated stops it too rather than being skipped.

    1  more planets in it -> stronger
    2  more of {Jupiter, Mercury, the rasi's lord} occupy or aspect it
    3  contains an exalted planet, the other does not
    4  its lord sits in a rasi of *different* oddity
    5  dual beats fixed beats movable
    6  its lord is more advanced in its own rasi

Also used for "finding the stronger rasi owned by a planet, when computing its
graha arudha". §15.5.2's own note says rule 4 always settles that case, because
the two rasis a planet owns have different oddity.

**The section carries a warning**, and it is not decoration: "The above rules
are too general. One should understand the meaning of each rule and adapt based
on the situation." Rule 2's three planets are right for Narayana and other
phalita dasas and wrong for others. ``purpose`` selects the adaptation; see
:data:`PURPOSE_ADAPTATIONS`.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.aspects import rasi_drishti
from hora.charts.colord import CO_LORDS
from hora.charts.colord import stronger as stronger_co_lord
from hora.core import validate
from hora.core.const import (
    EXALTATION_RASI,
    GRAHA_NAMES,
    KENDRA,
    PANAPHARA,
    RASI_IS_ODD,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
    Graha,
)


class RasiStrengthError(validate.InputError):
    """A rasi comparison that cannot be made."""


#: Rule 5: "Dual rasis are stronger than fixed rasis and fixed rasis are
#: stronger than movable rasis."
MODALITY_RANK = {0: 1, 1: 2, 2: 3}

#: The section's warning, as data. Only ``phalita`` and ``ak_based`` are
#: implemented; ``ayur`` is recorded because the book names it, not because it
#: is derivable from what the book says here.
PURPOSE_ADAPTATIONS: dict[str, dict] = {
    "phalita": {
        "name": "Phalita dasas",
        "applies_to": "Narayana dasa and other phalita dasas",
        "rule_2_planets": "Jupiter, Mercury and the rasi's lord",
        "implemented": True,
        "note": None,
    },
    "ak_based": {
        "name": "Dasas based on the Atma Karaka",
        "applies_to": "Atmakaraka kendradi graha and rasi dasas",
        "rule_2_planets": "Jupiter, Mercury and the rasi's lord",
        "implemented": True,
        "note": (
            "The sign containing AK is stronger than any other rasi. After the "
            "Mercury/Jupiter/lord check, a rasi whose lord is in a quadrant "
            "from AK beats one whose lord is in a panaphara from AK."
        ),
    },
    "ayur": {
        "name": "Ayur dasas",
        "applies_to": "dasas that show longevity",
        "rule_2_planets": (
            "the luminaries; aspect of all other planets is equally important; "
            "there is no significance for the aspect of lord"
        ),
        "implemented": False,
        "note": (
            "\"Aspect of all other planets is equally important\" does not say "
            "how to weigh them against the luminaries, so rule 2 cannot be "
            "computed for this purpose from the text alone."
        ),
    },
}

PURPOSES = tuple(PURPOSE_ADAPTATIONS)

#: Rule 6: "from the end of the rasi in the case of Rahu and Ketu".
MEASURED_FROM_END = frozenset({Graha.RAHU, Graha.KETU})


@dataclass(frozen=True)
class RuleVerdict:
    rule: str
    description: str
    winner: int | None
    winner_name: str | None
    decided: bool | None
    detail: str


@dataclass(frozen=True)
class RasiVerdict:
    first: int
    first_name: str
    second: int
    second_name: str
    purpose: str
    winner: int | None
    winner_name: str | None
    decided_by: str | None
    determined: bool
    reason: str
    rules: tuple[RuleVerdict, ...]


def _sign(longitude: float) -> int:
    return int(validate.longitude("longitude", longitude) // 30.0)


def advancement(longitude: float, graha: int) -> float:
    """Rule 6's advancement: from the rasi's start, or its end for the nodes.

    "If Rahu is at 9Sc34, his advancement in Sc is 30° - 9°34' = 20°26'."
    """
    within = validate.longitude("longitude", longitude) % 30.0
    return 30.0 - within if graha in MEASURED_FROM_END else within


def lord_of(
    rasi: int,
    longitudes: dict[int, float],
    dasa_years: dict[int, float] | None = None,
) -> tuple[int | None, str]:
    """The rasi's lord, resolving Scorpio and Aquarius through §15.5.1.

    Rule 6's note says so outright — "In the case of Aq and Sc, we use the
    stronger lord" — and §15.5.1 says the stronger co-lord "acts as its lord".

    **Rule 2 is the exception and does not use this.** Exercise 26 counts a
    co-lord's aspect even though it is not the stronger one: "Aq is aspected
    by co-lord Rahu (though Saturn is the primary/stronger lord, Rahu's
    aspect also counts)". So rule 2 takes `co_lords_of` instead. Rules 4 and
    5 keep this resolution, which rule 6's note attests and nothing
    contradicts — see docs/open-items.md OI-111.

    :returns: ``(lord, explanation)``. The lord is None when §15.5.1's own
        cascade could not decide, which stops this cascade too.
    """
    if rasi not in CO_LORDS:
        lord = int(RASI_LORD[rasi])
        return lord, f"lord of {RASI_NAMES[rasi]} is {GRAHA_NAMES[lord]}"
    verdict = stronger_co_lord(
        rasi, longitudes, purpose="dasa" if dasa_years else "arudha",
        dasa_years=dasa_years,
    )
    if verdict.winner is None:
        return None, (
            f"{RASI_NAMES[rasi]} is co-owned and section 15.5.1 could not "
            f"decide its lord: {verdict.reason}"
        )
    return verdict.winner, (
        f"lord of {RASI_NAMES[rasi]} is {verdict.winner_name}, the stronger "
        f"co-lord by section 15.5.1 rule {verdict.decided_by}"
    )


def occupants(rasi: int, longitudes: dict[int, float]) -> set[int]:
    """Grahas in a rasi."""
    return {g for g, lon in longitudes.items() if _sign(lon) == rasi}


def co_lords_of(rasi: int) -> tuple[int, ...]:
    """Every lord of a rasi — two for Scorpio and Aquarius, one otherwise.

    Rule 2 counts all of them. Exercise 26 says so: a co-lord's aspect
    counts even when it is not the stronger lord.
    """
    return CO_LORDS.get(rasi, (int(RASI_LORD[rasi]),))


def rule_2_count(
    rasi: int,
    lords: tuple[int, ...] | int,
    longitudes: dict[int, float],
) -> tuple[int, list[str]]:
    """How many of Jupiter, Mercury and the rasi's lord(s) occupy or aspect it.

    Counted by **role**, matching §15.5.1's sibling rule: a lord that is also
    Jupiter or Mercury contributes twice. A co-owned rasi has two lords and
    each is counted, per Exercise 26.
    """
    owners = (int(lords),) if isinstance(lords, int) else tuple(
        int(g) for g in lords)
    count, why = 0, []
    roles: list[tuple[str, int]] = [
        ("Jupiter", int(Graha.JUPITER)), ("Mercury", int(Graha.MERCURY))]
    roles += [
        ("lord" if len(owners) == 1 else "co-lord", g) for g in owners]
    for role, graha in roles:
        if graha not in longitudes:
            continue
        where = _sign(longitudes[graha])
        if where == rasi:
            count += 1
            why.append(f"{role} ({GRAHA_NAMES[graha]}) occupies it")
        elif rasi in rasi_drishti(where):
            count += 1
            why.append(f"{role} ({GRAHA_NAMES[graha]}) aspects from {RASI_NAMES[where]}")
    return count, why


def stronger(
    first: int,
    second: int,
    longitudes: dict[int, float],
    purpose: str = "phalita",
    dasa_years: dict[int, float] | None = None,
    atma_karaka_rasi: int | None = None,
) -> RasiVerdict:
    """Which of two rasis is stronger, by §15.5.2's cascade.

    :param purpose: which adaptation of the warning applies. ``"phalita"``
        (Narayana and other phalita dasas) or ``"ak_based"``. ``"ayur"`` is
        refused — the text does not say how to weigh its aspects.
    :param dasa_years: passed through to §15.5.1 when a co-owned rasi's lord
        must be resolved for dasa purposes.
    :param atma_karaka_rasi: the rasi holding the AK, required by ``ak_based``.
    :raises RasiStrengthError: on an out-of-range rasi, the same rasi twice,
        an unknown or unimplemented purpose, or a missing AK when one is needed.
    """
    a = validate.in_range("first", first, 0, 11)
    b = validate.in_range("second", second, 0, 11)
    if a == b:
        raise RasiStrengthError("cannot compare a rasi with itself")
    if purpose not in PURPOSE_ADAPTATIONS:
        raise RasiStrengthError(
            f"unknown purpose {purpose!r}; expected one of {PURPOSES}"
        )
    adaptation = PURPOSE_ADAPTATIONS[purpose]
    if not adaptation["implemented"]:
        raise RasiStrengthError(
            f"{adaptation['name']} are not implemented: {adaptation['note']}"
        )
    if purpose == "ak_based" and atma_karaka_rasi is None:
        raise RasiStrengthError(
            "ak_based needs atma_karaka_rasi — 'the sign containing AK is "
            "stronger than any other rasi'"
        )

    rules: list[RuleVerdict] = []

    def add(rule, desc, winner, decided, detail):
        rules.append(RuleVerdict(
            rule=rule, description=desc, winner=winner,
            winner_name=RASI_NAMES[winner] if winner is not None else None,
            decided=decided, detail=detail,
        ))

    def finish(winner, decided_by, reason):
        return RasiVerdict(
            first=a, first_name=RASI_NAMES[a], second=b, second_name=RASI_NAMES[b],
            purpose=purpose, winner=winner,
            winner_name=RASI_NAMES[winner] if winner is not None else None,
            decided_by=decided_by, determined=winner is not None,
            reason=reason, rules=tuple(rules),
        )

    # --- AK pre-rule ---
    if purpose == "ak_based":
        assert atma_karaka_rasi is not None      # guarded above
        holds = [r for r in (a, b) if r == atma_karaka_rasi]
        detail = (
            f"AK is in {RASI_NAMES[atma_karaka_rasi]}"
            + (f", which is {RASI_NAMES[holds[0]]}" if len(holds) == 1 else "")
        )
        if len(holds) == 1:
            add("ak", "The sign containing AK is stronger than any other rasi",
                holds[0], True, detail)
            return finish(holds[0], "ak", detail)
        add("ak", "The sign containing AK is stronger than any other rasi",
            None, False, detail + " — neither rasi holds it")

    # --- Rule 1 ---
    counts = {r: len(occupants(r, longitudes)) for r in (a, b)}
    detail = "; ".join(
        f"{RASI_NAMES[r]} contains {n} planet{'s' if n != 1 else ''}"
        for r, n in counts.items()
    )
    if counts[a] != counts[b]:
        winner = max(counts, key=lambda r: counts[r])
        add("1", "If one rasi contains more planets than the other, it is "
            "stronger", winner, True, detail)
        return finish(winner, "1", detail)
    add("1", "If one rasi contains more planets than the other, it is stronger",
        None, False, detail + " — tie")

    # Lords are needed from rule 2 onward.
    lords: dict[int, int] = {}
    for rasi in (a, b):
        lord, why = lord_of(rasi, longitudes, dasa_years)
        if lord is None:
            add("2", "More of Jupiter, Mercury and the rasi's lord occupy or "
                "aspect it", None, None, why)
            return finish(None, None, why)
        lords[rasi] = lord

    # --- Rule 2 ---
    scores = {r: rule_2_count(r, co_lords_of(r), longitudes) for r in (a, b)}
    detail = "; ".join(
        f"{RASI_NAMES[r]} count {n}" + (f" ({', '.join(why)})" if why else "")
        for r, (n, why) in scores.items()
    )
    if scores[a][0] != scores[b][0]:
        winner = max(scores, key=lambda r: scores[r][0])
        add("2", "More of Jupiter, Mercury and the rasi's lord occupy or "
            "aspect it", winner, True, detail)
        return finish(winner, "2", detail)
    add("2", "More of Jupiter, Mercury and the rasi's lord occupy or aspect it",
        None, False, detail + " — tie")

    # --- AK placement rule, after rule 2 ---
    if purpose == "ak_based":
        assert atma_karaka_rasi is not None      # guarded above
        ak_rasi = atma_karaka_rasi

        def house_from_ak(rasi: int) -> int:
            return ((_sign(longitudes[lords[rasi]]) - ak_rasi) % 12) + 1

        places = {r: house_from_ak(r) for r in (a, b)}
        detail = "; ".join(
            f"{RASI_NAMES[r]}'s lord {GRAHA_NAMES[lords[r]]} is in the {h}th "
            f"from AK" for r, h in places.items()
        )
        ranked = {r: (2 if h in KENDRA else 1 if h in PANAPHARA else 0)
                  for r, h in places.items()}
        if ranked[a] != ranked[b]:
            winner = max(ranked, key=lambda r: ranked[r])
            add("ak-placement", "A rasi whose lord is in a quadrant from AK is "
                "stronger than a rasi whose lord is in a panaphara from AK",
                winner, True, detail)
            return finish(winner, "ak-placement", detail)
        add("ak-placement", "A rasi whose lord is in a quadrant from AK is "
            "stronger than a rasi whose lord is in a panaphara from AK",
            None, False, detail + " — tie")

    # --- Rule 3 ---
    exalted = {
        r: sorted(g for g in occupants(r, longitudes)
                  if EXALTATION_RASI.get(g) == r)
        for r in (a, b)
    }
    detail = "; ".join(
        f"{RASI_NAMES[r]} holds "
        + (", ".join(GRAHA_NAMES[g] for g in gs) + " exalted" if gs
           else "no exalted planet")
        for r, gs in exalted.items()
    )
    if bool(exalted[a]) != bool(exalted[b]):
        winner = a if exalted[a] else b
        add("3", "If one rasi contains an exalted planet and the other does "
            "not, the former is stronger", winner, True, detail)
        return finish(winner, "3", detail)
    add("3", "If one rasi contains an exalted planet and the other does not, "
        "the former is stronger", None, False, detail + " — tie")

    # --- Rule 4 ---
    differing = {
        r: RASI_IS_ODD[_sign(longitudes[lords[r]])] != RASI_IS_ODD[r]
        for r in (a, b)
    }
    detail = "; ".join(
        f"{RASI_NAMES[r]} ({'odd' if RASI_IS_ODD[r] else 'even'}) has its lord "
        f"{GRAHA_NAMES[lords[r]]} in "
        f"{RASI_NAMES[_sign(longitudes[lords[r]])]} "
        f"({'odd' if RASI_IS_ODD[_sign(longitudes[lords[r]])] else 'even'}) — "
        f"{'different' if d else 'same'} oddity"
        for r, d in differing.items()
    )
    if differing[a] != differing[b]:
        winner = a if differing[a] else b
        add("4", "A rasi whose lord is in a rasi with a different oddity is "
            "stronger", winner, True, detail)
        return finish(winner, "4", detail)
    add("4", "A rasi whose lord is in a rasi with a different oddity is "
        "stronger", None, False, detail + " — tie")

    # --- Rule 5 ---
    names = {1: "movable", 2: "fixed", 3: "dual"}
    ranks = {r: MODALITY_RANK[RASI_MODALITY[r]] for r in (a, b)}
    detail = "; ".join(f"{RASI_NAMES[r]} is {names[k]}" for r, k in ranks.items())
    if ranks[a] != ranks[b]:
        winner = max(ranks, key=lambda r: ranks[r])
        add("5", "Dual rasis are stronger than fixed rasis and fixed rasis are "
            "stronger than movable rasis", winner, True, detail)
        return finish(winner, "5", detail)
    add("5", "Dual rasis are stronger than fixed rasis and fixed rasis are "
        "stronger than movable rasis", None, False,
        detail + " — tie (always so when comparing a rasi and the 7th from it)")

    # --- Rule 6 ---
    advances = {r: advancement(longitudes[lords[r]], lords[r]) for r in (a, b)}
    detail = "; ".join(
        f"{RASI_NAMES[r]}'s lord {GRAHA_NAMES[lords[r]]} advanced "
        f"{int(adv)}°{round((adv - int(adv)) * 60):02d}'"
        + (" (from the end of the rasi)" if lords[r] in MEASURED_FROM_END else "")
        for r, adv in advances.items()
    )
    if advances[a] == advances[b]:
        add("6", "The rasi owned by the planet with the higher advancement is "
            "stronger", None, False, detail + " — tie")
        return finish(None, None, "every rule tied")
    winner = max(advances, key=lambda r: advances[r])
    add("6", "The rasi owned by the planet with the higher advancement is "
        "stronger", winner, True, detail)
    return finish(winner, "6", detail)
