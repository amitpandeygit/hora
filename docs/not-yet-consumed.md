# Implemented but not yet consumed

Data that is correct, verified against the book, and exposed through the API —
but which **no calculation in this engine uses**.

This is not a defect list. A reference table has to exist before the thing that
consumes it can be built. It is here so that "chapter N is done" is never
mistaken for "chapter N is working", and so nothing is quietly forgotten.

`tests/unit/test_not_yet_consumed.py` checks this register against the code, so
it cannot drift: an entry that becomes consumed, or a new symbol that becomes
unconsumed, fails the suite.

---

## Register

### Chapter 2 — rasi attributes (9)

`RASI_LIMB` · `RASI_DOSHA` · `RASI_GUNA` ·
`RASI_DIRECTION` · `RASI_COLOR` · `RASI_IS_NIGHT` · `RASI_RISING` ·
`RASI_VARNA` · `MODALITY_DEITY`

| Symbol | What will consume it |
|---|---|
| `RASI_IS_NIGHT` | Divaratri bala, in shadbala |
| `RASI_VARNA` | Varna koota, in marriage compatibility |
| `RASI_RISING` | Dasa result timing — §2.2.11 says seershodaya planets give results in the first half of their dasa |
| `RASI_DIRECTION` | Dig analysis and the chakras |
| the rest | Interpretation and medical astrology; reference only |

### Chapter 2 — §2.2 reference vocabulary (15)

Names, definitions and stated uses from §2.2.1 to §2.2.5. None drives a
calculation; all are published on `/v1/util/tables/rasis` so a caller can name
what a classification is and what the book says it is for.

`ZODIAC_AS_VISHNU` · `LIMB_APPLIES_TO_NATIVE` · `ODD_EVEN_NAMES` ·
`ODD_EVEN_USE` · `FOOTED_USE` · `MODALITY_DEITY_ROLE` ·
`MODALITY_NATURE` · `TRINITY_NOTE` · `ELEMENT_DEFINITIONS` · `ETHER_NAME` ·
`ETHER_NAME_SA` · `ETHER_IN_EVERY_RASI` · `ELEMENTS_UNDERLIE_EVERYTHING` ·
`FIVE_ELEMENTS_BOOK_ORDER`

| Symbol | What will consume it |
|---|---|
| `ODD_EVEN_NAMES` | Rasi dasas and the sex-of-children rule — §2.2.2 names both uses |
| `MODALITY_NATURE`, `MODALITY_DEITY_ROLE`, `TRINITY_NOTE` | Interpretation; reference only |
| `ELEMENT_DEFINITIONS`, `ETHER_*`, `FIVE_ELEMENTS_BOOK_ORDER` | Element-based interpretation; reference only |
| the rest | Reference only |

### Chapter 2 — §2.2.6 to §2.2.12 reference vocabulary (21)

Names, glosses, definitions and stated uses. None drives a calculation; all are
published on `/v1/util/tables/rasis`.

`AYURVEDA_NOTE` · `DOSHA_NAMES_EN` · `DOSHA_ELEMENTS` · `DOSHA_SHOWS` ·
`DOSHA_BODY_EXAMPLE` · `DOSHA_SHOWS_TYPO` · `TRIGUNA_NAME` · `TRIGUNA_NOTE` ·
`GUNA_NAMES_ALT` · `GUNA_MEANINGS` · `GUNA_EFFECTS` · `DAY_NIGHT_NAMES` ·
`DAY_NIGHT_PAIR_RULE` · `DAY_NIGHT_GOVERNOR` · `RISING_DESCRIPTIONS` ·
`PRISHTHODAYA_NOTE` · `RISING_DASA_HALF` · `RISING_DASA_RULE` ·
`VARNA_NAMES_EN` · `VARNA_DESCRIPTIONS` · `VARNA_ELEMENT`

| Symbol | What will consume it |
|---|---|
| `RISING_DASA_HALF`, `RISING_DASA_RULE` | Dasa result timing — §2.2.11 states the rule; nothing implements it yet |
| `DAY_NIGHT_GOVERNOR` | Divaratri bala, alongside `RASI_IS_NIGHT` |
| `DOSHA_*` | Medical astrology; reference only |
| the rest | Interpretation; reference only |

### Chapter 3 — §3.1 to §3.2.7 reference vocabulary (6)

Names, offices and stated uses. None drives a calculation; all are published on
`/v1/util/tables/grahas`.

`AVATARA_DESCRIPTIONS` · `BENEFIC_CLASS_NAMES` · `MALEFIC_CLASS_NAMES` ·
`GRAHA_DEITY_ROLE` · `GRAHA_COLOR_USE` · `SEX_PREDICTION_NOTE`

| Symbol | What will consume it |
|---|---|
| `SEX_PREDICTION_NOTE` | Sex-of-children prediction — §3.2.7 states the method; nothing implements it yet |
| the rest | Interpretation; reference only |

### Chapter 3 — §3.2.8 to §3.2.13 reference vocabulary (17)

Governance clauses, glosses, definitions and stated uses. None drives a
calculation; all are published on `/v1/util/tables/grahas`.

`ELEMENT_GOVERNANCE` · `ELEMENT_GOVERNANCE_NOTE` ·
`SHARES_ELEMENT_WITHOUT_RULING` · `SHARES_ELEMENT_PHRASE` ·
`VARNA_NAMES_EN_3_2_9` · `VARNA_FORTE` · `VARNA_MEANS_NATURE_NOT_CASTE` ·
`VARNA_CABINET_NOTE` · `GUNA_DEFINITIONS` · `SATTWA_MEANING` ·
`SATTWA_MISCONCEPTION_NOTE` · `ABODE_NOTE` · `SAPTA_DHATU_NAME` ·
`SAPTA_DHATU_NOTE` · `DHATU_DESCRIPTIONS` · `DHATU_AFFLICTION_NOTE` ·
`TIME_PERIOD_USE`

| Symbol | What will consume it |
|---|---|
| `SHARES_ELEMENT_WITHOUT_RULING` | Element-based analysis, where a sharer must not be treated as a ruler |
| `TIME_PERIOD_USE` | Prasna — §3.2.13 says the periods are for horary; nothing implements it yet |
| `DHATU_*` | Medical astrology; reference only |
| the rest | Interpretation; reference only |

### Chapter 3 — §3.2.14 to §3.3 reference vocabulary (11)

Examples, names and the dignity analogy. None drives a calculation; all are
published on `/v1/util/tables/grahas`.

`TASTE_EXAMPLES` · `TASTE_USE` · `DIG_BALA_NAME` · `DIG_BALA_NOTE` ·
`ALWAYS_STRONG_NOTE` · `RITU_RULERSHIP_NOTE` · `DHATU_MOOLA_JEEVA_MEANINGS` ·
`DIGNITY_STRONG_PLACEMENTS` · `DIGNITY_STRONG_NOTE` · `DIGNITY_ANALOGY` ·
`DIGNITY_SUBTLE_DIFFERENCE`

