"""Display-name resolution.

Two transliteration schemes are carried:

* ``book`` — exactly as printed in P.V.R. Narasimha Rao's *Vedic Astrology: An
  Integrated Approach*. This is the default output.
* ``standard`` — the more common pan-Indian Sanskrit forms (Pushya, Magha,
  Ashlesha, Shravana), which many readers outside the south expect.

Names are display only. The integer indices in every response are the stable
contract, so a scheme change never breaks an API consumer.

PARITY: the book dates from 2000 and JHora 8.0 from 2016; JHora's own display
names have not been checked and may match neither scheme exactly.
"""
from __future__ import annotations

from enum import Enum

from hora.core import const


class NameScheme(str, Enum):
    BOOK = "book"
    STANDARD = "standard"


_TABLES: dict[str, dict[NameScheme, list[str]]] = {
    "nakshatra": {
        NameScheme.BOOK: const.NAKSHATRA_NAMES_BOOK,
        NameScheme.STANDARD: const.NAKSHATRA_NAMES,
    },
    "nakshatra28": {
        NameScheme.BOOK: const.NAKSHATRA_NAMES_28_BOOK,
        NameScheme.STANDARD: const.NAKSHATRA_NAMES_28,
    },
    "tithi": {
        NameScheme.BOOK: const.TITHI_NAMES_BOOK,
        NameScheme.STANDARD: const.TITHI_NAMES,
    },
    "yoga": {
        NameScheme.BOOK: const.YOGA_NAMES_BOOK,
        NameScheme.STANDARD: const.YOGA_NAMES,
    },
    "karana": {
        NameScheme.BOOK: const.KARANA_NAMES_BOOK,
        NameScheme.STANDARD: const.KARANA_NAMES,
    },
    "masa": {
        NameScheme.BOOK: const.MASA_NAMES_BOOK,
        NameScheme.STANDARD: const.MASA_NAMES,
    },
    "rasi": {
        NameScheme.BOOK: const.RASI_NAMES,
        NameScheme.STANDARD: const.RASI_NAMES,
    },
    "graha": {
        NameScheme.BOOK: const.GRAHA_NAMES,
        NameScheme.STANDARD: const.GRAHA_NAMES,
    },
    "vaara": {
        NameScheme.BOOK: const.VAARA_NAMES,
        NameScheme.STANDARD: const.VAARA_NAMES,
    },
    "paksha": {
        NameScheme.BOOK: const.PAKSHA_NAMES,
        NameScheme.STANDARD: const.PAKSHA_NAMES,
    },
}


def name(table: str, index: int, scheme: NameScheme = NameScheme.BOOK) -> str:
    """Look up one display name."""
    return _TABLES[table][scheme][index]


def both(table: str, index: int) -> dict[str, str]:
    """Return both spellings, for responses that want to carry each."""
    return {
        "name": _TABLES[table][NameScheme.BOOK][index],
        "name_standard": _TABLES[table][NameScheme.STANDARD][index],
    }
