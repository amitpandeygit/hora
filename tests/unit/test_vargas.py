"""Divisional chart rules, checked against the classical statements in BPHS."""
import pytest

from hora.charts.vargas import SHODASAVARGA, VARGA_REGISTRY, varga


@pytest.mark.parametrize(
    "longitude,expected_sign",
    [
        (0.0, 0),      # Aries 0 -> Aries (movable counts from itself)
        (30.0, 9),     # Taurus 0 -> Capricorn (fixed counts from the 9th)
        (60.0, 6),     # Gemini 0 -> Libra (dual counts from the 5th)
        (90.0, 3),     # Cancer 0 -> Cancer
        (120.0, 0),    # Leo 0 -> Aries
        (29.9999, 8),  # end of Aries -> Sagittarius, the ninth navamsa
    ],
)
def test_navamsa_matches_movable_fixed_dual_rule(longitude, expected_sign):
    assert varga(longitude, "D9").sign == expected_sign


@pytest.mark.parametrize(
    "longitude,expected_sign",
    [(0.0, 0), (15.0, 4), (25.0, 8)],  # 1st, 5th, 9th from Aries
)
def test_drekkana_steps_four_signs(longitude, expected_sign):
    assert varga(longitude, "D3").sign == expected_sign


def test_hora_parashari_splits_between_leo_and_cancer():
    assert varga(5.0, "D2").sign == 4     # odd sign, first half -> Leo
    assert varga(20.0, "D2").sign == 3    # odd sign, second half -> Cancer
    assert varga(35.0, "D2").sign == 3    # even sign, first half -> Cancer
    assert varga(50.0, "D2").sign == 4    # even sign, second half -> Leo


def test_trimsamsa_uses_unequal_spans():
    # Odd sign: Mars 0-5, Saturn 5-10, Jupiter 10-18, Mercury 18-25, Venus 25-30.
    assert varga(3.0, "D30").sign == 0     # Aries (Mars)
    assert varga(7.0, "D30").sign == 10    # Aquarius (Saturn)
    assert varga(14.0, "D30").sign == 8    # Sagittarius (Jupiter)
    assert varga(20.0, "D30").sign == 2    # Gemini (Mercury)
    assert varga(28.0, "D30").sign == 6    # Libra (Venus)
    # Even sign reverses the order, starting from Venus.
    assert varga(33.0, "D30").sign == 1    # Taurus (Venus)
    assert varga(59.0, "D30").sign == 7    # Scorpio (Mars)


def test_shashtyamsa_doubles_degrees():
    assert varga(1.0, "D60").sign == 2     # 1 deg -> 2 signs on from Aries
    assert varga(14.5, "D60").sign == 5


def test_dwadasamsa_counts_from_the_sign_itself():
    assert varga(0.0, "D12").sign == 0
    assert varga(2.6, "D12").sign == 1
    assert varga(29.0, "D12").sign == 11


@pytest.mark.parametrize("code", list(VARGA_REGISTRY))
def test_every_registered_varga_is_total_over_the_zodiac(code):
    """No longitude may produce an out-of-range sign or a gap."""
    for step in range(3600):
        pos = varga(step / 10.0, code)
        assert 0 <= pos.sign <= 11
        assert 0.0 <= pos.longitude < 360.0


def test_generic_varga_falls_back_to_cyclic_rule():
    assert varga(0.0, "D150").sign == 0
    assert varga(0.0, "D7").sign == varga(0.0, "D7", None).sign


def test_shodasavarga_is_sixteen_charts():
    assert len(SHODASAVARGA) == 16
    assert all(code in VARGA_REGISTRY for code in SHODASAVARGA)


def test_unknown_varga_raises():
    with pytest.raises(ValueError):
        varga(10.0, "X9")
