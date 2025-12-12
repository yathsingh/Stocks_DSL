from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ASTNode:
    """Base class for AST nodes (empty base for type clarity)."""

    pass


# 1. Primitive Nodes

@dataclass
class IdentifierNode(ASTNode):
    "Represents a bare identifier."

    name: str

    def __repr__(self):
        return f"Identifier({self.name!r})"


@dataclass
class NumberNode(ASTNode):
    "Represents a numeric literal (text preserved)."
    value: str

    def __repr__(self):
        return f"Number({self.value!r})"


# 2. Lookback Node

@dataclass
class LookbackNode(ASTNode):
    "Represents lookback like close[1]."

    name: str
    offset: int

    def __repr__(self):
        return f"Lookback({self.name!r}, {self.offset})"


# 3. Indicator Node

@dataclass
class IndicatorNode(ASTNode):
    "Represents an indicator call, holding canonical name and raw arg nodes."

    name: str
    args: List[ASTNode]

    def __repr__(self):
        return f"Indicator({self.name!r}, args={self.args!r})"


# 4. Cross Event Node 

class CrossNode(ASTNode):
    "Represents CROSS(left, direction, right), where direction is 'ABOVE' or 'BELOW'."

    left: ASTNode
    direction: str
    right: ASTNode

    def __repr__(self):
        return f"Cross({self.left!r}, {self.direction!r}, {self.right!r})"


# 5. Comparison Node

@dataclass
class CompareNode(ASTNode):
    "Binary comparison between two operands using operator like '>' or '<='."

    left: ASTNode
    op: str
    right: ASTNode

    def __repr__(self):
        return f"Compare({self.left!r} {self.op} {self.right!r})"


# 6. Logical Operators Node

@dataclass
class LogicalOpNode(ASTNode):
    "Logical operation node (AND, OR) with left/right. For NOT, right is the operand and left=None."

    op: str
    left: Optional[ASTNode]
    right: ASTNode

    def __repr__(self):
        if self.left is None:
            return f"LogicalOp({self.op!r} {self.right!r})"
        return f"LogicalOp({self.left!r} {self.op!r} {self.right!r})"


# 7. Rules and Strategy Container Nodes

@dataclass
class BuyRuleNode(ASTNode):
    "Holds the parsed condition AST for a BUY rule."

    condition: ASTNode

    def __repr__(self):
        return f"BuyRule({self.condition!r})"


@dataclass
class SellRuleNode(ASTNode):
    "Holds the parsed condition AST for a SELL rule."

    condition: ASTNode

    def __repr__(self):
        return f"SellRule({self.condition!r})"


@dataclass
class StrategyNode(ASTNode):
    "Top-level strategy container with buy_rules and sell_rules lists."
    
    buy_rules: List[BuyRuleNode]
    sell_rules: List[SellRuleNode]

    def __repr__(self):
        return f"StrategyNode(buy_rules={self.buy_rules!r}, sell_rules={self.sell_rules!r})"
