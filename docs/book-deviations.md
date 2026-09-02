# Where the book departs from convention

Places where *Vedic Astrology: An Integrated Approach* states something that
differs from a convention held elsewhere.

**Policy: follow PVR.** He wrote both the book and Jagannatha Hora, and JHora is
our benchmark. Silently "correcting" him would move us away from the target and
hide a real disagreement. Each deviation is encoded as printed and recorded here.

The full order of precedence — including why a commonly cited BPHS reading does
not overrule PVR, and how PVR-versus-PVR conflicts are broken — is in
[precedence.md](precedence.md).

---

## Where we stand against the book

Asked directly on 2026-08-26: *are we differing from the book?* The honest
tally, so it does not have to be reassembled from 24 entries each time.
Last revised 2026-08-27, after chapter 10.

**1. Ten internal conflicts (PVR-1 to PVR-10), nine resolved by rule.** The book
says X in one place and not-X in another; we pick one. These are not
disagreements with the book — they are places the book disagrees with itself,
adjudicated by the ladder in [precedence.md](precedence.md), which was written
before any of them arose: a stated rule beats its transcribed output, a table
beats prose, a definitional section beats a passing mention. **PVR-10 is the
one the ladder does not settle** — §10.6's "several malefics" rule is not
computable, so there was nothing to outrank Exercise 16's output with. Open as
[OI-65](open-items.md); the threshold is a per-call parameter, not a baked-in
constant.

**2. One departure from printed text, with internal support: D-6.** §3.2.7
prints "Saturn and Mercury are female" after already naming Moon and Venus as
the female group. We record neuter. The section's own worked example puts
Mercury on both the son and the daughter side, which only holds if Mercury
takes the sex of its company.

**3. Where we follow the book *against* modern convention** — the opposite of
differing: node exaltations in Gemini/Sagittarius (D-4), Mercury's moolatrikona
at 15° (D-5), the dosha assignment (D-1), upper-limb sunrise (D-10).

**3a. Book typos we transcribe rather than correct.** "Graha Drishri" for
Graha Drishti (D-24), two spellings each for subhaargala and paapaargala
(D-25), two different word-lists for the same reading in §10.5 and §10.7
(D-26), and two slips in §18.5's interpretation warning (D-56). None changes a
calculation; all would vanish under a "tidy-up" pass, and D-20 already showed
that costs real information. Chapter 18 adds two of a different kind, where the
book's own numbers disagree with each other rather than with ours: a
transposed antardasa pair (D-57), pratyantardasa dates that do not divide the
antardasa they are cut from (D-58), and an antardasa given 8 months where the
same sentence says 10 (D-60).

**4. Live divergences: one known-wrong, and undecided ones at D-52, D-53 and D-59.**

**[OI-36](open-items.md) — known wrong.** `ABHIJIT_END` runs
53'20" past what §1.3.6 defines, because classical Muhurta convention was
layered on top of PVR's sentence during Phase 1. The book does **not**
contradict itself here — our code contradicts an unambiguous statement. It is
unfixed only because the decision is deferred.

**[OI-68](open-items.md) — undecided.** Our `node_type` default is `true`.
Chart 6 prints its own birth data, and recomputing it reproduces every body to
one arcminute **only with the mean node**; under `true`, Rahu is thirty-nine
arcminutes out. This is the first hard evidence in the project about which
convention the book uses and it points against our default. One chart is one
data point, so it is registered rather than acted on — but it is a place where
our output and the book's printed output genuinely differ.

---

## D-1 · §2.2.6 — Ayurvedic humours of the rasis

**The book says:**

| Humour | Rasis | Element group |
|---|---|---|
| Pitta | Ar, Le, Sg | fiery |
| Vaata | Ta, Vi, Cp | earthy |
| Kapha | Cn, Sc, Pi | watery |
| Mixed | Ge, Li, Aq | airy |

**The section contradicts itself.** §2.2.6 states the compositions in its own
prose, two paragraphs above the assignment:

- pitta = fire + water
- vaata = air + ether
- kapha = earth + water

Applied to the sign elements, that would put **airy** signs in vaata and
**earthy** signs in kapha. The book instead assigns earthy signs to vaata,
watery signs to kapha, and leaves airy signs "mixed".

So this is an inconsistency **inside §2.2.6**, not between the book and modern
Ayurveda. An earlier version of this file and of the code comment in
`constants/rasi.py` credited the compositions to "conventional Ayurveda"; PVR
states them himself. Corrected 2026-08-26.

`test_2_2_6_the_compositions_do_not_give_the_sign_assignment` pins the
disagreement so nobody later "fixes" `RASI_DOSHA` to follow the formula.

**What we do:** encode the book's assignment verbatim in `RASI_DOSHA`
(`src/hora/core/const.py`), with the deviation flagged at the definition.

