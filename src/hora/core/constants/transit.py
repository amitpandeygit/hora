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
