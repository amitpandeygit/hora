# Open items

Unresolved only. Closed items and the evidence that closed them live in
[closed-items.md](closed-items.md) and are not repeated here.

**5 waiting on Amit · 59 waiting on evidence · 2 parked**

---

## Waiting on you

Deferred by decision, 2026-08-26: held until every algorithm in the book is
implemented. Do not act on these, and do not re-raise them each session.

| ID | Decision | What moves if you say yes |
|---|---|---|
| OI-39 | Multiply before dividing at all six floor-division sites | Nakshatra **and pada** on `/v1/chart`, yoga on `/v1/panchanga`, the starting dasha lord — all wrong at exact boundaries today |
| OI-36 | Shorten `ABHIJIT_END` to `21 × NAKSHATRA_SPAN`, per §1.3.6 | `abhijit_active` on `/v1/panchanga` — a live field, ~21.6 hours a year |
| OI-37 | Make the 1st tithi `Pratipat`, the book's first-listed name | `full_name` on `/v1/tithi/compute` and `/v1/util/tables/tithis` — breaking response change; no calculation moves |
| OI-40 | Pick a default reading for a hora's length | The hora lord, whenever the real day is not 24h00m. Both readings supported today; 24h is the default |
| OI-68 | Switch `node_type` to `mean`, or keep `true` | Rahu and Ketu on **every** endpoint. Charts 6, 7 **and now 10** reproduce with mean; with true they are 39', 12' and **56'** out |

Listed in the order I would take them: OI-39 is the only unambiguous defect and
the only one touching `/v1/chart`. OI-37 and OI-40 are preference.

### OI-39 — floor-dividing by 360/27 lands one unit early

One nakshatra span is 360/27 = 13.333…°, not representable in binary, so
`x // NAKSHATRA_SPAN` returns k−1 when x is exactly k spans. `40.0 // 13.333333333333334`
is 2.0, not 3.0.

| quantity | boundaries wrong |
|---|---|
| yoga (27) | 9 |
| nakshatra (27) | 9 |
| nakshatra **pada** (108) | **59** |

Sites: `panchanga/core.py:147`, `charts/chart.py:110-111`, `dasha/base.py:128`
and `:161`, `charts/special_lagna.py:123`.

Ephemeris values never land exactly on a boundary; hand-entered ones do, which
is what every book exercise uses. Moon = 40°00'00" gives nakshatra 3 pada 4
instead of 4 pada 1.

Fix is one line per site — `int(x * 27 / 360)` — proven and boundary-tested in
`charts/yoga.py:completed_spans`. **Live consequence meanwhile:**
`/v1/yoga/compute` (correct) and `/v1/panchanga` (not) disagree at nine points.

### OI-36 — Abhijit's end does not match §1.3.6

**This is the one place our code is wrong against the book and we know it.**
Everywhere else we depart from a printed statement, the book contradicts itself
and a written rule picks the side — see "Where we stand against the book" in
[book-deviations.md](book-deviations.md). Here §1.3.6 is unambiguous and we do
not follow it.

§1.3.6: "The last quarter of Uttarashadha is known as Abhijit." That is
6 Cp 40 → 10 Cp 00.

| | End | Length |
|---|---|---|
| §1.3.6 | 10 Cp 00 | 3°20' |
| our code | 10 Cp 53'20" | 4°13'20" |

The extra 53'20" is the first 1/15 of Sravana — the classical Muhurta
definition, which PVR does not give. Start agrees; end does not.

[precedence.md](precedence.md) puts PVR's stated rule above classical
convention he does not repeat, which points to shortening it.

### OI-37 — `Pratipada` vs `Pratipat`

Table 3 prints row 1 as "Pratipat/Pratipada/Padyami". We take the book's
first-listed name as canonical everywhere — rows 2, 3, 4, 15 all do. Row 1 is
the only exception. Both spellings are stored either way; only `full_name`
changes.

### OI-40 — §1.3.11 contradicts its own example on a hora's length

First paragraph: 24 equal parts of the *actual* sunrise-to-sunrise interval, so
"almost equal to an hour". The example: "a period of one hour", read off a
15:30 clock elapsed. At 15.5h into a 25-hour day the two give the 15th vs the
16th hora — different lord.

Both are supported; `day_length_hours` defaults to 24, reproducing the example.
`/v1/panchanga` already uses the actual interval.

---

## Waiting on evidence

### OI-1 — JHora itself: no tier-1 verification

Nothing checked against Jagannatha Hora 8.0; it is Windows-only and no Windows
layer is available. All 36 slots in `tests/benchmark/fixtures/pvr_1972.json`
remain `unverified`.

Two weaker tiers pass: PyJHora 4.8.7 (57/57) and the book's own chapter 1.

**Closes when:** one JHora run of the reference chart is transcribed into that
fixture and `python -m hora.benchmark tests/benchmark/fixtures/pvr_1972.json --strict`
passes.

### OI-2 — display name spellings unverified against JHora

Book spellings are the default (`Pushyami`, `Sakuna`, `Kaarteeka`); pan-Indian
forms are available via `settings.name_scheme = "standard"`. The book is 2000,
JHora 8.0 is 2016, and PVR's 2010 "Looking Back" note says he revised things
afterwards. Integer IDs are the contract, so a switch is one line.

**Closes when:** JHora's display names are transcribed.

### OI-3 — adhika maasa: no reckoning chosen

Both amanta and purnimanta names are returned; neither is default. The adhika
flag uses the classical no-sankranti rule.

§1.3.8.2 settles the naming rule (Table 4, implemented in `charts/maasa.py`)
and the symptom ("Sun-Moon conjunction coming twice in the same rasi"). It does
**not** say which of the two is Nija and which Adhika. `maasa.month_pair()`
therefore returns the pair unlabelled and never guesses.

**Closes when:** JHora's default reckoning is confirmed, and which member of a
pair it calls adhika.

### OI-4 — Swiss Ephemeris licence not purchased

Production needs the Professional Licence from Astrodienst. Until it is signed
the service must not be exposed publicly — the AGPL alternative would require
open-sourcing the whole API. See [licensing.md](licensing.md).

**Closes when:** the licence is signed.

### OI-8 — chapters 10 onward not yet audited

Chapters 1–9 and 15 have all had a sentence-level pass, section by section
from the screenshots: worked examples and exercises as fixtures, tables cell by
cell, footnotes recorded. Chapter 9 covers the six arudha steps, the exception,
Table 18, Examples 29–30 and Exercises 12–13; chapter 15 covers §15.1, §15.3,
§15.4.1–15.4.4 and §15.5.1–15.5.2 with Tables 36–37 and footnotes 51–52.

Two caveats on chapter 15, which are gaps in *coverage*, not in the sweep:

