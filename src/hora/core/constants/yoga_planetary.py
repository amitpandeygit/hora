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


# --------------------------------------------------------------------------
# §11.4 Pancha Mahapurusha yogas
# --------------------------------------------------------------------------

MAHAPURUSHA_TERMS = {"pancha": "five", "mahapurusha": "a great person"}
MAHAPURUSHA_INTRO = (
    "Pancha mahapurusha yogas give the combinations that produce 5 kinds of "
    "great persons."
)

#: §11.4 restates §3.2.8's five elements and adds two names for the set.
#: `PLANET_ELEMENT_TATTVAS` and `ELEMENT_RULER` in `constants/graha.py` were
#: transcribed from §3.2.8 and agree with §11.4 exactly — including the order,
#: which is what "(respectively)" depends on.
PANCHA_BHOOTA_NAMES = {
    "pancha bhootas": "five existences",
    "pancha tattvas": "five natures",
}
MAHAPURUSHA_ELEMENT_RULERS_SENTENCE = (
    "Mars, Mercury, Saturn, Venus and Jupiter (respectively) represent these "
    "5 elements."
)
MAHAPURUSHA_ELEMENT_ROLE = (
    "Pancha mahapurusha yogas produce five kinds of great persons with one of "
    "these 5 elements playing a predominant role in their personalities."
)

#: §11.4 writes "(fiery nature)" where §3.2.8 writes "(fiery element)".
#: Same five, differently glossed. See docs/book-deviations.md D-32.
TATTVA_GLOSS_IN_11_4 = "nature"
TATTVA_GLOSS_IN_3_2_8 = "element"

#: The five, in §11.4's order. `graha` is the ruler; `element_index` indexes
#: `PLANET_ELEMENT_NAMES`. The sign set is **derived** from `RASI_LORD` and
#: `EXALTATION_DEG` rather than transcribed — §11.4 prints it as "in other
#: words", so it is the rule's consequence, not a separate rule.
MAHAPURUSHA_YOGAS: tuple[dict, ...] = (
    {
        "key": "ruchaka", "name": "Ruchaka Yoga", "section": "11.4.1",
        "graha": Graha.MARS, "element_index": 0, "printed_signs": ("Ar", "Sc", "Cp"),
        "example": {"lagna": "Li", "graha_sign": "Ar"},
        "name_means": None,
    },
    {
        "key": "bhadra", "name": "Bhadra Yoga", "section": "11.4.2",
        "graha": Graha.MERCURY, "element_index": 1, "printed_signs": ("Ge", "Vi"),
        "example": {"lagna": "Ge", "graha_sign": "Vi"},
        "name_means": None,
    },
    {
        "key": "sasa", "name": "Sasa Yoga", "section": "11.4.3",
        "graha": Graha.SATURN, "element_index": 2, "printed_signs": ("Cp", "Aq", "Li"),
        "example": {"lagna": "Cp", "graha_sign": "Li"},
        "name_means": "rabbit",
    },
    {
        "key": "maalavya", "name": "Maalavya Yoga", "section": "11.4.4",
        "graha": Graha.VENUS, "element_index": 3, "printed_signs": ("Ta", "Li", "Pi"),
        "example": {"lagna": "Ge", "graha_sign": "Pi"},
        "name_means": None,
    },
    {
        "key": "hamsa", "name": "Hamsa Yoga", "section": "11.4.5",
        "graha": Graha.JUPITER, "element_index": 4, "printed_signs": ("Sg", "Pi", "Cn"),
        "example": {"lagna": "Sg", "graha_sign": "Pi"},
        "name_means": "swan",
    },
)

#: The sentence every one of the five repeats. Two restrictions, and the
#: second is the opposite of §11.2's preference for D-9 and D-10.
MAHAPURUSHA_REFERENCE_RULE = (
    "This yoga does not apply from Moon and it applies mainly in rasi chart."
)

#: §11.4.5's Definition opens "If Jupiter is in a quadrant in own sign or
#: exaltation sign, it is called **Ruchaka** yoga." Ruchaka is Mars's yoga,
#: named in §11.4.1. The heading reads "Hamsa Yoga" and is followed.
#: See docs/book-deviations.md D-30 and precedence.md PVR-12.
HAMSA_MISNAMED_IN_ITS_DEFINITION = "Ruchaka"

#: §11.4.4's heading reads "Maalavya Yoga"; its Definition reads "Malavya
#: yoga". See docs/book-deviations.md D-31.
MAALAVYA_SPELLING_VARIANTS: tuple[str, ...] = ("Malavya",)

