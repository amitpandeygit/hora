"""Chapter 29 — Tajaka yogas. §29.1, §29.2.1, §29.2.2, §29.2.3."""

import itertools
import random

import pytest

from hora.core.const import Graha
from hora.tajaka import yogas

# --------------------------------------------------------------------------
# §29.1 Introduction
# --------------------------------------------------------------------------


def test_the_introduction_is_transcribed():
    assert yogas.CHAPTER_TITLE == "Tajaka Yogas"
    assert "Tajaka annual/monthly charts" in yogas.INTRODUCTION
    assert "prasna charts (horary charts)" in yogas.INTRODUCTION


def test_prasna_is_named_here_and_taught_nowhere():
    """The only other mention in the book is §3.2.13's note on graha periods.
    """
    from hora.core.constants.graha import TIME_PERIOD_USE

    assert "prasna or horary astrology" in TIME_PERIOD_USE
    assert "never explains how a prasna chart is cast" in (
        yogas.PRASNA_IS_NAMED_BUT_NEVER_TAUGHT)


# --------------------------------------------------------------------------
# §29.2.1 Ishkavala and §29.2.2 Induvara
# --------------------------------------------------------------------------


def test_both_rules_are_transcribed_with_their_results():
    assert "apoklimas (3rd, 6th, 9th and 12th houses) are empty" in (
        yogas.ISHKAVALA_RULE)
    assert "wealth, happiness and good fortune" in yogas.ISHKAVALA_RULE
    assert "occupy only apoklimas" in yogas.INDUVARA_RULE
    assert "disappointments, worries and illnesses" in yogas.INDUVARA_RULE
    assert yogas.ISHKAVALA_RESULTS in yogas.ISHKAVALA_RULE
    assert yogas.INDUVARA_RESULTS in yogas.INDUVARA_RULE


def test_the_three_house_groups_match_chapter_7s():
    """§29.2 restates §7.4's groups house for house. If they had drifted the
    yogas would be reading a different chart from the rest of the book.
    """
    from hora.core.constants.house import APOKLIMA, KENDRA, PANAPHARA

    assert KENDRA == (1, 4, 7, 10)
    assert PANAPHARA == (2, 5, 8, 11)
    assert APOKLIMA == (3, 6, 9, 12)
    assert sorted(KENDRA + PANAPHARA + APOKLIMA) == list(range(1, 13))


def test_ishkavala_is_present_when_no_apoklima_is_occupied():
    assert yogas.ishkavala([1, 4, 7, 10])["present"] is True
    assert yogas.ishkavala([2, 5, 8, 11])["present"] is True
    assert yogas.ishkavala([1, 2, 4, 5, 7, 8, 10, 11])["present"] is True
    for spoiler in (3, 6, 9, 12):
        assert yogas.ishkavala([1, 4, spoiler])["present"] is False


def test_induvara_is_present_when_only_apoklimas_are_occupied():
    assert yogas.induvara([3, 6, 9, 12])["present"] is True
    assert yogas.induvara([3])["present"] is True
    for spoiler in (1, 2, 4, 5, 7, 8, 10, 11):
        assert yogas.induvara([3, 6, spoiler])["present"] is False


def test_an_empty_chart_gives_neither_yoga():
    """"If planets occupy only X" needs a planet to occupy something."""
    assert yogas.ishkavala([])["present"] is False
    assert yogas.induvara([])["present"] is False


def test_the_two_halves_of_each_rule_are_one_condition():
    """Over every non-empty subset of the twelve houses, "occupies only" and
    "the rest are empty" never disagree.
    """
    for size in range(1, 5):
        for houses in itertools.combinations(range(1, 13), size):
            ish = yogas.ishkavala(houses)
            assert (ish["occupies_only_kendras_and_panapharas"]
                    == ish["apoklimas_empty"])
            ind = yogas.induvara(houses)
            assert (ind["occupies_only_apoklimas"]
                    == ind["kendras_and_panapharas_empty"])
    assert "one condition" in yogas.THE_TWO_HALVES_OF_EACH_RULE_ARE_THE_SAME_TEST