- Three of its five strength measures are **not built** — `ashtakavarga` and
  `vimsopaka` are marked "not yet implemented", and `simple_rules` likewise.
  Only `avastha` is available. (`shadbala` is a different case: the book itself
  says its computation is beyond the book's scope.)
- Nothing in the code or the tests references a **§15.2**. Either the chapter
  has none, or a section was never screenshotted. Worth one look.

Chapters 10–27 hold aspects, argalas, yogas, dasas and Tajaka.

Chapter 6 was the warning: code written from general classical knowledge rather
than from PVR was wrong in three of twenty rules. Everything unaudited was
written the same way.

**Closes when:** every chapter has had a sentence-level pass.

### OI-12 — PVR's verbatim indications: redistribution licence unconfirmed

§2.3's rasi keyword lists and §8.2/§8.5's karaka readings are stored in
`data/content/*.yaml` under `source: pvr-vaia`, `licence_status: unconfirmed`.
Classical attributions are nobody's property; PVR's curated lists and prose are
his. They are withheld from responses unless `HORA_SERVE_UNCONFIRMED_CONTENT`
is set. §2.2.5's element readings are under the same gate.

**Closes when:** PVR grants redistribution rights, or the lists are replaced
with independently sourced ones.

### OI-14 — node exaltations: Gemini/Sagittarius vs Taurus/Scorpio

Table 6 exalts Rahu in Gemini and Ketu in Sagittarius; many texts say Taurus
and Scorpio. Following the book, approved 2026-08-25, recorded as
[D-4](book-deviations.md). Measured: the node's dignity label changes in ~33%
of charts. Node ownership stays co-lordship only; `RASI_LORD` unchanged.

**Closes when:** JHora confirms which pair it uses.

### OI-15 — Mercury's moolatrikona: 15° vs 16° Virgo

§3.3 rule 4 gives 15°–20°; BPHS is commonly read as 16°–20°. Following the
book, recorded as [D-5](book-deviations.md). Affects Mercury only between 15°
and 16° Virgo — about one chart in 360, dignity label only.

A BPHS disagreement does not by itself overrule PVR; BPHS survives in variant
recensions.

**Closes when:** what BPHS actually says is established, and whether 16° is well
attested or itself a variant.

### OI-18 — `charts/aspects.py` is premature and unverified

Written during Phase 1 scaffolding from general knowledge, not from the book.
Aspects and argalas are **chapter 10**, unaudited. `rasi_drishti` in it was
found wrong and corrected; the rest is unchecked. Nothing imports it, and
`tests/unit/test_not_yet_consumed.py` fails the moment anything does.

**Closes when:** chapter 10 is audited and the module is re-derived from it.

### OI-19 — sunrise: book says upper limb, PyJHora uses disc centre

| Source | Rank | Says |
|---|---|---|
| Book §5.5 comment (3) | 2 | Upper limb — "the latter approach is recommended" |
| PyJHora | 5 | `BIT_HINDU_RISING` — disc centre |

Default is now `disc_upper_limb`, recorded as [D-10](book-deviations.md).
Sunrise moves +3.7 min at the reference place; Ghati Lagna moves 4.6°.

This does not refute the PyJHora evidence — it is outranked, not wrong. If
JHora uses disc centre, rank 1 wins.

**Closes when:** JHora's sunrise definition is confirmed.

### OI-24 — chapter 8 gives only one chara karaka scheme

`/v1/karaka/chara` implements §8.2's eight-karaka scheme, the only one the book
defines. JHora offers four. There is no PVR text here to implement the others
from.

**Closes when:** a later chapter or another PVR source defines them, or they
are confirmed against JHora.

### OI-28 — §15.5.2's ayur-dasa adaptation cannot be computed

§15.5.2 adapts a rule using ayur-dasa, which requires dasa analysis.
`src/hora/dasha/rasi/` is empty.

**Closes when:** rasi dasas are implemented.

### OI-55 — §7.3's house-meaning rule derives 3 of the book's own 4 cases

§7.3: "the 4th houses in D-24, D-16, D-4 and D-12 show education, vehicle,
house and mother (respectively)."

`house_service.meanings_in_varga` takes the literal overlap of the two
signification lists, so every word it returns is PVR's own. It reaches D-24,
D-16 and D-4. **It cannot reach D-12**: that signifies "parents", the 4th house
signifies "Mother", and *mother is a parent* is world knowledge neither table
contains. The overlap returns `relative` — in both lists, not wrong, not what
PVR picked.

**This is a pattern, not one case.** Three instances so far, all in chapter 7:

| section | the book says | the tables say |
|---|---|---|
| §7.3 | 4th in D-12 shows **mother** | D-12 signifies "parents" |
| §7.3.5 | 5th shows **memory**, **success in competition** | 5th lists neither |
| §7.3.9 | 5th shows **progeny** | 5th lists "Children" |

The book links matters to houses by meaning throughout. Any code that matches
significations literally will keep hitting this, and each miss looks like a bug
until it is recognised as the same gap.

The response carries `derivable` and a `limitation` field naming this case
rather than presenting a partial method as complete. Nothing invents a synonym.

**Closes when:** a semantic map is taken from the book (not from general
knowledge), or you accept the overlap as a hint for callers to pick from —
which is what we do today.

### OI-83 — "deep exaltation" has an exact degree but no tolerance

Jaya wants the 10th lord "in deep exaltation"; Vidyut wants the 11th lord the
same. The book gives each planet's exact exaltation degree — Sun 10° Aries,
Saturn 20° Libra and so on — but never says how near that degree counts as
*deep*. A whole sign is plainly too wide, or the word adds nothing; an exact
match never happens.

**What we do:** neither yoga is ever reported present, and the two failures are
kept apart. When the planet is not in his exaltation sign at all the verdict is
a plain, definite absence — which settles almost every chart. When he *is*
there, the verdict names his distance from the exact degree, says section 11.6
gives no threshold, and carries a qualifier pointing here. A caller with their
own threshold has the number they need.

**Closes when:** you give a tolerance, or a later chapter defines it, or
JHora's output shows what it uses.

### OI-84 — Vasumati names no reference and no count

"If benefics occupy upachayas, then this yoga is present." Upachayas from
what — lagna, Moon, Sun? And how many benefics: one, or all of them?

§11.3's guideline 3 counts benefics in upachayas **from Moon** and grades the
result — all of them is great wealth, two is medium, one is little. Vasumati
neither names Moon nor grades.

**What we do:** houses are counted from **lagna**, as everywhere else in
§11.6, and one benefic in an upachaya is enough — the plain reading, and the
one the printed fullness clause implies when it says "the benefics occupying
upachayas should be strong", which presumes some do and some may not. Any
verdict that is present also names the benefics sitting outside the upachayas,
so a caller wanting the stricter "all of them" reading has what they need
without the engine choosing for them. The fullness clause's other half — "no
malefic should occupy upachayas" — is reported as a qualifier, never as part
of the presence test, because the book attaches it to full results.

**Closes when:** you settle the reference and the count.

### OI-85 — one planet lording both a quadrant and a trine

§11.7.1 asks for "the lord of a quadrant ... associated with the lord of a
trine", and every association it names needs **two** planets: conjoined, in
mutual drishti, or exchanging signs. A planet cannot do any of those with
himself.

But for six lagnas one planet lords a quadrant and a trine that are different
houses. Derived from the book's own house lists, not asserted:

| lagna | planet | quadrant | trine |
|---|---|---|---|
| Taurus | Saturn | 10th | 9th |
| Cancer | Mars | 10th | 5th |
| Leo | Mars | 4th | 9th |
| Libra | Saturn | 4th | 5th |
| Capricorn | Venus | 10th | 5th |
| Aquarius | Venus | 4th | 9th |

The lagna lord is a separate, trivial case the book has already handled —
"Lagna can be taken as a quadrant or a trine here. It is both" — so he holds
both sides in every chart and is excluded from the table above.

Taurus alone also makes Dharma-Karmadhipati unreachable: Saturn lords both the
9th (Capricorn) and the 10th (Aquarius), so for that lagna the two lords can
never associate. It is the only lagna whose 9th and 10th share a lord —
Capricorn and Aquarius are the only adjacent pair of signs under one lord.

**What we do:** nothing is concluded. `raaja_basic` reports such a planet as a
qualifier naming the houses, and `dharma_karmadhipati` says outright when the
two lords are one planet. Neither is counted as forming the yoga.

**Closes when:** a later section discusses it, or you decide.

### OI-86 — Vipareeta's second clause, and an ideal case that escapes the rule

The definition: "If their lords occupies dusthanas **or conjoin dusthanas**,
it results in this yoga." The first clause is plain. The second is not — a
planet cannot conjoin a house, so "conjoin dusthanas" has to mean conjoining
the lords of dusthanas.

The ideal case is what settles it: "the lords of the 6th, 8th and 12th houses
will all be together in one of the three houses (**or the 3rd house or the
11th house**)". The 3rd and 11th are not dusthanas. Three dusthana lords
together in the 3rd occupy no dusthana at all, so under the first clause alone
the book's own ideal case would not form the yoga. Under the second clause it
does — they conjoin each other.

**What we do:** both clauses are tested, and a verdict says which one fired.
The ideal case is reported as a qualifier, never as the presence test, because
the book itself says "the results of this yoga may be experienced with just one
or two dusthana lords occupying a dusthana".

**Closes when:** you confirm the reading, or JHora's output settles it.

### OI-87 — §11.7.1's Dharma-Karmadhipati results sentence is cut off

Printed: "One born with this yoga is sincere, devoted and righteous. He is
fortunate and."

The sentence stops mid-clause. Transcribed exactly as printed in
`data/content/yoga_results.yaml` with a note, rather than being completed or
trimmed. Nothing calculational turns on it.

**Closes when:** you supply the missing words, or confirm the book prints it
this way.

### OI-88 — "functional malefics" are used before they are defined

§11.7.2's first factor: "The two planets should be free from afflictions from
functional malefics."

Nothing read so far says what a functional malefic is. It is not a natural
malefic — §3.2.2's list is fixed and has nothing to do with a chart's lagna —
so it must be a lagna-relative notion the book defines elsewhere. Guessing at
it would be inventing a rule.

§11.7.2 does let two things slip, both in passing:

- **Libra lagna: Jupiter.** "They are afflicted by a functional malefic
  (Jupiter)" — of Chart 10, Emperor Akbar.
- **Leo lagna: one or more of Moon, Mercury, Venus.** "functional malefics were
  with them", of the Sun and Jupiter in Rajiv Gandhi's Leo lagna. Those three
  are the rest of Leo; the book names none of them.

Two points do not make a rule — Jupiter is a natural benefic and the 6th lord
for Libra, which is *a* hypothesis and not the book's.

**What we do:** the factor is returned with `satisfied: null` and a detail
naming this item, and `/v1/planetary-yoga/raaja-magnitude` lists it under
`not_assessed` — now with both data points served beside it, as data.
`FUNCTIONAL_MALEFIC_DATA_POINTS` records exactly what the book said and nothing
more; a lagna it has not spoken about is simply absent. The factor is never
silently treated as satisfied.

**Closes when:** a section defining functional malefics is supplied.

### OI-89 — §11.7.2 says "bad avasthas" without naming which

The third factor: "The two planets should not be combust, debilitated or in an
inimical house or in bad avasthas (states)."

Combustion, debilitation and an inimical house are all computed. The avasthas
are computed too — chapter 15's age, alertness and mood states are implemented
— but §11.7.2 never says which of them count as bad. Several are plainly
unfavourable by their own meaning (Duhkhita, "distressed"; Sushupta, "asleep";
Mrita, "dead"), and picking a set from those meanings would be our reading, not
the book's.

**What we do:** the three named blemishes are checked and reported. No avastha
is called a blemish, and the detail string says so. A pair with a real blemish
still comes back `satisfied: false`, so the factor is not weakened by the gap.

**Closes when:** a section names the bad avasthas, or you decide the set.

### OI-90 — the 6° rule is exemplified for a conjunction only

"The conjunction or aspect responsible for the Raaja Yoga should be close (say,
within 6° or so)."

