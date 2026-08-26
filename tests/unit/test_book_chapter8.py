"""Chapter 8 — Karakas.

The chapter gives two fully worked chara-karaka assignments: Example 28 and
Exercise 11, the latter with its answer printed in Table 17. Both are used as
fixtures here and both reproduce exactly, planet for planet and arcminute for
arcminute.

One deviation: Table 14's last row prints the wrong planet name. Recorded as
D-17 in docs/book-deviations.md and pinned below.
"""
import re

import pytest

from hora.charts.karaka import (
    KarakaError,
    advancement,
    atma_karaka,
    chara_karakas,
    karaka_of,
    naisargika_karaka,
    sthira_karaka_of_spouse,
)
from hora.core.const import (
    CHARA_KARAKA_ADVANCEMENT_LABELS,
    CHARA_KARAKA_ALIASES,
    CHARA_KARAKA_NAME_ALIASES,
    CHARA_KARAKA_NOTES,
    CHARA_KARAKA_PROCEDURE,
    CHARA_KARAKA_TIE_BREAK,
    CHARA_KARAKAS,
    CHOOSING_A_KARAKA,
    GRAHA_NAMES,
    JNAATI_PRONUNCIATION_NOTE,
    KARAKA_DEFINITION,
    KARAKA_KINDS,
    KARAKA_MEANING,
    KARAKA_PRONUNCIATION,
    KARAKA_USAGE_RULES,
    KARAKA_WARNING,
    MEASURED_FROM_END_OF_RASI,
    NAISARGIKA_DEFINITION,
    NAISARGIKA_KARAKA,
    NAISARGIKA_KARAKATWAS,
    NAISARGIKA_TABLE_16_RULE,
    NAISARGIKA_USED_IN,
    NAISARGIKA_WORKED_EXAMPLES,
    SHARED_KARAKATWA_NOTE,
    STHIRA_KARAKA_OF_SPOUSE,
    STHIRA_KARAKA_OF_SPOUSE_NOTE,
    STHIRA_KARAKAS,
    STRENGTH_COMPARISON_CHAPTER,
    TABLE_16_SOURCE_NOTE,
    Graha,
)
from hora.services import karaka_service

RASI_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def lon(text: str) -> float:
    """Parse the book's "12Ge47" notation into a sidereal longitude."""
    match = re.fullmatch(r"(\d+)([A-Za-z]{2})(\d+)", text)
    assert match, text
    return (
        RASI_ABBR.index(match.group(2)) * 30
        + int(match.group(1))
        + int(match.group(3)) / 60
    )


# --------------------------------------------------------------------------
# Example 28 (section 8.2) and its answer in Table 14
# --------------------------------------------------------------------------

EXAMPLE_28 = {
    Graha.SUN: "12Ge47", Graha.MOON: "20Ar28", Graha.MARS: "13Ge51",
    Graha.MERCURY: "25Ge18", Graha.JUPITER: "5Ta40", Graha.VENUS: "17Ge21",
    Graha.SATURN: "2Ta28", Graha.RAHU: "1Cn43",
}

#: Table 14, in printed order, with the advancement the book gives.
#: The eighth row is the deviation: the book names Venus, but Venus is already
#: MK at 17 deg 21' and 2 deg 28' is Saturn's. See D-17.
TABLE_14 = [
    ("AK", "Rahu", "28°17'"), ("AmK", "Mercury", "25°18'"),
    ("BK", "Moon", "20°28'"), ("MK", "Venus", "17°21'"),
    ("PiK", "Mars", "13°51'"), ("PK", "Sun", "12°47'"),
    ("GK", "Jupiter", "5°40'"), ("DK", "Saturn", "2°28'"),
]

# --------------------------------------------------------------------------
# Exercise 11 (section 8.2) and its answer in Table 17 (section 8.5)
# --------------------------------------------------------------------------

EXERCISE_11 = {
    Graha.SUN: "9Sg36", Graha.MOON: "15Le29", Graha.MARS: "13Ar40",
    Graha.MERCURY: "21Sc00", Graha.JUPITER: "2Aq06", Graha.VENUS: "17Sg42",
    Graha.SATURN: "9Sc41", Graha.RAHU: "14Ge30",
}

TABLE_17 = [
    ("AK", "Mercury", "21°0'"), ("AmK", "Venus", "17°42'"),
    ("BK", "Rahu", "15°30'"), ("MK", "Moon", "15°29'"),
    ("PiK", "Mars", "13°40'"), ("PK", "Saturn", "9°41'"),
    ("GK", "Sun", "9°36'"), ("DK", "Jupiter", "2°6'"),
]


def _degrees(text: str) -> float:
    d, m = text.replace("'", "").split("°")
    return int(d) + int(m) / 60


@pytest.mark.parametrize("index,expected", list(enumerate(TABLE_14)))
def test_example_28_reproduces_table_14(index, expected):
    symbol, graha_name, arc = expected
    karaka = chara_karakas({g: lon(s) for g, s in EXAMPLE_28.items()})[index]
    assert karaka.symbol == symbol
    assert karaka.graha_name == graha_name
    assert karaka.advancement == pytest.approx(_degrees(arc), abs=0.5 / 60)


@pytest.mark.parametrize("index,expected", list(enumerate(TABLE_17)))
def test_exercise_11_reproduces_table_17(index, expected):
    symbol, graha_name, arc = expected
    karaka = chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})[index]
    assert karaka.symbol == symbol
    assert karaka.graha_name == graha_name
    assert karaka.advancement == pytest.approx(_degrees(arc), abs=0.5 / 60)


def test_exercise_11_separates_a_one_arcminute_gap():
    """Rahu at 15 deg 30' and Moon at 15 deg 29' must not swap.

    The tightest ordering in either example. If advancement were rounded to
    degrees, BK and MK would be decided by luck.
    """
    karakas = {k.graha_name: k for k in
               chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})}
    assert karakas["Rahu"].symbol == "BK"
    assert karakas["Moon"].symbol == "MK"
    assert karakas["Rahu"].advancement > karakas["Moon"].advancement


def test_table_14_names_the_wrong_planet_in_its_last_row():
    """D-17. The value 2 deg 28' is Saturn's; Venus is already MK.

    Pinned so the deviation cannot be quietly "fixed" into the book's typo.
    """
    karakas = chara_karakas({g: lon(s) for g, s in EXAMPLE_28.items()})
    dara = next(k for k in karakas if k.symbol == "DK")
    assert dara.graha_name == "Saturn"
    assert lon(EXAMPLE_28[Graha.SATURN]) % 30 == pytest.approx(2 + 28 / 60)
    matri = next(k for k in karakas if k.symbol == "MK")
    assert matri.graha_name == "Venus", "Venus already holds MK, so it cannot be DK"


# --------------------------------------------------------------------------
# Section 8.2's rules
# --------------------------------------------------------------------------

def test_rahu_is_measured_from_the_end_of_his_rasi():
    """"For Rahu, measure the advancement from the end of his rasi"."""
    assert advancement(lon("1Cn43"), Graha.RAHU) == pytest.approx(28 + 17 / 60)
    # Every other graha is measured from the beginning.
    assert advancement(lon("1Cn43"), Graha.SUN) == pytest.approx(1 + 43 / 60)


def test_atma_karaka_is_the_highest_advancement():
    assert atma_karaka({g: lon(s) for g, s in EXAMPLE_28.items()}).graha_name == "Rahu"
    assert atma_karaka({g: lon(s) for g, s in EXERCISE_11.items()}).graha_name == "Mercury"


def test_karaka_of_accepts_both_symbols_for_jnaati_karaka():
    """Footnote 24: GK is also written JK."""
    longitudes = {g: lon(s) for g, s in EXAMPLE_28.items()}
    assert karaka_of(longitudes, "GK").graha_name == "Jupiter"
    assert karaka_of(longitudes, "JK").graha_name == "Jupiter"


def test_two_grahas_at_the_same_longitude_share_the_karakatwa():
    """8.2: they "hold a karakatwa together and the next will have no ruler"."""
    longitudes = {g: lon(s) for g, s in EXAMPLE_28.items()}
    longitudes[Graha.MARS] = longitudes[Graha.SUN] + 30.0   # same degrees in rasi
    shared = [k.graha_name for k in chara_karakas(longitudes) if k.shared]
    assert set(shared) == {"Mars", "Sun"}


def test_no_sharing_is_reported_when_every_advancement_differs():
    karakas = chara_karakas({g: lon(s) for g, s in EXAMPLE_28.items()})
    assert not any(k.shared for k in karakas)


# --------------------------------------------------------------------------
# Section 8.1 — the three kinds are not interchangeable
# --------------------------------------------------------------------------

def test_chara_karakas_reject_ketu():
    """8.1 excludes Ketu on purpose; dropping it silently would hide a misread."""
    longitudes = {g: lon(s) for g, s in EXAMPLE_28.items()}
    longitudes[Graha.KETU] = 100.0
    with pytest.raises(KarakaError, match="Ketu"):
        chara_karakas(longitudes)


def test_chara_karakas_reject_an_incomplete_set():
    longitudes = {g: lon(s) for g, s in EXAMPLE_28.items()}
    del longitudes[Graha.SATURN]
    with pytest.raises(KarakaError, match="Saturn"):
        chara_karakas(longitudes)


@pytest.mark.parametrize("kind,count,presiding", [
    ("naisargika", 9, "Brahma"), ("chara", 8, "Vishnu"), ("sthira", 7, "Shiva"),
])
def test_the_three_kinds_have_their_counts_and_presiding_deities(kind, count, presiding):
    entry = KARAKA_KINDS[kind]
    assert entry["count"] == count
    assert entry["presiding"] == presiding
    assert len(entry["grahas"]) == count


def test_only_chara_excludes_ketu_and_only_sthira_excludes_both_nodes():
    assert set(KARAKA_KINDS["chara"]["excludes"]) == {int(Graha.KETU)}
    assert set(KARAKA_KINDS["sthira"]["excludes"]) == {int(Graha.RAHU), int(Graha.KETU)}
    assert "excludes" not in KARAKA_KINDS["naisargika"]


# --------------------------------------------------------------------------
# Tables 13, 15 and 16
# --------------------------------------------------------------------------

def test_table_13_has_eight_karakas_in_the_printed_order():
    assert [k["symbol"] for k in CHARA_KARAKAS] == [
        "AK", "AmK", "BK", "MK", "PiK", "PK", "GK", "DK"
    ]


def test_table_15_covers_all_twelve_houses():
    assert sorted(NAISARGIKA_KARAKA) == list(range(1, 13))
    assert naisargika_karaka(4)["graha_name"] == "Moon"      # "shows mother"
    assert naisargika_karaka(5)["graha_name"] == "Jupiter"   # "shows children"


@pytest.mark.parametrize("house", [0, 13, -1])
def test_naisargika_karaka_rejects_a_house_out_of_range(house):
    with pytest.raises(ValueError):
        naisargika_karaka(house)


def test_table_16_covers_all_nine_grahas_and_only_real_houses():
    assert len(NAISARGIKA_KARAKATWAS) == 9
    for graha, entries in NAISARGIKA_KARAKATWAS.items():
        assert entries, graha
        for house, matters in entries:
            assert 1 <= house <= 12, (graha, house)
            assert matters.strip()


def test_table_16_agrees_with_table_15_where_they_overlap():
    """8.4's example: "Mercury and 5th house show memory"."""
    mercury = dict(NAISARGIKA_KARAKATWAS[Graha.MERCURY])
    assert "memory" in mercury[5]
    # Table 15 gives Mercury the 10th; Table 16 must carry the same pairing.
    assert NAISARGIKA_KARAKA[10]["graha"] == Graha.MERCURY
    assert 10 in mercury


# --------------------------------------------------------------------------
# Section 8.3
# --------------------------------------------------------------------------