#: Footnotes 29 and 30 hang off "rabbit-like" in §11.4.3's results and
#: "swan-like" in §11.4.5's. Supplied with §11.5 and now recorded as
#: `SASA_MEANS` and `HAMSA_MEANS`, which confirm the meanings taken from the
#: results sentences.
MAHAPURUSHA_FOOTNOTES_UNREAD: tuple[int, ...] = ()


# --------------------------------------------------------------------------
# §11.5 Naabhasa yogas
# --------------------------------------------------------------------------

NAABHASA_INTRO = "Naabhasa yogas are classified celestial combinations."

#: §11.5's classification. **Thirty-two names, five defined so far.** The rest
#: are listed here because the section lists them; a yoga named but not yet
#: defined is registered nowhere and appears in `NAABHASA_NOT_YET_DEFINED`, so
#: it is visibly pending rather than silently absent.
NAABHASA_CLASSIFICATION: dict[str, dict] = {
    "aasraya": {
        "count": 3,
        "names": ("Rajju", "Musala", "Nala"),
        "section": "11.5.1",
        "means": "dwelling or asylum",
        "basis": "the signs occupied by planets",
    },
    "dala": {
        "count": 2,
        "names": ("Maalaa", "Sarpa"),
        "section": "11.5.2",
        "means": None,
        "basis": "the natures of the planets occupying the quadrants",
    },
    "aakriti": {
        "count": 20,
        "names": (
            "Gadaa", "Sakata", "Sringaataka", "Vihangama", "Hala", "Vajra",
            "Yava", "Kamala", "Vaapi", "Yoopa", "Sara", "Sakti", "Danda",
            "Naukaa", "Koota", "Chatra", "Chaapa", "Ardhachandra", "Chakra",
            "Samudra",
        ),
        "section": "11.5.3",
        "means": None,
        "basis": None,
    },
    "sankhya": {
        "count": 7,
        "names": ("Veenaa", "Daama", "Paasa", "Kedaara", "Soola", "Yuga",
                  "Gola"),
        "section": "11.5.4",
        "means": None,
        "basis": None,
    },
}

#: §11.5's timing rule, and the only place so far that contrasts one family of
#: yogas with all the others. §11.2.4's Budha-Aaditya is an instance of the
#: first half: "the periods of Sun, Mercury and Leo will give those results in
#: particular".
NAABHASA_TIMING_RULE = (
    "Results of other yogas may be felt primarily during the dasas of the "
    "planets and signs involved. But the results of Naabhasa yogas are felt in "
    "all dasas."
)

AASRAYA_BASIS = (
    "Aasraya yogas are based on the signs occupied by planets. If all the "
    "planets are in movable signs or in fixed signs or in dual signs, these "
    "yogas arise."
)

#: §11.5.1 and §11.5.2's five, with the modality or nature each turns on.
#: `name_means` is the book's own gloss where it gives one — Nala is the only
#: one of the three Aasraya yogas left unglossed.
NAABHASA_YOGAS: tuple[dict, ...] = (
    {
        "key": "rajju", "name": "Rajju Yoga", "group": "aasraya",
        "section": "11.5.1", "modality": 0, "name_means": "a rope",
        "definition": (
            "If all the planets are exclusively in movable signs, this yoga "
            "is formed."
        ),
    },
    {
        "key": "musala", "name": "Musala Yoga", "group": "aasraya",
        "section": "11.5.1", "modality": 1, "name_means": "a pestle",
        "definition": (
            "If all the planets are exclusively in fixed signs, this yoga is "
            "formed."
        ),
    },
    {
        "key": "nala", "name": "Nala Yoga", "group": "aasraya",
        "section": "11.5.1", "modality": 2, "name_means": None,
        "definition": (
            "If all the planets are exclusively in dual signs, this yoga is "
            "formed."
        ),
    },
    {
        "key": "maalaa", "name": "Maalaa Yoga", "group": "dala",
        "section": "11.5.2", "nature": "benefic", "name_means": "a garland",
        "definition": (
            "If three quadrants are occupied by natural benefics, this yoga "
            "is formed."
        ),
        "weakened_by": "malefic",
        "weakened_text": (
            "If a malefic also occupies one of the quadrants, this yoga may "
            "not operate well."
        ),
        "example": {"lagna": "Ar", "placements": {"JUPITER": "Cn",
                                                  "VENUS": "Cp",
                                                  "MERCURY": "Li"}},
    },
    {
        "key": "sarpa", "name": "Sarpa Yoga", "group": "dala",
        "section": "11.5.2", "nature": "malefic", "name_means": "a serpant",
        "definition": (
            "If three quadrants are occupied by natural malefics, this yoga "
            "is formed."
        ),
        "weakened_by": "benefic",
        "weakened_text": (
            "If a benefic also occupies one of the quadrants, this yoga may "
            "not operate well."
        ),
        "example": {"lagna": "Sc", "placements": {"MARS": "Ta", "RAHU": "Le",
                                                  "KETU": "Aq"}},
    },
)

