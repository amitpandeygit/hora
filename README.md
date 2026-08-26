# Hora

Vedic astrology calculation engine and HTTP API, built to match
**Jagannatha Hora 8.0** as its correctness benchmark.

Calculation only — no UI, no chart rendering. Every endpoint is a pure function
of its request body.

## Quick start

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
./scripts/fetch_ephemeris.sh      # Swiss Ephemeris data files (see docs/licensing.md)
./scripts/run_api.sh              # http://localhost:8000/docs
```

```bash
curl -s localhost:8000/v1/chart/rasi -H 'content-type: application/json' -d '{
  "year": 1972, "month": 10, "day": 1, "hour": 13, "minute": 30,
  "tz_name": "Asia/Kolkata",
  "place": {"latitude": 16.2, "longitude": 81.13, "name": "Machilipatnam"}
}' | jq '.lagna, .grahas[0]'
```

## Endpoints

| Method | Path | What it does |
|---|---|---|
| `POST` | `/v1/ephemeris/positions` | Sidereal positions, speeds, ayanamsa |
| `POST` | `/v1/chart/rasi` | D-1 with bhavas, dignities, combustion, lordships |
| `POST` | `/v1/chart/vargas` | Any divisional charts by code (`D1`…`D300`) |
| `POST` | `/v1/chart/shodasavarga` | All sixteen shodasavarga charts |
| `POST` | `/v1/chart/upagrahas` | All eleven upagrahas (chapter 4) |
| `POST` | `/v1/chart/special-lagnas` | Bhaava, Hora, Ghati, Sree (chapter 5) |
| `POST` | `/v1/varga/compute` | Any longitude into any divisional chart |
| `GET` | `/v1/varga/rules` | Every chart's rule, aliases and signification |
| `POST` | `/v1/varga/amsabala` | Vaiseshikamsa strength (chapter 6) |
| `POST` | `/v1/lagna/special` | Special lagnas from longitudes, no birth needed |
| `GET` | `/v1/lagna/rules` | Each lagna's rate, signification and sensitivity |
| `POST` | `/v1/house/from` | Twelve houses counted from any reference rasi |
| `POST` | `/v1/house/references` | Resolve lagna, chandra, ravi, paaka and more |
| `GET` | `/v1/house/categories/{n}` | Trines, quadrants and the rest from any house |
| `GET` | `/v1/house/rules` | Significations, purusharthas, Table 12 |
| `GET` | `/v1/chart/varga-catalog` | The 23 named vargas |
| `POST` | `/v1/panchanga` | Five limbs, paksha, tithi lord, hora, lunar/solar month |
| `POST` | `/v1/dasha` | Nakshatra dasha tree, up to 6 levels |
| `GET` | `/v1/dasha/systems` | Dasha systems implemented |
| `GET` | `/v1/settings/schema` | Every calculation knob and its default |
| `POST` | `/v1/util/notation` | Parse `5s 17 45` / `25 Li 31` / decimal degrees |
| `GET` | `/v1/util/tables/nakshatras` | Table 2 — spans and Vimsottari lords |
| `GET` | `/v1/util/tables/tithis` | Table 3 — pakshas and tithi lords |
| `GET` | `/v1/util/tables/name-schemes` | Transliteration schemes |
| `GET` | `/v1/util/tables/rasis` | Chapter 2 — every rasi attribute |
| `GET` | `/v1/util/tables/grahas` | Chapter 3 — dignities, relations, attributes |
| `GET` | `/v1/reference/rasis` | Editorial indications (licence-gated) |
| `GET` | `/v1/reference/sources` | Content sources and licence status |

Every request takes an optional `settings` object mirroring JHora's
preferences — ayanamsa, node type, house system, sunrise definition, dasha year
length. Defaults are JHora's factory settings. `GET /v1/settings/schema` lists
them all.

## API contract

Every endpoint declares a response model, so `/openapi.json` fully describes
what comes back and a client can generate types from it. What is guaranteed,
what may change, and how a change is made is in
[docs/api-contract.md](docs/api-contract.md).

The contract is pinned by golden fixtures — one recorded response per case,
replayed on every test run. Changing a response by accident is not possible:

```bash
python scripts/capture_golden.py     # re-record, then review the diff
```

## Layout

```
src/hora/
  api/           routers (HTTP only), request schemas, response models
  services/      all application logic; never imports fastapi
  charts/        rasi chart, bhavas, vargas, dignity, upagrahas
  panchanga/     five limbs, day structure, calendars, hora
  dasha/         shared engine + per-system descriptors
  content/       editorial reference material, kept apart from calculation
  core/          settings, time, notation, names
    constants/   the book tables, filed by domain
    ephemeris/   EphemerisProvider protocol + Swiss Ephemeris backend
  benchmark/     JHora parity harness
