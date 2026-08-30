"""The book's charts, service layer."""
from __future__ import annotations

from hora.charts.book import (
    BookChartError,
    chart,
    describe,
    numbers,
    recomputable,
)
from hora.core.const import CHARTS_NOT_SUPPLIED


def index() -> dict:
    """Every chart the book has printed, and the ones it has not."""
    return {
        "charts": [
            {"number": n, "title": chart(n)["title"],
             "birth": chart(n).get("birth"),
             "recomputable": n in recomputable(),
             "first_seen": chart(n).get("first_seen")}
            for n in numbers()
        ],
        "recomputable": list(recomputable()),
        "not_supplied": list(CHARTS_NOT_SUPPLIED),
        "not_supplied_note": (
            "Chart 4 has never appeared in any section read so far, and "
            "nothing has cited it."
        ),
        "note": (
            "A chart with birth data is recomputed from its own birth line "
            "and so checks the ephemeris. One without is a transcription "
            "only, and its record says why."
        ),
    }


def one(number: int) -> dict:
    return describe(number)


__all__ = ["BookChartError", "index", "one"]