#: §11.5.2 calls Sarpa "a very bad combination" — the only yoga in chapter 11
#: the book grades that way in its own definition rather than its results.
SARPA_IS_VERY_BAD = "This is a very bad combination."

#: Named in §11.5's classification but not defined for us. **Empty** — §11.5.4
#: closed the last family. Kept, and kept published, because the guard that
#: holds "registered plus pending equals thirty-two" is what would catch a
#: future family being classified and forgotten.
NAABHASA_NOT_YET_DEFINED: tuple[str, ...] = ()

#: Footnotes 29 and 30, now supplied. They gloss the two Pancha Mahapurusha
#: names that carry a marker in §11.4.
SASA_MEANS = "a hare or a rabbit"
HAMSA_MEANS = "a swan"


# --------------------------------------------------------------------------
# §11.5.3 Aakriti yogas
# --------------------------------------------------------------------------

AAKRITI_MEANS = "a shape"
AAKRITI_BASIS = (
    "Aakriti means a shape and the many of these yogas are based on the shape "
    "of the arrangement of planets in a chart."
)

#: §11.5.3 answers the question OI-73 asks, for this family at least — and
#: attributes it rather than ruling: "by many authors".
AAKRITI_NODES_NOTE = (
    "In all these yogas, Rahu and Ketu are not counted as planets by many "
    "authors."
)

#: **The grammar rule that decides every definition here.** Eighteen of the
#: twenty read "all the planets occupy X" — the planets are the subject, so
#: the test is *confinement*: every planet lies in X. Vajra and Yava alone
#: read "the Nth house is occupied by ..." — the house is the subject, so
#: those houses must actually hold something.
AAKRITI_READING_RULE = (
    "Where a definition's subject is “all the planets”, the test is that "
    "every planet lies in the named houses. Where the subject is a house "
    "— “lagna and the 7th houses are occupied by natural benefics” "
    "— that house must be occupied."
)

_KENDRA_HOUSES = (1, 4, 7, 10)
_PANAPHARA_HOUSES = (2, 5, 8, 11)
_APOKLIMA_HOUSES = (3, 6, 9, 12)


def _run(start: int, length: int) -> tuple[int, ...]:
    return tuple((start - 1 + step) % 12 + 1 for step in range(length))


