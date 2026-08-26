# Which source wins

Every astrological question this engine answers has more than one candidate
answer in the literature. This document fixes the order of precedence so that a
disagreement is resolved by rule, not by whoever happens to be implementing.

## The principle

**P.V.R. Narasimha Rao is the gold standard, and his calculation is what we
implement.**

He takes Brihat Parashara Hora Shastra as his base, which is correct — BPHS is
the foundational text of Parashari astrology. But BPHS as it survives is not a
single fixed text:

- It comes down in **multiple recensions** with different verse counts and
  different chapter orders.
- Printed editions disagree with each other. The Sharma, Santhanam and
  Rangacharya translations do not always render the same rule the same way.
- Manuscripts accumulated **interpolations and copyist corruption** over
  centuries of transmission, as Sanskrit texts generally did.

So "BPHS says X" is often not a single fact but a claim about one recension.
Where PVR's reading differs from a commonly cited BPHS reading, **we follow
PVR** and record the difference. We do not assume the divergence is his error;
it may equally be that his manuscript is sounder, or that the common reading is
a corruption.

We also do not treat BPHS as irrelevant. A disagreement with BPHS is a **flag
for research**, not something to bury — see OI-15 for a live example.

**BPHS never overrides PVR silently.** It may override him only by an explicit
decision recorded here, taken case by case with the evidence set out — the same
bar as any other change to a calculation. Absent that decision, PVR stands.
Confirmed with Amit on 2026-08-26. This matters ahead of the BPHS work, because
several things the book puts out of scope — §5.7's "some more special lagnas
defined by Parasara", for instance — will arrive from BPHS with no PVR text to
check them against, and the temptation will be to let BPHS fill the gap by
default. Filling a gap is fine; overriding is not.

## The ladder

Resolved top down. The first rule that applies decides.

| Rank | Source | Notes |
|---|---|---|
| **1** | **Jagannatha Hora 8.0** (2016) | The benchmark. PVR's own software, and his latest word. Outranks the book where they differ. |
| **2** | **The book — *Vedic Astrology: An Integrated Approach*** (2000) | Definitional sections and tables outrank prose and worked examples. |
| **3** | **PVR's later writings** — his articles and the 2010 "Looking Back" note | Used to interpret 1 and 2, not to overrule them. |
| **4** | **BPHS and other classical texts** | Context and research input. Recorded when it disagrees; never silently substituted. |
| **5** | **Modern consensus / other software** | Weakest. Useful as a cross-check (PyJHora) but never decisive. |

### Why JHora outranks the book

PVR wrote in March 2010:

> "my astrology studies and research continued and my knowledge has been
> considerably refined. I have refined several calculations and concepts shared
> in this book"

The book is from 2000; JHora 8.0 is from 2016. Where the two differ, the later
and actively maintained one is his current position.

