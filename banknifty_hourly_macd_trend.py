import pandas as pd

def macd_trend_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bank Nifty hourly MACD trend following strategy.
    Buy when MACD crosses above signal and RSI in good zone.
    Exit when MACD crosses below signal or RSI > 70.
    """
    df = df.copy()
    df['signal'] = 0

    # Entry condition
    entry = (
        (df['macd'] > df['macd_signal']) &
        (df['macd'].shift(1) <= df['macd_signal'].shift(1)) &  # crossover now
        (df['rsi_14'] > 40) & (df['rsi_14'] < 65)
    )
    df.loc[entry, 'signal'] = 1

    # Exit condition
    exit = (
        (df['macd'] < df['macd_signal']) |
        (df['rsi_14'] > 70)
    )
    df.loc[exit, 'signal'] = 0

    df['signal'] = df['signal'].ffill().shift(1).fillna(0)

    return df
