import pandas as pd
import ta  # Technical Analysis library

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add standard indicators to a price DataFrame using 'ta' package.

    Parameters:
        df (pd.DataFrame): OHLCV data

    Returns:
        pd.DataFrame: Same data with new indicator columns
    """
    df = df.copy()

    # Simple Moving Averages
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()

    # RSI
    df['rsi_14'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    # MACD (optional — not used in all strategies)
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    return df
