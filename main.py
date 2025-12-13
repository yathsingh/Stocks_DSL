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

    print("\n======= NATURAL LANGUAGE INPUT =======\n")
    nl = """
    Buy when price closes above the 20-day moving average
    and volume is above 1M.
    Exit when RSI 14 is below 30.
    """
    nl = textwrap.dedent(nl).strip()
    print(nl)

    
    # 1) NL → structured objects
   
    struct = nl_to_struct(nl)

    print("\n======= STRUCTURED (JSON-style) RULES =======\n")
    print(struct)


    # 2) structured objects → DSL

    dsl = struct_to_dsl(struct)

    print("\n======= GENERATED DSL =======\n")
    print(dsl)
  
    # 3) DSL → AST

    ast = parse_strategy_text(dsl)

    print("\n======= AST =======\n")
    print(format_ast(ast))

    # 4) AST → Python strategy code

    python_src = generate_python(ast)

    print("\n======= GENERATED PYTHON CODE =======\n")
    print(python_src)

    # 5) Load evaluate_strategy(df)

    evaluate = load_evaluator(python_src)

    # 6) Sample data + compute signals

    df = load_sample_data()

    signals = evaluate(df)
    entry = signals["entry"]
    exit_ = signals["exit"]

    print("\n======= ENTRY SIGNAL (head) =======\n")
    print(entry.head())
    print("\n======= EXIT SIGNAL (head) =======\n")
    print(exit_.head())

    # 7) Backtest simulation
    
    trades, metrics = run_backtest(df, entry, exit_)

    print("\n======= BACKTEST TRADES =======\n")
    for t in trades:
        print(t)

    print("\n======= BACKTEST METRICS =======\n")
    print(metrics)

    print("\n======= END OF DEMO =======\n")


if __name__ == "__main__":
    main()
