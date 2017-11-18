ID, LPAREN, RPAREN, SEMI, EOF = \
"ID", "LPAREN", "RPAREN", "SEMI", "EOF"
DEFUN, COLON, ARROW, COMMA = "DEFUN", "COLON", "ARROW", "COMMA"
QMARK = "QMARK"
BEGIN, END = "BEGIN", "END"

OP = "OP"
INT, STR, BOOL = "INT", "STR", "BOOL"
SELECT, FROM, WHERE = "SELECT", "FROM", "WHERE"
IN, CONTAINS = "IN", "CONTAINS"
LIST = "LIST"
ECHO = "ECHO"

class Token(object):
    def __init__(self, token_type, token_value):
        # token types listed at top of file
        self.type = token_type
        # token values: e.g. MATH412
        self.value = token_value
    def __str__(self):
        return "Token(%s, %s)" % (self.type, repr(self.value))
    __repr__ = __str__
