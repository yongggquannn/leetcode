# ThoughtWorks SWE Grad — Practice Bank

ThoughtWorks' loop is **not** LeetCode. It's a craft interview. The people scoring you are developers who live in Kent Beck / Martin Fowler / Uncle Bob territory, and they will notice whether you wrote a test first.

Companion docs: [stripe_oa_prep_cheatsheet.md](stripe_oa_prep_cheatsheet.md) (Python stdlib), [stripe_screen_practice_bank.md](stripe_screen_practice_bank.md) (live OOD structure).

---

## 1. The loop (what to prepare for each round)

| # | Round | Length | Focus | Signal they want |
|---|-------|--------|-------|------------------|
| 1 | **HackerRank OA** | 75 min, 4 problems | DS/algo + one OOD-flavoured | Correctness + clean structure. 3/4 full solves is a typical advance threshold. |
| 2 | **Code Pairing** (the big one) | 60–90 min | TDD, OOD, refactoring | How you **think and collaborate**, not just whether you finish. Often two interviewers — one leaves mid-interview and the replacement asks you to onboard them. |
| 3 | **Technical Interview** | ~60 min | Past projects, architecture, language/OS/networking fundamentals, tree/graph coding | Depth on your own work + breadth on fundamentals. |
| 4 | **Cultural Fit** | 45 min | Behavioural, values alignment | TW is very opinionated on values (equity, social justice, craft). Don't wing this one. |