def test_sthira_karakas_give_father_and_mother_as_pairs():
    """"Sun or Venus (stronger): Father", not one fixed graha."""
    by_relative = {entry["relative"]: entry for entry in STHIRA_KARAKAS}
    father = by_relative["father"]
    assert father["rule"] == "stronger"
    assert set(father["grahas"]) == {Graha.SUN, Graha.VENUS}
    mother = by_relative["mother"]
    assert mother["rule"] == "stronger"
    assert set(mother["grahas"]) == {Graha.MOON, Graha.MARS}


def test_sthira_karakas_cover_seven_grahas_and_no_nodes():
    used = {g for entry in STHIRA_KARAKAS for g in entry["grahas"]}
    assert used == set(KARAKA_KINDS["sthira"]["grahas"])
    assert Graha.RAHU not in used and Graha.KETU not in used


def test_spouse_karaka_differs_by_chart_sex():
    """"Jupiter in female charts and Venus in male charts"."""
    assert sthira_karaka_of_spouse("female")["graha_name"] == "Jupiter"
    assert sthira_karaka_of_spouse("male")["graha_name"] == "Venus"


def test_spouse_karaka_rejects_anything_else():
    with pytest.raises(KarakaError, match="male"):
        sthira_karaka_of_spouse("unspecified")


# --------------------------------------------------------------------------
# Service layer
# --------------------------------------------------------------------------

def test_service_reports_advancement_in_degrees_minutes_and_seconds():
    """8.2's tie rule is stated in these units, so the response carries them."""
    result = karaka_service.chara({g: lon(s) for g, s in EXAMPLE_28.items()})
    ak = result["karakas"][0]
    assert ak["graha_name"] == "Rahu"
    assert (ak["advancement"]["degrees"], ak["advancement"]["minutes"]) == (28, 17)
    assert ak["measured_from_end_of_rasi"] is True
    assert result["karakas"][1]["measured_from_end_of_rasi"] is False


def test_service_kinds_carries_the_warning_against_mixing_them():
    payload = karaka_service.kinds()
    assert "mixed-up way" in payload["warning"]
    assert {k["key"] for k in payload["kinds"]} == {"naisargika", "chara", "sthira"}


def test_service_naisargika_marks_that_houses_are_counted_from_the_graha():
    """The distinction 8.4 turns on: "the 4th house *from* Moon"."""
    payload = karaka_service.naisargika()
    assert payload["counted_from_the_graha"] is True
    assert len(payload["primary"]) == 12
    assert len(payload["by_graha"]) == 9


# --------------------------------------------------------------------------
# The prose rules
#
# Everything above this point checks the chapter's *tables*. A first pass
# captured all of them and still missed most of what follows, because the part
# of chapter 8 that says how to *use* a karaka is prose, not a table. Found by
# re-reading pages 90 to 95 one at a time.
# --------------------------------------------------------------------------

def test_every_chara_karaka_footnote_is_captured():
    """Footnotes 22, 23 and 25 annotate four karakas between them.

    Footnote 23 is AmK's — "people who give advice" — and was the one missed.
    """
    from hora.core.const import CHARA_KARAKA_NOTES

    assert set(CHARA_KARAKA_NOTES) == {"AK", "AmK", "PK", "PiK", "GK"}
    assert "advisors" in CHARA_KARAKA_NOTES["AmK"]
    assert "inner self" in CHARA_KARAKA_NOTES["AK"]
    assert "boss" in CHARA_KARAKA_NOTES["PiK"]
    assert "paternal cousin" in CHARA_KARAKA_NOTES["GK"]


@pytest.mark.parametrize("kind,read_as", [
    ("naisargika", "house_from_karaka"),
    ("chara", "karaka_himself"),
    ("sthira", "karaka_himself"),
])
def test_each_kind_says_whether_it_is_read_directly_or_as_a_house(kind, read_as):
    """§8.3's structural rule, and the easiest thing in the chapter to get wrong.

    "sthira karakas themselves represent the physical bodies of the relatives.
    In the case of naisargika karakas, we must take the relevant house from
    the karaka." And chara karakas follow sthira: "We do not take the 7th from
    DK for spouse, but DK himself shows spouse."
    """
    assert KARAKA_KINDS[kind]["read_as"] == read_as
    assert KARAKA_KINDS[kind]["read_as_note"]


def test_the_marriage_rule_is_captured_with_the_mistake_it_corrects():
    """§8.3 names the wrong reading explicitly, so we store both halves."""
    from hora.core.const import KARAKA_USAGE_RULES

    marriage = next(r for r in KARAKA_USAGE_RULES if "marriage" in r["wrong"])
    assert "7th from Jupiter" in marriage["wrong"]
    assert "7th from Venus" in marriage["right"]
    assert "both male and female charts" in marriage["because"]


def test_choosing_a_karaka_routes_one_matter_three_ways():
    """§8.4's children example: the kind depends on the question, not the topic."""
    from hora.core.const import CHOOSING_A_KARAKA

    by_kind = {entry["kind"]: entry for entry in CHOOSING_A_KARAKA}
    assert set(by_kind) == {"naisargika", "chara", "sthira"}
    assert "5th from Jupiter" in by_kind["naisargika"]["use"]
    assert "PK" in by_kind["chara"]["use"]
    assert "death" in by_kind["sthira"]["question"]
    assert all(entry["matter"] == "children" for entry in CHOOSING_A_KARAKA)


def test_chara_karakas_carry_section_8_1s_examples_and_the_karma_claim():
    entry = KARAKA_KINDS["chara"]
    assert set(entry["examples"]) == {"mother", "father", "wife", "advisors"}
    assert "karma" in entry["also_shows"]
    assert "one life to another" in entry["also_shows"]


def test_sthira_karakas_carry_the_destruction_of_body_claim():
    """§8.1: "As Shiva presides over death, they show the destruction of body"."""
    assert "destruction of the body" in KARAKA_KINDS["sthira"]["also_shows"]


def test_the_two_truncated_relative_glosses_are_complete():
    """§8.3's parentheses were dropped on two rows in the first pass."""
    relatives = [entry["relative"] for entry in STHIRA_KARAKAS]
    mars = next(r for r in relatives if r.startswith("younger siblings"))
    assert "(spouses of siblings)" in mars
    jupiter = next(r for r in relatives if r.startswith("husband"))
    assert "(uncles and aunts)" in jupiter


def test_the_strength_comparison_is_declared_as_deferred():
    """Father and mother cannot be resolved from chapter 8 alone.

    Footnote 26 sends the comparison to a later chapter. Saying so in the
    response is the difference between a gap and a silent wrong answer.
    """
    payload = karaka_service.sthira()
    assert payload["strength_comparison_defined_in"] == "Strength of Planets and Rasis"
    stronger = [k for k in payload["karakas"] if k["rule"] == "stronger"]
    assert len(stronger) == 2
    assert all(len(k["grahas"]) == 2 for k in stronger)


def test_jnaati_pronunciation_note_is_captured():
    """Footnote 24 describes the sound, not just the two approximations."""
    from hora.core.const import JNAATI_PRONUNCIATION_NOTE

    assert "palatal" in JNAATI_PRONUNCIATION_NOTE
    assert "gnaati" in JNAATI_PRONUNCIATION_NOTE and "gyaati" in JNAATI_PRONUNCIATION_NOTE


def test_service_kinds_exposes_the_prose_rules():
    payload = karaka_service.kinds()
    assert len(payload["usage_rules"]) >= 2
    assert len(payload["choosing"]) == 3
    assert payload["jnaati_pronunciation"]
    for kind in payload["kinds"]:
        assert kind["read_as"] in {"karaka_himself", "house_from_karaka"}


# --------------------------------------------------------------------------
# The remainder
#
# A second page-by-page pass, this time enumerating every sentence on pages 90
# to 95 mechanically rather than reading for what looked important. Ninety-six
# units; these are the ones still uncovered after the first pass.
# --------------------------------------------------------------------------

def test_the_definition_of_a_karaka_is_stored_in_full():
    """§8.1 defines the word in two sentences; only the gloss was captured."""
    from hora.core.const import KARAKA_DEFINITION, KARAKA_MEANING

    assert KARAKA_MEANING == "one who causes"
    assert "significator of the matter" in KARAKA_DEFINITION
    assert "causes events related to that matter" in KARAKA_DEFINITION


def test_the_warning_carries_its_third_sentence():
    """The first two sentences say what not to do; the third says what to do."""
    from hora.core.const import KARAKA_WARNING

    assert "mixed-up way" in KARAKA_WARNING
    assert "specific purpose" in KARAKA_WARNING
    assert "understand the distinction" in KARAKA_WARNING
    assert "use them accordingly" in KARAKA_WARNING


@pytest.mark.parametrize("kind,fragment", [
    ("naisargika", "creator"),
    ("chara", "sustenance, achievements and spiritual progress"),
    ("sthira", "death"),
])
def test_each_kind_records_why_its_deity_presides(kind, fragment):
    """§8.1 gives a reason for each presiding deity, not just the name."""
    assert fragment in KARAKA_KINDS[kind]["presiding_because"]


def test_the_shared_karakatwa_note_says_how_rare_it_is():
    """§8.2: "this rarely becomes necessary".

    Without the frequency, a caller cannot tell whether the shared-karakatwa
    branch is a routine case to handle or a curiosity.
    """
    from hora.core.const import SHARED_KARAKATWA_NOTE

    assert "sthira karaka" in SHARED_KARAKATWA_NOTE
    assert "rarely" in SHARED_KARAKATWA_NOTE
    assert karaka_service.chara(
        {g: lon(s) for g, s in EXAMPLE_28.items()}
    )["shared_karakatwa_note"] == SHARED_KARAKATWA_NOTE


def test_service_kinds_carries_the_full_definition_and_warning():
    from hora.core.const import KARAKA_DEFINITION, KARAKA_WARNING

    payload = karaka_service.kinds()
    assert payload["definition"] == KARAKA_DEFINITION
    assert payload["warning"] == KARAKA_WARNING
    assert all(k["presiding_because"] for k in payload["kinds"])


# --------------------------------------------------------------------------
# Interpretive readings — the content store, not the calculation API
#
# Chapter 8 gives three readings for a graha holding a karakatwa. They are
# interpretation, so they follow the section 2.3 precedent: stored as verbatim
# text with the licence gate, never mixed into the calculation responses.
# --------------------------------------------------------------------------

def test_chapter_8_interpretive_readings_are_in_the_content_store():
    from hora.content import get_store

    store = get_store()
    assert "graha_karaka" in store.subjects()
    names = {
        entry.subject_name
        for gid in (Graha.MERCURY, Graha.RAHU)
        for entry in store.get("graha_karaka", int(gid))
    }
    assert names == {
        "Rahu as Atma Karaka",
        "Mercury as Amatya Karaka",
        "Mercury as Atma Karaka",
    }


def test_the_same_graha_reads_differently_in_different_roles():
    """Mercury as AK is not Mercury as AmK; the role is part of the key."""
    from hora.content import get_store

    entries = {e.subject_name: e for e in get_store().get("graha_karaka", int(Graha.MERCURY))}
    assert "advisors" in entries["Mercury as Amatya Karaka"].verbatim
    assert "orators" in entries["Mercury as Atma Karaka"].verbatim
    assert entries["Mercury as Amatya Karaka"].verbatim != \
        entries["Mercury as Atma Karaka"].verbatim


def test_karaka_readings_are_licence_gated_like_section_2_3():
    """OI-12. These are the author's words and are not served by default."""
    from hora.content import get_store

    for gid in (Graha.MERCURY, Graha.RAHU):
        for entry in get_store().get("graha_karaka", int(gid)):
            assert entry.licence_status == "unconfirmed"
            assert not entry.servable


def test_no_interpretive_text_leaks_into_the_calculation_responses():
    """The chapter 2 decision, held for chapter 8.

    Readings like "Rahu can show a saint" must not appear in /v1/karaka/*.
    """
    import json

    for payload in (karaka_service.kinds(), karaka_service.sthira(),
                    karaka_service.naisargika(),
                    karaka_service.chara({g: lon(s) for g, s in EXAMPLE_28.items()})):
        blob = json.dumps(payload).lower()
        for leaked in ("saint", "outcast", "revolutionary", "fickle-minded",
                       "orators", "journalists"):
            assert leaked not in blob, leaked


