# JHora feature inventory and build plan

Scope is the full feature list published at
<https://www.vedicastrologer.org/jh/features.htm> for Jagannatha Hora 8.0,
calculation-side only (no UI, no chart drawing, no PDF export).

Status key: **done** · *partial* · todo

---

## Phase 1 — Foundations (done)

| Area | Status | Where |
|---|---|---|
| Julian day / timezone / historical DST | done | `core/timeutil.py` |
| Ayanamsa (20 modes + custom) | done | `core/settings.py`, `core/ephemeris/swiss.py` |
| Sidereal planetary positions, speeds, retrogradation | done | `core/ephemeris/swiss.py` |
| Mean vs true node, Ketu derivation | done | `core/ephemeris/swiss.py` |
| Geocentric / topocentric, true vs apparent | done | `core/ephemeris/swiss.py` |
| Ascendant, MC, 17 house systems | done | `charts/bhava.py` |
| Bhava madhya vs bhava beginning (Indian vs Western cusps) | done | `charts/bhava.py` |
| Rasi chart, nakshatra, pada, house placement | done | `charts/chart.py` |
| Dignity, moolatrikona, compound (5-fold) relationships | done | `charts/dignity.py` |
| Combustion, planetary war | done | `charts/dignity.py` |
| Graha drishti, rasi drishti, virupa aspect values | done | `charts/aspects.py` |
| 23 named vargas + generic D-1..D-300 | done | `charts/vargas.py` |
| Panchanga: tithi, nakshatra, yoga, karana, vaara + end times | done | `panchanga/core.py` |
| Sunrise/sunset/moonrise/moonset, 3 sunrise definitions | done | `panchanga/core.py` |
| 10 nakshatra dasha systems, 6 levels deep | done | `dasha/` |
| Benchmark harness against JHora | done | `benchmark/` |

## Phase 2 — Strengths and classical analysis

| Area | Status | Notes |
|---|---|---|
| Shadbala (all six, ~30 components) | todo | PyJHora's README notes its shadbala differs from JHora's — expect this to need the most benchmark iteration |
| Ishta / kashta phala | todo | |
| Bhinna, Sarva, Prastara, Sodhita ashtakavarga; sodhya pinda | todo | Aspect tables already in `charts/aspects.py` |
| Vimsopaka bala (shadvarga, saptavarga, dasavarga, shodasavarga) | todo | Varga groups already defined |
| Vaiseshikamsa / parijatamsa | todo | |
| Avasthas (baladi, deeptadi, sayanadi, jagradadi) | todo | |
| Harsha bala, pancha vargeeya bala, dwadasa vargeeya bala | todo | Tajaka strengths |
| Upagrahas (Gulika, Maandi, Dhuma, Vyatipata, …) | todo | Needs sunrise-anchored day/night division — `DayStructure` already provides it |
| Special lagnas (Bhava, Hora, Ghati, Sree, Indu, Bhrigu Bindu, Pranapada) | todo | |
| Arudha padas — bhava | done | `/v1/arudha/*`; §9.2's six steps, Sc/Aq resolved via §15.5.1 |
| Arudha padas — graha | done | `/v1/graha-arudha/*`; §9.5's six steps, two-sign owners via §15.5.2 |
| Stronger rasi (§15.5.2) | done | `/v1/rasi-strength/stronger`; the start point for rasi dasas |
| Stronger co-lord (§15.5.1) | done | `/v1/colord/stronger`; unblocks arudha padas |
| Chara karakas (4 schemes) | partial | 8-karaka scheme done (ch. 8, `/v1/karaka/chara`); the other three schemes are not in this book |
| Argala, virodhargala, baadhaka, marana karaka sthana | todo | |
| Sphutas (Tri, Chatur, Pancha, Prana, Deha, Mrityu, Bheeja, Kshetra) | todo | |
| Varnada lagna (5 author variants) | todo | |
| Yogas (~184 in JHora, ~284 in PyJHora) | todo | Rule-DSL rather than 284 hand-written functions |
| Doshas (Kala Sarpa, Manglik, Pitru, Guru Chandala, Ganda Moola, …) | todo | |

## Phase 3 — Remaining dashas

Rasi dashas share one engine (a sign sequence + a duration rule), just as the
nakshatra dashas do — `dasha/base.py` is already shaped for that.

| Group | Systems |
|---|---|
| Rasi dashas | Narayana, Lagnaamsaka, Padanaathaamsa, Sudasa, Drigdasa, Lagna Kendradi, Atmakaraka Kendradi, Trikona, Chara (Parasara + KN Rao), Yogardha, Paryaaya, Shoola, Niryaana Shoola, Brahma, Sthira, Rudramsa Mandooka, Navamsa, Varnada, Kalachakra |
| Nakshatra dashas remaining | Kalachakra, Yogini, Tithi Ashtottari, Tithi Yogini, Tara, Naisargika, Karaka, Aayu, Rashmi, Saptharishi Nakshathra, Buddhi Gathi |
| Other | Moola, Patyayini, Sudarsana Chakra, Rasi-Bhukta Vimsottari, Mudda, Varsha Vimsottari, Varsha Narayana |

## Phase 4 — Transits, Tajaka, prasna

- Transit listings from lagna / Moon / navamsa; tara, murthi, vedha classification
- Graphical transit scores (kakshya-level ashtakavarga transits)
- Tajaka: varsha/maasa/2.5-day/5-hour/25-min/2-min charts; Muntha; Tajaka yogas
  (Ishkavala, Induvara, Ithasala, Eesarpha, Nakta, Yamaya, Manahoo, Kamboola,
  Radda, Duhphali Kutta); 36 sahams
- Tithi/Yoga/Nakshatra Pravesha charts; solar ingress charts
- Eclipse charts (solar and lunar), conjunctions, retrograde and ingress dates
- Prasna: 1-108 number charts, KP 1-249, KP 1-1800
- KP: nakshatra/sub/sub-sub lords to 5 levels for planets and cusps

## Phase 5 — Calendar, muhurta, compatibility

- Rahu kalam, Yama gandam, Gulika kalam, durmuhurtam, abhijit, brahma muhurta
- Choghadiya, Gauri choghadiya, hora lords
- Solar/lunar months (amanta and purnimanta), samvatsara, vedic date
- Festival and vratha finder (Ekadashi, Pradosham, Sankranti, Amavasya, …)
- Marriage compatibility: ashta koota, dasa koota, South Indian 10-porutham
- Chakras: Kaala, Kota, Sarvatobhadra, Shoola, Tripataki, Surya/Chandra Kalanala,
  Saptha Shalaka, Pancha Shalaka, Saptha Naadi
- Pancha Pakshi Sastra

## Phase 6 — Product surface

- City/atlas database with historical timezone resolution (JHora ships ~2.5M places)
- Batch endpoints, caching, rate limiting, API keys
- Monthly panchanga and ephemeris generation endpoints
- Multi-language name output (JHora supports ten Indian languages)

---

## Design principles

1. **One engine per family, not one per system.** The ten nakshatra dashas are
   one function plus ten descriptors. The same will hold for rasi dashas, vargas
   and yogas. JHora's breadth is combinatorial, not 300 independent algorithms.
2. **Settings are first-class.** Every JHora preference is a field on
   `Settings`, defaulted to JHora's factory value, and echoed back in responses.
   Parity is meaningless without knowing which knobs were set.
3. **Nothing above `EphemerisProvider` imports `swisseph`.** See
   [licensing.md](licensing.md).
4. **Unverified is not the same as correct.** Anything not yet diffed against
   real JHora output is marked `PARITY` in the source and listed in
   [parity.md](parity.md).
