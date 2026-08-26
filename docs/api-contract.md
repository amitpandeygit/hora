# The API contract

What a client can rely on, what may change, and how a change is made.

## What is guaranteed

Every endpoint declares a response model, so the OpenAPI document at
`/openapi.json` fully describes what comes back. A client can generate types
from it. Before these models existed every endpoint was declared as an untyped
`object` and the document guaranteed nothing.

Within a major version:

| Guaranteed | Not guaranteed |
|---|---|
| Field **names** and **types** stay | Field **order** in a JSON object |
| **Integer ids** keep their meaning | **Display names** — they follow `name_scheme` |
| Fields are **added**, never removed or retyped | Floating-point digits beyond documented tolerance |
| Error **status codes** for a given failure | Error **message wording** |

**Integer ids are the identity.** `rasi: 0` is Aries permanently.
`nakshatra_name: "Pushyami"` is display text that changes if the caller sets
`name_scheme: "standard"` — or if JHora turns out to spell it differently
([OI-2](open-items.md#oi-2)). Never key off a name.

## The envelope

Every **calculation** response — chart, varga, upagraha, panchanga, dasha,
ephemeris — opens with the same two members:

```json
{"input": { "local_time": "...", "utc": "...", "julian_day_ut": 0.0, "place": {...} },
 "settings": { "ayanamsa": "lahiri", "...": "..." }}
```

`input` is the request as the engine resolved it — zone applied, Julian Day
computed. `settings` is the configuration actually used, defaults included. A
response is therefore reproducible from its own body: a caller need not remember
what they sent or which defaults were in force.

Reference and content endpoints do not carry it. They publish static tables and
have no input to echo.

## Meaning of `null`

`null` means **the source gives no value** — Mars has no abode, the nodes have
no deep-exaltation degree. It never means "not computed" and never means zero.

**Every key is always present.** A field that does not apply is null, not
missing: `lord` is null on every panchanga limb but the tithi, and a withheld
content entry carries nulls for its text fields alongside a `reason`. A client
never has to test whether a key exists.

## Input validation

Rejection happens as early as it can and names the input that is wrong.

| Level | What it catches | Status |
|---|---|---|
| Request schema | types, ranges, list bounds, and whether the inputs can answer what was asked | 422 with a field `location` |
| Service | the same coherence rules again, because a service is callable without HTTP | 400 |
| Calculation | non-finite numbers, out-of-range division counts, negative elapsed time | 422 |

Two rules that are easy to get wrong:

- **A longitude wraps; it does not fail.** −45° is 315°, and 405° is 45°. The
  book itself says to "expunge multiples of 360". Only a non-finite value is an
  error.
- **An empty list is a mistake, not a request for nothing.** `charts: []` is
  rejected rather than answered with an empty result. Lists are capped too —
  unbounded fan-out is a denial-of-service shape however cheap each item is.

Every guard in `hora/core/validate.py` exists because something silently
produced a plausible wrong answer: a NaN longitude surfaced as
`cannot convert float NaN to integer` from inside a floor division, and a
negative elapsed time returned a perfectly ordinary-looking degree.

## Types

`mypy` runs clean over the whole package and is enforced by
`tests/unit/test_architecture.py::test_the_package_type_checks`.

It earned its place on the first run: the panchanga dataclass declared `hora`,
`lunar_months` and `solar_date` as bare `object`/`dict`, so nothing checked the
attributes the serializer read off them. Thirty errors in six files.

## Errors

One shape, whatever failed:

```json
{"error": {"type": "bad_request", "message": "unknown varga 'Q9'", "details": null}}
```

`type` is a stable slug and is safe to branch on. `message` is human-readable
and may be reworded. `details` lists per-field problems for a request that
failed validation, and is null otherwise.

Previously three shapes were in use — `{"detail": "..."}` from a raised error,
`{"detail": [...]}` from a failed validation (same key, different type), and a
third from the `ValueError` handler. A client could not parse an error without
knowing which produced it.

## Settings

Every calculation endpoint accepts a `settings` object; `GET /v1/settings/schema`
publishes all of it with defaults. Defaults reproduce Jagannatha Hora's factory
settings as far as they are known, and the responses echo the settings actually
used — a result is reproducible from its own body.

Two defaults were chosen from evidence and are recorded, not assumed:
`apparent_positions: false` and `sunrise_mode: traditional_hindu`. See
[parity.md](parity.md).

## How the contract changes

The contract is pinned by `tests/golden/responses/` — one recorded response per
case in `tests/golden/cases.py`, replayed by `tests/unit/test_golden_api.py`.
Any difference in any field of any response fails the suite.

To change it deliberately:

```bash
python scripts/capture_golden.py        # re-record
git diff tests/golden/responses         # review every changed field
```

The diff is the record of what changed. There is no way to change a response by
accident, and no way to change one quietly.

A new endpoint needs a case in `cases.py` before it is protected —
`test_every_endpoint_is_covered_by_at_least_one_case` enforces that.

## Versioning

The prefix is `/v1`. Within it, only additive change is permitted.

| Change | Allowed in v1? |
|---|---|
| Add an endpoint | yes |
| Add a field | yes |
| Add a settings knob with a default that preserves behaviour | yes |
| Add an enum value | yes |
| Rename or remove a field | no — needs `/v2` |
| Change a field's type | no — needs `/v2` |
| Change a default that alters results | no — needs `/v2`, or an explicit opt-in knob in v1 |
| Fix a calculation that was wrong | **yes** — see below |

### Correctness fixes are not breaking changes

This engine exists to be right. When a calculation is found to disagree with
PVR, the fix ships in v1 even though outputs change. Three have shipped
already — the position flag, the sunrise definition, and the thirteen-hour
pre-dawn upagraha error.

Each one is recorded in [book-deviations.md](book-deviations.md) or
[open-items.md](open-items.md) with what changed and how often it bites. That
record, not a version bump, is how a consumer learns their results moved.

### When `/v2` happens

Nothing is queued. The envelope, the always-present keys and the single error
shape were all settled before v1 had consumers, which is the only cheap moment
to settle them.

## Layering

```
routers/     HTTP only — parse, call one service, translate errors
services/    all application logic; never imports fastapi
charts/ panchanga/ dasha/    the engine
core/        settings, time, constants, the ephemeris seam
```

Enforced by `tests/unit/test_architecture.py`, not by convention: routers are
size-capped, may not import engine modules, and may not contain a loop; services
may not import fastapi or raise `HTTPException`.

The rule exists because the worst bug this project has shipped — the
thirteen-hour pre-dawn error — lived in a router, where the chapter's 109 tests
could not reach it.

---

## Design decisions

Choices in the contract that a caller can trip over, each tagged. These are
**decisions, not defects** — an entry here is settled and tested. Anything
still unresolved belongs in [open-items.md](open-items.md) instead.

<a id="d-1"></a>
### D-1 · Longitudes and rasi indices are told apart by a flag, never inferred · **CLOSED**

`/v1/chakra/build` takes positions as either sidereal longitudes or bare rasi
indices, selected by `positions_are_longitudes`. The two are **not** inferred
from the values, and cannot be mixed in one request.

**Why.** The ranges overlap. `5` is Gemini as an index and five degrees of
Aries as a longitude, and either reading produces a plausible chart. An
inferring parser would be right most of the time and silently wrong exactly
when a chart has an early-degree planet — the case least likely to be noticed.

**Consequences a caller should know:**

* A bare rasi yields `longitude: null` and `degrees_in_rasi: null`, not a
  fabricated `150.0`. Section 1.3.4 needs only the rasi; claiming a precision
  we were not given would be inventing data.
* **A fractional value in rasi mode is refused** — `5.5` is not a rasi index,
  so the likeliest misuse (a longitude with the flag off) is an error rather
  than a silent Virgo.
* **Residual risk, accepted:** a *whole* number below 12 is genuinely
  ambiguous. `5.0` with the flag off is Virgo, and if the caller meant five
  degrees of Aries nothing can tell. Only a caller who both forgets the flag
  *and* has a planet at a whole degree in the first sign is affected, and no
  check can separate those two meanings. Recorded rather than papered over.

Pinned by `test_a_fractional_value_is_refused_in_rasi_mode` and
`test_bare_rasi_indices_carry_no_longitude`.

<a id="d-2"></a>
### D-2 · Not asking for houses differs from asking for impossible ones · **CLOSED**

Omit `reference` on `/v1/chakra/build` and §1.3.3's default applies — "If no
reference point is specified when houses are mentioned, it means that lagna is
used as the reference" — but only when a lagna was supplied. When none was,
the chart comes back with `has_houses: false` and every cell's `house` null.

Naming a reference that cannot be resolved is a **400**.

**Why.** They are different mistakes. A caller who wants occupancy alone has
made none, and should not be blocked. A caller who asked for houses from the
Chandra Lagna without giving the Moon's rasi has, and should not be handed a
chart silently counted from somewhere else.

The first implementation raised in both cases; the tests caught it.

Pinned by `test_the_default_reference_is_skipped_when_no_lagna_was_given`,
`test_a_named_reference_without_a_rasi_is_refused` and
`test_houses_are_refused_when_there_is_no_reference`.
