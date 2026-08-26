# Page-by-page sweep — PDF pages 13 to 89

## What this is

The chapter-level passes read each chapter for its *rules* and encoded them.
That is how six real gaps survived: a rule can be implemented perfectly while a
whole column of the table beside it is never read. Chapter 2's pass captured
every nakshatra's name, span and lord, and never noticed Table 2 has a fourth
column.

So this sweep re-read the same material one page at a time, asking a narrower
question: **is everything on this page in the code?**

Scope is PDF pages 13–89, which is printed pages 2–78 — Part 1, Chart Analysis,
chapters 1 to 7. PDF 90 begins chapter 8.

## The ledger

`tests/unit/test_book_pages.py` holds one entry per page. A page either

* carries at least one assertion naming it (`test_page_44_...`), or
* appears in `PROSE_PAGES` with a written reason.

`test_every_page_is_accounted_for` fails if a page is in neither, and
`test_prose_pages_and_asserted_pages_do_not_overlap` fails if a page claims
both. Adding a page to neither list is exactly how Table 2's deity column was
missed, so the ledger makes that a test failure rather than an oversight.

The ledger is gated on `HORA_BOOK_PDF`, like `test_book_source_fidelity.py`.
The PDF is not redistributed.

## What the sweep found

Six gaps, all now closed and all exposed through the API:

| # | Gap | Where it hid |
|---|---|---|
| 1 | `NAKSHATRA_DEITY` — Table 2's fourth column, 27 entries | p22 |
| 2 | `YOGA_MEANINGS` — Table 5's third column, 27 entries | p27 |
| 3 | `TITHI_ALTERNATE_NAMES`, `PAKSHA_SYNONYMS`, `PAKSHA_DESCRIPTIONS` | p23 |
| 4 | D-6 was named `Shashtamsa`; the book prints **Shashthamsa** | p65 |
| 5 | `SPECIAL_LAGNA_ALIASES` — Ghati Lagna is also "Ghatika Lagna" | p58 |
| 6 | The relationship/dignity Sanskrit vocabulary — `RELATIONSHIP_KINDS`, `NATURAL_RELATION_NAMES`, `COMPOUND_RELATION_NAMES`, `COMPOUND_RELATION_GLOSSES`, `DIGNITY_NAMES_SA`, `ESSENCE_NAMES` | ch. 3 |

Every one is a *naming or reference* gap. **No calculation was found wrong by
this sweep** — the arithmetic had already been swept separately, longitude by
longitude, which is what caught D-5, D-8 and D-11.

New endpoints: `/v1/util/tables/yogas`, `/v1/util/tables/relationship-terms`.
Extended: `/v1/util/tables/nakshatras` (+`deity`), `/v1/util/tables/tithis`
(+`alternate_names`, `paksha_synonyms`).

## One new deviation

**[D-16 / PVR-8](book-deviations.md)** — §6.6 Example 27 prints `D-3: Li` for
Jupiter at 29°49' Sagittarius. The book's own §6.2.3 rule sends the last 10° of
a rasi to the 9th from it, which is **Leo**. We follow the rule. Blast radius is
nil: neither sign is one of Jupiter's good signs, so all four amsabala verdicts
in the example reproduce exactly, chart for chart.

## Prose pages that were not prose

Four pages had been marked "nothing checkable" and were wrong. Auditing the
`PROSE_PAGES` reasons against the extracted text (looking for `Table N:`,
`Example N:`, or a density of degree signs) surfaced them:

| Page | What was actually there | Now tested by |
|---|---|---|
| 19 | Example 1 — Sree Rama's chart as occupancies | `test_page_19_example_1_rama_occupancies` |
| 59 | The GL sensitivity figure, 1.25°/minute | `test_page_59_ghati_lagna_birthtime_sensitivity` |
| 61 | Exercise 10 **with its printed answer** — the only self-contained Sree Lagna case in the chapter | `test_page_61_exercise_10_sree_lagna_answer` |
| 76 | Example 27 — Jupiter's sign in all sixteen charts plus all four amsabala verdicts | `test_page_76_example_27_amsabala` |

Page 76 is the most valuable single page in the range: a complete worked
amsabala with sixteen intermediate values. Fifteen of the sixteen reproduce
exactly; the sixteenth is D-16 above.

Page 61's answer reproduces to the printed arcminute: Moon 15 Le 29 with lagna
14 Sc 19 gives Sree Lagna at 12°22' Capricorn.

## Status

77 pages, all accounted for: 52 carry assertions, 25 are prose with
written reasons. The ledger runs 125 tests. Full suite 1485 passing, ruff clean, mypy clean over 73 files.

## What this does not cover

The sweep checks that what the page says is *in the code*. It does not check
the code against JHora 8.0 — that is still [OI-1](open-items.md), and it still
gates shipping.
