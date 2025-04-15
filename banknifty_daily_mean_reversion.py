import pandas as pd

def mean_reversion_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bank Nifty daily mean reversion strategy.
    Buy when price < SMA50 and RSI rising from oversold.
    Exit when price > SMA50 or RSI > 60.
    """
    df = df.copy()
    df['signal'] = 0

    # Entry condition
    entry = (
        (df['close'] < df['sma_50']) &
        (df['rsi_14'] > df['rsi_14'].shift(1)) &
        (df['rsi_14'] < 35) &
        (df['close'] > df['close'].shift(1))
    )
    df.loc[entry, 'signal'] = 1

    # Exit condition
    exit = (df['close'] > df['sma_50']) | (df['rsi_14'] > 60)
    df.loc[exit, 'signal'] = 0

    df['signal'] = df['signal'].ffill().shift(1).fillna(0)

    return df
