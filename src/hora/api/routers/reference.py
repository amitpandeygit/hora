"""Reference content endpoints — editorial material, never calculation.

HTTP only — the store lives in :mod:`hora.services.content_service`. A client
joins this to a chart by the integer id every calculation response carries.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_reference import (
    AllRasiContentOut,
    ContentSourcesOut,
    RasiContentOut,
)
from hora.services import content_service

router = APIRouter(prefix="/v1/reference", tags=["reference"])


@router.get("/sources", response_model=ContentSourcesOut,
            summary="Content sources and their licence status")
def sources() -> dict:
    return content_service.sources()


@router.get("/rasis", response_model=AllRasiContentOut,
            summary="Indications for all twelve rasis")
def all_rasis(source: str | None = Query(None, description="Filter to one source key")) -> dict:
    return content_service.all_rasis(source)


@router.get("/rasis/{rasi}", response_model=RasiContentOut,
            summary="Indications for one rasi")
def one_rasi(rasi: int, source: str | None = Query(None)) -> dict:
    try:
        return content_service.one_rasi(rasi, source)
    except content_service.UnknownRasi as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except content_service.NoContent as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
