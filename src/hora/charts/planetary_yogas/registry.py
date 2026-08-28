"""The yoga registry, and the contract every detector obeys.

A yoga is a :class:`YogaSpec`: what the book calls it, where it is defined,
its verbatim definition, and a detector. :func:`evaluate` walks the whole
registry, so adding a yoga to the registry is the only step needed to have it
computed, published and reported on — it cannot be added and then forgotten.

Every detector returns a :class:`YogaVerdict` whether or not the yoga is
present. An absent yoga carries the reason it is absent, because "we did not
find it" and "we did not look" have to be distinguishable in the output.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from hora.core import validate
from hora.core.const import GRAHA_NAMES, NAVAGRAHA, RASI_NAMES, Graha
from hora.core.ephemeris.base import PlanetPosition


class YogaError(validate.InputError):
    """A yoga input that cannot be resolved."""


@dataclass(frozen=True, slots=True)
class YogaInput:
    """Everything a detector may look at.

    :param rasis: graha id to sign index, 0 = Aries.
    :param chart: which chart these positions are from — "D1", "D9", "D10".
        Recorded rather than used: §11.2 says the Ravi yogas are worth more in
        a divisional chart, and the caller needs that back.
    :param positions: the chart's `PlanetPosition` objects, when the caller
        has them. Needed only for qualifiers like combustion, which also
        depends on retrogression; a detector must work without them, and must
        never read their absence as a negative finding.
    :param include_nodes: whether Rahu and Ketu count as "a planet" in a
        definition that says so. Off by default — see OI-73.
    :param lagna_rasi: needed by §11.3.4's Kemadruma, the only yoga so far
        that reads a house from the ascendant rather than from a graha. A
        detector that needs it and does not have it must say so, not guess.
    :param paksha: 0 Sukla, 1 Krishna. The Moon has no benefic nature without
        it (§3.2.2), so a rule counting benefics is unanswerable without it.
    :param lagna_longitude: the ascendant in degrees. §11.7.3's yogas 7 and 9
        read the lagna of a divisional chart, which the sign alone cannot
        give. Absent, those yogas say so.
    :param special_lagnas: HL, GL and any other special lagna, in degrees.
        §11.7.3's yogas 6 and 8 turn on them, and they are computed from
        birth data rather than from a graha, so they are supplied rather than
        derived here.
    """

    rasis: dict[int, int]
    chart: str = "D1"
    positions: dict[int, PlanetPosition] | None = None
    include_nodes: bool = False
    lagna_rasi: int | None = None
    paksha: int | None = None
    lagna_longitude: float | None = None
    special_lagnas: dict[str, float] | None = None

    def special_lagna_sign(self, name: str) -> int | None:
        """The sign a special lagna falls in, or None if it was not given."""
        if not self.special_lagnas:
            return None
        value = self.special_lagnas.get(name)
        return None if value is None else int(value % 360.0 // 30)

    def sign_of(self, graha: int) -> int | None:
        return self.rasis.get(int(graha))

    def occupants(self, sign: int) -> tuple[int, ...]:
        return tuple(g for g in sorted(self.rasis) if self.rasis[g] == sign)

    def benefics(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """(benefics, undecidable) among the placed grahas, per §3.2.2.

        The second tuple is grahas whose nature could not be judged from what
        was supplied — the Moon without a paksha. A caller must be able to
        tell "not a benefic" from "we could not say".
        """
        from hora.charts.benefic import BeneficError, nature

        benefic: list[int] = []
        unknown: list[int] = []
        for graha in sorted(self.rasis):
            companions = frozenset(
                g for g in self.occupants(self.rasis[graha]) if g != graha
            )
            try:
                result = nature(graha, paksha=self.paksha, companions=companions)
            except BeneficError:
                unknown.append(graha)
                continue
            if result.nature == "benefic":
                benefic.append(graha)
        return tuple(benefic), tuple(unknown)

    def considered(self) -> tuple[int, ...]:
        """Grahas a definition saying "a planet" may draw on."""
        skip = () if self.include_nodes else (int(Graha.RAHU), int(Graha.KETU))
        return tuple(g for g in NAVAGRAHA if int(g) not in skip)


@dataclass(frozen=True, slots=True)
class YogaVerdict:
    """One yoga's verdict on one chart."""

    key: str
    name: str
    present: bool
    #: Why, either way. Always populated — an absent yoga says what was missing.
    reason: str
    #: Grahas forming the yoga, in graha order. Empty when absent.
    participants: tuple[int, ...] = ()
    #: Which house from the reference each participant occupies.
    houses: dict[int, int] = field(default_factory=dict)
    #: Qualifiers that weaken the yoga without cancelling it — §11.2.4's
    #: combustion is the first. Never used to flip `present`.
    qualifiers: tuple[str, ...] = ()
    #: True when the book itself says this yoga "may not operate well" —
    #: §11.5.2's Dala clause. Distinct from `qualifiers`, which merely
    #: annotate: this one is the book's own statement that the yoga does not
    #: fully operate, and §11.5.4's fallback turns on it. See OI-80.
    weakened: bool = False


