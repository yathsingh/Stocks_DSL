"""
Pipeline:
1. Take natural language strategy text
2. Convert NL → structured JSON (rule objects)
3. Convert structured JSON → DSL string
4. Parse DSL → AST StrategyNode
5. Generate Python code from AST
6. Execute code to get entry/exit signals
7. Run backtest simulator
8. Print a full report
"""

import pandas as pd
import textwrap

from nlp.nl_to_struct import nl_to_struct
from nlp.struct_to_dsl import struct_to_dsl

from parser.parser import parse_strategy_text
from codegen.generator import generate_python
from backtest.simulator import run_backtest


def format_ast(ast):
    return repr(ast)


def load_evaluator(python_src: str):
    namespace = {}
    exec(python_src, namespace)
    return namespace["evaluate_strategy"]


def load_sample_data():

    data = {
        "open":   [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        "high":   [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        "low":    [ 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
        "close":  [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        "volume": [500000, 1200000, 900000, 2000000, 1500000, 1100000, 950000, 1800000, 1300000, 1600000],
    }

    return pd.DataFrame(data)


def main():

    print("\n=== STRATEGY INPUT MODE ===")
    print("1) Use preset natural-language strategies")
    print("2) Enter your own natural-language strategy")

    choice = input("\nSelect option (1 or 2): ").strip()

    presets = {
        "1": """
        Buy when price closes above the 20-day moving average.
        Buy when volume is above 1M.
        Exit when RSI 14 is below 30.
        """,

        "2": """
        Enter when close crosses above the 10-day moving average.
        Exit when close crosses below the 10-day moving average.
        """,
        
        "3": """
        Buy when yesterday's high is above today's close.
        Exit when volume is below 900k.
        """
    }

    if choice == "1":
        print("\nAvailable presets:")
        for k in presets:
            print(f"{k}) Preset {k}")

        p = input("\nChoose preset number: ").strip()
        nl = presets.get(p)

        if not nl:
            print("Invalid preset.")
            return

    elif choice == "2":
        print("\nEnter your strategy (finish with an empty line):")
        lines = []
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        nl = "\n".join(lines)

    else:
        print("Invalid choice.")
        return

    nl = textwrap.dedent(nl).strip()

    print("\n======= NATURAL LANGUAGE INPUT =======\n")
    print(nl)

    # Pipeline continues exactly as before
    struct = nl_to_struct(nl)
    print("\n======= STRUCT =======\n", struct)

    dsl = struct_to_dsl(struct)
    print("\n======= DSL =======\n", dsl)

    ast = parse_strategy_text(dsl)
    print("\n======= AST =======\n", ast)

    python_src = generate_python(ast)
    print("\n======= PYTHON CODE =======\n", python_src)

    evaluate = load_evaluator(python_src)
    df = load_sample_data()

    signals = evaluate(df)
    trades, metrics = run_backtest(df, signals["entry"], signals["exit"])

    print("\n======= TRADES =======")
    for t in trades:
        print(t)

    print("\n======= METRICS =======")
    print(metrics)


if __name__ == "__main__":
    main()
