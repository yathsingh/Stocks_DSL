import re
from typing import Dict, Any, List, Optional


def normalize_number(text: str) -> float:
    """Shorthand support"""

    text = text.lower().strip()

    if text.endswith("m"):
        return float(text[:-1]) * 1_000_000

    if text.endswith("k"):
        return float(text[:-1]) * 1_000

    return float(text)


def parse_lookback_phrase(text: str) -> Optional[Dict[str, Any]]:
    """Detects lookback."""

    t = text.lower().strip()

    if "yesterday" in t or "previous" in t or "last session" in t:
        for name in ["high", "low", "close", "open", "volume"]:
            if name in t:
                return {
                    "type": "operand",
                    "kind": "lookback",
                    "name": name,
                    "offset": 1
                }

    match = re.search(r"(\d+)\s*(days?|bars?)\s*(ago|back)?", t)
    if match:
        offset = int(match.group(1))
        for name in ["high", "low", "close", "open", "volume"]:
            if name in t:
                return {
                    "type": "operand",
                    "kind": "lookback",
                    "name": name,
                    "offset": offset
                }

    match2 = re.search(r"look\s*back\s*(\d+)", t)
    if match2:
        offset = int(match2.group(1))
        for name in ["high", "low", "close", "open", "volume"]:
            if name in t:
                return {
                    "type": "operand",
                    "kind": "lookback",
                    "name": name,
                    "offset": offset
                }

    return None


def parse_indicator(text: str) -> Optional[Dict[str, Any]]:
    """Detects technical indicators."""

    t = text.lower().strip()

    sma_prefix = re.search(r"(sma|simple moving average|moving average)[\s\(]*(\d+)", t)

    if sma_prefix:

        period = int(sma_prefix.group(2))

        return {
            "type": "operand",
            "kind": "indicator",
            "name": "SMA",
            "args": ["close", period]
        }

    sma_suffix = re.search(r"(\d+)[-\s]*(day)?\s*(sma|simple moving average|moving average)", t)

    if sma_suffix:

        period = int(sma_suffix.group(1))
        return {
            "type": "operand",
            "kind": "indicator",
            "name": "SMA",
            "args": ["close", period]
        }


    rsi_match = re.search(r"(rsi|relative strength index)[\s\(]*(\d+)", t)

    if rsi_match:

        period = int(rsi_match.group(2))
        return {
            "type": "operand",
            "kind": "indicator",
            "name": "RSI",
            "args": ["close", period]
        }

    return None


def parse_basic_operand(text: str) -> Optional[Dict[str, Any]]:
    """Detects crossover events."""

    lowered = text.lower()

    for name in ["open", "high", "low", "close", "volume"]:
        if re.search(rf"\b{name}\b", lowered):
            return {
                "type": "operand",
                "kind": "identifier",
                "name": name
            }

    return None


def parse_cross_condition(sentence: str) -> Optional[Dict[str, Any]]:

    s = sentence.lower()

    if "cross" not in s:
        return None

    direction = None
    if "crosses above" in s:
        direction = "ABOVE"
    elif "crosses below" in s:
        direction = "BELOW"

    if not direction:
        return None

    left_part, right_part = re.split(r"crosses (?:above|below)", s, maxsplit=1)

    left_operand = (
        parse_indicator(left_part)
        or parse_lookback_phrase(left_part)
        or parse_basic_operand(left_part)
    )

    right_operand = (
        parse_indicator(right_part)
        or parse_lookback_phrase(right_part)
        or parse_basic_operand(right_part)
    )

    if left_operand and right_operand:
        return {
            "type": "cross",
            "left": left_operand,
            "direction": direction,
            "right": right_operand,
        }

    return None


def nl_to_struct(nl_text: str) -> Dict[str, List[Dict[str, Any]]]:
    """Main nl -> struct converter function."""

    text = nl_text.lower()

    entry_conditions: List[Dict[str, Any]] = []
    exit_conditions: List[Dict[str, Any]] = []

    sentences = re.split(r"[.,]", text)

    for sent in sentences:
        
        s = sent.strip()
        if not s:
            continue

        if any(word in s for word in ["sell", "exit", "close position"]):
            target = exit_conditions
        else:
            target = entry_conditions

        s = re.sub(r"\b(buy|sell|enter|exit|close position|when)\b", "", s).strip()

        cross = parse_cross_condition(s)
        if cross:
            target.append(cross)
            continue

        indicator = parse_indicator(s)

        if indicator:

            num_match = re.search(r"(above|below|>|<)\s*(\d+(\.\d+)?[mk]?)", s)
            if num_match:
                op_word, num_text = num_match.group(1), num_match.group(2)
                try:
                    right_val = normalize_number(num_text)
                except:
                    continue

                op = ">" if op_word in ("above", ">") else "<"

                target.append({
                    "type": "comparison",
                    "left": indicator,
                    "op": op,
                    "right": right_val,
                })
                continue

            op = ">" if ("above" in s or "greater than" in s or ">" in s) else "<"
            left = parse_basic_operand(s) or {
                "type": "operand",
                "kind": "identifier",
                "name": "close"
            }

            target.append({
                "type": "comparison",
                "left": left,
                "op": op,
                "right": indicator,
            })
            continue

        comp_match = re.search(r"(\w+)\s*(above|below|>|<)\s*([\w\.]+)", s)

        if comp_match:

            left_word, op_word, right_word = comp_match.groups()

            left = (
                parse_basic_operand(left_word)
                or parse_lookback_phrase(left_word)
            )

            if not left:
                continue

            op = ">" if op_word in ("above", ">") else "<"

            try:
                right_val = normalize_number(right_word)

            except:
                continue

            target.append({
                "type": "comparison",
                "left": left,
                "op": op,
                "right": right_val,
            })

    return {
        "entry": entry_conditions,
        "exit": exit_conditions,
    }
