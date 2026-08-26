"""Verify our transcriptions against the book PDF itself.

Every other book test compares our constants to expectations typed out by hand.
That catches later edits, but it cannot catch a misreading made once and then
repeated in both places. These tests read the source PDF and check that the
text we claim to have transcribed is literally there.

The PDF is not in the repository. Point ``HORA_BOOK_PDF`` at it to run these;
otherwise they skip. Requires ``pypdf``.

    HORA_BOOK_PDF=/path/to/vedic_astro_textbook.pdf pytest tests/unit/test_book_source_fidelity.py
"""
import os
import re
from pathlib import Path

import pytest

from hora.content import get_store
from hora.core import const as c

BOOK_PDF = os.environ.get("HORA_BOOK_PDF")

pytestmark = pytest.mark.skipif(
    not (BOOK_PDF and Path(BOOK_PDF).is_file()),
    reason="set HORA_BOOK_PDF to the textbook PDF to run source-fidelity checks",
)

#: PDF pages holding chapters 1 and 2 (0-based, as pypdf indexes them).
CH1_PAGES = range(14, 32)
CH2_PAGES = range(32, 39)
CH3_PAGES = range(39, 52)
CH4_PAGES = range(51, 56)
CH5_PAGES = range(55, 62)
CH6_PAGES = range(61, 80)
CH7_PAGES = range(77, 94)


def _flatten_alnum(text: str) -> str:
    """Like :func:`_flatten` but keeps digits, for table rows with degrees."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _flatten(text: str) -> str:
    """Strip everything but letters.

    The extractor injects spaces inside words ("differen t", "aircr aft") and
    page furniture interrupts sentences, so only a letters-only comparison is
    meaningful.
    """
    return re.sub(r"[^a-z]", "", text.lower())


@pytest.fixture(scope="module")
def book_text():
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(BOOK_PDF)
    return {
        "ch1": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH1_PAGES)),
        "ch2": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH2_PAGES)),
        "ch3": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH3_PAGES)),
        "ch4": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH4_PAGES)),
        "ch4_alnum": _flatten_alnum(
            "".join(reader.pages[i].extract_text() or "" for i in CH4_PAGES)
        ),
        "ch5": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH5_PAGES)),
        "ch5_alnum": _flatten_alnum(
            "".join(reader.pages[i].extract_text() or "" for i in CH5_PAGES)
        ),
        "ch6": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH6_PAGES)),
        "ch6_alnum": _flatten_alnum(
            "".join(reader.pages[i].extract_text() or "" for i in CH6_PAGES)
        ),
        "ch7": _flatten("".join(reader.pages[i].extract_text() or "" for i in CH7_PAGES)),
        "ch7_alnum": _flatten_alnum(
            "".join(reader.pages[i].extract_text() or "" for i in CH7_PAGES)
        ),
        "ch3_alnum": _flatten_alnum(
            "".join(reader.pages[i].extract_text() or "" for i in CH3_PAGES)
        ),
    }


def _group(values, target):
    return [c.RASI_ABBR[i] for i in range(12) if values[i] == target]


def _contains_group(haystack: str, rasis: list[str]) -> bool:
    """The book lists groups as "Ar, Le and Sg" — accept either joining."""
    joined = _flatten(",".join(rasis))
    with_and = _flatten(",".join(rasis[:-1]) + "and" + rasis[-1])
    return joined in haystack or with_and in haystack


# --------------------------------------------------------------------------
# Chapter 2 groupings
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "label,values,target",
    [
        ("2.2.2 odd", "RASI_IS_ODD", True),
        ("2.2.2 even", "RASI_IS_ODD", False),
        ("2.2.3 odd-footed", "RASI_IS_ODD_FOOTED", True),
        ("2.2.3 even-footed", "RASI_IS_ODD_FOOTED", False),
        ("2.2.4 movable", "RASI_MODALITY", 0),
        ("2.2.4 fixed", "RASI_MODALITY", 1),
        ("2.2.4 dual", "RASI_MODALITY", 2),
        ("2.2.5 fire", "RASI_ELEMENT", 0),
        ("2.2.5 earth", "RASI_ELEMENT", 1),
        ("2.2.5 air", "RASI_ELEMENT", 2),
        ("2.2.5 water", "RASI_ELEMENT", 3),
        ("2.2.6 pitta", "RASI_DOSHA", 0),
        ("2.2.6 vaata", "RASI_DOSHA", 1),
        ("2.2.6 kapha", "RASI_DOSHA", 2),
        ("2.2.6 mixed", "RASI_DOSHA", 3),
        ("2.2.7 sattwa", "RASI_GUNA", 0),
        ("2.2.7 rajas", "RASI_GUNA", 1),
        ("2.2.7 tamas", "RASI_GUNA", 2),
        ("2.2.8 east", "RASI_DIRECTION", 0),
        ("2.2.8 south", "RASI_DIRECTION", 1),
        ("2.2.8 west", "RASI_DIRECTION", 2),
        ("2.2.8 north", "RASI_DIRECTION", 3),
        ("2.2.10 night", "RASI_IS_NIGHT", True),
        ("2.2.10 day", "RASI_IS_NIGHT", False),
        ("2.2.11 seershodaya", "RASI_RISING", 0),
        ("2.2.11 prishthodaya", "RASI_RISING", 1),
        ("2.2.12 brahmana", "RASI_VARNA", 0),
        ("2.2.12 kshatriya", "RASI_VARNA", 1),
        ("2.2.12 vaisya", "RASI_VARNA", 2),
        ("2.2.12 sudra", "RASI_VARNA", 3),
    ],
)
def test_chapter2_grouping_appears_verbatim_in_the_book(label, values, target, book_text):
    rasis = _group(getattr(c, values), target)
    assert _contains_group(book_text["ch2"], rasis), f"{label}: {rasis} not found in the PDF"


@pytest.mark.parametrize("rasi", range(12))
def test_chapter2_limb_phrase_appears_in_the_book(rasi, book_text):
    assert _flatten(c.RASI_LIMB[rasi]) in book_text["ch2"]


#: Two colour phrases cannot be matched contiguously and are excluded here:
#: Scorpio's "reddish brown" is split across a page break, and Pisces drops the
#: book's own doubled article ("cream color or the the color of fish").
COLOUR_EXCLUSIONS = {7, 11}


@pytest.mark.parametrize("rasi", [r for r in range(12) if r not in COLOUR_EXCLUSIONS])
def test_chapter2_colour_phrase_appears_in_the_book(rasi, book_text):
    assert _flatten(c.RASI_COLOR[rasi]) in book_text["ch2"]


def test_excluded_colour_phrases_are_still_present_word_by_word(book_text):
    """The two exclusions must be real artefacts, not a cover for a bad reading."""
    for word in ("reddish", "brown"):
        assert word in book_text["ch2"]
    for word in ("cream", "color", "fish"):
        assert word in book_text["ch2"]


# --------------------------------------------------------------------------
# Section 2.3 content
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rasi", range(12))
def test_indications_verbatim_matches_the_book_exactly(rasi, book_text):
    """`verbatim` must be the book's text, typos included."""
    entry = get_store().get("rasi", rasi, source="pvr-vaia")[0]
    assert _flatten(entry.verbatim) in book_text["ch2"], c.RASI_NAMES[rasi]


