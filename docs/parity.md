# Parity with Jagannatha Hora

## Method

JHora is treated as a **black-box oracle**. The loop is:

1. Cast a chart in JHora 8.0 with a known, recorded set of preferences.
2. Transcribe its output into a fixture under `tests/benchmark/fixtures/`.
3. `python -m hora.benchmark tests/benchmark/fixtures/*.json` diffs this engine
   against it.

```bash
python -m hora.benchmark tests/benchmark/fixtures/pvr_1972.json --tolerance 1.0
```

A fixture slot whose expected value is `null` is reported as **unverified** —
never as a pass. `--strict` makes unverified slots fail, which is what CI should
use once a fixture is meant to be complete.

To see this engine's numbers in fixture shape for side-by-side transcription:

```bash
python scripts/emit_fixture_template.py tests/benchmark/fixtures/pvr_1972.json
```

That script writes into a separate `hora_observed` block and never into
`expected`, so our own output cannot be mistaken for the benchmark's.

## Tolerances

| Quantity | Tolerance | Rationale |
|---|---|---|
| Planetary longitude | 1 arcsecond | Below any interpretive significance, but tight enough to catch a wrong ayanamsa, node type or ephemeris source |
| Ayanamsa | 1 arcsecond | |
| Varga sign | exact | This tests the *rule*, not the ephemeris |
| Dasha balance | 1e-3 years (~9 hours) | |
| Panchanga end times | 1 second | |

## Evidence tiers

| Tier | Source | Status |
|---|---|---|
| **1** | Jagannatha Hora 8.0 itself | **Nothing recorded.** JHora is Windows-only and no Windows layer is available on this machine. All 36 slots in `pvr_1972.json` are `unverified`. |
| **2** | PyJHora 4.8.7 — an independent AGPL port whose author validated it against JHora | Recorded in `pvr_1972_pyjhora.json`. Run privately with the same `.se1` files, so only algorithms differ, not data. |

A tier-2 match means we agree with another implementation that claims JHora
parity. It is strong evidence and it is not proof. Tier 1 still decides.

## Tier-2 results (PyJHora cross-check)

```bash
python -m hora.benchmark tests/benchmark/fixtures/pvr_1972_pyjhora.json --variants
```

57 fields compared, under both candidate values of the unresolved
`apparent_positions` setting:

| | `apparent` (current) | `true_pos` |
|---|---|---|
| Match | 52 | **57** |
| Mismatch | 5 | **0** |

With both findings applied, the fixture now reports **57 match, 0 mismatch**,
and sunrise, sunset, moonrise and moonset all agree to the second.

The five mismatches are Sun, Mars, Mercury, Jupiter and Venus longitudes, off by
11-48 arcsec. Everything else agrees under **both** settings: ayanamsa, lagna,
Moon, Saturn, Rahu, Ketu, all five retrograde flags, and **all 40 varga signs
across D-9, D-10, D-30 and D-60**.

That last point matters: the varga *rules* are confirmed independently of the
open ephemeris question, because an arcsecond-scale shift does not cross an
amsa boundary here.

Panchanga was checked separately against PyJHora for Bangalore, 25 Aug 2026.

## Findings — APPLIED

Both were reviewed and approved, and are now the defaults.

### Finding A — position flag (APPLIED: `apparent_positions: false`)

PyJHora calls Swiss Ephemeris with `SEFLG_TRUEPOS` (its `PLANET_FLAGS` is
65810 = `SWIEPH | TRUEPOS | SPEED | SIDEREAL`). Setting
`apparent_positions: false` reproduces its output exactly on all ten bodies.

| Setting | Sun | Mercury | Vimshottari Saturn start |
|---|---|---|---|
| `apparent_positions: true` (current) | off by 20.5" | off by 48.2" | off by 2h 25m |
| `apparent_positions: false` | **exact** | **exact** | **exact** |

The 20.5" on the Sun is the annual aberration constant, which is what put us
onto it. `SEFLG_TRUEPOS` already subsumes `NOABERR` and `NOGDEFL` — adding
those changes nothing.

### Finding B — sunrise definition (APPLIED: `sunrise_mode: traditional_hindu`)

PyJHora uses `swe.BIT_HINDU_RISING` (896 = `BIT_DISC_CENTER` +
`BIT_NO_REFRACTION` + 128), read directly from its source, not inferred.
We currently default to `disc_center` (256).

