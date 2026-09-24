from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Message:
    role: str  # "user" | "assistant" | "tool"
    content: str
    tool_name: str | None = None
    data: dict | None = None


@dataclass
class ConversationState:
    history: list[Message] = field(default_factory=list)
    verified_email: str | None = None
    failed_verifications: int = 0
    escalated: bool = False
