"""Baadhaka endpoints — book section 13.3."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_baadhaka import (
    BaadhakaChartIn,
    BaadhakaCheckIn,
    BaadhakaRulesOut,
    BaadhakaSignIn,
)
from hora.services import baadhaka_service

router = APIRouter(prefix="/v1/baadhakas", tags=["interpretation"])


@router.get("/rules", response_model=BaadhakaRulesOut,
            summary="Section 13.3's rule, Table 31 and its example")
def rules() -> dict:
    return baadhaka_service.rules()


@router.post("/sign", summary="The baadhaka sthaana of one house or arudha")
def sign(req: BaadhakaSignIn) -> dict:
    try:
        return baadhaka_service.of_sign(req.sign, req.graha_signs)
    except (baadhaka_service.BaadhakaError,
            baadhaka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/check", summary="Whether one graha is a baadhaka from a sign")
def check(req: BaadhakaCheckIn) -> dict:
    try:
        return baadhaka_service.check(req.graha, req.sign, req.graha_signs)
    except (baadhaka_service.BaadhakaError,
            baadhaka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/chart", summary="The baadhaka of all twelve houses")
def chart(req: BaadhakaChartIn) -> dict:
    try:
        return baadhaka_service.for_chart(req.lagna_sign, req.graha_signs)
    except (baadhaka_service.BaadhakaError,
            baadhaka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
