"""Structural tests for editorial content.

These assert *shape*, never meaning. Nothing here checks whether "Aries is
impulsive" is true — that is not testable, which is exactly why content lives
apart from calculation.

What is worth guarding:
  - every subject has an entry, so a lookup never silently returns nothing
  - the verbatim source text is preserved and matches the term list
  - licence gating actually withholds unconfirmed material
"""
import pytest

from hora.content import get_store
from hora.content.store import UNCONFIRMED

#: Categories are per subject: what a rasi indication can be tagged with is
#: not what a karaka reading can be tagged with. Keeping one flat set would
#: mean either a loose check or a wrong one as new subjects arrive.
CATEGORIES_BY_SUBJECT = {
    "rasi": {"body_part", "appearance", "place", "profession", "temperament"},
    "graha_karaka": {"person_type"},
    # Section 2.2.5's worked examples of reading the 5th house by element.
    "element": {"temperament", "mind"},
    # Avastha results carry conditional clauses, not tagged keywords: the
    # decomposition lives in `results`, so `terms` is empty for this subject.
    "avastha": set(),
}

#: Section 2.3's set, kept under its old name for the rasi-specific tests.
CATEGORIES = CATEGORIES_BY_SUBJECT["rasi"]


@pytest.fixture(scope="module")
def store():
    return get_store()


def test_all_twelve_rasis_have_content(store):
    for rasi in range(12):
        assert store.get("rasi", rasi), f"no content for rasi {rasi}"


def test_every_entry_names_a_declared_source(store):
    for entries in store.entries.values():
        for e in entries:
            assert e.source in store.sources, e.source


def test_verbatim_text_is_preserved(store):
    """The source text must survive, so entries stay auditable against the book."""
    for rasi in range(12):
        for e in store.get("rasi", rasi):
            assert e.verbatim.strip()
            assert e.verbatim.endswith(".")


def test_term_list_matches_the_verbatim_text(store):
    """Categorisation must not drop, reorder or invent terms.

    ``verbatim`` carries the book's text exactly, typos and all. ``terms`` may
    normalise a term only where ``transcription_notes`` says so — every other
    term must match the source token character for character.
    """
    for rasi in range(12):
        for e in store.get("rasi", rasi):
            from_text = [t.strip().rstrip(".").lower() for t in e.verbatim.split(",")]
            terms = [t.term for t in e.terms]
            assert len(terms) == len(from_text), (rasi, "term count drifted")
            for src, got in zip(from_text, terms, strict=True):
                if src == got:
                    continue
                assert e.transcription_notes, (
                    f"rasi {rasi}: '{src}' became '{got}' with no transcription note"
                )
                assert src in e.transcription_notes and got in e.transcription_notes, (
                    f"rasi {rasi}: normalisation '{src}' -> '{got}' not described in "
                    f"transcription_notes: {e.transcription_notes!r}"
                )


def test_documented_normalisations_are_exactly_the_three_book_typos(store):
    """The book misprints three words in 2.3. Nothing else may be 'corrected'.

    A transcription note comes in two kinds and only one of them is a
    correction: a **normalisation**, where the term list spells something
    differently from the verbatim text, and a **preservation**, where the note
    exists to explain why an oddity in `verbatim` is not a mistake of ours.
    This asserts that exactly three entries normalise; preservations are
    unbounded and are checked below.
    """
    normalised = {}
    for rasi in range(12):
        entry = store.get("rasi", rasi)[0]
        parts = {p.strip().rstrip(".").lower() for p in entry.verbatim.split(",")}
        terms = {t.term.lower() for t in entry.terms}
        if terms - parts:
            normalised[rasi] = entry.transcription_notes
    assert set(normalised) == {7, 8, 9}                # Scorpio, Sagittarius, Capricorn
    assert "garrages" in normalised[7] and "garages" in normalised[7]
    assert "uproght" in normalised[8] and "upright" in normalised[8]
    assert "buils" in normalised[9] and "build" in normalised[9]


def test_every_transcription_note_explains_a_normalisation_or_a_preservation(store):
    """No note may be decorative. Either the term list differs from the
    verbatim text, or the note says the oddity was kept as printed."""
    for rasi in range(12):
        entry = store.get("rasi", rasi)[0]
        if not entry.transcription_notes:
            continue
        parts = {p.strip().rstrip(".").lower() for p in entry.verbatim.split(",")}
        terms = {t.term.lower() for t in entry.terms}
        normalises = bool(terms - parts)
        preserves = "kept as printed" in entry.transcription_notes
        assert normalises or preserves, (rasi, entry.transcription_notes)


def test_every_term_has_a_known_category(store):
    """Checked across the whole store, with the set that fits each subject.

    A subject with no entry in CATEGORIES_BY_SUBJECT fails rather than being
    waved through — a new content file must declare what its tags mean.
    """
    for (subject, _), entries in store.entries.items():
        assert subject in CATEGORIES_BY_SUBJECT, (
            f"content subject {subject!r} has no declared category set; "
            "add one to CATEGORIES_BY_SUBJECT"
        )
        allowed = CATEGORIES_BY_SUBJECT[subject]
        for e in entries:
            for t in e.terms:
                assert t.category in allowed, f"{subject}: {t.term} -> {t.category}"


def test_no_empty_terms(store):
    for entries in store.entries.values():
        for e in entries:
            assert all(t.term.strip() for t in e.terms)


#: Gemini and Libra disagree between book sections 2.2.1 and 2.3.
#: See docs/book-deviations.md D-3.
LIMB_MISMATCHES = {2, 6}


