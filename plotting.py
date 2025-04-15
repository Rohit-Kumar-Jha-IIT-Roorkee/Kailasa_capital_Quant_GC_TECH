import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curve(df: pd.DataFrame, title: str = "Equity Curve"):
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df['equity'], label='Equity', linewidth=2)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_drawdown(df: pd.DataFrame):
    peak = df['equity'].cummax()
    drawdown = (df['equity'] - peak) / peak

    plt.figure(figsize=(10, 3))
    plt.fill_between(df.index, drawdown, color='red', alpha=0.4)
    plt.title("Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_monthly_returns(df: pd.DataFrame):
    df = df.copy()
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)

    df['monthly_return'] = df['equity'].resample('ME').last().pct_change().fillna(0)

    plt.figure(figsize=(10, 3))
    df['monthly_return'].plot(kind='bar', color='skyblue')
    plt.title("Month-on-Month Returns")
    plt.xlabel("Month")
    plt.ylabel("Return")
    plt.tight_layout()
    plt.grid(True)
    plt.show()
