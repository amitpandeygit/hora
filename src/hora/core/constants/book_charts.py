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

#: Charts cited by a section we have read but not printed there. Chart 4 has
#: never appeared and nothing cites it. Chart 65 is cited by Exercise 39's
#: answer — "See Chart 65" — and has not been supplied; every claim the answer
#: makes about it is checked from Exercise 38's nativity and the given transit
#: date instead. Chart 1's JHora output is still the empty stub of OI-1.
CHARTS_NOT_SUPPLIED = (4, 65)

#: **Finding.** Every birth time in the book is printed to the minute, so a
#: printed ascendant can be up to half a minute of time away from ours while
#: every graha agrees. Nine of the register's forty-four recomputable charts
#: show it, the widest being Chart 17 at 15.8' — which is 48 seconds, the
#: ascendant there rising at 19.7' a minute. It is the stated time's
#: resolution, not the engine: the grahas in those same charts all land inside
#: an arcminute.
THE_ASCENDANT_CARRIES_THE_BIRTH_TIMES_ROUNDING = (
    "A printed ascendant can sit 5' to 16' from ours while every graha in the "
    "same chart agrees to under an arcminute. In every such case the gap is "
    "under a minute of birth time, which is the resolution the book prints."
)

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
        "events": {"India's Prime Minister since": "March 1998"},
        "first_seen": "chapter 12, Example 39",
        "note": (
            "Example 101 calls this \"birthdata and D-10 chart\"; the register "
            "holds the rasi diagram and the twelve rasi longitudes, and the "
            "D-10 is computed from them rather than transcribed. Its SAV, AL, "
            "A5 and GL all reproduce what Examples 39 and 101 assert."
        ),
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
        "events": {"died": "July 1997, aged 50"},
        "first_seen": "chapter 10",
        "note": (
            "Neutral on OI-68: it does not separate the node conventions. "
            "The chart the book returns to most -- chapter 10's argala "
            "exercise, Exercise 23's Rudra and longevity, chapter 20's Sudasa "
            "seed for OI-126, and Example 84, which times its death."
        ),
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
    14: {
        "title": "Rasi and D-3 — Rajiv Gandhi",
        "birth": "August 20, 1944, 7:11 am (IST), 72 E 49, 18 N 58",
        "birth_data": {
            "year": 1944, "month": 8, "day": 20, "hour": 7, "minute": 11,
            "second": 40.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 18 + 58 / 60, "longitude": 72 + 49 / 60},
        "longitudes": {
            "Asc": "14 Le 44", "Sun": "3 Le 49", "Moon": "17 Le 09",
            "Mars": "1 Vi 12", "Merc": "28 Le 34", "Jup": "12 Le 12",
            "Ven": "18 Le 40", "Sat": "14 Ge 13", "Rahu": "2 Cn 48",
            "Ketu": "2 Cp 48", "HL": "29 Le 06", "GL": "7 Li 04",
        },
        "divisional": {
            "D3": {
                "Merc": "Ar", "HL": "Ar", "Rahu": "Cn", "Sun": "Le",
                "Mars": "Vi", "AL": "Vi", "Sat": "Li", "GL": "Li",
                "Moon": "Sg", "Asc": "Sg", "Ven": "Sg", "Jup": "Sg",
                "Ketu": "Cp",
            },
        },
        "chara_karakas": {
            "Merc": "AK", "Rahu": "AmK", "Ven": "BK", "Mars": "DK",
            "Sun": "GK", "Moon": "MK", "Sat": "PiK", "Jup": "PK",
        },
        "related": {
            "His younger brother": {
                "title": "Rasi — Sanjay Gandhi",
                "drawn": {
                    "Rahu": "Ta", "GL": "Ge", "Sat": "Cn", "Moon": "Le",
                    "Ven": "Li", "Jup": "Li", "AL": "Li", "Merc": "Sc",
                    "Sun": "Sc", "Ketu": "Sc", "Mars": "Sg", "Asc": "Cp",
                    "HL": "Aq",
                },
                "retrograde": ("Sat",),
                "note": (
                    "Printed as boxes only — no longitudes and no birth "
                    "line — so it is a transcription and cannot be "
                    "recomputed. Example 45 draws parallels between it and "
                    "Rajiv's D-3."
                ),
            },
        },
        "first_seen": "chapter 13, Example 45",
        "note": (
            "The printed time is 7:11 am, but chapter 11's footnote 37 gives "
            "7:11:40 and only the seconds reproduce the ascendant: 0.8' "
            "against 8.6' at 7:11:00. Its D-3 is printed beside the rasi "
            "chart, and Sanjay Gandhi's rasi chart beside both."
        ),
    },
    15: {
        "title": "D-24 — the twins Satyam and Shivam Gaur",
        "birth": "November 4, 1970, 4:06 pm (IST), 76 E 53, 30 N 44",
        "birth_data": {
            "year": 1970, "month": 11, "day": 4, "hour": 16, "minute": 6,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 30 + 44 / 60, "longitude": 76 + 53 / 60},
        "longitudes": {
            "Asc": "19 Pi 54", "Sun": "18 Li 09", "Moon": "21 Sg 18",
            "Mars": "16 Vi 04", "Merc": "23 Li 07", "Jup": "21 Li 57",
            "Ven": "27 Li 32", "Sat": "26 Ar 16", "Rahu": "5 Aq 33",
            "Ketu": "5 Le 33", "HL": "1 Le 04", "GL": "6 Li 02",
        },
        "divisional": {
            "D24": {
                "Sat": "Ta", "Ven": "Ge", "AL": "Aq", "Merc": "Aq",
                "Mars": "Cn", "Jup": "Cp", "Moon": "Cp", "HL": "Le",
                "Ketu": "Sg", "Rahu": "Sg", "GL": "Sg", "Sun": "Li",
                "Asc": "Li",
            },
        },
        "chara_karakas": {
            "Ven": "AK", "Sat": "AmK", "Rahu": "BK", "Merc": "MK",
            "Jup": "PiK", "Moon": "PK", "Sun": "GK", "Mars": "DK",
        },
        "retrograde": ("Ven", "Sat"),
        "related": {
            "Shivam Gaur": {
                "title": "D-24 — Shivam Gaur, the second twin",
                "birth": "November 4, 1970, 4:08 pm (IST), 76 E 53, 30 N 44",
                "birth_data": {
                    "year": 1970, "month": 11, "day": 4, "hour": 16,
                    "minute": 8, "second": 0.0, "utc_offset_hours": 5.5,
                },
                "place": {"latitude": 30 + 44 / 60, "longitude": 76 + 53 / 60},
                "longitudes": {
                    "Asc": "20 Pi 37", "Sun": "18 Li 09", "Moon": "21 Sg 19",
                    "Mars": "16 Vi 04", "Merc": "23 Li 07", "Jup": "21 Li 57",
                    "Ven": "27 Li 32", "Sat": "26 Ar 16", "Rahu": "5 Aq 33",
                    "Ketu": "5 Le 33", "HL": "2 Le 03", "GL": "8 Li 30",
                },
                "divisional": {
                    "D24": {
                        "Sat": "Ta", "Ven": "Ge", "GL": "Aq", "Merc": "Aq",
                        "Mars": "Cn", "Jup": "Cp", "Moon": "Cp", "AL": "Cp",
                        "Ketu": "Sg", "Rahu": "Sg", "Asc": "Sc", "Sun": "Li",
                        "HL": "Vi",
                    },
                },
                "retrograde": ("Ven", "Sat"),
                "note": (
                    "Born two minutes after his twin. Only the ascendant, "
                    "Moon, HL and GL differ in the printed rasi chart — by "
                    "43', 1', 59' and 2 deg 28' — yet the D-24 lagna moves "
                    "from Libra to Scorpio."
                ),
            },
        },
        "first_seen": "chapter 13, Example 46",
        "note": (
            "Chart 15 prints the D-24 of both twins. They share a rasi chart "
            "to the printed precision, so the D-24 is where they part."
        ),
    },
    58: {
        "title": "A.B. Vajpayee, D-10 and its ashtakavarga — Example 108",
        "birth": "December 25, 1926, 5:12 am (IST), 78 E 10, 26 N 13",
        "birth_data": {
            "year": 1926, "month": 12, "day": 25, "hour": 5, "minute": 12,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 26 + 13 / 60, "longitude": 78 + 10 / 60},
        "longitudes": {
            "Asc": "14 Sc 18", "Sun": "9 Sg 35", "Moon": "15 Le 28",
            "Mars": "13 Ar 39", "Merc": "20 Sc 59", "Jup": "2 Aq 05",
            "Ven": "17 Sg 42", "Sat": "9 Sc 41", "Rahu": "14 Ge 30",
            "Ketu": "14 Sg 30", "HL": "13 Li 43", "GL": "21 Cn 18",
        },
        "chara_karakas": {
            "Merc": "AK", "Ven": "AmK", "Rahu": "BK", "Moon": "MK",
            "Mars": "PiK", "Sat": "PK", "Sun": "GK", "Jup": "DK",
        },
        "divisional": {
            "D10": {
                "Sun": "Pi", "Ketu": "Ar", "Ven": "Ta", "HL": "Aq",
                "Jup": "Aq", "Merc": "Cp", "Moon": "Cp", "Mars": "Le",
                "AL": "Vi", "Rahu": "Li", "Sat": "Li", "GL": "Li",
                "Asc": "Sc",
            },
        },
        "ashtakavarga": {
            "D10": {
                "Sun": (5, 3, 6, 2, 3, 4, 7, 6, 3, 3, 2, 4),
                "Moon": (2, 4, 2, 3, 6, 6, 4, 4, 4, 6, 3, 5),
                "Mars": (3, 4, 4, 3, 4, 2, 2, 5, 3, 4, 1, 4),
                "Mercury": (4, 4, 6, 4, 6, 5, 3, 6, 4, 5, 4, 3),
                "Jupiter": (4, 6, 4, 2, 3, 8, 3, 6, 4, 3, 7, 6),
                "Venus": (2, 4, 6, 4, 3, 5, 3, 5, 5, 6, 5, 4),
                "Saturn": (3, 1, 5, 2, 3, 3, 4, 3, 5, 4, 2, 4),
                "SAV": (23, 26, 33, 20, 28, 33, 26, 35, 28, 31, 24, 30),
            },
        },
        "events": {"became India's Prime Minister": "March 19, 1998"},
        "first_seen": "chapter 25, Example 108",
        "note": (
            "Chart 3's nativity reprinted, with the latitude given as 26 N "
            "**13** rather than 26 N 14. Every graha and the ascendant are "
            "identical to the printed arcminute; only HL and GL differ, by 3' "
            "and 7' — see OI-103, which this second casting sharpens. Its "
            "value is the **ashtakavarga**: the only place the book prints "
            "all seven BAVs and the SAV of one chart, and all 96 figures "
            "reproduce."
        ),
    },
    59: {
        "title": "Vajpayee's swearing-in transit — Example 108",
        "birth": "March 19, 1998, 9:32 am (IST), 77 E 12, 28 N 36",
        "kind": "transit",
        "birth_data": {
            "year": 1998, "month": 3, "day": 19, "hour": 9, "minute": 32,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 28 + 36 / 60, "longitude": 77 + 12 / 60},
        "longitudes": {
            "Asc": "4 Ta 01", "Sun": "4 Pi 31", "Moon": "9 Sc 46",
            "Mars": "17 Pi 20", "Merc": "22 Pi 53", "Jup": "16 Aq 23",
            "Ven": "18 Cp 21", "Sat": "26 Pi 21", "Rahu": "15 Le 48",
            "Ketu": "15 Aq 48", "HL": "6 Ge 27", "GL": "24 Li 33",
        },
        "chara_karakas": {
            "Sat": "AK", "Merc": "AmK", "Ven": "BK", "Sun": "DK",
            "Moon": "GK", "Mars": "MK", "Jup": "PiK", "Rahu": "PK",
        },
        "drawn": {
            "Mars": "Pi", "Sun": "Pi", "Sat": "Pi", "Merc": "Pi",
            "Asc": "Ta", "HL": "Ge", "Ketu": "Aq", "Jup": "Aq",
            "Ven": "Cp", "Rahu": "Le", "Moon": "Sc", "GL": "Li", "AL": "Vi",
        },
        "events": {"Vajpayee was sworn in as Prime Minister": "March 19, 1998"},
        "first_seen": "chapter 25, Example 108",
        "note": (
            "A transit chart with full data, unlike Charts 52 and 53. It is "
            "read against Chart 58's D-10 ashtakavarga, which makes it §25.4's "
            "interaction (1) with §25.5's rekha counts behind it."
        ),
    },
    57: {
        "title": "John F. Kennedy, Jr — natal rasi and transit D-11, Example 107",
        "birth": "November 25, 1960, 12:22 am (5:00 West), 77 W 02, 38 N 53",
        "birth_data": {
            "year": 1960, "month": 11, "day": 25, "hour": 0, "minute": 22,
            "second": 0.0, "utc_offset_hours": -5.0,
        },
        "place": {"latitude": 38 + 53 / 60, "longitude": -(77 + 2 / 60)},
        "longitudes": {
            "Asc": "18 Le 39", "Sun": "9 Sc 38", "Moon": "4 Aq 06",
            "Mars": "25 Ge 12", "Merc": "19 Li 55", "Jup": "12 Sg 31",
            "Ven": "18 Sg 35", "Sat": "22 Sg 15", "Rahu": "17 Le 58",
            "Ketu": "17 Aq 58", "HL": "19 Ar 11", "GL": "19 Ge 34",
        },
        "chara_karakas": {
            "Mars": "AK", "Sat": "AmK", "Merc": "BK", "Moon": "DK",
            "Sun": "GK", "Ven": "MK", "Jup": "PiK", "Rahu": "PK",
        },
        "retrograde": ("Mars",),
        "drawn": {
            "HL": "Ar", "GL": "Ge", "Mars": "Ge", "Rahu": "Le", "Asc": "Le",
            "Merc": "Li", "AL": "Sc", "Sun": "Sc", "Ven": "Sg", "Jup": "Sg",
            "Sat": "Sg", "Ketu": "Aq", "Moon": "Aq",
        },
        "transit": {
            "for": "his death",
            "date": "July 16, 1999, 9:45 pm (4:00 West), 71 W 12, 42 N 30",
            "birth_data": {
                "year": 1999, "month": 7, "day": 16, "hour": 21, "minute": 45,
                "second": 0.0, "utc_offset_hours": -4.0,
            },
            "place": {"latitude": 42.5, "longitude": -(71 + 12 / 60)},
            "longitudes": {
                "Asc": "0 Aq 51", "Sun": "0 Cn 14", "Moon": "21 Le 49",
                "Mars": "10 Li 37", "Merc": "14 Cn 58", "Jup": "8 Ar 45",
                "Ven": "8 Le 18", "Sat": "21 Ar 41", "Rahu": "20 Cn 06",
                "Ketu": "20 Cp 06", "HL": "10 Sc 49", "GL": "27 Sc 42",
            },
            "divisional": {
                "D11": {
                    "AL": "Pi", "Ven": "Pi", "Merc": "Ge", "Asc": "Ge",
                    "GL": "Cn", "Jup": "Cn", "Rahu": "Le", "Moon": "Le",
                    "Sat": "Sc", "HL": "Sg", "Mars": "Cp", "Sun": "Cp",
                    "Ketu": "Aq",
                },
            },
        },
        "events": {"died in a plane crash": "July 16, 1999"},
        "first_seen": "chapter 25, Example 107",
        "note": (
            "The same nativity and the same instant as Chart 56, drawn the "
            "other way round: the natal **rasi** chart against the transit "
            "**D-11**. That pairing is §25.4's interaction (2), the half the "
            "section says fine-tunes the timing, and this is the only place "
            "in the book it is worked. Its AL reaches Scorpio through §9.2's "
            "7th-house exception. The transit Moon's D-11 needs the "
            "**ephemeris**: the printed 21 Le 49 sits 5.5 arcseconds below "
            "the 9th ekadasamsa boundary and gives Cancer, while the true "
            "position is 47 arcseconds above it and gives Leo, as drawn."
        ),
    },
    56: {
        "title": "John F. Kennedy, Jr — natal D-11 and transit rasi, Example 107",
        "birth": "November 25, 1960, 12:22 am (5:00 West), 77 W 02, 38 N 53",
        "birth_data": {
            "year": 1960, "month": 11, "day": 25, "hour": 0, "minute": 22,
            "second": 0.0, "utc_offset_hours": -5.0,
        },
        "place": {"latitude": 38 + 53 / 60, "longitude": -(77 + 2 / 60)},
        "longitudes": {
            "Asc": "18 Le 39", "Sun": "9 Sc 38", "Moon": "4 Aq 06",
            "Mars": "25 Ge 12", "Merc": "19 Li 55", "Jup": "12 Sg 31",
            "Ven": "18 Sg 35", "Sat": "22 Sg 15", "Rahu": "17 Le 58",
            "Ketu": "17 Aq 58", "HL": "19 Ar 11", "GL": "19 Ge 34",
        },
        "chara_karakas": {
            "Mars": "AK", "Sat": "AmK", "Merc": "BK", "Moon": "DK",
            "Sun": "GK", "Ven": "MK", "Jup": "PiK", "Rahu": "PK",
        },
        "retrograde": ("Mars",),
        "divisional": {
            "D11": {
                "AL": "Ar", "Sat": "Ar", "Merc": "Ta", "Rahu": "Ge",
                "Asc": "Ge", "Moon": "Cn", "GL": "Vi", "HL": "Sc",
                "Mars": "Sc", "Jup": "Sg", "Sun": "Sg", "Ketu": "Sg",
                "Ven": "Aq",
            },
        },
        "transit": {
            "for": "his death",
            "date": "July 16, 1999, 9:45 pm (4:00 West), 71 W 12, 42 N 30",
            "birth_data": {
                "year": 1999, "month": 7, "day": 16, "hour": 21, "minute": 45,
                "second": 0.0, "utc_offset_hours": -4.0,
            },
            "place": {"latitude": 42.5, "longitude": -(71 + 12 / 60)},
            "longitudes": {
                "Asc": "0 Aq 51", "Sun": "0 Cn 14", "Moon": "21 Le 49",
                "Mars": "10 Li 37", "Merc": "14 Cn 58", "Jup": "8 Ar 45",
                "Ven": "8 Le 18", "Sat": "21 Ar 41", "Rahu": "20 Cn 06",
                "Ketu": "20 Cp 06", "HL": "10 Sc 49", "GL": "27 Sc 42",
            },
            "drawn": {
                "Sat": "Ar", "Jup": "Ar", "Merc": "Cn", "Sun": "Cn",
                "Rahu": "Cn", "Ven": "Le", "Moon": "Le", "Mars": "Li",
                "GL": "Sc", "HL": "Sc", "AL": "Sg", "Ketu": "Cp",
                "Asc": "Aq",
            },
        },
        "events": {
            "died in a plane crash": "July 16, 1999",
        },
        "first_seen": "chapter 25, Example 107",
        "note": (
            "The first chart in the register named for a public figure whose "
            "**death** it reads. Both halves recompute inside an arcminute, "
            "the ascendants included, and all twelve natal D-11 placements "
            "follow from the printed longitudes. Chart 57 prints the same two "
            "moments the other way round -- natal rasi against transit D-11 "
            "-- so the pair is one nativity and one instant drawn twice."
        ),
    },
    55: {
        "title": "A gentleman, and his daughter's birth transit — Example 106",
        "birth": "June 23, 1961, 10:46 pm (IST), 81 E 48, 17 N 00",
        "birth_data": {
            "year": 1961, "month": 6, "day": 23, "hour": 22, "minute": 46,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 17.0, "longitude": 81 + 48 / 60},
        "longitudes": {
            "Asc": "14 Aq 59", "Sun": "8 Ge 40", "Moon": "5 Li 49",
            "Mars": "3 Le 36", "Merc": "14 Ge 25", "Jup": "12 Cp 32",
            "Ven": "23 Ar 00", "Sat": "5 Cp 01", "Rahu": "6 Le 49",
            "Ketu": "6 Aq 49", "HL": "15 Sc 51", "GL": "12 Cp 40",
        },
        "chara_karakas": {
            "Rahu": "AK", "Ven": "AmK", "Merc": "BK", "Mars": "DK",
            "Sat": "GK", "Jup": "MK", "Sun": "PiK", "Moon": "PK",
        },
        "retrograde": ("Merc", "Jup", "Sat"),
        "divisional": {
            "D7": {
                "Ketu": "Pi", "Asc": "Ta", "Mars": "Le", "Sun": "Le",
                "HL": "Le", "Sat": "Le", "Jup": "Vi", "GL": "Vi",
                "Merc": "Vi", "Rahu": "Vi", "Ven": "Vi", "Moon": "Sc",
                "AL": "Cp",
            },
        },
        "transit": {
            "for": "the birth of his daughter",
            "date": "October 3, 1992, 11:58 am (IST), 78 E 30, 17 N 29",
            "birth_data": {
                "year": 1992, "month": 10, "day": 3, "hour": 11, "minute": 58,
                "second": 0.0, "utc_offset_hours": 5.5,
            },
            "place": {"latitude": 17 + 29 / 60, "longitude": 78.5},
            "longitudes": {
                "Asc": "6 Sg 06", "Sun": "16 Vi 32", "Moon": "12 Sg 55",
                "Mars": "17 Ge 26", "Merc": "29 Vi 49", "Jup": "4 Vi 41",
                "Ven": "16 Li 10", "Sat": "18 Cp 11", "Rahu": "1 Sg 24",
                "Ketu": "1 Ge 24", "HL": "11 Pi 56", "GL": "5 Sg 24",
            },
            "drawn": {
                "AL": "Pi", "HL": "Pi", "Ketu": "Ge", "Mars": "Ge",
                "Merc": "Vi", "Sun": "Vi", "Jup": "Vi", "Ven": "Li",
                "Moon": "Sg", "Asc": "Sg", "GL": "Sg", "Rahu": "Sg",
                "Sat": "Cp",
            },
        },
        "events": {"his daughter was born": "October 3, 1992"},
        "first_seen": "chapter 25, Example 106",
        "note": (
            "Supplied one section after Example 106 cited it, and it meets "
            "every line of the checklist that example allowed us to write "
            "without it -- the D-7 lagna is Taurus, Jupiter and Mercury both "
            "stand in Virgo there, and both transit Virgo at the birth. The "
            "nativity's own diagram is the **D-7**. Its ascendant sits 8.6' "
            "from ours, which is 28 seconds of birth time at the rate it "
            "rises here; every graha is inside an arcminute."
        ),
    },
    54: {
        "title": "An engineer, and his wedding-day transit — Example 105",
        "birth": "October 5, 1970, 12:34 pm (IST), 80 E 21, 15 N 49",
        "birth_data": {
            "year": 1970, "month": 10, "day": 5, "hour": 12, "minute": 34,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 15 + 49 / 60, "longitude": 80 + 21 / 60},
        "longitudes": {
            "Asc": "18 Sg 31", "Sun": "18 Vi 11", "Moon": "12 Sc 14",
            "Mars": "26 Le 56", "Merc": "2 Vi 35", "Jup": "15 Li 29",
            "Ven": "27 Li 37", "Sat": "28 Ar 21", "Rahu": "7 Aq 09",
            "Ketu": "7 Le 09", "HL": "5 Ar 23", "GL": "1 Aq 37",
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Mars": "BK", "Merc": "DK",
            "Moon": "GK", "Rahu": "MK", "Sun": "PiK", "Jup": "PK",
        },
        "retrograde": ("Sat",),
        "divisional": {
            "D9": {
                "AL": "Ta", "HL": "Ta", "Ven": "Ge", "Sun": "Ge",
                "Ketu": "Ge", "Jup": "Aq", "Merc": "Cp", "Sat": "Sg",
                "Mars": "Sg", "Rahu": "Sg", "GL": "Li", "Moon": "Li",
                "Asc": "Vi",
            },
        },
        "transit": {
            "for": "the wedding",
            "date": "January 24, 1999, 9:30 am (IST), 78 E 30, 17 N 20",
            "birth_data": {
                "year": 1999, "month": 1, "day": 24, "hour": 9, "minute": 30,
                "second": 0.0, "utc_offset_hours": 5.5,
            },
            "place": {"latitude": 17 + 20 / 60, "longitude": 78 + 30 / 60},
            "longitudes": {
                "Asc": "25 Aq 31", "Sun": "9 Cp 52", "Moon": "1 Ar 31",
                "Mars": "5 Li 11", "Merc": "2 Cp 32", "Jup": "2 Pi 03",
                "Ven": "0 Aq 32", "Sat": "3 Ar 31", "Rahu": "29 Cn 19",
                "Ketu": "29 Cp 19", "HL": "29 Pi 46", "GL": "29 Cn 47",
            },
            "drawn": {
                "HL": "Pi", "Jup": "Pi", "Sat": "Ar", "Moon": "Ar",
                "AL": "Ge", "GL": "Cn", "Rahu": "Cn", "Ven": "Aq",
                "Asc": "Aq", "Merc": "Cp", "Sun": "Cp", "Ketu": "Cp",
                "Mars": "Li",
            },
        },
        "events": {"the engineer married": "January 24, 1999"},
        "first_seen": "chapter 25, Example 105",
        "note": (
            "Two charts again, and this time both carry full data. The "
            "nativity's diagram is its **navamsa**, not its rasi chart, which "
            "is what Example 105 reads. Its transit chart is **the same chart "
            "as Chart 53's** -- same date, and every position, the Ascendant "
            "and the AL identical -- but where Chart 53 gave a date only, "
            "this gives 9:30 am IST at 78 E 30, 17 N 20. That falls inside "
            "the 07:57 to 09:36 window Chart 53's own diagram implied. The "
            "natural reading is that Examples 104 and 105 are the bride and "
            "the groom of one wedding; the book never says so."
        ),
    },
    53: {
        "title": "A lady, and her wedding-day transit — Example 104",
        "birth": "July 26, 1973, 9:41 pm (IST), 80 E 28, 16 N 13",
        "birth_data": {
            "year": 1973, "month": 7, "day": 26, "hour": 21, "minute": 41,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 13 / 60, "longitude": 80 + 28 / 60},
        "longitudes": {
            "Asc": "3 Pi 18", "Sun": "10 Cn 01", "Moon": "26 Ta 39",
            "Mars": "28 Pi 12", "Merc": "0 Cn 13", "Jup": "14 Cp 12",
            "Ven": "8 Le 25", "Sat": "5 Ge 48", "Rahu": "12 Sg 48",
            "Ketu": "12 Ge 48", "HL": "6 Sc 15", "GL": "1 Sc 32",
        },
        "chara_karakas": {
            "Mars": "AK", "Moon": "AmK", "Rahu": "BK", "Merc": "DK",
            "Sat": "GK", "Jup": "MK", "Sun": "PiK", "Ven": "PK",
        },
        "retrograde": ("Merc", "Jup"),
        "drawn": {
            "Mars": "Pi", "Asc": "Pi", "Moon": "Ta", "Ketu": "Ge",
            "Sat": "Ge", "Merc": "Cn", "Sun": "Cn", "Ven": "Le",
            "GL": "Sc", "HL": "Sc", "AL": "Sc", "Rahu": "Sg", "Jup": "Cp",
        },
        "sahams": {"vivaha": "1 Cp"},
        "transit": {
            "for": "the wedding",
            "date": "January 24, 1999 — no time given",
            "drawn": {
                "Jup": "Pi", "Sat": "Ar", "Moon": "Ar", "AL": "Ge",
                "Rahu": "Cn", "Mars": "Li", "Merc": "Cp", "Sun": "Cp",
                "Ketu": "Cp", "Ven": "Aq", "Asc": "Aq",
            },
        },
        "events": {"the lady married": "January 24, 1999"},
        "first_seen": "chapter 25, Example 104",
        "note": (
            "One number, two charts: the nativity and the transit chart for "
            "her wedding day. The nativity recomputes within an arcminute. "
            "The transit chart gives a date and no time, and its own diagram "
            "pins one: the Moon reaches Aries and the Ascendant Aquarius "
            "together only between about **07:57 and 09:36 IST**, where its "
            "AL also comes out Gemini as drawn. It carries the register's "
            "first printed **saham** -- vivaha saham at 1 Cp -- which we "
            "cannot compute, sahams being deferred to the Tajaka part, so it "
            "is held as a fixture for when that part arrives. See OI-116."
        ),
    },
    52: {
        "title": "Transit chart, June 7 1999 — Example 103",
        "birth": "June 7, 1999 — a transit chart; no time and no place given",
        "kind": "transit",
        "drawn": {
            "GL": "Pi", "Sat": "Ar", "Jup": "Ar", "Sun": "Ta", "Merc": "Ge",
            "Rahu": "Cn", "Ven": "Cn", "Asc": "Vi", "Mars": "Li", "AL": "Sg",
            "Ketu": "Cp", "HL": "Aq", "Moon": "Aq",
        },
        "first_seen": "chapter 25, Example 103",
        "note": (
            "The register's first **transit** chart: a date and a diagram, no "
            "birth data, because it is nobody's nativity. All nine grahas "
            "reproduce for **any** time on 7 June 1999 -- the Moon included, "
            "which stays in Aquarius the whole day. The Ascendant, AL, HL and "
            "GL need a moment and a place, and the diagram pins them: at 17 N "
            "78 E all four land together only between about **14:14 and "
            "14:37 IST**. The place is our assumption, so the window is "
            "indicative; what it shows is that the four are mutually "
            "consistent and that our HL and GL reach them, which OI-103 gave "
            "reason to doubt."
        ),
    },
    51: {
        "title": "Bill Cosby, D-10 — Exercise 37",
        "birth": "July 12, 1937, 12:30 am (5:00 West), 75 W 10, 39 N 57",
        "birth_data": {
            "year": 1937, "month": 7, "day": 12, "hour": 0, "minute": 30,
            "second": 0.0, "utc_offset_hours": -5.0,
        },
        "place": {"latitude": 39 + 57 / 60, "longitude": -(75 + 10 / 60)},
        "longitudes": {
            "Asc": "20 Ar 14", "Sun": "26 Ge 29", "Moon": "19 Le 28",
            "Mars": "28 Li 00", "Merc": "0 Cn 57", "Jup": "29 Sg 51",
            "Ven": "11 Ta 30", "Sat": "12 Pi 09", "Rahu": "20 Sc 24",
            "Ketu": "20 Ta 24", "HL": "19 Aq 33", "GL": "10 Le 20",
        },
        "chara_karakas": {
            "Jup": "AK", "Mars": "AmK", "Sun": "BK", "Merc": "DK",
            "Rahu": "GK", "Moon": "MK", "Sat": "PiK", "Ven": "PK",
        },
        "retrograde": ("Jup",),
        "divisional": {
            "D10": {
                "Sat": "Pi", "Merc": "Pi", "Ven": "Ar", "Ketu": "Cn",
                "Mars": "Cn", "AL": "Cn", "HL": "Le", "Jup": "Vi",
                "Asc": "Li", "GL": "Sc", "Rahu": "Cp", "Moon": "Aq",
                "Sun": "Aq",
            },
        },
        "sav": {
            "D10": {"Ar": 24, "Ta": 28, "Ge": 21, "Cn": 38, "Le": 34,
                    "Vi": 21, "Li": 26, "Sc": 26, "Sg": 37, "Cp": 31,
                    "Aq": 25, "Pi": 26},
        },
        "events": {
            "came to limelight in the TV serial \"I Spy\"": "1965",
            "won the Emmy Award for best actor": "1966, 1967 and 1968",
            "Cn dasa": "1964-1984",
        },
        "first_seen": "chapter 24, Exercise 37",
        "note": (
            "Bill Cosby, named in the answer. The only chart in the register "
            "whose **whole** SAV is printed, all twelve signs, and every one "
            "reproduces. Like Charts 49 and 50 it sits about 1.9' below the "
            "ayanamsa the other forty charts share -- see D-69."
        ),
    },
    50: {
        "title": "Divorced Lady — Exercise 36",
        "birth": "May 21, 1968, 11:05 pm (IST), 78 E 10, 18 N 40",
        "birth_data": {
            "year": 1968, "month": 5, "day": 21, "hour": 23, "minute": 5,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 18 + 40 / 60, "longitude": 78 + 10 / 60},
        "longitudes": {
            "Asc": "8 Cp 44", "Sun": "7 Ta 19", "Moon": "6 Pi 17",
            "Mars": "15 Ta 48", "Merc": "29 Ta 41", "Jup": "3 Le 45",
            "Ven": "29 Ar 17", "Sat": "27 Pi 33", "Rahu": "23 Pi 06",
            "Ketu": "23 Vi 06", "HL": "18 Li 01", "GL": "20 Sg 06",
        },
        "chara_karakas": {
            "Merc": "AK", "Ven": "AmK", "Sat": "BK", "Jup": "DK",
            "Moon": "GK", "Mars": "MK", "Sun": "PiK", "Rahu": "PK",
        },
        "drawn": {
            "Sat": "Pi", "Moon": "Pi", "Rahu": "Pi", "Ven": "Ar",
            "Mars": "Ta", "Sun": "Ta", "Merc": "Ta", "AL": "Ta",
            "Jup": "Le", "Ketu": "Vi", "HL": "Li", "GL": "Sg", "Asc": "Cp",
        },
        "divisional": {
            "D9": {
                "Sun": "Pi", "Asc": "Pi", "HL": "Pi", "Sat": "Pi",
                "Jup": "Ta", "Mars": "Ta", "AL": "Cn", "Ketu": "Cn",
                "Moon": "Le", "Merc": "Vi", "GL": "Li", "Ven": "Sg",
                "Rahu": "Cp",
            },
        },
        "events": {
            "the lady married": "February 1992",
            "the lady divorced": "late 1995",
        },
        "first_seen": "chapter 24, Exercise 36",
        "note": (
            "Both diagrams reproduce from the printed longitudes, but the "
            "ephemeris sits **0.8' to 1.75' below** every printed body -- the "
            "same signature as Chart 49 and outside the arcminute every other "
            "chart meets. Its Moon is in **Uttarabhadrapada**, the nakshatra "
            "D-67 says no savya sub-group table names, and the exercise's own "
            "dasa settles which table it belongs to: see OI-139."
        ),
    },
    49: {
        "title": "ISKCON devotee, D-20 — Example 102",
        "birth": "January 26, 1971, 10:43 am (3:00 East), 24 E 01, 49 N 49",
        "birth_data": {
            "year": 1971, "month": 1, "day": 26, "hour": 10, "minute": 43,
            "second": 0.0, "utc_offset_hours": 3.0,
        },
        "place": {"latitude": 49 + 49 / 60, "longitude": 24 + 1 / 60},
        "longitudes": {
            "Asc": "24 Aq 49", "Sun": "12 Cp 16", "Moon": "3 Cp 35",
            "Mars": "8 Sc 37", "Merc": "19 Sg 10", "Jup": "8 Sc 30",
            "Ven": "25 Sc 31", "Sat": "22 Ar 20", "Rahu": "1 Aq 11",
            "Ketu": "1 Le 11", "HL": "28 Aq 51", "GL": "8 Ta 49",
        },
        "chara_karakas": {
            "Rahu": "AK", "Ven": "AmK", "Sat": "BK", "Merc": "MK",
            "Sun": "PiK", "Mars": "PK", "Jup": "GK", "Moon": "DK",
        },
        "divisional": {
            "D20": {
                "Asc": "Ar", "Jup": "Ta", "Mars": "Ta", "GL": "Ta",
                "Ven": "Ta", "Sat": "Ge", "Moon": "Ge", "AL": "Ge",
                "HL": "Cn", "Merc": "Le", "Rahu": "Sg", "Sun": "Sg",
                "Ketu": "Sg",
            },
        },
        "sav_strongest": {"D20": {"Ar": 33, "Pi": 33, "Ge": 31, "Li": 30}},
        "events": {
            "left mathematics, wandered in the forests, found ISKCON and "
            "moved to a monastery": "1990",
        },
        "first_seen": "chapter 24, Example 102",
        "note": (
            "The same nativity as Chart 37, **cast differently**: one minute "
            "earlier, 10:43 against 10:44, and every graha 1' to 2' further "
            "on, which is an ayanamsa difference of about 1.5'. Our settings "
            "reproduce Chart 37 within an arcminute and are 1' to 1.8' below "
            "Chart 49. The difference is not cosmetic -- the two sets give "
            "different D-20 signs for Venus and GL, and only Chart 49's own "
            "longitudes give the D-20 SAV figures Example 102 quotes."
        ),
    },
    48: {
        "title": "A gentleman — Example 100",
        "birth": "July 15, 1933, 4:15 am (IST), 80 E 55, 16 N 05",
        "birth_data": {
            "year": 1933, "month": 7, "day": 15, "hour": 4, "minute": 15,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 5 / 60, "longitude": 80 + 55 / 60},
        "longitudes": {
            "Asc": "8 Ge 37", "Sun": "29 Ge 03", "Moon": "3 Ar 58",
            "Mars": "11 Vi 29", "Merc": "20 Cn 17", "Jup": "26 Le 05",
            "Ven": "21 Cn 34", "Sat": "21 Cp 40", "Rahu": "7 Aq 39",
            "Ketu": "7 Le 39", "HL": "14 Ta 48", "GL": "9 Pi 46",
        },
        "chara_karakas": {
            "Sun": "AK", "Jup": "AmK", "Rahu": "BK", "Moon": "DK",
            "Mars": "GK", "Sat": "MK", "Merc": "PK", "Ven": "PiK",
        },
        "retrograde": ("Sat",),
        "divisional": {
            "D12": {
                "Ven": "Pi", "Merc": "Pi", "Moon": "Ta", "Sun": "Ta",
                "Rahu": "Ta", "GL": "Ge", "Jup": "Ge", "AL": "Ge",
                "Sat": "Vi", "Asc": "Vi", "HL": "Li", "Ketu": "Sc",
                "Mars": "Cp",
            },
        },
        "events": {
            "the native's father passed away": "1967",
            "the native's mother died": "not dated; in Li-Li antardasa",
        },
        "first_seen": "chapter 24, Example 100",
        "note": (
            "A new native, and the first at 80 E 55, 16 N 05. Only the D-12 "
            "is drawn. Its Kalachakra dasa is the first dated event in the "
            "book that separates OI-115's year lengths: Cn dasa opens in "
            "September 1966 under savana years and in March 1967 under a "
            "solar year, and the example says September 1966."
        ),
    },
    47: {
        "title": "An astrologer — Example 99",
        "birth": "April 4, 1970, 5:50 pm (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "14 Vi 52", "Sun": "20 Pi 52", "Moon": "28 Aq 35",
            "Mars": "26 Ar 40", "Merc": "3 Ar 07", "Jup": "9 Li 45",
            "Ven": "7 Ar 55", "Sat": "15 Ar 06", "Rahu": "16 Aq 53",
            "Ketu": "16 Le 53", "HL": "15 Pi 42", "GL": "8 Vi 40",
        },
        "chara_karakas": {
            "Moon": "AK", "Mars": "AmK", "Sun": "BK", "Sat": "MK",
            "Rahu": "PiK", "Jup": "PK", "Ven": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "divisional": {
            "D24": {
                "Jup": "Pi", "Mars": "Ta", "Moon": "Ge", "Asc": "Ge",
                "HL": "Cn", "Sat": "Le", "Ketu": "Vi", "Rahu": "Vi",
                "Merc": "Li", "Sun": "Sc", "GL": "Cp", "Ven": "Aq",
                "AL": "Aq",
            },
        },
        "sav_strongest": {"D24": {"Le": 36, "Ge": 34, "Pi": 33}},
        "events": {
            "seriously into astrology since": "1993",
            "a very fruitful period for knowledge": "1996-2000",
        },
        "first_seen": "chapter 24, Example 99",
        "note": (
            "The **third** printing of the native of Charts 27 and 33 -- same "
            "birth data, longitudes and chara karakas. Chart 27 drew the D-4, "
            "Chart 33 the D-16 and Chart 47 the D-24, so between them the "
            "register now holds three vargas of one chart and no rasi "
            "diagram. Example 99 is the only worked SAV of a divisional "
            "chart: Le 36, Ge 34 and Pi 33 rekhas, and nothing else over 30."
        ),
    },
    46: {
        "title": "A male who married in Dec 1994 — Example 98",
        "birth": "May 9, 1971, 9:22 am (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1971, "month": 5, "day": 9, "hour": 9, "minute": 22,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "18 Ge 07", "Sun": "24 Ar 26", "Moon": "9 Li 29",
            "Mars": "9 Cp 14", "Merc": "0 Ar 58", "Jup": "9 Sc 53",
            "Ven": "25 Pi 13", "Sat": "1 Ta 24", "Rahu": "25 Cp 42",
            "Ketu": "25 Cn 42", "HL": "16 Le 16", "GL": "4 Aq 14",
        },
        "chara_karakas": {
            "Ven": "AK", "Sun": "AmK", "Jup": "BK", "Moon": "MK",
            "Mars": "PiK", "Rahu": "PK", "Sat": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "divisional": {
            "D9": {
                "Mars": "Pi", "Asc": "Pi", "Merc": "Ar",
                "Ketu": "Aq", "Ven": "Aq", "Sat": "Cp",
                "AL": "Sg", "Moon": "Sg", "GL": "Sc", "Sun": "Sc",
                "Jup": "Vi", "HL": "Le", "Rahu": "Le",
            },
        },
        "events": {
            "the native got married": "December 1994",
            "a love affair with the lady he was to marry": "Aq dasa, 1990-1994",
        },
        "first_seen": "chapter 24, Example 98",
        "note": (
            "The same native as Chart 44, to the printed arcminute -- same "
            "birth data, same twelve longitudes, same eight chara karakas. "
            "Chart 44 drew the rasi chart for a Pitri Shoola dasa; Chart 46 "
            "draws the **navamsa**, which is what Example 98 reads. The rasi "
            "positions are printed below both diagrams and are not redrawn."
        ),
    },
    45: {
        "title": "A lady — Exercise 33",
        "birth": "born in 1950",
        "drawn": {
            "Rahu": "Pi", "Moon": "Pi", "AL": "Aq",
            "Jup": "Cp", "Sun": "Cp", "Ven": "Cp", "Sat": "Le",
            "Merc": "Sg", "Asc": "Sg", "HL": "Sg",
            "GL": "Li", "Ketu": "Vi", "Mars": "Vi",
        },
        "retrograde": ("Ven", "Sat", "Merc"),
        "events": {"her husband died in a road accident": "2000"},
        "first_seen": "chapter 23, Exercise 33",
        "note": (
            "The first chart in the register printed with **no degrees at "
            "all** -- only the two diagrams and the year. Nothing that needs "
            "a longitude can be computed on it, which rules out section "
            "15.5.2 below rule 1, the arudha padas' co-lord tiebreaks and "
            "every varga. The exercise asks only for rasi-level work, and its "
            "seed is settled by rule 1."
        ),
    },
    44: {
        "title": "Pitri Shoola Example — Example 93",
        "birth": "May 9, 1971, 9:22 am (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1971, "month": 5, "day": 9, "hour": 9, "minute": 22,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "18 Ge 07", "Sun": "24 Ar 26", "Moon": "9 Li 29",
            "Mars": "9 Cp 14", "Merc": "0 Ar 58", "Jup": "9 Sc 53",
            "Ven": "25 Pi 13", "Sat": "1 Ta 24", "Rahu": "25 Cp 42",
            "Ketu": "25 Cn 42", "HL": "16 Le 16", "GL": "4 Aq 14",
        },
        "chara_karakas": {
            "Ven": "AK", "Sun": "AmK", "Jup": "BK", "Moon": "MK",
            "Mars": "PiK", "Rahu": "PK", "Sat": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "drawn": {
            "Ven": "Pi", "Merc": "Ar", "Sun": "Ar", "Sat": "Ta", "Asc": "Ge",
            "AL": "Aq", "GL": "Aq", "Ketu": "Cn",
            "Rahu": "Cp", "Mars": "Cp", "HL": "Le",
            "Jup": "Sc", "Moon": "Li",
        },
        "events": {"the native's father died": "second half of 1995"},
        "first_seen": "chapter 23, Example 93",
        "note": (
            "The third chart born at 81 E 12, 16 N 15, after Charts 40 and "
            "41. The only worked Pitri Shoola dasa: it dates a relative's "
            "death rather than the native's, so no longevity category is "
            "computed and the three trines are not narrowed."
        ),
    },
    43: {
        "title": "Shoola dasa exercise — Exercise 32",
        "birth": "December 12, 1915, 3:19 am (5:00 West), 74 W 02, 40 N 45",
        "birth_data": {
            "year": 1915, "month": 12, "day": 12, "hour": 3, "minute": 19,
            "second": 0.0, "utc_offset_hours": -5.0,
        },
        "place": {"latitude": 40 + 45 / 60, "longitude": -(74 + 2 / 60)},
        "longitudes": {
            "Asc": "9 Li 25", "Sun": "26 Sc 33", "Moon": "12 Aq 36",
            "Mars": "4 Le 53", "Merc": "24 Sc 30", "Jup": "27 Aq 11",
            "Ven": "19 Sg 15", "Sat": "22 Ge 10", "Rahu": "18 Cp 06",
            "Ketu": "18 Cn 06", "HL": "29 Cn 46", "GL": "5 Aq 53",
        },
        "chara_karakas": {
            "Jup": "AK", "Sun": "AmK", "Merc": "BK", "Sat": "MK",
            "Ven": "PiK", "Moon": "PK", "Rahu": "GK", "Mars": "DK",
        },
        "retrograde": ("Sat",),
        "drawn": {
            "Sat": "Ge", "Jup": "Aq", "Moon": "Aq", "AL": "Aq", "GL": "Aq",
            "HL": "Cn", "Ketu": "Cn", "Rahu": "Cp", "Mars": "Le",
            "Ven": "Sg", "Merc": "Sc", "Sun": "Sc", "Asc": "Li",
        },
        "events": {"died of a heart attack": "May 14, 1998, aged 82"},
        "first_seen": "chapter 23, Exercise 32",
        "note": (
            "Frank Sinatra, named only in the exercise's answer. The only "
            "chart in either ayur chapter where section 23.3's criterion 1 "
            "has work to do: the AK is Jupiter and it occupies the one trine "
            "from AL inside the longevity range, so the answer moves to the "
            "8th from AL. Born west of the Atlantic, the first such chart "
            "since Chart 12."
        ),
    },
    42: {
        "title": "Niryaana Shoola Exercise — Exercise 31",
        "birth": "April 20, 1889, 6:30 pm (1:00 East), 13 E 02, 48 N 15",
        "birth_data": {
            "year": 1889, "month": 4, "day": 20, "hour": 18, "minute": 30,
            "second": 0.0, "utc_offset_hours": 1.0,
        },
        "place": {"latitude": 48 + 15 / 60, "longitude": 13 + 2 / 60},
        "longitudes": {
            "Asc": "2 Li 56", "Sun": "8 Ar 29", "Moon": "14 Sg 14",
            "Mars": "24 Ar 04", "Merc": "3 Ar 21", "Jup": "15 Sg 56",
            "Ven": "24 Ar 23", "Sat": "21 Cn 09", "Rahu": "23 Ge 45",
            "Ketu": "23 Sg 45", "HL": "16 Ta 57", "GL": "15 Cp 27",
        },
        "chara_karakas": {
            "Ven": "AK", "Mars": "AmK", "Sat": "BK", "Jup": "MK",
            "Moon": "PiK", "Sun": "PK", "Rahu": "GK", "Merc": "DK",
        },
        "retrograde": ("Ven",),
        "drawn": {
            "Mars": "Ar", "Sun": "Ar", "Ven": "Ar", "Merc": "Ar",
            "HL": "Ta", "Rahu": "Ge", "AL": "Cn", "Sat": "Cn",
            "GL": "Cp", "Jup": "Sg", "Moon": "Sg", "Ketu": "Sg",
            "Asc": "Li",
        },
        "events": {"committed suicide": "April 30, 1945, aged 56"},
        "first_seen": "chapter 22, Exercise 31",
        "note": (
            "Adolf Hitler, named only in the exercise's answer. The only "
            "chart in the register whose three longevity pairs all disagree, "
            "which is the case section 14.4 breaks with its preferred pair -- "
            "and the only place the book prints a dasa boundary to the day, "
            "which is what fixes the dasa year at 365.25 days."
        ),
    },
    41: {
        "title": "A gentleman — Niryaana Shoola dasa",
        "birth": "March 14, 1902, 11:48 am (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1902, "month": 3, "day": 14, "hour": 11, "minute": 48,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "1 Ge 51", "Sun": "0 Pi 15", "Moon": "25 Ar 02",
            "Mars": "3 Pi 40", "Merc": "2 Aq 51", "Jup": "15 Cp 12",
            "Ven": "25 Cp 53", "Sat": "2 Cp 57", "Rahu": "14 Li 10",
            "Ketu": "14 Ar 10", "HL": "16 Le 09", "GL": "25 Ar 20",
        },
        "chara_karakas": {
            "Ven": "AK", "Moon": "AmK", "Rahu": "BK", "Jup": "MK",
            "Mars": "PiK", "Sat": "PK", "Merc": "GK", "Sun": "DK",
        },
        "drawn": {
            "Mars": "Pi", "Sun": "Pi", "Ketu": "Ar", "Moon": "Ar", "GL": "Ar",
            "Asc": "Ge", "Merc": "Aq",
            "Ven": "Cp", "Jup": "Cp", "Sat": "Cp", "HL": "Le",
            "AL": "Li", "Rahu": "Li",
        },
        "events": {"passed away": "1967, aged 65"},
        "first_seen": "chapter 22, Example 88",
        "note": (
            "Born at the same place as Chart 40, 25 years earlier. The second "
            "chart to run the Saturn exception, and the first whose Niryaana "
            "Shoola seed is the 8th house rather than the 2nd. Footnote 61's "
            "thumbrule -- any three consecutive dasas total 24 years -- is "
            "stated on this example."
        ),
    },
    40: {
        "title": "A male — Niryaana Shoola dasa, the Saturn exception",
        "birth": "January 20, 1927, 12:30 pm (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1927, "month": 1, "day": 20, "hour": 12, "minute": 30,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "19 Ar 04", "Sun": "6 Cp 24", "Moon": "3 Le 03",
            "Mars": "21 Ar 56", "Merc": "0 Cp 59", "Jup": "7 Aq 34",
            "Ven": "20 Cp 43", "Sat": "12 Sc 15", "Rahu": "13 Ge 07",
            "Ketu": "13 Sg 07", "HL": "2 Cn 18", "GL": "26 Pi 32",
        },
        "chara_karakas": {
            "Mars": "AK", "Ven": "AmK", "Rahu": "BK", "Sat": "MK",
            "Jup": "PiK", "Sun": "PK", "Moon": "GK", "Merc": "DK",
        },
        "drawn": {
            "GL": "Pi", "Mars": "Ar", "Asc": "Ar", "Rahu": "Ge",
            "Jup": "Aq", "HL": "Cn",
            "Merc": "Cp", "Sun": "Cp", "AL": "Cp", "Ven": "Cp",
            "Moon": "Le", "Ketu": "Sg", "Sat": "Sc",
        },
        "events": {"expired": "towards the end of 1949, aged 22"},
        "first_seen": "chapter 22, Example 87",
        "note": (
            "The chart that names the \"Saturn exception\" for Niryaana Shoola "
            "dasa, which section 22.2.1 never states: Saturn in the seed rasi "
            "Scorpio sends the run forward where an even rasi would send it "
            "back. Example 87 also contrasts the three Trishoolas outright -- "
            "death in Cp \"and not in Ta or Vi dasa\" -- which is the clearest "
            "statement of the rule closed OI-132 records."
        ),
    },
    39: {
        "title": "Rajiv Gandhi — Niryaana Shoola dasa",
        "birth": "August 20, 1944, 7:11 am (IST), 72 E 49, 18 N 58",
        "birth_data": {
            "year": 1944, "month": 8, "day": 20, "hour": 7, "minute": 11,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 18 + 58 / 60, "longitude": 72 + 49 / 60},
        "longitudes": {
            "Asc": "14 Le 44", "Sun": "3 Le 49", "Moon": "17 Le 09",
            "Mars": "1 Vi 12", "Merc": "28 Le 34", "Jup": "12 Le 12",
            "Ven": "18 Le 40", "Sat": "14 Ge 13", "Rahu": "2 Cn 48",
            "Ketu": "2 Cp 48", "HL": "29 Le 06", "GL": "7 Li 04",
        },
        "chara_karakas": {
            "Merc": "AK", "Rahu": "AmK", "Ven": "BK", "Moon": "MK",
            "Sat": "PiK", "Jup": "PK", "Sun": "GK", "Mars": "DK",
        },
        "drawn": {
            "AL": "Ta", "Sat": "Ge", "Rahu": "Cn", "Ketu": "Cp",
            "Sun": "Le", "Ven": "Le", "Jup": "Le", "Asc": "Le",
            "Merc": "Le", "HL": "Le", "Moon": "Le",
            "GL": "Li", "Mars": "Vi",
        },
        "events": {"assassinated": "May 1991, aged 46"},
        "first_seen": "chapter 22, Example 85",
        "note": (
            "Seven of the thirteen points printed fall in Leo -- the ascendant, "
            "five grahas and the Horalagna. Example 85 is the one place the "
            "book shows its working for a Niryaana Shoola seed, and it uses "
            "section 15.5.2 rule 1: the 2nd is stronger because a planet "
            "occupies it."
        ),
    },
    38: {
        "title": "Sri Aurobindo Ghose — Drigdasa",
        "birth": "August 15, 1872, 5:17 am (5:53 East), 88 E 20, 22 N 30",
        "birth_data": {
            "year": 1872, "month": 8, "day": 15, "hour": 5, "minute": 17,
            "second": 0.0, "utc_offset_hours": 5 + 53 / 60,
        },
        "place": {"latitude": 22.5, "longitude": 88 + 20 / 60},
        "longitudes": {
            "Asc": "25 Cn 09", "Sun": "0 Le 19", "Moon": "5 Sg 41",
            "Mars": "5 Cn 23", "Merc": "23 Le 30", "Jup": "21 Cn 35",
            "Ven": "8 Le 32", "Sat": "23 Sg 29", "Rahu": "16 Ta 37",
            "Ketu": "16 Sc 37", "HL": "19 Cn 48", "GL": "5 Cn 28",
        },
        "chara_karakas": {
            "Merc": "AK", "Sat": "AmK", "Jup": "BK", "Rahu": "MK",
            "Ven": "PiK", "Moon": "PK", "Mars": "GK", "Sun": "DK",
        },
        "retrograde": ("Sat",),
        "drawn": {
            "AL": "Ta", "Rahu": "Ta",
            "Mars": "Cn", "GL": "Cn", "Asc": "Cn", "HL": "Cn", "Jup": "Cn",
            "Merc": "Le", "Sun": "Le", "Ven": "Le",
            "Sat": "Sg", "Moon": "Sg", "Ketu": "Sc",
        },
        "events": {
            "imprisoned by the British": "1908",
            "released, withdrew from politics and started an aashram in "
            "Pondicherry": "1910",
            "the aashram grew and he became known": "early 1920s",
            "left charge of the aashram to the Mother and retired into "
            "seclusion for yogic sadhana": "1925",
        },
        "first_seen": "chapter 21, Example 83",
        "note": (
            "Born on a 5h53m offset -- Calcutta local time, not a zone -- so "
            "the birth line is not one of the round offsets the other charts "
            "use. Example 83 reads three of its Drigdasas, and two of them "
            "need references section 21.3 never lists: the 7th from AL, and "
            "Ketu's argala rather than Ketu's occupation."
        ),
    },
    37: {
        "title": "ISKCON devotee — Drigdasa",
        "birth": "January 26, 1971, 10:44 am (3:00 East), 24 E 01, 49 N 49",
        "birth_data": {
            "year": 1971, "month": 1, "day": 26, "hour": 10, "minute": 44,
            "second": 0.0, "utc_offset_hours": 3.0,
        },
        "place": {"latitude": 49 + 49 / 60, "longitude": 24 + 1 / 60},
        "longitudes": {
            "Asc": "25 Aq 20", "Sun": "12 Cp 15", "Moon": "3 Cp 34",
            "Mars": "8 Sc 36", "Merc": "19 Sg 08", "Jup": "8 Sc 28",
            "Ven": "25 Sc 29", "Sat": "22 Ar 18", "Rahu": "1 Aq 09",
            "Ketu": "1 Le 09", "HL": "29 Aq 20", "GL": "10 Ta 04",
        },
        "chara_karakas": {
            "Rahu": "AK", "Ven": "AmK", "Sat": "BK", "Merc": "MK",
            "Sun": "PiK", "Mars": "PK", "Jup": "GK", "Moon": "DK",
        },
        "drawn": {
            "Sat": "Ar", "GL": "Ta", "AL": "Ge",
            "Rahu": "Aq", "Asc": "Aq", "HL": "Aq",
            "Moon": "Cp", "Sun": "Cp", "Ketu": "Le",
            "Merc": "Sg", "Jup": "Sc", "Mars": "Sc", "Ven": "Sc",
        },
        "events": {
            "left mathematics at a Russian university, wandered in the "
            "forests, found ISKCON and moved to a monastery": "1990",
        },
        "first_seen": "chapter 21, Example 82",
        "note": (
            "The Drigdasa chart whose three group leaders are all "
            "odd-footed, so all three groups run forward -- the opposite "
            "extreme from Chart 36, which runs one forward and two backward. "
            "Aquarius lagna puts the 9th in movable Libra, so the groups "
            "cover the zodiac and OI-127's overlap does not arise. No "
            "retrogression is marked on any graha."
        ),
    },
    36: {
        "title": "A gentleman — Drigdasa",
        "birth": "not given",
        "longitudes": {
            "Asc": "2 Li 08", "Sun": "9 Vi 06", "Moon": "9 Cp 39",
            "Mars": "15 Vi 08", "Merc": "4 Li 18", "Jup": "16 Aq 49",
            "Ven": "28 Le 23", "Sat": "24 Ge 15", "Rahu": "20 Sc 13",
            "Ketu": "20 Ta 13", "HL": "28 Li 43", "GL": "13 Cp 15",
        },
        "chara_karakas": {
            "Ven": "AK", "Sat": "AmK", "Jup": "BK", "Mars": "MK",
            "Rahu": "PiK", "Moon": "PK", "Sun": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "drawn": {
            "Ketu": "Ta", "AL": "Ge", "Sat": "Ge", "Jup": "Aq",
            "GL": "Cp", "Moon": "Cp", "Ven": "Le", "Rahu": "Sc",
            "Merc": "Li", "Asc": "Li", "HL": "Li", "Mars": "Vi", "Sun": "Vi",
        },
        "first_seen": "chapter 21, Example 80",
        "note": (
            "Not recomputable: the chart is printed with no birth line at "
            "all, only the diagram and the longitudes. Example 80 spells out "
            "the walk inside a Drigdasa group -- go round the zodiac from the "
            "leader and pick up the signs that aspect it -- which section "
            "21.2 leaves to be read."
        ),
    },
    35: {
        "title": "Jayalalita — Sudasa",
        "birth": "February 24, 1948, 2:36 pm (IST), 80 E 18, 13 N 05",
        "birth_data": {
            "year": 1948, "month": 2, "day": 24, "hour": 14, "minute": 36,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 13 + 5 / 60, "longitude": 80 + 18 / 60},
        "longitudes": {
            "Asc": "21 Ge 19", "Sun": "11 Aq 33", "Moon": "6 Le 42",
            "Mars": "2 Le 09", "Merc": "2 Aq 40", "Jup": "2 Sg 01",
            "Ven": "21 Pi 51", "Sat": "24 Cn 53", "Rahu": "24 Ar 48",
            "Ketu": "24 Li 48", "HL": "15 Li 06", "GL": "20 Li 56",
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Sun": "BK", "Moon": "MK",
            "Rahu": "PiK", "Merc": "PK", "Mars": "GK", "Jup": "DK",
        },
        "retrograde": ("Merc", "Mars", "Sat"),
        "drawn": {
            "Ven": "Pi", "Rahu": "Ar", "Asc": "Ge", "Merc": "Aq", "Sun": "Aq",
            "Sat": "Cn", "Mars": "Le", "Moon": "Le", "Jup": "Sg",
            "HL": "Li", "Ketu": "Li", "AL": "Li", "GL": "Li",
        },
        "events": {"Chief Minister of Tamil Nadu": "1991 to 1996"},
        "first_seen": "chapter 20, Example 79",
        "note": (
            "Libra holds HL, GL and AL together, so one Sudasa reaches all "
            "three of section 20.3's readings at once -- wealth from HL, "
            "power from GL, status from AL. No other chart in the book puts "
            "the three special points in one rasi."
        ),
    },
    34: {
        "title": "Ronald Reagan — Lagna Kendradi Rasi Dasa",
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
        "drawn": {
            "Sat": "Ar", "Moon": "Ar", "Rahu": "Ar", "Ven": "Aq", "Sun": "Cp",
            "HL": "Le", "Merc": "Sg", "Mars": "Sg", "GL": "Sg", "Asc": "Sc",
            "Ketu": "Li", "Jup": "Li", "AL": "Vi",
        },
        "events": {
            "President of the United States": "January 1981 to January 1989",
            "shot": "30 March 1981",
            "died": "5 June 2004",
        },
        "first_seen": "chapter 19, Example 76",
        "note": (
            "Chart 7 re-printed. The book gives Reagan a second number for "
            "chapter 19 without changing a figure, so both entries carry the "
            "same twelve longitudes and a test pins them equal."
        ),
    },
    33: {
        "title": "Accident example — D-16 Narayana dasa",
        "birth": "April 4, 1970, 5:50 pm (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "14 Vi 52", "Sun": "20 Pi 52", "Moon": "28 Aq 35",
            "Mars": "26 Ar 40", "Merc": "3 Ar 07", "Jup": "9 Li 45",
            "Ven": "7 Ar 55", "Sat": "15 Ar 06", "Rahu": "16 Aq 53",
            "Ketu": "16 Le 53", "HL": "15 Pi 42", "GL": "8 Vi 40",
        },
        "chara_karakas": {
            "Moon": "AK", "Mars": "AmK", "Sun": "BK", "Sat": "MK",
            "Rahu": "PiK", "Jup": "PK", "Ven": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "divisional": {
            "D16": {
                "Asc": "Cn", "Sun": "Sc", "Moon": "Sc", "Mars": "Ge",
                "Merc": "Ta", "Jup": "Vi", "Ven": "Le", "Sat": "Sg",
                "Rahu": "Ta", "Ketu": "Ta", "HL": "Le", "GL": "Ar",
                "AL": "Pi",
            },
        },
        "events": {"vehicular accident": "December 1996"},
        "first_seen": "chapter 18, Example 75",
        "note": (
            "The same native as Chart 27, to the arcsecond -- the book draws "
            "him twice, in D-4 for Example 71's foreign stay and in D-16 "
            "here for a vehicle. Both nodes fall in Taurus in the D-16, "
            "Aquarius and Leo being both fixed and their degrees identical."
        ),
    },
    32: {
        "title": "A gentleman — Exercise 30, D-10 Narayana dasa",
        "birth": "July 25, 1961, 5:10 pm (IST), 75 E 50, 22 N 44",
        "birth_data": {
            "year": 1961, "month": 7, "day": 25, "hour": 17, "minute": 10,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 22 + 44 / 60, "longitude": 75 + 50 / 60},
        "longitudes": {
            "Asc": "9 Sg 44", "Sun": "8 Cn 57", "Moon": "6 Sg 11",
            "Mars": "22 Le 37", "Merc": "20 Ge 08", "Jup": "8 Cp 54",
            "Ven": "26 Ta 26", "Sat": "2 Cp 46", "Rahu": "5 Le 08",
            "Ketu": "5 Aq 08", "HL": "16 Ge 09", "GL": "12 Sc 37",
        },
        "chara_karakas": {
            "Ven": "AK", "Rahu": "AmK", "Mars": "BK", "Merc": "MK",
            "Sun": "PiK", "Jup": "PK", "Moon": "GK", "Sat": "DK",
        },
        "retrograde": ("Jup", "Sat"),
        "divisional": {
            "D10": {
                "Asc": "Pi", "Sun": "Ta", "Moon": "Aq", "Mars": "Pi",
                "Merc": "Sg", "Jup": "Sc", "Ven": "Vi", "Sat": "Vi",
                "Rahu": "Vi", "Ketu": "Pi", "HL": "Sc", "GL": "Sc",
                "AL": "Cn",
            },
        },
        "first_seen": "chapter 18, Exercise 30",
        "note": (
            "Its chara karakas turn on nine arcminutes -- the Sun at 8.950 "
            "degrees of advancement takes PiK from Jupiter at 8.900, which "
            "the printed labels confirm."
        ),
    },
    31: {
        "title": "An electrical engineer — D-10 Narayana dasa",
        "birth": "September 7, 1947, 6:00 pm (IST), 80 E 30, 15 N 54",
        "birth_data": {
            "year": 1947, "month": 9, "day": 7, "hour": 18, "minute": 0,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 15 + 54 / 60, "longitude": 80.5},
        "longitudes": {
            "Asc": "16 Aq 50", "Sun": "20 Le 55", "Moon": "12 Ta 40",
            "Mars": "22 Ge 40", "Merc": "29 Le 21", "Jup": "28 Li 35",
            "Ven": "21 Le 59", "Sat": "23 Cn 25", "Rahu": "3 Ta 48",
            "Ketu": "3 Sc 48", "HL": "22 Le 37", "GL": "25 Aq 56",
        },
        "chara_karakas": {
            "Merc": "AK", "Jup": "AmK", "Rahu": "BK", "Sat": "MK",
            "Mars": "PiK", "Ven": "PK", "Sun": "GK", "Moon": "DK",
        },
        "divisional": {
            "D10": {
                "Asc": "Cn", "Sun": "Aq", "Moon": "Ta", "Mars": "Cp",
                "Merc": "Ta", "Jup": "Cn", "Ven": "Pi", "Sat": "Li",
                "Rahu": "Aq", "Ketu": "Le", "HL": "Pi", "GL": "Li",
                "AL": "Pi",
            },
        },
        "events": {"suspended from his job": "1994 to 1996"},
        "first_seen": "chapter 18, Example 74",
        "note": (
            "The chart that confirms OI-123 outright: its D-10 lagna Cn, its "
            "seed house rasi Sc, its derived lagna Cp and its rasi lagna Aq "
            "are four different signs, and only the D-10's own lagna makes "
            "Aq the 8th house the example calls it. Also the first real use "
            "of section 18.4's thirds, which date the event."
        ),
    },
    30: {
        "title": "A lady — Exercise 29, a marriage ended",
        "birth": "June 3, 1976",
        "longitudes": {
            "Asc": "0 Sc 39", "Sun": "19 Ta 29", "Moon": "23 Cn 39",
            "Mars": "16 Cn 42", "Merc": "1 Ta 29", "Jup": "22 Ar 43",
            "Ven": "15 Ta 29", "Sat": "6 Cn 17", "Rahu": "17 Li 33",
            "Ketu": "17 Ar 33", "HL": "6 Ta 24", "GL": "17 Li 30",
        },
        "chara_karakas": {
            "Moon": "AK", "Jup": "AmK", "Sun": "BK", "Mars": "MK",
            "Ven": "PiK", "Rahu": "PK", "Sat": "GK", "Merc": "DK",
        },
        "divisional": {
            "D9": {
                "Asc": "Cn", "Sun": "Ge", "Moon": "Aq", "Mars": "Sg",
                "Merc": "Cp", "Jup": "Li", "Ven": "Ta", "Sat": "Le",
                "Rahu": "Pi", "Ketu": "Vi", "HL": "Aq", "GL": "Pi",
                "AL": "Vi", "UL": "Le",
            },
        },
        "events": {"marriage ended": "early June 2000"},
        "first_seen": "chapter 18, Exercise 29",
        "note": (
            "Not recomputable: the chart gives a date and nothing else -- no "
            "time, no place. The dasas still date from 3 June 1976, which is "
            "enough for the exercise. Both diagrams are the navamsa, and it "
            "draws the upapada, as Chart 29 does."
        ),
    },
    29: {
        "title": "A lady — navamsa Narayana dasa, marriage",
        "birth": "July 8, 1969, 10:47 am (IST), 82 E 15, 16 N 57",
        "birth_data": {
            "year": 1969, "month": 7, "day": 8, "hour": 10, "minute": 47,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 57 / 60, "longitude": 82 + 15 / 60},
        "longitudes": {
            "Asc": "4 Vi 08", "Sun": "22 Ge 26", "Moon": "11 Ar 59",
            "Mars": "8 Sc 16", "Merc": "6 Ge 40", "Jup": "5 Vi 37",
            "Ven": "7 Ta 57", "Sat": "13 Ar 53", "Rahu": "1 Pi 12",
            "Ketu": "1 Vi 12", "HL": "29 Sc 10", "GL": "24 Cn 34",
        },
        "chara_karakas": {
            "Rahu": "AK", "Sun": "AmK", "Sat": "BK", "Moon": "MK",
            "Mars": "PiK", "Ven": "PK", "Merc": "GK", "Jup": "DK",
        },
        "retrograde": ("Mars",),
        "divisional": {
            "D9": {
                "Asc": "Aq", "Sun": "Ar", "Moon": "Cn", "Mars": "Vi",
                "Merc": "Sg", "Jup": "Aq", "Ven": "Pi", "Sat": "Le",
                "Rahu": "Cn", "Ketu": "Cp", "HL": "Pi", "GL": "Aq",
                "AL": "Sg", "UL": "Pi",
            },
        },
        "events": {"married": "May 1989"},
        "first_seen": "chapter 18, Example 73",
        "note": (
            "The first varga Narayana dasa seeded from the 7th: the derived "
            "lagna is Pi and the dasas run from Vi. The only chart in the "
            "book whose diagram draws the upapada, and the example uses it "
            "throughout. Section 15.5.1's cascade is walked in print for "
            "Scorpio -- \"Mars' count of 2 beats Ketu's count of 1\"."
        ),
    },
    28: {
        "title": "A lady — navamsa Narayana dasa",
        "birth": "September 12, 1971, 8:25 am (IST), 80 E 23, 16 N 13",
        "birth_data": {
            "year": 1971, "month": 9, "day": 12, "hour": 8, "minute": 25,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 13 / 60, "longitude": 80 + 23 / 60},
        "longitudes": {
            "Asc": "0 Li 12", "Sun": "25 Le 14", "Moon": "29 Ta 39",
            "Mars": "18 Cp 28", "Merc": "7 Le 18", "Jup": "6 Sc 36",
            "Ven": "29 Le 25", "Sat": "13 Ta 01", "Rahu": "19 Cp 02",
            "Ketu": "19 Cn 02", "HL": "9 Sc 26", "GL": "0 Pi 52",
        },
        "chara_karakas": {
            "Moon": "AK", "Ven": "AmK", "Sun": "BK", "Mars": "MK",
            "Sat": "PiK", "Rahu": "PK", "Merc": "GK", "Jup": "DK",
        },
        "divisional": {
            "D9": {
                "Asc": "Li", "Sun": "Sc", "Moon": "Vi", "Mars": "Ge",
                "Merc": "Ge", "Jup": "Le", "Ven": "Sg", "Sat": "Ar",
                "Rahu": "Ge", "Ketu": "Sg", "HL": "Vi", "GL": "Cn",
                "AL": "Aq",
            },
        },
        "events": {"married": "August 1993"},
        "first_seen": "chapter 18, Example 72",
        "note": (
            "The second chart drawn as a varga rather than a rasi chart -- "
            "both diagrams are the navamsa. It closes OI-123: the D-9's own "
            "lagna is Li while the seed house rasi is Ge, and the example "
            "says \"Here Li is lagna\"."
        ),
    },
    27: {
        "title": "Foreign Stay Example",
        "birth": "April 4, 1970, 5:50 pm (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "14 Vi 52", "Sun": "20 Pi 52", "Moon": "28 Aq 35",
            "Mars": "26 Ar 40", "Merc": "3 Ar 07", "Jup": "9 Li 45",
            "Ven": "7 Ar 55", "Sat": "15 Ar 06", "Rahu": "16 Aq 53",
            "Ketu": "16 Le 53", "HL": "15 Pi 42", "GL": "8 Vi 40",
        },
        "chara_karakas": {
            "Moon": "AK", "Mars": "AmK", "Sun": "BK", "Sat": "MK",
            "Rahu": "PiK", "Jup": "PK", "Ven": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "divisional": {
            "D4": {
                "Asc": "Sg", "Sun": "Vi", "Moon": "Sc", "Mars": "Cp",
                "Merc": "Ar", "Jup": "Cp", "Ven": "Cn", "Sat": "Li",
                "Rahu": "Le", "Ketu": "Aq", "HL": "Vi", "GL": "Sg",
                "AL": "Aq",
            },
        },
        "events": {"moved to the US for higher studies": "15 August 1991"},
        "first_seen": "chapter 18, Example 71",
        "note": (
            "The only chart in the book drawn as a varga rather than a rasi "
            "chart -- both diagrams are the D-4, and the longitudes beneath "
            "them are the rasi chart's. Its Sagittarius dasa of zero years "
            "closes OI-121: the book prints the zero and gives the rasi 12 "
            "years in the second cycle."
        ),
    },
    26: {
        "title": "Narayana Dasa Exercise",
        "birth": "May 9, 1971, 9:20 am (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1971, "month": 5, "day": 9, "hour": 9, "minute": 20,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "17 Ge 40", "Sun": "24 Ar 26", "Moon": "9 Li 28",
            "Mars": "9 Cp 14", "Merc": "0 Ar 58", "Jup": "9 Sc 53",
            "Ven": "25 Pi 13", "Sat": "1 Ta 24", "Rahu": "25 Cp 42",
            "Ketu": "25 Cn 42", "HL": "15 Le 14", "GL": "1 Aq 40",
        },
        "chara_karakas": {
            "Ven": "AK", "Sun": "AmK", "Jup": "BK", "Moon": "MK",
            "Mars": "PiK", "Rahu": "PK", "Sat": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "drawn": {
            "Ven": "Pi", "Merc": "Ar", "Sun": "Ar", "Sat": "Ta", "Asc": "Ge",
            "AL": "Aq", "GL": "Aq", "Ketu": "Cn", "Rahu": "Cp", "Mars": "Cp",
            "HL": "Le", "Jup": "Sc", "Moon": "Li",
        },
        "events": {
            "excellent career in India": "until 1997",
            "moved to the US following his wife": "1997",
            "could not find work matching his qualifications": "after 1997",
        },
        "first_seen": "chapter 18, printed with Example 69",
        "note": (
            "Printed in the middle of Example 69's pages but read only by "
            "Exercise 28, which the chart titles itself for. The only chart "
            "in the book whose dasa seed is settled by section 15.5.2's "
            "rule 4: both Ge and Sg are empty and unaspected, so nothing "
            "above it fires."
        ),
    },
    25: {
        "title": "India's independence",
        "birth": "August 15, 1947, 12:00 am (IST), 78 E 30, 27 N 00",
        "birth_data": {
            "year": 1947, "month": 8, "day": 15, "hour": 0, "minute": 0,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 27.0, "longitude": 78.5},
        "longitudes": {
            "Asc": "8 Ta 17", "Sun": "27 Cn 59", "Moon": "3 Cn 59",
            "Mars": "7 Ge 27", "Merc": "13 Cn 41", "Jup": "25 Li 52",
            "Ven": "22 Cn 34", "Sat": "20 Cn 28", "Rahu": "5 Ta 04",
            "Ketu": "5 Sc 04", "HL": "4 Aq 06", "GL": "14 Ta 22",
        },
        "chara_karakas": {
            "Sun": "AK", "Jup": "AmK", "Rahu": "BK", "Ven": "MK",
            "Sat": "PiK", "Merc": "PK", "Mars": "GK", "Moon": "DK",
        },
        "drawn": {
            "Rahu": "Ta", "Asc": "Ta", "GL": "Ta", "Mars": "Ge",
            "Moon": "Cn", "Sat": "Cn", "Sun": "Cn", "Ven": "Cn", "Merc": "Cn",
            "HL": "Aq", "Ketu": "Sc", "Jup": "Li", "AL": "Vi",
        },
        "events": {
            "economy liberalised": "1991",
            "hawala probe": "1996",
            "minority government of the third force": "1996 to 1997",
            "nuclear tests": "May 1998",
        },
        "first_seen": "chapter 18, Example 69",
        "note": (
            "A mundane chart, not a nativity -- the first Narayana dasa the "
            "book works on a nation. It pins section 15.5.1 twice: only "
            "Saturn over Rahu for Aquarius and Mars over Ketu for Scorpio "
            "give the 7-year lengths printed for those two rasis."
        ),
    },
    24: {
        "title": "Bill Gates",
        "birth": "October 28, 1955, 9:18 pm (8:00 West), 122 W 20, 47 N 36",
        "birth_data": {
            "year": 1955, "month": 10, "day": 28, "hour": 21, "minute": 18,
            "second": 0.0, "utc_offset_hours": -8.0,
        },
        "place": {"latitude": 47 + 36 / 60, "longitude": -(122 + 20 / 60)},
        "longitudes": {
            "Asc": "25 Ge 38", "Sun": "11 Li 46", "Moon": "14 Pi 35",
            "Mars": "16 Vi 51", "Merc": "23 Vi 19", "Jup": "4 Le 32",
            "Ven": "26 Li 57", "Sat": "28 Li 21", "Rahu": "26 Sc 13",
            "Ketu": "26 Ta 13", "HL": "26 Sg 41", "GL": "19 Li 57",
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Merc": "BK", "Mars": "MK",
            "Moon": "PiK", "Sun": "PK", "Jup": "GK", "Rahu": "DK",
        },
        "drawn": {
            "Moon": "Pi", "Ketu": "Ta", "Asc": "Ge", "Jup": "Le",
            "HL": "Sg", "Rahu": "Sc", "Ven": "Li", "Sun": "Li", "GL": "Li",
            "Sat": "Li", "Merc": "Vi", "Mars": "Vi", "AL": "Vi",
        },
        "ashtakavarga": {
            "rasi": {
                "Moon": (4, 3, 4, 4, 6, 3, 1, 5, 5, 4, 4, 6),
                "Saturn": (3, 3, 4, 4, 7, 2, 1, 3, 2, 4, 3, 3),
            },
        },
        "sodhya_pindas": {"Moon": 122, "Saturn": 145},
        "events": {
            "a US judge ruled Microsoft a monopoly and ordered a breakup":
                "June 2000 — the month is printed, not the day",
        },
        "first_seen": "chapter 18, Example 68",
        "note": (
            "The first lagna-seeded chart in chapter 18, so the first on "
            "which section 18.4's dasa lagna is the dasa rasi itself. Its "
            "Virgo dasa settles OI-121: Mercury is exalted in his own Virgo, "
            "so exceptions 1 and 2 meet, and the book prints 12 years, not "
            "13. Example 112 returns to it for section 25.6 and prints the "
            "BAVs and sodhya pindas of the Moon and Saturn; all four "
            "reproduce."
        ),
    },
    23: {
        "title": "Dr. B.V. Raman",
        "birth": "August 8, 1912, 7:38 pm (IST), 77 E 35, 13 N 00",
        "birth_data": {
            "year": 1912, "month": 8, "day": 8, "hour": 19, "minute": 38,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 13.0, "longitude": 77 + 35 / 60},
        "longitudes": {
            "Asc": "9 Aq 15", "Sun": "22 Cn 59", "Moon": "23 Ta 38",
            "Mars": "21 Le 22", "Merc": "13 Le 57", "Jup": "12 Sc 58",
            "Ven": "2 Le 15", "Sat": "10 Ta 09", "Rahu": "22 Pi 47",
            "Ketu": "22 Vi 47", "HL": "8 Vi 34", "GL": "17 Ta 45",
        },
        "chara_karakas": {
            "Moon": "AK", "Sun": "AmK", "Mars": "BK", "Merc": "MK",
            "Jup": "PiK", "Sat": "PK", "Rahu": "GK", "Ven": "DK",
        },
        "retrograde": ("Merc",),
        "drawn": {
            "Rahu": "Pi", "Sat": "Ta", "Moon": "Ta", "AL": "Ta", "GL": "Ta",
            "Asc": "Aq", "Sun": "Cn", "Merc": "Le", "Mars": "Le", "Ven": "Le",
            "Jup": "Sc", "HL": "Vi", "Ketu": "Vi",
        },
        "events": {"died": "20 December 1998"},
        "first_seen": "chapter 16, Example 58",
        "note": (
            "The pada rule fires twice here: the Moon's own star and the 8th "
            "star both straddle two signs. Read from the Moon's star the dasa "
            "at death is Venus-Sun; from the 8th star it is Mercury-Rahu. "
            "Both reproduce. The ascendant is 8' out, about half a minute of "
            "birth time. See OI-118: the example calls Venus and Mercury "
            "marakas for occupying the 7th, which section 14.2's rule does "
            "not reach."
        ),
    },
    22: {
        "title": "A lady",
        "birth": "December 7, 1954, 2:13 am (6:00 West), 93 W 15, 44 N 58",
        "birth_data": {
            "year": 1954, "month": 12, "day": 7, "hour": 2, "minute": 13,
            "second": 0.0, "utc_offset_hours": -6.0,
        },
        "place": {"latitude": 44 + 58 / 60, "longitude": -(93 + 15 / 60)},
        "longitudes": {
            "Asc": "18 Vi 35", "Sun": "21 Sc 27", "Moon": "13 Ar 29",
            "Mars": "8 Aq 55", "Merc": "11 Sc 29", "Jup": "6 Cn 02",
            "Ven": "21 Li 28", "Sat": "22 Li 37", "Rahu": "13 Sg 29",
            "Ketu": "13 Ge 29", "HL": "8 Ge 23", "GL": "4 Li 58",
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Sun": "BK", "Rahu": "MK",
            "Moon": "PiK", "Mars": "GK", "Merc": "PK", "Jup": "DK",
        },
        "retrograde": ("Jup",),
        "drawn": {
            "Moon": "Ar", "HL": "Ge", "Ketu": "Ge", "Mars": "Aq",
            "Jup": "Cn", "AL": "Cp", "Rahu": "Sg", "Merc": "Sc",
            "Sun": "Sc", "Sat": "Li", "Ven": "Li", "GL": "Li", "Asc": "Vi",
        },
        "events": {"died": "April 6, 1988"},
        "first_seen": "chapter 16, Example 57",
        "note": (
            "The chart section 16.5.2's ayur path was built for: the Moon's "
            "4th star straddles two signs and its own pada resolves it, and "
            "the section's maraka-aspect criterion is actually applied to "
            "choose between the candidate signs. Read from the Moon's own "
            "star the dasa at death is Moon-Venus; read from the 4th star it "
            "is Jupiter-Venus, the book's answer. Both reproduce."
        ),
    },
    21: {
        "title": "John F. Kennedy, Jr.",
        "birth": "November 25, 1960, 12:22 am (5:00 West), 77 W 02, 38 N 54",
        "birth_data": {
            "year": 1960, "month": 11, "day": 25, "hour": 0, "minute": 22,
            "second": 0.0, "utc_offset_hours": -5.0,
        },
        "place": {"latitude": 38 + 54 / 60, "longitude": -(77 + 2 / 60)},
        "longitudes": {
            "Asc": "18 Le 39", "Sun": "9 Sc 38", "Moon": "4 Aq 06",
            "Mars": "25 Ge 12", "Merc": "19 Li 55", "Jup": "12 Sg 31",
            "Ven": "18 Sg 35", "Sat": "22 Sg 15", "Rahu": "17 Le 58",
            "Ketu": "17 Aq 58", "HL": "19 Ar 11", "GL": "19 Ge 34",
        },
        "chara_karakas": {
            "Mars": "AK", "Sat": "AmK", "Merc": "BK", "Rahu": "PK",
            "Jup": "PiK", "Sun": "GK", "Ven": "MK", "Moon": "DK",
        },
        "retrograde": ("Mars",),
        "drawn": {
            "HL": "Ar", "GL": "Ge", "Mars": "Ge", "Ketu": "Aq", "Moon": "Aq",
            "Rahu": "Le", "Asc": "Le", "Ven": "Sg", "Jup": "Sg", "Sat": "Sg",
            "AL": "Sc", "Sun": "Sc", "Merc": "Li",
        },
        "events": {"died": "the night of July 16, 1999"},
        "first_seen": "chapter 16, Example 56",
        "note": (
            "The first chart in the book to print a Rudra, and it disagrees "
            "with section 14.3's own instruction — see D-53. Every body "
            "recomputes within an arcminute. The example also puts Mercury "
            "in mritya bhaga, a degree table we do not hold; see OI-117."
        ),
    },
    20: {
        "title": "An engineer in USA",
        "birth": "November 12, 1954, 7:52 am (IST), 78 E 50, 12 N 30",
        "birth_data": {
            "year": 1954, "month": 11, "day": 12, "hour": 7, "minute": 52,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 12.5, "longitude": 78 + 50 / 60},
        "longitudes": {
            "Asc": "18 Sc 09", "Sun": "25 Li 56", "Moon": "17 Ta 12",
            "Mars": "21 Cp 12", "Merc": "7 Li 11", "Jup": "6 Cn 40",
            "Ven": "1 Sc 05", "Sat": "19 Li 42", "Rahu": "14 Sg 50",
            "Ketu": "14 Ge 50", "HL": "16 Sg 12", "GL": "1 Pi 43",
        },
        "chara_karakas": {
            "Sun": "AK", "Mars": "AmK", "Sat": "BK", "Merc": "PK",
            "Rahu": "PiK", "Jup": "GK", "Moon": "MK", "Ven": "DK",
        },
        "retrograde": ("Ven",),
        "drawn": {
            "AL": "Pi", "GL": "Pi", "Moon": "Ta", "Ketu": "Ge",
            "Jup": "Cn", "Mars": "Cp", "HL": "Sg", "Rahu": "Sg",
            "Ven": "Sc", "Asc": "Sc", "Merc": "Li", "Sun": "Li",
            "Sat": "Li",
        },
        "events": {
            "wife filed a lawsuit": "end of 1995",
            "evicted, accounts frozen": "December 1995 to February 1996",
            "returned to India": "mid-1996",
            "returned to USA": "1998",
        },
        "first_seen": "chapter 16, Example 55",
        "note": (
            "The one chart where the author records his own prediction "
            "failing. Read from the Moon's star it gives Jupiter-Moon at the "
            "crisis; read from the utpanna star, Pushyami, it gives Venus "
            "dasa with Rahu antardasa, which is the reading the example "
            "keeps. Both reproduce. See also D-51: the example calls Venus "
            "the lagna lord and later calls Ketu the lagna lord; Ketu is "
            "right."
        ),
    },
    19: {
        "title": "Sri Navin Patnaik",
        "birth": "October 16, 1946, 12:58 am (IST), 85 E 50, 20 N 30",
        "birth_data": {
            "year": 1946, "month": 10, "day": 16, "hour": 0, "minute": 58,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 20 + 30 / 60, "longitude": 85 + 50 / 60},
        "longitudes": {
            "Asc": "22 Cn 13", "Sun": "28 Vi 43", "Moon": "5 Ge 45",
            "Mars": "21 Li 22", "Merc": "18 Li 27", "Jup": "11 Li 11",
            "Ven": "6 Sc 37", "Sat": "14 Cn 36", "Rahu": "21 Ta 07",
            "Ketu": "21 Sc 07", "HL": "6 Ta 11", "GL": "3 Li 33",
        },
        "chara_karakas": {
            "Sun": "AK", "Mars": "AmK", "Merc": "BK", "Rahu": "PK",
            "Jup": "PiK", "Ven": "GK", "Sat": "MK", "Moon": "DK",
        },
        "drawn": {
            "HL": "Ta", "Rahu": "Ta", "AL": "Ta", "Moon": "Ge",
            "Sat": "Cn", "Asc": "Cn", "Ketu": "Sc", "Ven": "Sc",
            "Merc": "Li", "Mars": "Li", "GL": "Li", "Jup": "Li",
            "Sun": "Vi",
        },
        "events": {"elected Chief Minister of Orissa": "early 2000"},
        "first_seen": "chapter 16, Example 54",
        "note": (
            "Unlike Charts 17 and 18 the drawn diagram is the rasi chart "
            "itself. Every body recomputes within an arcminute. Example 54 "
            "also places Rajya saham in Libra; sahams are a Tajika concept "
            "the book defers to a later part and we do not compute them, so "
            "that one claim is unchecked — see docs/open-items.md OI-116."
        ),
    },
    18: {
        "title": "A lady",
        "birth": "June 1, 1972, 4:16 am (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1972, "month": 6, "day": 1, "hour": 4, "minute": 16,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "26 Ar 32", "Sun": "17 Ta 04", "Moon": "29 Sg 27",
            "Mars": "18 Ge 55", "Merc": "12 Ta 14", "Jup": "12 Sg 49",
            "Ven": "10 Ge 48", "Sat": "16 Ta 34", "Rahu": "5 Cp 06",
            "Ketu": "5 Cn 06", "HL": "7 Ar 55", "GL": "10 Aq 32",
        },
        "chara_karakas": {
            "Moon": "AK", "Rahu": "AmK", "Mars": "BK", "Sun": "MK",
            "Jup": "PK", "Sat": "PiK", "Merc": "GK", "Ven": "DK",
        },
        "retrograde": ("Jup", "Ven"),
        "divisional": {
            "D7": {
                "Asc": "Li", "Mars": "Li", "GL": "Ar", "HL": "Ta",
                "AL": "Ge", "Moon": "Ge", "Jup": "Aq", "Sun": "Aq",
                "Ketu": "Aq", "Sat": "Aq", "Merc": "Cp", "Rahu": "Le",
                "Ven": "Le",
            },
        },
        #: The only chart in the register with dated life events, which is
        #: what lets Example 53 be checked against something outside itself.
        "events": {
            "first child": "November 1994",
            "second child": "December 1996",
        },
        "first_seen": "chapter 16, Example 53",
        "note": (
            "The drawn diagram is the D-7, not the rasi chart; the printed "
            "longitudes are the rasi and recompute from the birth line within "
            "an arcminute, the ascendant included. Jupiter and Venus are "
            "printed retrograde. Example 53's dasa dates only come out under "
            "savana years — see docs/open-items.md OI-115."
        ),
    },
    17: {
        "title": "Pandit Sanjay Rath",
        "birth": "August 7, 1963, 9:14 pm (IST), 83 E 58, 21 N 27",
        "birth_data": {
            "year": 1963, "month": 8, "day": 7, "hour": 21, "minute": 14,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 21 + 27 / 60, "longitude": 83 + 58 / 60},
        "longitudes": {
            "Asc": "14 Pi 01", "Sun": "21 Cn 04", "Moon": "19 Aq 58",
            "Mars": "13 Vi 40", "Merc": "13 Le 23", "Jup": "26 Pi 07",
            "Ven": "14 Cn 56", "Sat": "26 Cp 49", "Rahu": "25 Ge 45",
            "Ketu": "25 Sg 45", "HL": "13 Sc 16", "GL": "2 Sc 31",
        },
        "chara_karakas": {
            "Sat": "AK", "Jup": "AmK", "Sun": "BK", "Mars": "PK",
            "Merc": "GK", "Ven": "PiK", "Moon": "MK", "Rahu": "DK",
        },
        "retrograde": ("Sat",),
        "divisional": {
            "D10": {
                "Asc": "Pi", "Sat": "Ta", "Rahu": "Aq", "Ven": "Cn",
                "Jup": "Cn", "GL": "Cn", "Ketu": "Le", "Moon": "Le",
                "Merc": "Sg", "AL": "Sc", "HL": "Sc", "Sun": "Li",
                "Mars": "Vi", "A3": "Vi",
            },
        },
        "first_seen": "chapter 16, Example 52",
        "note": (
            "The drawn diagram is the D-10, not the rasi chart; the printed "
            "longitudes are the rasi and recompute from the birth line within "
            "an arcminute for every graha. The ascendant is 16' out, which is "
            "about a minute of birth time against a time printed to the "
            "minute. A3 and AL are ours, not printed as longitudes — the "
            "diagram places them and both agree."
        ),
    },
    16: {
        "title": "D-27 — the twins Satyam and Shivam Gaur",
        "birth": "November 4, 1970, 4:06 pm (IST), 76 E 53, 30 N 44",
        "birth_data": {
            "year": 1970, "month": 11, "day": 4, "hour": 16, "minute": 6,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 30 + 44 / 60, "longitude": 76 + 53 / 60},
        "longitudes": {
            "Asc": "19 Pi 54", "Sun": "18 Li 09", "Moon": "21 Sg 18",
            "Mars": "16 Vi 04", "Merc": "23 Li 07", "Jup": "21 Li 57",
            "Ven": "27 Li 32", "Sat": "26 Ar 16", "Rahu": "5 Aq 33",
            "Ketu": "5 Le 33", "HL": "1 Le 04", "GL": "6 Li 02",
        },
        "divisional": {
            "D27": {
                "GL": "Pi", "Sat": "Pi", "AL": "Pi", "HL": "Ar", "Jup": "Ta",
                "Merc": "Ge", "Asc": "Ge", "Rahu": "Aq", "Sun": "Aq",
                "Ketu": "Le", "Moon": "Sc", "Ven": "Li", "Mars": "Vi",
            },
        },
        "retrograde": ("Ven", "Sat"),
        "related": {
            "Shivam Gaur": {
                "title": "D-27 — Shivam Gaur, the second twin",
                "birth": "November 4, 1970, 4:08 pm (IST), 76 E 53, 30 N 44",
                "birth_data": {
                    "year": 1970, "month": 11, "day": 4, "hour": 16,
                    "minute": 8, "second": 0.0, "utc_offset_hours": 5.5,
                },
                "place": {"latitude": 30 + 44 / 60, "longitude": 76 + 53 / 60},
                "longitudes": {
                    "Asc": "20 Pi 37", "Sun": "18 Li 09", "Moon": "21 Sg 19",
                    "Mars": "16 Vi 04", "Merc": "23 Li 07", "Jup": "21 Li 57",
                    "Ven": "27 Li 32", "Sat": "26 Ar 16", "Rahu": "5 Aq 33",
                    "Ketu": "5 Le 33", "HL": "2 Le 03", "GL": "8 Li 30",
                },
                "divisional": {
                    "D27": {
                        "AL": "Pi", "Sat": "Pi", "HL": "Ta", "Jup": "Ta",
                        "GL": "Ta", "Merc": "Ge", "Rahu": "Aq", "Sun": "Aq",
                        "Asc": "Cn", "Ketu": "Le", "Moon": "Sc", "Ven": "Li",
                        "Mars": "Vi",
                    },
                },
                "retrograde": ("Ven", "Sat"),
                "note": "The same two minutes move the D-27 lagna from "
                        "Gemini to Cancer.",
            },
        },
        "first_seen": "chapter 13, Example 46",
        "note": (
            "Chart 16 prints the D-27 of the same twins. Section 13.4 reads "
            "inherent nature, strengths and weaknesses from D-27."
        ),
    },
    60: {
        "title": "AV Timing Exercise — D-10 and a transit chart",
        "birth": "August 20, 1944, 7:11 am (IST), 72 E 49, 18 N 58",
        "birth_data": {
            "year": 1944, "month": 8, "day": 20, "hour": 7, "minute": 11,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 18 + 58 / 60, "longitude": 72 + 49 / 60},
        "longitudes": {
            "Asc": "14 Le 44", "Sun": "3 Le 49", "Moon": "17 Le 09",
            "Mars": "1 Vi 12", "Merc": "28 Le 34", "Jup": "12 Le 12",
            "Ven": "18 Le 40", "Sat": "14 Ge 13", "Rahu": "2 Cn 48",
            "Ketu": "2 Cp 48", "HL": "29 Le 06", "GL": "7 Li 04",
        },
        "chara_karakas": {
            "Merc": "AK", "Rahu": "AmK", "Ven": "BK", "Moon": "MK",
            "Sat": "PiK", "Jup": "PK", "Sun": "GK", "Mars": "DK",
        },
        "divisional": {
            "D10": {
                "Rahu": "Pi", "Merc": "Ta", "Mars": "Ta", "HL": "Ta",
                "Ven": "Aq", "Moon": "Cp", "Jup": "Sg", "Asc": "Sg",
                "GL": "Sg", "Sat": "Li", "Ketu": "Vi", "Sun": "Vi",
                "AL": "Vi",
            },
        },
        "transit": {
            "for": "the exercise",
            "date": "not printed — the transit chart carries no date",
            "drawn": {
                "Rahu": "Ta", "Moon": "Cp", "Jup": "Sg", "Mars": "Sg",
                "Ketu": "Sc", "Ven": "Sc", "Merc": "Li", "Sun": "Li",
                "Sat": "Li",
            },
            "inferred_date": "October 31 or November 1, 1984",
            "inferred_how": (
                "The nine drawn positions were scanned against every day "
                "from 1960 to 2025 at Mumbai. Exactly one window matches all "
                "nine: the Moon is in Capricorn only from the night of "
                "October 30 to the early hours of November 2, 1984, and the "
                "other eight hold across it, giving October 31 and November "
                "1 as the only full days that fit. No other day in the "
                "65-year span matches more than eight."
            ),
        },
        "first_seen": "chapter 25, after §25.5.2",
        "note": (
            "Printed for an exercise, so it is the diagrams and not a worked "
            "reading that must hold. Both top charts are the **D-10**, drawn "
            "South Indian and North Indian; the printed longitudes are the "
            "**rasi** longitudes, and all twelve of them map to the drawn "
            "D-10 signs. The D-10's AL comes out Virgo as drawn when the "
            "arudha is taken inside the D-10. Every graha recomputes within "
            "0.91' and all eight chara karakas match. The transit half is "
            "drawn without a date; Chart 61 prints the same nine positions "
            "for **October 31, 1984**, which settled it — see OI-142, closed."
        ),
    },
    61: {
        "title": "Indira Gandhi, and the transit at her assassination — "
                 "Example 110",
        "birth": "November 19, 1917, 11:03 pm (IST), 81 E 52, 25 N 28",
        "birth_data": {
            "year": 1917, "month": 11, "day": 19, "hour": 23, "minute": 3,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 25 + 28 / 60, "longitude": 81 + 52 / 60},
        "longitudes": {
            "Asc": "25 Cn 38", "Sun": "4 Sc 07", "Moon": "5 Cp 30",
            "Mars": "16 Le 22", "Merc": "13 Sc 13", "Jup": "14 Ta 59",
            "Ven": "21 Sg 00", "Sat": "21 Cn 47", "Rahu": "10 Sg 33",
            "Ketu": "10 Ge 33", "HL": "23 Pi 43", "GL": "24 Ar 09",
        },
        "chara_karakas": {
            "Sat": "AK", "Ven": "AmK", "Rahu": "BK", "Mars": "MK",
            "Jup": "PiK", "Merc": "PK", "Moon": "GK", "Sun": "DK",
        },
        "retrograde": ("Jup",),
        "drawn": {
            "HL": "Pi", "AL": "Ar", "GL": "Ar", "Jup": "Ta", "Ketu": "Ge",
            "Sat": "Cn", "Asc": "Cn", "Moon": "Cp", "Mars": "Le",
            "Rahu": "Sg", "Ven": "Sg", "Merc": "Sc", "Sun": "Sc",
        },
        "transit": {
            "for": "her assassination",
            "date": "October 31, 1984, 12:30 pm (IST), 77 E 12, 28 N 36",
            "birth_data": {
                "year": 1984, "month": 10, "day": 31, "hour": 12, "minute": 30,
                "second": 0.0, "utc_offset_hours": 5.5,
            },
            "place": {"latitude": 28 + 36 / 60, "longitude": 77 + 12 / 60},
            "longitudes": {
                "Asc": "4 Cp 25", "Sun": "14 Li 24", "Moon": "11 Cp 28",
                "Mars": "24 Sg 54", "Merc": "27 Li 05", "Jup": "15 Sg 04",
                "Ven": "19 Sc 47", "Sat": "24 Li 07", "Rahu": "4 Ta 46",
                "Ketu": "4 Sc 46", "HL": "12 Ar 53", "GL": "10 Cp 59",
            },
            "chara_karakas": {
                "Merc": "AK", "Rahu": "AmK", "Mars": "BK", "Sat": "MK",
                "Ven": "PiK", "Jup": "PK", "Sun": "GK", "Moon": "DK",
            },
            "drawn": {
                "Rahu": "Ta", "Moon": "Cp", "Asc": "Cp", "AL": "Ar",
                "Jup": "Sg", "Mars": "Sg", "Ketu": "Sc", "Ven": "Sc",
                "Merc": "Li", "Sun": "Li", "Sat": "Li",
            },
        },
        "events": {"she was assassinated": "October 31, 1984"},
        "first_seen": "chapter 25, Example 110",
        "note": (
            "Promised since chapter 1 and supplied only here, the last chart "
            "the register was missing. Both halves recompute — worst body "
            "1.01' (natal Mercury) and 1.00' (transit Venus), ascendants 0.40' "
            "and 0.95' — and all sixteen chara karakas match. Jupiter is "
            "printed (R) natally and computes retrograde. Its transit half "
            "carries the **same nine positions Chart 60 draws undated**, "
            "which is what closed OI-142."
        ),
    },
    62: {
        "title": "Princess Diana — Example 111",
        "birth": "July 1, 1961, 2:25 pm (1:00 East), 0 E 30, 52 N 50",
        "birth_data": {
            "year": 1961, "month": 7, "day": 1, "hour": 14, "minute": 25,
            "second": 0.0, "utc_offset_hours": 1.0,
        },
        "place": {"latitude": 52 + 50 / 60, "longitude": 0 + 30 / 60},
        "longitudes": {
            "Asc": "28 Vi 17", "Sun": "16 Ge 08", "Moon": "28 Cp 27",
            "Mars": "8 Le 12", "Merc": "9 Ge 59", "Jup": "11 Cp 48",
            "Ven": "0 Ta 51", "Sat": "4 Cp 30", "Rahu": "6 Le 24",
            "Ketu": "6 Aq 24", "HL": "8 Ar 15", "GL": "27 Ge 00",
        },
        "chara_karakas": {
            "Moon": "AK", "Rahu": "AmK", "Sun": "BK", "Jup": "MK",
            "Merc": "PiK", "Mars": "PK", "Sat": "GK", "Ven": "DK",
        },
        "retrograde": ("Merc", "Jup", "Sat"),
        "drawn": {
            "HL": "Ar", "Ven": "Ta", "Merc": "Ge", "Sun": "Ge", "GL": "Ge",
            "Ketu": "Aq", "Jup": "Cp", "Moon": "Cp", "Sat": "Cp",
            "Rahu": "Le", "Mars": "Le", "AL": "Sg", "Asc": "Vi",
        },
        "ashtakavarga": {
            "rasi": {"Saturn": (3, 4, 6, 3, 0, 2, 2, 5, 4, 3, 2, 5)},
        },
        "sodhya_pindas": {"Saturn": 203},
        "events": {
            "she died in a car crash": "August 31, 1997 — the date is not "
                                       "printed; the book says only that "
                                       "Saturn was in Revathi then",
        },
        "first_seen": "chapter 25, Example 111",
        "note": (
            "The chart §25.6 works. Every graha recomputes within 0.67', all "
            "three printed retrogrades come out retrograde and all eight "
            "chara karakas match; the ascendant is 4.8' out on a birth time "
            "given to the minute. Its value is the **timing**: Saturn's "
            "printed BAV reproduces to all twelve values, and his sodhya "
            "pinda of 203 reproduces through the whole §12.7 pipeline — "
            "trikona sodhana, ekaadhipatya sodhana, then rasi pinda 129 plus "
            "graha pinda 74. It is the first chart other than Chart 7 to "
            "check that pipeline against a printed pinda."
        ),
    },
    63: {
        "title": "Exercise 38 — natal D-4 against the transit rasi chart",
        "birth": "April 4, 1970, 5:50 pm (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "14 Vi 52", "Sun": "20 Pi 52", "Moon": "28 Aq 35",
            "Mars": "26 Ar 40", "Merc": "3 Ar 07", "Jup": "9 Li 45",
            "Ven": "7 Ar 55", "Sat": "15 Ar 06", "Rahu": "16 Aq 53",
            "Ketu": "16 Le 53", "HL": "15 Pi 42", "GL": "8 Vi 40",
        },
        "chara_karakas": {
            "Moon": "AK", "Mars": "AmK", "Sun": "BK", "Jup": "PK",
            "Sat": "MK", "Rahu": "PiK", "Ven": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "divisional": {
            "D4": {
                "Merc": "Ar", "Ketu": "Aq", "AL": "Aq", "Ven": "Cn",
                "Jup": "Cp", "Mars": "Cp", "Rahu": "Le", "GL": "Sg",
                "Asc": "Sg", "Moon": "Sc", "Sat": "Li", "HL": "Vi",
                "Sun": "Vi",
            },
        },
        "transit": {
            "for": "the event of August 16, 1991",
            "date": ("August 16, 1991 — no time printed on this half; "
                     "Chart 64 gives 2:45 am (IST) for the same instant"),
            "birth_data": {
                "year": 1991, "month": 8, "day": 16, "hour": 2, "minute": 45,
                "second": 0.0, "utc_offset_hours": 5.5,
            },
            "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
            "drawn": {
                "Ketu": "Ge", "Sun": "Cn", "Sat": "Cp", "Merc": "Le",
                "Mars": "Le", "Ven": "Le", "Jup": "Le", "Rahu": "Sg",
                "Moon": "Li",
            },
            "retrograde": ("Sat", "Merc", "Ven"),
        },
        "events": {"he left India and landed in the USA": "August 16, 1991"},
        "first_seen": "chapter 25, Exercise 38",
        "note": (
            "The chapter's exercise, and §25.4's interaction (1): a natal "
            "**divisional** chart read against the **transit rasi** chart. "
            "The natal half recomputes to 0.87' with the ascendant at 0.50', "
            "all eight chara karakas match, and all twelve natal D-4 signs "
            "map from the printed longitudes. Chart 64 is the same nativity "
            "and the same instant through interaction (2)."
        ),
    },
    64: {
        "title": "Exercise 38 — natal rasi chart against the transit D-4",
        "birth": "April 4, 1970, 5:50 pm (IST), 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Asc": "14 Vi 52", "Sun": "20 Pi 52", "Moon": "28 Aq 35",
            "Mars": "26 Ar 40", "Merc": "3 Ar 07", "Jup": "9 Li 45",
            "Ven": "7 Ar 55", "Sat": "15 Ar 06", "Rahu": "16 Aq 53",
            "Ketu": "16 Le 53", "HL": "15 Pi 42", "GL": "8 Vi 40",
        },
        "chara_karakas": {
            "Moon": "AK", "Mars": "AmK", "Sun": "BK", "Jup": "PK",
            "Sat": "MK", "Rahu": "PiK", "Ven": "GK", "Merc": "DK",
        },
        "retrograde": ("Jup",),
        "drawn": {
            "HL": "Pi", "Sun": "Pi", "Merc": "Ar", "Mars": "Ar", "Sat": "Ar",
            "Ven": "Ar", "Rahu": "Aq", "Moon": "Aq", "Ketu": "Le",
            "AL": "Sc", "Jup": "Li", "GL": "Vi", "Asc": "Vi",
        },
        "transit": {
            "for": "the event of August 16, 1991",
            "date": "August 16, 1991, 2:45 am (IST), 81 E 12, 16 N 15",
            "birth_data": {
                "year": 1991, "month": 8, "day": 16, "hour": 2, "minute": 45,
                "second": 0.0, "utc_offset_hours": 5.5,
            },
            "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
            "divisional": {
                "D4": {
                    "Ketu": "Pi", "Sat": "Ar", "Sun": "Ar", "Mars": "Ta",
                    "Moon": "Cp", "Jup": "Le", "Ven": "Sc", "Merc": "Sc",
                    "Rahu": "Vi",
                },
            },
            "retrograde": ("Sat", "Merc", "Ven"),
        },
        "events": {"he left India and landed in the USA": "August 16, 1991"},
        "first_seen": "chapter 25, Exercise 38",
        "note": (
            "The same nativity and instant as Chart 63, through §25.4's "
            "interaction (2): the **natal rasi** chart against a **transit "
            "divisional** chart. Every transit body reproduces in both the "
            "rasi and the D-4, and all three printed retrogrades come out "
            "retrograde. This half carries a **time** where Chart 63's does "
            "not, and it has to: across August 16 no transit rasi sign "
            "changes at all, while the Moon crosses three D-4 signs."
        ),
    },
}


