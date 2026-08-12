# CP31 800 — Main Concepts

Study reference for the seven 800-rated solutions in this folder.

## Overview

| Problem | File | Core idea | Key technique |
|---------|------|-----------|---------------|
| Q1 | [q1.py](q1.py) | Can the array be sorted? | Linear scan + case split on `k` |
| Q2 | [q2.py](q2.py) | Min fuel for a round trip | Greedy max over segments |
| Q3 | [q3.py](q3.py) | Min water placements | Substring pattern + count |
| Q4 | [q4.py](q4.py) | Who wins the game? | Modulo / game theory |
| Q5 | [q5.py](q5.py) | Valid array check | Single-element condition |
| Q6 | [q6.py](q6.py) | Can the array be rearranged to "good"? | Frequency counting + math |
| Q7 | [q7.py](q7.py) | Min appends until substring appears | Bounded search + string ops |

---

## Concepts by topic

### A. Array basics

- Linear traversal to check a property:
  - [q1.py](q1.py): walk the array and test if it is already sorted
  - [q5.py](q5.py): only the first element matters (`arr[0] == 1`)
- Early exit on the first violation (`break` when unsorted)

### B. Greedy / max-over-segments

In [q2.py](q2.py), the minimum tank size is the max of:

1. Distance from start to the first gas station
2. Gaps between consecutive stations
3. Round-trip distance from the last station to the end (`× 2` for the U-turn)

Edge case: no gas stations → answer is `end * 2`.

### C. String patterns

- [q3.py](q3.py): `'...' in string` detects a special configuration (the middle cell can auto-fill via neighbors, so answer collapses to `2`)
- [q7.py](q7.py): `str_s in curr` for substring search; check character-set feasibility before searching

### D. Counting and frequency

- [q3.py](q3.py): `string.count('.')` when there is no special `'...'` pattern
- [q6.py](q6.py): `Counter` for number of distinct values and their frequencies

### E. Mathematical characterization (avoid brute force)

**[q6.py](q6.py)** — a "good" array with `n ≥ 3` must alternate (`a, b, a, b, ...`):

| Case | Answer |
|------|--------|
| 1 distinct | Always Yes |
| 3+ distinct | Always No |
| 2 distinct, `n == 2` | Always Yes |
| 2 distinct, `n ≥ 3` | Yes iff `|count(a) - count(b)| ≤ 1` |

**[q4.py](q4.py)** — game outcome from modulo:

- `n % 3 == 0` → Second wins
- otherwise → First wins

### F. Bounded iteration (avoid TLE)

In [q7.py](q7.py):

- Each operation appends `x` to itself (length doubles: `n → 2n → 4n → ...`)
- Under the constraint `n · m ≤ 25`, the max answer is **5** ops (worst case `n = 1`, `m = 25`)
- Cap the loop (`for ops in range(6)`), then return `-1`
- Never use an unbounded `while` without an exit condition

### G. Input / output patterns (shared)

- Multi-test-case template: read `t`, then loop and parse each case
- Common pitfalls:
  - `n = int(input().strip())`, not `n = map(int, ...)`
  - Use `.strip()` on string inputs so newlines do not break comparisons

---

## Per-problem summaries

### Q1 — Array sorting check

- **Type:** Implementation / case split
- **Decision:** If the array is already sorted, or `k > 1`, answer is `YES`; otherwise `NO`
- **Core logic:**

```python
if isSorted or k > 1:
    return "YES"
return "NO"
```

- **Pitfall:** With `k == 1`, you cannot freely reverse segments, so an unsorted array is impossible

### Q2 — Gas stations / min fuel

- **Type:** Greedy
- **Decision:** Answer is the maximum of start→first gap, consecutive gaps, and `(end - last) * 2`
- **Core logic:**

```python
min_fuel = max(gas_stations[0], end - gas_stations[-1]) * ...  # plus consecutive gaps
```

- **Pitfall:** Forgetting the U-turn doubles the last segment

### Q3 — Water cells

- **Type:** String / observation
- **Decision:** If `'...'` appears, answer is `2`; else answer is the number of `'.'` cells
- **Core logic:**

```python
if '...' in string:
    return 2
return string.count('.')
```

- **Pitfall:** Overthinking simulation of action 2; the pattern observation is enough

### Q4 — Game (mod 3)

- **Type:** Math / game theory
- **Decision:** Second wins iff `n` is divisible by 3
- **Core logic:**

```python
return 'Second' if target_int % 3 == 0 else 'First'
```

- **Pitfall:** Do not simulate the full game when a closed form exists

### Q5 — First element check

- **Type:** Implementation
- **Decision:** Valid iff `arr[0] == 1`
- **Core logic:**

```python
return 'NO' if arr[0] != 1 else 'YES'
```

- **Pitfall:** Input parsing — ensure `n` is an `int`, not a `map` object

### Q6 — Good array after rearrangement

- **Type:** Counting / math
- **Decision:** Use distinct-count and frequency rules above (do not enumerate permutations)
- **Core logic:**

```python
c1, c2 = counts.values()
return 'Yes' if abs(c1 - c2) <= 1 else 'No'
```

- **Pitfall:** Rotations are not all rearrangements. `[1,1,2,2]` has a good permutation `1,2,1,2` that no rotation reaches — characterize with counts instead

### Q7 — Don't Try to Count (append until substring)

- **Type:** String / bounded search
- **Decision:** If any character of `s` is missing from `x`, return `-1`. Otherwise double `x` up to 5 times and check `s in curr`
- **Core logic:**

```python
for ops in range(6):
    if str_s in curr:
        return ops
    curr = curr + curr
return -1
```

- **Pitfall:** An unbounded `while` on impossible cases causes TLE. Cap ops from constraints (`n · m ≤ 25` → max answer 5)

---

## Cross-cutting lessons

Patterns to remember at 800 level:

1. **Check impossibility first** — q7 character set, q6 distinct count ≥ 3
2. **Characterize instead of simulate** — q6 frequency rules beat trying all rotations; q4 modulo beats game simulation
3. **Bound your loops from constraints** — q7 uses `range(6)`, not infinite doubling
4. **Watch off-by-one** — substring index loops need `range(len - m + 1)`, not `range(len - m)`
5. **Use efficient string building** — prefer `orig * factor` (or a few `curr + curr` doubles) over `+=` inside a large loop

---

## Quick skill checklist

After finishing these problems, you should be comfortable with:

- [ ] Scanning arrays for sortedness / local conditions
- [ ] Greedy "max gap" reasoning on a line
- [ ] String membership (`in`) and `count`
- [ ] `Counter` / frequency arguments
- [ ] Modulo-based game outcomes
- [ ] Deriving loop bounds from `n · m`-style constraints
- [ ] Multi-test-case I/O without type bugs
