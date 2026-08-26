"""Parity harness against Jagannatha Hora.

The workflow is deliberately black-box: run a chart in JHora, transcribe its
output into a fixture, and let this module diff our engine against it.  Nothing
here inspects or decompiles JHora itself — it treats the software purely as an
oracle, which is both the legally clean approach and the one that actually
catches disagreements.

A fixture slot with ``null`` for its expected value is reported as
``unverified`` rather than passing, so that unfilled slots can never be
mistaken for parity.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from hora.charts.chart import Place, compute_chart
from hora.charts.vargas import varga
from hora.core.const import GRAHA_NAMES, RASI_NAMES
from hora.core.settings import Settings
from hora.core.timeutil import from_local

#: Default tolerance for a longitude comparison, in arcseconds.
#: One arcsecond is far below any interpretive significance but tight enough to
#: catch a wrong ayanamsa, node type or ephemeris.
DEFAULT_TOLERANCE_ARCSEC = 1.0

FIXTURE_DIR = Path(__file__).resolve().parents[3] / "tests" / "benchmark" / "fixtures"


@dataclass(frozen=True, slots=True)
class Comparison:
    """One field compared against JHora."""

    path: str
    expected: Any
    actual: Any
    status: str            # "match" | "mismatch" | "unverified"
    delta_arcsec: float | None = None
    note: str | None = None


@dataclass(slots=True)
class Fixture:
    """A benchmark case: input, JHora's output, and settings used in JHora."""

    name: str
    source: str
    birth: dict
    place: dict
    settings: Settings
    expected: dict
    notes: str = ""
    #: Optional named settings overrides to run the same fixture under.
    #: Used when a JHora preference is unresolved and we report every
    #: candidate side by side instead of picking one.
    settings_variants: dict[str, dict] = field(default_factory=dict)
    comparisons: list[Comparison] = field(default_factory=list)


def load_fixture(path: str | Path) -> Fixture:
    data = json.loads(Path(path).read_text())
    return Fixture(
        name=data["name"],
        source=data.get("source", "unknown"),
        birth=data["birth"],
        place=data["place"],
        settings=Settings(**data.get("settings", {})),
        expected=data.get("expected", {}),
        notes=data.get("notes", ""),
        settings_variants=data.get("settings_variants", {}),
    )


def _arcsec(a: float, b: float) -> float:
    diff = abs((a - b + 180.0) % 360.0 - 180.0)
    return diff * 3600.0


def _compare_longitude(path: str, expected: Any, actual: float, tol: float) -> Comparison:
    if expected is None:
        return Comparison(path, None, round(actual, 6), "unverified",
                          note="no JHora value recorded yet")
    delta = _arcsec(float(expected), actual)
    return Comparison(
        path, expected, round(actual, 6),
        "match" if delta <= tol else "mismatch", round(delta, 4),
    )


def _compare_exact(path: str, expected: Any, actual: Any) -> Comparison:
    if expected is None:
        return Comparison(path, None, actual, "unverified",
                          note="no JHora value recorded yet")
    return Comparison(path, expected, actual, "match" if expected == actual else "mismatch")


def compare_fixture(
    fixture: Fixture,
    tolerance_arcsec: float = DEFAULT_TOLERANCE_ARCSEC,
    settings_override: dict | None = None,
) -> list[Comparison]:
    """Run our engine over a fixture's input and diff against the recorded output.

    ``settings_override`` layers extra settings on top of the fixture's own —
    used to evaluate an unresolved preference under every candidate value
    rather than committing to one.
    """
    instant = from_local(**fixture.birth)
    place = Place(**fixture.place)
    settings = (
        fixture.settings.model_copy(update=settings_override)
        if settings_override else fixture.settings
    )
    chart = compute_chart(instant, place, settings)
    exp = fixture.expected
    out: list[Comparison] = []

    if "ayanamsa" in exp:
        out.append(_compare_longitude("ayanamsa", exp["ayanamsa"], chart.ayanamsa, tolerance_arcsec))

    if "lagna_longitude" in exp:
        out.append(_compare_longitude("lagna.longitude", exp["lagna_longitude"],
                                      chart.lagna_longitude, tolerance_arcsec))

    for name, want in (exp.get("graha_longitudes") or {}).items():
        gid = GRAHA_NAMES.index(name)
        out.append(_compare_longitude(f"graha.{name}.longitude", want,
                                      chart.positions[gid].longitude, tolerance_arcsec))

    for name, want in (exp.get("graha_retrograde") or {}).items():
        gid = GRAHA_NAMES.index(name)
        out.append(_compare_exact(f"graha.{name}.retrograde", want, chart.grahas[gid].retrograde))

    # Varga signs are the highest-value check: they are what the varga *rule*
    # decides, independent of tiny ephemeris differences.
    for code, table in (exp.get("varga_signs") or {}).items():
        for name, want in table.items():
            lon = chart.lagna_longitude if name == "Lagna" else chart.positions[GRAHA_NAMES.index(name)].longitude
            got = RASI_NAMES[varga(lon, code).sign]
            out.append(_compare_exact(f"varga.{code}.{name}", want, got))

    for name, want in (exp.get("dasha_balance") or {}).items():
        from hora.core.const import Graha
        from hora.dasha.base import balance_at_birth
        from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

        spec = NAKSHATRA_DASHA_SYSTEMS[name]
        lord, years = balance_at_birth(spec, chart.positions[Graha.MOON].longitude)
        out.append(_compare_exact(f"dasha.{name}.lord", want.get("lord"), GRAHA_NAMES[lord]))
        if want.get("years") is not None:
            delta = abs(want["years"] - years)
            out.append(Comparison(
                f"dasha.{name}.years", want["years"], round(years, 6),
                "match" if delta < 1e-3 else "mismatch",
            ))

    if settings_override is None:
        fixture.comparisons = out
    return out


