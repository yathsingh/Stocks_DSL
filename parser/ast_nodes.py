class ASTNode:
    "Base class"
    pass

class ConditionNode(ASTNode):
    def __init__(self, indicator, operator, value):
        self.indicator = indicator
        self.operator = operator
        self.value = value

class BuyRuleNode(ASTNode):
    def __init__(self, condition):
        self.condition = condition

class SellRuleNode(ASTNode):
    def __init__(self, condition):
        self.condition = condition

class StrategyNode(ASTNode):
    def __init__(self, buy_rules, sell_rules):
        self.buy_rules = buy_rules
        self.sell_rules = sell_rules