"""Example 122 and Chart 67 — the chart chapter 30 times its three dasas on.

The example is set up once here and each dasa section reads it. Everything
computable in the setup is checked against the printed page.
"""

from __future__ import annotations

CHART_NUMBER = 67

#: Example 122's opening, verbatim.
EXAMPLE_122 = (
    "Let us consider a lady born on 1st June 1972 at 4:16 am (IST) at 81 E "
    "12, 16 N 15. She got married on 24th July 1993. Let us time this event "
    "from 1993-94 annual chart using all the 3 dasas."
)

#: The varsha pravesh line, verbatim.
VARSHA_PRAVESH_DATA = (
    "1st June 1993, 1:30:04 pm (IST), 81 E 12, 16 N 15. Rasi and navamsa "
    "charts of this data are given in Chart 67."
)

#: The "Marriage in this year" paragraph, verbatim.
MARRIAGE_IN_THIS_YEAR = (
    "Vivaha saham is at 2 degrees 22 minutes in Sg. Lagna has 7th lord and "
    "vivaha saham lord Jupiter in it. Lagna lord Mercury is in own sign and "
    "has ithasala with Jupiter. In navamsa, 7th lord Mercury is well-placed. "
    "Lagna lord Jupiter joins Venus in the 2nd house of family. All these "
    "factors brought marriage in the year."
)

#: The five reasons the paragraph gives, as data. Every one is checkable and
#: every one holds — see `EVERY_REASON_IN_THE_PARAGRAPH_CHECKS_OUT`.
MARRIAGE_REASONS: tuple[dict[str, object], ...] = (
    {"chart": "rasi", "claim": "vivaha saham is at 2 Sg 22",
     "checkable": True},
    {"chart": "rasi",
     "claim": "the lagna holds the 7th lord and the vivaha saham lord, "
              "both Jupiter",
     "checkable": True},
    {"chart": "rasi", "claim": "lagna lord Mercury is in his own sign",
     "checkable": True},
    {"chart": "rasi", "claim": "Mercury has an ithasala with Jupiter",
     "checkable": True},
    {"chart": "navamsa",
     "claim": "the 7th lord Mercury is well-placed, and the lagna lord "
              "Jupiter joins Venus in the 2nd",
     "checkable": True},
)

#: **Finding.** The nativity is **Chart 18**, and the example does not say so.
#: "A lady born on 1st June 1972 at 4:16 am (IST) at 81 E 12, 16 N 15" is
#: Chart 18's birth line word for word, and Chart 18's Sun is 17 Ta 04 —
#: which is Chart 67's Sun, as a solar return requires. Two charts printed
#: thirteen chapters apart, and the register now links them.
THE_NATIVITY_IS_CHART_18_UNNAMED = (
    "Example 122's birth data is Chart 18's, to the minute and the "
    "arcminute, and its natal Sun at 17 Ta 04 is Chart 67's Sun. The example "
    "does not name the chart."
)

#: **Finding.** The varsha pravesh reproduces to **6.6 seconds**. §27.1's
#: solar return on Chart 18's natal Sun, in her 22nd year, lands at 1 June
#: 1993 13:30:10.6 IST against the printed 13:30:04. The birth time is given
#: to the minute, and the Sun covers about 2.4 arcseconds a minute of clock
#: time, so a rounded birth time alone accounts for it. Example 118's residual
#: was nine seconds.
THE_VARSHA_PRAVESH_REPRODUCES_TO_SEVEN_SECONDS = (
    "Section 27.1's solar return gives 1 June 1993 13:30:10.6 IST against "
    "the printed 13:30:04, a difference of 6.6 seconds, which a birth time "
    "printed to the minute covers on its own."
)

#: **Finding.** Every printed longitude in Chart 67 reproduces within **one
#: arcminute**, and every difference is **positive** — ten bodies, ten
#: positive residuals between 0.14' and 0.93'. That is D-80's pattern again:
#: the diagram truncates the arcminute where our value carries the fraction.
CHART_67_TRUNCATES_LIKE_CHART_66 = (
    "All ten of Chart 67's printed longitudes reproduce within one "
    "arcminute and every residual is positive, which is the truncation D-80 "
    "recorded for Chart 66."
)