#: Charts the book supplies inside a worked example or an exercise without
#: giving them a "Chart N". Keyed by the label the book itself uses, because
#: Example 24 and Exercise 24 are different natives and a bare number would
#: not say which. They are partial by nature — the text prints only what its
#: own computation needs — so each record says what is missing.
UNNUMBERED_CHARTS: dict[str, dict[str, Any]] = {
    "Example 49": {
        "title": "Section 15.4.4's worked example",
        "birth": "April 4, 1970, 5:50 pm (IST), Machilipatnam, 81 E 12, 16 N 15",
        "birth_data": {
            "year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
            "second": 0.0, "utc_offset_hours": 5.5,
        },
        "place": {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60},
        "longitudes": {
            "Merc": "3 Ar 08", "Jup": "9 Li 46", "Ven": "7 Ar 55",
        },
        "stated": {
            "lagna_rasi": "Vi",
            "moon_constellation": 25,
            "sunrise": "6:00 am",
            "ghati_at_birth": 30,
            "name_initial": "V",
        },
        "first_seen": "chapter 15, Example 49",
        "note": (
            "Only the three grahas the example computes are printed. The Moon "
            "is given as its constellation (Poorvabhadrapada, the 25th) and "
            "the lagna as its rasi, with no longitude for either, so the "
            "chart cannot be drawn. Sunrise is stated as 6:00 am rather than "
            "computed; the book uses it to reach G = 30."
        ),
    },
    "Exercise 24": {
        "title": "Section 15.4.4's exercise",
        "birth": "November 8, 1927, 8:30 am (LMT), 67 E 03, 24 N 52",
        "birth_data": {
            "year": 1927, "month": 11, "day": 8, "hour": 8, "minute": 30,
            "second": 0.0,
            # LMT, not a zone: the meridian's own offset, 67.05 / 15.
            "utc_offset_hours": (67 + 3 / 60) / 15.0,
        },
        "place": {"latitude": 24 + 52 / 60, "longitude": 67 + 3 / 60},
        "longitudes": {},
        "stated": {"name_initial": "L"},
        "first_seen": "chapter 15, Exercise 24",
        "note": (
            "The exercise prints no positions at all, only the birth data and "
            "the name's first sound. Everything the answer needs is computed: "
            "the nakshatras and navamsas of Sun, Mars and Jupiter, the Moon's "
            "nakshatra, the lagna, and the ghati from our own sunrise. The "
            "book gives the three answers but never its own longitudes, so "
            "this chart is a check on the ephemeris, not a transcription."
        ),
    },
}
