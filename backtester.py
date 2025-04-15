import pandas as pd

def backtest_strategy(df: pd.DataFrame, symbol: str, capital: float = 1e7) -> pd.DataFrame:
    """
    Backtests a long-only strategy using signal column.
    
    Parameters:
        df (pd.DataFrame): Must contain 'signal' and 'close'
        symbol (str): 'nifty' or 'banknifty'
        capital (float): Starting capital (default: 1 Cr)
    
    Returns:
        pd.DataFrame with equity curve and trade-level PnL
    """

    df = df.copy()
    df['position'] = df['signal'].shift().fillna(0)  # hold position based on signal from previous day

    # Lot and margin info
    lot_size = 75 if symbol == 'nifty' else 25
    margin_pct = 0.20  # 20% margin
    slippage = 0.0001  # 0.01%

    # Position sizing
    df['price'] = df['close'] * (1 + slippage)  # assume slippage on entry
    notional_per_lot = df['price'] * lot_size
    margin_per_lot = notional_per_lot * margin_pct
    df['lots'] = (capital // margin_per_lot).astype(int)
    df['position_value'] = df['lots'] * lot_size * df['price']
    df['entry_price'] = df['price'].where(df['signal'] == 1)

    # Forward fill entry price until position closes
    df['entry_price'] = df['entry_price'].ffill()
    df['exit_price'] = df['price'].where(df['signal'] == 0)
    
    # Calculate returns
    df['pnl'] = 0.0
    df.loc[df['signal'] == 0, 'pnl'] = (
        (df['exit_price'] - df['entry_price']) * df['lots'] * lot_size
        - (df['entry_price'] + df['exit_price']) * slippage * df['lots'] * lot_size
    )

    df['cumulative_pnl'] = df['pnl'].cumsum()
    df['equity'] = capital + df['cumulative_pnl']

    return df
