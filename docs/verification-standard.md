# What "verified" means here

Twice a chapter was declared done, and twice a follow-up question found real
defects. Both had the same cause, so the remedy is a rule rather than more care.

## The failure

Tests were written by the same person, from the same reading, as the code.

- Chapter 1: the tithi and yoga formulas were **re-derived inside the test
  file**. Production could have been wrong and the tests would still pass.
- Chapter 2: constants were compared to expectations **typed by hand from the
  same reading of the PDF**. A misreading would appear in both places and agree
  with itself.

Neither suite could fail for the reason that mattered. They proved
self-consistency and were reported as fidelity to the source.

## The rule

> A check does not count as verification unless it can fail for the reason we
> actually care about.

In practice that means a claim of "verified against the book" requires **all
four** of the checks below. Three out of four is not verified — it is
self-consistent, and must be described that way.

## The four checks

### 1. Independent source read

Something other than my typing must read the source. For book chapters that is
`tests/unit/test_book_source_fidelity.py`, which opens the PDF and asserts our
text is literally in it.

If a value cannot be machine-checked against the source, say so explicitly and
list it as an exclusion, with a weaker check in its place. See the two colour
exclusions in [parity.md](parity.md).

### 2. Tests call production code

No formula may be re-implemented in a test. If a test needs a calculation, the
calculation must be a production function that the engine also uses.

Chapter 1's `tithi_at`, `yoga_at`, `karana_at` and `paksha_at` exist in
`hora.panchanga.core` for exactly this reason.

### 3. Mutation check

Break the production code on purpose and confirm the suite fails. If it still
passes, the test is decorative.

Recorded for Chapter 1 in [parity.md](parity.md): tithi divisor 12 to 11, yoga
sum to difference, hora cycle reversed — 3, 2 and 4 failures respectively.

### 4. Coverage audit against the chapter itself

Walk the chapter section by section and list every claim, including the ones
already implemented. Chapter 1's Table 1 was missed on the first pass precisely
because nobody enumerated the tables before writing tests.

State what is **not** covered as plainly as what is. For Chapter 2 that is: the
attributes are correct reference data but **no calculation consumes them yet**.

## Reporting

When a chapter is reported complete, the report must state:

- which of the four checks were run, and their counts
- what is implemented but **not yet consumed** by any calculation, added to
  [not-yet-consumed.md](not-yet-consumed.md)
- what was deliberately excluded, and why
- which evidence tier it reaches ([open-items.md](open-items.md) OI-1) — the
  book is tier 2b, not JHora itself

"Done" without those is a status update, not a verification.

## Applying this to chapters 3 onward

Before starting a chapter:

1. Extract its text and enumerate every table, formula, worked example and
   exercise. Write the list down first.
2. Implement.
3. Add the four checks.
4. Report using the format above.

