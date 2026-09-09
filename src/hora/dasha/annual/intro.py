"""§30.1 — Introduction to the annual dasas.

Three dasas compressed to the year an annual chart covers, and the choice the
chapter makes about how to seed two of them.
"""

from __future__ import annotations

from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS

CHAPTER_TITLE = "Annual Dasas"


# --------------------------------------------------------------------------
# §30.1's three paragraphs
# --------------------------------------------------------------------------

#: The question the chapter exists to answer, verbatim.
WHY_ANNUAL_DASAS = (
    "We have studied different dasa systems that enable us to time events in "
    "a person's life. In the previous few chapters, we have seen how Tajaka "
    "annual charts show the fortune in a one-year period. The next question "
    "is - how do we time events shown in a Tajaka annual chart? For example, "
    "an annual chart may show that the native will get married in the year. "
    "The question is - when in the year will (s)he get married?"
)

#: The second paragraph, verbatim.
WHY_THEY_MUST_BE_COMPRESSED = (
    "All the dasas covered earlier are valid for natal charts and their "
    "paramayush is of the order of 100 years. On the other hand, an annual "
    "chart applies only for a period of one year. So we need dasas that are "
    "compressed to a one-year period."
)

#: The third paragraph, verbatim.
HOW_THE_TWO_COMPRESSED_DASAS_ARE_SEEDED = (
    "In Vimsottari dasa and Narayana dasa, paramayush of 120 years is "
    "compressed to one year. One may try finding compressed Vimsottari dasa "
    "based on Moon's constellation in the annual chart, but the best results "
    "are obtained by progressing Moon's constellation in the natal chart at "
    "the rate of one constellation per year and using it to initiate dasas. "
    "Similarly, one may try finding compressed Narayana dasa based on lagna "
    "in the annual chart, but the best results are obtained by progressing "
    "lagna in the natal chart at the rate of one sign per year and using it "
    "as lagna for the purpose of Narayana dasa."
)

#: The three dasas the chapter will teach, in its own order.
ANNUAL_DASAS: tuple[dict[str, object], ...] = (
    {"number": 1, "name": "Patyayini dasa",
     "also_called": ("Varsha dasa",), "source": "mentioned by Tajaka writers",
     "compressed_from": None},
    {"number": 2, "name": "Mudda dasa",
     "also_called": ("Varsha Vimsottari dasa",), "source": None,
     "compressed_from": "vimshottari"},
    {"number": 3, "name": "Varsha Narayana dasa",
     "also_called": (), "source": None, "compressed_from": "narayana"},
)

#: Footnote 85, verbatim.
FOOTNOTE_85 = "Dr. B.V. Raman simply called this \"Varsha dasa\" (annual dasa)."

#: Footnote 86, verbatim.
FOOTNOTE_86 = "This is a result of the author's own researches."


# --------------------------------------------------------------------------
# The seeding choice
# --------------------------------------------------------------------------

#: The two dasas §30.1 seeds by progression, with the reading it declines and
#: the reading it takes. Footnote 86 attaches to both.
SEEDING_CHOICES: tuple[dict[str, str], ...] = (
    {"dasa": "Mudda dasa",
     "seed": "Moon's constellation",
     "declined": "Moon's constellation in the annual chart",
     "taken": ("Moon's constellation in the natal chart progressed at one "
               "constellation per year"),
     "rate": "one constellation per year"},
    {"dasa": "Varsha Narayana dasa",
     "seed": "lagna",
     "declined": "lagna in the annual chart",
     "taken": ("lagna in the natal chart progressed at one sign per year"),
     "rate": "one sign per year"},
)

#: **Finding.** The chapter builds its annual charts for one year and then
#: declines to seed two of its three dasas **from** that chart. Both are seeded
#: by progressing the **natal** chart instead, so a Varsha Vimsottari or Varsha
#: Narayana dasa needs the nativity as well as the annual chart, where the
#: whole of chapters 27 to 29 needed only the annual chart. §30.1 states the
#: obvious alternative in both cases and rejects it in the same sentence.
THE_ANNUAL_CHART_IS_NOT_THE_SEED = (
    "Sections 27 to 29 read the annual chart alone. Two of chapter 30's three "
    "dasas are seeded from the natal chart progressed, not from the annual "
    "chart, and the annual-chart reading is named and declined in both cases."
)

