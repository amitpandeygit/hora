"""Raw ephemeris endpoints.

HTTP only — the calculation lives in :mod:`hora.services.ephemeris_service`.
"""
from __future__ import annotations

from fastapi import APIRouter

from hora.api.deps import to_instant, to_place
from hora.api.models import EphemerisResponse
from hora.api.schemas import ChartRequest
from hora.services import ephemeris_service

router = APIRouter(prefix="/v1/ephemeris", tags=["ephemeris"])


@router.post("/positions", response_model=EphemerisResponse,
             summary="Sidereal positions of the grahas")
def positions(req: ChartRequest) -> dict:
    return ephemeris_service.positions(to_instant(req), to_place(req), req.settings)
