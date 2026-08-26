"""One error shape for the whole API.

Before this, three different shapes were in use: FastAPI's ``{"detail": "..."}``
for a raised ``HTTPException``, ``{"detail": [ ... ]}`` for a request that failed
validation — same key, different type — and a third shape from the ``ValueError``
handler. A client could not parse an error without knowing which path produced it.

Every error now looks the same::

    {"error": {"type": "...", "message": "...", "details": [...] or null}}

``type`` is a stable machine-readable slug; ``message`` is human-readable and may
be reworded; ``details`` carries per-field validation problems and is null when
there are none.
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

#: HTTP status -> stable error type slug.
_TYPE_BY_STATUS = {
    400: "bad_request",
    404: "not_found",
    409: "conflict",
    422: "unprocessable",
    429: "rate_limited",
    500: "internal_error",
}


class ErrorDetail(BaseModel):
    """One field-level problem, for a request that failed validation."""

    location: list[str] = Field(..., description="Path to the offending field")
    message: str
    type: str


class ErrorBody(BaseModel):
    type: str = Field(..., description="Stable slug; safe to branch on")
    message: str = Field(..., description="Human-readable; wording may change")
    details: list[ErrorDetail] | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody


def _payload(status: int, message: str, details=None) -> JSONResponse:
    body = ErrorBody(
        type=_TYPE_BY_STATUS.get(status, "error"), message=message, details=details
    )
    return JSONResponse(status_code=status, content=ErrorResponse(error=body).model_dump())


def install(app: FastAPI) -> None:
    """Attach the handlers. Called once, from the app factory."""

    @app.exception_handler(HTTPException)
    def _http(_request: Request, exc: HTTPException) -> JSONResponse:
        return _payload(exc.status_code, str(exc.detail))

    @app.exception_handler(RequestValidationError)
    def _validation(_request: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            ErrorDetail(
                location=[str(part) for part in err.get("loc", [])],
                message=err.get("msg", ""),
                type=err.get("type", ""),
            )
            for err in exc.errors()
        ]
        return _payload(422, "the request did not validate", details)

    @app.exception_handler(ValueError)
    def _value_error(_request: Request, exc: ValueError) -> JSONResponse:
        return _payload(422, str(exc))
