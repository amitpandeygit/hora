"""Input guards shared by the calculation modules.

Every one of these exists because something silently produced a plausible
wrong answer instead of failing: a NaN longitude surfaced as
``cannot convert float NaN to integer`` from deep inside a floor division, and
a negative elapsed time returned a perfectly ordinary-looking degree.

A calculation that cannot be meaningful should say so, in terms of the input
the caller gave it.
"""
from __future__ import annotations

import math


class InputError(ValueError):
    """Raised when an input cannot produce a meaningful result."""


def finite(name: str, value: float) -> float:
    """Reject NaN and infinity, which otherwise fail far from the cause."""
    number = float(value)
    if not math.isfinite(number):
        raise InputError(f"{name} must be a finite number, got {value!r}")
    return number


def positive(name: str, value: float) -> float:
    """Reject zero and negatives where only a positive quantity makes sense."""
    number = finite(name, value)
    if number <= 0.0:
        raise InputError(f"{name} must be positive, got {number}")
    return number


def non_negative(name: str, value: float) -> float:
    """Reject negatives where the quantity is measured forward from something."""
    number = finite(name, value)
    if number < 0.0:
        raise InputError(f"{name} must not be negative, got {number}")
    return number


def in_range(name: str, value: int, low: int, high: int) -> int:
    """Reject an integer outside an inclusive range."""
    if not low <= value <= high:
        raise InputError(f"{name} must be between {low} and {high}, got {value}")
    return value


def longitude(name: str, value: float) -> float:
    """A zodiacal longitude, reduced into 0-360.

    Wrapping is deliberate — the zodiac is a circle and the book itself says
    to "expunge multiples of 360". Only a non-finite value is an error.
    """
    return finite(name, value) % 360.0