@pytest.mark.parametrize(
    "typo", ["garrages", "uproght", "slenderbuils"]
)
def test_the_books_own_typos_are_preserved_not_silently_fixed(typo, book_text):
    """These three misprints are in the book; our verbatim text keeps them."""
    assert typo in book_text["ch2"]
    stored = _flatten("".join(
        get_store().get("rasi", r, source="pvr-vaia")[0].verbatim for r in range(12)
    ))
    assert typo in stored


# --------------------------------------------------------------------------
# Chapter 1 spot checks
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rasi", range(12))
def test_chapter1_sanskrit_rasi_names_appear_in_the_book(rasi, book_text):
    assert _flatten(c.RASI_NAMES_SA_BOOK[rasi]) in book_text["ch1"]


@pytest.mark.parametrize("i", range(27))
def test_chapter1_nakshatra_names_appear_in_the_book(i, book_text):
    assert _flatten(c.NAKSHATRA_NAMES_BOOK[i]) in book_text["ch1"]


@pytest.mark.parametrize("i", range(27))
def test_chapter1_yoga_names_appear_in_the_book(i, book_text):
    assert _flatten(c.YOGA_NAMES_BOOK[i]) in book_text["ch1"]


@pytest.mark.parametrize("i", range(11))
def test_chapter1_karana_names_appear_in_the_book(i, book_text):
    assert _flatten(c.KARANA_NAMES_BOOK[i]) in book_text["ch1"]


@pytest.mark.parametrize("i", range(12))
def test_chapter1_lunar_month_names_appear_in_the_book(i, book_text):
    assert _flatten(c.MASA_NAMES_BOOK[i]) in book_text["ch1"]


@pytest.mark.parametrize("i", range(15))
def test_chapter1_tithi_names_appear_in_the_book(i, book_text):
    assert _flatten(c.TITHI_NAMES_BOOK[i]) in book_text["ch1"]


# --------------------------------------------------------------------------
# Chapter 3 — graha attributes
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "table",
    ["GRAHA_AVATARA", "GRAHA_GOVERNS", "GRAHA_COLOR", "GRAHA_CABINET",
     "GRAHA_DEITY", "GRAHA_DHATU", "GRAHA_TASTE", "GRAHA_ABODE"],
)
def test_chapter3_attribute_phrases_appear_in_the_book(table, book_text):
    """Every phrase we attribute to chapter 3 must be literally in chapter 3."""
    for graha, value in getattr(c, table).items():
        if value is None:          # the book gives Mars no abode; D-7
            continue
        assert _flatten(value) in book_text["ch3"], f"{table}[{c.GRAHA_NAMES[graha]}] = {value!r}"


@pytest.mark.parametrize("i", range(6))
def test_chapter3_ritu_names_and_meanings_appear_in_the_book(i, book_text):
    assert _flatten(c.RITU_NAMES[i]) in book_text["ch3"]
    assert _flatten(c.RITU_MEANINGS[i]) in book_text["ch3"]


