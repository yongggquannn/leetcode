"""
Worker Task Assignment (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/f5cf12aa-aa83-48a2-8bb1-01881596c4cd

Public detail is SPARSE. The title and Stripe's interview style suggest a
load-balancing / job-scheduling problem similar to:
    - Assign N tasks to K workers minimizing max load.
    - Round-robin / least-loaded assignment with arrival times.
    - Tasks have durations; output schedule per worker.

================================================================================
PART 1: Minimize Makespan (offline greedy)
================================================================================

Given a list of tasks (each with a duration) and K workers, assign tasks to
workers to minimize the makespan (max total time across workers).

Function:
    assign_tasks_part1(tasks: list[int], k: int) -> list[list[int]]
        # returns list of K lists; each inner list = task INDICES for that worker

Greedy approach: sort tasks descending; assign next task to least-loaded worker.

Example:
    tasks = [5, 3, 8, 2, 7, 4]      # task 0 = duration 5, task 1 = 3, ...
    k = 2

    Sorted desc by duration: indices [2(8), 4(7), 0(5), 5(4), 1(3), 3(2)]
    Greedy assignment trace:
        worker0=[], worker1=[]                        loads (0, 0)
        take 2 (8) -> worker0=[2]                      loads (8, 0)
        take 4 (7) -> worker1=[4]                      loads (8, 7)
        take 0 (5) -> worker1=[4,0]                    loads (8, 12)
        take 5 (4) -> worker0=[2,5]                    loads (12, 12)
        take 1 (3) -> worker0=[2,5,1]                  loads (15, 12)
        take 3 (2) -> worker1=[4,0,3]                  loads (15, 14)

    assign_tasks_part1([5,3,8,2,7,4], 2) ==
        [[2, 5, 1], [4, 0, 3]]      # makespan = max(15, 14) = 15

Edge cases:
    assign_tasks_part1([], 3)       == [[], [], []]
    assign_tasks_part1([10], 3)     == [[0], [], []]   # one worker only

================================================================================
PART 2: Online / arrival-ordered assignment
================================================================================

Tasks arrive in order; assign each immediately to the least-loaded worker
(no reordering allowed).

Function:
    assign_tasks_part2(tasks: list[int], k: int) -> list[list[int]]

Example:
    assign_tasks_part2([5, 3, 8, 2, 7, 4], 2)
    Trace:
        task 0 (5) -> worker 0           (0, 0) -> (5, 0)
        task 1 (3) -> worker 1           (5, 0) -> (5, 3)
        task 2 (8) -> worker 1           (5, 3) -> (5, 11)
        task 3 (2) -> worker 0           (5, 11) -> (7, 11)
        task 4 (7) -> worker 0           (7, 11) -> (14, 11)
        task 5 (4) -> worker 1           (14, 11) -> (14, 15)
    Result: [[0, 3, 4], [1, 2, 5]]       # makespan = 15

================================================================================
PART 3: Heterogeneous workers (speed multipliers)
================================================================================

Each worker has a speed multiplier; effective time = duration / speed.

Function:
    assign_tasks_part3(tasks: list[int], speeds: list[float]) -> list[list[int]]

Example:
    tasks = [10, 10, 10, 10]
    speeds = [1.0, 2.0]              # worker1 is twice as fast

    Greedy by current effective load:
        task 0 -> worker0 (load 10.0); worker1 effective load 0
        task 1 -> worker1 (5.0)
        task 2 -> worker1 (10.0)
        task 3 -> worker0 (20.0) ... wait, after task 2 loads are (10, 10);
                                     ties broken by lowest index -> worker0
                                     -> (20, 10)

    A correct greedy gives roughly:
        assign_tasks_part3([10,10,10,10], [1.0, 2.0])
            == [[0, 3], [1, 2]]      # loads = (20.0, 10.0). Makespan 20.

Confirm exact tie-breaking + objective with the DarkInterview source.
"""


def assign_tasks_part1(tasks: list[int], k: int) -> list[list[int]]:
    pass


def assign_tasks_part2(*args, **kwargs):
    pass


def assign_tasks_part3(*args, **kwargs):
    pass


if __name__ == "__main__":
    pass
