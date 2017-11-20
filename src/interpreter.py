from tokens import *
from ast import *
from parser import Parser
from lexer import Lexer
import pickle
import os

# TODO: decide if short circuit
EVAL = {
        "<": (lambda x,y : x.upper() in y.upper()),
        ">": (lambda x,y : y.upper() in x.upper()),
        "*": (lambda x,y: x * y),
        "||": (lambda x,y : x + y),
        "+": (lambda x,y : x + y),
        "-": (lambda x,y : x - y),
        "=": (lambda x,y : x == y),
        "<>": (lambda x,y : x != y),
        "&": (lambda x,y : x and y), 
        "|": (lambda x,y : x or y),
       } 

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
        # self.insert(BuiltinTypeSymbol("DB"))
        # self.insert(BuiltinTypeSymbol("COURSE"))
        # self.insert(BuiltinTypeSymbol("DEPT"))
        # self.insert(BuiltinTypeSymbol("YEAR"))
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
        self._mem["Courses"] = Stack().push(pickle.load(open(os.path.join(os.path.dirname(__file__), "Courses.db"))))
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
        self.mem = Memory()
    def visit_TriOp(self, node):
        if node.op.type == SELECT:
            db = self.visit(node.middle)
            for d in db:
                for pair in d.__dict__.items():
                    self.mem.insert(pair[0], pair[1])
                if not node.right or self.visit(node.right):
                    cols = node.left # TODO: make sure this works for large DB
                    if node.left == "*":
                        cols = [Var(Token(ID, pair[0])) for pair in d.__dict__.items()]
                        cols.reverse()
                    for col in cols:
                        print self.visit(col)
                    print "-"*80
                for pair in d.__dict__.items():
                    self.mem.delete(pair[0])
        elif node.op.value == "?:":
            cond = self.visit(node.left)
            assert type(cond) is bool
            if cond:
                return self.visit(node.middle)
            else:
                return self.visit(node.right)
    def visit_BinOp(self, node):
        if node.op.type == WHILE:
            def true_bool(b):
                assert type(b) is bool
                return b
            while true_bool(self.visit(node.left)):
                self.visit(node.right)
            return    
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op.value in ["=", "<>"]:
            pass
        elif node.op.value in ["+", "*", "-"]:
            assert type(left) is type(right) is int
        elif node.op.value in ["<", ">", "||"]: # TODO: update this so IN and CONTAINS are handled by same condition in visit_BinOp
            assert type(left) is type(right) is str
        else:
            assert type(left) is type(right) is bool
        return EVAL[node.op.value](left, right)
    def visit_UnOp(self, node):
        if node.op.type == BEGIN:
            if len(node.expr.value) == 0:
                return None
            else:
                for innernode in node.expr.value[:-1]:
                    self.visit(innernode)
                return self.visit(node.expr.value[-1])
        elif node.op.type == ECHO:
            val = self.visit(node.expr)
            print val
            return val
        elif node.op.value == "!":
            val = self.visit(node.expr)
            assert type(val) is bool
            return not val
        elif node.op.value == "-":
            val = self.visit(node.expr)
            assert type(val) is int
            return -val
        elif node.op.value == "+":
            val = self.visit(node.expr)
            assert type(val) is int
            return val
        #elif node.op.value == "++":
        #   val = self.visit(node.expr)
        #   assert type(val) is int
        #   self.mem.insert(node.expr.value, val+1)
        #elif node.op.value == "--":
        #   val = self.visit(node.expr)
        #   assert type(val) is int
        #   self.mem.insert(node.expr.value, val-1)
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
    def visit_Boolean(self, node):
        return node.value
    def visit_Integer(self, node):
        return node.value
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

