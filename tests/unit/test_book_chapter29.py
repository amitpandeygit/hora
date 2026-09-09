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


# --------------------------------------------------------------------------
# §29.2.3's Special Notes — retrogression
# --------------------------------------------------------------------------

_RASI = {"Ar": 0, "Ta": 1, "Ge": 2, "Cn": 3, "Le": 4, "Vi": 5,
         "Li": 6, "Sc": 7, "Sg": 8, "Cp": 9, "Aq": 10, "Pi": 11}
_GRAHA = {"Sun": Graha.SUN, "Moon": Graha.MOON, "Mars": Graha.MARS,
          "Mercury": Graha.MERCURY, "Jupiter": Graha.JUPITER,
          "Venus": Graha.VENUS, "Saturn": Graha.SATURN}


def _longitude(printed: str) -> float:
    """"18 Li 10" -> 198.1666..."""
    parts = printed.split()
    minutes = float(parts[2]) / 60.0 if len(parts) > 2 else 0.0
    return _RASI[parts[1]] * 30.0 + float(parts[0]) + minutes


def test_the_special_notes_restate_the_criterion():
    assert "reach the same advancement in their rasis" in yogas.THE_REAL_CRITERION
    assert "sookshma drishti" in yogas.THE_REAL_CRITERION
    assert yogas.SOOKSHMA_DRISHTI == "sookshma drishti"
    assert "retrograde or about to become retrograde" in (
        yogas.ADAPT_THE_RULES_UNDER_RETROGRESSION)


def test_all_four_retrogression_cases_give_the_books_verdict():
    for case in yogas.RETROGRESSION_CASES:
        got = yogas.ithasala(
            faster=int(_GRAHA[str(case["faster"])]),
            slower=int(_GRAHA[str(case["slower"])]),
            faster_longitude=_longitude(str(case["faster_at"])),
            slower_longitude=_longitude(str(case["slower_at"])),
            faster_retrograde=bool(case["faster_retrograde"]),
            slower_retrograde=bool(case["slower_retrograde"]),
            faster_stations_at=case.get("stations_at"))
        assert got["approaching"] is case["has_ithasala"], case["case"]
        assert (got["type"] is not None) is case["has_ithasala"], case["case"]


def test_the_three_named_aspects_in_the_special_notes_are_right():
    """The section names a trinal aspect three times and it is one each
    time: Ge to Li, Vi to Cp, and Vi to Cp again.
    """
    for faster_at, slower_at in (("18 Ge", "18 Li 10"),
                                 ("23 Vi", "21 Cp"),
                                 ("18 Vi", "18 Cp 45")):
        got = yogas.ithasala(
            faster=int(Graha.MERCURY), slower=int(Graha.MARS),
            faster_longitude=_longitude(faster_at),
            slower_longitude=_longitude(slower_at))
        assert got["aspect"] == "Trinal aspect", (faster_at, slower_at)


def test_a_retrograde_faster_planet_behind_is_not_an_ithasala():
    """The section's sharpest case: 10 arcminutes apart in a trinal aspect,
    which reads as a textbook poorna and is failure.
    """
    direct = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                            faster_longitude=_longitude("18 Ge"),
                            slower_longitude=_longitude("18 Li 10"))
    assert direct["type"] == "Poorna"
    assert direct["separation_from_exact"] == pytest.approx(10 / 60)

    retro = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                           faster_longitude=_longitude("18 Ge"),
                           slower_longitude=_longitude("18 Li 10"),
                           faster_retrograde=True)
    assert retro["faster_is_less_advanced"] is True
    assert retro["converging"] is False
    assert retro["type"] is None
    assert (retro["vartamaana"], retro["poorna"], retro["bhavishya"]) == (
        False, False, False)
    assert "dogged with failure" in str(yogas.RETROGRESSION_CASES[0]["book_says"])
    assert "the more convincing the false reading" in (
        yogas.A_TIGHT_DIFFERENCE_CAN_BE_THE_WORST_CASE)


def test_a_retrograde_faster_planet_ahead_is_an_ithasala():
    """Mars 21 Cp, retrograde Mercury 23 Vi. The faster planet is more
    advanced and they still converge, near 22°.
    """
    got = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                         faster_longitude=_longitude("23 Vi"),
                         slower_longitude=_longitude("21 Cp"),
                         faster_retrograde=True)
    assert got["faster_is_less_advanced"] is False
    assert got["converging"] is True
    assert got["type"] == "Vartamaana"
    assert got["separation_from_exact"] == pytest.approx(2.0)


def test_a_retrograde_slower_planet_changes_nothing_but_the_speed():
    """Moon 18 Ar, retrograde Mercury 24 Ge. The verdict is the same either
    way; the section's point is that it happens sooner.
    """
    kwargs = {"faster": int(Graha.MOON), "slower": int(Graha.MERCURY),
              "faster_longitude": _longitude("18 Ar"),
              "slower_longitude": _longitude("24 Ge")}
    retro = yogas.ithasala(**kwargs, slower_retrograde=True)
    direct = yogas.ithasala(**kwargs)
    assert retro["converging"] is direct["converging"] is True
    assert retro["type"] == direct["type"] == "Vartamaana"
    assert retro["slower_retrograde"] is True
    assert "faster realization" in str(yogas.RETROGRESSION_CASES[1]["book_says"])


def test_only_the_faster_planets_direction_decides_convergence():
    """The whole retrogression rule in one clause, over every combination."""
    for faster_behind in (True, False):
        for faster_retro in (True, False):
            for slower_retro in (True, False):
                # 10° apart either way, in a sextile.
                faster_at = 4.0 if faster_behind else 14.0
                slower_at = 74.0 if faster_behind else 64.0
                got = yogas.ithasala(
                    faster=int(Graha.MOON), slower=int(Graha.SATURN),
                    faster_longitude=faster_at, slower_longitude=slower_at,
                    faster_retrograde=faster_retro,
                    slower_retrograde=slower_retro)
                assert got["faster_is_less_advanced"] is faster_behind
                assert got["converging"] is (faster_behind != faster_retro)
    assert "The slower planet's direction changes only how soon" in (
        yogas.ONLY_THE_FASTER_PLANETS_DIRECTION_DECIDES)


def test_both_retrograde_is_answered_by_the_same_clause():
    """The section never works it. The argument extends unchanged."""
    behind = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                            faster_longitude=4.0, slower_longitude=74.0,
                            faster_retrograde=True, slower_retrograde=True)
    ahead = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                           faster_longitude=14.0, slower_longitude=64.0,
                           faster_retrograde=True, slower_retrograde=True)
    assert behind["converging"] is False
    assert ahead["converging"] is True
    assert "never both at once" in yogas.BOTH_RETROGRADE_IS_NOT_WORKED


def test_a_planet_that_stations_first_never_reaches_the_meeting():
    """Mercury 18 Vi, Mars 18°45' Cp, neither retrograde: a poorna on the
    numbers. Mercury turns back at 18°05'.
    """
    kwargs = {"faster": int(Graha.MERCURY), "slower": int(Graha.MARS),
              "faster_longitude": _longitude("18 Vi"),
              "slower_longitude": _longitude("18 Cp 45")}
    unaware = yogas.ithasala(**kwargs)
    assert unaware["type"] == "Poorna"
    assert unaware["separation_from_exact"] == pytest.approx(45 / 60)

    aware = yogas.ithasala(**kwargs, faster_stations_at=18.0 + 5.0 / 60.0)
    assert aware["converging"] is True
    assert aware["stationed_before_the_meeting"] is True
    assert aware["approaching"] is False
    assert aware["type"] is None

    # A station beyond the slower planet does not block anything.
    later = yogas.ithasala(**kwargs, faster_stations_at=25.0)
    assert later["stationed_before_the_meeting"] is False
    assert later["type"] == "Poorna"


def test_the_station_test_works_backwards_for_a_retrograde_faster_planet():
    kwargs = {"faster": int(Graha.MERCURY), "slower": int(Graha.MARS),
              "faster_longitude": _longitude("23 Vi"),
              "slower_longitude": _longitude("21 Cp"),
              "faster_retrograde": True}
    blocked = yogas.ithasala(**kwargs, faster_stations_at=22.0)
    assert blocked["stationed_before_the_meeting"] is True
    assert blocked["type"] is None
    clear = yogas.ithasala(**kwargs, faster_stations_at=15.0)
    assert clear["stationed_before_the_meeting"] is False
    assert clear["type"] == "Vartamaana"


def test_a_station_outside_a_rasi_is_rejected():
    for bad in (-1.0, 30.0, 45.0):
        with pytest.raises(yogas.TajakaYogaError, match="advancement in a rasi"):
            yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                           faster_longitude=4.0, slower_longitude=64.0,
                           faster_stations_at=bad)


def test_the_defaults_leave_the_earlier_rule_untouched():
    """Both flags default to direct, so everything built before the Special
    Notes answers exactly as it did.
    """
    random.seed(2928)
    for _ in range(2000):
        a, b = random.sample(range(7), 2)
        got = yogas.ithasala(faster=a, slower=b,
                             faster_longitude=random.uniform(0, 360),
                             slower_longitude=random.uniform(0, 360))
        assert got["faster_retrograde"] is False
        assert got["slower_retrograde"] is False
        assert got["converging"] is got["faster_is_less_advanced"]
        assert got["approaching"] is got["faster_is_less_advanced"]


def test_the_narrower_window_under_retrogression_has_no_figure():
    """OI-162. The thresholds are left at one degree and the flag says so."""
    got = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                         faster_longitude=_longitude("23 Vi"),
                         slower_longitude=_longitude("21 Cp"),
                         faster_retrograde=True)
    assert got["retrogression_narrows_the_window"] is not None
    assert "gives no figure" in yogas.RETROGRESSION_NARROWS_THE_WINDOW
    assert yogas.POORNA_DEGREES == 1.0

    direct = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                            faster_longitude=_longitude("23 Vi"),
                            slower_longitude=_longitude("21 Cp"))
    assert direct["retrogression_narrows_the_window"] is None


# --------------------------------------------------------------------------
# §29.2.4 Eesarpha yoga
# --------------------------------------------------------------------------


def test_the_eesarpha_rule_and_results_are_transcribed():
    assert "opposite of ithasala" in yogas.EESARPHA_RULE
    assert "higher advancement in its rasi" in yogas.EESARPHA_RULE
    assert "failures and disappointments" in yogas.EESARPHA_RESULTS
    assert "president or prime minister or king" in yogas.EESARPHA_RESULTS
    assert "We have an ithasala yoga instead" in yogas.EESARPHA_SPECIAL_NOTES


def test_the_two_readings_are_data():
    matters = [row["matter"] for row in yogas.EESARPHA_READINGS]
    assert matters == ["children", "loss of power"]
    assert yogas.EESARPHA_READINGS[0]["other_side"] == (
        "the 5th lord", "the putra saham lord", "Jupiter")
    assert yogas.EESARPHA_READINGS[1]["only_for"] == (
        "a president or prime minister or king")
    for row in yogas.EESARPHA_READINGS:
        assert row["one_side"] == "lagna lord"
        assert str(row["shows"]) in yogas.EESARPHA_RESULTS


def test_both_sahams_the_results_name_are_in_table_74():
    """Putra saham and raajya saham — 13 and 11."""
    from hora.tajaka.sahams import TABLE_74_SAHAMS

    numbers = {str(row["name"]): row["number"] for row in TABLE_74_SAHAMS}
    assert numbers["Putra"] == 13
    assert numbers["Rajya"] == 11


def test_the_fifth_lord_appears_in_both_readings():
    first, second = yogas.EESARPHA_READINGS
    assert "the 5th lord" in first["other_side"]
    assert "the 5th lord" in second["other_side"]
    shared = set(first["other_side"]) & set(second["other_side"])
    assert shared == {"the 5th lord"}
    assert "the only reference in either list to appear twice" in (
        yogas.THE_FIFTH_LORD_IS_IN_BOTH_READINGS)


def test_the_eesarpha_example_reproduces():
    """Moon 23 Le, Venus 19 Li: a sextile, both inside the other's orb, and
    the Moon the more advanced.
    """
    want = yogas.EESARPHA_EXAMPLE
    got = yogas.eesarpha(
        faster=int(Graha.MOON), slower=int(Graha.VENUS),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]))
    assert got["aspect"] == want["aspect"]
    assert got["faster_advancement"] == pytest.approx(
        float(want["faster_advancement"]))
    assert got["slower_advancement"] == pytest.approx(
        float(want["slower_advancement"]))
    assert got["faster_is_more_advanced"] is True
    assert got["separation_from_exact"] == pytest.approx(4.0)
    assert got["present_within_orb"] is want["present"]
    assert got["ithasala_instead"] is None


def test_the_example_is_29_2_3s_example_with_the_moon_moved_on():
    """Same pair, same aspect, same orbs — the Moon at 23° instead of 14°."""
    ith = yogas.ITHASALA_EXAMPLE
    ees = yogas.EESARPHA_EXAMPLE
    assert ees["slower_longitude"] == ith["slower_longitude"]
    assert ees["aspect"] == ith["aspect"]
    assert float(ees["faster_longitude"]) - float(ith["faster_longitude"]) == 9.0


def test_all_four_special_note_cases_come_out_right():
    """Retrograde and less advanced is eesarpha; retrograde and more advanced
    is ithasala instead. Both directions of both flags.
    """
    cases = ((True, True, "eesarpha"), (True, False, "ithasala"),
             (False, False, "eesarpha"), (False, True, "ithasala"))
    for retrograde, behind, want in cases:
        faster_at = 4.0 if behind else 9.0
        slower_at = 69.0 if behind else 64.0       # 5° apart, inside both orbs
        got = yogas.eesarpha(
            faster=int(Graha.MOON), slower=int(Graha.SATURN),
            faster_longitude=faster_at, slower_longitude=slower_at,
            faster_retrograde=retrograde)
        other = yogas.ithasala(
            faster=int(Graha.MOON), slower=int(Graha.SATURN),
            faster_longitude=faster_at, slower_longitude=slower_at,
            faster_retrograde=retrograde)
        if want == "eesarpha":
            assert got["present_within_orb"] is True, (retrograde, behind)
            assert other["type"] is None, (retrograde, behind)
        else:
            assert got["present_within_orb"] is False, (retrograde, behind)
            assert other["type"] is not None, (retrograde, behind)
            assert got["ithasala_instead"] == other["type"]


