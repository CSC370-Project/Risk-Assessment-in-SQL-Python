import yfinance as yf

# Function to fetch stock data
def get_stock(ticker, stock_id):
    try:
        # Create a Ticker object for the specified ticker
        stock = yf.Ticker(ticker)
        
        # Fetch stock info with safe default values
        stock_info = stock.info
        symbol = stock_info.get('symbol', ticker)  # Default to the input ticker if 'symbol' is not available
        sector = stock_info.get('sector', 'Unknown')  # Default to 'Unknown' if 'sector' is not available
        price = stock_info.get('regularMarketPreviousClose', 0.0)  # Default to 0.0 if 'regularMarketPreviousClose' is not available
        sd = stock_info.get('beta', 0.0)  # Default to 0.0 if 'beta' is not available
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3)  # Default to 0.0 if 'forwardEps' is not available
        
        return stock_id, symbol, sector, price, sd, eret
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return stock_id, None, None, None, None, None

def main(tickers = ""):
    if tickers == "":
        tickers = input("Enter the stock ticker symbols (separated by commas): ").split(',')

    tickers = tickers.split(',')

    # Initialize stock_id counter
    stock_id = 1

    # List to hold the fetched data
    stock_data_list = []

    # Fetch and store stock data for each ticker symbol
    for ticker in tickers:
        ticker = ticker.strip()  # Remove any leading/trailing whitespace
        stock_data = get_stock(ticker, stock_id)
        if stock_data[1]:  # Check if symbol is not None
            stock_data_list.append(stock_data)
        stock_id += 1

    # Prepare the SQL insert statements
    insert_statements = []
    for data in stock_data_list:
        stock_id, symbol, sector, price, sd, eret = data
        insert_statement = f"INSERT INTO stock (StockID, Ticker, Sector, Price, SD, ERet) VALUES ({stock_id}, '{symbol}', '{sector}', {price}, {sd}, {eret});"
        insert_statements.append(insert_statement)

    # Combine all insert statements into a single string
    sql_insert_statements = "\n".join(insert_statements)

    # Save the SQL insert statements to a file
    # with open("insert_statements.sql", "w") as file:
    #     file.write(sql_insert_statements)

    
    return sql_insert_statements

# if __name__ == "__main__":
#     tickers = input("Enter the stock ticker symbols (separated by commas): ").split(',')
#     main(tickers)
