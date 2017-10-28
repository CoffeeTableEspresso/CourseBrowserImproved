import pickle
# Token types
VAR, SET, ID, MC, SA, LPAREN, RPAREN, FIRST, REST, SEMI, EOF = "VAR", "SET", \
"ID", "MC", "SA", "LPAREN", "RPAREN", "FIRST", "REST", "SEMI", "EOF"
IF, THEN, ELSE, FI = "IF", "THEN", "ELSE", "FI"
ISEMPTY = "ISEMPTY"
DEFUN, COLON, ARROW, COMMA, DOT, AT = "DEFUN", "COLON", "ARROW", "COMMA", "DOT", "AT"
# Data types

OP = "OP"
STR = "STR"
SELECT, FROM, WHERE, IN = "SELECT", "FROM", "WHERE", "IN"
STAR = "STAR"
LIST = "LIST"

TYPES = ["COURSE", "DEPT", "YEAR"]
# Course Operators
OPS = ["ttl", "dsc", "pr", "po", "co", "i", "rl", "tr", "gr"]
# list of depts.
DEPTS = ['AANB', 'ACAM', 'ADHE', 'AFST', 'AGEC', 'ANAT', 'ANSC', 'ANTH',
         'APBI', 'APPP', 'APSC', 'ARBC', 'ARC', 'ARCH', 'ARCL', 'ARST',
         'ARTH', 'ARTS', 'ASIA', 'ASIC', 'ASLA', 'ASTR', 'ASTU', 'ATSC',
         'AUDI', 'BA', 'BAAC', 'BABS', 'BAEN', 'BAFI', 'BAHC', 'BAHR',
         'BAIM', 'BAIT', 'BALA', 'BAMA', 'BAMS', 'BAPA', 'BASC', 'BASD',
         'BASM', 'BATL', 'BAUL', 'BIOC', 'BIOF', 'BIOL', 'BIOT', 'BMEG',
         'BOTA', 'BRDG', 'BUSI', 'CAPS', 'CCFI', 'CCST', 'CDST', 'CEEN',
         'CELL', 'CENS', 'CHBE', 'CHEM', 'CHIL', 'CHIN', 'CICS', 'CIVL',
         'CLCH', 'CLST', 'CNPS', 'CNRS', 'CNTO', 'COEC', 'COGS', 'COHR',
         'COMM', 'COMR', 'CONS', 'CPEN', 'CPSC', 'CRWR', 'CSIS', 'CSPW',
         'CTLN', 'DANI', 'DENT', 'DERM', 'DES', 'DHYG', 'DMED', 'DSCI',
         'ECED', 'ECON', 'ECPS', 'EDCP', 'EDST', 'EDUC', 'EECE', 'ELEC',
         'ELI', 'EMBA', 'ENDS', 'ENGL', 'ENPH', 'ENPP', 'ENVR', 'EOSC',
         'EPSE', 'ETEC', 'EXCH', 'EXGR', 'FACT', 'FEBC', 'FHIS', 'FIPR',
         'FISH', 'FIST', 'FMPR', 'FMST', 'FNEL', 'FNH', 'FNIS', 'FOOD',
         'FOPR', 'FRE', 'FREN', 'FRSI', 'FRST', 'FSCT', 'GBPR', 'GEM',
         'GENE', 'GEOB', 'GEOG', 'GERM', 'GPP', 'GREK', 'GRS', 'GRSJ',
         'GSAT', 'HEBR', 'HESO', 'HGSE', 'HINU', 'HIST', 'HPB', 'HUNU',
         'IAR', 'IEST', 'IGEN', 'INDE', 'INDO', 'INDS', 'INFO', 'ISCI',
         'ITAL', 'ITST', 'IWME', 'JAPN', 'JRNL', 'KIN', 'KORN', 'LAIS',
         'LARC', 'LASO', 'LAST', 'LATN', 'LAW', 'LFS', 'LIBE', 'LIBR',
         'LING', 'LLED', 'LWS', 'MATH', 'MDVL', 'MECH', 'MEDD', 'MEDG',
         'MEDI', 'MGMT', 'MICB', 'MIDW', 'MINE', 'MRNE', 'MTRL', 'MUSC',
         'NAME', 'NEST', 'NEUR', 'NRSC', 'NURS', 'OBMS', 'OBST', 'OHS',
         'ONCO', 'OPTH', 'ORNT', 'ORPA', 'OSOT', 'PAED', 'PATH', 'PCTH',
         'PERS', 'PHAR', 'PHIL', 'PHRM', 'PHTH', 'PHYL', 'PHYS', 'PLAN',
         'PLNT', 'POLI', 'POLS', 'PORT', 'PSYC', 'PSYT', 'PUNJ', 'RADI',
         'RELG', 'RES', 'RGLA', 'RHSC', 'RMST', 'RSOT', 'RUSS', 'SANS',
         'SCAN', 'SCIE', 'SEAL', 'SGES', 'SLAV', 'SOAL', 'SOCI', 'SOIL',
         'SOWK', 'SPAN', 'SPHA', 'SPPH', 'STAT', 'STS', 'SURG', 'SWED',
         'TEST', 'THTR', 'TIBT', 'TRSC', 'UDES', 'UFOR', 'UKRN', 'URO',
         'URST', 'URSY', 'VANT', 'VGRD', 'VISA', 'VRHC', 'VURS', 'WOOD',
         'WRDS', 'WRIT', 'ZOOL']
