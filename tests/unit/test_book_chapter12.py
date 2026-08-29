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
    bhinnashtakavarga,
    entry,
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
    BINDU_REKHA_FOOTNOTE,
    CLASSICAL_TABLE_TOTALS,
    CLASSICAL_TABLE_TOTALS_PROVENANCE,
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