| Symbol | What will consume it |
|---|---|
| `DIGNITY_ANALOGY` | Result wording — §3.3 says the three good placements differ in mood; nothing acts on that yet |
| `TASTE_*` | Medical and food analysis; reference only |
| the rest | Interpretation; reference only |

### Chapter 3 — graha attributes (15)

`GRAHA_AVATARA` · `GRAHA_GOVERNS` · `GRAHA_COLOR` · `GRAHA_CABINET` ·
`GRAHA_DEITY` · `GRAHA_SEX` · `GRAHA_ELEMENT` · `GRAHA_VARNA` · `GRAHA_GUNA` ·
`GRAHA_ABODE` · `GRAHA_DHATU` · `GRAHA_TIME_PERIOD` · `GRAHA_TASTE` ·
`GRAHA_DHATU_MOOLA_JEEVA` · `RITU_RULER`

| Symbol | What will consume it |
|---|---|
| `GRAHA_SEX` | Predicting the sex of children — §3.2.7 says so outright |
| `GRAHA_TIME_PERIOD` | Prasna — §3.2.13 says "very useful in prasna or horary astrology" |
| `GRAHA_DHATU` | Medical astrology |
| `GRAHA_TASTE` | §3.2.14's dietary guidance during a dasa |
| the rest | Interpretation; reference only |

### Chapter 3 — strength rules (7)

`STRONG_AT_NIGHT` · `STRONG_BY_DAY` · `STRONG_ALWAYS` ·
`BENEFIC_STRONG_PAKSHA` · `BENEFIC_STRONG_AYANA` · `RASI_AYANA` ·
`DIG_BALA_STRONG_HOUSE`

**All seven feed shadbala**, which is Phase 2 and not built. They are the
divaratri, paksha, ayana and dig components. This is the group most likely to
surface a problem when it is finally wired up, because nothing exercises the
values today beyond asserting they match the book.

### Chapter 4 — upagraha natures (2)

`VERY_MALEFIC_UPAGRAHAS` · `MALEFIC_UPAGRAHAS`

§4.2 says of the five Sun-based upagrahas: *"Any houses occupied by them in rasi
chart or divisional charts are spoiled by them."* **That judgement is not
applied anywhere.** House analysis and yogas will need it.

### Chapter 4 — §4.1 attribution (4)

`UPAGRAHA_SOURCE` · `UPAGRAHA_NOT_PHYSICAL` · `UPAGRAHA_GROUP_COUNT` ·
`UPAGRAHA_GROUPS`

§4.1's attribution to Sage Parasara and its statement that the upagrahas are
mathematical points rather than bodies. Reference only; nothing computes from
them.

### Chapter 4 — §4.3 prose and the two footnotes (6)

`TIME_BASED_HARDER_NOTE` · `UPAGRAHA_NAME_VARIANTS` · `DAY_NIGHT_DEFINITION` ·
`PARTS_PER_PERIOD` · `LONGITUDE_REDUCTION_NOTE` · `RISE_POINT_VARIANT_NOTE`

| Symbol | What will consume it |
|---|---|
| `PARTS_PER_PERIOD` | Already implicit in `part_lords` and `part_bounds`, which hard-code 8; the constant exists so §4.3's statement has a name |
| `RISE_POINT_VARIANT_NOTE` | Footnote 9's variant is already selectable via `Settings.upagraha_rise_point`; the note records why the setting exists |
| the rest | Reference only |

### Chapter 1 — nakshatra spelling variant (1)

`NAKSHATRA_NAME_VARIANTS`

The book spells one nakshatra two ways: Table 2 (§1.3.6) prints "Swaati",
§5.7's Example 10 prints "Swathi". Reference only.

### Chapter 5 — special lagnas

Bhaava, Hora, Ghati and Sree lagna are computed on request at
`POST /v1/chart/special-lagnas`, but no other calculation reads them. §5.6 says
Hora Lagna shows money and Ghati Lagna power; §5.7 says Sree Lagna is used in
Sudasa. None of that analysis exists yet.

### Chapter 6 — significations and amsa names

`VARGA_SIGNIFICATIONS` (Table 11) and `AMSA_NAMES` are published at
`/v1/varga/rules` but no calculation reads them. §6.6 notes that yogas depend on
amsabala — "lagna lord or ghati lagna lord in Simhaasanaamsa would make one very
famous" — and no yoga engine exists yet.

### Chapter 6 — §6.6 amsabala vocabulary (6)

`AMSABALA_RULE` · `AMSABALA_IS_MONOTONIC` · `AMSABALA_DIGNITIES` ·
`VARGA_GROUP_MEANINGS` · `DASAVARGA_NOTE` · `DASAVARGA_COMBINATIONS`

§6.5's method constants are consumed by `services/varga_service.py` and are not
listed here. These six are not.

| Symbol | What will consume it |
|---|---|
| `DASAVARGA_COMBINATIONS` | §6.6.3's two yogas — lagna/GL lord in Simhaasanaamsa, quadrant lord with good amsabala. Both need the yoga chapters. See OI-54 |
| `AMSABALA_DIGNITIES` | Already implicit in `amsabala`, which counts these three; the constant names them |
| the rest | Reference only |

### Chapter 6 — §6.4 the four planes (1)

`KAARMIC_PLANE_IS_ABOVE`

§6.4 groups the twenty charts into physical (1-12), mental (13-24),
sub-conscious (25-36) and kaarmic (above 36) planes, by the number of
divisions. Nothing computes with the grouping yet; interpretation will.

### Chapter 6 — §6.2.1 and §6.2.2 reference (3)

`D1_ALIAS` · `VARGA_BODY_DEFINITION` · `D2_INCOMPLETE_NOTE`

| Symbol | What will consume it |
|---|---|
| `VARGA_BODY_DEFINITION` | The only statement that upagrahas and special lagnas belong in a divisional chart. `/v1/chart/vargas` takes graha longitudes only; extending it to any body is what this licenses |
| the rest | Reference only |

### Chapter 7 — §7.5 the house-division controversy (11)

`HOUSES_ARE_FOUND_FROM` · `NARROW_VIEW_REJECTED` · `BHAAVA_CHAKRA_DEFINITION` ·
`EQUAL_HOUSE_DEFINITION` · `EQUAL_HOUSE_IS_POPULAR` · `SRIPATHI_METHOD_NOTE` ·
`EACH_RASI_IS_A_HOUSE` · `BPHS_HOUSE_DIVISION_ARGUMENT` ·
`RASI_AND_VARGA_ARE_NOT_DIFFERENTIATED` · `IGNORE_OTHER_HOUSE_DIVISION_METHODS` ·
`ARGALA_STHANA_FORWARD_REFERENCE`

§7.5 settles a question the engine already answers: the default house system is
whole sign and `house_of_rasi` counts rasis from the chosen reference. These
record the argument, not a new calculation.

| Symbol | What will consume it |
|---|---|
| `BPHS_HOUSE_DIVISION_ARGUMENT` | Consumed as policy: it is tie-break rule 4 in `docs/precedence.md` |
| `ARGALA_STHANA_FORWARD_REFERENCE` | Chapter 10, "Aspects and Argalas" |
| the rest | Reference only — they describe rejected methods |

