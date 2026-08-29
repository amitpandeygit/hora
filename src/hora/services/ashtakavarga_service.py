"""Chapter 12 — ashtakavarga, as the API sees it."""
from __future__ import annotations

from hora.charts.ashtakavarga import (
    AshtakavargaError,
    available_tables,
    benefic_houses,
    benefic_rasis_from_chart,
    bhinnashtakavarga,
    describe,
    summed,
    verify_tables,
)
from hora.core import validate
from hora.core.const import (
    ASHTAKAVARGA_ALL_PLANETS_ARE_REFERENCES,
    ASHTAKAVARGA_BENEFIC_SANSKRIT,
    ASHTAKAVARGA_BENEFIC_TERM,
    ASHTAKAVARGA_INTRO,
    ASHTAKAVARGA_MALEFIC_SANSKRIT,
    ASHTAKAVARGA_MALEFIC_TERM,
    ASHTAKAVARGA_MEANS,
    ASHTAKAVARGA_NOTATION,
    ASHTAKAVARGA_PURPOSE,
    ASHTAKAVARGA_REFERENCE_POINT_NOTE,
    ASHTAKAVARGA_REFERENCES,
    ASHTAKAVARGA_TABLE_NUMBERS,
    ASHTAKAVARGA_TABLES_PENDING,
    BINDU_REKHA_FOOTNOTE,
    CLASSICAL_TABLE_TOTALS_PROVENANCE,
    EXAMPLE_37,
    EXAMPLE_37_HOUSES,
    EXAMPLE_37_RASIS,
    EXAMPLE_37_WORKING,
    EXERCISE_18,
    EXERCISE_18_ANSWER,
    EXERCISE_18_HINT,
    RASI_NAMES,
    TABLE_19_WORKED_READING,
    TABLES_20_TO_26_NOTE,
    YUGA_FOOTNOTE,
    YUGA_YEARS,
)

InputError = validate.InputError


def rules() -> dict:
    """Chapter 12's framing, its notation, and which tables exist."""
    return {
        "intro": ASHTAKAVARGA_INTRO,
        "means": ASHTAKAVARGA_MEANS,
        "reference_point_note": ASHTAKAVARGA_REFERENCE_POINT_NOTE,
        "all_planets_are_references": ASHTAKAVARGA_ALL_PLANETS_ARE_REFERENCES,
        "purpose": ASHTAKAVARGA_PURPOSE,
        "references": list(ASHTAKAVARGA_REFERENCES),
        "table_numbers": dict(ASHTAKAVARGA_TABLE_NUMBERS),
        "tables_available": list(available_tables()),
        "tables_verified": verify_tables(),
        "classical_totals_provenance": CLASSICAL_TABLE_TOTALS_PROVENANCE,
        "tables_verified_note": (
            "Ninety-six hand-typed entries per table is where a silent "
            "transcription error would live, so the shape checks ship with "
            "the product. The Sun's table reaching a total of 48 — the "
            "classical figure — is an independent check on all ninety-six."
        ),
        "tables_pending": list(ASHTAKAVARGA_TABLES_PENDING),
        "tables_pending_note": TABLES_20_TO_26_NOTE,
        "notation": ASHTAKAVARGA_NOTATION,
        "benefic_entry": {
            "value": 1, "term": ASHTAKAVARGA_BENEFIC_TERM,
            "sanskrit": ASHTAKAVARGA_BENEFIC_SANSKRIT,
        },
        "malefic_entry": {
            "value": 0, "term": ASHTAKAVARGA_MALEFIC_TERM,
            "sanskrit": ASHTAKAVARGA_MALEFIC_SANSKRIT,
        },
        "bindu_rekha_footnote": BINDU_REKHA_FOOTNOTE,
        "naming_warning": (
            "PVR follows Parasara: 1 is a **rekha** and 0 is a **bindu**. "
            "Most modern software and most south Indian practice use the two "
            "words the other way round, so a figure labelled “bindus in a "
            "sign” elsewhere is what this API calls rekhas. Every count "
            "returned here counts 1s, and the fields are named `rekhas` so "
            "the two can never be confused."
        ),
        "worked_reading": TABLE_19_WORKED_READING,
        "example_37": {
            "question": EXAMPLE_37,
            "working": EXAMPLE_37_WORKING,
            "owner": "Jupiter", "reference": "Venus", "reference_sign": "Ge",
            "houses": list(EXAMPLE_37_HOUSES),
            "rasis": list(EXAMPLE_37_RASIS),
        },
        "exercise_18": {
            "question": EXERCISE_18,
            "hint": EXERCISE_18_HINT,
            "owner": "Mercury", "chart": "Chart 6",
            "answer": {ref: list(rasis)
                       for ref, rasis in EXERCISE_18_ANSWER.items()},
        },
        "yuga_footnote": YUGA_FOOTNOTE,
        "yugas": [{"name": name, "years": years} for name, years in YUGA_YEARS],
    }


def table(owner: str) -> dict:
    """One of the eight tables, in the shape the book prints it."""
    return describe(str(owner))


def benefic_rasis(owner: str, reference_signs: dict[str, int]) -> dict:
    """Where one planet is benefic, reference by reference — §12.2's Example
    37 and Exercise 18.

    "So ashtakavarga is essentially a system that tells us the benefic
    positions of lagna and seven planets with respect to each other." This is
    that sentence as an endpoint.
    """
    signs = {str(k): int(v) for k, v in reference_signs.items()}
    per_reference = benefic_rasis_from_chart(str(owner), signs)
    return {
        "owner": str(owner),
        "table": ASHTAKAVARGA_TABLE_NUMBERS[str(owner)],
        "reference_signs": {k: {"sign": v, "sign_name": str(RASI_NAMES[v])}
                            for k, v in signs.items()},
        "benefic_rasis": [
            {
                "reference": reference,
                "reference_sign": signs[reference],
                "reference_sign_name": str(RASI_NAMES[signs[reference]]),
                "houses": list(benefic_houses(str(owner), reference)),
                "rasis": list(rasis),
                "rasi_names": [str(RASI_NAMES[s]) for s in rasis],
            }
            for reference, rasis in per_reference.items()
        ],
    }


def chart(reference_signs: dict[str, int], owner: str | None = None) -> dict:
    """A chart's ashtakavarga.

    :param reference_signs: all eight reference points to their signs.
    :param owner: one table, or omit for every table that exists.
    """
    signs = {str(k): int(v) for k, v in reference_signs.items()}
    owners = [str(owner)] if owner else list(available_tables())
    per_owner = [
        {
            "owner": name,
            "table": ASHTAKAVARGA_TABLE_NUMBERS[name],
            "rekhas": list(result.rekhas),
            "total": result.total,
            "signs": [
                {"sign": sign, "sign_name": str(RASI_NAMES[sign]),
                 "rekhas": result.rekhas[sign],
                 "from": list(result.contributors[sign])}
                for sign in range(12)
            ],
        }
        for name, result in ((n, bhinnashtakavarga(n, signs)) for n in owners)
    ]
    return {
        "reference_signs": {k: {"sign": v, "sign_name": str(RASI_NAMES[v])}
                            for k, v in signs.items()},
        "bhinnashtakavarga": per_owner,
        "summed": summed(signs),
        "tables_pending": list(ASHTAKAVARGA_TABLES_PENDING),
    }


__all__ = ["AshtakavargaError", "InputError", "benefic_rasis", "chart",
           "rules", "table"]
