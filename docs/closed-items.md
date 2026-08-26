# Closed items

Resolved items, with the evidence that closed them. Nothing here needs action. Live items are in [open-items.md](open-items.md).

| ID | Item |
|---|---|
| [OI-5](#oi-5) | Upagrahas |
| [OI-6](#oi-6) | Special lagnas |
| [OI-9](#oi-9) | Apparent vs true planetary positions |
| [OI-11](#oi-11) | Chapter 1 calculations verified |
| [OI-13](#oi-13) | Chapter 2 rasi attributes verified |
| [OI-16](#oi-16) | Chapter 3 graha attributes and relationships verified |
| [OI-17](#oi-17) | Chapter 4 upagrahas verified |
| [OI-20](#oi-20) | Chapter 5 special lagnas verified |
| [OI-21](#oi-21) | Chapter 6 divisional charts verified |
| [OI-22](#oi-22) | Chapter 7 houses verified |
| [OI-25](#oi-25) | chapter 8 verified against the book |
| [OI-26](#oi-26) | §15.4.4's tables were transcribed outside this record |
| [OI-27](#oi-27) | `rasi_drishti` was wrong |
| [OI-29](#oi-29) | graha arudhas are not implemented |
| [OI-30](#oi-30) | Table 18's specific arudha names are not transcribed |
| [OI-31](#oi-31) | twenty constants were registered as published but were not |
| [OI-32](#oi-32) | §1.3.1's definitional statements were never captured |
| [OI-33](#oi-33) | §1.3.2's primary notation did not parse |
| [OI-34](#oi-34) | §1.3.3's definitional statements were never captured |
| [OI-35](#oi-35) | a false pass in the publication guard |
| [OI-38](#oi-38) | §1.3.8.2 lunar months implemented and verified |
| [OI-41](#oi-41) | §1.3.10 karanas and §1.3.11 horas implemented and verified |
| [OI-42](#oi-42) | §2.2.1 to §2.2.5 rechecked against the book |
| [OI-43](#oi-43) | §2.2.6 to §2.2.12 rechecked against the book |
| [OI-44](#oi-44) | §2.3 indications diffed against the book, two deviations found |
| [OI-45](#oi-45) | §3.2.2's conditional benefics were never implemented |
| [OI-46](#oi-46) | §3.1 and §3.2.1 to §3.2.7 rechecked against the book |
| [OI-47](#oi-47) | §3.2.8 to §3.2.13 rechecked and published |
| [OI-66](#oi-66) | §10.5 argala supplied; primary and secondary separated |

---

<a id="oi-5"></a>
## OI-5 — Upagrahas · **CLOSED**

Chapter 1 §1.3.1 states there are **11 upagrahas** (sub-planets) alongside the
nine grahas. Chapter 1 only names the category; the formulas are in **Chapter 4
(Upagrahas)**, book page 41.

Not a Chapter 1 gap, but they are part of a complete chart and are not built.

Missing: Dhuma, Vyatipaata, Parivesha, Indrachaapa, Upaketu, Kaala, Mrityu,
Artha Praharaka, Yama Ghantaka, Gulika, Maandi.

The sunrise-anchored `DayStructure` they need already exists in
`src/hora/panchanga/core.py`.

**Closed 2026-08-25.** Chapter 4 is implemented and verified to all four checks.

Verified before closing rather than assumed: each of the eleven names listed
above was confirmed to be implemented and to return a longitude in range, and
the four checks were confirmed individually. See [OI-17](#oi-17).

---

<a id="oi-6"></a>
## OI-6 — Special lagnas · **CLOSED**

Chapter 1 §1.3.1 mentions "special ascendants"; §1.3.3 uses horalagna in a worked
example of house reckoning. The formulas are in **Chapter 5 (Special Lagnas)**,
book page 45.

Missing: Bhava Lagna, Hora Lagna, Ghati Lagna, Vighati Lagna, Pranapada Lagna,
Indu Lagna, Bhrigu Bindu, Sree Lagna, Varnada Lagna.

Note: house reckoning *from* an arbitrary reference point already works —
`house_from_sign()` in `src/hora/charts/bhava.py` — so only the lagna longitudes
themselves are missing.

**Closed 2026-08-26.** Chapter 5 is implemented and verified to all four
checks. Verified before closing: Bhaava, Hora, Ghati and Sree lagnas each
compute and return a longitude in range, and each of the chapter's worked
examples reproduces. See [OI-20](#oi-20).

Note the scope: §5.7 ends with a warning that "there are some more special
lagnas defined by Parasara, but they are beyond the scope of this book" —
Vighati, Pranapada, Indu, Bhrigu Bindu and Varnada among them. Those are not
chapter 5's, and remain unbuilt.

---

<a id="oi-9"></a>
## OI-9 — Apparent vs true planetary positions · **CLOSED**

**Resolution:** `apparent_positions: false` — Swiss Ephemeris `SEFLG_TRUEPOS`.

**Evidence:** PyJHora calls Swiss Ephemeris with `SEFLG_TRUEPOS`
(`PLANET_FLAGS` = 65810). Switching to it took the reference chart from
52/57 to **57/57** and reconciled every Vimshottari start date. Apparent
positions put the Sun 20.5 arcsec out — exactly the annual aberration constant.

**Traditional basis:** classical siddhantic astronomy computes true geocentric
longitude; aberration is a telescope-era optical correction.

Approved and applied. Still tier-2 evidence — see OI-1.

---

<a id="oi-11"></a>
## OI-11 — Chapter 1 calculations verified · **CLOSED**

**Resolution:** every formula, table, worked example and exercise in Chapter 1
is implemented and tested. `tests/unit/test_book_chapter1.py`, 74 tests.

Covered: Table 1 (rasis), Table 2 (nakshatras and Vimsottari lords), Table 3
(tithis, pakshas, lords), Table 4 (lunar months), Table 5 (yogas), Examples 2
and 3, Exercises 1-4, the karana rule, the hora rule, solar calendar, Abhijit,
ayanamsa, and both 1999 conjunctions to within 3 seconds of the author's own
published figures.

**Verified honestly:** the tests call production code, not formulas re-derived
in the test file. Confirmed by mutation — changing the tithi divisor from 12 to
11, swapping the yoga sum for a difference, and reversing the hora lord cycle
each made the suite fail.

Excludes display names (OI-2), upagrahas (OI-5), special lagnas (OI-6) and
chart rendering (OI-7).

---

<a id="oi-13"></a>
## OI-13 — Chapter 2 rasi attributes verified · **CLOSED**

**Resolution:** all fifteen classifications in Chapter 2 are implemented and
tested. `tests/unit/test_book_chapter2.py`, 53 tests.

Covered: limbs of the kaala purusha (2.2.1), odd/even (2.2.2), odd-footed
(2.2.3), modality and deity (2.2.4), five elements (2.2.5), pitta/vaata/kapha
(2.2.6), trigunas (2.2.7), directions (2.2.8), colours (2.2.9), day/night
(2.2.10), seershodaya/prishthodaya (2.2.11), varna (2.2.12).

The book's own internal claims are asserted too — that every two-sign lord owns
one day sign and one night sign, and that varna follows the element grouping
exactly.

Two deviations found and recorded in [book-deviations.md](book-deviations.md):
D-1 (dosha mapping departs from conventional Ayurveda) and D-3 (§2.2.1 and §2.3
disagree on the Gemini limb). Both follow the book.

**Transcription verified against the PDF itself**, not from memory —
`tests/unit/test_book_source_fidelity.py`, 172 checks. That pass corrected four
paraphrased colour phrases and restored three of the book's own misprints to the
`verbatim` field. See [parity.md](parity.md#source-fidelity--checked-against-the-pdf-not-from-memory).

Section 2.3 is editorial, not calculation — see OI-12.

---

<a id="oi-16"></a>
## OI-16 — Chapter 3 graha attributes and relationships verified · **CLOSED**

**Resolution:** all 17 attribute sections, Table 6 (dignities), Table 7 (natural
relationships), Table 8 (compound relationships), the §3.4.1 derivation rule,
footnotes 5 and 6, and all four worked examples are implemented and tested.
`tests/unit/test_book_chapter3.py`, 135 tests.

Verified to all four checks in [verification-standard.md](verification-standard.md):

1. **Independent source read** — 61 chapter-3 checks in
   `test_book_source_fidelity.py`, bringing it to 233 against the PDF. Every
   Table 6 row and every Table 7 row is matched character for character,
   degrees included.
2. **Tests call production code** — the relationship examples run through
   `temporal_relation` and `compound_relation`, not re-derived logic.
3. **Mutation check** — six deliberate breaks, all caught: Mercury 15→16,
   Rahu Gemini→Taurus, temporary-friend houses 10→9, swapping mitra and sama in
   the compound table, Moon's Taurus arc, and removing Rahu's ownership.
4. **Coverage audit** — every section enumerated before any code was written.

### Defects this chapter found

- **A pre-existing bug in `sign_dignity`.** Exaltation was checked by *sign*
  before the §3.3 degree rules, so Moon read "exalted" throughout Taurus and
  Mercury throughout Virgo. The book gives Moon exaltation only for 0°–3° and
  Mercury only for 0°–15°. Fixed with `DIGNITY_BY_DEGREE`.
- **A table-drift risk.** The moolatrikona arc lived in two tables that could
  diverge; a mutation of one was caught by only a single test. A guard now
  asserts they agree.
- **A contradiction inside the book** — [D-8](book-deviations.md). The Exercise 6
  answer calls Venus a natural neutral of Jupiter; Table 7 calls it an enemy.
  Table 7 wins, and the §3.4.1 derivation rule independently confirms it.

### Found on re-audit, after this chapter was first reported done

Asked "are we honest for chapter 3?", a second pass found three things the first
report got wrong. All are now fixed, and the correction is recorded here rather
than quietly absorbed.

1. **Paksha and ayana strength were never encoded.** The first report said the
   three §3.2.15 strength rules were "held as constants". Only night/day was.
   `BENEFIC_STRONG_PAKSHA`, `MALEFIC_STRONG_PAKSHA`, `BENEFIC_STRONG_AYANA` and
   `MALEFIC_STRONG_AYANA` now exist and are tested.
2. **Footnote 5 was never captured.** It defines the two ayanas — Uttara is the
   Sun's transit from Capricorn to Gemini, Dakshina from Cancer to Sagittarius.
   Now `AYANA_NAMES` and `RASI_AYANA`. Footnote 6's "each ritu is two months"
   is now `RITU_MONTHS`.
3. **Ten tables were hand-verified only.** Table 6's classical rows, all of
   Table 7, and the element, varna, guna, time-period, dhatu-moola-jeeva,
   digbala and time-strength groupings had no independent source read — exactly
   the closed loop that check 1 exists to prevent. All are now matched against
   the PDF.

### Not yet consumed by any calculation

The attribute tables are correct reference data exposed at
`GET /v1/util/tables/grahas`, but **nothing computes with them yet**. The
§3.2.15 strength rules and the ayana table are constants awaiting shadbala.

---

<a id="oi-17"></a>
## OI-17 — Chapter 4 upagrahas verified · **CLOSED**

**Resolution:** all eleven upagrahas are implemented and tested.
`tests/unit/test_book_chapter4.py`, 109 tests. Exposed at
`POST /v1/chart/upagrahas`.

Covered: §4.1 (two groups), Table 9's five chained formulas and the two
equivalent forms of Upaketu, Example 6, Exercise 7, Table 10's two 7×8 grids of
part lords, the day and night starting rules, the lord-less part, the six rise
points, the natures, the Thursday-night worked example, and footnote 9's
variant.

Verified to all four checks in [verification-standard.md](verification-standard.md):

1. **Independent source read** — 41 chapter-4 checks in
   `test_book_source_fidelity.py`, bringing it to 273 against the PDF. Every
   Table 9 formula and every Table 10 row is matched as printed.
2. **Tests call production code** — everything runs through
   `hora.charts.upagraha`.
3. **Mutation check** — seven deliberate breaks, all caught: Dhuma's offset,
   Upaketu's offset, the night starting graha, the eight-slot cycle (dropping
   the lord-less part), Maandi's rise point, Maandi's part lord, and an
   off-by-one in the part bounds.
4. **Coverage audit** — §4.1 to §4.4 enumerated before any code was written.

### Table 10 is derived, not just transcribed

Every row of both grids is the same eight-slot cycle — the seven grahas in
weekday order then a lord-less slot — rotated to a starting point. Day rows
start at the weekday lord; night rows at the fifth graha from it. The generated
cycle is asserted against the transcribed table, so a slip in either is caught.
This is the same technique that condemned the Exercise 6 prose in chapter 3.

### One conflict found

**[PVR-5](precedence.md) / [D-9](book-deviations.md)** — Exercise 7's printed
answer for Upaketu contradicts both of Table 9's formulas. The formula wins.

### Found on re-audit, after this chapter was first reported done

Three things the first report got wrong, all now fixed:

1. **A serious bug in the endpoint's pre-dawn handling.** For a birth between
   midnight and sunrise, the night's start was estimated as
   `sunset - night_length` instead of being computed. Measured error: **up to
   13 hours**, which displaced all eight parts and every one of the six
   time-based upagrahas. There was **no endpoint test at all**, so nothing
   caught it. Replaced with `birth_period()`, which finds the real previous
   sunset, and covered by 15 tests plus three mutations.
2. **The vaara was wrong for the same births.** The weekday turns at sunrise, so
   a 02:00 birth belongs to the previous vaara. The endpoint took it from the
   following sunrise, rotating the whole Table 10 row and giving every part the
   wrong lord.
3. **Two claims were not encoded.** §4.2's "very malefic" and §4.3's naming of
   Kaala and Mrityu as malefic existed only as prose in an API note. Now
   `VERY_MALEFIC_UPAGRAHAS` and `MALEFIC_UPAGRAHAS`. Footnote 8's normalisation
   rule was also not enumerated; it is now tested.

### Not yet consumed by any calculation

See [not-yet-consumed.md](not-yet-consumed.md) for the full register. From this
chapter: `VERY_MALEFIC_UPAGRAHAS` and `MALEFIC_UPAGRAHAS`. §4.2 says the
Sun-based five "spoil" the houses they occupy — that judgement is applied
nowhere, and will matter for house analysis and yogas.

---

<a id="oi-20"></a>
## OI-20 — Chapter 5 special lagnas verified · **CLOSED**

**Resolution:** Bhaava, Hora, Ghati and Sree lagnas are implemented and tested.
`tests/unit/test_book_chapter5.py`, 31 tests. Exposed at
`POST /v1/chart/special-lagnas`.

Covered: the three rates and their definitions, all three worked illustrations,
Examples 7, 8, 9 and 10, Exercises 8, 9 and 10, §5.5's birthtime sensitivity
and its inversion, §5.6's significations, and §5.7's four-step Sree Lagna method
with its intermediate values.

Verified to all four checks in [verification-standard.md](verification-standard.md):

1. **Independent source read** — 15 chapter-5 checks in
   `test_book_source_fidelity.py`, bringing it to 288 against the PDF. Every
   worked answer and both halves of the PVR-6 contradiction are matched as
   printed.
2. **Tests call production code** — every example runs through
   `hora.charts.special_lagna`.
3. **Mutation check** — seven deliberate breaks, all caught: each of the three
   rates, the Sree Lagna zodiac fraction, its nakshatra span, its addition, and
   the direction of advancement.
4. **Coverage audit** — §5.1 to §5.8 enumerated before any code was written.

### What this chapter changed elsewhere

Reading §5.5 overturned the sunrise default set two chapters earlier. That is
the ladder working: a rank-2 source displaced a rank-5 one as soon as it was
read. See [OI-19](#oi-19).

### A useful confirmation

Exercise 8 works a 03:11 birth from the **previous day's** sunrise, which is
exactly what `birth_period()` does — the function written for chapter 4 after
the pre-dawn bug. The book independently confirms that rule.

### Not yet consumed by any calculation

The special lagnas are computed on request but nothing else uses them. §5.6 says
Hora Lagna shows money and Ghati Lagna shows power, and §5.7 says Sree Lagna is
used in Sudasa — none of that analysis exists yet.

---

<a id="oi-21"></a>
## OI-21 — Chapter 6 divisional charts verified · **CLOSED**

**Resolution:** all twenty divisional charts, Table 11's significations, the
four varga groups and their amsa names are implemented and tested.
`tests/unit/test_book_chapter6.py`, 122 tests.

**Three of our rules were wrong** — see
[D-12, D-13 and D-14](book-deviations.md). The vargas were implemented long
before the chapter was read, from general classical knowledge rather than from
PVR:

| Chart | Was | Should be | Longitudes misplaced |
|---|---|---|---|
| D-5 | odd sequence ended in Leo; even order wrong | Ar, Aq, Sg, Ge, Li / Ta, Vi, Pi, Cp, Sc | 40% |
| D-8 | Ar, Le, Sg (D-16's order) | Ar, Sg, Le | 67% |
| D-11 | counting back from the 12th | the rasi reflected about Aries | 100% |

Found by sweeping all 36,000 longitudes against the book's rules, implemented
independently. Before the fix our code reproduced 28 of 33 worked-example
placements; after it, 32 of 33 — the remaining one being the book's own error
([PVR-7](precedence.md)).

Verified to all four checks in [verification-standard.md](verification-standard.md):

1. **Independent source read** — 39 chapter-6 checks in
   `test_book_source_fidelity.py`, bringing it to 327 against the PDF. Each
   corrected rule rests on the book's own sentence, quoted and matched.
2. **Tests call production code** — every example runs through
   `hora.charts.vargas`.
3. **Mutation check** — seven deliberate breaks, all caught, including
   reverting each of the three corrections.
4. **Coverage audit** — §6.1 to §6.6 enumerated before any code was written.

### Why D-5 survived so long

The book gives **no worked example** for D-5, D-2, D-30, D-1 or the composite
charts. A rule with no example has nothing to catch a transcription slip, and
D-5 was wrong from the day it was written. `GET /v1/varga/rules` now reports
`worked_example_in_book` for every chart, so the weak spots are visible.

### API

Divisional charts are now a first-class API rather than only reachable through
a nativity, because a varga is a pure function of a longitude:

| Endpoint | |
|---|---|
| `POST /v1/varga/compute` | longitude in any notation, in; placements out, each with the rule that produced it |
| `GET /v1/varga/rules` | every chart, its divisions, part size, aliases, signification, and whether the book gives an example |
| `POST /v1/varga/amsabala` | vaiseshikamsa — §6.6's count of strong placements per group, and the amsa it earns |

### Not yet consumed

Table 11's significations and the amsa names are published but nothing reads
them. §6.6 notes that some yogas depend on amsabala — "lagna lord or ghati lagna
lord in Simhaasanaamsa would make one very famous" — and no yoga engine exists.

---

<a id="oi-22"></a>
## OI-22 — Chapter 7 houses verified · **CLOSED**

**Resolution:** the whole chapter is implemented and tested.
`tests/unit/test_book_chapter7.py`, 107 tests. Exposed under `/v1/house/*`.

Covered: §7.1's reference-relative counting with all three of its worked cases,
§7.2's twelve significations and its houses-from-houses composition, §7.3's
eight references including Paaka Lagna and Table 12, §7.4's seven categories
re-based onto any house, §7.4.1's four purusharthas, §7.4.5's two halves,
§7.4.6's summaries, and §7.5's rejection of cusp-based division.

Verified to all four checks in [verification-standard.md](verification-standard.md):

1. **Independent source read** — 30 chapter-7 checks in
   `test_book_source_fidelity.py`, bringing it to 357 against the PDF. Every
   category membership and every signification opening is matched as printed.
2. **Tests call production code** — through `hora.charts.house`.
3. **Mutation check** — six deliberate breaks, all caught: counting direction,
   an off-by-one in re-basing, chaturasra, upachaya, the halves, and a dropped
   entry in Table 12.
4. **Coverage audit** — §7.1 to §7.5 enumerated before any code was written.

### What was missing before

Ten items. `bhava.py` held six category tuples and nothing else — no
significations, no chaturasra, no halves, no purusharthas, no references, no
Table 12, and no way to compute a category from any house but the first.

The last of those is the substantive one. §7.4 works through "the 3rd, 7th and
11th houses are the trines from the 3rd house", and there was no function that
could express it.

### §7.5 confirms a default we already had

The chapter rejects bhava chalit, equal-house and Sripathi division by name —
"this author recommends neither" — and states that each rasi is a house. Our
default `house_system` was already `whole_sign`, so nothing changed; it is now
tested against the chapter that justifies it.

The other sixteen house systems remain available as settings, and are now
documented as being outside what PVR recommends.

### Not yet consumed

The significations, categories, purusharthas and Table 12 are published at
`/v1/house/rules` but no analysis reads them.

---

<a id="oi-25"></a>
## OI-25 — chapter 8 verified against the book · **CLOSED**

Two page-by-page passes over PDF pages 90 to 95.

The first pass captured every table — 13, 14, 15, 16, 17, both worked examples,
and most footnotes — and **missed eleven items**, all of them prose. The second
pass enumerated all 96 sentences mechanically instead of reading for what
looked important, and found **nine more**: the definition of "karaka", the
third sentence of §8.1's warning, the reason each deity presides, the rarity of
the shared-karakatwa case, and the four interpretive readings.

Both worked examples reproduce exactly, to the arcminute. Deviations
[D-17](book-deviations.md) (Table 14's last row names Venus where the value is
Saturn's) and [D-18](book-deviations.md) (Table 17 repeats Table 14's caption)
are recorded.

A third pass found three more, on an axis the first two never tested: not
whether content was *present*, but whether strings we present as the author's
words actually are his.

* The sthira row for Venus reads "mother-in-law **&** maternal grandparents"
  in the book; it had been silently normalised to "and". One cell in four
  tables — the other 40-odd match character for character.
* **Footnote 21** had no home in the code. It is the one that explains why the
  *fixed* significators govern death: sthira means fixed, and death is praana
  becoming fixed. It had been filed as background prose, which was a judgement
  call and a wrong one.
* Nothing distinguished transcription from our own summary. `VERBATIM_FIELDS`
  and `VERBATIM_CONSTANTS` now declare it, and a test enforces it against the
  PDF.

**The lesson, recorded because it generalises:** reading a chapter for its
rules finds tables and misses prose. The coverage gate does not catch that —
prose rules are written in words the codebase already contains. And neither
catches a paraphrase sitting in a field that claims to be a quotation; only a
character-level diff against the source does. Enumerate the sentences, then
diff the transcriptions. See [verification-standard.md](verification-standard.md).

---

<a id="oi-26"></a>
## OI-26 — §15.4.4's tables were transcribed outside this record · **CLOSED**

**This is the one open item that is about provenance rather than astrology.**

`core/constants/avastha.py` carries §15.4.4 in full — the twelve sayanaadi
states (Table 36), the sound-number groups (Table 37), the formula
`((C x P x A) + M + G + L) mod 12`, the planetary adjustments, and footnotes 51
and 52.

**None of it has been checked against the book.** It was written by a turn that
is not in the session record: it appeared on disk with constants and engine
complete and no service, API or tests, which is the shape of an interrupted
implementation. The user's screenshots covered §15.4.1, §15.4.2 and §15.4.3
only — not §15.4.4 — so the source for these tables is unaccounted for.

The API says so rather than hiding it: `/v1/strength/rules` returns
`activity.verified = false` with a pointer here, and the chapter-15 test module
carries a banner saying a green run does not establish that the constants match
the book.

**Every other part of chapter 15 in this codebase is verified**: §15.4.1's four
worked examples reproduce, and §15.4.2 and §15.4.3 were built from the
screenshots the user supplied.

### Update — mostly closed

The user supplied screenshots of §15.4.4 on 2026-08-26. Everything visible in
them was diffed against the code:

| Checked | Result |
|---|---|
| Table 36 — all 12 names and meanings | **match** |
| Table 37 — all 5 Devanagari groups and the Roman column | **match** |
| The six term definitions (C, P, A, M, G, L) | **match, verbatim** |
| The formula `(C x P x A) + M + G + L`, mod 12 | **match** |
| Planetary adjustments (5/2/3/4) | **match** |
| The three strength values | **match** |

One defect found and fixed: row 10 carried an alias **"Nrityalipsaa"** that the
book does not print. Table 36 gives only "Nriyalipsaa". Removed; recorded as
[D-20](book-deviations.md). Row 7's "Sabhaa vasati" is genuine — the book
prints "Sabhaa (Sabhaa vasati)".

`AVASTHA_VERBATIM_FIELDS` now declares which chapter-15 strings are
transcription, matching the discipline chapter 8 uses.

**Still open: footnotes 51 and 52.** The screenshots cut off above them. These
are the navamsa-index example ("Mercury in 22Ge14 ... A = 7") and the ghati
example ("17 hours = 42.5 ... the 43rd ghati"). The code implements both and
the behaviour is pinned by tests, but the footnote *text* has not been seen.

`/v1/strength/rules` reports `activity.verified = true` and
`activity.footnotes_verified = false`.

### Per-graha results — complete

§15.4.4 gives a result line for every (avastha, graha) pair: 12 x 9 = 108.
**All 108 are transcribed** from screenshots, in
`data/content/avastha_results.yaml`, and a test asserts there is exactly one
entry per pair with no gap and no duplicate.

### Closed

Footnotes 51 and 52 were supplied on 2026-08-26 and **both match character for
character**. Every part of §15.4.4 has now been diffed against the book:

| | Result |
|---|---|
| Table 36 — 12 states | match |
| Table 37 — 5 sound groups, Devanagari and Roman | match |
| The six term definitions | match |
| The formula and planetary adjustments | match |
| The three strength values | match |
| Footnote 51 — the navamsa-index example | match |
| Footnote 52 — the ghati example | match |
| All 108 per-graha result lines | transcribed and pinned |

Two defects were found and fixed along the way: an invented alias on Table 36
row 10, later shown to be the author's after all
([D-20](book-deviations.md)), and the remainder-zero reading
([D-19](book-deviations.md)), which stays open as a genuine gap in the book.

`/v1/avastha/rules` reports `activity.verified = true` and
`activity.footnotes_verified = true`.

**The provenance question that opened this item is settled** — not by finding
out who wrote the transcription, but by checking every line of it against the
source.

---

<a id="oi-27"></a>
## OI-27 — `rasi_drishti` was wrong · **CLOSED**

Not "unverified" any more. **Wrong**, with a proof.

`charts/aspects.py` encodes rasi drishti as house offsets:

```python
_RASI_DRISHTI_OFFSETS = {0: (4, 6, 8), 1: (2, 4, 10), 2: (2, 6, 10)}
```

§15.5.1's rule-2 example says: *"Rahu in Ar is aspected by Mars, his
dispositor, from Le."* So Leo must aspect Aries. Ours says Leo aspects Libra,
Sagittarius and Gemini — **not Aries**.

The rule is that movable rasis aspect fixed rasis, fixed aspect movable, and
dual aspect dual, each excluding the adjacent one. Every one of the three
offset triples violates it:

| From | Modality | Ours aspects | Their modalities | Should be |
|---|---|---|---|---|
| Ar | movable | Le, Li, Sg | fixed, **movable**, **dual** | Le, Sc, Aq |
| Le | fixed | Li, Sg, Ge | movable, **dual**, **dual** | Li, Cp, Ar |
| Ge | dual | Le, Sg, Ar | **fixed**, dual, **movable** | Vi, Sg, Pi |

The correct offsets are `{0: (4, 7, 10), 1: (2, 5, 8), 2: (3, 6, 9)}`.

### Fixed

Corrected on the user's approval to
`{0: (4, 7, 10), 1: (2, 5, 8), 2: (3, 6, 9)}`.

`tests/unit/test_rasi_drishti.py` pins it structurally rather than by listing
36 pairs, so a regression has to break an invariant:

* every sign aspects exactly three
* every target is of the modality the rule requires
* no sign aspects itself
* aspects are **mutual** — if A aspects B then B aspects A
* a movable sign skips the fixed sign next to it; a fixed sign skips the
  movable sign before it; a dual sign aspects the other three duals
* the section 15.5.1 example holds: Leo aspects Aries
* a named regression guard against the old offsets

Rule 2 is now self-contained: `charts/colord.py` imports `rasi_drishti` and
builds its own table. `rasi_aspects` remains an override, and an empty table
still models "no aspects known", which stops the cascade at rule 2.

**Verified against the book, not against JHora** — that is [OI-1](#oi-1), as
for everything else.

### Note on OI-18

`charts/aspects.py` is no longer wholly unimported. `rasi_drishti` is verified
and used; `graha_drishti_houses`, `graha_aspects_sign` and `drishti_value` are
still premature and unverified. `test_only_rasi_drishti_is_used_from_the_aspects_module`
fails if any of the three is imported into the engine, so the two halves
cannot blur.

---

<a id="oi-29"></a>
## OI-29 — graha arudhas are not implemented · **CLOSED**

`charts/arudha.py` implements **bhava** arudhas — §9.2's six steps, the arudha
pada of a *house*. `/v1/arudha/pada` and `/v1/arudha/table` return A1 to A12,
with AL and UL named.

**Graha arudhas — the arudha pada of a *planet* — are not implemented at all.**

§15.5.2 is what surfaced this. Its opening says the stronger-rasi rules serve
two purposes:

> We use the same rules for finding the stronger rasi owned by a planet, when
> computing its **graha arudha**.

So the piece §15.5.2 supplies is one input to a computation we do not have.

### What is already in place

* `/v1/rasi-strength/stronger` compares the two rasis a planet owns.
* §15.5.2's note on rule 4 says that comparison **always resolves** for this
  case: "If we have a tie upto rule (3) when finding the stronger rasi owned by
  a planet for computing its graha arudha, this rule will surely resolve the
  tie, because the two rasis owned by each planet have a different oddity."
* §9.2's arudha procedure itself is implemented and takes any rasi.

### What is missing

The section that **defines** graha arudha. Without it we do not know:

* whether the arudha of the stronger owned rasi *is* the graha arudha, or
  whether further steps apply;
* what happens for **Rahu and Ketu**, which own no rasi outright and only
  co-own Scorpio and Aquarius — §15.5.2's guarantee about "the two rasis owned
  by each planet" does not hold for them;
* whether the Sun and Moon, which own one rasi each, skip the comparison
  entirely.

### On the dasa dependency

The user expects this to require dasa analysis. **That is not yet confirmed and
does not follow from what has been read so far**: §15.5.2's own note says rule 4
settles the stronger-owned-rasi question outright, so neither §15.5.1 rule 5a
nor §15.5.2 rule 6 — the only two branches that touch dasa lengths — should be
reached for this purpose.

It may still hold for a reason the graha-arudha section gives, or because graha
arudhas are *used* in dasa analysis rather than *computed* from it. Recorded as
the user's expectation, unverified, rather than silently contradicted or
silently adopted.

### Closed

§9.5 was supplied on 2026-08-26 and is implemented in
`charts/graha_arudha.py`, exposed at `/v1/graha-arudha/*`. Its own worked
example reproduces: the Sun in Gemini owns Leo, the count is 3, and step 4
ends in Libra.

The three unknowns above are all answered:

* **Is the arudha of the stronger owned rasi the graha arudha?** No — the
  stronger owned sign is step 2, and steps 3 to 6 run on from there exactly as
  in §9.2. Those four steps are reused from `charts/arudha.py` rather than
  restated.
* **Rahu and Ketu?** They own one sign each — Aquarius and Scorpio, per §9.2's
  note — so no comparison arises. Same for the Sun and Moon.
* **Do the one-sign owners skip the step?** They do; `owned_decided_by` comes
  back null and the reason says "owns only <sign>".

### On the dasa dependency — settled

This item recorded an expectation that graha arudhas would need dasa analysis.
**They do not.** §15.5.2's rule 6 and §15.5.1's rule 5a are the only branches
that touch dasa lengths, and neither is reachable here: §15.5.2's note
guarantees rule 4 settles every two-sign comparison, because the two signs a
planet owns always differ in oddity.

That is asserted rather than argued —
`test_a_two_sign_owner_is_always_resolvable` runs all five two-sign planets
through all twelve placements and checks a rule always fires, and
`test_graha_arudhas_never_need_a_dasa_input` checks rule 6 is never the one
that fires.

---

<a id="oi-30"></a>
## OI-30 — Table 18's specific arudha names are not transcribed · **CLOSED**

§9.2's six steps, its NOTE on the co-owned signs, the An notation, the AL/UL
special cases and the generic names ("simply called arudha or pada also") are
all implemented and pinned by `tests/unit/test_book_chapter9.py`.

**Table 18 is not.** The section carries a table of specific names for each
arudha — A2 as Dhanarudha and Vitta pada, A9 as Bhagya pada and Pitrarudha,
and so on, several per house. None of it is in the codebase.

This is the same class of gap as Table 2's ruling-deity column in chapter 2:
the *rules* were captured and a *naming table* beside them was not.

**Why it is not simply typed in:** the table sits on the page after the six
steps, and has not been supplied as a screenshot. Text for it exists in an
earlier session transcript, read before the instruction to work only from
screenshots, but it has never been diffed against the source and would be
transcription of unverified provenance — the situation that produced
[OI-26](#oi-26).

### Closed

Table 18 was supplied on 2026-08-26 and transcribed: 12 rows, 51 names, each
pinned per house by `test_table_18_matches_the_book`. Returned on every pada as
`specific_names` and listed whole at `/v1/arudha/rules`.

One defect in the source recorded rather than smoothed over:
[D-21](book-deviations.md) — row A3 prints "Bhatrarudha" beside "Bhratri pada",
the first missing an r. Kept as printed.

Chapter 9 is now complete against §9.2: the six steps, the NOTE, both worked
charts, the An/AL/UL notation, the generic names and Table 18.

---

<a id="oi-31"></a>
## OI-31 — twenty constants were registered as published but were not · **CLOSED**

Found while reviewing §1.3.1 against the code.

`docs/not-yet-consumed.md` lists constants under a heading reading "Published
through `/v1/util/tables/*` and `/v1/reference/*`". **Twenty of the fifty were
not published at all:**

* **17 were never re-exported** from `hora.core.const` — defined in
  `core/constants/*.py` during the page sweep and the chapter 15 work, written
  into the register, and never wired up: `CHAAYAA_GRAHAS`,
  `CHAAYAA_GRAHA_NAME`, `NODE_ALIASES`, `ZODIAC_NAMES`, `ZODIAC_USED`,
  `FOOTED_NAMES`, `GUNA_ADJECTIVES`, the panchaanga and purushartha glosses,
  the element adjective and tattva forms, and the avatara, essence and upagraha
  aliases.
* **3 more reached a service but not a response** — `GRAHA_NAMES_SA`,
  `PAKSHA_DESCRIPTIONS` and `ESSENCE_NAMES` were computed and then dropped,
  because a Pydantic response model returns only the fields it declares.

`test_not_yet_consumed.py` passed throughout, because it asks only whether a
constant is *listed*, never whether what the register *says* about it is true.

### Fixed

All twenty are reachable now. Per-graha and per-rasi vocabulary went onto the
existing rows of `/v1/util/tables/grahas` and `/v1/util/tables/rasis`; the terms
belonging to no single row — the zodiac's two names, the panchaanga gloss, the
chaayaa grahas, the essences, the paksha descriptions, the purushartha gloss
and the upagraha aliases — went to a new `/v1/util/tables/terms`.

### The guard

`tests/unit/test_register_claims.py` turns the heading into a test. Per
constant it asserts the name is on the facade and that its content appears in
some reference or util response. **Adding a name to that section without wiring
it up now fails the suite.**

The lesson generalises past this item: a register that records *membership* is
not the same as one that records *true statements*, and only the second is
worth trusting.

---

<a id="oi-32"></a>
## OI-32 — §1.3.1's definitional statements were never captured · **CLOSED**

Found in the same review as [OI-31](#oi-31), and worth its own entry because it
is a different failure: OI-31 was content that existed and could not be
reached, this is content that was never there.

§1.3.1 is the section that says what a chart is made of. Its **tables** were
all captured long ago — nine grahas, eleven upagrahas, the node aliases. Its
**definitions** were not. Five statements were missing outright:

| Statement | Now |
|---|---|
| "a graha or a planet is a body that has considerable influence on the living beings on earth" | `GRAHA_DEFINITION` |
| Why that is not the astronomical sense — the Sun is a star, the Moon a satellite, both are grahas | `GRAHA_DEFINITION_NOTE` |
| "Rahu and Ketu are not real planets; they are just some mathematical points" | `NODES_ARE_MATHEMATICAL_POINTS` |
| "11 moving mathematical points known as Upagrahas (sub-planets or satellites)" | `UPAGRAHA_DEFINITION`, `UPAGRAHA_GLOSS`, `UPAGRAHA_COUNT` |
| lagna is "the point that rises on the eastern horizon as the earth rotates around itself" | `LAGNA_DEFINITION` |
| "special ascendants" as a named class | `SPECIAL_ASCENDANT_TERM` |

All published at `/v1/util/tables/terms` and pinned by
`tests/unit/test_book_1_3_1.py`.

### Why the node statement earns its place

"Rahu and Ketu are not real planets" is not decoration. It is the reason behind
several deliberate absences in this codebase: the nodes have no
deep-exaltation degree in Table 6, no combustion, and no disc. Those gaps have
each been defended separately over the chapters; this is the sentence they all
trace back to, and a test now ties it to two of them.

### The pattern, again

This is the same shape as Table 2's ruling-deity column and chapter 8's prose
rules: **the tables get captured and the sentences around them do not.** The
sentence-enumeration discipline in
[verification-standard.md](verification-standard.md) exists for exactly this,
and had not been applied to chapter 1 — the page sweep covered chapter 1 at the
level of *pages*, not sentences.

**Open consequence:** chapters 1 to 7 have had the page sweep but not the
sentence enumeration that chapters 8, 9 and 15 have had. This item is closed
for §1.3.1 only.

---

<a id="oi-33"></a>
## OI-33 — §1.3.2's primary notation did not parse · **CLOSED**

Found reviewing §1.3.2. Two defects, one in the parser and one in the service
that wraps it.

### The parser advertised a form it did not accept

`core/notation.py`'s own docstring listed three forms:

> * decimal degrees from 0 Aries — `94.3167`
> * sign-degree-minute — `7s 11d 37'`
> * rasi-relative — `25 Li 31`

`parse` implemented the second and third. **The first raised
`NotationError`** — and it is the form §1.3.2 states first ("measured in
degrees, minutes and seconds from the start of the zodiac"), the form the
Notation paragraph uses for 221°37', and the form Exercise 1 gives Jupiter in.
`94°19'` did not parse.

Added, last in the chain so the two sign-bearing forms keep first refusal —
"5s 17 45" must not read as 5°17'45".

### The service bypassed the parser entirely

`resolve_notation` began:

```python
try:
    lon = float(value)
except ValueError:
    lon = parse(value)
```

Anything `float()` accepted skipped every check `parse` makes. `"400"` came
back **200 OK as 10 Taurus**, because the bare float was then wrapped by a
`% 360`. Now everything goes through `parse`.

### The range is now enforced

§1.3.2: "the longitude of any planet in the skies can be from 0°0'0" ... to
359°59'59"". `parse` refuses anything outside it rather than wrapping, because
wrapping turns a typo into a plausible position in another sign — a worse
failure than an error.

### Verified

Exercise 1 reproduces in all three notations: Jupiter 94°19' to Cancer 4°19',
Mercury 5s 17°45' to Virgo 17°45', Venus 25 Li 31 to Libra 25°31'. Pinned by
`tests/unit/test_book_1_3_2.py` with golden fixtures for each, plus the
refusal path.

---

<a id="oi-34"></a>
## OI-34 — §1.3.3's definitional statements were never captured · **CLOSED**

Third section of chapter 1 reviewed, third set of missing sentences. Same
shape as [OI-32](#oi-32): the arithmetic was right and had been since chapter
7, and the prose around it was absent.

| Statement | Now |
|---|---|
| "house" (Sanskrit name: bhava) | `BHAVA_NAME` |
| "Starting from the rasi occupied by the selected reference point and proceeding in the regular order... the rasi containing the reference point chosen is the 1st house" | `HOUSE_DEFINITION` |
| "when we encounter Pisces, we go to Aries after it" | `HOUSE_ORDER_WRAPS` |
| "the reference points most commonly employed are lagna and special lagnas" | `HOUSE_COMMON_REFERENCES` |
| "If no reference point is specified when houses are mentioned, it means that lagna is used as the reference" | `HOUSE_DEFAULT_REFERENCE`, `HOUSE_DEFAULT_REFERENCE_RULE` |

Published at `/v1/house/rules` under `definition`, pinned by
`tests/unit/test_book_1_3_3.py`.

### The one that matters

Every reference argument in `charts/house.py` defaults to the lagna. That
default was correct but **undefended** — it read as a convention rather than a
rule. §1.3.3's last sentence is what licenses it, and it is now stored next to
the behaviour it justifies.

### Verified

§1.3.3's horalagna example (7 houses from Cancer, crossing the Pisces-Aries
wrap) and Exercise 2 in both parts: from the lagna in Cancer — Sun 10th, Moon
11th, Mars 7th; and from the Moon in Taurus — Sun 12th, Moon 1st, Mars 9th.

### Two guards disagreed, and both were right

`test_register_claims.py` failed on these six because it scanned only
`/v1/util/*` and `/v1/reference/*`, and they publish through
`/v1/house/rules`. The **claim** was too narrow, not the constants. The guard
now scans every parameterless GET and asserts it covers at least four endpoint
families, so it cannot silently narrow again.

Then `test_not_yet_consumed.py` failed on the same six, for the opposite
reason: `house_service` is not one of the register's declared *exposers*, so
naming a constant there counts as **consuming** it — and a consumed constant
must not sit in a register of unconsumed ones.

Both complaints were correct, and the fix satisfied both: the vocabulary moved
to `reference_service.house_definition()`, which *is* an exposer, and
`house_service.rules()` calls it rather than reading the constants. Published,
not consumed, and reachable from the endpoint a house caller is already
looking at.

The exchange is worth recording because the two guards were built for
different purposes and caught each other's blind spot without being designed
to.

---

<a id="oi-35"></a>
## OI-35 — a false pass in the publication guard · **CLOSED**

`test_register_claims.py` was written to catch constants registered as
published but not published ([OI-31](#oi-31)). It had a false pass of its own.

`AYANA_NAMES` is `("uttara", "dakshina")`. It was **published nowhere**. The
guard passed it because it sampled one value — the first — and `"uttara"`
appears inside the nakshatra names *Uttara Phalguni* and *Uttara Ashadha*. A
substring match on unrelated data.

Three other ayana constants were in the same state: `RASI_AYANA`,
`BENEFIC_STRONG_AYANA` and `MALEFIC_STRONG_AYANA`.

### Found by accident

Not by looking for it. §1.3.5 added `FOUR_PILLARS`, a tuple of dicts, which
the guard's sampler could not unwrap — it stopped at the dict and compared its
repr. Fixing the sampler to unwrap dicts and sequences in one pass, and to
prefer the **longest** string it can reach, changed `AYANA_NAMES`' needle from
`"uttara"` to `"dakshina"` — and that one appeared nowhere.

### Fixed

Ayana is now published where it belongs: per rasi on `/v1/util/tables/rasis`
as `ayana`, and per graha on `/v1/util/tables/grahas` as `strong_in_ayana`
(benefics in uttarayana, malefics in dakshinayana, null where the book
classifies the graha as neither).

### The guard is stricter

A new test requires that **every** string value of a short enumeration reaches
a response, not just one. Capped at eight values so it stays a check on
enumerations rather than on tables of prose.

`test_the_ayana_names_are_published_in_both_values` asserts both values appear.

### The lesson

A substring match is a weak assertion, and a weak assertion in a guard is
worse than no guard, because it reads as coverage. This one was written two
sections ago and had a hole from the start.

---

<a id="oi-38"></a>

## OI-38 — §1.3.8.2 lunar months implemented and verified · **CLOSED**

All 24 statements of §1.3.8.2 were enumerated and each is asserted in
`tests/unit/test_book_1_3_8_2.py` (53 tests). Built: `charts/maasa.py`,
`services/maasa_service.py`, `POST /v1/maasa/compute`, `POST /v1/maasa/pair`,
`GET /v1/maasa/rules`.

**What was missing before.** Table 4's columns 1 and 2 existed; **columns 3
and 4 did not**, nor did footnote 2's definition of "conjunction", the
365.2425 / 355 day figures, the three-year interval, the Nija/Adhika terms, or
the 1999 example. Ten constants were added.

**The trap in Table 4.** Column 3 is *not* derivable from column 2. Three rows
spell the month and its constellation differently (Chaitra/Chitra,
Kaarteeka/Krittika, Maagha/Makha) and one is unrelated: **Aaswayuja's
constellation is Aswini**. Four rows name a Poorva/Uttara pair rather than one
nakshatra. The column is transcribed, and a test asserts the Aaswayuja row
specifically so no one later "simplifies" it into a rule.

**Left undecided on purpose:** which member of a Nija/Adhika pair is which —
see [OI-3](#oi-3).

---

<a id="oi-41"></a>

## OI-41 — §1.3.10 karanas and §1.3.11 horas implemented and verified · **CLOSED**

Both sections enumerated statement by statement and asserted in
`tests/unit/test_book_1_3_10.py` (94 tests) and `tests/unit/test_book_1_3_11.py`
(31 tests). Built: `charts/karana.py`, `charts/hora.py`, their services, and
`POST /v1/karana/compute`, `POST /v1/karana/at`, `GET /v1/karana/rules`,
`POST /v1/hora/compute`, `GET /v1/hora/day/{weekday}`, `GET /v1/hora/rules`.

**Both mappings already existed and both were correct** — `_karana_slot` in
`panchanga/core.py` and `hora_lord` in `panchanga/hora.py`. Neither was
reachable as an API, neither was tested against §1.3.10 or §1.3.11 directly,
and `_karana_slot` was private. Tests now assert the new modules agree with
them at all 60 karana slots and all 168 weekday/hora pairs, so the two cannot
drift.

**The trap in §1.3.10.** The four once-only karanas wrap the month boundary:
Sakuna, Chatushpada and Naga close it, Kimstughna opens the next. So slot 1 —
the first half of the first tithi — carries the **11th** name, not the 1st. A
naive first-slot-gets-first-name reading shifts all 56 repeating karanas by one
and still totals 60, so the arithmetic looks right while every name is wrong.

**The trap in §1.3.11.** The cycle is entered at the weekday lord, not at
Saturn. Starting every day at Saturn makes all seven weekdays identical; a test
asserts the seven daily sequences are all distinct.

**Left undecided on purpose:** the hora length — see [OI-40](#oi-40).

---

<a id="oi-42"></a>

## OI-42 — §2.2.1 to §2.2.5 rechecked against the book · **CLOSED**

Audited on request against §2.2.1–§2.2.5. `tests/unit/test_book_2_2.py`, 53
tests, one per statement.

**Every membership list was already correct** — limbs, odd/even, odd-footed,
the three modalities, the four elements. All five partitions verified sign by
sign against the book's own abbreviations, not against an index formula.

**What was missing.** Fifteen constants, all reference vocabulary:

| Section | Missing |
|---|---|
| 2.2.1 | the zodiac-as-Vishnu claim, the applies-to-us statement |
| 2.2.2 | all four names per half (only a code comment mentioned "vishama"/"male"); the stated use |
| 2.2.3 | the stated use |
| 2.2.4 | the deity **roles** (Creator/Destroyer/Sustainer), the English names, the three natures, footnote 3's Trinity note |
| 2.2.5 | the five element definitions, ether/aakaasa as a named constant, the book's prose order of the five, the elements-underlie-everything statement |

All fifteen are now published on `/v1/util/tables/rasis` and registered in
`docs/not-yet-consumed.md`. §2.2.5's four 5th-house readings are PVR's
interpretation, so they went into `data/content/element_indications.yaml`
behind the same licence gate as §2.3 — see [OI-12](#oi-12).

**Two traps now pinned by tests.**

1. §2.2.2 and §2.2.3 are **different partitions**. They disagree on exactly
   four signs — Ta, Le, Sc, Aq — which are precisely the sthira rasis. Nothing
   in the book says so; it falls out of the two lists and is the cheapest
   check that neither was mistyped.
2. Ether is **not** a fifth index in `RASI_ELEMENT`. It is in every rasi, so a
   sign's element stays one of four. Adding a fifth index would take three
   signs away from another element.

**Corrected mid-audit:** my own first draft of the partition test asserted the
two splits disagree on eight signs. The real count is four. The code was
right; the test was wrong and was fixed against measurement.

---

<a id="oi-43"></a>

## OI-43 — §2.2.6 to §2.2.12 rechecked against the book · **CLOSED**

Audited on request. `tests/unit/test_book_2_2.py` now covers §2.2.1–§2.2.12 in
110 tests.

**Every membership list was already correct**, and so were all twelve colours,
character for character — including the two pairs that share a colour (Ta/Le
white, Vi/Cp variegated) and the Pisces entry whose doubled article was already
recorded as a source typo.

**What was missing.** Twenty-one constants, all reference vocabulary:

| Section | Missing |
|---|---|
| 2.2.6 | bilious/windy/phlegmatic; the element compositions; what each humour shows; the body examples; the Ayurveda definition |
| 2.2.7 | purity/energy/darkness; the three effects; "trigunas"; rajo/tamo guna |
| 2.2.10 | nishaa/divaa; the one-day-one-night rule; Moon and Sun as governors |
| 2.2.11 | the head/feet descriptions; footnote 4; the dasa-timing rule |
| 2.2.12 | scholars/warriors/traders/workers; the four descriptions; the element mapping |

All twenty-one are published on `/v1/util/tables/rasis` and registered.

**A correction to our own documentation.** The code comment on `RASI_DOSHA`
said conventional Ayurveda pairs fire+water as pitta and so on, implying the
compositions came from outside the book. **§2.2.6 states them itself**, two
paragraphs above the sign assignment that contradicts them. D-1's wording
carried the same implication. Both corrected: the inconsistency is internal to
§2.2.6.

**Two things now pinned that were previously only prose.**

1. The dosha compositions do **not** give the sign assignment — vaata is
   air+ether but gets the earthy signs, while the airy signs are called
   "mixed". Tested, so `RASI_DOSHA` cannot later be "fixed" into agreement.
2. §2.2.10's claim that each two-sign lord owns one day sign and one night
   sign is checked against `RASI_LORD`, not restated. It holds for all five,
   and it is the cheapest check that either table has been mistyped.

**One structural note.** `DAY_NIGHT_GOVERNOR` holds plain ints, not `Graha`
members: `constants/graha.py` imports `Rasi` from `constants/rasi.py`, so the
reverse import is circular — the same trap as the `VARGA_GROUPS` incident.
`test_2_2_10_the_governors_are_moon_and_sun` pins the two values to the enum.

---

<a id="oi-44"></a>

## OI-44 — §2.3 indications diffed against the book, two deviations found · **CLOSED**

§2.3's twelve lists were already transcribed. They had never been **diffed**
against the source, only checked for shape — every rasi present, categories
known, licence gate holding. Shape tests cannot catch a wrong word.

`tests/content/test_book_2_3_verbatim.py` now holds all twelve as printed and
asserts equality. Running it the first time found two deviations:

| Rasi | Book | We had |
|---|---|---|
| Libra | `Groins, **B**usinessmen, markets` | lowercase `businessmen` |
| Aquarius | `ill-formed teeth,··coarse hair` (double space) | single space |

Both are now restored verbatim with a `transcription_notes` line saying why
they look wrong. Aquarius needed a **quoted YAML scalar**: a plain folded
scalar collapses runs of whitespace, so the double space had been destroyed by
the serialiser rather than by a typist. A test pins it, so re-dumping the file
with default styles fails loudly instead of silently losing it again.

**The three known book typos were already handled correctly** — `garrages`,
`uproght`, `slender buils` are kept in `verbatim` and corrected only in
`terms`. That design was right and is now asserted both ways.

**A guard that was measuring the wrong thing.**
`test_documented_normalisations_are_exactly_the_three_book_typos` asserted that
exactly three entries carry a transcription note, meaning to enforce "only
three words may be corrected". Adding two notes about *preserved* oddities
broke it, because it counted notes rather than corrections. It now compares the
term list against the verbatim text to find real normalisations, and a second
test requires every note to explain either a normalisation or a preservation.

**D-3 confirmed independently and bounded.** Checking where each §2.2.1 limb
appears in its §2.3 list: ten of twelve contain it, and the two that do not are
exactly Gemini (arms vs chest) and Libra (space below navel vs groins) — which
is D-3. `test_d3_covers_exactly_gemini_and_libra` fails if a third ever drifts.
The limb is not always first: Aries opens with "Dynamic" and carries "head"
fifth, Taurus opens with "Beautiful" and carries "face" second.

Section 2.3 remains licence-gated under [OI-12](#oi-12).

---

<a id="oi-45"></a>

## OI-45 — §3.2.2's conditional benefics were never implemented · **CLOSED**

`NATURAL_BENEFIC` and `NATURAL_MALEFIC` were static sets covering seven of the
nine grahas. **Moon and Mercury were in neither**, and nothing implemented the
two conditional rules §3.2.2 states:

> "Mercury becomes a natural benefic when he is alone or with more natural
> benefics ... a natural malefic when he is joined by more natural malefics.
> Waxing Moon of Sukla paksha is a natural benefic. Waning Moon of Krishna
> paksha is a natural malefic."

So a caller reading those sets treated the Moon and Mercury as neither benefic
nor malefic in every chart. `charts/avastha.py` reads them directly at three
sites (`joined_malefics`, `benefic_aspects`, `hostile_aspects`), which means
**a waxing Moon has never counted as a benefic aspect** and Mercury has never
counted either way.

**Built:** `charts/benefic.py`, `services/benefic_service.py`,
`POST /v1/benefic/nature`, `GET /v1/benefic/rules`. The graha table now carries
`natural_nature`, which reads `conditional` for the two.

**A case the book does not cover.** §3.2.2 gives Mercury three situations —
alone, with more benefics, with more malefics. An **equal split** is none of
them. `mercury_nature` returns `neutral` and says so in its reason rather than
forcing a side. Not a defect in our code; a gap in the text.

**Not changed: `charts/avastha.py`.** Wiring the conditional rule into avastha
would move live output on `/v1/avastha`, and avastha would need a paksha and
the co-tenants threaded through it. Deferred with the other decisions — see
**Waiting on you**. The new module is standalone and changes nothing existing.

---

<a id="oi-46"></a>

## OI-46 — §3.1 and §3.2.1 to §3.2.7 rechecked against the book · **CLOSED**

`tests/unit/test_book_3_1_3_2.py`, 77 tests. **Every table was already
correct** — avataras and their aliases, governance, colours, cabinet, deities,
sex. Six reference constants were missing and are now published: the avatara
descriptions (fish, tortoise, boar, half-man half-lion, learned dwarf), the
Sanskrit class names (saumya/subha, kroora/paapa), the deity offices, the
colour-use note, and §3.2.7's sex-prediction note.

**D-6 upgraded.** See docs/book-deviations.md: §3.2.7's own worked example puts
Mercury on both the son and the daughter side, which is only coherent if
Mercury is neuter. Internal evidence now replaces the classical appeal.

**PVR-2 confirmed from the source.** §3.2.2's malefic list does print "Sun,
Mars, Rahu and Ketu" with Saturn absent, as PVR-2 recorded. A test now asserts
the departure explicitly rather than letting `NATURAL_MALEFIC` look like a
straight transcription.

---

<a id="oi-47"></a>

## OI-47 — §3.2.8 to §3.2.13 rechecked and published · **CLOSED**

`tests/unit/test_book_3_1_3_2.py` now covers §3.1 to §3.2.13 in 134 tests.

**All six tables were already correct** — tattvas and their rulers, varnas,
gunas, abodes, dhaatus, time periods. Including two absences that were already
recorded properly: §3.2.11 names no abode for **Mars**, and §3.2.8's Sun and
Moon share an element without ruling it.

**Seventeen constants were missing**, all prose: the five element-governance
clauses, §3.2.9's fortes and its varna glosses, the three guna definitions,
§3.2.10's misconception NOTE, the abode note, the sapta-dhaatu name and the
affliction note, Venus's dhatu gloss, and §3.2.13's prasna note. All now on
`/v1/util/tables/grahas`.

**The book glosses the varnas twice, differently.**

| | brahmana | kshatriya | vaisya | sudra |
|---|---|---|---|---|
| §2.2.12 | **scholars** | warriors | traders | **workers** |
| §3.2.9 | **learned** | warriors | traders | **worker** |

Both are PVR's own. Neither is normalised into the other; both are stored, and
a test pins the two positions where they differ so one cannot quietly win.

**Two apparent contradictions that are not deviations.** The book raises and
answers both itself, so neither is recorded in `book-deviations.md`:

1. The Moon is a **king** in §3.2.5 and a **Vaisya** in §3.2.9. §3.2.9 flags
   this in its own words — "Moon is a king who gets along well with everyone".
2. The Sun is a **kshatriya** in §3.2.9 and **saattwik** in §3.2.10. §3.2.10's
   NOTE exists precisely to explain that pair: "Sun is a king of the warrior
   class and yet he is saattwik."

Both are asserted against the two tables rather than restated, so the tables
cannot drift apart from the prose that reconciles them.

**One cross-chapter check.** §2.2.5 says ether "is present in every rasi" and
gives it no signs; §3.2.8 gives ether a ruling planet, Jupiter. Both hold and
neither is the other — tested, so nobody later adds ether as a fifth
`RASI_ELEMENT`.

---

---

## OI-66 — §10.5 (Argala) was not supplied; §10.6 was built without it · **CLOSED**

§10.6 names the four argala houses outright — "the argala on it from the 2nd,
4th, 11th and 5th houses from it" — so the computation is complete and
Exercise 16's ninety-six cells all reproduce.

But §10.5 is the section that *defines* argala, and it has not been read. Its
own statements — what argala means, whether the four houses carry different
weights, whether anything beyond nature distinguishes them — have had no pass.
`ARGALA_BY_NATURE` currently holds only paapaargala and subhaargala, taken from
§10.6's worked example rather than from §10.5's own definition.

**Closes when:** §10.5 gets a sentence-level pass like every other section.

**Closed 2026-08-27.** §10.5 supplied and given a sentence-level pass. It
corrected the build: the 2nd, 4th and 11th cause **primary** argala and the 5th
a **secondary** one — §10.6 lists all four together and never says so. Every
argala row now carries its kind, and a virodhargala inherits the kind of the
argala it obstructs.

§10.5 also ranks all three of chapter 10's influences in one passage — rasi
drishti "small", graha drishti "more concrete", argala "decisive" — which
settles §10.4's comparison and closes §7.4.6's forward reference (footnote 18
deferred "Argala sthanas: Decisive influences" to this chapter, and §10.5 uses
the same word). Still ordinal; no number anywhere. See OI-64.
