import csv
import os
import yfinance as yf
from colorama import init, Fore, Style

# Initialize colorama for terminal color formatting
init(autoreset=True)

def load_stock_database(filename="constituents.csv"):
    """Loads valid ticker symbols, company names, and GICS sectors from the provided CSV file."""
    stock_db = {}
    if os.path.exists(filename):
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    symbol = row["Symbol"].strip().upper()
                    security = row["Security"].strip()
                    sector = row["GICS Sector"].strip()
                    stock_db[symbol] = {"security": security, "sector": sector}
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not read '{filename}' ({e}).{Style.RESET_ALL}")
    return stock_db

def fetch_current_price(symbol):
    """Fetches real-time current market price using yfinance. Falls back to a mock price if offline."""
    try:
        ticker_obj = yf.Ticker(symbol)
        # Try fetching the latest market price
        todays_data = ticker_obj.history(period="1d")
        if not todays_data.empty:
            return round(float(todays_data['Close'].iloc[-1]), 2)
    except Exception:
        pass
    
    # Fallback simulation price if network fetch fails
    return 150.00

def display_portfolio(portfolio, stock_db):
    """Displays a neatly formatted portfolio table with color-coded gains/losses and sector breakdowns."""
    if not portfolio:
        print(f"\n{Fore.YELLOW}Your portfolio is currently empty.{Style.RESET_ALL}")
        return

    summary_data = []
    total_portfolio_cost = 0.0
    total_portfolio_value = 0.0
    sector_allocation = {}

    print("\n" + "=" * 105)
    print(f"{'Ticker':<8} | {'Shares':<8} | {'Buy ($)':<10} | {'Current ($)':<12} | {'Invested ($)':<12} | {'Market Val ($)':<14} | {'Gain/Loss (%)':<15} | {'Sector':<18}")
    print("-" * 105)

    for ticker, data in portfolio.items():
        shares = data['shares']
        buy_price = data['buy_price']
        current_price = fetch_current_price(ticker)
        
        invested_capital = shares * buy_price
        market_value = shares * current_price
        gain_loss_dollar = market_value - invested_capital
        gain_loss_percent = (gain_loss_dollar / invested_capital) * 100 if invested_capital > 0 else 0.0
        
        total_portfolio_cost += invested_capital
        total_portfolio_value += market_value

        # Track sector distribution
        sector = stock_db.get(ticker, {}).get('sector', 'Unknown')
        sector_allocation[sector] = sector_allocation.get(sector, 0.0) + market_value

        # Color coding for gain/loss percentage
        gl_str = f"{gain_loss_percent:>+6.2f}%"
        colored_gl = f"{Fore.GREEN}{gl_str}{Style.RESET_ALL}" if gain_loss_percent >= 0 else f"{Fore.RED}{gl_str}{Style.RESET_ALL}"

        summary_data.append({
            'Ticker': ticker,
            'Shares': shares,
            'Buy_Price': round(buy_price, 2),
            'Current_Price': round(current_price, 2),
            'Invested_Capital': round(invested_capital, 2),
            'Market_Value': round(market_value, 2),
            'Gain_Loss_Percent': round(gain_loss_percent, 2),
            'Sector': sector
        })

        print(f"{ticker:<8} | {shares:<8.2f} | ${buy_price:<9.2f} | ${current_price:<11.2f} | ${invested_capital:<11.2f} | ${market_value:<13.2f} | {colored_gl:<15} | {sector:<18}")

    total_gain_loss = total_portfolio_value - total_portfolio_cost
    total_gain_loss_pct = (total_gain_loss / total_portfolio_cost) * 100 if total_portfolio_cost > 0 else 0.0
    total_gl_str = f"{total_gain_loss:+,.2f} ({total_gain_loss_pct:+.2f}%)"
    colored_total_gl = f"{Fore.GREEN}{total_gl_str}{Style.RESET_ALL}" if total_gain_loss >= 0 else f"{Fore.RED}{total_gl_str}{Style.RESET_ALL}"

    print("-" * 105)
    print(f"Total Portfolio Cost:   ${total_portfolio_cost:,.2f}")
    print(f"Total Market Value:     ${total_portfolio_value:,.2f}")
    print(f"Total Net Gain/Loss:    {colored_total_gl}")
    print("=" * 105)

    # Display Sector Breakdown
    print(f"\n{Style.BRIGHT}--- Portfolio Sector Allocation ---{Style.RESET_ALL}")
    for sector, val in sector_allocation.items():
        pct = (val / total_portfolio_value) * 100 if total_portfolio_value > 0 else 0.0
        print(f"• {sector}: ${val:,.2f} ({pct:.1f}%)")

    return summary_data

def export_to_csv(summary_data, filename="portfolio_summary.csv"):
    """Exports portfolio summary data to an external CSV file."""
    if not summary_data:
        print(f"{Fore.YELLOW}No data available to export.{Style.RESET_ALL}")
        return
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as outfile:
            fieldnames = ['Ticker', 'Shares', 'Buy_Price', 'Current_Price', 'Invested_Capital', 'Market_Value', 'Gain_Loss_Percent', 'Sector']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_data:
                writer.writerow(row)
        print(f"\n{Fore.GREEN}📁 Portfolio summary successfully exported to '{filename}'!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error saving file: {e}{Style.RESET_ALL}")

