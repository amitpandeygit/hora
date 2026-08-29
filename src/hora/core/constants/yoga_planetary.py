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


# --------------------------------------------------------------------------
# 11.6, continued — thirty more popular yogas
#
# The section's list runs on past the Shivaji example. These thirty are not
# Shivaji's yogas; he is used only for Kalpadruma. Unlike the first eighteen,
# each of these prints its own Results sentence, which is transcribed in
# data/content/yoga_results.yaml.
# --------------------------------------------------------------------------

#: Footnote 35, defining the exchange three of these yogas turn on.
PARIVARTANA_FOOTNOTE = (
    "That means that the 2nd lord is in the 10th house and the 10th lord is "
    "in the 2nd house. Exchange is called \u201cparivartana\u201d in Sanskrit.")

PARIVARTANA_SANSKRIT = "parivartana"

#: NOTE (1) after Brahma yoga.
TRIMURTHI_NOTE = (
    "Some authors combine Hari yoga, Hara yoga and Brahma yoga and call it "
    "\u201cHari Hara Brahma yoga\u201d. Also, these three yogas are known as "
    "Trimurthi Yogas. Brahma is the Creator; Hari is the Sustainer; and, "
    "Shiva is the Destroyer. They form the Trinity of Gods (Trimurthis).")

TRIMURTHI_YOGAS: tuple[str, ...] = ("hari", "hara", "brahma")
TRIMURTHI_COMBINED_NAME = "Hari Hara Brahma yoga"

#: NOTE (2) after Brahma yoga: a second definition, kept beside the first.
BRAHMA_VARIATION = (
    "If (1) Jupiter is in a quadrant from the 9th lord, (2) Venus is in a "
    "quadrant from the 11th lord, and, (3) Mercury is in a quadrant from the "
    "1st lord or 10th lord, then this yoga is present.")

#: §11.6 says Lagnaadhi "means Adhi Yoga from lagna", but its own definition
#: takes only the 7th and 8th, where §11.3.6's Adhi takes the 6th, 7th and
#: 8th from Moon. The definition is followed. See docs/book-deviations.md.
LAGNAADHI_GLOSS = (
    "Adhi means over or above. We have already seen Adhi Yoga among Chandra "
    "yogas. Lagnaadhi yoga means Adhi Yoga from lagna.")
LAGNAADHI_HOUSES: tuple[int, ...] = (7, 8)
ADHI_HOUSES_FROM_MOON: tuple[int, ...] = (6, 7, 8)