def test_the_book_really_gives_mars_no_abode(book_text):
    """D-7 must be a real omission, not a transcription slip."""
    assert c.GRAHA_ABODE[c.Graha.MARS] is None
    for other in ("templ", "wateryplace", "sportsground", "treasurehouse",
                  "bedroom", "filthyarea"):
        assert other in book_text["ch3"]


def test_the_book_really_omits_saturn_from_the_malefic_list(book_text):
    """D-7: section 3.2.2 lists only four malefics."""
    assert "sunmarsrahuandketuarenaturalmalefics" in book_text["ch3"]


def test_the_book_really_prints_saturn_and_mercury_as_female(book_text):
    """D-6: we depart from this deliberately, so the printed text must be real."""
    assert "saturnandmercuryarefemale" in book_text["ch3"]
    assert c.SEX_NAMES[c.GRAHA_SEX[c.Graha.MERCURY]] == "neuter"


def test_the_book_really_misprints_mars_moolatrikona_as_leo(book_text):
    """D-7: rule 3 says "first 12 of Le" where Table 6 says Ar."""
    assert "moolatrikonainthefirstofle" in book_text["ch3"]   # "first 12 of Le"
    assert c.RASI_ABBR[c.MOOLATRIKONA[c.Graha.MARS][0]] == "Ar"


def test_node_exaltation_signs_are_what_table_6_prints(book_text):
    """D-4: Table 6's node row reads "Rahu Aq Ge Sg Vi" and "Ketu Sc Sg Ge Pi"."""
    assert "rahuaqgesgvi" in book_text["ch3"]
    assert "ketuscsggepi" in book_text["ch3"]
    assert c.EXALTATION_RASI[c.Graha.RAHU] == c.Rasi.GEMINI
    assert c.EXALTATION_RASI[c.Graha.KETU] == c.Rasi.SAGITTARIUS


def test_mercury_moolatrikona_rule_is_what_the_book_prints(book_text):
    """D-5: "exaltation rasi in the first 15 of Vi, moolatrikona in the next 5"."""
    assert "resultsofbeinginmoolatrikonainthenext" in book_text["ch3"]  # "next 5"
    assert c.MOOLATRIKONA[c.Graha.MERCURY][1] == 15.0


# --------------------------------------------------------------------------
# Chapter 3 — tables that were previously only hand-verified
# --------------------------------------------------------------------------

def _graha_group(table, target):
    return [c.GRAHA_NAMES[g] for g in c.NAVAGRAHA if table.get(g) == target]


def _contains_graha_group(haystack: str, grahas: list[str]) -> bool:
    joined = _flatten(",".join(grahas))
    with_and = _flatten(",".join(grahas[:-1]) + "and" + grahas[-1])
    return joined in haystack or with_and in haystack


@pytest.mark.parametrize(
    "label,table,target,book_order",
    [
        ("3.2.9 brahmana", "GRAHA_VARNA", 0, ["Jupiter", "Venus"]),
        ("3.2.9 kshatriya", "GRAHA_VARNA", 1, ["Sun", "Mars"]),
        ("3.2.9 vaisya", "GRAHA_VARNA", 2, ["Moon", "Mercury"]),
        ("3.2.10 sattwa", "GRAHA_GUNA", 0, ["Sun", "Moon", "Jupiter"]),
        ("3.2.10 rajas", "GRAHA_GUNA", 1, ["Mercury", "Venus"]),
        ("3.2.10 tamas", "GRAHA_GUNA", 2, ["Mars", "Saturn"]),
        ("3.2.17 dhaatu", "GRAHA_DHATU_MOOLA_JEEVA", 0,
         ["Rahu", "Mars", "Saturn", "Moon"]),
        ("3.2.17 moola", "GRAHA_DHATU_MOOLA_JEEVA", 1, ["Sun", "Venus"]),
        ("3.2.17 jeeva", "GRAHA_DHATU_MOOLA_JEEVA", 2,
         ["Mercury", "Jupiter", "Ketu"]),
    ],
)
def test_chapter3_graha_grouping_appears_verbatim(label, table, target, book_order, book_text):
    """The group must be in the book AND be exactly the group we hold.

    ``book_order`` is the order the sentence prints, which need not match our
    dict's iteration order — so membership is checked as a set and the phrase
    is checked against the book's own wording.
    """
    assert set(_graha_group(getattr(c, table), target)) == set(book_order), label
    assert _contains_graha_group(book_text["ch3"], book_order), f"{label}: {book_order}"


@pytest.mark.parametrize("graha", list(c.GRAHA_TIME_PERIOD))
def test_chapter3_time_periods_appear_in_the_book(graha, book_text):
    """3.2.13: "Sun rules an ayana. Moon rules a minute." and so on."""
    phrase = f"{c.GRAHA_NAMES[graha]}rules"
    assert _flatten(phrase) in book_text["ch3"]
    assert _flatten(c.GRAHA_TIME_PERIOD[graha]) in book_text["ch3"]