def test_no_chart_has_both_yogas():
    for size in range(1, 6):
        for houses in itertools.combinations(range(1, 13), size):
            both = (yogas.ishkavala(houses)["present"]
                    and yogas.induvara(houses)["present"])
            assert not both
    assert "no chart has both" in (
        yogas.THE_TWO_YOGAS_ARE_OPPOSITE_ENDS_OF_ONE_TEST)


def test_house_groups_partitions_what_it_is_given():
    got = yogas.house_groups([1, 2, 3, 4, 3])
    assert got == {"kendra": (1, 4), "panaphara": (2,), "apoklima": (3,)}


def test_ishkavala_is_far_commoner_than_induvara_in_real_charts():
    """Eight houses against four. Measured, because the chapter presents the
    two as a matched pair and they are not one.
    """
    from hora.charts.chart import Place, compute_chart
    from hora.core.settings import NodeType, Settings
    from hora.core.timeutil import from_local

    random.seed(291)
    place = Place(name="x", latitude=19.0, longitude=73.0)
    settings = Settings(node_type=NodeType.MEAN)
    hits = {"ishkavala": 0, "induvara": 0}
    trials = 400
    for _ in range(trials):
        chart = compute_chart(
            from_local(random.randint(1900, 2050), random.randint(1, 12),
                       random.randint(1, 28), random.randint(0, 23),
                       random.randint(0, 59), 0.0, utc_offset_hours=5.5),
            place, settings)
        houses = [(int(chart.positions[g].longitude // 30) - chart.lagna_rasi)
                  % 12 + 1 for g in range(7)]
        hits["ishkavala"] += yogas.ishkavala(houses)["present"]
        hits["induvara"] += yogas.induvara(houses)["present"]

    # (2/3)^7 = 5.9% and (1/3)^7 = 0.046%: the house count is the whole story.
    assert 0.02 < hits["ishkavala"] / trials < 0.12
    assert hits["induvara"] <= 1
    assert "one chart in sixteen" in (
        yogas.ISHKAVALA_IS_ORDERS_OF_MAGNITUDE_COMMONER)


def test_which_bodies_count_is_left_open():
    """OI-159. The functions take houses, never a body list."""
    assert "without saying whether Rahu" in yogas.WHICH_BODIES_COUNT_IS_NOT_SAID


# --------------------------------------------------------------------------
# §29.2.3 Ithasala — footnote 83
# --------------------------------------------------------------------------


def test_the_ithasala_rule_and_its_results_are_transcribed():
    assert "less advanced in its rasi" in yogas.ITHASALA_RULE
    assert "applying aspect" in yogas.ITHASALA_RULE
    assert "naisargika karaka" in yogas.ITHASALA_RESULTS
    assert "lord of vivaha saham or Venus" in yogas.ITHASALA_RESULTS
    assert yogas.ITHASALA_REFERENCE_LORDS == (
        "lagna lord", "lord of the related house",
        "lord of the related saham", "the naisargika karaka")


def test_footnote_83s_order_is_transcribed_and_ranked():
    assert "Saturn, Rahu/Ketu, Jupiter, Mars, Sun, Venus, Mercury and Moon" in (
        yogas.SPEED_ORDER_FOOTNOTE)
    names = [tuple(str(Graha(g).name).title() for g in group)
             for group in yogas.SPEED_ORDER]
    assert names == [("Saturn",), ("Rahu", "Ketu"), ("Jupiter",), ("Mars",),
                     ("Sun",), ("Venus",), ("Mercury",), ("Moon",)]
    assert yogas.speed_rank(int(Graha.SATURN)) == 0
    assert yogas.speed_rank(int(Graha.MOON)) == 7
    assert yogas.speed_rank(int(Graha.RAHU)) == yogas.speed_rank(int(Graha.KETU))


def test_rahu_and_ketu_are_the_only_pair_the_footnote_cannot_rank():
    assert yogas.faster_of(int(Graha.RAHU), int(Graha.KETU)) is None
    assert len(yogas.pairs_in_speed_order()) == 35      # 36 pairs less that one
    for slower, faster in yogas.pairs_in_speed_order():
        assert yogas.speed_rank(slower) < yogas.speed_rank(faster)


def test_the_footnote_is_right_about_the_seven_and_wrong_about_the_nodes():
    """Mean daily motion, measured over thirty years of samples. D-81."""
    import statistics

    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings

    eph = get_ephemeris(Settings(node_type=NodeType.MEAN))
    ids = list(range(9))
    speeds: dict[int, list[float]] = {g: [] for g in ids}
    for step in range(0, 11000, 60):
        for graha, position in eph.positions(2447893.0 + step, ids).items():
            speeds[graha].append(abs(position.speed_longitude))
    mean = {g: statistics.fmean(v) * 60 for g, v in speeds.items()}

    seven = [int(Graha.SATURN), int(Graha.JUPITER), int(Graha.MARS),
             int(Graha.SUN), int(Graha.VENUS), int(Graha.MERCURY),
             int(Graha.MOON)]
    # The footnote's order for the seven classical grahas is exactly right.
    assert seven == sorted(seven, key=lambda g: mean[g])
    assert [yogas.speed_rank(g) for g in seven] == sorted(
        yogas.speed_rank(g) for g in seven)

    # And exactly wrong for the nodes, which it puts above Saturn.
    assert mean[int(Graha.RAHU)] < mean[int(Graha.SATURN)]
    assert yogas.speed_rank(int(Graha.RAHU)) > yogas.speed_rank(
        int(Graha.SATURN))
    assert "not the second slowest" in (
        yogas.THE_NODES_ARE_THE_ONE_PLACE_THE_ORDER_IS_WRONG)


def test_the_fixed_order_and_the_true_speeds_disagree_often():
    """OI-160. 22 of the 36 pairs invert at some point."""
    from hora.core.ephemeris import get_ephemeris
    from hora.core.settings import NodeType, Settings

    eph = get_ephemeris(Settings(node_type=NodeType.MEAN))
    ids = list(range(9))
    speeds: dict[int, list[float]] = {g: [] for g in ids}
    for step in range(0, 11000, 30):
        for graha, position in eph.positions(2447893.0 + step, ids).items():
            speeds[graha].append(abs(position.speed_longitude))
    samples = len(speeds[0])

    inverting = 0
    for slower, faster in yogas.pairs_in_speed_order():
        if any(speeds[slower][i] > speeds[faster][i] for i in range(samples)):
            inverting += 1
    # 35 rankable pairs; the Rahu-Ketu pair the footnote ties is not among
    # them and never inverts anyway.
    assert inverting == 22
    assert "22 of the 36 pairs invert" in (
        yogas.THE_SPEED_ORDER_IS_A_LIST_NOT_A_MEASUREMENT)


# --------------------------------------------------------------------------
# §29.2.3 Ithasala — the yoga itself
# --------------------------------------------------------------------------


def test_advancement_is_the_degree_within_the_rasi():
    assert yogas.advancement(180 + 13) == pytest.approx(13.0)
    assert yogas.advancement(29.5) == pytest.approx(29.5)
    assert yogas.advancement(30.0) == pytest.approx(0.0)
    assert "not a comparison of longitudes" in (
        yogas.ADVANCEMENT_IS_WITHIN_THE_RASI)


def test_advancement_and_longitude_disagree_across_a_sign_boundary():
    """2° of Taurus is less advanced than 25° of Aries and ahead of it."""
    early, late = 30.0 + 2.0, 25.0
    assert early > late
    assert yogas.advancement(early) < yogas.advancement(late)


def test_a_worked_ithasala():
    """Venus at 13 Li and Jupiter at 20 Ge: a trinal aspect, and Venus, the
    faster, is less advanced in his rasi. Applying.
    """
    got = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                         faster_longitude=180 + 13, slower_longitude=60 + 20)
    assert got["faster_name"] == "Venus" and got["slower_name"] == "Jupiter"
    assert got["house_from_faster"] == 9
    assert got["aspect"] == "Trinal aspect"
    assert got["faster_is_less_advanced"] is True
    assert got["present_by_house"] is True
    assert got["present_within_orb"] is True


def test_the_same_pair_separating_is_not_an_ithasala():
    """Venus at 25 Li, Jupiter at 20 Ge: the aspect is the same and Venus is
    now past it.
    """
    got = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                         faster_longitude=180 + 25, slower_longitude=60 + 20)
    assert got["aspects_by_house"] is True
    assert got["faster_is_less_advanced"] is False
    assert got["present_by_house"] is False


