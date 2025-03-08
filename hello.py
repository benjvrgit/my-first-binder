import re
from typing import List, Tuple

# Define token types and their regex patterns.
TOKEN_SPECIFICATION = [
    ('NUMBER',      r'\d+'),                   # Integer or decimal number
    ('ID',          r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
    ('OP',          r'[+\-*/=><]'),              # Arithmetic operators
    ('PUNCT',       r'[(){};]'),               # Punctuation
    ('SKIP',        r'[ \t]+'),                # Skip over spaces and tabs
    ('NEWLINE',     r'\n'),                    # Line endings
    ('MISMATCH',    r'.'),                     # Any other character
]

# Compile the regex into a master pattern
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tok_regex).match

# Keywords for our toy language
KEYWORDS = {'if', 'else', 'while', 'return'}

def lexer(code: str) -> List[Tuple[str, str, int]]:
    """
    Lexical analyzer that returns a list of tokens.
    Each token is represented as a tuple: (token_type, token_value, position).
    """
    pos = 0
    tokens = []
    line = 1
    mo = get_token(code, pos)
    while mo is not None:
        typ = mo.lastgroup
        val = mo.group(typ)
        if typ == 'NEWLINE':
            line += 1
        elif typ == 'SKIP':
            pass
        elif typ == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {val!r} on line {line}')
        else:
            # Check if the identifier is a keyword.
            if typ == 'ID' and val in KEYWORDS:
                typ = val.upper()
            tokens.append((typ, val, pos))
        pos = mo.end()
        mo = get_token(code, pos)
    return tokens

# Sample input for testing
sample_code = """
if (count = 42) {
    return count + 1;
} else {
    while (count < 100) {
        count = count + 1;
    }
}
"""

# Run the lexer on the sample code
tokens = lexer(sample_code)
for token in tokens:
    print(token)
