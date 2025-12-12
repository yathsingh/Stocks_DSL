import pandas as pd

class Trade:
    """
    Simple trade record for clarity.
    """

    def __init__(self, entry_idx, entry_price):

        self.entry_idx = entry_idx
        self.entry_price = entry_price
        self.exit_idx = None
        self.exit_price = None

    def close(self, exit_idx, exit_price):

        self.exit_idx = exit_idx
        self.exit_price = exit_price

    def pnl(self):

        if self.exit_price is None:
            return 0.0
        return self.exit_price - self.entry_price

    def __repr__(self):
        return (
            f"Trade(entry_idx={self.entry_idx}, entry_price={self.entry_price}, "
            f"exit_idx={self.exit_idx}, exit_price={self.exit_price}, pnl={self.pnl():.2f})"
        )


def run_backtest(df, signals):
    """
    PARAMETERS:
    df : pandas DataFrame (must contain 'close')
    signals : dict with:
        1. 'entry' : pandas Series[bool]
        2. 'exit' : pandas Series[bool]

    RETURNS:
    dict with:
        1. 'trades': list of Trade objects
        2. 'metrics': simple summary
    """

    entry_signal = signals["entry"]
    exit_signal = signals["exit"]

    trades = []
    position = None   

    for idx in range(len(df)):
        close_price = df["close"].iloc[idx]

        if position is None and entry_signal.iloc[idx]:
            position = Trade(entry_idx=idx, entry_price=close_price)
            continue

        if position is not None and exit_signal.iloc[idx]:
            position.close(exit_idx=idx, exit_price=close_price)
            trades.append(position)
            position = None
            continue

    if position is not None:
        exit_price = df["close"].iloc[-1]
        position.close(exit_idx=len(df)-1, exit_price=exit_price)
        trades.append(position)

    total_pnl = sum(t.pnl() for t in trades)
    win_trades = [t for t in trades if t.pnl() > 0]
    loss_trades = [t for t in trades if t.pnl() <= 0]

    metrics = {
        "total_pnl": total_pnl,
        "num_trades": len(trades),
        "wins": len(win_trades),
        "losses": len(loss_trades),
    }

    return {
        "trades": trades,
        "metrics": metrics,
    }