def test_the_caller_cannot_invert_the_yoga_by_swapping_the_arguments():
    """Footnote 83 decides which planet is the faster, not the caller."""
    right = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                           faster_longitude=5.0, slower_longitude=100.0)
    wrong = yogas.ithasala(faster=int(Graha.SATURN), slower=int(Graha.MOON),
                           faster_longitude=100.0, slower_longitude=5.0)
    assert right["caller_had_them_the_right_way_round"] is True
    assert wrong["caller_had_them_the_right_way_round"] is False
    for key in ("faster", "slower", "faster_advancement", "slower_advancement",
                "faster_is_less_advanced", "present_by_house"):
        assert right[key] == wrong[key]


def test_the_sixth_and_eighth_houses_carry_no_aspect_so_no_ithasala():
    """§28.2 gives them none, and §29.2.3 needs an aspect."""
    for house in (6, 8):
        got = yogas.ithasala(
            faster=int(Graha.MOON), slower=int(Graha.SATURN),
            faster_longitude=5.0, slower_longitude=(house - 1) * 30.0 + 20.0)
        assert got["house_from_faster"] == house
        assert got["aspect"] is None
        assert got["aspects_by_house"] is False
        assert got["present_by_house"] is False


def test_the_orb_and_the_advancement_are_the_same_number():
    """Whole-sign aspects, so the separation from exact is the difference of
    the two advancements. Checked over three thousand random pairs.
    """
    random.seed(29)
    for _ in range(3000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        assert got["separation_from_exact"] == pytest.approx(
            abs(got["slower_advancement"] - got["faster_advancement"]),
            abs=1e-9)
    assert "equals the difference between the two planets' degrees" in (
        yogas.THE_ORB_AND_THE_ADVANCEMENT_ARE_ONE_NUMBER)


def test_the_two_deeptamsas_are_both_answered_and_neither_is_summed():
    """Venus's orb is 7° and Jupiter's 9°, so a separation of 8° is inside
    one and outside the other. The example requires both, so the yoga is
    absent — but the caller is still shown each answer.
    """
    got = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                         faster_longitude=180 + 13, slower_longitude=60 + 21)
    assert got["separation_from_exact"] == pytest.approx(8.0)
    assert got["deeptamsa_of_faster"] == 7.0
    assert got["deeptamsa_of_slower"] == 9.0
    assert got["aspects_within_faster_deeptamsa"] is False
    assert got["aspects_within_slower_deeptamsa"] is True
    assert got["deeptamsas_agree"] is False
    assert got["present_within_orb"] is False
    assert "both must hold" in yogas.WHOSE_DEEPTAMSA_GOVERNS_IS_NOT_SAID


