# Corporate Budget & Expense Automation Tracker

An enterprise-ready Python automation tool designed to manage operational budgets, validate transaction data types defensively, and monitor category expenditures against safety thresholds.

## Key Architecture & Features
- **Object-Oriented Architecture:** Core application logic is fully encapsulated within robust Python classes.
- **Defensive Data Input Validation:** Implements comprehensive `try-except` guardrails to neutralize runtime type errors without application crashes.
- **Data Persistence Layer:** Integrates built-in JSON File I/O serialization to preserve tracker logs across separate computing sessions.
- **Real-Time Breach Alerts:** Evaluates operational inputs instantly and flags items that exceed 40% of the total monthly target capital.

## Technical Skills Demonstrated
- Object-Oriented Programming (OOP)
- Exception Handling & System Stability
- Text Sanitization & Cleaning (`.strip()`, `.capitalize()`)
- File Handling & Serialization Ecosystems (JSON structures)

## How To Run Locally
1. Clone the repository.
2. Open terminal and execute: `python finance_tracker.py`
