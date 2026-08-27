"""§11.5.4 Sankhya yogas — the seven counts, and the fallback rule.

"Sankhya means a number. Sankhya yogas are based on the number of distinct
signs occupied by the seven planets combined."

Seven planets can occupy one to seven distinct signs, and there is one yoga per
count, so **exactly one Sankhya yoga always matches on count alone**. What
decides whether it *applies* is the second sentence:

    "These yogas apply if no other Naabhasa yogas mentioned previously are
    applicable in a chart. These are the least important of all Naabhasa
    yogas."

That makes Sankhya the first family in the book whose presence depends on
another yoga's **absence**, and it is part of the definition — "apply if" —
not a qualifier on the results, so it does govern `present`. Kemadruma by
contrast kills another yoga's *results* and leaves it present; the two are
deliberately handled differently.

A verdict whose count matches but which is superseded says so in its reason,
naming the yoga that supersedes it, so nothing is hidden by the `present`
flag alone.

The nodes are excluded outright here — "Rahu and Ketu are not included" — the
clearest statement in the book on the question OI-73 asks, so this family
ignores `include_nodes` rather than honouring it.
"""
from __future__ import annotations

from hora.charts.planetary_yogas.registry import (
    YOGA_REGISTRY,
    YogaInput,
    YogaSpec,
    YogaVerdict,
    register,
)
from hora.core.const import GRAHA_NAMES, RASI_NAMES, SANKHYA_YOGAS, Graha

_SPEC = {entry["key"]: entry for entry in SANKHYA_YOGAS}

#: §11.5.4 counts "the seven planets combined", never nine.
SEVEN_PLANETS: tuple[int, ...] = (
    Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
    Graha.VENUS, Graha.SATURN,
)

#: The families §11.5.4 means by "no other Naabhasa yogas mentioned
#: previously" — §11.5.1, §11.5.2 and §11.5.3, in that order.
_EARLIER_NAABHASA = ("naabhasa_aasraya", "naabhasa_dala", "naabhasa_aakriti")


def occupied_signs(data: YogaInput) -> tuple[int, ...] | None:
    """The distinct signs the seven planets occupy, or None if any is missing.

    Counting from a partial chart would undercount, and undercounting shifts
    the answer to a different yoga rather than merely weakening it.
    """
    signs = []
    for graha in SEVEN_PLANETS:
        sign = data.sign_of(graha)
        if sign is None:
            return None
        signs.append(sign)
    return tuple(sorted(set(signs)))


def superseding_yoga(data: YogaInput) -> str | None:
    """The first earlier Naabhasa yoga that applies, if any.

    Evaluated in the book's own order — Aasraya, then Dala, then Aakriti — so
    the yoga named is the one a reader would reach first.
    """
    for group in _EARLIER_NAABHASA:
        for key, spec in YOGA_REGISTRY.items():
            if spec.group != group:
                continue
            if spec.detect(data).present:
                return key
    return None


def _make_detector(key: str):
    spec = _SPEC[key]
    name = spec["name"]
    wanted = spec["signs"]

    def detect(data: YogaInput) -> YogaVerdict:
        signs = occupied_signs(data)
        if signs is None:
            missing = [GRAHA_NAMES[g] for g in SEVEN_PLANETS
                       if data.sign_of(g) is None]
            named = ", ".join(missing)
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"this yoga counts the signs of all seven planets and "
                        f"{named} {'is' if len(missing) == 1 else 'are'} "
                        f"missing; it cannot be decided"),
            )
        count = len(signs)
        where = ", ".join(RASI_NAMES[s] for s in signs)
        if count != wanted:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"the seven planets occupy {count} distinct signs "
                        f"({where}), not {wanted}"),
            )

        superseded_by = superseding_yoga(data)
        if superseded_by is not None:
            return YogaVerdict(
                key=key, name=name, present=False,
                reason=(f"the seven planets do occupy {wanted} distinct signs "
                        f"({where}), but {YOGA_REGISTRY[superseded_by].name} "
                        f"applies and Sankhya yogas apply only when no earlier "
                        f"Naabhasa yoga does"),
            )
        return YogaVerdict(
            key=key, name=name, present=True,
            reason=(f"the seven planets occupy exactly {wanted} distinct signs "
                    f"({where}) and no earlier Naabhasa yoga applies"),
            participants=tuple(sorted(int(g) for g in SEVEN_PLANETS)),
        )

    return detect


for _key, _entry in _SPEC.items():
    register(YogaSpec(
        key=_key,
        name=_entry["name"],
        aliases=tuple(_entry["aliases"]),
        section="11.5.4",
        group="naabhasa_sankhya",
        definition=(
            f"If the seven planets occupy exactly {_entry['signs']} distinct "
            f"signs among them, this yoga is formed."
            if _entry["signs"] > 1 else
            "If the seven planets are in one sign, this yoga is formed."
        ),
        detect=_make_detector(_key),
    ))
