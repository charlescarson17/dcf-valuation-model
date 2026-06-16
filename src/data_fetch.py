"""
Data layer: fetches raw financial statement data on analysis target company from yfinance.
This module's only responsibility is to retrieve the financial data.
Calculations don't happen here.
Strategy: This keeps the data source swappable.
"""

import yfinance as yf

def fetch_financials(ticker_symbol):
    """
    Fetch financial data for a given stock ticker.

    ticker_symbol (str): ex: "AAPL:
    
    Returns dictionary of raw financial statements and key figures

    """
    ticker = yf.Ticker(ticker_symbol)

    #Pull the 3 core financial statements (each a Pd DataFrame)
    income_statement = ticker.financials
    balance_sheet = ticker.balance_sheet
    cash_flow = ticker.cashflow

    #Info is dictionary of summary figures/facts
    info = ticker.info

    #Bundle everything into a single dictionary that can be used in the DCF analysis
    data = {
        'ticker': ticker_symbol,
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
        'beta': info.get('beta'),
        'shares_outstanding': info.get('sharesOutstanding'),
        'current_price': info.get('currentPrice'),
        'market_cap': info.get('marketCap'),
    }

    return data


def get_line_item(statement, possible_labels):
    """
    Safely pull a row from a financial statement DataFrame.
    Tries multiple possible label names since yFinance isn't always consistent on a company by company basis.

    statement (DataFrame): income statement, balance sheet, etc.
    possible_labels (list): list of label names to try

    Returns most recent value found or None if no lable matches
    """

    for label in possible_labels:
        if label in statement.index:
            # .iloc[0] grabs the most recent perdiod
            return statement.loc[label].iloc[0]
    
    return None



if __name__ == "__main__":
    #This block only runs when you execute this file directly
    #Does not run when imported elsewhere
    result = fetch_financials('AAPL')

    print(f"Ticker: {result['ticker']}")
    print(f"Beta: {result['beta']}")
    print(f"Shares Outstanding: {result['shares_outstanding']}")
    print(f"Current Price: {result['current_price']}")
    print("\nIncome Statement preview:")
    print(result['income_statement'].head())
