"""Planetary yogas — book chapter 11 onward.

**Not the nithya yoga.** `charts/yoga.py` and `/v1/yoga` compute §1.3.9's
Sun-plus-Moon panchanga yoga, one of twenty-seven, which shares only the word.
These are the planetary combinations of chapters 11 to 14, and they live under
`charts/planetary_yogas/` and `/v1/planetary-yoga` so the two can never be
reached for by mistake.

Every yoga is declared here and detected in `charts/planetary_yogas/`. The
registry is exhaustive by construction: the service evaluates **every**
registered yoga and reports each as present or absent with its evidence, so a
yoga can never be silently skipped.

Interpretive results are PVR's own prose and live in
``data/content/yoga_results.yaml`` under the licence gate of OI-12, not here.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

# --------------------------------------------------------------------------
# §11.2 Ravi yogas
# --------------------------------------------------------------------------

RAVI_YOGA_INTRO = "Ravi yogas are the solar combinations. There are several yogas based on Sun."

#: §11.2's caveat, and the reason these yogas are worth little in a rasi chart.
#: Verified astronomically in the tests: Mercury is **never** more than one
#: sign from the Sun, and Venus is within one sign about four times in five.
RAVI_YOGA_FREQUENCY_NOTE = (
    "Because Mercury and Venus are with Sun or a sign away from him most of "
    "the time, the following yogas are very common in rasi chart. However, "
    "they are less common in divisional charts. One can apply these yogas in "
    "D-9 and D-10 in particular."
)
RAVI_YOGA_PREFERRED_CHARTS: tuple[str, ...] = ("D9", "D10")

#: §11.2.1 to §11.2.4, verbatim definitions. The detector for each is in
#: `charts/planetary_yogas/ravi.py` and is written from these sentences.
RAVI_YOGAS: tuple[dict, ...] = (
    {
        "key": "vesi",
        "name": "Vesi Yoga",
        "aliases": (),
        "section": "11.2.1",
        "definition": (
            "If there is a planet other than Moon in the 2nd house from Sun, "
            "then this yoga is present."
        ),
        "example": (
            "If Sun is in Gemini and Jupiter and Mercury are in Cancer, then "
            "this yoga is present."
        ),
        "houses_from_sun": (2,),
        "excludes": (Graha.MOON,),
    },
    {
        "key": "vosi",
        "name": "Vosi Yoga",
        "aliases": (),
        "section": "11.2.2",
        "definition": (
            "If there is a planet other than Moon in the 12th house from Sun, "
            "then this yoga is present."
        ),
        "example": (
            "If Sun is in Aries and Jupiter and Venus are in Pisces, then this "
            "yoga is present."
        ),
        "houses_from_sun": (12,),
        "excludes": (Graha.MOON,),
    },
    {
        "key": "ubhayachara",
        "name": "Ubhayachara Yoga",
        "aliases": (),
        "section": "11.2.3",
        "definition": (
            "If there are planets other than Moon in the 2nd and 12th houses "
            "from Sun, then this yoga is present."
        ),
        "example": (
            "If Sun is in Cancer, Mars is in Leo and Venus is in Gemini, then "
            "this yoga is present."
        ),
        "houses_from_sun": (2, 12),
        "excludes": (Graha.MOON,),
    },
    {
        "key": "budha_aaditya",
        "name": "Budha-Aaditya Yoga",
        "aliases": ("Nipuna Yoga",),
        "section": "11.2.4",
        "definition": (
            "Budha means Mercury, Aaditya means Sun and yoga means "
            "togetherness. If Sun and Mercury are together (in one sign), this "
            "yoga is present."
        ),
        "example": None,
        "houses_from_sun": (1,),
        "excludes": (),
    },
)

#: §11.2.4's word-by-word gloss, and the alias's own.
BUDHA_AADITYA_TERMS = {
    "budha": "Mercury", "aaditya": "Sun", "yoga": "togetherness",
    "nipuna": "an expert",
}

#: §11.2.4's note. Combustion weakens a yoga but does not cancel it — "lose
#: **some** of their power to do good", not all — so the engine reports
#: combustion alongside a present yoga rather than suppressing it.
COMBUSTION_WEAKENS_YOGA = (
    "If Mercury is too close to Sun, he is combust (asta or astangata). Yogas "
    "formed by combust planets lose some of their power to do good."
)
BUDHA_AADITYA_CHART_NOTE = (
    "This yoga is the most powerful in divisional charts like D-10. In rasi "
    "chart also, it can give results if Mercury is not combust."
)

#: §11.2.4's worked reading. The only place chapter 11 so far says *when* a
#: yoga's results are felt.
BUDHA_AADITYA_TIMING_CHART = "D10"
BUDHA_AADITYA_TIMING_SIGN = 4
BUDHA_AADITYA_TIMING_TEXT = (
    "Suppose someone has Sun and Mercury together in Leo in D-10. Then that "
    "person has a powerful Budha-Aditya yoga in career. The results will be "
    "felt throughout one's life and the periods of Sun, Mercury and Leo will "
    "give those results in particular."
)
#: The two grahas whose periods carry the yoga. The sign's own period — Leo —
#: belongs to a rasi dasa, which is not built; see docs/not-yet-consumed.md.
BUDHA_AADITYA_TIMING_PERIODS: tuple[int, ...] = (Graha.SUN, Graha.MERCURY)

#: §11.2.4 writes the name "Budha-Aaditya" in its heading and "Budha-Aditya"
#: in the worked reading below it. Both forms appear on the same page.
BUDHA_AADITYA_SPELLING_VARIANTS: tuple[str, ...] = ("Budha-Aditya",)