POPULAR_YOGAS_CONTINUED: tuple[dict, ...] = (
    {"key": "lagnaadhi", "name": "Lagnaadhi Yoga", "name_means": None,
     "definition": ("If (1) the 7th and 8th houses from lagna are occupied by "
                    "benefics and (2) no malefics conjoin or aspect these "
                    "planets, then this yoga is present."),
     "gloss": LAGNAADHI_GLOSS},
    {"key": "hari", "name": "Hari Yoga",
     "name_means": "a name of Lord Vishnu",
     "definition": ("If benefics occupy the 2nd, 12th and 8th houses counted "
                    "from the 2nd lord, then this yoga is present."),
     "reason": ("The 2nd house is the house of food and money and it is a "
                "trine from karma sthana \u2013 the 10th house. It stands for "
                "sustenance and its lord represents Hari \u2013 Sustainer of "
                "Hindu Trinity \u2013 in a chart.")},
    {"key": "hara", "name": "Hara Yoga",
     "name_means": "a name of Lord Shiva",
     "definition": ("If benefics occupy the 4th, 9th and 8th houses counted "
                    "from the 7th lord, then this yoga is present."),
     "reason": ("The 7th house rules death and Shiva is represented by its "
                "lord. This is why the 7th house shows genitalia and Shiva "
                "is worshipped in the form of a Linga \u2013 Phallus \u2013 in "
                "Hindu temples.")},
    {"key": "brahma", "name": "Brahma Yoga",
     "name_means": "the creator of this universe",
     "definition": ("If benefics occupy the 4th, 10th and 11th houses counted "
                    "from lagna lord, then this yoga is present."),
     "reason": ("Lagna rules birth and the Creator is represented in a chart "
                "by lagna lord."),
     "variant": BRAHMA_VARIATION},
    {"key": "vishnu", "name": "Vishnu Yoga", "name_means": None,
     "definition": ("If (1) the 9th and 10th lords are in the 2nd house and "
                    "(2) the lord of the sign occupied in navamsa by the 9th "
                    "lord in rasi chart is also in the 2nd house, then this "
                    "yoga is present."),
     "needs_navamsa": True},
    {"key": "siva", "name": "Siva Yoga",
     "name_means": "one of the Trinity of Gods",
     "definition": ("If (1) the 5th lord is in the 9th house, (2) the 9th "
                    "lord is in the 10th house, and, (3) the 10th lord is in "
                    "the 5th house, then this yoga is present.")},
    {"key": "trilochana", "name": "Trilochana Yoga",
     "name_means": ("\u201cone with three eyes\u201d. It is another name of Lord "
                    "Siva, who has a hidden eye in His forehead"),
     "definition": ("If Sun, Moon and Mars are in mutual trines, then this "
                    "yoga is present.")},
    {"key": "gouri", "name": "Gouri Yoga",
     "name_means": ("a form of Parvati \u2013 Lord Siva\u2019s wife. She is an "
                    "epitome of marital bliss and purity"),
     "definition": ("If the lord of the sign occupied in navamsa by the 10th "
                    "lord is exalted in the 10th house and lagna lord joins "
                    "him, then this yoga is present."),
     "needs_navamsa": True},
    {"key": "chandikaa", "name": "Chandikaa Yoga",
     "name_means": ("an aggressive form of Parvati. She kills demons "
                    "mercilessly"),
     "definition": ("If (1) lagna is in a fixed sign aspected by 6th lord and "
                    "(2) Sun joins the lords of the signs occupied in navamsa "
                    "by 6th and 9th lords, then this yoga is present."),
     "needs_navamsa": True},
    {"key": "lakshmi", "name": "Lakshmi Yoga",
     "name_means": "Vishnu\u2019s wife. She is the goddess of prosperity",
     "definition": ("If (1) the 9th lord is in an own sign or in his "
                    "exaltation sign that happens to be quadrant from lagna "
                    "and (2) lagna lord is strong, then this yoga is present."),
     "strength": ("lagna lord",)},
    {"key": "saarada", "name": "Saarada Yoga",
     "name_means": ("another name of Saraswathi, the goddess of learning"),
     "definition": ("If (1) the 10th lord is in the 5th house, (2) Mercury is "
                    "in a quadrant, (3) Sun is strong in Leo, (4) Mercury or "
                    "Jupiter is in a trine from Moon, and, (5) Mars is in "
                    "11th, then this yoga is present."),
     "strength": ("Sun",)},
    {"key": "bhaarathi", "name": "Bhaarathi Yoga",
     "name_means": ("another name of Saraswathi, the goddess of learning"),
     "definition": ("If the lord of the sign occupied in navamsa by 2nd, 5th "
                    "or 11th lord exalted and joins the 9th lord, then this "
                    "yoga is present."),
     "printed_typo": ("the definition reads \u201cis occupied in navamsa by 2nd, "
                      "5th or 11th lord exalted and joins\u201d, with no verb "
                      "before \u201cexalted\u201d; read as \u201cis exalted and joins\u201d"),
     "needs_navamsa": True},
    {"key": "saraswathi", "name": "Saraswathi Yoga",
     "name_means": "the goddess of learning",
     "definition": ("If (1) each of Mercury, Jupiter and Venus occupies a "
                    "quadrant or a trine or the 2nd house (not necessarily "
                    "together) and (2) Jupiter is in an own or friendly or "
                    "exaltation sign, then this yoga is present.")},
    {"key": "amsaavatara", "name": "Amsaavatara Yoga",
     "name_means": "one who is an incarnation of a part of the Lord",
     "definition": ("If Jupiter, Venus and exalted Saturn are in quadrants, "
                    "then this yoga is present.")},
    {"key": "devendra", "name": "Devendra Yoga",
     "name_means": "the ruler of gods",
     "definition": ("If (1) lagna is in a fixed sign, (2) 2nd and 10th lords "
                    "have an exchange, and, (3) lagna and 11th lords have an "
                    "exchange, then this yoga is present."),
     "footnote": PARIVARTANA_FOOTNOTE},
    {"key": "indra", "name": "Indra Yoga",
     "name_means": "the ruler of gods",
     "definition": ("If (1) the 5th and 11th lords have an exchange and (2) "
                    "Moon occupies the 5th house, then this yoga is present.")},
    {"key": "ravi", "name": "Ravi Yoga", "name_means": "Sun",
     "definition": ("If (1) Sun is in the 10th house and (2) the 10th lord is "
                    "in the 3rd house with Saturn, then this yoga is present."),
     "alias_note": ("Not to be confused with the four Ravi yogas of section "
                    "11.2, which are a family and not a yoga of this name.")},
    {"key": "bhaaskara", "name": "Bhaaskara Yoga",
     "name_means": "\u201cone with bright rays\u201d. It is a name of Sun",
     "definition": ("If (1) Moon is in the 12th from Sun, (2) Mercury is in "
                    "the 2nd from Sun, and, (3) Jupiter is in the 5th or 9th "
                    "from Moon, then this yoga is present.")},
    {"key": "kulavardhana", "name": "Kulavardhana Yoga",
     "name_means": ("Kula means \u201clineage or community\u201d. Vardhana means "
                    "\u201cone who makes it grow and prosper\u201d"),
     "definition": ("If each planet occupies the 5th house from either lagna "
                    "or Moon or Sun, then this yoga is present.")},
    {"key": "vasumati", "name": "Vasumati Yoga", "name_means": "earth",
     "definition": ("If benefics occupy upachayas, then this yoga is "
                    "present."),
     "fullness": ("For it to give full results, malefics should not occupy "
                  "upachayas and the benefics occupying upachayas should be "
                  "strong."),
     "strength": ("benefics occupying upachayas",)},
    {"key": "gandharva", "name": "Gandharva Yoga",
     "name_means": ("a class of gods with excellent skills in singing and "
                    "other fine arts"),
     "definition": ("If (1) the 10th lord is in a trine from the 7th house, "
                    "(2) lagna lord is conjoined or aspected by Jupiter, (3) "
                    "Sun is exalted and strong, and, (4) Moon is in the 9th "
                    "house, then this yoga is present."),
     "strength": ("Sun",)},
    {"key": "go", "name": "Go Yoga", "name_means": "a cow",
     "definition": ("If (1) Jupiter is strong in his moolatrikona, (2) the "
                    "lord of the 2nd house is with Jupiter, and, (3) lagna "
                    "lord is exalted, then this yoga is present."),
     "strength": ("Jupiter",),
     "printed_typo": "resepcted"},
    {"key": "vidyut", "name": "Vidyut Yoga",
     "name_means": "a lightning bolt or electricity",
     "definition": ("If (1) the 11th lord is in deep exaltation, (2) he joins "
                    "Venus, and, (3) the two of them are in a quadrant from "
                    "lagna lord, then this yoga is present."),
     "needs_longitudes": True},
    {"key": "chapa", "name": "Chapa Yoga", "name_means": "a bow",
     "definition": ("If (1) the 4th and 10th lords have an exchange and (2) "
                    "lagna lord is exalted, then this yoga is present.")},
    {"key": "pushkala", "name": "Pushkala Yoga", "name_means": "abundant",
     "definition": ("If (1) lagna lord is with Moon, (2) dispositor of Moon "
                    "is in a quadrant or in the house of an adhimitra (good "
                    "friend), (2) dispositor of Moon aspects lagna, and, (4) "
                    "there is a planet in lagna, then this yoga is present."),
     "printed_typo": ("the clauses are numbered (1), (2), (2), (4); the third "
                      "is read as (3)")},
    {"key": "makuta", "name": "Makuta Yoga", "name_means": "crown",
     "definition": ("If (1) Jupiter is in the 9th house from the 9th lord, "
                    "(2) the 9th house from Jupiter has a benefic, and, (3) "
                    "Saturn is in the 10th house, then this yoga is present.")},
    {"key": "jaya", "name": "Jaya Yoga", "name_means": "victorious",
     "definition": ("If (1) the 10th lord is in deep exaltation and (2) the "
                    "6th lord is debilitated, then this yoga is present."),
     "needs_longitudes": True},
    {"key": "harsha", "name": "Harsha Yoga", "name_means": "joyous",
     "definition": ("If the 6th lord occupies the 6th house, then this yoga "
                    "is present.")},
    {"key": "sarala", "name": "Sarala Yoga", "name_means": "straight-forward",
     "definition": ("If the 8th lord occupies the 8th house, then this yoga "
                    "is present.")},
    {"key": "vimala", "name": "Vimala Yoga", "name_means": "pure",
     "definition": ("If the 12th lord occupies the 12th house, then this yoga "
                    "is present.")},
)

#: §11.6's three "the lord occupies his own house" yogas, printed together
#: at the end of the section: Harsha (6th), Sarala (8th) and Vimala (12th).
DUSTHANA_LORD_IN_OWN_HOUSE: tuple[str, ...] = ("harsha", "sarala", "vimala")


POPULAR_YOGA_CONTINUED_COUNT = len(POPULAR_YOGAS_CONTINUED)

#: Every §11.6 yoga, first eighteen and the thirty that follow the Shivaji
#: example. They are one list in the book; the split here is only the order
#: in which the section was read.
POPULAR_YOGAS_ALL: tuple[dict, ...] = POPULAR_YOGAS + POPULAR_YOGAS_CONTINUED
POPULAR_YOGA_TOTAL = len(POPULAR_YOGAS_ALL)


# --------------------------------------------------------------------------
# 11.7 Raaja yogas
# --------------------------------------------------------------------------

RAAJA_MEANS = "a king"

RAAJA_YOGA_INTRO = (
    "Raaja means a king. Raaja yogas are the combinations that give power and "
    "prosperity to a native. They make one the best in something.")

RAAJA_BASIC_PREMISE = (
    "In any chart, Lord Vishnu sits in the quadrants and Goddess Lakshmi sits "
    "in the trines. If the lord of a quadrant is associated with the lord of "
    "a trine, that association brings the combined blessings of Lakshmi and "
    "Vishnu. This is called a Raaja Yoga. The native is powerful and "
    "prosperous.")