The worked example measures a conjunction: Mercury at 2° Taurus and Venus at
26° are "too far apart", and Venus at 3° is "very close". Plain separation in
degrees, and our output reproduces both readings — 24.00° and 1.00°.

For an **aspect** the book gives no example. Graha drishti is whole-sign, so
"close" has to mean near the exact angle: an aspect on the Nth house is exact
at (N−1)×30° of separation, and the orb is the deviation from that.

**What we do:** that reading is used, and the response says so on every aspect
pair rather than reporting a bare number. The 6° figure itself is hedged twice
in the book — "say" and "or so" — so `close_orb_is_approximate` is served
alongside it and no verdict turns on the boundary alone.

**§11.7.2's two charts confirm the reading.** Both aspect orbs the book grades
are ones it calls close, and both are small under this measure and only this
measure: Akbar's Moon and Mercury are **1.32°** from an exact 7th-house aspect
("they have a close aspect"), and Rajiv Gandhi's Saturn is **2.01°** from an
exact 3rd-house aspect on Jupiter ("a very close aspect"). Measured as raw
separation instead they would be 178.68° and 57.99°, which no one would call
close.

**Closes when:** you confirm the reading. The evidence above is why it is no
longer a guess.

### OI-91 — §11.7.2's amsa grade assumes both planets share a count

"If the two planets are in Paarijaataamsa (count of 2)..." — every grade is
phrased as though the pair has one count.

Its own worked example does not. For Capricorn lagna with Mercury at 2° Taurus
and Venus at 26°, the dasavarga counts are **2 and 3**: Paarijaataamsa and
Uttamaamsa. The book does not say what to do then.

**What we do:** both planets' counts, amsas and the charts that produced them
are reported. A shared grade is given **only** when the two counts agree; when
they differ the response says so and asserts no amsa for the pair.

Two smaller gaps recorded with it: §6.6's table names a tenth amsa,
Sreedhaamaamsa, for a count of 10, which §11.7.2 does not discuss
(`amsa_count_not_discussed`); and §11.7.2 gives no result sentence for counts 6
to 9 beyond saying they occur "only for divine persons".

**Closes when:** you settle how a split count is graded.

### OI-95 — §11.8 (12) says "with benefics" and gives no number

"If the 11th lord is in the 11th house without aspects from any malefics and
**AK is with benefics**, then one has gains from a king."

Plural, unquantified. This is the third such phrase in chapter 11 — §11.6's
Vasumati says "benefics occupy upachayas" (OI-84) and §11.7.3 (17) says
"benefics are in quadrants" (OI-94) — and the three may not want the same
answer.

**What we do:** one benefic with AK satisfies it, which is the plain reading of
a planet being "with benefics" in the same sign. Every verdict, present or
absent, reports how many are actually with him, so a caller wanting two or more
has the number without the engine having chosen.

**Closes when:** you settle whether chapter 11's unquantified plurals mean one
or more, or all.

### OI-98 — "They are conjoined or aspected by a maraka planet" — how many of them?

Eight of §11.10's thirteen end with a clause of this shape, naming two or more
planets and then one maraka reaching "them". Three readings are possible:

| reading | combination (1) reachable on |
|---|---|
| **strict** — one maraka reaches every named planet | **2** of 12 lagnas |
| **middle** — each named planet is reached by some maraka | **8** of 12 |
| **loose** — a maraka reaches at least one of them | **12** of 12 |

Computed by exhausting every seat a maraka could take, for every lagna.

**What we do:** the loose reading, because it is the only one that leaves a
rule Parasara states for all charts alive on all twelve lagnas — the same
argument that settled OI-79 and D-37. Under the strict reading combination (1)
would be dead for ten lagnas including Aries, where the 2nd and 7th are both
Venus and her single 7th drishti cannot reach two adjacent signs.

Every verdict names which of the planets were reached and which were not, so
the two stricter readings are reconstructable from the answer without the
engine having chosen them.

**Closes when:** you confirm the reading, or an example fixes it.

