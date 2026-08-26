"""Editorial content service — the reference material, kept apart from calculation."""
from __future__ import annotations

from hora.content import get_store
from hora.content.store import serving_unconfirmed_allowed
from hora.core.const import RASI_NAMES


class UnknownRasi(ValueError):
    """Raised when a rasi index is outside 0..11."""


class NoContent(LookupError):
    """Raised when nothing is stored for a subject."""


def _entry_out(e) -> dict:
    base = {
        "source": e.source,
        "licence_status": e.licence_status,
        "term_count": len(e.terms),
    }
    if not e.servable:
        return {
            **base,
            "withheld": True,
            "reason": (
                "This source's redistribution licence is unconfirmed. Set "
                "HORA_SERVE_UNCONFIRMED_CONTENT=1 to release it."
            ),
        }
    return {
        **base,
        "withheld": False,
        "verbatim": e.verbatim,
        "transcription_notes": e.transcription_notes,
        "terms": [{"term": t.term, "category": t.category} for t in e.terms],
        "by_category": e.by_category(),
    }


def sources() -> dict:
    store = get_store()
    return {
        "serving_unconfirmed": serving_unconfirmed_allowed(),
        "sources": store.sources,
        "note": (
            "Categorisation of individual terms is this project's editorial judgement, "
            "not the source author's."
        ),
    }


def all_rasis(source: str | None = None) -> dict:
    store = get_store()
    return {
        "subject": "rasi",
        "rasis": [
            {
                "rasi": i,
                "rasi_name": RASI_NAMES[i],
                "entries": [_entry_out(e) for e in store.get("rasi", i, source=source)],
            }
            for i in range(12)
        ],
    }


def one_rasi(rasi: int, source: str | None = None) -> dict:
    if not 0 <= rasi <= 11:
        raise UnknownRasi("rasi must be 0..11 (0 = Aries)")
    store = get_store()
    entries = store.get("rasi", rasi, source=source)
    if not entries:
        raise NoContent(f"no content for rasi {rasi}")
    return {
        "rasi": rasi,
        "rasi_name": RASI_NAMES[rasi],
        "entries": [_entry_out(e) for e in entries],
    }
