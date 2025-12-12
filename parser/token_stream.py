from typing import List, Optional
from dsl.tokenizer import Token


class TokenStream:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0 

    # Basic operations

    def peek(self) -> Optional[Token]:
        """Return the current token without consuming it."""

        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def next(self) -> Optional[Token]:
        """Consume the current token and advance."""

        if self.pos >= len(self.tokens):
            return None
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    # Conditional match

    def match(self, type_: str, value: Optional[str] = None) -> Optional[Token]:
        """
        If the current token matches both type (and optionally value),
        consume and return it. Otherwise return None.
        """

        tok = self.peek()
        if tok is None:
            return None

        if tok.type != type_:
            return None
        
        if value is not None and tok.value.upper() != value.upper():
            return None

        return self.next()


    # Required match

    def expect(self, type_: str, value: Optional[str] = None) -> Token:
        """
        Same as match(), but throws a readable error if the expected
        token is not present.
        """

        tok = self.match(type_, value)
        if tok is None:
            expected = f"{type_}" if value is None else f"{type_}({value})"
            actual = self.peek()
            if actual:
                raise SyntaxError(
                    f"Expected {expected}, got {actual.type}({actual.value}) "
                    f"at line {actual.line}, col {actual.col}"
                )
            else:
                raise SyntaxError(f"Expected {expected}, but hit end of input")
        return tok

    # End-of-input helper

    def at_end(self) -> bool:
        """True if the stream has no more tokens."""
        return self.pos >= len(self.tokens)
