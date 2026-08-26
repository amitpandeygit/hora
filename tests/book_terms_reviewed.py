"""Every book term that is unaccounted for in the codebase, classified.

``scripts/book_coverage.py`` lists domain vocabulary that appears in the book
and nowhere in ``src/``, ``tests/`` or ``docs/``. Not all of it is a gap: the
PDF extractor breaks words across lines, the book has typos, and some
vocabulary belongs to chapters we have not reached.

But the difference between "not a gap" and "a gap nobody noticed" is exactly
what has been failing. So every such term is classified here, in writing,
before it stops failing the gate. **The gate is zero unreviewed terms, not zero
unaccounted terms.** New book material means new terms, which fail until
somebody looks at them.

Nothing may be added to ``OCR_FRAGMENTS`` or ``BOOK_TYPOS`` to make a test go
green without reading the page. The page numbers are in the probe output.
"""
from __future__ import annotations

#: Words the PDF text layer breaks across a line, leaving a fragment. These are
#: artifacts of extraction, not vocabulary: "alculated" is "calculated" with the
#: leading letter left on the previous line.
OCR_FRAGMENTS = {
    "alculated", "analyz", "criptures", "dercurrents", "derstand",
    # Page 82, "development" broken across a line. Surfaced only when
    # open-items.md was shortened: it had been matching our own prose,
    # not the codebase. Same false-pass shape as OI-35.
    "developme",
    "energeti",
    "estation", "ficant", "ficator", "freedo", "gnificantly", "i-based",
    "ifestations", "imagi", "informatio", "kitch", "lexible", "ligion",
    "analyzi", "children-relate", "losophy", "lyzing", "manif", "mportant", "nizes", "ominent", "onder",
    "perfectio", "prophe", "recog", "rresponding", "slightl", "striv",
    "sufferin", "superf", "tructions", "ttempt", "uildings", "ursue",
    "variatio", "vario", "warrio",
}

#: Misspellings in the book itself. Recorded rather than silently corrected —
#: the same discipline as the ``verbatim`` content fields, where quietly fixing
#: "garrages" once cost us the ability to prove what the book actually said.
BOOK_TYPOS = {
    "appropriatesly",   # p35, "appropriately"
    "brigher",          # p24, "brighter"
    "nuetral",          # p48, "neutral"
    "tranformation",    # p34, "transformation"
    "jeshtha",          # p26, "Jyeshtha" — spelled both ways in one sentence
}

#: Ordinary English the shipped wordlist (Webster's 2nd, 1934) simply lacks:
#: modern compounds, hyphenations and inflections.
ORDINARY_ENGLISH = {
    "bhava-based", "boxes", "businessmen", "counsellors", "fickle-minded", "doesn't", "duty-minded",
    "extra-saturnine", "feb", "fortified", "half-lion", "half-man",
    "hard-working", "ill-formed", "mixed-up", "mother-like", "non-sanskrit",
    "one-hour", "planet-based", "rasi-based", "real-life", "self-pride",
    "signified", "specified", "sub-consciousness", "sub-sub-periods",
    "sunsign", "two-hour", "two-letter", "well-being", "well-built",
    "well-defined",
}

#: Vocabulary belonging to chapters past 7, which this sweep does not cover.
#: These are forward references the text makes in passing. Each must be picked
#: up when its chapter is reached; docs/not-yet-consumed.md is the tracker.
LATER_CHAPTERS = {
    # "antardasa" left this set when chapter 15's STRENGTH_MEASURES quoted the
    # book on "determining who initiates dasas and antardasas". The word is now
    # in the codebase; the *feature* is still unbuilt, and that gap is tracked
    # in docs/roadmap.md, not here. This register tracks vocabulary only.

    "mahadasas",                   # ch. on dasas — main periods
    "pratyantardasas",             # ch. on dasas — sub-sub-periods
    "kaarmic",                     # p72, prose in the introduction to part 2
    "moolas",                      # p44, plural of moola; the concept is stored
}

#: Cultural and scriptural background the book gives as context, with no
#: calculation attached to it. Encoding these would be inventing content the
#: engine does not use.
BACKGROUND_PROSE = {
    "jyotishi",                # p16, a practitioner of jyotish
    "saastram",                # p89, "jyotisha saastram"
    "vedaanga",                # p16, jyotisha as a limb of the Vedas
    "sindhu",                  # p15, etymology of "Hindu"
    "paaraasara",              # p89, adjectival form of Parasara
    "parasara's",              # possessive; "Parasara" itself is stored
    "pooja", "purohit",        # p46, examples of Jupiter's significations
    "maharshis",               # p31, the sages generally
    "dharmik",                 # p46, adjectival form of dharma
    "swathi",                  # p60, the book's variant of "Swati" in Example 10
}

#: Everything classified above. A term in this set no longer fails the gate.
#: A term *not* in it, and not in the codebase, fails — which is the point.
REVIEWED: frozenset[str] = frozenset(
    OCR_FRAGMENTS | BOOK_TYPOS | ORDINARY_ENGLISH | LATER_CHAPTERS | BACKGROUND_PROSE
)

#: Sanity: a term must be classified once, not twice. Overlapping sets would
#: mean two different reasons were given for the same word.
_GROUPS = {
    "OCR_FRAGMENTS": OCR_FRAGMENTS,
    "BOOK_TYPOS": BOOK_TYPOS,
    "ORDINARY_ENGLISH": ORDINARY_ENGLISH,
    "LATER_CHAPTERS": LATER_CHAPTERS,
    "BACKGROUND_PROSE": BACKGROUND_PROSE,
}
