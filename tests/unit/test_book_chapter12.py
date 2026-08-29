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
    natal_grade,
    rekhas_per_reference,
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
    CHART_11_MERCURY_BAV,
    CLASSICAL_TABLE_TOTALS,
    CLASSICAL_TABLE_TOTALS_PROVENANCE,
    EXAMPLE_37,
    EXAMPLE_37_HOUSES,
    EXAMPLE_37_RASIS,
    EXAMPLE_37_WORKING,
    EXAMPLE_38_BEST_RASIS,
    EXAMPLE_38_WORST_RASIS,
    EXERCISE_18,
    EXERCISE_18_ANSWER,
    EXERCISE_18_HINT,
    RASI_ABBR,
    SUN_ASHTAKAVARGA_ROWS,
    TABLE_19_WORKED_READING,
    YUGA_YEARS,
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


def test_the_sum_is_not_called_a_sarvashtakavarga():
    """The book has not reached the term, and the two candidate sums differ:
    seven planets comes to 337 when complete, all eight references to 386.
    Both are returned and neither is chosen. See OI-100."""
    result = summed(AKBAR_SIGNS)
    assert result["complete"] is True
    assert result["owners_included"] == [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
        "Lagna"]
    assert result["owners_missing"] == []
    assert result["seven_planets"]["classical_total_when_complete"] == 337
    assert result["eight_references"]["classical_total_when_complete"] == 386
    assert "not a sarvashtakavarga" in result["not_yet_named_note"]
    assert "OI-100" in result["not_yet_named_note"]
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


def test_the_two_candidate_sums_are_both_live_now():
    """Table 26 landing is exactly the moment OI-100 was recorded against:
    the seven-planet sum stays 337 and the eight-reference sum moves to 386.
    Both are returned; neither is called a sarvashtakavarga."""
    result = summed(AKBAR_SIGNS)
    assert result["seven_planets"]["total"] == 337
    assert result["eight_references"]["total"] == 386
    assert (result["eight_references"]["total"]
            - result["seven_planets"]["total"]) == table_total("Lagna") == 49
    assert "not a sarvashtakavarga" in result["not_yet_named_note"]


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