@dataclass(frozen=True, slots=True)
class YogaSpec:
    key: str
    name: str
    aliases: tuple[str, ...]
    section: str
    group: str
    definition: str
    detect: Callable[[YogaInput], YogaVerdict]
    #: Yogas whose presence this one implies. §11.2.3's Ubhayachara requires
    #: both the 2nd and the 12th, so it cannot hold without Vesi and Vosi.
    implies: tuple[str, ...] = ()


#: Populated by each group module at import time.
YOGA_REGISTRY: dict[str, YogaSpec] = {}


def register(spec: YogaSpec) -> YogaSpec:
    if spec.key in YOGA_REGISTRY:
        raise ValueError(f"duplicate yoga key {spec.key!r}")
    YOGA_REGISTRY[spec.key] = spec
    return spec


def _validate(data: YogaInput) -> None:
    if not data.rasis:
        raise YogaError("no placements given; supply at least one graha and rasi")
    for graha, sign in data.rasis.items():
        if int(graha) not in set(NAVAGRAHA):
            raise YogaError(f"unknown graha {graha!r}")
        validate.in_range(
            f"rasi for {GRAHA_NAMES[int(graha)]}", int(sign), 0, 11)


def evaluate_one(key: str, data: YogaInput) -> YogaVerdict:
    """One yoga by key."""
    spec = YOGA_REGISTRY.get(key)
    if spec is None:
        raise YogaError(
            f"unknown yoga {key!r}; expected one of "
            f"{', '.join(sorted(YOGA_REGISTRY))}"
        )
    _validate(data)
    return spec.detect(data)


def evaluate(data: YogaInput, *, group: str | None = None) -> list[YogaVerdict]:
    """**Every** registered yoga, present or not, in registry order.

    Absent yogas are returned too. A caller building a reading needs to know
    that a yoga was checked and did not hold, which is not the same as its
    being missing from the response.
    """
    _validate(data)
    return [
        spec.detect(data)
        for spec in YOGA_REGISTRY.values()
        if group is None or spec.group == group
    ]


def groups() -> list[str]:
    seen: list[str] = []
    for spec in YOGA_REGISTRY.values():
        if spec.group not in seen:
            seen.append(spec.group)
    return seen


def describe(spec: YogaSpec) -> dict:
    return {
        "key": spec.key,
        "name": spec.name,
        "aliases": list(spec.aliases),
        "section": spec.section,
        "group": spec.group,
        "definition": spec.definition,
        "implies": list(spec.implies),
    }


def serialise(verdict: YogaVerdict) -> dict:
    return {
        "key": verdict.key,
        "name": verdict.name,
        "present": verdict.present,
        "reason": verdict.reason,
        "participants": [
            {"graha": g, "graha_name": GRAHA_NAMES[g],
             "sign": None, "house_from_reference": verdict.houses.get(g)}
            for g in verdict.participants
        ],
        "qualifiers": list(verdict.qualifiers),
    }


__all__ = [
    "RASI_NAMES",
    "YOGA_REGISTRY",
    "YogaError",
    "YogaInput",
    "YogaSpec",
    "YogaVerdict",
    "describe",
    "evaluate",
    "evaluate_one",
    "groups",
    "register",
    "serialise",
]
