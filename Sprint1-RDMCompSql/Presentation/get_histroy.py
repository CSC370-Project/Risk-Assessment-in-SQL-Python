import yfinance as yf
from datetime import datetime, timedelta

# Function to fetch stock history
def get_history(ticker, start_date, end_date):
    try:
        # Fetch stock history for the past week
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        
        # Extract relevant data (date and price)
        history_data = []
        for date, row in hist.iterrows():
            history_data.append((ticker, date.strftime('%Y-%m-%d'), row['Close']))
        
        return history_data
    except Exception as e:
        print(f"Error fetching history for {ticker}: {e}")
        return []

def main(tickers=""):
    if not tickers:
        tickers = input("Enter the stock ticker symbols (separated by commas): ")

    tickers = tickers.split(',')

    # Get current date and date one week ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Initialize history_id counter
    history_id = 1

    # List to hold the fetched data
    history_data_list = []

    # Fetch and store stock history data for each ticker symbol
    for ticker in tickers:
        ticker = ticker.strip()
        history_data = get_history(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        for data in history_data:
            history_data_list.append((history_id,) + data)
            history_id += 1

    # Prepare the SQL insert statements
    insert_statements = []
    for data in history_data_list:
        hid, ticker, date, price = data
        insert_statement = f"INSERT INTO history (historyID, Ticker, Date, Price) VALUES ({hid}, '{ticker}', '{date}', {price});"
        insert_statements.append(insert_statement)

    # Combine all insert statements into a single string
    sql_insert_statements = "\n".join(insert_statements)

    # Save the SQL insert statements to a file
    with open("insert_history_statements.sql", "w") as file:
        file.write(sql_insert_statements)

    return sql_insert_statements

# Example usage
if __name__ == "__main__":
    tickers = "AAPL, MSFT, GOOGL"
    print(main(tickers))
