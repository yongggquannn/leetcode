"""
Account Balance Manager (Stripe / "StripePay")
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/07b4da76-7763-4fce-b300-7156cccd1949
Reconstructed from: 1point3acres post 7100074 + Chegg StripePay Backend

Build the backend for a payment app called StripePay. Parse a list of commands
for an account-balance API and return a comma-separated string of the command
results in input (sequential) order.

KEY TWIST: Commands may arrive OUT OF ORDER; they MUST be executed in
chronological (timestamp) order, but the OUTPUT is in INPUT order.

================================================================================
COMMAND TYPES
================================================================================

INIT user starting_balance bank1 bank2 ...
    Sets the user's starting balance and lists the banks they use.
    Result: typically "SUCCESS" (no balance/timestamp side effect on output).

POST timestamp sender receiver amount
    Transfer `amount` from sender to receiver at the given timestamp.
    - If sender is one of receiver's banks -> deposit into receiver's account.
    - If receiver is one of sender's banks -> withdrawal from sender's account.
    - Otherwise: a P2P transfer between two user accounts.
    Returns "FAILURE" if the action would leave sender's balance negative,
    else "SUCCESS".

GET timestamp user
    Return the user's account balance AS OF the given timestamp (i.e. after
    all chronologically-earlier POSTs are applied).

================================================================================
PARTS
================================================================================

Part 1: INIT + POST (P2P only) + GET, all in chronological order.
Part 2: Out-of-order arrival - sort by timestamp before processing, but
        preserve input ordering in the output string.
Part 3: Bank deposits / withdrawals (sender or receiver is a known bank
        of the other party).

================================================================================
TODO ON FIRST OPEN
================================================================================

Confirm exact command syntax (delimiter, casing) and the output format from
the DarkInterview source.
"""


def run_commands_part1(commands: list[str]) -> str:
    pass


def run_commands_part2(commands: list[str]) -> str:
    pass


def run_commands_part3(commands: list[str]) -> str:
    pass


if __name__ == "__main__":
    pass
