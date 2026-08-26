"""A page-by-page ledger of the book, PDF pages 13 to 89.

The chapter-level suites check the rules. This one checks the *pages*, because
a chapter-level pass reads for headline rules and skips columns, footnotes and
asides — and that is precisely where five real gaps were hiding:

* Table 2's **ruling deity** column — 27 deities, never captured
* Table 5's **meaning** column — 27 glosses, never captured
* Table 3's **alternate tithi names** and the Suddha/Bahula paksha synonyms
* D-6 recorded as "Shashtamsa" where the book prints "Shashthamsa"
* §3.4's own vocabulary — adhimitra, mitra, sama, satru, adhisatru — where the
  engine had only its own invented English labels

Every page in the range is accounted for below: either it carries an assertion,
or it is listed in :data:`PROSE_PAGES` as having nothing machine-checkable.
A page in neither set fails :func:`test_every_page_is_accounted_for`.

Requires the PDF. Point ``HORA_BOOK_PDF`` at it; otherwise these skip.
"""
import os
import re
from pathlib import Path

import pytest

from hora.core import const as c
from hora.services import varga_service

BOOK_PDF = os.environ.get("HORA_BOOK_PDF")

pytestmark = pytest.mark.skipif(
    not (BOOK_PDF and Path(BOOK_PDF).is_file()),
    reason="set HORA_BOOK_PDF to the textbook PDF to run the page ledger",
)

FIRST_PAGE, LAST_PAGE = 13, 95


def _flat(text: str) -> str:
    return re.sub(r"[^a-z]", "", text.lower())