#: The three associations §11.7.1 names, in the order printed.
RAAJA_ASSOCIATIONS: tuple[dict, ...] = (
    {"key": "conjunction",
     "text": "The two planets are conjoined,"},
    {"key": "mutual_drishti",
     "text": "The two planets aspect each other with graha drishti, or,"},
    {"key": "parivartana",
     "text": ("The two planets have a parivartana (exchange). For example, if "
              "the 4th lord is in the 5th house and the 5th lord is in the "
              "4th house, then we say that there is a parivartana between the "
              "4th and 5th lords. This is an association.")},
)

RAAJA_ASSOCIATION_RULE = (
    "If the lord of a quadrant and the lord of a trine have one of the three "
    "kinds of associations mentioned above, it forms a Raaja Yoga. Lagna can "
    "be taken as a quadrant or a trine here. It is both.")

#: "Lagna can be taken as a quadrant or a trine here. It is both."
LAGNA_IS_BOTH_QUADRANT_AND_TRINE = True

DHARMA_KARMADHIPATI_DEFINITION = (
    "This is a special case of the above yoga. If the lords of dharma sthana "
    "(9th) and karma sthana (10th) form a raja yoga, it is known by this "
    "special name.")

DHARMA_KARMADHIPATI_REASON = (
    "The 9th house is the most important trine and the 10th house is the most "
    "important quadrant. Raja yoga involving the lords of these two houses is "
    "excellent.")

#: Printed exactly so, breaking off mid-sentence.
DHARMA_KARMADHIPATI_RESULTS_TRUNCATED = (
    "One born with this yoga is sincere, devoted and righteous. He is "
    "fortunate and.")

DHARMA_STHANA = 9
KARMA_STHANA = 10

TRIK_STHANA_NAMES: tuple[str, ...] = ("trik sthanas", "dusthanas")

VIPAREETA_MEANS = "extreme"

VIPAREETA_DEFINITION = (
    "The 6th, 8th and 12th houses are known as trik sthanas or dusthanas (bad "
    "houses). If their lords occupies dusthanas or conjoin dusthanas, it "
    "results in this yoga.")

VIPAREETA_REASON = (
    "Because dusthanas show the obstacles one faces in life, situation of "
    "dusthana lords in dusthanas shows that obstacles will run into obstacles "
    "themselves. One experiences tremendous success in the face of obstacles.")

VIPAREETA_IDEAL_CASE = (
    "In the ideal case, the lords of the 6th, 8th and 12th houses will all be "
    "together in one of the three houses (or the 3rd house or the 11th "
    "house), with no other planets conjoining them. But the results of this "
    "yoga may be experienced with just one or two dusthana lords occupying a "
    "dusthana.")

#: The ideal case admits two houses that are not dusthanas at all.
VIPAREETA_IDEAL_HOUSES: tuple[int, ...] = (6, 8, 12, 3, 11)

RAAJA_YOGAS: tuple[dict, ...] = (
    {"key": "raaja_basic", "name": "Basic Raaja Yoga", "name_means": None,
     "definition": RAAJA_ASSOCIATION_RULE,
     "premise": RAAJA_BASIC_PREMISE},
    {"key": "dharma_karmadhipati", "name": "Dharma-Karmadhipati Yoga",
     "name_means": ("dharma sthana is the 9th and karma sthana is the 10th; "
                    "adhipati means lord"),
     "definition": DHARMA_KARMADHIPATI_DEFINITION,
     "reason": DHARMA_KARMADHIPATI_REASON},
    {"key": "vipareeta_raaja", "name": "Vipareeta Raaja Yoga",
     "name_means": VIPAREETA_MEANS,
     "definition": VIPAREETA_DEFINITION,
     "reason": VIPAREETA_REASON,
     "ideal": VIPAREETA_IDEAL_CASE,
     "printed_typo": ("the definition reads “their lords occupies "
                      "dusthanas”; read as “occupy”")},
)

RAAJA_YOGA_COUNT = len(RAAJA_YOGAS)


# --------------------------------------------------------------------------
# 11.7.2 Magnitude of a Raaja yoga
#
# Not a yoga: a grading of one that is already present.
# --------------------------------------------------------------------------

RAAJA_MAGNITUDE_INTRO = (
    "We find the conjunction of the lords of a quadrant and a trine in many "
    "charts. The magnitude to which this raaja yoga fructifies depends on the "
    "strength of the two planets. The key factors that come into play are:")

RAAJA_MAGNITUDE_FACTORS: tuple[dict, ...] = (
    {"key": "unafflicted",
     "text": ("The two planets should be free from afflictions from "
              "functional malefics.")},
    {"key": "close",
     "text": ("The conjunction or aspect responsible for the Raaja Yoga "
              "should be close (say, within 6° or so).")},
    {"key": "unblemished",
     "text": ("The two planets should not be combust, debilitated or in an "
              "inimical house or in bad avasthas (states).")},
)

#: "within 6° or so" — the book's only number, and it is hedged twice.
RAAJA_CLOSE_ORB_DEGREES = 6.0
RAAJA_CLOSE_ORB_IS_APPROXIMATE = True

RAAJA_ORB_EXAMPLE = (
    "If Mercury and Venus are at 2° and 26° in Ta for a native with Cp lagna, "
    "for example, their conjunction brings a Raaja Yoga (Dharma-Karmadhipati "
    "Yoga in particular). However, the two planets are too far apart for this "
    "yoga to give its full results. They are still associated, but the "
    "association is not very strong. If Venus is at 3° in Ta in instead of "
    "26°, the conjunction is very close and the yoga can give its full "
    "results, if other factors are favorable.")

RAAJA_BLEMISH_RULE = (
    "Any blemishes here will considerably reduce the magnitude of the yoga.")

PARASARA_DASA_VARGA_RULE = (
    "In addition to the above factors, Sage Parasara recommended looking at "
    "the amsas occupied by the 2 planets as per Dasa Varga (ten division) "
    "scheme. Count the divisional charts – out of the ten charts of Dasa "
    "Varga scheme – in which a planet occupies an own, exaltation or "
    "moolatrikona sign. Based on the count of divisional charts with such a "
    "good placement for the planet in question, we say that it is in a "
    "particular amsa. Please see the chapter “Divisional Charts” for details.")

#: What §11.7.2 says each dasavarga count amounts to, keyed by the count.
#: Counts 0 and 1 share one sentence; 10 is not discussed at all.
RAAJA_AMSA_RESULTS: tuple[dict, ...] = (
    {"count": 0, "amsa": None,
     "result": ("the yoga is ordinary and gives good results depending on the "
                "factors already outlined")},
    {"count": 1, "amsa": None,
     "result": ("the yoga is ordinary and gives good results depending on the "
                "factors already outlined")},
    {"count": 2, "amsa": "Paarijaataamsa",
     "result": "one becomes a king who rules his people well"},
    {"count": 3, "amsa": "Uttamaamsa",
     "result": "one becomes a good king with tremendous assets"},
    {"count": 4, "amsa": "Gopuraamsa",
     "result": "one becomes a great king respected by many kings"},
    {"count": 5, "amsa": "Simhaasanaamsa",
     "result": "one becomes a great emperor who rules the whole world"},
    {"count": 6, "amsa": "Paaraavataamsa", "result": None},
    {"count": 7, "amsa": "Devalokaamsa", "result": None},
    {"count": 8, "amsa": "Brahmalokamsa", "result": None},
    {"count": 9, "amsa": "Airaavataamsa", "result": None},
)

#: §6.6's table names a tenth amsa, Sreedhaamaamsa. §11.7.2 stops at nine.
RAAJA_AMSA_COUNT_NOT_DISCUSSED = 10