# --------------------------------------------------------------------------
# Source fidelity — the tables as the PDF prints them
#
# Everything above compares our code to expectations typed out by hand. These
# read the PDF, so a misreading made once and repeated in both places cannot
# survive.
# --------------------------------------------------------------------------

import os
from pathlib import Path

BOOK_PDF = os.environ.get("HORA_BOOK_PDF")

needs_pdf = pytest.mark.skipif(
    not (BOOK_PDF and Path(BOOK_PDF).is_file()),
    reason="set HORA_BOOK_PDF to the textbook PDF to run source-fidelity checks",
)

#: Chapter 8 runs from PDF page 90 (printed 79) to 95 (printed 84).
CH8_PAGES = range(90, 96)


@pytest.fixture(scope="module")
def chapter8():
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(BOOK_PDF)
    return "\n".join(reader.pages[i].extract_text() or "" for i in CH8_PAGES)


def _flat(text: str) -> str:
    return re.sub(r"[^a-z]", "", text.lower())


def _flat_alnum(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


@needs_pdf
def test_the_three_kinds_are_named_and_counted_in_the_book(chapter8):
    flat = _flat_alnum(chapter8)
    assert "naisargikakarakasnaturalsignificators9innumber" in flat
    assert "charakarakasvariablesignificators8innumber" in flat
    assert "sthirakarakasfixedsignificators7innumber" in flat


@needs_pdf
def test_the_warning_against_mixing_kinds_is_quoted_verbatim(chapter8):
    assert _flat(karaka_service.kinds()["warning"]) in _flat(chapter8)


@needs_pdf
@pytest.mark.parametrize("kind,deity", [
    ("naisargika", "Brahma"), ("chara", "Vishnu"), ("sthira", "Shiva"),
])
def test_presiding_deities_are_in_the_book(kind, deity, chapter8):
    assert _flat(f"they are presided by {deity}") in _flat(chapter8) or \
        _flat(f"are preside d by {deity}") in _flat(chapter8), (kind, deity)


@needs_pdf
def test_rahu_measured_from_the_end_is_the_books_wording(chapter8):
    assert "forrahumeasuretheadvancementfromtheendofhisrasi" in _flat(chapter8)


@needs_pdf
def test_ketu_is_excluded_from_chara_karakas_for_the_books_reason(chapter8):
    assert "theydonotincludeketu" in _flat(chapter8)
    assert "ketustandsformoksha" in _flat(chapter8)


@needs_pdf
def test_sthira_karakas_are_seven_because_only_they_have_bodies(chapter8):
    assert "includeonly7planetsbecauseonlytheyhavephysicalbodies" in _flat_alnum(chapter8)


@needs_pdf
@pytest.mark.parametrize("row", CHARA_KARAKAS)
def test_every_table_13_name_and_symbol_is_printed(row, chapter8):
    flat = _flat(chapter8)
    assert _flat(row["name"]) in flat, row["name"]
    assert _flat(row["shows"]) in flat, row["shows"]


@needs_pdf
@pytest.mark.parametrize("house", range(1, 13))
def test_every_table_15_signification_is_printed(house, chapter8):
    """The row's opening phrase, which is enough to identify the row."""
    opening = NAISARGIKA_KARAKA[house]["signifies"].split(",")[0]
    assert _flat(opening) in _flat(chapter8), (house, opening)


@needs_pdf
@pytest.mark.parametrize("graha", sorted(NAISARGIKA_KARAKATWAS))
def test_every_table_16_row_is_printed(graha, chapter8):
    flat = _flat(chapter8)
    for _house, matters in NAISARGIKA_KARAKATWAS[graha]:
        assert _flat(matters.split(",")[0]) in flat, (graha, matters)


@needs_pdf
@pytest.mark.parametrize("entry", STHIRA_KARAKAS)
def test_every_sthira_karaka_relative_is_printed(entry, chapter8):
    """The first relative named in each row."""
    first = entry["relative"].split(",")[0].split(" and ")[0]
    assert _flat(first) in _flat(chapter8), entry["relative"]


@needs_pdf
def test_the_spouse_rule_is_the_books_wording(chapter8):
    assert "weusejupiterinfemalechartsandvenusinmalecharts" in _flat(chapter8)


@needs_pdf
def test_example_28_longitudes_are_as_printed(chapter8):
    flat = _flat_alnum(chapter8)
    for graha, text in EXAMPLE_28.items():
        assert _flat_alnum(text) in flat, (graha, text)


@needs_pdf
def test_exercise_11_longitudes_are_as_printed(chapter8):
    flat = _flat_alnum(chapter8)
    for graha, text in EXERCISE_11.items():
        assert _flat_alnum(text) in flat, (graha, text)


@needs_pdf
def test_the_read_as_rule_is_the_books_wording(chapter8):
    flat = _flat(chapter8)
    assert "sthirakarakasthemselvesrepresentthephysicalbodiesoftherelatives" in flat
    assert "wemusttaketherelevanthousefromthekaraka" in flat
    assert "wedonottakethe7thfromdkforspousebutdkhimselfshowsspouse" in \
        _flat_alnum(chapter8)


@needs_pdf
def test_the_marriage_correction_is_printed(chapter8):
    flat = _flat_alnum(chapter8)
    assert "someastrologersusethe7thfromjupiterinsteadofthe7thfromvenus" in flat
    assert "venusisthenaturalsignificatorofmarriage" in flat
    assert "bothinmaleandfemalecharts" in flat


@needs_pdf
def test_sthira_should_not_replace_naisargika_is_printed(chapter8):
    assert (
        "theyshouldnotbeusedingeneralpredictiveastrologyintheplaceof"
        "naisargikakarakas" in _flat(chapter8)
    )


@needs_pdf
def test_the_children_comparison_is_printed(chapter8):
    """§8.4 routes children three ways; all three must be on the page."""
    flat = _flat_alnum(chapter8)
    assert "the5thhousefromjupitershowssons" in flat
    assert "weshouldtakethe5thfromjupiter" in flat
    assert "morecloselyrelatedtopkputrakarakaofcharakarakas" in flat
    assert "sthirakarakaforchildrenjupitershouldbeused" in flat


@needs_pdf
def test_chara_karaka_examples_and_karma_claim_are_printed(chapter8):
    flat = _flat(chapter8)
    assert "examplesaremotherfatherwifeadvisorsetc" in flat
    assert "howourkarmacumulativesumofactionsiscarriedfromonelifetoanother" in flat


@needs_pdf
def test_footnote_23_is_amks(chapter8):
    """"In practical terms, this means people who give advice"."""
    assert "peoplewhogiveadviceadvisorsandcounsellors" in _flat(chapter8)


@needs_pdf
def test_ak_throws_light_on_the_inner_self(chapter8):
    assert "akthrowslightontheinnerselfofanative" in _flat(chapter8)


@needs_pdf
def test_shiva_presides_over_death_and_shows_its_destruction(chapter8):
    assert "theyshowthedestructionofbody" in _flat(chapter8)


@needs_pdf
def test_the_two_relative_glosses_are_printed_in_full(chapter8):
    flat = _flat(chapter8)
    assert "brotherinlawandsisterinlawspousesofsiblings" in flat
    assert "otherpaternalrelativesunclesandaunts" in flat


@needs_pdf
def test_footnote_26_defers_the_strength_comparison(chapter8):
    from hora.core.const import STRENGTH_COMPARISON_CHAPTER

    assert _flat(STRENGTH_COMPARISON_CHAPTER) in _flat(chapter8)
    assert "formethodstocomparethestrengthsofplanets" in _flat(chapter8)


@needs_pdf
def test_table_17_repeats_table_14s_caption(chapter8):
    """D-18. Table 17 answers Exercise 11 but is captioned "Example 28".

    Recorded so the caption is not mistaken for a second copy of Table 14 —
    the two tables hold different data.
    """
    assert _flat(chapter8).count("charakarakasinexample") == 2
    # The two tables are genuinely different: Table 14 opens on Rahu, 17 on Mercury.
    assert "rahu301432817" in _flat_alnum(chapter8)      # Table 14, AK row
    assert "mercury2101ak" in _flat_alnum(chapter8)     # Table 17, AK row


@needs_pdf
def test_the_karaka_definition_is_verbatim(chapter8):
    from hora.core.const import KARAKA_DEFINITION

    assert _flat(KARAKA_DEFINITION) in _flat(chapter8)


@needs_pdf
def test_the_warning_is_verbatim_including_its_third_sentence(chapter8):
    from hora.core.const import KARAKA_WARNING

    assert _flat(KARAKA_WARNING) in _flat(chapter8)


@needs_pdf
def test_the_presiding_reasons_are_printed(chapter8):
    flat = _flat(chapter8)
    assert "asvishnupresidesoveractivitiesrelatedtosustenanceachievements" in flat
    assert "asshivapresidesoverdeath" in flat


@needs_pdf
def test_the_rarity_of_shared_karakatwa_is_printed(chapter8):
    assert (
        "howeverthisrarelybecomesnecessaryastwoplanetsarerarelyatexactlythe"
        "samelongitude" in _flat(chapter8)
    )


@needs_pdf
@pytest.mark.parametrize("graha_id", [3, 7])
def test_every_stored_karaka_reading_is_verbatim(graha_id, chapter8):
    """The content store's text must be the book's, character for character."""
    from hora.content import get_store

    flat = _flat(chapter8)
    for entry in get_store().get("graha_karaka", graha_id):
        assert _flat(entry.verbatim) in flat, entry.subject_name


@needs_pdf
@pytest.mark.parametrize("graha_id", [3, 7])
def test_every_stored_karaka_term_appears_in_its_own_verbatim(graha_id):
    """A term we tagged must come from the sentence it was tagged from."""
    from hora.content import get_store

    for entry in get_store().get("graha_karaka", graha_id):
        for term in entry.terms:
            assert _flat(term.term) in _flat(entry.verbatim), (
                entry.subject_name, term.term
            )


# --------------------------------------------------------------------------
# Third pass — the verbatim/editorial boundary
#
# The first two passes checked that content was *present*. Neither checked
# whether the strings we present as the book's words actually are. One was
# not: the sthira row for Venus reads "&" in the book and had been silently
# normalised to "and", which is exactly how chapter 2 lost three of the
# author's typos.
# --------------------------------------------------------------------------

@needs_pdf
def test_declared_verbatim_fields_are_verbatim(chapter8):
    """Every field declared transcribed must appear in the PDF.

    This is the check that makes VERBATIM_FIELDS mean something. Without it the
    declaration is a comment, and a comment cannot stop a paraphrase drifting
    in.

    **What it does not catch.** `_flat` lowercases and strips every non-letter
    before comparing, so case, punctuation and word order within a phrase are
    all invisible to it. It catches a paraphrase; it does not catch "Dara
    karaka" stored as "Dara Karaka". See OI-61 and
    `test_the_verbatim_check_is_case_and_punctuation_insensitive`.
    """
    from hora.core import const as const_module
    from hora.core.const import VERBATIM_FIELDS

    flat = _flat(chapter8)
    problems = []
    for constant_name, field in VERBATIM_FIELDS:
        constant = getattr(const_module, constant_name)
        rows = constant.values() if isinstance(constant, dict) else constant
        for row in rows:
            # NAISARGIKA_KARAKATWAS holds (house, matters) tuples, not dicts.
            values = (
                [matters for _house, matters in row]
                if isinstance(row, tuple)
                else [row[field]]
            )
            for value in values:
                if _flat(value) not in flat:
                    problems.append(f"{constant_name}.{field}: {value!r}")
    assert not problems, (
        "these are declared verbatim but are not in the book as written:\n  "
        + "\n  ".join(problems)
    )


@needs_pdf
def test_declared_verbatim_constants_are_verbatim(chapter8):
    from hora.core import const as const_module
    from hora.core.const import VERBATIM_CONSTANTS

    for name in VERBATIM_CONSTANTS:
        assert _flat(getattr(const_module, name)) in _flat(chapter8), name


def test_the_venus_sthira_row_keeps_the_books_ampersand():
    """§8.3 writes "&", not "and". Pinned so it cannot be tidied away again."""
    relatives = [entry["relative"] for entry in STHIRA_KARAKAS]
    venus_row = next(r for r in relatives if r.startswith("wife"))
    assert "mother-in-law & maternal grandparents" in venus_row
    assert " and maternal grandparents" not in venus_row


@needs_pdf
def test_footnote_21_explains_why_sthira_karakas_govern_death(chapter8):
    """The one footnote of the nine that had no home in the code.

    Without it, "the fixed significators time death" is an unexplained rule
    rather than an etymological consequence: sthira means fixed, and death is
    praana becoming fixed.
    """
    explained = KARAKA_KINDS["sthira"]["name_explained"]
    assert _flat(explained) in _flat(chapter8)
    assert "praana" in explained and "sthira" in explained
    assert karaka_service.sthira()["name_explained"] == explained


@needs_pdf
@pytest.mark.parametrize("number", range(20, 29))
def test_every_footnote_in_the_chapter_is_accounted_for(number, chapter8):
    """Footnotes 20 to 28. Each must be findable in the codebase somewhere.

    Enumerating them by number is the point: footnote 23 was missed on the
    first pass and footnote 21 on the second, both because they were read as
    part of a block rather than counted individually.
    """
    import pathlib

    marker = {
        20: "kaaraka",
        21: "praana",
        22: "subordinates and followers",
        23: "advisors and counsellors",
        24: "palatal",
        25: "paternal cousin",
        26: "Strength of Planets and Rasis",
        27: "sthira karaka for children",
        28: "spouse in male charts",
    }[number]
    root = pathlib.Path(__file__).resolve().parents[2]
    corpus = "\n".join(
        path.read_text(errors="ignore")
        for folder in ("src", "data")
        for path in (root / folder).rglob("*")
        if path.is_file() and path.suffix in {".py", ".yaml"}
    )
    assert _flat(marker) in _flat(corpus), f"footnote {number}: {marker!r}"


# --------------------------------------------------------------------------
# 8.1 Introduction — sentence by sentence
# --------------------------------------------------------------------------


def test_8_1_the_word_and_the_definition():
    """"The word karaka means "one who causes". Karaka of a matter is the
    significator of the matter. He is the one who causes events related to
    that matter."

    Three sentences, and the second is not a restatement of the first: "one
    who causes" is the etymology, "significator of the matter" is the
    technical sense.
    """
    assert KARAKA_MEANING == "one who causes"
    assert "significator of the matter" in KARAKA_DEFINITION
    assert "causes events related to that matter" in KARAKA_DEFINITION


def test_footnote_20_gives_the_pronunciation_not_the_spelling():
    """The word is printed "karaka" throughout; footnote 20 says how it
    sounds. Both are kept, so neither silently replaces the other."""
    assert KARAKA_PRONUNCIATION == "kaaraka"
    assert KARAKA_MEANING != KARAKA_PRONUNCIATION


@pytest.mark.parametrize(
    "kind,name,gloss,count",
    [
        ("naisargika", "Naisargika karaka", "natural significator", 9),
        ("chara", "Chara karaka", "variable significator", 8),
        ("sthira", "Sthira karaka", "fixed significator", 7),
    ],
)
def test_8_1_the_three_kinds_as_listed(kind, name, gloss, count):
    """"(1) Naisargika karakas (*natural* significators, 9 in number).
    (2) Chara karakas (*variable* significators, 8 in number), and,
    (3) Sthira karakas (*fixed* significators, 7 in number)."""
    entry = KARAKA_KINDS[kind]
    assert entry["name"] == name
    assert entry["gloss"] == gloss
    assert entry["count"] == count
    assert len(entry["grahas"]) == count


def test_8_1_there_are_exactly_three_kinds_in_the_printed_order():
    """"There are 3 kinds of karakas" — and the order matters, because §8.1
    then explains them in the same order."""
    assert list(KARAKA_KINDS) == ["naisargika", "chara", "sthira"]


def test_8_1_the_graha_sets_nest():
    """9, 8, 7 is not a coincidence: each kind drops exactly what the next
    cannot use. Sthira ⊂ chara ⊂ naisargika, so a sthira karaka is always
    also a chara and a naisargika karaka — which is precisely why §8.1 has to
    warn against mixing them up.
    """
    sets = {k: set(v["grahas"]) for k, v in KARAKA_KINDS.items()}
    assert sets["sthira"] < sets["chara"] < sets["naisargika"]
    assert sets["naisargika"] - sets["chara"] == {Graha.KETU}
    assert sets["chara"] - sets["sthira"] == {Graha.RAHU}


def test_8_1_every_exclusion_carries_its_reason():
    """Neither node is dropped without a stated reason: Ketu for standing for
    moksha, both nodes for having no physical body."""
    assert KARAKA_KINDS["naisargika"].get("excludes") is None
    for kind in ("chara", "sthira"):
        excludes = KARAKA_KINDS[kind]["excludes"]
        missing = set(KARAKA_KINDS["naisargika"]["grahas"]) - set(
            KARAKA_KINDS[kind]["grahas"])
        assert {int(g) for g in missing} == set(excludes)
        assert all(reason for reason in excludes.values())


def test_8_1_the_warning_is_stored_whole():
    """"One should not use the three types of karakas in a mixed-up way.
    Karakas of each type have a specific purpose. One should understand the
    distinction between chara, sthira and naisargika karakas clearly and use
    them accordingly."

    The third sentence is the one that says what to *do*. Its ordering —
    chara, sthira, naisargika — is not the list's order, which is why it is
    stored verbatim rather than regenerated.
    """
    assert "mixed-up way" in KARAKA_WARNING
    assert "specific purpose" in KARAKA_WARNING
    assert "use them accordingly" in KARAKA_WARNING
    assert KARAKA_WARNING.index("chara") < KARAKA_WARNING.index("sthira")
    assert KARAKA_WARNING.index("sthira") < KARAKA_WARNING.index("naisargika")


def test_8_1_naisargika_includes_both_nodes_and_the_seven():
    """"They include Rahu, Ketu and the seven planets." The only kind that
    takes all nine."""
    grahas = set(KARAKA_KINDS["naisargika"]["grahas"])
    assert Graha.RAHU in grahas and Graha.KETU in grahas
    assert len(grahas) == 9


def test_8_1_naisargika_shows_more_than_people():
    """"Naisargika karakas show **not only human beings**, but they show
    various impersonal things and matters."

    The contrast is the whole distinction from chara, which shows people. A
    stored "shows" that mentions impersonal things without the contrast loses
    the sentence's work.
    """
    entry = KARAKA_KINDS["naisargika"]
    assert entry["not_limited_to"] == "human beings"
    assert "not only human beings" in entry["shows_contrast"]
    assert "impersonal" in entry["shows"]
    assert "people" in KARAKA_KINDS["chara"]["shows"]


def test_8_1_naisargika_is_for_general_results():
    """"Naisargika karakas are very useful in phalita Jyotish, i.e. analysis
    of general results."""
    assert "phalita" in KARAKA_KINDS["naisargika"]["used_for"]
    assert "general results" in KARAKA_KINDS["naisargika"]["used_for"]


def test_8_1_chara_excludes_ketu_for_a_reason_about_sustenance():
    """"They do not include Ketu, as Ketu stands for moksha (emancipation) and
    does not stand for any person who affects one's sustenance."

    The qualifier is load-bearing. Ketu is not dropped for failing to be a
    person — he is dropped for failing to be a person **who affects one's
    sustenance**, which is Vishnu's own domain. So the exclusion follows from
    who presides, and is not a separate rule.
    """
    reason = KARAKA_KINDS["chara"]["excludes"][int(Graha.KETU)]
    assert "moksha (emancipation)" in reason
    assert "affects one's sustenance" in reason
    assert "sustenance" in KARAKA_KINDS["chara"]["presiding_because"]


def test_8_1_ketus_exclusion_agrees_with_the_moksha_trikona():
    """Chapter 7 gave moksha its own trikona and chapter 8 gives Ketu to
    moksha. The two chapters agree that moksha is the one purushaartha that
    is not about people — which is exactly §8.1's argument for dropping him.
    """
    from hora.core.const import KARAKAMSA_MOKSHA_GRAHA, PURUSHARTHA_TRIKONAS

    assert KARAKAMSA_MOKSHA_GRAHA is Graha.KETU
    assert "liberation" in PURUSHARTHA_TRIKONAS["moksha"]["meaning"]


def test_8_1_chara_shows_people_broadly_and_then_narrowly():
    """"they show people who play a role in one's life" — then, after the
    reason from Vishnu — "Chara karakas show people who play an important role
    in one's sustenance and achievements."

    Both are kept: the broad statement is what contrasts with naisargika, the
    narrow one is what the karakas are actually used for.
    """
    entry = KARAKA_KINDS["chara"]
    assert entry["shows_broadly"] == "people who play a role in one's life"
    assert "sustenance and achievements" in entry["shows"]
    assert len(entry["shows"]) > len(entry["shows_broadly"])


def test_8_1_charas_examples_are_relatives_and_advisors():
    """"Examples are – mother, father, wife, advisors etc."

    Three of the four have chara karakas of their own in Table 13; "advisors"
    is Amatya Karaka, whose printed gloss is "Ministers".
    """
    assert KARAKA_KINDS["chara"]["examples"] == (
        "mother", "father", "wife", "advisors")
    shown = {k["shows"] for k in CHARA_KARAKAS}
    assert {"Mother", "Father", "Spouse"} <= shown
    assert "Ministers" in shown


def test_8_1_chara_karakas_carry_karma_across_lives():
    """"They also show how our karma (cumulative sum of actions) is carried
    from one life to another." The gloss on karma is the book's own."""
    also = KARAKA_KINDS["chara"]["also_shows"]
    assert "cumulative sum of actions" in also
    assert "one life to another" in also


def test_8_1_chara_is_for_raja_yogas_and_spiritual_progress():
    """"Chara karakas are very useful in Raja Yogas and in spiritual
    progress." Both named, and spiritual progress is also in Vishnu's
    domain — so the use follows the deity here too."""
    used = KARAKA_KINDS["chara"]["used_for"]
    assert "raja yogas" in used.lower()
    assert "spiritual progress" in used
    assert "spiritual progress" in KARAKA_KINDS["chara"]["presiding_because"]


def test_8_1_sthira_takes_only_the_seven_because_of_bodies():
    """"Sthira karakas include only 7 planets because only they have physical
    bodies."

    The nodes are shadow points, so the reason is astronomical and both are
    dropped for the same one.
    """
    entry = KARAKA_KINDS["sthira"]
    assert len(entry["grahas"]) == 7
    assert Graha.RAHU not in entry["grahas"]
    assert Graha.KETU not in entry["grahas"]
    reasons = set(entry["excludes"].values())
    assert len(reasons) == 1
    assert "physical bodies" in reasons.pop()


def test_8_1_sthira_shows_the_destruction_of_body():
    """"As Shiva presides over death, they show the destruction of body.
    Sthira karakas are useful in timing the death of various near
    relatives."""
    entry = KARAKA_KINDS["sthira"]
    assert "destruction of the body" in entry["also_shows"]
    assert "Shiva presides over death" in entry["presiding_because"]
    assert "timing the death" in entry["used_for"]


def test_footnote_21_explains_why_the_name_is_sthira():
    """"In Indian philosophy, death is nothing but praana (life) becoming
    sthira (fixed)."

    Without it the chain reads as arbitrary: fixed significators time death.
    The footnote is what makes "sthira" mean the same thing in the name and
    in the function.
    """
    entry = KARAKA_KINDS["sthira"]
    assert "sthira (fixed)" in entry["name_explained"]
    assert entry["gloss"] == "fixed significator"


@pytest.mark.parametrize(
    "kind,deity,role",
    [("naisargika", "Brahma", "creator"),
     ("chara", "Vishnu", "sustenance"),
     ("sthira", "Shiva", "death")],
)
def test_8_1_each_kind_takes_its_domain_from_its_deity(kind, deity, role):
    """The trimurti is the chapter's organising argument, not decoration:
    Brahma creates, so naisargika karakas show everything that exists; Vishnu
    sustains, so chara karakas show sustenance; Shiva destroys, so sthira
    karakas time death. Each kind's reason names its deity's own function.
    """
    entry = KARAKA_KINDS[kind]
    assert entry["presiding"] == deity
    assert role in entry["presiding_because"]


def test_8_1_vishnu_means_the_same_thing_here_as_in_chapter_7():
    """§7.4.2 called him "the Supreme Lord who **sustains** this universe" and
    made the quadrants — sustenance — his. §8.1 gives him the chara karakas
    for the same reason. Two chapters, one function, and the engine stores
    the same word in both places.
    """
    from hora.core.const import HOUSE_CATEGORIES, MAHA_VISHNU_EPITHET

    assert HOUSE_CATEGORIES["kendra"]["presiding"] == "Sri Maha Vishnu"
    assert "sustains" in MAHA_VISHNU_EPITHET
    assert KARAKA_KINDS["chara"]["presiding"] == "Vishnu"
    assert "sustenance" in KARAKA_KINDS["chara"]["presiding_because"]


def test_8_1_the_three_kinds_have_three_distinct_uses():
    """"Karakas of each type have a specific purpose." Specific means
    distinct: no two kinds share a use, which is what makes mixing them an
    error rather than a redundancy.
    """
    uses = [v["used_for"] for v in KARAKA_KINDS.values()]
    assert len(set(uses)) == 3


def test_8_1_the_kinds_endpoint_publishes_all_of_this(client):
    """Everything §8.1 establishes has to be reachable, not just stored."""
    body = client.get("/v1/karaka/kinds").json()
    kinds = {k["key"]: k for k in body["kinds"]}
    assert set(kinds) == {"naisargika", "chara", "sthira"}
    assert [kinds[k]["count"] for k in ("naisargika", "chara", "sthira")] == [9, 8, 7]
    assert [kinds[k]["presiding"] for k in ("naisargika", "chara", "sthira")] == [
        "Brahma", "Vishnu", "Shiva"]
    assert kinds["naisargika"]["not_limited_to"] == "human beings"
    assert "not only human beings" in kinds["naisargika"]["shows_contrast"]
    assert kinds["chara"]["shows_broadly"] == "people who play a role in one's life"
    ketu = next(e for e in kinds["chara"]["excludes"] if e["graha_name"] == "Ketu")
    assert "affects one's sustenance" in ketu["reason"]


# --------------------------------------------------------------------------
# 8.2 Chara karakas — the procedure, sentence by sentence
# --------------------------------------------------------------------------


def test_8_2_the_procedure_has_three_steps_and_is_published():
    """"We use the following procedure to find chara karakas" — then three
    numbered steps.

    They lived only in a docstring until now, so no caller could read the rule
    the engine applies.
    """
    assert len(CHARA_KARAKA_PROCEDURE) == 3
    assert CHARA_KARAKA_PROCEDURE[0].startswith("Take the eight planets")
    assert CHARA_KARAKA_PROCEDURE[1] == (
        "Arrange them in the decreasing order of advancement.")
    assert "highest advancement is Atma Karaka" in CHARA_KARAKA_PROCEDURE[2]


def test_8_2_step_1_names_the_eight_planets_in_order():
    """"Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn and Rahu."

    The same order as `Graha`, with Rahu last — so the chara set is the first
    eight graha indices and Ketu is simply the one left off the end.
    """
    for name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                 "Saturn", "Rahu"):
        assert name in CHARA_KARAKA_PROCEDURE[0]
    assert list(KARAKA_KINDS["chara"]["grahas"]) == [
        Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY,
        Graha.JUPITER, Graha.VENUS, Graha.SATURN, Graha.RAHU]


