# Top-level Structure

STRATEGY  ::= [ENTRY_BLOCK] [EXIT_BLOCK]

ENTRY_BLOCK ::= "ENTRY:" NEWLINE RULE_LIST

EXIT_BLOCK  ::= "EXIT:" NEWLINE RULE_LIST

RULE_LIST ::= RULE (NEWLINE RULE)*


# Rule / Expression Grammar

RULE ::= EXPR

EXPR ::= TERM ( ( "AND" | "OR" ) TERM ) 

TERM ::= FACTOR | "(" EXPR ")"

FACTOR ::= COMPARISON | CROSS_EVENT

COMPARISON ::= OPERAND COMP_OP OPERAND 

COMP_OP ::= ">" | "<" | ">=" | "<=" | "==" 

OPERAND ::= IDENTIFIER | NUMBER | INDICATOR | LOOKBACK_IDENTIFIER


# Indicator Syntax

INDICATOR ::= IDENT_NAME "(" ARG_LIST ")"

ARG_LIST ::= ARG ("," ARG)*

ARG ::= IDENTIFIER | NUMBER

IDENT_NAME ::= "SMA" | "RSI"   


# Cross Events

CROSS_EVENT ::= "CROSS" "(" OPERAND "," DIRECTION "," OPERAND ")"

DIRECTION ::= "\"ABOVE\"" | "\"BELOW\""   

LOOKBACK_IDENTIFIER ::= IDENTIFIER "[" INT "]"


# Basic Tokens

IDENTIFIER ::= "open" | "high" | "low" | "close" | "volume" | "price"

NUMBER ::= integer | float

INT ::= [0-9]+

NEWLINE ::= "\n"

WHITESPACE: ignored between tokens

COMMENTS: lines starting with "#" are ignored by the tokenizer/parser


# Examples that can be copy pasted

# 1. simple entry + exit example

ENTRY:
close > SMA(close,20) AND volume > 1000000
EXIT:
RSI(close,14) < 30

# 2. cross-event example

ENTRY: 
CROSS(close, "ABOVE", SMA(close,20))

# 3. lookback example (yesterday's high)

ENTRY:
close > high[1]

# 4. parentheses & OR example

ENTRY:
(close > SMA(close,20) AND volume > 1000000) OR RSI(close,14) < 30


# Assumptions

Square brackets '[' and ']' indicate optional.

Star '*' indicates zero or more repetitions.

Operator precedence is left-associative.

Keywords and identifiers are case-insensitive for usability.

Volume is a numeric column (no human shorthand like '1M' in grammar).

Natural-language normalization (e.g., "yesterday") will be handled separately, mapping those into lookbacks or numbers before parsing.

Grammar intentionally avoids ambiguous constructs and focuses on determinism.