#: §11.5.3's twenty. `alternatives` is the set of house-lists any one of which
#: the planets may be confined to; a yoga with one alternative names one list.
#: Derived where the book derives it — Gadaa's "two successive quadrants" is
#: computed from the quadrants, not typed out.
AAKRITI_YOGAS: tuple[dict, ...] = (
    {
        "key": "gadaa", "name": "Gadaa Yoga", "name_means": "a mace or a bludgeon",
        "definition": (
            "If all the planets occupy two successive quadrants from lagna, "
            "this yoga is formed."
        ),
        "alternatives": tuple(
            (_KENDRA_HOUSES[i], _KENDRA_HOUSES[(i + 1) % 4]) for i in range(4)
        ),
        "example_note": "4th and 7th (or 10th and 1st)",
    },
    {
        "key": "sakata", "name": "Sakata Yoga", "name_means": "a cart",
        "definition": (
            "If all the planets occupy 1st and 7th houses from lagna, this "
            "yoga is formed."
        ),
        "alternatives": ((1, 7),),
    },
    {
        "key": "vihanga", "name": "Vihanga Yoga", "name_means": "a bird",
        "definition": (
            "If all the planets occupy 4th and 10th houses from lagna, this "
            "yoga is formed."
        ),
        "alternatives": ((4, 10),),
        "aliases": ("Vihaga Yoga",),
        "alias_note": "Some authors call this Vihaga yoga.",
    },
    {
        "key": "sringaataka", "name": "Sringaataka Yoga",
        "name_means": "a cross-road junction",
        "name_means_note": "It has some other popular meanings too.",
        "definition": (
            "If all the planets occupy trines (1st, 5th and 9th) from lagna, "
            "this yoga is formed."
        ),
        "alternatives": ((1, 5, 9),),
    },
    {
        "key": "hala", "name": "Hala Yoga", "name_means": "a plough",
        "definition": (
            "If all the planets occupy mutual trines but not trines from "
            "lagna, this yoga is formed."
        ),
        "alternatives": ((2, 6, 10), (3, 7, 11), (4, 8, 12)),
        "excludes_alternative": (1, 5, 9),
    },
    {
        "key": "vajra", "name": "Vajra Yoga", "name_means": "a diamond",
        "definition": (
            "If lagna and the 7th houses are occupied by natural benefics and "
            "the 4th and 10th houses are occupied by natural malefics, this "
            "yoga is formed."
        ),
        "benefic_houses": (1, 7), "malefic_houses": (4, 10),
    },
    {
        "key": "yava", "name": "Yava Yoga",
        "name_means": "a grain among other things",
        "definition": (
            "If lagna and the 7th houses are occupied by natural malefics and "
            "the 4th and 10th houses are occupied by natural benefics, this "
            "yoga is formed."
        ),
        "benefic_houses": (4, 10), "malefic_houses": (1, 7),
    },
    {
        "key": "kamala", "name": "Kamala Yoga", "name_means": "a lotus",
        "definition": (
            "If all the planets are in quadrants from lagna, this yoga is "
            "formed."
        ),
        "alternatives": (_KENDRA_HOUSES,),
    },
    {
        "key": "vaapi", "name": "Vaapi Yoga",
        "name_means": "a pond or a water tank or a well",
        "definition": (
            "If all the planets are panaparas or in apoklimas, this yoga is "
            "formed."
        ),
        "alternatives": (_PANAPHARA_HOUSES, _APOKLIMA_HOUSES),
        "union_alternative": _PANAPHARA_HOUSES + _APOKLIMA_HOUSES,
    },
    {
        "key": "yoopa", "name": "Yoopa Yoga",
        "name_means": "a pillar and in particular a sacrificial post",
        "definition": (
            "If all the planets are in 1st, 2nd, 3rd and 4th houses from "
            "lagna, this yoga is formed."
        ),
        "alternatives": (_run(1, 4),),
    },
    {
        "key": "sara", "name": "Sara Yoga", "name_means": "an arrow",
        "definition": (
            "If all the planets are in 4th, 5th, 6th and 7th houses from "
            "lagna, this yoga is formed."
        ),
        "alternatives": (_run(4, 4),),
    },
    {
        "key": "sakti", "name": "Sakti Yoga",
        "name_means": "energy, and it is also a powerful weapon",
        "definition": (
            "If all the planets are in 7th, 8th, 9th and 10th houses from "
            "lagna, this yoga is formed."
        ),
        "alternatives": (_run(7, 4),),
    },
    {
        "key": "danda", "name": "Danda Yoga",
        "name_means": "a stick used to punish people",
        "definition": (
            "If all the planets are in 10th, 11th, 12th and 1st houses from "
            "lagna, this yoga is formed."
        ),
        "alternatives": (_run(10, 4),),
    },
    {
        "key": "naukaa", "name": "Naukaa Yoga", "name_means": "a ship",
        "definition": (
            "If all the planets occupy the 7 signs from lagna, this yoga is "
            "formed."
        ),
        "alternatives": (_run(1, 7),),
    },
    {
        "key": "koota", "name": "Koota Yoga", "name_means": "a group",
        "name_means_note": "It has several other meanings.",
        "definition": (
            "If all the planets occupy the 7 signs from the 4th house, this "
            "yoga is formed."
        ),
        "alternatives": (_run(4, 7),),
    },
    {
        "key": "chatra", "name": "Chatra Yoga", "name_means": "an umbrella",
        "definition": (
            "If all the planets occupy the 7 signs from the 7th house, this "
            "yoga is formed."
        ),
        "alternatives": (_run(7, 7),),
    },
    {
        "key": "chaapa", "name": "Chaapa Yoga", "name_means": "a bow",
        "definition": (
            "If all the planets occupy the 7 signs from the 10th house, this "
            "yoga is formed."
        ),
        "alternatives": (_run(10, 7),),
    },
    {
        "key": "ardha_chandra", "name": "Ardha Chandra Yoga",
        "name_means": "half-Moon",
        "definition": (
            "If all the planets occupy the 7 signs starting from a panapara "
            "or an apoklima, this yoga is formed."
        ),
        "alternatives": tuple(
            _run(start, 7)
            for start in sorted(_PANAPHARA_HOUSES + _APOKLIMA_HOUSES)
        ),
    },
    {
        "key": "chakra", "name": "Chakra Yoga", "name_means": "a wheel",
        "name_means_note": "Chakravarti means an emperor.",
        "definition": (
            "If all the planets occupy 1st, 3rd, 5th, 7th, 9th and 11th "
            "houses, this yoga is formed."
        ),
        "alternatives": ((1, 3, 5, 7, 9, 11),),
    },
    {
        "key": "samudra", "name": "Samudra Yoga",
        "name_means": "a sea or an ocean",
        "name_means_note": (
            "Samudra is also the name of the God of Ocean, who has a lot of "
            "wealth and many gems with him."
        ),
        "definition": (
            "If all the planets occupy 2nd, 4th, 6th, 8th, 10th and 12th "
            "houses, this yoga is formed."
        ),
        "alternatives": ((2, 4, 6, 8, 10, 12),),
    },
)