def test_eesarpha_is_the_negation_of_ithasalas_clause():
    """Over random pairs: given an aspect and unequal advancements, exactly
    one of the two yogas holds by house, whatever the flags.
    """
    random.seed(2941)
    both = neither = 0
    for _ in range(4000):
        a, b = random.sample(range(7), 2)
        kwargs = {"faster": a, "slower": b,
                  "faster_longitude": random.uniform(0, 360),
                  "slower_longitude": random.uniform(0, 360),
                  "faster_retrograde": random.random() < 0.3,
                  "slower_retrograde": random.random() < 0.3}
        ith = yogas.ithasala(**kwargs)
        ees = yogas.eesarpha(**kwargs)
        if not ith["aspects_by_house"]:
            assert not ith["present_by_house"] and not ees["present_by_house"]
            continue
        both += ith["present_by_house"] and ees["present_by_house"]
        neither += not (ith["present_by_house"] or ees["present_by_house"])
    assert both == 0
    assert neither == 0          # equal advancements never come up at random
    assert "negation of ithasala's condition" in (
        yogas.EESARPHA_IS_THE_NEGATION_OF_THE_SAME_CLAUSE)


def test_the_exact_aspect_is_neither_yoga():
    """Equal advancements: the faster planet is neither less nor more
    advanced, so no definition reaches it — and that is the sookshma drishti
    an ithasala is heading towards. OI-163.
    """
    ith = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                         faster_longitude=10.0, slower_longitude=70.0)
    ees = yogas.eesarpha(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                         faster_longitude=10.0, slower_longitude=70.0)
    assert ith["aspects_by_house"] is True
    assert ith["separation_from_exact"] == pytest.approx(0.0)
    assert ith["type"] is None
    assert ees["advancements_are_equal"] is True
    assert ees["present_by_house"] is False
    assert ees["present_within_orb"] is False
    assert "neither ithasala nor eesarpha" in yogas.THE_EXACT_ASPECT_IS_NEITHER_YOGA
    assert yogas.SOOKSHMA_DRISHTI in yogas.THE_EXACT_ASPECT_IS_NEITHER_YOGA


def test_eesarpha_needs_the_orb_the_same_way_ithasala_does():
    """The example checks it in the same words, so the same reading holds:
    both planets inside the other's deeptamsa.
    """
    assert yogas.EESARPHA_EXAMPLE["both_within_the_others_orb"] is True
    wide = yogas.eesarpha(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                          faster_longitude=25.0, slower_longitude=60.0 + 1.0)
    assert wide["faster_is_more_advanced"] is True
    assert wide["present_by_house"] is True
    assert wide["present_within_orb"] is False
    assert wide["separation_from_exact"] > wide["binding_deeptamsa"]


def test_an_eesarpha_with_a_node_leaves_the_orb_undecided():
    got = yogas.eesarpha(faster=int(Graha.RAHU), slower=int(Graha.SATURN),
                         faster_longitude=100.0, slower_longitude=5.0)
    assert got["present_by_house"] is True
    assert got["present_within_orb"] is None
    assert got["undecided"] == yogas.A_NODES_ITHASALA_CANNOT_BE_ORBED


def test_the_section_spells_its_own_yoga_three_ways():
    assert "Easarpha yoga is the opposite" in yogas.EESARPHA_RULE
    assert "eesarpha yoga" in yogas.EESARPHA_RULE
    assert "eesaarpha yoga" in yogas.EESARPHA_SPECIAL_NOTES
    assert "the Special Notes eesaarpha" in (
        yogas.THE_SECTION_SPELLS_ITS_OWN_YOGA_THREE_WAYS)


def test_the_station_case_is_named_here_and_not_worked():
    """The Special Notes point back at "about to become retrograde" and then
    work only the two retrograde cases.
    """
    assert "about to become retrograde" in yogas.EESARPHA_SPECIAL_NOTES
    assert "station" not in yogas.EESARPHA_SPECIAL_NOTES
    assert "no window is given" in (
        yogas.THE_STATION_CASE_IS_NAMED_BUT_NOT_WORKED_HERE)


# --------------------------------------------------------------------------
# §29.2.5 Nakta yoga
# --------------------------------------------------------------------------


def test_the_nakta_rule_is_transcribed_with_its_slip_intact():
    assert "no ithasala yoga or eesarpha yoga" in yogas.NAKTA_RULE
    assert "moves faster than both the planets" in yogas.NAKTA_RULE
    assert "forms ithasala yoga with both" in yogas.NAKTA_RULE
    # "shows by the 3rd planet" for "shown by", kept as printed.
    assert "someone shows by the 3rd planet" in yogas.NAKTA_RULE


def test_the_nakta_example_reproduces():
    """Venus 13 Ge, Mars 15 Sc, Moon 11 Cn. The Moon aspects both, is behind
    both, and is faster than both.
    """
    want = yogas.NAKTA_EXAMPLE
    got = yogas.nakta(
        first=int(Graha.VENUS), second=int(Graha.MARS),
        connector=int(Graha.MOON),
        first_longitude=float(want["first_longitude"]),
        second_longitude=float(want["second_longitude"]),
        connector_longitude=float(want["connector_longitude"]))
    assert got["first_pair_aspect"] is want["first_pair_aspect"]
    assert got["connector_aspects"] == (want["connector_to_first"],
                                        want["connector_to_second"])
    assert got["connector_is_faster_than_both"] is True
    assert got["connector_ithasala_types"] == ("Vartamaana", "Vartamaana")
    assert got["connector_carries"] is True
    assert got["present_as_worked"] is True


def test_the_examples_two_planets_have_no_aspect_at_all():
    """Ge to Sc is the 6th, which §28.2 leaves aspectless. The example says
    so and the rule says the opposite.
    """
    from hora.tajaka.aspects import aspect_on_house

    assert aspect_on_house(6) is None
    got = yogas.nakta(first=int(Graha.VENUS), second=int(Graha.MARS),
                      connector=int(Graha.MOON), first_longitude=73.0,
                      second_longitude=225.0, connector_longitude=101.0)
    assert got["first_pair_aspect"] is None
    assert got["first_pair_qualifies_as_worked"] is True
    assert got["first_pair_qualifies_as_worded"] is False
    assert got["readings_agree"] is False
    assert got["undecided"] is not None
    assert "have no aspect at all" in (
        yogas.THE_RULE_AND_ITS_EXAMPLE_DISAGREE_ON_THE_FIRST_PAIR)


def test_the_examples_lordships_and_placements_all_hold():
    """Venus lagna lord in the 2nd, Mars 7th lord in the 7th, Moon owning the
    3rd — from a Taurus lagna, every one of them.
    """
    from hora.core.const import RASI_LORD

    rasi = {"Ta": 1, "Ge": 2, "Cn": 3, "Sc": 7}
    lagna = rasi["Ta"]
    sits = {"Venus": rasi["Ge"], "Mars": rasi["Sc"], "Moon": rasi["Cn"]}
    for row in yogas.NAKTA_EXAMPLE["lordships"]:
        name = str(row["graha"])
        owned = (lagna + int(row["owns"]) - 1) % 12
        assert str(_GRAHA[name].name).title() == str(
            __import__("hora.core.const", fromlist=["GRAHA_NAMES"]
                       ).GRAHA_NAMES[int(RASI_LORD[owned])])
        assert (sits[name] - lagna) % 12 + 1 == int(row["sits_in"])


def test_as_worded_nakta_needs_an_aspect_wider_than_the_orb():
    """§29.2.4 showed an aspect inside the orb always gives one yoga or the
    other, so the rule's own condition needs a wide aspect.
    """
    # Mercury 1 Ar and Saturn 25 Ge: a sextile by house, 24° apart, far
    # outside the binding orb of 7° and outside bhavishya's further degree,
    # so no ithasala of any of the three kinds and no eesarpha.
    got = yogas.nakta(first=int(Graha.MERCURY), second=int(Graha.SATURN),
                      connector=int(Graha.MOON), first_longitude=1.0,
                      second_longitude=60.0 + 25.0, connector_longitude=0.5)
    assert got["first_pair_aspect"] == "Sextile aspect"
    assert got["first_pair_has_ithasala"] is None
    assert got["first_pair_has_eesarpha"] is False
    assert got["first_pair_qualifies_as_worded"] is True
    assert got["first_pair_qualifies_as_worked"] is False
    assert "an aspect wider than that" in (
        yogas.AS_WORDED_NAKTA_NEEDS_A_WIDE_ASPECT)


def test_a_close_aspect_can_never_satisfy_the_rule_as_worded():
    """The complement of §29.2.4's partition, over random pairs."""
    random.seed(2951)
    checked = 0
    for _ in range(3000):
        a, b = random.sample(range(7), 2)
        connector = next(g for g in (int(Graha.MOON), int(Graha.MERCURY),
                                     int(Graha.VENUS)) if g not in (a, b))
        got = yogas.nakta(first=a, second=b, connector=connector,
                          first_longitude=random.uniform(0, 360),
                          second_longitude=random.uniform(0, 360),
                          connector_longitude=random.uniform(0, 360))
        if not got["first_pair_qualifies_as_worded"]:
            continue
        checked += 1
        assert got["first_pair_aspect"] is not None
        assert got["first_pair_has_ithasala"] is None
        assert got["first_pair_has_eesarpha"] is False
    assert checked > 50


def test_the_connector_must_be_faster_than_both():
    """Swap the Moon for Saturn and nothing carries."""
    got = yogas.nakta(first=int(Graha.VENUS), second=int(Graha.MARS),
                      connector=int(Graha.SATURN), first_longitude=73.0,
                      second_longitude=225.0, connector_longitude=101.0)
    assert got["connector_is_faster_than_both"] is False
    assert got["connector_carries"] is False
    assert got["connector_ithasala_types"] == (None, None)
    assert got["present_as_worked"] is False


def test_the_speed_condition_and_the_two_ithasalas_are_one_condition():
    """A planet faster than both is the faster party in both legs, always."""
    random.seed(2952)
    for _ in range(1500):
        trio = random.sample(range(7), 3)
        trio.sort(key=yogas.speed_rank)
        first, second, connector = trio[0], trio[1], trio[2]
        got = yogas.nakta(first=first, second=second, connector=connector,
                          first_longitude=random.uniform(0, 360),
                          second_longitude=random.uniform(0, 360),
                          connector_longitude=random.uniform(0, 360))
        assert got["connector_is_faster_than_both"] is True
    assert "one condition stated twice" in (
        yogas.THE_SPEED_CONDITION_IS_THE_ITHASALA_CONDITION)


def test_a_bhavishya_leg_still_counts_as_an_ithasala():
    """"Forms ithasala with both" is not narrowed to vartamaana, and a
    bhavishya has not formed yet. Reported, not filtered.
    """
    assert "whether a bhavishya counts" in (
        yogas.WHICH_ITHASALA_THE_CONNECTOR_NEEDS_IS_NOT_SAID)
    # Moon 3° Ar; Venus at 11° Ge is 8° on, outside Venus's 7° orb by 1°.
    got = yogas.nakta(first=int(Graha.VENUS), second=int(Graha.MARS),
                      connector=int(Graha.MOON), first_longitude=60.0 + 11.0,
                      second_longitude=120.0 + 10.0, connector_longitude=3.0)
    assert got["connector_ithasala_types"] == ("Bhavishya", "Vartamaana")
    assert got["connector_carries"] is True


def test_nakta_needs_three_different_grahas():
    with pytest.raises(yogas.TajakaYogaError, match="three different grahas"):
        yogas.nakta(first=int(Graha.VENUS), second=int(Graha.VENUS),
                    connector=int(Graha.MOON), first_longitude=1.0,
                    second_longitude=2.0, connector_longitude=3.0)


def test_nakta_refuses_a_first_pair_footnote_83_cannot_rank():
    with pytest.raises(yogas.TajakaYogaError, match="cannot rank"):
        yogas.nakta(first=int(Graha.RAHU), second=int(Graha.KETU),
                    connector=int(Graha.MOON), first_longitude=1.0,
                    second_longitude=2.0, connector_longitude=3.0)


# --------------------------------------------------------------------------
# §29.2.6 Yamaya yoga
# --------------------------------------------------------------------------


def test_the_yamaya_rule_is_nakta_with_one_word_changed():
    assert "moves slower than both the planets" in yogas.YAMAYA_RULE
    assert "after obstacles and delays" in yogas.YAMAYA_RULE
    # The same slip, repeated verbatim.
    assert "someone shows by the 3rd planet" in yogas.YAMAYA_RULE

    # The two rules differ only in the speed word and the closing clause.
    swapped = yogas.YAMAYA_RULE.replace("Yamaya", "Nakta").replace(
        "moves slower than", "moves faster than").replace(
        " planet, after obstacles and delays.", " planet.")
    assert swapped == yogas.NAKTA_RULE
    assert "slower for faster" in yogas.YAMAYA_IS_NAKTA_WITH_THE_SPEED_REVERSED


def test_the_yamaya_example_reproduces():
    """Jupiter 16 Cn against Venus 13 Ge and Mars 15 Sc: a semi-sextile and a
    trinal, and Jupiter ahead of both because he is the slower party.
    """
    want = yogas.YAMAYA_EXAMPLE
    got = yogas.yamaya(
        first=int(Graha.VENUS), second=int(Graha.MARS),
        connector=int(Graha.JUPITER),
        first_longitude=float(want["first_longitude"]),
        second_longitude=float(want["second_longitude"]),
        connector_longitude=float(want["connector_longitude"]))
    assert got["first_pair_aspect"] is want["first_pair_aspect"]
    assert got["connector_aspects"] == (want["connector_to_first"],
                                        want["connector_to_second"])
    assert got["connector_is_slower_than_both"] is True
    assert got["connector_carries"] is True
    assert got["present_as_worked"] is True
    assert "after obstacles and delays" in str(got["shows"])


