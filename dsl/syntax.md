# Top-Level Structure

STRATEGY ::= [ENTRY_BLOCK] [EXIT_BLOCK]

ENTRY_BLOCK ::= "ENTRY:" [RULE] NEWLINE* RULE_LIST
EXIT_BLOCK  ::= "EXIT:"  [RULE] NEWLINE* RULE_LIST

RULE_LIST ::= RULE ( NEWLINE* RULE )*


# Rule / Expression Grammar

RULE ::= EXPR

EXPR ::= TERM ( ( "AND" | "OR" ) TERM )*


TERM ::= FACTOR | "(" EXPR ")"

FACTOR ::= COMPARISON | CROSS_EVENT


# Comparison Expressions

COMPARISON ::= OPERAND COMP_OP OPERAND

COMP_OP ::= ">" | "<" | ">=" | "<=" | "=="


# Operands

OPERAND ::= IDENTIFIER | NUMBER | STRING | INDICATOR | LOOKBACK_IDENTIFIER


# Indicator Syntax

INDICATOR ::= IDENT_NAME "(" ARG_LIST ")"

ARG_LIST ::= ARG ("," ARG)*

ARG ::= IDENTIFIER | NUMBER | STRING

IDENT_NAME ::= "SMA" | "RSI"


# Cross Events

CROSS_EVENT ::= "CROSS" "(" OPERAND "," DIRECTION "," OPERAND ")"

DIRECTION ::= "ABOVE" | "BELOW"


# Lookbacks

LOOKBACK_IDENTIFIER ::= IDENTIFIER "[" INT "]"


# Basic Tokens

IDENTIFIER ::= "open" | "high" | "low" | "close" | "volume" | "price"

NUMBER     ::= integer | float
STRING     ::= "\"" characters "\""
INT        ::= [0-9]+

NEWLINE    ::= "\n"

WHITESPACE : ignored between tokens
COMMENTS   : lines beginning with "#" are ignored


# Examples

# 1. Simple entry + exit
ENTRY:
close > SMA(close,20) AND volume > 1000000

EXIT:
RSI(close,14) < 30


# 2. Cross event
ENTRY:
CROSS(close, "ABOVE", SMA(close,20))


# 3. Lookback example
ENTRY:
close > high[1]


# 4. Parentheses & OR
ENTRY:
(close > SMA(close,20) AND volume > 1000000) OR RSI(close,14) < 30


# Assumptions

1. Square brackets '[X]' represent optional components.
2. '*' indicates zero or more repetitions.
3. Boolean operators are left-associative.
4. Keywords and identifiers are case-insensitive.
5. Natural-language expressions ("yesterday", "last week") are normalized
   BEFORE reaching this grammar.
6. Grammar is intentionally LL(1) and unambiguous to support recursive descent.
