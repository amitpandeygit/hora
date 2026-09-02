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
        "first_seen": "chapter 18, Example 68",
        "note": (
            "The first lagna-seeded chart in chapter 18, so the first on "
            "which section 18.4's dasa lagna is the dasa rasi itself. Its "
            "Virgo dasa settles OI-121: Mercury is exalted in his own Virgo, "
            "so exceptions 1 and 2 meet, and the book prints 12 years, not 13."
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
