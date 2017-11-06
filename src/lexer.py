from tokens import *

###############################################################################
#                                                                             #
#   LEXER                                                                     #
#                                                                             #
###############################################################################

RESERVED_KEYWORDS = {
    "SELECT": Token("SELECT", "SELECT"),
    "FROM": Token("FROM", "FROM"),
    "WHERE": Token("WHERE", "WHERE"),
    "IN": Token(OP, "IN"),
    "CONTAINS": Token(OP, "CONTAINS"),
    "SET": Token("SET", "SET"),
    "DEFUN": Token("DEFUN", "DEFUN"),
    "BEGIN": Token("BEGIN", "BEGIN"),
    "END": Token("END", "END"),
    "ECHO": Token("ECHO", "ECHO"),
}

# TODO: add INT
class Lexer(object):
    def __init__(self, text):
        # string input
        self.text = text
        # self.pos is index into self.text
        self.pos = 0
        # current char
        self.current_char = self.text[0]
    def error(self):
        raise Exception("LEXING ERROR: %s" % self.text[self.pos])
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        else:
            return self.text[peek_pos]
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    def _id(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        return RESERVED_KEYWORDS.get(result, Token(ID, result))
    def _str(self):
        result = ""
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        return result
    def get_next_token(self):
        # tokenizer
        text = self.text
        while self.current_char == " " or self.current_char == "\n":
            self.advance()
        if self.pos >= len(text):
            return Token(EOF, None)
        while self.current_char is not None:
            # RESERVED_KEYWORDS & ID
            if self.current_char.isalnum():
                return self._id()
            elif self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")
            elif self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")
            elif self.current_char == ":":
                self.advance()
                return Token(COLON, ":")
            elif self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")
            elif self.current_char == '"':
                self.advance()
                result = self._str()
                self.advance()
                return Token(STR, result)
            elif self.current_char == "-" and self.peek() == ">":
                self.advance()
                self.advance()
                return Token(ARROW, "->")
            elif self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")
            elif self.current_char == "*":
                self.advance()
                return Token(STAR, "*")
            elif self.current_char in ["=", "|", "&"]:
                op = self.current_char
                self.advance()
                return Token(OP, op)
        self.error()
