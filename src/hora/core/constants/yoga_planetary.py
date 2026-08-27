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


# --------------------------------------------------------------------------
# §11.3 Chandra yogas
# --------------------------------------------------------------------------

CHANDRA_YOGA_INTRO = (
    "Chandra yogas are the lunar combinations. There are several yogas based "
    "on Moon."
)

#: §11.3's three General Guidelines. **Not yogas.** Each is a graded reading
#: that always yields a verdict, where a yoga is present or absent — so they
#: are computed and returned separately rather than registered.
CHANDRA_GUIDELINE_1 = (
    "If Moon is in a quadrant from Sun, then one may possess little wealth, "
    "intelligence and skills. If Moon is in a panapara from Sun, then one may "
    "possess average wealth, intelligence and skills. If Moon is in an "
    "apoklima from Sun, then one may possess a lot of wealth, intelligence "
    "and skills."
)

#: The grading of guideline 1, keyed by the category of the Moon's house from
#: the Sun. Note the direction: the *apoklimas*, the weakest houses elsewhere
#: in the book, give the most here.
CHANDRA_MOON_FROM_SUN_GRADE = {
    "kendra": "little wealth, intelligence and skills",
    "panaphara": "average wealth, intelligence and skills",
    "apoklima": "a lot of wealth, intelligence and skills",
}

#: §11.3 writes "panapara" where chapter 7 writes "panaphara". Same category.
PANAPHARA_SPELLING_VARIANTS: tuple[str, ...] = ("panapara",)

CHANDRA_GUIDELINE_2 = (
    "If Moon is in own navamsa or that of an adhimitra (good friend), that is "
    "good. In such a situation, aspect of Jupiter on Moon beings wealth and "
    "comforts in the case of daytime birth (respectively). The same result is "
    "given by Venusian aspect on Moon in the case of night birth. On the other "
    "hand, Jupiter's aspect on Moon in a night birth and Venusian aspect on "
    "Moon in a daytime birth are detrimental to one's wealth and comforts."
)

#: Guideline 2's day/night rule, as a table. The benefit is not the graha's:
#: the *same* aspect helps in one half of the day and harms in the other.
CHANDRA_ASPECT_BY_BIRTH_TIME = {
    ("jupiter", "day"): "good", ("jupiter", "night"): "detrimental",
    ("venus", "night"): "good", ("venus", "day"): "detrimental",
}

#: Guideline 2 prints "beings" for "brings", and its "(respectively)" has two
#: things to pair with only if it looks back to "own navamsa or that of an
#: adhimitra" — own giving wealth and adhimitra's giving comforts. Recorded
#: rather than resolved. See docs/open-items.md OI-74.
CHANDRA_GUIDELINE_2_RESPECTIVELY_NOTE = (
    "The word “(respectively)” pairs two things with two things. The only "
    "pair in reach is “own navamsa or that of an adhimitra”, which would give "
    "wealth from the first and comforts from the second. The book does not "
    "say so."
)

CHANDRA_GUIDELINE_3 = (
    "If all the natural benefics occupy upachayas (3rd, 6th, 10th and 11th) "
    "from Moon, one has great wealth. If two benefics occupy upachayas from "
    "Moon, the native has medium wealth. If only one benefic occupies an "
    "upachaya from Moon, the native has little wealth."
)
CHANDRA_BENEFICS_IN_UPACHAYA_GRADE = {
    "all": "great wealth", 2: "medium wealth", 1: "little wealth",
}

#: §11.3.1 to §11.3.6. Each mirrors a Ravi yoga except Kemadruma and Adhi.
CHANDRA_YOGAS: tuple[dict, ...] = (
    {
        "key": "sunaphaa",
        "name": "Sunaphaa Yoga",
        "aliases": (),
        "section": "11.3.1",
        "definition": (
            "If there are planets other than Sun in the 2nd house from Moon, "
            "this yoga is present."
        ),
        "example": (
            "If Moon is in Gemini and Jupiter and Mercury are in Cancer, then "
            "this yoga is present."
        ),
        "houses_from_moon": (2,),
        "mirrors": "vesi",
    },
    {
        "key": "anaphaa",
        "name": "Anaphaa Yoga",
        "aliases": (),
        "section": "11.3.2",
        "definition": (
            "If there are planets other than Sun in the 12th house from Moon, "
            "this yoga is present."
        ),
        "example": (
            "If Moon is in Aries and Jupiter and Venus are in Pisces, then "
            "this yoga is present."
        ),
        "houses_from_moon": (12,),
        "mirrors": "vosi",
    },
    {
        "key": "duradhara",
        "name": "Duradhara Yoga",
        "aliases": (),
        "section": "11.3.3",
        "definition": (
            "If there are planets other than Sun in the 2nd and 12th houses "
            "from Moon, this yoga is present."
        ),
        "example": (
            "If Moon is in Cancer, Mars is in Leo and Venus is in Gemini, then "
            "this yoga is present."
        ),
        "houses_from_moon": (2, 12),
        "mirrors": "ubhayachara",
    },
    {
        "key": "kemadruma",
        "name": "Kemadruma Yoga",
        "aliases": (),
        "section": "11.3.4",
        "definition": (
            "If there are no planets other than Sun in the 1st, 2nd and 12th "
            "houses from Moon and if there are no planets other than Moon in "
            "the quadrants from lagna, this bad yoga is present."
        ),
        "example": (
            "If lagna is in Taurus, Moon is in Virgo, no planets other than "
            "Sun in Leo, Virgo and Libra and no planets in Taurus, Leo, "
            "Scorpio and Aquarius, then this yoga is present."
        ),
        "houses_from_moon": (1, 2, 12),
        "mirrors": None,
    },
    {
        "key": "chandra_mangala",
        "name": "Chandra-Mangala Yoga",
        "aliases": (),
        "section": "11.3.5",
        "definition": (
            "If Moon and Mars are together (in one sign), then this yoga is "
            "present."
        ),
        "example": None,
        "houses_from_moon": (1,),
        "mirrors": "budha_aaditya",
    },
    {
        "key": "adhi",
        "name": "Adhi Yoga",
        "aliases": (),
        "section": "11.3.6",
        "definition": (
            "If the natural benefics occupy 6th, 7th and 8th from Moon, this "
            "yoga is present."
        ),
        "example": (
            "If Moon is in Taurus, Mercury and Jupiter in Virgo and Venus is "
            "Leo, then this yoga is present."
        ),
        "houses_from_moon": (6, 7, 8),
        "mirrors": None,
    },
)

#: §11.3.4's cross-yoga claim. Kemadruma does not stop another yoga forming —
#: it kills what that yoga would have given — so it is applied as a qualifier
#: on other yogas and never flips their `present`.
KEMADRUMA_KILLS_OTHER_YOGAS = (
    "This bad yoga kills the results of other good yogas in the chart, "
    "especially Chandra yogas."
)
KEMADRUMA_EFFORT_NOTE = (
    "One with this yoga has to work hard and succeed through great efforts."
)

#: §11.3.6's example does not satisfy §11.3.6's rule. Leo is the 4th and Virgo
#: the 5th from Taurus, not the 6th, 7th or 8th. The rule is followed; see
#: docs/book-deviations.md D-28 and PVR-11.
ADHI_EXAMPLE_CONTRADICTS_RULE = (
    "Section 11.3.6's example places the Moon in Taurus and the benefics in "
    "Virgo and Leo, which are the 5th and 4th from Taurus. The rule asks for "
    "the 6th, 7th and 8th. The rule is followed."
)