#: §11.5's classification list and §11.5.3's own headings disagree on two
#: names and on one ordering. The headings win — a definitional section beats
#: a passing mention. See docs/book-deviations.md D-33.
AAKRITI_NAME_VARIANTS: dict[str, tuple[str, ...]] = {
    "vihanga": ("Vihangama", "Vihaga"),
    "ardha_chandra": ("Ardhachandra",),
}
AAKRITI_ORDER_DIFFERS = (
    "§11.5's classification lists Sringaataka before Vihangama; §11.5.3 "
    "defines Vihanga before Sringaataka."
)


# --------------------------------------------------------------------------
# §11.5.4 Sankhya yogas
# --------------------------------------------------------------------------

SANKHYA_MEANS = "a number"
SANKHYA_BASIS = (
    "Sankhya yogas are based on the number of distinct signs occupied by the "
    "seven planets combined. Rahu and Ketu are not included."
)

#: **The clearest statement in the book on the node question.** §11.5.3 said
#: the nodes are "not counted as planets by many authors" — attribution.
#: §11.5.4 rules: "Rahu and Ketu are not included." See OI-73.
SANKHYA_EXCLUDES_NODES = "Rahu and Ketu are not included."

#: §11.5.4's precedence rule. A Sankhya yoga is not merely weaker than the
#: other Naabhasa families — it does not apply at all when one of them does.
#: The only rule in chapter 11 where one yoga's presence depends on another's
#: absence.
SANKHYA_IS_A_FALLBACK = (
    "These yogas apply if no other Naabhasa yogas mentioned previously are "
    "applicable in a chart. These are the least important of all Naabhasa "
    "yogas."
)

#: §11.5.4's worked example: Lord Sri Rama's chart, Figure 1. The section
#: gives the signs occupied rather than the chart, so the sign count is
#: checkable and the fallback condition is only partly so — Figure 1 has not
#: been supplied and the lagna is unknown.
#: Figure 1 is §1.3.4's own Example 1, drawn in all three chart styles, and
#: `tests/unit/test_book_1_3_4.py` has held it as a fixture since chapter 1.
#: So the example is fully checkable — lagna included.
SANKHYA_EXAMPLE = {
    "chart": "Lord Sri Rama (Figure 1, from §1.3.4's Example 1)",
    "signs": ("Ar", "Ta", "Cn", "Li", "Cp", "Pi"),
    "count": 6,
    "yoga": "daama",
    "lagna": "Cn",
    "figure_supplied": True,
}

#: What Rama's chart settles. The only earlier Naabhasa yoga in it is a Sarpa
#: carrying §11.5.2's own weakening clause — benefics in the fourth quadrant.
#: Counted as applicable, it would supersede Daama and make §11.5.4's rule
#: contradict §11.5.4's example. Not counted, rule and example agree.
#:
#: So "applicable" is read as excluding a yoga the book itself says "may not
#: operate well". See docs/open-items.md OI-80 and precedence.md PVR-13.
WEAKENED_YOGA_IS_NOT_APPLICABLE = (
    "A yoga the book says “may not operate well” does not count as applicable "
    "for section 11.5.4's fallback. Lord Sri Rama's chart forces this: its "
    "only earlier Naabhasa yoga is a weakened Sarpa, and the book gives the "
    "chart as Daama."
)


