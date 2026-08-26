"""Karaka endpoints — book chapter 8.

Three kinds, three endpoints. §8.1 warns against using them interchangeably,
so none of these falls back to another; ``/kinds`` states the distinction.

Chara karakas take longitudes rather than a nativity: the assignment depends
only on where the eight grahas sit within their rasis.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_karaka import (
    CharaKarakaIn,
    CharaKarakasOut,
    KarakaKindsOut,
    NaisargikaKarakasOut,
    SthiraKarakasOut,
)
from hora.services import karaka_service

router = APIRouter(prefix="/v1/karaka", tags=["karakas"])


@router.post("/chara", response_model=CharaKarakasOut,
             summary="Assign the eight chara karakas from graha longitudes")
def chara(req: CharaKarakaIn) -> dict:
    try:
        return karaka_service.chara(req.longitudes)
    except karaka_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/sthira", response_model=SthiraKarakasOut,
            summary="Section 8.3's fixed significators")
def sthira() -> dict:
    return karaka_service.sthira()


@router.get("/naisargika", response_model=NaisargikaKarakasOut,
            summary="Tables 15 and 16 — the natural significators")
def naisargika() -> dict:
    return karaka_service.naisargika()


@router.get("/kinds", response_model=KarakaKindsOut,
            summary="All three kinds of karaka and what each is for")
def kinds() -> dict:
    return karaka_service.kinds()