### Chapter 7 — §7.4.2 to §7.4.6 (18)

`MAHA_VISHNU_EPITHET` · `QUADRANT_ABODE` · `QUADRANT_IS_SUSTENANCE` ·
`QUADRANT_HOUSE_REASONS` · `QUADRANTS_SUSTAIN_EACH_OTHER` ·
`MUTUAL_QUADRANTS_RULE` · `MUTUAL_QUADRANTS_DEFINITION` ·
`MUTUAL_TRINES_DEFINITION` · `UPACHAYA_RULE` · `UPACHAYA_EXAMPLE` ·
`DUSTHANA_RULE` · `DUSTHANA_STRENGTH_INVERSION` ·
`DUSTHANA_STRENGTH_EXAMPLE` · `HALVES_RULE` · `HALVES_ARE_IN_EVERY_CHART` ·
`HALVES_EXPLAIN_THE_TRIKONA_BASES` · `QUICK_SUMMARY` · `ARGALA_STHANA_SHOWS`

The category tables and both halves are consumed; these are §7.4's prose,
its two footnote definitions and its summary.

| Symbol | What will consume it |
|---|---|
| `DUSTHANA_STRENGTH_INVERSION`, `DUSTHANA_STRENGTH_EXAMPLE` | A strength-aware house reading — see OI-58 |
| `MUTUAL_QUADRANTS_RULE` | Planet-to-planet relations; nothing computes mutual-quadrant pairs yet |
| `UPACHAYA_EXAMPLE` | A worked reading from arudha lagna; the pieces exist, nothing joins them |
| `ARGALA_STHANA_SHOWS`, the fifth `QUICK_SUMMARY` row | Argalas, chapter 10, unaudited |
| the rest | Reference only |

### Chapter 7 — §7.4.1 trines and purushaarthas (10)

`TRINE_ABODE` · `TRINE_IS_BENEFICIAL` · `PURUSHARTHA_TRIKONA_NAMES` ·
`PURUSHARTHA_HOUSE_REASONS` · `DHARMA_IS_DECIDED_BY` ·
`DHARMA_LITERAL_MEANING` · `DHARMA_NOTE` · `PURUSHARTHA_STRENGTH_RULE` ·
`TRIKONA_DASA_NOTE` · `MUTUAL_TRINES_RULE`

The purushaartha trikona table itself is consumed by the house service.
These ten are §7.4.1's names, reasons and two forward references.

| Symbol | What will consume it |
|---|---|
| `PURUSHARTHA_STRENGTH_RULE` | Digbala joined to the purushaartha trikonas — see OI-57 |
| `TRIKONA_DASA_NOTE` | Trikona Dasa, a rasi dasa; `dasha/rasi/` is empty |
| `MUTUAL_TRINES_RULE` | Planet-to-planet relations in a chart; nothing computes mutual-trine pairs yet |
| the rest | Reference only |

### Chapter 7 — §7.4 and footnote 14 (5)

`DUSTHANA_GLOSS` · `CATEGORIES_ARE_RELATIVE` · `CATEGORIES_FROM_THIRD_HOUSE` ·
`THREE_CHARTS_FOR_SPEECH_NOTE` · `SPEECH_CHART_ROLES`

The seven categories and their relative computation are consumed by
`charts/house.py` and `services/house_service.py`. These are §7.4's prose and
footnote 14's per-chart roles.

| Symbol | What will consume it |
|---|---|
| `SPEECH_CHART_ROLES` | Multi-chart reading — footnote 14 is the only place the book says what each of three charts contributes to one matter |
| `CATEGORIES_FROM_THIRD_HOUSE` | The book's own worked answers; the relative computation reproduces all four |
| the rest | Reference only |

### Chapter 7 — §7.3.9 graha lagnas (7)

`GRAHA_LAGNA_NAME` · `GRAHA_LAGNA_ALIAS` · `GRAHA_LAGNA_RULE` ·
`GRAHA_LAGNA_PAIRS` · `GRAHA_LAGNA_STRENGTH_RULE` ·
`NAISARGIKA_REFERENCE_RULE` · `NAISARGIKA_REFERENCE_EXAMPLES`

Table 12 itself was already stored. These are §7.3.9's rule, its six worked
pairs and the naisargika extension.

| Symbol | What will consume it |
|---|---|
| `GRAHA_LAGNA_STRENGTH_RULE` | Choosing between a house from lagna and the same house from its graha. Needs a graha-versus-lagna strength comparison — see OI-56 |
| `GRAHA_LAGNA_PAIRS` | The six matters the book reads from two references each |
| `NAISARGIKA_REFERENCE_EXAMPLES` | Open-ended reference selection by natural significator; both cases name their divisional chart |
| the rest | Reference only |

### Chapter 7 — §7.3.6 to §7.3.8 and footnote 13 (10)

`KARAKAMSA_REASON` · `KARAKAMSA_DEFINITION` · `KARAKAMSA_TWELFTH_RULE` ·
`KARAKAMSA_MOKSHA_HOUSE` · `KARAKAMSA_MOKSHA_GRAHA` · `GHATI_LAGNA_SHOWS` ·
`GHATI_LAGNA_USED_FOR` · `HORA_LAGNA_SHOWS` · `HORA_LAGNA_USED_FOR` ·
`TRANSIT_DEFINITION`

The karakamsa *calculation* is consumed — `charts/house.py:karakamsa_rasi`
computes it and the reference now resolves. These are the statements around it.

| Symbol | What will consume it |
|---|---|
| `KARAKAMSA_TWELFTH_RULE` | Needs a strength measure over the 12th house's occupants (chapter 15) joined to the graha deities (chapter 3). Nothing joins them yet |
| `KARAKAMSA_MOKSHA_HOUSE`, `KARAKAMSA_MOKSHA_GRAHA` | The same rule's two operands |
| `TRANSIT_DEFINITION` | The transit chapters |
| the rest | Reference only; both echo chapter 5's significations |

### Chapter 7 — §7.3.3 to §7.3.5 reference vocabulary (13)

`RAVI_LAGNA_REASON` · `RAVI_LAGNA_SHOWS` · `RAVI_LAGNA_ALSO` ·
`ARUDHA_LAGNA_SHOWS` · `PAAKA_LAGNA_DEFINITION` · `PAAKA_LAGNA_SHOWS` ·
`PAAKA_LAGNA_REASON` · `PAAKA_LAGNA_USED_IN` · `PAAKA_LAGNA_EXAMPLES` ·
`LAGNA_IS_CONCEPTUAL` · `TENTH_HOUSE_BY_REFERENCE` ·
`FIFTH_HOUSE_IN_D24_BY_REFERENCE` · `SATURN_TRANSIT_BY_REFERENCE`

The paaka lagna *calculation* is consumed — `charts/house.py:paaka_lagna_rasi`
computes it and both of §7.3.5's worked cases reproduce. These are the
statements about what each reference **means**, which nothing selects on yet.