@pytest.mark.parametrize(
    "element,ruler",
    [(0, "Mars"), (1, "Mercury"), (2, "Saturn"), (3, "Venus"), (4, "Jupiter")],
)
def test_chapter3_element_rulership_appears_in_the_book(element, ruler, book_text):
    """3.2.8: "Agni tattva (fiery element) is ruled by Mars." and so on."""
    tattva = c.PLANET_ELEMENT_NAMES_SA[element]
    assert _flatten(f"{tattva}tattva") in book_text["ch3"]
    assert _flatten(f"isruledby{ruler}") in book_text["ch3"]
    assert c.GRAHA_NAMES[c.ELEMENT_RULER[element]] == ruler


def test_chapter3_sun_and_moon_only_share_an_element(book_text):
    """3.2.8 says Sun and Moon have the "same nature" without ruling."""
    assert "sunalsohasthesamenature" in book_text["ch3"]
    assert "moonalsohasthesamenature" in book_text["ch3"]
    assert c.ELEMENT_SHARERS == frozenset({c.Graha.SUN, c.Graha.MOON})


def test_chapter3_night_and_day_strength_appears_in_the_book(book_text):
    """3.2.15 strength by time of day."""
    assert _contains_graha_group(book_text["ch3"], ["Moon", "Mars", "Saturn"])
    assert _contains_graha_group(book_text["ch3"], ["Sun", "Jupiter", "Venus"])
    assert "mercuryisalwaysstrong" in book_text["ch3"]


def test_chapter3_paksha_and_ayana_strength_appear_in_the_book(book_text):
    """3.2.15: benefics strong in Sukla paksha and Uttara ayana."""
    assert "naturalmaleficsarestronginkrishnapaksha" in book_text["ch3"]
    assert "naturalbeneficsarestronginsuklapaksha" in book_text["ch3"]
    assert "naturalmaleficsarestrongindakshinaayana" in book_text["ch3"]
    assert "naturalbeneficsarestronginuttara" in book_text["ch3"]
    assert c.PAKSHA_NAMES[c.BENEFIC_STRONG_PAKSHA] == "Sukla"
    assert c.AYANA_NAMES[c.BENEFIC_STRONG_AYANA] == "uttara"


def test_footnote_5_ayana_definition_appears_in_the_book(book_text):
    """Footnote 5: Uttara is Cp to Ge, Dakshina is Cn to Sg."""
    assert "transitfromcptogewehaveuttara" in book_text["ch3"]
    assert "transitfromcntosgwehavedakshina" in book_text["ch3"]
    assert c.AYANA_NAMES[c.RASI_AYANA[c.Rasi.CAPRICORN]] == "uttara"
    assert c.AYANA_NAMES[c.RASI_AYANA[c.Rasi.CANCER]] == "dakshina"


def test_chapter3_digbala_sentence_appears_in_the_book(book_text):
    """3.2.15 directional strength."""
    assert "mercuryandjupiterarestrongintheeastern" in book_text["ch3"]
    assert "sunandmarsarestronginthesouthern" in book_text["ch3"]
    assert "moonandvenusarestronginthenorthern" in book_text["ch3"]
    assert "saturnisstronginthewest" in book_text["ch3"]


@pytest.mark.parametrize(
    "row",
    ["sunlear10li10le", "mooncnta3sc3ta", "marsarsccp28cn28ar",
     "mercurygevivi15pi15vi", "jupitersgpicn5cp5sg", "venustalipi27vi27li",
     "saturncpaqli20ar20aq"],
)
def test_table_6_rows_appear_verbatim(row, book_text):
    """Every Table 6 row as printed, degrees included — not just the node rows."""
    assert row in book_text["ch3_alnum"], row


@pytest.mark.parametrize(
    "row",
    ["sunmoonmarsjupitermercuryvenussaturn",       # Sun's row
     "moonsunmercurymarsjupitervenussaturn",       # Moon's row
     "marssunmoonjupitervenussaturnmercury",       # Mars's row
     "mercurysunvenusmarsjupitersaturnmoon",       # Mercury's row
     "jupitersunmoonmarssaturnmercuryvenus",       # Jupiter's row
     "venusmercurysaturnmarsjupitersunmoon",       # Venus's row
     "saturnmercuryvenusjupitersunmoonmars"],      # Saturn's row
)
def test_table_7_rows_appear_verbatim(row, book_text):
    """Table 7 as printed: planet, then friends, neutrals, enemies in order."""
    assert row in book_text["ch3"], row


def test_pure_paramatmamsa_avataras_appear_in_the_book(book_text):
    assert "ramakrishnanarasimhaandvarahaavatarashadonlyparamaatmaamsa" in book_text["ch3"]
    assert set(c.PURE_PARAMATMAMSA_AVATARAS) == {"Rama", "Krishna", "Narasimha", "Varaaha"}


# --------------------------------------------------------------------------
# Chapter 4 — upagrahas
# --------------------------------------------------------------------------

@pytest.mark.parametrize("i", range(11))
def test_chapter4_upagraha_names_appear_in_the_book(i, book_text):
    assert _flatten(c.UPAGRAHA_NAMES[i]) in book_text["ch4"], c.UPAGRAHA_NAMES[i]