def main():
    print(f"{Style.BRIGHT}{Fore.CYAN}=" * 60)
    print("       ENHANCED STOCK PORTFOLIO PERFORMANCE TRACKER      ")
    print("=" * 60 + f"{Style.RESET_ALL}")
    
    stock_db = load_stock_database()
    if stock_db:
        print(f"{Fore.GREEN}Successfully loaded {len(stock_db)} valid tickers from constituents.csv.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Note: constituents.csv not found. Operating without ticker restrictions.{Style.RESET_ALL}")

    portfolio = {}

    while True:
        print(f"\n{Style.BRIGHT}--- Main Menu ---{Style.RESET_ALL}")
        print("1. Add / Update Stock Position")
        print("2. Remove Stock Position")
        print("3. View Portfolio & Performance Report")
        print("4. Export Summary to CSV")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            ticker = input("Enter stock ticker symbol (e.g., AAPL, MSFT): ").strip().upper()
            if stock_db and ticker not in stock_db:
                print(f"{Fore.RED}❌ Error: '{ticker}' is not a valid S&P 500 ticker in the database.{Style.RESET_ALL}")
                continue
                
            try:
                shares = float(input(f"Enter number of shares for {ticker}: "))
                if shares <= 0:
                    print(f"{Fore.RED}❌ Shares must be greater than zero.{Style.RESET_ALL}")
                    continue
                    
                buy_price = float(input(f"Enter purchase price per share for {ticker} ($): "))
                if buy_price < 0:
                    print(f"{Fore.RED}❌ Buy price cannot be negative.{Style.RESET_ALL}")
                    continue
            except ValueError:
                print(f"{Fore.RED}❌ Invalid numeric input.{Style.RESET_ALL}")
                continue
                
            if ticker in portfolio:
                total_shares = portfolio[ticker]['shares'] + shares
                total_cost = (portfolio[ticker]['shares'] * portfolio[ticker]['buy_price']) + (shares * buy_price)
                portfolio[ticker]['buy_price'] = total_cost / total_shares
                portfolio[ticker]['shares'] = total_shares
            else:
                portfolio[ticker] = {'shares': shares, 'buy_price': buy_price}
                
            print(f"{Fore.GREEN}✅ Successfully updated position for {ticker}.{Style.RESET_ALL}")

        elif choice == '2':
            if not portfolio:
                print(f"{Fore.YELLOW}Portfolio is empty.{Style.RESET_ALL}")
                continue
            ticker = input("Enter ticker symbol to remove: ").strip().upper()
            if ticker in portfolio:
                del portfolio[ticker]
                print(f"{Fore.GREEN}✅ Removed {ticker} from your portfolio.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Ticker not found in your portfolio.{Style.RESET_ALL}")

        elif choice == '3':
            display_portfolio(portfolio, stock_db)

        elif choice == '4':
            summary = display_portfolio(portfolio, stock_db)
            if summary:
                export_to_csv(summary)

        elif choice == '5':
            print(f"\n{Fore.CYAN}Thank you for using the Portfolio Tracker. Good luck!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please select between 1 and 5.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()




"""============================================================
       ENHANCED STOCK PORTFOLIO PERFORMANCE TRACKER      
============================================================
Successfully loaded 503 valid tickers from constituents.csv.

--- Main Menu ---
1. Add / Update Stock Position
2. Remove Stock Position
3. View Portfolio & Performance Report
4. Export Summary to CSV
5. Exit
Select an option (1-5): 3

Your portfolio is currently empty.

--- Main Menu ---
1. Add / Update Stock Position
2. Remove Stock Position
3. View Portfolio & Performance Report
4. Export Summary to CSV
5. Exit
Select an option (1-5): 1
Enter stock ticker symbol (e.g., AAPL, MSFT): AEE
Enter number of shares for AEE: 3
Enter purchase price per share for AEE ($): 40
✅ Successfully updated position for AEE.

--- Main Menu ---
1. Add / Update Stock Position
2. Remove Stock Position
3. View Portfolio & Performance Report
4. Export Summary to CSV
5. Exit
Select an option (1-5): 3

=========================================================================================================
Ticker   | Shares   | Buy ($)    | Current ($)  | Invested ($) | Market Val ($) | Gain/Loss (%)   | Sector            
---------------------------------------------------------------------------------------------------------
$AEE: possibly delisted; no price data found  (period=1d)
AEE      | 3.00     | $40.00     | $150.00      | $120.00      | $450.00        | +275.00% | Utilities         
---------------------------------------------------------------------------------------------------------
Total Portfolio Cost:   $120.00
Total Market Value:     $450.00
Total Net Gain/Loss:    +330.00 (+275.00%)
=========================================================================================================

--- Portfolio Sector Allocation ---
• Utilities: $450.00 (100.0%)

--- Main Menu ---
1. Add / Update Stock Position
2. Remove Stock Position
3. View Portfolio & Performance Report
4. Export Summary to CSV
5. Exit
Select an option (1-5): 5   

Thank you for using the Portfolio Tracker."""