def test_8_2_advancement_is_measured_from_the_beginning_of_the_rasi():
    """"find its advancement from the beginning of the rasi occupied by it" —
    so advancement is the longitude modulo 30, and never reaches 30."""
    assert "from the beginning of the rasi" in CHARA_KARAKA_PROCEDURE[0]
    for longitude in (0.0, 12.75, 29.99, 195.5, 359.9):
        value = advancement(longitude, Graha.SUN)
        assert value == pytest.approx(longitude % 30)
        assert 0 <= value < 30


def test_8_2_only_rahu_is_measured_from_the_end():
    """"For Rahu, measure the advancement from the end of his rasi."

    One graha, and the set says so rather than the rule being buried in a
    branch. Ketu is not in the chara set at all, so no question arises.
    """
    assert "For Rahu, measure the advancement from the end" in CHARA_KARAKA_PROCEDURE[0]
    assert MEASURED_FROM_END_OF_RASI == frozenset({Graha.RAHU})
    assert advancement(lon("1Cn43"), Graha.RAHU) == pytest.approx(30 - 1 - 43 / 60)
    assert advancement(lon("1Cn43"), Graha.SUN) == pytest.approx(1 + 43 / 60)


def test_8_2_rahus_measurement_is_the_complement_of_everyone_elses():
    """The two rules sum to 30 for any longitude — Rahu's advancement is what
    is left of the rasi, which is why a Rahu near the start of a sign ranks
    highest. In Example 28 that is exactly what makes him AK.
    """
    for longitude in (0.5, 12.75, 29.5, 210.25):
        forward = advancement(longitude, Graha.SUN)
        backward = advancement(longitude, Graha.RAHU)
        assert forward + backward == pytest.approx(30.0)