def test_the_jupiter_to_mars_leg_is_exactly_a_poorna():
    """16° against 15° is one degree, which is poorna's threshold on the nose.
    """
    got = yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.MARS),
                       connector=int(Graha.JUPITER), first_longitude=73.0,
                       second_longitude=225.0, connector_longitude=106.0)
    assert got["connector_ithasala_types"] == ("Vartamaana", "Poorna")

    leg = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                         faster_longitude=225.0, slower_longitude=106.0)
    assert leg["separation_from_exact"] == pytest.approx(1.0)
    assert leg["separation_from_exact"] == yogas.POORNA_DEGREES


def test_the_yamaya_example_is_the_nakta_example_with_jupiter_substituted():
    nakta_case, yamaya_case = yogas.NAKTA_EXAMPLE, yogas.YAMAYA_EXAMPLE
    for key in ("lagna_rasi", "first", "first_at", "first_longitude",
                "second", "second_at", "second_longitude",
                "first_pair_aspect", "connector_to_first",
                "connector_to_second"):
        assert nakta_case[key] == yamaya_case[key], key
    assert nakta_case["connector"] == "Moon"
    assert yamaya_case["connector"] == "Jupiter"


def test_jupiter_owns_the_eleventh_from_taurus():
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    eleventh = (1 + 11 - 1) % 12
    assert str(GRAHA_NAMES[int(RASI_LORD[eleventh])]) == "Jupiter"
    row = next(r for r in yogas.YAMAYA_EXAMPLE["lordships"]
               if r["graha"] == "Jupiter")
    assert row["owns"] == 11
    assert row["matter"] == "elder siblings or friends"


def test_the_connector_looks_the_other_way_in_a_yamaya():
    """A nakta's connector is behind both; a yamaya's is ahead of both. The
    two examples differ in exactly that.
    """
    assert float(yogas.NAKTA_EXAMPLE["connector_longitude"]) % 30 == 11.0
    assert float(yogas.YAMAYA_EXAMPLE["connector_longitude"]) % 30 == 16.0
    for case in (yogas.NAKTA_EXAMPLE, yogas.YAMAYA_EXAMPLE):
        advancements = [float(case[k]) % 30 for k in
                        ("first_longitude", "second_longitude")]
        connector = float(case["connector_longitude"]) % 30
        if case["connector"] == "Moon":
            assert all(connector < x for x in advancements)
        else:
            assert all(connector > x for x in advancements)
    assert "must be more advanced than both" in (
        yogas.THE_CONNECTOR_LOOKS_THE_OTHER_WAY_IN_A_YAMAYA)


def test_a_yamaya_connector_that_is_behind_carries_nothing():
    """Put Jupiter at 11° instead of 16° and both legs fail, because as the
    slower party he now has an eesarpha with each.
    """
    got = yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.MARS),
                       connector=int(Graha.JUPITER), first_longitude=73.0,
                       second_longitude=225.0, connector_longitude=101.0)
    assert got["connector_is_slower_than_both"] is True
    assert got["connector_ithasala_types"] == (None, None)
    assert got["connector_carries"] is False


def test_the_moon_cannot_make_a_yamaya_and_jupiter_cannot_make_a_nakta():
    """Each section's own connector is disqualified by the other's rule."""
    shared = {"first": int(Graha.VENUS), "second": int(Graha.MARS),
              "first_longitude": 73.0, "second_longitude": 225.0}
    assert yogas.yamaya(**shared, connector=int(Graha.MOON),
                        connector_longitude=101.0)["connector_speed_holds"] is (
        False)
    assert yogas.nakta(**shared, connector=int(Graha.JUPITER),
                       connector_longitude=106.0)["connector_speed_holds"] is (
        False)


def test_a_third_of_every_possible_connector_has_no_yoga():
    """Faster than both, slower than both, or between — and between is a case
    §29.2 never names.
    """
    tally = {"Nakta": 0, "Yamaya": 0, None: 0}
    for a, b in itertools.combinations(range(7), 2):
        for c in range(7):
            if c in (a, b):
                continue
            tally[yogas.connector_role(a, b, c)] += 1
    assert tally == {"Nakta": 35, "Yamaya": 35, None: 35}
    assert "35 have no yoga at all" in (
        yogas.A_CONNECTOR_BETWEEN_THE_TWO_HAS_NO_YOGA)


def test_connector_role_agrees_with_both_functions():
    random.seed(2961)
    for _ in range(1200):
        a, b, c = random.sample(range(7), 3)
        role = yogas.connector_role(a, b, c)
        shared = {"first": a, "second": b, "connector": c,
                  "first_longitude": random.uniform(0, 360),
                  "second_longitude": random.uniform(0, 360),
                  "connector_longitude": random.uniform(0, 360)}
        assert yogas.nakta(**shared)["connector_speed_holds"] is (
            role == "Nakta")
        assert yogas.yamaya(**shared)["connector_speed_holds"] is (
            role == "Yamaya")


def test_yamaya_carries_oi_164_the_same_way_nakta_does():
    got = yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.MARS),
                       connector=int(Graha.JUPITER), first_longitude=73.0,
                       second_longitude=225.0, connector_longitude=106.0)
    assert got["first_pair_qualifies_as_worded"] is False
    assert got["first_pair_qualifies_as_worked"] is True
    assert got["readings_agree"] is False
    assert got["undecided"] == (
        yogas.THE_RULE_AND_ITS_EXAMPLE_DISAGREE_ON_THE_FIRST_PAIR)


def test_yamaya_rejects_the_same_bad_inputs_as_nakta():
    with pytest.raises(yogas.TajakaYogaError, match="three different grahas"):
        yogas.yamaya(first=int(Graha.VENUS), second=int(Graha.VENUS),
                     connector=int(Graha.JUPITER), first_longitude=1.0,
                     second_longitude=2.0, connector_longitude=3.0)
    with pytest.raises(yogas.TajakaYogaError, match="cannot rank"):
        yogas.yamaya(first=int(Graha.RAHU), second=int(Graha.KETU),
                     connector=int(Graha.JUPITER), first_longitude=1.0,
                     second_longitude=2.0, connector_longitude=3.0)


# --------------------------------------------------------------------------
# §29.2.7 Manahoo yoga
# --------------------------------------------------------------------------


def test_the_manahoo_rule_and_notes_are_transcribed():
    assert "Saturn or Mars is in conjunction with the faster moving planet" in (
        yogas.MANAHOO_RULE)
    assert "cancels the ithasala yoga" in yogas.MANAHOO_RULE
    assert yogas.MANAHOO_RESULTS in yogas.MANAHOO_RULE
    assert "we obviously need the other planet" in (
        yogas.MANAHOO_NEEDS_THE_OTHER_MALEFIC)
    assert "advised to consider only conjunction" in yogas.MANAHOO_NOTES
    assert "one of them is enough" in yogas.MANAHOO_NOTES
    assert yogas.MANAHOO_SPOILERS == (int(Graha.SATURN), int(Graha.MARS))


def test_the_manahoo_example_reproduces():
    """Moon 18 Cn behind Jupiter 21 Pi is an ithasala; Saturn at 19 Cn is
    conjunct the Moon and inside her twelve degrees, so it cancels.
    """
    want = yogas.MANAHOO_EXAMPLE
    got = yogas.manahoo(
        faster=int(Graha.MOON), slower=int(Graha.JUPITER),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]),
        spoiler=int(Graha.SATURN),
        spoiler_longitude=float(want["spoiler_longitude"]))
    assert got["ithasala_type"] == want["ithasala_without_the_spoiler"]
    assert got["conjunct"] is True
    assert got["separation_from_faster"] == pytest.approx(1.0)
    assert got["faster_deeptamsa"] == 12.0
    assert got["within_faster_deeptamsa"] is True
    assert got["present"] is want["manahoo"]
    assert got["cancels_the_ithasala"] is True


def test_the_example_misnames_a_trinal_as_a_sextile():
    """Cancer to Pisces is the 9th, which §28.2 makes a trinal. Counted the
    other way it is the 5th, also a trinal. There is no sextile in it.
    """
    from hora.tajaka.aspects import aspect_on_house

    base = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                          faster_longitude=108.0, slower_longitude=351.0)
    assert base["house_from_faster"] == 9
    assert base["aspect"] == "Trinal aspect"
    assert aspect_on_house(5)["name"] == "Trinal aspect"
    assert aspect_on_house(9)["name"] == "Trinal aspect"
    assert yogas.MANAHOO_EXAMPLE["book_calls_the_aspect"] == "sextile"
    assert yogas.MANAHOO_EXAMPLE["aspect_is_really"] == "Trinal aspect"

    # The verdict is unaffected: §29.2.3 needs an aspect, not a named one.
    assert base["type"] == "Vartamaana"
    assert "the verdict is unchanged" in (
        yogas.THE_EXAMPLE_MISNAMES_A_TRINAL_AS_A_SEXTILE)


def test_the_notes_window_reproduces_rasi_for_rasi_and_in_order():
    """6°-30° is 18° plus and minus the Moon's twelve, and the ten rasis are
    exactly the ten §28.2 gives her from Cancer.
    """
    from hora.core.const import RASI_ABBR

    want = yogas.MANAHOO_NOTES_WINDOW
    got = yogas.manahoo_window(int(Graha.MOON), 108.0)
    assert got["deeptamsa"] == want["deeptamsa"]
    assert got["degrees"] == want["degrees"]
    assert tuple(RASI_ABBR[r] for r in got["rasis"]) == want["rasis"]
    assert len(got["rasis"]) == 10

    # The two the section leaves out are the 6th and the 8th from Cancer.
    missing = {"Sg", "Aq"}
    assert set(RASI_ABBR) - set(want["rasis"]) == missing
    assert "the 6th and the 8th being the two it leaves out" in (
        yogas.THE_NOTES_WINDOW_CONFIRMS_THE_ASPECT_TABLE)


def test_the_orb_is_the_faster_planets_not_the_spoilers():
    """"the deeptaamsa of the latter". Mercury's 7° against Saturn's 9°."""
    from hora.tajaka.aspects import deeptamsa

    assert deeptamsa(int(Graha.SATURN)) == 9.0
    assert deeptamsa(int(Graha.MERCURY)) == 7.0

    # Saturn 8° from Mercury: inside Saturn's own orb, outside Mercury's.
    got = yogas.manahoo(faster=int(Graha.MERCURY), slower=int(Graha.JUPITER),
                        faster_longitude=10.0, slower_longitude=60.0 + 15.0,
                        spoiler=int(Graha.SATURN), spoiler_longitude=18.0)
    assert got["faster_deeptamsa"] == 7.0
    assert got["separation_from_faster"] == pytest.approx(8.0)
    assert got["conjunct"] is True
    assert got["within_faster_deeptamsa"] is False
    assert got["present"] is False
    assert "not within its own" in yogas.THE_ORB_IS_THE_FASTER_PLANETS_NOT_THE_SPOILERS


def test_a_spoiler_conjunct_the_slower_planet_does_nothing():
    """The rule names the faster planet and only the faster planet."""
    got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                        faster_longitude=108.0, slower_longitude=351.0,
                        spoiler=int(Graha.SATURN), spoiler_longitude=352.0)
    assert got["conjunct"] is False
    assert got["present"] is False
    assert got["cancels_the_ithasala"] is False


def test_no_ithasala_means_no_manahoo():
    """There has to be something to cancel."""
    got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                        faster_longitude=90.0 + 25.0, slower_longitude=351.0,
                        spoiler=int(Graha.SATURN), spoiler_longitude=116.0)
    assert got["ithasala_type"] is None
    assert got["conjunct"] is True
    assert got["within_faster_deeptamsa"] is True
    assert got["present"] is False


def test_a_spoiler_inside_the_pair_cannot_spoil_it():
    """"we obviously need the other planet"."""
    got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.SATURN),
                        faster_longitude=4.0, slower_longitude=69.0,
                        spoiler=int(Graha.SATURN), spoiler_longitude=69.0)
    assert got["ithasala_type"] is not None
    assert got["spoiler_is_in_the_pair"] is True
    assert got["the_other_spoiler"] == int(Graha.MARS)
    assert got["present"] is False


def test_a_mars_saturn_ithasala_has_no_spoiler_left():
    """Neither of the two is available. OI-165."""
    for spoiler in yogas.MANAHOO_SPOILERS:
        got = yogas.manahoo(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                            faster_longitude=4.0, slower_longitude=69.0,
                            spoiler=spoiler, spoiler_longitude=5.0)
        assert got["ithasala_type"] is not None
        assert got["no_spoiler_left"] is True
        assert got["present"] is False
    assert "The section covers one of them being in the pair and not both" in (
        yogas.BOTH_SPOILERS_IN_THE_PAIR_IS_NOT_REACHED)


def test_only_saturn_and_mars_are_accepted_as_spoilers():
    for graha in (Graha.SUN, Graha.MOON, Graha.MERCURY, Graha.JUPITER,
                  Graha.VENUS, Graha.RAHU, Graha.KETU):
        with pytest.raises(yogas.TajakaYogaError, match="only Saturn and Mars"):
            yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                          faster_longitude=108.0, slower_longitude=351.0,
                          spoiler=int(graha), spoiler_longitude=109.0)


def test_the_aspect_reading_is_carried_but_not_applied():
    """The Notes describe it and then decline it. Saturn at 19° Ta aspects
    the Moon at 18° Cn within her orb but is not conjunct her.
    """
    got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                        faster_longitude=108.0, slower_longitude=351.0,
                        spoiler=int(Graha.SATURN),
                        spoiler_longitude=30.0 + 19.0)
    assert got["conjunct"] is False
    assert got["present"] is False
    assert got["aspects_faster"] is True
    assert got["separation_from_exact_aspect"] == pytest.approx(1.0)
    assert got["present_by_aspect"] is True
    assert "The conjunction reading is the one applied" in (
        yogas.THE_ASPECT_READING_IS_NAMED_AND_DECLINED)


