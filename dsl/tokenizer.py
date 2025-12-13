import re 
from dataclasses import dataclass  
from typing import List, Iterator


@dataclass
class Token: 
    """A token produced by the DSL tokenizer."""
    
    type: str       
    value: str      
    line: int      
    col: int      

    def __repr__(self) -> str:

        return f"Token({self.type!r}, {self.value!r}, line={self.line}, col={self.col})"
    
    
_TOKEN_SPEC = [
    ("NUMBER",   r"\d+(?:\.\d+)?"),               # 123 or 12.34
    ("STRING",   r"\"[^\"]*\""),                  # "ABOVE" or "BELOW" 
    ("OP",       r">=|<=|==|>|<"),                # comparison ops
    ("COMMA",    r","),                           # comma
    ("LPAREN",   r"\("),                          # left parenthesis
    ("RPAREN",   r"\)"),                          # right parenthesis
    ("LBRACK",   r"\["),                          # left bracket for lookbacks
    ("RBRACK",   r"\]"),                          # right bracket
    ("COLON",    r":"),                           # colon (for ENTRY: / EXIT:)
    ("IDENT",    r"[A-Za-z_][A-Za-z0-9_]*"),      # identifiers & keywords
    ("SKIP",     r"[ \t]+"),                      # spaces and tabs (ignored)
    ("MISMATCH", r"."),                           # any other single char -> error
]


_master_pat = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in _TOKEN_SPEC))


def tokenize_line(line: str, line_no: int) -> Iterator[Token]:
    "Tokenize a single line and yield Token objects."

    comment_start = line.find("#")
    if comment_start != -1:
        line = line[:comment_start]

    pos = 0 
    for mo in _master_pat.finditer(line):

        kind = mo.lastgroup 
        value = mo.group()   
        start = mo.start()   
  
        col = start + 1

        if kind == "NUMBER":
            yield Token("NUMBER", value, line_no, col)

        elif kind == "STRING":
            yield Token("STRING", value, line_no, col)

        elif kind == "IDENT":
            yield Token("IDENT", value, line_no, col)

        elif kind == "OP":
            yield Token("OP", value, line_no, col)

        elif kind in ("COMMA", "LPAREN", "RPAREN", "LBRACK", "RBRACK", "COLON"):
            yield Token(kind, value, line_no, col)

        elif kind == "SKIP":
            continue

        elif kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character {value!r} at line {line_no}, col {col}")
        
        pos = mo.end()  


def tokenize_text(text: str) -> List[Token]:
    "Tokenize multiline DSL text into flat list of Tokens"

    tokens: List[Token] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
  
        for tok in tokenize_line(line, i):
            tokens.append(tok)

    return tokens


TOKEN_TYPES = {
    "NUMBER", "STRING", "IDENT", "OP",
    "COMMA", "LPAREN", "RPAREN", "LBRACK", "RBRACK", "COLON"
}