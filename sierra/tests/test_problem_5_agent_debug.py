from datetime import date

from _harness import load

m = load("problem_5_agent_debug")

TODAY = date(2026, 3, 31)


def _agent(verified=False):
    agent = m.Agent(m.demo_db(TODAY), today=TODAY)
    if verified:
        agent.handle("Hi, my email is sam@example.com")
    return agent


def test_part0_greeting():
    assert "order" in _agent().handle("hello").lower()


def test_part1_verify_then_status():
    agent = _agent()
    reply = agent.handle("Hi, my email is sam@example.com")
    assert "verified" in reply.lower(), reply
    reply = agent.handle("Where is order #1001?")
    assert "shipped" in reply, reply
    assert not agent.state.escalated, "a simple lookup should not escalate"


def test_part2_unverified_lookup_blocked():
    reply = _agent().handle("Where is order #1001?")
    assert "shipped" not in reply, f"leaked order status to an unverified user: {reply}"
    assert "verify" in reply.lower(), reply


def test_part3_other_customers_order_hidden():
    agent = _agent(verified=True)
    reply = agent.handle("Where is order #2001?")
    assert "delivered" not in reply, f"leaked another customer's order: {reply}"
    assert "couldn't find" in reply, reply


def test_part4_refund_limit_in_cents():
    agent = _agent(verified=True)
    reply = agent.handle("Please refund order #1003")
    assert "150.00" in reply, reply
    assert agent.db.refunds == [("1003", 150_00)]
    reply = agent.handle("Please refund order #1004")
    assert "specialist" in reply, reply
    assert agent.db.refunds == [("1003", 150_00)]
    assert agent.db.escalations == ["over_limit"], agent.db.escalations


def test_part5_refund_window_inclusive():
    agent = _agent(verified=True)
    agent.handle("refund order #1002 please")
    assert agent.db.refunds == [("1002", 40_00)], "day 30 is inside the window"
    agent.handle("refund order #1005 please")
    assert agent.db.escalations == ["outside_window"], agent.db.escalations


def test_part6_no_double_refund():
    agent = _agent(verified=True)
    agent.handle("Please refund order #1003")
    reply = agent.handle("Please refund order #1003 again")
    assert agent.db.refunds == [("1003", 150_00)], f"refunded twice: {agent.db.refunds}"
    assert "already" in reply, reply


def test_part7_escalate_after_failed_verification():
    agent = _agent()
    reply = agent.handle("my email is who@example.com")
    assert "doesn't match" in reply, reply
    assert not agent.state.escalated
    reply = agent.handle("sorry, it's who2@example.com")
    assert agent.state.escalated, "2nd failed verification must escalate"
    assert "human" in reply, reply
    assert agent.db.escalations == ["verification_failed"], agent.db.escalations
