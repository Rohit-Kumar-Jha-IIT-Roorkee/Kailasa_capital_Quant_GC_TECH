import pandas as pd
import os

def load_data(symbol: str, frequency: str = "daily") -> pd.DataFrame:
    """
    Load and return the data for a given symbol and frequency.

    Parameters:
        symbol (str): 'nifty' or 'banknifty'
        frequency (str): 'daily' or 'minute'

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    assert symbol in ["nifty", "banknifty"], "Symbol must be 'nifty' or 'banknifty'"
    assert frequency in ["daily", "minute"], "Frequency must be 'daily' or 'minute'"

    path = f"data/{symbol}_{frequency}.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found!")

    df = pd.read_csv(path)

    # Standardize column names
    df.columns = [c.strip().lower() for c in df.columns]
    if 'date' in df.columns:
        df['datetime'] = pd.to_datetime(df['date'])
    elif 'timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamp'])
    else:
        raise ValueError("No date or timestamp column found.")

    df.set_index('datetime', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    df.sort_index(inplace=True)

    return df