def test_the_aspect_reading_fires_far_more_often_than_the_conjunction_one():
    """Ten rasis of twelve against one. Counted, because the section says
    only that it is wider.
    """
    conjunction = aspecting = 0
    for degree in range(360):
        got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                            faster_longitude=108.0, slower_longitude=351.0,
                            spoiler=int(Graha.SATURN),
                            spoiler_longitude=float(degree))
        conjunction += got["present"]
        aspecting += got["present_by_aspect"]
    assert conjunction == 24            # 18 +/- 12, clipped to Cancer
    assert aspecting == 240
    assert aspecting == 10 * conjunction


def test_one_spoiler_is_enough():
    assert "one is enough to spoil the ithasala" in yogas.ONE_SPOILER_IS_ENOUGH
    for spoiler in yogas.MANAHOO_SPOILERS:
        got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                            faster_longitude=108.0, slower_longitude=351.0,
                            spoiler=spoiler, spoiler_longitude=109.0)
        assert got["present"] is True


def test_manahoo_is_the_first_cancelling_yoga_in_the_chapter():
    assert "takes one away" in yogas.MANAHOO_IS_THE_FIRST_CANCELLING_YOGA
    # Every earlier yoga reports presence; this one reports a cancellation.
    got = yogas.manahoo(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                        faster_longitude=108.0, slower_longitude=351.0,
                        spoiler=int(Graha.SATURN), spoiler_longitude=109.0)
    assert got["ithasala_type"] == "Vartamaana"
    assert got["cancels_the_ithasala"] is True


# --------------------------------------------------------------------------
# §29.2.8 Kamboola yoga
# --------------------------------------------------------------------------


def test_the_kamboola_rule_is_transcribed():
    assert "If Moon has an ithasala with one of the planets (or both)" in (
        yogas.KAMBOOLA_RULE)
    assert "adds power to the ithasala yoga" in yogas.KAMBOOLA_RULE
    assert "strength of Moon and other planets" in yogas.KAMBOOLA_RULE


def test_the_kamboola_example_reproduces():
    """Mars 23 Sc and Jupiter 26 Pi have a trinal ithasala; the Moon at
    22 Le makes one with Mars and none with Jupiter.
    """
    want = yogas.KAMBOOLA_EXAMPLE
    got = yogas.kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]),
        moon_longitude=float(want["moon_longitude"]))
    assert got["pair_ithasala"] == want["pair_ithasala"]
    assert got["moon_ithasala_types"] == (want["moon_to_faster"],
                                          want["moon_to_slower"])
    assert got["reaches_faster"] is True
    assert got["reaches_slower"] is False
    assert got["present"] is want["present"]
    assert got["strengthens"] is True


def test_the_pairs_own_aspect_is_the_trinal_the_book_names():
    base = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                          faster_longitude=233.0, slower_longitude=356.0)
    assert base["house_from_faster"] == 5
    assert base["aspect"] == "Trinal aspect"
    assert base["separation_from_exact"] == pytest.approx(3.0)
    assert base["type"] == "Vartamaana"


def test_the_moon_to_mars_leg_is_a_poorna():
    """22° against 23° is one degree, poorna's threshold. The book says only
    "an ithasala yoga".
    """
    leg = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.MARS),
                         faster_longitude=142.0, slower_longitude=233.0)
    assert leg["house_from_faster"] == 4
    assert leg["aspect"] == "Square aspect"
    assert leg["separation_from_exact"] == pytest.approx(1.0)
    assert leg["type"] == "Poorna"


def test_the_example_never_shows_its_own_or_both_case():
    """The Moon at 22 Le is the 8th from Jupiter in Pi, which §28.2 leaves
    aspectless, so that leg cannot form at all.
    """
    from hora.tajaka.aspects import aspect_on_house

    leg = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                         faster_longitude=142.0, slower_longitude=356.0)
    assert leg["house_from_faster"] == 8
    assert aspect_on_house(8) is None
    assert leg["aspect"] is None
    assert leg["type"] is None
    assert yogas.KAMBOOLA_EXAMPLE["moon_to_slower"] is None
    assert "never worked" in yogas.THE_EXAMPLE_DOES_NOT_SHOW_THE_BOTH_CASE


def test_the_moon_can_reach_both_planets():
    """The rule's parenthesis, built even though the example does not show it.
    """
    got = yogas.kamboola(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                         faster_longitude=210.0 + 23.0,
                         slower_longitude=210.0 + 26.0,
                         moon_longitude=120.0 + 22.0)
    assert got["reaches_both"] is True
    assert all(t is not None for t in got["moon_ithasala_types"])
    assert got["present"] is True


def test_no_ithasala_in_the_pair_means_no_kamboola():
    """There has to be something to strengthen."""
    got = yogas.kamboola(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                         faster_longitude=210.0 + 28.0, slower_longitude=356.0,
                         moon_longitude=142.0)
    assert got["pair_ithasala"] is None
    assert got["reaches_faster"] is True
    assert got["present"] is False


def test_the_moon_must_be_behind_the_planet_she_reaches():
    """She is footnote 83's fastest body, so she is always the faster party."""
    assert yogas.speed_rank(int(Graha.MOON)) == 7
    for graha in range(7):
        if graha == int(Graha.MOON):
            continue
        assert yogas.faster_of(int(Graha.MOON), graha) == int(Graha.MOON)

    ahead = yogas.kamboola(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                           faster_longitude=233.0, slower_longitude=356.0,
                           moon_longitude=120.0 + 26.0)
    assert ahead["moon_ithasala_types"] == (None, None)
    assert ahead["present"] is False
    assert "never retrograde" in yogas.THE_MOON_IS_ALWAYS_THE_FASTER_PARTY


def test_the_moon_inside_the_pair_is_declined_not_answered():
    """§29.2.7 wrote a paragraph for the same situation; §29.2.8 did not."""
    got = yogas.kamboola(faster=int(Graha.MOON), slower=int(Graha.JUPITER),
                         faster_longitude=4.0, slower_longitude=69.0,
                         moon_longitude=4.0)
    assert got["pair_ithasala"] is not None
    assert got["moon_is_in_the_pair"] is True
    assert got["present"] is False
    assert got["undecided"] == yogas.THE_MOON_INSIDE_THE_PAIR_IS_NOT_REACHED


def test_the_moon_is_a_nakta_connector_or_a_kamboola_never_both():
    """Nakta needs the pair to have no ithasala; kamboola needs them to have
    one. The Moon always qualifies on speed for either.
    """
    random.seed(2981)
    both = seen_nakta = seen_kamboola = 0
    for _ in range(3000):
        a, b = random.sample([g for g in range(7) if g != int(Graha.MOON)], 2)
        first_at, second_at = random.uniform(0, 360), random.uniform(0, 360)
        moon_at = random.uniform(0, 360)
        assert yogas.connector_role(a, b, int(Graha.MOON)) == "Nakta"
        as_nakta = yogas.nakta(first=a, second=b, connector=int(Graha.MOON),
                               first_longitude=first_at,
                               second_longitude=second_at,
                               connector_longitude=moon_at)
        pair = yogas.ithasala(faster=a, slower=b, faster_longitude=first_at,
                              slower_longitude=second_at) if (
            yogas.faster_of(a, b) == a) else yogas.ithasala(
            faster=b, slower=a, faster_longitude=second_at,
            slower_longitude=first_at)
        as_kamboola = yogas.kamboola(
            faster=pair["faster"], slower=pair["slower"],
            faster_longitude=first_at if pair["faster"] == a else second_at,
            slower_longitude=second_at if pair["slower"] == b else first_at,
            moon_longitude=moon_at)
        seen_nakta += as_nakta["present_as_worded"]
        seen_kamboola += as_kamboola["present"]
        both += as_nakta["present_as_worded"] and as_kamboola["present"]
    assert both == 0
    assert seen_nakta > 0 and seen_kamboola > 0
    assert "mutually exclusive" in (
        yogas.THE_MOON_IS_A_NAKTA_OR_A_KAMBOOLA_NEVER_BOTH)


def test_kamboola_is_manahoos_mirror():
    """The chapter's only two yogas that name a graha."""
    assert yogas.MANAHOO_SPOILERS == (int(Graha.SATURN), int(Graha.MARS))
    assert "chapter's only two yogas that name a graha" in (
        yogas.KAMBOOLA_IS_MANAHOOS_MIRROR)

    shared = {"faster": int(Graha.MARS), "slower": int(Graha.JUPITER),
              "faster_longitude": 233.0, "slower_longitude": 356.0}
    strengthened = yogas.kamboola(**shared, moon_longitude=142.0)
    cancelled = yogas.manahoo(**shared, spoiler=int(Graha.SATURN),
                              spoiler_longitude=234.0)
    assert strengthened["strengthens"] is True
    assert cancelled["cancels_the_ithasala"] is True


def test_how_much_power_is_added_is_not_scored():
    """OI-166. Chapter 28 has two strengths and §29.2.8 names neither."""
    got = yogas.kamboola(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                         faster_longitude=233.0, slower_longitude=356.0,
                         moon_longitude=142.0)
    assert got["power_added"] is None
    assert got["undecided"] == yogas.HOW_MUCH_POWER_IS_ADDED_IS_NOT_SAID
    assert "gives no measure and no scale" in (
        yogas.HOW_MUCH_POWER_IS_ADDED_IS_NOT_SAID)


# --------------------------------------------------------------------------
# §29.2.9 Gairi-Kamboola yoga
# --------------------------------------------------------------------------


def test_the_gairi_kamboola_rule_is_transcribed():
    assert "in the last degree of a rasi" in yogas.GAIRI_KAMBOOLA_RULE
    assert "Kamboola yoga in waiting" in yogas.GAIRI_KAMBOOLA_RULE
    assert "ithasala with a strong planet" in yogas.GAIRI_KAMBOOLA_RULE
    assert "own navamsa, drekkana or hadda" in yogas.GAIRI_KAMBOOLA_RULE
    assert yogas.GAIRI_KAMBOOLA_RESULTS in yogas.GAIRI_KAMBOOLA_RULE
    assert yogas.LAST_DEGREE_OF_A_RASI == 29.0


def test_the_gairi_kamboola_example_reproduces():
    """Mars 1 Cp and Jupiter 2 Pi are a sextile ithasala; the Moon at
    29°10' Vi reaches neither now and reaches Mars on entering Libra.
    """
    want = yogas.GAIRI_KAMBOOLA_EXAMPLE
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]),
        moon_longitude=float(want["moon_longitude"]),
        strong_planet=int(Graha.VENUS),
        strong_planet_longitude=float(want["strong_planet_longitude"]))
    assert got["pair_ithasala"] == want["pair_ithasala"]
    assert got["moon_in_last_degree"] is True
    assert got["already_has_a_kamboola"] is False
    assert got["reaches_after_moving"] == (True, False)
    assert got["moon_enters"] == 6                      # Libra
    assert got["moon_disqualified"] is False
    assert got["present"] is want["present"]


def test_the_pairs_aspect_is_the_sextile_the_book_names():
    """Cp to Pi is the 3rd, and §28.2 does make that a sextile — unlike
    §29.2.7's example, which named one where there was a trinal.
    """
    base = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                          faster_longitude=271.0, slower_longitude=332.0)
    assert base["house_from_faster"] == 3
    assert base["aspect"] == "Sextile aspect"
    assert base["type"] == "Poorna"


def test_the_moon_reaches_neither_planet_where_she_stands():
    """The book says so: "Moon has no ithasala with Mars or Jupiter"."""
    moon = 150.0 + 29.0 + 10.0 / 60.0
    for other, longitude in ((Graha.MARS, 271.0), (Graha.JUPITER, 332.0)):
        leg = yogas.ithasala(faster=int(Graha.MOON), slower=int(other),
                             faster_longitude=moon, slower_longitude=longitude)
        assert leg["aspect"] is not None
        assert leg["faster_is_less_advanced"] is False
        assert leg["type"] is None


def test_the_moon_reaches_mars_and_not_jupiter_on_entering_libra():
    """Li to Cp is the 4th, a square; Li to Pi is the 6th, aspectless."""
    to_mars = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.MARS),
                             faster_longitude=180.0, slower_longitude=271.0)
    assert to_mars["house_from_faster"] == 4
    assert to_mars["aspect"] == "Square aspect"
    assert to_mars["type"] == "Poorna"

    to_jupiter = yogas.ithasala(faster=int(Graha.MOON),
                                slower=int(Graha.JUPITER),
                                faster_longitude=180.0, slower_longitude=332.0)
    assert to_jupiter["house_from_faster"] == 6
    assert to_jupiter["aspect"] is None
    assert to_jupiter["type"] is None


def test_all_three_dignity_checks_reproduce():
    """Mercury's navamsa, Venus's drekkana, Saturn's hadda — and none of them
    the Moon's own, which is what the condition asks.
    """
    from hora.core.const import GRAHA_NAMES, RASI_ABBR

    want = yogas.GAIRI_KAMBOOLA_EXAMPLE
    got = yogas.moon_is_disqualified(float(want["moon_longitude"]))
    assert (RASI_ABBR[got["navamsa"]],
            str(GRAHA_NAMES[got["navamsa_lord"]])) == want["moon_navamsa"]
    assert (RASI_ABBR[got["drekkana"]],
            str(GRAHA_NAMES[got["drekkana_lord"]])) == want["moon_drekkana"]
    assert str(GRAHA_NAMES[got["hadda_lord"]]) == want["moon_hadda"]
    assert got["disqualified"] is False
    assert "none of the three is her own" in (
        yogas.THE_THREE_DIGNITY_CHECKS_REPRODUCE)