### OI-96 — §11.10's maraka NOTE has a circular third sentence

"The 2nd and 7th houses are maraka (killer houses). Their lords are marakas
(killers). Any malefics occupying 2nd and 7th or associating with 2nd and 7th
lords **also become malefics**."

The third sentence says malefics become malefics, which asserts nothing. In
context it must be "also become **marakas**" — the sentence is plainly
extending the maraka set, and the section then uses "a maraka planet" in eight
of its thirteen combinations.

**What we do:** presence is decided on the **base** set — the 2nd and 7th
lords, which the NOTE states without ambiguity. The extension the third
sentence describes is computed on every chart and reported: which planets it
would add, and, where a verdict is absent only because of the narrow set,
that the verdict turns on this item.

**Why narrow rather than wide.** These are poverty combinations. Telling
someone they have one on a reading the book garbled is worse than telling them
they do not.

**Closes when:** you confirm the reading, or a later printing settles it.

### OI-97 — §11.10 (10) uses "malefic houses" and "benefic houses", which nothing defines

"Benefics are in malefic houses and malefics are in benefic houses."

No section read so far defines either term. Chapter 7 names seven house
categories and neither is among them; the dusthanas are glossed "bad/evil
houses", not malefic. The obvious guess — dusthanas malefic, quadrants and
trines benefic — leaves the 2nd, 3rd, 7th and 11th unassigned, so it is not
even a complete reading.

**What we do:** the combination is reported undecidable, naming the two terms
and this item. It is the only one of §11.10's thirteen that cannot be
answered.

**Closes when:** a section defines the two terms.

### OI-93 — §11.7.3 (2)'s clause (d) does not say which planets it means

"If (a) lagna lord is in 5th, (b) 5th lord is in lagna, (c) AK and PK are in
lagna or the 5th house, and (d) **those planets** in owns rasi or amsa or in
exaltation or aspected by benefics..."

"Those planets" could be the two named immediately before in (c) — AK and PK —
or all four named across (a) to (c). The clauses are one sentence, so grammar
does not settle it.

**What we do:** both readings are computed on every chart. The **wider** one
decides the verdict, because it is the stricter of the two and cannot make a
yoga present that the narrow reading would not; a qualifier then reports what
each reading found, so a caller preferring the narrow one has the answer
without the engine having chosen for them.

**Closes when:** you settle the scope.

### OI-94 — §11.7.3 (17) does not say how many benefics and malefics

"If benefics are in quadrants and malefics are in the 3rd, 6th and 11th
houses, one becomes a king even if he is from a lowly family."

Read loosely — *some* benefic in a quadrant and *some* malefic in one of those
three — this fires on a very large share of charts, which sits badly with a
rule promising kingship from a lowly family. Read strictly — every placed
benefic in a quadrant and every placed malefic in the 3rd, 6th or 11th — it is
rare, which fits.

**What we do:** the strict reading, and the verdict names every planet that
falls outside so the looser reading is reconstructable from the answer. The
yoga also refuses to decide without a paksha, since it must sort every planet
into benefic or malefic and §3.2.2 gives the Moon no nature without one.

**Closes when:** you settle the reading, or an example fixes it.

### OI-81 — no §11.6 yoga can be reported fully present, because strength is not built

§11.6's preamble binds all eighteen:

> "Sometimes the results of a dasa may be felt even if all the required
> combinations are not present. But, for a yoga to be fully present, all the
> required combinations must be present and the participating planets must be
> strong."

Strength is chapter 15's. Of its five measures only avastha bala is
implemented; shadbala, ashtakavarga bala, vimsopaka bala and the simple
comparison rules all carry `available: False`. None of them answers "is this
planet strong" in the plain sense §11.6 asks for, so the engine can decide the
combinations and nothing more.

Four of the eighteen ask for a *named* lord's strength in the definition
itself: Kaahala and Mridanga the lagna lord, Bheri the 9th lord, Sankha both.
Their verdicts name that lord over and above the section-wide note.

What we do: `present=True` means the combinations hold, never that the yoga is
full, and **every** §11.6 verdict carries `STRENGTH_NOT_ASSESSED` saying so —
tested exhaustively across the group, not sampled. The `/rules` endpoint
carries the preamble and the note.

**Closes when:** chapter 15's strength measure is implemented, and the four
named-lord clauses can be decided rather than deferred.

### OI-82 — the first eighteen §11.6 yogas have no results prose

The §11.6 material supplied for the eighteen printed **before** the Shivaji
example gives each yoga's defining combinations, name meaning, footnotes and
alternatives, but no results paragraph, where §11.2 to §11.5 each have one.

The thirty printed **after** that example each carry their own Results
sentence, and all thirty are transcribed. So the gap is specific to the first
eighteen, not to the section.

Those eighteen have entries in `data/content/yoga_results.yaml` carrying
`results_transcribed: false` and a null `verbatim`, so the registry-to-results
exhaustiveness guard still holds and the gap is visible rather than reading as
"this yoga has no results".

Footnote 34 settles that the section *does* print them: it says "the results
of this yoga include the words 'principled' and 'kind'" about Kalpadruma, and
glosses a third, "likes wars" (yuddhapriyah). Three words are not a paragraph,
so the entry stays marked untranscribed.

**Closes when:** you supply the §11.6 results text.

### OI-80 — "applicable" in §11.5.4 excludes a weakened yoga, on the example's evidence

§11.5.4: "These yogas apply if no other Naabhasa yogas mentioned previously
are **applicable** in a chart."

Its own worked example decides what "applicable" means. Lord Sri Rama's chart
— §1.3.4's Example 1, which Figure 1 draws, and a fixture here since chapter 1
— is given as **Daama**. It contains exactly one earlier Naabhasa yoga:

> **Sarpa.** Malefics hold the 4th, 7th and 10th from Cancer — Saturn in
> Libra, Mars in Capricorn, the Sun in Aries. But Jupiter and the Moon hold
> the lagna itself, and §11.5.2 says: "If a benefic also occupies one of the
> quadrants, this yoga **may not operate well**."

Count that Sarpa as applicable and it supersedes Daama, so §11.5.4's rule
contradicts §11.5.4's example on the same page. Do not count it, and rule and
example agree exactly.

**So a yoga the book itself says may not operate well does not count as
applicable.** Implemented as a `weakened` flag, set only by the Dala detectors
— §11.5.2's clause is the only place the book says a yoga does not fully
operate. Combustion (§11.2.4) and Kemadruma (§11.3.4) weaken *results*, which
is a different claim, and they do not set it.

**This is a judgement call.** It is the reading under which the section is
self-consistent, which is why it was taken — but PVR never says it, and a
reader could instead conclude that his example simply overlooked the Sarpa.
Registered as PVR-13.

It does not rescue Gola or Yuga (OI-79): those are superseded by Aasraya and
Aakriti yogas, which carry no weakening clause at all.

**Closes when:** JHora's Naabhasa output shows whether a weakened Dala yoga
suppresses a Sankhya one.

### OI-79 — §11.5.4's fallback rule makes two of its own seven unreachable

§11.5.4: "These yogas apply if no other Naabhasa yogas mentioned previously
are applicable in a chart."

Taken literally, **Gola and Yuga can never be present**. Proved exhaustively:

| yoga | needs | reachable in |
|---|---|---|
| Gola | 1 distinct sign | 0 of 144 sign × lagna combinations |
| Yuga | 2 distinct signs | 0 of 792 sign-pair × lagna combinations |

