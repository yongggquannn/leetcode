from __future__ import annotations

import json
from datetime import date

from .db import OrderDB
from .llm import FakeLLM, Reply, ToolCall
from .state import ConversationState, Message
from .tools import TOOLS, ToolContext, escalate_to_human

MAX_STEPS = 5
HANDOFF = "I'm having trouble with this, so I've passed you to a human agent."


class Agent:
    def __init__(self, db: OrderDB, today: date, llm: FakeLLM | None = None):
        self.db = db
        self.today = today
        self.llm = llm or FakeLLM()
        self.state = ConversationState()

    def handle(self, user_text: str) -> str:
        state = self.state
        state.history.append(Message("user", user_text))
        ctx = ToolContext(self.db, state, self.today)
        for _ in range(MAX_STEPS):
            action = self.llm.decide(state.history)
            if isinstance(action, Reply):
                state.history.append(Message("assistant", action.text))
                return action.text
            result = self._run_tool(action, ctx)
            # Fix 1: every tool result goes back to the model, not just errors.
            state.history.append(Message("tool", json.dumps(result), tool_name=action.name, data=result))
        escalate_to_human(ctx, "max_steps")
        state.history.append(Message("assistant", HANDOFF))
        return HANDOFF

    def _run_tool(self, call: ToolCall, ctx: ToolContext) -> dict:
        tool = TOOLS.get(call.name)
        if tool is None:
            return {"error": "UNKNOWN_TOOL"}
        if tool.requires_auth and ctx.state.verified_email is None:  # Fix 2: honour the tool's flag
            return {"error": "AUTH_REQUIRED"}
        return tool.fn(ctx, **call.args)
