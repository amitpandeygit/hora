"""Functional-nature endpoints — book section 13.2."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_functional import (
    FunctionalLagnaOut,
    FunctionalPlanetIn,
    FunctionalRulesOut,
)
from hora.services import functional_service

router = APIRouter(prefix="/v1/functional", tags=["interpretation"])


@router.get("/rules", response_model=FunctionalRulesOut,
            summary="Section 13.2's rules, Table 30, and where they diverge")
def rules() -> dict:
    return functional_service.rules()


@router.get("/lagna", response_model=FunctionalLagnaOut,
            summary="Every planet's functional nature for one lagna")
def lagna(sign: int = Query(..., ge=0, le=11, examples=[1])) -> dict:
    try:
        return functional_service.lagna(sign)
    except (functional_service.FunctionalError,
            functional_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/planet", summary="One planet's functional nature")
def planet(req: FunctionalPlanetIn) -> dict:
    try:
        return functional_service.planet(req.planet, req.lagna, req.waxing)
    except (functional_service.FunctionalError,
            functional_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
