"""Chakra endpoints — book §1.3.4.

Occupancy and the rasi-based / bhava-based distinction. No drawing.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_chakra import ChakraIn, ChakraOut, ChartStylesOut
from hora.services import chakra_service

router = APIRouter(prefix="/v1/chakra", tags=["chakras"])


@router.post("/build", response_model=ChakraOut,
             summary="A chart's twelve cells, with rasi and house for each")
def build(req: ChakraIn) -> dict:
    try:
        return chakra_service.chart(
            req.graha_positions, req.upagraha_positions,
            req.special_lagna_positions, req.lagna,
            req.positions_are_longitudes,
            chakra_service.DEFAULT_REFERENCE
            if req.reference is None else req.reference,
            req.reference_rasi,
        )
    except chakra_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/styles", response_model=ChartStylesOut,
            summary="Section 1.3.4's three drawing styles")
def styles() -> dict:
    return chakra_service.styles()
