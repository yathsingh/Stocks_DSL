from typing import List, Dict, Tuple
import pandas as pd


def run_backtest(df: pd.DataFrame,
                 entry_signal: pd.Series,
                 exit_signal: pd.Series) -> Tuple[List[Dict], Dict]:
    """
    Parameters:
    df : pandas.DataFrame
        Must contain a 'close' price column.
    entry_signal : pandas.Series(bool)
        True when we should open a long position.
    exit_signal : pandas.Series(bool)
        True when we should close the position.

    Returns:
    -------
    trades : list of dicts
        One entry per trade with:
            entry_index
            exit_index
            entry_price
            exit_price
            pnl
    metrics : dict
        Simple performance summary:
            total_pnl
            num_trades
            wins
            losses
    """

    trades = []
    position_open = False

    entry_idx = None
    entry_price = None


    for i in range(len(df)):

        #ENTRY LOGIC
        if not position_open and entry_signal.iloc[i]:

            position_open = True
            entry_idx = i
            entry_price = df["close"].iloc[i]

        #EXIT LOGIC
        elif position_open and exit_signal.iloc[i]:
            
            exit_price = df["close"].iloc[i]
            pnl = exit_price - entry_price

            trades.append({
                "entry_index": entry_idx,
                "exit_index": i,
                "entry_price": float(entry_price),
                "exit_price": float(exit_price),
                "pnl": float(pnl),
            })

            # RESET STATE
            position_open = False
            entry_idx = None
            entry_price = None

  
    # At the end of the data, if still in a trade, then exit on last bar

    if position_open:
        exit_price = df["close"].iloc[-1]
        pnl = exit_price - entry_price

        trades.append({
            "entry_index": entry_idx,
            "exit_index": len(df) - 1,
            "entry_price": float(entry_price),
            "exit_price": float(exit_price),
            "pnl": float(pnl),
        })


    # Compute performance metrics

    total_pnl = sum(t["pnl"] for t in trades)
    wins = sum(1 for t in trades if t["pnl"] > 0)
    losses = sum(1 for t in trades if t["pnl"] <= 0)

    metrics = {
        "total_pnl": float(total_pnl),
        "num_trades": len(trades),
        "wins": wins,
        "losses": losses,
    }

    return trades, metrics
