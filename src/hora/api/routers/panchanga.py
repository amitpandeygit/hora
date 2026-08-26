"""Panchanga endpoint.

HTTP only — the calculation lives in :mod:`hora.services.panchanga_service`.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.deps import to_instant, to_place
from hora.api.models import PanchangaResponse
from hora.api.schemas import PanchangaRequest
from hora.services import panchanga_service

router = APIRouter(prefix="/v1/panchanga", tags=["panchanga"])


@router.post("", response_model=PanchangaResponse,
             summary="Five limbs plus sunrise-anchored day structure")
def panchanga(req: PanchangaRequest) -> dict:
    try:
        return panchanga_service.panchanga_for(
            to_instant(req), to_place(req), req.settings
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
