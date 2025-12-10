from typing import List
from parser.ast_nodes import StrategyNode, BuyRuleNode, SellRuleNode, ConditionNode

def _fmt_condition(cond: ConditionNode) -> str:

    if cond is None:
        return "# <empty condition>"
    return f"# condition: {cond.indicator} {cond.operator} {cond.value}"

def generate_python(strategy: StrategyNode) -> str:

    header = [
        "def evaluate_strategy(df):",
        "    \"\"\"",
        "    df: pandas.DataFrame with price/time columns (expected by backtester).",
        "    Returns a list of trade events (placeholder).",
        "    \"\"\"",
        "    trades = []",
        "    # ----- generated rules -----"
    ]

    if strategy.buy_rules:
        for i, br in enumerate(strategy.buy_rules, start = 1):
            header.append("    " + "BUY rule {i}")
            header.append("    " + _fmt_condition(br.condition))
    else:
        header.append("    " + "# no BUY rules defined")

    if strategy.sell_rules:
        for i, sr in enumerate(strategy.sell_rules, start=1):
            header.append("    " + "# SELL rule {i}")
            header.append("    " + _fmt_condition(sr.condition))
    else:
        header.append("    " + "# no SELL rules defined")

    footer = [
        "    return trades"
    ]

    return "\n".join(header + footer)

#DEMO
if __name__ == '__main__':
    s = StrategyNode(buy_rules=[], sell_rules=[])
    print(generate_python(s))
    