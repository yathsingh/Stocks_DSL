from pathlib import Path  
from lark import Lark, Transformer, v_args  


from parser.ast_nodes import (
    StrategyNode, BuyRuleNode, SellRuleNode,
    IdentifierNode, NumberNode, LookbackNode, IndicatorNode,
    CrossNode, CompareNode, LogicalOpNode
)


GRAMMAR_PATH = Path(__file__).parent / "dsl_grammar.lark"  
GRAMMAR = GRAMMAR_PATH.read_text()  


_lark = Lark(GRAMMAR, start="start", parser="lalr", propagate_positions=True)


# Transformer: Parse Tree -> AST

@v_args(inline=True)
class ToAST(Transformer):
    
    def IDENT(self, tok):
        return IdentifierNode(name=str(tok))

    def NUMBER(self, tok):
        return NumberNode(value=str(tok))

    def INT(self, tok):
        return int(str(tok))

    def STRING(self, tok):
        s = str(tok)
        return s[1:-1]
    

    def lookback(self, ident_node, idx):
        return LookbackNode(name=ident_node.name, offset=int(idx))

    def indicator_call(self, ident_node, *args):
        return IndicatorNode(name=ident_node.name.upper(), args=list(args))

    def grouped(self, expr):
        return expr

    def cross(self, *children):
        left, direction, right = children[0], children[1], children[2]
        return CrossNode(left=left, direction=direction, right=right)


    def compare(self, left, op_tok, right):
        return CompareNode(left=left, op=str(op_tok), right=right)

    def or_op(self, left, _op, right):
        return LogicalOpNode("OR", left, right)

    def and_op(self, left, _op, right):
        return LogicalOpNode("AND", left, right)

    def not_op(self, _op, operand):
        return LogicalOpNode("NOT", None, operand)

   
    def buy_line(self, *elems):
        expr = elems[-1]
        return BuyRuleNode(condition=expr)

    def sell_line(self, *elems):
        expr = elems[-1]
        return SellRuleNode(condition=expr)

    
    def expr_line(self, expr):
        return expr

   
    def entry_block(self, *rule_nodes):
        return ("ENTRY", list(rule_nodes))

    def exit_block(self, *rule_nodes):
        return ("EXIT", list(rule_nodes))


    def strategy(self, *blocks):

        buy_rules = []
        sell_rules = []

        for blk in blocks:

            if blk is None:

                continue

            typ, items = blk

            if typ == "ENTRY":

                for it in items:
                  
                    if isinstance(it, BuyRuleNode):
                        buy_rules.append(it)

                    else:
                        buy_rules.append(BuyRuleNode(condition=it))

            elif typ == "EXIT":

                for it in items:

                    if isinstance(it, SellRuleNode):
                        sell_rules.append(it)

                    else:
                        sell_rules.append(SellRuleNode(condition=it))


        return StrategyNode(buy_rules=buy_rules, sell_rules=sell_rules)


def parse_strategy_with_lark(text: str) -> StrategyNode:
    """
    Parse DSL text using Lark and return a StrategyNode AST.
    This function hides Lark's tree and returns our AST directly.
    Lark will raise lark.exceptions for syntax errors which the caller can catch.
    """

    tree = _lark.parse(text)        
    ast = ToAST().transform(tree)     
    return ast
