"""Aspects — book chapter 10.

§10.1: "Planets aspect other planets, rasis and houses in astrology." Two
kinds, and the chapter separates them at the outset:

* **graha drishti** (planetary aspect) — each graha aspects certain houses
  *counted from itself*, and the houses are fixed per graha;
* **rasi drishti** (sign aspect) — rasis aspect each other, and a graha
  inherits the aspects of the rasi it occupies.

Import from :mod:`hora.core.const`, which re-exports every constant.
"""
from __future__ import annotations

from hora.core.constants.graha import Graha

#: §10.2's heading is printed "Graha Drishri". Every other use in the chapter,
#: including §10.1's own sentence, spells it "drishti". Recorded so the typo is
#: not mistaken for a term.
GRAHA_DRISHTI_HEADING_AS_PRINTED = "Graha Drishri"
DRISHTI_MEANS = "aspect"

#: §10.1, in full.
ASPECT_DEFINITION = (
    "Planets aspect other planets, rasis and houses in astrology. A planet "
    "aspecting a house or a planet has some influence on the matters signified "
    "by that house or planet. The nature of the influence exerted and the "
    "degree to which that influence succeeds depends on the individual "
    "situation."
)

#: The two kinds, with what §10.1 says distinguishes them.
ASPECT_KINDS: dict[str, dict] = {
    "graha_drishti": {
        "name": "graha drishti",
        "gloss": "planetary aspect",
        "rule": (
            "Each planet aspects certain houses from it with graha drishti. "
            "The houses aspected are fixed based on the planet."
        ),
        "counted_from": "the graha",
        "varies_by": "graha",
    },
    "rasi_drishti": {
        "name": "rasi drishti",
        "gloss": "sign aspect",
        "rule": (
            "Rasis aspect each other and a planet aspects the rasis aspected "
            "by the rasi occupied by it."
        ),
        "counted_from": "the rasi occupied",
        "varies_by": "rasi",
    },
}

#: §10.2's universal rule, stated before any exception.
SEVENTH_HOUSE_RULE = (
    "All planets aspect the 7th house from them. Find the 7th house from the "
    "planet and the planet aspects that house."
)

#: §10.2's five worked one-liners for the 7th-house rule.
SEVENTH_HOUSE_EXAMPLES: tuple[tuple[int, int, int], ...] = (
    (Graha.SUN, 1, 7),        # Sun in Ta aspects Sc
    (Graha.MARS, 2, 8),       # Mars in Ge aspects Sg
    (Graha.MOON, 4, 10),      # Moon in Le aspects Aq
    (Graha.JUPITER, 11, 5),   # Jupiter in Pi aspects Vi
    (Graha.SATURN, 9, 3),     # Saturn in Cp aspects Cn
)

#: §10.2: "In addition, Mars, Jupiter and Saturn have special aspects."
#: Exactly three grahas, and the chapter names no others.
SPECIAL_ASPECT_GRAHAS: tuple[int, ...] = (Graha.MARS, Graha.JUPITER, Graha.SATURN)
SPECIAL_ASPECT_RULE = "In addition, Mars, Jupiter and Saturn have special aspects."

#: The three bullets, in the chapter's own order — Jupiter, Mars, Saturn.
SPECIAL_ASPECT_BULLETS: tuple[dict, ...] = (
    {"graha": Graha.JUPITER, "houses": (5, 9),
     "text": "Jupiter aspects the 5th and 9th houses from him, in addition to "
             "the 7th house."},
    {"graha": Graha.MARS, "houses": (4, 8),
     "text": "Mars aspects the 4th and 8th houses from him, in addition to the "
             "7th house."},
    {"graha": Graha.SATURN, "houses": (3, 10),
     "text": "Saturn aspects the 3rd and 10th houses from him, in addition to "
             "the 7th house."},
)

