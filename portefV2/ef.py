import pandas as pd
import numpy as np
from scipy.optimize import minimize


def calculate_efficient_frontier(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.pivot(index='Date', columns='Ticker', values='Price')
    returns = df.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(len(df.columns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_return = np.sum(weights * mean_returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        results[0,i] = portfolio_return
        results[1,i] = portfolio_stddev
        results[2,i] = results[0,i] / results[1,i]

    return results, weights_record, df


def store_allocation(connection, cursor, weights_record, results, df):
    max_sharpe_idx = np.argmax(results[2])
    optimal_weights = weights_record[max_sharpe_idx]
    tickers = df.columns.tolist()

    for ticker, weight in zip(tickers, optimal_weights):
        cursor.execute("INSERT INTO Allocation (Ticker, Amount) VALUES (%s, %s)", (ticker, weight))
    
    connection.commit()
    cursor.close()
    print("Optimal allocation stored successfully")

