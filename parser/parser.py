from typing import List, Optional
from dsl.tokenizer import tokenize_text, Token
from parser.token_stream import TokenStream
from dsl.operators import (
    is_logical_op,
    is_comparison_op,
    canonicalize_logical,
)
from dsl.indicators import is_supported
from parser.ast_nodes import (
    StrategyNode,
    EntryBlockNode,
    ExitBlockNode,
    CompareNode,
    LogicalOpNode,
    IdentifierNode,
    NumberNode,
    LookbackNode,
    IndicatorCallNode,
    CrossNode,
)


def parse_strategy_text(text: str) -> StrategyNode:
    """
    Top-level function used by main.py:
        DSL text → AST StrategyNode
    """

    tokens = tokenize_text(text)
    stream = TokenStream(tokens)
    return parse_strategy(stream)


def parse_strategy(ts: TokenStream) -> StrategyNode:
    """
    STRATEGY ::= [ENTRY_BLOCK] [EXIT_BLOCK]
    Order is always ENTRY first, EXIT second.
    Both are optional, but at least one must exist.
    """

    entry_block = None
    exit_block = None

    if ts.match("IDENT", "ENTRY"):

        ts.expect("COLON")
        entry_rules = parse_rule_list(ts)
        entry_block = EntryBlockNode(entry_rules)

    if ts.match("IDENT", "EXIT"):

        ts.expect("COLON")
        exit_rules = parse_rule_list(ts)
        exit_block = ExitBlockNode(exit_rules)

    if entry_block is None and exit_block is None:

        raise SyntaxError("A strategy must contain ENTRY: and/or EXIT:")

    return StrategyNode(entry_block, exit_block)


def parse_rule_list(ts: TokenStream) -> List:
    """
    RULE_LIST ::= RULE (NEWLINE RULE)*
    We treat each line as one rule/expression.
    """

    rules = []

    while True:

        nexttok = ts.peek()

        if nexttok is None:

            break

        if nexttok.type == "IDENT" and nexttok.value.upper() in ("ENTRY", "EXIT"):

            break

        rules.append(parse_expr(ts))

        while ts.match("NEWLINE"):

            pass

        nexttok = ts.peek()

        if nexttok is None:

            break

        if nexttok.type == "IDENT" and nexttok.value.upper() in ("ENTRY", "EXIT"):

            break

    return rules


def parse_expr(ts: TokenStream):
    """
    EXPR ::= TERM ( (AND | OR) TERM )*
    Left-associative.
    """

    node = parse_term(ts)

    while True:

        tok = ts.peek()

        if tok and tok.type == "IDENT" and is_logical_op(tok.value):

            op = canonicalize_logical(ts.next().value)
            right = parse_term(ts)
            node = LogicalOpNode(op, node, right)

        else:

            break

    return node


def parse_term(ts: TokenStream):
    """
    TERM ::= FACTOR | "(" EXPR ")"
    """

    if ts.match("LPAREN"):

        inner = parse_expr(ts)
        ts.expect("RPAREN")
        return inner

    return parse_factor(ts)


def parse_factor(ts: TokenStream):
    """
    FACTOR ::= COMPARISON | CROSS_EVENT
    """
    
    tok = ts.peek()

    if tok and tok.type == "IDENT" and tok.value.upper() == "CROSS":

        return parse_cross_event(ts)

    left = parse_operand(ts)

    tok = ts.peek()

    if tok and tok.type == "OP" and is_comparison_op(tok.value):

        op = ts.next().value
        right = parse_operand(ts)
        return CompareNode(left, op, right)

    return left


def parse_operand(ts: TokenStream):
    tok = ts.peek()

    if tok is None:
        raise SyntaxError("Unexpected end while parsing operand")

    if tok.type == "NUMBER":

        ts.next()
        return NumberNode(float(tok.value))

    if tok.type == "STRING":

        ts.next()
        return tok.value.strip('"')  

    if tok.type == "IDENT":

        ident_tok = ts.next()
        name = ident_tok.value

        if ts.match("LBRACK"):

            idx_tok = ts.expect("NUMBER")
            ts.expect("RBRACK")
            return LookbackNode(name, int(idx_tok.value))

        if ts.match("LPAREN"):
            
            args = parse_arg_list(ts)
            ts.expect("RPAREN")

            if not is_supported(name):
                raise SyntaxError(f"Unknown indicator {name}")

            return IndicatorCallNode(name.upper(), args)

        return IdentifierNode(name)

    raise SyntaxError(f"Unexpected token {tok.type}({tok.value}) while parsing operand")


def parse_arg_list(ts: TokenStream):
    """
    ARG_LIST ::= ARG ("," ARG)*
    ARG ::= IDENT | NUMBER | STRING
    """
    args = []

    if ts.peek() and ts.peek().type == "RPAREN":
        return args

    args.append(parse_operand(ts))

    while ts.match("COMMA"):
        args.append(parse_operand(ts))

    return args


def parse_cross_event(ts: TokenStream):
    """
    CROSS_EVENT ::= CROSS "(" OPERAND "," DIRECTION "," OPERAND ")"
    DIRECTION ::= "ABOVE" or "BELOW" (STRING token)
    """

    ts.expect("IDENT", "CROSS")
    ts.expect("LPAREN")

    left = parse_operand(ts)
    ts.expect("COMMA")

    dir_tok = ts.expect("STRING")
    direction = dir_tok.value.strip('"').upper()

    if direction not in ("ABOVE", "BELOW"):
        
        raise SyntaxError(f"Invalid CROSS direction: {direction}")

    ts.expect("COMMA")
    right = parse_operand(ts)

    ts.expect("RPAREN")
    return CrossNode(left, direction, right)
