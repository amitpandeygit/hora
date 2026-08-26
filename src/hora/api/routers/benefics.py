"""Natural benefic endpoints — book §3.2.2."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_benefic import BeneficIn, BeneficOut, BeneficRulesOut
from hora.services import benefic_service

router = APIRouter(prefix="/v1/benefic", tags=["benefics"])


@router.post("/nature", response_model=BeneficOut,
             summary="A graha's natural benefic status, with the reason")
def compute(req: BeneficIn) -> dict:
    try:
        return benefic_service.nature(req.graha, req.paksha, req.companions)
    except benefic_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=BeneficRulesOut,
            summary="Section 3.2.2's two clauses and the conditional grahas")
def rules() -> dict:
    return benefic_service.rules()
