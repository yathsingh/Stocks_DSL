from .ast_nodes import StrategyNode, BuyRuleNode, SellRuleNode, ConditionNode
from dsl.tokenizer import tokenize

def parse_strategy(dsl_text: str):
    "Placeholder basic parcer"

    lines = dsl_text.strip().split("\n")

    tokenized = [tokenize(line) for line in lines]

    #Mock empty logic to improve later
    return StrategyNode(buy_rules=[], sell_rules=[])