RAAJA_AMSA_DIVINE_COUNTS: tuple[int, ...] = (6, 7, 8, 9)

RAAJA_AMSA_DIVINE_RULE = (
    "Two planets giving Raaja Yoga can be in Paaraavataamsa (count of 6), "
    "Devalokamsa (count of 7), Brahmalokaamsa (count of 8) and Airaavataamsa "
    "(count of 9) only for divine persons such as Svaayambhuva Manu (Manu who "
    "was born by Himself), Brahma (Creator!!) and Vishnu’s incarnations such "
    "as Sri Rama and Sri Krishna.")

RAAJA_AMSA_DIVINE_PERSONS: tuple[str, ...] = (
    "Svaayambhuva Manu", "Brahma", "Sri Rama", "Sri Krishna")

SIMHAASANAAMSA_RULE = (
    "Parasara said that several great emperors of Indian mythology – like "
    "Harischandra, Manu, Bali, Vaiswaanara, Yudhisthira (also known as "
    "Dharmaraja) and Saalivaahana – were born with this combination.")

SIMHAASANAAMSA_EMPERORS: tuple[str, ...] = (
    "Harischandra", "Manu", "Bali", "Vaiswaanara", "Yudhisthira",
    "Saalivaahana")

#: Footnote 36 hangs off "Saalivaahana" and was not supplied.
SIMHAASANAAMSA_FOOTNOTE_UNREAD = "36"

RAAJA_FINAL_JUDGMENT = (
    "None of the above factors influences the end result completely. We "
    "should look at all the factors and make the final judgment.")

#: §11.7.2 spells three of §6.6's amsa names differently. §6.6 is the
#: definitional table and wins; the variants are recorded so a caller
#: matching the §11.7.2 spelling still finds the amsa.
AMSA_SPELLINGS_IN_11_7_2: dict[str, str] = {
    "Uttamsaamsa": "Uttamaamsa",
    "Devalokamsa": "Devalokaamsa",
    "Brahmalokaamsa": "Brahmalokamsa",
}


#: Everything §11.7.2 lets us say about functional malefics, which it uses
#: without ever defining — see docs/open-items.md OI-88.
#:
#: **Two data points, not a rule.** Nothing here is generalised: a lagna the
#: book has not spoken about is simply absent, and the Leo entry records a
#: constraint (one of three planets) rather than a name, because the book
#: names none.
FUNCTIONAL_MALEFIC_DATA_POINTS: dict[str, dict] = {
    "Libra": {
        "named": ("Jupiter",),
        "candidates": (),
        "example": "Chart 10, Emperor Akbar",
        "text": ("They are afflicted by a functional malefic (Jupiter), but "
                 "Jupiter is 22° away from them."),
    },
    "Leo": {
        "named": (),
        # The Sun and Jupiter are the yoga's own planets; these three are the
        # rest of Leo, and the book says only that malefics were among them.
        "candidates": ("Moon", "Mercury", "Venus"),
        "example": "Rajiv Gandhi, footnote 37",
        "text": "functional malefics were with them",
    },
}

FUNCTIONAL_MALEFIC_NOT_DEFINED = (
    "Section 11.7.2 asks that the two planets be free from afflictions from "
    "functional malefics, but no section read so far says what a functional "
    "malefic is. It cannot be section 3.2.2's natural malefics, which do not "
    "depend on the lagna. See docs/open-items.md OI-88.")


# --------------------------------------------------------------------------
# 11.7.3 More Raja Yogas — eighteen advanced combinations
# --------------------------------------------------------------------------

ADVANCED_RAAJA_INTRO = "Some advanced Raaja Yogas will be listed below."

#: Footnote 38, on §11.7.2's closeness rule. Supplied after §11.7.2 was
#: written up, where it was recorded as unread.
RAAJA_ORB_FOOTNOTE = (
    "Anything greater than 5 or 6 degrees is too large for a Raaja Yoga to "
    "give its full results.")

#: Footnote 39. Its second sentence settles the calendar question Chart 10
#: raises: 24 November 1542 Julian is 4 December 1542 Gregorian.
CHART_10_BIRTH_FOOTNOTE = (
    "Birthdata: December 4, 1542, 3:39 am (LMT), 69 E 47, 25 N 19. This date "
    "may be written by some as November 24, 1542 based on the old calendar.")

CHART_10_OLD_CALENDAR_DATE = "November 24, 1542"
CHART_10_TIME_IS_LMT = True

#: §11.7.3 (7) names the six shadvarga charts in words.
SHADVARGA_NAMED_IN_11_7_3: tuple[str, ...] = (
    "Rasi", "Navamsa", "Hora", "Drekkana", "Dwadasamsa", "Trimsamsa")

#: §11.7.3 (9) names three of them.
TRIVARGA_NAMED_IN_11_7_3: tuple[str, ...] = ("Rasi", "Navamsa", "Drekkana")

