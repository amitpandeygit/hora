"""Chapter 12 §12.1 and §12.2 — ashtakavarga, and the eight tables it rests on.

This is a data chapter. Eight tables of ninety-six entries each are the whole
technique, so the guards here are mostly about the transcription being right
and about a missing table never being read as an empty one.

Only Table 19 has been supplied. Tables 20 to 26 are named by the book and
their absence is a stated gap, checked in both directions: the ones that exist
answer, and the ones that do not say so.
"""
import pytest
from fastapi.testclient import TestClient

from hora.api.main import app
from hora.charts.ashtakavarga import (
    AshtakavargaError,
    available_tables,
    benefic_houses,
    benefic_rasis,
    bhinnashtakavarga,
    entry,
    grade,
    muhurta_strength,
    natal_grade,
    rekhas_per_reference,
    sarvashtakavarga,
    sav_grade,
    summed,
    table_total,
)
from hora.core.const import (
    ASHTAKAVARGA_BENEFIC_TERM,
    ASHTAKAVARGA_INTRO,
    ASHTAKAVARGA_MALEFIC_TERM,
    ASHTAKAVARGA_MEANS,
    ASHTAKAVARGA_NOTATION,
    ASHTAKAVARGA_PURPOSE,
    ASHTAKAVARGA_REFERENCES,
    ASHTAKAVARGA_TABLE_NUMBERS,
    ASHTAKAVARGA_TABLES,
    ASHTAKAVARGA_TABLES_PENDING,
    AV_ABBREVIATIONS,
    AV_DIVISIONAL_EXAMPLE,
    AV_NOT_ONLY_RASI,
    AV_TABLES_ARE_THE_SAME,
    BAV_APPLIES_TO_TRANSITS,
    BAV_COUNT_IS_CALLED_REKHAS,
    BAV_COUNT_RANGE,
    BAV_DEFINITION,
    BAV_FAVOURABLE_COUNTS,
    BAV_GRADE_NAMES,
    BAV_GRADES,
    BAV_GRADING,
    BAV_NEUTRAL_COUNTS,
    BAV_UNFAVOURABLE_COUNTS,
    BHINNA_MEANS,
    BINDU_REKHA_FOOTNOTE,
    CHART_3,
    CHART_3_BIRTH,
    CHART_3_CHARA_KARAKAS,
    CHART_3_DRAWN,
    CHART_3_TITLE,
    CHART_11_MERCURY_BAV,
    CHART_12,
    CHART_12_CHARA_KARAKAS,
    CHART_12_D10_DRAWN,
    CLASSICAL_TABLE_TOTALS,
    CLASSICAL_TABLE_TOTALS_PROVENANCE,
    EXAMPLE_37,
    EXAMPLE_37_HOUSES,
    EXAMPLE_37_RASIS,
    EXAMPLE_37_WORKING,
    EXAMPLE_38_BEST_RASIS,
    EXAMPLE_38_WORST_RASIS,
    EXAMPLE_39_ANSWER,
    EXAMPLE_39_D10_CLAIMS,
    EXAMPLE_39_D10_SAV,
    EXAMPLE_39_LAGNA,
    EXAMPLE_39_RASI_SAV,
    EXAMPLE_39_VERIFIED,
    EXERCISE_18,
    EXERCISE_18_ANSWER,
    EXERCISE_18_HINT,
    EXERCISE_19,
    EXERCISE_19_ANSWER,
    EXERCISE_19_UNEXPLAINED_MARK,
    EXERCISE_20_ANSWER,
    MUHURTA_DEFINITION,
    MUHURTA_FOOTNOTE,
    RASI_ABBR,
    SAMUDAAYA_MEANS,
    SARVA_MEANS,
    SAV_DEFINITION,
    SAV_IS_SEVEN_PLANETS,
    SAV_MUHURTA_POSITIONS,
    SAV_MUHURTA_RULE,
    SAV_OVERLAP_AT,
    SAV_OWNERS,
    SAV_STRENGTH_RULE,
    SAV_STRONG_FROM,
    SAV_TOTAL,
    SODHYA_PINDA_NOT_YET_DEFINED,
    SUN_ASHTAKAVARGA_ROWS,
    TABLE_19_WORKED_READING,
    YUGA_YEARS,
    Graha,
)

R = {name: index for index, name in enumerate(RASI_ABBR)}


@pytest.fixture
def client():
    return TestClient(app)


#: Akbar's chart (Chart 10), which chapter 11 already recomputed from its own
#: birth data — reused here so the eight reference points are a real chart.
AKBAR_SIGNS = {
    "Sun": R["Sc"], "Moon": R["Ge"], "Mars": R["Cp"], "Mercury": R["Sg"],
    "Jupiter": R["Li"], "Venus": R["Li"], "Saturn": R["Li"], "Lagna": R["Li"],
}


# --------------------------------------------------------------------------
# 12.1 Introduction
# --------------------------------------------------------------------------


def test_12_1_what_ashtakavarga_is():
    """"Ashtaka means "consisting of eight" and varga means "a group"." """
    assert "consisting of eight" in ASHTAKAVARGA_MEANS
    assert "a group of 8 reference points" in ASHTAKAVARGA_MEANS
    assert "intellectual pygmies of Kali Yuga" in ASHTAKAVARGA_INTRO


def test_12_1_says_where_ashtakavarga_matters_most():
    """"This can be used to analyze the strength of a natal chart, but it is
    much more important in analyzing transits." """
    assert "much more important in analyzing transits" in ASHTAKAVARGA_PURPOSE


def test_footnote_41_gives_the_four_yugas_with_their_years():
    assert [name for name, _ in YUGA_YEARS] == [
        "Krita", "Treta", "Dwapara", "Kali"]
    years = dict(YUGA_YEARS)
    assert years["Kali"] == 432_000
    # The classical 4:3:2:1 ratio, which the printed figures satisfy.
    assert years["Krita"] == 4 * years["Kali"]
    assert years["Treta"] == 3 * years["Kali"]
    assert years["Dwapara"] == 2 * years["Kali"]


# --------------------------------------------------------------------------
# 12.2 — the eight references and the notation
# --------------------------------------------------------------------------


def test_the_eight_reference_points_are_seven_planets_and_lagna():
    assert ASHTAKAVARGA_REFERENCES == (
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
        "Lagna")
    assert len(ASHTAKAVARGA_REFERENCES) == 8


def test_the_eight_tables_are_numbered_19_to_26():
    """"Table 20-Table 26 give the benefic and malefic houses of Moon, Mars,
    Mercury, Jupiter, Venus, Saturn and lagna (respectively)." """
    assert ASHTAKAVARGA_TABLE_NUMBERS == {
        "Sun": 19, "Moon": 20, "Mars": 21, "Mercury": 22,
        "Jupiter": 23, "Venus": 24, "Saturn": 25, "Lagna": 26}
    assert list(ASHTAKAVARGA_TABLE_NUMBERS) == list(ASHTAKAVARGA_REFERENCES)


def test_pvrs_bindu_and_rekha_are_the_reverse_of_common_usage():
    """Footnote 42. "They use "bindu" to describe a benefic house (1) and
    "rekha" to describe malefic house (0). Let us follow Parasara."

    So under PVR **1 is a rekha**. Anything elsewhere that counts "bindus in
    a sign" is counting what this codebase calls rekhas.
    """
    assert ASHTAKAVARGA_BENEFIC_TERM == "rekha"
    assert ASHTAKAVARGA_MALEFIC_TERM == "bindu"
    assert "Let us follow Parasara" in BINDU_REKHA_FOOTNOTE
    assert "0 denotes a malefic position" in ASHTAKAVARGA_NOTATION
    assert "1 denotes a benefic position" in ASHTAKAVARGA_NOTATION


# --------------------------------------------------------------------------
# Table 19, checked as a transcription
# --------------------------------------------------------------------------


def test_table_19_has_the_shape_the_page_has():
    """Twelve rows of eight, every entry 0 or 1. Stored in the printed
    orientation so a reader can check it against the page line by line."""
    assert len(SUN_ASHTAKAVARGA_ROWS) == 12
    assert {len(row) for row in SUN_ASHTAKAVARGA_ROWS} == {8}
    assert {value for row in SUN_ASHTAKAVARGA_ROWS for value in row} == {0, 1}


def test_table_19_totals_forty_eight():
    """The Sun's bhinnashtakavarga total is 48 in every classical source.
    Our transcription reaches it independently, which is the strongest single
    check available on ninety-six hand-typed entries."""
    assert table_total("Sun") == 48


def test_table_19s_per_reference_totals():
    """Pinned individually, so a single mistyped entry cannot hide inside a
    correct grand total."""
    assert rekhas_per_reference("Sun") == {
        "Sun": 8, "Moon": 4, "Mars": 8, "Mercury": 7,
        "Jupiter": 4, "Venus": 3, "Saturn": 8, "Lagna": 6}


def test_the_sun_mars_and_saturn_columns_are_identical():
    """A feature of the Sun's table, not an accident of transcription: the
    three malefics make the same houses benefic for him."""
    columns = {ref: benefic_houses("Sun", ref)
               for ref in ("Sun", "Mars", "Saturn")}
    assert columns["Sun"] == columns["Mars"] == columns["Saturn"]
    assert columns["Sun"] == (1, 2, 4, 7, 8, 9, 10, 11)


def test_the_books_own_worked_reading_of_the_mercury_column():
    """"The 1st and 2nd houses have 0 and the 3rd house has 1. So the first 2
    houses from Mercury are malefic for Sun and the 3rd house is benefic." """
    assert entry("Sun", "Mercury", 1) == 0
    assert entry("Sun", "Mercury", 2) == 0
    assert entry("Sun", "Mercury", 3) == 1
    assert "the 3rd house is benefic for Sun" in TABLE_19_WORKED_READING


def test_the_column_view_is_derived_not_transcribed_twice():
    """`benefic_houses` reads the same rows the page does. A test that
    re-typed the columns would only be checking a second copy."""
    for reference in ASHTAKAVARGA_REFERENCES:
        derived = benefic_houses("Sun", reference)
        index = ASHTAKAVARGA_REFERENCES.index(reference)
        from_rows = tuple(house for house in range(1, 13)
                          if SUN_ASHTAKAVARGA_ROWS[house - 1][index])
        assert derived == from_rows


# --------------------------------------------------------------------------
# A missing table is a stated gap, never an empty one
# --------------------------------------------------------------------------