#: **Finding.** The two progressions run at different rates because they count
#: different things: one constellation a year against one sign a year. Twenty-
#: seven constellations and twelve signs, so the Moon's seed returns to its
#: natal place after **27** years and the lagna's after **12**. The chapter
#: does not say what happens at either return.
THE_TWO_PROGRESSIONS_HAVE_DIFFERENT_PERIODS = (
    "One constellation a year cycles in 27 years and one sign a year in 12, "
    "so the two seeds return to their natal places on different schedules."
)

#: **Provenance, and the second place in the book to label its own technique.**
#: Footnote 86 marks the progression rule as "a result of the author's own
#: researches". §25.4 did the same for its whole section. Nothing else in the
#: book carries such a mark. See docs/precedence.md.
FOOTNOTE_86_IS_A_PROVENANCE_MARK = (
    "Footnote 86 labels the progression rule as the author's own research. "
    "Section 25.4 labels its whole section the same way. Those are the two "
    "places in the book that do it."
)

#: **Finding.** Footnote 86 is attached to the **Narayana** sentence, at the
#: end of the paragraph. Whether it also covers the Vimsottari sentence, which
#: makes the same claim in the same words one sentence earlier, is not marked.
#: The two rules are stated as a pair — "similarly" — so the natural reading is
#: that both are the author's, and the footnote is placed on only one.
WHETHER_FOOTNOTE_86_COVERS_BOTH_RULES_IS_NOT_MARKED = (
    "Footnote 86 sits on the Narayana sentence. The Vimsottari sentence "
    "makes the same claim one sentence earlier and carries no footnote, and "
    "the second sentence opens with \"similarly\"."
)

#: **Book defect.** "In Vimsottari dasa and Narayana dasa, paramayush of 120
#: years is compressed to one year." Vimsottari's paramayush **is** 120 years
#: exactly. **Narayana dasa's is 144.** Every rasi's first-cycle length is 1 to
#: 12 years and its second cycle is 12 minus that, so first and second together
#: are always 12, and twelve rasis give 144 whatever the chart. Neither is the
#: first cycle alone a fixed number, so 120 is not that either. The figure
#: matters: it is the divisor a compressed Narayana dasa is built on, and 120
#: against 144 moves every sub-period by a fifth. See OI-174.
NARAYANA_DASAS_PARAMAYUSH_IS_144_NOT_120 = (
    "Vimsottari dasa's paramayush is 120 years. Narayana dasa's full cycle is "
    "144 years - twelve years per rasi across both cycles, for twelve rasis - "
    "and the first cycle alone is not a fixed total at all."
)

#: **Finding.** "Their paramayush is of the order of 100 years" is loose but
#: not wrong for the systems the book taught: they run from 36 years
#: (shattrimsa sama) to 120 (vimsottari), and seven of the ten nakshatra dasas
#: sit between 84 and 120.
THE_ORDER_OF_A_HUNDRED_IS_A_RANGE_NOT_A_FIGURE = (
    "The nakshatra dasas the book taught run from 36 years to 120. Seven of "
    "the ten are between 84 and 120, which is what \"of the order of 100 "
    "years\" describes."
)


def paramayush(system: str) -> int:
    """A nakshatra dasa system's paramayush in years, from chapter 15's own
    table. `vimshottari` is the 120 §30.1 names.
    """
    return int(NAKSHATRA_DASHA_SYSTEMS[system].total_years)


def narayana_full_cycle_years() -> int:
    """Narayana dasa's paramayush: twelve years a rasi, twelve rasis.

    Derived rather than asserted — see
    `NARAYANA_DASAS_PARAMAYUSH_IS_144_NOT_120`.
    """
    from hora.dasha.rasi.narayana import second_cycle_length

    return sum(first + second_cycle_length(first) for first in range(1, 13))
