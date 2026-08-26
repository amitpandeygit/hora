"""Argala and virodhargala — book chapter 10, sections 10.5 and 10.6.

§10.6 states the pairing outright: planets and houses in the 12th, 10th, 3rd
and 9th from a house or planet obstruct the argala on it from the 2nd, 4th,
11th and 5th *respectively*. So the four argala houses and their four
obstructors are one table read two ways, and are stored that way.

* **Ketu reverses the direction.** "If a sign contains Ketu, argalas and
  virodhargalas on it are counted anti-zodiacally." The reversal is a property
  of the *target* sign, not of the counting graha.
§10.5 further splits the four: the 2nd, 4th and 11th cause **primary** argala
and the 5th a **secondary** one. Every row carries which it is, and a
virodhargala inherits the kind of the argala it obstructs.

Two rules complicate the plain count:

* **Several malefics in the 3rd cause argala instead.** How many "several" is
  the chapter never says, and Exercise 16's own answer table declines to fire
  it on two. See ``SEVERAL_MALEFICS`` and docs/open-items.md OI-65.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    ARGALA_HOUSE_KIND,
    ARGALA_PAIRS,
    SEVERAL_MALEFICS,
    Graha,
)


class ArgalaError(validate.InputError):
    """An argala input that cannot be resolved."""


@dataclass(frozen=True, slots=True)
class Argala:
    """One argala or virodhargala on a target sign."""

    #: "argala" or "virodhargala".
    kind: str
    #: House counted from the target, 1-based.
    house: int
    #: The sign that house falls in.
    sign: int
    #: Grahas occupying it. Empty means the argala is simply absent.
    grahas: tuple[int, ...]
    #: The house this one obstructs, or is obstructed by.
    paired_house: int
    #: "primary" or "secondary". §10.5 makes the 2nd, 4th and 11th primary and
    #: the 5th secondary; a virodhargala inherits the kind of the argala it
    #: obstructs, so the 9th is secondary and the other three primary.
    argala_kind: str = "primary"
    #: True when this row was moved from virodhargala to argala by §10.6's
    #: several-malefics-in-the-3rd rule.
    promoted_from_virodhargala: bool = False


def counts_anti_zodiacally(sign: int, ketu_sign: int | None) -> bool:
    """§10.6's note: a sign holding Ketu has its argalas counted in reverse.

    A property of the target sign alone — a graha elsewhere counts normally
    even when Ketu sits in the sign it is counting *to*.
    """
    return ketu_sign is not None and sign == ketu_sign


def house_sign(sign: int, house: int, *, reverse: bool = False) -> int:
    """The sign a house falls in, counted from ``sign``.

    Inclusive counting: the 1st house from a sign is that sign. ``reverse``
    counts anti-zodiacally, per §10.6's Ketu note.
    """
    validate.in_range("sign", sign, 0, 11)
    validate.in_range("house", house, 1, 12)
    step = -(house - 1) if reverse else (house - 1)
    return (sign + step) % 12


def _malefics(grahas: tuple[int, ...], malefic: frozenset[int]) -> tuple[int, ...]:
    return tuple(g for g in grahas if g in malefic)


def argalas_on_sign(
    sign: int,
    occupants: dict[int, tuple[int, ...]],
    *,
    ketu_sign: int | None = None,
    malefic: frozenset[int] | None = None,
    several: int = SEVERAL_MALEFICS,
) -> list[Argala]:
    """Every argala and virodhargala on one sign, in the book's pairing order.

    :param occupants: sign index to the grahas in it.
    :param ketu_sign: where Ketu is, so §10.6's reversal can apply.
    :param malefic: which grahas count as malefic, for the 3rd-house rule.
        Omitted, the rule never fires and nothing is promoted.
    :param several: how many malefics in the 3rd count as "several". The book
        does not say; see ``SEVERAL_MALEFICS``.
    """
    validate.in_range("sign", sign, 0, 11)
    reverse = counts_anti_zodiacally(sign, ketu_sign)
    malefic = malefic or frozenset()

    out: list[Argala] = []
    for argala_house, virodha_house in ARGALA_PAIRS:
        for kind, house, paired in (
            ("argala", argala_house, virodha_house),
            ("virodhargala", virodha_house, argala_house),
        ):
            target = house_sign(sign, house, reverse=reverse)
            grahas = tuple(occupants.get(target, ()))
            promoted = False
            # §10.6: "If there are several malefics in the 3rd house from a
            # house or a planet, they cause argala instead of virodhargala on
            # that house or planet."
            if (kind == "virodhargala" and house == 3
                    and len(_malefics(grahas, malefic)) >= several):
                kind, promoted = "argala", True
            out.append(Argala(
                kind=kind, house=house, sign=target, grahas=grahas,
                paired_house=paired,
                argala_kind=ARGALA_HOUSE_KIND[argala_house],
                promoted_from_virodhargala=promoted,
            ))
    return out


def occupants_from(rasis: dict[int, int]) -> dict[int, tuple[int, ...]]:
    """Invert a graha-to-sign map into a sign-to-grahas map, in graha order."""
    out: dict[int, list[int]] = {}
    for graha in sorted(rasis):
        out.setdefault(int(rasis[graha]), []).append(int(graha))
    return {sign: tuple(grahas) for sign, grahas in out.items()}


def ketu_sign_of(rasis: dict[int, int]) -> int | None:
    """Where Ketu is, or None if he was not supplied."""
    value = rasis.get(int(Graha.KETU))
    return None if value is None else int(value)
