"""Example 123 — a foreign trip timed by Varsha Narayana dasa of D-4.

The same native as Exercise 48, four years earlier. The chapter's only worked
case in a varga other than the navamsa, and its only one that names an
antardasa.
"""

from __future__ import annotations

CHART_NUMBER = 68

#: Example 123's opening, verbatim.
EXAMPLE_123 = (
    "The native of Exercise 48 went from India to US for his masters degree "
    "in engineering, on 15th August 1991. He went on a fellowship from a "
    "University in US. Let us time his foreign trip using Varsha Narayana "
    "dasa of D-4.")

VARSHA_PRAVESH_DATA = (
    "5th April 1991, 3:05:33 am (IST), 81 E 12, 16 N 15")

#: The "why he went abroad" paragraph, verbatim.
WHY_HE_WENT_ABROAD = (
    "In rasi chart, lagna has Saturn and Rahu. Both the planets show living "
    "away from the place of birth. Jupiter owns 12th - living away from "
    "homeland - and he is exalted in 7th - a long trip. In D-4 (see Chart "
    "68), 9th and 12th lord Mercury is in 7th showing a long trip to a "
    "foreign land. Mars owns 7th (long trips) and he is in 9th. Sun owns "
    "paradesa saham and jalapatana saham and he is in 12th - foreign lands - "
    "in D-4. For all these reasons, the native went abroad during the year.")

#: The dasa paragraph, verbatim.
THE_DASA_PARAGRAPH = (
    "Though rasi chart has lagna in Cp, muntha or annual progressed ascendant "
    "is in Ge. We should use Ge as lagna for Varsha Narayana dasa. The 4th "
    "house from Ge is Vi and Mercury owns it. He is in Ar in D-4. Ar with two "
    "planets is stronger than Li with one planet. Dasas go as Ar, Ta, Ge Cn "
    "etc.")

#: The timing paragraph, verbatim.
THE_TIMING_PARAGRAPH = (
    "Virgo dasa was running during August 10-26, 1991. The native went abroad "
    "on 15th/16th August 1991, during Virgo dasa, Gemini antardasa as per "
    "Varsha Narayana dasa of D-4. Virgo is the 12th house containing the lord "
    "of padesa saham and jalapatana saham. Gemini is the 9th house containing "
    "7th lord. Lord of both Virgo and Gemini is Mercury and he is in the 7th "
    "house.")

BIRTH = {"year": 1970, "month": 4, "day": 4, "hour": 17, "minute": 50,
         "second": 0.0, "utc_offset_hours": 5.5}
PLACE = {"latitude": 16 + 15 / 60, "longitude": 81 + 12 / 60}
VARSHA_PRAVESH = {"year": 1991, "month": 4, "day": 5, "hour": 3, "minute": 5,
                  "second": 33.0, "utc_offset_hours": 5.5}
DEPARTURE = {"year": 1991, "month": 8, "day": 15}
ANNUAL_YEAR = 22

#: The five reasons the first paragraph gives, as data. Four are read in the
#: D-4 and one in the rasi chart, and all of them hold.
REASONS_FOR_THE_TRIP: tuple[dict[str, object], ...] = (
    {"chart": "rasi", "claim": "the lagna holds Saturn and Rahu"},
    {"chart": "rasi",
     "claim": "Jupiter owns the 12th and is exalted in the 7th"},
    {"chart": "D-4",
     "claim": "Mercury, the 9th and 12th lord, is in the 7th"},
    {"chart": "D-4", "claim": "Mars owns the 7th and is in the 9th"},
    {"chart": "D-4",
     "claim": "the Sun, who owns paradesa and jalapatana sahams, is in "
              "the 12th"},
)

#: **Finding.** Chart 68 is the only chart in the register whose **diagram is a
#: divisional chart** while its printed longitudes are the rasi chart's. The
#: header says "D-4", the boxes are the chaturthamsa, and the twelve
#: longitudes below are the rasi positions the D-4 is built from — which the
#: text confirms: "Though rasi chart has lagna in Cp", and the printed Asc is
#: 27 Cp 20.
CHART_68_DRAWS_A_VARGA_AND_PRINTS_THE_RASI = (
    "Chart 68's diagram is the D-4 and its printed longitudes are the rasi "
    "chart's. No other chart in the register does that."
)

#: **Finding.** The varsha pravesh reproduces to **2.3 seconds**, the closest
#: of the four the book prints — Examples 118, 122 and Exercise 48 were out by
#: 9, 6.6 and 10.6.
THE_CLOSEST_VARSHA_PRAVESH_IN_THE_BOOK = (
    "The solar return gives 5 April 1991 03:05:30.7 IST against the printed "
    "03:05:33, a difference of 2.3 seconds and the smallest of the four the "
    "book prints."
)