#: The seven, by the number of distinct signs the seven planets occupy.
#: Gola's definition is phrased differently — "if the seven planets are in one
#: sign" rather than "occupy exactly 1 distinct sign" — but means the same.
SANKHYA_YOGAS: tuple[dict, ...] = (
    {"key": "veenaa", "name": "Veenaa Yoga", "signs": 7,
     "name_means": "a stringed musical instrument",
     "aliases": ("Vallaki Yoga",),
     "alias_note": "This is also called Vallaki yoga by some authors."},
    {"key": "daama", "name": "Daama Yoga", "signs": 6,
     "name_means": "a wreath",
     "aliases": ("Daamini Yoga",),
     "alias_note": "Some authors call this Daamini yoga."},
    {"key": "paasa", "name": "Paasa Yoga", "signs": 5,
     "name_means": "a noose", "aliases": (), "alias_note": None},
    {"key": "kedaara", "name": "Kedaara Yoga", "signs": 4,
     "name_means": "a field", "aliases": (), "alias_note": None},
    {"key": "soola", "name": "Soola Yoga", "signs": 3,
     "name_means": "Shiva's weapon", "aliases": (), "alias_note": None},
    {"key": "yuga", "name": "Yuga Yoga", "signs": 2,
     "name_means": "a pair", "aliases": (), "alias_note": None},
    {"key": "gola", "name": "Gola Yoga", "signs": 1,
     "name_means": "a sphere or a globe", "aliases": (), "alias_note": None,
     "definition_differs": (
         "Gola alone is phrased “if the seven planets are in one sign” "
         "rather than “occupy exactly 1 distinct sign”."
     )},
)


# --------------------------------------------------------------------------
# §11.6 Other popular yogas
# --------------------------------------------------------------------------

POPULAR_YOGA_INTRO = "Some other important combinations will be listed below."

#: §11.6's governing rule, and it binds **every** yoga in the section: a yoga
#: is fully present only when the combinations hold *and* the planets are
#: strong. Chapter 15's simple-rules measure is not built, so the engine can
#: report the combinations and never fullness. See OI-81.
POPULAR_YOGA_FULLNESS_RULE = (
    "Sometimes the results of a dasa may be felt even if all the required "
    "combinations are not present. But, for a yoga to be fully present, all "
    "the required combinations must be present and the participating planets "
    "must be strong."
)
STRENGTH_NOT_ASSESSED = (
    "Section 11.6 requires the participating planets to be strong for the "
    "yoga to be fully present. Strength is not computed — chapter 15's "
    "simple-rules measure is not built — so this verdict reports the "
    "combinations only."
)

#: Footnote 31, in full. Kartari is its own construction, reusable against any
#: house or planet, and two of §11.6's yogas are built on it.
KARTARI_MEANS = "scissors"
KARTARI_DEFINITION = (
    "Kartari literally means “scissors”. The 12th and 2nd houses from a "
    "house cast kartari on it. If the 2nd and 12th from a house have benefics, "
    "it is said to have a subha (benefic) kartari. Malefics in the same places "
    "cause paapa (malefic) kartari."
)
KARTARI_EFFECT = (
    "Subha kartari on any house does good to the matters of that house and "
    "paapa kartari does harm."
)
KARTARI_IS_GENERAL = (
    "Subha kartari and paapa kartari are also known as “subha kartari yoga” "
    "and “paapa kartari yoga” and they can be seen with reference to any "
    "house or planet."
)
KARTARI_HOUSES: tuple[int, ...] = (12, 2)

