"""Part 4's opening — what the Tajaka system is, and why it is in this book.

Every other part of the book rests on Parasara or Jaimini. This one opens by
saying plainly that it does not: "There are no references to it in the works of
Parasara, Jaimini and other maharshis." The part is included on the strength of
**precedent** — Neelakantha's `Tajaka Neelakanthi` and Dr B.V. Raman both
taught it — and the author says so in the same breath as conceding that
scholars "may validly question" its presence. Nothing else in the book is
defended that way, and `docs/precedence.md` has to account for it.

The part is also the one three earlier passages said they needed: footnote 68
credits Tajaka annual and monthly charts with the one-to-two-week predictions,
footnote 74 requires a Tajaka chart before a death reading may be made, and
Example 54's Rajya saham is deferred here (OI-116).

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

#: The part's own name for the system, and the claim it makes for it.
TAJAKA_IS_USEFUL_FOR_PRECISE_PREDICTIONS = (
    "A sub-system of Indian astrology, popularly known as \"Tajaka system\", "
    "is extremely useful in making precise and pointed predictions. It "
    "considers planetary aspects and yogas different from those employed in "
    "other classical methods of Vedic astrology and it is closer to western "
    "astrology in terms of aspects and yogas."
)

#: The provenance paragraph, verbatim. The book's own case for including it.
TAJAKA_PROVENANCE = (
    "In fact, some scholars may validly question why Tajaka system is being "
    "covered in a book on Vedic astrology. There are no references to it in "
    "the works of Parasara, Jaimini and other maharshis. The oldest reference "
    "to these techniques to be found in the works of a respected authority on "
    "Vedic astrology is in \"Tajaka Neelakanthi\", a work by Neelakantha who "
    "wrote a celebrated commentary on \"Jaimini Sutras\". His coverage of "
    "Tajaka system lends some authenticity to the system. One can only "
    "speculate whether Parasara talked about this system in parts that are "
    "possibly missing today. We will cover this system in this book, because "
    "some illustrious scholars of Vedic astrology, like Neelakantha and Dr. "
    "B.V. Raman, set the precedent by teaching this system."
)

#: The authorities the part names, and what each contributes.
TAJAKA_AUTHORITIES: tuple[dict[str, str], ...] = (
    {"who": "Parasara", "gives": "nothing — no reference to the system"},
    {"who": "Jaimini", "gives": "nothing — no reference to the system"},
    {"who": "other maharshis", "gives": "nothing — no reference to the system"},
    {"who": "Neelakantha",
     "gives": "Tajaka Neelakanthi, the oldest reference in a respected "
              "authority; he also wrote a celebrated commentary on Jaimini "
              "Sutras"},
    {"who": "Dr. B.V. Raman", "gives": "the precedent of teaching it"},
)

#: **Finding.** This is the only technique in the book admitted on **precedent**
#: rather than on authority. Everywhere else a rule is traced to Parasara,
#: Jaimini or a named classic; here the book states there is no such source,
#: offers a commentator and a modern teacher instead, and says outright that
#: the objection would be valid. `docs/precedence.md` ranks BPHS above other
#: classical works and both above modern writers — a ladder Tajaka is not on
#: at all by the book's own account.
TAJAKA_IS_ADMITTED_ON_PRECEDENT_NOT_AUTHORITY = (
    "The part concedes that Parasara, Jaimini and the other maharshis do not "
    "mention the system, and includes it because Neelakantha and Dr B.V. "
    "Raman taught it. No other part of the book argues for a technique this "
    "way."
)

#: **Finding.** The author marks his own speculation as speculation, in
#: italics: "One can only *speculate* whether Parasara talked about this
#: system in parts that are possibly missing today." That is a claim about the
#: transmission of a text, and he refuses to make it. Recorded because it is
#: the standard the rest of the book is read against.
THE_MISSING_PARASARA_IS_MARKED_AS_SPECULATION = (
    "The book italicises \"speculate\" when it raises the possibility that "
    "Parasara covered Tajaka in a lost portion. It is offered as a "
    "speculation and not as a provenance."
)

#: How a Tajaka year begins, and the chart cast for it.
SOLAR_RETURN_RULE = (
    "This system is based on solar return charts. When Sun returns every year "
    "to the position he occupied in the zodiac at the time of a person's "
    "birth, a new year is said to commence for the person and a chart drawn "
    "for that time is called \"Tajaka annual chart\" or \"Tajaka varsha "
    "chakra\"."
)

#: The two names the part gives the annual chart.
ANNUAL_CHART_NAMES: tuple[str, ...] = ("Tajaka annual chart",
                                       "Tajaka varsha chakra")

#: What the annual chart is for, and the gate the natal chart puts on it.
ANNUAL_CHART_SCOPE = (
    "Analysis of this chart can give insights into what may be in store "
    "during the one year following the solar return. Results suggested in the "
    "annual chart can take place only if they are 'possible' based on natal "
    "chart also. However, annual chart often gives a finer insight into the "
    "year in question than natal chart."
)

#: **Finding.** The natal chart is a **gate** and the annual chart a
#: **refinement** — the same coarse-and-fine shape §25.4 gave the two
#: divisional interactions and §26.9 demanded without naming a method. Here it
#: is named: the annual chart is cast for the native's own solar return
#: instant, so unlike every technique in chapters 25 and 26 it is personal in
#: its **timing** as well as in its valuation. That is precisely the
#: chart-sensitive companion §26.9 asked for and left unspecified.
THE_ANNUAL_CHART_IS_THE_CHART_SENSITIVE_METHOD_26_9_ASKED_FOR = (
    "Section 26.9 says the nakshatra techniques must be used with "
    "chart-sensitive methods and names none. A solar return is cast for one "
    "person's own moment, so both its timing and its reading belong to that "
    "nativity, which no technique in chapters 25 or 26 can say."
)

#: **Finding.** The gate runs one way only. The natal chart can veto a result
#: the annual chart suggests — "can take place only if they are 'possible'" —
#: but nothing here lets the annual chart veto the natal. So the two are not
#: peers, and an annual reading is never evidence on its own.
THE_NATAL_CHART_VETOES_AND_IS_NOT_VETOED = (
    "A result must be possible in the natal chart before the annual chart can "
    "deliver it. The part gives no reverse rule."
)

#: The finer charts the part announces, in its order.
TAJAKA_CHART_KINDS: tuple[dict[str, str], ...] = (
    {"chart": "Tajaka annual chart", "also": "Tajaka varsha chakra",
     "covers": "the one year following the solar return",
     "cast_for": "the Sun's return to its natal longitude"},
    {"chart": "Tajaka masa chakra", "also": "monthly solar return chart",
     "covers": "a one-month period, in depth", "cast_for": ""},
)

MASA_CHAKRA_RULE = (
    "Similar to the annual charts, \"monthly solar return charts\" (Tajaka "
    "masa chakras) can also be drawn and they are useful in analyzing a "
    "one-month period in depth."
)

DASAS_WITHIN_THE_YEAR = (
    "A few special dasa systems enable timing of events within the 365-day "
    "period of operation of an annual chart."
)

PART_4_SCOPE = (
    "This part explains the casting and use of annual charts in giving "
    "precise predictions."
)

#: **Finding.** A third opening that names nothing it will cover. Part 3's
#: opening promised "some" techniques, §26.1 promised "a couple of concepts"
#: and "a few principles", and this one promises "a few special dasa systems"
#: and names none of them. Only Part 2 gave a list to check off.
PART_4_NAMES_NONE_OF_ITS_DASAS = (
    "Part 4 says a few special dasa systems time events inside the year and "
    "names none. Part 3's opening and section 26.1 did the same; Part 2's "
    "roadmap of nine named systems remains the only checkable list."
)

#: **Watch this.** The part says "the 365-day period of operation of an annual
#: chart", but a solar return year is the interval between two returns of the
#: Sun to one sidereal longitude — about 365.2564 days. The two differ by some
#: six hours, which is nothing across one dasa and accumulates across a set of
#: them. Whether the special dasas divide 365 days or the true return interval
#: cannot be settled from this page; recorded so the arithmetic is checked
#: against the section that supplies it rather than assumed either way. Our
#: own `dasha_year_length` setting already offers both readings.
THE_YEAR_IS_CALLED_365_DAYS_AND_A_SOLAR_RETURN_IS_LONGER = (
    "The opening says the annual chart operates for 365 days. A sidereal "
    "solar return interval is about 365.2564 days. Which of the two the "
    "special dasas divide is not stated here."
)

#: The passages elsewhere in the book that were waiting on this part.
TAJAKA_WAS_PROMISED_BY: tuple[dict[str, str], ...] = (
    {"where": "footnote 68",
     "wants": "Tajaka annual and monthly charts for one-to-two-week "
              "predictions"},
    {"where": "footnote 74",
     "wants": "a Tajaka chart agreeing before a death reading may be made"},
    {"where": "Example 54, via OI-116",
     "wants": "the Rajya saham, deferred to the Tajaka part"},
    {"where": "Part 2's own map",
     "wants": "Sudarsana Chakra dasa, deferred to Tajaka Analysis"},
)

#: **Finding.** The opening page itself computes nothing: it says the part
#: will explain the casting and gives no moment rule, no place rule and no
#: ayanamsa convention. §27.1 supplies all three. What the opening promises
#: and §27.1 still does not give is a way to **read** an annual chart, so
#: footnote 74's bar on death readings is not lifted by either page.
THE_OPENING_PROMISES_THE_CASTING_AND_27_1_GIVES_IT = (
    "The opening states what a solar return is and defers the casting. "
    "Section 27.1 gives the moment and the place. Neither page says how to "
    "read the resulting chart, so nothing yet lifts footnote 74's bar."
)


# --------------------------------------------------------------------------
# §27.5 — chapter 27's conclusion
# --------------------------------------------------------------------------

CHAPTER_27_CONCLUSION = (
    "In this chapter, we learnt what Tajaka annual and monthly charts are and "
    "how they are cast. When Sun re-enters every year the same longitude "
    "occupied by him at the time of one's birth, it signals the commencement "
    "of a new year in the native's life. We can cast a chart for that exact "
    "moment and predict events in the next one year based on that chart. We "
    "can also cast monthly charts and sixty-hour charts."
)

THE_SOLAR_YEAR_IS_ONLY_AROUND_THE_BIRTHDAY = (
    "These new years are based on the solar years and the commencement of new "
    "year is around one's birthday as per the modern western calendar."
)

LUNAR_BIRTHDAYS_ARE_OUT_OF_SCOPE = (
    "However, many Indians – especially south Indians – celebrate birthday as "
    "per the lunar calendar. In fact, most Hindu holidays are based on the "
    "lunar calendar. For example, birthdays of Lord Rama and Lord Krishna are "
    "celebrated based on the tithi and not based on the solar calendar. Lunar "
    "calendar is of great importance in Indian culture. Correspondingly, "
    "there are techniques based on the birthday as per lunar calendar. "
    "However, those techniques are beyond the scope of this book and we will "
    "restrict ourselves to solar birthday and Tajaka annual charts."
)

#: **Finding.** "Around" is italicised, and it is the right word for the date
#: and much too generous for the time. Solving Example 118's native's varsha
#: pravesh for ninety-nine successive years puts it on his calendar birthday
#: **79 times**, a day later 19 times and a day earlier once — so the date is
#: nearly always right. The clock time sweeps the **whole twenty-four hours**
#: across those years. That is why an annual chart's ascendant bears no
#: relation to the natal one and why §27.1 insists on the exact moment.
THE_DATE_IS_STEADY_AND_THE_HOUR_IS_NOT = (
    "Over ninety-nine years one nativity's varsha pravesh falls on the "
    "western birthday 79 times, the day after 19 times and the day before "
    "once. Its clock time takes every hour of the day across the same span."
)

#: **Finding.** A whole family of techniques is named and excluded: the
#: **tithi-based** birthday and everything built on it. It is the fifth such
#: declaration in the book — the hora chart, Kendradi rasi dasa, shadbala and
#: the unlisted special lagnas are the others — and the only one that closes
#: off a calendar rather than a technique. Nothing here computes a lunar
#: return, and none is invented.
THE_LUNAR_RETURN_IS_A_NAMED_EXCLUSION = (
    "Section 27.5 names techniques based on the lunar-calendar birthday, says "
    "they are beyond the scope of the book, and restricts the part to the "
    "solar birthday. No tithi-based annual chart is built."
)

#: **Finding.** Three chapter conclusions, three different jobs. §25.7 restated
#: what its chapter had already said. §26.9 added a criterion — a test on
#: techniques that no earlier section stated. §27.5 draws a **boundary**: it
#: summarises and then says what the part will not cover. None of the three
#: does the same work as another.
THE_THREE_CONCLUSIONS_DO_DIFFERENT_WORK = (
    "Section 25.7 restated its chapter, section 26.9 added a coarseness test, "
    "and section 27.5 declares a scope boundary. Only 26.9 introduced a rule."
)

#: Chapter 27 end to end.
CHAPTER_27_IS_COMPLETE = (
    "§27.1 to §27.5, Table 71, Chart 66, Example 118, Exercise 47 and "
    "Footnotes 75 to 78, checked against the printed pages. The exact and "
    "approximate annual methods, the monthly charts and the sixty-hour "
    "charts are all built and reproduce the chapter's own figures. Closed "
    "here: OI-151. Opened here: D-78. Nothing yet reads an annual chart, so "
    "footnote 74's bar on death readings still stands."
)
