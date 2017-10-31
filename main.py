import pickle
# Token types
VAR, SET, ID, MC, SA, LPAREN, RPAREN, FIRST, REST, SEMI, EOF = "VAR", "SET", \
"ID", "MC", "SA", "LPAREN", "RPAREN", "FIRST", "REST", "SEMI", "EOF"
DEFUN, COLON, ARROW, COMMA, DOT, AT = "DEFUN", "COLON", "ARROW", "COMMA", "DOT", "AT"
# Data types

OP = "OP"
STR = "STR"
SELECT, FROM, WHERE, IN = "SELECT", "FROM", "WHERE", "IN"
CONTAINS = "CONTAINS"
STAR = "STAR"
EQUALS = "EQUALS"
LIST = "LIST"


###############################################################################
#                                                                             #
#   LEXER                                                                     #
#                                                                             #
###############################################################################

class Token(object):
    def __init__(self, token_type, token_value):
        # token types listed at top of file
        self.type = token_type
        # token values: e.g. MATH412
        self.value = token_value
    def __str__(self):
        return "Token(%s, %s)" % (self.type, repr(self.value))
    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    "SELECT": Token("SELECT", "SELECT"),
    "FROM": Token("FROM", "FROM"),
    "WHERE": Token("WHERE", "WHERE"),
    "IN": Token(OP, "IN"),
    "CONTAINS": Token(OP, "CONTAINS"),
    "SET": Token("SET", "SET"),
    #"EQUALS": Token(OP, "=")
}


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
        #text = filter(None, text.replace("(", " ( ").replace(")", " ) ").replace(";", " ; ").split(" "))
        # reached end of text?
        while self.current_char == " ":
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
            #elif self.current_char == ":":
            #    self.advance()
            #    return Token(COLON, ":")
            elif self.current_char == '"':
                self.advance()
                result = self._str()
                self.advance()
                return Token(STR, result)
            #elif self.current_char == "-" and self.peek() == ">":
            #    self.advance()
            #    self.advance()
            #    return Token(ARROW, "->")
            elif self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")
            elif self.current_char == "*":
                self.advance()
                return Token(STAR, "*")
            elif self.current_char == "=":
                self.advance()
                return Token(OP, "=")
            #elif self.current_char == ".":
            #    self.advance()
            #    return Token(DOT, ".")
        self.error()



###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):
    pass
class TriOp(AST):
    def __init__(self, op, left, middle, right):
        self.left = left
        self.middle = middle
        self.right = right
        self.token = self.op = op
class BinOp(AST):
    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.token = self.op = op
class UnOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
class NulOp(AST):
    def __init__(self, op):
        self.token = self.op = op