def test_an_ithasala_with_a_node_has_no_orb_to_be_tested_against():
    """Footnote 83 ranks the nodes; §28.2 gives them no deeptamsa."""
    got = yogas.ithasala(faster=int(Graha.RAHU), slower=int(Graha.SATURN),
                         faster_longitude=5.0, slower_longitude=100.0)
    assert got["aspects_by_house"] is True
    assert got["present_by_house"] is True
    assert got["aspects_within_faster_deeptamsa"] is None
    assert got["present_within_orb"] is None
    assert "no deeptamsa" in yogas.A_NODES_ITHASALA_CANNOT_BE_ORBED


def test_ithasala_rejects_a_pair_it_cannot_rank_or_a_graha_with_itself():
    with pytest.raises(yogas.TajakaYogaError, match="two different grahas"):
        yogas.ithasala(faster=int(Graha.SUN), slower=int(Graha.SUN),
                       faster_longitude=1.0, slower_longitude=2.0)
    with pytest.raises(yogas.TajakaYogaError, match="neither is the faster"):
        yogas.ithasala(faster=int(Graha.RAHU), slower=int(Graha.KETU),
                       faster_longitude=1.0, slower_longitude=2.0)


def test_the_marriage_example_is_the_third_rule_for_one_event():
    """§25.3, §28.8.2 and now §29.2.3 all read a marriage against vivaha
    saham, and no two of them agree.
    """
    from hora.tajaka.saham_use import NATAL_SAHAM_TRANSITS
    from hora.transits.gochara import SAHAM_TRANSIT_EXAMPLES

    assert any(row["saham"] == "vivaha" for row in SAHAM_TRANSIT_EXAMPLES)
    assert any("Vivaha" in row["sahams"] for row in NATAL_SAHAM_TRANSITS)
    assert yogas.ITHASALA_MARRIAGE_EXAMPLE["matter"] == "marriage"
    assert "the lord of vivaha saham" in (
        yogas.ITHASALA_MARRIAGE_EXAMPLE["other_side"])
    # This one reads the saham's lord, where the other two read the point.
    assert "with its lord" in yogas.A_THIRD_RULE_FOR_THE_SAME_MARRIAGE


