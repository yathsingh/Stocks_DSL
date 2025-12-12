from typing import Set, Dict

COMPARISON_OPS: Set[str] = {">", "<", ">=", "<=", "=="}

COMPARISON_TO_PY: Dict[str, str] = {
    ">": ">",
    "<": "<",
    ">=": ">=",
    "<=": "<=",
    "==": "==",
}

LOGICAL_OPS: Set[str] = {"AND", "OR", "NOT"}

LOGICAL_PRECEDENCE: Dict[str, int] = {
    "NOT": 3,
    "AND": 2,
    "OR": 1,
}


def canonicalize_logical(op: str) -> str:
    "Convert a logical operator token to its canonical uppercase form."
    
    return op.strip().upper()


def is_logical_op(tok: str) -> bool:
    "Return True if the token (any-case) is a supported logical operator."

    return canonicalize_logical(tok) in LOGICAL_OPS


def is_comparison_op(tok: str) -> bool:
    "Return True if the token is a supported comparison operator."

    return tok in COMPARISON_OPS


def get_python_comparison(tok: str) -> str:
    "Return the Python operator string for a comparison token."

    return COMPARISON_TO_PY[tok]


def get_logical_precedence(tok: str) -> int:
    "Return precedence integer for a logical operator token."

    return LOGICAL_PRECEDENCE[canonicalize_logical(tok)]