def test_8_2_step_2_orders_by_decreasing_advancement():
    """"Arrange them in the decreasing order of advancement." Order 1 is the
    highest, order 8 the lowest, in every case."""
    karakas = chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})
    assert [k.order for k in karakas] == list(range(1, 9))
    advancements = [k.advancement for k in karakas]
    assert advancements == sorted(advancements, reverse=True)


def test_8_2_step_3_the_highest_is_atma_karaka():
    """"The planet with the highest advancement is Atma Karaka (significator
    of self). We will denote him by AK."""
    karakas = chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})
    top = max(karakas, key=lambda k: k.advancement)
    assert top.symbol == "AK"
    assert top.name == "Atma Karaka"
    assert top.shows == "Self"
    assert atma_karaka({g: lon(s) for g, s in EXERCISE_11.items()}) == top


@pytest.mark.parametrize(
    "order,name,symbol,shows",
    [
        (1, "Atma Karaka", "AK", "Self"),
        (2, "Amatya Karaka", "AmK", "Ministers"),
        (3, "Bhratri Karaka", "BK", "Siblings"),
        (4, "Matri Karaka", "MK", "Mother"),
        (5, "Pitri Karaka", "PiK", "Father"),
        (6, "Putra Karaka", "PK", "Children"),
        (7, "Jnaati Karaka", "GK", "Rivals"),
        (8, "Dara Karaka", "DK", "Spouse"),
    ],
)
def test_table_13_row_by_row(order, name, symbol, shows):
    row = CHARA_KARAKAS[order - 1]
    assert row["name"] == name
    assert row["symbol"] == symbol
    assert row["shows"] == shows


def test_table_13_labels_only_its_two_extreme_rows():
    """The "Advancement" column reads "Highest" beside row 1 and "Lowest"
    beside row 8; the six between are unlabelled. The label is on the
    advancement, not on the karaka.
    """
    assert CHARA_KARAKA_ADVANCEMENT_LABELS == {"AK": "Highest", "DK": "Lowest"}
    labelled = {r["symbol"] for r in CHARA_KARAKAS
                if r["symbol"] in CHARA_KARAKA_ADVANCEMENT_LABELS}
    assert labelled == {CHARA_KARAKAS[0]["symbol"], CHARA_KARAKAS[-1]["symbol"]}


def test_table_13_symbols_are_unique_and_two_pairs_differ_by_one_letter():
    """AmK against AK, and PiK against PK: same first and last letter, one
    lowercase letter inserted. Nothing collides — the inserted letter survives
    uppercasing — but a truncating or fuzzy match would confuse them, so the
    eight are checked as printed.
    """
    symbols = [r["symbol"] for r in CHARA_KARAKAS]
    assert len(set(symbols)) == 8
    assert len({s.upper() for s in symbols}) == 8
    for longer, shorter in (("AmK", "AK"), ("PiK", "PK")):
        assert longer[0] == shorter[0] and longer[-1] == shorter[-1]
        assert longer.replace(longer[1], "", 1) == shorter


def test_8_2_the_tie_break_runs_degrees_then_minutes_then_seconds():
    """"If two planets have the same degrees, we should compare minutes. If
    minutes are same, we should compare the seconds."

    Comparing the float advancement does all three at once, and Exercise 11
    exercises the minutes step for real: Rahu 15º30' against Moon 15º29'.
    """
    assert "compare minutes" in CHARA_KARAKA_TIE_BREAK
    assert "compare the seconds" in CHARA_KARAKA_TIE_BREAK
    karakas = {k.graha_name: k for k in
               chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})}
    assert int(karakas["Rahu"].advancement) == int(karakas["Moon"].advancement)
    assert karakas["Rahu"].symbol == "BK" and karakas["Moon"].symbol == "MK"


def test_8_2_a_one_arcsecond_gap_still_separates_two_grahas():
    """The rule bottoms out at seconds, so a gap of one arcsecond decides the
    order rather than counting as a tie."""
    base = {g: lon(s) for g, s in EXERCISE_11.items()}
    base[Graha.MOON] = 20.0
    # Rahu is measured from the end, so a slightly *larger* longitude gives a
    # slightly smaller advancement.
    base[Graha.RAHU] = 30.0 - 20.0 + 1 / 3600
    karakas = {k.graha_name: k for k in chara_karakas(base)}
    assert karakas["Moon"].advancement > karakas["Rahu"].advancement
    assert not karakas["Moon"].shared and not karakas["Rahu"].shared


def test_8_2_an_exact_tie_shares_a_karakatwa():
    """"If two planets are exactly at the same longitude, then they will hold
    a karakatwa (signification) together and the next karakatwa will have no
    ruler."

    Both are marked shared; the engine does not invent a winner.
    """
    base = {g: lon(s) for g, s in EXERCISE_11.items()}
    base[Graha.MOON] = 20.0
    base[Graha.MARS] = 50.0
    karakas = {k.graha_name: k for k in chara_karakas(base)}
    assert karakas["Moon"].advancement == karakas["Mars"].advancement
    assert karakas["Moon"].shared and karakas["Mars"].shared


def test_8_2_the_fallback_for_a_shared_karakatwa_is_the_sthira_karaka():
    """"We should use the corresponding sthira karaka in that case. However,
    this rarely becomes necessary, as two planets are rarely at exactly the
    same longitude."

    Recorded with its own caveat. The fallback needs a strength comparison
    `chara_karakas` does not have, so it is left to the caller rather than
    guessed at.
    """
    assert "sthira karaka" in SHARED_KARAKATWA_NOTE
    assert "rarely" in SHARED_KARAKATWA_NOTE
    assert len(STHIRA_KARAKAS) == 7


def test_footnote_22_adds_meanings_the_table_column_does_not_carry():
    """"PK can also show subordinates and followers. PiK can show a boss."

    The footnote hangs off the "Persons shown" column header, so it qualifies
    the column rather than any one row.
    """
    assert "subordinates and followers" in CHARA_KARAKA_NOTES["PK"]
    assert "boss" in CHARA_KARAKA_NOTES["PiK"]
    assert CHARA_KARAKAS[5]["shows"] == "Children"
    assert CHARA_KARAKAS[4]["shows"] == "Father"