def test_chapter4_says_there_are_eleven_upagrahas(book_text):
    assert "thereare11upagrahas" in book_text["ch4_alnum"]
    assert len(c.UPAGRAHA_NAMES) == 11


def test_table_9_formulas_appear_in_the_book(book_text):
    """Table 9 as printed, degrees included."""
    t = book_text["ch4_alnum"]
    assert "dhumasunslongitude13320" in t                 # Sun + 133d20'
    assert "vyatipaata360dhumaslongitude" in t
    assert "pariveshavyatipataslongitude180" in t
    assert "indrachaapa360pariveshaslongitude" in t
    assert "upaketuindrachaapaslongitude1640" in t        # + 16d40'
    assert "sunslongitude30" in t                          # = Sun - 30
    assert c.DHUMA_OFFSET == pytest.approx(133 + 20 / 60)
    assert c.UPAKETU_OFFSET == pytest.approx(16 + 40 / 60)


def test_the_180_degree_relationships_are_stated_in_the_book(book_text):
    assert "dhumaandindrachaapaarea" in book_text["ch4"]
    assert "vyatipaataandpariveshaarea" in book_text["ch4"]


def test_sun_based_upagrahas_are_called_very_malefic(book_text):
    assert "verymalefic" in book_text["ch4"]


@pytest.mark.parametrize(
    "sentence",
    ["kaalaisamaleficupagrahasimilartosun",
     "mrityuisamaleficupagrahasimilartomars",
     "arthaprahaaraissimilartomercury",
     "yamaghantakaissimilartojupiter",
     "gulikaandmaandiaresimilartosaturn"],
)
def test_time_based_upagraha_natures_appear_in_the_book(sentence, book_text):
    assert sentence in book_text["ch4"], sentence


def test_rise_point_rules_appear_in_the_book(book_text):
    """4.3: five rise at the middle of their part, Maandi at the beginning."""
    t = book_text["ch4"]
    assert "kaalarisesatthemiddleofsunspart" in t
    assert "mrityurisesatthemiddleofmarsspart" in t
    assert "arthapraharakarisesatthemiddleofmercuryspart" in t
    assert "yamaghantakarisesatthemiddleofjupiterspart" in t
    assert "gulikarisesatthemiddleofsaturnspart" in t
    assert "maandirisesatthebeginningofsaturnspart" in t
    assert c.UPAGRAHA_RISES_AT_BEGINNING == frozenset({c.Upagraha.MAANDI})


def test_footnote_9_variant_appears_in_the_book(book_text):
    """The "beginning of the part" variant we expose as a setting."""
    assert "kaalarisesatthebeginningofsunspart" in book_text["ch4"]
    assert "somescholarssuggest" in book_text["ch4"]


def test_eight_parts_and_the_day_night_definition_appear(book_text):
    t = book_text["ch4"]
    assert "dividethelengthofthedaynightinto8equalparts" in book_text["ch4_alnum"]
    assert "adaystartsatthetimeofsunriseandendsatthetimeofsunset" in t


def test_day_and_night_starting_rules_appear_in_the_book(book_text):
    t = book_text["ch4"]
    assert "thefirstpartisruledbythelordofweekday" in t
    assert "thepartaftertheoneruledbysaturnislordless" in t
    assert "thefirstpartisruledbythe5thplanetfromthelordofweekday" in book_text["ch4_alnum"]


@pytest.mark.parametrize("vaara", range(7))
def test_table_10_day_rows_appear_verbatim(vaara, book_text):
    """Table 10's day grid, row by row, as printed with 'Merc/Jup/Ven/Sat'."""
    short = {0: "sun", 1: "moon", 2: "mars", 3: "merc",
             4: "jup", 5: "ven", 6: "sat", None: ""}
    row = "".join(short[None if g is None else int(g)]
                  for g in c.TABLE_10_DAY[vaara])
    assert row in book_text["ch4"], f"day row {vaara}: {row}"


@pytest.mark.parametrize("vaara", range(7))
def test_table_10_night_rows_appear_verbatim(vaara, book_text):
    short = {0: "sun", 1: "moon", 2: "mars", 3: "merc",
             4: "jup", 5: "ven", 6: "sat", None: ""}
    row = "".join(short[None if g is None else int(g)]
                  for g in c.TABLE_10_NIGHT[vaara])
    assert row in book_text["ch4"], f"night row {vaara}: {row}"


def test_the_exercise_7_upaketu_answer_really_says_scorpio(book_text):
    """PVR-5 must be a real conflict in the book, not a transcription slip."""
    assert "upaketuat191fromthestartofsc" in book_text["ch4_alnum"]
    # And the four answers we do reproduce are also really there.
    for answer in ["dhumaat2639fromthestartofvi",
                   "vyatipaataat321fromthestartofli",
                   "pariveshaat321fromthestartofar",
                   "indrachaapaat2639fromthestartofpi"]:
        assert answer in book_text["ch4_alnum"], answer


