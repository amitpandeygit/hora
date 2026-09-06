"""Part 3's opening — what a transit is, and what this part is for.

Part 2 opened with a roadmap: a classification and the names of nine dasa
systems, held here as ``PART_2_DASA_SYSTEMS``. Part 3 opens with no such list.
It defines the word, says where positions come from, and says that "some" of
the techniques are explained — so there is nothing to check off as the part is
read, and no way to know from the opening when it is complete.

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

#: Part 3's definition of the word.
TRANSITS_MEANS = (
    "The constant movement of planets in the skies is what is meant by the "
    "word \"transits\" in astrology. Planets keep moving."
)

#: And what makes a transit readable: it is a relation between two charts, not
#: a property of the sky alone.
TRANSITS_RELATE_TWO_CHARTS = (
    "The relationship between (1) the positions of planets at a given time and "
    "(2) the positions of planets at a person's birthtime, will have a major "
    "impact on the kind of results that planets can give the person at the "
    "time."
)

#: The two inputs, named. Part 3 assumes both and reads the relation between
#: them; it computes neither.
TRANSIT_INPUTS: tuple[dict[str, str], ...] = (
    {"input": "1", "is": "the positions of planets at a given time",
     "source": "computer programs/software or ephemeris or almanacs "
               "(panchangas)"},
    {"input": "2", "is": "the positions of planets at a person's birthtime",
     "source": "the natal (birth) chart"},
)

#: Part 3's scope, and the reason it needs nothing new from the ephemeris:
#: positions are an assumption, and judging them is the subject.
POSITIONS_ARE_ASSUMED = (
    "Position of planets at any given time can be found out from computer "
    "programs/software or ephemeris or almanacs (panchangas). Judging the "
    "results for a person based on those, given the natal (birth) chart, is "
    "the subject of this part."
)

#: **Finding.** Both of Part 3's inputs are things the engine already produces
#: — a chart for any instant and a chart for a birth — so unlike Part 2, which
#: needed nine new period engines, Part 3 is a reading layer over positions we
#: have. What it will need is a way to ask for a chart at an arbitrary moment
#: alongside the natal one, which `compute_chart` already allows.
PART_3_NEEDS_NO_NEW_EPHEMERIS = (
    "Part 3's two inputs are a chart at a given time and a chart at birth. "
    "Both are computed today; the part is the reading between them."
)

#: Part 3 says "some", and names none. Recorded because Part 2's opening did
#: name its nine, so the absence is a difference and not an oversight of ours.
PART_3_IS_KNOWINGLY_PARTIAL = (
    "There are many special techniques in Vedic astrology for interpreting "
    "transits. Some of those techniques are explained in this part."
)

#: Whole constants that are a transcribed sentence or passage.
TRANSIT_VERBATIM_CONSTANTS: tuple[str, ...] = (
    "TRANSITS_MEANS",
    "TRANSITS_RELATE_TWO_CHARTS",
    "POSITIONS_ARE_ASSUMED",
    "PART_3_IS_KNOWINGLY_PARTIAL",
)


# --------------------------------------------------------------------------
# §26.1 — Chapter 26's opening
# --------------------------------------------------------------------------

#: What chapter 26 says chapter 25 was, and what it leaves undone. Note the
#: name it gives chapter 25 — "Transits and Natal References" — which is the
#: title the chapter itself carries.
CHAPTER_26_LOOKS_BACK_AT_25 = (
    "In the chapter \"Transits and Natal References\", we concentrated on "
    "correlating the natal chart and the transit chart using the rasis "
    "occupied by planets in both. There are some principles about rasi "
    "transits that we haven't yet covered. We will cover a couple of "
    "concepts in this chapter.")

#: The second thread, and the chapter's reason for existing.
NAKSHATRAS_ARE_AS_IMPORTANT_AS_RASIS = (
    "Nakshatras are also an important division of the zodiac and they are as "
    "important as rasis. By looking at the interactions between the "
    "nakshatras occupied by planets in the natal and transit charts, we can "
    "make some predictions about the results given by them at the time of "
    "the transit. We will look at a few principles.")

#: **Finding.** Chapter 25's whole apparatus was rasi-based — janma rasi,
#: house_of_rasi, the standard result tables, the two divisional interactions,
#: ashtakavarga and kakshyas. §25.6's sodhya-pinda timing was the one place a
#: **nakshatra** appeared as an output, and even there it was derived from a
#: product rather than from a graha's own nakshatra. Chapter 26 is the first
#: to read a transit nakshatra against a natal one directly.
CHAPTER_26_IS_THE_FIRST_TO_PAIR_NAKSHATRAS = (
    "Chapter 25 correlated the two charts by rasi throughout. The only "
    "nakshatra it produced was section 25.6's, computed from a rekha count "
    "times a sodhya pinda. Chapter 26 pairs the nakshatra a graha occupies "
    "natally with the one it occupies in transit."
)

#: **Finding.** The chapter announces itself as partial twice over — "some
#: principles ... that we haven't yet covered", "a couple of concepts", "a few
#: principles". Like Part 3's own opening it names nothing, so there is again
#: no list to check off as the chapter is read. Recorded so that reaching the
#: end of it is not mistaken for having covered rasi transits.
CHAPTER_26_NAMES_NOTHING_IT_WILL_COVER = (
    "Section 26.1 promises \"a couple of concepts\" and \"a few principles\" "
    "and names none of them, exactly as Part 3's opening promised \"some\" "
    "techniques and named none."
)

#: The two threads §26.1 sets out, in its order.
CHAPTER_26_THREADS: tuple[dict[str, str], ...] = (
    {"thread": "rasi transits",
     "why": "some principles about rasi transits that we haven't yet covered",
     "scope": "a couple of concepts"},
    {"thread": "nakshatra transits",
     "why": "the interactions between the nakshatras occupied by planets in "
            "the natal and transit charts",
     "scope": "a few principles"},
)


# --------------------------------------------------------------------------
# §26.9 — Chapter 26's conclusion
# --------------------------------------------------------------------------

CHAPTER_26_CONCLUSION = (
    "Several important topics related to transits in nakshatras were covered "
    "in this chapter. One should carefully learn and practice all these "
    "classical nakshatra-based techniques. However, new students should not "
    "make predictions just based on these techniques. Any technique that "
    "divides people into 27 groups and gives the same result for everyone in "
    "the same group can be correct only to a limited extent. These methods "
    "should be used in conjunction with other chart-sensitive methods."
)

#: §26.9's criterion, which is the one thing in it that is not a summary: a
#: coarseness test on a technique, stated as a reason and not as a rule.
THE_TWENTY_SEVEN_GROUP_CRITERION = (
    "Any technique that divides people into 27 groups and gives the same "
    "result for everyone in the same group can be correct only to a limited "
    "extent."
)

#: **Finding.** §25.7 introduced nothing that was not already in chapter 25 —
#: see `THE_CONCLUSION_INTRODUCES_NOTHING_NEW`. §26.9 does: the 27-group
#: criterion is a test on techniques rather than a technique, it is stated
#: nowhere else in the chapter as a general rule, and it applies to chapter 25
#: as much as to this one. The two conclusions are not the same kind of thing.
THIS_CONCLUSION_INTRODUCES_A_CRITERION = (
    "Section 25.7 restated what chapter 25 had already said. Section 26.9 "
    "adds a coarseness test that no earlier section states in general form."
)

#: **Finding.** §26.4.2 had already made this exact argument for **one**
#: technique, and §26.9 lifts it to the chapter: "any country has almost the
#: same number of people with desa nakshatra in each constellation", so
#: malefics in the desa nakshatra do not ruin a country. That is the 27-group
#: criterion in miniature, four sections earlier and applied to a single
#: nakshatra rather than to the family.
THE_CRITERION_GENERALISES_SECTION_26_4_2S_OWN_CAUTION = (
    "Section 26.4.2 says a country holds about as many people of each "
    "constellation, so a transit through the desa nakshatra cannot be read "
    "against the country. Section 26.9 makes the same argument about every "
    "technique in the chapter."
)

#: **Finding.** The conclusion summarises the chapter as "transits in
#: nakshatras" and so drops the **first** of the two threads §26.1 announced.
#: §26.2's murthis and §26.3's vedha are rasi techniques: the murthi is read
#: from the house the transit Moon holds from the natal Moon at a **rasi**
#: ingress, and Table 63's vedha sthanas are houses from the janma **rasi**.
#: Neither is a nakshatra technique, and §26.9 does not account for them.
THE_CONCLUSION_DROPS_THE_RASI_THREAD = (
    "Section 26.1 sets out rasi transits and nakshatra transits. Section "
    "26.9 says the chapter covered topics related to transits in nakshatras "
    "and says nothing of sections 26.2 and 26.3, which are keyed to rasis."
)

#: **Finding.** No technique in the chapter actually yields 27 results. Fixing
#: a transit and varying the nativity across the whole zodiac, §26.4.1's taras
#: give **9** verdicts, §26.6's body parts **6 to 9** depending on the table,
#: §26.4.2's special nakshatras at most **12**, §26.7's latta a **yes or no**,
#: and §26.2's murthi **4** — from a partition of 12 rather than 27. So the
#: criterion names the finest partition any of them uses and every technique
#: is coarser than that. It understates its own case.
NOT_ONE_TECHNIQUE_GIVES_TWENTY_SEVEN_RESULTS = (
    "The taras give nine verdicts over 27 birth stars, the body-part tables "
    "six to nine, the latta two, and the murthi four over a partition of "
    "twelve. Section 26.9's 27 is the number of groups a nativity may fall "
    "into, not the number of answers the techniques can give."
)

#: **Finding.** §26.8's chakra is the one technique in the chapter the
#: criterion does not reach, because it is the only one that reads natal
#: points of more than one **kind**: a nakshatra, a rasi, a tithi, a weekday
#: and a letter of the native's name. Every other section here reads a single
#: point, the natal Moon's nakshatra or its rasi. And it is exactly the
#: technique footnote 70 says the author has hardly used.
THE_CHAKRA_IS_THE_ONE_THE_CRITERION_DOES_NOT_REACH = (
    "Sarvatobhadra chakra takes five natal points of four kinds where every "
    "other technique in the chapter takes one, so it does not divide people "
    "into 27 groups. Footnote 70 disclaims the author's experience of it."
)

#: **Finding.** The chapter is hedged four times and each hedge is wider than
#: the last: footnote 70 on the author's own experience of one technique,
#: footnote 74 on death readings and what must corroborate them, footnote 72
#: on the nakshatra principles as a family, and §26.9 on the chapter. Only
#: footnote 74 names **what** to use instead — dasas and the Tajaka chart.
#: §26.9 asks for "other chart-sensitive methods" and names none, so the
#: chapter's last word is also its least specific.
THE_FOUR_HEDGES_WIDEN_AND_THE_LAST_NAMES_NOTHING = (
    "Footnote 70 limits one technique, footnote 74 one kind of prediction, "
    "footnote 72 the nakshatra principles and section 26.9 the chapter. The "
    "only hedge that names a remedy is footnote 74."
)

#: **Finding.** "New students should not make predictions just based on these
#: techniques" is addressed to the reader's experience, not to the technique.
#: Nothing in the chapter says what changes for a practised reader, and the
#: 27-group criterion that follows it is about the method and holds whoever
#: is reading. So the sentence and its reason are not about the same thing.
THE_CAUTION_IS_ADDRESSED_TO_THE_READER_AND_THE_REASON_IS_NOT = (
    "The caution names new students. The reason given for it, that a "
    "27-group technique can be correct only to a limited extent, is a "
    "property of the technique and does not depend on who is reading."
)

#: Chapter 26 end to end, and what it leaves open.
CHAPTER_26_IS_COMPLETE = (
    "§26.1 to §26.9, Tables 62 to 70, Figure 3, Examples 113 to 117, "
    "Exercises 41 to 46 and Footnotes 70 to 74, checked against the printed "
    "pages. The chapter prints no chart of its own and reuses Chart 39, "
    "Chart 56 and Chart 60. Opened here: OI-144, OI-145, OI-148, OI-149 and "
    "OI-150, and D-74 to D-77. Closed here: OI-146 and OI-147."
)