ADVANCED_RAAJA_YOGAS: tuple[dict, ...] = (
    {"number": 1, "key": "raaja_pk_ak_and_lords",
     "name": "Raaja Yoga (11.7.3 #1) — PK with AK, lagna lord with 5th lord",
     "definition": ("If (a) chara putra karaka (PK) and chara atmaka karaka "
                    "(AK) are conjoined and (b) lagna and 5th lords conjoin, "
                    "then Raaja Yoga is present and the native enjoys power "
                    "and prosperity."),
     "partial": ("If only one condition is satisfied, still the results may "
                 "be felt, but not fully."),
     "needs_karakas": True},
    {"number": 2, "key": "raaja_maharajah",
     "name": "Raaja Yoga (11.7.3 #2) — the Maharajah combination",
     "definition": ("If (a) lagna lord is in 5th, (b) 5th lord is in lagna, "
                    "(c) AK and PK are in lagna or the 5th house, and (d) "
                    "those planets in owns rasi or amsa or in exaltation or "
                    "aspected by benefics, then this yoga is present and the "
                    "native becomes a great king (Maharajah) loved by his "
                    "associates."),
     "printed_typo": "“in owns rasi”, for “in own rasi”",
     "needs_karakas": True, "needs_navamsa": True},
    {"number": 3, "key": "raaja_ninth_lord_and_ak",
     "name": "Raaja Yoga (11.7.3 #3) — 9th lord and AK",
     "definition": ("If the 9th lord and AK are in lagna, 5th or 7th, "
                    "aspected by benefics, then Raaja Yoga is present."),
     "needs_karakas": True},
    {"number": 4, "key": "raaja_benefics_from_lord_and_ak",
     "name": "Raaja Yoga (11.7.3 #4) — benefics in the 2nd, 4th and 5th",
     "definition": ("If the 2nd, 4th and 5th houses from lagna lord and AK "
                    "are occupied by benefics, one becomes a king."),
     "needs_karakas": True},
    {"number": 5, "key": "raaja_malefics_from_lord_and_ak",
     "name": "Raaja Yoga (11.7.3 #5) — malefics in the 3rd and 6th",
     "definition": ("If the 3rd and 6th houses from lagna lord and AK are "
                    "occupied or aspected by malefics, one becomes a king."),
     "needs_karakas": True},
    {"number": 6, "key": "raaja_lagna_hl_gl_one_planet",
     "name": "Raaja Yoga (11.7.3 #6) — one planet on lagna, HL and GL",
     "definition": ("If lagna, HL and GL are joined or aspected by the same "
                    "planet, then that planet gives a Raaja Yoga. One may add "
                    "“owned” to “joined or aspected”."),
     "partial": ("Results of this yoga may be experienced if the conditions "
                 "are not strictly met, but a planet has an association with "
                 "lagna (or lagna lord), HL (or HL lord) and GL (or GL lord). "
                 "Association here can mean ownership, conjunction or aspect. "
                 "If lagna lord is in HL and aspects GL lord, for example, "
                 "results of this Raaja Yoga may be experienced to some "
                 "extent."),
     "reason": ("Planets aspecting or joining HL and GL give wealth and power "
                "respectively. If such a planet is associated with lagna "
                "also, its potential to do good increases."),
     "needs_special_lagnas": ("HL", "GL")},
    {"number": 7, "key": "raaja_shadvarga_lagna_aspect",
     "name": "Raaja Yoga (11.7.3 #7) — one planet aspecting lagna in all six",
     "definition": ("If the same planet aspects lagna in the six divisional "
                    "charts of shad vargas – Rasi, Navamsa, Hora, Drekkana, "
                    "Dwadasamsa, Trimsamsa – then that planet gives a Raaja "
                    "Yoga."),
     "needs_navamsa": True, "needs_lagna_longitude": True},
    {"number": 8, "key": "raaja_dignified_on_lagna_hl_gl",
     "name": "Raaja Yoga (11.7.3 #8) — dignified planets on lagna, HL and GL",
     "definition": ("If lagna, HL and GL are occupied by a planet in own or "
                    "exaltation sign, then the native becomes a king."),
     "note": "It can be different planets.",
     "needs_special_lagnas": ("HL", "GL")},
    {"number": 9, "key": "raaja_dignified_on_three_lagnas",
     "name": "Raaja Yoga (11.7.3 #9) — dignified planets on lagna in D-1, D-9, D-3",
     "definition": ("If lagna in Rasi, Navamsa and Drekkana charts is "
                    "occupied by a planet in own or exaltation sign, then the "
                    "native becomes a king."),
     "note": "It can be different planets.",
     "needs_navamsa": True, "needs_lagna_longitude": True},
    {"number": 10, "key": "raaja_debilitated_in_dusthanas",
     "name": "Raaja Yoga (11.7.3 #10) — debilitated planets in the 3rd, 6th and 8th",
     "definition": ("If (a) the 3rd, 6th and 8th houses are occupied by one "
                    "or two planets in debilitation and (b) lagna lord is in "
                    "an own or exaltation sign and aspects lagna, it forms a "
                    "Raaja Yoga.")},
    {"number": 11, "key": "raaja_afflicted_dusthana_lords",
     "name": "Raaja Yoga (11.7.3 #11) — afflicted 6th, 8th and 12th lords",
     "definition": ("If (a) the 6th, 8th and 12th lords are debilitated or "
                    "combust or in inimical signs and (b) lagna lord is in an "
                    "own or exaltation sign and aspects lagna, it forms a "
                    "Raaja Yoga.")},
    {"number": 12, "key": "raaja_fifth_and_ninth_lords",
     "name": "Raaja Yoga (11.7.3 #12) — the 5th and 9th lords",
     "definition": ("If the 5th and 9th lords are in a conjunction or a "
                    "mutual aspect, it makes one prosperous.")},
    {"number": 13, "key": "raaja_fourth_tenth_exchange",
     "name": "Raaja Yoga (11.7.3 #13) — the 4th/10th exchange, aspected",
     "definition": ("If (a) the 4th lord is in the 10th house and the 10th "
                    "lord is in the 4th house and (b) both of them are "
                    "aspected by the 5th lord or the 9th lord, then a Raaja "
                    "Yoga is formed.")},
    {"number": 14, "key": "raaja_fifth_lord_joined",
     "name": "Raaja Yoga (11.7.3 #14) — the 5th lord joined by the 1st or 9th",
     "definition": ("If (a) the 5th lord is in the 1st, 4th or 10th house and "
                    "(b) lagna lord or the 9th lord joins him, then the "
                    "native becomes a king.")},
    {"number": 15, "key": "raaja_vargottama_moon",
     "name": "Raaja Yoga (11.7.3 #15) — a vargottama Moon aspected by four",
     "definition": ("If (a) Moon is strong and occupies vargottamamsa and (b) "
                    "four or more planets aspect him, then one becomes a "
                    "king."),
     "strength": ("Moon",), "needs_navamsa": True},
    {"number": 16, "key": "raaja_four_dignified",
     "name": "Raaja Yoga (11.7.3 #16) — four planets in moolatrikona or exaltation",
     "definition": ("If 4 or more planets occupy moolatrikonas or exaltation "
                    "signs, one becomes a king even if he is from a lowly "
                    "family.")},
    {"number": 17, "key": "raaja_benefics_in_quadrants",
     "name": "Raaja Yoga (11.7.3 #17) — benefics in quadrants, malefics in 3/6/11",
     "definition": ("If benefics are in quadrants and malefics are in the "
                    "3rd, 6th and 11th houses, one becomes a king even if he "
                    "is from a lowly family.")},
)

ADVANCED_RAAJA_YOGA_COUNT = len(ADVANCED_RAAJA_YOGAS)

#: §11.7.3 (18) is not a yoga. It says how effective the chart's Raaja yogas
#: are, so it is reported beside them and never among them.
ARUDHA_EFFECTIVENESS_RULE = (
    "If arudha lagna and darapada (arudha pada of the 7th house) are not in "
    "mutual 2nd/12th or 6th/8th positions, then Raja Yogas in the chart will "
    "be more effective.")

ARUDHA_EFFECTIVENESS_BAD_PAIRS: tuple[tuple[int, int], ...] = (
    (2, 12), (6, 8))


#: §11.7.3 (15) asks for a strong Moon. Chapter 15's strength is not built,
#: and §11.6's note names its own section, so this one is separate.
ADVANCED_RAAJA_STRENGTH_NOT_ASSESSED = (
    "Section 11.7.3 requires this planet to be strong. Strength is not "
    "computed — chapter 15's simple-rules measure is not built — so this "
    "verdict reports the placements only. See docs/open-items.md OI-81.")


#: Footnote 40, supplied with §11.8. It closes what §11.7.3 (15) left open.
VARGOTTAMAAMSA_DEFINITION = (
    "A planet is in vargottamaamsa if it occupies the same sign in Rasi and "
    "Navamsa charts.")

#: §11.7.3's body spells it "vargottamamsa"; footnote 40 spells it
#: "vargottamaamsa". The footnote is the definition, so its spelling leads.
VARGOTTAMAAMSA_SPELLINGS: tuple[str, ...] = (
    "vargottamaamsa", "vargottamamsa")


# --------------------------------------------------------------------------
# 11.8 Raaja Sambandha Yogas
# --------------------------------------------------------------------------

SAMBANDHA_MEANS = "relation or association"

RAAJA_SAMBANDHA_INTRO = (
    "Raaja means a king. Sambandha means relation or association. Raaja "
    "sambandha yogas are the combinations that give association with rulers. "
    "Those who have these yogas are typically powerful ministers, "
    "secretaries, counsellors and bureaucrats, associated with the rulers and "
    "powerful men. However, these yogas are very common. The magnitude of "
    "success depends on the strength of the planets involved in raja yoga.")

#: The section says so itself, before listing a single one.
RAAJA_SAMBANDHA_ARE_COMMON = "However, these yogas are very common."

