import yfinance as yf
import numpy as np
data = yf.download(["SPY", "AAPL"], start="2021-01-01", end="2023-01-31")
closes = data['Adj Close']
spy_returns = closes.SPY.pct_change().dropna()
aapl_returns = closes.AAPL.pct_change().dropna()

def sortino_ratio(returns, adjustment_factor=0.0):
    returns_risk_adj = np.asanyarray(returns - adjustment_factor)
    mean_annual_return = returns_risk_adj.mean() * 252

    downside_diff = np.clip(returns_risk_adj, np.NINF, 0)
    np.square(downside_diff, out=downside_diff)
    annualized_downside_deviation = np.sqrt(downside_diff.mean()) * np.sqrt(252)
    
    return mean_annual_return / annualized_downside_deviation

sortino_ratio(spy_returns)
sortino_ratio(aapl_returns)
aapl_returns.rolling(30).apply(sortino_ratio).plot()

aapl_returns.rolling(30).apply(sortino_ratio).hist(bins=50)

(
    aapl_returns.rolling(30).apply(sortino_ratio)
    - spy_returns.rolling(30).apply(sortino_ratio)
).hist(bins=50)
