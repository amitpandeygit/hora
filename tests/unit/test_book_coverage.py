"""The inverted coverage gate — is anything in the book missing from the code?

Every other book test runs "here is our code, does it match the book?" That
direction finds contradictions inside material we already noticed. It cannot
find **omissions**, which is why Table 2's ruling-deity column survived a
chapter pass, a re-verification pass and a page-by-page pass untouched.

This test runs the other way. It takes every word in the book, subtracts
ordinary English, and fails if what remains — the domain vocabulary — includes
a term that appears nowhere in ``src/``, ``tests/`` or ``docs/`` and has not
been classified in ``tests/book_terms_reviewed.py``.

Nothing here depends on anybody noticing anything. That is the entire point.

The gate is **zero unreviewed terms**, not zero unaccounted terms. A term may
legitimately be an OCR fragment, a typo in the book, or vocabulary belonging to
a chapter we have not reached — but it must be classified as one of those in
writing, with the page number available from the probe output.

Set ``HORA_BOOK_PDF`` to run. The PDF is not redistributed.

    HORA_BOOK_PDF=/path/to/vedic_astro_textbook.pdf pytest tests/unit/test_book_coverage.py
"""
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from scripts.book_coverage import (
    DEFAULT_FIRST_PAGE,
    DEFAULT_LAST_PAGE,
    WORDLIST,
    codebase_corpus,
    is_english,
    unaccounted,
)
from tests.book_terms_reviewed import _GROUPS, REVIEWED

BOOK_PDF = os.environ.get("HORA_BOOK_PDF")

needs_pdf = pytest.mark.skipif(
    not (BOOK_PDF and Path(BOOK_PDF).is_file()),
    reason="set HORA_BOOK_PDF to the textbook PDF to run coverage checks",
)
needs_wordlist = pytest.mark.skipif(
    not WORDLIST.is_file(), reason=f"no system wordlist at {WORDLIST}"
)


@pytest.fixture(scope="module")
def missing():
    return unaccounted(Path(BOOK_PDF), DEFAULT_FIRST_PAGE, DEFAULT_LAST_PAGE, REPO)


# --------------------------------------------------------------------------
# The gate
# --------------------------------------------------------------------------

@needs_pdf
@needs_wordlist
def test_no_book_term_is_unreviewed(missing):
    """Every domain term is either in the codebase or classified in writing.

    If this fails, do NOT add the term to ``book_terms_reviewed.py`` to make it
    pass. Read the page it appears on first. Roughly a third of the terms this
    probe surfaced on its first run were real gaps in chapters that had already
    been declared done.
    """
    unreviewed = {t: p for t, p in missing.items() if t not in REVIEWED}
    assert not unreviewed, (
        f"{len(unreviewed)} book term(s) neither in the codebase nor reviewed:\n"
        + "\n".join(f"  {t:28s} pages {p}" for t, p in unreviewed.items())
        + "\n\nRead the pages before classifying. See tests/book_terms_reviewed.py."
    )


# --------------------------------------------------------------------------
# Keeping the register itself honest
# --------------------------------------------------------------------------

@needs_pdf
@needs_wordlist
def test_reviewed_terms_are_still_absent_from_the_codebase(missing):
    """A classified term that later gets encoded must leave the register.

    Otherwise the register slowly fills with terms that are no longer
    exclusions, and nobody can tell which entries still mean anything.

    Only the two categories that make a *claim about coverage* are checked.
    "We have not reached that chapter" and "this is background prose we chose
    not to encode" are real claims, and both expire the moment the word turns
    up in the code.

    OCR fragments, book typos and ordinary English are not claims about
    coverage — they are noise the probe could not filter. Whether "derstand"
    happens to sit inside the word "understand" in some docstring says nothing
    about anything, and checking it would make this test fire every time a
    paragraph of prose is added anywhere in the repo.
    """
    from tests.book_terms_reviewed import BACKGROUND_PROSE, LATER_CHAPTERS

    meaningful = BACKGROUND_PROSE | LATER_CHAPTERS
    stale = sorted(meaningful - set(missing))
    assert not stale, (
        "these terms are now in the codebase and should be removed from "
        f"tests/book_terms_reviewed.py: {stale}"
    )


def test_each_term_is_classified_exactly_once():
    """Two reasons for one word means at least one of them is wrong."""
    seen: dict[str, str] = {}
    duplicates = []
    for group, terms in _GROUPS.items():
        for term in terms:
            if term in seen:
                duplicates.append(f"{term} in both {seen[term]} and {group}")
            seen[term] = group
    assert not duplicates, duplicates


def test_reviewed_terms_are_lowercase_and_stripped():
    """The probe lowercases before comparing, so entries must match that."""
    bad = sorted(t for t in REVIEWED if t != t.lower().strip())
    assert not bad, bad


# --------------------------------------------------------------------------
# The probe's own machinery — if these break, the gate silently passes
# --------------------------------------------------------------------------

@needs_wordlist
def test_english_stemming_accepts_ordinary_inflections():
    """The shipped wordlist is Webster's 2nd and lacks most inflected forms.

    If stemming regressed, hundreds of ordinary English words would flood the
    unreviewed list and the real signal would be unreadable.
    """
    from scripts.book_coverage import load_english

    english = load_english()
    for word in ("abilities", "amounts", "analyzing", "accumulates", "alternatives"):
        assert is_english(word, english), word

    # Not exhaustive, and not meant to be: Webster's 2nd lacks some ordinary
    # headwords outright ("box" is absent, so "boxes" cannot be stemmed to it).
    # Those land in ORDINARY_ENGLISH instead. Stemming reduces the noise; the
    # register absorbs what is left.
    assert not is_english("boxes", english)


@needs_wordlist
def test_english_stemming_does_not_swallow_domain_terms():
    """The inverse risk: a filter so generous that real terms never surface."""
    from scripts.book_coverage import load_english

    english = load_english()
    for word in ("nakshatra", "vishamapada", "kalpavrikshaamsa", "indrachaapa"):
        assert not is_english(word, english), word


def test_corpus_flattening_finds_terms_across_case_and_separators():
    """``NAKSHATRA_DEITY`` must satisfy the term "nakshatra deity"."""
    corpus = codebase_corpus(REPO)
    for term in ("nakshatradeity", "vishamapada", "shashthamsa", "ojapada"):
        assert term in corpus, term


def test_corpus_covers_source_tests_and_docs():
    """A term encoded only in a doc still counts as accounted for."""
    corpus = codebase_corpus(REPO)
    assert "bookdeviations" in corpus or "pvr" in corpus
    assert len(corpus) > 100_000