#: **Finding, and the Moon decides it.** Every printed longitude reproduces
#: within an arcminute, but the Moon's **25 Sc 02** needs our own solved
#: varsha pravesh and not the book's printed one: at 03:05:33 the Moon is at
#: 25 Sc **03.01**, which truncates to 03, and at our 03:05:30.7 she is at 25
#: Sc **02.99**, which truncates to 02 as printed. Two hundredths of an
#: arcminute decide the figure, and the printed chart agrees with the earlier
#: instant.
THE_PRINTED_MOON_FITS_OUR_INSTANT_NOT_THE_PRINTED_ONE = (
    "At the printed varsha pravesh the Moon is 25 Sc 03.01 and at our solved "
    "one 25 Sc 02.99. The chart prints 25 Sc 02, so it agrees with the "
    "earlier instant by two hundredths of an arcminute."
)

#: **Finding.** Every box of the D-4 diagram reproduces, and so does every
#: house claim the paragraph makes from it: with the D-4 lagna in Libra,
#: Mercury is in the **7th**, Mars in the **9th** and the Sun in the **12th**.
THE_D4_REPRODUCES_BOX_FOR_BOX = (
    "All ten bodies fall in the rasis Chart 68's D-4 draws them in, and the "
    "three houses the paragraph reads from the Libra lagna are the 7th, the "
    "9th and the 12th as it says."
)

#: **Finding.** The example uses **two lagnas at once and never says so**. The
#: dasa **order** is seeded from the muntha — Gemini, the natal Virgo lagna
#: advanced 21 years — because §30.4 says to take the muntha as lagna. The
#: dasa **results** are then read from the **D-4 lagna**, Libra: "Virgo is the
#: 12th house" and "Gemini is the 9th house" are both counted from Libra, not
#: from Gemini. Two lagnas, two jobs, in one paragraph.
TWO_LAGNAS_DO_TWO_DIFFERENT_JOBS = (
    "The muntha Gemini seeds the dasa order and the D-4 lagna Libra is what "
    "the houses are counted from. The example uses both without naming the "
    "difference."
)

#: **Finding.** The seed comparison is decided by §15.5's **first** rule, the
#: count of planets, and the example says so outright: "Ar with two planets is
#: stronger than Li with one planet." Aries holds Mercury and Saturn in the
#: D-4 and Libra holds Jupiter — the ascendant in Libra is not a planet and is
#: not counted. Our own comparison reaches Aries the same way.
THE_SEED_IS_DECIDED_BY_COUNTING_PLANETS = (
    "Aries holds Mercury and Saturn in the D-4 and Libra holds Jupiter alone, "
    "the ascendant not counting, so section 15.5's first rule settles the "
    "seed without reaching any later one."
)

#: **Finding.** The Saturn exception fires and changes nothing. Saturn stands
#: in Aries in the D-4, so §18.2.1 forces a regular zodiacal progression — and
#: Aries is movable, whose own movement is already regular and forward. The
#: order is Ar, Ta, Ge, Cn either way, which is what the example prints.
#: Example 122's Scorpio was the case where the exception mattered.
THE_SATURN_EXCEPTION_FIRES_AND_CHANGES_NOTHING = (
    "Saturn is in the seed Aries, so section 18.2.1's exception applies, and "
    "Aries is movable so the progression was already regular and forward. The "
    "order is unchanged."
)

#: **Finding, and it does not reproduce.** The example names an **antardasa** —
#: "during Virgo dasa, Gemini antardasa" — and §30.4 states no antardasa rule
#: for Varsha Narayana dasa, exactly as §30.3 stated none for mudda. Under
#: §18.3's rule the antardasas of this Virgo dasa run from **Aries** forward,
#: so Gemini is the **third** of twelve and falls on 11-12 August; the trip on
#: 15/16 August lands in **Virgo's** own antardasa. Reading the dasa from the
#: book's printed dates instead gives **Leo**. Neither is Gemini. The dasa
#: itself reproduces; the antardasa does not. See OI-177.
THE_ANTARDASA_DOES_NOT_REPRODUCE = (
    "Section 18.3's antardasas of the Virgo dasa run from Aries, putting "
    "Gemini third and on 11-12 August. The trip on 15/16 August falls in "
    "Virgo's own antardasa, or in Leo's from the book's printed dates. The "
    "example says Gemini."
)

#: **Finding.** The dasa boundaries are a day or two off under every reading of
#: a solar day, and the verdict survives all of them. Virgo's dasa opens 126
#: days into the year and closes at 141: **9 to 24 August** as calendar days,
#: **14 to 29 August** as the solar days §30.4 defines, against the printed
#: **10 to 26 August**. The departure on 15/16 August is inside Virgo dasa on
#: all three. See OI-175.
THE_VIRGO_DASA_DATES_ARE_A_DAY_OR_TWO_OUT = (
    "Virgo's dasa runs 9 to 24 August as calendar days and 14 to 29 August as "
    "solar days, against the printed 10 to 26 August. The departure is inside "
    "it under every reading."
)
