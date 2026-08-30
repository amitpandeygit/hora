"""Chart-analysis endpoints — book section 13.4.1."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_analysis import AnalysisRulesOut, InfluencesIn
from hora.services import analysis_service

router = APIRouter(prefix="/v1/analysis", tags=["interpretation"])


@router.get("/rules", response_model=AnalysisRulesOut,
            summary="Section 13.4.1's six factors and its worked examples")
def rules() -> dict:
    return analysis_service.rules()


@router.get("/matters", summary="Every matter section 13.4.1 names")
def matters() -> dict:
    return analysis_service.matters()


@router.get("/matter", summary="Chart, house, reference and arudha for one matter")
def matter(name: str = Query(..., examples=["academic reputation"])) -> dict:
    try:
        return analysis_service.for_matter(name)
    except (analysis_service.AnalysisError,
            analysis_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/influences", summary="Every influence on one house or arudha")
def influences(req: InfluencesIn) -> dict:
    try:
        return analysis_service.influences(req.sign, req.graha_signs)
    except (analysis_service.AnalysisError,
            analysis_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
