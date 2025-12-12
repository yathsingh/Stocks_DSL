from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class StrategyNode:
    entry: Optional["EntryBlockNode"]
    exit: Optional["ExitBlockNode"]

    def __repr__(self):
        return f"StrategyNode(entry={self.entry}, exit={self.exit})"


@dataclass
class EntryBlockNode:
    rules: List[Any]   

    def __repr__(self):
        return f"EntryBlockNode(rules={self.rules})"


@dataclass
class ExitBlockNode:
    rules: List[Any]

    def __repr__(self):
        return f"ExitBlockNode(rules={self.rules})"


@dataclass
class LogicalOpNode:
    op: str            # AND / OR
    left: Any
    right: Any

    def __repr__(self):
        return f"LogicalOpNode({self.op}, {self.left}, {self.right})"


@dataclass
class CompareNode:
    left: Any
    op: str            # >, <, >=, <=, ==
    right: Any

    def __repr__(self):
        return f"CompareNode({self.left} {self.op} {self.right})"


@dataclass
class CrossNode:
    left: Any
    direction: str     # ABOVE / BELOW
    right: Any

    def __repr__(self):
        return f"CrossNode({self.left}, {self.direction}, {self.right})"


@dataclass
class IdentifierNode:
    name: str

    def __repr__(self):
        return f"Identifier({self.name})"


@dataclass
class NumberNode:
    value: float

    def __repr__(self):
        return f"Number({self.value})"


@dataclass
class LookbackNode:
    name: str
    offset: int

    def __repr__(self):
        return f"Lookback({self.name}[{self.offset}])"


@dataclass
class IndicatorCallNode:
    name: str            # SMA, RSI, etc.
    args: List[Any]      # list of operands or numbers

    def __repr__(self):
        return f"IndicatorCall({self.name}, args={self.args})"