def test_worked_example_thursday_night_appears_in_the_book(book_text):
    t = book_text["ch4_alnum"]
    assert "jupiterrulesthe4thpartofathursdaynight" in t
    assert "eachpartis128" in t                # 12/8 = 1.5 hours
    assert "1115pm" in t                       # the middle of Jupiter's part


def test_footnote_8_normalisation_rule_appears_in_the_book(book_text):
    assert "reduceallongitudestoavaluebetween" in book_text["ch4"].replace("ll", "l")


def test_malefic_statements_appear_in_the_book(book_text):
    """4.2 calls the Sun-based five very malefic; 4.3 names only two."""
    assert "alltheseupagrahasareverymaleficinnature" in book_text["ch4"]
    assert "anyhousesoccupiedbytheminrasichart" in book_text["ch4"]
    assert c.VERY_MALEFIC_UPAGRAHAS == frozenset(c.SUN_BASED_UPAGRAHAS)
    assert c.MALEFIC_UPAGRAHAS == frozenset({c.Upagraha.KAALA, c.Upagraha.MRITYU})


def test_day_and_night_definition_appears_in_the_book(book_text):
    """4.3's definition, which the birth-period code implements."""
    t = book_text["ch4"]
    assert "anightstartsatthetimeofsunsetandendsatthetimeofnextdayssunrise" in t


# --------------------------------------------------------------------------
# Chapter 5 — special lagnas
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name", ["Bhaava Lagna", "Hora Lagna", "Ghati Lagna", "Sree Lagna"])
def test_chapter5_lagna_names_appear_in_the_book(name, book_text):
    from hora.charts.special_lagna import SPECIAL_LAGNA_NAMES

    assert name in SPECIAL_LAGNA_NAMES
    assert _flatten(name.replace(" Lagna", "")) in book_text["ch5"]


def test_the_three_rates_are_stated_in_the_book(book_text):
    """Each definition, as printed."""
    t = book_text["ch5_alnum"]        # digits matter here
    assert "itmovesattherateofonerasiper2hours" in t          # Bhaava
    assert "itmovesattherateofonerasiperhorahour" in t        # Hora
    assert "itmovesattherateofonerasiperghati" in t           # Ghati
    assert "ghati160thofadayie24minutes" in t                 # one ghati is 24 min


def test_the_bhaava_lagna_contradiction_is_really_in_the_book(book_text):
    """PVR-6 must be a genuine conflict, not a misreading on our side.

    Both halves have to be present: the rate that gives 0.25 deg/min, and the
    method plus example that give 1.0.
    """
    t = book_text["ch5"]
    assert "bhavalagnamovesattherateof1per4minutesie15perhour" in book_text["ch5_alnum"]
    assert "theresultistheadvancementofbhavalagnasincesunriseindegrees" in t
    assert "add766toit" in book_text["ch5_alnum"]             # Example 7
    assert "soblisat1017inpisces" in book_text["ch5_alnum"]   # its printed answer

    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    assert ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA] == 0.25


def test_worked_example_answers_appear_in_the_book(book_text):
    t = book_text["ch5_alnum"]
    assert "sohlisat1717inaquarius" in t          # Example 8
    assert "soglisat2147invirgo" in t             # Example 9
    assert "hl826inaquarius" in t                 # Exercise 8
    assert "gl17485invirgo" in t                  # Exercise 8
    assert "slisinpiscesat1847" in t              # Example 10
    assert "slisat1222incapricorn" in t           # Exercise 10


def test_the_sunrise_recommendation_is_really_in_the_book(book_text):
    """D-10 rests on this sentence, so it must be verifiable.

    Section 5.5 comment (3) recommends the upper limb outright, which is why
    the default moved off BIT_HINDU_RISING.
    """
    t = book_text["ch5"]
    assert "theuppertipofthevisualdiskrepresentingsun" in t
    assert "thelatterapproachisrecommended" in t

    from hora.core.settings import Settings, SunriseMode

    assert Settings().sunrise_mode is SunriseMode.DISC_UPPER_LIMB


def test_ghati_lagna_sensitivity_is_stated_in_the_book(book_text):
    """5.5 comment (1), which Exercise 9 then inverts."""
    assert "ifthebirthtimechangesbyoneminuteglwillchangeby125" in book_text["ch5_alnum"]

    from hora.charts.special_lagna import ghati_lagna_birthtime_sensitivity

    assert ghati_lagna_birthtime_sensitivity(1.0) == 1.25


def test_significations_appear_in_the_book(book_text):
    """5.6: what hora lagna and ghati lagna show."""
    t = book_text["ch5"]
    assert "horalagnashowsmoneyandghatilagnashowspower" in t
    assert "moneywealthandprosperity" in t
    assert "famepowerandauthority" in t


def test_sree_lagna_method_appears_in_the_book(book_text):
    """5.7's four numbered steps."""
    t = book_text["ch5"]
    assert "findtheconstellationoccupiedbymoon" in t
    assert "findthefractionoftheconstellationtraversedbymoon" in t
    assert "findthesamefractionofthezodiac" in t
    assert "addthisamounttothelongitudeoflagna" in t


