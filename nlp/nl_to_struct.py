import re
from typing import Dict, Any, List, Optional


def normalize_number(text: str) -> float:
    text = text.lower().strip()

    if text.endswith("m"):        # 1m = 1,000,000
        return float(text[:-1]) * 1_000_000

    if text.endswith("k"):        # 100k = 100,000
        return float(text[:-1]) * 1_000

    return float(text)


def parse_lookback_phrase(text: str) -> Optional[Dict[str, Any]]:
    text = text.lower()

    if "yesterday" in text or "previous" in text:
    
        if "high" in text:
            return {"type": "operand", "kind": "lookback", "name": "high", "offset": 1}
        if "low" in text:
            return {"type": "operand", "kind": "lookback", "name": "low", "offset": 1}
        if "close" in text:
            return {"type": "operand", "kind": "lookback", "name": "close", "offset": 1}

    return None



def parse_indicator(text: str) -> Optional[Dict[str, Any]]:
    t = text.lower().strip()

    sma_match = re.search(r"(\d+)[-\s]*day moving average", t)
    if sma_match:
        period = int(sma_match.group(1))
        return {
            "type": "operand",
            "kind": "indicator",
            "name": "SMA",
            "args": ["close", period]
        }

    rsi_match = re.search(r"rsi[\s\(]*(\d+)", t)
    if rsi_match:
        period = int(rsi_match.group(1))
        return {
            "type": "operand",
            "kind": "indicator",
            "name": "RSI",
            "args": ["close", period]
        }

    return None


def parse_basic_operand(text: str) -> Optional[Dict[str, Any]]:
    lowered = text.lower()

    for name in ["open", "high", "low", "close", "volume"]:
        if name in lowered:
            return {"type": "operand", "kind": "identifier", "name": name}

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

    left_part, right_part = re.split(r"crosses (above|below)", s, maxsplit=1)

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

    text = nl_text.lower()

    entry_conditions: List[Dict[str, Any]] = []
    exit_conditions: List[Dict[str, Any]] = []

    sentences = re.split(r"[.,]", text)

    for sent in sentences:
        s = sent.strip()
        if not s:
            continue

        target = None
        if any(word in s for word in ["buy", "enter", "go long"]):
            target = entry_conditions
        elif any(word in s for word in ["sell", "exit", "close position"]):
            target = exit_conditions
        else:
            
            target = entry_conditions

        cross = parse_cross_condition(s)
        if cross:
            target.append(cross)
            continue

        indicator = parse_indicator(s)
        if indicator:
           
            if "above" in s or "greater than" in s or ">" in s:
                op = ">"
                right = indicator
            else:
                op = "<"
                right = indicator

            left = parse_basic_operand(s) or {"type": "operand", "kind": "identifier", "name": "close"}

            target.append({
                "type": "comparison",
                "left": left,
                "op": op,
                "right": right,
            })
            continue

        look = parse_lookback_phrase(s)

        comp_match = re.search(r"(\w+)\s*(above|below|>|<)\s*([\w\.]+)", s)
        if comp_match:
            left_word, op_word, right_word = comp_match.groups()

            left = (
                parse_basic_operand(left_word)
                or parse_lookback_phrase(left_word)
            )

            if not left:
                continue

            if op_word in ("above", ">"):
                op = ">"
            else:
                op = "<"

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
