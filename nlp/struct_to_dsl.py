from typing import Dict, Any, List


def operand_to_dsl(op: Dict[str, Any]) -> str:

    kind = op["kind"]

    # Identifier → close / high / volume
    if kind == "identifier":
        return op["name"]

    # Lookback → high[1]
    if kind == "lookback":
        return f"{op['name']}[{op['offset']}]"

    # Indicator → SMA(close,20)
    if kind == "indicator":
        name = op["name"].upper()
        args = op["args"]
        arg_strs = []

        for a in args:
            if isinstance(a, dict):  
                arg_strs.append(operand_to_dsl(a))
            else:
                arg_strs.append(str(a))

        return f"{name}({', '.join(arg_strs)})"

    raise ValueError(f"Unknown operand kind {kind}")


def comparison_to_dsl(node: Dict[str, Any]) -> str:

    left = node["left"]
    right = node["right"]
    op = node["op"]

    left_str = operand_to_dsl(left)

    if isinstance(right, dict):
        right_str = operand_to_dsl(right)
    else:
        right_str = str(right)

    return f"{left_str} {op} {right_str}"


def cross_to_dsl(node: Dict[str, Any]) -> str:

    left = operand_to_dsl(node["left"])
    right = operand_to_dsl(node["right"])
    direction = '"' + node["direction"].upper() + '"'
    return f"CROSS({left}, {direction}, {right})"


def rule_to_dsl(rule: Dict[str, Any]) -> str:

    rtype = rule["type"]

    if rtype == "comparison":
        return comparison_to_dsl(rule)

    if rtype == "cross":
        return cross_to_dsl(rule)

    raise ValueError(f"Unknown rule type {rtype}")


def struct_to_dsl(struct: Dict[str, Any]) -> str:

    entry_rules = struct.get("entry", [])
    exit_rules = struct.get("exit", [])

    lines: List[str] = []

    # ENTRY BLOCK
    if entry_rules:
        lines.append("ENTRY:")
        for rule in entry_rules:
            lines.append(rule_to_dsl(rule))
        lines.append("")  # blank line after block

    # EXIT BLOCK
    if exit_rules:
        lines.append("EXIT:")
        for rule in exit_rules:
            lines.append(rule_to_dsl(rule))
        lines.append("")

    return "\n".join(lines).rstrip()