Sources: [targetjobs pairing guide](https://targetjobs.co.uk/careers-advice/information-technology/thoughtworks-pair-programming-interview-insider-advice), [TW own blog — "what to expect"](https://www.thoughtworks.com/insights/blog/what-expect-pair-programming-interview), [TW blog — "how to excel"](https://www.thoughtworks.com/insights/blog/careers-at-thoughtworks/how-to-excel-in-thoughtworks-interviews), [GFG grad interview experience](https://www.geeksforgeeks.org/interview-experiences/thoughtworks-interview-experience-graduate-application-developer-role/), [Glassdoor TW grad](https://www.glassdoor.co.uk/Interview/Thoughtworks-Graduate-Software-Developer-Interview-Questions-EI_IE38334.0,12_KO13,40.htm), [InterviewQuery TW guide](https://www.interviewquery.com/interview-queries/thoughtworks-software-engineer), [Medium — TW interview experience](https://medium.com/@yogeshsharma_50096/thoughtworks-interview-experience-284adb209c26).

---

## 2. What ThoughtWorks actually grades (pairing round)

From their own blog plus candidate write-ups, in priority order:

1. **TDD, visibly.** Write a failing test, run it, make it pass, refactor. No writing implementation first "to sketch it out". They grade this directly.
2. **Domain modelling.** Do your class names match the domain? (A rover is a `Rover`, not a `Grid`. A conference talk is a `Talk`, not a `TalkInfo`.)
3. **SOLID, especially SRP and OCP.** Each class has one reason to change. New requirements ("rover on a toroidal grid") should add classes, not edit existing ones.
4. **Refactoring under pressure.** Halfway through they'll add a requirement. If you panic and paste code, you lose. If you delete a test, write a new one, refactor the model, you win.
5. **Onboarding a fresh listener.** Session 2 starts with a new interviewer. You must re-explain the problem, your model, and your rationale. Practice this verbally — it's the hardest-to-fake skill.
6. **Boundary conditions, packaging, error handling, documentation.** Candidates who pass have `tests/`, a `README`, domain exceptions, and input validation at the boundary.

Anti-signals that get people cut:
- Writing a 200-line procedural `main()` with no classes.
- Using `print` instead of returning values — hard to test.
- Catch-all `except Exception: pass`.
- Skipping tests "because the problem is simple".
- Going silent. This is the biggest single killer.

---

## 3. The TDD loop you must be fluent in

Memorise this cycle. You will run it ~8 times in 90 minutes.

```
RED    → write the smallest test that fails for the right reason. Run it. See the red.
GREEN  → write the minimum code to pass. Ugly is OK. Run the test. See the green.
REFACT → improve names, extract methods, remove duplication. Run tests every ~30s.
         NEVER refactor with a red test. Tests pass before AND after.
COMMIT → (verbal) "I'd commit here." Interviewers love hearing this.
```

Python template you should be able to type in under 60 seconds:

```python
# rover.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    x: int
    y: int

class Rover:
    def __init__(self, position: Position, heading: str = "N") -> None:
        self._position = position
        self._heading = heading

    @property
    def position(self) -> Position:
        return self._position
```

```python
# test_rover.py
import pytest
from rover import Rover, Position

def test_rover_starts_at_given_position() -> None:
    rover = Rover(Position(0, 0))
    assert rover.position == Position(0, 0)
```

Run with `pytest -q`. That's your first RED→GREEN before the interviewer finishes explaining the problem.

---

## 4. Problem 1 — Mars Rover (THE canonical TW problem)

> A squad of rovers is being deployed on a rectangular plateau on Mars. The plateau is a grid; rovers must stay within it. Each rover has a position `(x, y)` and a heading in `{N, E, S, W}`.
>
> Input is two lines per rover. The first gives position and heading, e.g. `1 2 N`. The second is a string of commands from `{L, R, M}`:
> - `L` / `R` — rotate 90° left / right in place
> - `M` — move one grid square in the current heading
>
> Print the final state of each rover on its own line.
>
> Example:
> ```
> 5 5           # plateau upper-right
> 1 2 N
> LMLMLMLMM
> 3 3 E
> MMRMMRMRRM
> ```
> Output:
> ```
> 1 3 N
> 5 1 E
> ```

### Parts (interviewer adds these live)
2. Rover refuses to move out of bounds (silently ignores the `M`, continues processing the rest).
3. Rovers cannot collide. Later rovers refuse moves that would land on another rover.
4. Plateau becomes toroidal (wraps around). Same `Rover`, different `Plateau`.

### TDD plan (order of tests to write)
1. Rover constructed with `(x, y, heading)` exposes position and heading.
2. `L` rotates `N → W`.
3. All 4 rotations of `L` and `R`.
4. `M` with heading `N` increments `y`.
5. `M` for all 4 headings.
6. Full command string applied in order.
7. Grid rejects out-of-bounds move (Part 2).
8. Collision rejection (Part 3).

### Design checklist
- `Rover`, `Plateau`, `Position`, `Heading` (prefer `Enum` over strings).
- `Rover.execute(commands, plateau)` — plateau is passed in, not owned. Enables Part 4 swap.
- Movement vector lookup: `{"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}`.
- Rotations: cycle `["N", "E", "S", "W"]`, `+1` for R, `-1` for L.

### Reference solution

```python
# rover.py
from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum

class Heading(str, Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

_ORDER = [Heading.N, Heading.E, Heading.S, Heading.W]
_DELTA = {Heading.N: (0, 1), Heading.E: (1, 0), Heading.S: (0, -1), Heading.W: (-1, 0)}

@dataclass(frozen=True)
class Position:
    x: int
    y: int

@dataclass(frozen=True)
class Plateau:
    width: int
    height: int

    def contains(self, p: Position) -> bool:
        return 0 <= p.x <= self.width and 0 <= p.y <= self.height

@dataclass(frozen=True)
class Rover:
    position: Position
    heading: Heading

    def turn_left(self) -> "Rover":
        i = _ORDER.index(self.heading)
        return replace(self, heading=_ORDER[(i - 1) % 4])

    def turn_right(self) -> "Rover":
        i = _ORDER.index(self.heading)
        return replace(self, heading=_ORDER[(i + 1) % 4])

    def move(self, plateau: Plateau, occupied: set[Position] | None = None) -> "Rover":
        dx, dy = _DELTA[self.heading]
        new_pos = Position(self.position.x + dx, self.position.y + dy)
        if not plateau.contains(new_pos):
            return self  # ignore out-of-bounds
        if occupied and new_pos in occupied:
            return self  # ignore collision
        return replace(self, position=new_pos)

    def execute(self, commands: str, plateau: Plateau, occupied: set[Position] | None = None) -> "Rover":
        rover = self
        for c in commands:
            if c == "L":
                rover = rover.turn_left()
            elif c == "R":
                rover = rover.turn_right()
            elif c == "M":
                rover = rover.move(plateau, occupied)
            else:
                raise ValueError(f"unknown command: {c!r}")
        return rover
```

```python
# test_rover.py
import pytest
from rover import Rover, Position, Heading, Plateau

PLATEAU = Plateau(5, 5)

def test_rover_turns_left_from_north_to_west():
    r = Rover(Position(2, 2), Heading.N).turn_left()
    assert r.heading == Heading.W

def test_rover_moves_north():
    r = Rover(Position(1, 1), Heading.N).move(PLATEAU)
    assert r.position == Position(1, 2)

def test_rover_ignores_move_out_of_bounds():
    r = Rover(Position(5, 5), Heading.N).move(PLATEAU)
    assert r.position == Position(5, 5)

def test_example_one():
    r = Rover(Position(1, 2), Heading.N).execute("LMLMLMLMM", PLATEAU)
    assert (r.position.x, r.position.y, r.heading.value) == (1, 3, "N")

def test_example_two():
    r = Rover(Position(3, 3), Heading.E).execute("MMRMMRMRRM", PLATEAU)
    assert (r.position.x, r.position.y, r.heading.value) == (5, 1, "E")

def test_collision_refused():
    other = Position(1, 2)
    r = Rover(Position(1, 1), Heading.N).move(PLATEAU, {other})
    assert r.position == Position(1, 1)
```

**Talking points:** "I used an immutable `Rover` — every move returns a new one. That's overkill for a single rover but makes the multi-rover case (Part 3) trivial to reason about; there's no way state accidentally leaks between them."

---

## 5. Problem 2 — Sales Taxes

> Basic sales tax is 10% on all goods except books, food, and medical products (which are exempt). Import duty is an additional 5% on all imported goods, no exemptions.
>
> Round tax up to the nearest 0.05 *per item* (not per line).
>
> Given a shopping basket (list of lines like `"1 book at 12.49"` or `"1 imported bottle of perfume at 27.99"`), print a receipt showing each line, the total taxes, and the total price.

### Parts
2. Add a `TaxPolicy` interface so new tax regimes (e.g. a GST variant) can plug in without changing `Receipt`.
3. Add "bulk discount": every 3rd identical item in one basket is free. Show on receipt.
4. Verbal: how would you localise this to a country with different exempt categories and a different rounding rule?

### TDD plan
1. Parse one line: quantity, description, price.
2. Detect "imported" from description.
3. Classify as book / food / medical / other by keyword list (document this assumption; it's a simplification).
4. Compute tax per item with rounding rule.
5. Format one receipt line.
6. Aggregate multi-line receipt with totals.

### Key trap
The rounding rule is `ceil(x / 0.05) * 0.05` *per item*, not per line. People lose points for rounding the line total. Use `Decimal`, not `float`:

```python
from decimal import Decimal, ROUND_UP

def round_up_to_nickel(amount: Decimal) -> Decimal:
    nickel = Decimal("0.05")
    return (amount / nickel).quantize(Decimal("1"), rounding=ROUND_UP) * nickel
```

### Reference solution (core)

```python
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_UP
import re

NICKEL = Decimal("0.05")
BASE_RATE = Decimal("0.10")
IMPORT_RATE = Decimal("0.05")
EXEMPT_KEYWORDS = {"book", "chocolate", "pill"}  # documented simplification

LINE_RE = re.compile(r"^(\d+)\s+(.*?)\s+at\s+(\d+\.\d{2})$")

@dataclass(frozen=True)
class Item:
    quantity: int
    description: str
    unit_price: Decimal

    @property
    def is_imported(self) -> bool:
        return "imported" in self.description.lower()

    @property
    def is_exempt(self) -> bool:
        d = self.description.lower()
        return any(k in d for k in EXEMPT_KEYWORDS)

def parse_line(line: str) -> Item:
    m = LINE_RE.match(line.strip())
    if not m:
        raise ValueError(f"malformed line: {line!r}")
    qty, desc, price = m.groups()
    return Item(int(qty), desc, Decimal(price))

def round_up_to_nickel(amount: Decimal) -> Decimal:
    return (amount / NICKEL).quantize(Decimal("1"), rounding=ROUND_UP) * NICKEL

def unit_tax(item: Item) -> Decimal:
    rate = Decimal("0")
    if not item.is_exempt:
        rate += BASE_RATE
    if item.is_imported:
        rate += IMPORT_RATE
    return round_up_to_nickel(item.unit_price * rate)

@dataclass(frozen=True)
class ReceiptLine:
    item: Item
    line_total: Decimal  # (unit_price + unit_tax) * qty

def build_receipt(lines: list[str]) -> tuple[list[ReceiptLine], Decimal, Decimal]:
    receipt: list[ReceiptLine] = []
    total_tax = Decimal("0")
    total = Decimal("0")
    for raw in lines:
        item = parse_line(raw)
        tax_per_unit = unit_tax(item)
        line_total = (item.unit_price + tax_per_unit) * item.quantity
        total_tax += tax_per_unit * item.quantity
        total += line_total
        receipt.append(ReceiptLine(item, line_total))
    return receipt, total_tax, total
```

**Talking points:** "`Decimal` not `float`, because 10% of $12.49 is an exactness question the tests will catch. The `EXEMPT_KEYWORDS` list is a known simplification — the real implementation would delegate to a product catalogue. I'd call that out and move on."

---

## 6. Problem 3 — Conference Track Management

> You're organising a conference. Given a list of talks with lengths (5–60 min, or a `lightning` talk of 5 min), schedule them into tracks.
>
> A track is:
> - **Morning session**: starts 9am, must end by 12:00 (180 min).
> - Lunch at 12:00.
> - **Afternoon session**: starts 1pm, ends no earlier than 3pm and no later than 5pm.
> - Networking event at 5pm.
>
> Every talk must be scheduled, no talk overlaps, and the total minutes per session fit the constraints. Minimise the number of tracks (but a greedy fit is accepted).
>
> Input:
> ```
> Writing Fast Tests Against Enterprise Rails 60min
> Overdoing it in Python 45min
> Lua for the Masses 30min
> ...
> Rails Magic 60min
> Ruby on Rails: Why We Should Move On 60min
> Clojure Ain't Afraid of the GIL 55min
> Programming in the Small lightning
> ```
> Output: a printed schedule with times filled in.

### TDD plan
1. Parse one talk line (including `lightning` = 5 min).
2. Sort talks and fit into a fixed-capacity session (classic bin-packing, greedy-first-fit-decreasing is enough).
3. Session with morning/afternoon capacity rules.
4. Track = morning + afternoon.
5. Format output.

### Design notes
- `Talk(title, minutes)` — value object.
- `Session(capacity_minutes, start_time)` — holds talks, tells you remaining capacity.
- `Track(morning, afternoon)` — prints itself.
- `Scheduler` — fills tracks until all talks placed.
- **Don't** build the "optimal" bin-packer. Interviewers explicitly say greedy is fine; they want design, not combinatorics.

### Classic mistake
Putting the `print_schedule` logic inside `Talk`. Formatting is a view concern; keep `Talk` as a value object.

### Skeleton (TDD would fill this in across 60 min)

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import time, timedelta, datetime
import re

LINE_RE = re.compile(r"^(.*?)\s+(\d+)min$|^(.*?)\s+lightning$")

@dataclass(frozen=True)
class Talk:
    title: str
    minutes: int

def parse_talk(line: str) -> Talk:
    m = LINE_RE.match(line.strip())
    if not m:
        raise ValueError(f"malformed: {line!r}")
    if m.group(3):  # lightning branch
        return Talk(m.group(3), 5)
    return Talk(m.group(1), int(m.group(2)))

@dataclass
class Session:
    start: time
    capacity_min: int
    min_fill_min: int = 0  # afternoon has a lower bound
    talks: list[Talk] = field(default_factory=list)

    @property
    def used(self) -> int:
        return sum(t.minutes for t in self.talks)

    def fits(self, talk: Talk) -> bool:
        return self.used + talk.minutes <= self.capacity_min

    def add(self, talk: Talk) -> None:
        if not self.fits(talk):
            raise ValueError("session full")
        self.talks.append(talk)

@dataclass
class Track:
    morning: Session
    afternoon: Session

def schedule(talks: list[Talk]) -> list[Track]:
    # First-fit decreasing over (morning, afternoon) per track.
    remaining = sorted(talks, key=lambda t: -t.minutes)
    tracks: list[Track] = []
    while remaining:
        morning = Session(time(9, 0), 180)
        afternoon = Session(time(13, 0), 240, min_fill_min=120)
        placed: list[Talk] = []
        for t in remaining:
            if morning.fits(t):
                morning.add(t); placed.append(t)
            elif afternoon.fits(t):
                afternoon.add(t); placed.append(t)
        if not placed:
            raise ValueError("cannot schedule — talk larger than any session")
        for t in placed:
            remaining.remove(t)
        tracks.append(Track(morning, afternoon))
    return tracks
```

**Talking points:** "I'm doing first-fit-decreasing. Optimal bin-packing is NP-hard; I'll note that and say if the interviewer wants tighter packing I can add a swap pass, but for a few dozen talks this is always acceptable."

---

## 7. Problem 4 — Bowling Game Kata (the TDD kata TW loves)

> Given an array of rolls for one bowling game (10 frames, each frame up to 2 rolls unless strike/spare), compute the total score. This is Uncle Bob's famous TDD kata.
>
> Scoring: each frame is pins knocked down, plus:
> - **Spare** (10 pins in 2 rolls): bonus = next roll
> - **Strike** (10 pins in 1 roll): bonus = next two rolls
> - 10th frame gets bonus rolls if spare/strike.

### Why interviewers pick this
It's a **design kata**. The naive procedural solution is ugly. A well-refactored one has `Game`, `Frame`, `Roll`. The question tests whether you'll let tests drive you to the clean design or whether you'll overthink it up front.

### TDD plan — literally, in this order
1. `Game().score() == 0` (no rolls).
2. All gutter balls → 0.
3. All ones → 20.
4. One spare + next roll → spare is counted with bonus.
5. One strike + next two rolls → strike counted with bonus.
6. Perfect game → 300.

### Reference solution (after refactoring)

```python
class Game:
    def __init__(self) -> None:
        self._rolls: list[int] = []

    def roll(self, pins: int) -> None:
        self._rolls.append(pins)

    def score(self) -> int:
        total = 0
        i = 0
        for _ in range(10):
            if self._is_strike(i):
                total += 10 + self._rolls[i + 1] + self._rolls[i + 2]
                i += 1
            elif self._is_spare(i):
                total += 10 + self._rolls[i + 2]
                i += 2
            else:
                total += self._rolls[i] + self._rolls[i + 1]
                i += 2
        return total

    def _is_strike(self, i: int) -> bool:
        return self._rolls[i] == 10

    def _is_spare(self, i: int) -> bool:
        return self._rolls[i] + self._rolls[i + 1] == 10
```

```python
def test_gutter_game():
    g = Game()
    for _ in range(20): g.roll(0)
    assert g.score() == 0

def test_all_ones():
    g = Game()
    for _ in range(20): g.roll(1)
    assert g.score() == 20

def test_one_spare():
    g = Game()
    g.roll(5); g.roll(5); g.roll(3)
    for _ in range(17): g.roll(0)
    assert g.score() == 16

def test_perfect_game():
    g = Game()
    for _ in range(12): g.roll(10)
    assert g.score() == 300
```

**Talking points — this one is scripted:** "I'm deliberately NOT modelling `Frame` as a class yet. The tests don't require it. If a new requirement came in — say, printing a scorecard — I'd extract `Frame` then. Premature structure is the main failure mode of this kata."

That line earns real points. TW consultants literally write blog posts about people over-designing the bowling kata.

---

## 8. Problem 5 — Splitwise (modern TW favourite)

> Model a shared-expense app. Users can log expenses split equally or by percentage. The system tracks how much each user owes each other user and supports querying balances.
>
> Required operations:
> - `add_user(user_id, name, email)`
> - `add_expense(payer_id, amount, participants: list[str], split_type: "EQUAL" | "EXACT" | "PERCENT", shares: list[Decimal] | None)`
> - `balance_of(user_id) -> dict[other_id, amount]` — positive = they owe this user; negative = this user owes them.
> - `show_balances()` — printable summary.

### TDD plan
1. User creation, lookup, duplicate rejection.
2. Equal split of 300 among 3 → 100 each.
3. Equal split with remainder (100 among 3) — rule: first N owe 1¢ more.
4. Exact split — validate shares sum to amount.
5. Percent split — validate shares sum to 100.
6. Balance query.
7. Balance simplification (if A owes B and B owes A, net them).

### Design notes
- `User`, `Expense`, `Split` (strategy pattern — `EqualSplit`, `ExactSplit`, `PercentSplit`), `BalanceSheet`.
- Store balances as `dict[(payer_id, debtor_id), Decimal]` — symmetric updates keep it consistent.
- Use `Decimal`, round cents explicitly, document rounding rule.
- Strategy pattern here is the OCP win: new split types plug in without editing `Expense`.

### Reference solution (core)

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal("0.01")

def q(x: Decimal) -> Decimal:
    return x.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str

class Split(ABC):
    @abstractmethod
    def shares(self, amount: Decimal, participants: list[str]) -> dict[str, Decimal]: ...

class EqualSplit(Split):
    def shares(self, amount: Decimal, participants: list[str]) -> dict[str, Decimal]:
        n = len(participants)
        base = q(amount / n)
        remainder = amount - base * n  # could be a few cents
        out = {p: base for p in participants}
        # Distribute residual cents to first few participants deterministically.
        cents = int((remainder / TWO_PLACES).to_integral_value())
        for i in range(cents):
            out[participants[i]] += TWO_PLACES
        return out

class ExactSplit(Split):
    def __init__(self, amounts: list[Decimal]) -> None:
        self._amounts = [q(a) for a in amounts]

    def shares(self, amount: Decimal, participants: list[str]) -> dict[str, Decimal]:
        if len(self._amounts) != len(participants):
            raise ValueError("amounts length mismatch")
        if sum(self._amounts) != q(amount):
            raise ValueError("exact shares must sum to expense amount")
        return dict(zip(participants, self._amounts))

class PercentSplit(Split):
    def __init__(self, percents: list[Decimal]) -> None:
        if sum(percents) != Decimal("100"):
            raise ValueError("percents must sum to 100")
        self._percents = percents

    def shares(self, amount: Decimal, participants: list[str]) -> dict[str, Decimal]:
        return {p: q(amount * pct / Decimal("100")) for p, pct in zip(participants, self._percents)}

class Splitwise:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        # key: (creditor, debtor) -> positive amount debtor owes creditor
        self._ledger: dict[tuple[str, str], Decimal] = defaultdict(lambda: Decimal("0"))

    def add_user(self, user_id: str, name: str, email: str) -> None:
        if user_id in self._users:
            raise ValueError(f"duplicate user: {user_id}")
        self._users[user_id] = User(user_id, name, email)

    def add_expense(self, payer: str, amount: Decimal, participants: list[str], split: Split) -> None:
        if payer not in self._users:
            raise ValueError("unknown payer")
        for p in participants:
            if p not in self._users:
                raise ValueError(f"unknown participant: {p}")
        shares = split.shares(amount, participants)
        for debtor, share in shares.items():
            if debtor == payer:
                continue
            self._credit(payer, debtor, share)

    def _credit(self, creditor: str, debtor: str, amount: Decimal) -> None:
        # Net against any reverse debt to keep the ledger tidy.
        reverse = self._ledger[(debtor, creditor)]
        if reverse >= amount:
            self._ledger[(debtor, creditor)] = reverse - amount
            return
        remaining = amount - reverse
        self._ledger[(debtor, creditor)] = Decimal("0")
        self._ledger[(creditor, debtor)] += remaining

    def balance_of(self, user_id: str) -> dict[str, Decimal]:
        out: dict[str, Decimal] = {}
        for (cr, dr), amt in self._ledger.items():
            if amt == 0:
                continue
            if cr == user_id:
                out[dr] = out.get(dr, Decimal("0")) + amt
            elif dr == user_id:
                out[cr] = out.get(cr, Decimal("0")) - amt
        return out
```

**Talking points:** "`Split` is the strategy pattern — it's the open/closed win here. If tomorrow we need a 'one person pays for two' split, that's a new class, not an edit. I'm using `Decimal` and a documented residual-cent rule because money tests catch rounding bugs."

---

## 9. Problem 6 — Vending Machine (state machine)

> A vending machine sells drinks. It accepts coins (5¢, 10¢, 25¢, 100¢), shows running balance on a display, dispenses the product, returns change.
>
> States: `IDLE → COLLECTING → VENDING → IDLE`. Also needs to handle refund and out-of-stock.

### Why this one
State-machine problems are TW's favourite follow-up variants because they want to see:
- Explicit state modelling (enum, not stringly-typed).
- State transitions in one place (not scattered `if` branches).
- Testable: each transition is a test.

### TDD plan
1. Fresh machine is `IDLE`, balance 0.
2. Inserting coin moves to `COLLECTING`, accumulates balance.
3. Selecting product when balance < price → error, stay `COLLECTING`.
4. Selecting product when balance ≥ price and stocked → dispense, return change, back to `IDLE`.
5. Refund button → return coins in, back to `IDLE`.
6. Out-of-stock product → refund and error.

### Design notes
- `enum State`, `Product`, `Inventory`, `VendingMachine`.
- `ChangeMaker` as a separate class — greedy change with largest denom first; fails gracefully if exact change impossible.
- All transitions log via a tiny `EventLog` — interviewers often extend with "add an audit trail".

(I'll skip the full code here — pattern is obvious from above. If you build it cleanly, it's ~120 lines.)

**Talking points:** "The state is an `Enum`, transitions live on `VendingMachine`, and every public method asserts which states it's valid in. That gives me one place to grep when 'add a maintenance mode state' lands as the next requirement."

---

## 10. Onboarding-the-fresh-interviewer drill

This is the differentiator in the TW pairing round. Practice this **out loud** the day before.

After you've coded for ~40 min, a new interviewer walks in. You have 3–5 min to onboard them. The script:

1. **Domain** (20 sec): "This is a rover on a plateau. Rovers take `L/R/M` commands. They can't leave the plateau."
2. **Model** (30 sec): "I've got `Rover`, `Plateau`, `Position`, `Heading`. Rover is immutable — every move returns a new rover."
3. **Why that model** (45 sec): "Immutable rover makes multi-rover collision safe — there's no shared mutable state. Plateau is passed in, not owned by rover, because a later requirement might swap in a toroidal plateau."
4. **Where we are** (30 sec): "I just made turning work across all 4 headings. Next test is `M` for south movement, then the out-of-bounds refusal."
5. **What's next and open questions** (30 sec): "After movement I want to add a `Fleet` class for multi-rover, and I'm unsure whether collisions should raise or silently ignore — what's your preference?"

Rehearse this on all 6 problems. Time yourself. Under 4 minutes end-to-end.

---

## 11. One-week study plan

| Day | Focus | Output |
|-----|-------|--------|
| Mon | Read §1–§3. Set up `pytest` + file layout you'll use in the interview. | Can run RED→GREEN in 60 seconds. |
| Tue | Problem 1 (Mars Rover), TDD from scratch. 60 min timer. | Working code + ≥6 tests. |
| Wed | Problem 4 (Bowling Kata). 45 min — this one should be fast the second time. | Perfect game test passes. |
| Thu | Problem 2 (Sales Taxes). Full 90 min. | Decimal math correct, receipt formatted. |
| Fri | Problem 3 (Conference Track). 90 min. | Schedule prints; bin-packing works. |
| Sat | Problem 5 (Splitwise). 90 min, hardest one. | Ledger nets correctly on circular debt. |
| Sun | Problem 6 (Vending) + onboarding drill (§10) for all 6. | Can explain each in <4 min out loud. |

---

## 12. Round 3 (technical interview) prep — separate track

The technical round after pairing is different. It's a **discussion**, not a coding session. Prep:

- **Pick 2 projects** from your CV. For each, be ready to answer:
  - "Why that architecture?" (name a trade-off you rejected and why)
  - "What would you change?" (shows growth mindset)
  - "How did you test it?"
  - "What failed in production and what did you learn?"
- **Core fundamentals** they revisit (from candidate reports):
  - OOP: inheritance vs composition, Liskov, Interface Segregation
  - OS: process vs thread, context switching, virtual memory basics
  - Networking: TCP vs UDP, HTTP methods and status codes, what happens when you type a URL
  - Data structures: HashMap internals, tree traversals
  - One coding question, usually **tree-based** (reported): level-order traversal, LCA, serialize/deserialize

For the tree question, drill these until they're automatic:
- Inorder/preorder/postorder (iterative with explicit stack, not just recursive)
- Level-order (BFS with `deque`)
- LCA of a binary tree
- Serialize/deserialize (preorder + null markers)

---

## 13. Round 4 (cultural fit) — don't sleep on this

TW is values-driven in a way that eats candidates who skip prep. Read:
- TW's "First-Class Promise" and their stance on social justice
- Their [technology radar](https://www.thoughtworks.com/radar) — name 2 blips you find interesting
- Prepare 3 stories using STAR format:
  - A time you pushed back on a senior engineer (TW values equity of voice)
  - A time you made a mistake in code shipped to users
  - A time you changed your mind based on someone else's input

Common questions:
- "What does inclusion mean to you in a technical team?"
- "Tell me about a time you disagreed with a design decision."
- "What would make you leave a team?"

---

## 14. What to install before the interview

```
pip install pytest pytest-cov
```

File layout ready to type from memory:

```
problem/
  src/
    __init__.py
    <module>.py
  tests/
    __init__.py
    test_<module>.py
  README.md        # 5 lines: how to run, assumptions, design notes
  pytest.ini       # 2 lines: testpaths, addopts
```

`pytest.ini`:
```ini
[pytest]
testpaths = tests
addopts = -q
```

Run: `pytest -q`. Coverage: `pytest --cov=src`.

Muscle-memory matters more than elegance. Interviewers watch the keystroke speed on the first 3 minutes.

---

## 15. Cross-links

- [stripe_oa_prep_cheatsheet.md](stripe_oa_prep_cheatsheet.md) — Python stdlib cheats (dates, `Decimal`, `deque`, `bisect`)
- [stripe_screen_practice_bank.md](stripe_screen_practice_bank.md) — OOD + follow-up drilling (complementary to §4–§9 here)
- [ThoughtWorks pairing interview blog](https://www.thoughtworks.com/insights/blog/what-expect-pair-programming-interview)
- [TW "how to excel" post](https://www.thoughtworks.com/insights/blog/careers-at-thoughtworks/how-to-excel-in-thoughtworks-interviews)
- [Mars Rover reference GitHub](https://github.com/priyaaank/MarsRover)
- [Splitwise coding assignment repo](https://github.com/pulkitent/thoughtworks-split-wise-assignment)