#: §11.6's eighteen. `clauses` are what the engine can decide; `strength`
#: lists what it cannot. `alternatives` holds an "Alternately, ..." rule, of
#: which the whole clause set is an independent way to satisfy the yoga.
POPULAR_YOGAS: tuple[dict, ...] = (
    {
        "key": "subha", "name": "Subha Yoga", "name_means": None,
        "definition": (
            "If lagna has benefics or has “subha kartari” — benefics in "
            "12th and 2nd — then this yoga is present."
        ),
    },
    {
        "key": "asubha", "name": "Asubha Yoga", "name_means": None,
        "definition": (
            "If lagna has malefics or has “paapa kartari” — malefics in "
            "12th and 2nd — then this yoga is present."
        ),
    },
    {
        "key": "gaja_kesari", "name": "Gaja-Kesari Yoga", "name_means": None,
        "definition": (
            "If (1) Jupiter is in a quadrant from Moon, (2) a benefic planet "
            "conjoins or aspects Jupiter, and, (3) Jupiter is not debilitated "
            "or combust or in an enemy's house, then this yoga is present."
        ),
        "variant": (
            "Some authors consider Gaja-Kesari yoga to be present even when "
            "Jupiter is in a quadrant from lagna and not Moon. If he is "
            "strong, this yoga can be present even without a benefic's aspect "
            "or conjunction."
        ),
        "printed_typo": "Juputer",
    },
    {
        "key": "guru_mangala", "name": "Guru-Mangala Yoga", "name_means": None,
        "definition": (
            "If Jupiter and Mars are together or in the 7th house from each "
            "other, then this yoga is present."
        ),
    },
    {
        "key": "amala", "name": "Amala Yoga", "name_means": "pure",
        "definition": (
            "If there are only natural benefics in the 10th house from lagna "
            "or Moon, then this yoga is present."
        ),
        "reason": (
            "Because the 10th house shows one conduct in society, situation of "
            "only benefics there makes one's conduct in the society very pure."
        ),
    },
    {
        "key": "parvata", "name": "Parvata Yoga", "name_means": "a mountain",
        "definition": (
            "If (1) quadrants are occupied only by benefics and (2) the 7th "
            "and 8th houses are either vacant or occupied only by benefics, "
            "then this yoga is present."
        ),
    },
    {
        "key": "kaahala", "name": "Kaahala Yoga",
        "name_means": "excessive. It also means mischievous",
        "definition": (
            "If (1) the 4th lord and Jupiter are in mutual quadrants and "
            "(2) lagna lord is strong, then this yoga is present."
        ),
        "alternative": (
            "Alternately, this yoga is present if the 4th lord is exalted or "
            "in own sign and the 10th lord joins him."
        ),
        "footnote": "Some say “9th lord” instead of Jupiter",
        "strength": ("lagna lord",),
    },
    {
        "key": "chaamara", "name": "Chaamara Yoga",
        "name_means": (
            "something akin to the plume on the head of a horse. By waving it, "
            "servants give relief to kings from heat (like a fan). It "
            "basically stands for the trappings of power"
        ),
        "definition": (
            "If the lagna lord is exalted in a quadrant with Jupiter's aspect "
            "or two benefics join in 7th, 9th or 10th, then this yoga is "
            "present."
        ),
    },
    {
        "key": "sankha", "name": "Sankha Yoga", "name_means": "a conch shell",
        "definition": (
            "If (1) lagna lord is strong and (2) 5th and 6th lords are in "
            "mutual quadrants, then this yoga is present."
        ),
        "alternative": (
            "Alternately, this yoga is present if (1) lagna lord and 10th lord "
            "are together in a movable sign and (2) the 9th lord is strong."
        ),
        "strength": ("lagna lord", "9th lord"),
    },
    {
        "key": "bheri", "name": "Bheri Yoga", "name_means": "a kettledrum",
        "definition": (
            "If (1) the 9th lord is strong and (2) 1st, 2nd, 7th and 12th "
            "houses are occupied by planets, then this yoga is present."
        ),
        "alternative": (
            "Alternately, this is yoga is present if (1) the 9th lord is "
            "strong and (2) Jupiter, Venus and lagna lord are in mutual "
            "quadrants."
        ),
        "strength": ("9th lord",),
    },
    {
        "key": "mridanga", "name": "Mridanga Yoga",
        "name_means": (
            "a rich and elegant percussion instrument popular in south India"
        ),
        "definition": (
            "If (1) there are planets in own and exaltation signs in quadrants "
            "and trines and (2) lagna lord is strong, then this yoga is "
            "present."
        ),
        "strength": ("lagna lord",),
    },
    {
        "key": "sreenaatha", "name": "Sreenaatha Yoga",
        "name_means": (
            "the lord of great wealth and prosperity. It also means Vishnu"
        ),
        "definition": (
            "If (1) the 7th lord is exalted in 10th and (2) 10th lord is with "
            "9th lord, then this yoga is present."
        ),
        "footnote": (
            "If this is to be applied strictly, 7th lord can be exalted in "
            "10th only for Sagittarius lagna."
        ),
    },
    {
        "key": "matsya", "name": "Matsya Yoga", "name_means": "a fish",
        "definition": (
            "If (1) benefics are in lagna and 9th, (2) some planets are in "
            "5th, and, (3) malefics are in chaturasras (4th and 8th houses), "
            "then this yoga is present."
        ),
    },
    {
        "key": "koorma", "name": "Koorma Yoga", "name_means": "a tortoise",
        "definition": (
            "If (1) the 5th, 6th and 7th houses are occupied by benefics who "
            "are in own, exaltation or friendly signs and (2) the 1st, 3rd and "
            "11th houses are occupied by malefics who are in own or exaltation "
            "signs, then this yoga is present."
        ),
    },
    {
        "key": "khadga", "name": "Khadga Yoga", "name_means": "a sword",
        "definition": (
            "If (1) the 2nd lord is in the 9th house, (2) the 9th lord is in "
            "the 2nd house, and, (3) lagna lord is in a quadrant or a trine, "
            "then this yoga is present."
        ),
    },
    {
        "key": "kusuma", "name": "Kusuma Yoga", "name_means": "a flower",
        "definition": (
            "If (1) lagna is in a fixed sign, (2) Venus is in a quadrant, "
            "(3) Moon is in a trine with a benefic, and, (4) Saturn is in the "
            "10th house, then this yoga is present."
        ),
    },
    {
        "key": "kalaanidhi", "name": "Kalaanidhi Yoga",
        "name_means": "a treasure of arts and skills",
        "definition": (
            "If (1) Jupiter is in the 2nd house or the 5th house and (2) he is "
            "conjoined or aspected by Mercury and Venus, then this yoga is "
            "present."
        ),
    },
    {
        "key": "kalpadruma", "name": "Kalpadruma Yoga",
        "name_means": "a celestial tree of the heaven",
        "aliases": ("Paarijaata Yoga",),
        "alias_note": (
            "This yoga is also known as Paarijaata yoga. Paarijaata is a "
            "celestial flower."
        ),
        "definition": (
            "Consider (1) lagna lord, (2) his dispositor, (3) the latter's "
            "dispositor in rasi and (4) in navamsa. If all the four planets "
            "are all in quadrants, trines or exaltation signs, then this yoga "
            "is present."
        ),
        "simplification_rejected": (
            "Some authors have simplified this yoga and wrote that one of the "
            "last two planets mentioned can bring the yoga if in a quadrant or "
            "a trine or exaltation sign. Taking all the four planets make this "
            "a less common yoga, which it ought to be. Let us follow Parasara."
        ),
    },
)

