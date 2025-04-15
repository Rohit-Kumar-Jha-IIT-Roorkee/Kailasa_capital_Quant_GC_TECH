import pandas as pd

def rsi_bollinger_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    RSI + Bollinger Band mean reversion strategy.
    Buy when RSI < 30 and price below lower BB. Exit when RSI > 50.
    
    Returns:
        pd.DataFrame with 'signal' column (1 = long, 0 = exit)
    """
    df = df.copy()
    df['signal'] = 0

    # Entry condition
    entry_condition = (df['rsi_14'] < 30) & (df['close'] < df['bb_lower'])
    df.loc[entry_condition, 'signal'] = 1

    # Exit condition
    exit_condition = (df['rsi_14'] > 50)
    df.loc[exit_condition, 'signal'] = 0

    # Forward fill signal and shift to avoid lookahead
    df['signal'] = df['signal'].ffill().shift(1).fillna(0)

    return df