#: And it sends the reader back to §11.7.2 for how far one goes.
RAAJA_SAMBANDHA_MAGNITUDE_RULE = (
    "The magnitude of success depends on the strength of the planets involved "
    "in raja yoga.")

#: The chara karakas §11.8 names in full, with the spellings it uses.
SAMBANDHA_KARAKA_NAMES: dict[str, str] = {
    "AK": "chara aatma kaaraka",
    "AmK": "chara amaatya kaaraka",
}

RAAJA_SAMBANDHA_YOGAS: tuple[dict, ...] = (
    {"number": 1, "key": "sambandha_tenth_lord_amk",
     "name": "Raaja Sambandha Yoga (11.8 #1) — 10th lord reached by AmK",
     "definition": ("If the 10th lord is conjoined or aspected by AmK (chara "
                    "amaatya kaaraka) or his dispositor, one becomes an "
                    "important person in the court of a king."),
     "result": "one becomes an important person in the court of a king",
     "needs_karakas": True},
    {"number": 2, "key": "sambandha_eleventh_lord_unafflicted",
     "name": "Raaja Sambandha Yoga (11.8 #2) — an unafflicted 10th and 11th",
     "definition": ("If the 11th lord aspects the 11th house and there are no "
                    "malefic planets joining or aspecting the 10th and 11th "
                    "houses, one becomes an important person in the court of "
                    "a king."),
     "result": "one becomes an important person in the court of a king"},
    {"number": 3, "key": "sambandha_ak_amk_conjoin",
     "name": "Raaja Sambandha Yoga (11.8 #3) — AK and AmK conjoined",
     "definition": ("If AK (chara aatma kaaraka) and AmK conjoin, one is very "
                    "intelligent and becomes a minister."),
     "result": "one is very intelligent and becomes a minister",
     "needs_karakas": True},
    {"number": 4, "key": "sambandha_amk_dignified",
     "name": "Raaja Sambandha Yoga (11.8 #4) — a dignified AmK",
     "definition": ("If AmK is very strong in own sign or his exaltation "
                    "sign, then also one becomes a minister."),
     "result": "one becomes a minister",
     "strength": ("AmK",), "needs_karakas": True},
    {"number": 5, "key": "sambandha_amk_in_a_trine",
     "name": "Raaja Sambandha Yoga (11.8 #5) — AmK in a trine from lagna",
     "definition": ("If AmK is in a trine from lagna, one becomes a famous "
                    "minister."),
     "result": "one becomes a famous minister", "needs_karakas": True},
    {"number": 6, "key": "sambandha_amk_from_ak",
     "name": ("Raaja Sambandha Yoga (11.8 #6) — AmK in a quadrant or trine "
              "from AK"),
     "definition": ("If AmK is in a quadrant or a trine from AK, one is an "
                    "associate liked by a king."),
     "result": "one is an associate liked by a king", "needs_karakas": True},
    {"number": 7, "key": "sambandha_malefics_from_three",
     "name": ("Raaja Sambandha Yoga (11.8 #7) — malefics in the 3rd and 6th "
              "from lagna, AL and AK"),
     "definition": ("If malefics occupy the 3rd and 6th houses from lagna, AL "
                    "and AK, then one becomes a powerful chief of army."),
     "result": "one becomes a powerful chief of army",
     "emphasis": ("The book italicises the “and” in “lagna, AL and AK”, so "
                  "all three references are meant, not any one of them."),
     "needs_karakas": True, "needs_arudha": True},
    {"number": 8, "key": "sambandha_ak_dignified_and_ninth_lord",
     "name": ("Raaja Sambandha Yoga (11.8 #8) — a dignified AK reaching the "
              "9th lord"),
     "definition": ("If AK is in an own or exaltation sign in a quadrant or a "
                    "trine and the 9th lord is conjoined or aspected by AK, "
                    "one becomes a minister."),
     "result": "one becomes a minister", "needs_karakas": True},
    {"number": 9, "key": "sambandha_ak_is_moons_dispositor",
     "name": ("Raaja Sambandha Yoga (11.8 #9) — AK as Moon's dispositor in "
              "lagna"),
     "definition": ("If AK happens to be Moon's dispositor and he occupies "
                    "lagna along with a benefic, one becomes a minister at an "
                    "old age."),
     "result": "one becomes a minister at an old age", "needs_karakas": True},
    {"number": 10, "key": "sambandha_ak_with_a_benefic",
     "name": ("Raaja Sambandha Yoga (11.8 #10) — AK with a benefic in the "
              "5th, 7th, 9th or 10th"),
     "definition": ("If AK is in the 5th, 7th, 9th or 10th houses with a "
                    "benefic, one will be associated with kings and earn "
                    "money thus."),
     "result": "one will be associated with kings and earn money thus",
     "needs_karakas": True},
    {"number": 11, "key": "sambandha_bhagyapada_or_ak_in_ninth",
     "name": ("Raaja Sambandha Yoga (11.8 #11) — bhagyapada in lagna, or AK "
              "in the 9th"),
     "definition": ("If bhagyapada (A9 – arudha pada of the 9th house) is in "
                    "lagna or AK is in 9th, one is fortunate and associates "
                    "with kings."),
     "result": "one is fortunate and associates with kings",
     "needs_karakas": True, "needs_arudha": True},
    {"number": 12, "key": "sambandha_eleventh_lord_and_ak",
     "name": ("Raaja Sambandha Yoga (11.8 #12) — the 11th lord unafflicted "
              "and AK with benefics"),
     "definition": ("If the 11th lord is in the 11th house without aspects "
                    "from any malefics and AK is with benefics, then one has "
                    "gains from a king."),
     "result": "one has gains from a king", "needs_karakas": True},
    {"number": 13, "key": "sambandha_first_tenth_exchange",
     "name": ("Raaja Sambandha Yoga (11.8 #13) — the lagna and 10th lords "
              "exchanged"),
     "definition": ("If lagna lord is in the 10th house and the 10th lord is "
                    "in lagna, one is powerful and associated with kings."),
     "result": "one is powerful and associated with kings"},
    {"number": 14, "key": "sambandha_moon_venus_from_ak",
     "name": ("Raaja Sambandha Yoga (11.8 #14) — Moon and Venus in the 4th "
              "from AK"),
     "definition": ("If Moon and Venus are in the 4th house from AK, one is "
                    "endowed with royal insignia."),
     "result": "one is endowed with royal insignia", "needs_karakas": True},
    {"number": 15, "key": "sambandha_fifth_lord_joined",
     "name": ("Raaja Sambandha Yoga (11.8 #15) — the 5th lord joined in a "
              "quadrant or trine"),
     "definition": ("If lagna lord or AK conjoins the 5th lord in a quadrant "
                    "or a trine, one becomes a king's friend."),
     "result": "one becomes a king's friend", "needs_karakas": True},
)

RAAJA_SAMBANDHA_COUNT = len(RAAJA_SAMBANDHA_YOGAS)


# --------------------------------------------------------------------------
# 11.9 Dhana Yogas
# --------------------------------------------------------------------------

DHANA_MEANS = "wealth"

DHANA_YOGA_INTRO = (
    "Dhana means wealth. Dhana yogas are combinations that give one abundant "
    "riches.")

