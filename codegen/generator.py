import pandas as pd

from parser.ast_nodes import (
    IdentifierNode,
    NumberNode,
    LookbackNode,
    IndicatorCallNode,
    CompareNode,
    LogicalOpNode,
    CrossNode,
)


def sma(series, period):
    """Compute Simple Moving Average."""

    period = int(period)

    return series.rolling(window=period, min_periods=period).mean()


def rsi(series, period):
    """Compute RSI using a standard Wilder-like formula."""

    period = int(period)
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.ewm(alpha=1/period, adjust=False).mean()
    roll_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = roll_up / (roll_down.replace(0, 1e-9))

    return 100 - (100 / (1 + rs))


def _expr_to_code(node):
    """Converts AST expression node → Python code string."""

    if isinstance(node, IdentifierNode):
        return f'df["{node.name}"]'

    if isinstance(node, NumberNode):
        return str(node.value)

    if isinstance(node, LookbackNode):
        return f'df["{node.name}"].shift({node.offset})'

    if isinstance(node, IndicatorCallNode):
        args = [_expr_to_code(arg) for arg in node.args]
        return f'{node.name.lower()}({", ".join(args)})'

    if isinstance(node, CompareNode):
        left = _expr_to_code(node.left)
        right = _expr_to_code(node.right)
        return f'({left} {node.op} {right})'

    if isinstance(node, LogicalOpNode):
        if node.op == "NOT":
            right = _expr_to_code(node.right)
            return f'(~({right}))'

        left = _expr_to_code(node.left)
        right = _expr_to_code(node.right)

        if node.op == "AND":
            return f'(({left}) & ({right}))'
        if node.op == "OR":
            return f'(({left}) | ({right}))'

    if isinstance(node, CrossNode):
        left = _expr_to_code(node.left)
        right = _expr_to_code(node.right)
        if node.direction.upper() == "ABOVE":
            return (
                f"(({left}.shift(1) < {right}.shift(1)) & "
                f"({left} >= {right}))"
            )
        else:
            return (
                f"(({left}.shift(1) > {right}.shift(1)) & "
                f"({left} <= {right}))"
            )

    raise TypeError(f"Unsupported AST node: {type(node).__name__}")


def _gen_rule_series_code(rules, series_name):
    """Converts rule list → Python code lines."""
    
    lines = []

    if not rules:
        lines.append(f"{series_name} = pd.Series(False, index=df.index)")
        return lines

    temp_vars = []

    for i, rule in enumerate(rules, start=1):
        expr = _expr_to_code(rule)
        var = f"r{i}"
        temp_vars.append(var)
        lines.append(f"{var} = ({expr})")

    lines.append(f"{series_name} = ({' | '.join(temp_vars)})")
    return lines


def generate_python(strategy):
    """Main python code generator"""

    lines = []
    lines.append("import pandas as pd")
    lines.append("")

    # Indicators
    lines.append("def sma(series, period):")
    lines.append("    return series.rolling(window=int(period), min_periods=1).mean()")
    lines.append("")
    lines.append("def rsi(series, period):")
    lines.append("    period = int(period)")
    lines.append("    delta = series.diff()")
    lines.append("    up = delta.clip(lower=0)")
    lines.append("    down = -1 * delta.clip(upper=0)")
    lines.append("    ma_up = up.ewm(alpha=1/period, adjust=False).mean()")
    lines.append("    ma_down = down.ewm(alpha=1/period, adjust=False).mean()")
    lines.append("    rs = ma_up / (ma_down.replace(0, 1e-9))")
    lines.append("    return 100 - (100 / (1 + rs))")
    lines.append("")

    # Strategy evaluation function
    lines.append("def evaluate_strategy(df):")

    # ENTRY BLOCK
    if strategy.entry:
        for l in _gen_rule_series_code(strategy.entry.rules, "entry_signal"):
            lines.append("    " + l)
    else:
        lines.append("    entry_signal = pd.Series(False, index=df.index)")

    # EXIT BLOCK
    if strategy.exit:
        for l in _gen_rule_series_code(strategy.exit.rules, "exit_signal"):
            lines.append("    " + l)
    else:
        lines.append("    exit_signal = pd.Series(False, index=df.index)")

    lines.append("    entry_signal = entry_signal.fillna(False)")
    lines.append("    exit_signal = exit_signal.fillna(False)")
    lines.append("    return {'entry': entry_signal, 'exit': exit_signal}")
    lines.append("")

    return "\n".join(lines)
