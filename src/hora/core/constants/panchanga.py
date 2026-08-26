"""Panchanga elements — tithi, yoga, karana, vaara, masa (chapter 1).

Split out of the former single ``const.py``. Import from
:mod:`hora.core.const`, which re-exports every constant — that facade is the
stable internal surface and keeps call sites independent of how the tables are
filed.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

# --------------------------------------------------------------------------
# Panchanga
# --------------------------------------------------------------------------

VAARA_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
#: Lord of each weekday, indexed the same as VAARA_NAMES.
VAARA_LORD = [Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER, Graha.VENUS, Graha.SATURN]

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Amavasya",
]

#: Tithi names as printed in Table 3 of the book.
TITHI_NAMES_BOOK = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashti",
    "Saptami", "Ashtami", "Navami", "Dasami", "Ekadasi", "Dwadasi",
    "Trayodasi", "Chaturdasi", "Paurnami",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashti",
    "Saptami", "Ashtami", "Navami", "Dasami", "Ekadasi", "Dwadasi",
    "Trayodasi", "Chaturdasi", "Amavasya",
]

#: Lord of each tithi, Table 3.
#:
#: The eight-lord cycle is attached to the tithi *name* (Pratipada..Paurnami),
#: not to the position in the 30-tithi month — so Krishna Pratipada shares
#: Sukla Pratipada's lord. Amavasya is the one exception: it continues the
#: cycle past Paurnami and lands on Rahu.
_TITHI_LORD_CYCLE = [
    Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
    Graha.JUPITER, Graha.VENUS, Graha.SATURN, Graha.RAHU,
]
TITHI_LORD = [
    Graha.RAHU if i == 29 else _TITHI_LORD_CYCLE[(i % 15) % 8]
    for i in range(30)
]

#: Paksha (fortnight) names, with the synonyms Table 3 heads its columns with:
#: "Sukla/Suddha Paksha (brighter fortnight)" and "Krishna/Bahula Paksha
#: (darker fortnight)".
PAKSHA_NAMES = ["Sukla", "Krishna"]
PAKSHA_SYNONYMS = [["Suddha"], ["Bahula"]]
PAKSHA_DESCRIPTIONS = ["brighter fortnight", "darker fortnight"]

#: Table 3 gives several tithis more than one name. Indexed by tithi number
#: 1-15; a tithi with no alternate name has an empty list.
TITHI_ALTERNATE_NAMES = [
    [],
    ["Pratipat", "Padyami"],          # 1st
    ["Vidiya"],                       # 2nd
    ["Tadiya"],                       # 3rd
    ["Chaviti", "Chauth"],            # 4th
    [], [], [], [], [], [], [], [], [], [],
    ["Paurnimasya", "Poornima", "Pournimasya"],   # 15th, Paurnami
]

#: Table 5's third column — what each yoga's name means.
YOGA_MEANINGS = [
    "Door bolt/supporting pillar", "Love/affection", "Long-lived",
    "Long life of spouse (good fortune)", "Splendid, bright", "Great danger",
    "One with good deeds", "Firmness", "Shiva's weapon of destruction (pain)",
    "Danger", "Growth", "Fixed, constant", "Great blow", "Cheerful",
    "Diamond (strong)", "Accomplishment", "Great fall", "Chief/best",
    "Obstacle/hindrance", "Lord Shiva (purity)", "Accomplished/ready",
    "Possible", "Auspicious", "White, bright",
    "Creator (good knowledge and purity)", "Ruler of gods", "A class of gods",
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti",
]

#: Yoga names as printed in Table 5 of the book.
YOGA_NAMES_BOOK = [
    "Vishkambha", "Preeti", "Aayushmaan", "Saubhaagya", "Sobhana", "Atiganda",
    "Sukarman", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaaghaata", "Harshana", "Vajra", "Siddhi", "Vyatipaata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Saadhya", "Subha", "Sukla",
    "Brahma", "Indra", "Vaidhriti",
]

#: The 11 karana names; the 60 half-tithis map onto these.
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti",
    "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]

#: Karana names as printed in section 1.3.10 of the book.
KARANA_NAMES_BOOK = [
    "Bava", "Balava", "Kaulava", "Taitula", "Garija", "Vanija", "Vishti",
    "Sakuna", "Chatushpada", "Naga", "Kimstughna",
]

#: 1.3.12 spells it "Panchaanga" ("one with 5 limbs"), and calls Indian
#: almanacs "panchaangas". We use the shorter transliteration everywhere;
#: this records the book's own spelling.
PANCHANGA_NAME_BOOK = "Panchaanga"
PANCHANGA_MEANING = "one with 5 limbs"
PANCHANGA_ALMANAC_NAME = "panchaangas"

#: Lunar month names (chaitradi).
MASA_NAMES = [
    "Chaitra", "Vaisakha", "Jyeshtha", "Ashadha", "Sravana", "Bhadrapada",
    "Asvina", "Kartika", "Margasira", "Pausha", "Magha", "Phalguna",
]

#: Lunar month names as printed in Table 4 of the book, indexed by the rasi
#: in which the Sun-Moon conjunction starting the month occurs. Table 4 begins
#: at Pisces (Chaitra), so index 0 here is Pisces, not Aries.
MASA_NAMES_BOOK = [
    "Chaitra", "Vaisaakha", "Jyeshtha", "Aashaadha", "Sraavana", "Bhaadrapada",
    "Aaswayuja", "Kaarteeka", "Maargasira", "Pushya", "Maagha", "Phaalguna",
]

#: Rasi of the Sun-Moon conjunction -> lunar month index (Table 4).
#: Pisces starts Chaitra, Aries starts Vaisakha, and so on.
MASA_FROM_CONJUNCTION_RASI = [(r - 11) % 12 for r in range(12)]

#: Table 4's third column, "Most likely constellation of Full Moon", verbatim.
#: §1.3.8.2: "These names come from the constellation that Moon is most likely
#: to occupy on the full Moon day." Four rows name a Poorva/Uttara pair rather
#: than one nakshatra, and are transcribed as the book prints them. Note that
#: the month name and the constellation are spelt differently in several rows
#: (Chaitra/Chitra, Kaarteeka/Krittika, Maagha/Makha) and are unrelated in one
#: (Aaswayuja/Aswini) — do not derive either column from the other.
MASA_FULL_MOON_NAKSHATRA_BOOK = [
    "Chitra", "Visaakha", "Jyeshtha", "Poorva/Uttara Aashaadha",
    "Sravana", "Poorva/Uttara Bhadrapada", "Aswini", "Krittika",
    "Mrigasira", "Pushyami", "Makha", "Poorva/Uttara Phalguni",
]

#: Table 4's fourth column, "Approx when?", verbatim. Indicative only: the
#: book says "Approx", and the correspondence drifts with adhika maasas.
MASA_APPROXIMATE_GREGORIAN_BOOK = [
    "Mar/Apr", "Apr/May", "May/June", "June/July", "July/Aug", "Aug/Sept",
    "Sept/Oct", "Oct/Nov", "Nov/Dec", "Dec/Jan", "Jan/Feb", "Feb/Mar",
]

#: Footnote 2 to §1.3.8.2, which defines the term the whole section rests on.
CONJUNCTION_DEFINITION = (
    "Two planets are said to be in \u201cconjunction\u201d if they are exactly at "
    "the same longitude."
)

#: The same footnote's NOTE, which loosens it. Both senses are used in the
#: book, so a caller must be told which one an API means.
CONJUNCTION_APPROXIMATE_NOTE = (
    "However, we sometimes use this term approximately. If two planets are in "
    "the same sign, but not exactly at the same longitude, we still say that "
    "they are in conjunction."
)

#: §1.3.8.2: "A solar year has about 365.2425 days, but a lunar year only has
#: about 355 days." Both are the book's own approximations, not our constants.
SOLAR_YEAR_DAYS_BOOK = 365.2425
LUNAR_YEAR_DAYS_BOOK = 355

#: "Once in every 3 years, this difference accumulates to one month and an
#: extra lunar month comes."
ADHIKA_MAASA_INTERVAL_YEARS = 3

#: "Nija means real and adhika means extra."
MAASA_QUALIFIERS = {"Nija": "real", "Adhika": "extra"}

#: "maasa = month", glossed by the book in §1.3.8.2.
MAASA_MEANING = "month"

#: "after about 29-30 days, he will catch up with Sun again".
LUNAR_MONTH_DAYS_BOOK = (29, 30)

#: Hora lords in order of decreasing apparent speed (section 1.3.11).
#: The first hora after sunrise belongs to the weekday lord, then this cycle.
HORA_LORD_ORDER = [
    Graha.SATURN, Graha.JUPITER, Graha.MARS, Graha.SUN,
    Graha.VENUS, Graha.MERCURY, Graha.MOON,
]

#: Sixty-year Jovian cycle (samvatsara) names.
SAMVATSARA_NAMES = [
    "Prabhava", "Vibhava", "Sukla", "Pramoduta", "Prajotpatti", "Angirasa",
    "Srimukha", "Bhava", "Yuva", "Dhatri", "Isvara", "Bahudhanya",
    "Pramathi", "Vikrama", "Vrisha", "Chitrabhanu", "Svabhanu", "Tarana",
    "Parthiva", "Vyaya", "Sarvajit", "Sarvadhari", "Virodhi", "Vikriti",
    "Khara", "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukhi",
    "Hevilambi", "Vilambi", "Vikari", "Sarvari", "Plava", "Subhakrit",
    "Sobhakrit", "Krodhi", "Visvavasu", "Parabhava", "Plavanga", "Kilaka",
    "Saumya", "Sadharana", "Virodhikrit", "Paridhavi", "Pramadica", "Ananda",
    "Rakshasa", "Nala", "Pingala", "Kalayukti", "Siddharthi", "Raudri",
    "Durmati", "Dundubhi", "Rudhirodgari", "Raktakshi", "Krodhana", "Akshaya",
]