#: §10.2's rule for turning aspected houses into aspected planets. A graha is
#: aspected because of *where it sits*, never in its own right.
ASPECTED_PLANET_RULE = (
    "We can decide the signs and houses aspected by a planet as above. If any "
    "planet occupies the aspected houses, then the planet is also aspected."
)
ASPECTED_PLANET_EXAMPLE = (
    "Jupiter in Ta will aspect Saturn in Cp, because Cp is the 9th house from "
    "Ta and Jupiter aspects the 9th from him."
)

#: §10.2 closes by telling the reader to practise on charts rather than giving
#: another rule. Recorded because it is the chapter's own statement of what the
#: computation is for.
ASPECTS_ARE_A_SKILL_NOTE = (
    "Look at a few charts and figure out which planets are aspecting which "
    "houses and which planets are aspecting which planets. With experience, "
    "you can become good at it and this is an important skill required in "
    "interpreting charts."
)


# --------------------------------------------------------------------------
# §10.3 Rasi drishti
# --------------------------------------------------------------------------

#: §10.3's three rules, in the order printed. Unlike §10.2's special aspects
#: these *are* derivable — the modality decides everything — which is why
#: `charts/aspects.py` computes them from `RASI_MODALITY` rather than storing
#: twelve rows.
RASI_DRISHTI_RULES: tuple[dict, ...] = (
    {"modality": "movable", "aspects": "fixed", "excludes": "adjacent",
     "text": "A movable rasi aspects all fixed rasis except the one adjacent "
             "to it."},
    {"modality": "fixed", "aspects": "movable", "excludes": "adjacent",
     "text": "A fixed rasi aspects all movable rasis except the one adjacent "
             "to it."},
    {"modality": "dual", "aspects": "dual", "excludes": "itself",
     "text": "A dual rasi aspects all other dual rasis."},
)
RASI_DRISHTI_INTRO = "Rasis aspect other rasis based on the following rules:"

#: §10.3's three worked examples, one per rule.
RASI_DRISHTI_EXAMPLES: tuple[dict, ...] = (
    {"rasi": 0, "modality": "movable", "excluded": 1, "aspects": (4, 7, 10),
     "text": "Ar is a movable sign. It aspects all the fixed signs except the "
             "one adjacent to it, i.e. Ta. So Ar aspects Le, Sc and Aq."},
    {"rasi": 1, "modality": "fixed", "excluded": 0, "aspects": (3, 6, 9),
     "text": "Ta is a fixed sign. It aspects all the movable signs except the "
             "one adjacent to it, i.e. Ar. So Ta aspects Cn, Li and Cp."},
    {"rasi": 2, "modality": "dual", "excluded": None, "aspects": (5, 8, 11),
     "text": "Ge is a dual sign. It aspects all other dual signs. So Ge "
             "aspects Vi, Sg and Pi."},
)

#: §10.3 states mutuality outright, which §10.2's graha drishti never does.
RASI_DRISHTI_IS_MUTUAL = (
    "It may be noted that sign Y will aspect sign X if sign X aspects sign Y."
)

#: Figure 2 draws one line per aspecting pair. Mutuality is what makes an
#: undirected line the right picture.
FIGURE_2_NOTE = (
    "A visual representation of rasi aspects is given in Figure 2. A line is "
    "drawn between every pair of signs that aspect each other."
)

#: How a graha inherits its rasi's aspects, and what it reaches.
RASI_DRISHTI_GRAHA_RULE = (
    "A planet aspects the signs aspected by the sign it occupies. It also "
    "aspects the houses and planets in those signs. This is called rasi "
    "drishti (sign aspect)."
)
RASI_DRISHTI_GRAHA_EXAMPLE = (
    "A planet in Libra will aspect the houses and planets in Aq, Ta and Le."
)


# --------------------------------------------------------------------------
# §10.4 Graha drishti vs rasi drishti
# --------------------------------------------------------------------------