def test_each_disqualifier_is_answered_separately():
    """Four conditions, four flags. The Moon in Taurus is exalted; in Scorpio
    debilitated; in Cancer she owns the sign, so early Cancer is her own
    navamsa and her own drekkana.
    """
    exalted = yogas.moon_is_disqualified(30.0 + 5.0)
    assert exalted["exalted"] is True and exalted["disqualified"] is True

    fallen = yogas.moon_is_disqualified(210.0 + 5.0)
    assert fallen["debilitated"] is True and fallen["disqualified"] is True

    # Cancer 0°: navamsa Cancer (movable sign starts from itself) and the
    # first drekkana is the sign itself — both the Moon's own.
    own = yogas.moon_is_disqualified(90.0 + 0.5)
    assert own["own_navamsa"] is True
    assert own["own_drekkana"] is True
    assert own["disqualified"] is True


def test_a_disqualified_moon_kills_the_yoga():
    """Move the example's Moon to the last degree of Taurus, where she is
    exalted. Everything else is unchanged.
    """
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=271.0, slower_longitude=332.0,
        moon_longitude=30.0 + 29.0 + 10.0 / 60.0,
        strong_planet=int(Graha.VENUS), strong_planet_longitude=63.0)
    assert got["moon_in_last_degree"] is True
    assert got["moon_disqualified"] is True
    assert got["moon_dignity"]["exalted"] is True
    assert got["present"] is False


def test_the_moon_must_not_be_the_strong_one():
    """Two of the four disqualifiers are dignities, so the section is not
    asking for a weak Moon by accident — it wants the strength elsewhere.
    """
    assert "The strength has to come from the other planet" in (
        yogas.THE_MOON_MUST_NOT_BE_THE_STRONG_ONE)
    dignified = yogas.moon_is_disqualified(30.0 + 5.0)
    assert dignified["exalted"] is True


def test_the_strong_planets_ithasala_is_also_in_waiting():
    """"He also has ithasala with Venus" is false where the Moon stands and
    true once she enters Libra.
    """
    moon, venus = 150.0 + 29.0 + 10.0 / 60.0, 183.0
    now = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                         faster_longitude=moon, slower_longitude=venus)
    assert now["aspect"] == "Semi-sextile aspect"
    assert now["faster_is_less_advanced"] is False
    assert now["type"] is None
    apart = yogas.eesarpha(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                           faster_longitude=moon, slower_longitude=venus)
    assert apart["faster_is_more_advanced"] is True

    later = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.VENUS),
                           faster_longitude=180.0, slower_longitude=venus)
    assert later["aspect"] == "Conjunction"
    assert later["separation_from_exact"] == pytest.approx(3.0)
    assert later["type"] == "Vartamaana"
    assert "only after entering Libra" in (
        yogas.THE_STRONG_PLANETS_ITHASALA_IS_ALSO_IN_WAITING)


def test_the_example_reports_the_venus_leg_as_waiting_not_present():
    want = yogas.GAIRI_KAMBOOLA_EXAMPLE
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=271.0, slower_longitude=332.0,
        moon_longitude=float(want["moon_longitude"]),
        strong_planet=int(Graha.VENUS), strong_planet_longitude=183.0)
    assert got["strong_planet_ithasala_now"] is None
    assert got["strong_planet_ithasala_after_moving"] == "Vartamaana"
    assert got["has_the_strong_leg"] is True


def test_crossing_a_rasi_puts_the_moon_behind_everything():
    """At 0° her advancement is zero, so she is less advanced than every
    planet at once and only the aspect and the orb are left to check.
    """
    random.seed(2991)
    for _ in range(1500):
        other = random.choice([g for g in range(7) if g != int(Graha.MOON)])
        other_at = random.uniform(0, 360)
        leg = yogas.ithasala(faster=int(Graha.MOON), slower=other,
                             faster_longitude=180.0,
                             slower_longitude=other_at)
        if advancement_is_zero := (other_at % 30 == 0):
            assert leg["faster_is_less_advanced"] is False
            continue
        assert advancement_is_zero is False
        assert leg["faster_is_less_advanced"] is True
        expected = (leg["aspect"] is not None
                    and leg["separation_from_exact"] <= leg["binding_deeptamsa"])
        assert leg["vartamaana"] is expected
    assert "less advanced than every planet" in (
        yogas.CROSSING_A_RASI_PUTS_THE_MOON_BEHIND_EVERYTHING)


def test_a_moon_not_in_the_last_degree_gives_no_gairi_kamboola():
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=271.0, slower_longitude=332.0,
        moon_longitude=150.0 + 20.0,
        strong_planet=int(Graha.VENUS), strong_planet_longitude=183.0)
    assert got["moon_advancement"] == pytest.approx(20.0)
    assert got["moon_in_last_degree"] is False
    assert got["present"] is False


def test_no_pair_ithasala_means_no_gairi_kamboola():
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=270.0 + 20.0, slower_longitude=332.0,
        moon_longitude=150.0 + 29.0 + 10.0 / 60.0,
        strong_planet=int(Graha.VENUS), strong_planet_longitude=183.0)
    assert got["pair_ithasala"] is None
    assert got["present"] is False


def test_the_strong_leg_is_required():
    """Drop the strong planet and the yoga fails, as the rule says it must."""
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=271.0, slower_longitude=332.0,
        moon_longitude=150.0 + 29.0 + 10.0 / 60.0)
    assert got["has_the_strong_leg"] is False
    assert got["present"] is False


def test_strength_is_taken_as_given_and_never_decided():
    """OI-166 again: §29.2.8 left the power unmeasured and §29.2.9 leaves
    "strong" unmeasured in the same way.
    """
    got = yogas.gairi_kamboola(
        faster=int(Graha.MARS), slower=int(Graha.JUPITER),
        faster_longitude=271.0, slower_longitude=332.0,
        moon_longitude=150.0 + 29.0 + 10.0 / 60.0,
        strong_planet=int(Graha.VENUS), strong_planet_longitude=183.0)
    assert got["strength_undecided"] == (
        yogas.WHICH_STRENGTH_MAKES_A_PLANET_STRONG_IS_NOT_SAID)
    assert "gives no measure of strength" in (
        yogas.WHICH_STRENGTH_MAKES_A_PLANET_STRONG_IS_NOT_SAID)


# --------------------------------------------------------------------------
# §29.2.10 Khallasara yoga
# --------------------------------------------------------------------------


def test_the_khallasara_rule_is_transcribed():
    assert "in the rasi between Moon and another planet X" in (
        yogas.KHALLASARA_RULE)
    assert "without ithasala with either planet" in yogas.KHALLASARA_RULE
    assert "destroys the signification of X" in yogas.KHALLASARA_RULE


def test_the_khallasara_example_reproduces():
    """Virgo lagna, Moon 1 Ar, Mercury 15 Ta, Jupiter 29 Ge."""
    want = yogas.KHALLASARA_EXAMPLE
    got = yogas.khallasara(
        lagna_rasi=5, moon_longitude=float(want["moon_longitude"]),
        lord_longitude=float(want["lord_longitude"]),
        x=int(Graha.JUPITER), x_longitude=float(want["x_longitude"]))
    assert got["lagna_lord_name"] == want["lagna_lord"]
    assert got["rasis"] == (0, 1, 2)
    assert got["moon_leg_aspect"] == want["moon_leg_aspect"]
    assert got["x_leg_aspect"] == want["x_leg_aspect"]
    assert got["no_ithasala_with_either"] is True
    assert got["present_on_the_arc"] is want["present"]
    assert got["present_if_consecutive"] is want["present"]


def test_the_lagna_lord_is_derived_from_the_lagna():
    """Virgo's lord is Mercury, and the section says "lagna lord" without
    naming him in the rule.
    """
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    assert str(GRAHA_NAMES[int(RASI_LORD[5])]) == "Mercury"
    got = yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                           lord_longitude=45.0, x=int(Graha.JUPITER),
                           x_longitude=89.0)
    assert got["lagna_lord"] == int(Graha.MERCURY)


def test_the_harms_are_the_houses_x_owns_from_the_lagna():
    """Jupiter owns the 4th and the 7th from Virgo, and the five matters the
    example lists are those two houses'.
    """
    want = yogas.KHALLASARA_EXAMPLE
    got = yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                           lord_longitude=45.0, x=int(Graha.JUPITER),
                           x_longitude=89.0)
    assert got["destroys_houses"] == want["x_owns"] == (4, 7)
    assert want["destroys"] == ("mother", "education", "house", "vehicles",
                                "marriage")
    assert "mother, education, house and vehicles from the 4th" in (
        yogas.THE_HARMS_ARE_THE_HOUSES_X_OWNS)


def test_both_legs_fail_on_width_and_not_on_a_missing_aspect():
    """Fourteen degrees against a binding orb of seven, twice."""
    moon_leg = yogas.ithasala(faster=int(Graha.MOON), slower=int(Graha.MERCURY),
                              faster_longitude=1.0, slower_longitude=45.0)
    x_leg = yogas.ithasala(faster=int(Graha.MERCURY), slower=int(Graha.JUPITER),
                           faster_longitude=45.0, slower_longitude=89.0)
    for leg in (moon_leg, x_leg):
        assert leg["aspect"] == "Semi-sextile aspect"
        assert leg["faster_is_less_advanced"] is True
        assert leg["separation_from_exact"] == pytest.approx(14.0)
        assert leg["binding_deeptamsa"] == 7.0
        assert leg["type"] is None                 # not even a bhavishya
    assert "satisfied by width" not in yogas.KHALLASARA_RULE
    assert "each has an aspect and no ithasala" in (
        yogas.THE_LEGS_FAIL_ON_WIDTH_NOT_ON_ASPECT)


def test_an_ithasala_on_either_leg_kills_the_yoga():
    """Bring Mercury to 5° Ta and the Moon reaches him."""
    got = yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                           lord_longitude=30.0 + 5.0, x=int(Graha.JUPITER),
                           x_longitude=89.0)
    assert got["moon_leg"] is not None
    assert got["no_ithasala_with_either"] is False
    assert got["present_on_the_arc"] is False


def test_between_is_answered_three_ways():
    """The example satisfies all three, so it separates none. OI-167."""
    got = yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                           lord_longitude=45.0, x=int(Graha.JUPITER),
                           x_longitude=89.0)
    assert got["between_on_the_arc_from_the_moon"] is True
    assert got["the_single_rasi_between"] is True
    # Not on the arc the other way: Ge to Ar the long way skips Taurus.
    assert got["between_on_the_arc_from_x"] is False
    assert "The example is all three at once" in (
        yogas.BETWEEN_CAN_BE_READ_THREE_WAYS)


def test_the_readings_come_apart_when_the_planets_are_further_off():
    """Moon in Ar, Mercury in Ge, Jupiter in Le: on the arc but not
    consecutive.
    """
    got = yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                           lord_longitude=60.0 + 15.0, x=int(Graha.JUPITER),
                           x_longitude=120.0 + 29.0)
    assert got["between_on_the_arc_from_the_moon"] is True
    assert got["the_single_rasi_between"] is False
    assert got["readings_agree"] is False
    assert got["undecided"] == yogas.BETWEEN_CAN_BE_READ_THREE_WAYS
    assert got["present_on_the_arc"] != got["present_if_consecutive"]


def test_the_arc_reading_fires_far_more_often_than_the_strict_one():
    """Counted over every arrangement of three rasis."""
    on_the_arc = consecutive = 0
    for moon in range(12):
        for lord in range(12):
            for other in range(12):
                got = yogas.khallasara(
                    lagna_rasi=5, moon_longitude=moon * 30.0 + 1.0,
                    lord_longitude=lord * 30.0 + 15.0, x=int(Graha.JUPITER),
                    x_longitude=other * 30.0 + 29.0)
                on_the_arc += got["between_on_the_arc_from_the_moon"]
                consecutive += got["the_single_rasi_between"]
    assert consecutive == 24            # 12 forward + 12 backward
    assert on_the_arc == 660
    assert on_the_arc > 25 * consecutive
    assert "fires far" in yogas.THE_READING_CHANGES_HOW_OFTEN_IT_FIRES


def test_x_cannot_be_the_moon_or_the_lagna_lord():
    for graha in (Graha.MOON, Graha.MERCURY):
        with pytest.raises(yogas.TajakaYogaError, match="third planet"):
            yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                             lord_longitude=45.0, x=int(graha),
                             x_longitude=89.0)


def test_khallasara_is_the_first_yoga_to_need_the_lagna():
    """Every earlier yoga in §29.2 reads planets against planets."""
    assert "Khallasara needs the lagna" in (
        yogas.KHALLASARA_IS_THE_FIRST_YOGA_TO_NEED_THE_LAGNA)
    # And it destroys significations, where §29.2.7 destroyed a yoga.
    got = yogas.khallasara(lagna_rasi=5, moon_longitude=1.0,
                           lord_longitude=45.0, x=int(Graha.JUPITER),
                           x_longitude=89.0)
    assert got["destroys_houses"] == (4, 7)
    assert "destroys the signification of X" in got["rule"]


# --------------------------------------------------------------------------
# §29.2.11 Radda yoga
# --------------------------------------------------------------------------


def test_the_radda_rule_and_its_four_triggers_are_transcribed():
    assert "debilitation or retrogression or combustion or otherwise weak" in (
        yogas.RADDA_RULE)
    assert "negates ithasala and gives bad results" in yogas.RADDA_RULE
    names = [row["trigger"] for row in yogas.RADDA_TRIGGERS]
    assert names == ["debilitation", "retrogression", "combustion",
                     "otherwise weak"]
    assert [row["computable"] for row in yogas.RADDA_TRIGGERS] == [
        True, True, True, False]


def test_the_debilitation_example_reproduces():
    """Aries lagna, Mars 15 Sg and Saturn 20 Ar are a trinal ithasala, and
    Saturn is debilitated in Aries.
    """
    want = yogas.RADDA_EXAMPLES[1]
    got = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                      faster_longitude=float(want["faster_longitude"]),
                      slower_longitude=float(want["slower_longitude"]),
                      lagna_rasi=0)
    assert got["ithasala_type"] == want["ithasala"]
    assert got["parties"][int(Graha.SATURN)]["debilitated"] is True
    assert got["triggered_by"] == (int(Graha.SATURN),)
    assert got["present"] is True
    assert got["negates_the_ithasala"] is True