| Flags | sunrise | sunset | moonrise | moonset |
|---|---|---|---|---|
| `disc_center` (our default) | 06:09:13 | 18:34:10 | 16:43:33 | 03:29:22 |
| `geometric_center` (ours) | 06:11:47 | 18:31:37 | 16:46:22 | 03:26:30 |
| `BIT_HINDU_RISING` | 06:11:46 | 18:31:38 | 16:36:58 | 03:31:43 |
| **PyJHora** | **06:11:47** | **18:31:38** | **16:36:58** | **03:31:44** |

A `SunriseMode.TRADITIONAL_HINDU` was added emitting 896, and it is now the
default. `body_rise` was also fixed: it hardcoded `BIT_DISC_CENTER`, so
moonrise ignored the configured definition.

### Where we deliberately do NOT match PyJHora

Tithi boundary times. We solve the elongation root exactly; PyJHora appears to
interpolate. For Dwadashi on 25 Aug 2026 the boundary is where elongation
reaches exactly 144.000000 deg:

| | time | elongation | error |
|---|---|---|---|
| hora | 06:22:04 | 144.000042 | **0.15"** |
| PyJHora | 06:22:46 | 144.005502 | 19.81" |

Ours is the more accurate answer, so it was left alone. Confirm against JHora
before treating the 42-second gap as a defect.

## Open parity questions

These are the settings and rules where JHora's default is not yet confirmed.
Each is marked `PARITY` at its definition site. Resolving them needs one
JHora run each.

| # | Question | Our current default | Where |
|---|---|---|---|
| 1 | Does JHora default Rahu/Ketu to the **mean** or **true** node? | `true` | `settings.py` — *tier-2: PyJHora sets `_use_true_nodes_for_rahu_ketu = True`, and our Rahu/Ketu match it exactly* |
| 2 | Which of the three sunrise definitions is JHora's default? | disc centre with refraction | `settings.py` — *tier-2: see Finding B, PyJHora uses `BIT_HINDU_RISING` (896)* |
| 3 | Which year length does JHora use for Vimshottari — sidereal, 365.25, or savana? | sidereal (365.2564 d) | `settings.py` — *tier-2: PyJHora's default is `TRUE_SIDEREAL_YEAR`; balance matches at 17y 11m 18d* |
| 4 | D-11 rudramsa: which of JHora's two variants is default, and what exactly is the reverse-counting rule? | reverse from the 12th | `vargas.py` |
| 5 | D-5 panchamsa: does JHora use the BPHS unequal sign table or the cyclic rule? | BPHS table | `vargas.py` |
| 6 | What are JHora's other five hora variants and its four drekkana variants? | Parashari + cyclic stubs | `vargas.py` |
| 7 | Which nakshatra starts each non-Vimshottari dasha cycle? | **Ashtottari settled by Table 39** — Ardra, over unequal arcs; the other eight systems still use plain modulo from Ashwini | `dasha/nakshatra/systems.py` |
| 8 | Does JHora's "Deva-datta ayanamsa" map to a Swiss Ephemeris mode, and which? | `SIDM_DJWHAL_KHUL` (a guess) | `settings.py` |
| 9 | Combustion orbs — are JHora's the classical BPHS set, and does it use separate retrograde orbs? | BPHS with retrograde variants | `const.py` |
| 10 | Does JHora resolve graha yuddha by latitude, or by brightness/other rule? | northern planet wins | `dignity.py` |
| 11 | Exact Sripati bhava construction — Porphyry cusps as madhyas, or a different trisection? | Porphyry cusps as madhyas | `bhava.py` |
| 12 | Rahu/Ketu 5th and 9th aspects — on or off by default? | off | `settings.py` |
| 13 | **Apparent vs true positions** — see Finding A. No default chosen; both reported. | apparent (unchanged) | `settings.py` |

## Known ephemeris caveat

Without the Swiss Ephemeris `.se1` data files, `pyswisseph` silently falls back
to the built-in Moshier ephemeris. That is sub-arcsecond for the classical seven
over historical dates, but it is **not** what JHora uses, and it will show up at
the 1-arcsecond tolerance. Run `scripts/fetch_ephemeris.sh` before any parity
run, and check which mode is active:

```python
from hora.core.ephemeris.swiss import _ephemeris_flag
import swisseph as swe
print(_ephemeris_flag() == swe.FLG_SWIEPH)   # True means the .se1 files are in use
```


## Tier-2b: the author's own textbook (Chapter 1)

*Vedic Astrology: An Integrated Approach* by P.V.R. Narasimha Rao — the same
author as JHora. Its worked examples were produced with his own software, so
they sit between PyJHora and JHora itself as evidence.

`tests/unit/test_book_chapter1.py` — 74 tests, all passing.

