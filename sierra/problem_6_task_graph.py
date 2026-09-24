"""
Task Dependency Graph (Sierra)
Reported pattern for the Sierra coding screen: "graph or tree traversal to find
paths or connected node sets", "cycle detection in linked structures". Framed
here as an agent-workflow / build pipeline, which is how Sierra would phrase it.
Source: https://www.tryexponent.com/guides/sierra-agent-engineer-interview

Suggested time: 50 min.    Run: python sierra/run.py 6

tasks: dict[str, list[str]]  -  task -> the tasks it depends on

    tasks = {"a": [], "b": [], "c": ["a"], "d": ["a", "b"], "e": ["c", "d"]}

================================================================================
PART 1: build_order(tasks) -> list[str]
================================================================================

- Every task appears after all of its dependencies.
- When several tasks are ready, take the alphabetically smallest (deterministic).
- A dependency that isn't a key in `tasks` -> UnknownDependencyError(task, dep).

    build_order(tasks) -> ["a", "b", "c", "d", "e"]

================================================================================
PART 2: Cycles
================================================================================

- If there is a cycle, raise CycleError. err.cycle is one cycle as a path that
  starts and ends on the same task, following "depends on" edges:
      {"a": ["b"], "b": ["c"], "c": ["a"], "d": ["a"]}  ->  e.g. ["a","b","c","a"]
  Tasks that merely depend on the cycle ("d") are not part of it.

================================================================================
PART 3: min_completion_time(tasks, durations) -> int
================================================================================

Unlimited parallel workers; a task starts when all its deps finish.
Missing or negative duration -> ValueError.

    durations = {"a": 3, "b": 2, "c": 1, "d": 4, "e": 2}
    min_completion_time(tasks, durations) -> 9     (b/a -> d -> e)

================================================================================
PART 4: affected_by(tasks, changed) -> list[str]
================================================================================

Every task that (transitively) depends on `changed`, excluding it, in build
order - i.e. what must be re-run after `changed` is modified.
Unknown task -> ValueError.

    affected_by(tasks, "a") -> ["c", "d", "e"]
    affected_by(tasks, "b") -> ["d", "e"]

================================================================================
PART 5: schedule(tasks, durations, workers) -> ScheduleResult
================================================================================

Now only `workers` tasks can run at once. At each moment, first finish every
task ending at that time, then start ready tasks (alphabetical) while a worker
is free. workers < 1 -> ValueError.

    schedule(tasks, durations, 2) -> makespan 9,  starts {a:0, b:0, c:3, d:3, e:7}
    schedule(tasks, durations, 1) -> makespan 12

================================================================================
FOLLOW-UPS
================================================================================

- Kahn's algorithm vs DFS three-colour: when would you pick each?
- Why is Part 5 greedy not always optimal? (scheduling is NP-hard in general)
- A task fails mid-run: what do you retry, what do you skip?
- The graph is 10M nodes in a DB: how do you find affected tasks?
"""
from __future__ import annotations

from dataclasses import dataclass, field


class UnknownDependencyError(ValueError):
    def __init__(self, task: str, dependency: str):
        super().__init__(f"{task!r} depends on unknown task {dependency!r}")
        self.task = task
        self.dependency = dependency


class CycleError(ValueError):
    def __init__(self, cycle: list[str]):
        super().__init__("cycle: " + " -> ".join(cycle))
        self.cycle = cycle


@dataclass
class ScheduleResult:
    makespan: int
    starts: dict[str, int] = field(default_factory=dict)


def build_order(tasks: dict[str, list[str]]) -> list[str]:
    raise NotImplementedError


def min_completion_time(tasks: dict[str, list[str]], durations: dict[str, int]) -> int:
    raise NotImplementedError


def affected_by(tasks: dict[str, list[str]], changed: str) -> list[str]:
    raise NotImplementedError


def schedule(tasks: dict[str, list[str]], durations: dict[str, int], workers: int) -> ScheduleResult:
    raise NotImplementedError