```

The layering is enforced by `tests/unit/test_architecture.py`, not by
convention: routers are size-capped and may not import engine modules or
contain a loop; services may not import fastapi. That rule exists because the
worst bug this project has shipped lived in a router, where the chapter's tests
could not reach it.

Nothing above `core/ephemeris/base.py` imports `swisseph`. That seam exists for
licensing reasons — see [docs/licensing.md](docs/licensing.md).

## Benchmarking against JHora

```bash
python -m hora.benchmark tests/benchmark/fixtures/*.json
```

JHora is used as a **black-box oracle**: cast a chart there, transcribe the
output into a fixture, diff. No decompilation. Unfilled fixture slots report as
`unverified`, never as passing. See [docs/parity.md](docs/parity.md) for the
method, tolerances, and the open questions about JHora's defaults.

## Calculation vs content

`/v1/chart/*`, `/v1/panchanga`, `/v1/dasha`, `/v1/util/*` are **calculation** —
deterministic, benchmarked against JHora, tested against numbers.

`/v1/reference/*` is **editorial content** — sourced prose and keyword lists,
kept in `data/content/`, tested for structure only. Nothing under
`src/hora/content/` imports calculation code, and calculation responses never
carry editorial text. Clients join the two on the integer ids already present
in every response.

Content from sources whose redistribution licence is unconfirmed is withheld
from responses unless `HORA_SERVE_UNCONFIRMED_CONTENT=1`. See
[docs/open-items.md](docs/open-items.md) OI-12.

## Naming

Display names default to the spellings printed in P.V.R. Narasimha Rao's
textbook (`Pushyami`, `Ekadasi`, `Sakuna`); the common pan-Indian forms are
available via `settings.name_scheme = "standard"`. **Integer indices are the
stable API contract** — every response carries both, so the spelling can change
without breaking a consumer.

## Status

Phase 1 (foundations) is complete and tested; Phases 2-6 cover shadbala,
ashtakavarga, yogas, rasi dashas, Tajaka, KP, muhurta and compatibility. See
[docs/roadmap.md](docs/roadmap.md) for the full JHora feature inventory mapped
to phases.

Chapters 1 to 7 of the author's textbook are verified end to end —
`test_book_chapter1.py` (74), `test_book_chapter2.py` (57),
`test_book_chapter3.py` (135), `test_book_chapter4.py` (142) and
`test_book_chapter5.py` (44), `test_book_chapter6.py` (137) and
`test_book_chapter7.py` (107). A further 357 checks read the book PDF directly
and assert our transcriptions are literally in it:

```bash
HORA_BOOK_PDF=/path/to/vedic_astro_textbook.pdf pytest tests/unit/test_book_source_fidelity.py
```

See [docs/parity.md](docs/parity.md).

Data that exists but that no calculation uses yet is registered in
[docs/not-yet-consumed.md](docs/not-yet-consumed.md), with a test that stops
the register going stale.

All open and closed questions are tracked with status tags in
[docs/open-items.md](docs/open-items.md) — read it before shipping.

What counts as "verified" is defined in
[docs/verification-standard.md](docs/verification-standard.md). Four checks are
required; three is self-consistency, not verification.

There is a fifth check, and it is the one that catches what the other four
cannot. They all ask "does our code match the book?", which can only find
contradictions in material somebody already noticed — never omissions. So
`scripts/book_coverage.py` runs the opposite direction: every word in the book,
minus ordinary English, must either appear in the codebase or be classified in
writing in `tests/book_terms_reviewed.py`.

```bash
HORA_BOOK_PDF=/path/to/vedic_astro_textbook.pdf python scripts/book_coverage.py
```

**Ask for that number rather than asking whether a chapter is done.** A claim of
completion without it is unverified by definition.

Chapters 1 to 7 were then re-read one page at a time, because a chapter-level
pass captures rules and can still miss a whole column of the table beside them.
[docs/page-sweep.md](docs/page-sweep.md) records that sweep: every PDF page from
13 to 89 either carries an assertion in `tests/unit/test_book_pages.py` or is
listed there as prose with a reason, and a test fails if a page is in neither.

Which source wins when the literature disagrees is fixed in
[docs/precedence.md](docs/precedence.md): JHora, then the book, then PVR's later
writings, then BPHS and the classics, then modern consensus. BPHS is the base
PVR builds on, but it survives in variant recensions, so a commonly cited BPHS
reading does not overrule him.

```bash
.venv/bin/python -m pytest -q      # tests
.venv/bin/mypy src/hora            # types
.venv/bin/ruff check src tests     # lint
```

Chapter 5 and 6 calculations are also exposed as **pure endpoints** that take
longitudes rather than a birth — `/v1/lagna/special` and `/v1/varga/compute` —
because that is what they are, and it is how the book's own worked examples are
stated.

## Licensing

Swiss Ephemeris is dual-licensed AGPL / commercial, and AGPL is triggered by
running a **public service**, not just by distribution. Read
[docs/licensing.md](docs/licensing.md) before this goes live.