**Open question:** whether JHora reports the same mapping. Tracked as part of
[OI-8](open-items.md#oi-8).

---

## D-10 · §5.5 — sunrise is the upper limb  · **supersedes an earlier choice**

**The book says**, in §5.5 comment (3):

> "Some people define sunrise as the time when the **center** of the visual disk
> representing Sun rises on the eastern horizon … Some other people consider
> sunrise as the time when the **upper tip** of the visual disk representing Sun
> appears to be rising … **The latter approach is recommended.**"

**What we did before.** On 2026-08-25 the default was set to
`traditional_hindu` — Swiss Ephemeris `BIT_HINDU_RISING`, disc centre with no
refraction — because PyJHora uses it and reproducing PyJHora made sunrise,
sunset, moonrise and moonset agree to the second.

**Why that changed.** [precedence.md](precedence.md) puts the book at rank 2
and PyJHora at rank 5, "never decisive". Chapter 5 contains an explicit
recommendation from PVR himself. Applying our own ladder consistently means the
book wins. Approved 2026-08-26.

**Repercussion — measured.** Sunrise moves **+3.7 minutes** at the reference
place and date. Everything anchored to sunrise moves with it:

| | Effect |
|---|---|
| Ghati Lagna | **4.6°** — and §5.5 calls GL the most birthtime-sensitive point in the chart |
| Hora Lagna | 1.8° |
| Bhaava Lagna | 0.9° |
| Panchanga | the limb current *at sunrise*, and the vaara boundary |
| Upagrahas | all eight day/night parts, so all six time-based upagrahas |

**Open.** PyJHora reproduced `BIT_HINDU_RISING` exactly, which is real evidence
about how JHora behaves — it is simply outranked, not refuted. If JHora turns
out to use disc-centre, the book's recommendation and the software disagree and
rank 1 wins. Tracked as [OI-19](open-items.md#oi-19).

---

## D-11 · §5.2 — Bhaava Lagna's rate contradicts its own method

**The section says three things that give 0.25°/min:**

- "It moves at the rate of one rasi per 2 hours."
- "Bhavalagna moves at the rate of 1° per 4 minutes (*i.e.*, 15° per hour)."
- Its own illustration: sunrise 06:00 with the Sun at 6s 4°47', and 6s 19°47'
  at 07:00 — fifteen degrees in sixty minutes.

**And a fourth, found 2026-08-26.** The illustration paragraph opens

> "then, **horalagna** is at 6s 4°47' at 6:00 am, at 6s 19°47' at 7:00 am..."

and closes "**Bhavalagna** moves at the rate of 1° per 4 minutes". The numbers
settle which is meant: 6s 4°47' at 06:00 to 6s 19°47' at 07:00 is **15° an
hour**, which is Bhaava Lagna's rate. Hora Lagna moves 30° an hour, so the
illustration cannot be its. "horalagna" there is a slip for "bhavalagna", and
the paragraph is a *fourth* statement of the 0.25°/min rate rather than a
statement about a different lagna.

**Where the slip came from, confirmed 2026-08-26.** §5.3's illustration is the
same one with the times halved:

| Longitude | §5.2 says | §5.3 says |
|---|---|---|
| 6s 4°47' | 6:00 am | 6:00 am |
| 6s 19°47' | 7:00 am | 6:30 am |
| 7s 4°47' | 8:00 am | 7:00 am |
| 8s 4°47' | 10:00 am | 8:00 am |

Identical longitudes; elapsed times **exactly double** at every point, which is
precisely the 15°/h versus 30°/h difference. §5.2's paragraph is §5.3's
re-timed for the slower lagna, and the word "horalagna" was left behind in its
first sentence. That is not an inference about intent — the two paragraphs are
the same illustration.

**And two that give 1°/min:**

- The numbered method: "Convert the difference into minutes. The result is the
  advancement of bhavalagna since sunrise, **in degrees**."
- Example 7, which adds 766° for 766 elapsed minutes.

At 1°/min Bhaava Lagna would advance **60° an hour — twice Hora Lagna's
speed** — contradicting "one rasi per 2 hours" outright and inverting the whole
family, in which Bhaava is meant to be the slowest.

**What we do:** the stated rate, 0.25°/min. Example 7's printed answer of
10°17' Pisces becomes 5°47' Leo. Registered as **PVR-6**.

The book notes that Bhaava Lagna "is defined only for the sake of completeness.
We will not use it in this book", which is the likely reason the error survived.

Hora Lagna's and Ghati Lagna's methods are correct: "divide by 2" is 0.5°/min
and "multiply by 5, divide by 4" is 1.25°/min, and every one of their worked
examples reproduces exactly.

---

## D-2 · §2.2.11 — "prishthodaya"

The book notes this itself, in a footnote:

> Many scholars have interpreted "prishthodaya" as "rising with the feet". So we
> will use the same interpretation. However, strictly speaking, one should note
> that "prishtha" means "back".

**What we do:** follow the book — `prishthodaya` means feet-first rising.
Naming only; no calculation depends on the etymology.

---

## D-3 · §2.2.1 vs §2.3 — body parts disagree for Gemini and Libra

The book gives the limbs of the kaala purusha in §2.2.1, then repeats body
parts inside the indication lists in §2.3. Two do not match.

| Rasi | §2.2.1 says | §2.3 says | Assessment |
|---|---|---|---|
| Gemini | arms | **chest** | genuine conflict |
| Libra | space below navel | **groins** | same region, different wording |

Gemini is a real disagreement. Classical BPHS assigns Gemini the arms and
shoulders, which agrees with §2.2.1, so §2.3's "chest" looks like a slip.

**What we do:** `RASI_LIMB` follows **§2.2.1**, the section whose stated purpose
is defining the limbs. §2.3's wording is preserved untouched in the content
store, so both readings survive and neither is silently discarded.

The other ten rasis agree between the two sections; that agreement is asserted
in `tests/content/test_rasi_indications.py`.

---

## D-4 · §3.3 Table 6 — Rahu and Ketu exalt in Gemini and Sagittarius

**The book says:** Rahu owns Aquarius, exalts in **Gemini**, debilitates in
Sagittarius, moolatrikona Virgo. Ketu owns Scorpio, exalts in **Sagittarius**,
debilitates in Gemini, moolatrikona Pisces.

**Many other texts** exalt Rahu in Taurus and Ketu in Scorpio. That was our
previous value.

**What we do:** follow the book. Approved 2026-08-25.

### Repercussions — measured, not estimated

- **The node's dignity label changes in about 33% of charts.** Measured over 400
  random charts: Rahu's label changed in 133, Ketu's in 133. Taurus and Scorpio
  stop being exaltation/debilitation; Gemini and Sagittarius start.
- **Node ownership is recorded as co-lordship only.** Table 6 gives Rahu
  Aquarius and Ketu Scorpio, which are Saturn's and Mars's signs. `RASI_LORD` is
  deliberately **unchanged**. Had ownership been applied there, two of every
  twelve house lords would be wrong, and house lordship, argala and dasa lords
  would all break. `CO_LORDS_ONLY` marks the distinction.
- **Fractional exaltation for the nodes stays undefined.** Table 6 gives the
  nodes an exaltation rasi but no deep-exaltation degree, so `EXALTATION_DEG`
  excludes them and `exaltation_score` returns the neutral 0.5. Nothing is
  invented. This will matter when uchcha bala is built.

**Still to research:** whether JHora agrees. Tracked as
[OI-14](open-items.md#oi-14).

---

## D-5 · §3.3 rule 4 — Mercury's moolatrikona starts at 15° Virgo

**The book says:** Mercury gives exaltation results in the first 15° of Virgo,
moolatrikona in the **next 5°** (so 15°–20°), own-sign in the remaining 10°.

**BPHS is commonly read as 16°–20°**, which was our previous value.

**What we do:** follow the book, 15°–20°. Approved 2026-08-25.

**Repercussion:** affects Mercury only between 15° and 16° of Virgo — roughly
one chart in 360, and only the dignity label.

**Still to research:** whether BPHS really says 16°, and which JHora uses. The
disagreement is a genuine concern, not a settled question. Tracked as
[OI-15](open-items.md#oi-15).

---

## D-6 · §3.2.7 — sex of Mercury and Saturn · **we depart from the book here**

This is the one place where we do **not** follow the printed text.

**The book prints:** "Sun, Mars and Jupiter are male. Moon and Venus are female.
Saturn and Mercury are female."

Two groups cannot both be the female group. The classical value for Mercury and
Saturn is **neuter** (napumsaka), and the sentence reads as a typo for it.

**The section settles it itself.** Added 2026-08-26, from the paragraph
immediately after the three sentences:

> "if the house ruling the first child is influenced by Jupiter, Mars and
> **Mercury**, we may predict a **son**. If it is influenced by Moon and
> **Mercury**, we may predict a **daughter**."

Mercury appears on **both** sides. With male planets it points to a son; with a
female planet it points to a daughter. That only works if Mercury takes the sex
of its company, which is exactly what neuter means. Were Mercury female as the
third sentence prints, it could not contribute to a son prediction at all.

This is stronger than the classical appeal it previously rested on: it is
internal evidence, from the same section, in PVR's own worked example. Pinned by
`test_3_2_7_the_sections_own_example_requires_mercury_to_be_neuter`.

**What we do:** record Mercury and Saturn as **neuter**. Decided explicitly on
2026-08-25, overriding the default policy of following the book verbatim, and
corroborated from the text itself on 2026-08-26.

Noted here precisely because it is an exception: everywhere else, a departure in
the book is preserved, not corrected.

---

## D-7 · §3.2.2 and §3.2.11 — two omissions in the book

**§3.2.2 omits Saturn from the natural malefics.** It lists only "Sun, Mars,
Rahu and Ketu". Searching the whole book resolves it: page 102 reads "Malefics
like Mars, **Saturn** and nodes…". So §3.2.2 is an omission, not doctrine.
`NATURAL_MALEFIC` keeps Saturn. No change was needed.

**§3.2.11 gives no abode for Mars.** Sun, Moon, Mercury, Jupiter, Venus and
Saturn each get one; Mars is simply absent. `GRAHA_ABODE[MARS]` is `None` rather
than a value borrowed from elsewhere.

**§3.3 rule 3 misprints Mars's moolatrikona** as "the first 12º of **Le**",
where Table 6 says **Ar**. Aries is correct and is what we hold; the rule text
is a typo.

---

## D-8 · §3.4.3 Exercise 6 contradicts Table 7 on Jupiter and Venus

**Table 7** lists Jupiter's natural enemies as Mercury **and Venus**.

**The Exercise 6 answer** (book page 39) says of Jupiter: *"Being a neutral
planet in natural relationship, Venus becomes an enemy in compound
relationship."* — calling Venus a natural **neutral**.

Both cannot hold. Table 7 is right, and it can be shown independently:

The derivation rule the book gives in §3.4.1 — friends are the lords of the
2nd, 4th, 5th, 8th, 9th and 12th from the moolatrikona, plus the lord of the
exaltation rasi — puts Jupiter's friendly rasis at Ar, Cn, Le, Sc, Cp, Pi.
Venus, lord of Ta and Li, appears in neither, so Venus is a natural **enemy**.
That reproduces Table 7 exactly, and all seven rows of Table 7 derive correctly
from the rule.

**What we do:** follow Table 7 and the derivation rule. Venus is a natural enemy
of Jupiter, so in Rama's chart (Venus a temporary enemy too) Venus is Jupiter's
**adhisatru**, where Exercise 6's prose says satru.

The other three worked examples — Example 4, Example 5 and the Venus half of
Exercise 6 — reproduce exactly.

**Strengthened 2026-08-26.** The derivation is no longer an argument on paper:
`charts/relationship.py:derive_natural` runs §3.4.1's rule, and
`test_3_4_1_the_derivation_reproduces_table_7` asserts it agrees with Table 7
in all **42** ordered pairs, Jupiter/Venus included. So the rule and its printed
table corroborate each other, and the Exercise 6 prose stands alone.

**The deviation is exactly one cell wide.**
`test_exercise_6_the_deviation_is_one_cell_wide` compares all twelve relations
across both halves of Exercise 6 and asserts that Jupiter→Venus is the only
disagreement. If a second ever appears, that test fails rather than the new one
passing unnoticed.

**It is also one-directional.** Exercise 6's Venus half calls Jupiter "a natural
neutral", which *is* Table 7's value for Venus→Jupiter. Only Jupiter's view of
Venus is disputed.


---

## D-9 · §4.4 Exercise 7 answer for Upaketu contradicts Table 9

**Table 9** defines Upaketu two ways, and they are the same thing:

- `Upaketu = Indrachaapa + 16°40'`
- `Upaketu = Sun − 30°`

Unrolling the chain confirms it algebraically: Dhuma is `Sun + 133°20'`, and
following Vyatipaata, Parivesha and Indrachaapa through leaves `Sun + 330°`,
which is `Sun − 30°`. Both forms are implemented and a test asserts they agree
for arbitrary Sun longitudes.

**Exercise 7** puts the Sun at 13°19' Taurus. Four of its five printed answers
reproduce exactly:

| | Ours | Book |
|---|---|---|
| Dhuma | 26°39' Vi | 26°39' Vi ✓ |
| Vyatipaata | 3°21' Li | 3°21' Li ✓ |
| Parivesha | 3°21' Ar | 3°21' Ar ✓ |
| Indrachaapa | 26°39' Pi | 26°39' Pi ✓ |
| **Upaketu** | **13°19' Ar** | **19°1' Sc** ✗ |

The formula gives Aries. The printed answer gives Scorpio.

**Where 19°1' Sc comes from is unknown.** An earlier version of this entry said
it was "consistent with the answer having been carried over from Example 6".
That claim does not survive checking: Example 6's Upaketu is **9°36' Sc**, so a
carry-over would print 9°36', not 19°1'. Only the *sign* coincides. Corrected
2026-08-26.

No arithmetic slip on either Table 9 form reaches 229°1' from a Sun at 43°19':
the two forms agree with each other exactly, and neither Dhuma, Vyatipaata,
Parivesha nor Indrachaapa plus any of the section's offsets lands there. The
answer is simply wrong, and we do not claim to know why.

**What we do:** follow Table 9. Registered as **PVR-5** in
[precedence.md](precedence.md), resolved by tie-break rules 1 and 3, which both
select the formula.

A source-fidelity test asserts the book really prints "19°1' from the start of
Sc", so the conflict cannot be mistaken for a transcription slip on our side.


---

## D-12, D-13, D-14 · Chapter 6 — three of our varga rules were wrong

Not deviations from the book: **defects in our implementation**, found when
chapter 6 was finally read. The vargas were written early, from general
classical knowledge rather than from PVR, and three of the twenty disagreed with
him. A sweep of all 36,000 longitudes against the book's rules found them.

### D-12 · D-5 Panchamsa

§6.2.5: "Bodies in the 5 parts of an odd rasi go into **Ar, Aq, Sg, Ge and Li**.
Bodies in the 5 parts of an even rasi go into **Ta, Vi, Pi, Cp and Sc**."

We ended the odd sequence in **Leo** instead of Libra, and had the even sequence
in the order Ta, Vi, Cp, Sc, Pi. **40% of longitudes were placed wrongly.**

D-5 is one of the charts the book gives **no worked example** for, which is
exactly why nothing caught it. `/v1/varga/rules` now marks which charts lack an
example, because those are where a transcription error can hide.

### D-13 · D-8 Ashtamsa

§6.2.8 counts from **Ar, Sg or Le** for movable, fixed and dual.

We used **Ar, Le, Sg** — the order the book gives for D-16 and D-45. The two
orders are printed separately and they differ; we had conflated them. **67% of
longitudes were placed wrongly**, and both halves of Example 15 failed.

**Example 15 also contradicts itself.** Found 2026-08-26. Its working says:

> "Because Ge is a dual rasi, counting starts from **Le**. The 3rd from Le is
> **Li**. So the 3rd part in Ge goes into **Li** in D-8."

and its closing sentence then says:

> "So Mercury is in **Le** and Jupiter is in Ta in D-8 for this example."

Le is the **starting sign** for dual rasis, not the destination. The summary
repeats the start where it means the result. The working is right and we follow
it — Mercury is in **Li**. Jupiter's half is consistent throughout.

This is a summary slip rather than a rule conflict, so it needs no PVR entry:
the section's rule and the example's own working agree, and only the one closing
clause disagrees with both. Pinned by
`test_example_15_summary_contradicts_its_own_working`.

### D-14 · D-11 Rudramsa

§6.2.11: "Count rasis from Ar to the rasi being divided, in the zodiacal order.
Count the same number of rasis anti-zodiacally from Ar. Bodies in the 11 parts go
into the 11 rasis starting from the rasi found thus."

The start is the natal rasi **reflected about Aries**. We had it counting
backwards from the twelfth sign — a guess made when the rule was marked
`PARITY: unverified`. **100% of longitudes were placed wrongly.**

Both halves of Example 18 now reproduce: Ge 11° gives Gemini, Sc 19° gives
Pisces.

---

## D-15 · §6.2.16 Example 23 miscounts by one

The rule is right and the example is wrong.

Example 23 places Mercury at 11° Gemini, correctly identifies the **10th** part
of 27, correctly starts from **Libra** because Gemini is airy — then says "The
10th from Li is **Le**".

Counting Libra as the first: Li, Sc, Sg, Cp, Aq, Pi, Ar, Ta, Ge, **Cn**. Leo is
the eleventh.

**What we do:** follow the rule. D-27 for 11° Gemini is **Cancer**. Registered as
**PVR-7**. The Scorpio half of the same example reproduces exactly, as do all
fifteen other worked examples in the chapter.

---

## D-16 · §6.6 Example 27 prints an inconsistent D-3

**Status: open** — the rule is right and the example is wrong, same pattern as
D-15.

Example 27 (page 76 of the PDF, printed 65) works Bill Cosby's amsabala.
Jupiter is at **29°49' in Sagittarius**, and the example lists his sign in all
sixteen charts. Fifteen of the sixteen reproduce exactly. The exception:

> `D-3: Li`

The book's own drekkana rule (§6.2.3, page 64 of the PDF) says bodies in the
**last 10°** of a rasi go to the **9th** from that rasi. Counting from
Sagittarius as the first: Sg, Cp, Aq, Pi, Ar, Ta, Ge, Cn, **Le**. Leo is the
9th; Libra is the 11th. Example 11 on the same page as the rule reproduces
exactly (Ge 3° → Ge, Ge 19° → Li, Ge 21° → Aq), so the rule is not in doubt.

**What we do:** follow the stated rule. D-3 for 29°49' Sagittarius is **Leo**.
Registered as **PVR-8**.

**Blast radius: nil.** Jupiter's good signs are Cn, Sg and Pi. Neither Libra
nor Leo is among them, so the D-3 cell is not counted in any group and every
amsa in the example is unaffected. We reproduce all four verdicts exactly,
chart for chart:

| Group | Charts counted | Book | Ours |
|---|---|---|---|
| shadvarga | D-1, D-2, D-9 | 3 → Vyanjanaamsa | 3 → Vyanjanaamsa |
| saptavarga | D-1, D-2, D-9 | 3 → Vyanjanaamsa | 3 → Vyanjanaamsa |
| dasavarga | D-1, D-2, D-9, D-16 | 4 → Gopuraamsa | 4 → Gopuraamsa |
| shodasavarga | D-1, D-2, D-9, D-16, D-20, D-24, D-40 | 7 → Kalpavrikshaamsa | 7 → Kalpavrikshaamsa |

**To close:** confirm against JHora 8.0 (OI-1) that it also prints Leo. Pinned
by `test_page_76_example_27_amsabala` in `tests/unit/test_book_pages.py`.

---

## D-17 · §8.2 Table 14 names the wrong planet in its last row

**Status: open** — the procedure is right and the table's transcription is
wrong. Same pattern as D-15 and D-16.

Example 28 (PDF page 92, printed 81) works the chara karakas for:

> Sun: 12Ge47, Moon: 20Ar28, Mars: 13Ge51, Mercury: 25Ge18, Jupiter: 5Ta40,
> Venus: 17Ge21, Saturn: 2Ta28, Rahu: 1Cn43

Table 14 lists all eight in decreasing advancement. Seven rows are right. The
last one reads:

> `Venus  2°28'  8  DK`

Venus cannot be DK: Venus is at 17Ge21, already listed three rows above as MK
with an advancement of 17°21'. The value 2°28' is **Saturn's** — Saturn is at
2Ta28, and it is the only graha missing from the table.

**What we do:** follow the procedure. DK in Example 28 is **Saturn**.
Registered as **PVR-9**.

**Blast radius: nil for the chapter's conclusions.** The example goes on to
discuss only AK (Rahu) and AmK (Mercury), both unaffected. Every other row
reproduces exactly, to the arcminute.

Exercise 11's answer (Table 17, printed 84) has no such error: all eight rows
reproduce exactly, including the one-arcminute gap between Rahu at 15°30' (BK)
and Moon at 15°29' (MK).

**To close:** confirm against JHora 8.0 that it also gives Saturn. Pinned by
`test_table_14_names_the_wrong_planet_in_its_last_row` in
`tests/unit/test_book_chapter8.py`.

---

## D-18 · §8.5 Table 17 repeats Table 14's caption

**Status: closed** — cosmetic, no calculation affected.

Table 17 (PDF page 95, printed 84) holds the answer to **Exercise 11**, but is
captioned:

> Table 17: Chara karakas in Example 28

which is Table 14's caption verbatim. The two tables hold different charts —
Table 14's AK row is Rahu at 28°17', Table 17's is Mercury at 21°0'.

**What we do:** nothing to compute. Recorded so the duplicate caption is never
mistaken for a second copy of Table 14, and pinned by
`test_table_17_repeats_table_14s_caption`, which asserts both that the caption
appears twice and that the two tables' contents differ.

All eight rows of Table 17 reproduce exactly.


---

## D-19 · §15.4.4 Table 36 has no row for a remainder of zero

**Status: open, and it sits behind [OI-26](open-items.md#oi-26)** — the whole
section is unverified transcription, so this deviation is provisional too.

The formula says to divide `(C x P x A) + M + G + L` by 12 and take the
remainder, then index Table 36 with it. Table 36 runs 1 to 12. A remainder of
zero indexes nothing.

**What we do:** read a remainder of zero as the **twelfth** state (Nidraa).
That is the only reading available — the twelve states must tile the twelve
residues, and 1 to 11 are already spoken for.

`avastha_by_activity` says so in its step 3 detail ("a remainder of 0 indexes
the 12th row") rather than silently normalising, and
`test_a_remainder_of_zero_indexes_the_twelfth_state` pins it.

**To close:** confirm against the book's own wording, and against JHora.


---

## D-20 · The tenth sayanaadi avastha is spelled two ways

**Status: closed.** Both spellings are the author's.

Table 36 prints:

> `10  Nriyalipsaa  Longing to dance`

and the results section a few pages later heads its list:

> **Results in Nrityalipsaa avastha:**

**What we do:** store "Nriyalipsaa" as the name, since Table 36 is the
defining table, and "Nrityalipsaa" as an alias, since the book prints it too.
The entries in `data/content/avastha_results.yaml` carry the results-section
spelling, because that is the heading they sit under.

### Correction to an earlier reading of this

An earlier pass **removed** the "Nrityalipsaa" alias, on the grounds that it
was a linguistically-motivated correction not in the book — *nritya* is dance,
so "Nriyalipsaa" looked like a typo someone had silently fixed. That reasoning
was sound but the evidence was incomplete: only Table 36 had been seen. The
results heading, supplied later, shows the author uses both.

The alias is restored. Recorded here rather than quietly reversed, because the
first judgement was made on partial evidence and the second should be visible
as a revision, not appear as though it had always been so.

Row 7's "Sabhaa (Sabhaa vasati)" is unaffected — that one is parenthesised in
Table 36 itself.

---

## D-21 · §9.2 Table 18 spells the third arudha two ways in one row

**Status: closed.** Transcribed as printed; nothing to compute.

Table 18's A3 row reads:

> `A3   Bhatrarudha, Bhratri pada, Vikramarudha, Vikrama pada`

**"Bhatrarudha"** and **"Bhratri pada"** — the first is missing the `r` the
second has. From *bhraatri* (brother), the expected form is "Bhratrarudha".

**What we do:** store both exactly as printed. Regularising the first to match
the second would be an unmarked correction inside transcribed data, which is
the failure [D-18](#) exists to prevent and which [D-20](#) shows costs real
information — there, a spelling that looked like a typo turned out to be the
author's second form, printed elsewhere in the book.

Pinned by `test_table_18_keeps_the_books_inconsistent_row`, which asserts
"Bhratrarudha" is **not** present.

---

## D-22 · §9.5 Exercise 13's hint says "respectively" and does not mean it

**Status: closed.** Cosmetic; the intended mapping is unambiguous.

Exercise 13's hint reads:

> Out of the 2 signs owned by Mars, Mercury, Jupiter, Venus and Saturn, Ar,
> Ta, Vi, Sg and Aq are stronger (**respectively**).

Taken as written, that pairs:

| Planet | Sign, literally | Owns it? |
|---|---|---|
| Mars | Ar | yes |
| Mercury | Ta | **no** — Mercury owns Ge and Vi |
| Jupiter | Vi | **no** — Jupiter owns Sg and Pi |
| Venus | Sg | **no** — Venus owns Ta and Li |
| Saturn | Aq | yes |

The five signs are listed in **zodiacal order**, and each belongs to exactly
one of the five planets, so the intended mapping is unambiguous:

    Ar -> Mars,  Ta -> Venus,  Vi -> Mercury,  Sg -> Jupiter,  Aq -> Saturn

**What we do:** read it by ownership. Our §15.5.2 cascade reaches all five
independently and agrees with every one, so nothing rests on the reading.

Recorded rather than silently reinterpreted, because "respectively" is a
precise word and a reader checking the exercise by hand will hit the same
snag. Pinned by
`test_exercise_13_hint_maps_by_ownership_not_by_its_stated_order`.

---

## D-23 · The four pillars are listed in two different orders

**Status: open** — cosmetic unless anyone indexes the pillars by number, which
the book itself does.

§1.3.5 introduces them:

> The science of Vedic astrology stands on the basis of 4 pillars – (1)
> *grahas* or planets, (2) *rasis* or signs, (3) *bhavas* or houses, and, (4)
> *varga chakras* or divisional charts.

§6.7's conclusion states the same four in a **different order**:

> The science of Vedic astrology stands on the basis of 4 pillars – grahas
> (planets), rasis (signs), vargas (divisional charts) and bhavas (houses).
> This chapter covered the **third pillar** – divisional charts.

| Pillar | §1.3.5 | §6.7 |
|---|---|---|
| 3rd | bhavas | **vargas** |
| 4th | varga chakras | **bhavas** |

§6.7 does not merely list them differently — it *counts* on its own order,
calling divisional charts the third pillar. Under §1.3.5's numbering they are
the fourth.

**What we do:** number them as §1.3.5 does, because that is the section that
defines them, and keep §6.7's order alongside as
`FOUR_PILLARS_CONCLUSION_ORDER` rather than resolving the disagreement by
silently preferring one. `/v1/util/tables/terms` returns both with a note.

Membership is not in dispute — both name the same four.

**To close:** confirm against JHora or a later PVR source which numbering he
intends, if either.

---

## D-24 · §10.2's heading is printed "Graha Drishri"

**Status: closed.** Recorded as printed; the term itself is spelled correctly
everywhere it is used.

The section heading reads:

> **10.2   Graha Drishri**

Every other occurrence in the chapter — §10.1's own sentence "There are 2 kinds
of aspects: (1) graha **drishti** and (2) rasi drishti", and §10.3's heading
"Rasi **Drishti**" one section later — spells it *drishti*. The `t` has become
an `r`.

**What we do:** `GRAHA_DRISHTI_HEADING_AS_PRINTED` holds the misprint;
`ASPECT_KINDS["graha_drishti"]["name"]` holds the term. Keeping both means a
reader searching the book for "Graha Drishri" finds it, and no code ever treats
"drishri" as a second kind of aspect.

Confirmed by Amit, 2026-08-27. Pinned by
`test_10_2_the_heading_is_printed_with_a_typo` and
`test_10_3_the_heading_is_spelled_correctly`, which asserts §10.3 sets the same
word correctly — which is what makes this a misprint rather than a variant.

---

## D-25 · §10.5 spells both argala natures two ways

**Status: closed.** Both spellings stored; the definitional forms are primary.

§10.5 defines them once:

> Argala by a benefic planet is called a "**subhaargala**" (benefic
> intervention) and argala by a malefic planet is called a "**paapaargala**"
> (malefic intervention).

Then uses the shorter forms in every example that follows:

> If Jupiter is in 5th house ... his **subhargala** (benefic intervention) on
> 4th will help one's education. If Rahu is in 5th house, his **papargala**
> (malefic intervention) on 4th will cause obstacles ...

Note §10.6 uses the long forms again — "this is a **paapaargala** (malefic
intervention)" — so the book alternates rather than switching once.

**What we do:** `ARGALA_BY_NATURE` carries "subhaargala" and "paapaargala",
the forms from the sentence whose stated purpose is to define them —
[precedence.md](precedence.md) tie-break rule 2, a definitional section beats a
passing mention. `ARGALA_NATURE_SPELLING_VARIANTS` records the short forms so
text matched against the book still resolves.

Same treatment as [D-20](#) and [D-21](#). Pinned by
`test_10_5_spells_both_terms_two_ways`.

---

## D-26 · §10.5 and §10.7 word the 2nd house's contribution differently

**Status: closed.** Both stored as printed; neither is a subset of the other.

Both sections work the same reading — what the argala houses contribute to
education/learning, read from the 4th house — and they name the same three
houses, the 5th, 7th and 2nd. Two of the three agree in wording. The 2nd does
not:

| House | §10.5 | §10.7 |
|---|---|---|
| 5th | intelligence | intelligence |
| 7th | interaction with others | interaction |
| 2nd | overall character and samskara | character, **grooming** and samskara |

§10.7 adds *grooming*, which §10.5 does not have; §10.5 has *overall*, which
§10.7 does not. So neither list contains the other, and "the same sentence
printed twice" is the wrong model.

**What we do:** `ARGALA_EXAMPLES` holds §10.5's wording and
`ARGALA_ROLE_EXAMPLES` holds §10.7's, each against its own section. Nothing
merges them.

This one is easy to lose: a reader checking the two sections against each other
would naturally normalise one into the other, and the fuller list would
disappear. Found by a test that assumed they matched and failed. Pinned by
`test_10_7_the_meanings_mostly_agree_between_10_5_and_10_7`.

---

## D-27 · §11.2.4 spells Budha-Aaditya two ways on one page

**Status: closed.** Heading spelling primary; the variant recorded.

The section heading reads:

> **11.2.4   Budha-Aaditya Yoga (Nipuna Yoga)**

and the worked reading four paragraphs below it reads:

> "Then that person has a powerful **Budha-Aditya** yoga in career."

One `a` dropped, on the same page. The heading also capitalises "Yoga" where
the prose does not.

**What we do:** the registry carries "Budha-Aaditya Yoga", the heading's form —
[precedence.md](precedence.md) tie-break rule 2, since the heading and the
Definition paragraph beneath it are what define the yoga.
`BUDHA_AADITYA_SPELLING_VARIANTS` records "Budha-Aditya", and the timing text
is stored with the short spelling as printed.

Same treatment as [D-20](#), [D-21](#) and [D-25](#). Pinned by
`test_11_2_4_the_name_is_spelled_two_ways_on_one_page`.

---

## D-28 · §11.3.6 Adhi Yoga's example does not satisfy its own rule

**Status: closed.** The rule is followed. Registered as
[PVR-11](precedence.md).

The rule:

> "If the natural benefics occupy **6th, 7th and 8th** from Moon, this yoga is
> present."

The example, immediately after it:

> "If Moon is in **Taurus**, Mercury and Jupiter in **Virgo** and Venus is
> **Leo**, then this yoga is present."

Counted inclusively from Taurus, Virgo is the **5th** and Leo the **4th**. The
6th, 7th and 8th from Taurus are Libra, Scorpio and Sagittarius, and the
example puts nothing in any of them. The example fails the rule outright, not
by one house.

**What we do:** implement 6/7/8 — [precedence.md](precedence.md) tie-break rule
1, a stated rule beats its transcribed output. The rule also matches the
classical Adhi Yoga, where the example matches nothing.

**The minimal repair**, recorded as an observation and not as a claim about
what PVR meant: with the Moon in **Pisces** instead of Taurus, Leo becomes the
6th and Virgo the 7th, and the example holds exactly. One substitution
reconciles them; changing the rule instead would need the houses to read 4th,
5th and 6th, which no source supports.

Pinned by `test_11_3_6_the_example_does_not_satisfy_the_rule`, which asserts
the example is **absent** under the rule, and
`test_11_3_6_the_rule_is_followed_not_the_example`.

---

## D-29 · §11.3 spells panaphara "panapara"

**Status: closed.** Both recorded; chapter 7's spelling is primary.

§11.3's first General Guideline reads:

> "If Moon is in a **panapara** from Sun, then one may possess average wealth"

Chapter 7 §7.4 names the category "panaphara" throughout, and
`HOUSE_CATEGORIES` uses that. The `ph` is dropped here.

**What we do:** the category keeps chapter 7's spelling, since §7.4 is the
definitional section — [precedence.md](precedence.md) tie-break rule 2 —
and `PANAPHARA_SPELLING_VARIANTS` records "panapara". Same treatment as
[D-20](#), [D-21](#), [D-25](#) and [D-27](#).

Pinned by `test_guideline_1_spells_panaphara_the_short_way`.

---

## D-30 · §11.4.5's definition calls Hamsa Yoga by Ruchaka's name

**Status: closed.** The heading is followed. Registered as
[PVR-12](precedence.md).

The heading:

> **11.4.5   Hamsa Yoga**

The Definition immediately beneath it:

> "If Jupiter is in a quadrant in own sign or exaltation sign, it is called
> **Ruchaka** yoga."

Ruchaka is **Mars's** yoga, defined four sections earlier at §11.4.1. The
sentence is §11.4.1's with the graha swapped and the name left behind — the
rest of it, down to "This yoga does not apply from Moon", is word for word the
same.

**Why the heading wins**, on three independent grounds:

1. §11.4 promises "5 kinds of great persons". Two yogas sharing a name leaves
   four names for five yogas, which the section cannot mean.
2. The Results paragraph beneath calls the native "swan-like", and *hamsa* is
   the Sanskrit for swan. Ruchaka has no such gloss.
3. The five yogas are one per element in the order Mars, Mercury, Saturn,
   Venus, Jupiter. Jupiter's slot is the fifth and cannot also be the first.

Tie-break rule 4 — corroboration elsewhere breaks a tie — and here three
separate things corroborate the heading.

**What we do:** the registry carries "Hamsa Yoga" for Jupiter's and "Ruchaka
Yoga" for Mars's, and a test asserts the five yogas have five distinct names.
`HAMSA_MISNAMED_IN_ITS_DEFINITION` records the misprint.

Pinned by `test_11_4_5_the_definition_calls_hamsa_by_ruchakas_name`.

---

## D-31 · §11.4.4 spells Maalavya two ways

**Status: closed.** Heading spelling primary; the variant recorded.

The heading reads "**Maalavya** Yoga"; the Definition beneath it reads "it is
called **Malavya** yoga". One `a` dropped, on the same page — the same slip as
[D-27](#), where §11.2.4's heading reads "Budha-Aaditya" and its worked reading
"Budha-Aditya".

**What we do:** the registry carries "Maalavya Yoga", the heading's form, and
`MAALAVYA_SPELLING_VARIANTS` records "Malavya".

Worth separating from [D-30](#) above, on the same two pages: this is a
spelling variant of the **right** name, that one is the **wrong** name. The
first is transcribed, the second is overruled.

Pinned by `test_11_4_4_maalavya_is_spelled_two_ways`.

---

## D-32 · §3.2.8 and §11.4 gloss the five tattvas differently

**Status: closed.** Both recorded; nothing to compute.

§3.2.8 writes each as "<Sanskrit> tattva (<adjective> **element**)" — for
instance "Aakaasa tattva (ethery element) is ruled by Jupiter". §11.4's bullet
list writes "Aakaasa tattva (ethery **nature**)", and calls the set "pancha
bhootas (five existences) or pancha tattvas (five **natures**)".

Same five, same order, same rulers — a different noun in the gloss.

**What matters is that everything else agrees.** `ELEMENT_RULER` and
`PLANET_ELEMENT_ADJECTIVES` were transcribed from §3.2.8 alone, and §11.4's
"Mars, Mercury, Saturn, Venus and Jupiter (respectively)" reproduces that order
exactly — which is the whole load-bearing part, since "respectively" fails if
the order differs. Eight chapters apart, with no cross-reference either way.

Pinned by `test_11_4_repeats_3_2_8_and_they_agree` and
`test_11_4_glosses_the_tattvas_differently_from_3_2_8`.

---

## D-33 · §11.5's classification and §11.5.3's headings disagree three times

**Status: closed.** The headings win; the variants are recorded.

§11.5 lists the twenty Aakriti yogas by name; §11.5.3 then defines them under
headings. The two passages disagree in three places:

| | §11.5's list | §11.5.3's heading | also |
|---|---|---|---|
| bird yoga | Vihanga**ma** | Vihanga | "Some authors call this **Vihaga** yoga" |
| half-Moon yoga | Ardhachandra | Ardha Chandra (two words) | |
| order | Sringaataka **before** Vihangama | Vihanga **before** Sringaataka | |

The third is not a spelling: the two passages put the same two yogas in
different order.

**What we do:** the registry carries the heading forms — "Vihanga Yoga" and
"Ardha Chandra Yoga" — since §11.5.3 is the definitional section and §11.5's
list is a passing mention ([precedence.md](precedence.md) tie-break rule 2).
`AAKRITI_NAME_VARIANTS` records "Vihangama", "Vihaga" and "Ardhachandra", and
"Vihaga Yoga" is carried as a registry alias so a caller matching that name
finds the yoga. The classification list itself is transcribed as printed, so
both forms survive.

Same family as [D-27](#) and [D-31](#), where a heading and the prose beneath
it disagreed — but this time the disagreement is between two *sections*, which
is why the ordering difference shows up too.

Pinned by `test_11_5_3_the_classification_and_the_headings_disagree_on_two_names`,
`test_11_5_3_vihaga_is_carried_as_an_alias` and
`test_11_5_3_the_classification_orders_two_yogas_differently`.

## D-34 · §11.6's example says Venus "is in a lagna" in navamsa; Chart 9 puts her in the 7th

**Status: recorded.** The chart wins; the sentence is transcribed as printed.

§11.6 closes its Kalpadruma example: "In navamsa also, Sun is exalted, Saturn
is in moolatrikona and Venus is in a lagna."

The first two hold against Chart 9's own drawn navamsa — the Sun in Aries,
Saturn in Aquarius. The third does not. The drawn navamsa puts Venus in Gemini
and the navamsa lagna in Sagittarius, so Venus is in the **7th** from it. Nor
is she with a special lagna: the same diagram draws HL in Taurus, AL in Libra
and GL with the ascendant in Sagittarius, and Gemini holds Venus alone.

Our D-9 reproduces all ten of Chart 9's drawn navamsa placements, so this is
not our computation disagreeing with the book — it is the book's sentence
disagreeing with the book's own diagram.

The likeliest reading is that "lagna" is a slip for "kendra": Venus in the 7th
*is* in a quadrant, which would make the sentence true and would parallel
"Sun is in a quadrant" in the rasi walkthrough two lines earlier.

**What we do:** nothing turns on it. The claim is not one of Kalpadruma's
conditions — those are decided in the rasi chart and the yoga is present for
Shivaji either way. The sentence is transcribed verbatim in
`KALPADRUMA_EXAMPLE_CONCLUSION`, the disputed phrase is isolated in
`KALPADRUMA_EXAMPLE_NAVAMSA_LAGNA_CLAIM`, and both readings are tested.

## D-35 · §11.6 says Lagnaadhi "means Adhi Yoga from lagna", but the two rules differ

**Status: recorded.** The definition is followed, not the gloss.

§11.6: "If (1) the 7th and 8th houses from lagna are occupied by benefics and
(2) no malefics conjoin or aspect these planets, then this yoga is present...
We have already seen Adhi Yoga among Chandra yogas. Lagnaadhi yoga means Adhi
Yoga from lagna."

§11.3.6's Adhi takes the **6th, 7th and 8th** from Moon. Lagnaadhi's own
definition takes the **7th and 8th** from lagna. If it were literally "Adhi
from lagna" it would take three houses, not two — and it adds a second clause
Adhi does not have, that no malefic conjoins or aspects those benefics.

**What we do:** the definition governs, per
[precedence.md](precedence.md) tie-break rule 2 — the sentence that states the
rule outranks the sentence that glosses the name. `LAGNAADHI_HOUSES` is
`(7, 8)` and `ADHI_HOUSES_FROM_MOON` is `(6, 7, 8)`, both served on `/rules`,
and a test builds one chart on which Adhi is absent and Lagnaadhi is present
so the difference is not merely asserted.

Note this is the second time §11.6 attaches a name to a rule that does not
match it — see D-30, where §11.4.5's Hamsa definition calls the yoga Ruchaka.

## D-36 · §11.7.2 puts Akbar's Venus in Uttamaamsa; the chart gives Paarijaataamsa

**Status: recorded.** Our count stands; the difference is one D-60 division.

§11.7.2, of Chart 10: "Venus and Saturn are only in Uttamaamsa and
Paarijaataamsa." Uttamaamsa is a dasavarga count of 3, Paarijaataamsa a count
of 2. Saturn agrees exactly. Venus does not — we count 2 for her as well.

**The whole disagreement is one division of one chart out of ten.** Venus's
shashtiamsa (D-60) leaves Taurus, her own sign, at exactly Libra 28°00'. She is
printed at **28 Li 10** and recomputes from Chart 10's own birth data to
**28 Li 10.3'**, ten arc-minutes past that boundary. Anywhere in Libra
27°30'–28°00' she counts 3, and the book and the engine agree.

Everything else §11.7.2 says about these two charts reproduces:

| claim | book | ours |
|---|---|---|
| Mars in Simhaasanaamsa | count 5 | 5 |
| Moon and Mercury "not even in Paarijaataamsa" | below 2 | 0 and 0 |
| Saturn | Paarijaataamsa | 2 |
| Venus and Saturn "less than a degree apart" | — | 0.70° |
| Jupiter "22° away from them" | 22° | 22.47° and 21.77° |
| Rajiv Gandhi's Sun and Jupiter in Simhaasanaamsa | count 5 | 5 and 5 |

**Not a rule difference.** Swapping the hora to parivritti would give Venus the
third chart, but it also lifts Mars to a count of 6 against the book's explicit
Simhaasanaamsa. No variant we support fixes one claim without breaking another,
and the Parashari hora is the definitional one. Checked and recorded rather
than tuned to fit.

**What we do:** nothing changes. The count is computed from §6.6's own
amsabala, which the same section's other five claims confirm.

## D-37 · §11.9 (12) names no planet for the 11th house, so no chart can satisfy it

**Status: recorded.** Reported undecidable, never absent. Not repaired.

Every one of §11.9's twelve entries has the same first shape — a planet in the
5th, and named planets in the 11th. Entry (12) is printed:

> "If Moon is in the 5th house and in the 11th house, one becomes very
> affluent."

One planet cannot hold two houses, and no second planet is named. As printed
the combination is unsatisfiable by any chart at all.

**What the other eleven imply.** The structure of the list is exact, and was
checked against all twelve lagnas rather than assumed:

| | holds across |
|---|---|
| the first combination places the **5th lord** in the 5th house | all 12 |
| the planets it wants in the 11th include the **11th lord** | all 11 that name any |
| the second combination places the **lagna lord** in lagna | all 12 |

For Pisces lagna the 11th is Capricorn, whose lord is **Saturn**. So the word
the sentence lost was almost certainly "Saturn".

**Not applied.** The inference is recorded in `DHANA_PISCES_LIKELY_MISSING` and
served on `/rules`, and the verdict names it — but the yoga stays undecidable
even on a chart that would satisfy the repaired rule, and a test asserts that.
Repairing a printed rule from a pattern is exactly the kind of quiet
substitution this project does not make.

Only the first half of entry (12) is defective; its second combination —
Jupiter in lagna reached by Mars and Mercury — is ordinary and is detected.

**Closes when:** you confirm the missing planet, or a later printing settles it.

## D-38 · Charts 6 and 11 are the same native at two different times

**Status: recorded.** Nothing in chapter 12 turns on it; anything degree-based
does.

P.V. Narasimha Rao's chart is printed twice, and the two printings disagree
about the time:

| | Chart 6 (§10.6) | Chart 11 (§12.3) |
|---|---|---|
| time | 12:49, 5h17m east | 1:08 pm (IST) |
| UT | 07:32 | 07:38 |

Six minutes apart. The seven planets and the nodes are unaffected — the largest
difference is the Moon's 3 arcminutes — so **every sign is the same and
Mercury's ashtakavarga is identical either way**, which is why Example 38 works
from either chart.

What does move:

| | Chart 6 | Chart 11 | difference |
|---|---|---|---|
| Ascendant | 24 Vi 19 | 25 Vi 45 | 1°26' |
| HL | 24 Cp 11 | 27 Cp 11 | 3°00' |
| GL | 25 Sg 59 | 3 Cp 29 | 7°30' — **a different sign** |

The ascendant moves about 1° in 4 minutes and GL five times as fast, so all
three are consistent with the six-minute gap rather than with a typo.

**Why it matters.** §11.7.3's yogas 6 and 8 read HL and GL, and GL changes sign
between the two printings — so a Raaja yoga verdict for this native depends on
which chart is used. Chapter 10's fixture uses Chart 6's time and reproduces
every body from it, so nothing changes today.

**What we do:** Chart 6 stays the fixture, since it is the one whose birth data
we recompute and verify against. Chart 11 is transcribed only for its BAV
figures, which are time-independent.

**Closes when:** you say which time is intended, or a later chapter uses one.

## D-39 · Charts 6 and 11 print different chara karakas for the same two planets

**Status: recorded.** Neither is followed over the other; the tie is reported.

Mercury is at **27 Ge 40** and Venus at **27 Ar 40** — the same degrees and the
same minutes, in different signs. §8.2 orders the chara karakas by advancement
within the sign, so this is an exact tie at the precision the book prints.

The two charts break it opposite ways:

| | Chart 6 | Chart 11 |
|---|---|---|
| Mercury | AmK | BK |
| Venus | BK | AmK |

§8.2's own tie-break is "If two planets have the same degrees, we should
compare minutes. If minutes are same, we should compare the seconds." The
printed data stops one level short of that: no seconds are given. PVR's own
software had them, so each chart is internally consistent — but the tie cannot
be resolved from the page.

**What we do:** the ordering uses a deterministic tie-break so a result is
never arbitrary between runs, and both grahas come back with
`shares_karakatwa: true`, which says the order between them is not settled by
the data. Chart 6's printed karakas remain the fixture, since that is the chart
we recompute.

**A defect this exposed.** The tie was not being detected at all. Two grahas at
the same degrees and minutes in *different* signs reach that advancement by
different arithmetic — `(60 + 27 + 40/60) % 30` against `(27 + 40/60)` — and
the two differ in the last bit of a float, by 3.6e-15 degrees. The equality
test missed it. Ties are compared with a tolerance now; 1e-9 degrees is 3.6
microarcseconds, far below anything the ephemeris resolves.

**Closes when:** you say which reading is intended, or seconds are supplied.

## D-40 · §12.4's SAV strength ranges overlap at 30

**Status: recorded.** Thirty is read as strong, on the section's own evidence.

> "A rasi with 30 or more rekhas becomes strong... A rasi with 25-30 rekhas is
> average. A rasi with less than 25 rekhas becomes weak."

Thirty falls in both "30 or more" and "25-30".

**Resolved from the section itself, not by preference.** The first clause is
unambiguous — "30 or more" names a bound and 30 meets it — and it is stated
first. The second is written as a loose range, the sort of phrasing that
usually means "the twenties". And the muhurta paragraph three sentences later
repeats the bound in the same direction: "Rasis containing **30 or more**
rekhas in SAV are favorable." A rasi cannot be favorable for a muhurta and
merely average at the same figure, so 30 is strong.

**What we do:** strong is 30 and above, average 25 to 29, weak below 25. The
overlap and this reasoning are served on `/v1/ashtakavarga/rules` as
`sav_overlap_note`, so the choice is visible to a caller rather than buried.

Chart 6 makes the boundary live: its Capricorn and Pisces both sit at exactly
30, and both are graded strong.

**Closes when:** you confirm, or a later passage settles it differently.

## D-41 · §12.7.2's rule (3) does not cover an empty rasi of equal value

**Status: NEEDS YOU.** A reading is implemented and flagged; it is not confirmed.

Rule (3) applies when one rasi of a co-owned pair is occupied and the other is
empty, and it splits two ways:

> "(3a) If the empty rasi has a **lower** value, replace the value with a zero.
> (3b) If the empty rasi has a **higher** value, replace the value with the
> value in the other rasi."

Equal is in neither branch, and equal values reach §12.7.2 routinely — Trikona
Sodhana zeroes and subtracts but does nothing to stop two co-owned signs
finishing level.

The two readings differ. Under (3a) the empty rasi becomes 0; under (3b) it is
replaced by a value it already holds, so nothing moves. A rekha is kept or lost.

**What we do:** read equal as (3a) and write zero. The book zeroes ties
everywhere else it meets one — rule (4a) here zeroes two empty rasis holding
the same value, and §12.7.1's rule (2) zeroes three trines holding the same
value. Reading equal as (3b) would make this the only place in either reduction
where a tie survives.

Every pair that hits the case is flagged in the result as
`tie_not_covered_by_the_book`, and `/v1/sodhana/ekaadhipatya` returns
`tie_hit_in_this_chart` listing them, so a caller can find the affected pairs
rather than be quietly handed an answer.

Neither Example 41 nor Example 42 reaches the case: 41 stops at rule (1) on all
five pairs, and none of 42's five hypotheticals has the empty rasi level with
the occupied one. So the book never demonstrates it.

**Closes when:** you confirm the reading, or a later passage settles it.

## D-42 · Table 28 gives Virgo 6; Exercise 22's own answers require 5

**Status: parked with Amit, 2026-08-30.** He is checking the classical
rasimana value against an outside source (BPHS, or a Jagannatha Hora run).
Until then the table is used **as printed** and nothing changes. Do not
re-raise this each turn.

Table 28's rasimana multipliers are `7 10 8 4 10 6 7 8 9 5 11 12`. Exercise 22
prints seven rasi pindas for Chart 7, and with Virgo at **6** every one of them
comes out too high by exactly the SoAV's Virgo rekhas:

| planet | ours (Virgo 6) | printed | excess | Virgo in SoAV |
|---|---|---|---|---|
| Sun | 155 | 152 | 3 | 3 |
| Moon | 86 | 85 | 1 | 1 |
| Mars | 55 | 52 | 3 | 3 |
| Mercury | 99 | 95 | 4 | 4 |
| Jupiter | 69 | 68 | 1 | 1 |
| Venus | 154 | 154 | 0 | 0 |
| Saturn | 166 | 162 | 4 | 4 |

With Virgo at **5**, all seven land exactly. That is seven independent
equations in one unknown fitting without residue, against one digit in one
table cell. Venus is the control: its SoAV holds zero in Virgo and it is the
one row that already agreed.

Nothing else in the chapter arbitrates. Example 43's SoAV also holds zero in
Virgo, so both multipliers give its printed 77 — a test asserts that, so the
example cannot be mistaken for corroboration of either value.

The rest of Exercise 22 is untouched by this: all 84 BAV figures, the SAV, all
84 SoAV figures and all seven **graha** pindas reproduce exactly. The
disagreement is confined to Table 28, which is what makes the single-cell
diagnosis safe.

**What we do:** `TABLE_28_RASIMANA` holds the printed 6, so
`/v1/sodhana/pinda` returns 155 for Chart 7's Sun where the book prints 152.
The conflict is served on that endpoint and on `/v1/sodhana/rules` as
`table_28_virgo_conflict`, so no caller meets the difference unwarned.

**Closes when:** Amit's outside check comes back. If the classical value is
5, the table is a misprint and we switch; if 6, Exercise 22's answers were
generated with a different multiplier and the disagreement is the book's to
own. Either way one line changes: `TABLE_28_RASIMANA`.

## D-43 · §12.7.2 says "occupied by a planet", but the lagna occupies too

**Status: resolved by Exercise 22, recorded for the record.**

§12.7.2's rules (2), (3) and (4) turn on whether a rasi is "occupied by a
planet (or planets)". Chart 7's Scorpio holds the **lagna and nothing else**,
and Scorpio is half of Mars's co-owned pair, so the Ar/Sc pair is decided by
whether the lagna counts.

Three of the seven printed SoAVs — Sun, Moon and Saturn — come out wrong if it
does not:

| planet | Ar/Sc before | lagna ignored | lagna counted | printed |
|---|---|---|---|---|
| Sun | (2, 1) | (2, 0) by rule (3a) | (2, 1) by rule (2) | (2, 1) |
| Moon | (3, 1) | (3, 0) by rule (3a) | (3, 1) by rule (2) | (3, 1) |
| Saturn | (2, 3) | (2, 2) by rule (3b) | (2, 3) by rule (2) | (2, 3) |

Two go through rule (3a) and one through (3b), so this is not one branch
misbehaving. The other four planets are unaffected and agree either way.

**What we do:** nothing changes in the code — `occupied_signs` is the caller's
to state, by OI-104 — but the finding is served as `lagna_occupies` so a caller
knows which set to pass. Our own fixtures pass the lagna's rasi.

This settles only the lagna. Rahu and Ketu remain open under OI-104: Chart 7
puts them in Aries and Libra, both of which already hold planets, so the
exercise cannot distinguish them.

## D-44 · §12.8's whole-sign example says "the 2nd house is in Li"; it is Vi

**Status: resolved from the sentence itself.** A transcription slip, not a rule.

§12.8 states the book's position on house division:

> "Even if Saturn is at 1° in Vi and lagna is at 29° in Le, we still say that
> the 1st house is in Le, the 2nd house is in **Li** and Saturn is in the 2nd
> house (though he is only 2° away from lagna)."

The 2nd from Leo is **Virgo**, not Libra. And the same sentence puts its Saturn
at 1° Virgo and says he is in the 2nd house. The two halves cannot both hold
with Li; read as Vi, they agree exactly and the sentence states the whole-sign
rule the paragraph is arguing for.

The paragraph above it agrees independently: a Saturn at 3° Vi with lagna at
27° Le is 2nd-house by PVR and 1st-house by the people he is arguing against.
Both readings put the boundary at the Le/Vi line, so nobody in the dispute
thinks Libra is involved.

**What we do:** the rule, not the typo. Every house in the chapter is counted
whole-sign from its reference. `whole_sign_stand_typo` on
`/v1/ashtakavarga/rules` carries the printed sentence and this reading, so the
slip is visible rather than silently corrected.

**Nothing needs deciding.** The correction is forced by the sentence itself.

## D-45 · §13.2's 1st house is a trine for nature and neither for yogakaraka

**Status: resolved from Table 30, which forces both readings.**

The 1st is a quadrant *and* a trine, and §13.2's rules treat those differently.
Table 30 settles which applies, twice, in opposite directions.

**For a planet's own nature, the 1st is a trine.** Cancer's Moon owns only the
1st and Table 30 lists him a functional benefic. Read as a quadrant he would be
phase-dependent — waxing benefic, waning malefic — and would have been left out
like Aries, Libra and Capricorn, whose Moons own the 4th, 10th and 7th.

**For the yogakaraka rule, the 1st is neither.** Table 30 names six
yogakarakas. Letting the 1st serve as the trine would name ten, adding
Gemini's and Virgo's Mercury and Sagittarius's and Pisces's Jupiter — each of
which owns the lagna and one other quadrant. So the quadrant must be the 4th,
7th or 10th and the trine the 5th or 9th.

Related: §13.2 says "Moon is not listed for movable rasis", but Cancer is
movable and its Moon *is* listed. The condition that actually holds is owning a
quadrant **other than the 1st**, which for Cancer's Moon is true of Aries,
Libra and Capricorn exactly. The wording is loose; the table is not, and Cancer
being the exception is what proves the first reading above.

**What we do:** both readings, each pinned by the test that forces it.
`/v1/functional/rules` carries `yogakaraka_rule` and `moon_movable_wording`.

**Nothing needs deciding.** Table 30 determines both.

## D-46 · Taurus's Sun: the rule says neutral, Table 30 says benefic

**Status: NEEDS YOU — but low stakes; the table is used.**

§13.2's rule: "The lord of a quadrant is a functional malefic if he is a
natural benefic and **functionally neutral if he is a natural malefic**."

Sun owns only Leo, which is the 4th from Taurus — one house, a quadrant, and
the Sun is a natural malefic. The rule gives **functionally neutral**. Table 30
lists him among Taurus's **functional benefics**.

No combining is involved, so this is not the "judiciously combine" licence
§13.2 grants for two-rasi owners. It is the only one of the nine
rule-versus-table divergences that is not a two-rasi owner.

The rule holds everywhere else it can be tested. Sun is the only planet besides
the Moon that owns a single rasi, and the Moon is omitted wherever he owns a
quadrant, so Taurus, Scorpio and Aquarius are the only three trials:

| lagna | Sun's house | rule | Table 30 |
|---|---|---|---|
| Taurus | 4th | neutral | **benefic** |
| Scorpio | 10th | neutral | neutral |
| Aquarius | 7th | neutral | neutral |

Two of three follow the rule, so this is one cell rather than a pattern — but
with only three trials that is weak evidence either way.

**What we do:** Table 30 is served, so callers get *benefic* for Taurus's Sun.
The divergence is listed on `/v1/functional/rules`.

**Closes when:** a worked example in a later chapter reads Taurus's Sun, or you
decide the rule should override the table.

## D-47 · §15.5.1's rule (2) illustration never reaches rule (2)

**Status: BOOK DEFECT — no decision needed; the counting is still verifiable.**

§15.5.1 states the cascade plainly: "We go from one rule to the next, only if
we do not have a winner." Rules (3), (4), (5a) and (5b) each preface their
example with "suppose we have a tie after step (N)". Rule (2)'s does not:

> "Suppose Saturn is in Ge with Mercury, Rahu is in Ar, Mars is in Le, Jupiter
> is in Ta."

Saturn has a co-tenant and Rahu has none, so rule (1) already declares Saturn
and the cascade stops before rule (2) is consulted. The example reaches the
right planet by the wrong rule.

**What we do:** `charts/colord.stronger` runs the cascade as written, so it
decides this placement at rule (1). The rule-2 counts the section quotes — 2
for Saturn, 1 for Rahu — are checked directly against `rule_2_count`, and a
separate fixture gives Rahu a co-tenant so rule (2) genuinely decides.

**Closes when:** nothing. The section's own cascade is unambiguous; only its
illustration is loose.

## D-48 · Exercises 25 and 26 name Chart 12 but describe a different chart

**Status: BOOK DEFECT — the chart reference is wrong, not the reasoning.**

Revised after Exercise 26. The first reading of this entry blamed scattered
premise errors in Exercise 25. Exercise 26 makes the cause plain: both
exercises reason about one internally consistent chart, and it is not Chart 12.

Chart 12 is Madonna's — 16 August 1958, 7:05 am (4:00 West), 83 W 53, 43 N 36 —
identified by the book's own Exercise 21, whose printed answer we reproduce. It
recomputes from that birth line with every graha inside an arcminute. It holds:

| | Ar | Ta | Ge | Cn | Le | Vi | Li | Sc | Sg | Cp | Aq | Pi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chart 12 | 2 | 0 | 0 | 2 | 2 | 0 | 2 | 1 | 0 | 0 | 0 | 0 |
| Exercise 26 says | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 2 | 1 | 0 | 1 |

Twelve occupancy claims. Every one that asserts an occupied rasi fails; the
three that hold — Ge, Vi and Aq — hold only because both charts leave those
empty, a coincidence of zeros. Exercise 25 adds four more failures: Rahu alone,
Saturn's dispositor being Jupiter, Saturn in a dual rasi, and Mars in Scorpio.

**The chart both exercises do describe** is fully determined by their own
statements, and no chart in the register matches it:

| rasi | grahas |
|---|---|
| Aries | Ketu |
| Taurus | Venus |
| Libra | Rahu |
| Scorpio | Mars, Jupiter |
| Sagittarius | Sun, Mercury |
| Capricorn | Moon |
| Pisces | Saturn |

It satisfies all twelve of Exercise 26's occupancy claims, all four of its
rule-2 readings — "Ar is aspected by Jupiter & lord Mars", "Li is aspected only
by lord Venus", "Le is not aspected by any of Jupiter, Mercury and lord Sun",
"Aq is aspected by co-lord Rahu" — and every premise of Exercise 25, including
Saturn alone in a dual rasi ruled by Jupiter, which fixes him in Pisces rather
than Sagittarius.

**On that chart `charts/rasi_strength.stronger` returns all six of the book's
answers, each by the book's own deciding rule.** The engine is not in question;
only which chart the exercises meant.

**On Chart 12 as printed** we answer Li, Sc, Ge, Cn, Le, Vi — one of six
agreeing with the book, and that one by coincidence of occupancy. For Exercise
25 we answer Rahu for Aquarius where the book answers Saturn, and Ketu for
Scorpio by rule (2) where the book uses the basic rule.

**What we do:** the engine runs against whatever chart it is given. Both
answers are fixtured — the reconstruction to show the engine reproduces the
book, and Chart 12 to record what the printed exercise actually asks for.

**Closes when:** the chart number is corrected in a later printing, or the
chart the exercises describe turns up numbered elsewhere in the book.

## D-49 · §15.5.2's rule (2) illustration contradicts its own cascade

**Status: BOOK DEFECT — sibling of D-47, and worse.**

§15.5.2 opens with the same instruction as §15.5.1: "We go from one rule to the
next only if there is no winner after the rule. When we have a winner, we stop
and do not go to the next rule." Rules (3), (4), (5) and (6) each preface their
example with "suppose we have a tie after rule (N)". Rule (2)'s does not:

> "Suppose Jupiter is in Ar, Mercury and Venus are in Ta and Mars is in Vi."

Aries holds Jupiter and Libra holds nothing, so rule (1) — "if one rasi
contains more planets than the other rasi, then it is stronger" — declares
**Aries** and the cascade stops. The section then computes rule (2) and
concludes **Libra**.

D-47 is the same omission in §15.5.1, but there rule (1) and rule (2) happened
to name the same planet, so only the route was wrong. Here they disagree, so
following the section's own cascade gives the opposite of the section's answer.

The rule-2 counts themselves are sound: Aries 1 (Jupiter occupies), Libra 2
(Mercury and lord Venus aspect from Taurus, Jupiter does not). Only the worked
placement is unusable as a cascade illustration.

**What we do:** `charts/rasi_strength.stronger` runs the cascade as written and
returns Aries for these placements. The counts are checked directly against
`rule_2_count`, and a separate fixture puts one planet in each rasi so rule (1)
ties and rule (2) genuinely decides — which then does give Libra.

**Closes when:** nothing. The cascade is unambiguous; two of its illustrations
are not.

## D-50 · Example 50's end date is one day early

**Status: BOOK DEFECT — one day, in the chapter's only worked example.**

Every figure in Example 50 reproduces exactly: Moon's advancement in Dhanishtha
9°3', the unspent fraction 257/800 = 0.32125, Mars as the lord, and a balance
of 7 × 0.32125 = 2.24875 years, which the example itself breaks down as 2 years
2 months 29 days 33 ghatis. In savana units — year 360 days, month 30, ghati
1/60 of a day — that is 720 + 60 + 29 + 0.55 = **809.55 days**.

Added to the stated birth of 5:50 am on 2000 April 28, that gives **2002 July
16, 19:02**. The example says "about 7 pm on 2002 July 15".

The time of day matches to two minutes, so the arithmetic path is the same and
only the day count differs. Adding 808.55 days — one less — lands on 2002 July
15 at 19:02, which is the example's answer exactly. The balance is the part of
Mars dasa still to run at birth, so it is measured forward from birth and 809.55
is the right count; the printed date is one day short.

Sidereal years are not the explanation. At 365.2564 days the same balance gives
2002 July 28, thirteen days out, which is what makes this example decisive
evidence for savana under OI-115 rather than a reason to doubt it.

**What we do:** the engine adds the balance forward from birth and returns July
16. Every intermediate the example prints is fixtured and matches; the end date
is fixtured as the divergence it is.

**Closes when:** a later printing corrects the date, or a second worked example
shows the inclusive count is deliberate.

## D-51 · Example 55 calls Venus the lagna lord, then calls Ketu the lagna lord

**Status: BOOK DEFECT — the example contradicts itself, and Ketu is right.**

Chart 20's lagna is Scorpio, owned by Mars with Ketu as co-lord. Example 55
says of Venus:

> "Venus is lagna lord and he gives Vesi yoga being in the 2nd from Sun."

Venus owns Taurus and Libra. He is **in** Scorpio, at 1 Sc 05 against a lagna
of 18 Sc 09 — in the lagna, not its lord. Three paragraphs later the same
example says "Ketu is lagna lord in the 8th house", which is correct.

Everything else in that sentence holds: Venus is in the 2nd from Sun and does
give Vesi yoga, and the next clause — "being the 8th lord from AL" — is right
too, since AL is in Pisces and the 8th from it is Venus's Libra. Only the
lordship is wrong, and being in the lagna is itself favourable, so the
conclusion "his dasa is good" survives its own reason.

**What we do:** nothing to fix — no calculation reads this. Chart 20's record
and the Example 55 fixtures assert Scorpio's lords are Mars and Ketu, and that
Venus occupies the lagna rather than ruling it, so the slip cannot be copied
into our data later.

**Closes when:** a later printing corrects it.

## D-52 · "Exalted" at sign level or degree level, and it changes dasa lengths

**Status: NEEDS YOU — no longer cosmetic.**

Two grahas have their moolatrikona inside their own exaltation sign, so for
those two the word "exalted" means different things at sign and degree level:

| graha | exalts at | `sign_dignity` says instead | band |
|---|---|---|---|
| Moon | 3° Taurus | moolatrikona | Taurus 3°–30° |
| Mercury | 15° Virgo | moolatrikona, then **own** | Virgo 15°–20°, 20°–30° |

`sign_dignity` reports the finer of the two, so a Moon at 23 Ta 38 comes back
**moolatrikona** and a Mercury at 23 Vi 19 comes back **own**, where the book
calls both **exalted**.

First seen in Example 55, where it only changed a word. §18.2.2 adds a year to
a dasa whose lord is exalted, and two examples now turn on it:

| example | graha | book | ours | cost |
|---|---|---|---|---|
| 66, Chart 23 | Moon 23 Ta 38 | Cn **3 years** | 2 | five later dasas shift a year; every date from 1946 on |
| 68, Chart 24 | Mercury 23 Vi 19 | Ge **4 years** | 3 | every date in the example from 1959 on |
| 74, Chart 31 | Moon at 6.67° of Taurus **in D-10** | Cn **3 years** | 2 | Cancer is the *first* dasa, so all six printed dates move |

Example 68 is the stronger of the two and is close to decisive. It calls
Mercury exalted three times in prose — including in the line that picks the
dasa seed, "as its exalted lord aspects it" — and its Ge dasa of 4 years is
arithmetically 4 − 1 + 1, which needs exception 2 to have fired. By degree that
Mercury is not even moolatrikona; he is plainly in his own sign, so this is not
a borderline reading of a boundary.

Example 74 is the third, and the most expensive: its Cancer dasa is the first
of the sequence, so the missing year moves every date the example prints. It is
also the first in a **varga** — Example 71 showed dignity there is read in the
varga, and the Moon's D-10 Taurus is past his 3-degree exaltation just as his
rasi-chart Taurus was in Example 66.

Nothing yet points the other way: no example has needed exaltation read by
degree.

**What we do:** nothing yet. `dasa_length` takes the dignity from the caller,
so both readings are reachable. The Example 66 and 68 fixtures assert both and
name which is which.

**Closes when:** you decide whether §18.2.2's "exalted" means the exaltation
sign or the exaltation degrees. It affects only these two grahas — and, if you
want the change made globally rather than in `dasa_length`'s callers, say so,
because `sign_dignity` is used well beyond this chapter.

## D-53 · Example 56's Rudra needs the ordinary 8th, which §14.3 forbids

**Status: NEEDS YOU — this one changes a calculation.**

§14.3 is explicit about which 8th house Rudra uses:

> "Find the 8th house using Table 32 and not in the normal way."

Table 32 differs from the ordinary 8th in eight of the twelve rasis, Leo among
them. Chart 21 has a Leo lagna, and Example 56 says "He joins Jupiter, who is
Rudra". Jupiter cannot be a candidate under Table 32:

| | 8th from lagna Leo | 8th from the 7th, Aquarius | candidates |
|---|---|---|---|
| Table 32 | Cancer | Capricorn | Moon, Saturn |
| ordinary | **Pisces** | Virgo | **Jupiter**, Mercury |

Under Table 32 our §14.3 cascade returns **Saturn**, decided at rule 1 — Saturn
has two co-tenants against the Moon's one. Under the ordinary 8th the same
cascade returns **Jupiter**, also at rule 1, because Jupiter shares Sagittarius
with Venus and Saturn while Mercury sits alone in Libra. So the cascade is not
in question; only which 8th feeds it.

Chapter 14 printed no Rudra, so Table 32 was transcribed and used on the
section's own instruction but never checked against an answer. Example 56 is
the first printed Rudra in the book, and it wants the ordinary 8th.

There is precedent for the ordinary 8th winning: §14.5's eighth lord method
raised the same question and Exercise 23 settled it that way, which is recorded
in `EIGHTH_LORD_USES_THE_ORDINARY_EIGHTH`. That makes two of the chapter's
three 8th-house rules resolving against the special table.

**What we do:** nothing yet. `rudra()` still follows §14.3 and returns Saturn.
The Example 56 fixture asserts both readings and states which the book's answer
requires, so the divergence is visible rather than buried.

**Closes when:** you decide whether Rudra should follow §14.3's instruction or
its own worked example, or a second printed Rudra breaks the tie.

## D-54 · Example 62 calls Mercury Uttamaamsa; our dasavarga count says Paarijaataamsa

**Status: one step apart, cause not established.**

Example 62 lists "Mercury is in Uttamamsa" among its reasons for calling him a
great yoga karaka in Chart 6. On the dasavarga scale Uttamaamsa is a count of
three; Paarijaataamsa is two. We compute **two**, from Mercury being in his own
Gemini in D1 and again in D9:

| chart | rasi | dignity |
|---|---|---|
| D1 | Gemini | own |
| D9 | Gemini | own |

To reach three, one more of the ten vargas would have to give Mercury a
dignity that counts. Which one, and under whose definition of "counts", the
example does not say — it states the amsa and moves on.

Everything else in that paragraph reproduces exactly, including the two
ashtakavarga figures that are easy to get wrong: Mercury's BAV in Gemini is 7
rekhas and Gemini's SAV is 34, both as printed. So this is one figure out of
several, not a broken reading.

Unrelated to OI-91, which asks what to do when the *two planets* of a pair have
different counts. This is a single planet's count differing from the book's.

**What we do:** nothing. `amsabala` reports the count and the charts that
produced it, so a reader can see exactly which two vargas we found and judge
the third for themselves.

**Closes when:** a chapter defines which dignities count towards the dasavarga
tally, or another example pins a count we can check the rule against.

## D-55 · Example 67's Ketu antardasa sequence prints eleven of twelve rasis

**Status: BOOK DEFECT — a dropped sign, not a rule.**

§18.3 opens by saying "Each dasa is divided into 12 antardasas", and Example
67's normal sequence duly lists twelve:

> Ta, Ar, Pi, Aq, Cp, Sg, Sc, Li, Vi, Le, Cn and Ge

Its Ketu variant lists eleven:

> Ta, Ge, Cn, Le, Vi, Li, Sc, Sg, Cp, Aq and Pi

Counting forward from Taurus, which is what the Ketu exception makes it do, the
twelfth is **Aries**. Our sequence agrees with all eleven that are printed and
supplies Aries at the end.

Nothing turns on it: the rule is unambiguous, the other sequence in the same
example is complete, and no antardasa can be dropped without the twelve failing
to fill the dasa. It is a printing slip.

**What we do:** return twelve. The Example 67 fixture asserts the eleven
printed match in order and that the missing one is Aries, so the divergence is
recorded rather than smoothed over.

**Closes when:** a later printing restores the sign.

## D-56 · §18.5's interpretation warning is printed with two slips

**Status: closed.** Transcribed as printed; nothing to compute.

> "So taking dasa rasi or the 7th from it as lagna and analyzing dasas **is
> has** no technical basis. **It applies only the rasi chart.**"

The first reads as a slip for "dasas has"; the second wants "only **to** the
rasi chart". Neither puts the meaning in doubt, and the sentence is load-bearing
— it is the reason `dasa_lagna` refuses a varga — so it is stored word for word
in `VARGA_INTERPRETATION_WARNING` and pinned by a test that names both slips.

Same treatment as D-24 and D-25: tidying a quotation is how a register stops
being one.

## D-57 · Example 71 prints its antardasa sequence with the first two swapped

**Status: closed.** The same paragraph contradicts it twice, so the reading is
not in doubt.

> "So antardasas start from Vi. Because Vi is an even sign, they go in the
> backward direction. Antardasas of 11 months go as **Le, Vi, Cn, Ge** etc."

Backward from Vi is **Vi, Le, Cn, Ge**. The paragraph has just said the
antardasas start from Vi, and the next one dates Vi antardasa from 4 April
1991 — the day Le dasa itself begins, so Vi runs first. Cn and Ge are right,
which is what makes it a transposition of the pair rather than a different
rule.

**What we do:** return Vi first. The Example 71 fixture asserts our order and
asserts it is not the printed one, so the divergence is visible.

Same shape as D-55, where Example 67 printed eleven of twelve rasis.

## D-58 · Example 71's pratyantardasa dates do not divide its own antardasa

**Status: closed.** Arithmetic, and it changes nothing the example concludes.

> "Vi antardasa is of 11 months and it runs from 4th April 1991 to 4th March
> 1992. Dividing it into 12 equal parts, we see that the 5th pratyantardasa
> runs from 27th July 1991 to 25th August 1991."

That span is 335 days, so a twelfth is 27.92 days and the 5th part runs
**24 July to 21 August 1991**. The printed part is 29 days long and begins
three days late; twelve of it would end the antardasa on 11 March 1992, not
the 4th the same sentence gives.

**What we do:** divide the antardasa as stated. The conclusion is unaffected —
the native landed on 15 August 1991, which falls in the 5th pratyantardasa on
either reading, and the 5th from Ar forward is Le either way. The fixture pins
both sets of dates and the landing inside both.

## D-59 · Example 72 does not add a year for an exalted **node**

**Status: NEEDS YOU — it changes a dasa length.** Sibling of D-52: both ask
what §18.2.2's exception 2 means by "exalted".

Chart 28's Aquarius dasa, in the navamsa. §15.5.1 gives Rahu as the stronger
co-lord, and Rahu is in Gemini in D-9 — which by **§3.3's own Table 6** is his
exaltation, the value D-4 records us as following on your approval.

| | count | base | exception 2 | length |
|---|---|---|---|---|
| ours, Table 6 applied | 9 | 8 | +1 | **9** |
| the book prints | 9 | 8 | not applied | **8** |

Saturn does not rescue it: he is in Aries in D-9, eleven houses on, giving 10
and then 9 for his debilitation. Only "Rahu, not exalted" gives 8, so this is
not a co-lord question.

Two readings fit. Either exception 2 does not reach the nodes at all — D-4
already notes Table 6 gives them an exaltation *rasi* but no deep-exaltation
degree, so they have no exaltation in the sense the other seven do — or the
example simply did not apply Table 6 here.

**What we do:** nothing. `dasa_length` takes the dignity from its caller, so
both are reachable, and the Example 72 fixture asserts both and names which is
which. One example is thin evidence either way, and no other chart in the
chapter puts a node in its Table 6 exaltation or debilitation as a dasa rasi's
lord, so nothing else in the book so far can corroborate it.

**Closes when:** a second example puts a node there, or you decide.

## D-60 · Exercise 29's answer gives the 9th antardasa 8 months, not 10

**Status: closed.** The same sentence contradicts it, and nothing turns on it.

> "Each antardasa lasts 10 months. It takes 80 months (or 6 years and 8
> months) for 8 antardasas to finish. So the 9th antardasa starts in February
> 2000 and **runs for 8 months**."

Ten. The clause two before it says so, and 8 x 10 = 80 is what puts the ninth
at February 2000 in the first place. The "8 months" reads as a stray from the
"6 years and 8 months" just ahead of it.

**What we do:** ten months, February to December 2000. Early June 2000 falls
inside on either reading, so the exercise's answer is unaffected. The fixture
asserts the event lands inside both spans.

Same shape as D-58, where Example 71's pratyantardasa dates did not divide the
antardasa they were cut from.