DHANA_BASIC_PRINCIPLE = (
    "The 5th and 9th lords and planets joining them are capable of giving "
    "money. They give dasas in their dasas. The 11th house is also important "
    "for material gains and it should be strong. The 2nd house is also "
    "important. If Moon, Mercury, Jupiter or Venus is exalted in the 2nd "
    "house, it makes the native very rich.")

#: "They give dasas in their dasas" is printed exactly so. Transcribed as
#: found; nothing is computed from it.
DHANA_PRINTED_ODDITY = "They give dasas in their dasas."

DHANA_PARASARA_NOTE = (
    "In addition to these general principles, Parasara listed specific "
    "combinations for various lagnas. In all these combinations, the strength "
    "of the participating planets decides the magnitude of results "
    "experienced.")

#: The one testable rule inside the Basic Principle.
DHANA_EXALTED_IN_SECOND: tuple[str, ...] = ("Moon", "Mercury", "Jupiter", "Venus")
DHANA_EXALTED_IN_SECOND_RULE = (
    "If Moon, Mercury, Jupiter or Venus is exalted in the 2nd house, it makes "
    "the native very rich.")

#: What the twelve lagna entries turn out to be, checked against all twelve
#: rather than assumed. Every first combination puts the **5th lord** in the
#: 5th house; every 11th-house list names the **11th lord** among its planets;
#: every second combination puts the **lagna lord** in lagna.
DHANA_STRUCTURE: tuple[str, ...] = (
    "the first combination always places the 5th lord in the 5th house",
    "the planets it wants in the 11th always include the 11th lord",
    "the second combination always places the lagna lord in lagna",
)

DHANA_YOGAS: tuple[dict, ...] = (
    # (12), for Pisces, is printed "If Moon is in the 5th house and in
    # the 11th house" and names no planet for the 11th, so no chart can
    # satisfy it. `eleventh` is empty on purpose — see D-37.
    {"number": 1, "lagna": "Ar", "fifth": "SUN",
     "eleventh": ('SATURN', 'MOON', 'JUPITER'),
     "lagna_planet": "MARS", "reachers": ('MERCURY', 'VENUS', 'SATURN'),
     "first_definition": (
         "If Sun is in the 5th house and Saturn, Moon and Jupiter are in the "
         "11th house, one becomes very affluent."),
     "second_definition": (
         "If Mars occupies lagna conjoined or aspected by Mercury, Venus and "
         "Saturn, then also one becomes very rich."),
     },
    {"number": 2, "lagna": "Ta", "fifth": "MERCURY",
     "eleventh": ('MOON', 'MARS', 'JUPITER'),
     "lagna_planet": "VENUS", "reachers": ('MERCURY', 'SATURN'),
     "first_definition": (
         "If Mercury is in the 5th house and Moon, Mars and Jupiter are in "
         "the 11th house, one becomes very affluent."),
     "second_definition": (
         "If Venus occupies lagna conjoined or aspected by Mercury and "
         "Saturn, then also one becomes very rich."),
     },
    {"number": 3, "lagna": "Ge", "fifth": "VENUS",
     "eleventh": ('MARS',),
     "lagna_planet": "MERCURY", "reachers": ('JUPITER', 'SATURN'),
     "first_definition": (
         "If Venus is in the 5th house and Mars is in the 11th house, one "
         "becomes very affluent."),
     "second_definition": (
         "If Mercury occupies lagna conjoined or aspected by Jupiter and "
         "Saturn, then also one becomes very rich."),
     },
    {"number": 4, "lagna": "Cn", "fifth": "MARS",
     "eleventh": ('VENUS',),
     "lagna_planet": "MOON", "reachers": ('MERCURY', 'JUPITER'),
     "first_definition": (
         "If Mars is in the 5th house and Venus is in the 11th house, one "
         "becomes very affluent."),
     "second_definition": (
         "If Moon occupies lagna conjoined or aspected by Mercury and "
         "Jupiter, then also one becomes very rich."),
     },
    {"number": 5, "lagna": "Le", "fifth": "JUPITER",
     "eleventh": ('MERCURY',),
     "lagna_planet": "SUN", "reachers": ('MARS', 'JUPITER'),
     "first_definition": (
         "If Jupiter is in the 5th house and Mercury is in the 11th house, "
         "one becomes very affluent."),
     "second_definition": (
         "If Sun occupies lagna conjoined or aspected by Mars and Jupiter, "
         "then also one becomes very rich."),
     },
    {"number": 6, "lagna": "Vi", "fifth": "SATURN",
     "eleventh": ('SUN', 'MOON'),
     "lagna_planet": "MERCURY", "reachers": ('JUPITER', 'SATURN'),
     "first_definition": (
         "If Saturn is in the 5th house and Sun and Moon are in the 11th "
         "house, one becomes very affluent."),
     "second_definition": (
         "If Mercury occupies lagna conjoined or aspected by Jupiter and "
         "Saturn, then also one becomes very rich."),
     },
    {"number": 7, "lagna": "Li", "fifth": "SATURN",
     "eleventh": ('SUN', 'MOON'),
     "lagna_planet": "VENUS", "reachers": ('MERCURY', 'SATURN'),
     "first_definition": (
         "If Saturn is in the 5th house and Sun and Moon are in the 11th "
         "house, one becomes very affluent."),
     "second_definition": (
         "If Venus occupies lagna conjoined or aspected by Mercury and "
         "Saturn, then also one becomes very rich."),
     },
    {"number": 8, "lagna": "Sc", "fifth": "JUPITER",
     "eleventh": ('MERCURY',),
     "lagna_planet": "MARS", "reachers": ('MERCURY', 'VENUS', 'SATURN'),
     "first_definition": (
         "If Jupiter is in the 5th house and Mercury is in the 11th house, "
         "one becomes very affluent."),
     "second_definition": (
         "If Mars occupies lagna conjoined or aspected by Mercury, Venus and "
         "Saturn, then also one becomes very rich."),
     },
    {"number": 9, "lagna": "Sg", "fifth": "MARS",
     "eleventh": ('VENUS',),
     "lagna_planet": "JUPITER", "reachers": ('MARS', 'MERCURY'),
     "first_definition": (
         "If Mars is in the 5th house and Venus is in the 11th house, one "
         "becomes very affluent."),
     "second_definition": (
         "If Jupiter occupies lagna conjoined or aspected by Mars and "
         "Mercury, then also one becomes very rich."),
     },
    {"number": 10, "lagna": "Cp", "fifth": "VENUS",
     "eleventh": ('MARS',),
     "lagna_planet": "SATURN", "reachers": ('MARS', 'JUPITER'),
     "first_definition": (
         "If Venus is in the 5th house and Mars is in the 11th house, one "
         "becomes very affluent."),
     "second_definition": (
         "If Saturn occupies lagna conjoined or aspected by Mars and "
         "Jupiter, then also one becomes very rich."),
     },
    {"number": 11, "lagna": "Aq", "fifth": "MERCURY",
     "eleventh": ('MOON', 'MARS', 'JUPITER'),
     "lagna_planet": "SATURN", "reachers": ('MARS', 'JUPITER'),
     "first_definition": (
         "If Mercury is in the 5th house and Moon, Mars and Jupiter are in "
         "the 11th house, one becomes very affluent."),
     "second_definition": (
         "If Saturn occupies lagna conjoined or aspected by Mars and "
         "Jupiter, then also one becomes very rich."),
     },
    {"number": 12, "lagna": "Pi", "fifth": "MOON",
     "eleventh": (),
     "eleventh_is_broken": True,
     "lagna_planet": "JUPITER", "reachers": ('MARS', 'MERCURY'),
     "first_definition": (
         "If Moon is in the 5th house and in the 11th house, one becomes "
         "very affluent."),
     "second_definition": (
         "If Jupiter occupies lagna conjoined or aspected by Mars and "
         "Mercury, then also one becomes very rich."),
     },
)

