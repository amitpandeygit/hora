"""Section 13.4.2 — reading family members from one's own chart."""
from __future__ import annotations

FAMILY_INTRO = (
    "We can analyze the fortunes of family members from one's chart. For "
    "parents, grandparents, uncles and aunts, we should see D-12. For "
    "children, children-in-law and grandchildren, we should see D-7. For "
    "brothers, sisters, brothers-in-law and sister-in-law, we should see D-3. "
    "For spouse and his/her family members, we should see D-9."
)

#: Which chart each family of relations is read from.
FAMILY_CHARTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("D12", ("parents", "grandparents", "uncles", "aunts")),
    ("D7", ("children", "children-in-law", "grandchildren")),
    ("D3", ("brothers", "sisters", "brothers-in-law", "sisters-in-law")),
    ("D9", ("spouse", "spouse's family members")),
)

FAMILY_METHOD = (
    "In each of these charts, we should look at the house that shows the "
    "person of interest and consider the rasi containing the lord of that "
    "house as lagna. We can consider the corresponding arudha pada also. For "
    "example, the 9th lord or the arudha pada of 9th house in D-12 shows "
    "father. The 4th lord or the arudha pada of 4th house in D-12 shows "
    "mother."
)

#: The two people §13.4.2 names outright, with the house each is read from.
NAMED_RELATIVES: tuple[tuple[str, str, int], ...] = (
    ("father", "D12", 9),
    ("mother", "D12", 4),
)

SIBLINGS_RULE = (
    "In D-3, we see siblings. The 3rd house shows younger sibling and the "
    "11th house shows elder sibling. Being the 3rd from the 3rd house, the "
    "5th house shows younger brother's younger brother, i.e. second younger "
    "brother. Being the 11th from the 11th house, the 9th house shows elder "
    "brother's elder brother, i.e. second elder brother. We take the 3rd "
    "lord, 5th lord, 7th lord etc as lagnas of first (immediate) younger "
    "sibling, second younger sibling, third younger sibling etc. We take the "
    "11th lord, 9th lord, 7th lord etc as lagnas of first (immediate) elder "
    "sibling, second elder sibling, third elder sibling etc."
)

CHILDREN_RULE = (
    "Similarly, the 5th house house shows children in D-7. The 7th house is "
    "the 3rd from 5th and shows one's child's younger sibling. So the 5th "
    "lord shows the first child, the 7th lord shows the second child, the 9th "
    "house shows the third child and so on."
)

#: The three "being the nth from the nth" claims §13.4.2 makes, as
#: ``(inner house, step, result)``. Each is checked arithmetically.
NESTED_HOUSE_CLAIMS: tuple[tuple[int, int, int], ...] = (
    (3, 3, 5),     # the 3rd from the 3rd is the 5th
    (11, 11, 9),   # the 11th from the 11th is the 9th
    (5, 3, 7),     # the 3rd from the 5th is the 7th
)

DIRECTION_RULE = (
    "When we count houses corresponding to siblings and children in D-3 and "
    "D-7, we count in the forward or backward direction based on whether "
    "lagna is odd or even (respectively). If lagna in D-7 is in Ge, Venus "
    "(lord of Li) shows first child, Jupiter (lord of Sg) shows the second "
    "child and so on. On the other hand, if lagna in D-7 is in Cn, Jupiter "
    "(lord of Pi) shows the first child, Saturn (lord of Cp) shows the second "
    "child and so on."
)

#: §13.4.2's two worked D-7 examples: ``(lagna, direction, first two children
#: as (sign, lord))``.
DIRECTION_EXAMPLES: tuple[
        tuple[str, str, tuple[tuple[str, str], ...]], ...] = (
    ("Ge", "forward", (("Li", "Venus"), ("Sg", "Jupiter"))),
    ("Cn", "backward", (("Pi", "Jupiter"), ("Cp", "Saturn"))),
)

#: The direction rule is scoped to D-3 and D-7. D-12's father and mother are
#: counted the ordinary way, and §13.4.2 does not extend it to them.
DIRECTION_SCOPE = (
    "The forward/backward rule is stated for siblings and children in D-3 and "
    "D-7 only. Section 13.4.2 does not apply it to D-12's 9th and 4th houses, "
    "so father and mother are counted forward as usual."
)

FAMILY_NOTE = (
    "After covering all the odd or even signs, we move from odd to even signs "
    "or even to odd signs, instead of coming back to where we started."
)

#: Stepping by two houses from an odd sign stays among the six odd signs, and
#: from an even sign among the six even ones — so a chain runs exactly six
#: deep before the note takes over.
FAMILY_CHAIN_DEPTH = 6

#: **Gap.** The note says to move to the other parity but not *which* sign of
#: it comes next, so the seventh sibling or child cannot be placed. See
#: docs/open-items.md OI-106.
FAMILY_NOTE_IS_UNDERSPECIFIED = (
    "The note says that after all six signs of one parity are used we move to "
    "the other parity instead of returning to the first sign. It does not say "
    "which sign of the other parity comes next, and no example in the section "
    "reaches a seventh sibling or child. So chains are answered six deep and "
    "the seventh is refused with this reason rather than guessed."
)