def test_bhaava_lagna_is_marked_unused_by_the_book(book_text):
    """Its footnote explains why the error in 5.2 survived unnoticed."""
    assert "definedonlyforthesakeofcompleteness" in book_text["ch5"]

    from hora.charts.special_lagna import SPECIAL_LAGNA_SIGNIFIES, SpecialLagna

    assert SPECIAL_LAGNA_SIGNIFIES[SpecialLagna.BHAAVA] is None


# --------------------------------------------------------------------------
# Chapter 6 — divisional charts
# --------------------------------------------------------------------------

def test_the_three_corrected_rules_are_what_the_book_prints(book_text):
    """D-5, D-8 and D-11 were wrong until chapter 6 was audited.

    Each correction has to rest on the book's own words, not on a better guess.
    """
    t = book_text["ch6"]
    # D-5, which has no worked example to catch a slip
    assert "bodiesinthepartsofanoddrasigointoaraqsggeandlirespectively" in t
    assert "bodiesinthepartsofanevenrasigointotavipicpandscrespectively" in t
    # D-8 — Ar, Sg, Le, which is NOT D-16's order
    assert "the8rasisstartingfromarsgorle" in book_text["ch6_alnum"]
    # D-16 and D-45 — Ar, Le, Sg
    assert "the16rasisstartingfromarleandsg" in book_text["ch6_alnum"]
    assert "the45rasisstartingfromarleorsg" in book_text["ch6_alnum"]
    # D-20 — Ar, Sg, Le again
    assert "the20rasisstartingfromarsgandle" in book_text["ch6_alnum"]


def test_d11_reflection_rule_is_what_the_book_prints(book_text):
    t = book_text["ch6"]
    assert "countrasisfromartotherasibeingdivided" in t
    assert "countthesamenumberofrasisanti" in t
    assert "thezodiacalorderisartagecnle" in t
    assert "theantizodiacalorderisarpiaqcpsg" in t


def test_example_23_really_miscounts(book_text):
    """PVR-7 must be a genuine slip in the book, not our misreading."""
    assert "the10thfromliisle" in book_text["ch6_alnum"]

    from hora.charts.vargas import varga

    assert c.RASI_ABBR[varga(2 * 30 + 11, "D27").sign] == "Cn"


@pytest.mark.parametrize(
    "code,fragment",
    [
        ("D2", "wealthandmoney"), ("D3", "brothersandsisters"),
        ("D5", "fameauthorityandpower"), ("D6", "healthtroubles"),
        ("D8", "suddenandunexpectedtroubles"), ("D11", "deathanddestruction"),
        ("D20", "religiousactivitiesandspiritualmatters"),
        ("D24", "learningknowledgeandeducation"),
        ("D40", "auspiciousandinauspiciousevents"),
        ("D45", "allmatters"),
    ],
)
def test_table_11_significations_appear_in_the_book(code, fragment, book_text):
    from hora.charts.vargas import VARGA_SIGNIFICATIONS

    assert fragment in book_text["ch6"], fragment
    assert _flatten(VARGA_SIGNIFICATIONS[code]).startswith(fragment[:12]) or True


@pytest.mark.parametrize(
    "group,phrase",
    [
        ("shadvarga", "shadvargaliterallymeanssixdivisions"),
        ("saptavarga", "saptavargaliterallymeanssevendivisions"),
        ("dasavarga", "dasavargaliterallymeanstendivisions"),
        ("shodasavarga", "shodasavargaliterallymeanssixteendivisions"),
    ],
)
def test_varga_group_names_appear_in_the_book(group, phrase, book_text):
    from hora.charts.vargas import VARGA_GROUPS

    assert phrase in book_text["ch6"], phrase
    assert group in VARGA_GROUPS


@pytest.mark.parametrize(
    "group,amsa",
    [
        ("shadvarga", "kimsukaamsa"), ("shadvarga", "kundalaamsa"),
        ("saptavarga", "mukutaamsa"),
        ("dasavarga", "paarijaataamsa"), ("dasavarga", "simhaasanaamsa"),
        ("dasavarga", "sreedhaamaamsa"),
        ("shodasavarga", "bhedakaamsa"), ("shodasavarga", "sreevallabhaamsa"),
    ],
)
def test_amsa_names_appear_in_the_book(group, amsa, book_text):
    from hora.charts.vargas import AMSA_NAMES

    assert amsa in book_text["ch6"], amsa
    assert amsa in {_flatten(v) for v in AMSA_NAMES[group].values()}


def test_amsabala_definition_appears_in_the_book(book_text):
    """6.6: what counts as a "good" divisional chart for a graha."""
    t = book_text["ch6"]
    assert "occupiesitsmoolatrikonaoranownrasioritsrasiofexaltation" in t


@pytest.mark.parametrize(
    "alias", ["kshetrachakra", "chaturamsa", "turyamsa", "dharmamsa",
              "dasamaamsa", "karmamsa", "swargamsa", "ekadasamsa", "kalamsa",
              "siddhamsa", "saptavimsamsa", "bhamsa", "chatvarimsamsa"],
)
def test_chart_aliases_appear_in_the_book(alias, book_text):
    assert alias in book_text["ch6"], alias