# list of years
YEARS = ["0th", "1st", "2nd", "3rd", "4th", "5th", "6th"]


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
    "IN": Token(OP, "IN")
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
        if result in DEPTS: return Token(DEPT, result)
        elif result in OPS: return Token(OP, result)
        elif result in YEARS: return Token(YEAR, result)
        elif result in TYPES: return Token(TYPE, result)
        elif len(result) >= 4 and not result.isalpha(): return Token(COURSE, result)
        else: return RESERVED_KEYWORDS.get(result, Token(ID, result))
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
            if self.current_char.isalnum():
                return self._id()
            # RESERVED_KEYWORDS & COURSE
            elif self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")
            elif self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")
            elif self.current_char == ":":
                self.advance()
                return Token(COLON, ":")
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
            elif self.current_char == ".":
                self.advance()
                return Token(DOT, ".")
        self.error()



###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):
    pass
#TODO: add TriOp
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
class Course(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class Dept(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class Year(AST):
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
class IfThenElse(AST):
    def __init__(self, cond, then_block, else_block):
        self.cond = cond
        self.then_block = then_block
        self.else_block = else_block
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
        return self.select_statement()
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
            return Token(LIST, []) # TODO: find better placeholder for STAR
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
        return Column(token)
    def cond(self):
        first = self.current_token
        self.eat(STR)
        self.eat(OP)
        column = self.column()
        return BinOp(Token(OP, IN), first, column)
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

# TODO: VAR can only declare nested lists one layer deep.

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

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.scope = None # TODO: fix this
    def visit_TriOp(self, node):
        pass # TODO: fix this
    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_UnOp(self, node):
        self.visit(node.expr)
    def visit_NulOp(self, node):
        pass
    def visit_Course(self, node):
        pass
    def visit_Dept(self, node):
        pass
    def visit_Year(self, node):
        pass
    def visit_DB(self, node):
        db_name = node.value
        db_symbol = self.scope.lookup(db_name)
        if db_symbol is None:
            raise NameError(repr(db_name))
    def visit_IfThenElse(self, node):
        self.visit(node.cond)
        self.visit(node.then_block)
        self.visit(node.else_block)
    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.scope.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
    def visit_FuncDecl(self, node):
        #self.visit(node.block)
        pass
    def visit_FuncCall(self, node):
        for param in node.params:
            self.visit(param)
    def visit_Decl(self, node):
        type_name = node.left.value
        type_symbol = self.scope.lookup(type_name)
        var_name = node.right.value
        var_symbol = VarSymbol(var_name, type_symbol)
        if self.scope.lookup(var_name, True):
            raise Exception("Error: Duplicate identifier %s found" % var_name)
        self.scope.insert(var_symbol)
    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.scope.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
        self.visit(node.right)

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
                    #store value
                #visit cond node
                # do stuff
                #remove valuesre


                #if node.right != None and node.right.op.value == IN:
                #    if node.right.left.value in getattr(d, node.right.right.value):
                #        for col in node.left.value:
                #            print getattr(d, col.value)
                        print "-"*80
    def visit_BinOp(self, node):
        return "SA: Year %s for %s" % (self.visit(node.left), self.visit(node.right))
    def visit_UnOp(self, node):
        def multiply(first, second):
            #TODO: doesn't work for nested lists yet
            def get(op, name):
                return "%s: %s" % (name.upper(), op.lower())
            result = Token(LIST, [])
            if first.type != LIST and second.type != LIST:
                result.value.append(Token(STR, get(first.value, second.value)))
            elif first.type == LIST:
                for element in first.value:
                    result.value.append(multiply(element, second))
            elif second.type == LIST:
                for element in second.value:
                    result.value.append(Token(STR, get(first.value, self.visit(element).value)))
            return result
        if node.op.type == OP:
            return multiply(node.token, self.visit(node.expr))
        elif node.op.type == REST:
            tmp = Token(LIST, [])
            for element in self.visit(node.expr).value[1:]:
                tmp.value.append(element)
            return tmp
        elif node.op.type == FIRST:
            result = self.visit(node.expr.value[0])
            return result
        elif node.op.type == ISEMPTY:
            if len(self.visit(node.expr).value) == 0:
                return Token(BOOL, True)
            else:
                return Token(BOOL, False)
        else:
            error()
    def visit_NulOp(self, node):
        return "MC TEXT"
    def visit_Course(self, node):
        if node.token.type == LIST:
            result = Token(LIST, [])
            for element in node.value:
                result.value.append(element)
            return result
        else:
            return node.token
    def visit_Dept(self, node):
        return node.token
    def visit_Year(self, node):
        return node.token
    def visit_IfThenElse(self, node):
        if self.visit(node.cond).value == True:
            return self.visit(node.then_block)
        else: return self.visit(node.else_block)
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
        if result.type == LIST:
            temp = Token(LIST, [])
            for element in result.value:
                temp.value.append(self.visit(element))
            #result = Token(LIST, [self.visit(element) for element in result.value])
            self.mem.insert(var_name, temp)
        else: self.mem.insert(var_name, result)
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
