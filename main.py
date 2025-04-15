
import pandas as pd

from utils.data_loader import load_data
from utils.resampler import resample_data
from utils.indicators import add_indicators
from backtest.backtester import backtest_strategy
from backtest.metrics import calculate_metrics
from utils.plotting import plot_equity_curve, plot_drawdown, plot_monthly_returns

# --- Strategy Imports ---
from strategies.nifty_daily_ma_crossover import ma_crossover_strategy
from strategies.nifty_hourly_rsi_reversal import rsi_bollinger_strategy
from strategies.nifty_15min_breakout import breakout_strategy as nifty_breakout
from strategies.banknifty_daily_mean_reversion import mean_reversion_strategy
from strategies.banknifty_hourly_macd_trend import macd_trend_strategy
from strategies.banknifty_15min_breakout import inverted_intraday_breakout_strategy

# --- Config ---
strategies = [
    {"name": "Nifty_Daily_MA_Crossover", "symbol": "nifty", "freq": "daily", "func": ma_crossover_strategy},
    {"name": "Nifty_Hourly_RSI_Reversal", "symbol": "nifty", "freq": "1H", "func": rsi_bollinger_strategy},
    {"name": "Nifty_15min_Breakout", "symbol": "nifty", "freq": "15T", "func": nifty_breakout},
    {"name": "BankNifty_Daily_MeanReversion", "symbol": "banknifty", "freq": "daily", "func": mean_reversion_strategy},
    {"name": "BankNifty_Hourly_MACD", "symbol": "banknifty", "freq": "1H", "func": macd_trend_strategy},
    {"name": "BankNifty_15min_InvertedBreakout", "symbol": "banknifty", "freq": "15min", "func": inverted_intraday_breakout_strategy},
]

# --- Master Runner ---
for strat in strategies:
    print(f"\n🔍 Running Strategy: {strat['name']}")

    # Load and resample data
    df = load_data(strat["symbol"], "minute" if strat["freq"] in ["15T", "15min", "1H"] else "daily")
    if strat["freq"] in ["15T", "15min", "1H"]:
        df = resample_data(df, strat["freq"].replace("T", "min"))

    # ⏳ Filter data from 2020-01-01 to 2025-03-31
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df[(df['datetime'] >= '2020-01-01') & (df['datetime'] <= '2025-03-31')]
    elif df.index.dtype == 'datetime64[ns]':
        df = df[(df.index >= '2020-01-01') & (df.index <= '2025-03-31')]

    # Run strategy pipeline
    df = add_indicators(df)
    df = strat["func"](df)
    df = backtest_strategy(df, strat["symbol"])
    metrics = calculate_metrics(df)

    print(f"📊 {strat['name']} Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    plot_equity_curve(df, strat["name"])
    plot_drawdown(df)
    plot_monthly_returns(df)
