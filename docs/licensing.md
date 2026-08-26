# Licensing — read before this goes public

Two dependencies in this space are AGPL-3.0, and AGPL is triggered by *network
use*, not just distribution. For an API product that is the whole ballgame.

## 1. Swiss Ephemeris — the blocking decision

Swiss Ephemeris (and therefore `pyswisseph`) is dual-licensed. From its own
LICENSE file:

> Swiss Ephemeris is made available by its authors under a dual licensing
> system … a) GNU Affero General Public License (AGPL) b) Swiss Ephemeris
> Professional License
>
> The choice must be made … **before any public service using the developed
> software is activated.**

So there are exactly three options:

| Option | Consequence |
|---|---|
| **Buy the Swiss Ephemeris Professional License** from Astrodienst | Keeps this codebase proprietary. One-time fee, signed contract. This is what every commercial Vedic astrology product does. |
| **Accept AGPL-3.0** | The entire API service must be published under AGPL, including anything that links to it in-process. |
| **Swap the ephemeris backend** | Use JPL DE440 via `skyfield` (MIT) or `jplephem` (MIT), and compute ayanamsa, houses and rise/set independently. No licence fee, but real work and a parity risk. |

The code is already structured for option 3 as an escape hatch:
`hora.core.ephemeris.base.EphemerisProvider` is the only surface the astrology
layer touches, and `SwissEphemeris` is one implementation of it. Nothing above
that layer imports `swisseph`.

**Recommendation:** buy the Professional License. JHora is built on Swiss
Ephemeris, so matching the benchmark exactly is dramatically easier with the
same ephemeris underneath, and the fee is small next to the engineering cost of
reimplementing sidereal positions to arcsecond parity.

## 2. PyJHora — do not vendor it

[PyJHora](https://github.com/naturalstupid/PyJHora) is an existing Python port
of JHora 8.0 by Sundar Sundaresan, and it is **AGPL-3.0**. Importing it, or
copying code from it, would put this service under AGPL.

It is still useful as a *private* cross-check oracle: running it locally to
generate comparison values is not distribution and does not trigger the
licence. Keep that in a separate, never-shipped tooling environment — not in
`pyproject.toml`.

## 3. Jagannatha Hora itself — source, and whether to reverse engineer

### Is the source available?

**No.** Searched 2026-08-25: there is no source release, no public repository,
and no source distribution on vedicastrologer.org, on the Internet Archive
mirror, or anywhere else found. Only community re-implementations exist —
[PyJHora](https://github.com/naturalstupid/PyJHora) (AGPL) and
[ndastro](https://github.com/jaganathanb/ndastro) — and neither is derived from
JHora's code. Both were written from the book and from black-box comparison,
which is what we are doing.

### What language is it written in?

**Unconfirmed.** Nothing published states it. It is a Win32 desktop application
supporting Windows 95 through 7, and the author is a software engineer, which
points to native C or C++ — but that is inference, not fact, and nothing should
be built on it.

### The licence

The distribution states:

> "This is a FREE SOFTWARE, others are allowed to redistribute it, provided they
> retain all the original copyright Notices and **do not make any profits from
> it**."

Two things follow:

- It is **freeware, not open source**. Free to use and to pass along; the source
  is not given and no right to modify is granted.
- It is **non-commercial**. We are not redistributing JHora, so this does not
  bind our product — but it states the author's intent plainly, and that matters
  for how we treat his work generally (see [OI-12](open-items.md#oi-12) on his
  book text).

### Should we reverse engineer it?

**No — and we do not need to.**

| Approach | Legality | Usefulness |
|---|---|---|
| **Black-box oracle** — run JHora, record outputs, diff | Clean. Observing published behaviour is not reverse engineering. | **High.** It is the benchmark, and it settles every open question we have. |
| **Decompilation** | Grey and jurisdiction-dependent. Narrow interoperability exceptions exist (EU Software Directive Art. 6, US DMCA §1201(f)) but they are narrow. The licence grants no modification right. | **Low.** |

Three reasons decompilation loses on the merits, before the legal question is
even reached:

1. **The algorithms are already published.** PVR wrote them down in the book and
   in his articles. That is the channel he intended, it is readable, and it is
   what we are already implementing successfully.
2. **Decompiled output is worse evidence than the book.** A machine translation
   of optimised native code, with symbols stripped, is harder to verify than a
   sentence stating the rule. It would slow the work down, not speed it up.
3. **Provenance.** For a commercial product, code derived from a decompiled
   binary is tainted. Clean-room separation matters if this is ever licensed,
   sold, or subjected to diligence. Everything we have written derives from the
   book, from classical texts, and from our own work — that is worth keeping
   true.

### A better move than reverse engineering

**Ask him.** PVR shares his work freely and answers correspondence. Two things
worth asking for:

- Permission to redistribute the §2.3 indications, which would close
  [OI-12](open-items.md#oi-12).
- Clarification on the places where the book contradicts itself — the four
  registered in [precedence.md](precedence.md) — and on his current values where
  JHora has moved on from the 2000 book.

That is faster, cleaner and more accurate than any amount of decompilation.

## 4. Jagannatha Hora — usage terms

JHora is free closed-source Windows freeware by P.V.R. Narasimha Rao. This
project treats it strictly as a **black-box oracle**: run a chart in JHora,
transcribe the output into a fixture, diff. No decompilation, no binary
inspection, no extraction of its data files.

That is also the more effective route. The calculations are not JHora's
invention — they come from Brihat Parashara Hora Shastra, Jaimini Sutras, and
Narasimha Rao's own published book *Vedic Astrology: An Integrated Approach*.
Implementing from those sources and validating against JHora's output gets a
correct, independently-owned engine; decompiling gets a legal problem and a
worse codebase.
