"""Karaka service — chapter 8.

Three kinds of karaka, and the chapter's central warning is that they are not
interchangeable: "One should not use the three types of karakas in a mixed-up
way." The API mirrors that — each kind has its own endpoint and its own
response shape, and none of them silently stands in for another.

Only chara karakas need computing. The other two are tables.
"""
from __future__ import annotations

from hora.charts.karaka import (
    KarakaError,
    chara_karakas,
    naisargika_karaka,
    sthira_karaka_of_spouse,
)
from hora.core import validate
from hora.core.const import (
    CHARA_KARAKA_ADVANCEMENT_LABELS,
    CHARA_KARAKA_ALIASES,
    CHARA_KARAKA_NAME_ALIASES,
    CHARA_KARAKA_NOTES,
    CHARA_KARAKA_PROCEDURE,
    CHARA_KARAKA_TIE_BREAK,
    CHARA_KARAKAS,
    CHOOSING_A_KARAKA,
    GRAHA_NAMES,
    JNAATI_PRONUNCIATION_NOTE,
    KARAKA_DEFINITION,
    KARAKA_KINDS,
    KARAKA_MEANING,
    KARAKA_PRONUNCIATION,
    KARAKA_USAGE_RULES,
    KARAKA_WARNING,
    MEASURED_FROM_END_OF_RASI,
    NAISARGIKA_DEFINITION,
    NAISARGIKA_KARAKA,
    NAISARGIKA_KARAKATWAS,
    NAISARGIKA_TABLE_16_RULE,
    NAISARGIKA_USED_IN,
    NAISARGIKA_WORKED_EXAMPLES,
    RASI_NAMES,
    SHARED_KARAKATWA_NOTE,
    STHIRA_KARAKA_OF_SPOUSE_NOTE,
    STHIRA_KARAKAS,
    STRENGTH_COMPARISON_CHAPTER,
    TABLE_16_SOURCE_NOTE,
)

InputError = validate.InputError

__all__ = [
    "InputError", "KarakaError", "chara", "kinds", "naisargika", "sthira",
]


def _degrees(value: float) -> dict:
    """Split a degree value into degrees, minutes and seconds.

    Chapter 8's tie rule is stated in exactly these units, so the response
    carries them rather than making a caller re-derive them from a float.
    """
    total_seconds = round(value * 3600)
    degrees, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return {
        "decimal": value,
        "degrees": degrees,
        "minutes": minutes,
        "seconds": seconds,
        "formatted": f"{degrees}°{minutes:02d}'{seconds:02d}\"",
    }


