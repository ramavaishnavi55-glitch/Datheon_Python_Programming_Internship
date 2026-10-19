<<<<<<< HEAD

# Hangman Word Guessing Game (Console)

An interactive, modular console-based Hangman game built in Python. This project features dynamic ASCII art gallows, robust input validation, and clean state tracking designed as a foundational programming exercise.

## Features

- **Visual ASCII Art:** Dynamic gallows stages that update with each incorrect guess.
- **Robust Input Validation:** Prevents crashes or invalid states by checking for single alphabetical characters, empty inputs, numbers, and symbols.
- **Duplicate Guess Protection:** Alerts users if a letter has already been tried without deducting extra penalties.
- **Flexible Word Loading:** Automatically loads words from an external text file with a built-in fallback word list.
- **Replay Loop:** Allows multiple rounds of gameplay without restarting the script.

## Requirements

- Python 3.x

## How to Run

1. Clone the repository or download the script files into your local directory.
2. Ensure `google-10000-english-no-swears.txt` (or your chosen word list) is in the same folder as `hangman.py`.
3. Open your terminal or command prompt and run:
   ```bash
   python hangman.py
   ```

---

## Project 2: Stock Portfolio Performance Tracker (CLI & CSV)

An investment portfolio tracking utility that computes real-time valuation, percentage returns, sector diversification, and automatically logs performance metrics to an external CSV file.

### Features

- **Live Market Data:** Integrates with `yfinance` to fetch real-time stock pricing.
- **CSV Database Validation:** Validates user-entered ticker symbols against the S&P 500 constituents dataset (`constituents.csv`).
- **Sector Diversification Analytics:** Automatically calculates and displays your portfolio allocation by GICS sector.
- **Terminal Color-Coding:** Uses `colorama` to highlight positive gains in green and losses in red.
- **Persistent Logging:** Exports session summaries directly to `portfolio_summary.csv`.

### Requirements

- Python 3.x
- External Libraries: `yfinance`, `pandas`, `colorama`

### How to Run

1. Ensure `constituents.csv` is in the same directory as `portfolio.py`.
2. Install the required dependencies:
   ```bash
   pip install yfinance pandas colorama
   ```