The reason is structural. Every set of one or two signs fits inside some
seven-consecutive-sign window — the shorter arc between any two signs is at
most six — and §11.5.3's five run-yogas (Naukaa, Koota, Chatra, Chaapa, Ardha
Chandra) cover all twelve windows. So one of them always applies and always
supersedes. One sign is also one modality, so an Aasraya yoga applies too.

Three signs *can* escape every window (40 of 220 triples do), which is why
Soola survives — rarely, in about 16% of three-sign charts.

**We implement the rule as stated**, so both yogas are defined, transcribed and
permanently absent. Their verdicts say so: the reason names the count *and* the
yoga that superseded them, so nothing is hidden.

Three readings, and the book supports none of them over the others:

- the fallback is meant strictly, and Gola and Yuga are dead letters PVR
  inherited from the classical list without checking;
- "applicable" means something weaker than "detected" — perhaps only the
  families §11.5 calls more important;
- the run-yogas are meant to require the *whole* seven-sign span to be used,
  not merely to contain the planets, which would free both.

**Closes when:** JHora's Naabhasa output shows whether it ever reports Gola.

### OI-78 — is Vaapi Yoga two alternatives or one union?

§11.5.3: "If all the planets are panaparas or in apoklimas, this yoga is
formed."

Two readings:

- **two alternatives** — all the planets in the panapharas (2nd, 5th, 8th,
  11th), *or* all of them in the apoklimas (3rd, 6th, 9th, 12th);
- **one union** — all the planets somewhere in those eight houses, which is
  the same as saying no planet is in a quadrant.

We implement the first. The sentence reads as two alternatives, and the union
reading makes Vaapi a much weaker claim — merely the complement of Kamala,
which is "all the planets are in quadrants".

Against that: §11.5.3's Ardha Chandra uses the same "or" for a union of
starting points — "the 7 signs starting from a panapara **or** an apoklima" —
where eight starts are all admitted. So the same word carries both senses in
one section.

`union_alternative` is kept on the spec, so switching readings is one line.

**Closes when:** JHora's Naabhasa output settles it, or a worked chart appears.

### OI-74 — §11.3 guideline 2's "(respectively)" has nothing to pair with

> "In such a situation, aspect of Jupiter on Moon beings wealth and comforts in
> the case of daytime birth **(respectively)**."

"Respectively" pairs an ordered list with another ordered list. Here it follows
"wealth and comforts" — two things — and the only two-item list in reach is the
sentence before it: "own navamsa **or** that of an adhimitra".

Read that way, an own-navamsa Moon gives *wealth* and an adhimitra's navamsa
gives *comforts*. That is the only reading in which the word does any work.

The book does not say so, and guideline 2 is not computed anyway (OI-76), so
nothing turns on it yet. Recorded because a later reader will otherwise have to
rediscover that the word is unexplained.

Also in the same sentence: "beings" for "brings", transcribed as printed.

**Closes when:** a later chapter uses guideline 2 with a worked chart, or JHora
shows which reading it implements.

### OI-75 — must all three of Adhi Yoga's houses be occupied?

§11.3.6: "If the natural benefics occupy 6th, 7th and 8th from Moon, this yoga
is present."

Two readings:

- **every** natural benefic sits in one of those three houses (what we
  implement), or
- benefics occupy **all three** houses, one apiece at least.

The book's own example cannot settle it, because the example does not satisfy
the rule at all (D-28). Repaired minimally — Moon to Pisces — it puts benefics
in the 6th and 7th and leaves the **8th empty**, which supports our reading and
rules out the stricter one. But that rests on a repair we chose.

We also exclude the Moon from her own test: a waxing Moon is a natural benefic
(§3.2.2) and can only ever be the 1st from herself, so counting her would make
Adhi impossible for every bright-half birth.

**Closes when:** a worked Adhi chart appears, or JHora's yoga output settles it.

### OI-76 — §11.3 guideline 2 needs four chapters joined and is not computed

> "If Moon is in own navamsa or that of an adhimitra (good friend), that is
> good. In such a situation, aspect of Jupiter on Moon beings wealth and
> comforts in the case of daytime birth..."

To decide it the engine must join:

- the Moon's **navamsa** and that navamsa's lord — chapter 6;
- the compound **relationship** between the Moon and that lord, to test for
  adhimitra — §3.4;
- whether the birth was by **day or night** — chapter 5 / the panchanga;
- **Jupiter's and Venus's graha drishti** on the Moon — §10.2.

Every piece is built. Nothing joins them, so the guideline is returned with its
text, its day/night table and a null verdict saying what is missing.

This is the first rule in the book needing four chapters at once, and it is
worth doing properly rather than approximately.

**Closes when:** the join is written and checked against a worked chart.

### OI-73 — do Rahu and Ketu count as "a planet" in the Ravi yogas?

§11.2.1, §11.2.2 and §11.2.3 all turn on the same phrase:

> "If there is **a planet other than Moon** in the 2nd house from Sun..."

One graha is excluded by name. Whether the nodes are in the set at all, the
chapter never says, and it changes how often three of the four Ravi yogas fire.

The book uses "planet" both ways elsewhere. §8.1 writes "Rahu, Ketu **and the
seven planets**", which puts the nodes outside the word; §10.2's "**All
planets** aspect the 7th house from them" puts them inside, and we treat it as
all nine. §11.2's four examples use Jupiter, Mercury, Venus and Mars only, so
they do not settle it either.

**Excluded by default**, as a per-call parameter (`include_nodes`), and the
response lists `grahas_considered` so the choice is visible in the output and
not only in the request.

**§11.5 sharpens it three ways.** §11.5.1's Aasraya yogas say "**all the
planets**", so two extra grahas must agree and the flag matters more — though
it can never make the yoga impossible, since the nodes are always six signs
apart and six signs apart is always the same modality. §11.5.2's Dala yogas say
"natural benefics/malefics" instead, which §3.2.2 settles, and their own Sarpa
example is built from Mars, **Rahu and Ketu** — so the flag governs the phrase
"a planet" only, and those detectors ignore it. And §11.5.3's preamble is the
closest the book comes to an answer: "Rahu and Ketu are **not counted as
planets by many authors**" — matching our default, but attribution rather than
a ruling, and scoped to the Aakriti twenty.

The default is the conservative one — it under-reports rather than
over-reports — but it *is* a choice, and it is not PVR's.

**Closes when:** JHora's yoga output settles it, or a later chapter uses a node
to form one of these.

### OI-72 — Exercise 17 is the only place chapter 10 compares strengths

§10.7 step 4 says "compare the strengths and decide whether argala dominates or
virodhargala", and chapter 10 never does it — Examples 35 and 36 both skip it
(OI-70). Exercise 17's hint is the exception, and even there it ranks planets
*within* an argala house rather than argala against virodhargala:

> "Being in **own house**, Venus dominates over Jupiter and Mercury. Being the
> **most advanced** planet, Mercury is also strong. Mars dominates over Sun and
> Ketu, being in own house and being **more advanced than Ketu** – the other
> owner of Sc."

Two criteria — **own house** and **most advanced** — plus a tie-break between
co-owners of a sign. All three belong to chapter 15's `simple_rules` measure,
which is marked "not yet implemented" and which
`test_simple_rules_is_the_measure_section_9_2_actually_wants` already flags as
wanted elsewhere.

This is evidence of what that measure must contain, gathered from a chapter
that has no business defining it.

**Closes when:** chapter 15's simple-rules measure is built and reproduces this
hint's three judgements.

### OI-70 — §10.7 step 3 is unvalidated: no counting rule fits both examples