def chara(longitudes: dict[int, float]) -> dict:
    """Assign the eight chara karakas from sidereal longitudes.

    :param longitudes: graha id -> sidereal longitude, exactly the eight
        grahas of 8.2 (the seven classical plus Rahu).
    :raises KarakaError: on a missing, extra or non-finite entry.
    """
    karakas = chara_karakas(longitudes)
    return {
        "kind": "chara",
        "presiding": KARAKA_KINDS["chara"]["presiding"],
        "used_for": KARAKA_KINDS["chara"]["used_for"],
        "read_as": KARAKA_KINDS["chara"]["read_as"],
        "read_as_note": KARAKA_KINDS["chara"]["read_as_note"],
        "shared_karakatwa_note": SHARED_KARAKATWA_NOTE,
        "karakas": [
            {
                "order": k.order,
                "symbol": k.symbol,
                "symbol_aliases": CHARA_KARAKA_ALIASES.get(k.symbol, []),
                "name": k.name,
                "name_aliases": CHARA_KARAKA_NAME_ALIASES.get(k.name, []),
                "shows": k.shows,
                "note": CHARA_KARAKA_NOTES.get(k.symbol),
                "graha": k.graha,
                "graha_name": k.graha_name,
                "rasi": int(longitudes[k.graha] % 360.0 // 30),
                "rasi_name": RASI_NAMES[int(longitudes[k.graha] % 360.0 // 30)],
                "advancement": _degrees(k.advancement),
                "measured_from_end_of_rasi": k.graha in MEASURED_FROM_END_OF_RASI,
                "shares_karakatwa": k.shared,
            }
            for k in karakas
        ],
    }


def sthira() -> dict:
    """§8.3's fixed significators, as printed.

    Father and mother are pairs, not single grahas: the stronger of the two
    holds the karakatwa. That is returned as a pair with ``rule: "stronger"``
    rather than resolved, because resolving it needs a strength comparison
    that chapter 8 explicitly defers to a later chapter.
    """
    return {
        "kind": "sthira",
        "presiding": KARAKA_KINDS["sthira"]["presiding"],
        "used_for": KARAKA_KINDS["sthira"]["used_for"],
        "name_explained": KARAKA_KINDS["sthira"]["name_explained"],
        "read_as": KARAKA_KINDS["sthira"]["read_as"],
        "read_as_note": KARAKA_KINDS["sthira"]["read_as_note"],
        # Footnote 26 sends the "stronger of the two" comparison to a later
        # chapter, so father and mother cannot be resolved from chapter 8.
        "strength_comparison_defined_in": STRENGTH_COMPARISON_CHAPTER,
        "karakas": [
            {
                "relative": entry["relative"],
                "grahas": [int(g) for g in entry["grahas"]],
                "graha_names": [GRAHA_NAMES[g] for g in entry["grahas"]],
                "rule": entry["rule"],
                "note": entry["note"],
            }
            for entry in STHIRA_KARAKAS
        ],
        "spouse": {
            "female": {
                "graha": sthira_karaka_of_spouse("female")["graha"],
                "graha_name": sthira_karaka_of_spouse("female")["graha_name"],
            },
            "male": {
                "graha": sthira_karaka_of_spouse("male")["graha"],
                "graha_name": sthira_karaka_of_spouse("male")["graha_name"],
            },
            "note": STHIRA_KARAKA_OF_SPOUSE_NOTE,
        },
    }


def naisargika() -> dict:
    """Tables 15 and 16 — the natural significators.

    §8.4 reads Table 15 as "the Nth house *from* the karaka", not the Nth
    house of the chart: "the 4th house from Moon shows mother". The response
    says so in ``counted_from_the_graha`` so the distinction cannot be lost.
    """
    return {
        "kind": "naisargika",
        "presiding": KARAKA_KINDS["naisargika"]["presiding"],
        "used_for": KARAKA_KINDS["naisargika"]["used_for"],
        "counted_from_the_graha": True,
        "read_as": KARAKA_KINDS["naisargika"]["read_as"],
        "read_as_note": KARAKA_KINDS["naisargika"]["read_as_note"],
        "primary": [naisargika_karaka(house) for house in sorted(NAISARGIKA_KARAKA)],
        "by_graha": [
            {
                "graha": int(graha),
                "graha_name": GRAHA_NAMES[graha],
                "significations": [
                    {"house": house, "matters": matters}
                    for house, matters in entries
                ],
            }
            for graha, entries in NAISARGIKA_KARAKATWAS.items()
        ],
        "definition": NAISARGIKA_DEFINITION,
        "used_in": NAISARGIKA_USED_IN,
        # Table 16 is compiled from the classics, Table 15 is the chapter's
        # own. A caller weighing sources needs to know which is which.
        "table_16_source": TABLE_16_SOURCE_NOTE,
        "table_16_rule": NAISARGIKA_TABLE_16_RULE,
        "worked_examples": [
            {"house": e["house"], "graha": int(e["graha"]),
             "graha_name": GRAHA_NAMES[e["graha"]], "shows": e["shows"],
             "table": e["table"]}
            for e in NAISARGIKA_WORKED_EXAMPLES
        ],
    }


def kinds() -> dict:
    """All three kinds side by side, with what each is and is not for.

    Exists because 8.1's warning against mixing them is the most consequential
    sentence in the chapter, and an API that only exposed the three tables
    separately would never say it.
    """
    return {
        "word": "karaka",
        "meaning": KARAKA_MEANING,
        "pronounced": KARAKA_PRONUNCIATION,
        "definition": KARAKA_DEFINITION,
        "warning": KARAKA_WARNING,
        "kinds": [
            {
                "key": key,
                "name": entry["name"],
                "gloss": entry["gloss"],
                "count": entry["count"],
                "presiding": entry["presiding"],
                "grahas": [int(g) for g in entry["grahas"]],
                "graha_names": [GRAHA_NAMES[g] for g in entry["grahas"]],
                "shows": entry["shows"],
                # 8.1 states each kind's scope twice — once broadly and once
                # narrowed. Both are published: the broad form is what
                # distinguishes the kinds from each other, and dropping it
                # leaves the warning against mixing them unillustrated.
                "shows_broadly": entry.get("shows_broadly"),
                "shows_contrast": entry.get("shows_contrast"),
                "not_limited_to": entry.get("not_limited_to"),
                "presiding_because": entry["presiding_because"],
                "used_for": entry["used_for"],
                # 8.3's distinction: naisargika karakas are read as a house
                # counted from the karaka, the other two as the karaka itself.
                "read_as": entry["read_as"],
                "read_as_note": entry["read_as_note"],
                "examples": list(entry.get("examples", ())),
                "also_shows": entry.get("also_shows"),
                "excludes": [
                    {"graha": g, "graha_name": GRAHA_NAMES[g], "reason": reason}
                    for g, reason in entry.get("excludes", {}).items()
                ],
            }
            for key, entry in KARAKA_KINDS.items()
        ],
        "jnaati_pronunciation": JNAATI_PRONUNCIATION_NOTE,
        "usage_rules": [dict(rule) for rule in KARAKA_USAGE_RULES],
        "choosing": [dict(entry) for entry in CHOOSING_A_KARAKA],
        "chara_table": [
            {
                "order": index + 1,
                "symbol": row["symbol"],
                "symbol_aliases": CHARA_KARAKA_ALIASES.get(row["symbol"], []),
                "name": row["name"],
                "shows": row["shows"],
                "note": CHARA_KARAKA_NOTES.get(row["symbol"]),
                # Table 13 labels only the two extreme rows, and the label is
                # on the advancement rather than on the karaka.
                "advancement": CHARA_KARAKA_ADVANCEMENT_LABELS.get(row["symbol"]),
            }
            for index, row in enumerate(CHARA_KARAKAS)
        ],
        # 8.2's procedure, so a caller can read the rule the engine applies
        # rather than inferring it from the output.
        "chara_procedure": list(CHARA_KARAKA_PROCEDURE),
        "chara_tie_break": CHARA_KARAKA_TIE_BREAK,
        "shared_karakatwa": SHARED_KARAKATWA_NOTE,
        "measured_from_end_of_rasi": [
            {"graha": int(g), "graha_name": GRAHA_NAMES[g]}
            for g in sorted(MEASURED_FROM_END_OF_RASI)
        ],
    }