#: §11.6's own count, checked against the list.
POPULAR_YOGA_COUNT = 18


#: Footnote 34, on the Kalpadruma results §11.6 prints and we have not been
#: given. It is the only sight we have of that paragraph: it quotes three of
#: its words.
KALPADRUMA_RESULTS_FOOTNOTE = (
    "This is not meant negatively. War and curbing bad elements are a king's "
    "duty. The results of this yoga include the words “principled” "
    "and “kind”. So the expression “likes wars” "
    "(yuddhapriyah) should be taken in a positive sense. Shivaji's example "
    "may explain it further.")

#: The three words footnote 34 quotes out of that results paragraph.
KALPADRUMA_RESULT_WORDS: tuple[str, ...] = (
    "principled", "kind", "likes wars")

KALPADRUMA_RESULT_WORD_SANSKRIT = "yuddhapriyah"

#: §11.6's worked example of Kalpadruma yoga: Chart 9, Chatrapati Shivaji.
KALPADRUMA_EXAMPLE_WALKTHROUGH = (
    "As an example, let us look at the rasi and navamsa charts of Chatrapati "
    "Shivaji, a great king of India (see Chart 9). Lagna lord is Sun. He is "
    "in Aq and his dispositor is Saturn (lord of Aq). Saturn is in Li and his "
    "dispositor is Venus. We also need Saturn's dispositor in navamsa. In "
    "navamsa, Saturn is in Aq and his dispositor is Saturn himself.")

KALPADRUMA_EXAMPLE_CONCLUSION = (
    "Thus we get the four planets as — Sun, Saturn, Venus and Saturn. "
    "Sun is in a quadrant. Saturn is exalted. Venus is in a trine. Thus "
    "Shivaji had Kalpadruma yoga. In navamsa also, Sun is exalted, Saturn is "
    "in moolatrikona and Venus is in a lagna.")

#: The four links the example names, in the order it names them. The fourth
#: repeats the second's navamsa dispositor, which is Saturn again.
KALPADRUMA_EXAMPLE_CHAIN: tuple[str, ...] = ("Sun", "Saturn", "Venus", "Saturn")

#: §11.6's closing sentence about the example says Venus "is in a lagna" in
#: navamsa. Chart 9's own navamsa diagram puts Venus in Gemini and the navamsa
#: lagna in Sagittarius, so Venus is in the 7th — a quadrant, not the lagna,
#: and no special lagna the chart draws sits in Gemini either. See
#: docs/book-deviations.md D-34.
KALPADRUMA_EXAMPLE_NAVAMSA_LAGNA_CLAIM = "Venus is in a lagna"