# --------------------------------------------------------------------------
# §29.2.3's worked example
# --------------------------------------------------------------------------


def test_the_ithasala_example_reproduces_on_all_four_claims():
    """Moon 14 Le, Venus 19 Li. Sextile; both inside the other's orb;
    advancements 14 and 19; the Moon the faster. Ithasala.
    """
    want = yogas.ITHASALA_EXAMPLE
    got = yogas.ithasala(
        faster=int(Graha.MOON), slower=int(Graha.VENUS),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]))

    assert got["faster_name"] == want["faster"]
    assert got["slower_name"] == want["slower"]
    assert got["aspect"] == want["aspect"]
    assert got["faster_advancement"] == pytest.approx(
        want["faster_advancement"])
    assert got["slower_advancement"] == pytest.approx(
        want["slower_advancement"])
    assert got["aspects_within_faster_deeptamsa"] is True
    assert got["aspects_within_slower_deeptamsa"] is True
    assert got["faster_is_less_advanced"] is True
    assert got["present_within_orb"] is want["present"]
    assert "All four reproduce" not in yogas.ITHASALA_RULE
    assert "The yoga is present" in yogas.THE_EXAMPLE_CHECKS_OUT_ON_ALL_FOUR_CLAIMS


def test_the_examples_longitudes_are_where_the_book_puts_them():
    from hora.core.const import RASI_ABBR

    want = yogas.ITHASALA_EXAMPLE
    for key, printed in (("faster_longitude", "14 Le"),
                         ("slower_longitude", "19 Li")):
        value = float(want[key])
        degree, rasi = printed.split()
        assert int(value % 30) == int(degree)
        assert RASI_ABBR[int(value // 30)] == rasi


def test_the_example_settles_whose_deeptamsa_governs():
    """"Both the planets are within the deeptaamsa (orb) of the other."
    Both, so the smaller of the two governs. OI-161, narrowed.
    """
    assert yogas.ITHASALA_EXAMPLE["both_within_the_others_orb"] is True
    assert "both must hold and" in yogas.WHOSE_DEEPTAMSA_GOVERNS_IS_NOT_SAID
    assert "smaller of the two deeptamsas" in yogas.THE_SMALLER_DEEPTAMSA_GOVERNS

    # 8° apart: inside Jupiter's 9° and outside Venus's 7°, so not an
    # ithasala under the example's reading, whichever way it is put.
    from hora.tajaka.aspects import deeptamsa

    near = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.JUPITER),
                          faster_longitude=180 + 13, slower_longitude=60 + 21)
    assert near["separation_from_exact"] == pytest.approx(8.0)
    assert near["present_by_house"] is True
    assert near["present_within_orb"] is False
    assert min(deeptamsa(int(Graha.VENUS)),
               deeptamsa(int(Graha.JUPITER))) == 7.0


def test_the_example_settles_that_the_orb_is_required():
    """The rule says only "have an aspect". The example checks the orb before
    declaring the yoga.
    """
    assert "so it is required" in (
        yogas.WHETHER_THE_ASPECT_NEEDS_THE_ORB_IS_NOT_SAID)
    # And the two readings do come apart: a wide separation aspects by house
    # and fails the orb.
    wide = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                          faster_longitude=1.0, slower_longitude=60 + 25.0)
    assert wide["aspects_by_house"] is True
    assert wide["faster_is_less_advanced"] is True
    assert wide["present_by_house"] is True
    assert wide["present_within_orb"] is False


