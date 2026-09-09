"""Exercise 48 — the chapter's only exercise, and the book answers none of it.

A second nativity, a second marriage, and three verifications the reader is
told to do. The answer key gives the varsha pravesh and "Try yourself".
"""

from __future__ import annotations

#: Exercise 48, verbatim.
EXERCISE_48 = (
    "A native born on 4th April 1970 at 5:50 pm (IST) at 81 E 12, 16 N 15 got "
    "married on 1st August 1993. Verify that navamsa lagna's dasa as per "
    "varsha Narayana dasa of navamsa was running at the time of marriage. "
    "Verify that the running dasa and antardasa as per Patyayini dasa and "
    "Mudda dasa - at the time of wedding - belonged to lagna/7th lord in "
    "rasi/navamsa.")

#: The answer, verbatim and complete.
EXERCISE_48_ANSWER = (
    "Try yourself. Varsha pravesh: 4th April 1993, 3:19:03 pm (IST), 81 E 12, "
    "16 N 15")

#: The nativity and the event.
BIRTH = {"year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
         "second": 0.0, "utc_offset_hours": 5.5}
PLACE = {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60}
VARSHA_PRAVESH = {"year": 1993, "month": 4, "day": 4, "hour": 15, "minute": 19,
                  "second": 3.0, "utc_offset_hours": 5.5}
MARRIAGE = {"year": 1993, "month": 8, "day": 1}
COMPLETED_YEARS = 23
ANNUAL_YEAR = 24

#: **Finding.** The varsha pravesh reproduces to **10.6 seconds**: §27.1's
#: solar return on this nativity's Sun, in the native's 24th year, gives
#: 4 April 1993 15:19:13.6 IST against the printed 15:19:03. The birth time is
#: given to the minute, as in Examples 118 and 122, whose residuals were 9 and
#: 6.6 seconds. Three nativities, three residuals under eleven seconds, all
#: from birth times printed to the minute.
THE_VARSHA_PRAVESH_REPRODUCES_TO_ELEVEN_SECONDS = (
    "The solar return gives 4 April 1993 15:19:13.6 IST against the printed "
    "15:19:03, a difference of 10.6 seconds. Examples 118 and 122 were out by "
    "9 and 6.6 seconds, and all three birth times are printed to the minute."
)

#: The three verifications and what they come to. All three hold.
EXERCISE_48_VERDICTS: tuple[dict[str, object], ...] = (
    {"dasa": "Varsha Narayana of navamsa",
     "running": "Gemini",
     "why_it_qualifies": "Gemini is the navamsa lagna",
     "holds": True},
    {"dasa": "Patyayini",
     "running": "Lagna", "antardasa": "Saturn",
     "why_it_qualifies": ("the dasa is the lagna's own, and Saturn is the "
                          "7th lord in the rasi chart"),
     "holds": True},
    {"dasa": "Mudda",
     "running": "Jupiter", "antardasa": "Saturn",
     "why_it_qualifies": ("Jupiter is the 7th lord in navamsa and Saturn the "
                          "7th lord in the rasi chart"),
     "holds": True},
)

#: **Finding.** The exercise reads "lagna/7th lord in rasi/navamsa", and
#: patyayini's answer settles how to parse it: the dasa running at the wedding
#: is the **Lagna's own**, which is a dasa patyayini alone has and which is not
#: a planet at all. So the phrase is "the lagna, or the 7th lord" and not "the
#: lagna lord or the 7th lord". Read the other way, patyayini's dasa would fail
#: the exercise its own answer key implies.
THE_PHRASE_MEANS_THE_LAGNA_ITSELF = (
    "Patyayini's dasa at the wedding is the Lagna's own, which no other dasa "
    "in the chapter has and which is not a planet. So the phrase is the "
    "lagna or the 7th lord, not the lagna lord or the 7th lord."
)

#: **Finding.** Every qualifying lord in this chart is a different planet, so
#: the exercise is a real test rather than a coincidence: the rasi lagna Leo
#: gives the Sun, the rasi 7th Aquarius gives Saturn, the navamsa lagna Gemini
#: gives Mercury and the navamsa 7th Sagittarius gives Jupiter. Four lords,
#: four planets, and two of the three answers land on two different ones.
THE_FOUR_QUALIFYING_LORDS_ARE_FOUR_DIFFERENT_PLANETS = (
    "Leo gives the Sun, Aquarius Saturn, Gemini Mercury and Sagittarius "
    "Jupiter, so the exercise's four references are four distinct planets and "
    "nothing is satisfied by accident."
)

#: **Finding.** The Varsha Narayana seed needed no exception and the earlier
#: example's did. Here the 9th from the muntha Leo is Aries, its lord Mars sits
#: in Taurus in the navamsa, Taurus beats Scorpio, and Taurus is fixed — so the
#: movement is "sixth" and the order runs Ta, Sg, Cn, Aq, Vi, Ar, Sc, **Ge**.
#: Mars and Jupiter occupy the seed and neither triggers §18.2.1's exceptions,
#: which belong to Saturn and Ketu. Example 122's seed held Saturn and did.
THIS_SEED_TAKES_NO_EXCEPTION_WHERE_EXAMPLE_122S_DID = (
    "Taurus holds Mars and Jupiter, and section 18.2.1's exceptions belong to "
    "Saturn and Ketu, so the progression is the plain sixth movement. Example "
    "122's Scorpio held Saturn and took the exception."
)

#: **Finding.** The exercise asks for a **mudda antardasa** and §30.3 never
#: gives an antardasa rule. Under Vimsottari's own — which is what §30.2 used
#: for patyayini, "just as in Vimsottari dasa" — Jupiter's 48-day dasa opens
#: with 6.40 days of Jupiter and then 7.60 of Saturn, and the wedding falls in
#: Saturn's. That answer qualifies, which is weak evidence that the rule is the
#: one intended. See OI-176.
THE_MUDDA_ANTARDASA_NEEDED_A_RULE_THE_SECTION_DOES_NOT_GIVE = (
    "Section 30.3 states no antardasa rule and the exercise asks for one. "
    "Vimsottari's proportional rule puts the wedding in Saturn's antardasa, "
    "which satisfies the exercise."
)
