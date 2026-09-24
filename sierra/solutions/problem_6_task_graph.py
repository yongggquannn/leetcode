"""Reference solution - problem 6."""
from __future__ import annotations

import heapq
from collections import defaultdict

from problem_6_task_graph import CycleError, ScheduleResult, UnknownDependencyError


def _dependents(tasks: dict[str, list[str]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for task, deps in tasks.items():
        for dep in deps:
            if dep not in tasks:
                raise UnknownDependencyError(task, dep)
            out[dep].append(task)
    return out


def _find_cycle(tasks: dict[str, list[str]], remaining: set[str]) -> list[str]:
    # Every task left over by Kahn has a leftover dependency, so walking deps must loop.
    node, path, index = min(remaining), [], {}
    while node not in index:
        index[node] = len(path)
        path.append(node)
        node = min(d for d in tasks[node] if d in remaining)
    return path[index[node] :] + [node]


def build_order(tasks: dict[str, list[str]]) -> list[str]:
    dependents = _dependents(tasks)
    indegree = {t: len(set(deps)) for t, deps in tasks.items()}
    ready = [t for t, d in indegree.items() if d == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        task = heapq.heappop(ready)
        order.append(task)
        for nxt in set(dependents[task]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(ready, nxt)
    if len(order) != len(tasks):
        raise CycleError(_find_cycle(tasks, set(tasks) - set(order)))
    return order


def _check_durations(tasks: dict[str, list[str]], durations: dict[str, int]) -> None:
    for t in tasks:
        if t not in durations or durations[t] < 0:
            raise ValueError(f"missing or negative duration for {t!r}")


def min_completion_time(tasks: dict[str, list[str]], durations: dict[str, int]) -> int:
    _check_durations(tasks, durations)
    finish: dict[str, int] = {}
    for task in build_order(tasks):
        finish[task] = durations[task] + max((finish[d] for d in tasks[task]), default=0)
    return max(finish.values(), default=0)


def affected_by(tasks: dict[str, list[str]], changed: str) -> list[str]:
    if changed not in tasks:
        raise ValueError(f"unknown task {changed!r}")
    dependents = _dependents(tasks)
    seen, stack = set(), [changed]
    while stack:
        for nxt in dependents[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return [t for t in build_order(tasks) if t in seen]


def schedule(tasks: dict[str, list[str]], durations: dict[str, int], workers: int) -> ScheduleResult:
    if workers < 1:
        raise ValueError("workers must be >= 1")
    _check_durations(tasks, durations)
    build_order(tasks)  # validates unknown deps and cycles up front
    dependents = _dependents(tasks)
    indegree = {t: len(set(deps)) for t, deps in tasks.items()}
    ready = sorted(t for t, d in indegree.items() if d == 0)
    running: list[tuple[int, str]] = []
    result = ScheduleResult(makespan=0)
    now = 0
    while ready or running:
        while ready and len(running) < workers:
            task = heapq.heappop(ready)
            result.starts[task] = now
            heapq.heappush(running, (now + durations[task], task))
        now = running[0][0]
        while running and running[0][0] == now:
            _, done = heapq.heappop(running)
            for nxt in set(dependents[done]):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    heapq.heappush(ready, nxt)
    result.makespan = now
    return result
