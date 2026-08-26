"""Dasha arithmetic."""
from itertools import pairwise

import pytest

from hora.core.const import Graha
from hora.core.settings import DashaYearLength
from hora.dasha.base import (
    balance_at_birth,
    compute_nakshatra_dasha,
    find_running,
    year_days,
)
from hora.dasha.nakshatra.systems import NAKSHATRA_DASHA_SYSTEMS, VIMSHOTTARI


def test_vimshottari_totals_120_years():
    assert VIMSHOTTARI.total_years == 120


def test_balance_at_start_of_nakshatra_is_the_full_period():
    lord, years = balance_at_birth(VIMSHOTTARI, 0.0)   # Ashwini 0 -> Ketu
    assert lord == Graha.KETU
    assert years == pytest.approx(7.0)


def test_balance_at_end_of_nakshatra_is_nearly_zero():
    _, years = balance_at_birth(VIMSHOTTARI, 13.3333330)
    assert years == pytest.approx(0.0, abs=1e-5)


def test_reference_chart_starts_in_saturn_dasha(pvr_chart):
    moon = pvr_chart.positions[Graha.MOON].longitude
    lord, years = balance_at_birth(VIMSHOTTARI, moon)
    assert lord == Graha.SATURN          # Pushya is ruled by Saturn
    assert 17.9 < years < 18.0


def test_mahadasha_sequence_is_contiguous_and_correctly_scaled(pvr_chart):
    periods = compute_nakshatra_dasha(
        VIMSHOTTARI, pvr_chart.positions[Graha.MOON].longitude,
        pvr_chart.instant.jd_ut, DashaYearLength.SIDEREAL, levels=1,
    )
    assert len(periods) == 9
    for a, b in pairwise(periods):
        assert a.end_jd == pytest.approx(b.start_jd)
    total = periods[-1].end_jd - periods[0].start_jd
    assert total == pytest.approx(120 * year_days(DashaYearLength.SIDEREAL), rel=1e-12)


def test_antardashas_fill_their_mahadasha_exactly(pvr_chart):
    periods = compute_nakshatra_dasha(
        VIMSHOTTARI, pvr_chart.positions[Graha.MOON].longitude,
        pvr_chart.instant.jd_ut, DashaYearLength.SIDEREAL, levels=2,
    )
    for md in periods:
        assert len(md.children) == 9
        assert md.children[0].start_jd == pytest.approx(md.start_jd)
        assert md.children[-1].end_jd == pytest.approx(md.end_jd)
        # The first antardasha of a mahadasha is always its own lord.
        assert md.children[0].lord == md.lord


def test_running_chain_at_birth_has_one_period_per_level(pvr_chart):
    periods = compute_nakshatra_dasha(
        VIMSHOTTARI, pvr_chart.positions[Graha.MOON].longitude,
        pvr_chart.instant.jd_ut, DashaYearLength.SIDEREAL, levels=3,
    )
    chain = find_running(periods, pvr_chart.instant.jd_ut)
    assert [p.level for p in chain] == [1, 2, 3]


@pytest.mark.parametrize("key", list(NAKSHATRA_DASHA_SYSTEMS))
def test_every_system_produces_a_contiguous_cycle(key, pvr_chart):
    spec = NAKSHATRA_DASHA_SYSTEMS[key]
    periods = compute_nakshatra_dasha(
        spec, pvr_chart.positions[Graha.MOON].longitude,
        pvr_chart.instant.jd_ut, DashaYearLength.SIDEREAL, levels=1,
    )
    assert len(periods) == len(spec.order)
    for a, b in pairwise(periods):
        assert a.end_jd == pytest.approx(b.start_jd)