#: §10.4 adds no calculation. It says what each kind of aspect *is*, and the
#: distinction changes how a reading is built, so it is recorded as data rather
#: than left in prose.
#:
#: **Nothing here is quantified.** The chapter calls graha drishti "greater
#: influence" and rasi drishti "limited influence on the neighbors" — a
#: comparison, never a number. Turning that into a weight would be our
#: invention, not PVR's.
ASPECT_SOURCE: dict[str, dict] = {
    "rasi_drishti": {
        "due_to": "the sign a planet is in",
        "analogy": "the influence people exert on their neighbors",
        "scope": "limited influence on the neighbors",
        "targets_shared_by_co_located_grahas": True,
        "nature_shared_by_co_located_grahas": False,
        "statement": (
            "Influence exerted by rasi drishti is due to the sign a planet is "
            "in. This is analogous to the influence people exert on their "
            "neighbors."
        ),
    },
    "graha_drishti": {
        "due_to": "the inherent nature of a planet",
        "analogy": (
            "the influence a priest has in the matters of the nearby temple "
            "where he works"
        ),
        "scope": "greater influence in the matters of the temple where he works",
        "targets_shared_by_co_located_grahas": False,
        "nature_shared_by_co_located_grahas": False,
        "statement": (
            "Influence exerted by graha drishti is due to the inherent nature "
            "of a planet. Different planets in the same sign may aspect "
            "different houses and planets with graha drishti."
        ),
    },
}

#: §10.4's central claim about rasi drishti: the *targets* are the sign's, the
#: *nature* is the graha's. Two grahas in one sign reach the same signs and do
#: different things there.
RASI_DRISHTI_SAME_TARGETS_DIFFERENT_NATURE = (
    "All planets in a sign will have rasi drishti on the same signs, just as "
    "people living in the same house see the same neighbors everyday and exert "
    "some influence over the same neighbors. But the influence they exert may "
    "differ. Thus, planets in the same sign exert influence on the same houses "
    "and planets through rasi drishti, but the nature of the influence varies "
    "from planet to planet."
)

#: The 7th house is the one target every graha shares, whatever it is and
#: wherever it sits — the analogy's family friends.
SEVENTH_HOUSE_ANALOGY = (
    "Everyone in a house may have a strong influence over friends of the "
    "family who visit the house frequently. Similarly, all planets aspect the "
    "7th house from them and have an influence over it."
)

#: §10.4's worked pair, kept because the chapter builds its whole distinction
#: on it: the priest and his movie-loving brother share a house, so they share
#: their neighbours, and they influence them in opposite directions.
PRIEST_AND_BROTHER_ANALOGY = (
    "A priest may tell his neighbors to pray to God. His movie-loving brother "
    "living in the same house may talk the same neighbors into watching all "
    "the movies of a particular actress."
)

#: §10.4's second example, and the reason an aspect is not good news by
#: default: the criminal influences his neighbours too.
MALEFIC_INFLUENCE_ANALOGY = (
    "Let us take a dreaded criminal as another example. He may also have an "
    "influence on his neighbors. Youngsters living in the neighboring houses "
    "may enter the criminal world because of him."
)

#: The claim that limits every aspect in the chapter. §10.1 states it too:
#: "the degree to which that influence succeeds depends on the individual
#: situation." §10.4 gives it a case — the criminal neighbour who is not
#: influenced by the priest.
#:
#: **Not modelled.** Nothing in the engine decides whether an aspect lands;
#: it decides only that the aspect exists. See OI-64.
INFLUENCE_MAY_NOT_LAND = (
    "How pious and god-fearing his influence makes his neighbors depends on "
    "other factors. If one of the neighbors is a dreaded criminal, he is not "
    "going to be influenced."
)
INFLUENCE_DEPENDS_ON_RECEIVER = (
    "Whether an aspect takes effect depends on the aspected graha or house as "
    "well as the aspecting graha. The engine reports that an aspect exists, "
    "never that it succeeds."
)
