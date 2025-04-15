import pandas as pd

def resample_data(df: pd.DataFrame, timeframe: str = '1H') -> pd.DataFrame:
    """
    Resamples minute-level data into higher timeframes like hourly, daily, etc.

    Parameters:
    - df (pd.DataFrame): Original dataframe with datetime index
    - timeframe (str): Resampling frequency (e.g., '1H', '1D', '15T')

    Returns:
    - pd.DataFrame: Resampled OHLCV dataframe
    """
    df = df.copy()
    
    # Ensure the datetime index is properly set
    if df.index.dtype != 'datetime64[ns]':
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)
        else:
            raise ValueError("DataFrame must have a datetime column or datetime index.")

    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    resampled_df = df.resample(timeframe.lower()).agg(ohlc_dict).dropna().reset_index()


    return resampled_df
