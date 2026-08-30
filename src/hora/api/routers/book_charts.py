"""The book's own charts — every chart it prints, by number."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from hora.services import book_chart_service

router = APIRouter(prefix="/v1/book-charts", tags=["book"])


@router.get("", summary="Every chart the book prints")
def index() -> dict:
    return book_chart_service.index()


@router.get("/{number}", summary="One chart, with everything derived from it")
def one(number: int = Path(..., ge=1, le=99)) -> dict:
    try:
        return book_chart_service.one(number)
    except book_chart_service.BookChartError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