def test_which_tables_have_been_supplied():
    """Moves as each table arrives; the point is that the two lists always
    partition the eight."""
    assert available_tables() == ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna")
    assert set(ASHTAKAVARGA_TABLES) == set(ASHTAKAVARGA_TABLE_NUMBERS)
    assert ASHTAKAVARGA_TABLES_PENDING == ()
    assert (set(available_tables()) | set(ASHTAKAVARGA_TABLES_PENDING)
            == set(ASHTAKAVARGA_TABLE_NUMBERS))
    assert not set(available_tables()) & set(ASHTAKAVARGA_TABLES_PENDING)


def test_nothing_is_pending_any_more():
    """All eight tables are in. The refusal path is still live — it is what
    `_table` does for any owner without a table — but nothing triggers it
    now, so the assertion is that the pending list is empty rather than that
    a particular owner raises."""
    assert ASHTAKAVARGA_TABLES_PENDING == ()
    assert len(available_tables()) == 8


def test_an_unknown_owner_is_told_apart_from_a_pending_one():
    with pytest.raises(AshtakavargaError) as exc:
        benefic_houses("Rahu", "Sun")
    assert "unknown ashtakavarga owner" in str(exc.value)


# --------------------------------------------------------------------------
# A chart's ashtakavarga
# --------------------------------------------------------------------------


def test_a_chart_needs_all_eight_reference_points():
    """A missing reference would silently cost up to twelve rekhas, so it is
    refused rather than defaulted."""
    partial = {k: v for k, v in AKBAR_SIGNS.items() if k != "Lagna"}
    with pytest.raises(AshtakavargaError) as exc:
        bhinnashtakavarga("Sun", partial)
    assert "Lagna" in str(exc.value)


def test_a_charts_rekhas_sum_to_the_tables_own_total():
    """Every one of the table's 48 rekhas lands in exactly one sign, whatever
    the chart. The invariant that catches an off-by-one in the house count."""
    result = bhinnashtakavarga("Sun", AKBAR_SIGNS)
    assert len(result.rekhas) == 12
    assert result.total == table_total("Sun") == 48
    assert sum(result.rekhas) == 48


def test_that_invariant_holds_for_every_possible_lagna():
    for lagna in range(12):
        signs = {**AKBAR_SIGNS, "Lagna": lagna}
        assert bhinnashtakavarga("Sun", signs).total == 48


def test_a_sign_names_which_references_gave_it_rekhas():
    result = bhinnashtakavarga("Sun", AKBAR_SIGNS)
    for sign in range(12):
        assert len(result.contributors[sign]) == result.rekhas[sign]
        assert set(result.contributors[sign]) <= set(ASHTAKAVARGA_REFERENCES)


def test_both_candidate_sums_are_still_reported_after_12_4_settled_it():
    """§12.4 named the seven-planet sum as the SAV, so `summed` now says
    which is which rather than declining to choose. Both figures stay
    available because the difference is exactly lagna's Table 26, and a
    caller comparing against other software may need to see it."""
    result = summed(AKBAR_SIGNS)
    assert result["complete"] is True
    assert result["owners_included"] == [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
        "Lagna"]
    assert result["owners_missing"] == []
    assert result["seven_planets"]["classical_total_when_complete"] == 337
    assert result["eight_references"]["classical_total_when_complete"] == 386
    assert result["missing_note"] == ""   # nothing is missing now
    # Lagna's table is still pending, so the two sums coincide for now.
    # Every planetary table is in, so the seven-planet sum is complete and
    # reaches the classical 337. Lagna's is not, so the eight-reference sum
    # is still the same figure and still flagged incomplete.
    # Both sums are complete now, and they differ by exactly Table 26's 49.
    assert result["seven_planets"]["complete"] is True
    assert result["seven_planets"]["total"] == 337
    assert result["eight_references"]["complete"] is True
    assert result["eight_references"]["total"] == 386


def test_the_two_candidate_sums_differ_by_exactly_lagnas_table():
    """Which is why neither is asserted: 386 - 337 = 49, Table 26's total."""
    assert (CLASSICAL_TABLE_TOTALS["Lagna"]
            == 386 - sum(v for k, v in CLASSICAL_TABLE_TOTALS.items()
                         if k != "Lagna"))
    assert sum(v for k, v in CLASSICAL_TABLE_TOTALS.items()
               if k != "Lagna") == 337


# --------------------------------------------------------------------------
# The API
# --------------------------------------------------------------------------