def test_the_pairs_aspect_is_the_trinal_the_ithasala_needs():
    base = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                          faster_longitude=255.0, slower_longitude=20.0)
    assert base["house_from_faster"] == 5
    assert base["aspect"] == "Trinal aspect"
    assert base["separation_from_exact"] == pytest.approx(5.0)
    assert base["binding_deeptamsa"] == 8.0
    assert base["type"] == "Vartamaana"


def test_the_harms_are_the_houses_the_weak_planet_owns():
    """Saturn owns the 10th and 11th from Aries: career and material gains.
    §29.2.10 read its harms the same way.
    """
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    for house in (10, 11):
        assert str(GRAHA_NAMES[int(RASI_LORD[(0 + house - 1) % 12])]) == "Saturn"
    got = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                      faster_longitude=255.0, slower_longitude=20.0,
                      lagna_rasi=0)
    assert got["destroys_houses"] == yogas.RADDA_EXAMPLES[1]["owns"] == (10, 11)
    assert "Section 29.2.10 read its harms the same way" in (
        yogas.THE_HARMS_ARE_THE_HOUSES_THE_WEAK_PLANET_OWNS)


def test_the_retrogression_example_has_no_ithasala_to_negate():
    """Retrograde Mercury 5 Vi and Mars 7 Sc: a sextile, and Mercury behind
    but retrograde, so the pair is diverging.
    """
    want = yogas.RADDA_EXAMPLES[0]
    got = yogas.radda(faster=int(Graha.MERCURY), slower=int(Graha.MARS),
                      faster_longitude=float(want["faster_longitude"]),
                      slower_longitude=float(want["slower_longitude"]),
                      faster_retrograde=True)
    assert got["ithasala_type"] is want["ithasala"]
    assert got["no_ithasala_to_negate"] is True
    assert got["eesarpha_instead"] is want["eesarpha"]
    assert got["triggered_by"] == (int(Graha.MERCURY),)
    assert got["present"] is False              # nothing to negate
    assert got["overlap"] is not None


def test_the_book_names_this_overlap_and_leaves_it():
    """"Whether one calls it Eesarpha or Radda yoga depends on one's
    interpretation, but the results are going to be bad in either case."
    """
    assert "depends on one's interpretation" in yogas.RADDA_OVERLAPS_EESARPHA
    assert "bad in either case" in yogas.RADDA_OVERLAPS_EESARPHA
    assert "No other section in the chapter admits an overlap" in (
        yogas.THE_BOOK_NAMES_THIS_OVERLAP_AND_LEAVES_IT)


def test_radda_contradicts_29_2_3_on_a_retrograde_slower_planet():
    """§29.2.3 called it "no problem" and "a faster realization"; §29.2.11
    negates the same ithasala. OI-168.
    """
    kwargs = {"faster": int(Graha.MOON), "slower": int(Graha.MERCURY),
              "faster_longitude": 18.0, "slower_longitude": 60.0 + 24.0}
    stands = yogas.ithasala(**kwargs, slower_retrograde=True)
    assert stands["type"] is not None           # §29.2.3: the ithasala holds
    assert "faster realization" in str(yogas.RETROGRESSION_CASES[1]["book_says"])

    negated = yogas.radda(**kwargs, slower_retrograde=True)
    assert negated["ithasala_type"] == stands["type"]
    assert negated["triggered_by"] == (int(Graha.MERCURY),)
    assert negated["negates_the_ithasala"] is True
    assert "the ones the second destroys" in (
        yogas.RADDA_CONTRADICTS_THE_ITHASALA_NOTES_ON_RETROGRESSION)


def test_29_2_3s_retrograde_faster_case_is_also_negated():
    """The case §29.2.3's Special Notes built specially — retrograde and more
    advanced — is an ithasala there and a radda here.
    """
    kwargs = {"faster": int(Graha.MERCURY), "slower": int(Graha.MARS),
              "faster_longitude": _longitude("23 Vi"),
              "slower_longitude": _longitude("21 Cp"),
              "faster_retrograde": True}
    stands = yogas.ithasala(**kwargs)
    assert stands["type"] == "Vartamaana"
    negated = yogas.radda(**kwargs)
    assert negated["negates_the_ithasala"] is True


def test_debilitation_is_read_for_either_party():
    """The rule says "involves a planet", not which one."""
    # Mars debilitated in Cancer, as the faster party.
    got = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                      faster_longitude=90.0 + 15.0, slower_longitude=150.0 + 20.0)
    assert got["parties"][int(Graha.MARS)]["debilitated"] is True
    assert got["triggered_by"] == (int(Graha.MARS),)


def test_combustion_needs_the_sun_and_says_so_when_it_is_missing():
    """The section names combustion and gives no orb; chapter 3 supplies one."""
    from hora.core.constants.graha import COMBUSTION_ORB

    without = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                          faster_longitude=255.0, slower_longitude=20.0)
    assert without["combustion_undecided"] is not None
    assert without["parties"][int(Graha.MARS)]["combust"] is None

    # Mars 3° from the Sun, inside chapter 3's direct orb.
    orb = COMBUSTION_ORB[int(Graha.MARS)][0]
    assert orb > 3.0
    burnt = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                        faster_longitude=255.0, slower_longitude=20.0,
                        sun_longitude=252.0)
    assert burnt["combustion_undecided"] is None
    assert burnt["parties"][int(Graha.MARS)]["combust"] is True
    assert burnt["parties"][int(Graha.MARS)]["combustion_separation"] == (
        pytest.approx(3.0))
    assert int(Graha.MARS) in burnt["triggered_by"]
    assert burnt["present"] is True
    assert next(row for row in yogas.RADDA_TRIGGERS
                if row["trigger"] == "combustion")["orb_from"] == (
        "chapter 3, not this section")


def test_a_retrograde_planet_uses_the_wider_combustion_orb():
    from hora.core.constants.graha import COMBUSTION_ORB

    direct, retro = COMBUSTION_ORB[int(Graha.MERCURY)]
    assert retro != direct
    gap = (direct + retro) / 2.0
    moving = yogas.radda(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                         faster_longitude=100.0, slower_longitude=160.0,
                         sun_longitude=100.0 - gap, faster_retrograde=True)
    still = yogas.radda(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                        faster_longitude=100.0, slower_longitude=160.0,
                        sun_longitude=100.0 - gap)
    assert moving["parties"][int(Graha.MERCURY)]["combust"] is (retro > direct)
    assert still["parties"][int(Graha.MERCURY)]["combust"] is (direct > retro)


def test_otherwise_weak_is_an_input_and_never_decided():
    """OI-166's family. Three triggers are decidable and the fourth is not."""
    got = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                      faster_longitude=233.0, slower_longitude=356.0,
                      slower_otherwise_weak=True)
    assert got["ithasala_type"] is not None
    assert got["parties"][int(Graha.JUPITER)]["triggers"] == ("otherwise_weak",)
    assert got["present"] is True
    assert "has no measure" in yogas.OTHERWISE_WEAK_HAS_NO_TEST

    clean = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.JUPITER),
                        faster_longitude=233.0, slower_longitude=356.0)
    assert clean["triggered_by"] == ()
    assert clean["present"] is False


def test_radda_cancels_from_inside_the_pair():
    """Manahoo needs a third planet, khallasara needs the lagna lord, radda
    needs nothing but the two already there.
    """
    got = yogas.radda(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                      faster_longitude=255.0, slower_longitude=20.0)
    assert got["present"] is True
    assert "needs only the condition of a planet already in the ithasala" in (
        yogas.RADDA_CANCELS_FROM_INSIDE_THE_PAIR)


# --------------------------------------------------------------------------
# §29.2.12 Duhphali-Kutta yoga
# --------------------------------------------------------------------------


def test_the_duhphali_kutta_rule_is_transcribed():
    assert "(a) the faster planet in an ithasala is exalted" in (
        yogas.DUHPHALI_KUTTA_RULE)
    assert "(b) the slower planet is not exalted" in yogas.DUHPHALI_KUTTA_RULE
    assert yogas.DUHPHALI_KUTTA_RESULTS in yogas.DUHPHALI_KUTTA_RULE
    assert yogas.GOOD_BALA_GRADES == ("strong", "very strong",
                                      "extraordinarily strong")


def test_the_example_is_the_exact_mirror_of_the_rule():
    """Saturn, the slower planet, is the strong one; Mars, the faster, is the
    weak one. The rule asks for the opposite. OI-169.
    """
    want = yogas.DUHPHALI_KUTTA_EXAMPLE
    got = yogas.duhphali_kutta(
        faster=int(Graha.MARS), slower=int(Graha.SATURN),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]),
        faster_bala=3.0, slower_bala=12.0)
    assert got["ithasala_type"] == want["ithasala"]
    assert got["slower_side"]["exalted"] is True
    assert got["slower_side"]["qualifies_as_the_strong_side"] is True
    assert got["faster_side"]["qualifies_as_the_weak_side"] is True
    assert got["present_as_worked"] is True
    assert got["present_as_worded"] is False
    assert got["readings_agree"] is False
    assert got["undecided"] == yogas.THE_RULE_AND_ITS_EXAMPLE_ARE_MIRROR_IMAGES
    assert "the slower planet" in str(want["book_says"])


def test_the_example_is_right_about_which_planet_is_faster():
    """It is not a labelling slip: footnote 83 does put Mars above Saturn."""
    assert yogas.faster_of(int(Graha.MARS), int(Graha.SATURN)) == int(Graha.MARS)
    assert yogas.speed_rank(int(Graha.MARS)) > yogas.speed_rank(int(Graha.SATURN))
    assert "The two are exact mirrors" in (
        yogas.THE_RULE_AND_ITS_EXAMPLE_ARE_MIRROR_IMAGES)


def test_the_pairs_ithasala_holds():
    base = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                          faster_longitude=78.0, slower_longitude=200.0)
    assert base["house_from_faster"] == 5
    assert base["aspect"] == "Trinal aspect"
    assert base["separation_from_exact"] == pytest.approx(2.0)
    assert base["type"] == "Vartamaana"


def test_saturn_is_exalted_in_libra_and_mars_is_not_dignified_in_gemini():
    from hora.core.constants.graha import EXALTATION_RASI

    assert int(EXALTATION_RASI[int(Graha.SATURN)]) == 6          # Libra
    assert int(EXALTATION_RASI[int(Graha.MARS)]) == 9            # Capricorn
    mars = yogas._duhphali_side(int(Graha.MARS), 78.0, 3.0)
    assert mars["exalted"] is False and mars["own_rasi"] is False


def test_the_rule_reads_the_other_way_round_when_the_chart_is_mirrored():
    """Swap the two balas and the rule is satisfied and the example is not."""
    got = yogas.duhphali_kutta(
        faster=int(Graha.MARS), slower=int(Graha.SATURN),
        faster_longitude=78.0, slower_longitude=150.0 + 20.0,
        faster_bala=12.0, slower_bala=3.0)
    assert got["ithasala_type"] is not None
    assert got["present_as_worded"] is True
    assert got["present_as_worked"] is False


def test_weak_is_a_band_name_and_good_is_not():
    """§28.4.6 names five bands; "weak" is one and "good" is not. The example
    calls the same bala good and then strong.
    """
    from hora.tajaka.panchavargeeya import (
        PANCHA_VARGEEYA_GRADES,
        PANCHA_VARGEEYA_TOP_GRADE,
    )

    bands = [row[2] for row in PANCHA_VARGEEYA_GRADES] + [
        PANCHA_VARGEEYA_TOP_GRADE]
    assert "weak" in bands
    assert "good" not in bands
    assert set(yogas.GOOD_BALA_GRADES) <= set(bands)
    assert yogas.DUHPHALI_KUTTA_EXAMPLE["slower_bala"] == "good"
    assert "is exalted and strong" in str(
        yogas.DUHPHALI_KUTTA_EXAMPLE["book_says"])
    assert "good is read as" in (
        yogas.GOOD_IS_NOT_A_BAND_NAME_BUT_THE_EXAMPLE_SUPPLIES_ONE)


def test_the_middle_band_satisfies_neither_condition():
    """Ordinary strength, 5 to 10, is neither good nor weak."""
    side = yogas._duhphali_side(int(Graha.MARS), 78.0, 7.0)
    assert side["bala_grade"] == "ordinary strength"
    assert side["has_good_bala"] is False
    assert side["has_weak_bala"] is False
    assert side["qualifies_as_the_strong_side"] is False
    assert side["qualifies_as_the_weak_side"] is False
    assert side["in_the_middle_band"] is True
    assert "The rule says nothing about it" in (
        yogas.THE_MIDDLE_BAND_SATISFIES_NEITHER_CONDITION)


def test_condition_b_is_stricter_than_the_negation_of_condition_a():
    """Over every band, being not-strong is not the same as being weak."""
    from hora.tajaka.panchavargeeya import pancha_vargeeya_grade

    for bala in (2.0, 7.0, 12.0, 17.0, 22.0):
        side = yogas._duhphali_side(int(Graha.MARS), 78.0, bala)
        not_a = not side["qualifies_as_the_strong_side"]
        b = side["qualifies_as_the_weak_side"]
        assert b <= not_a                       # (b) implies not-(a)
        if pancha_vargeeya_grade(bala) == "ordinary strength":
            assert not_a and not b              # and is strictly stronger


def test_condition_a_is_a_disjunction():
    """Exalted or own rasi or a good bala — any one of the three."""
    # Own rasi with a weak bala still qualifies as the strong side.
    own = yogas._duhphali_side(int(Graha.MARS), 210.0 + 5.0, 2.0)
    assert own["own_rasi"] is True
    assert own["has_good_bala"] is False
    assert own["qualifies_as_the_strong_side"] is True
    # And it is then disqualified from being the weak side.
    assert own["qualifies_as_the_weak_side"] is False