| Symbol | What will consume it |
|---|---|
| `FIFTH_HOUSE_IN_D24_BY_REFERENCE` | Reference selection — the book's clearest worked case: one house, one chart, three matters, three references |
| `TENTH_HOUSE_BY_REFERENCE` | The same, for the 10th house |
| `SATURN_TRANSIT_BY_REFERENCE` | Transit reading, which is a later chapter |
| `RAVI_LAGNA_ALSO` | Vitality analysis; §7.3.3 makes the Sun a second reference for it |
| the rest | Reference only |

### Chapter 7 — §7.3 reference vocabulary (9)

`THREE_CHOICES_RULE` · `FOURTH_HOUSE_BY_VARGA` ·
`HOUSE_DIFFERS_BY_REFERENCE_EXAMPLE` · `MANY_PARAMETERS_NOTE` · `LAGNA_SHOWS` ·
`LAGNA_SPIRIT_OF_I` · `LAGNA_NOT_FOR_STATUS` · `LAGNA_SEEN_FROM` ·
`CHANDRA_LAGNA_REASON` · `CHANDRA_LAGNA_NOT_IGNORED` · `CHANDRA_LAGNA_EXAMPLE` ·
`CHANDRA_LAGNA_SHOWS`

§7.3's choose-meaning-by-varga rule is consumed by
`services/house_service.py` and is deliberately absent from the list
above — naming it in backticks here would make the register guard read it
as listed.

