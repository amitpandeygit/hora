"""Section 13.3 — baadhakas.

Table 31 is transcribed, and every one of its twenty-four entries is also
derived from the rule above it, so the table checks the rule and the rule
checks the table.
"""
from __future__ import annotations

BAADHAKA_RULE = (
    "For a house falling in a movable/fixed/dual rasi, the 11th/9th/7th house "
    "(respectively) from there becomes baadhaka sthaana (troubling spot). Its "
    "lord is called a “baadhaka” (troublemaker) for the original house. "
    "The list of baadhaka sthaanas and baadhakas corresponding to each rasi is "
    "given in Table 31.")

BAADHAKA_STHAANA_MEANS = "troubling spot"
BAADHAKA_MEANS = "troublemaker"

#: The rule as data, indexed by `RASI_MODALITY` — 0 movable, 1 fixed, 2 dual.
BAADHAKA_HOUSE_BY_MODALITY: tuple[int, int, int] = (11, 9, 7)

#: Table 31. ``rasi -> (baadhaka sthaana, baadhakas)``. Aries and Capricorn
#: carry two baadhakas each because their sthaanas are the co-owned rasis, and
#: Table 31 names **both** co-lords rather than the stronger one — so §15.5.1's
#: cascade is not involved here, unlike §9.2's arudha.
TABLE_31_BAADHAKAS: dict[str, tuple[str, tuple[str, ...]]] = {
    "Ar": ("Aq", ("Saturn", "Rahu")),
    "Ta": ("Cp", ("Saturn",)),
    "Ge": ("Sg", ("Jupiter",)),
    "Cn": ("Ta", ("Venus",)),
    "Le": ("Ar", ("Mars",)),
    "Vi": ("Pi", ("Jupiter",)),
    "Li": ("Le", ("Sun",)),
    "Sc": ("Cn", ("Moon",)),
    "Sg": ("Ge", ("Mercury",)),
    "Cp": ("Sc", ("Mars", "Ketu")),
    "Aq": ("Li", ("Venus",)),
    "Pi": ("Vi", ("Mercury",)),
}

#: Table 31 names both co-lords where the sthaana is co-owned. Recorded
#: because §9.2 does the opposite — it needs the *stronger* co-lord — and the
#: difference is easy to get wrong.
BAADHAKA_TAKES_BOTH_CO_LORDS = (
    "Aries' baadhaka sthaana is Aquarius and Capricorn's is Scorpio, the two "
    "co-owned rasis. Table 31 lists both co-lords for each — Saturn and Rahu, "
    "Mars and Ketu — rather than the stronger one. Section 15.5.1's cascade "
    "is not involved, which is the opposite of what section 9.2's arudha "
    "needs from the same two rasis.")

BAADHAKA_EXAMPLE = (
    "For example, suppose lagna in someone's D-10 is in Ge. Then Jupiter is "
    "baadhaka for lagna. The periods of Jupiter and planets in Sg can create "
    "some obstructions and troubles in career. Let us take another house. Aq "
    "is the 9th house and the 9th house in D-10 shows the guidance one gets "
    "in one's career. It can show manager and elders giving guidance. "
    "Baadhaka sthana for Aq is Li. So the periods of Venus and occupants of "
    "Li can create some troubles related to the guidance one gets. There may "
    "be some troubles related to manager. Thus we can consider baadhaka from "
    "every house and arudha pada in every divisional chart.")

#: The example as data: ``(what is being read, its rasi, the sthaana, who
#: troubles it, what the trouble is about)``. Both halves share one D-10 whose
#: lagna is Gemini.
BAADHAKA_EXAMPLE_STEPS: tuple[tuple[str, str, str, tuple[str, ...], str], ...] = (
    ("lagna", "Ge", "Sg", ("Jupiter",),
     "obstructions and troubles in career"),
    ("the 9th house", "Aq", "Li", ("Venus",),
     "troubles related to the guidance one gets, and to the manager"),
)

#: §13.3's own statement of scope, and the reason §13.4.1 can say "if a planet
#: is a baadhaka from A3".
BAADHAKA_SCOPE = (
    "Thus we can consider baadhaka from every house and arudha pada in every "
    "divisional chart.")

#: Not only the lord: the example troubles by "the periods of Jupiter **and
#: planets in Sg**", and again by "the periods of Venus **and occupants of
#: Li**". Occupancy of the sthaana matters as much as owning it.
BAADHAKA_INCLUDES_OCCUPANTS = (
    "A baadhaka sthaana troubles through its lord and through whoever "
    "occupies it. Both halves of section 13.3's example say so — 'the periods "
    "of Jupiter and planets in Sg', and 'the periods of Venus and occupants "
    "of Li'.")
