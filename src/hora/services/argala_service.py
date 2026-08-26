"""Argala and virodhargala endpoints — book chapter 10, §10.5 and §10.6.

Exercise 16 asks for every argala and virodhargala on all twelve houses at
once, so :func:`chart` answers in that shape. :func:`on_sign` answers one
target, which is the form §10.6's own worked example takes.

The 3rd-house malefic rule needs to know which grahas are malefic, and
chapter 3 makes that conditional for the Moon and Mercury. The caller supplies
the nature; this service never guesses one.
"""
from __future__ import annotations

from hora.charts.argala import (
    argalas_on_sign,
    counts_anti_zodiacally,
    ketu_sign_of,
    occupants_from,
)
from hora.core import validate
from hora.core.const import (
    ARGALA_BY_NATURE,
    ARGALA_DEFINITION,
    ARGALA_DOMINANCE_UNDETERMINED,
    ARGALA_HOUSE_KIND,
    ARGALA_HOUSE_ROLE,
    ARGALA_MEANS,
    ARGALA_NATURE_RULE,
    ARGALA_PAIRS,
    ARGALA_USE_CONCLUSION,
    ARGALA_USE_PROCEDURE,
    GRAHA_NAMES,
    INFLUENCE_RANKING,
    KETU_REVERSES_ARGALA,
    NAVAGRAHA,
    PRIMARY_ARGALA_RULE,
    RASI_NAMES,
    SECONDARY_ARGALA_RULE,
    SEVERAL_MALEFICS,
    THIRD_HOUSE_MALEFIC_RULE,
    VIRODHARGALA_DEFINITION,
    VIRODHARGALA_RULE,
    Graha,
)

InputError = validate.InputError

__all__ = ["InputError", "chart", "on_karaka", "on_sign", "rules"]

#: The grahas chapter 3 fixes as malefic whatever the chart. The Moon and
#: Mercury are conditional there and are deliberately left out: a caller who
#: wants the 3rd-house rule to see them must say so.
FIXED_MALEFICS: frozenset[int] = frozenset(
    {Graha.SUN, Graha.MARS, Graha.SATURN, Graha.RAHU, Graha.KETU}
)


#: House ordinals as the book writes them — 1st, 2nd, 3rd, then -th.
_ORDINAL_SUFFIX = {1: "st", 2: "nd", 3: "rd"}


def _ordinal(house: int) -> str:
    return f"{house}{_ORDINAL_SUFFIX.get(house, 'th')}"


def _validate_rasis(rasis: dict[int, int]) -> dict[int, int]:
    if not rasis:
        raise InputError("no placements given; supply at least one graha and rasi")
    out = {}
    for graha, rasi in rasis.items():
        if int(graha) not in set(NAVAGRAHA):
            raise InputError(f"unknown graha {graha!r}")
        validate.in_range(f"rasi for {GRAHA_NAMES[int(graha)]}", int(rasi), 0, 11)
        out[int(graha)] = int(rasi)
    return out


def _resolve_malefics(malefics: list[int] | None) -> frozenset[int]:
    if malefics is None:
        return FIXED_MALEFICS
    out = set()
    for graha in malefics:
        if int(graha) not in set(NAVAGRAHA):
            raise InputError(f"unknown graha {graha!r} in malefics")
        out.add(int(graha))
    return frozenset(out)


def _row(entry, occupants) -> dict:
    return {
        "kind": entry.kind,
        "house": entry.house,
        "sign": entry.sign,
        "sign_name": RASI_NAMES[entry.sign],
        "grahas": [
            {"graha": g, "graha_name": GRAHA_NAMES[g]} for g in entry.grahas
        ],
        "obstructs" if entry.kind == "argala" else "obstructed_by":
            entry.paired_house,
        "paired_house": entry.paired_house,
        "argala_kind": entry.argala_kind,
        "present": bool(entry.grahas),
        "promoted_from_virodhargala": entry.promoted_from_virodhargala,
    }


def on_sign(
    sign: int,
    rasis: dict[int, int],
    *,
    malefics: list[int] | None = None,
    several: int | None = None,
) -> dict:
    """Every argala and virodhargala on one sign."""
    several = SEVERAL_MALEFICS if several is None else several
    validate.in_range("sign", int(sign), 0, 11)
    sign = int(sign)
    rasis = _validate_rasis(rasis)
    occupants = occupants_from(rasis)
    ketu = ketu_sign_of(rasis)
    malefic = _resolve_malefics(malefics)
    entries = argalas_on_sign(
        sign, occupants, ketu_sign=ketu, malefic=malefic, several=several)

    argalas = [e for e in entries if e.kind == "argala"]
    virodhas = [e for e in entries if e.kind == "virodhargala"]

    # §10.6: an argala is obstructed when its paired house is occupied. An
    # empty obstructor leaves it standing — "If Le (3rd from Ge) is empty,
    # this argala is unobstructed."
    obstructed = {v.house: bool(v.grahas) for v in virodhas}

    # §10.7 step 3: "If there are both, see if more planets cause argala or
    # virodhargala." Counted over every graha in every argala house against
    # every graha in every virodhargala house.
    argala_count = sum(len(e.grahas) for e in argalas)
    virodha_count = sum(len(e.grahas) for e in virodhas)
    if argala_count == 0 and virodha_count == 0:
        dominant, reason = None, "neither argala nor virodhargala is present"
    elif argala_count > virodha_count:
        dominant, reason = "argala", "more planets cause argala"
    elif virodha_count > argala_count:
        dominant, reason = "virodhargala", "more planets cause virodhargala"
    else:
        # §10.7 step 4 needs a strength comparison. Chapter 15's simple-rules
        # measure is not built, so the engine stops rather than picking one.
        dominant, reason = None, ARGALA_DOMINANCE_UNDETERMINED

    return {
        "sign": sign,
        "sign_name": RASI_NAMES[sign],
        "counted_anti_zodiacally": counts_anti_zodiacally(sign, ketu),
        "argala_graha_count": argala_count,
        "virodhargala_graha_count": virodha_count,
        "primary_argala_graha_count": sum(
            len(e.grahas) for e in argalas if e.argala_kind == "primary"),
        "secondary_argala_graha_count": sum(
            len(e.grahas) for e in argalas if e.argala_kind == "secondary"),
        "dominant": dominant,
        "dominance_reason": reason,
        "ketu_sign": ketu,
        "argalas": [
            {**_row(e, occupants),
             "obstructed": obstructed.get(e.paired_house, False)}
            for e in argalas
        ],
        "virodhargalas": [_row(e, occupants) for e in virodhas],
    }