Note the Chandra Lagna signification exists twice with different wording:
the §7.3.2 constant says "things from the perspective of mind" (the
book's word) while the references table says "matters". The first is the
transcription; the second is our own summary for the table.

| Symbol | What will consume it |
|---|---|
| `LAGNA_NOT_FOR_STATUS` | Reference selection — §7.3.1 says status must be read from arudha lagna, not lagna. Nothing chooses a reference by matter yet |
| `FOURTH_HOUSE_BY_VARGA` | The book's own four cases; `meanings_in_varga` reaches three of them |
| the rest | Reference only |

### Chapter 7 — §7.1 and §7.2 method (5)

`HOUSE_REFERENCE_RULE` · `HOUSE_MEANING_DEPENDS_ON_REFERENCE` ·
`HOUSE_MEANING_DEPENDS_ON_VARGA` · `HOUSES_FROM_HOUSES_EXAMPLES` ·
`HOUSE_RESULTS_REFERENCE`

§7.1's statements that a house's meaning depends on both the reference and the
divisional chart. Neither axis is applied yet — nothing varies a signification
by reference or by varga.

| Symbol | What will consume it |
|---|---|
| `HOUSE_MEANING_DEPENDS_ON_REFERENCE` | Arudha-relative readings; the 11th from AL differs from the 11th from lagna |
| `HOUSE_MEANING_DEPENDS_ON_VARGA` | Per-varga house meanings; the 4th in D-16 differs from the 4th in D-24 |
| `HOUSES_FROM_HOUSES_EXAMPLES` | The three worked derivations; `house_service.derived` computes them, these are the book's own cases |
| the rest | Reference only |

### Chapter 7 — house significations and categories

**This section used to list the four chapter-7 house tables — the
significations, the categories, the purushartha trikonas and the graha lagna
houses — as unconsumed. That was wrong**: `charts/house.py` reads all four.
(Their names are deliberately spelled out in prose here rather than in code
formatting, because the register's own test treats a backticked symbol as a
live claim that it is unconsumed.) The claim survived because the old
hand-typed `TRACKED` list did not include them, so the test that checks the
register never looked. Corrected when `TRACKED` was made automatic.

`MARAKA` is *consumed* — `classify_house` reports it in every chart
response — but is **unverified against the book**. See
[open-items.md](open-items.md#oi-23).

### Benefic/malefic classification — now consumed

The two natural benefic/malefic lists became consumed when chapter 15's
avastha engine landed: `charts/avastha.py` needs them for Vikala ("joined by
malefic planets"), Khala ("in a malefic planet's rasi"), Trishita ("without
the aspect of benefics") and Kshobhita.

Still true, and still a gap: §3.2.2's conditional cases — Mercury turning
benefic or malefic by association, and the Moon by paksha — are **not
implemented at all**, only the unconditional lists. Every avastha above is
therefore judged on the unconditional classification.

### Calendar (1)

`SAMVATSARA_NAMES` — the sixty-year Jovian cycle. Nothing computes which
samvatsara a date falls in.

---


### Reference vocabulary — names, spellings and glosses (82)

Reachable through the API — mostly `/v1/util/tables/*` and `/v1/reference/*`,
some through the rules endpoint of their own chapter, such as
`/v1/house/rules`. No calculation reads any of them; they exist so the API can
name things the way the book does.

**This heading is a claim, and it is tested.** Twenty of these once sat here
while being published nowhere — seventeen were not even re-exported from
`hora.core.const`, and three more were returned by a service but stripped by
its Pydantic response model. `tests/unit/test_register_claims.py` now asserts,
per constant, that it is on the facade and that its content appears in some
`/v1/util/*` or `/v1/reference/*` response. Adding a name here without wiring
it up fails the suite. See [open-items.md](open-items.md#oi-31).

`SOLAR_YEAR_DEGREES` · `SOLAR_MONTH_DEGREES` · `SOLAR_DAY_DEGREES` · `DAYS_PER_SOLAR_MONTH` · `SOLAR_CALENDAR_USED_IN` ·
`NAKSHATRA_COUNT` · `NAKSHATRA_COUNT_SPECIAL` · `PADAS_PER_NAKSHATRA` · `PADA_GLOSS` · `TWENTY_EIGHT_NAKSHATRA_CHARTS` · `ABHIJIT_RULE` ·
`VARGA_CHAKRA_NAME` · `VARGA_ALIASES` · `VARGA_DEFINITION` · `VARGA_SIGNIFIES_AN_AREA` · `VARGA_INDEPENDENT_CHART_RULE` · `FOUR_PILLARS` · `FOUR_PILLARS_CONCLUSION_ORDER` ·
`BHAVA_NAME` · `HOUSE_DEFINITION` · `HOUSE_ORDER_WRAPS` · `HOUSE_COMMON_REFERENCES` · `HOUSE_DEFAULT_REFERENCE` · `HOUSE_DEFAULT_REFERENCE_RULE` ·
`GRAHA_DEFINITION` · `GRAHA_DEFINITION_NOTE` · `NODES_ARE_MATHEMATICAL_POINTS` · `UPAGRAHA_DEFINITION` · `UPAGRAHA_GLOSS` · `UPAGRAHA_COUNT` · `LAGNA_DEFINITION` · `SPECIAL_ASCENDANT_TERM` ·
`GRAHA_ABBR` · `GRAHA_NAMES_SA` · `RASI_NAMES_SA` · `RASI_NAMES_SA_BOOK` ·
`DIRECTION_NAMES` · `DOSHA_NAMES` ·
`ELEMENT_NAMES_SA` · `ELEMENT_SHARERS` · `GUNA_NAMES` ·
`GUNA_ADJECTIVES` · `VARNA_NAMES` · `SEX_NAMES` · `RISING_NAMES` ·
`AYANA_NAMES` · `RITU_NAMES` · `RITU_MEANINGS` · `RITU_MONTHS` ·
`FOOTED_NAMES` · `ZODIAC_NAMES` · `ZODIAC_USED` · `NAKSHATRA_DEITY` ·
`PANCHANGA_NAME_BOOK` · `PANCHANGA_MEANING` ·
`PANCHANGA_ALMANAC_NAME` · `PURUSHARTHA_NAME_BOOK` · `PURUSHARTHA_MEANING` ·
`PLANET_ELEMENT_NAMES` · `PLANET_ELEMENT_NAMES_SA` ·
`DHATU_MOOLA_JEEVA_NAMES` · `ESSENCE_NAMES` · `ESSENCE_ALIASES` ·
`AVATARA_ALIASES` · `PURE_PARAMATMAMSA_AVATARAS` · `NODE_ALIASES` ·
`CHAAYAA_GRAHAS` · `CHAAYAA_GRAHA_NAME` · `UPAGRAHA_ALIASES` ·
`RELATIONSHIP_KINDS` · `COMPOUND_RELATION_NAMES` ·
`COMPOUND_RELATION_GLOSSES` · `DIGNITY_NAMES_SA`

**Three left this list in chapter 11.** The element-ruler table and the two
tattva name lists were transcribed from §3.2.8 and sat here unconsumed. §11.4's
Pancha Mahapurusha yogas read them — each yoga takes its ruler's element — so
they are now consumed by a calculation eight chapters later. That is the
register working as intended: a constant recorded early, consumed when the book
finally uses it.

Most were added by the inverted coverage sweep (see
[page-sweep.md](page-sweep.md)), which found the book naming things the code
had no word for. They are reference data by design and may stay unconsumed
indefinitely — being listed here is the normal state, not a defect.

### Tables a calculation duplicates rather than imports (12)

These are verified and correct, but the code that needs them defines its own
copy instead of importing these. **Two sources of truth for the same table.**
Nothing is wrong today — `test_vimshottari_tables_agree` pins the pair that
matters — but a future edit to one side would silently diverge.

`VIMSHOTTARI_ORDER` · `VIMSHOTTARI_YEARS` · `NAKSHATRA_LORD` ·
`TABLE_10_DAY` · `TABLE_10_NIGHT` · `TIME_BASED_UPAGRAHAS` ·
`MALEFIC_STRONG_AYANA` · `MALEFIC_STRONG_PAKSHA` · `CO_LORDS_ONLY` ·
`DEBILITATION_DEG` · `CHATURASRA` · `ABHIJIT_INDEX`

`dasha/nakshatra/systems.py` carries its own `order` and `years` for
Vimshottari; `constants/nakshatra.py` carries `VIMSHOTTARI_ORDER` and
`VIMSHOTTARI_YEARS`. They agree today, verified. Deduplicating them is a
behaviour-affecting refactor and is **not** being done unilaterally — raised as
a decision, not a change.

### Provenance declarations (5)

`VERBATIM_FIELDS` · `VERBATIM_CONSTANTS` · `AVASTHA_VERBATIM_FIELDS` ·
`AVASTHA_VERBATIM_CONSTANTS` · `DASHA_VERBATIM_CONSTANTS`

Not data — a declaration of *which* chapter-8 and chapter-15 strings are the author's words
and which are our summary. No calculation reads them; they exist so that
`test_declared_verbatim_fields_are_verbatim` can hold the line against a
paraphrase drifting into a field that claims to be a transcription.

They belong in `core/constants/` rather than in the test, because the claim
travels with the data. A constant moved to another module should carry its
provenance with it.

Expected to stay unconsumed. If chapters 9 onward adopt the same pattern, these
should generalise rather than multiply.

## Separate concern: premature, unverified code

### `src/hora/charts/aspects.py` — one function still premature

Written during Phase 1 scaffolding from general knowledge, before the
four-check standard existed. Three of its four public functions have since been
derived from the book:

| Function | Status |
|---|---|
| `rasi_drishti` | Corrected against §15.5.1's worked example; imported by `charts/colord.py`. All three offset rows had been wrong — see OI-27, closed |
| `graha_drishti_houses` | **Verified against chapter 10** — §10.2's rules, Example 34, Exercise 14's whole answer table. Wired into `services/aspect_service.py` |
| `graha_aspects_sign` | Same |
| `drishti_value` | **Still premature.** The virupa partial-aspect table for drik bala and ashtakavarga. Chapter 10 does not derive it, nothing imports it, and it has never been checked against PVR |

`test_only_rasi_drishti_is_used_from_the_aspects_module` keeps `drishti_value`
unimported until a chapter derives it. Its tables should be treated as a draft.
Tracked as [OI-18](open-items.md#oi-18).

### Chapter 11 — §11.5.4's worked example (1)

`SANKHYA_EXAMPLE`

Lord Sri Rama's chart, from §11.5.4. Figure 1 **was** supplied — it is
§1.3.4's own Example 1, and `tests/unit/test_book_1_3_4.py` has held it as a
fixture since chapter 1 was audited. So the example is fully checkable, lagna
included, and chapter 11's test imports chapter 1's fixture rather than
restating it.

| Symbol | What will consume it |
|---|---|
| `SANKHYA_EXAMPLE` | Nothing until Figure 1 arrives; then it becomes a chart fixture like Charts 5 to 8 |

### Chapter 10 — Exercise 17's technique (2)

`STRENGTH_CRITERIA_USED` · `KARAKA_SIGN_ELEMENT_READING`

Two techniques Exercise 17 uses that chapter 10 never defines.

| Symbol | What will consume it |
|---|---|
| `STRENGTH_CRITERIA_USED` | Chapter 15's simple-rules strength measure — own house, most advanced, co-owner tie-break. See OI-72 |
| `KARAKA_SIGN_ELEMENT_READING` | Reading a karaka's own sign element before its argalas; chapter 2 supplies the elements, nothing joins them to a karaka |

### Chapter 10 — Example 35's premise (2)

`EXAMPLE_35_PREMISE` · `EXAMPLE_35_RULE`

Example 35 asserts a karakatwa chapter 8 does not carry — Saturn for
livelihood and karma. Held here as the example's own claim rather than added
to Tables 15 or 16, which are transcribed. See OI-69.

| Symbol | What will consume it |
|---|---|
| both | Nothing, unless OI-69 settles that the karaka tables may be extended from worked examples |

### Chapter 10 — §10.7 worked instances (1)

`ARGALA_ROLE_EXAMPLES`

§10.7's seven worked instances of the four roles. The role table itself and
the procedure are consumed by `services/argala_service.py`; these are the
examples that demonstrate them.

| Symbol | What will consume it |
|---|---|
| `ARGALA_ROLE_EXAMPLES` | Nothing computes it — each instance names what a house *means* for a matter, and the engine assigns no meanings. §10.7 step 5 says "guess", and nothing here guesses |

### Chapter 10 — §10.5 prose and worked examples (6)

`ARGALA_IS_ADDITIONAL` · `ARGALA_IS_IMPORTANT` · `ARGALA_EXAMPLES` ·
`SECONDARY_ARGALA_EXAMPLES` · `ARGALA_NATURE_EXAMPLE` ·
`ARGALA_NATURE_SPELLING_VARIANTS`

§10.5's framing and its five worked readings. The rules they illustrate —
primary/secondary, the pairing, the nature naming — are all consumed by
`services/argala_service.py`; these are the prose around them.

| Symbol | What will consume it |
|---|---|
| `ARGALA_EXAMPLES`, `SECONDARY_ARGALA_EXAMPLES` | Nothing computes them: they name what each argala house *means* for a matter, and the engine assigns no meanings. A reading layer would |
| `ARGALA_NATURE_SPELLING_VARIANTS` | Text matching against the book; the engine uses the definitional spellings |
| the rest | Reference only |

### Chapter 10 — §10.6 worked examples (2)

`VIRODHARGALA_EXAMPLE` · `KETU_NOTE_EXAMPLE`

§10.6's two worked examples. Both are reproduced by
`tests/unit/test_book_chapter10_argala.py`; nothing in `src/` reads them,
because the computation they demonstrate is driven by the pairing table and
the Ketu reversal rather than by the examples themselves.

| Symbol | What will consume it |
|---|---|
| `VIRODHARGALA_EXAMPLE` | Nothing — a test fixture holding the example's placements and its printed text |
| `KETU_NOTE_EXAMPLE` | Likewise, for the anti-zodiacal note |

### Chapter 10 — §10.1 to §10.3 (3)

`GRAHA_DRISHTI_HEADING_AS_PRINTED` · `SEVENTH_HOUSE_EXAMPLES` ·
`RASI_DRISHTI_EXAMPLES`

Everything else chapter 10 added is consumed by `services/aspect_service.py`.

| Symbol | What will consume it |
|---|---|
| `GRAHA_DRISHTI_HEADING_AS_PRINTED` | Nothing — it records the heading's misprint ("Graha Drishri") so it is not mistaken for a term |
| `SEVENTH_HOUSE_EXAMPLES` | §10.2's five one-line examples; test fixtures, not a calculation |
| `RASI_DRISHTI_EXAMPLES` | §10.3's three worked examples, one per rule; likewise fixtures |

---

### Chapter 15 — §15.4.4's "Importance of Sayanaadi Avasthas" (2)

`SAYANAADI_ARE_MOST_IMPORTANT` · `SAYANAADI_CAUTION`

The eight special results themselves are consumed by
`charts/avastha.special_results`. These two are the passages around them.

| Symbol | What will consume it |
|---|---|
| `SAYANAADI_ARE_MOST_IMPORTANT` | The section's ranking of this family over the other three; a note for a reading, not a calculation |
| `SAYANAADI_CAUTION` | The closing warning, which qualifies every avastha result. Whether it may be served verbatim is the OI-12 licence question — see the note below |

Section 15.4.1's caution is already served verbatim by
`services/strength_service` while the author's result lines beside it are
withheld under OI-12. That is inconsistent, and it is why the caution above is
parked here rather than wired the same way: widening the practice before the
inconsistency is settled would be the wrong order.

---

### Part 2 — the dasa systems map and chapters 16-19's prose (61)

`PART_2_DASA_SYSTEMS` · `DASA_USES_ARE_NOT_IN_THE_CLASSICS` ·
`DEFERRED_TO_TAJAKA` · `VARIATIONS_ARE_OFTEN_IGNORED` · `DASA_FROM_LAGNA` ·
`DASA_LORD_AS_TEMPORARY_LAGNA` · `VIMSOTTARI_READING_EXAMPLES` ·
`NO_GUIDELINES_FOR_SIGN_STRENGTH` · `STAR_SPANNING_TWO_SIGNS` ·
`TRIPOD_OF_LIFE` · `TRIPOD_PRINCIPLE` · `USE_THE_VARIATIONS` ·
`KENDRADI_GRAHA_DASA_INSTEAD` · `DASA_ERROR_RULE` ·
`ASHTOTTARI_IS_CONDITIONAL` · `ASHTOTTARI_MEANS_108` ·
`ASHTOTTARI_HAS_NO_KETU` · `ASHTOTTARI_ANTARDASA_RULE` ·
`ASHTOTTARI_APPLICABILITY_VIEWS` ·
`ANTARDASA_SEED_BY_LORDS_UNQUANTIFIED` ·
`PARASARA_DASA_PRINCIPLES` · `NATAL_REFERENCE_READINGS` ·
`DASA_THIRDS` · `ANTARDASA_RESULT_RULE` · `MUNDANE_HOUSE_READINGS` ·
`UNLISTED_DASA_LAGNA_READINGS` · `ANTARDASA_ASPECT_RULE` ·
`EXALTED_DUSTHANA_LORD_CONVERSE` · `KETU_IN_THE_ELEVENTH_IS_FOREIGN` ·
`VARGA_SEED_RATIONALE` · `VARGA_DASA_USES` ·
`VARGA_DIGNITY_IS_READ_IN_THE_VARGA` · `NAVAMSA_MARRIAGE_DASA_RULES` ·
`MARRIAGE_TROUBLE_NEEDS_CORROBORATION` · `PRATYANTARDASA_RULE` ·
`ANTARDASA_CANDIDATE_BY_CONTENTS` · `CAREER_DASA_READINGS` ·
`AFFLICTED_KARAKA_IN_THE_DASA_RASI` · `VARGA_HOUSE_FRAME_DOES_NOT_ROTATE` ·
`ARUDHA_PADA_DASA_READINGS` · `ARUDHA_SHOWS_THE_APPEARANCE_OF_ITS_MATTER` ·
`DASA_LEVEL_BY_EVENT_DURATION` · `CHOOSE_THE_DASA_LEVEL_BY_THE_EVENT` ·
`MAHADASA_AND_ANTARDASA_COEXIST` · `SOLAR_ARC_IS_REQUIRED_FOR_CORRECT_RESULTS` ·
`SOLAR_ARC_REFERENCE_SOFTWARE` · `SEED_CHOICE_READINGS` ·
`NARAYANA_IS_THE_MOST_IMPORTANT_PHALITA_DASA` · `MOOLA_DASA_OUT_OF_SCOPE` ·
`MOOLA_DASA_WHEN_IT_IS_BETTER` · `SHOWS_MATERIAL_SUCCESS` ·
`PARASARA_MOVEMENT_RULERS` · `LAKSHMI_SHOWS_PROSPERITY` ·
`SUDASA_IS_KENDRADI_FROM_SREE_LAGNA` · `SUCCESS_READINGS` ·
`WHY_AMK_ARGALA_GIVES_POWER` · `STRONGER_CO_LORD_IS_NOT_THE_LORD` ·
`SUDASA_IS_SUPERIOR` · `GATI_NAMES` · `MANDOOKA_DASA_MISATTRIBUTION` ·
`MANDOOKA_DASA_IS_OF_RUDRAMSA`

Part 2 opens by classifying dasa systems two ways and naming the nine it will
teach. That is a roadmap rather than a calculation, so nothing computes from
it — but it is the coverage line for the whole part, and
`tests/unit/test_book_part2_dasa_map.py` holds it against what is built.

| Symbol | What will consume it |
|---|---|
| `PART_2_DASA_SYSTEMS` | Nothing computes from it. It exists so that two of nine systems built is a visible number rather than an impression |
| `DASA_USES_ARE_NOT_IN_THE_CLASSICS` | The part's own explanation for why no classic settles which dasa to use when; context for a reading, not an input |
| `DEFERRED_TO_TAJAKA` | Records that Sudarsana Chakra dasa is named here and taught elsewhere, so its absence from Part 2 is deliberate |
| `VARIATIONS_ARE_OFTEN_IGNORED` | §16.4.1's reason for having the kshema/utpanna/adhana variations at all. The variations themselves are consumed — `/v1/dasha` takes `start_star` — but the caution is prose |
| `DASA_FROM_LAGNA` | §16.4.2's caveat, that lagna reckoning helps only when lagna is much stronger than Moon. The reckoning is consumed — `/v1/dasha` takes `reckon_from` — but comparing the two strengths is a judgement the section leaves to the reader |
| `DASA_LORD_AS_TEMPORARY_LAGNA` | §16.5.1's closing technique. Needs an interpretation layer that re-reads the charts from a moving lagna; nothing computes from it yet |
| `VIMSOTTARI_READING_EXAMPLES` | §16.5.1's nine illustrations. The section calls them "just a few examples", so they are deliberately not a lookup table — they will feed a reading layer, not a predictor |
| `NO_GUIDELINES_FOR_SIGN_STRENGTH` | §16.5.2's own admission that the sign comparison it depends on is undefined. Nothing consumes it because nothing may: `variation_candidates` returns the candidate signs and refuses to pick |
| `STAR_SPANNING_TWO_SIGNS` | §16.5.2's pada rule as printed. The rule itself is implemented in `variation_sign`; this is the sentence it came from |
| `MUNDANE_HOUSE_READINGS` | Example 69's four house significations read for a nation rather than a person. §18.4's principles give a placement's valence and these give its subject; an interpretation layer needs both, and neither exists yet. **OI-122** |
| `UNLISTED_DASA_LAGNA_READINGS` | Two readings Example 69 gives that §18.4's sixteen principles do not reach — a conglomeration in the 12th, and Rahu in the 10th. Recorded rather than folded into the principles, which are Parasara's and closed. **OI-122** |
| `ANTARDASA_ASPECT_RULE` | Example 69's second way to read an antardasa: the antardasa rasi's aspect on a natal arudha. `rasi_drishti` and `arudha_pada` both exist, so only the reading layer is missing. **OI-122** |
| `EXALTED_DUSTHANA_LORD_CONVERSE` | Exercise 28 applies §18.4's principle 13 in reverse — an **exalted** dusthana lord giving hard times, where the principle states only the debilitated case. Kept apart from the sixteen, which are Parasara's and closed. **OI-122** |
| `KETU_IN_THE_ELEVENTH_IS_FOREIGN` | Principle 5 gives any planet in the 11th "gains"; Example 69 and Exercise 28 both make Ketu's specifically foreign. A reading layer needs the narrower sense, not just the valence. **OI-122** |
| `VARGA_SEED_RATIONALE` | §18.5's account of why each varga has the seed house it has — dharma for D-9, karma for D-10, the evolution of self for D-12 and D-24. `seed_house` computes the houses; these are the meanings behind them, and a test holds the two together |
| `VARGA_DASA_USES` | §18.5 names what six vargas' Narayana dasas time — career, marriage, children, residence, learning, parents. Choosing which varga answers a question is a reading, not a calculation; nothing selects one yet |
| `VARGA_DIGNITY_IS_READ_IN_THE_VARGA` | Example 71's note (1), which is the only place the book shows that a varga dasa's lengths take their dignities from the varga. `dasa_length` takes dignity from its caller, so this is the sentence that tells a caller which chart to read |
| `NAVAMSA_MARRIAGE_DASA_RULES` | Example 72's five readings for a navamsa dasa and marriage, counted from the navamsa's lagna and from UL. `arudha_pada` and `varga_house` compute both references; what is missing is a layer that reads them. **OI-122** |
| `MARRIAGE_TROUBLE_NEEDS_CORROBORATION` | The qualification Example 72 puts on both unfavourable readings — "when the chart has such indications". It stops the rule being read as a prediction, so any layer consuming the rules must carry it |
| `PRATYANTARDASA_RULE` | Example 71's derivation of the third dasa level. `pratyantardasas` computes the sequence; the sentence records that the book states no new rule for it, only §18.3 applied one rasi down |
| `ANTARDASA_CANDIDATE_BY_CONTENTS` | Example 73's third way to read an antardasa — by what its rasi holds, rather than by its lord's house or by what it aspects. The contents are computable; choosing among candidates on their strength is the reading. **OI-122** |
| `CAREER_DASA_READINGS` | Example 74's four readings for a D-10 dasa, counted from the varga lagna, the arudha lagna and the satru pada A6. `varga_house` and `arudha_pada` compute every reference; the reading layer is what is missing. **OI-122** |
| `AFFLICTED_KARAKA_IN_THE_DASA_RASI` | Example 74's Sun-with-Rahu reading — a karaka afflicted in the dasa rasi itself, which is neither a house nor a lordship and so reaches nothing in §18.4. **OI-122** |
| `VARGA_HOUSE_FRAME_DOES_NOT_ROTATE` | Why §18.4's occupancy principles say the same thing in every dasa of a varga: with no dasa lagna the house frame is the varga's own ascendant and never moves. A reading layer has to know this before it applies the sixteen to a varga at all |
| `ARUDHA_PADA_DASA_READINGS` | The six arudhas chapter 18 reads a dasa by — A1, A3, A6, A9, A10 and UL. `arudha_pada` computes every one; what is missing is the layer that reads a dasa of one. **OI-122** |
| `ARUDHA_SHOWS_THE_APPEARANCE_OF_ITS_MATTER` | Exercise 30's statement of the principle behind all six, which the chapter had used since Example 68 without saying. It also records that the meaning narrows to the chart the arudha is read in |
| `DASA_LEVEL_BY_EVENT_DURATION` | Example 75's five dasa levels against how long an event matters. The first three are computed — `antardasas` and `pratyantardasas` — but choosing which to read is the reading layer's job, and the last two have no lengths at all |
| `CHOOSE_THE_DASA_LEVEL_BY_THE_EVENT` | The rule itself, and the only place praana-antardasa and deha-antardasa are named. It gives them neither a length nor an order, so nothing computes them; a reading layer needs it before it treats pratyantardasa as the floor |
| `MAHADASA_AND_ANTARDASA_COEXIST` | Example 75's demonstration that two levels can say opposite things at once and neither cancels the other — ten good years with one bad ten-month period inside them. A reading layer must not resolve them into one verdict |
| `SOLAR_ARC_IS_REQUIRED_FOR_CORRECT_RESULTS` | §18.6's warning that only the solar-arc measure gives correct sub-periods. `sub_period_arc` and `solar_arc_instant` implement it; the sentence is why, and it is the one that withdrew D-58 |
| `SOLAR_ARC_REFERENCE_SOFTWARE` | PVR's own free program, which divides a mahadasa to deha-antardasa level by the same measure. A tier-2 check we could run one day, and it names the inputs the division needs |
| `SEED_CHOICE_READINGS` | §18.7's three named seedings and what each shows. `varga_lagna` takes the seed house, so all three compute; which to run for a question, and whether the answer is native-centric or direct, is the reading |
| `NARAYANA_IS_THE_MOST_IMPORTANT_PHALITA_DASA` | §18.7's assessment of the system and its instruction to master it. Nothing computes from an assessment; it is here so the chapter's closing claim is on the record with the rest |
| `MOOLA_DASA_OUT_OF_SCOPE` | §19.1 describes Kendradi Graha Dasa, or Moola dasa, in full and then declines to teach it. Recorded so its absence is visibly deliberate rather than an oversight, and so a reader meeting the name elsewhere finds the book's position |
| `MOOLA_DASA_WHEN_IT_IS_BETTER` | §19.1's one testable claim about it — four planets in quadrants from the stronger of lagna and Moon. Nothing consumes it because Moola dasa is not built, but it is the condition under which it would matter |
| `SHOWS_MATERIAL_SUCCESS` | §19.1's statement of what Lagna Kendradi Rasi Dasa is *for*. Narayana is general-purpose (§18.6); this one is narrow, and a reading layer choosing between them needs that |
| `PARASARA_MOVEMENT_RULERS` | §19.3's attribution of quadrants to Vishnu and trines to Lakshmi. `movement_grouping` computes which movement a house order is and names its ruler; this is the pairing that gives the answer meaning |
| `LAKSHMI_SHOWS_PROSPERITY` | Why the Kendradi walk is the one for prosperity. A reading layer choosing between the two rasi dasas needs the reason, not just the label |
| `SUDASA_IS_KENDRADI_FROM_SREE_LAGNA` | §19.3's forward reference — Sudasa is this dasa seeded from Sree Lagna. `sree_lagna` and `progression` both exist, so Sudasa is a seed away; the chapter that teaches it has not arrived |
| `SUCCESS_READINGS` | Chapter 19's only four reading rules, all from Example 76 — AK in the rasi, an unobstructed AmK argala, GL in the rasi, the lagna lord there. Every input computes (`chara_karakas`, `argalas_on_sign`, `special_lagna`); the layer that applies them does not exist |
| `WHY_AMK_ARGALA_GIVES_POWER` | The reason behind the AmK rule. A layer that gives the verdict without it claims more than the book does — the argala shows the *company of advisors*, from which power is inferred |
| `STRONGER_CO_LORD_IS_NOT_THE_LORD` | Example 76 says "lagna lord Mars" of a Scorpio lagna while the same chart's dasa length and arudha go to Ketu. Records that §15.5.1 answers only where a rule sends it, which is what D-4 assumed when it left the primary-lord table alone |
| `SUDASA_IS_SUPERIOR` | §19.4 ranks Sudasa above this dasa for the matter both read. A layer weighing the two rasi dasas needs the ordering, and it is the book's; nothing computes a ranking today |
| `GATI_NAMES` | The two movements §19.4 names. `kendraadi gati` is built and is `HOUSE_ORDER`; `mandooki gati` is defined only as "the 3rd/11th jump" plus a pointer to a Kalachakra discussion the book has not given, so it is recorded and not built |
| `MANDOOKA_DASA_MISATTRIBUTION` | §19.4's correction of another author — the only place the book disputes a named dasa by attribution. A claim about naming, not a calculation, so it is stored whole |
| `MANDOOKA_DASA_IS_OF_RUDRAMSA` | What the real Mandooka dasa is for — wars and death, read in D-11. The chart is in the varga registry; the dasa waits on mandooki gati, which waits on Kalachakra |
| `TRIPOD_OF_LIFE` | §16.5.3's three reference points, their rings in the Sudarsana chakra, how fast each one's results turn over, and which dasa level each judges. Reading a chart from a moving reference point is the interpretation layer that does not exist yet; the yoga half of the same section **is** consumed, by `planetary_yogas.registry.dasa_level` |
| `TRIPOD_PRINCIPLE` | The principle as Parasara stated it, kept with the data it explains |
| `USE_THE_VARIATIONS` | §16.7's advice to prefer the variations over the plain reckoning. The variations are consumed; the advice to use them is a reading decision, not a calculation |
| `KENDRADI_GRAHA_DASA_INSTEAD` | §16.7's condition for abandoning Vimsottari altogether. Not actionable twice over: the comparison it rests on, the stronger of lagna and Moon, is undefined, and Kendradi Graha Dasa is not one of Part 2's nine systems |
| `DASA_ERROR_RULE` | §16.7's birthtime-error rule of thumb. The number it turns on **is** consumed — `BIRTHTIME_ERROR_DAYS_PER_MINUTE` — and a test checks the rule against the engine; this is the sentence it came from |
| `ASHTOTTARI_IS_CONDITIONAL` | §17.1's warning that Parasara made this a conditional dasa and that the conditions are "highly controversial". No condition is given, so nothing can gate on it |
| `ASHTOTTARI_MEANS_108` | Why the total is 108 and why some read the system as an ayur dasa. The 108 itself is consumed — Table 39's years sum to it |
| `ASHTOTTARI_HAS_NO_KETU` · `ASHTOTTARI_ANTARDASA_RULE` ·
`ASHTOTTARI_APPLICABILITY_VIEWS` ·
`ANTARDASA_SEED_BY_LORDS_UNQUANTIFIED` ·
`PARASARA_DASA_PRINCIPLES` · `NATAL_REFERENCE_READINGS` ·
`DASA_THIRDS` · `ANTARDASA_RESULT_RULE` | §17.1's reason for reading Ashtottari through the chara karakas. That Ketu has no dasa **is** consumed, in `ASHTOTTARI.order`; this is the inference drawn from it |

**Two of the nine are built** — Vimsottari and Ashtottari, both nakshatra
dasas. The remaining seven are six rasi dasas (Narayana, Lagna Kendradi Rasi,
Sudasa, Drigdasa, Niryaana Shoola, Shoola) and one nakshatra dasa
(Kalachakra). `dasha/rasi/` does not exist.

---

## How to use this register

When a chapter is reported complete, its "not yet consumed" entries are listed
in that chapter's OI entry and mirrored here. When something becomes consumed,
delete it from here — the test will tell you if you forgot.
