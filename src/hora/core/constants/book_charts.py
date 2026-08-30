"""Every chart the book prints, in one place.

Charts arrived a chapter at a time and their fixtures grew where they were
first needed — Chart 6 in chapter 10's tests, Chart 3 in chapter 12's
constants, and so on. This module is the single register: one record per
chart, with the birth line as printed, the printed longitudes, the drawn
diagrams, and the chara karakas where the book prints them.

Longitudes are kept as the book prints them ("23 Le 10") rather than as
floats, because that is what a reader checks against. `charts.book` parses
them.

A chart with `birth_data` is recomputable from its own birth line and is used
as a check on the ephemeris. One without is a transcription only, and says why.
"""
from __future__ import annotations

from typing import Any

#: Chart 4 has never appeared in any section read so far, and nothing has
#: cited it. Chart 1's JHora output is still the empty stub of OI-1.
CHARTS_NOT_SUPPLIED = (4,)

#: number -> record. Keys used across records:
#:   title, birth, birth_data, place, longitudes, drawn, chara_karakas,
#:   divisional, note, first_seen
BOOK_CHARTS: dict[int, dict[str, Any]] = {
    1: {
        "title": "The reference chart",
        "birth": "April 9, 2000, 1:35 pm (5:00 West), 71 W 12, 42 N 30",
        "longitudes": {
            "Asc": "10 Vi 58", "Sun": "26 Pi 29", "Moon": "4 Ge 45",
            "Mars": "19 Ar 09", "Merc": "1 Pi 36", "Jup": "17 Ar 21",
            "Ven": "10 Pi 01", "Sat": "22 Ar 41", "Rahu": "5 Cn 55",
            "Ketu": "5 Cp 55",
        },
        "chara_karakas": {
            "Sun": "AK", "Rahu": "AmK", "Sat": "BK", "Mars": "MK",
            "Jup": "PiK", "Ven": "PK", "Moon": "GK", "Merc": "DK",
        },
        "first_seen": "chapter 9",
        "note": (
            "The book's reference chart. Its JHora output is still the empty "
            "stub of OI-1, so it cannot settle any convention question."
        ),
    },
    2: {
        "title": "The D-16 exercise chart",
        "birth": "April 9, 2000, 5:55 pm (5:00 West), 71 W 12, 42 N 30",
        "longitudes": {
            "Asc": "22 Vi 41", "Sun": "26 Pi 32", "Moon": "5 Ge 21",
            "Mars": "19 Ar 11", "Merc": "1 Pi 39", "Jup": "17 Ar 22",
            "Ven": "10 Pi 04", "Sat": "22 Ar 42", "Rahu": "5 Cn 55",
            "Ketu": "5 Cp 55",
        },
        "divisional": {
            "D16": {
                "Sun": "Aq", "Moon": "Aq", "Mars": "Aq", "Merc": "Sg",
                "Jup": "Cp", "Ven": "Ta", "Sat": "Ar", "Rahu": "Cn",
                "Ketu": "Cn",
            },
        },
        "first_seen": "chapter 9",
        "note": "The exercise works in the D-16 built from these longitudes.",
    },
    3: {
        "title": "Rasi — A.B. Vajpayee",
        "birth": "December 25, 1926, 5:12 am (IST), 78 E 10, 26 N 14",
        "birth_data": {
            "year": 1926, "month": 12, "day": 25, "hour": 5, "minute": 12,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 26 + 14 / 60, "longitude": 78 + 10 / 60},
        "longitudes": {
            "Asc": "14 Sc 18", "Sun": "9 Sg 35", "Moon": "15 Le 28",
            "Mars": "13 Ar 39", "Merc": "20 Sc 59", "Jup": "2 Aq 05",
            "Ven": "17 Sg 42", "Sat": "9 Sc 41", "Rahu": "14 Ge 30",
            "Ketu": "14 Sg 30", "HL": "13 Li 46", "GL": "21 Cn 25",
        },
        "drawn": {
            "Mars": "Ar", "Rahu": "Ge", "GL": "Cn", "Moon": "Le", "HL": "Li",
            "Merc": "Sc", "Asc": "Sc", "Sat": "Sc", "Ven": "Sg", "Sun": "Sg",
            "Ketu": "Sg", "AL": "Cp", "Jup": "Aq",
        },
        "chara_karakas": {
            "Merc": "AK", "Ven": "AmK", "Rahu": "BK", "Moon": "MK",
            "Mars": "PiK", "Sat": "PK", "Sun": "GK", "Jup": "DK",
        },
        "first_seen": "chapter 12, Example 39",
    },
    5: {
        "title": "The aspects exercise chart",
        "longitudes": {
            "Asc": "5 Li 23", "Sun": "6 Ar 20", "Moon": "20 Li 50",
            "Mars": "26 Ar 22", "Merc": "17 Pi 21", "Jup": "19 Ar 42",
            "Ven": "22 Pi 25", "Sat": "23 Ar 55", "Rahu": "5 Cn 23",
            "Ketu": "5 Cp 23", "HL": "17 Ta 16", "GL": "19 Cp 30",
        },
        "divisional": {
            "D9": {
                "Asc": "Sc", "Sun": "Ta", "Moon": "Ar", "Mars": "Sc",
                "Merc": "Sg", "Jup": "Vi", "Ven": "Cp", "Sat": "Sc",
                "Rahu": "Le", "Ketu": "Aq", "HL": "Ge", "GL": "Ge",
            },
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Mars": "BK", "Moon": "MK",
            "Jup": "PiK", "Merc": "PK", "Sun": "GK", "Rahu": "DK",
        },
        "first_seen": "chapter 10",
        "note": "No birth line is printed, so it is a transcription only.",
    },
    6: {
        "title": "Rasi — P.V. Narasimha Rao",
        "birth": "June 28, 1921, 12:49 pm (5:17 East), 79 E 09, 18 N 26",
        "birth_data": {
            "year": 1921, "month": 6, "day": 28, "hour": 12, "minute": 49,
            "second": 0.0, "utc_offset_hours": 5 + 17 / 60,
        },
        "place": {"latitude": 18 + 26 / 60, "longitude": 79 + 9 / 60},
        "longitudes": {
            "Asc": "24 Vi 19", "Sun": "13 Ge 16", "Moon": "10 Pi 33",
            "Mars": "13 Ge 33", "Merc": "27 Ge 40", "Jup": "20 Le 06",
            "Ven": "27 Ar 40", "Sat": "26 Le 26", "Rahu": "0 Li 47",
            "Ketu": "0 Ar 47", "HL": "24 Cp 11", "GL": "25 Sg 59",
        },
        "chara_karakas": {
            "Rahu": "AK", "Merc": "AmK", "Ven": "BK", "Sat": "MK",
            "Jup": "PiK", "Mars": "PK", "Sun": "GK", "Moon": "DK",
        },
        "first_seen": "chapter 10",
        "note": (
            "The offset is 5h17m east, not modern IST. Chart 11 is the same "
            "native at a different printed time — see D-38."
        ),
    },
    7: {
        "title": "Rasi — Ronald Reagan",
        "birth": "February 6, 1911, 2:04 am (6:00 West), 89 W 47, 41 N 38",
        "birth_data": {
            "year": 1911, "month": 2, "day": 6, "hour": 2, "minute": 4,
            "second": 0.0, "utc_offset_hours": -6.0,
        },
        "place": {"latitude": 41 + 38 / 60, "longitude": -(89 + 47 / 60)},
        "longitudes": {
            "Asc": "7 Sc 08", "Sun": "23 Cp 49", "Moon": "19 Ar 49",
            "Mars": "11 Sg 19", "Merc": "28 Sg 49", "Jup": "21 Li 07",
            "Ven": "10 Aq 56", "Sat": "8 Ar 12", "Rahu": "21 Ar 54",
            "Ketu": "21 Li 54", "HL": "19 Le 41", "GL": "29 Sg 42",
        },
        "chara_karakas": {
            "Merc": "AK", "Sun": "AmK", "Jup": "BK", "Moon": "MK",
            "Mars": "PiK", "Ven": "PK", "Sat": "GK", "Rahu": "DK",
        },
        "first_seen": "chapter 10",
        "note": "Exercise 22 works this chart through the whole of chapter 12.",
    },
    8: {
        "title": "The argala exercise chart",
        "birth": "December 2, 1946, 6:45 am (1:00 East), 15 E 39, 38 N 06",
        "birth_data": {
            "year": 1946, "month": 12, "day": 2, "hour": 6, "minute": 45,
            "second": 0.0, "utc_offset_hours": 1.0,
        },
        "place": {"latitude": 38 + 6 / 60, "longitude": 15 + 39 / 60},
        "longitudes": {
            "Asc": "13 Sc 14", "Sun": "16 Sc 20", "Moon": "20 Aq 15",
            "Mars": "25 Sc 30", "Merc": "28 Li 09", "Jup": "21 Li 27",
            "Ven": "24 Li 47", "Sat": "15 Cn 39", "Rahu": "18 Ta 36",
            "Ketu": "18 Sc 36", "HL": "10 Sc 16", "GL": "2 Sc 40",
        },
        "chara_karakas": {
            "Merc": "AK", "Mars": "AmK", "Ven": "BK", "Jup": "MK",
            "Moon": "PiK", "Sun": "PK", "Sat": "GK", "Rahu": "DK",
        },
        "first_seen": "chapter 10",
        "note": "Neutral on OI-68: it does not separate the node conventions.",
    },
    9: {
        "title": "Rasi — Chatrapati Shivaji",
        "birth": "Phalguna Bahula Tritiya, 1630 AD, 12:05 hrs after sunrise",
        "place": "73 E 53, 18 N 32",
        "longitudes": {
            "Asc": "27 Le 41", "Sun": "22 Aq 19", "Moon": "27 Vi 52",
            "Mars": "16 Ge 00", "Merc": "6 Pi 18", "Jup": "5 Aq 51",
            "Ven": "8 Ar 30", "Sat": "16 Li 34", "Rahu": "29 Ta 22",
            "Ketu": "29 Sc 22", "HL": "24 Aq 15", "GL": "27 Le 55",
        },
        "chara_karakas": {
            "Moon": "AK", "Sun": "AmK", "Sat": "BK", "Mars": "MK",
            "Ven": "PiK", "Merc": "PK", "Jup": "GK", "Rahu": "DK",
        },
        "first_seen": "chapter 11",
        "note": (
            "Not recomputable: a Hindu calendar date and a time measured from "
            "sunrise, with no Gregorian date and no time zone."
        ),
    },
    10: {
        "title": "Rasi — Akbar",
        "birth": "December 4, 1542, 3:39 am (4:39 East), 69 E 47, 25 N 19",
        "birth_data": {
            "year": 1542, "month": 12, "day": 4, "hour": 3, "minute": 39,
            "second": 0.0, "utc_offset_hours": 4 + 39 / 60,
        },
        "place": {"latitude": 25 + 19 / 60, "longitude": 69 + 47 / 60},
        "longitudes": {
            "Asc": "15 Li 30", "Sun": "23 Sc 46", "Moon": "8 Ge 51",
            "Mars": "23 Cp 05", "Merc": "10 Sg 10", "Jup": "5 Li 42",
            "Ven": "28 Li 10", "Sat": "27 Li 28", "Rahu": "7 Aq 56",
            "Ketu": "7 Le 56", "HL": "27 Le 03", "GL": "18 Ar 18",
        },
        "drawn": {
            "GL": "Ar", "Moon": "Ge", "Rahu": "Aq", "Mars": "Cp", "HL": "Le",
            "Ketu": "Le", "Merc": "Sg", "Sun": "Sc", "Jup": "Li", "Asc": "Li",
            "Sat": "Li", "Ven": "Li",
        },
        "first_seen": "chapter 11",
        "note": "Forty years before the Gregorian reform. Favours the mean node.",
    },
    11: {
        "title": "Rasi — the SAV chart",
        "birth": "June 28, 1921, 1:08 pm (IST), 79 E 09, 18 N 26",
        "longitudes": {
            "Asc": "25 Vi 45", "Sun": "13 Ge 17", "Moon": "10 Pi 36",
            "Mars": "13 Ge 33", "Merc": "27 Ge 40", "Jup": "20 Le 06",
            "Ven": "27 Ar 40", "Sat": "26 Le 26", "Rahu": "0 Li 47",
            "Ketu": "0 Ar 47", "HL": "27 Cp 11", "GL": "3 Cp 29",
        },
        "chara_karakas": {
            "Rahu": "AK", "Ven": "AmK", "Merc": "BK", "Sat": "MK",
            "Jup": "PiK", "Mars": "PK", "Sun": "GK", "Moon": "DK",
        },
        "first_seen": "chapter 12",
        "note": (
            "The same native as Chart 6 at a different printed time — 1:08 pm "
            "IST against 12:49 pm at 5h17m east. See D-38 and D-39."
        ),
    },
    12: {
        "title": "D-10 SAV Exercise",
        "birth": "August 16, 1958, 7:05 am (4:00 West), 83 W 53, 43 N 36",
        "birth_data": {
            "year": 1958, "month": 8, "day": 16, "hour": 7, "minute": 5,
            "second": 0.0, "utc_offset_hours": -4.0,
        },
        "place": {"latitude": 43 + 36 / 60, "longitude": -(83 + 53 / 60)},
        "longitudes": {
            "Asc": "3 Le 29", "Sun": "29 Cn 47", "Moon": "17 Le 39",
            "Mars": "22 Ar 05", "Merc": "12 Le 23", "Jup": "3 Li 06",
            "Ven": "7 Cn 13", "Sat": "25 Sc 51", "Rahu": "2 Li 03",
            "Ketu": "2 Ar 03", "HL": "11 Le 38", "GL": "29 Le 25",
        },
        "divisional": {
            "D10": {
                "Sat": "Pi", "Ketu": "Ar", "Ven": "Ta", "GL": "Ta",
                "Moon": "Cp", "Merc": "Sg", "Sun": "Sg", "Jup": "Sc",
                "Mars": "Sc", "HL": "Sc", "Rahu": "Li", "Asc": "Vi",
            },
        },
        "chara_karakas": {
            "Sun": "AK", "Rahu": "AmK", "Sat": "BK", "Mars": "MK",
            "Merc": "PK", "Ven": "GK", "Jup": "DK", "Moon": "PiK",
        },
        "first_seen": "chapter 12, Exercise 21",
        "note": (
            "Its drawn diagram is the D-10, not the rasi chart. Exercise 21 "
            "identifies the native as Madonna."
        ),
    },
    13: {
        "title": "Rasi — Swami Chandrasekhara Saraswathi",
        "birth": "May 20, 1894, 1:22 pm (IST), 79 E 32, 11 N 57",
        "birth_data": {
            "year": 1894, "month": 5, "day": 20, "hour": 13, "minute": 22,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 11 + 57 / 60, "longitude": 79 + 32 / 60},
        "longitudes": {
            "Asc": "23 Le 10", "Sun": "6 Ta 52", "Moon": "14 Sc 01",
            "Mars": "14 Aq 49", "Merc": "6 Ta 28", "Jup": "17 Ta 58",
            "Ven": "22 Pi 11", "Sat": "26 Vi 50", "Rahu": "15 Pi 25",
            "Ketu": "15 Vi 25", "HL": "23 Sg 54", "GL": "4 Sg 55",
        },
        "drawn": {
            "Rahu": "Pi", "Ven": "Pi", "Merc": "Ta", "Sun": "Ta", "Jup": "Ta",
            "Mars": "Aq", "Asc": "Le", "GL": "Sg", "HL": "Sg", "AL": "Sc",
            "Moon": "Sc", "Ketu": "Vi", "Sat": "Vi",
        },
        "divisional": {
            "D20": {
                "Asc": "Pi", "Merc": "Ar", "Sun": "Ar", "Ketu": "Ge",
                "Rahu": "Ge", "AL": "Cn", "Sat": "Cp", "Jup": "Sc",
                "HL": "Sc", "GL": "Sc", "Ven": "Li", "Mars": "Vi",
                "Moon": "Vi",
            },
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Jup": "BK", "Mars": "MK",
            "Rahu": "PiK", "Moon": "PK", "Sun": "GK", "Merc": "DK",
        },
        "retrograde": ("Sat",),
        "first_seen": "chapter 13, Example 44",
        "note": (
            "The chief pontiff of Kanchi Kama Koti Peetham. Its D-20 is "
            "printed beside the rasi chart, which makes Example 44 a check on "
            "the varga as well as on the reading."
        ),
    },
}
