"""Reference solution - problem 9."""
from __future__ import annotations

from typing import Any, Callable

from problem_9_conversation_history import ConversationContext


def retrieve_conversation(
    fetch_page: Callable[..., dict[str, Any]], conversation_id: str
) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    cursor: str | None = None
    seen_cursors: set[str] = set()

    while True:
        page = fetch_page(conversation_id, next_cursor=cursor)
        messages.extend(page.get("messages", []))
        next_cursor = page.get("next_cursor")
        if next_cursor is None:
            return messages
        if next_cursor in seen_cursors:
            raise ValueError(f"endpoint repeated cursor: {next_cursor!r}")
        seen_cursors.add(next_cursor)
        cursor = next_cursor


def _token_total(messages: list[dict[str, Any]]) -> int:
    return sum(message.get("token_count", 0) for message in messages)


def _property_ids(messages: list[dict[str, Any]]) -> set[Any]:
    return {
        property_id
        for message in messages
        for property_id in message.get("property_ids", [])
    }


def compact_by_tokens(
    context: ConversationContext,
    compact: Callable[..., list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    while (before := _token_total(context.messages)) > 20_000:
        context.messages = compact(context.messages, target_tokens=9_999)
        after = _token_total(context.messages)
        if after >= before:
            raise ValueError("token compaction did not reduce the token count")
        context.compaction_events.append(
            {"stage": 2, "before_tokens": before, "after_tokens": after}
        )
    return context.compaction_events


def compact_by_unique_properties(
    context: ConversationContext,
    compact: Callable[..., list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    while (before := len(_property_ids(context.messages))) > 20:
        context.messages = compact(context.messages, target_properties=10)
        after = len(_property_ids(context.messages))
        if after >= before:
            raise ValueError("property compaction did not reduce the unique count")
        context.compaction_events.append(
            {"stage": 3, "before_properties": before, "after_properties": after}
        )
    return context.compaction_events
