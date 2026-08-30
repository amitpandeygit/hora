"""Maraka endpoints — book chapter 14."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_maraka import (
    MarakaIn,
    MarakaRulesOut,
)
from hora.services import maraka_service

router = APIRouter(prefix="/v1/marakas", tags=["longevity"])


@router.get("/rules", response_model=MarakaRulesOut,
            summary="Chapter 14's framing and section 14.2's rules")
def rules() -> dict:
    return maraka_service.rules()


@router.post("", summary="Every maraka for one lagna")
def for_lagna(req: MarakaIn) -> dict:
    try:
        return maraka_service.for_lagna(req.lagna, req.graha_signs)
    except (maraka_service.MarakaError, maraka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
