"""The book's own charts, looked up by number.

`core.constants.book_charts` holds them as the book prints them; this module
parses those printed longitudes and answers the questions a caller actually
has — what sign is each body in, which charts can be recomputed, which
divisionals are drawn beside the rasi chart.
"""
from __future__ import annotations

import re
from typing import Any

from hora.core import validate
from hora.core.const import (
    BOOK_CHARTS,
    CHARTS_NOT_SUPPLIED,
    RASI_ABBR,
    UNNUMBERED_CHARTS,
    Graha,
)

_LONGITUDE = re.compile(r"(\d+) ?([A-Za-z]{2}) ?(\d+)")

_RASI_INDEX = {abbr: index for index, abbr in enumerate(RASI_ABBR)}

#: The book's abbreviations for the nine grahas, as printed beside the charts.
GRAHA_OF: dict[str, Graha] = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
    "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU,
}


class BookChartError(validate.InputError):
    """Raised when a chart is asked for that the book has not supplied."""


def longitude(text: str) -> float:
    """Parse a printed longitude such as "23 Le 10" into degrees."""
    match = _LONGITUDE.fullmatch(text.strip())
    if not match or match.group(2) not in _RASI_INDEX:
        raise BookChartError(
            f"{text!r} is not a printed longitude; the book writes them as "
            f'"23 Le 10" — degrees, rasi abbreviation, minutes')
    degrees, rasi, minutes = match.groups()
    return _RASI_INDEX[rasi] * 30 + int(degrees) + int(minutes) / 60


def numbers() -> tuple[int, ...]:
    """Every chart number the book has supplied, ascending."""
    return tuple(sorted(BOOK_CHARTS))


def unnumbered_labels() -> tuple[str, ...]:
    """Every example or exercise that supplies a chart without a "Chart N"."""
    return tuple(sorted(UNNUMBERED_CHARTS))


def unnumbered_chart(label: str) -> dict[str, Any]:
    """One of those charts, by the book's own label ("Exercise 24").

    Partial by nature — see the record's note for what the text withheld.
    """
    if label in UNNUMBERED_CHARTS:
        return UNNUMBERED_CHARTS[label]
    raise BookChartError(
        f"{label!r} does not supply a chart of its own. Those that do are "
        f"{', '.join(unnumbered_labels())}")


def chart(number: int) -> dict[str, Any]:
    """One chart's record, exactly as the register holds it."""
    if number in BOOK_CHARTS:
        return BOOK_CHARTS[number]
    if number in CHARTS_NOT_SUPPLIED:
        raise BookChartError(
            f"Chart {number} has never been printed in any section read so "
            f"far. The charts we have are "
            f"{', '.join(str(n) for n in numbers())}")
    raise BookChartError(
        f"there is no Chart {number}. The charts we have are "
        f"{', '.join(str(n) for n in numbers())}")


def has_longitudes(number: int) -> bool:
    """Whether the book printed degrees for this chart, or only a diagram."""
    return bool(chart(number).get("longitudes"))


def longitudes(number: int) -> dict[str, float]:
    """One chart's printed longitudes, parsed. Keys are the book's names.

    :raises BookChartError: for a chart the book printed as a diagram only.
    """
    record = chart(number)
    if not record.get("longitudes"):
        raise BookChartError(
            f"Chart {number} is printed as a diagram with no degrees, so it "
            f"has no longitudes. Use `signs({number})` for the rasis.")
    return {name: longitude(text)
            for name, text in record["longitudes"].items()}


def signs(number: int) -> dict[str, int]:
    """The sign each printed body occupies. 0 = Aries.

    Falls back to the drawn diagram for a chart printed without degrees.
    """
    if has_longitudes(number):
        return {name: int(value // 30)
                for name, value in longitudes(number).items()}
    drawn = chart(number).get("drawn")
    if not drawn:
        raise BookChartError(
            f"Chart {number} prints neither longitudes nor a diagram")
    index = {abbr: n for n, abbr in enumerate(RASI_ABBR)}
    return {name: index[abbr] for name, abbr in drawn.items()}


def graha_signs(number: int) -> dict[int, int]:
    """Graha id to sign, for the nine grahas — the shape most modules take."""
    found = signs(number)
    return {int(graha): found[name]
            for name, graha in GRAHA_OF.items() if name in found}


def graha_longitudes(number: int) -> dict[int, float]:
    """Graha id to longitude, for the nine grahas."""
    found = longitudes(number)
    return {int(graha): found[name]
            for name, graha in GRAHA_OF.items() if name in found}


def lagna(number: int) -> int:
    """The sign the ascendant falls in."""
    found = signs(number)
    if "Asc" not in found:
        raise BookChartError(
            f"Chart {number} prints no ascendant, so it has no lagna")
    return found["Asc"]


def is_recomputable(number: int) -> bool:
    """Whether the chart's own birth line is complete enough to recompute."""
    return "birth_data" in chart(number)


def recomputable() -> tuple[int, ...]:
    """Every chart that can be checked against the ephemeris."""
    return tuple(n for n in numbers() if is_recomputable(n))


def divisional(number: int, code: str) -> dict[str, str]:
    """A divisional diagram printed beside the rasi chart, box by box."""
    drawn = chart(number).get("divisional", {})
    if code not in drawn:
        available = ", ".join(sorted(drawn)) or "none"
        raise BookChartError(
            f"Chart {number} prints no {code} diagram; it prints {available}")
    return dict(drawn[code])


def describe(number: int) -> dict[str, Any]:
    """One chart, with everything derived that a caller usually wants next."""
    record = chart(number)
    return {
        "number": number,
        "title": record["title"],
        "birth": record.get("birth"),
        "place": record.get("place"),
        "recomputable": is_recomputable(number),
        "longitudes": dict(record.get("longitudes", {})),
        "signs": {name: RASI_ABBR[sign] for name, sign in signs(number).items()},
        "lagna": (RASI_ABBR[lagna(number)]
                  if "Asc" in signs(number) else None),
        "drawn": record.get("drawn"),
        "divisional": {code: dict(boxes)
                       for code, boxes in record.get("divisional", {}).items()},
        "chara_karakas": record.get("chara_karakas"),
        "retrograde": list(record.get("retrograde", ())),
        "first_seen": record.get("first_seen"),
        "note": record.get("note"),
        "related": {
            name: dict(body) for name, body in record.get("related", {}).items()
        },
    }
