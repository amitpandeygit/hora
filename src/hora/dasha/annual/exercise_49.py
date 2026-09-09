"""Exercise 49 — a car bought in 1995-96, timed by Varsha Narayana of D-16.

The chapter's last worked case. Its seed comparison is the one that closes
OI-124; its dates are the one thing in the chapter that does not come out.
"""

from __future__ import annotations

CHART_NUMBER = 71

#: Exercise 49, verbatim.
EXERCISE_49 = (
    "Given that the native of Exercise 48 bought a car in 1995-96, try to "
    "time it using Varsha Narayana dasa of D-16.")

#: The answer's varsha pravesh line, verbatim.
EXERCISE_49_ANSWER = (
    "[Varsha pravesh data: 5th April 1995, 3:28:36 am (IST), 81 E 12, "
    "16 N 15]")

#: The worked solution, verbatim.
THE_SOLUTION = (
    "Look at D-16 of the annual chart. The 4th from lagna is not strong. If "
    "the native bought a vehicle, it must be due to the strength of the 4th "
    "from Venus. Exalted Jupiter is in the 4th from Venus. Jupiter owns 3rd "
    "and shows expenditure on 4th, i.e. expenditure on account of happiness "
    "from vehicle. He is exalted in the 4th from Venus showing a good "
    "vehicle. Muntha is in Li and Cp is the 4th. Saturns owns it and occupies "
    "Vi in D-16. Pi is stronger than Vi. So dasas go as Pi, Cn, Sc, Sg, Ar, "
    "Le etc. Cancer dasa in the second cycle ran during Jan 16-Feb 9, 1996. "
    "The native bought a car in this dasa.")

BIRTH = {"year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
         "second": 0.0, "utc_offset_hours": 5.5}
PLACE = {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60}
VARSHA_PRAVESH = {"year": 1995, "month": 4, "day": 5, "hour": 3, "minute": 28,
                  "second": 36.0, "utc_offset_hours": 5.5}
ANNUAL_YEAR = 26
VARGA = 16

#: The printed second-cycle Cancer dasa.
PRINTED_CANCER = {"from": (1996, 1, 16), "to": (1996, 2, 9), "days": 24}

#: **Finding, and it closes OI-124.** The seed comparison is the first in the
#: book to tie past §15.5's rule 5 inside a **varga**. In the D-16 Virgo holds
#: Saturn and Pisces holds the Moon — one planet each — and nothing separates
#: them until rule 6, the lords' advancement. Read in the **D-16** that gives
#: Mercury 27°16' against Jupiter's 15°09' and so **Virgo**; read in the
#: **rasi** chart it gives Mercury 11°05' against Jupiter's 21°34' and so
#: **Pisces**, which is what the solution prints.
#:
#: The chapter's four other varga seeds are all decided at rule 1 by the
#: **varga's** own occupants, and three of the four come out wrong from the
#: rasi chart. So the cascade reads the varga up to rule 5 and the rasi chart
#: at rule 6, which is exactly the reading OI-124 could not choose between.
THE_SEED_COMPARISON_CLOSES_OI_124 = (
    "Virgo and Pisces tie past rule 5 in the D-16. The varga's advancements "
    "give Virgo and the rasi chart's give Pisces, and the solution says "
    "Pisces. Rules 1 to 5 read the varga and rule 6 reads the rasi chart."
)

#: **Finding.** The seed decides the movement as well as the order, and the
#: two possible seeds would have given different progressions. Pisces is dual,
#: so its movement is **trinal** — Pi, Cn, Sc, then the 10th and its trine,
#: Sg, Ar, Le, which is exactly the order the solution prints. Virgo is dual
#: too, but Saturn stands in Virgo in the D-16, so §18.2.1's Saturn exception
#: would have forced a regular zodiacal order instead. Getting rule 6 wrong
#: would have changed every dasa in the year, not just the first.
THE_SEED_DECIDES_THE_MOVEMENT_TOO = (
    "Pisces is dual and empty of Saturn, so the movement is trinal and the "
    "order is Pi, Cn, Sc, Sg, Ar, Le as printed. Virgo would have taken the "
    "Saturn exception and run zodiacally instead."
)

#: **Finding.** Every reading in the solution reproduces. The 4th from the
#: D-16 lagna Libra is Capricorn and it is **empty** — "not strong". Venus is
#: in Aries, the 4th from him is Cancer, and **exalted Jupiter** is there.
#: Jupiter owns Sagittarius, the 3rd from the lagna. The muntha is Libra, its
#: 4th is Capricorn, Saturn owns it and stands in Virgo in the D-16.
EVERY_READING_IN_THE_SOLUTION_REPRODUCES = (
    "Capricorn, the 4th from the D-16 lagna, is empty; Jupiter is exalted in "
    "Cancer, the 4th from Venus; Jupiter owns the 3rd; and the muntha's 4th "
    "is Capricorn, whose lord Saturn is in Virgo."
)

#: **Finding.** This is the chapter's first use of the **second** Narayana
#: cycle. A rasi's second-cycle length is twelve less its first, so Cancer's
#: first-cycle 4 years become **8**, which compress to the **24 solar days**
#: the solution's window spans — 16 January to 9 February 1996 is exactly 24
#: days. The length reproduces; where it sits does not.
THE_SECOND_CYCLE_LENGTH_REPRODUCES = (
    "Cancer's first-cycle dasa is 4 years, so its second-cycle dasa is 8, "
    "which is 24 solar days. The solution's window is 24 days wide."
)

#: **Gap.** The position does not reproduce. Our first cycle totals 252 solar
#: days and the second cycle opens with Pisces's 9, so the second-cycle Cancer
#: runs **22 December 1995 to 15 January 1996** — twenty-five days before the
#: printed 16 January to 9 February. Nothing tried closes the gap: the
#: dignities move it by three days, reading the days as solar days by four,
#: and taking dignities from the rasi chart makes it worse. Every other Varsha
#: Narayana date in the chapter is out by a day or two; this one is out by
#: twenty-five. See OI-178.
THE_SECOND_CYCLE_POSITION_IS_TWENTY_FIVE_DAYS_OUT = (
    "Our second-cycle Cancer runs 22 December 1995 to 15 January 1996 and "
    "the solution prints 16 January to 9 February. The length matches and the "
    "position is twenty-five days early."
)

#: **Finding.** Five vargas now, five houses, one rule: D-9 takes the 9th,
#: D-4 the 4th, D-24 the 12th, D-7 the 7th and D-16 the **4th** — sixteen
#: reduced by twelve. The solution says so in as many words: "Muntha is in Li
#: and Cp is the 4th."
THE_VARGA_HOUSE_RULE_HOLDS_A_FIFTH_TIME = (
    "D-16 takes the 4th house from the muntha, sixteen reduced by twelve. "
    "With D-9, D-4, D-24 and D-7 that is five vargas and one rule."
)
