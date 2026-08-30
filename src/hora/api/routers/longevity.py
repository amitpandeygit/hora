"""Longevity endpoints — book sections 14.3 to 14.5.

Kept apart from `marakas.py`, which covers section 14.2 and is at the
architecture line cap.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from hora.api.models_maraka import (
    EighthLordIn,
    LongevityIn,
    MaheswaraIn,
    RudraIn,
)
from hora.services import maraka_service

router = APIRouter(prefix="/v1/longevity", tags=["longevity"])


def _guard(call, *args) -> dict:
    try:
        return call(*args)
    except (maraka_service.MarakaError, maraka_service.InputError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rudra-rules", summary="Section 14.3's framing and Table 32")
def rudra_rules() -> dict:
    return maraka_service.section_14_3()


@router.get("/rudra", summary="Section 14.3's two Rudra candidates")
def rudra(lagna: int = Query(..., ge=0, le=11, examples=[4])) -> dict:
    return _guard(maraka_service.rudra, lagna)


@router.get("/trishoola", summary="The three Trishoola rasis from Rudra")
def trishoola(rudra_sign: int = Query(..., ge=0, le=11, examples=[7])) -> dict:
    return _guard(maraka_service.trishoola, rudra_sign)


@router.post("/maheswara", summary="Section 14.3's Maheswara and exceptions")
def maheswara(req: MaheswaraIn) -> dict:
    return _guard(maraka_service.maheswara_for, req.ak_sign, req.graha_signs)


@router.get("/rules", summary="Section 14.4's rules and its tables")
def longevity_rules() -> dict:
    return maraka_service.section_14_4()


@router.post("/three-pairs", summary="Section 14.4's method of three pairs")
def longevity(req: LongevityIn) -> dict:
    return _guard(maraka_service.longevity, req.lagna, req.graha_signs,
                  req.hl_sign)


@router.get("/eighth-lord-rules",
            summary="Section 14.5, Example 48 and Exercise 23")
def eighth_lord_rules() -> dict:
    return maraka_service.section_14_5()


@router.post("/eighth-lord", summary="Section 14.5's eighth lord method")
def eighth_lord(req: EighthLordIn) -> dict:
    return _guard(maraka_service.eighth_lord, req.reference, req.graha_signs)


@router.post("/rudra", summary="Section 14.3's Rudra, through the cascade")
def rudra_decided(req: RudraIn) -> dict:
    return _guard(maraka_service.rudra_for, req.lagna, req.graha_signs,
                  req.graha_longitudes)
