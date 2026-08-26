"""Houses — book chapter 7.

A house is a rasi counted from a reference point. §7.1: "The rasi containing
the point of reference is the 1st house." Lagna is the default reference, but
never the only one, and §7.5 is emphatic that a house never spans two rasis:

    "Each rasi is a house. The rasi containing the reference point chosen is
    the 1st house and the next rasi is the 2nd house."

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

#: 1.3.3: "Another important concept is 'house' (Sanskrit name: bhava)."
BHAVA_NAME = "bhava"
HOUSE_DEFINITION = (
    "Starting from the rasi occupied by the selected reference point and "
    "proceeding in the regular order across the zodiac, we associate each rasi "
    "with a house. Always the rasi containing the reference point chosen is "
    "the 1st house."
)

#: 1.3.3's wrap rule, stated because it is the one step a reader gets wrong:
#: "Just remember that when we encounter Pisces, we go to Aries after it."
HOUSE_ORDER_WRAPS = (
    "when we encounter Pisces, we go to Aries after it"
)

#: 1.3.3's default. Every function taking a reference defaults to the lagna,
#: and this is the sentence that licenses it.
HOUSE_DEFAULT_REFERENCE = "lagna"
HOUSE_DEFAULT_REFERENCE_RULE = (
    "If no reference point is specified when houses are mentioned, it means "
    "that lagna is used as the reference"
)

#: 1.3.3: "the reference points most commonly employed are lagna and special
#: lagnas". The full set §7.3 names is in HOUSE_REFERENCES below.
HOUSE_COMMON_REFERENCES = ("lagna", "special lagnas")

#: 1.3.1's definition of lagna. Chapter 7 makes it the default house
#: reference; this is what it actually is.
LAGNA_DEFINITION = (
    "the point that rises on the eastern horizon as the earth rotates around "
    "itself"
)

#: 1.3.1 names a further class of points without listing them; chapter 5
#: defines them. See :mod:`hora.charts.special_lagna`.
SPECIAL_ASCENDANT_TERM = "special ascendants"

#: §7.2 — what each house signifies, in the book's own wording. 1-indexed by
#: house number, so index 0 is unused and kept as an empty string.
#: §7.3's rule for picking which of a house's many meanings applies.
CHOOSE_MEANING_BY_VARGA = (
    "We have to note the area of life seen in the divisional chart under "
    "examination. We have to choose the meanings of houses that are relevant "
    "in that area of life."
)

#: §7.3's worked case, stored as the book gives it. The 4th house shows
#: education, vehicle, house and mother among other things; which of them is
#: meant depends on the chart the house is being read in.
FOURTH_HOUSE_BY_VARGA = (
    {"chart": "D24", "area": "learning", "means": "education"},
    {"chart": "D16", "area": "pleasures and comforts", "means": "vehicle"},
    {"chart": "D4", "area": "house and immovable property", "means": "house"},
    {"chart": "D12", "area": "parents", "means": "mother"},
)

#: §7.3: the same house from different references also differs.
HOUSE_DIFFERS_BY_REFERENCE_EXAMPLE = (
    "The 4th house from lagna, the 4th house from arudha lagna and the 4th "
    "house from paaka lagna can mean different things, depending on the "
    "matters shown by lagna, arudha lagna and paaka lagna."
)

#: §7.3: all three must be chosen correctly, not just the house.
THREE_CHOICES_RULE = (
    "Depending on the matter we are analyzing, we should look at the correct "
    "divisional chart, the correct reference and the correct house. Then only "
    "good results can be obtained."
)

#: §7.3's defence of the model's size. Recorded because it is the book's own
#: answer to "why are there so many parameters".
MANY_PARAMETERS_NOTE = (
    "Human existence is a very complicated thing and it is silly and "
    "unscientific to expect a simplistic model for the complicated human "
    "life. Though Vedic astrology has too many parameters used in chart "
    "analysis, they are all important as they give us the degrees of freedom "
    "necessary for modeling something as complicated as human life. However, "
    "if we do not understand what each parameter means and end up using them "
    "in a mixed-up way, we will get nowhere."
)

#: §7.3.1: what lagna is, and what it is **not** for.
LAGNA_SHOWS = "true self"
LAGNA_SPIRIT_OF_I = "the overall spirit of \u201cI\u201d (self)"
LAGNA_NOT_FOR_STATUS = (
    "If we are trying to understand someone's status in society, lagna may "
    "not be the correct reference. Status does not relate to \u201ctrue self\u201d. "
    "It is a part of the illusion of this world."
)

#: §7.3.1: what *is* seen from lagna.
LAGNA_SEEN_FROM = ("intentions in doing something", "knowledge", "persistence")

#: §7.3.2: Chandra lagna, and why it is not optional.
CHANDRA_LAGNA_SHOWS = "things from the perspective of mind"
CHANDRA_LAGNA_REASON = "Moon is the significator of mind"
CHANDRA_LAGNA_NOT_IGNORED = (
    "When we judge how happy one is, how ambitious one is and how one views "
    "one's career, the role of mind is paramount. So Chandra lagna should not "
    "be ignored."
)

#: §7.3.2's worked contrast \u2014 the same house from two references, showing
#: two different things about one native.
CHANDRA_LAGNA_EXAMPLE = {
    "house": 10,
    "from_lagna": {"graha": "Saturn", "shows": "routine job"},
    "from_moon": {"graha": "Mars", "shows": "active and enterprising"},
    "reading": (
        "someone may be working in a routine job, but he may have an active "
        "and enterprising mind and he may be using it in his career"
    ),
}

#: §7.3.3: why Sun works as a reference, and the second thing it is good for.
RAVI_LAGNA_REASON = "Sun is the significator of soul"
RAVI_LAGNA_SHOWS = "things from the perspective of soul"
RAVI_LAGNA_ALSO = (
    "For things related to physical vitality also, Sun is an important "
    "reference."
)

#: §7.3.4, verbatim. The computation is chapter 9's; this is what it *shows*.
ARUDHA_LAGNA_SHOWS = (
    "arudha lagna shows how a native is perceived in the world. It also shows "
    "the status of a native."
)

#: §7.3.5: paaka lagna is the lagna lord's rasi, and why that means what it
#: means.
PAAKA_LAGNA_DEFINITION = "Paaka lagna is nothing but lagna lord taken as a reference."
PAAKA_LAGNA_SHOWS = "matters related to the physical self of a native"
PAAKA_LAGNA_REASON = (
    "Rasis represent situations and forces influencing the course of a "
    "native's life and planets represent individual beings. Lagna lord "
    "represents the physical self of a native."
)
PAAKA_LAGNA_USED_IN = ("the natal chart", "dasas", "transits")

#: §7.3.5's two worked cases, as (lagna, lord's rasi, paaka lagna).
PAAKA_LAGNA_EXAMPLES = (
    {"lagna": "Pi", "lord": "Jupiter", "lord_rasi": "Cn", "paaka": "Cn"},
    {"lagna": "Le", "lord": "Sun", "lord_rasi": "Vi", "paaka": "Vi"},
)

#: §7.3.5: the distinction the whole reference scheme turns on.
LAGNA_IS_CONCEPTUAL = (
    "Lagna shows the concept of self and it deals with one's true "
    "personality. The physical existence of the person is different from this "
    "conceptual self. This applies to all divisional charts."
)

#: §7.3.4's worked contrast — one house, three references, three readings.
TENTH_HOUSE_BY_REFERENCE = (
    {"reference": "lagna", "shows": "some important developments in one's profession"},
    {"reference": "chandra_lagna",
     "shows": "some important mental activity in one's profession"},
    {"reference": "arudha_lagna",
     "shows": "some important developments in one's professional status"},
)

#: §7.3.5's worked contrast — the 5th house in D-24, read three ways. The
#: clearest statement in the chapter of *how* a reference is chosen.
FIFTH_HOUSE_IN_D24_BY_REFERENCE = (
    {
        "matter": "success in competition",
        "reference": "arudha_lagna",
        "why": "related to the illusions and perceptions of the world",
    },
    {
        "matter": "scholarship",
        "reference": "lagna",
        "why": (
            "not a measurable attribute of the physical existence; a property "
            "of one's true personality and one's conceptual self"
        ),
    },
    {
        "matter": "memory",
        "reference": "paaka_lagna",
        "why": "a property of one's self that physically exists",
    },
)

#: Footnote 13's subject — Saturn's transit read from three references.
SATURN_TRANSIT_BY_REFERENCE = (
    {"reference": "lagna", "shows": "obstructions, and hampers one's activities"},
    {"reference": "chandra_lagna", "shows": "frustration and mental depression"},
    {"reference": "paaka_lagna",
     "shows": "feeling sick all the time, and attacks the physical vitality"},
)

#: §7.3.6: why the atma karaka is read in navamsa rather than the rasi chart.
KARAKAMSA_REASON = (
    "Atma karaka stands for the soul of the person. Because the soul is an "
    "important factor in deciding the nature of inner self than the physical "
    "existence, atma karaka is an important reference point in navamsa chart."
)
KARAKAMSA_DEFINITION = (
    "Navamsa chart throws light on the inner self and the rasi occupied by "
    "atma karaka in it is called \u201cKarakamsa\u201d."
)

#: §7.3.6's one derived rule, and the only moksha rule in the chapter.
KARAKAMSA_TWELFTH_RULE = (
    "The 12th house from Karakamsa shows the liberation of the soul and the "
    "situation of Ketu there is conducive to moksha. Propitiation of the "
    "deities corresponding to the strongest planet in the 12th house in "
    "navamsa from Karakamsa lagna can take one's soul towards moksha."
)
KARAKAMSA_MOKSHA_HOUSE = 12
KARAKAMSA_MOKSHA_GRAHA = Graha.KETU

#: §7.3.7 and §7.3.8, verbatim. Both echo chapter 5's significations.
GHATI_LAGNA_SHOWS = "self, from the point of view of power, authority and fame"
GHATI_LAGNA_USED_FOR = (
    "When we analyze promotions in career or political power of politicians, "
    "this reference is very important."
)
HORA_LAGNA_SHOWS = "self, from the point of view of wealth"
HORA_LAGNA_USED_FOR = "This reference is important when analyzing one's wealth."

#: Footnote 13 — the definition the transit chapters rest on.
TRANSIT_DEFINITION = (
    "If a planet occupies, on a given day, a particular rasi, then it is said "
    "to \u201ctransit\u201d in that sign on that day. Transit positions refer to the "
    "positions of planets on a given day and natal positions refer to the "
    "positions of planets at the time of one's birth."
)

#: §7.4's gloss on the dusthanas — the only category given one.
DUSTHANA_GLOSS = "bad/evil houses"

#: §7.4's closing rule: the categories are relative, like the houses.
CATEGORIES_ARE_RELATIVE = (
    "We can find trines, quadrants etc from lagna or other references or even "
    "from houses. Thus we can find trines, quadrants etc from any house."
)

#: §7.4's worked example, from the 3rd house. Four categories, each checked
#: against the relative computation.
CATEGORIES_FROM_THIRD_HOUSE = {
    "trikona": (3, 7, 11),
    "kendra": (3, 6, 9, 12),
    "upachaya": (5, 8, 12, 1),
    "dusthana": (8, 10, 2),
}

#: Footnote 14 — why speech is read in three charts, and what disagreement
#: between them means. The clearest worked case in the chapter of two charts
#: saying different things about one matter.
THREE_CHARTS_FOR_SPEECH_NOTE = (
    "Rasi chart shows the overall picture and the manifestation at the "
    "physical level. Navamsa shows basic skills and the way one interacts "
    "with others. D-27 shows one's strengths and weaknesses. All the three "
    "charts are important. One may have strong benefics in the 2nd from lagna "
    "in rasi and navamsa charts, but malefics in the 2nd from Mercury in "
    "D-27. In such a case, one will be a skilled speaker, but harsh speech "
    "may be his weakness."
)

#: Footnote 14's per-chart roles, which §7.3.9's speech example rests on.
SPEECH_CHART_ROLES = (
    {"chart": "D1", "shows": "the overall picture and the manifestation at the "
                             "physical level"},
    {"chart": "D9", "shows": "basic skills and the way one interacts with others"},
    {"chart": "D27", "shows": "one's strengths and weaknesses"},
)

#: §7.4.1's opening — what a trine is *for*, and why it is relative.
TRINE_IS_BENEFICIAL = (
    "Trines from any reference are houses that are beneficial to the "
    "reference. They bring prosperity and well-being to the reference."
)
TRINE_ABODE = "Trines are the abode of Goddess Lakshmi, who rules prosperity."

#: §7.4.1's Sanskrit name and gloss for each purushartha trikona, keyed as
#: PURUSHARTHA_TRIKONAS. Each is the trines from the 1st, 2nd, 3rd and 4th.
PURUSHARTHA_TRIKONA_NAMES = {
    "dharma": {"name": "dharma trikonas", "gloss": "trines of duty", "base": 1},
    "artha": {"name": "artha trikonas", "gloss": "trines of money", "base": 2},
    "kaama": {"name": "kaama trikonas", "gloss": "trines of desire", "base": 3},
    "moksha": {"name": "moksha trikonas", "gloss": "trines of liberation", "base": 4},
}

#: §7.4.1 says what each of the twelve houses contributes to its purushartha.
#: Not the same as §7.2's signification list — four of the twelve are given in
#: words §7.2 does not use. See OI-55.
PURUSHARTHA_HOUSE_REASONS = {
    1: "prosperity of self", 5: "intelligence", 9: "dharma",
    2: "wealth", 6: "service", 10: "career and activities in society",
    3: "persistence", 7: "relations and sex", 11: "gains",
    4: "harmony", 8: "occult studies and spiritual awakening", 12: "moksha",
}

#: §7.4.1: what decides how one follows dharma.
DHARMA_IS_DECIDED_BY = (
    "The character of a person, his intelligence and his righteousness decide "
    "how one follows dharma."
)

#: Footnote 15.
DHARMA_LITERAL_MEANING = "duty"
DHARMA_NOTE = (
    "Dharma literally means duty. However, it has come to mean righteousness."
)

#: §7.4.1's two forward references, neither implemented.
PURUSHARTHA_STRENGTH_RULE = (
    "Digbala of planets who attain full digbala in various of these trines "
    "shows the strength of different purushaarthas in one's life."
)
TRIKONA_DASA_NOTE = (
    "Dasas like \u201cTrikona Dasa\u201d which are based on trines show how one "
    "follows the four purushaarthas in life."
)

#: Footnote 16's subject.
MUTUAL_TRINES_RULE = "Planets in mutual trines make each other prosper."

# --------------------------------------------------------------------------
# §7.4.2 Quadrants
# --------------------------------------------------------------------------

#: §7.4.2's epithet for Sri Maha Vishnu. "Sustains" is the whole reason the
#: quadrants are his: the category's signification is sustenance.
MAHA_VISHNU_EPITHET = "the Supreme Lord who sustains this universe as per Hinduism"
QUADRANT_ABODE = "Quadrants are the abode of Sri Maha Vishnu."
QUADRANT_IS_SUSTENANCE = "Quadrants from any reference show its sustenance."

#: §7.4.2's reason for each quadrant, the counterpart of the purushaartha
#: reasons in §7.4.1. Only the 1st is not §7.2's own word — see OI-55.
QUADRANT_HOUSE_REASONS = {
    1: "self",
    4: "comforts",
    7: "marriage and relations with others",
    10: "profession",
}
QUADRANTS_SUSTAIN_EACH_OTHER = (
    "The 1st house (self), 4th house (comforts), 7th house (marriage and "
    "relations with others) and the 10th house (profession) sustain each other."
)

#: Footnote 17, the mirror of footnote 16.
MUTUAL_QUADRANTS_RULE = (
    "Planets in mutual quadrants have a sustaining effect on each other."
)
MUTUAL_QUADRANTS_DEFINITION = (
    "We say that two planets are in \u201cmutual quadrants\u201d, if one planet is "
    "in a quadrant from the other."
)
MUTUAL_TRINES_DEFINITION = (
    "We say that two planets are in \u201cmutual trines\u201d, if one planet is in a "
    "trine from the other."
)

# --------------------------------------------------------------------------
# §7.4.3 Upachayas
# --------------------------------------------------------------------------

UPACHAYA_RULE = (
    "Upachayas from a reference show forces causing gains and growth to the "
    "matters signified by the reference."
)

#: §7.4.3's worked example. The only place in §7.4 where a category is applied
#: to a non-lagna reference by name.
UPACHAYA_EXAMPLE = {
    "reference": "arudha_lagna",
    "reference_shows": "one's status",
    "upachayas_show": "improvement of status",
}

# --------------------------------------------------------------------------
# §7.4.4 Dusthanas
# --------------------------------------------------------------------------

DUSTHANA_RULE = (
    "Dusthanas from a reference show forces causing setbacks to the matters "
    "signified by it."
)

#: §7.4.4's inversion: strength in a dusthana is bad news, weakness is good.
#: The only category in §7.4 whose reading flips with strength.
DUSTHANA_STRENGTH_INVERSION = (
    "If a dusthana is fortified or afflicted by malefics, it may show serious "
    "obstacles. If a dusthana is weak, it shows that obstacles will be easily "
    "overcome."
)
DUSTHANA_STRENGTH_EXAMPLE = (
    "Exalted 8th lord may show a lot of troubles and debilitated 8th lord may "
    "show easy sailing."
)

# --------------------------------------------------------------------------
# §7.4.5 Visible and invisible halves
# --------------------------------------------------------------------------

HALVES_RULE = (
    "The houses in the visible half of the zodiac with respect to a reference "
    "give results that can be seen in the material world and the houses in the "
    "invisible half of the zodiac give results that cannot be easily seen."
)
HALVES_ARE_IN_EVERY_CHART = "The zodiac is divided into two halves in every chart."
HALVES_EXPLAIN_THE_TRIKONA_BASES = (
    "It is for this reason that the bases of dharma trikona (1st house) and "
    "moksha trikona (4th house) are in the invisible half and the bases of "
    "artha trikona (10th house) and kaama trikona (7th house) are in the "
    "visible half."
)

# --------------------------------------------------------------------------
# §7.4.6 Quick summary
# --------------------------------------------------------------------------

#: §7.4.6's five-line table. Four of the lines restate `HOUSE_CATEGORIES`;
#: the fifth names a category §7.4 never listed — argala sthanas, which are
#: chapter 10. Kept as its own constant rather than forced into the seven.
QUICK_SUMMARY = {
    "Trines": "Prosperity and flourishing",
    "Quadrants": "Sustenance and vital activity",
    "Upachayas": "Gains and growth",
    "Dusthanas": "Setbacks and obstacles",
    "Argala sthanas": "Decisive influences",
}
ARGALA_STHANA_SHOWS = "Decisive influences"


#: §7.1: houses are always relative to something, and that something is the
#: lagna unless another reference is named.
HOUSE_REFERENCE_RULE = (
    "If we mention houses without clearly specifying the reference used, it "
    "means that the reference used is lagna (ascendant). Lagna is the default "
    "reference when finding houses."
)

#: §7.1: the same sign is a different house from a different reference, and
#: the *meaning* changes with it too.
HOUSE_MEANING_DEPENDS_ON_REFERENCE = (
    "The matters signified by a house also depend on the reference used. Each "
    "reference throws light on matters of a specific nature and that colors "
    "the meaning of a house."
)

#: §7.1: and on the divisional chart the houses are found in.
HOUSE_MEANING_DEPENDS_ON_VARGA = (
    "In addition, the matters signified by a house depend on the divisional "
    "chart in which we are finding houses."
)

#: §7.2's closing method \u2014 a house counted from another house, with the two
#: meanings concatenated.
HOUSES_FROM_HOUSES_RULE = (
    "We can find houses from houses and concatenate the meanings in some "
    "places."
)

#: §7.2's three worked derivations. Each is (house, from_house, result) with
#: the meaning the concatenation yields.
HOUSES_FROM_HOUSES_EXAMPLES = (
    {
        "house": 2, "from_house": 3, "result": 4,
        "shows": "the wealth, speech etc of younger brother",
    },
    {
        "house": 7, "from_house": 3, "result": 9,
        "shows": "younger sibling's spouse",
    },
    {
        "house": 6, "from_house": 11, "result": 4,
        "shows": "enemies, diseases and debts of friends",
    },
)

#: §7.2's pointer for fuller treatment of house results.
HOUSE_RESULTS_REFERENCE = (
    "For further discussion on the results of various houses, readers may "
    "refer either to the ancient classics or to the modern classic \u2013 "
    "\u201cHow to Judge a Horoscope\u201d (Vols I & II) by Dr. B.V. Raman."
)

HOUSE_SIGNIFICATIONS: list[str] = [
    "",
    (
        "Physical body, complexion, appearance, head, intelligence, strength, "
        "energy, fame, success, nature of birth, caste"
    ),
    "Wealth, assets, family, speech, eyes, mouth, face, voice, food",
    (
        "Younger co-borns, confidants, courage, mental strength, "
        "communication skills, creativity, throat, ears, arms, father's "
        "death (7th from 9th), expenditure on vehicles and house "
        "(12th from 4th), travels"
    ),
    (
        "Mother, vehicles, house, lands, immovable property, motherland, "
        "childhood, wealth from real estate, education, relatives, happiness, "
        "comforts, pleasures, peace, state of mind, heart"
    ),
    (
        "Children, poorvapunya (good deeds of previous lives), intelligence, "
        "knowledge & scholarship, devotion, mantras (prayers), stomach, "
        "digestive "
        "system, authority/power, fame, love, affection, emotions, judgment, "
        "speculation"
    ),
    (
        "Enemies, service, servants, relatives, mental tension, injuries, "
        "health, diseases, agriculture, accidents, mental affliction, "
        "mother's younger brother, hips"
    ),
    (
        "Marriage, marital life, life partner, sex, passion (and related "
        "happiness), long journeys, "
        "partners, business, death, the portion of the body below the navel"
    ),
    (
        "Longevity, debts, disease, ill-fame, inheritance, loss of friends, "
        "occult studies, evils, gifts, unearned wealth, windfall, disgrace, "
        "secrets, genitals"
    ),
    (
        "Father, teacher, boss, fortune, religiousness, spirituality, God, "
        "higher studies & high knowledge, fortune in a foreign land, "
        "foreign trips, diksha (joining a religious order), past life "
        "and the cause of birth, "
        "grandchildren, principles, dharma, intuition, compassion, sympathy, "
        "leadership, charity, thighs"
    ),
    (
        "Growth, profession, career, karma (action), conduct in society, "
        "fame, honors, awards, self-respect, dignity, knees"
    ),
    "Elder co-borns, income, gains, realization of hopes, friends, ankles",
    (
        "Losses, expenditure, punishment, imprisonment, hospitalization, "
        "pleasures in bed, misfortune, bad habits, sleep, meditation, "
        "donation, secret enemies, heaven, left eye, feet, residence away "
        "from the place of birth, moksha (emancipation/liberation)"
    ),
]

# --------------------------------------------------------------------------
# §7.4 Special categories
#
# Every one of these is relative: the book computes them from any house, not
# only from the 1st. "The 3rd, 7th and 11th houses are the trines from the 3rd
# house."
# --------------------------------------------------------------------------

TRIKONA = (1, 5, 9)          # konas, trines
KENDRA = (1, 4, 7, 10)       # quadrants, angles
PANAPHARA = (2, 5, 8, 11)    # succedants — quadrants from the 2nd
APOKLIMA = (3, 6, 9, 12)     # precedants — quadrants from the 3rd
UPACHAYA = (3, 6, 10, 11)
DUSTHANA = (6, 8, 12)        # trik sthanas
CHATURASRA = (4, 8)

#: Every category the chapter names, with its synonyms and what it shows.
#: §7.4.6 gives the one-line summaries.
HOUSE_CATEGORIES: dict[str, dict] = {
    "trikona": {
        "houses": TRIKONA,
        "synonyms": ["kona", "trine"],
        "shows": "Prosperity and flourishing",
        "presiding": "Goddess Lakshmi",
    },
    "kendra": {
        "houses": KENDRA,
        "synonyms": ["quadrant", "angle"],
        "shows": "Sustenance and vital activity",
        "presiding": "Sri Maha Vishnu",
    },
    "panaphara": {
        "houses": PANAPHARA,
        "synonyms": ["succedant"],
        # §7.4 gives these two no signification, only a derivation: "These
        # are basically the quadrants from the 2nd house." That belongs in
        # `derivation`, not `shows` — a caller reading `shows` wants a
        # meaning, and this field previously handed it a definition.
        "shows": None,
        "derivation": "the quadrants from the 2nd house",
        "presiding": None,
    },
    "apoklima": {
        "houses": APOKLIMA,
        "synonyms": ["precedant"],
        "shows": None,
        "derivation": "the quadrants from the 3rd house",
        "presiding": None,
    },
    "upachaya": {
        "houses": UPACHAYA,
        "synonyms": [],
        "shows": "Gains and growth",
        "presiding": None,
    },
    "dusthana": {
        "houses": DUSTHANA,
        "synonyms": ["trik sthana"],
        "shows": "Setbacks and obstacles",
        "presiding": None,
    },
    "chaturasra": {
        "houses": CHATURASRA,
        "synonyms": [],
        "shows": None,
        "presiding": None,
    },
}

# --------------------------------------------------------------------------
# §7.4.1 The four purusharthas
# --------------------------------------------------------------------------

#: 7.4.1: "there are 4 purushaarthas (purposes/goals of man)". We key these
#: by the short transliteration; this records the book's own spelling.
PURUSHARTHA_NAME_BOOK = "purushaarthas"
PURUSHARTHA_MEANING = "purposes/goals of man"

#: Each group is the trines from its base house: 1st, 2nd, 3rd and 4th.
PURUSHARTHA_TRIKONAS: dict[str, dict] = {
    "dharma": {"houses": (1, 5, 9), "meaning": "righteousness and adherence to one's duty"},
    "artha": {"houses": (2, 6, 10), "meaning": "money and career"},
    "kaama": {"houses": (3, 7, 11), "meaning": "desiring things and getting them"},
    "moksha": {"houses": (4, 8, 12), "meaning": "final liberation of soul"},
}

# --------------------------------------------------------------------------
# §7.4.5 The two halves
# --------------------------------------------------------------------------

#: Results in the visible half can be seen in the material world; those in the
#: invisible half cannot easily be. The bases of the dharma and moksha trikonas
#: fall in the invisible half, and those of artha and kaama in the visible.
VISIBLE_HALF = (7, 8, 9, 10, 11, 12)
INVISIBLE_HALF = (1, 2, 3, 4, 5, 6)

# --------------------------------------------------------------------------
# §7.3 Reference points
# --------------------------------------------------------------------------

#: What each reference colours the houses with. A reference that needs a later
#: chapter to compute is marked ``available: False`` rather than omitted, so
#: the gap is visible in the API instead of silent.
HOUSE_REFERENCES: dict[str, dict] = {
    "lagna": {
        "name": "Lagna", "shows": "true self", "available": True,
        "note": "The default reference when none is named",
    },
    "chandra_lagna": {
        "name": "Chandra Lagna", "shows": "matters from the perspective of mind",
        "available": True, "note": "The Moon's rasi",
    },
    "ravi_lagna": {
        "name": "Ravi Lagna", "shows": "matters from the perspective of soul",
        "available": True, "note": "The Sun's rasi",
    },
    "paaka_lagna": {
        "name": "Paaka Lagna", "shows": "matters related to the physical self",
        "available": True, "note": "The rasi occupied by the lagna lord",
    },
    "ghati_lagna": {
        "name": "Ghati Lagna", "shows": "self, from the point of view of power, "
        "authority and fame", "available": True, "note": "See chapter 5",
    },
    "hora_lagna": {
        "name": "Hora Lagna", "shows": "self, from the point of view of wealth",
        "available": True, "note": "See chapter 5",
    },
    "arudha_lagna": {
        "name": "Arudha Lagna", "shows": "how a native is perceived, and status",
        # Turned on 2026-08-27. §7.3.4 says "Computation of arudha lagna will
        # be explained in the chapter on Arudha Padas" — chapter 9, which is
        # implemented in charts/arudha.py. The flag had been left False after
        # that chapter was built. Stale, not blocked.
        "available": True,
        "note": (
            "The arudha pada of the 1st house, computed by section 9.2's six "
            "steps in charts/arudha.py"
        ),
    },
    "karakamsa_lagna": {
        "name": "Karakamsa Lagna", "shows": "the inner self",
        # Turned on 2026-08-27. This entry previously read that karakamsa is
        # "named in chapter 7 and defined later" — that was wrong. §7.3.6
        # defines it outright: "the rasi occupied by atma karaka in it is
        # called Karakamsa". The atma karaka is §8.2's and the navamsa is
        # §6.2.9's, and §7.3.6 is the section that joins them. Computed by
        # charts/house.py:karakamsa_rasi.
        "available": True,
        "note": (
            "The rasi of the atma karaka in navamsa, defined in section 7.3.6"
        ),
    },
}

#: §7.3.9's name for the scheme, and the rule behind it.
GRAHA_LAGNA_NAME = "graha lagnas"
GRAHA_LAGNA_ALIAS = "planetary references"
GRAHA_LAGNA_RULE = (
    "For each house, a planet works as the natural significator. To see "
    "matters signified by a house, we can take the relevant planet as the "
    "reference."
)

#: §7.3.9's six worked pairs: read the house from lagna **and** from its
#: graha, and weigh the two.
GRAHA_LAGNA_PAIRS = (
    {"house": 3, "graha": Graha.MARS,
     "matter": "courage or persistence or weapons or younger brothers or the "
               "expenditure on house or the expenditure on car"},
    {"house": 4, "graha": Graha.MOON, "matter": "mother"},
    {"house": 9, "graha": Graha.SUN, "matter": "father"},
    {"house": 12, "graha": Graha.SATURN, "matter": "losses"},
    {"house": 5, "graha": Graha.JUPITER, "matter": "progeny"},
    {"house": 7, "graha": Graha.VENUS, "matter": "marriage"},
)

#: §7.3.9's comparative rule — the only place the chapter says how to choose
#: between two references rather than which to use.
GRAHA_LAGNA_STRENGTH_RULE = (
    "If Mars is stronger than lagna, then the 3rd house from Mars may be more "
    "important than the 3rd house from lagna."
)

#: §7.3.9's extension beyond Table 12: any naisargika karaka of the matter can
#: serve as the reference, in the divisional chart that shows that matter.
NAISARGIKA_REFERENCE_RULE = (
    "we can find a house with respect to the naisargika karaka (natural "
    "significator) who signifies the matter shown by a house"
)

#: The section's two worked instances of that extension. Both name the chart,
#: which Table 12's own pairs do not.
NAISARGIKA_REFERENCE_EXAMPLES = (
    {
        "matter": "vehicles",
        "graha": Graha.VENUS,
        "house": 4,
        "charts": ("D16",),
        "shows": "one's happiness from vehicles and other luxuries",
    },
    {
        "matter": "speech",
        "graha": Graha.MERCURY,
        "house": 2,
        "charts": ("D1", "D9", "D27"),
        "shows": "speech",
    },
)

#: Table 12 — the houses each graha is a natural reference for.
GRAHA_LAGNA_HOUSES: dict[int, tuple[int, ...]] = {
    Graha.SUN: (9, 10, 11),
    Graha.MOON: (4, 1, 2, 11, 9),
    Graha.MARS: (3,),
    Graha.MERCURY: (6,),
    Graha.JUPITER: (5,),
    Graha.VENUS: (7,),
    Graha.SATURN: (8, 12),
}

# --------------------------------------------------------------------------
# §7.5 A controversy — house division
# --------------------------------------------------------------------------

#: §7.5's opening. Three kinds of reference and every chart, not just the rasi
#: chart — the position "some scholars" narrow and PVR restores.
HOUSES_ARE_FOUND_FROM = (
    "Houses are found with respect to lagna, special lagnas and some planets. "
    "Houses are found in rasi chart and in all the divisional charts."
)
NARROW_VIEW_REJECTED = (
    "Some scholars ignore all these and take houses only with respect to lagna "
    "and only in rasi chart."
)

#: The two schemes §7.5 names and rejects, and what makes each identifiable.
BHAAVA_CHAKRA_DEFINITION = (
    "They prepare something called \u201cbhaava chakra\u201d or \u201cchalit chakra\u201d, "
    "in which houses can start in one rasi and end in another. They take "
    "lagna\u2019s longitude to be the mid-point of the first house and construct "
    "all the houses accordingly."
)
EQUAL_HOUSE_DEFINITION = (
    "In the \u201cequal house method\u201d, they take a 30\u00b0 arc with center at lagna "
    "as the 1st house. The next 30\u00b0 arc is taken as the 2nd house and so on."
)
EQUAL_HOUSE_IS_POPULAR = "This method is popular among Indian astrologers."
SRIPATHI_METHOD_NOTE = (
    "Another method taught by Sripathi is more complicated and it is also "
    "popular. However, this author recommends neither."
)

#: The rule that replaces them. Note "the reference point chosen" — not lagna:
#: §7.5's own definition is already relative, which is why every reference in
#: §7.3 can carry houses.
EACH_RASI_IS_A_HOUSE = (
    "Each rasi is a house. The rasi containing the reference point chosen is "
    "the 1st house and the next rasi is the 2nd house."
)

#: §7.5's precedence argument, and the clearest statement in the book of the
#: rule `docs/precedence.md` encodes: a direct reference beats an indirect one.
BPHS_HOUSE_DIVISION_ARGUMENT = (
    "Though there are some indirect references in BPHS suggesting that Parasara "
    "supported house divisions placing houses in 2 rasis, there are quite a few "
    "direct references making it amply clear that each house falls in one rasi. "
    "Parasara taught us to find houses by counting rasis from the reference "
    "chosen."
)

#: The architectural claim: the basic techniques are chart-agnostic.
RASI_AND_VARGA_ARE_NOT_DIFFERENTIATED = (
    "Only this approach is logical as we go to divisional charts. Parasara\u2019s "
    "treatment does not differentiate between rasi and divisional charts, as "
    "far as the basic techniques go."
)
IGNORE_OTHER_HOUSE_DIVISION_METHODS = (
    "So readers are advised to ignore all the discussions found in other "
    "textbooks on house division methods, \u201cbhaava chakra\u201d and "
    "\u201cchalit chakra\u201d. It may do good to follow the instructions in this "
    "chapter."
)

#: Footnote 18 — where §7.4.6's fifth summary line is taken up.
ARGALA_STHANA_FORWARD_REFERENCE = (
    "This will be covered in the chapter on \u201cAspects and Argalas\u201d."
)
