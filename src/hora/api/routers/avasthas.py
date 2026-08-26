"""Avastha endpoints — book §15.4.

The states themselves. Comparing two planets' strength lives in
``routers/strength.py``, because that is a different question built on top of
these.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from hora.api.models_strength import (
    ActivityIn,
    ActivityOut,
    ActivityResultsIn,
    ActivityResultsOut,
    AvasthaIn,
    AvasthaOut,
    AvasthaRulesOut,
    GhatiIn,
    GhatiOut,
    SoundIn,
    SoundOut,
)
from hora.services import strength_service

router = APIRouter(prefix="/v1/avastha", tags=["avasthas"])


@router.post("/state", response_model=AvasthaOut,
             summary="Every computable state of one graha, section 15.4")
def state(req: AvasthaIn) -> dict:
    try:
        return strength_service.avasthas(
            req.graha, req.graha_longitudes, req.house,
            req.aspected_by, req.close_orb,
        )
    except strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/activity", response_model=ActivityOut,
             summary="Section 15.4.4's sayanaadi avastha, with the formula's working")
def activity(req: ActivityIn) -> dict:
    try:
        return strength_service.activity(
            req.graha, req.graha_longitude, req.moon_longitude,
            req.lagna_rasi, req.ghati, req.name_sound,
        )
    except strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/activity/results", response_model=ActivityResultsOut,
             summary="Per-graha results for a sayanaadi avastha")
def activity_results(req: ActivityResultsIn) -> dict:
    """Licence-gated: structure always, the author's text only when allowed."""
    try:
        return strength_service.activity_results(
            req.avastha, req.graha, req.house, req.rasi, req.joined_by,
            req.moon_phase, req.dignity,
            req.associated_with_malefics, req.associated_with_benefics,
        )
    except strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/ghati", response_model=GhatiOut,
             summary="The ghati running at birth, from hours since sunrise")
def ghati(req: GhatiIn) -> dict:
    try:
        return strength_service.ghatis(req.hours_after_sunrise)
    except strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/sound", response_model=SoundOut,
             summary="Table 37's number for the first sound of a name")
def sound(req: SoundIn) -> dict:
    try:
        return strength_service.sound(req.syllable)
    except strength_service.InputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/rules", response_model=AvasthaRulesOut,
            summary="Section 15.4's avastha tables")
def rules() -> dict:
    return strength_service.rules()