def test_only_the_node_hole_is_left_in_the_orb_rule():
    """Two of OI-161's three holes are closed by the example. §28.2 still
    gives Rahu and Ketu no deeptamsa.
    """
    got = yogas.ithasala(faster=int(Graha.RAHU), slower=int(Graha.SATURN),
                         faster_longitude=5.0, slower_longitude=100.0)
    assert got["present_by_house"] is True
    assert got["present_within_orb"] is None
    assert got["deeptamsa_of_faster"] is None
    assert got["undecided"] == yogas.A_NODES_ITHASALA_CANNOT_BE_ORBED


# --------------------------------------------------------------------------
# §29.2.3 — the three types of ithasala
# --------------------------------------------------------------------------


def test_the_three_types_are_transcribed_with_their_meanings():
    names = [row["name"] for row in yogas.ITHASALA_TYPES]
    assert names == ["Vartamaana", "Poorna", "Bhavishya"]
    means = [row["means"] for row in yogas.ITHASALA_TYPES]
    assert means == ["present (current)", "complete", "future"]
    assert "within the deeptaamsa (orb) of the other" in (
        yogas.ITHASALA_TYPES[0]["rule"])
    assert "within 1 degree of each other" in yogas.ITHASALA_TYPES[1]["rule"]
    assert "speedy fulfillment" in yogas.ITHASALA_TYPES[1]["gives"]
    assert "is about to be formed" in yogas.ITHASALA_TYPES[2]["rule"]
    assert "obstructions or delay" in yogas.ITHASALA_TYPES[2]["gives"]
    assert yogas.POORNA_DEGREES == yogas.BHAVISHYA_DEGREES == 1.0


def test_the_three_worked_cases_reproduce():
    """One pair, three separations, three types. Every number the book prints
    comes back, including the 0°45' it computes by hand for bhavishya.
    """
    for want in yogas.ITHASALA_TYPE_EXAMPLES:
        got = yogas.ithasala(
            faster=int(Graha.MOON), slower=int(Graha.VENUS),
            faster_longitude=float(want["moon_longitude"]),
            slower_longitude=float(want["venus_longitude"]))
        assert got["type"] == want["type"], want["type"]
        assert got["separation_from_exact"] == pytest.approx(
            float(want["separation"]), abs=1e-9), want["type"]
        if "degrees_to_vartamaana" in want:
            assert got["degrees_to_vartamaana"] == pytest.approx(
                float(want["degrees_to_vartamaana"]), abs=1e-9)
    assert "three types" in yogas.THE_THREE_TYPE_EXAMPLES_REPRODUCE


def test_the_deeptamsa_windows_the_book_prints_come_back():
    """Venus at 19° gives 12° to 26°; the Moon at 13°35' gives 1°35' to
    25°35'; Venus at 21°20' gives 14°20' to 28°20'.
    """
    from hora.tajaka.aspects import aspect_span

    venus_at_19 = aspect_span(int(Graha.VENUS), 180.0 + 19.0, 11)
    assert venus_at_19["from"] % 30 == pytest.approx(12.0)
    assert venus_at_19["to"] % 30 == pytest.approx(26.0)

    moon_at_13_35 = aspect_span(int(Graha.MOON), 120.0 + 13.0 + 35 / 60, 3)
    assert moon_at_13_35["from"] % 30 == pytest.approx(1 + 35 / 60)
    assert moon_at_13_35["to"] % 30 == pytest.approx(25 + 35 / 60)

    venus_at_21_20 = aspect_span(int(Graha.VENUS), 180.0 + 21.0 + 20 / 60, 11)
    assert venus_at_21_20["from"] % 30 == pytest.approx(14 + 20 / 60)
    assert venus_at_21_20["to"] % 30 == pytest.approx(28 + 20 / 60)


