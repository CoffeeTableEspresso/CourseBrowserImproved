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
    "SET": Token("SET", "SET"),
    "BEGIN": Token("BEGIN", "BEGIN"),
    "END": Token("END", "END"),
    "DEFUN": Token("DEFUN", "DEFUN"),
    "ECHO": Token("ECHO", "ECHO"),
    "->": Token("ARROW", "->"),
    #"True": Token("BOOL", "True"),
    #"False": Token("BOOL", "False"),
    ":": Token("COLON", ":"),
    ";": Token("SEMI", ";"),
    ",": Token("COMMA", ","),
    "(": Token("LPAREN", "("),
    ")": Token("RPAREN", ")"),
    ":=": Token(OP, ":="),
    "||=": Token(OP, "||="),
    "+=": Token(OP, "+="),
    "*=": Token(OP, "*="),
    #"-=": Token(OP, "-="),
    "&": Token("OP", "&"),
    "|": Token("OP", "|"),
    "<>": Token("OP", "<>"),
    "=": Token("OP", "="),
    "IN": Token(OP, "<"),
    "<": Token(OP, "<"),
    "CONTAINS": Token(OP, ">"),
    ">": Token(OP, ">"),
    "+": Token(OP, "+"),
    "-": Token(OP, "-"),
    "||": Token("OP", "||"),
    "*": Token(OP, "*"),
    "!": Token(OP, "!"),
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
    def peek(self, lookahead=1):
        peek_pos = self.pos + lookahead
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
    def _int(self):
        result = ""
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        return Token(INT, int(result.replace("_", "")))   
    def get_next_token(self):
        # tokenizer
        text = self.text
        while self.current_char == " " or self.current_char == "\n":
            self.advance()
        if self.pos >= len(text):
            return Token(EOF, None)
        while self.current_char is not None:
            # alphabetic RESERVED_KEYWORDS & ID
            if self.current_char.isdigit():
                return self._int()
            if self.current_char.isalnum():
                return self._id()
            # STR
            elif self.current_char == '"':
                self.advance()
                result = self._str()
                self.advance()
                return Token(STR, result)
            # all other two character operators, see RESERVED_KEYWORDS 
            elif self.current_char + (self.peek() or "") + (self.peek(2) or "") in RESERVED_KEYWORDS:
                cur = self.current_char + (self.peek() or "") + (self.peek(2) or "")
                self.advance()
                self.advance()
                self.advance()
                return RESERVED_KEYWORDS[cur]
            elif self.current_char + (self.peek() or "") in RESERVED_KEYWORDS:
                cur = self.current_char + (self.peek() or "")
                self.advance()
                self.advance()
                return RESERVED_KEYWORDS[cur]
            # All other one character operators, see RESERVED_KEYWORDS
            elif self.current_char in RESERVED_KEYWORDS:
                cur = self.current_char
                self.advance()
                return RESERVED_KEYWORDS[cur]
            self.error()