def _flat_alnum(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


@pytest.fixture(scope="module")
def pages():
    """PDF page index -> extracted text."""
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(BOOK_PDF)
    return {i: (reader.pages[i].extract_text() or "") for i in range(FIRST_PAGE, LAST_PAGE + 1)}


#: Pages whose content is narrative, philosophical or interpretive, with
#: nothing an engine can be checked against. Listed explicitly so the ledger
#: stays complete and a page is never skipped by accident.
PROSE_PAGES: dict[int, str] = {
    13: "Part 1 divider",
    14: "1.1 what astrology is; the twins argument",
    15: "1.2 India's astrology; naming",
    20: "Figure 1, the three chart styles",
    29: "1.3.13 ayanamsa prose and 1.4 dasa introduction",
    30: "1.4 dasa systems, narrative",
    31: "1.5 conclusion; a caution about mixing western technique",
    33: "2.2.5 five elements, explained by example",
    35: "2.2.7 trigunas illustrated by a parable",
    39: "3.2.1 Vishnu's avataras, narrative",
    42: "3.2.10 gunas, with a note on what sattwa means",
    46: "3.3 the home/office/picnic analogy for dignities",
    47: "3.3 the Mercury and Ketu dignity discussion",
    51: "3.5 exercise answers, prose form",
    62: "6.1 what a division is",
    72: "6.4 insights on divisional charts",
    73: "6.5 using divisional charts",
    77: "6.7 conclusion, continued",
    78: "7.1 houses introduction",
    81: "7.3.1 lagna, narrative",
    82: "7.3.2 chandra lagna, narrative",
    83: "7.3.5 paaka lagna discussion",
    87: "7.4.2 quadrants and 7.4.3 upachayas, narrative",
    88: "7.4.4 dusthanas, narrative",
    89: "7.5 the controversy over house division",
}


# --------------------------------------------------------------------------
# Chapter 1 — pages 16 to 32
# --------------------------------------------------------------------------

def test_page_16_the_nine_grahas_and_eleven_upagrahas(pages):
    """§1.3.1 states both counts, and both are structural."""
    t = _flat_alnum(pages[16])
    assert "sevenplanetsareconsideredinindianastrology" in t
    assert "11movingmathematicalpoints" in t
    assert len(c.NAVAGRAHA) == 9
    assert len(c.UPAGRAHA_NAMES) == 11


def test_page_17_table_1_rasi_boundaries(pages):
    """Every rasi runs a whole 30 degrees, ending at 59'59"."""
    t = _flat_alnum(pages[17])
    for i, abbr in enumerate(c.RASI_ABBR):
        assert _flat(abbr) in _flat(pages[17]), abbr
        # Each row reads e.g. "30 °0'0'' 59 °59'59''" — start, then end.
        assert f"{i * 30}00" in t, (abbr, "start")
        assert f"{i * 30 + 29}5959" in t, (abbr, "end")
    assert c.RASI_NAMES_SA_BOOK[6] == "Thula"


def test_page_18_houses_are_counted_from_a_reference(pages):
    """§1.3.3's horalagna-in-Cancer walkthrough."""
    t = _flat(pages[18])
    assert "therasicontainingthereferencepointchosen" in t
    from hora.charts.house import house_of_rasi

    assert house_of_rasi(c.Rasi.CANCER, c.Rasi.CANCER) == 1
    assert house_of_rasi(c.Rasi.CANCER, c.Rasi.PISCES) == 9


def test_page_21_four_pillars_and_the_pada_span(pages):
    t = _flat(pages[21])
    assert "grahasorplanets" in t and "vargachakras" in t
    assert "thelengthofanakshatrapadais" in t
    assert c.PADA_SPAN == pytest.approx(3 + 20 / 60)


@pytest.mark.parametrize("i", range(27))
def test_page_22_table_2_carries_a_ruling_deity_for_every_nakshatra(i, pages):
    """The column the chapter-level pass missed entirely."""
    deity = c.NAKSHATRA_DEITY[i]
    # "Ahirbudhanya" is broken across a line in the PDF.
    needle = _flat(deity)[:10]
    assert needle in _flat(pages[22]), (i, deity)


def test_page_22_has_twenty_seven_deities(pages):
    assert len(c.NAKSHATRA_DEITY) == len(c.NAKSHATRA_NAMES) == 27


def test_page_23_table_3_paksha_synonyms(pages):
    """"Sukla/Suddha Paksha (brighter fortnight)"."""
    t = _flat(pages[23])
    assert "suklasuddha" in t and "krishnabahula" in t
    assert "brighterfortnight" in t and "darkerfortnight" in t
    assert c.PAKSHA_SYNONYMS == [["Suddha"], ["Bahula"]]
    assert c.PAKSHA_DESCRIPTIONS == ["brighter fortnight", "darker fortnight"]


@pytest.mark.parametrize(
    "number,alternates",
    [(1, ["Pratipat", "Padyami"]), (4, ["Chaviti", "Chauth"]),
     (15, ["Paurnimasya", "Poornima"])],
)
def test_page_23_table_3_alternate_tithi_names(number, alternates, pages):
    t = _flat(pages[23])
    for name in alternates:
        assert _flat(name) in t, name
    # Subset, not equality: the 15th also picks up "Pournimasya" from the
    # Chaitra worked example on page 26, which Table 3 does not print.
    assert set(alternates) <= set(c.TITHI_ALTERNATE_NAMES[number]), number


def test_page_24_tithi_definition(pages):
    """A tithi is 12 degrees of elongation."""
    assert "exactly12" in _flat_alnum(pages[24])
    from hora.panchanga.core import TITHI_SPAN

    assert TITHI_SPAN == 12.0


def test_page_25_and_26_lunar_months(pages):
    assert "thenameofalunarmonthisdecidedbytherasi" in _flat(pages[25])
    assert _flat("Chaitra") in _flat(pages[26])
    assert c.MASA_NAMES_BOOK[c.MASA_FROM_CONJUNCTION_RASI[c.Rasi.PISCES]] == "Chaitra"


@pytest.mark.parametrize("i", range(27))
def test_page_27_table_5_carries_a_meaning_for_every_yoga(i, pages):
    """The other column the chapter-level pass missed."""
    meaning = c.YOGA_MEANINGS[i]
    assert _flat(meaning)[:12] in _flat(pages[27]), (i, meaning)


def test_page_27_has_twenty_seven_meanings():
    assert len(c.YOGA_MEANINGS) == len(c.YOGA_NAMES) == 27


def test_page_28_karana_rule_and_hora_lords(pages):
    t = _flat(pages[28])
    assert "thefirst7karanasrepeat8times" in _flat_alnum(pages[28])
    assert "saturnjupitermarssunvenusmercuryandmoon" in t
    assert [c.GRAHA_NAMES[g] for g in c.HORA_LORD_ORDER] == [
        "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"
    ]


def test_page_32_odd_and_even_rasis(pages):
    t = _flat(pages[32])
    assert "vishamarasisorojarasis" in t
    assert "samarasisoryugmarasis" in t


# --------------------------------------------------------------------------
# Chapter 2 — pages 34 to 38
# --------------------------------------------------------------------------

def test_page_34_doshas(pages):
    """The mapping D-1 records as a deviation from conventional Ayurveda."""
    t = _flat(pages[34])
    assert "arleandsgareofpittanature" in t
    assert "vaatanature" in t
    assert [c.RASI_ABBR[i] for i in range(12) if c.RASI_DOSHA[i] == 1] == ["Ta", "Vi", "Cp"]


def test_page_36_day_night_and_rising(pages):
    t = _flat(pages[36])
    assert "seershodayarasis" in t and "prishthodayarasis" in t
    assert c.RISING_NAMES[c.RASI_RISING[c.Rasi.PISCES]] == "ubhayodaya"


@pytest.mark.parametrize("rasi", range(7))
def test_pages_37_and_38_rasi_indications(rasi, pages):
    """§2.3's lists, stored in the content package."""
    from hora.content import get_store

    entry = get_store().get("rasi", rasi, source="pvr-vaia")[0]
    combined = _flat(pages[37]) + _flat(pages[38])
    assert _flat(entry.verbatim) in combined, c.RASI_NAMES[rasi]


# --------------------------------------------------------------------------
# Chapter 3 — pages 40 to 50
# --------------------------------------------------------------------------

def test_page_40_benefics_and_malefics(pages):
    t = _flat(pages[40])
    assert "saumyagrahasorsubhagrahas" in t
    assert "krooragrahasorpaapagrahas" in t


def test_page_41_cabinet_and_deities(pages):
    t = _flat(pages[41])
    for graha, role in c.GRAHA_CABINET.items():
        if graha in (c.Graha.RAHU, c.Graha.KETU):
            continue
        assert _flat(role.split(" (")[0]) in t, role


def test_page_43_seven_dhatus_and_time_periods(pages):
    t = _flat(pages[43])
    for value in c.GRAHA_DHATU.values():
        assert _flat(value) in t, value
    for value in c.GRAHA_TIME_PERIOD.values():
        assert _flat(value) in t, value


def test_page_44_digbala_and_paksha_strength(pages):
    t = _flat(pages[44])
    assert "mercuryandjupiterarestrongintheeasterndirection" in t
    assert "naturalmaleficsarestronginkrishnapaksha" in t


def test_page_45_table_6_and_the_sanskrit_dignity_terms(pages):
    t = _flat(pages[45])
    assert "uchcha" in t and "neecha" in t
    assert c.DIGNITY_NAMES_SA["exalted"] == "uchcha"
    assert c.DIGNITY_NAMES_SA["debilitated"] == "neecha"
    assert "sunlear10li10le" in _flat_alnum(pages[45])


def test_page_48_relationship_vocabulary(pages):
    """§3.4's own terms, which the engine had replaced with English labels."""
    t = _flat(pages[48])
    assert "tatkaala" in t
    assert "mitra" in t and "sama" in t and "satru" in t
    assert c.RELATIONSHIP_KINDS["temporary"] == "tatkaala"
    assert c.NATURAL_RELATION_NAMES[2] == "mitra"


def test_page_49_table_8_compound_names(pages):
    t = _flat(pages[49])
    for label, sanskrit in c.COMPOUND_RELATION_NAMES.items():
        assert _flat(sanskrit) in t, (label, sanskrit)
    assert c.COMPOUND_RELATION_GLOSSES["great_friend"] == "good friend"


def test_page_50_the_pvr3_contradiction_is_on_this_page(pages):
    """Exercise 6's answer, which contradicts Table 7. See precedence.md."""
    assert "beinganeutralplanetinnaturalrelationshipven" in _flat(pages[50])


# --------------------------------------------------------------------------
# Chapter 4 — pages 52 to 55
# --------------------------------------------------------------------------

def test_page_52_table_9(pages):
    t = _flat_alnum(pages[52])
    assert "dhumasunslongitude13320" in t
    assert c.DHUMA_OFFSET == pytest.approx(133 + 20 / 60)


def test_page_53_day_night_division(pages):
    assert "into8equalparts" in _flat_alnum(pages[53])


def test_page_54_table_10(pages):
    """Both grids, row by row."""
    t = _flat(pages[54])
    short = {0: "sun", 1: "moon", 2: "mars", 3: "merc", 4: "jup", 5: "ven",
             6: "sat", None: ""}
    for row in c.TABLE_10_DAY + c.TABLE_10_NIGHT:
        assert "".join(short[None if g is None else int(g)] for g in row) in t


def test_page_55_rise_points_and_footnote_9(pages):
    t = _flat(pages[55])
    assert "maandirisesatthebeginningofsaturnspart" in t
    assert "somescholarssuggest" in t


# --------------------------------------------------------------------------
# Chapter 5 — pages 56 to 60
# --------------------------------------------------------------------------

def test_page_56_bhaava_lagna_rate(pages):
    """The rate that PVR-6 follows, against the method on the same page."""
    assert "bhavalagnamovesattherateof1per4minutesie15perhour" in _flat_alnum(pages[56])
    from hora.charts.special_lagna import ADVANCE_PER_MINUTE, SpecialLagna

    assert ADVANCE_PER_MINUTE[SpecialLagna.BHAAVA] == 0.25


def test_page_57_hora_lagna(pages):
    assert "itmovesattherateofonerasiperhorahour" in _flat_alnum(pages[57])


def test_page_58_ghati_lagna_and_its_alias(pages):
    """"Ghati lagna is also called 'ghatika lagna'" — an alias we lacked."""
    t = _flat(pages[58])
    assert "ghatilagnaisalsocalledghatikalagna" in t
    from hora.charts.special_lagna import SPECIAL_LAGNA_ALIASES, SpecialLagna

    assert SPECIAL_LAGNA_ALIASES[SpecialLagna.GHATI] == ["Ghatika Lagna"]


def test_page_60_sree_lagna_method(pages):
    t = _flat(pages[60])
    assert "findthefractionoftheconstellationtraversedbymoon" in t
    assert "findthesamefractionofthezodiac" in t


# --------------------------------------------------------------------------
# Chapter 6 — pages 63 to 75
# --------------------------------------------------------------------------

def test_page_63_hora_chart_rule(pages):
    assert "bodiesinthefirst15ofoddrasisareinsunshora" in _flat_alnum(pages[63])


def test_page_65_d6_is_named_shashthamsa(pages):
    """The book spells it with the second h; we had "Shashtamsa"."""
    from hora.charts.vargas import VARGA_REGISTRY

    assert "shashthamsachart" in _flat(pages[65])
    assert VARGA_REGISTRY["D6"][1] == "Shashthamsa"


def test_pages_65_and_66_d8_and_d9_start_signs(pages):
    """The two rules we had wrong, each read off its own page.

    D-8 counts from Ar/Sg/Le — *not* D-16's Ar/Le/Sg. Getting these two
    confused was the original bug, so both are pinned to the printed text.
    """
    from hora.charts.vargas import _D8_START, d9_navamsa

    assert "the8rasisstartingfromarsgorle" in _flat_alnum(pages[65])
    assert _D8_START == (c.Rasi.ARIES, c.Rasi.SAGITTARIUS, c.Rasi.LEO)

    # D-9 is implemented as the cyclic rasi*9+amsa. The book states it as a
    # start sign per element; assert the two agree for every rasi rather than
    # duplicating the table as a constant.
    assert "startingfromarcpliorcn" in _flat_alnum(pages[66])
    d9_start_by_element = {
        "fire": c.Rasi.ARIES, "earth": c.Rasi.CAPRICORN,
        "air": c.Rasi.LIBRA, "water": c.Rasi.CANCER,
    }
    for rasi in range(12):
        first_navamsa = d9_navamsa(rasi * 30.0).sign
        element = c.ELEMENT_NAMES[c.RASI_ELEMENT[rasi]]
        assert first_navamsa == d9_start_by_element[element], rasi


def test_page_67_d11_reflection_rule(pages):
    t = _flat(pages[67])
    assert "countthesamenumberofrasisanti" in t


def test_page_71_d60_part_rule(pages):
    assert "multiplyitby2takedegreesandignoreminutesadd1toit" in _flat_alnum(pages[71])


def test_pages_74_and_75_varga_groups(pages):
    from hora.charts.vargas import VARGA_GROUPS

    combined = _flat(pages[74]) + _flat(pages[75])
    for group in ("shadvarga", "saptavarga", "dasavarga"):
        assert group in combined, group
    # 6.6.3 lists the ten by name; the count is the cheap invariant.
    assert len(VARGA_GROUPS["dasavarga"]) == 10


# --------------------------------------------------------------------------
# Chapter 7 — pages 79 to 85
# --------------------------------------------------------------------------

@pytest.mark.parametrize("house", range(1, 13))
def test_pages_79_and_80_house_significations(house, pages):
    combined = _flat(pages[79]) + _flat(pages[80])
    opening = _flat(c.HOUSE_SIGNIFICATIONS[house].split(",")[0])
    assert opening in combined, (house, opening)


def test_page_84_table_12(pages):
    t = _flat_alnum(pages[84])
    assert "sun9th10th11th" in t
    assert "moon4th1st2nd11th9th" in t


def test_pages_85_and_86_the_category_list(pages):
    """The category definitions run across the page break."""
    assert "the1st5thand9thhousesformatriangle" in _flat_alnum(pages[85])
    assert "chaturasras" in _flat(pages[86])
    assert c.CHATURASRA == (4, 8)



def test_page_26_table_4_lunar_months(pages):
    """Table 4 keys the month off the rasi of the Sun-Moon conjunction.

    Pisces starts Chaitra, so the table is rotated eleven signs from Aries;
    ``MASA_FROM_CONJUNCTION_RASI`` encodes that rotation.
    """
    t = _flat(pages[26])
    assert "table4lunarmonths" in _flat_alnum(pages[26])
    for month in ("chaitra", "vaisaakha", "aashaadha", "kaarteeka"):
        assert month in t, month
    assert c.MASA_NAMES_BOOK[c.MASA_FROM_CONJUNCTION_RASI[c.Rasi.PISCES]] == "Chaitra"
    assert c.MASA_NAMES_BOOK[c.MASA_FROM_CONJUNCTION_RASI[c.Rasi.ARIES]] == "Vaisaakha"
    # The same page spells the 15th tithi "Pournimasya"; Table 3 on page 23
    # spells it "Paurnimasya". Both are stored.
    assert "pournimasya" in t
    assert "Pournimasya" in c.TITHI_ALTERNATE_NAMES[15]


def test_page_64_d3_drekkana_rule(pages):
    """Example 11: Mercury 3 deg, Jupiter 19 deg, Venus 21 deg, all in Gemini."""
    from hora.charts.vargas import d3_drekkana

    t = _flat_alnum(pages[64])
    assert "dividedinto3equalpartsof10" in t
    base = c.Rasi.GEMINI * 30.0
    assert d3_drekkana(base + 3.0).sign == c.Rasi.GEMINI          # same rasi
    assert d3_drekkana(base + 19.0).sign == c.Rasi.LIBRA          # 5th from Ge
    assert d3_drekkana(base + 21.0).sign == c.Rasi.AQUARIUS       # 9th from Ge


def test_page_68_d16_kalamsa(pages):
    """D-16 counts from Ar, Le or Sg by modality, and is also called Kalamsa."""
    from hora.charts.vargas import VARGA_RULES, d16_shodasamsa

    t = _flat_alnum(pages[68])
    assert "16equalpartsof15230" in t
    assert "startingfromarleandsg" in t
    assert "kalamsa" in _flat(pages[68])
    # D-16 is computed as modality*4, which is exactly Ar/Le/Sg. Assert the
    # behaviour rather than a constant, since no start table is stored.
    assert d16_shodasamsa(c.Rasi.ARIES * 30.0).sign == c.Rasi.ARIES        # movable
    assert d16_shodasamsa(c.Rasi.TAURUS * 30.0).sign == c.Rasi.LEO         # fixed
    assert d16_shodasamsa(c.Rasi.GEMINI * 30.0).sign == c.Rasi.SAGITTARIUS  # dual
    assert "Kalamsa" in VARGA_RULES["D16"]["aliases"]


def test_page_69_d24_example_22(pages):
    """Mercury at 11 deg Ge lands in Ar; Jupiter at 19 deg Sc lands in Li."""
    from hora.charts.vargas import d24_chaturvimsamsa

    t = _flat_alnum(pages[69])
    assert "geisanoddrasiandcountingstartsfromle" in t
    assert d24_chaturvimsamsa(c.Rasi.GEMINI * 30.0 + 11.0).sign == c.Rasi.ARIES
    assert d24_chaturvimsamsa(c.Rasi.SCORPIO * 30.0 + 19.0).sign == c.Rasi.LIBRA


def test_page_70_d30_even_rasi_arcs(pages):
    """The five unequal trimsamsa arcs for even rasis, read off the bullets."""
    from hora.charts.vargas import _D30_EVEN, d40_khavedamsa

    t = _flat_alnum(pages[70])
    expected = ((5.0, c.Rasi.TAURUS), (12.0, c.Rasi.VIRGO), (20.0, c.Rasi.PISCES),
                (25.0, c.Rasi.CAPRICORN), (30.0, c.Rasi.SCORPIO))
    assert _D30_EVEN == expected
    lower = 0
    for upper, sign in expected:
        # "Bodies in 5 deg-12 deg in even rasis are placed in Vi in D-30."
        abbr = c.RASI_ABBR[sign].lower()
        needle = f"bodiesin{lower}{int(upper)}inevenrasisareplacedin{abbr}ind30"
        assert needle in t, needle
        lower = int(upper)

    # D-40 begins on the same page: 40 parts of 45 minutes, from Ar or Li.
    assert "40equalpartsof45" in t
    assert d40_khavedamsa(0.0).sign == c.Rasi.ARIES
    assert d40_khavedamsa(30.0).sign == c.Rasi.LIBRA



def test_page_19_example_1_rama_occupancies(pages):
    """Example 1 gives Sree Rama's chart as rasi occupancies.

    The page is mostly about chart *drawing* styles, which is out of scope,
    but the occupancy list is data and is the same chart chapter 3 uses.
    """
    from tests.unit.test_book_chapter3 import RAMA_PLACEMENTS

    t = _flat(pages[19])
    assert "southindianstylechart" in t and "northindiandiamond" in t.replace(
        "northindianstylediamond", "northindiandiamond")
    for graha, abbr in RAMA_PLACEMENTS.items():
        assert f"{abbr.lower()}" in t, (graha, abbr)


def test_page_59_ghati_lagna_birthtime_sensitivity(pages):
    """"If the birthtime changes by one minute, GL will change by 1.25 deg"."""
    from hora.charts.special_lagna import (
        ADVANCE_PER_MINUTE,
        SpecialLagna,
        ghati_lagna_birthtime_sensitivity,
    )

    t = _flat_alnum(pages[59])
    assert "ifthebirthtimechangesbyoneminuteglwillchangeby125" in t
    assert ADVANCE_PER_MINUTE[SpecialLagna.GHATI] == 1.25
    assert ghati_lagna_birthtime_sensitivity(1.0) == pytest.approx(1.25)


def test_page_61_exercise_10_sree_lagna_answer(pages):
    """Exercise 10 with its printed answer: Moon 15 Le 29, lagna 14 Sc 19.

    The book answers "SL is at 12 deg 22' in Capricorn". This is the only
    fully self-contained SL case in the chapter, so it is worth a round trip
    through the production function rather than a restatement of the formula.
    """
    from hora.charts.special_lagna import sree_lagna

    t = _flat_alnum(pages[61])
    assert "slisat1222incapricorn" in t

    moon = 120 + 15 + 29 / 60          # 15 Le 29
    lagna = 210 + 14 + 19 / 60         # 14 Sc 19
    sl = sree_lagna(moon, lagna)
    assert sl // 30 == c.Rasi.CAPRICORN
    assert sl % 30 == pytest.approx(12 + 22 / 60, abs=0.5 / 60)


def test_page_76_example_27_amsabala(pages):
    """Bill Cosby's Jupiter at 29 deg 49' in Sg — the worked amsabala case.

    The book prints Jupiter's sign in all sixteen charts and the resulting
    amsa in all four groups. Both are checked end to end.

    D-3 IS DELIBERATELY EXCLUDED: the example prints Li, but the book's own
    D-3 rule (page 64, section 6.2.3) sends the last 10 deg of Sg to the 9th
    from Sg, which is Le. We follow the stated rule. Neither Li nor Le is one
    of Jupiter's good signs, so every amsa count below is unaffected either
    way. Recorded as D-16 in docs/book-deviations.md.
    """
    from hora.charts.vargas import VARGA_REGISTRY, d3_drekkana

    jupiter = 240 + 29 + 49 / 60
    printed = {
        "D2": "Cn", "D4": "Vi", "D7": "Ge", "D9": "Sg", "D10": "Vi",
        "D12": "Sc", "D16": "Pi", "D20": "Pi", "D24": "Cn", "D27": "Ge",
        "D30": "Li", "D40": "Cn", "D45": "Le", "D60": "Sc",
    }
    assert c.RASI_ABBR[int(jupiter // 30)] == "Sg"
    for code, abbr in printed.items():
        got = c.RASI_ABBR[VARGA_REGISTRY[code][0](jupiter).sign]
        assert got == abbr, (code, abbr, got)

    # The documented deviation, pinned so it cannot drift unnoticed.
    assert c.RASI_ABBR[d3_drekkana(jupiter).sign] == "Le"
    assert "d3li" in _flat_alnum(pages[76])

    result = varga_service.amsabala(jupiter, c.Graha.JUPITER)
    expected = {
        "shadvarga": (3, "Vyanjanaamsa"),
        "saptavarga": (3, "Vyanjanaamsa"),
        "dasavarga": (4, "Gopuraamsa"),
        "shodasavarga": (7, "Kalpavrikshaamsa"),
    }
    for group, (count, amsa) in expected.items():
        assert result["groups"][group]["count"] == count, group
        assert result["groups"][group]["amsa"] == amsa, group


# --------------------------------------------------------------------------
# Chapter 8 — pages 90 to 95
#
# The chapter's own tests live in test_book_chapter8.py, including the two
# worked examples and the source-fidelity checks. These are the ledger entries
# that keep every page accounted for.
# --------------------------------------------------------------------------

def test_page_90_the_three_kinds_of_karaka(pages):
    t = _flat_alnum(pages[90])
    assert "therearekindsofkarakas" in t.replace("3", "")
    assert "kaaraka" in _flat(pages[90])          # footnote 20
    assert c.KARAKA_PRONUNCIATION == "kaaraka"
    assert c.KARAKA_MEANING == "one who causes"
    assert set(c.KARAKA_KINDS) == {"naisargika", "chara", "sthira"}


def test_page_91_table_13_and_the_chara_procedure(pages):
    from hora.charts.karaka import advancement

    t = _flat(pages[91])
    assert "forrahumeasuretheadvancementfromtheendofhisrasi" in t
    assert "arrangetheminthedecreasingorderofadvancement" in t
    for row in c.CHARA_KARAKAS:
        assert _flat(row["name"]) in t, row["name"]
    # Rahu at 1 deg into a rasi has advanced 29 from its end.
    assert advancement(1.0, c.Graha.RAHU) == pytest.approx(29.0)


def test_page_92_example_28(pages):
    """The worked assignment; the full check is in test_book_chapter8.py."""
    t = _flat_alnum(pages[92])
    assert "sun12ge47" in t and "rahu1cn43" in t
    assert "table14charakarakasinexample28" in t


def test_page_93_sthira_karakas(pages):
    t = _flat(pages[93])
    assert "sunorvenusstrongerfather" in t.replace(":", "")
    assert "moonormarsstrongermother" in t.replace(":", "")
    assert "weusejupiterinfemalechartsandvenusinmalecharts" in t
    assert len(c.STHIRA_KARAKAS) == 7


def test_page_94_table_15(pages):
    assert "table15primarynaisargikakarakas" in _flat_alnum(pages[94])
    assert "the4thhousefrommoonshowsmother" in _flat_alnum(pages[94])
    assert sorted(c.NAISARGIKA_KARAKA) == list(range(1, 13))


def test_page_95_table_16_and_the_exercise_answer(pages):
    t = _flat_alnum(pages[95])
    assert "table17charakarakas" in t
    assert "mercury210" in t          # AK row of the answer
    assert len(c.NAISARGIKA_KARAKATWAS) == 9


# --------------------------------------------------------------------------
# Completeness
# --------------------------------------------------------------------------

def _asserted_pages() -> set[int]:
    """Pages this module names in a test, read from its own source."""
    source = Path(__file__).read_text()
    singles = {int(n) for n in re.findall(r"def test_page_(\d+)", source)}
    pairs = {
        int(a) for a, b in re.findall(r"def test_pages_(\d+)_and_(\d+)", source)
    } | {int(b) for a, b in re.findall(r"def test_pages_(\d+)_and_(\d+)", source)}
    return singles | pairs


def test_every_page_is_accounted_for():
    """No page between 13 and 89 may be silently skipped.

    A page either carries an assertion here or is listed in PROSE_PAGES with a
    reason. Adding a page to neither is how a column like Table 2's deities
    goes unnoticed for five chapters.
    """
    covered = _asserted_pages() | set(PROSE_PAGES)
    missing = sorted(set(range(FIRST_PAGE, LAST_PAGE + 1)) - covered)
    assert not missing, (
        f"pages with neither an assertion nor a PROSE_PAGES entry: {missing}"
    )


def test_prose_pages_each_give_a_reason():
    for page, reason in PROSE_PAGES.items():
        assert FIRST_PAGE <= page <= LAST_PAGE, page
        assert len(reason) > 10, page


def test_prose_pages_and_asserted_pages_do_not_overlap():
    """A page is either checkable or it is not; claiming both hides a gap."""
    overlap = _asserted_pages() & set(PROSE_PAGES)
    assert not overlap, f"pages both asserted and marked prose: {sorted(overlap)}"
