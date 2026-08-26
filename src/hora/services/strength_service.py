"""Strength and avastha service — book chapter 15.

Shapes §15.4's states and the two-planet comparison for the API. Every
response says which measures of strength exist and which are available, so a
caller is never left assuming that "strength" means the one we happen to have.
"""
from __future__ import annotations

from hora.charts.avastha import (
    AvasthaError,
    all_avasthas,
    avastha_by_activity,
    ghati_at_birth,
    sound_number,
)
from hora.charts.strength import BOOK_CAVEAT, StrengthError, compare
from hora.core import validate
from hora.core.const import (
    ACTIVITY_IS_MOST_IMPORTANT,
    ACTIVITY_STRENGTH,
    ADDITIONAL_MOOD_AVASTHAS,
    AGE_AVASTHA_CAUTION,
    AGE_AVASTHAS,
    ALERTNESS_AVASTHAS,
    AVASTHA_EFFECTS,
    GHATI_NOTE,
    GHATIS_PER_HOUR,
    MOOD_AVASTHAS,
    NAVAMSA_INDEX_NOTE,
    SAYANAADI_AVASTHAS,
    SAYANAADI_FORMULA,
    SAYANAADI_TERMS,
    SOUND_NUMBERS,
    STRENGTH_MEASURES,
    VICHESHTA_REMAINDER_NOTE,
)
from hora.core.ephemeris.base import PlanetPosition

InputError = validate.InputError

__all__ = [
    "AvasthaError", "InputError", "StrengthError",
    "activity", "activity_results", "avasthas", "comparison", "ghatis",
    "measures", "rules", "sound",
]


def _positions(graha_longitudes: dict[int, float]) -> dict[int, PlanetPosition]:
    """Build positions from bare longitudes.

    Avasthas need nothing but longitude, so the API takes longitudes rather
    than demanding a full nativity. The unused fields are zeroed, not faked.
    """
    return {
        graha: PlanetPosition(
            graha=graha,
            longitude=validate.longitude(f"graha_longitudes[{graha}]", lon),
            latitude=0.0, distance=0.0,
            speed_longitude=0.0, speed_latitude=0.0, speed_distance=0.0,
        )
        for graha, lon in graha_longitudes.items()
    }


def avasthas(
    graha: int,
    graha_longitudes: dict[int, float],
    house: int | None = None,
    aspected_by: list[int] | None = None,
    close_orb: float | None = None,
) -> dict:
    """Every computable state for one graha — §15.4."""
    result = all_avasthas(
        graha, _positions(graha_longitudes), house,
        set(aspected_by) if aspected_by is not None else None, close_orb,
    )
    return {
        "graha": result.graha,
        "graha_name": result.graha_name,
        "age": {
            "name": result.age.name,
            "meaning": result.age.meaning,
            "results": result.age.results,
            "fraction": result.age.fraction,
            "rasi": result.age.rasi,
            "rasi_name": result.age.rasi_name,
            "rasi_is_odd": result.age.rasi_is_odd,
            "degrees_in_rasi": result.age.degrees_in_rasi,
            "band": list(result.age.band),
            "caution": AGE_AVASTHA_CAUTION,
        },
        "alertness": {
            "name": result.alertness.name,
            "meaning": result.alertness.meaning,
            "results": result.alertness.results,
            "when": result.alertness.when,
            "basis": result.alertness.basis,
        },
        "mood": [
            {
                "name": m.name, "meaning": m.meaning, "when": m.when,
                "applies": m.applies, "reason": m.reason, "additional": m.additional,
            }
            for m in result.mood
        ],
        "in_mood": result.in_mood,
        "undetermined": result.undetermined,
    }


def activity(
    graha: int,
    graha_longitude: float,
    moon_longitude: float,
    lagna_rasi: int,
    ghati: int,
    name_sound: int | str | None = None,
) -> dict:
    """§15.4.4 — the sayanaadi avastha, with the formula's working shown.

    The strength of the activity needs the first sound of the native's name,
    so it comes back as null when none is given rather than being guessed.
    """
    result = avastha_by_activity(
        graha, graha_longitude, moon_longitude, lagna_rasi, ghati, name_sound,
    )
    return {
        "graha": result.graha,
        "graha_name": result.graha_name,
        "formula": SAYANAADI_FORMULA,
        "terms": [
            {
                "symbol": term["symbol"],
                "name": term["name"],
                "text": term["text"],
                "value": result.terms[term["symbol"]],
            }
            for term in SAYANAADI_TERMS
        ],
        "index": result.index,
        "name": result.name,
        "meaning": result.meaning,
        "aliases": list(result.aliases),
        "sound_number": result.sound_number,
        "strength": result.strength,
        "strength_results": result.strength_results,
        "strength_remainder": result.strength_remainder,
        "steps": [
            {
                "number": step.number, "name": step.name,
                "description": step.description,
                "value": step.value, "detail": step.detail,
            }
            for step in result.steps
        ],
    }


