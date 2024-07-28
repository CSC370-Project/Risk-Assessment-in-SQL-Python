#!/usr/bin/env python3

from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_sh import get_stock

def main():
    connection, cursor = connect_to_database()
    if connection:
        try:
            tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
            if not tickers_input:
                raise ValueError("Ticker symbols input cannot be empty.")
            tickers = [ticker.strip() for ticker in tickers_input.split(',')]
            
            db_setup(connection, cursor)
            get_stock(connection, cursor, tickers)
            
            print("Program executed successfully.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            close_connection(connection, cursor)
    else:
        print("Failed to connect to the database. Exiting program.")

if __name__ == "__main__":
    main()
