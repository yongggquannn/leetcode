"""
Conversation History and Context Compaction (Sierra)

Implement the three stages of a chat-agent conversation workflow.

Suggested time: 45 min.

STAGE 1: Retrieve the full conversation
---------------------------------------
The cursor-paginated endpoint returns up to five messages per page:

    fetch_page(conversation_id, *, next_cursor=None) -> {
        "messages": [{"token_count": int, "property_ids": [...]}, ...],
        "next_cursor": str | None,
    }

Fetch every page in order until `next_cursor` is absent or None. Preserve
message order and duplicates. A repeated cursor should fail clearly instead
of looping forever.

STAGE 2: Compact by token count
-------------------------------
- Sum `token_count` across the current messages.
- If the total exceeds 20_000, call the supplied compactor repeatedly until
  the total is below 10_000.
- Record one event per compaction with stage, before count, and after count.

STAGE 3: Compact by unique properties
-------------------------------------
- Count distinct property IDs present in message `property_ids` fields.
- If the count exceeds 20, compact repeatedly until it is at most 10.
- Record one event per compaction, with stage and before/after unique counts.

The compactor takes the current messages and one keyword target at a time,
then returns the new messages:

    compact(messages, *, target_tokens=None, target_properties=None) -> messages

The context object owns the current messages and accumulated events. The
compaction functions return the events; callers do not need a compacted thread
as their result. Treat a compaction that makes no progress as an error.

EXAMPLES
--------
Stage 1: the next cursor from the first response is passed to the second call.

    fetch_page("c-7", next_cursor=None)
      -> {"messages": [{"id": "m1"}, {"id": "m2"}], "next_cursor": "p2"}
    fetch_page("c-7", next_cursor="p2")
      -> {"messages": [{"id": "m3"}], "next_cursor": None}
    retrieve_conversation(..., "c-7") -> [m1, m2, m3]

Stage 2: two messages total 24,000 tokens. The compactor returns a 9,000-token
summary message, so one compaction event is recorded:

    context.messages = [
        {"id": "m1", "token_count": 12_000},
        {"id": "m2", "token_count": 12_000},
    ]
    compact(messages, target_tokens=9_999)
      -> [{"id": "summary", "token_count": 9_000}]
    compact_by_tokens(context, compact)
      -> [{"stage": 2, "before_tokens": 24_000, "after_tokens": 9_000}]

Stage 3: 21 distinct property IDs exceed the limit. The compactor keeps 10;
one event is recorded. (The property IDs shown here stand in for IDs extracted
from property-search tool results.)

    context.messages = [{"id": "search", "property_ids": list(range(1, 22))}]
    compact(messages, target_properties=10)
      -> [{"id": "search_summary", "property_ids": list(range(1, 11))}]
    compact_by_unique_properties(context, compact)
      -> [{"stage": 3, "before_properties": 21, "after_properties": 10}]

FOLLOW-UPS
- How do you handle endpoint errors, timeouts, and rate limiting?
- What should happen if compaction cannot meet its target?
- In production, how would compaction preserve important booking constraints
  while dropping stale search results?
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ConversationContext:
    messages: list[dict[str, Any]] = field(default_factory=list)
    compaction_events: list[dict[str, Any]] = field(default_factory=list)


"""
Stage 1: the next cursor from the first response is passed to the second call.

    fetch_page("c-7", next_cursor=None)
      -> {"messages": [{"id": "m1"}, {"id": "m2"}], "next_cursor": "p2"}
    fetch_page("c-7", next_cursor="p2")
      -> {"messages": [{"id": "m3"}], "next_cursor": None}
    retrieve_conversation(..., "c-7") -> [m1, m2, m3]
"""

def retrieve_conversation(
    fetch_page: Callable[..., dict[str, Any]], conversation_id: str
) -> list[dict[str, Any]]:

    res = []
    cursor = None

    while True:
        payload = fetch_page(conversation_id, next_cursor=cursor)
        messages_list = payload['messages']
        for message in messages_list:
            res.append(message['id'])
        cursor = payload['next_cursor']
        if cursor == None:
            return res

"""
- Sum `token_count` across the current messages.
- If the total exceeds 20_000, call the supplied compactor repeatedly until
  the total is below 10_000.
- Record one event per compaction with stage, before count, and after count.

Stage 2: two messages total 24,000 tokens. The compactor returns a 9,000-token
summary message, so one compaction event is recorded:

    context.messages = [
        {"id": "m1", "token_count": 12_000},
        {"id": "m2", "token_count": 12_000},
    ]
    compact(messages, target_tokens=9_999)
      -> [{"id": "summary", "token_count": 9_000}]
    compact_by_tokens(context, compact)
      -> [{"stage": 2, "before_tokens": 24_000, "after_tokens": 9_000}]
"""

def compact_by_tokens(
    context: ConversationContext,
    compact: Callable[..., list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    # Helper function to sum total count tokens
    def total_count(messages):
        res = 0
        for message in messages:
            res += message['token_count']
        return res

    initial_token_count = total_count(context.messages)
    while initial_token_count > 20000:
        updated_messages = compact(context.messages, target_tokens=9999)
        after_token_count = total_count(updated_messages)

        context.messages = updated_messages
        context.compaction_events.append({
                      "stage": 2,
                      "before_tokens": initial_token_count,
                      "after_tokens": after_token_count,
        })
    return context.compaction_events


def compact_by_unique_properties(
    context: ConversationContext,
    compact: Callable[..., list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    raise NotImplementedError
