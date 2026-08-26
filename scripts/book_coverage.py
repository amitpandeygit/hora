#!/usr/bin/env python
"""Inverted coverage probe — what is in the book but nowhere in the codebase?

Every other book test runs in the direction "here is our code, does it match
the book?" That direction can only find *contradictions* inside material we
already noticed. It is structurally blind to **omissions**, which is how a
whole column of Table 2 (the ruling deity of each nakshatra) survived a
chapter-level pass, a re-verification pass, and a page-by-page pass.

This runs the other way, and needs nobody to notice anything:

    1. Take every word on every page of the book in range.
    2. Subtract ordinary English (a system wordlist, plus inflections).
    3. What remains is domain vocabulary — Sanskrit terms, proper nouns,
       abbreviations. This is the material that has repeatedly been missed.
    4. Any such term whose letters appear nowhere in src/, tests/ or docs/ is
       **unaccounted**.

**Known limitation.** Matching is by flattened substring, so that a constant
named ``NAKSHATRA_DEITY`` satisfies the term "nakshatra deity". The cost is
that a short term can be satisfied by an unrelated longer one — "raaja" (king,
a signification of Jupiter) is covered by "raajasik" (of the rajas guna), which
is a different word. Terms under about six letters are therefore weak evidence.
Exact token matching would fix this but would break the compound-constant case,
which matters more often; the trade is deliberate and recorded here rather than
left for someone to discover.

An unaccounted term is not automatically a bug. It may be an OCR fragment, a
typo in the book, or vocabulary belonging to a chapter we have not reached.
But it must be *classified as one of those in writing* — see
``tests/book_terms_reviewed.py``. The gate is not "zero unaccounted terms
forever"; it is **zero unreviewed terms**. New book material means new terms,
which fails the gate until somebody looks at them.

Usage::

    HORA_BOOK_PDF=/path/to/vedic_astro_textbook.pdf python scripts/book_coverage.py
    HORA_BOOK_PDF=... python scripts/book_coverage.py --first 13 --last 89
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

#: Where a term may be "accounted for": constants, tests, or written docs.
CORPUS_DIRS = ("src", "tests", "docs")
CORPUS_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".json", ".txt"}

#: Files that are the *accounting* rather than the code, and must never count
#: as evidence that a term is covered.
#:
#: Without this the probe is circular: writing "ojapada" into the reviewed-terms
#: register would put the word inside ``tests/``, so the very next run would
#: report it as found in the codebase and it would be excused twice over — once
#: as reviewed and once as encoded. A real gap could be buried by classifying
#: it. These three files are therefore invisible to the corpus.
CORPUS_EXCLUDE = {
    "tests/book_terms_reviewed.py",
    "tests/unit/test_book_coverage.py",
    "scripts/book_coverage.py",
}

#: macOS and most Linux boxes ship this. Checked at call time, not import.
WORDLIST = Path("/usr/share/dict/words")

#: Suffixes stripped before asking the wordlist, because the shipped list is
#: Webster's 2nd and has few inflected forms ("abilities", "boxes", "amounts").
_SUFFIXES = ("s", "es", "ed", "ing", "ly", "er", "est", "ers", "ings", "d", "n")

#: Pages 13-89 (0-based) are printed pages 2-78: Part 1, chapters 1 to 7.
DEFAULT_FIRST_PAGE = 13
DEFAULT_LAST_PAGE = 95


def load_english(path: Path = WORDLIST) -> set[str]:
    """The system wordlist, lowercased. Raises if the box does not ship one."""
    if not path.is_file():
        raise FileNotFoundError(
            f"no system wordlist at {path}; the coverage probe needs one to "
            "subtract ordinary English"
        )
    return {line.strip().lower() for line in path.read_text(errors="ignore").splitlines()}


def is_english(word: str, english: set[str]) -> bool:
    """True if ``word`` is ordinary English, allowing for simple inflections.

    Deliberately generous. A false "yes" here hides a term from review, but a
    false "no" only adds noise that gets classified once and stays classified,
    so the cost is asymmetric and this errs toward letting terms through.
    """
    if word in english:
        return True
    if word.endswith("ies") and word[:-3] + "y" in english:
        return True
    for suffix in _SUFFIXES:
        if not word.endswith(suffix):
            continue
        stem = word[: -len(suffix)]
        if stem in english or stem + "e" in english:
            return True
        # "running" -> "run": undouble a final consonant.
        if len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in english:
            return True
    return False


def page_texts(pdf_path: Path, first: int, last: int) -> dict[int, str]:
    """Extract pages ``first``..``last`` inclusive.

    Indices are **0-based, as pypdf indexes them**, matching
    ``tests/unit/test_book_pages.py`` and ``test_book_source_fidelity.py`` so
    that a page number means the same thing in every book test.
    """
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    return {n: reader.pages[n].extract_text() or "" for n in range(first, last + 1)}


def book_terms(pages: dict[int, str], english: set[str]) -> dict[str, set[int]]:
    """Domain vocabulary in the book, mapped to the pages it appears on."""
    terms: dict[str, set[int]] = defaultdict(set)
    for number, text in pages.items():
        for raw in re.findall(r"[A-Za-z][A-Za-z'-]*", text):
            word = raw.lower().strip("'-")
            if len(word) < 2:
                continue
            # A hyphenated compound counts as English if every part does.
            parts = [p for p in ([word] + word.split("-")) if p]
            if all(is_english(p, english) for p in parts):
                continue
            terms[word].add(number)
    return terms


def codebase_corpus(root: Path = REPO, dirs: tuple[str, ...] = CORPUS_DIRS) -> str:
    """Every source, test and doc file flattened to bare alphanumerics.

    ``CORPUS_EXCLUDE`` files are skipped, so the register cannot vouch for
    itself. Flattening means a term is found regardless of how it is cased,
    spaced, hyphenated or split across a line — ``NAKSHATRA_DEITY`` and "nakshatra
    deity" both contain "nakshatradeity".
    """
    chunks = []
    for name in dirs:
        for path in sorted((root / name).rglob("*")):
            if not (path.is_file() and path.suffix in CORPUS_SUFFIXES):
                continue
            if path.relative_to(root).as_posix() in CORPUS_EXCLUDE:
                continue
            chunks.append(path.read_text(errors="ignore"))
    return re.sub(r"[^a-z0-9]", "", "\n".join(chunks).lower())


def unaccounted(
    pdf_path: Path,
    first: int = DEFAULT_FIRST_PAGE,
    last: int = DEFAULT_LAST_PAGE,
    root: Path = REPO,
) -> dict[str, list[int]]:
    """Domain terms in the book whose letters appear nowhere in the codebase."""
    english = load_english()
    terms = book_terms(page_texts(pdf_path, first, last), english)
    corpus = codebase_corpus(root)
    return {
        term: sorted(pages)
        for term, pages in sorted(terms.items())
        if re.sub(r"[^a-z0-9]", "", term) not in corpus
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--first", type=int, default=DEFAULT_FIRST_PAGE)
    parser.add_argument("--last", type=int, default=DEFAULT_LAST_PAGE)
    parser.add_argument(
        "--all", action="store_true",
        help="list every unaccounted term, not only the unreviewed ones",
    )
    args = parser.parse_args(argv)

    pdf = os.environ.get("HORA_BOOK_PDF")
    if not (pdf and Path(pdf).is_file()):
        print("set HORA_BOOK_PDF to the textbook PDF", file=sys.stderr)
        return 2

    missing = unaccounted(Path(pdf), args.first, args.last)
    if not args.all:
        from tests.book_terms_reviewed import REVIEWED
        missing = {t: p for t, p in missing.items() if t not in REVIEWED}
        label = "unreviewed"
    else:
        label = "unaccounted"

    print(f"pages {args.first}-{args.last}: {len(missing)} {label} term(s)")
    for term, pages in missing.items():
        shown = ", ".join(str(p) for p in pages[:8])
        more = "..." if len(pages) > 8 else ""
        print(f"  {term:28s} p{shown}{more}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
