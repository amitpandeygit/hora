"""Chapter 12 — computing an ashtakavarga from the chapter's tables.

The tables are transcribed row-wise, as the book prints them. Everything here
derives from that one copy: the column view, the benefic-house list per
reference, and a chart's own bhinnashtakavarga.

**Naming.** §12.2's footnote 42 warns that the two words are used both ways
round. PVR follows Parasara: **1 is a rekha** (benefic, "sthana") and **0 is a
bindu** (malefic, "karana"). Most modern software says "bindus" for the count
of benefic points, which under this naming is the count of *rekhas*. Every
number this module returns counts 1s, and the field names say `rekhas`.
"""
from __future__ import annotations

from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    ASHTAKAVARGA_REFERENCES,
    ASHTAKAVARGA_TABLE_NUMBERS,
    ASHTAKAVARGA_TABLES,
    ASHTAKAVARGA_TABLES_PENDING,
    GRAHA_NAMES,
    RASI_NAMES,
    SUN_ASHTAKAVARGA_ROWS,
    Graha,
)


class AshtakavargaError(validate.InputError):
    """An ashtakavarga input or table that cannot be resolved."""


#: Reference name to graha id. "Lagna" has none — it is the ascendant.
REFERENCE_GRAHA: dict[str, int | None] = {
    "Sun": int(Graha.SUN), "Moon": int(Graha.MOON), "Mars": int(Graha.MARS),
    "Mercury": int(Graha.MERCURY), "Jupiter": int(Graha.JUPITER),
    "Venus": int(Graha.VENUS), "Saturn": int(Graha.SATURN), "Lagna": None,
}


def verify_tables() -> dict[str, dict]:
    """Shape checks every supplied table must pass, run on demand.

    Ninety-six hand-typed entries per table is exactly where a silent
    transcription error lives, so the checks are part of the product rather
    than only of the test suite: twelve rows of eight, every entry 0 or 1,
    and — for the Sun — the classical total of 48 that his table reaches
    independently of anything we assert about it.
    """
    #: The registry must hold the same object the page was transcribed into,
    #: not a second copy that could drift from it.
    assert ASHTAKAVARGA_TABLES["Sun"] is SUN_ASHTAKAVARGA_ROWS

    out: dict[str, dict] = {}
    for owner, rows in ASHTAKAVARGA_TABLES.items():
        total = sum(sum(row) for row in rows)
        out[owner] = {
            "table": ASHTAKAVARGA_TABLE_NUMBERS[owner],
            "rows": len(rows),
            "columns": sorted({len(row) for row in rows}),
            "values": sorted({v for row in rows for v in row}),
            "total": total,
            "shape_ok": (len(rows) == 12
                         and {len(row) for row in rows} == {8}
                         and {v for row in rows for v in row} <= {0, 1}),
        }
    return out


def available_tables() -> tuple[str, ...]:
    """Which of the eight tables have been supplied."""
    return tuple(o for o in ASHTAKAVARGA_TABLE_NUMBERS if o in ASHTAKAVARGA_TABLES)


def _table(owner: str) -> tuple[tuple[int, ...], ...]:
    if owner not in ASHTAKAVARGA_TABLE_NUMBERS:
        raise AshtakavargaError(
            f"unknown ashtakavarga owner {owner!r}; expected one of "
            f"{', '.join(ASHTAKAVARGA_TABLE_NUMBERS)}")
    table = ASHTAKAVARGA_TABLES.get(owner)
    if table is None:
        raise AshtakavargaError(
            f"Table {ASHTAKAVARGA_TABLE_NUMBERS[owner]} — {owner}'s "
            f"ashtakavarga — has not been supplied. Available: "
            f"{', '.join(available_tables())}")
    return table


def entry(owner: str, reference: str, house: int) -> int:
    """One cell: 1 if the house is benefic for `owner` from `reference`."""
    if reference not in ASHTAKAVARGA_REFERENCES:
        raise AshtakavargaError(
            f"unknown reference {reference!r}; expected one of "
            f"{', '.join(ASHTAKAVARGA_REFERENCES)}")
    validate.in_range("house", int(house), 1, 12)
    column = ASHTAKAVARGA_REFERENCES.index(reference)
    return int(_table(owner)[int(house) - 1][column])


def benefic_houses(owner: str, reference: str) -> tuple[int, ...]:
    """The houses from `reference` in which `owner` is benefically placed.

    This is the column view of the printed table, derived rather than typed a
    second time.
    """
    return tuple(house for house in range(1, 13)
                 if entry(owner, reference, house))


def table_as_rows(owner: str) -> list[dict]:
    """The table in the shape the book prints it, for serving and checking."""
    rows = _table(owner)
    return [
        {"house": house,
         "entries": {ref: int(rows[house - 1][index])
                     for index, ref in enumerate(ASHTAKAVARGA_REFERENCES)}}
        for house in range(1, 13)
    ]