| Section | Checked | Result |
|---|---|---|
| 1.3.2 | Table 1 — 12 rasis, Sanskrit names, symbols, boundaries | pass |
| 1.3.2 | Exercise 1, sign-degree-minute and rasi notation | pass |
| 1.3.3 | Exercise 2, houses from lagna and from Moon | pass |
| 1.3.6 | Table 2 — 27 boundaries and 27 Vimsottari lords | pass |
| 1.3.6 | Abhijit = last pada of Uttarashadha (6 Cp 40) | **start passes, end does not** — `ABHIJIT_END` runs 53' past the pada, adding the first 1/15 of Sravana. See [open-items.md](open-items.md#oi-36) |
| 1.3.7 | Solar month = rasi of Sun, solar day = degrees + 1 | pass |
| 1.3.8 | Example 2 and Exercise 3 — tithi and paksha | pass |
| 1.3.8 | Table 3 — 30 tithi lords | pass |
| 1.3.8.2 | Table 4 — month name from conjunction rasi | pass |
| 1.3.8.2 | **Both 1999 conjunctions, to the second** | pass |
| 1.3.8.2 | Two Jyeshtha maasas in 1999, one adhika | pass |
| 1.3.9 | Example 3, Exercise 4, Table 5 — yogas | pass |
| 1.3.10 | Karana rule: 4 fixed, 7 movable x 8 | pass |
| 1.3.11 | Hora worked example and weekday lords | pass |
| 1.3.13 | Book uses Lahiri — matches our default | pass |

Every one of these calls production code, not a formula re-derived in the test.
That was verified by mutation: changing the tithi divisor from 12 to 11,
swapping the yoga sum for a difference, and reversing the hora lord cycle each
made the suite fail.

The conjunction check is the tightest constraint we have:

| New Moon | Book | Ours | Diff |
|---|---|---|---|
| Nija Jyeshtha | 1999-05-15 17:35:32 IST, Ta 0d23' | 17:35:33 | +1 sec |
| Adhika Jyeshtha | 1999-06-14 00:33:27 IST, Ta 28d29' | 00:33:24 | -3 sec |

### Caveat on names

Book spellings are now the default output (`name_scheme: book`), with the
standard forms available. The book is from 2000 and JHora 8.0 from 2016;
**JHora's own display names are still unverified** and may match neither.
Integer indices are the stable API contract precisely so this can change.

Tracked as item 2 in [open-items.md](open-items.md).

### Deliberate open choice

Adhika maasa is detected by the classical no-sankranti rule, which agrees with
Chapter 1's two-conjunctions-in-one-rasi observation. Both amanta and
purnimanta month names are returned; no reckoning is chosen as the default.


## Source fidelity — checked against the PDF, not from memory

Every other book test compares our constants to expectations typed out by hand.
That guards against later edits but cannot catch a misreading made once and
repeated in both places.

`tests/unit/test_book_source_fidelity.py` closes that hole: it reads the
textbook PDF and asserts our text is literally in it. 172 checks.

```bash
HORA_BOOK_PDF=/path/to/vedic_astro_textbook.pdf pytest tests/unit/test_book_source_fidelity.py
```

Skipped when the variable is unset, so the suite still runs without the book.

| Checked against the PDF | Count |
|---|---|
| Chapter 2 groupings (odd, footed, modality, element, dosha, guna, direction, day/night, rising, varna) | 30 |
| Chapter 2 limb phrases | 12 |
| Chapter 2 colour phrases | 10 |
| Section 2.3 indication lists, character for character | 12 |
| The book's own three typos, preserved | 3 |
| Chapter 1 name tables (rasi, nakshatra, yoga, karana, masa, tithi) | 105 |

### What this pass corrected

Running it the first time found three places where our text had drifted from
the book:

1. **Four colour phrases were paraphrased.** We had written "colour of the husk
   of grass" and "cream, the colour of fish". The book writes "the color of the
   husk of grass" and "cream color or the color of fish", in American spelling.
   Corrected to the book's own wording.
2. **Section 2.3 `verbatim` was not verbatim.** It carried three silent
   corrections of the book's misprints — "garrages", "uproght", "slender buils".
   The field now holds the book's text exactly; the corrections live in `terms`
   and are described in `transcription_notes`, and a test asserts those are the
   only three normalisations.
3. **A YAML line-wrap defeated one of those restorations**, leaving Sagittarius
   still reading "upright". Caught by the same check.

### Two documented exclusions

Scorpio's colour "reddish brown" is split across a page break in the PDF, and
Pisces drops the book's own doubled article ("cream color or **the the** color
of fish"). Both are excluded from the contiguous-match test and asserted
word-by-word instead, so the exclusions cannot hide a bad reading.