def activity_results(
    avastha: int,
    graha: int,
    house: int | None = None,
    rasi: int | None = None,
    joined_by: list[int] | None = None,
    moon_phase: str | None = None,
    dignity: str | None = None,
    associated_with_malefics: bool | None = None,
    associated_with_benefics: bool | None = None,
) -> dict:
    """§15.4.4's per-graha results for one sayanaadi avastha.

    Editorial content, licence-gated like every verbatim source: the text is
    withheld unless ``HORA_SERVE_UNCONFIRMED_CONTENT`` is set. The structure —
    which clauses apply and why — is always returned, because that is
    calculation rather than the author's prose.
    """
    from hora.content import get_store
    from hora.content.resolve import Placement, resolve

    index = validate.in_range("avastha", avastha, 1, 12)
    graha_id = validate.in_range("graha", graha, 0, 8)
    entries = get_store().get("avastha", index, qualifier=graha_id)
    if not entries:
        return {
            "avastha": index, "graha": graha_id,
            "available": False,
            "note": (
                "No results are stored for this avastha and graha yet. "
                "Section 15.4.4 lists all 12 x 9; transcription is partial."
            ),
            "results": [],
        }

    entry = entries[0]
    placement = Placement(
        house=house, rasi=rasi,
        joined_by=frozenset(joined_by or ()),
        associated_with_malefics=associated_with_malefics,
        associated_with_benefics=associated_with_benefics,
        moon_phase=moon_phase, dignity=dignity,
    )
    resolved = resolve(entry, placement)
    servable = entry.servable
    return {
        "avastha": index,
        "avastha_name": entry.subject_name,
        "graha": graha_id,
        "graha_name": entry.qualifier_name,
        "available": True,
        "source": entry.source,
        "licence_status": entry.licence_status,
        "text_withheld": not servable,
        "verbatim": entry.verbatim if servable else None,
        "transcription_notes": entry.transcription_notes if servable else None,
        "results": [
            {
                "text": r.text if servable else None,
                "applies": r.applies,
                "conditional": r.conditional,
                "reason": r.reason,
            }
            for r in resolved
        ],
        "applies_count": sum(1 for r in resolved if r.applies),
        "undetermined_count": sum(1 for r in resolved if r.applies is None),
    }


def ghatis(hours_after_sunrise: float) -> dict:
    """``G`` — the ghati running at birth, from hours since sunrise."""
    return {
        "hours_after_sunrise": hours_after_sunrise,
        "ghatis_per_hour": GHATIS_PER_HOUR,
        "ghati": ghati_at_birth(hours_after_sunrise),
        "note": GHATI_NOTE,
    }


def sound(syllable: str) -> dict:
    """Table 37's number for the first sound of a name."""
    return {"syllable": syllable, "sound_number": sound_number(syllable)}


def comparison(left: int, right: int, graha_longitudes: dict[int, float]) -> dict:
    """Which of two grahas is stronger, axis by axis."""
    result = compare(left, right, _positions(graha_longitudes))
    return {
        "left": result.left, "left_name": result.left_name,
        "right": result.right, "right_name": result.right_name,
        "axes": [
            {
                "axis": ax.axis, "winner": ax.winner, "winner_name": ax.winner_name,
                "left": ax.left, "right": ax.right,
                "determined": ax.determined, "reason": ax.reason,
            }
            for ax in result.axes
        ],
        "winner": result.winner, "winner_name": result.winner_name,
        "determined": result.determined, "reason": result.reason,
        "caveat": result.caveat,
    }


def measures() -> dict:
    """The five measures of strength the chapter names, and which we have."""
    return {
        "measures": [dict(m) for m in STRENGTH_MEASURES],
        "caveat": BOOK_CAVEAT,
    }


def rules() -> dict:
    """§15.4's avastha tables as data."""
    return {
        "section": "15.4 Avasthas (States)",
        "age": {
            "table": "Table 35: Avasthas related to age",
            "rows": [
                {
                    "name": r["name"], "meaning": r["meaning"],
                    "results": r["results"], "fraction": r["fraction"],
                    "odd_rasi": list(r["odd"]), "even_rasi": list(r["even"]),
                }
                for r in AGE_AVASTHAS
            ],
            "caution": AGE_AVASTHA_CAUTION,
        },
        "alertness": [dict(r) for r in ALERTNESS_AVASTHAS],
        "mood": [
            {"name": r["name"], "meaning": r["meaning"], "when": r["when"],
             "needs": list(r["needs"]), "additional": False}
            for r in MOOD_AVASTHAS
        ] + [
            {"name": r["name"], "meaning": r["meaning"], "when": r["when"],
             "needs": list(r["needs"]), "additional": True}
            for r in ADDITIONAL_MOOD_AVASTHAS
        ],
        "effects": [dict(e) for e in AVASTHA_EFFECTS],
        "activity": {
            "most_important": ACTIVITY_IS_MOST_IMPORTANT,
            "formula": SAYANAADI_FORMULA,
            "terms": [dict(t) | {"range": list(t["range"])} for t in SAYANAADI_TERMS],
            "states": [
                {"index": index, "name": row["name"], "meaning": row["meaning"],
                 "aliases": list(row.get("aliases", ()))}
                for index, row in sorted(SAYANAADI_AVASTHAS.items())
            ],
            "sound_numbers": [
                {"number": number, "devanagari": list(row["devanagari"]),
                 "roman": row["roman"]}
                for number, row in sorted(SOUND_NUMBERS.items())
            ],
            "strength": [
                {"remainder": remainder, "name": row["name"], "results": row["results"]}
                for remainder, row in sorted(ACTIVITY_STRENGTH.items())
            ],
            "vicheshta_remainder_note": VICHESHTA_REMAINDER_NOTE,
            "navamsa_index_note": NAVAMSA_INDEX_NOTE,
            "ghati_note": GHATI_NOTE,
            "ghatis_per_hour": GHATIS_PER_HOUR,
            "verified": True,
            "verification_note": (
                "Section 15.4.4 is fully checked against the book: Tables 36 "
                "and 37, the formula, the six term definitions, the planetary "
                "adjustments, footnotes 51 and 52, and all 108 per-graha "
                "result lines."
            ),
            "footnotes_verified": True,
        },
    }
