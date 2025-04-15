import pandas as pd
import numpy as np

def calculate_metrics(df: pd.DataFrame, capital: float = 1e7) -> dict:
    """
    Calculates performance metrics from backtested equity curve.
    
    Parameters:
        df (pd.DataFrame): DataFrame with 'equity' and 'pnl' columns
        capital (float): Initial capital
    
    Returns:
        dict: Performance metrics
    """
    result = {}

    df = df.copy()
    df['returns'] = df['equity'].pct_change().fillna(0)

    # Sharpe Ratio (assuming daily data, 252 trading days/year)
    result['Sharpe'] = (df['returns'].mean() / df['returns'].std()) * np.sqrt(252)

    # Calmar Ratio
    peak = df['equity'].cummax()
    drawdown = (df['equity'] - peak) / peak
    max_dd = drawdown.min()
    duration = (drawdown < 0).sum()
    result['Calmar'] = (df['equity'].iloc[-1] / capital - 1) / abs(max_dd) if max_dd != 0 else np.nan

    # Max Drawdown
    result['Max Drawdown (%)'] = round(max_dd * 100, 2)
    result['Time in Drawdown'] = duration

    # CAGR (with overflow-safe calculation)
    try:
        start = pd.to_datetime(df.index[0])
        end = pd.to_datetime(df.index[-1])
        days = max((end - start).days, 1)
        raw_cagr = ((df['equity'].iloc[-1] / capital) ** (365.25 / days)) - 1
        cagr = min(raw_cagr, 10)  # cap to avoid overflow
    except Exception:
        cagr = 0

    result['CAGR (%)'] = round(cagr * 100, 2)

    # Win rate & trades
    trades = df[df['pnl'] != 0]
    wins = trades[trades['pnl'] > 0]
    result['Total Trades'] = len(trades)
    result['Win Rate (%)'] = round(len(wins) / len(trades) * 100, 2) if len(trades) > 0 else 0

    return result