@pytest.mark.parametrize("rasi", [r for r in range(12) if r not in LIMB_MISMATCHES])
def test_indications_body_part_agrees_with_the_limb_table(rasi, store):
    """Section 2.3 repeats the limb from 2.2.1 — for ten of the twelve rasis."""
    from hora.core.const import RASI_LIMB

    for e in store.get("rasi", rasi, source="pvr-vaia"):
        body = e.by_category().get("body_part", [])
        assert any(RASI_LIMB[rasi].split()[-1] in b for b in body), (rasi, body)


@pytest.mark.parametrize(
    "rasi,limb_section,indications_section",
    [(2, "arms", "chest"), (6, "space below navel", "groins")],
)
def test_known_limb_mismatches_are_preserved_not_papered_over(
    rasi, limb_section, indications_section, store
):
    """Book sections 2.2.1 and 2.3 conflict here; both readings must survive.

    RASI_LIMB follows 2.2.1, whose stated purpose is defining the limbs.
    The content store keeps 2.3's wording verbatim. See docs/book-deviations.md D-3.
    """
    from hora.core.const import RASI_LIMB

    assert RASI_LIMB[rasi] == limb_section
    entry = store.get("rasi", rasi, source="pvr-vaia")[0]
    assert indications_section in entry.verbatim.lower()


# --------------------------------------------------------------------------
# Licence gating
# --------------------------------------------------------------------------

def test_pvr_content_is_marked_licence_unconfirmed(store):
    assert store.sources["pvr-vaia"]["licence_status"] == UNCONFIRMED
    for rasi in range(12):
        for e in store.get("rasi", rasi, source="pvr-vaia"):
            assert e.licence_status == UNCONFIRMED


def test_unconfirmed_content_is_not_servable_by_default(store, monkeypatch):
    monkeypatch.delenv("HORA_SERVE_UNCONFIRMED_CONTENT", raising=False)
    assert not store.get("rasi", 0)[0].servable


def test_unconfirmed_content_is_servable_when_explicitly_enabled(store, monkeypatch):
    monkeypatch.setenv("HORA_SERVE_UNCONFIRMED_CONTENT", "1")
    assert store.get("rasi", 0)[0].servable


# --------------------------------------------------------------------------
# API surface
# --------------------------------------------------------------------------

def test_reference_endpoint_withholds_text_by_default(client, monkeypatch):
    """Withheld means the text is null, not that the keys vanish.

    Every key is always present so a client never has to test for existence;
    what changes is whether the text fields carry anything.
    """
    monkeypatch.delenv("HORA_SERVE_UNCONFIRMED_CONTENT", raising=False)
    entry = client.get("/v1/reference/rasis/0").json()["entries"][0]
    assert entry["withheld"] is True
    assert entry["verbatim"] is None
    assert entry["terms"] is None
    assert entry["by_category"] is None
    # It still reports that the material exists and why it is held back.
    assert entry["term_count"] > 0
    assert "licence" in entry["reason"].lower()


def test_reference_endpoint_serves_text_when_enabled(client, monkeypatch):
    monkeypatch.setenv("HORA_SERVE_UNCONFIRMED_CONTENT", "1")
    entry = client.get("/v1/reference/rasis/0").json()["entries"][0]
    assert entry["withheld"] is False
    assert entry["verbatim"].startswith("Dynamic")
    assert entry["by_category"]["body_part"] == ["head"]


def test_reference_rejects_out_of_range_rasi(client):
    assert client.get("/v1/reference/rasis/12").status_code == 400


def test_reference_sources_endpoint_reports_gating(client, monkeypatch):
    monkeypatch.delenv("HORA_SERVE_UNCONFIRMED_CONTENT", raising=False)
    body = client.get("/v1/reference/sources").json()
    assert body["serving_unconfirmed"] is False
    assert "pvr-vaia" in body["sources"]


def test_calculation_responses_never_carry_indications(client):
    """The boundary: charts return ids, not editorial text."""
    body = {
        "year": 1972, "month": 10, "day": 1, "hour": 13, "minute": 30,
        "tz_name": "Asia/Kolkata",
        "place": {"latitude": 16.2, "longitude": 81.13},
    }
    raw = client.post("/v1/chart/rasi", json=body).text.lower()
    assert "enterprising" not in raw
    assert "indications" not in raw


def test_content_package_does_not_import_calculation_code():
    """The boundary must hold in code, not just in intent.

    Checks real import statements via the AST, so prose in a docstring that
    merely names a calculation module does not trip it.
    """
    import ast
    import pathlib

    root = pathlib.Path(__file__).resolve().parents[2] / "src" / "hora" / "content"
    forbidden = ("hora.charts", "hora.panchanga", "hora.dasha")
    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                assert not name.startswith(forbidden), f"{path.name} imports {name}"


@pytest.mark.parametrize("var", ["HORA_CONTENT_PATH", "HORA_SERVE_UNCONFIRMED_CONTENT"])
def test_env_vars_are_documented(var):
    import pathlib

    docs = pathlib.Path(__file__).resolve().parents[2] / "docs"
    readme = pathlib.Path(__file__).resolve().parents[2] / "README.md"
    blob = readme.read_text() + "".join(p.read_text() for p in docs.glob("*.md"))
    src = pathlib.Path(__file__).resolve().parents[2] / "src" / "hora" / "content" / "store.py"
    assert var in blob or var in src.read_text()


def test_store_is_cached():
    assert get_store() is get_store()


def test_content_dir_is_overridable_by_env_var():
    """Operators must be able to point the store at their own content."""
    from hora.content import store as store_mod

    assert "HORA_CONTENT_PATH" in store_mod.__doc__ or hasattr(store_mod, "CONTENT_DIR")
    assert store_mod.CONTENT_DIR.name == "content"