DHANA_YOGA_COUNT = len(DHANA_YOGAS)

DHANA_FIRST_RESULT = "one becomes very affluent"
DHANA_SECOND_RESULT = "then also one becomes very rich"

#: §11.9 (12), exactly as printed.
DHANA_PISCES_PRINTED = (
    "If Moon is in the 5th house and in the 11th house, one becomes very "
    "affluent.")

#: What the other eleven entries imply was dropped from it. Recorded as an
#: inference and **not applied** — the yoga stays undecidable. See D-37.
DHANA_PISCES_LIKELY_MISSING = "Saturn"


# --------------------------------------------------------------------------
# 11.10 Daridra Yogas
# --------------------------------------------------------------------------

DARIDRA_YOGA_INTRO = (
    "One experiences poverty if the following yogas (combinations) are "
    "present in one's chart:")

#: The NOTE after combination (1). It is the first place the book defines
#: maraka, and it confirms `charts/bhava.py`'s MARAKA = (2, 7) — see OI-23.
MARAKA_NOTE = (
    "The 2nd and 7th houses are maraka (killer houses). Their lords are "
    "marakas (killers). Any malefics occupying 2nd and 7th or associating "
    "with 2nd and 7th lords also become malefics.")

MARAKA_HOUSES: tuple[int, ...] = (2, 7)

#: The NOTE's third sentence reads "also become **malefics**", which is
#: circular — malefics becoming malefics says nothing. In context it must be
#: "also become marakas". Transcribed as printed and not silently corrected;
#: the extension it describes is computed but kept out of the base set. See
#: docs/open-items.md OI-96.
MARAKA_NOTE_CIRCULAR_CLAUSE = (
    "Any malefics occupying 2nd and 7th or associating with 2nd and 7th lords "
    "also become malefics.")

DARIDRA_YOGAS: tuple[dict, ...] = (
    {"number": 1, "key": "daridra_first_twelfth_exchange",
     "name": "Daridra Yoga (11.10 #1) — the lagna and 12th lords exchanged",
     "definition": ("Lagna lord is in 12th and 12th lord is in lagna. They "
                    "are conjoined or aspected by a maraka planet.")},
    {"number": 2, "key": "daridra_first_sixth_exchange",
     "name": "Daridra Yoga (11.10 #2) — the lagna and 6th lords exchanged",
     "definition": ("Lagna lord is in 6th and 6th lord is in lagna. They are "
                    "conjoined or aspected by a maraka planet.")},
    {"number": 3, "key": "daridra_ketu_and_eighth",
     "name": "Daridra Yoga (11.10 #3) — Ketu on lagna or Moon, lagna lord in the 8th",
     "definition": ("Lagna or Moon is with Ketu. Lagna lord is in 8th. A "
                    "maraka planet conjoins or aspects lagna lord.")},
    {"number": 4, "key": "daridra_lord_with_malefic_in_dusthana",
     "name": "Daridra Yoga (11.10 #4) — lagna lord with a malefic in a dusthana",
     "definition": ("Lagna lord is with a malefic in a dusthana (6th, 8th or "
                    "12th) and 2nd lord is debilitated or in an enemy's "
                    "sign. Even a royal scion with this combination becomes "
                    "poor."),
     "result": "Even a royal scion with this combination becomes poor."},
    {"number": 5, "key": "daridra_fifth_and_ninth_lords_fallen",
     "name": "Daridra Yoga (11.10 #5) — the 5th lord in the 6th, the 9th in the 12th",
     "definition": ("The 5th lord is in 6th and 9th lord is in 12th, with "
                    "aspects from marakas.")},
    {"number": 6, "key": "daridra_malefics_in_lagna",
     "name": "Daridra Yoga (11.10 #6) — malefics in lagna without the 9th and 10th lords",
     "definition": ("Malefics occupy lagna without 9th and 10th lords, "
                    "aspected or conjoined by marakas.")},
    {"number": 7, "key": "daridra_dispositors_in_dusthanas",
     "name": "Daridra Yoga (11.10 #7) — the dusthana lords' dispositors in dusthanas",
     "definition": ("Lords of the signs occupied by 6th, 8th and 12th lords "
                    "are in 6th, 8th and 12th houses, conjoined or aspected "
                    "by malefics.")},
    {"number": 8, "key": "daridra_moons_navamsa_dispositor",
     "name": "Daridra Yoga (11.10 #8) — the Moon's navamsa dispositor with a maraka",
     "definition": ("Lord of the sign occupied by Moon in navamsa is with a "
                    "maraka or occupies a maraka house (2nd and 7th)."),
     "needs_navamsa": True},
    {"number": 9, "key": "daridra_both_lagna_lords",
     "name": "Daridra Yoga (11.10 #9) — the rasi and navamsa lagna lords reached by marakas",
     "definition": ("Lords of lagna in rasi and navamsa are conjoined or "
                    "aspected by marakas."),
     "needs_navamsa": True},
    {"number": 10, "key": "daridra_benefics_and_malefics_swapped",
     "name": "Daridra Yoga (11.10 #10) — benefics in malefic houses and the reverse",
     "definition": ("Benefics are in malefic houses and malefics are in "
                    "benefic houses."),
     "undefined_terms": ("malefic houses", "benefic houses")},
    {"number": 11, "key": "daridra_planets_with_dusthana_lords",
     "name": "Daridra Yoga (11.10 #11) — planets conjoined by the 6th, 8th and 12th lords",
     "definition": ("Planets conjoined by 6th, 8th and 12th lords give loss "
                    "of wealth in their dasas, if they are not conjoined or "
                    "aspected by the lords of trines."),
     "is_about_dasas": True},
    {"number": 12, "key": "daridra_mars_saturn_in_second",
     "name": "Daridra Yoga (11.10 #12) — Mars and Saturn in the 2nd, unaspected by Mercury",
     "definition": ("Mars and Saturn are in 2nd and Mercury doesn't aspect "
                    "them."),
     "exception": ("If Mercury aspects Mars and Saturn in 2nd, great wealth "
                   "is generated.")},
    {"number": 13, "key": "daridra_sun_in_second_aspected_by_saturn",
     "name": "Daridra Yoga (11.10 #13) — the Sun in the 2nd aspected by Saturn",
     "definition": "Sun in 2nd is aspected by Saturn.",
     "exception": ("If Saturn doesn't aspect, Sun in 2nd gives wealth.")},
)

DARIDRA_YOGA_COUNT = len(DARIDRA_YOGAS)

DARIDRA_GENERAL_PRINCIPLES = (
    "Dusthanas (6th, 8th and 12th) and their lords are detrimental to wealth. "
    "If lagna, lagna lord and trine lords are afflicted by them, one may be "
    "poor. Conjunction or aspect of marakas clinches the issue. However, "
    "conjunction or aspect of trine lords is a saving factor. In addition, "
    "the planets in the 2nd house and the strength of 2nd lord matter.")

#: The one clause of the general principles that runs the other way.
DARIDRA_SAVING_FACTOR = (
    "However, conjunction or aspect of trine lords is a saving factor.")
