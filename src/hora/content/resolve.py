"""Deciding which conditional clauses of an entry apply to a given chart.

The book writes results with bracketed conditions — "[in lagna] lame", "[if
waning] sinful", "[in 5th with Rahu] faces a severe fall". :mod:`store` keeps
those as structured :class:`~hora.content.store.Condition` objects. This module
answers "which of them fire, for this planet in this chart?"

**Nothing here computes astrology.** It takes an already-computed placement as
plain values and does set membership. That keeps the content package free of
any import from ``hora.charts``, which is the boundary the store's docstring
sets out.

A condition whose input was not supplied is **undetermined**, never false. An
API that quietly dropped "[conjoined by malefics] poor" because nobody passed
the aspects would be inventing a favourable reading by omission.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.content.store import Condition, Entry, Result


@dataclass(frozen=True, slots=True)
class Placement:
    """What is known about a graha's placement, for resolving conditions.

    Every field is optional. An omitted field makes any condition that needs
    it undetermined rather than false.
    """

    house: int | None = None
    rasi: int | None = None
    #: Grahas sharing the rasi.
    joined_by: frozenset[int] = frozenset()
    #: Whether the graha is conjoined or aspected by malefics / benefics.
    #: None means unknown — this engine does not compute aspects (OI-18).
    associated_with_malefics: bool | None = None
    associated_with_benefics: bool | None = None
    #: "waxing" or "waning", for the Moon.
    moon_phase: str | None = None
    #: The graha's dignity, e.g. "exalted", "own", "friend".
    dignity: str | None = None
    #: "malefic" or "benefic" — nature of the lord of the occupied rasi.
    rasi_lord: str | None = None
    #: "strong" or "weak". No measure in this book can set it; see
    #: /v1/strength/measures. Left None, conditions on it stay undetermined.
    strength: str | None = None


@dataclass(frozen=True, slots=True)
class ResolvedResult:
    """One clause, with whether it applies here."""

    text: str
    applies: bool | None
    reason: str
    conditional: bool


def _test(condition: Condition, placement: Placement) -> tuple[bool | None, str]:
    """Evaluate one condition. Returns (applies, reason)."""
    if condition.unconditional:
        return True, "unconditional"
    if condition.otherwise:
        # Handled by the caller, which needs the sibling clauses to decide.
        return None, "the [else] branch, decided against its siblings"

    checks: list[tuple[bool | None, str]] = []

    if condition.houses:
        wanted = ", ".join(str(h) for h in condition.houses)
        if placement.house is None:
            checks.append((None, f"needs the house (wants {wanted})"))
        else:
            checks.append((
                placement.house in condition.houses,
                f"house {placement.house}, wants {wanted}",
            ))
    if condition.rasis:
        if placement.rasi is None:
            checks.append((None, "needs the rasi"))
        else:
            checks.append((
                placement.rasi in condition.rasis,
                f"rasi {placement.rasi}, wants {list(condition.rasis)}",
            ))
    if condition.joined_by:
        checks.append((
            all(g in placement.joined_by for g in condition.joined_by),
            f"joined by {sorted(placement.joined_by)}, wants {list(condition.joined_by)}",
        ))
    if condition.associated_with:
        known = (
            placement.associated_with_malefics
            if condition.associated_with == "malefics"
            else placement.associated_with_benefics
        )
        if known is None:
            missing = (
                f"needs to know about association with "
                f"{condition.associated_with} "
                f"(aspects are not computed — see OI-18)"
            )
            checks.append((None, missing))
        else:
            checks.append((known, f"associated with {condition.associated_with}: {known}"))
    if condition.not_joined_by:
        absent = [g for g in condition.not_joined_by if g not in placement.joined_by]
        detail = (
            f"joined by {sorted(placement.joined_by)}, wants none of "
            f"{list(condition.not_joined_by)}"
        )
        checks.append((len(absent) == len(condition.not_joined_by), detail))
    if condition.rasi_lord:
        if placement.rasi_lord is None:
            detail = (
                f"needs the rasi lord's nature (wants {condition.rasi_lord})"
            )
            checks.append((None, detail))
        else:
            checks.append((
                placement.rasi_lord == condition.rasi_lord,
                f"rasi lord is {placement.rasi_lord}, wants {condition.rasi_lord}",
            ))
    if condition.strength:
        if placement.strength is None:
            detail = (
                f"needs to know if the graha is {condition.strength}; no "
                f"measure in this book settles that "
                f"(see /v1/strength/measures)"
            )
            checks.append((None, detail))
        else:
            checks.append((
                placement.strength == condition.strength,
                f"strength {placement.strength}, wants {condition.strength}",
            ))
    if condition.moon_phase:
        if placement.moon_phase is None:
            checks.append((None, f"needs the moon phase (wants {condition.moon_phase})"))
        else:
            checks.append((
                placement.moon_phase == condition.moon_phase,
                f"moon is {placement.moon_phase}, wants {condition.moon_phase}",
            ))
    if condition.dignity:
        if placement.dignity is None:
            checks.append((None, "needs the dignity"))
        else:
            checks.append((
                placement.dignity in condition.dignity,
                f"dignity {placement.dignity}, wants {list(condition.dignity)}",
            ))

    reason = "; ".join(text for _v, text in checks)
    if any(value is False for value, _t in checks):
        return False, reason
    if any(value is None for value, _t in checks):
        return None, reason
    return True, reason


def resolve(entry: Entry, placement: Placement) -> list[ResolvedResult]:
    """Which of an entry's clauses apply to this placement.

    The "[else]" clause fires only when every sibling *conditional* clause is
    determined and none of them applies. If any sibling is undetermined, the
    else branch is undetermined too — we cannot know it is the fallback until
    we know the others are not.
    """
    verdicts: list[tuple[Result, bool | None, str]] = []
    for result in entry.results:
        applies, reason = _test(result.condition, placement)
        verdicts.append((result, applies, reason))

    conditional_siblings = [
        (applies, result) for result, applies, _r in verdicts
        if not result.condition.unconditional and not result.condition.otherwise
    ]

    out: list[ResolvedResult] = []
    for result, applies, reason in verdicts:
        if result.condition.otherwise:
            if any(a is None for a, _r in conditional_siblings):
                applies, reason = None, "a sibling condition is undetermined"
            else:
                fired = any(a for a, _r in conditional_siblings)
                applies = not fired
                reason = (
                    "another branch applies" if fired
                    else "no other branch applies, so the [else] branch does"
                )
        out.append(ResolvedResult(
            text=result.text,
            applies=applies,
            reason=reason,
            conditional=not result.condition.unconditional,
        ))
    return out
