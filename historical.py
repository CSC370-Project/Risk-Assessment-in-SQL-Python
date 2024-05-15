import yfinance as yf
from datetime import datetime

# Prompt the user to input a ticker symbol
ticker_symbol = input("Enter a ticker symbol (e.g., AAPL): ")

# Todays date
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch historical price data from Yahoo Finance
data = yf.download(ticker_symbol, start="2019-01-01", end=end_date)

# Save the data to a CSV file
csv_filename = f"{ticker_symbol}_historical_data.csv"
data.to_csv(csv_filename)

print(f"Historical price data has been saved to {csv_filename}")