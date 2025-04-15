import pandas as pd

def breakout_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Intraday 15-min breakout strategy using first 1-hour high/low.
    Entry: Break above 1-hour high with RSI confirmation
    Exit: RSI > 70 or price below high
    """
    df = df.copy()
    df['signal'] = 0

    # Ensure datetime index
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)

    # Create first-hour high and low reference
    first_hour = df.between_time("09:15", "10:15")  # assumes 15-min candles start at 9:15
    breakout_high = first_hour['high'].resample('D').max()
    breakout_low = first_hour['low'].resample('D').min()

    # Map breakout levels back to full dataframe
    df['date'] = df.index.date
    df['breakout_high'] = df['date'].map(breakout_high)
    df['breakout_low'] = df['date'].map(breakout_low)

    # Entry: price crosses above high and RSI < 60
    entry = (df['close'] > df['breakout_high']) & (df['rsi_14'] < 60)
    df.loc[entry, 'signal'] = 1

    # Exit: RSI > 70 or price falls back under high
    exit = (df['rsi_14'] > 70) | (df['close'] < df['breakout_high'])
    df.loc[exit, 'signal'] = 0

    df['signal'] = df['signal'].ffill().shift(1).fillna(0)

    return df