def test_footnote_23_says_what_ministers_means_in_practice():
    """"In practical terms, this means people who give advice (advisors and
    counsellors)."

    Without it "Ministers" reads as government office. §8.1's own example list
    says "advisors", so the footnote is what reconciles the two.
    """
    assert "advisors and counsellors" in CHARA_KARAKA_NOTES["AmK"]
    assert "advisors" in KARAKA_KINDS["chara"]["examples"]
    assert CHARA_KARAKAS[1]["shows"] == "Ministers"


def test_footnote_25_separates_common_use_from_literal_meaning():
    """"This karaka is commonly used for enemies or rivals. However, the
    literal meaning of "jnaati" is "paternal cousin"."

    Table 13's "Rivals" is the *common* use, not the literal meaning — the
    footnote is a correction on its own table, and both halves are kept.
    """
    note = CHARA_KARAKA_NOTES["GK"]
    assert "enemies or rivals" in note
    assert "paternal cousin" in note
    assert CHARA_KARAKAS[6]["shows"] == "Rivals"


def test_footnote_24_and_the_two_symbols_for_jnaati_karaka():
    """Table 13 prints the symbol as "GK (JK)" — both, in the cell. Footnote
    24 explains why: "jn" is hard to pronounce, so the name is approximated,
    and the symbol follows the approximation.
    """
    assert CHARA_KARAKA_ALIASES["GK"] == ["JK"]
    assert "palatal" in JNAATI_PRONUNCIATION_NOTE
    assert CHARA_KARAKA_NAME_ALIASES["Jnaati Karaka"] == [
        "Gnaati Karaka", "Gyaati Karaka"]
    positions = {g: lon(s) for g, s in EXERCISE_11.items()}
    assert karaka_of(positions, "JK") == karaka_of(positions, "GK")
    assert karaka_of(positions, "JK").graha_name == "Sun"


# --------------------------------------------------------------------------
# Example 28's conclusion, and Exercise 11's answer
# --------------------------------------------------------------------------


def test_example_28_rahu_is_the_atma_karaka():
    """"So Rahu represents the self of the native for the purpose of raja
    yogas, analysis of sustenance, achievements and spiritual evolution."

    Rahu at 1Cn43 is only 1º43' into Cancer, so measuring from the *end* gives
    him 28º17' — the highest of the eight. The whole result turns on step 1's
    last sentence.
    """
    top = atma_karaka({g: lon(s) for g, s in EXAMPLE_28.items()})
    assert top.graha_name == "Rahu"
    assert top.advancement == pytest.approx(28 + 17 / 60, abs=0.5 / 60)
    assert lon(EXAMPLE_28[Graha.RAHU]) % 30 == pytest.approx(1 + 43 / 60)


def test_example_28_ak_is_read_as_the_inner_self():
    """"AK throws light on the inner self of a native." Kept as a note on the
    karaka, not as part of Table 13's "Self"."""
    assert CHARA_KARAKA_NOTES["AK"] == "throws light on the inner self of a native"
    assert CHARA_KARAKAS[0]["shows"] == "Self"


def test_exercise_11_the_full_answer():
    """Solved end to end: Mercury AK, Venus AmK, Rahu BK, Moon MK, Mars PiK,
    Saturn PK, Sun GK, Jupiter DK.

    Two things make it a harder case than Example 28. Rahu at 14Ge30 gives
    15º30' from the end, which lands one arcminute above the Moon's 15º29';
    and Saturn 9º41' against Sun 9º36' is a second sub-degree decision.
    """
    karakas = chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})
    assert [(k.symbol, k.graha_name) for k in karakas] == [
        ("AK", "Mercury"), ("AmK", "Venus"), ("BK", "Rahu"), ("MK", "Moon"),
        ("PiK", "Mars"), ("PK", "Saturn"), ("GK", "Sun"), ("DK", "Jupiter"),
    ]
    assert not any(k.shared for k in karakas)


def test_exercise_11_the_second_sub_degree_decision():
    """Saturn 9º41' against Sun 9º36' — same degree, five arcminutes apart.
    Together with Rahu against the Moon, the exercise decides two of its eight
    places on minutes alone.
    """
    karakas = {k.graha_name: k for k in
               chara_karakas({g: lon(s) for g, s in EXERCISE_11.items()})}
    assert int(karakas["Saturn"].advancement) == int(karakas["Sun"].advancement) == 9
    assert karakas["Saturn"].symbol == "PK"
    assert karakas["Sun"].symbol == "GK"


def test_exercise_11_the_inner_self_is_read_from_mercury_as_ak():
    """"Guess the nature of the inner self of the native."

    The reading itself is PVR's prose and is licence-gated in the content
    store; what the calculation settles is *which* graha to read — Mercury,
    as AK — and that AK is the karaka the question is asking about.
    """
    top = atma_karaka({g: lon(s) for g, s in EXERCISE_11.items()})
    assert top.graha_name == "Mercury"
    assert "inner self" in CHARA_KARAKA_NOTES["AK"]


def test_8_2_the_kinds_endpoint_publishes_the_procedure(client):
    body = client.get("/v1/karaka/kinds").json()
    assert len(body["chara_procedure"]) == 3
    assert "decreasing order" in body["chara_procedure"][1]
    assert "compare the seconds" in body["chara_tie_break"]
    assert "sthira karaka" in body["shared_karakatwa"]
    assert body["measured_from_end_of_rasi"] == [{"graha": 7, "graha_name": "Rahu"}]
    rows = {r["symbol"]: r for r in body["chara_table"]}
    assert rows["AK"]["advancement"] == "Highest"
    assert rows["DK"]["advancement"] == "Lowest"
    assert rows["BK"]["advancement"] is None


# --------------------------------------------------------------------------
# 8.3 Sthira karakas — the list, line by line
# --------------------------------------------------------------------------

#: §8.3's list exactly as printed, in its printed order.
STHIRA_LIST = [
    ((Graha.SUN, Graha.VENUS), "stronger", "father"),
    ((Graha.MOON, Graha.MARS), "stronger", "mother"),
    ((Graha.MARS,), "fixed",
     ("younger siblings, brother-in-law and sister-in-law "
      "(spouses of siblings)")),
    ((Graha.MERCURY,), "fixed", "maternal relatives (uncles and aunts)"),
    ((Graha.JUPITER,), "fixed",
     ("husband, sons, paternal grandparents and other paternal relatives "
      "(uncles and aunts)")),
    ((Graha.VENUS,), "fixed",
     "wife, father-in-law, mother-in-law & maternal grandparents"),
    ((Graha.SATURN,), "fixed", "elder siblings"),
]


@pytest.mark.parametrize("grahas,rule,relative", STHIRA_LIST)
def test_8_3_the_list_line_by_line(grahas, rule, relative):
    """The seven lines of §8.3's list, each with its graha or pair."""
    row = next(r for r in STHIRA_KARAKAS if r["relative"] == relative)
    assert tuple(row["grahas"]) == grahas
    assert row["rule"] == rule


def test_8_3_the_list_is_in_the_printed_order():
    """Sun-or-Venus, Moon-or-Mars, Mars, Mercury, Jupiter, Venus, Saturn — the
    two pairs first, then the five singles in graha order."""
    assert [r["relative"] for r in STHIRA_KARAKAS] == [
        relative for _, _, relative in STHIRA_LIST]
    singles = [r["grahas"][0] for r in STHIRA_KARAKAS if r["rule"] == "fixed"]
    assert singles == sorted(singles)


def test_8_3_only_the_first_two_lines_are_pairs():
    """"Sun or Venus (stronger)" and "Moon or Mars (stronger)" — everything
    else names one graha outright. Those two are the only entries this chapter
    cannot resolve on its own.
    """
    pairs = [r for r in STHIRA_KARAKAS if r["rule"] == "stronger"]
    assert len(pairs) == 2
    assert all(len(r["grahas"]) == 2 for r in pairs)
    assert all(len(r["grahas"]) == 1 for r in STHIRA_KARAKAS if r["rule"] == "fixed")


def test_8_3_the_pairs_are_the_parents():
    """Both unresolved entries are parents — father and mother. Every other
    relative gets a fixed graha, so the strength comparison the chapter defers
    is needed for exactly two readings.
    """
    assert {r["relative"] for r in STHIRA_KARAKAS if r["rule"] == "stronger"} == {
        "father", "mother"}
    assert STRENGTH_COMPARISON_CHAPTER == "Strength of Planets and Rasis"


def test_8_3_mars_and_venus_each_appear_twice():
    """Mars is half of the mother pair and the fixed karaka of younger
    siblings; Venus is half of the father pair and the fixed karaka of wife.
    So a graha can hold two sthira roles, and the pair entries are what make
    that happen.
    """
    appearances = {}
    for row in STHIRA_KARAKAS:
        for graha in row["grahas"]:
            appearances.setdefault(graha, []).append(row["relative"])
    assert sorted(appearances[Graha.MARS]) == [
        "mother", STHIRA_LIST[2][2]]
    assert sorted(appearances[Graha.VENUS]) == ["father", STHIRA_LIST[5][2]]
    assert len(appearances) == 7


def test_8_3_every_graha_but_the_nodes_holds_a_sthira_role():
    """Seven lines, seven grahas, each named at least once — which is the
    §8.1 claim "only 7 planets because only they have physical bodies" made
    concrete."""
    named = {g for row in STHIRA_KARAKAS for g in row["grahas"]}
    assert named == set(KARAKA_KINDS["sthira"]["grahas"])
    assert len(named) == 7


def test_8_3_jupiter_and_venus_split_the_spouse_between_them():
    """Jupiter's line reads "Husband, sons, ..."; Venus's reads "Wife, ...".

    So `STHIRA_KARAKA_OF_SPOUSE` is not independent data — it falls out of the
    list. Checked against the list rather than restated, so the two cannot
    drift apart.
    """
    by_graha = {row["grahas"][0]: row["relative"]
                for row in STHIRA_KARAKAS if row["rule"] == "fixed"}
    assert by_graha[Graha.JUPITER].startswith("husband")
    assert by_graha[Graha.VENUS].startswith("wife")
    assert STHIRA_KARAKA_OF_SPOUSE["female"] == Graha.JUPITER
    assert STHIRA_KARAKA_OF_SPOUSE["male"] == Graha.VENUS


def test_footnote_27_records_the_dissent_on_saturn():
    """Saturn's line carries footnote 27. Some scholars give him children
    rather than elder siblings — recorded as dissent, not adopted, because
    §8.4 gives children to Jupiter.
    """
    saturn = next(r for r in STHIRA_KARAKAS if r["grahas"] == (Graha.SATURN,))
    assert saturn["relative"] == "elder siblings"
    assert "children instead of elder siblings" in saturn["note"]
    children = next(e for e in CHOOSING_A_KARAKA if e["kind"] == "sthira")
    assert "Jupiter" in children["use"]


def test_footnote_28_records_the_dissent_on_the_spouse_karaka():
    """"When predicting the death of spouse, we use Jupiter in female charts
    and Venus in male charts." Footnote 28's dissent — Jupiter in male charts
    too — is stored beside it and not adopted.
    """
    assert "male charts also" in STHIRA_KARAKA_OF_SPOUSE_NOTE
    assert sthira_karaka_of_spouse("male")["graha_name"] == "Venus"


# --------------------------------------------------------------------------
# 8.3's prose — what sthira karakas are and are not for
# --------------------------------------------------------------------------


def test_8_3_sthira_karakas_time_the_death_of_the_listed_relatives():
    """"They are presided by Shiva and they are used in the timing of death of
    the above relatives."

    "the above relatives" — the scope is exactly the seven lines of the list,
    not relatives in general.
    """
    entry = KARAKA_KINDS["sthira"]
    assert entry["presiding"] == "Shiva"
    assert "timing the death" in entry["used_for"]
    assert len(STHIRA_KARAKAS) == 7


def test_8_3_sthira_must_not_replace_naisargika_in_general_prediction():
    """"They should not be used in general predictive astrology in the place
    of naisargika karakas."

    Stored as a rule with the mistake it corrects, so the API can say what to
    do instead rather than only what to avoid.
    """
    rule = KARAKA_USAGE_RULES[0]
    assert "should not be used in general predictive astrology" in rule["rule"]
    assert rule["wrong"] == "the 7th from Jupiter to predict marriage"
    assert rule["right"] == "the 7th from Venus to predict marriage"


