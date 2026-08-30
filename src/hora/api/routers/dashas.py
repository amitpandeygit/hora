"""Dasha endpoints.

HTTP only — the calculation lives in :mod:`hora.services.dasha_service`.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.deps import to_instant, to_place
from hora.api.models import DashaCatalogOut, DashaResponse
from hora.api.schemas import DashaRequest
from hora.services import dasha_service, reference_service

router = APIRouter(prefix="/v1/dasha", tags=["dashas"])


@router.get("/systems", response_model=DashaCatalogOut,
            summary="Dasha systems currently implemented")
def systems() -> dict:
    return reference_service.dasha_catalog()


@router.post("", response_model=DashaResponse,
             summary="Compute a nakshatra-based dasha tree")
def dasha(req: DashaRequest) -> dict:
    try:
        return dasha_service.dasha_tree(
            to_instant(req), to_place(req), req.settings,
            system=req.system, levels=req.levels, cycles=req.cycles,
            start_star=req.start_star,
            as_of=req.as_of, tz_name=req.tz_name,
            utc_offset_hours=req.utc_offset_hours,
        )
    except dasha_service.UnknownDashaSystem as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except dasha_service.BadAsOf as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
