"""Stronger co-lord — book §15.5.1.

The rule §9.2 defers to. Scorpio is co-owned by Mars and Ketu, Aquarius by
Saturn and Rahu; the stronger acts as lord and decides the arudha pada. The
same choice sets the dasa duration of Sc or Aq in rasi dasas such as Narayana.

    "The stronger planet of two planets is determined using the following
    rules. We go from one rule to the next, only if we do not have a winner.
    If we have a winner in one step, we do not go through the remaining steps."

That sentence is the whole design. The cascade **stops** at the first rule that
decides, and — the part easy to get wrong — a rule that *cannot be evaluated*
stops it too, with no winner. Skipping an undecidable rule to reach a later one
would let a lower rule answer a question a higher one might have settled
differently.

    basic  one co-lord sits in the rasi itself -> take the other
    1      more planets joined -> stronger
    2      more of {Jupiter, Mercury, dispositor} conjoin or aspect -> stronger
    3      exalted beats not exalted
    4      dual rasi beats fixed beats movable
    5a     (dasa duration) the planet giving the longer dasa
    5b     (arudha padas) the planet more advanced in its rasi

Rule 2 needs **rasi** aspects and now computes them itself, from
``charts.aspects.rasi_drishti``. That function was wrong until §15.5.1's own
rule-2 example exposed it — Leo did not aspect Aries — and was corrected;
see docs/open-items.md OI-27. ``rasi_aspects`` remains an override for a
caller who wants a different table.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.charts.aspects import rasi_drishti
from hora.core import validate
from hora.core.const import (
    EXALTATION_RASI,
    GRAHA_NAMES,
    RASI_LORD,
    RASI_MODALITY,
    RASI_NAMES,
    Graha,
    Rasi,
)


class CoLordError(validate.InputError):
    """A co-lord comparison that cannot be made."""


#: §15.5.1: the two co-owned rasis and their co-lords.
CO_LORDS: dict[int, tuple[int, int]] = {
    Rasi.SCORPIO: (Graha.MARS, Graha.KETU),
    Rasi.AQUARIUS: (Graha.SATURN, Graha.RAHU),
}

#: Rule 4: "Dual rasis are stronger than fixed rasis and fixed rasis are
#: stronger than movable rasis." RASI_MODALITY is 0 movable, 1 fixed, 2 dual,
#: which is already the ranking order.
MODALITY_RANK = {0: 1, 1: 2, 2: 3}

#: Rule 2's three roles. The book counts them as roles, not as distinct
#: planets: "Saturn is conjoined by Mercury and his dispositor (who is Mercury
#: again). His count is 2."
RULE_2_ROLES = ("Jupiter", "Mercury", "dispositor")


def default_rasi_aspects() -> dict[int, tuple[int, ...]]:
    """Jaimini rasi drishti for all twelve signs — rule 2's default table."""
    return {sign: rasi_drishti(sign) for sign in range(12)}

#: What the tie-break at step 5 is for.
PURPOSES = ("arudha", "dasa")

#: Rule 5b: "We measure the advancement of Rahu and Ketu from the end of the
#: rasi." **Both** nodes, unlike §8.2's chara karakas, which measure only Rahu
#: from the end because they exclude Ketu altogether. Reusing chapter 8's
#: helper here gave Ketu the wrong advancement and lost §15.5.1's own worked
#: example; the two rules are kept separate deliberately.
MEASURED_FROM_END = frozenset({Graha.RAHU, Graha.KETU})


def rule_5b_advancement(longitude: float, graha: int) -> float:
    """Degrees advanced in the occupied rasi, per rule 5b."""
    within = validate.longitude("longitude", longitude) % 30.0
    return 30.0 - within if graha in MEASURED_FROM_END else within


@dataclass(frozen=True)
class RuleVerdict:
    """One rule of the cascade, and what it decided."""

    rule: str
    description: str
    winner: int | None
    winner_name: str | None
    #: True when the rule was evaluated at all. False means the cascade
    #: stopped before it.
    evaluated: bool
    #: None when the rule could not be evaluated from the inputs given.
    decided: bool | None
    detail: str


@dataclass(frozen=True)
class CoLordVerdict:
    """The primary lord of a co-owned rasi, and how it was reached."""

    rasi: int
    rasi_name: str
    co_lords: tuple[int, int]
    co_lord_names: tuple[str, str]
    winner: int | None
    winner_name: str | None
    decided_by: str | None
    determined: bool
    reason: str
    rules: tuple[RuleVerdict, ...]


