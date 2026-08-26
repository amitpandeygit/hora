#!/usr/bin/env python3
"""Print this engine's output in fixture shape, for side-by-side transcription.

Run a chart here, run the same chart in JHora, and fill the fixture's
``expected`` block from the JHora screen. This script never writes into
``expected`` — its output goes in a separate ``hora_observed`` block so that our
own numbers can never be mistaken for the benchmark's.

    python scripts/emit_fixture_template.py tests/benchmark/fixtures/pvr_1972.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hora.charts.chart import Place, compute_chart
from hora.charts.vargas import varga
from hora.core.const import GRAHA_NAMES, RASI_NAMES, Graha
from hora.core.settings import Settings
from hora.core.timeutil import format_dms, from_local
from hora.dasha.base import balance_at_birth
from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text())
    chart = compute_chart(
        from_local(**data["birth"]),
        Place(**data["place"]),
        Settings(**data.get("settings", {})),
    )
    exp = data.get("expected", {})

    observed: dict = {
        "ayanamsa": round(chart.ayanamsa, 6),
        "ayanamsa_dms": format_dms(chart.ayanamsa),
        "lagna_longitude": round(chart.lagna_longitude, 6),
        "lagna_readable": f"{RASI_NAMES[chart.lagna_rasi]} {format_dms(chart.lagna_longitude % 30)}",
        "graha_longitudes": {},
        "graha_readable": {},
        "graha_retrograde": {},
        "varga_signs": {},
        "dasha_balance": {},
    }
    for gid, st in chart.grahas.items():
        name = GRAHA_NAMES[gid]
        observed["graha_longitudes"][name] = round(st.longitude, 6)
        observed["graha_readable"][name] = f"{st.rasi_name} {format_dms(st.degrees_in_rasi)}"
        observed["graha_retrograde"][name] = st.retrograde

    varga_request = exp.get("varga_signs") or {"D9": None}
    for code in varga_request:
        names = varga_request.get(code) or {"Lagna": None, **{n: None for n in GRAHA_NAMES[:9]}}
        table = {}
        for name in names:
            lon = chart.lagna_longitude if name == "Lagna" else chart.positions[GRAHA_NAMES.index(name)].longitude
            table[name] = RASI_NAMES[varga(lon, code).sign]
        observed["varga_signs"][code] = table

    for key in (exp.get("dasha_balance") or {"vimshottari": None}):
        lord, years = balance_at_birth(NAKSHATRA_DASHA_SYSTEMS[key], chart.positions[Graha.MOON].longitude)
        observed["dasha_balance"][key] = {"lord": GRAHA_NAMES[lord], "years": round(years, 6)}

    print(json.dumps({"hora_observed": observed}, indent=2))


if __name__ == "__main__":
    main()