def on_karaka(
    graha: int,
    rasis: dict[int, int],
    *,
    malefics: list[int] | None = None,
    several: int | None = None,
) -> dict:
    """§10.7 step 1: "take the relevant house **or the relevant karaka**".

    Argala on a graha is argala on the sign it occupies — §10.6 says so
    outright: planets in the argala houses "cause argala on Vi *and on the
    planets in Vi*". So this resolves the graha to its sign and answers the
    same question, naming the graha it was asked about.
    """
    if int(graha) not in set(NAVAGRAHA):
        raise InputError(f"unknown graha {graha!r}")
    graha = int(graha)
    rasis = _validate_rasis(rasis)
    if graha not in rasis:
        raise InputError(
            f"{GRAHA_NAMES[graha]} has no placement; supply its rasi")
    result = on_sign(rasis[graha], rasis, malefics=malefics, several=several)
    return {
        "karaka": graha,
        "karaka_name": GRAHA_NAMES[graha],
        **result,
    }


def chart(
    rasis: dict[int, int],
    lagna_rasi: int,
    *,
    malefics: list[int] | None = None,
    several: int | None = None,
) -> dict:
    """Exercise 16's shape: all twelve houses, argalas and virodhargalas."""
    several = SEVERAL_MALEFICS if several is None else several
    rasis = _validate_rasis(rasis)
    validate.in_range("lagna_rasi", int(lagna_rasi), 0, 11)
    lagna_rasi = int(lagna_rasi)
    return {
        "lagna_rasi": lagna_rasi,
        "lagna_rasi_name": RASI_NAMES[lagna_rasi],
        "houses": [
            {"house": house,
             **on_sign((lagna_rasi + house - 1) % 12, rasis,
                       malefics=malefics, several=several)}
            for house in range(1, 13)
        ],
        "several_malefics_threshold": several,
    }


def rules() -> dict:
    """§10.6's rules, and what the engine does not decide."""
    return {
        "argala_means": ARGALA_MEANS,
        "argala_definition": ARGALA_DEFINITION,
        "primary_rule": PRIMARY_ARGALA_RULE,
        "secondary_rule": SECONDARY_ARGALA_RULE,
        "house_kinds": dict(ARGALA_HOUSE_KIND),
        "nature_rule": ARGALA_NATURE_RULE,
        # §10.5 ranks all three influences in one passage. Ordinal only — the
        # chapter gives "small", "more concrete" and "decisive" and no number.
        "influence_ranking": [dict(r) for r in INFLUENCE_RANKING],
        "definition": VIRODHARGALA_DEFINITION,
        "rule": VIRODHARGALA_RULE,
        "pairs": [
            {"argala_house": a, "virodhargala_house": v,
             "argala_kind": ARGALA_HOUSE_KIND[a],
             "text": f"the {_ordinal(v)} obstructs the argala from the {_ordinal(a)}"}
            for a, v in ARGALA_PAIRS
        ],
        "by_nature": {k: dict(v) for k, v in ARGALA_BY_NATURE.items()},
        "ketu_note": KETU_REVERSES_ARGALA,
        "third_house_rule": THIRD_HOUSE_MALEFIC_RULE,
        "several_malefics_threshold": SEVERAL_MALEFICS,
        "use_procedure": [dict(step) for step in ARGALA_USE_PROCEDURE],
        "house_roles": [
            {"house": house, **{k: v for k, v in entry.items()}}
            for house, entry in ARGALA_HOUSE_ROLE.items()
        ],
        "use_conclusion": ARGALA_USE_CONCLUSION,
        "dominance_note": (
            "Step 3 is computed: `dominant` names whichever of argala and "
            "virodhargala is caused by more planets. Step 4 is not — when the "
            "counts tie, `dominant` is null and `dominance_reason` says why. "
            "Step 5 says \u201cguess\u201d, and nothing here guesses."
        ),
        "several_malefics_note": (
            "The book does not say how many malefics count as “several”. "
            "Exercise 16's own answer table leaves two malefics in the 3rd as "
            "virodhargala — Mars and Saturn in Sc, the 3rd from the 11th "
            "house — so three is the smallest threshold that reproduces "
            "it. Configurable per call. See docs/open-items.md OI-65."
        ),
        "fixed_malefics": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
            for g in sorted(FIXED_MALEFICS)
        ],
        "malefics_note": (
            "Chapter 3 makes the Moon and Mercury conditionally malefic, so "
            "they are not in the default set. Supply `malefics` to override it."
        ),
    }
