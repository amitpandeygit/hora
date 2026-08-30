"""Maraka endpoints — book chapter 14."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_maraka import (
    LongevityIn,
    MaheswaraIn,
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


@router.get("/rudra-rules", summary="Section 14.3's framing and Table 32")
def rudra_rules() -> dict:
    return maraka_service.section_14_3()


@router.get("/rudra", summary="Section 14.3's two Rudra candidates")
def rudra(lagna: int = Query(..., ge=0, le=11, examples=[4])) -> dict:
    try:
        return maraka_service.rudra(lagna)
    except (maraka_service.MarakaError, maraka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/trishoola", summary="The three Trishoola rasis from Rudra")
def trishoola(rudra_sign: int = Query(..., ge=0, le=11, examples=[7])) -> dict:
    try:
        return maraka_service.trishoola(rudra_sign)
    except (maraka_service.MarakaError, maraka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/maheswara", summary="Section 14.3's Maheswara and exceptions")
def maheswara(req: MaheswaraIn) -> dict:
    try:
        return maraka_service.maheswara_for(req.ak_sign, req.graha_signs)
    except (maraka_service.MarakaError, maraka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/longevity-rules", summary="Section 14.4's rules and its tables")
def longevity_rules() -> dict:
    return maraka_service.section_14_4()


@router.post("/longevity", summary="Section 14.4's method of three pairs")
def longevity(req: LongevityIn) -> dict:
    try:
        return maraka_service.longevity(
            req.lagna, req.graha_signs, req.hl_sign)
    except (maraka_service.MarakaError, maraka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
