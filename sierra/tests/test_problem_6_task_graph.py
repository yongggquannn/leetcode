from _harness import load

m = load("problem_6_task_graph")

TASKS = {"a": [], "b": [], "c": ["a"], "d": ["a", "b"], "e": ["c", "d"]}
DURATIONS = {"a": 3, "b": 2, "c": 1, "d": 4, "e": 2}


def _raises(exc_type, fn):
    try:
        fn()
    except exc_type as err:
        return err
    raise AssertionError(f"expected {exc_type.__name__}")


# ---- Part 1
def test_part1_example():
    assert m.build_order(TASKS) == ["a", "b", "c", "d", "e"]


def test_part1_alphabetical_ties_and_empty():
    assert m.build_order({"b": [], "a": [], "c": []}) == ["a", "b", "c"]
    assert m.build_order({"z": [], "y": ["z"], "x": ["z"]}) == ["z", "x", "y"]
    assert m.build_order({}) == []


def test_part1_duplicate_deps():
    assert m.build_order({"a": [], "b": ["a", "a"]}) == ["a", "b"]


def test_part1_unknown_dependency():
    err = _raises(m.UnknownDependencyError, lambda: m.build_order({"a": ["ghost"]}))
    assert (err.task, err.dependency) == ("a", "ghost")


# ---- Part 2
def test_part2_cycle_reported():
    tasks = {"a": ["b"], "b": ["c"], "c": ["a"], "d": ["a"]}
    err = _raises(m.CycleError, lambda: m.build_order(tasks))
    cycle = err.cycle
    assert cycle[0] == cycle[-1], cycle
    assert set(cycle[:-1]) == {"a", "b", "c"}, f"'d' only depends on the cycle: {cycle}"
    for task, dep in zip(cycle, cycle[1:]):
        assert dep in tasks[task], f"{task} does not depend on {dep}"


def test_part2_self_loop():
    err = _raises(m.CycleError, lambda: m.build_order({"a": ["a"]}))
    assert err.cycle == ["a", "a"]


# ---- Part 3
def test_part3_critical_path():
    assert m.min_completion_time(TASKS, DURATIONS) == 9
    assert m.min_completion_time({"x": []}, {"x": 5}) == 5


def test_part3_bad_durations():
    _raises(ValueError, lambda: m.min_completion_time(TASKS, {"a": 1}))
    _raises(ValueError, lambda: m.min_completion_time({"a": []}, {"a": -1}))


# ---- Part 4
def test_part4_affected():
    assert m.affected_by(TASKS, "a") == ["c", "d", "e"]
    assert m.affected_by(TASKS, "b") == ["d", "e"]
    assert m.affected_by(TASKS, "e") == []
    _raises(ValueError, lambda: m.affected_by(TASKS, "zzz"))


# ---- Part 5
def test_part5_two_workers():
    result = m.schedule(TASKS, DURATIONS, 2)
    assert result.makespan == 9
    assert result.starts == {"a": 0, "b": 0, "c": 3, "d": 3, "e": 7}, result.starts


def test_part5_one_worker():
    result = m.schedule(TASKS, DURATIONS, 1)
    assert result.makespan == 12
    assert result.starts == {"a": 0, "b": 3, "c": 5, "d": 6, "e": 10}, result.starts


def test_part5_finish_before_start_at_same_time():
    tasks = {"a": [], "z": [], "b": ["a"]}
    result = m.schedule(tasks, {"a": 1, "z": 1, "b": 1}, 1)
    # t=1: a finishes, then both b and z are ready -> b (alphabetical) goes first.
    assert result.starts == {"a": 0, "b": 1, "z": 2}, result.starts


def test_part5_invalid_workers():
    _raises(ValueError, lambda: m.schedule(TASKS, DURATIONS, 0))
