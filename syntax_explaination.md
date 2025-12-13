**Format**

Our grammar format uses a standard EBNF-style notation.

1. ::= is the production operator, representing 'is defined as'

2. [] represents optional items.

3. * stands for 'zero or more'. It allows multiple AND/OR pairs in a single expression.

4. () denote grouping and control operator precedence in expressions.

5. | represents alternatives seaprated by OR.


**Analysis of Notation Methodology**

The grammar is designed so that:

1. Each production begins with a token or pattern that uniquely identifies it.
   This guarantees deterministic parsing with only one token of lookahead (LL(1)).

2. The parser never needs backtracking.

3. Error messages remain clear because branching is predictable.

4. This keeps the DSL extremely easy to debug, extend, and reason about.


**Grammar Details**

*A. Top-level Structure*

1. Parsing strategy may have

only ENTRY,

only EXIT,

or both, but ENTRY must come first.

2. ENTRY can have

a rule immediately after colon
(eg. ENTRY: close > 10),

or begin on the next line
(eg. ENTRY:
close > 10)

NOTE: Parser does not enforce NEWLINE. 
It simply expects COLON then parses rules until EXIT or EOF.

3. EXIT works similar as ENTRY.

4. Newline is not mandatory for rule separation. 

Rule boundaries are detected structurally. 

When EXPR finishes, the next token either begins the next EXPR or marks the end of the block.
This structural boundary detection eliminates whitespace dependency.


*B. Rule/Expression Grammar*

1. Every rule is a pure boolean expression maps cleanly to boolean AST nodes
   to avoid syntactic noise.

This simplifies AST structure and matches trading domain semantics.

2. Left associative.

eg. A AND B AND C OR D  →  (((A AND B) AND C) OR D)

3. Equal precedence between AND and OR simplifies the grammar and the implementation.
   Users expecting different precedence can use parentheses.

4. An operand can be: (type: example)

    4.1. A data series: close

    4.2. A literal: 100.0

    4.3. A string: "ABOVE"

    4.4. An indicator: SMA(close,20)

    4.5. A lookback reference: high[1]

5. CROSS expresses temporal transitions, not static comparisons. 
It is a first-class function to prevent ambiguity.

eg. CROSS(close, "ABOVE", SMA(close,20))

6. Static integers used in lookback identifiers to ensure deterministic evaluation.

7. Whitespace is ignored except where distinguishing tokens. Comments are ignored.

8. Keywords and identifiers are case-insensitive.