def _sign(longitude: float) -> int:
    return int(validate.longitude("longitude", longitude) // 30.0)


def _co_tenants(graha: int, longitudes: dict[int, float]) -> set[int]:
    sign = _sign(longitudes[graha])
    return {g for g, lon in longitudes.items() if g != graha and _sign(lon) == sign}


def rule_2_count(
    graha: int,
    longitudes: dict[int, float],
    rasi_aspects: dict[int, tuple[int, ...]],
) -> tuple[int, list[str]]:
    """How many of Jupiter, Mercury and the dispositor conjoin or aspect a graha.

    Counted by **role**, so a dispositor that is also Mercury contributes twice
    — which is exactly what §15.5.1's example does.
    """
    target = _sign(longitudes[graha])
    dispositor = int(RASI_LORD[target])
    roles = [
        ("Jupiter", int(Graha.JUPITER)),
        ("Mercury", int(Graha.MERCURY)),
        ("dispositor", dispositor),
    ]
    count, why = 0, []
    for role, other in roles:
        if other not in longitudes or other == graha:
            continue
        other_sign = _sign(longitudes[other])
        if other_sign == target:
            count += 1
            why.append(f"{role} ({GRAHA_NAMES[other]}) conjoins")
        elif target in rasi_aspects.get(other_sign, ()):
            count += 1
            why.append(f"{role} ({GRAHA_NAMES[other]}) aspects from {RASI_NAMES[other_sign]}")
    return count, why


def stronger(
    rasi: int,
    longitudes: dict[int, float],
    purpose: str = "arudha",
    rasi_aspects: dict[int, tuple[int, ...]] | None = None,
    dasa_years: dict[int, float] | None = None,
    advancement_known: bool = True,
) -> CoLordVerdict:
    """The primary lord of Scorpio or Aquarius, by §15.5.1's cascade.

    :param rasi: Scorpio (7) or Aquarius (10).
    :param longitudes: sidereal longitude per graha; both co-lords required.
    :param purpose: ``"arudha"`` uses rule 5b (more advanced in its rasi);
        ``"dasa"`` uses rule 5a (the longer dasa), which needs ``dasa_years``.
    :param rasi_aspects: sign -> signs it aspects, for rule 2. Defaults to
        Jaimini rasi drishti. Pass a different table to override it; pass an
        empty dict to model "no aspects known", which stops the cascade at
        rule 2 rather than skipping to rule 3.
    :param dasa_years: graha -> dasa length, for rule 5a only.
    :param advancement_known: False when the caller has only signs, not
        longitudes. Rules basic to 4 need nothing finer than a sign, so the
        cascade still runs; rule 5b then reports that it needs longitudes
        instead of comparing two zeros and calling it a tie.
    :raises CoLordError: on a rasi that is not co-owned, a missing co-lord, or
        an unknown purpose.
    """
    index = validate.in_range("rasi", rasi, 0, 11)
    if index not in CO_LORDS:
        owned = " and ".join(RASI_NAMES[r] for r in sorted(CO_LORDS))
        raise CoLordError(
            f"{RASI_NAMES[index]} has one lord; §15.5.1 applies to {owned}"
        )
    if purpose not in PURPOSES:
        raise CoLordError(f"unknown purpose {purpose!r}; expected one of {PURPOSES}")

    first, second = CO_LORDS[index]
    for graha in (first, second):
        if graha not in longitudes:
            raise CoLordError(f"no position given for {GRAHA_NAMES[graha]}")

    rules: list[RuleVerdict] = []

    def add(rule, desc, winner, decided, detail) -> RuleVerdict:
        verdict = RuleVerdict(
            rule=rule, description=desc, winner=winner,
            winner_name=GRAHA_NAMES[winner] if winner is not None else None,
            evaluated=True, decided=decided, detail=detail,
        )
        rules.append(verdict)
        return verdict

    def finish(winner, decided_by, reason) -> CoLordVerdict:
        return CoLordVerdict(
            rasi=index, rasi_name=RASI_NAMES[index],
            co_lords=(int(first), int(second)),
            co_lord_names=(GRAHA_NAMES[first], GRAHA_NAMES[second]),
            winner=winner,
            winner_name=GRAHA_NAMES[winner] if winner is not None else None,
            decided_by=decided_by, determined=winner is not None,
            reason=reason, rules=tuple(rules),
        )

    # --- Basic rule ---
    in_rasi = [g for g in (first, second) if _sign(longitudes[g]) == index]
    if len(in_rasi) == 1:
        other = second if in_rasi[0] == first else first
        verdict = add(
            "basic", "If one of the co-lords is in the rasi, take the other planet",
            other, True,
            f"{GRAHA_NAMES[in_rasi[0]]} is in {RASI_NAMES[index]}, so "
            f"{GRAHA_NAMES[other]} is the primary lord",
        )
        return finish(other, "basic", verdict.detail)
    add("basic", "If one of the co-lords is in the rasi, take the other planet",
        None, False,
        "both co-lords are in the rasi" if in_rasi
        else "neither co-lord is in the rasi")

    # --- Rule 1: more planets joined ---
    counts = {g: len(_co_tenants(g, longitudes)) for g in (first, second)}
    detail = "; ".join(
        f"{GRAHA_NAMES[g]} with {n} other planet{'s' if n != 1 else ''}"
        for g, n in counts.items()
    )
    if counts[first] != counts[second]:
        winner = max(counts, key=lambda g: counts[g])
        add("1", "If one planet is joined by more planets than the other, it "
            "is stronger", winner, True, detail)
        return finish(winner, "1", detail)
    add("1", "If one planet is joined by more planets than the other, it is "
        "stronger", None, False, detail + " — tie")

    # --- Rule 2: Jupiter, Mercury, dispositor ---
    aspects = default_rasi_aspects() if rasi_aspects is None else rasi_aspects
    if not aspects:
        add("2", "More of Jupiter, Mercury and the dispositor conjoin or "
            "aspect it", None, None,
            "no rasi aspects available; the cascade stops here rather than "
            "skipping to rule 3")
        return finish(None, None, "rule 2 could not be evaluated")
    scores = {g: rule_2_count(g, longitudes, aspects) for g in (first, second)}
    detail = "; ".join(
        f"{GRAHA_NAMES[g]} count {n}" + (f" ({', '.join(why)})" if why else "")
        for g, (n, why) in scores.items()
    )
    if scores[first][0] != scores[second][0]:
        winner = max(scores, key=lambda g: scores[g][0])
        add("2", "More of Jupiter, Mercury and the dispositor conjoin or "
            "aspect it", winner, True, detail)
        return finish(winner, "2", detail)
    add("2", "More of Jupiter, Mercury and the dispositor conjoin or aspect "
        "it", None, False, detail + " — tie")

    # --- Rule 3: exaltation ---
    exalted = {
        g: EXALTATION_RASI.get(g) == _sign(longitudes[g]) for g in (first, second)
    }
    detail = "; ".join(
        f"{GRAHA_NAMES[g]} in {RASI_NAMES[_sign(longitudes[g])]}"
        + (" (exalted)" if e else "")
        for g, e in exalted.items()
    )
    if exalted[first] != exalted[second]:
        winner = first if exalted[first] else second
        add("3", "If one planet is exalted and the other not, the exalted "
            "planet is stronger", winner, True, detail)
        return finish(winner, "3", detail)
    add("3", "If one planet is exalted and the other not, the exalted planet "
        "is stronger", None, False, detail + " — tie")

    # --- Rule 4: natural strength of the rasi ---
    ranks = {g: MODALITY_RANK[RASI_MODALITY[_sign(longitudes[g])]]
             for g in (first, second)}
    names = {1: "movable", 2: "fixed", 3: "dual"}
    detail = "; ".join(
        f"{GRAHA_NAMES[g]} in {RASI_NAMES[_sign(longitudes[g])]} ({names[r]})"
        for g, r in ranks.items()
    )
    if ranks[first] != ranks[second]:
        winner = max(ranks, key=lambda g: ranks[g])
        add("4", "Dual rasis are stronger than fixed rasis and fixed rasis "
            "are stronger than movable rasis", winner, True, detail)
        return finish(winner, "4", detail)
    add("4", "Dual rasis are stronger than fixed rasis and fixed rasis are "
        "stronger than movable rasis", None, False, detail + " — tie")

    # --- Rule 5 ---
    if purpose == "dasa":
        if dasa_years is None or not all(g in dasa_years for g in (first, second)):
            add("5a", "When finding dasa duration: take the planet giving a "
                "larger length for dasa", None, None,
                "needs the dasa length each planet would give, which was not "
                "supplied")
            return finish(None, None, "rule 5a could not be evaluated")
        detail = "; ".join(
            f"{GRAHA_NAMES[g]} gives {dasa_years[g]:g} years" for g in (first, second)
        )
        if dasa_years[first] == dasa_years[second]:
            add("5a", "When finding dasa duration: take the planet giving a "
                "larger length for dasa", None, False, detail + " — tie")
            return finish(None, None, "every rule tied")
        winner = max((first, second), key=lambda g: dasa_years[g])
        add("5a", "When finding dasa duration: take the planet giving a larger "
            "length for dasa", winner, True, detail)
        return finish(winner, "5a", detail)

    # 5b — the arudha branch.
    if not advancement_known:
        add("5b", "When finding the lord for arudha padas: take the planet "
            "more advanced in its rasi", None, None,
            "needs longitudes; only signs were supplied, and advancement "
            "within a rasi cannot be read from a sign")
        return finish(None, None,
                      "rule 5b needs longitudes, which were not supplied")
    advances = {g: rule_5b_advancement(longitudes[g], g) for g in (first, second)}
    detail = "; ".join(
        f"{GRAHA_NAMES[g]} advanced {int(a)}°{round((a - int(a)) * 60):02d}'"
        + (" (from the end of the rasi)" if g in MEASURED_FROM_END else "")
        for g, a in advances.items()
    )
    if advances[first] == advances[second]:
        add("5b", "When finding the lord for arudha padas: take the planet "
            "more advanced in its rasi", None, False, detail + " — tie")
        return finish(None, None, "every rule tied")
    winner = max(advances, key=lambda g: advances[g])
    add("5b", "When finding the lord for arudha padas: take the planet more "
        "advanced in its rasi", winner, True, detail)
    return finish(winner, "5b", detail)
