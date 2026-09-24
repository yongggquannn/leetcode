import json

from _harness import load

m = load("problem_8_cancellation_flow")

EMAIL = "sam@example.com"


def _flow(plan="annual", price=120_000, days=100):
    return m.CancellationFlow(m.Subscription(EMAIL, plan, price, days))


def _drive(flow, *events):
    for e in events:
        reply = flow.handle(e)
        assert isinstance(reply, str) and reply, f"empty reply for {e}"
    return flow


START = {"type": "start"}
VERIFY = {"type": "verify", "email": EMAIL}


# ---- Part 1
def test_part1_happy_path_without_offer():
    f = _flow()
    _drive(f, START)
    assert f.state == "VERIFY"
    _drive(f, {"type": "verify", "email": "  Sam@Example.COM "})
    assert f.state == "REASON"
    _drive(f, {"type": "reason", "reason": "missing_feature"})
    assert f.state == "CONFIRM"
    _drive(f, {"type": "confirm"})
    assert f.state == "CANCELLED"


def test_part1_wrong_email_stays():
    f = _drive(_flow(), START, {"type": "verify", "email": "lee@example.com"})
    assert f.state == "VERIFY"


def test_part1_abort_keeps_plan():
    f = _drive(_flow(), START, VERIFY, {"type": "reason", "reason": "other"}, {"type": "abort"})
    assert f.state == "RETAINED" and f.applied_offer is None


# ---- Part 2
def test_part2_discount_offer_accepted():
    f = _drive(_flow(), START, VERIFY, {"type": "reason", "reason": "too_expensive"})
    assert f.state == "OFFER"
    _drive(f, {"type": "accept"})
    assert f.state == "RETAINED"
    assert f.applied_offer == {"kind": "discount", "percent": 50, "months": 3}


def test_part2_pause_offer_declined():
    f = _drive(_flow(), START, VERIFY, {"type": "reason", "reason": "not_using"})
    assert f.state == "OFFER"
    _drive(f, {"type": "decline"}, {"type": "confirm"})
    assert f.state == "CANCELLED" and f.applied_offer is None


def test_part2_human_anytime():
    for prefix in [[], [START], [START, VERIFY]]:
        f = _drive(_flow(), *prefix, {"type": "human"})
        assert f.state == "ESCALATED", prefix


# ---- Part 3
def test_part3_invalid_input_keeps_state():
    f = _drive(_flow(), START, VERIFY)
    _drive(f, {"type": "confirm"})
    assert f.state == "REASON"
    _drive(f, {"type": "reason", "reason": "bored"})
    assert f.state == "REASON"
    _drive(f, {})
    assert f.state == "ESCALATED", "3rd invalid input escalates"


def test_part3_failed_verification_counts():
    f = _drive(_flow(), START)
    for _ in range(2):
        _drive(f, {"type": "verify", "email": "nope@example.com"})
    assert f.state == "VERIFY"
    _drive(f, {"type": "dance"})
    assert f.state == "ESCALATED"


def test_part3_terminal_is_closed():
    f = _drive(_flow(), START, VERIFY, {"type": "reason", "reason": "other"}, {"type": "confirm"})
    audit_len = len(f.audit)
    _drive(f, {"type": "human"}, {"type": "start"}, {"type": "nonsense"})
    assert f.state == "CANCELLED" and len(f.audit) == audit_len


def test_part3_refunds():
    cases = [("monthly", 2_000, 10, 0), ("annual", 120_000, 10, 120_000), ("annual", 120_000, 30, 120_000),
             ("annual", 120_000, 100, 87_123), ("annual", 120_000, 400, 0)]
    for plan, price, days, expected in cases:
        f = _flow(plan, price, days)
        _drive(f, START, VERIFY, {"type": "reason", "reason": "other"})
        assert f.refund_cents is None, "no refund before cancelling"
        _drive(f, {"type": "confirm"})
        assert f.refund_cents == expected, (plan, days, f.refund_cents)


# ---- Part 4
def test_part4_audit_log():
    f = _drive(_flow(), START, {"type": "verify", "email": "x@example.com"}, VERIFY,
               {"type": "reason", "reason": "too_expensive"}, {"type": "decline"}, {"type": "confirm"})
    assert f.audit == [
        ("START", "VERIFY", "start"),
        ("VERIFY", "REASON", "verify"),
        ("REASON", "OFFER", "reason"),
        ("OFFER", "CONFIRM", "decline"),
        ("CONFIRM", "CANCELLED", "confirm"),
    ], f.audit


def test_part4_resume_after_serialise():
    sub = m.Subscription(EMAIL, "annual", 120_000, 100)
    f = _drive(m.CancellationFlow(sub), START, {"type": "bogus"}, VERIFY, {"type": "reason", "reason": "not_using"})
    data = json.loads(json.dumps(f.to_dict()))
    restored = m.CancellationFlow.from_dict(sub, data)
    assert restored.state == "OFFER"
    assert restored.audit == f.audit
    _drive(restored, {"type": "accept"})
    assert restored.state == "RETAINED"
    assert restored.applied_offer == {"kind": "pause", "months": 2}


def test_part4_resume_keeps_invalid_count():
    sub = m.Subscription(EMAIL, "monthly", 2_000, 5)
    f = _drive(m.CancellationFlow(sub), START, {"type": "bogus"}, {"type": "bogus"})
    restored = m.CancellationFlow.from_dict(sub, json.loads(json.dumps(f.to_dict())))
    _drive(restored, {"type": "bogus"})
    assert restored.state == "ESCALATED"
