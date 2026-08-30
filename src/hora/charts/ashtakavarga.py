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

from collections.abc import Sequence
from dataclasses import dataclass

from hora.core import validate
from hora.core.const import (
    ASHTAKAVARGA_REFERENCES,
    ASHTAKAVARGA_TABLE_NUMBERS,
    ASHTAKAVARGA_TABLES,
    ASHTAKAVARGA_TABLES_PENDING,
    BAV_COUNT_RANGE,
    BAV_GRADES,
    CLASSICAL_TABLE_TOTALS,
    GRAHA_NAMES,
    JUPITER_ASHTAKAVARGA_ROWS,
    LAGNA_ASHTAKAVARGA_ROWS,
    MARS_ASHTAKAVARGA_ROWS,
    MERCURY_ASHTAKAVARGA_ROWS,
    MOON_ASHTAKAVARGA_ROWS,
    MUHURTA_DEFINITION,
    MUHURTA_FOOTNOTE,
    RASI_NAMES,
    SATURN_ASHTAKAVARGA_ROWS,
    SAV_AVERAGE_FROM,
    SAV_MUHURTA_POSITIONS,
    SAV_MUHURTA_RULE,
    SAV_OWNERS,
    SAV_STRONG_FROM,
    SAV_TOTAL,
    SUN_ASHTAKAVARGA_ROWS,
    VENUS_ASHTAKAVARGA_ROWS,
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
    and the total the wider tradition records for that planet, which each
    table reaches independently of anything we assert about it.

    `CLASSICAL_TABLE_TOTALS` is a check, not a source — the book prints no
    totals. A mismatch is reported here, never corrected.
    """
    #: The registry must hold the same objects the pages were transcribed
    #: into, not second copies that could drift from them.
    assert ASHTAKAVARGA_TABLES["Sun"] is SUN_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Moon"] is MOON_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Mars"] is MARS_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Mercury"] is MERCURY_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Jupiter"] is JUPITER_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Venus"] is VENUS_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Saturn"] is SATURN_ASHTAKAVARGA_ROWS
    assert ASHTAKAVARGA_TABLES["Lagna"] is LAGNA_ASHTAKAVARGA_ROWS

    out: dict[str, dict] = {}
    for owner, rows in ASHTAKAVARGA_TABLES.items():
        total = sum(sum(row) for row in rows)
        classical = CLASSICAL_TABLE_TOTALS[owner]
        out[owner] = {
            "table": ASHTAKAVARGA_TABLE_NUMBERS[owner],
            "rows": len(rows),
            "columns": sorted({len(row) for row in rows}),
            "values": sorted({v for row in rows for v in row}),
            "total": total,
            "classical_total": classical,
            "matches_classical_total": total == classical,
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


def signs_in_chart(reference_longitudes: dict[str, float],
                   chart: str = "D1") -> dict[str, int]:
    """The eight reference points' signs in any divisional chart.

    §12.5: "Ashtakavarga of divisional charts is prepared in the same manner
    as that of rasi chart. The benefic houses for each planet with respect to
    the 8 references are the same." So nothing about the tables changes — only
    which signs the eight references occupy.

    :param reference_longitudes: all eight names to sidereal longitudes.
    :param chart: a varga code, "D1" for the rasi chart.
    """
    from hora.charts.vargas import varga

    missing = [r for r in ASHTAKAVARGA_REFERENCES
               if r not in reference_longitudes]
    if missing:
        raise AshtakavargaError(
            f"every one of the eight reference points is needed; "
            f"{', '.join(missing)} "
            f"{'is' if len(missing) == 1 else 'are'} missing")
    code = str(chart).upper()
    try:
        return {name: varga(float(reference_longitudes[name]), code).sign
                for name in ASHTAKAVARGA_REFERENCES}
    except ValueError as exc:
        raise AshtakavargaError(str(exc)) from exc


def benefic_rasis(owner: str, reference: str, reference_sign: int
                  ) -> tuple[int, ...]:
    """The **rasis** in which `owner` is benefic with respect to `reference`.

    §12.2's Example 37 in one call: take the reference's benefic houses from
    the owner's table, count them from the sign the reference occupies, and
    report the signs they land in.
    """
    validate.in_range("reference_sign", int(reference_sign), 0, 11)
    base = int(reference_sign)
    return tuple(sorted((base + house - 1) % 12
                        for house in benefic_houses(owner, reference)))


def benefic_rasis_from_chart(owner: str, reference_signs: dict[str, int]
                             ) -> dict[str, tuple[int, ...]]:
    """Exercise 18 in one call: every reference at once, for one owner."""
    missing = [r for r in ASHTAKAVARGA_REFERENCES if r not in reference_signs]
    if missing:
        raise AshtakavargaError(
            f"every one of the eight reference points is needed; "
            f"{', '.join(missing)} "
            f"{'is' if len(missing) == 1 else 'are'} missing")
    return {reference: benefic_rasis(owner, reference,
                                     int(reference_signs[reference]))
            for reference in ASHTAKAVARGA_REFERENCES}


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


def grade(rekhas: int) -> str:
    """§12.3's reading of a count: 5-8 favorable, 4 neutral, 3-0 unfavorable.

    "If a planet is in a sign with a count of 5, 6, 7 or 8 ... the planet is
    favorable ... If the count is 4, the planet is neutral."

    The book's own spelling of "favorable" is kept.
    """
    validate.in_range("rekhas", int(rekhas), *BAV_COUNT_RANGE)
    return BAV_GRADES[int(rekhas)]


@dataclass(frozen=True, slots=True)
class Bhinnashtakavarga:
    """One planet's BAV over the twelve signs.

    "When preparing the BAV of a planet, we count the number of references
    from which the planet is benefic in each rasi and put that count in that
    rasi."
    """

    owner: str
    table: int
    #: Rekhas per sign, indexed 0 = Aries. §12.3 calls this count the rekhas.
    rekhas: tuple[int, ...]
    #: Which references contributed to each sign.
    contributors: tuple[tuple[str, ...], ...]
    total: int

    @property
    def grades(self) -> tuple[str, ...]:
        """§12.3's grade per sign — usable for a transit as well as a natal
        placement, which is what the section says at the end."""
        return tuple(grade(count) for count in self.rekhas)


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


def natal_grade(owner: str, reference_signs: dict[str, int]) -> dict:
    """§12.3 applied to where the planet actually sits.

    The grade is defined for every sign — that is what makes it usable for
    transits, which §12.3 says at the end — but the natal reading is the
    grade of the sign the planet occupies. Lagna has no such reading of its
    own: it is a reference point, not a body that sits anywhere else.
    """
    result = bhinnashtakavarga(owner, reference_signs)
    if owner == "Lagna":
        return {
            "owner": owner,
            "applicable": False,
            "reason": ("lagna is a reference point, not a planet that "
                       "occupies a sign of its own, so section 12.3's natal "
                       "reading does not apply to its BAV"),
        }
    sign = int(reference_signs[owner])
    return {
        "owner": owner,
        "applicable": True,
        "sign": sign,
        "sign_name": str(RASI_NAMES[sign]),
        "rekhas": result.rekhas[sign],
        "grade": grade(result.rekhas[sign]),
    }


def sav_grade(rekhas: int) -> str:
    """§12.4's reading of an SAV count.

    "A rasi with 30 or more rekhas becomes strong ... A rasi with 25-30
    rekhas is average. A rasi with less than 25 rekhas becomes weak."

    The printed ranges overlap at 30. It is read as **strong**: that clause
    is unambiguous and stated first, and the muhurta rule repeats "30 or more
    ... are favorable". See docs/book-deviations.md D-40.
    """
    count = int(rekhas)
    if count >= SAV_STRONG_FROM:
        return "strong"
    if count >= SAV_AVERAGE_FROM:
        return "average"
    return "weak"


def sarvashtakavarga(reference_signs: dict[str, int]) -> dict:
    """§12.4's SAV: the seven planets' BAVs added sign by sign.

    "Samudaaya Ashtakavarga is nothing but the sum of the ashtakavargas of
    seven planets." Lagna's table is **not** among them — which is what
    OI-100 was open about until this section settled it.
    """
    missing = [o for o in SAV_OWNERS if o not in ASHTAKAVARGA_TABLES]
    if missing:
        raise AshtakavargaError(
            f"the SAV needs all seven planetary tables; "
            f"{', '.join(missing)} "
            f"{'is' if len(missing) == 1 else 'are'} not supplied")
    per_owner = {owner: bhinnashtakavarga(owner, reference_signs)
                 for owner in SAV_OWNERS}
    totals = [sum(per_owner[o].rekhas[sign] for o in SAV_OWNERS)
              for sign in range(12)]
    return {
        "owners": list(SAV_OWNERS),
        "excludes": ["Lagna"],
        "excludes_note": (
            "Section 12.4 defines the SAV as the sum of seven planets' "
            "ashtakavargas. Lagna has a table of its own — Table 26 — but it "
            "is not part of the SAV."
        ),
        "rekhas": totals,
        "total": sum(totals),
        "expected_total": SAV_TOTAL,
        "signs": [
            {"sign": sign, "sign_name": str(RASI_NAMES[sign]),
             "rekhas": totals[sign], "grade": sav_grade(totals[sign])}
            for sign in range(12)
        ],
    }


def summed(reference_signs: dict[str, int]) -> dict:
    """Both candidate sums, kept for the record.

    §12.4 settled which one is the SAV — the seven planets — so
    `sarvashtakavarga` is the function to use. This one still reports the
    eight-reference sum beside it, because the difference is exactly lagna's
    own table and a caller comparing against other software may need to see
    both.
    """
    available = available_tables()
    per_owner = {owner: bhinnashtakavarga(owner, reference_signs)
                 for owner in available}
    planets = [o for o in available if o != "Lagna"]

    def totals(owners: list[str]) -> list[int]:
        return [sum(per_owner[o].rekhas[sign] for o in owners)
                for sign in range(12)]

    planet_totals = totals(planets)
    all_totals = totals(list(available))
    return {
        "complete": not ASHTAKAVARGA_TABLES_PENDING,
        "owners_included": list(available),
        "owners_missing": list(ASHTAKAVARGA_TABLES_PENDING),
        "seven_planets": {
            "owners": planets,
            "complete": not [o for o in ASHTAKAVARGA_TABLES_PENDING
                             if o != "Lagna"],
            "rekhas": planet_totals,
            "total": sum(planet_totals),
            "classical_total_when_complete": SAV_TOTAL,
            "is_the_sav": True,
        },
        "eight_references": {
            "owners": list(available),
            "complete": not ASHTAKAVARGA_TABLES_PENDING,
            "rekhas": all_totals,
            "total": sum(all_totals),
            "classical_total_when_complete": 386,
            "is_the_sav": False,
        },
        "settled_note": (
            "Section 12.4 settles this: the SAV is the seven-planet sum. The "
            "eight-reference figure is reported beside it only because the "
            "difference is exactly lagna's own table, Table 26."
        ),
        "missing_note": (
            "" if not ASHTAKAVARGA_TABLES_PENDING else
            "Tables "
            + ", ".join(str(ASHTAKAVARGA_TABLE_NUMBERS[o])
                        for o in ASHTAKAVARGA_TABLES_PENDING)
            + " have not been supplied, so these are partial sums."
        ),
        "signs": [
            {"sign": sign, "sign_name": str(RASI_NAMES[sign]),
             "seven_planets": planet_totals[sign],
             "eight_references": all_totals[sign]}
            for sign in range(12)
        ],
    }


def muhurta_strength(natal_reference_signs: dict[str, int],
                     muhurta_signs: dict[str, int]) -> dict:
    """§12.4's muhurta rule.

    "One should look at the strengths, as per SAV of the natal chart, of the
    rasis containing lagna, Moon and Sun in the muhurta chart. Rasis
    containing 30 or more rekhas in SAV are favorable."

    The SAV is the **natal** chart's; the signs looked up in it are the
    muhurta chart's.
    """
    sav = sarvashtakavarga(natal_reference_signs)
    missing = [p for p in SAV_MUHURTA_POSITIONS if p not in muhurta_signs]
    if missing:
        raise AshtakavargaError(
            f"the muhurta chart's {', '.join(missing)} "
            f"{'is' if len(missing) == 1 else 'are'} needed; section 12.4 "
            f"reads lagna, Moon and Sun")
    rows = []
    for position in SAV_MUHURTA_POSITIONS:
        sign = int(muhurta_signs[position])
        validate.in_range(f"muhurta {position}", sign, 0, 11)
        rekhas = sav["rekhas"][sign]
        rows.append({
            "position": position,
            "sign": sign,
            "sign_name": str(RASI_NAMES[sign]),
            "natal_sav_rekhas": rekhas,
            "grade": sav_grade(rekhas),
            "favorable": rekhas >= SAV_STRONG_FROM,
        })
    return {
        "rule": SAV_MUHURTA_RULE,
        "favorable_from": SAV_STRONG_FROM,
        "positions": rows,
        "all_favorable": all(row["favorable"] for row in rows),
        "natal_sav": sav["rekhas"],
        "footnote": MUHURTA_FOOTNOTE,
        "muhurta_definition": MUHURTA_DEFINITION,
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
    # Validate before indexing: an unknown owner must reach the caller as a
    # stated error, not as a KeyError from a dict lookup.
    rows = _table(owner)
    graha = REFERENCE_GRAHA[owner]
    assert rows
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


# --------------------------------------------------------------------------
# §12.6 — Prastaara Ashtakavarga
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Prastaara:
    """One planet's PAV — §12.6's "spread-out" ashtakavarga.

    `bhinnashtakavarga` already walks every (reference, house) pair; a BAV
    throws the pairing away and keeps only the count. A PAV keeps it. So this
    is not a second calculation, it is the same one stopped a step earlier,
    and `rekhas` here is `Bhinnashtakavarga.rekhas` by construction.
    """

    #: The planet whose PAV this is.
    owner: str
    #: Which table it came from.
    table: int
    #: Reference name to twelve 0/1 entries, Aries first — Table 27's rows.
    rows: dict[str, tuple[int, ...]]
    #: Table 27's last row: the column sums, which are the BAV's rekhas.
    rekhas: tuple[int, ...]
    #: Sign index to the references the owner is benefic from there. The same
    #: information read down a column instead of across a row.
    benefic_from: tuple[tuple[str, ...], ...]


def prastaara(owner: str, reference_signs: dict[str, int]) -> Prastaara:
    """`owner`'s PAV — which references it is benefic from, in each rasi.

    :param reference_signs: every name in `ASHTAKAVARGA_REFERENCES` to the
        sign it occupies, 0 = Aries. All eight are required, as for a BAV.
    """
    bav = bhinnashtakavarga(owner, reference_signs)
    rows = {
        reference: tuple(
            1 if reference in bav.contributors[sign] else 0
            for sign in range(12)
        )
        for reference in ASHTAKAVARGA_REFERENCES
    }
    return Prastaara(
        owner=bav.owner,
        table=bav.table,
        rows=rows,
        rekhas=bav.rekhas,
        benefic_from=bav.contributors,
    )


def benefic_from_in(owner: str, reference_signs: dict[str, int],
                    rasi: int) -> tuple[str, ...]:
    """Exactly which references `owner` is benefic from in one rasi.

    §12.6's stated purpose in one call: "we need to know exactly which
    references a planet is benefic from".
    """
    validate.in_range("rasi", rasi, 0, 11)
    return prastaara(owner, reference_signs).benefic_from[rasi]


def is_benefic_from(owner: str, reference_signs: dict[str, int], rasi: int,
                    references: Sequence[str]) -> dict:
    """§12.6's transit question: benefic in this rasi from *these* references?

    The book's example is Jupiter's transit for marriage, wanted benefic from
    Venus or the DK or the 7th lord in navamsa. Only the first is an
    ashtakavarga reference — the other two are ways of choosing which graha to
    ask about, and the caller resolves them to a name before calling here.

    :param references: the references the caller cares about, in any order.
    :returns: a verdict for each one, never a bare absence, plus whether all
        of them hold.
    """
    if not references:
        raise AshtakavargaError(
            "name at least one reference to ask about; section 12.6 exists "
            "because 'benefic in this rasi' on its own is the question a BAV "
            "already answers")
    unknown = [r for r in references if r not in ASHTAKAVARGA_REFERENCES]
    if unknown:
        raise AshtakavargaError(
            f"unknown reference {', '.join(sorted(unknown))}; the eight are "
            f"{', '.join(ASHTAKAVARGA_REFERENCES)}")

    benefic = set(benefic_from_in(owner, reference_signs, rasi))
    verdicts = {
        reference: {
            "benefic": reference in benefic,
            "why": (
                f"{owner} is benefic in {RASI_NAMES[rasi]} from {reference}"
                if reference in benefic else
                f"{owner} is not benefic in {RASI_NAMES[rasi]} from "
                f"{reference}"
            ),
        }
        for reference in references
    }
    return {
        "owner": owner,
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "asked_about": list(references),
        "verdicts": verdicts,
        "all_of_them": all(v["benefic"] for v in verdicts.values()),
        "any_of_them": any(v["benefic"] for v in verdicts.values()),
        "benefic_from": sorted(benefic),
        "rekhas": len(benefic),
    }