def test_8_3_the_seventh_from_venus_applies_to_both_sexes():
    """"Venus is the natural significator of marriage and the 7th from Venus
    should be used for predicting marriage, **both in male and female
    charts**."

    The qualifier is the point: marriage does not switch karaka by sex, only
    the death of a spouse does. Table 15 gives the 7th house to Venus, so the
    two agree.
    """
    assert "both male and female charts" in KARAKA_USAGE_RULES[0]["because"]
    assert NAISARGIKA_KARAKA[7]["graha"] == Graha.VENUS
    assert set(STHIRA_KARAKA_OF_SPOUSE.values()) == {Graha.JUPITER, Graha.VENUS}


def test_8_3_the_same_graha_reads_two_ways_for_one_matter():
    """The chapter's sharpest case. In a female chart, husband is read as:

    * **Jupiter himself** — his physical body, for timing death (sthira);
    * **the 7th from Venus** — for timing marriage (naisargika).

    Both involve a husband; neither reading substitutes for the other. That is
    exactly the confusion §8.1's warning against mixing the kinds exists to
    prevent, and §8.3 names it as a mistake astrologers actually make.
    """
    assert sthira_karaka_of_spouse("female")["graha_name"] == "Jupiter"
    assert NAISARGIKA_KARAKA[7]["graha"] == Graha.VENUS
    assert KARAKA_KINDS["sthira"]["read_as"] == "karaka_himself"
    assert KARAKA_KINDS["naisargika"]["read_as"] == "house_from_karaka"
    second = KARAKA_USAGE_RULES[1]
    assert second["wrong"] == "Venus for the death of a husband in a female chart"
    assert second["right"] == "Jupiter for the death of a husband in a female chart"


def test_8_3_the_reading_rule_splits_two_against_one():
    """"Another difference between sthira and naisargika karakas is that
    sthira karakas themselves represent the physical bodies... In the case of
    naisargika karakas, we must take the relevant house from the karaka." And
    then: "Chara karakas are also similar to sthira karakas in this aspect."

    So the split is 2-vs-1 with naisargika alone on one side — not three
    different rules. Only two values exist, and that is what makes the
    distinction learnable.
    """
    read_as = {k: v["read_as"] for k, v in KARAKA_KINDS.items()}
    assert len(set(read_as.values())) == 2
    assert read_as["sthira"] == read_as["chara"] != read_as["naisargika"]


def test_8_3_chara_follows_sthira_with_dk_as_the_example():
    """"We do not take the 7th from DK for spouse, but DK himself shows
    spouse."

    DK's Table 13 row already says "Spouse", so the note and the table agree:
    the karaka *is* the matter.
    """
    assert "DK himself shows spouse" in KARAKA_KINDS["chara"]["read_as_note"]
    assert CHARA_KARAKAS[-1]["symbol"] == "DK"
    assert CHARA_KARAKAS[-1]["shows"] == "Spouse"


def test_8_3_the_seventh_from_venus_is_not_venus_himself():
    """"the 7th from Venus (**and not Venus himself**) shows husband."

    Computable, and the two readings land on different rasis for every
    placement — so conflating them is never harmless.
    """
    from hora.charts.house import rasi_of_house

    for venus_rasi in range(12):
        assert rasi_of_house(venus_rasi, 7) != venus_rasi


def test_8_3_the_usage_rules_are_published(client):
    body = client.get("/v1/karaka/kinds").json()
    rules = body["usage_rules"]
    assert len(rules) == 2
    assert all(r["wrong"] and r["right"] and r["because"] for r in rules)
    assert any("general predictive astrology" in r["rule"] for r in rules)


# --------------------------------------------------------------------------
# What the verbatim check actually guarantees
# --------------------------------------------------------------------------


def test_the_verbatim_check_is_case_and_punctuation_insensitive():
    """`_flat` lowercases and strips every non-letter before comparing, so
    `test_declared_verbatim_fields_are_verbatim` cannot see a case or
    punctuation difference between our text and the book's.

    That matters twice in this chapter: Table 13 prints "Dara karaka" with a
    lowercase k (OI-60), and §8.3's list capitalises every relative
    ("Younger siblings") where we store lowercase. Neither would fail the
    check. Pinned here so the guarantee is not mistaken for a stronger one —
    see OI-61.
    """
    assert _flat("Dara karaka") == _flat("Dara Karaka")
    assert _flat("Younger siblings") == _flat("younger siblings")
    assert _flat("mother-in-law & maternal") == _flat("mother in law and maternal") \
        .replace("and", "")


def test_the_venus_row_keeps_the_ampersand_despite_the_flattening():
    """Because `_flat` erases it, the ampersand needs a check of its own —
    which is why one exists separately. §8.3's Venus line is the only entry
    in the list that uses "&" rather than "and".
    """
    venus = next(r for r in STHIRA_KARAKAS if r["grahas"] == (Graha.VENUS,))
    assert "&" in venus["relative"]
    assert sum("&" in r["relative"] for r in STHIRA_KARAKAS) == 1


# --------------------------------------------------------------------------
# 8.4 Naisargika karakas — Table 15, cell by cell
# --------------------------------------------------------------------------

#: Table 15 exactly as printed: house, From Planet, Matters signified.
TABLE_15 = [
    (1, Graha.SUN, "Self, physical constitution, soul, health"),
    (2, Graha.JUPITER, "Family, wealth"),
    (3, Graha.MARS, "Younger siblings, courage"),
    (4, Graha.MOON, "Mother"),
    (5, Graha.JUPITER, "Children"),
    (6, Graha.MARS, "Enemies"),
    (7, Graha.VENUS, "Wife, husband, marital bliss, relationships"),
    (8, Graha.SATURN, "Longevity, troubles"),
    (9, Graha.JUPITER, "Teacher, religion, fortune"),
    (10, Graha.MERCURY, "Work, achievements, honors"),
    (11, Graha.JUPITER, "Elder siblings"),
    (12, Graha.SATURN, "Losses"),
]


@pytest.mark.parametrize("house,graha,signifies", TABLE_15)
def test_table_15_cell_by_cell(house, graha, signifies):
    entry = NAISARGIKA_KARAKA[house]
    assert entry["graha"] == graha
    assert entry["signifies"] == signifies


def test_table_15_uses_only_the_seven_planets():
    """Rahu and Ketu appear nowhere in Table 15, though both have rows in
    Table 16. So the primary list is drawn from the seven, and the nodes
    contribute only secondary significations.
    """
    grahas = {g for _, g, _ in TABLE_15}
    assert Graha.RAHU not in grahas and Graha.KETU not in grahas
    assert grahas == set(KARAKA_KINDS["sthira"]["grahas"])
    assert {Graha.RAHU, Graha.KETU} <= set(NAISARGIKA_KARAKATWAS)


def test_table_15_gives_jupiter_four_houses():
    """Jupiter holds the 2nd, 5th, 9th and 11th — a third of the table, and
    more than any other graha. Mars and Saturn take two each; Sun, Moon,
    Mercury and Venus one each.
    """
    from collections import Counter

    counts = Counter(g for _, g, _ in TABLE_15)
    assert counts[Graha.JUPITER] == 4
    assert sorted(h for h, g, _ in TABLE_15 if g == Graha.JUPITER) == [2, 5, 9, 11]
    assert counts[Graha.MARS] == counts[Graha.SATURN] == 2
    assert sum(counts.values()) == 12


def test_table_15_is_read_as_a_house_from_the_graha():
    """"the 4th house from Moon shows mother" — the 4th house *from Moon*, not
    the 4th house of the chart. The header says "From Planet" for the same
    reason.
    """
    assert KARAKA_KINDS["naisargika"]["read_as"] == "house_from_karaka"
    assert karaka_service.naisargika()["counted_from_the_graha"] is True


@pytest.mark.parametrize(
    "house,graha,shows",
    [(4, Graha.MOON, "mother"), (5, Graha.JUPITER, "sons")],
)
def test_8_4_the_two_table_15_worked_examples(house, graha, shows):
    """"For example, the 4th house from Moon shows mother. The 5th house from
    Jupiter shows sons."""
    example = next(e for e in NAISARGIKA_WORKED_EXAMPLES
                   if e["house"] == house and e["graha"] == graha)
    assert example["shows"] == shows
    assert example["table"] == 15
    assert NAISARGIKA_KARAKA[house]["graha"] == graha


def test_8_4_says_sons_where_table_15_says_children():
    """The prose reads "The 5th house from Jupiter shows **sons**"; Table 15's
    5th row reads "Children"; Table 16's Jupiter (5th) reads "children,
    intelligence".

    Not a conflict — the narrower word appears twice for Jupiter, §8.3's
    sthira line also giving him "Husband, **sons**...". Both are kept rather
    than one being normalised into the other.
    """
    assert NAISARGIKA_KARAKA[5]["signifies"] == "Children"
    jupiter = dict(NAISARGIKA_KARAKATWAS[Graha.JUPITER])
    assert "children" in jupiter[5]
    sthira = next(r for r in STHIRA_KARAKAS if r["grahas"] == (Graha.JUPITER,))
    assert "sons" in sthira["relative"]


# --------------------------------------------------------------------------
# 8.4 Table 16, cell by cell
# --------------------------------------------------------------------------

#: Table 16 exactly as printed, semicolon-separated cell by cell.
TABLE_16 = {
    Graha.SUN: [(1, "Self, soul, constitution, health"), (5, "fame, power"),
                (9, "father, boss"), (10, "career, achievements")],
    Graha.MOON: [(1, "Mind"), (4, "mother, peace of mind"), (11, "friends")],
    Graha.MARS: [(3, "Courage, younger siblings"), (4, "real estate"),
                 (5, "scholarship in Nyaya sastra, speculation"),
                 (6, "enemies, diseases, accidents, loans")],
    Graha.MERCURY: [(2, "Speech"), (4, "learning"),
                    (5, "memory, scholarship, students"),
                    (10, "work, achievements, honors"), (11, "credits")],
    Graha.JUPITER: [(2, "Family, wealth"), (4, "traditional learning"),
                    (5, "children, intelligence"),
                    (9, "teacher, religion, fortune"),
                    (11, "elder brother, gains")],
    Graha.VENUS: [(4, "Vehicles"), (7, "wife, husband, marital bliss"),
                  (12, "bed pleasures")],
    Graha.SATURN: [(5, "Following"), (6, "servants"), (8, "Longevity, troubles"),
                   (12, "losses, hospitalization")],
    Graha.RAHU: [(6, "Accidents"), (8, "occult knowledge"),
                 (9, "pilgrimages, going abroad")],
    Graha.KETU: [(8, "Occult knowledge"), (9, "pilgrimages, going abroad"),
                 (12, "moksha")],
}


@pytest.mark.parametrize("graha", list(TABLE_16))
def test_table_16_row_by_row(graha):
    """Each planet's whole row, in the printed order, cell for cell."""
    assert list(NAISARGIKA_KARAKATWAS[graha]) == [
        tuple(cell) for cell in TABLE_16[graha]]


def test_table_16_has_all_nine_planets_in_graha_order():
    """Sun through Ketu — the same order as `Graha`, so the table can be read
    straight down."""
    assert list(NAISARGIKA_KARAKATWAS) == [
        Graha.SUN, Graha.MOON, Graha.MARS, Graha.MERCURY, Graha.JUPITER,
        Graha.VENUS, Graha.SATURN, Graha.RAHU, Graha.KETU]


def test_table_16_houses_ascend_within_each_row():
    """Every row lists its houses in increasing order. A row out of order
    would be a transcription slip rather than a claim."""
    for graha, entries in NAISARGIKA_KARAKATWAS.items():
        houses = [house for house, _ in entries]
        assert houses == sorted(houses), GRAHA_NAMES[graha]
        assert len(set(houses)) == len(houses), GRAHA_NAMES[graha]


