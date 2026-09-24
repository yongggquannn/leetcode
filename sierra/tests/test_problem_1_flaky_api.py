from _harness import load

m = load("problem_1_flaky_api")


def _flaky(failures, value=42, exc=None):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise (exc or m.TransientError("boom"))
        return value

    return fn, state


def _product(pid):
    return {"id": pid, "name": f"Product {pid}", "price_cents": 1000}


# ---- Part 1
def test_part1_succeeds_first_try():
    sleeps = []
    fn, state = _flaky(0)
    assert m.call_with_retry(fn, sleep=sleeps.append) == 42
    assert sleeps == [] and state["calls"] == 1


def test_part1_retries_with_backoff():
    sleeps = []
    fn, _ = _flaky(2)
    assert m.call_with_retry(fn, base_delay=0.1, sleep=sleeps.append) == 42
    assert sleeps == [0.1, 0.2], sleeps


def test_part1_caps_delay_and_raises_chained():
    sleeps = []
    fn, state = _flaky(99)
    try:
        m.call_with_retry(fn, max_attempts=5, base_delay=0.5, max_delay=1.0, sleep=sleeps.append)
    except m.RetryExhaustedError as err:
        assert err.attempts == 5
        assert isinstance(err.__cause__, m.TransientError), "chain the last error with `from`"
    else:
        raise AssertionError("expected RetryExhaustedError")
    assert sleeps == [0.5, 1.0, 1.0, 1.0], f"no sleep after last attempt; got {sleeps}"
    assert state["calls"] == 5


# ---- Part 2
def test_part2_permanent_error_not_retried():
    sleeps = []
    fn, state = _flaky(99, exc=m.ProductNotFound("p1"))
    try:
        m.call_with_retry(fn, sleep=sleeps.append)
    except m.PermanentError:
        pass
    else:
        raise AssertionError("expected PermanentError to propagate")
    assert state["calls"] == 1 and sleeps == []


def test_part2_bug_not_retried():
    sleeps = []
    fn, state = _flaky(99, exc=KeyError("oops"))
    try:
        m.call_with_retry(fn, sleep=sleeps.append)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError to propagate")
    assert state["calls"] == 1


def test_part2_invalid_max_attempts():
    fn, _ = _flaky(0)
    try:
        m.call_with_retry(fn, max_attempts=0, sleep=lambda s: None)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


# ---- Part 3
def test_part3_resolves_ids_and_fallbacks():
    listings = [
        {"id": "p1", "fallback_ids": []},
        {"id": "p2", "fallback_ids": ["p20", "p21"]},
        {"id": "p3", "fallback_ids": []},
        {"id": "p4", "fallback_ids": ["p1"]},
    ]
    products = {pid: _product(pid) for pid in ["p1", "p21", "p4"]}
    api = m.FakeProductAPI(listings, products, flaky={"p4": 2}, list_failures=1)
    result = m.resolve_catalog(api, sleep=lambda s: None)
    assert [p["id"] for p in result.products] == ["p1", "p21", "p4"], result.products
    assert result.unresolved == ["p3"]


def test_part3_exhausted_candidate_falls_back():
    listings = [{"id": "p5", "fallback_ids": ["p6"]}]
    api = m.FakeProductAPI(listings, {"p5": _product("p5"), "p6": _product("p6")}, flaky={"p5": 99})
    result = m.resolve_catalog(api, sleep=lambda s: None)
    assert [p["id"] for p in result.products] == ["p6"]
    assert result.unresolved == []


def test_part3_list_exhausted_raises():
    api = m.FakeProductAPI([], {}, list_failures=99)
    try:
        m.resolve_catalog(api, sleep=lambda s: None)
    except m.RetryExhaustedError:
        return
    raise AssertionError("expected RetryExhaustedError when list_products never succeeds")


# ---- Part 4
def test_part4_follows_redirects():
    listings = [{"id": "p1", "fallback_ids": []}]
    products = {"p1": {"id": "p1", "moved_to": "p7"}, "p7": {"id": "p7", "moved_to": "p8"}, "p8": _product("p8")}
    result = m.resolve_catalog(m.FakeProductAPI(listings, products), sleep=lambda s: None)
    assert [p["id"] for p in result.products] == ["p8"]


def test_part4_redirect_cycle_falls_back():
    listings = [{"id": "a", "fallback_ids": ["c"]}]
    products = {"a": {"id": "a", "moved_to": "b"}, "b": {"id": "b", "moved_to": "a"}, "c": _product("c")}
    result = m.resolve_catalog(m.FakeProductAPI(listings, products), sleep=lambda s: None)
    assert [p["id"] for p in result.products] == ["c"]


def test_part4_each_id_fetched_once():
    listings = [
        {"id": "x1", "fallback_ids": ["gone", "shared"]},
        {"id": "x2", "fallback_ids": ["gone", "shared"]},
        {"id": "x3", "fallback_ids": ["gone", "shared"]},
    ]
    api = m.FakeProductAPI(listings, {"shared": _product("shared")})
    result = m.resolve_catalog(api, sleep=lambda s: None)
    assert len(result.products) == 3
    assert api.calls["shared"] == 1, f"shared fetched {api.calls['shared']} times"
    assert api.calls["gone"] == 1, "cache misses (404s) too"