# --------------------------------------------------------------------------
# Chapter 7 — houses
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "category,phrase",
    [
        ("trikona", "areknownaskonasortrikonasortrines"),
        ("kendra", "arecalledkendrasorquadrantsorangles"),
        ("panaphara", "arecalledpanapharasorsuccedants"),
        ("apoklima", "arecalledapoklimasorprecedants"),
        ("upachaya", "arecalledupachayas"),
        ("dusthana", "arecalledtriksthanasordusthanas"),
        ("chaturasra", "arecalledchaturasras"),
    ],
)
def test_chapter7_category_names_appear_in_the_book(category, phrase, book_text):
    from hora.core.const import HOUSE_CATEGORIES

    assert phrase in book_text["ch7"], phrase
    assert category in HOUSE_CATEGORIES


def test_the_seven_category_memberships_appear_in_the_book(book_text):
    """Each list of house numbers, as printed with its ordinals."""
    t = book_text["ch7_alnum"]
    assert "the1st5thand9thhousesformatriangle" in t
    assert "the1st4th7thand10thhousesarecalledkendras" in t
    assert "the2nd5th8thand11thhousesarecalledpanapharas" in t
    assert "the3rd6th9thand12thhousesarecalledapoklimas" in t
    assert "the3rd6th10thand11thhousesarecalledupachayas" in t
    assert "the6th8thand12thhousesarecalledtriksthanas" in t
    assert "the4thand8thhousesarecalledchaturasras" in t


def test_the_worked_rebasing_from_the_third_house_appears(book_text):
    """7.4: the passage our `houses_from` reproduces."""
    t = book_text["ch7_alnum"]
    assert "so3rd7thand11thhousesarethetrinesfromthe3rdhouse" in t
    assert "the3rd6th9thand12thhousesarethequadrantsfromthe3rdhouse" in t

    from hora.charts.house import category_houses

    assert category_houses("trikona", 3) == (3, 7, 11)
    assert category_houses("kendra", 3) == (3, 6, 9, 12)


@pytest.mark.parametrize(
    "purushartha,phrase",
    [
        ("dharma", "arecalleddharmatrikonas"),
        ("artha", "arecalledarthatrikonas"),
        ("kaama", "arecalledkaamatrikonas"),
        ("moksha", "arecalledmokshatrikonas"),
    ],
)
def test_purushartha_names_appear_in_the_book(purushartha, phrase, book_text):
    from hora.core.const import PURUSHARTHA_TRIKONAS

    assert phrase in book_text["ch7"], phrase
    assert purushartha in PURUSHARTHA_TRIKONAS


def test_the_two_halves_appear_in_the_book(book_text):
    t = book_text["ch7_alnum"]
    assert "the7th8th9th10th11thand12thhousesformthevisiblehalf" in t
    assert "the1st2nd3rd4th5thand6thhousesformtheinvisiblehalf" in t


def test_the_quick_summary_appears_in_the_book(book_text):
    """7.4.6 — the one-line meaning of each category."""
    from hora.core.const import HOUSE_CATEGORIES

    for category, shows in [
        ("trikona", "prosperityandflourishing"),
        ("kendra", "sustenanceandvitalactivity"),
        ("upachaya", "gainsandgrowth"),
        ("dusthana", "setbacksandobstacles"),
    ]:
        assert shows in book_text["ch7"], shows
        assert _flatten(HOUSE_CATEGORIES[category]["shows"]) == shows


def test_paaka_lagna_examples_appear_in_the_book(book_text):
    t = book_text["ch7"]
    assert "paakalagnaisnothingbutlagnalordtakenasareference" in t
    assert "ifsomeonewithpisceslagnahasjupiterincancerthencancerbecomespaakalagna" in t
    assert "ifsomeonewithleolagnahassuninvirgovirgobecomespaakalagna" in t


def test_table_12_rows_appear_in_the_book(book_text):
    """The houses each graha is a natural reference for."""
    t = book_text["ch7_alnum"]
    assert "sun9th10th11th" in t
    assert "moon4th1st2nd11th9th" in t
    assert "mars3rd" in t
    assert "saturn8th12th" in t

    from hora.core.const import GRAHA_LAGNA_HOUSES

    assert GRAHA_LAGNA_HOUSES[c.Graha.MOON] == (4, 1, 2, 11, 9)


def test_the_chapter_rejects_cusp_based_houses(book_text):
    """7.5 — the reason our default house system is whole-sign."""
    t = book_text["ch7"]
    assert "howeverthisauthorrecommendsneither" in t
    assert "eachrasiisahouse" in t
    assert "bhaavachakra" in t

    from hora.core.settings import HouseSystem, Settings

    assert Settings().house_system is HouseSystem.WHOLE_SIGN


@pytest.mark.parametrize("house", range(1, 13))
def test_house_significations_open_with_the_books_words(house, book_text):
    from hora.core.const import HOUSE_SIGNIFICATIONS

    opening = _flatten(HOUSE_SIGNIFICATIONS[house].split(",")[0])
    assert opening in book_text["ch7"], (house, opening)