**Today this is theoretical**: no JHora output has been recorded yet
([OI-1](open-items.md#oi-1)), so in practice rank 2 is deciding everything. Once
JHora output exists, any place it contradicts the book gets re-opened.

## When PVR contradicts PVR — STRICT RULE

The book is not internally consistent. This is not a footnote; it is a standing
hazard, and it is governed by a hard rule.

### The rule

> **A PVR-versus-PVR conflict is NEVER resolved silently, NEVER split, and NEVER
> averaged. It is resolved by the ladder below, registered in the table below,
> and encoded with a comment naming its PVR-id.**

Splitting the difference between two PVR statements is forbidden outright. One
of them is what he meant; a value that is neither is what nobody meant.

### Tie-break ladder — apply in order, first match wins

| Order | Rule | Rationale |
|---|---|---|
| **1** | **A stated derivation rule beats everything.** Compute from it. | If the book says how to derive a table, the derivation is the author's own method and outranks any transcription of its output. |
| **2** | **A definitional section beats a passing mention.** | A section whose stated purpose is to define X is more authoritative on X than a place that merely uses X. |
| **3** | **A table beats prose.** | Tables are compiled deliberately; prose in a worked example is written once. |
| **4** | **A direct reference beats an indirect one.** | §7.5, PVR's own words: "there are some *indirect* references in BPHS suggesting that Parasara supported house divisions placing houses in 2 rasis, [but] there are quite a few *direct* references making it amply clear that each house falls in one rasi." He does not deny the indirect references exist; he ranks them. This applies within any source, and is the rule BPHS work will lean on hardest. |
| **5** | **Corroboration elsewhere in the book breaks a tie.** | A statement repeated elsewhere is likelier than an isolated one. |
| **6** | **Nothing resolves it → OPEN item.** | A guess is never acceptable. It waits for JHora. |

### Mandatory registry

Every conflict found gets an id here. No exceptions, including ones judged
trivial — a conflict that looked trivial is how a wrong default gets in.

| id | Conflict | Sources | Resolved by | Outcome | Deviation |
|---|---|---|---|---|---|
| **PVR-1** | Gemini's body part | §2.2.1 "arms" vs §2.3 "chest" | Rule 2 — §2.2.1 defines the limbs | arms | [D-3](book-deviations.md) |
| **PVR-2** | Saturn as a natural malefic | §3.2.2 omits it vs p.102 "Malefics like Mars, Saturn and nodes" | Rule 4 — corroborated on p.102 | Saturn is a malefic | [D-7](book-deviations.md) |
| **PVR-3** | Jupiter's relationship to Venus | Table 7 "enemy" vs Exercise 6 answer "neutral" | Rule 1 — §3.4.1's derivation rule reproduces Table 7 in all seven rows | enemy | [D-8](book-deviations.md) |
| **PVR-4** | Mars's moolatrikona sign | Table 6 "Ar" vs §3.3 rule 3 "first 12º of Le" | Rule 3 — table beats prose | Aries | [D-7](book-deviations.md) |
| **PVR-7** | D-27 in Example 23 | §6.2.16's rule (count from Ar/Cn/Li/Cp by element) vs the example's "The 10th from Li is Le" | Rule 1 — the stated rule beats its transcribed output; Leo is the 11th from Libra, not the 10th | Cancer | [D-15](book-deviations.md) |
| **PVR-6** | Bhaava Lagna's rate | §5.2's stated rate, restated rate and own illustration (0.25°/min) vs its numbered method and Example 7 (1°/min) | Rules 2 and 4 — the definitional statement, corroborated twice within the section | 0.25°/min | [D-11](book-deviations.md) |
| **PVR-5** | Upaketu in Exercise 7 | Table 9's two formulas (both give 13°19' Ar) vs the §4.4 answer "19°1' Sc" | Rules 1 and 3 — a derivation rule beats its transcribed output, and a table beats prose | 13°19' Aries | [D-9](book-deviations.md) |
| **PVR-9** | DK in Example 28 | §8.2's procedure (decreasing advancement) vs Table 14's last row "Venus 2º28' 8 DK" | Rule 1 — the stated procedure beats its transcribed output; Venus is already MK at 17º21', and 2º28' is Saturn's | Saturn | [D-17](book-deviations.md) |
| **PVR-8** | D-3 in Example 27 | §6.2.3's rule (last 10º goes to the 9th from the rasi) vs the example's "D-3: Li" for 29º49' Sg | Rule 1 — the stated rule beats its transcribed output; Leo is the 9th from Sagittarius, Libra is the 11th | Leo | [D-16](book-deviations.md) |

### Obligations on every entry

1. **Register it here before encoding it.** The id exists first.
2. **Cite both sources with section numbers**, so the conflict can be re-checked
   against the book by anyone.
3. **Name the tie-break rule used.** "It seemed obvious" is not a rule.
4. **Comment the code** with the PVR-id at the definition site.
5. **Re-open it when JHora output arrives.** Every one of these is a place where
   the book is unreliable, which makes it exactly where JHora is most needed.

## When we depart from PVR

Rarely, and never silently. One case so far:

- **[D-6](book-deviations.md)** — §3.2.7 prints "Saturn and Mercury are female"
  immediately after "Moon and Venus are female". Two groups cannot both be the
  female group, and the classical value is neuter. Recorded as neuter by
  explicit decision on 2026-08-25.

Everything else the book prints is preserved as printed, including its typos
(`garrages`, `uproght`, `slender buils`) and its non-standard readings
(earthy signs as vaata).

## Obligations

Whatever the ladder decides:

1. **Record the divergence** in [book-deviations.md](book-deviations.md) with
   what each source says.
2. **Measure the repercussion** in astrological terms — does a planet change
   sign, nakshatra, pada, varga or dasa date, and in what fraction of charts.
   D-4 changes the node's dignity in 33% of charts; D-5 in about 1 in 360.
   Arcseconds are not an answer.
3. **Open a research item** when the loser is a serious source, so the choice
   can be revisited. BPHS disagreements always qualify.
4. **Never let a divergence change a default without approval** — see
   [verification-standard.md](verification-standard.md).
