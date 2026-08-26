"""Jaimini rasi drishti — the sign aspects section 15.5.1's rule 2 needs.

This table was **wrong** until §15.5.1's own worked example exposed it: the
example says "Rahu in Ar is aspected by Mars, his dispositor, from Le", and
Leo did not aspect Aries. All three modality rows were wrong. See
docs/open-items.md OI-27.

These tests pin the rule structurally rather than by listing 36 pairs, so a
future edit has to break an invariant to get through.
"""
import pytest

from hora.charts.aspects import rasi_drishti
from hora.core.const import RASI_MODALITY, RASI_NAMES

MOVABLE, FIXED, DUAL = 0, 1, 2

#: Which modality each modality aspects. Movable and fixed aspect each other;
#: dual aspects only dual.
ASPECTED_MODALITY = {MOVABLE: FIXED, FIXED: MOVABLE, DUAL: DUAL}

ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def test_the_section_15_5_1_example_holds():
    """"Rahu in Ar is aspected by Mars, his dispositor, from Le".

    This single assertion is what caught the original bug.
    """
    assert ABBR.index("Ar") in rasi_drishti(ABBR.index("Le"))


@pytest.mark.parametrize("sign", range(12))
def test_every_sign_aspects_exactly_three(sign):
    assert len(rasi_drishti(sign)) == 3
    assert len(set(rasi_drishti(sign))) == 3


@pytest.mark.parametrize("sign", range(12))
def test_targets_are_all_of_the_right_modality(sign):
    """Movable aspect fixed, fixed aspect movable, dual aspect dual.

    The old table sent movable signs to a movable and a dual target.
    """
    expected = ASPECTED_MODALITY[RASI_MODALITY[sign]]
    for target in rasi_drishti(sign):
        assert RASI_MODALITY[target] == expected, (
            f"{RASI_NAMES[sign]} aspects {RASI_NAMES[target]}, "
            f"modality {RASI_MODALITY[target]} not {expected}"
        )


@pytest.mark.parametrize("sign", range(12))
def test_no_sign_aspects_itself(sign):
    assert sign not in rasi_drishti(sign)


@pytest.mark.parametrize("sign", range(12))
def test_aspects_are_mutual(sign):
    """Rasi drishti is a symmetric relation."""
    for target in rasi_drishti(sign):
        assert sign in rasi_drishti(target), (
            f"{RASI_NAMES[sign]} aspects {RASI_NAMES[target]} but not conversely"
        )


@pytest.mark.parametrize("sign", [0, 3, 6, 9])
def test_a_movable_sign_skips_the_fixed_sign_next_to_it(sign):
    """"the fixed rasis other than the one next to it"."""
    assert RASI_MODALITY[sign] == MOVABLE
    fixed = {s for s in range(12) if RASI_MODALITY[s] == FIXED}
    assert set(rasi_drishti(sign)) == fixed - {(sign + 1) % 12}


@pytest.mark.parametrize("sign", [1, 4, 7, 10])
def test_a_fixed_sign_skips_the_movable_sign_before_it(sign):
    assert RASI_MODALITY[sign] == FIXED
    movable = {s for s in range(12) if RASI_MODALITY[s] == MOVABLE}
    assert set(rasi_drishti(sign)) == movable - {(sign - 1) % 12}


@pytest.mark.parametrize("sign", [2, 5, 8, 11])
def test_a_dual_sign_aspects_the_other_three_duals(sign):
    assert RASI_MODALITY[sign] == DUAL
    dual = {s for s in range(12) if RASI_MODALITY[s] == DUAL}
    assert set(rasi_drishti(sign)) == dual - {sign}


def test_the_old_offsets_would_fail_these():
    """A regression guard naming the exact values that were wrong.

    If someone reinstates them, the failure says so rather than leaving a
    reader to rediscover why the table looks the way it does.
    """
    from hora.charts.aspects import _RASI_DRISHTI_OFFSETS

    assert _RASI_DRISHTI_OFFSETS != {0: (4, 6, 8), 1: (2, 4, 10), 2: (2, 6, 10)}
    assert _RASI_DRISHTI_OFFSETS == {0: (4, 7, 10), 1: (2, 5, 8), 2: (3, 6, 9)}