def test_this_is_the_only_strength_29_2_ever_names():
    """§29.2.8 and §29.2.9 asked for strength and named no measure. OI-166."""
    assert "panchavargeeya bala" in yogas.DUHPHALI_KUTTA_RULE
    assert "strength of Moon and other planets" in yogas.KAMBOOLA_RULE
    assert "panchavargeeya" not in yogas.KAMBOOLA_RULE
    assert "ithasala with a strong planet" in yogas.GAIRI_KAMBOOLA_RULE
    assert "panchavargeeya" not in yogas.GAIRI_KAMBOOLA_RULE
    assert "no other section in" in (
        yogas.PANCHA_VARGEEYA_BALA_IS_THE_ONE_STRENGTH_29_2_NAMES)


def test_a_missing_bala_leaves_the_grade_unknown():
    got = yogas.duhphali_kutta(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                               faster_longitude=78.0, slower_longitude=200.0)
    assert got["balas_supplied"] is False
    assert got["faster_side"]["bala_grade"] is None
    assert got["faster_side"]["has_weak_bala"] is False
    # Saturn is still exalted, so the strong side holds without a bala.
    assert got["slower_side"]["qualifies_as_the_strong_side"] is True
    assert got["present_as_worked"] is False        # Mars cannot be shown weak


def test_no_ithasala_means_no_duhphali_kutta():
    got = yogas.duhphali_kutta(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                               faster_longitude=60.0 + 25.0,
                               slower_longitude=200.0,
                               faster_bala=3.0, slower_bala=12.0)
    assert got["ithasala_type"] is None
    assert got["present_as_worded"] is False
    assert got["present_as_worked"] is False


# --------------------------------------------------------------------------
# §29.2.13 Duttota yoga
# --------------------------------------------------------------------------


def test_the_duttota_rule_and_its_two_test_lists_are_transcribed():
    assert "two planets in an ithasala are weak" in yogas.DUTTOTA_RULE
    assert "one of them has an ithasala yoga with a strong planet" in (
        yogas.DUTTOTA_RULE)
    assert yogas.DUTTOTA_WEAK_TESTS == (
        "debilitated", "inimical rasi", "low panchavargeeya bala")
    assert yogas.DUTTOTA_STRONG_TESTS == (
        "exalted", "own rasi", "high panchavargeeya bala")
    assert yogas.DUTTOTA_RESULTS in yogas.DUTTOTA_RULE


def test_the_duttota_example_reproduces():
    """Aries lagna. Mars 19 Li opposes Saturn 20 Ar in a poorna ithasala;
    Saturn is debilitated; exalted Venus at 18 Pi reaches Saturn.
    """
    want = yogas.DUTTOTA_EXAMPLE
    got = yogas.duttota(
        faster=int(Graha.MARS), slower=int(Graha.SATURN),
        faster_longitude=float(want["faster_longitude"]),
        slower_longitude=float(want["slower_longitude"]),
        rescuer=int(Graha.VENUS),
        rescuer_longitude=float(want["rescuer_longitude"]), lagna_rasi=0)
    assert got["ithasala_type"] == want["pair_ithasala"]
    assert got["slower_side"]["debilitated"] is True
    assert got["strong_side"]["exalted"] is want["rescuer_exalted"]
    assert got["rescue_aspects"][int(Graha.SATURN)] == want["rescue_aspect"]
    assert got["rescue_types"][int(Graha.SATURN)] == want["rescue_ithasala"]
    assert got["rescued"] is True
    assert got["present_as_worked"] is True
    assert got["houses"] == want["owns"] == (10, 11)


def test_the_pair_is_an_opposition_and_a_poorna():
    base = yogas.ithasala(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                          faster_longitude=199.0, slower_longitude=20.0)
    assert base["house_from_faster"] == 7
    assert base["aspect"] == "Opposition"
    assert base["separation_from_exact"] == pytest.approx(1.0)
    assert base["type"] == "Poorna"


def test_the_rescue_leg_is_venus_to_saturn():
    """Ar to Pi is the 12th and Pi to Ar the 2nd — a semi-sextile either way,
    which is what the example calls it.
    """
    leg = yogas.ithasala(faster=int(Graha.VENUS), slower=int(Graha.SATURN),
                         faster_longitude=348.0, slower_longitude=20.0)
    assert leg["house_from_faster"] == 2
    assert leg["aspect"] == "Semi-sextile aspect"
    assert leg["separation_from_exact"] == pytest.approx(2.0)
    assert leg["binding_deeptamsa"] == 7.0
    assert leg["type"] == "Vartamaana"


def test_the_rule_wants_two_weak_planets_and_the_example_shows_one():
    """Mars at 19 Li is not debilitated, not in an enemy's rasi and has no
    bala given. OI-171.
    """
    from hora.core.constants.graha import DEBILITATION_RASI

    mars = yogas._duttota_side(int(Graha.MARS), 199.0, None)
    assert int(DEBILITATION_RASI[int(Graha.MARS)]) == 3          # Cancer
    assert mars["debilitated"] is False
    assert mars["relation_to_the_rasi_lord"] == "sama"
    assert mars["inimical_rasi"] is False
    assert mars["weak"] is False

    got = yogas.duttota(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                        faster_longitude=199.0, slower_longitude=20.0,
                        rescuer=int(Graha.VENUS), rescuer_longitude=348.0)
    assert got["both_weak"] is False
    assert got["any_weak"] is True
    assert got["present_as_worded"] is False
    assert got["present_as_worked"] is True
    assert got["readings_agree"] is False
    assert got["undecided"] == (
        yogas.THE_RULE_WANTS_TWO_WEAK_PLANETS_AND_THE_EXAMPLE_SHOWS_ONE)


def test_saturn_is_weak_on_two_of_the_three_tests():
    """The book names the debilitation. Aries is also Mars's rasi, and Mars is
    Saturn's enemy, so the inimical test fires too.
    """
    from hora.core.constants.graha import (
        NATURAL_RELATION,
        NATURAL_RELATION_NAMES,
    )

    assert NATURAL_RELATION_NAMES[
        NATURAL_RELATION[int(Graha.SATURN)][int(Graha.MARS)]] == "satru"
    saturn = yogas._duttota_side(int(Graha.SATURN), 20.0, None)
    assert saturn["weak_by"] == ("debilitated", "inimical_rasi")
    assert yogas.DUTTOTA_EXAMPLE["weak_because"] == "debilitated"


def test_both_weak_satisfies_the_rule_as_worded():
    """Put Mars in Gemini, Mercury's rasi and Mars's enemy's."""
    from hora.core.constants.graha import (
        NATURAL_RELATION,
        NATURAL_RELATION_NAMES,
    )

    assert NATURAL_RELATION_NAMES[
        NATURAL_RELATION[int(Graha.MARS)][int(Graha.MERCURY)]] == "satru"
    got = yogas.duttota(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                        faster_longitude=60.0 + 19.0, slower_longitude=20.0,
                        rescuer=int(Graha.VENUS), rescuer_longitude=348.0)
    assert got["faster_side"]["inimical_rasi"] is True
    assert got["both_weak"] is True
    assert got["present_as_worded"] is True
    assert got["readings_agree"] is True


def test_the_two_sections_define_weak_differently():
    """Only debilitation is on both lists."""
    radda_tests = {str(row["trigger"]) for row in yogas.RADDA_TRIGGERS}
    assert radda_tests == {"debilitation", "retrogression", "combustion",
                           "otherwise weak"}
    duttota_tests = set(yogas.DUTTOTA_WEAK_TESTS)
    assert "retrogression" not in duttota_tests
    assert "inimical rasi" not in radda_tests
    assert "Only debilitation is on both lists" in (
        yogas.THE_TWO_SECTIONS_DEFINE_WEAK_DIFFERENTLY)

    # A retrograde Mercury in his own Virgo is a radda trigger and duttota
    # calls him strong — the two sections disagree about the same planet.
    retro = yogas._duttota_side(int(Graha.MERCURY), 150.0 + 15.0, None)
    assert retro["weak"] is False
    assert retro["own_rasi"] is True and retro["strong"] is True
    negated = yogas.radda(faster=int(Graha.MERCURY), slower=int(Graha.SATURN),
                          faster_longitude=150.0 + 15.0,
                          slower_longitude=210.0 + 20.0,
                          faster_retrograde=True)
    assert negated["parties"][int(Graha.MERCURY)]["triggers"] == ("retrograde",)


def test_duttota_restores_what_radda_destroyed():
    """The chapter's first restoring yoga, and the example runs the chain."""
    pair = {"faster": int(Graha.MARS), "slower": int(Graha.SATURN),
            "faster_longitude": 199.0, "slower_longitude": 20.0}
    stands = yogas.ithasala(**pair)
    assert stands["type"] == "Poorna"

    destroyed = yogas.radda(**pair, lagna_rasi=0)
    assert destroyed["negates_the_ithasala"] is True
    assert destroyed["destroys_houses"] == (10, 11)

    restored = yogas.duttota(**pair, rescuer=int(Graha.VENUS),
                             rescuer_longitude=348.0, lagna_rasi=0)
    assert restored["present_as_worked"] is True
    assert restored["houses"] == (10, 11)
    assert "Duttota restores" in yogas.DUTTOTA_IS_THE_FIRST_RESTORING_YOGA


def test_the_same_houses_carry_the_opposite_result():
    """§29.2.11 read Saturn's 10th and 11th as damaged; §29.2.13 reads them as
    promised, from the same lagna and the same ownership.
    """
    assert yogas.RADDA_EXAMPLES[1]["owns"] == yogas.DUTTOTA_EXAMPLE["owns"]
    assert yogas.RADDA_EXAMPLES[1]["lagna_rasi"] == (
        yogas.DUTTOTA_EXAMPLE["lagna_rasi"]) == "Ar"
    assert "career and material gains promised" in (
        yogas.THE_SAME_HOUSES_CARRY_THE_OPPOSITE_RESULT)


def test_high_and_good_are_read_the_same_way():
    """§29.2.12 said "good", §29.2.13 says "high", and neither is a band."""
    strong = yogas._duttota_side(int(Graha.MARS), 199.0, 12.0)
    assert strong["bala_grade"] == "strong"
    assert strong["high_bala"] is True
    middling = yogas._duttota_side(int(Graha.MARS), 199.0, 7.0)
    assert middling["high_bala"] is False
    assert middling["low_bala"] is False
    assert "both are read as the strong band or better" in (
        yogas.HIGH_AND_GOOD_ARE_THE_SAME_UNNAMED_BAND)


def test_a_weak_rescuer_rescues_nothing():
    """Move Venus out of Pisces and the yoga fails."""
    got = yogas.duttota(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                        faster_longitude=199.0, slower_longitude=20.0,
                        rescuer=int(Graha.VENUS),
                        rescuer_longitude=300.0 + 18.0)
    assert got["strong_side"]["strong"] is False
    assert got["rescued"] is False
    assert got["present_as_worked"] is False


def test_the_rescuer_must_reach_one_of_the_pair():
    """Exalted Venus with no ithasala to either planet does nothing."""
    got = yogas.duttota(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                        faster_longitude=199.0, slower_longitude=20.0,
                        rescuer=int(Graha.VENUS),
                        rescuer_longitude=330.0 + 28.0)
    assert got["strong_side"]["exalted"] is True
    assert got["reaches"] == ()
    assert got["rescued"] is False


def test_the_rescuer_must_be_a_third_planet():
    with pytest.raises(yogas.TajakaYogaError, match="third planet"):
        yogas.duttota(faster=int(Graha.MARS), slower=int(Graha.SATURN),
                      faster_longitude=199.0, slower_longitude=20.0,
                      rescuer=int(Graha.MARS), rescuer_longitude=199.0)


# --------------------------------------------------------------------------
# §29.2.14 Thambira yoga
# --------------------------------------------------------------------------


def test_the_thambira_rule_is_transcribed():
    assert "in the last degree of a rasi" in yogas.THAMBIRA_RULE
    assert "after moving to the next rasi with a slower moving planet" in (
        yogas.THAMBIRA_RULE)
    assert yogas.THAMBIRA_RESULTS in yogas.THAMBIRA_RULE


def test_the_thambira_example_reproduces():
    """Aries lagna. Venus 29 Ta 10 has a square and no ithasala with Mars
    2 Le, and a sextile vartamaana once he enters Gemini.
    """
    want = yogas.THAMBIRA_EXAMPLE
    got = yogas.thambira(
        mover=int(Graha.VENUS),
        mover_longitude=float(want["mover_longitude"]),
        other=int(Graha.MARS), other_longitude=float(want["other_longitude"]),
        lagna_rasi=0)
    assert got["mover_in_last_degree"] is True
    assert got["aspect_now"] == want["aspect_now"]
    assert got["ithasala_now"] is want["ithasala_now"]
    assert got["aspect_after_moving"] == want["aspect_after"]
    assert got["ithasala_after_moving"] == want["ithasala_after"]
    assert got["other_is_slower"] is True
    assert got["present"] is True


def test_the_mover_enters_gemini():
    from hora.core.const import RASI_ABBR

    got = yogas.thambira(mover=int(Graha.VENUS),
                         mover_longitude=30.0 + 29.0 + 10.0 / 60.0,
                         other=int(Graha.MARS), other_longitude=122.0)
    assert RASI_ABBR[got["mover_enters"]] == yogas.THAMBIRA_EXAMPLE[
        "mover_enters"]