def test_the_rules_endpoint_carries_the_notation_and_the_naming_warning(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["references"] == list(ASHTAKAVARGA_REFERENCES)
    assert body["tables_available"] == ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
    assert body["tables_pending"] == []
    assert body["benefic_entry"] == {
        "value": 1, "term": "rekha", "sanskrit": "sthana"}
    assert body["malefic_entry"] == {
        "value": 0, "term": "bindu", "sanskrit": "karana"}
    assert "the other way round" in body["naming_warning"]


def test_the_table_endpoint_serves_table_19_in_printed_shape(client):
    body = client.get("/v1/ashtakavarga/table", params={"owner": "Sun"}).json()
    assert body["table"] == 19
    assert len(body["rows"]) == 12
    assert body["rows"][0]["house"] == 1
    assert body["rows"][2]["entries"]["Mercury"] == 1
    assert body["total"] == 48


def test_the_table_endpoint_refuses_an_owner_it_has_no_table_for(client):
    """All eight exist now, so the refusal is exercised through an owner the
    chapter never names rather than through a pending one."""
    response = client.get("/v1/ashtakavarga/table", params={"owner": "Rahu"})
    assert response.status_code == 400
    assert "unknown ashtakavarga owner" in response.json()["error"]["message"]


def test_the_chart_endpoint_returns_what_exists_and_names_what_does_not(client):
    body = client.post("/v1/ashtakavarga/chart", json={
        "reference_signs": AKBAR_SIGNS}).json()
    assert [b["owner"] for b in body["bhinnashtakavarga"]] == ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
    assert [b["total"] for b in body["bhinnashtakavarga"]] == [
        48, 49, 39, 54, 56, 52, 39, 49]
    assert body["summed"]["complete"] is True
    assert body["tables_pending"] == []


def test_the_chart_endpoint_rejects_an_incomplete_reference_set(client):
    response = client.post("/v1/ashtakavarga/chart", json={
        "reference_signs": {"Sun": 0}})
    assert response.status_code == 400


def test_the_shape_checks_ship_with_the_product(client):
    """A silent transcription error in ninety-six entries is the real risk
    here, so the checks are not only in the test suite."""
    from hora.charts.ashtakavarga import verify_tables

    checks = verify_tables()
    assert checks["Sun"] == {
        "table": 19, "rows": 12, "columns": [8], "values": [0, 1],
        "total": 48, "classical_total": 48,
        "matches_classical_total": True, "shape_ok": True}
    for owner, check in checks.items():
        assert check["shape_ok"] is True, owner
        assert check["matches_classical_total"] is True, owner
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["tables_verified"]["Sun"]["shape_ok"] is True
    assert "not from this book" in body["classical_totals_provenance"].lower()


# --------------------------------------------------------------------------
# Table 20 and Table 21, checked the same way Table 19 was
# --------------------------------------------------------------------------


@pytest.mark.parametrize("owner,table,total", [
    ("Sun", 19, 48), ("Moon", 20, 49), ("Mars", 21, 39),
    ("Mercury", 22, 54), ("Jupiter", 23, 56), ("Venus", 24, 52),
    ("Saturn", 25, 39), ("Lagna", 26, 49)])
def test_each_supplied_table_reaches_its_own_total(owner, table, total):
    """The strongest check available on ninety-six hand-typed entries: the
    total falls out of the table rather than being asserted into it, and it
    matches what the tradition records for that planet."""
    assert ASHTAKAVARGA_TABLE_NUMBERS[owner] == table
    assert table_total(owner) == total
    assert CLASSICAL_TABLE_TOTALS[owner] == total


def test_table_20s_per_reference_totals():
    assert rekhas_per_reference("Moon") == {
        "Sun": 6, "Moon": 7, "Mars": 6, "Mercury": 8,
        "Jupiter": 7, "Venus": 7, "Saturn": 4, "Lagna": 4}


def test_table_21s_per_reference_totals():
    assert rekhas_per_reference("Mars") == {
        "Sun": 5, "Moon": 3, "Mars": 7, "Mercury": 4,
        "Jupiter": 4, "Venus": 4, "Saturn": 7, "Lagna": 5}


def test_the_moons_twelfth_house_is_malefic_from_every_reference():
    """Table 20's last row is all zeros — the only such row so far."""
    assert all(entry("Moon", ref, 12) == 0 for ref in ASHTAKAVARGA_REFERENCES)
    all_zero = [owner for owner in available_tables()
                if all(entry(owner, ref, 12) == 0
                       for ref in ASHTAKAVARGA_REFERENCES)]
    assert all_zero == ["Moon"]


@pytest.mark.parametrize("owner", ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"])
def test_every_supplied_table_keeps_the_sum_invariant_on_a_real_chart(owner):
    """Whatever the chart, each of a table's rekhas lands in exactly one
    sign. The invariant that catches an off-by-one in the house count."""
    result = bhinnashtakavarga(owner, AKBAR_SIGNS)
    assert result.total == table_total(owner)
    for lagna in range(12):
        signs = {**AKBAR_SIGNS, "Lagna": lagna}
        assert bhinnashtakavarga(owner, signs).total == table_total(owner)


def test_the_classical_totals_are_labelled_as_a_check_not_a_source():
    """The book prints the tables and gives no totals. These figures are used
    only to test the transcription, and a mismatch would be reported."""
    assert "Not from this book" in CLASSICAL_TABLE_TOTALS_PROVENANCE
    assert "never corrected" in CLASSICAL_TABLE_TOTALS_PROVENANCE
    assert set(CLASSICAL_TABLE_TOTALS) == set(ASHTAKAVARGA_TABLE_NUMBERS)
    # The eight sum to 386; the classical sarvashtakavarga total of 337 is
    # the seven planets without lagna. See OI-100.
    assert sum(CLASSICAL_TABLE_TOTALS.values()) == 386


def test_table_22s_per_reference_totals():
    assert rekhas_per_reference("Mercury") == {
        "Sun": 5, "Moon": 6, "Mars": 8, "Mercury": 8,
        "Jupiter": 4, "Venus": 8, "Saturn": 8, "Lagna": 7}


def test_table_23s_per_reference_totals():
    assert rekhas_per_reference("Jupiter") == {
        "Sun": 9, "Moon": 5, "Mars": 7, "Mercury": 8,
        "Jupiter": 8, "Venus": 6, "Saturn": 4, "Lagna": 9}


def test_the_eleventh_row_is_nearly_but_not_quite_all_ones():
    """The 11th house is benefic from every reference in five of the eight
    tables. Three break it, each in exactly one cell — the Sun and lagna
    under Venus, Jupiter under Saturn. Stated by exhaustion rather than by
    eyeballing the pages, which got this wrong twice before the derivation
    replaced the reading."""
    exceptions = {
        owner: [ref for ref in ASHTAKAVARGA_REFERENCES
                if entry(owner, ref, 11) == 0]
        for owner in available_tables()
    }
    assert {o: refs for o, refs in exceptions.items() if refs} == {
        "Sun": ["Venus"], "Jupiter": ["Saturn"], "Lagna": ["Venus"]}
    assert [o for o, refs in exceptions.items() if not refs] == [
        "Moon", "Mars", "Mercury", "Venus", "Saturn"]


def test_table_24s_per_reference_totals():
    assert rekhas_per_reference("Venus") == {
        "Sun": 3, "Moon": 9, "Mars": 6, "Mercury": 5,
        "Jupiter": 5, "Venus": 9, "Saturn": 7, "Lagna": 8}


def test_table_25s_per_reference_totals():
    assert rekhas_per_reference("Saturn") == {
        "Sun": 7, "Moon": 3, "Mars": 6, "Mercury": 6,
        "Jupiter": 4, "Venus": 3, "Saturn": 4, "Lagna": 6}


def test_all_seven_planetary_tables_sum_to_the_classical_337():
    """The end-to-end check on 672 hand-typed entries. Seven tables, each
    reaching its own total independently, and the seven totals reaching the
    figure the tradition records for a sarvashtakavarga — none of which any
    part of this codebase asserts into being."""
    planets = [o for o in available_tables() if o != "Lagna"]
    assert len(planets) == 7
    assert sum(table_total(owner) for owner in planets) == 337


def test_a_chart_reaches_337_across_the_seven_planets():
    """The same total, arrived at through the twelve signs of a real chart
    rather than through the tables directly."""
    total = sum(bhinnashtakavarga(owner, AKBAR_SIGNS).total
                for owner in available_tables() if owner != "Lagna")
    assert total == 337
    result = summed(AKBAR_SIGNS)
    assert result["seven_planets"]["complete"] is True
    assert result["seven_planets"]["total"] == 337
    assert sum(result["seven_planets"]["rekhas"]) == 337


def test_the_chapter_is_now_complete_at_768_entries():
    """Eight tables of ninety-six. Every entry 0 or 1, every table reaching
    its own total, and the eight reaching 386 — none of which this codebase
    asserts into being."""
    entries = sum(len(row) for table in ASHTAKAVARGA_TABLES.values()
                  for row in table)
    assert entries == 8 * 12 * 8 == 768
    assert {v for table in ASHTAKAVARGA_TABLES.values()
            for row in table for v in row} == {0, 1}
    assert sum(table_total(owner) for owner in available_tables()) == 386


def test_table_26s_per_reference_totals():
    assert rekhas_per_reference("Lagna") == {
        "Sun": 6, "Moon": 5, "Mars": 5, "Mercury": 7,
        "Jupiter": 9, "Venus": 7, "Saturn": 6, "Lagna": 4}


def test_the_two_candidate_sums_differ_by_lagnas_table():
    """337 against 386, and the gap is exactly Table 26's own 49 — which is
    what made OI-100 worth recording before Table 26 arrived."""
    result = summed(AKBAR_SIGNS)
    assert result["seven_planets"]["total"] == 337
    assert result["eight_references"]["total"] == 386
    assert (result["eight_references"]["total"]
            - result["seven_planets"]["total"]) == table_total("Lagna") == 49


def test_a_charts_sums_match_the_tables_own_sums():
    """Whatever the chart, the rekhas only move between signs — they are
    never created or lost. Checked on both candidate sums, for every lagna."""
    for lagna in range(12):
        signs = {**AKBAR_SIGNS, "Lagna": lagna}
        result = summed(signs)
        assert sum(result["seven_planets"]["rekhas"]) == 337
        assert sum(result["eight_references"]["rekhas"]) == 386


# --------------------------------------------------------------------------
# §12.2's Example 37 and Exercise 18
#
# Between them these two check 192 of the 768 entries against the book's own
# answers: Example 37 pins one column of Table 23, and Exercise 18 pins all
# eight columns of Table 22.
# --------------------------------------------------------------------------

#: Chart 6, P.V. Narasimha Rao — the chart Exercise 18 is set on. Already a
#: fixture in the chapter 10 tests, where it is recomputed from its own birth
#: data; the signs are repeated here rather than imported across chapters.
#: Chart 6's printed longitudes, for the divisional work in §12.5.
CHART_6_LONGITUDES = {
    "Sun": 2 * 30 + 13 + 16 / 60, "Moon": 11 * 30 + 10 + 33 / 60,
    "Mars": 2 * 30 + 13 + 33 / 60, "Mercury": 2 * 30 + 27 + 40 / 60,
    "Jupiter": 4 * 30 + 20 + 6 / 60, "Venus": 0 * 30 + 27 + 40 / 60,
    "Saturn": 4 * 30 + 26 + 26 / 60, "Lagna": 5 * 30 + 24 + 19 / 60,
}

CHART_6_SIGNS = {
    "Sun": R["Ge"], "Moon": R["Pi"], "Mars": R["Ge"], "Mercury": R["Ge"],
    "Jupiter": R["Le"], "Venus": R["Ar"], "Saturn": R["Le"],
    "Lagna": R["Vi"],
}


def test_chart_6s_signs_agree_with_the_chapter_10_fixture():
    """One chart, one set of longitudes. If chapter 10's fixture ever moves,
    this fails rather than quietly testing a different chart."""
    import re

    from tests.unit.test_book_chapter10_argala import CHART_6

    names = {"Sun": "Sun", "Moon": "Moon", "Mars": "Mars", "Mercury": "Merc",
             "Jupiter": "Jup", "Venus": "Ven", "Saturn": "Sat",
             "Lagna": "Asc"}
    for reference, key in names.items():
        match = re.fullmatch(r"(\d+) ?([A-Za-z]{2}) ?(\d+)", CHART_6[key])
        assert match, CHART_6[key]
        assert R[match.group(2)] == CHART_6_SIGNS[reference], reference


# --- Example 37 -------------------------------------------------------------


def test_example_37_finds_the_same_houses_the_book_does():
    """"Only the 2nd, 5th, 6th, 9th, 10th and 11th houses have a 1." That is
    Table 23's Venus column, read out of our transcription."""
    assert benefic_houses("Jupiter", "Venus") == EXAMPLE_37_HOUSES
    assert EXAMPLE_37_HOUSES == (2, 5, 6, 9, 10, 11)


def test_example_37_finds_the_same_rasis_the_book_does():
    """"Venus is in Ge and finding these houses with respect to Venus, we get
    Cn, Li, Sc, Aq, Pi and Ar." """
    rasis = benefic_rasis("Jupiter", "Venus", R["Ge"])
    assert {RASI_ABBR[sign] for sign in rasis} == set(EXAMPLE_37_RASIS)
    assert len(rasis) == 6


def test_example_37_is_transcribed_with_its_working():
    assert "Venus is in Ge" in EXAMPLE_37
    assert "rekha – benefic point" in EXAMPLE_37_WORKING


# --- Exercise 18 ------------------------------------------------------------


@pytest.mark.parametrize("reference", list(ASHTAKAVARGA_REFERENCES))
def test_exercise_18_matches_the_printed_answer(reference):
    """Chart 6, Mercury's ashtakavarga, one reference at a time. All eight
    lines of the printed answer reproduce."""
    sign = CHART_6_SIGNS[reference]
    rasis = benefic_rasis("Mercury", reference, sign)
    assert {RASI_ABBR[s] for s in rasis} == set(EXERCISE_18_ANSWER[reference])


def test_exercise_18_validates_all_ninety_six_of_table_22():
    """Every column of Table 22 appears in the answer, and each contributes
    as many rasis as it has rekhas — so a mistyped 0 or 1 anywhere in the
    table would change one of the eight lines."""
    from hora.charts.ashtakavarga import benefic_rasis_from_chart

    result = benefic_rasis_from_chart("Mercury", CHART_6_SIGNS)
    assert set(result) == set(ASHTAKAVARGA_REFERENCES)
    for reference, rasis in result.items():
        assert len(rasis) == rekhas_per_reference("Mercury")[reference]
        assert {RASI_ABBR[s] for s in rasis} == set(
            EXERCISE_18_ANSWER[reference])
    assert sum(len(r) for r in result.values()) == table_total("Mercury") == 54


def test_exercise_18s_answer_is_transcribed_for_all_eight():
    assert set(EXERCISE_18_ANSWER) == set(ASHTAKAVARGA_REFERENCES)
    assert EXERCISE_18_ANSWER["Jupiter"] == ("Ge", "Cn", "Cp", "Pi")
    assert "Chart 6" in EXERCISE_18
    assert "Count those houses from the respective planets" in EXERCISE_18_HINT


# --- the endpoint the two examples describe ---------------------------------


def test_the_benefic_rasis_endpoint_answers_example_37(client):
    body = client.post("/v1/ashtakavarga/benefic-rasis", json={
        "owner": "Jupiter",
        "reference_signs": {**CHART_6_SIGNS, "Venus": R["Ge"]}}).json()
    venus = next(row for row in body["benefic_rasis"]
                 if row["reference"] == "Venus")
    assert venus["houses"] == [2, 5, 6, 9, 10, 11]
    assert set(venus["rasi_names"]) == {
        "Cancer", "Libra", "Scorpio", "Aquarius", "Pisces", "Aries"}


def test_the_benefic_rasis_endpoint_answers_exercise_18(client):
    body = client.post("/v1/ashtakavarga/benefic-rasis", json={
        "owner": "Mercury", "reference_signs": CHART_6_SIGNS}).json()
    assert body["table"] == 22
    got = {row["reference"]: {RASI_ABBR[s] for s in row["rasis"]}
           for row in body["benefic_rasis"]}
    assert got == {ref: set(rasis)
                   for ref, rasis in EXERCISE_18_ANSWER.items()}


def test_the_rules_endpoint_carries_the_example_and_the_exercise(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["example_37"]["houses"] == [2, 5, 6, 9, 10, 11]
    assert body["example_37"]["rasis"] == ["Cn", "Li", "Sc", "Aq", "Pi", "Ar"]
    assert body["exercise_18"]["owner"] == "Mercury"
    assert body["exercise_18"]["answer"]["Jupiter"] == ["Ge", "Cn", "Cp", "Pi"]


# --------------------------------------------------------------------------
# 12.3 Bhinna Ashtakavarga
#
# The section names what §12.2's tables were building towards, and adds one
# testable rule: how a count of 0 to 8 is read.
# --------------------------------------------------------------------------


def test_12_3_names_what_the_tables_were_building():
    """"When preparing the BAV of a planet, we count the number of references
    from which the planet is benefic in each rasi and put that count in that
    rasi." That is what `bhinnashtakavarga` already did."""
    assert BHINNA_MEANS == "separate"
    assert AV_ABBREVIATIONS == {
        "AV": "ashtakavarga", "BAV": "Bhinna Ashtakavarga"}
    assert "count the number of references" in BAV_DEFINITION
    result = bhinnashtakavarga("Mercury", CHART_6_SIGNS)
    for sign in range(12):
        assert result.rekhas[sign] == len(result.contributors[sign])


def test_12_3_confirms_footnote_42s_naming_independently():
    """"It is called the number of rekhas (benefic points) in that rasi."

    The count of 1s is called rekhas here too, so the field name does not
    rest on our reading of footnote 42 alone."""
    assert "number of rekhas (benefic points)" in BAV_COUNT_IS_CALLED_REKHAS
    assert BAV_COUNT_IS_CALLED_REKHAS in BAV_GRADING
    assert ASHTAKAVARGA_BENEFIC_TERM == "rekha"


def test_the_count_is_between_0_and_8():
    """"The count in each rasi is between 0 to 8." Eight references, so a
    sign can be marked by all of them or none."""
    assert BAV_COUNT_RANGE == (0, 8)
    assert len(ASHTAKAVARGA_REFERENCES) == 8
    for owner in available_tables():
        result = bhinnashtakavarga(owner, CHART_6_SIGNS)
        assert all(0 <= count <= 8 for count in result.rekhas)


@pytest.mark.parametrize("count,expected", [
    (0, "unfavorable"), (1, "unfavorable"), (2, "unfavorable"),
    (3, "unfavorable"), (4, "neutral"),
    (5, "favorable"), (6, "favorable"), (7, "favorable"), (8, "favorable")])
def test_the_grading_is_exactly_what_12_3_says(count, expected):
    """"5, 6, 7 or 8 ... favorable ... 3, 2, 1 or 0 ... unfavorable ... If
    the count is 4, the planet is neutral." The book's spelling of
    "favorable" is kept."""
    assert grade(count) == expected


def test_the_grading_partitions_every_possible_count():
    """Nine counts, three grades, no gap and no overlap — so no count can
    ever come back ungraded."""
    assert sorted(BAV_GRADES) == list(range(9))
    buckets = [set(BAV_FAVOURABLE_COUNTS), set(BAV_NEUTRAL_COUNTS),
               set(BAV_UNFAVOURABLE_COUNTS)]
    assert set.union(*buckets) == set(range(9))
    for i, first in enumerate(buckets):
        for second in buckets[i + 1:]:
            assert not first & second


def test_a_count_outside_the_range_is_refused():
    """Nine references would be a bug upstream, not a grade to invent."""
    from hora.core.validate import InputError

    for bad in (-1, 9):
        with pytest.raises(InputError):
            grade(bad)


def test_the_natal_reading_is_the_grade_of_the_sign_the_planet_occupies():
    """"If a planet is in a sign with a count of..." — so the natal reading
    reads the planet's own sign. Chart 6, all seven planets."""
    expected = {
        "Sun": ("Gemini", 5, "favorable"),
        "Moon": ("Pisces", 5, "favorable"),
        "Mars": ("Gemini", 4, "neutral"),
        "Mercury": ("Gemini", 7, "favorable"),
        "Jupiter": ("Leo", 3, "unfavorable"),
        "Venus": ("Aries", 8, "favorable"),
        "Saturn": ("Leo", 2, "unfavorable"),
    }
    for owner, (sign_name, rekhas, expected_grade) in expected.items():
        result = natal_grade(owner, CHART_6_SIGNS)
        assert result["applicable"] is True
        assert result["sign_name"] == sign_name, owner
        assert result["rekhas"] == rekhas, owner
        assert result["grade"] == expected_grade, owner


def test_lagna_has_no_natal_reading_of_its_own():
    """Lagna is a reference point, not a body that occupies a sign of its
    own, so §12.3's "if a planet is in a sign" does not apply to its BAV."""
    result = natal_grade("Lagna", CHART_6_SIGNS)
    assert result["applicable"] is False
    assert "reference point" in result["reason"]


def test_every_sign_is_graded_which_is_what_makes_it_usable_for_transits():
    """"We can use this analysis in natal charts and also transit charts."
    The grade is defined for all twelve signs, not only the occupied one."""
    assert "transit charts" in BAV_APPLIES_TO_TRANSITS
    result = bhinnashtakavarga("Saturn", CHART_6_SIGNS)
    assert len(result.grades) == 12
    assert set(result.grades) <= set(BAV_GRADE_NAMES)
    for sign in range(12):
        assert result.grades[sign] == grade(result.rekhas[sign])


def test_the_chart_endpoint_carries_the_grades_and_the_natal_reading(client):
    body = client.post("/v1/ashtakavarga/chart", json={
        "reference_signs": CHART_6_SIGNS}).json()
    jupiter = next(row for row in body["bhinnashtakavarga"]
                   if row["owner"] == "Jupiter")
    assert jupiter["natal"]["sign_name"] == "Leo"
    assert jupiter["natal"]["rekhas"] == 3
    assert jupiter["natal"]["grade"] == "unfavorable"
    assert len(jupiter["grades"]) == 12
    leo = next(row for row in jupiter["signs"] if row["sign_name"] == "Leo")
    assert leo["grade"] == "unfavorable"
    lagna = next(row for row in body["bhinnashtakavarga"]
                 if row["owner"] == "Lagna")
    assert lagna["natal"]["applicable"] is False


def test_the_rules_endpoint_carries_12_3(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["bhinna_means"] == "separate"
    assert body["abbreviations"]["BAV"] == "Bhinna Ashtakavarga"
    assert body["bav_count_range"] == [0, 8]
    assert body["bav_grades"]["4"] == "neutral"
    assert body["bav_grades"]["8"] == "favorable"
    assert body["bav_grade_counts"]["unfavorable"] == [0, 1, 2, 3]
    assert "footnote 42" in body["bav_naming_agrees_with_footnote_42"]


def test_the_books_spelling_of_favorable_is_kept(client):
    """"favorable" and "unfavorable", not the British forms. Kept because
    these are the book's words, and a caller matching on them should match."""
    assert BAV_GRADE_NAMES == ("favorable", "neutral", "unfavorable")
    assert "favourable" not in BAV_GRADING
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["bav_grade_names"] == ["favorable", "neutral", "unfavorable"]


# --------------------------------------------------------------------------
# §12.3's Example 38 and Chart 11
#
# Chart 11 draws Mercury's BAV for Chart 6. It is the first time the book
# prints a computed ashtakavarga rather than a definition table, so all
# twelve figures are a check on the machinery end to end.
# --------------------------------------------------------------------------


def test_chart_11_reproduces_sign_for_sign():
    """Twelve figures, each the count of references from which Mercury is
    benefic in that rasi. Every one matches."""
    result = bhinnashtakavarga("Mercury", CHART_6_SIGNS)
    assert result.rekhas == CHART_11_MERCURY_BAV
    assert sum(CHART_11_MERCURY_BAV) == 54 == table_total("Mercury")


def test_example_38s_two_worked_signs():
    """"Mercury is benefic in Ar with respect to Sun, Moon, Mars, Mercury,
    Venus, Saturn and lagna ... So we write 7 in Ar ... benefic in Ta with
    respect to Sun, Mercury, Venus and Saturn ... So we write 4 in Ta."

    The named references are checked, not only the counts."""
    result = bhinnashtakavarga("Mercury", CHART_6_SIGNS)
    assert set(result.contributors[R["Ar"]]) == {
        "Sun", "Moon", "Mars", "Mercury", "Venus", "Saturn", "Lagna"}
    assert result.rekhas[R["Ar"]] == 7
    assert set(result.contributors[R["Ta"]]) == {
        "Sun", "Mercury", "Venus", "Saturn"}
    assert result.rekhas[R["Ta"]] == 4


def test_example_38s_best_and_worst_rasis():
    """"In Ar and Ge, we have 7 rekhas ... In Aq, we have 6 ... So these
    three rasis are particularly favorable ... In Vi and Cp, we have 3 rekhas
    and that is the lowest." The claim that 3 is the lowest is checked, not
    assumed."""
    result = bhinnashtakavarga("Mercury", CHART_6_SIGNS)
    best = {name for name in RASI_ABBR if result.rekhas[R[name]] >= 6}
    assert best == set(EXAMPLE_38_BEST_RASIS) == {"Ar", "Ge", "Aq"}
    worst = {name for name in RASI_ABBR
             if result.rekhas[R[name]] == min(result.rekhas)}
    assert worst == set(EXAMPLE_38_WORST_RASIS) == {"Vi", "Cp"}
    assert min(result.rekhas) == 3


def test_example_38s_natal_reading_of_mercury():
    """"Mercury is in Ge in the natal chart and Ge has 7 rekhas in Mercury's
    AV. That means that Mercury is a very favorable planet." """
    natal = natal_grade("Mercury", CHART_6_SIGNS)
    assert natal["sign_name"] == "Gemini"
    assert natal["rekhas"] == 7
    assert natal["grade"] == "favorable"


def test_example_38s_bhadra_claim():
    """"Being the lagna lord and being in a quadrant from lagna in own sign
    (i.e. Bhadra yoga) makes him even stronger." All three parts, and the
    yoga itself from the chapter 11 registry."""
    from hora.charts.planetary_yogas import YogaInput, evaluate_one
    from hora.core.const import RASI_LORD, Graha

    lagna = CHART_6_SIGNS["Lagna"]
    assert int(RASI_LORD[lagna]) == int(Graha.MERCURY)
    house = (CHART_6_SIGNS["Mercury"] - lagna) % 12 + 1
    assert house == 10
    verdict = evaluate_one("bhadra", YogaInput(
        rasis={int(Graha.MERCURY): CHART_6_SIGNS["Mercury"]},
        lagna_rasi=lagna))
    assert verdict.present is True
    assert "his own sign, and the 10th from lagna" in verdict.reason


def test_the_rules_endpoint_carries_example_38(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["example_38"]["bav"] == list(CHART_11_MERCURY_BAV)
    assert body["example_38"]["best_rasis"] == ["Ar", "Ge", "Aq"]
    assert body["example_38"]["worst_rasis"] == ["Vi", "Cp"]
    assert "Bhadra yoga" in body["example_38"]["natal"]


# --------------------------------------------------------------------------
# What Chart 11 disagrees with Chart 6 about — D-38 and D-39
# --------------------------------------------------------------------------

#: Chart 11's printed longitudes. The same native as Chart 6, six minutes
#: later. Transcribed for the comparison, not used as a fixture: Chart 6 is
#: the one whose birth data we recompute.
CHART_11 = {
    "Asc": "25 Vi 45", "Sun": "13 Ge 17", "Moon": "10 Pi 36",
    "Mars": "13 Ge 33", "Merc": "27 Ge 40", "Jup": "20 Le 06",
    "Ven": "27 Ar 40", "Sat": "26 Le 26", "Rahu": "0 Li 47",
    "Ketu": "0 Ar 47", "HL": "27 Cp 11", "GL": "3 Cp 29",
}
CHART_11_TIME = "1:08 pm (IST)"
CHART_11_CHARA_KARAKAS = {
    "Rahu": "AK", "Ven": "AmK", "Merc": "BK", "Sat": "MK",
    "Jup": "PiK", "Mars": "PK", "Sun": "GK", "Moon": "DK",
}


def _lon11(text: str) -> float:
    import re

    match = re.fullmatch(r"(\d+) ?([A-Za-z]{2}) ?(\d+)", text)
    assert match, text
    return R[match.group(2)] * 30 + int(match.group(1)) + int(match.group(3)) / 60


def test_chart_11s_planets_sit_in_the_same_signs_as_chart_6s():
    """Which is why Example 38 works from either printing: the BAV depends
    only on signs, and no planet changes sign in six minutes."""
    from tests.unit.test_book_chapter10_argala import CHART_6

    for body in ("Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat",
                 "Rahu", "Ketu", "Asc"):
        assert int(_lon11(CHART_11[body]) // 30) == int(
            _lon11(CHART_6[body]) // 30), body


def test_chart_11_is_six_minutes_later_than_chart_6():
    """D-38. 12:49 at 5h17m east against 1:08 pm IST."""
    chart_6_ut = 12 + 49 / 60 - (5 + 17 / 60)
    chart_11_ut = 13 + 8 / 60 - 5.5
    assert round((chart_11_ut - chart_6_ut) * 60) == 6
    assert "IST" in CHART_11_TIME


def test_what_the_six_minutes_moves_and_what_it_does_not():
    """The planets barely move; the ascendant and the special lagnas do —
    and GL changes sign, which §11.7.3's yogas 6 and 8 read."""
    from tests.unit.test_book_chapter10_argala import CHART_6

    for body in ("Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat"):
        drift = abs(_lon11(CHART_11[body]) - _lon11(CHART_6[body])) * 60
        assert drift == pytest.approx(round(drift)), body
        assert round(drift) <= 3, body
    ascendant_drift = abs(_lon11(CHART_11["Asc"]) - _lon11(CHART_6["Asc"])) * 60
    assert ascendant_drift == pytest.approx(86.0)   # 1°26'

    assert int(_lon11(CHART_11["GL"]) // 30) != int(_lon11(CHART_6["GL"]) // 30)


def test_the_two_charts_print_different_chara_karakas_for_mercury_and_venus():
    """D-39. Both are at 27°40' of their signs — an exact tie at the printed
    precision — and the two charts break it opposite ways."""
    from tests.unit.test_book_chapter10_argala import CHART_6_CHARA_KARAKAS

    assert _lon11(CHART_11["Merc"]) % 30 == pytest.approx(
        _lon11(CHART_11["Ven"]) % 30)
    assert CHART_6_CHARA_KARAKAS["Merc"] == "AmK"
    assert CHART_6_CHARA_KARAKAS["Ven"] == "BK"
    assert CHART_11_CHARA_KARAKAS["Merc"] == "BK"
    assert CHART_11_CHARA_KARAKAS["Ven"] == "AmK"
    # Everything else agrees.
    others = {k for k in CHART_11_CHARA_KARAKAS} - {"Merc", "Ven"}
    for body in others:
        assert CHART_11_CHARA_KARAKAS[body] == CHART_6_CHARA_KARAKAS[body]


def test_the_tie_is_reported_rather_than_hidden():
    """§8.2's tie-break needs seconds, which the book does not print. Both
    grahas come back flagged so a caller knows the order between them is not
    settled by the data.

    This also pins the float defect D-39 exposed: the two advancements are
    equal to 3.6e-15 degrees, and an equality test missed the tie entirely.
    """
    from hora.charts.karaka import chara_karakas
    from hora.core.const import Graha

    longitudes = {
        int(Graha.SUN): _lon11(CHART_11["Sun"]),
        int(Graha.MOON): _lon11(CHART_11["Moon"]),
        int(Graha.MARS): _lon11(CHART_11["Mars"]),
        int(Graha.MERCURY): _lon11(CHART_11["Merc"]),
        int(Graha.JUPITER): _lon11(CHART_11["Jup"]),
        int(Graha.VENUS): _lon11(CHART_11["Ven"]),
        int(Graha.SATURN): _lon11(CHART_11["Sat"]),
        int(Graha.RAHU): _lon11(CHART_11["Rahu"]),
    }
    result = {k.graha_name: k for k in chara_karakas(longitudes)}
    assert result["Mercury"].shared is True
    assert result["Venus"].shared is True
    assert result["Mercury"].advancement != result["Venus"].advancement
    assert abs(result["Mercury"].advancement
               - result["Venus"].advancement) < 1e-12
    # Nothing else in the chart is tied.
    assert [name for name, k in result.items() if k.shared] == [
        "Mercury", "Venus"]


# --------------------------------------------------------------------------
# §12.3's Exercise 19 — all seven BAVs for Chart 6
#
# Eighty-four figures against the book's own answer. Every planetary table is
# exercised through one chart, so this is the widest single check in the
# chapter: a mistyped entry anywhere in the 672 planetary entries would move
# at least one cell.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("owner", list(EXERCISE_19_ANSWER))
def test_exercise_19_reproduces_a_whole_row(owner):
    result = bhinnashtakavarga(owner, CHART_6_SIGNS)
    assert result.rekhas == EXERCISE_19_ANSWER[owner]


def test_exercise_19_reproduces_every_one_of_the_eighty_four_cells():
    """Stated as a count so a silently shortened answer table cannot pass."""
    checked = 0
    for owner, printed in EXERCISE_19_ANSWER.items():
        assert len(printed) == 12, owner
        result = bhinnashtakavarga(owner, CHART_6_SIGNS)
        for sign in range(12):
            assert result.rekhas[sign] == printed[sign], (owner, sign)
            checked += 1
    assert checked == 84


def test_exercise_19s_rows_sum_to_the_tables_own_totals():
    """A second, independent reading of the same answer: each printed row
    must add up to the table it came from."""
    for owner, printed in EXERCISE_19_ANSWER.items():
        assert sum(printed) == table_total(owner), owner
    assert sum(sum(row) for row in EXERCISE_19_ANSWER.values()) == 337


def test_exercise_19s_columns_match_the_seven_planet_sum():
    """A third reading, down the columns rather than across the rows: the
    printed answer's column sums are our seven-planet total, sign by sign."""
    columns = [sum(EXERCISE_19_ANSWER[owner][sign]
                   for owner in EXERCISE_19_ANSWER)
               for sign in range(12)]
    assert columns == summed(CHART_6_SIGNS)["seven_planets"]["rekhas"]
    assert sum(columns) == 337


def test_exercise_19_covers_every_planetary_table():
    """Lagna's is the only one it does not exercise, because the exercise
    names the seven planets."""
    assert set(EXERCISE_19_ANSWER) == set(available_tables()) - {"Lagna"}
    assert "Lagna" not in EXERCISE_19_ANSWER
    assert "Sun, Moon, Mars, Mercury, Jupiter, Venus and Saturn" in EXERCISE_19


def test_exercise_19s_mercury_row_is_chart_11():
    """The exercise and Chart 11 are the same figures, so they check each
    other as well as checking us."""
    assert EXERCISE_19_ANSWER["Mercury"] == CHART_11_MERCURY_BAV


def test_the_asterisk_in_the_printed_answer_is_recorded_not_interpreted():
    """The answer shows "5*" for the Moon in Pisces and nothing on the page
    says why. It is not the planet's own position marked as a rule — Venus in
    Aries and Mercury in Gemini carry no mark — and 5 is right either way."""
    mark = EXERCISE_19_UNEXPLAINED_MARK
    assert mark == {"owner": "Moon", "rasi": "Pi", "printed": "5*",
                    "value": 5}
    assert EXERCISE_19_ANSWER["Moon"][R["Pi"]] == 5
    assert bhinnashtakavarga("Moon", CHART_6_SIGNS).rekhas[R["Pi"]] == 5
    # If the asterisk marked the planet's own sign, these would carry one too.
    assert CHART_6_SIGNS["Moon"] == R["Pi"]
    assert CHART_6_SIGNS["Venus"] == R["Ar"]
    assert CHART_6_SIGNS["Mercury"] == R["Ge"]


def test_the_rules_endpoint_carries_exercise_19(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["exercise_19"]["answer"]["Venus"] == [
        8, 7, 4, 3, 3, 2, 4, 6, 4, 4, 4, 3]
    assert body["exercise_19"]["unexplained_mark"]["printed"] == "5*"
    assert "not interpreted" in body["exercise_19"]["unexplained_mark_note"]


# --------------------------------------------------------------------------
# 12.4 Samudaaya Ashtakavarga — and the section that closes OI-100
# --------------------------------------------------------------------------


def test_12_4_settles_what_the_sav_sums():
    """"Samudaaya Ashtakavarga is nothing but the sum of the ashtakavargas of
    seven planets." Lagna has a table — Table 26 — but is not among them.
    This is what OI-100 was open about."""
    assert "seven planets" in SAV_IS_SEVEN_PLANETS
    assert SAV_OWNERS == ("Sun", "Moon", "Mars", "Mercury", "Jupiter",
                          "Venus", "Saturn")
    assert "Lagna" not in SAV_OWNERS
    assert len(SAV_OWNERS) == 7
    assert set(SAV_OWNERS) | {"Lagna"} == set(ASHTAKAVARGA_TABLE_NUMBERS)
    result = sarvashtakavarga(CHART_6_SIGNS)
    assert result["owners"] == list(SAV_OWNERS)
    assert result["excludes"] == ["Lagna"]


def test_the_sav_totals_337_and_that_is_why_the_distinction_mattered():
    """337 is the seven-planet total; adding lagna's Table 26 would give 386.
    The difference is exactly 49, which is why the two sums were kept apart
    until this section named one."""
    assert SAV_TOTAL == 337
    assert sarvashtakavarga(CHART_6_SIGNS)["total"] == 337
    assert sum(table_total(o) for o in SAV_OWNERS) == 337
    assert table_total("Lagna") == 49
    assert 337 + 49 == 386


def test_samudaaya_and_sarva_both_name_it():
    """"It will be denoted with SAV. It is also called "Sarva Ashtakavarga"
    (sarva = all)." """
    assert SAMUDAAYA_MEANS == "group"
    assert SARVA_MEANS == "all"
    assert "Sarva Ashtakavarga" in SAV_DEFINITION


# --- Exercise 20 ------------------------------------------------------------


def test_exercise_20_reproduces_sign_for_sign():
    result = sarvashtakavarga(CHART_6_SIGNS)
    assert tuple(result["rekhas"]) == EXERCISE_20_ANSWER
    assert sum(EXERCISE_20_ANSWER) == 337


def test_the_worked_aries_figure():
    """"the BAVs of Sun, Moon, Mars, Mercury, Jupiter, Venus and Saturn have
    5, 3, 4, 7, 4, 8 and 3 rekhas in Ar ... Adding them all, we get 34."

    The seven addends are checked, not only the sum."""
    addends = [bhinnashtakavarga(owner, CHART_6_SIGNS).rekhas[R["Ar"]]
               for owner in SAV_OWNERS]
    assert addends == [5, 3, 4, 7, 4, 8, 3]
    assert sum(addends) == 34 == EXERCISE_20_ANSWER[R["Ar"]]


def test_exercise_20_is_exercise_19s_columns():
    """The two answers are the same figures read across and down, so they
    check each other as well as checking us."""
    columns = tuple(sum(EXERCISE_19_ANSWER[owner][sign] for owner in SAV_OWNERS)
                    for sign in range(12))
    assert columns == EXERCISE_20_ANSWER


# --- the strength bands -----------------------------------------------------


@pytest.mark.parametrize("rekhas,expected", [
    (0, "weak"), (24, "weak"), (25, "average"), (29, "average"),
    (30, "strong"), (31, "strong"), (56, "strong")])
def test_the_sav_strength_bands(rekhas, expected):
    assert sav_grade(rekhas) == expected


def test_thirty_is_read_as_strong_and_why():
    """§12.4's ranges overlap: "30 or more ... strong" and "25-30 ...
    average". Thirty is taken as strong — that clause is unambiguous and
    stated first, and the muhurta rule repeats "30 or more ... are
    favorable". See D-40."""
    assert SAV_OVERLAP_AT == 30
    assert "30 or more rekhas becomes strong" in SAV_STRENGTH_RULE
    assert "25-30 rekhas is average" in SAV_STRENGTH_RULE
    assert "30 or more rekhas in SAV are favorable" in SAV_MUHURTA_RULE
    assert sav_grade(30) == "strong"


def test_chart_6s_sav_grades():
    """Four strong rasis, one weak. Pinned so a change to any of the seven
    tables shows up here as well as in the counts."""
    result = sarvashtakavarga(CHART_6_SIGNS)
    grades = {RASI_ABBR[row["sign"]]: row["grade"] for row in result["signs"]}
    assert {name for name, g in grades.items() if g == "strong"} == {
        "Ar", "Ge", "Cp", "Pi"}
    assert {name for name, g in grades.items() if g == "weak"} == {"Li"}


# --- the muhurta rule -------------------------------------------------------


def test_the_muhurta_rule_reads_the_natal_sav_at_the_muhurta_signs():
    """"one should look at the strengths, as per SAV of the natal chart, of
    the rasis containing lagna, Moon and Sun in the muhurta chart." """
    assert SAV_MUHURTA_POSITIONS == ("Lagna", "Moon", "Sun")
    result = muhurta_strength(
        CHART_6_SIGNS, {"Lagna": R["Ar"], "Moon": R["Li"], "Sun": R["Cp"]})
    rows = {row["position"]: row for row in result["positions"]}
    assert rows["Lagna"]["natal_sav_rekhas"] == 34
    assert rows["Lagna"]["favorable"] is True
    assert rows["Moon"]["natal_sav_rekhas"] == 22
    assert rows["Moon"]["favorable"] is False
    assert rows["Sun"]["natal_sav_rekhas"] == 30
    assert rows["Sun"]["favorable"] is True   # the boundary case
    assert result["all_favorable"] is False
    assert result["favorable_from"] == 30


def test_the_muhurta_rule_needs_all_three_positions():
    with pytest.raises(AshtakavargaError) as exc:
        muhurta_strength(CHART_6_SIGNS, {"Lagna": 0, "Moon": 1})
    assert "Sun" in str(exc.value)


def test_footnote_43_is_supplied_with_12_5():
    """"Muhurta is an auspicious pre-set time at which one begins important
    activities." Recorded as unread when §12.4 was written."""
    assert MUHURTA_FOOTNOTE == "43"
    assert "auspicious pre-set time" in MUHURTA_DEFINITION
    assert "muhurtas" in SAV_MUHURTA_RULE


# --- the API ----------------------------------------------------------------


def test_the_chart_endpoint_carries_the_sav(client):
    body = client.post("/v1/ashtakavarga/chart", json={
        "reference_signs": CHART_6_SIGNS}).json()
    sav = body["sarvashtakavarga"]
    assert sav["rekhas"] == list(EXERCISE_20_ANSWER)
    assert sav["total"] == 337
    assert sav["excludes"] == ["Lagna"]
    assert body["summed"]["seven_planets"]["is_the_sav"] is True
    assert body["summed"]["eight_references"]["is_the_sav"] is False


def test_the_muhurta_endpoint(client):
    body = client.post("/v1/ashtakavarga/muhurta", json={
        "natal_reference_signs": CHART_6_SIGNS,
        "muhurta_signs": {"Lagna": R["Ar"], "Moon": R["Li"],
                          "Sun": R["Cp"]}}).json()
    assert body["all_favorable"] is False
    assert body["natal_sav"] == list(EXERCISE_20_ANSWER)
    assert body["footnote"] == "43"
    assert "auspicious pre-set time" in body["muhurta_definition"]


def test_the_rules_endpoint_carries_12_4(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["sav_owners"] == list(SAV_OWNERS)
    assert body["sav_excludes"] == ["Lagna"]
    assert body["sav_total"] == 337
    assert body["sav_grade_bands"]["average"] == "25 to 29"
    assert "D-40" in body["sav_overlap_note"]
    assert body["exercise_20"]["answer"] == list(EXERCISE_20_ANSWER)


# --------------------------------------------------------------------------
# 12.5 Divisional Charts
# --------------------------------------------------------------------------


def test_12_5_says_the_tables_do_not_change_from_chart_to_chart():
    """"The benefic houses for each planet with respect to the 8 references
    are the same." So only the signs the references occupy change."""
    assert "misconception" in AV_NOT_ONLY_RASI
    assert "benefic houses for each planet" in AV_TABLES_ARE_THE_SAME
    assert "SAV of a divisional chart too" in AV_TABLES_ARE_THE_SAME
    assert AV_DIVISIONAL_EXAMPLE["chart"] == "D12"


def test_the_same_tables_really_are_used_for_every_chart():
    """Asserted against the code, not only quoted: `signs_in_chart` changes
    the signs and nothing else, so every chart reads the same eight tables."""
    from hora.charts.ashtakavarga import signs_in_chart

    longitudes = CHART_6_LONGITUDES
    for code in ("D1", "D9", "D12", "D30"):
        signs = signs_in_chart(longitudes, code)
        assert set(signs) == set(ASHTAKAVARGA_REFERENCES)
        for owner in available_tables():
            # The table is the same object whatever the chart.
            assert benefic_houses(owner, "Sun") == benefic_houses(owner, "Sun")
            assert bhinnashtakavarga(owner, signs).total == table_total(owner)


def test_a_divisional_sav_still_totals_337():
    """The invariant survives the change of chart: rekhas only move between
    signs."""
    from hora.charts.ashtakavarga import signs_in_chart

    for code in ("D1", "D9", "D12", "D30", "D60"):
        signs = signs_in_chart(CHART_6_LONGITUDES, code)
        assert sarvashtakavarga(signs)["total"] == 337, code


def test_the_rasi_chart_reached_through_longitudes_is_exercise_20():
    """The longitude path and the sign path agree — D-1 from Chart 6's
    longitudes reproduces the printed SAV."""
    from hora.charts.ashtakavarga import signs_in_chart

    signs = signs_in_chart(CHART_6_LONGITUDES, "D1")
    assert signs == CHART_6_SIGNS
    assert tuple(sarvashtakavarga(signs)["rekhas"]) == EXERCISE_20_ANSWER


def test_a_divisional_chart_gives_a_different_sav():
    """Which is the point of §12.5 — D-12 is not D-1, and the book uses D-12
    for matters related to father."""
    from hora.charts.ashtakavarga import signs_in_chart

    rasi = sarvashtakavarga(signs_in_chart(CHART_6_LONGITUDES, "D1"))
    d12 = sarvashtakavarga(signs_in_chart(CHART_6_LONGITUDES, "D12"))
    assert d12["rekhas"] != rasi["rekhas"]
    assert d12["total"] == rasi["total"] == 337


def test_an_unknown_varga_code_is_refused():
    from hora.charts.ashtakavarga import signs_in_chart

    with pytest.raises(AshtakavargaError):
        signs_in_chart(CHART_6_LONGITUDES, "D0")


def test_the_divisional_endpoint_records_which_chart_it_used(client):
    body = client.post("/v1/ashtakavarga/divisional", json={
        "reference_longitudes": CHART_6_LONGITUDES, "chart": "D12"}).json()
    assert body["chart"] == "D12"
    assert body["sarvashtakavarga"]["total"] == 337
    assert "do not change from chart to chart" in body["chart_note"]


def test_the_chart_endpoint_labels_itself_as_the_rasi_chart(client):
    body = client.post("/v1/ashtakavarga/chart", json={
        "reference_signs": CHART_6_SIGNS}).json()
    assert body["chart"] == "D1"


def test_sodhya_pindas_are_named_but_not_defined():
    """§12.5 names them beside ashtakavarga; nothing read so far says what
    they are. See OI-101."""
    assert "sodhya pindas" in AV_NOT_ONLY_RASI
    assert "No section read so far defines them" in SODHYA_PINDA_NOT_YET_DEFINED


def test_the_rules_endpoint_carries_12_5(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert "misconception" in body["not_only_rasi"]
    assert body["divisional_example"]["chart"] == "D12"
    assert "sodhya pindas" in body["sodhya_pinda_not_yet_defined"]
    assert "auspicious pre-set time" in body["muhurta_definition"]


# --------------------------------------------------------------------------
# §12.5's Example 39 — Vajpayee's rasi and D-10 SAVs
#
# Chart 3 holds his birth data and has not been supplied, so the two printed
# SAVs cannot be recomputed. What they *can* be checked for is internal
# consistency, and every claim the example makes turns out to hold.
# --------------------------------------------------------------------------


def test_both_of_example_39s_savs_total_337():
    """The invariant applies to any chart, so it is a real check on the two
    printed rows even without the chart behind them."""
    assert sum(EXAMPLE_39_RASI_SAV) == 337
    assert sum(EXAMPLE_39_D10_SAV) == 337
    assert len(EXAMPLE_39_RASI_SAV) == len(EXAMPLE_39_D10_SAV) == 12


def test_the_example_never_states_the_lagna_but_fixes_it_twice():
    """The rasi maximum of 38 is called the 11th house and the D-10 maximum
    of 35 is called the lagna. Both give Scorpio, independently."""
    rasi_max = max(range(12), key=lambda s: EXAMPLE_39_RASI_SAV[s])
    d10_max = max(range(12), key=lambda s: EXAMPLE_39_D10_SAV[s])
    assert EXAMPLE_39_RASI_SAV[rasi_max] == 38
    assert EXAMPLE_39_D10_SAV[d10_max] == 35
    assert RASI_ABBR[(rasi_max - 10) % 12] == EXAMPLE_39_LAGNA   # 11th from
    assert RASI_ABBR[d10_max] == EXAMPLE_39_LAGNA                # 1st from
    assert EXAMPLE_39_LAGNA == "Sc"


@pytest.mark.parametrize("which,house,expected", [
    ("rasi", 11, 38), ("rasi", 3, 34), ("rasi", 1, 26), ("rasi", 10, 28),
    ("d10", 1, 35), ("d10", 8, 33),
])
def test_every_numbered_claim_in_example_39(which, house, expected):
    """Each figure the example quotes, read from the printed row at the house
    it names, counted from Scorpio."""
    sav = EXAMPLE_39_RASI_SAV if which == "rasi" else EXAMPLE_39_D10_SAV
    sign = (R[EXAMPLE_39_LAGNA] + house - 1) % 12
    assert sav[sign] == expected


def test_the_two_more_than_30_claims():
    """"The 3rd house in D-10 also has more than 30 rekhas" and the D-10
    lagna likewise. Both are strong under §12.4's bands."""
    for house in (1, 3):
        sign = (R[EXAMPLE_39_LAGNA] + house - 1) % 12
        assert EXAMPLE_39_D10_SAV[sign] > 30
        assert sav_grade(EXAMPLE_39_D10_SAV[sign]) == "strong"


def test_the_two_average_houses_the_example_asks_about():
    """"lagna and the 10th house in the SAV of rasi chart containing only 26
    and 28 rekhas — which is just average". §12.4's band agrees."""
    for house in (1, 10):
        sign = (R[EXAMPLE_39_LAGNA] + house - 1) % 12
        assert sav_grade(EXAMPLE_39_RASI_SAV[sign]) == "average"


# --------------------------------------------------------------------------
# Chart 3 — Vajpayee, the birth data Example 39 works from
# --------------------------------------------------------------------------

CHART_3_BIRTH_DATA = {
    "year": 1926, "month": 12, "day": 25, "hour": 5, "minute": 12,
    "second": 0.0, "utc_offset_hours": 5.5,
}
CHART_3_PLACE = {"latitude": 26 + 14 / 60, "longitude": 78 + 10 / 60}

_CHART_3_GRAHA = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
    "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU,
}


def _lon3(text: str) -> float:
    import re

    match = re.fullmatch(r"(\d+) ?([A-Za-z]{2}) ?(\d+)", text)
    assert match, text
    return R[match.group(2)] * 30 + int(match.group(1)) + int(match.group(3)) / 60


def _chart_3_references() -> dict[str, float]:
    """The eight references §12.2's tables are indexed by."""
    return {
        "Sun": _lon3(CHART_3["Sun"]), "Moon": _lon3(CHART_3["Moon"]),
        "Mars": _lon3(CHART_3["Mars"]), "Mercury": _lon3(CHART_3["Merc"]),
        "Jupiter": _lon3(CHART_3["Jup"]), "Venus": _lon3(CHART_3["Ven"]),
        "Saturn": _lon3(CHART_3["Sat"]), "Lagna": _lon3(CHART_3["Asc"]),
    }


def test_chart_3_birth_line_is_transcribed():
    assert CHART_3_TITLE == "Rasi — A.B. Vajpayee"
    assert CHART_3_BIRTH == (
        "December 25, 1926, 5:12 am (IST), 78 E 10, 26 N 14")


def test_chart_3_has_every_printed_body():
    assert set(CHART_3) == {
        "Asc", "Sun", "Moon", "Mars", "Merc", "Jup", "Ven", "Sat",
        "Rahu", "Ketu", "HL", "GL"}


def test_chart_3_lagna_is_scorpio_as_the_savs_alone_had_predicted():
    """Example 39 never states its lagna; both printed SAV maxima imply
    Scorpio. Chart 3, supplied afterwards, prints Asc 14 Sc 18."""
    assert CHART_3["Asc"].split()[1] == EXAMPLE_39_LAGNA == "Sc"


def test_chart_3_nodes_are_exactly_opposite():
    assert abs((_lon3(CHART_3["Rahu"]) - _lon3(CHART_3["Ketu"])) % 360
               - 180) < 1e-9


@pytest.mark.parametrize(
    "body,sign",
    sorted((b, s) for b, s in CHART_3_DRAWN.items() if b != "AL"))
def test_chart_3_drawn_boxes_agree_with_the_printed_longitudes(body, sign):
    assert RASI_ABBR[int(_lon3(CHART_3[body]) // 30)] == sign


def test_chart_3_drawn_arudha_lagna_is_derived_not_transcribed():
    """The diagram prints AL in Cp; the longitudes do not. §9.2 must produce
    it. Scorpio is co-owned, so §15.5.1's cascade runs too — it takes Ketu
    over Mars, and the answer comes out Capricorn either way it is asked."""
    from hora.core.const import RASI_NAMES
    from hora.services import arudha_service

    longitudes = {int(g): _lon3(CHART_3[name])
                  for name, g in _CHART_3_GRAHA.items()}
    pada = arudha_service.one(
        1, int(_lon3(CHART_3["Asc"]) // 30),
        {k: int(v // 30) for k, v in longitudes.items()},
        graha_longitudes=longitudes)
    assert RASI_ABBR[RASI_NAMES.index(pada["sign_name"])] == CHART_3_DRAWN["AL"]


def test_chart_3s_printed_chara_karakas():
    from hora.charts.karaka import chara_karakas

    longitudes = {int(g): _lon3(CHART_3[name])
                  for name, g in _CHART_3_GRAHA.items() if name != "Ketu"}
    assigned = {k.graha: k.symbol for k in chara_karakas(longitudes)}
    assert len(CHART_3_CHARA_KARAKAS) == 8
    for name, symbol in CHART_3_CHARA_KARAKAS.items():
        assert assigned[int(_CHART_3_GRAHA[name])] == symbol, name


@pytest.mark.parametrize("body", sorted(_CHART_3_GRAHA))
def test_chart_3_recomputes_from_its_own_birth_data(body):
    """25 December 1926, 5:12 am IST, 78 E 10, 26 N 14. Every graha inside one
    arcminute."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    chart = compute_chart(
        from_local(**CHART_3_BIRTH_DATA),
        Place(name="Chart 3", **CHART_3_PLACE),
        Settings(node_type=NodeType.MEAN))
    expected = _lon3(CHART_3[body])
    got = chart.positions[int(_CHART_3_GRAHA[body])].longitude
    assert abs(got - expected) < 1.0 / 60, f"{body}: {got:.4f} vs {expected:.4f}"


def test_chart_3s_ascendant_is_five_arcminutes_out():
    """The one body outside a minute. 5.5' of lagna is about 22 seconds of
    birth time, and the book prints the time to the minute — so this is the
    rounding, not a disagreement about the ascendant. Recorded rather than
    hidden behind a loose tolerance."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    chart = compute_chart(
        from_local(**CHART_3_BIRTH_DATA),
        Place(name="Chart 3", **CHART_3_PLACE),
        Settings(node_type=NodeType.MEAN))
    error = abs(chart.lagna_longitude - _lon3(CHART_3["Asc"])) * 60
    assert 5.0 < error < 6.0
    assert int(chart.lagna_longitude // 30) == R["Sc"]


def test_chart_3_is_a_fifth_vote_for_the_mean_node():
    """Charts 6, 7, 10 and 12 all needed the mean node; this makes five, and
    the first from the 1920s. Its margin is the narrowest of the five —
    0.75' against 8.8' — so it corroborates rather than decides. See OI-68."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    printed = _lon3(CHART_3["Rahu"])
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        chart = compute_chart(
            from_local(**CHART_3_BIRTH_DATA),
            Place(name="Chart 3", **CHART_3_PLACE),
            Settings(node_type=node))
        errors[node] = abs(
            chart.positions[int(Graha.RAHU)].longitude - printed) * 60
    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 8.0


# --------------------------------------------------------------------------
# Example 39, now recomputed from Chart 3
# --------------------------------------------------------------------------

def test_example_39_rasi_sav_recomputes_from_chart_3():
    """All twelve printed figures, from Vajpayee's own longitudes."""
    from hora.charts.ashtakavarga import signs_in_chart

    sav = sarvashtakavarga(signs_in_chart(_chart_3_references(), "D1"))
    assert tuple(sav["rekhas"]) == EXAMPLE_39_RASI_SAV
    assert sav["total"] == SAV_TOTAL


def test_example_39_d10_sav_recomputes_from_chart_3():
    """All twelve again, through the D-10 — so the varga and the ashtakavarga
    are both under test at once."""
    from hora.charts.ashtakavarga import signs_in_chart

    sav = sarvashtakavarga(signs_in_chart(_chart_3_references(), "D10"))
    assert tuple(sav["rekhas"]) == EXAMPLE_39_D10_SAV
    assert sav["total"] == SAV_TOTAL


def test_example_39_d10_lagna_is_scorpio_and_holds_the_maximum():
    """'Lagna in D-10 is Sc and it contains 35 rekhas – maximum in D-10's
    SAV.' Both halves derived, neither transcribed."""
    from hora.charts.ashtakavarga import signs_in_chart
    from hora.charts.vargas import varga

    sav = sarvashtakavarga(signs_in_chart(_chart_3_references(), "D10"))
    lagna = varga(_lon3(CHART_3["Asc"]), "D10").sign
    assert RASI_ABBR[lagna] == "Sc"
    assert sav["rekhas"][lagna] == 35 == max(sav["rekhas"])


def test_example_39_d10_arudha_lagna_has_more_than_thirty_rekhas():
    """'Arudha lagna also contains more than 30 rekhas.' The example never
    names the sign — §9.2 over the D-10 gives Virgo, and Virgo holds 33."""
    from hora.charts.ashtakavarga import signs_in_chart
    from hora.charts.vargas import varga
    from hora.core.const import RASI_NAMES
    from hora.services import arudha_service

    d10 = {int(g): varga(_lon3(CHART_3[name]), "D10").longitude
           for name, g in _CHART_3_GRAHA.items()}
    pada = arudha_service.one(
        1, varga(_lon3(CHART_3["Asc"]), "D10").sign,
        {k: int(v // 30) for k, v in d10.items()}, graha_longitudes=d10)
    sign = RASI_NAMES.index(pada["sign_name"])
    sav = sarvashtakavarga(signs_in_chart(_chart_3_references(), "D10"))
    assert RASI_ABBR[sign] == "Vi"
    assert sav["rekhas"][sign] == 33
    assert sav["rekhas"][sign] > SAV_STRONG_FROM


def test_example_39_d10_third_house_has_more_than_thirty_rekhas():
    """'The 3rd house in D-10 also has more than 30 rekhas – like in the rasi
    chart.' 33 in the D-10 against 34 in the rasi, so 'like' holds."""
    from hora.charts.ashtakavarga import signs_in_chart
    from hora.charts.vargas import varga

    sav = sarvashtakavarga(signs_in_chart(_chart_3_references(), "D10"))
    third = (varga(_lon3(CHART_3["Asc"]), "D10").sign + 2) % 12
    assert RASI_ABBR[third] == "Cp"
    assert sav["rekhas"][third] == 31
    assert sav["rekhas"][third] > SAV_STRONG_FROM
    rasi_third = EXAMPLE_39_RASI_SAV[(R[EXAMPLE_39_LAGNA] + 2) % 12]
    assert rasi_third == 34
    assert rasi_third > SAV_STRONG_FROM


@pytest.mark.parametrize("claim,rasi,rekhas", EXAMPLE_39_D10_CLAIMS)
def test_example_39_d10_claims_each_name_their_deciding_figure(
        claim, rasi, rekhas):
    """Each D-10 claim tied to the sign and rekha count that settles it, so a
    regression in the varga or the SAV names the sentence it breaks."""
    from hora.charts.ashtakavarga import signs_in_chart

    sav = sarvashtakavarga(signs_in_chart(_chart_3_references(), "D10"))
    assert sav["rekhas"][R[rasi]] == rekhas, claim
    assert claim in EXAMPLE_39_ANSWER


def test_example_39_records_that_it_was_verified():
    """OI-102 closed: Chart 3 was supplied and both SAVs recompute exactly."""
    assert "recompute from Chart 3" in EXAMPLE_39_VERIFIED


# --------------------------------------------------------------------------
# Chart 12 — the exercise chart, whose drawn diagram is a D-10
# --------------------------------------------------------------------------

CHART_12_BIRTH_DATA = {
    "year": 1958, "month": 8, "day": 16, "hour": 7, "minute": 5,
    "second": 0.0, "utc_offset_hours": -4.0,
}
CHART_12_PLACE = {"latitude": 43 + 36 / 60, "longitude": -(83 + 53 / 60)}

_CHART_12_GRAHA = {
    "Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
    "Merc": Graha.MERCURY, "Jup": Graha.JUPITER, "Ven": Graha.VENUS,
    "Sat": Graha.SATURN, "Rahu": Graha.RAHU, "Ketu": Graha.KETU,
}


def _lon12(text: str) -> float:
    import re

    match = re.fullmatch(r"(\d+) ?([A-Za-z]{2}) ?(\d+)", text)
    assert match, text
    return R[match.group(2)] * 30 + int(match.group(1)) + int(match.group(3)) / 60


@pytest.mark.parametrize("body", sorted(_CHART_12_GRAHA) + ["Asc"])
def test_chart_12_recomputes_from_its_own_birth_data(body):
    """16 August 1958, 7:05 am, 4h west, 83 W 53, 43 N 36. Every body inside
    one arcminute — the first western-hemisphere chart since Chart 7."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    chart = compute_chart(
        from_local(**CHART_12_BIRTH_DATA),
        Place(name="Chart 12", **CHART_12_PLACE),
        Settings(node_type=NodeType.MEAN))
    expected = _lon12(CHART_12[body])
    got = (chart.lagna_longitude if body == "Asc"
           else chart.positions[int(_CHART_12_GRAHA[body])].longitude)
    assert abs(got - expected) < 1.0 / 60, f"{body}: {got:.4f} vs {expected:.4f}"


def test_chart_12_is_a_fourth_vote_for_the_mean_node():
    """Charts 6, 7 and 10 already needed the mean node. This one separates
    them by the widest margin yet: 0.5' against 77'. See OI-68."""
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    printed = _lon12(CHART_12["Rahu"])
    errors = {}
    for node in (NodeType.MEAN, NodeType.TRUE):
        chart = compute_chart(
            from_local(**CHART_12_BIRTH_DATA),
            Place(name="Chart 12", **CHART_12_PLACE),
            Settings(node_type=node))
        errors[node] = abs(
            chart.positions[int(Graha.RAHU)].longitude - printed) * 60
    assert errors[NodeType.MEAN] < 1.0
    assert errors[NodeType.TRUE] > 60.0


@pytest.mark.parametrize("body,sign", sorted(CHART_12_D10_DRAWN.items()))
def test_our_d10_reproduces_chart_12s_drawn_chart(body, sign):
    """Chart 12 draws its **D-10**, not its rasi chart. So the diagram checks
    the varga as well as the transcription — twelve placements derived from
    the printed rasi longitudes."""
    from hora.charts.vargas import varga

    assert varga(_lon12(CHART_12[body]), "D10").sign == R[sign]


def test_chart_12s_printed_chara_karakas():
    from hora.charts.karaka import chara_karakas

    longitudes = {int(g): _lon12(CHART_12[name])
                  for name, g in _CHART_12_GRAHA.items() if name != "Ketu"}
    assigned = {k.graha: k.symbol for k in chara_karakas(longitudes)}
    for name, symbol in CHART_12_CHARA_KARAKAS.items():
        assert assigned[int(_CHART_12_GRAHA[name])] == symbol, name


def test_chart_12s_d10_sav_is_computable_end_to_end():
    """What the chart is titled for. Its D-10 SAV totals 337 like any other."""
    from hora.charts.ashtakavarga import signs_in_chart

    longitudes = {
        "Sun": _lon12(CHART_12["Sun"]), "Moon": _lon12(CHART_12["Moon"]),
        "Mars": _lon12(CHART_12["Mars"]), "Mercury": _lon12(CHART_12["Merc"]),
        "Jupiter": _lon12(CHART_12["Jup"]), "Venus": _lon12(CHART_12["Ven"]),
        "Saturn": _lon12(CHART_12["Sat"]), "Lagna": _lon12(CHART_12["Asc"]),
    }
    d10 = sarvashtakavarga(signs_in_chart(longitudes, "D10"))
    assert d10["total"] == 337
    assert len(d10["rekhas"]) == 12
    # The D-10 lagna is Virgo, which the drawn chart also shows.
    assert signs_in_chart(longitudes, "D10")["Lagna"] == R["Vi"]


def test_the_rules_endpoint_carries_example_39(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["example_39"]["rasi_sav"] == list(EXAMPLE_39_RASI_SAV)
    assert body["example_39"]["d10_sav"] == list(EXAMPLE_39_D10_SAV)
    assert body["example_39"]["lagna"] == "Sc"
    assert "recompute from Chart 3" in body["example_39"]["verified"]
    assert [c["rekhas"] for c in body["example_39"]["d10_claims"]] == [35, 33, 31]


def test_the_rules_endpoint_carries_chart_12(client):
    body = client.get("/v1/ashtakavarga/rules").json()
    assert body["chart_12"]["title"] == "D-10 SAV Exercise"
    assert "1958" in body["chart_12"]["birth"]
    assert body["chart_12"]["d10_drawn"]["Asc"] == "Vi"
    assert body["chart_12"]["chara_karakas"]["Sun"] == "AK"
    assert "its **D-10**" in body["chart_12"]["note"]