def test_table_16_covers_every_house_across_the_nine_rows():
    """All twelve houses appear somewhere in Table 16 — no house is left
    without a natural significator."""
    covered = {house for entries in NAISARGIKA_KARAKATWAS.values()
               for house, _ in entries}
    assert covered == set(range(1, 13))


def test_table_16_saturn_keeps_the_books_capital_in_the_middle_of_a_row():
    """Saturn's row reads "Following (5th); servants (6th)**,** Longevity,
    troubles (8th)" — a comma where every other separator is a semicolon, and
    "Longevity" capitalised mid-row.

    The capital is the author's and is kept. The comma is lost by storing the
    row as cells rather than as raw text, which is a structural choice, not a
    transcription one.
    """
    saturn = dict(NAISARGIKA_KARAKATWAS[Graha.SATURN])
    assert saturn[8] == "Longevity, troubles"
    assert saturn[8][0].isupper()


def test_table_16_only_the_first_cell_of_each_row_is_capitalised():
    """Every row opens with a capital and continues lowercase — except
    Saturn's, whose (8th) cell is also capitalised. Pinned so the exception
    stays visible rather than being tidied away.
    """
    exceptions = []
    for graha, entries in NAISARGIKA_KARAKATWAS.items():
        for index, (house, matters) in enumerate(entries):
            if index and matters[0].isupper():
                exceptions.append((GRAHA_NAMES[graha], house))
    assert exceptions == [("Saturn", 8)]


# --------------------------------------------------------------------------
# 8.4 — how the two tables relate
# --------------------------------------------------------------------------


@pytest.mark.parametrize("house,graha,signifies", TABLE_15)
def test_every_table_15_row_is_confirmed_by_table_16(house, graha, signifies):
    """The strong property the chapter never states: for all twelve houses,
    Table 15's primary graha carries that same house in Table 16.

    So Table 15 is a view of Table 16 and not an independent list — which is
    why a change to either would have to be a change to both.
    """
    houses_in_16 = {h for h, _ in NAISARGIKA_KARAKATWAS[graha]}
    assert house in houses_in_16


def test_the_reverse_does_not_hold_which_is_why_table_15_says_primary():
    """Table 16 gives the 5th house to five different grahas — Sun, Mars,
    Mercury, Jupiter and Saturn — while Table 15 names only Jupiter.

    That is what "**Primary** Naisargika Karakas" in Table 15's title means:
    one karaka per house chosen out of several, not the only one.
    """
    from collections import defaultdict

    by_house = defaultdict(set)
    for graha, entries in NAISARGIKA_KARAKATWAS.items():
        for house, _ in entries:
            by_house[house].add(graha)
    assert by_house[5] == {Graha.SUN, Graha.MARS, Graha.MERCURY,
                           Graha.JUPITER, Graha.SATURN}
    assert NAISARGIKA_KARAKA[5]["graha"] == Graha.JUPITER
    assert len(by_house[4]) == 5


def test_only_the_third_and_seventh_houses_have_a_single_karaka():
    """Mars alone holds the 3rd and Venus alone the 7th, in both tables. Every
    other house has a choice to make, so those two are the only unambiguous
    readings in the chapter.
    """
    from collections import defaultdict

    by_house = defaultdict(set)
    for graha, entries in NAISARGIKA_KARAKATWAS.items():
        for house, _ in entries:
            by_house[house].add(graha)
    single = {h for h in range(1, 13) if len(by_house[h]) == 1}
    assert single == {3, 7}
    assert NAISARGIKA_KARAKA[3]["graha"] == Graha.MARS
    assert NAISARGIKA_KARAKA[7]["graha"] == Graha.VENUS


def test_8_4_the_table_16_rule_and_its_example():
    """"For example, Mercury and 5th house show memory and so the 5th house
    from Mercury shows memory."

    The rule for reading Table 16: a matter shared by a graha and a house is
    read at that house counted from that graha. Checkable — Mercury's 5th cell
    does say memory.
    """
    assert "5th house from Mercury shows memory" in NAISARGIKA_TABLE_16_RULE
    mercury = dict(NAISARGIKA_KARAKATWAS[Graha.MERCURY])
    assert "memory" in mercury[5]
    example = NAISARGIKA_WORKED_EXAMPLES[-1]
    assert (example["graha"], example["house"], example["table"]) == (
        Graha.MERCURY, 5, 16)


def test_8_4_table_16_is_attributed_to_the_classics():
    """"In addition, we have various other matters allotted to different
    planets **in classics**."

    Table 16's provenance is classical; Table 15 is the chapter's own
    presentation. The two do not carry the same weight when a source has to be
    ranked, so the attribution is stored rather than dropped.
    """
    assert "in classics" in TABLE_16_SOURCE_NOTE
    assert "Table 16" in TABLE_16_SOURCE_NOTE


def test_8_4_naisargika_karakas_are_for_general_phalita_jyotish():
    """"In addition, we have naisargika karakas, who are the natural
    significators of various matters. These significations are used in general
    Phalita Jyotish."""
    assert "natural significators" in NAISARGIKA_DEFINITION
    assert "Phalita Jyotish" in NAISARGIKA_USED_IN
    assert "phalita" in KARAKA_KINDS["naisargika"]["used_for"]


def test_8_4_recaps_the_other_two_kinds_before_introducing_this_one():
    """"We have seen that chara karakas are used in analyzing the influences
    of various persons on a native, from the point of view of sustenance,
    achievements and spiritual evolution. We have seen that sthira karakas are
    used in analyzing the death of relatives."

    Both recaps match what §8.1 and §8.3 already established, so the chapter
    is consistent with itself.
    """
    chara = KARAKA_KINDS["chara"]
    assert "sustenance and achievements" in chara["shows"]
    assert "spiritual progress" in chara["presiding_because"]
    assert "timing the death" in KARAKA_KINDS["sthira"]["used_for"]


def test_8_4_children_route_to_all_three_kinds():
    """§8.4's worked comparison: the 5th from Jupiter for the birth of
    children; PK for children-related troubles and achievements; the sthira
    karaka for children for timing a child's death.

    One matter, three kinds, three different readings — the clearest
    demonstration in the chapter of why §8.1 forbids mixing them.
    """
    assert {e["kind"] for e in CHOOSING_A_KARAKA} == {
        "naisargika", "chara", "sthira"}
    assert all(e["matter"] == "children" for e in CHOOSING_A_KARAKA)
    naisargika_route = next(e for e in CHOOSING_A_KARAKA if e["kind"] == "naisargika")
    assert naisargika_route["use"] == "the 5th from Jupiter"
    assert NAISARGIKA_KARAKA[5]["graha"] == Graha.JUPITER
    chara_route = next(e for e in CHOOSING_A_KARAKA if e["kind"] == "chara")
    assert "PK" in chara_route["use"]
    assert CHARA_KARAKAS[5]["symbol"] == "PK"


def test_8_4_the_sthira_route_for_children_contradicts_footnote_27():
    """§8.4 gives children to **Jupiter** as sthira karaka. Footnote 27 records
    that "some scholars give **Saturn** as the sthira karaka for children
    instead of elder siblings".

    §8.3's list gives Saturn elder siblings, so the chapter follows its own
    list and the footnote's dissent is not adopted. Both are kept.
    """
    sthira_route = next(e for e in CHOOSING_A_KARAKA if e["kind"] == "sthira")
    assert "Jupiter" in sthira_route["use"]
    saturn = next(r for r in STHIRA_KARAKAS if r["grahas"] == (Graha.SATURN,))
    assert saturn["relative"] == "elder siblings"
    assert "Saturn" in saturn["note"] or "children" in saturn["note"]


def test_elder_siblings_have_a_different_karaka_in_each_kind():
    """Jupiter is the naisargika karaka of the 11th (elder siblings); Saturn is
    the sthira karaka of elder siblings. Same matter, two kinds, two grahas.

    A live instance of §8.1's warning: whoever mixes the kinds here reads the
    wrong planet, and neither table is wrong.
    """
    assert NAISARGIKA_KARAKA[11]["graha"] == Graha.JUPITER
    assert NAISARGIKA_KARAKA[11]["signifies"] == "Elder siblings"
    jupiter = dict(NAISARGIKA_KARAKATWAS[Graha.JUPITER])
    assert "elder brother" in jupiter[11]
    saturn = next(r for r in STHIRA_KARAKAS if r["grahas"] == (Graha.SATURN,))
    assert saturn["relative"] == "elder siblings"


# --------------------------------------------------------------------------
# Footnotes 26, 27 and 28
# --------------------------------------------------------------------------


def test_footnote_26_names_the_chapter_that_settles_the_strength_comparison():
    """"For methods to compare the strengths of planets, one may refer to the
    chapter "Strength of Planets and Rasis"."

    Which is why §8.3's father and mother entries cannot be resolved here.
    """
    assert STRENGTH_COMPARISON_CHAPTER == "Strength of Planets and Rasis"
    assert all(r["rule"] == "stronger" and r["note"]
               for r in STHIRA_KARAKAS if len(r["grahas"]) == 2)


def test_footnote_26_puts_the_two_luminaries_on_opposite_halves_of_the_day():
    """"Sun should be taken as the fixed significator of father for *daytime*
    births and Venus for *nighttime* births. Similarly, Moon is taken as the
    fixed significator of mother for *nighttime* births and Mars for
    *daytime* births."

    Note the crossing: the **Sun** takes daytime, the **Moon** takes
    nighttime, and the non-luminary of each pair takes the other half. Easy to
    store backwards, so both halves are checked in both directions.
    """
    father = next(r for r in STHIRA_KARAKAS if r["relative"] == "father")
    mother = next(r for r in STHIRA_KARAKAS if r["relative"] == "mother")
    assert "Sun for daytime" in father["note"]
    assert "Venus for nighttime" in father["note"]
    assert "Moon for nighttime" in mother["note"]
    assert "Mars for daytime" in mother["note"]


def test_footnote_26_is_a_dissent_and_is_not_the_engines_rule():
    """"Some people opine" — the day/night split is other people's view. The
    chapter's own rule is the stronger of the two, so the engine keeps
    "stronger" and stores the alternative as a note.
    """
    for row in STHIRA_KARAKAS:
        if len(row["grahas"]) == 2:
            assert row["rule"] == "stronger"
            assert "some take" in row["note"]


def test_footnote_27_and_28_are_both_recorded_as_dissent_not_adopted():
    """27: Saturn for children instead of elder siblings. 28: Jupiter as the
    spouse karaka in male charts also. Neither changes what the engine
    returns.
    """
    saturn = next(r for r in STHIRA_KARAKAS if r["grahas"] == (Graha.SATURN,))
    assert saturn["relative"] == "elder siblings"
    assert "Some scholars" in saturn["note"] or "some scholars" in saturn["note"]
    assert "male charts also" in STHIRA_KARAKA_OF_SPOUSE_NOTE
    assert STHIRA_KARAKA_OF_SPOUSE["male"] == Graha.VENUS


def test_all_three_footnote_dissents_are_attributed_the_same_way():
    """26 says "some people opine", 27 and 28 say "some scholars". All three
    are other people's views, and none is adopted — so the engine has exactly
    three recorded dissents in this chapter and returns none of them.
    """
    dissents = [r["note"] for r in STHIRA_KARAKAS if r["note"]]
    assert len(dissents) == 3
    assert STHIRA_KARAKA_OF_SPOUSE_NOTE


def test_8_4_the_naisargika_endpoint_publishes_both_tables_whole(client):
    body = client.get("/v1/karaka/naisargika").json()
    assert len(body["primary"]) == 12
    assert len(body["by_graha"]) == 9
    assert "Phalita Jyotish" in body["used_in"]
    assert "in classics" in body["table_16_source"]
    assert "memory" in body["table_16_rule"]
    assert [e["shows"] for e in body["worked_examples"]] == [
        "mother", "sons", "memory"]
    cells = sum(len(row["significations"]) for row in body["by_graha"])
    assert cells == sum(len(v) for v in TABLE_16.values()) == 34
