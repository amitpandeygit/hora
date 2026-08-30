"""Part 2's own map of the dasa systems it will teach.

The part opens by classifying dasa systems two ways and then naming the nine
it covers. That list is a roadmap, not a calculation, but it is worth holding
as data: it says which systems the book considers in scope, what each is for,
and — read against what is built — what is still missing.

Two classifications, both from the opening:

* **nakshatra** dasas run from the Moon's nakshatra; **rasi** dasas run from
  the rasis planets occupy, and their periods are owned by rasis.
* **phalita** dasas give general results; **ayur** dasas predict death.

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

#: Why the classics do not settle which dasa to use when.
DASA_USES_ARE_NOT_IN_THE_CLASSICS = (
    "Hundreds of dasa systems were enumerated by the seers of Vedic "
    "astrologey. Specific uses of these dasa systems weren't clearly "
    "mentioned in classics. These are hidden in remote corners of India as "
    "family secrets."
)

#: The nine systems Part 2 teaches, in the order it lists them. ``kind`` is
#: nakshatra or rasi; ``purpose`` is the part's own parenthesis, kept in its
#: printed order — Vimsottari reads "phalita/ayur" and Ashtottari
#: "ayur/phalita", which is the only thing distinguishing their emphasis.
PART_2_DASA_SYSTEMS: tuple[dict, ...] = (
    {"name": "Vimsottari dasa", "kind": "nakshatra",
     "purpose": "phalita/ayur", "key": "vimshottari"},
    {"name": "Ashtottari dasa", "kind": "nakshatra",
     "purpose": "ayur/phalita", "key": "ashtottari"},
    {"name": "Narayana dasa", "kind": "rasi",
     "purpose": "phalita - general", "key": None},
    {"name": "Lagna Kendradi Rasi dasa", "kind": "rasi",
     "purpose": "phalita - material fortune", "key": None},
    {"name": "Sudasa", "kind": "rasi",
     "purpose": "phalita - material fortune", "key": None},
    {"name": "Drigdasa", "kind": "rasi",
     "purpose": "phalita - spirituality", "key": None},
    {"name": "Niryaana Shoola dasa", "kind": "rasi",
     "purpose": "ayur", "key": None},
    {"name": "Shoola dasa", "kind": "rasi", "purpose": "ayur", "key": None},
    {"name": "Kalachakra dasa", "kind": "nakshatra",
     "purpose": "phalita", "key": None},
)

#: Named in Part 2 but deliberately deferred by it.
DEFERRED_TO_TAJAKA = (
    "Sudarsana Chakra dasa is one of the most important dasas mentioned by "
    "Parasara. However, for reasons that will become clear later, we will "
    "learn it in the part \"Tajaka Analysis\"."
)

#: Whole constants that are a transcribed sentence or passage.
DASHA_VERBATIM_CONSTANTS: tuple[str, ...] = (
    "DASA_USES_ARE_NOT_IN_THE_CLASSICS",
    "DEFERRED_TO_TAJAKA",
)
