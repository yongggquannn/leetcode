import random

from _harness import load

m = load("problem_4_first_unique")


def _brute_windows(items, k):
    out = []
    for end in range(k - 1, len(items)):
        window = items[end - k + 1 : end + 1]
        out.append(next((x for x in window if window.count(x) == 1), None))
    return out


# ---- Part 1
def test_part1_examples():
    assert m.first_unique_index("leetcode") == 0
    assert m.first_unique_index("loveleetcode") == 2
    assert m.first_unique_index("aabb") == -1
    assert m.first_unique_index("") == -1
    assert m.first_unique_index("z") == 0


# ---- Part 2
def test_part2_stream():
    t = m.FirstUniqueTracker()
    assert t.first_unique() is None
    t.add("u1")
    t.add("u2")
    assert t.first_unique() == "u1"
    t.add("u1")
    assert t.first_unique() == "u2"
    t.add("u2")
    assert t.first_unique() is None
    t.add("u3")
    t.add("u1")
    assert t.first_unique() == "u3", "a repeated item never becomes unique again"


def test_part2_hashable_items():
    t = m.FirstUniqueTracker()
    for x in [(1, 2), 7, (1, 2), "7"]:
        t.add(x)
    assert t.first_unique() == 7


def test_part2_scales():
    t = m.FirstUniqueTracker()
    for i in range(200_000):
        t.add(i // 2)  # every item appears twice
        t.first_unique()
    t.add("last")
    assert t.first_unique() == "last"


# ---- Part 3
def test_part3_example():
    assert m.first_unique_per_window(["a", "b", "a", "c", "b"], 3) == ["b", "b", "a"]


def test_part3_item_becomes_unique_again():
    items = ["x", "y", "x", "y", "z", "z"]
    assert m.first_unique_per_window(items, 4) == _brute_windows(items, 4)


def test_part3_matches_brute_force():
    rng = random.Random(7)
    for _ in range(200):
        items = [rng.choice("abcd") for _ in range(rng.randint(1, 25))]
        k = rng.randint(1, len(items))
        assert m.first_unique_per_window(items, k) == _brute_windows(items, k), (items, k)


def test_part3_invalid_k():
    try:
        m.first_unique_per_window(["a"], 0)
    except ValueError:
        return
    raise AssertionError("expected ValueError for k <= 0")
