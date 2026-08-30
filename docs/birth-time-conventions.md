# Birth times on Indian charts

Indian birth records and hand-cast kundalis often carry **two** times. Reading
them wrong shifts the ascendant by about nine degrees without moving it out of
its rasi, so the error is silent. This note fixes how to read them.

## The three times

| Name | Offset | What it is |
|---|---|---|
| **IST** | UTC+5:30 | Since 1906. What a hospital clock shows. |
| **Bombay Time** | UTC+4:51 | A legal standard for Bombay until IST replaced it. Defined as Bombay's approximate local mean time. |
| **Local Mean Time** | longitude ÷ 15 | The place's own solar time. Ghatkopar's is UTC+4:51.7. |

Madras Time (UTC+5:21) and Calcutta Time (UTC+5:53) were the other two.

## The rule

**Feed the engine the clock time with its own offset.** `compute_chart` takes
the longitude and does the sidereal-time correction itself. Feeding it a time
that has *already* been converted to local mean time double-counts the
longitude.

A hand-caster converting IST to LMT before drawing the chart is doing by hand
what the engine does internally. Their intermediate value is not an input.

## The worked case that prompted this

A Ghatkopar birth, 7 May 1978. Hospital clock **12:55**; the kundali also
carried **12:16** marked "st. time".

    12:55 IST (UTC+5:30)              ->  Asc 28 Cn 04.9'
    12:16 Bombay Time (UTC+4:51)      ->  Asc 28 Cn 04.9'   identical
    12:16 read as if it were IST      ->  Asc 19 Cn 13.2'   wrong by 8.9 deg

12:55 IST is 07:25 UTC, which is 12:16 in Bombay Time exactly. So "st. time"
was **Standard Time** — the older Bombay standard, not IST — and the two
entries are one instant. Either can be used if given its own offset. Only the
third line is wrong, and it stays inside Cancer, which is what makes it
dangerous.

## The check

If a supplied kundali's ascendant matches our chart, the caster handled the
conversion. If it sits about nine degrees earlier, they double-counted. That
difference is a usable diagnostic on any Indian chart with two times on it.
