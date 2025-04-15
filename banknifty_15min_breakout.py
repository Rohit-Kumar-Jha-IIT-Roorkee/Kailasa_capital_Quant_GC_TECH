import pandas as pd

def inverted_intraday_breakout_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    INVERTED version of 15-min breakout strategy.
    Original logic was poor — so we short the same breakout signals instead.
    """

    df = df.copy()
    df['signal'] = 0

    # Ensure datetime index
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)

    # Create previous day high
    daily_high = df['high'].resample("1D").max().shift(1)
    df['prev_day'] = df.index.date
    df['prev_high'] = df['prev_day'].map(daily_high)

    # ORIGINAL entry condition
    original_entry = (df['close'] > df['prev_high']) & (df['rsi_14'] > df['rsi_14'].shift(1))
    df.loc[original_entry, 'signal'] = 1

    # ORIGINAL exit condition
    original_exit = (df['close'] < df['prev_high']) | (df['rsi_14'] > 75)
    df.loc[original_exit, 'signal'] = 0

    # Forward fill signal and shift for realism
    df['signal'] = df['signal'].ffill().shift(1).fillna(0)

    # ✅ Invert the signal — flip long to short logic
    df['signal'] = 1 - df['signal']

    return df