def rekhas_per_reference(owner: str) -> dict[str, int]:
    """How many of the twelve houses each reference makes benefic."""
    return {ref: len(benefic_houses(owner, ref))
            for ref in ASHTAKAVARGA_REFERENCES}


def table_total(owner: str) -> int:
    """The table's own total — 48 for the Sun, which is the classical value."""
    return sum(rekhas_per_reference(owner).values())


@dataclass(frozen=True, slots=True)
class Bhinnashtakavarga:
    """One planet's ashtakavarga over the twelve signs."""

    owner: str
    table: int
    #: Rekhas per sign, indexed 0 = Aries.
    rekhas: tuple[int, ...]
    #: Which references contributed to each sign.
    contributors: tuple[tuple[str, ...], ...]
    total: int


def bhinnashtakavarga(owner: str, reference_signs: dict[str, int]
                      ) -> Bhinnashtakavarga:
    """`owner`'s rekhas in each of the twelve signs.

    :param reference_signs: every name in `ASHTAKAVARGA_REFERENCES` to the
        sign it occupies, 0 = Aries. All eight are required — a missing one
        would silently cost the chart up to twelve rekhas.
    """
    missing = [r for r in ASHTAKAVARGA_REFERENCES if r not in reference_signs]
    if missing:
        raise AshtakavargaError(
            f"every one of the eight reference points is needed; "
            f"{', '.join(missing)} "
            f"{'is' if len(missing) == 1 else 'are'} missing")
    for name, sign in reference_signs.items():
        if name not in ASHTAKAVARGA_REFERENCES:
            raise AshtakavargaError(f"unknown reference {name!r}")
        validate.in_range(f"{name} sign", int(sign), 0, 11)

    counts = [0] * 12
    who: list[list[str]] = [[] for _ in range(12)]
    for reference in ASHTAKAVARGA_REFERENCES:
        base = int(reference_signs[reference])
        for house in benefic_houses(owner, reference):
            sign = (base + house - 1) % 12
            counts[sign] += 1
            who[sign].append(reference)
    return Bhinnashtakavarga(
        owner=owner,
        table=ASHTAKAVARGA_TABLE_NUMBERS[owner],
        rekhas=tuple(counts),
        contributors=tuple(tuple(names) for names in who),
        total=sum(counts),
    )


def sarvashtakavarga(reference_signs: dict[str, int]) -> dict:
    """The eight bhinnashtakavargas summed, sign by sign.

    Returns what can be computed and names what cannot: until Tables 20 to 26
    are supplied this is a partial sum, and it says so rather than passing a
    seven-table total off as a sarvashtakavarga.
    """
    available = available_tables()
    per_owner = {owner: bhinnashtakavarga(owner, reference_signs)
                 for owner in available}
    totals = [sum(b.rekhas[sign] for b in per_owner.values())
              for sign in range(12)]
    complete = not ASHTAKAVARGA_TABLES_PENDING
    return {
        "complete": complete,
        "owners_included": list(available),
        "owners_missing": list(ASHTAKAVARGA_TABLES_PENDING),
        "missing_note": (
            "" if complete else
            "This is not a sarvashtakavarga. Tables "
            + ", ".join(str(ASHTAKAVARGA_TABLE_NUMBERS[o])
                        for o in ASHTAKAVARGA_TABLES_PENDING)
            + " have not been supplied, so "
            + ", ".join(ASHTAKAVARGA_TABLES_PENDING)
            + " contribute nothing to these totals. A sign's figure is a "
              "partial sum and must not be compared against the usual "
              "sarvashtakavarga thresholds."
        ),
        "rekhas": totals,
        "signs": [
            {"sign": sign, "sign_name": str(RASI_NAMES[sign]),
             "rekhas": totals[sign]}
            for sign in range(12)
        ],
        "total": sum(totals),
    }


def graha_of(reference: str) -> int | None:
    return REFERENCE_GRAHA[reference]


def reference_name(graha: int) -> str | None:
    for name, value in REFERENCE_GRAHA.items():
        if value == int(graha):
            return name
    return None


def describe(owner: str) -> dict:
    """Everything about one table, for the reference endpoint."""
    graha = REFERENCE_GRAHA[owner]
    return {
        "owner": owner,
        "owner_graha": graha,
        "owner_graha_name": None if graha is None else str(GRAHA_NAMES[graha]),
        "table": ASHTAKAVARGA_TABLE_NUMBERS[owner],
        "references": list(ASHTAKAVARGA_REFERENCES),
        "rows": table_as_rows(owner),
        "benefic_houses": {ref: list(benefic_houses(owner, ref))
                           for ref in ASHTAKAVARGA_REFERENCES},
        "rekhas_per_reference": rekhas_per_reference(owner),
        "total": table_total(owner),
    }
