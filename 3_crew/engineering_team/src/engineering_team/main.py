#!/usr/bin/env python
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

REQUIREMENTS = """
## Goal
Build a self-contained, in-memory account management system for a single-user trading simulation platform.
No external dependencies beyond the Python standard library. No database or file persistence required.

## Constructor
Account(get_share_price: Callable[[str], float])
- Accepts a `get_share_price(symbol: str) -> float` callable as its only parameter.
- Include a module-level test implementation: `test_get_share_price(symbol: str) -> float`
  returning fixed prices: AAPL=182.0, TSLA=250.0, GOOGL=140.0. Raise ValueError for unknown symbols.

## Methods

### Cash Management
- deposit(amount: float) -> None
  Add funds to cash balance. Raise ValueError if amount <= 0.

- withdraw(amount: float) -> None
  Deduct funds from cash balance. Raise ValueError if amount <= 0 or if it would result in a negative balance.

### Share Trading
- buy(symbol: str, quantity: int) -> None
  Purchase shares at the current price from get_share_price(symbol).
  Raise ValueError if quantity <= 0 or if the total cost exceeds the available cash balance.

- sell(symbol: str, quantity: int) -> None
  Sell shares at the current price from get_share_price(symbol).
  Raise ValueError if quantity <= 0 or if the user holds fewer shares than the requested quantity.

### Portfolio Reporting
- get_holdings() -> dict[str, int]
  Return a mapping of symbol -> quantity for all shares currently held. Exclude symbols with zero quantity.

- get_portfolio_value() -> float
  Return the total market value of all held shares at current prices. Excludes cash balance.

- get_total_value() -> float
  Return cash balance + get_portfolio_value().

- get_profit_loss() -> float
  Return get_total_value() minus the total amount ever deposited via deposit().
  Withdrawals do not reduce the deposit baseline — they are treated as money taken out of profit.

### Transaction History
- get_transactions() -> list[dict]
  Return all transactions in chronological order. Each transaction is a dict with keys:
    - type: str         — one of "deposit", "withdrawal", "buy", "sell"
    - symbol: str       — ticker symbol, empty string for cash transactions
    - quantity: int     — number of shares, 0 for cash transactions
    - price: float      — price per share at time of transaction, 0.0 for cash transactions
    - amount: float     — total cash impact (positive for deposit/sell, negative for withdrawal/buy)
    - timestamp: str    — ISO 8601 format from datetime.now().isoformat()

## Constraints
- All monetary values are floats denominated in USD.
- quantity parameters must be positive integers; validate before executing any trade.
- Every successful deposit, withdrawal, buy, and sell must append an entry to the transaction log.
- All methods must be fully type-annotated.
"""
MODULE_NAME = "accounts.py"
CLASS_NAME = "Account"


def run() -> None:
    output_dir = os.path.join(
        "output", datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(output_dir, exist_ok=True)

    inputs = {
        "requirements": REQUIREMENTS,
        "module_name": MODULE_NAME,
        "class_name": CLASS_NAME,
        "output_dir": output_dir,
    }

    EngineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