#: **Finding.** The five reasons the marriage paragraph gives are all
#: checkable and all hold. The vivaha saham is Table 74's with the
#: thirty-degree correction applied — **2 Sg 22** against the printed 2°22' —
#: the lagna's Jupiter is both the 7th lord and the saham's lord, Mercury is
#: in his own Gemini, the Mercury–Jupiter ithasala is a **vartamaana** at 6.20°
#: against a binding deeptamsa of 7, and in the navamsa Jupiter and Venus sit
#: in Aries, the 2nd from a Pisces lagna, with Mercury in the 9th.
EVERY_REASON_IN_THE_PARAGRAPH_CHECKS_OUT = (
    "The saham, both lordships, the own sign, the ithasala and both navamsa "
    "placements all reproduce. The ithasala is the closest call: 6.20 "
    "degrees against Mercury's deeptaamsa of 7."
)

#: **Finding.** The vivaha saham needs the **thirty-degree correction** and is
#: the second saham in the book to show it working on a printed number, after
#: Example 121's samartha. It is also the third printed vivaha saham overall,
#: after Chart 53's, and the first that both needs the correction and is cast
#: in a **day** chart — the varsha pravesh is at 1:30 pm.
THE_VIVAHA_SAHAM_NEEDS_THE_CORRECTION = (
    "Venus minus Saturn plus lagna gives 2 Sc 21 and the lagna is not on the "
    "arc from Saturn to Venus, so the thirty degrees are added and the saham "
    "is 2 Sg 22, which is what the book prints."
)

#: **Finding.** The muntha is drawn in Capricorn and §28.1's rule puts it
#: there: an Aries natal lagna advanced one rasi a year reaches Capricorn in
#: the native's 22nd year, which 1993 is. The chart prints no muntha longitude,
#: only the box, so this is the rule checked against a diagram.
THE_MUNTHA_IN_CAPRICORN_IS_28_1S_RULE = (
    "Chart 18's lagna is Aries and 1993-94 is the native's 22nd year, so "
    "section 28.1's muntha is Aries plus 21, which is Capricorn. The diagram "
    "draws it in Capricorn."
)

#: **Finding.** All eight chara karakas match the printed chart, and one pair
#: is decided by **1.6 arcminutes**: the Moon at 4.812° and Mercury at 4.786°
#: settle PK against GK. Chart 67 is a sharper test of the scheme than most
#: nativities because of it.
THE_KARAKA_ORDER_TURNS_ON_1_6_ARCMINUTES = (
    "Mars AK, Sun AmK, Rahu BK, Jupiter MK, Saturn PiK, Moon PK, Mercury GK "
    "and Venus DK all match, and the Moon and Mercury are 1.6 arcminutes "
    "apart."
)

#: **Finding, and it removes a hypothesis from OI-103.** Chart 67's HL and GL
#: miss, like every chart in the book that prints them, and a **single**
#: sunrise explains both: fitting one sunrise to the printed HL reproduces the
#: printed GL to 0.38 arcminutes. That instant, 05:32:31 IST, lies 39 seconds
#: after our upper-limb sunrise and 33 seconds before disc-centre — 54% of the
#: way between them, at 16 N 15. OI-103 recorded 23% at 26 N and 53% at 43 N
#: and suggested the offset diverged with latitude. The lowest latitude of the
#: four now gives the highest fraction, so it does not.
THE_SUNRISE_OFFSET_IS_NOT_A_FUNCTION_OF_LATITUDE = (
    "One sunrise at 05:32:31 IST reproduces Chart 67's printed HL exactly "
    "and its GL to 0.38 arcminutes. It sits 54% of the way from upper limb "
    "to disc centre at 16 N 15, against 23% at 26 N, so the offset does not "
    "grow with latitude."
)