class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class DB(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class Column(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class Param(AST):
    def __init__(self, var_node):
        self.node = var_node
class FuncDecl(AST):
    def __init__(self, token, params, block):
        self.token = token
        self.value = token.value
        self.params = params # list of formal params
        self.block = block
class FuncCall(AST):
    def __init__(self, token, params):
        self.token = token
        self.value = token.value
        self.params = params
class Decl(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right
class Assign(AST):
    def __init__(self, left, right):
        self.left = left  # ID
        self.right = right # val
class Var(AST):
    # ID Token is used here
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    def error(self,token_type):
        raise Exception("Expected %s Token at pos %s, got %s" % \
            (token_type, self.lexer.pos, self.current_token))
    def eat(self, token_type):
        #print self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)
    def statement(self):
        if self.current_token.type == SELECT:
            return self.select_statement()
        elif self.current_token.type == SET:
            return self.assign_var()
        else:
            self.error()
    def select_statement(self):
        self.eat(SELECT)
        columns = self.columns()
        self.eat(FROM)
        db = self.db()
        if self.current_token.type == WHERE:
            self.eat(WHERE)
            cond = self.cond()
        else:
            cond = None
        return TriOp(Token(SELECT, SELECT), columns, db, cond)
    def columns(self):
        # TODO: fix return values
        if self.current_token.type == STAR:
            self.eat(STAR)
            return Token(STAR, "*") # TODO: find better placeholder for STAR
        else:
            columns = []
            columns.append(self.column())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                columns.append(self.column())
            return Token(LIST, columns)
    def db(self):
        token = self.current_token
        self.eat(ID)
        return DB(token)
    def column(self):
        token = self.current_token
        self.eat(ID)
        return Var(token) #Column
    def cond(self):
        if self.current_token.type == STR:
            first = String(self.current_token)
            self.eat(STR)
        else:
            first = self.column()
        op = self.current_token
        self.eat(OP)
        if self.current_token.type == STR:
            second = String(self.current_token)
            self.eat(STR)
        else:
            second = self.column()
        return BinOp(op, first, second)
    def assign_var(self):
        self.eat(SET)
        var = Var(self.current_token)
        self.eat(ID)
        if self.current_token.value == "=":
            self.eat(OP)
        val = String(self.current_token) # TODO: case when current token is not STR
        self.eat(STR)
        return Assign(var, val)
    def parse(self):
        while self.current_token.type != EOF:
            result = self.statement()
            if self.current_token.type == SEMI:
                self.eat(SEMI)
            elif self.current_token.type != EOF:
                self.error(EOF)
        return result


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class Symbol(object):
    def __init__(self, name, stype=None):
        self.name = name
        self.type = stype
class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)
    def __str__(self):
        return self.name
    __repr__ = __str__
class VarSymbol(Symbol):
    def __init__(self, name, stype):
        super(VarSymbol, self).__init__(name, stype)
    def __str__(self):
        return "%s: %s" % (self.name, self.type)
    __repr__ = __str__
class FuncSymbol(Symbol):
    def __init__(self, name, params=None):
        super(FuncSymbol, self).__init__(name)
        self.params = params if params is not None else []
    def __str__(self):
        return "<%s(name=%s, parameters=%s)>" % (self.__class__.__name__, self.name, self.params)
    __repr__ = __str__

class ScopedSymbolTable(object):
    def __init__(self, name, level, parent=None):
        self._symbols = {}
        self.scope_name = name
        self.scope_level = level
        self.parent = parent
        self._init_builtins()
    def _init_builtins(self):
        self.insert(VarSymbol("Courses", "DB"))
        self.insert(BuiltinTypeSymbol("DB"))
        self.insert(BuiltinTypeSymbol("COURSE"))
        self.insert(BuiltinTypeSymbol("DEPT"))
        self.insert(BuiltinTypeSymbol("YEAR"))
    def __str__(self):
        return "Symbols: %s" % str([value for value in self._symbols.values()])
    __repr__ = __str__
    def insert(self, symbol):
        #print "Insert: %s" % symbol
        self._symbols[symbol.name] = symbol
    def lookup(self, name, cur_only=False):
        #print "Lookup: %s" % name
        symbol = self._symbols.get(name) # return Symbol | None
        if symbol is not None:
            return symbol
        if cur_only:
            return None
        if self.parent is not None:
            return self.parent.lookup(name)
        return None #not found


class Memory(object):
    def __init__(self):
        self._mem = {}
        self._mem["Courses"] = Stack().push(pickle.load(open("Courses.db")))
    def insert(self, key, value):
        #print "Insert: %s, %s" % (key, value)
        if key in self._mem.keys():
            self._mem.get(key).push(value)
        else:
            self._mem[key] = Stack().push(value)
    def get(self, key):
        #print "Lookup: %s, %s" % (key, self._mem[key].peek())
        return self._mem[key].peek()
    def delete(self, key):
        #print "Delete: %s, %s" % (key, self._mem[key].peek())
        self._mem[key].pop()
    def __str__(self):
        result = ""
        for key in self._mem.keys():
            result += "%s: %s\n" % (key, self._mem.get(key))
	return result
    __repr__ = __str__

class Stack(object):
    def __init__(self):
        self.stack = []
    def push(self, val):
        self.stack.append(val)
        return self
    def pop(self):
        tmp = self.stack[-1]
        self.stack = self.stack[:-1]
        return tmp
    def peek(self):
        return self.stack[-1]
    def __str__(self):
        result = ""
        for element in self.stack:
            result += ("\t%s\n" % element)
        return result
    __repr__ = __str__

class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception("No visit_%s method: %s" % (type(node).__name__, node))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.current_scope = ScopedSymbolTable("GLOBAL", 1)
        self.stb = SymbolTableBuilder()
        self.stb.scope = self.current_scope
        self.mem = Memory()
    def visit_TriOp(self, node):
        if node.op.type == SELECT:
            db = self.visit(node.middle)
            for d in db:
                for pair in d.__dict__.items():
                    self.mem.insert(pair[0], pair[1])
                if not node.right or self.visit(node.right):
                    for col in node.left.value: # TODO: update to handle SELECT * FROM ...
                        print self.visit(col)
                    print "-"*80
                for pair in d.__dict__.items():
                    self.mem.delete(pair[0])
    def visit_BinOp(self, node):
        if node.op.value == "IN":
            return self.visit(node.left) in self.visit(node.right)
        elif node.op.value == "CONTAINS":
            return self.visit(node.right) in self.visit(node.left)
        elif node.op.value == "=":
            return self.visit(node.left) == self.visit(node.right)
    #def visit_UnOp(self, node):
    #    def multiply(first, second):
    #   pass
    #def visit_NulOp(self, node):
    #   return "MC TEXT"
    def visit_FuncDecl(self, node):
        self.mem.insert(node.value, (node.params, node.block))
    def visit_FuncCall(self, node):
        func = self.mem.get(node.value)
        for i in range(0, len(func[0])):
            self.mem.insert(func[0][i].value, self.visit(node.params[i]))
        tmp = self.visit(func[1])
        for i in range(0, len(func[0])):
            self.mem.delete(func[0][i].value)
        return tmp
    def visit_Decl(self, node):
        pass
    def visit_Assign(self, node):
        var_name = node.left.value
        result = self.visit(node.right)
        self.mem.insert(var_name, result)
        return self.mem.get(var_name)
    def visit_Var(self, node):
        var_name = node.value
        val = self.mem.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val
    def visit_DB(self, node):
        db_name = node.value
        val = self.mem.get(db_name)
        if val is None:
            raise NameError(repr(db_name))
        else:
            return val
    def visit_String(self, node):
        return node.value
    def interpret(self):
        tree = self.parser.parse()
        self.stb.visit(tree)
        return self.visit(tree)


def main():
    interpreter = Interpreter("")
    while True:
        try:
            text = raw_input(">>> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter.parser = parser # = Interpreter(parser)
        result = interpreter.interpret()
        print result

if __name__ == "__main__":
    main()
