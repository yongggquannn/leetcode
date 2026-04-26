"""
Factory Cost Optimizer (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/c039a7f2-d3d5-4190-8624-46786b99ee5a

Public detail is SPARSE. The title hints at an optimization problem over
factories with per-unit costs / capacities. Common Stripe-style framings:

================================================================================
DATA SHAPE (assumed - confirm with source)
================================================================================

factories = [
    {"id": "F1", "capacity": <int>, "unit_cost": <int>, "fixed_cost": <int>},
    ...
]

================================================================================
PART 1: Greedy (unlimited capacity, no fixed cost)
================================================================================

All factories have unlimited capacity, fixed_cost is ignored. Pick the cheapest
unit_cost factory and produce all `demand` units there.

Function:
    optimize_part1(factories: list[dict], demand: int) -> int

Example:
    factories = [
        {"id": "F1", "unit_cost": 5},
        {"id": "F2", "unit_cost": 3},   # cheapest
        {"id": "F3", "unit_cost": 7},
    ]
    optimize_part1(factories, 100) == 300        # 100 * 3

================================================================================
PART 2: Capacity Limits
================================================================================

Each factory has a hard capacity. Sort by unit_cost ascending and fill
greedily until demand is met. Return total cost. Return -1 if total capacity
< demand.

Example:
    factories = [
        {"id": "F1", "capacity": 30, "unit_cost": 5},
        {"id": "F2", "capacity": 40, "unit_cost": 3},
        {"id": "F3", "capacity": 50, "unit_cost": 7},
    ]
    demand = 100

    Greedy: F2 (40 @ 3) = 120; F1 (30 @ 5) = 150; F3 (30 @ 7) = 210
    optimize_part2(factories, 100) == 480

    optimize_part2(factories, 200) == -1         # total capacity = 120 < 200

================================================================================
PART 3: Fixed (Setup) Costs
================================================================================

Each factory also has a fixed_cost paid once if it produces ANY units. Now
the choice of which factories to OPEN matters; this is the
capacitated-facility-location problem (NP-hard in general; small K -> brute
force over 2^K subsets, or DP).

Function:
    optimize_part3(factories: list[dict], demand: int) -> int

Example:
    factories = [
        {"id": "F1", "capacity": 30, "unit_cost": 5, "fixed_cost": 10},
        {"id": "F2", "capacity": 40, "unit_cost": 3, "fixed_cost": 200},
        {"id": "F3", "capacity": 50, "unit_cost": 7, "fixed_cost": 20},
    ]
    demand = 60

    Subsets that can meet demand=60:
        {F1, F2}: cap 70.  Use 40 from F2 + 20 from F1 = 200 + 10 + 120 + 100
                            = 430
        {F1, F3}: cap 80.  Use 30 from F1 + 30 from F3 = 10 + 20 + 150 + 210
                            = 390
        {F2, F3}: cap 90.  Use 40 from F2 + 20 from F3 = 200 + 20 + 120 + 140
                            = 480
        {F1, F2, F3}: even more fixed cost overhead.
        {F3}: cap 50 < 60 -> infeasible.

    optimize_part3(factories, 60) == 390         # open {F1, F3}
"""


def optimize_part1(factories: list[dict], demand: int) -> int:
    pass


def optimize_part2(factories: list[dict], demand: int) -> int:
    pass


def optimize_part3(factories: list[dict], demand: int) -> int:
    pass


if __name__ == "__main__":
    pass