Tracked as [OI-8](open-items.md#oi-8).

---

## The fifth check: inverted coverage

The four checks above all run in one direction — *here is our code, does it
match the book?* That direction finds contradictions inside material somebody
already noticed. **It cannot find omissions.**

That is not a theory. Table 2's ruling-deity column passed a chapter-level
pass, a re-verification pass and a page-by-page pass without being noticed,
because nothing in any of those asked "what does the book contain that the code
does not?" Every gap the sweeps have found has been an omission, never a
contradiction. Reading more carefully does not fix this; it is the same closed
loop, slower.

So there is a fifth check, and it does not depend on anybody noticing anything:

> **Take every word in the book, subtract ordinary English, and fail if what
> remains includes a term that appears nowhere in the codebase and has not been
> classified in writing.**

`scripts/book_coverage.py` runs it; `tests/unit/test_book_coverage.py` gates
it; `tests/book_terms_reviewed.py` holds the classifications.

### Three rules that keep it honest

1. **The gate is zero *unreviewed* terms, not zero unaccounted terms.** Some
   terms are OCR fragments, book typos, or vocabulary from a later chapter.
   Those are fine — but the reason must be written down, not assumed.

2. **Never classify a term to make the test pass.** Read the page first. On the
   probe's first run, roughly a third of what it surfaced was a real gap in a
   chapter that had already been declared done.

3. **The register cannot vouch for itself.** `book_terms_reviewed.py` lives in
   `tests/`, which is part of the searched corpus, so writing a term into it
   would also make that term "found in the codebase" — excusing a real gap
   twice over. Those files are excluded from the corpus; see `CORPUS_EXCLUDE`.

### The same principle elsewhere

`test_not_yet_consumed.py` had a hand-typed list of 37 symbols to track. It
covered 37 of 165 constants, and the register consequently carried four stale
claims that nobody could see. The list is now **discovered from the source**,
not typed.

**Any list of "things to check" that a human maintains by hand has this defect.
Derive it or expect it to be incomplete.**

### What "done" may mean

A chapter is never "done" because it was read. It is done when the numbers say
so, and the numbers are printed by a script:

```
HORA_BOOK_PDF=... python scripts/book_coverage.py     # unreviewed terms
HORA_BOOK_PDF=... pytest tests/unit/test_book_pages.py # page ledger
```

A claim of completion without those numbers is unverified by definition.

---

## The sixth check: enumerate every sentence

The fifth check finds missing **vocabulary**. It cannot find a missing **rule**,
because a rule is usually written in words the codebase already contains.

Chapter 8 proved this twice. The first pass captured all five tables and both
worked examples, and missed eleven prose items — including §8.3's rule that
naisargika karakas are read as *a house counted from the karaka* while chara
and sthira karakas are read as *the karaka itself*. Every word in that sentence
was already somewhere in the repo, so the coverage gate was silent. A second
pass, asked for by the user, found nine more.

What worked was not reading harder. It was making the enumeration mechanical:

> Split the chapter into sentences, number them, and account for **every
> number**. Not "read the page and check the code" — number the sentences,
> then answer for each one.

Chapter 8 came to 96 units across six pages. Going through them in order
surfaced things no amount of careful reading had: that §8.1's warning has a
third sentence, that the book gives a *reason* for each presiding deity, that
the definition of "karaka" is two sentences and only the first was stored.

### Why reading fails where enumeration works

Reading is selective by nature — it looks for what seems important, and a rule
stated in one clause of a long sentence does not seem important. Enumeration
removes the judgement. The unit either has a home in the code or it does not.

### The rule for closing a chapter

A chapter is not done when its tables are in. It is done when:

1. Every sentence has been enumerated and accounted for.
2. Every worked example reproduces, checked through production code.
3. `scripts/book_coverage.py` reports zero unreviewed terms.
4. Every page appears in `tests/unit/test_book_pages.py`.
5. Interpretive text is in `data/content/`, licence-gated, and a test proves it
   does not leak into calculation responses.

Anything less is "the tables are in", and should be said that way.

---

## The seventh check: diff the transcriptions

Checks five and six ask whether content is **present**. Neither asks whether
the strings we present as the author's words **are** his.

Chapter 8's third pass tested that axis for the first time by diffing every
stored string against the PDF character for character. Of forty-odd
transcribed table cells, one was wrong: §8.3's Venus row reads

> Wife, father-in-law, mother-in-law **&** maternal grandparents

and had been stored with "and". Harmless in isolation — and precisely the slip
that lost three of the author's typos in chapter 2 before anyone noticed.

The deeper problem was that **nothing said which strings were transcription**.
Book text and our own summaries sat side by side in the same dicts, so no check
was possible even in principle.

### The fix

Declare it in the data:

```python
VERBATIM_FIELDS = (("STHIRA_KARAKAS", "relative"), ...)
VERBATIM_CONSTANTS = ("KARAKA_DEFINITION", "KARAKA_WARNING")
```

and enforce it with a test that reads the PDF. Everything not declared is ours
by default, which is the safe direction: an unmarked paraphrase stays a
paraphrase, while an unmarked quotation gets caught the moment someone tries to
declare it.

The declaration lives with the constants, not in the test, so a constant that
moves modules carries its provenance with it.

### Also: count the footnotes

Footnote 23 was missed on the first pass and footnote 21 on the second, both
because they were read as part of a block rather than counted. Chapter 8 has
nine footnotes, numbered 20 to 28. A test now asserts each one individually.

**Enumerate footnotes by number, the same way sentences are enumerated.** Any
structure the book numbers — footnotes, tables, examples, exercises, sections —
should be checked by walking its numbering, not by reading past it.