Step 3: "If there are both, see if **more planets** cause argala or
virodhargala." Two ways to count are defensible — every planet in an argala or
virodhargala house (**literal**), or only those that do something, dropping a
virodhargala whose paired argala house is empty and an argala that is itself
obstructed (**effective**, using §10.6's own obstruction rule).

Both worked examples read the **argala** as decisive. Neither count fits both:

| Saturn as target | literal | effective | the book reads |
|---|---|---|---|
| Ex 35, Narasimha Rao | 3 v 3 tie | 0 v 1 → virodha | argala — writing, politics |
| Ex 36, Reagan | 1 v 3 → virodha | 1 v 0 → argala | argala — acting |

**What both examples actually do is skip step 3.** They identify the argala and
read it, weighing no obstruction, though both charts have one.

So `dominant` implements a stated rule that **no worked example confirms**. It
is returned because §10.7 states it, and should not be trusted until something
validates it. The effective *counts* are returned as data; no
`dominant_effective` verdict is offered, since that would be our judgement
rather than PVR's.

Where the book does give a verdict — "Sun's **unobstructed** argala on GL" —
both counts agree, and "unobstructed" is the effective test applied to one
argala rather than a tally.

Related: OI-67 is the same question one level down, and step 4 is unavailable
in both examples anyway.

**Closes when:** an example applies step 3 where the counts differ, or JHora's
argala output settles it.

### OI-68 — Charts 6, 7 and 10 all need the **mean** node; our default is `true`

Three charts print their own birth data, so all three can be recomputed rather
than transcribed. All three reproduce every body to within one arcminute —
**only with the mean node**.

| Chart | Rahu, mean | Rahu, true | printed |
|---|---|---|---|
| 6 · Narasimha Rao, 1921, 5h17m **east** | 0 Li 48 | 1 Li 26 | 0 Li 47 |
| 7 · Reagan, 1911, 6h **west** | 21 Ar 54 | 21 Ar 42 | 21 Ar 54 |
| 10 · Akbar, **1542**, 4h39m east | 7 Aq 57 | 7 Aq 00 | 7 Aq 56 |

Thirty-nine, twelve and **fifty-six** arcminutes out under `true`. Every other
body in all three charts — ascendant, seven grahas — lands within one
arcminute, which is the book's own display rounding. Chart 8 remains neutral;
it does not separate the conventions.

The three share no dates, hemispheres or offsets, and Chart 10 is four
centuries earlier than the others and forty years before the Gregorian reform,
so the agreement is not an artefact of one setup or one era.

This is the only hard evidence in the project about which convention the book
uses, and it points against our default. The reference chart (Chart 1, 1972)
cannot settle it: its JHora output is still the empty stub of OI-1.

**Not changed.** `node_type` is a live default touching Rahu and Ketu on every
endpoint — chart, panchanga, karakas, dasa lords, argala. Pinned by
`test_chart_6_needs_the_mean_node`, `test_chart_7_confirms_oi_68_independently`
and `test_chart_10_is_a_third_vote_for_the_mean_node`, which assert the failure
in both directions so the evidence cannot be lost.

**Closes when:** you decide, or a JHora run of Chart 1 settles it.

### OI-69 — Example 35 makes Saturn the karaka of livelihood and karma; chapter 8 does not

"Saturn is the significator of livelihood and karma. Argalas on him denote
decisive influences on livelihood and karma."

Chapter 8 does not say this anywhere:

- **Table 15** gives the 10th house — whose §7.2 signification includes
  "karma (action)" — to **Mercury**, not Saturn.
- **Table 16's** Saturn row lists the 5th (Following), 6th (servants), 8th
  (Longevity, troubles) and 12th (losses, hospitalization). No karma, no
  livelihood.

**Used three times.** Example 35 opens with it, Example 36 assumes it, and
Exercise 17 repeats it word for word. A settled premise, not a slip.

Saturn as karma karaka is standard classical doctrine, so the claim is not
surprising — but chapter 8 is the chapter that was supposed to hold the karaka
tables, and it does not hold this. Either Table 16 is not exhaustive, or a
later chapter adds to it.

Recorded as the example's own premise rather than added to the tables, since
adding a karakatwa PVR did not print there would corrupt a transcribed table.

**Closes when:** a later chapter states Saturn's karakatwas, or you decide the
tables may be extended from worked examples.

### OI-67 — does a secondary argala count equally in §10.7's planet tally?

§10.7 step 3: "If there are both, see if **more planets** cause argala or
virodhargala."

§10.5 has already split the four argala houses into three **primary** (2nd,
4th, 11th) and one **secondary** (5th), and §10.7 gives the 5th the weakest
role — "the additional contributing factors", against "basic ingredient" and
"basic factor" for the 2nd and 4th. But step 3 says "more planets" and draws no
distinction.

So a graha in the 5th may or may not count as a full vote against a
virodhargala. The book never says.

The engine counts all argala houses equally, and returns
`primary_argala_graha_count` and `secondary_argala_graha_count` separately so a
caller can weight them differently without recomputing. No verdict changes
today that would not change under either reading — but that is because nothing
consumes the tally yet.

Bound up with **step 4**, which is also unresolved: "compare the strengths and
decide whether argala dominates" needs a graha strength measure. Chapter 15's
`simple_rules` is the one section 9.2 wants and it is not built. On a tie the
engine returns `dominant: null` with the reason, rather than picking.

**Closes when:** the strength chapters land and step 4 becomes computable —
the same evidence will probably settle whether the 5th votes at full weight.

### OI-65 — how many malefics are "several" in §10.6's 3rd-house rule?

§10.6: "If there are **several** malefics in the 3rd house from a house or a
planet, they cause argala instead of virodhargala on that house or planet."

The book never says how many. The only evidence is Exercise 16's own answer
table: the 11th house is Vi, the 3rd from Vi is Sc, and Sc holds **Mars and
Saturn** — two unambiguous malefics. The printed answer still lists them under
*virodhargalas*.

So by the book's own worked output two is not "several", and three is the
smallest threshold that reproduces Exercise 16. `SEVERAL_MALEFICS = 3`, and a
test states the failing case: at two, the 11th row stops matching.

**The evidence is thin.** Exactly one cell in the whole exercise has two or
more malefics in its 3rd, so this rests on a single data point — and the
exercise may simply be listing occupants mechanically and leaving the special
principle to the reader, in which case it is no evidence at all.

The threshold is a per-call parameter, so nothing is baked in.

**Closes when:** JHora's argala output settles it, or PVR states a number
elsewhere.

### OI-64 — an aspect may not land, and nothing decides whether it does

Two sections say it outright.

§10.1: "The nature of the influence exerted and **the degree to which that
influence succeeds** depends on the individual situation."

§10.4, with a case: "How pious and god-fearing his influence makes his
neighbors depends on other factors. **If one of the neighbors is a dreaded
criminal, he is not going to be influenced.**"

So an aspect existing and an aspect taking effect are different things. The
engine computes the first and says nothing about the second — correctly, since
chapter 10 gives no rule for it, only the warning that one is needed.

Two further §10.4 claims are recorded and equally uncomputed:

- **Nature.** Grahas sharing a rasi share their rasi-drishti *targets* but not
  the nature of the influence — the priest and his movie-loving brother reach
  the same neighbours and do opposite things there. Nothing computes nature.
- **Scope.** Graha drishti is "greater influence"; rasi drishti is "limited
  influence on the neighbors". Comparative, never numeric. `ASPECT_SOURCE`
  keeps it as prose and a test asserts no number is exposed — quantifying it
  would put our judgement inside PVR's rule.

This matters most for interpretation, which is where the temptation to invent a
weight will come from. The response carries `influence_caveat` so a caller
cannot read an aspect as an outcome.

**Closes when:** a later chapter gives a rule for whether an aspect succeeds —
benefic/malefic nature of the aspected graha, strength, or argala — or you
decide the engine should stop at "the aspect exists" permanently.

### OI-63 — `SPECIAL_ASPECTS` gives Rahu and Ketu the 5th and 9th; §10.2 does not

§10.2: "In addition, **Mars, Jupiter and Saturn** have special aspects." Three
grahas, three bullets, no fourth. The chapter gives the nodes nothing beyond
the 7th that "all planets" get.

`core/constants/graha.py` carries:

```python
Graha.RAHU: (5, 9),   # optional in JHora; gated by settings.rahu_ketu_aspects
Graha.KETU: (5, 9),
```

**No behaviour is wrong today** — `rahu_ketu_aspects` defaults False, so
`graha_drishti_houses(RAHU)` returns `(7,)` and Exercise 14 reproduces exactly.
The problem is provenance: 5 and 9 for the nodes is not in this chapter, and
the comment cites JHora rather than PVR. It is the same shape as the
`rasi_drishti` offsets that were wrong in all three rows (OI-27, closed) —
written from general classical knowledge, not from the book.

Some schools give the nodes 5/9/12, some 5/7/9, some none. Which one JHora
implements has not been checked.

Options: (a) confirm against JHora and cite it; (b) find PVR's own statement in
a later chapter, if he makes one; (c) drop the entries and let the flag raise
rather than silently return a school we cannot source.

**Closes when:** the source for the nodes' 5 and 9 is named, or the entries go.

### OI-62 — the not-yet-consumed register counts publication as consumption

`test_not_yet_consumed.py` exempts four named "exposer" files plus
`core/constants/`. Every other file that mentions a symbol counts as consuming
it — including a `*_service.py` that only copies the string into a response.

Measured: **49 constants** have no consumer other than a `*_service.py`, and
most are prose. Examples: `CHARA_KARAKA_PROCEDURE`, `CHARA_KARAKA_TIE_BREAK`,
`CHOOSING_A_KARAKA`, `AVASTHA_EFFECTS`, `CONJUNCTION_DEFINITION`,
`CHOOSE_MEANING_BY_VARGA`.

`reference_service.py` is exempt for exactly this reason — its docstring says
it "formats constants and computes nothing astrological". But `karaka_service`,
`strength_service`, `varga_service`, `maasa_service` and `house_service` all
publish prose the same way in among their real calculations, and the guard
cannot tell the two apart at file granularity.

Consequence: the register **understates** how much of the book is recorded but
not acted on. Publishing a rule is not applying it.

Options: (a) exempt at function granularity rather than file — a service
function that only reads constants and returns them is an exposer; (b) mark the
publication-only constants explicitly, e.g. a `PUBLISHED_ONLY` tuple per
module; (c) accept it and say so in the register's preamble.

Related to OI-61 — both are guards that promise more than they check.

**Closes when:** you pick an option.

### OI-61 — the "verbatim" fidelity check is case- and punctuation-blind

`test_declared_verbatim_fields_are_verbatim` compares through `_flat`:

```python
def _flat(text): return re.sub(r"[^a-z]", "", text.lower())
```

Everything but the letters is thrown away. So the check that gives
`VERBATIM_FIELDS` its meaning cannot see:

- case — "Dara karaka" against "Dara Karaka" (OI-60);
- punctuation — "&" against "and", parentheses, commas;
- word boundaries — a phrase split differently still matches.

It catches a paraphrase, not a normalisation — the failure mode
`core/constants/karaka.py`'s own docstring warns about. §8.3's list is a live
instance: the book capitalises every relative, we store lowercase, and the
check is satisfied.

The flattening exists because PDF extraction inserts line breaks and
hyphenation. But only whitespace and soft hyphens genuinely need normalising;
case and punctuation survive extraction fine.

Proposed: a second, stricter comparison that collapses whitespace and soft
hyphens only, run alongside the existing one. Not written, because the check is
PDF-gated and cannot be run here to see what it flags.

The docstring has been corrected to state the real guarantee, and
`test_the_verbatim_check_is_case_and_punctuation_insensitive` pins the
weakness so it is not mistaken for a stronger one.

**Run 2026-08-27: all 109 fidelity checks pass** — weaker evidence than it
sounds, since the comparison cannot see either known discrepancy and would
pass whether or not they were fixed.

**Closes when:** the stricter comparison is written and run against the PDF,
and whatever it flags is settled.

### OI-60 — Table 13 prints "Dara karaka" with a lowercase k; we store "Dara Karaka"

Table 13's Karaka column reads: Atma Karaka, Amatya Karaka, Bhratri Karaka,
Matri Karaka, Pitri Karaka, Putra Karaka, Jnaati Karaka, **Dara karaka**.

Seven rows capitalise "Karaka"; row 8 does not. Almost certainly the author's
slip, but `CHARA_KARAKAS["name"]` is a **declared-verbatim field**
(`VERBATIM_FIELDS` in `core/constants/karaka.py`), and a declared-verbatim
field must match character for character. Ours reads "Dara Karaka".

This is the failure mode that module's own docstring warns about: chapter 2
lost three of the author's typos to silent normalisation before anyone noticed.

Two ways to settle it, and they point opposite ways:

- **Transcribe faithfully** — store "Dara karaka". Keeps the verbatim
  guarantee true, changes API output for one row.
- **Drop `name` from `VERBATIM_FIELDS`** — admit the names are normalised, and
  the guarantee no longer covers them.

Not acting either way. The API name is a published string.

**Closes when:** you pick one, or JHora's own label settles it.

### OI-59 — the equal-house scheme §7.5 describes is not the one we call `equal_lagna`

§7.5: "In the "equal house method", they take a 30º arc **with center at
lagna** as the 1st house."

Centred, not starting. Measured against the ephemeris for JD 2451545.0 at
Hyderabad:

| Setting | Swiss code | Ascendant | 1st cusp | Offset |
|---|---|---|---|---|
| `equal_lagna` | `A` | 72.2904 | 72.2904 | 0º |
| `vehlow_equal` | `V` | 72.2904 | 57.2904 | 15º |

So §7.5's "equal house method" is our `vehlow_equal`; `equal_lagna` is a
different scheme (JHora's "Equal housing", first cusp at the lagna degree).

**No calculation is wrong.** PVR recommends neither, and the default is whole
sign, so nothing we ship uses either. The risk is a caller who reads §7.5 and
picks `equal_lagna` expecting the book's description.

Options: (a) leave both, document which is which in the enum docstring;
(b) rename. Not acting either way.

**Closes when:** you say whether to document or rename, or JHora's own
"Equal housing" output settles which construction it means.

### OI-58 — §7.4.4 inverts a house reading with strength; nothing computes it

"If a dusthana is fortified or afflicted by malefics, it may show serious
obstacles. If a dusthana is weak, it shows that obstacles will be easily
overcome. For example, exalted 8th lord may show a lot of troubles and
debilitated 8th lord may show easy sailing."

The dusthanas are the only §7.4 category whose reading **flips** with strength:
everywhere else a strong house is good news. Both inputs exist — `sign_dignity`
gives exalted/debilitated, `category_houses` gives the dusthanas — but nothing
reads them together, so a caller asking about the 8th gets "setbacks and
obstacles" whether its lord is exalted or debilitated.

Related to OI-57: both are §7.4 rules whose two halves are built and unjoined,
and both wait on the strength chapters for what "fortified" and "weak" mean as
thresholds.

**Closes when:** the strength chapters define fortification, and a house
reading consumes dignity.

### OI-57 — §7.4.1's digbala rule joins two tables nothing connects

"Digbala of planets who attain full digbala in various of these trines shows
the strength of different purushaarthas in one's life."

Both halves exist: chapter 3 gives each graha its digbala house (`Mercury and
Jupiter` the 1st, `Sun and Mars` the 10th, `Moon and Venus` the 4th, `Saturn`
the 7th) and §7.4.1 gives the four purushaartha trikonas. Nothing joins them.

The join is discriminating: the four digbala houses are 1, 4, 7 and 10 — one in
each purushaartha — so a chart's digbala pattern maps directly onto which of
the four goals is strong.

**Closes when:** the strength chapters settle what "attains full digbala"
means as a threshold, and something consumes the mapping.

### OI-56 — §7.3.9's strength rule needs a graha-versus-lagna comparison

"If Mars is stronger than lagna, then the 3rd house from Mars may be more
important than the 3rd house from lagna."

The only place chapter 7 says how to **choose** between two references rather
than which to use for what. Table 12's six pairs each give a house from lagna
and the same house from a graha; this rule decides which to weigh more.

Not implemented. It needs a strength comparison between a graha and the lagna —
chapter 15 has graha strength and rasi strength, but nothing compares the two
kinds. `GRAHA_LAGNA_STRENGTH_RULE` records the statement.

**Closes when:** chapter 15's sweep settles what "stronger than lagna" means,
or a later chapter defines it.

### OI-54 — §6.6.3's two amsa yogas are not implemented

"lagna lord or ghati lagna lord in Simhaasanaamsa would make one very famous. A
quadrant lord with good amsabala in dasavarga makes one very successful."

Both are stored in `DASAVARGA_COMBINATIONS` and neither is computed. They need
the yoga chapters, and the second needs a threshold for "good amsabala" that
§6.6 never gives.

This was cited in code before it existed here — a dangling reference, found by
grepping `src/` and `tests/` for OI numbers and checking each against this file.
Worth repeating that sweep occasionally.

**Closes when:** the yoga chapters are reached and "good amsabala" is defined.

### OI-53 — three served vargas are not in the book

`/v1/varga/rules` serves **23** divisional charts. Chapter 6 defines **twenty**.

The extras are **D-81** (Nava Navamsa), **D-108** (Ashtottaramsa) and **D-144**
(Dwadas Dwadasamsa) — composites: D-9 of the D-9 longitude, D-12 of the D-9,
D-12 of the D-12. PVR defines none of them. They have no Table 11 signification
and no worked example, and §6.4's planes do not name them (though "above 36"
would take them).

They are a known classical construction and are almost certainly right, but
"almost certainly right" is what D-5 and D-11 looked like before the sweep —
both were written from general knowledge rather than from PVR, and both were
wrong (D-12, D-14).

**Not removed.** They are harmless while nothing consumes them, and JHora
computes them. `test_three_served_charts_are_not_in_the_book` pins the set so a
fourth cannot appear unnoticed.

**Closes when:** they are verified against JHora, or a PVR source defining them
is found, or they are withdrawn.

### OI-52 — §6.2.2 calls the D-2 rule "not quite complete"

"Though absolutely correct, the above is not quite complete. Proper use of hora
chart is beyond the scope of this book. So we will ignore and not use hora
chart in this book."

So `d2_hora` implements a rule PVR himself says is **incomplete**, and the
completion is nowhere in the book. All four cases of the stated rule reproduce,
and D-2 places every body in Cancer or Leo — but if the missing part changes
that, our D-2 is wrong in a way no worked example can reveal, because **the
book gives D-2 no worked example**.

D-2 is in `SHADVARGA` and `SHODASAVARGA`, so it carries a weight in amsabala.
Chapter 6's Example 27 exercises amsabala and reproduces, which bounds the risk
but does not remove it.

**Closes when:** the completion is found — in BPHS (as a gap-fill, never an
override; see [OI-51](#oi-51)), in PVR's later writings, or against JHora.

### OI-51 — §5.7 names more Parasara lagnas that the book leaves out

"There are some more special lagnas defined by Parasara, but they are beyond
the scope of this book. We will restrict ourselves to the ones defined in this
book."

So the four we implement — BL, HL, GL, SL — are not the whole Parasari set.
The rest will arrive from BPHS, with **no PVR text to check them against**.

**The rule, confirmed with Amit 2026-08-26 and written into
[precedence.md](precedence.md):** BPHS may *fill a gap* PVR leaves, but may
**never override** him without an explicit decision recorded case by case. The
temptation here will be to let BPHS quietly become the authority for anything
the book puts out of scope. Filling is fine; overriding is not.

**Closes when:** the BPHS work reaches special lagnas, and each additional one
is either implemented from BPHS as a gap-fill or deliberately left out.

### OI-50 — umbrella APIs: five design decisions, deferred

A front end must call many of the ~80 endpoints and join them. An umbrella is
wanted, **deferred 2026-08-26** until the chapters are done — chapters 16+ are
what a real reading assembles, so designing it now means guessing at the
consumer.

**Shape, when we build it.** Not one per chapter; two, split by whether a chart
is needed: `GET /v1/reference/book` (static tables and rules) and
`POST /v1/reading/chart` (panchanga, positions, dignity, relationships,
arudhas, strength, houses, vargas). Both alongside the existing endpoints.

**The five decisions, unanswered:**

| # | Decision | My recommendation |
|---|---|---|
| 1 | Input: nativity or explicit longitudes? | Accept **both**; one required |
| 2 | Section selection — `?include=...`? | **Yes**, default to all |
| 3 | If one section cannot be produced, does the whole call fail? | **No** — that section returns `available: false` with a reason |
| 4 | Expose chapter 15 strength as it stands, or finish §15 first? | Finish first |
| 5 | Sweep chapters 9 and 15 to sentence level before wrapping them? | **Done.** Both were swept screenshot by screenshot; the note claiming otherwise was stale. See OI-8 |

**Keeping the cost down meanwhile:** every chapter's endpoints follow the same
shape — `/rules`, `/compute`, and a chart-level view where a chart applies, as
`/v1/relationship/chart` does. Then the umbrella is assembly, not redesign.

**Closes when:** the chapters are done and these five are answered.

### OI-49 — §3.4.2 excludes the nodes; nothing states why

Example 4 proves §3.4.2 counts only the classical seven: Rahu sits in the 9th
from the Sun and the book still calls Saturn "the **only** temporary enemy".
`charts/relationship.py` therefore excludes the nodes by default, and
`include_nodes=True` is available for a caller who wants them.

But the book gives no *rule* saying so — only the example's silence. JHora may
count them.

**Closes when:** JHora's temporary-relationship treatment of the nodes is
confirmed, or a later chapter states the rule.

### OI-48 — `charts/avastha.py` still reads the fixed benefic sets

§3.2.2's conditional rules are implemented in `charts/benefic.py` (OI-45,
closed), but
`charts/avastha.py` reads `NATURAL_BENEFIC`/`NATURAL_MALEFIC` directly at three
sites, so a waxing Moon still never counts as a benefic aspect and Mercury
never counts either way. Wiring it in moves live `/v1/avastha` output and needs
paksha and co-tenants threaded through.

**Closes when:** you approve the avastha change — it belongs with the four
decisions above.

---

## Parked

### OI-7 — chart drawing styles (South/North/East Indian) · **OUT OF SCOPE**

Deliberately not built. This is a calculation API; rendering belongs to the
client. Not a gap.

### OI-10 — sunrise definition · **SUPERSEDED** by OI-19

---

**Design decisions are not open items.** A settled, tested choice in the API
contract lives in [api-contract.md](api-contract.md#design-decisions). This file
is for what is still unresolved.
