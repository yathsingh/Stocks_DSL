import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_sample_prices(n: int = 100, start_price: float = 100.0) -> List[Dict[str, Any]]:
    """
    Generates mock OHLC values
    Each item: {'time': iso-string, 'open': float, 'high': float, 'low': float, 'close': float}
    """

    data = []
    t = datetime.utcnow()
    price = start_price

    for i in range(n):

        change = random.uniform(-1.0, 1.0)

        open_p = round(price, 2)
        close_p = round(price + change, 2)

        high_p = round(max(open_p, close_p) + random.uniform(0, 0.5), 2)

        low_p = round(min(open_p, close_p) - random.uniform(0, 0.5), 2)

        data.append({
            "time": (t + timedelta(minutes=i)).isoformat(),
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p
        })
        price = close_p
    return data


def simulate(sample_data: List[Dict[str, Any]], evaluate_strategy_fn=None):
    """
    Minimal simulate function 
    sample_data: list of bar dicts from generate_sample_prices
    evaluate_strategy_fn: mock placeholder function
    """
    trades = []  
  
    meta = {
        "n_bars": len(sample_data),  
        "sample_start": sample_data[0]["time"] if sample_data else None,  
        "sample_end": sample_data[-1]["time"] if sample_data else None,   
        "notes": "Placeholder simulator — no trades generated yet"  
    }
    return {"trades": trades, "meta": meta} 


# Direct demo
if __name__ == "__main__":
    
    sample = generate_sample_prices(10)
    print("Sample bars (first 3):")  #
    for b in sample[:3]: 
        print(b)  
    result = simulate(sample)  
    print("\nSimulate result:", result)  