def test_the_result_is_again_read_off_the_houses_owned():
    """Venus owns the 2nd and 7th from Aries: family and marital life."""
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    for house in (2, 7):
        assert str(GRAHA_NAMES[int(RASI_LORD[(0 + house - 1) % 12])]) == "Venus"
    got = yogas.thambira(mover=int(Graha.VENUS),
                         mover_longitude=30.0 + 29.0 + 10.0 / 60.0,
                         other=int(Graha.MARS), other_longitude=122.0,
                         lagna_rasi=0)
    assert got["houses"] == yogas.THAMBIRA_EXAMPLE["owns"] == (2, 7)
    assert "family and marital life" in str(yogas.THAMBIRA_EXAMPLE["shows"])
    assert "Four sections running" in (
        yogas.THE_RESULT_IS_AGAIN_READ_OFF_THE_HOUSES_OWNED)


def test_the_slower_condition_is_forced_by_the_crossing():
    """At 0° the mover is behind every planet, so it can only be the faster
    party — which makes the other planet the slower one by construction.
    """
    random.seed(2141)
    for _ in range(1500):
        mover, other = random.sample(range(7), 2)
        got = yogas.thambira(
            mover=mover, mover_longitude=random.randrange(12) * 30.0 + 29.5,
            other=other, other_longitude=random.uniform(0, 360))
        if not got["other_is_slower"]:
            # A faster other planet can never give the crossing an ithasala.
            assert got["ithasala_after_moving"] is None
            assert got["present"] is False
    assert "has to be the slower one" in (
        yogas.THE_SLOWER_CONDITION_IS_FORCED_BY_THE_CROSSING)


def test_a_mover_not_in_the_last_degree_gives_no_thambira():
    got = yogas.thambira(mover=int(Graha.VENUS), mover_longitude=30.0 + 20.0,
                         other=int(Graha.MARS), other_longitude=122.0)
    assert got["mover_in_last_degree"] is False
    assert got["present"] is False


def test_an_ithasala_that_already_exists_is_not_a_thambira():
    """The yoga is one in waiting: it needs there to be nothing yet."""
    got = yogas.thambira(mover=int(Graha.VENUS), mover_longitude=90.0 + 29.5,
                         other=int(Graha.MARS), other_longitude=210.0 + 29.8)
    if got["ithasala_now"] is not None:
        assert got["present"] is False


def test_the_crossing_must_actually_produce_an_ithasala():
    """Move Mars to a rasi Venus will not aspect from Gemini — the 6th, Sc."""
    got = yogas.thambira(mover=int(Graha.VENUS),
                         mover_longitude=30.0 + 29.0 + 10.0 / 60.0,
                         other=int(Graha.MARS), other_longitude=210.0 + 2.0)
    assert got["aspect_after_moving"] is None
    assert got["ithasala_after_moving"] is None
    assert got["present"] is False


def test_every_gairi_kamboola_crossing_satisfies_thambiras_speed_condition():
    """The Moon is faster than every graha, so the planet she reaches is
    always slower — which is exactly what §29.2.14 asks.
    """
    for other in range(7):
        if other == int(Graha.MOON):
            continue
        got = yogas.thambira(mover=int(Graha.MOON), mover_longitude=179.5,
                             other=other, other_longitude=95.0)
        assert got["other_is_slower"] is True
    assert "Only the Moon can make a gairi-kamboola" in (
        yogas.EVERY_GAIRI_KAMBOOLA_IS_ALSO_A_THAMBIRA)


def test_the_gairi_kamboola_example_is_also_a_thambira():
    """§29.2.9's Moon at 29 Vi 10 reaching Mars at 1 Cp on entering Libra."""
    want = yogas.GAIRI_KAMBOOLA_EXAMPLE
    got = yogas.thambira(
        mover=int(Graha.MOON), mover_longitude=float(want["moon_longitude"]),
        other=int(Graha.MARS),
        other_longitude=float(want["faster_longitude"]))
    assert got["ithasala_now"] is None
    assert got["ithasala_after_moving"] == "Poorna"
    assert got["present"] is True


def test_thambira_drops_every_condition_gairi_kamboola_added():
    """A dignified mover is refused by §29.2.9 and accepted by §29.2.14."""
    exalted_moon = 30.0 + 29.5                     # Taurus, the Moon exalted
    refused = yogas.moon_is_disqualified(exalted_moon)
    assert refused["exalted"] is True

    got = yogas.thambira(mover=int(Graha.MOON), mover_longitude=exalted_moon,
                         other=int(Graha.SATURN), other_longitude=120.0 + 2.0)
    assert got["mover_in_last_degree"] is True
    assert got["ithasala_after_moving"] is not None
    assert got["present"] is True
    assert "no dignity test" in (
        yogas.THAMBIRA_IS_GAIRI_KAMBOOLA_WITHOUT_THE_CONDITIONS)


def test_thambira_needs_two_different_rankable_grahas():
    with pytest.raises(yogas.TajakaYogaError, match="two different grahas"):
        yogas.thambira(mover=int(Graha.VENUS), mover_longitude=59.5,
                       other=int(Graha.VENUS), other_longitude=122.0)
    with pytest.raises(yogas.TajakaYogaError, match="cannot rank"):
        yogas.thambira(mover=int(Graha.RAHU), mover_longitude=59.5,
                       other=int(Graha.KETU), other_longitude=122.0)


# --------------------------------------------------------------------------
# §29.2.15 Kutta yoga
# --------------------------------------------------------------------------


def test_the_kutta_rule_and_its_footnote_are_transcribed():
    assert "a planet occupying lagna is aspected by" in yogas.KUTTA_RULE
    # "in occupying own or exaltation rasi", kept as printed.
    assert "by a planet in occupying own or exaltation rasi" in yogas.KUTTA_RULE
    assert "in a kendra or a panaphara" in yogas.KUTTA_RULE
    assert yogas.KUTTA_FOOTNOTE == (
        "This yoga was interpreted differently by scholars.")


def test_the_kutta_example_reproduces():
    """Taurus lagna, Sun 21 Ta, Mercury 16 Vi in the 5th."""
    want = yogas.KUTTA_EXAMPLE
    got = yogas.kutta(
        lagna_rasi=1, in_lagna=int(Graha.SUN),
        in_lagna_longitude=float(want["in_lagna_longitude"]),
        aspecting=int(Graha.MERCURY),
        aspecting_longitude=float(want["aspecting_longitude"]))
    assert got["is_in_lagna"] is True
    assert got["aspecting_house"] == want["aspecting_house"]
    assert got["aspecting_house_class"] == want["aspecting_house_class"]
    assert got["exalted"] is True
    assert got["aspect"] == want["aspect"]
    assert got["present"] is True
    assert got["houses"] == want["owns"] == (4,)


def test_the_example_needs_28_2s_aspects_and_fails_under_graha_drishti():
    """Vi to Ta is the 9th, a trinal. Mercury's graha drishti reaches only
    the 7th, Pisces.
    """
    from hora.charts.aspects import graha_drishti_houses
    from hora.tajaka.aspects import aspect_on_house

    assert aspect_on_house(9)["name"] == "Trinal aspect"
    reached = [(5 + h - 1) % 12 for h in graha_drishti_houses(int(Graha.MERCURY))]
    assert reached == [11]                       # Pisces only
    assert 1 not in reached                      # not Taurus
    assert "the example would not form" in (
        yogas.GRAHA_DRISHTI_WOULD_GIVE_NO_YOGA_HERE)


def test_virgo_is_both_mercurys_own_and_his_exaltation():
    """And he is the only graha for which the two coincide, so the one worked
    case cannot separate the rule's disjunction.
    """
    from hora.core.const import RASI_LORD
    from hora.core.constants.graha import EXALTATION_RASI

    both = [g for g in range(7)
            if int(RASI_LORD[int(EXALTATION_RASI[g])]) == g]
    assert both == [int(Graha.MERCURY)]

    got = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                      in_lagna_longitude=51.0, aspecting=int(Graha.MERCURY),
                      aspecting_longitude=166.0)
    assert got["own_rasi"] is True and got["exalted"] is True
    assert yogas.KUTTA_EXAMPLE["aspecting_dignity"] == ("own rasi",
                                                       "exaltation")
    assert "the only graha for which the two are the same" in (
        yogas.MERCURY_IN_VIRGO_IS_BOTH_AND_ONLY_MERCURY_IS)


def test_either_half_of_the_dignity_alone_is_enough():
    """The rule is a disjunction even though its example cannot show it."""
    # Venus in his own Libra, the 6th from Taurus — an apoklima, so no yoga,
    # but the dignity holds on its own.
    own_only = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                           in_lagna_longitude=51.0, aspecting=int(Graha.VENUS),
                           aspecting_longitude=180.0 + 16.0)
    assert own_only["own_rasi"] is True and own_only["exalted"] is False
    assert own_only["dignified"] is True

    # The Sun exalted in Aries, which is not his own rasi.
    exalted_only = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.MOON),
                               in_lagna_longitude=51.0,
                               aspecting=int(Graha.SUN),
                               aspecting_longitude=10.0)
    assert exalted_only["exalted"] is True and exalted_only["own_rasi"] is False
    assert exalted_only["dignified"] is True


def test_an_apoklima_gives_no_kutta():
    """A kendra or a panaphara only — the same eight houses as ishkavala's."""
    from hora.core.constants.house import APOKLIMA, KENDRA, PANAPHARA

    assert sorted(KENDRA + PANAPHARA) == [1, 2, 4, 5, 7, 8, 10, 11]
    assert len(KENDRA + PANAPHARA) == 8
    allowed = set(KENDRA + PANAPHARA)
    assert allowed == set(range(1, 13)) - set(APOKLIMA)
    assert yogas.ishkavala(list(allowed))["present"] is True
    assert "section 29.2.1 requires every planet to occupy" in (
        yogas.THE_SAME_EIGHT_HOUSES_AS_ISHKAVALA)

    # Jupiter exalted in Cancer is the 3rd from Taurus, an apoklima.
    got = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                      in_lagna_longitude=51.0, aspecting=int(Graha.JUPITER),
                      aspecting_longitude=90.0 + 16.0)
    assert got["exalted"] is True
    assert got["aspecting_house_class"] == "apoklima"
    assert got["in_a_kendra_or_panaphara"] is False
    assert got["present"] is False


def test_the_planet_must_actually_be_in_the_lagna():
    got = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                      in_lagna_longitude=60.0 + 21.0,
                      aspecting=int(Graha.MERCURY), aspecting_longitude=166.0)
    assert got["is_in_lagna"] is False
    assert got["present"] is False


def test_the_sixth_and_eighth_leave_the_lagna_unaspected():
    """§28.2 gives them no aspect, so a dignified planet there gives nothing.
    """
    # Saturn in his own Aquarius is the 10th from Taurus, a kendra, and Aq to
    # Ta is the 4th — an aspect. Move him to his own Capricorn, the 9th, an
    # apoklima; then use Mars exalted in Capricorn instead for the 6th/8th.
    got = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                      in_lagna_longitude=51.0, aspecting=int(Graha.SATURN),
                      aspecting_longitude=300.0 + 16.0)
    assert got["aspecting_house"] == 10
    assert got["own_rasi"] is True
    assert got["aspect"] is not None
    assert got["present"] is True


def test_the_matters_are_the_houses_the_lagna_planet_owns():
    """Fifth section running. The Sun owns the 4th from Taurus."""
    from hora.core.const import GRAHA_NAMES, RASI_LORD

    assert str(GRAHA_NAMES[int(RASI_LORD[(1 + 4 - 1) % 12])]) == "Sun"
    got = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                      in_lagna_longitude=51.0, aspecting=int(Graha.MERCURY),
                      aspecting_longitude=166.0)
    assert got["houses"] == (4,)
    assert "4th house matters" in str(yogas.KUTTA_EXAMPLE["shows"])
    assert "Five sections running" in (
        yogas.SIGNIFIED_MATTERS_ARE_THE_HOUSES_OWNED_AGAIN)


def test_kutta_is_the_first_yoga_since_29_2_2_without_an_ithasala():
    """Its result mentions no ithasala and neither does its rule."""
    assert "ithasala" not in yogas.KUTTA_RULE
    for rule in (yogas.EESARPHA_RULE, yogas.NAKTA_RULE, yogas.YAMAYA_RULE,
                 yogas.MANAHOO_RULE, yogas.KAMBOOLA_RULE,
                 yogas.GAIRI_KAMBOOLA_RULE, yogas.KHALLASARA_RULE,
                 yogas.RADDA_RULE, yogas.DUHPHALI_KUTTA_RULE,
                 yogas.DUTTOTA_RULE, yogas.THAMBIRA_RULE):
        assert "ithasala" in rule.lower()
    assert "Kutta needs none" in (
        yogas.KUTTA_IS_THE_FIRST_YOGA_SINCE_29_2_2_WITHOUT_AN_ITHASALA)


def test_a_dignified_planet_in_lagna_satisfies_the_rule_against_itself():
    """The 1st is a kendra and §28.2 makes the 1st a conjunction. OI-172."""
    got = yogas.kutta(lagna_rasi=5, in_lagna=int(Graha.MERCURY),
                      in_lagna_longitude=166.0, aspecting=int(Graha.MERCURY),
                      aspecting_longitude=166.0)
    assert got["is_in_lagna"] is True
    assert got["aspecting_house"] == 1
    assert got["aspecting_house_class"] == "kendra"
    assert got["aspect"] == "Conjunction"
    assert got["aspecting_is_the_lagna_planet"] is True
    assert got["self_aspect_undecided"] is not None
    assert "does not say whether that counts" in (
        yogas.A_PLANET_IN_LAGNA_COULD_ASPECT_ITSELF)


def test_the_book_marks_this_yoga_contested_and_says_no_more():
    """Footnote 84 is the only such mark in §29.2 and carries no content."""
    assert "interpreted differently by scholars" in yogas.KUTTA_FOOTNOTE
    assert "gives neither the other interpretations" in (
        yogas.THE_BOOK_MARKS_THIS_YOGA_CONTESTED_AND_SAYS_NO_MORE)
    got = yogas.kutta(lagna_rasi=1, in_lagna=int(Graha.SUN),
                      in_lagna_longitude=51.0, aspecting=int(Graha.MERCURY),
                      aspecting_longitude=166.0)
    assert got["footnote"] == yogas.KUTTA_FOOTNOTE
