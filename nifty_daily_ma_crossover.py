import pandas as pd

def ma_crossover_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Smarter MA Crossover Strategy:
    - Entry: SMA20 > SMA50 AND Close > 20-day High AND RSI > 50
    - Exit: Close < SMA50 OR RSI < 45
    """
    df = df.copy()
    df['signal'] = 0

    # Create breakout threshold
    df['20d_high'] = df['close'].rolling(window=20).max()

    # Entry condition: strong bullish trend
    entry = (
        (df['sma_20'] > df['sma_50']) &
        (df['close'] > df['20d_high'].shift(1)) &
        (df['rsi_14'] > 50)
    )
    df.loc[entry, 'signal'] = 1

    # Exit condition: momentum loss
    exit = (
        (df['close'] < df['sma_50']) |
        (df['rsi_14'] < 45)
    )
    df.loc[exit, 'signal'] = 0

    # Carry forward signal and avoid lookahead
    df['signal'] = df['signal'].ffill().shift(1).fillna(0)

    return df