def summarise(comparisons: list[Comparison]) -> dict[str, int]:
    counts = {"match": 0, "mismatch": 0, "unverified": 0}
    for c in comparisons:
        counts[c.status] += 1
    return counts


def format_report(fixture: Fixture, comparisons: list[Comparison]) -> str:
    counts = summarise(comparisons)
    lines = [
        f"Fixture: {fixture.name}",
        f"Source:  {fixture.source}",
        f"Result:  {counts['match']} match, {counts['mismatch']} mismatch, {counts['unverified']} unverified",
        "",
    ]
    for c in comparisons:
        if c.status == "match":
            continue
        mark = "MISMATCH" if c.status == "mismatch" else "unverified"
        delta = f"  (delta {c.delta_arcsec}\")" if c.delta_arcsec is not None else ""
        lines.append(f"  [{mark:10s}] {c.path}: jhora={c.expected!r} hora={c.actual!r}{delta}")
    return "\n".join(lines)


def compare_variants(
    fixture: Fixture,
    tolerance_arcsec: float = DEFAULT_TOLERANCE_ARCSEC,
) -> dict[str, list[Comparison]]:
    """Run the fixture under every declared settings variant."""
    if not fixture.settings_variants:
        return {"default": compare_fixture(fixture, tolerance_arcsec)}
    return {
        name: compare_fixture(fixture, tolerance_arcsec, override)
        for name, override in fixture.settings_variants.items()
    }


def format_variant_report(fixture: Fixture, results: dict[str, list[Comparison]]) -> str:
    """Print one column per settings variant, so no default has to be chosen."""
    names = list(results)
    by_path: dict[str, dict[str, Comparison]] = {}
    for variant, comps in results.items():
        for c in comps:
            by_path.setdefault(c.path, {})[variant] = c

    width = max((len(p) for p in by_path), default=10)
    header = f"{'field':<{width}}  " + "  ".join(f"{n:>18s}" for n in names)
    lines = [
        f"Fixture: {fixture.name}",
        f"Source:  {fixture.source}",
        "",
        header,
        "-" * len(header),
    ]
    for path, row in by_path.items():
        cells = []
        for n in names:
            cell: Comparison | None = row.get(n)
            if cell is None:
                cells.append(f"{'-':>18s}")
            elif cell.status == "match":
                cells.append(f"{'match':>18s}")
            elif cell.status == "unverified":
                cells.append(f"{'(no value)':>18s}")
            elif cell.delta_arcsec is not None:
                cells.append(f"{cell.delta_arcsec:>15.3f}\"")
            else:
                cells.append(f"{str(cell.actual)[:18]:>18s}")
        lines.append(f"{path:<{width}}  " + "  ".join(cells))

    lines.append("-" * len(header))
    totals = f"{'TOTAL match':<{width}}  "
    totals += "  ".join(f"{summarise(results[n])['match']:>18d}" for n in names)
    lines.append(totals)
    mism = f"{'TOTAL mismatch':<{width}}  "
    mism += "  ".join(f"{summarise(results[n])['mismatch']:>18d}" for n in names)
    lines.append(mism)
    return "\n".join(lines)
