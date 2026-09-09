"""Example 125 — a childbirth timed by Varsha Narayana dasa of D-7.

The chapter's fourth and cleanest Varsha Narayana case: the only one whose
printed dasa length and printed opening both come out exactly.
"""

from __future__ import annotations

CHART_NUMBER = 70

#: Example 125's opening, verbatim.
EXAMPLE_125 = (
    "The native of Exercise 48 had a son on 21st August 1998. Let us time "
    "this using Varsha Narayana dasa of D-7.")

VARSHA_PRAVESH_DATA = "4th April 1998, 9:59:49 pm (IST), 81 E 12, 16 N 15"

#: The putra saham paragraph, verbatim.
WHY_A_CHILD = (
    "In rasi chart, lagna is in Sc and putra saham is in Ar. Lord Mars is in "
    "5th house. D-7 shows children. In D-7, Jupiter owns 5th and he aspects "
    "5th from 11th (see Chart 70). This resulted in a son in the year.")

#: The dasa paragraph, verbatim.
THE_DASA_PARAGRAPH = (
    "Muntha is in Cp in rasi chart. The 7th house is in Cn. Moon owns it. "
    "Moon is in Cp in D-7 and Cp is stronger than Cn. So Narayana dasa of D-7 "
    "starts from Cp and goes as Cp, Sg, Sc, Li etc. Ge dasa of 24 solar days "
    "started just before the birth of son.")

#: The six reasons for Gemini, verbatim in substance, with the kind of aspect
#: each one needs. See `THE_PARAGRAPH_MIXES_TWO_KINDS_OF_ASPECT`.
WHY_GEMINI: tuple[dict[str, object], ...] = (
    {"number": 1, "reason": "Ge is the 11th house in D-7, showing happiness "
                            "related to children", "aspect": None},
    {"number": 2, "reason": "Ge has Jupiter, the significator of children",
     "aspect": None},
    {"number": 3, "reason": "Ge has Jupiter, the 5th lord who aspects the 5th",
     "aspect": "graha drishti"},
    {"number": 4, "reason": "the 3rd house is the 11th from the 5th and shows "
                            "childbirth, and its exalted lord Venus aspects Ge",
     "aspect": "rasi drishti"},
    {"number": 5, "reason": "Mars owns putra saham and he aspects Ge",
     "aspect": "graha drishti"},
    {"number": 6, "reason": "putra pada, the arudha pada of the 5th, aspects "
                            "Ge from Vi", "aspect": "rasi drishti"},
)

#: The closing line, verbatim.
THE_CLEAR_CANDIDATE = (
    "Gemini is a clear candidate simply because it is 11th and 5th lord "
    "Jupiter occupies it.")

BIRTH = {"year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
         "second": 0.0, "utc_offset_hours": 5.5}
PLACE = {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60}
VARSHA_PRAVESH = {"year": 1998, "month": 4, "day": 4, "hour": 21, "minute": 59,
                  "second": 49.0, "utc_offset_hours": 5.5}
BIRTH_OF_SON = (1998, 8, 21)
ANNUAL_YEAR = 29
VARGA = 7

#: **Finding.** The cleanest of the chapter's four Varsha Narayana cases. The
#: dasa length is **printed** — "Ge dasa of 24 solar days" — and comes out at
#: 24 exactly, Gemini's 8 years times three. Its opening is 20 August 1998
#: against a birth on the 21st, which is "just before the birth of son" to the
#: day. No other Varsha Narayana date in the chapter lands this well; Example
#: 124's opening was exact and its close a day short, and Examples 122 and 123
#: were out by a day or two at both ends.
THE_ONLY_EXAMPLE_WHOSE_LENGTH_AND_OPENING_BOTH_COME_OUT = (
    "Gemini's dasa is printed as 24 solar days and computes to 24, and it "
    "opens on 20 August 1998 against a birth on the 21st. It is the only "
    "Varsha Narayana date in the chapter that lands to the day."
)

#: **Finding, and the fourth confirmation.** The seed lord comes from the
#: **7th** house of the muntha for a D-7, as it came from the 9th for a D-9,
#: the 4th for a D-4 and the 12th for a D-24. Four vargas, four houses, one
#: rule — the varga number reduced by twelves. The muntha is Capricorn, its
#: 7th is Cancer, the Moon owns it, the Moon stands in Capricorn in the D-7,
#: and Capricorn beats Cancer.
THE_VARGA_HOUSE_RULE_HOLDS_A_FOURTH_TIME = (
    "D-7 takes the 7th house from the muntha. With D-9's 9th, D-4's 4th and "
    "D-24's 12th that is four vargas and one rule."
)

#: **Finding.** Both sahams the example uses reproduce. Putra saham lands at
#: **23 Ar 33** — Aries, ruled by Mars, as the paragraph says — and Mars stands
#: in the **5th** from the Scorpio rasi lagna. The chart is cast at 9:59 pm, so
#: putra saham takes its night form.
THE_PUTRA_SAHAM_REPRODUCES = (
    "Putra saham is at 23 Ar 33 in its night form, ruled by Mars, and Mars is "
    "in the 5th from the Scorpio lagna of the rasi chart."
)

#: **Finding.** The six reasons for Gemini use **two different kinds of
#: aspect** and the paragraph never says which is which. Jupiter reaching the
#: 5th and Mars reaching Gemini are **graha drishti** — Jupiter's 7th and
#: Mars's special 4th. Venus reaching Gemini from Pisces and the putra pada
#: reaching it from Virgo are **rasi drishti**: Pisces, Virgo and Gemini are
#: all dual signs. The pada could only ever aspect that way — an arudha is a
#: sign, not a planet, so graha drishti does not apply to it.
THE_PARAGRAPH_MIXES_TWO_KINDS_OF_ASPECT = (
    "Jupiter's and Mars's aspects are graha drishti and Venus's and the putra "
    "pada's are rasi drishti between dual signs. An arudha pada has no graha "
    "drishti of its own, so reason six could not have been anything else."
)

#: **Finding.** All six reasons hold, and the section's own closing line says
#: the first three would have done: "Gemini is a clear candidate simply
#: because it is 11th and 5th lord Jupiter occupies it." The remaining three
#: are corroboration the example offers and then sets aside.
THE_SECTION_SAYS_THREE_OF_THE_SIX_WOULD_HAVE_DONE = (
    "All six reasons check out and the example closes by resting on two of "
    "them - Gemini being the 11th and holding the 5th lord."
)