def test_vartamaana_is_the_orb_test_already_built():
    """(i) restates §29.2.3's own rule, so the two must agree in every chart.
    """
    random.seed(2923)
    for _ in range(2000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        assert got["vartamaana"] == got["present_within_orb"]


def test_every_poorna_is_also_a_vartamaana():
    """1° against a smallest deeptamsa of 7°, so poorna nests inside."""
    from hora.tajaka.aspects import DEEPTAMSA

    assert min(DEEPTAMSA.values()) > yogas.POORNA_DEGREES

    random.seed(2924)
    poornas = 0
    for _ in range(4000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if got["poorna"]:
            poornas += 1
            assert got["vartamaana"] is True
            assert got["type"] == "Poorna"
    assert poornas > 20
    assert "every poorna ithasala is also a" in (
        yogas.POORNA_IS_A_KIND_OF_VARTAMAANA)


def test_bhavishya_excludes_the_other_two():
    random.seed(2925)
    for _ in range(4000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if got["bhavishya"]:
            assert got["vartamaana"] is False and got["poorna"] is False
            assert got["type"] == "Bhavishya"
            assert 0 < got["degrees_to_vartamaana"] <= 1.0


def test_all_three_types_are_one_subtraction():
    """The separation against the smaller deeptamsa decides everything."""
    random.seed(2926)
    for _ in range(3000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if not got["aspects_by_house"] or not got["faster_is_less_advanced"]:
            assert got["type"] is None
            continue
        gap, orb = got["separation_from_exact"], got["binding_deeptamsa"]
        assert got["vartamaana"] == (gap <= orb)
        assert got["poorna"] == (gap <= 1.0)
        assert got["bhavishya"] == (orb < gap <= orb + 1.0)
    assert "smaller deeptamsa" in yogas.ALL_THREE_TYPES_READ_ONE_SEPARATION


def test_the_binding_orb_is_the_smaller_of_the_two():
    got = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                         faster_longitude=134.0, slower_longitude=199.0)
    assert got["deeptamsa_of_faster"] == 12.0
    assert got["deeptamsa_of_slower"] == 7.0
    assert got["binding_deeptamsa"] == 7.0


def test_a_separating_pair_has_no_type_at_all():
    """None of the three survives the faster planet being ahead."""
    got = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                         faster_longitude=120.0 + 25.0, slower_longitude=199.0)
    assert got["faster_is_less_advanced"] is False
    assert got["type"] is None
    assert (got["vartamaana"], got["poorna"], got["bhavishya"]) == (
        False, False, False)


def test_a_bhavishya_can_never_reach_the_end_of_a_rasi():
    """The obvious worry — the faster planet changing sign as it advances,
    taking the whole-sign aspect with it — cannot arise. A bhavishya needs a
    separation above the binding orb, so the faster planet is below 23° of
    its rasi and a further degree leaves it below 24°.
    """
    from hora.tajaka.aspects import DEEPTAMSA

    smallest = min(DEEPTAMSA.values())
    assert smallest == 7.0

    random.seed(2927)
    seen = 0
    for _ in range(6000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        if got["degrees_to_vartamaana"] is not None:
            assert got["bhavishya_crosses_a_rasi"] is False
        if got["bhavishya"]:
            seen += 1
            assert got["faster_advancement"] < 30.0 - smallest
    assert seen > 20
    assert "cannot take it out of the sign" in (
        yogas.BHAVISHYA_CANNOT_REACH_THE_END_OF_A_RASI)


def test_the_bhavishya_example_swaps_two_rasi_names():
    """Venus is put in Le where the arithmetic needs Li, and his window in Li
    where it needs Le. Both are checkable from the numbers.
    """
    from hora.tajaka.aspects import aspect_on_house

    # If Venus were in Le with the Moon the aspect would be a conjunction,
    # not the sextile the paragraph names.
    assert aspect_on_house(1)["name"] == "Conjunction"
    assert aspect_on_house(3)["name"] == "Sextile aspect"

    bhavishya = yogas.ITHASALA_TYPE_EXAMPLES[2]
    assert bhavishya["venus"] == "21 Li 20"
    assert int(float(bhavishya["venus_longitude"]) // 30) == 6      # Libra
    assert int(float(bhavishya["moon_longitude"]) // 30) == 4       # Leo
    assert "Le for Li, then Li for Le" not in yogas.ITHASALA_RULE
    assert "the two rasi names are exchanged" in (
        yogas.THE_BHAVISHYA_EXAMPLE_SWAPS_TWO_RASI_NAMES)
