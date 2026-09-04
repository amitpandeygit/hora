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
